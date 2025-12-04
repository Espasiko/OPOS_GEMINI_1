#!/usr/bin/env python3
"""
Comparación de calidad de Q&A generadas por todos los modelos
"""

import os
import json
from datetime import datetime

def load_json_file(filepath):
    """Carga archivo JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content.startswith('['):
                return json.loads(content)
            else:
                # JSONL
                return [json.loads(line) for line in content.split('\n') if line.strip()]
    except Exception as e:
        return []

def analyze_qa_quality(qa_list, model_name):
    """Analiza calidad de un conjunto de Q&A"""
    if not qa_list:
        return None
    
    stats = {
        'model': model_name,
        'total': len(qa_list),
        'avg_pregunta_len': 0,
        'avg_explicacion_len': 0,
        'con_articulos': 0,
        'con_dificultad': 0,
        'dificultades': {},
        'campos_completos': 0,
        'quality_score': 0
    }
    
    pregunta_lens = []
    explicacion_lens = []
    
    for qa in qa_list:
        # Longitudes
        pregunta = qa.get('pregunta', '')
        explicacion = qa.get('explicacion', '')
        pregunta_lens.append(len(pregunta))
        explicacion_lens.append(len(explicacion))
        
        # Artículos
        if qa.get('articulos') or qa.get('articulos_referencia') or 'art.' in explicacion.lower():
            stats['con_articulos'] += 1
        
        # Dificultad
        dif = qa.get('dificultad', 'N/A')
        if dif != 'N/A':
            stats['con_dificultad'] += 1
            stats['dificultades'][dif] = stats['dificultades'].get(dif, 0) + 1
        
        # Campos completos
        required = ['pregunta', 'opciones', 'respuesta_correcta', 'explicacion']
        if all(qa.get(f) for f in required):
            stats['campos_completos'] += 1
    
    # Promedios
    stats['avg_pregunta_len'] = sum(pregunta_lens) / len(pregunta_lens) if pregunta_lens else 0
    stats['avg_explicacion_len'] = sum(explicacion_lens) / len(explicacion_lens) if explicacion_lens else 0
    
    # Quality Score (0-100)
    score = 0
    score += min(30, stats['avg_pregunta_len'] / 10)  # Hasta 30 pts por longitud pregunta
    score += min(30, stats['avg_explicacion_len'] / 20)  # Hasta 30 pts por explicación
    score += (stats['con_articulos'] / stats['total']) * 20  # 20 pts por referencias legales
    score += (stats['campos_completos'] / stats['total']) * 20  # 20 pts por completitud
    stats['quality_score'] = round(score, 1)
    
    return stats

def main():
    print("\n" + "=" * 70)
    print("📊 COMPARACIÓN DE CALIDAD - TODOS LOS MODELOS")
    print("=" * 70)
    
    # Archivos a analizar
    files = {
        'Claude (5 MaxDif)': 'qa_claude_5_maxdif_20251203_163524.json',
        'Cohere (20)': 'qa_cohere_20_20251203_163417.json',
        'DeepSeek Reasoner (3)': 'qa_deepseek_reasoner_20_20251203_164107.json',
        'Groq Llama3.3 (20)': 'qa_groq_llama33_20_20251203_163920.json',
        'Kimi K2 (9)': 'qa_kimi_10_20251203_163928.json',
        'Kiro MaxQuality (10)': 'qa_kiro_maxquality_10_20251203_165000.json',
        'Mistral MaxDif (10)': 'qa_mistral_10_maxdif_20251203_180448.json',
        'Mistral API (20)': 'qa_mistral_api_20_20251203_161500.json',
        'Combinado (20)': 'qa_combinado_20_20251203_162236.json',
    }
    
    results = []
    
    for model_name, filename in files.items():
        filepath = f'dataset_output/{filename}'
        if os.path.exists(filepath) and os.path.getsize(filepath) > 10:
            qa_list = load_json_file(filepath)
            stats = analyze_qa_quality(qa_list, model_name)
            if stats:
                results.append(stats)
                print(f"\n✅ {model_name}: {stats['total']} Q&A")
        else:
            print(f"\n❌ {model_name}: archivo no encontrado o vacío")
    
    # Ordenar por quality score
    results.sort(key=lambda x: x['quality_score'], reverse=True)
    
    # Tabla comparativa
    print("\n" + "=" * 70)
    print("🏆 RANKING POR CALIDAD")
    print("=" * 70)
    print(f"{'#':<3} {'Modelo':<25} {'Q&A':<5} {'Preg':<6} {'Expl':<6} {'Arts':<5} {'Score':<6}")
    print("-" * 70)
    
    for i, r in enumerate(results, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        print(f"{medal}{i:<2} {r['model']:<25} {r['total']:<5} {int(r['avg_pregunta_len']):<6} {int(r['avg_explicacion_len']):<6} {r['con_articulos']:<5} {r['quality_score']:<6}")
    
    # Resumen por dificultad
    print("\n" + "=" * 70)
    print("📈 DISTRIBUCIÓN DE DIFICULTAD POR MODELO")
    print("=" * 70)
    
    for r in results:
        if r['dificultades']:
            difs = ', '.join([f"{k}: {v}" for k, v in r['dificultades'].items()])
            print(f"{r['model']:<25} → {difs}")
    
    # Total Q&A generadas
    total_qa = sum(r['total'] for r in results)
    print("\n" + "=" * 70)
    print(f"📊 TOTAL Q&A GENERADAS: {total_qa}")
    print("=" * 70)
    
    # Mejor modelo
    if results:
        best = results[0]
        print(f"\n🏆 MEJOR MODELO: {best['model']}")
        print(f"   Score: {best['quality_score']}/100")
        print(f"   Promedio pregunta: {int(best['avg_pregunta_len'])} chars")
        print(f"   Promedio explicación: {int(best['avg_explicacion_len'])} chars")
        print(f"   Con referencias legales: {best['con_articulos']}/{best['total']}")
    
    # Guardar resultados
    with open('dataset_output/comparacion_modelos.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n📁 Guardado: dataset_output/comparacion_modelos.json")

if __name__ == "__main__":
    main()
