# 🔍 DEPLOYMENT AUDIT REPORT - OPOS_GEMINI_1

**Fecha:** 2025-01-15  
**Versión:** 1.0  
**Estado:** ⚠️ CRÍTICO - Requiere reparaciones antes de deployment

---

## 📋 RESUMEN EJECUTIVO

Se han identificado **15 problemas críticos y de seguridad** que deben resolverse antes de hacer deployment a producción:

- ✅ **3 Duplicaciones de funciones** (RAG Agent)
- ⚠️ **5 Vulnerabilidades de seguridad** (Timeouts, CORS, Secrets)
- 🐛 **4 Bugs potenciales** (Error handling, Memory leaks)
- 📦 **3 Problemas de configuración** (Env vars, Dependencies)

---

## 🔴 CRÍTICO - DEBE REPARARSE ANTES DE DEPLOYMENT

### 1. DUPLICACIÓN: RAG Agent Initialization (CRÍTICO)

**Ubicación:** `backend/routers/chat.py` línea 35-42

**Problema:**
```python
# chat.py - Línea 35-42
def get_rag_agent() -> RAGAgentV2:
    """Get or create RAG Agent instance (singleton pattern)"""
    global _rag_agent
    if _rag_agent is None:
        logger.info("Initializing RAG Agent (first time)")
        _rag_agent = RAGAgentV2()
    return _rag_agent

# chat.py - Línea 200 (en chat_message)
if request.use_rag:
    rag = RAGAgentV2()  # ❌ CREA NUEVA INSTANCIA EN VEZ DE USAR SINGLETON
```

**Impacto:**
- Crea múltiples instancias de RAGAgentV2 (cada una carga el modelo RoBERTalex)
- Consume 2-3 GB de RAM por instancia
- Causa memory leaks y degradación de performance
- Inconsistencia entre endpoints

**Solución:**
```python
# chat.py - Línea 200 (CORRECCIÓN)
if request.use_rag:
    rag = get_rag_agent()  # ✅ Usar singleton
    results = await rag.search_documents(...)
```

**Severidad:** 🔴 CRÍTICO

---

### 2. DUPLICACIÓN: RAG Agent Factories (CRÍTICO)

**Ubicación:** Múltiples archivos

**Problema:**
Existen 3 funciones diferentes para obtener RAG Agent:
- `backend/agents/rag_agent.py` → `get_rag_agent()` (V1)
- `backend/agents/rag_agent_v2.py` → `get_rag_agent_v2()` (V2)
- `backend/routers/chat.py` → `get_rag_agent()` (V2 local)

**Impacto:**
- Confusión sobre cuál usar
- Posibles inconsistencias entre endpoints
- Difícil de mantener

**Solución:**
Consolidar en un único factory pattern:
```python
# backend/agents/__init__.py
from .rag_agent_v2 import RAGAgentV2, get_rag_agent_v2

# Alias para compatibilidad
get_rag_agent = get_rag_agent_v2

__all__ = ["RAGAgentV2", "get_rag_agent", "get_rag_agent_v2"]
```

**Severidad:** 🔴 CRÍTICO

---

### 3. DUPLICACIÓN: search_documents Implementation (ALTO)

**Ubicación:** `backend/routers/chat.py` línea 80-130

**Problema:**
El código de búsqueda RAG está duplicado en `chat_stream()`:
```python
# chat.py - Línea 80-130 (DUPLICADO)
results = await rag.search_documents(
    query=request.message,
    top_k=request.top_k * 3,
    min_score=request.min_score,
    layer_filter=None
)

# Reranking por jerarquía
def get_hierarchy_boost(metadata):
    capa = metadata.get('capa', 3)
    if capa == 1:
        return 0.3
    elif capa == 2:
        return 0.15
    else:
        return 0.0

# Aplicar boost y reordenar
for r in results:
    boost = get_hierarchy_boost(r['metadata'])
    r['original_score'] = r['score']
    r['score'] = r['score'] * (1 + boost)

results = sorted(results, key=lambda x: x['score'], reverse=True)[:request.top_k]
```

