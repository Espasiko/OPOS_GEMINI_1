# 🏗️ ARQUITECTURA ACTUAL DEL PROYECTO OPOSITAIA
**Fecha de Análisis:** 11 de febrero de 2026  
**Analista:** BMad Master  
**Estado:** Documentación de arquitectura existente (SIN MODIFICACIONES)

---

## 📋 RESUMEN EJECUTIVO

OpositaIA es una plataforma educativa para preparación de oposiciones de Seguridad Social española que actualmente tiene:

- ✅ **Backend FastAPI funcional** con 8 routers operativos
- ✅ **Frontend React** con 20+ componentes
- ✅ **Sistema RAG V2** con Qdrant + embeddings especializados
- ✅ **Multi-proveedor LLM** (Groq, Gemini, DeepSeek, Mistral local)
- ✅ **Base de datos PostgreSQL** para usuarios y progreso
- ⚠️ **Sistema de agentes** en fase de diseño (carpeta `opos-agents/`)
- ⚠️ **Datasets generados** pero no completamente integrados

---

## 🗂️ ESTRUCTURA DEL WORKSPACE

### Archivos en Raíz (Críticos)
```
OPOS_GEMINI_1/
├── .env                          # Variables de entorno globales
├── .env.backend.example          # Template para backend
├── docker-compose.yml            # Qdrant + PostgreSQL
├── pnpm-workspace.yaml           # Monorepo config
├── README.md                     # Documentación principal
└── [100+ archivos .md]           # Memorias, planes, investigaciones
```

**Observación:** La raíz está saturada con archivos de documentación, logs y scripts de prueba. Recomendación futura: mover a `docs/` o `archive/`.

---

## 🎯 BACKEND (FastAPI)

### Ubicación
```
backend/
├── main.py                       # ✅ Punto de entrada FastAPI
├── requirements.txt              # ✅ Dependencias Python
├── .env.backend                  # ✅ Config local
├── routers/                      # ✅ 8 routers activos
├── agents/                       # ✅ RAG Agent V2 + LLM providers
├── database/                     # ✅ PostgreSQL schema
├── scripts/                      # ⚠️ 50+ scripts (mantenimiento/tests)
└── tests/                        # ⚠️ Tests parciales
```

### Routers Activos (8)

| Router | Endpoint | Estado | Descripción |
|--------|----------|--------|-------------|
| `rag.py` | `/api/rag/*` | ✅ Legacy | RAG V1 (deprecado) |
| `rag_v2.py` | `/api/v2/rag/*` | ✅ **ACTIVO** | RAG con 2 capas + reranking |
| `chat.py` | `/chat/*` | ✅ **ACTIVO** | Chat streaming con Mistral + RAG |
| `ai_functions.py` | `/ai/*` | ✅ **ACTIVO** | 9 funciones IA (casos, mapas, flashcards) |
| `upload.py` | `/upload/*` | ✅ ACTIVO | Subida de archivos/URLs |
| `user.py` | `/user/*` | ✅ ACTIVO | Gestión de usuarios |
| `boe.py` | `/boe/*` | ✅ ACTIVO | API oficial BOE |
| `mcp_gateway.py` | `/mcp/*` | ✅ ACTIVO | Gateway MCP para otras IAs |

### Agentes Implementados

#### 1. RAG Agent V2 (`agents/rag_agent_v2.py`)
```python
class RAGAgentV2:
    """
    Sistema de 2 capas con reranking jerárquico
    
    Capa 1: Normativa Oficial (Leyes BOE)
    Capa 3: Materiales de Estudio
    
    Modelo: pablosi/bge-m3-spa-law-qa-trained-2 (1024 dims)
    """
    
    # Métodos principales:
    - search_documents()          # Búsqueda semántica
    - format_context_for_llm()    # Formateo para LLM
    - search_and_answer()         # Pipeline completo
```

**Características:**
- ✅ Embeddings especializados en legislación española
- ✅ Filtrado por capa (normativa vs materiales)
- ✅ Reranking jerárquico (leyes > jurisprudencia > materiales)
- ⚠️ Cohere Rerank comentado (no activo)

#### 2. LLM Providers (`agents/llm_providers.py`)
```python
# Proveedores disponibles:
- groq-8b          # Llama 3.3 8B (rápido)
- groq-70b         # Llama 3.3 70B (potente)
- gemini-flash     # Gemini 2.0 Flash
- gemini-pro       # Gemini 2.5 Pro
- deepseek-chat    # DeepSeek V3
- mistral-local    # Mistral en VPS (llama.cpp)
```

**Arquitectura Multi-Proveedor:**
```python
def get_provider(provider_id: str) -> LLMProvider:
    """Factory pattern para proveedores"""
    
async def generate_stream(messages, temperature, max_tokens):
    """Streaming unificado para todos los proveedores"""
```

---

## 🎨 FRONTEND (React)

### Ubicación
```
frontend/
├── App.tsx                       # ✅ Componente principal
├── index.tsx                     # ✅ Entry point
├── components/                   # ✅ 20+ componentes
├── services/                     # ✅ API clients
├── contexts/                     # ✅ React contexts
├── hooks/                        # ✅ Custom hooks
├── utils/                        # ✅ Utilidades
└── package.json                  # ✅ Dependencias
```

### Componentes Principales (20+)

**Navegación:**
- `Navbar.tsx` - Barra de navegación
- `Sidebar.tsx` - Menú lateral

**Funcionalidades Core:**
- `ChatInterface.tsx` - Chat con IA + RAG
- `PracticalCaseGenerator.tsx` - Generador de casos
- `MockExamGenerator.tsx` - Simulacros
- `MindMapGenerator.tsx` - Mapas mentales
- `FlashcardsGenerator.tsx` - Tarjetas de estudio
- `StudyPlanGenerator.tsx` - Planes de estudio

