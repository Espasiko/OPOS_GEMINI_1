# 📘 Mejores Prácticas del Proyecto OpositaIA

## 1. Propósito del Proyecto

OpositaIA es un asistente RAG full-stack para exámenes públicos españoles (Seguridad Social). Ingiere fuentes legales (leyes BOE, jurisprudencia), materiales académicos y exámenes oficiales en bases de datos vectoriales (Qdrant Cloud/Local) y expone una API backend utilizada por un frontend para flujos de estudio como generación de Q&A, simulacros de examen y verificación de razonamiento legal. Incluye pipelines de generación y verificación de datasets con múltiples proveedores LLM.

## 2. Estructura del Proyecto

- **Raíz**
- **backend/** — Backend FastAPI, agentes, routers, tests, scripts de setup/migración
  - **agents/** — Agentes RAG, utilidades de ingesta/indexación, adaptadores de proveedores, herramientas
  - **routers/** — Routers API (ej. rag_v2.py, upload.py, chat.py)
  - **models/** — Esquemas y metadatos (ej. metadata_schema.py)
  - **tests/** — Suite Pytest para API, herramientas, rendimiento
  - **setup_qdrant_collection.py, migrate_qdrant_to_cloud.py** — scripts infra
  - **main.py** — Punto de entrada del backend
- **dataset_generator/** — Scripts de creación, verificación, enriquecimiento y análisis de datasets
  - **config.json** — configuración del pipeline de datasets
  - **varios generadores/verificadores** (mistral/groq/claude/local)
- **frontend/** — Frontend React/TypeScript (componentes, servicios, hooks, tests)
- **ai-specs/** — Especificaciones, estándares y logs de cambios
- **docs/** y múltiples *.md — Docs de arquitectura, decisiones, roadmaps, resúmenes
- **qdrant_storage/** — Almacenamiento local Qdrant (debe ignorarse en VCS)
- **.env*.example** — Plantillas de variables de entorno
- **docker-compose.yml, Dockerfile** — Containerización y orquestación local
- **requirements.txt** — Dependencias Python
- **README.md, SETUP.md** — Guías de inicio y configuración

### Convenciones:
- Separación de responsabilidades: ingesta/agentes vs. routers HTTP vs. modelos/esquemas
- Configuración dual de BD vectorial: Qdrant Cloud y Qdrant local (WSL/Docker)
- Configuración basada en env para credenciales y endpoints
- Pipeline de datasets vive en dataset_generator con scripts modulares y configs

## 3. Estrategia de Testing

### Frameworks:
- **Python:** Pytest para backend y scripts utilitarios (ej. backend/tests, test_* en raíz y dataset_generator)
- **Frontend:** Jest + React Testing Library (components/__tests__, services/__tests__, utils/__tests__, hooks/__tests__)

### Estructura:
- Tests de backend bajo backend/tests y archivos test_* a nivel raíz para checks E2E o integración
- Tests de frontend colocados por dominio (components, hooks, services, utils)

### Nomenclatura:
- **Python:** test_*.py, carpetas tests
- **Frontend:** *.test.ts/tsx colocados con carpetas de features

### Guías de Mocking:
- Mock servicios externos (APIs LLM, Qdrant), I/O de red y filesystem
- Usar fixtures para variables de entorno y payloads de muestra
- Para verificadores de datasets, suministrar inputs determinísticos y stub llamadas HTTP

### Unit vs Integration:
- **Tests unitarios** para lógica pura, validación de esquemas, tokenización/chunking, ensamblado de payloads
- **Tests de integración** para endpoints de routers, búsqueda RAG end-to-end, checks de cordura de ingesta (con colecciones de test)
- **Tests E2E** pueden apuntar a un stack docker-compose local con colecciones efímeras

### Expectativas de Cobertura:
- Lógica crítica de ingesta, validación de esquemas y routers API deben estar cubiertos
- Al menos smoke tests para pipelines de datasets y adaptadores de proveedores

## 4. Estilo de Código

### Python:
- Usar type hints donde sea factible; añadir modelos pydantic para payload/esquemas
- Preferir pathlib sobre os.path; usar logging en lugar de print
- Manejar operaciones de red con timeouts y reintentos; fallar rápido en vars env faltantes
- Estructurar agentes con funciones pequeñas para descargar → parsear → chunk → embed → upsert

### TypeScript/React:
- Componentes funcionales con hooks; mantener componentes presentacionales y delegar datos a servicios
- Tipado fuerte para servicios y hooks; evitar any
- Mantener estado local a menos que sea compartido; usar contexts para selección global de proveedor/modelo

### Nomenclatura:
- **snake_case** para módulos/funciones/variables Python
- **PascalCase** para componentes React y tipos/interfaces TypeScript
- **camelCase** para variables y funciones JS/TS

### Comentarios/Docs:
- Docstrings para funciones públicas, particularmente pasos de ingesta y transformaciones de esquemas
- Mantener justificación de alto nivel "por qué" en docs; "qué/cómo" en comentarios de código solo si no es obvio

### Manejo de Errores:
- Envolver I/O externo con try/except y lanzar excepciones significativas
- Validar inputs temprano; retornar respuestas de error estructuradas en routers
- Distinguir errores reintentables vs no-reintentables; log mensajes ricos en contexto

## 5. Patrones Comunes

### Patrón de ingesta RAG:
- Descargar → Extraer → Normalizar → Chunk → Embed → Upsert (por lotes)
- Payload enriquecido con layer, norma, artículo, proveniencia y timestamps

### Configuración dual Qdrant:
- Cambio basado en env entre local y cloud; almacenamiento sincronizado cuando sea necesario

### Abstracción de proveedores:
- Adaptadores de herramientas LLM centralizados; evitar esparcir código específico de vendor

### Config-first:
- Usar .env y config.json para endpoints, nombres de colecciones y elecciones de modelo

### Idiomas de testing:
- Usar factories/fixtures para payloads de muestra
- Snapshot tests para componentes presentacionales de frontend

### Logging:
- Logs estructurados con niveles e identificadores (colección, layer, número de lote)

## 6. Qué Hacer y Qué No Hacer

### ✅ Hacer:
- Cargar variables env vía dotenv; validar vars requeridas al inicio
- Usar Sessions de requests con reintentos/backoff y timeouts estrictos
- Hacer upserts vectoriales por lotes y reportar progreso con logs estructurados
- Mantener ingesta idempotente; verificar existencia antes de reprocesar
- Centralizar constantes (nombres de colecciones, URLs) en módulos de config
- Añadir tests unitarios para integridad de esquemas y metadatos
- Documentar nuevos scripts en README/SETUP y entradas .env.example

### ❌ No Hacer:
- Hardcodear API keys, URLs o nombres de colecciones en scripts
- Commitear qdrant_storage o datasets generados a menos que sea intencionado
- Usar print para logs operacionales; evitar fallos silenciosos
- Mezclar lógica UI con fetching de datos; mantener servicios separados
- Crear agentes monolíticos; preferir funciones y módulos componibles

## 7. Herramientas y Dependencias

### Backend:
- **FastAPI** (API), **pydantic** (esquemas), **qdrant-client** (BD vectorial), **transformers/torch** o **bge embeddings** (generación de embeddings), **requests/httpx** (HTTP)
- **dotenv** para configuración; **logging** para observabilidad; **pytest** para testing

### Frontend:
- **React + TypeScript**; **Jest + React Testing Library** para tests

### BD Vectorial:
- **Qdrant Cloud** y **Qdrant local** (WSL/Docker); scripts de sync/migración

### Proveedores LLM:
- Integraciones **Mistral/Groq/Claude** a través de pipelines de datasets y agentes

### Setup:
- **Python 3.10+** recomendado; instalar vía requirements.txt
- Usar **docker-compose** para stack local; asegurar que .env.backend y .env.example estén configurados
- Ejecutar tests vía **pytest** y **npm/yarn test** para frontend

## 8. Validaciones y Mejoras Críticas

### Validación Temprana:
- Varios scripts dependen de URL Qdrant, API Keys y nombres de colecciones. Añadir validación temprana para fallar rápido con mensajes accionables para evitar ejecuciones parciales y estado inconsistente durante ingesta

### Llamadas de Red Robustas:
- Las llamadas de red a PDFs BOE deben usar session con reintentos, backoff y timeouts estrictos para evitar cuelgues y estados parciales en ingesta

### Centralización de Configuración:
- Evitar esparcir constantes como nombres de colecciones y URLs a través de scripts centralizándolas en un módulo de config usado por herramientas de ingesta y migración

### Logging Estructurado:
- Los scripts contienen prints extensivos. Usar logging Python con niveles y formateo JSON opcional para integrar con logs Docker/K8s y permitir control de verbosidad

## 9. Notas Adicionales

### Seguridad:
- Secretos solo vía environment; mantener .env*.example actualizado
- Auditar cualquier key hardcodeada antes de publicar

### Gobernanza de Datos:
- Rastrear proveniencia (IDs BOE, referencias de artículos) en payloads
- Separar datasets verificados vs no verificados; nunca mezclar datos de test con fuentes de producción

### Rendimiento:
- Controlar tamaños de lote, concurrencia y parámetros de tokenización vía config
- Preferir modelos de embedding más pequeños y ajustados al dominio cuando sea factible

### Documentación:
- Mantener alineación de ai-specs/specs/base-standards.mdc y opositaia-standards.mdc
- Actualizar docs de plan y arquitectura cuando evolucionen layers de ingesta o esquemas

---

*Este documento establece las mejores prácticas para el desarrollo, mantenimiento y evolución del proyecto OpositaIA. Debe ser consultado regularmente y actualizado conforme el proyecto crezca.*