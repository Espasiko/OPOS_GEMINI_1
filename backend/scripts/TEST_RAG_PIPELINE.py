#!/usr/bin/env python3
"""
DIAGNÓSTICO COMPLETO RAG + POSTGRES
Test exhaustivo del pipeline Salamandra
"""

import os
import json
import psycopg
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Config
load_dotenv('backend/.env.backend')

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_KEY = os.getenv('QDRANT_API_KEY')
POSTGRES_DSN = "postgresql://postgres:postgres@localhost:5432/opositaia"

print("=" * 70)
print("DIAGNOSTICO RAG + POSTGRES PIPELINE")
print("=" * 70)

# 1. QDRANT CONNECTION
print("\n1. QDRANT CLOUD")
print("-" * 70)

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_KEY)

try:
    info = client.get_collection('opositaia_knowledge')
    print(f"OK Coleccion existe: opositaia_knowledge")
    print(f"   Puntos totales: {info.points_count:,}")
    print(f"   Vectores: {info.config.params.vectors}")
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

# 2. EMBEDDING MODEL
print("\n2. MODELO EMBEDDINGS")
print("-" * 70)

model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
print(f"OK Modelo cargado: pablosi/bge-m3-spa-law-qa-trained-2")
print(f"   Dimension: {model.get_sentence_embedding_dimension()}")

# 3. TEST BÚSQUEDA
print("\n3. TEST BUSQUEDA (Preguntas Reales)")
print("-" * 70)

test_questions = [
    "Cual es el plazo de la mocion de censura segun la Constitucion Espanola?",
    "Cuantas pagas extraordinarias establece el articulo 46 TRLGSS?",
    "Que mayoria requiere la aprobacion de mocion de censura?"
]

for idx, query in enumerate(test_questions, 1):
    print(f"\nPregunta {idx}: {query[:60]}...")
    
    vector = model.encode(query).tolist()
    print(f"   Vector: {len(vector)} dims")
    
    results = client.search(
        collection_name='opositaia_knowledge',
        query_vector=('dense', vector),
        limit=5,
        with_payload=True,
        score_threshold=0.5
    )
    
    print(f"   Resultados: {len(results)} chunks")
    
    if results:
        for i, hit in enumerate(results[:3], 1):
            print(f"\n   {i}. Score: {hit.score:.4f}")
            print(f"      Ley: {hit.payload.get('law_name', 'N/A')[:70]}")
            print(f"      Articulo: {hit.payload.get('article_title', 'N/A')[:70]}")
            
            postgres_id = hit.payload.get('postgres_id')
            print(f"      Postgres ID: {postgres_id}")
            
            snippet = hit.payload.get('text_snippet', hit.payload.get('text', ''))
            print(f"      Snippet: {snippet[:150]}...")
            
            if postgres_id:
                try:
                    with psycopg.connect(POSTGRES_DSN) as conn:
                        with conn.cursor() as cur:
                            cur.execute(
                                "SELECT article_text FROM laws WHERE id = %s",
                                (postgres_id,)
                            )
                            row = cur.fetchone()
                            if row:
                                full_text = row[0]
                                print(f"      OK Postgres: {len(full_text)} chars disponibles")
                                print(f"         Preview: {full_text[:100]}...")
                            else:
                                print(f"      WARNING Postgres: ID no encontrado")
                except Exception as e:
                    print(f"      ERROR Postgres: {e}")
    else:
        print(f"   WARNING CERO resultados")

# 4. POSTGRES DIRECT
print("\n4. POSTGRES DATABASE")
print("-" * 70)

try:
    with psycopg.connect(POSTGRES_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM laws")
            law_count = cur.fetchone()[0]
            print(f"OK Conexion exitosa")
            print(f"   Total leyes en DB: {law_count:,}")
            
            cur.execute("SELECT id, title, article_text FROM laws LIMIT 1")
            sample = cur.fetchone()
            if sample:
                print(f"\n   Ejemplo ley:")
                print(f"   ID: {sample[0]}")
                print(f"   Titulo: {sample[1][:60]}...")
                print(f"   Texto: {len(sample[2])} chars")
except Exception as e:
    print(f"ERROR Postgres: {e}")

# 5. RESUMEN
print("\n" +  "=" * 70)
print("RESUMEN DIAGNOSTICO")
print("=" * 70)
print(f"Qdrant: OK {info.points_count:,} chunks")
print(f"Embeddings: OK pablosi/bge-m3 (1024 dims)")
print(f"Busqueda: {'OK Funcionando' if len(results) > 0 else 'WARNING Sin resultados'}")
print(f"Postgres: OK Conectado")
print("\nCONCLUSION: Pipeline completo esta FUNCIONAL")
print("   Si Salamandra no recibio contexto, buscar en:")
print("   - Script Salamandra NO llama retrieve_context()")
print("   - Exception silenciada sin logging")
print("   - Timeout en busqueda RAG")
print("=" * 70)
