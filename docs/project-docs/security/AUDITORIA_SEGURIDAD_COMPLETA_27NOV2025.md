# 🔒 INFORME DE AUDITORÍA DE SEGURIDAD
**Fecha**: 27 de Noviembre de 2025  
**Auditor**: Análisis exhaustivo basado en documento de estrategia de seguridad  
**Herramienta**: Aikido Security Scanner + Revisión manual

---

## 📊 RESUMEN EJECUTIVO

**Estado General**: 🔴 **CRÍTICO - Acción inmediata requerida**

Se han identificado **9 vulnerabilidades** de las cuales:
- 🔴 **4 CRÍTICAS** (XSS sin sanitización)
- 🟡 **3 MEDIAS** (SSRF, Path Traversal, Docker root)
- 🟢 **2 BAJAS** (Dependencias obsoletas)

**Nivel de cumplimiento de reglas de oro**: ❌ **40%** (4 de 10 reglas críticas NO cumplidas)

---

## 🚨 VULNERABILIDADES DETECTADAS

### 1. XSS via dangerouslySetInnerHTML ⭐⭐⭐⭐⭐ CRÍTICO

**Estado**: ❌ **PRESENTE EN 4 COMPONENTES**  
**Severidad**: 🔴 **ALTA**  
**CVSS**: 7.5 (High)

#### Componentes Afectados:

**1.1 ChatView.tsx - Línea 263**
```typescript
dangerouslySetInnerHTML={{ __html: msg.text.replace(/\n/g, '<br />') }}
```
- **Riesgo**: Mensajes de IA pueden contener HTML/JS malicioso
- **Vector de ataque**: Prompt injection → XSS
- **Impacto**: Robo de sesión, phishing, defacement

**1.2 ComparatorView.tsx - Línea 137**
```typescript
dangerouslySetInnerHTML={{ __html: comparison.replace(/\n/g, '<br />') }}
```
- **Riesgo**: Comparaciones pueden inyectar scripts
- **Vector de ataque**: Texto malicioso en archivos subidos
- **Impacto**: XSS stored

**1.3 SchemaView.tsx - Línea 132**
```typescript
dangerouslySetInnerHTML={{ __html: parseSchemaToHtml(schema) }}
```
- **Riesgo**: Parser HTML personalizado sin sanitización
- **Vector de ataque**: Esquemas generados con HTML malicioso
- **Impacto**: XSS reflected

**1.4 SummaryView.tsx - Línea 124**
```typescript
dangerouslySetInnerHTML={{ __html: summary.replace(/\n/g, '<br />') }}
```
- **Riesgo**: Resúmenes de IA sin sanitización
- **Vector de ataque**: Documentos maliciosos → resumen XSS
- **Impacto**: XSS stored

#### Solución Recomendada:
```typescript
// INSTALAR: npm install dompurify @types/dompurify
import DOMPurify from 'dompurify';

// USAR EN TODOS LOS COMPONENTES:
dangerouslySetInnerHTML={{ 
  __html: DOMPurify.sanitize(msg.text.replace(/\n/g, '<br />'), {
    ALLOWED_TAGS: ['br', 'p', 'strong', 'em', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: []
  })
}}
```

**Regla de Oro Violada**:
> ✅ Sanitiza absolutamente toda la entrada (usuario y proveedores IA). Escapa HTML/Markdown.

---

### 2. Docker Container Running as Root ⭐⭐⭐ MEDIO

**Estado**: ❌ **PRESENTE**  
**Archivo**: `backend/Dockerfile`  
**Severidad**: 🟡 **MEDIA**

#### Problema:
```dockerfile
# NO HAY USER STATEMENT
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Riesgo:
- Container ejecuta como root
- Si hay exploit en la app → acceso root al host
- Escalación de privilegios facilitada

#### Solución:
```dockerfile
# Añadir ANTES del CMD:
RUN adduser --disabled-password --gecos '' appuser
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Regla de Oro Violada**:
> ✅ Aplica "least privilege" y rotación de credenciales.

---

### 3. SSRF (Server-Side Request Forgery) ⭐⭐⭐ MEDIO

**Estado**: ❌ **PRESENTE EN 8 ARCHIVOS**  
**Severidad**: 🟡 **MEDIA**

#### Archivos Afectados:
1. `backend/agents/download_lgss_only.py:29`
2. `backend/agents/download_and_index_3_leyes_criticas.py:109`
3. `backend/agents/index_rd_cotizacion_final.py:74`
4. `backend/agents/boe_downloader.py:80`
5. `backend/agents/download_constitucion.py:29`
6. `backend/agents/fix_rd_cotizacion.py:39`
7. `backend/agents/download_and_index_leyes_restantes.py:181`
8. `backend/migrate_qdrant_to_cloud.py:43`

#### Código Vulnerable:
```python
response = requests.get(ley['url'], timeout=180)
```

