# 🌐 OpositAIA — Visión 360º Completa

**Fecha:** 15/05/2026 18:30 UTC+2 — **Versión:** 1.0
**Propósito:** Documento maestro de referencia con TODAS las vertientes del proyecto (estrategias, stack, productos, gaps).
**Fuentes:** Verificación runtime + grafo MCP Memory (~80 entidades) + archivos `.md` del workspace.

---

## 1. Estrategias (las 6 vertientes filosóficas)

### 🌟 1.1 COSMIC — *Create Once, Serve Many*

> 1 concepto atómico → 6 formatos derivados automáticos

- **Formatos derivados:** test + flashcard + mapa mental + caso práctico + esquema + mnemotecnia
- **Reutilización:** 60%+ del contenido entre los 4 cuerpos (SS C1, SS A2, AGE C1, AGE C2)
- **Banco objetivo:** 8K-10K preguntas verificadas (revisado a la baja desde 54K originales del PRD §5)
- **Distribución dificultad:** 20% básico, 50% medio, 30% difícil
- **Diseño:** `plan_app_oposiciones_cosmic.docx` (esquema BD relacional + anti-repetición spaced-repetition)
- **Estado:** ⚠️ DISEÑADO completamente, NO implementado en BD

### 🕸️ 1.2 NEXO v5.1 — Wiki opositora con Muro de Abstracción

> Plan en `/home/spas/OPOS_GEMINI_1/20_04_26_PLAN_WIKI_NEXO_v5_1.md` (archivo real)

- **3 zonas arquitectónicas:**
  1. **FUERA del vault:** `academias/`, `raw_privado/`, `meta_auditoria/` (todo gitignored)
  2. **MURO DE ABSTRACCIÓN:** reescritura para evitar copia literal (Art. 13 LPI)
  3. **Vault público:** `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/` (publicable)
- **Estado actual:** ✅ **249 archivos generados** en vault (184 trampas + 18 esquemas + 22 MOCs/índices)
- **Frontmatter COSMIC obligatorio:**
  ```yaml
  id: T-A1
  titulo: "..."
  tipo: trampa | esquema | concepto | tema | precepto | caso | calculo
  categoria: A | B | ... | R | CA | N_AUTO
  articulos: [Art. 168 TRLGSS, ...]
  tags: []
  peso_examen: alta | media | baja
  verificado_boe: true | false
  confidence: 0.0 - 1.0
  fuentes: [BOE-A-2025-..., ...]
  fecha_creacion: 2026-04-19
  fecha_actualizacion: 2026-04-20
  origen: BOE-DIRECTO | ANÁLISIS-INTERNO | SIMULACRO-PROPIO | JURISPRUDENCIA | CALCULADORA-DOCSTRING | APUNTE-SPAS
  ```
- **Nomenclatura propia** (anti-LCD): *Hueco de Ley, Ancla de Memoria, Repaso Inteligente, Ficha Viva, Curva de Dominio, Ruta Adaptativa, Mapa Legal, Caso Vivo*
- **Versiones recientes:**
  - v5 (20/04 mañana): Muro estricto
  - v5.1 (20/04 tarde): Trampas YA verificadas se reutilizan sin reescribir
  - v5.2 (20/04 17:50): Muro RELAJADO para operación diaria; nombres españoles comunes sueltos NO se prohíben

### 🎭 1.3 Serie Turca — 6 personajes ciclo vital trabajador

> Plan en `/home/spas/OPOS_GEMINI_1/21_04_2026_PLAN_SERIE_TURCA.md` (archivo real, 466 líneas)

| Personaje | Edad | Régimen | Temas que vehicula |
|-----------|------|---------|---------------------|
| **Amparo Rodríguez** | 23 | Becaria/prácticas | T1 + T3 + T11 |
| **Darío Méndez** | 35 | Asalariado + accidente | T2 + T4 + T7 + T8 |
| **Pilar Sáez** | 42 | Autónoma societaria SL | T1 + T4 + T8 (abogada-asesora) |
| **Bartolomé Cañete** | 51 | Empresario impagos | T5 + T6 + T12 |
| **Carmen Ibáñez** | 58 | Prejubilación | T9 + T10 + T11 |
| **Estanislao Vela** | 72 | Pensionista | T9 + T13 |

- **Relaciones familiares cruzadas:**
  - Amparo es sobrina de Carmen
  - Darío trabaja en empresa de Bartolomé (responsabilidad solidaria por accidente)
  - Pilar es abogada-autónoma que asesora a todos
  - Estanislao es padre de Bartolomé (pensión + dependencia + complementos)
  - Carmen es hermana de Darío (gestiona papeles cuando el accidente)
- **1 capítulo = 1 tema oficial** pero cruza 2-3 personajes → universo, no silos
- **Fichas a crear:** `wiki/personajes/{amparo,dario,pilar,bartolome,carmen,estanislao}.md`

### 🧱 1.4 Arquitectura 3 Capas Wiki

> Definida en MCP entity `Arquitectura_3_Capas_Wiki`

- **CAPA 1 — TÉCNICA:** 13 fichas tema específico + 23 generales, neutras, BOE literal. Ruta `wiki/temario/bloque_general/` y `wiki/temario/bloque_especifico_ss/`
- **CAPA 2 — NARRATIVA:** 6 personajes con vidas entrelazadas (serie turca). Temporadas de 13 capítulos. Ruta `wiki/capitulos/temporada_X_*/`
- **CAPA 3 — PRÁCTICA:** 600+ trampas + calculadoras 2026 + simulacros oficiales. Ruta `wiki/trampas/` + `wiki/calculos/` + `wiki/simulacros/`
- **Interconexión wikilinks:** abrir `[[Art. 168 TRLGSS]]` muestra automáticamente:
  - Tema asociado (Capa 1)
  - Personajes afectados (Capa 2)
  - Trampas que lo explotan (Capa 3)
  - Cálculos asociados (Capa 3)
  - Jurisprudencia
- **Veredicto:** la narrativa COMPLEMENTA la técnica, NO la sustituye. Las 3 capas son obligatorias e interconectadas

### 🛡️ 1.5 V14.5 Schema-First (Casos Prácticos)

> LLM NUNCA calcula, NUNCA inventa

```
Blueprint (10 activos: bp_s02-s16)
    ↓
CaseSchemaBuilder (586 LOC) → consulta Neo4j (Precepto)
    ↓
JSON Hermético (datos + trampas + contexto_legal literal)
    ↓
Mistral Large (redactor_v14.yaml) → solo narra prosa
    ↓
ProseValidator (extrae números, bloquea alucinaciones)
    ↓
VerificationOrchestrator (7 agentes de verificación)
    ↓
Caso final 18 preguntas (15 + 3 reserva)
```

- **Estado:** ✅ V14.5 operativo. Bug Neo4j ARREGLADO (case_schema_builder.py:218 ya usa `:Precepto`)
- **Pendiente:** 4 fixes menores en blueprints S11, S16, S10, S12

### 🚧 1.6 Muro de Abstracción Legal (Art. 13 LPI)

- **Material externo de referencia** (uso interno del autor, NO ingestable) NO entra crudo al vault.
- Solo se extraen **patrones genéricos** (estructuras narrativas + mecánicas de trampa) sin contenido literal, sin nombres propios, sin enunciados originales.
- Se reescriben con personajes propios + empresas inventadas.
- **184 trampas** YA pasaron por este filtro (verificadas en lotes 1+2 18-19/04).
- **Cero copia literal** de fuentes externas. **Cero referencia a academias, preparadores, emails, URLs, teléfonos** en código, base de datos o documentación pública.
- Reglas formales: ver `backend/trampas/AUDITORIA_04_05_2026.md` §0.1.

---

## 2. Stack técnico (las 7 capas operativas)

