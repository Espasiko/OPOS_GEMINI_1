#!/usr/bin/env python3
"""
Script Maestro para Descargar las 60 Leyes del Temario SS + AGE
Usa la API oficial de datos abiertos del BOE.
"""
import os
import sys
import json
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.boe_api_client import BOEApiClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =====================================================
# LISTA COMPLETA DE LEYES Y REGLAMENTOS (60 normas)
# =====================================================

LEYES_TEMARIO = [
    # Bloque 1: Constitución y Organización del Estado
    {"boe_id": "BOE-A-1978-31229", "nombre": "Constitución Española 1978"},
    {"boe_id": "BOE-A-1979-23709", "nombre": "LO 2/1979 Tribunal Constitucional"},
    {"boe_id": "BOE-A-1981-7118", "nombre": "LO 3/1981 Defensor del Pueblo"},
    {"boe_id": "BOE-A-1985-12666", "nombre": "LO 6/1985 Poder Judicial"},
    {"boe_id": "BOE-A-1997-25336", "nombre": "Ley 50/1997 del Gobierno"},
    {"boe_id": "BOE-A-1997-7878", "nombre": "LO 6/1997 LOFAGE"},
    {"boe_id": "BOE-A-1985-5392", "nombre": "Ley 7/1985 Bases Régimen Local"},
    {"boe_id": "BOE-A-2013-13756", "nombre": "Ley 27/2013 Racionalización Admin Local"},
    
    # Bloque 2: Procedimiento Administrativo
    {"boe_id": "BOE-A-2015-10565", "nombre": "Ley 39/2015 PAC"},
    {"boe_id": "BOE-A-2015-10566", "nombre": "Ley 40/2015 LRJSP"},
    {"boe_id": "BOE-A-1998-16718", "nombre": "Ley 29/1998 Contencioso-Administrativo"},
    # Código Civil es muy extenso, BOE-A-1889-4763 (se descargará aparte si es necesario)
    
    # Bloque 3: Empleo Público
    {"boe_id": "BOE-A-2015-11719", "nombre": "EBEP RDL 5/2015"},
    {"boe_id": "BOE-A-1984-17387", "nombre": "Ley 30/1984 Reforma Función Pública"},
    
    # Bloque 4: Igualdad y Derechos
    {"boe_id": "BOE-A-2007-6115", "nombre": "LO 3/2007 Igualdad Mujeres Hombres"},
    {"boe_id": "BOE-A-2004-21760", "nombre": "LO 1/2004 Violencia de Género"},
    {"boe_id": "BOE-A-2023-5366", "nombre": "Ley 4/2023 LGTBI"},
    {"boe_id": "BOE-A-2006-21990", "nombre": "Ley 39/2006 Dependencia"},
    {"boe_id": "BOE-A-2013-12632", "nombre": "RDL 1/2013 Derechos Discapacidad"},
    
    # Bloque 5: Protección de Datos
    # RGPD no está en BOE (EUR-Lex) - se marca para descarga manual
    {"boe_id": "BOE-A-2018-16673", "nombre": "LO 3/2018 LOPDGDD"},
    
    # Bloque 6: Transparencia y Administración Electrónica
    {"boe_id": "BOE-A-2013-12887", "nombre": "Ley 19/2013 Transparencia"},
    {"boe_id": "BOE-A-2007-12352", "nombre": "Ley 11/2007 Acceso Electrónico"},
    {"boe_id": "BOE-A-2010-1330", "nombre": "RD 3/2010 ENI"},
    {"boe_id": "BOE-A-2010-1331", "nombre": "RD 4/2010 ENS"},  # Corregido: ENS es RD 4/2010
    
    # Bloque 7: Contratos y Subvenciones
    {"boe_id": "BOE-A-2017-12902", "nombre": "Ley 9/2017 Contratos Sector Público"},
    {"boe_id": "BOE-A-2003-20977", "nombre": "Ley 38/2003 General Subvenciones"},
    {"boe_id": "BOE-A-2006-13371", "nombre": "RD 887/2006 Reglamento Subvenciones"},
    
    # Bloque 8: Presupuestos y Tribunal de Cuentas
    {"boe_id": "BOE-A-2003-21614", "nombre": "Ley 47/2003 General Presupuestaria"},
    {"boe_id": "BOE-A-2012-5730", "nombre": "LO 2/2012 Estabilidad Presupuestaria"},
    {"boe_id": "BOE-A-1982-9050", "nombre": "LO 2/1982 Tribunal de Cuentas"},
    {"boe_id": "BOE-A-1988-9526", "nombre": "Ley 7/1988 Funcionamiento TC"},
    
    # Bloque 9: Laboral y PRL
    {"boe_id": "BOE-A-2015-11430", "nombre": "Estatuto Trabajadores RDL 2/2015"},
    {"boe_id": "BOE-A-1995-24292", "nombre": "Ley 31/1995 PRL"},
    {"boe_id": "BOE-A-1997-1853", "nombre": "RD 39/1997 Servicios Prevención"},
    {"boe_id": "BOE-A-1999-23945", "nombre": "RD 1971/1999 Accidentes Trabajo"},
    {"boe_id": "BOE-A-2002-18099", "nombre": "Orden TAS/2926/2002 Enfermedades Prof"},
    
    # Bloque 10: SEGURIDAD SOCIAL (CRÍTICO)
    {"boe_id": "BOE-A-2015-11724", "nombre": "LGSS RDL 8/2015"},
    {"boe_id": "BOE-A-1996-4447", "nombre": "RD 84/1996 Afiliación"},
    {"boe_id": "BOE-A-2022-7260", "nombre": "RD 504/2022 Modifica Afiliación"},
    {"boe_id": "BOE-A-1996-1579", "nombre": "RD 2064/1995 Cotización"},
    {"boe_id": "BOE-A-2004-11836", "nombre": "RD 1415/2004 Recaudación"},
    {"boe_id": "BOE-A-1996-1074", "nombre": "RD 1694/1995 Hacienda Patrimonio SS"},
    
    # Incapacidad Temporal y Permanente
    {"boe_id": "BOE-A-2009-5693", "nombre": "RD 1430/2009 Control IT"},
    {"boe_id": "BOE-A-1995-24156", "nombre": "RD 1300/1995 Incapacidades"},
    {"boe_id": "BOE-A-2006-19348", "nombre": "RD 1369/2006 Revisión Incapacidad"},
    {"boe_id": "BOE-A-2001-20795", "nombre": "RD 1415/2001 IP Accidente"},
    
    # Maternidad/Paternidad
    {"boe_id": "BOE-A-2009-3780", "nombre": "RD 295/2009 Maternidad Paternidad"},
    {"boe_id": "BOE-A-2009-15931", "nombre": "Ley 9/2009 Nacimiento Adopción"},
    {"boe_id": "BOE-A-2019-3244", "nombre": "RDL 6/2019 Igualdad Empleo"},
    
    # Pensiones
    {"boe_id": "BOE-A-2024-12124", "nombre": "RDL 11/2024 Mejora Pensiones"},  # ID aproximado
    {"boe_id": "BOE-A-2011-13242", "nombre": "Ley 27/2011 Modernización SS"},
    {"boe_id": "BOE-A-1995-2081", "nombre": "RD 2274/1994 Jubilación Supervivencia"},
    {"boe_id": "BOE-A-2006-16891", "nombre": "RD 1112/2006 Prescripción Caducidad"},
    {"boe_id": "BOE-A-2008-17156", "nombre": "RD 1646/2008 Actualización Pensiones"},
    
    # IMV
    {"boe_id": "BOE-A-2020-6898", "nombre": "RDL 20/2020 IMV Provisional"},
    {"boe_id": "BOE-A-2021-21007", "nombre": "Ley 19/2021 IMV Definitivo"},
    
    # Pensiones No Contributivas
    {"boe_id": "BOE-A-1986-2012", "nombre": "RD 2670/1985 PNC"},
    
    # Regímenes Especiales
    {"boe_id": "BOE-A-1985-22915", "nombre": "RD 2617/1985 Trabajadores Mar"},
    
    # Estructura Ministerial
    {"boe_id": "BOE-A-2023-25411", "nombre": "RD 1009/2023 Estructura Ministerios"},
]

