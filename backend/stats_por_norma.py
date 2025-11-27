"""
Estadísticas por norma indexada
"""
from qdrant_client import QdrantClient
from collections import Counter

def stats_por_norma():
    """Muestra estadísticas agrupadas por norma"""
    
    client = QdrantClient(url="http://localhost:6333")
    collection_name = "opositaia_leyes_seguridad_social"
    
    print("\n" + "="*70)
    print("📊 ESTADÍSTICAS POR NORMA INDEXADA")
    print("="*70 + "\n")
    
    # Obtener todos los puntos (en batches)
    all_points = []
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
        all_points.extend(points)
        
        if offset is None:
            break
    
    print(f"✅ Total puntos recuperados: {len(all_points)}\n")
    
    # Agrupar por norma
    normas = Counter()
    tipos = Counter()
    layers = Counter()
    
    for point in all_points:
        norma = point.payload.get('norma_nombre', 'Desconocido')
        tipo = point.payload.get('tipo', 'Desconocido')
        layer = point.payload.get('layer', 'N/A')
        
        normas[norma] += 1
        tipos[tipo] += 1
        layers[layer] += 1
    
    # Mostrar resultados
    print("📚 DISTRIBUCIÓN POR NORMA:")
    print("-"*70)
    for norma, count in normas.most_common():
        porcentaje = (count / len(all_points)) * 100
        print(f"  {norma:30s} {count:4d} chunks ({porcentaje:5.1f}%)")
    
    print("\n📄 DISTRIBUCIÓN POR TIPO:")
    print("-"*70)
    for tipo, count in tipos.most_common():
        porcentaje = (count / len(all_points)) * 100
        print(f"  {tipo:30s} {count:4d} chunks ({porcentaje:5.1f}%)")
    
    print("\n📑 DISTRIBUCIÓN POR CAPA:")
    print("-"*70)
    for layer, count in sorted(layers.items()):
        porcentaje = (count / len(all_points)) * 100
        print(f"  Capa {layer} {count:4d} chunks ({porcentaje:5.1f}%)")
    
    # Detalles por norma
    print("\n" + "="*70)
    print("📖 DETALLES POR NORMA")
    print("="*70 + "\n")
    
    for norma in normas.keys():
        norma_points = [p for p in all_points if p.payload.get('norma_nombre') == norma]
        
        if norma_points:
            first = norma_points[0].payload
            
            print(f"📘 {norma}")
            print(f"   BOE ID: {first.get('norma_id', 'N/A')}")
            print(f"   Nombre completo: {first.get('norma_completa', 'N/A')}")
            print(f"   Fecha: {first.get('fecha', 'N/A')}")
            print(f"   Chunks: {len(norma_points)}")
            print(f"   Tipo: {first.get('tipo', 'N/A')}")
            print(f"   Layer: {first.get('layer', 'N/A')}")
            print(f"   Jerarquía: {first.get('nivel_jerarquia', 'N/A')}")
            
            # Contar artículos únicos
            articulos = set(p.payload.get('articulo') for p in norma_points if p.payload.get('articulo'))
            if articulos:
                print(f"   Artículos detectados: {len(articulos)}")
            
            print()
    
    print("="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)

if __name__ == "__main__":
    stats_por_norma()