### 🐍 2.1 Backend Python FastAPI (puerto 8080)

| Componente | Archivos | Estado |
|-----------|----------|--------|
| **9 routers principales** | `backend/routers/*.py` | ✅ |
| **opos_chat.py** (Chandra OpenAI-compat) | `backend/routers/opos_chat.py` (364 LOC) | ✅ |
| **31 calculadoras SS** | `backend/calculators/calculos_ss_extended.py` (2.457 LOC) | ✅ |
| **40 calculadoras AGE** | `backend/calculators/calculadora_age.py` (1.128 LOC) | ✅ |
| **calculadora_presupuesto.py** | 466 LOC | ✅ |
| **calculos_imv.py** | 319 LOC | ✅ |
| **dispatcher.py** (routing calculadoras) | 558 LOC | ✅ |
| **11 agentes YAML** | `opos-agents/agents/*.yaml` | ✅ |
| **CaseSchemaBuilder V14** | `backend/v14/case_schema_builder.py` (586 LOC) | ✅ |
| **10 blueprints activos** | `backend/v14/blueprints/bp_s*.py` | ⚠️ 4 con bugs |
| **ProseValidator** | `backend/v14/prose_validator.py` | ✅ |
| **VerificationOrchestrator** | `backend/agents/verification_agents.py` (40 KB) | ✅ 7+ agentes |
| **chandra_tools.py** | `backend/agents/chandra_tools.py` (557 LOC) | ✅ 7 tools |
| **mcp_gateway.py** (Vault REST API) | `backend/routers/mcp_gateway.py` | ✅ |

### 🗄️ 2.2 Bases de datos

| BD | Puerto | Contenido | Estado |
|----|--------|-----------|--------|
| **Neo4j Community** | 7687 | 103 leyes + 6.334 preceptos + 359 EXCEPCION_A bidireccionales | ✅ HEALTHY |
| **Qdrant local** | 6333 | 25.273 puntos FULL_XML + colecciones híbridas | ✅ legacy |
| **PostgreSQL** | 5432 | 8 tablas (user_progress, answer_history, simulacros…) | ⚠️ Schema OK, infrautilizada |

- **Neo4j etiquetas reales:** `:Ley`, `:Precepto`, `:Disposicion` (NO `:Articulo` como decía la auditoría obsoleta)
- **Embeddings Neo4j:** modelo `pablosi/bge-m3-spa-law-qa-trained-2` (1024 dims)
- **Excepciones:** 359 verificadas humano (`verificado_humano: true` en 100%)

### 🤖 2.3 Agentes operativos

| Agente | Modelo | Rol | Dónde |
|--------|--------|-----|-------|
| **Chandra** | mistral-medium-latest | Agente legal 7 tools | BMO Obsidian + backend |
| **redactor_v14** | mistral-large-latest | Narrador casos prácticos (T=0.3, max 8000) | `opos-agents/agents/redactor_v14.yaml` |
| **VerificationOrchestrator** | Multi-modelo | 7+ agentes verificación | `backend/agents/verification_agents.py` |
| **ProseValidator** | Python puro | Anti-alucinación numérica | `backend/v14/prose_validator.py` |
| **CaseSchemaBuilder** | Python puro | Builder JSON hermético | `backend/v14/case_schema_builder.py` |
| **orchestrator** | Multi-modelo | Orquestación pipelines | `backend/agents/orchestrator.py` (374 LOC, ⚠️ legacy) |
| **examiner, validator, generator…** | YAML | Definidos pero subutilizados | `opos-agents/agents/*.yaml` |

#### Las 7 manos de Chandra (`chandra_tools.py`):

1. `tavily_search` — búsqueda web verificada
2. `search_boe` — legislación consolidada BOE
3. `get_law_text_block` — artículos exactos BOE con `as_of_date`
4. `consultar_neo4j` — grafo legal
5. `calcular_ss` — calculadoras SS (vía dispatcher.py)
6. `buscar_vault` — Obsidian trampas/esquemas
7. `escribir_vault` — guardar nota en vault

### 🌐 2.4 Frontend React 19 (Vite + TypeScript)

**17 vistas operativas:**

1. ChatView (RAG + multi-proveedor)
2. CaseGeneratorView (casos prácticos con MCQ)
3. SearchGroundingView (RAG + grounding)
4. SyllabusView (temario navegable)
5. MindMapView (Excalidraw + export PNG/MD/JSON)
6. SchemaView (esquemas jerárquicos)
7. SummaryView (resúmenes)
8. ComparatorView (compara textos legales)
9. StudyPlanView (planes semanales)
10. MockExamView (simulacros cronometrados 70 preg + temporizador)
11. FlashcardsView (flip 3D)
12. ProgressView (dashboard aciertos/fallos)
13. UserGuideView (ayuda)
14. SettingsView (BYOK placeholder)
15. ModelSelector
16. VPSTestView (debug)
17. BackendTestView (debug)

- **Persistencia:** localStorage (no Postgres todavía)
- **Multi-proveedor:** Groq, DeepSeek, Gemini, Mistral, Ollama configurados en `.env.frontend`
- **Estado actual:** funcional pero el flujo real del usuario está derivando a Obsidian. **¿Mantener o aplazar?** decisión pendiente

### 📁 2.5 Vault Obsidian (`/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/`)

- **184 trampas** verificadas BOE en `wiki/trampas/` (18 categorías A-R + CA + N_AUTO)
- **17 esquemas Mermaid** en `wiki/esquemas_con_mapa/`
- **359 excepciones** exportadas a `wiki/_INDICE_EXCEPCIONES.md`
- **Total:** 249 archivos curados (184 trampas + 18 esquemas + 22 MOCs/índices + 25 misc)
- **Plugins instalados** (no Copilot, descartado por licencia):
  - **Activos**: BMO Chatbot (fork), Smart Connections, Excalidraw, Templater, Spaced Repetition, Obsidian-to-Anki, MCP-tools, Execute-code, Local REST API, Mind-map, Mermaid, Dataview, Linter, Git, Find-unlinked-files
- **Perfiles BMO:** `BMO/Profiles/Chandra_Opos.md` (principal), `BMO/Profiles/ExaminadorLegal.md`

### 🔌 2.6 BMO Chandra Edition (fork MIT) — **ÚNICA interfaz Obsidian**

> Copilot DESCARTADO por mala licencia

- **Repo:** `Espasiko/obsidian-bmo-chatbot-plus` rama `feature/multi-chat`
- **4 commits desplegados:** 49dc120 → e34cb2b → a8985c2 → 3ed480e
- **Features hechas (Fase 1A-1B-2-3):**
  - Multi-chat con sidebar de conversaciones
  - Header editable inline con título auto-generado
  - Persistencia `.md` en `BMO/Chats/{Perfil}/{fecha}__{titulo}__{uuid}.md` con frontmatter
  - Comando `/clear` crea conversación nueva
- **Pendiente Fases 4-7:**
  - PDF support (drag & drop o click)
  - Multimodal (imágenes via Mistral Pixtral / Gemini Vision)
  - Tool calling UI visible (streaming + bloques colapsables)
  - Autocompletados `@agente`, `/workflow`, `*ejecutar`
  - Selector de modelo inline
  - Toggle context-picker (3 botones: nota actual / vault / solo prompt)

### 🔧 2.7 MCP Servers conectados

| Server | Nombre técnico | Para qué | Estado |
|--------|---------------|----------|--------|
| **memory** | `@modelcontextprotocol/server-memory` | Grafo conocimiento (~80+ entidades) | ✅ activo (mcp4_*) |
| **boe** | `mcp-boe` (uvx) | Búsqueda legislación BOE | ✅ activo (mcp0_*) |
| **github** | `github-mcp-server` (Docker) | Repos y PRs | ✅ activo (mcp2_*) |
| **fetch** | mcp-server-fetch | URLs externas | ✅ activo (mcp1_*) |
| **kaggle** | `mcp-remote` | Fine-tuning | ✅ activo |

