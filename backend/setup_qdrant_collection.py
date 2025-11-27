"""
Setup Qdrant Collection for OpositaIA
Creates unified collection with 768 dimensions (RoBERTalex)
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

def create_collection():
    """Create opositaia_unified collection in Qdrant"""
    client = QdrantClient(url="http://localhost:6333")
    
    collection_name = "opositaia_unified"
    
    # Delete if exists
    try:
        client.delete_collection(collection_name)
        print(f"✅ Colección anterior '{collection_name}' eliminada")
    except Exception:
        print(f"ℹ️  No había colección anterior '{collection_name}'")
    
    # Create new collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=768,  # RoBERTalex dimension
            distance=Distance.COSINE
        )
    )
    
    print(f"✅ Colección '{collection_name}' creada exitosamente")
    print(f"   - Dimensión: 768 (RoBERTalex)")
    print(f"   - Distancia: COSINE")
    
    # Verify
    collection_info = client.get_collection(collection_name)
    print(f"\n📊 Información de la colección:")
    print(f"   - Nombre: {collection_info.config.params.vectors.size}")
    print(f"   - Puntos: {collection_info.points_count}")
    print(f"   - Estado: OK")

if __name__ == "__main__":
    create_collection()
