#!/usr/bin/env python3
"""Generador de 3 Q&A de prueba con Mistral Local"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient
import hashlib

print("\n🎯 GENERADOR DE 3 Q&A DE PRUEBA\n")

# Conectar
qdrant = QdrantClient("http://localhost:6333")
ollama_url = "http://localhost:11434"

# Extraer 3 preguntas
print("📥 Extrayendo 3 preguntas...")
points, _ = qdrant.scroll(
    collection_name="materiales_academia",
    limit=50,
    with_payload=True,
    with_vectors=False
)

questions = [p for p in points if p.payload.get("subcategory") == "preguntas"][:3]
print(f"✅ Encontradas {len(questions)} preguntas\n")

generated_qa = []

# Generar 1 variación para cada pregunta
for i, q in enumerate(questions, 1):
    print(f"--- Pregunta {i}/3 ---")
    print(f"Archivo: {q.payload['filename']}")
    print(f"Texto: {q.payload['text'][:150]}...")
    
    prompt = f"""Eres experto en oposiciones de Seguridad Social España.
Crea 1 variación de esta pregunta oficial, transformándola completamente.

PREGUNTA: {q.payload['text'][:400]}

Responde SOLO con JSON válido:
{{"pregunta": "texto reformulado", "opciones": ["A) op1", "B) op2", "C) op3", "D) op4"], "respuesta_correcta": "A", "explicacion": "explicacion", "tema": "tema SS", "dificultad": "intermedia"}}"""
    
    print(f"🔄 Consultando Mistral (puede tardar 2-3 minutos)...")
    
    try:
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={"model": "mistral:latest", "prompt": prompt, "stream": False},
            timeout=300  # 5 minutos timeout
        )
        
        if response.status_code == 200:
            result = response.json().get('response', '')
            
            # Extraer JSON
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            
            if json_start >= 0:
                try:
                    qa = json.loads(result[json_start:json_end])
                    qa['source_file'] = q.payload['filename']
                    qa['source_page'] = q.payload.get('page_number', 0)
                    qa['generated_at'] = datetime.now().isoformat()
                    qa['model'] = 'mistral:latest (ollama)'
                    generated_qa.append(qa)
                    print(f"✅ Q&A {i} generada correctamente\n")
                except Exception as e:
                    print(f"❌ Error parseando JSON: {e}\n")
            else:
                print(f"❌ No se encontró JSON en respuesta\n")
        else:
            print(f"❌ Error HTTP: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

# Exportar resultados
if generated_qa:
    os.makedirs('dataset_output', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'dataset_output/qa_prueba_3_{timestamp}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(generated_qa, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"✅ GENERACIÓN COMPLETADA")
    print(f"{'='*60}")
    print(f"Q&A generadas: {len(generated_qa)}/3")
    print(f"Archivo: {output_file}")
    print(f"\n📋 MUESTRA:")
    for i, qa in enumerate(generated_qa, 1):
        print(f"\n--- Q&A {i} ---")
        print(f"Tema: {qa['tema']}")
        print(f"Pregunta: {qa['pregunta'][:100]}...")
        print(f"Opciones: {len(qa['opciones'])} opciones")
        print(f"Correcta: {qa['respuesta_correcta']}")
else:
    print("\n❌ No se generaron Q&A")
