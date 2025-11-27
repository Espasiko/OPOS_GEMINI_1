# 🏆 REGLAS DE ORO CONSOLIDADAS - OPOSITAIA
**Versión**: 2.0 (Consolidada)  
**Fecha**: 27 de Noviembre de 2025  
**Fuentes**: Estrategia de Seguridad + Best Practices + Auditoría de Seguridad

---

## 📋 ÍNDICE

1. [Objetivos y Criterios de Éxito](#objetivos)
2. [Reglas Generales Obligatorias](#reglas-generales)
3. [Frontend (React/TypeScript)](#frontend)
4. [Backend (FastAPI/Python)](#backend)
5. [Seguridad y IA](#seguridad-ia)
6. [RAG y Vectores](#rag)
7. [Testing](#testing)
8. [Observabilidad](#observabilidad)
9. [CI/CD y Deployment](#cicd)
10. [Checklist de PR](#checklist-pr)

---

## 🎯 1. OBJETIVOS Y CRITERIOS DE ÉXITO {#objetivos}

### Robustez
- ✅ Cero errores en runtime en producción
- ✅ Degradación controlada ante fallos de proveedores externos (LLMs, Qdrant, red)
- ✅ Retry con backoff exponencial en todas las integraciones externas
- ✅ Circuit breakers para servicios críticos

### Seguridad
- ✅ Sin vulnerabilidades críticas (OWASP Top 10)
- ✅ Cero secretos expuestos (código + historial Git)
- ✅ Cumplimiento GDPR y minimización de datos
- ✅ Sanitización XSS con DOMPurify en TODOS los outputs de IA
- ✅ Validación de inputs con Zod (frontend) y Pydantic (backend)

### Calidad
- ✅ Cobertura de tests: Frontend \u003e90%, Backend \u003e85% en core
- ✅ E2E tests verdes
- ✅ PRs con verificación automática (lint + type + test + coverage + SAST)
- ✅ Sin warnings de ESLint/TypeScript sin justificar

### Observabilidad
- ✅ Trazabilidad extremo a extremo de cada petición
- ✅ Tracking de cada llamada a IA (latencia, coste, tokens, prompts anonimizados)
- ✅ Logs estructurados (JSON) con correlation IDs
- ✅ OpenTelemetry para traces/spans

### Eficiencia
- ✅ Tiempos P95 de API \u003c 500ms (excluyendo latencia LLM)
- ✅ Colas/streams para operaciones largas
- ✅ Caching estratégico (RAG results, feature flags)
- ✅ Async-first en backend

### Mantenibilidad
- ✅ Arquitectura clara (docs/ARCHITECTURE.md actualizado)
- ✅ Estándares de código (ai-specs/specs/*)
- ✅ Linters y type-safety estrictos
- ✅ Funciones pequeñas, puras, testeables

---

## ⚡ 2. REGLAS GENERALES OBLIGATORIAS {#reglas-generales}

### 2.1 Seguridad Primero

#### Secretos y Configuración
```typescript
// ❌ NUNCA HACER
const API_KEY = "sk-1234567890";

// ✅ SIEMPRE HACER
import { z } from 'zod';

const EnvSchema = z.object({
  OPENAI_API_KEY: z.string().min(1),
  QDRANT_URL: z.string().url(),
  QDRANT_API_KEY: z.string().min(1),
});

// Validar al iniciar
const env = EnvSchema.parse(process.env);
```

**Reglas**:
- ✅ Nunca hardcodear secretos
- ✅ Validar `process.env`/`os.environ` con esquema al iniciar
- ✅ Aplicar "least privilege" en todas las credenciales
- ✅ Rotación periódica de API keys (cada 90 días)
- ✅ Segregación por entorno (dev/staging/prod)
- ✅ Solo `.env.example` en repo; `.env` fuera de VCS

#### Sanitización de Inputs/Outputs
```typescript
// ❌ NUNCA HACER - XSS VULNERABLE
<div dangerouslySetInnerHTML={{ __html: aiResponse }} />

// ✅ SIEMPRE HACER
import DOMPurify from 'dompurify';

const SafeAIContent = ({ html }: { html: string }) => (
  <div dangerouslySetInnerHTML={{ 
    __html: DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['br', 'p', 'strong', 'em', 'ul', 'ol', 'li', 'code', 'pre'],
      ALLOWED_ATTR: ['class']
    })
  }} />
);
```

**Reglas**:
- ✅ Sanitizar **absolutamente toda** la entrada (usuario Y proveedores IA)
- ✅ Escapar HTML/Markdown con DOMPurify
- ✅ Validar inputs con Zod (frontend) y Pydantic (backend)
- ✅ Nunca confiar en datos externos

#### Protección SSRF
```python
# ❌ NUNCA HACER
response = requests.get(user_provided_url)

# ✅ SIEMPRE HACER
from urllib.parse import urlparse

ALLOWED_DOMAINS = ['boe.es', 'www.boe.es']

def safe_request(url: str, timeout: int = 60):
    parsed = urlparse(url)
    
    if parsed.netloc not in ALLOWED_DOMAINS:
        raise ValueError(f"Dominio no permitido: {parsed.netloc}")
    
    if parsed.scheme not in ['http', 'https']:
        raise ValueError(f"Esquema no permitido: {parsed.scheme}")
    
    return requests.get(url, timeout=timeout, allow_redirects=False)
```

**Reglas**:
- ✅ Whitelist de dominios permitidos
- ✅ Bloquear IPs privadas (127.0.0.1, 169.254.169.254)
- ✅ Deshabilitar redirects automáticos
- ✅ Validar esquemas (solo http/https)

---

### 2.2 Tipado y Validación

#### Frontend (TypeScript)
```typescript
// ✅ SIEMPRE: Tipos estrictos
interface ChatMessage {
  id: string;
  role: 'user' | 'model';
  text: string;
  timestamp?: number;
}

// ✅ SIEMPRE: Validación con Zod
import { z } from 'zod';

const ChatRequestSchema = z.object({
  message: z.string().min(1).max(10000),
  conversation_id: z.string().uuid(),
  use_rag: z.boolean(),
});

type ChatRequest = z.infer<typeof ChatRequestSchema>;
```

**Reglas**:
- ✅ TypeScript estricto (no `any`, no `non-null assertions`)
- ✅ Tipos explícitos en funciones públicas
- ✅ Validación de inputs/outputs con Zod
- ✅ PascalCase para componentes, camelCase para variables

#### Backend (Python)
```python
# ✅ SIEMPRE: Pydantic strict mode
from pydantic import BaseModel, Field, validator

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: str
    use_rag: bool = True
    
    @validator('message')
    def validate_message(cls, v):
        if '<script' in v.lower():
            raise ValueError('Contenido no permitido')
        return v

# ✅ SIEMPRE: response_model en routes
@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    ...
```

**Reglas**:
- ✅ Pydantic models para request/response
- ✅ `response_model` explícito en todas las rutas
- ✅ Validadores custom para lógica de negocio
- ✅ snake_case para funciones, PascalCase para clases

---

### 2.3 Errores y Resiliencia

#### Retry con Backoff
```typescript
// ✅ Frontend: Implementado en Sprint 10
import { useAIProvider } from '../hooks/useAIProvider';

const { executeWithRetry } = useAIProvider();

const response = await executeWithRetry(async provider =>
  generateSummary({ text, provider })
);
```

```python
# ✅ Backend: Patrón estándar
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
async def call_llm_with_retry(prompt: str):
    return await llm_client.generate(prompt)
```

**Reglas**:
- ✅ Cada integración externa: timeouts, retries, circuit breakers
- ✅ Backoff exponencial (1s, 2s, 4s)
- ✅ Máximo 3 reintentos
- ✅ Nunca romper UI por error de IA: mostrar fallback

#### Manejo de Errores
```python
# ✅ Backend: HTTPException con mensajes claros
from fastapi import HTTPException

try:
    result = await external_service()
except TimeoutError:
    raise HTTPException(
        status_code=503,
        detail="Servicio de IA temporalmente no disponible"
    )
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
```

**Reglas**:
- ✅ Manejo global con HTTPException
- ✅ No exponer stack traces en prod
- ✅ Mapear errores de proveedores a 4xx/5xx apropiados
- ✅ Error boundaries en React para fallos de componentes

---

## 🎨 3. FRONTEND (REACT/TYPESCRIPT) {#frontend}

### 3.1 Estructura y Organización

```
frontend/
├── components/          # Componentes presentacionales
│   ├── ChatView.tsx
│   └── __tests__/      # Tests co-localizados
├── hooks/              # Custom hooks
│   └── useAIProvider.ts
├── services/           # API calls y abstracciones
│   ├── backendService.ts
│   └── geminiService.ts
├── utils/              # Utilidades puras
│   ├── formatters.ts
│   ├── providers.ts
│   └── cache.ts
├── contexts/           # React Context
└── __tests__/          # Tests de integración
```

**Reglas**:
- ✅ Separación estricta: UI (components) vs lógica (hooks/services)
- ✅ Componentes funcionales con hooks
- ✅ Side effects en hooks o services, no en componentes
- ✅ Co-localizar tests con código

### 3.2 Code Style

```typescript
// ✅ SIEMPRE: Componentes funcionales tipados
interface Props {
  message: string;
  onSend: (text: string) => void;
}

const ChatInput: React.FC<Props> = ({ message, onSend }) => {
  // Hooks primero
  const [input, setInput] = useState('');
  
  // Handlers después
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSend(input);
  };
  
  // Render al final
  return <form onSubmit={handleSubmit}>...</form>;
};
```

**Reglas**:
- ✅ ESLint config: single quotes, semicolons, 2-space indent, max-len 120
- ✅ Prefer functional components
- ✅ Strong typing over `any`
- ✅ Async: prefer async/await
- ✅ Naming: PascalCase (components), camelCase (vars), kebab-case (files)

### 3.3 Seguridad Frontend

```typescript
// ✅ SIEMPRE: Sanitización XSS
import DOMPurify from 'dompurify';

const SafeContent = ({ html }: { html: string }) => (
  <div dangerouslySetInnerHTML={{ 
    __html: DOMPurify.sanitize(html, { USE_PROFILES: { html: true } })
  }} />
);

// ✅ SIEMPRE: Validación de inputs
import { z } from 'zod';

const MessageSchema = z.string().min(1).max(10000);

const handleSubmit = (text: string) => {
  const validated = MessageSchema.parse(text);
  // ...
};
```

**Reglas**:
- ✅ DOMPurify para TODO contenido de IA
- ✅ Validación con Zod antes de enviar al backend
- ✅ No acoplar componentes directamente a fetch/HTTP
- ✅ Usar services/ para todas las llamadas API

---

## 🚀 4. BACKEND (FASTAPI/PYTHON) {#backend}

### 4.1 Estructura y Organización

```
backend/
├── main.py             # Entrypoint
├── routers/            # Endpoints (thin)
│   ├── chat.py
│   └── rag.py
├── agents/             # Lógica de negocio
│   ├── llm_providers.py
│   └── rag_agent.py
├── models/             # Pydantic models
├── database/           # DB helpers
└── tests/              # Tests
```

**Reglas**:
- ✅ Routers thin: solo validación y orquestación
- ✅ Lógica de negocio en agents/services
- ✅ Dependency injection para sessions/clients
- ✅ Evitar estado global (salvo memoized safely)

### 4.2 Code Style

```python
# ✅ SIEMPRE: Async-first
@router.post("/chat")
async def chat(req: ChatRequest, user=Depends(auth_guard)):
    async with httpx.AsyncClient() as client:
        response = await client.post(...)
    return response

# ✅ SIEMPRE: Logging estructurado
import logging
logger = logging.getLogger(__name__)

logger.info("Chat request", extra={
    "user_id": user.id,
    "conversation_id": req.conversation_id,
    "provider": req.provider
})
```

**Reglas**:
- ✅ Async def para todos los routers
- ✅ httpx.AsyncClient para HTTP calls
- ✅ Logging estructurado (no print)
- ✅ Nunca loggear secretos o PII

### 4.3 Seguridad Backend

```python
# ✅ SIEMPRE: Middlewares de seguridad
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://opositaia.com"],  # NO "*" en prod
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["opositaia.com", "*.opositaia.com"]
)

# ✅ SIEMPRE: Headers de seguridad
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# ✅ SIEMPRE: Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: Request):
    ...
```

**Reglas**:
- ✅ CORS restringido en producción
- ✅ CSP headers configurados
- ✅ Rate limiting por IP/usuario
- ✅ JWT con rotación y expiración corta

---

## 🤖 5. SEGURIDAD Y IA {#seguridad-ia}

### 5.1 Prompts Seguros

```python
# ✅ SIEMPRE: Versionado de prompts
PROMPTS = {
    "chat_v1": {
        "system": """Eres un tutor experto en Seguridad Social española.
        REGLAS ESTRICTAS:
        - Solo responde sobre legislación española
        - Cita siempre el artículo y ley
        - Si no sabes, di "No tengo información suficiente"
        - NUNCA inventes información
        """,
        "version": "1.0.0",
        "created": "2025-11-27"
    }
}

# ✅ SIEMPRE: Delimitadores claros
def make_prompt(user_query: str, context: str) -> str:
    return f"""
    CONTEXTO:
    ---
    {context}
    ---
    
    PREGUNTA DEL USUARIO:
    ---
    {user_query}
    ---
    
    INSTRUCCIONES: Responde basándote SOLO en el contexto proporcionado.
    """
```

**Reglas**:
- ✅ Prompts versionados en repo
- ✅ Delimitadores claros (---, ###, etc.)
- ✅ Instrucciones anti-prompt injection
- ✅ Variables tipadas

### 5.2 Evaluación y Filtrado

```python
# ✅ SIEMPRE: Filtrado de PII antes de enviar a LLM
import re

PII_PATTERNS = {
    'dni': r'\b\d{8}[A-Z]\b',
    'email': r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',
    'phone': r'\b\d{9}\b',
}

def anonymize_pii(text: str) -> str:
    for pattern_name, pattern in PII_PATTERNS.items():
        text = re.sub(pattern, f"[{pattern_name.upper()}_REDACTED]", text, flags=re.I)
    return text

# ✅ SIEMPRE: Evaluación de outputs
def is_safe_output(text: str) -> bool:
    # Verificar PII leakage
    for pattern in PII_PATTERNS.values():
        if re.search(pattern, text, re.I):
            return False
    
    # Verificar toxicity (usar modelo pequeño)
    # toxicity_score = toxicity_classifier(text)
    # if toxicity_score > 0.8:
    #     return False
    
    return True
```

**Reglas**:
- ✅ No enviar PII a LLM sin anonimizar
- ✅ Loggear solo metadatos no sensibles
- ✅ Evaluación automática de outputs (PII, toxicity)
- ✅ Red teaming periódico (prompt injection tests)

### 5.3 Observabilidad de IA

```python
# ✅ SIEMPRE: Tracking completo
async def track_llm_call(
    user_id: str,
    feature: str,
    provider: str,
    model: str,
    tokens_input: int,
    tokens_output: int,
    latency_ms: float,
    cost: float = 0.0
):
    logger.info("LLM call completed", extra={
        "user_id": user_id,
        "feature": feature,
        "provider": provider,
        "model": model,
        "tokens_input": tokens_input,
        "tokens_output": tokens_output,
        "tokens_total": tokens_input + tokens_output,
        "latency_ms": latency_ms,
        "cost": cost,
        "timestamp": datetime.now().isoformat()
    })
```

**Reglas**:
- ✅ Tracking de latencia, tokens, coste por request
- ✅ Métricas por proveedor/modelo
- ✅ Cuotas diarias por usuario y globales
- ✅ Alertas de límites

---

## 🔍 6. RAG Y VECTORES {#rag}

### 6.1 Pipeline RAG

```python
# ✅ SIEMPRE: Pipeline completo
async def rag_search(query: str, top_k: int = 5) -> List[Chunk]:
    # 1. Limpieza/normalización
    clean_query = normalize_text(query)
    
    # 2. Embedding
    query_vector = await embedder.encode(clean_query)
    
    # 3. Búsqueda con filtros
    results = await qdrant_client.search(
        collection_name="leyes",
        query_vector=query_vector,
        limit=top_k * 3,  # Recuperar más para reranking
        score_threshold=0.5
    )
    
    # 4. Re-ranking (opcional)
    reranked = apply_hierarchical_boost(results)
    
    # 5. Trim a top-k
    return reranked[:top_k]
```

**Reglas**:
- ✅ Normalizar y limpiar textos
- ✅ Controlar encoding (UTF-8)
- ✅ Limitar K (no más de 10)
- ✅ Filtrar duplicados
- ✅ Attribution para grounding

### 6.2 Seguridad RAG

```python
# ✅ SIEMPRE: Filtrar PII al indexar
def prepare_chunk_for_indexing(text: str) -> str:
    # Limpiar PII
    text = anonymize_pii(text)
    
    # Validar encoding
    text = text.encode('utf-8', errors='ignore').decode('utf-8')
    
    # Normalizar espacios
    text = ' '.join(text.split())
    
    return text

# ✅ SIEMPRE: Control de acceso
async def search_with_access_control(
    query: str,
    user_id: str,
    allowed_collections: List[str]
):
    # Verificar permisos
    if collection not in allowed_collections:
        raise PermissionError("Acceso denegado")
    
    return await qdrant_client.search(...)
```

**Reglas**:
- ✅ Filtrar PII al indexar Y antes de enviar a LLM
- ✅ Control de acceso por colección/payload
- ✅ Evaluación continua de calidad (P@K, Recall@K)
- ✅ Alertas si baja la calidad

---

## 🧪 7. TESTING {#testing}

### 7.1 Estrategia de Tests

**Frontend (Vitest + Testing Library)**
```typescript
// ✅ Unit test: Utilidades puras
import { describe, it, expect } from 'vitest';
import { formatSummary } from '../utils/formatters';

describe('formatSummary', () => {
  it('should format summary with key points', () => {
    const result = formatSummary({ summary: 'Test' });
    expect(result).toContain('Test');
  });
});

// ✅ Integration test: Componentes con servicios
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

it('should send chat message', async () => {
  render(<ChatView />);
  await userEvent.type(screen.getByRole('textbox'), 'Hello');
  await userEvent.click(screen.getByRole('button', { name: /send/i }));
  await waitFor(() => {
    expect(screen.getByText(/respuesta/i)).toBeInTheDocument();
  });
});
```

**Backend (Pytest)**
```python
# ✅ Unit test: Funciones puras
def test_anonymize_pii():
    text = "Mi DNI es 12345678A"
    result = anonymize_pii(text)
    assert "12345678A" not in result
    assert "[DNI_REDACTED]" in result

# ✅ Integration test: Endpoints con mocks
@pytest.mark.asyncio
async def test_chat_endpoint(client, mock_llm):
    response = await client.post("/api/chat", json={
        "message": "Test",
        "conversation_id": "test-123"
    })
    assert response.status_code == 200
    assert "text" in response.json()
```

**Reglas**:
- ✅ Frontend: \u003e90% coverage (statements/branches/functions/lines)
- ✅ Backend: \u003e85% coverage en core (routers, agents, services)
- ✅ Unit tests para toda utilidad y función pura
- ✅ Integration tests para rutas con deps externos mockeadas
- ✅ E2E tests en entornos efímeros
- ✅ Snapshots y golden tests para prompts

---

## 📊 8. OBSERVABILIDAD {#observabilidad}

### 8.1 Logging Estructurado

```python
# ✅ SIEMPRE: Logs estructurados con correlation ID
import logging
import uuid
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar('request_id', default='')

@app.middleware("http")
async def add_correlation_id(request, call_next):
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Usar en logs
logger.info("Processing chat", extra={
    "request_id": request_id_var.get(),
    "user_id": user.id,
    "provider": provider
})
```

**Reglas**:
- ✅ 100% de requests con traceId/correlation ID
- ✅ Logs estructurados (JSON)
- ✅ Niveles apropiados (DEBUG/INFO/WARNING/ERROR)
- ✅ Nunca loggear secretos o PII

### 8.2 Métricas y Alertas

```python
# ✅ SIEMPRE: Métricas clave
from prometheus_client import Counter, Histogram

llm_requests = Counter('llm_requests_total', 'Total LLM requests', ['provider', 'model'])
llm_latency = Histogram('llm_latency_seconds', 'LLM latency', ['provider'])
llm_tokens = Counter('llm_tokens_total', 'Total tokens', ['provider', 'type'])

# Usar en código
llm_requests.labels(provider='groq', model='llama-3.3-70b').inc()
llm_latency.labels(provider='groq').observe(response_time)
llm_tokens.labels(provider='groq', type='input').inc(tokens_input)
```

**Reglas**:
- ✅ p50/p90/p99 latencia API y LLM
- ✅ Tokens por request y coste estimado
- ✅ Tasa de timeouts y fallbacks
- ✅ Calidad RAG (proxy)
- ✅ Alertas: Coste diario \u003e umbral, Error rate \u003e umbral

---

## 🚢 9. CI/CD Y DEPLOYMENT {#cicd}

### 9.1 Pipeline CI/CD

```yaml
# ✅ Pipeline recomendado
stages:
  - lint_and_type
  - test
  - security
  - build
  - deploy

lint_and_type:
  - npm run lint
  - npm run type-check
  - ruff check backend/
  - mypy backend/

test:
  - npm run test:coverage
  - pytest --cov=backend --cov-report=xml

security:
  - npm audit
  - pip-audit
  - git secrets --scan
  - trivy scan

build:
  - npm run build
  - docker build

deploy:
  - deploy canary (10%)
  - smoke tests
  - auto-rollback if fail
```

**Reglas**:
- ✅ Branch protection: 2 reviews, status checks obligatorios
- ✅ No merge sin pasar lint/type/test/coverage/scan
- ✅ Build reproducible con lockfiles
- ✅ Conventional Commits y CHANGELOG automatizado

### 9.2 Docker Seguro

```dockerfile
# ✅ SIEMPRE: Non-root user
FROM python:3.11-slim

WORKDIR /app

# Instalar deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# ✅ CRÍTICO: Crear usuario no-root
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:8000/health || exit 1

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Reglas**:
- ✅ Nunca ejecutar como root
- ✅ Multi-stage builds para tamaño mínimo
- ✅ Escaneo de vulnerabilidades (Trivy)
- ✅ SBOM generado

---

## ✅ 10. CHECKLIST DE PR {#checklist-pr}

### Seguridad
- [ ] Sin secretos hardcodeados
- [ ] Inputs/outputs validados (Zod/Pydantic)
- [ ] Sanitización de contenido IA (DOMPurify)
- [ ] Headers de seguridad (CSP, X-Frame-Options)
- [ ] CSRF protection donde aplique
- [ ] URLs validadas (whitelist para SSRF)
- [ ] Paths validados (no path traversal)

### Calidad
- [ ] Tests pasan (unit + integration)
- [ ] Cobertura no baja (Frontend \u003e90%, Backend \u003e85%)
- [ ] Snapshots actualizados
- [ ] Prompts versionados (si aplica)
- [ ] Sin warnings de ESLint/TypeScript
- [ ] Código formateado (Prettier/Black)

### Performance
- [ ] Sin queries sin índice
- [ ] Sin N+1 queries
- [ ] Sin renders innecesarios
- [ ] Caching usado apropiadamente
- [ ] Async I/O en backend

### Observabilidad
- [ ] Logs/metrics/traces añadidos para nuevas rutas
- [ ] Correlation IDs propagados
- [ ] Errores loggeados con contexto
- [ ] Métricas de IA trackeadas

### Documentación
- [ ] README/ARCHITECTURE actualizado (si aplica)
- [ ] ai-specs/specs actualizado (si aplica)
- [ ] Comentarios en decisiones de diseño críticas
- [ ] API docs actualizados (OpenAPI)

---

## 📚 REFERENCIAS

- **Estándares del proyecto**: `ai-specs/specs/*`
- **Arquitectura**: `docs/ARCHITECTURE.md`
- **RAG Best Practices**: `docs/RAG_BEST_PRACTICES_NOV2025.md`
- **Testing Strategy**: `docs/TESTING_STRATEGY.md`
- **Security Audit**: `docs/project-docs/security/AUDITORIA_SEGURIDAD_COMPLETA_27NOV2025.md`

---

**Versión**: 2.0 (Consolidada)  
**Última actualización**: 27 de Noviembre de 2025  
**Estado**: Normativo - Cumplimiento obligatorio
