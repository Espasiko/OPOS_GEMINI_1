# 🗺️ BORRADOR v2 — AUDITORÍA COMPLETA Y PLAN MAESTRO

**Fecha:** 15/05/2026 17:55 UTC+2 — **Versión:** 2.0 (verificada runtime)
**Estado:** Borrador para revisión humana — NO ejecutar nada todavía
**Objetivo:** Reorientar el proyecto OPOSITAIA tras 2 meses de evolución acelerada

> ## ⚡ CORRECCIONES TRAS VERIFICACIÓN RUNTIME + MCP MEMORY (15/05 18:20)
>
> - ✅ **Bug Neo4j ARREGLADO** — `case_schema_builder.py:218` ya usa `MATCH (p:Precepto)`. La auditoría de marzo (`AUDITORIA_IMPLEMENTADO_VS_DISEÑO`) está obsoleta en este punto.
> - ✅ **Neo4j healthy** — 103 leyes + 6.334 preceptos + 359 `EXCEPCION_A` (100% `verificado_humano=true`).
> - ✅ **Calculadoras NO son tan monstruosas** — 20 funciones top-level en SS (2.457 LOC) + 40 en AGE. Refactor real: **2-3 horas con tests** (según `Plan_Refactor_Calculadoras_Pendiente_29_04_2026` MCP).
> - ✅ **Intento refactor 29/04 FALLÓ por conflicto nombres** `calculos_ss.py` ↔ paquete `calculos_ss/`. **Estrategia segura:** usar nombre `prestaciones_ss/` o renombrar `calculos_ss.py → calculos_ss_base.py`.
> - ✅ **165 archivos sueltos en raíz** (más que los 149 reportados, pero muchos son memoria útil).
> - ✅ **Plan Kimi/Antigravity ya consolidado** en `10_05_2026_IDEAS_KIMI.MD` con fases 1→2→4→3→5 — **reutilizable**.
> - ✅ **Plan_Chandra_v2_03_05_2026** ya documentado en MCP Memory con 10 best practices BP1-BP10, decisiones Q1-Q4 pendientes.
> - ✅ **Modelo de negocio 3 SKUs confirmado** (`Modelo_Negocio_3_SKUs_28_04_2026` MCP): Web App + Vault Premium .zip+.exe + API B2B.
> - ✅ **LiteLLM ya planificado** en `implementation_plan.md.resolved` (Mistral → Groq → Gemini con Exponential Backoff).
> - ✅ **184 trampas verificadas BOE** confirmadas en MCP `Trampas_Verificadas_184_19_04_26` + 2 lotes de verificación 18-19/04.
> - ✅ **Patrones narrativos genéricos = 9** (no solo 3) catálogo en entidad MCP `Patrones_Narrativos_DM_9` (nombre legacy de la entidad, contenido abstracto).
> - ✅ **PLAN_MAESTRO_CASOS_SIMULACROS v4** = ~479 mecánicas + ~752 preguntas (uso interno autor, anonimizado).
> - ⚠️ **MISTRAL_URL obsoleta** en `.env.backend` (proxy VPS muerto, código la ignora pero `/opos/health` la sigue reportando).
> - 🚫 **Copilot DESCARTADO** por mala licencia. El interfaz único en Obsidian es **BMO Chandra Edition** (fork MIT).
>
> ### ⚠️ ACLARACIÓN sobre fuentes de información:
>
> Las entidades como `Plan_Chandra_v2_03_05_2026`, `Modelo_Negocio_3_SKUs_28_04_2026`, `Plan_Refactor_Calculadoras_Pendiente_29_04_2026` **NO son archivos .md en disco**. Son **nodos del grafo MCP Memory** (servidor `@modelcontextprotocol/server-memory`). Se consultan con `mcp4_open_nodes` o `mcp4_search_nodes`.
>
> Los **archivos .md reales** en disco son: `10_05_2026_IDEAS_KIMI.MD`, `14_05_2026_MEMORIA_SESION_ANTI.md`, `21_04_2026_PLAN_SERIE_TURCA.md`, `20_04_26_PLAN_WIKI_NEXO_v5_1.md`, `docs/prd.md`, `docs/product-brief.md`, `docs/project-overview.md`, `FLUJO_24_03.md`, más un Plan Maestro de Simulacros v4 que vive en una carpeta privada del autor (uso interno, gitignored). Esa carpeta NUNCA se cita por nombre completo.
>
> ### 📚 DOCUMENTO COMPAÑERO:
>
> `/home/spas/OPOS_GEMINI_1/15_05_2026_VISION_360_OPOSITAIA.md` — **Visión 360º** con TODAS las vertientes (estrategias COSMIC + NEXO + Serie Turca + 3 Capas Wiki + V14.5 + Muro Abstracción), las 7 capas del stack, los 3 SKUs, los 9 patrones narrativos genéricos, qué falta priorizado y todas las fuentes (archivos + entidades MCP).

---

## 0. RESUMEN EJECUTIVO (TL;DR)

