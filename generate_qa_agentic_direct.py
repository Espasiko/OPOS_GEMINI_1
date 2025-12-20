#!/usr/bin/env python3
"""
Agente Completo: Groq + RAG Directo (sin MCP)
Genera 10 Q&A de máxima calidad con variedad de tipos
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
env_path = Path("backend/.env.backend")
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Cargado .env desde: {env_path}")
else:
    print(f"⚠️  No se encontró {env_path}, usando variables de sistema")

# Configuración
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# INSTRUCCIONES COMPLETAS DEL AGENTE
SYSTEM_PROMPT = """
Eres un experto en oposiciones de la Administración General del Estado (AGE) y Seguridad Social española.

TU MISIÓN:
Generar preguntas de MÁXIMA CALIDAD (99%+) para oposiciones.

REGLAS ESTRICTAS:
1. Basa TODO en la legislación oficial del contexto RAG
2. SIEMPRE cita el artículo de ley específico
3. Las 4 opciones deben ser plausibles pero solo 1 correcta
4. Incluye explicación detallada con razonamiento legal
5. NO inventes datos, USA solo lo del contexto
6. Verifica que la respuesta sea actual y vigente

CALIDAD PREMIUM:
- Referencias legales exactas (art. X Ley Y)
- Explicación con razonamiento paso a paso
- Opciones que reflejen confusiones comunes
- Lenguaje técnico pero claro
"""

# EJEMPLO DE CALIDAD PREMIUM
EJEMPLO_PREMIUM = {
    "id": "PREMIUM-001",
    "pregunta": "¿Cuál es el plazo máximo de duración de la incapacidad temporal según el art. 169 LGSS?",
    "opciones": [
        "A) 365 días prorrogables 180 más",
        "B) 545 días sin prórroga",
        "C) 365 días prorrogables 180 más, evaluando a los 365",
        "D) 12 meses renovables"
    ],
    "respuesta_correcta": "A",
    "respuesta": "Según art. 169 LGSS, la IT tiene duración máxima de 365 días prorrogables por otros 180 cuando se presuma curación en ese plazo.",
    "explicacion": "El art. 169 LGSS establece que la IT dura hasta la curación o alta médica, con límite de 365 días. Puede prorrogarse 180 días más si se estima curación. Tras 545 días, pasa a evaluación de IP.",
    "referencias": ["art. 169 LGSS", "art. 174 LGSS"],
    "tema": "seguridad_social",
    "subtema": "incapacidad_temporal",
    "dificultad": "alta",
    "tipo": "test"
}

def consultar_rag_directo(query: str, limit: int = 5) -> dict:
    """Consultar RAG directamente (endpoint correcto)"""
    try:
        response = requests.post(
            f"{FASTAPI_URL}/api/rag/search",
            json={"query": query, "top_k": limit, "min_score": 0.3},  # Lowered to get more results
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            # Convertir formato a results
            return {
                "results": [
                    {
                        "title": doc.get("metadata", {}).get("title", "Documento"),
                        "content": doc.get("content", ""),
                        "score": doc.get("score", 0)
                    }
                    for doc in data.get("documents", [])
                ]
            }
        else:
            print(f"      ❌ Error RAG: {response.status_code}")
            return {"results": []}
    except Exception as e:
        print(f"      ❌ Error consultando RAG: {e}")
        return {"results": []}

def generar_con_groq(instruccion: str, contexto_rag: str, tipo: str) -> dict:
    """Generar Q&A con Groq (llama-3.3-70b)"""
    try:
        import groq
        client = groq.Groq(api_key=GROQ_API_KEY)
        
        # Formato específico por tipo
        formato_json = """
{
  "pregunta": "Texto de la pregunta citando artículo",
  "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "respuesta_correcta": "A",
  "respuesta": "Respuesta breve con referencia legal",
  "explicacion": "Explicación detallada del razonamiento",
  "referencias": ["art. X Ley Y"],
  "tema": "seguridad_social|procedimiento_administrativo|...",
  "subtema": "...",
  "dificultad": "media"
}
"""
        
        full_prompt = f"""
{SYSTEM_PROMPT}

EJEMPLO DE CALIDAD:
{json.dumps(EJEMPLO_PREMIUM, indent=2, ensure_ascii=False)}

CONTEXTO LEGAL DEL RAG:
{contexto_rag}

INSTRUCCIÓN:
{instruccion}

FORMATO OBLIGATORIO:
{formato_json}

