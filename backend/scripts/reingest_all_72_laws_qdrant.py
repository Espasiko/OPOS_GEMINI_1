#!/usr/bin/env python3
import os
import sys
import hashlib
import requests
import pickle
import re
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, SparseVector
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"
BM25_VOCAB_PATH = Path("/home/spas/OPOS_GEMINI_1/backend/data/bm25_vocab.pkl")
FECHA_HOY = datetime.now().strftime("%Y-%m-%d")

# ============================================================================
# UTILIDADES
# ============================================================================
def safe_get_text(soup_node, default=""):
    return soup_node.get_text(strip=True) if soup_node else default

def safe_get_attr(soup_node, attr, default=""):
    return soup_node.get(attr, default) if soup_node else default

def tokenize_legal(text: str) -> list:
    text = text.lower()
    tokens = re.findall(r'[a-záéíóúñ0-9]+', text)
    stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'se', 'por', 'para', 'con', 'un', 'una', 'al', 'lo', 'su', 'sus'}
    return [t for t in tokens if len(t) > 2 and t not in stopwords]

def generate_sparse_vector(text: str, vocab_data: dict) -> SparseVector:
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
    indices, values = [], []
    for term, freq in term_freq.items():
        if term in vocab:
            idx = vocab[term]
            idf = idf_dict.get(term, 0.0)
            score = idf * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / avgdl))
            indices.append(idx)
            values.append(float(score))
    return SparseVector(indices=indices, values=values)

def get_unique_laws_from_qdrant(client) -> dict:
    unique_laws = {}
    offset = None
    print(f"📡 Buscando las leyes previamente indexadas en Qdrant ({COLLECTION_NAME})...")
    while True:
        points, next_offset = client.scroll(
            collection_name=COLLECTION_NAME,
            with_payload=["boe_id", "law_name"],
            with_vectors=False,
            limit=5000,
            offset=offset
        )
        for p in points:
            bid = p.payload.get("boe_id")
            if bid and bid not in unique_laws:
                unique_laws[bid] = p.payload.get("law_name", "Desconocida")
        offset = next_offset
        if offset is None: break
    return unique_laws

def download_and_parse(boe_id: str) -> dict:
    url = f"https://www.boe.es/buscar/xml.php?id={boe_id}"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"⚠️ Error conectando al BOE para {boe_id}: {e}")
        return {}
    
    xml_content = r.text
    if "<documento" not in xml_content and "<p" not in xml_content:
        print(f"⚠️ {boe_id} no retornó XML válido")
        return {}

    soup = BeautifulSoup(xml_content, 'xml')
    meta_node = soup.find('metadatos')
    meta_dict = {}
    if meta_node:
        for child in meta_node.find_all(recursive=False):
            if child.find(recursive=False):
                meta_dict[child.name] = {"codigo": safe_get_attr(child, "codigo"), "_text": child.get_text(strip=True)}
            else:
                meta_dict[child.name] = {"_text": child.get_text(strip=True)}

    chunks = []
    articulos = soup.find_all('articulo')
    if articulos:
        for art in articulos:
            art_id = safe_get_attr(art, "id", f"art_{len(chunks)}")
            title = safe_get_text(art.find('h4')) or safe_get_text(art.find('p', class_='centro_negrita')) or f"Artículo {art_id}"
            content = art.get_text(separator="\n", strip=True)
            chunks.append({"id": art_id, "title": title, "content": content})
    else:
        # Fallback de párrafos
        all_ps = soup.find_all('p')
        legal_ps = []
        for p in all_ps:
            is_meta = any(parent.name in ['metadatos', 'analisis'] for parent in p.parents)
            if not is_meta: legal_ps.append(p.get_text(strip=True))
            
        legal_ps = [p for p in legal_ps if len(p)>5]
        
        current_chunk_ps = []
        char_cnt = 0
        for p in legal_ps:
            if ("Artículo" in p[:20] or "Disposición" in p[:25]) and current_chunk_ps:
                chunks.append({"id": f"p_{len(chunks)}", "title": current_chunk_ps[0][:100], "content": "\n".join(current_chunk_ps)})
                current_chunk_ps = []
                char_cnt = 0
            current_chunk_ps.append(p)
            char_cnt += len(p)
            if char_cnt > 3000:
                chunks.append({"id": f"p_{len(chunks)}", "title": current_chunk_ps[0][:100], "content": "\n".join(current_chunk_ps)})
                current_chunk_ps = []
                char_cnt = 0
        if current_chunk_ps:
            chunks.append({"id": f"p_{len(chunks)}", "title": current_chunk_ps[0][:100], "content": "\n".join(current_chunk_ps)})
            
    if not chunks:
        full_text = soup.get_text(separator="\n", strip=True)
        if full_text:
            chunks.append({"id": "full", "title": "Contenido Completo", "content": full_text[:5000]})
            
    return {
        "metadatos": meta_dict,
        "chunks": chunks,
        "law_title": meta_dict.get("titulo", {}).get("_text", boe_id)
    }

def main():
    print(f"🚀 Iniciando REINGESTA INTELIGENTE (Meta-fecha {FECHA_HOY})")
    client = QdrantClient(url=QDRANT_URL)
    
    unique_laws = get_unique_laws_from_qdrant(client)
    total_laws = len(unique_laws)
    print(f"📚 {total_laws} leyes identificadas para actualización consolidada.")

    print("🤖 Cargando modelos...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    with open(BM25_VOCAB_PATH, 'rb') as f:
        bm25_data = pickle.load(f)

    for idx, (boe_id, law_name) in enumerate(unique_laws.items(), 1):
        print(f"\n📂 [{idx}/{total_laws}] {boe_id} - {law_name[:60]}")
        data = download_and_parse(boe_id)
        if not data or not data["chunks"]:
            print(f"⚠️ Omitiendo {boe_id} (error de parseo o descarga)")
            continue
            
        points = []
        for chunk in data["chunks"]:
            # AÑADIENDO METADATA ESTRICTA DE BARRERA TEMPORAL
            payload = {
                "boe_id": boe_id,
                "law_name": data["law_title"],
                "article_number": chunk["id"],
                "article_title": chunk["title"],
                "text_snippet": chunk["content"],
                "source": "hybrid_sync_FULL_XML_2026_FIX",
                "vigente": True,
                "fecha_texto_consolidado": FECHA_HOY, # <--- AQUI LA MARCA DE TIEMPO
                "advertencia_rag": "Atención: Si es Seguridad Social (SS), el LLM debe omitir normas publicadas después del 04/03/2026, ignorando la consolidación de este texto.",
                "url_boe": f"https://www.boe.es/buscar/act.php?id={boe_id}"
            }
            
            text_to_embed = f"{payload['law_name']} {payload['article_title']} {payload['text_snippet']}"
            dense_vec = model.encode(text_to_embed).tolist()
            sparse_vec = generate_sparse_vector(text_to_embed, bm25_data)
            
            point_id = hashlib.md5(f"{boe_id}_{chunk['id']}".encode()).hexdigest()
            points.append(PointStruct(id=point_id, vector={"dense": dense_vec, "text": sparse_vec}, payload=payload))
            
        if points:
            client.upsert(collection_name=COLLECTION_NAME, points=points)
            print(f"✅ {len(points)} puntos ingresados.")

    print("\n✨ REINGESTA COMPLETADA EXITOSAMENTE ✨")

if __name__ == "__main__":
    main()
