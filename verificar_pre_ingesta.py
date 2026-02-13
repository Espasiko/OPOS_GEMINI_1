#!/usr/bin/env python3
"""
VERIFICACIÓN FINAL PRE-INGESTA
Comprueba que el script de ingesta está listo para ejecutar 8 horas
"""

import sys
import os
from pathlib import Path

print("=" * 80)
print("🔍 VERIFICACIÓN FINAL PRE-INGESTA")
print("=" * 80)

errors = []
warnings = []

# 1. Verificar vocabulario BM25
print("\n1️⃣ Verificando vocabulario BM25...")
bm25_path = Path("/home/spas/OPOS_GEMINI_1/backend/data/bm25_vocab.pkl")
if not bm25_path.exists():
    errors.append("❌ Vocabulario BM25 NO existe")
else:
    import pickle
    with open(bm25_path, 'rb') as f:
        bm25_data = pickle.load(f)
    
    if isinstance(bm25_data, dict) and 'vocab' in bm25_data:
        vocab = bm25_data['vocab']
        print(f"   ✅ Vocabulario BM25 cargado: {len(vocab)} términos")
        if len(vocab) < 10000:
            warnings.append(f"⚠️  Vocabulario pequeño: {len(vocab)} términos")
    else:
        errors.append("❌ Formato de vocabulario BM25 incorrecto")

# 2. Verificar archivos XML
print("\n2️⃣ Verificando archivos XML...")
xml_dir = Path("/home/spas/OPOS_GEMINI_1/data/boe_xml")
if not xml_dir.exists():
    errors.append("❌ Directorio XML NO existe")
else:
    xml_files = list(xml_dir.glob("*.json"))
    print(f"   ✅ {len(xml_files)} archivos XML encontrados")
    if len(xml_files) < 50:
        warnings.append(f"⚠️  Menos de 50 leyes: {len(xml_files)}")

# 3. Verificar Qdrant
print("\n3️⃣ Verificando Qdrant...")
try:
    from qdrant_client import QdrantClient
    client = QdrantClient(url="http://localhost:6333", timeout=10)
    collections = [c.name for c in client.get_collections().collections]
    print(f"   ✅ Qdrant conectado: {len(collections)} colecciones")
except Exception as e:
    errors.append(f"❌ Qdrant NO accesible: {e}")

# 4. Verificar modelo embeddings
print("\n4️⃣ Verificando modelo embeddings...")
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
    test_vec = model.encode("test")
    if len(test_vec) == 1024:
        print(f"   ✅ Modelo embeddings cargado: {len(test_vec)} dim")
    else:
        errors.append(f"❌ Dimensión incorrecta: {len(test_vec)} (esperado 1024)")
except Exception as e:
    errors.append(f"❌ Modelo embeddings NO cargable: {e}")

# 5. Verificar script de ingesta
print("\n5️⃣ Verificando script de ingesta...")
script_path = Path("/home/spas/OPOS_GEMINI_1/backend/scripts/reingest_qdrant_DIRECT_XML.py")
if not script_path.exists():
    errors.append("❌ Script de ingesta NO existe")
else:
    with open(script_path, 'r') as f:
        script_content = f.read()
    
    # Verificar correcciones críticas
    checks = {
        "BATCH_SIZE = 50": "Batches de 50 chunks",
        "wait=True": "Confirmación por batch",
        "timeout=300": "Timeout de 300s",
        "bm25_data['vocab']": "Extracción correcta de vocabulario BM25",
        "SparseVector(indices=indices, values=values)": "Sparse vectors correctos"
    }
    
    for check, desc in checks.items():
        if check in script_content:
            print(f"   ✅ {desc}")
        else:
            errors.append(f"❌ {desc} NO encontrado")

# 6. Estimaciones
print("\n6️⃣ Estimaciones de ingesta...")
if xml_files:
    total_leyes = len(xml_files)
    chunks_por_ley = 1272  # Promedio de LGSS
    total_chunks_estimado = total_leyes * chunks_por_ley
    batches_estimados = (total_chunks_estimado + 49) // 50
    tiempo_por_batch = 10  # segundos
    tiempo_total_horas = (batches_estimados * tiempo_por_batch) / 3600
    
    print(f"   📊 Leyes: {total_leyes}")
    print(f"   📊 Chunks estimados: ~{total_chunks_estimado:,}")
    print(f"   📊 Batches: ~{batches_estimados:,}")
    print(f"   📊 Tiempo estimado: ~{tiempo_total_horas:.1f} horas")

# RESUMEN
print("\n" + "=" * 80)
if errors:
    print("❌ ERRORES CRÍTICOS ENCONTRADOS:")
    for error in errors:
        print(f"   {error}")
    print("\n⛔ NO EJECUTAR INGESTA - Resolver errores primero")
    sys.exit(1)
elif warnings:
    print("⚠️  ADVERTENCIAS:")
    for warning in warnings:
        print(f"   {warning}")
    print("\n✅ Script listo, pero revisar advertencias")
else:
    print("✅ TODAS LAS VERIFICACIONES PASADAS")
    print("✅ Script listo para ingesta completa")

print("=" * 80)