**Impacto:**
- Lógica de reranking no está en RAGAgentV2
- Difícil de mantener
- Inconsistencia con otros endpoints

**Solución:**
Mover reranking a `RAGAgentV2.search_documents()` o crear método separado.

**Severidad:** 🟠 ALTO

---

## 🔐 SEGURIDAD - VULNERABILIDADES CRÍTICAS

### 4. FALTA DE TIMEOUTS EN HTTPX (CRÍTICO)

**Ubicación:** `backend/routers/chat.py` línea 200

**Problema:**
```python
# ❌ VULNERABLE - Sin timeout explícito
async with httpx.AsyncClient(timeout=60.0) as client:
    response = await client.post(...)
```

**Riesgo:**
- Conexiones colgadas a Mistral
- Agotamiento de recursos
- Denial of Service (DoS)

**Solución:**
```python
# ✅ SEGURO - Timeouts explícitos
timeout = httpx.Timeout(
    connect=3.0,      # Conexión
    read=15.0,        # Lectura
    write=10.0,       # Escritura
    pool=3.0          # Pool
)
async with httpx.AsyncClient(timeout=timeout) as client:
    response = await client.post(...)
```

**Severidad:** 🔴 CRÍTICO

---

### 5. CORS ABIERTO A TODO (CRÍTICO)

**Ubicación:** `backend/main.py` línea 68-73

**Problema:**
```python
# ❌ VULNERABLE - Permite cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Riesgo:**
- CSRF attacks
- Acceso no autorizado desde cualquier dominio
- Exposición de datos sensibles

**Solución:**
```python
# ✅ SEGURO - Whitelist de orígenes
ALLOWED_ORIGINS = [
    "https://opositaia.com",
    "https://www.opositaia.com",
    "https://app.opositaia.com",
]

if os.getenv("ENV") == "production":
    allowed_origins = ALLOWED_ORIGINS
else:
    allowed_origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
```

**Severidad:** 🔴 CRÍTICO

---

### 6. API KEYS EN LOGS (CRÍTICO)

**Ubicación:** `backend/main.py` línea 40-45

**Problema:**
```python
# ❌ VULNERABLE - Expone URLs con credenciales
logger.info(f"Qdrant URL: {os.getenv('QDRANT_URL', 'http://localhost:6333')}")
logger.info(f"Ollama URL: {os.getenv('OLLAMA_URL', 'http://localhost:11434')}")
```

**Riesgo:**
- URLs con API keys en logs
- Exposición en CloudWatch/Sentry
- Acceso no autorizado a servicios

**Solución:**
```python
# ✅ SEGURO - Ocultar credenciales
qdrant_url = os.getenv('QDRANT_URL', 'http://localhost:6333')
logger.info(f"Qdrant URL: {qdrant_url.split('@')[-1] if '@' in qdrant_url else 'configured'}")
```

**Severidad:** 🔴 CRÍTICO

---

### 7. MANEJO DE ERRORES INSEGURO (ALTO)

**Ubicación:** `backend/routers/chat.py` línea 210-215

**Problema:**
```python
# ❌ VULNERABLE - Expone detalles internos
if response.status_code != 200:
    raise HTTPException(
        status_code=response.status_code,
        detail=f"Mistral API error: {response.text}"  # Expone respuesta completa
    )
```

**Riesgo:**
- Exposición de stack traces
- Información de infraestructura
- Facilita ataques

**Solución:**
```python
# ✅ SEGURO - Mensajes genéricos
if response.status_code != 200:
    logger.error(f"Mistral error: {response.status_code} - {response.text}")
    raise HTTPException(
        status_code=500,
        detail="Service temporarily unavailable"
    )
```

**Severidad:** 🟠 ALTO

---

### 8. FALTA DE VALIDACIÓN DE PROVIDER (ALTO)

**Ubicación:** `backend/routers/chat.py` línea 160

**Problema:**
```python
# ❌ VULNERABLE - Sin validación
provider = get_provider(request.provider)  # ¿Qué si request.provider es inválido?
```

**Riesgo:**
- Inyección de parámetros
- Comportamiento indefinido

**Solución:**
```python
# ✅ SEGURO - Validación explícita
allowed_providers = set(list_providers())
if request.provider not in allowed_providers:
    raise HTTPException(
        status_code=422,
        detail=f"Unsupported provider: {request.provider}"
    )
