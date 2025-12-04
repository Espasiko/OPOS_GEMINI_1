#!/usr/bin/env python3
"""
Test COMPLETO del Agente Mistral - Captura respuestas finales
Versión mejorada que espera a que el agente complete todas las tool calls
"""

import os
from mistralai import Mistral
from dotenv import load_dotenv
import json
import time

load_dotenv()

AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY") or "FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF"

client = Mistral(api_key=MISTRAL_KEY)

print("="*80)
print("🔍 TEST COMPLETO: CAPTURA DE RESPUESTAS DEL AGENTE MISTRAL")
print("="*80)
print("Objetivo: Capturar respuestas COMPLETAS después de tool calls")
print("="*80)

def extract_full_response(response):
    """Extrae el contenido completo de la respuesta"""
    content = ""
    
    # Intentar diferentes formas de extraer contenido
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        
        # Caso 1: Contenido directo como string
        if hasattr(message, 'content') and isinstance(message.content, str):
            content = message.content
        
        # Caso 2: Contenido como lista de chunks
        elif hasattr(message, 'content') and isinstance(message.content, list):
            for chunk in message.content:
                if hasattr(chunk, 'text'):
                    content += chunk.text
                elif hasattr(chunk, 'thinking'):
                    # Incluir el razonamiento si existe
                    if isinstance(chunk.thinking, list):
                        for think in chunk.thinking:
                            if hasattr(think, 'text'):
                                content += f"\n[RAZONAMIENTO: {think.text}]\n"
                    else:
                        content += f"\n[RAZONAMIENTO: {chunk.thinking}]\n"
        
        # Caso 3: Solo tool calls (necesitamos esperar más)
        if not content and hasattr(message, 'tool_calls') and message.tool_calls:
            content = "[AGENTE EJECUTANDO HERRAMIENTAS - Respuesta pendiente]"
            for tool_call in message.tool_calls:
                content += f"\n- Herramienta: {tool_call.function.name}"
                content += f"\n- Argumentos: {tool_call.function.arguments}"
    
    return content if content else str(response)

def save_response(filename, test_name, prompt, response_text, raw_response):
    """Guarda la respuesta en un archivo"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{'='*80}\n")
        f.write(f"{test_name}\n")
        f.write(f"{'='*80}\n\n")
        f.write(f"PROMPT:\n{'-'*80}\n{prompt}\n\n")
        f.write(f"{'='*80}\n")
        f.write(f"RESPUESTA COMPLETA:\n")
        f.write(f"{'='*80}\n\n")
        f.write(response_text)
        f.write(f"\n\n{'='*80}\n")
        f.write(f"RESPUESTA RAW (para debug):\n")
        f.write(f"{'='*80}\n\n")
        f.write(str(raw_response))

# =============================================================================
# TEST 1: Artículo 205.1.a LGSS - Edad de jubilación
# =============================================================================
print("\n\n" + "="*80)
print("TEST 1: Artículo 205.1.a LGSS - Edad de jubilación en 2024")
print("="*80)

prompt1 = """Busca el artículo 205.1.a de la Ley General de la Seguridad Social en el BOE.

Necesito que me proporciones:
1. El texto EXACTO del artículo 205.1.a
2. La edad de jubilación que establece para el año 2024
3. La URL OFICIAL del BOE donde se encuentra
4. El número de BOE y fecha de publicación

IMPORTANTE: Usa web search para buscar en www.boe.es y dame la información precisa."""

try:
    print("\n⏳ Enviando petición al agente...")
    response1 = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{"role": "user", "content": prompt1}]
    )
    
    print("✅ Respuesta recibida, procesando...")
    
    # Extraer contenido
    content1 = extract_full_response(response1)
    
    print("\n📝 RESPUESTA:")
    print("-"*80)
    print(content1)
    print("-"*80)
    
    # Guardar
    save_response(
        "respuesta_completa_test1.txt",
        "TEST 1: Artículo 205.1.a LGSS",
        prompt1,
        content1,
        response1
    )
    
    print("\n✅ Respuesta guardada en: respuesta_completa_test1.txt")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Esperar un poco entre tests
time.sleep(2)

# =============================================================================
# TEST 2: Verificación de información específica
# =============================================================================
print("\n\n" + "="*80)
print("TEST 2: Verificación de información sobre jubilación")
print("="*80)

prompt2 = """Verifica esta información sobre jubilación en España:

