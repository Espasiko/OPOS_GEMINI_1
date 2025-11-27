"""
RAG API Endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import logging

from agents import get_rag_agent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/rag", tags=["RAG"])


# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class RAGSearchRequest(BaseModel):
    """Request model for RAG search"""
    query: str = Field(..., min_length=3, max_length=1000, description="User query")
    top_k: int = Field(5, ge=1, le=20, description="Number of results")
    min_score: float = Field(0.7, ge=0.0, le=1.0, description="Minimum similarity score")
    tema_filter: Optional[int] = Field(None, description="Filter by topic ID")


class DocumentResult(BaseModel):
    """Single document result"""
    id: str
    score: float
    content: str
    metadata: Dict


class RAGSearchResponse(BaseModel):
    """Response model for RAG search"""
    query: str
    documents: List[DocumentResult]
    context: str
    metadata: Dict


class CollectionStatsResponse(BaseModel):
    """Collection statistics"""
    collection_name: str
    total_documents: int = 0
    vector_size: int = 0
    distance: str = ""
    status: str


# ============================================
# ENDPOINTS
# ============================================

@router.post("/search", response_model=RAGSearchResponse)
async def search_documents(request: RAGSearchRequest):
    """
    Busca documentos relevantes en el BOE usando RAG
    
    **Ejemplo de uso:**
    ```json
    {
        "query": "¿Qué es la incapacidad temporal?",
        "top_k": 5,
        "min_score": 0.7,
        "tema_filter": 3
    }
    ```
    
    **Respuesta:**
    - `documents`: Lista de documentos encontrados con score
    - `context`: Contexto formateado para LLM
    - `metadata`: Información sobre la búsqueda
    """
    try:
        rag_agent = get_rag_agent()
        
        result = await rag_agent.search_and_answer(
            query=request.query,
            top_k=request.top_k,
            min_score=request.min_score,
            tema_filter=request.tema_filter
        )
        
        return result
        
    except Exception as e:
        logger.error(f"RAG search error: {e}")
        raise HTTPException(status_code=500, detail=f"RAG search failed: {str(e)}")


@router.get("/stats", response_model=CollectionStatsResponse)
async def get_collection_stats():
    """
    Obtiene estadísticas de la colección Qdrant
    
    **Respuesta:**
    - `total_documents`: Número de documentos indexados
    - `vector_size`: Dimensión de los embeddings
    - `status`: Estado de la colección
    """
    try:
        rag_agent = get_rag_agent()
        stats = await rag_agent.get_collection_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check del servicio RAG
    """
    try:
        rag_agent = get_rag_agent()
        stats = await rag_agent.get_collection_stats()
        
        return {
            "status": "healthy" if stats.get("status") == "healthy" else "unhealthy",
            "embedding_model": rag_agent.embedding_model,
            "qdrant_url": rag_agent.qdrant_url,
            "collection": stats.get("collection_name"),
            "documents": stats.get("total_documents", 0)
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.post("/test")
async def test_rag():
    """
    Endpoint de prueba rápida del RAG
    
    Busca "incapacidad temporal" como ejemplo
    """
    try:
        rag_agent = get_rag_agent()
        
        result = await rag_agent.search_and_answer(
            query="¿Qué es la incapacidad temporal?",
            top_k=3,
            min_score=0.5
        )
        
        return {
            "status": "success",
            "test_query": "¿Qué es la incapacidad temporal?",
            "documents_found": len(result["documents"]),
            "top_score": result["metadata"]["top_score"],
            "search_time_ms": result["metadata"]["search_time_ms"],
            "sample_document": result["documents"][0] if result["documents"] else None
        }
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")
