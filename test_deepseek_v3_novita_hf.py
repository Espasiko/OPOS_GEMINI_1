#!/usr/bin/env python3
"""
Test DeepSeek V3.1 via Novita usando HuggingFace Token
Modelo: deepseek-ai/deepseek-v3 (vía Novita endpoint en HF)
"""

import os
import json
from datetime import datetime
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Cargar .env
load_dotenv("/home/spas/OPOS_GEMINI_1/backend/.env.backend")

# Configuración
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "deepseek-ai/deepseek-v3"  # DeepSeek V3.1

# System Prompt
SYSTEM_PROMPT = """Eres un preparador experto de oposiciones de Seguridad Social y AGE en España con 20 años de experiencia. Tu especialidad es crear casos prácticos tipo examen oficial que:

1. Enseñen razonamiento jurídico profundo (no solo memorización)
2. Incluyan trampas realistas como en los exámenes oficiales que confundan los opositores
3. TUS casos estén 100% verificados con la normativa del BOE
4. Sigan un formato estructurado de máxima calidad didáctica y estricta información contrastada y real 

REGLAS ESTRICTAS:
- NUNCA inventes artículos, conceptos, fechas, cantidades o leyes
- SIEMPRE cita el BOE con URL verificada
- Fechas ESPECÍFICAS (dd/mm/aaaa), no genéricas
- Cantidades EXACTAS (años, meses, euros)
- Sin contradicciones internas
- Razonamiento paso a paso completo
- distingues siempre días hábiles y naturales, validas y usas las fórmulas correctas cuando es necesario
- aplicas correctamente salario y cotización, porcentajes reales y bases imponibles, reguladoras etc. detalles importantes
- siempre usas la posición de la respuesta correcta equilibradamente, por ej. a-25% b-25% c-25% y d-25%
"""

# User Prompt para caso de prueba
USER_PROMPT = """Genera un caso práctico de oposición siguiendo EXACTAMENTE este formato JSON:

TEMA: Incapacidad Permanente Total
MATERIA: Seguridad Social
DIFICULTAD: alta
TIPO DE TRAMPA: confusion_requisitos_alta_vs_no_alta

FORMATO OBLIGATORIO:
{
  "id": "SS_IPT_001",
  "categoria": "Seguridad Social",
  "subcategoria": "Incapacidad Permanente Total",
  "dificultad": "alta",
  "tipo_trampa": "confusion_requisitos_alta_vs_no_alta",
  "fuente": "Caso creado basado en TRLGSS",
  "fecha_creacion": "12/01/2026",
  
  "enunciado": "REDACTA UN CASO COMPLETO con:
    - Contexto personal (nombre, edad, situación laboral)
    - Fechas ESPECÍFICAS (ej: 15 de marzo de 2025)
    - Cantidades EXACTAS (ej: 22 años 6 meses y 3 días cotizados, 1.800€)
    - Hechos cronológicos ordenados
    - Pregunta final clara
    
    REQUISITOS:
    - Mínimo 150 palabras
    - Sin ambigüedades
    - Sin contradicciones
    - Datos suficientes para resolver",
  
  "opciones": {
    "a": "Opción con trampa común tipo 1 (confusión de requisitos)",
    "b": "Opción con trampa común tipo 2 (aplicación incorrecta norma)",
    "c": "Respuesta CORRECTA (debe ser la más difícil de identificar)",
    "d": "Distractor obvio (error fácil de descartar)"
  },
  
  "respuesta_correcta": "c",
  
  "razonamiento_completo": {
    "paso_1_identificacion_cuestion": "¿Cuál es la pregunta jurídica específica que debemos responder?",
    
    "paso_2_marco_normativo": [
      "Art. X de Ley Y (cita EXACTA)",
      "Art. Z de RD W (cita EXACTA)"
    ],
    
    "paso_3_analisis_hechos_relevantes": {
      "dato_clave_1": "Valor o situación",
      "dato_clave_2": "Valor o situación",
      "dato_clave_3": "Valor o situación"
    },
    
    "paso_4_subsuncion_juridica": {
      "norma_general": "Explicación de la regla general aplicable",
      "excepcion_si_aplica": "Explicación de excepciones relevantes",
      "aplicacion_al_caso": "Cómo se aplica la norma a los hechos concretos"
    },
    
    "paso_5_descarte_opciones_incorrectas": {
      "opcion_a": {
        "error": "Descripción del error jurídico",
        "por_que_seduce": "Razón psicológica por la que se marca"
      },
      "opcion_b": {
        "error": "Descripción del error jurídico",
        "por_que_seduce": "Razón psicológica por la que se marca"
      },
      "opcion_d": {
        "error": "Descripción del error jurídico",
        "por_que_seduce": "Razón psicológica por la que se marca"
      }
    },
    
    "paso_6_conclusion_fundamentada": "Explicación completa y clara de por qué la opción correcta es la c"
  },
  
  "trampa_pedagogica": {
    "tipo": "confusion_requisitos_alta_vs_no_alta",
    "explicacion": "Explicación detallada de por qué el opositor marca la opción incorrecta (mínimo 100 palabras)",
    "concepto_clave": "Concepto fundamental que debe dominar para evitar el error",
    "como_evitarla": "Técnica mnemotécnica o regla práctica para recordar"
  },
  
  "normativa_verificada": [
    {
      "norma": "Nombre completo oficial de la ley",
      "articulo": "Número exacto del artículo",
      "texto_literal": "Fragmento literal del artículo (mínimo 50 palabras)",
      "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-YYYY-XXXXX#aXXX",
      "fecha_verificacion": "12/01/2026",
      "status_url": "✅ Verificada"
    }
  ],
  
  "metadata_calidad": {
    "validado_por": "DeepSeek V3.1",
    "precision_tecnica": 0.98,
    "claridad_enunciado": 0.95,
    "utilidad_didactica": 0.97,
    "nivel_confianza_respuesta": 0.99
  }
}

IMPORTANTE:
1. Responde SOLO con el JSON válido, sin texto adicional
2. URLs del BOE deben ser reales y verificables
3. Citas textuales de artículos deben ser LITERALES
4. El razonamiento legal explicativo debe ser completo y educativo
5. La trampa debe ser realista (basada en errores reales de opositores)
"""

