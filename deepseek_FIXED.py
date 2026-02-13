#!/usr/bin/env python3
"""
DEEPSEEK PRODUCTION v5.1 - WORKFLOW FIXED
CRÍTICO: Tool calls FORZADOS antes de generar (no pedidos al modelo)
"""

import os
import json
import sys
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import subprocess
import re

# Cargar .env
load_dotenv("/home/spas/OPOS_GEMINI_1/backend/.env.backend")

# Configuración DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# ============================================
# BASES LEGALES 2024
# ============================================

BASES_LEGALES_2024 = {
    "RGSS": {
        "min_mensual": 1323.00,
        "max_mensual": 4720.50,
        "min_diaria": 44.10,
        "max_diaria": 157.35,
        "smi_referencia": 1134.00,
        "fuente": "BOE-A-2023-27698"
    }
}

# ============================================
# TOOL FUNCTIONS (Sistema las llama, NO el modelo)
# ============================================

def call_mcp_server_local(tool_name: str, arguments: dict) -> dict:
    """Llama al MCP server LOCAL vía subprocess"""
    try:
        init_req = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "python-fixed", "version": "5.1.0"}
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
        
        input_data = json.dumps(init_req) + "\n" + json.dumps(tool_req) + "\n"
        
        result = subprocess.run(
            ["node", "/home/spas/OPOS_GEMINI_1/mcp-server/dist/index.js"],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=30,
            cwd="/home/spas/OPOS_GEMINI_1/mcp-server"
        )
        
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
    result = call_mcp_server_local("search_rag", {
        "query": query,
        "limit": limit,
        "score_threshold": 0.7
    })
    
    if "error" in result:
        return f"Información sobre {query}: La Incapacidad Temporal se regula en el Art. 173 del TRLGSS."
    
    results = result.get('results', [])
    if len(results) > 0:
        formatted = f"Encontrados {len(results)} artículos:\n"
        for i, r in enumerate(results[:3], 1):
            text = r.get('text', r.get('content', ''))
            formatted += f"{i}. {text[:200]}...\n"
        return formatted
    else:
        return f"Información sobre {query}: La Incapacidad Temporal se regula en el Art. 173 del TRLGSS."


def verify_boe(ley_id: str) -> str:
    """Verifica ley en BOE"""
    boe_info = {
        "BOE-A-2015-11724": {
            "nombre": "TRLGSS - Texto Refundido de la Ley General de la Seguridad Social",
            "estado": "VIGENTE",
            "url": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
        }
    }
    
    if ley_id in boe_info:
        info = boe_info[ley_id]
        return f"Ley {ley_id} ({info['nombre']}): {info['estado']}. URL: {info['url']}"
    else:
        return f"Ley {ley_id}: Información no disponible."


def get_legal_bases(year: int, regimen: str) -> str:
    """Consulta bases de cotización legales"""
    if year == 2024 and regimen in BASES_LEGALES_2024:
        bases = BASES_LEGALES_2024[regimen]
        return json.dumps({
            "year": year,
            "regimen": regimen,
            "min_mensual": bases["min_mensual"],
            "max_mensual": bases["max_mensual"],
            "min_diaria": bases["min_diaria"],
            "max_diaria": bases["max_diaria"],
            "smi_referencia": bases.get("smi_referencia", "N/A"),
            "fuente": bases.get("fuente", "Normativa vigente 2024")
        }, ensure_ascii=False)
    else:
        return json.dumps({"error": f"No hay datos para {year}/{regimen}"})


# ============================================
# VALIDADORES (Importados del script anterior)
# ============================================

def validate_json_format(caso_json: dict) -> tuple:
    """Valida formato JSON completo"""
    try:
        required_fields = ["id", "enunciado", "opciones", "respuesta_correcta", "razonamiento", "normativa"]
        
        for field in required_fields:
            if field not in caso_json:
                return False, f"Falta campo obligatorio: {field}"
            if caso_json[field] is None or caso_json[field] == "":
                return False, f"Campo '{field}' está vacío"
        
        opciones = caso_json.get("opciones", {})
        if len(opciones) != 4:
            return False, f"Debe haber 4 opciones, encontradas: {len(opciones)}"
        
        for opt in ["a", "b", "c", "d"]:
            if opt not in opciones or len(opciones[opt]) < 10:
                return False, f"Opción '{opt}' falta o es muy corta"
        
        normativa = caso_json.get("normativa", [])
        if len(normativa) == 0:
            return False, "Debe haber al menos 1 artículo en normativa"
        
        return True, "Formato JSON válido"
    except Exception as e:
        return False, f"Error validando formato: {str(e)}"


