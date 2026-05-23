# Memoria de Sesión — 21/05/2026
> Sesión con Claude Sonnet 4.6 (CLI Claude Code)
> Continuación de la sesión del 20/05/2026 (comprimida por límite de contexto)

---

## Contexto de entrada

La sesión anterior (20/05/2026) había dejado dos tareas pendientes sin completar:
1. Crear entrada en MCP memory (`memory.jsonl`) con resumen de la sesión del 20/05
2. Corregir todos los errores marcados por el usuario en `BMAD_EXPLICADO_ADAPTADO.md`

Esta sesión retomó exactamente esas tareas y añadió trabajo nuevo.

---

## Tareas completadas

### 1. Entrada MCP Memory — sesión 20/05/2026
- **Archivo modificado:** `/home/spas/memory.jsonl` (651 líneas tras añadir)
- **Qué se añadió:** entidad `Sesion_20_05_2026_BMAD_MCP_Agentes` con resumen completo + entidades auxiliares (`CLAUDE_md_20_05_2026`, `Agente_Staff_BMAD`, `BMAD_Explicado_Adaptado`) + 9 relaciones
- **Contenido del resumen:** temas tratados, archivos creados, correcciones detectadas por el usuario, pendientes

### 2. Correcciones en BMAD_EXPLICADO_ADAPTADO.md — 10 ediciones
- **Archivo modificado:** `/home/spas/OPOS_GEMINI_1/BMAD_EXPLICADO_ADAPTADO.md`
- **Correcciones aplicadas:**

| # | Qué se corrigió | Dónde estaba |
|---|----------------|--------------|
| 1 | Header — eliminado "!!NO ES DEFINITIVO!!" y comentario de anotaciones | Línea 3-5 |
| 2 | **COSMIC real** — reescrito: componentes intercambiables (personajes, cálculos, plazos, trampas), no "6 formatos". La IP real del sistema. | PARTE 2 |
| 3 | Bloque de corrección del usuario en CAPS eliminado + título PARTE 3 limpiado ("y una mierda!" → limpio) | Entre PARTE 2 y 3 |
| 4 | **Desarrollador ≠ opositor** — el opositor ESTUDIA, no construye nada. Separación clara de capas. | PARTE 3 |
| 5 | **VALERIA → VALERA** (typo en el diagrama de capas) | PARTE 3 diagrama |
| 6 | **NEXO con duda** → pregunta al usuario antes de enrutar (no lanzar ambos en paralelo) | Agente 1 |
| 7 | **VALERA base** → `valera_agent.py` (por implementar). Eliminada referencia a `proxy_agente_escritor.py` (es del proyecto de libros de la mujer de Spas, irrelevante para OpositAIA) | Agente 3 |
| 8 | `proxy_agente_escritor.py` eliminado del listado de backend | PARTE 2 código |
| 9 | **CAPA 4 BOE** → ID BOE viene del nodo Neo4j, nunca lo inventa el LLM | PARTE 5 |
| 10 | **CHANDRA flow** → reescrito como tool calling iterativo autónomo (hasta 10 rondas, Mistral decide qué herramienta llamar en cada ronda). Eliminado el pipeline rígido incorrecto. | PARTE 5 flujo |
| 11 | Summary final — COSMIC corregido en el resumen ejecutivo | PARTE 10 |

### 3. Versiones V14.5 y V17 — investigación y aclaración
- **V14.5** = `backend/v14/` — motor "Narrativa en Red". CaseSchemaBuilder + prose_validator + cambios_dm_2026 + nombres_pool + 10 blueprints (S02-S16). Evolución de V14 (casos lineales) a V14.5 (redes de 3-8 personajes). Pendientes: S17 (Mar/Minería), S18 (Cese RETA).
- **V17** = `backend/scripts/ingest_neo4j_v17.py` — script de ingesta de leyes en Neo4j. 108 leyes, 6683 preceptos, 6683 embeddings.
- Confirmado en `memory.jsonl` y en `docs/prd.md` (RF-02.5 lo citaba explícitamente).

### 4. Gaps arquitectónicos identificados y documentados
Gaps que **no estaban en el plan** y se añadieron al PRD y a BMAD:
- **LiteLLM** como proxy unificado (solo mencionado superficialmente en addendum 01/05)
- **Content Quality Gate** — flujo draft→verificado→publicado (no existía en ningún doc)
- **Jerarquía de caché de 6 niveles** (solo mencionada como "misma pregunta = misma respuesta")
- **Dual Interface** Frontend React vs Obsidian BMO (no estaba formalizado)
- **Modelo por tarea** — qué modelo usa cada agente y por qué

---

## Archivos leídos en esta sesión

