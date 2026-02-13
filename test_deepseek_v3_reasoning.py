#!/usr/bin/env python3
"""
Test DeepSeek-V3 Reasoning con MCPs
- MCP Local: RAG Qdrant (/home/spas/OPOS_GEMINI_1/mcp-server)
- MCP BOE: Verificación legislación (ComputingVictor/MCP-BOE)
"""

import os
import json
import asyncio
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Cargar .env
load_dotenv("/home/spas/OPOS_GEMINI_1/backend/.env.backend")

# Configuración
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "deepseek-ai/DeepSeek-V3"  # Modelo de razonamiento

# Cliente HF
client = InferenceClient(token=HF_TOKEN)

def create_legal_case_prompt():
    """Prompt para generar caso legal con razonamiento"""
    return """Eres un experto en Seguridad Social española. 

TAREA: Crea un caso práctico complejo sobre INCAPACIDAD PERMANENTE TOTAL que requiera razonamiento profundo.

REQUISITOS:
1. Situación: Trabajador con enfermedad crónica + accidente laboral
2. Dilema: Conflicto entre normativa de IT y IPT
3. Cita artículos específicos del TRLGSS
4. Incluye cálculo de prestaciones
5. Plantea 2 interpretaciones posibles

FORMATO:
{
  "caso": "Descripción del caso (200 palabras)",
  "articulos_relevantes": ["Art. X TRLGSS", "Art. Y TRLGSS"],
  "razonamiento": "Análisis paso a paso",
  "solucion_propuesta": "Resolución con cálculos",
  "verificacion_boe": ["URL BOE Art. X", "URL BOE Art. Y"]
}

IMPORTANTE: Usa razonamiento explícito (piensa en voz alta) antes de dar la respuesta final."""

def test_deepseek_reasoning():
    """Test básico de DeepSeek-V3"""
    print("🧠 Testing DeepSeek-V3 Reasoning...")
    print(f"📡 Modelo: {MODEL}")
    print(f"🔑 Token HF: {HF_TOKEN[:20]}...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": create_legal_case_prompt()
            }],
            max_tokens=4000,
            temperature=0.6,  # Recomendado por DeepSeek
            stream=False
        )
        
        result = response.choices[0].message.content
        
        print("\n" + "="*80)
        print("📝 RESPUESTA DEEPSEEK-V3:")
        print("="*80)
        print(result)
        print("\n" + "="*80)
        
        # Guardar resultado
        output_file = "/home/spas/OPOS_GEMINI_1/deepseek_v3_test_result.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "model": MODEL,
                "prompt": create_legal_case_prompt(),
                "response": result,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else "N/A"
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Resultado guardado en: {output_file}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_boe_urls(response_text):
    """Extrae URLs de BOE de la respuesta"""
    import re
    # Patrón para URLs del BOE
    pattern = r'https?://(?:www\.)?boe\.es/[^\s\)\"\']*'
    urls = re.findall(pattern, response_text)
    return list(set(urls))  # Eliminar duplicados

async def verify_with_mcp_boe(boe_urls):
    """
    Verificar URLs de BOE usando MCP-BOE
    NOTA: Requiere que MCP-BOE esté instalado y corriendo
    """
    print("\n🔍 Verificando URLs de BOE con MCP...")
    
    if not boe_urls:
        print("⚠️  No se encontraron URLs de BOE para verificar")
        return
    
    # TODO: Integrar con MCP-BOE cuando esté instalado
    # Por ahora, solo mostramos las URLs encontradas
    print(f"📋 URLs encontradas ({len(boe_urls)}):")
    for url in boe_urls:
        print(f"  - {url}")
    
    print("\n💡 Para verificar estas URLs, instala MCP-BOE:")
    print("   uvx mcp-boe")

def main():
    print("="*80)
    print("🚀 DEEPSEEK-V3 REASONING TEST")
    print("="*80)
    print(f"📍 Modelo: {MODEL}")
    print(f"🔧 MCPs disponibles:")
    print(f"   - Local RAG: /home/spas/OPOS_GEMINI_1/mcp-server")
    print(f"   - BOE Verify: ComputingVictor/MCP-BOE (pendiente instalación)")
    print("="*80 + "\n")
    
    # Test DeepSeek
    result = test_deepseek_reasoning()
    
    if result:
        # Extraer y verificar URLs de BOE
        boe_urls = extract_boe_urls(result)
        asyncio.run(verify_with_mcp_boe(boe_urls))
        
        print("\n✅ Test completado exitosamente")
    else:
        print("\n❌ Test falló")

if __name__ == "__main__":
    main()
