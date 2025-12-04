#!/usr/bin/env python3
"""
Test del agente Mistral con pregunta compleja sobre legislación española
"""

import os
from mistralai import Mistral
import json
from datetime import datetime

# Configuración
AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"
API_KEY = os.getenv("MISTRAL_API_KEY")

if not API_KEY:
    print("❌ ERROR: MISTRAL_API_KEY no configurada")
    print("Configura: export MISTRAL_API_KEY='tu_key'")
    exit(1)

# Cliente
client = Mistral(api_key=API_KEY)

# Pregunta compleja para probar
PREGUNTA_COMPLEJA = """
Analiza este caso práctico complejo sobre jubilación:

Un trabajador nacido el 15 de marzo de 1958 ha cotizado 37 años y 8 meses. 
Sus bases de cotización de los últimos 25 años son:
- Años 2000-2010: 1,800€/mes
- Años 2011-2020: 2,200€/mes  
- Años 2021-2024: 2,800€/mes

PREGUNTAS:
1. ¿A qué edad puede jubilarse en 2024 según el artículo 205 LGSS?
2. ¿Cuál es su base reguladora exacta?
3. ¿Qué porcentaje de pensión le corresponde?
4. ¿Cuál sería su pensión mensual aproximada?

REQUISITOS:
- Busca el artículo 205 LGSS actualizado en el BOE
- Calcula la base reguladora usando código Python
- Verifica los porcentajes según años cotizados
- Cita todas las fuentes legales

Devuelve un análisis completo con:
1. Respuestas detalladas
2. Cálculos paso a paso
3. Referencias legales del BOE
4. Código Python usado
"""

print("🤖 PRUEBA DEL AGENTE MISTRAL")
print("=" * 60)
print(f"Agent ID: {AGENT_ID}")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)
print("\n📝 PREGUNTA COMPLEJA:")
print(PREGUNTA_COMPLEJA)
print("\n" + "=" * 60)
print("⏳ Enviando al agente...")
print("=" * 60)

try:
    # Llamada al agente
    response = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{
            "role": "user",
            "content": PREGUNTA_COMPLEJA
        }]
    )
    
    print("\n✅ RESPUESTA DEL AGENTE:")
    print("=" * 60)
    print(response.choices[0].message.content)
    print("\n" + "=" * 60)
    
    # Analizar uso y costes
    print("\n📊 ANÁLISIS DE USO:")
    print("=" * 60)
    
    usage = response.usage
    print(f"Modelo usado: {response.model}")
    print(f"Input tokens: {usage.prompt_tokens:,}")
    print(f"Output tokens: {usage.completion_tokens:,}")
    print(f"Total tokens: {usage.total_tokens:,}")
    
    # Calcular costes
    # Mistral Large 2: Input $2/1M, Output $6/1M
    input_cost = (usage.prompt_tokens / 1_000_000) * 2.0
    output_cost = (usage.completion_tokens / 1_000_000) * 6.0
    
    # Costes de herramientas (estimado)
    # Web search: $30/1000 = $0.03/llamada
    # Code execution: $30/1000 = $0.03/llamada
    tool_cost = 0.06  # Estimado: 1 web search + 1 code execution
    
    total_cost = input_cost + output_cost + tool_cost
    
    print(f"\n💰 COSTES:")
    print(f"Input: ${input_cost:.6f}")
    print(f"Output: ${output_cost:.6f}")
    print(f"Herramientas (estimado): ${tool_cost:.6f}")
    print(f"TOTAL: ${total_cost:.6f}")
    
    # Coste por Q&A
    print(f"\n📈 PROYECCIÓN:")
    print(f"Coste por Q&A: ${total_cost:.6f}")
    print(f"Coste 10,000 Q&A: ${total_cost * 10000:.2f}")
    
    # Guardar respuesta
    output = {
        "timestamp": datetime.now().isoformat(),
        "agent_id": AGENT_ID,
        "model": response.model,
        "question": PREGUNTA_COMPLEJA,
        "response": response.choices[0].message.content,
        "usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens
        },
        "costs": {
            "input": input_cost,
            "output": output_cost,
            "tools": tool_cost,
            "total": total_cost
        }
    }
    
    with open("test_agent_result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("\n💾 Resultado guardado en: test_agent_result.json")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ PRUEBA COMPLETADA")
print("=" * 60)
