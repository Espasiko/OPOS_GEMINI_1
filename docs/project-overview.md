# OpositAIA — Project Overview (Brownfield Documentation)

> **Generado:** 03/03/2026 · **Addendum:** 19/05/2026 | **Workflow:** BMAD document-project v1.2.0 | **Scan Level:** Reconciliado (100% Real) · Revisión 19/05 Graph Intelligence

---

> ## 🔄 ADDENDUM 19/05/2026 — Graph Intelligence
>
> ### Neo4j — Estado real 19/05/2026
> - **108 leyes, 6.683 preceptos, 6.683 embeddings** (catálogo v17.6)
> - **Louvain Community Detection:** 517 comunidades calculadas (Python networkx+louvain). Prop `communityId` en cada Precepto.
> - **Búsqueda híbrida nativa:** Vector HNSW 1024d + Fulltext spanish + Cypher graph traversal. Qdrant NO necesario.
> - **Multi-hop reasoning:** `consultar_neo4j` de Chandra ejecuta queries multi-relación.
> - **RD 1413/2005** (capitalización desempleo) ingestado: 4 preceptos + relaciones Art. 262/296 TRLGSS.
> - **Docker Compose:** 4 servicios (Qdrant + Postgres + Backend + Neo4j). Ollama corre directo en WSL.
>
> ### Correcciones al overview
> - **BMO SÍ conecta a Neo4j** vía Chandra mano #4. Cadena: BMO → Mistral API → :8080 → Chandra → Neo4j.
> - **Bóveda OPOS** = `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/` (vault pruebas). OPOS_GEMINI_1 = repo de desarrollo.
> - **PII** = materiales de academias (copyright/nombres), NO leyes públicas.
> - **Contadores corregidos:** Ley→108, Precepto→6683 (era 4742 en addendum 01/05).
>
> ---
>
> ## 🔄 ADDENDUM 01/05/2026 — Chandra 7 Manos + Obsidian Integration
>
> ### Chandra Agente Legal (NUEVO — no estaba en este overview)
>
> - **Chandra es un agente legal de 7 herramientas** integrado en Obsidian vía BMO/Copilot
> - **7 herramientas:** tavily_search, search_boe, get_law_text_block, consultar_neo4j, calcular_ss, buscar_vault, **escribir_vault** (NUEVA 01/05/2026)
> - **Archivo modificado:** `backend/agents/chandra_tools.py` — Schema + implementación + dispatcher actualizados
> - **Solución de red:** Backend movido a puerto 8080 para evitar ERR_CONNECTION_REFUSED en Windows/WSL2
> - **Alucinación temporal resuelta:** Inyección dinámica de fecha actual en system prompt (datetime.now())
> - **Integración Obsidian:** BMO Chatbot y Copilot conectados a Chandra vía http://127.0.0.1:8080/opos/v1
> - **Tool escribir_vault (01/05/2026):** Chandra puede crear notas automáticamente en el vault sin copiar/pegar manual
> - **Backend endpoint:** `/mcp/vault/write` ya existía en `mcp_gateway.py` (implementado 24/04/2026)
>
> ### LiteLLM Fallback Multi-Cloud (NUEVO — de implementation_plan.md.resolved)
>
> - **Resiliencia anti-bloqueos:** LiteLLM permite fallback automático entre Mistral → Gemini → Groq
> - **Groq modelos disponibles:** GPT OSS 120B, GPT OSS 20B, Llama 4 Scout, Qwen 3 32B (function calling + reasoning)
> - **Batch API Groq:** 50% descuento para procesamiento masivo (54K preguntas banco)
>
> ### Tauri Desktop App (NUEVO — de IDEAS_MAESTRAS_OPOSITAIA_2026.md.resolved)
>
> - **Empaquetado:** Frontend React + Backend Python (chandra.exe) usando Tauri + Sidecar
> - **BYOV (Bring Your Own Vault):** App distribuye limpia, usuario instala Obsidian + Vault ZIP por separado
>
> ### Componentes NUEVOS no documentados aquí (17/04/2026)
>
> - **V14.5 "Narrativa en Red"** (`/backend/v14/`): `CaseSchemaBuilder` (28.5KB), `prose_validator.py` (10KB), `cambios_dm_2026.py` (13KB), `nombres_pool.py` (4.8KB), 10 blueprints activos S02-S16 en `/backend/v14/blueprints/`.
> - **Agentes YAML (11)** en `/opos-agents/agents/`: orchestrator, generator, examiner, redactor_v13, redactor_v14, investigator_v13, intent, compile, resumidor, validator, generator_r1.
> - **mcp_gateway.py** (`/backend/routers/mcp_gateway.py`, 9.4KB) — gateway REST multi-IA (formatos Claude/OpenAI/Mistral).
> - **Constantes 2026** (`/backend/calculators/constantes_2026.py`, 6KB) — SMI, IPREM, topes, pensiones actualizados.
> - **Catálogo trampas** (`catalogo_trampas.yaml` + `catalogo_trampas_adicional.yaml`) — ~100 trampas A-T.
> - **Temario 2026 troceado** (`/academias/.../temario_troceado_v2026/`) — 13 temas con correcciones Marzo.
> - **Calculadora presupuesto** (`calculadora_presupuesto.py`, 18.6KB) — NO mencionada en §4.2.
>
> ### Contadores corregidos
>
> | Valor en este doc | Valor real Abril 2026 |
> |---|---|
> | Qdrant Cloud 48.866 chunks | ❌ Qdrant descartado. Neo4j: 4.742 preceptos + 6.334 embeddings |
> | 31 calculadoras SS + 33 AGE = 64 | **60+ reales confirmadas por grep** (calculos_ss_extended 30+ funciones, calculadora_age 30+ funciones) |
> | 25 agentes backend | **27 archivos en `/backend/agents/`** (diff = 2 nuevos) |
> | Salamandra R1 operativo | ❌ **Descartado** en producción |
> | 9 routers | Ya 10 (añadido `casos_practicos`) |
> | 6 MCP tools | 5 (`list_collections` opcional) |
>
> ### Trampas codificadas en docstrings (descubrimiento Abril)
>
> Las funciones de `calculos_ss_extended.py` **tienen las trampas DM documentadas inline**:
> - `calcular_derivacion_responsabilidad_ss` → TRAMPA G4
> - `calcular_fecha_efectos_cambio_base_reta` → TRAMPA H7
> - `calcular_cuota_contrato_corta_duracion` → TRAMPA I12
> - `calcular_base_cotizacion_completa` → trampa "estructurales ≠ fuerza mayor"
>
> Estas pueden extraerse automáticamente por parsing AST para alimentar la wiki Obsidian.
>
> ### Bugs corregidos (no reflejados antes)
>
> - `PENSION_MAXIMA_JUBILACION_2026` = **3.359,60 €/mes** (14 pagas) — era incorrecto 3.175,04 €
> - `SMI_2026` = **1.221,00 €** (RD 126/2026) — era 1.184,00 €
> - `Art. IT menstruación` = **Art. 173** (no 173bis) — pendiente en docs legales
>
> ### Docs estratégicos nuevos (imprescindibles para sesiones futuras)
>
> 1. **`/17_04_26_ESTRATEGIA_EXTRACCION_SABIDURIA.md`** — pipeline 5 fases, 9 patrones DM, cómo la wiki recuerda
> 2. **`/academias/1_casos_recientes_2026_DM/temario_troceado/PLAN_CLD+_OBCIDIAN_AL.md` v3** — plan Obsidian (arquitectura, plugins, skills)
> 3. **`/academias/1_casos_recientes_2026_DM/PLAN_MAESTRO_CASOS_SIMULACROS.md` v4** — 1157 líneas, 8K-10K preguntas objetivo
> 4. **`/ANALISIS_SOFISTICACION_DM_VS_V14.md`** — gap V14 vs DM real (personajes, salto régimen)
>
> ### Gaps pendientes para el roadmap
>
> - **TREBEP, LPAC, LRJSP, LCSP** infrarrepresentados en banco de preguntas
> - **V14.5**: necesita red de 3-8 personajes (hoy solo 1) y saltos de régimen
> - **149 archivos sueltos en raíz** → candidatos para limpieza o absorción por la wiki
> - **Settings BYOK**: `SettingsView.tsx` sigue como placeholder (confirmado §3.1 fila 14)