Tienes un proyecto **muy avanzado** que ya tiene **plan consolidado** (`10_05_2026_IDEAS_KIMI.MD` + `IDEAS_MAESTRAS_OPOSITAIA_2026.md.resolved`). El núcleo funciona:

- ✅ **Chandra** (agente legal con 7 tools) → operativo en BMO Obsidian (puerto 8080)
- ✅ **Neo4j** verificado en runtime (103 leyes, 6.334 preceptos, 359 excepciones bidireccionales)
- ✅ **184 trampas verificadas** en el vault (18 categorías A-R)
- ✅ **Constantes 2026** verificadas BOE corte 04/03/2026
- ✅ **Fork BMO Chandra Edition** con multi-chat, sidebar, header editable, persistencia .md
- ✅ **Calculadoras SS** 2.457 LOC con 20 funciones públicas (refactor abordable)
- ✅ **52 trampas catalogadas** en `backend/trampas/AUDITORIA_04_05_2026.md` (TPL, TCM, TCT…)
- ✅ **3 patrones narrativos genéricos** identificados (A, B, C) en catálogo abstracto interno
- ✅ **Muro de Abstracción + PII rules** definidos en `AUDITORIA_04_05` §0.1

Lo que **falta o está fragmentado**:

- ❌ **Refactor calculadoras** SS+AGE en paquete modular (≈1-2 días)
- ❌ **LiteLLM enrutador** (CONFIRMADO necesario: 11+ providers en `.env`)
- ❌ **PDF support en BMO** + **tool calling UI visible**
- ❌ **Más herramientas** (file ops vault, exec código, fetch web, conversores PDF→MD, MCPs)
- ❌ **3 bugs blueprints S11, S16, S10, S12** detectados 04/05 (5 min fix cada uno)
- ❌ **Patrones narrativos A y B** en `CaseSchemaBuilder` (solo genera C)
- ❌ **52 trampas** sin cargar a Neo4j (`seed_trampas_neo4j.py` planeado)
- ❌ **Análisis sistemático** de simulacros nuevos del Drive
- ❌ **Productos derivados COSMIC** (vaults para abogados, estudiantes, AGE, autónomos)

**Decisión clave:** Seguir el orden ya consolidado en Kimi: **Fase 1 (limpieza P1) → 2 (Chandra+LiteLLM) → 4 (Templates AI) → 3 (Fork BMO UI) → 5 (Repoblado)**.

---

## 1. INVENTARIO DEL PROYECTO (verificado runtime 15/05)

### 1.1 Backend (`/home/spas/OPOS_GEMINI_1/`)

| Componente | Estado | Notas |
|-----------|--------|-------|
| **Chandra agent** (`backend/agents/chandra_tools.py`) | ✅ Operativo | 7 tools, 631 LOC |
| **Backend FastAPI** (`backend/routers/opos_chat.py`) | ✅ Operativo | Puerto 8080 |
| **Calculadoras SS** (`calculos_ss_extended.py`) | ⚠️ Refactor abordable | 2.457 LOC, **20 funciones públicas** |
| **Calculadoras AGE** (`calculadora_age.py`) | ⚠️ Refactor abordable | **40 funciones públicas** |
| **constantes_2026.py** | ✅ Correctas | Verificadas BOE 04/03/2026 |
| **Blueprints V14** (10 activos: bp_s02-s16) | ⚠️ 4 bugs detectados 04/05 | S11, S16, S10, S12 (fix 5 min c/u) |
| **CaseSchemaBuilder** (586 líneas) | ✅ Bug Neo4j ARREGLADO | Usa `MATCH (p:Precepto)` correcto |
| **Agentes YAML** (11 en `opos-agents/agents/`) | ✅ Operativo | redactor_v14, examiner, validator… |
| **mcp_gateway.py** | ✅ Operativo | Endpoint `/mcp/vault/write` |
| **Neo4j** (Docker local) | ✅ HEALTHY (runtime) | 103 Ley + 6.334 Precepto + **359 EXCEPCION_A 100% verificadas** |
| **Qdrant** | ✅ Operativo | 25.273 puntos FULL_XML |
| **Frontend React** (17 vistas) | ⚠️ Mezclado | localStorage en vez de Postgres |

### 1.2 Vault Obsidian (`/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/`)

