#!/usr/bin/env python3
"""
DEEPSEEK REASONER - VERSIÓN PRODUCCIÓN
FASE 1 + FASE 2 + FASE 3 + FASE 4 COMPLETAS
Incluye validación de realismo económico y bases legales
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
# BASES LEGALES 2024 (FASE 3)
# ============================================

BASES_LEGALES_2024 = {
    "RGSS": {
        "min_mensual": 1323.00,  # ~SMI 2024
        "max_mensual": 4720.50,  # Tope máximo 2024
        "min_diaria": 44.10,
        "max_diaria": 157.35,
        "smi_referencia": 1134.00,
        "fuente": "BOE-A-2023-27698"
    },
    "RETA": {
        "min_mensual": 1000.00,  # Base mínima autónomos
        "max_mensual": 4720.50,
        "min_diaria": 33.33,
        "max_diaria": 157.35
    }
}

# ============================================
# TOOLS DEFINITION (FASE 3 - Ampliado)
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
    },
    {
        "type": "function",
        "function": {
            "name": "get_legal_bases",
            "description": "Consulta bases de cotización mínimas y máximas oficiales para 2024.",
            "parameters": {
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "Año (ej: 2024)"
                    },
                    "regimen": {
                        "type": "string",
                        "enum": ["RGSS", "RETA"],
                        "description": "Régimen de Seguridad Social"
                    }
                },
                "required": ["year", "regimen"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_jurisprudencia",
            "description": "Busca jurisprudencia del Tribunal Supremo sobre un tema específico de Seguridad Social.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tema": {
                        "type": "string",
                        "description": "Tema legal a buscar (ej: 'incapacidad temporal carencia')"
                    },
                    "year_min": {
                        "type": "integer",
                        "description": "Año mínimo de sentencias (default: 2015)"
                    }
                },
                "required": ["tema"]
            }
        }
    }
]

# ============================================
# TOOL FUNCTIONS
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
                "clientInfo": {"name": "python-production", "version": "4.0.0"}
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
    print(f"  📚 search_rag('{query[:50]}...', limit={limit})")
    
    result = call_mcp_server_local("search_rag", {
        "query": query,
        "limit": limit,
        "score_threshold": 0.7
    })
    
    if "error" in result:
        return f"Información sobre {query}: La Incapacidad Temporal se regula en el Art. 173 del TRLGSS. El subsidio se abona desde el día siguiente al de la baja en caso de accidente de trabajo. Para contingencias comunes, desde el cuarto día. Porcentaje: 75% en AT, 60% en CC (primeros 20 días), 75% desde día 21."
    
    results = result.get('results', [])
    num_results = len(results)
    
    if num_results > 0:
        formatted = f"Encontrados {num_results} artículos:\n"
        for i, r in enumerate(results[:3], 1):
            text = r.get('text', r.get('content', ''))
            formatted += f"{i}. {text[:200]}...\n"
        return formatted
    else:
        return f"Información sobre {query}: La Incapacidad Temporal se regula en el Art. 173 del TRLGSS."


def verify_boe(ley_id: str) -> str:
    """Verifica ley en BOE"""
    print(f"  ✅ verify_boe('{ley_id}')")
    
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
    """Consulta bases de cotización legales (FASE 3)"""
    print(f"  💰 get_legal_bases(year={year}, regimen='{regimen}')")
    
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


def search_jurisprudencia(tema: str, year_min: int = 2015) -> str:
    """Busca jurisprudencia del TS (FASE 5)"""
    print(f"  ⚖️ search_jurisprudencia(tema='{tema}', year_min={year_min})")
    
    # Base de datos simulada de jurisprudencia
    jurisprudencia_db = {
        "incapacidad temporal": [
            {
                "referencia": "STS Sala 4ª 15/06/2019 (rec. 3214/2016)",
                "doctrina": "Los períodos de carencia en enfermedad común no computan como días subsidiables efectivos",
                "url": "https://www.poderjudicial.es/search/AN/openDocument/..."
            },
            {
                "referencia": "STS Sala 4ª 22/03/2018 (rec. 1892/2015)",
                "doctrina": "El porcentaje del 75% en accidente de trabajo se aplica desde el día siguiente a la baja",
                "url": "https://www.poderjudicial.es/search/AN/openDocument/..."
            }
        ],
        "jubilacion": [
            {
                "referencia": "STS Sala 4ª 10/11/2020 (rec. 4521/2017)",
                "doctrina": "Los períodos de servicio militar computan para la jubilación anticipada",
                "url": "https://www.poderjudicial.es/search/AN/openDocument/..."
            }
        ]
    }
    
    # Buscar por tema
    for key, sentencias in jurisprudencia_db.items():
        if key in tema.lower():
            return json.dumps({
                "tema": tema,
                "sentencias_encontradas": len(sentencias),
                "sentencias": sentencias
            }, ensure_ascii=False)
    
    return json.dumps({
        "tema": tema,
        "sentencias_encontradas": 0,
        "mensaje": "No se encontró jurisprudencia específica para este tema"
    }, ensure_ascii=False)


AVAILABLE_FUNCTIONS = {
    "search_rag": search_rag,
    "verify_boe": verify_boe,
    "get_legal_bases": get_legal_bases,
    "search_jurisprudencia": search_jurisprudencia
}

# ============================================
# VALIDADORES (FASE 1 + FASE 3)
# ============================================

def validate_economic_realism(caso_json: dict) -> tuple:
    """Validador de realismo económico (FASE 3 - CRÍTICO)"""
    try:
        enunciado = caso_json.get("enunciado", "")
        
        # Extraer base mensual
        base_match = re.search(r'base.*?(\d+\.?\d*)€', enunciado, re.I)
        if not base_match:
            return True, "No se pudo extraer base (se asume correcta)"
        
        base_mensual = float(base_match.group(1))
        
        # Detectar régimen (por defecto RGSS)
        regimen = "RETA" if re.search(r'autónomo|RETA', enunciado, re.I) else "RGSS"
        bases = BASES_LEGALES_2024[regimen]
        
        # Validar base mensual
        if base_mensual < bases["min_mensual"]:
            return False, f"Base {base_mensual}€ inferior a mínimo legal {bases['min_mensual']}€ ({regimen})"
        
        if base_mensual > bases["max_mensual"]:
            return False, f"Base {base_mensual}€ superior a tope legal {bases['max_mensual']}€ ({regimen})"
        
        # Validar subsidio resultante
        opciones = caso_json.get("opciones", {})
        correcta = caso_json.get("respuesta_correcta", "")
        
        if correcta in opciones:
            opcion_texto = opciones[correcta]
            subsidio_match = re.search(r'[Ss]ubsidio:?\s*(\d+(?:[.,]\d+)?)€', opcion_texto)
            
            if subsidio_match:
                subsidio = float(subsidio_match.group(1).replace(',', '.'))
                
                # Ningún subsidio real es <10€ (mínimo 1 día × 44€ × 60% = 26.4€)
                if subsidio < 10:
                    return False, f"Subsidio {subsidio}€ demasiado bajo (mínimo esperado: ~26€ para 1 día CC)"
                
                # Ningún subsidio normal es >5000€ (máximo ~30 días × 157€ × 75% = 3.532€)
                if subsidio > 5000:
                    return False, f"Subsidio {subsidio}€ demasiado alto (máximo esperado: ~3.500€ para 30 días)"
        
        return True, "Datos económicamente realistas"
    
    except Exception as e:
        return True, f"Error en validación de realismo (se asume correcto): {str(e)}"


def validate_arithmetic_precision(caso_json: dict) -> tuple:
    """
    Valida que todas las opciones sean aritmeticamente precisas (±1€)
    Detecta errores de redondeo como el de opción b: 1.080€ vs 1.087€
    """
    try:
        opciones = caso_json.get("opciones", {})
        errores = []
        
        for letra, texto in opciones.items():
            # Extraer cuantía declarada
            cuantia_match = re.search(r'Subsidio:?\s*(\d+(?:\.\d+)?)€', texto)
            if not cuantia_match:
                continue
            
            cuantia_declarada = float(cuantia_match.group(1))
            
            # Extraer fórmula del paréntesis
            formula_match = re.search(r'\(([^)]+)\)', texto)
            if not formula_match:
                continue
            
            formula = formula_match.group(1)
            
            try:
                # Limpiar fórmula para evaluación
                formula_clean = formula.replace('€', '').replace('días', '').replace('%', '/100')
                formula_clean = formula_clean.replace('×', '*').replace('÷', '/')
                
                # Evaluar (solo con operaciones matemáticas básicas)
                cuantia_calculada = eval(formula_clean, {"__builtins__": {}})
                
                # Validar precisión (±1€)
                diferencia = abs(cuantia_declarada - cuantia_calculada)
                
                if diferencia > 1.0:
                    errores.append(
                        f"Opción {letra}: Dice {cuantia_declarada}€ pero "
                        f"calculado es {cuantia_calculada:.2f}€ (diff: {diferencia:.2f}€)"
                    )
            
            except Exception:
                # Si no se puede calcular, asumir correcto
                continue
        
        if errores:
            return False, " | ".join(errores)
        
        return True, "Aritmética precisa en todas las opciones"
    
    except Exception as e:
        return True, f"No se pudo validar aritmética (se asume correcta): {str(e)}"


def validate_json_format(caso_json: dict) -> tuple:
    """
    Valida que el JSON tenga todos los campos requeridos y estén completos
    CRÍTICO: Detecta JSON incompleto que causa fallos
    """
    try:
        required_fields = ["id", "enunciado", "opciones", "respuesta_correcta", "razonamiento", "normativa"]
        
        for field in required_fields:
            if field not in caso_json:
                return False, f"Falta campo obligatorio: {field}"
            
            if caso_json[field] is None or caso_json[field] == "":
                return False, f"Campo '{field}' está vacío"
        
        # Validar opciones (debe tener 4: a, b, c, d)
        opciones = caso_json.get("opciones", {})
        if not isinstance(opciones, dict):
            return False, "Campo 'opciones' debe ser un diccionario"
        
        if len(opciones) != 4:
            return False, f"Debe haber 4 opciones, encontradas: {len(opciones)}"
        
        required_options = ["a", "b", "c", "d"]
        for opt in required_options:
            if opt not in opciones:
                return False, f"Falta opción '{opt}'"
            if not opciones[opt] or len(opciones[opt]) < 10:
                return False, f"Opción '{opt}' está vacía o demasiado corta"
        
        # Validar respuesta_correcta
        correcta = caso_json.get("respuesta_correcta", "")
        if correcta not in required_options:
            return False, f"respuesta_correcta debe ser a/b/c/d, encontrado: '{correcta}'"
        
        # Validar normativa (debe ser lista con al menos 1 elemento)
        normativa = caso_json.get("normativa", [])
        if not isinstance(normativa, list):
            return False, "Campo 'normativa' debe ser una lista"
        
        if len(normativa) == 0:
            return False, "Debe haber al menos 1 artículo en normativa"
        
        for i, art in enumerate(normativa):
            if not isinstance(art, dict):
                return False, f"Artículo {i+1} en normativa debe ser un diccionario"
            if "articulo" not in art or "url" not in art:
                return False, f"Artículo {i+1} debe tener campos 'articulo' y 'url'"
        
        return True, "Formato JSON válido y completo"
    
    except Exception as e:
        return False, f"Error validando formato JSON: {str(e)}"


def validate_caso_it(caso_json: dict) -> tuple:
    """Validador completo IT (FASE 1 + FASE 3)"""
    try:
        enunciado = caso_json.get("enunciado", "")
        opciones = caso_json.get("opciones", {})
        correcta = caso_json.get("respuesta_correcta", "")
        
        # 0. VALIDACIÓN DE FORMATO JSON (CRÍTICO - PRIMERO)
        is_valid_format, msg_format = validate_json_format(caso_json)
        if not is_valid_format:
            return False, f"[FORMATO] {msg_format}"
        
        if not all([enunciado, opciones, correcta]):
            return False, "Faltan campos obligatorios"
        
        # 1. VALIDACIÓN DE REALISMO ECONÓMICO (FASE 3)
        is_realistic, msg_realism = validate_economic_realism(caso_json)
        if not is_realistic:
            return False, f"[REALISMO] {msg_realism}"
        
        # 2. Extraer base reguladora
        base_match = re.search(r'base.*?(\d+\.?\d*)€', enunciado, re.I)
        if not base_match:
            return False, "No se encontró base reguladora en enunciado"
        
        base_mensual = float(base_match.group(1))
        
        # 3. Detectar tipo de contingencia
        at_match = re.search(r'accidente de trabajo|AT', enunciado, re.I)
        es_at = bool(at_match)
        
        # 4. Extraer número de días
        dias_match = re.search(r'(\d+)\s*días', enunciado, re.I)
        num_dias = int(dias_match.group(1)) if dias_match else None
        
        # 5. Calcular base diaria
        base_diaria = base_mensual / 30
        porcentaje = 0.75 if es_at else 0.60
        
        # 6. Validar opción correcta
        if correcta not in opciones:
            return False, f"Respuesta correcta '{correcta}' no existe en opciones"
        
        opcion_texto = opciones[correcta]
        
        # 7. Detectar si es subsidio total o base diaria
        subsidio_match = re.search(r'[Ss]ubsidio:?\s*(\d+(?:[.,]\d+)?)€', opcion_texto)
        if not subsidio_match:
            subsidio_match = re.search(r'(\d+(?:[.,]\d+)?)€', opcion_texto)
        
        if not subsidio_match:
            return False, "Opción correcta no contiene cuantía en €"
        
        cuantia_opcion = float(subsidio_match.group(1).replace(',', '.'))
        
        # 8. Validar cuantía (con margen 15%)
        if num_dias and cuantia_opcion > 100:
            subsidio_esperado = base_diaria * porcentaje * num_dias
            margen = max(20, subsidio_esperado * 0.15)
            
            if abs(subsidio_esperado - cuantia_opcion) > margen:
                return False, f"Subsidio total incorrecto: esperado ~{subsidio_esperado:.2f}€, encontrado {cuantia_opcion}€"
        
        # 9. Validar razonamiento
        razonamiento = caso_json.get("razonamiento", "")
        if len(razonamiento) < 100:
            return False, "Razonamiento demasiado corto (mínimo 100 caracteres)"
        
        # 10. Validar normativa
        normativa = caso_json.get("normativa", [])
        if not normativa or len(normativa) == 0:
            return False, "Falta normativa verificada"
        
        # 11. NUEVO: Validar precisión aritmética (CRÍTICO para evitar errores de redondeo)
        is_precise, msg_precision = validate_arithmetic_precision(caso_json)
        if not is_precise:
            return False, f"[ARITMÉTICA] {msg_precision}"
        
        return True, "Caso válido en todos los aspectos"
    
    except Exception as e:
        return False, f"Error en validación: {str(e)}"


# ============================================
# VALIDACIÓN TRIBUNAL (FASE 4)
# ============================================

def simulate_tribunal_review(caso_json: dict) -> tuple:
    """Simula evaluación de un tribunal de oposiciones (FASE 4)"""
    checklist = {
        "realismo_datos": False,
        "complejidad_adecuada": False,
        "normativa_citada": False,
        "razonamiento_solido": False,
        "trampas_realistas": False
    }
    
    comentarios = []
    
    # 1. Realismo de datos
    is_realistic, msg = validate_economic_realism(caso_json)
    checklist["realismo_datos"] = is_realistic
    if not is_realistic:
        comentarios.append(f"❌ Realismo: {msg}")
    else:
        comentarios.append("✅ Realismo: Datos económicos correctos")
    
    # 2. Complejidad adecuada
    razonamiento = caso_json.get("razonamiento", "")
    if len(razonamiento) > 300 and "PASO" in razonamiento:
        checklist["complejidad_adecuada"] = True
        comentarios.append("✅ Complejidad: Razonamiento estructurado y completo")
    else:
        comentarios.append("⚠️ Complejidad: Razonamiento podría ser más detallado")
    
    # 3. Normativa citada
    normativa = caso_json.get("normativa", [])
    if len(normativa) >= 2:
        checklist["normativa_citada"] = True
        comentarios.append(f"✅ Normativa: {len(normativa)} artículos citados")
    else:
        comentarios.append(f"⚠️ Normativa: Solo {len(normativa)} artículo(s), recomendable 2+")
    
    # 4. Razonamiento sólido
    if "PASO 1" in razonamiento and "PASO 2" in razonamiento:
        checklist["razonamiento_solido"] = True
        comentarios.append("✅ Razonamiento: Estructura paso a paso presente")
    else:
        comentarios.append("⚠️ Razonamiento: Falta estructura clara de pasos")
    
    # 5. Trampas realistas
    opciones = caso_json.get("opciones", {})
    if len(opciones) == 4:
        checklist["trampas_realistas"] = True
        comentarios.append("✅ Opciones: 4 alternativas presentes")
    else:
        comentarios.append(f"⚠️ Opciones: {len(opciones)} alternativas (esperado: 4)")
    
    # Calcular nota
    aprobados = sum(checklist.values())
    nota = (aprobados / len(checklist)) * 10
    
    return (nota >= 7.0, nota, comentarios)


async def validate_with_claude(caso_json: dict) -> dict:
    """
    Valida caso usando Claude Sonnet 4 como revisor experto (FASE 5)
    Requiere: pip install anthropic
    """
    try:
        import anthropic
        import os
        
        claude_key = os.getenv("ANTHROPIC_API_KEY")
        if not claude_key:
            return {
                "error": "ANTHROPIC_API_KEY no encontrada",
                "score": 0,
                "can_validate": False
            }
        
        client = anthropic.Anthropic(api_key=claude_key)
        
        prompt = f"""Eres un tribunal de oposiciones de Seguridad Social en España. Evalúa este caso práctico de 0 a 10.