---

## 3. Productos: 3 SKUs comerciales

> Fuente autoritativa: nodo MCP `Modelo_Negocio_3_SKUs_28_04_2026`

### 🌐 3.1 SKU 1 — Web App OpositAIA

- **Cliente:** opositor casual no técnico
- **Entregable:** Frontend React 17 vistas → backend `/opos/v1/chat/completions`
- **Pricing:** Trial €1/3d + Pro €69/mes (decidido en `docs/prd.md` §RF-05)
- **Estado:** 17 vistas operativas, falta Stripe + Auth + migración localStorage→Postgres
- **Decisión legal:** contenido BOE es dominio público (Art. 13 LPI). Mitigación LCD via nomenclatura propia
- **Tiempo estimado para MVP venta:** ~30 días (Stripe + Auth + Postgres + UX polish)

### 📦 3.2 SKU 2 — OPOS Vault Premium (.zip + .exe)

- **Cliente:** opositor hardcore técnico
- **Entregable:**
  - Vault Obsidian preconfigurado con plugins (BMO Chandra Edition + Smart Connections + Excalidraw + Spaced Repetition + Anki bridge)
  - `.exe` proxy que conecta su BMO local a `/opos/v1/chat/completions` vía License Key
  - `INSTALAR.md` con guía paso a paso
- **Pricing:** pago único o anual
- **Validación:** ✅ vault YA existe en `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/`. Solo falta empaquetar
- **Precedente:** existe **EscritorAIA Nina_v2_27_04_2026** (vault para novelistas) que demuestra el patrón
- **Tiempo estimado:** ~7-10 días (script de packaging + .exe proxy con Tauri/Electron + License Key server)

### 🔌 3.3 SKU 3 — API B2B (futuro)

- **Cliente:** academias y centros de formación (clientes B2B)
- **Entregable:** SDK + endpoint OpenAI-compat con rate limits + facturación por tokens
- **Pricing:** €/1K tokens o flat fee mensual
- **Estado:** trivial sobre la base existente (router `opos_chat.py` ya es OpenAI-compatible)
- **Tiempo estimado:** ~14 días (auth keys + rate limit + dashboard)

---

## 4. Productos derivados COSMIC (visión)

> Aplicabilidad de la arquitectura COSMIC más allá de OPOS SS

| Producto | Vault destino | Reutilización backend | Ventana mercado |
|----------|---------------|----------------------|-----------------|
| **OpositAIA SS C1** (actual) | `BOVEDA_OPOS` | 100% (origen) | 5.794 plazas turno libre 2026 |
| **OpositAIA SS A2 Gestión** | `BOVEDA_GESTION` | 80% | A confirmar |
| **OpositAIA AGE C1/C2/PI** | `BOVEDA_AGE` | 60% | Convocatoria anual |
| **JuristaAIA** (abogados) | `VAULT_LEGAL_PRO` | 50% | ~250.000 abogados España |
| **EstudiantesDerecho** | `VAULT_DERECHO` | 40% | ~50.000 alumnos/año |
| **AutónomoAIA** (cash-flow RETA + Prophet) | `VAULT_AUTONOMO` | 30% | ~3.4M autónomos España |
| **EscritorAIA** (Nina) | `BOOK_VAULT_NINA` | 10% ✅ ya existe v2 | Nicho |

---

## 5. Trampas y patrones (Capa 3 Práctica)

### 5.1 Catálogo activo

- **184 trampas** verificadas BOE en `wiki/trampas/` (18 categorías):
  - A — Encuadramiento
  - B — IT
  - C — Jubilación
  - D — IP
  - E — Procedimiento
  - F — Bases CC
  - G — Recargos
  - H — Plazos
  - I — Otras
  - J — MS ampliada
  - Q — FP ampliada
  - R — RETA
  - S — Mixtas
  - CA — Casos
  - N_AUTO — Autónomos
  - + 3 más

### 5.2 Plan Maestro Simulacros v4

> Archivo: documento maestro en carpeta privada del autor (uso interno, gitignored). Ruta abstracta: `academias/<carpeta_privada>/PLAN_MAESTRO_CASOS_SIMULACROS.md` (1157 líneas).

- **Total trampas catalogadas (mecánicas genéricas):** ~479
- **Total preguntas banco interno auditado:** ~752
- **Materiales de referencia (uso interno autor, NO ingestados):** simulacros mensuales 2025-2026 procedentes de fuentes externas locales, anonimizadas en el catalogo de mecánicas.
- **Fecha de corte normativa:** 04/03/2026

### 5.3 Patrones narrativos genéricos (9 identificados)

> Patrones abstractos catalogados desde análisis interno del autor sobre material de referencia local. Sin contenido literal, sin nombres propios, sin vínculo a fuentes externas concretas.

| # | Patrón | V14 implementa | hay version 14.5 IMPORTANTE!!!
|---|--------|----------------|
| 1 | Red de personajes (4-6 actores con nombres + parentescos + conflictos) | ❌ |
| 2 | Conflictos cruzados (impago + accidente + embargo en un caso) | ❌ |
| 3 | Salto de régimen (Encuadramiento → Recaudación → Jubilación) | ❌ |
| 4 | Narrativa evolutiva ('en junio… en noviembre…') | ❌ |
| 5 | Trampa de parentesco (hijo discapacitado altera prestación) | ❌ |
| 6 | Relleno inteligente (distractores puros sin valor calculatorio) | ⚠️ Parcial |
| 7 | Vuelco de los 15 días (notificación vs emisión) | ❌ |
| 8 | Numeración desordenada (P1→P17→P20→P18→P19) | ❌ |
| 9 | Errores tipográficos intencionales del enunciador | ❌ |

**Gap:** V14 solo tiene patrón 6 parcialmente. Necesita implementar 1-5 + 7-9.

---

## 6. Qué FALTA por hacer (priorizado por urgencia)

### 🔴 Crítico (días)

1. **4 fixes blueprints** S11, S16, S10, S12 (5 min c/u)
2. **REGLA 8 anti-alucinación** en `redactor_v14.yaml`
3. **Refactor calculadoras** modular (2-3h con tests + estrategia segura: `prestaciones_ss/` o renombrar `calculos_ss.py → calculos_ss_base.py`)
4. **LiteLLM enrutador** multi-IA (Mistral → DeepSeek → Cohere → Groq, con Exponential Backoff)
5. **Filtrar PII** del YAML trampas (cualquier nombre propio + empresa inventada residual)
6. **Limpiar MISTRAL_URL** obsoleta de `.env.backend`

### 🟡 Importante (semanas)

7. **Chain-of-Verification (CoVe)** post-respuesta en Chandra
8. **Auto-RAG pre-respuesta** (inyectar trampas relevantes antes del primer token)
9. **Few-shot calibration** en CHANDRA_SYSTEM_PROMPT (3-5 ejemplos)
10. **4 manos nuevas Chandra:** `flashcards_anki`, `mermaid`, `simulacro_test`, `resumir_nota`
11. **9 patrones narrativos genéricos completos** en CaseSchemaBuilder
12. **Seed 52 mecánicas de trampas** a Neo4j como nodos `:Trampa` (TPL, TCM, TCT...)
13. **Sync blueprints ↔ Neo4j** (relación `:APLICA_EN`)
14. **Casos validados internamente** (cross-check Mistral + DeepSeek + Cohere)

### 🟢 Deseable (meses)

