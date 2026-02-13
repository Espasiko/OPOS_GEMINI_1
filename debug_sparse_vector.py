#!/usr/bin/env python3
"""
DEBUG: Probar función generate_sparse_vector
"""

import pickle
from pathlib import Path
from qdrant_client.models import SparseVector

BM25_VOCAB_PATH = Path("/home/spas/OPOS_GEMINI_1/backend/data/bm25_vocab.pkl")

def tokenize_simple(text: str):
    """Tokenización simple por palabras"""
    return text.lower().split()

def generate_sparse_vector(text: str, vocab: dict) -> SparseVector:
    """Genera vector sparse BM25-like"""
    if not vocab:
        print("❌ Vocabulario vacío!")
        return SparseVector(indices=[], values=[])
    
    tokens = tokenize_simple(text)
    print(f"Tokens: {tokens[:10]}")
    
    token_counts = {}
    for token in tokens:
        token_counts[token] = token_counts.get(token, 0) + 1
    
    indices = []
    values = []
    
    for token, count in token_counts.items():
        if token in vocab:
            idx = vocab[token]
            tf = count / len(tokens) if tokens else 0
            indices.append(int(idx))
            values.append(float(tf))
    
    print(f"Términos encontrados en vocab: {len(indices)}/{len(token_counts)}")
    return SparseVector(indices=indices, values=values)

# Cargar vocabulario
print("📚 Cargando vocabulario...")
with open(BM25_VOCAB_PATH, 'rb') as f:
    bm25_data = pickle.load(f)

# El pickle contiene un dict con 'vocab', 'idf', 'avgdl', etc.
if isinstance(bm25_data, dict) and 'vocab' in bm25_data:
    vocab = bm25_data['vocab']
else:
    vocab = bm25_data

print(f"✅ Vocabulario cargado: {len(vocab)} términos")
print(f"Primeros 10: {list(vocab.keys())[:10]}")

# Probar con texto de ejemplo
text = "Artículo 173 de la LGSS. La cuantía del subsidio de incapacidad temporal será del 60% de la base reguladora."

print(f"\n📝 Texto de prueba:")
print(f"   {text}")

sparse_vec = generate_sparse_vector(text, vocab)

print(f"\n✅ Sparse vector generado:")
print(f"   Términos: {len(sparse_vec.indices)}")
print(f"   Índices: {sparse_vec.indices[:10]}")
print(f"   Valores: {sparse_vec.values[:10]}")
