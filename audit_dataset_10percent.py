#!/usr/bin/env python3
"""
Auditoría exhaustiva del 10% del dataset según mejores prácticas de fine-tuning diciembre 2025
"""

import json
import requests
import re
from collections import Counter
from pathlib import Path

SAMPLE = "dataset_sample_10percent.jsonl"
BACKEND = "http://127.0.0.1:8000"

# Mejores prácticas de fine-tuning diciembre 2025
BEST_PRACTICES = {
    "min_quality_score": 90,  # Score mínimo de calidad
    "require_citations": True,  # Requiere citas legales
    "require_urls": False,  # URLs opcionales (muchos items conceptuales)
    "max_hallucination_rate": 0.05,  # Máximo 5% de alucinaciones
    "min_diversity": 0.7,  # Diversidad mínima de temas
    "require_balanced_types": True,  # Tipos de contenido balanceados
}

def audit_item(item, index):
    """Auditar un item individual"""
    issues = []
    score = 100
    
    # 1. Verificar estructura básica
    required_fields = ['pregunta', 'explicacion']
    for field in required_fields:
        if field not in item or not item[field]:
            issues.append(f"Falta campo '{field}'")
            score -= 20
    
    # 2. Verificar calidad de explicación
    explicacion = item.get('explicacion', '')
    if len(explicacion) < 50:
        issues.append("Explicación muy corta (<50 chars)")
        score -= 10
    
    # 3. Verificar citas legales
    articulos = extract_articulos(explicacion)
    if not articulos and BEST_PRACTICES['require_citations']:
        issues.append("Sin citas legales en explicación")
        score -= 15
    
    # 4. Verificar URL BOE
    url_boe = item.get('url_boe', '')
    if url_boe in ['', 'N/A', None, 'NO_VERIFICABLE', 'PENDIENTE_MANUAL']:
        if BEST_PRACTICES['require_urls']:
            issues.append("Sin URL BOE verificada")
            score -= 10
    else:
        # Verificar que URL es válida
        if not url_boe.startswith('http'):
            issues.append(f"URL BOE inválida: {url_boe[:50]}")
            score -= 15
    
    # 5. Detectar posibles alucinaciones
    if 'artículos_referencia' in item:
        refs = item['articulos_referencia']
        if refs and isinstance(refs, list):
            # Verificar que las referencias mencionadas están en la explicación
            for ref in refs:
                if str(ref) not in explicacion:
                    issues.append(f"Referencia '{ref}' no aparece en explicación")
                    score -= 5
    
    # 6. Verificar diversidad de opciones (si es tipo test)
    if 'opciones' in item:
        opciones = item.get('opciones', [])
        if isinstance(opciones, list) and len(opciones) < 4:
            issues.append(f"Pocas opciones ({len(opciones)} < 4)")
            score -= 10
    
    # 7. Verificar respuesta correcta
    if 'respuesta_correcta' in item:
        if not item['respuesta_correcta']:
            issues.append("Sin respuesta correcta")
            score -= 20
    
    return {
        'index': index,
        'score': max(0, score),
        'issues': issues,
        'has_citations': len(articulos) > 0,
        'has_url': url_boe not in ['', 'N/A', None, 'NO_VERIFICABLE', 'PENDIENTE_MANUAL'],
        'tipo': item.get('tipo', 'unknown')
    }

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
    print("🔍 AUDITORÍA DE CALIDAD DEL DATASET (10% MUESTRA)")
    print("="*70)
    print(f"📁 Archivo: {SAMPLE}")
    print(f"\n📋 Mejores Prácticas Diciembre 2025:")
    for key, value in BEST_PRACTICES.items():
        print(f"   - {key}: {value}")
    
    items = []
    with open(SAMPLE, 'r', encoding='utf-8') as f:
        for line in f:
            items.append(json.loads(line))
    
    print(f"\n📊 Auditando {len(items)} items...")
    
    results = []
    for i, item in enumerate(items, 1):
        result = audit_item(item, i)
        results.append(result)
        
        if i % 50 == 0:
            print(f"   Progreso: {i}/{len(items)}")
    
    # Análisis de resultados
    print("\n" + "="*70)
    print("📊 RESULTADOS DE AUDITORÍA")
    print("="*70)
    
    scores = [r['score'] for r in results]
    avg_score = sum(scores) / len(scores)
    
    print(f"\n🎯 Score Promedio: {avg_score:.1f}/100")
    
    # Distribución de scores
    excellent = sum(1 for s in scores if s >= 90)
    good = sum(1 for s in scores if 70 <= s < 90)
    poor = sum(1 for s in scores if s < 70)
    
    print(f"\nDistribución de Calidad:")
    print(f"   Excelente (90-100): {excellent} ({excellent/len(scores)*100:.1f}%)")
    print(f"   Buena (70-89):      {good} ({good/len(scores)*100:.1f}%)")
    print(f"   Pobre (<70):        {poor} ({poor/len(scores)*100:.1f}%)")
    
    # Citas y URLs
    with_citations = sum(1 for r in results if r['has_citations'])
    with_urls = sum(1 for r in results if r['has_url'])
    
    print(f"\n📚 Verificación:")
    print(f"   Con citas legales:  {with_citations} ({with_citations/len(results)*100:.1f}%)")
    print(f"   Con URLs BOE:       {with_urls} ({with_urls/len(results)*100:.1f}%)")
    
    # Tipos de contenido
    tipos = Counter(r['tipo'] for r in results)
    print(f"\n📋 Tipos de Contenido:")
    for tipo, count in tipos.most_common(10):
        print(f"   {tipo}: {count} ({count/len(results)*100:.1f}%)")
    
    # Problemas más comunes
    all_issues = []
    for r in results:
        all_issues.extend(r['issues'])
    
    if all_issues:
        issue_counts = Counter(all_issues)
        print(f"\n⚠️ Problemas Más Comunes:")
        for issue, count in issue_counts.most_common(10):
            print(f"   {issue}: {count} ({count/len(results)*100:.1f}%)")
    
    # Items con problemas graves
    critical_items = [r for r in results if r['score'] < 70]
    if critical_items:
        print(f"\n🚨 Items con Problemas Graves ({len(critical_items)}):")
        for item in critical_items[:5]:
            print(f"   Item {item['index']}: Score {item['score']}, Issues: {item['issues']}")
    
    # Evaluación final
    print("\n" + "="*70)
    print("✅ EVALUACIÓN FINAL")
    print("="*70)
    
    if avg_score >= 90:
        print("🟢 EXCELENTE: Dataset de alta calidad, listo para fine-tuning")
    elif avg_score >= 70:
        print("🟡 BUENO: Dataset aceptable, requiere mejoras menores")
    else:
        print("🔴 POBRE: Dataset requiere mejoras significativas antes de fine-tuning")
    
    print(f"\nRecomendaciones:")
    if with_citations / len(results) < 0.5:
        print("   ⚠️ Añadir más citas legales a las explicaciones")
    if with_urls / len(results) < 0.3:
        print("   ⚠️ Verificar y añadir URLs BOE a más items")
    if poor > len(results) * 0.1:
        print("   ⚠️ Revisar y mejorar items con score < 70")
    if len(tipos) < 5:
        print("   ⚠️ Aumentar diversidad de tipos de contenido")
    
    print("="*70)

if __name__ == "__main__":
    main()
