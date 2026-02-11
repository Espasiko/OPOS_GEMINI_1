
import json
import os
import time
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Configuración
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
STAGING_DIR = BASE_DIR / "staging_area/05_01_26_exams_processing"
ENRICHMENT_DIR = BASE_DIR / "staging_area/06_01_26_enrichment"
INPUT_FILE = STAGING_DIR / "smart_paired_exams_cleaned.jsonl"
OUTPUT_FILE = ENRICHMENT_DIR / "salamandra_reasoning.jsonl"
ENV_FILE = BASE_DIR / "backend/.env.backend"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("salamandra_reasoner")

def load_env():
    load_dotenv(ENV_FILE)
    qdrant_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL") 
    mistral_url = os.getenv("MISTRAL_URL", "http://147.93.95.67:8080")
    
    if not qdrant_key or not qdrant_url:
        raise ValueError("QDRANT cloud credentials missing in .env")
        
    return qdrant_url, qdrant_key, mistral_url

class SalamandraAgent:
    def __init__(self):
        url, key, mistral_url = load_env()
        
        logger.info("🦕 Inicializando Salamandra (RAG + VPS)...")
        # 1. Qdrant
        self.qdrant = QdrantClient(url=url, api_key=key)
        self.collection = "opositaia_knowledge"
        
        # 2. Embedding Model (Local)
        logger.info("   -> Cargando modelo de embeddings (bge-m3)...")
        self.embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
        
        # VPS Endpoint (Domain + FastAPI salamandra endpoint)
        self.vps_url = "http://electroyhogarpelotazo.tienda/salamandra/reason"
        logger.info(f"   -> VPS Endpoint: {self.vps_url}")

        
    def retrieve_context(self, query):
        """Busca chunks relevantes en Qdrant (Vector 'dense')"""
        vector = self.embedder.encode(query).tolist()
        
        # Usamos search con tupla para vector nombrado ('dense', vector)
        hits = self.qdrant.search(
            collection_name=self.collection,
            query_vector=("dense", vector), 
            limit=5 
        )
        
        context_text = ""
        for hit in hits:
            # Construir cita rica
            law_name = hit.payload.get('law_name', 'Ley desconocida')
            art_title = hit.payload.get('article_title', '')
            content = hit.payload.get('text_snippet', hit.payload.get('text', ''))
            
            context_text += f"-- FUENTE: {law_name} | {art_title} --\n{content}\n\n"
            
        return context_text

    def reason(self, question_text, context):
        """Llama al LLM del VPS con contexto y Prompt Mejorado"""
        
        system_prompt = """Eres 'Salamandra', un Asistente Jurídico de Alto Nivel especializado en Oposiciones Españolas.
Tu objetivo es resolver preguntas de examen tipo test con PRECISIÓN QUIRÚRGICA, basándote EXCLUSIVAMENTE en el contexto legal proporcionado.

INSTRUCCIONES DE RAZONAMIENTO (Chain of Thought):
1. ANÁLISIS PREVIO: Lee la pregunta y las opciones.
2. BUSQUEDA DE EVIDENCIA: Escanea el CONTEXTO LEGAL aportado en busca de frases exactas o principios que confirmen o refuten cada opción.
3. DESCARTE: Explica por qué las opciones incorrectas fallan (e.g., "La opción B dice 3 meses, pero la ley dice 6").
4. CONCLUSIÓN: Selecciona la opción correcta sin dudas.

FORMATO DE SALIDA (JSON PURO):
Debes generar ÚNICAMENTE un objeto JSON válido. No incluyas markdown (```json) ni texto adicional.
Estructura:
{
  "thought_process": "Escribe aquí tu razonamiento interno detallado. Cita textualmente el artículo de ley que usas...",
  "selected_option": "a", 
  "rag_context_used": true,
  "analysis": {
     "a": "Correcta/Incorrecta porque...",
     "b": "Correcta/Incorrecta porque...",
     "c": "Correcta/Incorrecta porque...",
     "d": "Correcta/Incorrecta porque..."
  }
}
"""
        user_msg = f"""### CONTEXTO LEGAL (RAG):
{context}

### PREGUNTA DE EXAMEN:
{question_text}

Analiza, razona y responde:
"""

        payload = {
            "model": "salamandra-opos:latest", 
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            "temperature": 0.1, 
            "max_tokens": 1000,
            "response_format": {"type": "json_object"}
        }
        
        try:
            logger.info("      -> ⏳ Esperando respuesta VPS (Timeout 300s)...")
            r = requests.post(self.vps_url, json=payload, timeout=300) # 5 minutos
            r.raise_for_status()
            data = r.json()
            return data['choices'][0]['message']['content']
        except requests.exceptions.Timeout:
            logger.error("❌ VPS TIMEOUT (300s) - El modelo tardó demasiado.")
            return None
        except Exception as e:
            logger.error(f"❌ Error llamando VPS: {e}")
            if 'r' in locals() and r:
                 logger.error(f"Response: {r.text}")
            return None

def main():
    try:
        agent = SalamandraAgent()
        ENRICHMENT_DIR.mkdir(parents=True, exist_ok=True)
    
        processed_exams = 0
        MAX_EXAMS = 2
        
        with open(INPUT_FILE, "r") as f_in, open(OUTPUT_FILE, "w") as f_out:
            for line in f_in:
                if processed_exams >= MAX_EXAMS:
                    break
                    
                exam_data = json.loads(line)
                filename = exam_data['filename']
                questions = exam_data['content']
                
                logger.info(f"🦕 Procesando Examen con Salamandra: {filename}")
                
                for q in questions:
                    if not q.get('options') or len(q['options']) < 2:
                        continue
                    
                    logger.info(f"   -> Q{q['number']}: RAG Search...")
                    # Solo texto pregunta para embedding (sin opciones)
                    question_text = q['text']
                    options_dict = q['options']
                    
                    # 1. RAG Retrieve
                    try:
                        context = agent.retrieve_context(question_text) 
                        logger.info(f"   -> Q{q['number']}: RAG OK. Context len: {len(context)}")
                    except Exception as e:
                        logger.error(f"   ❌ Error RAG Q{q['number']}: {e}")
                        context = ""

                    # 2. Reason (VPS FastAPI format: question/context/options)
                    logger.info(f"   -> Q{q['number']}: Sending to VPS FastAPI...")
                    json_response = agent.reason(question_text, context, options_dict)
                    
                    if json_response:
                        try:
                            clean = json_response.replace("```json", "").replace("```", "").strip()
                            analysis = json.loads(clean)
                            
                            record = {
                                "exam_filename": filename,
                                "question_number": q['number'],
                                "salamandra_output": analysis,
                                "rag_context_dump": context,
                                "model_used": "salamandra-vps-rag"
                            }
                            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
                            f_out.flush()
                            logger.info(f"   ✅ Q{q['number']} Guardada.")
                            
                        except:
                            logger.error(f"   ❌ Error parseando JSON Salamandra Q{q['number']}")
                    else:
                        logger.warning(f"   ⚠️ Q{q['number']} Sin respuesta del VPS.")
                            
                    # time.sleep(1) # Relax VPS (Eliminado para ir a tope, el timeout nos protege)
                    
                processed_exams += 1
    except Exception as fatal:
        logger.critical(f"☠️ FATAL ERROR EN MAIN: {fatal}", exc_info=True)

    logger.info(f"✅ Proceso Salamandra terminado. Resultados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
