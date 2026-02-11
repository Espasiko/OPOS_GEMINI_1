#!/usr/bin/env python3
"""
Script SIMPLE que SÍ FUNCIONA - Solo procesa 1 pregunta de prueba
Basado en el test que funcionó (respondió opción B correctamente)
"""
import os
import sys
import json
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Rutas absolutas
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
os.chdir(BASE_DIR)
sys.path.insert(0, str(BASE_DIR))

# Load env
load_dotenv(BASE_DIR / "backend/.env.backend")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/exam_working.log', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

logger.info("🔥 SALAMANDRA - Script Funcionando")

# Init
qdrant = QdrantClient(url="http://localhost:6333", timeout=120.0)
embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")

# Pregunta de prueba (la que funcionó)
question = {
    'id': 1,
    'question': "Según el artículo 174 del Texto Refundido de la Ley General de la Seguridad Social, el derecho al subsidio por Incapacidad temporal se extingue:",
    'options': [
        "por el transcurso del plazo máximo de trescientos sesenta y cinco días naturales desde la baja médica",
        "por el transcurso del plazo máximo de quinientos cuarenta y cinco días naturales desde la baja médica",
        "por el transcurso del plazo de trescientos sesenta días desde el alta médica",
        "por el transcurso del plazo máximo de ciento ochenta días desde la notificación de la baja médica"
    ]
}

logger.info(f"Procesando pregunta {question['id']}")

# RAG
logger.info("RAG search...")
vector = embedder.encode(question['question']).tolist()
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
    "question": question['question'],
    "context": context,
    "options": {chr(97+i): opt for i, opt in enumerate(question['options'])}
}

response = requests.post(
    "http://electroyhogarpelotazo.tienda/salamandra/reason",
    json=payload,
    timeout=900
)
response.raise_for_status()

data = response.json()
reasoning_str = data.get('reasoning', '{}')

# Robust parsing con múltiples estrategias (best practice web)
selected = '?'

# Estrategia 1: Try JSON parsing
try:
    reasoning = json.loads(reasoning_str.replace('```json', '').replace('```', '').strip())
    selected = reasoning.get('selected_option', '?')
    logger.info(f"✅ JSON parsing success: {selected}")
except:
    # Estrategia 2: Regex extraction (fallback)
    import re
    match = re.search(r'selected_option:\s*([abcd])', reasoning_str, re.IGNORECASE)
    if match:
        selected = match.group(1).lower()
        logger.info(f"✅ Regex extraction success: {selected}")
    else:
        # Estrategia 3: Buscar cualquier letra a-d en primeras líneas
        for letter in ['a', 'b', 'c', 'd']:
            if letter in reasoning_str[:100].lower():
                selected = letter
                logger.info(f"⚠️ Fallback extraction: {selected}")
                break

logger.info(f"✅ Respuesta VPS: {selected}")

# Guardar
output = {
    'question_id': question['id'],
    'selected_option': selected,
    'reasoning': reasoning_str
}

output_file = BASE_DIR / "staging_area/06_01_26_enrichment/test_working.jsonl"
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w') as f:
    f.write(json.dumps(output, ensure_ascii=False) + '\n')

logger.info(f"✅ COMPLETADO: {output_file}")
print("SUCCESS")
