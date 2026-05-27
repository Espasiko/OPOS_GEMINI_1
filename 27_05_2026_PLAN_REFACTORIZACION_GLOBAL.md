# Plan de Refactorizacion Global — OPOS_GEMINI_1 + Cerebrito

**Fecha:** 27/05/2026
**Version:** 1.0
**Estado:** BORRADOR — NO APLICAR sin confirmacion de Spas
**Fuentes:** MCP Memory (Plan_Refactor_Calculadoras_Pendiente_29_04_2026, Backend_FastAPI, Cerebrito_Refactorizacion), Wiki OPOS_PROJECT, Graphify (commit 91a49f1b), PRD Cerebrito v1.1, VISION_360

---

## 0. Principio rector

**NO ROMPER NADA.** Cada paso se puede revertir. Cada paso tiene test de verificacion. Si un paso falla, se para y se revierte sin afectar los demas. No se tocan archivos protegidos (calculos_ss_extended.py, catalog_FINAL_v2.json, blueprints/, docker-compose.yml, .env.backend).

**Orden de ejecucion:** Las fases son SECUENCIALES. No empezar la siguiente hasta que la anterior pase todos los tests.

---

## 1. Estado actual — que hay y que molesta

### 1.1 Backend OPOS_GEMINI_1 (Python, puerto 8080)

| Archivo | LOC | Problema | Fuente |
|---------|-----|----------|--------|
| `calculators/calculos_ss_extended.py` | 2457 | Monolito, dificil de mantener, PROTEGIDO | MCP: Plan_Refactor_Calculadoras |
| `calculators/calculadora_age.py` | 1128 | Grande, candidato a partir | MCP: Backend_FastAPI |
| `agents/chandra_tools.py` | 743 | Vault tools duplicados con proxy_agente_escritor.py | Graphify + code review |
| `agents/mistral_tools.py` | 699 | Partes legacy (Qdrant, duplicados con dispatcher) | MCP: Backend_FastAPI |
| `agents/orchestrator.py` | 374 | Legacy, no usa function-calling, reemplazado por Chandra | MCP + Graphify |
| `agents/verification_agents.py` | ~40KB | Funciona, ESPECIFICO SS, no universal | code review sesion 26/05 |
| `agents/confidence_scorer.py` | ? | ESPECIFICO SS (cita LGSS, opciones A/B/C/D) | code review sesion 26/05 |
| `agents/reasoning_tracer.py` | ? | ESPECIFICO SS | code review sesion 26/05 |
| `calculators/constantes_2026.py` | 130 | Desordenado tras bug fixes | MCP: Backend_FastAPI |
| `proxy_agente_escritor.py` | 536 | Tools vault inline, duplicados con chandra_tools | Graphify |
| `routers/rag.py` | ? | LEGACY — usa Qdrant descartado | Wiki: Routers_Map |
| `routers/rag_v2.py` | ? | LEGACY — usa Qdrant | Wiki: Routers_Map |
| `routers/upload.py` | ? | LEGACY — sin conexion activa | Wiki: Routers_Map |
| `routers/user.py` | ? | LEGACY — Postgres no activo | Wiki: Routers_Map |
| Raiz del repo | ~28 scripts | Sueltos, sin organizar | Wiki: Estado_Mayo_2026 |

### 1.2 Plugin BMO Chatbot Plus (TypeScript)

| Archivo | LOC | Problema |
|---------|-----|----------|
| `FetchModelResponse.ts` | 2337 | 14 funciones (7 proveedores x 2 modos stream) |
| `main.ts` | 1287 | Mezcla lifecycle + profile management |
| `Commands.ts` | ~55K | Enorme, mezcla categorias |
| `view.ts` | 734 | Routing mezclado con vista |
| `AppearanceSettings.ts` | ~26K | Monolito settings |
| `OllamaSettings.ts` | ~24K | Monolito settings |

### 1.3 Duplicaciones detectadas (Graphify confirma)

Graphify muestra relacion directa entre `chandra_tools.py` y `proxy_agente_escritor.py` (shared connections). Ambos implementan:
- `read_obsidian_note()` / `tool_buscar_vault()`
- `create_obsidian_note()` / `tool_escribir_vault()`
- `update_obsidian_note()`
- `search_internet()` / `tool_tavily_search()`

Ademas `mistral_tools.py` duplica `buscar_rag_qdrant` (Qdrant descartado) y `calcular_prestacion_ss` (ya en dispatcher.py).

