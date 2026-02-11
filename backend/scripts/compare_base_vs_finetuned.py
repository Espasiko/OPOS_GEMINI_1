#!/usr/bin/env python3
"""
🔬 COMPARACIÓN: SALAMANDRA BASE vs SALAMANDRA FINETUNED
========================================================
Usa OLLAMA LOCAL porque HuggingFace API está deprecada (error 410)
"""

import json
import os
import sys
import time
import requests
from pathlib import Path
from typing import Dict
from datetime import datetime
from dotenv import load_dotenv

# Setup
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
os.chdir(BASE_DIR)
load_dotenv(BASE_DIR / "backend/.env.backend")

# Configuración
PREGUNTAS_JSON = Path("/tmp/todas_preguntas_enero25.json")
RESPUESTAS_OFICIALES = BASE_DIR / "extracted_texts/examenes_oficiales_academias/12._respuestas_examen_c1_extraord_enero_25.txt"
RESULTADOS_FINETUNED = BASE_DIR / "staging_area/06_01_26_enrichment/examen_enero25_COMPLETO_FINAL.jsonl"
RESULTS_DIR = BASE_DIR / "staging_area/comparacion_base_vs_finetuned"

# Ollama LOCAL
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "salamandra-base"

# RAG local (mismo que prueba 7h)
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

print("🔬 COMPARACIÓN: SALAMANDRA BASE vs FINETUNED")
print("=" * 60)
print(f"Modelo: {OLLAMA_MODEL} (Ollama local)")

# Init RAG
print("\n1️⃣ Inicializando RAG...")
qdrant = QdrantClient(url="http://localhost:6333", timeout=60.0)
embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
print("   ✅ RAG inicializado")

# Prompt anti-sesgo
PROMPT_ANTI_BIAS = """IMPORTANTE: La respuesta correcta puede ser A, B, C o D con IGUAL probabilidad.
NO asumas que ninguna posición es más probable que otra.
Analiza CADA opción de forma INDEPENDIENTE antes de elegir."""

def parse_respuestas_oficiales() -> Dict[int, str]:
    """Extrae respuestas correctas del archivo oficial."""
    import re
    content = RESPUESTAS_OFICIALES.read_text(encoding='utf-8')
    respuestas = {}
    matches = re.findall(r'(\d+)\s+([ABCD])\s', content)
    for num, letra in matches:
        num = int(num)
        if num not in respuestas:
            respuestas[num] = letra.lower()
    return respuestas

