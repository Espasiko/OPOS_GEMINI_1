#!/usr/bin/env python3
"""
Test ÚNICO del Agente Mistral con pregunta compleja
Verifica si usa web search y code execution
"""

import os
from mistralai import Mistral
import json

# Tu Agent ID actualizado
AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"
MISTRAL_KEY = "FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF"

client = Mistral(api_key=MISTRAL_KEY)

print("="*80)
print("🧪 TEST ÚNICO: AGENTE MISTRAL CON PREGUNTA COMPLEJA")
print("="*80)
print(f"Agent ID: {AGENT_ID}")
print(f"Max tokens: 4096 (aumentado)")
print("="*80)

# Pregunta compleja que requiere web search + verificación
prompt = """
Genera UNA pregunta tipo test sobre el artículo 205 de la LGSS sobre edad de jubilación.

REQUISITOS OBLIGATORIOS:
1. Busca en el BOE el texto exacto del artículo 205.1.a LGSS
2. Verifica cuál es la edad de jubilación en 2024
3. Genera 1 pregunta con 4 opciones (a, b, c, d)
4. Incluye explicación detallada
5. Cita la URL exacta del BOE que consultaste

Formato JSON:
{
  "pregunta": "...",
  "opciones": {
    "a": "...",
    "b": "...",
    "c": "...",
    "d": "..."
  },
  "respuesta_correcta": "c",
  "explicacion": "...",
  "referencia_legal": "art. 205.1.a LGSS",
  "fuente_boe": "https://www.boe.es/...",
  "verificado_con_web_search": true,
  "confidence": 0.95
}

IMPORTANTE: Usa web search para buscar en BOE antes de responder.
"""

try:
    print("\n⏳ Enviando request al agente...")
    print(f"Prompt: {len(prompt)} caracteres\n")
    
    response = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    print("="*80)
    print("📝 RESPUESTA COMPLETA:")
    print("="*80)
    print(response.choices[0].message.content)
    print("="*80)
    
    # Analizar la respuesta
    content = response.choices[0].message.content
    
    # Verificar si menciona web search
    if "boe.es" in content.lower():
        print("\n✅ CONTIENE URL DEL BOE")
    else:
        print("\n⚠️ NO CONTIENE URL DEL BOE")
    
    # Verificar si es JSON válido
    try:
        if "```json" in content:
            json_text = content.split("```json")[1].split("```")[0]
        else:
            json_text = content
        
        qa_data = json.loads(json_text.strip())
        print("✅ JSON VÁLIDO")
        
        # Verificar campos
        if "verificado_con_web_search" in qa_data:
            print(f"✅ Web search usado: {qa_data['verificado_con_web_search']}")
        else:
            print("⚠️ No indica si usó web search")
        
        if "fuente_boe" in qa_data:
            print(f"✅ Fuente BOE: {qa_data['fuente_boe']}")
        else:
            print("⚠️ No incluye fuente BOE")
        
        if "confidence" in qa_data:
            print(f"✅ Confianza: {qa_data['confidence']}")
        
    except json.JSONDecodeError:
        print("⚠️ NO ES JSON VÁLIDO")
    
    # Verificar uso de herramientas
    print("\n" + "="*80)
    print("🔧 ANÁLISIS DE HERRAMIENTAS:")
    print("="*80)
    
    if hasattr(response.choices[0].message, 'tool_calls'):
        print("✅ HERRAMIENTAS DETECTADAS:")
        for tool in response.choices[0].message.tool_calls:
            print(f"  - {tool.function.name}")
    else:
        print("⚠️ No se detectaron tool_calls en la respuesta")
        print("   Esto puede significar:")
        print("   1. El agente no tiene herramientas activadas")
        print("   2. Las herramientas se usaron pero no se reportan")
        print("   3. El agente decidió no usarlas")
    
    # Tokens y coste
    if hasattr(response, 'usage'):
        print("\n" + "="*80)
        print("📊 TOKENS Y COSTE:")
        print("="*80)
        print(f"Input tokens: {response.usage.prompt_tokens}")
        print(f"Output tokens: {response.usage.completion_tokens}")
        print(f"Total tokens: {response.usage.total_tokens}")
        
        # Calcular coste (Mistral Large 2)
        input_cost = (response.usage.prompt_tokens / 1_000_000) * 2.0
        output_cost = (response.usage.completion_tokens / 1_000_000) * 6.0
        total_cost = input_cost + output_cost
        
        print(f"\nCoste:")
        print(f"  Input: ${input_cost:.6f}")
        print(f"  Output: ${output_cost:.6f}")
        print(f"  TOTAL: ${total_cost:.6f}")
        print(f"\nProyección 200 Q&A: ${total_cost * 200:.2f}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"\nTipo de error: {type(e).__name__}")
    
    if "capacity" in str(e).lower():
        print("\n⚠️ LÍMITE DE CAPACIDAD ALCANZADO")
        print("Soluciones:")
        print("1. Esperar unas horas")
        print("2. Usar API normal de Mistral (sin agente)")
        print("3. Contactar soporte para aumentar límite")

print("\n" + "="*80)
print("📋 CONCLUSIONES:")
print("="*80)
print("""
Si el agente funcionó:
- ✅ Revisar si usó web search
- ✅ Revisar calidad de la respuesta
- ✅ Verificar URLs del BOE
- ✅ Comprobar formato JSON

Si dio error de capacidad:
- ⚠️ Usar API normal de Mistral
- ⚠️ Implementar web search manualmente
- ⚠️ O esperar a que se libere capacidad

RECOMENDACIÓN:
Usar Mistral Large 2 API normal + RAG de Qdrant
para generar Q&A críticas sin límites de capacidad.
""")