---

## 2. Arquitectura objetivo (decision firme PRD Cerebrito v1.1, 26/05/2026)

```
4 repos GitHub (Espasiko/):

1. obsidian-bmo-chatbot-plus  ← Plugin TypeScript (YA EXISTE)
2. OPOS_GEMINI_1              ← Backend OPOS Chandra (YA EXISTE)
3. cerebrito-backend           ← Backend Cerebrito universal (A CREAR)
4. shared-tools                ← Submodulo git con tools comunes (A CREAR)

shared-tools se monta como submodulo en repos 2 y 3.
```

---

## 3. Fases del plan

### FASE 0 — Snapshots y seguridad (30 min)

**Objetivo:** Puntos de retorno seguros antes de tocar nada.

| Paso | Accion | Verificacion | Reversible |
|------|--------|-------------|------------|
| 0.1 | `git tag v1.0-pre-cerebrito` en OPOS_GEMINI_1 | `git tag -l` muestra el tag | `git tag -d` |
| 0.2 | `git tag v1.0-multi-chat` en obsidian-bmo-chatbot-plus | idem | idem |
| 0.3 | Branch `refactor/clean-codebase` desde main en OPOS_GEMINI_1 | `git branch -a` | `git branch -D` |
| 0.4 | Branch `feature/cerebrito-v1.1` desde feature/multi-chat en BMO | idem | idem |
| 0.5 | Verificar que `py_compile calculos_ss_extended.py` pasa | exit code 0 | N/A (read-only) |
| 0.6 | Verificar que backend arranca: `curl localhost:8080/health` | HTTP 200 | N/A |

**Criterio de exito:** Tags creados, branches creados, backend arranca OK.

---

### FASE 1 — Crear shared-tools (estimado 2h)

**Objetivo:** Extraer tools comunes sin romper nada existente. Los archivos originales se convierten en facades que importan de shared-tools.

#### 1.1 Crear repo Espasiko/shared-tools

```
shared-tools/
  tools/
    __init__.py
    vault_tools.py       ← EXTRAER de proxy_agente_escritor.py (read, create, update) + chandra_tools.py (buscar, escribir)
    search_tools.py      ← EXTRAER search_internet() de proxy_agente_escritor.py
    pdf_tools.py         ← NUEVO (pypdf, cascada OCR) — Fase 1 Cerebrito
    capability.py        ← Clase abstracta tool base — Fase 1 Cerebrito
    telemetry.py         ← NUEVO — Fase 1 Cerebrito
    verification.py      ← NUEVO, configurable por vertiente — Fase 1 Cerebrito
  tests/
    test_vault_tools.py
    test_search_tools.py
  README.md
```

#### 1.2 Extraer vault_tools.py

**De donde sale:**
- `proxy_agente_escritor.py` lineas ~80-200: `read_obsidian_note()`, `create_obsidian_note()`, `update_obsidian_note()`, `get_obsidian_base_url()`, `detectar_ip_windows()`
- `chandra_tools.py`: `tool_buscar_vault()`, `tool_escribir_vault()`

**Como:**
1. Copiar funciones a `shared-tools/tools/vault_tools.py`
2. Parametrizar: recibir `base_url` y `api_key` como argumentos (no leer .env directamente)
3. En `proxy_agente_escritor.py`: `from shared_tools.tools.vault_tools import read_obsidian_note, create_obsidian_note, update_obsidian_note` — las funciones locales se borran
4. En `chandra_tools.py`: `from shared_tools.tools.vault_tools import buscar_vault, escribir_vault` — wrappers que llaman a las funciones comunes

**Test:** Backend arranca, `curl POST /v1/chat/completions` con mensaje "lee la nota index.md" funciona igual que antes.

#### 1.3 Extraer search_tools.py

**De donde sale:**
- `proxy_agente_escritor.py` lineas ~200-350: `search_internet()`, `_enrich_query_with_date()`, `_wrap_results_with_date_anchor()`
- `chandra_tools.py`: `tool_tavily_search()`

**Como:** Igual que vault_tools. Funciones originales se convierten en imports.

**Test:** `search_internet("test")` devuelve resultados.

#### 1.4 Montar submodulo

```bash
cd /home/spas/OPOS_GEMINI_1
git submodule add https://github.com/Espasiko/shared-tools.git shared-tools
```