15. **Tool calling UI** visible en BMO (streaming + bloques colapsables)
16. **Soporte PDF + multimodal** en BMO (drag & drop)
17. **6 plantillas Templater** (T1-T6: caso práctico, simulacro, flashcards, mermaid, mapa mental, esquema)
18. **9 tools utilitarias** (PDF, exec, file ops vault, fetch URL, MCP genérico)
19. **Repoblado completo** `wiki/temario/` (13 temas con Muro de Abstracción)
20. **Fichas personajes** `wiki/personajes/{amparo,dario,pilar,bartolome,carmen,estanislao}.md`
21. **Capítulos serie turca** `wiki/capitulos/temporada_X_*/`
22. **Ideas creativas Wiki 12** (matriz puentes, Error Museum, timeline legal, glosario falsos amigos…)
23. **Stripe + Auth** para SKU 1 (Fase 3 PRD)
24. **Empaquetado SKU 2** (.zip + .exe + License Key)

### 🔵 Futuro (cuando producto esté maduro)

25. **API B2B** (SKU 3) — endpoint OpenAI-compat con rate limits
26. **Tauri Desktop App** (después de SKUs 1+2)
27. **Productos derivados COSMIC** (JuristaAIA, AutónomoAIA, EstudiantesDerecho…)

---

## 7. Decisiones clave pendientes

### Q1-Q4 desde el `Plan_Chandra_v2_03_05_2026` (12 días abiertas)

- **Q1:** ✅ HECHO — BMO repo clonado (`Espasiko/obsidian-bmo-chatbot-plus`)
- **Q2:** ¿Borrar `BMO_back_mal/` y `ChatGPT_MD/` vacías del vault?
- **Q3:** Orden fases: ¿confirmas **1→2→4→3→5** (recomendación Kimi)?
- **Q4:** ~~¿Priorizar Copilot?~~ → **DESCARTADO por mala licencia**

### Nuevas (auditoría 15/05)

- **Q5:** ¿Frontend React mantener o sustituir? (flujo real ya en Obsidian)
- **Q6:** ¿Migrar localStorage → Postgres en frontend ahora o aplazar?
- **Q7:** ¿Cuándo activar Knowledge Tracing / FSRS? (antes/después de 1.000 usuarios)
- **Q8:** ¿Empezar packaging SKU 2 en paralelo con SKU 1, o secuencial?

---

## 8. Fuentes autoritativas

### 8.1 Archivos `.md` reales (en disco)

- `/home/spas/OPOS_GEMINI_1/10_05_2026_IDEAS_KIMI.MD` — plan consolidado Kimi (5 fases)
- `/home/spas/OPOS_GEMINI_1/14_05_2026_MEMORIA_SESION_ANTI.md` — memoria Antigravity
- `/home/spas/OPOS_GEMINI_1/21_04_2026_PLAN_SERIE_TURCA.md` — Serie Turca (466 líneas)
- `/home/spas/OPOS_GEMINI_1/20_04_26_PLAN_WIKI_NEXO_v5_1.md` — NEXO v5.1
- `academias/<carpeta_privada>/PLAN_MAESTRO_CASOS_SIMULACROS.md` — Plan Maestro v4 (1157 líneas, uso interno autor, gitignored)
- `/home/spas/OPOS_GEMINI_1/docs/prd.md` — PRD oficial
- `/home/spas/OPOS_GEMINI_1/docs/product-brief.md` — Brief producto
- `/home/spas/OPOS_GEMINI_1/docs/project-overview.md` — Overview
- `/home/spas/OPOS_GEMINI_1/FLUJO_24_03.md` — Flujo procesos
- `/home/spas/OPOS_GEMINI_1/.gemini/antigravity/brain/44a94c17-.../IDEAS_MAESTRAS_OPOSITAIA_2026.md.resolved` — Ideas maestras
- `/home/spas/OPOS_GEMINI_1/backend/trampas/AUDITORIA_04_05_2026.md` — Auditoría 04/05 con 52 trampas TPL/TCM/TCT
- `/home/spas/OPOS_GEMINI_1/15_05_2026_BORRADOR_AUDITORIA_Y_PLAN.md` — Borrador auditoría 15/05

### 8.2 Entidades MCP Memory (consultar con `mcp4_open_nodes`)

| Entidad | Tipo | Contiene |
|---------|------|----------|
| `Plan_Chandra_v2_03_05_2026` | StrategicPlan | Plan 5 fases + 10 BPs + Q1-Q4 |
| `Modelo_Negocio_3_SKUs_28_04_2026` | BusinessModel | 3 SKUs + pricing |
| `Plan_Refactor_Calculadoras_Pendiente_29_04_2026` | TechnicalDebt | Estrategia segura refactor |
| `Chandra_Agent_System` | AgentSystem | 7 tools + system prompt |
| `BMO_Chandra_Edition_Fork` | ArchitectureComponent | Estado fork |
| `Verificacion_Sistema_03_05_2026` | AuditSnapshot | Estado infra |
| `Auditoria_Calculadoras_29_04_2026_BugsResueltos` | AuditReport | 8 bugs + 5 gaps |
| `Plan_Wiki_NEXO_v5_1` | plan_arquitectura | NEXO v5.1+v5.2 |
| `Plan_Serie_Turca_21_04_2026` | MasterPlan | Serie Turca + 6 personajes |
| `Personajes_Ciclo_Vital_OPOS` | PedagogicalCharacters | 6 personajes detallados |
| `Arquitectura_3_Capas_Wiki` | Architecture | 3 capas wiki |
| `Estrategia_COSMIC` | Strategy | Create Once Serve Many |
| `Patrones_Narrativos_DM_9` (entity MCP, nombre legacy) | catalogo_descubrimiento | 9 patrones narrativos genéricos extraídos del análisis interno |
| `Plan_Maestro_Simulacros_v4` | documento_plan | 479 trampas + 752 preguntas |
| `Catalogo_Trampas_Principal_YAML` + `_Adicional_YAML` | CatalogFile | 120+ trampas verificadas BOE |
| `Trampas_Verificadas_184_19_04_26` | Verification | 184 trampas curadas |
| `Ideas_Creativas_Wiki_12` | FeatureBacklog | 12 ideas creativas |
| `Ideas Groq Multi-modelo 02.05.26` | Strategy | LiteLLM detallado |
| `Sistema_Casos_Practicos_V14_09_04_2026` | ProjectSubsystem | V14.5 Schema-First |
| `Sesion_03_05_2026_BMO_Chandra_Edition` | Session | Fase 1A+1B BMO |

---

**Próximo paso:** revisar este documento y discutir piezas concretas que necesiten aclaración.

---

## 9. Wiki LLM híbrido (Karpathy + Nate + Zettelkasten + Dataview)

> Filosofía actualizada 17/05/2026 tras revisión `12_05_26_GROK_CONVERSACION_SECOND_BRAIN.md` + `20_04_26_PLAN_WIKI_NEXO_v5_1.md`.

### 9.1 Mezcla de tres patrones probados

| Patrón | Origen | Aporte al proyecto |
|--------|--------|--------------------|
| **LLM-Wiki** | Andrej Karpathy (tweet famoso) | 3 capas: `raw/` (fuentes brutas) + `wiki/` (LLM mantiene) + `schema/CLAUDE.md` (reglas inviolables que el LLM obedece al editar) |
| **Building a Second Brain / PARA** | Tiago Forte / Nate Liason | Flujo `capture → distill → develop → express`. Estructura PARA (Proyecto/Área/Recurso/Archivo) |
| **Zettelkasten / Folgezettel** | Niklas Luhmann (DE) | Notas atómicas (1 idea = 1 archivo), enlaces densos `[[wiki-link]]`, MOCs (Maps of Content) emergentes desde abajo, índice mínimo |

### 9.2 Estado en el proyecto OPOSITAIA

