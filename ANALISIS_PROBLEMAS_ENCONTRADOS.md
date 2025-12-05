# 🔍 ANÁLISIS COMPLETO DE PROBLEMAS ENCONTRADOS

**Fecha:** 5 Diciembre 2025  
**Proyecto:** OpositaIA (2 meses de evolución, no 3 años)  
**Estado:** 15 intentos fallidos de iniciar backend

---

## 📊 RESUMEN EJECUTIVO

El proyecto **estaba funcionando hace poco** pero fue roto por cambios recientes en:
1. **docker-compose.yml** - comando con ruta incorrecta
2. **Dockerfile** - ruta incorrecta al módulo
3. **requirements.txt** - dependencias duplicadas
4. **falta sincronización** entre configuración Docker y código Python

**Resultado:** Los 15 intentos fallaron porque no hay coordinación entre:
- El volumen Docker (`./backend:/app`)
- La ruta del comando (`uvicorn app.main:app` vs `uvicorn main:app`)
- El WORKDIR del Dockerfile

---

## 🔴 PROBLEMA 1: COMANDO EN docker-compose.yml INCORRECTO

### Ubicación
`docker-compose.yml` línea 111:
```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### El Problema
- El volumen monta: `./backend:/app`
- Dentro del container, los archivos están en `/app/`
- Pero el comando busca: `app.main:app`
- Resultado: **Busca `/app/app/main.py` (NO EXISTE)**

### Lo Correcto
```yaml
command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🔴 PROBLEMA 2: DOCKERFILE CON RUTA INCORRECTA

### Ubicación
`backend/Dockerfile` línea 21:
```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### El Problema
- El WORKDIR es `/app`
- El archivo principal se llama `main.py`
- No hay carpeta `app/` dentro de `/app/`
- Resultado: **Falla al buscar el módulo `app.main`**

### Lo Correcto
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔴 PROBLEMA 3: requirements.txt CON DUPLICACIÓN

### Ubicación
`backend/requirements.txt` líneas 1-24 y 31-39

### El Problema
```plaintext
# Líneas 1-24: Dependencias normales
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.0
...

# Líneas 31-39: DUPLICADAS (error de merge/copy)
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.0
pydantic-settings==2.6.0
...
```

### Impacto
- ⚠️ Puede causar conflictos de versiones
- ⚠️ Instala dependencias dos veces (desperdicia tiempo)
- ⚠️ Potencial de inconsistencias

---

## 🔴 PROBLEMA 4: docker-compose.yml ESPERA HEALTHCHECKS INCOMPLETOS

### Ubicación
`docker-compose.yml` líneas 86-87:

```yaml
depends_on:
  qdrant:
    condition: service_healthy
  ollama:
    condition: service_healthy  # ← Aquí asume que Ollama está en Docker
```

### El Problema
- **Ollama está en WSL**, NO en Docker
- Docker espera que `ollama` container sea healthy
- Pero ollama NO está siendo levantado por docker-compose
- Resultado: **Backend nunca inicia porque espera a Ollama que no existe**

### Estado Real
- ✅ Qdrant: local en Docker (correcto)
- ✅ PostgreSQL: en Docker (correcto)
- ❌ Ollama: en WSL (no en Docker)
- ✅ Backend: debería estar en Docker

---

## 🟡 PROBLEMA 5: VARIABLES DE ENTORNO CON INCONSISTENCIA

### Ubicación
`docker-compose.yml` líneas 72:

```yaml
environment:
  - GEMINI_API_KEY=${GEMINI_API_KEY}  # ← Viene de DÓNDE?
```

### El Problema
- `${GEMINI_API_KEY}` busca en **variables del host** (Windows PowerShell)
- Pero está definido en `backend/.env.backend`
- Docker NO lee archivos `.env` de forma automática
- Resultado: **GEMINI_API_KEY es NULL dentro del container**

### Lo Correcto
Opciones:
1. Usar `env_file`:
```yaml
backend:
  env_file:
    - backend/.env.backend
```

2. O pasar explícitamente variables críticas

---

## 🟡 PROBLEMA 6: FALTA POSTGRES EN depends_on DEL BACKEND

### Ubicación
`docker-compose.yml` líneas 86-87:

```yaml
depends_on:
  qdrant:
    condition: service_healthy
  ollama:
    condition: service_healthy
  # ❌ FALTA: postgres
```

### El Problema
- El backend necesita PostgreSQL
- Pero NO espera a que PostgreSQL sea healthy
- Resultado: **Backend intenta conectar a DB que aún no está lista**

### Lo Correcto
```yaml
depends_on:
  qdrant:
    condition: service_healthy
  postgres:
    condition: service_healthy
  ollama:
    condition: service_healthy
```

---

## 🟡 PROBLEMA 7: BACKEND NO INICIALIZA DATABASE AUTOMÁTICAMENTE

### Ubicación
`backend/main.py` líneas 50-56:

```python
# Initialize DB
try:
    db.initialize()
    logger.info("✅ Database connection initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize database: {e}")
