#!/usr/bin/env python3
"""
Test E2E Completo - OpositAIA
Prueba end-to-end de toda la aplicación
"""

import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "backend"))

# Load environment
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / "backend" / ".env.backend"
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Environment loaded from: {env_path}\n")
except Exception as e:
    print(f"⚠️  Could not load environment: {e}\n")

import os
import json
from datetime import datetime

# Test results
test_results = {
    "timestamp": datetime.now().isoformat(),
    "tests": {},
    "summary": {}
}

def log_test(name: str, status: str, details: str = ""):
    """Log test result"""
    symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"{symbol} {name}: {status}")
    if details:
        print(f"   {details}")
    test_results["tests"][name] = {"status": status, "details": details}

async def test_1_environment():
    """Test 1: Verificar variables de entorno"""
    print("\n" + "="*60)
    print("TEST 1: Environment Variables")
    print("="*60)
    
    required_vars = [
        "QDRANT_URL",
        "QDRANT_API_KEY",
        "MISTRAL_API_KEY"
    ]
    
    optional_vars = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            log_test(f"ENV: {var}", "FAIL", "Missing required variable")
        else:
            log_test(f"ENV: {var}", "PASS", "Configured")
    
    for var in optional_vars:
        if os.getenv(var):
            log_test(f"ENV: {var}", "PASS", "Configured (optional)")
        else:
            log_test(f"ENV: {var}", "SKIP", "Not configured (optional)")
    
    return len(missing) == 0

async def test_2_qdrant_connection():
    """Test 2: Conexión a Qdrant"""
    print("\n" + "="*60)
    print("TEST 2: Qdrant Connection")
    print("="*60)
    
    try:
        from qdrant_client import QdrantClient
        
        client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        
        collections = client.get_collections()
        log_test("Qdrant Connection", "PASS", f"Connected - {len(collections.collections)} collections")
        
        # Check for our collection
        collection_name = "leyes_seguridad_social"
        try:
            info = client.get_collection(collection_name)
            log_test(f"Collection: {collection_name}", "PASS", f"{info.points_count} points")
            return True
        except Exception as e:
            log_test(f"Collection: {collection_name}", "FAIL", str(e)[:100])
            return False
            
    except Exception as e:
        log_test("Qdrant Connection", "FAIL", str(e)[:100])
        return False

async def test_3_llm_providers():
    """Test 3: Proveedores LLM"""
    print("\n" + "="*60)
    print("TEST 3: LLM Providers")
    print("="*60)
    
    try:
        from backend.agents.llm_providers import PROVIDERS
        
        working_providers = []
        
        for provider_id, provider in PROVIDERS.items():
            info = provider.get_info()
            
            if not info['configured']:
                log_test(f"Provider: {provider_id}", "SKIP", "Not configured")
                continue
            
            try:
                messages = [{"role": "user", "content": "Di 'OK'"}]
                response = ""
                async for chunk in provider.generate_stream(messages, max_tokens=10):
                    response += chunk
                
                if response:
                    log_test(f"Provider: {provider_id}", "PASS", f"Response: {response[:30]}")
                    working_providers.append(provider_id)
                else:
                    log_test(f"Provider: {provider_id}", "FAIL", "Empty response")
                    
            except Exception as e:
                log_test(f"Provider: {provider_id}", "FAIL", str(e)[:100])
        
        return len(working_providers) > 0
        
    except Exception as e:
        log_test("LLM Providers", "FAIL", str(e)[:100])
        return False

async def test_4_rag_system():
    """Test 4: Sistema RAG"""
    print("\n" + "="*60)
    print("TEST 4: RAG System")
    print("="*60)
    
    try:
        from backend.agents.rag_agent_v2 import RAGAgentV2
        
        agent = RAGAgentV2()
        
        # Test query
        query = "¿Qué es la incapacidad temporal?"
        print(f"\n📤 Query: {query}")
        
        result = await agent.query(query, provider="mistral")
        
        if result and result.get("answer"):
            answer_len = len(result["answer"])
            sources_count = len(result.get("sources", []))
            log_test("RAG Query", "PASS", f"Answer: {answer_len} chars, Sources: {sources_count}")
            
            # Verify sources
            if sources_count > 0:
                log_test("RAG Sources", "PASS", f"Found {sources_count} relevant sources")
            else:
                log_test("RAG Sources", "WARN", "No sources found")
            
            return True
        else:
            log_test("RAG Query", "FAIL", "No answer generated")
            return False
            
    except Exception as e:
        log_test("RAG System", "FAIL", str(e)[:100])
        return False

