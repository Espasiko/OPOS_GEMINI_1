
import os
import time
import requests
import json
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load env from backend config
load_dotenv("backend/.env.backend")


# --- CONFIG ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"
OUTPUT_DIR = "dataset_generator/premium_content/groq_extreme"
MAX_RETRIES = 3

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY env var not set")

os.makedirs(OUTPUT_DIR, exist_ok=True)

METHODS = [
    "Sanciones LISOS: Graduación, Reincidencia y Prescripción",
    "Jubilación Parcial con Contrato de Relevo: Requisitos Empresa y Trabajador",
    "Incapacidad Temporal: Pago Directo vs Delegado y Extinción",
    "Prestación por Nacimiento y Cuidado de Menor: Parto Múltiple y Hospitalización",
    "Régimen de Autónomos (RETA): Tarifa Plana y Pluriactividad",
    "Recaudación Ejecutiva: Embargo de Salarios y Compensación de Deudas",
    "Subsidio de Desempleo para Mayores de 52 años: Rentas y Continuidad",
    "Prestaciones por Muerte y Supervivencia: Pareja de Hecho vs Matrimonio",
    "Convenio Especial con la Seguridad Social: Tipos y Requisitos",
    "Accidente de Trabajo in Itinere vs En Misión: Jurisprudencia Reciente"
]

# JSON Schema for Tool/Function Calling ensures valid output
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "submit_practical_case",
            "description": "Submits a generated practical legal case with scenario and 15 questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "scenario": {"type": "string", "description": "Complex legal scenario (400-600 words)."},
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
                                            "id": {"type": "string", "enum": ["a", "b", "c", "d"]},
                                            "text": {"type": "string"},
                                            "true": {"type": "boolean"}
                                        },
                                        "required": ["id", "text"]
                                    },
                                    "minItems": 4,
                                    "maxItems": 4
                                },
                                "correct_option_id": {"type": "string", "enum": ["a", "b", "c", "d"]},
                                "explanation": {"type": "string"}
                            },
                            "required": ["id", "question", "options", "correct_option_id", "explanation"]
                        },
                        "minItems": 15,
                        "maxItems": 15
                    }
                },
                "required": ["topic", "scenario", "questions"]
            }
        }
    }
]

def generate_groq_case(topic: str) -> Optional[Dict[str, Any]]:
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Eres un experto Jurista de la Seguridad Social española.
    Genera un CASO PRÁCTICO EXTREMO sobre: {topic}.
    
    Instrucciones:
    1. Redacta un ESCENARIO denso y complejo.
    2. Genera 15 PREGUNTAS (12 OFICIALES + 3 RESERVA).
    3. Usa la herramienta 'submit_practical_case' para entregar el resultado.
    """

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that generates JSON data."},
            {"role": "user", "content": prompt}
        ],
        "tools": TOOLS,
        "tool_choice": {"type": "function", "function": {"name": "submit_practical_case"}},
        "temperature": 0.3
    }

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Generating Groq case for '{topic}'...")
            res = requests.post(url, headers=headers, json=payload, timeout=120)
            
            if res.status_code == 429:
                logger.warning("Rate limit. Waiting 10s...")
                time.sleep(10)
                continue
                
            res.raise_for_status()
            data = res.json()
            
            # Extract arguments from tool call
            tool_calls = data["choices"][0]["message"].get("tool_calls")
            if tool_calls:
                arguments = tool_calls[0]["function"]["arguments"]
                case_json = json.loads(arguments)
                return case_json
                
        except Exception as e:
            logger.error(f"Error Groq: {e}")
            time.sleep(5)
            
    return None

def main():
    logger.info("Starting Groq Generation...")
    for i, topic in enumerate(METHODS):
        filename = f"{OUTPUT_DIR}/case_extreme_groq_v{i+1}.json"
        if os.path.exists(filename): 
            continue
            
        case_data = generate_groq_case(topic)
        if case_data:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(case_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {filename}")
        time.sleep(2)

if __name__ == "__main__":
    main()
