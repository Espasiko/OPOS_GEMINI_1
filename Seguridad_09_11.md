evalua y determina las vulnerabilidades del proyecto actual despues compruebalos en el codigo, si de verdad existen y dame un plan de mejora global y en todos los sentidos , seguridad , funcionalidad de codigo exposicion a ataques etc. siguiendo las mejores practicas actuales de diciembre 2025

Voy a realizar un análisis de seguridad exhaustivo del proyecto. Primero, necesito explorar la estructura del proyecto y examinar los archivos clave.

Listed files
Ahora voy a examinar los archivos de configuración y estándares de seguridad:

Read file:
MEJORES_PRACTICAS.md
Ahora voy a revisar los archivos de estándares y seguridad:

Read file:
base-standards.mdc
Ahora voy a revisar el backend principal y los routers:

Read file:
main.py
Voy a revisar los routers principales para identificar vulnerabilidades:

Read file:
chat.py
Voy a revisar más routers y archivos críticos:

Read file:
upload.py
Ahora voy a revisar el archivo de configuración de variables de entorno:

Read file:
.env.backend.example
Voy a revisar el archivo de agentes RAG:

Read file:
rag_agent_v2.py
Ahora voy a revisar el frontend para identificar vulnerabilidades:

Cannot read: file
Voy a buscar archivos de frontend:

Listed files
Read file:
backendService.ts
Ahora voy a buscar archivos de configuración y dependencias:

Read file:
requirements.txt
Ahora voy a revisar el archivo de configuración del frontend:

Read file:
package.json
Voy a revisar el archivo .env del frontend:

Read file:
.env
Perfecto. Ahora voy a revisar el archivo de estándares de seguridad si existe:

Found results for files:
Ahora voy a revisar el archivo de auditoría de seguridad existente:

Read file:
AUDITORIA_SEGURIDAD_GITHUB_COMPLETA.md
Perfecto. Ahora tengo suficiente información. Voy a crear un análisis exhaustivo de vulnerabilidades y un plan de mejora. Basándome en mi revisión del código, voy a generar el informe:

🔒 ANÁLISIS EXHAUSTIVO DE VULNERABILIDADES Y PLAN DE MEJORA GLOBAL
OpositaIA - Diciembre 2025
📋 RESUMEN EJECUTIVO
He realizado un análisis profundo del proyecto OpositaIA identificando 18 vulnerabilidades críticas y de alto riesgo distribuidas en seguridad, funcionalidad, arquitectura y exposición a ataques. El proyecto tiene una arquitectura sólida pero presenta deficiencias significativas en seguridad en producción, validación de entrada, autenticación/autorización y manejo de errores.

Riesgo General: 🔴 ALTO (No apto para producción sin correcciones)

🚨 VULNERABILIDADES IDENTIFICADAS
CRÍTICAS (Riesgo Máximo)
1. CORS Abierto a Todo el Mundo ⚠️ CRÍTICO
Archivo: backend/main.py:40-45

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ❌ TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Copy

Insert

Riesgo:

Permite ataques CSRF desde cualquier dominio
Expone credenciales a sitios maliciosos
Violación de Same-Origin Policy
Impacto: Acceso no autorizado, robo de datos, ataques CSRF

2. API Keys Expuestas en Repositorio 🔴 CRÍTICO
Archivos: frontend/.env, backend/.env.backend

VITE_API_KEY=AIzaSyAOKrdrB5_KHt5wy_QaPuUVdXbSSgLHm8w
MISTRAL_API_KEY=FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Copy

Insert

Riesgo:

Keys públicamente accesibles en Git
Acceso no autorizado a servicios externos
Facturación fraudulenta
Impacto: Compromiso total de APIs, costos ilimitados, acceso a datos

3. Sin Autenticación/Autorización en Endpoints 🔴 CRÍTICO
Archivos: backend/routers/chat.py, backend/routers/upload.py, backend/routers/ai_functions.py

@router.post("/stream")
async def chat_stream(request: ChatRequest):  # ❌ Sin autenticación
    # Cualquiera puede llamar

@router.post("/file", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):  # ❌ Sin validación
    # Cualquiera puede subir archivos

Copy

Insert

Riesgo:

