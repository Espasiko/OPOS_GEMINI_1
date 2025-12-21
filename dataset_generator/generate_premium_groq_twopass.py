import os
import json
import logging
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path

# --- CONFIGURACIÓN ---
# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv("backend/.env.backend")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.error("❌ FALTA GROQ_API_KEY en backend/.env.backend")

# Cliente Groq
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    logger.error(f"Error inicializando cliente Groq: {e}")
    client = None

# Variables Globales
OUTPUT_DIR = Path("dataset_generator/premium_content/groq_rematch")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- PROMPTS ---

# 1. ROL: ARQUITECTO (Fase Thinking)
SYSTEM_PROMPT_ARCHITECT = """Eres un Miembro del Tribunal de Oposiciones de la Seguridad Social y un Jurista Experto.
Tu misión NO es redactar preguntas, sino DISEÑAR la estructura de un Caso Práctico de Dificultad Extrema para filtrar opositores.
Debes actuar como un estratega legal: busca las excepciones, los conflictos de leyes y los plazos engañosos."""

PROMPT_ARCHITECT_TEMPLATE = """
TEMA: "{topic}"

CONTEXTO LEGAL (RAG):
{context}

TAREA DE DISEÑO (THINKING):
Analiza el tema y el contexto legal.
1. Identifica 3 puntos de conflicto normativo (donde la ley es ambigua o hay excepciones).
2. Diseña un ESCENARIO DRAFT: Resume los hechos clave que deben ocurrir para activar estas trampas (fechas, parentescos, tipos de contrato).
3. Planifica 3 "Trampas Mortales": ¿Qué detalle pasará desapercibido al opositor novato?

SALIDA ESPERADA:
Un análisis detallado en texto plano. NO generes JSON todavía. Piensa paso a paso.
"""

# 2. ROL: EJECUTOR (Fase Writing)
SYSTEM_PROMPT_WRITER = """Eres un Redactor Oficial de Exámenes de la Administración Pública.
Tu trabajo es convertir un PLAN JURÍDICO en un examen real, con un formato estricto y tono formal."""

PROMPT_WRITER_TEMPLATE = """
PLAN JURÍDICO (DEL TRIBUNAL):
{architect_plan}

TAREA DE REDACCIÓN:
Basándote EXCLUSIVAMENTE en el plan anterior, redacta el caso práctico final en formato JSON.

REQUISITOS OBLIGATORIOS:
1. ESCENARIO: Narrativa densa (600-800 palabras), con fechas exactas y datos administrativos.
2. PREGUNTAS: Genera EXACTAMENTE 18 preguntas:
   - Preguntas 1 a 15: Tipo "Ordinaria".
   - Preguntas 16 a 18: Tipo "Reserva" (OBLIGATORIO).
3. EXPLICACIONES: Justificación legal citando artículos concretos.

FORMATO JSON (Stricto Sensu):
{{
  "titulo": "...",
  "dificultad": "EXTREMA",
  "escenario": "...",
  "preguntas": [
    {{
      "numero": 1,
      "enunciado": "...",
      "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "respuesta_correcta": "A",
      "tipo": "Ordinaria",
      "justificacion_legal": "Art. ...",
      "trampa_logica": "..."
    }}
    // ... hasta la 18
  ]
}}
Responde SOLO con el JSON.
"""

# --- FUNCIONES ---

def generate_architect_plan(topic, context):
    """Fase 1: Generar el plan de diseño (Thinking)."""
    logger.info(f"🧠 [Fase 1] Tribunal analizando: {topic}...")
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_ARCHITECT},
        {"role": "user", "content": PROMPT_ARCHITECT_TEMPLATE.format(topic=topic, context=context)}
    ]
    
    try:
        # Usamos Llama-3.3-70b-versatile porque es el más capaz de Groq actualmente
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=4096, # Suficiente para pensar
            timeout=120      # Timeout alto solicitado
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"❌ Error Fase 1 (Arquitecto): {e}")
        return None

def generate_final_case(architect_plan):
    """Fase 2: Generar y Parsear el JSON (Writing)."""
    logger.info(f"✍️ [Fase 2] Redactor escribiendo el examen...")
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_WRITER},
        {"role": "user", "content": PROMPT_WRITER_TEMPLATE.format(architect_plan=architect_plan)}
    ]
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.2, # Baja temperatura para JSON estricto
            response_format={"type": "json_object"}, # Forzar modo JSON
            max_tokens=8000, # Ventana ampliada al máximo
            timeout=180      # 3 minutos de timeout para generación larga
        )
        content = completion.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        logger.error(f"❌ Error Fase 2 (Redactor): {e}")
        return None

def get_rag_context(topic):
    # Simulación de RAG si no tenemos la función accesible, 
    # pero aquí vamos a intentar importar la función real si es posible 
    # o usar un placeholder fuerte para probar el script.
    # TODO: Integrar con `buscar_rag_exhaustivo` del proyecto real.
    # Por ahora devolvemos un string genérico para probar la lógica Two-Pass.
    return f"Normativa aplicable a: {topic}. Ley General de Seguridad Social, arts. 160-180. RD 8/2015."

# --- MAIN ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, default="Jubilación Activa para Autónomos vs Trabajadores Cuenta Ajena")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not GROQ_API_KEY:
        logger.error("Abortando: No API Key.")
        exit(1)

    logger.info("🚀 Iniciando REMATCH PREMIUM (Groq Two-Pass)...")
    
    # 0. Contexto
    # En producción real, aquí llamaríamos al RAG.
    # Para este test, usamos un contexto simulado o vacío si es un dry run simple.
    test_context = "Ley General de la Seguridad Social, Artículo 214. Pensión de jubilación y envejecimiento activo. Requisitos: 100% cotización, compatibilidad trabajo-pensión (50% o 100% si contrata). Plazos de solicitud."
    
    # 1. Fase Arquitecto
    plan = generate_architect_plan(args.topic, test_context)
    if not plan:
        exit(1)
    
    logger.info(f"📜 Plan Generado ({len(plan)} chars):\n{plan[:300]}...\n")
    
    # 2. Fase Redactor
    final_json = generate_final_case(plan)
    
    if final_json:
        # Validación básica
        qs = final_json.get("preguntas", [])
        logger.info(f"✅ JSON Generado con {len(qs)} preguntas.")
        
        # Validar 18 preguntas
        if len(qs) < 18:
            logger.warning(f"⚠️ Alerta: Se generaron {len(qs)} preguntas en lugar de 18. Revisar prompt.")
        else:
             logger.info(f"🏆 EXITO: 18 Preguntas generadas.")

        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"groq_rematch_case_{timestamp}.json"
        path = OUTPUT_DIR / filename
        
        final_data = {
            "metadata": {
                "model": "llama-3.3-70b-versatile",
                "strategy": "Two-Pass (Architect -> Writer)",
                "topic": args.topic
            },
            "architect_plan": plan, # Guardamos el Thinking
            "case": final_json
        }
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Guardado en: {path}")
    else:
        logger.error("❌ Falló la generación del JSON final.")
