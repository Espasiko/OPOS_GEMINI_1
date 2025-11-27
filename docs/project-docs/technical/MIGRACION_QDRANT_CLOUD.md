# 🚀 MIGRACIÓN A QDRANT CLOUD - PLAN COMPLETO

**Fecha**: 23 Noviembre 2025  
**Estado**: Pendiente ejecución

---

## 📊 SITUACIÓN ACTUAL

### Lo que tienes:
- ✅ Qdrant local (localhost:6333)
- ✅ Colección: `opositaia_leyes_seguridad_social`
- ✅ Datos indexados localmente
- ✅ RAG Agent funcionando con Qdrant local

### Lo que necesitas:
- 🎯 Migrar a Qdrant Cloud
- 🎯 Mantener todos los datos
- 🎯 Actualizar configuración
- 🎯 Probar que funciona

---

## 🎯 OPCIONES DE MIGRACIÓN

### **Opción 1: Exportar/Importar (RECOMENDADO)** ⭐

**Ventajas:**
- ✅ Mantiene todos los datos
- ✅ Mantiene metadatos
- ✅ Rápido (minutos)
- ✅ Sin re-procesar documentos

**Pasos:**
1. Exportar colección local
2. Crear colección en Qdrant Cloud
3. Importar datos
4. Actualizar configuración

### **Opción 2: Re-indexar desde cero**

**Ventajas:**
- ✅ Datos limpios
- ✅ Oportunidad de mejorar embeddings
- ✅ Actualizar metadatos

**Desventajas:**
- ❌ Toma más tiempo (horas)
- ❌ Necesita re-procesar PDFs

---

## 📋 PASO A PASO: OPCIÓN 1 (Exportar/Importar)

### **Paso 1: Obtener credenciales de Qdrant Cloud**

1. Ve a https://cloud.qdrant.io
2. Crea un cluster (si no lo tienes)
3. Obtén:
   - URL del cluster (ej: `https://xyz-abc123.eu-central.aws.cloud.qdrant.io`)
   - API Key (en la sección "API Keys")

### **Paso 2: Añadir credenciales al .env**

Edita `backend/.env.backend`:

```bash
# Qdrant Cloud (NUEVO)
QDRANT_URL=https://tu-cluster.qdrant.io:6333
QDRANT_API_KEY=tu-api-key-aqui
COLLECTION_NAME=opositaia_leyes_seguridad_social

# Qdrant Local (BACKUP - comentar después)
# QDRANT_URL_LOCAL=http://localhost:6333
```

### **Paso 3: Exportar colección local**

```python
# backend/scripts/export_qdrant_local.py
from qdrant_client import QdrantClient
import json

# Conectar a Qdrant local
local_client = QdrantClient(url="http://localhost:6333")

# Obtener info de la colección
collection_info = local_client.get_collection("opositaia_leyes_seguridad_social")
print(f"Colección: {collection_info.points_count} puntos")

# Exportar todos los puntos
points = local_client.scroll(
    collection_name="opositaia_leyes_seguridad_social",
    limit=10000,  # Ajustar según cantidad
    with_payload=True,
    with_vectors=True
)

# Guardar a archivo
with open("qdrant_export.json", "w", encoding="utf-8") as f:
    json.dump({
        "collection_name": "opositaia_leyes_seguridad_social",
        "points_count": collection_info.points_count,
        "vector_size": collection_info.config.params.vectors.size,
        "distance": collection_info.config.params.vectors.distance,
        "points": [
            {
                "id": point.id,
                "vector": point.vector,
                "payload": point.payload
            }
            for point in points[0]
        ]
    }, f, ensure_ascii=False, indent=2)

print(f"✅ Exportados {len(points[0])} puntos a qdrant_export.json")
```

Ejecutar:
```bash
cd backend
python scripts/export_qdrant_local.py
```

### **Paso 4: Crear colección en Qdrant Cloud**

```python
# backend/scripts/create_cloud_collection.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from dotenv import load_dotenv

load_dotenv(".env.backend")

# Conectar a Qdrant Cloud
cloud_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Crear colección (mismo config que local)
cloud_client.create_collection(
    collection_name="opositaia_leyes_seguridad_social",
    vectors_config=VectorParams(
        size=768,  # Tamaño del embedding (RoBERTalex)
        distance=Distance.COSINE
    )
)

print("✅ Colección creada en Qdrant Cloud")
```

Ejecutar:
```bash
cd backend
python scripts/create_cloud_collection.py
```

### **Paso 5: Importar datos a Qdrant Cloud**

```python
# backend/scripts/import_to_cloud.py
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import json
import os
from dotenv import load_dotenv

load_dotenv(".env.backend")

# Conectar a Qdrant Cloud
cloud_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Leer datos exportados
with open("qdrant_export.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Importando {len(data['points'])} puntos...")

# Importar en batches de 100
batch_size = 100
for i in range(0, len(data['points']), batch_size):
    batch = data['points'][i:i+batch_size]
    
    points = [
        PointStruct(
            id=point['id'],
            vector=point['vector'],
            payload=point['payload']
        )
        for point in batch
    ]
    
    cloud_client.upsert(
        collection_name="opositaia_leyes_seguridad_social",
        points=points
    )
    
    print(f"✅ Importados {i+len(batch)}/{len(data['points'])} puntos")

print("✅ Importación completada!")

# Verificar
info = cloud_client.get_collection("opositaia_leyes_seguridad_social")
print(f"✅ Colección en cloud: {info.points_count} puntos")
```

