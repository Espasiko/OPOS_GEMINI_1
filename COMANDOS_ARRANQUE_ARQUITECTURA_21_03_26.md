# 🏗️ ARQUITECTURA COMPLETA Y COMANDOS DE ARRANQUE — OpositAIA
## Actualizado: 21/03/2026 — Para que cualquier IA pueda conocer el sistema al completo

---

## 📍 1. INFORMACIÓN GLOBAL DEL PROYECTO

| Dato | Valor |
|------|-------|
| **Nombre** | OpositAIA |
| **Propósito** | Sistema multi-agente RAG para generar casos prácticos de oposiciones (Gestión SS A2) |
| **Raíz del proyecto** | `/home/spas/OPOS_GEMINI_1/` |
| **Usuario OS** | `spas` (Linux Ubuntu) |
| **Fecha documento** | 21/03/2026 |

---

## 🌐 2. SERVIDOR HOSTINGER / DOMINIO PÚBLICO

| Campo | Valor |
|-------|-------|
| **Dominio público** | `https://electroyhogarpelotazo.tienda` |
| **Proveedor** | Hostinger (VPS) |
| **API Backend pública** | `https://electroyhogarpelotazo.tienda` |
| **Variable de entorno** | `VITE_VPS_API_URL=https://electroyhogarpelotazo.tienda` |
| **Uso** | El frontend accede al backend VPS en producción a través de este dominio |

> ⚠️ En desarrollo local el frontend apunta a `http://localhost:8000` directamente.

---

## 🐍 3. PYTHON — ENTORNO VIRTUAL (VENV)

### VENV CORRECTO (usar siempre este):
```bash
# VENV REAL: en la RAÍZ del proyecto (NO en backend/venv — ese NO existe)
/home/spas/OPOS_GEMINI_1/.venv/

# Activar manualmente:
source /home/spas/OPOS_GEMINI_1/.venv/bin/activate

# Python del venv:
/home/spas/OPOS_GEMINI_1/.venv/bin/python   # → Python 3.12.x

# uvicorn del venv:
/home/spas/OPOS_GEMINI_1/.venv/bin/uvicorn

# Paquetes instalados: 229 paquetes
```

### Versiones verificadas (21/03/2026):
```
Python:  3.12.3  (via .venv)
Node.js: v24.11.1
pnpm:    10.19.0
```

### ⚠️ Trampas conocidas con el venv:
- El script `scripts/maintenance/start-backend.sh` apuntaba a `backend/venv` — **YA CORREGIDO** al venv raíz
- El Python del sistema (`/usr/bin/python3`) NO tiene uvicorn ni fastapi instalado
- Siempre usar el `.venv` de la raíz del proyecto

---

## 🚀 4. COMANDOS DE ARRANQUE COMPLETOS

### 4.1 Backend FastAPI (Puerto 8000)
```bash
# COMANDO DIRECTO (recomendado — sin activar venv):
cd /home/spas/OPOS_GEMINI_1/backend
/home/spas/OPOS_GEMINI_1/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# CON VENV ACTIVADO:
source /home/spas/OPOS_GEMINI_1/.venv/bin/activate
cd /home/spas/OPOS_GEMINI_1/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# USANDO EL SCRIPT (actualizado 21/03/2026):
bash /home/spas/OPOS_GEMINI_1/scripts/maintenance/start-backend.sh

# Verificar que está up:
curl http://localhost:8000/
# → Responde: {"name":"OpositAIA API","version":"2.0.0","status":"healthy",...}
```

### 4.2 Frontend React/Vite (Puerto 5173)
```bash
cd /home/spas/OPOS_GEMINI_1/frontend
pnpm dev
# → Arranca en http://localhost:5173

# Build producción:
pnpm build
# → Genera dist/ para desplegar en Hostinger

# Preview build:
pnpm preview
```

### 4.3 Docker — Todos los servicios
```bash
# Arrancar todos (desde la raíz del proyecto):
cd /home/spas/OPOS_GEMINI_1
docker-compose up -d

# Arrancar solo DB (sin backend Docker — usar el local):
docker-compose up -d qdrant postgres neo4j

# Ver estado:
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

# Parar todo:
docker-compose down
```

### 4.4 MCP Node.js server
```bash
# MCP Server de OpositAIA (RAG access para otras IAs):
cd /home/spas/OPOS_GEMINI_1/mcp-server
pnpm start
# → Usa dist/index.js

# Build primero si es necesario:
pnpm build
# → Genera dist/ desde src/

# Development mode (watch):
pnpm dev
```

