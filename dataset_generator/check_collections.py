#!/usr/bin/env python3
from qdrant_client import QdrantClient
c = QdrantClient('http://localhost:6333')
collections = c.get_collections().collections
print("=== COLECCIONES EN QDRANT ===")
for col in collections:
    info = c.get_collection(col.name)
    print(f"  - {col.name}: {info.points_count} puntos")
