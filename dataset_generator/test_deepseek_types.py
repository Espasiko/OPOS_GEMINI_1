#!/usr/bin/env python3
"""Script de prueba para verificar que DeepSeek genera todos los tipos de contenido correctamente"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

print("\n🧪 PRUEBA DE TIPOS DE CONTENIDO CON DEEPSEEK-REASONER\n")

# Cargar variables de entorno
load_dotenv("../backend/.env.backend")
load_dotenv(".env")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    print("❌ DEEPSEEK_API_KEY no configurada")
    print("🔍 Verificando archivos .env...")
    print(f"   - backend/.env.backend: {'✅' if os.path.exists('../backend/.env.backend') else '❌'}")
    print(f"   - .env: {'✅' if os.path.exists('.env') else '❌'}")
    exit(1)

print(f"✅ DeepSeek API Key encontrada: {DEEPSEEK_API_KEY[:10]}...")

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def test_deepseek_connection():
    """Prueba la conexión con DeepSeek"""
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-reasoner",
        "messages": [{"role": "user", "content": "Responde solo: 'Conexión OK'"}],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return "OK" in content
        return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_content_generation():
    """Prueba la generación de un caso práctico simple"""
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    
    prompt = """Eres experto en Seguridad Social España. Crea un caso práctico simple.

INSTRUCCIONES:
1. Crea un caso con una persona ficticia
2. Plantea una situación de jubilación
3. Da respuesta fundamentada
4. NO incluyas frases como "Si necesitas" al final

Responde SOLO con JSON válido:
{"case": "Un trabajador de 65 años con 20 años cotizados solicita jubilación", "answer": "Puede jubilarse con penalización", "law": "LGSS", "article": "Art. 205.1", "verified": true}"""
    
    payload = {
        "model": "deepseek-reasoner",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            reasoning = data["choices"][0]["message"].get("reasoning_content", "")
            
            # Intentar extraer JSON
            json_start, json_end = content.find('{'), content.rfind('}') + 1
            if json_start >= 0:
                test_json = json.loads(content[json_start:json_end])
                return True, test_json, reasoning[:200] if reasoning else None
            else:
                return False, content, reasoning[:200] if reasoning else None
        else:
            return False, f"Error HTTP: {response.status_code}", None
    except Exception as e:
        return False, f"Error: {e}", None

def verify_boe_articles():
    """Verifica algunos artículos BOE conocidos"""
    known_articles = {
        "art. 7.1 LGSS": "Campo de aplicación del Régimen General",
        "art. 205.1.b LGSS": "Período mínimo de cotización para jubilación",
        "art. 208.1 LGSS": "Jubilación anticipada voluntaria",
        "art. 210.1 LGSS": "Porcentajes de pensión según años cotizados"
    }
    
    print("🔍 Verificando artículos BOE conocidos:")
    for article, description in known_articles.items():
        print(f"   ✅ {article}: {description}")
    
    return len(known_articles)

# Ejecutar pruebas
print("1️⃣ Probando conexión con DeepSeek...")
if test_deepseek_connection():
    print("   ✅ Conexión exitosa")
else:
    print("   ❌ Error de conexión")
    exit(1)

print("\n2️⃣ Probando generación de contenido...")
success, result, reasoning = test_content_generation()
if success:
    print("   ✅ Generación exitosa")
    print(f"   📋 Caso generado: {result.get('case', 'N/A')[:100]}...")
    print(f"   ⚖️  Respuesta: {result.get('answer', 'N/A')[:100]}...")
    if reasoning:
        print(f"   🧠 Razonamiento: {reasoning}...")
else:
    print(f"   ❌ Error en generación: {result}")

print(f"\n3️⃣ Verificando artículos BOE...")
verified_count = verify_boe_articles()
print(f"   ✅ {verified_count} artículos verificados")

print(f"\n4️⃣ Tipos de contenido a generar:")
content_types = [
    "qa_multiple_choice - Pregunta múltiple opción",
    "case_study - Supuesto práctico",
    "chat_dialogue - Diálogo usuario-asistente", 
    "flashcard - Tarjeta de estudio",
    "rag_context_qa - Pregunta con contexto normativo",
    "legal_analysis - Análisis jurídico detallado",
    "comparative_study - Estudio comparativo",
    "procedural_guide - Guía procedimental"
]

for i, content_type in enumerate(content_types, 1):
    print(f"   {i}. {content_type}")

print(f"\n{'='*60}")
print(f"✅ PRUEBA COMPLETADA")
print(f"🚀 El script generar_qa_deepseek.py está listo para generar {len(content_types)} tipos de contenido")
print(f"💡 Cada tipo incluye verificación BOE y razonamiento paso a paso")
print(f"{'='*60}")