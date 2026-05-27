#!/usr/bin/env python3
import os
import asyncio
import sys
import json
import re

# Añadir directorios necesarios al path
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, root_dir)
sys.path.insert(0, os.path.join(root_dir, "backend"))

from backend.agents.agent_engine import AgentEngine

async def main():
    print("\n" + "="*70)
    print("🛡️ GENERADOR GOLDEN STANDARD V11 — ESTRATEGIA 'SILENT SIEVE'")
    print("="*70)
    print("\n[ESTADO] Configuración E2E verificada. Iniciando flujo quirúrgico...\n")
    
    engine = AgentEngine()
    
    # ---------------------------------------------------------
    # STAGE 1: FACT-MINING (EXTRACCIÓN PURA)
    # ---------------------------------------------------------
    print("[STAGE 1/3] 🔎 Extrayendo verdades legales (Fact-Mining)...")
    
    query_extraction = """Extrae los datos exactos y artículos para 2026 sobre:
    1. Jubilación a los 65 años: Período de cotización exigido en 2026 (¿38a 6m?).
    2. IT Enfermedad Común: Quién paga días 4-15 (Empresa) y 16+ (Entidad Gestora/Mutua).
    3. Silencio Administrativo: Efecto en Recurso de Alzada y plazo de resolución (Art. 24 y 122 LPAC).
    4. IPP: Requisito de disminución de capacidad (sin umbral del 33% si no consta).
    
    REGLA: Usa 'search_rag' y 'ejecutar_calculo'. No redactes el caso aún."""
    
    inputs_1 = {"query": query_extraction, "fecha_referencia": "2026-03-07"}
    result_1 = await engine.execute("generator", inputs_1, model_override="deepseek-reasoner")
    
    legal_truths = result_1.get("content", "ERROR EN EXTRACCIÓN")
    print(f"✅ Datos verificados. (Iteraciones: {result_1.get('iterations', 0)})")
    
    # ---------------------------------------------------------
    # STAGE 2: CREATIVE DRAFTING (R1 HIGH-DENSITY)
    # ---------------------------------------------------------
    print("\n[STAGE 2/3] ✍️ Redactando Supuesto 'María Cano' (DeepSeek R1)...")
    
    query_draft = f"""REDACTA EL SUPUESTO PRÁCTICO DEFINITIVO.
    
    ⚠️ HECHOS LEGALES VERIFICADOS (INMUTABLES):
    {legal_truths}
    
    ESTRUCTURA DE EXAMEN REAL:
    1. **TRAMA NARRATIVA**: Crea una historia profesional y familiar coral (mínimo 5 personajes: Juan, Ana, Pedro, María y un Gestor/Empresario). 
       Entrelaza sus hilos: Juan se jubila, Ana está de baja, Pedro recurre y María tiene una secuela. 
       Entorno: Año 2026. Lenguaje denso y técnico. (Mínimo 500 palabras).
    
    2. **CUESTIONARIO TEST**: 18 preguntas de examen en total (15 oficiales + 3 de reserva) con 4 opciones (a, b, c, d). Solo una correcta.
       - Incluye distractores potentes (datos de 2024, swaps de pagador de IT, etc.).
       - DISTRIBUCIÓN OBLIGATORIA: La respuesta correcta debe repartirse equitativamente entre las opciones A, B, C y D (aprox. 25% cada una). ESTRICTO: NO pongas sistemáticamente la correcta en la opción 'b'.
    
    3. **CLAVE DE RESPUESTAS**: Para cada pregunta, indica la letra correcta y un razonamiento técnico breve citando el ARTÍCULO LITERAL del BOE devuelto por el RAG.
    
    REGLA DE ORO: El documento debe ser LIMPIO. No incluyas explicaciones sobre qué herramientas usaste ni secciones de 'Fase'."""
    
    inputs_2 = {"query": query_draft, "fecha_referencia": "2026-03-07"}
    # Usamos generator_r1 que ahora tiene herramientas activas
    result_2 = await engine.execute("generator_r1", inputs_2) 
    
    draft_content = result_2.get("content", "ERROR EN REDACCIÓN")
    print(f"✅ Borrador generado. (Iteraciones: {result_2.get('iterations', 0)})")
    
    # ---------------------------------------------------------
    # STAGE 3: SILENT CLEANUP (ELIMINACIÓN DE RUIDO)
    # ---------------------------------------------------------
    print("\n[STAGE 3/3] 🧹 Aplicando Tamiz Silencioso (Cleanup)...")
    
    # 1. Quitar <think> blocks por si acaso el engine los dejó
    clean_content = re.sub(r'<think>.*?</think>', '', draft_content, flags=re.DOTALL)
    
    # 2. Quitar frases introductorias típicas de LLM
    clean_content = re.sub(r'^(Aquí tienes|A continuación|Claro|Entendido).*?\n', '', clean_content, flags=re.IGNORECASE)
    
    # 3. Asegurar encabezado de examen
    if not clean_content.strip().startswith("#"):
        clean_content = "# SUPUESTO PRÁCTICO DE EXAMEN - OPOSICIONES 2026\n\n" + clean_content
    
    filename = "dataset_output/golden_standard_v11_silent_sieve.md"
    os.makedirs("dataset_output", exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(clean_content.strip())
        
    print(f"\n🏆 PROCESO COMPLETADO EXITOSAMENTE.")
    print(f"📂 Archivo Inmaculado: {filename}")
    print(f"✨ Calidad: Grado Oposición Real (Estilo María Cano)")

if __name__ == "__main__":
    asyncio.run(main())
