---
title: Integración Frontend-Backend con Mistral + RAG
status: planned
priority: critical
created: 2025-11-19
sprint: 7
estimated_days: 7-8
---

# 🎯 SPEC: Integración Frontend-Backend con Mistral + RAG

## 📋 CONTEXTO

**Problema actual**:
- Frontend usa Gemini API directamente desde navegador
- Backend FastAPI con RAG no está conectado
- Archivos se procesan en cliente, no en servidor
- Mistral en VPS no se está usando

**Objetivo**:
Conectar frontend React con backend FastAPI para usar Mistral + RAG en lugar de Gemini directo.

---

## 🎯 OBJETIVOS DEL SPRINT

### Sprint 7: Integración Frontend-Backend (7-8 días)

**Objetivo principal**: Conectar frontend con backend y migrar de Gemini a Mistral + RAG

**Entregables**:
1. ✅ Servicio de backend en frontend
2. ✅ Endpoint de chat con streaming
3. ✅ Endpoint de upload de archivos
4. ✅ Tests de integración
5. ✅ Documentación actualizada

---

## 📊 ARQUITECTURA OBJETIVO

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Frontend (React + Vite)            │
│  - ChatView.tsx                     │
│  - services/backendService.ts  ✨   │
│  - services/mistralService.ts  ✨   │
└──────────────┬──────────────────────┘
               │ HTTP/WebSocket
               ▼
┌─────────────────────────────────────┐
│  Backend (FastAPI)                  │
│  - /chat/stream  ✨                 │
│  - /upload  ✨                      │
│  - /rag/search (existente)          │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│   Qdrant    │  │   Mistral   │
│   (RAG)     │  │   (VPS)     │
└─────────────┘  └─────────────┘
```

---

## 🔧 TAREAS DETALLADAS

### Fase 1: Setup Backend (Días 1-2)

#### Tarea 1.1: Crear Router de Chat
**Archivo**: `backend/routers/chat.py`

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator
import httpx

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    use_rag: bool = True
    top_k: int = 3

class ChatResponse(BaseModel):
    response: str
    sources: list[dict] = []
    conversation_id: str

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Chat con streaming usando Mistral + RAG
    """
    async def generate():
        # 1. Consultar RAG si use_rag=True
        context = ""
        sources = []
        
        if request.use_rag:
            from agents.rag_agent_v2 import RAGAgentV2
            rag = RAGAgentV2()
            
            results = rag.search(
                query=request.message,
                top_k=request.top_k,
                layer_filter=None
            )
            
            context = "\n\n".join([
                f"[{r['metadata']['norma_completa']}]\n{r['content']}"
                for r in results['documents']
            ])
            
            sources = [
                {
                    "norma": r['metadata']['norma_completa'],
                    "articulo": r['metadata'].get('articulo'),
                    "score": r['score']
                }
                for r in results['documents']
            ]
        
        # 2. Construir prompt con contexto
        system_prompt = """Eres un experto tutor en legislación de Seguridad Social española.
Tu objetivo es ayudar a opositores a preparar el examen C1 de Seguridad Social.

Cuando respondas:
1. Sé preciso y cita artículos específicos
2. Explica paso a paso
3. Usa ejemplos prácticos
4. Responde en español
"""
        
        user_prompt = request.message
        if context:
            user_prompt = f"""Contexto legal relevante:
{context}

---

Pregunta del usuario: {user_prompt}

Responde basándote en el contexto legal proporcionado."""
        
        # 3. Llamar a Mistral con streaming
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                "http://147.93.95.67:8001/v1/chat/completions",
                json={
                    "model": "mistral-8b",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "stream": True,
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        chunk = line[6:]
                        if chunk != "[DONE]":
                            yield f"data: {chunk}\n\n"
                
                # Enviar fuentes al final
                if sources:
                    import json
                    yield f"data: {json.dumps({'sources': sources})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    Chat sin streaming (para compatibilidad)
    """
    # Similar a /stream pero acumula respuesta completa
    pass
```

**Tests**:
```python
# backend/tests/test_chat.py
import pytest
from fastapi.testclient import TestClient

def test_chat_stream():
    response = client.post("/chat/stream", json={
        "message": "¿Qué es la incapacidad temporal?",
        "conversation_id": "test-123",
        "use_rag": True
    })
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]

def test_chat_with_rag():
    response = client.post("/chat/message", json={
        "message": "Duración máxima IT",
        "conversation_id": "test-123",
        "use_rag": True
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["sources"]) > 0
```

---

#### Tarea 1.2: Crear Router de Upload
**Archivo**: `backend/routers/upload.py`

