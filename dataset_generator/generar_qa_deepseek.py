#!/usr/bin/env python3
"""Generador de 20 Q&A con DeepSeek REASONER (modelo de razonamiento tipo o1)"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient
import time

print("\n🎯 GENERADOR DE 20 Q&A CON DEEPSEEK-REASONER (Chain of Thought)\n")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY environment variable not set")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

qdrant = QdrantClient("http://localhost:6333")

print("📥 Extrayendo 20 preguntas...")
points, _ = qdrant.scroll(collection_name="materiales_academia", limit=150, with_payload=True, with_vectors=False)
questions = [p for p in points if p.payload.get("subcategory") == "preguntas"][40:60]
print(f"✅ {len(questions)} preguntas (offset 40-60)\n")

generated_qa = []

def query_deepseek_reasoner(prompt):
    """Usa el modelo deepseek-reasoner con Chain of Thought"""
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-reasoner",  # Modelo de razonamiento tipo o1
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000
    }
    response = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=120)
    if response.status_code == 200:
        data = response.json()
        # El modelo devuelve reasoning_content (CoT) y content (respuesta final)
        reasoning = data["choices"][0]["message"].get("reasoning_content", "")
        content = data["choices"][0]["message"]["content"]
        return content, reasoning
    raise Exception(f"Error: {response.status_code} - {response.text}")

for i, q in enumerate(questions, 1):
    print(f"--- Pregunta {i}/20 ---")
    prompt = f"""Eres experto en oposiciones de Seguridad Social España.
Razona paso a paso y crea 1 variación de esta pregunta oficial, transformándola completamente.

PREGUNTA ORIGINAL: {q.payload['text'][:500]}

INSTRUCCIONES:
1. Analiza qué conocimiento legal evalúa la pregunta
2. Reformula completamente manteniendo el mismo concepto
3. Crea 4 opciones donde solo UNA sea correcta
4. La explicación debe ser detallada con referencias legales

Responde SOLO con JSON válido:
{{"pregunta": "texto reformulado completo", "opciones": ["A) op1", "B) op2", "C) op3", "D) op4"], "respuesta_correcta": "A", "explicacion": "explicacion legal detallada con artículos", "tema": "tema SS específico", "dificultad": "intermedia"}}"""
    
    try:
        content, reasoning = query_deepseek_reasoner(prompt)
        json_start, json_end = content.find('{'), content.rfind('}') + 1
        if json_start >= 0:
            qa = json.loads(content[json_start:json_end])
            qa.update({
                'source_file': q.payload['filename'],
                'generated_at': datetime.now().isoformat(),
                'model': 'deepseek-reasoner (CoT)',
                'reasoning_preview': reasoning[:500] if reasoning else None  # Guardar parte del razonamiento
            })
            generated_qa.append(qa)
            print(f"✅ Q&A {i} generada (con Chain of Thought)\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    time.sleep(1)

os.makedirs('dataset_output', exist_ok=True)
output_file = f'dataset_output/qa_deepseek_reasoner_20_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(generated_qa, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}\n✅ DEEPSEEK-REASONER: {len(generated_qa)}/20 Q&A\nArchivo: {output_file}")

if generated_qa:
    print(f"\n📋 MUESTRA con razonamiento:")
    qa = generated_qa[0]
    print(f"Tema: {qa.get('tema')}")
    print(f"Pregunta: {qa['pregunta'][:150]}...")
    if qa.get('reasoning_preview'):
        print(f"Razonamiento (preview): {qa['reasoning_preview'][:200]}...")