**Test:** `python -c "from shared_tools.tools.vault_tools import read_obsidian_note; print('OK')"`

**Criterio de exito Fase 1:** Backend OPOS arranca y todas las tools funcionan identicamente. proxy_agente_escritor.py y chandra_tools.py importan de shared-tools. Zero duplicacion de vault/search tools.

---

### FASE 2 — Limpieza legacy backend (estimado 1.5h)

**Objetivo:** Eliminar codigo muerto sin afectar funcionalidad activa.

**IMPORTANTE:** Solo en branch `refactor/clean-codebase`. Main intacto.

#### 2.1 Routers legacy

| Router | Accion | Justificacion |
|--------|--------|---------------|
| `routers/rag.py` | Mover a `_legacy/` | Usa Qdrant (descartado, decision firme CLAUDE.md) |
| `routers/rag_v2.py` | Mover a `_legacy/` | Usa Qdrant |
| `routers/upload.py` | Mover a `_legacy/` | Sin conexion activa (Wiki: Routers_Map) |
| `routers/user.py` | Mover a `_legacy/` | Postgres no activo (Wiki: Routers_Map) |

**Como:** NO borrar. Mover a carpeta `backend/_legacy/` y quitar los `include_router()` de `main.py`.

**Test:** Backend arranca. `curl localhost:8080/opos/v1/models` responde. Chandra responde chat.

#### 2.2 Codigo legacy en agents/

| Archivo | Accion | Justificacion |
|---------|--------|---------------|
| `agents/orchestrator.py` | Mover a `_legacy/` | Legacy, no usa function-calling, reemplazado por Chandra (MCP + Graphify confirman) |
| `agents/mistral_tools.py` | Limpiar: borrar `buscar_rag_qdrant()` y `calcular_prestacion_ss()` | Qdrant descartado, duplicado con dispatcher (MCP: Backend_FastAPI) |

**Test:** Backend arranca. Chandra funciona. `dispatcher.py` importa OK.

#### 2.3 Scripts raiz

Mover los ~28 scripts sueltos de la raiz a `scripts/` o `_archive/` segun si son utiles o no:

| Destino | Criterio |
|---------|----------|
| `scripts/` | Scripts de utilidad activos (run_*.py, verify_*.py) |
| `_archive/` | Analisis, experimentos, one-offs (analisis_*.md, caso_*.md, etc.) |

**Test:** `git status` limpio despues del commit. Backend arranca.

**Criterio de exito Fase 2:** 4 routers legacy en `_legacy/`, orchestrator en `_legacy/`, mistral_tools limpio, raiz organizada. Backend funciona identico.

---

### FASE 3 — Refactor calculadoras (estimado 2-3h)

**Objetivo:** Partir `calculos_ss_extended.py` (2457 LOC) en submodulos sin perder funcionalidad.

**FUENTE AUTORITATIVA:** MCP entity `Plan_Refactor_Calculadoras_Pendiente_29_04_2026`

#### 3.1 Estrategia (aprendida del intento fallido 29/04)

El intento anterior fallo por conflicto de nombres: no se puede tener `calculos_ss.py` (archivo) y `calculos_ss/` (paquete) a la vez.

**Solucion confirmada:** Usar nombre `prestaciones_ss/` para el paquete nuevo.

```
backend/calculators/
  calculos_ss_extended.py     ← se convierte en FACADE (solo re-exports)
  calculos_ss.py              ← NO TOCAR (usado por dispatcher.py:145, :490)
  calculadora_age.py          ← fase posterior (1128 LOC)
  calculos_imv.py             ← OK como esta (319 LOC)
  calculadora_presupuesto.py  ← OK como esta (466 LOC)
  constantes_2026.py          ← reorganizar por dominio
  dispatcher.py               ← OK como esta (558 LOC, ya unifica)
  prestaciones_ss/             ← NUEVO paquete
    __init__.py               ← re-exporta todo (facade)
    jubilacion.py             ← Jubilacion, JubilacionParcial, BR DUAL, anticipada
    incapacidad.py            ← IT, IPT, IPP, IPA, Gran Incapacidad, LPNI, Riesgo Embarazo
    desempleo.py              ← Paro, cese actividad RETA
    maternidad.py             ← RGSS 19s, FP AGE, subsidio NC nacimiento
    viudedad_orfandad.py      ← Viudedad, orfandad, supervivencia
    cotizacion.py             ← Bases, MEI, Adicional Solidaridad
    recargos_lagunas.py       ← Art. 30, intereses, derivacion, Art. 322
    autonomos.py              ← RETA tramos, bonificaciones
    complementos.py           ← Minimos, hijo a cargo, brecha genero, PNC
    reglas_especiales.py      ← Art. 207.2, especies, IT pensionistas
```

