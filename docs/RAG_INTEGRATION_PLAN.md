# RAG + Qdrant Integration Plan - OpositaIA

## 🎯 Objetivo

Integrar un sistema RAG (Retrieval Augmented Generation) con Qdrant para mejorar las respuestas de OpositaIA usando documentación legal del BOE y materiales de estudio.

## 📊 Recursos Disponibles

### Local Infrastructure
- ✅ **Docker**: v27.5.1 (WSL)
- ✅ **Ollama**: Corriendo en puerto 11434
  - `tinyllama:latest` (637 MB) - Para embeddings rápidos
  - `all-minilm:latest` (45 MB) - Para embeddings ligeros
- ✅ **Qdrant**: Instalado pero detenido (puerto 6333-6334)
- ✅ **PostgreSQL + pgvector**: Corriendo (puerto 5432)
- ✅ **Mistral 8B GGUF**: VPS Hostinger (root@147.93.95.67)
  - Modelo cuantizado, eficiente
  - Ideal para tareas medianas
  - Ya instalado y configurado

### Repositorios de Referencia
1. **justicio** - RAG para BOE
   - FastAPI backend
   - Qdrant para vectores
   - Embeddings en español
   - ETL diario de BOE
   
2. **BOE_API_Enhanced** - API BOE con IA
   - Integración con API oficial BOE (sin scraping)
   - Qdrant + Mistral + Cohere
   - Búsqueda semántica
   - Comparador de versiones
   
3. **V0Opos** - Plataforma oposiciones
   - Next.js + PocketBase
   - Endpoints BOE API documentados
   - UI/UX de referencia
   
4. **Mind-map-API** - FastAPI para mapas mentales
   - Estructura de API REST
   - Integración con LLMs

5. **transformersDSEEK** - Fine-tuning de modelos
   - Google Colab notebooks
   - Técnicas de fine-tuning

## 🏗️ Arquitectura Propuesta

```
┌──────────────────────────────────────────────────────────────────┐
│                     OpositaIA Frontend                            │
│                    (React + TypeScript)                           │
│                    Vercel Free Tier ($0/mes)                      │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ├──────────────┬──────────────┬────────────┐
                         │              │              │            │
                    ┌────▼────┐   ┌────▼────┐   ┌────▼────┐  ┌───▼────┐
                    │ Gemini  │   │ Mistral │   │ Ollama  │  │FastAPI │
                    │   API   │   │   8B    │   │  Local  │  │Backend │
                    │ (Cloud) │   │  (VPS)  │   │ (WSL)   │  │ (VPS)  │
                    │ $0/mes  │   │ $0/mes  │   │ $0/mes  │  │ $0/mes │
                    └─────────┘   └────┬────┘   └────┬────┘  └───┬────┘
                                       │             │            │
                                       └─────────────┴────────────┘
                                                     │
                                       ┌─────────────▼──────────────┐
                                       │   Qdrant Vector DB         │
                                       │   (Docker/WSL or VPS)      │
                                       │   - BOE Documents          │
                                       │   - Study Materials        │
                                       │   - Legal Texts            │
                                       │   $0/mes (self-hosted)     │
                                       └────────────┬───────────────┘
                                                    │
                                       ┌────────────▼───────────────┐
                                       │   BOE API Oficial          │
                                       │   (Datos Abiertos)         │
                                       │   - Sin API key            │
                                       │   - Sin límites            │
                                       │   $0/mes                   │
                                       └────────────────────────────┘

COSTO TOTAL: $0/mes 🎉
```

## 📋 Fases de Implementación

### Fase 1: Infraestructura Base (Semana 1)

#### 1.1 Docker Compose Setup
**Archivo**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: opositaia-qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
    restart: unless-stopped
    networks:
      - opositaia-network

  ollama:
    image: ollama/ollama:latest
    container_name: opositaia-ollama
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama
    restart: unless-stopped
    networks:
      - opositaia-network

  fastapi:
    build: ./backend
    container_name: opositaia-backend
    ports:
      - "8000:8000"
    environment:
      - QDRANT_URL=http://qdrant:6333
      - OLLAMA_URL=http://ollama:11434
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - qdrant
      - ollama
    restart: unless-stopped
    networks:
      - opositaia-network

