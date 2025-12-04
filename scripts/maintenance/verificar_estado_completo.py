#!/usr/bin/env python3
"""
VERIFICAR ESTADO COMPLETO Y CONSTITUCIÓN
Verifica todas las leyes indexadas y analiza la Constitución
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from collections import Counter

# Cargar variables de entorno
env_path = Path(__file__).parent / 'backend' / '.env.backend'
load_dotenv(env_path)

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print("="*80)
print("🔍 VERIFICACIÓN COMPLETA DEL ESTADO")
print("="*80)

# Conectar a Qdrant
print(f"\n🔌 Conectando a Qdrant Cloud...")
try:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    collection_info = client.get_collection(COLLECTION_NAME)
    total_puntos = collection_info.points_count
    print(f"✅ Conectado - Total puntos: {total_puntos:,}")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Obtener TODOS los puntos
print(f"\n📊 Obteniendo todas las leyes...")
try:
    scroll_result = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=10000,
        with_payload=True,
        with_vectors=False
    )
    
    puntos = scroll_result[0]
    print(f"✅ Analizados {len(puntos):,} puntos")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Contar por norma
normas_counter = Counter()
for point in puntos:
    norma = point.payload.get('norma', 'N/A')
    normas_counter[norma] += 1

# Mostrar todas las leyes
print(f"\n{'='*80}")
print(f"📚 TODAS LAS LEYES INDEXADAS ({len(normas_counter)} normas)")
print(f"{'='*80}")

for norma, count in sorted(normas_counter.items(), key=lambda x: x[1], reverse=True):
    if norma != 'N/A':
        print(f"   {norma:40} {count:5} chunks")

# Analizar Constitución en detalle
print(f"\n{'='*80}")
print(f"📜 ANÁLISIS DETALLADO DE LA CONSTITUCIÓN")
print(f"{'='*80}")

try:
    # Obtener todos los chunks de la Constitución
    scroll_result = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="norma",
                    match=MatchValue(value="Constitucion")
                )
            ]
        ),
        limit=1000,
        with_payload=True,
        with_vectors=False
    )
    
    chunks_constitucion = scroll_result[0]
    print(f"\n📊 Total chunks Constitución: {len(chunks_constitucion)}")
    
    # Extraer artículos
    articulos = []
    for point in chunks_constitucion:
        articulo = point.payload.get('articulo')
        if articulo:
            # Extraer número
            try:
                num = int(articulo.split()[1])
                articulos.append(num)
            except:
                pass
    
    if articulos:
        articulos_unicos = sorted(set(articulos))
        print(f"   Artículos detectados: {len(articulos_unicos)}")
        print(f"   Rango: Art. {min(articulos)} - Art. {max(articulos)}")
        print(f"   Último artículo: Art. {max(articulos)}")
        
        # Verificar si está completa (la Constitución tiene 169 artículos)
        if max(articulos) >= 169:
            print(f"\n✅ CONSTITUCIÓN COMPLETA (tiene hasta el Art. 169)")
        elif max(articulos) >= 100:
            print(f"\n⚠️  CONSTITUCIÓN PARCIAL (llega hasta Art. {max(articulos)}, faltan hasta 169)")
        else:
            print(f"\n❌ CONSTITUCIÓN INCOMPLETA (solo hasta Art. {max(articulos)})")
        
        # Mostrar algunos artículos
        print(f"\n   Primeros 10 artículos: {articulos_unicos[:10]}")
        print(f"   Últimos 10 artículos: {articulos_unicos[-10:]}")
        
        # Detectar huecos
        huecos = []
        for i in range(min(articulos), max(articulos)):
            if i not in articulos:
                huecos.append(i)
        
        if huecos:
            print(f"\n   ⚠️  Artículos faltantes: {len(huecos)}")
            if len(huecos) <= 20:
                print(f"      {huecos}")
        else:
            print(f"\n   ✅ Sin huecos en el rango detectado")
    else:
        print(f"   ⚠️  No se detectaron artículos numerados")
        
except Exception as e:
    print(f"❌ Error analizando Constitución: {e}")

# Verificar leyes nuevas del temario
print(f"\n{'='*80}")
print(f"📋 LEYES DEL TEMARIO OFICIAL")
print(f"{'='*80}")

leyes_temario = {
    "Ley_34_2014": "Ley 34/2014 - Liquidación e ingreso de cuotas SS",
    "LO_6_1985_LOPJ": "LO 6/1985 - Poder Judicial",
    "LO_2_1979_LOTC": "LO 2/1979 - Tribunal Constitucional",
    "LO_5_1985_LOREG": "LO 5/1985 - Régimen Electoral General"
}

print(f"\n🔍 Leyes añadidas recientemente:")
for norma_id, nombre in leyes_temario.items():
    chunks = normas_counter.get(norma_id, 0)
    if chunks > 0:
        print(f"   ✅ {nombre:50} {chunks:5} chunks")
    else:
        print(f"   ❌ {nombre:50} NO INDEXADA")

print(f"\n{'='*80}")
print(f"📊 RESUMEN FINAL")
print(f"{'='*80}")
print(f"   Total puntos: {total_puntos:,}")
print(f"   Total normas: {len(normas_counter)}")
print(f"   Tamaño estimado: ~{(total_puntos * 4) / 1024:.2f} MB")

print(f"\n{'='*80}")
