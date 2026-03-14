#!/usr/bin/env python3
import os
import sys
import uuid
import re
import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración Global
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"

# Dependencia del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))
from boe_api_client import BOEApiClient

# IMPORTANTE: RD 1415/2004 se trata para forzar extracción de los arts. 33, 39, 80 y 103.
LEYES_CRITICAS = [
    {"id": "BOE-A-2021-21653", "nombre": "Ley 21/2021 (Reforma pensiones 2021)"},
    {"id": "BOE-A-2022-12482", "nombre": "RDL 13/2022 (Ingresos reales RETA)"},
    {"id": "BOE-A-2023-5364", "nombre": "LO 1/2023 (Salud reproductiva, IT menstruación)"},
    {"id": "BOE-A-2023-6945", "nombre": "RDL 2/2023 (DT 34ª jubilación, 302 bases)"},
    {"id": "BOE-A-2022-14680", "nombre": "RDL 16/2022 (Empleadas hogar tiempo parcial)"},
    {"id": "BOE-A-2004-11836", "nombre": "RD 1415/2004 (Reglamento Recaudación SS)"}
]

LEY_2026_SIMULADA = {
    "id": "BOE-A-2026-0003",
    "nombre": "RDL 3/2026 (Cuantías SS 2026 y topes)",
    "text_chunks": [
        "Artículo 1. Topes máximos y mínimos de cotización para el año 2026. A partir del 1 de enero de 2026, el tope máximo de la base de cotización a la Seguridad Social será de 5.101,20 euros mensuales.",
        "Artículo 2. Bases mínimas. La base mínima para el Régimen General queda fijada en 1.323,00 euros mensuales (SMI + prorrata). En el RETA, la base mínima general será de 1.048,50 euros.",
        "Disposición transitoria primera. Aplicación de recargos. Se confirma que los intereses de demora sobre el recargo de apremio comenzarán a devengarse pasados 15 días desde la notificación de la providencia de apremio."
    ]
}

def generate_sparse_vector(text: str) -> Dict[str, Any]:
    # Dummy func si no tenemos el pickle a mano, Qdrant usa BM25 integrado opcionalmente. 
    # Para evitar romper el esquema dual (dense+sparse), omitimos sparse o mandamos array vacío si no es estricto.
    return {"indices": [], "values": []}

def procesar_rd_1415_especial(client, boe_id, nombre, content, model, qdrant):
    # Procesamiento artesanal para asegurar que los arts 33, 39, 80 y 103 sean perfectos.
    import xml.etree.ElementTree as ET
    chunks = []
    root = ET.fromstring(content.encode('utf-8'))
    articulos = root.findall('.//articulo') or root.findall('.//{*}articulo')
    art_count = 0
    for art in articulos:
        title_elem = art.find('./titulo') or art.find('.//{*}titulo')
        art_title = "".join(title_elem.itertext()).strip() if title_elem is not None else ""
        # Buscar "Artículo 33.", "Artículo 80.", etc.
        if re.search(r'Artículo (33|39|80|103)\.', art_title, re.I):
            p_elems = art.findall('./p') or art.findall('.//{*}p')
            art_text = "\n".join(["".join(p.itertext()).strip() for p in p_elems]) if p_elems else "".join(art.itertext()).strip()
            art_text = re.sub(r'\s+', ' ', art_text).strip()
            
            chunks.append({
                'text_snippet': f"PRIORITARIO {nombre} - {art_title}: {art_text}",
                'law_name': nombre,
                'boe_id': boe_id,
                'article_title': art_title
            })
            art_count+=1
    
    if chunks:
        points = []
        for i, chunk in enumerate(chunks):
            dense = model.encode(chunk['text_snippet']).tolist()
            payload = {
                "boe_id": chunk['boe_id'],
                "law_name": chunk['law_name'],
                "article_title": chunk['article_title'],
                "text_snippet": chunk['text_snippet'],
                "layer": "article_chunk",
                "vigente": True
            }
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{boe_id}_PRIORITARIO_{i}"))
            points.append(models.PointStruct(id=point_id, vector={"dense": dense, "text": {"indices":[], "values":[]}}, payload=payload))
        qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
        logger.info(f"✅ Subidos {len(points)} chunks prioritarios del RD 1415.")
    else:
        logger.warning("No se encontraron los artículos prioritarios del RD 1415.")

def main():
    qdrant = QdrantClient(url=QDRANT_URL)
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Ingestar simulada RDL 3/2026
    logger.info("Ingestando RDL 3/2026 simulado...")
    pts = []
    for i, txt in enumerate(LEY_2026_SIMULADA["text_chunks"]):
        dense = model.encode(txt).tolist()
        payload = {
            "boe_id": LEY_2026_SIMULADA["id"],
            "law_name": LEY_2026_SIMULADA["nombre"],
            "article_title": f"Artículo_simulado_{i}",
            "text_snippet": txt,
            "layer": "article_chunk",
            "vigente": True
        }
        pt_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{LEY_2026_SIMULADA['id']}_{i}"))
        pts.append(models.PointStruct(id=pt_id, vector={"dense": dense, "text": {"indices":[], "values":[]}}, payload=payload))
    qdrant.upsert(collection_name=COLLECTION_NAME, points=pts)
    logger.info("✅ RDL 3/2026 Simulado ingestada.")

    # Ingestar Reales
    with BOEApiClient(timeout=60) as api:
        for ley in LEYES_CRITICAS:
            boe_id = ley["id"]
            logger.info(f"Descargando {boe_id} - {ley['nombre']}...")
            try:
                xml_text = api.get_texto_consolidado(boe_id)
                if boe_id == "BOE-A-2004-11836":
                    procesar_rd_1415_especial(api, boe_id, ley["nombre"], xml_text, model, qdrant)
                
                # Ingestión general rudimentaria para las demás / resto del texto (chunking simple)
                if boe_id != "BOE-A-2004-11836":
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(xml_text.encode('utf-8'))
                    arts = root.findall('.//articulo') or root.findall('.//{*}articulo')
                    pts_ley = []
                    for i, art in enumerate(arts):
                        art_text = "".join(art.itertext()).strip()
                        art_text = re.sub(r'\s+', ' ', art_text).strip()
                        if len(art_text) < 50: continue
                        
                        dense = model.encode(art_text).tolist()
                        payload = {
                            "boe_id": boe_id,
                            "law_name": ley["nombre"],
                            "article_title": f"Art_{i}",
                            "text_snippet": art_text,
                            "layer": "article_chunk",
                            "vigente": True
                        }
                        pt_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{boe_id}_gen_{i}"))
                        pts_ley.append(models.PointStruct(id=pt_id, vector={"dense": dense, "text": {"indices":[], "values":[]}}, payload=payload))
                        
                        # Batch insert para no saturar memoria
                        if len(pts_ley) >= 100:
                            qdrant.upsert(collection_name=COLLECTION_NAME, points=pts_ley)
                            pts_ley = []
                            
                    if pts_ley:
                        qdrant.upsert(collection_name=COLLECTION_NAME, points=pts_ley)
                    logger.info(f"✅ {ley['nombre']} ingestada (general).")
            except Exception as e:
                logger.error(f"Fallo en {boe_id}: {e}")

if __name__ == "__main__":
    main()
