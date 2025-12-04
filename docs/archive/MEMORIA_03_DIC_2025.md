# 📚 MEMORIA TÉCNICA OPOSITAIA - 3 Diciembre 2025

> **DOCUMENTO DE REFERENCIA RÁPIDA** - Consultar antes de cada sesión de trabajo

---

## 🎯 RESUMEN EJECUTIVO

**Proyecto**: OpositAIA - Plataforma de preparación de oposiciones con IA
**Estado**: Sprint 16 en progreso - Agente Mistral con herramientas reales
**Ubicación Windows**: `E:\1\OPOS_GEMINI_1\`
**Ubicación WSL**: `/home/espasiko/OPOS_GEMINI_1/`

---

## 🏗️ ARQUITECTURA DEL SISTEMA

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         OPOSITAIA ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
│  │   FRONTEND  │    │   BACKEND   │    │   MISTRAL   │                 │
│  │   React/TS  │◄──►│   FastAPI   │◄──►│   AGENT     │                 │
│  │   Vite      │    │   Python    │    │   Studio    │                 │
│  └─────────────┘    └─────────────┘    └─────────────┘                 │
│         │                  │                  │                         │
│         ▼                  ▼                  ▼                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    INFRAESTRUCTURA                              │   │
│  ├─────────────┬─────────────┬─────────────┬─────────────────────┤   │
│  │   Qdrant    │   Ollama    │  PostgreSQL │      VPS            │   │
│  │   (Docker)  │   (WSL)     │   (Docker)  │   (Hostinger)       │   │
│  └─────────────┴─────────────┴─────────────┴─────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🐍 ENTORNOS VIRTUALES (VENV)

### ✅ ACTIVOS (3 necesarios)

| Entorno | Ubicación | Propósito | Python | Activación |
|---------|-----------|-----------|--------|------------|
| **backend/venv** | Windows | FastAPI + APIs | 3.12 | `.\backend\venv\Scripts\activate` |
| **dataset_generator/venv** | Windows | Generación Q&A | 3.12 | `.\dataset_generator\venv\Scripts\activate` |
| **venv_indexer** | WSL | Indexación BGE-M3 | 3.10+ | `source venv_indexer/bin/activate` |

### ❌ ELIMINAR (duplicado)
- `elemplos_leyes_info/venv/` - Redundante, creado en WSL (tiene bin/ en lugar de Scripts/)

### 🔍 CÓMO IDENTIFICAR EL ENTORNO

#### Windows (PowerShell):
```powershell
# Verificar si venv está activo
$env:VIRTUAL_ENV  # Debe mostrar ruta del venv

# Ver qué Python se está usando
Get-Command python | Select-Object Source

# Ver versión de Python
python --version

# Listar paquetes instalados
pip list
```

#### WSL (Bash):
```bash
# Verificar si venv está activo
echo $VIRTUAL_ENV  # Debe mostrar ruta del venv

# Ver qué Python se está usando
which python3

# Ver versión de Python
python3 --version

# Listar paquetes instalados
pip list
```

### 📍 UBICACIONES EXACTAS

#### Windows:
```
E:\1\OPOS_GEMINI_1\backend\venv\
├── Scripts\          ← Carpeta de activación en Windows
│   ├── activate.ps1  ← Para PowerShell
│   ├── activate.bat  ← Para CMD
│   ├── python.exe    ← Python del venv
│   └── pip.exe       ← Pip del venv
└── Lib\
    └── site-packages\  ← Paquetes instalados

E:\1\OPOS_GEMINI_1\dataset_generator\venv\
└── (misma estructura)
```

#### WSL:
```
/home/espasiko/OPOS_GEMINI_1/venv_indexer/
├── bin/              ← Carpeta de activación en Linux
│   ├── activate      ← Script de activación
│   ├── python3       ← Python del venv
│   └── pip           ← Pip del venv
└── lib/
    └── python3.x/
        └── site-packages/  ← Paquetes instalados
