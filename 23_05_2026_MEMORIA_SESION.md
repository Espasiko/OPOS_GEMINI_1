---
title: Sesion 23/05/2026 — Wiki + Graphify + Limpieza Git
type: session
domain: meta
tags: [session, graphify, wiki, git, limpieza]
created: 2026-05-23
updated: 2026-05-23
status: active
source: session
related: [[Estado_Mayo_2026]], [[WIKI_INDEX]]
---

# Sesion 23/05/2026 — Wiki + Graphify + Limpieza Git

## Que se hizo

### 1. Git Push de toda la sincronización mayo 2026
- Commit `91a49f1` — 81 archivos: CLAUDE.md, VISION_360, BMAD_EXPLICADO, inventario, memorias sesión, MCP ecosystem, Graphify skill, backend updates, docs actualizados
- Se detectó token GitHub expuesto en `20_05_MCP-S_PROYECTO_IDES.md:46` — redactado antes del push
- **ACCIÓN**: Revocar token `ghp_8nRMx...` en GitHub Settings > Tokens

### 2. Grafo Graphify generado
- **Corpus**: backend/ (134 archivos Python) + frontend/ (65 archivos TS/TSX)
- **Resultado**: 2295 nodos → 2010 nodos limpios, 2938 edges, 164 comunidades Louvain
- **God Nodes**: calculos_ss_extended.py (91), backendService.ts (64), BOEApiClient (42)
- **Outputs**: `graphify-out/graph.json`, `GRAPH_REPORT.md`, `graph.html`
- **Wiki Graphify**: 164 páginas auto-generadas en `/mnt/d/OPOS_PROJECT/01-Wiki/Graphify/`
- **NO se usó Gemini API** — extracción AST pura (0 tokens LLM)
- **Problema PDFs**: `academias/` atascaba el detect → solución: escanear subcarpetas por separado

### 3. Agente Staff actualizado
- Step 2: añadidas fuentes wiki + grafo Graphify con rutas y jerarquía de verdad
- Menú: opciones `[WK]` wiki y `[GR]` grafo Graphify
- Prompts nuevos: `#consultar-wiki` y `#consultar-grafo` con god nodes y comandos

### 4. Limpieza masiva Git — archivos sacados del tracking

#### PDFs (21 archivos — copyright + binarios grandes)
- `backend/data/leyes/LGSS.pdf`
- `conceptual_materials/pdfs/` — 18 esquemas de academia (EasyLeyes, Academia Las Cortes, AENA)
- `docs/APIconsolidada.pdf`, `docs/APIsumarioBOE.pdf`

#### Directorios enteros sacados del tracking
- `conceptual_materials/` — textos extraídos de PDFs + QA generados (era RAG/Qdrant)
- `dataset_generator/` — 125 archivos generadores de datasets (era Salamandra)
- `list_utracked_files/` — lista obsoleta
- `powers/` — power de RAG antiguo
- `INVESTIGACION_MATERIALES_ACADEMIAS_30_03_GEMINI_BMAD.MD` — investigación obsoleta

#### Archivos raíz de análisis/experimentos sacados
- `21_04_NOMBRES_EMPRESAS_FECHAS.md`
- `ANALISIS_CASO_19_BOE.md`
- `ANALISIS_CASO_FEBRERO_BOE.md`
- `analisis_comparativo_casos_DM.md`
- `analisis_final_51_referencias.md`
- `analisis_legislacion_temas.md`
- `ANALISIS_RESULTADOS_FEBRERO_GEMINI_VS_DM.md`
- `ANALISIS_SOFISTICACION_DM_VS_V14.md`
- `caso_23_DM_STYLE.md`
- `CASO_EJEMPLO_1.md`
- `CASOS_TRAMPAS_DM_2026.md`
- `run_generator_v11_silent.py`
- `run_generator_v11_mistral_large.py`
- `verify_v12_legal.py`

#### .gitignore actualizado con reglas nuevas
- `*.pdf` — regla global, ningún PDF se sube
- `list_utracked_files/`
- `powers/`

### 5. Limpieza Graphify — nodos sensibles purgados
- 225 nodos eliminados del grafo:
  - `escritor_configs_backup/` — configs Copilot con nombres de API keys (solo nombres, no valores)
  - `agents/indexar_materiales_academia.py` — AcademyMaterialsIndexer (usa Qdrant descartado)
- Verificado: NO hay valores de API keys en el grafo, solo nombres de campos
- Wiki Graphify regenerada limpia: 164 páginas

## Decisiones tomadas
- PDFs de academia FUERA del repo para siempre (`*.pdf` en .gitignore)
- `conceptual_materials/`, `dataset_generator/`, `powers/` FUERA del repo
- Graphify escanea solo `backend/` y `frontend/` (no raíz, no academias/)
- Extracción Graphify sin LLM (AST puro) es suficiente para el grafo de código

## Pendiente para proxima sesion
- [ ] Commit + push de toda la limpieza
- [ ] Plan detallado agente Durga + sistema `/ * @ #` en BMO
- [ ] Más páginas wiki: Dispatcher_Flow, NEXO_v5_1, Serie_Turca, Muro_Abstraccion
- [ ] Configurar Smart Connections + Bases + Dataview en vault OPOS_PROJECT
- [ ] Revocar token GitHub comprometido `ghp_8nRMx...`
- [ ] Graphify semántico (añadir LLM para docs .md) — fase 2
