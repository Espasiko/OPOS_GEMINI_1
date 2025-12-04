#!/usr/bin/env python3
"""Comparador de calidad entre Q&A de Mistral API vs Mistral Local"""

import json
import os
from datetime import datetime

print("\n📊 COMPARACIÓN DE CALIDAD: MISTRAL API vs MISTRAL LOCAL\n")

# Buscar archivos más recientes
api_files = [f for f in os.listdir('dataset_output') if 'mistral_api' in f and f.endswith('.json')]
local_files = [f for f in os.listdir('dataset_output') if 'mistral_local' in f and f.endswith('.json')]

if not api_files:
    print("❌ No se encontraron archivos de Mistral API")
    exit(1)

# Cargar datos
api_file = sorted(api_files)[-1]  # Más reciente
print(f"📁 Archivo API: {api_file}")

with open(f'dataset_output/{api_file}', 'r', encoding='utf-8') as f:
    api_qa = json.load(f)

local_qa = []
if local_files:
    local_file = sorted(local_files)[-1]
    print(f"📁 Archivo Local: {local_file}")
    with open(f'dataset_output/{local_file}', 'r', encoding='utf-8') as f:
        local_qa = json.load(f)
else:
    print("⚠️  No hay archivo de Mistral Local aún")

print(f"\n{'='*70}")
print(f"📈 ESTADÍSTICAS GENERALES")
print(f"{'='*70}")
print(f"Q&A Mistral API:   {len(api_qa)}")
print(f"Q&A Mistral Local: {len(local_qa)}")
print(f"Total Q&A:         {len(api_qa) + len(local_qa)}")

# Análisis de calidad
def analyze_qa(qa_list, name):
    if not qa_list:
        return
    
    print(f"\n{'='*70}")
    print(f"📋 ANÁLISIS DE CALIDAD: {name}")
    print(f"{'='*70}")
    
    # Métricas
    total = len(qa_list)
    avg_pregunta_len = sum(len(q['pregunta']) for q in qa_list) / total
    avg_explicacion_len = sum(len(q.get('explicacion', '')) for q in qa_list) / total
    
    # Temas únicos
    temas = set(q.get('tema', 'Sin tema') for q in qa_list)
    
    # Respuestas correctas
    respuestas = {}
    for q in qa_list:
        r = q.get('respuesta_correcta', '?')
        respuestas[r] = respuestas.get(r, 0) + 1
    
    print(f"Total Q&A:                    {total}")
    print(f"Longitud media pregunta:      {avg_pregunta_len:.0f} caracteres")
    print(f"Longitud media explicación:   {avg_explicacion_len:.0f} caracteres")
    print(f"Temas únicos:                 {len(temas)}")
    print(f"Distribución respuestas:      {respuestas}")
    
    print(f"\n📚 Temas cubiertos:")
    for tema in sorted(temas):
        count = sum(1 for q in qa_list if q.get('tema') == tema)
        print(f"  - {tema}: {count}")
    
    # Muestras
    print(f"\n📝 MUESTRAS ({name}):")
    for i, qa in enumerate(qa_list[:3], 1):
        print(f"\n--- Muestra {i} ---")
        print(f"Tema: {qa.get('tema', 'N/A')}")
        print(f"Pregunta: {qa['pregunta'][:200]}...")
        print(f"Opciones: {len(qa.get('opciones', []))} opciones")
        print(f"Correcta: {qa.get('respuesta_correcta', 'N/A')}")
        print(f"Explicación: {qa.get('explicacion', 'N/A')[:150]}...")

analyze_qa(api_qa, "MISTRAL API")
analyze_qa(local_qa, "MISTRAL LOCAL")

# Comparación directa
if api_qa and local_qa:
    print(f"\n{'='*70}")
    print(f"⚖️  COMPARACIÓN DIRECTA")
    print(f"{'='*70}")
    
    api_avg_len = sum(len(q['pregunta']) for q in api_qa) / len(api_qa)
    local_avg_len = sum(len(q['pregunta']) for q in local_qa) / len(local_qa)
    
    api_avg_exp = sum(len(q.get('explicacion', '')) for q in api_qa) / len(api_qa)
    local_avg_exp = sum(len(q.get('explicacion', '')) for q in local_qa) / len(local_qa)
    
    print(f"                          API        LOCAL")
    print(f"Cantidad:                 {len(api_qa):>5}      {len(local_qa):>5}")
    print(f"Long. media pregunta:     {api_avg_len:>5.0f}      {local_avg_len:>5.0f}")
    print(f"Long. media explicación:  {api_avg_exp:>5.0f}      {local_avg_exp:>5.0f}")
    print(f"Temas únicos:             {len(set(q.get('tema') for q in api_qa)):>5}      {len(set(q.get('tema') for q in local_qa)):>5}")

# Exportar dataset combinado
if api_qa or local_qa:
    combined = api_qa + local_qa
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_file = f'dataset_output/qa_combinado_{len(combined)}_{timestamp}.json'
    
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"✅ DATASET COMBINADO EXPORTADO")
    print(f"{'='*70}")
    print(f"Archivo: {combined_file}")
    print(f"Total Q&A: {len(combined)}")
