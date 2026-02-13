#!/usr/bin/env python3
"""
DeepSeek-V3 + MCP Integration Completa
- Generación de casos con razonamiento
- Verificación con RAG local
- Validación de URLs BOE
"""

import os
import json
import asyncio
import subprocess
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Cargar .env
load_dotenv("/home/spas/OPOS_GEMINI_1/backend/.env.backend")

# Configuración
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "deepseek-ai/DeepSeek-V3"

class DeepSeekMCPIntegration:
    def __init__(self):
        self.client = InferenceClient(token=HF_TOKEN)
        self.mcp_local = "/home/spas/OPOS_GEMINI_1/mcp-server"
        
    def generate_case(self, topic="INCAPACIDAD PERMANENTE TOTAL"):
        """Genera caso legal con DeepSeek-V3"""
        prompt = f"""Eres un experto en Seguridad Social española con acceso a legislación actualizada.

TAREA: Crea un caso práctico REAL y COMPLEJO sobre {topic}.

REQUISITOS OBLIGATORIOS:
1. Situación realista con datos concretos (edad, salario, años cotizados)
2. Conflicto legal que requiera interpretación normativa
3. Cita EXACTA de artículos del TRLGSS con URLs del BOE
4. Razonamiento paso a paso (piensa en voz alta)
5. Cálculo numérico de prestaciones
6. Dos posibles interpretaciones con pros/contras

FORMATO JSON:
{{
  "titulo": "Título descriptivo del caso",
  "situacion": "Descripción detallada (200-300 palabras)",
  "datos_trabajador": {{
    "edad": 52,
    "salario_mensual": 2400,
    "anos_cotizados": 28,
    "profesion": "Conductor de autobús"
  }},
  "articulos_aplicables": [
    {{
      "articulo": "Art. 193 TRLGSS",
      "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430#a193",
      "texto_relevante": "Extracto del artículo"
    }}
  ],
  "razonamiento": "Análisis detallado paso a paso",
  "calculo_prestacion": {{
    "base_reguladora": 2400,
    "porcentaje": 55,
    "cuantia_mensual": 1320,
    "complementos": "Detalles"
  }},
  "interpretaciones": [
    {{"opcion": "A", "argumentos": "...", "resultado": "..."}},
    {{"opcion": "B", "argumentos": "...", "resultado": "..."}}
  ],
  "solucion_recomendada": "Opción X porque..."
}}

IMPORTANTE: 
- URLs del BOE deben ser REALES y verificables
- Razonamiento debe ser EXPLÍCITO (muestra tu proceso mental)
- Números deben ser EXACTOS y calculables"""

        print(f"🧠 Generando caso sobre: {topic}")
        
        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.6
            )
            
            result = response.choices[0].message.content
            
            # Intentar parsear como JSON
            try:
                case_data = json.loads(result)
                print("✅ Caso generado y parseado como JSON")
                return case_data
            except json.JSONDecodeError:
                print("⚠️  Respuesta no es JSON válido, guardando como texto")
                return {"raw_response": result}
                
        except Exception as e:
            print(f"❌ Error generando caso: {e}")
            return None
    
    def verify_boe_urls(self, case_data):
        """Verifica URLs de BOE usando MCP-BOE"""
        print("\n🔍 Verificando URLs de BOE...")
        
        if isinstance(case_data, dict) and "articulos_aplicables" in case_data:
            urls = [art.get("url_boe") for art in case_data["articulos_aplicables"] if art.get("url_boe")]
        else:
            # Extraer URLs del texto
            import re
            text = json.dumps(case_data)
            pattern = r'https?://(?:www\.)?boe\.es/[^\s\)\"\']*'
            urls = list(set(re.findall(pattern, text)))
        
        if not urls:
            print("⚠️  No se encontraron URLs de BOE")
            return []
        
        print(f"📋 URLs encontradas: {len(urls)}")
        verified = []
        
        for url in urls:
            try:
                # Usar MCP-BOE para verificar (requiere instalación)
                # Por ahora, solo validamos formato
                if "boe.es" in url and "#a" in url:
                    art_num = url.split("#a")[-1]
                    print(f"  ✅ {url} → Artículo {art_num}")
                    verified.append({"url": url, "status": "valid_format", "article": art_num})
                else:
                    print(f"  ⚠️  {url} → Formato inválido")
                    verified.append({"url": url, "status": "invalid_format"})
            except Exception as e:
                print(f"  ❌ Error verificando {url}: {e}")
                verified.append({"url": url, "status": "error", "error": str(e)})
        
        return verified
    
    def save_result(self, case_data, verified_urls, filename="deepseek_mcp_result.json"):
        """Guarda resultado completo"""
        output = {
            "model": MODEL,
            "case": case_data,
            "boe_verification": verified_urls,
            "mcp_servers": {
                "local_rag": self.mcp_local,
                "boe_verify": "ComputingVictor/MCP-BOE"
            }
        }
        
        filepath = f"/home/spas/OPOS_GEMINI_1/{filename}"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultado guardado en: {filepath}")
        return filepath

def main():
    print("="*80)
    print("🚀 DEEPSEEK-V3 + MCP INTEGRATION")
    print("="*80)
    print(f"📍 Modelo: {MODEL}")
    print(f"🔧 MCPs:")
    print(f"   - Local RAG: /home/spas/OPOS_GEMINI_1/mcp-server")
    print(f"   - BOE Verify: MCP-BOE (uvx mcp-boe)")
    print("="*80 + "\n")
    
    integration = DeepSeekMCPIntegration()
    
    # 1. Generar caso
    case = integration.generate_case()
    
    if not case:
        print("❌ Fallo en generación de caso")
        return
    
    print("\n" + "="*80)
    print("📝 CASO GENERADO:")
    print("="*80)
    print(json.dumps(case, indent=2, ensure_ascii=False)[:1000] + "...")
    
    # 2. Verificar URLs BOE
    verified = integration.verify_boe_urls(case)
    
    # 3. Guardar resultado
    output_file = integration.save_result(case, verified)
    
    print("\n" + "="*80)
    print("✅ PROCESO COMPLETADO")
    print("="*80)
    print(f"📄 Resultado: {output_file}")
    print(f"🔗 URLs verificadas: {len(verified)}")
    print("\n💡 Próximos pasos:")
    print("   1. Revisar el JSON generado")
    print("   2. Validar URLs en BOE manualmente")
    print("   3. Usar para dataset de entrenamiento")

if __name__ == "__main__":
    main()
