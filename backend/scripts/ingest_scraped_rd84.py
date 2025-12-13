#!/usr/bin/env python3
"""
Specific Ingestion Script for RD 84/1996 using SCRAPED Markdown content.
This bypasses the faulty BOE API for this specific law.
"""
import os
import sys
import uuid
import logging
import psycopg2
import re
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "opositaia")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

COLLECTION_NAME = "opositaia_knowledge"
MODEL_NAME = "pablosi/bge-m3-spa-law-qa-trained-2"
VECTOR_SIZE = 1024

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SCRAPED_FILE = "backend/data/RD_84_1996_scraped.md"
LAW_METADATA = {
    "id": "BOE-A-1996-4447", 
    "nombre": "Real Decreto 84/1996 - Reglamento General de Afiliación",
    "titulo": "Real Decreto 84/1996, de 26 de enero, por el que se aprueba el Reglamento General sobre inscripción de empresas y afiliación, altas, bajas y variaciones de datos de trabajadores en la Seguridad Social."
}

class ScrapedIngester:
    def __init__(self):
        logger.info("Initializing Scraped Content Ingester...")
        
        self.qdrant = QdrantClient(url=QDRANT_URL)
        self.db_conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASSWORD
        )
        self.db_cursor = self.db_conn.cursor()
        self.model = SentenceTransformer(MODEL_NAME)
        
        logger.info("✅ All connections ready")
    
    def parse_markdown_law(self, file_path):
        """
        Parses the scraped markdown into logical chunks (Articles/Headings).
        Assumes structure: 
        # Title
        ## Heading/Article
        Text...
        """
        chunks = []
        current_chunk = {"title": "", "content": []}
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("# "):
                # Main Title - skip or handle separately
                continue
            
            if line.startswith("## "):
                # New Section/Article
                if current_chunk["title"] or current_chunk["content"]:
                    chunks.append({
                        "id": current_chunk["title"][:50].replace(" ", "_"), # simple ID gen
                        "title": current_chunk["title"],
                        "text": "\n".join(current_chunk["content"])
                    })
                
                current_chunk = {
                    "title": line.replace("## ", ""), 
                    "content": []
                }
            else:
                current_chunk["content"].append(line)
        
        # Append last chunk
        if current_chunk["title"] or current_chunk["content"]:
             chunks.append({
                "id": current_chunk["title"][:50].replace(" ", "_"),
                "title": current_chunk["title"],
                "text": "\n".join(current_chunk["content"])
            })
            
        return chunks

    def ingest(self):
        law_id = LAW_METADATA['id']
        nombre = LAW_METADATA['nombre']
        
        logger.info(f"Ingesting: {nombre}")
        
        # 1. Parse content
        chunks = self.parse_markdown_law(SCRAPED_FILE)
        logger.info(f"✅ Parsed {len(chunks)} logical chunks from markdown")
        
        # 2. Save Document Root (Layer 1)
        doc_id = f"{law_id}-document"
        
        # Insert metadata into Postgres
        try:
            self.db_cursor.execute("""
                INSERT INTO laws (id, law_id, law_name, title, content, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (doc_id, law_id, nombre, LAW_METADATA['titulo'], LAW_METADATA['titulo'], datetime.now()))
            self.db_conn.commit()
        except Exception as e:
            logger.warning(f"Metadata insertion warning: {e}")
            self.db_conn.rollback()

        # Vectorize chunks
        points = []
        for i, chunk in enumerate(chunks):
            chunk_text = chunk["text"]
            chunk_title = chunk["title"]
            
            if len(chunk_text) < 20: 
                continue
                
            full_text = f"{chunk_title}\n{chunk_text}"
            
            # IDs
            article_id = f"{law_id}-chunk_{i}"
            qdrant_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, article_id))
            
            # Embedding
            embedding = self.model.encode(full_text).tolist()
            
            # Postgres (Text Store)
            try:
                self.db_cursor.execute("""
                    INSERT INTO laws (id, law_id, law_name, title, content, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET content = EXCLUDED.content;
                """, (article_id, law_id, nombre, chunk_title, full_text, datetime.now()))
            except Exception as e:
                logger.error(f"Postgres insert error: {e}")
                self.db_conn.rollback()
            
            # Qdrant (Vector Store)
            points.append(models.PointStruct(
                id=qdrant_id,
                vector={"dense": embedding},
                payload={
                    "layer": "article_chunk",
                    "boe_id": law_id,
                    "law_name": nombre,
                    "chunk_index": i,
                    "title": chunk_title,
                    "text": chunk_text[:1000], # Limit text payload in Qdrant (Hybrid approach)
                    "is_scraped": True
                }
            ))
            
            if len(points) >= 20:
                self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
                self.db_conn.commit()
                logging.info(f"  Inserted batch of {len(points)} chunks")
                points = []

        if points:
            self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
            self.db_conn.commit()
            logging.info(f"  Inserted final batch of {len(points)} chunks")
            
        logger.info(f"✅ Ingestion complete for {nombre}")

    def close(self):
        self.db_cursor.close()
        self.db_conn.close()

if __name__ == "__main__":
    ingester = ScrapedIngester()
    try:
        ingester.ingest()
    finally:
        ingester.close()
