#!/usr/bin/env python3
"""
Migrar datos Qdrant Cloud → Local Híbrido
- Lee puntos de Cloud (dense only)
- Genera sparse vectors (BM25)
- Inserta en local (dense + sparse)
"""

import os
import sys
from pathlib import Path
from collections import Counter
from typing import List
import numpy as np
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env.backend")

print("=" * 70)
print("MIGRACIÓN QDRANT CLOUD → LOCAL HÍBRIDO")
print("=" * 70)

# Configuración
CLOUD_COLLECTION = "opositaia_knowledge"
LOCAL_COLLECTION = "opositaia_knowledge_hybrid"
BATCH_SIZE = 50  # Reducido de 100 a 50 para evitar timeouts
MAX_POINTS = None  # None = todos

# Conectar
print("\n1. Conectando a Qdrant...")
client_cloud = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=60.0  # Aumentar timeout a 60s
)
client_local = QdrantClient(
    url="http://localhost:6333",
    timeout=30.0
)

# Verificar colecciones
cloud_info = client_cloud.get_collection(CLOUD_COLLECTION)
local_info = client_local.get_collection(LOCAL_COLLECTION)

print(f"   Cloud: {cloud_info.points_count:,} points")
print(f"   Local: {local_info.points_count:,} points")

# 2. Tokenizer
def tokenize_legal(text: str) -> List[str]:
    """Tokenizer para textos legales"""
    import re
    text = text.lower()
    tokens = re.findall(r'[a-záéíóúñ0-9]+', text)
    stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'se', 'por', 'para', 'con', 'un', 'una', 'al', 'lo', 'su', 'sus'}
    return [t for t in tokens if len(t) > 2 and t not in stopwords]

# 3. Cargar vocabulario BM25 guardado
print("\n2. Cargando vocabulario BM25...")

import pickle
vocab_path = Path(__file__).parent.parent / "data/bm25_vocab.pkl"

with open(vocab_path, 'rb') as f:
    bm25_data = pickle.load(f)
    
vocab = bm25_data['vocab']
idf_dict = bm25_data['idf']
avgdl = bm25_data['avgdl']
k1 = bm25_data['k1']
b = bm25_data['b']

print(f"   ✅ Vocabulario BM25: {len(vocab):,} términos, avgdl={avgdl:.1f}")

def vectorize_bm25(text: str) -> models.SparseVector:
    """Generate BM25 sparse vector using shared vocabulary"""
    from collections import Counter
    tokens = tokenize_legal(text)
    term_freq = Counter(tokens)
    doc_len = len(tokens)
    
    indices = []
    values = []
    
    for term, freq in term_freq.items():
        if term in vocab:
            idx = vocab[term]
            idf_score = idf_dict.get(idx, 0)
            
            # BM25 formula
            score = idf_score * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / avgdl))
            
            if score > 0.01:
                indices.append(idx)
                values.append(float(score))
                
    return models.SparseVector(indices=indices, values=values)

# 4. Migración
print("\n4. Migrando puntos...")

total_migrated = 0
offset = None

with tqdm(total=cloud_info.points_count if MAX_POINTS is None else MAX_POINTS, desc="Migrating") as pbar:
    while True:
        # Scroll Cloud
        scroll_result = client_cloud.scroll(
            collection_name=CLOUD_COLLECTION,
            limit=BATCH_SIZE,
            offset=offset,
            with_payload=True,
            with_vectors=True
        )
        
        points, next_offset = scroll_result
        
        if not points:
            break
            
        # Transform points
        hybrid_points = []
        for point in points:
            # Get dense vector
            dense_vec = point.vector
            
            # Generate sparse vector using shared vocabulary
            text = point.payload.get('text_snippet', point.payload.get('text', ''))
            sparse_vec = vectorize_bm25(text) if text else models.SparseVector(indices=[], values=[])
            
            # Create hybrid point
            hybrid_point = models.PointStruct(
                id=point.id,
                vector={
                    "dense": dense_vec,
                    "text": sparse_vec
                },
                payload=point.payload
            )
            hybrid_points.append(hybrid_point)
            
        # Upload to local
        client_local.upsert(
            collection_name=LOCAL_COLLECTION,
            points=hybrid_points
        )
        
        total_migrated += len(points)
        pbar.update(len(points))
        
        if MAX_POINTS and total_migrated >= MAX_POINTS:
            break
            
        if next_offset is None:
            break
            
        offset = next_offset

print(f"\n✅ Migración completada: {total_migrated:,} puntos")

# 5. Verificar
final_info = client_local.get_collection(LOCAL_COLLECTION)
print(f"   Colección local híbrida: {final_info.points_count:,} puntos")

print("\n" + "=" * 70)
print("LISTO - Próximo paso:")
print("  python backend/scripts/compare_search_dense_vs_hybrid.py")
print("=" * 70)
