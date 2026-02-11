# 🔍 ARQUITECTURA REAL DEL VPS - AUDITORIA 22/01/2026

**IP del VPS:** `147.93.95.67`  
**Hostname:** `srv838554`  
**Dominio:** `electroyhogarpelotazo.tienda`  
**Sistema Operativo:** Ubuntu Server  
**RAM Total:** 7.8 GB (6.0 GB usados, 1.7 GB disponibles)  
**Disco:** 96 GB (26 GB usados, 71 GB libres - 27% uso)  
**Swap:** 2.0 GB (268 MB usados)

---

## 🔐 CONEXIÓN SSH

### Comando de Conexión
```bash
ssh root@147.93.95.67
```

**Usuario principal:** `root`  
**Usuario de aplicación:** `ubuntu` (UID 1000)  
**Directorio home:** `/home/ubuntu`

### Verificación de Conexión
```bash
# Test básico
ssh root@147.93.95.67 "hostname && whoami"

# Salida esperada:
# srv838554
# root
```

---

## 🏗️ ARQUITECTURA DE SERVICIOS

### 1. **Llama.cpp Server** (Salamandra 7B)

**Estado:** ✅ **ACTIVO** (corriendo desde 10 de enero)

**Servicio systemd:**
```bash
systemctl status llama-server.service
```

**Configuración:**
- **Archivo:** `/etc/systemd/system/llama-server.service`
- **Usuario:** `ubuntu`
- **Comando:** `/usr/local/bin/llama-server`
- **Modelo:** `/home/ubuntu/models/salamandra-7b-instruct-Q4_K_M.gguf`
- **Tamaño del modelo:** 4.6 GB
- **Puerto:** `8080` (escucha en `0.0.0.0`)
- **Contexto:** 8192 tokens
- **Memoria usada:** ~5.7 GB
- **PID:** 1247170

**Endpoints internos (llama.cpp):**
```bash
# Health check
curl http://127.0.0.1:8080/health
# Respuesta: {"status":"ok"}

# Listar modelos
curl http://127.0.0.1:8080/v1/models

# Completions (OpenAI compatible)
curl http://127.0.0.1:8080/v1/completions
curl http://127.0.0.1:8080/v1/chat/completions
```

**Acceso externo (vía nginx):**
```bash
# Endpoint público para llama.cpp
https://electroyhogarpelotazo.tienda/v1/models
https://electroyhogarpelotazo.tienda/v1/chat/completions
```

---

### 2. **Salamandra FastAPI** (Wrapper)

**Estado:** ✅ **ACTIVO** (corriendo desde 10 de enero)

**Servicio systemd:**
```bash
systemctl status salamandra-api.service
```

**Configuración:**
- **Archivo:** `/etc/systemd/system/salamandra-api.service`
- **Usuario:** `ubuntu`
- **Directorio:** `/home/ubuntu/salamandra-api/`
- **Comando:** `uvicorn main:app --host 127.0.0.1 --port 8001 --workers 1`
- **Puerto:** `8001` (solo localhost)
- **Memoria usada:** ~37 MB
- **PID:** 1236413

**Código del servidor:**
```python
# /home/ubuntu/salamandra-api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import requests

app = FastAPI(title="Salamandra API", version="1.0.0")

class SalamandraRequest(BaseModel):
    question: str
    context: str
    options: Dict[str, str]

@app.get("/health")
async def health():
    return {"status": "ok", "service": "salamandra-api"}

@app.post("/salamandra/reason")
async def salamandra_reason(request: SalamandraRequest):
    # Llama a Ollama local en puerto 11434 (NO FUNCIONA - Ollama no instalado)
    # En realidad debería llamar a llama.cpp en puerto 8080
    pass
```

**⚠️ PROBLEMA DETECTADO:** El código intenta llamar a Ollama en puerto 11434, pero Ollama NO está instalado. Debería llamar directamente a llama.cpp en puerto 8080.

