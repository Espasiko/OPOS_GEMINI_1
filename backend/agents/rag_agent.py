"""
RAG Agent - Búsqueda semántica en documentos BOE
Usa bge-m3 embeddings + Qdrant + Gemini
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

logger = logging.getLogger(__name__)

class RAGAgent:
    """
    Agente especializado en búsqueda RAG sobre documentos BOE
    """
    
    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        qdrant_url: str = "http://localhost:6333",
        embedding_model: str = "bge-m3",
        collection_name: str = "opositaia_documents"
    ):
        self.ollama_url = ollama_url
        self.qdrant_url = qdrant_url
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(url=qdrant_url)
        
        logger.info(f"RAG Agent initialized with {embedding_model}")
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Genera embedding usando Ollama (bge-m3)
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/embeddings",
                    json={
                        "model": self.embedding_model,
                        "prompt": text
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data["embedding"]
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    async def search_documents(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.7,
        tema_filter: Optional[int] = None
    ) -> List[Dict]:
        """
        Busca documentos relevantes en Qdrant
        
        Args:
            query: Consulta del usuario
            top_k: Número de resultados
            min_score: Score mínimo (0-1)
            tema_filter: Filtrar por tema específico
        
        Returns:
            Lista de documentos con score y metadata
        """
        try:
            # 1. Generar embedding de la query
            query_embedding = await self.generate_embedding(query)
            
            # 2. Preparar filtros (opcional)
            query_filter = None
            if tema_filter:
                query_filter = Filter(
                    must=[
                        FieldCondition(
                            key="tema_id",
                            match=MatchValue(value=tema_filter)
                        )
                    ]
                )
            
            # 3. Buscar en Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=min_score,
                query_filter=query_filter
            )
            
            # 4. Formatear resultados
            documents = []
            for result in search_results:
                doc = {
                    "id": result.id,
                    "score": result.score,
                    "content": result.payload.get("content", ""),
                    "metadata": {
                        "titulo": result.payload.get("titulo", ""),
                        "tema_id": result.payload.get("tema_id"),
                        "tema_nombre": result.payload.get("tema_nombre", ""),
                        "fuente": result.payload.get("fuente", ""),
                        "url_boe": result.payload.get("url_boe", ""),
                        "fecha": result.payload.get("fecha", "")
                    }
                }
                documents.append(doc)
            
            logger.info(f"Found {len(documents)} documents for query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            raise
    
    def format_context_for_llm(self, documents: List[Dict]) -> str:
        """
        Formatea documentos encontrados como contexto para el LLM
        """
        if not documents:
            return "No se encontraron documentos relevantes en el BOE."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            metadata = doc["metadata"]
            context_parts.append(
                f"[Documento {i}] {metadata.get('titulo', 'Sin título')}\n"
                f"Fuente: {metadata.get('fuente', 'BOE')}\n"
                f"Tema: {metadata.get('tema_nombre', 'N/A')}\n"
                f"Relevancia: {doc['score']:.2%}\n"
                f"Contenido:\n{doc['content']}\n"
                f"---"
            )
        
        return "\n\n".join(context_parts)
    
    async def search_and_answer(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.7,
        tema_filter: Optional[int] = None
    ) -> Dict:
        """
        Busca documentos y prepara respuesta completa
        
        Returns:
            {
                "query": str,
                "documents": List[Dict],
                "context": str,
                "metadata": Dict
            }
        """
        start_time = datetime.now()
        
        # Buscar documentos
        documents = await self.search_documents(
            query=query,
            top_k=top_k,
            min_score=min_score,
            tema_filter=tema_filter
        )
        
        # Formatear contexto
        context = self.format_context_for_llm(documents)
        
        # Calcular tiempo
        elapsed_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return {
            "query": query,
            "documents": documents,
            "context": context,
            "metadata": {
                "total_documents": len(documents),
                "top_score": documents[0]["score"] if documents else 0.0,
                "search_time_ms": elapsed_ms,
                "embedding_model": self.embedding_model,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    async def get_collection_stats(self) -> Dict:
        """
        Obtiene estadísticas de la colección Qdrant
        """
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "total_documents": collection_info.points_count,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "status": "healthy"
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {
                "collection_name": self.collection_name,
                "status": "error",
                "error": str(e)
            }


# Singleton instance
_rag_agent_instance = None

def get_rag_agent() -> RAGAgent:
    """
    Get or create RAG Agent singleton
    """
    global _rag_agent_instance
    if _rag_agent_instance is None:
        _rag_agent_instance = RAGAgent(
            ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
            qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "bge-m3"),
            collection_name=os.getenv("QDRANT_COLLECTION", "opositaia_documents")
        )
    return _rag_agent_instance