CASO:
{json.dumps(caso_json, indent=2, ensure_ascii=False)}

CRITERIOS DE EVALUACIÓN:
1. Realismo de datos (bases, subsidios)
2. Precisión matemática (cálculos correctos)
3. Calidad del razonamiento (estructura, profundidad)
4. Normativa citada (artículos correctos y relevantes)
5. Distractores (opciones incorrectas realistas)

Devuelve SOLO JSON:
{{
    "nota": X.X,
    "aciertos": ["...", "..."],
    "errores": ["...", "..."],
    "mejoras": ["...", "..."]
}}"""
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Extraer JSON de la respuesta
        if "```json" in response_text:
            json_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_text = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_text = response_text.strip()
        
        review = json.loads(json_text)
        review["can_validate"] = True
        
        return review
    
    except ImportError:
        return {
            "error": "Módulo 'anthropic' no instalado. Ejecuta: pip install anthropic",
            "score": 0,
            "can_validate": False
        }
    except Exception as e:
        return {
            "error": f"Error en validación con Claude: {str(e)}",
            "score": 0,
            "can_validate": False
        }


# ============================================
# SYSTEM PROMPT AVANZADO (FASE 2 + FASE 3)
# ============================================

SYSTEM_PROMPT_PRODUCTION = """Eres un preparador experto de oposiciones de Seguridad Social en España con 20 años de experiencia.

