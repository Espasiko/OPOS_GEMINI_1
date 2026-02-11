"""
RAG Helper - Búsqueda de artículos en Qdrant local
"""
import logging
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class RAGHelper:
    """
    Helper para búsqueda RAG en Qdrant local
    """
    
    def __init__(self):
        # Qdrant local
        self.qdrant_url = "http://localhost:6333"
        self.client = QdrantClient(url=self.qdrant_url)
        
        # Modelo de embeddings
        self.model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
        
        # Colecciones
        self.collection_chunks = "opositaia_knowledge_v2"
        self.collection_laws = "opositaia_leyes_master"
        
        logger.info(f"RAGHelper initialized: {self.qdrant_url}")
    
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
            # Generar embedding
            query_vector = self.model.encode(query).tolist()
            
            # Buscar en chunks
            results = self.client.search(
                collection_name=self.collection_chunks,
                query_vector=query_vector,
                limit=limit,
                with_payload=True
            )
            
            articles = []
            seen_articles = set()
            
            for hit in results:
                payload = hit.payload
                article_id = payload.get('article_id', '')
                
                # Evitar duplicados
                if article_id in seen_articles:
                    continue
                seen_articles.add(article_id)
                
                # Buscar artículo completo en master
                full_article = self._get_full_article(article_id)
                
                if full_article:
                    articles.append({
                        'article_id': article_id,
                        'titulo': full_article.get('titulo', ''),
                        'texto': full_article.get('texto', ''),
                        'boe_id': full_article.get('boe_id', ''),
                        'score': hit.score
                    })
            
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

{art['texto'][:500]}...
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
