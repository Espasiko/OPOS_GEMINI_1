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
import httpx

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


# ============================================================================
# OBSIDIAN VAULT BRIDGE (via Local REST API plugin, puerto 27124)
# Permite leer, buscar y escribir notas en la Bóveda de Obsidian
# ============================================================================

import subprocess as _sp

def _get_obsidian_url() -> str:
    """
    Detecta automáticamente la URL del Local REST API de Obsidian.
    Si hay una URL fija en el .env, la usa. Si no, detecta la IP del
    host Windows (necesaria en WSL2 sin mirrored networking).
    """
    # 1. Si hay URL explícita en .env, usarla
    env_url = os.getenv("OBSIDIAN_REST_URL", "")
    if env_url and "localhost" not in env_url:
        return env_url

    port = 27123  # HTTP plano (sin certificado autofirmado)

    # 2. Intentar localhost primero (funciona con mirrored networking o Windows nativo)
    # Lo detectaremos en runtime, no aquí — devolvemos candidatos ordenados
    try:
        result = _sp.run(
            ["ip", "route", "show", "default"],
            capture_output=True, text=True, timeout=3
        )
        # Línea tipo: "default via 172.26.240.1 dev eth0"
        for line in result.stdout.splitlines():
            if "default via" in line:
                windows_ip = line.split("via")[1].strip().split()[0]
                logger.info(f"[Obsidian] IP Windows detectada automáticamente: {windows_ip}")
                return f"http://{windows_ip}:{port}"
    except Exception as e:
        logger.warning(f"[Obsidian] No se pudo detectar IP Windows: {e}")

    # 3. Fallback a localhost (por si mirrored networking está activo)
    return f"http://localhost:{port}"

OBSIDIAN_KEY = os.getenv("OBSIDIAN_REST_API_KEY", "")

def _obsidian_headers():
    return {"Authorization": f"Bearer {OBSIDIAN_KEY}"}

def _obsidian_url() -> str:
    """Retorna la URL de Obsidian, detectándola si hace falta."""
    return _get_obsidian_url()

class VaultSearchRequest(BaseModel):
    query: str
    limit: int = 10

class VaultReadRequest(BaseModel):
    path: str  # Ruta relativa dentro del vault, ej: "00_Agentes/ExaminadorLegal.md"

class VaultWriteRequest(BaseModel):
    path: str
    content: str
    mode: str = "append"  # "append" o "overwrite"

@router.post("/vault/search")
async def vault_search(request: VaultSearchRequest):
    """
    Busca notas en la Bóveda de Obsidian por texto.
    Requiere que Obsidian esté abierto con el plugin 'Local REST API' activo.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{_obsidian_url()}/search/simple/",
                params={"query": request.query, "contextLength": 200},
                headers=_obsidian_headers()
            )
            resp.raise_for_status()
            results = resp.json()
            # Limitar resultados y formatear
            limited = results[:request.limit]
            return {
                "status": "ok",
                "query": request.query,
                "total": len(results),
                "results": [
                    {
                        "filename": r.get("filename", ""),
                        "score": r.get("score", 0),
                        "matches": r.get("matches", [])
                    }
                    for r in limited
                ]
            }
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Obsidian no está abierto o el plugin Local REST API no está activo.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar en vault: {str(e)}")


@router.get("/vault/read")
async def vault_read(path: str):
    """
    Lee el contenido de una nota específica de la Bóveda.
    Ejemplo: /mcp/vault/read?path=00_Agentes/ExaminadorLegal.md
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{_obsidian_url()}/vault/{path}",
                headers=_obsidian_headers()
            )
            resp.raise_for_status()
            return {
                "status": "ok",
                "path": path,
                "content": resp.text
            }
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Obsidian no está abierto o el plugin Local REST API no está activo.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Nota no encontrada: {path}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vault/write")
async def vault_write(request: VaultWriteRequest):
    """
    Escribe o añade contenido a una nota de la Bóveda.
    mode='overwrite' reemplaza el contenido. mode='append' lo añade al final.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            method = client.put if request.mode == "overwrite" else client.post
            resp = await method(
                f"{_obsidian_url()}/vault/{request.path}",
                content=request.content.encode("utf-8"),
                headers={**_obsidian_headers(), "Content-Type": "text/markdown"},
            )
            resp.raise_for_status()
            return {
                "status": "ok",
                "path": request.path,
                "mode": request.mode,
                "message": f"Nota {'actualizada' if request.mode == 'overwrite' else 'actualizada (append)'} correctamente."
            }
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Obsidian no está abierto o el plugin Local REST API no está activo.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al escribir en vault: {str(e)}")


@router.get("/vault/health")
async def vault_health():
    """Verifica que el puente con Obsidian funciona correctamente."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                f"{_obsidian_url()}/",
                headers=_obsidian_headers()
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "status": "ok",
                "obsidian_connected": True,
                "vault": data.get("vault", "desconocido"),
                "api_version": data.get("apiVersion", "?"),
                "tools": ["vault_search", "vault_read", "vault_write"]
            }
    except httpx.ConnectError:
        return {
            "status": "error",
            "obsidian_connected": False,
            "message": "Obsidian está cerrado o el plugin Local REST API no está activo."
        }
    except Exception as e:
        return {"status": "error", "obsidian_connected": False, "message": str(e)}