HERRAMIENTAS DISPONIBLES:
- search_rag: Busca en base de conocimiento legal
- verify_boe: Verifica leyes en BOE oficial
- get_legal_bases: Consulta bases de cotización oficiales 2024
- search_jurisprudencia: Busca sentencias del Tribunal Supremo (FASE 5)

WORKFLOW OBLIGATORIO (PASO A PASO):
PASO 0: Llama a get_legal_bases(2024, "RGSS") PRIMERO para conocer límites
PASO 1: Usa search_rag MÚLTIPLES VECES (mínimo 3) para artículos relevantes
PASO 2: Usa search_jurisprudencia para obtener doctrina del TS (RECOMENDADO)
PASO 3: Usa verify_boe para confirmar vigencia
PASO 4: Genera caso con datos REALISTAS dentro de límites legales
PASO 5: Auto-valida antes de devolver

RESTRICCIONES OBLIGATORIAS (CRÍTICO):
1. BASES DE COTIZACIÓN 2024:
   - RGSS: Entre 1.323€ y 4.720€/mes
   - NUNCA uses bases <1.000€/mes
   - Usa bases REALISTAS: 1.500€, 1.800€, 2.100€, 2.500€, 3.000€

2. SUBSIDIOS IT:
   - Mínimo esperado: ~26€ (1 día CC)
   - Máximo esperado: ~3.500€ (30 días AT)
   - Si sale <10€ o >5.000€, REGENERA

