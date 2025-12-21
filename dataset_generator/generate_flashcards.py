
import os
import json
import logging
import requests
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_env_vars():
    env_path = "backend/.env.backend"
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)

load_env_vars()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

TOPICS = [
    "Artículos clave de la Constitución Española",
    "Ley 39/2015: El Acto Administrativo",
    "Ley 40/2015: Régimen Jurídico del Sector Público",
    "Ley General de la Seguridad Social: Entidades Gestoras",
    "Infracciones y Sanciones en el Orden Social (LISOS)"
]

def generate_flashcards(topic, count=10):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    
    prompt = f"""Eres un experto pedagógico en oposiciones de España.
Genera {count} FLASHCARDS (Anki-style) para memorizar conceptos del tema: '{topic}'.

Criterio:
- Anverso (Front): Pregunta corta o término (ej: "Art. 14 CE").
- Reverso (Back): Definición o contenido exacto abreviado.

Responde ÚNICAMENTE en un ARRAY JSON:
[
  {{"front": "...", "back": "...", "id": "..."}}
]
"""

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        clean_json = content.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        logger.error(f"Error generando flashcards: {e}")
        return []

if __name__ == "__main__":
    all_flashcards = []
    output_file = "dataset_generator/premium_content/flashcards_legal_v1.jsonl"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    for topic in TOPICS:
        logger.info(f"🗂️ Generando flashcards para: {topic}")
        cards = generate_flashcards(topic, 10)
        all_flashcards.extend(cards)
        
        with open(output_file, "a", encoding="utf-8") as f:
            for card in cards:
                card["topic"] = topic
                card["timestamp"] = datetime.now().isoformat()
                f.write(json.dumps(card, ensure_ascii=False) + "\n")
                
    print(f"✅ Generadas {len(all_flashcards)} flashcards en {output_file}")
