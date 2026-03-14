import os
import uuid
import logging
from pathlib import Path
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
import bs4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"

def ingest_stc():
    client = QdrantClient(url=QDRANT_URL, timeout=120)
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    html_path = Path("/home/spas/OPOS_GEMINI_1/backend/scripts/stc_31_2010_REAL.html")
    if not html_path.exists():
        logger.error("❌ No se encontró el archivo HTML")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        soup = bs4.BeautifulSoup(f, "html.parser")
    
    # El BOE usa id="DOdocText" para el cuerpo del diario
    text_div = soup.find("div", id="DOdocText") or soup.find("div", id="textox") or soup.find("div", class_="bloque")
    if not text_div:
        logger.error("❌ No se encontró el contenido de la sentencia")
        return

    full_text = text_div.get_text(separator="\n").strip()
    
    # Chunking más agresivo para sentencias gigantes
    chunk_size = 3000
    overlap = 300
    chunks = []
    
    for i in range(0, len(full_text), chunk_size - overlap):
        chunk = full_text[i:i + chunk_size]
        if len(chunk) < 200: continue
        chunks.append(chunk)

    points = []
    boe_id = "BOE-A-2010-11409" # ID REAL DE LA STC 31/2010
    law_name = "Sentencia 31/2010 (Estatuto de Autonomía de Cataluña)"
    
    for i, text in enumerate(chunks):
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{boe_id}_chunk_{i}"))
        dense = model.encode(text).tolist()
        
        payload = {
            "boe_id": boe_id,
            "law_name": law_name,
            "article_title": f"Fundamento/Parte {i+1}",
            "text_snippet": text,
            "layer": "jurisprudence_chunk",
            "url_boe": f"https://www.boe.es/buscar/doc.php?id={boe_id}",
            "source": "manual_ingest_stc"
        }
        
        points.append(models.PointStruct(id=point_id, vector={"dense": dense}, payload=payload))

    client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
    logger.info(f"✅ STC 31/2010 indexada: {len(points)} chunks.")

if __name__ == "__main__":
    ingest_stc()
