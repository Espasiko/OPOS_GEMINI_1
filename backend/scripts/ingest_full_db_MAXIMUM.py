#!/usr/bin/env python3
"""
INGESTA COMPLETA BD → Qdrant Local Híbrido
Configuración MÁXIMA EXCELENCIA - Sin límites

Target: 85-90% Recall@10
Chunks: 3000 chars, Overlap 30%
"""

import os, sys, json, pickle, re
from pathlib import Path
from typing import List, Dict
from collections import Counter
import psycopg2
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env.backend")

# === CONFIGURACIÓN MÁXIMA ===
CHUNK_SIZE = 3000  # chars
OVERLAP_PCT = 0.30  # 30%
OVERLAP_CHARS = int(CHUNK_SIZE * OVERLAP_PCT)  # 900 chars
STEP = CHUNK_SIZE - OVERLAP_CHARS  # 2100 chars

COLLECTION_NAME = "opositaia_knowledge_hybrid_FULL"
BATCH_SIZE = 50

print("=" * 90)
print("INGESTA COMPLETA BD → QDRANT LOCAL HÍBRIDO - CONFIGURACIÓN MÁXIMA")
print("=" * 90)
print(f"\n📐 Configuración:")
print(f"   Chunk size: {CHUNK_SIZE} chars")
print(f"   Overlap: {OVERLAP_PCT*100:.0f}% ({OVERLAP_CHARS} chars)")
print(f"   Step: {STEP} chars")
print(f"   Target: 85-90% Recall@10\n")

# === SETUP ===
print("1. Inicializando...")

# Qdrant local
qdrant = QdrantClient(url="http://localhost:6333", timeout=120.0)

# Embedder
embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
print(f"   ✅ Embedder: {embedder}")

# BM25 vocab
vocab_file = Path(__file__).parent.parent / "data" / "bm25_vocab.pkl"
with open(vocab_file, 'rb') as f:
    bm25_data = pickle.load(f)

vocab = bm25_data['vocab']
idf_dict = bm25_data['idf']
avgdl, k1, b = bm25_data['avgdl'], bm25_data['k1'], bm25_data['b']
print(f"   ✅ BM25 vocab: {len(vocab):,} términos")

# Tokenizer
def tokenize_legal(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r'[a-záéíóúñ0-9]+', text)
    stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'se', 'por', 'para', 'con', 'un', 'una', 'al', 'lo', 'su', 'sus'}
    return [t for t in tokens if len(t) > 2 and t not in stopwords]

# Sparse vectorizer
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

# === CREAR COLECCIÓN ===
print("\n2. Creando colección híbrida...")

try:
    qdrant.delete_collection(COLLECTION_NAME)
    print(f"   ⚠️  Colección existente eliminada")
except:
    pass

qdrant.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config={
        "dense": models.VectorParams(
            size=1024,
            distance=models.Distance.COSINE
        )
    },
    sparse_vectors_config={
        "text": models.SparseVectorParams()
    }
)

print(f"   ✅ Colección '{COLLECTION_NAME}' creada")

# === CHUNKING INTELIGENTE ===
def chunk_text_smart(text: str, law_id: str, law_name: str) -> List[Dict]:
    """Chunking con overlap y metadata"""
    chunks = []
    
    # Split en párrafos primero
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    full_text = ' '.join(paragraphs)
    
    # Chunking con overlap
    start = 0
    chunk_id = 0
    
    while start < len(full_text):
        end = start + CHUNK_SIZE
        
        # Ajustar fin al final de palabra
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
                'chunk_size': len(chunk_text),
                'overlap_start': start > 0
            })
            chunk_id += 1
        
        # Avanzar con overlap
        start += STEP
    
    return chunks

# === CONECTAR POSTGRES ===
print("\n3. Conectando a Postgres...")

conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', 5432),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD')
)

cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM laws WHERE content IS NOT NULL AND content != ''")
total_laws = cur.fetchone()[0]

print(f"   ✅ {total_laws:,} leyes con contenido")

# === PROCESAR E INGESTAR ===
print(f"\n4. Procesando e ingiriendo...")

cur.execute("""
    SELECT id, law_id, law_name, content
    FROM laws
    WHERE content IS NOT NULL AND content != ''
    ORDER BY law_id
""")

batch_points = []
total_chunks = 0
processed_laws = 0

with tqdm(total=total_laws, desc="Leyes") as pbar_laws:
    for row in cur:
        db_id, law_id, law_name, content = row
        
        # Chunking
        chunks = chunk_text_smart(content, law_id or db_id, law_name or "Ley sin nombre")
        
        # Vectorizar chunks
        for chunk in chunks:
            # Dense
            dense_vec = embedder.encode(chunk['text']).tolist()
            
            # Sparse
            sparse_vec = vectorize_bm25(chunk['text'])
            
            # Point
            point = models.PointStruct(
                id=total_chunks,
                vector={
                    "dense": dense_vec,
                    "text": sparse_vec
                },
                payload={
                    "text_snippet": chunk['text'],
                    "law_id": chunk['law_id'],
                    "law_name": chunk['law_name'],
                    "chunk_index": chunk['chunk_index'],
                    "chunk_size": chunk['chunk_size'],
                    "created_at": datetime.now().isoformat()
                }
            )
            
            batch_points.append(point)
            total_chunks += 1
            
            # Upsert batch
            if len(batch_points) >= BATCH_SIZE:
                qdrant.upsert(
                    collection_name=COLLECTION_NAME,
                    points=batch_points
                )
                batch_points = []
        
        processed_laws += 1
        pbar_laws.update(1)
        pbar_laws.set_postfix({'chunks': total_chunks})

# Final batch
if batch_points:
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=batch_points
    )

cur.close()
conn.close()

# === RESUMEN ===
print("\n" + "=" * 90)
print("RESUMEN FINAL")
print("=" * 90)

final_info = qdrant.get_collection(COLLECTION_NAME)

print(f"\n✅ Ingesta completada:")
print(f"   Leyes procesadas: {processed_laws:,}")
print(f"   Chunks generados: {total_chunks:,}")
print(f"   Chunks en Qdrant: {final_info.points_count:,}")
print(f"   Configuración: {CHUNK_SIZE} chars, {OVERLAP_PCT*100:.0f}% overlap")

# Guardar metadata
metadata = {
    'collection': COLLECTION_NAME,
    'timestamp': datetime.now().isoformat(),
    'config': {
        'chunk_size': CHUNK_SIZE,
        'overlap_pct': OVERLAP_PCT,
        'overlap_chars': OVERLAP_CHARS,
        'step': STEP
    },
    'stats': {
        'laws_processed': processed_laws,
        'chunks_generated': total_chunks,
        'points_in_qdrant': final_info.points_count
    }
}

metadata_file = Path("ingestion_metadata_FULL.json")
with open(metadata_file, 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"\n📄 Metadata: {metadata_file}")
print("\n" + "=" * 90)
