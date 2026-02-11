import os
import sys
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

# Load env
load_dotenv("/home/spas/OPOS_GEMINI_1/backend/.env.backend")
# TARGET LOCAL FOR THIS CHECK
LOCAL_URL = "http://localhost:6333"
API_KEY = os.getenv("QDRANT_API_KEY") 

def search_exam_text(client, collection_name, search_text):
    print(f"--- SEARCHING IN: {collection_name} ---")
    try:
        # We use scroll with filter because 'search' needs a vector
        # Using a dummy vector [0.0]*1024 or [0.0]*768 might work if we knew the dim
        # But 'scroll' with filter is safer if we just look for exact match or full text match
        
        # Try full text match if indexed, or exact match
        resp, _ = client.scroll(
            collection_name=collection_name,
            limit=5,
            with_payload=True,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="text",
                        match=models.MatchText(text=search_text)
                    )
                ]
            )
        )
        
        if resp:
            print(f"✅ FOUND {len(resp)} matches in {collection_name}!")
            for p in resp:
                print(f"ID: {p.id} | Preview: {p.payload.get('text', '')[:100]}...")
        else:
            print(f"❌ NO matches found in {collection_name}")
            
    except Exception as e:
        print(f"⚠️ Error searching {collection_name}: {e}")

if __name__ == "__main__":
    print(f"Connecting to Local Qdrant: {LOCAL_URL}...")
    client = QdrantClient(url=LOCAL_URL, api_key=None) # Local usually no key
    
    # Text from Examen C1 SS 2022
    QUERY = "acceso al Cuerpo Administrativo de la Administración de la Seguridad Social"
    
    search_exam_text(client, "leyes_espana", QUERY)
    search_exam_text(client, "opositaia_knowledge", QUERY)
