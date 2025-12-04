#!/usr/bin/env python3
"""
Test usando Mistral Chat API (no agente)
Para verificar calidad de respuestas sobre legislación
"""

import os
from mistralai import Mistral
from dotenv import load_dotenv
import json

load_dotenv()

MISTRAL_KEY = os.getenv("MISTRAL_API_KEY") or "FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF"
client = Mistral(api_key=MISTRAL_KEY)

# Usar mistral-small (más disponible)
MODEL = "mistral-small-latest"

print("="*80)
print("🔍 TEST DE VERIFICACIÓN: MISTRAL CHAT API")
print("="*80)
print(f"Modelo: {MODEL}")
print("Objetivo: Verificar calidad de respuestas sobre legislación")
print("="*80)

def ask_mistral(prompt, temperature=0):
    """Hace una pregunta a Mistral y devuelve la respuesta"""
    try:
        response = client.chat.complete(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR: {e}"

def save_response(filename, test_name, prompt, response):
    """Guarda la respuesta en un archivo"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{'='*80}\n")
        f.write(f"{test_name}\n")
        f.write(f"{'='*80}\n\n")
        f.write(f"PROMPT:\n{'-'*80}\n{prompt}\n\n")
        f.write(f"{'='*80}\n")
        f.write(f"RESPUESTA:\n")
        f.write(f"{'='*80}\n\n")
        f.write(response)

# =============================================================================
# TEST 1: Conocimiento sobre artículo 205.1.a LGSS
# =============================================================================
print("\n\n" + "="*80)
print("TEST 1: Conocimiento sobre artículo 205.1.a LGSS")
print("="*80)

prompt1 = """Eres un experto en legislación española de Seguridad Social.

Pregunta: ¿Cuál es la edad de jubilación ordinaria en España para el año 2024 según el artículo 205.1.a de la Ley General de la Seguridad Social?

Proporciona:
1. La edad exacta (años y meses)
2. El artículo específico que lo regula
3. La URL del BOE donde se encuentra (si la conoces)
4. Cualquier matiz importante sobre esta edad

Responde de forma precisa y concisa."""

print("\n⏳ Consultando a Mistral...")
response1 = ask_mistral(prompt1)

print("\n📝 RESPUESTA:")
print("-"*80)
print(response1)
print("-"*80)

save_response("verificacion_test1.txt", "TEST 1: Edad de jubilación 2024", prompt1, response1)
print("\n✅ Guardado en: verificacion_test1.txt")

# =============================================================================
# TEST 2: Verificación de información específica
# =============================================================================
print("\n\n" + "="*80)
print("TEST 2: Verificación de información")
print("="*80)

prompt2 = """Eres un verificador de información legal sobre Seguridad Social en España.

Verifica esta información:
- Afirmación: "La edad de jubilación en 2024 es 66 años y 6 meses según el artículo 205.1.a de la LGSS"
- URL: https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724

Responde:
1. ¿Es correcta la edad de 66 años y 6 meses para 2024? (SÍ/NO/PARCIALMENTE)
2. ¿Es correcto el artículo 205.1.a? (SÍ/NO)
3. ¿Es correcta la URL del BOE? (SÍ/NO)
4. Si hay errores, ¿cuáles son?
5. Nivel de confianza en tu respuesta (0-100%)

Sé preciso y honesto. Si no estás seguro, dilo."""

print("\n⏳ Consultando a Mistral...")
response2 = ask_mistral(prompt2)

print("\n📝 RESPUESTA:")
print("-"*80)
print(response2)
print("-"*80)

save_response("verificacion_test2.txt", "TEST 2: Verificación de datos", prompt2, response2)
print("\n✅ Guardado en: verificacion_test2.txt")

# =============================================================================
# TEST 3: Información sobre IMV
# =============================================================================
print("\n\n" + "="*80)
print("TEST 3: Información sobre Ingreso Mínimo Vital")
print("="*80)

prompt3 = """Eres un experto en legislación española de Seguridad Social.

Pregunta: ¿Qué Real Decreto regula el Ingreso Mínimo Vital (IMV) en España?

Proporciona:
1. El número y año del Real Decreto
2. La fecha de publicación en el BOE
3. La URL del BOE donde se encuentra (si la conoces)
4. Un resumen breve de qué es el IMV (1-2 líneas)

Responde de forma precisa y concisa."""

print("\n⏳ Consultando a Mistral...")
response3 = ask_mistral(prompt3)

print("\n📝 RESPUESTA:")
print("-"*80)
print(response3)
print("-"*80)

save_response("verificacion_test3.txt", "TEST 3: Información IMV", prompt3, response3)
print("\n✅ Guardado en: verificacion_test3.txt")

# =============================================================================
# TEST 4: Caso con trampa (información incorrecta)
# =============================================================================
print("\n\n" + "="*80)
print("TEST 4: Detección de información incorrecta")
print("="*80)

prompt4 = """Eres un verificador de información legal sobre Seguridad Social en España.

Verifica esta información:
- Afirmación: "La edad de jubilación en 2024 es 65 años según el artículo 200 de la LGSS"

¿Es correcta esta información? Explica qué está mal (si algo está mal) y proporciona la información correcta."""

print("\n⏳ Consultando a Mistral...")
response4 = ask_mistral(prompt4)

print("\n📝 RESPUESTA:")
print("-"*80)
print(response4)
print("-"*80)

save_response("verificacion_test4.txt", "TEST 4: Detección de errores", prompt4, response4)
print("\n✅ Guardado en: verificacion_test4.txt")

# =============================================================================
# RESUMEN
# =============================================================================
print("\n\n" + "="*80)
print("📊 RESUMEN DE VERIFICACIÓN")
print("="*80)
print("""
✅ Tests completados con Mistral Chat API

ARCHIVOS GENERADOS:
1. verificacion_test1.txt - Edad de jubilación 2024
2. verificacion_test2.txt - Verificación de datos
3. verificacion_test3.txt - Información IMV
4. verificacion_test4.txt - Detección de errores

PRÓXIMOS PASOS:
1. Revisar las respuestas generadas
2. Contrastar con información oficial del BOE
3. Evaluar precisión y calidad
4. Documentar hallazgos

NOTA: Estas respuestas son del modelo Mistral sin herramientas.
      Representan el conocimiento base del modelo.
      Para comparar con el agente (que usa web_search),
      revisar las respuestas en Mistral Studio.
""")

print("\n" + "="*80)
print("🎯 VERIFICACIÓN COMPLETADA")
print("="*80)
