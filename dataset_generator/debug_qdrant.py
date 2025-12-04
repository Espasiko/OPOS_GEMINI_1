#!/usr/bin/env python3
from qdrant_client import QdrantClient

c = QdrantClient('http://localhost:6333')

print("=== VERIFICANDO COLECCIONES ===\n")

# Ver colecciones
for col in c.get_collections().collections:
    info = c.get_collection(col.name)
    print(f"{col.name}: {info.points_count} puntos")

# Ver estructura de datos en opositaia_leyes
print("\n=== MUESTRA DE opositaia_leyes_seguridad_social ===")
try:
    points, _ = c.scroll("opositaia_leyes_seguridad_social", limit=2, with_payload=True)
    for p in points:
        print(f"\nID: {p.id}")
        print(f"Keys: {list(p.payload.keys())}")
        for k, v in p.payload.items():
            val = str(v)[:100] if v else "None"
            print(f"  {k}: {val}")
except Exception as e:
    print(f"Error: {e}")

# Ver estructura de materiales_academia
print("\n=== MUESTRA DE materiales_academia ===")
try:
    points, _ = c.scroll("materiales_academia", limit=2, with_payload=True)
    for p in points:
        print(f"\nID: {p.id}")
        print(f"Keys: {list(p.payload.keys())}")
        for k, v in p.payload.items():
            val = str(v)[:100] if v else "None"
            print(f"  {k}: {val}")
except Exception as e:
    print(f"Error: {e}")