#### 3.2 Migracion gradual (NO big-bang)

1. Crear `prestaciones_ss/` con `__init__.py` vacio
2. Mover UNA familia a la vez (empezar por `cotizacion.py` que es la mas aislada)
3. Despues de cada movimiento:
   - `py_compile calculos_ss_extended.py` → OK
   - `python -m pytest tests/verify_ss_calculators_2026.py` → OK (si existe)
   - Backend arranca → OK
4. `calculos_ss_extended.py` se convierte en facade:
   ```python
   # FACADE — mantiene imports legacy
   from .prestaciones_ss.jubilacion import *
   from .prestaciones_ss.incapacidad import *
   # ... etc
   ```
5. Los 3 archivos que importan (`verification_agents.py`, `dispatcher.py:145`, `dispatcher.py:490`, `tests/verify_ss_calculators_2026.py`) NO CAMBIAN porque el facade re-exporta todo

#### 3.3 Reorganizar constantes_2026.py

```python
# Secciones claras:
# --- COTIZACION ---
# --- PENSIONES ---
# --- IPREM ---
# --- EDADES ---
# --- COMPLEMENTOS ---
```

**Test:** `py_compile` + backend arranca + dispatcher funciona + Chandra responde calculos.

**Criterio de exito Fase 3:** `prestaciones_ss/` con 10 submodulos. `calculos_ss_extended.py` es facade. Todos los tests pasan. Chandra calcula identico.

---

### FASE 4 — Crear cerebrito-backend (estimado 3h)

**Objetivo:** Repo nuevo para el backend universal Cerebrito. Importa de shared-tools.

**NO toca OPOS_GEMINI_1.** Es repo independiente.

```
cerebrito-backend/
  pyproject.toml           ← Build flags para 4 SKUs
  cerebrito/
    main.py                ← FastAPI puerto 27182
    llm_router.py          ← Parsea @prefijo, elige proveedor
    llm_adapters/
      mistral_adapter.py
      groq_adapter.py
      ollama_adapter.py
      gemini_adapter.py
      deepseek_adapter.py
    agents/
      escritor_agent.py    ← Perfil escritor: vault + search + kuzu
      cerebrito_agent.py   ← Perfil generico
    kuzu/                  ← Grafo embebido (Fase 4 PRD)
  shared-tools/            ← Submodulo git
  tests/
```

**Test:** `curl localhost:27182/v1/models` devuelve lista. Chat basico funciona.

**Criterio de exito Fase 4:** Repo creado, proxy_agente_escritor.py migrado a cerebrito-backend, AgenteEscritor_Para_Nina apunta a nuevo backend.

---

### FASE 5 — Refactor plugin BMO (estimado 4-6h)

**Objetivo:** Partir archivos grandes del plugin en modulos. Solo en branch `feature/cerebrito-v1.1`.

| Paso | De | A | LOC |
|------|-----|---|-----|
| 5.1 | `FetchModelResponse.ts` | `providers/RestApiProvider.ts`, `providers/AnthropicProvider.ts`, `providers/MistralProvider.ts`, etc. | 2337 → ~300 cada uno |
| 5.2 | `main.ts` | `ProfileManager.ts` (gestion perfiles/prompts) + `main.ts` (lifecycle) | 1287 → ~700 + ~500 |
| 5.3 | `view.ts` | `ModelRouter.ts` (routing logica) + `view.ts` (UI) | 734 → ~300 + ~400 |
| 5.4 | `Commands.ts` | `ChatCommands.ts`, `EditorCommands.ts`, `NavigationCommands.ts` | ~55K → dividido |

**Test despues de cada paso:** `npm run build` pasa. Plugin carga en Obsidian. Chat funciona con REST API.

**Criterio de exito Fase 5:** Build OK, deploy a 1 vault de test, chat funciona.

---

## 4. Orden de ejecucion y dependencias

