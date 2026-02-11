"""
MCP Client - Python interface to MCP HTTP wrapper
"""

import requests
from typing import List, Dict, Any

MCP_BASE_URL = "http://127.0.0.1:3100"

def search_rag(query: str, limit: int = 5, score_threshold: float = 0.7) -> List[Dict[str, Any]]:
    """
    Search for legal context using RAG (Qdrant Cloud via MCP)
    
    Args:
        query: Search query text
        limit: Maximum number of results
        score_threshold: Minimum relevance score (0-1)
    
    Returns:
        List of results with law_name, article_id, content, score
    """
    try:
        response = requests.post(
            f"{MCP_BASE_URL}/tools/search_rag",
            json={
                "query": query,
                "limit": limit,
                "score_threshold": score_threshold
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "ok":
            return data.get("results", [])
        else:
            print(f"MCP Error: {data.get('error', 'Unknown error')}")
            return []
            
    except requests.exceptions.ConnectionError:
        print("MCP server not running on port 3100")
        return []
    except requests.exceptions.Timeout:
        print("MCP request timed out")
        return []
    except Exception as e:
        print(f"MCP client error: {e}")
        return []

def format_context(results: List[Dict[str, Any]]) -> str:
    """
    Format RAG results into context string for LLM
    
    Args:
        results: List of RAG search results
    
    Returns:
        Formatted context string
    """
    if not results:
        return ""
    
    context = ""
    for r in results:
        law_name = r.get("law_name", "Desconocida")
        article_id = r.get("article_id", "")
        content = r.get("content", "")
        score = r.get("score", 0)
        
        context += f"-- FUENTE: {law_name} | {article_id} (relevancia: {score:.2f}) --\n"
        context += f"{content}\n\n"
    
    return context

def health_check() -> bool:
    """Check if MCP server is running"""
    try:
        response = requests.get(f"{MCP_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False
