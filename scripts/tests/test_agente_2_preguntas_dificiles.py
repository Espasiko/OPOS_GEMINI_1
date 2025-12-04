"""
Test del Agente Mistral - Generar 2 preguntas muy difíciles
"""
import os
import sys

# Añadir backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Cargar variables de entorno
from pathlib import Path
env_path = Path(__file__).parent / "backend" / ".env.backend"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from mistralai import Mistral

# Configuración
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "").strip()
MISTRAL_MODEL = "mistral-large-latest"

# System prompt CORRECTO (sin opciones múltiples)
SYSTEM_PROMPT = """Eres un experto en oposiciones de Seguridad Social en España.

## Cómo debes trabajar

1. Genera UNA pregunta con UNA respuesta correcta (SIN opciones múltiples)
2. Verifica ley y artículos - deben existir en BOE
3. Devuelve SOLO: pregunta + respuesta + ley + artículos
4. NO resúmenes, NO explicaciones largas

## Formato de respuestas - FORMATO EXACTO:

PREGUNTA: [Pregunta directa sobre legislación]
RESPUESTA: [Respuesta correcta verificada]
LEY: [Nombre de la ley]
ARTÍCULO: [Art. X, Y, Z]

## EJEMPLO:

PREGUNTA: ¿Cuál es la edad ordinaria de jubilación en 2024?
RESPUESTA: 66 años y 6 meses
LEY: Ley General de la Seguridad Social
ARTÍCULO: Art. 205.1.a

## REGLAS ESTRICTAS:
- ❌ NO opciones múltiples (A, B, C, D)
- ❌ NO resúmenes
- ❌ NO explicaciones largas
- ✅ UNA pregunta, UNA respuesta correcta verificada
- ✅ Ley y artículos VERIFICADOS
"""

def main():
    print("=" * 60)
    print("TEST AGENTE MISTRAL - 2 PREGUNTAS MUY DIFÍCILES")
    print("=" * 60)
    
    if not MISTRAL_API_KEY:
        print("❌ ERROR: MISTRAL_API_KEY no configurada")
        return
    
    print(f"✅ API Key encontrada: {MISTRAL_API_KEY[:10]}...")
    
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    # Mensaje del usuario
    user_message = "Genera 2 preguntas MUY DIFÍCILES sobre Seguridad Social española. Nivel oposición avanzado."
    
    print(f"\n📝 Enviando: {user_message}")
    print("-" * 60)
    
    try:
        response = client.chat.complete(
            model=MISTRAL_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3
        )
        
        if response.choices:
            respuesta = response.choices[0].message.content
            print("\n🤖 RESPUESTA DEL AGENTE:")
            print("=" * 60)
            print(respuesta)
            print("=" * 60)
            
            # Verificar formato
            print("\n📊 VERIFICACIÓN DE FORMATO:")
            if "PREGUNTA:" in respuesta and "RESPUESTA:" in respuesta:
                print("✅ Formato correcto (PREGUNTA + RESPUESTA)")
            else:
                print("⚠️ Formato incorrecto")
            
            if "A)" in respuesta or "B)" in respuesta or "C)" in respuesta or "D)" in respuesta:
                print("❌ ERROR: Contiene opciones múltiples (A/B/C/D)")
            else:
                print("✅ Sin opciones múltiples")
            
            if "LEY:" in respuesta or "ARTÍCULO:" in respuesta:
                print("✅ Incluye referencias legales")
            else:
                print("⚠️ Faltan referencias legales")
                
            # Tokens usados
            if hasattr(response, 'usage'):
                print(f"\n📈 Tokens usados: {response.usage.total_tokens}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
