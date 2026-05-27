# OpositAIA — CLAUDE.md
> **Leer esto primero.** Cualquier IA que abra este proyecto debe leer este archivo antes de actuar.
> Última actualización: 20/05/2026

---

## Qué es este proyecto

**OpositAIA** — plataforma IA para preparación de oposiciones de la Seguridad Social española.
- 4 cuerpos objetivo: Aux AGE (C2), Adm AGE (C1), Adm SS (C1), Gest SS (A2)
- Estrategia COSMIC: Create Once, Serve Many — 54.000 preguntas únicas, patres de casos practicos que se pueden incorporar y mezclar sin cambiar el sentido, de 4-8 personajes o por separado, hay 3 tipos de casos practicos! pregntas para test pos tema, partes de serie turca que se pueden modificar para distintas combinaciones de temas y parecer nuevas al usuario, con seguimiento de errores frequentes etc. 
- Estado: sistema funcional con agente Chandra operativo, calculadoras SS/AGE verificadas. memoria actualizada en mcp memory grafo, md-s obsidian project vault en neo4j 

**Developer:** Spas | **Idioma de trabajo:** Español

---

## Stack técnico crítico

| Componente | Detalle |
|-----------|---------|
| **Backend** | FastAPI, Python 3.12, puerto **8080** |
| **Arrancar backend** | `cd backend && ../.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080 --reload` |
| **Neo4j** | bolt://localhost:**7687** · user: neo4j · pass: opositaia2026 |
| **Obsidian vault SS** | `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/` — leyes, trampas, estudio |
| **Obsidian vault proyecto** | `D:\OPOS_PROJECT` — PRD, arquitectura, segundo cerebro |
| **BMO Chandra** | Plugin Obsidian fork (MIT) — interfaz único de chat en Obsidian |
| **MCP memory** | `/home/spas/memory.jsonl` (637 líneas, grafo de conocimiento) |
| **Corte legal** | **04/03/2026** — no se usan datos normativos posteriores |

---

## Archivos clave para entender el proyecto

```
CLAUDE.md                              ← este archivo (leer primero)
docs/prd.md                            ← PRD oficial
docs/project-overview.md               ← visión técnica
15_05_2026_VISION_360_OPOSITAIA.md     ← visión completa (estado mayo 2026)
BMAD_EXPLICADO_ADAPTADO.md             ← arquitectura agentes + roadmap
20_05_MCP-S_PROYECTO_IDES.md           ← ecosistema MCP completo
docs/AUDITORIA_IMPLEMENTADO_VS_DISEÑO_17_03_26.md  ← auditoría técnica
15_05_2026_BORRADOR_AUDITORIA_Y_PLAN.md ← estado y plan actualizado
/home/spas/obsidian-bmo-chatbot-plus/docs_planes - cerebrito BMO refactorizacion+ planes
```

---

## Decisiones FIRMES — no reabrir, no cuestionar

| Decisión | Estado |
|----------|--------|
| **Qdrant DESCARTADO** para búsqueda legal | Neo4j 2026 tiene HNSW nativo. Qdrant solo para PDFs de academia |
| **Copilot DESCARTADO** en Obsidian | Mala licencia. El único interfaz es **BMO Chandra Edition** |
| **Salamandra DESCARTADA** para producción | Solo para preguntas pre-hechas COSMIC |
| **Supabase DESCARTADO** | Neo4j es la base de datos de grafos |
| **NO re-entrenar Salamandra** | Confirmado definitivamente |
| **Proxy VPS muerto** | MISTRAL_URL en .env.backend apunta a proxy muerto — el código lo ignora. URL real: api.mistral.ai |
| **Neo4j puerto 7687** (no 7688) | 7688 era temporal. El correcto es 7687 |

---

## Agente Chandra — el corazón del sistema

- **Endpoint:** `POST /opos/v1/chat/completions` (OpenAI-compatible)
- **Modelo:** Mistral medium-latest
- **7 Manos:** tavily_search, search_boe, get_law_text_block, consultar_neo4j, calcular_ss, buscar_vault, escribir_vault
- **Regla:** Chandra NUNCA genera datos numéricos sin pasar por calculadora Python
- **Anti-alucinación:** Tier 1 (auto) → Tier 2 (DeepSeek) → Tier 3 (Claude Sonnet)

---

## Los dos vaults de Obsidian — NO confundirlos

| Vault | Ruta | Contenido |
|-------|------|-----------|
| **BOVEDA_OPOS** | `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/` | Leyes SS, trampas, flashcards, estudio oposiciones |
| **OPOS_PROJECT** | `D:\OPOS_PROJECT` | PRD, arquitectura, sesiones, segundo cerebro del PROYECTO |

**Bridge REST API** (para BOVEDA_OPOS): `http://172.26.240.1:27123`
**API Key Obsidian:** `097befc68922b9c32d6388ebbb871e127c5c9037af91a83813107e5e1e60699d`

---

## Archivos PROHIBIDOS sin confirmación de Spas

- `backend/calculators/calculos_ss_extended.py` — 2457 líneas verificadas BOE
- `backend/data/catalog_FINAL_v2.json` — catálogo 108 leyes
- `backend/v14/blueprints/` — blueprints de casos prácticos
- `docker-compose.yml` — configuración servicios Docker
- `.env.backend` — credenciales de producción

---

## Estado Neo4j (19/05/2026)

- **108 leyes** indexadas
- **6683 preceptos** con embeddings HNSW
- **379 EXCEPCION_A** (trampas del examen)
- **517 comunidades** Louvain
- BMO conecta via Chandra mano #4 (consultar_neo4j)

---

## BMAD en este proyecto

BMAD v6.1.1 instalado. Módulos: core, bmm, cis, tea, wds.
- Config: `_bmad/bmm/config.yaml` (user_name: Spas, language: Spanish)
- Output: `_bmad-output/`
- Agente Staff: `.bmad-staff` — LEERLO SIEMPRE antes de empezar tarea compleja

**Agente Staff** es el guardián de la memoria del proyecto. Lo conoce todo. Invócalo si tienes dudas sobre decisiones pasadas o si algún agente usa información desactualizada.

---

## MCPs activos en Claude Code (desde 20/05/2026)

- `memory` → `/home/spas/memory.jsonl` (grafo de 637 entidades)
- `boe` → búsqueda BOE en tiempo real
- `fetch` → descargar URLs
- `github` → operaciones GitHub

Ver detalle completo en `20_05_MCP-S_PROYECTO_IDES.md`

---

## Reglas de conducta para cualquier IA

1. **Citar siempre el artículo BOE** cuando se afirme algo legal
2. **Nunca calcular en LLM** — usar `calcular_ss` o `calculadora_age.py`
3. **Verificar en Neo4j primero** antes de inventar estructura legal
4. **Corte 04/03/2026** — normativa posterior = no existe para este sistema
5. **No crear archivos nuevos en la raíz** — ya hay ~170 archivos sueltos
6. **Consultar al agente Staff** si hay confusión sobre decisiones previas
7. **Preguntar antes de modificar** los archivos prohibidos
