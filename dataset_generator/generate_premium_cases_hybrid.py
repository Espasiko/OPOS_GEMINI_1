#!/usr/bin/env python3
"""
GENERADOR PREMIUM DEEPSEEK "ALL-IN-ONE" (R1 + PROMPT CACHING)
-------------------------------------------------------------
Estrategia "Magister":
1. RAG EXHAUSTIVO: Recupera el contexto legal real.
2. ESCENARIO (DeepSeek R1): Genera un caso de dificultad extrema.
3. PREGUNTAS (DeepSeek R1): Genera 18 preguntas (Batch 3x6) para formato oficial.

Optimizaciones:
- Batching (3 lotes de 6 preguntas) para manejar el massive-reasoning y 18 preguntas total.
- Manejo correcto de API DeepSeek R1 (reasoning_content vs content).
- Modo JSON Nativo para preguntas.
- Timeout RAG extendido (120s).
"""

import os
import json
import time
import requests
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar entorno
env_path = Path("backend/.env.backend")
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
BACKEND_URL = "http://127.0.0.1:8000"

# -----------------------------------------------------------------------------
# 1. RAG EXHAUSTIVO (Consulta DB Local)
# -----------------------------------------------------------------------------
def buscar_rag_exhaustivo(topic: str, limit: int = 10, dry_run: bool = False) -> str:
    """Recupera contexto legal amplio para 'alimentar' al Magistrado."""
    logger.info(f"📚 [Fase 1] Buscando jurisprudencia y leyes sobre: {topic}")
    
    # Check simple connectivity first
    if not dry_run:
        try:
             # Timeout generoso de 120s para evitar fallos de lectura en cargas frías
            response = requests.post(
                f"{BACKEND_URL}/api/rag/search",
                json={"query": topic, "top_k": limit, "min_score": 0.3}, # Min score ajustado
                timeout=120 
            )
            if response.status_code == 200:
                results = response.json().get("documents", [])
                if not results:
                     logger.error("⚠️ RAG devolvió 0 resultados. ¡ABORTANDO POR SEGURIDAD!")
                     raise ValueError("RAG devolvió 0 resultados para la query.")
                     
                context = "\n\n".join([
                    f"DOCUMENTO {i+1} ({r.get('metadata', {}).get('title', 'Sin titulo')}):\n{r.get('content', '')[:1200]}"
                    for i, r in enumerate(results)
                ])
                logger.info(f"✅ Contexto recuperado: {len(results)} documentos.")
                return context
            else:
                logger.error(f"⚠️ Error RAG: {response.status_code} - ABORTANDO.")
                raise ConnectionError(f"RAG Endpoint returned {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ CRITICAL RAG FAILURE: {e}")
            raise e  # Re-raise to stop execution immediately
    else:
        logger.info("🧪 [DRY RUN] Simulando llamada RAG (Exitosa)")
        return "CONTEXTO SIMULADO: LEY GENERAL DE LA SEGURIDAD SOCIAL..."

# -----------------------------------------------------------------------------
# 2. GENERACIÓN DE ESTRUCTURA (Prompt Caching Friendly)
# -----------------------------------------------------------------------------
SYSTEM_PROMPT_MAGISTRADO = """Eres el MAGISTRADO SUPREMO del Tribunal de Oposiciones de la Seguridad Social.
Tu intelecto es puramente lógico, frío y jurídico. Tu misión es filtrar a los candidatos mediante la "PRUEBA DE FUEGO".

DEFINICIÓN DE "DIFICULTAD EXTREMA":
1. Cruce de Normativas: El caso debe involucrar al menos 3 normas (ej. LGSS, ET, RD de desarrollo).
2. Trampas Temporales: Fechas de solicitud, hechos causantes y plazos de prescripción milimétricos.
3. Silencios: Situaciones donde la administración no responde y se aplica silencio (positivo/negativo).
4. Procedimiento: Errores en la vía administrativa (alzada, reposición, plazos).

INSTRUCCIONES PARA CHAIN OF THOUGHT (CoT):
Antes de escribir el caso o las preguntas, debes RAZONAR internamente:
- ¿Qué artículo exacto aplica?
- ¿Dónde está la excepción?
- ¿Cómo puedo inducir al error al opositor promedio?

FORMATO EXAMEN OFICIAL (Basado en Noviembre 2024):
- 1 Supuesto Práctico (puede tener varios sub-casos o empleados, 600-800 palabras).
- 18 Preguntas TOTALES:
  * 15 Preguntas Ordinarias (Numeradas 1-15).
  * 3 Preguntas de Reserva (Numeradas 1-3, internamente 16-18).
- 4 Opciones (A, B, C, D).
- Justificación jurídica impecable basada en el contexto aportado.
"""

