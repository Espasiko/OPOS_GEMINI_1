#!/usr/bin/env python3
"""
Universal Ingestion Script for Scraped Markdown Laws.
Usage: python ingest_scraped_universal.py <MD_FILE_PATH> <BOE_ID>
"""
import os
import sys
import uuid
import logging
import psycopg2
import argparse
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UniversalIngester:
    def __init__(self):
        logger.info("Initializing Universal Scraped Content Ingester...")
        self.qdrant = QdrantClient(url=QDRANT_URL, check_compatibility=False)
        self.db_conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASSWORD
        )
        self.db_cursor = self.db_conn.cursor()
        self.model = SentenceTransformer(MODEL_NAME) # device='cpu' implicit
        logger.info("✅ All connections ready")
    
    def parse_markdown_law(self, file_path):
        """
        Parses the scraped markdown into logical chunks.
        """
        chunks = []
        current_chunk = {"title": "", "content": []}
        law_title = ""
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("# "):
                law_title = line.replace("# ", "")
                continue
            
            if line.startswith("## "):
                # Save previous chunk
                if current_chunk["title"] or current_chunk["content"]:
                    chunks.append({
                        "title": current_chunk["title"],
                        "text": "\n".join(current_chunk["content"])
                    })
                
                # Start new chunk
                current_chunk = {
                    "title": line.replace("## ", ""), 
                    "content": []
                }
            else:
                current_chunk["content"].append(line)
        
        # Append last chunk
        if current_chunk["title"] or current_chunk["content"]:
             chunks.append({
                "title": current_chunk["title"],
                "text": "\n".join(current_chunk["content"])
            })
            
        return law_title, chunks

    def ingest(self, file_path, boe_id):
        logger.info(f"🚀 Starting ingestion for {boe_id} from {file_path}")
        
        # 1. Parse content
        law_title, chunks = self.parse_markdown_law(file_path)
        if not law_title:
            law_title = f"Ley {boe_id}" # Fallback
            
        logger.info(f"   Law Title: {law_title}")
        logger.info(f"   Parsed {len(chunks)} chunks")
        
        # 2. Save Document Root (Layer 1)
        doc_id = f"{boe_id}-document"
        
        try:
            self.db_cursor.execute("""
                INSERT INTO laws (id, law_id, law_name, title, content, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (doc_id, boe_id, law_title, law_title, law_title, datetime.now()))
            self.db_conn.commit()
            logger.info("✅ Document root saved to Postgres")
        except Exception as e:
            logger.error(f"❌ Postgres Metadata Error: {e}")
            self.db_conn.rollback()

        # 3. Vectorize and Insert Chunks
        points = []
        for i, chunk in enumerate(chunks):
            chunk_text = chunk["text"]
            chunk_title = chunk["title"]
            
            if len(chunk_text) < 20: 
                continue
                
            full_text = f"{chunk_title}\n{chunk_text}"
            
            # IDs
            article_id = f"{boe_id}-chunk_{i}"
            qdrant_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, article_id))
            
            # Embedding
            embedding = self.model.encode(full_text).tolist()
            
            # Postgres (Text Store)
            try:
                self.db_cursor.execute("""
                    INSERT INTO laws (id, law_id, law_name, title, content, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET content = EXCLUDED.content;
                """, (article_id, boe_id, law_title, chunk_title, full_text, datetime.now()))
            except Exception as e:
                logger.error(f"Postgres Chunk Error: {e}")
                self.db_conn.rollback()
            
            # Qdrant (Vector Store)
            points.append(models.PointStruct(
                id=qdrant_id,
                vector={"dense": embedding},
                payload={
                    "layer": "article_chunk",
                    "boe_id": boe_id,
                    "law_name": law_title,
                    "chunk_index": i,
                    "title": chunk_title,
                    "text": chunk_text[:1200], # Limit text payload
                    "is_scraped": True
                }
            ))
            
            if len(points) >= 20:
                self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
                self.db_conn.commit()
                logger.info(f"   Batch upserted: {len(points)} chunks")
                points = []

        if points:
            self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
            self.db_conn.commit()
            logger.info(f"   Final batch upserted: {len(points)} chunks")
            
        logger.info(f"✅ Ingestion COMPLETE for {boe_id}")

    def close(self):
        self.db_cursor.close()
        self.db_conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Scraped Markdown Ingestor")
    parser.add_argument("file_path", help="Path to scraped markdown file")
    parser.add_argument("boe_id", help="BOE Identifier (e.g., BOE-A-2015-10438)")
    args = parser.parse_args()

    ingester = UniversalIngester()
    try:
        ingester.ingest(args.file_path, args.boe_id)
    finally:
        ingester.close()
