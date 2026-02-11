#!/usr/bin/env python3
"""
Crear Colección Híbrida Qdrant desde Snapshot
- Carga snapshot existente (dense vectors)
- Genera sparse vectors (BM25) para cada punto
- Crea nueva colección con dense + sparse
"""

import json
import tarfile
from pathlib import Path
from collections import Counter
from typing import List, Dict, Tuple
import numpy as np
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

# Config
SNAPSHOT_PATH = Path("gastos_ tokens/opositaia_knowledge-7212264562315011-2026-01-07-13-08-55.snapshot")
QDRANT_URL = "http://localhost:6333"
NEW_COLLECTION = "opositaia_knowledge_hybrid"

print("=" * 60)
print("CREACIÓN COLECCIÓN HYBRID QDRANT")
print("=" * 60)

# 1. Cargar embedding model (dense)
print("\n1. Cargando modelo embeddings...")
embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
print("   ✅ BGE-M3 cargado")

# 2. Generar vocabulario para BM25 (sparse)
print("\n2. Generando vocabulario BM25...")

def tokenize_legal(text: str) -> List[str]:
    """Tokenize para textos legales españoles"""
    import re
    # Lowercase
    text = text.lower()
    # Preservar artículos, siglas, números
    text = re.sub(r'([a-záéíóúñ]+)', r' \1 ', text)
    tokens = text.split()
    # Filtrar stopwords básicas
    stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'se', 'por', 'para', 'con'}
    return [t for t in tokens if len(t) > 2 and t not in stopwords]

class BM25Vectorizer:
    def __init__(self):
        self.vocab = {}
        self.idf = {}
        self.doc_count = 0
        
    def fit(self, documents: List[str]):
        """Build vocabulary from documents"""
        doc_freq = Counter()
        
        for doc in documents:
            tokens = set(tokenize_legal(doc))
            for token in tokens:
                doc_freq[token] += 1
                
        # Create vocab (top 10K terms)
        self.vocab = {word: idx for idx, (word, _) in enumerate(doc_freq.most_common(10000))}
        
        # Calculate IDF
        self.doc_count = len(documents)
        for word, idx in self.vocab.items():
            df = doc_freq[word]
            self.idf[idx] = np.log((self.doc_count - df + 0.5) / (df + 0.5) + 1.0)
            
        print(f"   ✅ Vocabulario: {len(self.vocab)} términos")
        
    def transform(self, text: str) -> models.SparseVector:
        """Generate sparse vector for text"""
        tokens = tokenize_legal(text)
        term_freq = Counter(tokens)
        
        indices = []
        values = []
        
        for term, freq in term_freq.items():
            if term in self.vocab:
                idx = self.vocab[term]
                # BM25 score (simplified: k1=1.5, b=0.75)
                score = self.idf.get(idx, 0) * freq / (freq + 1.5)
                if score > 0.01:  # Threshold
                    indices.append(idx)
                    values.append(float(score))
                    
        return models.SparseVector(indices=indices, values=values)

# 3. Extraer datos del snapshot
print("\n3. Extrayendo snapshot...")
print(f"   Archivo: {SNAPSHOT_PATH.name}")
print(f"   Tamaño: {SNAPSHOT_PATH.stat().st_size / 1024 / 1024:.1f} MB")

# Read snapshot (it's a tarball)
points_data = []

try:
    with tarfile.open(SNAPSHOT_PATH, 'r') as tar:
        # Find collections JSON
        for member in tar.getmembers():
            if 'collections' in member.name and member.name.endswith('.json'):
                f = tar.extractfile(member)
                if f:
                    data = json.load(f)
                    print(f"   ✅ Metadata cargado: {member.name}")
                    
        # Extract points
        for member in tar.getmembers():
            if 'points' in member.name or 'segments' in member.name:
                print(f"   📦 Procesando: {member.name}")
                # Note: Qdrant snapshots use binary format
                # Necesitaríamos Qdrant CLI restore o API
                
except Exception as e:
    print(f"   ⚠️ Error extrayendo snapshot directo: {e}")
    print("   → Usando API Qdrant para restore")

# 4. Método alternativo: Restore via Qdrant API
print("\n4. Restore snapshot via Qdrant API...")

client = QdrantClient(url=QDRANT_URL)

# Upload snapshot to Qdrant
snapshot_file = SNAPSHOT_PATH.name

try:
    # Use Qdrant's snapshot recovery (requires snapshot in Qdrant's snapshot dir)
    print("   ⚠️ Snapshot debe estar en directorio Qdrant")
    print("   Copiando snapshot a container...")
    
    # Ver método manual abajo
    
except Exception as e:
    print(f"   Error: {e}")
    
print("\n" + "=" * 60)
print("SIGUIENTE PASO:")
print("1. Copiar snapshot a Docker container:")
print(f"   docker cp '{SNAPSHOT_PATH}' opositaia-qdrant:/qdrant/snapshots/")
print("")
print("2. Ejecutar script parte 2 (create_hybrid_qdrant_part2.py)")
print("=" * 60)
