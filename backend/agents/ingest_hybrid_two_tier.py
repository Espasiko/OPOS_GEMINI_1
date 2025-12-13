#!/usr/bin/env python3
"""
INGESTA HÍBRIDA TWO-TIER STORAGE
=================================
Implementa la estrategia documentada en docs/ESTRATEGIAS_QDRANT_COMPLETO.md

ARQUITECTURA:
- Qdrant: Fragmentos (artículos) con embeddings para búsqueda semántica
- PostgreSQL: Texto completo + metadatos para recuperación y trazabilidad

LEYES: 17 leyes del temario oficial (SS + AGE)
"""

import os
import sys
import uuid
import logging
import time
import psycopg2
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup

try:
    from backend.agents.boe_api_client import BOEApiClient
except ImportError:
    from boe_api_client import BOEApiClient

# Configuration (Docker-aware)
QDRANT_HOST = os.getenv("QDRANT_HOST", "opositaia-qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"

DB_HOST = os.getenv("POSTGRES_HOST", "opositaia-postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "opositaia")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

COLLECTION_NAME = "opositaia_knowledge"
MODEL_NAME = "pablosi/bge-m3-spa-law-qa-trained-2"
VECTOR_SIZE = 1024

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 17 Leyes del Temario Oficial (SS + AGE)
LEYES_TEMARIO_OFICIAL = [
    # === CRÍTICAS (Seguridad Social) ===
    {"id": "BOE-A-2015-11724", "nombre": "LGSS", "prioridad": "CRÍTICA"},
    {"id": "BOE-A-1996-3981", "nombre": "RD 84/1996 - Afiliación", "prioridad": "CRÍTICA"},
    {"id": "BOE-A-1995-26497", "nombre": "RD 2064/1995 - Cotización", "prioridad": "CRÍTICA"},
    {"id": "BOE-A-2004-11607", "nombre": "RD 1415/2004 - Recaudación", "prioridad": "CRÍTICA"},
    
    # === TEMARIO GENERAL (AGE + SS - 75% solapamiento) ===
    {"id": "BOE-A-1978-31229", "nombre": "Constitución Española", "prioridad": "CRÍTICA"},
    {"id": "BOE-A-2015-10565", "nombre": "Ley 39/2015 - LPACAP", "prioridad": "ALTA"},
    {"id": "BOE-A-2015-10566", "nombre": "Ley 40/2015 - LRJSP", "prioridad": "ALTA"},
    {"id": "BOE-A-2015-10438", "nombre": "TREBEP", "prioridad": "ALTA"},
    {"id": "BOE-A-1979-23709", "nombre": "LOTC", "prioridad": "ALTA"},
    {"id": "BOE-A-1985-12666", "nombre": "LOPJ", "prioridad": "ALTA"},
    {"id": "BOE-A-1997-25336", "nombre": "Ley del Gobierno", "prioridad": "MEDIA"},
    
    # === ADICIONALES (Presentes en temario) ===
    {"id": "BOE-A-2021-21007", "nombre": "Ley IMV", "prioridad": "MEDIA"},
    {"id": "BOE-A-2007-6115", "nombre": "Ley Igualdad", "prioridad": "MEDIA"},
    {"id": "BOE-A-2004-21760", "nombre": "Ley Violencia Género", "prioridad": "MEDIA"},
    {"id": "BOE-A-2009-4918", "nombre": "RD 295/2009 - Maternidad", "prioridad": "MEDIA"},
    
    # === SECUNDARIAS (Ya ingestadas parcialmente) ===
    {"id": "BOE-A-1985-5392", "nombre": "LBRL", "prioridad": "BAJA"},
    {"id": "BOE-A-2003-20977", "nombre": "LGP", "prioridad": "BAJA"},
]

class HybridIndexer:
    def __init__(self):
        logger.info("Initializing Hybrid Two-Tier Indexer...")
        
        # Qdrant Client
        try:
            self.qdrant = QdrantClient(url=QDRANT_URL)
            logger.info(f"✅ Qdrant connected: {QDRANT_URL}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Qdrant: {e}")
            raise
        
        # PostgreSQL Connection
        try:
            self.db_conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            self.db_cursor = self.db_conn.cursor()
            logger.info(f"✅ PostgreSQL connected: {DB_HOST}:{DB_PORT}/{DB_NAME}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
            raise
        
        # Embedding Model
        logger.info(f"Loading embedding model: {MODEL_NAME}...")
        self.model = SentenceTransformer(MODEL_NAME)
        logger.info("✅ Model loaded successfully")
        
        # BOE API Client
        self.boe_client = BOEApiClient()
        
        # Ensure database schema
        self.ensure_db_schema()
    
    def ensure_db_schema(self):
        """Create/Update laws table schema."""
        # Primero, crear la tabla si no existe (sin xml_content)
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS laws (
                id TEXT PRIMARY KEY,
                law_id TEXT,
                law_name TEXT,
                title TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Luego, intentar agregar las columnas nuevas si no existen
        try:
            self.db_cursor.execute("""
                ALTER TABLE laws ADD COLUMN IF NOT EXISTS xml_content TEXT;
            """)
        except Exception as e:
            logger.warning(f"Could not add xml_content column (may already exist): {e}")
        
        try:
            self.db_cursor.execute("""
                ALTER TABLE laws ADD COLUMN IF NOT EXISTS metadata TEXT;
            """)
        except Exception as e:
            logger.warning(f"Could not add metadata column (may already exist): {e}")
        
        self.db_conn.commit()
        logger.info("✅ Database schema ensured")
    
    def ensure_qdrant_collection(self):
        """Create Qdrant collection if it doesn't exist."""
        max_retries = 10
        for i in range(max_retries):
            try:
                if not self.qdrant.collection_exists(COLLECTION_NAME):
                    logger.info(f"Creating Qdrant collection: {COLLECTION_NAME}")
                    self.qdrant.create_collection(
                        collection_name=COLLECTION_NAME,
                        vectors_config={
                            "dense": models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE)
                        },
                    )
                    
                    # Create payload indexes
                    self.qdrant.create_payload_index(COLLECTION_NAME, "layer", models.PayloadSchemaType.KEYWORD)
                    self.qdrant.create_payload_index(COLLECTION_NAME, "boe_id", models.PayloadSchemaType.KEYWORD)
                    self.qdrant.create_payload_index(COLLECTION_NAME, "parent_id", models.PayloadSchemaType.KEYWORD)
                    logger.info("✅ Qdrant collection created")
                else:
                    logger.info(f"✅ Qdrant collection already exists: {COLLECTION_NAME}")
                return
            except Exception as e:
                logger.warning(f"Connection attempt {i+1}/{max_retries} failed: {e}. Retrying in 5s...")
                time.sleep(5)
        
        raise Exception("Could not connect to Qdrant after multiple retries")
    
    def process_law(self, ley_info: Dict[str, str]):
        """Process one law: Download -> Parse -> Save to Qdrant + PostgreSQL"""
        boe_id = ley_info["id"]
        nombre = ley_info["nombre"]
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {nombre} ({boe_id})")
        logger.info(f"{'='*60}")
        
        try:
            # 1. Download metadata and XML
            metadatos = self.boe_client.get_metadatos(boe_id)
            texto_xml = self.boe_client.get_texto_consolidado(boe_id)
            
            if not texto_xml:
                logger.warning(f"⚠️ No XML content for {boe_id}")
                return
            
            titulo_completo = metadatos.get('titulo', nombre)
            logger.info(f"📄 Title: {titulo_completo}")
            
            # 2. Parse articles with BeautifulSoup
            soup = BeautifulSoup(texto_xml, 'xml')
            articulos = soup.find_all('articulo')
            
            if not articulos:
                logger.warning(f"⚠️ No <articulo> tags found. Using fallback chunking.")
                articulos = self._fallback_chunking(texto_xml)
            else:
                logger.info(f"✅ Found {len(articulos)} articles")
            
            # 3. Save to PostgreSQL (Law Document - Full XML)
            doc_id = f"{boe_id}-document"
            self.db_cursor.execute("""
                INSERT INTO laws (id, law_id, law_name, title, content, xml_content, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    content = EXCLUDED.content,
                    xml_content = EXCLUDED.xml_content,
                    metadata = EXCLUDED.metadata;
            """, (
                doc_id,
                boe_id,
                nombre,
                titulo_completo,
                soup.get_text(separator=" ", strip=True)[:5000],  # Preview
                texto_xml,
                str(metadatos)
            ))
            self.db_conn.commit()
            logger.info(f"✅ PostgreSQL: Saved document {doc_id}")
            
            # 4. Save to Qdrant (Layer 1: Document Metadata)
            qdrant_doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_id))
            self.qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    models.PointStruct(
                        id=qdrant_doc_id,
                        vector={"dense": self.model.encode(titulo_completo).tolist()},
                        payload={
                            "layer": "document",
                            "boe_id": boe_id,
                            "law_name": nombre,
                            "title": titulo_completo,
                            "text": titulo_completo,
                            "metadata": metadatos
                        }
                    )
                ]
            )
            logger.info(f"✅ Qdrant Layer 1: Saved metadata")
            
            # 5. Save articles to BOTH systems (Layer 2: Articles)
            points_qdrant = []
            for i, art in enumerate(articulos):
                if isinstance(art, str):
                    # Fallback chunk
                    art_text = art
                    art_id = f"chunk_{i}"
                else:
                    # Real article
                    art_text = art.get_text(separator=" ", strip=True)
                    art_id = art.get('id', f"art_{i}")
                
                if len(art_text) < 50:
                    continue
                
                # PostgreSQL: Save article
                article_db_id = f"{boe_id}-{art_id}"
                self.db_cursor.execute("""
                    INSERT INTO laws (id, law_id, law_name, title, content)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        content = EXCLUDED.content;
                """, (
                    article_db_id,
                    boe_id,
                    nombre,
                    art_id,
                    art_text
                ))
                
                # Qdrant: Save article with embedding
                chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, article_db_id))
                embedding = self.model.encode(art_text).tolist()
                
                points_qdrant.append(models.PointStruct(
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
                        "metadata": metadatos,
                        "is_smart_chunk": not isinstance(art, str)
                    }
                ))
                
                # Batch upsert every 50 articles
                if len(points_qdrant) >= 50:
                    self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points_qdrant)
                    self.db_conn.commit()
                    logger.info(f"  ✅ Batch saved: {len(points_qdrant)} articles")
                    points_qdrant = []
            
            # Final batch
            if points_qdrant:
                self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points_qdrant)
                self.db_conn.commit()
                logger.info(f"  ✅ Final batch: {len(points_qdrant)} articles")
            
            logger.info(f"✅ COMPLETED: {nombre} ({len(articulos)} articles)")
            
        except Exception as e:
            logger.error(f"❌ Error processing {boe_id}: {e}")
            self.db_conn.rollback()
    
    def _fallback_chunking(self, texto_xml: str) -> List[str]:
        """Fallback: Simple chunking if no <articulo> tags found."""
        chunk_size = 1000
        chunks = [texto_xml[i:i+chunk_size] for i in range(0, len(texto_xml), chunk_size)]
        return chunks
    
    def close(self):
        """Close database connections."""
        self.db_cursor.close()
        self.db_conn.close()
        logger.info("✅ Connections closed")

