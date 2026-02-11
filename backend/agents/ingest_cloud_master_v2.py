#!/usr/bin/env python3
"""
Master Cloud Ingestion Script V2 (Secure & Smart)
Implements Hybrid RAG Strategy:
1. Load Secrets from backend/.env.backend
2. Wipes Qdrant Cloud Collection
3. Syncs Postgres Chunks -> Qdrant
4. Extracts 'Artículo X' from content for better Metadata
"""
import os
import sys
import uuid
import logging
import psycopg2
import json
import re
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load Environment Variables from backend/.env.backend
env_path = "/home/spas/OPOS_GEMINI_1/backend/.env.backend"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

if os.path.exists(env_path):
    load_dotenv(env_path)
    logger.info(f"✅ Loaded env from {env_path}")
else:
    logger.error(f"❌ Env file not found: {env_path}")
    sys.exit(1)

# Configuration
# Specific Cloud URL as requested by user verification
TARGET_CLOUD_URL = "https://b554ceb5-2169-4064-9ce7-83c8cd44cf84.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_API_KEY:
    logger.error("❌ QDRANT_API_KEY missing in .env.backend")
    sys.exit(1)

COLLECTION_NAME = "opositaia_knowledge"
MODEL_NAME = "pablosi/bge-m3-spa-law-qa-trained-2"

# Postgres Config
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "opositaia")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

class CloudIngester:
    def __init__(self):
        logger.info("☁️  Initializing Ingester V2 (Resume Mode)...")
        
        # 1. Connect to Qdrant Cloud
        try:
            self.qdrant = QdrantClient(url=TARGET_CLOUD_URL, api_key=QDRANT_API_KEY, timeout=300) # Increased to 300s
            self.qdrant.get_collections()
            logger.info("✅ Qdrant Cloud Connected (Timeout=300s)")
        except Exception as e:
            logger.error(f"❌ Qdrant Connection Failed: {e}")
            sys.exit(1)

        # 2. Connect to Local Postgres
        try:
            self.db_conn = psycopg2.connect(
                host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
                user=DB_USER, password=DB_PASSWORD
            )
            self.db_cursor = self.db_conn.cursor()
            logger.info("✅ Postgres Connected")
        except Exception as e:
            logger.error(f"❌ Postgres Connection Failed: {e}")
            sys.exit(1)

        # 3. Load Model
        logger.info(f"🧠 Loading Model: {MODEL_NAME}...")
        self.model = SentenceTransformer(MODEL_NAME)
        logger.info("✅ Model Loaded")

    def fetch_existing_ids(self):
        """Fetches all existing Point IDs to allow resuming"""
        logger.info("🔎 Fetching existing points to Resume...")
        existing_ids = set()
        offset = None
        while True:
            try:
                points, next_offset = self.qdrant.scroll(
                    collection_name=COLLECTION_NAME,
                    with_payload=False,
                    with_vectors=False,
                    limit=1000,
                    scroll_filter=None,
                    offset=offset
                )
                for p in points:
                    existing_ids.add(p.id)
                
                offset = next_offset
                if offset is None:
                    break
            except Exception as e:
                logger.error(f"❌ Scroll failed: {e}")
                break
                
        logger.info(f"✅ Found {len(existing_ids)} existing chunks. Resuming ingestion...")
        return existing_ids

    def safe_upsert(self, points):
        """Upsert with retry logic"""
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
                return True
            except Exception as e:
                logger.warning(f"⚠️ Upsert failed (Attempt {attempt+1}/{max_retries}): {e}")
                time.sleep(5)
        logger.error("❌ Upsert failed after retries. Skipping batch.")
        return False

    def recreate_collection(self):
        """Wipes and creates collection"""
        logger.info("🗑️  Wiping collection for clean ingestion...")
        try:
            self.qdrant.delete_collection(COLLECTION_NAME)
            logger.info(f"✅ Deleted old collection: {COLLECTION_NAME}")
        except:
            pass

        self.qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1024,
                distance=models.Distance.COSINE
            )
        )
        logger.info(f"🆕 Created fresh collection: {COLLECTION_NAME}")

        # Create Payload Indexes for Performance
        logger.info("⚡ Creating Payload Indexes...")
        self.qdrant.create_payload_index(COLLECTION_NAME, "boe_id", models.PayloadSchemaType.KEYWORD)
        self.qdrant.create_payload_index(COLLECTION_NAME, "law_name", models.PayloadSchemaType.TEXT)
        self.qdrant.create_payload_index(COLLECTION_NAME, "layer", models.PayloadSchemaType.KEYWORD)
        self.qdrant.create_payload_index(COLLECTION_NAME, "article_title", models.PayloadSchemaType.TEXT)
        logger.info("✅ Indexes created")

    def extract_article_title(self, text):
        """Attempts to find 'Artículo X' at start of text"""
        # Look for "Artículo N" in first 100 chars
        match = re.search(r'(Artículo\s+\d+)', text[:100], re.IGNORECASE)
        if match:
            return match.group(0) # e.g. "Artículo 41"
        return None

    def process_all_laws(self):
        # Fetch existing IDs first
        existing_ids = self.fetch_existing_ids()
        
        # Fetch all laws
        self.db_cursor.execute("SELECT boe_id, titulo FROM leyes_catalogo")
        laws = self.db_cursor.fetchall()
        
        logger.info(f"🎯 Syncing {len(laws)} laws...")
        
        total_chunks = 0
        skipped_chunks = 0
        points_buffer = []
        
        for law in laws:
            boe_id, law_title = law
            
            # Fetch Chunks
            self.db_cursor.execute(
                "SELECT id, content, title FROM laws WHERE law_id = %s",
                (boe_id,)
            )
            chunks = self.db_cursor.fetchall()
            
            for row in chunks:
                chunk_id, content, chunk_code_title = row
                
                # Create ID deterministically
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(chunk_id)))
                
                # SKIP IF EXISTS
                if point_id in existing_ids:
                    skipped_chunks += 1
                    continue

                if not content or len(content) < 10: continue

                # Intelligence: Extract real title
                real_title = self.extract_article_title(content)
                final_title = real_title if real_title else chunk_code_title

                # Embed: Title + Content
                text_to_embed = f"{law_title}\n{final_title}\n{content}"
                vector = self.model.encode(text_to_embed).tolist()
                
                # Payload (BALANCED MODE: Snippet + Key Metadata)
                text_snippet = content[:500] if content else ""  # 500 chars for reranking/preview
                payload = {
                    "boe_id": boe_id,
                    "law_name": law_title,
                    "article_title": final_title,
                    "text_snippet": text_snippet,
                    "postgres_id": chunk_id,
                    "layer": "article_chunk",
                    "source": "hybrid_sync_v3"
                }
                
                points_buffer.append(models.PointStruct(id=point_id, vector=vector, payload=payload))
                
                if len(points_buffer) >= 20: # Smaller batch for stability
                    self.safe_upsert(points_buffer)
                    total_chunks += len(points_buffer)
                    points_buffer = []
                    print(f"\r🚀 Synced {total_chunks} new chunks (Skipped {skipped_chunks})...", end="", flush=True)

        # Flush remaining
        if points_buffer:
            self.safe_upsert(points_buffer)
            total_chunks += len(points_buffer)

        print("")
        logger.info(f"✅ FINAL SUCCESS: Synced {total_chunks} NEW chunks to Cloud. (Skipped {skipped_chunks} existing)")

if __name__ == "__main__":
    ingester = CloudIngester()
    # ingester.recreate_collection()  # DISABLED: Resume mode active
    ingester.process_all_laws()
