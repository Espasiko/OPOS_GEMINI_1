#!/usr/bin/env python3
"""
Enhanced Claude Judge - Batch API (CORRECTED)
Usando tipos correctos de anthropic library
"""

import json
import os
import time
import random
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

# Configuración
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
ENRICHMENT_DIR = BASE_DIR / "staging_area/06_01_26_enrichment"
OUTPUT_FILE = ENRICHMENT_DIR / "claude_critical_evaluation.jsonl"
ENV_FILE = BASE_DIR / "backend/.env.backend"

# Archivos de entrada (4 modelos)
FILE_SALAMANDRA = ENRICHMENT_DIR / "salamandra_reasoning.jsonl"
FILE_DEEPSEEK = ENRICHMENT_DIR / "deepseek_reasoning.jsonl"
FILE_GROQ_LLAMA = ENRICHMENT_DIR / "groq_llama.jsonl"
FILE_GROQ_GPT = ENRICHMENT_DIR / "groq_gpt_oss.jsonl"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("claude_batch_judge")

def load_env():
    """Cargar API key de Claude"""
    load_dotenv(ENV_FILE)
    key = os.getenv("CLAUDE_API_KEY")
    if not key:
        raise ValueError("CLAUDE_API_KEY no encontrada en .env.backend")
    return key

def load_jsonl_map(filepath):
    """Cargar JSONL y crear mapa por (filename, question_number)"""
    data = {}
    if not filepath.exists():
        logger.warning(f"⚠️ Archivo no encontrado: {filepath}")
        return data
        
    with open(filepath, "r") as f:
        for line in f:
            try:
                record = json.loads(line)
                key = (record['exam_filename'], record['question_number'])
                data[key] = record
            except Exception as e:
                logger.debug(f"Error parsing line: {e}")
    return data

def sample_common_questions(data_maps, sample_size=50):
    """Seleccionar N preguntas comunes a todos los modelos"""
    all_keys_sets = [set(data.keys()) for data in data_maps.values()]
    common_keys = set.intersection(*all_keys_sets) if all_keys_sets else set()
    
    logger.info(f"📊 Preguntas comunes: {len(common_keys)}")
    
    if len(common_keys) < sample_size:
        logger.warning(f"⚠️ Solo hay {len(common_keys)} preguntas comunes")
        return list(common_keys)
    
    sampled = random.sample(list(common_keys), sample_size)
    logger.info(f"🎲 Seleccionadas {len(sampled)} preguntas")
    return sampled

def build_system_prompt():
    return """Eres un Magistrado del Tribunal Supremo, Experto en Derecho Administrativo.

Evalúa CRÍTICAMENTE 4 sistemas de IA que responden preguntas de oposiciones jurídicas.

Tareas:
1. EVALUAR cada razonamiento (coherencia, fundamento legal, lógica)
2. CRITICAR fallos lógicos o errores
3. PROPONER lógicas alternativas
4. DECIDIR respuesta correcta final

Sé estricto pero justo."""

def build_user_message(question_data, model_outputs):
    return f"""CASO:

📋 PREGUNTA:
{question_data.get('text', 'N/A')}

📝 OPCIONES:
{json.dumps(question_data.get('options', {}), ensure_ascii=False, indent=2)}

---

🤖 SALAMANDRA: {model_outputs.get('salamandra', {}).get('selected_option', 'N/A')}
Razonamiento: {model_outputs.get('salamandra', {}).get('thought_process', 'N/A')[:400]}...

🤖 DEEPSEEK: {model_outputs.get('deepseek', {}).get('selected_option', 'N/A')}
Razonamiento: {model_outputs.get('deepseek', {}).get('thought_process', 'N/A')[:400]}...

🤖 GROQ LLAMA: {model_outputs.get('groq_llama', {}).get('selected_option', 'N/A')}
Razonamiento: {model_outputs.get('groq_llama', {}).get('thought_process', 'N/A')[:400]}...

🤖 GROQ GPT: {model_outputs.get('groq_gpt', {}).get('selected_option', 'N/A')}
Razonamiento: {model_outputs.get('groq_gpt', {}).get('thought_process', 'N/A')[:400]}...

---

RESPONDE EN JSON:
{{
  "final_correct_option": "b",
  "model_evaluations": {{
    "salamandra": {{"score": 7, "critique": "...", "logic_quality": "..."}},
    "deepseek": {{"score": 9, "critique": "...", "logic_quality": "..."}},
    "groq_llama": {{"score": 6, "critique": "...", "logic_quality": "..."}},
    "groq_gpt": {{"score": 8, "critique": "...", "logic_quality": "..."}}
  }},
  "alternative_reasoning_paths": ["..."],
  "golden_reasoning": "...",
  "best_model_for_this_question": "deepseek"
}}
"""