def generate_full_case_deepseek(topic: str, context: str, dry_run: bool = False) -> dict:
    """Genera Escenario + 18 Preguntas (Batching) para evitar cortes."""
    
    # FASE A: ESCENARIO
    logger.info(f"⚖️  [Fase 2] El Magistrado DeepSeek está redactando el ESCENARIO...")
    
    prompt_escenario = f"""
CONTEXTO LEGAL RECUPERADO (ÚSALO OBLIGATORIAMENTE):
{context}

TEMA DEL CASO: "{topic}"

TAREA A (ESCENARIO):
Escribe un CASO PRÁCTICO de 600-800 palabras.
- Debe ser una narrativa densa (estilo "Señor de La Lage, S.L.") que puede involucrar a la empresa y varios trabajadores con situaciones distintas (altas, bajas, jubilación, deudas, embargos).
- Introduce al menos 3 trampas jurídicas sutiles.
- NO escribas las preguntas todavía. Solo el relato fáctico.
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_MAGISTRADO},
        {"role": "user", "content": prompt_escenario}
    ]

    # Call for Scenario
    response_a = call_deepseek_reasoner(messages, json_mode=False, dry_run=dry_run, phase="ESCENARIO")
    if not response_a: return None
    
    scenario_text = response_a["content"]
    scenario_reasoning = response_a["reasoning"]
    
    logger.info("✅ Escenario redactado. Procediendo a las 18 preguntas (POR LOTES)...")
    
    # Add scenario to history
    messages.append({"role": "assistant", "content": scenario_text})
    
    all_questions = []
    all_q_reasoning = []
    
    # FASE B: PREGUNTAS (Batching 3 x 6 = 18)
    # Lote 1: 1-6
    # Lote 2: 7-12
    # Lote 3: 13-18 (Donde 16, 17, 18 son Reserva)
    BATCHES = [(1, 6), (7, 12), (13, 18)]
    
    for start, end in BATCHES:
        logger.info(f"🧠 [Fase 3] Generando Preguntas {start}-{end}...")
        
        prompt_batch = f"""
TAREA B (PREGUNTAS {start}-{end}):
Basándote en el escenario anterior, genera las PREGUNTAS del lote correspondiente.

REGLAS DE ESTE LOTE ({start}-{end}):
- Genera EXACTAMENTE 6 preguntas.
- Sigue la numeración continua: {start}, {start+1}, ..., {end}.
- CRÍTICO: Si el número es > 15, es una PREGUNTA DE RESERVA (Tipo "Reserva").
  * Pregunta 16 equivale a Reserva 1.
  * Pregunta 17 equivale a Reserva 2.
  * Pregunta 18 equivale a Reserva 3.
- Estilo Examen Oficial: Enunciados directos, fechas concretas, cálculo de bases o plazos.

