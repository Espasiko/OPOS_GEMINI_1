#!/usr/bin/env python3
"""
Agente Mistral 8B con Instrucciones Completas
Genera 10 Q&A de máxima calidad usando MCP + RAG
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv("backend/.env.backend")

# Configuración
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# INSTRUCCIONES DEL AGENTE
AGENT_INSTRUCTIONS = """
Eres un experto en oposiciones de la Administración General del Estado (AGE) y Seguridad Social española.

TU MISIÓN:
Generar preguntas tipo test de MÁXIMA CALIDAD (99%+) para oposiciones.

REGLAS ESTRICTAS:
1. Basa TODO en la legislación oficial que consultas del RAG
2. SIEMPRE cita el artículo de ley específico
3. Las 4 opciones deben ser plausibles pero solo 1 correcta
4. Incluye explicación detallada con razonamiento legal
5. NO inventes datos, USA solo lo que encuentres en el RAG
6. Verifica que la respuesta sea actual y vigente

FORMATO OBLIGATORIO:
{
  "id": "AGENTIC-001",
  "pregunta": "Texto de la pregunta citando artículo",
  "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "respuesta_correcta": "A",
  "respuesta": "Respuesta breve con referencia legal",
  "explicacion": "Explicación detallada del razonamiento",
  "referencias": ["art. X Ley Y", "art. Z LGSS"],
  "tema": "seguridad_social|procedimiento_administrativo|...",
  "subtema": "incapacidad_temporal|...",
  "dificultad": "media",
  "tipo": "test",
  "verified": true,
  "created_by": "mistral_8b_agentic",
  "generated_at": "2024-12-19T..."
}

PROCESO:
1. Consulta RAG con tema específico
2. Lee contexto legal devuelto
3. Genera pregunta basada SOLO en ese contexto
4. Verifica que la respuesta esté en el contexto
5. Añade referencias exactas
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
    "tipo": "test",
    "verified": True,
    "created_by": "gemini_cot"
}

