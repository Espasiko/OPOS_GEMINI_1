# 📊 DIAGRAMA DE ARQUITECTURA - OpositaIA

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENTE (USUARIO)                                 │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                 ┌─────────────┴──────────────┐
                 │                            │
         ┌──────▼──────┐            ┌────────▼────────┐
         │  Navigator  │            │  Web Browser    │
         │  (Optional) │            │                 │
         └─────────────┘            └────────┬────────┘
                                             │
                                 ┌───────────▼───────────┐
                                 │  FRONTEND (React)     │
                                 │  :5173                │
                                 │  ┌─────────────────┐  │
                                 │  │  App.tsx        │  │
                                 │  │  Components (20)│  │
                                 │  │  Services       │  │
                                 │  └────────┬────────┘  │
                                 └────────────┼──────────┘
                                              │
                        ┌─────────────────────┼─────────────────────┐
                        │                     │                     │
                        │                     │                     │
                 ┌──────▼──────┐      ┌──────▼──────┐      ┌────────▼───────┐
                 │   REST API   │      │ WebSocket   │      │   SSE Stream    │
                 │   HTTP/1.1   │      │   (Chat)    │      │   (Streaming)   │
                 └──────┬──────┘      └──────┬──────┘      └────────┬────────┘
                        │                     │                     │
        ┌───────────────┴─────────────────────┼─────────────────────┴────────┐
        │                                     │                              │
        │                    ┌────────────────┴─────────────────┐            │
        │                    │                                  │            │
    ┌───▼─────────────────────────────────────────────────────────┴──────────▼───┐
    │                    BACKEND (FastAPI)                                       │
    │                    :8000                                                   │
    │  ┌─────────────────────────────────────────────────────────────────────┐  │
    │  │  main.py - Application Server                                      │  │
    │  │  ├─ CORS Middleware                                                │  │
    │  │  ├─ Lifespan Manager (startup/shutdown)                            │  │
    │  │  └─ 8 Routers Registrados:                                         │  │
    │  │     ├─ chat.py ✅                 → /chat/stream                  │  │
    │  │     ├─ rag_v2.py ✅               → /api/v2/rag/*                │  │
    │  │     ├─ ai_functions.py ✅         → /ai/*  (9 endpoints)         │  │
    │  │     ├─ casos_practicos.py ✅      → /casos/*                     │  │
    │  │     ├─ user.py ✅                 → /user/*                      │  │
    │  │     ├─ upload.py ✅               → /upload/*                    │  │
    │  │     ├─ boe.py ✅                  → /boe/*                       │  │
    │  │     └─ mcp_gateway.py ✅          → /mcp/*                       │  │
    │  └─────────────────────────────────────────────────────────────────────┘  │
    │                                                                            │
    │  ┌──────────────────────┬────────────────────┬──────────────────────┐    │
    │  │                      │                    │                      │    │
    │  ▼                      ▼                    ▼                      ▼    │
    │ ┌─────────────┐  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐ │
    │ │   AGENTS    │  │  CALCULATORS │   │ DATABASE     │   │   UTILS      │ │
    │ │ ┌─────────┐ │  │              │   │              │   │              │ │
    │ │ │RAG V2   │ │  │ ┌──────────┐ │   │ ┌──────────┐ │   │ ┌──────────┐ │ │
    │ │ │┌───────┐│ │  │ │Incapacid │ │   │ │SQLAlchemy│ │   │ │Embedding │ │ │
    │ │ ││Search ││ │  │ │Temporal  │ │   │ │          │ │   │ │Utils     │ │ │
    │ │ │├───────┤│ │  │ ├──────────┤ │   │ ├──────────┤ │   │ ├──────────┤ │ │
    │ │ ││Rerank ││ │  │ │Desempleo │ │   │ │Models    │ │   │ │PDF Parse │ │ │
    │ │ │├───────┤│ │  │ │          │ │   │ ├──────────┤ │   │ │          │ │ │
    │ │ ││Format ││ │  │ └──────────┘ │   │ │Schema    │ │   │ └──────────┘ │ │
    │ │ │└───────┘│ │  └──────────────┘   │ └──────────┘ │   └──────────────┘ │
    │ │ └─────────┘ │                     └──────────────┘                    │
    │ │             │                                                          │
    │ │ ┌─────────┐ │                                                          │
    │ │ │LLM      │ │                                                          │
    │ │ │Provider │ │                                                          │
    │ │ │Factory  │ │                                                          │
    │ │ │         │ │                                                          │
    │ │ │✓ Groq   │ │                                                          │
    │ │ │✓ Gemini │ │                                                          │
    │ │ │✓ Deep   │ │                                                          │
    │ │ │  Seek   │ │                                                          │
    │ │ │✓ Mistral│ │                                                          │
    │ │ └─────────┘ │                                                          │
    │ └─────────────┘                                                          │
    │                                                                            │
    └─────────────────────────────┬──────────────────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        │                         │                         │
    ┌───▼────────────┐   ┌────────▼─────────┐   ┌─────────▼────────┐
    │  QDRANT        │   │  PostgreSQL      │   │  LLM PROVIDERS   │
    │  :6333         │   │  :5432           │   │                  │
    │                │   │                  │   │  ┌─────────────┐ │
    │  Collections:  │   │  Tables:         │   │  │ GROQ        │ │
    │  ┌──────────┐ │   │  ┌──────────┐   │   │  │ llama-3.3   │ │
    │  │Knowledge │ │   │  │users     │   │   │  │ 70B/8B      │ │
    │  │v2        │ │   │  ├──────────┤   │   │  └─────────────┘ │
    │  │(48.8k)   │ │   │  │progress  │   │   │  ┌─────────────┐ │
    │  ├──────────┤ │   │  ├──────────┤   │   │  │ GEMINI      │ │
    │  │Leyes     │ │   │  │test_     │   │   │  │ 2.5 Pro     │ │
    │  │Master    │ │   │  │results   │   │   │  │ Flash       │ │
    │  │(54)      │ │   │  ├──────────┤   │   │  └─────────────┘ │
    │  └──────────┘ │   │  │generated │   │   │  ┌─────────────┐ │
    │                │   │  │_cases    │   │   │  │ DEEPSEEK    │ │
    │ Vector Dim:    │   │  ├──────────┤   │   │  │ V3          │ │
    │ 1024D (Dense)  │   │  │conversat │   │   │  │ Reasoner    │ │
    │ + Sparse BM25  │   │  │ions      │   │   │  └─────────────┘ │
    │                │   │  └──────────┘   │   │  ┌─────────────┐ │
    │ Hybrid Search  │   │                  │   │  │ MISTRAL     │ │
    └────────────────┘   └──────────────────┘   │  │ LOCAL       │ │
                                                 │  │ Salamandra  │ │
                                                 │  │ 7B          │ │
                                                 │  └─────────────┘ │
                                                 │  (VPS Hostinger) │
                                                 └──────────────────┘
```

---

## 🔄 FLUJO CHAT + RAG (Interactivo)

```
USUARIO ESCRIBE: "¿Qué es la incapacidad temporal?"
        │
        ↓ (50ms)
    FRONTEND
    ├─ Valida mensaje
    └─ POST /chat/stream
            │
            ↓ (100ms)
    BACKEND chat.py
    ├─ Parse request
    └─ useRAG = true → RAG Agent
            │
    ┌───────┴───────────────────────────────┐
    │                                        │
    ↓ (150ms)                         ↓
EMBEDDING                         LLM PROVIDER
├─ Convert query                 (Groq)
│  to vector                     ├─ Prepare
└─ pablosi/bge-m3               │  prompt
   1024D vector                 └─ Stream
        │                        │  response
        │                   ┌────┴─────┐
        ↓ (200ms)           │           │
    QDRANT SEARCH        [chunk 1]  [chunk 2]
    ├─ Layer 1 (Laws)    "La IT es" "...30%"
    │  Top 5
    ├─ Layer 2 (Materials)
    │  Top 5
    └─ Rerank
        │
        ↓ (250ms)
    FORMAT CONTEXT
    ├─ Combine layers
    └─ Build prompt
        │
        └────────────────→ SSE STREAM TO FRONTEND
                         (Streaming in real-time)
                         
TOTAL LATENCY: 1.5-2.5 segundos
```

---

## 📋 LISTA DE VERIFICACIÓN - ESTADO DEL SISTEMA

```
┌─ COMPONENTES
│
├─ [✅] Backend FastAPI
│   ├─ main.py OPERATIVO
│   ├─ 8 routers cargados
│   └─ Docs en :8000/docs
│
├─ [✅] Frontend React
│   ├─ Componentes compilados
│   ├─ 20+ componentes activos
│   └─ Página en :5173
│
├─ [✅] Qdrant Vector DB
│   ├─ 2 colecciones activas
│   ├─ 48,866 chunks indexados
│   └─ API en :6333
│
├─ [✅] PostgreSQL
│   ├─ Base de datos creada
│   ├─ Tablas schema completo
│   └─ Puerto 5432
│
├─ [✅] LLM Providers
│   ├─ Groq API configurado
│   ├─ Gemini API configurado
│   ├─ DeepSeek API configurado
│   └─ Mistral Local disponible
│
├─ [✅] RAG Agent V2
│   ├─ 2-layer architecture
│   ├─ Reranking jerárquico
│   └─ Búsqueda híbrida
│
├─ [✅] Generadores de Contenido
│   ├─ Casos prácticos
│   ├─ Simulacros
│   ├─ Mapas mentales
│   ├─ Flashcards
│   └─ Planes de estudio
│
├─ [✅] MCP Server
│   ├─ TypeScript compilado
│   ├─ Puerto 3000
│   └─ Gateway proxy
│
└─ [⚠️ ] Sistema de Agentes (Diseño)
    ├─ opos-agents/ existe
    └─ NO integrado en backend

┌─ DEPENDENCIAS
│
├─ [✅] Python 3.9+
├─ [✅] Node.js 18+
├─ [✅] Docker
├─ [✅] PostgreSQL 14+
└─ [✅] Qdrant

┌─ CONFIGURACIÓN
│
├─ [✅] .env.backend cargado
├─ [✅] QDRANT_URL configurado
├─ [✅] API Keys en variables
└─ [✅] CORS habilitado

┌─ SERVICIOS EXTERNOS
│
├─ [✅] Groq API (llama-3.3-70b)
├─ [✅] Google Gemini API
├─ [✅] DeepSeek API
└─ [✅] VPS Mistral (Salamandra 7B)
```

---

## 🎯 COMANDOS RÁPIDOS

### Iniciar Sistema Completo

```bash
# Terminal 1: Backend
cd /home/spas/OPOS_GEMINI_1/backend
python3 main.py

# Terminal 2: Frontend
cd /home/spas/OPOS_GEMINI_1/frontend
npm run dev

# Terminal 3: MCP Server (opcional)
cd /home/spas/OPOS_GEMINI_1/mcp-server
npm run dev
```

### URLs de Acceso

```
🌐 Frontend:   http://localhost:5173
📚 Docs:       http://localhost:8000/docs
🗄️  Qdrant:    http://localhost:6333
🔌 MCP Server: http://localhost:3000
```

### Tests Rápidos

```bash
# Test backend health
curl http://localhost:8000/docs

# Test Qdrant health
curl http://localhost:6333/health

# Test RAG search
curl -X POST http://localhost:8000/api/v2/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query":"incapacidad temporal"}'

# Test case generation
curl -X POST http://localhost:8000/ai/practical-case \
  -H "Content-Type: application/json" \
  -d '{"tema":"Incapacidad Temporal","dificultad":"media","provider":"groq"}'
```

---

## 📈 MÉTRICAS DE RENDIMIENTO

| Operación | Latencia Típica | P95 | Bottleneck |
|-----------|-----------------|-----|-----------|
| RAG Search | 200ms | 500ms | Qdrant |
| Embedding | 100ms | 150ms | Model loading |
| LLM Generation | 1-5s | 30s | API respuesta |
| Chat Stream | 500ms-2s | 5s | Network |
| Case Generation | 10-40s | 60s | LLM |
| Mock Exam (100q) | 60-120s | 180s | LLM batch |

---

## 🔗 RELACIONES ENTRE COMPONENTES

```
Frontend React
    ↓ REST API
Backend FastAPI
    ↓
    ├→ Chat Router → RAG Agent V2 → Qdrant
    ├→ AI Functions → LLM Providers → External APIs
    ├→ User Router → PostgreSQL
    ├→ Upload Router → File Storage
    └→ MCP Gateway → External Systems

Vector DB (Qdrant)
    ├→ Dense Vectors (1024D)
    ├→ Sparse Index (BM25)
    └→ Metadata Payload

LLM Providers
    ├→ Groq (API)
    ├→ Gemini (API)
    ├→ DeepSeek (API)
    └→ Mistral (Local VPS)
```

---

## 📚 DOCUMENTOS DE REFERENCIA

- `ARQUITECTURA_ACTUAL_20_01_26.md` - Análisis detallado
- `PLAN_EJECUTIVO_FINAL_21_01_26.md` - Plan de negocio
- `ARQUITECTURA_COMPLETA_DETALLADA_22_01_26.md` - ⭐ DOCUMENTO PRINCIPAL

---

**Generado:** 22 Enero 2026  
**Versión:** 1.0 - DIAGRAMA TÉCNICO
