# 📋 INVENTARIO COMPLETO DEL SISTEMA OPOS_GEMINI_1

**Fecha verificación:** 16/01/2026 16:00  
**Estado:** ✅ ANÁLISIS EXHAUSTIVO COMPLETO (LOCAL + VPS)

---

## 📊 RESUMEN GENERAL

### Local (WSL):
| Métrica | Valor |
|---------|-------|
| **Subdirectorios raíz** | 48 |
| **Archivos raíz** | 257 |
| **Virtual envs** | 4 |
| **Docker containers** | 18 (4 activos) |
| **Paquetes pip** | 126+ |
| **Ollama modelos** | 2 |
| **Datasets JSONL** | 15+ archivos |
| **Workflows BMAD** | 62 |

### VPS Hostinger (147.93.95.67):
| Métrica | Valor |
|---------|-------|
| **Sistema** | Ubuntu 24.04 LTS |
| **RAM** | 7.8 GB (6.3 GB usados) |
| **Disco** | 96 GB (25 GB usados) |
| **Modelo IA** | Salamandra 7B Q4_K_M (4.85 GB) |
| **Servicios activos** | 4 (llama-server, salamandra-api, nginx, ssh) |
| **Puertos** | 22, 80, 443, 8080, 8001 |

---

## 🐳 DOCKER CONTAINERS (18 total)

### Activos:
| Container | Estado | Imagen | Puerto |
|-----------|--------|--------|--------|
| **opositaia-postgres** | ✅ UP (healthy) | postgres:15-alpine | 5432 |
| **opositaia-qdrant** | ✅ UP | qdrant/qdrant:v1.12.0 | 6333, 6334 |

### Parados (disponibles):
| Container | Imagen |
|-----------|--------|
| opositaia-backend | opos_gemini_1-backend |
| sim_old-simstudio-1 | ghcr.io/simstudioai/simstudio |
| sim_old-realtime-1 | ghcr.io/simstudioai/realtime |
| sim_old-db-1 | pgvector/pgvector:pg17 |
| + 12 backend-run containers | opos_gemini_1-backend |

### docker-compose.yml:
```yaml
services:
  qdrant:     # Puerto 6333, 6334
  postgres:   # Puerto 5432
  backend:    # Puerto 8000 (FastAPI)
volumes:
  qdrant_storage, postgres_data
networks:
  opositaia-network
```

---

## 🐍 VIRTUAL ENVIRONMENTS (4)

| Venv | Ubicación | Propósito |
|------|-----------|-----------|
| **.venv** | `/home/spas/OPOS_GEMINI_1/.venv` | Principal |
| **.venv_cpu** | `.venv_cpu/` | CPU only (sin GPU) |
| **.venv_conversion** | `.venv_conversion/` | Conversión modelos |
| **.venv_kaggle** | `.venv_kaggle/` | Kaggle específico |

---

## 📦 PAQUETES PIP INSTALADOS (126+)

### Principales:
```
httpx==0.28.1
qdrant-client==1.16.1
sentence-transformers==5.2.0
huggingface-hub==0.36.0
grpcio==1.76.0
lxml==6.0.2
aiohttp==3.9.1
cryptography==41.0.7
fsspec==2025.12.0
joblib==1.5.2
```

### ❌ Faltantes:
```
llama-cpp-python  ← Necesario para BGE Reranker
```

---

## 🤖 OLLAMA + MODELOS

```bash
/usr/local/bin/ollama

Modelos instalados:
├── salamandra-base:latest  (4.9 GB, 7.8B, Q4_K_M)
└── mistral:latest          (4.4 GB)
```

---

## 📁 ESTRUCTURA PRINCIPAL

