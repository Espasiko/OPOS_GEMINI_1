"""
Migrar colección de Qdrant local a Qdrant Cloud
Útil para:
1. Backup de datos
2. Migración a producción
3. Calcular tamaño real de la BD vectorial
"""

import requests
import json
from typing import List, Dict
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo correcto
env_path = Path(__file__).parent / '.env.backend'
load_dotenv(env_path)

# Configuración
QDRANT_LOCAL_URL = "http://localhost:6333"
QDRANT_CLOUD_URL_RAW = os.getenv('QDRANT_URL', 'https://b554ceb5-2169-4064-9ce7-83c8cd44cf84.europe-west3.gcp.cloud.qdrant.io')
# Asegurar que tiene el puerto 6333
if ':6333' not in QDRANT_CLOUD_URL_RAW:
    QDRANT_CLOUD_URL = f"{QDRANT_CLOUD_URL_RAW}:6333"
else:
    QDRANT_CLOUD_URL = QDRANT_CLOUD_URL_RAW

QDRANT_CLOUD_API_KEY = os.getenv('QDRANT_API_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.8bgnDB3v7ze2ST9THOHf7IdWziXM5cmA_PQpzHZUGGU')

COLLECTION_NAME = "opositaia_leyes_seguridad_social"

print(f"🔧 Debug: URL: {QDRANT_CLOUD_URL}")
print(f"🔧 Debug: API Key cargada: {QDRANT_CLOUD_API_KEY[:20]}..." if QDRANT_CLOUD_API_KEY else "❌ No API Key")

