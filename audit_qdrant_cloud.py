#!/usr/bin/env python3
"""
Auditoría de Qdrant Cloud - Estructura real de colecciones y vectores
"""

from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

# Cargar credenciales
load_dotenv("mcp-server/.env")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

print(f"Conectando a Qdrant Cloud: {QDRANT_URL}")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# 1. Listar todas las colecciones
print("\n" + "="*60)
print("COLECCIONES DISPONIBLES:")
print("="*60)
collections = client.get_collections()
for col in collections.collections:
    print(f"  - {col.name}")

# 2. Inspeccionar la colección específica
target_collection = "opositaia_leyes_seguridad_social"
print(f"\n" + "="*60)
print(f"ESTRUCTURA DE: {target_collection}")
print("="*60)

try:
    collection_info = client.get_collection(target_collection)
    
    print(f"\nVectores configurados:")
    if hasattr(collection_info.config, 'params'):
        params = collection_info.config.params
        if hasattr(params, 'vectors'):
            vectors = params.vectors
            print(f"  Type: {type(vectors)}")
            print(f"  Content: {vectors}")
            
            # Si es un dict, listar cada vector
            if isinstance(vectors, dict):
                for vector_name, vector_config in vectors.items():
                    print(f"\n  Vector Name: '{vector_name}'")
                    print(f"    Size: {vector_config.size if hasattr(vector_config, 'size') else 'N/A'}")
                    print(f"    Distance: {vector_config.distance if hasattr(vector_config, 'distance') else 'N/A'}")
    
    print(f"\nPuntos indexados: {collection_info.points_count}")
    print(f"Segmentos: {collection_info.segments_count}")
    
    # 3. Obtener un punto de ejemplo para ver la estructura
    print(f"\n" + "="*60)
    print("PUNTO DE EJEMPLO:")
    print("="*60)
    
    sample = client.scroll(
        collection_name=target_collection,
        limit=1,
        with_payload=True,
        with_vectors=True
    )
    
    if sample[0]:
        point = sample[0][0]
        print(f"\nID: {point.id}")
        print(f"\nPayload keys: {list(point.payload.keys())}")
        print(f"\nVector keys: {list(point.vector.keys()) if isinstance(point.vector, dict) else 'Single vector'}")
        
        if isinstance(point.vector, dict):
            for vec_name, vec_data in point.vector.items():
                vec_len = len(vec_data) if isinstance(vec_data, list) else "N/A"
                print(f"  - '{vec_name}': {vec_len} dimensions")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
