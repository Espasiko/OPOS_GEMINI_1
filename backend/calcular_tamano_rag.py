"""
Calcular tamaño exacto del RAG para Qdrant Cloud
"""
from qdrant_client import QdrantClient

def calcular_tamano():
    """Calcula el tamaño del RAG en Qdrant"""
    
    client = QdrantClient(url="http://localhost:6333")
    collection_name = "opositaia_leyes_seguridad_social"
    
    print("\n" + "="*70)
    print("📊 CÁLCULO DE TAMAÑO DEL RAG")
    print("="*70 + "\n")
    
    # Obtener info de la colección
    info = client.get_collection(collection_name)
    
    # Datos básicos
    points_count = info.points_count
    vector_size = info.config.params.vectors.size  # 768 para RoBERTalex
    
    print(f"📈 Puntos indexados: {points_count:,}")
    print(f"📐 Dimensión vectores: {vector_size}")
    print(f"📏 Distancia: {info.config.params.vectors.distance}")
    
    # Cálculo de tamaño
    print("\n" + "="*70)
    print("💾 CÁLCULO DE TAMAÑO")
    print("="*70 + "\n")
    
    # Tamaño de vectores (float32 = 4 bytes)
    vector_size_bytes = points_count * vector_size * 4
    vector_size_mb = vector_size_bytes / (1024 * 1024)
    
    print(f"Vectores:")
    print(f"  - {points_count:,} puntos × {vector_size} dimensiones × 4 bytes")
    print(f"  - Tamaño: {vector_size_mb:.2f} MB")
    
    # Estimación de payload (metadata + texto)
    # Promedio: ~500 bytes por punto (metadata + texto truncado)
    payload_size_bytes = points_count * 500
    payload_size_mb = payload_size_bytes / (1024 * 1024)
    
    print(f"\nPayload (metadata + texto):")
    print(f"  - {points_count:,} puntos × ~500 bytes")
    print(f"  - Tamaño estimado: {payload_size_mb:.2f} MB")
    
    # Overhead de Qdrant (índices, estructuras internas)
    # Estimación: ~20% adicional
    overhead_mb = (vector_size_mb + payload_size_mb) * 0.20
    
    print(f"\nOverhead Qdrant (~20%):")
    print(f"  - Tamaño estimado: {overhead_mb:.2f} MB")
    
    # Total
    total_mb = vector_size_mb + payload_size_mb + overhead_mb
    total_gb = total_mb / 1024
    
    print("\n" + "="*70)
    print("📊 TAMAÑO TOTAL ESTIMADO")
    print("="*70 + "\n")
    
    print(f"✅ Tamaño total: {total_mb:.2f} MB ({total_gb:.3f} GB)")
    
    # Comparación con Qdrant Cloud Free Tier
    print("\n" + "="*70)
    print("☁️  QDRANT CLOUD FREE TIER")
    print("="*70 + "\n")
    
    free_tier_gb = 1.0
    free_tier_mb = free_tier_gb * 1024
    
    print(f"Límite Free Tier: {free_tier_gb} GB ({free_tier_mb:.0f} MB)")
    print(f"Uso actual: {total_mb:.2f} MB ({total_gb:.3f} GB)")
    print(f"Disponible: {free_tier_mb - total_mb:.2f} MB ({free_tier_gb - total_gb:.3f} GB)")
    
    porcentaje_uso = (total_mb / free_tier_mb) * 100
    print(f"\n📊 Uso del Free Tier: {porcentaje_uso:.1f}%")
    
    # Veredicto
    print("\n" + "="*70)
    if total_mb < free_tier_mb:
        margen = free_tier_mb - total_mb
        print("✅ CABE EN FREE TIER")
        print("="*70 + "\n")
        print(f"🎉 Tu RAG cabe perfectamente en Qdrant Cloud Free Tier!")
        print(f"📊 Margen disponible: {margen:.2f} MB ({(margen/1024):.3f} GB)")
        print(f"📈 Podrías agregar ~{int(margen / (total_mb / points_count)):,} chunks más")
    else:
        exceso = total_mb - free_tier_mb
        print("❌ NO CABE EN FREE TIER")
        print("="*70 + "\n")
        print(f"⚠️  Excede el límite por: {exceso:.2f} MB ({(exceso/1024):.3f} GB)")
        print(f"💰 Necesitarías Qdrant Cloud Paid (~$25/mes)")
    
    # Desglose por capa
    print("\n" + "="*70)
    print("📊 DESGLOSE POR CAPA")
    print("="*70 + "\n")
    
    # Obtener puntos por capa
    capa1_points = client.scroll(
        collection_name=collection_name,
        limit=1,
        scroll_filter={"must": [{"key": "layer", "match": {"value": 1}}]}
    )[0]
    
    capa3_points = client.scroll(
        collection_name=collection_name,
        limit=1,
        scroll_filter={"must": [{"key": "layer", "match": {"value": 3}}]}
    )[0]
    
    # Contar todos los puntos por capa
    capa1_count = 0
    capa3_count = 0
    offset = None
    
    while True:
        result = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        points, offset = result
        
        for p in points:
            layer = p.payload.get('layer', 0)
            if layer == 1:
                capa1_count += 1
            elif layer == 3:
                capa3_count += 1
        
        if offset is None:
            break
    
    capa1_mb = (capa1_count * vector_size * 4 + capa1_count * 500) / (1024 * 1024)
    capa3_mb = (capa3_count * vector_size * 4 + capa3_count * 500) / (1024 * 1024)
    
    print(f"Capa 1 (Normativa):")
    print(f"  - Puntos: {capa1_count:,}")
    print(f"  - Tamaño: {capa1_mb:.2f} MB ({(capa1_mb/total_mb)*100:.1f}%)")
    
    print(f"\nCapa 3 (Materiales):")
    print(f"  - Puntos: {capa3_count:,}")
    print(f"  - Tamaño: {capa3_mb:.2f} MB ({(capa3_mb/total_mb)*100:.1f}%)")
    
    print("\n" + "="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)

if __name__ == "__main__":
    calcular_tamano()