```

### 🚨 PROBLEMA COMÚN: Ejecutar desde Windows un script que necesita venv de WSL

**Síntoma**: `ModuleNotFoundError: No module named 'httpx'` aunque httpx esté instalado

**Causa**: Estás en Windows PowerShell intentando ejecutar un script que usa el venv de WSL

**Solución**:
```bash
# Opción 1: Ejecutar desde WSL
wsl
cd /home/espasiko/OPOS_GEMINI_1
source venv_indexer/bin/activate
python3 backend/agents/test_agent_completo.py

# Opción 2: Usar el venv correcto de Windows
cd E:\1\OPOS_GEMINI_1\backend
.\venv\Scripts\activate
python agents/test_agent_completo.py
```

### Comandos de activación:
```bash
# Windows PowerShell - Backend
cd E:\1\OPOS_GEMINI_1\backend
.\venv\Scripts\activate

# Windows PowerShell - Dataset Generator
cd E:\1\OPOS_GEMINI_1\dataset_generator
.\venv\Scripts\activate

# WSL - Indexación
cd /home/espasiko/OPOS_GEMINI_1
source venv_indexer/bin/activate
```

### 🔧 INSTALAR DEPENDENCIAS

```bash
# Windows - Backend
cd E:\1\OPOS_GEMINI_1\backend
.\venv\Scripts\activate
pip install -r requirements.txt

# Windows - Dataset Generator
cd E:\1\OPOS_GEMINI_1\dataset_generator
.\venv\Scripts\activate
pip install -r requirements.txt

# WSL - Indexación
cd /home/espasiko/OPOS_GEMINI_1
source venv_indexer/bin/activate
pip install -r backend/requirements.txt
```

---

## 🐳 DOCKER & CONTENEDORES

### docker-compose.yml
```yaml
services:
  qdrant:      # Puerto 6333 (HTTP), 6334 (gRPC)
  ollama:      # Puerto 11434
  backend:     # Puerto 8000
```

### Comandos Docker:
```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f qdrant

# Reiniciar Qdrant
docker-compose restart qdrant

# Ver estado
docker ps
```

---

## 📊 QDRANT - BASE DE DATOS VECTORIAL

### Configuración
| Parámetro | Valor |
|-----------|-------|
| **URL Local** | `http://localhost:6333` |
| **URL Cloud** | `https://b554ceb5-2169-4064-9ce7-83c8cd44cf84.europe-west3-0.gcp.cloud.qdrant.io` |
| **API Key Cloud** | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (ver .env.backend) |

### Colecciones
| Colección | Documentos | Descripción |
|-----------|------------|-------------|
| `opositaia_leyes_seguridad_social` | ~7,861 | Leyes y temarios |
| `materiales_academia` | ~364 | Exámenes y materiales |
| `qa_cache` | Variable | Caché semántica |

### Verificar Qdrant:
```bash
# Desde Windows
curl http://localhost:6333/collections

# Desde WSL
curl http://localhost:6333/collections
```

---

## 🤖 MISTRAL AGENT STUDIO

### Configuración
```env
MISTRAL_API_KEY=FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF
MISTRAL_AGENT_ID=ag_019ad601946d7323a81c544229de40a1
MISTRAL_MODEL=mistral-large-latest
```

### Cómo usar el Agente (según docs.mistral.ai):
```python
from mistralai import Mistral

client = Mistral(api_key="FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF")

# Opción 1: Usar agent_id como modelo
response = client.chat.complete(
    model="ag_019ad601946d7323a81c544229de40a1",  # Agent ID
    messages=[{"role": "user", "content": "Tu pregunta"}]
)

# Opción 2: API de Agentes (Beta)
response = client.agents.complete(
    agent_id="ag_019ad601946d7323a81c544229de40a1",
    messages=[{"role": "user", "content": "Tu pregunta"}]
)
```

### Capacidades del Agente Mistral Studio:
- ✅ **Web Search**: Puede buscar en internet
- ✅ **Code Interpreter**: Puede ejecutar código
- ✅ **Image Generation**: Puede generar imágenes
- ✅ **Document Library**: RAG integrado
- ✅ **Function Calling**: Herramientas personalizadas
- ✅ **MCP Servers**: Integración con servidores MCP

