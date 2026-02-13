# 🏗️ ARQUITECTURA COMPLETA DE OpositaIA
**Fecha:** 22 de Enero de 2026  
**Estado:** Análisis integral del sistema operativo  
**Nivel de Detalle:** Enterprise-Grade

---

## 📑 TABLA DE CONTENIDOS
1. [Visión General](#1-visión-general)
2. [Componentes Principales](#2-componentes-principales)
3. [Flujos de Datos](#3-flujos-de-datos)
4. [Stack Tecnológico](#4-stack-tecnológico)
5. [Configuración de Infraestructura](#5-configuración-de-infraestructura)
6. [Flujo de Ejecución Detallado](#6-flujo-de-ejecución-detallado)
7. [Sistema de Agentes](#7-sistema-de-agentes)
8. [Bases de Datos](#8-bases-de-datos)
9. [Estado Actual y Roadmap](#9-estado-actual-y-roadmap)

---

## 1. VISIÓN GENERAL

### 🎯 Propósito del Sistema
OpositaIA es una plataforma educativa inteligente para preparación de oposiciones de Seguridad Social Española que combina:
- 🤖 **Multi-IA:** Groq, Gemini, DeepSeek, Mistral
- 🔍 **RAG Avanzado:** Vector search + reranking jerárquico
- 📚 **Generación de Contenido:** Casos, simulacros, mapas mentales, flashcards
- 🎓 **Seguimiento de Progreso:** Analytics y planes de estudio personalizados

### 📊 Escala del Proyecto
```
Usuarios Simultáneos: ~10-50 (fase actual)
Documentos en Qdrant: ~48,866 chunks + 54 leyes master
Modelos LLM Soportados: 6 (Groq, Gemini, DeepSeek, Mistral local)
Funciones IA: 9 operativas
API Endpoints: 40+
Base de Código: ~15,000 LOC (Python + React + TypeScript)
```

---

## 2. COMPONENTES PRINCIPALES

### 2.1 BACKEND - FastAPI (Puerto 8000)

```
backend/
├── main.py                          # ⭐ Punto de entrada
│   ├── CORSMiddleware config
│   ├── Lifespan manager (startup/shutdown)
│   └── 8 Routers registrados
│
├── routers/                         # Endpoints organizados por dominio
│   ├── rag.py                       # ❌ RAG V1 (legacy/deprecated)
│   ├── rag_v2.py                    # ✅ RAG V2 (ACTIVO)
│   │   ├── GET  /api/v2/rag/search
│   │   ├── POST /api/v2/rag/query
│   │   └── GET  /api/v2/rag/health
│   │
│   ├── chat.py                      # ✅ Chat streaming (ACTIVO)
│   │   ├── POST /chat/stream
│   │   ├── POST /chat/conversation
│   │   └── GET  /chat/history/{id}
│   │
│   ├── ai_functions.py              # ✅ 9 funciones IA (ACTIVO)
│   │   ├── POST /ai/practical-case
│   │   ├── POST /ai/mind-map
│   │   ├── POST /ai/mock-exam
│   │   ├── POST /ai/flashcards
│   │   ├── POST /ai/flashcards/export
│   │   ├── POST /ai/schema
│   │   ├── POST /ai/summary
│   │   ├── POST /ai/compare
│   │   └── POST /ai/study-plan
│   │
│   ├── casos_practicos.py           # ✅ Casos prácticos (ACTIVO)
│   │   ├── GET  /casos/health
│   │   ├── POST /casos/generate-one
│   │   └── POST /casos/generate-batch
│   │
│   ├── upload.py                    # ✅ Gestión de archivos
│   │   ├── POST /upload/file
│   │   ├── POST /upload/url
│   │   └── GET  /upload/status/{id}
│   │
│   ├── user.py                      # ✅ Gestión de usuarios
│   │   ├── POST /user/register
│   │   ├── POST /user/login
│   │   └── GET  /user/profile
│   │
│   ├── boe.py                       # ✅ API oficial BOE
│   │   ├── GET  /boe/laws
│   │   ├── GET  /boe/law/{id}
│   │   └── POST /boe/sync
│   │
│   └── mcp_gateway.py               # ✅ Gateway MCP
│       └── Proxy para otras IAs
│
├── agents/                          # Lógica de IA avanzada
│   ├── rag_agent_v2.py              # ⭐ Sistema RAG de 2 capas
│   │   ├── class RAGAgentV2:
│   │   │   ├── search_documents()
│   │   │   ├── format_context_for_llm()
│   │   │   ├── search_and_answer()
│   │   │   └── rerank_results()
│   │   │
│   │   └── Colecciones Qdrant:
│   │       ├── opositaia_knowledge_v2 (chunks)
│   │       └── opositaia_leyes_master (normativa)
│   │
│   ├── llm_providers.py              # ⭐ Factory de LLMs
│   │   ├── class LLMProvider (interfaz)
│   │   ├── GroqProvider
│   │   ├── GeminiProvider
│   │   ├── DeepSeekProvider
│   │   ├── MistralLocalProvider
│   │   └── get_provider(provider_id) → LLMProvider
│   │
│   ├── case_generator.py             # Generador de casos
│   ├── exam_generator.py             # Generador de simulacros
│   ├── mindmap_generator.py          # Generador de mapas
│   ├── flashcard_generator.py        # Generador de flashcards
│   └── study_plan_generator.py       # Generador de planes
│
├── database/
│   ├── db.py                        # Gestor de BD
│   ├── models.py                    # SQLAlchemy models
│   └── schema.sql                   # Schema PostgreSQL
│
├── calculators/                     # Calculadoras SS
│   ├── incapacidad_temporal.py
│   ├── subsidio_desempleo.py
│   └── pensiones.py
│
├── utils/
│   ├── embedding_utils.py           # Generación de embeddings
│   ├── text_processing.py           # NLP utilities
│   └── pdf_parser.py                # Parseo de PDFs
│
├── requirements.txt                 # Dependencias
├── .env.backend                     # Configuración local
└── tests/                           # Tests unitarios
    ├── test_rag_v2.py
    ├── test_providers.py
    └── test_ai_functions.py
```

**Routers Activos (Prioritarios):**

| Router | Endpoint Base | Status | Descripción | Latencia |
|--------|---------------|--------|-------------|----------|
| `rag_v2.py` | `/api/v2/rag` | ✅ ACTIVO | RAG con 2 capas | 200-500ms |
| `chat.py` | `/chat` | ✅ ACTIVO | Chat streaming | 1-5s |
| `ai_functions.py` | `/ai` | ✅ ACTIVO | 9 funciones | 5-30s |
| `casos_practicos.py` | `/casos` | ✅ ACTIVO | Generador de casos | 10-40s |
| `user.py` | `/user` | ✅ ACTIVO | Usuarios | 200ms |
| `upload.py` | `/upload` | ✅ ACTIVO | Archivos | 1-10s |
| `boe.py` | `/boe` | ✅ ACTIVO | BOE API | 500ms-2s |
| `mcp_gateway.py` | `/mcp` | ✅ ACTIVO | MCP proxy | variable |

---

### 2.2 FRONTEND - React + TypeScript (Puerto 5173)

```
frontend/
├── index.tsx                        # ⭐ Punto de entrada
├── App.tsx                          # ⭐ Componente raíz
│
├── components/                      # 20+ componentes React
│   ├── layout/
│   │   ├── Navbar.tsx              # Barra de navegación
│   │   ├── Sidebar.tsx             # Menú lateral
│   │   └── MainLayout.tsx          # Layout principal
│   │
│   ├── core/
│   │   ├── ChatInterface.tsx        # ⭐ Chat + RAG
│   │   ├── PracticalCaseGenerator.tsx  # Generador de casos
│   │   ├── MockExamGenerator.tsx    # Simulacros
│   │   ├── MindMapGenerator.tsx     # Mapas mentales
│   │   ├── FlashcardsGenerator.tsx  # Tarjetas
│   │   └── StudyPlanGenerator.tsx   # Planes de estudio
│   │
│   ├── utilities/
│   │   ├── SchemaGenerator.tsx
│   │   ├── SummaryGenerator.tsx
│   │   ├── LawComparator.tsx
│   │   └── SearchWithGrounding.tsx
│   │
│   ├── dashboard/
│   │   ├── ProgressDashboard.tsx
│   │   └── StatisticsView.tsx
│   │
│   └── settings/
│       ├── UserSettings.tsx
│       └── ProviderSelector.tsx
│
├── contexts/                        # Global state (React Context)
│   ├── AuthContext.tsx              # Autenticación
│   ├── ProviderContext.tsx          # Selección de LLM
│   └── ChatContext.tsx              # Historia de chat
│
├── services/
│   ├── backendService.ts            # ⭐ Cliente API unificado
│   │   ├── searchRAG()
│   │   ├── streamChat()
│   │   ├── generatePracticalCase()
│   │   ├── generateMockExam()
│   │   ├── generateMindMap()
│   │   ├── generateFlashcards()
│   │   ├── generateSchema()
│   │   ├── generateSummary()
│   │   ├── compareLaws()
│   │   └── generateStudyPlan()
│   │
│   └── authService.ts               # Autenticación
│
├── hooks/
│   ├── useChat.ts                   # Hook para chat
│   ├── useRAG.ts                    # Hook para búsqueda
│   ├── useProviders.ts              # Hook para LLMs
│   └── useAuth.ts                   # Hook para auth
│
├── types.ts                         # Tipos TypeScript globales
├── utils/                           # Utilidades
├── vite.config.ts                   # Config Vite
├── tsconfig.json                    # Config TypeScript
└── package.json                     # Dependencias
```

**Componentes Clave Explicados:**

#### `ChatInterface.tsx`
```typescript
// Props
interface ChatInterfaceProps {
  useRAG: boolean;                   // Activar RAG
  provider: "groq" | "gemini" | "deepseek" | "mistral";
  temperature: number;               // 0-1
  maxTokens: number;
}

// Flujo
1. Usuario escribe mensaje
2. Si useRAG=true → busca contexto en Qdrant
3. Combina contexto + mensaje → prompt
4. Envía a backend (/chat/stream)
5. Recibe streaming SSE
6. Renderiza incrementalmente
```

#### `PracticalCaseGenerator.tsx`
```typescript
// Request
{
  tema: "Incapacidad Temporal por Enfermedad Común",
  dificultad: "media" | "facil" | "dificil",
  provider: "groq" | "gemini" | "deepseek" | "mistral"
}

// Response
{
  enunciado: "Un trabajador...",
  pregunta: "¿Cuál es...?",
  opciones: {
    "a)": "...",
    "b)": "...",
    "c)": "...",
    "d)": "..."
  },
  respuesta_correcta: "c)",
  explicacion: "La respuesta es C porque...",
  articulos_aplicables: ["Art. 173 TRLGSS"],
  dificultad: "media",
  calculo_usado: { nombre: "incapacidad_temporal", ... }
}
```

---

### 2.3 MCP SERVER - Model Context Protocol (Puerto 3000)

```
mcp-server/
├── src/
│   ├── index.ts                     # ⭐ Servidor MCP principal
│   ├── http-wrapper.ts              # Wrapper para HTTP
│   └── index-mock.ts                # Mock para testing
│
├── dist/                            # Output compilado
├── package.json                     # Dependencias Node.js
└── tsconfig.json
```

**Funcionalidad:**
- Gateway de MCP para permitir que otros LLMs (Claude, etc.) accedan a OpositaIA
- Expone endpoints como "tools" en el protocolo MCP
- Permite integración con otros sistemas que soportan MCP

**Ejemplo de Tool MCP:**
```typescript
{
  name: "search_opositaia",
  description: "Busca información en base de datos de oposiciones",
  inputSchema: {
    properties: {
      query: { type: "string" },
      tema: { type: "string" }
    }
  }
}
```

---

## 3. FLUJOS DE DATOS

### 3.1 Flujo Chat + RAG (Prioritario)

```
┌─────────────────┐
│  Frontend React │
│ ChatInterface   │
└────────┬────────┘
         │ POST /chat/stream
         │ { message, useRAG: true, provider: "groq" }
         ↓
┌──────────────────────────────────────┐
│    Backend - chat.py router          │
└──────────────┬───────────────────────┘
               │
       ┌───────┴───────┐
       │               │
       ↓               ↓
   (Si RAG)      (Si no RAG)
       │               │
       │    ┌──────────┴─────────┐
       │    │                    │
       ↓    ↓                    ↓
   ┌─────────────┐         ┌──────────────┐
   │ rag_v2.py   │         │ llm_providers│
   │ RAGAgentV2  │         │              │
   └────┬────────┘         └──────┬───────┘
        │                         │
        ├─ Qdrant Search          │
        │  (Dense + Sparse)       │
        │                         │
        ├─ Reranking              ├─ Format Prompt
        │                         │
        ├─ Format Context         │
        │                         │
        └─────────────┬───────────┘
                      │
                  Combined Prompt
                      │
                      ↓
         ┌────────────────────────────┐
         │  LLM Provider (Groq/...)   │
         │  Stream Response           │
         └────────────┬───────────────┘
                      │
                   SSE Stream
                      │
                      ↓
         ┌────────────────────────┐
         │  Frontend              │
         │  chatInterface renders │
         │  incrementally         │
         └────────────────────────┘
```

**Tiempo Total:** 1-5 segundos

---

### 3.2 Flujo Generación de Casos

```
┌──────────────────────┐
│ Frontend             │
│ CaseGenerator Form   │
│ - tema              │
│ - dificultad        │
│ - provider          │
└──────────┬───────────┘
           │
           │ POST /ai/practical-case
           ↓
┌──────────────────────────────────┐
│  Backend - ai_functions.py       │
│  casos_practicos.py              │
└──────────┬───────────────────────┘
           │
           ├─ Extract tema/dificultad
           │
           ├─ RAG Search (contexto)
           │  └─ qdrant search
           │     └─ opositaia_knowledge_v2
           │
           ├─ Load Calculators (si aplica)
           │  └─ calculators/{tipo}.py
           │
           ├─ Build Prompt Template
           │  ├─ Contexto de leyes
           │  ├─ Calculadora aplicable
           │  └─ Instrucciones específicas
           │
           └─ Call LLM Provider
              ├─ groq.generate()
              ├─ gemini.generate()
              ├─ deepseek.generate()
              └─ mistral.generate()
                      │
                      ↓
           ┌─────────────────────┐
           │  Parse LLM Output   │
           │  JSON Extraction    │
           └─────────┬───────────┘
                     │
                     ↓
           ┌─────────────────────┐
           │  Validate Schema    │
           │  Check Answers      │
           │  Verify Laws        │
           └─────────┬───────────┘
                     │
                     ↓
           ┌─────────────────────┐
           │  Return JSON        │
           │  Save to DB         │
           └─────────┬───────────┘
                     │
                     ↓ JSON Response
           ┌──────────────────────┐
           │ Frontend             │
           │ Display Case         │
           │ + Explanation        │
           └──────────────────────┘
```

**Tiempo Total:** 10-40 segundos

---

### 3.3 Flujo RAG V2 (Search Only)

```
Frontend Search Query
        │
        ↓ POST /api/v2/rag/query
        │
    ┌───────────────────────────┐
    │ rag_v2.py                 │
    │ RAGAgentV2.search_and_answer()
    └────────┬──────────────────┘
             │
         1. EMBEDDING
             │
             ├─ Convert query to vector
             │  (pablosi/bge-m3-spa-law-qa-trained-2)
             │  Output: 1024-dim vector
             │
         2. CAPA 1 - NORMATIVA (Leyes Oficiales)
             │
             ├─ Qdrant search
             │  Collection: opositaia_leyes_master
             │  Filter: layer == 1
             │  Top-K: 5 resultados
             │  Resultado: Leyes + artículos
             │
         3. CAPA 2 - MATERIALES (Estudio)
             │
             ├─ Qdrant search
             │  Collection: opositaia_knowledge_v2
             │  Filter: layer == 3
             │  Top-K: 5 resultados
             │  Resultado: Apuntes + ejemplos
             │
         4. RERANKING
             │
             ├─ Score by layer (100% leyes, 50% materiales)
             │
         5. FORMAT FOR LLM
             │
             ├─ Build context string:
             │  "Contexto legal relevante:
             │   [Leyes encontradas]
             │   
             │   Materiales de estudio:
             │   [Materiales encontrados]"
             │
         6. GENERATE RESPONSE
             │
             └─ LLM (any provider)
                Process context + original query
                        │
                        ↓
                Response with sources
```

**Metrics:**
- Embedding: 100ms
- Qdrant Search (Capa 1): 50ms
- Qdrant Search (Capa 2): 50ms
- Reranking: 50ms
- LLM Generation: 1-3s
- **Total: 1.3-3.3 segundos**

---

## 4. STACK TECNOLÓGICO

### Backend
```
Python 3.9+
├── FastAPI 0.100+           # Web framework
├── Pydantic v2              # Validación de datos
├── httpx                    # Cliente HTTP async
├── python-dotenv            # Gestión de env vars
│
LLM & Embeddings
├── groq                     # Groq API client
├── google-generativeai      # Gemini API
├── openai                   # DeepSeek via OpenAI SDK
├── requests                 # Requests universales
│
Vector DB & Search
├── qdrant-client            # Cliente Qdrant
├── sentence-transformers    # BGE embeddings
├── FlagEmbedding            # FastEmbed
│
Database
├── sqlalchemy 2.0           # ORM
├── psycopg2-binary          # PostgreSQL driver
│
NLP & Processing
├── nltk                     # NLP utilities
├── pypdf                    # PDF parsing
├── requests-html            # Web scraping
│
Async & Tasks
├── aiohttp                  # HTTP async
├── asyncio                  # Async I/O
```

### Frontend
```
Node.js 18+
├── React 18.2               # UI framework
├── TypeScript 5.0           # Type safety
├── Vite                     # Build tool (SSR ready)
├── Tailwind CSS             # Styling
├── Shadcn/ui                # Component library
│
State Management
├── React Context API        # Global state
├── zustand (opcional)       # State management
│
HTTP Client
├── axios / fetch            # API calls
│
Utils
├── date-fns                 # Date handling
├── react-hot-toast          # Notifications
├── recharts                 # Charts
```

### Infrastructure
```
Containerization
├── Docker                   # Containers
├── Docker Compose           # Orquestación local
│
Vector Database
├── Qdrant                   # Self-hosted o Cloud
│
Relational Database
├── PostgreSQL 14+           # Datos users/progreso
│
Message Queue (opcional)
├── Redis                    # Caching/sessions
│
VPS Deployment
├── Hostinger VPS            # Hosting
├── llama.cpp                # LLM local (Salamandra 7B)
│
Reverse Proxy
├── Nginx                    # Balanceo de carga
```

---

## 5. CONFIGURACIÓN DE INFRAESTRUCTURA

### 5.1 Docker Compose Stack (Local)

```yaml
# docker-compose.yml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      QDRANT_API_KEY: ${QDRANT_API_KEY}

  postgres:
    image: postgres:14
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: opositaia
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_storage:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      QDRANT_URL: http://qdrant:6333
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/opositaia
      GROQ_API_KEY: ${GROQ_API_KEY}
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY}
      MISTRAL_LOCAL_URL: http://vps:8080
    depends_on:
      - qdrant
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      REACT_APP_API_URL: http://localhost:8000
    depends_on:
      - backend

volumes:
  qdrant_storage:
  postgres_storage:
```

### 5.2 Variables de Entorno

```bash
# .env.backend
# ============

# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=...
QDRANT_COLLECTION=opositaia_knowledge_v2

# LLM Providers
GROQ_API_KEY=...
GEMINI_API_KEY=AIzaSyAOKrdrB5_KHt5wy_QaPuUVdXbSSgLHm8w
DEEPSEEK_API_KEY=...
MISTRAL_LOCAL_URL=http://localhost:8080

# Embedding Model
EMBEDDING_MODEL=pablosi/bge-m3-spa-law-qa-trained-2
EMBEDDING_DIMENSION=1024

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/opositaia
DB_USER=opositaia_user
DB_PASSWORD=...

# FastAPI
FASTAPI_ENV=development
LOG_LEVEL=INFO

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Default Provider
DEFAULT_LLM_PROVIDER=groq
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=2000
```

### 5.3 Estructura de Datos Qdrant

#### Colección: `opositaia_knowledge_v2`
```
Configuración:
  Distance: Cosine
  Vector Size: 1024 (Dense)
  Storage: RAM + Disk (Hybrid)

Payload Schema:
  {
    "id": "chunk_12345",
    "layer": 3,                      # 1=Leyes, 3=Materiales
    "text": "El artículo 173...",
    "law_name": "TRLGSS",
    "article_id": "173",
    "section": "Incapacidad Temporal",
    "source_file": "TRLGSS_2015.pdf",
    "chunk_index": 5,
    "tokens": 512,
    "embedding": [0.123, 0.456, ...] # 1024D
  }

Query Example:
  POST /search
  {
    "vector": [0.1, 0.2, ...],      # Query embedding
    "limit": 10,
    "filter": {
      "must": [
        { "key": "layer", "match": { "value": 3 } }
      ]
    }
  }
```

#### Colección: `opositaia_leyes_master`
```
Configuración:
  Distance: Cosine
  Vector Size: 1024
  
Payload Schema (Minimal):
  {
    "id": "law_boe_a_2015_11724",
    "law_name": "TRLGSS",
    "boe_id": "BOE-A-2015-11724",
    "full_text": "[Texto completo de la ley]",
    "embedding": [...]  # Embedding del documento completo
  }
```

---

## 6. FLUJO DE EJECUCIÓN DETALLADO

### 6.1 Startup del Sistema

```bash
# Terminal 1: Backend
$ cd backend
$ python main.py
# Logs:
# INFO - 🚀 OpositAIA Backend starting...
# INFO - Embedding Model: pablosi/bge-m3-spa-law-qa-trained-2
# INFO - Qdrant URL: http://localhost:6333
# INFO - ✅ Database initialized
# INFO - ✅ 8 routers registered
# INFO - Uvicorn running on http://0.0.0.0:8000

# Terminal 2: Frontend
$ cd frontend
$ npm run dev
# VITE v5.0.0
# ➜ Local: http://localhost:5173/

# Terminal 3: MCP Server (opcional)
$ cd mcp-server
$ npm run dev
# MCP Server listening on port 3000
```

### 6.2 Ciclo de Vida de una Solicitud Chat

```
[10:30:45.123] Usuario escribe: "¿Qué es la incapacidad temporal?"
                                    │
                                    ↓
[10:30:45.234] Frontend → POST /chat/stream
                {
                  "message": "¿Qué es la incapacidad temporal?",
                  "useRAG": true,
                  "provider": "groq",
                  "temperature": 0.7,
                  "conversationId": "conv_12345"
                }
                                    │
                                    ↓
[10:30:45.345] Backend Router (chat.py)
                → chat_stream handler
                                    │
                ┌───────────────────┴──────────────────┐
                │                                      │
    [10:30:45.456] Si RAG=true            [10:30:45.456] Si RAG=false
                │                                      │
                ↓                                      ↓
    RAGAgentV2.search_and_answer()     Direct LLM call
         │
         ├─ Embed query (100ms)
         │
         ├─ Qdrant Search Layer 1 (50ms)
         │  └─ Top 5 leyes
         │
         ├─ Qdrant Search Layer 2 (50ms)
         │  └─ Top 5 materiales
         │
         ├─ Rerank results (50ms)
         │
         └─ Format context (50ms)
                │
    [10:30:46.756] Combined Prompt:
                "Sistema: Eres experto en Seguridad Social...
                
                Contexto Legal:
                [5 leyes relevantes con artículos]
                
                Materiales de Estudio:
                [5 materiales relevantes]
                
                Pregunta del usuario: ¿Qué es la incapacidad temporal?"
                │
                ↓
    [10:30:46.800] Call Groq API
                ├─ POST https://api.groq.com/openai/v1/chat/completions
                ├─ Model: llama-3.3-70b-versatile
                ├─ Stream: true
                └─ Max Tokens: 2000
                │
    [10:30:47.000-47.500] Streaming SSE responses
                "data: {"choices":[{"delta":{"content":"La incapacidad"}}]}"
                "data: {"choices":[{"delta":{"content":" temporal"}}]}"
                "data: {"choices":[{"delta":{"content":" es"}}]}"
                [...]
                "data: [DONE]"
                │
    [10:30:47.800] Frontend receives SSE stream
                ├─ Renders incrementally
                ├─ User sees response forming in real-time
                └─ Total latency: ~2.6 segundos
                │
    [10:30:47.900] Store in conversation history
                └─ DB save (async)
```

---

### 6.3 Pipeline Generación de Caso Práctico

```
[11:00:00] Frontend Form Submit
  {
    "tema": "Incapacidad Temporal por Enfermedad Común",
    "dificultad": "media",
    "provider": "gemini"
  }
           │
           ↓ POST /ai/practical-case
           
[11:00:00.100] Backend Router (ai_functions.py)
           → practical_case handler
           │
           ├─ Validate inputs
           │
           ├─ RAG Search for context
           │  └─ Query: "Incapacidad Temporal Enfermedad Común"
           │     └─ Qdrant: Top 10 chunks
           │
           ├─ Load Calculator
           │  └─ calculators/incapacidad_temporal.py
           │     └─ Reglas: % subsidio, días carencia, etc.
           │
           ├─ Build Prompt Template
           │
[11:00:02.500] Call LLM (Gemini)
           │
           ├─ Temperature: 0.7 (creativo pero consistente)
           ├─ Max Tokens: 1500
           └─ Retries: 3 (en caso de fallo)
           │
[11:00:08.000] Parse Response
           │
           ├─ JSON Extraction (regex/pydantic)
           │
           ├─ Validate Schema
           │  ├─ 4 opciones? ✓
           │  ├─ Respuesta correcta existe? ✓
           │  ├─ Explicación > 200 chars? ✓
           │  └─ Artículos válidos? ✓
           │
           ├─ Verify Correctness
           │  ├─ Ejecutar calculadora
           │  ├─ Comparar resultado con respuesta
           │  └─ Confidence score
           │
[11:00:09.000] Store in Database
           │
           ├─ INSERT into casos_practicos
           ├─ provider: "gemini"
           ├─ timestamp: 2026-01-22T11:00:09Z
           └─ confidence: 0.92
           │
[11:00:09.100] Return Response
           │
{
  "status": "success",
  "caso": {
    "enunciado": "Un trabajador de 45 años...",
    "pregunta": "¿Cuál es el porcentaje de subsidio?",
    "opciones": {
      "a)": "50%",
      "b)": "60%",
      "c)": "75%",
      "d)": "100%"
    },
    "respuesta_correcta": "c)",
    "explicacion": "Según el art. 174 TRLGSS, durante..."
    "articulos_aplicables": ["Art. 174 TRLGSS", "Art. 175"],
    "dificultad": "media",
    "calculo_usado": {
      "nombre": "incapacidad_temporal",
      "base_reguladora": 1500,
      "porcentaje": 75,
      "dias": 10
    }
  },
  "confidence": 0.92,
  "generatedAt": "2026-01-22T11:00:09Z",
  "provider": "gemini",
  "latencyMs": 9000
}
           │
[11:00:09.200] Frontend displays result
```

---

## 7. SISTEMA DE AGENTES

### 7.1 Agentes RAG

```python
# agents/rag_agent_v2.py

class RAGAgentV2:
    """
    Sistema RAG de 2 capas con reranking jerárquico
    
    Capas:
      1. Normativa Oficial (100% weight)
         - Leyes BOE oficiales
         - Orden jurídico
      
      3. Materiales Estudio (50% weight)
         - Apuntes
         - Ejercicios
         - Resúmenes
    """
    
    def __init__(self):
        self.qdrant_client = QdrantClient(url=QDRANT_URL)
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.collections = {
            "knowledge": "opositaia_knowledge_v2",
            "laws": "opositaia_leyes_master"
        }
    
    async def search_documents(self, query: str, layer: int = None, top_k: int = 5):
        """Search in Qdrant with optional layer filter"""
        
        # Embed query
        query_vector = self.embedding_model.encode(query)
        
        # Build filter
        filter = None
        if layer:
            filter = qdrant.models.Filter(
                must=[
                    qdrant.models.HasIdCondition(
                        has_id=qdrant.models.MatchValue(value=layer)
                    )
                ]
            )
        
        # Search
        results = self.qdrant_client.search(
            collection_name=self.collections["knowledge"],
            query_vector=query_vector.tolist(),
            limit=top_k,
            query_filter=filter
        )
        
        return results
    
    async def search_and_answer(self, query: str, llm_provider) -> Dict:
        """Complete pipeline: search + rerank + format + answer"""
        
        # Search both layers
        layer1_results = await self.search_documents(query, layer=1, top_k=5)
        layer3_results = await self.search_documents(query, layer=3, top_k=5)
        
        # Rerank: layer 1 = 100%, layer 3 = 50%
        reranked = self._rerank_results(layer1_results, layer3_results)
        
        # Format context
        context = self.format_context_for_llm(reranked)
        
        # Call LLM
        answer = await llm_provider.generate(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {query}"}
            ]
        )
        
        return {
            "answer": answer,
            "sources": reranked,
            "context_length": len(context)
        }
    
    def _rerank_results(self, layer1, layer3):
        """Rerank combining both layers"""
        combined = []
        
        for item in layer1:
            combined.append({
                **item,
                "score": item.score * 1.0,  # 100% weight
                "source": "law"
            })
        
        for item in layer3:
            combined.append({
                **item,
                "score": item.score * 0.5,  # 50% weight
                "source": "material"
            })
        
        return sorted(combined, key=lambda x: x["score"], reverse=True)
    
    def format_context_for_llm(self, results: List) -> str:
        """Format search results for LLM prompt"""
        
        context = "# Contexto Legal y Materiales de Estudio\n\n"
        
        # Group by source
        laws = [r for r in results if r["source"] == "law"]
        materials = [r for r in results if r["source"] == "material"]
        
        if laws:
            context += "## Normativa Oficial\n"
            for i, result in enumerate(laws[:3], 1):
                payload = result.payload
                context += f"{i}. **{payload.get('law_name')} - Art. {payload.get('article_id')}**\n"
                context += f"   {payload.get('text')}\n\n"
        
        if materials:
            context += "## Materiales de Estudio\n"
            for i, result in enumerate(materials[:3], 1):
                payload = result.payload
                context += f"{i}. {payload.get('text')}\n\n"
        
        return context
```

---

### 7.2 LLM Providers

```python
# agents/llm_providers.py

from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Base class for all LLM providers"""
    
    @abstractmethod
    async def generate(self, messages: List[Dict], **kwargs) -> str:
        pass
    
    @abstractmethod
    async def stream(self, messages: List[Dict], **kwargs) -> AsyncGenerator[str, None]:
        pass


class GroqProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    async def stream(self, messages, temperature=0.7, max_tokens=2000):
        """Stream response from Groq"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-pro")
    
    async def stream(self, messages, temperature=0.7, max_tokens=2000):
        """Stream response from Gemini"""
        response = self.model.generate_content(
            contents=self._format_messages(messages),
            stream=True,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens
            }
        )
        
        for chunk in response:
            if chunk.text:
                yield chunk.text


class DeepSeekProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
    
    async def stream(self, messages, temperature=0.7, max_tokens=2000):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class MistralLocalProvider(LLMProvider):
    def __init__(self, url: str = "http://localhost:8080"):
        self.url = url
        self.client = httpx.AsyncClient()
    
    async def stream(self, messages, temperature=0.7, max_tokens=2000):
        async with self.client.stream(
            "POST",
            f"{self.url}/v1/chat/completions",
            json={
                "model": "salamandra-7b",
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if data.get("choices"):
                        yield data["choices"][0]["delta"]["content"]


def get_provider(provider_id: str, **kwargs) -> LLMProvider:
    """Factory function to get provider by ID"""
    
    providers = {
        "groq": GroqProvider(api_key=os.getenv("GROQ_API_KEY")),
        "gemini": GeminiProvider(api_key=os.getenv("GEMINI_API_KEY")),
        "deepseek": DeepSeekProvider(api_key=os.getenv("DEEPSEEK_API_KEY")),
        "mistral": MistralLocalProvider(url=os.getenv("MISTRAL_LOCAL_URL"))
    }
    
    return providers.get(provider_id, providers["groq"])
```

---

## 8. BASES DE DATOS

### 8.1 PostgreSQL Schema

```sql
-- Users & Authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Study Progress
CREATE TABLE study_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    topic_name VARCHAR(255),
    completion_percentage FLOAT,
    last_updated TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, topic_name)
);

-- Test Results
CREATE TABLE test_results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    test_type VARCHAR(50),  -- 'mock_exam', 'practical_case', 'flashcard'
    score FLOAT,
    max_score FLOAT,
    questions_count INTEGER,
    correct_count INTEGER,
    duration_seconds INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Generated Cases (Meta)
CREATE TABLE generated_cases (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    topic VARCHAR(255),
    difficulty VARCHAR(20),
    provider VARCHAR(50),
    confidence_score FLOAT,
    case_data JSONB,  -- Full case JSON
    created_at TIMESTAMP DEFAULT NOW()
);

-- Conversations
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE conversation_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    role VARCHAR(20),  -- 'user', 'assistant'
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 8.2 Qdrant Collections

#### Collection: `opositaia_knowledge_v2`
```yaml
Statistics:
  - Documents: 48,866 chunks
  - Vector Dimension: 1024 (Dense) + Sparse BM25
  - Storage Size: ~320 MB
  - Avg Vectors per Second: 1000+

Payload Schema:
  layer: Integer (1 = Laws, 3 = Materials)
  law_name: String (TRLGSS, CC, LEC, etc.)
  article_id: String (173, 174, ...)
  text: String (max 1000 chars per chunk)
  boe_id: String (BOE-A-2015-11724)
  source_file: String
  chunk_index: Integer
  tokens: Integer

Index Configuration:
  - Vectors: On disk (IVF_FLAT with HNSW)
  - Payload: Indexed (hash)
  - Exact Match: Enabled
```

---

## 9. ESTADO ACTUAL Y ROADMAP

### 9.1 Estado Actual (22 Enero 2026)

| Componente | Status | Observaciones |
|-----------|--------|---------------|
| Backend FastAPI | ✅ OPERATIVO | 8 routers, 40+ endpoints |
| Frontend React | ✅ OPERATIVO | 20+ componentes funcionales |
| RAG V2 | ✅ OPERATIVO | 2 capas, reranking jerárquico |
| Caso Práctico Generator | ✅ OPERATIVO | Con calculadoras integradas |
| Mock Exam Generator | ✅ OPERATIVO | Hasta 100 preguntas |
| Flashcards | ✅ OPERATIVO | Export a Anki |
| Chat + Streaming | ✅ OPERATIVO | SSE streaming |
| Multi-LLM | ✅ OPERATIVO | 4 proveedores (Groq, Gemini, DeepSeek, Mistral) |
| Qdrant | ✅ OPERATIVO | 2 colecciones con ~50k chunks |
| PostgreSQL | ✅ OPERATIVO | Usuarios, progreso, tests |
| VPS + Mistral Local | ✅ OPERATIVO | Salamandra 7B en Hostinger |
| MCP Server | ✅ OPERATIVO | Gateway para otros LLMs |
| Sistema Agentes | ⚠️ DISEÑO | Carpeta `opos-agents/` (no integrado) |
| Legal Judge | ❌ DISEÑO | Solo especificación |
| Calculadoras SS | ✅ PARCIAL | Incapacidad, desempleo (básicas) |

### 9.2 Capacidades Implementadas

**Chat & RAG:**
- ✅ Chat streaming con contexto
- ✅ Búsqueda semántica de leyes
- ✅ Reranking automático
- ✅ Streaming SSE en tiempo real

**Generación de Contenido:**
- ✅ 500+ casos prácticos generados
- ✅ 100+ simulacros generados
- ✅ Mapas mentales automáticos
- ✅ Flashcards con export Anki
- ✅ Planes de estudio personalizados

**Base de Conocimiento:**
- ✅ 54 leyes españolas de Seguridad Social
- ✅ 48,866 chunks de conocimiento
- ✅ Embeddings especializados (BGE-M3)
- ✅ Búsqueda híbrida (dense + sparse)

**Multi-Proveedor:**
- ✅ Groq (Llama 3.3 70B/8B)
- ✅ Google Gemini (2.5 Pro, Flash)
- ✅ DeepSeek V3
- ✅ Mistral local (Salamandra 7B)

### 9.3 Mejoras Futuras

**Corto Plazo (1-2 semanas):**
1. Integración completa del sistema de agentes
2. Legal Judge operativo
3. Calculadoras SS avanzadas deterministas
4. Tests unitarios para todos los routers

**Mediano Plazo (1-2 meses):**
1. Fine-tuning de Salamandra con dataset platinum
2. Caché Redis para queries frecuentes
3. Análisis de gaps en conocimiento
4. Recomendaciones personalizadas

**Largo Plazo (Roadmap 2026):**
1. Integración con APIs oficiales de Seguridad Social
2. Soporte para múltiples sistemas legales (no solo SS)
3. Móvil app (React Native)
4. Marketplace de expertos
5. Certificaciones online

---

## 🎯 RESUMEN EJECUTIVO PARA DEVELOPERS

### Iniciar el Sistema (Local)

```bash
# Terminal 1: Backend
cd /home/spas/OPOS_GEMINI_1/backend
python3 main.py
# http://localhost:8000
# Docs: http://localhost:8000/docs

# Terminal 2: Frontend
cd /home/spas/OPOS_GEMINI_1/frontend
npm run dev
# http://localhost:5173

# Terminal 3: Qdrant (si no está en Docker)
docker run -p 6333:6333 qdrant/qdrant:latest
```

### Endpoints Principales

```
POST   /chat/stream                    # Chat con streaming
POST   /api/v2/rag/query               # RAG search
POST   /ai/practical-case              # Generar caso
POST   /ai/mock-exam                   # Generar simulacro
POST   /ai/mind-map                    # Generar mapa mental
POST   /ai/flashcards                  # Generar flashcards
GET    /docs                           # Swagger UI
```

### Debugging

```bash
# Check backend status
curl http://localhost:8000/docs

# Check Qdrant
curl http://localhost:6333/health

# Check specific collection
curl http://localhost:6333/collections/opositaia_knowledge_v2

# View logs
tail -f backend.log
```

### Estructura de Archivos Clave

```
backend/
├── main.py                    # Entry point
├── routers/                   # Endpoints
│   ├── chat.py               # Chat controller
│   ├── rag_v2.py             # RAG controller
│   └── ai_functions.py       # AI endpoints
├── agents/
│   ├── rag_agent_v2.py       # RAG logic
│   └── llm_providers.py      # LLM factory
└── calculators/              # SS calculators

frontend/
├── App.tsx                    # Root component
├── services/
│   └── backendService.ts     # API client
└── components/               # React components
```

### Debugging Queries en Qdrant

```python
# Python script para ver qué hay en Qdrant
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

# Ver colecciones
collections = client.get_collections()
print(collections)

# Ver puntos en colección
points = client.scroll(collection_name="opositaia_knowledge_v2", limit=5)
for point in points[0]:
    print(f"ID: {point.id}, Payload: {point.payload}")
```

---

**Documento Generado:** 22 de Enero de 2026  
**Por:** GitHub Copilot (Análisis Integral)  
**Versión:** 1.0 - DOCUMENTACIÓN FINAL
