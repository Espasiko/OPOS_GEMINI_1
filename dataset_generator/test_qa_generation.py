#!/usr/bin/env python3
"""Test simple de generación de Q&A"""

import json
import requests
from qdrant_client import QdrantClient

# Conectar
qdrant = QdrantClient("http://localhost:6333")
ollama_url = "http://localhost:11434"

# Extraer 3 preguntas
print("Extrayendo preguntas...")
points, _ = qdrant.scroll(
    collection_name="materiales_academia",
    limit=50,
    with_payload=True,
    with_vectors=False
)

questions = [p for p in points if p.payload.get("subcategory") == "preguntas"][:3]
print(f"Encontradas {len(questions)} preguntas")

# Generar 1 variación para la primera pregunta
if questions:
    q = questions[0]
    print(f"\nPregunta original: {q.payload['text'][:200]}...")
    
    prompt = "Explica en una frase que es la Seguridad Social en España."
    
    print("\nConsultando Mistral...")
    response = requests.post(
        f"{ollama_url}/api/generate",
        json={"model": "mistral:latest", "prompt": prompt, "stream": False},
        timeout=120
    )
    
    if response.status_code == 200:
        result = response.json().get('response', '')
        print(f"\nRespuesta de Mistral:\n{result[:500]}...")
        
        # Intentar extraer JSON
        json_start = result.find('{')
        json_end = result.rfind('}') + 1
        if json_start >= 0:
            try:
                qa = json.loads(result[json_start:json_end])
                print(f"\n✅ Q&A generada:")
                print(json.dumps(qa, indent=2, ensure_ascii=False))
            except:
                print("❌ No se pudo parsear JSON")
    else:
        print(f"❌ Error: {response.status_code}")
else:
    print("❌ No se encontraron preguntas")
