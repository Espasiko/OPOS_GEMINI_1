# PLAN MAESTRO DEFINITIVO — OpositAIA (13/03/2026)

> **Estado del Proyecto:** Brownfield Consolidado | **Actualizado:** 13/03/2026 15:45
> **Visión:** Sistema generador de casos prácticos de nivel tribunal con rigor legal 100% y trazabilidad total al BOE.
> **Documento fuente de verdad del proyecto** — Sustituye a todos los planes anteriores.

---

## 1. ARQUITECTURA DEL SISTEMA (VERIFICADA 13/03/2026) ✅

### 1.1 Stack Técnico Real

| Capa | Tecnología | Estado |
|------|------------|--------|
| Frontend | Vite 6.2 + React 19 + TailwindCSS (17 vistas) | ✅ Operativo |
| Backend | FastAPI (9 routers) + Python 3.12 | ✅ Operativo |
| Vector RAG | Qdrant v1.12 (Docker local) | ✅ 25.273 puntos |
| Grafos | Neo4j 5 Community (Docker local) | ✅ Healthy (12/03) |
| DB Relacional | PostgreSQL 15 (Docker local) | ✅ Healthy |
| MCP Server | Node.js + TypeScript (6 tools) | ✅ Operativo |
| Calculadoras | Python determinístico (13 SS + AGE) | ✅ 13 SS verificadas |

### 1.2 Colecciones Qdrant

| Colección | Puntos | Uso |
|-----------|--------|-----|
| `opositaia_knowledge_FULL_XML` | **25.273** | RAG principal — Leyes con metadata XML BOE |
| `opositaia_knowledge_hybrid` | 48.866 | RAG híbrido (backup) |
| `opositaia_leyes_master` | 54 | Índice de leyes |
| `opositaia_memory_mcp` | 3 | Memoria MCP server |

### 1.3 Estrategia de Testing (Verificada 13/03)
- **Frameworks**: Vitest (Unit), Playwright (E2E).
- **Cobertura Objetivo**: 90% (Crítica: 100% en `geminiService` y `types`).
- **Scripts Reales**: `test_e2e_completo.py` (valida Qdrant + LLM + RAG) y `test_mistral_agent_complete.py` (comparativa vs Claude).
- **Estado Actual**: 25 tests activos en `scripts/tests/`.

---

## 2. MOTOR DE GENERACIÓN — ESTADO REAL (V12) SE PREVE CREAR PLAN CONSOLIDADO V13 

### 2.1 Arquitectura Multi-Agente Productor-Crítico

```
Orquestador → Investigador (tools: search_rag + calculator) 
           → Redactor (genera caso)
           → Auditor Adversarial (verifica vs BOE)
           → [loop si hay errores]
```

### 2.2 Errores Críticos Identificados (Claude, 10/03/2026)

> ⚠️ **ATENCIÓN**: Estos errores están documentados en `conversacion_claude_full_resumen_10_03_26.md` y son el bloqueo principal para la calidad de los casos generados.

| # | Error | Impacto | Estado |
|---|-------|---------|--------|
| E1 | `verify_boe` no declarada en `generator.yaml` | LLM genera sin verificación real | ✅ **CORREGIDO** - Ya está en tools |
| E2 | Umbral jubilación 2026: `38.5` en lugar de `38.25` en `calculos_ss_extended.py` | Error sistemático en todas las preguntas de jubilación | ✅ **CORREGIDO 12/03** |
| E3 | `calculos_ss.py` no diferencia quién paga IT días 4-15 (empresa) vs 16+ (INSS) | Alucinaciones en sujeto pagador | ✅ **CORREGIDO** |
| E4 | RAG no filtra por `vigente=true` → artículos derogados contaminan resultados | LLM usa normas obsoletas | ✅ **CORREGIDO** - Priorizado en orquestador |
| E5 | Model string Claude incorrecto en `llm_providers.py` | Confusión en qué modelo se usa | ✅ **CORREGIDO** |
| E6 | `temperature: 0.3` para DeepSeek R1 (requiere `1.0`) | R1 se "compromete" con datos incorrectos | ✅ **CORREGIDO** |
| E7 | `MCPClient` instanciado globalmente al importar → `FileNotFoundError` en startup | Backend cae si MCP no activo | ⚠️ Pendiente lazy init |
| E8 | Dispatcher IT hardcodea `dia_baja=15` siempre | Ignora diferencias días 5 vs 22 vs 183 | ✅ **CORREGIDO V13.1** |

---

## 3. PROMPT MAESTRO — NIVEL DIEGO DE MIGUEL

