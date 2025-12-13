#!/usr/bin/env python3
"""
Universal Verification Script.
Usage: python verify_ingestion_universal.py <BOE_ID>
"""
import os
import sys
import psycopg2
import argparse
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

def verify(law_id):
    print(f"🔍 VERIFYING INGESTION FOR: {law_id}")
    print("-" * 50)

    # 1. POSTGRES CHECK
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASSWORD
        )
        cur = conn.cursor()
        
        # Check Document Root
        # Use %% for literal % in LIKE clauses to avoid escaping issues with psycopg2 executing with args
        cur.execute("SELECT id, title FROM laws WHERE law_id = %s AND id LIKE '%%-document'", (law_id,))
        doc_root = cur.fetchone()
        
        if doc_root:
            print(f"✅ [Postgres] Document Root found: {doc_root[1][:50]}...")
        else:
            print(f"⚠️ [Postgres] Document Root NOT found")

        # Check Chunks
        cur.execute("SELECT COUNT(*) FROM laws WHERE law_id = %s AND id LIKE '%%-chunk_%%'", (law_id,))
        res = cur.fetchone()
        
        if res and res[0] > 0:
            print(f"✅ [Postgres] Total Text Chunks found: {res[0]}")
        else:
             print(f"❌ [Postgres] No Text Chunks found (Count: {res})")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ [Postgres] Connection Failed: {e}")

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
                    match=models.MatchValue(value=law_id)
                )
            ]
        )
        
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
    parser = argparse.ArgumentParser()
    parser.add_argument("law_id", help="BOE ID to verify")
    args = parser.parse_args()
    
    verify(args.law_id)
