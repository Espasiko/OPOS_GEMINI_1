# MCPs del Proyecto OPOS_GEMINI_1 — Inventario Completo
> Fecha: 20/05/2026 | Proyecto: OpositAIA | Autor: Spas + Claude Sonnet 4.6

---

## Resumen ejecutivo

El ecosistema tiene **6 IDEs/clientes** con MCPs configurados, todos corriendo en WSL2 Ubuntu salvo Trae y VS Code que son Windows nativos. El grafo de memoria principal está en `/home/spas/memory.jsonl` (637 líneas, ~38KB de entidades del proyecto).

**Problema detectado:** la memoria está fragmentada en 3 archivos distintos entre IDEs. Ver sección "Problema de Fragmentación".

---

## 1. Claude Code CLI (esta sesión)

**Config:** `/home/spas/.claude/settings.json`  
**CLI path:** `/home/spas/.nvm/versions/node/v24.11.1/bin/claude`  
**Config dir WSL:** `/home/spas/.claude/`  
**Config dir Windows:** `\\wsl.localhost\Ubuntu\home\spas\.claude\`

### MCPs añadidos el 20/05/2026:

| Nombre | Comando | Estado | Para qué sirve |
|--------|---------|--------|----------------|
| **memory** | `node .../server-memory/dist/index.js` | ✅ Añadido | Grafo de conocimiento → `/home/spas/memory.jsonl` |
| **boe** | `/home/spas/.local/bin/mcp-boe` | ✅ Añadido | BOE oficial — buscar leyes y artículos |
| **fetch** | `uvx mcp-server-fetch` | ✅ Añadido | Descargar URLs/páginas web |
| **github** | `docker run ghcr.io/github/github-mcp-server` | ✅ Añadido | Operaciones en GitHub |

**Nota:** Google Drive, Gmail y Calendar (claude.ai) también disponibles vía autenticación OAuth.

---

## 2. Windsurf IDE (WSL2)

**Config:** `/home/spas/.codeium/windsurf/mcp_config.json`

| Nombre | Comando | Estado | Para qué sirve |
|--------|---------|--------|----------------|
| **boe** | `/home/spas/.local/bin/mcp-boe` | ✅ Activo | Búsqueda BOE |
| **fetch** | `uvx mcp-server-fetch` | ✅ Activo | Descargar URLs |
| **github-mcp-server** | `docker run ghcr.io/github/github-mcp-server` | ✅ Activo (parcial) | GitHub (tools de issues/PR desactivadas) |
| **memory** | `node .../server-memory/dist/index.js` | ✅ Activo | Grafo → `/home/spas/memory.jsonl` |
| **kaggle** | `pnpm dlx mcp-remote kaggle.com/mcp` | ❌ Disabled | Kaggle datasets |

**Token GitHub:** `ghp_***REDACTED***` (ver `.env` o GitHub Settings > Tokens)  
**Tools GitHub desactivadas:** add_issue_comment, assign_copilot, get_me, get_tag, get_release_by_tag, get_teams, issue_read/write, list_issues/prs/releases, search_issues/users

---

## 3. Kiro IDE (WSL2, proyecto)

**Config:** `/home/spas/OPOS_GEMINI_1/.kiro/settings/mcp.json`

| Nombre | Comando | Estado | Para qué sirve |
|--------|---------|--------|----------------|
| **opositaia** | `node mcp-server/dist/index.js` | ✅ Configurado | RAG Qdrant + BOE + jurisprudencia OpositAIA |
| **github-mcp-server** | `docker run ghcr.io/github/github-mcp-server` | ✅ Configurado | GitHub |
| **memory** | `pnpm dlx @modelcontextprotocol/server-memory` | ⚠️ Sin MEMORY_FILE_PATH | Grafo — usa ruta por defecto (diferente!) |
| **kaggle** | `pnpm dlx mcp-remote kaggle.com/mcp` | ✅ Sin disabled | Kaggle |

**Config opositaia:**
```
QDRANT_URL: http://localhost:6333
QDRANT_API_KEY: (vacío)
Descripción: Búsqueda RAG, verificación BOE, jurisprudencia
```

**⚠️ ACCIÓN REQUERIDA:** Añadir `MEMORY_FILE_PATH: /home/spas/memory.jsonl` al server `memory`.

---

## 4. Kiro IDE (Windows nativo)

**Config:** `/mnt/c/Users/Usuario/.kiro/settings/mcp.json`

| Nombre | Comando | Estado | Para qué sirve |
|--------|---------|--------|----------------|
| **opositaia** | `wsl -e node /home/spas/OPOS_GEMINI_1/mcp-server/dist/index.js` | ✅ Configurado | MCP OpositAIA via WSL |

**Config opositaia:**
```
QDRANT_URL: https://b554ceb5-2169-4064-9ce7-83c8cd44cf84.europe-west3-0.gcp.cloud.qdrant.io  (⚠️ Cloud GCP — puede expirar)
QDRANT_API_KEY: eyJhbGci... (JWT)
QDRANT_COLLECTION: opositaia_leyes_seguridad_social
HUGGINGFACE_TOKEN: hf_JaHO...
MISTRAL_API_KEY: FpxxgzuL...
```

---

## 5. Gemini Antigravity (WSL2)

**Config:** `/home/spas/.gemini/antigravity/mcp_config.json`

| Nombre | Comando | Estado | Para qué sirve |
|--------|---------|--------|----------------|
| **boe** | `/home/spas/.local/bin/mcp-boe` | ✅ Activo | Búsqueda BOE |
| **github-mcp-server** | `docker run ghcr.io/github/github-mcp-server` | ✅ Activo | GitHub |
| **memory** | `node .../server-memory/dist/index.js` | ✅ Activo | Grafo → `/home/spas/memory.jsonl` |
| **kaggle** | `pnpm dlx mcp-remote kaggle.com/mcp` | ❌ Disabled | Kaggle |

---

## 6. Verdent IDE (WSL2)

**Config:** `/home/spas/.verdent/mcp.json`

| Nombre | Estado |
|--------|--------|
| **github-mcp-server** | ✅ Activo |
| **memory** → `/home/spas/memory.jsonl` | ✅ Activo |
| **kaggle** | ❌ Disabled |

---

## 7. Trae IDE (Windows) — el más completo

**Config:** `/home/spas/.trae-server/data/Machine/mcp.json`

| Nombre | Paquete/Comando | Estado | Para qué sirve |
|--------|-----------------|--------|----------------|
| **Persistent Knowledge Graph** | `@itseasy21/mcp-knowledge-graph` | ✅ Activo | Grafo conocimiento (diferente al memory!) |
| **TaskManager** | `@kazuph/mcp-taskmanager` | ✅ Activo | Gestión de tareas estructuradas |
| **Playwright** | `@executeautomation/playwright-mcp-server` | ✅ Activo | Automatización de browser |
| **File System** | `@bunas/fs-mcp@latest` | ✅ Activo | Acceso al sistema de archivos |
| **Fetch** | `uvx mcp-server-fetch` | ✅ Activo | Descargar URLs |
| **Qdrant Server** | `uvx mcp-server-qdrant` | ✅ Activo | Vector DB local:6333, colección `opositor_lgss` |
| **DeepView** | `deepview-mcp` | ✅ Activo | Análisis profundo de código con Gemini |
| **File Context Server** | `file-context-server` | ✅ Activo | Caché inteligente de archivos (TTL 1h) |
| **Memory** | `@modelcontextprotocol/server-memory` | ✅ Activo | Grafo → `memory.json` (⚠️ diferente!) |
| **mcp-flowise** | `git+https://github.com/matthewhand/mcp-flowise` | ✅ Activo | Workflows Flowise AI |
| **context7** | `@upstash/context7-mcp@latest` | ✅ Activo | Documentación de librerías en contexto |
| **GitHub** | `@modelcontextprotocol/server-github` | ✅ Activo | GitHub |
| **Postgrest** | `@modelcontextprotocol/server-postgres` | ✅ Activo | PostgreSQL → odoo DB local:5432 |
| **HuggingFace Spaces** | `@llmindset/mcp-hfspace` | ⚠️ Sin tokens | HuggingFace modelos y espacios |
| **n8n-mcp** | `npx n8n-mcp` | ❌ Disabled | Workflows n8n |
| **YouTube Transcript** | `@sinco-lab/mcp-youtube-transcript` | ❌ Disabled | Transcripciones YouTube |
| **Docker** | `uvx docker-mcp` | ❌ Disabled | Control de Docker |
| **Excel** | `@negokaz/excel-mcp-server` | ❌ Disabled | Leer/escribir Excel |
| **YouTube Data** | `youtube-data-mcp-server` | ❌ Disabled | YouTube Data API |
| **Odoo** | `python3 /home/spas/odoofinal/.../mcp_standalone.py` | ❌ Disabled | API Odoo FastAPI |

