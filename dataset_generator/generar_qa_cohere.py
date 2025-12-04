#!/usr/bin/env python3
"""Generador de 20 Q&A con Cohere Command R+ (mejor modelo)"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient
import time

print("\n🎯 GENERADOR DE 20 Q&A CON COHERE COMMAND R+\n")

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable not set")
COHERE_URL = "https://api.cohere.ai/v1/chat"

qdrant = QdrantClient("http://localhost:6333")

print("📥 Extrayendo 20 preguntas...")
points, _ = qdrant.scroll(collection_name="materiales_academia", limit=200, with_payload=True, with_vectors=False)
questions = [p for p in points if p.payload.get("subcategory") == "preguntas"][60:80]
print(f"✅ {len(questions)} preguntas (offset 60-80)\n")

generated_qa = []

def query_cohere(prompt):
    """Usa Cohere Command A (mejor modelo actual de Cohere - marzo 2025)"""
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "command-a-03-2025",  # Mejor modelo actual de Cohere
        "message": prompt,
        "temperature": 0.3,
        "max_tokens": 1500
    }
    response = requests.post(COHERE_URL, headers=headers, json=payload, timeout=60)
    if response.status_code == 200:
        return response.json()["text"]
    raise Exception(f"Error: {response.status_code} - {response.text}")

for i, q in enumerate(questions, 1):
    print(f"--- Pregunta {i}/20 ---")
    prompt = f"""Eres experto en oposiciones de Seguridad Social España.
Crea 1 variación de esta pregunta oficial, transformándola completamente.

PREGUNTA ORIGINAL: {q.payload['text'][:500]}

INSTRUCCIONES:
1. Mantén el MISMO conocimiento legal evaluado
2. Cambia COMPLETAMENTE la redacción
3. 4 opciones (A, B, C, D) con UNA correcta
4. Explicación detallada con referencias legales

Responde SOLO con JSON válido:
{{"pregunta": "texto reformulado completo", "opciones": ["A) op1", "B) op2", "C) op3", "D) op4"], "respuesta_correcta": "A", "explicacion": "explicacion legal detallada", "tema": "tema SS específico", "dificultad": "intermedia"}}"""
    
    try:
        result = query_cohere(prompt)
        json_start, json_end = result.find('{'), result.rfind('}') + 1
        if json_start >= 0:
            qa = json.loads(result[json_start:json_end])
            qa.update({
                'source_file': q.payload['filename'],
                'generated_at': datetime.now().isoformat(),
                'model': 'command-a-03-2025 (Cohere)'
            })
            generated_qa.append(qa)
            print(f"✅ Q&A {i} generada\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    time.sleep(0.5)

os.makedirs('dataset_output', exist_ok=True)
output_file = f'dataset_output/qa_cohere_20_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(generated_qa, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}\n✅ COHERE: {len(generated_qa)}/20 Q&A\nArchivo: {output_file}")

if generated_qa:
    print(f"\n📋 MUESTRA:")
    qa = generated_qa[0]
    print(f"Tema: {qa.get('tema')}")
    print(f"Pregunta: {qa['pregunta'][:150]}...")
