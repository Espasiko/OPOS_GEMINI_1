#!/usr/bin/env python3
"""
CREAR ÍNDICE PARA CAMPO 'norma' EN QDRANT CLOUD
Esto permite filtrado eficiente por norma específica
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Cargar variables de entorno
env_path = Path(__file__).parent / 'backend' / '.env.backend'
load_dotenv(env_path)

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print("="*80)
print("🔧 CREAR ÍNDICE PARA CAMPO 'norma'")
print("="*80)

# Conectar a Qdrant
print(f"\n🔌 Conectando a Qdrant Cloud...")
print(f"   URL: {QDRANT_URL}")
print(f"   Colección: {COLLECTION_NAME}")

try:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print(f"✅ Conectado")
except Exception as e:
    print(f"❌ Error conectando: {e}")
    exit(1)

# Crear índice para 'norma'
print(f"\n🔨 Creando índice para campo 'norma'...")
try:
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="norma",
        field_schema="keyword"
    )
    print(f"✅ Índice creado exitosamente")
except Exception as e:
    if "already exists" in str(e).lower():
        print(f"⚠️  Índice ya existe")
    else:
        print(f"❌ Error creando índice: {e}")
        exit(1)

# Crear índices adicionales útiles
campos_adicionales = [
    ("tipo", "keyword"),
    ("prioridad", "keyword"),
    ("articulo", "keyword"),
    ("layer", "integer")
]

print(f"\n🔨 Creando índices adicionales...")
for campo, tipo in campos_adicionales:
    try:
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=campo,
            field_schema=tipo
        )
        print(f"   ✅ Índice '{campo}' ({tipo}) creado")
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"   ⚠️  Índice '{campo}' ya existe")
        else:
            print(f"   ❌ Error con '{campo}': {e}")

# Verificar índices creados
print(f"\n📊 Verificando índices...")
try:
    collection_info = client.get_collection(COLLECTION_NAME)
    print(f"✅ Colección: {COLLECTION_NAME}")
    print(f"   Total puntos: {collection_info.points_count:,}")
    print(f"   Vectores: {collection_info.vectors_count:,}")
except Exception as e:
    print(f"⚠️  Error obteniendo info: {e}")

print(f"\n{'='*80}")
print(f"✅ ÍNDICES CREADOS")
print(f"{'='*80}")
print(f"\n💡 Ahora puedes usar filtros eficientemente:")
print(f"   - Por norma: filter={{\"norma\": \"LGSS\"}}")
print(f"   - Por tipo: filter={{\"tipo\": \"ley\"}}")
print(f"   - Por prioridad: filter={{\"prioridad\": \"critica\"}}")
print(f"   - Por artículo: filter={{\"articulo\": \"Art. 41\"}}")
print(f"   - Por capa: filter={{\"layer\": 1}}")