| Patrón | Estado | Detalle |
|--------|--------|---------|
| 3 capas (raw/wiki/schema) | ⚠️ parcial | `wiki/` existe; falta `schema/CLAUDE.md` con reglas LLM y `raw/` privada gitignored |
| Notas atómicas | ⚠️ parcial | 184 trampas son atómicas, los 13 temas no |
| Dataview queries como índices | ❌ no | Plugin instalable; falta `index.md` con queries |
| MOCs (Maps of Content) | ❌ no | Hay `_INDICE_EXCEPCIONES.md` (76 KB!) — convertir en MOCs por tema |
| `CLAUDE.md` con reglas LLM | ❌ falta | Plan describe formato; no creado en disco |
| Graph RAG Neo4j para excepciones | ✅ | 359 `EXCEPCION_A` bidireccionales |
| Generador + Revisor crítico | ⚠️ parcial | `redactor_v14` existe; `validator.yaml` desconectado del flujo live |

### 9.3 Sistema multi-agente + workflows + comandos en BMO

#### Estructura propuesta dentro del vault del usuario:
```
.bmo/
├── agents/
│   ├── chandra.yaml             ← agente legal por defecto (chat normal)
│   ├── indexador_pdf.yaml       ← extrae PDFs y crea Zettel
│   ├── conversor_doc.yaml       ← .docx/.html → Markdown limpio
│   ├── cartografo_zettel.yaml   ← detecta clusters y crea MOCs
│   ├── validador_boe.yaml       ← cruza con Neo4j BOE
│   └── jurista.yaml             ← variante para mercado legal
├── workflows/
│   ├── ingest_simulacro.yaml    ← pipeline 4 pasos: index→detectar→validar→cartografiar
│   ├── nuevo_tema.yaml          ← crea estructura Zettelkasten + MOC para un tema
│   ├── auditar_vault.yaml       ← detecta huérfanos, links rotos, frontmatter incompleto
│   └── publicar_release.yaml    ← prepara vault para empaquetar (.exe ready)
└── tools/
    ├── pdf_ocr.json             ← spec OpenAI tool format
    ├── docx_reader.json
    ├── vault_grep.json
    ├── vault_create_note.json
    ├── exec_python.json         ← sandbox Pyodide
    ├── exec_terminal.json       ← bash con whitelist
    ├── flashcards_anki.json
    ├── mermaid_validator.json
    ├── fetch_url.json           ← whitelist
    └── mcp_proxy.json           ← cliente genérico MCP
```

#### Comandos BMO ampliados (a implementar en `Commands.ts`):
```
/agent <nombre>              → cambia agente activo (= profile + system_prompt + tools subset)
/agent indexador_pdf <archivo>  → invoca agente puntualmente
/workflow <nombre> <args>    → ejecuta pipeline multi-paso
/byok <provider> <key>       → añade/cambia API key sin abrir settings
/mcp <server> <comando>      → consulta a un servidor MCP local
@modelo "pregunta"           → switch puntual de modelo (@groq-llama-70b, @deepseek-r1)
*tool <args>                 → invocar herramienta directa
```

#### Indexación con Dataview + Zettelkasten:

```markdown
# wiki/MOCs/jubilacion.md (auto-generado por agente cartografo_zettel)

## Trampas relacionadas
\`\`\`dataview
TABLE codigo, dificultad, ultima_revision
FROM "wiki/trampas"
WHERE contains(temas, "jubilacion")
SORT codigo ASC
\`\`\`

## Preceptos clave
\`\`\`dataview
LIST
FROM "wiki/preceptos"
WHERE ley = "TRLGSS" AND numero >= 204 AND numero <= 215
\`\`\`

## Notas Zettelkasten relacionadas
\`\`\`dataview
LIST file.link
FROM "wiki/zettelkasten"
WHERE contains(tags, "jubilacion") OR contains(tags, "edad-ordinaria")
SORT file.ctime DESC
\`\`\`
```

### 9.4 Loop autosostenido de crecimiento de la wiki

```
PDF/.docx/URL externa
   ↓ /workflow ingest_simulacro
indexador_pdf crea fichas en wiki/zettelkasten/{YYYYMMDD-HHMM}-{slug}.md
   ↓
detector_trampas marca patrones y los cataloga en wiki/trampas/
   ↓
validador_boe cruza contra Neo4j (verificado_boe = true|false)
   ↓
cartografo_zettel actualiza wiki/MOCs/{tema}.md
   ↓
Dataview re-genera índices al abrir notas
   ↓
Wiki crece de forma orgánica + verificada
```

---

## 10. Estado de leyes en Neo4j (verificado 17/05/2026)

### 10.1 Leyes ingeridas correctamente

- ✅ TRLGSS RDLeg 8/2015 (`BOE-A-2015-11724`) — 6.334 preceptos
- ✅ Estatuto de los Trabajadores RDLeg 2/2015 (`BOE-A-2015-11430`)
- ✅ LPAC Ley 39/2015 (`BOE-A-2015-10565`)
- ✅ LRJSP Ley 40/2015 (`BOE-A-2015-10566`)
- ✅ TREBEP RDLeg 5/2015 (`BOE-A-2015-11719`)
- ✅ Ley 19/2021 IMV (`BOE-A-2021-21007`)
- ✅ RD 1539/2003 jubilación discapacidad ≥65% (`BOE-A-2003-23401`)
- ✅ RD 1851/2009 jubilación discapacidad ≥45% (`BOE-A-2009-20652`) ← **renombrado por RD 370/2023**

### 10.2 Leyes faltantes — estado tras verificación MCP BOE (17/05/2026)

#### Verificadas vía MCP BOE y AÑADIDAS a `catalog_v17.json` v17.4 → INGESTANDO 17/05

| Norma | BOE ID real | Estado | Prioridad |
|-------|--------------|--------|-----------|
| **RD 2366/1984** Minería del carbón | `BOE-A-1985-806` ✅ | Ingestando (9 preceptos) | � |
| **Ley 15/2022** Igualdad de trato | `BOE-A-2022-11589` ✅ | Ingestando | 🔴 |
| **RDL 5/2023** Conciliación familiar/profesional | `BOE-A-2023-15135` ✅ | Ingestando | 🔴 |
| **RD 370/2023** Modifica RD 1851/2009 | `BOE-A-2023-11644` ✅ | Ingestando | 🟢 |

#### Descartadas tras verificación BOE

| Norma propuesta | Razón |
|-----------------|-------|
| ~~RD 1538/2003~~ | `BOE-A-2003-23400` es **inspección educativa**, NO discapacidad SS. Referencia previa errónea |
| ~~RD 1413/2005~~ | ✅ **CORREGIDO 19/05/2026** — SÍ es desempleo/capitalización. INGESTADO a Neo4j (4 preceptos + relaciones Art. 262, Art. 296 TRLGSS, RD 625/1985) |
| ~~OM 31/01/1970~~ | Sin consolidar en BOE. Demasiado histórica para pipeline `ingest_neo4j_v17.py` |

#### Leyes FALTANTES pendientes de ingestión (verificado 19/05/2026)

| Norma | BOE ID | Prioridad | Estado |
|-------|--------|-----------|--------|
| **Ley 45/2002** Reforma desempleo/ocupabilidad | `BOE-A-2002-24244` | **ALTA** — Ley madre que modifica RD 1413/2005. 6 arts + 12 DA + 9 DT. Capitalización, compromiso actividad, renta activa inserción | ❌ No ingestada |
| **LO 3/1980** Consejo de Estado | `BOE-A-1980-8648` | MEDIA — AGE. Ya en Neo4j con 0 preceptos | ⚠️ Re-ingestar con `ingest_boe_html_historico.py` |
| **RD 1311/2007** Trabajadores del mar | ELI: `/eli/es/rd/2007/10/05/1311` | BAJA — Sistema especial. BOE ID consolidado no encontrado | ❌ Pendiente búsqueda manual |

