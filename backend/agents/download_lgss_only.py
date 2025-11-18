"""
Download LGSS only for testing
"""
import requests
from pathlib import Path
import time

def download_lgss():
    """Download only LGSS for initial testing"""
    
    ley = {
        "nombre": "LGSS",
        "boe_id": "BOE-A-2015-11724",
        "descripcion": "Ley General de la Seguridad Social",
        "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-11724-consolidado.pdf"
    }
    
    output_dir = Path("backend/data/leyes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("📥 DESCARGANDO LGSS (Ley General Seguridad Social)")
    print("="*60)
    print(f"\n📁 Directorio: {output_dir}")
    print(f"🔗 URL: {ley['url']}\n")
    
    try:
        print("⏳ Descargando...")
        response = requests.get(ley['url'], timeout=60)
        response.raise_for_status()
        
        # Save PDF
        filepath = output_dir / f"{ley['nombre']}.pdf"
        filepath.write_bytes(response.content)
        
        size_mb = len(response.content) / (1024 * 1024)
        
        print(f"✅ LGSS descargado exitosamente")
        print(f"   - Tamaño: {size_mb:.2f} MB")
        print(f"   - Ubicación: {filepath}")
        print(f"   - BOE ID: {ley['boe_id']}")
        
        return {
            "nombre": ley['nombre'],
            "boe_id": ley['boe_id'],
            "descripcion": ley['descripcion'],
            "filepath": str(filepath),
            "size_mb": size_mb,
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ Error descargando LGSS: {e}")
        return {
            "nombre": ley['nombre'],
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    result = download_lgss()
    
    print("\n" + "="*60)
    if result['status'] == 'success':
        print("✅ DESCARGA COMPLETADA")
        print("\nPróximo paso: Procesar y embedear LGSS")
    else:
        print("❌ DESCARGA FALLIDA")
        print(f"Error: {result.get('error')}")
    print("="*60)
