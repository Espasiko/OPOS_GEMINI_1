import os
import json
import logging
import argparse
import re
import uuid
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any

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
    import xml.etree.ElementTree as ET
    import pickle
    import numpy as np
    import httpx
except ImportError as e:
    logger.error(f"❌ Error importando dependencias: {e}")
    sys.exit(1)

# CONFIGURACIÓN DE RUTAS
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT / "backend" / "agents"))

try:
    from boe_api_client import BOEApiClient
except ImportError:
    try:
        from agents.boe_api_client import BOEApiClient
    except ImportError:
        logger.error(f"❌ No se encontró boe_api_client.py en {PROJECT_ROOT / 'backend' / 'agents'}")
        sys.exit(1)

# CONFIGURACIÓN GLOBAL
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"
QDRANT_URL = "http://localhost:6333"
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
BM25_VOCAB_FILE = PROJECT_ROOT / "backend" / "data" / "bm25_vocab.pkl"
JSON_DIR = PROJECT_ROOT / "data" / "boe_xml"
JSON_DIR.mkdir(parents=True, exist_ok=True)

MISSING_LAWS = [
    {"id": "BOE-A-2023-6967", "nombre": "RDL 2/2023 Pensiones y Sostenibilidad", "prioridad": "CRÍTICA"},
    {"id": "BOE-A-2011-15936", "nombre": "Ley 36/2011 Reguladora Jurisdicción Social", "prioridad": "ALTA"},
    {"id": "BOE-A-2020-1246", "nombre": "RD 139/2020 Estructura Orgánica AGE", "prioridad": "ALTA"},
    {"id": "BOE-A-1995-8729", "nombre": "RD 364/1995 Ingreso Personal AGE", "prioridad": "ALTA"},
    {"id": "BOE-A-1995-8730", "nombre": "RD 365/1995 Situaciones Administrativas AGE", "prioridad": "ALTA"},
    {"id": "BOE-A-2010-1331", "nombre": "RD 4/2010 Esquema Nacional de Interoperabilidad", "prioridad": "ALTA"}
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
                # Caso: el pickle es directamente el dict {token: id}
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

def safe_get_text(node, default=""):
    if isinstance(node, dict): return node.get('_text', default)
    return str(node) if node else default

def extract_article_number(title: str) -> str:
    m = re.search(r'(?:Artículo|Art\.|Art)\s*(\d+(?:\.\d+)?)', title, re.I)
    return m.group(1) if m else ""

def download_law_from_boe(boe_id: str, nombre: str):
    analisis_data = {}; texto_xml = None
    with BOEApiClient(timeout=60) as client:
        try:
            doc = client.get_documento_consolidado(boe_id)
            if doc and 'data' in doc: analisis_data = doc
        except: pass
        try: texto_xml = client.get_texto_consolidado(boe_id)
        except: pass
    return analisis_data, texto_xml

def download_from_html_fallback(boe_id: str) -> Optional[str]:
    url = f"https://www.boe.es/buscar/act.php?id={boe_id}"
    logger.info(f"  🌍 Intentando fallback HTML para {boe_id}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        with httpx.Client(timeout=30, follow_redirects=True, headers=headers) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                html = resp.text
                match = re.search(r'<div id="textox(?:slt)?">(.*?)</div>\s*<!-- #textox', html, re.DOTALL)
                if not match:
                    match = re.search(r'<div id="textox(?:slt)?">(.*?)</div>\s*<!-- #DOdocText', html, re.DOTALL)
                if match:
                    content = match.group(1)
                    # Marcar artículos usando marcador especial
                    content = re.sub(r'<h[45] class="articulo">(.*?)</h[45]>', r'===ARTICULO===\1\n', content)
                    content = re.sub(r'<p class="parrafo">(.*?)</p>', r'\1\n', content)
                    content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
                    content = re.sub(r'<.*?>', ' ', content)
                    content = re.sub(r'\s+', ' ', content).strip()
                    return f"__HTML_FALLBACK__\n{content}"
            return None
    except Exception as e:
        logger.warning(f"  ⚠️ Fallback HTML falló para {boe_id}: {e}")
        return None

def parse_xml_to_chunks(boe_id: str, nombre: str, content_str: str) -> List[Dict]:
    chunks = []
    if not content_str: return chunks
    if content_str.startswith("__HTML_FALLBACK__"):
        content = content_str.replace("__HTML_FALLBACK__\n", "")
        parts = re.split(r'===ARTICULO===', content)
        for i, part in enumerate(parts):
            if not part.strip(): continue
            lines = part.strip().split('\n', 1)
            title = lines[0] if len(lines) > 1 else f"Artículo {i}"
            text = lines[1] if len(lines) > 1 else lines[0]
            if len(text) < 40: continue
            chunks.append({'boe_id': boe_id, 'law_name': nombre, 'article_title': title[:250], 'text_snippet': text.strip(), 'layer': 'article_chunk', 'id': f"html_art_{i}"})
        return chunks
    try:
        root = ET.fromstring(content_str.encode('utf-8'))
        articulos = root.findall('.//articulo') or root.findall('.//{*}articulo')
        if not articulos:
            paragraphs = root.findall('.//p') or root.findall('.//{*}p')
            if paragraphs:
                full_text = " ".join(["".join(p.itertext()).strip() for p in paragraphs])
                for i in range(0, len(full_text), 2500):
                    chunks.append({'boe_id': boe_id, 'law_name': nombre, 'article_title': f"Parte {i//2500 + 1}", 'text_snippet': full_text[i:i+2500].strip(), 'layer': 'article_chunk', 'id': f"chunk_{i}"})
                return chunks
            return []
        for i, art in enumerate(articulos):
            title_elem = art.find('./titulo') or art.find('.//{*}titulo')
            art_title = "".join(title_elem.itertext()).strip() if title_elem is not None else f"Artículo {i+1}"
            p_elems = art.findall('./p') or art.findall('.//{*}p')
            art_text = "\n".join(["".join(p.itertext()).strip() for p in p_elems]) if p_elems else "".join(art.itertext()).strip()
            art_text = re.sub(r'\s+', ' ', art_text).strip()
            if len(art_text) < 40: continue
            chunks.append({'boe_id': boe_id, 'law_name': nombre, 'article_title': art_title[:250], 'text_snippet': art_text, 'layer': 'article_chunk', 'id': art.get('id', f'art_{i}')})
        return chunks
    except Exception as e:
        logger.error(f"  ❌ Error parseando XML de {boe_id}: {e}")
        return []

def build_chunk_payload(chunk, anal_data):
    boe_id = chunk['boe_id']
    payload = {
        "boe_id": boe_id, "law_name": chunk['law_name'] or '', "article_title": chunk['article_title'] or '',
        "text_snippet": chunk['text_snippet'] or '', "chunk_index": chunk.get('chunk_index', 0),
        "total_chunks": chunk.get('total_chunks', 1), "article_number": extract_article_number(chunk['article_title']),
        "layer": "article_chunk", "source": "ingest_missing_v2",
    }
    if anal_data:
        data = anal_data.get('data', anal_data)
        meta = data.get('metadatos', {}); anal = data.get('analisis', {})
        payload.update({
            "organismo_emisor": safe_get_text(meta.get('departamento')),
            "rango": safe_get_text(meta.get('rango')),
            "url_boe": f"https://www.boe.es/buscar/act.php?id={boe_id}"
        })
    return payload

def ingest_laws(laws: List[Dict], dry_run: bool = False):
    qdrant = QdrantClient(url=QDRANT_URL, timeout=120)
    model = get_embedding_model()
    total_p = 0
    for ley in laws:
        boe_id = ley['id']; nombre = ley['nombre']
        logger.info(f"👉 Procesando {boe_id}...")
        anal_data, content = download_law_from_boe(boe_id, nombre)
        if not content: content = download_from_html_fallback(boe_id)
        chunks = parse_xml_to_chunks(boe_id, nombre, content)
        if not chunks: logger.warning(f"  ⚠️ Fallo total en {boe_id}"); continue
        points = []
        for j, chunk in enumerate(chunks):
            chunk['chunk_index'] = j + 1; chunk['total_chunks'] = len(chunks)
            payload = build_chunk_payload(chunk, anal_data)
            dense = model.encode(chunk['text_snippet']).tolist()
            sparse = generate_sparse_vector(chunk['text_snippet'])
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{boe_id}_{chunk['id']}"))
            points.append(models.PointStruct(id=point_id, vector={"dense": dense, "text": sparse}, payload=payload))
        if not dry_run:
            qdrant.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
            total_p += len(points); logger.info(f"  ✅ {len(points)} puntos indexados.")
    logger.info(f"Fin. {total_p} puntos indexados.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="+")
    parser.add_argument("--criticas", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    laws = MISSING_LAWS.copy()
    if args.ids:
        laws = [{"id": i, "nombre": f"Norma {i}"} for i in args.ids]
    elif args.criticas:
        laws = [l for l in MISSING_LAWS if l["prioridad"] == "CRÍTICA"]
    ingest_laws(laws, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