#### Riesgo:
- URLs controladas por datos externos
- Posible acceso a metadata service (169.254.169.254)
- Lectura de servicios internos
- Bypass de firewall

#### Solución:
```python
from urllib.parse import urlparse

ALLOWED_DOMAINS = ['boe.es', 'www.boe.es']
BLOCKED_IPS = ['127.0.0.1', 'localhost', '0.0.0.0', '169.254.169.254']

def safe_request(url: str, timeout: int = 60):
    parsed = urlparse(url)
    
    # Validar dominio
    if parsed.netloc not in ALLOWED_DOMAINS:
        raise ValueError(f"Dominio no permitido: {parsed.netloc}")
    
    # Validar esquema
    if parsed.scheme not in ['http', 'https']:
        raise ValueError(f"Esquema no permitido: {parsed.scheme}")
    
    # Hacer request con validación
    response = requests.get(url, timeout=timeout, allow_redirects=False)
    return response
```

**Regla de Oro Violada**:
> ✅ If possible, only allow requests to allowlisting domains.

---

### 4. Path Traversal en open() ⭐⭐⭐ MEDIO

**Estado**: ❌ **PRESENTE**  
**Archivo**: `backend/agents/pdf_processor.py:38`  
**Severidad**: 🟡 **MEDIA**

#### Código Vulnerable:
```python
with open(pdf_path, 'rb') as file:
    pdf_reader = pypdf.PdfReader(file)
```

#### Riesgo:
- Si `pdf_path` es controlable por usuario
- Lectura de archivos sensibles (/etc/passwd, .env, etc.)
- Información disclosure

#### Solución:
```python
from pathlib import Path
import os

ALLOWED_PDF_DIR = Path("/app/data/leyes")

def safe_open_pdf(pdf_path: str):
    # Resolver path absoluto
    abs_path = Path(pdf_path).resolve()
    
    # Verificar que está dentro del directorio permitido
    if not str(abs_path).startswith(str(ALLOWED_PDF_DIR)):
        raise ValueError(f"Path no permitido: {pdf_path}")
    
    # Verificar que existe y es archivo
    if not abs_path.is_file():
        raise FileNotFoundError(f"Archivo no encontrado: {pdf_path}")
    
    with open(abs_path, 'rb') as file:
        return pypdf.PdfReader(file)
```

**Regla de Oro Violada**:
> ✅ Ignore this issue only after you've verified or sanitized the input going into this function.

---

### 5. Secret Expuesto en Git History ⭐⭐ BAJO

**Estado**: 🟡 **PARCIALMENTE RESUELTO**  
**Archivo**: `backend/migrate_qdrant_simple.py` (ELIMINADO)  
**Severidad**: 🟢 **BAJA** (archivo eliminado pero en historial)

#### Problema:
- Secret `*****UGGU` detectado en commit histórico
- Archivo ya no existe en versión actual
- Pero sigue en historial de Git

#### Riesgo:
- Si alguien tiene acceso al repo → puede ver el secret
- Posible compromiso de Qdrant Cloud

#### Solución:
```bash
# 1. Rotar la API key de Qdrant Cloud INMEDIATAMENTE
# 2. Limpiar historial de Git (opcional, complejo):
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/migrate_qdrant_simple.py" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Forzar push (CUIDADO - afecta a todos):
git push origin --force --all
```

**Regla de Oro Violada**:
> ✅ Nunca hardcodees secretos. Valida process.env/os.environ con esquema al iniciar.

---

### 6. python-multipart DoS Vulnerability ⭐ BAJO

**Estado**: ❌ **PRESENTE**  
**Dependencia**: `python-multipart==0.0.9`  
**CVE**: CVE-2024-53981  
**Severidad**: 🟢 **BAJA**

#### Problema:
- Versión vulnerable a DoS con multipart requests maliciosos
- Puede causar agotamiento de recursos

#### Solución:
```bash
# En requirements.txt cambiar:
python-multipart==0.0.9  # VULNERABLE
# Por:
python-multipart==0.0.18  # FIXED
```

---

### 7. pypdf DoS Vulnerability ⭐ BAJO

**Estado**: ❌ **PRESENTE**  
**Dependencia**: `pypdf==5.1.0`  
**Severidad**: 🟢 **BAJA**

#### Problema:
- Vulnerable a decompression bomb (PDF → 1 PB)
- Puede agotar memoria del servidor

#### Solución:
```bash
# Actualizar a versión parcheada:
pip install --upgrade pypdf
```

---

### 8. python-jose Information Disclosure ⭐ BAJO

**Estado**: ❌ **PRESENTE**  
**Dependencia**: `python-jose==3.3.0`  
**Severidad**: 🟢 **BAJA**

#### Problema:
- Errores JWKError exponen datos de claves
- Posible información disclosure en JWT

#### Solución:
```bash
# Actualizar a versión parcheada:
python-jose==3.5.0
```

---

## ✅ CUMPLIMIENTO DE REGLAS DE ORO