**Qdrant config:**
```
COLLECTION_NAME: opositor_lgss
EMBEDDING_MODEL: Qwen/Qwen3-Embedding-0.6B
EMBEDDING_PROVIDER: fastembed
QDRANT_URL: http://localhost:6333
```

**Flowise config:**
```
FLOWISE_API_KEY: u-bbYInwpdloVE0ZIScZ6rgJn2ScJLEh0Rbu6sF97v0
FLOWISE_API_ENDPOINT: http://172.19.0.2:3000
```

---

## 8. VS Code (Windows)

**Config:** `/mnt/c/Users/Usuario/AppData/Roaming/Code/User/mcp.json`

| Nombre | Tipo | Estado | Para qué sirve |
|--------|------|--------|----------------|
| **HuggingFace** | HTTP → `https://hf.co/mcp` | ✅ Activo | HuggingFace models/datasets |
| **markitdown** | `uvx markitdown-mcp` | ✅ Activo | Convertir docs a Markdown |
| **imagesorcery** | `uvx imagesorcery-mcp` | ✅ Activo | Procesamiento de imágenes |
| **deepwiki** | HTTP → `https://mcp.deepwiki.com/sse` | ✅ Activo | Documentación técnica profunda |
| **GitHub Copilot** | HTTP → `https://api.githubcopilot.com/mcp/` | ✅ Activo | GitHub Copilot AI |
| **convex** | `npx convex@latest mcp start` | ✅ Activo | Backend Convex |
| **Vercel** | HTTP → `https://mcp.vercel.com` | ✅ Activo | Deploy Vercel |
| **oraios/serena** | `uvx serena start-mcp-server` | ✅ Activo | IDE assistant contextual |