### Raíz del proyecto:
```
/home/spas/OPOS_GEMINI_1/
├── .agent/              # 63 items (workflows BMAD)
│   ├── rules/           # 1 item
│   └── workflows/       # 62 workflows
├── .bmad/               # Sistema BMAD completo
│   ├── _cfg/
│   ├── bmb/
│   ├── bmm/
│   ├── cis/
│   ├── core/
│   └── docs/
├── .claude/             # Config Claude
├── .clinerules/
├── .continue/
├── .cursor/
├── .gemini/             # 67 items
├── .git/
├── .github/             # 17 items (CI/CD)
├── .kiro/
├── .opencode/
├── .roo/
├── .trae/
├── .venv/               # Virtual env principal
├── .venv_cpu/
├── .venv_conversion/
├── .venv_kaggle/
├── .vscode/
├── .windsurf/
```

### Directorios principales:
```
├── academias/           # 331 items
├── backend/             # 109 items (FastAPI)
│   ├── agents/          # 15 scripts ingesta
│   ├── database/
│   ├── routers/         # 9 routers
│   ├── scripts/         # 52 scripts
│   ├── models/          # 1 item (vacío)
│   ├── tests/
│   └── utils/
├── frontend/            # 61 items (Vite + React + TS)
│   ├── components/      # 40 componentes
│   ├── contexts/
│   ├── hooks/
│   ├── services/
│   ├── utils/
│   └── node_modules/
├── data/                # 58 items
│   ├── boe_xml/         # 55 XMLs
│   └── boe_pdf/         # 3 PDFs
├── dataset_generator/   # 140 items
│   ├── MASTER_DATASET_V4/5/6/7/8/9*.jsonl
│   ├── agents/
│   ├── golden_dataset/
│   └── 126+ scripts
├── docs/                # 279 items
│   ├── 01_arquitectura/
│   ├── 02_planes/       # 11 planes
│   ├── 03_investigacion/
│   ├── 04_datasets/
│   ├── 08_guias/
│   ├── 10_memoria/
│   ├── Iideas_rama_gemini/  # 54 ideas
│   └── archive/         # 131 archivados
├── mcp-server/          # MCP TypeScript
│   ├── src/
│   ├── dist/
│   └── .env
├── opos-agents/         # 12 items
│   ├── agents/
│   ├── prompts/
│   ├── tools/
│   └── workflows/
├── llama.cpp/           # Repositorio completo
├── kaggle_dataset/      # Checkpoints
├── kaggle_kernel/
├── model_gguf/
├── model_merged/        # 8 items
├── conceptual_materials/  # 39 items
├── extracted_texts/     # 99 textos
└── staging_area/        # 9 items
```

---

## 📊 BASES DE DATOS

### PostgreSQL (opositaia):
```sql
Tablas:
├── laws             # 48,866 chunks
└── leyes_catalogo   # 54 leyes, 51 columnas

Columnas leyes_catalogo:
- id, boe_id, identificador_eli, nombre_corto, titulo
- tipo_norma, rango_codigo, rango_nombre
- departamento_codigo, departamento_nombre
- fecha_publicacion, fecha_entrada_vigor, fecha_derogacion
- vigente, consolidado, version_consolidada
- url_boe, url_eli, url_pdf, url_xml, url_html
- analisis_modificaciones (JSONB)
- analisis_afecta_a, analisis_afectada_por (JSONB)
- num_articulos, num_disposiciones_*
- texto_completo, xml_original
- materias[], palabras_clave[], tags[]
```

### Qdrant Local:
```
Storage: 610 MB
Colecciones:
├── opositaia_knowledge_hybrid      # 48,866 puntos
├── opositaia_knowledge_hybrid_FULL # 48,329 puntos
└── leyes_espana                    # 1,067 puntos

Vectores: Dense (1024D) + Sparse
HNSW: m=16, ef_construct=100
```

---

## 📄 DATASETS PRINCIPALES

### En raíz:
```
MASTER_DATASET_v11_UTF8_FIXED.jsonl    (1.7 MB)
MASTER_DATASET_v12_PLATINUM.jsonl      (1.9 MB)
gran-basurero.jsonl                    (52 MB)
```

