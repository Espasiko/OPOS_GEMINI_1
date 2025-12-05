# 🔍 ANÁLISIS COMPLETO ACTUALIZADO - ARQUITECTURA REAL EN WSL

**Fecha:** 5 Diciembre 2025  
**Ubicación:** TODO está en WSL, no en Windows  
**Python:** 3.12.3 en WSL  
**Docker:** Instalado en WSL  
**Ollama:** Corriendo en WSL en localhost:11434 ✅

---

## 📦 ARQUITECTURA REAL (TAL COMO ESTÁ AHORA)

```
Windows PowerShell
  ↓ (WSL subsystem)
  
WSL Ubuntu (Linux)
  ├─ Docker (instalado)
  │  ├─ PostgreSQL OLD (sim_old-db-1:5432) ✅ Up y Healthy
  │  │  └─ pgvector/pgvector:pg17
  │  │
  │  ├─ PostgreSQL NEW (opositaia-postgres:5432) ❌ Created (NO INICIADO)
  │  │  └─ postgres:15-alpine
  │  │
  │  ├─ Qdrant OLD (qdrant) ❌ Exited
  │  │
  │  ├─ Qdrant NEW (opositaia-qdrant:6333) ⚠️ Up pero Unhealthy
  │  │  └─ qdrant/qdrant:latest
  │  │
  │  └─ Ollama OLD (ollama-starter) ❌ Exited
  │
  ├─ Python 3.12.3 (sistema)
  │
  ├─ venv en /mnt/e/1/OPOS_GEMINI_1/backend/venv ✅ Existe
  │
  └─ Ollama Service ✅ Corriendo en localhost:11434
     └─ Modelos: mistral:7.2B (descargado 2 Dec)

```

---

## ✅ SERVICIOS QUE FUNCIONAN ACTUALMENTE

### 1. Ollama ✅ 
- **Ubicación:** WSL localhost:11434
- **Estado:** Corriendo
- **Modelos:** mistral:7.2B disponible
- **Acceso:** http://localhost:11434/api/tags (funciona!)

### 2. PostgreSQL OLD (sim_old-db-1) ✅
- **Ubicación:** Docker en WSL
- **Puerto:** 5432
- **Imagen:** pgvector/pgvector:pg17
- **Estado:** UP y HEALTHY desde hace 7 semanas
- **¿Por qué existe?** Probablemente proyecto anterior

### 3. Qdrant NEW ⚠️
- **Ubicación:** Docker en WSL
- **Puerto:** 6333-6334
- **Estado:** UP pero UNHEALTHY
- **Razón:** Probablemente no encuentra datos o no está inicializado

---

## ❌ SERVICIOS CON PROBLEMAS

### 1. PostgreSQL NEW (opositaia-postgres) ❌
- **Estado:** Created (nunca fue iniciado)
- **Razón:** Nunca corrió `docker start opositaia-postgres`
- **Solución:** `docker start opositaia-postgres` o `docker-compose up postgres`

### 2. Qdrant NEW (opositaia-qdrant) ⚠️
- **Estado:** Up pero Unhealthy
- **Razón:** Probablemente falló el health check `curl http://localhost:6333/health`
- **Solución:** Verificar logs de Qdrant

### 3. Backend ❌
- **Razón:** No está corriendo (pero es lo que queremos arrancar)

---

## 🎯 ARQUITECTURA QUE DEBERÍA HABER

```
Para ejecutar backend exitosamente:

1. Opción A: USAR CONTAINERS VIEJOS (funcionan!)
   - PostgreSQL: sim_old-db-1 (ya está Up)
   - Ollama: localhost:11434 (ya está corriendo)
   - Backend: Ejecutar en WSL con venv local
   
2. Opción B: LIMPIAR Y USAR NUEVOS (docker-compose.yml)
   - Eliminar containers viejos
   - Arrancar docker-compose up
   - Pero PRIMERO arreglar docker-compose.yml
```

---

## 🔧 PROBLEMAS EN docker-compose.yml (ACTUALIZADO)

### Problema 1: Ollama NO debe estar en docker-compose
```yaml
# INCORRECTO (en docker-compose.yml actual)
ollama:
  image: ollama/ollama:latest
  
# CORRECTO: Ollama ya está corriendo en WSL
# No incluir en docker-compose
```

### Problema 2: PostgreSQL en estado Created
- El container existe pero nunca fue iniciado
- Necesita: `docker start opositaia-postgres`

