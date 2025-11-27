"""
SPRINT 5: Indexar Capa 3 - Tests y Materiales de Estudio
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agents.pdf_processor import PDFProcessor
from agents.robertalex_embedder import RoBERTalexEmbedder
from agents.indexer import QdrantIndexer
from qdrant_client.models import PointStruct
import uuid

def index_capa3_tests():
    """Indexa tests y materiales de estudio (Capa 3)"""
    
    # Archivos de tests prioritarios
    tests_files = [
        {
            "filename": "Test_Admtvos_AGE_1contestando.pdf",
            "descripcion": "Tests AGE Parte 1 con respuestas",
            "fuente": "Academia",
            "tipo": "test",
            "tiene_respuestas": True
        },
        {
            "filename": "Test_Admtvos_AGE_2contestando.pdf",
            "descripcion": "Tests AGE Parte 2 con respuestas",
            "fuente": "Academia",
            "tipo": "test",
            "tiene_respuestas": True
        },
        {
            "filename": "SS Temario Unificado - Parte específica (1).pdf",
            "descripcion": "Temario Unificado Seguridad Social",
            "fuente": "Academia",
            "tipo": "temario",
            "tiene_respuestas": False
        },
        {
            "filename": "C1-AGE-SUPUESTOS-PRACTICOS-ADMINISTRATIVO-DEL-ESTADO.pdf",
            "descripcion": "Casos Prácticos C1 AGE",
            "fuente": "Academia",
            "tipo": "caso_practico",
            "tiene_respuestas": True
        },
        {
            "filename": "Temario1_Administrativos_Acceso_Libre_AGE.pdf",
            "descripcion": "Temario 1 Administrativos AGE",
            "fuente": "Academia",
            "tipo": "temario",
            "tiene_respuestas": False
        },
        {
            "filename": "Temario2_Administrativos_Acceso_Libre_AGE.pdf",
            "descripcion": "Temario 2 Administrativos AGE",
            "fuente": "Academia",
            "tipo": "temario",
            "tiene_respuestas": False
        }
    ]
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         🎓 SPRINT 5: CAPA 3 - MATERIALES DE ESTUDIO         ║
║                                                              ║
║  Contenido a indexar:                                        ║
║  • Tests con respuestas (2 archivos)                        ║
║  • Temarios de academia (3 archivos)                        ║
║  • Casos prácticos (1 archivo)                              ║
║                                                              ║
║  Tiempo estimado: 2-3 horas                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar archivos
    base_dir = Path("elemplos_leyes_info/de_mi_hija")
    missing = []
    
    for file_info in tests_files:
        filepath = base_dir / file_info['filename']
        if not filepath.exists():
            missing.append(file_info['filename'])
    
    if missing:
        print("❌ ERROR: Faltan archivos:")
        for m in missing:
            print(f"   - {m}")
        print(f"\n💡 Verifica la ruta: {base_dir.absolute()}")
        return
    
    print(f"✅ Todos los archivos encontrados en: {base_dir}\n")
    
    # Confirmar
    print("⚠️  Este proceso puede tomar 2-3 horas")
    print("   Los archivos son grandes (~2,000+ páginas totales)")
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
    
    # Procesar cada archivo
    total_chunks = 0
    total_points = 0
    
    for i, file_info in enumerate(tests_files, 1):
        print("\n" + "="*70)
        print(f"📚 ARCHIVO {i}/{len(tests_files)}: {file_info['filename']}")
        print("="*70)
        print(f"📋 {file_info['descripcion']}")
        print(f"📂 Tipo: {file_info['tipo']}")
        print(f"✅ Respuestas: {'Sí' if file_info['tiene_respuestas'] else 'No'}\n")
        
        filepath = base_dir / file_info['filename']
        
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
                        # Capa 3: Materiales de Estudio
                        "layer": 3,
                        "nivel_jerarquia": 3,
                        "tipo": file_info['tipo'],
                        
                        # Información del material
                        "fuente": file_info['fuente'],
                        "material_nombre": file_info['filename'],
                        "material_descripcion": file_info['descripcion'],
                        "tiene_respuestas": file_info['tiene_respuestas'],
                        
                        # Información del chunk
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
                
                if uploaded % 500 == 0 or uploaded == len(points):
                    print(f"   Subidos {uploaded}/{len(points)} puntos...")
            
            print(f"\n✅ {file_info['filename']} indexado exitosamente")
            print(f"   - Chunks: {len(chunks)}")
            print(f"   - Puntos: {len(points)}")
            
            total_chunks += len(chunks)
            total_points += len(points)
            
        except Exception as e:
            print(f"\n❌ Error indexando {file_info['filename']}: {e}")
            import traceback
            traceback.print_exc()
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN SPRINT 5 - CAPA 3")
    print("="*70 + "\n")
    
    print(f"✅ Archivos indexados: {len(tests_files)}")
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
    print("1. Ver estadísticas por capa:")
    print("   python backend/stats_por_capa.py")
    print()
    print("2. Probar búsquedas en Capa 3:")
    print("   python backend/test_capa3.py")
    print()
    print("3. Integrar con backend FastAPI")

if __name__ == "__main__":
    index_capa3_tests()