def main():
    indexer = HybridIndexer()
    
    try:
        indexer.ensure_qdrant_collection()
        
        # Check which laws are already processed
        indexer.db_cursor.execute("SELECT DISTINCT law_id FROM laws;")
        processed_laws = set(row[0] for row in indexer.db_cursor.fetchall())
        
        pending_laws = [ley for ley in LEYES_TEMARIO_OFICIAL if ley['id'] not in processed_laws]
        
        if processed_laws:
            logger.info(f"\n{'#'*60}")
            logger.info(f"✅ Already processed: {len(processed_laws)} laws")
            for law_id in sorted(processed_laws):
                logger.info(f"   ✓ {law_id}")
            logger.info(f"{'#'*60}\n")
        
        if not pending_laws:
            logger.info("🎉 All laws already processed!")
            return
        
        logger.info(f"\n{'#'*60}")
        logger.info(f"# RESUMING INGESTION: {len(pending_laws)} PENDING LAWS")
        logger.info(f"{'#'*60}\n")
        
        for idx, ley in enumerate(pending_laws, 1):
            logger.info(f"\n[{idx}/{len(pending_laws)}] {ley['nombre']} ({ley['id']})")
            indexer.process_law(ley)
            time.sleep(1)  # Rate limiting
        
        logger.info(f"\n{'#'*60}")
        logger.info("# ✅ INGESTION COMPLETE")
        logger.info(f"{'#'*60}\n")
        
    finally:
        indexer.close()

if __name__ == "__main__":
    main()
