#!/usr/bin/env python3
"""
🔬 COMPARACIÓN: SALAMANDRA BASE vs FINETUNED (HUGGINGFACE VERSION)
===================================================================
Usa la NUEVA API de HuggingFace (router.huggingface.co)
Formato: https://router.huggingface.co/hf-inference/models/{model}

NOTA: Esta es una copia del script con HuggingFace arreglado.
El script principal usa Ollama local.
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

# HuggingFace NUEVA API (router.huggingface.co)
HF_TOKEN = os.environ.get('HF_TOKEN', '')
HF_MODEL = "BSC-LT/salamandra-7b-instruct"
# NUEVA URL - antes era api-inference.huggingface.co (DEPRECADA en 2025)
HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

# RAG local
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

print("🔬 COMPARACIÓN: SALAMANDRA BASE vs FINETUNED (HuggingFace)")
print("=" * 60)
print(f"Modelo: {HF_MODEL}")
print(f"API URL: {HF_API_URL}")
print(f"HF Token: {HF_TOKEN[:10]}..." if HF_TOKEN else "⚠️ Sin HF Token")

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
    resultados = {}
    with open(RESULTADOS_FINETUNED, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                resultados[item['question_id']] = item
    return resultados

def search_rag(query: str) -> str:
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

def query_hf_new_api(prompt: str) -> Dict:
    """
    Consulta HuggingFace con la NUEVA API (router.huggingface.co)
    
    Formato nuevo:
    - URL: https://router.huggingface.co/hf-inference/models/{model}
    - Headers: Authorization: Bearer {token}
    - Body: {"inputs": "...", "parameters": {...}}
    """
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.3,
            "return_full_text": False,
            "do_sample": True
        }
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=180)
        
        if response.status_code == 200:
            result = response.json()
            # La respuesta puede ser lista o dict dependiendo del modelo
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get('generated_text', '')
            elif isinstance(result, dict):
                text = result.get('generated_text', result.get('text', ''))
            else:
                text = str(result)
            return {"success": True, "text": text}
        
        if response.status_code == 503:
            # Modelo cargando
            estimated_time = response.json().get('estimated_time', 20)
            return {"success": False, "error": f"Modelo cargando (~{estimated_time}s)", "retry": True}
        
        if response.status_code == 401:
            return {"success": False, "error": "Token inválido o sin permisos de Inference", "retry": False}
        
        if response.status_code == 404:
            return {"success": False, "error": f"Modelo no encontrado: {HF_MODEL}", "retry": False}
            
        return {"success": False, "error": f"Status {response.status_code}: {response.text[:200]}", "retry": False}
    
    except requests.Timeout:
        return {"success": False, "error": "Timeout (180s)", "retry": True}
    except Exception as e:
        return {"success": False, "error": str(e), "retry": False}

def parse_respuesta(text: str) -> str:
    import re
    match = re.search(r'selected_option:\s*([a-dA-D])', text, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    match = re.search(r'respuesta[:\s]+([a-d])', text.lower())
    if match:
        return match.group(1)
    match = re.search(r'opci[oó]n[:\s]+([a-d])', text.lower())
    if match:
        return match.group(1)
    match = re.search(r'\b([a-d])\)', text.lower())
    if match:
        return match.group(1)
    return "?"

def main():
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
    
    # Test HuggingFace
    print("\n3️⃣ Verificando HuggingFace (nueva API)...")
    test = query_hf_new_api("Responde solo: OK")
    if not test['success']:
        print(f"   ⚠️ {test['error']}")
        if test.get('retry'):
            print("   Esperando 30s y reintentando...")
            time.sleep(30)
            test = query_hf_new_api("Responde solo: OK")
            if not test['success']:
                print(f"   ❌ Falló de nuevo: {test['error']}")
                print("\n   Posibles soluciones:")
                print("   1. Verificar que HF_TOKEN tiene permisos de 'Inference'")
                print("   2. El modelo puede requerir Inference Endpoints (de pago)")
                print("   3. Usar Ollama local: python compare_base_vs_finetuned.py")
                return
    else:
        print("   ✅ HuggingFace OK")
    
    # Crear directorio
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESULTS_DIR / f"comparacion_hf_{datetime.now().strftime('%Y%m%d_%H%M')}.jsonl"
    
    # Procesar
    print("\n4️⃣ Procesando preguntas...")
    print("-" * 60)
    
    resultados = []
    base_correct = 0
    ft_correct = 0
    retries = 0
    max_retries = 3
    
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
        
        result = query_hf_new_api(prompt)
        
        # Retry si es necesario
        while not result['success'] and result.get('retry') and retries < max_retries:
            retries += 1
            print(f"(retry {retries})...", end=" ", flush=True)
            time.sleep(20)
            result = query_hf_new_api(prompt)
        
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
            retries = 0  # Reset retries
        else:
            print(f"❌ {result['error'][:40]}")
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    total = len(resultados)
    if total > 0:
        print(f"\n📈 PRECISIÓN:")
        print(f"   BASE (HF):  {base_correct}/{total} = {base_correct/total*100:.1f}%")
        print(f"   FINETUNED:  {ft_correct}/{total} = {ft_correct/total*100:.1f}%")
        
        base_b = sum(1 for r in resultados if r['base_answer'] == 'b')
        ft_b = sum(1 for r in resultados if r['finetuned_answer'] == 'b')
        print(f"\n📉 SESGO HACIA B:")
        print(f"   BASE:      {base_b}/{total} = {base_b/total*100:.1f}%")
        print(f"   FINETUNED: {ft_b}/{total} = {ft_b/total*100:.1f}%")
        
        print(f"\n📁 Guardado: {output_file}")

if __name__ == "__main__":
    main()
