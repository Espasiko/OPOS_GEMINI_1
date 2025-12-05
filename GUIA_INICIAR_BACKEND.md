# 🚀 GUÍA DEFINITIVA - INICIAR BACKEND EN OPOSITAIA

**Última actualización:** 5 Diciembre 2025  
**Proyecto:** OpositaIA (2 meses de desarrollo)  
**Arquitectura:** Windows PowerShell + WSL (Docker + Python)  

---

## 📋 ESTADO ACTUAL DEL PROYECTO

### ✅ SERVICIOS QUE FUNCIONAN

| Servicio | Ubicación | Puerto | Estado | Nota |
|----------|-----------|--------|--------|------|
| **Ollama** | WSL localhost | 11434 | ✅ Corriendo | mistral:7.2B descargado |
| **PostgreSQL** | WSL Docker | 5432 | ✅ UP (sim_old-db-1) | pgvector/pg17 (7 semanas corriendo) |
| **Qdrant** | WSL Docker | 6333 | ⚠️ UP (unhealthy) | Necesita verificación |
| **Backend** | - | 8000 | ❌ NO CORRIENDO | Listo para iniciar |

### ✅ ARCHIVOS REPARADOS

1. ✅ `backend/requirements.txt` - Eliminada duplicación (59 → 45 líneas)
2. ✅ `backend/Dockerfile` - Comando corregido (`app.main:app` → `main:app`)
3. ✅ `docker-compose.yml` - Múltiples ajustes:
   - Removido servicio Ollama (está en WSL)
   - Agregado `depends_on: postgres`
   - Agregado `env_file: backend/.env.backend`
   - Comando corregido
4. ✅ `start-backend.ps1` - Nuevo script para PowerShell

---

## 🎯 CÓMO INICIAR EL BACKEND

### OPCIÓN 1: Script automático (RECOMENDADO)

```powershell
# Desde la carpeta raíz del proyecto en PowerShell

# Modo local (usa servicios existentes)
.\start-backend.ps1

# Modo docker-compose (limpio y coordinado)
.\start-backend.ps1 -Compose

# Modo docker-compose con limpieza total
.\start-backend.ps1 -Compose -Clean
```

---

### OPCIÓN 2: Manual paso a paso (si el script no funciona)

```powershell
# 1. Entrar a WSL
wsl bash

# 2. Dentro de WSL:
cd /mnt/e/1/OPOS_GEMINI_1/backend

# 3. Activar virtual environment
source venv/bin/activate

# 4. (Opcional) Actualizar dependencias
pip install --upgrade -r requirements.txt

# 5. Iniciar FastAPI
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

### OPCIÓN 3: Con docker-compose (servicio completo)

```powershell
# Desde raíz del proyecto

# 1. Iniciar todos los servicios
wsl docker-compose up -d

# 2. Verificar estado
wsl docker ps

# 3. Ver logs del backend
wsl docker logs -f opositaia-backend

# 4. Para detener
wsl docker-compose down
```

---

## ✅ VERIFICACIÓN RÁPIDA

Después de iniciar el backend, verifica que todo funciona:

```powershell
# 1. Backend respondiendo
Invoke-WebRequest -Uri "http://localhost:8000/health" | Select-Object -ExpandProperty Content

# 2. Qdrant disponible
wsl curl http://localhost:6333/health

# 3. PostgreSQL disponible
wsl docker ps | Select-String "postgres"

# 4. Ollama disponible
wsl curl http://localhost:11434/api/tags
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Problema: "WSL not found"
```powershell
# Instalar WSL
wsl --install

# Actualizar a WSL 2
wsl --set-default-version 2
```

### Problema: "Docker not found in WSL"
```bash
# En WSL, instalar Docker
sudo apt-get update
sudo apt-get install docker.io

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

### Problema: PostgreSQL no inicia
```bash
# En WSL:
docker start sim_old-db-1
# O
docker-compose up -d postgres
```

### Problema: Qdrant unhealthy
```bash
# Ver logs
docker logs opositaia-qdrant

# Reiniciar
docker restart opositaia-qdrant
```

### Problema: Ollama no responde
```bash
# En WSL, verificar si está corriendo
ps aux | grep ollama