### 4.5 Generador V13 (pipeline de casos prácticos)
```bash
cd /home/spas/OPOS_GEMINI_1
source .venv/bin/activate
python backend/scripts/run_ecosistema_v13_mistral_engine.py

# Script antiguo V12:
python backend/scripts/run_ecosistema_mistral_v12.py
```

---

## 🐋 5. DOCKER — CONTENEDORES Y CREDENCIALES

### Contenedores activos (21/03/2026 — UP 5 días):

| Contenedor | Imagen | Puerto Host | Puerto Interno | Credenciales |
|-----------|--------|-------------|----------------|-------------|
| `opositaia-neo4j` | `neo4j:5-community` | 7474 (HTTP), 7687 (Bolt) | 7474, 7687 | `neo4j / opositaia2026` |
| `opositaia-qdrant` | `qdrant/qdrant:v1.12.0` | 6333 (HTTP), 6334 (gRPC) | 6333, 6334 | Sin auth |
| `opositaia-postgres` | `postgres:15-alpine` | 5432 | 5432 | `postgres / postgres`, DB: `opositaia` |
| `affectionate_cori` | `ghcr.io/github/github-mcp-server` | — | — | GitHub MCP (token en env) |

### Comandos Docker útiles:
```bash
# Ver logs de Neo4j:
docker logs opositaia-neo4j --tail 50

# Conectar a Neo4j Browser:
# Abrir: http://localhost:7474
# User: neo4j | Password: opositaia2026

# Query Cypher desde terminal:
docker exec opositaia-neo4j cypher-shell -u neo4j -p opositaia2026 "MATCH (n) RETURN COUNT(n)"

# Conectar a Postgres:
docker exec -it opositaia-postgres psql -U postgres -d opositaia

# Reiniciar un contenedor:
docker restart opositaia-neo4j

# Ver volumes:
docker volume ls
# neo4j_data, neo4j_logs, neo4j_import, neo4j_plugins
# postgres_data, qdrant_storage
```

### docker-compose.yml — Ubicación:
```
/home/spas/OPOS_GEMINI_1/docker-compose.yml
```

---

## 📂 6. ESTRUCTURA DE CARPETAS DEL PROYECTO

