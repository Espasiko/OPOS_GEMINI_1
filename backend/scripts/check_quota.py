import os
import sys
import psycopg2
import logging
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client import QdrantClient

# Load Environment Variables from backend/.env.backend
env_path = "/home/spas/OPOS_GEMINI_1/backend/.env.backend"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

if os.path.exists(env_path):
    load_dotenv(env_path)
    logger.info(f"✅ Loaded env from {env_path}")

# Configuration
TARGET_CLOUD_URL = "https://b554ceb5-2169-4064-9ce7-83c8cd44cf84.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "opositaia_knowledge"

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "opositaia")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

def check_postgres_size():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT pg_size_pretty(pg_database_size(%s));", (DB_NAME,))
        size_pretty = cursor.fetchone()[0]
        
        cursor.execute("SELECT pg_database_size(%s);", (DB_NAME,))
        size_bytes = cursor.fetchone()[0]
        
        logger.info(f"🐘 Postgres DB '{DB_NAME}' Size: {size_pretty} ({size_bytes} bytes)")
        
        conn.close()
    except Exception as e:
        logger.error(f"❌ Postgres check failed: {e}")

def check_qdrant_size():
    try:
        client = QdrantClient(url=TARGET_CLOUD_URL, api_key=QDRANT_API_KEY)
        collection = client.get_collection(COLLECTION_NAME)
        
        count = collection.points_count
        status = collection.status
        
        logger.info(f"🟢 Qdrant Collection '{COLLECTION_NAME}':")
        logger.info(f"   - Status: {status}")
        logger.info(f"   - Points Count: {count}")
        
        # Estimation
        # 1024 dim * 4 bytes = 4096 bytes/vector
        # Payload approx 1KB/point
        estimated_size_mb = (count * (4096 + 1024)) / (1024 * 1024)
        logger.info(f"   - Estimated Size (RAM/Disk): ~{estimated_size_mb:.2f} MB")
        
        if estimated_size_mb > 900:
             logger.warning("⚠️  WARNING: Approaching 1GB Free Tier Limit!")
        else:
             logger.info("✅ Well within 1GB Free Tier limit.")

    except Exception as e:
        logger.error(f"❌ Qdrant check failed: {e}")

if __name__ == "__main__":
    check_postgres_size()
    check_qdrant_size()
