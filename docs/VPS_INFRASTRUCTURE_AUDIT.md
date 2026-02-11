# Auditoría de Infraestructura VPS - Hostinger

## 📊 Estado Actual del VPS (147.93.95.67)

### ✅ Servicios Activos

#### 1. Opositor Agent API (FastAPI)
- **Estado**: ✅ Activo y corriendo
- **Puerto**: 8001 (interno)
- **Ubicación**: `/home/ubuntu/opositor_agent/`
- **Servicio**: `opositor-api.service`
- **Workers**: 2
- **Memoria**: 831.9 MB
- **Uptime**: 3 semanas

**Endpoints Disponibles**:
- `GET /health` - Health check
- `POST /rag/index` - Indexar documentos
- Swagger UI: `http://127.0.0.1:8001/docs`

#### 2. Configuración Actual

**Modelos configurados** (`.env`):
```bash
LLM_MODEL=ollama:mistral
EMBEDDING_MODEL=ollama:nomic-embed-text
FALLBACK_MODEL=ollama:phi3:mini
OLLAMA_BASE_URL=http://localhost:11434
```

**Estructura**:
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
├── .env                   # Configuration
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── working_ollama_provider.py
```

### ⚠️ Servicios NO Activos

#### 1. Ollama
- **Estado**: ❌ No instalado/corriendo
- **Esperado**: `http://localhost:11434`
- **Problema**: La API está configurada para usar Ollama pero no está disponible

#### 2. Salamandra 7B Instruct (Q4_K_M) - **NUEVO**
- **Estado**: ✅ Listo para subir
- **Ubicación Local**: `/home/spas/OPOS_GEMINI_1/model_gguf/salamandra-7b-instruct-unsloth.Q4_K_M.gguf`
- **Ubicación Destino**: `/root/models/` o `/usr/share/ollama/.ollama/models/`
- **Tamaño**: 4.6 GB (Perfecto para 8GB RAM)
- **Ventaja**: Modelo especializado en Oposiciones Española.

## 🎯 Opciones de Integración

### Opción 1: Usar la API Existente (Recomendado)

**Ventajas**:
- ✅ Ya está funcionando
- ✅ Ya tiene RAG implementado
- ✅ Ya tiene endpoints
- ✅ Fácil de integrar

**Integración**:
```typescript
// frontend/services/vpsService.ts
const VPS_API_URL = 'http://147.93.95.67:8001';

export async function ragSearch(query: string) {
  const response = await fetch(`${VPS_API_URL}/rag/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  return response.json();
}
```

**Acción requerida**:
1. Exponer puerto 8001 externamente (o usar proxy)
2. Configurar CORS en la API
3. Documentar endpoints disponibles
4.estos creoque ya estan aplicadas , comprobarlo YA !!! 



### Opción 3: Arquitectura Híbrida (Recomendado)

```
```

# 📋 Plan de Acción Inmediato

### Fase 1: Conectar con API Existente (1 día)

1. **Exponer API del VPS**:
```bash
# Opción A: Nginx reverse proxy
sudo apt install nginx
sudo nano /etc/nginx/sites-available/opositor-api

# Configuración:
server {
    listen 80;
    server_name 147.93.95.67;
    
    location /api/ {
        proxy_pass http://127.0.0.1:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

sudo ln -s /etc/nginx/sites-available/opositor-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

2. **Configurar CORS**:
```python
# /home/ubuntu/opositor_agent/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. **Documentar endpoints**:
```bash
ssh root@147.93.95.67
curl http://127.0.0.1:8001/openapi.json > vps-api-spec.json
```

### Fase 2: Instalar Ollama (Opcional, 1 día)

```bash
# SSH al VPS
ssh root@147.93.95.67

# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Descargar modelos
ollama pull mistral
ollama pull nomic-embed-text

# Verificar
ollama list
systemctl status ollama
```

### Fase 3: Integrar con Frontend (2 días)

1. Crear servicio VPS en frontend
2. Actualizar componentes para usar VPS API
3. Fallback a Gemini si VPS falla
4. Testing

## 💰 Costos

### Actual:
- VPS Hostinger: Ya pagado
- API corriendo: $0/mes adicional
- **Total: $0/mes** ✅

### Si instalamos Ollama:
- Espacio: ~10 GB (verificar disponible)
- RAM: ~4-8 GB (verificar disponible)
- **Total: $0/mes** ✅

## 🔐 Seguridad

### Recomendaciones:

1. **Firewall**:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

2. **SSL/TLS**:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

3. **API Key**:
```python
# Añadir autenticación a la API
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/protected")
async def protected_route(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403)
    return {"status": "ok"}
```

## 📊 Recursos del VPS

### Verificar disponibles:
```bash
# Espacio en disco
df -h

# RAM
free -h

# CPU
lscpu

# Procesos
top
```

## ✅ Decisión Recomendada

### Para MVP (Ahora):

1. **Usar API existente del VPS** (ya funciona)
2. **Ollama local en WSL** (para desarrollo)
3. **Gemini API** (para producción)
4. **Qdrant local en WSL** (para desarrollo)

**Ventajas**:
- ✅ Funciona inmediatamente
- ✅ $0/mes
- ✅ Sin instalaciones complejas
- ✅ Fácil de debuggear

### Para Producción (Después):

1. Instalar Ollama en VPS
2. Migrar Qdrant a VPS
3. Configurar SSL/TLS
4. Monitoreo y logs

---

**Última actualización**: 2025-01-16  
**Estado**: ✅ API funcionando, Ollama pendiente  
**Costo actual**: $0/mes