```
/home/spas/OPOS_GEMINI_1/
│
├── 🐍 .venv/                          ← VENV Python 3.12 (229 paquetes)
├── 🌐 frontend/                        ← React + Vite + TypeScript (pnpm)
│   ├── App.tsx
│   ├── components/
│   ├── contexts/
│   ├── hooks/
│   ├── index.html
│   ├── index.tsx
│   ├── package.json                    ← scripts: dev, build, test, lint
│   ├── pnpm-lock.yaml
│   └── .env                           ← VITE_VPS_API_URL, VITE_ENABLE_RAG
│
├── ⚡ backend/                          ← FastAPI Python
│   ├── main.py                         ← Entry point, 8 routers incluidos
│   ├── .env.backend                    ← LLM API keys, DB config
│   ├── requirements.txt
│   ├── agents/                         ← Lógica LLM
│   │   ├── agent_engine.py             ← Motor principal de agentes YAML
│   │   ├── llm_providers.py            ← 7 proveedores (Groq/DeepSeek/Gemini/Mistral/HF/Cohere/Claude)
│   │   ├── rag_helper.py               ← Qdrant RAG (colección FULL_XML)
│   │   └── verification_agents.py      ← Sieves de calidad (parcialmente decorativos — V14 lo repara)
│   ├── calculators/                    ← 22+ calculadoras SS y AGE
│   │   ├── dispatcher.py               ← Dispatcher central
│   │   ├── calculos_ss.py
│   │   ├── calculos_ss_extended.py     ← El más grande (83KB)
│   │   ├── calculos_imv.py
│   │   ├── calculadora_age.py
│   │   └── calculadora_presupuesto.py
│   ├── routers/                        ← Endpoints FastAPI
│   │   ├── rag.py                      ← /api/rag/ V1 legacy
│   │   ├── rag_v2.py                   ← /api/v2/rag/ (búsqueda híbrida)
│   │   ├── chat.py                     ← /api/chat/ — Chat con RAG
│   │   ├── upload.py                   ← /api/upload/
│   │   ├── ai_functions.py             ← /api/ai/ — multi-provider
│   │   ├── user.py                     ← /api/user/
│   │   ├── boe.py                      ← /api/boe/ — API oficial BOE
│   │   └── mcp_gateway.py              ← /mcp/ — Gateway MCP HTTP
│   ├── mcp_servers/
│   │   └── legal_graph_mcp.py          ← MCP SQLite para grafo legal (ACTUALMENTE VACÍO)
│   └── scripts/
│       ├── run_ecosistema_v13_mistral_engine.py  ← Pipeline V13 activo
│       └── run_ecosistema_mistral_v12.py         ← Pipeline V12
│
├── 🤖 opos-agents/                     ← Sistema de agentes YAML
│   ├── config.yaml                     ← Modelos: salamandra, groq-70b, deepseek-r1, claude, mistral-large
│   ├── agents/                         ← 10 agentes YAML
│   │   ├── investigator_v13.yaml       ← Fact mining (Mistral-large, T=0.1, search_rag+ejecutar_calculo)
│   │   ├── redactor_v13.yaml           ← Generador caso (Mistral-large, T=1.0, 3 tools)
│   │   ├── validator.yaml              ← Validador (NO llamado por V13 — existe pero inactivo)
│   │   ├── orchestrator.yaml
│   │   ├── examiner.yaml
│   │   ├── generator.yaml / generator_r1.yaml
│   │   ├── intent.yaml
│   │   ├── resumidor.yaml
│   │   └── compile.yaml
│   └── docs_ideas_sistema_agentes/
│
├── 📦 mcp-server/                      ← MCP Node.js (@opositaia/mcp-server)
│   ├── src/                            ← TypeScript source
│   ├── dist/                           ← Build JS (ejecutar con pnpm start)
│   ├── package.json
│   └── .env
│
├── 🧠 _bmad/                           ← BMAD Method agents framework
│   ├── core/                           ← bmad-master, config.yaml
│   ├── cis/                            ← Innovation agents
│   ├── tea/                            ← Testing agents
│   ├── wds/                            ← Web design agents
│   └── _memory/                        ← Memoria BMAD
│
├── .agents/                            ← Skills BMAD (87+ skills)
├── .agent/                             ← Workflows (bmad method)
├── .gemini/                            ← Config Antigravity AI
├── .claude/                            ← Config Claude
├── .cursor/                            ← Config Cursor
├── .continue/                          ← Config Continue.dev
│
├── 📚 academias/                       ← Material académico oposiciones
│   ├── 1_casos_recientes_2026_DM/      ← Casos Diego de Miguel 2026
│   │   ├── arquitectura_10_10_v14.md   ← Plan V14 (658 líneas, ACTUALIZADO 21/03)
│   │   └── auditoria_v13_1683ddbe.md   ← Auditoría V13
│   ├── textos_limpios/                 ← 242 archivos OCR'd y anonimizados
│   ├── textos_anonimizados/
│   ├── de la academia de radi/
│   ├── Opos de Radi todo/
│   └── temario_oficial/
│
├── 📊 docs/
│   └── 10_memoria/
│       └── ESTADO_REAL_Y_ARQUITECTURA_20_02_26.md
│
├── 🔑 .env                             ← Raíz: VITE_*, API keys globales
├── docker-compose.yml
├── COMANDOS_ARRANQUE_ARQUITECTURA_21_03_26.md  ← ESTE FICHERO
└── LISTA_COMPLETA_TRAMPAS_PEDAGOGICAS.md
```

---

## 🔑 7. FICHEROS .ENV — UBICACIONES Y PROPÓSITO

| Fichero | Ubicación | Propósito |
|---------|-----------|-----------|
| `.env` | `/home/spas/OPOS_GEMINI_1/.env` | Variables globales + VITE_VPS_API_URL |
| `backend/.env.backend` | `/home/spas/OPOS_GEMINI_1/backend/.env.backend` | **PRINCIPAL**: LLM keys (Groq, DeepSeek, Gemini, Mistral, Claude, HF, Cohere) + DB config |
| `frontend/.env` | `/home/spas/OPOS_GEMINI_1/frontend/.env` | VITE_VPS_API_URL, feature flags |
| `mcp-server/.env` | `/home/spas/OPOS_GEMINI_1/mcp-server/.env` | Config del MCP Node.js |

