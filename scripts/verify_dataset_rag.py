
import json
import random
import numpy as np
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Config
DATASET_FILE = "/home/spas/OPOS_GEMINI_1/MASTER_DATASET_v11_REMASTERED.jsonl"
REPORT_FILE = "/home/spas/OPOS_GEMINI_1/DATASET_VERIFICATION_REPORT.md"
SAMPLE_RATE = 0.10
RAG_COLLECTION = "opositaia_knowledge_hybrid_FULL"

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Verifier")

def main():
    print(f"🚀 Iniciando Verificación de Integridad (Muestra {SAMPLE_RATE*100}%)")
    
    # 1. Cargar Dataset
    items = []
    with open(DATASET_FILE, 'r') as f:
        for line in f:
            items.append(json.loads(line))
            
    sample_size = int(len(items) * SAMPLE_RATE)
    sample = random.sample(items, sample_size)
    print(f"📄 Muestra seleccionada: {len(sample)} ítems")
    
    # 2. Conectar a Recursos
    try:
        qdrant = QdrantClient(url="http://localhost:6333", timeout=60) # Increased timeout
        # Check connection
        # qdrant.get_collections() # Skip check to save time if slow
        
        print("🧠 Cargando modelo de embeddings (esto puede tardar un poco)...")
        embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
    except Exception as e:
        print(f"❌ Error conectando a recursos: {e}")
        return

    # 3. Verificación
    results = []
    high_confidence = 0
    low_confidence = 0
    
    print("🔍 Verificando contra Leyes/BOE en Qdrant...")
    
    with open(REPORT_FILE, 'w') as report:
        report.write("# 🛡️ Reporte de Verificación de Dataset v11\n\n")
        report.write(f"**Items verificados:** {len(sample)}\n")
        report.write(f"**Método:** Contraste semántico de Razonamiento vs Base Legal (Qdrant)\n\n")
        
        for i, item in enumerate(sample):
            try:
                # Extraer datos
                msgs = item['messages']
                user_text = next(m['content'] for m in msgs if m['role'] == 'user')
                # Question is part before "Opciones:"
                question = user_text.split("Opciones:")[0].strip()
                
                assist_text = next(m['content'] for m in msgs if m['role'] == 'assistant')
                # Extract Reasoning part
                if "Razonamiento:" in assist_text:
                    reasoning = assist_text.split("Razonamiento:")[1].strip()
                else:
                    reasoning = assist_text
                
                # RAG Search
                q_vec = embedder.encode(question).tolist()
                search_result = qdrant.search(
                    collection_name=RAG_COLLECTION,
                    query_vector=("dense", q_vec),
                    limit=1
                )
                
                if not search_result:
                    score = 0
                    law_text = "No encontrado"
                    law_name = "N/A"
                else:
                    top_hit = search_result[0]
                    law_name = top_hit.payload.get('law_name', 'Unknown')
                    law_text = top_hit.payload.get('text', '') or top_hit.payload.get('text_snippet', '')
                    
                    # Calculate similarity
                    r_vec = embedder.encode(reasoning).reshape(1, -1)
                    l_vec = embedder.encode(law_text[:1000]).reshape(1, -1)
                    score = cosine_similarity(r_vec, l_vec)[0][0]

                # Categorize - Adjusted Thresholds
                status = "✅ VALIDADO" if score > 0.5 else "⚠️ DUDOSO" if score > 0.3 else "❌ SIN REFERENCIA CLARA"
                
                if score > 0.5: high_confidence += 1
                else: low_confidence += 1
                
                print(f"   [{i+1}/{len(sample)}] Score: {score:.2f} - {status}")

                # Write detailed report for samples
                if i < 10 or score < 0.3:
                    report.write(f"### Item {i+1} [{status}] (Score: {score:.2f})\n")
                    report.write(f"**Pregunta:** {question[:150]}...\n")
                    report.write(f"**Razonamiento:** {reasoning[:150]}...\n")
                    report.write(f"**Ley RAG:** {law_name}\n")
                    report.write(f"**Texto Legal:** {law_text[:200]}...\n")
                    report.write("---\n")
                    report.flush() # Force write
                    
            except Exception as e:
                print(f"Error procesando item {i}: {e}")
                
        # Final Stats
        report.write(f"\n## Resumen Estadístico\n")
        report.write(f"- Alta Confianza (Respaldado por Ley): {high_confidence} ({high_confidence/len(sample)*100:.1f}%)\n")
        report.write(f"- Baja Confianza (Requiere revisión): {low_confidence} ({low_confidence/len(sample)*100:.1f}%)\n")

        
    print(f"\n✅ Verificación completada. Reporte guardado en {REPORT_FILE}")
    print(f"Altos: {high_confidence}, Bajos: {low_confidence}")

if __name__ == "__main__":
    main()
