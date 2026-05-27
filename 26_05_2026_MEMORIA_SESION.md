# Memoria de Sesion — 26/05/2026

**Proyecto:** Cerebrito (BMO Chatbot Plus + OPOS Chandra) | **Workflow:** BMAD v1.2.0 | **MCP:** `Decisiones_Cerebrito_26_05_2026`

---

## 1. Resumen Ejecutivo

Sesion de iteracion PRD Cerebrito v1.0 -> v1.1 con **17 decisiones firmes**. Ejecucion del Plan Fase 0: **5 de 6 tareas completadas**. Pendiente: terminar Paso 5 (submodulo shared-tools en OPOS_GEMINI_1).

---

## 2. Decisiones Estrategicas (17 firmes)

### Arquitectura
| # | Decision | Detalle |
|---|----------|---------|
| 1 | **Kuzu vs Neo4j** | Core (Lite/Privacy) usa Kuzu embebido (~10 MB, 0 Docker). OPOS Pack/Server usa Neo4j (108 leyes). Sin migracion forzosa. |
| 2 | **Backend separados** | OPOS_GEMINI_1 (WSL+Docker, 8080, no tocar) + cerebrito-backend (nuevo, Windows, 27182) + shared-tools (submodulo). |
| 3 | **4 repos GitHub** | BMO plugin (existe) + OPOS_GEMINI_1 (existe) + cerebrito-backend (nuevo) + shared-tools (nuevo). |
| 4 | **SKUs via build flags** | Opcion B confirmada. Una sola codebase `main` con extras `pyproject.toml`: `cerebrito`, `cerebrito[privacy]`, `cerebrito[opos]`, `cerebrito[opos-server]`. NO branches por SKU. |
| 5 | **shared-tools como submodulo** | Almacen comun: capability, vault_tools, pdf_tools (cascada), search_tools, telemetry, verification. |
| 6 | **Puerto 27182** | Euler e x 10000, IANA sin asignar, >1024. Descartado 9000 por conflicto con PHP-FPM, Docker Registry, Portainer. |

### Producto/Licencia
| # | Decision | Detalle |
|---|----------|---------|
| 7 | **Licencia dual** | BMO plugin -> MIT (atribucion longy2k). Backend Cerebrito -> Commercial. Vaults -> propietarios. |
| 8 | **Vault Miguel Angel** | Fase 4.1: clonar Vault Nina + perfil hitita (Imperio Hitita 1650-1178 a.C.). Entrega USB/zip. |
| 9 | **Nina no migrar** | AgenteEscritor.exe sigue funcionando. Migracion opcional en Fase 4.2 tras validar Miguel Angel. |

### Tecnicas
| # | Decision | Detalle |
|---|----------|---------|
| 10 | **Capability framework** | Clase abstracta `Capability` universal con triggers, verification, requires_confirm, vertiente. Adapters por LLM: Mistral, Claude, Ollama, Groq, BMAD (oculto). |
| 11 | **Anti-alucinacion por vertiente** | `verification_level`: strict (opos/abogado), medium (investigador/autonomo), soft (estudiante), off (escritor). confidence_scorer y reasoning_tracer son ESPECIFICOS SS -> NO universales. |
| 12 | **Cascada PDF** | pypdf (rapido) -> Mistral OCR cloud (99%, 1000 pag/mes gratis) -> EasyOCR local (privacy, ~130 MB). 3 API keys Mistral ya configuradas. |
| 13 | **Smart Connections** | Reusar via mcp-tools, NO reimplementar. Ambos plugins ya en BOVEDA_OPOS conviven OK. |
| 14 | **Telemetria local Niveles 1+2** | `~/.cerebrito/telemetry.jsonl` + comando `/telemetria`. 100% legal sin papeleo. Nivel 3 NO inicialmente. |
| 15 | **Graphify killer feature** | Demo mapeo de cualquier codebase. Validado ahorro tokens **68%** con wiki cache. |
| 16 | **Refactor OPOS post-MVP** | Tag v1.0-pre-cerebrito como snapshot. NO tocar calculos_ss_extended.py (verificado BOE). Refactor BMO SI: dividir FetchModelResponse.ts, main.ts, Commands.ts. |
| 17 | **Modelo negocio TBD** | Pricing provisional 9-19EUR/mes. Definir tras competencia y validacion. |

---

## 3. Tareas Ejecutadas (Plan Fase 0)