### Variables de entorno CRÍTICAS (backend/.env.backend):
```bash
# LLM Providers (las keys reales están en el fichero .env.backend — NO en Git):
GROQ_API_KEY=gsk_...
DEEPSEEK_API_KEY=sk-...
GEMINI_API_KEY=AIza...
MISTRAL_API_KEY=...
CLAUDE_API_KEY=sk-ant-...
HF_TOKEN=hf_...
COHERE_API_KEY=...

# Databases (Docker local):
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=opositaia_knowledge_FULL_XML
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=opositaia2026
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=opositaia
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Embedding Model:
EMBEDDING_MODEL=pablosi/bge-m3-spa-law-qa-trained-2

# Frontend URL para CORS:
CORS_ORIGINS=http://localhost:5173,https://electroyhogarpelotazo.tienda
```

---

## 🌐 8. API ENDPOINTS FASTAPI (Puerto 8000)

### Docs interactivos:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints principales:

| Router | Prefijo | Descripción |
|--------|---------|-------------|
| `rag.py` | `/api/rag/` | Búsqueda RAG V1 (legacy) |
| `rag_v2.py` | `/api/v2/rag/` | Búsqueda RAG V2 híbrida (Dense+BM25) |
| `chat.py` | `/api/chat/` | Chat con LLM + RAG |
| `upload.py` | `/api/upload/` | Subida ficheros y URLs |
| `ai_functions.py` | `/api/ai/` | Funciones AI multi-proveedor |
| `user.py` | `/api/user/` | Gestión usuarios |
| `boe.py` | `/api/boe/` | API oficial datos abiertos BOE |
| `mcp_gateway.py` | `/mcp/` | Gateway MCP HTTP para otras IAs |

### Endpoint MCP Gateway (para agentes externos):
```bash
# Verificar BOE:
curl -X POST http://localhost:8000/mcp/verify_boe \
  -H "Content-Type: application/json" \
  -d '{"article": "Art. 173.1 TRLGSS"}'

# Buscar en RAG:
curl -X POST http://localhost:8000/mcp/search_rag \
  -H "Content-Type: application/json" \
  -d '{"query": "incapacidad temporal accidente trabajo", "limit": 3}'

# Ejecutar calculadora:
curl -X POST http://localhost:8000/mcp/ejecutar_calculo \
  -H "Content-Type: application/json" \
  -d '{"query": "IT accidente trabajo salario 1600 euros mes anterior"}'
```

---

## 🔍 9. QDRANT — BASE VECTORIAL RAG

| Campo | Valor |
|-------|-------|
| **URL local** | `http://localhost:6333` |
| **Colección activa** | `opositaia_knowledge_FULL_XML` |
| **Puntos indexados** | ~14.038 |
| **Modelo embedding** | `pablosi/bge-m3-spa-law-qa-trained-2` |
| **Búsqueda** | Híbrida Dense (BGE-M3) + Sparse (BM25) |
| **Metadatos por punto** | >50 (vigente, article_id, law_title, boe_id, url, fecha_vigencia, derogated_by...) |
| **Fecha de corte SS** | `2026-03-04` (Solo normas vigentes hasta esta fecha para oposición SS) |

```bash
# Verificar Qdrant:
curl http://localhost:6333/collections/opositaia_knowledge_FULL_XML
curl http://localhost:6333/dashboard  # Browser dashboard
```

---

## 🕸️ 10. NEO4J — GRAFO DE CONOCIMIENTO LEGAL

| Campo | Valor |
|-------|-------|
| **Contenedor** | `opositaia-neo4j` |
| **Browser** | `http://localhost:7474` |
| **Bolt URI** | `bolt://localhost:7687` |
| **Usuario** | `neo4j` |
| **Contraseña** | `opositaia2026` |
| **Estado actual** | UP (healthy), pero VACÍO — solo 6 artículos ejemplo |
| **Driver Python** | `neo4j` (pip install neo4j) |

```bash
# Conectar desde terminal:
docker exec opositaia-neo4j cypher-shell -u neo4j -p opositaia2026

# Query ejemplo:
MATCH (n) RETURN COUNT(n) AS total;
MATCH (a:Articulo {id: "Art. 173.1"}) RETURN a;

# Poblar desde Python (script a crear):
python backend/scripts/populate_legal_graph_from_qdrant.py
```

---

## 🤖 11. SISTEMA DE AGENTES

### 11.1 Agentes YAML (backend) — `opos-agents/agents/`