**Endpoints públicos (vía nginx):**
```bash
# Health check
curl https://electroyhogarpelotazo.tienda/health
# Respuesta: {"status":"ok","service":"salamandra-api"}

# Razonamiento con Salamandra
curl -X POST https://electroyhogarpelotazo.tienda/salamandra/reason \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuál es el plazo de prescripción?",
    "context": "Art. 43 LGSS...",
    "options": {"a": "4 años", "b": "5 años", "c": "10 años"}
  }'

# Swagger UI
https://electroyhogarpelotazo.tienda/docs
```

---

### 3. **Nginx (Reverse Proxy)**

**Estado:** ✅ **ACTIVO**

**Configuración:** `/etc/nginx/sites-enabled/opositor-api.conf`

**Certificado SSL:** Let's Encrypt (válido)
- **Certificado:** `/etc/letsencrypt/live/electroyhogarpelotazo.tienda/fullchain.pem`
- **Clave privada:** `/etc/letsencrypt/live/electroyhogarpelotazo.tienda/privkey.pem`

**Rutas configuradas:**

#### HTTP (Puerto 80)
```nginx
server {
  listen 80;
  server_name electroyhogarpelotazo.tienda;
  
  location / {
    proxy_pass http://127.0.0.1:8001;  # FastAPI Salamandra
    proxy_read_timeout 900s;
  }
}
```

#### HTTPS (Puerto 443)
```nginx
server {
  listen 443 ssl http2;
  server_name electroyhogarpelotazo.tienda;
  
  # SSL configurado con Let's Encrypt
  
  location / {
    proxy_pass http://127.0.0.1:8001;  # FastAPI Salamandra
    proxy_read_timeout 900s;
  }
  
  location /explain/stream {
    proxy_pass http://127.0.0.1:8001/explain/stream;
    # Configuración especial para streaming
  }
  
  location /v1/ {
    proxy_pass http://127.0.0.1:8080/v1/;  # Llama.cpp directo
    proxy_read_timeout 900s;
  }
}
```

**Timeouts configurados:**
- `proxy_connect_timeout`: 120s
- `proxy_send_timeout`: 900s (15 minutos)
- `proxy_read_timeout`: 900s (15 minutos)
- `send_timeout`: 900s

---

## 📡 ENDPOINTS DISPONIBLES

### Endpoints Públicos (HTTPS)

| Endpoint | Método | Descripción | Servicio Backend |
|----------|--------|-------------|------------------|
| `https://electroyhogarpelotazo.tienda/health` | GET | Health check FastAPI | salamandra-api:8001 |
| `https://electroyhogarpelotazo.tienda/docs` | GET | Swagger UI | salamandra-api:8001 |
| `https://electroyhogarpelotazo.tienda/salamandra/reason` | POST | Razonamiento con Salamandra | salamandra-api:8001 |
| `https://electroyhogarpelotazo.tienda/v1/models` | GET | Listar modelos llama.cpp | llama-server:8080 |
| `https://electroyhogarpelotazo.tienda/v1/chat/completions` | POST | Chat completions (OpenAI API) | llama-server:8080 |
| `https://electroyhogarpelotazo.tienda/v1/completions` | POST | Text completions | llama-server:8080 |

### Endpoints Internos (Solo VPS)

| Endpoint | Puerto | Servicio |
|----------|--------|----------|
| `http://127.0.0.1:8001/health` | 8001 | Salamandra FastAPI |
| `http://127.0.0.1:8001/salamandra/reason` | 8001 | Salamandra FastAPI |
| `http://127.0.0.1:8080/health` | 8080 | Llama.cpp Server |
| `http://127.0.0.1:8080/v1/models` | 8080 | Llama.cpp Server |
| `http://127.0.0.1:8080/v1/chat/completions` | 8080 | Llama.cpp Server |

### Puertos Externos Bloqueados

⚠️ **IMPORTANTE:** Los puertos 8001 y 8080 NO son accesibles directamente desde fuera del VPS. Solo se puede acceder vía nginx (puerto 80/443).

```bash
# ❌ NO FUNCIONA (puerto bloqueado por firewall)
curl http://147.93.95.67:8080/health

# ✅ FUNCIONA (vía nginx)
curl https://electroyhogarpelotazo.tienda/v1/models
```

---

## 🧠 MODELO SALAMANDRA