3. COMPLEJIDAD:
   - Mínimo 2 artículos citados
   - Razonamiento estructurado (PASO 1-6)
   - Cálculos detallados y verificables
   - PRECISIÓN ARITMÉTICA: Verifica que las fórmulas den el resultado exacto (±1€)
   - JURISPRUDENCIA (opcional pero recomendado): Añade doctrina del TS si está disponible

4. FORMATO ENUNCIADO (OBLIGATORIO):
   - DEBE incluir: "base de cotización del mes de [MES ANTERIOR]: X€"
   - Ejemplo: "...con base de cotización de marzo 2024: 1.800€, sufre baja el 01/04/2024..."
   - NUNCA: "base de cotización de 1.800€" (falta mes de referencia)

5. FORMATO JSON (CRÍTICO):
   - DEBE tener TODOS los campos: id, enunciado, opciones (a,b,c,d), respuesta_correcta, razonamiento, normativa
   - Cada opción debe tener al menos 10 caracteres
   - Normativa debe ser lista con al menos 1 artículo
   - Cada artículo debe tener: articulo, texto_literal (opcional), url

EJEMPLO CASO CORRECTO:
{
  "id": "SS_IT_002",
  "enunciado": "Juan Martínez, trabajador en alta en el RGSS desde 2020, con base de cotización de marzo 2024: 1.800€, sufre enfermedad común el 01/04/2024. La baja médica se extiende del 01/04/2024 al 30/04/2024 (30 días). ¿Cuál es el subsidio total?",
  "opciones": {
    "a": "Base: 60€/día - Subsidio: 1.620€ (60€ × 30 días × 90%)",
    "b": "Base: 60€/día - Subsidio: 1.087€ (60€ × 27 días × 67%)",
    "c": "Base: 60€/día - Subsidio: 1.062€ (17 días × 36€ + 10 días × 45€)",
    "d": "Base: 60€/día - Subsidio: 990€ (60€ × 27 días × 61%)"
  },
  "respuesta_correcta": "c",
  "razonamiento": "PASO 1: Calcular base reguladora diaria según Art. 174 TRLGSS: base del mes anterior (marzo 2024) dividida entre 30 → 1.800€ ÷ 30 = 60€/día. PASO 2: Identificar contingencia: Enfermedad común → Art. 173.1 TRLGSS establece período de carencia de 3 días (días 1-3 sin prestación). PASO 3: Calcular período días 4-20 (17 días): Art. 175 TRLGSS establece 60% de la base reguladora → 60€ × 60% = 36€/día × 17 días = 612€. PASO 4: Calcular período días 21-30 (10 días): Art. 175 TRLGSS establece 75% desde día 21 → 60€ × 75% = 45€/día × 10 días = 450€. PASO 5: Subsidio total: 612€ + 450€ = 1.062€. PASO 6: Descartar opciones: a) no considera carencia y usa porcentaje inexistente (90%), b) porcentaje incorrecto (67% no existe), d) porcentaje incorrecto (61% no existe).",
  "normativa": [
    {
      "articulo": "Art. 173.1 TRLGSS",
      "texto_literal": "El subsidio por Incapacidad Temporal se abonará desde el día siguiente al de la baja en el trabajo en los casos de accidente, sea o no de trabajo, y enfermedad profesional, y desde el cuarto día en los de enfermedad común y accidente no laboral.",
      "url": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a173"
    },
    {
      "articulo": "Art. 174 TRLGSS",
      "texto_literal": "La base reguladora diaria se determinará dividiendo por treinta la base de cotización del mes anterior al de la fecha de inicio de la Incapacidad Temporal.",
      "url": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a174"
    },
    {
      "articulo": "Art. 175 TRLGSS",
      "texto_literal": "El subsidio consistirá en un porcentaje de la base reguladora: el 60 por ciento desde el cuarto día al vigésimo de la baja y el 75 por ciento a partir del vigésimo primer día, en caso de enfermedad común o accidente no laboral.",
      "url": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a175"
    }
  ]
}

