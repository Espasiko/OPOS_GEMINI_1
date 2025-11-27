"""
Verificar RD Cotización indexado
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = QdrantClient(url="http://localhost:6333")
collection_name = "opositaia_leyes_seguridad_social"

print("="*80)
print("🔍 VERIFICACIÓN RD COTIZACIÓN Y LIQUIDACIÓN")
print("="*80)

# Buscar chunks del RD Cotización
results = client.scroll(
    collection_name=collection_name,
    scroll_filter=Filter(
        must=[
            FieldCondition(key="norma_nombre", match=MatchValue(value="RD_Cotizacion_Liquidacion"))
        ]
    ),
    limit=200
)

chunks = results[0]
print(f"\n✅ Chunks indexados: {len(chunks)}")

# Estadísticas de artículos
articulos = {}
for point in chunks:
    art = point.payload.get('articulo')
    if art:
        if art not in articulos:
            articulos[art] = 0
        articulos[art] += 1

articulos_ordenados = sorted(articulos.keys(), key=lambda x: int(x) if x.isdigit() else 999)

print(f"📋 Artículos únicos: {len(articulos_ordenados)}")
if articulos_ordenados:
    print(f"   Rango: {articulos_ordenados[0]} - {articulos_ordenados[-1]}")
    print(f"   Lista (primeros 20): {', '.join(articulos_ordenados[:20])}")

# Mostrar ejemplo de contenido
if chunks:
    ejemplo = chunks[0]
    print(f"\n📝 Ejemplo de contenido:")
    print(f"   BOE ID: {ejemplo.payload.get('boe_id')}")
    print(f"   Tipo: {ejemplo.payload.get('tipo')}")
    print(f"   Artículo: {ejemplo.payload.get('articulo', 'N/A')}")
    print(f"   Preview: {ejemplo.payload.get('content', '')[:200]}...")

# Estadísticas finales
print(f"\n{'='*80}")
print(f"📊 ESTADÍSTICAS FINALES")
print(f"{'='*80}")

collection_info = client.get_collection(collection_name)
print(f"Total puntos en colección: {collection_info.points_count:,}")

# Contar todas las leyes
all_points = client.scroll(collection_name=collection_name, limit=10000)[0]
normas_capa1 = {}
for point in all_points:
    if point.payload.get('layer') == 1:
        norma = point.payload.get('norma_nombre', 'unknown')
        if norma not in normas_capa1:
            normas_capa1[norma] = 0
        normas_capa1[norma] += 1

print(f"\nTotal leyes en Capa 1: {len(normas_capa1)}")
print(f"RD Cotización incluido: {'✅ SÍ' if 'RD_Cotizacion_Liquidacion' in normas_capa1 else '❌ NO'}")

print(f"{'='*80}")
