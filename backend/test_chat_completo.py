"""
Test completo: Chat con RAG + Mistral VPS
"""
import requests
import json

print("🧪 TEST COMPLETO: Chat con RAG + Mistral VPS")
print("=" * 70)

# Test 1: Health checks
print("\n1️⃣ Backend Health...")
response = requests.get("http://localhost:8000/health")
print(f"   Status: {response.status_code}")
print(f"   {json.dumps(response.json(), indent=2)}")

print("\n2️⃣ Chat Health...")
response = requests.get("http://localhost:8000/chat/health")
print(f"   Status: {response.status_code}")
data = response.json()
print(f"   Mistral: {data['mistral']} ✅" if data['mistral'] == 'up' else f"   Mistral: {data['mistral']} ❌")
print(f"   RAG: {data['rag']} ✅" if data['rag'] == 'up' else f"   RAG: {data['rag']} ❌")

# Test 2: Chat SIN RAG
print("\n3️⃣ Chat SIN RAG (solo Mistral)...")
print("   Pregunta: 'Hola, ¿cómo estás?'")
response = requests.post(
    "http://localhost:8000/chat/message",
    json={
        "message": "Hola, ¿cómo estás?",
        "conversation_id": "test-sin-rag",
        "use_rag": False
    },
    timeout=60
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   ✅ Respuesta: {data['response'][:150]}...")
else:
    print(f"   ❌ Error: {response.text}")

# Test 3: Chat CON RAG
print("\n4️⃣ Chat CON RAG (Mistral + RAG)...")
print("   Pregunta: '¿Qué es la incapacidad temporal?'")
response = requests.post(
    "http://localhost:8000/chat/message",
    json={
        "message": "¿Qué es la incapacidad temporal?",
        "conversation_id": "test-con-rag",
        "use_rag": True,
        "top_k": 3,
        "min_score": 0.5
    },
    timeout=60
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   ✅ Respuesta: {data['response'][:200]}...")
    print(f"\n   📚 Fuentes encontradas: {len(data['sources'])}")
    for i, source in enumerate(data['sources'], 1):
        print(f"      {i}. {source['norma']}")
        if source.get('articulo'):
            print(f"         Artículo: {source['articulo']}")
        print(f"         Score: {source['score']}")
else:
    print(f"   ❌ Error: {response.text}")

print("\n" + "=" * 70)
print("✅ Test completado")