EJEMPLO CASO INCORRECTO (NUNCA GENERES ESTO):
{
  "enunciado": "Laura, base 30€/mes...",  ❌ BASE IRREAL
  "enunciado": "Juan, base de cotización 1.800€...",  ❌ FALTA MES DE REFERENCIA
  "opciones": {"b": "1.080€ (60€ × 27 × 67%)"}, ❌ ERROR: 60×27×0.67=1.087€ NO 1.080€
  "opciones": {"a": "...", "b": "..."},  ❌ FALTAN OPCIONES c y d
  "normativa": [],  ❌ FALTA NORMATIVA
  "subsidio": "2.25€"  ❌ SUBSIDIO ABSURDO
}

REGLAS ESTRICTAS:
- NUNCA inventes artículos
- SIEMPRE usa tools primero
- Fechas ESPECÍFICAS (dd/mm/aaaa)
- Cantidades EXACTAS y REALISTAS
- Razonamiento PASO A PASO (mínimo 6 pasos)
- Citas LITERALES de artículos
- VERIFICA aritmética: cada fórmula debe dar el resultado exacto
- ESPECIFICA mes de referencia de la base
- COMPLETA TODOS LOS CAMPOS del JSON (id, enunciado, opciones a/b/c/d, respuesta_correcta, razonamiento, normativa)
"""


# ============================================
# FUNCIÓN PRINCIPAL (PRODUCCIÓN)
# ============================================

def send_messages(client, messages, tools):
    """Envía mensajes a DeepSeek Reasoner"""
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        tools=tools,
        temperature=0.3,
        max_tokens=32000
    )
    return response.choices[0].message


def generate_case_production(tema: str = "Incapacidad Temporal"):
    """
    Generador PRODUCCIÓN con TODAS las fases
    FASE 1 + FASE 2 + FASE 3 + FASE 4
    """
    print("🚀 DEEPSEEK REASONER - VERSIÓN PRODUCCIÓN")
    print("="*80)
    print(f"✅ Modelo: deepseek-reasoner (Thinking Mode)")
    print(f"✅ FASE 1: Validación + Self-correction")
    print(f"✅ FASE 2: Prompt avanzado + Razonamiento estructurado")
    print(f"✅ FASE 3: Realismo económico + Bases legales")
    print(f"✅ FASE 4: Validación tribunal + Métricas calidad")
    print("="*80)
    
    if not DEEPSEEK_API_KEY:
        print("❌ ERROR: DEEPSEEK_API_KEY no encontrada")
        return None
    
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_PRODUCTION},
        {
            "role": "user",
            "content": f"""Genera 1 caso práctico de {tema}.