Responde ÚNICAMENTE con el JSON de la pregunta, sin texto adicional.
"""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres un experto en legislación española. Generas preguntas de oposiciones de máxima calidad basándote SOLO en el contexto legal proporcionado."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        
        # Extraer JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        qa = json.loads(content.strip())
        qa["tipo"] = tipo
        qa["generated_at"] = datetime.now().isoformat()
        qa["created_by"] = "groq_llama_3.3_70b_agentic"
        qa["verified"] = False  # Pendiente revisión humana
        
        return qa
        
    except Exception as e:
        print(f"      ❌ Error generando con Groq: {e}")
        import traceback
        traceback.print_exc()
        return None

def generar_10_qa():
    """Generar 10 Q&A de calidad con VARIEDAD DE TIPOS"""
    print("\n" + "="*70)
    print("GENERACIÓN DE 10 Q&A CON VARIEDAD DE TIPOS")
    print("Groq llama-3.3-70b + RAG Directo (v2)")
    print("="*70)
    
    # Verificar tokens
    if not GROQ_API_KEY:
        print("\n❌ GROQ_API_KEY no encontrada")
        print("   Añade GROQ_API_KEY=... en backend/.env.backend")
        return
    
    print(f"\n✅ Groq API Key: {GROQ_API_KEY[:15]}...")
    
    # VARIEDAD DE TIPOS Y TEMAS (10 preguntas)
    tareas = [
        # TEST (4 preguntas)
        {
            "tipo": "test",
            "tema": "incapacidad temporal duración",
            "dificultad": "alta",
            "instruccion": "Genera una pregunta tipo test con 4 opciones (A, B, C, D). Solo una correcta. Sobre duración y plazos de IT."
        },
        {
            "tipo": "test",
            "tema": "jubilación ordinaria requisitos",
            "dificultad": "media",
            "instruccion": "Genera una pregunta tipo test sobre requisitos de jubilación ordinaria."
        },
        {
            "tipo": "test",
            "tema": "prestación desempleo cuantía",
            "dificultad": "media",
            "instruccion": "Genera una pregunta tipo test sobre cuantía del desempleo contributivo."
        },
        {
            "tipo": "test",
            "tema": "recurso de alzada plazo",
            "dificultad": "baja",
            "instruccion": "Genera una pregunta tipo test sobre el plazo del recurso de alzada."
        },
        
        # COMPARACIÓN (2 preguntas)
        {
            "tipo": "comparacion",
            "tema": "incapacidad permanente parcial total",
            "dificultad": "alta",
            "instruccion": "Genera una pregunta que compare IP parcial vs IP total, explicando diferencias clave en porcentajes y efectos."
        },
        {
            "tipo": "comparacion",
            "tema": "moción de censura cuestión de confianza",
            "dificultad": "media",
            "instruccion": "Genera una pregunta comparando moción de censura y cuestión de confianza según la CE."
        },
        
        # PROCEDIMIENTO (2 preguntas)
        {
            "tipo": "procedimiento",
            "tema": "solicitar pensión jubilación",
            "dificultad": "media",
            "instruccion": "Genera una pregunta sobre los pasos del procedimiento para solicitar jubilación, en orden."
        },
        {
            "tipo": "procedimiento",
            "tema": "tramitación recurso de alzada",
            "dificultad": "alta",
            "instruccion": "Genera una pregunta sobre las fases de tramitación del recurso de alzada."
        },
        
        # RAZONAMIENTO (1 pregunta)
        {
            "tipo": "razonamiento",
            "tema": "incapacidad temporal supera 365 días",
            "dificultad": "alta",
            "instruccion": "Genera un caso práctico: trabajador en IT que llega a 365 días. ¿Qué pasa después? Razonamiento paso a paso."
        },
        
        # RELACIÓN (1 pregunta)
        {
            "tipo": "relacion",
            "tema": "LGSS Constitución derechos sociales",
            "dificultad": "media",
            "instruccion": "Genera una pregunta sobre cómo se relacionan LGSS y CE en materia de derechos sociales."
        }
    ]
    
    qa_generadas = []
    
    for i, tarea in enumerate(tareas, 1):
        tipo = tarea["tipo"]
        tema = tarea["tema"]
        dificultad = tarea["dificultad"]
        instruccion = tarea["instruccion"]
        
        print(f"\n{'─'*70}")
        print(f"[{i}/10] Tipo: {tipo.upper()}")
        print(f"       Tema: {tema}")
        print('─'*70)
        
        # 1. Consultar RAG
        print(f"   1️⃣ Consultando RAG...")
        rag_result = consultar_rag_directo(tema, limit=3)
        results = rag_result.get("results", [])
        
        if not results:
            print(f"      ⚠️  Sin resultados RAG, saltando...")
            continue
        
        print(f"      ✅ {len(results)} resultados encontrados")
        
        # 2. Preparar contexto
        contexto = "\n\n".join([
            f"[{r.get('title', r.get('metadata', {}).get('title', 'Documento legal'))}]\n{r.get('content', r.get('text', ''))[:600]}"
            for r in results
        ])
        
        # 3. Generar con Groq
        print(f"   2️⃣ Generando con Groq...")
        qa = generar_con_groq(instruccion, contexto, tipo)
        
        if qa:
            qa["id"] = f"AGENTIC-{i:03d}"
            qa["dificultad"] = dificultad
            qa_generadas.append(qa)
            print(f"      ✅ Generada: {qa['pregunta'][:55]}...")
        else:
            print(f"      ❌ Error generando Q&A")
    
    # Guardar resultados
    if qa_generadas:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"qa_agentic_groq_{timestamp}.jsonl"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for qa in qa_generadas:
                f.write(json.dumps(qa, ensure_ascii=False) + '\n')
        
        print("\n" + "="*70)
        print(f"✅ COMPLETADO: {len(qa_generadas)}/10 Q&A generadas")
        print("="*70)
        
        # Estadísticas
        from collections import Counter
        tipos_count = Counter(qa["tipo"] for qa in qa_generadas)
        print("\n📊 TIPOS GENERADOS:")
        for tipo, count in sorted(tipos_count.items()):
            print(f"   {tipo}: {count}")
        
        print(f"\n📁 Guardado en: {output_file}")
        
        # Mostrar muestra
        if qa_generadas:
            print("\n" + "="*70)
            print("📋 MUESTRA (primera pregunta):")
            print("="*70)
            print(json.dumps(qa_generadas[0], indent=2, ensure_ascii=False))
        
        return output_file
    else:
        print("\n❌ No se generaron Q&A")
        print("   Verifica que FastAPI esté corriendo:")
        print("   cd backend && uvicorn main:app --reload")
        return None

if __name__ == "__main__":
    generar_10_qa()