def main():
    parser = argparse.ArgumentParser(description="Claude Batch Judge - FIXED")
    parser.add_argument("--sample-size", type=int, default=10, help="Número de preguntas (default: 10)")
    parser.add_argument("--seed", type=int, default=42, help="Semilla (default: 42)")
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    logger.info("🎯 Claude Batch Judge - VERSIÓN CORREGIDA")
    logger.info(f"📊 Sample: {args.sample_size} preguntas")
    
    # 1. API Key
    api_key = load_env()
    client = Anthropic(api_key=api_key)
    
    # 2. Cargar datos
    logger.info("📚 Cargando datos...")
    data_salamandra = load_jsonl_map(FILE_SALAMANDRA)
    data_deepseek = load_jsonl_map(FILE_DEEPSEEK)
    data_groq_llama = load_jsonl_map(FILE_GROQ_LLAMA)
    data_groq_gpt = load_jsonl_map(FILE_GROQ_GPT)
    
    data_maps = {
        "salamandra": data_salamandra,
        "deepseek": data_deepseek,
        "groq_llama": data_groq_llama,
        "groq_gpt": data_groq_gpt
    }
    
    logger.info(f"  Sal:{len(data_salamandra)} DS:{len(data_deepseek)} GL:{len(data_groq_llama)} GG:{len(data_groq_gpt)}")
    
    # 3. Sample preguntas
    common_keys = sample_common_questions(data_maps, args.sample_size)
    
    if not common_keys:
        logger.error("❌ No hay preguntas comunes")
        return
    
    # 4. Construir batch requests CON TIPOS CORRECTOS
    logger.info(f"🔨 Construyendo batch...")
    
    system_prompt = build_system_prompt()
    batch_requests = []
    key_mapping = {}  # Para recuperar después
    
    for idx, key in enumerate(common_keys):
        filename, q_num = key
        
        rec_sal = data_salamandra.get(key, {})
        rec_ds = data_deepseek.get(key, {})
        rec_gl = data_groq_llama.get(key, {})
        rec_gg = data_groq_gpt.get(key, {})
        
        question_data = (rec_sal.get('question_data') or rec_ds.get('question_data') or 
                        rec_gl.get('question_data') or rec_gg.get('question_data', {}))
        
        model_outputs = {
            "salamandra": rec_sal.get('salamandra_output', {}),
            "deepseek": rec_ds.get('deepseek_output', {}),
            "groq_llama": rec_gl.get('groq_output', {}),
            "groq_gpt": rec_gg.get('groq_output', {})
        }
        
        user_message = build_user_message(question_data, model_outputs)
        custom_id = f"q{idx:03d}"
        
        # USAR TIPOS CORRECTOS de anthropic
        request = Request(
            custom_id=custom_id,
            params=MessageCreateParamsNonStreaming(
                model="claude-sonnet-4-5-20250929",  # ✅ Claude 4.5 correcto (no deprecated)
                max_tokens=2048,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
        )
        
        batch_requests.append(request)
        key_mapping[custom_id] = (key, question_data, model_outputs)
    
    # 5. Enviar batch
    logger.info(f"📤 Enviando batch de {len(batch_requests)} requests...")
    
    try:
        message_batch = client.messages.batches.create(requests=batch_requests)
        batch_id = message_batch.id
        
        logger.info(f"✅ Batch creado: {batch_id}")
        logger.info(f"📊 Estado: {message_batch.processing_status}")
        
        # 6. Polling
        logger.info(f"⏱️ Esperando (15-60 min)...")
        
        while True:
            batch_status = client.messages.batches.retrieve(batch_id)
            status = batch_status.processing_status
            
            if status == "ended":
                logger.info(f"✅ Batch completado!")
                break
            elif status in ["canceling", "canceled", "expired"]:
                logger.error(f"❌ Batch {status}")
                return
            
            logger.info(f"⏳ {status} - Esperando 30s...")
            time.sleep(30)
        
        # 7. Descargar resultados
        logger.info("📥 Descargando resultados...")
        
        processed = 0
        errors = 0
        
        with open(OUTPUT_FILE, "w") as f_out:
            for result in client.messages.batches.results(batch_id):
                custom_id = result.custom_id
                
                if custom_id not in key_mapping:
                    logger.warning(f"⚠️ ID desconocido: {custom_id}")
                    continue
                
                key, question_data, model_outputs = key_mapping[custom_id]
                filename, q_num = key
                
                # Parsear resultado
                if result.result.type == "succeeded":
                    content = result.result.message.content[0].text
                    
                    import re
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        try:
                            judge_output = json.loads(json_match.group(0))
                        except json.JSONDecodeError:
                            judge_output = {"error": "JSON parse failed", "raw": content[:200]}
                            errors += 1
                    else:
                        judge_output = {"error": "No JSON found", "raw": content[:200]}
                        errors += 1
                        
                elif result.result.type == "errored":
                    error_info = result.result.error
                    judge_output = {
                        "error": "API error",
                        "message": str(error_info)
                    }
                    logger.error(f"  ❌ Q{q_num}: {error_info}")
                    errors += 1
                else:
                    judge_output = {"error": f"Unknown type: {result.result.type}"}
                    errors += 1
                
                # Guardar
                final_result = {
                    "filename": filename,
                    "question_number": q_num,
                    "question_text": question_data.get('text'),
                    "options": question_data.get('options'),
                    "models_selected_options": {
                        "salamandra": model_outputs["salamandra"].get('selected_option'),
                        "deepseek": model_outputs["deepseek"].get('selected_option'),
                        "groq_llama": model_outputs["groq_llama"].get('selected_option'),
                        "groq_gpt": model_outputs["groq_gpt"].get('selected_option')
                    },
                    "claude_evaluation": judge_output
                }
                
                f_out.write(json.dumps(final_result, ensure_ascii=False) + "\n")
                f_out.flush()
                
                processed += 1
                if "error" not in judge_output:
                    best = judge_output.get('best_model_for_this_question', 'N/A')
                    logger.info(f"  ✅ Q{q_num} - Mejor: {best}")
        
        logger.info(f"\n🎉 Completado: {processed} procesados, {errors} errores")
        logger.info(f"📄 Output: {OUTPUT_FILE}")
        logger.info(f"💰 Costo: ~${len(common_keys) * 0.015:.2f}")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
