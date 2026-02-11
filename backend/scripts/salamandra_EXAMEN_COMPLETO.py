#!/usr/bin/env python3
"""
Salamandra ULTRA - Examen Completo con Checkpoints
Ejecuta TODAS las preguntas con recuperación de errores
"""
import os
import sys
import json
import logging
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

# Qdrant + Embeddings
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Setup
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
ENV_FILE = BASE_DIR / "backend/.env.backend"
load_dotenv(ENV_FILE)

# Logging detallado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/salamandra_examen_completo.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SalamandraEXAMEN")

# === CONFIG ===
CONFIG = {
    "qdrant_url": "http://localhost:6333",
    "collection": "opositaia_knowledge_hybrid_FULL",
    "top_k_initial": 10,
    "top_k_final": 10,
    "timeout": 900,  # 15 min por pregunta
    "checkpoint_file": "/tmp/salamandra_checkpoint.json"
}

class SalamandraExamen:
    def __init__(self):
        logger.info("="*80)
        logger.info("🔥 SALAMANDRA EXAMEN COMPLETO - Init")
        logger.info("="*80)
        
        self.qdrant = QdrantClient(url=CONFIG['qdrant_url'], timeout=120.0)
        self.embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
        
        logger.info(f"✅ RAG: {CONFIG['qdrant_url']}")
        logger.info(f"✅ Timeout: {CONFIG['timeout']}s por pregunta\n")
    
    def search_rag(self, query: str) -> List[Dict]:
        """RAG Search con manejo de errores"""
        try:
            vector = self.embedder.encode(query).tolist()
            results = self.qdrant.search(
                collection_name=CONFIG['collection'],
                query_vector=("dense", vector),
                limit=CONFIG['top_k_initial'],
                with_payload=True,
                score_threshold=0.3
            )
            
            return [{
                'score': hit.score,
                'law_name': hit.payload.get('law_name', 'Unknown'),
                'text': hit.payload.get('text_snippet', hit.payload.get('text', ''))
            } for hit in results]
        except Exception as e:
            logger.error(f"RAG Error: {e}")
            return []
    
    def build_context(self, results: List[Dict]) -> str:
        context = "===CONTEXTO LEGAL RAG===\n\n"
        for i, r in enumerate(results, 1):
            context += f"[{i}] {r['law_name']} (relevancia: {r['score']:.3f})\n"
            context += f"{r['text']}\n\n"
        return context
    
    def call_vps(self, question: str, context: str, options: List[str], q_id: int) -> Dict:
        """Llamada VPS con retry logic"""
        payload = {
            "question": question,
            "context": context,
            "options": {chr(97+i): opt for i, opt in enumerate(options)}
        }
        
        max_retries = 2
        for attempt in range(max_retries):
            try:
                logger.info(f"   🧠 VPS request (attempt {attempt+1}/{max_retries})...")
                response = requests.post(
                    "http://electroyhogarpelotazo.tienda/salamandra/reason",
                    json=payload,
                    timeout=CONFIG['timeout']
                )
                response.raise_for_status()
                
                data = response.json()
                reasoning_str = data.get('reasoning', '{}')
                
                try:
                    reasoning = json.loads(reasoning_str.replace('```json', '').replace('```', '').strip())
                    selected = reasoning.get('selected_option', '?')
                except:
                    selected = '?'
                
                logger.info(f"   ✅ VPS response: {selected}")
                
                return {
                    'question_id': q_id,
                    'selected_option': selected,
                    'confidence': 0.9 if selected != '?' else 0.0,
                    'reasoning': reasoning_str
                }
                
            except requests.exceptions.Timeout:
                logger.error(f"   ⏱️ VPS timeout (attempt {attempt+1})")
                if attempt == max_retries - 1:
                    return {
                        'question_id': q_id,
                        'selected_option': '?',
                        'confidence': 0.0,
                        'error': 'timeout_all_retries'
                    }
                time.sleep(10)
            except Exception as e:
                logger.error(f"   ❌ VPS error: {e}")
                if attempt == max_retries - 1:
                    return {
                        'question_id': q_id,
                        'selected_option': '?',
                        'confidence': 0.0,
                        'error': str(e)
                    }
                time.sleep(10)
    
    def answer_question(self, question: str, options: List[str], q_id: int, total: int) -> Dict:
        """Pipeline completo con logging detallado"""
        logger.info(f"\n{'='*80}")
        logger.info(f"PREGUNTA #{q_id}/{total}")
        logger.info(f"{'='*80}")
        logger.info(f"Q: {question[:80]}...")
        
        start_time = time.time()
        
        # RAG
        logger.info(f"   🔍 RAG búsqueda...")
        rag_results = self.search_rag(question)
        logger.info(f"   ✅ RAG: {len(rag_results)} resultados")
        
        # Context
        context = self.build_context(rag_results)
        
        # VPS
        result = self.call_vps(question, context, options, q_id)
        
        # Metadata
        elapsed = time.time() - start_time
        result['rag_sources'] = [f"{r['law_name']} ({r['score']:.3f})" for r in rag_results[:3]]
        result['time_seconds'] = round(elapsed, 1)
        
        logger.info(f"✅ Respuesta: {result.get('selected_option', '?')} (en {elapsed:.1f}s)")
        
        return result
    
    def save_checkpoint(self, current_id: int, results: List[Dict]):
        """Guardar checkpoint para recuperación"""
        checkpoint = {
            'last_completed': current_id,
            'timestamp': datetime.now().isoformat(),
            'total_processed': len(results)
        }
        with open(CONFIG['checkpoint_file'], 'w') as f:
            json.dump(checkpoint, f)
    
    def load_checkpoint(self) -> int:
        """Cargar último checkpoint"""
        try:
            with open(CONFIG['checkpoint_file'], 'r') as f:
                data = json.load(f)
                return data.get('last_completed', 0)
        except:
            return 0

