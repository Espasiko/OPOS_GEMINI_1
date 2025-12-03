#!/usr/bin/env python3
"""
Script para preparar materiales de oposiciones C1 SS/AGE para indexación RAG
Copia archivos relevantes desde elemplos_leyes_info a backend/data/materiales_opos
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple

# Rutas
BASE_DIR = Path(__file__).parent.parent
SOURCE_DIR = BASE_DIR.parent / "elemplos_leyes_info" / "de_mi_hija"
TARGET_DIR = BASE_DIR / "data" / "materiales_opos"

# Crear directorios de destino
CATEGORIES = {
    "examenes": TARGET_DIR / "examenes_oficiales_c1_ss",
    "tests": TARGET_DIR / "tests_age",
    "temarios": TARGET_DIR / "temarios_ss_age",
    "esquemas": TARGET_DIR / "esquemas",
}

for cat_dir in CATEGORIES.values():
    cat_dir.mkdir(parents=True, exist_ok=True)


# Patrones de archivos relevantes
PATTERNS = {
    "examenes": [
        "*examen_c1_ss*.pdf",
        "*examen_c1_*202*.pdf",
        "*examen_c1_pi*.pdf",
        "*examen_c1_extraord*.pdf",
        "*respuestas_examen*.pdf",
        "*caso_monografico*.pdf",
    ],
    "tests": [
        "Test_Admtvos_AGE*.pdf",
    ],
    "temarios": [
        "Temario*_Administrativos_Acceso_Libre_AGE.pdf",
        "SS Temario Unificado*.pdf",
        "*Muestra-Temario-C1*.pdf",
    ],
    "esquemas": [
        "PAC esquemas*.pdf",
        "ESQUEMAS/*",
    ],
}

# Archivos a EXCLUIR (facturas, tickets, listas de nombres, etc.)
EXCLUDE_PATTERNS = [
    "*factura*",
    "*ticket*",
    "*pago*",
    "*lista*",
    "*ListadoAdmitidos*",
    "*Alegaciones*",
    "*.jpg",
    "*.JPG",
    "*.docx",
    "*.rtf",
]


def should_exclude(file_path: Path) -> bool:
    """Verifica si un archivo debe ser excluido"""
    name_lower = file_path.name.lower()
    for pattern in EXCLUDE_PATTERNS:
        if file_path.match(pattern):
            return True
    return False


def find_files(source_dir: Path, patterns: List[str]) -> List[Path]:
    """Encuentra archivos que coincidan con los patrones"""
    found_files = []
    for pattern in patterns:
        # Buscar recursivamente
        matches = list(source_dir.rglob(pattern))
        found_files.extend(matches)
    
    # Filtrar excluidos y duplicados
    unique_files = []
    seen_names = set()
    
    for f in found_files:
        if f.is_file() and not should_exclude(f):
            # Evitar duplicados por nombre
            if f.name not in seen_names:
                unique_files.append(f)
                seen_names.add(f.name)
    
    return sorted(unique_files)


def copy_file(source: Path, dest_dir: Path) -> Tuple[bool, str]:
    """Copia un archivo al directorio de destino"""
    try:
        dest_file = dest_dir / source.name
        
        if dest_file.exists():
            # Verificar si son iguales
            if dest_file.stat().st_size == source.stat().st_size:
                return True, "Ya existe (mismo tamaño)"
        
        shutil.copy2(source, dest_file)
        size_mb = dest_file.stat().st_size / (1024 * 1024)
        return True, f"Copiado ({size_mb:.2f} MB)"
        
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    print("=" * 80)
    print("📚 PREPARACIÓN DE MATERIALES DE OPOSICIONES - C1 SS/AGE")
    print("=" * 80)
    print(f"\n📁 Origen: {SOURCE_DIR}")
    print(f"📁 Destino: {TARGET_DIR}\n")
    
    if not SOURCE_DIR.exists():
        print(f"❌ ERROR: No existe el directorio de origen: {SOURCE_DIR}")
        return 1
    
    total_copied = 0
    total_found = 0
    
    for category, patterns in PATTERNS.items():
        print(f"\n{'═' * 80}")
        print(f"📂 Categoría: {category.upper()}")
        print(f"{'═' * 80}")
        
        files = find_files(SOURCE_DIR, patterns)
        total_found += len(files)
        
        if not files:
            print(f"  ⚠️  No se encontraron archivos para esta categoría")
            continue
        
        print(f"  ✅ Encontrados: {len(files)} archivos\n")
        
        dest_dir = CATEGORIES[category]
        category_copied = 0
        
        for file_path in files:
            # Mostrar ruta relativa para mayor claridad
            rel_path = file_path.relative_to(SOURCE_DIR)
            
            success, msg = copy_file(file_path, dest_dir)
            icon = "✅" if success else "❌"
            
            print(f"  {icon} {file_path.name}")
            print(f"      {rel_path.parent}")
            print(f"      → {msg}")
            
            if success and "Copiado" in msg:
                category_copied += 1
                total_copied += 1
        
        print(f"\n  📊 Copiados en {category}: {category_copied}/{len(files)}")
    
    # Resumen final
    print("\n" + "=" * 80)
    print("📊 RESUMEN FINAL")
    print("=" * 80)
    print(f"✅ Archivos encontrados: {total_found}")
    print(f"📥 Archivos copiados: {total_copied}")
    print(f"\n📁 Estructura creada:")
    
    for cat_name, cat_dir in CATEGORIES.items():
        file_count = len(list(cat_dir.glob("*.pdf")))
        print(f"   {cat_dir.name}/  ({file_count} archivos)")
    
    print(f"\n💾 Todos los materiales en: {TARGET_DIR}")
    print("=" * 80)
    
    print("\n🚀 PRÓXIMOS PASOS:")
    print("   1. Revisar archivos copiados")
    print("   2. Ejecutar script de indexación RAG")
    print("   3. Embeddings → Qdrant local")
    print("   4. Testear búsquedas con nuevo contenido")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
