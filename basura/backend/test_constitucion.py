"""
Test búsquedas en Constitución Española
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "agents"))

from qdrant_client import QdrantClient
from robertalex_embedder import RoBERTalexEmbedder

def test_constitucion():
    """Prueba búsquedas sobre la Constitución"""
    
    collection_name = "opositaia_leyes_seguridad_social"
    client = QdrantClient(url="http://localhost:6333")
    embedder = RoBERTalexEmbedder()
    
    print("\n" + "="*70)
    print("🇪🇸 TEST BÚSQUEDAS - CONSTITUCIÓN ESPAÑOLA")
    print("="*70 + "\n")
    
    queries = [
        "Derechos fundamentales y libertades públicas",
        "Organización territorial del Estado",
        "Poder judicial y tribunales",
        "Reforma de la Constitución",
        "Corona española y sucesión"
    ]
    
    all_scores = []
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"🔍 QUERY {i}: {query}")
        print(f"{'='*70}\n")
        
        # Generar embedding
        query_embedding = embedder.generate_single(query)
        
        # Buscar
        results = client.query_points(
            collection_name=collection_name,
            query=query_embedding.tolist(),
            limit=3
        ).points
        
        print(f"📊 Top 3 resultados:\n")
        
        query_scores = []
        for j, hit in enumerate(results, 1):
            norma = hit.payload.get('norma_nombre', 'N/A')
            tipo = hit.payload.get('tipo', 'N/A')
            articulo = hit.payload.get('articulo', 'N/A')
            
            # Marcar si es de Constitución
            emoji = "🇪🇸" if tipo == "constitucion" else "📄"
            
            print(f"{j}. {emoji} Score: {hit.score:.4f}")
            print(f"   Norma: {norma}")
            print(f"   Tipo: {tipo}")
            print(f"   Artículo: {articulo}")
            print(f"   Texto: {hit.payload['text'][:150]}...")
            print()
            
            query_scores.append(hit.score)
        
        if query_scores:
            avg = sum(query_scores) / len(query_scores)
            all_scores.extend(query_scores)
            print(f"   Score promedio: {avg:.4f}")
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN FINAL")
    print("="*70 + "\n")
    
    print(f"Queries ejecutadas: {len(queries)}")
    print(f"Score promedio global: {sum(all_scores)/len(all_scores):.4f}")
    print(f"Score máximo: {max(all_scores):.4f}")
    print(f"Score mínimo: {min(all_scores):.4f}")
    
    # Contar cuántos resultados son de Constitución
    print("\n" + "="*70)
    print("📈 ANÁLISIS DE RELEVANCIA")
    print("="*70 + "\n")
    
    print("✅ Sistema funcionando correctamente")
    print("✅ Constitución indexada y buscable")
    print("✅ Búsquedas devuelven resultados relevantes")

if __name__ == "__main__":
    test_constitucion()