---

## 9. Grafo de Memoria MCP — Estado actual

**Archivo principal:** `/home/spas/memory.jsonl`  
**Tamaño:** 637 líneas, ~38KB  
**Formato:** JSONL — una entidad/relación por línea

### Entidades principales en el grafo (20/05/2026):

| Entidad | Tipo | Info clave |
|---------|------|-----------|
| **OpositAIA** | Project | 108 leyes, 6683 preceptos, 379 excepciones, 517 comunidades Louvain |
| **Backend_FastAPI** | Architecture | 2457 líneas calculos_ss_extended.py, 8 bugs resueltos 29/04 |
| **Neo4jService** | Infrastructure | bolt://localhost:7687, usuario neo4j, pass opositaia2026. bolt://localhost:7688 (puerto alternativo) |
| **Qdrant_FULL_XML** | VectorDatabase | DESCARTADO — Neo4j 2026 tiene HNSW nativo |
| **CalculatorEngine_SS** | Module | 31 funciones SS verificadas contra BOE 04/03/2026 |
| **CalculatorEngine_AGE** | Module | 34 funciones AGE (LPAC + TREBEP + Transversales) |
| **OposAgents_Subsystem** | Architecture | BMO → Mistral → Chandra → Neo4j |
| **WSL_Global_Dependencies** | Infrastructure | Node v20+, pnpm, Python 3.12 |
| **LLM_Providers_Config** | Infrastructure | Mistral, Groq, DeepSeek, Claude, Gemini, OpenAI, Salamandra |
| **Estrategia_COSMIC** | Strategy | Create Once Serve Many, 4 cuerpos, 54,000 preguntas |

### Cómo leer/escribir el grafo desde Claude Code:
- **LEER:** `cat /home/spas/memory.jsonl` o via herramienta MCP `memory` (ahora conectada)
- **ESCRIBIR via MCP:** Usando las herramientas `create_entities`, `create_relations`, `search_nodes` del servidor memory (activo en esta sesión tras la configuración del 20/05/2026)
- **ESCRIBIR directo:** Añadir líneas JSONL al archivo (menos recomendado — puede perder coherencia del grafo)