def consultar_rag(query: str, limit: int = 5) -> dict:
    """Consultar RAG vía MCP"""
    try:
        response = requests.post(
            f"{FASTAPI_URL}/mcp/search_rag",
            json={"query": query, "limit": limit, "score_threshold": 0.7},
            timeout=15
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error RAG: {response.status_code}")
            return {"results": []}
    except Exception as e:
        print(f"❌ Error consultando RAG: {e}")
        return {"results": []}

def generar_con_groq(prompt: str, contexto_rag: str) -> dict:
    """Generar Q&A con Groq (llama-3.3-70b)"""
    try:
        import groq
        client = groq.Groq(api_key=GROQ_API_KEY)
        
        full_prompt = f"""
{AGENT_INSTRUCTIONS}

EJEMPLO DE CALIDAD:
{json.dumps(EJEMPLO_PREMIUM, indent=2, ensure_ascii=False)}

CONTEXTO LEGAL DEL RAG:
{contexto_rag}

INSTRUCCIÓN:
Genera 1 pregunta tipo test sobre: {prompt}

Usa SOLO el contexto legal proporcionado.
Responde ÚNICAMENTE con el JSON de la pregunta, sin texto adicional.
"""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres un experto en legislación española. Generas preguntas de oposiciones de máxima calidad."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        
        # Extraer JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        qa = json.loads(content.strip())
        qa["generated_at"] = datetime.now().isoformat()
        qa["created_by"] = "groq_llama_3.3_70b"
        
        return qa
        
    except Exception as e:
        print(f"❌ Error generando con Groq: {e}")
        return None

def generar_10_qa():
    """Generar 10 Q&A de calidad con VARIEDAD DE TIPOS"""
    print("\n" + "="*60)
    print("GENERACIÓN DE 10 Q&A CON VARIEDAD DE TIPOS")
    print("="*60)
    
    # Verificar tokens
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY no encontrada en .env")
        return
    
    print(f"✅ Groq API Key: {GROQ_API_KEY[:10]}...")
    
    # VARIEDAD DE TIPOS Y TEMAS
    tareas = [
        # TEST (4)
        {"tipo": "test", "tema": "incapacidad temporal duración", "dificultad": "alta"},
        {"tipo": "test", "tema": "jubilación ordinaria requisitos", "dificultad": "media"},
        {"tipo": "test", "tema": "prestación desempleo cuantía", "dificultad": "media"},
        {"tipo": "test", "tema": "recurso de alzada plazo", "dificultad": "baja"},
        
        # COMPARACIÓN (2)
        {"tipo": "comparacion", "tema": "diferencia entre incapacidad permanente parcial y total", "dificultad": "alta"},
        {"tipo": "comparacion", "tema": "moción de censura vs cuestión de confianza", "dificultad": "media"},
        
        # PROCEDIMIENTO (2)
        {"tipo": "procedimiento", "tema": "pasos para solicitar pensión de jubilación", "dificultad": "media"},
        {"tipo": "procedimiento", "tema": "tramitación recurso de alzada", "dificultad": "alta"},
        
        # RAZONAMIENTO (1)
        {"tipo": "razonamiento", "tema": "caso práctico incapacidad temporal que supera 365 días", "dificultad": "alta"},
        
        # RELACIÓN (1)
        {"tipo": "relacion", "tema": "relación entre LGSS y Constitución en derechos sociales", "dificultad": "media"}
    ]
    
    qa_generadas = []
    
    for i, tarea in enumerate(tareas, 1):
        tipo = tarea["tipo"]
        tema = tarea["tema"]
        dificultad = tarea["dificultad"]
        
        print(f"\n{'─'*60}")
        print(f"[{i}/10] Tipo: {tipo.upper()} | Tema: {tema}")
        print('─'*60)
        
        # 1. Consultar RAG
        print(f"   1️⃣ Consultando RAG...")
        rag_result = consultar_rag(tema, limit=3)
        results = rag_result.get("results", [])
        
        if not results:
            print(f"   ⚠️  Sin resultados RAG, saltando...")
            continue
        
        print(f"   ✅ {len(results)} resultados encontrados")
        
        # 2. Preparar contexto
        contexto = "\n\n".join([
            f"[{r.get('title', 'Doc')}]\n{r.get('content', '')[:500]}"
            for r in results
        ])
        
        # 3. Instrucción específica por tipo
        if tipo == "test":
            instruccion_tipo = "Genera una pregunta tipo test con 4 opciones (A, B, C, D). Solo una correcta."
        elif tipo == "comparacion":
            instruccion_tipo = "Genera una pregunta que compare dos conceptos legales, explicando diferencias clave."
        elif tipo == "procedimiento":
            instruccion_tipo = "Genera una pregunta sobre los pasos de un procedimiento administrativo, en orden."
        elif tipo == "razonamiento":
            instruccion_tipo = "Genera un caso práctico que requiera razonamiento legal paso a paso con conclusión."
        elif tipo == "relacion":
            instruccion_tipo = "Genera una pregunta sobre cómo se relacionan dos normas o conceptos legales."
        
        prompt_completo = f"{instruccion_tipo}\n\nTema: {tema}\nDificultad: {dificultad}"
        
        # 4. Generar con Groq
        print(f"   2️⃣ Generando tipo '{tipo}'...")
        qa = generar_con_groq(prompt_completo, contexto)
        
        if qa:
            qa["id"] = f"AGENTIC-{i:03d}"
            qa["tipo"] = tipo
            qa["dificultad"] = dificultad
            qa_generadas.append(qa)
            print(f"   ✅ Generada: {qa['pregunta'][:60]}...")
        else:
            print(f"   ❌ Error generando Q&A")
    
    # Guardar resultados
    if qa_generadas:
        output_file = f"qa_agentic_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for qa in qa_generadas:
                f.write(json.dumps(qa, ensure_ascii=False) + '\n')
        
        print("\n" + "="*60)
        print(f"✅ COMPLETADO: {len(qa_generadas)}/10 Q&A generadas")
        print("="*60)
        
        # Estadísticas
        from collections import Counter
        tipos_count = Counter(qa["tipo"] for qa in qa_generadas)
        print("\n📊 TIPOS GENERADOS:")
        for tipo, count in tipos_count.items():
            print(f"   {tipo}: {count}")
        
        print(f"\n📁 Guardado en: {output_file}")
        
        # Mostrar muestra
        if qa_generadas:
            print("\n📋 MUESTRA (primera pregunta):")
            print(json.dumps(qa_generadas[0], indent=2, ensure_ascii=False))
    else:
        print("\n❌ No se generaron Q&A")

if __name__ == "__main__":
    generar_10_qa()