```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import pypdf
import io

router = APIRouter(prefix="/upload", tags=["upload"])

class UploadResponse(BaseModel):
    document_id: str
    filename: str
    text_length: int
    pages: int = None
    indexed: bool = False

@router.post("/file", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Sube un archivo y extrae su texto
    """
    # Validar tipo de archivo
    allowed_types = ["application/pdf", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, "Tipo de archivo no soportado")
    
    # Leer contenido
    content = await file.read()
    
    # Extraer texto según tipo
    if file.content_type == "application/pdf":
        pdf = pypdf.PdfReader(io.BytesIO(content))
        text = "\n".join([page.extract_text() for page in pdf.pages])
        pages = len(pdf.pages)
    else:
        text = content.decode('utf-8')
        pages = None
    
    # Generar ID único
    import uuid
    doc_id = str(uuid.uuid4())
    
    # Guardar en caché temporal (Redis o memoria)
    # TODO: Implementar caché
    
    return UploadResponse(
        document_id=doc_id,
        filename=file.filename,
        text_length=len(text),
        pages=pages,
        indexed=False
    )

@router.post("/url")
async def upload_url(url: str):
    """
    Descarga contenido de una URL y extrae texto
    """
    import httpx
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        
        # Extraer texto (simplificado)
        text = response.text
        
        # Generar ID
        import uuid
        doc_id = str(uuid.uuid4())
        
        return {
            "document_id": doc_id,
            "url": url,
            "text_length": len(text),
            "indexed": False
        }
```

**Tests**:
```python
# backend/tests/test_upload.py
def test_upload_pdf():
    with open("test.pdf", "rb") as f:
        response = client.post(
            "/upload/file",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["pages"] > 0

def test_upload_url():
    response = client.post("/upload/url", params={
        "url": "https://www.boe.es/buscar/doc.php?id=BOE-A-2015-11724"
    })
    assert response.status_code == 200
```

---

### Fase 2: Setup Frontend (Días 3-4)

#### Tarea 2.1: Crear Backend Service
**Archivo**: `services/backendService.ts`