def get_collection_info(base_url: str, api_key: str = None) -> Dict:
    """Obtiene información de la colección"""
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["api-key"] = api_key
    
    response = requests.get(
        f"{base_url}/collections/{COLLECTION_NAME}",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()["result"]
    else:
        raise Exception(f"Error obteniendo info: {response.text}")

def create_collection_in_cloud(config: Dict):
    """Crea la colección en Qdrant Cloud con la misma configuración"""
    headers = {
        "api-key": QDRANT_CLOUD_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "vectors": config["config"]["params"]["vectors"],
        "optimizers_config": config["config"]["optimizer_config"],
        "hnsw_config": config["config"]["hnsw_config"]
    }
    
    response = requests.put(
        f"{QDRANT_CLOUD_URL}/collections/{COLLECTION_NAME}",
        headers=headers,
        json=payload
    )
    
    if response.status_code in [200, 201]:
        print(f"✅ Colección creada en cloud")
    elif response.status_code == 409:
        print(f"⚠️  Colección ya existe en cloud (esto es OK)")
    else:
        print(f"⚠️  Error: {response.text}")

def get_all_points_local() -> List[Dict]:
    """Obtiene todos los puntos de Qdrant local"""
    print("📥 Descargando puntos de Qdrant local...")
    
    # Primero, contar cuántos puntos hay
    count_response = requests.post(
        f"{QDRANT_LOCAL_URL}/collections/{COLLECTION_NAME}/points/count",
        json={"exact": True}
    )
    
    total_points = count_response.json()["result"]["count"]
    print(f"   Total puntos: {total_points}")
    
    if total_points == 0:
        print("⚠️  No hay puntos para migrar")
        return []
    
    # Descargar todos los puntos (en batches si es necesario)
    all_points = []
    offset = None
    batch_size = 100
    
    while True:
        payload = {
            "limit": batch_size,
            "with_payload": True,
            "with_vector": True
        }
        
        if offset:
            payload["offset"] = offset
        
        response = requests.post(
            f"{QDRANT_LOCAL_URL}/collections/{COLLECTION_NAME}/points/scroll",
            json=payload
        )
        
        result = response.json()["result"]
        points = result["points"]
        
        if not points:
            break
        
        all_points.extend(points)
        print(f"   Descargados: {len(all_points)}/{total_points}")
        
        offset = result.get("next_page_offset")
        if not offset:
            break
    
    return all_points

def upload_points_to_cloud(points: List[Dict]):
    """Sube puntos a Qdrant Cloud"""
    print(f"\n📤 Subiendo {len(points)} puntos a Qdrant Cloud...")
    
    headers = {
        "api-key": QDRANT_CLOUD_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Subir en batches de 100
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i+batch_size]
        
        payload = {
            "points": batch
        }
        
        response = requests.put(
            f"{QDRANT_CLOUD_URL}/collections/{COLLECTION_NAME}/points",
            headers=headers,
            json=payload
        )
        
        if response.status_code in [200, 201]:
            print(f"   ✅ Batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1} subido")
        else:
            print(f"   ❌ Error en batch {i//batch_size + 1}: {response.text}")
            raise Exception("Error subiendo puntos")
        
        time.sleep(0.5)  # Rate limiting

def calculate_storage_size(points: List[Dict]) -> Dict:
    """Calcula el tamaño aproximado de almacenamiento"""
    if not points:
        return {"vectors": 0, "payload": 0, "total_mb": 0}
    
    # Tamaño de vectores
    vector_dim = len(points[0]["vector"])
    num_points = len(points)
    vector_size_bytes = vector_dim * 4 * num_points  # 4 bytes por float32
    
    # Tamaño de payloads (aproximado)
    payload_size_bytes = sum(
        len(json.dumps(p["payload"]).encode('utf-8'))
        for p in points
    )
    
    total_mb = (vector_size_bytes + payload_size_bytes) / (1024 * 1024)
    
    return {
        "num_points": num_points,
        "vector_dimension": vector_dim,
        "vectors_mb": vector_size_bytes / (1024 * 1024),
        "payload_mb": payload_size_bytes / (1024 * 1024),
        "total_mb": total_mb,
        "qdrant_cloud_tier": "Free (1GB)" if total_mb < 1000 else "Paid ($25/mes para 10GB)"
    }

def migrate():
    """Función principal de migración"""
    print("="*60)
    print("🚀 MIGRACIÓN QDRANT LOCAL → CLOUD")
    print("="*60)
    
    # Paso 1: Verificar colección local
    print("\n📍 Paso 1: Verificar colección local")
    try:
        local_info = get_collection_info(QDRANT_LOCAL_URL)
        print(f"✅ Colección local encontrada")
        print(f"   Puntos: {local_info['points_count']}")
        print(f"   Vectores: {local_info['config']['params']['vectors']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Paso 2: Descargar puntos
    print("\n📍 Paso 2: Descargar puntos de local")
    points = get_all_points_local()
    
    if not points:
        print("⚠️  No hay puntos para migrar. Abortando.")
        return
    
    # Paso 3: Calcular tamaño
    print("\n📍 Paso 3: Calcular tamaño de almacenamiento")
    size_info = calculate_storage_size(points)
    print(f"   Puntos: {size_info['num_points']}")
    print(f"   Dimensión: {size_info['vector_dimension']}")
    print(f"   Vectores: {size_info['vectors_mb']:.2f} MB")
    print(f"   Payloads: {size_info['payload_mb']:.2f} MB")
    print(f"   TOTAL: {size_info['total_mb']:.2f} MB")
    print(f"   Tier Qdrant Cloud: {size_info['qdrant_cloud_tier']}")
    
    # Paso 4: Crear colección en cloud
    print("\n📍 Paso 4: Crear colección en Qdrant Cloud")
    print(f"   URL: {QDRANT_CLOUD_URL}")
    print(f"   Colección: {COLLECTION_NAME}")
    
    if not QDRANT_CLOUD_API_KEY:
        print("❌ No se encontró QDRANT_API_KEY en .env.backend")
        print("\n📊 RESUMEN:")
        print(f"   - Puntos a migrar: {size_info['num_points']}")
        print(f"   - Tamaño total: {size_info['total_mb']:.2f} MB")
        print(f"   - Tier necesario: {size_info['qdrant_cloud_tier']}")
        return
    
    try:
        create_collection_in_cloud(local_info)
    except Exception as e:
        print(f"❌ Error creando colección: {e}")
        return
    
    # Paso 5: Subir puntos
    print("\n📍 Paso 5: Subir puntos a cloud")
    try:
        upload_points_to_cloud(points)
    except Exception as e:
        print(f"❌ Error subiendo puntos: {e}")
        return
    
    # Paso 6: Verificar
    print("\n📍 Paso 6: Verificar migración")
    try:
        cloud_info = get_collection_info(QDRANT_CLOUD_URL, QDRANT_CLOUD_API_KEY)
        print(f"✅ Colección en cloud verificada")
        print(f"   Puntos: {cloud_info['points_count']}")
        
        if cloud_info['points_count'] == local_info['points_count']:
            print("\n🎉 MIGRACIÓN EXITOSA")
        else:
            print(f"\n⚠️  Advertencia: Puntos no coinciden")
            print(f"   Local: {local_info['points_count']}")
            print(f"   Cloud: {cloud_info['points_count']}")
    except Exception as e:
        print(f"❌ Error verificando: {e}")
    
    print("\n" + "="*60)
    print("✅ PROCESO COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    migrate()
