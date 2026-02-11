
import json
import os
import requests
import logging
import time
from pathlib import Path
from dotenv import load_dotenv

# Configuración
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
STAGING_DIR = BASE_DIR / "staging_area/05_01_26_exams_processing"
ENRICHMENT_DIR = BASE_DIR / "staging_area/06_01_26_enrichment"
INPUT_FILE = STAGING_DIR / "smart_paired_exams_cleaned.jsonl"
OUTPUT_FILE = ENRICHMENT_DIR / "deepseek_reasoning.jsonl"
ENV_FILE = BASE_DIR / "backend/.env.backend"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("deepseek_reasoner")

def load_env():
    load_dotenv(ENV_FILE)
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise ValueError("DEEPSEEK_API_KEY no encontrada en .env.backend")
    return key

def call_deepseek(api_key, system_prompt, user_prompt, model="deepseek-reasoner"):
    """
    Llama a la API de DeepSeek. Intenta usar 'deepseek-reasoner' (R1) primero.
    Si falla, fallback a 'deepseek-chat' (V3).
    """
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3, 
        "stream": False
    }

    response = None
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=90) # Increased timeout
        data = response.json()
        
        # Extraer contenido y posible contenido de razonamiento (si el modelo lo soporta nativamente)
        content = data['choices'][0]['message']['content']
        reasoning = data['choices'][0]['message'].get('reasoning_content', None) 
        
        # Si no hay campo 'reasoning_content' específico, asumimos que está en el content si usamos deepseek-reasoner
        # Pero si usamos chat, el content es todo.
        
        return content, reasoning
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error Request DeepSeek: {e}")
        if response is not None:
             logger.error(f"Response Body: {response.text}")
        return None, None

def main():
    api_key = load_env()
    ENRICHMENT_DIR.mkdir(parents=True, exist_ok=True)
    
    # SYSTEM PROMPT ROBUSTO (Chain of Thought enforced)
    system_prompt = """Eres un Experto Jurídico de Oposiciones en España.
Tu tarea es analizar preguntas de examen tipo test, RAZONAR paso a paso cuál es la correcta basándote en la ley vigente (Constitución, TREBEP, LPAC, LRJSP, etc.), y explicar por qué las distractoras son falsas.

IMPORTANTE:
1. Actúa en DOS FASES:
   - FASE DE PENSAMIENTO: Analiza la pregunta. Identifica la normativa aplicable. Evalúa cada opción (A, B, C, D) contra la ley. Determina la trampa.
   - FASE DE RESPUESTA JSON: Genera un JSON final con la estructura solicitada.

2. Tu output final debe ser EXCLUSIVAMENTE un bloque JSON válido (sin markdown ```json ... ```) con este formato:
{
  "thought_process": "Aquí escribe todo tu razonamiento previo, paso a paso...",
  "selected_option": "a", 
  "law_reference": "Art. X de la Ley Y...",
  "analysis": {
     "a": "Correcta porque...",
     "b": "Incorrecta porque...",
     "c": "Incorrecta porque...",
     "d": "Incorrecta porque..."
  }
}
"""

    processed_exams = 0
    MAX_EXAMS = 2 # Limite solicitado por el usuario para probar
    
    with open(INPUT_FILE, "r") as f_in, open(OUTPUT_FILE, "w") as f_out:
        for line in f_in:
            if processed_exams >= MAX_EXAMS:
                break
                
            exam_data = json.loads(line)
            filename = exam_data['filename']
            paired_key = exam_data['paired_with']
            questions = exam_data['content']
            
            logger.info(f"🧠 Procesando Examen: {filename} (Total preguntas: {len(questions)})")
            
            # Procesar cada pregunta
            for q in questions:
                # Validar que tenga opciones
                if not q.get('options') or len(q['options']) < 2:
                    continue
                    
                q_text = f"Pregunta {q['number']}: {q['text']}\n"
                for k, v in q['options'].items():
                    q_text += f"{k}) {v}\n"
                
                # A veces el 'correct_answer' ya viene del pairing script anterior
                # Lo pasamos en el prompt? NO. El usuario quiere que DeepSeek razone A CIEGAS ("compara con las preguntas correctas").
                # DeepSeek NO debe saber la respuesta correcta a priori.
                
                user_msg = f"Resuelve esta pregunta:\n\n{q_text}"
                
                logger.info(f"   -> Enviando Q{q['number']} a DeepSeek...")
                
                # Intentar primero con deepseek-reasoner (R1) que es el bueno para CoT
                content, reasoning_raw = call_deepseek(api_key, system_prompt, user_msg, model="deepseek-reasoner")
                
                # Si falla o no está disponible, fallback a deepseek-chat
                if not content: 
                    logger.warning("   ⚠️ Fallo deepseek-reasoner, reintentando con deepseek-chat...")
                    content, reasoning_raw = call_deepseek(api_key, system_prompt, user_msg, model="deepseek-chat")
                
                if content:
                    # Intentar parsear el JSON del content
                    try:
                        # Limpiar posible markdown ```json
                        clean_content = content.replace("```json", "").replace("```", "").strip()
                        analysis_json = json.loads(clean_content)
                        
                        # Construir registro final
                        result_record = {
                            "exam_filename": filename,
                            "question_number": q['number'],
                            "question_data": q,
                            "official_correct_answer_from_key": q.get('correct_answer'), # Truth actual (extraída de plantilla)
                            "deepseek_output": analysis_json,
                            "deepseek_raw_reasoning_field": reasoning_raw, # Si la API devuelve campo separado
                            "model_used": "deepseek-reasoner" if reasoning_raw else "deepseek-chat"
                        }
                        
                        f_out.write(json.dumps(result_record, ensure_ascii=False) + "\n")
                        f_out.flush() # Guardar seguro
                        
                    except json.JSONDecodeError:
                        logger.error(f"   ❌ Error parseando JSON de DeepSeek en Q{q['number']}")
                        logger.error(f"   Content received: {content[:200]}...")
                else:
                    logger.error(f"   ❌ Fallo total en Q{q['number']}")
                
                # Rate limit protection (simple)
                time.sleep(1.5) 

            processed_exams += 1
            
    logger.info(f"✅ Proceso terminado. Resultados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
