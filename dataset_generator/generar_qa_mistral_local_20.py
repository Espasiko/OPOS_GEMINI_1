#!/usr/bin/env python3
"""Generador de 20 Q&A con Mistral Local (Ollama)"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient
import time

print("\n🎯 GENERADOR DE 20 Q&A CON MISTRAL LOCAL (OLLAMA)\n")

# Config
OLLAMA_URL = "http://localhost:11434"

# Conectar a Qdrant
qdrant = QdrantClient("http://localhost:6333")

# Extraer 20 preguntas diferentes (offset 20 para no repetir las de API)
print("📥 Extrayendo 20 preguntas de Qdrant (diferentes a las de API)...")
points, _ = qdrant.scroll(
    collection_name="materiales_academia",
    limit=100,
    with_payload=True,
    with_vectors=False
)

# Usar preguntas 21-40 para no repetir
all_questions = [p for p in points if p.payload.get("subcategory") == "preguntas"]
questions = all_questions[20:40]  # Offset para usar preguntas diferentes
print(f"✅ Encontradas {len(questions)} preguntas (offset 20-40)\n")

generated_qa = []
errors = 0
timeouts = 0

def query_ollama(prompt, timeout=180):
    """Consulta Ollama con timeout"""
    payload = {
        "model": "mistral:latest",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "top_p": 0.9}
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=timeout)
    if response.status_code == 200:
        return response.json().get('response', '')
    else:
        raise Exception(f"Ollama Error: {response.status_code}")

# Generar Q&A
for i, q in enumerate(questions, 1):
    print(f"--- Pregunta {i}/20 ---")
    print(f"Archivo: {q.payload['filename']}")
    print(f"🔄 Generando (puede tardar 2-3 min)...")
    
    prompt = f"""Eres experto en oposiciones de Seguridad Social España.
Crea 1 variación de esta pregunta oficial, transformándola completamente.

PREGUNTA: {q.payload['text'][:400]}

Responde SOLO JSON:
{{"pregunta": "texto reformulado", "opciones": ["A) op1", "B) op2", "C) op3", "D) op4"], "respuesta_correcta": "A", "explicacion": "explicacion", "tema": "tema SS", "dificultad": "intermedia"}}"""
    
    try:
        result = query_ollama(prompt, timeout=180)
        
        # Extraer JSON
        json_start = result.find('{')
        json_end = result.rfind('}') + 1
        
        if json_start >= 0:
            qa = json.loads(result[json_start:json_end])
            qa['source_file'] = q.payload['filename']
            qa['source_page'] = q.payload.get('page_number', 0)
            qa['generated_at'] = datetime.now().isoformat()
            qa['model'] = 'mistral:latest (ollama local)'
            generated_qa.append(qa)
            print(f"✅ Q&A {i} generada ({len(generated_qa)} total)\n")
        else:
            print(f"❌ No JSON en respuesta\n")
            errors += 1
            
    except requests.exceptions.Timeout:
        print(f"⏱️ Timeout (>3 min)\n")
        timeouts += 1
    except Exception as e:
        print(f"❌ Error: {e}\n")
        errors += 1
    
    # Pausa entre preguntas
    time.sleep(2)

# Exportar
os.makedirs('dataset_output', exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'dataset_output/qa_mistral_local_20_{timestamp}.json'

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(generated_qa, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"✅ GENERACIÓN MISTRAL LOCAL COMPLETADA")
print(f"{'='*60}")
print(f"Q&A generadas: {len(generated_qa)}/20")
print(f"Errores: {errors}")
print(f"Timeouts: {timeouts}")
print(f"Archivo: {output_file}")

# Mostrar 2 muestras
if generated_qa:
    print(f"\n📋 MUESTRAS:")
    for i, qa in enumerate(generated_qa[:2], 1):
        print(f"\n--- Muestra {i} ---")
        print(f"Tema: {qa['tema']}")
        print(f"Pregunta: {qa['pregunta'][:150]}...")
        print(f"Correcta: {qa['respuesta_correcta']}")