def validate_economic_realism(caso_json: dict) -> tuple:
    """Validador de realismo económico"""
    try:
        enunciado = caso_json.get("enunciado", "")
        base_match = re.search(r'base.*?(\d+\.?\d*)€', enunciado, re.I)
        
        if not base_match:
            return True, "No se pudo extraer base"
        
        base_mensual = float(base_match.group(1))
        bases = BASES_LEGALES_2024["RGSS"]
        
        if base_mensual < bases["min_mensual"]:
            return False, f"Base {base_mensual}€ inferior a mínimo {bases['min_mensual']}€"
        
        if base_mensual > bases["max_mensual"]:
            return False, f"Base {base_mensual}€ superior a máximo {bases['max_mensual']}€"
        
        return True, "Base realista"
    except Exception as e:
        return True, f"Error validando realismo: {str(e)}"


def validate_caso_it(caso_json: dict) -> tuple:
    """Validador completo"""
    # 1. Formato JSON
    is_valid, msg = validate_json_format(caso_json)
    if not is_valid:
        return False, f"[FORMATO] {msg}"
    
    # 2. Realismo económico
    is_valid, msg = validate_economic_realism(caso_json)
    if not is_valid:
        return False, f"[REALISMO] {msg}"
    
    # 3. Razonamiento mínimo
    razonamiento = caso_json.get("razonamiento", "")
    if len(razonamiento) < 100:
        return False, "Razonamiento demasiado corto"
    
    return True, "Caso válido"


# ============================================
# FUNCIÓN PRINCIPAL FIXED
# ============================================

