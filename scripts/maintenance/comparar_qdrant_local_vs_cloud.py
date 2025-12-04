#!/usr/bin/env python3
"""
Comparar contenido de Qdrant Local vs Cloud
Verificar las 3 capas del RAG
"""
import os
import requests
from dotenv import load_dotenv
from collections import Counter

# Cargar variables de entorno
load_dotenv('backend/.env.backend')

QDRANT_LOCAL_URL = "http://localhost:6333"
QDRANT_CLOUD_URL = os.getenv('QDRANT_URL')
QDRANT_CLOUD_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print("="*80)
print("🔍 COMPARACIÓN QDRANT LOCAL VS CLOUD")
print("="*80)

def get_collection_stats(base_url, api_key=None, name="Local"):
    """Obtiene estadísticas de una colección"""
    print(f"\n📊 Analizando {name}...")
    print(f"   URL: {base_url}")
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["api-key"] = api_key
    
    try:
        # Obtener info de colección
        response = requests.get(
            f"{base_url}/collections/{COLLECTION_NAME}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            return None
        
        info = response.json()["result"]
        total_points = info['points_count']
        print(f"   ✅ Total puntos: {total_points}")
        
        # Obtener muestra de puntos para analizar
        print(f"   📥 Descargando muestra de puntos...")
        
        layers = Counter()
        tipos = Counter()
        normas = Counter()
        fuentes = Counter()
        
        offset = None
        batch_size = 100
        total_checked = 0
        max_check = min(1000, total_points)  # Limitar a 1000 para velocidad
        
        while total_checked < max_check:
            payload = {
                "limit": batch_size,
                "with_payload": True,
                "with_vector": False
            }
            
            if offset:
                payload["offset"] = offset
            
            response = requests.post(
                f"{base_url}/collections/{COLLECTION_NAME}/points/scroll",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"   ⚠️  Error en scroll: {response.status_code}")
                break
            
            result = response.json()["result"]
            points = result["points"]
            
            if not points:
                break
            
            for point in points:
                payload_data = point["payload"]
                
                # Contar por capa
                layer = payload_data.get('layer', 'N/A')
                layers[layer] += 1
                
                # Contar por tipo
                tipo = payload_data.get('tipo', 'N/A')
                tipos[tipo] += 1
                
                # Contar por norma
                norma = payload_data.get('norma', payload_data.get('material_nombre', 'N/A'))
                normas[norma] += 1
                
                # Contar por fuente
                fuente = payload_data.get('fuente', 'N/A')
                fuentes[fuente] += 1
            
            total_checked += len(points)
            print(f"   Analizados: {total_checked}/{max_check}", end='\r')
            
            offset = result.get("next_page_offset")
            if not offset:
                break
        
        print(f"\n   ✅ Análisis completado: {total_checked} puntos")
        
        return {
            'total_points': total_points,
            'analyzed': total_checked,
            'layers': dict(layers),
            'tipos': dict(tipos),
            'normas': dict(normas),
            'fuentes': dict(fuentes)
        }
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def print_stats(stats, name):
    """Imprime estadísticas de forma legible"""
    if not stats:
        print(f"\n❌ No hay estadísticas para {name}")
        return
    
    print(f"\n{'='*80}")
    print(f"📊 ESTADÍSTICAS {name.upper()}")
    print(f"{'='*80}")
    
    print(f"\n📈 Total de puntos: {stats['total_points']}")
    print(f"🔍 Analizados: {stats['analyzed']} ({stats['analyzed']/stats['total_points']*100:.1f}%)")
    
    print(f"\n🔢 DISTRIBUCIÓN POR CAPA (Sistema de 3 capas):")
    for layer in sorted(stats['layers'].keys()):
        count = stats['layers'][layer]
        percentage = (count / stats['analyzed']) * 100
        print(f"   Capa {layer}: {count:,} docs ({percentage:.1f}%)")
    
    print(f"\n📑 DISTRIBUCIÓN POR TIPO:")
    for tipo in sorted(stats['tipos'].keys(), key=lambda x: stats['tipos'][x], reverse=True):
        count = stats['tipos'][tipo]
        percentage = (count / stats['analyzed']) * 100
        print(f"   {tipo}: {count:,} docs ({percentage:.1f}%)")
    
    print(f"\n📚 TOP 10 NORMAS/MATERIALES:")
    top_normas = sorted(stats['normas'].items(), key=lambda x: x[1], reverse=True)[:10]
    for norma, count in top_normas:
        percentage = (count / stats['analyzed']) * 100
        # Truncar nombre si es muy largo
        norma_short = norma[:60] + '...' if len(norma) > 60 else norma
        print(f"   {norma_short}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n🏢 DISTRIBUCIÓN POR FUENTE:")
    for fuente in sorted(stats['fuentes'].keys(), key=lambda x: stats['fuentes'][x], reverse=True):
        count = stats['fuentes'][fuente]
        percentage = (count / stats['analyzed']) * 100
        print(f"   {fuente}: {count:,} docs ({percentage:.1f}%)")

# Analizar Local
print("\n" + "="*80)
print("🏠 QDRANT LOCAL")
print("="*80)
local_stats = get_collection_stats(QDRANT_LOCAL_URL, name="Local")

# Analizar Cloud
print("\n" + "="*80)
print("☁️  QDRANT CLOUD")
print("="*80)
cloud_stats = get_collection_stats(QDRANT_CLOUD_URL, QDRANT_CLOUD_API_KEY, name="Cloud")

# Imprimir estadísticas detalladas
if local_stats:
    print_stats(local_stats, "LOCAL")

if cloud_stats:
    print_stats(cloud_stats, "CLOUD")

# Comparación
print(f"\n{'='*80}")
print("🔄 COMPARACIÓN")
print(f"{'='*80}")

if local_stats and cloud_stats:
    print(f"\n📊 Puntos totales:")
    print(f"   Local:  {local_stats['total_points']:,}")
    print(f"   Cloud:  {cloud_stats['total_points']:,}")
    print(f"   Diferencia: {abs(local_stats['total_points'] - cloud_stats['total_points']):,}")
    
    if local_stats['total_points'] == cloud_stats['total_points']:
        print(f"   ✅ Mismo número de puntos")
    else:
        print(f"   ⚠️  Diferente número de puntos")
    
    print(f"\n🔢 Capas presentes:")
    local_layers = set(local_stats['layers'].keys())
    cloud_layers = set(cloud_stats['layers'].keys())
    
    print(f"   Local: {sorted(local_layers)}")
    print(f"   Cloud: {sorted(cloud_layers)}")
    
    if local_layers == cloud_layers:
        print(f"   ✅ Mismas capas")
    else:
        missing_in_cloud = local_layers - cloud_layers
        extra_in_cloud = cloud_layers - local_layers
        if missing_in_cloud:
            print(f"   ⚠️  Faltan en Cloud: {sorted(missing_in_cloud)}")
        if extra_in_cloud:
            print(f"   ⚠️  Extra en Cloud: {sorted(extra_in_cloud)}")
    
    print(f"\n📑 Tipos de documento:")
    local_tipos = set(local_stats['tipos'].keys())
    cloud_tipos = set(cloud_stats['tipos'].keys())
    
    print(f"   Local: {sorted(local_tipos)}")
    print(f"   Cloud: {sorted(cloud_tipos)}")
    
    if local_tipos == cloud_tipos:
        print(f"   ✅ Mismos tipos")
    else:
        missing_in_cloud = local_tipos - cloud_tipos
        if missing_in_cloud:
            print(f"   ⚠️  Faltan en Cloud: {sorted(missing_in_cloud)}")

print(f"\n{'='*80}")
print("✅ ANÁLISIS COMPLETADO")
print(f"{'='*80}")
