#!/usr/bin/env python3
"""
Test simple del Agente Mistral Studio
Prueba básica para verificar que funciona
"""

import os
from pathlib import Path

# Cargar .env.backend
env_path = Path("backend/.env.backend")
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

try:
    from mistralai import Mistral
    
    # Configuración
    api_key = os.getenv("MISTRAL_API_KEY", "")
    agent_id = os.getenv("MISTRAL_AGENT_ID", "ag_019ad601946d7323a81c544229de40a1")
    
    print("\n" + "=" * 70)
    print("🤖 TEST AGENTE MISTRAL STUDIO")
    print("=" * 70)
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else 'N/A'}")
    print(f"🤖 Agent ID: {agent_id}")
    
    if not api_key:
        print("❌ No hay API key configurada")
        exit(1)
    
    # Crear cliente
    client = Mistral(api_key=api_key)
    
    # Test 1: Pregunta simple
    print("\n📝 TEST 1: Pregunta Simple")
    print("-" * 50)
    print("Pregunta: ¿Cuál es la edad de jubilación ordinaria en España en 2024?")
    
    # Usar API de Agentes (no chat.complete)
    response = client.agents.complete(
        agent_id=agent_id,
        messages=[
            {"role": "user", "content": "¿Cuál es la edad de jubilación ordinaria en España en 2024? Responde de forma breve y precisa."}
        ]
    )
    
    if response.choices:
        content = response.choices[0].message.content
        print(f"\n✅ Respuesta del agente:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        
        if hasattr(response, 'usage'):
            print(f"\n📊 Tokens usados: {response.usage.total_tokens}")
            print(f"   - Input: {response.usage.prompt_tokens}")
            print(f"   - Output: {response.usage.completion_tokens}")
        
        # Test 2: Pregunta que requiere búsqueda
        print("\n📝 TEST 2: Pregunta con Verificación BOE")
        print("-" * 50)
        print("Pregunta: ¿Qué dice exactamente el artículo 205.1.a de la LGSS?")
        
        response2 = client.agents.complete(
            agent_id=agent_id,
            messages=[
                {"role": "user", "content": "¿Qué dice exactamente el artículo 205.1.a de la Ley General de la Seguridad Social? Cita el texto oficial del BOE."}
            ]
        )
        
        if response2.choices:
            content2 = response2.choices[0].message.content
            print(f"\n✅ Respuesta del agente:")
            print("-" * 50)
            print(content2)
            print("-" * 50)
            
            if hasattr(response2, 'usage'):
                print(f"\n📊 Tokens usados: {response2.usage.total_tokens}")
        
        print("\n" + "=" * 70)
        print("✅ TESTS COMPLETADOS - AGENTE FUNCIONANDO")
        print("=" * 70)
        
    else:
        print("❌ No se recibió respuesta")
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Instalar: pip install mistralai")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
