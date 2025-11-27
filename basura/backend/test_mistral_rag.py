"""
Test de integración: Mistral VPS + RAG
"""
import asyncio
import httpx

async def test_chat_with_rag():
    """Test chat con RAG usando Mistral VPS"""
    
    print("🧪 TEST: Chat con RAG + Mistral VPS")
    print("=" * 60)
    
    # Configuración
    backend_url = "http://localhost:8000"
    
    # Test 1: Health check
    print("\n1️⃣ Health Check...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    
    # Test 2: Chat health
    print("\n2️⃣ Chat Health...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/chat/health")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Mistral: {data.get('mistral')}")
        print(f"   RAG: {data.get('rag')}")
        print(f"   URL: {data.get('mistral_url')}")
    
    # Test 3: Chat con RAG
    print("\n3️⃣ Chat con RAG...")
    print("   Pregunta: '¿Qué es la incapacidad temporal?'")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{backend_url}/chat/message",
            json={
                "message": "¿Qué es la incapacidad temporal?",
                "conversation_id": "test-123",
                "use_rag": True,
                "top_k": 3,
                "min_score": 0.5
            }
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n   ✅ Respuesta recibida:")
            print(f"   {data.get('response', '')[:200]}...")
            print(f"\n   📚 Fuentes encontradas: {len(data.get('sources', []))}")
            for i, source in enumerate(data.get('sources', [])[:3], 1):
                print(f"      {i}. {source.get('norma')} (score: {source.get('score')})")
        else:
            print(f"   ❌ Error: {response.text}")
    
    print("\n" + "=" * 60)
    print("✅ Test completado")

if __name__ == "__main__":
    asyncio.run(test_chat_with_rag())
