"""
Test Search - Prueba búsquedas en Qdrant
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from qdrant_client import QdrantClient
try:
    from .robertalex_embedder import RoBERTalexEmbedder
except ImportError:
    from robertalex_embedder import RoBERTalexEmbedder

class SearchTester:
    """Prueba búsquedas en la colección indexada"""
    
    def __init__(
        self,
        collection_name: str = "opositaia_leyes_seguridad_social",
        qdrant_url: str = "http://localhost:6333"
    ):
        self.collection_name = collection_name
        self.client = QdrantClient(url=qdrant_url)
        self.embedder = RoBERTalexEmbedder()
        
        print(f"✅ SearchTester inicializado")
        print(f"   - Colección: {collection_name}")
    
    def search(self, query: str, top_k: int = 5):
        """Realiza búsqueda semántica"""
        print(f"\n{'='*60}")
        print(f"🔍 BÚSQUEDA: {query}")
        print(f"{'='*60}\n")
        
        # Generar embedding de la query
        query_embedding = self.embedder.generate_single(query)
        
        # Buscar en Qdrant
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=top_k
        ).points
        
        # Mostrar resultados
        print(f"📊 Top {top_k} resultados:\n")
        
        for i, hit in enumerate(results, 1):
            print(f"{i}. Score: {hit.score:.4f}")
            print(f"   Artículo: {hit.payload.get('articulo', 'N/A')}")
            print(f"   Página: {hit.payload.get('page_num', 'N/A')}")
            print(f"   Texto: {hit.payload['text'][:200]}...")
            print()
        
        return results
    
    def test_queries(self):
        """Ejecuta queries de prueba"""
        queries = [
            "¿Cuál es la edad de jubilación ordinaria?",
            "Requisitos para la incapacidad permanente total",
            "¿Qué es la incapacidad temporal?",
            "Prestaciones por desempleo",
            "Cotización a la Seguridad Social"
        ]
        
        print(f"\n{'='*60}")
        print(f"🧪 EJECUTANDO {len(queries)} QUERIES DE PRUEBA")
        print(f"{'='*60}")
        
        all_scores = []
        
        for query in queries:
            results = self.search(query, top_k=3)
            
            if results:
                avg_score = sum(r.score for r in results) / len(results)
                all_scores.append(avg_score)
                print(f"   Score promedio: {avg_score:.4f}\n")
        
        if all_scores:
            print(f"\n{'='*60}")
            print(f"📊 RESUMEN")
            print(f"{'='*60}\n")
            print(f"Queries ejecutadas: {len(queries)}")
            print(f"Score promedio global: {sum(all_scores)/len(all_scores):.4f}")
            print(f"Score máximo: {max(all_scores):.4f}")
            print(f"Score mínimo: {min(all_scores):.4f}")

if __name__ == "__main__":
    tester = SearchTester()
    
    # Verificar colección
    try:
        info = tester.client.get_collection(tester.collection_name)
        print(f"\n✅ Colección encontrada: {info.points_count} puntos\n")
        
        # Ejecutar tests
        tester.test_queries()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nAsegúrate de:")
        print("1. Qdrant está corriendo (docker ps)")
        print("2. La colección existe (python backend/setup_qdrant_collection.py)")
        print("3. LGSS está indexado (python backend/agents/indexer.py)")
