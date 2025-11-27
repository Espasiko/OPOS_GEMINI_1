"""
Quick Setup Test Script
Tests: Ollama (bge-m3), Qdrant, PostgreSQL
"""

import asyncio
import httpx
import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from dotenv import load_dotenv

load_dotenv(".env.backend")

# Colors for terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


async def test_ollama():
    """Test Ollama + bge-m3"""
    print(f"\n{YELLOW}Testing Ollama + bge-m3...{RESET}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test embedding generation
            response = await client.post(
                "http://localhost:11434/api/embeddings",
                json={
                    "model": "bge-m3",
                    "prompt": "¿Qué es la incapacidad temporal?"
                }
            )
            response.raise_for_status()
            data = response.json()
            embedding = data["embedding"]
            
            print(f"{GREEN}✅ Ollama OK{RESET}")
            print(f"   Model: bge-m3")
            print(f"   Embedding dimension: {len(embedding)}")
            print(f"   Sample values: {embedding[:5]}")
            return True
            
    except Exception as e:
        print(f"{RED}❌ Ollama FAILED: {e}{RESET}")
        return False


def test_qdrant():
    """Test Qdrant connection"""
    print(f"\n{YELLOW}Testing Qdrant...{RESET}")
    
    try:
        client = QdrantClient(url="http://localhost:6333")
        
        # Get collections
        collections = client.get_collections()
        
        print(f"{GREEN}✅ Qdrant OK{RESET}")
        print(f"   Collections: {len(collections.collections)}")
        
        # Check if opositaia_documents exists
        collection_names = [c.name for c in collections.collections]
        if "opositaia_documents" in collection_names:
            info = client.get_collection("opositaia_documents")
            print(f"   opositaia_documents: {info.points_count} documents")
        else:
            print(f"   {YELLOW}⚠️  opositaia_documents not found (will be created){RESET}")
            
            # Create collection
            client.create_collection(
                collection_name="opositaia_documents",
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
            )
            print(f"   {GREEN}✅ Created opositaia_documents collection{RESET}")
        
        return True
        
    except Exception as e:
        print(f"{RED}❌ Qdrant FAILED: {e}{RESET}")
        return False


def test_postgres():
    """Test PostgreSQL connection"""
    print(f"\n{YELLOW}Testing PostgreSQL...{RESET}")
    
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            database=os.getenv("POSTGRES_DB", "opositaia"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres")
        )
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print(f"{GREEN}✅ PostgreSQL OK{RESET}")
        print(f"   Database: {os.getenv('POSTGRES_DB', 'opositaia')}")
        print(f"   Tables: {len(tables)}")
        
        if len(tables) == 0:
            print(f"   {YELLOW}⚠️  No tables found. Run: python backend/database/init_db.py{RESET}")
        else:
            for table in tables[:5]:  # Show first 5
                print(f"     - {table[0]}")
            if len(tables) > 5:
                print(f"     ... and {len(tables) - 5} more")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"{RED}❌ PostgreSQL FAILED: {e}{RESET}")
        print(f"   {YELLOW}Make sure PostgreSQL is running and credentials are correct{RESET}")
        return False


async def main():
    """Run all tests"""
    print(f"\n{'='*60}")
    print(f"OpositAIA Setup Test")
    print(f"{'='*60}")
    
    results = []
    
    # Test Ollama
    results.append(await test_ollama())
    
    # Test Qdrant
    results.append(test_qdrant())
    
    # Test PostgreSQL
    results.append(test_postgres())
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary")
    print(f"{'='*60}")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{GREEN}✅ All tests passed ({passed}/{total}){RESET}")
        print(f"\n{GREEN}🚀 Ready to start backend!{RESET}")
        print(f"   Run: python backend/main.py")
    else:
        print(f"{RED}❌ Some tests failed ({passed}/{total}){RESET}")
        print(f"\n{YELLOW}Fix the issues above before starting backend{RESET}")


if __name__ == "__main__":
    asyncio.run(main())
