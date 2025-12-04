#!/usr/bin/env python3
"""
Test del Agente Mistral Studio con herramientas reales

Este script prueba el agente creado en Mistral Studio (ag_019ad601946d7323a81c544229de40a1)
para ver sus capacidades y cómo usarlo.
"""

import os
import sys
from pathlib import Path

# Cargar .env.backend
env_path = Path(__file__).parent.parent / ".env.backend"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from mistralai import Mistral

# Configuración
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_AGENT_ID = os.getenv("MISTRAL_AGENT_ID", "ag_019ad601946d7323a81c544229de40a1")

def test_agent_info():
    """Obtiene información del agente"""
    print("\n" + "=" * 60)
    print("🤖 INFORMACIÓN DEL AGENTE MISTRAL STUDIO")
    print("=" * 60)
    
    print(f"\n📋 Agent ID: {MISTRAL_AGENT_ID}")
    print(f"🔑 API Key: {MISTRAL_API_KEY[:10]}...{MISTRAL_API_KEY[-4:]}")
    
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    # Intentar obtener info del agente
    try:
        # La API de agentes puede tener un endpoint específico
        # Por ahora, probamos con una consulta simple
        print("\n✅ Cliente Mistral inicializado correctamente")
        return client
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_agent_chat(client, query: str):
    """Prueba el chat con el agente"""
    print(f"\n🔍 Query: {query}")
    print("-" * 40)
    
    try:
        # Usar el agente como modelo
        response = client.agents.complete(
            agent_id=MISTRAL_AGENT_ID,
            messages=[
                {"role": "user", "content": query}
            ]
        )
        
        print(f"✅ Respuesta recibida")
        
        # Extraer contenido
        if hasattr(response, 'choices') and response.choices:
            message = response.choices[0].message
            print(f"\n📝 Contenido:\n{message.content[:500]}...")
            
            # Ver si usó herramientas
            if hasattr(message, 'tool_calls') and message.tool_calls:
                print(f"\n🔧 Herramientas usadas:")
                for tc in message.tool_calls:
                    print(f"   - {tc.function.name}: {tc.function.arguments[:100]}...")
        
        return response
        
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        
        # Intentar método alternativo
        print("\n🔄 Intentando método alternativo (chat.complete)...")
        try:
            response = client.chat.complete(
                model=MISTRAL_AGENT_ID,  # Usar agent_id como modelo
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            
            if hasattr(response, 'choices') and response.choices:
                content = response.choices[0].message.content
                print(f"✅ Respuesta (alternativo):\n{content[:500]}...")
                return response
                
        except Exception as e2:
            print(f"❌ Error alternativo: {e2}")
        
        return None

def test_agent_with_boe_query():
    """Prueba específica para ver si el agente puede acceder al BOE"""
    print("\n" + "=" * 60)
    print("🌐 TEST: ACCESO A BOE DESDE AGENTE")
    print("=" * 60)
    
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    queries = [
        "¿Cuál es el texto exacto del artículo 205 de la LGSS sobre jubilación? Busca en el BOE.",
        "Verifica si la URL https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724 está activa",
        "¿Cuáles son los requisitos de edad para la jubilación anticipada según el BOE actual?"
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        result = test_agent_chat(client, query)
        if result:
            print("✅ Query completada")
        else:
            print("❌ Query fallida")

def test_agent_tools_discovery():
    """Intenta descubrir qué herramientas tiene el agente"""
    print("\n" + "=" * 60)
    print("🔧 DESCUBRIMIENTO DE HERRAMIENTAS DEL AGENTE")
    print("=" * 60)
    
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    # Preguntar al agente sobre sus capacidades
    discovery_query = """
    Eres un agente de Mistral. Por favor, lista todas las herramientas y capacidades que tienes disponibles.
    Incluye:
    1. ¿Puedes acceder a internet/web?
    2. ¿Puedes buscar en el BOE?
    3. ¿Qué funciones/tools tienes definidas?
    4. ¿Puedes hacer cálculos?
    
    Responde de forma estructurada.
    """
    
    result = test_agent_chat(client, discovery_query)
    return result

def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print("🧪 TESTS DEL AGENTE MISTRAL STUDIO")
    print("=" * 60)
    
    # 1. Info básica
    client = test_agent_info()
    if not client:
        print("❌ No se pudo inicializar el cliente")
        return False
    
    # 2. Descubrir herramientas
    test_agent_tools_discovery()
    
    # 3. Test con BOE
    test_agent_with_boe_query()
    
    print("\n" + "=" * 60)
    print("✅ TESTS COMPLETADOS")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