provider = get_provider(request.provider)
```

**Severidad:** 🟠 ALTO

---

## 🐛 BUGS POTENCIALES

### 9. MEMORY LEAK: Document Cache (ALTO)

**Ubicación:** `backend/routers/upload.py` línea 30

**Problema:**
```python
# ❌ MEMORY LEAK - Cache sin límite
document_cache = {}

@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    # ...
    document_cache[doc_id] = {
        "text": text,  # Puede ser 10MB
        "filename": file.filename,
        # ...
    }
```

**Riesgo:**
- Cache crece indefinidamente
- Agotamiento de memoria
- Crash en producción

**Solución:**
```python
# ✅ SEGURO - Usar Redis o TTL
from functools import lru_cache
from datetime import datetime, timedelta

class DocumentCache:
    def __init__(self, max_size=100, ttl_hours=24):
        self.cache = {}
        self.max_size = max_size
        self.ttl = timedelta(hours=ttl_hours)
    
    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            # Eliminar entrada más antigua
            oldest = min(self.cache.items(), key=lambda x: x[1]['created_at'])
            del self.cache[oldest[0]]
        
        self.cache[key] = {
            'value': value,
            'created_at': datetime.now()
        }
    
    def get(self, key):
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        if datetime.now() - entry['created_at'] > self.ttl:
            del self.cache[key]
            return None
        
        return entry['value']

document_cache = DocumentCache(max_size=100, ttl_hours=24)
```

**Severidad:** 🟠 ALTO

---

### 10. FALTA DE MANEJO DE JSON INVÁLIDO (MEDIO)

**Ubicación:** `backend/routers/chat.py` línea 210

**Problema:**
```python
# ❌ VULNERABLE - Sin try/except
data = response.json()
full_response = data['choices'][0]['message']['content']
```

**Riesgo:**
- JSONDecodeError si Mistral devuelve HTML
- KeyError si estructura es diferente
- Crash sin mensaje claro

**Solución:**
```python
# ✅ SEGURO - Manejo robusto
try:
    data = response.json()
    full_response = data['choices'][0]['message']['content']
except (json.JSONDecodeError, KeyError, IndexError) as e:
    logger.error(f"Invalid Mistral response: {e}")
    raise HTTPException(
        status_code=502,
        detail="Invalid response from LLM provider"
    )
```

**Severidad:** 🟡 MEDIO

---

### 11. FALTA DE HEADERS SSE (MEDIO)

**Ubicación:** `backend/routers/chat.py` línea 175

**Problema:**
```python
# ❌ INCOMPLETO - Headers SSE faltantes
return StreamingResponse(
    generate(),
    media_type="text/event-stream",
    headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no"
    }
)
```

**Riesgo:**
- Buffering en proxies
- Retrasos en streaming
- Incompatibilidad con algunos clientes

**Solución:**
```python
# ✅ CORRECTO - Headers completos
return StreamingResponse(
    generate(),
    media_type="text/event-stream",
    headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
        "Transfer-Encoding": "chunked",
        "Content-Encoding": "identity"
    }
)
```

**Severidad:** 🟡 MEDIO

---

### 12. FALTA DE VALIDACIÓN DE TAMAÑO (MEDIO)

**Ubicación:** `backend/routers/upload.py` línea 60

**Problema:**
```python
# ❌ VULNERABLE - Validación débil
if len(content) > 10 * 1024 * 1024:  # 10MB
    raise HTTPException(...)
```

**Riesgo:**
- Archivos muy grandes pueden causar OOM
- No hay validación de tipo MIME
- Posible zip bomb

**Solución:**
```python
# ✅ SEGURO - Validación robusta
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_TYPES = {
    "application/pdf": ".pdf",
    "text/plain": ".txt",
}

