"""
BOE Downloader for OpositaIA
Downloads main laws from BOE official website
"""
import requests
from pathlib import Path
from typing import List, Dict
import time

class BOEDownloader:
    """Downloads PDFs from BOE"""
    
    LEYES_PRINCIPALES = [
        {
            "nombre": "LGSS",
            "boe_id": "BOE-A-2015-11724",
            "descripcion": "Ley General de la Seguridad Social",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-11724-consolidado.pdf"
        },
        {
            "nombre": "Ley_39_2015",
            "boe_id": "BOE-A-2015-10565",
            "descripcion": "Procedimiento Administrativo Común",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-10565-consolidado.pdf"
        },
        {
            "nombre": "Ley_40_2015",
            "boe_id": "BOE-A-2015-10566",
            "descripcion": "Régimen Jurídico del Sector Público",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-10566-consolidado.pdf"
        },
        {
            "nombre": "EBEP",
            "boe_id": "BOE-A-2015-11719",
            "descripcion": "Estatuto Básico del Empleado Público",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-11719-consolidado.pdf"
        },
        {
            "nombre": "RD_Recaudacion",
            "boe_id": "BOE-A-2004-11836",
            "descripcion": "Reglamento General de Recaudación SS",
            "url": "https://www.boe.es/buscar/pdf/2004/BOE-A-2004-11836-consolidado.pdf"
        },
        {
            "nombre": "RD_Afiliacion",
            "boe_id": "BOE-A-1996-4447",
            "descripcion": "Reglamento de Afiliación, Altas y Bajas",
            "url": "https://www.boe.es/buscar/pdf/1996/BOE-A-1996-4447-consolidado.pdf"
        },
        {
            "nombre": "Ley_IMV",
            "boe_id": "BOE-A-2021-21007",
            "descripcion": "Ley del Ingreso Mínimo Vital",
            "url": "https://www.boe.es/buscar/pdf/2021/BOE-A-2021-21007-consolidado.pdf"
        },
        {
            "nombre": "LOPDGDD",
            "boe_id": "BOE-A-2018-16673",
            "descripcion": "Ley Orgánica de Protección de Datos",
            "url": "https://www.boe.es/buscar/pdf/2018/BOE-A-2018-16673-consolidado.pdf"
        }
    ]
    
    def __init__(self, output_dir: str = "backend/data/leyes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download_all(self) -> List[Dict]:
        """Download all main laws"""
        results = []
        
        print(f"📥 Descargando {len(self.LEYES_PRINCIPALES)} leyes principales del BOE...")
        print(f"📁 Directorio: {self.output_dir}\n")
        
        for i, ley in enumerate(self.LEYES_PRINCIPALES, 1):
            print(f"[{i}/{len(self.LEYES_PRINCIPALES)}] {ley['nombre']} - {ley['descripcion']}")
            
            try:
                # Download PDF
                response = requests.get(ley['url'], timeout=60)
                response.raise_for_status()
                
                # Save PDF
                filepath = self.output_dir / f"{ley['nombre']}.pdf"
                filepath.write_bytes(response.content)
                
                size_mb = len(response.content) / (1024 * 1024)
                
                results.append({
                    "nombre": ley['nombre'],
                    "boe_id": ley['boe_id'],
                    "descripcion": ley['descripcion'],
                    "filepath": str(filepath),
                    "size_mb": size_mb,
                    "status": "success"
                })
                
                print(f"   ✅ Descargado ({size_mb:.2f} MB)\n")
                
                # Be nice to BOE servers
                time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Error: {e}\n")
                results.append({
                    "nombre": ley['nombre'],
                    "boe_id": ley['boe_id'],
                    "descripcion": ley['descripcion'],
                    "status": "error",
                    "error": str(e)
                })
        
        # Summary
        successful = sum(1 for r in results if r['status'] == 'success')
        failed = sum(1 for r in results if r['status'] == 'error')
        total_size = sum(r.get('size_mb', 0) for r in results)
        
        print(f"\n{'='*60}")
        print(f"📊 RESUMEN DE DESCARGA")
        print(f"{'='*60}")
        print(f"✅ Exitosos: {successful}/{len(self.LEYES_PRINCIPALES)}")
        print(f"❌ Errores: {failed}/{len(self.LEYES_PRINCIPALES)}")
        print(f"💾 Tamaño total: {total_size:.2f} MB")
        print(f"📁 Ubicación: {self.output_dir}")
        
        return results

if __name__ == "__main__":
    downloader = BOEDownloader()
    results = downloader.download_all()