def test_deepseek_v3_case():
    """Test: generar 1 caso práctico con DeepSeek V3.1"""
    print("🚀 Testing DeepSeek V3.1 via Novita (HuggingFace)")
    print(f"📡 Modelo: {MODEL}")
    print(f"🔑 HF Token: {HF_TOKEN[:20] if HF_TOKEN else 'NOT FOUND'}...")
    print("="*80)
    
    if not HF_TOKEN:
        print("❌ ERROR: HF_TOKEN no encontrada en .env.backend")
        return None
    
    try:
        # Cliente HF
        client = InferenceClient(token=HF_TOKEN)
        
        print("\n📤 Enviando request a DeepSeek V3.1...")
        print(f"📝 Generando caso: SS_IPT_001 (Incapacidad Permanente Total)")
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT}
            ],
            max_tokens=4000,
            temperature=0.7,
            stream=False
        )
        
        result = response.choices[0].message.content
        usage = response.usage if hasattr(response, 'usage') else None
        
        print("\n" + "="*80)
        print("✅ CASO GENERADO:")
        print("="*80)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("\n" + "="*80)
        
        if usage:
            print("📊 USAGE:")
            print(f"   Input tokens:  {usage.prompt_tokens}")
            print(f"   Output tokens: {usage.completion_tokens}")
            print(f"   Total tokens:  {usage.total_tokens}")
            print("="*80)
        
        # Guardar resultado
        output_file = "/home/spas/OPOS_GEMINI_1/deepseek_v3_caso_prueba.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "model": MODEL,
                "provider": "Novita via HuggingFace",
                "timestamp": datetime.now().isoformat(),
                "caso_generado": result,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens if usage else "N/A",
                    "completion_tokens": usage.completion_tokens if usage else "N/A",
                    "total_tokens": usage.total_tokens if usage else "N/A"
                },
                "status": "success"
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Resultado guardado en: {output_file}")
        return result
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_deepseek_v3_case()
