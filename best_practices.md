# 📘 Project Best Practices

## 1. Project Purpose
OpositAIA is a multi-agent, RAG-powered study assistant focused on the Spanish Social Security C1 exam. It provides a React frontend, a FastAPI backend, and integrates vector search (Qdrant), LLM providers (Gemini, Mistral, Ollama), and content ingestion/agents to deliver grounded, article-cited responses and study tools (flashcards, mock exams, mind maps).

## 2. Project Structure
- Frontend (TypeScript + React + Vite)
  - App.tsx, components/, services/, hooks/, utils/, contexts/
  - Vitest for unit tests; __tests__/ contains setup and suites
  - ESLint + Prettier + TypeScript config enforced
- Backend (Python + FastAPI)
  - backend/main.py entrypoint, routers/, agents/, database/, models/, tests/
  - requirements.txt for pinned deps; .env.example and .env.production.example
  - Agents for RAG and content ingestion under backend/agents
  - Scripts for indexation and migrations in backend/
- Docs
  - docs/ and ai-specs/ with standards (frontend/backend/docs), architecture, data model, roadmap, RAG practices, testing strategy
  - Security audits under docs/project-docs/security/
- Infra
  - docker-compose.yml, vercel.json, vite.config.ts, vitest.config.ts, eslint.config.js

Guidelines
- Keep strict separation: frontend UI logic (components, hooks) vs backend APIs (routers, services, database).
- Use services/ for API calls and provider abstractions on the frontend; use routers/ and agents/ for endpoints and intelligence on the backend.
- Store environment config in .env files with documented .env.example templates.
- Keep architectural docs updated alongside changes (docs/, ai-specs/).

## 3. Test Strategy
- Frameworks: Vitest + @testing-library for frontend; Pytest for backend.
- Layout
  - Frontend: __tests__/ for setup, accessibility and integration tests; components and utils have focused unit tests under respective __tests__ directories.
  - Backend: backend/tests/ (ensure parity with routers and agents modules).
- Coverage
  - Vitest thresholds: 90% statements/branches/functions/lines. Enforce via CI.
  - Pytest: use pytest-cov and target 85–90% for critical modules (routers, agents, services). Exclude scripts and generated code.
- Mocking
  - Frontend: prefer Testing Library queries, user-event; mock network via MSW or vi.mock for services.
  - Backend: mock network/LLM/Qdrant via httpx mocking and fixtures; provide fake providers and in-memory stores.
- Test types
  - Unit: pure logic (formatters, providers, hooks), small components.
  - Integration: chat flow, RAG retrieval, provider selection, agents orchestration.
  - E2E: existing test_e2e_*.py are maintained; isolate from production data and run on ephemeral envs.

## 4. Code Style
- Frontend (TS/React)
  - Follow eslint.config.js rules; single quotes, semicolons, 2-space indent, max-len 120.
  - Prefer functional components, React hooks, and co-locate component-specific types.
  - Strong typing over any; avoid non-null assertions; use explicit return types for public APIs.
  - Async: prefer async/await, handle errors with typed error boundaries in services.
  - Naming: PascalCase for components, camelCase for variables/functions, kebab-case for files.
  - Keep components presentational; move side-effects/data fetching into hooks or services.
- Backend (Python/FastAPI)
  - Pydantic models for request/response; explicit response_model on routes.
  - Use dependency injection for sessions/clients; avoid global state unless memoized safely.
  - Logging: use module-level logger; structured messages; avoid printing secrets.
  - Error handling: raise HTTPException with clear messages; map provider errors to 4xx/5xx properly.
  - Async-first design: prefer async def routers; use httpx.AsyncClient and await all I/O.
  - Naming: snake_case for functions/vars, PascalCase for classes, kebab-case for scripts.

## 5. Common Patterns
- Providers as adapters: services/geminiService.ts and backend agents.llm_providers should expose a common interface (generate/generateStream) and feature flags (get_info()).
- RAG pipeline
  - Retrieve top-k×N, apply hierarchical/reranking boosts (capas), then trim to top-k.
  - Build explicit, instruction-rich prompts prioritizing law articles and explicit citations.
- Streaming SSE
  - Use StreamingResponse with well-formed SSE frames and [DONE] sentinel; disable proxy buffering via headers.
- Config
  - Load environment via dotenv; default to safe local values; document required envs.
- Database
  - Use connection/session helpers; wrap DB writes in try/except with logging and no hard failures in streaming.

