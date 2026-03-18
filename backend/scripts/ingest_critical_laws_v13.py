#!/usr/bin/env python3
import os
import json
import logging
import argparse
import re
import uuid
import sys
import pickle
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Dependencias
try:
    from qdrant_client import QdrantClient, models
    from sentence_transformers import SentenceTransformer
    import httpx
except ImportError as e:
    logger.error(f"❌ Error importando dependencias: {e}")
    sys.exit(1)

# CONFIGURACIÓN DE RUTAS
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT / "backend"))

from agents.boe_api_client import BOEApiClient

# CONFIGURACIÓN GLOBAL
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"
QDRANT_URL = "http://localhost:6333"
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
BM25_VOCAB_FILE = PROJECT_ROOT / "backend" / "data" / "bm25_vocab.pkl"

CRITICAL_LAWS = [
    {"id": "BOE-A-2021-21652", "nombre": "Ley 21/2021 de garantía del poder adquisitivo de las pensiones", "ley_id": "ley_21_2021", "bloque": "BLOQUE 5", "cuerpos": ["c1_ss", "a2_ss"]},
    {"id": "BOE-A-2022-12482", "nombre": "RDL 13/2022 Nuevo sistema de cotización para autónomos (Ingresos Reales)", "ley_id": "rdl_13_2022", "bloque": "BLOQUE 5", "cuerpos": ["c1_ss", "a2_ss"]},
    {"id": "BOE-A-2023-5364", "nombre": "LO 1/2023 Salud sexual y reproductiva (IT Menstruación)", "ley_id": "lo_1_2023", "bloque": "BLOQUE 5", "cuerpos": ["c1_ss", "a2_ss"]},
    {"id": "BOE-A-2023-6967", "nombre": "RDL 2/2023 Medidas urgentes para la ampliación de derechos de los pensionistas", "ley_id": "rdl_2_2023", "bloque": "BLOQUE 5", "cuerpos": ["c1_ss", "a2_ss"]},
    {"id": "BOE-A-2022-14680", "nombre": "RDL 16/2022 Mejora condiciones trabajadoras del hogar", "ley_id": "rdl_16_2022", "bloque": "BLOQUE 5", "cuerpos": ["c1_ss", "a2_ss"]},
    {"id": "BOE-A-2004-11836", "nombre": "RD 1415/2004 Reglamento General de Recaudación de la Seguridad Social", "ley_id": "rd_1415_2004", "bloque": "BLOQUE 4", "cuerpos": ["c1_ss", "a2_ss"]}
]

_MODEL = None
_BM25 = None

def get_embedding_model():
    global _MODEL
    if _MODEL is None: _MODEL = SentenceTransformer(EMBEDDING_MODEL)
    return _MODEL

def get_bm25_vocab():
    global _BM25
    if _BM25 is None:
        if BM25_VOCAB_FILE.exists():
            with open(BM25_VOCAB_FILE, 'rb') as f: _BM25 = pickle.load(f)
            if isinstance(_BM25, dict) and 'vocab' not in _BM25:
                _BM25 = {'vocab': _BM25, 'avgdl': 38.0}
        else: _BM25 = {'vocab': {}, 'avgdl': 38.0}
    return _BM25

def tokenize_legal(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r'[^a-záéíóúñ0-9]+', ' ', text)
    return [t for t in text.split() if len(t) > 2]

def generate_sparse_vector(text: str) -> Dict[str, Any]:
    vocab_data = get_bm25_vocab()
    vocab = vocab_data['vocab']
    avgdl = vocab_data.get('avgdl', 38.0)
    tokens = tokenize_legal(text)
    doc_len = len(tokens)
    if not tokens: return {"indices": [], "values": []}
    counts = {}
    for t in tokens:
        if t in vocab:
            idx = vocab[t]
            counts[idx] = counts.get(idx, 0) + 1
    indices = []; values = []
    k1, b = 1.2, 0.75
    for idx, f in counts.items():
        score = f * (k1 + 1) / (f + k1 * (1 - b + b * doc_len / avgdl))
        indices.append(idx); values.append(float(score))
    sorted_pairs = sorted(zip(indices, values))
    return {"indices": [p[0] for p in sorted_pairs], "values": [p[1] for p in sorted_pairs]}

