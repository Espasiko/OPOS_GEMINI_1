#!/usr/bin/env python3
"""
Auditoría de catálogo BOE - Verifica que cada BOE ID sea una ley válida
y extrae metadatos reales (título, artículos, disposiciones).

Filtra contenido basura: nombramientos, resoluciones, órdenes sin relevancia.
"""

import sys
import json
import time
import re
from pathlib import Path
from typing import Dict, List, Optional

# Añadir backend al path para importar BOEApiClient
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.boe_api_client import BOEApiClient

# Catálogo de leyes del plan (BOE Código 93 secciones 3+4 + adicionales)
CATALOG_BOES = [
    # 3.1 Marco general
    "BOE-A-2015-11724",  # TRLGSS
    
    # 3.2 Incorporación
    "BOE-A-1996-4447",   # RD 84/1996 Afiliación
    "BOE-A-2003-19281",  # Convenio especial
    "BOE-A-2024-8713",   # Convenio especial prácticas
    "BOE-A-1994-1565",   # Solicitudes afiliación
    "BOE-A-2013-3362",   # Sistema RED
    "BOE-A-2023-16892",  # Alta asimilada desplazados
    
    # 3.3 Regímenes especiales
    "BOE-A-1970-1000",   # RETA Ley
    "BOE-A-1970-1066",   # RETA Reglamento
    "BOE-A-1973-282",    # Minería Carbón
    "BOE-A-2015-11346",  # Trabajadores Mar
    "BOE-A-2007-13025",  # Agrarios → RETA
    "BOE-A-2011-15038",  # Agrarios → RG
    
    # 3.4 Cotización y Recaudación
    "BOE-A-1996-1579",   # RD 2064/1995 Cotización
    "BOE-A-2004-11836",  # RD 1415/2004 Recaudación
    "BOE-A-2025-6098",   # Recaudación voluntaria
    "BOE-A-2025-3188",   # Fondo Reserva
    
    # 3.5 Prestaciones (38 leyes)
    "BOE-A-1972-944",    # Prestaciones RG
    "BOE-A-1966-21116",  # Cuantía prestaciones
    "BOE-A-2003-7073",   # Plazos resolución
    "BOE-A-1996-3691",   # Reintegro prestaciones
    "BOE-A-1997-16981",  # Desarrollo reintegro
    "BOE-A-1974-1165",   # LGSS antigua (parcial)
    "BOE-A-2003-10715",  # Ley cohesión SNS
    "BOE-A-2009-15442",  # RD 428/2009 IT
    "BOE-A-2014-7684",   # RD 625/2014 IT
    "BOE-A-2015-6839",   # Desarrollo IT
    "BOE-A-2009-4724",   # RD 295/2009 Maternidad
    "BOE-A-2011-13119",  # RD 1148/2011 Cuidado menores
    "BOE-A-1969-575",    # Invalidez
    "BOE-A-1984-12729",  # IP SS
    "BOE-A-1985-20582",  # Racionalización pensiones
    "BOE-A-1995-19848",  # RD 1300/1995 Incapacidades
    "BOE-A-1996-1644",   # Desarrollo RD 1300/1995
    "BOE-A-1967-1189",   # Vejez
    "BOE-A-1997-24163",  # Consolidación SS
    "BOE-A-2002-23038",  # RD 1132/2002 Jubilación
    "BOE-A-2022-9850",   # Hecho causante jubilación
    "BOE-A-2009-20652",  # Jubilación discapacidad
    "BOE-A-2023-11645",  # Complemento económico
    "BOE-A-2024-391",    # Períodos organizaciones internacionales
    "BOE-A-2025-10488",  # Coeficientes reductores
    "BOE-A-2025-20691",  # Comisión coeficientes (verificar fecha)
    "BOE-A-2011-13242",  # Muerte y supervivencia
    "BOE-A-2018-10397",  # Porcentaje viudedad
    "BOE-A-1967-2876",   # MS RG
    "BOE-A-2005-19151",  # RD 1335/2005 Familiares
    "BOE-A-1991-7270",   # RD 357/1991 PNC
    "BOE-A-2021-21007",  # Ley 19/2021 IMV
    "BOE-A-2021-20316",  # Registro Mediadores IMV
    "BOE-A-2022-15764",  # Compatibilidad IMV
    "BOE-A-2022-12508",  # Consejo IMV
    "BOE-A-2022-4298",   # Comité Ético IMV
    "BOE-A-2022-8639",   # Comité Asesor SS
    "BOE-A-1985-8124",   # Desempleo
    "BOE-A-1984-4850",   # Sistema especial prestaciones
    
    # 4. PRL
    "BOE-A-1995-24292",  # Ley 31/1995 PRL
    "BOE-A-1997-1853",   # RD 39/1997 Servicios Prevención
    
    # Adicionales
    "BOE-A-1978-31229",  # CE
    "BOE-A-2015-11719",  # EBEP
    "BOE-A-2015-11430",  # ET
    "BOE-A-2007-13409",  # LETA
    "BOE-A-2022-12482",  # RDL 13/2022 Autónomos
    "BOE-A-2000-323",    # LEC (solo art. 607)
]

