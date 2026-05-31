# OpositAIA — CLAUDE.md
> **Leer esto primero.** Cualquier IA que abra este proyecto debe leer este archivo antes de actuar.
> Última actualización: 31/05/2026

---

## Qué es este proyecto

**OpositAIA** — plataforma IA para preparación de oposiciones de la Seguridad Social española.
- 4 cuerpos objetivo: Aux AGE (C2), Adm AGE (C1), Adm SS (C1), Gest SS (A2)
- Estrategia COSMIC: Create Once, Serve Many — 54.000 preguntas únicas, casos prácticos modulares, series turca, seguimiento de errores
- Estado: sistema funcional con agente Chandra operativo, calculadoras SS/AGE verificadas, BMO Chandra Edition multi-chat

**Developer:** Spas | **Idioma de trabajo:** Español

---

## Fuentes de verdad (en orden de prioridad)

1. **Wiki OPOS_PROJECT** → `/mnt/d/OPOS_PROJECT/01-Wiki/` — estado actualizado del proyecto (usar skill `/check-wiki`)
2. **Graphify graph** → `graphify-out/graph.json` — mapa del código (usar skill `/sync-graphify`)
3. **MCP memory grafo** → `/home/spas/memory.jsonl` — conocimiento acumulado
4. **Este archivo** → resumen ejecutivo, NO fuente primaria de detalles
5. **Código fuente** → leer solo cuando las fuentes anteriores no bastan
6. **Lecciones IAs anteriores** → `/mnt/d/OPOS_PROJECT/01-Wiki/Lecciones_IAs_Anteriores.md` — LEER antes de diagnosticar bugs

---

## Stack técnico crítico

| Componente | Detalle |
|-----------|---------|
| **Backend** | FastAPI, Python 3.12, puerto **8080** |
| **Arrancar backend** | Usar skill `/arrancar-backend` o `/arrancar-chandra` |
| **Neo4j** | bolt://localhost:**7687** · user: neo4j · pass: opositaia2026 |
| **BMO Chandra** | Plugin Obsidian fork — repo: `/home/spas/obsidian-bmo-chatbot-plus/` |
| **AgenteEscritor** | Proxy Nina puerto **9000** — wiki: `01-Wiki/Backend/AgenteEscritor_Proxy.md` |
| **Corte legal** | **04/03/2026** — normativa posterior = no existe para este sistema |

---

## Decisiones FIRMES — no reabrir, no cuestionar

| Decisión | Estado |
|----------|--------|
| **Qdrant DESCARTADO** para búsqueda legal | Neo4j HNSW nativo. Qdrant solo para PDFs de academia |
| **Copilot DESCARTADO** en Obsidian | El único interfaz es **BMO Chandra Edition** |
| **Salamandra DESCARTADA** para producción | Solo para preguntas pre-hechas COSMIC |
| **Supabase DESCARTADO** | Neo4j es la base de datos de grafos |
| **NO re-entrenar Salamandra** | Confirmado definitivamente |
| **Neo4j puerto 7687** (no 7688) | 7688 era temporal |

---

## Skills personalizadas disponibles

| Skill | Comando | Qué hace |
|-------|---------|----------|
| Arrancar backend | `/arrancar-backend` | Levanta FastAPI en 8080 |
| Arrancar Chandra | `/arrancar-chandra` | Backend + Neo4j + test ping |
| Sync Graphify | `/sync-graphify` | Actualiza grafos de los 3 repos |
| Check Wiki | `/check-wiki` | Revisa wiki vs CLAUDE.md |
| Deploy BMO | `/deploy-bmo` | Build + copy a vaults |
| Rebuild EXE | `/rebuild-exe` | Docker cross-compile proxy |

---

## Archivos PROHIBIDOS sin confirmación de Spas

- `backend/calculators/calculos_ss_extended.py` — 2457 líneas verificadas BOE
- `backend/data/catalog_FINAL_v2.json` — catálogo 108 leyes
- `backend/v14/blueprints/` — blueprints de casos prácticos
- `docker-compose.yml` — configuración servicios Docker
- `.env.backend` — credenciales de producción