Ejecutar:
```bash
cd backend
python scripts/import_to_cloud.py
```

### **Paso 6: Actualizar RAG Agent**

```python
# backend/agents/rag_agent.py
import os
from qdrant_client import QdrantClient

class RAGAgent:
    def __init__(self):
        # Conectar a Qdrant Cloud (en vez de local)
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),           # Cloud URL
            api_key=os.getenv("QDRANT_API_KEY"),   # API Key
            timeout=30.0                            # Timeout para cloud
        )
        
        self.collection_name = os.getenv(
            "COLLECTION_NAME",
            "opositaia_leyes_seguridad_social"
        )
        
        logger.info(f"✅ RAG Agent conectado a Qdrant Cloud: {os.getenv('QDRANT_URL')}")
```

### **Paso 7: Probar conexión**

```python
# backend/scripts/test_cloud_connection.py
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv(".env.backend")

try:
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
    # Listar colecciones
    collections = client.get_collections()
    print("✅ Conectado a Qdrant Cloud!")
    print(f"Colecciones: {[c.name for c in collections.collections]}")
    
    # Info de la colección
    info = client.get_collection("opositaia_leyes_seguridad_social")
    print(f"✅ Colección: {info.points_count} puntos")
    
    # Búsqueda de prueba
    results = client.scroll(
        collection_name="opositaia_leyes_seguridad_social",
        limit=3,
        with_payload=True
    )
    
    print(f"✅ Primeros 3 documentos:")
    for point in results[0]:
        print(f"  - {point.payload.get('ley_nombre', 'Sin nombre')}")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

Ejecutar:
```bash
cd backend
python scripts/test_cloud_connection.py
```

---

## 🔧 CONFIGURACIÓN MCP QDRANT (Para Kiro)

Si quieres usar el MCP de Qdrant en Kiro (para desarrollo):

### **Instalar MCP Server de Qdrant:**

```bash
# Instalar con uvx (automático)
uvx mcp-server-qdrant
```

### **Configurar en Kiro:**

Edita `C:\Users\USER\.kiro\settings\mcp.json`:

```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "qdrant": {
      "command": "uvx",
      "args": ["mcp-server-qdrant"],
      "env": {
        "QDRANT_URL": "https://tu-cluster.qdrant.io:6333",
        "QDRANT_API_KEY": "tu-api-key-aqui",
        "COLLECTION_NAME": "opositaia_leyes_seguridad_social",
        "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2"
      }
    }
  }
}
```

### **Herramientas disponibles en Kiro:**

1. **qdrant-store**: Guardar información
   ```
   "Guarda en Qdrant: La base de cotización máxima 2025 es 4.720,50€"
   ```

2. **qdrant-find**: Buscar información
   ```
   "Busca en Qdrant: base de cotización máxima"
   ```

**Uso:** Solo para TI (desarrollo/debugging), NO para usuarios finales

---

## ✅ CHECKLIST DE MIGRACIÓN

### Pre-migración:
- [ ] Obtener credenciales de Qdrant Cloud
- [ ] Verificar que Qdrant local funciona
- [ ] Backup de datos locales

### Migración:
- [ ] Exportar colección local
- [ ] Crear colección en cloud
- [ ] Importar datos a cloud
- [ ] Verificar cantidad de puntos

### Post-migración:
- [ ] Actualizar `.env.backend`
- [ ] Actualizar `rag_agent.py`
- [ ] Probar búsquedas
- [ ] Probar desde frontend
- [ ] Monitorear performance

### Opcional (Kiro):
- [ ] Instalar MCP Qdrant
- [ ] Configurar en `mcp.json`
- [ ] Probar herramientas MCP

---

## 🚨 TROUBLESHOOTING

### Error: "Connection refused"
```bash
# Verificar URL y API key
curl -X GET 'https://tu-cluster.qdrant.io:6333' \
  --header 'api-key: tu-api-key'
```

### Error: "Collection not found"
```python
# Listar colecciones disponibles
collections = client.get_collections()
print([c.name for c in collections.collections])
```

### Error: "Timeout"
```python
# Aumentar timeout
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=60.0  # ← Aumentar a 60 segundos
)
```

---

## 💰 COSTES QDRANT CLOUD

### Free Tier:
- ✅ 1 GB de almacenamiento
- ✅ Suficiente para ~1M documentos pequeños
- ✅ Sin límite de requests

### Si superas 1 GB:
- Starter: $25/mes (5 GB)
- Standard: $95/mes (20 GB)

**Tu caso:** Con leyes de Seguridad Social, probablemente < 1 GB = **GRATIS**

---

## 📊 RESUMEN

### Opción A: API Directa (Para tu app) ⭐ RECOMENDADO
```python
# Cambiar en rag_agent.py
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),      # Cloud
    api_key=os.getenv("QDRANT_API_KEY")
)
```

### Opción B: MCP Qdrant (Para Kiro/desarrollo)
```json
// Solo para TI en Kiro
{
  "qdrant": {
    "command": "uvx",
    "args": ["mcp-server-qdrant"]
  }
}
```

**Conclusión:** Usa API directa para la app, MCP solo para desarrollo

---

**Próximo paso:** Ejecutar scripts de migración