---

## 1. Qué es OpositAIA

**Sistema de IA multi-agente para preparación de oposiciones** (Seguridad Social y AGE España). Combina:

- **RAG legal** sobre normas BOE con embeddings especializados (`pablosi/bge-m3-spa-law-qa-trained-2`)
- **Calculadoras determinísticas** para 64 tipos (33 AGE + 31 SS/IMV)
- **Generación IA** de exámenes, mapas mentales, flashcards, esquemas, resúmenes, casos prácticos
- **Chat IA** multi-proveedor (7 APIs: Groq, DeepSeek, Gemini, Mistral, Claude, OpenAI, Ollama)
- **Tracking de progreso** del usuario con análisis de temas débiles
- **Golden Datasets** curados para training y validación

**Estrategia:** COSMIC (Create Once, Serve Many) — contenido etiquetado una vez, servido filtrado a 4 cuerpos de oposiciones.

---

## 2. Arquitectura del Repositorio

| Aspecto | Detalle |
|---------|---------|
| **Tipo** | Multi-part (monorepo) |
| **Partes** | 4: Backend, Frontend, MCP Server, Agent Definitions |
| **Lenguajes** | Python 3.12, TypeScript 5.8 |
| **Infra** | Docker Compose (Qdrant + Postgres + Backend) |

