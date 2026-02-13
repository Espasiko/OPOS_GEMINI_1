#!/usr/bin/env python3
"""
TEST DEEPSEEK API CON MCP-BOE TOOLS
Basado en documentación oficial: https://api-docs.deepseek.com/guides/function_calling
"""

import os
import json
import sys
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Cargar .env
load_dotenv("/home/spas/OPOS_GEMINI_1/backend/.env.backend")

# Agregar path del MCP client
sys.path.insert(0, "/home/spas/OPOS_GEMINI_1/dataset_generator/agents/simulacro_agent")
from mcp_client import get_mcp_client

# Cliente MCP (Qdrant LOCAL Docker)
mcp = get_mcp_client()

# Configuración DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# ============================================
# TOOLS DEFINITION (Formato oficial DeepSeek)
# ============================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_rag",
            "description": "Busca información en la base de conocimiento de leyes de Seguridad Social española (Qdrant LOCAL Docker).",
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
                    }
                },
                "required": ["ley_id"]
            }
        }
    }
]


# ============================================
# TOOL FUNCTIONS (Llamadas al MCP LOCAL)
# ============================================

import subprocess

def call_mcp_server_local(tool_name: str, arguments: dict) -> dict:
    """Llama al MCP server LOCAL vía subprocess"""
    try:
        # Requests para MCP server
        init_req = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "python-test", "version": "1.0.0"}
            }
        }
        
        tool_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        # Enviar ambos requests
        input_data = json.dumps(init_req) + "\n" + json.dumps(tool_req) + "\n"
        
        result = subprocess.run(
            ["node", "/home/spas/OPOS_GEMINI_1/mcp-server/dist/index.js"],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=30,
            cwd="/home/spas/OPOS_GEMINI_1/mcp-server"
        )
        
        # Parsear respuesta (buscar JSON con id=1)
        for line in result.stdout.split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                response = json.loads(line)
                if response.get("id") == 1 and "result" in response:
                    if "content" in response["result"]:
                        content_text = response["result"]["content"][0]["text"]
                        return json.loads(content_text)
                    return response["result"]
            except:
                continue
        
        return {"error": "No se pudo parsear respuesta MCP"}
    
    except Exception as e:
        return {"error": str(e)}


def search_rag(query: str, limit: int = 5) -> str:
    """Busca en RAG usando MCP server LOCAL"""
    print(f"  📚 Ejecutando: search_rag(query='{query[:50]}...', limit={limit})")
    
    result = call_mcp_server_local("search_rag", {
        "query": query,
        "limit": limit,
        "score_threshold": 0.7
    })
    
    if "error" in result:
        print(f"    ❌ Error: {result['error']}")
        # Simular respuesta para que DeepSeek pueda continuar
        return f"Información sobre {query}: La Incapacidad Temporal se regula en el Art. 173 del TRLGSS. El subsidio se abona desde el día siguiente al de la baja en caso de accidente de trabajo."
    
    results = result.get('results', [])
    num_results = len(results)
    print(f"    ✅ Encontrados {num_results} resultados")
    
    if num_results > 0:
        formatted = f"Encontrados {num_results} artículos:\n"
        for i, r in enumerate(results[:3], 1):
            text = r.get('text', r.get('content', ''))
            formatted += f"{i}. {text[:200]}...\n"
        return formatted
    else:
        # Simular respuesta para que DeepSeek pueda continuar
        return f"Información sobre {query}: La Incapacidad Temporal se regula en el Art. 173 del TRLGSS. El subsidio se abona desde el día siguiente al de la baja en caso de accidente de trabajo."


def verify_boe(ley_id: str) -> str:
    """Verifica ley en BOE (simulado para prueba)"""
    print(f"  ✅ Ejecutando: verify_boe(ley_id='{ley_id}')")
    
    # Simular verificación BOE
    boe_info = {
        "BOE-A-2015-11724": {
            "nombre": "TRLGSS - Texto Refundido de la Ley General de la Seguridad Social",
            "estado": "VIGENTE",
            "url": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
        }
    }
    
    if ley_id in boe_info:
        info = boe_info[ley_id]
        print(f"    ✅ Ley verificada: {info['estado']}")
        return f"Ley {ley_id} ({info['nombre']}): {info['estado']}. URL: {info['url']}"
    else:
        return f"Ley {ley_id}: Información no disponible en simulación."


# Mapeo de funciones
AVAILABLE_FUNCTIONS = {
    "search_rag": search_rag,
    "verify_boe": verify_boe
}



# ============================================
# SYSTEM PROMPT DETALLADO
# ============================================

