# Guía de Configuración de Servicios - OpositaIA

## 📦 Servicios Necesarios

### 1. **Docker** (Qdrant + PostgreSQL)

#### Instalación de Docker:
- **Windows**: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux**: `sudo apt install docker.io docker-compose`

#### Iniciar Servicios:
```bash
# Desde la raíz del proyecto
docker-compose up -d

# Verificar estado
docker ps
```

Deberías ver:
- `opositaia-qdrant` (puerto 6333) - Vector Database
- `opositaia-postgres` (puerto 5432) - Base de datos relacional

#### Comandos Útiles:
```bash
# Ver logs
docker logs opositaia-qdrant
docker logs opositaia-postgres

# Reiniciar servicios
docker restart opositaia-qdrant
docker restart opositaia-postgres

# Detener servicios
docker-compose down

# Eliminar todo (¡cuidado! borra datos)
docker-compose down -v
```

---

### 2. **Qdrant** (Vector Database)

**Estado Actual**: Usando **Qdrant Cloud** (configurado en `backend/.env.backend`)

```env
QDRANT_URL=https://b554ceb5-2169-4064-9ce7-83c8cd44cf84.europe-west3-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=eyJhbGci...
```

#### Opción Local (Backup):
Si quieres usar Qdrant local en Docker:

1. Comenta la URL de Qdrant Cloud en `.env.backend`
2. Descomenta la URL local:
```env
# QDRANT_URL=https://... (comentar)
QDRANT_URL=http://localhost:6333
```

3. Asegúrate de que el container está corriendo:
```bash
docker ps | grep qdrant
```

---

### 3. **PostgreSQL** (Base de Datos)

**Configuración Actual** (en `backend/.env.backend`):
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=opositaia
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/opositaia
```

#### Acceder a PostgreSQL:
```bash
# Conectar con psql
docker exec -it opositaia-postgres psql -U postgres -d opositaia

# Ver tablas
\dt

# Salir
\q
```

---

### 4. **WSL + Ollama** (Opcional - LLM Local)

**Estado**: Ollama instalado en WSL (puerto 11434)

#### Verificar Ollama:
```bash
# En WSL
ollama list

# Verificar servicio
curl http://localhost:11434/api/tags
```

#### Modelos Disponibles:
- `mistral` - Modelo local para generación de Q&A

#### Usar Ollama desde Backend:
El backend ya está configurado para usar Ollama:
```env
OLLAMA_URL=http://localhost:11434
```

---

## 🔧 Configuración Completa

### **Paso 1: Iniciar Docker**
```bash
docker-compose up -d
```

### **Paso 2: Verificar Servicios**
```bash
# Qdrant
curl http://localhost:6333/collections

# PostgreSQL
docker exec -it opositaia-postgres pg_isready

# Ollama (si está en WSL)
curl http://localhost:11434/api/tags
```

### **Paso 3: Configurar Backend**
```bash
cd backend
cp .env.backend.example .env.backend
# Edita .env.backend con tus API keys
```

### **Paso 4: Configurar Frontend**
```bash
cd frontend
cp .env.example .env
# Edita .env con tu API key de Google Gemini
```

---

## 🚨 Solución de Problemas

### **Qdrant "unhealthy"**
```bash
docker restart opositaia-qdrant
docker logs opositaia-qdrant --tail 50
```

### **PostgreSQL no arranca**
```bash
docker logs opositaia-postgres
# Si hay error de permisos en volumen:
docker-compose down -v
docker-compose up -d
```

### **Ollama no responde (WSL)**
```bash
# En WSL
sudo systemctl restart ollama
# O reiniciar el servicio manualmente
ollama serve
```

### **Puerto ocupado**
```bash
# Ver qué proceso usa el puerto
# Windows:
netstat -ano | findstr :6333
netstat -ano | findstr :5432

# Linux/WSL:
sudo lsof -i :6333
sudo lsof -i :5432
```

---

## 📊 Resumen de Puertos

| Servicio | Puerto | Protocolo | Ubicación |
|----------|--------|-----------|-----------|
| Frontend (Vite) | 3000 | HTTP | `frontend/` |
| Backend (FastAPI) | 8000 | HTTP | `backend/` |
| Qdrant | 6333 | HTTP | Docker |
| PostgreSQL | 5432 | TCP | Docker |
| Ollama | 11434 | HTTP | WSL |

---

## 🔐 Variables de Entorno Críticas

### **Backend** (`backend/.env.backend`):
```env
# APIs Externas
GROQ_API_KEY=...
DEEPSEEK_API_KEY=...
GEMINI_API_KEY=...
CLAUDE_API_KEY=...

# Qdrant (Cloud o Local)
QDRANT_URL=https://...
QDRANT_API_KEY=...

# PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/opositaia
```

### **Frontend** (`frontend/.env`):
```env
# Google Gemini
VITE_API_KEY=...

# Backend URL
VITE_VPS_API_URL=http://localhost:8000
```

---

## ✅ Checklist de Verificación

- [ ] Docker Desktop instalado y corriendo
- [ ] `docker-compose up -d` ejecutado sin errores
- [ ] Qdrant accesible en `http://localhost:6333`
- [ ] PostgreSQL accesible en `localhost:5432`
- [ ] Backend `.env.backend` configurado con API keys
- [ ] Frontend `.env` configurado con `VITE_API_KEY`
- [ ] Backend corriendo en `http://localhost:8000`
- [ ] Frontend corriendo en `http://localhost:3000`
