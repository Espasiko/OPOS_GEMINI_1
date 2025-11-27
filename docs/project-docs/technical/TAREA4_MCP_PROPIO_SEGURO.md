# 🔐 TAREA 4: CREAR MCP PROPIO SEGURO

**Objetivo**: Implementar servidor MCP personalizado con máxima seguridad

---

## 📚 ¿Qué es un MCP Server?

**Model Context Protocol (MCP)** es un estándar abierto para conectar aplicaciones IA con sistemas externos.

**Componentes**:
- **Server**: Expone herramientas, recursos y prompts
- **Client**: Consume las capacidades del server
- **Transport**: SSE, HTTP, o WebSocket

---

## 🏗️ ARQUITECTURA MCP PARA OPOSITAIA

```
┌────────────────────────────────────────────────────────────┐
│                  OpositAIA MCP Server                       │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                    TOOLS (Herramientas)               │ │
│  │                                                        │ │
│  │  • rag_search(query, filters)                        │ │
│  │  • boe_search(query, date_range)                     │
│  │  • jurisprudencia_search(query, area)                │ │
│  │  • generate_summary(text, provider)                  │ │
│  │  • generate_flashcards(content, count)               │ │
│  │  • generate_mind_map(topic)                          │ │
│  │  • generate_study_plan(subject, weeks)               │ │
│  │  • check_boe_updates(area, days)                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                  RESOURCES (Recursos)                 │ │
│  │                                                        │ │
│  │  • opositaia://rag/stats                             │ │
│  │  • opositaia://boe/latest                            │ │
│  │  • opositaia://jurisprudencia/recent                 │ │
│  │  • opositaia://leyes/list                            │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                   PROMPTS (Plantillas)                │ │
│  │                                                        │ │
│  │  • explain_law(law_name)                             │ │
│  │  • compare_laws(law1, law2)                          │ │
│  │  • exam_question(topic, difficulty)                  │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## 🔒 IMPLEMENTACIÓN SEGURA

### 1. Estructura del Proyecto

```
backend/mcp_server/
├── server.py              # Servidor MCP principal
├── auth.py                # Autenticación y autorización
├── tools/                 # Herramientas
│   ├── __init__.py
│   ├── rag_tools.py
│   ├── boe_tools.py
│   ├── jurisprudencia_tools.py
│   └── ai_tools.py
├── resources/             # Recursos
│   ├── __init__.py
│   └── data_resources.py
├── prompts/               # Prompts
│   ├── __init__.py
│   └── exam_prompts.py
├── middleware/            # Seguridad
│   ├── __init__.py
│   ├── rate_limiter.py
│   ├── validator.py
│   └── logger.py
└── config.py              # Configuración
```

### 2. Servidor MCP Base

```python
# backend/mcp_server/server.py
from mcp.server import Server
from mcp.types import Tool, Resource, Prompt
import logging
from .auth import require_auth, check_permissions
from .middleware import rate_limit, validate_input, audit_log

logger = logging.getLogger(__name__)

# Crear servidor
server = Server("opositaia")

# ============================================================================
# TOOLS (Herramientas)
# ============================================================================

@server.tool()
@require_auth
@rate_limit(max_calls=100, window=60)  # 100 calls/min
@validate_input
@audit_log
async def rag_search(
    query: str,
    top_k: int = 5,
    min_score: float = 0.5,
    layer_filter: int = None
) -> dict:
    """
    Busca en la base de conocimiento RAG
    
    Args:
        query: Consulta del usuario
        top_k: Número de resultados (1-20)
        min_score: Score mínimo (0.0-1.0)
        layer_filter: Filtrar por capa (1=Normativa, 3=Materiales)
    
    Returns:
        Documentos relevantes con scores
    
    Security:
        - Requiere autenticación
        - Rate limited: 100 calls/min
        - Input validation
        - Audit logged
    """
    from agents.rag_agent_v2 import get_rag_agent_v2
    
    # Validar parámetros
    if not 1 <= top_k <= 20:
        raise ValueError("top_k must be between 1 and 20")
    if not 0.0 <= min_score <= 1.0:
        raise ValueError("min_score must be between 0.0 and 1.0")
    
    # Buscar
    agent = get_rag_agent_v2()
    results = await agent.search_documents(
        query=query,
        top_k=top_k,
        min_score=min_score,
        layer_filter=layer_filter
    )
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }

@server.tool()
@require_auth
@rate_limit(max_calls=50, window=60)
@validate_input
@audit_log
async def boe_search(
    query: str,
    fecha_desde: str = None,
    fecha_hasta: str = None
) -> dict:
    """
    Busca en el BOE
    
    Args:
        query: Término de búsqueda
        fecha_desde: Fecha inicio (YYYYMMDD)
        fecha_hasta: Fecha fin (YYYYMMDD)
    
    Returns:
        Documentos del BOE
    
    Security:
        - Requiere autenticación
        - Rate limited: 50 calls/min
        - Input validation
        - Audit logged
    """
    from agents.boe_agent import BOEAgent
    
    agent = BOEAgent()
    results = await agent.search(query, fecha_desde, fecha_hasta)
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }

