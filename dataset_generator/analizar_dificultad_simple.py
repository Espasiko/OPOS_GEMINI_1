#!/usr/bin/env python3
"""Análisis simplificado de dificultad de exámenes"""

import os
import json
import requests
from qdrant_client import QdrantClient

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

def call_mistral(prompt: str) -> str:
    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-large-latest",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "max_tokens": 1000
            },
            timeout=90
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("\n📊 ANÁLISIS DE DIFICULTAD - EXÁMENES SS")
    print("=" * 50)
    
    qdrant = QdrantClient(url="http://localhost:6333")
    
    # Extraer preguntas
    points, _ = qdrant.scroll(
        collection_name="materiales_academia",
        limit=200,
        with_payload=True,
        with_vectors=False
    )
    
    preguntas = [p.payload.get('text', '')[:300] for p in points 
                 if p.payload.get('subcategory') == 'preguntas' and len(p.payload.get('text', '')) > 50][:15]
    
    print(f"📥 Analizando {len(preguntas)} preguntas...")
    
    prompt = f"""Eres experto en oposiciones Seguridad Social España.

Clasifica estas {len(preguntas)} preguntas por dificultad (FACIL/MEDIA/DIFICIL/MUY_DIFICIL).

PREGUNTAS:
{chr(10).join([f'{i+1}. {p}' for i, p in enumerate(preguntas)])}

Responde SOLO con este formato exacto:
FACIL: X
MEDIA: X  
DIFICIL: X
MUY_DIFICIL: X
PORCENTAJE_DIFICILES: X%
CONCLUSION: Una frase sobre la distribución típica"""

    response = call_mistral(prompt)
    
    if response:
        print("\n" + "=" * 50)
        print("📊 RESULTADOS:")
        print("=" * 50)
        print(response)
        
        # Extraer porcentaje
        for line in response.split('\n'):
            if 'PORCENTAJE' in line.upper():
                print(f"\n🎯 {line}")

if __name__ == "__main__":
    main()