## 6. Do's and Don'ts
- Do
  - Validate all inputs with schemas (frontend and backend). Use zod/yup on frontend; Pydantic on backend.
  - Protect secrets in env files; never log API keys or tokens.
  - Add types for API responses; centralize endpoints in services layer.
  - Keep routers thin; move business logic to agents/services.
  - Add unit tests on every utility and pure function; add integration tests for routes with external deps mocked.
  - Document new endpoints and data models in ai-specs/specs and docs/.
  - Restrict CORS in production; audit allowed origins/headers.
  - Use retry and timeouts in external HTTP calls.
- Don't
  - Don’t hardcode URLs or tokens in code.
  - Don’t perform blocking I/O in async routes.
  - Don’t bypass lint/type checks; fix warnings or justify suppressions.
  - Don’t couple components directly to fetch/HTTP; go through services.

## 7. Tools & Dependencies
- Frontend
  - Vite, React 19, TypeScript 5.8, Vitest, Testing Library, ESLint, Prettier.
- Backend
  - FastAPI, Uvicorn, Pydantic v2, httpx, qdrant-client, sentence-transformers, langchain, google-generativeai, prometheus-client.
- Setup
  - Install Node deps (npm i) and Python deps (pip install -r backend/requirements.txt).
  - Configure .env and backend/.env.backend from templates; verify with npm run dev and uvicorn backend/main.py.

## 8. Other Notes
- The repository contains extensive standards under ai-specs/specs (backend-standards.mdc, frontend-standards.mdc, documentation-standards.mdc) and should be treated as normative for code generation.
- Adhere to RAG_BEST_PRACTICES_NOV2025.md for indexing and retrieval; follow TESTING_STRATEGY.md for coverage and patterns.
- Streaming chat must accumulate full content server-side if persisted; otherwise document frontend-side persistence behavior.
- Ensure consistent path aliases '@' map to project root in vite and vitest.

3) Plan de acción propuesto (fases y tareas concretas)
Fase 1 — Observabilidad, seguridad y gobernanza
Logging y métricas
Integrar OpenTelemetry en backend (FastAPI) y propagar trace-id en SSE.
Estructurar logs en JSON con campos: conversation_id, provider, latency_ms, token_usage.
Guardrails
Añadir capa de validación/seguridad previa a LLM: filtros de PII, jailbreak heurístico y listas de deny-patterns.
Implementar thresholds de confianza y fallbacks de proveedor.
Secret management
Migrar .env sensibles a un gestor de secretos (Vault/KMS). Añadir pre-commit git-secrets.
Compliance
Políticas de retención de conversaciones y anonimización by default.
Documentación de lineage: versión del índice RAG, hash de corpus, fechas de compilación.
Entregables:

backend/middleware/observability.py (OTel, correlation IDs)
backend/guards/input_filters.py (PII/jailbreak)
Docs: SECURITY.md actualizado, flujo de rotación de secretos, retención de datos
Métricas de éxito:

95% de peticiones con trace-id correlacionado

0 incidentes de secretos en repositorio (CI scanning)
100% de llamadas a LLM con guardrails ejecutados
Fase 2 — RAG 2.5: calidad y evaluación continua
Indexación y retrieval
Incorporar re-ranking con cross-encoder (p. ej., bge-reranker-large) o ColBERT-lite.
Enriquecer metadata (fuente, autoridad, artículo, versión, BOE, fecha vigencia).
Implementar chunking semántico con títulos y contexto supra/intra sección.
Evaluación RAG
Crear datasets de queries-canónicas basadas en temario C1.
Métricas: NDCG@k, Recall@k, Answer faithfulness (con LLM-as-a-judge) y rate de citas correctas.
QA pipeline en CI
Ejecutar batería de evaluación RAG en CI con thresholds; bloquear merges si métricas caen.
Entregables:

backend/agents/rag/reranker.py
scripts/indexers/ con pipeline reproducible
backend/tests/eval/ con datasets y harness de métricas
Docs: RAG_EVALUATION.md con resultados baseline
Métricas de éxito:

+10–15% NDCG@5 vs baseline
90% de respuestas con cita válida a artículo

<5% alucinaciones detectadas por judge
Fase 3 — Resiliencia multi-proveedor y latencia
Orquestación y resiliencia
Strategy: selección de proveedor por costo/latencia/estado.
Circuit breakers y timeouts diferenciados por proveedor.
Retries con backoff y degradación controlada.
Caching
Cache semántico de consultas frecuentes (vector cache + TTL).
Embedding cache local con LRU y warm-up del índice.
Streaming robusto
Heartbeats cada N segundos, reintentos, y cierre limpio con [DONE].
En frontend: AbortController, reconexión, y acumulación segura.
Entregables:

