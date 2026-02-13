#!/usr/bin/env python3
"""
Script de prueba para Salamandra R1 con MCP BOE local
Prueba CoT (Chain of Thought) y búsquedas en Qdrant
"""

import json
import requests
from typing import List, Dict

print("=" * 80)
print("🧪 PRUEBAS SALAMANDRA R1 + MCP BOE")
print("=" * 80)

# Configuración
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "salamandra-7b-r1"  # Ajustar según el nombre real en Ollama

# Consultas de prueba
TEST_QUERIES = [
    "¿Cuál es el periodo de vacaciones de los funcionarios públicos?",
    "¿Cuáles son los requisitos para acceder a la función pública?",
    "Explica qué es el silencio administrativo positivo",
    "¿Cuál es la diferencia entre recurso de alzada y recurso de reposición?"
]

def query_salamandra(prompt: str, system_prompt: str = None) -> str:
    """Consulta a Salamandra R1 vía Ollama"""
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,  # Bajo para respuestas legales precisas
            "top_p": 0.9,
            "num_predict": 1024
        }
    }
    
    if system_prompt:
        payload["system"] = system_prompt
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except Exception as e:
        return f"❌ Error: {e}"

# System prompt para modo legal
LEGAL_SYSTEM_PROMPT = """Eres un asistente experto en legislación española y oposiciones.
Tu objetivo es responder con precisión legal basándote en la normativa vigente.

PROTOCOLO DE RESPUESTA:
1. Analiza la pregunta cuidadosamente
2. Identifica las leyes y artículos relevantes
3. Proporciona una respuesta clara y precisa
4. Cita siempre los artículos y leyes específicas

Usa un estilo claro y educativo, apropiado para opositores."""

print("\n📋 PRUEBAS BÁSICAS DE COT (Sin MCP)")
print("-" * 80)

for i, query in enumerate(TEST_QUERIES, 1):
    print(f"\n{'='*80}")
    print(f"CONSULTA {i}: {query}")
    print('='*80)
    
    print("\n🤔 Generando respuesta...")
    response = query_salamandra(query, LEGAL_SYSTEM_PROMPT)
    
    print(f"\n📝 RESPUESTA:")
    print(response[:500] + "..." if len(response) > 500 else response)
    
    # Análisis de calidad
    has_cot = "<think>" in response or "razonamiento:" in response.lower()
    has_citation = "artículo" in response.lower() or "ley" in response.lower()
    
    print(f"\n📊 ANÁLISIS:")
    print(f"  CoT detectado: {'✅' if has_cot else '❌'}")
    print(f"  Citas legales: {'✅' if has_citation else '❌'}")
    print(f"  Longitud: {len(response)} caracteres")

print("\n\n" + "=" * 80)
print("✅ PRUEBAS COMPLETADAS")
print("=" * 80)

print("\n📝 PRÓXIMOS PASOS:")
print("  1. Integrar con MCP BOE para búsquedas en Qdrant")
print("  2. Probar function calling con herramientas")
print("  3. Comparar con DeepSeek R1 y GPT-4o")
print("  4. Medir latencia y calidad de respuestas")
