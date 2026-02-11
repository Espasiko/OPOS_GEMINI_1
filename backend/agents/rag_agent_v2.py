"""
RAG Agent V2 - Sistema de 2 capas con Pablosi (bge-m3-spa-law-qa-trained-2)
Capa 1: Normativa Oficial (Leyes BOE)
Capa 3: Materiales de Estudio

MODELO ÚNICO: pablosi/bge-m3-spa-law-qa-trained-2 (1024 dims)
NO usar RoBERTalex ni otros modelos para embeddings.
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import time
# import cohere  # TODO: Descomentar cuando se use reranking

logger = logging.getLogger(__name__)

class RAGAgentV2:
    """
    Agente RAG con arquitectura de 2 capas y reranking jerárquico
    """
    
    def __init__(
        self,
        qdrant_url: Optional[str] = None,
        collection_name: Optional[str] = None,
        embedding_model: Optional[str] = None,
        api_key: Optional[str] = None,
        use_local_embeddings: Optional[bool] = None,
    ):
        # Leer desde variables de entorno si no se proporcionan
        self.qdrant_url = qdrant_url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self.collection_name = collection_name or os.getenv("COLLECTION_NAME", "opositaia_knowledge")
        # Modelo pablosi para embeddings especializados en legislación española
        self.embedding_model = embedding_model or os.getenv("EMBEDDING_MODEL", "pablosi/bge-m3-spa-law-qa-trained-2")
        self.use_local_embeddings = use_local_embeddings if use_local_embeddings is not None else True
        api_key = api_key or os.getenv("QDRANT_API_KEY")
        
        logger.info("Initializing RAG Agent V2")
        logger.info(f"  Qdrant URL: {self.qdrant_url}")
        logger.info(f"  Collection: {self.collection_name}")
        logger.info(f"  Embedding Model: {self.embedding_model}")
        logger.info(f"  Local embeddings: {self.use_local_embeddings}")
        
        # Initialize Qdrant client
        try:
            if api_key:
                self.qdrant_client = QdrantClient(url=self.qdrant_url, api_key=api_key, timeout=30)
                logger.info("  Connected to Qdrant Cloud with API key")
            else:
                self.qdrant_client = QdrantClient(url=self.qdrant_url, timeout=30)
                logger.info("  Connected to Qdrant (local)")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise
        
        # Initialize embedding model (local) si procede
        if self.use_local_embeddings:
            logger.info(f"Loading embedding model: {self.embedding_model}")
            self.model = SentenceTransformer(self.embedding_model)
        else:
            self.model = None
            
        # Initialize Cohere client for Reranking
        self.co_key = os.getenv("COHERE_API_KEY")
        if self.co_key:
            try:
                self.co = cohere.ClientV2(self.co_key)
                logger.info("  Cohere Rerank initialized")
            except Exception as e:
                logger.error(f"  Failed to init Cohere: {e}")
                self.co = None
        else:
            self.co = None
        
        logger.info("✅ RAG Agent V2 initialized successfully")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Genera embedding usando bge-m3-spa-law-qa local o endpoint externo"""
        if self.use_local_embeddings and self.model:
            embedding = self.model.encode([text], convert_to_numpy=True)[0]
            return embedding.tolist()
        else:
            # Usar endpoint externo (ejemplo Ollama)
            import httpx
            ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            try:
                with httpx.Client(timeout=30.0) as client:
                    response = client.post(
                        f"{ollama_url}/api/embeddings",
                        json={
                            "model": self.embedding_model,
                            "prompt": text
                        }
                    )
                    response.raise_for_status()
                    data = response.json()
                    return data.get("embedding", [])
            except Exception as e:
                logger.error(f"Error generating embedding via Ollama: {e}")
                return []
    
    async def search_documents(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.5,
        layer_filter: Optional[int] = None,
        apply_reranking: bool = True
    ) -> List[Dict]:
        """
        Busca documentos con filtro opcional por capa
        
        Args:
            query: Consulta del usuario
            top_k: Número de resultados
            min_score: Score mínimo (0-1)
            layer_filter: Filtrar por capa (1=Normativa, 3=Materiales)
            apply_reranking: Aplicar reranking jerárquico
        
        Returns:
            Lista de documentos con score y metadata
        """
        try:
            # 1. Generar embedding
            query_embedding = self.generate_embedding(query)
            
            # 2. Preparar filtro por capa
            search_filter = None
            if layer_filter:
                search_filter = {
                    "must": [{"key": "layer", "match": {"value": layer_filter}}]
                }
            
            # 3. Buscar en Qdrant (obtener más para reranking)
            search_results = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k * 2 if apply_reranking else top_k,
                query_filter=search_filter,
                using="dense"  # Named vector for opositaia_knowledge collection
            ).points
            
            # 4. Filtrar por min_score
            search_results = [r for r in search_results if r.score >= min_score]
            
            # 5. Aplicar reranking jerárquico inicial (Nivel de Ley)
            if apply_reranking and not layer_filter:
                search_results = sorted(search_results, key=lambda x: (
                    -x.payload.get('nivel_jerarquia', 999),  # Menor = mayor prioridad
                    -x.score
                ))
            
            # 6. Aplicar COHERE RERANK (Si está disponible)
            # TODO: Descomentar cuando se use Cohere
            # if apply_reranking and self.co:
            #     try:
            #         logger.info("  Applying Cohere Rerank...")
            #         documents_to_rerank = [r.payload.get("text", "") for r in search_results]
            #         if documents_to_rerank:
            #             rerank_response = self.co.rerank(
            #                 model="rerank-v3.5",
            #                 query=query,
            #                 documents=documents_to_rerank,
            #                 top_n=top_k
            #             )
            #             # Reordenar resultados basados en el índice devuelto por cohere
            #             new_results = []
            #             for result in rerank_response.results:
            #                 idx = result.index
            #                 orig_r = search_results[idx]
            #                 orig_r.score = result.relevance_score # Actualizar score
            #                 new_results.append(orig_r)
            #             search_results = new_results
            #     except Exception as e:
            #         logger.error(f"  Cohere Rerank error: {e}")
            
            # 7. Tomar top_k después de reranking
            search_results = search_results[:top_k]
            
            # 7. Formatear resultados - INCLUIR SIEMPRE TODOS LOS CAMPOS
            documents = []
            for result in search_results:
                layer = result.payload.get('layer', 0)
                
                # SIEMPRE incluir campos básicos del payload (independiente de layer)
                metadata = {
                    "layer": layer,
                    "boe_id": result.payload.get('boe_id', ''),
                    "law_name": result.payload.get('law_name', ''),
                    "article_id": result.payload.get('article_id', ''),
                    "chunk_index": result.payload.get('chunk_index', 0),
                    "parent_id": result.payload.get('parent_id', ''),
                    "nivel_jerarquia": result.payload.get('nivel_jerarquia', 3),
                    "is_smart_chunk": result.payload.get('is_smart_chunk', False)
                }
                
                # Añadir metadata anidado si existe
                if 'metadata' in result.payload and isinstance(result.payload['metadata'], dict):
                    metadata['metadata_nested'] = result.payload['metadata']
                
                # Campos adicionales según tipo de documento
                if layer == 1 or layer == "article_chunk":
                    # Normativa / article_chunk
                    metadata.update({
                        "tipo": result.payload.get('tipo', ''),
                        "norma_nombre": result.payload.get('norma_nombre', result.payload.get('law_name', '')),
                        "norma_completa": result.payload.get('norma_completa', ''),
                        "articulo": result.payload.get('articulo', result.payload.get('article_id', '')),
                        "fecha": result.payload.get('fecha', '')
                    })

                    # LOGICA ROBUSTA: Construir URL desde BOE ID si es necesario
                    url = ""
                    boe_id = result.payload.get('boe_id', '')
                    
                    # 1. Intentar sacar de metadata_nested (si existe)
                    if 'metadata' in result.payload and 'data' in result.payload['metadata']:
                         try:
                             url = result.payload['metadata']['data']['metadatos']['url_html_consolidada']['_text']
                         except:
                             pass
                    
                    # 2. Si falla, construirla usando el patrón oficial
                    if not url and boe_id and boe_id.startswith('BOE'):
                        url = f"https://www.boe.es/buscar/act.php?id={boe_id}"
                        logger.info(f"🔗 URL Construida desde ID: {url}")
                    
                    metadata["url"] = url
                elif layer == 3:
                    # Materiales
                    metadata.update({
                        "tipo": result.payload.get('tipo', ''),
                        "material_nombre": result.payload.get('material_nombre', ''),
                        "material_descripcion": result.payload.get('material_descripcion', ''),
                        "fuente": result.payload.get('fuente', ''),
                        "tiene_respuestas": result.payload.get('tiene_respuestas', False)
                    })
                
                doc = {
                    "id": str(result.id),
                    "score": float(result.score),
                    "content": result.payload.get("text", ""),
                    "metadata": metadata
                }
                documents.append(doc)
            
            logger.info(f"Found {len(documents)} documents for query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            raise
    
    def format_context_for_llm(self, documents: List[Dict]) -> str:
        """
        Formatea documentos como contexto para el LLM
        """
        if not documents:
            return "No se encontraron documentos relevantes."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            meta = doc["metadata"]
            layer = meta.get("layer", 0)
            
            # Formato según la capa
            if layer == 1:
                # Normativa
                source = f"{meta.get('norma_nombre', 'N/A')}"
                if meta.get('articulo'):
                    source += f" - Artículo {meta['articulo']}"
                tipo = meta.get('tipo', 'ley')
            else:
                # Materiales
                source = meta.get('material_descripcion', 'Material de estudio')
                tipo = meta.get('tipo', 'material')
            
            context_parts.append(
                f"[{i}] {source} ({tipo})\n"
                f"Relevancia: {doc['score']:.2%}\n"
                f"Contenido:\n{doc['content']}\n"
                f"---"
            )
        
        return "\n\n".join(context_parts)
    
    async def search_and_answer(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.5,
        layer_filter: Optional[int] = None,
        apply_reranking: bool = True
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
        start_time = time.time()
        
        # Buscar documentos
        documents = await self.search_documents(
            query=query,
            top_k=top_k,
            min_score=min_score,
            layer_filter=layer_filter,
            apply_reranking=apply_reranking
        )
        
        # Formatear contexto
        context = self.format_context_for_llm(documents)
        
        # Calcular tiempo
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        return {
            "query": query,
            "documents": documents,
            "context": context,
            "metadata": {
                "total_documents": len(documents),
                "top_score": documents[0]["score"] if documents else 0.0,
                "search_time_ms": elapsed_ms,
                "embedding_model": self.embedding_model,
                "reranking_applied": apply_reranking,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    async def get_collection_stats(self) -> Dict:
        """
        Obtiene estadísticas de la colección
        """
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "total_documents": collection_info.points_count,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": str(collection_info.config.params.vectors.distance),
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
_rag_agent_v2_instance = None

def get_rag_agent_v2() -> RAGAgentV2:
    """Get or create RAG Agent V2 singleton"""
    global _rag_agent_v2_instance
    if _rag_agent_v2_instance is None:
        _rag_agent_v2_instance = RAGAgentV2(
            qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            collection_name=os.getenv("COLLECTION_NAME", "opositaia_knowledge"),  # Changed from QDRANT_COLLECTION
            embedding_model=os.getenv("EMBEDDING_MODEL", "pablosi/bge-m3-spa-law-qa-trained-2"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
    return _rag_agent_v2_instance
