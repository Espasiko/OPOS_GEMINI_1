#!/usr/bin/env python3
"""
Test simple del agente Mistral Studio
Verifica que el agente funciona correctamente antes de generar las 10 Q&A
"""

from mistralai import Mistral

# Configuración
MISTRAL_API_KEY = "xeE9w6vpnlANxBU9T90sC62zQnM0AYhZ"
AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"

print("🧪 TEST AGENTE MISTRAL STUDIO")
print("="*70)
print(f"Agent ID: {AGENT_ID}\n")

client = Mistral(api_key=MISTRAL_API_KEY)

print("📤 Enviando pregunta de prueba...")
print("Pregunta: ¿Cuál es la edad de jubilación ordinaria en 2024?")
print("          Usa buscar_rag para verificar.\n")

try:
    response = client.agents.complete(
        agent_id=AGENT_ID,
        messages=[{
            "role": "user",
            "content": "¿Cuál es la edad de jubilación ordinaria en 2024? Usa buscar_rag para verificar en Qdrant y PostgreSQL."
        }]
    )
    
    print("📥 RESPUESTA DEL AGENTE:")
    print("="*70)
    print(response.choices[0].message.content)
    print("="*70)
    
    print("\n✅ TEST EXITOSO - El agente funciona correctamente")
    print("Puedes ejecutar: python generate_10_qa_mistral_studio.py")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    print("\nVerifica:")
    print("1. API Key de Mistral es correcta")
    print("2. Agent ID es correcto")
    print("3. El agente está configurado en Mistral Studio")