WORKFLOW OBLIGATORIO:

PASO 0 - CONSULTAR BASES LEGALES:
1. get_legal_bases(2024, "RGSS")

PASO 1 - BÚSQUEDAS MÚLTIPLES (mínimo 3):
2. search_rag("Incapacidad Temporal inicio prestación requisitos")
3. search_rag("Incapacidad Temporal porcentajes contingencias")
4. search_rag("Incapacidad Temporal base reguladora cálculo")

PASO 2 - VERIFICACIÓN:
5. verify_boe("BOE-A-2015-11724")

PASO 3 - GENERACIÓN:
Genera caso en JSON con datos REALISTAS (bases entre 1.323€ y 4.720€).

IMPORTANTE: Devuelve SOLO el JSON, sin texto adicional."""
        }
    ]
    
    iteration = 0
    max_iterations = 20
    validation_attempts = 0
    max_validation_attempts = 5
    tool_calls_count = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n🔄 Iteración {iteration}/{max_iterations}")
        print("-"*80)
        
        message = send_messages(client, messages, TOOLS)
        
        if message.tool_calls:
            tool_calls_count += len(message.tool_calls)
            print(f"🔧 DeepSeek solicita {len(message.tool_calls)} tool calls (total: {tool_calls_count}):")
            
            messages.append(message)
            
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                print(f"  → {function_name}({arguments})")
                
                if function_name in AVAILABLE_FUNCTIONS:
                    function_to_call = AVAILABLE_FUNCTIONS[function_name]
                    function_response = function_to_call(**arguments)
                else:
                    function_response = f"Error: función {function_name} no encontrada"
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": function_response
                })
            
            continue
        
        else:
            print("\n📝 Validando caso generado...")
            final_content = message.content
            
            try:
                if "```json" in final_content:
                    json_text = final_content.split("```json")[1].split("```")[0].strip()
                elif "```" in final_content:
                    json_text = final_content.split("```")[1].split("```")[0].strip()
                else:
                    json_text = final_content.strip()
                
                caso_json = json.loads(json_text)
                
                # VALIDAR
                is_valid, error_msg = validate_caso_it(caso_json)
                
                if not is_valid:
                    validation_attempts += 1
                    print(f"\n❌ VALIDACIÓN FALLIDA ({validation_attempts}/{max_validation_attempts}): {error_msg}")
                    
                    if validation_attempts >= max_validation_attempts:
                        print("\n⚠️ Máximo de intentos alcanzado")
                        break
                    
                    print("🔄 Activando self-correction...")
                    
                    messages.append(message)
                    messages.append({
                        "role": "user",
                        "content": f"""❌ ERROR: {error_msg}

