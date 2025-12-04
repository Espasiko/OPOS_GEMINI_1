#!/usr/bin/env python3
"""Generador de 10 Q&A con Groq API (Kimi K2 - modelo de razonamiento)"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient
import time

print("\n🎯 GENERADOR DE 10 Q&A CON KIMI K2 (Razonamiento)\n")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

qdrant = QdrantClient("http://localhost:6333")

print("📥 Extrayendo 10 preguntas...")
points, _ = qdrant.scroll(collection_name="materiales_academia", limit=220, with_payload=True, with_vectors=False)
questions = [p for p in points if p.payload.get("subcategory") == "preguntas"][100:110]
print(f"✅ {len(questions)} preguntas (offset 100-110)\n")

generated_qa = []

def query_kimi(prompt):
    """Consulta Groq API con Kimi K2"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "moonshotai/kimi-k2-instruct-0905",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2000
    }
    response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=90)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    raise Exception(f"Error: {response.status_code} - {response.text}")

for i, q in enumerate(questions, 1):
    print(f"--- Pregunta {i}/10 ---")
    prompt = f"""Eres experto en oposiciones de Seguridad Social España.
Razona paso a paso y crea 1 variación de esta pregunta oficial, transformándola completamente.

PREGUNTA ORIGINAL: {q.payload['text'][:500]}

INSTRUCCIONES:
1. Analiza qué conocimiento legal evalúa
2. Reformula completamente manteniendo el concepto
3. 4 opciones (A, B, C, D) con UNA correcta
4. Explicación MUY detallada con artículos específicos

Responde SOLO con JSON válido:
{{"pregunta": "texto reformulado completo", "opciones": ["A) op1", "B) op2", "C) op3", "D) op4"], "respuesta_correcta": "A", "explicacion": "explicacion legal muy detallada con artículos", "tema": "tema SS específico", "dificultad": "alta"}}"""
    
    try:
        result = query_kimi(prompt)
        json_start, json_end = result.find('{'), result.rfind('}') + 1
        if json_start >= 0:
            qa = json.loads(result[json_start:json_end])
            qa.update({
                'source_file': q.payload['filename'],
                'generated_at': datetime.now().isoformat(),
                'model': 'kimi-k2-instruct (Groq)'
            })
            generated_qa.append(qa)
            print(f"✅ Q&A {i} generada\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    time.sleep(1)  # Rate limiting más conservador

os.makedirs('dataset_output', exist_ok=True)
output_file = f'dataset_output/qa_kimi_10_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(generated_qa, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}\n✅ KIMI K2: {len(generated_qa)}/10 Q&A\nArchivo: {output_file}")

if generated_qa:
    print(f"\n📋 MUESTRA:")
    qa = generated_qa[0]
    print(f"Tema: {qa.get('tema')}")
    print(f"Pregunta: {qa['pregunta'][:150]}...")