| ID | Tarea | Estado |
|----|-------|:------:|
| p0 | Diagnosticar y arrancar backends Chandra (8080) y AgenteEscritor (8000) | **Completado** |
| p1 | Tags v1.0-pre-cerebrito (OPOS) y v1.0-multi-chat (BMO) | **Completado** |
| p2 | Crear repo Espasiko/shared-tools | **Completado** |
| p3 | Crear repo Espasiko/cerebrito-backend | **Completado** |
| p4 | Branches feature/cerebrito-v1.1 (BMO) y refactor/clean-codebase (OPOS) | **Completado** |
| p5 | Anadir submodule shared-tools (cerebrito done, OPOS pendiente) | **En progreso** |

### Detalle p0 — Diagnostico backends
- Problema: Chandra y Nina no funcionaban en Obsidian.
- Causa: Backends no estaban corriendo.
- Fix adicional: Proxy escritor tenia `PROXY_PORT=8080` en `.env.backend` (conflicto con Chandra). Solucionado arrancando con `PROXY_PORT=8000`.
- Verificacion: `curl http://127.0.0.1:8080/health` -> 200. `curl http://127.0.0.1:8000/health` -> 200.

### Detalle p1-p4 — Git ops
- Tag `v1.0-pre-cerebrito` en OPOS_GEMINI_1/main.
- Tag `v1.0-multi-chat` en obsidian-bmo-chatbot-plus/feature/multi-chat.
- Repo `Espasiko/shared-tools` creado con estructura: tools/, tests/, pyproject.toml, README, LICENSE MIT.
- Repo `Espasiko/cerebrito-backend` creado como **private** con estructura: cerebrito/, llm_adapters/, agents/, packaging/, tests/, pyproject.toml, shared-tools (submodulo).
- Branch `feature/cerebrito-v1.1` en BMO desde feature/multi-chat.
- Branch `refactor/clean-codebase` en OPOS desde main.
- **Error resuelto:** "Author identity unknown" en cerebrito-backend -> se configuro `user.name "spas"` y `user.email "spas@1H85102X71.localdomain"` localmente.

### Detalle p5 — Submodulo (en progreso)
- **cerebrito-backend (main):** Submodulo anadido, commiteado y pusheado OK.
- **OPOS_GEMINI_1 (refactor/clean-codebase):** Pendiente. Bloqueado por cambios locales sin commitear. Proximo comando:
  ```bash
  cd /home/spas/OPOS_GEMINI_1
  git checkout refactor/clean-codebase
  git submodule add https://github.com/Espasiko/shared-tools.git shared-tools
  git commit -m "chore: anadir shared-tools como submodulo"
  git push -u origin refactor/clean-codebase
  ```

---

## 4. Documentos Actualizados/Creados

| Documento | Ubicacion | Accion | Version |
|-----------|-----------|--------|:-------:|
| PRD Cerebrito | `obsidian-bmo-chatbot-plus/docs_planes/prd_cerebrito.md` | Actualizado | **v1.1** |
| Product Brief | `obsidian-bmo-chatbot-plus/docs_planes/product_brief_cerebrito.md` | Actualizado | **v1.1** |
| Project Overview | `obsidian-bmo-chatbot-plus/docs_planes/project_overview_cerebrito.md` | Actualizado | **v1.1** |
| Plan Fase 0 | `obsidian-bmo-chatbot-plus/docs_planes/fase_0_plan.md` | **Creado** | v1.0 |
| Plan proyecto | `obsidian-bmo-chatbot-plus/docs_planes/project_cerebrito_plan.md` | Actualizado | - |

---

## 5. Arquitectura Repos Confirmada

```
Espasiko/obsidian-bmo-chatbot-plus (BMO)          Espasiko/cerebrito-backend (NUEVO)
  TypeScript plugin                                   Python FastAPI 27182
  branches: main, feature/multi-chat,                 Kuzu embebido
            feature/cerebrito-v1.1                    Build flags 4 SKUs
  tag: v1.0-multi-chat
         |                                                  |
         v habla con REST API                               v
  Espasiko/OPOS_GEMINI_1 (OPOS)                          |
    Python FastAPI 8080                                   |
    Chandra 7 tools                                       |
    Neo4j 108 leyes                                       |
    branches: main, refactor/clean-codebase             |
    tag: v1.0-pre-cerebrito                               |
         |                                                  |
         +-----------------+-------------------------------+
                           v submodulo git
              Espasiko/shared-tools (ALMACEN)
                tools/capability.py
                tools/vault_tools.py
                tools/pdf_tools.py (cascada)
                tools/search_tools.py
                tools/telemetry.py
                tools/verification.py
```

### SKUs via pyproject.toml extras

