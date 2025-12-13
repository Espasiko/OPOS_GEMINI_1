#!/usr/bin/env python3
"""
Verification script for ID: BOE-A-1996-4447 (RD 84/1996)
Checks:
1. Postgres: Count rows for this law_id
2. Qdrant: Count points for this boe_id in payload
"""
import os
import sys
import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Config
QDRANT_URL = "http://localhost:6333"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "opositaia"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
COLLECTION_NAME = "opositaia_knowledge"

LAW_ID = "BOE-A-1996-4447"

def verify():
    print(f"🔍 VERIFYING INGESTION FOR: {LAW_ID}")
    print("-" * 50)

    # 1. POSTGRES CHECK
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    
    # Check Document Root
    cur.execute("SELECT id, title FROM laws WHERE law_id = %s AND id LIKE '%%-document'", (LAW_ID,))
    doc_root = cur.fetchone()
    
    print(f"DEBUG: doc_root raw: {doc_root}")

    if doc_root and len(doc_root) > 1:
        print(f"✅ [Postgres] Document Root found: {doc_root[1][:50]}...")
    else:
        print(f"⚠️ [Postgres] Document Root NOT found or invalid (Result: {doc_root})")

    # Check Chunks
    cur.execute("SELECT COUNT(*) FROM laws WHERE law_id = %s AND id LIKE '%%-chunk_%%'", (LAW_ID,))
    res = cur.fetchone()
    print(f"DEBUG: count raw: {res}")
    if res:
        print(f"✅ [Postgres] Total Text Chunks found: {res[0]}")
    else:
            print(f"❌ [Postgres] Total Text Chunks query returned None")
    
    cur.close()
    conn.close()

    print("-" * 50)

    # 2. QDRANT CHECK
    try:
        # Compatibility check skip
        client = QdrantClient(url=QDRANT_URL, check_compatibility=False)
        
        # Filter by payload boe_id
        scroll_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="boe_id",
                    match=models.MatchValue(value=LAW_ID)
                )
            ]
        )
        
        # Count points (using scroll with limit 0 + with_payload=False to be fast? 
        # Actually Qdrant count api is better)
        count_res = client.count(
            collection_name=COLLECTION_NAME,
            count_filter=scroll_filter
        )
        
        print(f"✅ [Qdrant] Total Vectors found: {count_res.count}")
        
        if count_res.count > 0:
            # Sample one point
            points, _ = client.scroll(
                collection_name=COLLECTION_NAME,
                scroll_filter=scroll_filter,
                limit=1,
                with_payload=True
            )
            if points:
                p = points[0]
                print(f"   Sample Payload Title: {p.payload.get('title')}")
                print(f"   Sample Payload Is_Scraped: {p.payload.get('is_scraped')}")

    except Exception as e:
        print(f"❌ [Qdrant] Connection Failed: {e}")

if __name__ == "__main__":
    verify()
