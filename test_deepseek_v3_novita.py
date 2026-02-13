#!/usr/bin/env python3
"""
Test DeepSeek V3.1 (R1) via Novita AI
Modelo: deepseek-ai/DeepSeek-V3
Precio: $0.27/M input + $1.00/M output
"""

import os
import json
import requests
from dotenv import load_dotenv

# Cargar .env
load_dotenv("/home/spas/OPOS_GEMINI_1/backend/.env.backend")

# Configuración Novita
NOVITA_API_KEY = os.getenv("NOVITA_API_KEY")
NOVITA_BASE_URL = "https://api.novita.ai/v3/openai"
MODEL = "deepseek-ai/deepseek-v3"  # DeepSeek V3.1

def test_novita_connection():
    """Test simple: enviar 'Hola' y ver respuesta"""
    print("🚀 Testing DeepSeek V3.1 via Novita AI")
    print(f"📡 Modelo: {MODEL}")
    print(f"🔑 API Key: {NOVITA_API_KEY[:20] if NOVITA_API_KEY else 'NOT FOUND'}...")
    print("="*80)
    
    if not NOVITA_API_KEY:
        print("❌ ERROR: NOVITA_API_KEY no encontrada en .env.backend")
        print("💡 Añade: NOVITA_API_KEY=tu_key_aqui")
        return None
    
    headers = {
        "Authorization": f"Bearer {NOVITA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": "Hola, ¿estás funcionando correctamente?"
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7,
        "stream": False
    }
    
    try:
        print("\n📤 Enviando request a Novita...")
        response = requests.post(
            f"{NOVITA_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Extraer respuesta
            message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            usage = data.get("usage", {})
            
            print("\n" + "="*80)
            print("✅ RESPUESTA DE DEEPSEEK V3.1:")
            print("="*80)
            print(message)
            print("\n" + "="*80)
            print("📊 USAGE:")
            print(f"   Input tokens:  {usage.get('prompt_tokens', 'N/A')}")
            print(f"   Output tokens: {usage.get('completion_tokens', 'N/A')}")
            print(f"   Total tokens:  {usage.get('total_tokens', 'N/A')}")
            print("="*80)
            
            # Guardar resultado
            output_file = "/home/spas/OPOS_GEMINI_1/deepseek_v3_novita_test.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({
                    "model": MODEL,
                    "provider": "Novita AI",
                    "request": payload,
                    "response": message,
                    "usage": usage,
                    "status": "success"
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Resultado guardado en: {output_file}")
            return data
            
        else:
            print(f"\n❌ ERROR {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_novita_connection()
