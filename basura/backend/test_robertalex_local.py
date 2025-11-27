"""
Test RoBERTalex embeddings locally
Compara con all-minilm para ver diferencia en calidad
"""

import time
from sentence_transformers import SentenceTransformer
import numpy as np

def test_embeddings():
    print("="*60)
    print("🧪 TEST: RoBERTalex vs all-minilm")
    print("="*60)
    
    # Textos de ejemplo (queries reales de opositores)
    queries = [
        "Diferencia entre incapacidad permanente total y absoluta según LGSS",
        "Requisitos para jubilación anticipada voluntaria Art. 208",
        "Cálculo de la base reguladora en prestación por IT",
        "Situaciones asimiladas al alta en Seguridad Social",
        "Cotización en Régimen General vs Régimen Especial Autónomos"
    ]
    
    documentos = [
        "Art. 194 LGSS: Incapacidad permanente total inhabilita para profesión habitual",
        "Art. 195 LGSS: Incapacidad permanente absoluta inhabilita para toda profesión",
        "Art. 208 LGSS: Jubilación anticipada requiere 35 años cotizados",
        "Art. 173 LGSS: Base reguladora IT es promedio últimos 180 días",
        "Art. 166 LGSS: Situaciones asimiladas incluyen desempleo y IT",
        "Art. 305 LGSS: Autónomos cotizan por base elegida entre mínima y máxima"
    ]
    
    print("\n📝 Queries de prueba:")
    for i, q in enumerate(queries, 1):
        print(f"  {i}. {q}")
    
    print("\n📚 Documentos de prueba:")
    for i, d in enumerate(documentos, 1):
        print(f"  {i}. {d}")
    
    # Test 1: all-minilm (actual)
    print("\n" + "="*60)
    print("🔹 TEST 1: all-minilm (modelo actual)")
    print("="*60)
    
    try:
        print("Cargando modelo all-minilm...")
        start = time.time()
        model_minilm = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        load_time = time.time() - start
        print(f"✅ Cargado en {load_time:.2f}s")
        
        print("\nGenerando embeddings...")
        start = time.time()
        query_emb = model_minilm.encode(queries[0])
        doc_embs = model_minilm.encode(documentos)
        embed_time = time.time() - start
        
        print(f"✅ Embeddings generados en {embed_time:.2f}s")
        print(f"   Dimensión: {len(query_emb)}")
        
        # Calcular similitudes
        similarities = np.dot(doc_embs, query_emb) / (
            np.linalg.norm(doc_embs, axis=1) * np.linalg.norm(query_emb)
        )
        
        print(f"\n📊 Similitudes para query: '{queries[0]}'")
        for i, (doc, sim) in enumerate(zip(documentos, similarities), 1):
            print(f"   {i}. {sim:.4f} - {doc[:60]}...")
        
        top_idx = np.argmax(similarities)
        print(f"\n🎯 Documento más relevante: #{top_idx+1} (score: {similarities[top_idx]:.4f})")
        
    except Exception as e:
        print(f"❌ Error con all-minilm: {e}")
    
    # Test 2: RoBERTalex
    print("\n" + "="*60)
    print("🔹 TEST 2: RoBERTalex (modelo legal español)")
    print("="*60)
    
    try:
        print("Descargando RoBERTalex desde HuggingFace...")
        print("⚠️  Esto puede tardar ~5 minutos la primera vez (420 MB)")
        start = time.time()
        # Nombre correcto del modelo en HuggingFace
        model_robertalex = SentenceTransformer('PlanTL-GOB-ES/RoBERTalex')
        load_time = time.time() - start
        print(f"✅ Cargado en {load_time:.2f}s")
        
        print("\nGenerando embeddings...")
        start = time.time()
        query_emb = model_robertalex.encode(queries[0])
        doc_embs = model_robertalex.encode(documentos)
        embed_time = time.time() - start
        
        print(f"✅ Embeddings generados en {embed_time:.2f}s")
        print(f"   Dimensión: {len(query_emb)}")
        
        # Calcular similitudes
        similarities = np.dot(doc_embs, query_emb) / (
            np.linalg.norm(doc_embs, axis=1) * np.linalg.norm(query_emb)
        )
        
        print(f"\n📊 Similitudes para query: '{queries[0]}'")
        for i, (doc, sim) in enumerate(zip(documentos, similarities), 1):
            print(f"   {i}. {sim:.4f} - {doc[:60]}...")
        
        top_idx = np.argmax(similarities)
        print(f"\n🎯 Documento más relevante: #{top_idx+1} (score: {similarities[top_idx]:.4f})")
        
    except Exception as e:
        print(f"❌ Error con RoBERTalex: {e}")
        print(f"   Puede que necesites instalar: pip install sentence-transformers")
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    test_embeddings()
