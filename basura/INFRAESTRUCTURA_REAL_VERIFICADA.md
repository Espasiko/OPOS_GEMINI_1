# 🔍 INFRAESTRUCTURA REAL VERIFICADA

**Fecha**: 20 Noviembre 2025  
**Verificación**: SSH + Docker + Health Checks

---

## ✅ VPS HOSTINGER (147.93.95.67)

### Acceso
- **IP**: 147.93.95.67
- **Dominio**: electroyhogarpelotazo.tienda
- **Usuario**: root
- **Contraseña**: Mamkavigadna?1 (ver `.credentials.local`)
- **Puerto SSH**: 22

### Servicios Corriendo ✅

**1. FastAPI opositor-api**
- **Status**: ✅ Active (running)
- **Uptime**: 3 semanas 4 días
- **Puerto**: 8001 (interno)
- **Workers**: 2
- **Memory**: 823.2 MB
- **Path**: `/home/ubuntu/opositor_agent/`
- **Servicio**: `opositor-api.service`
- **Health**: http://127.0.0.1:8001/health → `{"status":"ok","version":"0.1.0"}`

**2. Nginx**
- **Status**: ✅ Corriendo
- **Dominio**: https://electroyhogarpelotazo.tienda
- **SSL**: Let's Encrypt
- **Config**: `/etc/nginx/sites-enabled/opositor-api.conf`
- **Proxy**: 127.0.0.1:8001 → electroyhogarpelotazo.tienda

### Servicios Adicionales ✅

**3. Mistral 7B (llama.cpp)**
- **Status**: ✅ CORRIENDO (PID 964)
- **Modelo**: mistral-7b-instruct-v0.1.Q4_K_M.gguf (4.1 GB)
- **Ubicación**: `/home/ubuntu/opositor_ia/`
- **Puerto**: 8080 (interno)
- **Host**: 0.0.0.0
- **Uptime**: Desde Oct 26 (casi 1 mes)
- **Servidor**: llama_cpp.server
- **Contexto**: 8192 tokens
- **Threads**: 4
- **API**: Compatible con OpenAI (v1/models, v1/chat/completions)
- **Health**: http://localhost:8080/v1/models → `{"object":"list","data":[{"id":"mistral",...}]}`

**4. Ollama**
- **Status**: ❌ NO instalado como servicio
- **Nota**: Hay librerías Python de ollama en venv, pero no el servidor

### Estructura del Proyecto VPS

```
/home/ubuntu/opositor_agent/
├── api-venv/              # Virtual environment
├── apps/                  # Applications
├── credentials/           # Credentials
├── data/                  # Data storage
├── docs/                  # Documentation
├── logs/                  # Logs
├── opositor_agent/        # Main app
├── vector_store/          # Vector storage
├── venv/                  # Another venv
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── README.md
```

---

## ✅ LOCAL (WSL en PC Windows)

### Docker Containers Corriendo

**1. Qdrant**
- **Container**: opositaia-qdrant
- **Image**: qdrant/qdrant:latest
- **Status**: ✅ Up 2 days (unhealthy)
- **Puertos**: 0.0.0.0:6333-6334 → 6333-6334/tcp
- **Datos**: 7,833 chunks indexados
- **Colecciones**: opositaia_leyes_seguridad_social

**2. Ollama**
- **Container**: ollama-starter
- **Image**: ollama/ollama
- **Status**: ✅ Up 2 days
- **Puerto**: 0.0.0.0:11434 → 11434/tcp
- **Modelos instalados**:
  - tinyllama:latest (637 MB)
  - all-minilm:latest (45 MB)

**3. PostgreSQL + pgvector**
- **Container**: sim_old-db-1
- **Image**: pgvector/pgvector:pg17
- **Status**: ✅ Up 2 days (healthy)
- **Puerto**: 0.0.0.0:5432 → 5432/tcp

### Servicios NO Docker

**Backend FastAPI**
- **Status**: ✅ Corriendo
- **Puerto**: 8000
- **Path**: `E:\1\OPOS_GEMINI_1\backend`
- **Venv**: `elemplos_leyes_info/venv`
- **Health**: http://localhost:8000/health → `{"status":"healthy"}`

---

## 🔍 VERIFICACIÓN DE ENDPOINTS

### Backend Local (localhost:8000)

**Health Check**:
```bash
curl http://localhost:8000/health
```
**Respuesta**:
```json
{
  "status": "healthy",
  "embedding_model": "PlanTL-GOB-ES/RoBERTalex",
  "qdrant_url": "http://localhost:6333",
  "ollama_url": "http://localhost:11434"
}
```