| SKU | Comando pip | Extras | Tamano | Para quien |
|-----|-------------|--------|--------|------------|
| Core Lite | `pip install cerebrito` | base | ~50 MB | Escritores, estudiantes |
| Core Privacy | `pip install cerebrito[privacy]` | +easyocr | ~180 MB | Abogados |
| OPOS Pack | `pip install cerebrito[opos]` | +neo4j | ~700 MB | Opositores SS |
| OPOS Server | `pip install cerebrito[opos-server]` | +neo4j,+docker | ~3 GB | Power users |

---

## 6. Puertos Definitivos

| Puerto | Servicio | Estado |
|--------|----------|--------|
| 27123 | Obsidian Local REST API | Activo |
| 27182 | Cerebrito Core (nuevo) | Por implementar |
| 8080 | Chandra OPOS | Activo |
| 8000 | AgenteEscritor (DEPRECATED) | Activo |
| 7687 | Neo4j (Docker) | Activo (108 leyes, 6683 preceptos) |
| 11434 | Ollama | Instalado |
| 6333 | Qdrant (local) | Legacy, no critico |

---

## 7. Estado Neo4j (Sesiones Previas Relevantes)

- **108 leyes, 6683 preceptos, 6683 embeddings**
- **379 EXCEPCION_A, 517 comunidades Louvain**
- Embedding: pablosi/bge-m3-spa-law-qa-trained-2, dim=1024
- Catalogo: catalog_v17.6 (108 entradas)
- Boveda OPOS: `D:\BOVEDA_OPOS\BOVEDA_OPOS\`
- OPOS_PROJECT wiki: 25 paginas, Graphify 164 comunidades, 2010 nodos, 2938 edges

### 6 Leyes SS FALTANTES CRITICAS (pendiente ingesta)
1. RD 84/1996 — Reglamento Afiliacion, Altas y Bajas
2. RD 2064/1995 — Reglamento Cotizacion y Liquidacion
3. RD 1415/2004 — Reglamento Recaudacion SS
4. RD 1430/2009 — Gestion SS / IT
5. RD 1300/1995 — Incapacidad Permanente
6. Ley 39/2006 — Dependencia

---

## 8. Fases de Implementacion (Dependencias)

```
Fase 0 (estabilizacion) -> bloquea TODO
Fase 1 (tools) <-> Fase 2 (multi-modelo)  [paralelizables]
Fase 3 (UI) -> requiere Fase 1 + 2
Fase 4 (Kuzu) -> independiente, paralelo con Fase 1
Fase 4.1 (Miguel Angel) -> antes de Fase 5
Fase 5 (segundo cerebro) -> requiere Fase 4
Fase 6 (vertientes) -> tras validar piloto
Fase 7 (empaquetado 4 SKUs) -> al final
```

---

## 9. Pendientes Inmediatos

1. **Terminar Paso 5:** Submodulo `shared-tools` en `OPOS_GEMINI_1` branch `refactor/clean-codebase`.
2. **Paso 6 (sesion aparte):** Migrar tools comunes a `shared-tools` (vault_tools, pdf_tools) — analisis manual archivo por archivo.
3. **Paso 7 (sesion aparte, 4-8h):** Refactor BMO frontend — dividir `FetchModelResponse.ts`, extraer `ProfileManager` y `PluginLifecycle`, dividir `Commands.ts`.
4. **Ingesta 6 leyes SS faltantes** en Neo4j.
5. **Re-ingesta LO 3/1980** (BOE-A-1980-8648) con HTML parser (ingesta previa dio 0 paginas).

---

## 10. Tests E2E Verificacion Fase 0

```bash
# Test 1: Chandra OPOS responde
curl -X POST http://127.0.0.1:8080/opos/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"chandra","messages":[{"role":"user","content":"Hola Chandra"}]}'

# Test 2: AgenteEscritor (Nina) responde en Windows (manual)

# Test 3: BMO Plus cargado en BOVEDA_OPOS sin errores
# Obsidian Settings -> BMO Chatbot Plus -> ver consola -> 0 errores

# Test 4: Submodulo shared-tools funcional
cd /home/spas/cerebrito-backend
python -c "from shared_tools.tools.capability import Capability; print('OK')"

# Test 5: Tags y branches en lugar correcto
git -C /home/spas/OPOS_GEMINI_1 tag -l  # v1.0-pre-cerebrito
git -C /home/spas/obsidian-bmo-chatbot-plus tag -l  # v1.0-multi-chat
```

**Si los 5 tests pasan -> Fase 0 COMPLETADA.**

---

*Memoria generada el 26/05/2026 por Spas + Cascade.*  
*Referencias: PRD v1.1, Project Overview v1.1, fase_0_plan.md, MCP Entity Decisiones_Cerebrito_26_05_2026.*
