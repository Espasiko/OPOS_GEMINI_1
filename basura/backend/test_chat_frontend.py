#!/usr/bin/env python3
"""
Test Chat Frontend Integration
Verifica que el endpoint de streaming funciona correctamente
"""

import requests
import json
import time

BACKEND_URL = "http://localhost:8000"

def test_chat_stream():
    """Test streaming chat endpoint"""
    print("🧪 Testing Chat Stream Endpoint...")
    print("=" * 60)
    
    url = f"{BACKEND_URL}/chat/stream"
    payload = {
        "message": "¿Qué es la jubilación anticipada?",
        "conversation_id": "test-conv-123",
        "use_rag": True,
        "top_k": 3,
        "min_score": 0.5
    }
    
    print(f"📤 Request: {json.dumps(payload, indent=2)}")
    print()
    
    try:
        response = requests.post(
            url,
            json=payload,
            stream=True,
            timeout=180
        )
        
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
        
        print("📥 Streaming response:")
        print("-" * 60)
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data = line_str[6:]
                    if data == '[DONE]':
                        print("\n✅ Stream completed")
                        break
                    try:
                        parsed = json.loads(data)
                        if 'choices' in parsed:
                            content = parsed['choices'][0].get('delta', {}).get('content', '')
                            if content:
                                print(content, end='', flush=True)
                                full_response += content
                        elif 'sources' in parsed:
                            print(f"\n\n📚 Sources: {len(parsed['sources'])} documents")
                    except json.JSONDecodeError:
                        pass
        
        print()
        print("-" * 60)
        print(f"✅ Total response length: {len(full_response)} chars")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat_health():
    """Test health endpoint"""
    print("\n🏥 Testing Health Endpoint...")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BACKEND_URL}/chat/health", timeout=30)
        data = response.json()
        
        print(f"Status: {data.get('status')}")
        print(f"Mistral: {data.get('mistral')}")
        print(f"RAG: {data.get('rag')}")
        
        if data.get('status') == 'healthy':
            print("✅ Health check passed")
            return True
        else:
            print("❌ Health check failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Chat Frontend Integration")
    print("=" * 60)
    print()
    
    # Test health first
    health_ok = test_chat_health()
    
    if health_ok:
        # Test streaming
        time.sleep(1)
        stream_ok = test_chat_stream()
        
        print()
        print("=" * 60)
        if stream_ok:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed")
    else:
        print("❌ Backend not healthy, skipping stream test")