---

## 3. Frontend — Entregables y Vistas (17 vistas)

Ruta: `/frontend/` | Stack: Vite 6.2 + React 19 + TypeScript 5.8 + TailwindCSS

### 3.1 Vistas activas en App.tsx

| # | Vista | Archivo | Descripción | Estado |
|---|-------|---------|-------------|--------|
| 1 | **Chat IA** | `ChatView.tsx` | Chat con RAG + multi-proveedor | ✅ Operativo |
| 2 | **Casos Prácticos** | `CaseGeneratorView.tsx` | Genera casos + preguntas MCQ, guarda progreso | ✅ Operativo |
| 3 | **Búsqueda RAG** | `SearchGroundingView.tsx` | Búsqueda con fuentes BOE + grounding | ✅ Operativo |
| 4 | **Temario** | `SyllabusView.tsx` | Navegación del temario oficial | ✅ Operativo |
| 5 | **Mapas Mentales** | `MindMapView.tsx` | Genera mapas mentales, exporta JSON/MD/PNG | ✅ Operativo |
| 6 | **Esquemas** | `SchemaView.tsx` | Genera esquemas jerárquicos de temas | ✅ Operativo |
| 7 | **Resúmenes** | `SummaryView.tsx` | Genera resúmenes con puntos clave | ✅ Operativo |
| 8 | **Comparador** | `ComparatorView.tsx` | Compara dos textos legales (similitudes/diffs) | ✅ Operativo |
| 9 | **Plan de Estudio** | `StudyPlanView.tsx` | Genera planes semanales personalizados | ✅ Operativo |
| 10 | **Simulacros** | `MockExamView.tsx` | Exámenes tipo test con timer, selecciona temas | ✅ Operativo |
| 11 | **Flashcards** | `FlashcardsView.tsx` | Tarjetas de memoria con flip 3D | ✅ Operativo |
| 12 | **Mi Progreso** | `ProgressView.tsx` | Dashboard: aciertos/fallos, % éxito, filtros 7d/30d | ✅ Operativo |
| 13 | **Guía de Usuario** | `UserGuideView.tsx` | Ayuda y documentación in-app | ✅ Operativo |
| 14 | **Configuración** | `SettingsView.tsx` | API keys BYOK + modelo negocio Freemium | ⚠️ Solo UI placeholder |
| 15 | **Selector Modelo** | `ModelSelector.tsx` | Cambia entre Gemini, GPT-4, Groq, etc. | ✅ Operativo |
| 16 | **Test VPS** | `VPSTestView.tsx` | Diagnóstico conexión VPS/Salamandra | 🔧 Debug |
| 17 | **Test Backend** | `BackendTestView.tsx` | Diagnóstico conexión backend | 🔧 Debug |