# Mapeo BOE ID → Siglas esperadas
SIGLAS_MAP = {
    "BOE-A-2015-11724": "TRLGSS",
    "BOE-A-1978-31229": "CE",
    "BOE-A-1996-4447": "RD 84/1996",
    "BOE-A-1996-1579": "RD 2064/1995",
    "BOE-A-2004-11836": "RD 1415/2004",
    "BOE-A-2009-15442": "RD 428/2009",
    "BOE-A-2014-7684": "RD 625/2014",
    "BOE-A-2009-4724": "RD 295/2009",
    "BOE-A-2011-13119": "RD 1148/2011",
    "BOE-A-1995-19848": "RD 1300/1995",
    "BOE-A-2002-23038": "RD 1132/2002",
    "BOE-A-2005-19151": "RD 1335/2005",
    "BOE-A-1991-7270": "RD 357/1991",
    "BOE-A-2021-21007": "Ley 19/2021 IMV",
    "BOE-A-1985-8124": "RD 625/1985",
    "BOE-A-2015-11719": "EBEP",
    "BOE-A-2015-11430": "ET",
    "BOE-A-2007-13409": "LETA",
    "BOE-A-2022-12482": "RDL 13/2022",
    "BOE-A-1995-24292": "Ley 31/1995 PRL",
    "BOE-A-1997-1853": "RD 39/1997",
    "BOE-A-2000-323": "LEC",
}

# Patrones para detectar contenido basura (no son leyes normativas)
# IMPORTANTE: Real Decreto-ley, Real Decreto, Ley, Orden ministerial SON VÁLIDOS
BASURA_PATTERNS = [
    r"^nombramiento\s",  # Solo si empieza con "Nombramiento"
    r"^cese\s",
    r"^designación\s",
    r"^resolución\s+de.*convocatoria",
    r"^orden\s+de.*convocatoria",  # Orden DE convocatoria (no Orden ministerial)
    r"corrección de errores",
    r"corrección de erratas",
    r"^anuncio\s",
    r"^edicto\s",
    r"^notificación\s",
]

# IMPORTANTE: La API BOE de legislación consolidada NO tiene parámetro de fecha
# Devuelve el XML completo con TODAS las versiones históricas de cada bloque
# Cada <version> tiene fecha_vigencia → filtraremos por fecha en el código de ingesta
# La web HTML (buscar/act.php?id=X&p=20260303) SÍ permite fecha, pero no la API XML
FECHA_CORTE = "20260303"  # 03/03/2026 - usaremos para filtrar versiones en ingesta


def is_basura(titulo: str) -> bool:
    """Detecta si el título corresponde a basura (no es una ley)."""
    titulo_lower = titulo.lower()
    for pattern in BASURA_PATTERNS:
        if re.search(pattern, titulo_lower):
            return True
    return False


def extract_tipo_norma(titulo: str) -> str:
    """Extrae el tipo de norma del título."""
    titulo_lower = titulo.lower()
    if "real decreto legislativo" in titulo_lower or "texto refundido" in titulo_lower:
        return "rdl"
    elif "real decreto-ley" in titulo_lower:
        return "rdley"
    elif "real decreto" in titulo_lower:
        return "rd"
    elif "ley orgánica" in titulo_lower:
        return "lo"
    elif re.search(r"\bley\s+\d+/", titulo_lower):
        return "ley"
    elif "orden" in titulo_lower:
        return "orden"
    elif "constitución" in titulo_lower:
        return "constitucion"
    else:
        return "otro"