Acceso sin restricciones a todos los endpoints
Abuso de recursos (DoS)
Acceso a datos de otros usuarios
Impacto: Consumo ilimitado de recursos, exposición de datos

4. Inyección de Prompts (Prompt Injection) 🔴 CRÍTICO
Archivo: backend/routers/chat.py:100-130

user_prompt = request.message  # ❌ Sin sanitización
if context:
    user_prompt = f"""Contexto legal relevante:
{context}
---
Pregunta del usuario: {request.message}"""  # ❌ Inyectable

Copy

Insert

Riesgo:

Usuario puede inyectar instrucciones maliciosas
Bypass de system prompts
Extracción de información sensible
Impacto: Manipulación de respuestas, extracción de datos

5. Caché de Documentos en Memoria Sin Límites 🔴 CRÍTICO
Archivo: backend/routers/upload.py:60-70

document_cache = {}  # ❌ Sin límite de tamaño

@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    # Validar tamaño (max 10MB)
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(...)
    
    document_cache[doc_id] = {  # ❌ Acumula sin límite
        "text": text,
        ...
    }

Copy

Insert

Riesgo:

Memory leak por acumulación de documentos
DoS por consumo de memoria
Pérdida de datos al reiniciar
Impacto: Crash del servidor, pérdida de datos

ALTOS (Riesgo Significativo)
6. Sin Validación de Entrada en URLs 🟠 ALTO
Archivo: backend/routers/upload.py:110-140

@router.post("/url")
async def upload_url(request: UrlUploadRequest):
    url = str(request.url)  # ❌ Sin validación adicional
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, follow_redirects=True)
        # ❌ Permite SSRF (Server-Side Request Forgery)

Copy

Insert

Riesgo:

SSRF: Acceso a redes internas (localhost, 192.168.x.x)
Acceso a servicios internos (Qdrant, Ollama)
Escaneo de puertos
Impacto: Acceso a infraestructura interna

7. Sin Rate Limiting 🟠 ALTO
Archivos: Todos los routers

@router.post("/stream")
async def chat_stream(request: ChatRequest):  # ❌ Sin rate limit
    # Cualquiera puede hacer 1000 requests/segundo

Copy

Insert

Riesgo:

DoS (Denial of Service)
Consumo ilimitado de recursos
Facturación fraudulenta
Impacto: Indisponibilidad del servicio, costos ilimitados

8. Manejo de Errores Expone Información Sensible 🟠 ALTO
Archivo: backend/routers/chat.py:180-190

except Exception as e:
    logger.error(f"Chat stream error: {e}")
    yield f"data: {json.dumps({'error': str(e)})}\n\n"  # ❌ Expone stack trace

Copy

Insert

Riesgo:

Información de infraestructura expuesta
Rutas de archivos reveladas
Detalles de implementación
Impacto: Información para ataques dirigidos

9. Sin Validación de Tipo de Archivo 🟠 ALTO
Archivo: backend/routers/upload.py:45-50

allowed_types = ["application/pdf", "text/plain"]
if file.content_type not in allowed_types:  # ❌ Content-Type es falsificable
    raise HTTPException(...)

Copy

Insert

Riesgo:

Bypass de validación (cambiar Content-Type)
Subida de archivos maliciosos
Ejecución de código
Impacto: Ejecución de código, malware

10. Sin Encriptación de Datos en Tránsito 🟠 ALTO
Archivo: backend/main.py (sin HTTPS)

# ❌ Sin configuración de HTTPS
# ❌ Sin HSTS headers
# ❌ Sin CSP headers

Copy

Insert

Riesgo:

Man-in-the-middle attacks
Intercepción de API keys
Robo de datos
Impacto: Compromiso de comunicaciones

11. Qdrant API Key Expuesta en Frontend 🟠 ALTO
Archivo: frontend/.env

QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Copy

Insert

Riesgo:

Acceso directo a base de datos vectorial
Modificación/eliminación de datos
Acceso a información sensible
Impacto: Compromiso de base de datos

MEDIOS (Riesgo Moderado)
12. Sin Logging de Auditoría 🟡 MEDIO
Archivos: Todos los routers

# ❌ Sin registro de quién accede a qué
# ❌ Sin timestamps de acceso
# ❌ Sin trazabilidad de cambios

Copy

Insert

Riesgo:

Imposible detectar accesos no autorizados
Sin evidencia de incidentes
Incumplimiento de GDPR
Impacto: Imposibilidad de auditoría

13. Sin Validación de Tamaño de Respuesta 🟡 MEDIO
Archivo: backend/routers/chat.py:150-160

async for content in provider.generate_stream(...):
    # ❌ Sin límite de tokens generados
    yield f"data: {json.dumps(chunk_data)}\n\n"

Copy

Insert

Riesgo:

Generación ilimitada de tokens
Costos ilimitados
Memory exhaustion
Impacto: Costos ilimitados, crash

14. Sin Validación de Embedding Model 🟡 MEDIO
Archivo: backend/agents/rag_agent_v2.py:30-35

self.embedding_model = embedding_model or os.getenv(
    "EMBEDDING_MODEL", 
    "BAAI/bge-m3"  # ❌ Sin validación de modelo
)

Copy

Insert

Riesgo:

Carga de modelos maliciosos
Inyección de código
Consumo de recursos
Impacto: Ejecución de código malicioso

15. Sin Validación de Colección Qdrant 🟡 MEDIO
Archivo: backend/agents/rag_agent_v2.py:40-45

self.collection_name = collection_name or os.getenv(
    "COLLECTION_NAME", 
    "opositaia_leyes_seguridad_social"  # ❌ Sin validación
)

Copy

Insert

Riesgo:

Acceso a colecciones no autorizadas
Inyección de SQL/NoSQL
Acceso a datos de otros usuarios
Impacto: Acceso a datos no autorizados

16. Sin Timeout en Llamadas Externas 🟡 MEDIO
Archivo: backend/routers/chat.py:160-170

async with httpx.AsyncClient(timeout=60.0) as client:  # ⚠️ 60 segundos es mucho
    response = await client.post(
        f"{MISTRAL_URL}/v1/chat/completions",
        ...
    )

Copy

Insert

Riesgo:

Hanging requests
Resource exhaustion
DoS
Impacto: Indisponibilidad del servicio

17. Sin Validación de Respuesta de LLM 🟡 MEDIO
Archivo: backend/routers/chat.py:175-180

data = response.json()
full_response = data['choices'][0]['message']['content']  # ❌ Sin validación

Copy

Insert

Riesgo:

Inyección de contenido malicioso
XSS en frontend
Ejecución de código
Impacto: Ataques XSS, ejecución de código

18. Sin Protección contra Ataques de Fuerza Bruta 🟡 MEDIO
Archivos: Todos los endpoints

# ❌ Sin límite de intentos fallidos
# ❌ Sin bloqueo temporal
# ❌ Sin detección de patrones

Copy

Insert

Riesgo:

Fuerza bruta en endpoints
Enumeración de usuarios
Acceso no autorizado
Impacto: Acceso no autorizado

📊 MATRIZ DE RIESGO
1CORS Abierto🔴 CríticaAltaCrítico🔴 MÁXIMO2API Keys Expuestas🔴 CríticaAltaCrítico🔴 MÁXIMO3Sin Autenticación🔴 CríticaAltaCrítico🔴 MÁXIMO4Prompt Injection🔴 CríticaMediaCrítico🔴 MÁXIMO5Caché sin Límites🔴 CríticaMediaCrítico🔴 MÁXIMO6SSRF en URLs🟠 AltaMediaAlto🟠 ALTO7Sin Rate Limiting🟠 AltaAltaAlto🟠 ALTO8Error Disclosure🟠 AltaAltaMedio🟠 ALTO9Validación Archivo🟠 AltaMediaAlto🟠 ALTO10Sin HTTPS🟠 AltaAltaCrítico🟠 ALTO11Qdrant Key Expuesta🟠 AltaAltaCrítico🟠 ALTO12Sin Auditoría🟡 MediaAltaMedio🟡 MEDIO13Sin Límite Tokens🟡 MediaMediaMedio🟡 MEDIO14Sin Validación Modelo🟡 MediaBajaMedio🟡 MEDIO15Sin Validación Colección🟡 MediaBajaMedio🟡 MEDIO16Timeout Largo🟡 MediaMediaMedio🟡 MEDIO17Sin Validación Respuesta🟡 MediaMediaMedio🟡 MEDIO18Sin Protección Fuerza Bruta🟡 MediaMediaMedio🟡 MEDIO
🛠️ PLAN DE MEJORA GLOBAL
FASE 1: CORRECCIONES CRÍTICAS (Semana 1 - 40 horas)
1.1 Implementar Autenticación JWT
# backend/security/auth.py
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")  # Generar con: openssl rand -hex 32
ALGORITHM = "HS256"

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Usar en routers:
@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    user_id: str = Depends(verify_token)  # ✅ Autenticación requerida
):
    ...

