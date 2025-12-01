#!/usr/bin/env python3
"""
Test del Agente Mistral con ID ag_019ad601946d7323a81c544229de40a1
Características:
- Puede crear código
- Tiene acceso web
- Usa Mistral Medium
- NOTA: "malo sin instrucciones" según comentario
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('backend/.env.backend')

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
AGENT_ID = os.getenv('AGENTE_ID')

print("="*70)
print("🤖 TEST AGENTE MISTRAL")
print("="*70)
print(f"API Key: {MISTRAL_API_KEY[:20]}..." if MISTRAL_API_KEY else "❌ No API Key")
print(f"Agent ID: {AGENT_ID}")
print(f"Modelo: Mistral Medium")
print("="*70 + "\n")


async def test_mistral_agent_with_instructions():
    """Test del agente CON instrucciones claras"""
    
    print("📝 TEST 1: Agente CON instrucciones (recomendado)")
    print("-" * 70)
    
    url = "https://api.mistral.ai/v1/agents/completions"
    
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # PROMPT CON INSTRUCCIONES CLARAS (para compensar "malo sin instrucciones")
    payload = {
        "agent_id": AGENT_ID,
        "messages": [
            {
                "role": "system",
                "content": """Eres un asistente experto en derecho español de Seguridad Social.
Tu tarea es responder preguntas de forma precisa, citando siempre las fuentes legales.
Cuando generes código, usa Python y comenta bien cada sección.
Si necesitas buscar en web, hazlo solo de fuentes oficiales (BOE, CENDOJ, seg-social.es)."""
            },
            {
                "role": "user",
                "content": "¿Cuál es el artículo de la LGSS que regula la incapacidad temporal? Dame el número exacto y un breve resumen."
            }
        ]
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            print("⏳ Enviando request...")
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ RESPUESTA EXITOSA:")
                print(f"Choices: {len(result.get('choices', []))}")
                
                if result.get('choices'):
                    message = result['choices'][0].get('message', {})
                    content = message.get('content', '')
                    print(f"\n📄 Contenido:\n{content}\n")
                    
                    # Verificar si usó web search
                    if 'tool_calls' in message:
                        print(f"🔧 Tool calls: {message['tool_calls']}")
                
                print(f"\n📊 Uso tokens:")
                usage = result.get('usage', {})
                print(f"   Input: {usage.get('prompt_tokens', 0)}")
                print(f"   Output: {usage.get('completion_tokens', 0)}")
                print(f"   Total: {usage.get('total_tokens', 0)}")
                
            else:
                print(f"\n❌ ERROR {response.status_code}:")
                print(response.text)
                
        except Exception as e:
            print(f"\n❌ EXCEPCIÓN: {e}")


async def test_mistral_agent_code_generation():
    """Test generación de código con el agente"""
    
    print("\n" + "="*70)
    print("💻 TEST 2: Generación de código")
    print("-" * 70)
    
    url = "https://api.mistral.ai/v1/agents/completions"
    
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "agent_id": AGENT_ID,
        "messages": [
            {
                "role": "system",
                "content": "Eres un experto en Python. Genera código limpio, bien comentado y siguiendo PEP 8."
            },
            {
                "role": "user",
                "content": """Crea una función Python que valide un DNI español.
Debe:
1. Verificar formato (8 dígitos + letra)
2. Validar letra correcta según algoritmo oficial
3. Devolver True/False
4. Incluir docstring y ejemplos"""
            }
        ]
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            print("⏳ Generando código...")
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ CÓDIGO GENERADO:")
                
                if result.get('choices'):
                    content = result['choices'][0]['message'].get('content', '')
                    print(f"\n{content}\n")
                    
                    usage = result.get('usage', {})
                    print(f"\n📊 Tokens: {usage.get('total_tokens', 0)}")
                
            else:
                print(f"\n❌ ERROR {response.status_code}:")
                print(response.text)
                
        except Exception as e:
            print(f"\n❌ EXCEPCIÓN: {e}")


async def test_mistral_agent_web_access():
    """Test acceso web del agente"""
    
    print("\n" + "="*70)
    print("🌐 TEST 3: Acceso web (búsqueda BOE)")
    print("-" * 70)
    
    url = "https://api.mistral.ai/v1/agents/completions"
    
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "agent_id": AGENT_ID,
        "messages": [
            {
                "role": "system",
                "content": "Eres un asistente legal. Cuando busques información, usa solo fuentes oficiales del BOE."
            },
            {
                "role": "user",
                "content": "Busca en el BOE la fecha de publicación del Real Decreto Legislativo 8/2015 (LGSS) y dime qué dice su artículo 1."
            }
        ]
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            print("⏳ Buscando en web...")
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ RESULTADO CON WEB SEARCH:")
                
                if result.get('choices'):
                    message = result['choices'][0]['message']
                    content = message.get('content', '')
                    print(f"\n📄 Respuesta:\n{content}\n")
                    
                    if 'tool_calls' in message:
                        print("\n🔧 Herramientas usadas:")
                        for tool in message['tool_calls']:
                            print(f"   - {tool}")
                
            else:
                print(f"\n❌ ERROR {response.status_code}:")
                print(response.text)
                
        except Exception as e:
            print(f"\n❌ EXCEPCIÓN: {e}")


async def test_gemini_25_pro():
    """Test Gemini 2.5 Pro con la API key actual"""
    
    print("\n" + "="*70)
    print("🔷 TEST BONUS: Gemini 2.5 Pro")
    print("-" * 70)
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_key:
        print("❌ No hay GEMINI_API_KEY")
        return
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Resume en 2 líneas qué es la incapacidad temporal según la LGSS"
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 200
        }
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            print("⏳ Testing Gemini 2.0 Flash...")
            response = await client.post(
                url,
                params={"key": gemini_key},
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ GEMINI FUNCIONA:")
                
                if result.get('candidates'):
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    print(f"\n📄 Respuesta:\n{text}\n")
                    
                    usage = result.get('usageMetadata', {})
                    print(f"📊 Tokens: {usage.get('totalTokenCount', 0)}")
                
            else:
                print(f"\n❌ ERROR {response.status_code}:")
                print(response.text)
                
        except Exception as e:
            print(f"\n❌ EXCEPCIÓN: {e}")


async def main():
    """Ejecuta todos los tests"""
    
    if not MISTRAL_API_KEY or not AGENT_ID:
        print("\n❌ ERROR: Faltan credenciales")
        print("Verifica MISTRAL_API_KEY y AGENTE_ID en .env.backend")
        return
    
    # Test 1: Con instrucciones (recomendado)
    await test_mistral_agent_with_instructions()
    
    # Test 2: Generación de código
    await test_mistral_agent_code_generation()
    
    # Test 3: Web access
    await test_mistral_agent_web_access()
    
    # Bonus: Gemini 2.5
    await test_gemini_25_pro()
    
    print("\n" + "="*70)
    print("✅ TESTS COMPLETADOS")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
