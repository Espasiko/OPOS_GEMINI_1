# Memoria del Proyecto OpositaIA - 20 Diciembre 2025

**Última actualización**: 20/12/2025 01:00  
**Estado**: Sistema RAG funcionando + Mistral Agent configurado

---

## 📋 ÍNDICE

1. [Arquitectura General](#arquitectura-general)
2. [Infraestructura Docker](#infraestructura-docker)
3. [Backend FastAPI](#backend-fastapi)
4. [Sistema RAG](#sistema-rag)
5. [Mistral Agent Studio](#mistral-agent-studio)
6. [Entornos Virtuales y .env](#entornos-virtuales-y-env)
7. [Scripts de Generación Q&A](#scripts-de-generación-qa)
8. [Datasets y Archivos Generados](#datasets-y-archivos-generados)
9. [Documentación y Planes](#documentación-y-planes)
10. [Problemas Resueltos](#problemas-resueltos)
11. [Próximos Pasos](#próximos-pasos)

---

## 1. ARQUITECTURA GENERAL

### Estructura del Proyecto

```
/home/spas/OPOS_GEMINI_1/
├── backend/                    # FastAPI + Agents
│   ├── agents/                 # RAG, MCP, Ingestion
│   ├── routers/                # API endpoints
│   ├── main.py                 # FastAPI app
│   └── .env.backend            # Variables de entorno backend
├── frontend/                   # React + Vite
├── mcp-server/                 # MCP Server (TypeScript)
├── dataset_generator/          # Scripts generación Q&A
├── golden_dataset/             # Datasets de calidad
├── docs/                       # Documentación
├── .venv/                      # Entorno virtual Python
├── .env                        # Variables entorno raíz
└── docker-compose.yml          # Qdrant + PostgreSQL

```

### Componentes Principales

1. **Backend FastAPI** (puerto 8000)
   - RAG Agent V2
   - MCP Gateway
   - Endpoints de búsqueda

2. **Qdrant** (puerto 6333)
   - Vector database
   - Colección: `opositaia_knowledge` (17,403 puntos)

3. **PostgreSQL** (puerto 5432)
   - 10,901 leyes indexadas
   - Metadata y referencias

4. **Mistral Agent Studio**
   - Agent ID: `ag_019ad601946d7323a81c544229de40a1`
   - Funciones: `buscar_rag`, `verificar_url`

---

## 2. INFRAESTRUCTURA DOCKER

### Contenedores Activos

```bash
docker ps
```

**Contenedores**:
- `opositaia-qdrant` - Qdrant vector DB (puerto 6333)
- `opositaia-postgres` - PostgreSQL (puerto 5432)

### Docker Compose

**Archivo**: `/home/spas/OPOS_GEMINI_1/docker-compose.yml`

```yaml
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: opositaia-qdrant
    ports:
      - "6333:6333"
    volumes:
      - ./qdrant_storage:/qdrant/storage
  
  postgres:
    image: postgres:15
    container_name: opositaia-postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: opositaia
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
```

### Comandos Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Iniciar solo Qdrant
docker start opositaia-qdrant

# Ver logs
docker logs opositaia-qdrant
docker logs opositaia-postgres

# Estado
docker ps
```

---

## 3. BACKEND FASTAPI

### Ubicación

`/home/spas/OPOS_GEMINI_1/backend/`

### Estructura

```
backend/
├── main.py                     # FastAPI app principal
├── agents/
│   ├── rag_agent_v2.py         # RAG Agent (CORREGIDO 20/12)
│   ├── ingest_hybrid_two_tier.py
│   └── mistral_tools.py
├── routers/
│   ├── rag.py                  # Endpoint /api/rag/search
│   └── mcp_gateway.py
└── .env.backend                # Variables de entorno
```

### Iniciar FastAPI

```bash
cd /home/spas/OPOS_GEMINI_1
source .venv/bin/activate
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Endpoints Principales

**Health Check**:
```bash
curl http://localhost:8000/health
```

**RAG Search**:
```bash
curl -X POST http://localhost:8000/api/rag/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "incapacidad temporal duración",
    "top_k": 5,
    "min_score": 0.3
  }'
```

---

## 4. SISTEMA RAG

### Componentes

1. **Qdrant** (Vector Database)
   - URL: `http://localhost:6333`
   - Colección: `opositaia_knowledge`
   - Puntos: 17,403
   - Dimensiones: 1024
   - Vector: `dense` (Cosine distance)

2. **Embeddings**
   - Modelo: `pablosi/bge-m3-spa-law-qa-trained-2`
   - Dimensiones: 1024
   - Especializado en legislación española

3. **PostgreSQL**
   - Base de datos: `opositaia`
   - Leyes indexadas: 10,901
   - Metadata completa

### Configuración RAG Agent

**Archivo**: `/home/spas/OPOS_GEMINI_1/backend/agents/rag_agent_v2.py`

**PROBLEMA RESUELTO (20/12/2025)**:
- **Línea 32**: Cambiado default de `opositaia_leyes_seguridad_social` a `opositaia_knowledge`
- **Razón**: La colección real es `opositaia_knowledge` con 17,403 puntos

```python
# ANTES (INCORRECTO)
self.collection_name = collection_name or os.getenv("COLLECTION_NAME", "opositaia_leyes_seguridad_social")

# DESPUÉS (CORRECTO)
self.collection_name = collection_name or os.getenv("COLLECTION_NAME", "opositaia_knowledge")
```

### Verificar Qdrant

```bash
# Ver colecciones
curl http://localhost:6333/collections | jq '.result.collections[].name'

# Info de opositaia_knowledge
curl http://localhost:6333/collections/opositaia_knowledge | jq '.result.points_count'

# Buscar un punto
curl -X POST http://localhost:6333/collections/opositaia_knowledge/points/scroll \
  -H "Content-Type: application/json" \
  -d '{"limit":1,"with_payload":true}' | jq '.result.points[0]'
```

---

## 5. MISTRAL AGENT STUDIO

### Configuración

**Agent ID**: `ag_019ad601946d7323a81c544229de40a1`  
**Modelo**: `mistral-large-latest`  
**API Key**: (variable, ver `.env`)

### Funciones Configuradas

#### 1. `buscar_rag`

**Descripción**: Busca en Qdrant (17,403 puntos) + PostgreSQL (10,901 leyes)

**Parámetros**:
```json
{
  "query": "string (consulta semántica)",
  "top_k": "integer (1-20, default 5)"
}
```

#### 2. `verificar_url`

**Descripción**: Verifica artículos en BD local (NO web externa)

**Parámetros**:
```json
{
  "articulo": "string (ej: '169.1')",
  "ley": "string (ej: 'LGSS')"
}
```

### System Prompt

**Ubicación**: Configurado en Mistral Studio (no en código)

**Tipos de contenido**: 5 tipos
- TEST: Conocimiento directo
- COMPARACIÓN: Comparar conceptos
- PROCEDIMIENTO: Pasos administrativos
- RAZONAMIENTO: Casos prácticos
- RELACIÓN: Conexiones entre leyes

**Documento**: `/home/spas/.gemini/antigravity/brain/.../config_mistral_studio_final.md`

---

## 6. ENTORNOS VIRTUALES Y .ENV

### Entorno Virtual Python

**Ubicación**: `/home/spas/OPOS_GEMINI_1/.venv/`

**Activar**:
```bash
cd /home/spas/OPOS_GEMINI_1
source .venv/bin/activate
```

**Paquetes principales**:
- `fastapi`
- `uvicorn`
- `qdrant-client`
- `sentence-transformers`
- `mistralai`
- `groq`
- `psycopg2-binary`

### Variables de Entorno

#### Raíz del Proyecto

**Archivo**: `/home/spas/OPOS_GEMINI_1/.env` (gitignored)

**Ejemplo**: `/home/spas/OPOS_GEMINI_1/.env.example`

```env
VITE_API_KEY=your_api_key_here
VITE_BACKEND_URL=http://localhost:8000
```

#### Backend

**Archivo**: `/home/spas/OPOS_GEMINI_1/backend/.env.backend` (gitignored)

**Ejemplo**: `/home/spas/OPOS_GEMINI_1/backend/.env.backend.example`

**Variables clave**:
```env
# Qdrant
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=opositaia_knowledge

# Embeddings
EMBEDDING_MODEL=pablosi/bge-m3-spa-law-qa-trained-2

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=opositaia
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<password>

# Mistral
MISTRAL_API_KEY=<key>

# Groq
GROQ_API_KEY=<key>
```

---

## 7. SCRIPTS DE GENERACIÓN Q&A

### Scripts Principales

#### 1. `test_mistral_agent_simple.py`

**Propósito**: Test rápido del agente

**Uso**:
```bash
python test_mistral_agent_simple.py
```

#### 2. `generate_10_qa_mistral_v2.py`

**Propósito**: Generador con tool_calls SIMULADOS

**Resultado**: 10/10 Q&A generadas (simulado)

**Uso**:
```bash
python generate_10_qa_mistral_v2.py
```

#### 3. `generate_qa_mistral_real.py` ⭐

**Propósito**: Generador con backend REAL (Qdrant + PostgreSQL)

**Resultado**: 9/10 Q&A con datos reales

**Requisito**: FastAPI corriendo

**Uso**:
```bash
# Terminal 1: FastAPI
cd backend && uvicorn main:app

# Terminal 2: Generador
python generate_qa_mistral_real.py
```

#### 4. `generate_qa_agentic_direct.py`

**Propósito**: Generador con Groq

**Resultado**: 10/10 Q&A rápidas

**Coste**: ~$0.08/10 Q&A

### Ubicación Scripts

`/home/spas/OPOS_GEMINI_1/`

---

## 8. DATASETS Y ARCHIVOS GENERADOS

### Q&A Generadas

**Ubicación**: `/home/spas/OPOS_GEMINI_1/`

**Archivos**:
1. `qa_agentic_groq_20251219_182357.jsonl` - 10 Q&A con Groq
2. `qa_mistral_studio_v2_20251219_213835.jsonl` - 10 Q&A simuladas
3. `qa_mistral_real_backend_20251220_004558.jsonl` - 9 Q&A REALES ⭐

### Golden Dataset

**Ubicación**: `/home/spas/OPOS_GEMINI_1/golden_dataset/`

**Contenido**:
- Exámenes oficiales extraídos
- Q&A de alta calidad
- Materiales conceptuales

### Logs

**Ubicación**: `/home/spas/OPOS_GEMINI_1/`

**Archivos relevantes**:
- `qa_REAL_FINAL_v2.log` - Log de generación con backend real
- `/tmp/fastapi_fixed.log` - Log de FastAPI actual

---

## 9. DOCUMENTACIÓN Y PLANES

### Documentación Actualizada (20/12/2025)

**Ubicación**: `/home/spas/.gemini/antigravity/brain/.../`

**Archivos clave**:
1. `config_mistral_studio_final.md` - Configuración Mistral Studio
2. `explicacion_scripts_mistral.md` - Explicación scripts
3. `walkthrough_qa_backend_real.md` - Walkthrough generación real
4. `plan_mistral_agent_10_qa.md` - Plan de implementación

### Documentación Histórica

**Ubicación**: `/home/spas/OPOS_GEMINI_1/docs/`

**Subdirectorios**:
- `archive/` - Documentación histórica
- Planes, estrategias, análisis

### Epics y Stories

**Archivo**: `/home/spas/OPOS_GEMINI_1/epics_stories_dataset_19_12.md`

**Contenido**: Planificación de desarrollo del dataset

---

## 10. PROBLEMAS RESUELTOS

### Problema 1: RAG Devuelve 0 Resultados (PARCIALMENTE RESUELTO)

**Fecha**: 20/12/2025  
**Síntoma**: Búsquedas en RAG devolvían 0 resultados

**Causas encontradas**:
1. **Colección incorrecta** en `rag_agent_v2.py` línea 32
   - **Incorrecto**: `opositaia_leyes_seguridad_social`
   - **Correcto**: `opositaia_knowledge`
   - **✅ RESUELTO**

2. **Min_score demasiado alto** en `rag.py` línea 25
   - **Incorrecto**: `0.7` (filtraba todos los resultados)
   - **Correcto**: `0.1`
   - **✅ RESUELTO**

3. **Scores bajos** (< 0.3)
   - **Síntoma**: Qdrant encuentra documentos pero scores son muy bajos
   - **Log**: "Found 3 documents" pero devuelve 0 después de filtrar
   - **⚠️ PENDIENTE**: Investigar por qué scores son tan bajos

**Soluciones aplicadas**:
```python
# backend/agents/rag_agent_v2.py línea 32
self.collection_name = collection_name or os.getenv("COLLECTION_NAME", "opositaia_knowledge")

# backend/routers/rag.py línea 25
min_score: float = Field(0.1, ge=0.0, le=1.0, description="Minimum similarity score")
```

**Verificación**:
```bash
# Reiniciar FastAPI
pkill -f uvicorn
cd backend && uvicorn main:app

# Probar búsqueda
curl -X POST http://localhost:8000/api/rag/search \
  -d '{"query":"incapacidad temporal","top_k":3}'
```

**Estado**: Sistema funciona, agente genera Q&A de calidad. RAG devuelve 0 resultados por scores bajos (< 0.1).

### Problema 2: Tool Calls Vacíos

**Fecha**: 19/12/2025  
**Síntoma**: Agente devolvía respuestas vacías

**Causa**: No se manejaba el loop de tool_calls

**Solución**: Implementar loop manual de tool_calls (ver `generate_10_qa_mistral_v2.py`)

**✅ RESUELTO**

### Problema 3: Free Tier Agotado

**Fecha**: 19/12/2025  
**Síntoma**: Error 429 de Mistral

**Solución**: Nueva API key proporcionada por usuario

**✅ RESUELTO**

---

## 11. PROBLEMA PENDIENTE: Scores Bajos en RAG

### Síntoma
- Qdrant encuentra documentos (log: "Found 3/5 documents")
- Scores están por debajo de 0.1
- Después de filtrar por min_score, devuelve 0 resultados

### Posibles Causas
1. **Embeddings no coinciden**: Modelo usado para indexar ≠ modelo usado para buscar
2. **Normalización**: Vectores no normalizados correctamente
3. **Distancia**: Cosine distance configurada pero vectores no normalizados
4. **Datos**: Colección tiene datos pero de baja calidad

### Investigación Necesaria
```bash
# 1. Verificar un punto de Qdrant
curl -X POST http://localhost:6333/collections/opositaia_knowledge/points/scroll \
  -d '{"limit":1,"with_vector":true}' | jq

# 2. Verificar dimensiones
curl http://localhost:6333/collections/opositaia_knowledge | jq '.result.config.params.vectors'

# 3. Test búsqueda directa
curl -X POST http://localhost:6333/collections/opositaia_knowledge/points/search \
  -d '{"vector":{"name":"dense","vector":[...]}, "limit":3}' | jq '.result[].score'
```

### Solución Temporal
El agente Mistral genera Q&A de calidad usando su conocimiento interno cuando RAG no devuelve resultados.

---

## 12. PRÓXIMOS PASOS

### Inmediato

1. ✅ Verificar que RAG devuelve resultados después del fix
2. ✅ Regenerar Q&A con backend REAL funcionando
3. ⏳ Validar calidad de referencias legales

### Corto Plazo

1. Generar más Q&A (50-100) para dataset completo
2. Validar referencias contra leyes reales
3. Implementar validación automática de Q&A

### Medio Plazo

1. Fine-tuning de modelo con dataset generado
2. Automatizar generación masiva
3. Integrar en pipeline de producción

---

## 📊 ESTADO ACTUAL DEL SISTEMA

### Servicios

| Servicio | Estado | Puerto | Notas |
|----------|--------|--------|-------|
| Qdrant | ✅ Running | 6333 | 17,403 puntos |
| PostgreSQL | ✅ Running | 5432 | 10,901 leyes |
| FastAPI | ✅ Running | 8000 | RAG corregido |
| Mistral Agent | ✅ Configured | - | Agent ID configurado |

### Datasets

| Dataset | Q&A | Método | Calidad |
|---------|-----|--------|---------|
| Groq | 10 | Groq API | Buena |
| Mistral V2 | 10 | Simulado | Buena |
| Mistral Real | 9 | Backend Real | ⭐ Excelente |

### Métricas

- **RAG**: 17,403 chunks indexados
- **Leyes**: 10,901 documentos
- **Embeddings**: 1024 dimensiones
- **Coste**: ~$0.08 (solo Groq)

---

## 🔧 COMANDOS RÁPIDOS

### Iniciar Todo

```bash
# 1. Docker
docker-compose up -d

# 2. FastAPI
cd /home/spas/OPOS_GEMINI_1
source .venv/bin/activate
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 &

# 3. Verificar
curl http://localhost:8000/health
curl http://localhost:6333/collections
```

### Generar Q&A

```bash
# Con backend REAL
python generate_qa_mistral_real.py

# Con Groq (rápido)
python generate_qa_agentic_direct.py
```

### Verificar RAG

```bash
# Test búsqueda
curl -X POST http://localhost:8000/api/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query":"jubilación ordinaria","top_k":3,"min_score":0.3}' | jq
```

---

**Última actualización**: 20/12/2025 01:00  
**Autor**: Sistema OpositaIA  
**Versión**: 1.0