def main():
    OUTPUT_FILE = BASE_DIR / "staging_area/06_01_26_enrichment/salamandra_examen_enero25_COMPLETO.jsonl"
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Cargar preguntas
    with open('/tmp/todas_preguntas_enero25.json', 'r') as f:
        all_questions = json.load(f)
    
    logger.info(f"📝 Total preguntas: {len(all_questions)}")
    
    agent = SalamandraExamen()
    
    # Checkpoint recovery
    last_completed = agent.load_checkpoint()
    if last_completed > 0:
        logger.info(f"⚠️ Recuperando desde pregunta #{last_completed+1}")
    
    # Procesar todas
    results = []
    with open(OUTPUT_FILE, 'a') as f_out:  # Append mode
        for q in all_questions:
            if q['id'] <= last_completed:
                continue  # Skip ya completadas
            
            try:
                result = agent.answer_question(
                    q['question'],
                    q['options'],
                    q['id'],
                    len(all_questions)
                )
                results.append(result)
                f_out.write(json.dumps(result, ensure_ascii=False) + '\n')
                f_out.flush()  # Flush inmediato
                
                # Checkpoint cada 5 preguntas
                if q['id'] % 5 == 0:
                    agent.save_checkpoint(q['id'], results)
                    logger.info(f"💾 Checkpoint guardado: {q['id']}/{len(all_questions)}")
                
            except Exception as e:
                logger.error(f"💥 Error crítico en pregunta #{q['id']}: {e}")
                # Guardar error y continuar
                error_result = {
                    'question_id': q['id'],
                    'selected_option': '?',
                    'error': f'critical_{str(e)[:50]}'
                }
                f_out.write(json.dumps(error_result, ensure_ascii=False) + '\n')
                f_out.flush()
    
    logger.info(f"\n{'='*80}")
    logger.info(f"✅ EXAMEN COMPLETADO")
    logger.info(f"📊 Total preguntas procesadas: {len(results)}")
    logger.info(f"📁 Output: {OUTPUT_FILE}")
    logger.info(f"{'='*80}")

if __name__ == "__main__":
    main()
