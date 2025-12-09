#!/usr/bin/env python3
"""
Consolidador de Dataset Final

Combina:
1. dataset_consolidado_top100.jsonl (100 Q&A iniciales)
2. nuevas_qa_gemini_5k_*.jsonl (5,000 Q&A generadas)

Output: dataset_final_5100.jsonl (o menos si se aplican filtros)

Procesos:
- Deduplicación por pregunta
- Filtro de calidad (score > 60)
- Normalización de campos
- Rankeo por score
- Metadatos de combinación
"""

import os
import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

print("\n" + "="*70)
print("🔗 CONSOLIDADOR DE DATASET FINAL")
print("="*70)

# ============================================================
# CONFIGURACIÓN
# ============================================================

DATASET_DIR = Path("dataset_output")
MIN_QUALITY_SCORE = 40  # Mínima calidad aceptada

# ============================================================
# FUNCIONES
# ============================================================

def load_jsonl_file(filepath):
    """Carga archivo JSONL"""
    qa_list = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    qa = json.loads(line.strip())
                    if qa and qa.get('pregunta'):
                        qa_list.append(qa)
                except json.JSONDecodeError as e:
                    print(f"  ⚠️ Error JSON línea {line_num}: {str(e)[:50]}")
    except Exception as e:
        print(f"  ⚠️ Error leyendo {filepath.name}: {str(e)[:50]}")
    
    return qa_list

def normalize_qa(qa, source):
    """Normaliza estructura Q&A"""
    normalized = {
        'pregunta': qa.get('pregunta', ''),
        'opciones': qa.get('opciones', []),
        'respuesta_correcta': qa.get('respuesta_correcta'),
        'explicacion': qa.get('explicacion', ''),
        'articulos': qa.get('articulos', []),
        'tema': qa.get('tema', 'general'),
        'dificultad': qa.get('dificultad', 'media'),
        'source': source,
        'original_score': qa.get('_qa_score', qa.get('_model_score', 0)),
    }
    return normalized

def calculate_final_score(qa):
    """Calcula score final consolidado"""
    score = 0
    
    # 1. Longitud pregunta (0-25)
    pregunta_len = len(qa.get('pregunta', ''))
    if 100 < pregunta_len < 500:
        score += 25
    elif 50 < pregunta_len < 800:
        score += 20
    elif pregunta_len > 30:
        score += 10
    
    # 2. Explicación detallada (0-25)
    explicacion_len = len(qa.get('explicacion', ''))
    if 200 < explicacion_len < 1000:
        score += 25
    elif 100 < explicacion_len < 1500:
        score += 20
    elif explicacion_len > 50:
        score += 10
    
    # 3. Referencias legales (0-25)
    articulos = qa.get('articulos', [])
    if isinstance(articulos, list) and len(articulos) >= 2:
        score += 25
    elif articulos and len(articulos) > 0:
        score += 15
    elif 'art.' in qa.get('explicacion', '').lower():
        score += 10
    
    # 4. Completitud (0-25)
    required_fields = ['pregunta', 'opciones', 'respuesta_correcta', 'explicacion']
    if all(qa.get(f) for f in required_fields):
        if len(qa.get('opciones', [])) == 4:
            score += 25
        else:
            score += 20
    else:
        score += 5
    
    return score

def deduplicate_questions(qa_list):
    """Elimina preguntas duplicadas o muy similares"""
    seen = {}
    deduplicated = []
    
    for qa in qa_list:
        pregunta = qa.get('pregunta', '').lower().strip()
        
        # Buscar pregunta similar
        encontrada = False
        for key in seen:
            # Comparar primeras 50 caracteres
            if key[:50] == pregunta[:50]:
                # Mantener la de mayor score
                if qa.get('_final_score', 0) > seen[key]['_final_score']:
                    idx = deduplicated.index(seen[key])
                    deduplicated[idx] = qa
                    seen[key] = qa
                encontrada = True
                break
        
        if not encontrada:
            seen[pregunta] = qa
            deduplicated.append(qa)
    
    return deduplicated

# ============================================================
# MAIN
# ============================================================

