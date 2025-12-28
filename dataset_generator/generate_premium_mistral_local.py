import os
import json
import logging
import requests
import argparse
from datetime import datetime
from pathlib import Path

# --- CONFIGURACIÓN ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral:latest"

OUTPUT_DIR = Path("dataset_generator/premium_content/mistral_rematch")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- PROMPTS (IDÉNTICOS AL GROQ REMATCH) ---

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

def call_ollama(messages, json_mode=False):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.2 if json_mode else 0.7,
        "stream": False,
        "options": {
            "num_ctx": 8192,  # Contexto amplio
            "num_predict": 4096 # Output largo
        }
    }
    
    if json_mode:
        payload["format"] = "json"

    try:
        # AQUI ESTA EL CAMBIO IMPORTANTE: Timeout 1200 segundos (20 min)
        response = requests.post(OLLAMA_URL, json=payload, timeout=1200) 
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        logger.error(f"❌ Error Ollama: {e}")
        return None

def generate_architect_plan(topic, context):
    logger.info(f"🧠 [Fase 1] Mistral (Arquitecto) pensando sobre: {topic}...")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_ARCHITECT},
        {"role": "user", "content": PROMPT_ARCHITECT_TEMPLATE.format(topic=topic, context=context)}
    ]
    return call_ollama(messages, json_mode=False)

def generate_final_case(architect_plan):
    logger.info(f"✍️ [Fase 2] Mistral (Redactor) escribiendo JSON...")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_WRITER},
        {"role": "user", "content": PROMPT_WRITER_TEMPLATE.format(architect_plan=architect_plan)}
    ]
    
    content = call_ollama(messages, json_mode=True)
    if content:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.error("❌ Error decodificando JSON de Mistral.")
            return None
    return None

# --- MAIN ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, default="Jubilación Activa para Autónomos vs Trabajadores Cuenta Ajena")
    args = parser.parse_args()

    logger.info(f"🚀 Iniciando MISTRAL LOCAL REMATCH (Two-Pass). Modelo: {MODEL_NAME}")
    
    # Contexto Simulado (mismo que Groq para comparación justa)
    test_context = "Ley General de la Seguridad Social, Artículo 214. Pensión de jubilación y envejecimiento activo. Requisitos: 100% cotización, compatibilidad trabajo-pensión (50% o 100% si contrata). Plazos de solicitud."
    
    # 1. Fase Arquitecto
    plan = generate_architect_plan(args.topic, test_context)
    if not plan: exit(1)
    
    logger.info(f"📜 Plan Generado: {len(plan)} chars.")
    
    # 2. Fase Redactor
    final_json = generate_final_case(plan)
    
    if final_json:
        qs = final_json.get("preguntas", [])
        logger.info(f"✅ JSON Generado con {len(qs)} preguntas.")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mistral_rematch_case_{timestamp}.json"
        path = OUTPUT_DIR / filename
        
        final_data = {
            "metadata": {
                "model": MODEL_NAME,
                "strategy": "Two-Pass (Architect -> Writer)",
                "topic": args.topic
            },
            "architect_plan": plan,
            "case": final_json
        }
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"💾 Guardado: {path}")
    else:
        logger.error("❌ Falló la generación final.")
