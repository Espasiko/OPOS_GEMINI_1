"""
Verificar que el artículo 168 está indexado
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = QdrantClient(url="http://localhost:6333")
collection_name = "opositaia_leyes_seguridad_social"

print("="*80)
print("🔍 VERIFICACIÓN ARTÍCULO 168 - REFORMA CONSTITUCIONAL")
print("="*80)

# Buscar artículo 168
results = client.scroll(
    collection_name=collection_name,
    scroll_filter=Filter(
        must=[
            FieldCondition(key="norma_nombre", match=MatchValue(value="Constitución_Española")),
            FieldCondition(key="articulo", match=MatchValue(value="168"))
        ]
    ),
    limit=10
)

if results[0]:
    print(f"\n✅ ARTÍCULO 168 ENCONTRADO - {len(results[0])} chunk(s)")
    for point in results[0]:
        print(f"\n{'='*80}")
        print(f"ID: {point.id}")
        print(f"Artículo: {point.payload.get('articulo')}")
        print(f"\nContenido:")
        print(point.payload.get('content', '')[:800])
        print(f"{'='*80}")
else:
    print("\n❌ ARTÍCULO 168 NO ENCONTRADO")

# Listar todos los artículos
print("\n" + "="*80)
print("📋 TODOS LOS ARTÍCULOS INDEXADOS")
print("="*80)

all_const = client.scroll(
    collection_name=collection_name,
    scroll_filter=Filter(
        must=[
            FieldCondition(key="norma_nombre", match=MatchValue(value="Constitución_Española"))
        ]
    ),
    limit=100
)

articulos = {}
for point in all_const[0]:
    art = point.payload.get('articulo')
    if art:
        if art not in articulos:
            articulos[art] = 0
        articulos[art] += 1

articulos_ordenados = sorted(articulos.keys(), key=lambda x: int(x) if x.isdigit() else 999)

print(f"\nTotal chunks: {len(all_const[0])}")
print(f"Artículos únicos: {len(articulos_ordenados)}")
print(f"\nLista completa de artículos:")
for i in range(0, len(articulos_ordenados), 10):
    batch = articulos_ordenados[i:i+10]
    print(f"  {', '.join(batch)}")

print("\n" + "="*80)