---

## 🔑 API KEYS (en .env.backend)

| Servicio | Variable | Estado |
|----------|----------|--------|
| Mistral | `MISTRAL_API_KEY` | ✅ Activa |
| Groq | `GROQ_API_KEY` | ✅ Activa |
| DeepSeek | `DEEPSEEK_API_KEY` | ✅ Activa |
| Gemini | `GEMINI_API_KEY` | ✅ Activa |
| Claude | `CLAUDE_API_KEY` | ✅ Activa |
| Cohere | `COHERE_API_KEY` | ✅ Activa |
| HuggingFace | `HF_TOKEN` | ✅ Activa |

---

## 🖥️ VPS HOSTINGER

### Conexión SSH
```bash
# Desde Windows PowerShell
ssh root@147.93.95.67

# Desde WSL
ssh root@147.93.95.67
```

### Servicios en VPS
| Servicio | Puerto | URL |
|----------|--------|-----|
| Mistral Local | 8080 | `http://147.93.95.67:8080` |
| Nginx | 80/443 | `http://147.93.95.67` |

### Configuración VPS en .env:
```env
MISTRAL_URL=http://147.93.95.67:8080
```

---

## 📁 ESTRUCTURA DE DIRECTORIOS CLAVE

```
E:\1\OPOS_GEMINI_1\
├── backend/                    # FastAPI Backend
│   ├── agents/                 # Agentes y herramientas
│   │   ├── mistral_tools.py    # 9 herramientas reales ✅
│   │   ├── mistral_agent_v2.py # Agente integrado
│   │   ├── boe_downloader.py   # Descarga BOE
│   │   └── rag_agent_v2.py     # RAG Agent
│   ├── routers/                # Endpoints FastAPI
│   ├── tests/                  # Tests unitarios
│   ├── venv/                   # Entorno virtual ✅
│   └── .env.backend            # Configuración
├── dataset_generator/          # Generación de Q&A
│   ├── venv/                   # Entorno virtual ✅
│   └── *.py                    # Scripts de generación
├── ai-specs/                   # Especificaciones
│   ├── changes/                # Sprints
│   └── specs/                  # Documentación técnica
├── components/                 # React Components
├── services/                   # Frontend Services
├── docs/                       # Documentación
└── qdrant_storage/             # Datos Qdrant local
```

---

## 🧪 COMANDOS DE TEST

### Tests de Herramientas Mistral (Windows)
```powershell
cd E:\1\OPOS_GEMINI_1\backend
.\venv\Scripts\activate
python tests/test_mistral_tools.py
```

### Tests de Herramientas Mistral (WSL)
```bash
cd /home/espasiko/OPOS_GEMINI_1
source venv_indexer/bin/activate
python3 backend/tests/test_mistral_tools.py
```

### Test del Agente Mistral Studio
```bash
# WSL
cd /home/espasiko/OPOS_GEMINI_1
source venv_indexer/bin/activate
python3 backend/agents/test_mistral_studio_agent.py
```

---

## 🚀 INICIAR EL SISTEMA

### 1. Iniciar Docker (Qdrant + PostgreSQL)
```bash
cd E:\1\OPOS_GEMINI_1
docker-compose up -d qdrant
```

