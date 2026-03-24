"""
RAG Helper - Búsqueda de artículos en Qdrant local
"""
import logging
from typing import List, Dict, Any
from qdrant_client import QdrantClient, models as qmodels
# from sentence_transformers import SentenceTransformer  # Lazy import

logger = logging.getLogger(__name__)


class RAGHelper:
    """
    Helper para búsqueda RAG en Qdrant local
    """
    
    def __init__(self):
        # Qdrant local
        self.qdrant_url = "http://localhost:6333"
        self.client = QdrantClient(url=self.qdrant_url)
        
        # Modelo de embeddings (Lazy load)
        self.model = None
        self.embedding_model_name = "pablosi/bge-m3-spa-law-qa-trained-2"
        
        # Colecciones — FULL_XML es la colección maestra (14.038 puntos, Dense+BM25)
        self.collection_chunks = "opositaia_knowledge_FULL_XML"
        self.collection_laws = "opositaia_leyes_master"
        
        logger.info(f"RAGHelper initialized: {self.qdrant_url} → {self.collection_chunks}")

    
    def search_articles(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Busca artículos relevantes en Qdrant
        
        Args:
            query: Query de búsqueda
            limit: Número de resultados
        
        Returns:
            Lista de artículos con texto completo
        """
        try:
            # Validación de query para evitar ruido (Error detectado por el usuario)
            if not query or not query.strip() or len(query.strip()) < 3:
                logger.warning(f"Query de RAG demasiado corta o vacía: '{query}'. Cancelando búsqueda.")
                return []

            # Generar embedding (con lazy load)
            if self.model is None:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(self.embedding_model_name)
                
            query_vector = self.model.encode(query).tolist()
            
            # Buscar en chunks usando el vector nombrado 'dense' (FULL_XML tiene vectores nombrados)
            # Nota: La colección FULL_XML tiene vectores: 'dense' (1024d) y 'text' (sparse BM25)
            # Filtro de vigencia estricto (Error 4)
            search_filter = qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key="vigente",
                        match=qmodels.MatchValue(value=True),
                    )
                ]
            )
            
            # Buscar en chunks usando el vector nombrado 'dense'
            response = self.client.query_points(
                collection_name=self.collection_chunks,
                query=query_vector,
                using="dense",
                limit=limit,
                query_filter=search_filter,
                with_payload=True
            )
            results = response.points
            
            articles = []
            seen_articles = set()
            
            for hit in results:
                payload = hit.payload or {}
                
                # HEURÍSTICA DE EXTRACCIÓN ROBUSTA (FULL_XML es inconsistente)
                # 1. Identificador del artículo (lo que R1 debe citar)
                article_id = (
                    payload.get('article_id') or 
                    payload.get('precepto') or 
                    payload.get('precepto_id') or 
                    payload.get('article_title', '').split('.')[0] or # Ej: 'Artículo 123. Título' -> 'Artículo 123'
                    "Artículo Desconocido"
                )
                
                # 2. Título de la ley o contexto
                law_context = (
                    payload.get('law_title') or 
                    payload.get('law_name') or 
                    payload.get('titulo') or 
                    "Legislación Española"
                )

                # Evitar duplicados por nombre de artículo
                if article_id in seen_articles:
                    continue
                seen_articles.add(article_id)
                
                artikel = {
                    'article_id': article_id,
                    'titulo': law_context,
                    'texto': payload.get('text', payload.get('text_snippet', '')),
                    'boe_id': payload.get('boe_id', ''),
                    'law_name': law_context,
                    'vigente': payload.get('vigente', True),
                    'url': payload.get('url_boe', payload.get('url', '')),
                    'score': float(hit.score) if hit.score else 0.0
                }
                articles.append(artikel)
            
            logger.info(f"Found {len(articles)} articles for query: {query[:50]}...")
            return articles
        
        except Exception as e:
            logger.error(f"Error searching articles: {e}")
            return []

    
    def _get_full_article(self, article_id: str) -> Dict[str, Any]:
        """
        Recupera artículo completo de opositaia_leyes_master
        """
        try:
            # Buscar por article_id en metadata
            results = self.client.scroll(
                collection_name=self.collection_laws,
                scroll_filter={
                    "must": [
                        {
                            "key": "article_id",
                            "match": {"value": article_id}
                        }
                    ]
                },
                limit=1,
                with_payload=True
            )
            
            if results[0]:  # results es (points, next_offset)
                return results[0][0].payload
            
            return {}
        
        except Exception as e:
            logger.error(f"Error getting full article {article_id}: {e}")
            return {}
    
    def format_articles_for_prompt(self, articles: List[Dict[str, Any]]) -> str:
        """
        Formatea artículos para incluir en el prompt
        """
        if not articles:
            return "No se encontraron artículos relevantes."
        
        formatted = []
        for art in articles:
            formatted.append(f"""
**{art['article_id']}** - {art['titulo']}
BOE: {art['boe_id']}

{art['texto']}
""".strip())
        
        return "\n\n---\n\n".join(formatted)


# Singleton
_rag_helper = None

def get_rag_helper() -> RAGHelper:
    """Get or create RAG helper singleton"""
    global _rag_helper
    if _rag_helper is None:
        _rag_helper = RAGHelper()
    return _rag_helper
