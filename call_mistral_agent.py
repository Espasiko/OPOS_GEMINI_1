#!/usr/bin/env python3
"""
Llamada directa al Agente Mistral Studio
El agente YA tiene configurado MCP y herramientas
"""

import os
from mistralai import Mistral

# Config
MISTRAL_API_KEY = "FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF"
AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"

# Prompt simple - el agente hace todo
prompt = """Genera 10 preguntas tipo test de máxima calidad para oposiciones de Seguridad Social española.

REQUISITOS:
- 4 opciones (A, B, C, D), solo 1 correcta
- Basadas en legislación oficial (usa tus herramientas para buscar)
- Incluye explicación y referencias legales
- Variedad de temas: IT, jubilación, desempleo, procedimiento administrativo

FORMATO JSON para cada pregunta:
{
  "pregunta": "...",
  "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "respuesta_correcta": "A",
  "explicacion": "...",
  "referencias": ["art. X Ley Y"]
}

Genera las 10 preguntas."""

print("🤖 Llamando al Agente Mistral Studio...")
print(f"Agent ID: {AGENT_ID}\n")

client = Mistral(api_key=MISTRAL_API_KEY)

response = client.agents.complete(
    agent_id=AGENT_ID,
    messages=[{
        "role": "user",
        "content": prompt
    }]
)

print("📥 Respuesta del agente:")
print("="*70)
print(response.choices[0].message.content)
print("="*70)