### En dataset_generator/:
```
MASTER_DATASET_V4_FINAL.jsonl          (7.0 MB)
MASTER_DATASET_V5_FINAL.jsonl          (8.2 MB)
MASTER_DATASET_v6_ULTIMATE.jsonl       (8.3 MB)
MASTER_DATASET_v7_EXHAUSTIVE.jsonl     (10.2 MB)
MASTER_DATASET_v8_OMNI.jsonl           (13.5 MB)
MASTER_DATASET_v9_GOLD_OPTIMIZED.jsonl (13.5 MB)
training_data_v9_llama_cpp.txt         (7.9 MB)
groq_batch_500.jsonl                   (403 KB)
```

---

## 🔑 APIs Y CREDENCIALES

### En backend/.env.backend:
```
DEEPSEEK_API_KEY=sk-950b...  ✅
QDRANT_URL=https://...cloud  (backup cloud)
QDRANT_API_KEY=eyJ...
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=opositaia
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

### Kaggle:
```
~/.kaggle/kaggle.json
username: spasmilev
key: KGAT_0ffb...
```

---

## 🤖 SCRIPTS GENERACIÓN (deepseek_*.py)

```
deepseek_COMPLETE.py     ✅ v5.2 - 9.0/10, 1 intento
deepseek_FIXED.py        ✅ v5.1 - Workflow corregido
deepseek_production.py   ⚠️ v5.0
deepseek_advanced.py
deepseek_mcp_real.py
deepseek_mcp_integration.py
```

---

## 🔄 WORKFLOWS BMAD (62 total)

### En .agent/workflows/:
```
/analyst, /architect, /bmad-master, /dev, /pm, /sm, /tea
/bmad-bmm-workflows-create-prd
/bmad-bmm-workflows-create-architecture
/bmad-bmm-workflows-create-story
/bmad-bmm-workflows-dev-story
/bmad-bmm-workflows-code-review
/bmad-bmm-workflows-sprint-planning
/bmad-cis-workflows-design-thinking
/bmad-cis-workflows-innovation-strategy
... y 50+ más
```

---

## 🌐 FRONTEND (Vite + React + TypeScript)

```
frontend/
├── App.tsx
├── index.html
├── package.json (pnpm)
├── vite.config.ts
├── tsconfig.json
├── components/      # 40 componentes
├── services/        # 2 servicios
├── contexts/        # 1 contexto
├── hooks/           # 1 hook
└── utils/           # 3 utilities
```

---

## 🔧 HERRAMIENTAS EXTERNAS

### llama.cpp:
```
llama.cpp/
├── build/
├── ggml/
├── gguf-py/
├── examples/
├── scripts/
└── models/
```

### MCP Server:
```
mcp-server/
├── src/           # TypeScript source
├── dist/          # Compilado
├── .env           # Configuración
└── package.json   # Node.js
```

---

## 🌐 VPS HOSTINGER (PRODUCCIÓN)

### Conexión SSH:
```bash
Host: hostinger
IP: 147.93.95.67
User: ubuntu
Key: ~/.ssh/id_ed25519
```

### Dominio Web:
```
Dominio: electroyhogarpelotazo.tienda
SSL: ✅ Let's Encrypt activo
Ubicación cert: /etc/letsencrypt/live/electroyhogarpelotazo.tienda/
```

### Sistema Operativo:
```
OS: Ubuntu 24.04.3 LTS (Noble Numbat)
Kernel: 6.8.0-71-generic
Arch: x86_64
```

### Recursos Hardware:
| Recurso | Total | Usado | Disponible |
|---------|-------|-------|------------|
| **RAM** | 7.8 GB | 6.3 GB | 1.5 GB |
| **Swap** | 2.0 GB | 9 MB | 2.0 GB |
| **Disco** | 96 GB | 25 GB (27%) | 71 GB |

### Servicios systemd activos:
| Servicio | Estado | Puerto | Descripción |
|----------|--------|--------|-------------|
| **llama-server** | ✅ running | 8080 | Salamandra GGUF (llama.cpp) |
| **salamandra-api** | ✅ running | 8001 | FastAPI wrapper |
| **nginx** | ✅ running | 80, 443 | Reverse proxy |
| **ssh** | ✅ running | 22 | OpenSSH |

### Puertos abiertos:
```
22    - SSH
80    - HTTP (nginx)
443   - HTTPS (nginx)
8080  - llama-server (Salamandra)
8001  - salamandra-api (FastAPI, solo localhost)
```

### Modelo IA instalado:
```
~/models/salamandra-7b-instruct-Q4_K_M.gguf
  Tamaño: 4.85 GB
  Params: 7B
  Quantization: Q4_K_M
  Context: 8192 tokens