# Directorio de salida
OUTPUT_DIR = "/home/spas/OPOS_GEMINI_1/data/boe_xml"

def download_law(client: BOEApiClient, boe_id: str, nombre: str) -> bool:
    """
    Descarga una ley desde BOE API y la guarda como JSON.
    """
    output_file = os.path.join(OUTPUT_DIR, f"{boe_id}.json")
    
    # Skip si ya existe
    if os.path.exists(output_file):
        logger.info(f"⏭️  {nombre} ya existe, saltando...")
        return True
    
    try:
        logger.info(f"📥 Descargando: {nombre} ({boe_id})...")
        
        # Obtener documento consolidado completo
        doc = client.get_documento_consolidado(boe_id)
        
        if doc and 'error' not in doc:
            # Guardar como JSON con encoding UTF-8
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(doc, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Guardado: {output_file}")
            return True
        else:
            logger.warning(f"⚠️  No se pudo obtener: {nombre}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error descargando {nombre}: {e}")
        return False

def main():
    """
    Descarga todas las leyes del temario.
    """
    # Crear directorio si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    total = len(LEYES_TEMARIO)
    success = 0
    failed = []
    
    logger.info(f"🚀 Iniciando descarga de {total} leyes...")
    
    with BOEApiClient(timeout=60) as client:
        for i, ley in enumerate(LEYES_TEMARIO, 1):
            boe_id = ley["boe_id"]
            nombre = ley["nombre"]
            
            logger.info(f"\n[{i}/{total}] {nombre}")
            
            if download_law(client, boe_id, nombre):
                success += 1
            else:
                failed.append(ley)
            
            # Rate limiting: esperar 1 segundo entre requests
            time.sleep(1)
    
    # Resumen
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 RESUMEN:")
    logger.info(f"   ✅ Descargadas: {success}/{total}")
    logger.info(f"   ❌ Fallidas: {len(failed)}")
    
    if failed:
        logger.info(f"\n📋 Leyes que fallaron:")
        for ley in failed:
            logger.info(f"   - {ley['nombre']} ({ley['boe_id']})")
        
        # Guardar lista de fallidas
        failed_file = os.path.join(OUTPUT_DIR, "_failed_downloads.json")
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump(failed, f, ensure_ascii=False, indent=2)
        logger.info(f"\n💾 Lista de fallidas guardada en: {failed_file}")

if __name__ == "__main__":
    main()