### 3.2 Estado persistido (localStorage)

El `App.tsx` usa `usePersistentState` para guardar entre sesiones:
- `selectedModel` — modelo IA actual
- `caseGenerator_currentCase` + `caseGenerator_caseAnswers` — caso práctico en curso
- `progressTracker_data` — historial de respuestas
- `mindMap_lastState` — último mapa mental
- `schema_lastState` — último esquema
- `summary_lastState` — último resumen
- `comparator_lastResult` — última comparación

### 3.3 Servicios y Utils

| Archivo | Función |
|---------|---------|
| `services/backendService.ts` (757 líneas) | 12+ funciones API: `sendChatMessage`, `generatePracticalCase`, `generateMindMap`, `generateFlashcards`, `generateSchema`, `generateSummary`, `compareLegalTexts`, `generateStudyPlan`, `generateMockExam`, `uploadFile`, `uploadUrl`, `healthCheck` |
| `services/vpsService.ts` | Conexión VPS/Salamandra |
| `hooks/useAIProvider.ts` | Hook multi-proveedor con retry automático |
| `contexts/ModelContext.tsx` | Context global del modelo seleccionado |
| `utils/providers.ts` | Configuración de proveedores IA |
| `utils/formatters.ts` | Formateo y validación de respuestas |
| `utils/cache.ts` | Caché local de resultados |

### 3.4 Types (types.ts)

```
AppView (enum): 17 vistas
ChatMessage, Conversation
PracticalCase, PracticalCaseQuestion, PracticalCaseOption, CaseAnswer
GroundingSource
MindMapNode (recursivo)
StudyPlanInput
MockExam
Flashcard
```

### 3.5 Dependencias clave

| Dep | Uso |
|-----|-----|
| `@excalidraw/excalidraw` | Mapas mentales / diagramas interactivos |
| `@google/genai` | Gemini API desde cliente |
| `html-to-image` | Exportar mapas mentales a PNG |
| `vite-plugin-pwa` | PWA offline support |
| `vitest` + `@testing-library` | Testing unitario |

---

## 4. Backend — APIs y Agentes

### 4.1 Routers API (9)

| Router | Archivo | KB | Descripción |
|--------|---------|-----|-------------|
| `rag` | rag.py | 4.8 | RAG v1 (legacy) |
| `rag_v2` | rag_v2.py | 6.2 | RAG v2 (RoBERTalex + 2 capas) |
| `chat` | chat.py | 13.6 | Chat con Mistral + RAG contextual |
| `upload` | upload.py | 8.0 | Subida PDF/DOCX/URL → indexación |
| `ai_functions` | ai_functions.py | 18.4 | **Funciones IA multi-proveedor** (mapas mentales, casos, flashcards, esquemas, resúmenes, comparación, plan estudio, simulacros) |
| `user` | user.py | 9.8 | Gestión usuarios y progreso |
| `boe` | boe.py | 10.9 | API oficial datos abiertos BOE |
| `mcp_gateway` | mcp_gateway.py | 9.4 | Gateway MCP para acceso desde otras IAs |
| `casos_practicos` | casos_practicos.py | 3.2 | Casos prácticos con Salamandra R1 |

### 4.2 Calculadoras (Módulo Crítico)