**Utilidades:**
- `SchemaGenerator.tsx` - Esquemas
- `SummaryGenerator.tsx` - Resúmenes
- `LawComparator.tsx` - Comparador de leyes
- `SearchWithGrounding.tsx` - Búsqueda actualizada

**Progreso:**
- `ProgressDashboard.tsx` - Dashboard de estadísticas

### Servicios API

#### `backendService.ts`
```typescript
// Cliente unificado para backend FastAPI
export const backendService = {
  // RAG
  searchRAG(query, options),
  
  // Chat
  streamChat(message, conversationId, useRAG),
  
  // AI Functions
  generatePracticalCase(topic, difficulty, provider),
  generateMockExam(topics, numQuestions, provider),
  generateMindMap(topic, provider),
  generateFlashcards(topic, numCards, provider),
  // ... 5 funciones más
  
  // Providers
  listProviders()
}
```

---

## 🗄️ BASES DE DATOS

### 1. Qdrant (Vector DB) - ACTUALIZADO 11/02/2026

**Estado:** ✅ OPERATIVO - Docker local + Qdrant Cloud

**Colecciones Locales (7 colecciones activas):**

| Colección | Puntos | Campos Metadata | Vectores | Estado | Uso Principal |
|-----------|--------|-----------------|----------|--------|---------------|
| **`opositaia_knowledge_FULL_XML`** | 12,090 | **48 campos** ✅ | Dense (1024D) + Sparse (BM25) | ✅ Green | **Ingesta directa XML con metadatos completos** |
| `opositaia_knowledge_v2` | 48,866 | 19 campos | Dense (1024D) | ✅ Green | RAG principal (legacy) |
| `opositaia_knowledge_hybrid_FULL` | 48,329 | 6 campos | Dense + Sparse | ✅ Green | Búsqueda híbrida |
| `opositaia_knowledge_hybrid` | 48,866 | 6 campos | Dense + Sparse | ✅ Green | Búsqueda híbrida legacy |
| `opositaia_leyes_master` | 54 | 15 campos | Dense (1024D) | ✅ Green | Catálogo de leyes |
| `leyes_espana` | 1,067 | ~10 campos | Dense (1024D) | ✅ Green | Leyes españolas |
| `opositaia_memory_mcp` | 2 | ~5 campos | Dense (1024D) | ✅ Green | Memoria MCP |

**Total chunks locales:** ~157,274 puntos vectoriales

#### Colección Principal: `opositaia_knowledge_FULL_XML` (48 campos)

**Metadatos Completos del XML BOE:**

```yaml
Campos Básicos (8):
  - boe_id: "BOE-A-2010-1331"
  - law_name: "Real Decreto 4/2010..."
  - article_title: "Artículo 48"
  - text_snippet: Contenido del chunk
  - chunk_index: 0
  - total_chunks: 1
  - tokens: 116
  - vigente: true

Campos Temporales (6):
  - fecha_publicacion: "20100129"
  - fecha_vigencia: "20100130"
  - fecha_disposicion: "20100108"
  - fecha_actualizacion: "20251219T123624Z"
  - fecha_actualizacion_payload: timestamp
  - fecha_derogacion: null (si aplica)

Campos Administrativos (8):
  - organismo_emisor: "Ministerio de la Presidencia"
  - departamento_codigo: "7710"
  - rango: "Real Decreto"
  - rango_codigo: "1340"
  - ambito: "Estatal"
  - ambito_codigo: "1"
  - diario: "Boletín Oficial del Estado"
  - diario_numero: "25"

Campos de Estado (5):
  - estatus_derogacion: "N"
  - estatus_anulacion: "N"
  - vigencia_agotada: "N"
  - estado_consolidacion: "Finalizado"
  - numero_oficial: "4/2010"

Campos de Referencias Legales (12):
  - deroga_a: [lista de normas derogadas]
  - derogado_por: [lista de normas que derogan]
  - modifica_a: [lista de normas modificadas]
  - modificado_por: [lista de normas que modifican]
  - añade_a: [lista de normas añadidas]
  - añadido_por: [lista de normas que añaden]
  - desarrolla_a: [lista de normas desarrolladas]
  - sustituye_a: [lista de normas sustituidas]
  - sustituido_por: [lista de normas que sustituyen]
  - transpone_a: [lista de directivas transpuestas]
  - otras_anteriores: [otras referencias anteriores]
  - otras_posteriores: [otras referencias posteriores]

Campos de Conteo (4):
  - num_deroga: cantidad de normas derogadas
  - num_derogado_por: cantidad de normas que derogan
  - num_modifica: cantidad de normas modificadas
  - num_modificado_por: cantidad de normas que modifican

Campos de URLs (2):
  - url_boe: "https://www.boe.es/buscar/act.php?id=BOE-A-2010-1331"
  - url_eli: "https://www.boe.es/eli/es/rd/2010/01/08/4"

Campos Estructurados (3):
  - materias: [lista de materias con códigos]
  - metadata_xml: {objeto JSON completo del XML}
  - notas: [notas adicionales]
```

**Configuración Vectorial:**
```yaml
Vectores Dense:
  - Dimensiones: 1024
  - Modelo: pablosi/bge-m3-spa-law-qa-trained-2
  - Distancia: Cosine

Vectores Sparse (BM25):
  - Vocabulario: 14,666 términos únicos
  - Promedio: 4 términos por chunk
  - Índices: uint32
  - Valores: float32

HNSW Config:
  - m: 16
  - ef_construct: 100
  - full_scan_threshold: 10000
  - on_disk: false
```