Comando ingestión: `.venv/bin/python backend/scripts/ingest_neo4j_v17.py --only-law BOE-A-2002-24244 --skip-purge`

#### Fallback BOE HTML en Chandra (PENDIENTE implementar)

> Problema: `get_law_text_block` usa la API de datos abiertos del BOE (`datosabiertos/api/legislacion-consolidada`).
> No todas las leyes tienen XML consolidado → 404 en la API.
> Solución: añadir fallback en `chandra_tools.py` que scrapeé el HTML de `boe.es/buscar/act.php?id={ID}` cuando la API da 404.
> Archivo: `backend/agents/chandra_tools.py` → función `tool_get_law_text_block()` → añadir `httpx.get(html_url)` + `BeautifulSoup` parse como último recurso.

### 10.3 Resúmenes del vault: estado de validación

- ✅ `wiki/temario/RD_1539_2003_jubilacion_discapacidad/resumen_opositor.md` — generado por Mistral, contenido correcto vs Neo4j, **PENDIENTE revisión humana** (NO marcado verificado).
- ⚠️ Hueco menor: no menciona el renombrado por RD 370/2023.

---

## 11. Bloqueante crítico — DATOS_ACADEMIA contiene PII

> Detectado 17/05/2026.

`/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/DATOS_ACADEMIA/ac_las_cortes_md/` contiene materiales privados de academia con **PII flagrante** (nombres propios de preparadores, esquemas firmados, exámenes, listados oficiales con DNI). Si el vault se empaqueta tal cual al `.exe`, se publica una violación masiva del Art. 13 LPI + GDPR.

**Acción inmediata requerida (antes de cualquier release)**:
1. Mover `wiki/DATOS_ACADEMIA/` fuera del vault publicable → a `/mnt/d/MATERIAL_PRIVADO_AUTOR/` (no enlazada al vault).
2. Crear `.dataviewignore` en raíz del vault con entrada explícita.
3. Añadir entrada en `.gitignore` del vault.
4. Crear `.bmo/exclude_patterns.yaml` para que el agente `publicar_release` excluya cualquier carpeta con patrones PII.

> **Actualización 17/05/2026:** Decisión USER → NO mover nada todavía. Vault actual se mantiene para pruebas multi-LLM (Mistral, DeepSeek, Groq, Cohere…). El vault publicable será nuevo y se construirá desde cero más adelante. Uso personal por la hija del autor con materiales que ella compró es lícito (uso doméstico, no infringe LPI/GDPR mientras no se comparta/publique).

---

## 12. Pipeline de ingestión Neo4j (verificado 17/05/2026)

### 12.1 Script DEFINITIVO

`@/home/spas/OPOS_GEMINI_1/backend/scripts/ingest_neo4j_v17.py:1-1324` — Cypher 5, Neo4j 2026.02.3, idempotente con MERGE.

### 12.2 Modelo de embeddings

- **Modelo:** `pablosi/bge-m3-spa-law-qa-trained-2` (1024 dims, fine-tuneado en español legal Q&A).
- **Normalización:** `normalize_embeddings=True` (vectores unitarios → cosine = dot product).
- **Batch:** 16 preceptos por encode call.

### 12.3 Chunking con overlap

```python
MAX_CHARS_PER_CHUNK  = 20000   # ~5000 tokens
CHUNK_OVERLAP_CHARS  = 2000    # ~500 tokens solapamiento (10%)
```

- **Corte preferido:** primero `\n`, luego `". "`, último recurso corte duro.
- **Artículos largos:** se dividen en chunks `Art_X_LEY_c0`, `_c1`, `_c2`… enlazados con relación `:SIGUIENTE` para reconstrucción ordenada.
- **Stats actuales:** 25 relaciones `:SIGUIENTE` en BD (chunks de preceptos largos como `DF 3ª LRJSP` con 2 chunks).

### 12.4 Esquema Neo4j real (verificado 17/05)

#### Labels
- **`:Ley`** (108 nodos) — uno por norma BOE
- **`:Precepto`** (6.683 nodos) — base label de todo articulado
- **`:Articulo`** (~5.036 nodos) — multi-label `:Precepto:Articulo`
- **`:Disposicion`** (~1.643 nodos) — multi-label `:Precepto:Disposicion`
- **`:ValorLegal`** (36 nodos) — constantes legales (cuantías, plazos…)
- **`:Indice`** (1 nodo) — root opcional

#### Relaciones
| Tipo | Cantidad | Significado |
|------|----------|-------------|
| `PERTENECE_A` | 6.683 | `Precepto → Ley` |
| `EXCEPCION_A` | 379 | `Precepto → Precepto` (bidireccional, curada manual) |
| `TIENE_EXCEPCION_EN` | 323 | inverso semántico de `EXCEPCION_A` |
| `MODIFICA` | 76+ | `Ley → Ley` (desde `<analisis>` BOE) |
| `DEROGA` | 49 | `Ley → Ley` |
| `ESTABLECIDO_EN` | 44 | `ValorLegal → Precepto` |
| `SIGUIENTE` | 28+ | `Precepto → Precepto` (chunks ordenados) |
| `DESARROLLA` | 7 | `Ley → Ley` (reglamentos) |
| `RELACIONADO_CON` | 2+ | `Precepto → Precepto` (conexiones temáticas cross-ley) |

#### Indexes
- **`precepto_embedding`** VECTOR HNSW (1024 dims, m=16, ef=100, cosine) ← búsqueda semántica
- **`precepto_fulltext`** FULLTEXT spanish analyzer sobre `(texto, title)` ← búsqueda léxica
- **`precepto_id`**, **`precepto_ley_id`**, **`precepto_vigente`**, **`ley_boe_id`**, **`ley_siglas`**, **`articulo_numero`** RANGE
- **`precepto_community`** RANGE sobre `communityId` ← Louvain community detection
- **`valor_legal_id`** RANGE, **`valor_legal_fulltext`** FULLTEXT

#### Constraints UNIQUE
- `Ley.boe_id`, `Precepto.id`, `ValorLegal.id`

### 12.5 Cadena de fallback BOE (4 etapas)

```
1. Caché XML v17 local en /home/spas/OPOS_GEMINI_1/data/boe_xml/{boe_id}_v17.xml
2. API consolidada BOE: https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{boe_id}
3. Caché JSON legacy v16 (ene 2026) — desactualizada, último recurso
4. buscar/xml.php (publicación original) https://www.boe.es/buscar/xml.php?id={boe_id}
```

### 12.6 Propiedades Precepto

`id`, `title`, `texto`, `ley_id`, `ley_siglas`, `vigente`, `fecha_vigencia`, `url_boe`, `source`, `numero`, `sufijo`, `tipo_disposicion`, `ordinal`, `chunk_index`, `total_chunks`, `embedding` (1024 floats).

### 12.7 Propiedades Ley

`boe_id`, `titulo`, `siglas`, `tipo`, `rango_codigo`, `ambito`, `departamento`, `numero_oficial`, `fecha_pub`, `fecha_disposicion`, `fecha_vigencia_ley`, `fecha_consolidacion`, `url_eli`, `url_boe`, `estado_consolidacion`, `estatus_derogacion`, `num_articulos_boe`, `num_disposiciones_boe`, `tiene_xml`, `historica`, `materias` (vocab. controlado), `prioridad`, `boe_id_verificado`, `ingested_at`.

### 12.8 Comando estándar para añadir nueva ley

```bash
# 1. Añadir entrada al catálogo
vim backend/data/catalog_v17.json   # añadir { boe_id, siglas, titulo, url, parte, cuerpos, ... }

# 2. Ingestar SIN purge (preserva los 103 leyes existentes)
.venv/bin/python backend/scripts/ingest_neo4j_v17.py --only-law BOE-A-NNNN-NNNN --skip-purge
```

