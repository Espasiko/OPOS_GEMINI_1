# OpositAIA — Brownfield Documentation Index

> **Generado:** 14/03/2026 | **Scan:** Reconciliado (100%) | **Tipo:** Multi-part (monorepo)
> 
> **FUENTE DE LA VERDAD:** [28_02_2026_SINTESIS_PLAN_DEFINITIVO.md](file:///home/spas/OPOS_GEMINI_1/28_02_2026_SINTESIS_PLAN_DEFINITIVO.md), [AUDITORIA_IMPLEMENTADO_VS_DISEÑO_27_02_26.md](file:///home/spas/OPOS_GEMINI_1/docs/AUDITORIA_IMPLEMENTADO_VS_DISEÑO_27_02_26.md) y [CASOS_TRAMPAS_DM_2026.md](file:///home/spas/OPOS_GEMINI_1/CASOS_TRAMPAS_DM_2026.md)

---

## Resumen Rápido

- **Proyecto:** Sistema IA multi-agente para oposiciones SS + AGE España
- **Estrategia:** COSMIC (Create Once, Serve Many) — 4 cuerpos
- **Stack:** FastAPI 0.115 + Vite/React 19 + Qdrant 1.12 + Postgres 15 + Neo4j 5 + Docker
- **LLMs:** 7 proveedores (Groq, DeepSeek, Gemini, Mistral, Claude, OpenAI, Ollama)
- **Frontend:** 17 vistas funcionales + Excalidraw + PWA
- **KB Actual:** 13,210 puntos (FULL_XML), 100% cobertura legal verificada.
- **MVP:** Auxiliar AGE C2 (28 temas) | **Beta:** Mayo 2026

---

## Documentación Principal

| Documento | Contenido |
|-----------|-----------|
| [**Project Overview**](./project-overview.md) | **Inventario exhaustivo** — 13 secciones: 17 vistas frontend, 9 routers, 31 calculadoras SS, 33 calculadoras AGE, 25 agentes, 8 tablas DB, 6 MCP tools, golden datasets, evaluación COSMIC |
| [Scan Report](./project-scan-report.json) | Datos del escaneo BMAD |

---

## Frontend (17 vistas operativas)

| Categoría | Vistas | Estado |
|-----------|--------|--------|
| **Estudio** | Chat IA, Temario, Plan de Estudio | ✅ |
| **Generación IA** | Mapas Mentales (Excalidraw, export PNG), Casos Prácticos (MCQ), Flashcards (3D flip), Esquemas, Resúmenes, Comparador Legal | ✅ |
| **Evaluación** | Simulacros (timer + temas), Mi Progreso (% aciertos, filtros 7d/30d) | ✅ |
| **Búsqueda** | Búsqueda RAG con fuentes BOE | ✅ |
| **Config** | Configuración (BYOK API keys), Guía de Usuario | ⚠️ UI placeholder |
| **Debug** | Test VPS, Test Backend | 🔧 |

---

## Backend (9 routers + 28 calculadoras + 25 agentes)

| Módulo | Detalle |
|--------|---------|
| **Routers** | rag, rag_v2, chat, upload, ai_functions (multi-provider), user, boe, mcp_gateway, casos_practicos |
| **Calculadoras** | 31 SS implementadas (IT, IPT, IPA, Jubilación, Desempleo, Maternidad, IMV...) + 33 AGE implementadas + 2 nuevas (AGE, Presupuesto) |
| **Agentes** | llm_providers (7 APIs), verification_agents (anti-hallucination 3-tier), mistral_tools, rag_agent_v2, orchestrator, salamandra_client |
| **DB Schema** | 8 tablas PostgreSQL: user_progress, answer_history, user_cases, simulacros, mind_maps, study_sessions, recommendations, rag_queries + views + triggers |

---

## MCP Server (6 tools)

`search_rag`, `verify_boe`, `search_jurisprudence`, `get_law_summary`, `ingest_new_law`, `list_collections`
Embedding: `pablosi/bge-m3-spa-law-qa-trained-2` (1024 dims)

---

## Datasets y Contenido

| Fuente | Archivos | Reutilizable COSMIC |
|--------|----------|:-------------------:|
| Golden Dataset (`golden_dataset/`) | 42 | ✅ Sí (etiquetar por cuerpo) |
| MASTER_DATASET v12 Platinum | 1 (1.9MB) | ✅ Sí |
| Conceptual Materials (20 PDFs + QA) | 45 | ✅ Sí (AGE) |
| Exámenes Golden generados | 5 | ✅ Template |
| Staging enrichment (multi-modelo) | 26 | ⚠️ Filtrar calidad |
| gran-basurero.jsonl (52MB) | 1 | ⚠️ Rescatar items |
| Dataset Generator archive | 102+ | ❌ Revisar caso por caso |

---

## Documentos de Referencia (con estado de vigencia)

### 🟢 Fuentes de la Verdad (vigentes)

| Documento | Fecha | KB | Estado |
|-----------|-------|-----|--------|
| [Síntesis Plan Definitivo](file:///home/spas/OPOS_GEMINI_1/28_02_2026_SINTESIS_PLAN_DEFINITIVO.md) | 28/02/2026 | 14 | ✅ **Vigente** — Fuente de verdad, 13 secciones, 9 docs consolidados |
| [Auditoría Completa](file:///home/spas/OPOS_GEMINI_1/docs/AUDITORIA_IMPLEMENTADO_VS_DISEÑO_27_02_26.md) | 27/02/2026 | 24 | ✅ **Vigente** — 10 secciones, estado impl. vs diseño |
| [Catálogo Trampas Pedagógicas](file:///home/spas/OPOS_GEMINI_1/CASOS_TRAMPAS_DM_2026.md) | 14/03/2026 | 15 | ✅ **Vigente** — Compilación completa desde YAMLs, errores corregidos |

### 🟡 Arquitectura y Planes (parcialmente obsoletos)

| Documento | Fecha | KB | Estado |
|-----------|-------|-----|--------|
| [Arquitectura Actual](file:///home/spas/OPOS_GEMINI_1/ARQUITECTURA_ACTUAL_11_02_26.md) | 14/02/2026 | 39 | ⚠️ **Parcial** — Detallada pero anterior a síntesis |
| [Plan Desarrollo 2026](file:///home/spas/OPOS_GEMINI_1/PLAN_DESARROLLO_2026.md) | 09/01/2026 | 50 | ⚠️ **Parcial** — Ambicioso, pre-COSMIC. Contrastar con síntesis |
| [Resumen Ejecutivo](file:///home/spas/OPOS_GEMINI_1/RESUMEN_EJECUTIVO_5_MINUTOS.md) | 13/02/2026 | 10 | ⚠️ **Parcial** — Resumen rápido, no tiene últimas decisiones |

### 📘 READMEs

| Documento | Fecha | KB | Estado |
|-----------|-------|-----|--------|
| [README proyecto](file:///home/spas/OPOS_GEMINI_1/README.md) | 05/02/2026 | 7 | ⚠️ Actualizar con estado actual |
| [Backend README](file:///home/spas/OPOS_GEMINI_1/backend/README.md) | 09/12/2025 | 8 | 📦 **Legacy** — Pre-sprint 9, no refleja ai_functions |
| [MCP Server README](file:///home/spas/OPOS_GEMINI_1/mcp-server/README.md) | 09/12/2025 | 2 | 📦 **Legacy** — No refleja tools actuales (6 tools) |

### 📂 Plan Definitivo — Claude (`docs/PLAN_DEFINITIVO_MD/`)

9 documentos del plan estratégico original creados con Claude. **Imprescindibles para contrastar decisiones**.

| # | Archivo | Contenido |
|---|---------|-----------|
| 1 | [Plan COSMIC](file:///home/spas/OPOS_GEMINI_1/docs/PLAN_DEFINITIVO_MD/plan_app_oposiciones_cosmic.md) | **Plan maestro** — Estrategia COSMIC, modelo negocio, roadmap completo |
| 2 | [Apéndice II](file:///home/spas/OPOS_GEMINI_1/docs/PLAN_DEFINITIVO_MD/apendice_II_tecnico_actualizado.md) | Stack técnico actualizado, decisiones de arquitectura |
| 3 | [Apéndice III](file:///home/spas/OPOS_GEMINI_1/docs/PLAN_DEFINITIVO_MD/apendice_III_actualizacion_tecnica.md) | Actualización técnica post-stack |
| 4 | [Apéndice IV](file:///home/spas/OPOS_GEMINI_1/docs/PLAN_DEFINITIVO_MD/apendice_IV_final.md) | Plan final detallado |
| 5 | [Apéndice IV Suplement](file:///home/spas/OPOS_GEMINI_1/docs/PLAN_DEFINITIVO_MD/apendice_IV_suplemento.md) | Suplemento al plan final |
| 6 | [Apéndice V](file:///home/spas/OPOS_GEMINI_1/docs/PLAN_DEFINITIVO_MD/apendice_V.md) | Expansión: multi-cuerpo, escalabilidad |
| 7 | [Apéndice VI](file:///home/spas/OPOS_GEMINI_1/docs/PLAN_DEFINITIVO_MD/apendice_VI.md) | Monetización y modelo de negocio |
| 8 | [Apéndice VII](file:///home/spas/OPOS_GEMINI_1/docs/PLAN_DEFINITIVO_MD/apendice_VII.md) | Roadmap detallado de implementación |
| 9 | [Apéndice VIII — Leyes RAG](file:///home/spas/OPOS_GEMINI_1/docs/PLAN_DEFINITIVO_MD/apendice_VIII_leyes_RAG.md) | **54 normas legales** inventariadas con BOE URLs, prioridades, categorías |

### 📊 Datasets y verificación

| Documento | Fecha | KB | Estado |
|-----------|-------|-----|--------|
| [Investigación Temas Frecuentes](file:///home/spas/OPOS_GEMINI_1/investigacion_temas_frecuentes_nuestra.md) | 14/03/2026 | 8 | ✅ **Vigente** — Análisis local de temas frecuentes en oposiciones SS |
| [Sesión 12/03](file:///home/spas/OPOS_GEMINI_1/memoria_actual_12_03.md) | 12/03/2026 | 12 | ✅ **Vigente** — Estado anterior |
| [Sesión 17/03 (V13.1)](file:///home/spas/OPOS_GEMINI_1/17_03_26_MEMORIA_SESION.md) | 17/03/2026 | 16 | ✅ **Vigente** — Hitos Mistral V13.1 y DeepSeek R1 |

### 🧹 Operativo

| Documento | Fecha | KB | Estado |
|-----------|-------|-----|--------|
| [Plan Limpieza Raíz](file:///home/spas/OPOS_GEMINI_1/PLAN_LIMPIEZA_RAIZ.txt) | 22/01/2026 | 20 | ⚠️ No ejecutado aún |

---

## Métricas del Escaneo

| Métrica | Valor |
|---------|-------|
| Archivos raíz | 216 (⚠️ archivos no rastreados, muchos en academias/, backend/, docs/, scripts/) |
| Vistas frontend | 17 (15 operativas + 2 debug) |
| Routers API | 9 |
| Calculadoras SS/IMV | 31 implementadas + 2 nuevas (AGE, Presupuesto) |
| Calculadoras AGE | 33 implementadas |
| Agentes backend | 25 archivos Python |
| Tablas PostgreSQL | 8 + 3 views + triggers |
| MCP Server tools | 6 |
| LLM Providers | 7 |
| Golden dataset archivos | 42 |
| Conceptual materials | 45 (20 PDFs + 17 textos + 8 QA) |
| MASTER_DATASET versiones | v4 → v12 (8 iteraciones) |
| Docker services | 3 (Qdrant, Postgres, Backend) |
| Qdrant Cloud chunks | 48,866 |
| Líneas `backendService.ts` | 757 |
| Líneas `schema.sql` | 377 |

---

## Próximos Pasos

1. **Crear PRD Brownfield** usando este `index.md` como input
2. **Auditar golden datasets** — identificar Q&A/razonamientos/casos válidos para COSMIC
3. **Etiquetar contenido COSMIC** — cuerpo + tema_id + dificultad en cada item
4. **Probar Neo4j en Docker local** (añadir al `docker-compose.yml`)
5. **Implementar 28 calculadoras AGE** (código ya diseñado)
6. **Completar Settings page** (BYOK funcional)
7. **Migrar localStorage → PostgreSQL** (schema ya listo)
8. **Decidir sobre archivos no rastreados** (216 archivos pendientes de seguimiento)