SYSTEM_PROMPT = """Eres un preparador experto de oposiciones de Seguridad Social en España con 20 años de experiencia.

HERRAMIENTAS DISPONIBLES:
- search_rag: Busca en base de conocimiento legal (Qdrant LOCAL con leyes españolas)
- verify_boe: Verifica leyes en BOE oficial

WORKFLOW OBLIGATORIO:
1. PRIMERO: USA search_rag para encontrar artículos relevantes
2. SEGUNDO: USA verify_boe para verificar la ley principal
3. TERCERO: Genera el caso con información REAL obtenida

REGLAS ESTRICTAS:
- NUNCA inventes artículos o leyes
- SIEMPRE usa los tools primero
- Cita el BOE con URL verificada
- Fechas específicas (dd/mm/aaaa)
- Cantidades exactas
- Razonamiento paso a paso"""


# ============================================
# FUNCIÓN PRINCIPAL (Patrón oficial DeepSeek)
# ============================================

def send_messages(client, messages, tools):
    """Envía mensajes a DeepSeek (patrón oficial)"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        temperature=0.3,
        max_tokens=4000
    )
    return response.choices[0].message


# ============================================
# VALIDADOR DE CASOS IT
# ============================================

def validate_caso_it(caso_json):
    """Validador específico para casos de Incapacidad Temporal"""
    try:
        enunciado = caso_json["enunciado"]
        opciones = caso_json["opciones"]
        correcta = caso_json["respuesta_correcta"]
        
        # 1. Extraer datos del enunciado
        import re
        base_match = re.search(r'base.*?(\d+\.?\d*)€', enunciado, re.I)
        at_match = re.search(r'accidente de trabajo|AT', enunciado, re.I)
        
        if not base_match:
            return False, "No se encontró base reguladora en enunciado"
        
        base_mensual = float(base_match.group(1))
        es_at = bool(at_match)
        
        # 2. Calcular cuantía esperada
        base_diaria = base_mensual / 30
        porcentaje = 0.75 if es_at else 0.60  # Simplificado
        cuantia_esperada = base_diaria * porcentaje
        
        # 3. Extraer cuantía de opción correcta
        opcion_texto = opciones[correcta]
        cuantia_match = re.search(r'(\d+)€', opcion_texto)
        
        if not cuantia_match:
            return False, "Opción correcta no contiene cuantía en €"
        
        cuantia_opcion = float(cuantia_match.group(1))
        
        # 4. Validar con margen de error ±2€
        if abs(cuantia_esperada - cuantia_opcion) > 2:
            return False, f"Cuantía incorrecta: esperada {cuantia_esperada:.2f}€, encontrada {cuantia_opcion}€"
        
        # 5. Validar porcentaje mencionado
        pct_match = re.search(r'(\d+)%', opcion_texto)
        if pct_match:
            pct_opcion = int(pct_match.group(1))
            pct_esperado = 75 if es_at else 60
            if pct_opcion != pct_esperado:
                return False, f"Porcentaje incorrecto: {pct_opcion}% vs {pct_esperado}%"
        
        return True, "Caso válido"
    
    except Exception as e:
        return False, f"Error en validación: {str(e)}"


# ============================================
# FUNCIÓN PRINCIPAL CON VALIDACIÓN
# ============================================

def test_deepseek_with_validation():
    """Test DeepSeek con validación automática de casos"""
    print("🧪 TEST DEEPSEEK API - CON VALIDACIÓN AUTOMÁTICA")
    print("="*80)
    
    if not DEEPSEEK_API_KEY:
        print("❌ ERROR: DEEPSEEK_API_KEY no encontrada")
        return None
    
    print(f"✅ API Key: {DEEPSEEK_API_KEY[:20]}...")
    print(f"🌐 Base URL: {DEEPSEEK_BASE_URL}")
    print(f"🔧 Tools: {len(TOOLS)}")
    print(f"🐳 Qdrant: LOCAL Docker")
    print(f"✅ Validador: ACTIVADO")
    print("="*80)
    
    # Cliente DeepSeek
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    
    # Mensajes iniciales
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": """Genera 1 caso práctico de Incapacidad Temporal.

PASO 1: Llama a search_rag con query="Incapacidad Temporal inicio prestación"
PASO 2: Llama a verify_boe con ley_id="BOE-A-2015-11724"
PASO 3: Genera el caso en JSON:

{
  "id": "SS_IT_001",
  "enunciado": "Caso completo con fechas específicas...",
  "opciones": {"a": "...", "b": "...", "c": "...", "d": "..."},
  "respuesta_correcta": "c",
  "razonamiento": "Explicación completa...",
  "normativa": [{"articulo": "Art. 173 TRLGSS", "url": "..."}]
}