```
FASE 0 (snapshots)
  |
  v
FASE 1 (shared-tools)  ←--- prerequisito para Fases 2 y 4
  |
  ├──→ FASE 2 (limpieza legacy) — puede hacerse en paralelo con Fase 4
  |
  ├──→ FASE 3 (refactor calculadoras) — independiente, solo branch refactor/
  |
  └──→ FASE 4 (cerebrito-backend) — nuevo repo, no toca OPOS
  |
  v
FASE 5 (refactor plugin BMO) — independiente, solo branch feature/cerebrito-v1.1
```

**Fases 2, 3, 4, 5 son independientes entre si** (distintos repos o branches). Se pueden hacer en cualquier orden o en paralelo.

---

## 5. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|-------------|---------|------------|
| Conflicto nombre paquete (como 29/04) | BAJA (usamos `prestaciones_ss/`) | ALTO | Tag de rollback v1.0-pre-cerebrito |
| Import roto en dispatcher.py | MEDIA | ALTO | Facade en calculos_ss_extended.py re-exporta todo |
| Plugin no compila tras refactor | MEDIA | MEDIO | Branch aislada, vault de test |
| shared-tools submodulo no resuelve en CI | BAJA | MEDIO | Fallback: copiar archivos si submodulo falla |
| Backend OPOS deja de arrancar | BAJA | CRITICO | Test: `curl /health` despues de CADA paso |

---

## 6. Archivos PROHIBIDOS (no tocar en ninguna fase)

- `backend/calculators/calculos_ss_extended.py` — se convierte en FACADE, no se edita el contenido de las funciones
- `backend/data/catalog_FINAL_v2.json`
- `backend/v14/blueprints/`
- `docker-compose.yml`
- `.env.backend`

---

## 7. Verificacion post-refactor (checklist)

Despues de completar TODAS las fases:

- [ ] `git tag v1.0-pre-cerebrito` existe
- [ ] Backend OPOS arranca en puerto 8080
- [ ] `curl POST /opos/v1/chat/completions` con Chandra responde
- [ ] Calculadoras SS responden via dispatcher
- [ ] shared-tools es submodulo funcional
- [ ] cerebrito-backend arranca en puerto 27182
- [ ] BMO plugin compila (`npm run build`)
- [ ] Chat funciona en vault BOVEDA_OPOS (Chandra)
- [ ] Chat funciona en vault AgenteEscritor_Para_Nina
- [ ] Routers legacy en `_legacy/`, no en main.py
- [ ] Zero archivos sueltos en raiz (movidos a scripts/ o _archive/)
- [ ] `prestaciones_ss/` contiene 10 submodulos
- [ ] `calculos_ss_extended.py` es facade de re-exports

---

## 8. Tiempo total estimado

| Fase | Tiempo | Puede hacerse en paralelo |
|------|--------|--------------------------|
| 0 — Snapshots | 30 min | No (primero) |
| 1 — shared-tools | 2h | No (prerequisito) |
| 2 — Limpieza legacy | 1.5h | Si (con 3, 4, 5) |
| 3 — Calculadoras | 2-3h | Si (con 2, 4, 5) |
| 4 — cerebrito-backend | 3h | Si (con 2, 3, 5) |
| 5 — Plugin BMO | 4-6h | Si (con 2, 3, 4) |
| **Total secuencial** | **13-16h** | |
| **Total con paralelismo** | **7-9h** (Fase 0+1 serie, luego 2+3+4+5 paralelo) | |

---

## 9. Relacion con VISION_360 y otros planes

### Cosas que VISION_360 (15/05/2026) NO tiene y este plan SI:

- Plan Cerebrito completo (4 repos, shared-tools, SKUs)
- Arquitectura BMO interna (routing, profiles, prompts)
- Refactorizacion plugin BMO (8095 LOC TypeScript)
- Puerto 27182 para Cerebrito (decision firme 26/05)
- Workflows y Skills (* y # prefijos)
- Opciones ocultar carpeta BMO
- PRD Cerebrito v1.1 (con sandbox, seguridad, 4 SKUs vs 3)

### Cosas que VISION_360 tiene y este plan respeta:

- Calculadoras: plan identico al del MCP Memory (prestaciones_ss/, facade, migracion gradual)
- Routers legacy: coincide con Wiki Estado_Mayo_2026
- Archivos protegidos: coincide con CLAUDE.md
- Decision Qdrant descartado: plan elimina referencias legacy
- orchestrator.py legacy: plan mueve a _legacy/

---

*Plan generado el 27/05/2026 por Spas + Claude.*
*NO APLICAR hasta confirmacion explicita de Spas.*
