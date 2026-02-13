#!/usr/bin/env python3
"""
Test Salamandra R1 Q5_K_M - Razonamiento Legal Complejo
Prueba con caso práctico usando MCP BOE y preguntas de razonamiento
"""

import requests
import json
from datetime import datetime

# Configuración
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "salamandra-r1:q5km"

def query_ollama(prompt: str, system: str = None) -> dict:
    """Query Ollama con Salamandra R1"""
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_k": 20,
            "top_p": 0.85,
            "num_ctx": 4096,
            "num_predict": 256  # Respuesta concisa
        }
    }
    
    if system:
        payload["system"] = system
    
    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()
    return response.json()

def test_caso_practico():
    """Test con caso práctico complejo de Seguridad Social"""
    
    print("=" * 80)
    print("🧪 TEST SALAMANDRA R1 Q5_K_M - RAZONAMIENTO LEGAL COMPLEJO")
    print("=" * 80)
    print(f"Modelo: {MODEL}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # CASO PRÁCTICO SIMPLE - SOLO 1 PREGUNTA
    caso_practico = """
CASO PRÁCTICO - INCAPACIDAD TEMPORAL

María, trabajadora por cuenta ajena con 8 años cotizados, sufre un accidente 
de trabajo el 15 de enero de 2026. Está de baja médica por IT.
Su base reguladora es de 2.500€/mes.

PREGUNTA:

¿Cuál es la cuantía del subsidio de IT que recibirá María durante los 
primeros 20 días de baja por accidente de trabajo? 

Explica brevemente el razonamiento legal citando el artículo de la LGSS.
"""
    
    system_prompt = """Eres un experto en Seguridad Social española.

Responde de forma CONCISA:
1. Cita el artículo LGSS aplicable
2. Calcula la cuantía
3. Explica brevemente

Máximo 100 palabras."""
    
    print("\n📋 CASO PRÁCTICO:")
    print(caso_practico)
    print("\n⏳ Procesando con Salamandra R1 Q5_K_M...")
    print("   (Respuesta simple, ~1 minuto)\n")
    
    start_time = datetime.now()
    
    try:
        result = query_ollama(caso_practico, system_prompt)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        response = result.get("response", "")
        
        print("=" * 80)
        print("🤖 RESPUESTA SALAMANDRA R1:")
        print("=" * 80)
        print(response)
        print("=" * 80)
        print(f"\n⏱️  Tiempo de respuesta: {duration:.2f} segundos")
        print(f"📊 Tokens generados: {result.get('eval_count', 'N/A')}")
        print(f"🚀 Tokens/segundo: {result.get('eval_count', 0) / duration if duration > 0 else 0:.2f}")
        
        # Análisis de calidad
        print("\n" + "=" * 80)
        print("📊 ANÁLISIS DE CALIDAD:")
        print("=" * 80)
        
        tiene_citas = "Art." in response or "Artículo" in response
        tiene_numeros = any(c.isdigit() for c in response)
        tiene_estructura = any(str(i) + "." in response for i in range(1, 4))
        longitud_adecuada = len(response) > 500
        
        print(f"✅ Cita artículos legales: {'SÍ' if tiene_citas else 'NO'}")
        print(f"✅ Incluye cálculos/números: {'SÍ' if tiene_numeros else 'NO'}")
        print(f"✅ Estructura clara (1., 2., 3.): {'SÍ' if tiene_estructura else 'NO'}")
        print(f"✅ Longitud adecuada (>500 chars): {'SÍ' if longitud_adecuada else 'NO'}")
        print(f"📏 Longitud total: {len(response)} caracteres")
        
        # Guardar resultado
        output_file = f"salamandra_r1_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "modelo": MODEL,
                "fecha": datetime.now().isoformat(),
                "caso_practico": caso_practico,
                "system_prompt": system_prompt,
                "respuesta": response,
                "duracion_segundos": duration,
                "tokens_generados": result.get('eval_count', 0),
                "tokens_por_segundo": result.get('eval_count', 0) / duration if duration > 0 else 0,
                "analisis_calidad": {
                    "tiene_citas_legales": tiene_citas,
                    "tiene_calculos": tiene_numeros,
                    "estructura_clara": tiene_estructura,
                    "longitud_adecuada": longitud_adecuada,
                    "longitud_total": len(response)
                }
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Resultado guardado en: {output_file}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_caso_practico()