```typescript
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatStreamResponse {
  delta: string;
  sources?: Array<{
    norma: string;
    articulo?: string;
    score: number;
  }>;
}

export class BackendService {
  /**
   * Envía un mensaje al chat con streaming
   */
  async *chatStream(
    message: string,
    conversationId: string,
    useRAG: boolean = true
  ): AsyncGenerator<ChatStreamResponse> {
    const response = await fetch(`${BACKEND_URL}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        use_rag: useRAG,
        top_k: 3,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') continue;

          try {
            const parsed = JSON.parse(data);
            
            // Si tiene sources, es el mensaje final
            if (parsed.sources) {
              yield { delta: '', sources: parsed.sources };
            } else if (parsed.choices?.[0]?.delta?.content) {
              yield { delta: parsed.choices[0].delta.content };
            }
          } catch (e) {
            console.error('Error parsing SSE:', e);
          }
        }
      }
    }
  }

  /**
   * Sube un archivo al backend
   */
  async uploadFile(file: File): Promise<{
    document_id: string;
    filename: string;
    text_length: number;
  }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${BACKEND_URL}/upload/file`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Descarga contenido de una URL
   */
  async uploadUrl(url: string): Promise<{
    document_id: string;
    url: string;
    text_length: number;
  }> {
    const response = await fetch(`${BACKEND_URL}/upload/url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      throw new Error(`URL fetch failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Health check del backend
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${BACKEND_URL}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

export const backendService = new BackendService();
```

---

#### Tarea 2.2: Crear Mistral Service
**Archivo**: `services/mistralService.ts`

```typescript
import { backendService, ChatStreamResponse } from './backendService';
import { ChatMessage } from '../types';

/**
 * Servicio para interactuar con Mistral a través del backend
 * Reemplaza geminiService.ts para el chat
 */
export class MistralService {
  /**
   * Envía un mensaje y recibe respuesta en streaming
   */
  async *sendMessageStream(
    message: string,
    conversationId: string,
    useRAG: boolean = true
  ): AsyncGenerator<string> {
    let fullResponse = '';
    let sources: any[] = [];

    for await (const chunk of backendService.chatStream(message, conversationId, useRAG)) {
      if (chunk.delta) {
        fullResponse += chunk.delta;
        yield chunk.delta;
      }
      if (chunk.sources) {
        sources = chunk.sources;
      }
    }

    // Agregar fuentes al final si existen
    if (sources.length > 0) {
      const sourcesText = '\n\n---\n**Fuentes consultadas:**\n' +
        sources.map(s => `- ${s.norma}${s.articulo ? ` (Art. ${s.articulo})` : ''}`).join('\n');
      
      yield sourcesText;
    }
  }

  /**
   * Procesa un archivo subido
   */
  async processFile(file: File): Promise<string> {
    const result = await backendService.uploadFile(file);
    return `Archivo "${result.filename}" procesado correctamente (${result.text_length} caracteres).`;
  }

  /**
   * Procesa una URL
   */
  async processUrl(url: string): Promise<string> {
    const result = await backendService.uploadUrl(url);
    return `Contenido de "${url}" descargado correctamente (${result.text_length} caracteres).`;
  }
}

export const mistralService = new MistralService();
```

---

#### Tarea 2.3: Modificar ChatView
**Archivo**: `components/ChatView.tsx`

```typescript
// Cambiar import
// import { getChatInstance } from '../services/geminiService';
import { mistralService } from '../services/mistralService';

// En handleSendMessage, reemplazar:
// const stream = await chat.sendMessageStream({ message: messageText });
// for await (const chunk of stream) { ... }

// Por:
for await (const chunk of mistralService.sendMessageStream(
  messageText,
  activeConvId,
  true // useRAG
)) {
  setConversations(prev =>
    prev.map(conv => {
      if (conv.id === activeConvId) {
        return {
          ...conv,
          messages: conv.messages.map(msg =>
            msg.id === modelResponseId 
              ? { ...msg, text: msg.text + chunk } 
              : msg
          ),
        };
      }
      return conv;
    })
  );
}
```

---

### Fase 3: Testing e Integración (Días 5-6)

#### Tarea 3.1: Tests Unitarios Backend
```bash
# backend/tests/test_integration.py
pytest backend/tests/test_chat.py -v
pytest backend/tests/test_upload.py -v
```

#### Tarea 3.2: Tests E2E Frontend
```typescript
// __tests__/chat-integration.test.tsx
describe('Chat Integration', () => {
  it('should connect to backend', async () => {
    const isHealthy = await backendService.healthCheck();
    expect(isHealthy).toBe(true);
  });

  it('should send message and receive response', async () => {
    const responses: string[] = [];
    
    for await (const chunk of mistralService.sendMessageStream(
      '¿Qué es la IT?',
      'test-123',
      true
    )) {
      responses.push(chunk);
    }
    
    expect(responses.length).toBeGreaterThan(0);
  });

  it('should upload file', async () => {
    const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
    const result = await mistralService.processFile(file);
    expect(result).toContain('procesado correctamente');
  });
});
```

---

### Fase 4: Documentación y Deploy (Días 7-8)

#### Tarea 4.1: Actualizar .env
```bash
# .env
VITE_BACKEND_URL=http://localhost:8000

# .env.production
VITE_BACKEND_URL=https://api.opositaia.com
```

#### Tarea 4.2: Documentación
**Archivo**: `docs/INTEGRACION_FRONTEND_BACKEND.md`

```markdown
# Integración Frontend-Backend

## Arquitectura

Frontend (React) → Backend (FastAPI) → Mistral + RAG

## Endpoints

### POST /chat/stream
Envía mensaje y recibe respuesta en streaming

### POST /upload/file
Sube archivo y extrae texto

### POST /upload/url
Descarga contenido de URL

## Uso en Frontend

```typescript
import { mistralService } from './services/mistralService';

// Enviar mensaje
for await (const chunk of mistralService.sendMessageStream(
  'pregunta',
  'conv-id',
  true
)) {
  console.log(chunk);
}
```

## Testing

```bash
# Backend
pytest backend/tests/

# Frontend
npm test
```
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

### Funcionales
- [ ] Usuario puede chatear usando Mistral en lugar de Gemini
- [ ] Respuestas incluyen contexto del RAG
- [ ] Archivos se procesan en servidor
- [ ] URLs se descargan en servidor
- [ ] Streaming funciona correctamente

### Técnicos
- [ ] Tests unitarios pasan (>80% coverage)
- [ ] Tests E2E pasan
- [ ] Latencia <3 segundos por respuesta
- [ ] Sin errores en consola
- [ ] Documentación actualizada

### No Funcionales
- [ ] Código sigue estándares del proyecto
- [ ] Commits en inglés
- [ ] Sin warnings de ESLint
- [ ] TypeScript sin errores

---

## 📊 MÉTRICAS DE ÉXITO

- **Performance**: <3s latencia promedio
- **Calidad**: Scores RAG >0.65
- **Cobertura**: >80% tests
- **Disponibilidad**: >99% uptime backend

---

## 🚨 RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Mistral VPS caído | Media | Alto | Fallback a Gemini |
| CORS issues | Alta | Medio | Configurar CORS correctamente |
| Streaming no funciona | Baja | Alto | Implementar polling como fallback |
| RAG lento | Media | Medio | Caché de búsquedas frecuentes |

---

## 📅 CRONOGRAMA

| Día | Tarea | Responsable |
|-----|-------|-------------|
| 1-2 | Backend routers | Backend Dev |
| 3-4 | Frontend services | Frontend Dev |
| 5-6 | Testing | QA + Devs |
| 7-8 | Docs + Deploy | DevOps |

---

## 🔗 DEPENDENCIAS

- ✅ Backend FastAPI operativo
- ✅ Qdrant con 7,833 chunks
- ✅ Mistral en VPS (147.93.95.67:8001)
- ⏸️ Frontend Vite corriendo

---

## 📝 NOTAS

- Mantener Gemini como fallback por si Mistral falla
- Implementar rate limiting en backend
- Considerar WebSockets para mejor performance
- Monitorear uso de Mistral vs Gemini

---

**Creado**: 2025-11-19  
**Sprint**: 7  
**Estimación**: 7-8 días  
**Prioridad**: CRÍTICA
