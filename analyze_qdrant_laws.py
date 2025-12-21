
import asyncio
from qdrant_client import QdrantClient
from qdrant_client.http import models

async def analyze_qdrant_metadata():
    client = QdrantClient(url="http://localhost:6333", prefer_grpc=False)
    collection_name = "opositaia_knowledge"
    
    print(f"🕵️  Analyzing collection: {collection_name}")
    
    # Scroll through points to collect distinct 'ley' and 'layer' (topic)
    # Note: This is a scan, might be slow if millions of points, but we have ~17k.
    
    laws = set()
    layers = set()
    
    # We'll scroll 1000 points to get a good sample, or all if feasible. 
    # For speed, let's grab a few batches.
    
    offset = None
    limit = 2000 # Checked 2000 points
    
    points, next_offset = client.scroll(
        collection_name=collection_name,
        limit=limit,
        with_payload=True,
        with_vectors=False
    )
    
    for point in points:
        payload = point.payload
        if "ley" in payload:
            laws.add(payload["ley"])
        if "layer" in payload:
             layers.add(str(payload["layer"])) # Keep as string for set
             
    print("\n📜 Leyes Detectadas (Muestra):")
    for ley in sorted(list(laws)):
        print(f"  - {ley}")
        
    print("\n📚 Layers (Temas) Detectados:")
    for layer in sorted(list(layers)):
        print(f"  - {layer}")
        
    # Check total count
    count = client.count(collection_name=collection_name)
    print(f"\n🔢 Total Vectors: {count.count}")

if __name__ == "__main__":
    asyncio.run(analyze_qdrant_metadata())