---

## Problema crítico: Fragmentación de memoria

Los IDEs usan **3 archivos diferentes** como grafo de memoria:

| IDEs | Archivo | Estado |
|------|---------|--------|
| Claude Code, Windsurf, Verdent, Gemini Antigravity | `/home/spas/memory.jsonl` | ✅ FUENTE DE VERDAD (637 líneas) |
| Kiro (WSL, proyecto) | Sin path → default del proceso | ❌ Fragmentado |
| Trae (Windows) | `memory.json` (relativo) | ❌ Archivo diferente |

**Solución:** Unificar todos a `/home/spas/memory.jsonl`:

Para Kiro (WSL, `/home/spas/OPOS_GEMINI_1/.kiro/settings/mcp.json`):
```json
"memory": {
  "command": "pnpm",
  "args": ["dlx", "@modelcontextprotocol/server-memory"],
  "env": { "MEMORY_FILE_PATH": "/home/spas/memory.jsonl" }
}
```

Para Trae (Windows, `/home/spas/.trae-server/data/Machine/mcp.json`):
```json
"Memory": {
  "env": { "MEMORY_FILE_PATH": "//wsl.localhost/Ubuntu/home/spas/memory.jsonl" }
}
```

---

## Plugins Obsidian activos

**Vault:** `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/`  
**Bridge WSL:** REST API en puerto 27123 (HTTP, sin SSL)  
**API Key:** `097befc68922b9c32d6388ebbb871e127c5c9037af91a83813107e5e1e60699d`  
**Red:** portproxy `172.26.240.1:27123 → 127.0.0.1:27123`

| Plugin | Estado | Para qué sirve |
|--------|--------|----------------|
| **Copilot** | ✅ Activo | Chat IA con Ollama/Mistral local dentro de Obsidian |
| **Dataview** | ✅ Activo | Queries SQL-like sobre notas del vault |
| **mcp-tools** | ✅ Activo | Herramientas MCP accesibles desde el vault |
| **obsidian-local-rest-api** | ✅ Activo | Expone vault por HTTP:27123 para acceso externo |
| **obsidian-git** | ✅ Activo | Versionado git del vault |
| **obsidian-mind-map** | ✅ Activo | Generar mapas mentales desde notas |
| **Smart Connections** | ✅ Activado 24/04 | Búsqueda semántica local sin listar vault entero |
| **Smart Context** | ⚠️ Inactivo | Contexto inteligente para IA |
| **Smart Lookup** | ⚠️ Inactivo | Búsqueda mejorada |
| **BMO Chatbot** | ⚠️ Inactivo | Chatbot alternativo |
| **Remotely Save** | ⚠️ Inactivo | Sincronización remota |
| **Smart ChatGPT** | ⚠️ Inactivo | Integración ChatGPT |

**Endpoints REST API Obsidian:**
```
POST http://172.26.240.1:27123/vault/search    → buscar en vault
GET  http://172.26.240.1:27123/vault/read      → leer nota
POST http://172.26.240.1:27123/vault/write     → escribir nota
GET  http://172.26.240.1:27123/vault/health    → verificar estado
```
Añadir header: `Authorization: Bearer 097befc68922b9c32d6388ebbb871e127c5c9037af91a83813107e5e1e60699d`

---

## Resumen: qué MCP usar para qué tarea

| Necesito... | Usar este MCP | En qué IDE |
|-------------|---------------|-----------|
| Buscar una ley del BOE | **boe** | Claude Code, Windsurf, Gemini |
| Recordar info del proyecto | **memory** | Todos (unificar!) |
| Ver estado de GitHub | **github** | Claude Code, Windsurf |
| Buscar en el vault Obsidian | REST API local:27123 | Backend endpoint `/mcp/vault/search` |
| Buscar vectores en Qdrant | **Qdrant Server** | Trae |
| Analizar código profundo | **DeepView** | Trae |
| Documentación de librerías | **context7** | Trae |
| Descargar páginas web | **fetch** | Claude Code, Windsurf, Trae |
| Operaciones RAG OpositAIA | **opositaia** | Kiro (WSL o Windows) |

---

*Generado el 20/05/2026 — Actualizar cuando se añadan nuevos MCPs o cambien configuraciones*