| Archivo | KB | Contenido |
|---------|-----|-----------|
| `calculos_ss.py` | 4.6 | Calculadoras SS básicas |
| `calculos_ss_extended.py` | 49.6 | **27+ calculadoras extendidas** |
| `calculos_imv.py` | 10.9 | Calculadora IMV completa |
| `dispatcher.py` | 4.1 | Router query → calculadora |
| **Total SS/IMV** | | **31 implementadas** |
| **Total AGE** | | **33 implementadas** |

### 4.3 Agentes IA (25 archivos)

| Archivo | KB | Rol |
|---------|-----|-----|
| `llm_providers.py` | 22.6 | 7 proveedores LLM configurados |
| `verification_agents.py` | 40.5 | Validación anti-alucinación 3 tiers |
| `mistral_tools.py` | 39.4 | Tools Mistral (OCR, cálculos, search) |
| `rag_agent_v2.py` | 15.8 | Agente RAG v2 con reranking Cohere |
| `boe_api_client.py` | 12.0 | Cliente API BOE datos abiertos |
| `orchestrator.py` | 12.6 | Orquestador multi-agente |
| `confidence_scorer.py` | 6.0 | Scoring de confianza respuestas |
| `query_validator.py` | 11.2 | Validación queries usuario |
| `reasoning_tracer.py` | 11.2 | Trazabilidad razonamiento |
| `salamandra_client.py` | 7.9 | Cliente Salamandra R1 local |
| `salamandra_memory.py` | 7.4 | Memoria contextual Salamandra |
| `generate_salamandra.py` | 6.5 | Generación contenido con Salamandra |
| `indexer.py` | 5.0 | Indexador vectorial Qdrant |
| `ingest_hybrid_two_tier.py` | 15.2 | Ingesta híbrida dense+BM25 |
| `mel_client.py` | 7.1 | Cliente Mistral Embeddings Legal |
| `setup_semantic_cache.py` | 5.7 | Caché semántico |

---

## 5. Base de Datos PostgreSQL (8 tablas)

Ruta: `/backend/database/schema.sql` (377 líneas)

| # | Tabla | Registra |
|---|-------|----------|
| 1 | `user_progress` | Usuarios: métricas globales, rachas, temas débiles |
| 2 | `answer_history` | Cada respuesta: pregunta, correcta/no, tiempo, intentos |
| 3 | `user_cases` | Casos prácticos creados por usuarios (público/privado) |
| 4 | `simulacros` | Resultados de simulacros: puntuación, temas, detalle JSONB |
| 5 | `mind_maps` | Mapas mentales guardados (contenido JSONB) |
| 6 | `study_sessions` | Sesiones de estudio: duración, preguntas, temas |
| 7 | `recommendations` | Recomendaciones IA personalizadas (prioridad, expiración) |
| 8 | `rag_queries` | Queries RAG logueadas para análisis (embedding VECTOR(1024)) |

**Views:** `user_performance_by_topic`, `user_weak_topics`, `user_study_streaks`
**Triggers:** Auto-update `user_progress` tras cada respuesta
**Functions:** `calculate_weak_topics()`, `update_weak_topics()`

---

## 6. MCP Server (6 tools)

Ruta: `/mcp-server/src/index.ts` (278 líneas) | Stack: Node.js + TypeScript

| Tool | Descripción |
|------|-------------|
| `search_rag` | Busca en la base de conocimiento legal (Qdrant) |
| `verify_boe` | Verifica disposiciones en el BOE |
| `search_jurisprudence` | Busca sentencias del Tribunal Supremo/TSJ |
| `get_law_summary` | Obtiene resumen de una ley por ID |
| `ingest_new_law` | Ingesta nueva ley al sistema |
| `list_collections` | Lista colecciones disponibles en Qdrant |

**Embeddings:** Modelo `pablosi/bge-m3-spa-law-qa-trained-2` (HuggingFace, 1024 dims) o fallback Mistral.

---

## 7. Golden Datasets y Datos de Entrenamiento

### 7.1 Golden Dataset (`/golden_dataset/` — 42 archivos)

