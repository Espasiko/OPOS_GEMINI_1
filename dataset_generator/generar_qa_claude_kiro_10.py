#!/usr/bin/env python3
"""Generador de 10 Q&A de MÁXIMA CALIDAD Y DIFICULTAD con Claude (Kiro)"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient

print("\n🎯 GENERADOR DE 10 Q&A MÁXIMA CALIDAD - KIRO + CLAUDE\n")

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
if not CLAUDE_API_KEY:
    raise ValueError("CLAUDE_API_KEY environment variable not set")
CLAUDE_URL = "https://api.anthropic.com/v1/messages"

qdrant = QdrantClient("http://localhost:6333")

print("📥 Seleccionando 10 preguntas más complejas...")
points, _ = qdrant.scroll(collection_name="materiales_academia", limit=243, with_payload=True, with_vectors=False)
all_q = [p for p in points if p.payload.get("subcategory") == "preguntas"]
# Seleccionar las más largas y complejas, diferentes a las anteriores
questions = sorted(all_q, key=lambda x: len(x.payload.get('text', '')), reverse=True)[5:15]
print(f"✅ {len(questions)} preguntas complejas seleccionadas\n")

generated_qa = []

def query_claude(prompt):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 3000,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(CLAUDE_URL, headers=headers, json=payload, timeout=120)
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    raise Exception(f"Error: {response.status_code} - {response.text}")

# Temas específicos para máxima dificultad
temas_avanzados = [
    "Cálculo de bases reguladoras con lagunas de cotización y coeficientes reductores",
    "Compatibilidad/incompatibilidad de prestaciones: jubilación activa, IT durante desempleo",
    "Responsabilidad empresarial en materia de SS: recargos, capitales coste, derivación",
    "Régimen de trabajadores desplazados y convenios bilaterales de SS",
    "Prestaciones por cese de actividad de autónomos: requisitos y cálculo",
    "Incapacidad permanente: grados, revisión, compatibilidades con trabajo",
    "Jubilación anticipada: coeficientes reductores según vía de acceso",
    "Cotización en pluriactividad y pluriempleo: bases y topes",
    "Prestaciones familiares: IMV, complemento infancia, asignaciones",
    "Recaudación ejecutiva: embargo de bienes, tercerías, prescripción"
]

for i, (q, tema) in enumerate(zip(questions, temas_avanzados), 1):
    print(f"--- Pregunta {i}/10: {tema[:50]}... ---")
    
    prompt = f"""Eres un CATEDRÁTICO de Derecho de la Seguridad Social con 30 años de experiencia preparando opositores para el Cuerpo Superior de la Administración de la Seguridad Social.

TAREA: Crear UNA pregunta de MÁXIMA DIFICULTAD Y CALIDAD sobre: {tema}

Basándote en esta pregunta de examen real como inspiración (pero creando algo MUCHO más complejo):
{q.payload['text'][:500]}

REQUISITOS OBLIGATORIOS PARA MÁXIMA DIFICULTAD:
1. CASO PRÁCTICO DETALLADO: Incluye fechas específicas, cantidades, situaciones concretas
2. MÚLTIPLES ARTÍCULOS: Combina al menos 3-4 artículos de la LGSS o normativa relacionada
3. CÁLCULOS O PLAZOS: Requiere conocer fórmulas, porcentajes o plazos exactos
4. PREGUNTA TRAMPA: Al menos 2 opciones deben parecer correctas a primera vista
5. EXCEPCIONES: Incluye alguna excepción o caso especial poco conocido
6. JURISPRUDENCIA: Si aplica, menciona criterios del TS o TGSS

FORMATO DE RESPUESTA (JSON válido):
{{
    "pregunta": "Caso práctico detallado con fechas, cantidades y situación específica. La pregunta debe requerir análisis profundo.",
    "opciones": [
        "A) Opción elaborada que parece correcta pero tiene un matiz incorrecto",
        "B) Opción correcta con todos los detalles técnicos precisos",
        "C) Opción que confunde conceptos similares",
        "D) Opción que aplica normativa derogada o incorrecta"
    ],
    "respuesta_correcta": "B",
    "explicacion": "Explicación EXHAUSTIVA de 300+ palabras que incluya: 1) Por qué la correcta es correcta con cita de artículos exactos, 2) Por qué cada incorrecta está mal, 3) Jurisprudencia relevante si aplica, 4) Errores comunes de los opositores",
    "tema": "{tema}",
    "dificultad": "muy_alta",
    "articulos_relacionados": ["art. X.Y LGSS", "art. Z RD...", "Disp. Adic. X"],
    "conceptos_clave": ["concepto1", "concepto2", "concepto3"],
    "errores_comunes": ["error típico 1", "error típico 2"]
}}

Responde SOLO con el JSON, sin texto adicional."""

    try:
        result = query_claude(prompt)
        json_start, json_end = result.find('{'), result.rfind('}') + 1
        if json_start >= 0:
            qa = json.loads(result[json_start:json_end])
            qa.update({
                'source_file': q.payload['filename'],
                'source_inspiration': q.payload['text'][:200],
                'generated_at': datetime.now().isoformat(),
                'model': 'claude-sonnet-4-5 (Kiro Max Quality)',
                'generator': 'Kiro AI Assistant'
            })
            generated_qa.append(qa)
            print(f"✅ Q&A {i} generada - Dificultad: {qa.get('dificultad', 'muy_alta')}")
            print(f"   Artículos: {qa.get('articulos_relacionados', [])[:3]}...\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    import time
    time.sleep(2)

os.makedirs('dataset_output', exist_ok=True)
output_file = f'dataset_output/qa_kiro_maxquality_10_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(generated_qa, f, indent=2, ensure_ascii=False)

print(f"\n{'='*70}")
print(f"✅ KIRO MÁXIMA CALIDAD: {len(generated_qa)}/10 Q&A GENERADAS")
print(f"{'='*70}")
print(f"Archivo: {output_file}")

if generated_qa:
    print(f"\n📋 MUESTRA DE CALIDAD:")
    qa = generated_qa[0]
    print(f"\n🎯 Tema: {qa.get('tema')}")
    print(f"📊 Dificultad: {qa.get('dificultad')}")
    print(f"📚 Artículos: {qa.get('articulos_relacionados', [])}")
    print(f"🔑 Conceptos: {qa.get('conceptos_clave', [])}")
    print(f"⚠️  Errores comunes: {qa.get('errores_comunes', [])}")
    print(f"\n❓ Pregunta:\n{qa['pregunta'][:300]}...")
    print(f"\n✅ Respuesta correcta: {qa['respuesta_correcta']}")
    print(f"\n📖 Explicación (extracto):\n{qa['explicacion'][:400]}...")
