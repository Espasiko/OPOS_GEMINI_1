#!/usr/bin/env python3
import os
import sys
import json
import re
import pickle
import hashlib
import requests
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, SparseVector

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
EMBEDDING_DIM = 1024
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"
BM25_VOCAB_PATH = Path("/home/spas/OPOS_GEMINI_1/backend/data/bm25_vocab.pkl")

LAWS_TO_INGEST = [
    {"id": "BOE-A-2024-26917", "name": "Real Decreto-ley 11/2024 (Reforma Jubilación 2026)"},
    {"id": "BOE-A-2025-26605", "name": "Orden HAC/1517/2025 (Umbrales SARA 2026)"}
]

# ============================================================================
# UTILIDADES
# ============================================================================

def safe_get_text(soup_node, default=""):
    return soup_node.get_text(strip=True) if soup_node else default

def safe_get_attr(soup_node, attr, default=""):
    return soup_node.get(attr, default) if soup_node else default

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

def tokenize_legal(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r'[a-záéíóúñ0-9]+', text)
    stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'se', 'por', 'para', 'con', 'un', 'una', 'al', 'lo', 'su', 'sus'}
    return [t for t in tokens if len(t) > 2 and t not in stopwords]

def generate_sparse_vector(text: str, vocab_data: Dict) -> SparseVector:
    vocab = vocab_data['vocab']
    idf_dict = vocab_data['idf']
    avgdl = vocab_data['avgdl']
    k1 = vocab_data['k1']
    b = vocab_data['b']
    
    tokens = tokenize_legal(text)
    doc_len = len(tokens)
    if doc_len == 0:
        return SparseVector(indices=[], values=[])
    
    from collections import Counter
    term_freq = Counter(tokens)
    indices = []
    values = []
    
    for term, freq in term_freq.items():
        if term in vocab:
            idx = vocab[term]
            idf = idf_dict.get(term, 0.0)
            score = idf * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / avgdl))
            indices.append(idx)
            values.append(float(score))
    
    return SparseVector(indices=indices, values=values)

# ============================================================================
# PROCESAMIENTO
# ============================================================================

def download_and_parse(boe_id: str) -> Dict:
    # Intentar descargar XML del diario (contiene metadatos de análisis)
    # Si no, intentar XML de legislación consolidada
    urls = [
        f"https://www.boe.es/diario_boe/xml.php?id={boe_id}",
        f"https://www.boe.es/buscar/xml.php?id={boe_id}"
    ]
    
    xml_content = None
    for url in urls:
        print(f"📥 Descargando {boe_id} desde {url}...")
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            r.raise_for_status()
            if "<documento" in r.text or "<p" in r.text:
                xml_content = r.text
                print(f"✅ Descargado ({len(xml_content)}) bytes")
                break
        except Exception as e:
            print(f"⚠️ Error en {url}: {e}")
            
    if not xml_content:
        raise Exception(f"No se pudo descargar el XML para {boe_id}")
        
    soup = BeautifulSoup(xml_content, 'xml')
    meta_node = soup.find('metadatos')
    anal_node = soup.find('analisis')
    texto_node = soup.find('texto')
    
    # Extraer metadatos
    meta_dict = {}
    if meta_node:
        for child in meta_node.find_all(recursive=False):
            if child.find(recursive=False): # Tiene submetadatos (ej: departamento)
                meta_dict[child.name] = {"codigo": safe_get_attr(child, "codigo"), "_text": child.get_text(strip=True)}
            else:
                meta_dict[child.name] = {"_text": child.get_text(strip=True)}
                
    # Extraer materias
    materias = []
    if anal_node:
        mats = anal_node.find_all('materia')
        for m in mats:
            materias.append({"codigo": safe_get_attr(m, "codigo"), "_text": m.get_text(strip=True)})
            
    # Extraer texto por bloques/artículos
    chunks = []
    
    # Intentar primero con estructura <articulo>
    articulos = soup.find_all('articulo')
    if articulos:
        print(f"   🔍 Se encontraron {len(articulos)} etiquetas <articulo>")
        for art in articulos:
            art_id = safe_get_attr(art, "id", f"art_{len(chunks)}")
            title = safe_get_text(art.find('h4')) or safe_get_text(art.find('p', class_='centro_negrita')) or f"Artículo {art_id}"
            content = art.get_text(separator="\n", strip=True)
            chunks.append({"id": art_id, "title": title, "content": content})
    else:
        # Fallback definitivo: buscar TODOS los <p> del documento pero filtrar metadatos
        print(f"   🔍 Buscando párrafos globales (fallback)")
        all_ps = soup.find_all('p')
        metadata_tags = ['metadatos', 'analisis', 'metadata-eli', 'metadata-boe'] # Posibles contenedores de meta
        
        legal_ps = []
        for p in all_ps:
            # Verificar que no esté dentro de etiquetas de metadatos
            is_meta = False
            for parent in p.parents:
                if parent.name in metadata_tags:
                    is_meta = True
                    break
            if not is_meta:
                legal_ps.append(p.get_text(strip=True))
        
        # Limpiar vacíos y cortos
        all_ps_texts = [p for p in legal_ps if len(p) > 5]
        print(f"   🔍 Párrafos legales detectados: {len(all_ps_texts)}")
        
        current_chunk_ps = []
        chunk_char_count = 0
        MAX_CHAR_PER_CHUNK = 3000 # ~750 tokens
        
        for p_text in all_ps_texts:
            # Si empieza por Artículo/Disposición, cerramos el actual
            if ( ("Artículo" in p_text[:20] or "Disposición" in p_text[:25]) and current_chunk_ps ):
                full_txt = "\n".join(current_chunk_ps)
                chunks.append({
                    "id": f"p_{len(chunks)}", 
                    "title": current_chunk_ps[0][:100], 
                    "content": full_txt
                })
                current_chunk_ps = []
                chunk_char_count = 0
            
            current_chunk_ps.append(p_text)
            chunk_char_count += len(p_text)
            
            # Si el chunk se hace muy grande, cerramos
            if chunk_char_count > MAX_CHAR_PER_CHUNK:
                full_txt = "\n".join(current_chunk_ps)
                chunks.append({
                    "id": f"p_{len(chunks)}", 
                    "title": current_chunk_ps[0][:100], 
                    "content": full_txt
                })
                current_chunk_ps = []
                chunk_char_count = 0
                
        if current_chunk_ps:
            chunks.append({
                "id": f"p_{len(chunks)}", 
                "title": current_chunk_ps[0][:100], 
                "content": "\n".join(current_chunk_ps)
            })
                
    if not chunks:
        # Último recurso: todo el texto como un solo chunk si no hay nada más
        full_text = soup.get_text(separator="\n", strip=True)
        if full_text:
            chunks.append({"id": "full", "title": "Contenido Completo", "content": full_text[:5000]})
                
    return {
        "metadatos": meta_dict,
        "materias": materias,
        "analisis_raw": str(anal_node) if anal_node else "",
        "chunks": chunks,
        "boe_id": boe_id,
        "law_title": meta_dict.get("titulo", {}).get("_text", boe_id)
    }

