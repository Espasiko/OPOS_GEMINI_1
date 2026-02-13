"""
Test de conexión con Salamandra VPS
"""
import asyncio
import sys
sys.path.insert(0, 'backend')

from agents.salamandra_client import get_salamandra_client
import logging

logging.basicConfig(level=logging.INFO)

async def test_vps():
    print("=" * 60)
    print("TEST: Conexión con Salamandra VPS")
    print("=" * 60)
    
    client = get_salamandra_client()
    
    # Test simple
    prompt = """Genera un caso práctico breve sobre Incapacidad Temporal.

DATOS:
- Base reguladora: 1500€
- Día de baja: 10
- Tipo: Enfermedad Común

Calcula la prestación del día 10 y explica brevemente."""
    
    system = "Eres experto en Seguridad Social española. Responde de forma concisa y precisa."
    
    try:
        print("\n📤 Enviando prompt a VPS...")
        print(f"Prompt: {prompt[:100]}...")
        
        response = await client.generate(
            prompt=prompt,
            system_prompt=system,
            temperature=0.1,
            max_tokens=500
        )
        
        print("\n✅ RESPUESTA RECIBIDA:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        print(f"\n📊 Longitud: {len(response)} caracteres")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_vps())
    sys.exit(0 if success else 1)