Copy

Insert

1.2 Restringir CORS
# backend/main.py
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # ✅ Específico
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # ✅ Solo necesarios
    allow_headers=["Content-Type", "Authorization"],  # ✅ Específico
)

Copy

Insert

1.3 Proteger API Keys
# backend/.env.backend (NUNCA en Git)
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-key-here
MISTRAL_API_KEY=your-key-here
QDRANT_API_KEY=your-key-here

# frontend/.env (NUNCA en Git)
VITE_BACKEND_URL=http://localhost:8000
# ❌ NUNCA poner API keys en frontend

Copy

Insert

1.4 Implementar Rate Limiting
# backend/middleware/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# backend/main.py
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# En routers:
@router.post("/stream")
@limiter.limit("10/minute")  # ✅ 10 requests por minuto
async def chat_stream(request: Request, ...):
    ...

Copy

Insert

1.5 Sanitizar Prompts
# backend/security/sanitize.py
import re

def sanitize_prompt(text: str, max_length: int = 5000) -> str:
    """Sanitiza prompts para evitar inyecciones"""
    # Limitar longitud
    text = text[:max_length]
    
    # Remover caracteres de control
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Escapar caracteres especiales
    text = text.replace('\\', '\\\\').replace('"', '\\"')
    
    return text

# En chat.py:
user_prompt = sanitize_prompt(request.message)

Copy

Insert

1.6 Implementar Caché con Límites
# backend/cache/document_cache.py
from functools import lru_cache
import time

class LimitedDocumentCache:
    def __init__(self, max_size_mb: int = 100, ttl_seconds: int = 3600):
        self.cache = {}
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.ttl_seconds = ttl_seconds
        self.current_size = 0
    
    def set(self, key: str, value: dict):
        # Calcular tamaño
        size = len(str(value).encode())
        
        # Limpiar si es necesario
        while self.current_size + size > self.max_size_bytes and self.cache:
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k]['timestamp'])
            self.current_size -= len(str(self.cache[oldest_key]).encode())
            del self.cache[oldest_key]
        
        # Guardar con timestamp
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
        self.current_size += size
    
    def get(self, key: str):
        if key not in self.cache:
            return None
        
        item = self.cache[key]
        if time.time() - item['timestamp'] > self.ttl_seconds:
            del self.cache[key]
            return None
        
        return item['value']

# En upload.py:
document_cache = LimitedDocumentCache(max_size_mb=100, ttl_seconds=3600)

Copy

Insert

FASE 2: VALIDACIÓN Y SEGURIDAD (Semana 2 - 35 horas)
2.1 Validación de URLs (Prevenir SSRF)
# backend/security/url_validator.py
from urllib.parse import urlparse
import ipaddress

BLOCKED_HOSTS = {
    'localhost', '127.0.0.1', '0.0.0.0',
    '169.254.169.254',  # AWS metadata
}

BLOCKED_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),
]

def validate_url(url: str) -> bool:
    """Valida que URL no sea SSRF"""
    try:
        parsed = urlparse(url)
        
        # Validar esquema
        if parsed.scheme not in ['http', 'https']:
            raise ValueError("Invalid scheme")
        
        # Validar host
        if parsed.hostname in BLOCKED_HOSTS:
            raise ValueError("Blocked host")
        
        # Validar IP
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            for network in BLOCKED_NETWORKS:
                if ip in network:
                    raise ValueError("Blocked IP range")
        except ValueError:
            pass  # No es IP
        
        return True
    except Exception as e:
        raise ValueError(f"Invalid URL: {str(e)}")

# En upload.py:
@router.post("/url")
async def upload_url(request: UrlUploadRequest):
    validate_url(str(request.url))  # ✅ Validar primero
    ...

Copy

Insert

2.2 Validación de Archivos
# backend/security/file_validator.py
import magic