```

### Configuración llama-server:
```bash
# /etc/systemd/system/llama-server.service
ExecStart=/usr/local/bin/llama-server \
  -m /home/ubuntu/models/salamandra-7b-instruct-Q4_K_M.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  --ctx-size 8192
User: ubuntu
Restart: always
```

### Configuración salamandra-api:
```bash
# /etc/systemd/system/salamandra-api.service
ExecStart=uvicorn main:app --host 127.0.0.1 --port 8001 --workers 1
WorkingDirectory: /home/ubuntu/salamandra-api
Endpoint: POST /salamandra/reason
```

### API Endpoints VPS:
| Endpoint | URL | Estado |
|----------|-----|--------|
| **llama-server health** | http://147.93.95.67:8080/health | ✅ {"status":"ok"} |
| **salamandra-api health** | localhost:8001/health | ✅ {"status":"ok","service":"salamandra-api"} |
| **salamandra reason** | POST /salamandra/reason | ✅ disponible |

### Estructura directorios VPS:
```
/home/ubuntu/
├── models/
│   └── salamandra-7b-instruct-Q4_K_M.gguf  (4.85 GB)
├── salamandra-api/
│   ├── main.py          # FastAPI wrapper
│   └── venv/            # Python virtualenv
├── opositor_ia/
│   ├── server.py        # Legacy
│   └── venv/
├── Modelfile            # Ollama config (legacy)
└── salamandra_*.json    # Response examples
```

### Sin Docker en VPS:
⚠️ **Docker NO está instalado** en el VPS.  
Los servicios corren directamente en el sistema via systemd.

### Paquetes pip sistema VPS:
```
bcrypt, boto3, botocore, certifi, click,
cloud-init, cryptography, httplib2, etc.
(Instalación mínima del sistema)
```

---

## ❌ LO QUE FALTA IMPLEMENTAR

| Componente | Estado | Ubicación |
|------------|--------|-----------|
| **backend/rag/** | ❌ No existe | Crear directorio |
| **query_expansion.py** | ❌ Código listo | backend/rag/ |
| **relevance_filter.py** | ❌ Código listo | backend/rag/ |
| **reranker.py** | ❌ Código listo | backend/rag/ |
| **legal_judge.py** | ❌ Por crear | backend/rag/ |
| **agentic_pipeline.py** | ❌ Código listo | backend/rag/ |
| **BGE Reranker GGUF** | ❌ No descargado | backend/models/ |
| **llama-cpp-python** | ❌ No instalado | pip install |
| **Metadata Qdrant** | ⚠️ Solo 6 campos | FASE 0 re-ingest |

---

## 📊 TAMAÑOS DE ALMACENAMIENTO

| Componente | Tamaño |
|------------|--------|
| Qdrant storage | 610 MB |
| gran-basurero.jsonl | 52 MB |
| MASTER_DATASET_v9 | 13.5 MB |
| backend_debug.log | 13.8 MB |
| llama.cpp/ | ~500 MB (estimado) |
| .venv + venvs | ~2-3 GB (estimado) |
| node_modules (frontend) | ~200-500 MB |

---

## ✅ PRÓXIMOS PASOS

### Inmediatos (FASE 0-1):
1. Crear `backend/rag/` directory
2. Instalar `pip install llama-cpp-python`
3. Descargar BGE Reranker (350 MB)
4. Re-ingestar Qdrant con metadata rica

### Corto plazo (FASE 2-4):
5. Implementar componentes RAG
6. Crear Legal Judge Agent
7. Integrar pipeline en FastAPI
8. Testing y benchmark

---

*Inventario exhaustivo completado 16/01/2026 15:45*
