#!/usr/bin/env python3
"""
Verifica estado de Qdrant local
"""
from qdrant_client import QdrantClient

def main():
    client = QdrantClient(url='http://localhost:6333')
    
    print("=== COLECCIONES EN QDRANT LOCAL ===\n")
    
    collections = client.get_collections()
    
    if not collections.collections:
        print("❌ No hay colecciones en Qdrant")
        return
    
    for i, col in enumerate(collections.collections, 1):
        print(f"{i}. Colección: {col.name}")
        
        # Obtener info detallada
        try:
            info = client.get_collection(col.name)
            count = client.count(col.name)
            
            print(f"   Puntos: {count.count}")
            print(f"   Vectores: {info.config.params.vectors}")
            
            # Obtener muestra
            if count.count > 0:
                sample = client.scroll(col.name, limit=1, with_payload=True)
                if sample[0]:
                    payload_keys = list(sample[0][0].payload.keys())
                    print(f"   Payload keys: {payload_keys[:5]}...")  # Primeros 5
        except Exception as e:
            print(f"   Error: {e}")
        print()

if __name__ == "__main__":
    main()