| Carpeta | Archivos | Contenido |
|---------|----------|-----------|
| `consolidated/` | 5 | Datasets consolidados (cleaned, enriched, final training) |
| `premium/` | 11 | 30 casos premium, QA por proveedor (Gemini, Groq), razonamiento legal, comparativas, simulacros |
| `premium_final/` | 5 | Casos DeepSeek R1, Gemini premium manual |
| `special/` | 6 | Legacy: cases, dialogues, flashcards, QA extra, RAG context |
| `standard/` | 5 | DeepSeek extreme/premium, Groq 500 verified, Mistral consolidated |
| `enriched/` | 1 | Exámenes oficiales enriquecidos con Mistral |

### 7.2 Dataset Generator (`/dataset_generator/` — 102+ archivos)

- **MASTER_DATASET** versiones v4 → v9 (6 iteraciones)
- **Scripts:** `analyze_coverage.py`, `analyze_duplicates.py`, `consolidar_dataset_final.py`, `export_dataset.py`
- **Agente simulacro:** `agents/simulacro_agent/` (agente completo con MCP client)
- **Archives:** Legacy output, Groq batch, Mistral batch

### 7.3 Datasets en Raíz

| Archivo | KB | Contenido |
|---------|-----|-----------|
| `MASTER_DATASET_v11_UTF8_FIXED.jsonl` | 1,778 | Dataset master v11 |
| `MASTER_DATASET_v12_PLATINUM.jsonl` | 1,918 | Dataset master v12 (último) |
| `gran-basurero.jsonl` | 52,077 | Todos los datos raw sin filtrar |

### 7.4 Exámenes Golden Generados

`/EXAMENES_GENERADOS/` — 5 exámenes golden (22/02/2026)

### 7.5 Staging Area (`/staging_area/`)

- `05_01_26_exams_processing/` — Pipeline de procesamiento de exámenes oficiales (OCR, pairing, validación)
- `06_01_26_enrichment/` — Enriquecimiento multi-modelo (Claude, DeepSeek, Groq, Salamandra)

---

## 8. Materiales Conceptuales

Ruta: `/conceptual_materials/`

| Tipo | Cantidad | Contenido |
|------|----------|-----------|
| PDFs | 20 | Esquemas: AAPPEE, CE, UE, Gobierno, Entidades Locales, CGPJ, PAC, LCSP, Plazos, Decretos, SS, Ley 3/2007 |
| Textos extraídos | 17 | Versiones texto de los PDFs |
| QA generados | 11 | `conceptual_qa_100.jsonl`, versiones CLEAN/FINAL/IMPROVED/REVIEWED |

---

## 9. Estado Implementación vs Diseño

| Componente | Impl. | Diseñado | Estado |
|-----------|:-----:|:--------:|--------|
| Backend FastAPI (9 routers) | ✅ | ✅ | Operativo |
| endpoint `/ai/generate` (mapas, casos, flash, esquemas, resúmenes, comparador, plan, simulacro) | ✅ | ✅ | Operativo vía `ai_functions.py` |
| RAG v2 (Qdrant + RoBERTalex + Cohere rerank) | ✅ | ✅ | Operativo |
| Calculadoras SS (31) | ✅ | ✅ | Operativo |
| Calculadoras AGE (33) | ✅ | ✅ | Operativo en `backend/calculators/` |
| Frontend React (17 vistas) | ✅ | ✅ | La mayoría operativas |
| **Mapas Mentales** (Excalidraw + export) | ✅ | ✅ | Operativo, exporta JSON/MD/PNG |
| **Casos Prácticos** (generador + MCQ) | ✅ | ✅ | Operativo multi-proveedor |
| **Flashcards** (flip 3D) | ✅ | ✅ | Operativo |
| **Simulacros** (timer + temas) | ✅ | ✅ | Operativo |
| **Progress Tracking** (filtros temporales) | ✅ | ✅ | Operativo (localStorage) |
| **Settings/Config** page | ⚠️ | ✅ | Solo UI placeholder, BYOK disabled |
| Docker Compose | ✅ | ✅ | Qdrant + PG + Backend + Neo4j |
| MCP Server (6 tools) | ✅ | ✅ | Operativo |
| Qdrant Cloud | ✅ | ✅ | 48,866 chunks + 54 leyes |
| Qdrant Local Híbrido | ✅ | ✅ | 1,272 chunks (Dense + BM25) |
| PostgreSQL Schema (8 tablas) | ✅ | ✅ | Schema completo, triggers + views |
| Golden Datasets | ✅ | ✅ | v12 + premium + enriched |
| Sistema Multi-Agente BMAD bridge | ✅ | ✅ | BMAD V6 Integrado |
| Pipeline COSMIC integrado | ✅ | ✅ | Scripts operativos |
| Neo4j (grafos) | ✅ | ✅ | 108 leyes, 6683 preceptos, Louvain 517 comunidades |
| Auth (Clerk/Lucia) | ❌ | ✅ | Pendiente decisión |
| Stripe (pagos) | ❌ | ✅ | Pendiente |
| Repetición espaciada Leitner | ❌ | ✅ | Algoritmo diseñado, no implementado |
| Persistencia servidor (DB en vez de localStorage) | ❌ | ✅ | Frontend usa localStorage, DB ready |

