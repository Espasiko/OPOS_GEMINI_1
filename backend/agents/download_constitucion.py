"""
Download Constitución Española from BOE
"""
import requests
from pathlib import Path
import time

def download_constitucion():
    """Download Constitución Española"""
    
    constitucion = {
        "nombre": "Constitución_Española",
        "boe_id": "BOE-A-1978-31229",
        "descripcion": "Constitución Española de 1978",
        "url": "https://www.boe.es/buscar/pdf/1978/BOE-A-1978-31229-consolidado.pdf"
    }
    
    output_dir = Path("backend/data/leyes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("📥 DESCARGANDO CONSTITUCIÓN ESPAÑOLA")
    print("="*60)
    print(f"\n📁 Directorio: {output_dir}")
    print(f"🔗 URL: {constitucion['url']}\n")
    
    try:
        print("⏳ Descargando...")
        response = requests.get(constitucion['url'], timeout=60)
        response.raise_for_status()
        
        # Save PDF
        filepath = output_dir / f"{constitucion['nombre']}.pdf"
        filepath.write_bytes(response.content)
        
        size_mb = len(response.content) / (1024 * 1024)
        
        print(f"✅ Constitución descargada exitosamente")
        print(f"   - Tamaño: {size_mb:.2f} MB")
        print(f"   - Ubicación: {filepath}")
        print(f"   - BOE ID: {constitucion['boe_id']}")
        
        return {
            "nombre": constitucion['nombre'],
            "boe_id": constitucion['boe_id'],
            "descripcion": constitucion['descripcion'],
            "filepath": str(filepath),
            "size_mb": size_mb,
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ Error descargando Constitución: {e}")
        return {
            "nombre": constitucion['nombre'],
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    result = download_constitucion()
    
    print("\n" + "="*60)
    if result['status'] == 'success':
        print("✅ DESCARGA COMPLETADA")
        print("\nPróximo paso: Indexar Constitución")
        print("Comando: python backend/index_constitucion.py")
    else:
        print("❌ DESCARGA FALLIDA")
        print(f"Error: {result.get('error')}")
    print("="*60)
