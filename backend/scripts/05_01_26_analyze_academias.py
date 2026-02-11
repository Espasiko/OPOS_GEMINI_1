#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT: 05_01_26_analyze_academias.py
PROPÓSITO: Inventariar, deduplicar y clasificar carpeta 'academias'.
"""

import os
import hashlib
import json
import logging
from pathlib import Path
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path("/home/spas/OPOS_GEMINI_1/academias")
OUTPUT_JSON = Path("/home/spas/OPOS_GEMINI_1/staging_area/academias_inventory.json")
OUTPUT_MD = Path("/home/spas/OPOS_GEMINI_1/staging_area/academias_inventory.md")

# Asegurar dir
OUTPUT_JSON.parent.mkdir(exist_ok=True, parents=True)

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logger.error(f"Error hash {file_path}: {e}")
        return None

def classify_file(filename):
    lower = filename.lower()
    if any(x in lower for x in ['test', 'cuestionario', 'examen', 'preguntas']):
        return "test"
    if any(x in lower for x in ['simulacro']):
        return "simulacro"
    if any(x in lower for x in ['tema ', 'temario', 'bloque']):
        return "temario"
    if any(x in lower for x in ['esquema', 'resumen', 'cuadro', 'tabla']):
        return "esquema"
    if any(x in lower for x in ['caso', 'supuesto', 'practico']):
        return "caso_practico"
    return "otros"

def main():
    logger.info(f"📂 Iniciando escaneo en: {BASE_DIR}")
    
    if not BASE_DIR.exists():
        logger.error("❌ Carpeta academias no existe.")
        return

    inventory = []
    seen_hashes = {}
    duplicates = []
    
    # Walk con limite de profundidad manual si fuera necesario, pero os.walk es recursivo total.
    # El usuario pidio "hasta 6 niveles".
    base_depth = str(BASE_DIR).count(os.sep)
    
    for root, dirs, files in os.walk(BASE_DIR):
        current_depth = str(root).count(os.sep) - base_depth
        if current_depth > 6: continue
        
        for file in files:
            file_path = Path(root) / file
            
            # Skip hidden and Zone.Identifier (just in case)
            if file.startswith('.') or "Zone.Identifier" in file: continue
            
            file_hash = calculate_md5(file_path)
            
            is_duplicate = False
            original_path = None
            
            if file_hash in seen_hashes:
                is_duplicate = True
                original_path = seen_hashes[file_hash]
                duplicates.append((str(file_path), original_path))
            else:
                seen_hashes[file_hash] = str(file_path)
            
            item = {
                "filename": file,
                "path": str(file_path),
                "rel_path": str(file_path.relative_to(BASE_DIR)),
                "size_bytes": file_path.stat().st_size,
                "type": classify_file(file),
                "md5": file_hash,
                "is_duplicate": is_duplicate,
                "duplicate_of": original_path
            }
            inventory.append(item)

    # Guardar JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)
        
    # Generar MD
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("# 📚 Inventario Carpeta Academias\n\n")
        
        # Resumen
        total = len(inventory)
        dupes = len(duplicates)
        unique = total - dupes
        
        f.write(f"**Total Archivos:** {total}\n")
        f.write(f"**Únicos:** {unique}\n")
        f.write(f"**Duplicados:** {dupes}\n\n")
        
        # Por Tipo
        by_type = defaultdict(list)
        for i in inventory:
            if not i['is_duplicate']:
                by_type[i['type']].append(i)
                
        f.write("## 📊 Distribución por Tipo (Únicos)\n")
        for t, items in by_type.items():
            f.write(f"- **{t.upper()}**: {len(items)}\n")
            
        f.write("\n## ⚠️ Duplicados Detectados\n")
        for dup, orig in duplicates:
            f.write(f"- `{Path(dup).name}` -> es copia de `{Path(orig).name}`\n")
            
        f.write("\n## 📜 Lista Completa de Archivos Únicos\n")
        for i in inventory:
            if not i['is_duplicate']:
                f.write(f"- `{i['filename']}` ({i['type']}) - {i['rel_path']}\n")

    logger.info(f"✅ Inventario generado: {OUTPUT_MD}")
    logger.info(f"   Total: {total} | Duplicados: {dupes}")

if __name__ == "__main__":
    main()
