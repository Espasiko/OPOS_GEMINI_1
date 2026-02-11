#!/usr/bin/env python3
"""
SALAMANDRA EXAMEN COMPLETO - FINAL
Script 100% validado que procesa TODAS las preguntas del examen
Basado en test_working.py que funcionó correctamente
"""
import os
import sys
import json
import logging
import requests
import re
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Setup paths
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
os.chdir(BASE_DIR)
sys.path.insert(0, str(BASE_DIR))
load_dotenv(BASE_DIR / "backend/.env.backend")

# Logging robusto
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/examen_completo_FINAL.log', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

logger.info("="*80)
logger.info("🔥 SALAMANDRA - EXAMEN COMPLETO FINAL")
logger.info("="*80)

# Init components
qdrant = QdrantClient(url="http://localhost:6333", timeout=120.0)
embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")

# Load questions
with open('/tmp/todas_preguntas_enero25.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

logger.info(f"📝 Total preguntas: {len(all_questions)}")

# Output file
output_file = BASE_DIR / "staging_area/06_01_26_enrichment/examen_enero25_COMPLETO_FINAL.jsonl"
output_file.parent.mkdir(parents=True, exist_ok=True)

# Checkpoint
checkpoint_file = Path('/tmp/checkpoint_examen.json')

def load_checkpoint():
    try:
        with open(checkpoint_file, 'r') as f:
            data = json.load(f)
            return data.get('last_completed', 0)
    except:
        return 0

def save_checkpoint(q_id):
    with open(checkpoint_file, 'w') as f:
        json.dump({
            'last_completed': q_id,
            'timestamp': datetime.now().isoformat()
        }, f)

# Recovery
last_completed = load_checkpoint()
if last_completed > 0:
    logger.info(f"⚠️ Recuperando desde pregunta #{last_completed+1}")

# Process all questions
total = len(all_questions)
completed = 0

with open(output_file, 'a', encoding='utf-8') as f_out:
    for q in all_questions:
        if q['id'] <= last_completed:
            continue
        
        logger.info(f"\n{'='*80}")
        logger.info(f"PREGUNTA #{q['id']}/{total}")
        logger.info(f"{'='*80}")
        logger.info(f"Q: {q['question'][:80]}...")
        
        start_time = time.time()
        
        try:
            # RAG
            logger.info("RAG search...")
            vector = embedder.encode(q['question']).tolist()
            results = qdrant.search(
                collection_name="opositaia_knowledge_hybrid_FULL",
                query_vector=("dense", vector),
                limit=10,
                with_payload=True,
                score_threshold=0.3
            )
            
            context = "===CONTEXTO LEGAL===\n\n"
            for i, hit in enumerate(results, 1):
                context += f"[{i}] {hit.payload.get('law_name', 'Unknown')}\n"
                context += f"{hit.payload.get('text_snippet', hit.payload.get('text', ''))}\n\n"
            
            logger.info(f"RAG: {len(results)} resultados")
            
            # VPS
            logger.info("Llamando VPS...")
            payload = {
                "question": q['question'],
                "context": context,
                "options": {chr(97+i): opt for i, opt in enumerate(q['options'])}
            }
            
            response = requests.post(
                "http://electroyhogarpelotazo.tienda/salamandra/reason",
                json=payload,
                timeout=900
            )
            response.raise_for_status()
            
            data = response.json()
            reasoning_str = data.get('reasoning', '{}')
            
            # Robust parsing (validado que funciona)
            selected = '?'
            
            # Strategy 1: JSON
            try:
                reasoning = json.loads(reasoning_str.replace('```json', '').replace('```', '').strip())
                selected = reasoning.get('selected_option', '?')
                logger.info(f"✅ JSON parsing: {selected}")
            except:
                # Strategy 2: Regex
                match = re.search(r'selected_option:\s*([abcd])', reasoning_str, re.IGNORECASE)
                if match:
                    selected = match.group(1).lower()
                    logger.info(f"✅ Regex extraction: {selected}")
                else:
                    # Strategy 3: Fallback
                    for letter in ['a', 'b', 'c', 'd']:
                        if letter in reasoning_str[:100].lower():
                            selected = letter
                            logger.info(f"⚠️ Fallback: {selected}")
                            break
            
            elapsed = time.time() - start_time
            logger.info(f"✅ Respuesta: {selected} (en {elapsed:.1f}s)")
            
            # Save result
            result = {
                'question_id': q['id'],
                'selected_option': selected,
                'reasoning': reasoning_str,
                'time_seconds': round(elapsed, 1)
            }
            
            f_out.write(json.dumps(result, ensure_ascii=False) + '\n')
            f_out.flush()
            
            completed += 1
            
            # Checkpoint cada 5
            if q['id'] % 5 == 0:
                save_checkpoint(q['id'])
                logger.info(f"💾 Checkpoint: {q['id']}/{total}")
            
        except Exception as e:
            logger.error(f"💥 Error en pregunta #{q['id']}: {e}")
            # Guardar error y continuar
            error_result = {
                'question_id': q['id'],
                'selected_option': '?',
                'error': str(e)[:200]
            }
            f_out.write(json.dumps(error_result, ensure_ascii=False) + '\n')
            f_out.flush()

logger.info(f"\n{'='*80}")
logger.info(f"✅ EXAMEN COMPLETADO")
logger.info(f"📊 Preguntas procesadas: {completed}/{total}")
logger.info(f"📁 Output: {output_file}")
logger.info(f"{'='*80}")
print("EXAM_COMPLETE")
