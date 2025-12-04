#!/usr/bin/env python3
"""Test simple de Qdrant"""

from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

# Ver colecciones
collections = client.get_collections()
print("Colecciones disponibles:")
for col in collections.collections:
    print(f"  - {col.name}")

# Info de la colección
info = client.get_collection("materiales_academia")
print(f"\nColección: materiales_academia")
print(f"Vectores: {info.points_count}")
print(f"Dimensión: {info.config.params.vectors.size}")

# Ver algunos puntos
print("\nPrimeros 5 puntos:")
points = client.scroll(
    collection_name="materiales_academia",
    limit=5
)[0]

for point in points:
    print(f"\nID: {point.id}")
    print(f"Archivo: {point.payload.get('filename', 'N/A')}")
    print(f"Categoría: {point.payload.get('category', 'N/A')}")
    print(f"Texto: {point.payload.get('text', '')[:100]}...")
