import os
import psycopg2
from qdrant_client import QdrantClient

# Configuration
DB_HOST = os.getenv("POSTGRES_HOST", "opositaia-postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "opositaia")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

QDRANT_HOST = os.getenv("QDRANT_HOST", "opositaia-qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "leyes_espana"

def check_status():
    print(f"Checking connections to Postgres ({DB_HOST}) and Qdrant ({QDRANT_HOST})...")
    
    # Check Postgres
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT law_name FROM laws;")
        pg_laws = [row[0] for row in cursor.fetchall()]
        print("\n✅ Postgres Laws Ingested:")
        for law in pg_laws:
            print(f" - {law}")
        conn.close()
    except Exception as e:
        print(f"\n❌ Postgres Error: {e}")
        pg_laws = []

    # Check Qdrant
    try:
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        collections = client.get_collections()
        exists = any(c.name == COLLECTION_NAME for c in collections.collections)
        if exists:
            count = client.count(collection_name=COLLECTION_NAME)
            print(f"\n✅ Qdrant Collection '{COLLECTION_NAME}' exists with {count.count} vectors.")
        else:
            print(f"\n❌ Qdrant Collection '{COLLECTION_NAME}' does NOT exist.")
    except Exception as e:
        print(f"\n❌ Qdrant Error: {e}")

if __name__ == "__main__":
    check_status()