### Reglas CUMPLIDAS ✅ (6/10)

1. ✅ **Tipado y validación**: Pydantic en backend, TypeScript en frontend
2. ✅ **Errores y resiliencia**: Retry con backoff implementado (Sprint 10)
3. ✅ **Código limpio**: ESLint, Prettier, refactoring Sprint 10
4. ✅ **Tests como contrato**: Vitest configurado, tests unitarios presentes
5. ✅ **Documentación**: docs/ actualizado, ARCHITECTURE.md presente
6. ✅ **Observabilidad parcial**: Logs estructurados, correlation IDs pendientes

### Reglas NO CUMPLIDAS ❌ (4/10)

1. ❌ **Seguridad primero**: 
   - Secretos hardcodeados en historial
   - Sin sanitización XSS
   - Sin validación de URLs (SSRF)

2. ❌ **IA segura y controlada**:
   - Sin DOMPurify para outputs de IA
   - Sin evaluación de toxicity/PII
   - Prompts no versionados

3. ❌ **RAG confiable**:
   - Sin filtrado de PII al indexar
   - Sin control de acceso a colecciones
   - Sin validación de encoding

4. ❌ **Observabilidad y costes**:
   - Sin OpenTelemetry
   - Sin tracking de tokens (CRÍTICO)
   - Sin cuotas/alertas

---

## 🎯 PLAN DE REMEDIACIÓN PRIORIZADO

### FASE 1: CRÍTICO (Esta semana)

**Día 1-2: Fix XSS**
```bash
# 1. Instalar DOMPurify
npm install dompurify @types/dompurify

# 2. Crear utilidad de sanitización
# utils/sanitize.ts
import DOMPurify from 'dompurify';

export const sanitizeHTML = (html: string): string => {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['br', 'p', 'strong', 'em', 'ul', 'ol', 'li', 'code', 'pre'],
    ALLOWED_ATTR: ['class']
  });
};

# 3. Aplicar en los 4 componentes
# ChatView.tsx, ComparatorView.tsx, SchemaView.tsx, SummaryView.tsx
```

**Día 3: Fix Docker + Dependencias**
```bash
# 1. Actualizar Dockerfile
# 2. Actualizar requirements.txt:
python-multipart==0.0.18
python-jose==3.5.0
pypdf>=5.2.0  # Última versión
```

**Día 4: Rotar Secrets**
```bash
# 1. Generar nueva API key en Qdrant Cloud
# 2. Actualizar .env
# 3. Verificar que no hay otros secrets expuestos
git secrets --scan-history
```

### FASE 2: IMPORTANTE (Próxima semana)

**Día 5-7: Fix SSRF + Path Traversal**
```python
# 1. Crear utils/safe_requests.py con whitelist
# 2. Crear utils/safe_file_access.py con path validation
# 3. Refactorizar los 8 archivos afectados
```

### FASE 3: MEJORAS (Semana 3)

**Implementar reglas faltantes**:
1. Sistema de tracking de tokens (ya en roadmap)
2. OpenTelemetry para observabilidad
3. Versionado de prompts
4. Filtrado de PII en RAG

---

## 📊 MÉTRICAS DE ÉXITO

### Antes de Remediación
- ❌ Vulnerabilidades críticas: 4
- ❌ Cumplimiento reglas: 60%
- ❌ DOMPurify instalado: No
- ❌ Secrets en historial: Sí

### Después de Remediación (Objetivo)
- ✅ Vulnerabilidades críticas: 0
- ✅ Cumplimiento reglas: 90%+
- ✅ DOMPurify instalado: Sí
- ✅ Secrets rotados: Sí
- ✅ Docker non-root: Sí
- ✅ SSRF mitigado: Sí

---

## 🔍 FALSOS POSITIVOS

**Aikido reportó**: "Service not internet-connected" en varios issues

**Análisis**: ✅ **CORRECTO - NO son falsos positivos**
- La app SÍ está conectada a internet
- Descarga PDFs del BOE
- Hace requests a URLs externas
- El downgrade de severidad es INCORRECTO

**Conclusión**: Todas las vulnerabilidades son REALES y deben ser corregidas.

---

## 📝 RECOMENDACIONES ADICIONALES

### 1. Implementar CSP (Content Security Policy)
```python
# backend/main.py
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["opositaia.com", "*.opositaia.com"]
)

# Añadir headers de seguridad
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response
```

### 2. Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: Request):
    ...
```

### 3. Input Validation con Pydantic
```python
from pydantic import BaseModel, validator

class ChatRequest(BaseModel):
    message: str
    
    @validator('message')
    def validate_message(cls, v):
        if len(v) > 10000:
            raise ValueError('Mensaje demasiado largo')
        if '<script' in v.lower():
            raise ValueError('Contenido no permitido')
        return v
```

---

**Fin del Informe**

**Próximo paso**: Iniciar FASE 1 de remediación (Fix XSS crítico)
