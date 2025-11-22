"""
Verificar si el artículo 168 de la Constitución está indexado
"""
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
collection_name = "opositaia_leyes_seguridad_social"

# Buscar chunks de la Constitución con artículo 168
results = client.scroll(
    collection_name=collection_name,
    scroll_filter={
        "must": [
            {"key": "norma_nombre", "match": {"value": "Constitución_Española"}},
            {"key": "articulo", "match": {"value": "168"}}
        ]
    },
    limit=10
)

print(f"Chunks encontrados con artículo 168: {len(results[0])}")

if results[0]:
    for point in results[0]:
        print(f"\nID: {point.id}")
        print(f"Artículo: {point.payload.get('articulo')}")
        print(f"Contenido (primeros 500 chars):")
        print(point.payload.get('content', '')[:500])
        print("-" * 80)
else:
    print("\n❌ No se encontró el artículo 168 indexado")
    print("\nBuscando todos los artículos de la Constitución...")
    
    # Buscar todos los chunks de la Constitución
    all_const = client.scroll(
        collection_name=collection_name,
        scroll_filter={
            "must": [
                {"key": "norma_nombre", "match": {"value": "Constitución_Española"}}
            ]
        },
        limit=100
    )
    
    articulos = set()
    for point in all_const[0]:
        art = point.payload.get('articulo')
        if art:
            articulos.add(art)
    
    print(f"\nTotal chunks de Constitución: {len(all_const[0])}")
    print(f"Artículos únicos encontrados: {sorted(articulos, key=lambda x: int(x) if x.isdigit() else 999)}")