def parsear_referencias(nodo_referencias):
    if not nodo_referencias: return []
    lista = []
    refs = nodo_referencias.get("referencia", [])
    if isinstance(refs, dict): refs = [refs]
    for r in refs:
        texto = r.get("texto", "")
        palabra = r.get("palabra", "")
        if palabra and texto: lista.append(f"{palabra} {texto}")
        elif texto: lista.append(texto)
    return lista

def parsear_materias(nodo_materias):
    if not nodo_materias: return []
    lista = []
    mats = nodo_materias.get("materia", [])
    if isinstance(mats, dict): mats = [mats]
    if isinstance(mats, str): mats = [mats]
    for m in mats:
        if isinstance(m, str): lista.append(m)
        elif isinstance(m, dict) and "texto" in m: lista.append(m["texto"])
    return lista

def extract_article_number(title: str) -> str:
    m = re.search(r'(?:Artículo|Art\.|Art)\s*(\d+(?:\.\d+)?)', title, re.I)
    return m.group(1) if m else ""

def find_sentence_boundary(text: str, position: int, direction: str = "forward") -> int:
    """Busca el fin de frase más cercano a la posición dada."""
    sentence_endings = ['. ', '.\n', '? ', '?\n', '! ', '!\n', ':\n', ')\n']
    if direction == "forward":
        search_range = range(position, min(position + 100, len(text)))
        for i in search_range:
            for ending in sentence_endings:
                if text[i:i+len(ending)] == ending:
                    return i + len(ending)
        return min(position + 50, len(text))
    else:
        search_range = range(position, max(position - 100, 0), -1)
        for i in search_range:
            for ending in sentence_endings:
                if i >= len(ending) and text[i-len(ending)+1:i+1] == ending:
                    return i + 1
        return max(position - 50, 0)

def chunk_text_with_overlap(text: str, chunk_size: int = 800, overlap: int = 150) -> List[Tuple[str, int]]:
    """Divide texto en chunks con solapamiento, respetando límites de oraciones."""
    if len(text) <= chunk_size:
        return [(text, 0)]
    chunks = []
    start = 0
    chunk_index = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunk = text[start:].strip()
            if len(chunk) > 50:
                chunks.append((chunk, chunk_index))
            break
        boundary = find_sentence_boundary(text, end, "forward")
        chunk = text[start:boundary].strip()
        if len(chunk) > 50:
            chunks.append((chunk, chunk_index))
            chunk_index += 1
        start = boundary - overlap
        if start < 0: start = 0
    return chunks

