#!/usr/bin/env python3
"""
FASE 1: LIMPIEZA DEL DATASET
- Eliminar items con score <70
- Clasificar items "unknown" por tipo
- Validar campos requeridos
"""

import json
import re
from pathlib import Path

DATASET = Path("golden_dataset/consolidated/golden_dataset_consolidated_20251221.jsonl")
OUTPUT = Path("golden_dataset/consolidated/golden_dataset_cleaned.jsonl")

def classify_tipo(item):
    """Clasificar item por tipo basado en su contenido"""
    
    # Si ya tiene tipo definido y no es "unknown", mantenerlo
    tipo_actual = item.get('tipo', 'unknown')
    if tipo_actual and tipo_actual != 'unknown' and tipo_actual.strip():
        return tipo_actual
    
    # Clasificar por contenido
    if 'opciones' in item and isinstance(item.get('opciones'), list):
        if len(item['opciones']) == 4:
            return 'test'
    
    if 'escenario' in item or 'caso' in item.get('pregunta', '').lower():
        return 'caso_practico'
    
    if 'razonamiento' in item or 'pasos' in item:
        return 'razonamiento_juridico'
    
    if 'comparación' in item.get('pregunta', '').lower() or 'diferencia' in item.get('pregunta', '').lower():
        return 'comparacion'
    
    if 'procedimiento' in item.get('pregunta', '').lower():
        return 'procedimiento'
    
    if 'flashcard' in item or 'tarjeta' in item:
        return 'flashcard'
    
    # Por defecto, si tiene pregunta y respuesta, es Q&A
    if 'pregunta' in item and ('respuesta' in item or 'explicacion' in item):
        return 'qa_simple'
    
    return 'unknown'

def calculate_score(item):
    """Calcular score de calidad de un item"""
    score = 100
    
    # Verificar campos requeridos
    if 'pregunta' not in item or not item['pregunta']:
        score -= 20
    
    if 'explicacion' not in item or not item['explicacion']:
        score -= 20
    
    # Verificar calidad de explicación
    explicacion = item.get('explicacion', '')
    if len(explicacion) < 50:
        score -= 10
    
    # Verificar citas legales
    articulos = extract_articulos(explicacion)
    if not articulos:
        score -= 15
    
    # Verificar respuesta correcta (si es test)
    if 'opciones' in item and 'respuesta_correcta' not in item:
        score -= 20
    
    return max(0, score)

def extract_articulos(texto):
    """Extraer menciones de artículos del texto"""
    if not texto:
        return []
    
    patrones = [
        r'Art\.\s*(\d+)',
        r'Artículo\s*(\d+)',
        r'art\s+(\d+)',
    ]
    
    articulos = []
    for patron in patrones:
        matches = re.findall(patron, texto, re.IGNORECASE)
        articulos.extend(matches)
    
    return list(set(articulos))

def main():
    print("="*70)
    print("🧹 FASE 1: LIMPIEZA DEL DATASET")
    print("="*70)
    print(f"📁 Input: {DATASET}")
    print(f"📁 Output: {OUTPUT}")
    
    items = []
    stats = {
        'total': 0,
        'eliminados': 0,
        'clasificados': 0,
        'mantenidos': 0
    }
    
    print("\n📖 Leyendo dataset...")
    with open(DATASET, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            stats['total'] += 1
            
            # Calcular score
            score = calculate_score(item)
            
            # Eliminar si score < 70
            if score < 70:
                stats['eliminados'] += 1
                continue
            
            # Clasificar tipo
            tipo_original = item.get('tipo', 'unknown')
            tipo_nuevo = classify_tipo(item)
            
            if tipo_original in ['unknown', '', None] and tipo_nuevo != 'unknown':
                item['tipo'] = tipo_nuevo
                stats['clasificados'] += 1
            
            items.append(item)
            stats['mantenidos'] += 1
    
    print(f"\n📊 Estadísticas:")
    print(f"   Total items leídos: {stats['total']}")
    print(f"   Items eliminados (score <70): {stats['eliminados']}")
    print(f"   Items clasificados: {stats['clasificados']}")
    print(f"   Items mantenidos: {stats['mantenidos']}")
    
    # Guardar dataset limpio
    print(f"\n💾 Guardando dataset limpio...")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"\n✅ Dataset limpio guardado: {OUTPUT}")
    print(f"   Items finales: {len(items)}")
    print(f"   Reducción: {stats['eliminados']} items ({stats['eliminados']/stats['total']*100:.1f}%)")
    
    # Distribución de tipos
    from collections import Counter
    tipos = Counter(item.get('tipo', 'unknown') for item in items)
    print(f"\n📋 Distribución de tipos:")
    for tipo, count in tipos.most_common(15):
        print(f"   {tipo}: {count} ({count/len(items)*100:.1f}%)")
    
    print("\n" + "="*70)
    print("✅ FASE 1 COMPLETADA")
    print("="*70)

if __name__ == "__main__":
    main()
