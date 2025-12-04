#!/usr/bin/env python3
"""
Prueba búsquedas en materiales de academia indexados
Verifica que no se filtren datos sensibles
"""

from qdrant_client import QdrantClient
from FlagEmbedding import BGEM3FlagModel
import re

class AcademySearchTester:
    def __init__(self):
        self.qdrant = QdrantClient(host="localhost", port=6333)
        print("🔄 Cargando modelo BGE-M3...")
        self.model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
        print("✅ Modelo cargado")
        self.collection_name = "materiales_academia"
    
    def search(self, query: str, limit: int = 5):
        """Busca en la colección"""
        print(f"\n🔍 Búsqueda: '{query}'")
        print("-" * 60)
        
        # Generar embedding de la query
        query_embedding = self.model.encode([query])['dense_vecs'][0]
        
        # Buscar
        results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.tolist(),
            limit=limit
        )
        
        for i, result in enumerate(results, 1):
            print(f"\n[{i}] Score: {result.score:.4f}")
            print(f"Tipo: {result.payload.get('type', 'N/A')}")
            print(f"Archivo: {result.payload.get('filename', 'N/A')}")
            print(f"Texto: {result.payload['text'][:200]}...")
            
            # Verificar que no hay datos sensibles
            self._check_sensitive_data(result.payload['text'])
    
    def _check_sensitive_data(self, text: str):
        """Verifica que no haya datos sensibles sin anonimizar"""
        issues = []
        
        # DNI/NIE sin anonimizar
        if re.search(r'\b\d{8}[A-Z]\b', text):
            issues.append("⚠️  DNI sin anonimizar detectado")
        
        # Teléfonos sin anonimizar
        if re.search(r'\b[6-9]\d{8}\b', text):
            issues.append("⚠️  Teléfono sin anonimizar detectado")
        
        # Emails sin anonimizar
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            issues.append("⚠️  Email sin anonimizar detectado")
        
        if issues:
            print("\n🚨 PROBLEMAS DE PRIVACIDAD:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("✅ Sin datos sensibles detectados")
    
    def get_stats(self):
        """Muestra estadísticas de la colección"""
        collection_info = self.qdrant.get_collection(self.collection_name)
        print("\n📊 Estadísticas de la colección:")
        print(f"  - Vectores indexados: {collection_info.points_count}")
        print(f"  - Dimensión: {collection_info.config.params.vectors.size}")

def main():
    print("🧪 Test de Búsqueda en Materiales de Academia")
    print("=" * 60)
    
    tester = AcademySearchTester()
    tester.get_stats()
    
    # Queries de prueba
    queries = [
        "¿Cuál es la duración máxima de la incapacidad temporal?",
        "Requisitos para la jubilación anticipada voluntaria",
        "Prestaciones por hijo a cargo con discapacidad",
        "Cotización en el régimen general de la seguridad social",
        "Prestación por muerte y supervivencia"
    ]
    
    for query in queries:
        tester.search(query, limit=3)
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
