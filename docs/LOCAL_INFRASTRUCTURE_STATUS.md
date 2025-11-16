# Estado de Infraestructura Local - OpositaIA

## 📊 Resumen Ejecutivo

**Fecha**: 2025-01-16  
**Estado**: ✅ Todo funcionando  
**Costo**: $0/mes

## 🐳 Docker Containers (WSL)

### 1. Qdrant Vector Database
- **Container**: `qdrant`
- **Estado**: ✅ Running
- **Puertos**: 6333 (HTTP), 6334 (gRPC)
- **Uptime**: Recién iniciado

#### Colecciones Existentes:

**a) `boe_docs`**
- **Puntos**: 3 documentos
- **Dimensión**: 384 (all-minilm embeddings)
- **Distancia**: Cosine
- **Estado**: Green
- **Origen**: Proyecto anterior (puede limpiarse)

**b) `justicio`**
- **Puntos**: 0 documentos (vacía)
- **Dimensión**: 768 (embeddings más grandes)
- **Distancia**: Cosine
- **Estado**: Green
- **Origen**: Proyecto justicio (puede limpiarse)

### 2. Ollama (LLM Local)
- **Container**: `ollama-starter`
- **Estado**: ✅ Running (3 horas uptime)
- **Puerto**: 11434
- **API**: http://localhost:11434

#### Modelos Instalados:

**a) tinyllama:latest**
- **ID**: 2644915ede35
- **Tamaño**: 637 MB
- **Instalado**: Hace 3 meses
- **Uso**: LLM ligero para tareas simples

**b) all-minilm:latest**
- **ID**: 1b226e2802db
- **Tamaño**: 45 MB
- **Instalado**: Hace 3 meses
- **Uso**: Embeddings (dimensión 384)
- **Perfecto para**: RAG, búsqueda semántica

### 3. PostgreSQL + pgvector
- **Container**: `sim_old-db-1`
- **Estado**: ✅ Running (healthy)
- **Puerto**: 5432
- **Uptime**: 1 hora

## 🎯 Recomendaciones

### Opción 1: Limpiar y Empezar Fresco (Recomendado)

```bash
# Eliminar colecciones antiguas
curl -X DELETE http://localhost:6333/collections/boe_docs
curl -X DELETE http://localhost:6333/collections/justicio

# Crear nueva colección para OpositaIA
curl -X PUT http://localhost:6333/collections/opositaia_documents \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": {
      "size": 384,
      "distance": "Cosine"
    }
  }'
```

### Opción 2: Reutilizar Colección Existente

```bash
# Limpiar boe_docs (mantener estructura)
curl -X POST http://localhost:6333/collections/boe_docs/points/delete \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "must": [
        {"key": "id", "match": {"any": []}}
      ]
    }
  }'
```

### Opción 3: Instalar Más Modelos en Ollama

```bash
# Modelos recomendados para OpositaIA

# 1. Mistral 7B (mejor que tinyllama)
wsl docker exec ollama-starter ollama pull mistral

# 2. Nomic Embed Text (embeddings mejorados)
wsl docker exec ollama-starter ollama pull nomic-embed-text

# 3. Phi-3 Mini (rápido y eficiente)
wsl docker exec ollama-starter ollama pull phi3:mini

# 4. Llama 3.2 (más reciente)
wsl docker exec ollama-starter ollama pull llama3.2
```

## 📋 Comandos Útiles

### Qdrant

```bash
# Ver todas las colecciones
curl http://localhost:6333/collections

# Ver detalles de una colección
curl http://localhost:6333/collections/boe_docs

# Contar puntos
curl http://localhost:6333/collections/boe_docs/points/count

# Buscar puntos
curl -X POST http://localhost:6333/collections/boe_docs/points/search \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, ...],
    "limit": 5
  }'

# Eliminar colección
curl -X DELETE http://localhost:6333/collections/boe_docs

# Crear colección
curl -X PUT http://localhost:6333/collections/nueva_coleccion \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": {
      "size": 384,
      "distance": "Cosine"
    }
  }'
```

### Ollama

```bash
# Listar modelos
wsl docker exec ollama-starter ollama list

# Descargar modelo
wsl docker exec ollama-starter ollama pull mistral

# Eliminar modelo
wsl docker exec ollama-starter ollama rm tinyllama

# Generar texto
wsl docker exec ollama-starter ollama run tinyllama "Hola"

# Generar embeddings
curl http://localhost:11434/api/embeddings \
  -d '{
    "model": "all-minilm",
    "prompt": "Texto a embedear"
  }'
```

### Docker

```bash
# Ver containers corriendo
wsl docker ps

# Iniciar container
wsl docker start qdrant
wsl docker start ollama-starter

# Detener container
wsl docker stop qdrant

# Ver logs
wsl docker logs qdrant
wsl docker logs ollama-starter

# Reiniciar container
wsl docker restart qdrant
```

## 🔧 Configuración para OpositaIA

### 1. Variables de Entorno

```bash
# .env.backend
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=opositaia_documents
OLLAMA_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=all-minilm
OLLAMA_LLM_MODEL=tinyllama
```

### 2. Crear Colección OpositaIA

```bash
curl -X PUT http://localhost:6333/collections/opositaia_documents \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": {
      "size": 384,
      "distance": "Cosine"
    },
    "optimizers_config": {
      "indexing_threshold": 10000
    },
    "hnsw_config": {
      "m": 16,
      "ef_construct": 100
    }
  }'
```

### 3. Probar Embeddings

```python
import requests

# Generar embedding
response = requests.post(
    'http://localhost:11434/api/embeddings',
    json={
        'model': 'all-minilm',
        'prompt': 'Incapacidad temporal en la Seguridad Social'
    }
)
embedding = response.json()['embedding']
print(f"Dimensión: {len(embedding)}")  # Debe ser 384
```

## 📊 Uso de Recursos

### Actual:
- **Qdrant**: ~100 MB RAM
- **Ollama**: ~500 MB RAM (idle)
- **PostgreSQL**: ~50 MB RAM
- **Total**: ~650 MB RAM

### Con Modelos Adicionales:
- **Mistral 7B**: +4 GB RAM cuando activo
- **Nomic Embed**: +200 MB RAM
- **Total máximo**: ~5 GB RAM

## ✅ Checklist de Limpieza

Antes de empezar con OpositaIA:

- [ ] Decidir si limpiar colecciones antiguas
- [ ] Crear colección `opositaia_documents`
- [ ] Verificar que all-minilm funciona
- [ ] Considerar instalar modelos adicionales
- [ ] Configurar variables de entorno
- [ ] Probar conexión desde backend

## 🎯 Decisión Recomendada

**Para OpositaIA MVP**:

1. ✅ **Mantener**: all-minilm (embeddings)
2. ✅ **Mantener**: tinyllama (LLM simple)
3. ✅ **Limpiar**: Colecciones antiguas
4. ✅ **Crear**: Nueva colección `opositaia_documents`
5. 🤔 **Opcional**: Instalar mistral (mejor que tinyllama)

**Comandos para ejecutar**:
```bash
# 1. Limpiar colecciones antiguas
curl -X DELETE http://localhost:6333/collections/boe_docs
curl -X DELETE http://localhost:6333/collections/justicio

# 2. Crear colección OpositaIA
curl -X PUT http://localhost:6333/collections/opositaia_documents \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 384, "distance": "Cosine"}}'

# 3. Verificar
curl http://localhost:6333/collections
```

---

**Última actualización**: 2025-01-16  
**Estado**: ✅ Infraestructura lista  
**Costo**: $0/mes
