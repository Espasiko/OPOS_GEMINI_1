#!/usr/bin/env python3
"""
Salamandra Reasoner FINAL - Versión correcta
- RAG: Qdrant directo + embeddings locales
- VPS: FastAPI electroyhogarpelotazo.tienda (formato question/context/options)
"""

import os
import json
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Config
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
INPUT_FILE = BASE_DIR / "staging_area/05_01_26_exams_processing/smart_paired_exams_cleaned.jsonl"
OUTPUT_FILE = BASE_DIR / "staging_area/06_01_26_enrichment/salamandra_reasoning.jsonl"
ENV_FILE = BASE_DIR / "backend/.env.backend"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("salamandra")

def load_env():
    load_dotenv(ENV_FILE)
    return os.getenv("QDRANT_URL"), os.getenv("QDRANT_API_KEY")

class SalamandraAgent:
    def __init__(self):
        qdrant_url, qdrant_key = load_env()
        
        logger.info("Init Salamandra Agent (RAG + VPS)...")
        # Qdrant
        self.qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_key)
        self.collection = "opositaia_knowledge"
        
        # Embeddings
        logger.info("  Loading embeddings model...")
        self.embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
        
        # VPS FastAPI endpoint
        self.vps_url = "http://electroyhogarpelotazo.tienda/salamandra/reason"
        logger.info(f"  VPS: {self.vps_url}")
        
    def retrieve_context(self, query):
        """RAG search in Qdrant"""
        vector = self.embedder.encode(query).tolist()
        
        # Qdrant Cloud usa vector DEFAULT (unnamed), no named vector "dense"
        hits = self.qdrant.search(
            collection_name=self.collection,
            query_vector=vector,  # Vector directo, NO tupla ('dense', vector)
            limit=5,
            with_payload=True
        )
        
        context_text = ""
        for hit in hits:
            law = hit.payload.get('law_name', 'Unknown')
            art = hit.payload.get('article_title', '')
            text = hit.payload.get('text_snippet', hit.payload.get('text', ''))
            
            context_text += f"-- SOURCE: {law} | {art} --\n{text}\n\n"
            
        return context_text

    def reason(self, question, context, options):
        """Call VPS FastAPI (format: question/context/options)"""
        payload = {
            "question": question,
            "context": context,
            "options": options
        }
        
        try:
            logger.info("      -> WAIT VPS (timeout 300s)...")
            r = requests.post(self.vps_url, json=payload, timeout=300)
            r.raise_for_status()
            data = r.json()
            
            # VPS returns {"reasoning": "<json_string>"}
            return data.get("reasoning", "{}")
            
        except Exception as e:
            logger.error(f"      ERROR VPS: {e}")
            return None

def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    agent = SalamandraAgent()
    processed = 0
    MAX_EXAMS = 2  # Test

    with open(INPUT_FILE, 'r') as f_in, open(OUTPUT_FILE, 'w') as f_out:
        for line in f_in:
            if processed >= MAX_EXAMS:
                break
                
            exam = json.loads(line)
            filename = exam['filename']
            questions = exam['content']
            
            logger.info(f"Processing exam: {filename}")
            
            for q in questions:
                if not q.get('options') or len(q['options']) < 2:
                    continue
                
                q_text = q['text']
                q_options = q['options']
                q_num = q['number']
                
                logger.info(f"  Q{q_num}: RAG search...")
                
                # 1. RAG
                try:
                    context = agent.retrieve_context(q_text)
                    logger.info(f"  Q{q_num}: RAG OK - {len(context)} chars")
                except Exception as e:
                    logger.error(f"  Q{q_num}: RAG ERROR - {e}")
                    context = ""
                
                # 2. VPS Reason
                logger.info(f"  Q{q_num}: Sending to VPS...")
                response = agent.reason(q_text, context, q_options)
                
                if response:
                    try:
                        clean = response.replace("```json", "").replace("```", "").strip()
                        analysis = json.loads(clean)
                        
                        record = {
                            "exam_filename": filename,
                            "question_number": q_num,
                            "salamandra_output": analysis,
                            "rag_context_dump": context,
                            "model_used": "salamandra-vps-rag"
                        }
                        
                        f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
                        f_out.flush()
                        logger.info(f"  Q{q_num}: SAVED")
                        
                    except Exception as e:
                        logger.error(f"  Q{q_num}: JSON parse error - {e}")
                else:
                    logger.warning(f"  Q{q_num}: No VPS response")
                    
            processed += 1

    logger.info(f"DONE - Output: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