networks:
  opositaia-network:
    driver: bridge

volumes:
  qdrant_storage:
  ollama_data:
```

#### 1.2 Variables de Entorno
**Archivo**: `.env.backend`

```bash
# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Opcional para producción
QDRANT_COLLECTION_NAME=opositaia_documents

# Ollama Configuration (Local WSL)
OLLAMA_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=all-minilm
OLLAMA_LLM_MODEL=tinyllama

# Mistral Configuration (VPS Hostinger)
MISTRAL_URL=http://147.93.95.67:8000
MISTRAL_MODEL=mistral-8b-gguf
MISTRAL_API_KEY=  # Si está protegido

# Gemini Configuration (Cloud fallback)
GEMINI_API_KEY=your_key_here

# BOE API Configuration (Oficial, sin API key)
BOE_BASE_URL=https://www.boe.es
BOE_API_URL=https://www.boe.es/diario_boe/xml.php

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Vector Database Settings
VECTOR_DIMENSION=384  # all-minilm dimension
CHUNK_SIZE=512
CHUNK_OVERLAP=50
TOP_K_RESULTS=5

# ETL Configuration
ETL_SCHEDULE_CRON=0 2 * * *  # 2 AM daily
ETL_DAYS_BACK=30  # Días hacia atrás para sincronizar

# Model Selection Strategy
DEFAULT_MODEL=mistral  # gemini | mistral | ollama
EMBEDDING_MODEL=ollama  # Siempre usar Ollama (gratis)
```

#### 1.3 Actualizar .gitignore

```gitignore
# Backend
backend/__pycache__/
backend/.pytest_cache/
backend/venv/
backend/.env.backend

# Docker volumes
qdrant_storage/
ollama_data/

# API Keys
.env
.env.local
.env.backend
.env.production
```

### Fase 2: Backend FastAPI (Semana 2)

#### 2.1 Estructura del Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py          # Pydantic models
│   │   └── embeddings.py       # Embedding models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── qdrant_service.py   # Qdrant operations
│   │   ├── ollama_service.py   # Ollama integration
│   │   ├── mistral_service.py  # Mistral 8B (VPS)
│   │   ├── gemini_service.py   # Gemini fallback
│   │   ├── boe_api_service.py  # BOE API oficial
│   │   └── rag_service.py      # RAG orchestration
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── search.py           # Search endpoints
│   │   ├── documents.py        # Document management
│   │   ├── boe.py              # BOE endpoints
│   │   └── health.py           # Health checks
│   └── utils/
│       ├── __init__.py
│       ├── text_processing.py  # Text chunking
│       └── boe_parser.py       # BOE XML/JSON parser
├── tests/
│   ├── __init__.py
│   ├── test_qdrant.py
│   ├── test_ollama.py
│   └── test_rag.py
├── Dockerfile
├── requirements.txt
└── README.md
```

#### 2.2 Dependencias Backend
**Archivo**: `backend/requirements.txt`

```txt
# FastAPI
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.0
pydantic-settings==2.6.0

# Vector Database
qdrant-client==1.12.0

# Embeddings & LLM
sentence-transformers==3.3.0
ollama==0.4.0

# Mistral (VPS)
mistralai==1.0.0
# O usar requests directamente al endpoint

# Gemini (fallback)
google-generativeai==0.8.0

# Text Processing
langchain==0.3.0
langchain-community==0.3.0
beautifulsoup4==4.12.0
lxml==5.3.0

# BOE API (oficial, sin scraping)
requests==2.31.0
xmltodict==0.13.0

# Utilities
python-dotenv==1.0.0
httpx==0.27.0
aiofiles==24.1.0

# Testing
pytest==8.3.0
pytest-asyncio==0.24.0
pytest-cov==6.0.0

# Monitoring
prometheus-client==0.21.0
```

#### 2.3 Servicio Mistral 8B
**Archivo**: `backend/app/services/mistral_service.py`

