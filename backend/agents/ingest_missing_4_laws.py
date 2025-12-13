#!/usr/bin/env python3
"""
Re-ingest the 4 missing laws that failed due to fallback chunking
- TREBEP (BOE-A-2015-10438)
- RD 84/1996 (BOE-A-1996-3981)
- RD 2064/1995 (BOE-A-1995-26497)
- RD 1415/2004 (BOE-A-2004-11607)
"""
import os
import sys
import uuid
import logging
import psycopg2
from typing import List
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup

try:
    from agents.boe_api_client import BOEApiClient
except ImportError:
    from boe_api_client import BOEApiClient

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://opositaia-qdrant:6333")
DB_HOST = os.getenv("POSTGRES_HOST", "opositaia-postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "opositaia")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

COLLECTION_NAME = "opositaia_knowledge"
MODEL_NAME = "pablosi/bge-m3-spa-law-qa-trained-2"
VECTOR_SIZE = 1024

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Only the 4 missing laws
MISSING_LAWS = [
    {"id": "BOE-A-2015-10438", "nombre": "TREBEP"},
    {"id": "BOE-A-1996-3981", "nombre": "RD 84/1996 - Afiliación"},
    {"id": "BOE-A-1995-26497", "nombre": "RD 2064/1995 - Cotización"},
    {"id": "BOE-A-2004-11607", "nombre": "RD 1415/2004 - Recaudación"},
]

class QuickIndexer:
    def __init__(self):
        logger.info("Initializing Quick Re-Indexer...")
        
        self.qdrant = QdrantClient(url=QDRANT_URL)
        self.db_conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASSWORD
        )
        self.db_cursor = self.db_conn.cursor()
        self.model = SentenceTransformer(MODEL_NAME)
        self.boe_client = BOEApiClient()
        
        logger.info("✅ All connections ready")
    
    def process_law(self, ley: dict):
        boe_id = ley['id']
        nombre = ley['nombre']
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Processing: {nombre} ({boe_id})")
        logger.info(f"{'='*80}")
        
        try:
            metadatos = self.boe_client.get_metadatos(boe_id)
            texto_xml = self.boe_client.get_texto_consolidado(boe_id)
            
            if not texto_xml:
                logger.error(f"❌ No XML content for {boe_id}")
                return
            
            titulo = metadatos.get('titulo', nombre)
            soup = BeautifulSoup(texto_xml, 'xml')
            articulos = soup.find_all('articulo')
            
            if not articulos:
                logger.warning(f"⚠️ No <articulo> tags. Using fallback chunking.")
                # Fallback: 1000 char chunks
                chunk_size = 1000
                texto_plano = soup.get_text(separator=" ", strip=True)
                articulos = [texto_plano[i:i+chunk_size] for i in range(0, len(texto_plano), chunk_size)]
                is_fallback = True
            else:
                logger.info(f"✅ Found {len(articulos)} articles")
                is_fallback = False
            
            # Save document metadata (Layer 1)
            doc_id = f"{boe_id}-document"
            self.db_cursor.execute("""
                INSERT INTO laws (id, law_id, law_name, title, content, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (doc_id, boe_id, nombre, titulo, titulo, datetime.now()))
            
            # Qdrant metadata
            qdrant_doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_id))
            self.qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=[models.PointStruct(
                    id=qdrant_doc_id,
                    vector={"dense": self.model.encode(titulo).tolist()},
                    payload={
                        "layer": "document",
                        "boe_id": boe_id,
                        "law_name": nombre,
                        "title": titulo,
                        "text": titulo,
                        "metadata": metadatos
                    }
                )]
            )
            logger.info(f"✅ Layer 1 saved")
            
            # Save articles/chunks (Layer 2)
            points = []
            for i, art in enumerate(articulos):
                if is_fallback:
                    art_text = art
                    art_id = f"chunk_{i}"
                else:
                    art_text = art.get_text(separator=" ", strip=True)
                    art_id = art.get('id', f"art_{i}")
                
                if len(art_text) < 50:
                    continue
                
                # PostgreSQL
                article_id = f"{boe_id}-{art_id}"
                self.db_cursor.execute("""
                    INSERT INTO laws (id, law_id, law_name, title, content, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET content = EXCLUDED.content;
                """, (article_id, boe_id, nombre, art_id, art_text, datetime.now()))
                
                # Qdrant
                chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, article_id))
                embedding = self.model.encode(art_text).tolist()
                
                points.append(models.PointStruct(
                    id=chunk_id,
                    vector={"dense": embedding},
                    payload={
                        "layer": "article_chunk",
                        "boe_id": boe_id,
                        "law_name": nombre,
                        "parent_id": qdrant_doc_id,
                        "chunk_index": i,
                        "article_id": art_id,
                        "text": art_text,
                        "is_smart_chunk": not is_fallback
                    }
                ))
                
                if len(points) >= 50:
                    self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
                    self.db_conn.commit()
                    logger.info(f"  ✅ Batch: {len(points)} articles")
                    points = []
            
            if points:
                self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
                self.db_conn.commit()
                logger.info(f"  ✅ Final batch: {len(points)} articles")
            
            logger.info(f"✅ COMPLETED: {nombre} ({len(articulos)} articles)")
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            self.db_conn.rollback()
    
    def close(self):
        self.db_cursor.close()
        self.db_conn.close()
        logger.info("✅ Closed")

def main():
    indexer = QuickIndexer()
    
    try:
        for ley in MISSING_LAWS:
            indexer.process_law(ley)
        
        logger.info("\n" + "#"*60)
        logger.info("# ✅ RE-INGESTION COMPLETE")
        logger.info("#"*60)
        
    finally:
        indexer.close()

if __name__ == "__main__":
    main()
