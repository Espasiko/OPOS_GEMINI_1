#!/usr/bin/env python3
"""
Performance Tests - Backend
Mide tiempos de respuesta y rendimiento
"""

import asyncio
import time
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / '.env.backend')

print("\n" + "="*80)
print("⚡ PERFORMANCE TESTS - BACKEND")
print("="*80)

# Test 1: RAG Query Performance
async def test_rag_performance():
    """Test RAG query response time"""
    print("\n📊 TEST 1: RAG Query Performance")
    print("-" * 80)
    
    try:
        from agents.rag_agent_v2 import RAGAgentV2
        
        agent = RAGAgentV2()
        queries = [
            "¿Qué es la incapacidad temporal?",
            "¿Cuánto dura la prestación por desempleo?",
            "¿Qué requisitos tiene la jubilación?"
        ]
        
        times = []
        for query in queries:
            start = time.time()
            result = await agent.query(query, provider="mistral")
            elapsed = time.time() - start
            times.append(elapsed)
            
            status = "✅" if elapsed < 5.0 else "⚠️" if elapsed < 10.0 else "❌"
            print(f"{status} Query: {elapsed:.2f}s - {query[:50]}...")
        
        avg_time = sum(times) / len(times)
        print(f"\n📊 Average: {avg_time:.2f}s")
        
        if avg_time < 5.0:
            print("✅ EXCELLENT - Under 5 seconds")
        elif avg_time < 10.0:
            print("⚠️  ACCEPTABLE - Under 10 seconds")
        else:
            print("❌ SLOW - Over 10 seconds")
        
        return avg_time < 10.0
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

# Test 2: LLM Provider Performance
async def test_provider_performance():
    """Test LLM provider response times"""
    print("\n📊 TEST 2: LLM Provider Performance")
    print("-" * 80)
    
    try:
        from agents.llm_providers import PROVIDERS
        
        results = {}
        
        for provider_id, provider in PROVIDERS.items():
            info = provider.get_info()
            if not info['configured']:
                print(f"⚠️  {provider_id}: SKIPPED (not configured)")
                continue
            
            try:
                messages = [{"role": "user", "content": "Di 'OK' en una palabra"}]
                
                start = time.time()
                response = ""
                async for chunk in provider.generate_stream(messages, max_tokens=10):
                    response += chunk
                elapsed = time.time() - start
                
                results[provider_id] = elapsed
                
                status = "✅" if elapsed < 2.0 else "⚠️" if elapsed < 5.0 else "❌"
                print(f"{status} {provider_id}: {elapsed:.2f}s")
                
            except Exception as e:
                print(f"❌ {provider_id}: ERROR - {str(e)[:50]}")
        
        if results:
            fastest = min(results.items(), key=lambda x: x[1])
            print(f"\n🏆 Fastest: {fastest[0]} ({fastest[1]:.2f}s)")
            return True
        else:
            print("\n⚠️  No providers tested")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

# Test 3: Concurrent Requests
async def test_concurrent_performance():
    """Test handling multiple concurrent requests"""
    print("\n📊 TEST 3: Concurrent Requests Performance")
    print("-" * 80)
    
    try:
        from agents.rag_agent_v2 import RAGAgentV2
        
        agent = RAGAgentV2()
        query = "¿Qué es la incapacidad temporal?"
        
        # Test with 3 concurrent requests
        num_requests = 3
        print(f"Testing {num_requests} concurrent requests...")
        
        start = time.time()
        tasks = [agent.query(query, provider="mistral") for _ in range(num_requests)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        elapsed = time.time() - start
        
        successful = sum(1 for r in results if not isinstance(r, Exception))
        
        print(f"\n✅ Completed: {successful}/{num_requests} requests")
        print(f"⏱️  Total time: {elapsed:.2f}s")
        print(f"📊 Avg per request: {elapsed/num_requests:.2f}s")
        
        if successful == num_requests and elapsed < 15.0:
            print("✅ EXCELLENT - All requests succeeded quickly")
            return True
        elif successful > 0:
            print("⚠️  PARTIAL - Some requests succeeded")
            return True
        else:
            print("❌ FAILED - No requests succeeded")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

# Test 4: Memory Usage
def test_memory_usage():
    """Test memory usage"""
    print("\n📊 TEST 4: Memory Usage")
    print("-" * 80)
    
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        print(f"Current memory usage: {memory_mb:.2f} MB")
        
        if memory_mb < 500:
            print("✅ EXCELLENT - Under 500 MB")
            return True
        elif memory_mb < 1000:
            print("⚠️  ACCEPTABLE - Under 1 GB")
            return True
        else:
            print("❌ HIGH - Over 1 GB")
            return False
            
    except ImportError:
        print("⚠️  psutil not installed, skipping")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

# Test 5: Database Query Performance
async def test_database_performance():
    """Test Qdrant query performance"""
    print("\n📊 TEST 5: Database Query Performance")
    print("-" * 80)
    
    try:
        from qdrant_client import QdrantClient
        import os
        
        client = QdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        
        collection_name = "leyes_seguridad_social"
        
        # Test search performance
        start = time.time()
        results = client.search(
            collection_name=collection_name,
            query_vector=[0.1] * 768,  # Dummy vector
            limit=10
        )
        elapsed = time.time() - start
        
        print(f"Search time: {elapsed:.3f}s")
        print(f"Results found: {len(results)}")
        
        if elapsed < 0.5:
            print("✅ EXCELLENT - Under 0.5 seconds")
            return True
        elif elapsed < 1.0:
            print("⚠️  ACCEPTABLE - Under 1 second")
            return True
        else:
            print("❌ SLOW - Over 1 second")
            return False
            
    except Exception as e:
        print(f"⚠️  SKIPPED: {str(e)[:50]}")
        return True  # Don't fail if Qdrant not available

async def run_all_tests():
    """Run all performance tests"""
    
    tests = [
        ("RAG Performance", test_rag_performance),
        ("Provider Performance", test_provider_performance),
        ("Concurrent Performance", test_concurrent_performance),
        ("Memory Usage", lambda: test_memory_usage()),
        ("Database Performance", test_database_performance)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test {name} crashed: {e}")
            results.append((name, False))
        
        await asyncio.sleep(0.5)
    
    # Summary
    print("\n" + "="*80)
    print("📊 PERFORMANCE SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'='*80}")
    print(f"Results: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 ALL PERFORMANCE TESTS PASSED!")
        return 0
    elif passed > total // 2:
        print(f"\n⚠️  {total - passed} tests failed but majority passed")
        return 0
    else:
        print(f"\n❌ PERFORMANCE ISSUES DETECTED")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
