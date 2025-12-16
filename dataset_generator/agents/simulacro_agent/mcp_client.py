"""
Cliente MCP para OpositaIA
Conecta con el servidor MCP de opositaia para consultar el RAG de Qdrant
"""

import os
import json
import subprocess
from typing import Optional, List, Dict, Any
from pathlib import Path

class MCPClient:
    """Cliente para interactuar con el MCP de OpositaIA"""
    
    def __init__(self):
        self.mcp_path = Path(__file__).parent.parent.parent.parent / "mcp-server"
        self._load_env()
    
    def _load_env(self):
        """Cargar variables de entorno del MCP"""
        env_file = self.mcp_path / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value
    
    def search_rag(self, query: str, limit: int = 5, score_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Buscar en el RAG de Qdrant usando el MCP
        
        Args:
            query: Pregunta o término a buscar
            limit: Número máximo de resultados
            score_threshold: Umbral mínimo de similitud
            
        Returns:
            Resultados de la búsqueda
        """
        # Por ahora, implementación directa con Qdrant
        # En producción, esto llamaría al MCP server
        try:
            from qdrant_client import QdrantClient
            import requests
            
            qdrant_url = os.getenv("QDRANT_URL", "")
            qdrant_key = os.getenv("QDRANT_API_KEY", "")
            hf_token = os.getenv("HUGGINGFACE_TOKEN", os.getenv("HF_TOKEN", ""))
            
            if not all([qdrant_url, qdrant_key, hf_token]):
                return {"error": "Faltan variables de entorno", "results": []}
            
            # Generar embedding con pablosi
            embedding = self._generate_embedding(query, hf_token)
            if not embedding:
                return {"error": "Error generando embedding", "results": []}
            
            # Buscar en Qdrant
            client = QdrantClient(url=qdrant_url, api_key=qdrant_key)
            
            results = client.search(
                collection_name="opositaia_knowledge",
                query_vector=embedding,
                limit=limit,
                score_threshold=score_threshold
            )
            
            return {
                "query": query,
                "results": [
                    {
                        "score": r.score,
                        "content": r.payload.get("content", r.payload.get("text", "")),
                        "metadata": {k: v for k, v in r.payload.items() if k not in ["content", "text"]}
                    }
                    for r in results
                ]
            }
            
        except Exception as e:
            return {"error": str(e), "results": []}
    
    def _generate_embedding(self, text: str, hf_token: str) -> Optional[List[float]]:
        """Generar embedding usando pablosi/bge-m3-spa-law-qa-trained-2"""
        try:
            import requests
            
            url = "https://api-inference.huggingface.co/pipeline/feature-extraction/pablosi/bge-m3-spa-law-qa-trained-2"
            headers = {"Authorization": f"Bearer {hf_token}"}
            
            response = requests.post(url, headers=headers, json={"inputs": text})
            
            if response.status_code == 200:
                embedding = response.json()
                if isinstance(embedding, list) and len(embedding) > 0:
                    if isinstance(embedding[0], list):
                        return embedding[0]
                    return embedding
            return None
            
        except Exception as e:
            print(f"Error generando embedding: {e}")
            return None
    
    def list_collections(self) -> Dict[str, Any]:
        """Listar colecciones disponibles en Qdrant"""
        try:
            from qdrant_client import QdrantClient
            
            qdrant_url = os.getenv("QDRANT_URL", "")
            qdrant_key = os.getenv("QDRANT_API_KEY", "")
            
            client = QdrantClient(url=qdrant_url, api_key=qdrant_key)
            collections = client.get_collections()
            
            result = []
            for col in collections.collections:
                info = client.get_collection(col.name)
                result.append({
                    "name": col.name,
                    "points_count": info.points_count,
                    "status": info.status.value if hasattr(info.status, 'value') else str(info.status)
                })
            
            return {"collections": result}
            
        except Exception as e:
            return {"error": str(e), "collections": []}
    
    def get_law_summary(self, ley_name: str) -> Dict[str, Any]:
        """Obtener resumen de una ley"""
        # Buscar información sobre la ley en el RAG
        query = f"Resumen de la {ley_name}"
        results = self.search_rag(query, limit=3)
        
        if results.get("results"):
            return {
                "ley": ley_name,
                "resumen": "\n\n".join([r["content"][:500] for r in results["results"]]),
                "fuentes": len(results["results"])
            }
        return {"ley": ley_name, "resumen": "No encontrado", "fuentes": 0}


# Singleton para uso global
_mcp_client = None

def get_mcp_client() -> MCPClient:
    """Obtener instancia del cliente MCP"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client


if __name__ == "__main__":
    # Test del cliente
    client = get_mcp_client()
    
    print("=== Test MCP Client ===\n")
    
    # Listar colecciones
    print("1. Listando colecciones...")
    cols = client.list_collections()
    print(json.dumps(cols, indent=2, ensure_ascii=False))
    
    # Buscar en RAG
    print("\n2. Buscando 'jubilación anticipada'...")
    results = client.search_rag("jubilación anticipada requisitos", limit=3)
    print(json.dumps(results, indent=2, ensure_ascii=False)[:1000])
