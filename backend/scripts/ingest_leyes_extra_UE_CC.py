#!/usr/bin/env python3
"""
Ingestar Código Civil + TUE + TFUE en Qdrant LOCAL
Config: 3000 chars, 30% overlap (igual que BD completa)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pickle
import re
from typing import List, Dict
from collections import Counter
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from datetime import datetime

# === CONFIG ===
CHUNK_SIZE = 3000  # chars
OVERLAP_PCT = 0.30
OVERLAP_CHARS = int(CHUNK_SIZE * OVERLAP_PCT)  # 900
STEP = CHUNK_SIZE - OVERLAP_CHARS  #2100

COLLECTION_NAME = "opositaia_knowledge_hybrid_FULL"  # Misma colección
BATCH_SIZE = 50

print("=" * 80)
print("INGESTA CÓDIGO CIVIL + TRATADOS UE → Qdrant LOCAL")
print("=" * 80)
print(f"\nConfig: {CHUNK_SIZE} chars, {OVERLAP_PCT*100:.0f}% overlap")
print(f"Colección: {COLLECTION_NAME} (añadir a existente)\n")

# === ARCHIVOS ===
DATA_DIR = Path("/home/spas/OPOS_GEMINI_1/backend/data/leyes_extra")

LAWS_TO_INGEST = {
    "codigo_civil": {
        "file": DATA_DIR / "codigo_civil_BOE-A-1889-4763_parsed.txt",
        "law_id": "BOE-A-1889-4763",
        "law_name": "Código Civil"
    },
    "tue": {
        "file": DATA_DIR / "TUE_eurlex_parsed.txt",
        "law_id": "CELEX-12012M",
        "law_name": "Tratado de la Unión Europea (TUE)"
    },
    "tfue": {
        "file": DATA_DIR / "TFUE_eurlex_parsed.txt",
        "law_id": "CELEX-12012E",
        "law_name": "Tratado de Funcionamiento de la UE (TFUE)"
    }
}

# === SETUP ===
print("1. Inicializando...")

# Qdrant local
qdrant = QdrantClient(url="http://localhost:6333", timeout=120.0)

# Embedder
embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
print(f"   ✅ Embedder: pablosi/bge-m3-spa-law-qa-trained-2")

# BM25 vocab
vocab_file = Path(__file__).parent.parent / "data" / "bm25_vocab.pkl"
with open(vocab_file, 'rb') as f:
    bm25_data = pickle.load(f)

vocab = bm25_data['vocab']
idf_dict = bm25_data['idf']
avgdl, k1, b = bm25_data['avgdl'], bm25_data['k1'], bm25_data['b']
print(f"   ✅ BM25 vocab: {len(vocab):,} términos")

# === TOKENIZER ===
def tokenize_legal(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r'[a-záéíóúñ0-9]+', text)
    stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'se', 'por', 'para', 'con', 'un', 'una', 'al', 'lo', 'su', 'sus'}
    return [t for t in tokens if len(t) > 2 and t not in stopwords]

def vectorize_bm25(text: str) -> models.SparseVector:
    tokens = tokenize_legal(text)
    term_freq = Counter(tokens)
    doc_len = len(tokens)
    
    indices, values = [], []
    for term, freq in term_freq.items():
        if term in vocab:
            idx = vocab[term]
            idf_score = idf_dict.get(idx, 0)
            score = idf_score * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / avgdl))
            if score > 0.01:
                indices.append(idx)
                values.append(float(score))
    
    return models.SparseVector(indices=indices, values=values)

# === CHUNKING ===
def chunk_text_smart(text: str, law_id: str, law_name: str) -> List[Dict]:
    """Chunking con overlap"""
    chunks = []
    
    # Limpiar texto
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    full_text = ' '.join(paragraphs)
    
    # Chunking con overlap
    start = 0
    chunk_id = 0
    
    while start < len(full_text):
        end = start + CHUNK_SIZE
        
        # Ajustar fin al final de frase
        if end < len(full_text):
            while end > start and full_text[end] not in ' .,:;!?\n':
                end -= 1
        else:
            end = len(full_text)
        
        chunk_text = full_text[start:end].strip()
        
        if len(chunk_text) > 100:  # Mínimo 100 chars
            chunks.append({
                'id': f"{law_id}_chunk_{chunk_id}",
                'text': chunk_text,
                'law_id': law_id,
                'law_name': law_name,
                'chunk_index': chunk_id,
                'chunk_size': len(chunk_text)
            })
            chunk_id += 1
        
        start += STEP
    
    return chunks

# === VERIFICAR COLECCIÓN ===
print("\n2. Verificando colección...")

try:
    collection_info = qdrant.get_collection(COLLECTION_NAME)
    current_points = collection_info.points_count
    print(f"   ✅ Colección existe: {current_points:,} puntos actuales")
    print(f"   📝 Añadiremos las nuevas leyes a esta colección")
except:
    print(f"   ❌ Colección '{COLLECTION_NAME}' no existe")
    print(f"   ⚠️ Ejecuta primero: ingest_full_db_MAXIMUM.py")
    sys.exit(1)

# === PROCESAR E INGESTAR ===
print(f"\n3. Procesando {len(LAWS_TO_INGEST)} leyes...")

batch_points = []
total_chunks = 0
next_id = current_points  # Continuar desde último ID

for key, law in LAWS_TO_INGEST.items():
    if not law['file'].exists():
        print(f"\n   ⚠️ SKIP {law['law_name']}: archivo no existe")
        continue
    
    print(f"\n   📄 {law['law_name']}")
    print(f"      Archivo: {law['file'].name}")
    
    # Leer texto
    with open(law['file'], 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"      Texto: {len(text):,} chars")
    
    # Chunking
    chunks = chunk_text_smart(text, law['law_id'], law['law_name'])
    print(f"      Chunks: {len(chunks)}")
    
    # Vectorizar e ingestar
    for chunk in tqdm(chunks, desc=f"      Ingiriendo {key}", leave=False):
        # Dense
        dense_vec = embedder.encode(chunk['text']).tolist()
        
        # Sparse
        sparse_vec = vectorize_bm25(chunk['text'])
        
        # Point
        point = models.PointStruct(
            id=next_id,
            vector={
                "dense": dense_vec,
                "text": sparse_vec
            },
            payload={
                "text_snippet": chunk['text'][:500],  # Preview
                "law_id": chunk['law_id'],
                "law_name": chunk['law_name'],
                "chunk_index": chunk['chunk_index'],
                "chunk_size": chunk['chunk_size'],
                "created_at": datetime.now().isoformat(),
                "source": "leyes_extra_08012026"
            }
        )
        
        batch_points.append(point)
        total_chunks += 1
        next_id += 1
        
        # Upsert batch
        if len(batch_points) >= BATCH_SIZE:
            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=batch_points
            )
            batch_points = []

# Final batch
if batch_points:
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=batch_points
    )

# === RESUMEN ===
print("\n" + "=" * 80)
print("RESUMEN FINAL")
print("=" * 80)

final_info = qdrant.get_collection(COLLECTION_NAME)

print(f"\n✅ Ingesta completada:")
print(f"   Puntos antes: {current_points:,}")
print(f"   Puntos añadidos: {total_chunks:,}")
print(f"   Puntos totales: {final_info.points_count:,}")

print(f"\n📊 Leyes extra ingestadas:")
for key, law in LAWS_TO_INGEST.items():
    if law['file'].exists():
        print(f"   ✅ {law['law_name']}")

print("\n" + "=" * 80)
print("SIGUIENTE PASO: Ejecutar Salamandra sobre examen enero_25")
print("=" * 80)
