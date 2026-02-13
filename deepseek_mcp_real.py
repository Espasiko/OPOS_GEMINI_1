#!/usr/bin/env python3
"""
DeepSeek V3.1 + Function Calling + MCP REAL Integration
Usa MCP server local y Qdrant Cloud REAL
"""

import os
import json
import subprocess
from datetime import datetime
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Cargar .env del MCP server (tiene las credenciales reales)
load_dotenv("/home/spas/OPOS_GEMINI_1/mcp-server/.env")

# Configuración
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
MODEL = "deepseek-ai/deepseek-v3"

# MCP Server path
MCP_SERVER_PATH = "/home/spas/OPOS_GEMINI_1/mcp-server"

# ============================================
# TOOLS: MCP Server Integration (REAL)
# ============================================

def call_mcp_tool(tool_name: str, arguments: dict) -> dict:
    """
    Llama al MCP server local usando node
    
    Args:
        tool_name: Nombre del tool (search_rag, verify_boe, etc.)
        arguments: Argumentos del tool
    
    Returns:
        dict con resultado del MCP
    """
    print(f"  🔧 MCP Tool: {tool_name}({arguments})")
    
    try:
        # Preparar request MCP
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        # Llamar al MCP server via node
        cmd = [
            "node",
            f"{MCP_SERVER_PATH}/dist/index.js"
        ]
        
        result = subprocess.run(
            cmd,
            input=json.dumps(mcp_request),
            capture_output=True,
            text=True,
            timeout=30,
            cwd=MCP_SERVER_PATH
        )
        
        if result.returncode == 0:
            # Parsear respuesta MCP
            response = json.loads(result.stdout)
            if "result" in response:
                content = response["result"]["content"][0]["text"]
                return json.loads(content)
            else:
                return {"error": "No result in MCP response", "raw": result.stdout}
        else:
            return {
                "error": f"MCP server error (code {result.returncode})",
                "stderr": result.stderr,
                "stdout": result.stdout
            }
            
    except Exception as e:
        print(f"    ❌ Error llamando MCP: {e}")
        return {
            "error": str(e),
            "tool": tool_name
        }


def search_rag(query: str, limit: int = 5, score_threshold: float = 0.7) -> dict:
    """
    Tool: Busca en RAG (Qdrant Cloud) usando MCP server
    """
    return call_mcp_tool("search_rag", {
        "query": query,
        "limit": limit,
        "score_threshold": score_threshold
    })


def verify_boe(ley_id: str, articulo: str = None) -> dict:
    """
    Tool: Verifica ley en BOE oficial usando MCP server
    """
    args = {"ley_id": ley_id}
    if articulo:
        args["articulo"] = articulo
    return call_mcp_tool("verify_boe", args)


def get_law_summary(ley_name: str) -> dict:
    """
    Tool: Obtiene resumen de una ley usando MCP server
    """
    return call_mcp_tool("get_law_summary", {"ley_name": ley_name})


# ============================================
# TOOLS DEFINITION (OpenAI Format)
# ============================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_rag",
            "description": "Busca información en la base de conocimiento de leyes de Seguridad Social española (Qdrant Cloud con 48K artículos).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Pregunta o término legal a buscar"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Número máximo de resultados (default: 5)"
                    },
                    "score_threshold": {
                        "type": "number",
                        "description": "Umbral mínimo de similitud 0-1 (default: 0.7)"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "verify_boe",
            "description": "Verifica si una ley está vigente consultando el BOE oficial.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ley_id": {
                        "type": "string",
                        "description": "Identificador BOE (ej: 'BOE-A-2015-11724')"
                    },
                    "articulo": {
                        "type": "string",
                        "description": "Número de artículo específico (opcional)"
                    }
                },
                "required": ["ley_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_law_summary",
            "description": "Obtiene un resumen estructurado de una ley con sus artículos principales.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ley_name": {
                        "type": "string",
                        "description": "Nombre de la ley (ej: 'LGSS', 'TRLGSS')"
                    }
                },
                "required": ["ley_name"]
            }
        }
    }
]


# ============================================
# FUNCTION DISPATCHER
# ============================================

AVAILABLE_FUNCTIONS = {
    "search_rag": search_rag,
    "verify_boe": verify_boe,
    "get_law_summary": get_law_summary
}


def execute_function_call(function_name: str, arguments: dict) -> dict:
    """Ejecuta una función tool"""
    if function_name in AVAILABLE_FUNCTIONS:
        function = AVAILABLE_FUNCTIONS[function_name]
        return function(**arguments)
    else:
        return {"error": f"Función {function_name} no encontrada"}


# ============================================
# MAIN: DeepSeek V3.1 con Function Calling
# ============================================

