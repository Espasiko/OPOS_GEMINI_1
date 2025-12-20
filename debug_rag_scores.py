
import os
import sys
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge"
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
TEST_QUERY = "incapacidad temporal duración máxima"

def debug_rag():
    print(f"🔍 Diagnosticando RAG...")
    print(f"  URL: {QDRANT_URL}")
    print(f"  Colección: {COLLECTION_NAME}")
    print(f"  Modelo: {EMBEDDING_MODEL}")
    
    # 1. Conectar a Qdrant
    client = QdrantClient(url=QDRANT_URL)
    
    # Verificar colección
    try:
        collections = client.get_collections()
        exists = any(c.name == COLLECTION_NAME for c in collections.collections)
        if not exists:
            print(f"❌ La colección {COLLECTION_NAME} NO existe en Qdrant!")
            return
        
        info = client.get_collection(COLLECTION_NAME)
        print(f"✅ Colección encontrada. Puntos: {info.points_count}")
        print(f"   Configuración vectores: {info.config.params.vectors}")
    except Exception as e:
        print(f"❌ Error conectando a Qdrant: {e}")
        return

    # 2. Cargar modelo y generar embedding
    print(f"\n🧠 Cargando modelo {EMBEDDING_MODEL}...")
    try:
        model = SentenceTransformer(EMBEDDING_MODEL)
        query_vector = model.encode([TEST_QUERY])[0].tolist()
        print(f"✅ Embedding generado. Dimensión: {len(query_vector)}")
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return

    # 3. Buscar en Qdrant (RAW SEARCH)
    print(f"\n🔎 Buscando '{TEST_QUERY}' en Qdrant (sin filtros)...")
    try:
        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=5,
            using="dense", # Asegurarnos de usar el vector nombrado correcto si existe, o None si es default
            with_payload=True
        ).points
        
        print(f"📊 Resultados encontrados: {len(results)}")
        for i, res in enumerate(results):
            print(f"\n  Result #{i+1}:")
            print(f"    SCORE: {res.score}")
            print(f"    ID: {res.id}")
            payload = res.payload
            text = payload.get('text', 'No text found')[:100] + "..."
            print(f"    TEXT: {text}")
            print(f"    METADATA: {payload.get('metadata', {})}")
            
    except Exception as e:
        print(f"❌ Error buscando en Qdrant: {e}")
        # Intentar búsqueda sin vector nombrado "dense" por si acaso es vector default
        try:
            print("   Intentando búsqueda en vector default...")
            results = client.query_points(
                collection_name=COLLECTION_NAME,
                query=query_vector,
                limit=5,
                with_payload=True
            ).points
            print(f"   📊 Resultados (vector default): {len(results)}")
            if results:
                print(f"   SCORE TOP 1: {results[0].score}")
        except Exception as e2:
            print(f"   ❌ También falló vector default: {e2}")

if __name__ == "__main__":
    debug_rag()