**Comparación de Colecciones:**

| Característica | FULL_XML | knowledge_v2 | hybrid_FULL | leyes_master |
|----------------|----------|--------------|-------------|--------------|
| Metadatos completos | ✅ 48 campos | ⚠️ 19 campos | ❌ 6 campos | ⚠️ 15 campos |
| Referencias legales | ✅ Completas | ❌ No | ❌ No | ⚠️ Parciales |
| Vigencia temporal | ✅ Sí | ✅ Sí | ❌ No | ✅ Sí |
| Sparse vectors (BM25) | ✅ Sí | ❌ No | ✅ Sí | ❌ No |
| Metadata XML completo | ✅ Sí | ❌ No | ❌ No | ❌ No |
| Relaciones normativas | ✅ Sí | ❌ No | ❌ No | ❌ No |

**Conclusión:** La colección `opositaia_knowledge_FULL_XML` es la **MÁS COMPLETA** con 48 campos de metadatos, incluyendo todas las referencias legales, vigencia temporal, y el XML completo del BOE.

**Capas Implementadas:**
- **Capa 1:** Normativa Oficial (Constitución, LGSS, Leyes, RDs)
- **Capa 3:** Materiales de Estudio (Tests, Temarios, Casos)

### 2. PostgreSQL

**Schema:** `backend/database/schema.sql`

```sql
-- Tablas implementadas:
CREATE TABLE user_progress (...)      -- Progreso del usuario
CREATE TABLE answer_history (...)     -- Historial de respuestas
CREATE TABLE user_cases (...)         -- Casos creados
CREATE TABLE simulacros (...)         -- Simulacros realizados
CREATE TABLE mind_maps (...)          -- Mapas mentales
CREATE TABLE study_sessions (...)     -- Sesiones de estudio
CREATE TABLE recommendations (...)    -- Recomendaciones IA
CREATE TABLE rag_queries (...)        -- Logs de búsquedas RAG
```

**Estado:** ✅ Schema definido, ⚠️ Integración parcial con frontend

---

## 🤖 SISTEMA DE AGENTES (EN DISEÑO)

### Ubicación: `opos-agents/` (12 items)

```
opos-agents/
├── config.yaml                   # ⚠️ Config de agentes (diseño)
├── agents/                       # ⚠️ Vacío (no implementado)
├── prompts/                      # ⚠️ Vacío
├── tools/                        # ⚠️ Vacío
├── workflows/                    # ⚠️ Vacío
├── docs_ideas_sistema_agentes/   # 📚 Documentación de diseño
└── 12_01_26_deepseek_v3_mcp_informe.md  # ✅ Informe DeepSeek V3 + MCP
```

### Config Actual (`config.yaml`)

```yaml
models:
  local_finetuned:
    name: "salamandra-opos"
    url: "https://electroyhogarpelotazo.tienda/salamandra/reason"
    
  cloud_fast:
    name: "llama-3.3-70b-versatile"
    provider: "groq"
    
  cloud_reasoning:
    name: "deepseek-chat"
    provider: "deepseek"

rag:
  qdrant_url: "http://localhost:6333"
  collection: "opositaia_knowledge_hybrid_FULL"
  embedding_model: "pablosi/bge-m3-spa-law-qa-trained-2"
```

### Informe DeepSeek V3 + MCP (12/01/2026)

**Resultado:** ✅ **ÉXITO COMPLETO**

**Modelo:** `deepseek-ai/DeepSeek-V3` vía Novita AI/HuggingFace
**Caso Generado:** Incapacidad Permanente Total - Conductor de autobús
**Calidad:** 
- ✅ Razonamiento explícito paso a paso
- ✅ Citas legales precisas (URLs BOE reales)
- ✅ Cálculos numéricos correctos
- ✅ Formato JSON estructurado

**MCPs Integrados:**
- ✅ Local RAG: `mcp-server/` (Disponible)
- ⚠️ BOE Verify: `ComputingVictor/MCP-BOE` (Instalado parcialmente)

**Recomendación:** Usar DeepSeek-V3 para generación de casos complejos (~$2-3 por 1,000 casos vs $30-40 con Claude)

**Estado:** 🚧 Diseño conceptual, NO implementado en código funcional

### Plan de Implementación (docs/16_01_26_AGENTIC_RAG_PLAN.md)

**6 Fases Definidas:**
- FASE 0: Re-ingestión + Colección Master (4-6h) 🔴 BLOQUEANTE
- FASE 1: Infraestructura (2h)
- FASE 2: Componentes RAG (5h) - Query expansion, Reranker, Hybrid search
- FASE 3: Legal Judge + BOE API (3h)
- FASE 4: Pipeline + FastAPI (4h)
- FASE 5: Testing + Benchmark (3h)

**Total estimado:** 21-23h (3-4 días)

**Componentes Diseñados:**
- Query Expansion con VPS fallback (Salamandra)
- Relevance Filter (Salamandra)
- BGE Reranker (local 350MB)
- Hybrid Search (Dense + Sparse)
- Legal Judge Agent (DeepSeek Reasoner)
- Agentic Pipeline integrado

---

## 📊 DATASETS GENERADOS

### Ubicación: `dataset_generator/` (140 items)