def generate_case_with_mcp(case_topic: str, max_iterations: int = 5):
    """
    Genera caso legal usando DeepSeek V3.1 + Function Calling + MCP REAL
    
    Workflow:
    1. DeepSeek decide qué tools necesita
    2. Ejecutamos los tools (MCP server → Qdrant Cloud)
    3. DeepSeek usa los resultados REALES para generar caso verificado
    """
    print("🏭 GENERANDO CASO CON MCP REAL")
    print("="*80)
    print(f"📋 Tema: {case_topic}")
    print(f"🔧 Tools disponibles: {len(TOOLS)}")
    print(f"🌐 MCP Server: {MCP_SERVER_PATH}")
    print(f"☁️  Qdrant Cloud: europe-west3 (48K points)")
    print("="*80)
    
    if not HF_TOKEN:
        print("❌ ERROR: HF_TOKEN no encontrada")
        return None
    
    client = InferenceClient(token=HF_TOKEN)
    
    # Mensajes iniciales
    messages = [
        {
            "role": "system",
            "content": """Eres un experto en derecho de Seguridad Social española.

IMPORTANTE: Tienes acceso a herramientas (tools) REALES:
1. search_rag → Busca en 48K artículos de leyes (Qdrant Cloud)
2. verify_boe → Verifica leyes en BOE oficial
3. get_law_summary → Obtiene resumen de leyes

WORKFLOW OBLIGATORIO:
1. USA search_rag para encontrar artículos relevantes
2. USA verify_boe para verificar URLs y vigencia
3. USA get_law_summary para contexto adicional
4. SOLO ENTONCES genera el caso usando información VERIFICADA

NO inventes URLs ni textos legales. USA LAS TOOLS CON DATOS REALES."""
        },
        {
            "role": "user",
            "content": f"""Genera un caso práctico sobre: {case_topic}

INSTRUCCIONES OBLIGATORIAS (PASO A PASO):

PASO 1 - BUSCAR ARTÍCULOS (OBLIGATORIO):
Llama a la función search_rag con:
- query: "{case_topic} requisitos normativa"
- limit: 5

PASO 2 - VERIFICAR BOE (OBLIGATORIO):
Llama a la función verify_boe con:
- ley_id: "BOE-A-2015-11724" (TRLGSS)

PASO 3 - GENERAR CASO:
Usa los resultados de los tools para generar el caso en formato JSON:
{{
  "id": "SS_IPT_001",
  "enunciado": "...",
  "opciones": {{"a": "...", "b": "...", "c": "...", "d": "..."}},
  "respuesta_correcta": "c",
  "razonamiento_completo": {{...}},
  "normativa_verificada": [...]
}}

IMPORTANTE: PRIMERO llama a los tools, LUEGO genera el caso."""
        }
    ]
    
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n🔄 Iteración {iteration}/{max_iterations}")
        print("-"*80)
        
        try:
            # Llamar a DeepSeek con tools (FORZAR tool calling)
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="required",  # FORZAR al menos 1 tool call
                max_tokens=4000,
                temperature=0.7  # Aumentar creatividad
            )
            
            message = response.choices[0].message
            
            # ¿DeepSeek quiere llamar a un tool?
            if hasattr(message, 'tool_calls') and message.tool_calls:
                print(f"🔧 DeepSeek solicita {len(message.tool_calls)} tool calls:")
                
                # Añadir mensaje del asistente
                messages.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": message.tool_calls
                })
                
                # Ejecutar cada tool call
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    print(f"  → {function_name}({arguments})")
                    
                    # Ejecutar tool REAL (MCP server)
                    result = execute_function_call(function_name, arguments)
                    
                    # Añadir resultado a mensajes
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(result, ensure_ascii=False)
                    })
                    
                    print(f"    ✅ Resultado: {json.dumps(result, ensure_ascii=False)[:200]}...")
                
                # Continuar loop para que DeepSeek procese los resultados
                continue
            
            else:
                # DeepSeek terminó (no más tool calls)
                print("\n✅ DeepSeek terminó de generar el caso")
                final_content = message.content
                
                print("\n" + "="*80)
                print("📄 CASO GENERADO:")
                print("="*80)
                print(final_content[:1000] + "..." if len(final_content) > 1000 else final_content)
                
                # Guardar resultado
                output_file = "/home/spas/OPOS_GEMINI_1/caso_mcp_real.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump({
                        "model": MODEL,
                        "provider": "Novita via HuggingFace",
                        "timestamp": datetime.now().isoformat(),
                        "case_topic": case_topic,
                        "iterations": iteration,
                        "tool_calls_made": iteration - 1,
                        "mcp_server": MCP_SERVER_PATH,
                        "caso_generado": final_content,
                        "messages_history": messages
                    }, f, indent=2, ensure_ascii=False)
                
                print(f"\n💾 Guardado en: {output_file}")
                return final_content
                
        except Exception as e:
            print(f"\n❌ ERROR en iteración {iteration}: {e}")
            import traceback
            traceback.print_exc()
            break
    
    print(f"\n⚠️ Alcanzado límite de iteraciones ({max_iterations})")
    return None


if __name__ == "__main__":
    # Test: Generar 1 caso con MCP REAL
    generate_case_with_mcp(
        case_topic="Incapacidad Permanente Total - Requisitos de alta o asimilada"
    )
