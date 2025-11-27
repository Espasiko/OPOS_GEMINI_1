# OpositAIA Backend

Multi-Agent AI System for Spanish Social Security Exam Preparation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              ORQUESTADOR PRINCIPAL (Gemini 2.0)             │
│  - Decide qué agente usar según la consulta del usuario     │
│  - Mantiene contexto conversacional                         │
│  - Coordina respuestas de múltiples agentes                 │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│   AGENTE RAG     │ │ AGENTE ANÁLISIS  │ │  AGENTE QUIZ     │
│   (Búsqueda)     │ │   (Progreso)     │ │  (Evaluación)    │
└──────────────────┘ └──────────────────┘ └──────────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Qdrant Vector DB │ │ PostgreSQL       │ │ Gemini Flash     │
│ + bge-m3         │ │ (User Progress)  │ │ (Generación)     │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.backend.example .env.backend
# Edit .env.backend with your credentials
```

**Required:**
- `GEMINI_API_KEY`: Get from https://aistudio.google.com/app/apikey
- `POSTGRES_*`: PostgreSQL connection details

### 3. Initialize Database

```bash
python database/init_db.py
```

This will:
- Create `opositaia` database
- Create 8 tables (user_progress, answer_history, etc.)
- Create views for analytics
- Create triggers for auto-updates

### 4. Start Backend

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test RAG Endpoint

```bash
curl -X POST http://localhost:8000/api/rag/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "¿Qué es la incapacidad temporal?",
    "top_k": 5,
    "min_score": 0.7
  }'
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧠 Agents

### 1. RAG Agent (✅ Implemented)

**Endpoint**: `POST /api/rag/search`

**Purpose**: Search BOE documents using semantic search

**Features**:
- Uses `bge-m3` embeddings (1024 dims, Spanish legal)
- Qdrant vector database
- Top-k results with score threshold
- Optional topic filtering

**Example**:
```json
{
  "query": "¿Qué es la incapacidad temporal?",
  "top_k": 5,
  "min_score": 0.7,
  "tema_filter": 3
}
```

**Response**:
```json
{
  "query": "¿Qué es la incapacidad temporal?",
  "documents": [
    {
      "id": "doc_123",
      "score": 0.89,
      "content": "La incapacidad temporal es...",
      "metadata": {
        "titulo": "Real Decreto 625/2014",
        "tema_id": 3,
        "tema_nombre": "Incapacidad Temporal",
        "fuente": "BOE",
        "url_boe": "https://...",
        "fecha": "2014-07-25"
      }
    }
  ],
  "context": "[Documento 1] Real Decreto 625/2014...",
  "metadata": {
    "total_documents": 5,
    "top_score": 0.89,
    "search_time_ms": 234,
    "embedding_model": "bge-m3"
  }
}
```

### 2. Analysis Agent (🚧 TODO)

**Endpoint**: `GET /api/analysis/weaknesses`

**Purpose**: Analyze user progress and detect weak topics

**Features**:
- Calculate precision by topic
- Identify topics <70% accuracy
- Generate personalized recommendations

### 3. Quiz Agent (🚧 TODO)

**Endpoint**: `POST /api/quiz/generate`

**Purpose**: Generate adaptive questions

**Features**:
- Generate questions with Gemini
- Adaptive difficulty
- Evaluate answers
- Track history

### 4. Recommendations Agent (🚧 TODO)

**Endpoint**: `GET /api/recommendations`

**Purpose**: Proactive suggestions

**Features**:
- "You fail at IT, review topic 3"
- Study streak tracking
- Next steps suggestions

## 🗄️ Database Schema

### Tables

1. **user_progress**: Overall user stats
2. **answer_history**: Every answer submitted
3. **user_cases**: User-created practical cases
4. **simulacros**: Mock exam results
5. **mind_maps**: User mind maps
6. **study_sessions**: Session tracking
7. **recommendations**: AI recommendations
8. **rag_queries**: RAG search logs

### Views

- `user_performance_by_topic`: Precision by topic
- `user_weak_topics`: Topics <70% accuracy
- `user_study_streaks`: Study streak stats

### Functions

- `update_user_progress_after_answer()`: Auto-update progress
- `calculate_weak_topics(user_id)`: Get weak topics
- `update_weak_topics(user_id)`: Refresh weak topics

## 🔧 Configuration

### Embeddings Model

**Current**: `bge-m3` (1024 dims, Spanish legal)

**Alternatives**:
- `all-minilm` (384 dims, faster but less accurate)
- `nomic-embed-text` (variable dims)

**Change in `.env.backend`**:
```bash
OLLAMA_EMBEDDING_MODEL=bge-m3
VECTOR_DIMENSION=1024
```

**Note**: If you change dimensions, you must recreate Qdrant collection:
```bash
curl -X DELETE http://localhost:6333/collections/opositaia_documents
curl -X PUT http://localhost:6333/collections/opositaia_documents \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 1024, "distance": "Cosine"}}'
```

### PostgreSQL

**Local**:
```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=opositaia
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

**Docker**:
```bash
docker run -d \
  --name opositaia-postgres \
  -e POSTGRES_DB=opositaia \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:15
```

## 📊 Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# RAG health
curl http://localhost:8000/api/rag/health

# Qdrant stats
curl http://localhost:8000/api/rag/stats
```

### Logs

```bash
# View logs
tail -f logs/backend.log

# Filter errors
grep ERROR logs/backend.log
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_rag_agent.py
```

## 🐳 Docker

```bash
# Build
docker build -t opositaia-backend .

# Run
docker run -d \
  --name opositaia-backend \
  -p 8000:8000 \
  --env-file .env.backend \
  opositaia-backend
```

## 📝 Development

### Add New Agent

1. Create `backend/agents/new_agent.py`
2. Create `backend/routers/new_agent.py`
3. Add router to `main.py`
4. Update `agents/__init__.py`

### Add New Endpoint

1. Add to existing router in `backend/routers/`
2. Define Pydantic models
3. Add tests in `tests/`

## 🔐 Security

- API keys in `.env.backend` (never commit)
- CORS configured for production
- Input validation with Pydantic
- SQL injection protection (parameterized queries)

## 📚 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [bge-m3 Model](https://huggingface.co/BAAI/bge-m3)
- [Gemini API](https://ai.google.dev/gemini-api/docs)

## 🤝 Contributing

1. Create feature branch
2. Add tests
3. Update docs
4. Submit PR

## 📄 License

MIT