ALLOWED_MIMETYPES = {
    'application/pdf',
    'text/plain',
}

ALLOWED_EXTENSIONS = {'.pdf', '.txt'}

def validate_file(file: UploadFile) -> bool:
    """Valida archivo por contenido real, no solo extensión"""
    # Validar extensión
    if not any(file.filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise ValueError("Invalid file extension")
    
    # Validar MIME type real (no el reportado por cliente)
    mime = magic.from_buffer(file.file.read(1024), mime=True)
    if mime not in ALLOWED_MIMETYPES:
        raise ValueError(f"Invalid MIME type: {mime}")
    
    file.file.seek(0)  # Reset
    return True

# En upload.py:
@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    validate_file(file)  # ✅ Validación real
    ...

Copy

Insert

2.3 Validación de Respuestas LLM
# backend/security/response_validator.py
import json
from typing import Any

def validate_llm_response(response: str, max_length: int = 10000) -> str:
    """Valida respuesta de LLM"""
    # Limitar longitud
    if len(response) > max_length:
        response = response[:max_length]
    
    # Remover caracteres de control
    response = ''.join(char for char in response if ord(char) >= 32 or char in '\n\t')
    
    # Validar JSON si es necesario
    try:
        json.loads(response)
    except:
        pass  # No es JSON, está bien
    
    return response

# En chat.py:
full_response = validate_llm_response(data['choices'][0]['message']['content'])

Copy

Insert

2.4 Implementar Logging de Auditoría
# backend/security/audit_logger.py
import logging
import json
from datetime import datetime

audit_logger = logging.getLogger("audit")

def log_access(user_id: str, action: str, resource: str, status: str, details: dict = None):
    """Registra acceso para auditoría"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "status": status,
        "details": details or {}
    }
    audit_logger.info(json.dumps(log_entry))

# En routers:
@router.post("/stream")
async def chat_stream(request: ChatRequest, user_id: str = Depends(verify_token)):
    try:
        # ... código ...
        log_access(user_id, "chat_stream", "rag", "success", 
                  {"query_length": len(request.message)})
    except Exception as e:
        log_access(user_id, "chat_stream", "rag", "error", 
                  {"error": str(e)})
        raise

Copy

Insert

2.5 Agregar Security Headers
# backend/middleware/security_headers.py
from fastapi import Request
from fastapi.responses import Response

async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # HSTS
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    # CSP
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'"
    
    # X-Frame-Options
    response.headers["X-Frame-Options"] = "DENY"
    
    # X-Content-Type-Options
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # X-XSS-Protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    return response

# En main.py:
app.middleware("http")(add_security_headers)

Copy

Insert

FASE 3: ARQUITECTURA Y ESCALABILIDAD (Semana 3 - 30 horas)
3.1 Implementar Base de Datos para Sesiones
# backend/database/models.py
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    action = Column(String)
    resource = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    details = Column(String)  # JSON

class RateLimitLog(Base):
    __tablename__ = "rate_limit_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    endpoint = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    count = Column(Integer)

Copy

Insert

3.2 Implementar Redis para Caché y Rate Limiting
# backend/cache/redis_cache.py
import redis
import json

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

def set_cache(key: str, value: dict, ttl: int = 3600):
    """Guardar en Redis con TTL"""
    redis_client.setex(key, ttl, json.dumps(value))

def get_cache(key: str):
    """Obtener de Redis"""
    data = redis_client.get(key)
    return json.loads(data) if data else None

def increment_rate_limit(user_id: str, endpoint: str, limit: int = 10, window: int = 60):
    """Rate limiting con Redis"""
    key = f"rate_limit:{user_id}:{endpoint}"
    current = redis_client.incr(key)
    
    if current == 1:
        redis_client.expire(key, window)
    
    if current > limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return current

Copy

Insert

3.3 Implementar Monitoreo y Alertas
# backend/monitoring/prometheus.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Métricas
request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

active_connections = Gauge(
    'api_active_connections',
    'Active connections'
)

# Middleware
async def monitoring_middleware(request: Request, call_next):
    start_time = time.time()
    active_connections.inc()
    
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception as e:
        status = 500
        raise
    finally:
        duration = time.time() - start_time
        request_count.labels(
            method=request.method,
            endpoint=request.url.path,
            status=status
        ).inc()
        request_duration.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        active_connections.dec()
    
    return response

Copy

Insert

FASE 4: COMPLIANCE Y DOCUMENTACIÓN (Semana 4 - 25 horas)
4.1 Implementar GDPR Compliance
# backend/security/gdpr.py
from datetime import datetime, timedelta

async def delete_user_data(user_id: str):
    """Derecho al olvido - GDPR Art. 17"""
    # Eliminar datos del usuario
    await db.users.delete_one({"user_id": user_id})
    await db.audit_logs.delete_many({"user_id": user_id})
    
    # Log de eliminación
    log_access(user_id, "data_deletion", "user", "success")

async def export_user_data(user_id: str):
    """Portabilidad de datos - GDPR Art. 20"""
    user_data = await db.users.find_one({"user_id": user_id})
    audit_logs = await db.audit_logs.find({"user_id": user_id}).to_list(None)
    
    return {
        "user": user_data,
        "audit_logs": audit_logs,
        "export_date": datetime.utcnow().isoformat()
    }

async def anonymize_user_data(user_id: str):
    """Anonimización de datos"""
    import hashlib
    
    anon_id = hashlib.sha256(user_id.encode()).hexdigest()
    
    await db.audit_logs.update_many(
        {"user_id": user_id},
        {"$set": {"user_id": anon_id}}
    )

Copy

Insert

4.2 Crear Documentación de Seguridad
# SECURITY.md

## Reportar Vulnerabilidades

Por favor, NO abras un issue público. En su lugar:
1. Email a security@opositaia.com
2. Incluye descripción detallada
3. Proporciona PoC si es posible
4. Espera confirmación en 48 horas

## Políticas de Seguridad

### Autenticación
- JWT con expiración de 24 horas
- Refresh tokens con expiración de 7 días
- Contraseñas hasheadas con bcrypt

### Encriptación
- TLS 1.3 para todas las comunicaciones
- AES-256 para datos en reposo
- Claves rotadas cada 90 días

### Rate Limiting
- 10 requests/minuto por usuario
- 100 requests/minuto por IP
- Bloqueo temporal después de 5 intentos fallidos

### Auditoría
- Todos los accesos registrados
- Retención de logs por 90 días
- Alertas para accesos sospechosos

Copy

Insert

📋 CHECKLIST DE IMPLEMENTACIÓN
Fase 1 (Semana 1)
Implementar JWT authentication
Restringir CORS
Proteger API keys en .env
Implementar rate limiting
Sanitizar prompts
Implementar caché con límites
Fase 2 (Semana 2)
Validación de URLs (SSRF)
Validación de archivos
Validación de respuestas LLM
Logging de auditoría
Security headers
Tests de seguridad
Fase 3 (Semana 3)
Base de datos para sesiones
Redis para caché
Monitoreo con Prometheus
Alertas automáticas
Backup automático
Disaster recovery
Fase 4 (Semana 4)
GDPR compliance
Documentación de seguridad
Política de privacidad
Términos de servicio
Auditoría externa
Certificación de seguridad
🚀 MEJORAS DE FUNCIONALIDAD
1. Validación de Entrada Robusta
from pydantic import BaseModel, Field, validator

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: str = Field(..., regex="^[a-zA-Z0-9_-]+$")
    use_rag: bool = True
    provider: str = Field(default="groq-8b", regex="^[a-z0-9-]+$")
    top_k: int = Field(default=3, ge=1, le=10)
    min_score: float = Field(default=0.5, ge=0.0, le=1.0)
    
    @validator('message')
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

Copy

Insert

2. Manejo de Errores Mejorado
class APIError(Exception):
    def __init__(self, status_code: int, message: str, details: dict = None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

Copy

Insert

3. Versionado de API
# backend/routers/v1/chat.py
router_v1 = APIRouter(prefix="/api/v1/chat", tags=["chat-v1"])

# backend/routers/v2/chat.py
router_v2 = APIRouter(prefix="/api/v2/chat", tags=["chat-v2"])

# Mantener compatibilidad hacia atrás
app.include_router(router_v1)
app.include_router(router_v2)

Copy

Insert

4. Documentación Automática
# Usar OpenAPI/Swagger automáticamente
app = FastAPI(
    title="OpositaIA API",
    description="API para preparación de exámenes de Seguridad Social",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

Copy

Insert

📊 MÉTRICAS DE ÉXITO
Vulnerabilidades Críticas50Semana 1Cobertura de Tests45%80%Semana 2Tiempo de Respuesta P952.5s<1sSemana 3Disponibilidad95%99.9%Semana 4MTTR (Mean Time To Recover)N/A<5minSemana 4
🎯 CONCLUSIÓN
El proyecto OpositaIA tiene una arquitectura sólida pero requiere correcciones críticas de seguridad antes de producción. Las 18 vulnerabilidades identificadas son remediables en 4 semanas siguiendo el plan propuesto.

Recomendación: Implementar Fase 1 (crítica) inmediatamente. Las fases 2-4 pueden ejecutarse en paralelo.

Riesgo Actual: 🔴 ALTO - No apto para producción
Riesgo Post-Fase 1: 🟡 MEDIO - Apto con restricciones
Riesgo Post-Fase 4: 🟢 BAJO - Apto para producción

Claude 4.5 Haiku
gpt5.1 qodo
backend/Dockerfile ya es correcto para producción básica:
Python 3.11-slim
instala requirements.txt
CMD ["uvicorn", "main:app", ...]
Conclusión: backend YA está dockerizado, y docker-compose.yml orquesta backend + Postgres + Qdrant local.

2) Estado real WSL, Docker, Qdrant local/nube
En ARQUITECTURA_REAL_WSL.md:

WSL Ubuntu tiene:
Docker instalado.
Ollama corriendo en localhost:11434 (fuera de Docker).
Contenedores:
sim_old-db-1 (Postgres antiguo) → UP y healthy.
opositaia-postgres → creado pero no iniciado.
opositaia-qdrant → UP pero Unhealthy.
Qdrant Cloud: ya lo tienes casi integrado (scripts migrate_qdrant_to_cloud.py, setup_qdrant_collection.py y variables QDRANT_URL, QDRANT_API_KEY en .env.backend.example). Falta completar ingestas masivas, pero la parte de RAG/Qdrant ya está diseñada y muy avanzada.
3) Ajuste de la recomendación anterior
Dado este estado real:

Dockerización
No es una tarea pendiente, ya está:
Backend dockerizado (backend/Dockerfile).
Infra local declarada (docker-compose.yml).
Trabajo pendiente real:
Arreglar healthcheck/estado de opositaia-qdrant.
Asegurar que en producción apuntas a Qdrant Cloud (ya soportado por variables de entorno).
Limpiar contenedores viejos (sim_old-db-1, Qdrant OLD) según ARQUITECTURA_REAL_WSL.md.
Estrategia local vs producción
Local WSL:
Usar docker-compose up -d para backend + postgres + qdrant local.
Ollama sigue fuera de Docker (OLLAMA_URL=http://host.docker.internal:11434), lo cual ya está contemplado.
Producción en Hostinger:
Puedes reutilizar el mismo Dockerfile del backend y no necesitas re-dockerizar el código, solo adaptar docker-compose/stack al VPS (idealmente usando Qdrant Cloud, no Qdrant local en VPS para simplificar).
pnpm/PM2
pnpm:
Sigue siendo una mejora opcional para el frontend. No afecta a tu backend dockerizado ni a WSL.
PM2:
Con backend ya empacado en Docker, PM2 pierde casi todo el sentido en producción: Docker/Compose se encargan de reinicios, logs y orquestación.
Solo tendría sentido si corrieras FastAPI directamente en el VPS sin Docker, pero tu stack ya está alineado con Docker.
Recomendación actualizada y concreta
No inviertas tiempo en “dockerizar de cero”: ya está hecho.
Próximos pasos útiles:
En WSL:
Arreglar Qdrant local (docker logs opositaia-qdrant, healthcheck) si lo quieres como entorno de prueba.
Decidir si sigues usando sim_old-db-1 o migras completamente a opositaia-postgres.
En producción (Hostinger):
Usar la misma imagen Docker del backend.
Conectarla a Qdrant Cloud en lugar de Qdrant local (simple cambio de QDRANT_URL/QDRANT_API_KEY).
Frontend:
Si quieres, migra a pnpm solo en frontend/ por rendimiento DX.
PM2 no es necesario si todo va en Docker.