def main():
    print("🚀 Iniciando ingesta directa de Normativa 2026...")
    
    # 1. Cargar Recurso de Qdrant y Modelos
    client = QdrantClient(url=QDRANT_URL)
    print("🤖 Cargando modelo de embeddings...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    print("📚 Cargando vocabulario BM25...")
    with open(BM25_VOCAB_PATH, 'rb') as f:
        bm25_data = pickle.load(f)
        
    for law_info in LAWS_TO_INGEST:
        boe_id = law_info["id"]
        print(f"\n📂 Procesando {boe_id} - {law_info['name']}")
        
        try:
            data = download_and_parse(boe_id)
            print(f"📄 Dividida en {len(data['chunks'])} chunks")
            
            points = []
            for chunk in data["chunks"]:
                # Construir Payload EXACTO como FULL_XML
                payload = {
                    "boe_id": boe_id,
                    "law_name": data["law_title"],
                    "article_number": chunk["id"],
                    "article_title": chunk["title"],
                    "text_snippet": chunk["content"],
                    "source": "hybrid_sync_FULL_XML_2026_FIX",
                    "vigente": True,
                    "organismo_emisor": data["metadatos"].get("departamento", {}).get("_text", ""),
                    "fecha_publicacion": data["metadatos"].get("fecha_publicacion", {}).get("_text", ""),
                    "rango": data["metadatos"].get("rango", {}).get("_text", ""),
                    "url_boe": f"https://www.boe.es/buscar/act.php?id={boe_id}",
                    "materias": [m["_text"] for m in data["materias"]],
                    "metadata_xml_raw": data["analisis_raw"] # Para LLMs
                }
                
                # Generar Vectores
                text_to_embed = f"{payload['law_name']} {payload['article_title']} {payload['text_snippet']}"
                dense_vec = model.encode(text_to_embed).tolist()
                sparse_vec = generate_sparse_vector(text_to_embed, bm25_data)
                
                point_id = hashlib.md5(f"{boe_id}_{chunk['id']}".encode()).hexdigest()
                
                points.append(PointStruct(
                    id=point_id,
                    vector={"dense": dense_vec, "text": sparse_vec},
                    payload=payload
                ))
            
            # Upsert
            if points:
                client.upsert(collection_name=COLLECTION_NAME, points=points)
                print(f"✅ {len(points)} puntos ingresados en {COLLECTION_NAME}")
            
        except Exception as e:
            print(f"❌ Error procesando {boe_id}: {e}")
            import traceback
            traceback.print_exc()

    print("\n✨ Proceso de ingesta 2026 completado.")

if __name__ == "__main__":
    main()
