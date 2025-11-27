"""
SPRINT 3: Indexar 3 leyes prioritarias
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agents.pdf_processor import PDFProcessor
from agents.robertalex_embedder import RoBERTalexEmbedder
from agents.indexer import QdrantIndexer
from qdrant_client.models import PointStruct
import uuid

def index_sprint3():
    """Indexa las 3 leyes del Sprint 3"""
    
    leyes_sprint3 = [
        {
            "nombre": "Ley_39_2015",
            "boe_id": "BOE-A-2015-10565",
            "descripcion": "Ley 39/2015 Procedimiento Administrativo Común",
            "tipo": "ley",
            "nivel_jerarquia": 1
        },
        {
            "nombre": "Ley_40_2015",
            "boe_id": "BOE-A-2015-10566",
            "descripcion": "Ley 40/2015 Régimen Jurídico del Sector Público",
            "tipo": "ley",
            "nivel_jerarquia": 1
        },
        {
            "nombre": "EBEP",
            "boe_id": "BOE-A-2015-11719",
            "descripcion": "Estatuto Básico del Empleado Público (EBEP)",
            "tipo": "ley",
            "nivel_jerarquia": 1
        }
    ]
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🚀 SPRINT 3: INDEXACIÓN MASIVA                 ║
║                                                              ║
║  Leyes a indexar:                                            ║
║  1. Ley 39/2015 - Procedimiento Administrativo              ║
║  2. Ley 40/2015 - Régimen Jurídico                          ║
║  3. EBEP - Estatuto Empleado Público                        ║
║                                                              ║
║  Tiempo estimado: 30-45 minutos                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar archivos
    data_dir = Path("backend/data/leyes")
    missing = []
    
    for ley in leyes_sprint3:
        filepath = data_dir / f"{ley['nombre']}.pdf"
        if not filepath.exists():
            missing.append(ley['nombre'])
    
    if missing:
        print("❌ ERROR: Faltan archivos:")
        for m in missing:
            print(f"   - {m}.pdf")
        print("\n💡 Solución:")
        print("   python backend/download_sprint3.py")
        return
    
    print("✅ Todos los archivos encontrados\n")
    
    # Confirmar
    print("⚠️  Este proceso puede tomar 30-45 minutos")
    print("   - Procesamiento: ~5 min")
    print("   - Embeddings: ~25-35 min")
    print("   - Indexación: ~3 min")
    
    respuesta = input("\n¿Continuar? (s/n): ").strip().lower()
    
    if respuesta != 's':
        print("\n❌ Cancelado")
        return
    
    # Inicializar componentes
    print("\n" + "="*70)
    print("🔧 INICIALIZANDO COMPONENTES")
    print("="*70 + "\n")
    
    processor = PDFProcessor(chunk_size=512, overlap=50)
    embedder = RoBERTalexEmbedder()
    indexer = QdrantIndexer()
    
    # Procesar cada ley
    total_chunks = 0
    total_points = 0
    
    for i, ley in enumerate(leyes_sprint3, 1):
        print("\n" + "="*70)
        print(f"📚 LEY {i}/3: {ley['nombre']}")
        print("="*70)
        print(f"📋 {ley['descripcion']}")
        print(f"🔗 {ley['boe_id']}\n")
        
        filepath = data_dir / f"{ley['nombre']}.pdf"
        
        try:
            # 1. Procesar PDF
            print("🔄 Procesando PDF...")
            chunks = processor.process_pdf(filepath)
            
            # 2. Generar embeddings
            print(f"\n🔄 Generando embeddings para {len(chunks)} chunks...")
            texts = [chunk.text for chunk in chunks]
            embeddings = embedder.generate_embeddings(texts, batch_size=32)
            
            # 3. Crear puntos
            print(f"\n📤 Preparando puntos para Qdrant...")
            points = []
            
            for j, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.tolist(),
                    payload={
                        # Capa 1: Normativa Oficial
                        "layer": 1,
                        "nivel_jerarquia": ley['nivel_jerarquia'],
                        "tipo": ley['tipo'],
                        
                        # Información de la norma
                        "norma_id": ley['boe_id'],
                        "norma_nombre": ley['nombre'],
                        "norma_completa": ley['descripcion'],
                        "fecha": "2015-10-01" if "2015" in ley['boe_id'] else "N/A",
                        
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
            
            # 4. Subir a Qdrant
            print(f"📤 Subiendo {len(points)} puntos a Qdrant...")
            
            batch_size = 100
            uploaded = 0
            
            for k in range(0, len(points), batch_size):
                batch = points[k:k + batch_size]
                indexer.client.upsert(
                    collection_name=indexer.collection_name,
                    points=batch
                )
                uploaded += len(batch)
                
                if uploaded % 200 == 0 or uploaded == len(points):
                    print(f"   Subidos {uploaded}/{len(points)} puntos...")
            
            print(f"\n✅ {ley['nombre']} indexado exitosamente")
            print(f"   - Chunks: {len(chunks)}")
            print(f"   - Puntos: {len(points)}")
            
            total_chunks += len(chunks)
            total_points += len(points)
            
        except Exception as e:
            print(f"\n❌ Error indexando {ley['nombre']}: {e}")
            import traceback
            traceback.print_exc()
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN SPRINT 3")
    print("="*70 + "\n")
    
    print(f"✅ Leyes indexadas: {len(leyes_sprint3)}")
    print(f"📄 Total chunks: {total_chunks}")
    print(f"📍 Total puntos: {total_points}")
    
    # Estadísticas de colección
    stats = indexer.get_collection_stats()
    print(f"\n🗂️  Colección: {stats['name']}")
    print(f"📈 Total puntos en colección: {stats.get('points_count', 'N/A')}")
    print(f"✅ Estado: {stats['status']}")
    
    print("\n" + "="*70)
    print("🎯 PRÓXIMOS PASOS")
    print("="*70 + "\n")
    print("1. Ver estadísticas:")
    print("   python backend/stats_por_norma.py")
    print()
    print("2. Probar búsquedas:")
    print("   python backend/agents/test_search.py")
    print()
    print("3. Monitor en vivo:")
    print("   python backend/monitor_qdrant.py")

if __name__ == "__main__":
    index_sprint3()