| Agente | Fichero | Modelo | Temperatura | Tools | Estado |
|--------|---------|--------|-------------|-------|--------|
| **Investigador V13** | `investigator_v13.yaml` | `mistral-large-latest` | 0.1 | search_rag, ejecutar_calculo | ✅ Activo |
| **Redactor V13** | `redactor_v13.yaml` | `mistral-large-latest` | 1.0 | search_rag, ejecutar_calculo, verify_boe | ✅ Activo |
| **Validator** | `validator.yaml` | — | — | search_rag | ❌ No llamado en pipeline |
| **Orchestrator** | `orchestrator.yaml` | — | — | — | ❌ No activo |
| **Examiner** | `examiner.yaml` | — | — | — | ❌ Antiguo |
| **Generator** | `generator.yaml` | — | — | — | ❌ Antiguo |
| **Generator R1** | `generator_r1.yaml` | DeepSeek R1 | — | — | ❌ Antiguo |
| **Intent** | `intent.yaml` | — | — | — | ❌ Antiguo |
| **Resumidor** | `resumidor.yaml` | — | — | — | ❌ Antiguo |
| **Compile** | `compile.yaml` | — | — | — | ❌ Antiguo |

### 11.2 Flujo V13 activo:
```
run_ecosistema_v13_mistral_engine.py
  → investigator_v13 (Mistral-large, T=0.1) → Fact Sheet
  → redactor_v13 (Mistral-large, T=1.0) → Caso Completo Markdown
  → SilentSieveOrchestrator (5 sieves, 3 decorativos — V14 los repara)
```

### 11.3 BMAD Method (`_bmad/`)
- **87+ skills** en `.agents/skills/`
- Activar agente: mencionar en chat del IDE el nombre del skill
- Ejemplo: `@bmad-master`, `/bmad-sprint-planning`, `/bmad-create-prd`

### 11.4 MCP Node.js (`mcp-server/`)
- Nombre paquete: `@opositaia/mcp-server`
- Accede al RAG de Qdrant para otras IAs
- Arranque: `cd mcp-server && pnpm start`

---

## ⚙️ 12. PROVEEDORES LLM CONFIGURADOS

| Proveedor | Modelo default | Uso en pipeline |
|-----------|---------------|-----------------|
| **Mistral** | `mistral-large-latest` | ✅ V13 ACTIVO (investigator + redactor) |
| **Groq** | `llama-3.3-70b-versatile` | ✅ Disponible (rápido, gratis 500K/día) |
| **DeepSeek** | `deepseek-reasoner` (R1) | ✅ Disponible (razonamiento) |
| **Gemini** | `gemini-2.5-flash` | ✅ Disponible |
| **Claude** | `claude-3-5-sonnet` | ✅ Disponible (gold standard legal) |
| **Cohere** | — | ✅ Disponible (reranking) |
| **HuggingFace** | Salamandra R1 | ✅ Via VPS/Ollama local |
| **Ollama local** | `salamandra-r1:q5km` | ✅ Si Ollama está corriendo |

---

## 🧮 13. CALCULADORAS (backend/calculators/)

El dispatcher (`dispatcher.py`) detecta el tipo de cálculo por palabras clave y llama a la función correcta.

### Calculadoras SS (`calculos_ss.py` + `calculos_ss_extended.py`):
- IT enfermedad común (tramo 1-3 días, 4-15 días, 16-20 días, 21+ días)
- IT accidente de trabajo (75% base día anterior)
- Incapacidad Permanente Total, Absoluta, Gran Invalidez
- Jubilación ordinaria (DT 7ª — edad 2026)
- Porcentaje pensión (DT 9ª — escala 2026)
- Jubilación anticipada involuntaria (Art. 207)
- Jubilación anticipada voluntaria (Art. 208, check 35 años)
- Viudedad (52%/60%/70%) + Orfandad
- Desempleo (70%/50%, duración)
- IMV (Ingreso Mínimo Vital)
- RETA cotización
- Recargos SS (10%/20%/35%)

### Calculadoras AGE (`calculadora_age.py`):
- Nómina funcionario (trienios, complementos, quinquenios)
- IRPF retenciones
- MUFACE
- Clases pasivas

### Constantes históricas disponibles en dispatcher:
- IPC por año (2010-2026)
- IPREM por año (2010-2026)
- SMI por año (2010-2026)
- BBCC máxima/mínima por año y grupo

---

## 📝 14. ESTADO DEL PIPELINE V13 (CONOCIDO)

### ✅ Funciona bien:
- Generación de casos narrativos complejos (7+ personajes)
- Uso real de calculadoras Python desde el dispatcher
- Búsqueda RAG en Qdrant (colección FULL_XML)
- Deduplicación por hash MD5 (Coherence sieve)
- `mandatory_searches` del investigator (3 búsquedas RAG antes de fact sheet)

