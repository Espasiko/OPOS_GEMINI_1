"""
Indexer - Indexa chunks con embeddings en Qdrant
"""
from pathlib import Path
from typing import List, Dict
from datetime import date
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid

from .pdf_processor import PDFProcessor, Chunk
from .robertalex_embedder import RoBERTalexEmbedder

class QdrantIndexer:
    """Indexa documentos en Qdrant"""
    
    def __init__(
        self,
        collection_name: str = "opositaia_leyes_seguridad_social",
        qdrant_url: str = "http://localhost:6333"
    ):
        self.collection_name = collection_name
        self.client = QdrantClient(url=qdrant_url)
        self.embedder = RoBERTalexEmbedder()
        
        print(f"✅ Indexer inicializado")
        print(f"   - Colección: {collection_name}")
        print(f"   - Qdrant: {qdrant_url}")
    
    def index_lgss(self, pdf_path: Path):
        """Indexa LGSS completo"""
        print(f"\n{'='*60}")
        print(f"📚 INDEXANDO LGSS")
        print(f"{'='*60}\n")
        
        # 1. Procesar PDF
        processor = PDFProcessor(chunk_size=512, overlap=50)
        chunks = processor.process_pdf(pdf_path)
        
        print(f"\n{'='*60}")
        print(f"🔄 GENERANDO EMBEDDINGS")
        print(f"{'='*60}\n")
        
        # 2. Generar embeddings
        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedder.generate_embeddings(texts, batch_size=32)
        
        print(f"\n{'='*60}")
        print(f"📤 SUBIENDO A QDRANT")
        print(f"{'='*60}\n")
        
        # 3. Crear puntos para Qdrant
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    # Capa 1: Normativa Oficial
                    "layer": 1,
                    "nivel_jerarquia": 1,
                    "tipo": "ley",
                    
                    # Información de la ley
                    "norma_id": "BOE-A-2015-11724",
                    "norma_nombre": "LGSS",
                    "norma_completa": "Ley General de la Seguridad Social (RDL 8/2015)",
                    "fecha": "2015-10-30",
                    "fecha_vigencia": "2016-01-02",
                    
                    # Información del chunk
                    "articulo": chunk.articulo,
                    "page_num": chunk.page_num,
                    "chunk_id": chunk.chunk_id,
                    "total_chunks": chunk.total_chunks,
                    
                    # Contenido
                    "text": chunk.text
                }
            )
            points.append(point)
            
            if (i + 1) % 100 == 0:
                print(f"   Preparados {i + 1}/{len(chunks)} puntos...")
        
        # 4. Subir a Qdrant en batches
        batch_size = 100
        total_uploaded = 0
        
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch
            )
            total_uploaded += len(batch)
            print(f"   Subidos {total_uploaded}/{len(points)} puntos...")
        
        print(f"\n✅ INDEXACIÓN COMPLETADA")
        print(f"   - Total chunks: {len(chunks)}")
        print(f"   - Total puntos: {len(points)}")
        print(f"   - Colección: {self.collection_name}")
        
        return {
            "total_chunks": len(chunks),
            "total_points": len(points),
            "collection": self.collection_name
        }
    
    def get_collection_stats(self) -> Dict:
        """Obtiene estadísticas de la colección"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "status": "ok"
            }
        except Exception as e:
            return {
                "name": self.collection_name,
                "status": "error",
                "error": str(e)
            }

if __name__ == "__main__":
    # Indexar LGSS
    indexer = QdrantIndexer()
    
    lgss_path = Path("backend/data/leyes/LGSS.pdf")
    
    if lgss_path.exists():
        result = indexer.index_lgss(lgss_path)
        
        print(f"\n{'='*60}")
        print(f"📊 ESTADÍSTICAS FINALES")
        print(f"{'='*60}\n")
        
        stats = indexer.get_collection_stats()
        print(f"Colección: {stats['name']}")
        print(f"Puntos: {stats.get('points_count', 'N/A')}")
        print(f"Estado: {stats['status']}")
        
    else:
        print(f"❌ No se encontró {lgss_path}")
        print("   Ejecuta primero: python backend/agents/download_lgss_only.py")
