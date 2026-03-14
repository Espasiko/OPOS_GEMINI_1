#!/usr/bin/env python3
import os
import sys
import json
import asyncio
import re
import httpx
from dotenv import load_dotenv

# Añadir directorios necesarios al path
root_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, root_dir)
sys.path.insert(0, os.path.join(root_dir, "backend"))

from agents.rag_helper import get_rag_helper
from calculators.dispatcher import CasosPracticosDispatcher
from json_repair import repair_json

load_dotenv(os.path.join(root_dir, ".env"))

# Inicializar cliente HTTP (httpx) apuntando a Mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    print("❌ ERROR: MISTRAL_API_KEY no encontrada en .env")
    sys.exit(1)

# URLs y cabeceras
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
MODEL_NAME = "mistral-large-latest"

# ---------------------------------------------------------
# DEFINICIÓN DE HERRAMIENTAS MISTRAL
# ---------------------------------------------------------
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_rag",
            "description": "Busca legislación vigente en el RAG de Seguridad Social y AGE. Úsala para encontrar los artículos exactos y requisitos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Término legal o artículo a buscar (ej. 'jubilación anticipada involuntaria requisitos')"},
                    "limit": {"type": "integer", "description": "Número de resultados", "default": 5}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ejecutar_calculo",
            "description": "Calculadora legal python que ejecuta cálculos exactos de Seguridad Social (it, jubilación, imv) y AGE.",
            "parameters": {
                "type": "object",
                "properties": {
                    "consulta": {"type": "string", "description": "Ej. 'Cálculo IT contingencia común BR 2000'"}
                },
                "required": ["consulta"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "verify_boe",
            "description": "Verifica vigencia de una ley directa en el BOE oficial.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ley_id": {"type": "string", "description": "ID del BOE (ej. BOE-A-2015-11724)"},
                    "fecha_examen": {"type": "string", "description": "Fecha de vigencia a verificar (YYYY-MM-DD)"}
                },
                "required": ["ley_id"]
            }
        }
    }
]

# ---------------------------------------------------------
# PROMPTS DEL SISTEMA (V12)
# ---------------------------------------------------------

SYSTEM_INVESTIGATOR = """Eres el Agente Investigador (El Perito).
Tu única función es extraer datos crudos, matemáticos, artículos vigentes y porcentajes inmutables sobre la temática solicitada.
Usa obligatoriamente tus herramientas (search_rag, ejecutar_calculo) repetidas veces hasta estar seguro de obtener la LEY EXACTA Y VIGENTE. 
NO redactas historias ni casos prácticos. Debes devolver un bloque estructurado con los HECHOS LEGALES EXACTOS que el Redactor usará."""

SYSTEM_REDACTOR = """Eres el Agente Redactor (El Examinador).
Tu función es redactar el supuesto práctico definitivo basado en los hechos proporcionados por el Investigador.

ESTRUCTURA EXIGIDA:
1. TRAMA NARRATIVA: Crea una historia profesional (ej. una empresa con varios trabajadores). 
2. PREGUNTAS: Crea entre justo 15 preguntas y justo 3 preguntas de reserva preguntas tipo test (4 opciones a,b,c,d), solo una correcta.
3. CLAVE DE RESPUESTAS: Al final, da la solución y justifica citando el artículo exacto.

REGLAS ESTRICTAS DE V12:
-usa la tabla de tarmpas para saber como hacer trampas pedagogicas al uauario como en los examenes oficiales! 
- REGLA DE ESCENARIOS MÚLTIPLES: Aisla a cada sujeto. Si la empresa tiene al trabajador A y al B, haz preguntas bloque para A y luego para B. BAJO NINGÚN CONCEPTO mezcles datos de ambos en los distractores de una pregunta.
- TRAMPAS SUTILES: Usa la técnica de "Maldad Sistémica". Distrae con datos irrelevantes en la narrativa (ej. "el trabajador A, que ha trabajado en regimen RETA..."), pero el cálculo debe ser matemáticamente puro en base a la ley.
- DISTRIBUCIÓN: Las respuestas correctas deben estar repartidas uniformemente (A, B, C, D). No uses siempre la "B".
"""