```
dataset_generator/
├── dataset_output/               # 50+ archivos (casos, simulacros, QA)
├── dataset_output_CLEAN/         # 12 archivos limpios (sin PII)
├── premium_content/              # 10 subdirectorios por modelo
│   ├── claude_extreme/
│   ├── deepseek_extreme/
│   ├── deepseek_gold_batch/
│   ├── groq_extreme/
│   ├── mistral_extreme/
│   └── mistral_night_mode/
├── golden_dataset/               # Dataset validado final
│   ├── standard/                 # QA estándar
│   ├── enriched/                 # Exámenes enriquecidos
│   ├── special/                  # Flashcards, diálogos
│   └── DATASET_GAPS_REPORT.md    # ⚠️ Faltan 250 items
├── multi_model_20_12/            # Batches multi-modelo
├── rejected/                     # 50+ casos rechazados
├── archive/                      # Outputs antiguos
└── [126+ scripts Python]         # Generadores con múltiples LLMs
```

### Datasets Principales

| Dataset | Ubicación | Items | Estado |
|---------|-----------|-------|--------|
| **MASTER_DATASET_v9_GOLD_OPTIMIZED** | dataset_generator/ | ~12k casos | ✅ Generado |
| **groq_500_qa_verified.jsonl** | golden_dataset/standard/ | 500 QA | ✅ Validado |
| **mistral_legacy_qa_consolidated.jsonl** | golden_dataset/standard/ | 671 QA | ✅ Validado |
| **deepseek_extreme_cases.jsonl** | golden_dataset/standard/ | 150 casos | ✅ Validado |
| **official_exams_enriched_mistral.jsonl** | golden_dataset/enriched/ | 5000+ | 🔄 En progreso |
| **MASTER_DATASET_v12_PLATINUM** | Raíz | ~12k casos | ✅ Generado |
| **gran-basurero.jsonl** | Raíz | 52 MB | ⚠️ Casos descartados |

### Scripts de Generación (126+)

**Por Modelo:**
- **DeepSeek:** 10+ scripts (reasoning, batch, premium)
- **Groq:** 15+ scripts (batch, premium, experiments)
- **Mistral:** 20+ scripts (local, API, night mode)
- **Claude:** 5+ scripts (extreme quality)
- **Gemini:** 3+ scripts (comparativas)

**Por Tipo:**
- Casos prácticos: 30+ scripts
- QA/Tests: 25+ scripts
- Flashcards: 5+ scripts
- Simulacros: 10+ scripts
- Consolidación: 15+ scripts
- Verificación: 20+ scripts

### Gaps Identificados (DATASET_GAPS_REPORT.md)

| Tipo | Objetivo | Actual | GAP |
|------|----------|--------|-----|
| Simulacro Examen | 50 | 0 | ❌ **50** |
| Esquema Estructurado | 50 | 0 | ❌ **50** |
| Comparativa Legal | 30 | 0 | ❌ **30** |
| Plazos Procedimiento | 20 | 0 | ❌ **20** |
| Razonamiento Legal | 100 | 0 | ❌ **100** |

**Total faltante:** 250 items antes de fine-tuning

**Estado:** ✅ Datasets generados masivamente, ⚠️ No servidos por API, ⚠️ Gaps identificados

---

## 🔧 SCRIPTS Y UTILIDADES

### Backend Scripts (`backend/scripts/`) - 52 scripts

**Categorías:**
1. **Ingesta de datos** (15+ scripts en `backend/agents/`)
   - `ingest_full_db_MAXIMUM.py`
   - `reingest_qdrant_v3.py`
   - `migrate_cloud_to_hybrid_local.py`
   - `05_01_26_ingest_exams_pipeline.py`

2. **Evaluación de modelos** (5+ scripts)
   - `06_01_26_salamandra_FINAL.py`
   - `compare_hybrid_EXCELLENT_2026.py`
   - `dry_run_salamandra_ultra.py`

3. **Procesamiento de exámenes** (5+ scripts)
   - `05_01_26_ingest_exams_pipeline.py`
   - `05_01_26_parse_questions.py`

4. **Tests y verificación** (10+ scripts)
   - `TEST_RAG_PIPELINE.py`
   - `verify_ingestion_*.py`

### Scripts Organizados (`scripts/`)

```
scripts/
├── tests/                        # 28 scripts de testing
│   ├── test_agente_*.py          # Tests de agentes
│   ├── test_mistral_*.py         # Tests Mistral (10+ scripts)
│   ├── test_claude_*.py          # Tests Claude
│   ├── test_rag_*.py             # Tests RAG
│   └── test_e2e_*.py             # Tests end-to-end
├── maintenance/                  # 18 scripts de mantenimiento
│   ├── check_*.py                # Verificación de estado
│   ├── verificar_*.py            # Verificación de datos
│   ├── limpiar_*.py              # Limpieza
│   ├── reindexar_*.sh            # Re-indexación
│   └── url_verifier.py           # Verificador de URLs BOE
└── verify_dataset_rag.py         # Verificación dataset-RAG
```

### Root Scripts (100+ archivos)

**Tipos:**
- `test_*.py` - Tests de integración (30+)
- `verify_*.py` - Verificación de datos (15+)
- `consolidate_*.py` - Consolidación de datasets (10+)
- `generate_*.py` - Generación de contenido (5+)
- `audit_*.py` - Auditorías (5+)
- `deepseek_*.py` - Scripts DeepSeek (10+)
- `query_*.py` - Tests de queries (5+)
- Otros: debug, fix, extract, etc. (20+)

**Observación:** Muchos scripts son experimentales o de una sola vez. Candidatos para archivo en `docs/archive/`.

---

## 📚 DOCUMENTACIÓN

### Estructura

