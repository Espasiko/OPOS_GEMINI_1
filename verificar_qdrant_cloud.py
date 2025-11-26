#!/usr/bin/env python3
"""
Verificar contenido de Qdrant Cloud
"""
import os
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

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
    timeout=30
)

# Obtener información de la colección
try:
    collection_info = client.get_collection(collection_name)
    print(f"✅ Colección encontrada: {collection_name}")
    print(f"📊 Total de puntos: {collection_info.points_count}")
    
    # Manejar diferentes estructuras de config
    try:
        if hasattr(collection_info.config.params.vectors, 'size'):
            vector_size = collection_info.config.params.vectors.size
        elif isinstance(collection_info.config.params.vectors, dict):
            vector_size = collection_info.config.params.vectors.get('size', 'N/A')
        else:
            vector_size = 'N/A'
        print(f"📏 Dimensión de vectores: {vector_size}")
    except:
        print(f"📏 Dimensión de vectores: N/A")
    
    print(f"🔢 Segmentos: {collection_info.segments_count}\n")
    
    # Obtener algunos puntos de ejemplo para ver los metadatos
    print("📝 Obteniendo puntos de ejemplo...")
    scroll_result = client.scroll(
        collection_name=collection_name,
        limit=10,
        with_payload=True,
        with_vectors=False
    )
    
    points = scroll_result[0]
    
    if points:
        print(f"\n✅ Encontrados {len(points)} puntos de ejemplo\n")
        
        # Analizar metadatos únicos
        normas = set()
        tipos = set()
        
        for point in points:
            payload = point.payload
            if 'norma' in payload:
                normas.add(payload['norma'])
            if 'tipo' in payload:
                tipos.add(payload['tipo'])
        
        print(f"📚 Normas encontradas en la muestra:")
        for norma in sorted(normas):
            print(f"  - {norma}")
        
        print(f"\n📑 Tipos de documento encontrados:")
        for tipo in sorted(tipos):
            print(f"  - {tipo}")
        
        # Mostrar un ejemplo completo
        print(f"\n📄 Ejemplo de punto (primero):")
        example = points[0]
        print(f"  ID: {example.id}")
        print(f"  Payload: {example.payload}")
    else:
        print("⚠️  No se encontraron puntos en la colección")
    
    # Saltar búsqueda de prueba por ahora
    
    # Contar documentos por norma
    print(f"\n📊 Contando documentos por norma...")
    
    # Obtener más puntos para análisis
    all_normas = {}
    offset = None
    batch_size = 100
    total_checked = 0
    
    while total_checked < min(1000, collection_info.points_count):  # Limitar a 1000 para no tardar mucho
        scroll_result = client.scroll(
            collection_name=collection_name,
            limit=batch_size,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        
        points, offset = scroll_result
        
        if not points:
            break
        
        for point in points:
            norma = point.payload.get('norma', 'Desconocida')
            all_normas[norma] = all_normas.get(norma, 0) + 1
        
        total_checked += len(points)
        
        if offset is None:
            break
    
    print(f"\n📈 Distribución de documentos (primeros {total_checked} puntos):")
    for norma, count in sorted(all_normas.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_checked) * 100
        print(f"  {norma}: {count} docs ({percentage:.1f}%)")
    
    print(f"\n✅ Verificación completada")
    print(f"📊 Total de normas diferentes: {len(all_normas)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