def main():
    print("\n📦 INICIANDO CONSOLIDACIÓN...")
    
    if not DATASET_DIR.exists():
        print(f"❌ Directorio no encontrado: {DATASET_DIR}")
        return
    
    # 1. CARGAR DATASETS EXISTENTES
    print("\n📂 Paso 1: Cargando datasets...")
    
    all_qa = []
    stats = {
        'consolidado': 0,
        'gemini': 0,
        'otros': 0
    }
    
    # Cargar dataset consolidado inicial
    dataset_top100 = DATASET_DIR / "dataset_consolidado_top100.jsonl"
    if dataset_top100.exists():
        print(f"  ✅ {dataset_top100.name}", end=" ... ")
        qa_list = load_jsonl_file(dataset_top100)
        for qa in qa_list:
            normalized = normalize_qa(qa, "consolidado_top100")
            all_qa.append(normalized)
        stats['consolidado'] = len(qa_list)
        print(f"✓ {len(qa_list)} Q&A")
    else:
        print(f"  ⚠️ {dataset_top100.name}: NO ENCONTRADO")
    
    # Cargar nuevos datasets Gemini (si existen)
    print(f"\n  Buscando datasets Gemini...", end=" ")
    gemini_files = list(DATASET_DIR.glob("nuevas_qa_gemini_*.jsonl"))
    if gemini_files:
        print(f"✓ Encontrados {len(gemini_files)}")
        for gemini_file in sorted(gemini_files):
            print(f"    ✅ {gemini_file.name}", end=" ... ")
            qa_list = load_jsonl_file(gemini_file)
            for qa in qa_list:
                normalized = normalize_qa(qa, f"gemini_{gemini_file.stem.split('_')[-1]}")
                all_qa.append(normalized)
            stats['gemini'] += len(qa_list)
            print(f"✓ {len(qa_list)} Q&A")
    else:
        print("❌ NO ENCONTRADOS")
        print("  ℹ️ Ejecuta primero: python3 generar_qa_gemini_5k.py")
    
    # Cargar otros datasets JSON (compatibilidad)
    print(f"\n  Buscando otros datasets...", end=" ")
    json_files = list(DATASET_DIR.glob("qa_*.json"))
    json_files = [f for f in json_files if f.name not in [
        "dataset_consolidado_top100.jsonl",
        "analisis_completo.json"
    ]]
    if json_files:
        print(f"✓ Encontrados {len(json_files)}")
        for json_file in sorted(json_files)[:3]:  # Máximo 3 para evitar duplicados
            print(f"    ✅ {json_file.name}", end=" ... ")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        qa_list = data
                    else:
                        qa_list = [data]
                    
                    for qa in qa_list:
                        if qa.get('pregunta'):
                            normalized = normalize_qa(qa, json_file.stem)
                            all_qa.append(normalized)
                    stats['otros'] += len(qa_list)
                    print(f"✓ {len(qa_list)} Q&A")
            except Exception as e:
                print(f"❌ {str(e)[:30]}")
    else:
        print("✗ NO ENCONTRADOS")
    
    print(f"\n  📊 Total cargado: {len(all_qa)} Q&A")
    print(f"     - Consolidado: {stats['consolidado']}")
    print(f"     - Gemini: {stats['gemini']}")
    print(f"     - Otros: {stats['otros']}")
    
    if len(all_qa) == 0:
        print("❌ No hay datos para consolidar")
        return
    
    # 2. CALCULAR SCORES FINALES
    print("\n📈 Paso 2: Calculando scores finales...")
    for qa in all_qa:
        qa['_final_score'] = calculate_final_score(qa)
    
    print(f"  ✓ Score calculado para {len(all_qa)} Q&A")
    print(f"  Score mín: {min(qa['_final_score'] for qa in all_qa):.1f}")
    print(f"  Score máx: {max(qa['_final_score'] for qa in all_qa):.1f}")
    print(f"  Score prom: {sum(qa['_final_score'] for qa in all_qa) / len(all_qa):.1f}")
    
    # 3. FILTRO DE CALIDAD
    print(f"\n🔍 Paso 3: Aplicando filtros de calidad (min: {MIN_QUALITY_SCORE})...")
    filtered_qa = [qa for qa in all_qa if qa['_final_score'] >= MIN_QUALITY_SCORE]
    removed = len(all_qa) - len(filtered_qa)
    
    print(f"  ✓ {len(filtered_qa)} Q&A válidas")
    print(f"  ❌ {removed} Q&A descartadas (score < {MIN_QUALITY_SCORE})")
    
    if len(filtered_qa) == 0:
        print("❌ No quedan Q&A después del filtro")
        return
    
    # 4. DEDUPLICACIÓN
    print(f"\n🔗 Paso 4: Deduplicando...")
    deduplicated = deduplicate_questions(filtered_qa)
    removed_dups = len(filtered_qa) - len(deduplicated)
    
    print(f"  ✓ {len(deduplicated)} Q&A únicas")
    print(f"  ⚠️ {removed_dups} Q&A duplicadas removidas")
    
    # 5. ORDENAR POR SCORE
    print(f"\n⬇️ Paso 5: Ordenando por calidad...")
    deduplicated.sort(key=lambda x: x['_final_score'], reverse=True)
    print(f"  ✓ Ordenadas de mayor a menor score")
    
    # 6. GUARDAR DATASET FINAL
    print(f"\n💾 Paso 6: Guardando dataset final...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = DATASET_DIR / f"dataset_final_{len(deduplicated)}_{timestamp}.jsonl"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for qa in deduplicated:
            # Remover campos internos
            qa_clean = {k: v for k, v in qa.items() if not k.startswith('_')}
            f.write(json.dumps(qa_clean, ensure_ascii=False) + '\n')
    
    print(f"  ✅ Guardado: {output_file.name}")
    
    # 7. CREAR LINK PRINCIPAL
    main_link = DATASET_DIR / "dataset_final.jsonl"
    if main_link.exists():
        main_link.unlink()
    try:
        # En Windows, copiar en lugar de hacer symlink
        import shutil
        shutil.copy(output_file, main_link)
        print(f"  ✅ Link principal: {main_link.name}")
    except:
        pass
    
    # 8. GENERAR REPORTE
    print(f"\n📊 Paso 7: Generando reporte...")
    
    # Distribución por fuente
    source_dist = defaultdict(int)
    for qa in deduplicated:
        source_dist[qa['source']] += 1
    
    # Distribución por dificultad
    dificultad_dist = defaultdict(int)
    for qa in deduplicated:
        dificultad_dist[qa['dificultad']] += 1
    
    # Distribución por tema
    tema_dist = defaultdict(int)
    for qa in deduplicated:
        tema_dist[qa.get('tema', 'general')] += 1
    
    reporte = {
        'timestamp': datetime.now().isoformat(),
        'total_qa': len(deduplicated),
        'score_promedio': sum(qa['_final_score'] for qa in deduplicated) / len(deduplicated),
        'score_min': min(qa['_final_score'] for qa in deduplicated),
        'score_max': max(qa['_final_score'] for qa in deduplicated),
        'por_fuente': dict(source_dist),
        'por_dificultad': dict(dificultad_dist),
        'por_tema': dict(tema_dist),
        'estadisticas': {
            'total_inicial': len(all_qa),
            'removidas_por_filtro': removed,
            'removidas_por_duplicado': removed_dups,
            'final_validas': len(deduplicated)
        }
    }
    
    reporte_file = DATASET_DIR / f"reporte_consolidacion_{timestamp}.json"
    with open(reporte_file, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ Reporte: {reporte_file.name}")
    
    # RESUMEN FINAL
    print("\n" + "="*70)
    print("✅ CONSOLIDACIÓN COMPLETADA")
    print("="*70)
    print(f"\n📈 RESUMEN:")
    print(f"   Total Q&A consolidadas: {len(deduplicated)}")
    print(f"   Score promedio: {reporte['score_promedio']:.1f}/100")
    print(f"   Rango: {reporte['score_min']:.1f} - {reporte['score_max']:.1f}")
    
    print(f"\n📊 DISTRIBUCIÓN:")
    print(f"   Por fuente:")
    for source, count in sorted(source_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"      • {source}: {count}")
    print(f"   Por dificultad:")
    for dif, count in sorted(dificultad_dist.items()):
        print(f"      • {dif}: {count}")
    
    print(f"\n📁 ARCHIVOS:")
    print(f"   • Dataset: {output_file.name}")
    print(f"   • Link: {main_link.name}")
    print(f"   • Reporte: {reporte_file.name}")
    
    print(f"\n🚀 PRÓXIMOS PASOS:")
    print(f"   1. Revisar reporte: {reporte_file.name}")
    print(f"   2. Evaluar: cd ../backend/scripts && python3 evaluate_rag_gemini.py")
    print(f"   3. Fine-tune: (en laptop con 16GB RAM)")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Consolidación interrumpida")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
