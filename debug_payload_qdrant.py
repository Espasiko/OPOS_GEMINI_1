import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import json

def debug_payload():
    print("Depurando payload de Qdrant...")
    client = QdrantClient("http://localhost:6333")
    model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
    
    query = "umbral cotización jubilación 65 años 2026"
    vector = model.encode(query).tolist()
    
    res = client.query_points(
        collection_name="opositaia_knowledge_FULL_XML",
        query=vector,
        using="dense",
        limit=2,
        with_payload=True
    ).points
    
    for i, hit in enumerate(res):
        print(f"\n--- HIT {i+1} (Score: {hit.score}) ---")
        print(json.dumps(hit.payload, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    debug_payload()