**Ubicación:** `/home/ubuntu/models/salamandra-7b-instruct-Q4_K_M.gguf`  
**Tamaño:** 4.6 GB  
**Formato:** GGUF (Q4_K_M quantization)  
**Parámetros:** 7.77B  
**Contexto máximo:** 8192 tokens  
**Vocabulario:** 256,000 tokens

**Modelfile (Ollama - NO USADO):**
```bash
# /home/ubuntu/Modelfile
FROM ./salamandra-7b.gguf

TEMPLATE """<|im_start|>system
{{ .System }}<|im_end|>
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""

PARAMETER stop "<|im_start|>"
PARAMETER stop "<|im_end|>"
PARAMETER temperature 0.1
PARAMETER num_ctx 4096

SYSTEM "Eres un asistente experto en legislación y oposiciones del Estado español."
```

**Información del modelo (desde llama.cpp):**
```json
{
  "id": "salamandra-7b-instruct-Q4_K_M.gguf",
  "object": "model",
  "owned_by": "llamacpp",
  "meta": {
    "vocab_type": 1,
    "n_vocab": 256000,
    "n_ctx_train": 8192,
    "n_embd": 4096,
    "n_params": 7768117248,
    "size": 4844109824
  }
}
```

---

## 🚫 SERVICIOS NO ACTIVOS

### Ollama
**Estado:** ❌ **NO INSTALADO**

- No está en PATH
- No responde en puerto 11434
- No hay servicio systemd `ollama.service`

**Implicación:** El código de `salamandra-api` que intenta llamar a Ollama en puerto 11434 **FALLARÁ**.

### Servicio opositor-api.service
**Estado:** ❌ **INACTIVO** (detenido desde 8 de enero)

**Configuración:** `/etc/systemd/system/opositor-api.service`
```ini
[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/opositor_agent/apps/api
ExecStart=/home/ubuntu/opositor_agent/api-venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001
```

**Problema:** El directorio `/home/ubuntu/opositor_agent/apps/api/` **NO EXISTE**.

---

## 📂 ESTRUCTURA DE DIRECTORIOS

```
/home/ubuntu/
├── models/
│   └── salamandra-7b-instruct-Q4_K_M.gguf (4.6 GB)
├── salamandra-api/
│   ├── main.py (FastAPI app)
│   ├── venv/ (Python virtual environment)
│   └── ... 
├── opositor_ia/
│   ├── server.py
│   ├── venv/
│   └── llama_server.log
├── Modelfile (Ollama config - no usado)
├── salamandra_fixed.json
└── salamandra_response.json
```

**Directorios que NO existen:**
- `/home/ubuntu/opositor_agent/` ❌
- `/home/ubuntu/opositor_agent/apps/api/` ❌

---

## 🔧 COMANDOS ÚTILES

### Gestión de Servicios

```bash
# Ver estado de servicios
ssh root@147.93.95.67 "systemctl status llama-server.service"
ssh root@147.93.95.67 "systemctl status salamandra-api.service"

# Reiniciar servicios
ssh root@147.93.95.67 "systemctl restart llama-server.service"
ssh root@147.93.95.67 "systemctl restart salamandra-api.service"

# Ver logs
ssh root@147.93.95.67 "journalctl -u llama-server.service -n 50"
ssh root@147.93.95.67 "journalctl -u salamandra-api.service -n 50"
```

### Monitoreo de Recursos

```bash
# Memoria y CPU
ssh root@147.93.95.67 "free -h"
ssh root@147.93.95.67 "top -b -n 1 | head -20"

# Disco
ssh root@147.93.95.67 "df -h"

# Procesos de IA
ssh root@147.93.95.67 "ps aux | grep -E 'llama|uvicorn' | grep -v grep"

# Puertos abiertos
ssh root@147.93.95.67 "ss -tlnp | grep -E '8001|8080'"
```

### Testing de Endpoints

