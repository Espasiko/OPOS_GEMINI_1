"""
Paso 1: Exportar colección de Qdrant local
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qdrant_client import QdrantClient
import json
from datetime import datetime

print("🔄 Exportando colección de Qdrant local...")

try:
    # Conectar a Qdrant local
    local_client = QdrantClient(url="http://localhost:6333")
    
    collection_name = "opositaia_leyes_seguridad_social"
    
    # Verificar que existe
    try:
        collection_info = local_client.get_collection(collection_name)
        print(f"✅ Colección encontrada: {collection_info.points_count} puntos")
    except Exception as e:
        print(f"❌ Error: Colección '{collection_name}' no encontrada")
        print(f"   Colecciones disponibles: {[c.name for c in local_client.get_collections().collections]}")
        sys.exit(1)
    
    # Exportar todos los puntos
    print("📦 Exportando puntos...")
    all_points = []
    offset = None
    
    while True:
        result = local_client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=True
        )
        
        points, next_offset = result
        
        if not points:
            break
        
        all_points.extend(points)
        print(f"   Exportados {len(all_points)} puntos...")
        
        if next_offset is None:
            break
        
        offset = next_offset
    
    # Preparar datos para exportar
    export_data = {
        "collection_name": collection_name,
        "exported_at": datetime.now().isoformat(),
        "points_count": len(all_points),
        "vector_size": collection_info.config.params.vectors.size,
        "distance": str(collection_info.config.params.vectors.distance),
        "points": [
            {
                "id": str(point.id),
                "vector": point.vector,
                "payload": point.payload
            }
            for point in all_points
        ]
    }
    
    # Guardar a archivo
    output_file = "qdrant_export.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Exportación completada!")
    print(f"   Archivo: {output_file}")
    print(f"   Puntos exportados: {len(all_points)}")
    print(f"   Tamaño del vector: {export_data['vector_size']}")
    print(f"   Distancia: {export_data['distance']}")
    
except Exception as e:
    print(f"\n❌ Error durante la exportación: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
