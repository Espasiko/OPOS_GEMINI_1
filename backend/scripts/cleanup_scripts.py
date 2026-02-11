#!/usr/bin/env python3
"""
LIMPIEZA SCRIPTS BASURA
Elimina scripts fallidos/no usados creados HOY
"""

from pathlib import Path
import os

SCRIPTS_DIR = Path("/home/spas/OPOS_GEMINI_1/backend/scripts")

# Scripts a MANTENER (válidos y en uso)
KEEP = {
    "ingest_full_db_MAXIMUM.py",  # ✅ Ingesta principal
    "ingest_leyes_extra_UE_CC.py",  # ✅ Ingesta UE/CC (ejecutado OK)
    "salamandra_ULTRA_prototype.py",  # ✅ Nuevo sistema completo
    "06_01_26_salamandra_FINAL.py",  # ✅ Script base funcionando
    "verify_enero_25_pairing.py",  # ✅ Verificación exámenes
    "05_01_26_parse_questions.py",  # ✅ Parser preguntas
}

# Scripts a BORRAR (basura/fallidos/obsoletos)
DELETE = {
    "test_salamandra_accuracy_REAL.py",  # ❌ Obsoleto, sustituido por ULTRA
    "test_salamandra_accuracy_SIMPLE.py",  # ❌ Obsoleto
    "test_salamandra_accuracy_FINAL.py",  # ❌ Obsoleto
    "find_answer_key_file.py",  # ❌ Temporal, ya cumplió función
    "select_20_for_verification.py",  # ❌ Temporal
    "analyze_salamandra_deep.py",  # ❌ Análisis temporal
    "evaluate_salamandra_10_difficult.py",  # ❌ Temporal
    "evaluate_salamandra_5_CORRECTO.py",  # ❌ Temporal
}

print("=" * 70)
print("LIMPIEZA SCRIPTS BASURA")
print("=" * 70)

print("\n✅ MANTENER (scripts válidos):")
for s in sorted(KEEP):
    path = SCRIPTS_DIR / s
    if path.exists():
        size = path.stat().st_size
        print(f"   ✅ {s} ({size:,} bytes)")

print("\n❌ ELIMINAR (basura/obsoletos):")
deleted = 0
for s in sorted(DELETE):
    path = SCRIPTS_DIR / s
    if path.exists():
        size = path.stat().st_size
        print(f"   🗑️  {s} ({size:,} bytes)")
        try:
            path.unlink()
            deleted += 1
            print(f"       ✅ Eliminado")
        except Exception as e:
            print(f"       ❌ Error: {e}")
    else:
        print(f"   ⚠️  {s} (no existe)")

print("\n" + "=" * 70)
print(f"RESUMEN: {deleted} archivos eliminados")
print("=" * 70)
