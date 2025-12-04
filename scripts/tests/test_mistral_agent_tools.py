#!/usr/bin/env python3
"""
Test del Agente Mistral con herramientas activadas
Verifica si usa web search, code execution, etc.
"""

import os
from mistralai import Mistral
from dotenv import load_dotenv
import json

load_dotenv()

# Tu Agent ID
AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY") or "FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF"

client = Mistral(api_key=MISTRAL_KEY)

print("="*80)
print("🧪 TEST: AGENTE MISTRAL CON HERRAMIENTAS")
print("="*80)
print(f"Agent ID: {AGENT_ID}")
print(f"API Key: {MISTRAL_KEY[:20]}...")
print("="*80)

# Test 1: Pregunta que requiere web search
print("\n\n" + "="*80)
print("TEST 1: Web Search - Buscar artículo 205 LGSS en BOE")
print("="*80)

prompt1 = """Verifica el artículo 205 de la Ley General de la Seguridad Social.

Necesito que:
1. Busques en el BOE el texto exacto del artículo 205.1.a
2. Me digas cuál es la edad de jubilación en 2024
3. Me des la URL exacta del BOE

Usa web search para buscar en www.boe.es"""

try:
    response1 = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{
            "role": "user",
            "content": prompt1
        }]
    )
    
    print("\n📝 RESPUESTA:")
    print("-"*80)
    print(response1.choices[0].message.content)
    print("-"*80)
    
    # Verificar si usó herramientas
    if hasattr(response1.choices[0].message, 'tool_calls'):
        print("\n🔧 HERRAMIENTAS USADAS:")
        for tool in response1.choices[0].message.tool_calls:
            print(f"  - {tool.function.name}")
    else:
        print("\n⚠️ No se detectaron tool_calls en la respuesta")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

# Test 2: Pregunta que requiere code execution
print("\n\n" + "="*80)
print("TEST 2: Code Execution - Calcular base reguladora")
print("="*80)

prompt2 = """Calcula la base reguladora de jubilación con estos datos:
- Últimos 24 meses de cotización
- Base de cotización: 2,500€ cada mes

Usa Python para hacer el cálculo y muéstrame el código ejecutado."""

try:
    response2 = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{
            "role": "user",
            "content": prompt2
        }]
    )
    
    print("\n📝 RESPUESTA:")
    print("-"*80)
    print(response2.choices[0].message.content)
    print("-"*80)
    
    # Verificar si usó herramientas
    if hasattr(response2.choices[0].message, 'tool_calls'):
        print("\n🔧 HERRAMIENTAS USADAS:")
        for tool in response2.choices[0].message.tool_calls:
            print(f"  - {tool.function.name}")
    else:
        print("\n⚠️ No se detectaron tool_calls en la respuesta")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

# Test 3: Verificación de Q&A con contexto
print("\n\n" + "="*80)
print("TEST 3: Verificación de Q&A")
print("="*80)

prompt3 = """Verifica esta Q&A:

Pregunta: ¿Cuál es la edad de jubilación en 2024?
Respuesta: 66 años y 6 meses según art. 205.1.a LGSS
URL: https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724

Necesito que:
1. Busques en el BOE si el artículo existe
2. Verifiques si la edad es correcta
3. Verifiques si la URL es correcta
4. Me des un score de confianza (0-1)

Formato de respuesta JSON:
{
  "verified": true/false,
  "confidence": 0.95,
  "issues": ["lista de problemas encontrados"],
  "recommendation": "APROBAR/CORREGIR/RECHAZAR"
}"""

try:
    response3 = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{
            "role": "user",
            "content": prompt3
        }]
    )
    
    print("\n📝 RESPUESTA:")
    print("-"*80)
    print(response3.choices[0].message.content)
    print("-"*80)
    
    # Verificar si usó herramientas
    if hasattr(response3.choices[0].message, 'tool_calls'):
        print("\n🔧 HERRAMIENTAS USADAS:")
        for tool in response3.choices[0].message.tool_calls:
            print(f"  - {tool.function.name}")
    else:
        print("\n⚠️ No se detectaron tool_calls en la respuesta")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

# Resumen
print("\n\n" + "="*80)
print("📊 RESUMEN DEL TEST")
print("="*80)
print("""
OBJETIVO: Verificar si el agente Mistral usa herramientas automáticamente

HERRAMIENTAS ESPERADAS:
- web_search: Para buscar en BOE
- code_interpreter: Para ejecutar Python
- retrieval: Para buscar en documentos

PRÓXIMOS PASOS:
1. Si NO usa herramientas → Revisar configuración en Mistral Studio
2. Si SÍ usa herramientas → Integrar en pipeline de generación
3. Mejorar instrucciones del agente si es necesario

NOTA: Las instrucciones del agente deben estar en Mistral Studio
      para que se apliquen automáticamente.
""")