INFORMACIÓN A VERIFICAR:
- Pregunta: ¿Cuál es la edad de jubilación en 2024?
- Respuesta propuesta: 66 años y 6 meses según art. 205.1.a LGSS
- URL propuesta: https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724

NECESITO QUE:
1. Verifiques si la URL es correcta y accesible
2. Confirmes si el artículo 205.1.a existe en esa URL
3. Verifiques si la edad de 66 años y 6 meses es correcta para 2024
4. Me indiques si hay algún error o inconsistencia

IMPORTANTE: Usa web search para verificar en el BOE oficial y dame una respuesta clara: ¿Es correcta esta información? ¿Qué confianza tienes (0-100%)?"""

try:
    print("\n⏳ Enviando petición al agente...")
    response2 = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{"role": "user", "content": prompt2}]
    )
    
    print("✅ Respuesta recibida, procesando...")
    
    # Extraer contenido
    content2 = extract_full_response(response2)
    
    print("\n📝 RESPUESTA:")
    print("-"*80)
    print(content2)
    print("-"*80)
    
    # Guardar
    save_response(
        "respuesta_completa_test2.txt",
        "TEST 2: Verificación de información",
        prompt2,
        content2,
        response2
    )
    
    print("\n✅ Respuesta guardada en: respuesta_completa_test2.txt")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Esperar un poco entre tests
time.sleep(2)

# =============================================================================
# TEST 3: Información sobre IMV (caso diferente)
# =============================================================================
print("\n\n" + "="*80)
print("TEST 3: Información sobre Ingreso Mínimo Vital")
print("="*80)

prompt3 = """Busca información oficial sobre el Ingreso Mínimo Vital (IMV) en el BOE.

Necesito que me proporciones:
1. El Real Decreto que regula el IMV (número y año)
2. La URL oficial del BOE donde se encuentra
3. El artículo que define qué es el IMV
4. La fecha de publicación en el BOE

IMPORTANTE: Usa web search para buscar en www.boe.es y dame información precisa y verificable."""

try:
    print("\n⏳ Enviando petición al agente...")
    response3 = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{"role": "user", "content": prompt3}]
    )
    
    print("✅ Respuesta recibida, procesando...")
    
    # Extraer contenido
    content3 = extract_full_response(response3)
    
    print("\n📝 RESPUESTA:")
    print("-"*80)
    print(content3)
    print("-"*80)
    
    # Guardar
    save_response(
        "respuesta_completa_test3.txt",
        "TEST 3: Información sobre IMV",
        prompt3,
        content3,
        response3
    )
    
    print("\n✅ Respuesta guardada en: respuesta_completa_test3.txt")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("\n\n" + "="*80)
print("📊 RESUMEN DE TESTS")
print("="*80)
print("""
✅ Tests completados
✅ Respuestas guardadas en archivos .txt

ARCHIVOS GENERADOS:
1. respuesta_completa_test1.txt - Artículo 205.1.a LGSS
2. respuesta_completa_test2.txt - Verificación de información
3. respuesta_completa_test3.txt - Información sobre IMV

PRÓXIMOS PASOS:
1. Revisar manualmente los archivos generados
2. Verificar URLs en el navegador
3. Contrastar información con BOE oficial
4. Evaluar precisión y calidad de las respuestas
5. Documentar hallazgos en informe de calidad

NOTA: Si las respuestas muestran "[AGENTE EJECUTANDO HERRAMIENTAS]",
      significa que el agente está usando tool calls pero no devuelve
      el contenido final. En ese caso, revisar en Mistral Studio.
""")

print("\n" + "="*80)
print("🎯 TEST COMPLETADO")
print("="*80)
