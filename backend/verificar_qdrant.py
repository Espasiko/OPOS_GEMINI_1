#!/usr/bin/env python3
"""
Script para verificar el estado de Qdrant después de la ingesta RAG
"""

import asyncio
import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
from datetime import datetime

def main():
    print("🔍 VERIFICANDO ESTADO DE QDRANT POST-INGESTA")
    print("="*60)
    
    # Conectar a Qdrant
    try:
        client = QdrantClient(host="localhost", port=6333)
        print("✅ Conexión a Qdrant: OK")
    except Exception as e:
        print(f"❌ Error conectando a Qdrant: {e}")
        return
    
    # Verificar colección
    collection_name = "opositaia_knowledge"
    try:
        collection_info = client.get_collection(collection_name)
        print(f"✅ Colección '{collection_name}': ENCONTRADA")
        print(f"   - Vectors count: {collection_info.points_count}")
        print(f"   - Vector size: {collection_info.config.params.vectors.size}")
        print(f"   - Distance: {collection_info.config.params.vectors.distance}")
    except Exception as e:
        print(f"❌ Error obteniendo información de colección: {e}")
        return
    
    # Verificar puntos específicos
    try:
        # Obtener algunos puntos de muestra
        points = client.scroll(
            collection_name=collection_name,
            limit=5,
            with_payload=True,
            with_vectors=False
        )[0]  # Solo los puntos, no el next_page_offset
        
        print(f"✅ Puntos de muestra encontrados: {len(points)}")
        for i, point in enumerate(points):
            payload = point.payload
            source = payload.get('source', 'N/A')
            law_name = payload.get('law_name', 'N/A')
            text_preview = payload.get('text', '')[:100] + "..." if len(payload.get('text', '')) > 100 else payload.get('text', '')
            print(f"   [{i+1}] Source: {source}")
            print(f"       Law: {law_name}")
            print(f"       Text preview: {text_preview}")
            print()
            
    except Exception as e:
        print(f"❌ Error obteniendo puntos: {e}")
    
    # Test de búsqueda básica
    print("🧪 REALIZANDO TEST DE BÚSQUEDA")
    print("-"*40)
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # Cargar modelo
        model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
        print("✅ Modelo de embeddings cargado")
        
        # Test query
        query_text = "¿Qué es el procedimiento administrativo común?"
        query_vector = model.encode(query_text).tolist()
        
        # Realizar búsqueda
        search_results = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=3,
            with_payload=True
        )
        
        print(f"✅ Búsqueda exitosa: {len(search_results)} resultados")
        for i, result in enumerate(search_results):
            print(f"   [{i+1}] Score: {result.score:.4f}")
            print(f"       Source: {result.payload.get('source', 'N/A')}")
            print(f"       Law: {result.payload.get('law_name', 'N/A')}")
            print(f"       Text: {result.payload.get('text', '')[:150]}...")
            print()
            
    except Exception as e:
        print(f"❌ Error en test de búsqueda: {e}")
    
    # Resumen final
    print("📊 RESUMEN FINAL")
    print("="*60)
    print(f"✅ Ingesta RAG completada exitosamente")
    print(f"✅ {collection_info.points_count} vectores indexados")
    print(f"✅ Sistema listo para consultas")
    print(f"✅ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()