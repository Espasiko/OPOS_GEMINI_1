#!/usr/bin/env python3
"""
Verificar 100% del dataset golden_dataset_consolidated_20251221.jsonl
NO crear nuevos archivos. MODIFICAR el existente.
"""

import json
import requests
from pathlib import Path
import re

DATASET = Path("golden_dataset/consolidated/golden_dataset_consolidated_20251221.jsonl")
BACKEND = "http://127.0.0.1:8000"

def extraer_articulos(texto):
    """Extraer menciones de artículos del texto"""
    if not texto:
        return []
    
    # Patrones: Art. 215, Artículo 215, art 215
    patrones = [
        r'Art\.\s*(\d+)',
        r'Artículo\s*(\d+)',
        r'art\s+(\d+)',
    ]
    
    articulos = []
    for patron in patrones:
        matches = re.findall(patron, texto, re.IGNORECASE)
        articulos.extend(matches)
    
    return list(set(articulos))[:3]  # Max 3 artículos

def verificar_item(item, index):
    """Verificar un item y añadir URL BOE si falta"""
    
    # Si ya tiene URL BOE válida, skip
    url_actual = item.get('url_boe', '')
    if url_actual and url_actual not in ['', 'N/A', None]:
        return item, 'ya_verificado'
    
    # Extraer artículos de la explicación
    explicacion = item.get('explicacion', '')
    articulos_ref = item.get('articulos_referencia', [])
    
    # Intentar extraer artículos del texto
    articulos_texto = extraer_articulos(explicacion)
    
    # Si no hay artículos, marcar como no_verificable
    if not articulos_ref and not articulos_texto:
        item['url_boe'] = 'NO_VERIFICABLE'
        item['verificado'] = False
        return item, 'no_verificable'
    
    # Construir query para RAG
    if articulos_texto:
        query = f"artículo {articulos_texto[0]} LGSS {explicacion[:100]}"
    elif articulos_ref:
        query = f"{articulos_ref[0]} {explicacion[:100]}"
    else:
        query = explicacion[:200]
    
    try:
        response = requests.post(
            f"{BACKEND}/api/rag/search",
            json={"query": query, "top_k": 3, "min_score": 0.3},
            timeout=10
        )
        
        if response.status_code == 200:
            docs = response.json().get('documents', [])
            
            if docs:
                # Tomar la URL del primer resultado
                url_boe = docs[0]['metadata'].get('url', '')
                if url_boe and url_boe != 'N/A':
                    item['url_boe'] = url_boe
                    item['verificado'] = True
                    print(f"  ✅ {index}: Verificado - {url_boe[:50]}...")
                    return item, 'verificado_ahora'
    
    except Exception as e:
        print(f"  ❌ {index}: Error - {str(e)[:50]}")
    
    # Si falla, marcar como pendiente
    item['url_boe'] = 'PENDIENTE_MANUAL'
    item['verificado'] = False
    return item, 'pendiente'

def main():
    print("="*70)
    print("🔍 VERIFICANDO 100% DEL DATASET")
    print("="*70)
    print(f"📁 Archivo: {DATASET}")
    print(f"🌐 Backend: {BACKEND}")
    
    # Verificar backend
    try:
        response = requests.get(f"{BACKEND}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Backend funcionando")
        else:
            print(f"❌ Backend no responde correctamente")
            return
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        print("   Asegúrate de que el backend está corriendo en http://localhost:8000")
        return
    
    items = []
    stats = {
        'ya_verificado': 0,
        'verificado_ahora': 0,
        'no_verificable': 0,
        'pendiente': 0
    }
    
    total_items = 0
    
    # Leer dataset
    print("\n📖 Leyendo dataset...")
    with open(DATASET, 'r', encoding='utf-8') as f:
        for line in f:
            total_items += 1
    
    print(f"Total items: {total_items}")
    print("\n🔄 Verificando items...")
    print("   (Esto puede tardar 30-60 minutos)\n")
    
    with open(DATASET, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            item = json.loads(line)
            item_verificado, status = verificar_item(item, i)
            items.append(item_verificado)
            stats[status] += 1
            
            if i % 100 == 0:
                print(f"\n📊 Progreso: {i}/{total_items}")
                print(f"   Ya verificados: {stats['ya_verificado']}")
                print(f"   Verificados ahora: {stats['verificado_ahora']}")
                print(f"   No verificables: {stats['no_verificable']}")
                print(f"   Pendientes: {stats['pendiente']}")
    
    # SOBRESCRIBIR archivo original
    print(f"\n💾 Guardando cambios en {DATASET}...")
    with open(DATASET, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print("\n" + "="*70)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("="*70)
    print(f"Ya verificados:    {stats['ya_verificado']:>6} ({stats['ya_verificado']/total_items*100:>5.1f}%)")
    print(f"Verificados ahora: {stats['verificado_ahora']:>6} ({stats['verificado_ahora']/total_items*100:>5.1f}%)")
    print(f"No verificables:   {stats['no_verificable']:>6} ({stats['no_verificable']/total_items*100:>5.1f}%)")
    print(f"Pendientes manual: {stats['pendiente']:>6} ({stats['pendiente']/total_items*100:>5.1f}%)")
    print("-"*70)
    
    total_verificados = stats['ya_verificado'] + stats['verificado_ahora']
    porcentaje = (total_verificados / total_items) * 100
    print(f"📊 TOTAL VERIFICADO: {total_verificados}/{total_items} ({porcentaje:.1f}%)")
    print("="*70)

if __name__ == "__main__":
    main()