```
docs/ (279 items)
├── 01_arquitectura/              # Documentos de arquitectura
├── 02_planes/                    # 11 planes estratégicos
├── 03_investigacion/             # Investigaciones técnicas
├── 04_datasets/                  # Documentación de datasets
├── 08_guias/                     # Guías de uso
├── 10_memoria/                   # Memorias de sesiones
├── Iideas_rama_gemini/           # 54 ideas y experimentos
├── archive/                      # 131 documentos archivados
├── 16_01_26_AGENTIC_RAG_PLAN.md  # ✅ Plan completo RAG (6 fases)
├── 16_01_26_INVENTARIO_SISTEMA.md # ✅ Inventario exhaustivo
└── MULTI_AGENT_ARCHITECTURE.md   # ✅ Diseño de agentes

Raíz (100+ .md):
├── 21_12_25_mapa_arquitectura_completo.md
├── 26_12_ESTRATEGIA_FINAL_RAG.md
├── PLAN_DESARROLLO_2026.md
├── 01_01_26_BD_RAG_MEMORIA.MD
├── 14_01_26_MEMORIA_DEEPSEEK_ARREGLO.md
├── 07_01_26_MEMORIA_ESTADO.md
├── 060126_memoria_mcp_vps_salamandra.md
└── [97+ archivos más]            # ⚠️ Desorganizado
```

### Documentación Clave

**Planes Estratégicos:**
- `docs/16_01_26_AGENTIC_RAG_PLAN.md` - Plan completo de 6 fases para RAG agentic
- `PLAN_DESARROLLO_2026.md` - Roadmap 2026
- `26_12_ESTRATEGIA_FINAL_RAG.md` - Estrategia RAG
- `24_12_OPOS_PLAN_COMPLETO.md` - Plan completo del proyecto

**Arquitectura:**
- `docs/MULTI_AGENT_ARCHITECTURE.md` - Diseño sistema de agentes
- `docs/1_AI_AGENTS.md` - Definición de agentes IA
- `21_12_25_mapa_arquitectura_completo.md` - Mapa completo
- `ARQUITECTURA_ACTUAL_20_01_26.md` - Este documento

**Inventarios:**
- `docs/16_01_26_INVENTARIO_SISTEMA.md` - Inventario exhaustivo (local + VPS)
- `25_12_INVENTARIO_DATASETS_COMPLETO.md` - Inventario de datasets
- `21_12_25_inventario_jsonl.md` - Inventario JSONL

**Memorias de Sesiones:**
- `01_01_26_BD_RAG_MEMORIA.MD` - Memoria BD y RAG
- `14_01_26_MEMORIA_DEEPSEEK_ARREGLO.md` - Arreglo DeepSeek
- `060126_memoria_mcp_vps_salamandra.md` - MCP + VPS + Salamandra
- `07_01_26_MEMORIA_ESTADO.md` - Estado del proyecto

**Observación:** Documentación extensa pero dispersa. Necesita consolidación en `docs/` con estructura clara.

---

## 🚀 FLUJOS OPERACIONALES ACTUALES

### 1. Chat con RAG (✅ FUNCIONAL)

```
Usuario escribe mensaje
    ↓
Frontend: ChatInterface.tsx
    ↓
API: POST /chat/stream
    ↓
Backend: chat.py
    ├─→ RAG Agent V2: search_documents()
    │   ├─→ Qdrant: búsqueda semántica
    │   └─→ Reranking jerárquico
    ├─→ LLM Provider: generate_stream()
    │   └─→ Groq/Gemini/DeepSeek/Mistral
    └─→ Streaming SSE al frontend
```

### 2. Generación de Casos Prácticos (✅ FUNCIONAL)

```
Usuario solicita caso
    ↓
Frontend: PracticalCaseGenerator.tsx
    ↓
API: POST /ai/practical-case
    ↓
Backend: ai_functions.py
    ├─→ LLM Provider (groq-70b por defecto)
    └─→ Prompt especializado + JSON schema
    ↓
Respuesta JSON parseada
    ↓
Frontend: Renderiza caso + preguntas
```

### 3. Simulacros de Examen (✅ FUNCIONAL)

```
Usuario configura simulacro
    ↓
Frontend: MockExamGenerator.tsx
    ↓
API: POST /ai/mock-exam
    ↓
Backend: ai_functions.py
    ├─→ Generación en lotes (10-15 preguntas/lote)
    └─→ LLM Provider (groq-70b o gemini-pro)
    ↓
Respuesta JSON con 100 preguntas
    ↓
Frontend: Modo examen con timer
```

---

## 🔌 INTEGRACIONES EXTERNAS

### APIs Activas

| Servicio | Uso | Estado |
|----------|-----|--------|
| **Groq** | LLM rápido (Llama 3.3) | ✅ ACTIVO |
| **Gemini** | LLM potente (2.5 Pro) | ✅ ACTIVO |
| **DeepSeek** | Reasoning (V3) | ✅ ACTIVO |
| **Mistral VPS** | LLM local (llama.cpp) | ✅ ACTIVO |
| **BOE API** | Datos oficiales | ✅ ACTIVO |
| **Cohere** | Reranking | ⚠️ Configurado pero no usado |
| **Novita AI** | DeepSeek V3 vía HF | ✅ ACTIVO |

### Modelos Locales

| Modelo | Ubicación | Estado |
|--------|-----------|--------|
| **Salamandra 7B** | VPS (llama.cpp) | ✅ Desplegado |
| **bge-m3-spa-law-qa** | Local (sentence-transformers) | ✅ Activo |
| **Salamandra GGUF** | model_gguf/ (Q4_K_M) | ✅ Disponible |

### Kiro Powers

**Ubicación:** `powers/opositaia-rag/`

```
powers/opositaia-rag/
├── POWER.md                      # ✅ Documentación completa
└── mcp-config.json               # ✅ Configuración MCP
```

**Herramientas MCP Disponibles:**
1. `search_rag` - Búsqueda en base de conocimiento SS
2. `verify_boe` - Verificación de vigencia en BOE oficial
3. `search_jurisprudence` - Búsqueda de sentencias
4. `generate_flashcards` - Generación de tarjetas de estudio
5. `get_law_summary` - Resumen estructurado de leyes

