import os
import json
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path

# --- CONFIGURACIÓN ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv("backend/.env.backend")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.error("❌ FALTA GROQ_API_KEY")
    exit(1)

client = Groq(api_key=GROQ_API_KEY)

OUTPUT_DIR = Path("dataset_generator/premium_content/groq_experiments")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- EXPERIMENTO 1: EL JUEZ (GPT OSS 120B) ---
# Usamos un caso "Draft" generado aleatoriamente o cargado.
# Para este test, inyectaremos un caso con un ERROR INTENCIONADO.

DUMMY_CASE_WITH_ERROR = {
    "titulo": "Caso Jubilación (Con Error Intencionado)",
    "escenario": "Juan, 67 años. Cotizados 10 años. Solicita Jubilación Contributiva.",
    "preguntas": [
        {
            "enunciado": "¿Tiene derecho a la contributiva?",
            "respuesta_correcta": "A",
            "opciones": ["A) Sí, porque tiene más de 65 años.", "B) No."],
            "justificacion": "Error: Se requieren 15 años mínimo, no 10. La opción A es jurídicamente falsa."
        }
    ]
}

def run_judge_experiment():
    logger.info("⚖️  [Exp 1] Iniciando JUEZ (openai/gpt-oss-120b)...")
    
    prompt = f"""
ACTÚA COMO: Magistrado del Tribunal Supremo (Sala Social).
TAREA: Audita el siguiente caso práctico.
DETECTA: Errores jurídicos graves.
CASO A AUDITAR: {json.dumps(DUMMY_CASE_WITH_ERROR)}

FORMATO RESPUESTA (JSON):
{{
  "veredicto": "APTO" o "NO APTO",
  "critica_juridica": "...",
  "errores_detectados": ["..."]
}}
"""
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b", # ID Confirmado
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"❌ Error Juez: {e}")
        return None

# --- EXPERIMENTO 2: EL INVESTIGADOR (COMPOUND) ---
# Usaremos groq/compound para buscar datos reales.

def run_researcher_experiment():
    logger.info("🕵️  [Exp 2] Iniciando INVESTIGADOR (groq/compound)...")
    
    # Prompt específico con limitación temporal solicitada por usuario
    prompt = """
TAREA: Investiga y redacta un mini-caso práctico.
TEMA: "Subsidio para mayores de 52 años y el SMI".
RESTRICCIÓN TEMPORAL: Búsqueda limitada a datos hasta AGOSTO 2025.
DATO CLAVE: Necesito que uses el valor del SMI vigente en ese periodo exacto (antes de posibles subidas posteriores).

SALIDA:
1. Valor del SMI encontrado.
2. Breve escenario (1 párrafo) usando ese valor para un cálculo de rentas (75% SMI).
"""
    
    try:
        completion = client.chat.completions.create(
            model="groq/compound", # ID Confirmado
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
            # No definimos tools manualmente, 'groq/compound' las tiene integradas (Web Search)
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"❌ Error Investigador: {e}")
        return None

# --- MAIN ---

if __name__ == "__main__":
    # 1. Ejecutar Juez
    judge_result = run_judge_experiment()
    if judge_result:
        logger.info(f"👨‍⚖️ Veredicto del Juez:\n{judge_result}\n")
        with open(OUTPUT_DIR / "exp1_judge_oss120b.json", "w") as f:
            f.write(judge_result)

    # 2. Ejecutar Investigador
    researcher_result = run_researcher_experiment()
    if researcher_result:
        logger.info(f"🕵️ Resultado Investigador:\n{researcher_result}\n")
        with open(OUTPUT_DIR / "exp2_researcher_compound.txt", "w") as f:
            f.write(researcher_result)
            
    logger.info("✅ Experimentos finalizados.")
