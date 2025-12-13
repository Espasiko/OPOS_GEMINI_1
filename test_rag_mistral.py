import os
import json
import requests
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Configuration
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge"
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "mistral:latest"

def main():
    print(f"Loading embedding model: {EMBEDDING_MODEL}...")
    encoder = SentenceTransformer(EMBEDDING_MODEL)
    
    print(f"Connecting to Qdrant at {QDRANT_URL}...")
    client = QdrantClient(url=QDRANT_URL, timeout=60)
    
    # Test Query
    query_text = "Cuales son los requisitos para ser beneficiario de la prestación por desempleo?"
    print(f"\nQuery: {query_text}")
    
    # 1. Retrieve
    print("Encoding query...")
    query_vector = encoder.encode(query_text).tolist()
    
    print("Searching Qdrant...")
    # Using query_points with named vector "dense"
    search_result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        using="dense",
        limit=3
    ).points
    
    context_parts = []
    print("\n--- Retrieved Documents ---")
    for hit in search_result:
        payload = hit.payload
        text = payload.get('text', '')
        boe_id = payload.get('boe_id', 'Unknown')
        score = hit.score
        print(f"[Score: {score:.4f}] ID: {boe_id}")
        print(f"Text snippet: {text[:200]}...")
        context_parts.append(f"Documento ({boe_id}): {text}")
    
    context_str = "\n\n".join(context_parts)
    
    # 2. Generate
    print("\n--- Generating Answer with Mistral ---")
    prompt = f"""Eres un asistente experto en leyes españolas. Usa el siguiente contexto para responder a la pregunta.
    Si la respuesta no está en el contexto, di que no tienes información suficiente.
    
    Contexto:
    {context_str}
    
    Pregunta: {query_text}
    
    Respuesta:"""
    
    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result.get("response", "")
        print("\n--- Mistral Answer ---")
        print(answer)
    except Exception as e:
        print(f"Error calling Ollama: {e}")

if __name__ == "__main__":
    main()
