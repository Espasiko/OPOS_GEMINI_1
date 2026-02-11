#!/usr/bin/env python3
"""
Generar y guardar vocabulario BM25 desde colección híbrida
Para reutilizar en comparaciones
"""

import os
import sys
import json
import pickle
from pathlib import Path
from collections import Counter
from typing import List
import numpy as np
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env.backend")

print("=" * 70)
print("GENERANDO VOCABULARIO BM25 DESDE COLECCIÓN HÍBRIDA")
print("=" * 70)

# Connect
client = QdrantClient(url="http://localhost:6333", timeout=30.0)

# Tokenizer
def tokenize_legal(text: str) -> List[str]:
    import re
    text = text.lower()
    tokens = re.findall(r'[a-záéíóúñ0-9]+', text)
    stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'se', 'por', 'para', 'con', 'un', 'una', 'al', 'lo', 'su', 'sus'}
    return [t for t in tokens if len(t) > 2 and t not in stopwords]

print("\n1. Extrayendo sample de textos...")
sample_texts = []
offset = None
max_sample = 5000  # 5K docs para vocabulario

with tqdm(total=max_sample, desc="Extrayendo") as pbar:
    while len(sample_texts) < max_sample:
        scroll_result = client.scroll(
            collection_name="opositaia_knowledge_hybrid",
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        
        points, next_offset = scroll_result
        
        if not points:
            break
            
        for point in points:
            text = point.payload.get('text_snippet', point.payload.get('text', ''))
            if text:
                sample_texts.append(text)
                pbar.update(1)
                
            if len(sample_texts) >= max_sample:
                break
                
        if next_offset is None:
            break
            
        offset = next_offset

print(f"   ✅ {len(sample_texts):,} textos extraídos")

print("\n2. Construyendo vocabulario BM25...")
doc_freq = Counter()
total_len = 0

for text in tqdm(sample_texts, desc="Procesando"):
    tokens = tokenize_legal(text)
    total_len += len(tokens)
    for token in set(tokens):
        doc_freq[token] += 1

# Top 20K términos
vocab = {word: idx for idx, (word, _) in enumerate(doc_freq.most_common(20000))}

# IDF
num_docs = len(sample_texts)
avgdl = total_len / max(num_docs, 1)

idf = {}
for word, idx in vocab.items():
    df = doc_freq[word]
    idf[idx] = np.log((num_docs - df + 0.5) / (df + 0.5) + 1.0)

print(f"   ✅ Vocabulario: {len(vocab):,} términos")
print(f"   ✅ avgdl: {avgdl:.1f} tokens")

# Guardar
output_vocab = Path("backend/data/bm25_vocab.pkl")
output_vocab.parent.mkdir(parents=True, exist_ok=True)

with open(output_vocab, 'wb') as f:
    pickle.dump({
        'vocab': vocab,
        'idf': idf,
        'avgdl': avgdl,
        'k1': 1.5,
        'b': 0.75
    }, f)

print(f"\n✅ Vocabulario guardado: {output_vocab}")

# Guardar también JSON legible
with open(output_vocab.with_suffix('.json'), 'w') as f:
    json.dump({
        'vocab_size': len(vocab),
        'avgdl': avgdl,
        'top_20_terms': list(vocab.keys())[:20]
    }, f, indent=2, ensure_ascii=False)

print(f"✅ Metadata guardado: {output_vocab.with_suffix('.json')}")
print("=" * 70)
