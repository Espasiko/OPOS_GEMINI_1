#!/usr/bin/env python3
"""
Script simple para verificar Qdrant Cloud
"""
import os
import sys

# Agregar el path del backend al PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Cargar variables de entorno
load_dotenv('backend/.env.backend')

# Conectar a Qdrant Cloud
qdrant_url = os.getenv('QDRANT_URL')
qdrant_api_key = os.getenv('QDRANT_API_KEY')
collection_name = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print(f"🔍 Conectando a Qdrant Cloud...")
print(f"URL: {qdrant_url}")
print(f"Collection: {collection_name}\n")

try:
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=30
    )
    
    # Listar colecciones
    print("📚 Colecciones disponibles:")
    collections = client.get_collections()
    for col in collections.collections:
        print(f"  - {col.name}")
    
    print()
    
    # Obtener información de la colección principal
    collection_info = client.get_collection(collection_name)
    print(f"✅ Colección: {collection_name}")
    print(f"📊 Total de puntos: {collection_info.points_count:,}")
    print(f"🔢 Segmentos: {collection_info.segments_count}")
    
    # Obtener tamaño aproximado
    # Cada vector de 768 dimensiones = 768 * 4 bytes (float32) = 3,072 bytes = 3 KB
    # Más metadata ~1 KB por punto
    estimated_size_mb = (collection_info.points_count * 4) / 1024  # Aproximado
    print(f"💾 Tamaño estimado: ~{estimated_size_mb:.2f} MB")
    
    print(f"\n📝 Obteniendo muestra de puntos...")
    
    # Obtener muestra de puntos
    scroll_result = client.scroll(
        collection_name=collection_name,
        limit=100,
        with_payload=True,
        with_vectors=False
    )
    
    points = scroll_result[0]
    
    if points:
        print(f"✅ Muestra obtenida: {len(points)} puntos\n")
        
        # Analizar capas
        capas = {}
        normas = {}
        tipos = {}
        
        for point in points:
            payload = point.payload
            
            # Contar por capa
            layer = payload.get('layer', 'Sin capa')
            capas[layer] = capas.get(layer, 0) + 1
            
            # Contar por norma
            norma = payload.get('norma', 'N/A')
            normas[norma] = normas.get(norma, 0) + 1
            
            # Contar por tipo
            tipo = payload.get('tipo', 'Desconocido')
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        print("🔢 DISTRIBUCIÓN POR CAPAS (muestra de 100):")
        for capa in sorted(capas.keys()):
            count = capas[capa]
            pct = (count / len(points)) * 100
            print(f"  Capa {capa}: {count} docs ({pct:.1f}%)")
        
        print("\n📚 NORMAS ENCONTRADAS (muestra de 100):")
        for norma, count in sorted(normas.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(points)) * 100
            print(f"  {norma}: {count} docs ({pct:.1f}%)")
        
        print("\n📑 TIPOS DE DOCUMENTO (muestra de 100):")
        for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(points)) * 100
            print(f"  {tipo}: {count} docs ({pct:.1f}%)")
        
        # Mostrar ejemplo de punto
        print(f"\n📄 EJEMPLO DE PUNTO:")
        example = points[0]
        print(f"  ID: {example.id}")
        print(f"  Payload keys: {list(example.payload.keys())}")
        print(f"  Layer: {example.payload.get('layer', 'N/A')}")
        print(f"  Tipo: {example.payload.get('tipo', 'N/A')}")
        print(f"  Norma: {example.payload.get('norma', 'N/A')}")
        if 'text' in example.payload:
            text_preview = example.payload['text'][:200] + "..." if len(example.payload['text']) > 200 else example.payload['text']
            print(f"  Text preview: {text_preview}")
    
    print(f"\n✅ Verificación completada exitosamente")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
