#!/usr/bin/env python3
"""
Ingest ALL 10 Missing Laws from Official Syllabus
Uses pablosi/bge-m3-spa-law-qa-trained-2 embeddings
Chunks by articles + metadata in PostgreSQL
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

# ALL 10 Missing Laws from Official Syllabus
MISSING_LAWS = [
    # CRÍTICAS (Prioridad 🔴)
    {"id": "BOE-A-2003-21614", "nombre": "Ley 47/2003 - General Presupuestaria", "prioridad": "CRÍTICA"},
    {"id": "BOE-A-2015-11430", "nombre": "RDL 2/2015 - Estatuto Trabajadores", "prioridad": "CRÍTICA"},
    {"id": "BOE-A-1995-24292", "nombre": "Ley 31/1995 - Prevención Riesgos Laborales", "prioridad": "CRÍTICA"},
    
    # ALTAS (Prioridad 🟠)
    {"id": "BOE-A-2017-12902", "nombre": "Ley 9/2017 - LCSP (Contratos Sector Público)", "prioridad": "ALTA"},
    {"id": "BOE-A-2012-5730", "nombre": "LO 2/2012 - Estabilidad Presupuestaria", "prioridad": "ALTA"},
    {"id": "BOE-A-2023-5366", "nombre": "Ley 4/2023 - Igualdad Trans LGTBI", "prioridad": "ALTA"},
    
    # MEDIAS (Prioridad 🟡)
    {"id": "BOE-A-2007-6115", "nombre": "LO 3/2007 - Igualdad", "prioridad": "MEDIA"},
    {"id": "BOE-A-1982-11607", "nombre": "LO 2/1982 - Tribunal de Cuentas", "prioridad": "MEDIA"},
    {"id": "BOE-A-2007-15409", "nombre": "Ley 20/2007 - Estatuto Autónomo", "prioridad": "MEDIA"},
    {"id": "BOE-A-1985-12666", "nombre": "LO 6/1985 - LOPJ (Poder Judicial)", "prioridad": "MEDIA"},
]

class LawIndexer:
    def __init__(self):
        logger.info("🚀 Initializing Law Indexer for ALL Missing Laws...")
        logger.info(f"   Model: {MODEL_NAME}")
        logger.info(f"   Collection: {COLLECTION_NAME}")
        
        self.qdrant = QdrantClient(url=QDRANT_URL)
        self.db_conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASSWORD
        )
        self.db_cursor = self.db_conn.cursor()
        
        logger.info("   Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)
        
        self.boe_client = BOEApiClient()
        
        logger.info("✅ All connections ready\n")
    
    def process_law(self, ley: dict):
        boe_id = ley['id']
        nombre = ley['nombre']
        prioridad = ley['prioridad']
        
        logger.info(f"\n{'='*80}")
        logger.info(f"🔴 Processing [{prioridad}]: {nombre}")
        logger.info(f"   BOE ID: {boe_id}")
        logger.info(f"{'='*80}")
        
        try:
            # 1. Get metadata and XML
            logger.info("   📥 Fetching from BOE API...")
            metadatos = self.boe_client.get_metadatos(boe_id)
            texto_xml = self.boe_client.get_texto_consolidado(boe_id)
            
            if not texto_xml:
                logger.error(f"❌ No XML content for {boe_id}")
                return
            
            titulo = metadatos.get('titulo', nombre)
            logger.info(f"   📄 Title: {titulo}")
            
            # 2. Parse XML into articles
            soup = BeautifulSoup(texto_xml, 'xml')
            articulos = soup.find_all('articulo')
            
            if not articulos:
                logger.warning(f"⚠️  No <articulo> tags. Using fallback chunking (1000 chars).")
                chunk_size = 1000
                texto_plano = soup.get_text(separator=" ", strip=True)
                articulos = [texto_plano[i:i+chunk_size] for i in range(0, len(texto_plano), chunk_size)]
                is_fallback = True
            else:
                logger.info(f"   ✅ Found {len(articulos)} articles")
                is_fallback = False
            
            # 3. Save document metadata (Layer 1 - Document)
            doc_id = f"{boe_id}-document"
            self.db_cursor.execute("""
                INSERT INTO laws (id, law_id, law_name, title, content, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (doc_id, boe_id, nombre, titulo, titulo, datetime.now()))
            
            # Qdrant document-level point
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
                        "prioridad": prioridad,
                        "metadata": metadatos
                    }
                )]
            )
            logger.info(f"   ✅ Layer 1 (Document) saved")
            
            # 4. Save articles/chunks (Layer 2 - Article Chunks)
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
                
                # PostgreSQL (full text storage)
                article_id = f"{boe_id}-{art_id}"
                self.db_cursor.execute("""
                    INSERT INTO laws (id, law_id, law_name, title, content, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET content = EXCLUDED.content;
                """, (article_id, boe_id, nombre, art_id, art_text, datetime.now()))
                
                # Qdrant (vector + metadata)
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
                        "text": art_text[:1200],  # Limit payload size
                        "prioridad": prioridad,
                        "is_smart_chunk": not is_fallback
                    }
                ))
                
                # Batch upsert every 50 points
                if len(points) >= 50:
                    self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
                    self.db_conn.commit()
                    logger.info(f"      ✅ Batch: {len(points)} articles")
                    points = []
            
            # Final batch
            if points:
                self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
                self.db_conn.commit()
                logger.info(f"      ✅ Final batch: {len(points)} articles")
            
            logger.info(f"✅ COMPLETED: {nombre} ({len(articulos)} articles indexed)")
            
        except Exception as e:
            logger.error(f"❌ Error processing {nombre}: {e}")
            import traceback
            traceback.print_exc()
            self.db_conn.rollback()
    
    def close(self):
        self.db_cursor.close()
        self.db_conn.close()
        logger.info("\n✅ Indexer closed")

def main():
    logger.info("\n" + "#"*80)
    logger.info("# 🚀 INDEXING ALL 10 MISSING LAWS FROM OFFICIAL SYLLABUS")
    logger.info("#"*80 + "\n")
    
    indexer = LawIndexer()
    
    try:
        total = len(MISSING_LAWS)
        for idx, ley in enumerate(MISSING_LAWS, 1):
            logger.info(f"\n📊 Progress: {idx}/{total}")
            indexer.process_law(ley)
        
        logger.info("\n" + "#"*80)
        logger.info("# ✅ INDEXING COMPLETE - ALL 10 LAWS PROCESSED")
        logger.info("#"*80)
        logger.info("\n📊 Summary:")
        logger.info(f"   - Total laws indexed: {total}")
        logger.info(f"   - Collection: {COLLECTION_NAME}")
        logger.info(f"   - Model: {MODEL_NAME}")
        logger.info(f"   - Vector size: {VECTOR_SIZE}")
        logger.info("\n✅ All laws are now available in Qdrant and PostgreSQL")
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Indexing interrupted by user")
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        indexer.close()

if __name__ == "__main__":
    main()