```python
import httpx
from typing import List, Dict

class MistralService:
    def __init__(self):
        self.base_url = "http://147.93.95.67:8000"  # VPS Hostinger
        self.model = "mistral-8b-gguf"
    
    async def generate(self, prompt: str, max_tokens: int = 512) -> str:
        """Generate text using Mistral 8B on VPS"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/v1/completions",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                }
            )
            return response.json()["choices"][0]["text"]
    
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings using Mistral"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/v1/embeddings",
                json={"model": self.model, "input": text}
            )
            return response.json()["data"][0]["embedding"]
```

#### 2.4 Servicio BOE API
**Archivo**: `backend/app/services/boe_api_service.py`

```python
import httpx
import xmltodict
from datetime import datetime
from typing import List, Dict, Optional

class BOEAPIService:
    """
    Servicio para interactuar con la API oficial del BOE
    Basado en: https://github.com/Espasiko/BOE_API_Enhanced
    """
    def __init__(self):
        self.base_url = "https://www.boe.es"
        self.api_base = f"{self.base_url}/diario_boe/xml.php"
    
    async def get_sumario(self, fecha: str) -> Dict:
        """
        Obtener sumario del BOE para una fecha
        
        Args:
            fecha: Formato YYYYMMDD (ej: "20250116")
        
        Returns:
            Dict con el sumario parseado
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.api_base,
                params={"id": f"BOE-S-{fecha}"}
            )
            # Parse XML to dict
            data = xmltodict.parse(response.text)
            return data
    
    async def buscar_documento(
        self,
        texto: str,
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None
    ) -> List[Dict]:
        """
        Buscar documentos en el BOE
        
        Args:
            texto: Texto a buscar
            fecha_desde: Fecha inicio (YYYYMMDD)
            fecha_hasta: Fecha fin (YYYYMMDD)
        
        Returns:
            Lista de documentos encontrados
        """
        params = {
            "texto": texto,
            "formato": "json"
        }
        if fecha_desde:
            params["fecha_desde"] = fecha_desde
        if fecha_hasta:
            params["fecha_hasta"] = fecha_hasta
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/buscar/doc",
                params=params
            )
            return response.json()
    
    async def get_documento_pdf(self, doc_id: str) -> bytes:
        """Descargar PDF de un documento"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/datos/pdfs/{doc_id}.pdf"
            )
            return response.content
```

#### 2.5 Ejemplo de Endpoint RAG