### ❌ Problemas conocidos (roadmap V14):
- BOE sieve: solo verifica existencia, no contenido (score siempre positivo)
- Pedagogy sieve: hardcoded `return 1.0`
- Trap-Distractor sieve: hardcoded `return 1.0`
- Interdependence sieve: hardcoded `return 1.0`
- Neo4j VACÍO (solo 6 artículos ejemplo, no poblado)
- `validator.yaml` no se llama en el flujo principal
- El redactor puede no usar las tools si el LLM decide no llamarlas

---

## 🗺️ 15. PLAN V14 ROADMAP (REFERENCIA)

Ver: `/home/spas/OPOS_GEMINI_1/academias/CRITICAS_PLANES/PLAN_impl_V14_ROADMAP_20_03_ANTIGRAVITIcl.md`

| Sprint | Días | Objetivo |
|--------|------|----------|
| **S1** | 3 | Sieves reales (BOE, Pedagogy, Trap, Interdependence) |
| **S2** | 3 | Poblar Neo4j desde Qdrant (artículos + relaciones derogaciones) |
| **S3** | 3 | Extracción trampas de academias (242 archivos en textos_limpios/) |
| **S4** | 1 | `boe_api_client.py` — verify_article_exact() con fecha corte |
| **S5** | 4 | CaseSchemaBuilder V14 + 10 Blueprints + Eval CI 50 preguntas |

**Arquitectura 3 capas de verdad (V14):**
```
Capa 1: Qdrant RAG → búsqueda semántica de contexto (rápido, offline)
Capa 2: BOE API   → verificación de artículo EXACTO (oficial)
Capa 3: Neo4j     → grafo de derogaciones/modificaciones (instantáneo)
```

---

## 🔧 16. COMANDOS DE DIAGNÓSTICO RÁPIDO

```bash
# Estado general del sistema:
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
curl http://localhost:8000/          # Backend OK?
curl http://localhost:6333/          # Qdrant OK?
curl http://localhost:7474/          # Neo4j OK?

# Probar Qdrant RAG:
curl -X POST http://localhost:8000/api/v2/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query": "incapacidad temporal", "limit": 2}'

# Python del venv:
/home/spas/OPOS_GEMINI_1/.venv/bin/python --version

# Paquetes Python instalados:
/home/spas/OPOS_GEMINI_1/.venv/bin/pip list | grep -E "fastapi|uvicorn|qdrant|neo4j"

# Verificar Neo4j desde Python:
/home/spas/OPOS_GEMINI_1/.venv/bin/python -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'opositaia2026'))
with driver.session() as s:
    r = s.run('MATCH (n) RETURN COUNT(n) AS count')
    print('Neo4j nodos:', r.single()['count'])
"

# Verificar Qdrant desde Python:
/home/spas/OPOS_GEMINI_1/.venv/bin/python -c "
from qdrant_client import QdrantClient
c = QdrantClient('http://localhost:6333')
info = c.get_collection('opositaia_knowledge_FULL_XML')
print('Qdrant puntos:', info.points_count)
"

# Ver backend logs en tiempo real:
tail -f /home/spas/OPOS_GEMINI_1/backend/backend.log

# Ver todos los procesos del proyecto:
ps aux | grep -E "uvicorn|node.*mcp|python.*ecosistema"
```

---

## 📋 17. CHECKLIST DE ARRANQUE COMPLETO DEL ENTORNO

```bash
# 1. Verificar Docker containers
docker ps | grep -E "neo4j|qdrant|postgres"
# Si no están: docker-compose up -d qdrant postgres neo4j

# 2. Arrancar backend FastAPI
cd /home/spas/OPOS_GEMINI_1/backend
/home/spas/OPOS_GEMINI_1/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# 3. Verificar backend
curl http://localhost:8000/

# 4. Arrancar frontend (si necesario)
cd /home/spas/OPOS_GEMINI_1/frontend && pnpm dev &

# 5. Verificar frontend
# Abrir http://localhost:5173

# 6. (Opcional) Arrancar MCP Node.js
cd /home/spas/OPOS_GEMINI_1/mcp-server && pnpm start &
```

---

*Documento generado automáticamente el 21/03/2026 por Antigravity AI.*
*Para actualizarlo: revisar Docker, .env.backend y ejecutar los comandos de diagnóstico.*