@server.tool()
@require_auth
@rate_limit(max_calls=20, window=60)
@validate_input
@audit_log
async def generate_summary(
    text: str,
    provider: str = "groq",
    max_length: int = 500
) -> dict:
    """
    Genera resumen de texto
    
    Args:
        text: Texto a resumir (max 10,000 chars)
        provider: Proveedor LLM (groq, deepseek, gemini)
        max_length: Longitud máxima del resumen
    
    Returns:
        Resumen generado
    
    Security:
        - Requiere autenticación
        - Rate limited: 20 calls/min
        - Input validation (max 10K chars)
        - Audit logged
    """
    from routers.ai_functions import generate_summary as gen_summary
    
    # Validar longitud
    if len(text) > 10000:
        raise ValueError("Text too long (max 10,000 chars)")
    
    result = await gen_summary(text, provider)
    return result

# ============================================================================
# RESOURCES (Recursos)
# ============================================================================

@server.resource("opositaia://rag/stats")
@require_auth
async def get_rag_stats() -> dict:
    """
    Obtiene estadísticas del sistema RAG
    
    Returns:
        Estadísticas de la colección
    
    Security:
        - Requiere autenticación
        - Read-only
    """
    from agents.rag_agent_v2 import get_rag_agent_v2
    
    agent = get_rag_agent_v2()
    stats = await agent.get_collection_stats()
    
    return stats

@server.resource("opositaia://boe/latest")
@require_auth
@rate_limit(max_calls=10, window=60)
async def get_latest_boe() -> dict:
    """
    Obtiene el sumario más reciente del BOE
    
    Returns:
        Sumario del BOE de hoy
    
    Security:
        - Requiere autenticación
        - Rate limited: 10 calls/min
    """
    from agents.boe_agent import BOEAgent
    
    agent = BOEAgent()
    sumario = await agent.get_latest_sumario()
    
    return sumario

# ============================================================================
# PROMPTS (Plantillas)
# ============================================================================

@server.prompt()
async def explain_law(law_name: str) -> str:
    """
    Genera prompt para explicar una ley
    
    Args:
        law_name: Nombre de la ley
    
    Returns:
        Prompt optimizado
    """
    return f"""
Eres un experto en legislación española de Seguridad Social.

Explica de forma clara y concisa la siguiente ley:
{law_name}

Incluye:
1. Objetivo principal de la ley
2. Ámbito de aplicación
3. Puntos clave
4. Ejemplos prácticos
5. Relación con otras leyes

Usa un lenguaje accesible pero preciso.
"""

@server.prompt()
async def exam_question(topic: str, difficulty: str = "medium") -> str:
    """
    Genera prompt para crear pregunta de examen
    
    Args:
        topic: Tema de la pregunta
        difficulty: Dificultad (easy, medium, hard)
    
    Returns:
        Prompt optimizado
    """
    difficulty_map = {
        "easy": "básica, conceptual",
        "medium": "intermedia, aplicación práctica",
        "hard": "avanzada, casos complejos"
    }
    
    return f"""
Eres un experto en oposiciones de Seguridad Social en España.

Crea una pregunta de examen tipo test sobre: {topic}

Dificultad: {difficulty_map.get(difficulty, "intermedia")}

Formato:
- Pregunta clara y precisa
- 4 opciones de respuesta (A, B, C, D)
- Solo una respuesta correcta
- Explicación de por qué es correcta
- Referencias legales si aplica

La pregunta debe ser realista y similar a las de exámenes oficiales.
"""

# ============================================================================
# STARTUP
# ============================================================================

async def startup():
    """Inicialización del servidor"""
    logger.info("🚀 OpositAIA MCP Server starting...")
    
    # Verificar conexiones
    from agents.rag_agent_v2 import get_rag_agent_v2
    agent = get_rag_agent_v2()
    stats = await agent.get_collection_stats()
    logger.info(f"✅ RAG connected: {stats['total_documents']} documents")
    
    logger.info("✅ OpositAIA MCP Server ready")

if __name__ == "__main__":
    import asyncio
    asyncio.run(startup())
    server.run()
