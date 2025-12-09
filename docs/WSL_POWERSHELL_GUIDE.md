# 🐧 Guía WSL + PowerShell para OpositAIA

**Fecha:** 5 de diciembre de 2025  
**Entorno:** Windows + WSL (Ubuntu)  

---

## 🎯 Resumen

Este proyecto utiliza **WSL (Windows Subsystem for Linux)** para ejecutar el backend Python/FastAPI debido a:

1. ✅ Python 3.12.3 ya instalado y configurado
2. ✅ Virtualenv con todas las dependencias listas
3. ✅ Mejor compatibilidad con herramientas Linux (uvicorn, bash scripts)
4. ✅ Acceso a archivos Windows desde `/mnt/e/1/OPOS_GEMINI_1`

---

## 📂 Estructura de Rutas

### Desde PowerShell (Windows)

```powershell
E:\1\OPOS_GEMINI_1\backend\main.py
E:\1\OPOS_GEMINI_1\frontend\src\App.tsx
```

### Desde WSL (Ubuntu)

```bash
/mnt/e/1/OPOS_GEMINI_1/backend/main.py
/mnt/e/1/OPOS_GEMINI_1/frontend/src/App.tsx
```

**Regla de conversión:**
```
E:\1\OPOS_GEMINI_1  →  /mnt/e/1/OPOS_GEMINI_1
C:\Users\USER       →  /mnt/c/Users/USER
```

---

## 🚀 Iniciar Backend FastAPI

### ✅ Opción 1: WSL (Recomendado)

```bash
# Abrir WSL
wsl

# Navegar al proyecto
cd /mnt/e/1/OPOS_GEMINI_1/backend

# Activar virtualenv
source venv/bin/activate

# Iniciar FastAPI con hot reload
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Verificar:**
```bash
# Desde WSL
curl http://localhost:8000/health

# Desde PowerShell
curl http://localhost:8000/health
```

### ⚠️ Opción 2: PowerShell (Alternativa)

**Problema:** Python no está en PATH de PowerShell.

**Solución temporal:**
```powershell
# Ejecutar uvicorn desde WSL directamente
wsl bash -c 'cd /mnt/e/1/OPOS_GEMINI_1/backend && source venv/bin/activate && python -m uvicorn main:app --host 0.0.0.0 --port 8000'
```

---

## 🧪 Ejecutar Scripts Python

### Desde WSL

```bash
cd /mnt/e/1/OPOS_GEMINI_1/backend
source venv/bin/activate

# Ejecutar script
python agents/boe_api_client.py

# Ejecutar tests
python test_boe_router.py
```

### Desde PowerShell

```powershell
# Opción 1: Llamar a WSL
wsl bash -c 'cd /mnt/e/1/OPOS_GEMINI_1/backend && source venv/bin/activate && python agents/boe_api_client.py'

# Opción 2: Usar py launcher (si Python está instalado en Windows)
py agents\boe_api_client.py
```

---

## 🔧 Comandos Útiles

### Navegar entre WSL y Windows

```bash
# Desde WSL: abrir explorador Windows en carpeta actual
explorer.exe .

# Desde WSL: abrir VS Code en carpeta actual
code .

# Desde PowerShell: entrar a WSL en carpeta actual
wsl

# Desde PowerShell: ejecutar comando en WSL
wsl ls -la
wsl python3 --version
```

### Gestión de Procesos

```bash
# Desde WSL: verificar si uvicorn está corriendo
lsof -i :8000

# Desde WSL: matar proceso en puerto 8000
kill -9 $(lsof -t -i:8000)

# Desde PowerShell: verificar puerto 8000
netstat -ano | findstr :8000

# Desde PowerShell: matar proceso por PID
taskkill /PID <PID> /F
```

---

## 📦 Gestión del Virtualenv

### Activar/Desactivar

```bash
# Activar (WSL)
source /mnt/e/1/OPOS_GEMINI_1/backend/venv/bin/activate

# Desactivar
deactivate
```

### Instalar Dependencias

```bash
# Desde WSL con venv activado
pip install -r requirements.txt

# Agregar nueva dependencia
pip install nombre-paquete
pip freeze > requirements.txt
```

### Verificar Virtualenv

```bash
# Verificar que estamos en el venv correcto
which python
# Output esperado: /mnt/e/1/OPOS_GEMINI_1/backend/venv/bin/python

# Ver paquetes instalados
pip list
```

---

## 🌐 Acceso a Servicios

| Servicio | Puerto | URL (WSL) | URL (Windows) |
|----------|--------|-----------|---------------|
| **FastAPI Backend** | 8000 | http://localhost:8000 | http://localhost:8000 |
| **React Frontend** | 3000 | http://localhost:3000 | http://localhost:3000 |
| **Qdrant Local** | 6333 | http://localhost:6333 | http://localhost:6333 |
| **Ollama Local** | 11434 | http://localhost:11434 | http://localhost:11434 |

**Nota:** Los puertos se comparten entre WSL y Windows gracias a WSL2.

---

## 🐞 Solución de Problemas

### Problema 1: "python: command not found" en PowerShell

**Causa:** Python solo está instalado en WSL, no en Windows.

**Solución:**
```powershell
# Usar WSL para ejecutar Python
wsl python3 script.py

# O instalar Python en Windows desde:
# https://www.python.org/downloads/
```

### Problema 2: "ModuleNotFoundError" en WSL

**Causa:** Virtualenv no activado o dependencias faltantes.

**Solución:**
```bash
cd /mnt/e/1/OPOS_GEMINI_1/backend
source venv/bin/activate
pip install -r requirements.txt
```

### Problema 3: Permisos denegados en archivos

**Causa:** Diferencias de permisos entre Windows y WSL.

**Solución:**
```bash
# Dar permisos de ejecución
chmod +x script.sh

