"""
Chat Router - Streaming chat with Mistral + RAG
Sprint 7 - Fase 1
Sprint 11 - Tracking PostgreSQL
"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from typing import AsyncGenerator, Optional
import httpx
import json
import logging
import os
import time
from datetime import datetime

# Import RAG Agent V2 and LLM Providers
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from agents.rag_agent_v2 import RAGAgentV2
from agents.llm_providers import get_provider, list_providers
from services.token_counter import token_counter
from services.usage_logger import usage_logger
from database.db import db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# Configuration
# Mistral directo (puerto 8080) - Nginx tiene problema con proxy /v1/
MISTRAL_URL = os.getenv("MISTRAL_URL", "http://localhost:8080")
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
    user_id: Optional[str] = None  # Sprint 11: Para tracking


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
async def chat_stream(request: ChatRequest, raw_request: Request):
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
        start_time = time.time()
        input_messages = []
        output_accumulator = []
        
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
                input_messages = messages
                
                async for content in provider.generate_stream(messages, temperature=0.7, max_tokens=2000):
                    # Enviar en formato SSE compatible con frontend
                    chunk_data = {
                        "choices": [{
                            "delta": {"content": content}
                        }]
                    }
                    yield f"data: {json.dumps(chunk_data)}\n\n"
                    output_accumulator.append(content)
                
            except Exception as e:
                error_msg = f"Provider {request.provider} error: {str(e)}"
                logger.error(error_msg)
                yield f"data: {json.dumps({'error': error_msg})}\n\n"
                return
            
            # 4. Enviar fuentes al final
            if sources:
                yield f"data: {json.dumps({'sources': sources})}\n\n"
            
            # 5. Tracking tokens y costos
            try:
                input_tokens = token_counter.count_messages_tokens([
                    {"role": m["role"], "content": m["content"]} for m in input_messages
                ])
                output_text = "".join(output_accumulator)
                output_tokens = token_counter.count_tokens(output_text)
                usage = token_counter.calculate_cost(request.provider, input_tokens, output_tokens)

                duration_ms = int((time.time() - start_time) * 1000)
                usage_logger.log({
                    'user_id': request.user_id or 'anonymous',
                    'session_id': raw_request.headers.get('X-Session-ID', 'no-session'),
                    'provider_id': request.provider,
                    'model_name': provider.get_info().get('model'),
                    'input_tokens': usage['input_tokens'],
                    'output_tokens': usage['output_tokens'],
                    'total_tokens': usage['total_tokens'],
                    'input_cost_eur': usage['input_cost_eur'],
                    'output_cost_eur': usage['output_cost_eur'],
                    'total_cost_eur': usage['total_cost_eur'],
                    'endpoint': '/chat/stream',
                    'request_type': 'chat',
                    'request_duration_ms': duration_ms,
                    'success': True
                })
                # Enviar línea final con metadata de uso
                usage_chunk = {
                    'usage': {
                        'total_tokens': usage['total_tokens'],
                        'total_cost_eur': usage['total_cost_eur']
                    }
                }
                yield f"data: {json.dumps(usage_chunk)}\n\n"
            except Exception as te:
                logger.error(f"Usage tracking failed: {te}")

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

@router.get("/usage/summary")
async def usage_summary():
    """Resumen agregado de uso (file fallback si DB no disponible)."""
    return usage_logger.summary()


@router.get("/usage/export")
async def usage_export(
    from_ts: Optional[str] = None,
    to_ts: Optional[str] = None,
    user_id: Optional[str] = None,
    provider: Optional[str] = None,
):
    """
    Exporta el uso como CSV desde la tabla `usage_logs`.
    Filtros opcionales: `from_ts`, `to_ts` (ISO-8601), `user_id`, `provider`.
    Si la base de datos no está disponible, hace fallback a los logs JSONL.
    """

    def parse_dt(s: Optional[str]) -> Optional[datetime]:
        if not s:
            return None
        try:
            return datetime.fromisoformat(s)
        except Exception:
            return None

    from_dt = parse_dt(from_ts)
    to_dt = parse_dt(to_ts)

    async def generate_csv_db():
        # Cabecera CSV
        headers = [
            "created_at","user_id","session_id","provider_id","model_name",
            "input_tokens","output_tokens","total_tokens",
            "input_cost_eur","output_cost_eur","total_cost_eur",
            "endpoint","request_type","request_duration_ms","success","error_message",
        ]
        yield ",".join(headers) + "\n"

        where = []
        params = []
        if from_dt is not None:
            where.append("created_at >= %s")
            params.append(from_dt)
        if to_dt is not None:
            where.append("created_at <= %s")
            params.append(to_dt)
        if user_id:
            where.append("user_id = %s")
            params.append(user_id)
        if provider:
            where.append("provider_id = %s")
            params.append(provider)
        where_sql = (" WHERE " + " AND ".join(where)) if where else ""

        query = f"""
            SELECT created_at, user_id, session_id, provider_id, model_name,
                   input_tokens, output_tokens, total_tokens,
                   input_cost_eur, output_cost_eur, total_cost_eur,
                   endpoint, request_type, request_duration_ms, success, error_message
            FROM usage_logs
            {where_sql}
            ORDER BY created_at DESC
        """

        with db.get_cursor() as cur:
            cur.execute(query, params)
            for row in cur.fetchall():
                # Convertir a strings y escapar comas/barras
                out = []
                for val in row:
                    if val is None:
                        out.append("")
                    else:
                        s = str(val)
                        if ',' in s or '\n' in s or '"' in s:
                            s = '"' + s.replace('"', '""') + '"'
                        out.append(s)
                yield ",".join(out) + "\n"

    async def generate_csv_file():
        # Fallback leyendo el JSONL del usage_logger
        headers = [
            "created_at","user_id","session_id","provider_id","model_name",
            "input_tokens","output_tokens","total_tokens",
            "input_cost_eur","output_cost_eur","total_cost_eur",
            "endpoint","request_type","request_duration_ms","success","error_message",
        ]
        yield ",".join(headers) + "\n"

        try:
            # Acceder al path del JSONL del usage_logger
            log_path = getattr(usage_logger, 'log_path', None)
            if not log_path or not os.path.exists(log_path):
                return
            with open(log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Filtros básicos
                    created_at = rec.get('created_at')
                    # El fallback de archivo no garantiza created_at; saltar filtro temporal si no existe
                    if from_dt and created_at:
                        try:
                            cdt = datetime.fromisoformat(created_at)
                            if cdt < from_dt:
                                continue
                        except Exception:
                            pass
                    if to_dt and created_at:
                        try:
                            cdt = datetime.fromisoformat(created_at)
                            if cdt > to_dt:
                                continue
                        except Exception:
                            pass
                    if user_id and rec.get('user_id') != user_id:
                        continue
                    if provider and rec.get('provider_id') != provider:
                        continue

                    row = [
                        rec.get('created_at', ''),
                        rec.get('user_id', ''),
                        rec.get('session_id', ''),
                        rec.get('provider_id', ''),
                        rec.get('model_name', ''),
                        rec.get('input_tokens', 0),
                        rec.get('output_tokens', 0),
                        rec.get('total_tokens', 0),
                        rec.get('input_cost_eur', 0.0),
                        rec.get('output_cost_eur', 0.0),
                        rec.get('total_cost_eur', 0.0),
                        rec.get('endpoint', ''),
                        rec.get('request_type', ''),
                        rec.get('request_duration_ms', ''),
                        rec.get('success', ''),
                        rec.get('error_message', ''),
                    ]
                    out = []
                    for val in row:
                        s = str(val) if val is not None else ""
                        if ',' in s or '\n' in s or '"' in s:
                            s = '"' + s.replace('"', '""') + '"'
                        out.append(s)
                    yield ",".join(out) + "\n"
        except Exception as e:
            logger.error(f"Failed to export from file fallback: {e}")

    # Intentar DB; si falla, fallback a archivo
    try:
        gen = generate_csv_db()
        return StreamingResponse(
            gen,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=usage_export.csv"
            }
        )
    except Exception as e:
        logger.warning(f"DB export failed, using file fallback: {e}")
        gen = generate_csv_file()
        return StreamingResponse(
            gen,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=usage_export.csv"
            }
        )


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
