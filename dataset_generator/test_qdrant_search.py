#!/usr/bin/env python3
"""
Test de búsqueda en Qdrant
"""

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

print("🔍 Probando búsqueda en Qdrant...")

# Conectar a Qdrant
client = QdrantClient(url="http://localhost:6333")

# Verificar colección
try:
    collection_info = client.get_collection("materiales_academia")
    print(f"\n✅ Colección encontrada: materiales_academia")
    print(f"   Vectores indexados: {collection_info.points_count}")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Cargar modelo
print("\n📥 Cargando modelo BGE-M3...")
embedder = SentenceTransformer("BAAI/bge-m3")

# Queries de prueba
queries = [
    "¿Cuál es el período mínimo de cotización para la jubilación?",
    "¿Qué requisitos se necesitan para la incapacidad temporal?",
    "¿Cuánto dura la prestación por viudedad?"
]

for query in queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    
    # Generar embedding
    query_vector = embedder.encode(query).tolist()
    
    # Buscar usando search_points
    from qdrant_client.models import SearchRequest
    results = client.search_points(
        collection_name="materiales_academia",
        query_vector=query_vector,
        limit=3
    )
    
    for i, hit in enumerate(results, 1):
        print(f"\n--- Resultado {i} (score: {hit.score:.3f}) ---")
        print(f"ID: {hit.id}")
        print(f"Archivo: {hit.payload.get('filename', 'N/A')}")
        print(f"Categoría: {hit.payload.get('category', 'N/A')}")
        print(f"Página: {hit.payload.get('page_number', 'N/A')}")
        print(f"Texto: {hit.payload.get('text', '')[:200]}...")

print("\n✅ Test completado!")