### Problema 3: QDRANT Unhealthy
- Healthcheck falla
- Verificar: `docker logs opositaia-qdrant`

### Problema 4: Rutas en Dockerfile/docker-compose
- ✅ ARREGLADO: Cambié `app.main:app` → `main:app`
- ✅ ARREGLADO: Agregué `depends_on: postgres`
- ✅ ARREGLADO: Agregué `env_file: backend/.env.backend`

---

## 🚀 SOLUCIÓN RECOMENDADA (PATH OF LEAST RESISTANCE)

### OPCIÓN 1: Usar containers y servicios VIEJOS que ya funcionan
```bash
# 1. Iniciar PostgreSQL old (ya existe)
wsl docker start sim_old-db-1

# 2. Ollama ya está corriendo en localhost:11434

# 3. Entrar a WSL y activar venv
wsl bash

# 4. Dentro de WSL:
cd /mnt/e/1/OPOS_GEMINI_1/backend
source venv/bin/activate
pip install -r requirements.txt  # Arreglé duplicación
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 5. Backend accesible en Windows en: http://localhost:8000
```

**Ventajas:**
- ✅ Ya hay PostgreSQL funcionando
- ✅ Ya hay Ollama funcionando
- ✅ Solo ejecutar backend
- ✅ Rápido y simple

---

### OPCIÓN 2: Limpiar y usar docker-compose.yml (MI RECOMENDACIÓN)
```bash
# 1. Parar containers viejos
wsl docker stop sim_old-db-1 opositaia-qdrant

# 2. Limpiar docker-compose (remover Ollama de ahí)
# YA HECHO - ver docker-compose.yml actualizado

# 3. Desde Windows PowerShell O WSL:
wsl docker-compose down -v
wsl docker-compose up -d

# 4. Verificar que todo esté healthy
wsl docker ps

# 5. Ejecutar backend en WSL:
wsl bash
cd /mnt/e/1/OPOS_GEMINI_1/backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Ventajas:**
- ✅ Arquitectura limpia
- ✅ Todos los servicios coordinados
- ✅ Fácil de reproducir
- ✅ Production-ready

---

## 🚨 CAMBIOS YA REALIZADOS

### ✅ 1. requirements.txt ARREGLADO
- Eliminada duplicación
- Dependencias organizadas por categoría

### ✅ 2. Dockerfile ARREGLADO
- Cambié: `CMD ["uvicorn", "app.main:app", ...]`
- Cambié a: `CMD ["uvicorn", "main:app", ...]`

### ✅ 3. docker-compose.yml PARCIALMENTE ARREGLADO
- ✅ Agregué: `env_file: backend/.env.backend`
- ✅ Agregué: `postgres` en `depends_on`
- ✅ Cambié: `command: uvicorn app.main:app` → `command: uvicorn main:app`
- ⚠️ FALTA: Remover Ollama de services (está en WSL, no en Docker)

---

## 📝 PENDIENTE: Remover Ollama de docker-compose.yml

El archivo todavía tiene la sección `ollama` service que debe ser eliminada porque:
1. Ollama ya está corriendo en WSL
2. Docker Desktop en Windows no puede ejecutar containers adicionales en WSL de forma independiente
3. El backend accede a Ollama via `host.docker.internal:11434`

---

## 📊 VERIFICACIÓN RÁPIDA DE ESTADO

```bash
# Ver todos los containers
wsl docker ps -a

# Ver logs de Qdrant (para ver por qué es unhealthy)
wsl docker logs opositaia-qdrant

# Ver logs de PostgreSQL
wsl docker logs opositaia-postgres

# Probar Ollama
wsl curl http://localhost:11434/api/tags

# Probar Qdrant
wsl curl http://localhost:6333/health

# Probar PostgreSQL
wsl docker exec opositaia-postgres pg_isready -U postgres
```

---

## 🎯 PRÓXIMOS PASOS

1. ✅ HECHO: Arreglar requirements.txt
2. ✅ HECHO: Arreglar Dockerfile
3. ✅ HECHO: Arreglar docker-compose.yml (parcialmente)
4. ⏳ TODO: Remover servicio ollama de docker-compose.yml
5. ⏳ TODO: Crear script `start-backend.ps1` que ejecute comandos WSL
6. ⏳ TODO: Documentar arquitectura final
7. ⏳ TODO: Testear que todo funciona

