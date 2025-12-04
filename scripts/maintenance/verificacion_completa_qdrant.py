#!/usr/bin/env python3
"""
Verificación COMPLETA de Qdrant Cloud
Analiza TODOS los documentos, no solo una muestra
"""
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv('backend/.env.backend')

qdrant_url = os.getenv('QDRANT_URL')
qdrant_api_key = os.getenv('QDRANT_API_KEY')
collection_name = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print(f"🔍 VERIFICACIÓN COMPLETA DE QDRANT CLOUD")
print(f"=" * 60)
print(f"URL: {qdrant_url}")
print(f"Collection: {collection_name}\n")

try:
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=60
    )
    
    # 1. LISTAR TODAS LAS COLECCIONES
    print("📚 PASO 1: Listar todas las colecciones")
    print("-" * 60)
    collections = client.get_collections()
    print(f"Total de colecciones: {len(collections.collections)}\n")
    
    for col in collections.collections:
        print(f"  📁 {col.name}")
        try:
            info = client.get_collection(col.name)
            print(f"     └─ Puntos: {info.points_count:,}")
            print(f"     └─ Segmentos: {info.segments_count}")
        except Exception as e:
            print(f"     └─ Error al obtener info: {e}")
    
    print()
    
    # 2. INFORMACIÓN DETALLADA DE LA COLECCIÓN PRINCIPAL
    print("📊 PASO 2: Información detallada de la colección")
    print("-" * 60)
    
    collection_info = client.get_collection(collection_name)
    total_points = collection_info.points_count
    
    print(f"✅ Colección: {collection_name}")
    print(f"📊 Total de puntos: {total_points:,}")
    print(f"🔢 Segmentos: {collection_info.segments_count}")
    
    # Calcular tamaño
    # Vector 768 dim * 4 bytes = 3 KB + metadata ~1 KB = 4 KB por punto
    estimated_size_mb = (total_points * 4) / 1024
    print(f"💾 Tamaño estimado: ~{estimated_size_mb:.2f} MB")
    print(f"📈 Uso del Free Tier: {(estimated_size_mb / 1024) * 100:.2f}% (de 1 GB)")
    print()
    
    # 3. ANÁLISIS COMPLETO DE TODOS LOS PUNTOS
    print("🔍 PASO 3: Analizando TODOS los puntos...")
    print("-" * 60)
    print(f"Esto puede tardar un momento...\n")
    
    # Contadores
    capas = defaultdict(int)
    normas = defaultdict(int)
    tipos = defaultdict(int)
    
    # Scroll por todos los puntos
    offset = None
    batch_size = 100
    total_processed = 0
    
    while True:
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
            payload = point.payload
            
            # Contar por capa
            layer = payload.get('layer', 'Sin capa')
            capas[layer] += 1
            
            # Contar por norma
            norma = payload.get('norma', 'N/A')
            normas[norma] += 1
            
            # Contar por tipo
            tipo = payload.get('tipo', 'Desconocido')
            tipos[tipo] += 1
        
        total_processed += len(points)
        print(f"  Procesados: {total_processed}/{total_points} ({(total_processed/total_points)*100:.1f}%)", end='\r')
        
        if offset is None:
            break
    
    print(f"\n✅ Análisis completado: {total_processed:,} puntos procesados\n")
    
    # 4. RESULTADOS POR CAPAS
    print("🔢 DISTRIBUCIÓN POR CAPAS:")
    print("-" * 60)
    for capa in sorted(capas.keys()):
        count = capas[capa]
        pct = (count / total_processed) * 100
        print(f"  Capa {capa}: {count:,} docs ({pct:.1f}%)")
    
    print()
    
    # 5. RESULTADOS POR NORMAS
    print("📚 NORMAS INDEXADAS:")
    print("-" * 60)
    for norma, count in sorted(normas.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_processed) * 100
        print(f"  {norma}: {count:,} docs ({pct:.1f}%)")
    
    print()
    
    # 6. RESULTADOS POR TIPOS
    print("📑 TIPOS DE DOCUMENTO:")
    print("-" * 60)
    for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_processed) * 100
        print(f"  {tipo}: {count:,} docs ({pct:.1f}%)")
    
    print()
    
    # 7. VERIFICAR SI HAY PROBLEMAS
    print("🔍 VERIFICACIÓN DE CALIDAD:")
    print("-" * 60)
    
    problemas = []
    
    # Verificar norma="N/A"
    if 'N/A' in normas and normas['N/A'] > 0:
        problemas.append(f"⚠️  {normas['N/A']} documentos con norma='N/A'")
    else:
        print("✅ No hay documentos con norma='N/A'")
    
    # Verificar capas
    if 2 not in capas:
        problemas.append("❌ Capa 2 (Jurisprudencia) NO existe")
    else:
        print(f"✅ Capa 2 existe: {capas[2]} docs")
    
    if 3 not in capas:
        problemas.append("❌ Capa 3 (Temarios/Tests) NO existe")
    else:
        print(f"✅ Capa 3 existe: {capas[3]} docs")
    
    # Verificar cantidad de leyes
    total_normas = len([n for n in normas.keys() if n != 'N/A'])
    if total_normas < 13:
        problemas.append(f"⚠️  Solo {total_normas}/13 leyes indexadas")
    else:
        print(f"✅ Todas las leyes indexadas: {total_normas}/13")
    
    print()
    
    # 8. RESUMEN FINAL
    print("=" * 60)
    print("📋 RESUMEN FINAL")
    print("=" * 60)
    print(f"Total de puntos: {total_points:,}")
    print(f"Tamaño estimado: ~{estimated_size_mb:.2f} MB")
    print(f"Capas activas: {len(capas)}")
    print(f"Normas diferentes: {len([n for n in normas.keys() if n != 'N/A'])}")
    print(f"Tipos de documento: {len(tipos)}")
    
    if problemas:
        print(f"\n⚠️  PROBLEMAS DETECTADOS ({len(problemas)}):")
        for problema in problemas:
            print(f"  {problema}")
    else:
        print(f"\n✅ No se detectaron problemas")
    
    print()
    
    # 9. MOSTRAR EJEMPLO COMPLETO
    print("📄 EJEMPLO DE DOCUMENTO COMPLETO:")
    print("-" * 60)
    scroll_result = client.scroll(
        collection_name=collection_name,
        limit=1,
        with_payload=True,
        with_vectors=False
    )
    
    if scroll_result[0]:
        example = scroll_result[0][0]
        print(f"ID: {example.id}")
        print(f"\nPayload completo:")
        for key, value in example.payload.items():
            if key == 'text':
                text_preview = str(value)[:150] + "..." if len(str(value)) > 150 else str(value)
                print(f"  {key}: {text_preview}")
            else:
                print(f"  {key}: {value}")
    
    print("\n✅ Verificación completa finalizada")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
