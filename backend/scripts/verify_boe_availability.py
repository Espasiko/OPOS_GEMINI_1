#!/usr/bin/env python3
"""
Script de verificación de disponibilidad BOE para leyes del catálogo.
Prueba 4 fuentes para cada BOE-ID: caché, XML consolidado, XML diario, HTML scraping.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# Añadir backend al path
sys.path.insert(0, "/home/spas/OPOS_GEMINI_1/backend")

from services.boe_service import BOEService, get_boe_service


@dataclass
class VerificationResult:
    boe_id: str
    siglas: str
    titulo: str
    cache: bool
    xml_consolidado: bool
    xml_diario: bool
    html_scrape: bool
    source_usable: Optional[str]
    materias_count: int
    relaciones_count: int
    error: Optional[str] = None


async def verify_single_law(boe_service: BOEService, boe_id: str, siglas: str, titulo: str) -> VerificationResult:
    """Verifica una ley contra las 4 fuentes"""
    result = VerificationResult(
        boe_id=boe_id,
        siglas=siglas,
        titulo=titulo,
        cache=False,
        xml_consolidado=False,
        xml_diario=False,
        html_scrape=False,
        source_usable=None,
        materias_count=0,
        relaciones_count=0
    )
    
    try:
        # 1. Verificar caché
        cached = boe_service._load_from_cache(boe_id)
        if cached:
            result.cache = True
            result.source_usable = "CACHE"
            result.materias_count = len(cached.get("analisis", {}).get("materias", []))
            result.relaciones_count = (
                len(cached.get("analisis", {}).get("referencias_anteriores", [])) +
                len(cached.get("analisis", {}).get("referencias_posteriores", []))
            )
            return result
        
        # 2. Intentar XML consolidado
        try:
            xml_text = await boe_service.fetch_xml_consolidado(boe_id)
            if xml_text:
                result.xml_consolidado = True
                result.source_usable = "XML_CONSOLIDADO"
                # Parsear para contar datos
                law_data = boe_service._parse_xml_completo(xml_text, boe_id, "TEST")
                result.materias_count = len(law_data.analisis.materias)
                result.relaciones_count = (
                    len(law_data.analisis.referencias_anteriores) +
                    len(law_data.analisis.referencias_posteriores)
                )
                # Guardar en caché
                boe_service._save_to_cache(boe_id, law_data)
                return result
        except Exception as e:
            pass  # Continuar con siguiente fuente
        
        # 3. Intentar XML diario + HTML
        analisis = await boe_service.fetch_analisis_from_diario(boe_id)
        html_text = await boe_service.scrape_html_consolidado(boe_id)
        
        if analisis.materias or analisis.referencias_anteriores or analisis.referencias_posteriores:
            result.xml_diario = True
            result.materias_count = len(analisis.materias)
            result.relaciones_count = len(analisis.referencias_anteriores) + len(analisis.referencias_posteriores)
        
        if html_text:
            result.html_scrape = True
        
        if result.xml_diario and result.html_scrape:
            result.source_usable = "DIARIO+HTML"
            # Guardar en caché
            law_data = boe_service._parse_cached_json({
                "boe_id": boe_id,
                "texto_xml": None,
                "texto_html": html_text,
                "metadatos": {"boe_id": boe_id, "titulo": titulo},
                "analisis": analisis.to_dict(),
                "source": "DIARIO+HTML"
            }, boe_id)
            boe_service._save_to_cache(boe_id, law_data)
        elif result.html_scrape:
            result.source_usable = "HTML_ONLY"
        elif result.xml_diario:
            result.source_usable = "DIARIO_ONLY"
        
        if not result.source_usable:
            result.error = "No disponible en ninguna fuente"
        
        return result
        
    except Exception as e:
        result.error = str(e)
        return result


async def verify_catalog(catalog_path: str, only_failed: bool = False):
    """Verifica todas las leyes del catálogo"""
    
    # Cargar catálogo
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    
    boe_service = get_boe_service()
    results: List[VerificationResult] = []
    
    print(f"🔍 Verificando {len(catalog)} leyes del catálogo...")
    print("=" * 80)
    
    for i, entry in enumerate(catalog, 1):
        boe_id = entry["boe_id"]
        siglas = entry.get("siglas", "N/A")
        titulo = entry.get("titulo", "")[:60]
        
        print(f"\n[{i}/{len(catalog)}] {boe_id} ({siglas})")
        print(f"    {titulo}...")
        
        result = await verify_single_law(boe_service, boe_id, siglas, entry.get("titulo", ""))
        results.append(result)
        
        # Mostrar resultado
        if result.source_usable:
            print(f"    ✅ {result.source_usable}")
            print(f"       Materias: {result.materias_count}, Relaciones: {result.relaciones_count}")
        else:
            print(f"    ❌ NO DISPONIBLE")
            if result.error:
                print(f"       Error: {result.error}")
        
        # Delay para no saturar BOE
        await asyncio.sleep(0.5)
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 80)
    
    disponibles = [r for r in results if r.source_usable]
    no_disponibles = [r for r in results if not r.source_usable]
    
    print(f"\n✅ Disponibles: {len(disponibles)}/{len(results)}")
    print(f"❌ No disponibles: {len(no_disponibles)}/{len(results)}")
    
    # Por fuente
    fuentes = {}
    for r in results:
        if r.source_usable:
            fuentes[r.source_usable] = fuentes.get(r.source_usable, 0) + 1
    
    print("\n📁 Por fuente:")
    for fuente, count in sorted(fuentes.items(), key=lambda x: -x[1]):
        print(f"   - {fuente}: {count}")
    
    # Leyes no disponibles (críticas)
    if no_disponibles:
        print("\n🚨 LEYES NO DISPONIBLES (requieren atención manual):")
        for r in no_disponibles:
            print(f"   - {r.boe_id} ({r.siglas})")
            print(f"     {r.titulo[:60]}...")
    
    # Guardar reporte
    report_path = Path("/home/spas/OPOS_GEMINI_1/data/boe_verification_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in results], f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Reporte guardado en: {report_path}")
    
    return results


async def verify_specific_laws(boe_ids: List[str]):
    """Verifica una lista específica de BOE-IDs"""
    
    boe_service = get_boe_service()
    results = []
    
    print(f"🔍 Verificando {len(boe_ids)} BOE-IDs específicos...")
    print("=" * 80)
    
    for boe_id in boe_ids:
        print(f"\n🔎 {boe_id}")
        
        result = await verify_single_law(boe_service, boe_id, "N/A", "")
        results.append(result)
        
        if result.source_usable:
            print(f"   ✅ {result.source_usable}")
            print(f"      Materias: {result.materias_count}, Relaciones: {result.relaciones_count}")
        else:
            print(f"   ❌ NO DISPONIBLE")
        
        await asyncio.sleep(0.5)
    
    return results


def main():
    """Entry point para ejecución desde línea de comandos"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Verifica disponibilidad BOE de leyes")
    parser.add_argument("--catalog", default="/home/spas/OPOS_GEMINI_1/backend/data/catalog_FINAL_v2.json",
                        help="Ruta al catálogo JSON")
    parser.add_argument("--only-failed", action="store_true",
                        help="Solo mostrar leyes no disponibles")
    parser.add_argument("--boe-ids", nargs="+",
                        help="Lista específica de BOE-IDs a verificar")
    
    args = parser.parse_args()
    
    if args.boe_ids:
        results = asyncio.run(verify_specific_laws(args.boe_ids))
    else:
        results = asyncio.run(verify_catalog(args.catalog, args.only_failed))
    
    # Exit code: 0 si todas disponibles, 1 si hay fallos
    failed = [r for r in results if not r.source_usable]
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
