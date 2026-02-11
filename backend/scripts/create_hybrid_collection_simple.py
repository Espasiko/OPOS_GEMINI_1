#!/usr/bin/env python3
"""
Crear colección híbrida SIMPLE en Qdrant local
Estrategia: Crear nueva colección híbrida vacía, luego migrar datos manualmente
"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

# Load env
load_dotenv(Path(__file__).parent.parent / ".env.backend")

print("=" * 60)
print("CREAR COLECCIÓN HÍBRIDA - QDRANT LOCAL")
print("=" * 60)

# Connect to LOCAL Qdrant
client_local = QdrantClient(url="http://localhost:6333")

# Connect to CLOUD Qdrant (para copiar data)
client_cloud = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

NEW_COLLECTION = "opositaia_knowledge_hybrid"

print(f"\n1. Verificando estado actual...")
collections_local = [c.name for c in client_local.get_collections().collections]
print(f"   Colecciones locales: {collections_local}")

if NEW_COLLECTION in collections_local:
    print(f"   ⚠️  Colección {NEW_COLLECTION} ya existe")
    response = input("   ¿Eliminar y recrear? (y/n): ")
    if response.lower() == 'y':
        client_local.delete_collection(NEW_COLLECTION)
        print("   ✅ Colección eliminada")
    else:
        print("   ❌ Cancelado")
        sys.exit(0)

print(f"\n2. Creando colección híbrida...")

try:
    client_local.create_collection(
        collection_name=NEW_COLLECTION,
        vectors_config={
            "dense": models.VectorParams(
                size=1024,  # BGE-M3
                distance=models.Distance.COSINE
            )
        },
        sparse_vectors_config={
            "text": models.SparseVectorParams()  # BM25-like
        }
    )
    print(f"   ✅ Colección {NEW_COLLECTION} creada")
    print("   - Dense vector: 1024 dims (Cosine)")
    print("   - Sparse vector: 'text' (BM25)")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print(f"\n3. Verificando colección...")
info = client_local.get_collection(NEW_COLLECTION)
print(f"   Status: {info.status}")
print(f"   Points: {info.points_count}")

print("\n" + "=" * 60)
print("✅ COLECCIÓN HÍBRIDA CREADA")
print("\nPróximo paso:")
print("  python backend/scripts/migrate_cloud_to_hybrid_local.py")
print("=" * 60)