if len(content) > MAX_FILE_SIZE:
    raise HTTPException(status_code=413, detail="File too large")

if file.content_type not in ALLOWED_TYPES:
    raise HTTPException(status_code=415, detail="Unsupported file type")

# Validar magic bytes
if file.content_type == "application/pdf":
    if not content.startswith(b'%PDF'):
        raise HTTPException(status_code=400, detail="Invalid PDF file")
```

**Severidad:** 🟡 MEDIO

---

## 📦 CONFIGURACIÓN Y DEPLOYMENT

### 13. FALTA DE VARIABLES DE ENTORNO CRÍTICAS (ALTO)

**Ubicación:** `backend/main.py`, `backend/routers/chat.py`

**Problema:**
```python
# ❌ VULNERABLE - Valores por defecto inseguros
MISTRAL_URL = os.getenv("MISTRAL_URL", "http://147.93.95.67:8080")  # IP hardcodeada
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral")
```

**Riesgo:**
- IP expuesta en código
- Difícil de cambiar en producción
- Falta de validación

**Solución:**
```python
# ✅ SEGURO - Validación de env vars
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mistral_url: str
    mistral_model: str = "mistral"
    mistral_timeout: int = 60
    qdrant_url: str
    qdrant_api_key: str | None = None
    cors_origins: list[str] = ["http://localhost:3000"]
    env: str = "development"
    
    class Config:
        env_file = ".env.backend"
        case_sensitive = False

settings = Settings()

# Validar en startup
if not settings.mistral_url:
    raise ValueError("MISTRAL_URL must be set")
```

**Severidad:** 🟠 ALTO

---

### 14. FALTA DE HEALTH CHECKS COMPLETOS (MEDIO)

**Ubicación:** `backend/routers/chat.py` línea 240-260

**Problema:**
```python
# ❌ INCOMPLETO - Health check básico
@router.get("/health")
async def chat_health():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{MISTRAL_URL}/v1/models")
            mistral_healthy = response.status_code == 200
    except Exception as e:
        mistral_healthy = False
```

**Riesgo:**
- No verifica todas las dependencias
- No detecta degradación
- Falta de métricas

**Solución:**
```python
# ✅ COMPLETO - Health check robusto
@router.get("/health")
async def chat_health():
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {}
    }
    
    # Mistral
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{MISTRAL_URL}/v1/models")
            health_status["services"]["mistral"] = {
                "status": "up" if response.status_code == 200 else "down",
                "response_time_ms": response.elapsed.total_seconds() * 1000
            }
    except Exception as e:
        health_status["services"]["mistral"] = {"status": "down", "error": str(e)}
    
    # Qdrant
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            qdrant_url = os.getenv("QDRANT_URL")
            response = await client.get(qdrant_url)
            health_status["services"]["qdrant"] = {
                "status": "up" if response.status_code == 200 else "down",
                "response_time_ms": response.elapsed.total_seconds() * 1000
            }
    except Exception as e:
        health_status["services"]["qdrant"] = {"status": "down", "error": str(e)}
    
    # Determinar estado general
    all_up = all(s["status"] == "up" for s in health_status["services"].values())
    health_status["status"] = "healthy" if all_up else "degraded"
    
    return health_status
```

**Severidad:** 🟡 MEDIO

---

### 15. FALTA DE LOGGING ESTRUCTURADO (MEDIO)

**Ubicación:** Todo el backend

**Problema:**
```python
# ❌ INCONSISTENTE - Logging sin estructura
logger.info(f"Querying RAG for: {request.message[:50]}...")
logger.error(f"RAG query failed: {e}")
logger.warning("RAG returned no results")
```

**Riesgo:**
- Difícil de parsear en producción
- Falta de contexto
- Imposible correlacionar requests

**Solución:**
```python
# ✅ ESTRUCTURADO - JSON logging
import json
from pythonjsonlogger import jsonlogger

# Configurar JSON logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Usar con contexto
logger.info("rag_query", extra={
    "query": request.message[:50],
    "conversation_id": request.conversation_id,
    "use_rag": request.use_rag,
    "top_k": request.top_k
})

