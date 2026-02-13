#!/usr/bin/env python3
"""
Test Salamandra R1 con MCP BOE - Verificar si puede usar tools
"""

import requests
import json
from datetime import datetime

# Configuración
OLLAMA_URL = "http://localhost:11434/api/chat"  # CAMBIO: usar /api/chat para tools
MODEL = "salamandra-r1:q5km"

def query_ollama_with_tools(prompt: str, system: str = None) -> dict:
    """Query Ollama con Salamandra R1 y tools usando /api/chat"""
    
    # Definir tools disponibles (MCP BOE simulado)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "buscar_articulo_boe",
                "description": "Busca un artículo específico en la LGSS (Ley General de Seguridad Social)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numero_articulo": {
                            "type": "string",
                            "description": "Número del artículo a buscar (ej: '173', '174')"
                        },
                        "ley": {
                            "type": "string",
                            "description": "Nombre de la ley (ej: 'LGSS', 'TRLGSS')"
                        }
                    },
                    "required": ["numero_articulo", "ley"]
                }
            }
        }
    ]
    
    # Formato /api/chat: usar messages array
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": MODEL,
        "messages": messages,  # CAMBIO: messages en vez de prompt
        "stream": False,
        "tools": tools,  # Añadir tools
        "options": {
            "temperature": 0.1,
            "top_k": 20,
            "top_p": 0.85,
            "num_ctx": 4096,
            "num_predict": 512
        }
    }
    
    print(f"\n🔧 DEBUG - Payload enviado:")
    print(f"   Endpoint: {OLLAMA_URL}")
    print(f"   Tools definidos: {len(tools)}")
    print(f"   Messages: {len(messages)}")
    
    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()
    return response.json()

def test_salamandra_con_mcp():
    """Test Salamandra R1 con MCP BOE"""
    
    print("=" * 80)
    print("🧪 TEST SALAMANDRA R1 + MCP BOE - TOOLS")
    print("=" * 80)
    print(f"Modelo: {MODEL}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Pregunta que debería activar el tool
    pregunta = """
¿Qué dice el artículo 173 de la LGSS sobre la cuantía del subsidio de IT?

Si necesitas consultar el artículo, usa la función buscar_articulo_boe.
"""
    
    system_prompt = """Eres un experto en Seguridad Social española.

Tienes acceso a la función buscar_articulo_boe para consultar artículos de la LGSS.

Si necesitas información específica de un artículo, DEBES usar la función.

Responde de forma concisa citando los artículos consultados."""
    
    print("\n📋 PREGUNTA:")
    print(pregunta)
    print("\n⏳ Procesando con Salamandra R1 + MCP BOE...\n")
    
    start_time = datetime.now()
    
    try:
        result = query_ollama_with_tools(pregunta, system_prompt)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 80)
        print("🔍 DEBUG - Respuesta completa de Ollama:")
        print("=" * 80)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("=" * 80)
        
        print("\n" + "=" * 80)
        print("🤖 RESPUESTA SALAMANDRA R1:")
        print("=" * 80)
        
        # /api/chat devuelve formato diferente
        message = result.get("message", {})
        
        # Verificar si usó tools
        if "tool_calls" in message and message["tool_calls"]:
            print("✅ ¡SALAMANDRA INTENTÓ USAR TOOLS!")
            print("\nTool calls:")
            print(json.dumps(message["tool_calls"], indent=2, ensure_ascii=False))
        else:
            print("❌ Salamandra NO usó tools")
            print(f"   Claves en message: {list(message.keys())}")
        
        response = message.get("content", "")
        print(f"\nRespuesta:\n{response}")
        
        print("=" * 80)
        print(f"\n⏱️  Tiempo: {duration:.2f}s")
        print(f"📊 Tokens: {result.get('eval_count', 'N/A')}")
        
        # Guardar resultado
        output_file = f"salamandra_mcp_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "modelo": MODEL,
                "fecha": datetime.now().isoformat(),
                "pregunta": pregunta,
                "system_prompt": system_prompt,
                "respuesta": response,
                "tool_calls": message.get("tool_calls"),
                "duracion_segundos": duration,
                "tokens_generados": result.get('eval_count', 0),
                "uso_tools": "tool_calls" in message and message["tool_calls"],
                "respuesta_completa": result
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Resultado guardado en: {output_file}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_salamandra_con_mcp()