---

## BMAD en este proyecto

BMAD v6.1.1 instalado. 27 skills activas (86 movidas a backup en `.claude/skills-backup-bmad-wds/`).
- Agente Staff (`/bmad-staff`): guardián de la memoria del proyecto. Invocarlo si hay dudas sobre decisiones previas.

---

## Reglas de conducta para cualquier IA

1. **Consultar wiki y graphify ANTES de leer código** — usar fuentes de verdad
2. **Leer Lecciones_IAs_Anteriores.md** antes de diagnosticar bugs en BMO/proxy
3. **Citar siempre el artículo BOE** cuando se afirme algo legal
4. **Nunca calcular en LLM** — usar `calcular_ss` o `calculadora_age.py`
5. **Verificar en Neo4j primero** antes de inventar estructura legal
6. **Corte 04/03/2026** — normativa posterior = no existe
7. **No crear archivos nuevos en la raíz** — ya hay ~170 archivos sueltos
8. **Preguntar antes de modificar** los archivos prohibidos

---

## Detalle técnico → ver rules (se cargan automáticamente por directorio)

- `.claude/rules/chandra.md` — agente Chandra, 7 manos, Neo4j
- `.claude/rules/proxy-agente.md` — proxy AgenteEscritor, 17 tools, puerto 9000
- `.claude/rules/bmo-plugin.md` — plugin BMO fork, build, deploy
- `.claude/rules/vaults.md` — los 3 vaults de Obsidian, REST API bridge

---

## AgenteEscritor — estado actualizado (31/05/2026)

> Leer esto ANTES de tocar el proxy o los vaults de escritura.

- **Fuente de verdad del código:** `/home/spas/build_agente/proxy_agente_escritor.py` (NO el repo)
- **17 tools** — ver lista completa en `01-Wiki/Backend/AgenteEscritor_Proxy.md`
- **EXE compilado:** 23.4 MB · desplegado en Nina (`/mnt/d/AgenteEscritor_Para_Nina/`) y Miguel Ángel (`/mnt/d/AgenteEscritor_Miguel_Angel/`)
- **Skill rebuild:** `/rebuild-exe` — sincroniza build→repo, compila con Docker, despliega a todos los vaults
- **Multi-modelo:** 11+ proveedores. Selección por `model: "proveedor:modelo"` en perfil BMO.
- **⚠️ Los IDs de OpenRouter cambian frecuentemente.** Verificar antes de hardcodear. Última verificación: 31/05/2026. Modelos activos documentados en `01-Wiki/Backend/31_05_2026_MEMORIA_HECHO.md`
- **Vaults clientes:**
  - Nina: vault búlgaro, perfil Sara, `/mnt/d/AgenteEscritor_Para_Nina/`
  - Miguel Ángel: novela hitita, perfil Edi, `/mnt/d/AgenteEscritor_Miguel_Angel/` · entregado 31/05/2026
- **Templates Templater:** sintaxis dual `tp.mcpTools ? ... : await tp.system.prompt()` — funciona tanto por proxy REST como desde UI Obsidian
- **obsidian-git vs proxy git_save:** dos sistemas independientes. El plugin necesita `authorName`/`authorEmail` en su `data.json` o config local del repo git.
- **Ollama local** en máquina Spas: `mistral-local:latest` (recomendado tools), `salamandra-r1:q5km`, `qwen2.5-coder:1.5b-base`
- **Bitácora sesión 29-30/05:** `/mnt/d/AgenteEscritor_Para_Nina/30_05_26_BITACORA_AGENTE.md`
- **Memoria sesión 31/05:** `/mnt/d/OPOS_PROJECT/01-Wiki/Backend/31_05_2026_MEMORIA_HECHO.md`
- **PRD Cerebrito** (producto): `/home/spas/obsidian-bmo-chatbot-plus/docs_planes/prd_cerebrito.md`