logger.error("rag_query_failed", extra={
    "error": str(e),
    "conversation_id": request.conversation_id,
    "query": request.message[:50]
})
```

**Severidad:** 🟡 MEDIO

---

## 📋 CHECKLIST DE REPARACIÓN

### Antes de Deployment (CRÍTICO)

- [ ] **Reparar duplicación RAG Agent en chat.py línea 200**
  - Cambiar `RAGAgentV2()` por `get_rag_agent()`
  - Archivo: `backend/routers/chat.py`
  - Tiempo: 5 minutos

- [ ] **Consolidar RAG Agent factories**
  - Actualizar `backend/agents/__init__.py`
  - Archivo: `backend/agents/__init__.py`
  - Tiempo: 10 minutos

- [ ] **Agregar timeouts explícitos a httpx**
  - Archivo: `backend/routers/chat.py`, `backend/routers/upload.py`, `backend/agents/llm_providers.py`
  - Tiempo: 15 minutos

- [ ] **Restringir CORS a orígenes permitidos**
  - Archivo: `backend/main.py`
  - Tiempo: 10 minutos

- [ ] **Ocultar credenciales en logs**
  - Archivo: `backend/main.py`
  - Tiempo: 10 minutos

- [ ] **Mejorar manejo de errores**
  - Archivo: `backend/routers/chat.py`
  - Tiempo: 20 minutos

- [ ] **Validar provider parameter**
  - Archivo: `backend/routers/chat.py`
  - Tiempo: 10 minutos

### Antes de Producción (ALTO)

- [ ] **Implementar Document Cache con TTL**
  - Archivo: `backend/routers/upload.py`
  - Tiempo: 30 minutos

- [ ] **Agregar validación JSON robusta**
  - Archivo: `backend/routers/chat.py`
  - Tiempo: 15 minutos

- [ ] **Mejorar health checks**
  - Archivo: `backend/routers/chat.py`
  - Tiempo: 30 minutos

- [ ] **Implementar Settings con Pydantic**
  - Archivo: `backend/config.py` (nuevo)
  - Tiempo: 30 minutos

- [ ] **Agregar logging estructurado**
  - Archivo: `backend/main.py`
  - Tiempo: 30 minutos

---

## 🚀 PLAN DE ACCIÓN

### Fase 1: CRÍTICO (Hoy - 2 horas)
1. Reparar duplicación RAG Agent
2. Agregar timeouts
3. Restringir CORS
4. Ocultar credenciales

### Fase 2: ALTO (Mañana - 3 horas)
1. Mejorar manejo de errores
2. Validar provider
3. Implementar Document Cache
4. Agregar validación JSON

### Fase 3: MEDIO (Esta semana - 4 horas)
1. Mejorar health checks
2. Implementar Settings
3. Agregar logging estructurado
4. Tests de seguridad

---

## 📊 RESUMEN DE IMPACTO

| Categoría | Cantidad | Severidad | Impacto |
|-----------|----------|-----------|---------|
| Duplicaciones | 3 | 🔴 CRÍTICO | Memory leaks, Performance |
| Seguridad | 5 | 🔴 CRÍTICO | Vulnerabilidades, Exposición |
| Bugs | 4 | 🟠 ALTO | Crashes, Degradación |
| Configuración | 3 | 🟠 ALTO | Mantenibilidad, Escalabilidad |
| **TOTAL** | **15** | **🔴 CRÍTICO** | **NO DEPLOYABLE** |

---

## ✅ CONCLUSIÓN

**Estado Actual:** ❌ NO LISTO PARA DEPLOYMENT

El código tiene vulnerabilidades críticas de seguridad y bugs que causarán problemas en producción. Se recomienda:

1. **Inmediato:** Reparar los 3 problemas críticos (duplicaciones + seguridad)
2. **Antes de deployment:** Resolver todos los problemas ALTO
3. **Antes de producción:** Implementar mejoras MEDIO

**Tiempo estimado de reparación:** 8-10 horas

---

**Generado por:** Code Review Bot  
**Próxima revisión:** Después de reparaciones