```

### 3. Autenticación y Autorización

```python
# backend/mcp_server/auth.py
import jwt
import os
from functools import wraps
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("MCP_SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"

def create_token(user_id: str, permissions: list = None) -> str:
    """
    Crea JWT token para usuario
    
    Args:
        user_id: ID del usuario
        permissions: Lista de permisos
    
    Returns:
        JWT token
    """
    payload = {
        "sub": user_id,
        "permissions": permissions or ["read"],
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> dict:
    """
    Verifica JWT token
    
    Args:
        token: JWT token
    
    Returns:
        Payload del token
    
    Raises:
        jwt.InvalidTokenError: Si el token es inválido
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def require_auth(func):
    """
    Decorator para requerir autenticación
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Obtener token del contexto
        token = kwargs.get("_token")
        if not token:
            raise ValueError("Authentication required")
        
        # Verificar token
        try:
            payload = verify_token(token)
            kwargs["_user"] = payload
        except ValueError as e:
            logger.warning(f"Auth failed: {e}")
            raise ValueError(f"Authentication failed: {e}")
        
        return await func(*args, **kwargs)
    
    return wrapper

def check_permissions(required_permissions: list):
    """
    Decorator para verificar permisos
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("_user")
            if not user:
                raise ValueError("User not authenticated")
            
            user_permissions = user.get("permissions", [])
            
            # Verificar permisos
            if not any(perm in user_permissions for perm in required_permissions):
                raise ValueError(f"Insufficient permissions. Required: {required_permissions}")
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator
```

### 4. Rate Limiting

```python
# backend/mcp_server/middleware/rate_limiter.py
import time
from collections import defaultdict
from functools import wraps
import logging

logger = logging.getLogger(__name__)

# Almacenamiento en memoria (usar Redis en producción)
_rate_limit_store = defaultdict(list)

def rate_limit(max_calls: int, window: int):
    """
    Rate limiter decorator
    
    Args:
        max_calls: Máximo número de llamadas
        window: Ventana de tiempo en segundos
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("_user", {})
            user_id = user.get("sub", "anonymous")
            
            # Clave única por usuario y función
            key = f"{user_id}:{func.__name__}"
            
            # Limpiar llamadas antiguas
            now = time.time()
            _rate_limit_store[key] = [
                t for t in _rate_limit_store[key]
                if now - t < window
            ]
            
            # Verificar límite
            if len(_rate_limit_store[key]) >= max_calls:
                logger.warning(f"Rate limit exceeded for {user_id} on {func.__name__}")
                raise ValueError(f"Rate limit exceeded. Max {max_calls} calls per {window}s")
            
            # Registrar llamada
            _rate_limit_store[key].append(now)
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator
```

### 5. Validación de Inputs

```python
# backend/mcp_server/middleware/validator.py
from functools import wraps
import re
import logging

logger = logging.getLogger(__name__)

def validate_input(func):
    """
    Valida inputs para prevenir inyecciones
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Validar strings
        for key, value in kwargs.items():
            if isinstance(value, str):
                # Prevenir SQL injection
                if re.search(r"(;|--|'|\"|\\|\/\*|\*\/)", value):
                    logger.warning(f"Suspicious input detected: {key}={value[:50]}")
                    raise ValueError(f"Invalid characters in {key}")
                
                # Prevenir XSS
                if re.search(r"(<script|javascript:|onerror=|onload=)", value, re.IGNORECASE):
                    logger.warning(f"XSS attempt detected: {key}={value[:50]}")
                    raise ValueError(f"Invalid content in {key}")
        
        return await func(*args, **kwargs)
    
    return wrapper
```

### 6. Audit Logging

```python
# backend/mcp_server/middleware/logger.py
import logging
from functools import wraps
from datetime import datetime
import json

logger = logging.getLogger(__name__)

def audit_log(func):
    """
    Registra todas las llamadas para auditoría
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs.get("_user", {})
        user_id = user.get("sub", "anonymous")
        
        # Log entrada
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "function": func.__name__,
            "args": {k: v for k, v in kwargs.items() if not k.startswith("_")}
        }
        
        logger.info(f"AUDIT: {json.dumps(log_entry)}")
        
        try:
            result = await func(*args, **kwargs)
            
            # Log éxito
            logger.info(f"AUDIT SUCCESS: {func.__name__} by {user_id}")
            
            return result
        except Exception as e:
            # Log error
            logger.error(f"AUDIT ERROR: {func.__name__} by {user_id}: {str(e)}")
            raise
    
    return wrapper
```

---

## 🚀 DEPLOYMENT

### Opción 1: Cloudflare Workers (Recomendado)

```bash
# Deploy a Cloudflare
wrangler deploy

# Configurar secrets
wrangler secret put MCP_SECRET_KEY
wrangler secret put QDRANT_API_KEY
```

### Opción 2: Docker en VPS

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/mcp_server/ ./mcp_server/
COPY backend/agents/ ./agents/

CMD ["python", "-m", "mcp_server.server"]
```

```bash
# Build y deploy
docker build -t opositaia-mcp .
docker run -d \
  -p 8001:8001 \
  -e MCP_SECRET_KEY=your-secret \
  -e QDRANT_URL=your-qdrant-url \
  --name opositaia-mcp \
  opositaia-mcp
```

---

## 💰 COSTES

**Cloudflare Workers**: €0/mes (free tier)  
**Docker en VPS**: €0/mes (ya tienes el VPS)

**TOTAL**: €0/mes

---

## 🎯 RECOMENDACIÓN

**Implementar MCP Server en Cloudflare Workers**: ⭐⭐⭐⭐⭐

**Razones**:
1. **Gratis** para tu escala
2. **Global**: Baja latencia
3. **Seguro**: DDoS protection
4. **Escalable**: Automático
5. **Mantenimiento**: Cero

**Tiempo de implementación**: 8-10 horas