| Sección | Estado | Notas |
|---------|--------|-------|
| **wiki/trampas/** | ✅ 184 trampas | 18 categorías (A-Q + CA, N_AUTO, R) |
| **wiki/trampas/_INDICE.md** | ✅ Curado | 53 errores corregidos en abril 2026 |
| **wiki/_INDICE_EXCEPCIONES.md** | ✅ Generado | 359 excepciones Neo4j → MD |
| **wiki/esquemas_con_mapa/** | ✅ 17 archivos | Mapas verificados con Mermaid |
| **wiki/calculadoras_python/** | ⚠️ Casi vacía | Solo `pdf_processor.py` |
| **wiki/temario/** | ⚠️ Casi vacía | Solo 1 carpeta RD_1539_2003 |
| **BMO/Profiles/Chandra_Opos.md** | ✅ Operativo | Perfil principal |
| **Plugins instalados (32)** | ✅ Robusto | BMO, Dataview, Excalidraw, Templater, Mind-map, Spaced-Repetition, Obsidian-to-Anki, MCP-tools, Smart-connections, Execute-code, Find-unlinked-files, Linter, Local-REST-API |

### 1.3 Plugin BMO Fork (`/home/spas/obsidian-bmo-chatbot-plus/`)

| Feature | Estado |
|---------|--------|
| Multi-chat sidebar | ✅ Implementado |
| Header editable | ✅ Implementado |
| Persistencia `.md` en BMO/History/ | ✅ Implementado |
| **PDF support** | ❌ Pendiente |
| **Image multimodal** | ❌ Pendiente |
| **Tool calling visible UI** | ❌ Pendiente |
| **LiteLLM enrutador** | ❌ Pendiente |
| Autocompletado `/`, `@`, `*` | ❌ Pendiente |
| Selector modelo inline | ❌ Pendiente |

### 1.4 Documentos clave (últimas 2 semanas)

| Doc | Importancia | Estado |
|-----|-------------|--------|
| `01_05_26MEMORIA_FIN_CHANDRA_FUNCIONAL.md` | 🔥 Fuente verdad | ✅ |
| `10_05_2026_IDEAS_KIMI.MD` | 🔥 Plan consolidado | ✅ |
| `14_05_2026_MEMORIA_SESION_ANTI.md` | 🔥 Hito Excepciones | ✅ |
| `15_05_2026_clasificacion_calculos_gemini.md` | 🔥 Catálogo cálculos | ✅ |
| `docs/AUDITORIA_IMPLEMENTADO_VS_DISEÑO_17_03_26.md` | 🔥 Brownfield audit | ✅ Rev 5.0 (12/05) |
| `FLUJO_24_03.md` | 📜 Histórico | ✅ |
| `docs/project-overview.md` | 🔥 Overview maestro | ✅ Rev 01/05 |
| Catálogos trampas YAML (3 archivos) | 🔥 Cerebro de mecánicas anonimizadas | ✅ |
| `1_CATALOGO_TRAMPAS_DEFINITIVO_C1_SS.md` | ⚠️ Sin integrar | 423 líneas, recién extraído |
| `29_03_GROK_TRAMPAS_CALCULADORAS_TEMAS.md` | ⚠️ Sin integrar | Trampas + fórmulas Python |

---

## 2. PROBLEMAS IDENTIFICADOS

### 🔴 Críticos (bloquean evolución)

1. ~~**Bug Neo4j v17 schema mismatch**~~ — ✅ **ARREGLADO**. Verificado `case_schema_builder.py:218` ya usa `MATCH (p:Precepto)`.
2. **Calculadoras monolíticas** — `calculos_ss_extended.py` 2.457 LOC pero solo **20 funciones públicas**. Refactor a paquete modular `calculadoras/{prestaciones, recaudacion, encuadramiento, jubilacion, ...}/` en **1-2 días con tests**.
3. **Multi-IA roto en BMO** — solo Mistral funciona. Necesario LiteLLM (confirmado: 11+ providers en `.env`).
4. **4 bugs blueprints V14** (S11, S16, S10, S12) — fixes de 5 min c/u (sección 6.1 `AUDITORIA_04_05_2026.md`).

### 🟡 Importantes (bloquean productos)

5. **PII residual** — trampas con nombres propios y/o empresas reconocibles que pudieran filtrar fuentes. Imposible publicar/vender hasta filtrar. Regla de oro en `AUDITORIA_04_05` §0.1.
6. **Catálogo trampas fragmentado en 5 fuentes — propuesta de unificación:**
   - 🎯 **Fuente de verdad:** `wiki/trampas/` (184 archivos MD verificados con frontmatter)
   - 🤖 **Catálogo de mecánicas abstractas:** 52 IDs en `backend/trampas/AUDITORIA_04_05_2026.md` §4 (TPL/TCM/TCT/TRQ/TEC/TCP/TSE/TAR/TIN)
   - 📦 **Auto-generar** `wiki/trampas/_MASTER.yaml` único para consumo backend
   - 🗑️ **Archivar** los 4 YAMLs obsoletos (`catalogo_trampas*.yaml`, `trampas_unificadas_v2`, `1_CATALOGO_DEFINITIVO_C1_SS.md`)
7. **52 trampas sin cargar a Neo4j** — script `seed_trampas_neo4j.py` planeado en §5.4 de la auditoría, no ejecutado.
8. **`CaseSchemaBuilder` solo genera Patrón C** (empresa-eje). Faltan A (cronología vital) y B (bloques sin conexión).
9. **165 archivos sueltos en raíz** del repo — incluye 30+ memorias .md útiles que NO se deben borrar.
10. **localStorage en frontend** — Postgres ya existe pero sin usar.
11. **Settings page placeholder** — BYOK sin implementar.

### 🟢 Mejoras deseables (productos derivados)

12. Falta soporte PDF/imagen en BMO (visible Fase 3 de Kimi).
13. Falta tool calling UI visible (como ChatGPT).
14. Falta LiteLLM enrutador multi-IA (CONFIRMADO necesario por user).
15. Faltan herramientas extra Chandra: 4 nuevas en Kimi Fase 2.A (`flashcards_anki`, `mermaid`, `simulacro_test`, `resumir_nota`) + las nuevas que propones (PDF, exec, file ops vault, fetch URL).
16. Falta sistema YAML de skills/agents/workflows (Chandra_Tribunal, Chandra_Resumen, etc.).

---

## 3. PRODUCTOS DERIVADOS COSMIC (visión)

> Una sola fuente de verdad → muchas presentaciones por público
> Confirmado en `IDEAS_MAESTRAS_OPOSITAIA_2026.md` §3 y `product-brief.md` (modelo Freemium BYOK)

| Producto | Público | Vault sugerido | Reutilización | Precio sugerido |
|----------|---------|----------------|--------------|-----------------|
| **OpositAIA SS C1** (actual) | Opositores SS Admin | `BOVEDA_OPOS` | 100% — origen | Trial €1/3d + Pro €69/mes |
| **OpositAIA SS A2 (Gestión)** | Opositores SS Gestión | `BOVEDA_GESTION` | 80% — solo cambia profundidad | €69/mes |
| **OpositAIA AGE C1/C2/PI** | Opositores AGE | `BOVEDA_AGE` | 60% — TREBEP, LPAC, LRJSP, LCSP | €69/mes |
| **JuristaAIA** | Abogados / despachos | `VAULT_LEGAL_PRO` | 50% — Neo4j + jurisprudencia + tools, sin trampas | €19,99-49/mes |
| **EstudiantesDerecho** | Universidad | `VAULT_DERECHO` | 40% — temarios LO + casos prácticos | €9,99/mes |
| **AutónomoAIA** (de §9 IDEAS_MAESTRAS) | Autónomos RETA | `VAULT_AUTONOMO` | 30% — Predicción cash-flow + calculadoras RETA | €19,99/mes |
| **EscritorAIA** (de §7 PRD-IDEAS) | Novelistas | `VAULT_ESCRITOR` | 10% — solo Chandra + plantillas narrativas | €9,99/mes |

**Implicación arquitectónica:** El **backend Chandra** debe ser **agnóstico al vault** — basta cambiar el path de Obsidian REST API y el corpus de trampas/blueprints.

**Modelo Freemium BYOK confirmado:**
- **Gratis:** Límite diario de consultas
- **Premium:** 9,99€-19,99€ (según producto)
- **Premium BYOK:** El usuario aporta su propia clave de API → suscripción reducida

---

## 4. PLAN MAESTRO PROPUESTO — Alineado con `IDEAS_KIMI.MD` (orden 1→2→4→3→5)

> Cada fase tiene un único objetivo y entregable claro. **No abrir fase nueva sin cerrar la anterior.**
> Estimación realista total: **~5-6 semanas** (productos derivados aparte)

### 🔧 FASE 1 — Limpieza, P1 fixes y consolidación (3-4 días)

**Objetivo:** dejar el repo coherente y arreglar los 3 bugs P1 detectados 04/05.

| Tarea | Archivo / Acción | Tiempo |
|-------|------------------|--------|
| 1.1 ~~Fix bug Neo4j~~ | ✅ YA HECHO | 0 |
| 1.2 **Fix BP-S11** eliminar "19 semanas", añadir `Art. 48 ET` + `Art. 177 TRLGSS` | `backend/v14/blueprints/bp_s11_*.py` | 5 min |
| 1.3 **Fix BP-S16** separar PNC IPP de IMV, añadir `Art. 11 Ley 19/2021` | `backend/v14/blueprints/bp_s16_*.py` | 10 min |
| 1.4 **Fix BP-S10** añadir `Art. 174` + `Art. 196 TRLGSS` | `backend/v14/blueprints/bp_s10_*.py` | 5 min |
| 1.5 **Fix BP-S12** añadir `Art. 205 TRLGSS` | `backend/v14/blueprints/bp_s12_*.py` | 5 min |
| 1.6 **REGLA 8 anti-alucinación** en `redactor_v14.yaml` (no inventar apartados) | `opos-agents/agents/redactor_v14.yaml` | 5 min |
| 1.7 **Unificar catálogo trampas**: `wiki/trampas/` como verdad + script auto-genera `_MASTER.yaml` para backend | `backend/scripts/generate_trampas_master.py` (nuevo) | 1 h |
| 1.8 Archivar YAMLs obsoletos (`catalogo_trampas*.yaml`, `trampas_unificadas_v2_CURADO.yaml`, `1_CATALOGO_DEFINITIVO_C1_SS.md`) | `mv → academias/_archivo/` | 5 min |
| 1.9 **Filtrar PII** (regex de nombres propios + empresas + revisión muestra humana) | script + Muro Abstracción (§0.1 AUDITORIA_04_05) | 2-3 h |
| 1.10 Mover memorias antiguas a `docs/memorias/` (conservar 30+ MDs útiles) | bulk mv | 30 min |
| 1.11 Limpiar `.env.backend` (`MISTRAL_URL` obsoleta) | comentarios + ordenar | 5 min |

**Entregable:** repo navegable + un solo catálogo trampas + 4 blueprints corregidos + REGLA 8 activa.

---

### 🛠️ FASE 2 — Backend robusto + LiteLLM + Chandra mejorado (5-7 días)

> Alineado con **Kimi §FASE 2** (8-11 manos + CoVe + Auto-RAG + Few-shot)

**Objetivo:** que el backend sea mantenible, multi-IA y con anti-alucinación reforzada.

| Tarea | Detalle | Tiempo |
|-------|---------|--------|
| 2.1 **Refactor calculadoras** SS → paquete modular | `backend/calculators/{prestaciones, recaudacion, encuadramiento, jubilacion, it, ip, ms, desempleo}/` (20 funciones a separar) | 1 día |
| 2.2 Refactor calculadoras AGE → paquete modular | `backend/calculators/age/{lpac, trebep, transversales}/` (40 funciones) | 1 día |
| 2.3 **Tests pytest** mínimos por módulo | 1 test por función pública = 60 tests | 1 día |
| 2.4 **LiteLLM enrutador** `backend/agents/llm_router.py` | Fallback Mistral → DeepSeek → Cohere → Groq (Gemini DESCARTADO según `IDEAS_MAESTRAS`) | 1 h |
| 2.5 **Chain-of-Verification (CoVe)** en `opos_chat.py` | Hook post-respuesta: 3 preguntas internas (¿artículo existe? ¿cuantía correcta? ¿fecha aplica corte?) → verificar → devolver. Reduce alucinaciones ~40% | 2-3 h |
| 2.6 **Auto-RAG pre-respuesta** | Antes de Mistral, ejecutar `buscar_vault(carpeta='wiki/trampas')` con la query y inyectar las 3 trampas relevantes | 1 h |
| 2.7 **Few-shot calibración** en `CHANDRA_SYSTEM_PROMPT` | 3 ejemplos de `Para_Dudas.md` (IT 4-15, jubilación 66a+10m con 37 años, IPT vs IPA) | 30 min |
| 2.8 **Nuevas 4 manos Chandra** (Kimi §2.A): `flashcards_anki`, `mermaid`, `simulacro_test`, `resumir_nota` | `backend/agents/chandra_tools.py` | 1-2 días |
| 2.9 **Prose Validator fix** P2.1: extraer art_id citados → verificar contra `articulos_obligatorios` ∪ `contexto_legal` (detección TAR-01/02/03) | `backend/v14/prose_validator.py` | 30 min |
| 2.10 **Patrón narrativo A/B/C** en `CaseSchemaBuilder` + 3 few-shots en redactor | `backend/v14/case_schema_builder.py` + `redactor_v14.yaml` | 1 h |

**Entregable:** backend modular + LiteLLM fallback + CoVe + Auto-RAG + 11 manos Chandra + 3 patrones narrativos.

---

### 🪛 FASE 4 — Templates AI + nuevas tools utilitarias (3-4 días)

> Alineado con **Kimi §FASE 4** (templates) — orden Kimi: hacer **antes** del fork BMO

**Objetivo:** crear las plantillas Templater + ampliar Chandra con tools de file/PDF/web.

**4.A Templates Templater + Chandra (Kimi §4):**

| Template | Uso |
|----------|-----|
| `T1_Caso_Practico.md` | input tema → hechos → análisis BOE → resultado + cita |
| `T2_Simulacro_10.md` | usa `simulacro_test` |
| `T3_Flashcards_Anki.md` | usa `flashcards_anki` |
| `T4_Mermaid_Concepto.md` | usa `mermaid` |
| `T5_Mapa_Mental_Markmap.md` | bloque markmap + plugin mind-map |
| `T6_Esquema_Tema.md` | CoT: bullets → resumen → trampas |

**4.B Tools utilitarias adicionales (lo que pediste):**

| # | Herramienta | Para qué |
|---|-------------|---------|
| 12 | `extraer_texto_pdf` | PDF → texto via pymupdf/pdfplumber |
| 13 | `convertir_a_md` | PDF/DOCX/HTML → Markdown limpio con frontmatter |
| 14 | `fetch_url` | Descargar y limpiar HTML de URL externa (no Tavily) |
| 15 | `ejecutar_codigo_py` | Sandbox para Python (vía plugin `execute-code`) |
| 16 | `mover_vault` | mv archivo entre carpetas del vault |
| 17 | `borrar_vault` | rm con confirmación + papelera lógica |
| 18 | `crear_carpeta_vault` | mkdir |
| 19 | `indexar_vault` | reindexar Smart Connections / Omnisearch |
| 20 | `consultar_mcp` | invocar cualquier MCP server registrado (genérico) |

**Entregable:** 6 plantillas operativas + Chandra con ~20 manos.

---

### 🎨 FASE 3 — Fork BMO Chandra Edition (7-10 días)

> Alineado con **Kimi §FASE 3** — orden Kimi: hacer **DESPUÉS** de tools/templates estables

**Objetivo:** UI a la altura de las nuevas tools, publicable como `obsidian-bmo-chandra-edition`.

| Tarea | Detalle |
|-------|---------|
| 3.1 **Tool calling UI visible** | Streaming de eventos `tool_call`/`tool_result` con bloques colapsables tipo ChatGPT |
| 3.2 **Soporte PDF** | `ReferenceCurrentNote.ts` detecta `.pdf` activo + llama `extraer_texto_pdf` |
| 3.3 **Imagen multimodal** | base64 + envío como `image_url` (Mistral Pixtral / Claude / GPT-4V) |
| 3.4 **Autocompletado `/comando`** | `/flashcard`, `/simulacro`, `/caso_practico`, `/mermaid`, `/examen` |
| 3.5 **Autocompletado `@perfil`** | carga perfil al vuelo (`@chandra_opos`, `@examinador`, `@resumidor`) |
| 3.6 **Autocompletado `*ejecutar`** | pasa bloque python a `execute-code` y devuelve output |
| 3.7 **Selector modelo inline** | Dropdown abajo-izquierda — cambia solo modelo (no perfil) — conecta con LiteLLM |
| 3.8 **Context toggles** | botones `[Nota]` `[Vault]` `[Solo prompt]` junto al input |

**Entregable:** Plugin publicable como `obsidian-bmo-chandra-edition` (MIT).

---

### 📚 FASE 5 — Repoblado del vault + Neo4j taxonomía trampas (7-10 días)

> Alineado con **Kimi §FASE 5** + `AUDITORIA_04_05_2026.md` §5.4 (carga Neo4j)

**Objetivo:** vault completo, sin PII, listo como semilla COSMIC.

| Tarea | Detalle |
|-------|---------|
| 5.1 **Seed Trampas Neo4j** | Cargar los 52 IDs de `AUDITORIA_04_05` §4 (TPL/TCM/TCT…) como nodos `:Trampa` (sin contenido externo) — script `seed_trampas_neo4j.py` |
| 5.2 **Sync blueprints ↔ Neo4j** | `scripts/sync_blueprints_to_neo4j.py` — relaciones `:APLICA_EN` |
| 5.3 **Integrar trampas mayo** (`1_CATALOGO_DEFINITIVO_C1_SS.md`) en `wiki/trampas/` | Convertir cada A1-A5, B1-B6… a archivo MD individual con frontmatter, sin PII |
| 5.4 **Integrar fórmulas Grok** (`29_03_GROK_TRAMPAS_CALCULADORAS_TEMAS.md`) | Validar fórmulas Python → tests → integrar en calculadoras modulares |
| 5.5 **Procesar simulacros del Drive** (cuando los bajes) | OCR + extracción patrones genéricos A/B/C + 52 mecánicas, anonimizando nombres y empresas → wiki |
| 5.6 **`wiki/temario/` completo** (13 temas C1) | Troceados con corte 04/03/2026 + Muro Abstracción aplicado |
| 5.7 **`wiki/preceptos/`** enlazados a Neo4j | YAML con `neo4j_id`, `ley`, `vigencia`, `materias` |
| 5.8 **`CasoEntrenamiento` validados** generados internamente | Pipeline multi-IA cross-check (Mistral + DeepSeek + Cohere) → supervisión humana → `validado=true` |
| 5.9 **Etiquetado `:USA_TRAMPA` + `:CITA_PRECEPTO`** | Sobre casos validados |
| 5.10 **Relaciones `:CONFUNDIBLE_CON`** | Derivar de trampas + revisión humana |
| 5.11 **Sistema skills/agentes/workflows YAML** | `.bmo/skills/*.yaml`, `.bmo/agents/*.yaml`, `.bmo/workflows/*.yaml` |

**Entregable:** vault BOVEDA_OPOS completo, sin PII, Neo4j con taxonomía trampas + casos validados, listo como semilla COSMIC.

---

### 🚀 FASE 6 — Productos derivados COSMIC (variable, NUNCA antes de 1-5 cerradas)

**Objetivo:** clonar la fórmula a otros públicos.

| Producto | Esfuerzo |
|----------|----------|
| Vault SS A2 (Gestión) | 2-3 días — re-etiquetar trampas, ajustar profundidad |
| Vault AGE C1/C2/PI | 1-2 semanas — añadir LPAC, LRJSP, TREBEP, LCSP |
| JuristaAIA (abogados) | 2-3 semanas — quitar trampas didácticas, añadir jurisprudencia + plantillas demanda |
| EstudiantesDerecho | 1 semana — temarios universidad |
| **AutónomoAIA** (cash-flow RETA) | 2-3 semanas — Prophet/NeuralProphet + dashboard Streamlit + calculadoras RETA |
| **EscritorAIA** | 1 semana — solo Chandra + plantillas narrativas + RAG sobre borradores |
| **Tauri Desktop App** (chandra.exe) | 2-3 semanas — Tauri + Sidecar + frontend React empaquetado |

---

## 5. ARQUITECTURA SUGERIDA POST-REFACTOR

```
OpositAIA/
├── backend/
│   ├── routers/
│   │   ├── opos_chat.py           # Chat OpenAI-compatible (BMO)
│   │   ├── ai_functions.py        # Funciones IA (mapas, casos, …)
│   │   ├── mcp_gateway.py         # Vault REST API gateway
│   │   └── boe.py                 # API BOE
│   ├── agents/
│   │   ├── chandra_tools.py       # 20 manos
│   │   ├── llm_router.py          # NUEVO: LiteLLM fallback
│   │   ├── verification_agents.py # CoVe + 7 dimensiones
│   │   └── …
│   ├── calculators/               # REFACTOR: paquete modular
│   │   ├── prestaciones/
│   │   ├── recaudacion/
│   │   ├── encuadramiento/
│   │   ├── jubilacion/
│   │   ├── it/
│   │   ├── ip/
│   │   ├── ms/
│   │   ├── desempleo/
│   │   ├── age/
│   │   └── constantes_2026.py     # ✅ ya existe
│   └── v14/                       # Schema-First builder + blueprints
└── vault_seeds/                   # NUEVO: semillas COSMIC
    ├── ss_c1/                     # Vault BOVEDA_OPOS actual
    ├── ss_a2/
    ├── age_c1/
    └── jurista/

obsidian-bmo-chandra-edition/      # Fork BMO publicable
```

---

## 6. ORDEN DE PRIORIDADES (recomendado, alineado con Kimi 1→2→4→3→5)

1. ~~HOY: fix bug Neo4j~~ → ✅ YA HECHO
2. **ESTA SEMANA** (Fase 1 = 3-4 días): 4 fixes blueprints + REGLA 8 + unificar trampas + filtro PII.
3. **PRÓXIMAS 2 SEMANAS** (Fase 2 = 5-7 días): refactor calculadoras modular + LiteLLM + CoVe + Auto-RAG + 4 manos Chandra nuevas.
4. **SEMANA SIGUIENTE** (Fase 4 = 3-4 días): 6 templates AI + 9 tools utilitarias (PDF, exec, file ops vault, fetch URL, MCP).
5. **MES 2** (Fase 3 = 7-10 días): Fork BMO con tool calling UI + PDF + multimodal + autocompletados + selector modelo + LiteLLM dropdown.
6. **MES 2-3** (Fase 5 = 7-10 días): Repoblado vault + seed trampas Neo4j + casos validados.
7. **NUNCA ANTES DE 1-5** (Fase 6 = variable): productos derivados COSMIC.

---

## 7. DECISIONES PENDIENTES PARA TI (actualizadas tras verificación runtime)

Necesito tu ok antes de tocar nada:

- [ ] **¿Apruebas orden Kimi 1→2→4→3→5?** (ya consolidado en `IDEAS_KIMI.MD`)
- [ ] **¿Empezamos Fase 1 esta semana?** (4 fixes blueprints de 5 min c/u + unificación catálogo)
- [ ] **¿Cómo gestionamos PII?** Script regex blacklist + revisión muestra humana (recomendado)
- [ ] **Memorias sueltas (30+ MDs en raíz)** → ¿mover a `docs/memorias/` o dejar?
- [ ] **¿Mantenemos `MISTRAL_URL` obsoleta** o la limpio del `.env.backend`?
- [ ] **¿Compilamos BMO fork para producción** o seguimos en `feature/multi-chat`?
- [ ] **LiteLLM YA confirmado necesario** — ¿implemento en Fase 2.4 o antes?
- [ ] **¿Cuándo bajas los simulacros del Drive?** — bloquea Fase 5.5
- [ ] **Productos derivados:** ¿AutónomoAIA y EscritorAIA son prioridad después de C1 SS, o solo SS A2/AGE/Jurista?
- [ ] **¿Quitamos Gemini de fallback LiteLLM?** (descartado en `IDEAS_MAESTRAS_OPOSITAIA_2026` por inestable). Mantenemos Mistral → DeepSeek → Cohere → Groq.

---

## 8. RIESGOS

| Riesgo | Mitigación |
|--------|-----------|
| Refactor calculadoras rompe E2E | Tests pytest antes de mover código + git branch |
| LiteLLM API quirks | Empezar con Mistral solo + añadir Groq como fallback opcional |
| Tool calling UI lenta de implementar | Empezar con versión mínima (logs colapsables) |
| PII residual no detectada | 2 pasadas: regex automática + revisión humana muestra |
| Fork BMO se desincroniza del upstream | Rebase periódico de `main` |
| Productos derivados consumen tiempo sin generar ingresos | NO empezarlos hasta tener 0-4 cerradas |

---

## 9. NOTAS DE MEMORIAS Y MCP

- **MCP Memory** ✅ leído. Grafo de conocimiento con ~80+ entidades, cubriendo desde `OpositAIA` raíz hasta sesiones recientes.
- **Ground truth excepciones**: `backend/data/ground_truth_excepciones.json` (20 muestras verificadas).
- **Catálogo cálculos Gemini 15/05**: lista de 13 cálculos verificados — usar como **checklist** del refactor calculadoras.

### 9.1 Entidades MCP CLAVE para continuidad (consulta al reiniciar sesión)

| Entidad MCP | Tipo | Contiene |
|-------------|------|----------|
| `Plan_Chandra_v2_03_05_2026` | StrategicPlan | **FUENTE DE VERDAD del plan**: 5 fases + 10 best practices BP1-BP10 + 4 decisiones Q1-Q4 pendientes |
| `Modelo_Negocio_3_SKUs_28_04_2026` | BusinessModel | **FUENTE DE VERDAD del producto**: 3 SKUs + pricing + diferenciación legal |
| `Plan_Refactor_Calculadoras_Pendiente_29_04_2026` | TechnicalDebt | Plan de 10 submódulos + estrategia segura para evitar conflicto nombres |
| `Chandra_Agent_System` | AgentSystem | 7 tools, mistral-medium, loop iterativo, system prompt |
| `BMO_Chandra_Edition_Fork` | ArchitectureComponent | Fork `Espasiko/obsidian-bmo-chatbot-plus` `feature/multi-chat` (4 commits) |
| `Verificacion_Sistema_03_05_2026` | AuditSnapshot | Estado infra + plugins + vault + bugs |
| `Auditoria_Calculadoras_29_04_2026_BugsResueltos` | AuditReport | 8 bugs corregidos + 5 gaps implementados |
| `Catalogo_Trampas_Principal_YAML` + `Adicional_YAML` | CatalogFile | 120+ trampas verificadas BOE |
| `Trampas_Verificadas_184_19_04_26` | Verification | 184 trampas curadas en wiki/trampas/ |
| `PLAN_MAESTRO_CASOS_SIMULACROS.md` v4 | Document | 479 trampas + 752 preguntas |
| `Patrones_Narrativos_DM_9` (nombre legacy de entidad) | Knowledge | 9 patrones narrativos genéricos (no solo A/B/C) |
| `Ideas_Creativas_Wiki_12` | Knowledge | 12 ideas creativas para la wiki |
| `Ideas Groq Multi-modelo 02.05.26` | Strategy | LiteLLM detallado + modelos Groq actuales |
| `Sesion_03_05_2026_BMO_Chandra_Edition` | Session | Reglas 9-11 SYSTEM_PROMPT + Fase 1A+1B BMO |

### 9.2 Q1-Q4 del Plan_Chandra_v2_03_05_2026 (pendientes hace 12 días)

- **Q1:** ¿Clonar BMO repo ahora al workspace para empezar fork? → **YA HECHO** (Espasiko/obsidian-bmo-chatbot-plus)
- **Q2:** ¿Borrar `BMO_back_mal` y `ChatGPT_MD` vacías o dejar para ti decidir?
- **Q3:** ¿Orden preferido de fases? → Kimi recomienda **1→2→4→3→5**
- **Q4:** ~~¿Priorizar Copilot (8000)?~~ → **DESCARTADO** (mala licencia). Única interfaz Obsidian: BMO Chandra Edition (puerto 8080).

---

## 10. PREGUNTAS QUE NO ME ATREVO A RESPONDER SOLO (actualizadas 17:55)

1. **¿Vendes o no vendes?** El PRD + Brief dicen claramente: Trial €1/3d + Pro €69/mes (B2C primero, B2B después). **Si confirmas, la Fase 6 es OBLIGATORIA** después de cerrar 1-5.
2. ~~¿Tauri Desktop ya o aún no?~~ → IDEAS_MAESTRAS dice "prematuro, perfeccionar producto primero". **Decidido: Fase 6+.**
3. ~~¿LiteLLM imprescindible?~~ → **CONFIRMADO** por ti (11 providers en `.env`, queremos usar todos). **Fase 2.4.**
4. **¿Frontend React mantener o sustituir?** Tienes 17 vistas pero flujo real está en Obsidian. ¿Vale la pena seguir manteniendo el frontend React, o lo dejamos en mantenimiento mínimo hasta Tauri (Fase 6)?
5. **¿Migración localStorage → Postgres** en frontend React es prioridad ahora o se aplaza?
6. **¿Cuándo activas el agente Knowledge Tracing / FSRS** (§8 IDEAS_MAESTRAS) — antes o después de tener 1.000 usuarios?

---

> *Borrador v2 actualizado 15/05/2026 17:55 UTC+2 tras verificación runtime de Neo4j, calculadoras y env files.*
> *Próximo paso: tu aprobación de las decisiones pendientes §7 para arrancar Fase 1.*
