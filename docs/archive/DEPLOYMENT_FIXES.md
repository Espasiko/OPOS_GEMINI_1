# 🔧 DEPLOYMENT FIXES - CÓDIGO CORREGIDO

Este documento contiene el código corregido para todos los problemas identificados.

---

## FIX #1: Duplicación RAG Agent en chat.py

**Archivo:** `backend/routers/chat.py`  
**Línea:** 200  
**Severidad:** 🔴 CRÍTICO

### Antes (INCORRECTO):
```python
@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Chat sin streaming"""
    full_response = ""
    sources = []
    
    try:
        # Consultar RAG
        if request.use_rag:
            rag = RAGAgentV2()  # ❌ CREA NUEVA INSTANCIA
            results = await rag.search_documents(...)
```

### Después (CORRECTO):
```python
@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Chat sin streaming"""
    full_response = ""
    sources = []
    
    try:
        # Consultar RAG
        if request.use_rag:
            rag = get_rag_agent()  # ✅ USA SINGLETON
            results = await rag.search_documents(...)
```

---

## FIX #2: Consolidar RAG Agent Factories

**Archivo:** `backend/agents/__init__.py`  
**Severidad:** 🔴 CRÍTICO

### Antes (INCORRECTO):
```python
from .rag_agent import RAGAgent, get_rag_agent

__all__ = ["RAGAgent", "get_rag_agent"]
```

### Después (CORRECTO):
```python
from .rag_agent import RAGAgent, get_rag_agent
from .rag_agent_v2 import RAGAgentV2, get_rag_agent_v2

# Alias para compatibilidad - usar V2 como default
get_rag_agent = get_rag_agent_v2

__all__ = [
    "RAGAgent",
    "RAGAgentV2",
    "get_rag_agent",
    "get_rag_agent_v2"
]
```

---

## FIX #3: Agregar Timeouts Explícitos

**Archivo:** `backend/routers/chat.py`  
**Línea:** 200  
**Severidad:** 🔴 CRÍTICO

### Antes (VULNERABLE):
```python
async with httpx.AsyncClient(timeout=60.0) as client:
    response = await client.post(
        f"{MISTRAL_URL}/v1/chat/completions",
        json={...}
    )
```

### Después (SEGURO):
```python
# Definir timeouts explícitos
timeout = httpx.Timeout(
    connect=3.0,      # Conexión
    read=15.0,        # Lectura
    write=10.0,       # Escritura
    pool=3.0          # Pool
)

async with httpx.AsyncClient(timeout=timeout) as client:
    response = await client.post(
        f"{MISTRAL_URL}/v1/chat/completions",
        json={...}
    )
```

**Aplicar también en:**
- `backend/routers/upload.py` línea 120
- `backend/agents/llm_providers.py` (todos los providers)

---

## FIX #4: Restringir CORS

**Archivo:** `backend/main.py`  
**Línea:** 68-73  
**Severidad:** 🔴 CRÍTICO

### Antes (VULNERABLE):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Después (SEGURO):
```python
# Configurar CORS según ambiente
if os.getenv("ENV") == "production":
    allowed_origins = [
        "https://opositaia.com",
        "https://www.opositaia.com",
        "https://app.opositaia.com",
    ]
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)
```

---

## FIX #5: Ocultar Credenciales en Logs

**Archivo:** `backend/main.py`  
**Línea:** 40-45  
**Severidad:** 🔴 CRÍTICO

### Antes (VULNERABLE):
```python
logger.info(f"Embedding Model: {os.getenv('EMBEDDING_MODEL', 'PlanTL-GOB-ES/RoBERTalex')}")
logger.info(f"Qdrant URL: {os.getenv('QDRANT_URL', 'http://localhost:6333')}")
logger.info(f"Ollama URL: {os.getenv('OLLAMA_URL', 'http://localhost:11434')}")
```

### Después (SEGURO):
```python
def mask_url(url: str) -> str:
    """Oculta credenciales en URLs"""
    if not url:
        return "not configured"
    if "@" in url:
        # URL con credenciales: user:pass@host
        return url.split("@")[-1]
    return url

logger.info(f"Embedding Model: configured")
logger.info(f"Qdrant URL: {mask_url(os.getenv('QDRANT_URL'))}")
logger.info(f"Ollama URL: {mask_url(os.getenv('OLLAMA_URL'))}")
```

---

## FIX #6: Mejorar Manejo de Errores

**Archivo:** `backend/routers/chat.py`  
**Línea:** 210-215  
**Severidad:** 🟠 ALTO

### Antes (VULNERABLE):
```python
if response.status_code != 200:
    raise HTTPException(
        status_code=response.status_code,
        detail=f"Mistral API error: {response.text}"  # Expone detalles
    )
```

### Después (SEGURO):
```python
if response.status_code != 200:
    # Log detallado internamente
    logger.error(
        "mistral_api_error",
        extra={
            "status_code": response.status_code,
            "response": response.text[:500],  # Limitar
            "conversation_id": request.conversation_id
        }
    )
    # Respuesta genérica al cliente
    raise HTTPException(
        status_code=502,
        detail="Service temporarily unavailable"
    )
```