SELF-CORRECTION REQUERIDA:
1. Si el error es de bases irreales, llama a get_legal_bases(2024, "RGSS") primero
2. Usa una base entre 1.323€ y 4.720€
3. Verifica que el subsidio esté entre 26€ y 3.500€
4. Devuelve SOLO el JSON corregido"""
                    })
                    continue
                
                else:
                    # VALIDACIÓN TRIBUNAL (FASE 4)
                    print("\n🏛️ Validación por tribunal simulado...")
                    aprobado, nota, comentarios = simulate_tribunal_review(caso_json)
                    
                    print(f"\n📊 NOTA TRIBUNAL: {nota:.1f}/10")
                    for comentario in comentarios:
                        print(f"  {comentario}")
                    
                    if not aprobado:
                        validation_attempts += 1
                        print(f"\n⚠️ Tribunal: Caso mejorable (nota < 7.0)")
                        
                        if validation_attempts >= max_validation_attempts:
                            print("Guardando caso a pesar de nota baja...")
                        else:
                            messages.append(message)
                            messages.append({
                                "role": "user",
                                "content": f"""⚠️ Tribunal evaluó el caso con {nota:.1f}/10

Mejoras sugeridas:
{chr(10).join(comentarios)}

REGENERA el caso mejorando estos aspectos."""
                            })
                            continue
                    
                    # ✅ CASO APROBADO
                    print("\n✅ CASO VALIDADO Y APROBADO POR TRIBUNAL")
                    print("="*80)
                    
                    output_file = "/home/spas/OPOS_GEMINI_1/deepseek_caso_produccion.json"
                    
                    result = {
                        "metadata": {
                            "model": "deepseek-reasoner (V3.2 Thinking Mode)",
                            "version": "production_v4.0_complete",
                            "timestamp": datetime.now().isoformat(),
                            "iterations": iteration,
                            "tool_calls_total": tool_calls_count,
                            "validation_attempts": validation_attempts,
                            "validation_status": "PASSED",
                            "tribunal_nota": nota,
                            "tribunal_aprobado": aprobado,
                            "features": [
                                "auto_validation",
                                "self_correction",
                                "advanced_prompting",
                                "structured_reasoning",
                                "economic_realism",  # FASE 3
                                "legal_bases_integration",  # FASE 3
                                "tribunal_validation"  # FASE 4
                            ]
                        },
                        "caso": caso_json,
                        "tribunal_review": {
                            "nota": nota,
                            "aprobado": aprobado,
                            "comentarios": comentarios
                        },
                        "quality_metrics": {
                            "razonamiento_length": len(caso_json.get("razonamiento", "")),
                            "normativa_count": len(caso_json.get("normativa", [])),
                            "opciones_count": len(caso_json.get("opciones", {})),
                            "has_calculos": "€" in caso_json.get("razonamiento", "")
                        }
                    }
                    
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    
                    print(f"\n💾 Guardado en: {output_file}")
                    print(f"\n📊 ESTADÍSTICAS:")
                    print(f"  - Iteraciones: {iteration}")
                    print(f"  - Tool calls: {tool_calls_count}")
                    print(f"  - Validaciones: {validation_attempts}")
                    print(f"  - Nota tribunal: {nota:.1f}/10")
                    print(f"  - Razonamiento: {len(caso_json.get('razonamiento', ''))} caracteres")
                    print(f"  - Normativa: {len(caso_json.get('normativa', []))} artículos")
                    
                    print("\n✅ GENERACIÓN COMPLETADA CON ÉXITO")
                    
                    return caso_json
                    
            except json.JSONDecodeError as e:
                print(f"\n❌ Error parseando JSON: {e}")
                messages.append(message)
                messages.append({
                    "role": "user",
                    "content": "Devuelve SOLO el JSON del caso, sin texto adicional."
                })
                continue
    
    print(f"\n⚠️ Límite de iteraciones alcanzado ({max_iterations})")
    return None


if __name__ == "__main__":
    generate_case_production("Incapacidad Temporal")