### 2. Iniciar Backend (Windows)
```powershell
cd E:\1\OPOS_GEMINI_1\backend
.\venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Iniciar Frontend
```powershell
cd E:\1\OPOS_GEMINI_1
npm run dev
```

---

## 📋 SPRINT 16 - ESTADO ACTUAL

### Tareas Completadas ✅
- [x] T-16.1: `mistral_tools.py` con 9 herramientas
- [x] T-16.2: `buscar_rag_qdrant()` funcionando
- [x] T-16.3: `buscar_boe_oficial()` funcionando
- [x] T-16.4: `verificar_url_boe()` funcionando
- [x] T-16.5: `calcular_prestacion_ss()` funcionando
- [x] T-16.6: Colección `qa_cache` creada
- [x] T-16.7: Clase `SemanticCache` implementada
- [x] T-16.9: Métricas de hit rate

### Tareas Pendientes 🔄
- [ ] T-16.8: Integrar caché con pipeline
- [ ] T-16.10: `mistral_agent_v2.py` completo
- [ ] T-16.11: Tool calling con Mistral API
- [ ] T-16.12: `verificar_qa_completa()` E2E
- [ ] T-16.13: Tests de integración

### Tests Pasados: 7/7 (100%)
| Test | Estado |
|------|--------|
| buscar_rag_qdrant | ✅ |
| buscar_boe_oficial | ✅ |
| verificar_url_boe | ✅ |
| calcular_prestacion_ss | ✅ |
| clasificar_qa_tema | ✅ |
| extraer_articulos_texto | ✅ |
| semantic_cache | ✅ |

---

## 🔧 HERRAMIENTAS IMPLEMENTADAS

### En `backend/agents/mistral_tools.py`:
1. **buscar_rag_qdrant()** - Búsqueda semántica en Qdrant
2. **buscar_boe_oficial()** - Búsqueda en BOE
3. **verificar_url_boe()** - Verificación de URLs
4. **calcular_prestacion_ss()** - Cálculos SS (jubilación, IMV)
5. **generar_qa_legal()** - Preparar contexto para Q&A
6. **verificar_qa_completa()** - Verificación exhaustiva
7. **clasificar_qa_tema()** - Clasificación por tema
8. **extraer_articulos_texto()** - Extracción de referencias
9. **obtener_normativa_vigente()** - Normativa actualizada

---

## 📊 MÉTRICAS Y COSTES

### Costes por Proveedor (aproximados)
| Proveedor | Coste/1M tokens | Uso recomendado |
|-----------|-----------------|-----------------|
| Groq | GRATIS (500K/día) | Desarrollo |
| DeepSeek | $0.21 | Producción económica |
| Mistral | $0.25-2 | Agente principal |
| Claude | $3-15 | Q&A complejas |
| Gemini | GRATIS (1.5M/día) | Desarrollo |

### Ahorro con Caché Semántica
- **Objetivo**: 60-70% reducción de llamadas LLM
- **Coste estimado sin caché**: $2/día
- **Coste estimado con caché**: $0.60-0.80/día

---

## 🐧 WSL - COMANDOS ÚTILES

```bash
# Acceder a WSL
wsl

# Navegar al proyecto
cd /home/espasiko/OPOS_GEMINI_1

# Activar entorno
source venv_indexer/bin/activate

# Ver procesos Python
ps aux | grep python

# Matar proceso
kill -9 <PID>

# Acceder a archivos Windows desde WSL
cd /mnt/e/1/OPOS_GEMINI_1
```

---

## 🔗 ENLACES ÚTILES

- **Mistral Docs**: https://docs.mistral.ai/
- **Mistral Agents**: https://docs.mistral.ai/capabilities/agents/
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **BOE API**: https://www.boe.es/datosabiertos/

---

## ⚠️ PROBLEMAS CONOCIDOS Y SOLUCIONES

### 1. Python no encontrado en Windows
```powershell
# Usar ruta completa o activar venv primero
.\venv\Scripts\python.exe script.py
```

### 2. Qdrant no responde
```bash
docker-compose restart qdrant
docker logs opositaia-qdrant
```

### 3. Error de conexión WSL ↔ Windows
```bash
# Usar localhost, no 127.0.0.1
curl http://localhost:6333/collections
```

### 4. Mistral API timeout
```python
# Aumentar timeout
client = Mistral(api_key=key, timeout=60)
```

---

## 📝 NOTAS IMPORTANTES

1. **Siempre activar venv** antes de ejecutar scripts Python
2. **Qdrant debe estar corriendo** antes de tests
3. **WSL para indexación** (BGE-M3 funciona mejor)
4. **Windows para desarrollo** (FastAPI, tests)
5. **Agente Mistral Studio** tiene web search integrado
6. **Caché semántica** reduce costes 60-70%

---

**Última actualización**: 3 Diciembre 2025
**Autor**: AI Assistant + Usuario
**Versión**: 1.0
