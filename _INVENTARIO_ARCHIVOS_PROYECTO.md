# Inventario Completo de Archivos — OPOS_GEMINI_1
> Generado: 23/05/2026 | Excluidos: .gitignore, .venv, node_modules, __pycache__

## RESUMEN

| Tipo | Cantidad | Nota |
|------|----------|------|
| .py | 175 | 119 backend + 28 raíz + 21 scripts + 3 scratch + 4 trampas |
| .md | 360 | 66 raíz + 125 docs/archive + ~50 docs/ + ~40 gastos_tokens + resto |
| .ts/.tsx | 306 | 60 frontend + 246 mcp-server (¡en gitignore!) |
| .json | 55 | 14 backend/data + 5 EXAMENES + 11 opos-agents + resto |
| .yaml/.yml | 21 | 12 opos-agents + backend + bmad-custom + docker-compose |
| .sh | 9 | scripts/maintenance + verificar |
| **TOTAL proyecto** | **926** | Sin contar BMAD ni IDE configs |

### BMAD overhead (framework copiado en ~10 IDEs)
| Carpeta | Archivos |
|---------|----------|
| _bmad/ | 1,144 |
| .agent + .agents + .claude + .cline + .continue + .cursor + .kiro + .opencode + .roo + .trae + .windsurf | 2,466 |
| **TOTAL BMAD** | **3,610** |

### Directorios top-level (49 carpetas)
```
backend/          ← CORE (157 archivos)
frontend/         ← React app (69 archivos sin node_modules)
docs/             ← Documentación (180+ archivos, 120 en archive/)
scripts/          ← Tests y maintenance (30 archivos)
opos-agents/      ← YAML agentes (14 archivos)
_bmad/            ← BMAD framework (1,144 archivos)
.agent/.agents/.claude/.cline/.continue/.cursor/.gemini/.github/.kiro/.opencode/.roo/.trae/.windsurf
                  ← IDE configs con BMAD duplicado (2,466 archivos)
brain/            ← 1 archivo (Mapa_Calculos_AGE)
powers/           ← 2 archivos (opositaia-rag)
bmad-custom-src/  ← 2 archivos (staff.md, custom.yaml)
design-artifacts/ ← VACÍO
scratch/          ← 3 archivos .py
EXAMENES_GENERADOS/ ← 5 JSON golden
gastos_ tokens/   ← Checkpoints, planes, docs duplicados
gastos_tokens/    ← TEMARIO_SS_2026
list_utracked_files/ ← 1 archivo
mcp-server/       ← En gitignore pero existe (6 .ts)
resultados/       ← 1 JSON piloto
```

---

## LISTING 1: Python (.py) — 175 archivos

### backend/ — 119 archivos
```
backend/__init__.py
backend/agents/__init__.py
backend/agents/agent_engine.py
backend/agents/boe_api_client.py
backend/agents/boe_downloader.py
backend/agents/chandra_tools.py
backend/agents/confidence_scorer.py
backend/agents/indexar_materiales_academia.py
backend/agents/indexer.py
backend/agents/ingest_all_missing_laws.py
backend/agents/ingest_cloud_master_v2.py
backend/agents/ingest_missing_4_laws.py
backend/agents/llm_providers.py
backend/agents/mistral_tools.py
backend/agents/orchestrator.py
backend/agents/patcher.py
backend/agents/pdf_processor.py
backend/agents/query_validator.py
backend/agents/rag_agent.py
backend/agents/rag_agent_v2.py
backend/agents/rag_helper.py
backend/agents/reasoning_tracer.py
backend/agents/salamandra_client.py
backend/agents/salamandra_memory.py
backend/agents/setup_semantic_cache.py
backend/agents/verification_agents.py
backend/calculators/__init__.py
backend/calculators/calculadora_age.py
backend/calculators/calculadora_presupuesto.py
backend/calculators/calculos_imv.py
backend/calculators/calculos_ss.py
backend/calculators/calculos_ss_extended.py
backend/calculators/constantes_2026.py
backend/calculators/dispatcher.py
backend/database/db.py
backend/database/init_db.py
backend/fase2_enriquecimiento_CORREGIDO.py
backend/main.py
backend/mcp_servers/legal_graph_mcp.py
backend/mcp_servers/test_mcps.py
backend/models/metadata_schema.py
backend/proxy_agente_escritor.py
backend/routers/__init__.py
backend/routers/ai_functions.py
backend/routers/boe.py
backend/routers/casos_practicos.py
backend/routers/chat.py
backend/routers/mcp_gateway.py
backend/routers/opos_chat.py
backend/routers/rag.py
backend/routers/rag_v2.py
backend/routers/upload.py
backend/routers/user.py
backend/run_chandra.py
backend/scripts/ (24 archivos)
backend/services/__init__.py
backend/services/boe_service.py
backend/stats_por_norma.py
backend/test_*.py (7 archivos)
backend/tests/ (2 archivos)
backend/trampas/ (4 archivos)
backend/utils/ (4 archivos)
backend/v14/ (18 archivos incl. 10 blueprints)
backend/verificar_qdrant.py
backend/verificar_sistema.py
```

### Raíz — 28 archivos
```
check_codigo_ss.py          check_neo4j_state.py
check_new_laws.py           check_ss_critical_laws.py
check_ss_exam_laws.py       consulta_directa_neo4j.py
debug_payload_qdrant.py     explore_calculations_fts.py
explore_calculations_neo4j.py  extract_exceptions_report.py
fetch_more.py               fix_cypher_queries.py
fix_ids.py                  get_art27.py
inject_exceptions.py        patch_agents.py
run_generator_v11_mistral_large.py  run_generator_v11_silent.py
run_injection.py            test_art173.py
test_articles.py            test_e2e_completo_v14_5.py
test_prose_validator_v14_5.py  test_queries.py
test_queries_neo4j.py       test_rag_calculators.py
verificar_neo4j.py          verify_v12_legal.py
```

### scripts/ — 25 archivos
```
scripts/maintenance/ (4 .py)
scripts/tests/ (17 .py)
scratch/ (3 .py)
```

---

## LISTING 2: Markdown (.md) — 360 archivos

### Raíz — 66 archivos (memorias, análisis, planes, verificaciones)
### docs/ — 180+ archivos (120 en archive/, resto en subdirectorios temáticos)
### gastos_ tokens/ — ~40 archivos (planes, correcciones, duplicados de docs/)
### Otros — backend/, opos-agents/, powers/, brain/, etc.

(Ver listing completo arriba en los resultados de búsqueda)

---

## LISTING 3: TypeScript (.ts/.tsx) — 60 frontend

```
frontend/App.tsx
frontend/components/ (21 componentes + 2 tests + 20 icons)
frontend/contexts/ModelContext.tsx
frontend/hooks/ (useAIProvider.ts + test)
frontend/services/ (backendService.ts, vpsService.ts + test)
frontend/utils/ (cache.ts, formatters.ts, providers.ts + 3 tests)
frontend/types.ts, index.tsx, vite configs
```

---

## LISTING 4: JSON — 55 archivos
## LISTING 5: YAML — 21 archivos
## LISTING 6: Shell (.sh) — 9 archivos

(Detalle en listings anteriores)