### 12.9 Louvain Community Detection (NUEVO 19/05/2026)

> **Implementación:** Python `networkx` + `python-louvain` (GDS no instalado en Community Edition).
>
> **Resultado:** 517 comunidades sobre 6.683 preceptos. Propiedad `communityId` en cada nodo `:Precepto`.
>
> **Metodología:**
> 1. Exportar grafo (aristas directas + co-pertenencia a misma ley)
> 2. Ejecutar Louvain (resolution=1.0, weight-aware)
> 3. Escribir `communityId` de vuelta a Neo4j con UNWIND batch
>
> **Top comunidades:** TRLGSS(447), LCSP(393), Ley 36/2011(326), TRLGSS-1994(314), Ley 13/1996(223), LRJSP(214)
>
> **Usos inmediatos:**
> - Generar resúmenes por comunidad (Cascade, no Ollama)
> - Flashcards agrupadas por cluster temático
> - Mapas mentales / esquemas por comunidad
> - Blueprints y checklists por tema del temario
> - Tracking progreso usuario por comunidad
>
> **Script:** Inline Python (sesión 19/05/2026). Mapa JSON: `backend/data/louvain_communities.json`
>
> **Ejecución:** `MATCH (p:Precepto {communityId: X}) RETURN p.title, p.ley_siglas`

### 12.10 Qdrant — estado oficial

> **Qdrant DESCARTADO como fuente de verdad.** Neo4j es la fuente única.
>
> Se mantiene Qdrant local (puerto 6333, 25.273 puntos legacy FULL_XML) por si se reutiliza en un flujo no crítico (p.ej. búsqueda fulltext baja latencia para BMO sin ir a Neo4j). NO se sincroniza con Neo4j ni se actualiza con las nuevas leyes.

### 12.11 Búsqueda Híbrida — estado (19/05/2026)

> **Neo4j 2026 soporta búsqueda híbrida nativa** (vector + fulltext + Cypher). Qdrant NO necesario.
>
> **Indexes existentes:**
> - `precepto_embedding` HNSW 1024d → `CALL db.index.vector.queryNodes('precepto_embedding', K, $embedding)`
> - `precepto_fulltext` spanish → `CALL db.index.fulltext.queryNodes('precepto_fulltext', $query)`
>
> **Estado:** ✅ IMPLEMENTADO 19/05/2026. `_hybrid_search_neo4j()` en `chandra_tools.py`:
> - Vector HNSW + Fulltext spanish + RRF reranking (k=60)
> - Modelo embedding cacheado como singleton (`_get_embedding_model()`)
> - Se activa automáticamente cuando `consultar_neo4j` recibe `pregunta_nl` (modo por defecto)
> - Devuelve: `id`, `title`, `ley`, `extracto`, `rrf_score`, `community`

### 12.12 Multi-hop Reasoning (19/05/2026)

> **Qué es:** Recorrer 2-3 relaciones en el grafo para responder preguntas complejas.
>
> **Ejemplo:** "¿Excepciones al plazo de prescripción con reclamación previa?"
> ```cypher
> MATCH (p:Precepto)-[:EXCEPCION_A]->(exc:Precepto)-[:PERTENECE_A]->(l:Ley)
> WHERE p.texto CONTAINS 'prescripción' AND exc.texto CONTAINS 'reclamación'
> RETURN p.title, exc.title, l.siglas
> ```
>
> **Implementación:** ✅ COMPLETADO 19/05/2026. 5 few-shot examples añadidos al system prompt de Chandra:
> 1. Excepciones a un artículo (`MATCH (p)-[:EXCEPCION_A]->(exc)`)
> 2. Qué modifica una ley (`MATCH (src)-[:MODIFICA]->(dst)`)
> 3. Preceptos de la misma comunidad Louvain (`MATCH {communityId}`)
> 4. Búsqueda híbrida automática (pregunta NL → RRF)
> 5. Cadena de chunks de artículo largo (`[:SIGUIENTE*0..5]`)

### 12.13 Sincronización Obsidian ↔ Neo4j (Project Synapse)

> **Concepto:** MCP server bidireccional vault ↔ grafo.
>
> **Lo que YA existe:**
> - `escribir_vault` (Chandra mano #7) → crea notas en vault
> - `buscar_vault` (Chandra mano #6) → busca en vault
> - `mcp_gateway.py` endpoint REST `/mcp/vault/write`
>
> **Lo que FALTA:**
> - File watcher: cambios vault → auto-actualiza Neo4j
> - Post-ingesta hook: nueva ley Neo4j → genera `.md` en vault
> - NOT urgent, implementable como custom plugin o MCP server

---

## 13. Roadmap de fases (consolidado 19/05/2026)

### Fase 0 — Estabilización ✅ COMPLETADO 17/05/2026
- 4 fixes blueprints (BP-S10, BP-S11, BP-S12, BP-S16)
- REGLA 8 anti-alucinación de apartados en `redactor_v14.yaml`
- 4 leyes nuevas ingestadas a Neo4j (RD 2366/1984, Ley 15/2022, RDL 5/2023, RD 370/2023)
- Few-shot del `redactor_v14.yaml` anonimizado preservando veracidad jurídica
- VISION_360 ampliado con secciones 9-13
- Grafo MCP Memory actualizado con sesión 17/05

### Fase 0.5 — Graph Intelligence ✅ COMPLETADO 19/05/2026
- **RD 1413/2005** ingestado (capitalización desempleo, 4 preceptos + embeddings + relaciones)
- **Louvain Community Detection:** 517 comunidades calculadas, `communityId` en cada Precepto
- **Relaciones cross-ley:** `RELACIONADO_CON` (Art. 262, 296 TRLGSS) + `DESARROLLA` (RD 625/1985)
- **Hybrid search nativa:** `_hybrid_search_neo4j()` implementado (Vector + Fulltext + RRF)
- **Multi-hop few-shots:** 5 patrones Cypher añadidos al system prompt de Chandra
- **Catálogo actualizado:** v17.6 (108 leyes)
- **Corrección:** RD 1413/2005 erróneamente descartado → recuperado e ingestado
- **Formato RD 1413/2005 corregido:** props `sufijo`, `ordinal`, `fecha_vigencia` alineadas con pipeline v17
- **⚠️ PENDIENTE post-Fase 0.5:** Fallback BOE HTML en `get_law_text_block` (API 404 → scrape `boe.es/buscar/act.php?id=`)

### Fase 1 — Anti-alucinación Chandra
- **Auto-RAG pre-respuesta:** inyectar trampas relevantes a Neo4j ANTES del primer token
- **Chain-of-Verification (CoVe):** revisar y corregir cada respuesta antes de mostrarla
- **Few-shot calibration:** 3-5 ejemplos en `CHANDRA_SYSTEM_PROMPT`
- **4 manos nuevas:** `flashcards_anki`, `mermaid_validator`, `simulacro_test`, `resumir_nota`
- **Eval set:** 50-100 ejemplos para medir tasa de alucinación pre/post

### Fase 2 — Multi-IA + Robustez
- **LiteLLM router:** `Mistral → DeepSeek → Cohere → Groq` con Exponential Backoff
- **BYOK ampliado:** 6+ providers (Anthropic, OpenAI, Mistral, Cohere, Groq, DeepSeek, Gemini)
- **Comando `/byok <provider> <key>`** sin abrir settings
- **Switch puntual `@modelo`** en mensaje (ej. `@groq-llama-70b ¿pregunta?`)

### Fase 3 — BMO Agentes + Workflows + Comandos
- **Estructura `.bmo/agents/`:** chandra, indexador_pdf, conversor_doc, cartografo_zettel, validador_boe, jurista
- **Comandos:** `/agent`, `/workflow`, `/byok`, `/mcp`, `@modelo`, `*tool`
- **Workflows:** ingest_simulacro, nuevo_tema, auditar_vault, publicar_release
- **MCP proxy:** cliente genérico para servidores MCP locales

### Fase 4 — Empaquetable (.exe para producción)
- Excluir `DATOS_ACADEMIA/` y materiales PII de release
- Sandbox tools (Pyodide para Python; whitelist para fetch_url y exec_terminal)
- Licencia clara: uso personal materiales propios = lícito GDPR/LPI
- Instalador WSL → Windows
- Vault publicable nuevo desde cero (BOVEDA_OPOS_LIMPIA_2026)

### Las 4 opciones que tienes hoy (17/05/2026)

| Opción | Descripción | Por qué empezar aquí |
|--------|-------------|----------------------|
| **A) Fase 1** | Anti-alucinación Chandra (Auto-RAG + CoVe + 4 manos) | Mejor calidad de respuestas — máximo impacto para la hija usando BMO |
| **B) Fase 2** | LiteLLM router multi-IA + BYOK ampliado | Más robustez ante caídas de Mistral; permite probar Groq/DeepSeek/Cohere |
| **C) Fase 3** | BMO agentes + workflows + comandos | Mayor flexibilidad de uso; agentes especializados (indexador, cartógrafo…) |
| **D) Fase 4** | Empaquetar `.exe` para la hija | Entrega inmediata; aprovecha el estado actual sin más cambios |