**Estado:** ✅ Power documentado, ⚠️ MCP server en `mcp-server/` (TypeScript)

### MCP Server

**Ubicación:** `mcp-server/` (TypeScript + Node.js)

```
mcp-server/
├── src/                          # Código fuente TypeScript
├── dist/                         # Compilado JavaScript
├── .env                          # Configuración
└── package.json                  # Dependencias Node.js
```

**Configuración requerida:**
- `QDRANT_URL`: http://localhost:6333
- `QDRANT_API_KEY`: API key de Qdrant
- `QDRANT_COLLECTION`: leyes_seguridad_social
- `GEMINI_API_KEY`: API key de Gemini (opcional)

**Estado:** ✅ Implementado, ⚠️ Requiere compilación (`npm run build`)

---

## 🐳 INFRAESTRUCTURA

### Docker Compose (`docker-compose.yml`)

```yaml
services:
  qdrant:
    image: qdrant/qdrant:v1.12.0
    ports: ["6333:6333", "6334:6334"]
    volumes: ["./qdrant_storage:/qdrant/storage"]
    
  postgres:
    image: postgres:15
    ports: ["5432:5432"]
    environment:
      POSTGRES_DB: opositaia
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
```

**Estado Docker Actual:**
```
Container: opositaia-qdrant
Image: qdrant/qdrant:v1.12.0
Status: ⚠️ EXITED (255) - Detenido hace 10 minutos
Ports: 0.0.0.0:6333-6334->6333-6334/tcp
Container ID: 74195ca77445
```

**Observación:** El contenedor Qdrant está detenido. Para reiniciarlo:
```bash
docker start opositaia-qdrant
# o
docker-compose up -d qdrant
```

**Estado:** ⚠️ Configurado pero contenedor detenido

### VPS Externo

```
URL: https://electroyhogarpelotazo.tienda
Servicios:
  - Salamandra 7B (llama.cpp) en puerto 8080
  - Nginx reverse proxy
  - Qdrant Cloud (alternativa)
```

---

## 📊 MÉTRICAS ACTUALES

### Código

```
Backend:
  - Routers: 8 activos
  - Agentes: 2 implementados (RAG V2, LLM Providers)
  - Scripts: 50+ (mantenimiento/tests)
  - Tests: Parciales

Frontend:
  - Componentes: 20+
  - Servicios: 2 (backendService, geminiService legacy)
  - Hooks: Custom hooks implementados

Documentación:
  - Archivos .md: 100+ (dispersos)
  - Docs organizados: ~10%
```

### Datos

```
Qdrant:
  - Documentos: ~48,866 chunks
  - Tamaño: ~320 MB
  - Capas: 2 (normativa + materiales)

Datasets:
  - Casos generados: ~12,000+
  - Golden dataset: Validado
  - Datasets limpios: 5
```

---

## 📂 MATERIALES CONCEPTUALES

### Ubicación: `conceptual_materials/` (39 items)

```
conceptual_materials/
├── pdfs/                         # 18 PDFs de estudio
│   ├── 01_esquemaAAPPEE.pdf
│   ├── 02_CE_T_VIII.pdf
│   ├── 03_Instituciones_UE.pdf
│   ├── 11_PAC_Plazos.pdf
│   ├── 19_Ficha_SS.pdf
│   └── ...
├── extracted_texts/              # 18 textos extraídos
│   ├── 01_esquemaAAPPEE.txt
│   ├── 02_CE_T_VIII.txt
│   └── ...
└── qa_generated/                 # 11 archivos QA generados
    ├── conceptual_qa_100.jsonl
    ├── conceptual_qa_FINAL.jsonl
    ├── conceptual_qa_IMPROVED.jsonl
    └── stats_20251219_013135.json
```

**Contenido:**
- Esquemas de Administraciones Públicas
- Constitución Española (Título VIII)
- Instituciones de la UE
- Procedimiento Administrativo Común (plazos)
- Ley de Contratos del Sector Público
- Fichas de Seguridad Social
- Comparativas de leyes

**Estado:** ✅ PDFs extraídos, ✅ QA generado, ⚠️ No indexado en Qdrant

---

## 🏛️ DATOS LEGALES

### BOE XML/JSON (`data/boe_xml/`) - 55 archivos

**Contenido:**
- XMLs originales del BOE
- JSONs con análisis completo de cada ley
- Metadata: vigencia, modificaciones, derogaciones
- Referencias: anteriores y posteriores
- URLs: BOE, ELI, PDF, XML, HTML

**Estructura JSON:**
```json
{
  "boe_id": "BOE-A-2015-11724",
  "titulo": "Real Decreto Legislativo 8/2015, TRLGSS",
  "vigente": true,
  "analisis": {
    "materias": ["Seguridad Social", "Pensiones"],
    "referencias": {
      "anteriores": [{"id_norma": "...", "relacion": "DEROGA"}],
      "posteriores": [{"id_norma": "...", "relacion": "MODIFICA"}]
    }
  },
  "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
}
```

**Estado:** ✅ 55 leyes analizadas, ⚠️ Metadata no integrada en Qdrant (pendiente FASE 0)

---

## 🎓 MATERIALES DE ACADEMIAS

### Ubicación: `academias/` (331 items)

```
academias/
├── temario_oficial/              # Temarios oficiales
├── Opos de Radi todo/            # Material de academia
├── de la academia de radi/       # Más material
├── extract_academias_pdfs.py     # Extractor de PDFs
├── extract_pdfs_ocr_mistral.py   # OCR con Mistral
├── test_mistral_ocr.py           # Tests OCR
├── ocr_execution.log             # Log de ejecución
└── pdfs_fallidos.txt             # PDFs que fallaron
```

