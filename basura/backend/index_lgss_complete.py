"""
Script Maestro - Indexa LGSS completo en Qdrant
Ejecuta todo el pipeline: procesar → embeddings → indexar → test
"""
import sys
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent))

from agents.indexer import QdrantIndexer

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🚀 INDEXACIÓN LGSS - SPRINT 2                     ║
║                                                              ║
║  Pipeline completo:                                          ║
║  1. ✅ Procesar PDF (pypdf)                                 ║
║  2. ✅ Crear chunks (512 tokens, overlap 50)                ║
║  3. ✅ Generar embeddings (RoBERTalex 768 dim)              ║
║  4. ✅ Indexar en Qdrant (Capa 1: Normativa)                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar que existe LGSS.pdf
    lgss_path = Path("backend/data/leyes/LGSS.pdf")
    
    if not lgss_path.exists():
        print("❌ ERROR: No se encontró LGSS.pdf")
        print(f"   Ruta esperada: {lgss_path.absolute()}")
        print("\n💡 Solución:")
        print("   python backend/agents/download_lgss_only.py")
        return
    
    print(f"✅ LGSS.pdf encontrado ({lgss_path.stat().st_size / (1024*1024):.2f} MB)\n")
    
    # Preguntar confirmación
    print("⚠️  Este proceso puede tomar 10-20 minutos")
    print("   - Procesamiento PDF: ~2 min")
    print("   - Generación embeddings: ~5-10 min")
    print("   - Indexación Qdrant: ~2 min")
    
    respuesta = input("\n¿Continuar? (s/n): ").strip().lower()
    
    if respuesta != 's':
        print("\n❌ Cancelado por el usuario")
        return
    
    print("\n" + "="*60)
    print("🚀 INICIANDO INDEXACIÓN")
    print("="*60 + "\n")
    
    try:
        # Crear indexer y ejecutar
        indexer = QdrantIndexer()
        result = indexer.index_lgss(lgss_path)
        
        # Mostrar estadísticas finales
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS FINALES")
        print("="*60 + "\n")
        
        stats = indexer.get_collection_stats()
        
        print(f"✅ INDEXACIÓN COMPLETADA CON ÉXITO\n")
        print(f"Colección: {stats['name']}")
        print(f"Total puntos: {stats.get('points_count', 'N/A')}")
        print(f"Total chunks: {result['total_chunks']}")
        print(f"Estado: {stats['status']}")
        
        print("\n" + "="*60)
        print("🎯 PRÓXIMOS PASOS")
        print("="*60 + "\n")
        print("1. Probar búsquedas:")
        print("   python backend/agents/test_search.py")
        print()
        print("2. Ver colección en Qdrant UI:")
        print("   http://localhost:6333/dashboard")
        print()
        print("3. Continuar con Sprint 3:")
        print("   Indexar más leyes del BOE")
        
    except Exception as e:
        print(f"\n❌ ERROR durante la indexación:")
        print(f"   {e}")
        print("\n💡 Verifica:")
        print("   1. Qdrant está corriendo: docker ps | findstr qdrant")
        print("   2. La colección existe: python backend/setup_qdrant_collection.py")
        print("   3. Dependencias instaladas: pip install -r backend/requirements.txt")
        return

if __name__ == "__main__":
    main()
