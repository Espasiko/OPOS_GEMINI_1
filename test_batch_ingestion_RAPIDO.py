#!/usr/bin/env python3
"""
TEST RÁPIDO: 1 artículo, batches de 50
"""

import sys
sys.path.append('/home/spas/OPOS_GEMINI_1')

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, SparseVector
import hashlib

# Config
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"

def test_batch_ingestion():
    """Test con 1 artículo chunkeado en 3 partes"""
    
    print("🧪 TEST RÁPIDO - Ingesta con batches")
    print("=" * 60)
    
    # Cliente Qdrant
    client = QdrantClient(url=QDRANT_URL, timeout=300)
    
    # Modelo embeddings
    print("\n📦 Cargando modelo embeddings...")
    model = SentenceTransformer('pablosi/bge-m3-spa-law-qa-trained-2')
    print("✅ Modelo cargado")
    
    # Crear 3 chunks de prueba (simulando 1 artículo)
    chunks = [
        {
            "text": "Artículo 173 LGSS. La cuantía del subsidio de IT será del 60% de la base reguladora.",
            "boe_id": "BOE-A-2015-11724",
            "article_title": "Artículo 173",
            "chunk_index": 0
        },
        {
            "text": "A partir del día 21 de baja, el subsidio será del 75% de la base reguladora.",
            "boe_id": "BOE-A-2015-11724",
            "article_title": "Artículo 173",
            "chunk_index": 1
        },
        {
            "text": "El pago del subsidio corresponde al empresario durante los primeros 15 días.",
            "boe_id": "BOE-A-2015-11724",
            "article_title": "Artículo 173",
            "chunk_index": 2
        }
    ]
    
    print(f"\n📝 Chunks de prueba: {len(chunks)}")
    
    # Simular ingesta con batches de 2 (para probar el batching)
    BATCH_SIZE = 2
    total_chunks = len(chunks)
    
    for batch_start in range(0, total_chunks, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total_chunks)
        batch_chunks = chunks[batch_start:batch_end]
        batch_num = (batch_start // BATCH_SIZE) + 1
        total_batches = (total_chunks + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"\n📦 Batch {batch_num}/{total_batches} ({batch_start+1}-{batch_end}/{total_chunks})")
        
        points = []
        
        for chunk in batch_chunks:
            # Embeddings
            dense_vector = model.encode(chunk['text']).tolist()
            
            # Sparse vector simple (sin vocabulario, solo para test)
            sparse_vector = SparseVector(indices=[1, 2, 3], values=[0.5, 0.3, 0.2])
            
            # ID único
            chunk_id = hashlib.md5(
                f"{chunk['boe_id']}_{chunk['article_title']}_{chunk['chunk_index']}".encode()
            ).hexdigest()
            
            point = PointStruct(
                id=chunk_id,
                vector={
                    "dense": dense_vector,
                    "text": sparse_vector
                },
                payload={
                    "boe_id": chunk["boe_id"],
                    "article_title": chunk["article_title"],
                    "text": chunk["text"],
                    "chunk_index": chunk["chunk_index"]
                }
            )
            
            points.append(point)
        
        # Upsert batch
        try:
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=points,
                wait=True
            )
            print(f"   ✅ Batch {batch_num} ingresado ({len(points)} chunks)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    # Verificar
    print(f"\n🔍 Verificando ingesta...")
    count = client.count(COLLECTION_NAME)
    print(f"   Chunks en Qdrant: {count.count}")
    
    if count.count >= 3:
        print("\n✅ TEST EXITOSO - Batches funcionan correctamente")
        return True
    else:
        print(f"\n❌ TEST FALLIDO - Solo {count.count}/3 chunks guardados")
        return False

if __name__ == "__main__":
    success = test_batch_ingestion()
    sys.exit(0 if success else 1)