| Archivo | Por qué |
|---------|---------|
| `/home/spas/OPOS_GEMINI_1/BMAD_EXPLICADO_ADAPTADO.md` | Leer todas las correcciones del usuario para aplicarlas |
| `/home/spas/memory.jsonl` (líneas 560-638 + líneas 1-20) | Ver formato de entidades y relaciones + contexto de sesiones anteriores |
| `/home/spas/OPOS_GEMINI_1/15_05_2026_VISION_360_OPOSITAIA.md` (primeras 40 líneas) | Contexto COSMIC y estado del proyecto |
| `/home/spas/OPOS_GEMINI_1/docs/prd.md` | Verificar qué estaba ya en el PRD antes de añadir |
| `/home/spas/.claude/settings.json` | (desde sesión anterior, ver MCPs configurados) |
| `/home/spas/OPOS_GEMINI_1/docs/AUDITORIA_IMPLEMENTADO_VS_DISEÑO_17_03_26.md` | (desde sesión anterior, contexto auditoría) |
| `/home/spas/OPOS_GEMINI_1/bmad-custom-src/custom.yaml` | (desde sesión anterior, confirmar agente Staff registrado) |
| `/home/spas/OPOS_GEMINI_1/.claude/skills/bmad-staff/SKILL.md` | (desde sesión anterior, confirmar skill activo) |

---

## Archivos creados en esta sesión

| Archivo | Contenido |
|---------|-----------|
| `/home/spas/OPOS_GEMINI_1/21_05_2026_MEMORIA_SESION.md` | Este archivo |

---

## Archivos actualizados en esta sesión

| Archivo | Qué cambió |
|---------|-----------|
| `/home/spas/OPOS_GEMINI_1/BMAD_EXPLICADO_ADAPTADO.md` | 10 correcciones del usuario aplicadas + PARTE 11 añadida (LiteLLM, Content Gate, caché, dual interface) |
| `/home/spas/OPOS_GEMINI_1/docs/prd.md` | ADDENDUM 21/05/2026 añadido al inicio (antes del addendum 01/05) |
| `/home/spas/memory.jsonl` | 14 líneas nuevas: entidad sesión 20/05 + 3 entidades auxiliares + 9 relaciones |

---

## Archivos creados en sesión anterior (20/05/2026) — para referencia

Estos archivos los creó la sesión anterior (comprimida). Se listan aquí para tener el inventario completo:

| Archivo | Qué es |
|---------|--------|
| `/home/spas/OPOS_GEMINI_1/CLAUDE.md` | Contexto permanente del proyecto. Leer al inicio de CADA sesión. |
| `/home/spas/OPOS_GEMINI_1/BMAD_EXPLICADO_ADAPTADO.md` | BMAD adaptado a OpositAIA: 12 agentes, arquitectura 3 capas, roadmap sprints |
| `/home/spas/OPOS_GEMINI_1/20_05_MCP-S_PROYECTO_IDES.md` | Inventario completo de MCPs en los 6 IDEs |
| `/home/spas/OPOS_GEMINI_1/bmad-custom-src/agents/staff.md` | Agente Staff — guardián de la memoria del proyecto |
| `/home/spas/OPOS_GEMINI_1/.claude/skills/bmad-staff/SKILL.md` | Trigger skill para invocar Staff con `.bmad-staff` |
| `/home/spas/.claude/projects/-home-spas-OPOS-GEMINI-1/memory/MEMORY.md` | Índice de memorias persistentes de Claude Code |
| `/home/spas/.claude/projects/-home-spas-OPOS-GEMINI-1/memory/project_mcp_ecosystem.md` | Memoria: ecosistema MCP |
| `/home/spas/.claude/projects/-home-spas-OPOS-GEMINI-1/memory/opos_agent_ecosystem.md` | Memoria: ecosistema de agentes OPOS |

---

## Decisiones y correcciones clave de esta sesión

1. **COSMIC** no es "6 formatos de un contenido" — es componentes verificados (personajes, cálculos, plazos, trampas) intercambiables para que una IA pequeña sirva simulacros "nuevos" que son 100% verificados.

2. **proxy_agente_escritor.py** no tiene nada que ver con OpositAIA — es el proyecto de escritura de libros de la mujer de Spas.

3. **CHANDRA** no sigue un pipeline rígido — Mistral decide autónomamente qué herramienta llamar en cada ronda (hasta 10 rondas). El LLM no genera datos, solo decide herramientas y compone con sus resultados.

4. **Content Quality Gate** es el gap más crítico: sin él, el opositor podría recibir contenido con artículos inventados o plazos incorrectos. V14.5 ya ha demostrado este problema (Art. 190.5 TRLGSS no existe, 19 semanas nacimiento tampoco).

5. **V14.5** y **V17** son versiones del propio código del proyecto, no modelos externos.

---

## Pendientes para próximas sesiones

| Tarea | Prioridad |
|-------|-----------|
| Implementar `backend/agents/content_gate.py` | 🔴 Alta |
| Configurar LiteLLM proxy (`litellm_config.yaml`) | 🔴 Alta |
| Blueprints pendientes: S17 (Mar/Minería), S18 (Cese RETA) | 🟠 Media |
| Graphify para indexar proyecto → wiki en `D:\OPOS_PROJECT` | 🟠 Media |
| Unificar fragmentación de memoria entre IDEs | 🟡 Baja |
| Sprint 1 BMAD: historias para PROGRESO + WIKI + VALERA modo ALEGRE | 🟠 Media |

---

*Generado al final de la sesión del 21/05/2026.*