---

## 10. Deuda Técnica

> [!WARNING]
> **149 archivos sueltos en la raíz** del proyecto. Plan de limpieza en `PLAN_LIMPIEZA_RAIZ.txt`.

- **Scripts duplicados:** 4× `generar_parte2_*.py`, 8× `test_salamandra_*.py`
- **Logs en raíz:** `groq_gen.log`, `qa_*.log`, `backend.log` (10MB)
- **Datasets en raíz:** `gran-basurero.jsonl` (52MB), 2× `MASTER_DATASET_v1*.jsonl`
- **Virtualenvs múltiples:** `.venv`, `.venv_conversion`, `.venv_cpu`, `.venv_kaggle`
- **Frontend usa localStorage:** DB PostgreSQL tiene schema completo pero frontend no lo utiliza
- **Settings page:** UI placeholder sin funcionalidad real
- **Exámenes JSON sueltos:** 6× `SUPUESTO_*.json` en raíz

---

## 11. Documentos de Referencia (con estado de vigencia)

### 🟢 Fuentes de la Verdad (vigentes)

| Documento | Fecha | KB | Estado |
|-----------|-------|-----|--------|
| **Síntesis Plan Definitivo** (`/28_02_2026_SINTESIS_PLAN_DEFINITIVO.md`) | 28/02/2026 | 14 | ✅ **Vigente** — Fuente de verdad |
| Auditoría Completa (`/27_02_2026_AUDITORIA_TODO.md`) | 27/02/2026 | 24 | ✅ **Vigente** — 10 secciones |

### 🟡 Arquitectura y Planes (parcialmente obsoletos)

| Documento | Fecha | KB | Estado |
|-----------|-------|-----|--------|
| Arquitectura Actual (`/ARQUITECTURA_ACTUAL_11_02_26.md`) | 12/02/2026 | 39 | ⚠️ Anterior a síntesis |
| Plan Desarrollo 2026 (`/PLAN_DESARROLLO_2026.md`) | 09/01/2026 | 50 | ⚠️ Pre-COSMIC |
| Resumen Ejecutivo (`/RESUMEN_EJECUTIVO_5_MINUTOS.md`) | 13/02/2026 | 10 | ⚠️ No tiene últimas decisiones |

### 📘 READMEs

| Documento | Fecha | KB | Estado |
|-----------|-------|-----|--------|
| README proyecto | 05/02/2026 | 7 | ⚠️ Actualizar |
| Backend README | 09/12/2025 | 8 | 📦 Legacy (pre-sprint 9) |
| MCP Server README | 09/12/2025 | 2 | 📦 Legacy (no refleja 6 tools) |

### 📂 Plan Definitivo — Claude (`docs/PLAN_DEFINITIVO_MD/`)

9 documentos del plan estratégico original. **Imprescindibles para contrastar decisiones.**

