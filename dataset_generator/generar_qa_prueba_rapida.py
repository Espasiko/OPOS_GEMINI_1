#!/usr/bin/env python3
"""
Generador rápido de Q&A - Solo 5 preguntas para prueba
"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient

print("\n🎯 GENERADOR RÁPIDO DE Q&A\n")

# Conectar
print("🔄 Conectando...")
qdrant = QdrantClient(url="http://localhost:6333")
ollama_url = "http://localhost:11434"

# Extraer 5 preguntas
print("📥 Extrayendo 5 preguntas...")
points, _ = qdrant.scroll(
    collection_name="materiales_academia",
    limit=5,
    with_payload=True,
    with_vectors=False
)

print(f"✅ Extraídas {len(points)} preguntas\n")

# Generar variaciones
qa_generated = []
for i, point in enumerate(points, 1):
    payload = point.payload
    text = payload.get("text", "")[:300]
    
    print(f"--- Pregunta {i}/{len(points)} ---")
    print(f"Archivo: {payload.get('filename', 'N/A')}")
    print(f"Texto: {text}...\n")
    
    prompt = f"""Crea 1 pregunta tipo test sobre Seguridad Social basada en este contenido:

{text}

Formato JSON:
{{
  "pregunta": "Pregunta reformulada",
  "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "respuesta_correcta": "A",
  "explicacion": "Por qué es correcta",
  "tema": "Seguridad Social",
  "dificultad": "intermedia"
}}

Solo JSON, sin texto adicional."""
    
    try:
        print("🔄 Consultando Mistral...")
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": "mistral:latest",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "max_tokens": 1000}
            },
            timeout=180  # 3 minutos
        )
        
        if response.status_code == 200:
            result = response.json().get('response', '')
            
            # Extraer JSON
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = result[json_start:json_end]
                qa = json.loads(json_str)
                qa["source_file"] = payload.get("filename", "")
                qa["generated_at"] = datetime.now().isoformat()
                qa_generated.append(qa)
                print(f"✅ Q&A generada\n")
            else:
                print(f"⚠️  No se encontró JSON\n")
        else:
            print(f"❌ Error: {response.status_code}\n")
            
    except Exception as e:
        print(f"❌ Error: {e}\n")
        continue

# Exportar
if qa_generated:
    os.makedirs("dataset_output", exist_ok=True)
    output_file = f"dataset_output/qa_prueba_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(qa_generated, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"✅ COMPLETADO")
    print(f"{'='*60}")
    print(f"Q&A generadas: {len(qa_generated)}")
    print(f"Archivo: {output_file}")
    
    # Mostrar muestra
    if qa_generated:
        print(f"\n--- MUESTRA ---")
        qa = qa_generated[0]
        print(f"Pregunta: {qa['pregunta']}")
        print(f"Respuesta: {qa['respuesta_correcta']}")
        print(f"Tema: {qa['tema']}")
else:
    print("\n❌ No se generaron Q&A")
