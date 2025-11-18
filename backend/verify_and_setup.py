"""
Verification and Setup Script for OpositaIA RAG
Step-by-step verification before indexing
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import sys

def check_qdrant_connection():
    """Check if Qdrant is running"""
    print("🔍 PASO 1: Verificando conexión a Qdrant...")
    try:
        client = QdrantClient(url="http://localhost:6333")
        collections = client.get_collections()
        print(f"✅ Qdrant está corriendo")
        print(f"   Colecciones existentes: {len(collections.collections)}")
        for col in collections.collections:
            print(f"   - {col.name}: {col.points_count} puntos")
        return client
    except Exception as e:
        print(f"❌ Error conectando a Qdrant: {e}")
        print("   Asegúrate de que Qdrant está corriendo:")
        print("   wsl docker-compose up -d qdrant")
        sys.exit(1)

def clean_all_collections(client):
    """Delete ALL collections to start fresh"""
    print("\n🧹 PASO 2: Limpiando TODAS las colecciones...")
    collections = client.get_collections()
    
    if len(collections.collections) == 0:
        print("ℹ️  No hay colecciones para limpiar")
        return
    
    for col in collections.collections:
        print(f"   Eliminando: {col.name} ({col.points_count} puntos)")
        client.delete_collection(col.name)
    
    print(f"✅ {len(collections.collections)} colecciones eliminadas")

def create_opositaia_collection(client):
    """Create opositaia_leyes_seguridad_social collection"""
    print("\n📦 PASO 3: Creando colección 'opositaia_leyes_seguridad_social'...")
    
    collection_name = "opositaia_leyes_seguridad_social"
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=768,  # RoBERTalex dimension
            distance=Distance.COSINE
        )
    )
    
    print(f"✅ Colección '{collection_name}' creada")
    print(f"   - Dimensión: 768 (RoBERTalex)")
    print(f"   - Distancia: COSINE")
    print(f"   - Nombre descriptivo: ✅")
    
    # Verify
    collection_info = client.get_collection(collection_name)
    print(f"\n📊 Verificación:")
    print(f"   - Vectores size: {collection_info.config.params.vectors.size}")
    print(f"   - Puntos actuales: {collection_info.points_count}")
    print(f"   - Estado: OK ✅")

def main():
    print("="*60)
    print("🚀 VERIFICACIÓN Y SETUP - OpositaIA RAG")
    print("="*60)
    
    # Step 1: Check connection
    client = check_qdrant_connection()
    
    # Step 2: Clean all
    clean_all_collections(client)
    
    # Step 3: Create new collection
    create_opositaia_collection(client)
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETADO")
    print("="*60)
    print("\nPróximo paso: Descargar LGSS")
    print("python backend/agents/boe_downloader.py")

if __name__ == "__main__":
    main()