**Chat Health**:
```bash
curl http://localhost:8000/chat/health
```
**Respuesta esperada**:
```json
{
  "status": "degraded",
  "mistral": "down",  // VPS no tiene Mistral
  "rag": "up",
  "mistral_url": "http://147.93.95.67:8001",
  "model": "mistral-8b"
}
```

### VPS API (electroyhogarpelotazo.tienda)

**Health Check**:
```bash
ssh root@147.93.95.67 "curl -s http://127.0.0.1:8001/health"
```
**Respuesta**:
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

## ⚠️ PROBLEMA IDENTIFICADO

### Backend Apunta al Puerto Incorrecto

**Configuración actual** (`backend/routers/chat.py`):
```python
MISTRAL_URL = os.getenv("MISTRAL_URL", "http://147.93.95.67:8001")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-8b")
```

**Realidad**:
- ✅ VPS SÍ tiene Mistral 7B instalado
- ✅ Mistral está corriendo en puerto **8080** (NO 8001)
- ❌ Backend apunta al puerto **8001** (FastAPI opositor-api)
- ✅ Mistral usa llama.cpp server (compatible OpenAI API)

### Solución: Cambiar Puerto en Backend

**Cambio necesario** en `backend/routers/chat.py` o `.env.backend`:

```python
# ANTES (INCORRECTO)
MISTRAL_URL = "http://147.93.95.67:8001"  # ← FastAPI, NO Mistral
MISTRAL_MODEL = "mistral-8b"

# DESPUÉS (CORRECTO)
MISTRAL_URL = "http://147.93.95.67:8080"  # ← Mistral llama.cpp
MISTRAL_MODEL = "mistral"  # ← Nombre del modelo en llama.cpp
```

**O en `.env.backend`**:
```bash
MISTRAL_URL=http://147.93.95.67:8080
MISTRAL_MODEL=mistral
```

**Verificar que funciona**:
```bash
curl http://147.93.95.67:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral",
    "messages": [{"role": "user", "content": "Hola"}],
    "max_tokens": 100
  }'
```

---

## 📊 RESUMEN DE SERVICIOS

### ✅ Funcionando

| Servicio | Ubicación | Puerto | Status |
|----------|-----------|--------|--------|
| Qdrant | WSL Docker | 6333 | ✅ Up (unhealthy) |
| Ollama | WSL Docker | 11434 | ✅ Up |
| PostgreSQL | WSL Docker | 5432 | ✅ Up (healthy) |
| Backend FastAPI | WSL | 8000 | ✅ Running |
| VPS FastAPI | VPS | 8001 | ✅ Running |
| Nginx | VPS | 80/443 | ✅ Running |

### ❌ NO Instalado

| Servicio | Ubicación | Razón |
|----------|-----------|-------|
| Mistral 8B | VPS | NO instalado |
| Ollama | VPS | NO instalado |

---

## 🎯 PRÓXIMOS PASOS

### Inmediato (HOY)
1. ✅ Verificar infraestructura (COMPLETADO)
2. ⏰ Decidir: ¿Instalar Mistral en VPS o usar Ollama local?
3. ⏰ Actualizar configuración backend según decisión

### Opción Recomendada: Instalar Ollama + Mistral en VPS

**Ventajas**:
- ✅ Producción real (no depende de PC local)
- ✅ Disponible 24/7
- ✅ Mejor latencia para usuarios
- ✅ Escalable

**Pasos**:
```bash
# 1. Conectar al VPS
ssh root@147.93.95.67

# 2. Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 3. Descargar Mistral
ollama pull mistral

# 4. Verificar
ollama list
systemctl status ollama

# 5. Probar
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Hola"
}'
```

---

## 📝 NOTAS IMPORTANTES

1. **VPS NO tiene Mistral**: El backend espera Mistral en `147.93.95.67:8001` pero NO está instalado.

2. **Ollama Local SÍ funciona**: Podemos usar `localhost:11434` temporalmente.

3. **vpsService.ts apunta al dominio correcto**: `electroyhogarpelotazo.tienda` es tu VPS real.

4. **backendService.ts SÍ intenta usar Mistral**: Pero falla porque no está instalado.

5. **Contraseña SSH guardada**: En `.credentials.local` (NO en Git).

---

**Documento creado**: 20 Noviembre 2025  
**Verificación**: SSH + Docker + Health Checks  
**Estado**: Infraestructura verificada, Mistral pendiente de instalar