# Iniciar Ollama (si WSL tiene systemd)
systemctl start ollama
# O
ollama serve &
```

### Problema: Backend error "GEMINI_API_KEY not found"
```bash
# Verificar que .env.backend existe
ls -la /mnt/e/1/OPOS_GEMINI_1/backend/.env.backend

# Verificar que tiene contenido
cat /mnt/e/1/OPOS_GEMINI_1/backend/.env.backend | head -20
```

### Problema: ModuleNotFoundError
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Verificar que venv está activado
which python  # Debe mostrar path del venv
```

---

## 📊 ARQUITECTURA FINAL

```
Windows PowerShell
  │
  ├─ Frontend
  │  ├─ npm run dev (localhost:5173)
  │  └─ Conexión a Backend
  │
  └─ WSL (Ubuntu en Docker)
     ├─ Backend (FastAPI)
     │  ├─ puerto 8000
     │  ├─ venv en /mnt/e/1/OPOS_GEMINI_1/backend/venv
     │  └─ conexiones a:
     │     ├─ PostgreSQL (sim_old-db-1:5432)
     │     ├─ Qdrant (opositaia-qdrant:6333)
     │     └─ Ollama (localhost:11434)
     │
     ├─ PostgreSQL (Docker)
     │  └─ pgvector/pg17:5432 (sim_old-db-1)
     │
     ├─ Qdrant (Docker)
     │  └─ qdrant/qdrant:6333 (opositaia-qdrant)
     │
     └─ Ollama (servicio WSL)
        └─ localhost:11434 (mistral:7.2B)
```

---

## 📝 CAMBIOS REALIZADOS Y RAZONES

| Archivo | Cambio | Razón |
|---------|--------|-------|
| `requirements.txt` | Eliminar duplicación | Evitar conflictos de versiones |
| `Dockerfile` | `app.main:app` → `main:app` | main.py está en /app directamente |
| `docker-compose.yml` | Remover Ollama | Ollama corre en WSL, no en Docker |
| `docker-compose.yml` | Agregar `postgres` en depends_on | Backend necesita DB lista |
| `docker-compose.yml` | Agregar `env_file` | Cargar API keys de .env.backend |
| `docker-compose.yml` | Cambiar comando a `uvicorn main:app` | Ruta correcta del módulo |
| (nuevo) | `start-backend.ps1` | Script automático para Windows |

---

## 🔧 CONFIGURACIÓN PARA PRODUCCIÓN

Cuando estés listo para producción:

```bash
# 1. Cambiar RELOAD a false
API_RELOAD=false

# 2. Usar Gunicorn en lugar de uvicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app

# 3. Configurar HTTPS
# Usar Nginx como proxy inverso

# 4. Agregar monitoreo
# Prometheus está en requirements.txt

# 5. Configurar logs centralizados
# Implementar ELK stack o similar
```

---

## 📚 RECURSOS

- **FastAPI Docs:** http://localhost:8000/docs (cuando Backend esté corriendo)
- **Qdrant Dashboard:** http://localhost:6333/dashboard (si está disponible)
- **Backend .env:** `backend/.env.backend` (todas las API keys aquí)

---

## ✅ CHECKLIST DE INICIO

- [ ] WSL instalado y funcionando
- [ ] Docker en WSL disponible
- [ ] Ollama corriendo en WSL (localhost:11434)
- [ ] PostgreSQL corriendo en Docker (localhost:5432)
- [ ] Qdrant corriendo en Docker (localhost:6333)
- [ ] `backend/.env.backend` existe y tiene API keys
- [ ] `backend/venv` existe y está activado
- [ ] `requirements.txt` instalado (sin duplicación)
- [ ] `backend/main.py` existe y es accesible
- [ ] Backend iniciado: `python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
- [ ] `http://localhost:8000/health` responde correctamente

---

## 🎯 SIGUIENTES PASOS

1. Testear que el backend inicia correctamente
2. Verificar conectividad con todas las bases de datos
3. Probar endpoints del RAG
4. Testear con el frontend
5. Preparar para producción

