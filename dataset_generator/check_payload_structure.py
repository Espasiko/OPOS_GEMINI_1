#!/usr/bin/env python3
"""Script para verificar estructura de payloads en Qdrant"""

from qdrant_client import QdrantClient
import json

client = QdrantClient("http://localhost:6333")

points, _ = client.scroll(
    collection_name="materiales_academia",
    limit=3,
    with_payload=True,
    with_vectors=False
)

print("Estructura de payloads:\n")
for i, point in enumerate(points, 1):
    print(f"--- Punto {i} ---")
    print(json.dumps(point.payload, indent=2, ensure_ascii=False))
    print()