# Cambiar owner (si necesario)
sudo chown $USER:$USER archivo
```

### Problema 4: Uvicorn no inicia

**Soluciones:**

1. Verificar puerto no ocupado:
```bash
lsof -i :8000
```

2. Verificar virtualenv activo:
```bash
which python
# Debe ser: /mnt/e/.../venv/bin/python
```

3. Verificar dependencias:
```bash
pip install fastapi uvicorn httpx
```

4. Ver logs completos:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug
```

### Problema 5: "cannot find module 'fastapi'"

**Causa:** Ejecutando Python fuera del virtualenv.

**Solución:**
```bash
# Asegurar venv activado
source venv/bin/activate

# Verificar instalación
pip show fastapi
```

---

## 📝 Scripts de Atajo

### Crear alias en WSL

Agregar al `~/.bashrc`:

```bash
# Aliases OpositAIA
alias opos='cd /mnt/e/1/OPOS_GEMINI_1'
alias oback='cd /mnt/e/1/OPOS_GEMINI_1/backend && source venv/bin/activate'
alias ofront='cd /mnt/e/1/OPOS_GEMINI_1/frontend'

# Iniciar servicios
alias start-backend='cd /mnt/e/1/OPOS_GEMINI_1/backend && source venv/bin/activate && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload'
alias start-frontend='cd /mnt/e/1/OPOS_GEMINI_1/frontend && npm run dev'

# Tests
alias test-boe='cd /mnt/e/1/OPOS_GEMINI_1/backend && source venv/bin/activate && python test_boe_router.py'
```

**Recargar bashrc:**
```bash
source ~/.bashrc
```

**Usar:**
```bash
oback  # Ir a backend y activar venv
start-backend  # Iniciar FastAPI
```

### Crear scripts PowerShell

Crear `scripts/start-backend.ps1`:

```powershell
wsl bash -c 'cd /mnt/e/1/OPOS_GEMINI_1/backend && source venv/bin/activate && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload'
```

**Ejecutar:**
```powershell
.\scripts\start-backend.ps1
```

---

## 🎓 Buenas Prácticas

### 1. Siempre activar virtualenv

```bash
# ❌ MAL
python script.py

# ✅ BIEN
source venv/bin/activate
python script.py
```

### 2. Usar rutas absolutas en scripts

```python
# ❌ MAL (relativas)
open("data/archivo.txt")

# ✅ BIEN (absolutas)
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent
open(BASE_DIR / "data" / "archivo.txt")
```

### 3. Verificar PATH antes de ejecutar

```bash
# Verificar Python correcto
which python
# Esperado: /mnt/e/1/OPOS_GEMINI_1/backend/venv/bin/python

# Verificar pip correcto
which pip
# Esperado: /mnt/e/1/OPOS_GEMINI_1/backend/venv/bin/pip
```

### 4. Logs descriptivos

```bash
# ❌ MAL
python script.py

# ✅ BIEN
python script.py 2>&1 | tee logs/script_$(date +%Y%m%d_%H%M%S).log
```

---

## 🔄 Workflow Típico

### Desarrollo Backend

```bash
# 1. Entrar a WSL
wsl

# 2. Ir a backend
cd /mnt/e/1/OPOS_GEMINI_1/backend

# 3. Activar venv
source venv/bin/activate

# 4. Editar código (VS Code desde WSL)
code .

# 5. Ejecutar tests
python test_boe_router.py

# 6. Iniciar servidor
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 7. En otra terminal WSL: probar endpoints
curl http://localhost:8000/api/boe/legislacion/lista?limit=2
```

### Desarrollo Frontend

```bash
# 1. Entrar a WSL (o PowerShell)
wsl

# 2. Ir a frontend
cd /mnt/e/1/OPOS_GEMINI_1/frontend

# 3. Instalar dependencias (primera vez)
npm install

# 4. Iniciar dev server
npm run dev

# 5. Abrir browser
# http://localhost:3000
```

---

## 📊 Comparación WSL vs PowerShell

| Acción | WSL | PowerShell |
|--------|-----|------------|
| **Python disponible** | ✅ Nativo | ❌ No en PATH |
| **Virtualenv** | ✅ Funciona perfecto | ⚠️ Requiere configuración |
| **Bash scripts** | ✅ Nativos | ❌ Incompatibles |
| **npm/Node** | ✅ Si está instalado | ✅ Si está instalado |
| **Acceso archivos** | ✅ `/mnt/e/...` | ✅ `E:\...` |
| **Networking** | ✅ Compartido | ✅ Compartido |
| **Performance** | ⚡ Excelente | ⚡ Excelente |

**Recomendación:** Usar WSL para backend Python, PowerShell o WSL para frontend Node.

---

## ✅ Checklist de Configuración

- [x] WSL instalado y funcionando
- [x] Python 3.12.3 en WSL
- [x] Virtualenv creado en `/mnt/e/1/OPOS_GEMINI_1/backend/venv`
- [x] Dependencias instaladas (fastapi, uvicorn, httpx, etc.)
- [x] Puertos 8000, 3000, 6333, 11434 accesibles
- [ ] Aliases de bash configurados
- [ ] Scripts PowerShell creados
- [ ] FastAPI corriendo en background
- [ ] Frontend conectando correctamente al backend

---

**Última actualización:** 5 de diciembre de 2025  
**Autor:** AI Assistant  
**Versión:** 1.0
