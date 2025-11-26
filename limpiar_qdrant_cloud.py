#!/usr/bin/env python3
"""
Limpiar Qdrant Cloud - Eliminar toda la colección
CUIDADO: Esto borrará TODOS los datos de la colección
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Cargar variables de entorno
load_dotenv('backend/.env.backend')

QDRANT_CLOUD_URL = os.getenv('QDRANT_URL')
QDRANT_CLOUD_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print("="*80)
print("🗑️  LIMPIAR QDRANT CLOUD")
print("="*80)
print(f"\n⚠️  ADVERTENCIA: Esto eliminará TODA la colección '{COLLECTION_NAME}'")
print(f"   URL: {QDRANT_CLOUD_URL}")
print(f"\n¿Estás seguro? (escribe 'SI' para confirmar)")

confirmacion = input("> ").strip()

if confirmacion != "SI":
    print("\n❌ Operación cancelada")
    exit(0)

print(f"\n🔌 Conectando a Qdrant Cloud...")

try:
    client = QdrantClient(
        url=QDRANT_CLOUD_URL,
        api_key=QDRANT_CLOUD_API_KEY,
        timeout=30
    )
    
    # Verificar que la colección existe
    try:
        collection_info = client.get_collection(COLLECTION_NAME)
        total_points = collection_info.points_count
        print(f"✅ Colección encontrada: {total_points} documentos")
    except Exception as e:
        print(f"⚠️  Colección no existe o error: {e}")
        print(f"   No hay nada que eliminar")
        exit(0)
    
    # Eliminar la colección
    print(f"\n🗑️  Eliminando colección '{COLLECTION_NAME}'...")
    client.delete_collection(COLLECTION_NAME)
    print(f"✅ Colección eliminada exitosamente")
    
    print(f"\n📊 Resumen:")
    print(f"   - Documentos eliminados: {total_points}")
    print(f"   - Colección: {COLLECTION_NAME}")
    print(f"   - Estado: Eliminada")
    
    print(f"\n✅ Qdrant Cloud limpio y listo para re-indexar")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*80)
print("✅ LIMPIEZA COMPLETADA")
print("="*80)
