"""
Indexar Constitución Española en Qdrant
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agents.indexer import QdrantIndexer
from agents.pdf_processor import PDFProcessor
from agents.robertalex_embedder import RoBERTalexEmbedder
from qdrant_client.models import PointStruct
import uuid

def index_constitucion():
    """Indexa la Constitución Española"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🇪🇸 INDEXACIÓN CONSTITUCIÓN ESPAÑOLA 1978            ║
║                                                              ║
║  Pipeline:                                                   ║
║  1. ✅ Descargar PDF del BOE                                ║
║  2. ✅ Procesar y detectar artículos                        ║
║  3. ✅ Generar embeddings (RoBERTalex)                      ║
║  4. ✅ Indexar en Qdrant (Capa 1: Normativa)               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar archivo
    const_path = Path("backend/data/leyes/Constitución_Española.pdf")
    
    if not const_path.exists():
        print("❌ ERROR: No se encontró Constitución_Española.pdf")
        print(f"   Ruta esperada: {const_path.absolute()}")
        print("\n💡 Solución:")
        print("   python backend/agents/download_constitucion.py")
        return
    
    print(f"✅ Constitución encontrada ({const_path.stat().st_size / (1024*1024):.2f} MB)\n")
    
    # Confirmar
    print("⚠️  Este proceso puede tomar 5-10 minutos")
    respuesta = input("\n¿Continuar? (s/n): ").strip().lower()
    
    if respuesta != 's':
        print("\n❌ Cancelado")
        return
    
    print("\n" + "="*60)
    print("🚀 INICIANDO INDEXACIÓN")
    print("="*60 + "\n")
    
    try:
        # Inicializar componentes
        processor = PDFProcessor(chunk_size=512, overlap=50)
        embedder = RoBERTalexEmbedder()
        indexer = QdrantIndexer()
        
        # 1. Procesar PDF
        print("="*60)
        print("🔄 PROCESANDO PDF")
        print("="*60 + "\n")
        
        chunks = processor.process_pdf(const_path)
        
        # 2. Generar embeddings
        print("\n" + "="*60)
        print("🔄 GENERANDO EMBEDDINGS")
        print("="*60 + "\n")
        
        texts = [chunk.text for chunk in chunks]
        embeddings = embedder.generate_embeddings(texts, batch_size=32)
        
        # 3. Crear puntos con metadata específica
        print("\n" + "="*60)
        print("📤 SUBIENDO A QDRANT")
        print("="*60 + "\n")
        
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    # Capa 1: Normativa Oficial
                    "layer": 1,
                    "nivel_jerarquia": 1,  # Máxima jerarquía
                    "tipo": "constitucion",
                    
                    # Información de la norma
                    "norma_id": "BOE-A-1978-31229",
                    "norma_nombre": "Constitución_Española",
                    "norma_completa": "Constitución Española de 1978",
                    "fecha": "1978-12-29",
                    "fecha_vigencia": "1978-12-29",
                    
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
            
            if (i + 1) % 50 == 0:
                print(f"   Preparados {i + 1}/{len(chunks)} puntos...")
        
        # 4. Subir a Qdrant
        batch_size = 100
        total_uploaded = 0
        
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            indexer.client.upsert(
                collection_name=indexer.collection_name,
                points=batch
            )
            total_uploaded += len(batch)
            print(f"   Subidos {total_uploaded}/{len(points)} puntos...")
        
        print(f"\n✅ INDEXACIÓN COMPLETADA")
        print(f"   - Total chunks: {len(chunks)}")
        print(f"   - Total puntos: {len(points)}")
        
        # Estadísticas finales
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS FINALES")
        print("="*60 + "\n")
        
        stats = indexer.get_collection_stats()
        print(f"Colección: {stats['name']}")
        print(f"Total puntos: {stats.get('points_count', 'N/A')}")
        print(f"Estado: {stats['status']}")
        
        print("\n" + "="*60)
        print("🎯 PRÓXIMOS PASOS")
        print("="*60 + "\n")
        print("1. Verificar indexación:")
        print("   python backend/monitor_qdrant.py")
        print()
        print("2. Probar búsquedas:")
        print("   python backend/agents/test_search.py")
        print()
        print("3. Ver en Qdrant UI:")
        print("   http://localhost:6333/dashboard")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    index_constitucion()
