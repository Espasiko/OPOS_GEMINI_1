#!/usr/bin/env python3
"""
Test simple de indexación - Solo crear colección y probar
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

print("🔄 Conectando a Qdrant...")
client = QdrantClient(url="http://localhost:6333")

print("📋 Colecciones existentes:")
collections = client.get_collections()
for col in collections.collections:
    print(f"  - {col.name}")

print("\n📦 Creando colección 'materiales_base'...")
try:
    client.create_collection(
        collection_name="materiales_base",
        vectors_config=VectorParams(
            size=1024,  # BGE-M3
            distance=Distance.COSINE
        )
    )
    print("✅ Colección creada!")
except Exception as e:
    print(f"⚠️  {e}")

print("\n📋 Colecciones después de crear:")
collections = client.get_collections()
for col in collections.collections:
    print(f"  - {col.name}")
