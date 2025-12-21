
import os
import json
import requests
import logging
import time
from datetime import datetime

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_env_vars():
    env_path = "backend/.env.backend"
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)

load_env_vars()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Schema Definition for Structured Outputs
CASE_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {"type": "string", "description": "Titulo del tema"},
        "scenario": {"type": "string", "description": "Escenario detallado del caso práctico (400-600 palabras)"},
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "question": {"type": "string"},
                    "options": {
                        "type": "array", 
                        "items": {
                            "type": "object", 
                            "properties": {
                                "id": {"type": "string"}, 
                                "text": {"type": "string"}
                            }, 
                            "required": ["id", "text"],
                            "additionalProperties": False
                        }
                    },
                    "correct_option_id": {"type": "string"},
                    "explanation": {"type": "string", "description": "Explicación jurídica detallada"}
                },
                "required": ["id", "question", "options", "correct_option_id", "explanation"],
                "additionalProperties": False
            }
        }
    },
    "required": ["topic", "scenario", "questions"],
    "additionalProperties": False
}

def generate_premium_case(topic, max_retries=5):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "anthropic-beta": "structured-outputs-2025-11-13" # Header oficial del Cookbook
    }
    
    prompt = f"""Eres un Preparador de Élite de la Escala Técnica de Gestión de la Seguridad Social.
Tu tarea es redactar un CASO PRÁCTICO DE DIFICULTAD EXTREMA sobre: '{topic}'.

OBJETIVO:
- Crear trampas sutiles basadas en plazos legales, excepciones y jurisprudencia minoritaria.
- El 90% de los opositores debería fallar estas preguntas si no analizan cada palabra del enunciado.

REQUERIMIENTOS:
1. ESCENARIO (400-600 palabras): Relato denso con múltiples fechas, situaciones cruzadas y datos técnicos.
2. PREGUNTAS: 10 preguntas de test derivadas exclusivamente del escenario.
3. EXPLICACIÓN: Disertación jurídica citando normas exactas (LGSS, etc.).
"""

    payload = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 4096,
        "tools": [
            {
                "name": "generate_case",
                "description": "Generates a complete legal case study with questions.",
                "input_schema": CASE_SCHEMA,
                # Strict mode enabled via tool definition for this beta
            }
        ],
        "tool_choice": {"type": "tool", "name": "generate_case"},
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4
    }

    # Add strict: true to the tool definition's top level if supported by the beta, 
    # but based on test script success, it seems implicit or handled via Schema structure + beta header.
    # We will explicitly add it as per some docs patterns just to be safe if the API accepts it.
    payload["tools"][0]["strict"] = True

    for attempt in range(max_retries):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=300)
            
            if r.status_code == 429:
                wait_time = (2 ** attempt) * 30
                logger.warning(f"⚠️ Rate limit (429). Reintentando en {wait_time}s... (Intento {attempt+1}/{max_retries})")
                time.sleep(wait_time)
                continue
                
            r.raise_for_status()
            data = r.json()
            
            # Parsing Structured Output from Tool Use
            if "content" in data:
                for block in data["content"]:
                    if block["type"] == "tool_use":
                        return block["input"] # Devuelve el JSON ya parseado y validado
            
            logger.error(f"❌ No se encontró 'tool_use' en la respuesta: {data}")
            return None

        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"⚠️ Error en intento {attempt+1}: {e}. Reintentando...")
                time.sleep(10)
            else:
                logger.error(f"❌ Error definitivo para '{topic}': {e}")
                if 'r' in locals() and hasattr(r, 'text'):
                    logger.error(f"Response Body: {r.text}")
                return None
    return None

if __name__ == "__main__":
    test_topics = [
        "Jubilación Anticipada: Coexistencia de coeficientes reductores por discapacidad y por naturaleza penosa del trabajo",
        "Incapacidad Permanente: Revisión por agravamiento tras los 65 años habiendo optado por la prestación de IP",
        "Responsabilidad Solidaria: Contratas de 'propia actividad' vs no propia actividad y derivación de deudas a la SS",
        "Pensión de Viudedad: Divorcio con pensión compensatoria extinguida por fallecimiento y límites de cuantía",
        "Ingreso Mínimo Vital: Unidad de convivencia compleja con personas con vínculos no registrados y cómputo de rentas",
        "Prestación por Desempleo: Capitalización para autónomo societario y mantenimiento de la actividad (Plazos LGSS)",
        "Procedimiento Administrativo: Silencio administrativo negativo vs positivo en solicitudes de prestaciones de SS",
        "Convenios Internacionales: Cómputo de periodos de seguro en países extracomunitarios con convenio bilateral",
        "Régimen del Mar: Coeficientes de bonificación por edad en embarcaciones de pesca de altura",
        "Infracciones y Sanciones: Recargo de prestaciones por falta de medidas de seguridad y su aseguramiento"
    ]
    
    output_dir = "dataset_generator/premium_content/claude_extreme"
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info(f"🚀 Iniciando generación de {len(test_topics)} casos EXTREMOS con Claude 4.5 Sonnet (Structured Outputs)...")
    
    for i, topic in enumerate(test_topics):
        output_file = f"{output_dir}/case_extreme_claude_v{i+1}.json"
        if os.path.exists(output_file) and os.path.getsize(output_file) > 100:
            logger.info(f"⏭️  [{i+1}/{len(test_topics)}] Saltando (Ya existe): {topic}")
            continue

        logger.info(f"🎭 [{i+1}/{len(test_topics)}] Generando: {topic}")
        case = generate_premium_case(topic)
        
        if case:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(case, f, ensure_ascii=False, indent=2)
            logger.info(f"✅ Caso {i+1} guardado correctamente.")
            time.sleep(10) 
        else:
            logger.error(f"❌ Fallo en el caso {i+1}.")
            # No abortamos, intentamos el siguiente