def load_resultados_finetuned() -> Dict[int, Dict]:
    """Carga resultados del modelo finetuned (prueba 7h)."""
    resultados = {}
    with open(RESULTADOS_FINETUNED, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                resultados[item['question_id']] = item
    return resultados

def search_rag(query: str) -> str:
    """Busca contexto legal en RAG local (mismo que prueba 7h)."""
    vector = embedder.encode(query).tolist()
    results = qdrant.search(
        collection_name="opositaia_knowledge_hybrid_FULL",
        query_vector=("dense", vector),
        limit=10,
        with_payload=True,
        score_threshold=0.3
    )
    context = "===CONTEXTO LEGAL===\n\n"
    for i, hit in enumerate(results, 1):
        context += f"[{i}] {hit.payload.get('law_name', 'Unknown')}\n"
        context += f"{hit.payload.get('text_snippet', hit.payload.get('text', ''))}\n\n"
    return context

def query_ollama(prompt: str) -> Dict:
    """Consulta modelo base en Ollama LOCAL."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 500}
            },
            timeout=300
        )
        if response.status_code == 200:
            result = response.json()
            return {"success": True, "text": result.get('response', '')}
        return {"success": False, "error": f"Status {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def parse_respuesta(text: str) -> str:
    """Extrae opción seleccionada - VERSIÓN MEJORADA."""
    import re
    text = str(text)
    # 1. selected_option: X
    match = re.search(r'selected_option:\s*\[?([a-dA-D])\]?', text, re.IGNORECASE)
    if match: return match.group(1).lower()
    # 2. answer: X o answer: [X]
    match = re.search(r'answer:\s*\[?([a-dA-D])\]?', text, re.IGNORECASE)
    if match: return match.group(1).lower()
    # 3. La respuesta correcta es X
    match = re.search(r'respuesta\s+(correcta|es)\s+\[?([a-dA-D])\]?', text, re.IGNORECASE)
    if match: return match.group(2).lower()
    # 4. respuesta: X
    match = re.search(r'respuesta[:\s]+([a-d])', text.lower())
    if match: return match.group(1)
    # 5. opción: X
    match = re.search(r'opci[oó]n[:\s]+([a-d])', text.lower())
    if match: return match.group(1)
    # 6. [A] al inicio
    match = re.search(r'\[([a-dA-D])\]', text[:200])
    if match: return match.group(1).lower()
    # 7. letra seguida de )
    match = re.search(r'\b([a-d])\)', text.lower()[:150])
    if match: return match.group(1)
    return "?"

def main():
    # Cargar datos
    print("\n2️⃣ Cargando datos...")
    
    if not PREGUNTAS_JSON.exists():
        print(f"   ❌ No existe: {PREGUNTAS_JSON}")
        return
    
    with open(PREGUNTAS_JSON, 'r', encoding='utf-8') as f:
        preguntas = json.load(f)
    print(f"   ✅ {len(preguntas)} preguntas cargadas")
    
    respuestas_oficiales = parse_respuestas_oficiales()
    print(f"   ✅ {len(respuestas_oficiales)} respuestas oficiales")
    
    resultados_ft = load_resultados_finetuned()
    print(f"   ✅ {len(resultados_ft)} resultados finetuned")
    
    # Test Ollama
    print("\n3️⃣ Verificando Ollama...")
    test = query_ollama("Responde solo: OK")
    if not test['success']:
        print(f"   ❌ {test['error']}")
        print("   Asegúrate de que Ollama está corriendo: ollama serve")
        return
    print("   ✅ Ollama OK")
    
    # Crear directorio
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESULTS_DIR / f"comparacion_{datetime.now().strftime('%Y%m%d_%H%M')}.jsonl"
    
    # Procesar
    print("\n4️⃣ Procesando preguntas...")
    print("-" * 60)
    
    resultados = []
    base_correct = 0
    ft_correct = 0
    
    for i, q in enumerate(preguntas):
        qid = q['id']
        if qid not in respuestas_oficiales or qid not in resultados_ft:
            continue
        
        correcta = respuestas_oficiales[qid]
        ft_respuesta = resultados_ft[qid]['selected_option'].lower()
        
        # RAG
        context = search_rag(q['question'])
        
        # Prompt
        opciones = "\n".join([f"{chr(97+i).upper()}) {opt}" for i, opt in enumerate(q['options'])])
        prompt = f"""Eres un experto en Seguridad Social española.

{PROMPT_ANTI_BIAS}

CONTEXTO LEGAL:
{context[:2000]}

PREGUNTA:
{q['question']}

OPCIONES:
{opciones}

Responde en formato:
selected_option: [a/b/c/d]
thought_process: [razonamiento breve]
"""
        
        print(f"   [{i+1}/{len(preguntas)}] Pregunta {qid}...", end=" ", flush=True)
        start = time.time()
        
        result = query_ollama(prompt)
        
        if result['success']:
            base_respuesta = parse_respuesta(result['text'])
            elapsed = time.time() - start
            
            base_ok = base_respuesta == correcta
            ft_ok = ft_respuesta == correcta
            
            if base_ok: base_correct += 1
            if ft_ok: ft_correct += 1
            
            resultado = {
                "question_id": qid,
                "correct_answer": correcta,
                "base_answer": base_respuesta,
                "finetuned_answer": ft_respuesta,
                "base_correct": base_ok,
                "ft_correct": ft_ok,
                "base_reasoning": result['text'][:300],
                "time_seconds": round(elapsed, 1)
            }
            resultados.append(resultado)
            
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(resultado, ensure_ascii=False) + '\n')
            
            status = "✅" if base_ok else "❌"
            print(f"{status} Base={base_respuesta} FT={ft_respuesta} Correcta={correcta} ({elapsed:.1f}s)")
        else:
            print(f"❌ {result['error'][:40]}")
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    total = len(resultados)
    if total > 0:
        print(f"\n📈 PRECISIÓN:")
        print(f"   BASE:      {base_correct}/{total} = {base_correct/total*100:.1f}%")
        print(f"   FINETUNED: {ft_correct}/{total} = {ft_correct/total*100:.1f}%")
        
        base_b = sum(1 for r in resultados if r['base_answer'] == 'b')
        ft_b = sum(1 for r in resultados if r['finetuned_answer'] == 'b')
        print(f"\n📉 SESGO HACIA B:")
        print(f"   BASE:      {base_b}/{total} = {base_b/total*100:.1f}%")
        print(f"   FINETUNED: {ft_b}/{total} = {ft_b/total*100:.1f}%")
        
        print(f"\n📁 Guardado: {output_file}")

if __name__ == "__main__":
    main()
