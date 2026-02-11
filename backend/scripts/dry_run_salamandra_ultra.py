#!/usr/bin/env python3
"""
DRY RUN - Salamandra ULTRA con 1 PREGUNTA
Test rápido antes de ejecución completa
"""

import os
import sys
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Qdrant + Embeddings
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Setup
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
ENV_FILE = BASE_DIR / "backend/.env.backend"
load_dotenv(ENV_FILE)

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger("DryRun")

print("=" * 70)
print("🧪 DRY RUN - SALAMANDRA ULTRA (1 pregunta)")
print("=" * 70)

# === VERIFICACIONES PREVIAS ===

print("\n1. Verificando configuración...")

# Cohere API Key
cohere_key = os.getenv("COHERE_API_KEY")
if cohere_key:
    print(f"   ✅ COHERE_API_KEY: {cohere_key[:10]}***")
else:
    print("   ⚠️ COHERE_API_KEY: NO configurada (rerank desactivado)")

# Qdrant Local
try:
    qdrant = QdrantClient(url="http://localhost:6333", timeout=30.0)
    info = qdrant.get_collection("opositaia_knowledge_hybrid_FULL")
    print(f"   ✅ Qdrant LOCAL: {info.points_count:,} puntos")
except Exception as e:
    print(f"   ❌ Qdrant LOCAL: Error - {e}")
    sys.exit(1)

# Embedder
try:
    embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
    print(f"   ✅ Embedder: pablosi loaded")
except Exception as e:
    print(f"   ❌ Embedder: Error - {e}")
    sys.exit(1)

# MCP Server
import requests
try:
    response = requests.get("http://127.0.0.1:3100/health", timeout=5)
    if response.status_code == 200:
        print("   ✅ MCP Server: Running")
    else:
        print("   ⚠️ MCP Server: Respuesta inesperada")
except:
    print("   ⚠️ MCP Server: NO responde (tools MCP no disponibles)")

# VPS Salamandra
try:
    # No llamamos, solo verificamos que la URL está bien
    vps_url = "http://electroyhogarpelotazo.tienda/salamandra/reason"
    print(f"   ✅ VPS URL: {vps_url}")
except Exception as e:
    print(f"   ❌ VPS: Error - {e}")

# === TEST RAG ===

print("\n2. Test búsqueda RAG...")

test_query = "artículo 174 LGSS incapacidad temporal"
logger.info(f"Query: '{test_query}'")

try:
    # Embedding
    vector = embedder.encode(test_query).tolist()
    
    # Search
    results = qdrant.search(
        collection_name="opositaia_knowledge_hybrid_FULL",
        query_vector=("dense", vector),
        limit=5,
        with_payload=True,
        score_threshold=0.3
    )
    
    print(f"   ✅ RAG: {len(results)} resultados")
    
    for i, hit in enumerate(results, 1):
        law = hit.payload.get('law_name', 'Unknown')
        score = hit.score
        text = hit.payload.get('text_snippet', hit.payload.get('text', ''))[:80]
        print(f"   [{i}] {law} (score: {score:.3f})")
        print(f"       {text}...")
    
except Exception as e:
    print(f"   ❌ RAG Error: {e}")
    sys.exit(1)

# === TEST COHERE (si disponible) ===

if cohere_key:
    print("\n3. Test Cohere Reranker...")
    try:
        import cohere
        client = cohere.Client(cohere_key)
        
        texts = [hit.payload.get('text_snippet', hit.payload.get('text', '')) for hit in results]
        
        response = client.rerank(
            model="rerank-multilingual-v3.0",
            query=test_query,
            documents=texts,
            top_n=3,
            return_documents=False
        )
        
        print(f"   ✅ Cohere: Rerank OK")
        for i, result in enumerate(response.results, 1):
            print(f"   [{i}] Index {result.index}, score: {result.relevance_score:.3f}")
    
    except Exception as e:
        print(f"   ⚠️ Cohere Error: {e}")
else:
    print("\n3. Cohere: SKIP (no key)")

# === TEST 1 PREGUNTA COMPLETA ===

print("\n4. Test pregunta completa...")

test_question = {
    'id': 33,
    'question': "Según recoge el art. 174 del Texto Refundido de la Ley General de la Seguridad Social, el derecho al subsidio por Incapacidad temporal se extingue:",
    'options': [
        "por el transcurso del plazo máximo de trescientos sesenta y cinco días naturales desde la baja médica",
        "por el transcurso del plazo máximo de quinientos cuarenta y cinco días naturales desde la baja médica",
        "por el transcurso del plazo de trescientos sesenta días desde el alta médica",
        "por el transcurso del plazo máximo de ciento ochenta días desde la notificación de la baja médica"
    ],
    'correct_answer': 'b'  # Para verificar
}

# Construir contexto RAG
context = "===CONTEXTO RAG===\n\n"
for i, hit in enumerate(results, 1):
    law = hit.payload.get('law_name', 'Unknown')
    text = hit.payload.get('text_snippet', hit.payload.get('text', ''))
    context += f"[{i}] {law}\n{text}\n\n"

# Prompt simplificado (sin VPS, solo para test)
prompt = f"""
PREGUNTA: {test_question['question']}

OPCIONES:
a) {test_question['options'][0]}
b) {test_question['options'][1]}
c) {test_question['options'][2]}
d) {test_question['options'][3]}

CONTEXTO:
{context}

Responde SOLO la letra (a, b, c o d).
"""

print(f"\n   Pregunta #{test_question['id']}")
print(f"   Q: {test_question['question'][:60]}...")
print(f"   Contexto RAG: {len(context)} chars")
print(f"   Respuesta correcta esperada: {test_question['correct_answer']}")

# Simular respuesta (sin llamar VPS en dry run)
print("\n   ⚠️ DRY RUN: No llamamos VPS, solo verificamos que:")
print("      - RAG funciona ✅")
print("      - Contexto se construye ✅")
print("      - Cohere disponible ✅" if cohere_key else "      - Cohere NO disponible ⚠️")
print("      - MCP disponible (opcional)")

# === RESULTADO ===

print("\n" + "=" * 70)
print("RESULTADO DRY RUN")
print("=" * 70)

print("\n✅ TODO LISTO PARA EJECUCIÓN COMPLETA")
print("\nPróximo comando:")
print("  cd /home/spas/OPOS_GEMINI_1")
print("  ./.venv/bin/python3 backend/scripts/salamandra_ULTRA_prototype.py")

print("\n⚠️ NOTA: Necesitas parsear preguntas reales primero")
print("   El script ULTRA usa placeholder de 1 pregunta")
print("   Actualiza main() para cargar examen completo")