```

### El Problema
- `db.initialize()` **no crea tablas**
- Necesita `backend/database/init_db.py` ejecutado primero
- Resultado: **Queries fallan porque no hay tablas**

### Lo Correcto
Crear un script de inicialización en el Dockerfile:

```dockerfile
RUN python database/init_db.py || echo "DB already initialized"
```

---

## 🟡 PROBLEMA 8: OLLAMA NO ESTÁ EN docker-compose (está en WSL)

### Estado Real
```
Windows PowerShell
  ↓
WSL (Ubuntu)
  ├─ Ollama (puerto 11434)
  ├─ PostgreSQL (docker dentro de WSL)
  └─ Qdrant (local en Windows)
```

### El Problema
- docker-compose.yml define `ollama` service en Docker
- Pero Ollama realmente está corriendo en WSL
- Backend intenta conectar a `http://ollama:11434` (nombre interno de Docker)
- Pero debería conectar a `http://localhost:11434` o IP de WSL

### Lo Correcto
En `backend/.env.backend`:
```env
OLLAMA_URL=http://localhost:11434  # No http://ollama:11434
```

---

## 🟡 PROBLEMA 9: script start-backend.sh ES MUY SIMPLE

### Archivo
`scripts/maintenance/start-backend.sh`:

```bash
#!/bin/bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### El Problema
- ✅ Script es correcto para ejecución local
- ✅ Activa venv correctamente
- ✅ Usa la ruta correcta `main:app`
- ❌ Pero NO existe `venv` en PATH de Windows
- ❌ Necesita convertirse a `.ps1` (PowerShell) o ejecutarse en WSL

---

## 🟡 PROBLEMA 10: POSTGRES EN DOCKER vs WSL CONFUSIÓN

### Problema de Arquitectura
```
¿Dónde está PostgreSQL?
  ├─ docker-compose.yml lo define como servicio
  ├─ Pero .env.backend usa localhost:5432
  └─ ¿Funciona porque docker-compose lo expone en 5432? ✓ SÍ
```

### Pero el Problema es
- backend intenta conectar a `localhost:5432`
- Docker container no tiene acceso a `localhost` (está aislado)
- Debería usar `postgres:5432` (nombre del servicio)

---

## 📋 RESUMEN DE LOS 15 INTENTOS FALLIDOS

```
1-5:   Docker/Qdrant checks (repetidos)
       ❌ Problema: No hay Docker CLI en Windows PowerShell

6-9:   PowerShell activation sin WSL
       ❌ Problema: venv no existe en PATH, requirements.txt corrupto

10-15: WSL + backend
       ❌ Problema: docker-compose con rutas incorrectas + Ollama no coordinado
```

---

## ✅ SOLUCIONES NECESARIAS (Por Prioridad)

### CRÍTICAS (Impide iniciar backend):
1. ✅ Arreglar `requirements.txt` (eliminar duplicación)
2. ✅ Arreglar `docker-compose.yml` comando (ruta correcta)
3. ✅ Arreglar `Dockerfile` comando (ruta correcta)
4. ✅ Agregar `postgres` a `depends_on` del backend
5. ✅ Agregar `/health` endpoint (ya existe ✓)

### IMPORTANTES (Previene errores en runtime):
6. ✅ Usar `env_file` en docker-compose para cargar `.env.backend`
7. ✅ Quitar Ollama de docker-compose.yml (está en WSL)
8. ✅ Configurar `OLLAMA_URL` correctamente
9. ✅ Agregar script de inicialización de DB
10. ✅ Crear `start-backend.ps1` para Windows

### MEJORAS (Optimización):
11. ✅ Agregar logging más detallado
12. ✅ Crear script maestro que valide todo

---

## 🎯 ARQUITECTURA REAL (CORRECTA)

```
Windows PowerShell
  ├─ Frontend (Vite) en localhost:5173
  ├─ Docker Desktop
  │  ├─ Qdrant (puerto 6333)
  │  ├─ PostgreSQL (puerto 5432)
  │  └─ Backend (puerto 8000) - NUEVA
  └─ WSL (Ubuntu)
     └─ Ollama (puerto 11434)

Comunicación:
  Frontend → Backend (localhost:8000)
  Backend → Qdrant (http://qdrant:6333 desde Docker)
  Backend → PostgreSQL (postgres:5432 desde Docker)
  Backend → Ollama (http://localhost:11434 desde Docker)
```

---

## 📝 ARCHIVOS A REPARAR

1. ✅ `backend/requirements.txt` - Eliminar duplicación
2. ✅ `docker-compose.yml` - Corregir comando y config
3. ✅ `backend/Dockerfile` - Corregir comando
4. ✅ `backend/.env.backend` - Verificar (ya está bien)
5. ✅ Crear `start-backend.ps1` - Script Windows
6. ✅ Crear `SETUP_REPARACION.md` - Guía

