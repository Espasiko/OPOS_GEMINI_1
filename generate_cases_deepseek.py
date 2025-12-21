
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
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
MODEL = "deepseek-reasoner"
OUTPUT_DIR = "dataset_generator/premium_content/deepseek_extreme"
MAX_RETRIES = 3

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY env var not set")

os.makedirs(OUTPUT_DIR, exist_ok=True)

METHODS = [
    "Cálculo de Pensiones: Lagunas de Cotización y Bases Mínimas (Integración)",
    "Falta de Alta y Responsabilidad Empresarial: Principio de Automaticidad",
    "Jubilación en Clases Pasivas vs Régimen General: Cómputo Recíproco",
    "Incapacidad Permanente en Funcionarios (MUFACE): Diferencias con RGSS",
    "ERTE y Mecanismo RED: Exoneraciones y Prohibición de Despido",
    "Procedimiento Sancionador: Actas de Liquidación y de Infracción (Concurrencia)",
    "Prestación por Cuidado de Menor con Cáncer: Requisitos y Reducción Jornada",
    "Trabajadores Fijos Discontinuos: Llamamiento y Desempleo (Cómputo Antigüedad)",
    "Alta Dirección: Indemnizaciones y Fondo de Garantía Salarial (FOGASA)",
    "Expatriados y Desplazados: Seguridad Social en Teletrabajo Internacional"
]

def generate_deepseek_case(topic: str) -> Optional[Dict[str, Any]]:
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Genera un CASO PRÁCTICO EXTREMO sobre: {topic}.
    
    ESTRUCTURA JSON:
    {{
      "topic": "{topic}",
      "scenario": "...",
      "questions": [
        {{ "id": "q1", "question": "...", "options": [ ... ], "correct_option_id": "...", "explanation": "..." }},
        ... (15 preguntas)
      ]
    }}
    
    IMPORTANTE:
    - Primero piensa paso a paso (Chain of Thought).
    - Luego devuelve SOLAMENTE el JSON.
    """
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Output JSON only."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"DeepSeek Reasoning for '{topic}'...")
            res = requests.post(url, headers=headers, json=payload, timeout=240)
            
            if res.status_code != 200:
                logger.error(f"Status Code: {res.status_code}")
                logger.error(f"Response Body: {res.text}")
                res.raise_for_status()
                
            data = res.json()
            content = data["choices"][0]["message"]["content"]
            
            case_json = json.loads(content)
            return case_json

        except Exception as e:
            logger.error(f"Error DeepSeek (Requests): {e}")
            time.sleep(10)
            
    return None

def main():
    logger.info("Starting DeepSeek Generation...")
    for i, topic in enumerate(METHODS):
        filename = f"{OUTPUT_DIR}/case_extreme_deepseek_v{i+1}.json"
        if os.path.exists(filename): continue
            
        case_data = generate_deepseek_case(topic)
        if case_data:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(case_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {filename}")
        time.sleep(5)

if __name__ == "__main__":
    main()