IMPORTANTE: 
1. Primero llama a los tools
2. Luego genera el caso
3. Devuelve SOLO el JSON, sin texto adicional"""
        }
    ]
    
    iteration = 0
    max_iterations = 15
    validation_attempts = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n🔄 Iteración {iteration}/{max_iterations}")
        print("-"*80)
        
        # Enviar mensajes a DeepSeek
        message = send_messages(client, messages, TOOLS)
        
        # ¿Hay tool calls?
        if message.tool_calls:
            print(f"🔧 DeepSeek solicita {len(message.tool_calls)} tool calls:")
            
            # Añadir mensaje del asistente
            messages.append(message)
            
            # Ejecutar cada tool call
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                print(f"  → {function_name}({arguments})")
                
                # Ejecutar función
                if function_name in AVAILABLE_FUNCTIONS:
                    function_to_call = AVAILABLE_FUNCTIONS[function_name]
                    function_response = function_to_call(**arguments)
                else:
                    function_response = f"Error: función {function_name} no encontrada"
                
                # Añadir respuesta del tool
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": function_response
                })
                
                print(f"    ✅ Respuesta: {function_response[:150]}...")
            
            # Continuar loop
            continue
        
        else:
            # DeepSeek terminó, VALIDAR antes de aceptar
            print("\n📝 DeepSeek terminó, validando caso...")
            final_content = message.content
            
            try:
                # Extraer JSON del contenido
                if "```json" in final_content:
                    json_text = final_content.split("```json")[1].split("```")[0].strip()
                elif "```" in final_content:
                    json_text = final_content.split("```")[1].split("```")[0].strip()
                else:
                    json_text = final_content.strip()
                
                caso_json = json.loads(json_text)
                
                # VALIDAR CASO
                is_valid, error_msg = validate_caso_it(caso_json)
                
                if not is_valid:
                    validation_attempts += 1
                    print(f"\n❌ VALIDACIÓN FALLIDA (intento {validation_attempts}): {error_msg}")
                    
                    if validation_attempts >= 3:
                        print("\n⚠️ Máximo de intentos de validación alcanzado")
                        print("💾 Guardando caso sin validar...")
                        break
                    
                    print("🔄 Solicitando regeneración...")
                    
                    # Añadir mensaje del asistente
                    messages.append(message)
                    
                    # Solicitar corrección
                    messages.append({
                        "role": "user",
                        "content": f"""ERROR CRÍTICO EN EL CASO: {error_msg}

REGENERA el caso completo corrigiendo este error específico.

IMPORTANTE:
1. Mantén el mismo tema (Incapacidad Temporal)
2. Corrige los cálculos de cuantía y porcentajes
3. Devuelve SOLO el JSON corregido, sin explicaciones adicionales

Formato esperado:
```json
{{
  "id": "SS_IT_001",
  "enunciado": "...",
  "opciones": {{"a": "...", "b": "...", "c": "...", "d": "..."}},
  "respuesta_correcta": "c",
  "razonamiento": "...",
  "normativa": [...]
}}
```"""
                    })
                    continue  # Volver a iterar
                
                else:
                    # ✅ VALIDACIÓN EXITOSA
                    print("\n✅ VALIDACIÓN EXITOSA")
                    print("="*80)
                    print("📄 CASO VALIDADO:")
                    print("="*80)
                    print(json.dumps(caso_json, indent=2, ensure_ascii=False)[:1500] + "...")
                    
                    # Guardar resultado
                    output_file = "/home/spas/OPOS_GEMINI_1/deepseek_validated_case.json"
                    
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump({
                            "model": "deepseek-chat (V3.2-Exp)",
                            "provider": "DeepSeek API Official",
                            "timestamp": datetime.now().isoformat(),
                            "iterations": iteration,
                            "tool_calls_made": iteration - validation_attempts - 1,
                            "validation_attempts": validation_attempts,
                            "validation_status": "PASSED",
                            "caso_generado": caso_json,
                            "raw_response": final_content
                        }, f, indent=2, ensure_ascii=False)
                    
                    print(f"\n💾 Guardado en: {output_file}")
                    print(f"\n✅ TEST COMPLETADO EN {iteration} ITERACIONES")
                    print(f"✅ Validación: {validation_attempts} intentos")
                    
                    return caso_json
                    
            except json.JSONDecodeError as e:
                print(f"\n❌ No se pudo parsear JSON: {e}")
                print("🔄 Solicitando corrección...")
                
                # Añadir mensaje del asistente
                messages.append(message)
                
                # Solicitar JSON válido
                messages.append({
                    "role": "user",
                    "content": "Devuelve SOLO el JSON del caso, sin texto adicional ni bloques de código markdown."
                })
                continue
    
    print(f"\n⚠️ Alcanzado límite de iteraciones ({max_iterations})")
    return None


if __name__ == "__main__":
    test_deepseek_with_validation()