**Contenido:**
- Exámenes oficiales anteriores
- Temarios de academias
- Tests y simulacros
- Material de estudio

**Estado:** ✅ Material recopilado, ⚠️ OCR parcial, ⚠️ No completamente indexado

---

## ⚠️ GAPS Y ÁREAS DE MEJORA

### 1. Sistema de Agentes
- ❌ **NO implementado** (solo diseño en `opos-agents/`)
- ❌ Orquestador principal ausente
- ❌ Agentes especializados no existen
- ✅ Plan de 6 fases definido (21-23h estimadas)
- ✅ DeepSeek V3 + MCP probado exitosamente

### 2. Integración de Datasets
- ⚠️ 12k+ casos generados pero no servidos por API
- ⚠️ No hay endpoint para acceder a casos prácticos pre-generados
- ⚠️ COSM (Create Once, Serve Many) no implementado
- ❌ Faltan 250 items según DATASET_GAPS_REPORT.md
- ✅ Golden dataset validado (1,381 items)

### 3. Legal Judge
- ❌ **NO implementado** (solo diseño en planes)
- ❌ Validación jurídica ausente
- ❌ Calculadoras deterministas no existen
- ✅ Diseño completo en FASE 3 del plan RAG
- ✅ Integración BOE API diseñada

### 4. Calculadoras SS
- ❌ **NO implementadas**
- ❌ Motor de reglas YAML no existe
- ❌ Cálculos de IT, pensiones, etc. no automatizados
- ⚠️ Mencionadas en planes pero sin implementación

### 5. RAG Agentic
- ❌ Query Expansion no implementado
- ❌ Relevance Filter no implementado
- ❌ BGE Reranker no descargado (350MB)
- ❌ Hybrid Search no implementado
- ⚠️ Metadata enriquecida pendiente (FASE 0)
- ✅ RAG V2 básico funcional

### 6. Frontend-Backend Sync
- ⚠️ PostgreSQL schema definido pero poco usado
- ⚠️ Tracking de progreso no completamente integrado
- ⚠️ Dashboard de estadísticas parcial
- ✅ 9 funciones IA implementadas en `/ai/*`

### 7. Organización del Código
- ⚠️ Raíz saturada (257 archivos, 100+ .md)
- ⚠️ Scripts experimentales mezclados con producción
- ⚠️ Documentación dispersa (279 items en docs/, 100+ en raíz)
- ⚠️ 4 virtual envs (.venv, .venv_cpu, .venv_conversion, .venv_kaggle)

### 8. Materiales No Indexados
- ⚠️ Conceptual materials (18 PDFs) no en Qdrant
- ⚠️ Academias (331 items) parcialmente procesados
- ⚠️ Extracted texts (99 archivos) no indexados
- ⚠️ Staging area (9 items) sin procesar

---

## ✅ FORTALEZAS ACTUALES

1. **Backend Sólido**
   - FastAPI bien estructurado
   - Multi-proveedor LLM funcional
   - RAG V2 con reranking implementado

2. **Frontend Completo**
   - 20+ componentes funcionales
   - Todas las features principales implementadas
   - UX coherente

3. **Datos de Calidad**
   - Embeddings especializados en legislación española
   - Datasets validados
   - Qdrant optimizado

4. **Infraestructura Flexible**
   - Docker para desarrollo
   - VPS para producción
   - Multi-cloud (Groq, Gemini, DeepSeek)

---

## 🎯 PRÓXIMOS PASOS RECOMENDADOS

### Prioridad Alta
1. **Implementar Sistema de Agentes** (opos-agents/)
2. **Integrar Datasets** (API endpoints + COSM)
3. **Legal Judge** (validación jurídica)
4. **Calculadoras SS** (IT, pensiones)

### Prioridad Media
5. **Consolidar Documentación** (mover .md a docs/)
6. **Limpiar Raíz** (archivar scripts experimentales)
7. **Tests Completos** (coverage >80%)

### Prioridad Baja
8. **Optimizaciones** (cache, performance)
9. **Monitoreo** (Prometheus, Grafana)
10. **CI/CD** (GitHub Actions)

---

## 📝 CONCLUSIONES

**Estado General:** 🟢 **FUNCIONAL PERO INCOMPLETO**

### Lo que FUNCIONA ✅

El proyecto tiene una base técnica sólida y operativa:

**Backend:**
- ✅ FastAPI robusto con 8 routers activos
- ✅ RAG V2 con embeddings especializados (bge-m3-spa-law-qa)
- ✅ Multi-proveedor LLM (Groq, Gemini, DeepSeek, Mistral)
- ✅ 9 funciones IA implementadas (casos, exámenes, mapas, flashcards)
- ✅ PostgreSQL + Qdrant operativos (48,866 chunks, 320MB)

**Frontend:**
- ✅ React completo con 20+ componentes
- ✅ Todas las features principales implementadas
- ✅ UX coherente y funcional
- ✅ Integración con backend via backendService.ts

**Datos:**
- ✅ 12k+ casos generados y validados
- ✅ 55 leyes del BOE analizadas (XMLs + JSONs)
- ✅ Embeddings especializados en legislación española
- ✅ Qdrant optimizado con vectores híbridos (Dense + Sparse)

**Infraestructura:**
- ✅ Docker para desarrollo (Qdrant + PostgreSQL)
- ✅ VPS Hostinger con Salamandra 7B (147.93.95.67)
- ✅ Dominio SSL activo (electroyhogarpelotazo.tienda)
- ✅ Multi-cloud (Groq, Gemini, DeepSeek)

