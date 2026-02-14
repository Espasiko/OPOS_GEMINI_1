#!/usr/bin/env python3
"""
Debug: Ver qué devuelve Salamandra en raw
"""
import requests
import json

base_url = "http://localhost:11434"
model = "salamandra-r1:q5km"

system_prompt = """Eres experto en casos SS. Devuelve JSON válido solamente."""

user_prompt = """Genera JSON de caso IT EC día 15.
{
  "pregunta": "¿Subsidio día 15 IT EC con base 1500€?",
  "opciones": {"A": "30€", "B": "37,50€", "C": "50€", "D": "0€"},
  "respuesta_correcta": "A"
}"""

print("🔍 Consultando Salamandra...")
response = requests.post(
    f"{base_url}/api/generate",
    json={
        "model": model,
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False,
        "temperature": 0.1,
    },
    timeout=60
)

resultado = response.json()
respuesta_raw = resultado.get("response", "")

print("=" * 80)
print("RAW RESPONSE:")
print("=" * 80)
print(respuesta_raw)
print("=" * 80)

# Intentar parser
try:
    import re
    json_match = re.search(r'\{[^{}]*\}', respuesta_raw, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        print(f"\nJSON encontrado:\n{json_str}")
        parsed = json.loads(json_str)
        print(f"\n✅ JSON válido:\n{json.dumps(parsed, indent=2)}")
    else:
        print("\n❌ No se encontró JSON")
except Exception as e:
    print(f"\n❌ Error: {e}")