```bash
# Desde local (vía HTTPS)
curl https://electroyhogarpelotazo.tienda/health
curl https://electroyhogarpelotazo.tienda/v1/models

# Desde VPS (interno)
ssh root@147.93.95.67 "curl -s http://127.0.0.1:8001/health"
ssh root@147.93.95.67 "curl -s http://127.0.0.1:8080/health"

# Test completo de Salamandra
curl -X POST https://electroyhogarpelotazo.tienda/salamandra/reason \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuál es el plazo de IT por EC?",
    "context": "Art. 173 LGSS: La IT por EC tiene un plazo máximo de 365 días prorrogables 180 más.",
    "options": {
      "a": "365 días",
      "b": "545 días",
      "c": "730 días",
      "d": "180 días"
    }
  }'
```

---

## ⚠️ PROBLEMAS DETECTADOS

### 1. **Salamandra API llama a Ollama inexistente**

**Problema:** El código en `/home/ubuntu/salamandra-api/main.py` intenta conectar a:
```python
# Línea 48
response = requests.post(
    "http://127.0.0.1:11434/v1/chat/completions",  # ❌ Ollama no existe
    ...
)
```

**Solución:** Cambiar a:
```python
# Línea 48 - Cambiar puerto
response = requests.post(
    "http://127.0.0.1:8080/v1/chat/completions",  # ✅ Llama.cpp
    ...
)
```

**También cambiar:**
- **Línea 38:** `"model": "salamandra-opos:optimized"` → `"model": "salamandra-7b-instruct-Q4_K_M.gguf"`
- **Línea 60:** `"model_used": "salamandra-opos:optimized"` → `"model_used": "salamandra-7b-instruct-Q4_K_M.gguf"`

### 2. **Servicio opositor-api.service roto**

**Problema:** El servicio apunta a un directorio inexistente.

**Solución:** Deshabilitar o eliminar el servicio:
```bash
ssh root@147.93.95.67 "systemctl disable opositor-api.service"
```

### 3. **Modelo Ollama referenciado pero no existe**

**Problema:** El código usa `model: "salamandra-opos:optimized"` que es un tag de Ollama.

**Solución:** Usar el nombre del modelo GGUF directamente:
```python
# En lugar de:
"model": "salamandra-opos:optimized"

# Usar:
"model": "salamandra-7b-instruct-Q4_K_M.gguf"
```


---

## ✅ RECOMENDACIONES

### Inmediatas

1. **Corregir salamandra-api para usar llama.cpp:**
   ```bash
   ssh root@147.93.95.67
   cd /home/ubuntu/salamandra-api
   nano main.py  # Cambiar puerto 11434 → 8080
   systemctl restart salamandra-api.service
   ```

2. **Verificar que funciona:**
   ```bash
   curl -X POST https://electroyhogarpelotazo.tienda/salamandra/reason \
     -H "Content-Type: application/json" \
     -d '{"question":"test","context":"test","options":{"a":"1"}}'
   ```

3. **Limpiar servicios rotos:**
   ```bash
   ssh root@147.93.95.67 "systemctl disable opositor-api.service"
   ```

### A Medio Plazo

1. **Instalar Ollama (opcional):**
   - Solo si se quiere usar la gestión de modelos de Ollama
   - Actualmente llama.cpp funciona bien

2. **Monitoreo:**
   - Configurar alertas de memoria (actualmente 6GB/8GB usados)
   - Logs centralizados

3. **Backup del modelo:**
   - El modelo de 4.6GB solo está en el VPS
   - Hacer backup a local o cloud

---

## 📊 RESUMEN DE RECURSOS

| Componente | RAM Usada | CPU | Disco |
|------------|-----------|-----|-------|
| **Sistema Base** | ~500 MB | - | - |
| **Llama.cpp + Modelo** | ~5.7 GB | Variable | 4.6 GB |
| **Salamandra FastAPI** | ~37 MB | Mínimo | ~100 MB |
| **Nginx** | ~50 MB | Mínimo | ~50 MB |
| **Swap usado** | 268 MB | - | 2 GB |
| **TOTAL** | **6.0 GB / 7.8 GB** | - | **26 GB / 96 GB** |

**Margen disponible:**
- RAM: 1.7 GB libres (22%)
- Disco: 71 GB libres (73%)

---

**Última actualización:** 22/01/2026 16:25 CET  
**Auditoría realizada por:** Antigravity AI  
**Estado general:** ✅ Operativo con correcciones menores necesarias
