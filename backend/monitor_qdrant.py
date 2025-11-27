"""
Monitor Qdrant - Muestra estado en vivo de la colección
"""
from qdrant_client import QdrantClient
from datetime import datetime

def monitor_collection():
    """Monitorea el estado de la colección"""
    
    collection_name = "opositaia_leyes_seguridad_social"
    
    try:
        client = QdrantClient(url="http://localhost:6333")
        
        print("\n" + "="*60)
        print(f"📊 MONITOR QDRANT - {datetime.now().strftime('%H:%M:%S')}")
        print("="*60 + "\n")
        
        # Obtener info de la colección
        info = client.get_collection(collection_name)
        
        print(f"🗂️  Colección: {collection_name}")
        print(f"📈 Puntos indexados: {info.points_count:,}")
        print(f"� VDimensión: {info.config.params.vectors.size}")
        print(f"� Diistancia: {info.config.params.vectors.distance}")
        print(f"✅ Status: {info.status}")
        
        # Calcular tamaño aproximado
        size_mb = (info.points_count * info.config.params.vectors.size * 4) / (1024 * 1024)
        print(f"💾 Tamaño estimado: {size_mb:.2f} MB")
        
        # Obtener un punto de ejemplo
        print("\n" + "="*60)
        print("📝 EJEMPLO DE PUNTO INDEXADO")
        print("="*60 + "\n")
        
        points = client.scroll(
            collection_name=collection_name,
            limit=1,
            with_payload=True,
            with_vectors=False
        )[0]
        
        if points:
            point = points[0]
            payload = point.payload
            
            print(f"ID: {point.id}")
            print(f"Layer: {payload.get('layer')}")
            print(f"Tipo: {payload.get('tipo')}")
            print(f"Norma: {payload.get('norma_nombre')}")
            print(f"Artículo: {payload.get('articulo', 'N/A')}")
            print(f"Página: {payload.get('page_num')}")
            print(f"Chunk: {payload.get('chunk_id')}/{payload.get('total_chunks')}")
            print(f"\nTexto (primeros 200 chars):")
            print(f"{payload.get('text', '')[:200]}...")
        
        # Estadísticas por artículo
        print("\n" + "="*60)
        print("📊 DISTRIBUCIÓN POR ARTÍCULOS")
        print("="*60 + "\n")
        
        # Contar chunks por artículo (sample)
        all_points = client.scroll(
            collection_name=collection_name,
            limit=100,
            with_payload=True,
            with_vectors=False
        )[0]
        
        articulos = {}
        for p in all_points:
            art = p.payload.get('articulo', 'Sin artículo')
            articulos[art] = articulos.get(art, 0) + 1
        
        print(f"Artículos en muestra (primeros 100 chunks):")
        for art, count in sorted(articulos.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  Art. {art}: {count} chunks")
        
        print("\n" + "="*60)
        print("✅ COLECCIÓN OPERATIVA")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Verifica:")
        print("  1. Qdrant está corriendo: docker ps")
        print("  2. La colección existe")

if __name__ == "__main__":
    monitor_collection()