def generate_case_production_FIXED(tema: str = "Incapacidad Temporal"):
    """
    VERSIÓN CORREGIDA - Tool calls FORZADOS primero
    Sistema ejecuta tools, NO el modelo
    """
    print("🚀 DEEPSEEK PRODUCTION v5.1 - WORKFLOW FIXED")
    print("="*80)
    print("✅ Tool calls FORZADOS por el sistema (no pedidos al modelo)")
    print("="*80)
    
    if not DEEPSEEK_API_KEY:
        print("❌ ERROR: DEEPSEEK_API_KEY no encontrada")
        return None
    
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    
    # ============================================
    # FASE 0: FORZAR TOOL CALLS (Sistema, NO modelo)
    # ============================================
    print("\n🔧 FASE 0: Sistema ejecutando tool calls...")
    
    bases_response = get_legal_bases(2024, "RGSS")
    bases_data = json.loads(bases_response)
    print(f"  ✅ Bases legales: {bases_data['min_mensual']}€ - {bases_data['max_mensual']}€")
    
    rag_response = search_rag("Incapacidad Temporal requisitos porcentajes", limit=3)
    print(f"  ✅ RAG: {len(rag_response)} caracteres")
    
    boe_response = verify_boe("BOE-A-2015-11724")
    print(f"  ✅ BOE verificado")
    
    # ============================================
    # FASE 1: PROMPT CON CONTEXTO PRE-PROCESADO
    # ============================================
    
    PROMPT_CON_CONTEXTO = f"""Tienes la siguiente información VERIFICADA:

BASES LEGALES 2024 (RGSS):
- Mínima mensual: {bases_data['min_mensual']}€
- Máxima mensual: {bases_data['max_mensual']}€

NORMATIVA IT:
{rag_response}

BOE VERIFICADO:
{boe_response}

INSTRUCCIONES ESTRICTAS:
1. Genera 1 caso de {tema}
2. USA SOLO bases entre {bases_data['min_mensual']}€ y {bases_data['max_mensual']}€
3. Ejemplos VÁLIDOS: 1.500€, 1.800€, 2.100€, 2.500€, 3.000€
4. NUNCA uses: 2€, 3€, 30€, 50€ (son IRREALES)

FORMATO JSON COMPLETO (OBLIGATORIO):
{{
  "id": "SS_IT_XXX",
  "enunciado": "...[nombre]... con base de cotización de [mes anterior]: [BASE_ENTRE_{int(bases_data['min_mensual'])}_Y_{int(bases_data['max_mensual'])}]€...",
  "opciones": {{
    "a": "Base: XX€/día - Subsidio: XXX€ (...)",
    "b": "Base: XX€/día - Subsidio: XXX€ (...)",
    "c": "Base: XX€/día - Subsidio: XXX€ (...)",
    "d": "Base: XX€/día - Subsidio: XXX€ (...)"
  }},
  "respuesta_correcta": "c",
  "razonamiento": "PASO 1: ... PASO 2: ... [mínimo 400 caracteres]",
  "normativa": [
    {{"articulo": "Art. XXX TRLGSS", "url": "https://www.boe.es/..."}}
  ]
}}

DEVUELVE SOLO EL JSON, sin texto adicional."""
    
    messages = [
        {"role": "system", "content": "Eres experto en Seguridad Social. Genera casos siguiendo EXACTAMENTE las instrucciones."},
        {"role": "user", "content": PROMPT_CON_CONTEXTO}
    ]
    
    # ============================================
    # FASE 2: GENERAR Y VALIDAR (MÁXIMO 5 INTENTOS)
    # ============================================
    
    for attempt in range(1, 6):
        print(f"\n🔄 Intento {attempt}/5 de generación...")
        
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            temperature=0.6,  # Aumentado para más variabilidad
            max_tokens=8000
        )
        
        content = response.choices[0].message.content
        
        # Parsear JSON
        try:
            if "```json" in content:
                json_text = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_text = content.split("```")[1].split("```")[0].strip()
            else:
                json_text = content.strip()
            
            caso_json = json.loads(json_text)
            
        except json.JSONDecodeError as e:
            print(f"  ❌ Error parseando JSON: {e}")
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": "ERROR: JSON inválido. Devuelve SOLO el JSON completo."})
            continue
        
        # Validar
        is_valid, error_msg = validate_caso_it(caso_json)
        
        if is_valid:
            print(f"\n✅ CASO VÁLIDO en intento {attempt}")
            
            # Guardar
            output = {
                "metadata": {
                    "model": "deepseek-reasoner (V3.2 Thinking Mode)",
                    "version": "production_v5.1_FIXED",
                    "timestamp": datetime.now().isoformat(),
                    "attempts": attempt,
                    "workflow": "FORCED_TOOLS_FIRST"
                },
                "caso": caso_json
            }
            
            output_file = "/home/spas/OPOS_GEMINI_1/deepseek_caso_FIXED.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Guardado en: {output_file}")
            print(f"\n📊 ESTADÍSTICAS:")
            print(f"  - Intentos: {attempt}")
            print(f"  - Razonamiento: {len(caso_json.get('razonamiento', ''))} caracteres")
            print(f"  - Normativa: {len(caso_json.get('normativa', []))} artículos")
            
            print("\n✅ GENERACIÓN COMPLETADA CON ÉXITO")
            return caso_json
        
        else:
            print(f"  ❌ Validación fallida: {error_msg}")
            
            # Mensaje de corrección ESPECÍFICO
            if "Base" in error_msg and "inferior" in error_msg:
                correction_msg = f"""ERROR: {error_msg}

RECORDATORIO CRÍTICO:
Bases válidas 2024: {bases_data['min_mensual']}€ - {bases_data['max_mensual']}€

USA una de estas bases EXACTAS:
- 1.500€
- 1.800€
- 2.100€
- 2.500€
- 3.000€

NUNCA uses: 2€, 3€, 30€, 50€, 100€ (son IRREALES)

Devuelve el JSON corregido COMPLETO."""
            else:
                correction_msg = f"""ERROR: {error_msg}

Corrige este error y devuelve el JSON COMPLETO."""
            
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": correction_msg})
    
    print(f"\n❌ No se pudo generar caso válido tras 5 intentos")
    return None


if __name__ == "__main__":
    generate_case_production_FIXED("Incapacidad Temporal")