ESTRUCTURA JSON BATCH:
{{
  "preguntas": [
    {{
      "numero": {start},      // Del 1 al 18
      "enunciado": "¿...",
      "opciones": ["A)", "B)", "C)", "D)"],
      "respuesta_correcta": "A",
      "tipo": "Ordinaria" (si num <= 15) o "Reserva" (si num > 15),
      "justificacion_legal": "Art...",
      "trampa_logica": "..."
    }}
  ]
}}
RESPONDE SOLO CON JSON. NO INCLUYAS MARKDOWN FUERA DEL JSON.
"""
        messages.append({"role": "user", "content": prompt_batch})
        
        response_b = call_deepseek_reasoner(messages, json_mode=True, dry_run=dry_run, phase=f"PREGUNTAS_{start}_{end}")
        
        if not response_b:
            logger.error(f"⚠️ Falló el lote {start}-{end}. Saltando...")
            continue
            
        json_content = response_b["content"]
        q_reasoning = response_b["reasoning"]
        all_q_reasoning.append(f"--- LOTE {start}-{end} ---\n{q_reasoning}")
        
        try:
            clean_json = json_content.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            batch_qs = data.get("preguntas", [])
            all_questions.extend(batch_qs)
            logger.info(f"✅ Lote {start}-{end} recibido ({len(batch_qs)} preguntas).")
            
            # Append assistant response 
            messages.append({"role": "assistant", "content": json_content})
            
        except Exception as e:
            logger.error(f"❌ Error JSON Lote {start}-{end}: {e}")
            with open(f"debug_failed_batch_{start}.txt", "w") as f: f.write(json_content)

    if not all_questions:
        return None

    # Ensamble Final
    final_data = {
        "titulo": f"Supuesto Práctico Oficial: {topic}",
        "dificultad": "EXTREMA (Formato Oficial 2024/25)",
        "escenario": scenario_text,
        "preguntas": all_questions,
        "razonamiento_escenario": scenario_reasoning,
        "razonamiento_preguntas": "\n".join(all_q_reasoning),
        "metadata": {
            "model": "deepseek-reasoner",
            "generated_at": datetime.now().isoformat(),
            "batches": len(BATCHES),
            "ref_format": "15 Ord + 3 Res"
        }
    }
             
    return final_data

def call_deepseek_reasoner(messages, json_mode=False, dry_run=False, phase="DEFAULT"):
    """Llamada a la API de DeepSeek optimizada."""
    if dry_run:
        logger.info(f"🧪 [DRY RUN] Saltando llamada API DeepSeek ({phase})...")
        if phase == "ESCENARIO":
            return {"content": "ESCENARIO SIMULADO...", "reasoning": "RAZONAMIENTO SIMULADO..."}
        if "PREGUNTAS" in phase:
            return {"content": json.dumps({"preguntas": [{"numero": 1, "enunciado": "Simulada"}]}), "reasoning": "RAZ..."}
        return {"content": "", "reasoning": ""}

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-reasoner",
        "messages": messages,
        "temperature": 0.6,
        "max_tokens": 8000
    }
    
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=400)
        r.raise_for_status()
        resp_json = r.json()
        choice = resp_json["choices"][0]["message"]
        
        content = choice.get("content", "")
        reasoning = choice.get("reasoning_content", "")
        
        logger.info(f"🤖 [Respuesta API] Content len: {len(content)}, Reasoning len: {len(reasoning)}")
        
        return {
            "content": content,
            "reasoning": reasoning
        }
    except Exception as e:
        logger.error(f"❌ Error API DeepSeek: {e}")
        if 'r' in locals() and hasattr(r, 'text'):
            logger.error(f"Detalle: {r.text}")
        return None

# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generador de Casos Premium (Dry Run available)')
    parser.add_argument('--dry-run', action='store_true', help='Ejecutar sin gastar API credits')
    args = parser.parse_args()

    if not args.dry_run and not DEEPSEEK_API_KEY:
        logger.error("❌ FALTA DEEPSEEK_API_KEY en .env.backend")
        exit(1)

    TOPICS = [
        "Ingreso Mínimo Vital 2025: Computo de rentas, unidad de convivencia y procedimiento administrativo (Inspirado en examen oficial 2024)"
    ]
    
    OUTPUT_DIR = Path("/home/spas/OPOS_GEMINI_1/dataset_generator/premium_content/deepseek_pilot")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"🚀 INICIANDO GENERADOR. MODO DRY-RUN: {args.dry_run}")

    for topic in TOPICS:
        logger.info(f"\n🚀 PROCESANDO TEMA: {topic}")
        
        try:
            contexto = buscar_rag_exhaustivo(topic, dry_run=False) # RAG R E A L
            
            caso_completo = generate_full_case_deepseek(topic, contexto, dry_run=args.dry_run)
            
            if caso_completo and not args.dry_run:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"deepseek_r1_case_{timestamp}.json"
                save_path = OUTPUT_DIR / filename
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(caso_completo, f, indent=2, ensure_ascii=False)
                logger.info(f"💾 Guardado: {save_path}")
            elif args.dry_run:
                logger.info("✅ [DRY RUN COMPLETADO] Flujo validado correctamente.")

        except Exception as e:
            logger.error(f"❌ FALLO EN PROCESO: {e}")
            exit(1)