---

## FIX #7: Validar Provider Parameter

**Archivo:** `backend/routers/chat.py`  
**Línea:** 160  
**Severidad:** 🟠 ALTO

### Antes (VULNERABLE):
```python
provider = get_provider(request.provider)
```

### Después (SEGURO):
```python
# Validar provider
allowed_providers = {p["id"] for p in list_providers()}
if request.provider not in allowed_providers:
    raise HTTPException(
        status_code=422,
        detail=f"Unsupported provider: {request.provider}. Allowed: {', '.join(allowed_providers)}"
    )

provider = get_provider(request.provider)
```

---

## FIX #8: Implementar Document Cache con TTL

**Archivo:** `backend/routers/upload.py`  
**Línea:** 30  
**Severidad:** 🟠 ALTO

### Antes (MEMORY LEAK):
```python
# Caché temporal de documentos (en producción usar Redis)
document_cache = {}

@router.post("/file", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    # ...
    document_cache[doc_id] = {
        "text": text,
        "filename": file.filename,
        "content_type": file.content_type,
        "pages": pages
    }
```

### Después (SEGURO):
```python
from datetime import datetime, timedelta
from typing import Dict, Any

class TTLCache:
    """Cache con Time-To-Live y límite de tamaño"""
    
    def __init__(self, max_size: int = 100, ttl_hours: int = 24):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl = timedelta(hours=ttl_hours)
    
    def set(self, key: str, value: Any) -> None:
        """Agregar item al cache"""
        # Limpiar expirados
        self._cleanup_expired()
        
        # Si está lleno, eliminar el más antiguo
        if len(self.cache) >= self.max_size:
            oldest_key = min(
                self.cache.keys(),
                key=lambda k: self.cache[k]["created_at"]
            )
            del self.cache[oldest_key]
            logger.info(f"Evicted cache entry: {oldest_key}")
        
        self.cache[key] = {
            "value": value,
            "created_at": datetime.now()
        }
    
    def get(self, key: str) -> Any | None:
        """Obtener item del cache"""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        if datetime.now() - entry["created_at"] > self.ttl:
            del self.cache[key]
            logger.info(f"Cache entry expired: {key}")
            return None
        
        return entry["value"]
    
    def delete(self, key: str) -> bool:
        """Eliminar item del cache"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def _cleanup_expired(self) -> None:
        """Limpiar entradas expiradas"""
        now = datetime.now()
        expired_keys = [
            k for k, v in self.cache.items()
            if now - v["created_at"] > self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def size(self) -> int:
        """Obtener tamaño del cache"""
        return len(self.cache)

# Instanciar cache
document_cache = TTLCache(max_size=100, ttl_hours=24)

@router.post("/file", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    # ...
    document_cache.set(doc_id, {
        "text": text,
        "filename": file.filename,
        "content_type": file.content_type,
        "pages": pages
    })
```

---

## FIX #9: Agregar Validación JSON Robusta

**Archivo:** `backend/routers/chat.py`  
**Línea:** 210  
**Severidad:** 🟡 MEDIO

### Antes (VULNERABLE):
```python
data = response.json()
full_response = data['choices'][0]['message']['content']
```

### Después (SEGURO):
```python
try:
    data = response.json()
    
    # Validar estructura
    if not isinstance(data, dict):
        raise ValueError("Response is not a JSON object")
    
    choices = data.get('choices', [])
    if not choices or not isinstance(choices, list):
        raise ValueError("Invalid choices in response")
    
    message = choices[0].get('message', {})
    if not isinstance(message, dict):
        raise ValueError("Invalid message structure")
    
    full_response = message.get('content', '')
    if not full_response:
        raise ValueError("Empty content in response")
        
except (json.JSONDecodeError, ValueError, KeyError, IndexError, TypeError) as e:
    logger.error(
        "invalid_mistral_response",
        extra={
            "error": str(e),
            "response_text": response.text[:500],
            "status_code": response.status_code
        }
    )
    raise HTTPException(
        status_code=502,
        detail="Invalid response from LLM provider"
    )
```

---

## FIX #10: Mejorar Health Checks

**Archivo:** `backend/routers/chat.py`  
**Línea:** 240-260  
**Severidad:** 🟡 MEDIO

### Antes (INCOMPLETO):
```python
@router.get("/health")
async def chat_health():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{MISTRAL_URL}/v1/models")
            mistral_healthy = response.status_code == 200
    except Exception as e:
        mistral_healthy = False
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
            response = await client.get(qdrant_url)
            rag_healthy = response.status_code == 200
    except:
        rag_healthy = False
    
    return {
        "status": "healthy" if (mistral_healthy and rag_healthy) else "degraded",
        "mistral": "up" if mistral_healthy else "down",
        "rag": "up" if rag_healthy else "down",
    }
```

