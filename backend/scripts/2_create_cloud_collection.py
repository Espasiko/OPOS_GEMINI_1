"""
Paso 2: Crear colección en Qdrant Cloud
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(".env.backend")

print("🔄 Creando colección en Qdrant Cloud...")

# Leer configuración del export
try:
    with open("qdrant_export.json", "r", encoding="utf-8") as f:
        export_data = json.load(f)
    print(f"✅ Datos de exportación cargados: {export_data['points_count']} puntos")
except FileNotFoundError:
    print("❌ Error: Archivo qdrant_export.json no encontrado")
    print("   Ejecuta primero: python scripts/1_export_local.py")
    sys.exit(1)

# Obtener credenciales
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

if not qdrant_url or not qdrant_api_key:
    print("❌ Error: Faltan credenciales de Qdrant Cloud")
    print("   Añade QDRANT_URL y QDRANT_API_KEY en .env.backend")
    sys.exit(1)

print(f"🔗 Conectando a: {qdrant_url}")

try:
    # Conectar a Qdrant Cloud
    cloud_client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=60.0
    )
    
    # Verificar conexión
    collections = cloud_client.get_collections()
    print(f"✅ Conectado a Qdrant Cloud")
    print(f"   Colecciones existentes: {[c.name for c in collections.collections]}")
    
    collection_name = export_data["collection_name"]
    
    # Verificar si ya existe
    existing_collections = [c.name for c in collections.collections]
    if collection_name in existing_collections:
        print(f"⚠️  La colección '{collection_name}' ya existe")
        response = input("   ¿Eliminar y recrear? (s/n): ")
        if response.lower() == 's':
            cloud_client.delete_collection(collection_name)
            print(f"   ✅ Colección eliminada")
        else:
            print("   ❌ Operación cancelada")
            sys.exit(0)
    
    # Crear colección
    print(f"📦 Creando colección '{collection_name}'...")
    
    # Mapear distancia
    distance_map = {
        "Cosine": Distance.COSINE,
        "Euclid": Distance.EUCLID,
        "Dot": Distance.DOT
    }
    distance = distance_map.get(export_data["distance"], Distance.COSINE)
    
    cloud_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=export_data["vector_size"],
            distance=distance
        )
    )
    
    print(f"✅ Colección creada exitosamente!")
    print(f"   Nombre: {collection_name}")
    print(f"   Tamaño vector: {export_data['vector_size']}")
    print(f"   Distancia: {export_data['distance']}")
    
    # Verificar
    info = cloud_client.get_collection(collection_name)
    print(f"✅ Verificación: {info.points_count} puntos (debería ser 0)")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
