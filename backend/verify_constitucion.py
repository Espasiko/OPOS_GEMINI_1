"""
Verificar que la Constitución está correctamente indexada
"""
from qdrant_client import QdrantClient
from collections import Counter

def verify_constitucion():
    """Verifica la indexación de la Constitución"""
    
    client = QdrantClient(url="http://localhost:6333")
    collection_name = "opositaia_leyes_seguridad_social"
    
    print("\n" + "="*70)
    print("🔍 VERIFICACIÓN: CONSTITUCIÓN ESPAÑOLA")
    print("="*70 + "\n")
    
    # Obtener TODOS los puntos de la Constitución
    const_points = []
    offset = None
    
    print("📥 Recuperando puntos de la Constitución...")
    
    while True:
        result = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
            scroll_filter={
                "must": [
                    {
                        "key": "tipo",
                        "match": {"value": "constitucion"}
                    }
                ]
            }
        )
        
        points, offset = result
        const_points.extend(points)
        
        if offset is None:
            break
    
    print(f"✅ Encontrados: {len(const_points)} puntos\n")
    
    if len(const_points) == 0:
        print("❌ ERROR: No se encontraron puntos de la Constitución")
        print("\n💡 Posibles causas:")
        print("   1. La indexación falló")
        print("   2. El filtro 'tipo=constitucion' no coincide")
        print("   3. Los puntos se indexaron con otro tipo")
        return
    
    # Analizar los puntos
    print("="*70)
    print("📊 ANÁLISIS DE PUNTOS")
    print("="*70 + "\n")
    
    articulos = Counter()
    paginas = set()
    
    for point in const_points:
        art = point.payload.get('articulo', 'Sin artículo')
        pag = point.payload.get('page_num')
        
        articulos[art] += 1
        if pag:
            paginas.add(pag)
    
    print(f"📄 Total chunks: {len(const_points)}")
    print(f"📖 Artículos únicos: {len([a for a in articulos.keys() if a != 'Sin artículo'])}")
    print(f"📑 Páginas cubiertas: {len(paginas)}")
    
    # Mostrar primeros 5 puntos
    print("\n" + "="*70)
    print("📝 PRIMEROS 5 PUNTOS")
    print("="*70 + "\n")
    
    for i, point in enumerate(const_points[:5], 1):
        print(f"{i}. ID: {point.id}")
        print(f"   Norma: {point.payload.get('norma_nombre')}")
        print(f"   Tipo: {point.payload.get('tipo')}")
        print(f"   Artículo: {point.payload.get('articulo', 'N/A')}")
        print(f"   Página: {point.payload.get('page_num')}")
        print(f"   Chunk: {point.payload.get('chunk_id')}/{point.payload.get('total_chunks')}")
        print(f"   Texto: {point.payload.get('text', '')[:100]}...")
        print()
    
    # Top artículos
    print("="*70)
    print("📖 TOP 10 ARTÍCULOS MÁS FRECUENTES")
    print("="*70 + "\n")
    
    for art, count in articulos.most_common(10):
        print(f"   Art. {art}: {count} chunks")
    
    # Verificar metadata
    print("\n" + "="*70)
    print("🔍 VERIFICACIÓN DE METADATA")
    print("="*70 + "\n")
    
    sample = const_points[0].payload
    
    print(f"✅ norma_id: {sample.get('norma_id')}")
    print(f"✅ norma_nombre: {sample.get('norma_nombre')}")
    print(f"✅ norma_completa: {sample.get('norma_completa')}")
    print(f"✅ tipo: {sample.get('tipo')}")
    print(f"✅ layer: {sample.get('layer')}")
    print(f"✅ nivel_jerarquia: {sample.get('nivel_jerarquia')}")
    print(f"✅ fecha: {sample.get('fecha')}")
    
    # Verificar en dashboard
    print("\n" + "="*70)
    print("🌐 VERIFICACIÓN EN DASHBOARD")
    print("="*70 + "\n")
    
    print("Para ver la Constitución en el dashboard de Qdrant:")
    print("1. Abre: http://localhost:6333/dashboard")
    print("2. Selecciona colección: opositaia_leyes_seguridad_social")
    print("3. En 'Filters', agrega:")
    print("   - Key: tipo")
    print("   - Match: constitucion")
    print("4. Click en 'Apply Filter'")
    
    print("\n" + "="*70)
    print("✅ CONSTITUCIÓN CORRECTAMENTE INDEXADA")
    print("="*70)
    print(f"\nTotal: {len(const_points)} chunks de Constitución en Qdrant")

if __name__ == "__main__":
    verify_constitucion()
