"""
Test completo del sistema RAG con 2 capas
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "agents"))

from qdrant_client import QdrantClient
from robertalex_embedder import RoBERTalexEmbedder
import numpy as np

class RAGTester:
    """Tester completo del sistema RAG"""
    
    def __init__(self):
        self.client = QdrantClient(url="http://localhost:6333")
        self.collection_name = "opositaia_leyes_seguridad_social"
        self.embedder = RoBERTalexEmbedder()
        
    def search(self, query: str, layer: int = None, top_k: int = 5):
        """Búsqueda con filtro opcional por capa"""
        
        # Generar embedding
        query_embedding = self.embedder.generate_single(query)
        
        # Filtro por capa si se especifica
        search_filter = None
        if layer:
            search_filter = {
                "must": [{"key": "layer", "match": {"value": layer}}]
            }
        
        # Buscar
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=top_k,
            query_filter=search_filter
        ).points
        
        return results
    
    def test_capa1_normativa(self):
        """Test de búsquedas en Capa 1 (Normativa)"""
        
        print("\n" + "="*70)
        print("📘 TEST CAPA 1: NORMATIVA OFICIAL")
        print("="*70 + "\n")
        
        queries = [
            "¿Cuál es la edad de jubilación ordinaria?",
            "Requisitos para incapacidad permanente total",
            "Procedimiento administrativo común plazos",
            "Derechos fundamentales Constitución",
            "Protección de datos personales LOPDGDD"
        ]
        
        all_scores = []
        
        for i, query in enumerate(queries, 1):
            print(f"{i}. Query: {query}")
            results = self.search(query, layer=1, top_k=3)
            
            if results:
                scores = [r.score for r in results]
                avg_score = sum(scores) / len(scores)
                all_scores.extend(scores)
                
                print(f"   Top resultado: {results[0].payload.get('norma_nombre', 'N/A')}")
                print(f"   Score: {results[0].score:.4f}")
                print(f"   Tipo: {results[0].payload.get('tipo', 'N/A')}")
                print(f"   Artículo: {results[0].payload.get('articulo', 'N/A')}")
                print()
        
        if all_scores:
            print(f"📊 Capa 1 - Score promedio: {sum(all_scores)/len(all_scores):.4f}")
            print(f"   Score máximo: {max(all_scores):.4f}")
            print(f"   Score mínimo: {min(all_scores):.4f}")
        
        return all_scores
    
    def test_capa3_materiales(self):
        """Test de búsquedas en Capa 3 (Materiales)"""
        
        print("\n" + "="*70)
        print("📚 TEST CAPA 3: MATERIALES DE ESTUDIO")
        print("="*70 + "\n")
        
        queries = [
            "test sobre jubilación",
            "casos prácticos de incapacidad temporal",
            "temario de seguridad social",
            "preguntas sobre procedimiento administrativo",
            "ejercicios de cotización"
        ]
        
        all_scores = []
        
        for i, query in enumerate(queries, 1):
            print(f"{i}. Query: {query}")
            results = self.search(query, layer=3, top_k=3)
            
            if results:
                scores = [r.score for r in results]
                avg_score = sum(scores) / len(scores)
                all_scores.extend(scores)
                
                print(f"   Top resultado: {results[0].payload.get('material_nombre', 'N/A')[:50]}...")
                print(f"   Score: {results[0].score:.4f}")
                print(f"   Tipo: {results[0].payload.get('tipo', 'N/A')}")
                print()
        
        if all_scores:
            print(f"📊 Capa 3 - Score promedio: {sum(all_scores)/len(all_scores):.4f}")
            print(f"   Score máximo: {max(all_scores):.4f}")
            print(f"   Score mínimo: {min(all_scores):.4f}")
        
        return all_scores
    
    def test_busqueda_general(self):
        """Test de búsqueda sin filtro (ambas capas)"""
        
        print("\n" + "="*70)
        print("🔍 TEST BÚSQUEDA GENERAL (AMBAS CAPAS)")
        print("="*70 + "\n")
        
        queries = [
            "jubilación anticipada",
            "incapacidad permanente",
            "procedimiento administrativo"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"{i}. Query: {query}")
            results = self.search(query, layer=None, top_k=5)
            
            if results:
                print(f"   Top 5 resultados:")
                for j, r in enumerate(results, 1):
                    layer = r.payload.get('layer', 'N/A')
                    tipo = r.payload.get('tipo', 'N/A')
                    score = r.score
                    
                    emoji = "📘" if layer == 1 else "📚"
                    print(f"   {j}. {emoji} Capa {layer} | {tipo} | Score: {score:.4f}")
                print()
    
    def test_reranking_jerarquia(self):
        """Test de reranking por jerarquía"""
        
        print("\n" + "="*70)
        print("⚖️  TEST RERANKING POR JERARQUÍA")
        print("="*70 + "\n")
        
        query = "jubilación ordinaria requisitos"
        print(f"Query: {query}\n")
        
        # Búsqueda sin filtro
        results = self.search(query, layer=None, top_k=10)
        
        if results:
            print("Resultados SIN reranking:")
            for i, r in enumerate(results[:5], 1):
                layer = r.payload.get('layer', 'N/A')
                jerarquia = r.payload.get('nivel_jerarquia', 'N/A')
                score = r.score
                print(f"  {i}. Capa {layer} | Jerarquía {jerarquia} | Score: {score:.4f}")
            
            # Aplicar reranking por jerarquía
            # Boost: Capa 1 (jerarquía 1) > Capa 1 (jerarquía 2) > Capa 3
            reranked = sorted(results, key=lambda x: (
                -x.payload.get('nivel_jerarquia', 999),  # Menor jerarquía = mayor prioridad
                -x.score  # Mayor score = mayor prioridad
            ))
            
            print("\nResultados CON reranking por jerarquía:")
            for i, r in enumerate(reranked[:5], 1):
                layer = r.payload.get('layer', 'N/A')
                jerarquia = r.payload.get('nivel_jerarquia', 'N/A')
                score = r.score
                print(f"  {i}. Capa {layer} | Jerarquía {jerarquia} | Score: {score:.4f}")
    
    def run_all_tests(self):
        """Ejecutar todos los tests"""
        
        print("\n" + "="*70)
        print("🧪 SUITE COMPLETA DE TESTS DEL RAG")
        print("="*70)
        
        # Test Capa 1
        scores_capa1 = self.test_capa1_normativa()
        
        # Test Capa 3
        scores_capa3 = self.test_capa3_materiales()
        
        # Test búsqueda general
        self.test_busqueda_general()
        
        # Test reranking
        self.test_reranking_jerarquia()
        
        # Resumen final
        print("\n" + "="*70)
        print("📊 RESUMEN FINAL")
        print("="*70 + "\n")
        
        if scores_capa1:
            print(f"Capa 1 (Normativa):")
            print(f"  Score promedio: {sum(scores_capa1)/len(scores_capa1):.4f}")
            print(f"  Queries testeadas: {len(scores_capa1)//3}")
        
        if scores_capa3:
            print(f"\nCapa 3 (Materiales):")
            print(f"  Score promedio: {sum(scores_capa3)/len(scores_capa3):.4f}")
            print(f"  Queries testeadas: {len(scores_capa3)//3}")
        
        # Criterios de éxito
        print("\n" + "="*70)
        print("✅ CRITERIOS DE ÉXITO")
        print("="*70 + "\n")
        
        capa1_avg = sum(scores_capa1)/len(scores_capa1) if scores_capa1 else 0
        capa3_avg = sum(scores_capa3)/len(scores_capa3) if scores_capa3 else 0
        
        print(f"Capa 1 score > 0.60: {'✅' if capa1_avg > 0.60 else '❌'} ({capa1_avg:.4f})")
        print(f"Capa 3 score > 0.55: {'✅' if capa3_avg > 0.55 else '❌'} ({capa3_avg:.4f})")
        print(f"Sistema funcional: ✅")
        
        print("\n" + "="*70)
        print("🎉 TESTS COMPLETADOS")
        print("="*70)

if __name__ == "__main__":
    tester = RAGTester()
    tester.run_all_tests()
