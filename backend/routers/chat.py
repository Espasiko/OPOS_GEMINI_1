"""
Chat Router - Streaming chat with Mistral + RAG
Sprint 7 - Fase 1
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator, Optional
import httpx
import json
import logging
import os

# Import RAG Agent V2 and LLM Providers
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from agents.rag_agent_v2 import RAGAgentV2
from agents.llm_providers import get_provider, list_providers

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# Configuration
# Mistral directo (puerto 8080) - Nginx tiene problema con proxy /v1/
MISTRAL_URL = os.getenv("MISTRAL_URL", "http://147.93.95.67:8080")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral")

# Global RAG Agent instance (lazy loaded)
_rag_agent: Optional[RAGAgentV2] = None

def get_rag_agent() -> RAGAgentV2:
    """Get or create RAG Agent instance (singleton pattern)"""
    global _rag_agent
    if _rag_agent is None:
        logger.info("Initializing RAG Agent (first time)")
        _rag_agent = RAGAgentV2()
    return _rag_agent


class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    use_rag: bool = True
    provider: str = 'groq-8b'  # ID del proveedor
    top_k: int = 3
    min_score: float = 0.5


class ChatResponse(BaseModel):
    response: str
    sources: list[dict] = []
    conversation_id: str


class Source(BaseModel):
    norma: str
    articulo: Optional[str] = None
    score: float
    content_preview: str


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Chat con streaming usando Mistral + RAG
    
    Flujo:
    1. Consultar RAG si use_rag=True
    2. Construir prompt con contexto
    3. Llamar a Mistral con streaming
    4. Enviar fuentes al final
    """
    async def generate() -> AsyncGenerator[str, None]:
        context = ""
        sources = []
        
        try:
            # 1. Consultar RAG si use_rag=True
            if request.use_rag:
                logger.info(f"Querying RAG for: {request.message[:50]}...")
                
                try:
                    rag = get_rag_agent()
                    
                    # Buscar más documentos para poder reranquear
                    results = await rag.search_documents(
                        query=request.message,
                        top_k=request.top_k * 3,  # Buscar 3x más para reranquear
                        min_score=request.min_score,
                        layer_filter=None  # Buscar en todas las capas
                    )
                    
                    # Reranking por jerarquía: Capa 1 (leyes) > Capa 2 (jurisprudencia) > Capa 3 (materiales)
                    def get_hierarchy_boost(metadata):
                        capa = metadata.get('capa', 3)
                        if capa == 1:
                            return 0.3  # Boost +30% para leyes
                        elif capa == 2:
                            return 0.15  # Boost +15% para jurisprudencia
                        else:
                            return 0.0  # Sin boost para materiales
                    
                    # Aplicar boost y reordenar
                    for r in results:
                        boost = get_hierarchy_boost(r['metadata'])
                        r['original_score'] = r['score']
                        r['score'] = r['score'] * (1 + boost)
                    
                    # Reordenar por score boosted y tomar top_k
                    results = sorted(results, key=lambda x: x['score'], reverse=True)[:request.top_k]
                    
                    # Construir contexto
                    if results:
                        context_parts = []
                        for r in results:
                            norma = r['metadata'].get('norma_completa', r['metadata'].get('material_nombre', 'Documento'))
                            articulo = r['metadata'].get('articulo')
                            content = r['content'][:500]  # Limitar a 500 chars
                            
                            if articulo:
                                context_parts.append(f"[{norma} - Art. {articulo}]\n{content}")
                            else:
                                context_parts.append(f"[{norma}]\n{content}")
                        
                        context = "\n\n---\n\n".join(context_parts)
                        
                        # Preparar fuentes para enviar al final
                        sources = [
                            {
                                "norma": r['metadata'].get('norma_completa', r['metadata'].get('material_nombre', 'Documento')),
                                "articulo": r['metadata'].get('articulo'),
                                "score": round(r['score'], 3),
                                "content_preview": r['content'][:200]
                            }
                            for r in results
                        ]
                        
                        logger.info(f"RAG found {len(sources)} relevant documents")
                    else:
                        logger.warning("RAG returned no results")
                        
                except Exception as e:
                    logger.error(f"RAG query failed: {e}")
                    # Continuar sin RAG
                    yield f"data: {json.dumps({'error': 'RAG query failed, continuing without context'})}\n\n"
            
            # 2. Construir prompt con contexto
            system_prompt = """Eres un experto tutor en legislación de Seguridad Social española.
Tu objetivo es ayudar a opositores a preparar el examen C1 de Seguridad Social.

INSTRUCCIONES IMPORTANTES:
1. SIEMPRE cita los artículos específicos de las leyes cuando respondas (ej: "Según el artículo 195 del TRLGSS...")
2. Prioriza información de leyes oficiales sobre materiales de estudio
3. Explica paso a paso los conceptos complejos
4. Usa ejemplos prácticos cuando sea apropiado
5. Responde siempre en español
6. Si no estás seguro, indícalo claramente

FORMATO DE RESPUESTA:
- Comienza citando el artículo relevante
- Explica el concepto claramente
- Proporciona ejemplos si es necesario
- Mantén un tono profesional pero cercano

Ejemplo: "Según el artículo 195 del TRLGSS, la incapacidad temporal es..."

Mantén un tono profesional pero cercano, como un tutor experimentado."""
            
            user_prompt = request.message
            if context:
                user_prompt = f"""Contexto legal relevante (prioriza las leyes sobre los materiales de estudio):

{context}

---

Pregunta del usuario: {request.message}

IMPORTANTE: Responde basándote PRINCIPALMENTE en las leyes oficiales del contexto. Cita los artículos específicos (ej: "artículo 195 del TRLGSS"). Si usas información de materiales de estudio, indícalo claramente."""
            
            # 3. Llamar al proveedor seleccionado con streaming
            try:
                provider = get_provider(request.provider)
                logger.info(f"Using provider: {request.provider} - {provider.get_info()}")
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                
                async for content in provider.generate_stream(messages, temperature=0.7, max_tokens=2000):
                    # Enviar en formato SSE compatible con frontend
                    chunk_data = {
                        "choices": [{
                            "delta": {"content": content}
                        }]
                    }
                    yield f"data: {json.dumps(chunk_data)}\n\n"
                
            except Exception as e:
                error_msg = f"Provider {request.provider} error: {str(e)}"
                logger.error(error_msg)
                yield f"data: {json.dumps({'error': error_msg})}\n\n"
                return
            
            # 4. Enviar fuentes al final
            if sources:
                yield f"data: {json.dumps({'sources': sources})}\n\n"
            
            # Señal de finalización
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            logger.error(f"Chat stream error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    Chat sin streaming (para compatibilidad)
    Acumula toda la respuesta antes de devolverla
    """
    full_response = ""
    sources = []
    
    try:
        # Consultar RAG
        if request.use_rag:
            rag = RAGAgentV2()
            results = await rag.search_documents(
                query=request.message,
                top_k=request.top_k,
                min_score=request.min_score
            )
            
            if results:
                sources = [
                    {
                        "norma": r['metadata'].get('norma_completa', r['metadata'].get('material_nombre', 'Documento')),
                        "articulo": r['metadata'].get('articulo'),
                        "score": round(r['score'], 3),
                        "content_preview": r['content'][:200]
                    }
                    for r in results
                ]
        
        # Construir prompt
        system_prompt = """Eres un experto tutor en legislación de Seguridad Social española."""
        
        context = ""
        if sources:
            context_parts = []
            for s in sources:
                if s['articulo']:
                    context_parts.append(f"[{s['norma']} - Art. {s['articulo']}]\n{s['content_preview']}")
                else:
                    context_parts.append(f"[{s['norma']}]\n{s['content_preview']}")
            context = "\n\n---\n\n".join(context_parts)
        
        user_prompt = request.message
        if context:
            user_prompt = f"Contexto:\n{context}\n\nPregunta: {request.message}"
        
        # Llamar a Mistral sin streaming
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{MISTRAL_URL}/v1/chat/completions",
                json={
                    "model": MISTRAL_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "stream": False,
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Mistral API error: {response.text}"
                )
            
            data = response.json()
            full_response = data['choices'][0]['message']['content']
        
        return ChatResponse(
            response=full_response,
            sources=sources,
            conversation_id=request.conversation_id
        )
        
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Mistral server"
        )
    except Exception as e:
        logger.error(f"Chat message error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers")
async def get_providers():
    """
    Lista todos los proveedores de LLM disponibles
    """
    return {
        "providers": list_providers()
    }


@router.get("/health")
async def chat_health():
    """
    Health check del servicio de chat
    """
    try:
        # Verificar conexión con Mistral (llama.cpp server)
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Usar endpoint correcto de llama.cpp
            response = await client.get(f"{MISTRAL_URL}/v1/models")
            mistral_healthy = response.status_code == 200
            logger.info(f"Mistral health check: {response.status_code}")
    except Exception as e:
        logger.error(f"Mistral health check failed: {e}")
        mistral_healthy = False
    
    # Verificar RAG (solo check rápido, no cargar modelo)
    try:
        # Solo verificar que Qdrant está disponible
        async with httpx.AsyncClient(timeout=5.0) as client:
            qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
            response = await client.get(qdrant_url)
            rag_healthy = response.status_code == 200
    except:
        rag_healthy = False
    
    return {
        "status": "healthy" if (mistral_healthy and rag_healthy) else "degraded",
        "mistral": "up" if mistral_healthy else "down",
        "rag": "up" if rag_healthy else "down",
        "mistral_url": MISTRAL_URL,
        "model": MISTRAL_MODEL
    }
