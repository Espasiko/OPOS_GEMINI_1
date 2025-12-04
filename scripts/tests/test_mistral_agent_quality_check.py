#!/usr/bin/env python3
"""
Test de CALIDAD del Agente Mistral
Captura respuestas completas y URLs para verificación manual
"""

import os
from mistralai import Mistral
from dotenv import load_dotenv
import json

load_dotenv()

AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY") or "FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF"

client = Mistral(api_key=MISTRAL_KEY)

print("="*80)
print("🔍 TEST DE CALIDAD: AGENTE MISTRAL")
print("="*80)
print("Objetivo: Capturar respuestas completas para verificación de calidad")
print("="*80)

# Test 1: Buscar artículo 205 LGSS
print("\n\n" + "="*80)
print("TEST 1: Buscar artículo 205.1.a LGSS en BOE")
print("="*80)

prompt1 = """Busca el artículo 205.1.a de la Ley General de la Seguridad Social en el BOE.

Necesito que me proporciones:
1. El texto EXACTO del artículo 205.1.a
2. La edad de jubilación que establece para 2024
3. La URL OFICIAL del BOE donde se encuentra
4. El número de BOE y fecha de publicación

Usa web search para buscar en www.boe.es"""

try:
    response1 = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{"role": "user", "content": prompt1}]
    )
    
    # Extraer contenido
    content = ""
    if hasattr(response1.choices[0].message, 'content'):
        if isinstance(response1.choices[0].message.content, str):
            content = response1.choices[0].message.content
        elif isinstance(response1.choices[0].message.content, list):
            # Si es una lista de chunks
            for chunk in response1.choices[0].message.content:
                if hasattr(chunk, 'text'):
                    content += chunk.text
                elif hasattr(chunk, 'thinking'):
                    content += f"\n[THINKING: {chunk.thinking}]\n"
    
    print("\n📝 RESPUESTA COMPLETA:")
    print("-"*80)
    print(content if content else str(response1.choices[0].message))
    print("-"*80)
    
    # Guardar respuesta
    with open("test_quality_response_1.txt", "w", encoding="utf-8") as f:
        f.write("TEST 1: Artículo 205.1.a LGSS\n")
        f.write("="*80 + "\n\n")
        f.write(content if content else str(response1.choices[0].message))
        f.write("\n\n" + "="*80 + "\n")
        f.write("RESPUESTA RAW:\n")
        f.write(str(response1))
    
    print("\n✅ Respuesta guardada en: test_quality_response_1.txt")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

# Test 2: Verificar URL específica
print("\n\n" + "="*80)
print("TEST 2: Verificar información específica")
print("="*80)

prompt2 = """Verifica esta información sobre jubilación:

Pregunta: ¿Cuál es la edad de jubilación en 2024?
Respuesta propuesta: 66 años y 6 meses según art. 205.1.a LGSS
URL propuesta: https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724

Necesito que:
1. Verifiques si la URL es correcta y accesible
2. Confirmes si el artículo 205.1.a existe en esa URL
3. Verifiques si la edad de 66 años y 6 meses es correcta para 2024
4. Me indiques cualquier error o inconsistencia

Usa web search para verificar en el BOE oficial."""

try:
    response2 = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{"role": "user", "content": prompt2}]
    )
    
    # Extraer contenido
    content = ""
    if hasattr(response2.choices[0].message, 'content'):
        if isinstance(response2.choices[0].message.content, str):
            content = response2.choices[0].message.content
        elif isinstance(response2.choices[0].message.content, list):
            for chunk in response2.choices[0].message.content:
                if hasattr(chunk, 'text'):
                    content += chunk.text
                elif hasattr(chunk, 'thinking'):
                    content += f"\n[THINKING: {chunk.thinking}]\n"
    
    print("\n📝 RESPUESTA COMPLETA:")
    print("-"*80)
    print(content if content else str(response2.choices[0].message))
    print("-"*80)
    
    # Guardar respuesta
    with open("test_quality_response_2.txt", "w", encoding="utf-8") as f:
        f.write("TEST 2: Verificación de URL y contenido\n")
        f.write("="*80 + "\n\n")
        f.write(content if content else str(response2.choices[0].message))
        f.write("\n\n" + "="*80 + "\n")
        f.write("RESPUESTA RAW:\n")
        f.write(str(response2))
    
    print("\n✅ Respuesta guardada en: test_quality_response_2.txt")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

# Test 3: Buscar información sobre prestaciones
print("\n\n" + "="*80)
print("TEST 3: Buscar información sobre IMV")
print("="*80)

prompt3 = """Busca información oficial sobre el Ingreso Mínimo Vital (IMV) en el BOE.

Necesito que me proporciones:
1. El Real Decreto que regula el IMV
2. La URL oficial del BOE
3. El artículo que define qué es el IMV
4. La cuantía básica establecida

Usa web search para buscar en www.boe.es"""

try:
    response3 = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{"role": "user", "content": prompt3}]
    )
    
    # Extraer contenido
    content = ""
    if hasattr(response3.choices[0].message, 'content'):
        if isinstance(response3.choices[0].message.content, str):
            content = response3.choices[0].message.content
        elif isinstance(response3.choices[0].message.content, list):
            for chunk in response3.choices[0].message.content:
                if hasattr(chunk, 'text'):
                    content += chunk.text
                elif hasattr(chunk, 'thinking'):
                    content += f"\n[THINKING: {chunk.thinking}]\n"
    
    print("\n📝 RESPUESTA COMPLETA:")
    print("-"*80)
    print(content if content else str(response3.choices[0].message))
    print("-"*80)
    
    # Guardar respuesta
    with open("test_quality_response_3.txt", "w", encoding="utf-8") as f:
        f.write("TEST 3: Información sobre IMV\n")
        f.write("="*80 + "\n\n")
        f.write(content if content else str(response3.choices[0].message))
        f.write("\n\n" + "="*80 + "\n")
        f.write("RESPUESTA RAW:\n")
        f.write(str(response3))
    
    print("\n✅ Respuesta guardada en: test_quality_response_3.txt")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n\n" + "="*80)
print("📊 RESUMEN")
print("="*80)
print("""
✅ Tests completados
✅ Respuestas guardadas en archivos .txt

PRÓXIMO PASO:
1. Revisar manualmente los archivos test_quality_response_*.txt
2. Verificar URLs en el navegador
3. Contrastar información con BOE oficial
4. Evaluar calidad de las respuestas
""")
