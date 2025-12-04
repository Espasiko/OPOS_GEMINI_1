"""
Setup Semantic Cache Collection for OpositaIA
Crea la colección qa_cache en Qdrant para caché semántica

Objetivo: Ahorrar 60-70% de llamadas al LLM cacheando respuestas similares
"""
import os
import sys
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Configuración
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COLLECTION_NAME = "qa_cache"
VECTOR_SIZE = 1024  # BGE-M3 dimension


def get_qdrant_client() -> QdrantClient:
    """Obtiene cliente Qdrant"""
    if QDRANT_API_KEY:
        return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    return QdrantClient(url=QDRANT_URL)


def create_cache_collection(force_recreate: bool = False):
    """
    Crea la colección qa_cache para caché semántica.
    
    Args:
        force_recreate: Si True, elimina y recrea la colección
    """
    client = get_qdrant_client()
    
    print(f"🔧 Configurando colección de caché semántica...")
    print(f"   URL: {QDRANT_URL}")
    print(f"   Colección: {COLLECTION_NAME}")
    print(f"   Dimensión: {VECTOR_SIZE} (BGE-M3)")
    
    # Verificar si existe
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)
    
    if exists and not force_recreate:
        print(f"\n✅ Colección '{COLLECTION_NAME}' ya existe")
        info = client.get_collection(COLLECTION_NAME)
        print(f"   Puntos: {info.points_count}")
        return True
    
    # Eliminar si existe y force_recreate
    if exists and force_recreate:
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"🗑️  Colección anterior eliminada")
        except Exception as e:
            print(f"⚠️  Error eliminando: {e}")
    
    # Crear colección
    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
        print(f"\n✅ Colección '{COLLECTION_NAME}' creada exitosamente")
        print(f"   - Dimensión: {VECTOR_SIZE}")
        print(f"   - Distancia: COSINE")
        print(f"   - Uso: Caché semántica de Q&A")
        return True
        
    except Exception as e:
        print(f"\n❌ Error creando colección: {e}")
        return False


def verify_collection():
    """Verifica el estado de la colección"""
    client = get_qdrant_client()
    
    try:
        info = client.get_collection(COLLECTION_NAME)
        print(f"\n📊 Estado de la colección '{COLLECTION_NAME}':")
        print(f"   - Puntos: {info.points_count}")
        print(f"   - Vectores: {info.config.params.vectors.size}D")
        print(f"   - Distancia: {info.config.params.vectors.distance}")
        print(f"   - Estado: ✅ OK")
        return True
    except Exception as e:
        print(f"\n❌ Colección no encontrada: {e}")
        return False


def test_cache_operations():
    """Prueba operaciones básicas de caché"""
    client = get_qdrant_client()
    
    print(f"\n🧪 Probando operaciones de caché...")
    
    # Crear vector de prueba (dummy)
    import random
    test_vector = [random.random() for _ in range(VECTOR_SIZE)]
    
    test_payload = {
        'query': '¿Cuál es la edad de jubilación ordinaria?',
        'query_hash': 'test_hash_123',
        'response': {
            'answer': 'La edad de jubilación ordinaria es 67 años...',
            'sources': ['Art. 205 LGSS']
        },
        'created_at': datetime.now().isoformat(),
        'ttl_days': 30,
        'hit_count': 0
    }
    
    try:
        # Insertar punto de prueba
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=1,
                    vector=test_vector,
                    payload=test_payload
                )
            ]
        )
        print(f"   ✅ Inserción: OK")
        
        # Buscar punto
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=test_vector,
            limit=1
        )
        
        if results and len(results) > 0:
            print(f"   ✅ Búsqueda: OK (score: {results[0].score:.4f})")
        else:
            print(f"   ⚠️  Búsqueda: Sin resultados")
        
        # Eliminar punto de prueba
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=[1]
        )
        print(f"   ✅ Eliminación: OK")
        
        print(f"\n✅ Todas las operaciones funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en operaciones: {e}")
        return False


def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 SETUP SEMANTIC CACHE - OpositaIA")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar argumentos
    force = '--force' in sys.argv or '-f' in sys.argv
    test = '--test' in sys.argv or '-t' in sys.argv
    
    if force:
        print("\n⚠️  Modo FORCE: Se recreará la colección")
    
    # Crear colección
    success = create_cache_collection(force_recreate=force)
    
    if success:
        # Verificar
        verify_collection()
        
        # Test si se solicita
        if test:
            test_cache_operations()
    
    print("\n" + "=" * 60)
    print("✅ Setup completado")
    print("=" * 60)


if __name__ == "__main__":
    main()
