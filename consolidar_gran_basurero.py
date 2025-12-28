#!/usr/bin/env python3
"""
Consolidador BRUTAL - Extrae TODO el contenido de TODOS los JSON/JSONL
sin filtros, sin deduplicación, sin validación.
"""
import json
import glob
import os
from pathlib import Path

OUTPUT = "/home/spas/OPOS_GEMINI_1/gran-basurero.jsonl"
TOTAL = 0
ERRORES = 0

def extraer_todo(filepath):
    """Extrae cualquier cosa que parezca datos de un archivo JSON/JSONL"""
    global TOTAL, ERRORES
    items = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return items
                
            # Intentar como JSON
            if filepath.endswith('.json'):
                try:
                    data = json.loads(content)
                    items.append({"source": filepath, "data": data})
                    TOTAL += 1
                except:
                    ERRORES += 1
                    
            # Intentar como JSONL
            else:
                for line in content.splitlines():
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        items.append({"source": filepath, "data": data})
                        TOTAL += 1
                    except:
                        ERRORES += 1
    except Exception as e:
        print(f"ERROR leyendo {filepath}: {e}")
        ERRORES += 1
        
    return items

def main():
    print("🗑️  INICIANDO CONSOLIDACIÓN BRUTAL - GRAN BASURERO")
    
    all_items = []
    
    # 1. dataset_generator
    print("\n📦 Procesando dataset_generator...")
    paths = [
        "/home/spas/OPOS_GEMINI_1/dataset_generator/**/*.json",
        "/home/spas/OPOS_GEMINI_1/dataset_generator/**/*.jsonl"
    ]
    for pattern in paths:
        for f in glob.glob(pattern, recursive=True):
            items = extraer_todo(f)
            all_items.extend(items)
            if items:
                print(f"  ✓ {len(items)} de {os.path.basename(f)}")
    
    # 2. golden_dataset
    print("\n💎 Procesando golden_dataset...")
    paths = [
        "/home/spas/OPOS_GEMINI_1/golden_dataset/**/*.json",
        "/home/spas/OPOS_GEMINI_1/golden_dataset/**/*.jsonl"
    ]
    for pattern in paths:
        for f in glob.glob(pattern, recursive=True):
            items = extraer_todo(f)
            all_items.extend(items)
            if items:
                print(f"  ✓ {len(items)} de {os.path.basename(f)}")
    
    # 3. Raíz del proyecto (archivos sueltos)
    print("\n🏠 Procesando raíz del proyecto...")
    for f in glob.glob("/home/spas/OPOS_GEMINI_1/*.json") + glob.glob("/home/spas/OPOS_GEMINI_1/*.jsonl"):
        items = extraer_todo(f)
        all_items.extend(items)
        if items:
            print(f"  ✓ {len(items)} de {os.path.basename(f)}")
    
    # 4. gastos_tokens
    print("\n💰 Procesando gastos_tokens...")
    for f in glob.glob("/home/spas/OPOS_GEMINI_1/gastos_ tokens/*.json*"):
        items = extraer_todo(f)
        all_items.extend(items)
        if items:
            print(f"  ✓ {len(items)} de {os.path.basename(f)}")
    
    # ESCRIBIR TODO
    print(f"\n💾 Escribiendo {len(all_items)} items a {OUTPUT}...")
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        for item in all_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"\n✅ COMPLETADO")
    print(f"   Total items: {TOTAL}")
    print(f"   Errores: {ERRORES}")
    print(f"   Archivo: {OUTPUT}")

if __name__ == "__main__":
    main()
