#!/usr/bin/env python3
"""
DETECTAR LEYES FALTANTES
Compara las leyes del temario oficial con las indexadas en Qdrant Cloud
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from collections import Counter

# Cargar variables de entorno
env_path = Path(__file__).parent / 'backend' / '.env.backend'
load_dotenv(env_path)

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print("="*80)
print("🔍 DETECCIÓN DE LEYES FALTANTES")
print("="*80)

# Leyes esperadas según el temario oficial
LEYES_ESPERADAS = {
    # CRÍTICAS (5)
    "LGSS": {"nombre": "RDL 8/2015 - Ley General Seguridad Social", "prioridad": "🔴", "chunks_min": 400},
    "RD_84_1996": {"nombre": "RD 84/1996 - Afiliación", "prioridad": "🔴", "chunks_min": 50},
    "RD_2064_1995": {"nombre": "RD 2064/1995 - Cotización", "prioridad": "🔴", "chunks_min": 50},
    "RD_1415_2004": {"nombre": "RD 1415/2004 - Recaudación", "prioridad": "🔴", "chunks_min": 50},
    "Constitucion": {"nombre": "Constitución Española 1978", "prioridad": "🔴", "chunks_min": 40},
    
    # ALTAS (5)
    "Ley_39_2015": {"nombre": "Ley 39/2015 - Procedimiento Administrativo", "prioridad": "🟠", "chunks_min": 100},
    "Ley_40_2015": {"nombre": "Ley 40/2015 - Régimen Jurídico", "prioridad": "🟠", "chunks_min": 150},
    "RDL_5_2015_EBEP": {"nombre": "RDL 5/2015 - EBEP", "prioridad": "🟠", "chunks_min": 80},
    "RD_1430_2009": {"nombre": "RD 1430/2009 - Incapacidad Temporal", "prioridad": "🟠", "chunks_min": 10},
    "RD_1300_1995": {"nombre": "RD 1300/1995 - Incapacidad Permanente", "prioridad": "🟠", "chunks_min": 10},
    
    # MEDIAS (3)
    "Ley_19_2021_IMV": {"nombre": "Ley 19/2021 - IMV", "prioridad": "🟡", "chunks_min": 15},
    "LO_3_2018_LOPDGDD": {"nombre": "LO 3/2018 - Protección de Datos", "prioridad": "🟡", "chunks_min": 100},
    "Ley_39_2006_Dependencia": {"nombre": "Ley 39/2006 - Dependencia", "prioridad": "🟡", "chunks_min": 40}
}

# Conectar a Qdrant
print(f"\n🔌 Conectando a Qdrant Cloud...")
try:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print(f"✅ Conectado")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Obtener todas las normas indexadas
print(f"\n📊 Analizando leyes indexadas...")
try:
    # Obtener muestra grande para análisis
    scroll_result = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=10000,
        with_payload=True,
        with_vectors=False
    )
    
    total_puntos = len(scroll_result[0])
    print(f"✅ Analizados {total_puntos:,} puntos")
    
    # Contar por norma
    normas_counter = Counter()
    for point in scroll_result[0]:
        norma = point.payload.get('norma', 'N/A')
        normas_counter[norma] += 1
    
except Exception as e:
    print(f"❌ Error obteniendo datos: {e}")
    exit(1)

# Analizar resultados
print(f"\n{'='*80}")
print(f"📋 ANÁLISIS DE LEYES")
print(f"{'='*80}")

leyes_ok = []
leyes_incompletas = []
leyes_faltantes = []

for norma_id, info in LEYES_ESPERADAS.items():
    chunks_actuales = normas_counter.get(norma_id, 0)
    chunks_min = info['chunks_min']
    prioridad = info['prioridad']
    nombre = info['nombre']
    
    if chunks_actuales == 0:
        leyes_faltantes.append({
            'id': norma_id,
            'nombre': nombre,
            'prioridad': prioridad,
            'chunks': 0,
            'esperados': chunks_min
        })
    elif chunks_actuales < chunks_min:
        leyes_incompletas.append({
            'id': norma_id,
            'nombre': nombre,
            'prioridad': prioridad,
            'chunks': chunks_actuales,
            'esperados': chunks_min,
            'porcentaje': (chunks_actuales / chunks_min) * 100
        })
    else:
        leyes_ok.append({
            'id': norma_id,
            'nombre': nombre,
            'prioridad': prioridad,
            'chunks': chunks_actuales
        })

# Mostrar resultados
print(f"\n✅ LEYES COMPLETAS ({len(leyes_ok)}/{len(LEYES_ESPERADAS)})")
print(f"{'-'*80}")
for ley in sorted(leyes_ok, key=lambda x: x['chunks'], reverse=True):
    print(f"{ley['prioridad']} {ley['nombre']:50} {ley['chunks']:4} chunks")

if leyes_incompletas:
    print(f"\n⚠️  LEYES INCOMPLETAS ({len(leyes_incompletas)})")
    print(f"{'-'*80}")
    for ley in sorted(leyes_incompletas, key=lambda x: x['porcentaje']):
        print(f"{ley['prioridad']} {ley['nombre']:50} {ley['chunks']:4}/{ley['esperados']:4} chunks ({ley['porcentaje']:.0f}%)")

if leyes_faltantes:
    print(f"\n❌ LEYES FALTANTES ({len(leyes_faltantes)})")
    print(f"{'-'*80}")
    for ley in leyes_faltantes:
        print(f"{ley['prioridad']} {ley['nombre']:50} 0 chunks (FALTA)")

# Leyes no esperadas
leyes_extra = []
for norma, count in normas_counter.items():
    if norma not in LEYES_ESPERADAS and norma != 'N/A':
        leyes_extra.append({'norma': norma, 'chunks': count})

if leyes_extra:
    print(f"\n📌 LEYES ADICIONALES ({len(leyes_extra)})")
    print(f"{'-'*80}")
    for ley in sorted(leyes_extra, key=lambda x: x['chunks'], reverse=True):
        print(f"   {ley['norma']:50} {ley['chunks']:4} chunks")

# Resumen
print(f"\n{'='*80}")
print(f"📊 RESUMEN")
print(f"{'='*80}")
print(f"   Total leyes esperadas: {len(LEYES_ESPERADAS)}")
print(f"   ✅ Completas: {len(leyes_ok)}")
print(f"   ⚠️  Incompletas: {len(leyes_incompletas)}")
print(f"   ❌ Faltantes: {len(leyes_faltantes)}")
print(f"   📌 Adicionales: {len(leyes_extra)}")
print(f"   📈 Cobertura: {(len(leyes_ok) / len(LEYES_ESPERADAS)) * 100:.1f}%")

# Recomendaciones
if leyes_faltantes or leyes_incompletas:
    print(f"\n{'='*80}")
    print(f"💡 RECOMENDACIONES")
    print(f"{'='*80}")
    
    if leyes_faltantes:
        print(f"\n🔴 URGENTE - Indexar leyes faltantes:")
        for ley in leyes_faltantes:
            print(f"   {ley['prioridad']} {ley['id']}")
    
    if leyes_incompletas:
        print(f"\n⚠️  IMPORTANTE - Re-indexar leyes incompletas:")
        for ley in sorted(leyes_incompletas, key=lambda x: x['porcentaje'])[:3]:
            print(f"   {ley['prioridad']} {ley['id']} ({ley['porcentaje']:.0f}% completa)")
    
    print(f"\n📝 Comandos sugeridos:")
    if leyes_faltantes or leyes_incompletas:
        print(f"   wsl bash -c \"cd backend && source venv/bin/activate && python agents/indexar_todas_las_leyes.py\"")
else:
    print(f"\n🎉 ¡PERFECTO! Todas las leyes están indexadas correctamente")

print(f"\n{'='*80}")
