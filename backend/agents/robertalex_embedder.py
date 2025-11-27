"""
RoBERTalex Embedder - Genera embeddings con RoBERTalex
"""
from pathlib import Path
from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

class RoBERTalexEmbedder:
    """Genera embeddings usando RoBERTalex"""
    
    def __init__(self, model_name: str = "PlanTL-GOB-ES/RoBERTalex"):
        print(f"🤖 Cargando modelo: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = 768  # RoBERTalex dimension
        print(f"✅ Modelo cargado (dimensión: {self.embedding_dim})")
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Genera embeddings en batches"""
        print(f"🔄 Generando embeddings para {len(texts)} textos...")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        print(f"✅ Embeddings generados: shape {embeddings.shape}")
        return embeddings
    
    def generate_single(self, text: str) -> np.ndarray:
        """Genera embedding para un solo texto"""
        return self.model.encode([text], convert_to_numpy=True)[0]

if __name__ == "__main__":
    # Test rápido
    embedder = RoBERTalexEmbedder()
    
    test_texts = [
        "Artículo 212. Jubilación ordinaria",
        "La incapacidad temporal es una prestación económica",
        "Requisitos para la jubilación anticipada"
    ]
    
    print(f"\n{'='*60}")
    print("🧪 TEST DE EMBEDDINGS")
    print(f"{'='*60}\n")
    
    embeddings = embedder.generate_embeddings(test_texts)
    
    print(f"\n📊 Resultados:")
    print(f"   - Textos procesados: {len(test_texts)}")
    print(f"   - Shape embeddings: {embeddings.shape}")
    print(f"   - Dimensión: {embeddings.shape[1]}")
    print(f"   - Tipo: {embeddings.dtype}")
    
    # Calcular similitud entre primeros dos
    from numpy.linalg import norm
    
    def cosine_similarity(a, b):
        return np.dot(a, b) / (norm(a) * norm(b))
    
    sim = cosine_similarity(embeddings[0], embeddings[1])
    print(f"\n🔍 Similitud entre texto 1 y 2: {sim:.4f}")