> **Fuente:** Conversación Claude 10/03/2026 — Sistema Prompt definitivo para `generator.yaml`
> Implementa el método Diego de Miguel: identificar régimen jurídico → línea de tiempo → distractores desde errores reales.
nuevos datos y prompt: prompt_maestro_opositaia_COSMIC.md](file:///home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/prompt_maestro_opositaia_COSMIC.md) 
### 3.1 Estructura en 3 Fases Obligatorias

**FASE 0 — Consultas Previas (antes de escribir nada)**
- Mapa de materias: marcar con X cada bloque (Jubilación, IT_EC, IT_AT, BR_IT, IP, Alzada, Silencio, LCSP, RETA)
- Consulta obligatoria por materia marcada con `search_rag` + `ejecutar_calculo`
- Registrar DATOS_INMUTABLES verificados

**FASE 1 — Construcción de Trama**
- Mapa de personas (régimen, situación, fechas exactas)
- Línea de tiempo cronológica verificada
- Entrelazamiento causal entre al menos 2 materias

**FASE 2 — 15 Preguntas** (con PASO A→D para cada una)
- Identificar concepto a evaluar
- Localizar DATO_INMUTABLE de Fase 0
- 4 distractores desde errores reales de opositores y catalogo de trampas.
- Razonamiento: por qué correcta + por qué falsas + mnemotécnica

**FASE 3 — Autovalidación** (checklist antes de entregar)
```
□ Umbral jubilación 2026 = 38,25 (38a3m) — NO 38,5
□ BR de IT = promedio 3 meses — NO mes anterior/30
□ Plazo resolución alzada = 3 meses (Art.122.2) — NO 1 mes
□ Plazo interposición alzada = 1 mes (Art.121)
□ 15 preguntas son distintas entre sí
□ Vía procesal: LRJS para prestaciones SS, LPAC para AGE
□ Sin preguntas respondibles con "todos los anteriores" 
□ Hay que añadir más verificaciones!!!! 
```

---

## 4. CALCULADORAS SS — ESTADO REAL (12/03/2026)

**Archivo:** `backend/calculators/calculos_ss_extended.py` — **1982 líneas, sintaxis OK** 

## 4.1 Las 13 Calculadoras Verificadas (Estado Actual)
- **Jubilación**: Umbral 38.25 corregido en `calculos_ss_extended.py`
- **IT EC**: Diferencia pagador empresa (días 4-15) vs INSS (días 16+)
- **Subsidio Desempleo**: 70%/60% según semanas cotizadas
- **IMV**: Cuantías y umbrales actualizados 2026
- **Maternidad/Paternidad**: 16-18 semanas
- **Recargo Largo Plazo**: 40-50% según edad
- **Intereses Demora**: 10% anual + 25% recargo
- **LO 1/2023**: Incrementos por edad
- **Jubilación Anticipada**: Reducciones voluntaria/involuntaria
- **Cuotas Cotización**: Empresario/trabajador
- **Complementos Mínimos**: Pensiones no contributivas
- **Ayuda Hijo a Cargo**: Por descendientes
- **Bonificaciones Cuotas**: Reducciones cotización

---

## 5. ARQUITECTURA V13 "EL PREPARADOR" — PLAN DE IMPLEMENTACIÓN (Fase 17+)

### 5.1 Flujo Expandido V13
1. **Agente Investigador**: RAG + Calculator → Hechos.
2. **Agente Envenenador**: Inyecta Red Herrings + 65 Trampas del catálogo YAML.
3. **Agente Redactor**: Hila hechos con "veneno" → 15 preguntas + Enigmas de Calendario.
4. **Agente Auditor**: Verifica vs BOE + Equilibrio estadístico A/B/C/D.

### 5.2 Bloqueadores Inmediatos (Estado Actual)
1. **P0**: ✅ `verify_boe` ya está en `generator.yaml`.
2. **P1**: ⚠️ Filtro `vigente=true` pendiente en RAG.
3. **P2**: ✅ Temperatura 1.0 ya implementada en `llm_providers.py`.
4. **P3**: ❌ **6 LEYES CRÍTICAS NO INGESTADAS** - Ninguna de las 6 leyes está en Qdrant:
   - BOE-A-2021-21653 (Ley 21/2021 Reforma pensiones)
   - BOE-A-2022-12482 (RDL 13/2022 Ingresos RETA)
   - BOE-A-2023-5364 (LO 1/2023 Salud reproductiva)
   - BOE-A-2023-6945 (RDL 2/2023 Jubilación)
   - BOE-A-2022-14680 (RDL 16/2022 Empleadas hogar)
   - BOE-A-2004-11836 (RD 1415/2004 Recaudación SS)

---

## 6. REGLAS DE ORO (MANDATORIAS) 🛡️
1. **Barrera Temporal**: Prohibido citar legislación posterior a **04/03/2026**.
2. **Zero Alucinaciones**: Si el cálculo no coincide con la calculadora Python → caso descartado y reiterar o recrear.
3. **Formato AGE Oficial**: Preguntas 30-60 palabras. Sin dobles negaciones.
4. **Trazabilidad**: Todo dato normativo trazable a BOE XML.
5. **Agentes BMAD para codificacion en la ide**: Todos los agentes (`analyst`, `planner`, `dev`, `qa`) están instalados en `.agents/skills/`.
6. **AGENTES QUE USA LA APLICACION** /home/spas/OPOS_GEMINI_1/backend/agents YE EL SISTEMA ESTA EN /BACKEND, ROUTERS, DISPATCHER, CALULADORAS, ETC. 
---
---

## 7. HITOS V13.1 "SENTINEL" (17/03/2026) ✅
- **Sieve Math Activo:** Verificación real de 35 años (Jubilación) y base mes anterior (IT-AT).
- **DeepSeek R1 E2E:** Éxito total en el "Caso Beatriz" (Multi-personaje complex).
- **Resiliencia:** Retry loop (90s) para errores 429 de Mistral implementado.

*Firma: Antigravity AI + Claude — 17/03/2026*