### Lo que FALTA ❌

Componentes críticos diseñados pero no implementados:

**Sistema de Agentes:**
- ❌ Orquestador principal
- ❌ Query Expansion (Salamandra)
- ❌ Relevance Filter (Salamandra)
- ❌ BGE Reranker (350MB)
- ❌ Hybrid Search avanzado
- ✅ Plan completo de 6 fases (21-23h)

**Legal Judge:**
- ❌ Validación jurídica automática
- ❌ Verificación de vigencia
- ❌ Calculadoras deterministas SS
- ✅ Diseño completo con DeepSeek Reasoner

**Integración de Datos:**
- ❌ API endpoints para datasets pre-generados
- ❌ COSM (Create Once, Serve Many)
- ❌ 250 items faltantes (gaps report)
- ❌ Materiales conceptuales no indexados

**Organización:**
- ⚠️ 257 archivos en raíz (100+ .md)
- ⚠️ 279 items en docs/ + 100+ en raíz
- ⚠️ Scripts experimentales sin archivar
- ⚠️ 4 virtual envs diferentes

### Análisis de Capacidades

**Capacidad Actual (Funcional):**
```
✅ Chat con IA + RAG básico
✅ Generación de casos prácticos
✅ Simulacros de examen (hasta 100 preguntas)
✅ Mapas mentales
✅ Flashcards (con export Anki)
✅ Esquemas y resúmenes
✅ Comparador de textos
✅ Planes de estudio
✅ Búsqueda con grounding
```

**Capacidad Diseñada (No Implementada):**
```
❌ RAG agentic con reranking avanzado
❌ Validación jurídica automática (Legal Judge)
❌ Calculadoras deterministas SS
❌ Sistema multi-agente orquestado
❌ COSM para datasets
❌ Verificación BOE en tiempo real
```

### Métricas del Sistema

**Código:**
- Backend: 8 routers, 2 agentes, 52+ scripts
- Frontend: 20+ componentes, 2 servicios
- Tests: Parciales (scripts/tests/ con 28 tests)
- Documentación: 379+ archivos .md (dispersos)

**Datos:**
- Qdrant: 48,866 chunks (320 MB)
- PostgreSQL: 54 leyes (50 columnas metadata)
- Datasets: 12k+ casos generados
- Golden dataset: 1,381 items validados
- Gaps: 250 items faltantes

**Infraestructura:**
- Local: Docker (Qdrant + PostgreSQL)
- VPS: Salamandra 7B (4.85 GB GGUF)
- APIs: 5 proveedores activos
- MCP: Server TypeScript implementado

### Roadmap Inmediato

**Prioridad CRÍTICA (Bloqueante):**
1. **FASE 0: Re-ingestión Qdrant** (4-6h)
   - Integrar metadata de análisis BOE
   - Crear colección master con 54 leyes
   - Enriquecer payloads con vigencia/modificaciones

**Prioridad ALTA (Funcionalidad Core):**
2. **FASE 1-5: Agentic RAG** (17-19h)
   - Implementar componentes RAG avanzados
   - Legal Judge con DeepSeek Reasoner
   - Pipeline integrado en FastAPI
   
3. **Integrar Datasets** (8-12h)
   - API endpoints para casos pre-generados
   - COSM implementation
   - Completar 250 items faltantes

**Prioridad MEDIA (Mejoras):**
4. **Consolidar Documentación** (4-6h)
   - Mover 100+ .md de raíz a docs/
   - Organizar por categorías
   - Archivar scripts experimentales

5. **Tests Completos** (8-10h)
   - Coverage >80%
   - Tests E2E
   - Benchmarks de rendimiento

**Prioridad BAJA (Optimización):**
6. **Optimizaciones** (variable)
   - Cache de queries
   - Performance tuning
   - Monitoreo (Prometheus/Grafana)

### Estimación de Esfuerzo Total

```
FASE 0 (Bloqueante):        4-6h   🔴 CRÍTICO
FASE 1-5 (Agentic RAG):    17-19h  🔴 ALTA
Integración Datasets:       8-12h  🔴 ALTA
Consolidación Docs:         4-6h   🟡 MEDIA
Tests Completos:            8-10h  🟡 MEDIA
Optimizaciones:            Variable 🟢 BAJA
─────────────────────────────────────────
TOTAL MÍNIMO VIABLE:       41-49h  (~1 semana)
TOTAL COMPLETO:            60-80h  (~2 semanas)
```

### Recomendación Final

**Estrategia Sugerida:**

1. **Semana 1: Core Functionality**
   - Completar FASE 0-5 del plan Agentic RAG
   - Implementar Legal Judge
   - Integrar datasets existentes

2. **Semana 2: Polish & Testing**
   - Completar gaps de datasets (250 items)
   - Tests completos
   - Consolidar documentación
   - Preparar para usuarios beta

3. **Post-Launch: Optimization**
   - Monitoreo y métricas
   - Fine-tuning Salamandra
   - Calculadoras SS
   - Features adicionales

**Conclusión:** El proyecto está en un estado avanzado con infraestructura sólida y funcionalidad básica operativa. Con 1-2 semanas de trabajo enfocado en los componentes críticos faltantes (Agentic RAG + Legal Judge + Integración Datasets), el sistema estará listo para usuarios beta.

---

**Documento generado por:** Kiro AI  
**Fecha:** 20 de Enero de 2026  
**Versión:** 2.0 - Análisis Exhaustivo Enriquecido  
**Fuentes:** Workspace completo + docs/16_01_26_AGENTIC_RAG_PLAN.md + docs/16_01_26_INVENTARIO_SISTEMA.md + opos-agents/12_01_26_deepseek_v3_mcp_informe.md