def audit_boe_id(boe_id: str, client: BOEApiClient) -> Optional[Dict]:
    """
    Audita un BOE ID usando BOEApiClient:
    1. Llama a get_metadatos() para obtener título y tipo
    2. Verifica que sea una ley válida (no basura)
    3. Llama a get_indice_texto() para contar artículos y disposiciones
    4. Retorna dict con info o None si es basura/error
    """
    try:
        print(f"  Auditando {boe_id}...", end=" ")
        
        # Paso 1: Obtener metadatos
        try:
            metadatos = client.get_metadatos(boe_id, formato="json")
        except Exception as e:
            if "404" in str(e):
                print("❌ 404 - No disponible en XML API")
                return {
                    "boe_id": boe_id,
                    "siglas": SIGLAS_MAP.get(boe_id, boe_id),
                    "tiene_xml_api": False,
                    "titulo": None,
                    "tipo": None,
                    "num_articulos_boe": 0,
                    "num_disposiciones_boe": 0,
                    "es_basura": False,
                    "error": "404_no_xml_api"
                }
            else:
                raise
        
        # Extraer título de metadatos (data puede ser dict o list)
        data = metadatos.get("data", {})
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        titulo = data.get("titulo", "Sin título") if isinstance(data, dict) else "Sin título"
        
        # Verificar si es basura
        if is_basura(titulo):
            print(f"🗑️  BASURA: {titulo[:60]}")
            return {
                "boe_id": boe_id,
                "siglas": SIGLAS_MAP.get(boe_id, boe_id),
                "tiene_xml_api": True,
                "titulo": titulo,
                "tipo": None,
                "num_articulos_boe": 0,
                "num_disposiciones_boe": 0,
                "es_basura": True,
                "error": "contenido_basura"
            }
        
        # Paso 2: Obtener texto consolidado XML para contar artículos
        try:
            import xml.etree.ElementTree as ET
            texto_xml = client.get_texto_consolidado(boe_id)
            root = ET.fromstring(texto_xml)
            
            # Buscar todos los <bloque> con atributo titulo
            articulos = []
            disposiciones = []
            
            # Navegar por el XML: <response><data><texto><bloque>
            for bloque in root.findall(".//bloque"):
                titulo_bloque = bloque.get("titulo", "")
                
                # Artículos: "Artículo N" o "Artículo N bis/ter/quater"
                if re.match(r"artículo\s+\d+", titulo_bloque, re.I):
                    articulos.append(titulo_bloque)
                
                # Disposiciones
                elif re.search(r"disposición\s+(adicional|transitoria|final|derogatoria)", titulo_bloque, re.I):
                    disposiciones.append(titulo_bloque)
        
        except Exception as e:
            # Si falla, dejar en 0
            articulos = []
            disposiciones = []
            print(f"⚠️ No se pudo parsear XML: {str(e)[:40]}", end=" ")
        
        # Extraer tipo de norma
        tipo_norma = extract_tipo_norma(titulo)
        
        # Fecha de consolidación (si está en metadatos)
        fecha_cons = data.get("fecha_consolidacion") if isinstance(data, dict) else None
        
        print(f"✅ {len(articulos)} arts, {len(disposiciones)} disp")
        
        return {
            "boe_id": boe_id,
            "siglas": SIGLAS_MAP.get(boe_id, boe_id),
            "tiene_xml_api": True,
            "titulo": titulo,
            "tipo": tipo_norma,
            "fecha_consolidacion": fecha_cons,
            "num_articulos_boe": len(articulos),
            "num_disposiciones_boe": len(disposiciones),
            "articulos_sample": articulos[:5],
            "disposiciones_sample": disposiciones[:3],
            "es_basura": False,
            "error": None
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)[:60]}")
        return {
            "boe_id": boe_id,
            "siglas": SIGLAS_MAP.get(boe_id, boe_id),
            "tiene_xml_api": False,
            "titulo": None,
            "tipo": None,
            "num_articulos_boe": 0,
            "num_disposiciones_boe": 0,
            "es_basura": False,
            "error": f"error: {str(e)[:100]}"
        }


def main():
    print(f"🔍 Auditoría BOE - Fecha corte: {FECHA_CORTE} (03/03/2026)")
    print(f"📋 Total leyes a auditar: {len(CATALOG_BOES)}")
    print(f"ℹ️  API devuelve TODAS las versiones - contamos artículos de la más reciente")
    print(f"ℹ️  En ingesta filtraremos versiones vigentes a {FECHA_CORTE}\n")
    
    results = []
    validas = 0
    basura = 0
    sin_xml = 0
    errores = 0
    
    with BOEApiClient(timeout=30) as client:
        for i, boe_id in enumerate(CATALOG_BOES, 1):
            print(f"[{i}/{len(CATALOG_BOES)}]", end=" ")
            
            result = audit_boe_id(boe_id, client)
            
            if result:
                results.append(result)
                
                if result["es_basura"]:
                    basura += 1
                elif result["error"] and "404" in result["error"]:
                    sin_xml += 1
                elif result["error"]:
                    errores += 1
                else:
                    validas += 1
            
            # Rate limiting: 1 request/segundo
            if i < len(CATALOG_BOES):
                time.sleep(1)
    
    # Guardar resultados
    output_path = Path("/home/spas/OPOS_GEMINI_1/backend/data/catalog_boe_verified_20260303.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"✅ Auditoría completada")
    print(f"{'='*60}")
    print(f"📊 Resultados:")
    print(f"  - Leyes válidas con XML API: {validas}")
    print(f"  - Sin XML API (404): {sin_xml}")
    print(f"  - Basura detectada: {basura}")
    print(f"  - Errores: {errores}")
    print(f"\n💾 Guardado en: {output_path}")
    
    # Mostrar leyes basura si las hay
    if basura > 0:
        print(f"\n⚠️  LEYES BASURA DETECTADAS:")
        for r in results:
            if r["es_basura"]:
                print(f"  - {r['boe_id']}: {r['titulo'][:80]}")
    
    # Mostrar leyes sin XML API
    if sin_xml > 0:
        print(f"\n⚠️  LEYES SIN XML API (requieren scraping HTML):")
        for r in results:
            if r["error"] and "404" in r["error"]:
                print(f"  - {r['boe_id']} ({r['siglas']})")


if __name__ == "__main__":
    main()
