#!/usr/bin/env python3
"""
Script modificado para usar Ollama API DIRECTA (sin FastAPI wrapper)
Timeout: 600s (10 min)
Modelo: salamandra-opos:optimized (num_ctx=2048)
"""
import os
import sys
import json
import logging
import requests
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/salamandra_ultra.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SalamandraULTRA")

# === CONFIG ===
CONFIG = {
    # RAG
    "qdrant_url": "http://localhost:6333",
    "collection": "opositaia_knowledge_hybrid_FULL",
    "top_k_initial": 10,  # Reducido de 30 a 10
    "top_k_final": 10,    # Reducido de 10 a 10 (todos)
    
    # LLM Salamandra - OLLAMA API DIRECTA
    "ollama_url": "http://electroyhogarpelotazo.tienda:11434/api/chat",
    "model_name": "salamandra-opos:optimized",
    "timeout": 900,  # 15 minutos
    
    # MCP
    "mcp_url": "http://127.0.0.1:3100",
    
    # Cohere
    "cohere_api_key": os.getenv("COHERE_API_KEY"),
    "cohere_model": "rerank-multilingual-v3.0",
    
    # Temporal
    "exam_reference_date": "2024-12-30",
}

class SalamandraULTRA:
    def __init__(self):
        logger.info("="*80)
        logger.info("🔥 SALAMANDRA ULTRA - Init...")
        logger.info("="*80)
        
        # Qdrant
        self.qdrant = QdrantClient(url=CONFIG['qdrant_url'], timeout=120.0)
        
        # Embedder
        self.embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
        
        logger.info(f"✅ RAG Local: {CONFIG['qdrant_url']}")
        logger.info(f"✅ Ollama: {CONFIG['ollama_url']}")
        logger.info(f"✅ Modelo: {CONFIG['model_name']}")
        logger.info(f"✅ Timeout: {CONFIG['timeout']}s\n")
    
    def search_rag(self, query: str, limit: int = 30) -> List[Dict]:
        """RAG Search"""
        logger.info(f"   🔍 RAG: '{query[:50]}...' (limit={limit})")
        
        try:
            vector = self.embedder.encode(query).tolist()
            
            results = self.qdrant.search(
                collection_name=CONFIG['collection'],
                query_vector=("dense", vector),
                limit=limit,
                with_payload=True,
                score_threshold=0.3
            )
            
            formatted = []
            for hit in results:
                formatted.append({
                    'score': hit.score,
                    'law_name': hit.payload.get('law_name', 'Unknown'),
                    'text': hit.payload.get('text_snippet', hit.payload.get('text', ''))
                })
            
            logger.info(f"   ✅ RAG: {len(formatted)} resultados")
            return formatted
        except Exception as e:
            logger.error(f"   ❌ RAG Error: {e}")
            return []
    
    def build_context(self, results: List[Dict]) -> str:
        """Build RAG context"""
        context = "===CONTEXTO LEGAL RAG===\n\n"
        for i, r in enumerate(results, 1):
            context += f"[{i}] {r['law_name']} (relevancia: {r['score']:.3f})\n"
            context += f"{r['text']}\n\n"
        return context
    
    def call_ollama(self, question: str, context: str, options: List[str], q_id: int) -> Dict:
        """Call FastAPI /salamandra/reason endpoint"""
        
        # Build payload for FastAPI endpoint
        payload = {
            "question": question,
            "context": context,
            "options": {chr(97+i): opt for i, opt in enumerate(options)}  # Dict format
        }
        
        try:
            logger.info(f"   🧠 FastAPI /salamandra/reason...")
            response = requests.post(
                "http://electroyhogarpelotazo.tienda/salamandra/reason",
                json=payload,
                timeout=CONFIG['timeout']
            )
            response.raise_for_status()
            
            data = response.json()
            reasoning_str = data.get('reasoning', '{}')
            
            # Parse reasoning JSON
            try:
                reasoning = json.loads(reasoning_str.replace('```json', '').replace('```', '').strip())
                selected = reasoning.get('selected_option', '?')
            except:
                selected = '?'
            
            logger.info(f"   ✅ FastAPI response: {selected}")
            
            return {
                'question_id': q_id,
                'selected_option': selected,
                'confidence': 0.9 if selected != '?' else 0.0,
                'reasoning': reasoning_str
            }
            
        except requests.exceptions.Timeout:
            logger.error (f"   ❌ FastAPI timeout ({CONFIG['timeout']}s)")
            return {
                'question_id': q_id,
                'selected_option': '?',
                'confidence': 0.0,
                'error': f'timeout_{CONFIG["timeout"]}s'
            }
        except Exception as e:
            logger.error(f"   ❌ FastAPI error: {e}")
            return {
                'question_id': q_id,
                'selected_option': '?',
                'confidence': 0.0,
                'error': str(e)
            }

    
    def answer_question(self, question: str, options: List[str], q_id: int) -> Dict:
        """Pipeline completo"""
        logger.info(f"\n{'='*80}")
        logger.info(f"PREGUNTA #{q_id}")
        logger.info(f"{'='*80}")
        logger.info(f"Q: {question[:60]}...")
        
        # RAG
        rag_results = self.search_rag(question, limit=CONFIG['top_k_initial'])
        
        # Build context
        context = self.build_context(rag_results[:CONFIG['top_k_final']])
        
        # Ollama
        result = self.call_ollama(question, context, options, q_id)
        
        # Metadata
        result['rag_sources'] = [
            f"{r['law_name']} (score: {r['score']:.3f})"
            for r in rag_results[:3]
        ]
        
        logger.info(f"✅ Respuesta: {result.get('selected_option', '?')}")
        logger.info(f"   Confianza: {result.get('confidence', 0):.2%}")
        
        return result

def main():
    OUTPUT_FILE = BASE_DIR / "staging_area/06_01_26_enrichment/salamandra_ultra_enero25.jsonl"
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Test con 1 pregunta
    test_questions = [
        {
            'id': 1,
            'question': "Según el artículo 174 del Texto Refundido de la Ley General de la Seguridad Social, el derecho al subsidio por Incapacidad temporal se extingue:",
            'options': [
                "por el transcurso del plazo máximo de trescientos sesenta y cinco días naturales desde la baja médica",
                "por el transcurso del plazo máximo de quinientos cuarenta y cinco días naturales desde la baja médica",
                "por el transcurso del plazo de trescientos sesenta días desde el alta médica",
                "por el transcurso del plazo máximo de ciento ochenta días desde la notificación de la baja médica"
            ]
        }
    ]
    
    agent = SalamandraULTRA()
    
    with open(OUTPUT_FILE, 'w') as f_out:
        for q in test_questions:
            result = agent.answer_question(
                q['question'],
                q['options'],
                q['id']
            )
            f_out.write(json.dumps(result, ensure_ascii=False) + '\\n')
    
    logger.info(f"\n✅ Completado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