def ingest_laws(dry_run: bool = False):
    client = QdrantClient(url=QDRANT_URL, timeout=120)
    model = get_embedding_model()
    boe_api = BOEApiClient(timeout=60)
    
    total_p = 0
    for ley in CRITICAL_LAWS:
        boe_id = ley['id']
        nombre = ley['nombre']
        logger.info(f"👉 Inyectando {boe_id} ({nombre})...")
        
        # 1. Metadatos globales (JSON para facilidad de acceso)
        try:
            meta_resp = boe_api.get_metadatos(boe_id, formato="json")
            
            # Manejar caso de lista o diccionario
            if isinstance(meta_resp, list) and len(meta_resp) > 0:
                meta_json = meta_resp[0]
            elif isinstance(meta_resp, dict):
                meta_json = meta_resp
            else:
                meta_json = {}
                
            data_meta = meta_json.get("data", {}) if isinstance(meta_json, dict) else {}
            documento = data_meta.get("documento", {}) if isinstance(data_meta, dict) else {}
            metadatos_globales = documento.get("metadatos", {}) if isinstance(documento, dict) else {}
            analisis_global = documento.get("analisis", {}) if isinstance(documento, dict) else {}
            
            if not metadatos_globales and not analisis_global:
                # Reintentar extraer directamente del objeto meta_json si la estructura es distinta
                metadatos_globales = meta_json.get("documento", {}).get("metadatos", {}) if isinstance(meta_json, dict) else {}
                analisis_global = meta_json.get("documento", {}).get("analisis", {}) if isinstance(meta_json, dict) else {}

        except Exception as e:
            logger.error(f"  ❌ Error bajando metadatos para {boe_id}: {e}")
            continue
            
        # 2. Texto consolidado (XML para parseo por artículos y vigencias)
        try:
            texto_xml_raw = boe_api.get_texto_consolidado(boe_id)
            root = ET.fromstring(texto_xml_raw.encode('utf-8'))
        except Exception as e:
            logger.error(f"  ❌ Error bajando/parseando XML para {boe_id}: {e}")
            continue
            
        # Extract global fields for all points of this law
        materias = parsear_materias(analisis_global.get("materias", {}))
        ref_ant = parsear_referencias(analisis_global.get("referencias_anteriores", {}))
        ref_post = parsear_referencias(analisis_global.get("referencias_posteriores", {}))
        
        # Mapeo de referencias para coincidir con el payload extendido
        modificado_por = [r for r in ref_post if "modifica" in r.lower()]
        derogado_por = [r for r in ref_post if "deroga" in r.lower()]
        anadido_por = [r for r in ref_post if "añade" in r.lower()]
        
        global_payload = {
            "boe_id": boe_id,
            "law_name": nombre,
            "ley_id": ley.get("ley_id", ""),
            "bloque": ley.get("bloque", ""),
            "cuerpos": ley.get("cuerpos", []),
            "organismo_emisor": metadatos_globales.get("departamento", {}).get("_text", ""),
            "fecha_publicacion": metadatos_globales.get("fecha_publicacion", {}).get("_text", ""),
            "fecha_vigencia": metadatos_globales.get("fecha_vigencia", {}).get("_text", ""),
            "vigente": metadatos_globales.get("estatus", {}).get("_text", "") == "Vigente",
            "estatus_derogacion": metadatos_globales.get("estatus", {}).get("_text", ""),
            "rango": metadatos_globales.get("rango", {}).get("_text", ""),
            "materias": materias,
            "deroga_a": [r for r in ref_ant if "deroga" in r.lower()],
            "modificado_por": modificado_por,
            "derogado_por": derogado_por,
            "anadido_por": anadido_por,
            "url_boe": f"https://www.boe.es/buscar/act.php?id={boe_id}",
            "url_xml": f"https://www.boe.es/buscar/act.php?id={boe_id}&xml=1",
            "source": "ingest_v13_critical",
            "layer": "article_chunk",
            "consolidado": True,
            "estado_consolidacion": "Finalizado",
            "fecha_actualizacion_payload": datetime.now().isoformat()
        }
        
        # 3. Parsear artículos o bloques
        articulos_nodos = root.findall('.//articulo')
        usando_bloques = False
        if not articulos_nodos:
            articulos_nodos = root.findall('.//bloque')
            usando_bloques = True
            
        points = []
        for i, node in enumerate(articulos_nodos):
            if usando_bloques:
                # Filtrar bloques que no son contenido (pueden ser divisiones, etc.)
                tipo = node.get('tipo', '')
                if tipo not in ('precepto', 'preambulo', 'disposicion', 'anexo'):
                    continue
                
                art_id = node.get('id', f'bloque_{i}')
                art_title_raw = node.get('titulo', '')
                
                # Buscar la versión más reciente del texto
                versiones = node.findall('./version')
                if not versiones: continue
                # Tomar la última versión (asumiendo que es la más actualizada/vigente)
                version_actual = versiones[-1]
                
                # Extraer número si es precepto
                art_num = extract_article_number(art_title_raw) if tipo == 'precepto' else art_id
                
                # Título limpio
                art_title = art_title_raw if art_title_raw else f"Bloque {art_id}"
                
                # Vigencia y Notas (pueden estar en el bloque o en la versión)
                vig_elem = node.find('./vigencia_texto') or version_actual.find('./vigencia_texto')
                vigencia_texto = "".join(vig_elem.itertext()).strip() if vig_elem is not None else ""
                
                notas_elem = node.find('./notas') or version_actual.find('./notas')
                notas_art = "".join(notas_elem.itertext()).strip() if notas_elem is not None else ""
                
                # Párrafos del artículo
                p_elems = version_actual.findall('.//p')
                art_text = "\n".join(["".join(p.itertext()).strip() for p in p_elems]) if p_elems else "".join(version_actual.itertext()).strip()
            else:
                # Formato antiguo/distinto <articulo>
                art_id = node.get('id', f'art_{i}')
                num_elem = node.find('./num')
                art_num = num_elem.text if num_elem is not None else extract_article_number(art_id)
                
                title_elem = node.find('./titulo')
                art_title = "".join(title_elem.itertext()).strip() if title_elem is not None else f"Artículo {art_num}"
                
                vig_elem = node.find('./vigencia_texto')
                vigencia_texto = "".join(vig_elem.itertext()).strip() if vig_elem is not None else ""
                
                notas_elem = node.find('./notas')
                notas_art = "".join(notas_elem.itertext()).strip() if notas_elem is not None else ""
                
                p_elems = node.findall('./p')
                art_text = "\n".join(["".join(p.itertext()).strip() for p in p_elems]) if p_elems else "".join(node.itertext()).strip()
            
            art_text = re.sub(r'\s+', ' ', art_text).strip()
            if len(art_text) < 20: continue
            
            # 4. Dividir en chunks con solapamiento (800 / 150)
            text_chunks = chunk_text_with_overlap(art_text, chunk_size=800, overlap=150)
            
            for j, (chunk_text, chunk_index) in enumerate(text_chunks):
                # Combinar payload global con local
                item_payload = global_payload.copy()
                item_payload.update({
                    "article_number": art_num,
                    "article_title": f"{art_title} (Chunk {chunk_index+1})" if len(text_chunks) > 1 else art_title,
                    "text_snippet": chunk_text,
                    "texto": chunk_text,
                    "chunk_index": chunk_index + 1,
                    "total_chunks": len(text_chunks),
                    "vigencia_texto": vigencia_texto,
                    "notas_articulo": notas_art,
                    "metadata_xml_dump": ET.tostring(node, encoding='unicode')
                })
                
                # Embeddings con el texto del chunk
                dense = model.encode(chunk_text).tolist()
                sparse = generate_sparse_vector(chunk_text)
                
                # ID único considerando el chunk_index
                point_id_seed = f"{boe_id}_{art_id}_{chunk_index}"
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, point_id_seed))
                
                points.append(models.PointStruct(
                    id=point_id,
                    vector={"dense": dense, "text": sparse},
                    payload=item_payload
                ))
            
        if not dry_run and points:
            batch_size = 50
            for i in range(0, len(points), batch_size):
                batch = points[i:i+batch_size]
                client.upsert(collection_name=COLLECTION_NAME, points=batch, wait=True)
            total_p += len(points)
            logger.info(f"  ✅ {len(points)} puntos (chunks) indexados con éxito.")
        elif dry_run:
            logger.info(f"  🔍 (Dry-run) Se habrían indexado {len(points)} artículos.")
            
    logger.info(f"🚀 INGESTA COMPLETADA. Total puntos: {total_p}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ingest_laws(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