backend/agents/llm_orchestrator.py (policy + health)
services/backendService.ts: manejo de abort/retry/timeout
Tests de streaming y reconexión en tests/integration
Métricas de éxito:

P95 de latencia < N ms definidos
Tasa de éxito > 99% bajo fallas intermitentes
Tasa de reconexión exitosa del stream > 98%
Fase 4 — Testing avanzado y seguridad continua
Testing
Suites de streaming con simulación de backpressure.
Providers matrix tests (groq/mistral/ollama simulados).
Fixtures para Qdrant in-memory o httpx-mock para RAG/LLM.
Seguridad
Pruebas automáticas de prompt injection y PII leakage (con data fuzzer).
Linting de prompts (estructura, instrucciones, citación obligatoria).
E2E
E2E que validen citas correctamente formateadas y matching a artículos reales.
Entregables:

backend/tests/test_stream_resilience.py
frontend tests/integration/chat-streaming.test.ts
security tests y promplinter
Métricas de éxito:

Cobertura: FE 90% (statements/branches), BE 85–90% en routers/agents
Cero vulnerabilidades críticas en SAST/DAST
E2E citación correcta >90%
4) Cambios específicos sugeridos en el código actual
chat.py (backend/routers/chat.py)
Añadir OpenTelemetry context y correlation-id en headers SSE.
Acumular full_content en streaming para persistencia trazable.
Try/except más granular alrededor de provider.generate_stream; métricas por error.
Validar provider en request.provider contra lista blanca controlada.
RAG Agent
Añadir reranker externo y capa de boosts configurable por metadata (ya hay boosts jerárquicos; elevar a módulo).
Registrar scores originales y finales; exportar para evaluación.
Frontend (services/backendService.ts)
Implementar abort, retry con backoff, y reporting de latencia por chunk.
Asegurar progressive rendering y cancelación limpia.
Ejemplo de acumulación en streaming (ilustrativo):

# dentro de chat_stream
full_content = ""
async for content in provider.generate_stream(...):
    full_content += content
    yield f"data: {json.dumps(chunk_data)}\n\n"
# luego de finalizar:
save_message_to_db(request.conversation_id, "assistant", full_content, request.provider)

Copy

Insert

5) Riesgos, supuestos y áreas a investigar
Supuestos
Qdrant está accesible y con versión estable compatible con nuevas features de filtros y scores.
Los proveedores LLM exponen métricas básicas o podemos medir latencia al nivel de cliente.
Riesgos
Aumento de latencia por reranking (mitigar con caching y top_k×N razonable).
Costos por judge LLM en evaluación (usar ventanas periódicas y muestreo).
Áreas a investigar
Estado de ColBERT-lite vs cross-encoders en corpus legal español en 2025.
Librerías guardrails específicas que mejor performen en español jurídico.
Estrategias de actualización incremental del índice legal (detección de cambios BOE y reindex selectivo).
Verificación criptográfica o hashing de corpus para compliance.
6) Métricas de éxito globales
Calidad de respuesta
Answer faithfulness > 0.9
Citas correctas y verificables > 90%
RAG
+10–15% NDCG@5 vs baseline
Recall@k consistente por tópicos del temario
Fiabilidad
P95 latencia objetivo por vista (definir budgets)
Tasa de éxito > 99% con reintentos y circuit breakers
Seguridad y gobernanza
0 secretos en repos
Guardrails ejecutados en 100% de solicitudes
Retención y anonimización validadas
7) Roadmap temporal propuesto
Semana 1: Observabilidad + guardrails + secret management
Semana 2: Reranker + evaluación RAG + datasets + baseline
Semana 3: Orquestador multi-proveedor + circuit breakers + caching
Semana 4: Testing avanzado (streaming/backpressure/providers matrix) + seguridad continua + CI gates
8) Cierre
El repositorio ya incorpora una base muy alineada con las prácticas de 2025. El plan anterior prioriza mejoras en observabilidad, seguridad, evaluación RAG y resiliencia multi-proveedor, con métricas claras y entregables concretos para integrar en el código actual, manteniendo la separación de capas, el enfoque async-first, y la trazabilidad necesaria para un producto en el dominio legal-educativo.

