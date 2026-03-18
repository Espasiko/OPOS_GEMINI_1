"""
MCP Gateway Router - Exponer MCP como REST API
Para que otras IAs puedan acceder al RAG sin MCP directo
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import subprocess
import json
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mcp", tags=["mcp-gateway"])

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class SearchRAGRequest(BaseModel):
    query: str
    limit: int = 5
    score_threshold: float = 0.7

class VerifyBOERequest(BaseModel):
    ley_id: str
    articulo: Optional[str] = None

class SearchJurisprudenceRequest(BaseModel):
    query: str
    tribunal: str = "todos"  # TS, TSJ, todos
    limit: int = 3

class GetLawSummaryRequest(BaseModel):
    ley_name: str

class IngestNewLawRequest(BaseModel):
    boe_id: str

# ============================================================================
# MCP CLIENT WRAPPER
# ============================================================================

class MCPClient:
    """Wrapper para llamar al MCP server desde FastAPI"""
    
    def __init__(self):
        # Usar path absoluto desde la raíz del proyecto
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.mcp_path = os.path.join(project_root, "mcp-server/dist/index.js")
        self.node_path = "node"
        
        # Verificar que el archivo existe
        if not os.path.exists(self.mcp_path):
            logger.error(f"MCP server not found at: {self.mcp_path}")
            raise FileNotFoundError(f"MCP server not found at: {self.mcp_path}")
        
        logger.info(f"MCP Client initialized with path: {self.mcp_path}")
    
    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Llamar a una herramienta del MCP server"""
        try:
            # Preparar comando
            cmd = [
                self.node_path,
                self.mcp_path,
                "call-tool",
                tool_name,
                json.dumps(arguments)
            ]
            
            # Ejecutar
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                env={
                    **os.environ,
                    "QDRANT_URL": os.getenv("QDRANT_URL"),
                    "QDRANT_API_KEY": os.getenv("QDRANT_API_KEY"),
                    "HUGGINGFACE_TOKEN": os.getenv("HUGGINGFACE_TOKEN"),
                    "MISTRAL_API_KEY": os.getenv("MISTRAL_API_KEY")
                }
            )
            
            if result.returncode != 0:
                logger.error(f"MCP error: {result.stderr}")
                raise Exception(f"MCP call failed: {result.stderr}")
            
            return json.loads(result.stdout)
            
        except subprocess.TimeoutExpired:
            raise Exception("MCP call timed out")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}, stdout: {result.stdout}")
            raise Exception("Invalid JSON response from MCP")
        except Exception as e:
            logger.error(f"MCP call error: {e}")
            raise Exception(f"MCP call failed: {str(e)}")

# Global MCP client (Lazy)
_mcp_client = None

def get_mcp_client():
    """Retorna la instancia global del cliente MCP, creándola si es necesario."""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/search_rag")
async def search_rag(request: SearchRAGRequest):
    """Buscar en el RAG usando MCP"""
    try:
        result = await get_mcp_client().call_tool("mcp_opositaia_search_rag", {
            "query": request.query,
            "limit": request.limit,
            "score_threshold": request.score_threshold
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/collections")
async def list_collections():
    """Listar colecciones Qdrant"""
    try:
        result = await get_mcp_client().call_tool("mcp_opositaia_list_collections", {})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify_boe")
async def verify_boe(request: VerifyBOERequest):
    """Verificar vigencia de ley en BOE"""
    try:
        args = {"ley_id": request.ley_id}
        if request.articulo:
            args["articulo"] = request.articulo
            
        result = await get_mcp_client().call_tool("mcp_opositaia_verify_boe", args)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search_jurisprudence")
async def search_jurisprudence(request: SearchJurisprudenceRequest):
    """Buscar jurisprudencia"""
    try:
        result = await get_mcp_client().call_tool("mcp_opositaia_search_jurisprudence", {
            "query": request.query,
            "tribunal": request.tribunal,
            "limit": request.limit
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get_law_summary")
async def get_law_summary(request: GetLawSummaryRequest):
    """Obtener resumen de ley"""
    try:
        result = await get_mcp_client().call_tool("mcp_opositaia_get_law_summary", {
            "ley_name": request.ley_name
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest_new_law")
async def ingest_new_law(request: IngestNewLawRequest):
    """Ingestar nueva ley del BOE"""
    try:
        result = await get_mcp_client().call_tool("mcp_opositaia_ingest_new_law", {
            "boe_id": request.boe_id
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def mcp_health():
    """Health check del MCP gateway"""
    try:
        # Test básico - listar colecciones
        result = await get_mcp_client().call_tool("mcp_opositaia_list_collections", {})
        return {
            "status": "healthy",
            "mcp_server": "connected",
            "collections": len(result.get("collections", [])),
            "tools_available": [
                "search_rag",
                "list_collections", 
                "verify_boe",
                "search_jurisprudence",
                "get_law_summary",
                "ingest_new_law"
            ]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "mcp_server": "disconnected"
        }

# ============================================================================
# WEBHOOK PARA OTRAS IAS
# ============================================================================

@router.post("/webhook/search")
async def webhook_search(request: dict):
    """
    Webhook genérico para otras IAs
    Soporta diferentes formatos de salida
    """
    try:
        query = request.get("query", "")
        format_type = request.get("format", "json")
        limit = request.get("limit", 5)
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Buscar en RAG
        result = await get_mcp_client().call_tool("mcp_opositaia_search_rag", {
            "query": query,
            "limit": limit
        })
        
        # Formatear según el tipo solicitado
        if format_type == "claude":
            return format_for_claude(result)
        elif format_type == "openai":
            return format_for_openai(result)
        elif format_type == "mistral":
            return format_for_mistral(result)
        else:
            return result
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def format_for_claude(result: dict) -> dict:
    """Formatear respuesta para Claude"""
    return {
        "type": "search_results",
        "results": [
            {
                "title": item.get("title", "Documento legal"),
                "content": item.get("content", ""),
                "score": item.get("score", 0),
                "source": item.get("source", "")
            }
            for item in result.get("results", [])
        ]
    }

def format_for_openai(result: dict) -> dict:
    """Formatear respuesta para OpenAI"""
    return {
        "data": result.get("results", []),
        "metadata": {
            "total_results": len(result.get("results", [])),
            "query_time": result.get("query_time", 0)
        }
    }

def format_for_mistral(result: dict) -> dict:
    """Formatear respuesta para Mistral"""
    return {
        "search_results": result.get("results", []),
        "context": "\n\n".join([
            f"[{item.get('title', 'Doc')}] {item.get('content', '')[:500]}"
            for item in result.get("results", [])
        ])
    }