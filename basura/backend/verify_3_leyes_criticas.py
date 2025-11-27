"""
Verificar las 3 leyes críticas indexadas
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = QdrantClient(url="http://localhost:6333")
collection_name = "opositaia_leyes_seguridad_social"

print("="*80)
print("🔍 VERIFICACIÓN DE 3 LEYES CRÍTICAS INDEXADAS")
print("="*80)

leyes_criticas = [
    {
        "nombre": "RD_1430_2009_Incapacidad_Temporal",
        "nombre_completo": "RD 1430/2009 Incapacidad Temporal",
        "boe_id": "BOE-A-2009-15442"
    },
    {
        "nombre": "RD_1300_1995_Incapacidad_Permanente",
        "nombre_completo": "RD 1300/1995 Incapacidad Permanente",
        "boe_id": "BOE-A-1995-19848"
    },
    {
        "nombre": "Ley_39_2006_Dependencia",
        "nombre_completo": "Ley 39/2006 Dependencia",
        "boe_id": "BOE-A-2006-21990"
    }
]

total_chunks = 0

for i, ley in enumerate(leyes_criticas, 1):
    print(f"\n{'='*80}")
    print(f"📄 LEY {i}/3: {ley['nombre_completo']}")
    print(f"{'='*80}")
    
    # Buscar chunks de esta ley
    results = client.scroll(
        collection_name=collection_name,
        scroll_filter=Filter(
            must=[
                FieldCondition(key="norma_nombre", match=MatchValue(value=ley['nombre']))
            ]
        ),
        limit=100
    )
    
    chunks = results[0]
    print(f"✅ Chunks indexados: {len(chunks)}")
    total_chunks += len(chunks)
    
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
        print(f"   Lista: {', '.join(articulos_ordenados[:15])}{'...' if len(articulos_ordenados) > 15 else ''}")
    
    # Mostrar un chunk de ejemplo
    if chunks:
        ejemplo = chunks[0]
        print(f"\n📝 Ejemplo de contenido:")
        print(f"   Artículo: {ejemplo.payload.get('articulo', 'N/A')}")
        print(f"   Preview: {ejemplo.payload.get('content', '')[:200]}...")

print(f"\n{'='*80}")
print(f"✅ VERIFICACIÓN COMPLETADA")
print(f"{'='*80}")
print(f"📊 Total chunks de las 3 leyes: {total_chunks}")
print(f"📚 Leyes verificadas: 3/3")
print(f"{'='*80}")

# Estadísticas generales de la colección
print(f"\n📊 ESTADÍSTICAS GENERALES DE LA COLECCIÓN")
print(f"{'='*80}")

collection_info = client.get_collection(collection_name)
print(f"Total puntos: {collection_info.points_count}")
print(f"Vector size: {collection_info.config.params.vectors.size}")

# Contar por tipo
print(f"\n📋 Distribución por tipo de norma:")
tipos = {}
all_points = client.scroll(collection_name=collection_name, limit=10000)[0]
for point in all_points:
    tipo = point.payload.get('tipo', 'unknown')
    if tipo not in tipos:
        tipos[tipo] = 0
    tipos[tipo] += 1

for tipo, count in sorted(tipos.items()):
    print(f"   {tipo}: {count} chunks")

print(f"{'='*80}")
