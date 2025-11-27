"""
SPRINT 4: Descargar leyes restantes
- RD Recaudación SS
- RD Afiliación
- Ley IMV
- LOPDGDD
"""
import requests
from pathlib import Path
import time

def download_sprint4():
    """Descarga las 4 leyes restantes del Sprint 4"""
    
    leyes_sprint4 = [
        {
            "nombre": "RD_Recaudacion",
            "boe_id": "BOE-A-2004-11836",
            "descripcion": "Reglamento General de Recaudación SS",
            "url": "https://www.boe.es/buscar/pdf/2004/BOE-A-2004-11836-consolidado.pdf",
            "prioridad": "MEDIA"
        },
        {
            "nombre": "RD_Afiliacion",
            "boe_id": "BOE-A-1996-4447",
            "descripcion": "Reglamento de Afiliación, Altas y Bajas",
            "url": "https://www.boe.es/buscar/pdf/1996/BOE-A-1996-4447-consolidado.pdf",
            "prioridad": "MEDIA"
        },
        {
            "nombre": "Ley_IMV",
            "boe_id": "BOE-A-2021-21007",
            "descripcion": "Ley del Ingreso Mínimo Vital",
            "url": "https://www.boe.es/buscar/pdf/2021/BOE-A-2021-21007-consolidado.pdf",
            "prioridad": "BAJA"
        },
        {
            "nombre": "LOPDGDD",
            "boe_id": "BOE-A-2018-16673",
            "descripcion": "Ley Orgánica de Protección de Datos",
            "url": "https://www.boe.es/buscar/pdf/2018/BOE-A-2018-16673-consolidado.pdf",
            "prioridad": "BAJA"
        }
    ]
    
    output_dir = Path("backend/data/leyes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("📥 SPRINT 4: DESCARGA DE LEYES RESTANTES")
    print("="*70)
    print(f"\n📁 Directorio: {output_dir}")
    print(f"📊 Total leyes: {len(leyes_sprint4)}\n")
    
    results = []
    
    for i, ley in enumerate(leyes_sprint4, 1):
        print(f"{'='*70}")
        print(f"[{i}/{len(leyes_sprint4)}] {ley['nombre']}")
        print(f"{'='*70}")
        print(f"📋 Descripción: {ley['descripcion']}")
        print(f"🔗 BOE ID: {ley['boe_id']}")
        print(f"🟡 Prioridad: {ley['prioridad']}\n")
        
        try:
            print("⏳ Descargando...")
            response = requests.get(ley['url'], timeout=90)
            response.raise_for_status()
            
            # Save PDF
            filepath = output_dir / f"{ley['nombre']}.pdf"
            filepath.write_bytes(response.content)
            
            size_mb = len(response.content) / (1024 * 1024)
            
            print(f"✅ Descargado exitosamente")
            print(f"   - Tamaño: {size_mb:.2f} MB")
            print(f"   - Ubicación: {filepath}\n")
            
            results.append({
                "nombre": ley['nombre'],
                "boe_id": ley['boe_id'],
                "descripcion": ley['descripcion'],
                "filepath": str(filepath),
                "size_mb": size_mb,
                "status": "success"
            })
            
            # Be nice to BOE servers
            if i < len(leyes_sprint4):
                print("⏸️  Esperando 3 segundos...\n")
                time.sleep(3)
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
            results.append({
                "nombre": ley['nombre'],
                "status": "error",
                "error": str(e)
            })
    
    # Summary
    print("\n" + "="*70)
    print("📊 RESUMEN SPRINT 4")
    print("="*70 + "\n")
    
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'error']
    total_size = sum(r.get('size_mb', 0) for r in results)
    
    print(f"✅ Exitosos: {len(successful)}/{len(leyes_sprint4)}")
    print(f"❌ Errores: {len(failed)}/{len(leyes_sprint4)}")
    print(f"💾 Tamaño total: {total_size:.2f} MB\n")
    
    if successful:
        print("📄 Leyes descargadas:")
        for r in successful:
            print(f"   ✅ {r['nombre']} ({r['size_mb']:.2f} MB)")
    
    if failed:
        print("\n❌ Errores:")
        for r in failed:
            print(f"   ❌ {r['nombre']}: {r.get('error', 'Unknown')}")
    
    print("\n" + "="*70)
    if len(successful) == len(leyes_sprint4):
        print("✅ SPRINT 4 DESCARGA COMPLETADA")
        print("\nPróximo paso: Indexar las 4 leyes")
        print("Comando: python backend/index_sprint4.py")
    else:
        print("⚠️  DESCARGA PARCIAL")
        print(f"Completadas: {len(successful)}/{len(leyes_sprint4)}")
    print("="*70)
    
    return results

if __name__ == "__main__":
    download_sprint4()
