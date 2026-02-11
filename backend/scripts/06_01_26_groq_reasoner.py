
import json
import os
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Configuración
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
STAGING_DIR = BASE_DIR / "staging_area/05_01_26_exams_processing"
ENRICHMENT_DIR = BASE_DIR / "staging_area/06_01_26_enrichment"
INPUT_FILE = STAGING_DIR / "smart_paired_exams_cleaned.jsonl"
OUTPUT_FILE = ENRICHMENT_DIR / "groq_llama.jsonl"
ENV_FILE = BASE_DIR / "backend/.env.backend"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("groq_reasoner")

def load_env():
    load_dotenv(ENV_FILE)
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY no encontrada en .env.backend")
    return key

def main():
    api_key = load_env()
    client = Groq(api_key=api_key)
    
    ENRICHMENT_DIR.mkdir(parents=True, exist_ok=True)
    
    # SYSTEM PROMPT (Idéntico al de DeepSeek para "Igualdad de Condiciones")
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

    model_id = "llama-3.3-70b-versatile" # Llama 3.3
    
    processed_exams = 0
    MAX_EXAMS = 2 

    
    with open(INPUT_FILE, "r") as f_in, open(OUTPUT_FILE, "w") as f_out:
        for line in f_in:
            if processed_exams >= MAX_EXAMS:
                break
                
            exam_data = json.loads(line)
            filename = exam_data['filename']
            questions = exam_data['content']
            
            logger.info(f"⚡ Procesando Examen con Groq: {filename}")
            
            for q in questions:
                if not q.get('options') or len(q['options']) < 2:
                    continue
                    
                q_text = f"Pregunta {q['number']}: {q['text']}\n"
                for k, v in q['options'].items():
                    q_text += f"{k}) {v}\n"
                
                user_msg = f"Resuelve esta pregunta:\n\n{q_text}"
                
                try:
                    logger.info(f"   -> Enviando Q{q['number']} a Groq ({model_id})...")
                    
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_msg}
                        ],
                        model=model_id,
                        temperature=0.3, # Baja temperatura para precisión legal
                        response_format={"type": "json_object"}
                    )
                    
                    content = chat_completion.choices[0].message.content
                    
                    # Parse JSON
                    analysis_json = json.loads(content)
                    
                    result_record = {
                        "exam_filename": filename,
                        "question_number": q['number'],
                        "question_data": q,
                        "official_correct_answer_from_key": q.get('correct_answer'),
                        "groq_output": analysis_json,
                        "model_used": model_id
                    }
                    
                    f_out.write(json.dumps(result_record, ensure_ascii=False) + "\n")
                    f_out.flush()
                    
                    # Rate limit handling (Groq es rápido pero tiene límites por minuto)
                    time.sleep(2) 
                    
                except Exception as e:
                    logger.error(f"   ❌ Error Groq API en Q{q['number']}: {e}")
            
            processed_exams += 1
            
    logger.info(f"✅ Proceso Groq terminado. Resultados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
