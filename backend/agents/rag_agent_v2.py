"""
RAG Agent V2 - Sistema de 2 capas con Pablosi (bge-m3-spa-law-qa-trained-2)
Capa 1: Normativa Oficial (Leyes BOE)
Capa 3: Materiales de Estudio (DESACTIVADO - Foco en Exámenes Oficiales)

MODELO ÚNICO: pablosi/bge-m3-spa-law-qa-trained-2 (1024 dims)
NO usar RoBERTalex ni otros modelos para embeddings.

BÚSQUEDA: HÍBRIDA (Dense + BM25 sparse) con fusión RRF
La colección opositaia_knowledge_FULL_XML fue creada con ambos vectores.
"""

import os
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from qdrant_client import QdrantClient, models
# from sentence_transformers import SentenceTransformer  # Movido a lazy import
import time

logger = logging.getLogger(__name__)

class RAGAgentV2:
    """
    Agente RAG centrado en normativa oficial (BOE) usando la colección FULL_XML.
    Búsqueda HÍBRIDA: Dense (semántico) + BM25 sparse (léxico) fusionados con RRF.
    Metadatos completos del XML BOE expuestos al LLM.
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
        # Colección Maestra: opositaia_knowledge_FULL_XML
        self.collection_name = collection_name or os.getenv("COLLECTION_NAME", "opositaia_knowledge_FULL_XML")
        # Modelo pablosi para embeddings especializados en legislación española
        self.embedding_model = embedding_model or os.getenv("EMBEDDING_MODEL", "pablosi/bge-m3-spa-law-qa-trained-2")
        self.use_local_embeddings = use_local_embeddings if use_local_embeddings is not None else True
        api_key = api_key or os.getenv("QDRANT_API_KEY")
        
        logger.info("Initializing RAG Agent V2 (Hybrid Edition)")
        logger.info(f"  Qdrant URL: {self.qdrant_url}")
        logger.info(f"  Collection: {self.collection_name}")
        logger.info(f"  Embedding Model: {self.embedding_model}")
        logger.info(f"  Search Mode: HYBRID (Dense + BM25)")
        
        # Initialize Qdrant client
        try:
            if api_key:
                self.qdrant_client = QdrantClient(url=self.qdrant_url, api_key=api_key, timeout=30)
                logger.info("  Connected to Qdrant Cloud")
            else:
                self.qdrant_client = QdrantClient(url=self.qdrant_url, timeout=30)
                logger.info("  Connected to Qdrant Local")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise
        
        # Initialize embedding model (local)
        if self.use_local_embeddings:
            self.model = None  # Lazy load in generate_embedding
        else:
            self.model = None
            
        logger.info("✅ RAG Agent V2 Híbrido inicializado")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Genera embedding denso usando bge-m3-spa-law-qa local"""
        if self.use_local_embeddings:
            if self.model is None:
                logger.info(f"Cargando modelo de embeddings {self.embedding_model} (Lazy Load)...")
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(self.embedding_model)
                logger.info("Modelo de embeddings cargado.")
            
            embedding = self.model.encode([text], convert_to_numpy=True)[0]
            return embedding.tolist()
        return []

    def _generate_sparse_vector(self, text: str) -> models.SparseVector:
        """
        Genera vector sparse BM25-compatible a partir del texto.
        Usa tokenización simple (word tokens -> índices hash) compatible 
        con el vocab BM25 creado durante la ingestión.
        """
        words = text.lower().split()
        word_freq: Dict[int, float] = {}
        for word in words:
            idx = hash(word) % 100000  # mismo rango que en el ingestor
            word_freq[idx] = word_freq.get(idx, 0) + 1.0
        if not word_freq:
            return models.SparseVector(indices=[0], values=[0.0])
        return models.SparseVector(
            indices=list(word_freq.keys()),
            values=list(word_freq.values())
        )
    
    async def search_documents(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.35,
        apply_reranking: bool = True
    ) -> List[Dict]:
        """
        Busca documentos usando búsqueda HÍBRIDA (Dense + BM25) con fusión RRF.
        Si el vector sparse no está disponible en la colección, hace fallback a dense.
        """
        try:
            # 1. Generar embeddings
            query_dense = self.generate_embedding(query)
            query_sparse = self._generate_sparse_vector(query)
            
            # 2. Intentar búsqueda HÍBRIDA con prefetch + RRF
            try:
                search_results = self.qdrant_client.query_points(
                    collection_name=self.collection_name,
                    prefetch=[
                        models.Prefetch(
                            query=query_dense,
                            using="dense",
                            limit=top_k * 3,  # Traer más para la fusión
                        ),
                        models.Prefetch(
                            query=query_sparse,
                            using="text",  # Nombre del sparse vector en FULL_XML
                            limit=top_k * 3,
                        ),
                    ],
                    query=models.FusionQuery(fusion=models.Fusion.RRF),  # Fusión RRF
                    limit=top_k * 2,
                    with_payload=True,
                ).points
                logger.info(f"✅ Búsqueda HÍBRIDA (Dense+BM25 RRF): {len(search_results)} resultados")
            except Exception as hybrid_err:
                # Fallback a dense si la colección no tiene sparse o hay error
                logger.warning(f"Búsqueda híbrida fallida ({hybrid_err}), usando dense solo")
                search_results = self.qdrant_client.query_points(
                    collection_name=self.collection_name,
                    query=query_dense,
                    limit=top_k,
                    using="dense",
                    with_payload=True,
                ).points
            
            # 3. Formatear resultados con TODOS los metadatos disponibles
            documents = []
            for result in search_results:
                if hasattr(result, 'score') and result.score < min_score:
                    continue
                    
                payload = result.payload or {}
                
                # --- METADATOS BÁSICOS ---
                boe_id = payload.get('boe_id', '')
                url_boe = payload.get('url_boe') or payload.get('url') or f"https://www.boe.es/buscar/act.php?id={boe_id}"
                
                # --- VIGENCIA Y ESTADO LEGAL --- (campos clave para no alucinar)
                vigente = payload.get('vigente', True)
                estatus_derogacion = payload.get('estatus_derogacion', 'N')
                estado_consolidacion = payload.get('estado_consolidacion', '')
                
                # --- ORGANISMO Y RANGO ---
                organismo_emisor = payload.get('organismo_emisor', '')
                rango = payload.get('rango', '')
                
                # --- FECHAS ---
                fecha_publicacion = payload.get('fecha_publicacion', '')
                fecha_vigencia = payload.get('fecha_vigencia', '')
                
                # --- MATERIAS (del análisis XML) ---
                materias = payload.get('materias', [])
                
                # --- METADATOS XML COMPLETOS (analisis del BOE) ---
                metadata_xml = payload.get('metadata_xml', {})
                analisis_xml = metadata_xml.get('analisis', {}) if metadata_xml else {}
                
                # Construir metadata completa para el LLM
                metadata = {
                    # Identificación
                    "boe_id": boe_id,
                    "law_name": payload.get('law_name', ''),
                    "article_id": payload.get('article_id', ''),
                    "article_title": payload.get('article_title', ''),
                    # Estado legal
                    "vigente": vigente,
                    "estatus_derogacion": estatus_derogacion,  # 'N'=vigente, 'S'=derogado
                    "estado_consolidacion": estado_consolidacion,
                    # Fechas
                    "fecha_publicacion": fecha_publicacion,
                    "fecha_vigencia": fecha_vigencia,
                    # Emisor
                    "organismo_emisor": organismo_emisor,
                    "rango": rango,  # ej: "Ley", "Real Decreto", "Orden"
                    # URLs
                    "url": url_boe,
                    "url_eli": payload.get('url_eli', ''),
                    # Materias del análisis
                    "materias": materias,
                    # Análisis XML completo (derogaciones, modificaciones, relaciones)
                    "analisis_boe": analisis_xml,
                    # Score
                    "score": float(result.score) if hasattr(result, 'score') else 0.0,
                }
                
                documents.append({
                    "id": str(result.id),
                    "score": float(result.score) if hasattr(result, 'score') else 0.0,
                    "content": payload.get("text") or payload.get("text_snippet") or "",
                    "metadata": metadata
                })
            
            # Ordenar por score y tomar top_k
            documents.sort(key=lambda x: x["score"], reverse=True)
            logger.info(f"Found {len(documents[:top_k])} documents for query: {query[:50]}...")
            return documents[:top_k]
            
        except Exception as e:
            logger.error(f"Error en búsqueda RAG: {e}")
            return []
    
    def format_context_for_llm(self, documents: List[Dict]) -> str:
        """
        Formatea TODOS los metadatos para el prompt del LLM.
        Incluye estado de vigencia, derogación, organismo, fechas y materias.
        """
        if not documents:
            return "No se encontró normativa aplicable relevante en el BOE."
        
        context_lines = ["### NORMATIVA OFICIAL (BOE) RELEVANTE:"]
        for i, doc in enumerate(documents, 1):
            m = doc["metadata"]
            
            # Indicador de vigencia — MUY IMPORTANTE para el LLM
            vigencia_tag = "✅ VIGENTE" if m.get("vigente", True) else "⚠️ DEROGADO/MODIFICADO"
            if m.get("estatus_derogacion", "N") == "S":
                vigencia_tag = "❌ DEROGADO"
            
            # Materias
            materias_str = ", ".join(m.get("materias", [])[:3]) if m.get("materias") else ""
            
            # Análisis XML — relaciones legales (normas que derogan/modifican ésta)
            analisis = m.get("analisis_boe", {})
            relaciones = []
            if analisis.get("norma_modificadora"):
                relaciones.append(f"Modificado por: {analisis['norma_modificadora']}")
            if analisis.get("norma_derogadora"):
                relaciones.append(f"Derogado por: {analisis['norma_derogadora']}")
            relaciones_str = " | ".join(relaciones) if relaciones else ""
            
            block = (
                f"\n--- [{i}] {m.get('law_name', 'N/A')} ---\n"
                f"  Artículo: {m.get('article_title', 'N/A')}\n"
                f"  Estado: {vigencia_tag}\n"
            )
            if m.get("organismo_emisor"):
                block += f"  Organismo: {m['organismo_emisor']}\n"
            if m.get("rango"):
                block += f"  Rango: {m['rango']}\n"
            if m.get("fecha_publicacion"):
                block += f"  Publicación BOE: {m['fecha_publicacion']}"
                if m.get("fecha_vigencia"):
                    block += f"  | Desde: {m['fecha_vigencia']}"
                block += "\n"
            if materias_str:
                block += f"  Materias: {materias_str}\n"
            if relaciones_str:
                block += f"  Relaciones: {relaciones_str}\n"
            block += (
                f"  Contenido: {doc['content'][:600]}\n"
                f"  Fuente: {m.get('url', 'N/A')}\n"
            )
            context_lines.append(block)
        
        context_lines.append("\n> INSTRUCCIÓN: Si el artículo aparece como DEROGADO o MODIFICADO, indícalo "
                             "explícitamente en tu respuesta y cita la norma que lo sustituyó si está disponible.")
        
        return "\n".join(context_lines)
    
    async def search_and_answer(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.35,
        layer_filter: Optional[int] = None,  # Kept for compatibility, ignored
        apply_reranking: bool = True         # Kept for compatibility, ignored
    ) -> Dict:
        """
        Busca documentos y prepara respuesta completa con todos los metadatos.
        
        Returns:
            {
                "query": str,
                "documents": List[Dict],
                "context": str,        # Formateado con todos los metadatos
                "metadata": Dict
            }
        """
        start_time = time.time()
        
        # Buscar documentos (búsqueda híbrida)
        documents = await self.search_documents(
            query=query,
            top_k=top_k,
            min_score=min_score,
        )
        
        # Formatear contexto completo
        context = self.format_context_for_llm(documents)
        
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
                "search_mode": "HYBRID (Dense + BM25 RRF)",
                "reranking_applied": False,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    async def get_collection_stats(self) -> Dict:
        """Obtiene estadísticas de la colección"""
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "total_documents": collection_info.points_count,
                "status": "healthy",
                "search_mode": "HYBRID (Dense + BM25 RRF)"
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
        _rag_agent_v2_instance = RAGAgentV2()
    return _rag_agent_v2_instance
