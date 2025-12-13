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

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT law_id, law_name FROM laws ORDER BY law_name;")
    rows = cursor.fetchall()
    print("--- LAWS IN POSTGRES ---")
    for row in rows:
        print(f"{row[0]}: {row[1]}")
    conn.close()
except Exception as e:
    print(f"Postgres Error: {e}")

# try:
#     client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
#     info = client.get_collection(COLLECTION_NAME)
#     print(f"\n--- QDRANT COLLECTION INFO ---")
#     print(f"Points count: {info.points_count}")
#     print(f"Vectors count: {info.vectors_count}")
# except Exception as e:
#     print(f"Qdrant Error: {e}")