| # | Archivo | Contenido |
|---|---------|-----------|
| 1 | `plan_app_oposiciones_cosmic.md` | **Plan maestro** — Estrategia COSMIC, modelo negocio, roadmap |
| 2 | `apendice_II_tecnico_actualizado.md` | Stack técnico, decisiones arquitectura |
| 3 | `apendice_III_actualizacion_tecnica.md` | Actualización técnica post-stack |
| 4 | `apendice_IV_final.md` | Plan final detallado |
| 5 | `apendice_IV_suplemento.md` | Suplemento al plan final |
| 6 | `apendice_V.md` | Expansión multi-cuerpo, escalabilidad |
| 7 | `apendice_VI.md` | Monetización y modelo de negocio |
| 8 | `apendice_VII.md` | Roadmap detallado implementación |
| 9 | `apendice_VIII_leyes_RAG.md` | **54 normas legales** con BOE URLs, prioridades |

### 📊 Datasets y verificación

| Documento | Fecha | KB | Estado |
|-----------|-------|-----|--------|
| Dataset Gaps Report | 22/12/2025 | 1 | 📦 Legacy (pre-enriquecimiento) |
| Dataset Verification Report | 09/01/2026 | 13 | ⚠️ Pre-v12 Platinum |
| Scripts Dataset Analysis | 23/12/2025 | 9 | 📦 Legacy |

### 🧹 Operativo

| Documento | Fecha | KB | Estado |
|-----------|-------|-----|--------|
| Plan Limpieza Raíz | 22/01/2026 | 20 | ⚠️ No ejecutado aún |

---

## 12. Datasets: Evaluación COSMIC y Reutilización

### ¿Qué es válido y reutilizable?

| Dataset/Fuente | Tipo | Reutilizable COSMIC | Acción Sugerida |
|----------------|------|:-------------------:|-----------------|
| `MASTER_DATASET_v12_PLATINUM.jsonl` (1.9MB) | Q&A SS | ✅ Sí | Etiquetar por cuerpo + tema |
| `golden_dataset/consolidated/golden_dataset_enriched.jsonl` | Q&A enriquecido | ✅ Sí | Verificar y etiquetar COSMIC |
| `golden_dataset/premium/` (11 archivos) | Razonamiento legal, comparativas, simulacros | ✅ Sí (alto valor) | Curar → contenido premium |
| `golden_dataset/standard/groq_500_qa_verified.jsonl` | Q&A verificado | ✅ Sí | Ya verificado, etiquetar |
| `conceptual_materials/qa_generated/` (11 archivos) | Q&A conceptual | ✅ Sí (AGE) | Mapear a temas AGE |
| `EXAMENES_GENERADOS/` (5 golden) | Exámenes completos | ✅ Sí | Template para generación |
| `staging_area/06_01_26_enrichment/` | Multi-modelo reasoning | ⚠️ Parcial | Filtrar mejor calidad |
| `gran-basurero.jsonl` (52MB) | TODO raw | ⚠️ Filtrar | Rescatar items de calidad |
| `dataset_generator/archive/` | Legacy | ❌ Probablemente no | Revisar caso por caso |

### Adaptación COSMIC recomendada

1. **Etiquetar** todos los Q&A válidos con: `cuerpo` (SS/AGE-C1/AGE-C2/AGE-PI), `tema_id`, `dificultad`
2. **Deduplicar** entre versiones v4→v12 (mucho overlap)
3. **Verificar** calidad con pipeline anti-alucinación existente
4. **Calcular tokens** para estimar costes de re-generación vs reutilización

---

## 13. Cómo Empezar

```bash
# Backend
cd backend
source ../.venv/bin/activate  # O crear venv
pip install -r requirements.txt
cp .env.backend.example .env.backend  # Configurar API keys
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
pnpm install
pnpm dev  # http://localhost:5173

# Docker (Qdrant + Postgres)
docker compose up -d qdrant postgres

# MCP Server
cd mcp-server
pnpm install
pnpm build
```
