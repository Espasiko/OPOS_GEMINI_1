#!/usr/bin/env python3
import sys
import os
import json
import logging
from pathlib import Path
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http import models

# Configuración y paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT / "backend"))

# Imports desde el backend
from agents.boe_api_client import BOEApiClient
from utils.analizador_legal import analizar_metadatos_legales
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
JSON_DIR = PROJECT_ROOT / "data" / "boe_xml"

BASURA = [
    "BOE-A-1982-9050", "BOE-A-1985-22915", "BOE-A-1988-9526", "BOE-A-1995-2081",
    "BOE-A-1995-24156", "BOE-A-2001-20795", "BOE-A-2006-16891", "BOE-A-2006-19348",
    "BOE-A-2008-17156", "BOE-A-2009-3780", "BOE-A-2009-5693", "BOE-A-2020-6898",
    "BOE-A-2022-7260", "BOE-A-2023-25411", "BOE-A-2023-6945", "BOE-A-2011-15673", 
    "BOE-A-2020-2047", "BOE-A-1995-10652", "BOE-A-1995-10653", "BOE-A-2010-1172"
]

REEMPLAZOS = [
    {"id": "BOE-A-2023-6967", "nombre": "RDL 2/2023 (Pensiones y DT 34)", "prioridad": "CRÍTICA"},
    {"id": "BOE-A-2011-15936", "nombre": "Ley 36/2011 (Jurisdicción Social)", "prioridad": "ALTA"},
    {"id": "BOE-A-2020-1246", "nombre": "RD 139/2020 (Estructura Orgánica AGE)", "prioridad": "ALTA"},
    {"id": "BOE-A-1995-8729", "nombre": "RD 364/1995 (Ingreso Personal Administración AGE)", "prioridad": "ALTA"},
    {"id": "BOE-A-1995-8730", "nombre": "RD 365/1995 (Situaciones Administrativas AGE)", "prioridad": "ALTA"},
    {"id": "BOE-A-2010-1331", "nombre": "RD 4/2010 (Esquema Nacional Interoperabilidad ENI)", "prioridad": "ALTA"}
]

# Chunking helper directly inline
def chunk_text(text: str, max_chars: int = 1500) -> List[str]:
    import re
    chunks = []
    current_chunk = []
    current_length = 0
    # Dividir por párrafos groseros
    paragraphs = re.split(r'\n\s*\n', text)
    for p in paragraphs:
        if current_length + len(p) > max_chars and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [p]
            current_length = len(p)
        else:
            current_chunk.append(p)
            current_length += len(p)
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
    return chunks

def ingestar():
    client = QdrantClient(url=QDRANT_URL)
    
    logger.info("=========================================")
    logger.info("1. PURGANDO LEYES BASURA DEL RAG")
    logger.info("=========================================")
    for bad_id in BASURA:
        try:
            client.delete(
                collection_name=COLLECTION_NAME,
                points_selector=models.Filter(
                    must=[models.FieldCondition(key="boe_id", match=models.MatchValue(value=bad_id))]
                )
            )
            logger.info(f"✅ Eliminado de Qdrant: {bad_id}")
        except Exception as e:
            logger.error(f"Error borrando {bad_id}: {e}")

    logger.info("=========================================")
    logger.info("2. INGESTANDO LEYES OFICIALES CORREGIDAS")
    logger.info("=========================================")
    
    boe_api = BOEApiClient(timeout=20)
    logger.info(f"Cargando modelo de embeddings {EMBEDDING_MODEL} (1200+ dim)")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    for ley in REEMPLAZOS:
        boe_id = ley["id"]
        law_name = ley["nombre"]
        
        # 1. Bajar texto y meta
        logger.info(f"🔍 Evaluando: {law_name} ({boe_id})")
        
        texto_norma = ""
        meta_dict = {}
        
        # Intento consolidado JSON primero
        try:
            consol = boe_api.get_legislacion_consolidada(boe_id, formato="json")
            if isinstance(consol, dict) and "data" in consol:
                meta_dict = consol.get("data", {}).get("documento", {})
            elif isinstance(consol, list) and len(consol) > 0:
                meta_dict = consol[0].get("documento", {}) if isinstance(consol[0], dict) else {}
        except Exception as e:
            logger.warning(f"  Fallo consolidado JSON para {boe_id}, bajando original...")
        
        # Intentar XML oficial si meta_dict "texto" no está bien formateado
        try:
            texto_norma = boe_api.get_ley_text(boe_id)
        except Exception as e:
            logger.warning(f"  No hay texto vía XML: {e}")
            texto_norma = ""
            
        if not texto_norma and getattr(boe_api, 'descargar_ley_html', None):
            logger.info(f"  Intentando scrape HTML pasivo...")
            try:
                texto_norma = boe_api.descargar_ley_html(boe_id)
            except Exception as e:
                logger.error(f"  Fallo también el HTML para {boe_id}")

        if not texto_norma:
             # si en consol json estaba el texto
             t = meta_dict.get("texto", "")
             if t:
                 texto_norma = t
             else:
                 logger.error(f"❌ Imposible obtener texto para {boe_id}. Omisiones críticas.")
                 continue
                 
        # 2. Análisis legal para metadatos (vigencia, afectaciones)
        logger.info(f"  Analizando metadatos legales para {boe_id} (Length: {len(texto_norma)})")
        legal_meta = analizar_metadatos_legales(boe_id, texto_norma)
        
        # Enriquecer legal_meta
        legal_meta["ley"] = law_name
        legal_meta["prioridad"] = ley["prioridad"]
        
        # 3. Chunking
        frisson = chunk_text(texto_norma, 1500)
        logger.info(f"  Generados {len(frisson)} chunks.")
        
        # 4. Embeddings e ingesta
        points = []
        import uuid
        for i, ck in enumerate(frisson):
            emb = model.encode(ck, normalize_embeddings=True).tolist()
            payload = {
                "boe_id": boe_id,
                "law_name": law_name,
                "texto": ck,
                "chunk_index": i,
                "total_chunks": len(frisson),
                **legal_meta
            }
            points.append(
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=emb,
                    payload=payload
                )
            )
            
            if len(points) >= 50:
                client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=points
                )
                points = []
                
        if points:
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=points
            )
        
        logger.info(f"✅ Ingesta completa para {law_name} ({boe_id}) - {len(frisson)} puntos")

if __name__ == "__main__":
    ingestar()
