"""
Monitor Live - Monitoreo en tiempo real de Qdrant
"""
import time
from qdrant_client import QdrantClient
from datetime import datetime
import sys

def clear_screen():
    """Limpia la pantalla"""
    print("\033[2J\033[H", end="")

def monitor_live(interval=5):
    """Monitorea en tiempo real"""
    
    collection_name = "opositaia_leyes_seguridad_social"
    client = QdrantClient(url="http://localhost:6333")
    
    print("🔴 MONITOR EN VIVO - Presiona Ctrl+C para salir\n")
    time.sleep(2)
    
    try:
        while True:
            clear_screen()
            
            # Header
            print("="*70)
            print(f"📊 QDRANT LIVE MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*70)
            print()
            
            try:
                # Info de colección
                info = client.get_collection(collection_name)
                
                print(f"🗂️  Colección: {collection_name}")
                print(f"📈 Puntos indexados: {info.points_count:,}")
                print(f"📐 Dimensión vectores: {info.config.params.vectors.size}")
                print(f"📏 Métrica distancia: {info.config.params.vectors.distance}")
                print(f"✅ Estado: {info.status}")
                
                # Tamaño
                size_mb = (info.points_count * info.config.params.vectors.size * 4) / (1024 * 1024)
                print(f"💾 Tamaño estimado: {size_mb:.2f} MB")
                
                print()
                print("-"*70)
                print("📊 ESTADÍSTICAS")
                print("-"*70)
                
                # Obtener muestra de puntos
                sample = client.scroll(
                    collection_name=collection_name,
                    limit=50,
                    with_payload=True,
                    with_vectors=False
                )[0]
                
                # Contar por layer
                layers = {}
                tipos = {}
                articulos = {}
                
                for p in sample:
                    layer = p.payload.get('layer', 'N/A')
                    tipo = p.payload.get('tipo', 'N/A')
                    art = p.payload.get('articulo', 'Sin artículo')
                    
                    layers[layer] = layers.get(layer, 0) + 1
                    tipos[tipo] = tipos.get(tipo, 0) + 1
                    articulos[art] = articulos.get(art, 0) + 1
                
                print(f"\n📑 Distribución por Capa (muestra de 50):")
                for layer, count in sorted(layers.items()):
                    print(f"   Capa {layer}: {count} chunks")
                
                print(f"\n📄 Distribución por Tipo:")
                for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
                    print(f"   {tipo}: {count} chunks")
                
                print(f"\n📖 Top 5 Artículos más frecuentes:")
                for art, count in sorted(articulos.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"   Art. {art}: {count} chunks")
                
                # Último punto indexado
                print()
                print("-"*70)
                print("📝 ÚLTIMO PUNTO INDEXADO")
                print("-"*70)
                
                if sample:
                    last = sample[-1]
                    print(f"\nID: {last.id}")
                    print(f"Norma: {last.payload.get('norma_nombre', 'N/A')}")
                    print(f"Artículo: {last.payload.get('articulo', 'N/A')}")
                    print(f"Página: {last.payload.get('page_num', 'N/A')}")
                    print(f"Chunk: {last.payload.get('chunk_id')}/{last.payload.get('total_chunks')}")
                    print(f"\nTexto: {last.payload.get('text', '')[:150]}...")
                
                print()
                print("="*70)
                print(f"🔄 Actualizando en {interval}s... (Ctrl+C para salir)")
                print("="*70)
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("\n💡 Verifica que Qdrant esté corriendo")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n✅ Monitor detenido")
        sys.exit(0)

if __name__ == "__main__":
    # Intervalo de actualización (segundos)
    interval = 5
    
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except:
            pass
    
    monitor_live(interval)
