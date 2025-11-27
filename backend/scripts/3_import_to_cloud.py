"""
Paso 3: Importar datos a Qdrant Cloud
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import json
from dotenv import load_dotenv
from tqdm import tqdm

# Cargar variables de entorno
load_dotenv(".env.backend")

print("🔄 Importando datos a Qdrant Cloud...")

# Leer datos exportados
try:
    with open("qdrant_export.json", "r", encoding="utf-8") as f:
        export_data = json.load(f)
    print(f"✅ Datos cargados: {export_data['points_count']} puntos")
except FileNotFoundError:
    print("❌ Error: Archivo qdrant_export.json no encontrado")
    sys.exit(1)

# Obtener credenciales
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

if not qdrant_url or not qdrant_api_key:
    print("❌ Error: Faltan credenciales de Qdrant Cloud")
    sys.exit(1)

try:
    # Conectar a Qdrant Cloud
    cloud_client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=120.0  # Timeout largo para importación
    )
    
    collection_name = export_data["collection_name"]
    points_data = export_data["points"]
    
    print(f"📦 Importando {len(points_data)} puntos en batches de 100...")
    
    # Importar en batches
    batch_size = 100
    total_imported = 0
    
    for i in tqdm(range(0, len(points_data), batch_size), desc="Importando"):
        batch = points_data[i:i+batch_size]
        
        points = [
            PointStruct(
                id=point['id'],
                vector=point['vector'],
                payload=point['payload']
            )
            for point in batch
        ]
        
        cloud_client.upsert(
            collection_name=collection_name,
            points=points
        )
        
        total_imported += len(batch)
    
    print(f"\n✅ Importación completada!")
    print(f"   Puntos importados: {total_imported}")
    
    # Verificar
    info = cloud_client.get_collection(collection_name)
    print(f"✅ Verificación: {info.points_count} puntos en cloud")
    
    if info.points_count == export_data['points_count']:
        print("✅ ¡Migración exitosa! Todos los puntos importados correctamente")
    else:
        print(f"⚠️  Advertencia: Esperados {export_data['points_count']}, encontrados {info.points_count}")
    
    # Probar búsqueda
    print("\n🔍 Probando búsqueda...")
    results = cloud_client.scroll(
        collection_name=collection_name,
        limit=3,
        with_payload=True
    )
    
    print(f"✅ Primeros 3 documentos:")
    for point in results[0]:
        ley = point.payload.get('ley_nombre', 'Sin nombre')
        articulo = point.payload.get('articulo', 'N/A')
        print(f"   - {ley} - Art. {articulo}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