### Después (COMPLETO):
```python
@router.get("/health")
async def chat_health():
    """Health check completo del servicio de chat"""
    from datetime import datetime
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {},
        "version": "1.0.0"
    }
    
    # Verificar Mistral
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            start = datetime.now()
            response = await client.get(f"{MISTRAL_URL}/v1/models")
            elapsed = (datetime.now() - start).total_seconds() * 1000
            
            health_status["services"]["mistral"] = {
                "status": "up" if response.status_code == 200 else "down",
                "response_time_ms": round(elapsed, 2),
                "status_code": response.status_code
            }
    except httpx.ConnectError as e:
        health_status["services"]["mistral"] = {
            "status": "down",
            "error": "connection_failed"
        }
    except httpx.TimeoutException:
        health_status["services"]["mistral"] = {
            "status": "down",
            "error": "timeout"
        }
    except Exception as e:
        health_status["services"]["mistral"] = {
            "status": "down",
            "error": str(e)[:100]
        }
    
    # Verificar Qdrant
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
            start = datetime.now()
            response = await client.get(qdrant_url)
            elapsed = (datetime.now() - start).total_seconds() * 1000
            
            health_status["services"]["qdrant"] = {
                "status": "up" if response.status_code == 200 else "down",
                "response_time_ms": round(elapsed, 2),
                "status_code": response.status_code
            }
    except httpx.ConnectError:
        health_status["services"]["qdrant"] = {
            "status": "down",
            "error": "connection_failed"
        }
    except httpx.TimeoutException:
        health_status["services"]["qdrant"] = {
            "status": "down",
            "error": "timeout"
        }
    except Exception as e:
        health_status["services"]["qdrant"] = {
            "status": "down",
            "error": str(e)[:100]
        }
    
    # Determinar estado general
    all_up = all(
        s.get("status") == "up"
        for s in health_status["services"].values()
    )
    health_status["status"] = "healthy" if all_up else "degraded"
    
    return health_status
```

---

## FIX #11: Crear Config con Pydantic

**Archivo:** `backend/config.py` (NUEVO)  
**Severidad:** 🟡 MEDIO

```python
"""
Configuration management for OpositAIA Backend
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Environment
    env: str = "development"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Mistral
    mistral_url: str
    mistral_model: str = "mistral"
    mistral_timeout: int = 60
    
    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    qdrant_collection: str = "opositaia_leyes_seguridad_social"
    
    # Embedding
    embedding_model: str = "PlanTL-GOB-ES/RoBERTalex"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # API Keys
    groq_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    cohere_api_key: Optional[str] = None
    hf_token: Optional[str] = None
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "opositaia"
    postgres_user: str = "postgres"
    postgres_password: str
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env.backend"
        case_sensitive = False
        extra = "ignore"
    
    def validate_production(self) -> None:
        """Validar configuración para producción"""
        if self.env == "production":
            if not self.mistral_url:
                raise ValueError("MISTRAL_URL must be set in production")
            if not self.postgres_password:
                raise ValueError("POSTGRES_PASSWORD must be set in production")
            if self.debug:
                raise ValueError("DEBUG must be False in production")
            if self.cors_origins == ["http://localhost:3000"]:
                raise ValueError("CORS_ORIGINS must be configured for production")

# Instancia global
settings = Settings()

# Validar en startup
if settings.env == "production":
    settings.validate_production()
```

---

## FIX #12: Agregar Logging Estructurado

**Archivo:** `backend/main.py`  
**Severidad:** 🟡 MEDIO

### Agregar al inicio:
```python
import logging
import json
from pythonjsonlogger import jsonlogger

def setup_logging():
    """Configurar logging estructurado en JSON"""
    
    # Logger root
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Handler para stdout
    handler = logging.StreamHandler()
    
    # Formatter JSON
    formatter = jsonlogger.JsonFormatter(
        fmt='%(timestamp)s %(level)s %(name)s %(message)s',
        timestamp=True
    )
    handler.setFormatter(formatter)
    
    # Agregar handler
    root_logger.addHandler(handler)
    
    return root_logger

# Llamar en startup
logger = setup_logging()

# Usar en código:
logger.info("rag_query", extra={
    "query": request.message[:50],
    "conversation_id": request.conversation_id,
    "use_rag": request.use_rag,
    "top_k": request.top_k
})
```

---

## 📋 ORDEN DE APLICACIÓN

1. **Inmediato (30 min):**
   - FIX #1: Duplicación RAG Agent
   - FIX #3: Timeouts
   - FIX #4: CORS
   - FIX #5: Credenciales en logs

2. **Hoy (1 hora):**
   - FIX #6: Manejo de errores
   - FIX #7: Validar provider
   - FIX #9: Validación JSON

3. **Esta semana (2 horas):**
   - FIX #2: Consolidar factories
   - FIX #8: Document Cache
   - FIX #10: Health checks
   - FIX #11: Config
   - FIX #12: Logging

---

## ✅ VERIFICACIÓN

Después de aplicar los fixes:

```bash
# 1. Ejecutar tests
pytest backend/tests/ -v

# 2. Verificar health
curl http://localhost:8000/chat/health

# 3. Verificar CORS
curl -H "Origin: http://localhost:3000" http://localhost:8000/

# 4. Verificar logs (deben ser JSON)
tail -f backend.log | jq .

# 5. Verificar memory
ps aux | grep python
```

---

**Generado por:** Code Review Bot  
**Última actualización:** 2025-01-15