async def test_5_ai_functions():
    """Test 5: Funciones de IA (resumen, esquema, etc.)"""
    print("\n" + "="*60)
    print("TEST 5: AI Functions")
    print("="*60)
    
    try:
        from backend.routers.ai_functions import generate_summary
        
        test_text = """
        La incapacidad temporal es una prestación económica que cubre la pérdida de 
        rentas del trabajador cuando está temporalmente incapacitado para trabajar 
        debido a enfermedad común o accidente.
        """
        
        # Test summary generation
        print("\n📤 Testing summary generation...")
        result = await generate_summary(test_text, "mistral")
        
        if result and result.get("summary"):
            summary_len = len(result["summary"])
            log_test("AI Function: Summary", "PASS", f"Generated {summary_len} chars")
            return True
        else:
            log_test("AI Function: Summary", "FAIL", "No summary generated")
            return False
            
    except Exception as e:
        log_test("AI Functions", "FAIL", str(e)[:100])
        return False

async def test_6_frontend_integration():
    """Test 6: Integración Frontend (verificar archivos)"""
    print("\n" + "="*60)
    print("TEST 6: Frontend Integration")
    print("="*60)
    
    try:
        # Check key frontend files
        frontend_files = [
            "App.tsx",
            "components/ChatView.tsx",
            "components/ModelSelector.tsx",
            "contexts/ModelContext.tsx",
            "services/backendService.ts",
            "utils/providers.ts",
            "hooks/useAIProvider.ts"
        ]
        
        missing = []
        for file in frontend_files:
            path = Path(__file__).parent / file
            if path.exists():
                log_test(f"Frontend: {file}", "PASS", "File exists")
            else:
                log_test(f"Frontend: {file}", "FAIL", "File missing")
                missing.append(file)
        
        return len(missing) == 0
        
    except Exception as e:
        log_test("Frontend Integration", "FAIL", str(e)[:100])
        return False

async def test_7_backend_api():
    """Test 7: Backend API endpoints"""
    print("\n" + "="*60)
    print("TEST 7: Backend API")
    print("="*60)
    
    try:
        # Check backend files
        backend_files = [
            "backend/main.py",
            "backend/routers/rag_v2.py",
            "backend/routers/ai_functions.py",
            "backend/agents/rag_agent_v2.py",
            "backend/agents/llm_providers.py"
        ]
        
        missing = []
        for file in backend_files:
            path = Path(__file__).parent / file
            if path.exists():
                log_test(f"Backend: {file}", "PASS", "File exists")
            else:
                log_test(f"Backend: {file}", "FAIL", "File missing")
                missing.append(file)
        
        return len(missing) == 0
        
    except Exception as e:
        log_test("Backend API", "FAIL", str(e)[:100])
        return False

async def run_all_tests():
    """Ejecutar todos los tests E2E"""
    print("\n" + "="*80)
    print("🚀 OPOSITAIA - TEST E2E COMPLETO")
    print("="*80)
    print(f"Timestamp: {test_results['timestamp']}")
    
    tests = [
        ("Environment", test_1_environment),
        ("Qdrant", test_2_qdrant_connection),
        ("LLM Providers", test_3_llm_providers),
        ("RAG System", test_4_rag_system),
        ("AI Functions", test_5_ai_functions),
        ("Frontend", test_6_frontend_integration),
        ("Backend API", test_7_backend_api)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test {name} crashed: {e}")
            results.append((name, False))
        
        await asyncio.sleep(0.5)
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'='*80}")
    print(f"Results: {passed}/{total} tests passed ({passed*100//total}%)")
    
    test_results["summary"] = {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "percentage": passed * 100 // total
    }
    
    # Save results
    results_file = Path(__file__).parent / "test_e2e_results.json"
    with open(results_file, "w") as f:
        json.dump(test_results, f, indent=2)
    print(f"\n📄 Results saved to: {results_file}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is fully operational.")
        return 0
    elif passed > 0:
        print(f"\n⚠️  {total - passed} tests failed. Check details above.")
        return 1
    else:
        print("\n❌ ALL TESTS FAILED! System needs attention.")
        return 2

if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