---

## 14. 4 Ideas Arquitectónicas (aprobadas 19/05/2026)

> Fuente: `academias/1_casos_recientes_2026_DM/criticas18__03_26/18_05_2026_IDEAS_GROQ_DSEEK.md`

### 14.1 Arquitectura Híbrida (Vector + Graph + Fulltext)

**Estado:** ✅ Parcialmente implementado. Neo4j tiene los 3 indexes. Falta `hybrid_search()` unificado (~50 LOC).

| Componente | Estado | Dónde |
|---|---|---|
| Vector HNSW 1024d | ✅ Operativo | Neo4j `precepto_embedding` |
| Fulltext spanish | ✅ Operativo | Neo4j `precepto_fulltext` |
| Graph traversal | ✅ Operativo | Cypher vía `consultar_neo4j` |
| Pipeline unificado | ❌ Pendiente | Endpoint FastAPI → combine+rerank |
| Qdrant | ❌ Descartado | Legacy 25K puntos sin sincronizar |

### 14.2 Tools y Plugins (Chandra + BMO)

**Estado:** ✅ Implementado. Chandra 7 manos + BMO conectado vía Mistral API.

| Tool | Estado | Función |
|---|---|---|
| `tavily_search` | ✅ | Búsqueda web jurisprudencia |
| `search_boe` | ✅ | Búsqueda BOE consolidada |
| `get_law_text_block` | ✅ | Texto exacto artículo BOE |
| `consultar_neo4j` | ✅ | Cypher directo a Neo4j |
| `calcular_ss` | ✅ | Calculadoras SS/IMV |
| `buscar_vault` | ✅ | Búsqueda Obsidian vault |
| `escribir_vault` | ✅ | Crear notas vault |

**Conexión BMO:** `BMO → Mistral API key → /opos/v1 (puerto 8080) → Chandra → Neo4j`

### 14.3 App Concepto ("Segundo Cerebro")

**Estado:** 🟡 Diseñado. Frontend React 19 (17 vistas operativas) + Tauri Desktop App planificado.

- Web nativa: React 19 + Vite + Tailwind → operativa
- Vault Obsidian: bóveda OPOS en `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/` (pruebas)
- Tauri .exe: planificado Fase 4 (empaquetado + BYOV)
- Multi-tenant Neo4j: diseñado (filtro `propietario` por usuario)

### 14.4 GDS Louvain Community Detection

**Estado:** ✅ Implementado 19/05/2026 (via Python, no GDS plugin).

| Aspecto | Detalle |
|---|---|
| **Algoritmo** | Louvain (python-louvain + networkx) |
| **Resultado** | 517 comunidades sobre 6.683 preceptos |
| **Propiedad** | `communityId` en cada `:Precepto` |
| **Index** | `precepto_community` RANGE |
| **Mapa** | `backend/data/louvain_communities.json` |

**Usos aprobados:**
- Resúmenes por comunidad (generados por Cascade)
- Flashcards agrupadas por cluster temático
- Mapas mentales / esquemas por comunidad
- Blueprints y checklists por tema del temario
- Tracking progreso usuario por comunidad
- Clustering personajes serie turca por relaciones narrativas

---

## 15. Sesión 19/05/2026 — Cambios ejecutados

1. **Ingesta RD 1413/2005** (BOE-A-2005-20552): 4 preceptos + embeddings + 3 relaciones cross-ley
2. **Louvain implementado:** 517 comunidades, `communityId` persistido, JSON exportado
3. **VISION_360 actualizado:** secciones 12.9-12.13, 14.1-14.4, Fase 0.5
4. **Catálogo v17.6:** 108 leyes total
5. **Correcciones conceptuales:**
   - BMO SÍ conecta a Neo4j vía Chandra mano #4
   - PII = materiales de academias, NO leyes públicas
   - Qdrant NO necesario para búsqueda híbrida (Neo4j lo hace todo)
   - Docker Compose ya tiene 4 servicios (Qdrant, Postgres, Backend, Neo4j)
   - Bóveda OPOS ≠ OPOS_GEMINI_1 (repo dev)

---

## 16. Neo4j Graphify — Segunda instancia aislada (19/05/2026)

**Propósito:** Memoria para cliente final, completamente aislada del Neo4j SS actual.

### Configuración Docker

| Propiedad | Neo4j SS (actual) | Neo4j Graphify (nuevo) |
|-----------|------------------|----------------------|
| Servicio | `neo4j` | `neo4j-graphify` |
| Contenedor | `opositaia-neo4j` | `opositaia-neo4j-graphify` |
| Imagen | `neo4j:2026-community` | `neo4j:2026-community` |
| Puertos host | 7474 (HTTP), 7687 (Bolt) | **7475 (HTTP), 7688 (Bolt)** |
| Password | `opositaia2026` | `nina12ya` |
| Volumes | `opos_gemini_1_neo4j_*` | `opos_gemini_1_neo4j_graphify_*` |
| Network | `opositaia-network` | `opositaia-network` |

### Volumes Docker

- `opos_gemini_1_neo4j_graphify_data` — datos del grafo
- `opos_gemini_1_neo4j_graphify_logs`
- `opos_gemini_1_neo4j_graphify_import`
- `opos_gemini_1_neo4j_graphify_plugins`

### Credenciales de conexión (Python)

```python
NEO4J_URI = "bolt://localhost:7688"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "nina12ya"
```

### Browser Neo4j

- URL: http://localhost:7475
- Usuario: `neo4j`
- Password: `nina12ya`

### Comandos Docker

```bash
# Levantar solo Graphify
docker-compose up -d neo4j-graphify

# Ver logs
docker-compose logs neo4j-graphify

# Parar
docker-compose stop neo4j-graphify

# Reiniciar
docker-compose restart neo4j-graphify
```

### Archivo de configuración

`/home/spas/OPOS_GEMINI_1/docker-compose.yml` — servicio `neo4j-graphify` añadido 19/05/2026

### ⚠️ Problema Browser Web con múltiples instancias

El browser web de Neo4j tiene conflictos con múltiples instancias en localhost (localStorage/cache). Solución: usar **Neo4j Desktop** (app nativa) para conectar a `bolt://localhost:7688`.

---
