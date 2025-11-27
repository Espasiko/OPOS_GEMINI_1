#!/usr/bin/env python3
"""
VERIFICAR LEYES DEL TEMARIO OFICIAL
Compara las leyes mencionadas en el temario con las indexadas
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
print("🔍 VERIFICACIÓN LEYES DEL TEMARIO OFICIAL")
print("="*80)

# Leyes del temario oficial según el usuario
LEYES_TEMARIO_OFICIAL = {
    # BLOQUE GENERAL
    "Constitucion": {
        "nombre": "Constitución Española de 1978",
        "bloque": "General",
        "indexada": None
    },
    "Ley_39_2015": {
        "nombre": "Ley 39/2015 - Procedimiento Administrativo Común",
        "bloque": "General",
        "indexada": None
    },
    "Ley_40_2015": {
        "nombre": "Ley 40/2015 - Régimen Jurídico del Sector Público",
        "bloque": "General",
        "indexada": None
    },
    "LO_Poder_Judicial": {
        "nombre": "Ley Orgánica del Poder Judicial",
        "bloque": "General",
        "indexada": None
    },
    "LO_Tribunal_Constitucional": {
        "nombre": "Ley Orgánica del Tribunal Constitucional",
        "bloque": "General",
        "indexada": None
    },
    "LO_Regimen_Electoral": {
        "nombre": "Ley Orgánica del Régimen Electoral General",
        "bloque": "General",
        "indexada": None
    },
    
    # BLOQUE ESPECÍFICO (SEGURIDAD SOCIAL)
    "LGSS": {
        "nombre": "RDL 8/2015 - Ley General de la Seguridad Social",
        "bloque": "Seguridad Social",
        "indexada": None
    },
    "RD_1415_2004": {
        "nombre": "RD 1415/2004 - Reglamento General de Recaudación",
        "bloque": "Seguridad Social",
        "indexada": None
    },
    "Ley_34_2014": {
        "nombre": "Ley 34/2014 - Medidas en materia de liquidación e ingreso de cuotas",
        "bloque": "Seguridad Social",
        "indexada": None
    },
    "RD_84_1996": {
        "nombre": "RD 84/1996 - Afiliación, Altas y Bajas (implícito)",
        "bloque": "Seguridad Social",
        "indexada": None
    },
    "RD_2064_1995": {
        "nombre": "RD 2064/1995 - Cotización (implícito)",
        "bloque": "Seguridad Social",
        "indexada": None
    }
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
print(f"\n📊 Obteniendo leyes indexadas...")
try:
    scroll_result = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=10000,
        with_payload=True,
        with_vectors=False
    )
    
    # Contar por norma
    normas_counter = Counter()
    for point in scroll_result[0]:
        norma = point.payload.get('norma', 'N/A')
        normas_counter[norma] += 1
    
    print(f"✅ Analizadas {len(scroll_result[0]):,} puntos")
    print(f"   Normas únicas encontradas: {len(normas_counter)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Verificar cada ley del temario
print(f"\n{'='*80}")
print(f"📋 VERIFICACIÓN POR BLOQUE")
print(f"{'='*80}")

# Bloque General
print(f"\n📚 BLOQUE GENERAL")
print(f"{'-'*80}")
leyes_general = {k: v for k, v in LEYES_TEMARIO_OFICIAL.items() if v['bloque'] == 'General'}
for norma_id, info in leyes_general.items():
    chunks = normas_counter.get(norma_id, 0)
    if chunks > 0:
        print(f"✅ {info['nombre']:60} {chunks:4} chunks")
        info['indexada'] = True
    else:
        print(f"❌ {info['nombre']:60} NO INDEXADA")
        info['indexada'] = False

# Bloque Seguridad Social
print(f"\n📚 BLOQUE ESPECÍFICO (SEGURIDAD SOCIAL)")
print(f"{'-'*80}")
leyes_ss = {k: v for k, v in LEYES_TEMARIO_OFICIAL.items() if v['bloque'] == 'Seguridad Social'}
for norma_id, info in leyes_ss.items():
    chunks = normas_counter.get(norma_id, 0)
    if chunks > 0:
        print(f"✅ {info['nombre']:60} {chunks:4} chunks")
        info['indexada'] = True
    else:
        print(f"❌ {info['nombre']:60} NO INDEXADA")
        info['indexada'] = False

# Resumen
print(f"\n{'='*80}")
print(f"📊 RESUMEN")
print(f"{'='*80}")

total_leyes = len(LEYES_TEMARIO_OFICIAL)
leyes_indexadas = sum(1 for v in LEYES_TEMARIO_OFICIAL.values() if v['indexada'])
leyes_faltantes = sum(1 for v in LEYES_TEMARIO_OFICIAL.values() if not v['indexada'])

print(f"   Total leyes del temario: {total_leyes}")
print(f"   ✅ Indexadas: {leyes_indexadas}")
print(f"   ❌ Faltantes: {leyes_faltantes}")
print(f"   📈 Cobertura: {(leyes_indexadas/total_leyes)*100:.1f}%")

# Leyes faltantes
if leyes_faltantes > 0:
    print(f"\n{'='*80}")
    print(f"❌ LEYES FALTANTES ({leyes_faltantes})")
    print(f"{'='*80}")
    
    for norma_id, info in LEYES_TEMARIO_OFICIAL.items():
        if not info['indexada']:
            print(f"\n📌 {info['nombre']}")
            print(f"   Bloque: {info['bloque']}")
            print(f"   ID sugerido: {norma_id}")
            
            # Buscar posibles variantes
            posibles = []
            for norma_indexada in normas_counter.keys():
                if any(palabra in norma_indexada.lower() for palabra in norma_id.lower().split('_')):
                    posibles.append(norma_indexada)
            
            if posibles:
                print(f"   ⚠️  Posibles variantes indexadas:")
                for p in posibles:
                    print(f"      - {p} ({normas_counter[p]} chunks)")
    
    print(f"\n💡 RECOMENDACIÓN:")
    print(f"   Las siguientes leyes NO están indexadas:")
    for norma_id, info in LEYES_TEMARIO_OFICIAL.items():
        if not info['indexada']:
            print(f"   - {info['nombre']}")
    
    print(f"\n   Necesitas indexar estas leyes adicionales para completar el temario oficial.")
else:
    print(f"\n🎉 ¡PERFECTO! Todas las leyes del temario oficial están indexadas")

# Leyes adicionales indexadas
print(f"\n{'='*80}")
print(f"📌 LEYES ADICIONALES INDEXADAS (no en temario)")
print(f"{'='*80}")

leyes_adicionales = []
for norma, count in normas_counter.items():
    if norma not in LEYES_TEMARIO_OFICIAL and norma != 'N/A':
        leyes_adicionales.append({'norma': norma, 'chunks': count})

if leyes_adicionales:
    for ley in sorted(leyes_adicionales, key=lambda x: x['chunks'], reverse=True):
        print(f"   {ley['norma']:50} {ley['chunks']:4} chunks")
    print(f"\n   Total: {len(leyes_adicionales)} leyes adicionales")
else:
    print(f"   Ninguna")

print(f"\n{'='*80}")
