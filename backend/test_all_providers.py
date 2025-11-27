#!/usr/bin/env python3
"""
Test All LLM Providers
Prueba cada proveedor configurado
"""

import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

# Load .env.backend
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env.backend'
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Loaded environment from: {env_path}\n")
except ImportError:
    print("⚠️  python-dotenv not installed\n")
except Exception as e:
    print(f"❌ Error loading .env.backend: {e}\n")

from agents.llm_providers import PROVIDERS

async def test_provider(provider_id: str):
    """Test un proveedor específico"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {provider_id}")
    print(f"{'='*60}")
    
    try:
        provider = PROVIDERS[provider_id]
        info = provider.get_info()
        
        print(f"Provider: {info['provider']}")
        print(f"Model: {info['model']}")
        print(f"Speed: {info['speed']}")
        print(f"Cost: {info['cost']}")
        print(f"Configured: {info['configured']}")
        
        if not info['configured']:
            print("⚠️  SKIPPED - Not configured")
            return False
        
        # Test simple
        messages = [
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": "Di 'Hola' en una palabra."}
        ]
        
        print("\n📤 Sending test message...")
        response = ""
        
        try:
            async for chunk in provider.generate_stream(messages, temperature=0.7, max_tokens=50):
                response += chunk
                print(chunk, end='', flush=True)
            
            print(f"\n\n✅ SUCCESS - Response length: {len(response)} chars")
            return True
            
        except Exception as e:
            print(f"\n\n❌ FAILED - {str(e)[:200]}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR - {str(e)[:200]}")
        return False

async def test_all():
    """Test todos los proveedores"""
    print("🚀 Testing All LLM Providers")
    print("="*60)
    
    results = {}
    
    for provider_id in PROVIDERS.keys():
        success = await test_provider(provider_id)
        results[provider_id] = success
        await asyncio.sleep(1)  # Pausa entre tests
    
    # Resumen
    print(f"\n\n{'='*60}")
    print("📊 SUMMARY")
    print(f"{'='*60}")
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for provider_id, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {provider_id}")
    
    print(f"\n{success_count}/{total_count} providers working")
    
    if success_count == 0:
        print("\n⚠️  WARNING: No providers are working!")
        print("Check your API keys in .env.backend")
    elif success_count < total_count:
        print(f"\n⚠️  {total_count - success_count} providers failed")
    else:
        print("\n🎉 All providers working!")

if __name__ == "__main__":
    asyncio.run(test_all())