SYSTEM_AUDITOR = """Eres el Agente Auditor Adversarial (El Fiscal).
Eres un crítico implacable. Tu trabajo es DESTRUIR el examen generado por el Redactor buscando fallos legales.

REGLAS DE AUDITORÍA:
1. FECHA LÍMITE DE VIGENCIA NORMATIVA: Aplica ESTRICTAMENTE el filtro de fecha límite. Cualquier modificación de ley posterior a la fecha del examen NO EXISTE a efectos de puntuación y es un ERROR GRAVÍSIMO.
2. CÁLCULOS: Verifica matemáticamente cada operación.
3. NO MEZCLAS IRREGULARES: Comprueba que el Redactor no ha mezclado los datos de distintos personajes en la misma pregunta de forma ilógica.

De ser necesario puedes usar herramientas como 'verify_boe' o 'search_rag' para validar si tienes dudas.

FORMATO DE RESPUESTA EXIGIDO AL FINAL:
Debes responder SIEMPRE con un JSON válido con esta estructura:
{
    "status": "PASS" o "REJECT",
    "feedback": "Tus críticas detalladas aquí o un OK si todo está perfecto"
}
Si encuentras el más mínimo fallo legal o duda documentada, devuelve "REJECT" y explica por qué.
"""

async def execute_tool_call(call):
    """Ejecuta la función solicitada por Mistral."""
    func_name = call.get("function", {}).get("name")
    args_str = call.get("function", {}).get("arguments", "{}")
    
    try:
        args = repair_json(args_str, return_objects=True)
        if not isinstance(args, dict):
            args = {"query": str(args)}
    except:
        args = {"query": args_str}

    print(f"   🔧 Tool Called: {func_name} -> {args}")
    
    if func_name == "search_rag":
        query = args.get("query", args.get("consulta", ""))
        limit = args.get("limit", 5)
        rag = get_rag_helper()
        articles = rag.search_articles(query, limit=limit)
        return f"RESULTADOS RAG:\n{rag.format_articles_for_prompt(articles)}"
        
    elif func_name == "ejecutar_calculo":
        consulta = args.get("consulta", args.get("query", ""))
        calc_res = CasosPracticosDispatcher.ejecutar(consulta)
        return f"RESULTADO CÁLCULO:\n{calc_res}"
        
    elif func_name == "verify_boe":
        ley_id = args.get("ley_id", "")
        # Simulado por ahora, o podría llamar a httpx local:8000
        return f"BOE VERIFY: Modificación normativa no excede fecha límite. Norma vigente. (MOCK)"
        
    return "Error: Herramienta desconocida"

async def call_mistral_with_tools(system_prompt: str, user_prompt: str, tools=None, json_mode: bool = False, temperature: float = 0.7) -> str:
    """Función para llamar a Mistral resolviendo las herramientas en bucle si es necesario."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    total_iterations = 0
    max_iterations = 10
    
    while total_iterations < max_iterations:
        total_iterations += 1
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": temperature,
        }
        
        if tools:
            payload["tools"] = tools
            
        if json_mode and not tools:
            payload["response_format"] = {"type": "json_object"}
            
        try:
            async with httpx.AsyncClient(timeout=180.0) as client:
                response = await client.post(MISTRAL_URL, headers=HEADERS, json=payload)
                
                if response.status_code != 200:
                    print(f"❌ Error HTTP {response.status_code}: {response.text}")
                    return "{}" if json_mode else "ERROR"
                    
                data = response.json()
                choice = data["choices"][0]
                message = choice["message"]
                
                # Chequear si Mistral llamó a herramientas
                if message.get("tool_calls"):
                    # Mistral requiere que apendes su propio mensaje que contiene la llamada
                    messages.append(message)
                    
                    for call in message["tool_calls"]:
                        # Ejecutar herramienta
                        tool_result = await execute_tool_call(call)
                        # Apendar resultado
                        messages.append({
                            "role": "tool",
                            "name": call["function"]["name"],
                            "content": tool_result,
                            "tool_call_id": call["id"]
                        })
                    
                    continue # Siguiente loop al LLM
                    
                else:
                    return message.get("content", "")
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return "{}" if json_mode else "ERROR"
            
    print("⚠️ Max iterations reached in tool calling loop!")
    return messages[-1].get("content", "ERROR: MAX ITERATIONS")

async def main():
    print("\n" + "="*70)
    print("🛡️ ORQUESTADOR V12 (MISTRAL LARGE) — PATRÓN PRODUCER-CRITIC + HERRAMIENTAS")
    print("="*70 + "\n")
    
    # Parámetros del caso
    tematica = "Seguridad Social - Incapacidad Temporal y Jubilación"
    fecha_limite = "2026-03-04"  # Fecha de corte de vigencia
    
    # ---------------------------------------------------------
    # FASE 0: INVESTIGATOR (CON HERRAMIENTAS)
    # ---------------------------------------------------------
    print(f"[FASE 0] 🔎 Investigador extrayendo datos con herramientas (RAG/Calculadoras)...")
    
    investigator_query = f"""Extrae los porcentajes y requisitos matemáticos y legales puros para {tematica}. 
    Aplica estrictamente la normativa vigente a fecha de corte: {fecha_limite}.
    Asegúrate de investigar artículos relevantes usando tus herramientas. NO supongas nada."""
    
    legal_facts = await call_mistral_with_tools(SYSTEM_INVESTIGATOR, investigator_query, tools=TOOLS_SCHEMA, temperature=0.1)
    if legal_facts == "ERROR": return
    print("✅ Hechos extraídos con éxito (con evidencias RAG/Calculadoras).")
    
    # ---------------------------------------------------------
    # BUCLE ORQUESTADOR: REDACTOR -> AUDITOR
    # ---------------------------------------------------------
    max_loops = 3
    current_loop = 1
    draft_content = ""
    status = "REJECT"
    feedback = "Genera el primer borrador."
    
    while current_loop <= max_loops:
        print(f"\n🔄 [ITERACIÓN {current_loop}/{max_loops}]")
        
        # Pausa para rate limits API gratis de Mistral
        print("⏳ Pausando 4s por Rate Limits de Mistral...")
        await asyncio.sleep(4)
        
        # --- REDACTOR ---
        print(f"✍️ [FASE 1] Redactor (Productor) generando examen...")
        
        if current_loop == 1:
            redactor_query = f"""Hechos Legales Validados (Fecha Límite Normativa: {fecha_limite}):
{legal_facts}

