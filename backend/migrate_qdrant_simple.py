"""
Migración simple usando qdrant-client
"""
from qdrant_client import QdrantClient
from pathlib import Path
from dotenv import load_dotenv
import os

# Cargar env
env_path = Path(__file__).parent / '.env.backend'
load_dotenv(env_path)

# Configuración
LOCAL_URL = "http://localhost:6333"
# Qdrant Cloud usa el formato sin puerto en la URL
CLOUD_URL = "https://b554ceb5-2169-4064-9ce7-83c8cd44cf84.europe-west3-0.gcp.cloud.qdrant.io"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.8bgnDB3v7ze2ST9THOHf7IdWziXM5cmA_PQpzHZUGGU"
COLLECTION = "opositaia_leyes_seguridad_social"

print("="*60)
print("🚀 MIGRACIÓN QDRANT LOCAL → CLOUD")
print("="*60)

# Conectar a local
print("\n📍 Conectando a Qdrant local...")
local_client = QdrantClient(url=LOCAL_URL)
local_info = local_client.get_collection(COLLECTION)
print(f"✅ Colección local: {local_info.points_count} puntos")

# Conectar a cloud
print("\n📍 Conectando a Qdrant Cloud...")
cloud_client = QdrantClient(
    url=CLOUD_URL,
    api_key=API_KEY
)

# Verificar si la colección ya existe en cloud
try:
    cloud_info = cloud_client.get_collection(COLLECTION)
    print(f"✅ Colección ya existe en cloud: {cloud_info.points_count} puntos")
    
    if cloud_info.points_count == local_info.points_count:
        print("\n🎉 ¡La migración ya está completa!")
        print(f"   Local: {local_info.points_count} puntos")
        print(f"   Cloud: {cloud_info.points_count} puntos")
        exit(0)
    else:
        print(f"⚠️  Diferencia detectada:")
        print(f"   Local: {local_info.points_count} puntos")
        print(f"   Cloud: {cloud_info.points_count} puntos")
        print(f"   Procediendo a sincronizar...")
except Exception as e:
    print(f"ℹ️  Colección no existe en cloud, creando...")
    # Crear colección en cloud
    cloud_client.create_collection(
        collection_name=COLLECTION,
        vectors_config=local_info.config.params.vectors
    )
    print(f"✅ Colección creada en cloud")

# Descargar todos los puntos de local
print(f"\n📥 Descargando {local_info.points_count} puntos de local...")
points, next_offset = local_client.scroll(
    collection_name=COLLECTION,
    limit=10000,  # Descargar todos de una vez
    with_payload=True,
    with_vectors=True
)
print(f"✅ Descargados {len(points)} puntos")

# Convertir Records a PointStructs
from qdrant_client.models import PointStruct
print(f"\n🔄 Convirtiendo formato de puntos...")
point_structs = [
    PointStruct(
        id=point.id,
        vector=point.vector,
        payload=point.payload
    )
    for point in points
]
print(f"✅ Puntos convertidos")

# Subir a cloud en batches
print(f"\n📤 Subiendo puntos a cloud en batches...")
batch_size = 100
total_batches = (len(point_structs) + batch_size - 1) // batch_size

for i in range(0, len(point_structs), batch_size):
    batch = point_structs[i:i+batch_size]
    cloud_client.upsert(
        collection_name=COLLECTION,
        points=batch
    )
    batch_num = i // batch_size + 1
    print(f"   ✅ Batch {batch_num}/{total_batches} subido ({len(batch)} puntos)")

print(f"✅ Todos los puntos subidos")

# Verificar
print(f"\n📍 Verificando migración...")
cloud_info_final = cloud_client.get_collection(COLLECTION)
print(f"✅ Colección en cloud: {cloud_info_final.points_count} puntos")

if cloud_info_final.points_count == local_info.points_count:
    print("\n🎉 ¡MIGRACIÓN EXITOSA!")
    print(f"   Local: {local_info.points_count} puntos")
    print(f"   Cloud: {cloud_info_final.points_count} puntos")
    print(f"   Tamaño: ~43 MB")
    print(f"   Tier: Free (1GB)")
else:
    print(f"\n⚠️  Advertencia: Puntos no coinciden")
    print(f"   Local: {local_info.points_count}")
    print(f"   Cloud: {cloud_info_final.points_count}")

print("\n" + "="*60)
