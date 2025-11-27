"""
SPRINT 3: Descargar leyes de prioridad alta
- Ley 39/2015 (Procedimiento Administrativo)
- Ley 40/2015 (Régimen Jurídico)
- EBEP (Estatuto Empleado Público)
"""
import requests
from pathlib import Path
import time

def download_sprint3():
    """Descarga las 3 leyes del Sprint 3"""
    
    leyes_sprint3 = [
        {
            "nombre": "Ley_39_2015",
            "boe_id": "BOE-A-2015-10565",
            "descripcion": "Procedimiento Administrativo Común",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-10565-consolidado.pdf",
            "prioridad": "ALTA"
        },
        {
            "nombre": "Ley_40_2015",
            "boe_id": "BOE-A-2015-10566",
            "descripcion": "Régimen Jurídico del Sector Público",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-10566-consolidado.pdf",
            "prioridad": "ALTA"
        },
        {
            "nombre": "EBEP",
            "boe_id": "BOE-A-2015-11719",
            "descripcion": "Estatuto Básico del Empleado Público",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-11719-consolidado.pdf",
            "prioridad": "ALTA"
        }
    ]
    
    output_dir = Path("backend/data/leyes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("📥 SPRINT 3: DESCARGA DE LEYES PRIORITARIAS")
    print("="*70)
    print(f"\n📁 Directorio: {output_dir}")
    print(f"📊 Total leyes: {len(leyes_sprint3)}\n")
    
    results = []
    
    for i, ley in enumerate(leyes_sprint3, 1):
        print(f"{'='*70}")
        print(f"[{i}/{len(leyes_sprint3)}] {ley['nombre']}")
        print(f"{'='*70}")
        print(f"📋 Descripción: {ley['descripcion']}")
        print(f"🔗 BOE ID: {ley['boe_id']}")
        print(f"🔴 Prioridad: {ley['prioridad']}\n")
        
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
            if i < len(leyes_sprint3):
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
    print("📊 RESUMEN SPRINT 3")
    print("="*70 + "\n")
    
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'error']
    total_size = sum(r.get('size_mb', 0) for r in results)
    
    print(f"✅ Exitosos: {len(successful)}/{len(leyes_sprint3)}")
    print(f"❌ Errores: {len(failed)}/{len(leyes_sprint3)}")
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
    if len(successful) == len(leyes_sprint3):
        print("✅ SPRINT 3 DESCARGA COMPLETADA")
        print("\nPróximo paso: Indexar las 3 leyes")
        print("Comando: python backend/index_sprint3.py")
    else:
        print("⚠️  DESCARGA PARCIAL")
        print(f"Completadas: {len(successful)}/{len(leyes_sprint3)}")
    print("="*70)
    
    return results

if __name__ == "__main__":
    download_sprint3()