```python
# backend/app/routers/search.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import SearchRequest, SearchResponse
from app.services.rag_service import RAGService

router = APIRouter(prefix="/api/v1/search", tags=["search"])
rag_service = RAGService()

@router.post("/", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """
    Perform RAG search on legal documents
    
    - Uses Ollama for embeddings (local, free)
    - Searches Qdrant vector database
    - Generates answer with Gemini, Mistral or Ollama
    """
    try:
        # 1. Generate embedding for query
        query_embedding = await rag_service.embed_query(request.query)
        
        # 2. Search similar documents in Qdrant
        similar_docs = await rag_service.search_similar(
            query_embedding,
            top_k=request.top_k or 5,
            filters=request.filters
        )
        
        # 3. Generate answer using RAG
        # Model selection: gemini (complex), mistral (medium), ollama (simple)
        answer = await rag_service.generate_answer(
            query=request.query,
            context_docs=similar_docs,
            model=request.model or "mistral"  # Default: Mistral 8B (free)
        )
        
        return SearchResponse(
            answer=answer,
            sources=similar_docs,
            model_used=request.model or "mistral"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Fase 3: Integración Frontend (Semana 3)

#### 3.1 Nuevo Servicio RAG
**Archivo**: `services/ragService.ts`

```typescript
import { SearchRequest, SearchResponse, Document } from '../types';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export async function searchWithRAG(
  query: string,
  options?: {
    topK?: number;
    model?: 'gemini' | 'ollama';
    filters?: Record<string, any>;
  }
): Promise<SearchResponse> {
  const response = await fetch(`${BACKEND_URL}/api/v1/search/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      top_k: options?.topK || 5,
      model: options?.model || 'gemini',
      filters: options?.filters || {}
    })
  });

  if (!response.ok) {
    throw new Error(`RAG search failed: ${response.statusText}`);
  }

  return response.json();
}

export async function uploadDocument(
  file: File,
  metadata?: Record<string, any>
): Promise<{ success: boolean; document_id: string }> {
  const formData = new FormData();
  formData.append('file', file);
  if (metadata) {
    formData.append('metadata', JSON.stringify(metadata));
  }

  const response = await fetch(`${BACKEND_URL}/api/v1/documents/upload`, {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    throw new Error(`Document upload failed: ${response.statusText}`);
  }

  return response.json();
}
```

#### 3.2 Actualizar Variables de Entorno Frontend
**Archivo**: `.env`

```bash
# Gemini API (Cloud)
VITE_API_KEY=your_gemini_key_here

# Backend API (Local)
VITE_BACKEND_URL=http://localhost:8000

# Feature Flags
VITE_ENABLE_RAG=true
VITE_ENABLE_OLLAMA=true
VITE_ENABLE_MULTI_PROVIDER=true
```

#### 3.3 Componente de Configuración Multi-Provider
**Archivo**: `components/ProviderSettings.tsx`

```typescript
import React, { useState } from 'react';

interface Provider {
  id: string;
  name: string;
  enabled: boolean;
  apiKey?: string;
  endpoint?: string;
  cost: string;
  speed: 'fast' | 'medium' | 'slow';
  quality: 'high' | 'medium' | 'low';
}

export const ProviderSettings: React.FC = () => {
  const [providers, setProviders] = useState<Provider[]>([
    {
      id: 'gemini',
      name: 'Google Gemini',
      enabled: true,
      cost: 'Gratis (15 req/min)',
      speed: 'fast',
      quality: 'high'
    },
    {
      id: 'mistral',
      name: 'Mistral 8B (VPS)',
      enabled: true,
      endpoint: 'http://147.93.95.67:8000',
      cost: 'Gratis (self-hosted)',
      speed: 'medium',
      quality: 'medium'
    },
    {
      id: 'ollama',
      name: 'Ollama (Local)',
      enabled: true,
      endpoint: 'http://localhost:11434',
      cost: 'Gratis (local)',
      speed: 'fast',
      quality: 'low'
    },
    {
      id: 'openai',
      name: 'OpenAI GPT-4',
      enabled: false,
      cost: '$0.03/1K tokens',
      speed: 'medium',
      quality: 'high'
    },
    {
      id: 'anthropic',
      name: 'Claude (Anthropic)',
      enabled: false,
      cost: '$0.015/1K tokens',
      speed: 'medium',
      quality: 'high'
    },
  ]);

  return (
    <div className="provider-settings">
      <h2>🤖 Configuración de Proveedores de IA</h2>
      <p className="subtitle">
        Elige qué modelos usar. Los modelos gratuitos están habilitados por defecto.
      </p>
      
      {providers.map(provider => (
        <div key={provider.id} className={`provider-card ${provider.enabled ? 'enabled' : ''}`}>
          <div className="provider-header">
            <input
              type="checkbox"
              checked={provider.enabled}
              onChange={(e) => {
                setProviders(prev =>
                  prev.map(p =>
                    p.id === provider.id ? { ...p, enabled: e.target.checked } : p
                  )
                );
              }}
            />
            <label>{provider.name}</label>
            <span className={`badge ${provider.cost.includes('Gratis') ? 'free' : 'paid'}`}>
              {provider.cost}
            </span>
          </div>
          
          <div className="provider-stats">
            <span className={`stat speed-${provider.speed}`}>
              ⚡ {provider.speed}
            </span>
            <span className={`stat quality-${provider.quality}`}>
              ⭐ {provider.quality}
            </span>
          </div>
          
          {provider.enabled && !provider.cost.includes('Gratis') && (
            <input
              type="password"
              placeholder="API Key (requerida)"
              className="api-key-input"
              onChange={(e) => {
                setProviders(prev =>
                  prev.map(p =>
                    p.id === provider.id ? { ...p, apiKey: e.target.value } : p
                  )
                );
              }}
            />
          )}
        </div>
      ))}
      
      <div className="provider-recommendation">
        <h3>💡 Recomendación</h3>
        <ul>
          <li><strong>Tareas complejas</strong>: Gemini (gratis, alta calidad)</li>
          <li><strong>Tareas medianas</strong>: Mistral 8B (gratis, buena calidad)</li>
          <li><strong>Embeddings</strong>: Ollama (gratis, rápido)</li>
        </ul>
      </div>
    </div>
  );
};
```

### Fase 4: ETL y Carga de Datos (Semana 4)

#### 4.1 Script de Carga Inicial
**Archivo**: `backend/scripts/load_initial_data.py`

```python
import asyncio
from datetime import datetime, timedelta
from app.services.qdrant_service import QdrantService
from app.services.ollama_service import OllamaService
from app.services.boe_api_service import BOEAPIService

async def load_boe_documents(days_back: int = 30):
    """
    Load BOE documents into Qdrant using official BOE API
    
    Args:
        days_back: Number of days to go back from today
    """
    qdrant = QdrantService()
    ollama = OllamaService()
    boe_api = BOEAPIService()
    
    print(f"📥 Loading BOE documents from last {days_back} days...")
    
    # 1. Fetch BOE documents using official API (no scraping!)
    documents = []
    today = datetime.now()
    
    for i in range(days_back):
        date = today - timedelta(days=i)
        fecha_str = date.strftime("%Y%m%d")
        
        try:
            # Get sumario for this date
            sumario = await boe_api.get_sumario(fecha_str)
            
            # Parse documents from sumario
            if 'sumario' in sumario and 'diario' in sumario['sumario']:
                diario = sumario['sumario']['diario']
                
                # Extract documents
                for seccion in diario.get('seccion', []):
                    for departamento in seccion.get('departamento', []):
                        for epigrafe in departamento.get('epigrafe', []):
                            for item in epigrafe.get('item', []):
                                doc = {
                                    'id': item.get('@id'),
                                    'title': item.get('titulo'),
                                    'text': item.get('texto', ''),
                                    'date': fecha_str,
                                    'section': seccion.get('@nombre'),
                                    'department': departamento.get('@nombre'),
                                    'url': f"https://www.boe.es/boe/dias/{fecha_str[:4]}/{fecha_str[4:6]}/{fecha_str[6:]}/pdfs/{item.get('@id')}.pdf"
                                }
                                documents.append(doc)
            
            print(f"✅ Loaded {len(documents)} docs from {fecha_str}")
        
        except Exception as e:
            print(f"⚠️  Error loading {fecha_str}: {e}")
            continue
    
    print(f"\n📊 Total documents fetched: {len(documents)}")
    
    # 2. Generate embeddings using Ollama (free!)
    print("🔄 Generating embeddings...")
    for i, doc in enumerate(documents):
        if i % 100 == 0:
            print(f"  Progress: {i}/{len(documents)}")
        
        # Combine title and text for embedding
        text_to_embed = f"{doc['title']} {doc['text']}"
        embedding = await ollama.generate_embedding(text_to_embed)
        doc['embedding'] = embedding
    
    # 3. Upload to Qdrant
    print("💾 Uploading to Qdrant...")
    await qdrant.upsert_documents(documents)
    
    print(f"✅ Successfully loaded {len(documents)} documents into Qdrant!")
    print(f"💰 Cost: $0 (using official BOE API + local Ollama)")

if __name__ == "__main__":
    asyncio.run(load_boe_documents(days_back=30))
```

#### 4.2 Cron Job para ETL Diario
**Archivo**: `backend/scripts/daily_etl.sh`

```bash
#!/bin/bash
# Run daily at 2 AM

cd /path/to/backend
source venv/bin/activate
python scripts/load_initial_data.py
```

### Fase 5: CI/CD Pipeline (Semana 5)

#### 5.1 GitHub Actions Workflow
**Archivo**: `.github/workflows/backend-ci.yml`

```yaml
name: Backend CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - 'backend/**'
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      qdrant:
        image: qdrant/qdrant:latest
        ports:
          - 6333:6333
      
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        env:
          QDRANT_URL: http://localhost:6333
        run: |
          cd backend
          pytest tests/ --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          # Deploy script here
```

## 💰 Modelo de Monetización

### Opción 1: Freemium con Límites
```
Free Tier:
- 50 búsquedas RAG/día
- Ollama local (gratis)
- Gemini Flash (rápido, barato)

Pro Tier ($9.99/mes):
- 500 búsquedas RAG/día
- Acceso a Gemini Pro
- Prioridad en respuestas
- Sin anuncios

Enterprise ($49.99/mes):
- Búsquedas ilimitadas
- API key propia
- Soporte prioritario
- Datos privados
```

### Opción 2: BYOK (Bring Your Own Key)
```
- Usuario usa su propia API key
- Nosotros cobramos por:
  - Infraestructura RAG (Qdrant hosting)
  - Backend FastAPI
  - Mantenimiento de datos BOE
  - Features premium
  
Precio: $4.99/mes por infraestructura
```

### Opción 3: Híbrido
```
Free:
- Ollama local (100% gratis)
- Datos públicos BOE

Premium:
- Gemini con nuestra key ($9.99/mes)
- O tu propia key ($4.99/mes)
- Datos privados + RAG
```

## 🔐 Seguridad de API Keys

### Backend (.env.backend)
```bash
# NUNCA commitear este archivo
GEMINI_API_KEY=secret_key_here
QDRANT_API_KEY=secret_key_here
```

### Frontend (.env)
```bash
# Solo URL del backend, NO keys
VITE_BACKEND_URL=http://localhost:8000
VITE_ENABLE_RAG=true
```

### Gestión de Keys de Usuario
```typescript
// Guardar en localStorage encriptado
const encryptedKey = await encryptAPIKey(userKey);
localStorage.setItem('user_api_key', encryptedKey);

// Enviar al backend con headers
headers: {
  'X-User-API-Key': encryptedKey
}
```

## 📊 Métricas y Monitoreo

### Prometheus Metrics
```python
from prometheus_client import Counter, Histogram

rag_searches = Counter('rag_searches_total', 'Total RAG searches')
rag_latency = Histogram('rag_latency_seconds', 'RAG search latency')
```

### Health Checks
```python
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "qdrant": await qdrant_service.health(),
        "ollama": await ollama_service.health(),
        "gemini": await gemini_service.health()
    }
```

## 🚀 Deployment

### Local Development
```bash
# 1. Start infrastructure
docker-compose up -d

# 2. Load initial data
cd backend
python scripts/load_initial_data.py

# 3. Start backend
uvicorn app.main:app --reload

# 4. Start frontend
npm run dev
```

### Production (Render/Railway)
```bash
# Backend: Deploy FastAPI to Render
# Frontend: Deploy React to Vercel/Netlify
# Qdrant: Qdrant Cloud (free tier)
# Ollama: Self-hosted or Replicate API
```

## 📝 Checklist de Implementación

### Semana 1: Infraestructura
- [ ] Crear docker-compose.yml
- [ ] Configurar Qdrant
- [ ] Configurar Ollama
- [ ] Actualizar .gitignore
- [ ] Crear .env.backend
- [ ] Documentar setup

### Semana 2: Backend
- [ ] Estructura FastAPI
- [ ] Qdrant service
- [ ] Ollama service
- [ ] RAG service
- [ ] Endpoints REST
- [ ] Tests unitarios
- [ ] Tests de integración

### Semana 3: Frontend
- [ ] ragService.ts
- [ ] ProviderSettings component
- [ ] Actualizar .env
- [ ] Integrar con backend
- [ ] UI para multi-provider
- [ ] Tests E2E

### Semana 4: Datos
- [ ] BOE scraper
- [ ] ETL script
- [ ] Carga inicial
- [ ] Cron job
- [ ] Validación de datos

### Semana 5: CI/CD
- [ ] GitHub Actions
- [ ] Tests automatizados
- [ ] Deploy pipeline
- [ ] Monitoring
- [ ] Documentación

## 🎓 Recursos de Aprendizaje

### Justicio (tu repo)
- Arquitectura RAG completa
- Integración Qdrant
- ETL de BOE
- FastAPI patterns

### Mind-map-API (tu repo)
- FastAPI structure
- API design
- Deployment en Render

### transformersDSEEK (tu repo)
- Fine-tuning embeddings
- Google Colab notebooks
- Optimización de modelos

## 📚 Documentación Adicional

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Ollama Documentation](https://ollama.ai/docs)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering/)

---

**Última actualización**: 2025-01-16  
**Versión**: 1.0.0  
**Estado**: Ready to implement 🚀
