#!/usr/bin/env python3
"""Generador de 5 Q&A de MÁXIMA DIFICULTAD con Claude API"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient
# Seleccionar preguntas más largas (más complejas)
all_q = [p for p in points if p.payload.get("subcategory") == "preguntas"]
questions = sorted(all_q, key=lambda x: len(x.payload.get('text', '')), reverse=True)[:5]
print(f"✅ {len(questions)} preguntas complejas seleccionadas\n")

generated_qa = []

def query_claude(prompt):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "claude-sonnet-4-5-20250929",  # Claude 4.5 Sonnet (mejor modelo actual)
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(CLAUDE_URL, headers=headers, json=payload, timeout=90)
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    raise Exception(f"Error: {response.status_code} - {response.text}")

for i, q in enumerate(questions, 1):
    print(f"--- Pregunta {i}/5 (MÁXIMA DIFICULTAD) ---")
    prompt = f"""Eres un EXPERTO MÁXIMO en oposiciones de Seguridad Social de España con 20 años de experiencia.

Tu tarea es crear UNA pregunta de MÁXIMA DIFICULTAD basada en esta pregunta oficial, pero MUCHO más compleja:

PREGUNTA ORIGINAL: {q.payload['text'][:600]}

REQUISITOS PARA MÁXIMA DIFICULTAD:
1. Combina MÚLTIPLES artículos de la LGSS en una sola pregunta
2. Incluye casos prácticos con cálculos o plazos específicos
3. Usa "preguntas trampa" donde varias opciones parezcan correctas
4. Requiere conocimiento profundo de excepciones y casos especiales
5. La explicación debe ser MUY detallada con referencias legales exactas

Responde SOLO con JSON válido:
{{"pregunta": "pregunta muy compleja y detallada", "opciones": ["A) opcion elaborada", "B) opcion elaborada", "C) opcion elaborada", "D) opcion elaborada"], "respuesta_correcta": "A", "explicacion": "explicacion MUY detallada con artículos específicos y jurisprudencia si aplica", "tema": "tema específico SS", "dificultad": "muy_alta", "articulos_relacionados": ["art. X LGSS", "art. Y RD..."]}}"""
    
    try:
        result = query_claude(prompt)
        json_start, json_end = result.find('{'), result.rfind('}') + 1
        if json_start >= 0:
            qa = json.loads(result[json_start:json_end])
            qa.update({'source_file': q.payload['filename'], 'generated_at': datetime.now().isoformat(), 'model': 'claude-sonnet-4-5 (API)'})
            generated_qa.append(qa)
            print(f"✅ Q&A {i} generada (dificultad: {qa.get('dificultad', 'muy_alta')})\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    time.sleep(1)

os.makedirs('dataset_output', exist_ok=True)
output_file = f'dataset_output/qa_claude_5_maxdif_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(generated_qa, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}\n✅ CLAUDE (Máx. Dificultad): {len(generated_qa)}/5 Q&A\nArchivo: {output_file}")

if generated_qa:
    print(f"\n📋 MUESTRA:")
    qa = generated_qa[0]
    print(f"Tema: {qa.get('tema')}")
    print(f"Pregunta: {qa['pregunta'][:200]}...")
    print(f"Artículos: {qa.get('articulos_relacionados', [])}")