Genera el supuesto práctico completo siguiendo estrictamente tus instrucciones de sistema."""
        else:
            redactor_query = f"""El Auditor ha RECHAZADO tu intento anterior con el siguiente FEEDBACK:
---
{feedback}
---
CORRIGE el examen teniendo en cuenta las críticas y manteniedo los estándares intactos (no mezclar personajes, distribucion uniforme).
Aquí tienes los Hechos Legales Originales:
{legal_facts} 
"""

        draft_content = await call_mistral_with_tools(SYSTEM_REDACTOR, redactor_query, temperature=0.4)
        
        # --- AUDITOR ---
        print("⏳ Pausando 4s por Rate Limits de Mistral antes de auditar...")
        await asyncio.sleep(4)
        print(f"⚖️ [FASE 2] Auditor (Crítico) validando el examen con herramientas...")
        
        auditor_query = f"""Filtro de Vigencia Normativa (Límite): {fecha_limite}
Examen a auditar:
---
{draft_content}
---
Usa las herramientas (RAG/BOE) si necesitas corroborar algún artículo o porcentaje.
SIEMPRE devuelve FINALMENTE un bloque JSON ({{\"status\": \"PASS\" o \"REJECT\", \"feedback\": \"...\"}})."""
        
        auditor_response = await call_mistral_with_tools(SYSTEM_AUDITOR, auditor_query, tools=TOOLS_SCHEMA, json_mode=False, temperature=0.1)
        
        # Parseo robusto del feedback final buscando el JSON
        import re
        json_match = re.search(r'\{.*\}', auditor_response, re.DOTALL)
        if json_match:
            try:
                audit_json = json.loads(json_match.group(0))
                status = str(audit_json.get("status", "REJECT")).upper()
                feedback = str(audit_json.get("feedback", "No feedback provided."))
            except json.JSONDecodeError:
                status = "REJECT"
                feedback = "Error decodificando el JSON del Auditor: " + auditor_response
        else:
            status = "REJECT"
            feedback = "Auditor falló al devolver un JSON estructurado. Texto devuelto: " + auditor_response[:200]
            
        print(f"🛑 Veredicto del Auditor: {status}")
        print(f"📝 Feedback: {feedback[:150]}...")
        
        if status == "PASS":
            print("\n🎉 ¡EL AUDITOR HA APROBADO EL EXAMEN!")
            break
            
        current_loop += 1
        
    # ---------------------------------------------------------
    # COMPILACIÓN FINAL (EL "COMMIT")
    # ---------------------------------------------------------
    if status != "PASS":
        print("\n⚠️ ALERTA: Se alcanzó el límite de iteraciones sin aprobación pura del Auditor. Guardando la mejor versión obtenida.")
        
    print("\n📦 Compilando y guardando el artefacto final...")
    
    os.makedirs(os.path.join(root_dir, "dataset_output"), exist_ok=True)
    filename = os.path.join(root_dir, "dataset_output", "v12_ecosistema_mistral_final.md")
    
    final_output = f"""# SUPUESTO PRÁCTICO GENERADO V12 - MISTRAL
> **Orquestador**: Producer-Critic + Tools Loop (Investigador + Auditor)
> **Iteraciones necesarias**: {current_loop if status == "PASS" else max_loops}
> **Estado Final Auditor**: {status}

{draft_content}
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_output)
        
    print(f"✅ ¡Proceso completado! Archivo guardado en: {filename}")

if __name__ == "__main__":
    asyncio.run(main())
