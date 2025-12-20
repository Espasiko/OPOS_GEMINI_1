#!/usr/bin/env python3
"""
Generador de 10 Q&A usando Mistral Agent Studio
Agent ID: ag_019ad601946d7323a81c544229de40a1
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from mistralai import Mistral

# Cargar .env
env_path = Path("backend/.env.backend")
if env_path.exists():
    load_dotenv(env_path)

# Configuración
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF")
MISTRAL_AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

# System prompt
SYSTEM_PROMPT = """Eres un experto en oposiciones de la Administración General del Estado (AGE) y Seguridad Social española.

GENERA preguntas de MÁXIMA CALIDAD basándote SOLO en el contexto legal proporcionado.

FORMATO OBLIGATORIO - Responde ÚNICAMENTE con JSON:
{
  "pregunta": "...",
  "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "respuesta_correcta": "A",
  "respuesta": "...",
  "explicacion": "...",
  "referencias": ["art. X Ley Y"],
  "tema": "...",
  "subtema": "...",
  "dificultad": "media"
}"""

def consultar_rag(tema: str, top_k: int = 3) -> str:
    """Consulta el RAG para obtener contexto legal"""
    try:
        response = requests.post(
            f"{FASTAPI_URL}/api/rag/search",
            json={"query": tema, "top_k": top_k, "min_score": 0.3},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            docs = data.get("documents", [])
            if docs:
                context = "\n\n".join([
                    f"[Fuente {i+1}] {doc.get('content', '')[:500]}"
                    for i, doc in enumerate(docs)
                ])
                return context
        return ""
    except Exception as e:
        print(f"      ❌ Error consultando RAG: {e}")
        return ""

def generar_con_mistral_agent(instruccion: str, contexto_rag: str, tipo: str) -> dict:
    """Generar Q&A con Mistral API (mistral-small)"""
    try:
        client = Mistral(api_key=MISTRAL_API_KEY)
        
        prompt = f"""{SYSTEM_PROMPT}

CONTEXTO LEGAL:
{contexto_rag[:2000]}

INSTRUCCIÓN:
{instruccion}

Responde SOLO con el JSON, sin texto adicional."""
        
        print(f"      📤 Enviando prompt a Mistral API...")
        
        # Usar chat.complete con mistral-small (NO agents.complete para evitar tool calls)
        response = client.chat.complete(
            model="mistral-small-latest",  # Modelo directo sin agente
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=1500
        )
        
        print(f"      📥 Respuesta recibida")
        
        # Extraer texto de la respuesta
        content = response.choices[0].message.content
        generated_text = str(content)
        
        print(f"      📝 Texto generado (primeros 200 chars): {generated_text[:200]}")
        print(f"      📝 Longitud total: {len(generated_text)}")
        
        if not generated_text.strip():
            print(f"      ⚠️  Texto vacío!")
            return None
        
        # Extraer JSON
        if "```json" in generated_text:
            generated_text = generated_text.split("```json")[1].split("```")[0]
        elif "```" in generated_text:
            generated_text = generated_text.split("```")[1].split("```")[0]
        
        # Buscar JSON en el texto
        start = generated_text.find('{')
        end = generated_text.rfind('}') + 1
        if start >= 0 and end > start:
            generated_text = generated_text[start:end]
        
        print(f"      🔧 JSON extraído: {generated_text[:200]}...")
        
        qa = json.loads(generated_text.strip())
        qa["tipo"] = tipo
        qa["generated_at"] = datetime.now().isoformat()
        qa["created_by"] = "mistral_small_api"
        qa["verified"] = False
        
        return qa
        
    except json.JSONDecodeError as e:
        print(f"      ❌ Error parseando JSON: {e}")
        print(f"      📄 Texto que intentó parsear: {generated_text[:500]}")
        return None
    except Exception as e:
        print(f"      ❌ Error generando con Mistral API: {e}")
        import traceback
        traceback.print_exc()
        return None

def generar_10_qa():
    """Generar 10 Q&A con Mistral Agent"""
    print("\n" + "="*70)
    print("GENERACIÓN DE 10 Q&A CON VARIEDAD DE TIPOS")
    print("Mistral Agent Studio + RAG")
    print("="*70)
    print(f"\nAgent ID: {MISTRAL_AGENT_ID}")
    print(f"API Key: {MISTRAL_API_KEY[:15]}...")
    
    # Tareas
    tareas = [
        {"tipo": "test", "tema": "incapacidad temporal duración", "dificultad": "alta",
         "instruccion": "Genera una pregunta tipo test con 4 opciones (A, B, C, D). Solo una correcta. Sobre duración y plazos de IT."},
        {"tipo": "test", "tema": "jubilación ordinaria requisitos", "dificultad": "media",
         "instruccion": "Genera una pregunta tipo test sobre requisitos de jubilación ordinaria."},
        {"tipo": "test", "tema": "prestación desempleo cuantía", "dificultad": "media",
         "instruccion": "Genera una pregunta tipo test sobre cuantía del desempleo contributivo."},
        {"tipo": "test", "tema": "recurso de alzada plazo", "dificultad": "baja",
         "instruccion": "Genera una pregunta tipo test sobre el plazo del recurso de alzada."},
        {"tipo": "comparacion", "tema": "incapacidad permanente parcial total", "dificultad": "alta",
         "instruccion": "Genera una pregunta que compare IP parcial vs IP total, explicando diferencias clave."},
        {"tipo": "comparacion", "tema": "moción de censura cuestión de confianza", "dificultad": "media",
         "instruccion": "Genera una pregunta comparando moción de censura y cuestión de confianza según la CE."},
        {"tipo": "procedimiento", "tema": "solicitar pensión jubilación", "dificultad": "media",
         "instruccion": "Genera una pregunta sobre los pasos del procedimiento para solicitar jubilación."},
        {"tipo": "procedimiento", "tema": "tramitación recurso de alzada", "dificultad": "alta",
         "instruccion": "Genera una pregunta sobre las fases de tramitación del recurso de alzada."},
        {"tipo": "razonamiento", "tema": "incapacidad temporal supera 365 días", "dificultad": "alta",
         "instruccion": "Genera un caso práctico: trabajador en IT que llega a 365 días. ¿Qué pasa después?"},
        {"tipo": "relacion", "tema": "LGSS Constitución derechos sociales", "dificultad": "media",
         "instruccion": "Genera una pregunta sobre cómo se relacionan LGSS y CE en materia de derechos sociales."}
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
        contexto = consultar_rag(tema, top_k=3)
        
        if not contexto:
            print(f"      ⚠️  Sin resultados RAG, saltando...")
            continue
        
        print(f"      ✅ Contexto obtenido")
        
        # 2. Generar con Mistral Agent
        print(f"   2️⃣ Generando con Mistral Agent...")
        qa = generar_con_mistral_agent(instruccion, contexto, tipo)
        
        if qa:
            qa["id"] = f"MISTRAL-AGENT-{i:03d}"
            qa["dificultad"] = dificultad
            qa_generadas.append(qa)
            print(f"      ✅ Generada: {qa['pregunta'][:55]}...")
        else:
            print(f"      ❌ Error generando Q&A")
    
    # Guardar resultados
    if qa_generadas:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"qa_mistral_agent_{timestamp}.jsonl"
        
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
        return None

if __name__ == "__main__":
    generar_10_qa()
