import os
import sys
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Configuration
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge"

def check_qdrant_status():
    try:
        client = QdrantClient(url=QDRANT_URL)
        
        # Check if collection exists
        if not client.collection_exists(COLLECTION_NAME):
            print(f"Collection '{COLLECTION_NAME}' does not exist.")
            return

        # Get collection info
        info = client.get_collection(COLLECTION_NAME)
        print(f"Collection: {COLLECTION_NAME}")
        print(f"Status: {info.status}")
        print(f"Total Points (Vectors): {info.points_count}")
        print(f"Vectors Config: {info.config.params.vectors}")

        # Get unique BOE IDs (using scroll and payload)
        # Note: This might be slow for huge collections, but fine for checking ~17 laws
        # A more efficient way is to use the payload index if we just want to count unique ones,
        # but Qdrant doesn't have a "SELECT DISTINCT" API directly.
        # We will scroll through layer='document' points which represent the laws.
        
        print("\nChecking indexed laws (layer='document')...")
        
        scroll_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="layer",
                    match=models.MatchValue(value="document")
                )
            ]
        )
        
        points, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=scroll_filter,
            limit=1000,
            with_payload=True,
            with_vectors=False
        )
        
        indexed_ids = set()
        print(f"Found {len(points)} document entries:")
        for point in points:
            boe_id = point.payload.get('boe_id')
            title = point.payload.get('title', 'No title')
            if boe_id:
                indexed_ids.add(boe_id)
                print(f" - {boe_id}: {title[:50]}...")
        
        print(f"\nTotal Unique Laws Indexed: {len(indexed_ids)}")
        return list(indexed_ids)

    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")

if __name__ == "__main__":
    check_qdrant_status()
