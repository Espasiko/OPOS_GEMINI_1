#!/usr/bin/env python3
"""Generador de 20 Q&A con Mistral API (rápido)"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient
import time

print("\n🎯 GENERADOR DE 20 Q&A CON MISTRAL API\n")

# Config
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY environment variable not set")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Conectar a Qdrant
qdrant = QdrantClient("http://localhost:6333")

# Extraer 20 preguntas diferentes
print("📥 Extrayendo 20 preguntas de Qdrant...")
points, _ = qdrant.scroll(
    collection_name="materiales_academia",
    limit=100,
    with_payload=True,
    with_vectors=False
)

questions = [p for p in points if p.payload.get("subcategory") == "preguntas"][:20]
print(f"✅ Encontradas {len(questions)} preguntas\n")

generated_qa = []
errors = 0

def query_mistral_api(prompt):
    """Consulta Mistral API"""
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 1500
    }
    
    response = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=60)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# Generar Q&A
for i, q in enumerate(questions, 1):
    print(f"--- Pregunta {i}/20 ---")
    print(f"Archivo: {q.payload['filename']}")
    
    prompt = f"""Eres experto en oposiciones de Seguridad Social España.
Crea 1 variación de esta pregunta oficial, transformándola completamente para que NO se identifique el origen.

PREGUNTA ORIGINAL: {q.payload['text'][:500]}

INSTRUCCIONES:
1. Mantén el MISMO conocimiento legal evaluado
2. Cambia COMPLETAMENTE la redacción
3. 4 opciones (A, B, C, D) con UNA correcta
4. NO copies frases literales

Responde SOLO con JSON válido:
{{"pregunta": "texto reformulado completo", "opciones": ["A) opcion1", "B) opcion2", "C) opcion3", "D) opcion4"], "respuesta_correcta": "A", "explicacion": "explicacion legal detallada", "tema": "tema especifico SS", "dificultad": "intermedia"}}"""
    
    try:
        result = query_mistral_api(prompt)
        
        # Extraer JSON
        json_start = result.find('{')
        json_end = result.rfind('}') + 1
        
        if json_start >= 0:
            qa = json.loads(result[json_start:json_end])
            qa['source_file'] = q.payload['filename']
            qa['source_page'] = q.payload.get('page_number', 0)
            qa['generated_at'] = datetime.now().isoformat()
            qa['model'] = 'mistral-small-latest (API)'
            generated_qa.append(qa)
            print(f"✅ Q&A {i} generada\n")
        else:
            print(f"❌ No JSON en respuesta\n")
            errors += 1
            
    except Exception as e:
        print(f"❌ Error: {e}\n")
        errors += 1
    
    # Rate limiting
    time.sleep(0.5)

# Exportar
os.makedirs('dataset_output', exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'dataset_output/qa_mistral_api_20_{timestamp}.json'

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(generated_qa, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"✅ GENERACIÓN MISTRAL API COMPLETADA")
print(f"{'='*60}")
print(f"Q&A generadas: {len(generated_qa)}/20")
print(f"Errores: {errors}")
print(f"Archivo: {output_file}")

# Mostrar 2 muestras
print(f"\n📋 MUESTRAS:")
for i, qa in enumerate(generated_qa[:2], 1):
    print(f"\n--- Muestra {i} ---")
    print(f"Tema: {qa['tema']}")
    print(f"Pregunta: {qa['pregunta'][:150]}...")
    print(f"Correcta: {qa['respuesta_correcta']}")
    print(f"Explicación: {qa['explicacion'][:100]}...")
