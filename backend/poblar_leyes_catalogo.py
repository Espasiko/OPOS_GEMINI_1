#!/usr/bin/env python3
"""
SCRIPT DE POBLACIÓN DE TABLA leyes_catalogo
============================================
Consulta API BOE y puebla tabla con metadata completa:
- Metadatos (fechas, organismo, URLs)
- Análisis (modificaciones, afectaciones)
- Índice de artículos (desde EPUB o API)
"""

import requests
import psycopg2
import json
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

# Configuración
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'opositaia'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# Leyes del temario oficial (TODAS las ingestadas - 27 leyes)
LEYES_TEMARIO = [
    # === CRÍTICAS (Seguridad Social) ===
    {"boe_id": "BOE-A-2015-11724", "nombre_corto": "LGSS"},
    {"boe_id": "BOE-A-1996-4447", "nombre_corto": "RD 84/1996"},
    {"boe_id": "BOE-A-1995-26497", "nombre_corto": "RD 2064/1995"},
    {"boe_id": "BOE-A-2004-11607", "nombre_corto": "RD 1415/2004"},
    {"boe_id": "BOE-A-1996-1579", "nombre_corto": "RD Cotización"},
    {"boe_id": "BOE-A-2004-11836", "nombre_corto": "RD Recaudación"},
    
    # === CONSTITUCIÓN Y AGE ===
    {"boe_id": "BOE-A-1978-31229", "nombre_corto": "Constitución"},
    {"boe_id": "BOE-A-2015-10565", "nombre_corto": "LPACAP"},
    {"boe_id": "BOE-A-2015-10566", "nombre_corto": "LRJSP"},
    {"boe_id": "BOE-A-2015-10438", "nombre_corto": "TREBEP"},
    {"boe_id": "BOE-A-2015-11719", "nombre_corto": "EBEP"},
    {"boe_id": "BOE-A-1979-23709", "nombre_corto": "LOTC"},
    {"boe_id": "BOE-A-1985-12666", "nombre_corto": "LOPJ"},
    {"boe_id": "BOE-A-1997-25336", "nombre_corto": "Ley Gobierno"},
    
    # === ADICIONALES IMPORTANTES ===
    {"boe_id": "BOE-A-2021-21007", "nombre_corto": "Ley IMV"},
    {"boe_id": "BOE-A-2007-6115", "nombre_corto": "Ley Igualdad"},
    {"boe_id": "BOE-A-2004-21760", "nombre_corto": "Ley Violencia Género"},
    {"boe_id": "BOE-A-1995-24292", "nombre_corto": "Ley PRL"},
    {"boe_id": "BOE-A-2015-11430", "nombre_corto": "Estatuto Trabajadores"},
    {"boe_id": "BOE-A-2009-4918", "nombre_corto": "RD Maternidad"},
    
    # === OTRAS LEYES INGESTADAS ===
    {"boe_id": "BOE-A-1985-5392", "nombre_corto": "LBRL"},
    {"boe_id": "BOE-A-2003-20977", "nombre_corto": "LGP"},
    {"boe_id": "BOE-A-2003-21614", "nombre_corto": "Ley 47/2003"},
    {"boe_id": "BOE-A-2017-12902", "nombre_corto": "LCSP"},
    {"boe_id": "BOE-A-2012-5730", "nombre_corto": "LO Estabilidad"},
    {"boe_id": "BOE-A-2023-5366", "nombre_corto": "Ley Igualdad Trans"},
    {"boe_id": "BOE-A-2007-15409", "nombre_corto": "Estatuto Autónomo"},
]

def consultar_metadatos_boe(boe_id):
    """Consulta metadatos de una ley en la API BOE"""
    # URL correcta: XML directo del BOE
    url = f'https://www.boe.es/diario_boe/xml.php?id={boe_id}'
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Parsear XML
            root = ET.fromstring(response.content)
            
            # Extraer campos principales
            metadatos = {}
            
            # Metadatos básicos
            meta_elem = root.find('.//metadatos')
            if meta_elem is not None:
                for child in meta_elem:
                    # Extraer texto y código si existe
                    if child.text:
                        metadatos[child.tag] = child.text.strip()
                    if 'codigo' in child.attrib:
                        metadatos[f'{child.tag}_codigo'] = child.attrib['codigo']
            
            # URLs (si existen en el XML)
            for url_tag in ['url_eli', 'url_pdf', 'url_pdf_consolidado', 'url_epub', 'url_xml', 'url_html']:
                elem = root.find(f'.//{url_tag}')
                if elem is not None and elem.text:
                    metadatos[url_tag] = elem.text.strip()
            
            return metadatos
        else:
            print(f"  ⚠️ Error {response.status_code} consultando metadatos de {boe_id}")
            return None
    except Exception as e:
        print(f"  ❌ Error consultando metadatos: {e}")
        return None

def consultar_analisis_boe(boe_id):
    """Consulta análisis (modificaciones) de una ley - Por ahora retorna vacío"""
    # TODO: Implementar cuando se encuentre el endpoint correcto de análisis
    # Por ahora retornamos estructura vacía
    return {
        'modificaciones': [],
        'afecta_a': [],
        'afectada_por': []
    }

def poblar_ley(conn, ley_info):
    """Puebla una ley en la tabla leyes_catalogo"""
    boe_id = ley_info['boe_id']
    nombre_corto = ley_info['nombre_corto']
    
    print(f"\n{'='*70}")
    print(f"Procesando: {nombre_corto} ({boe_id})")
    print(f"{'='*70}")
    
    # 1. Consultar metadatos
    print("  📥 Consultando metadatos...")
    metadatos = consultar_metadatos_boe(boe_id)
    
    if not metadatos:
        print(f"  ❌ No se pudieron obtener metadatos para {boe_id}")
        return False
    
    # 2. Consultar análisis
    print("  📥 Consultando análisis...")
    analisis = consultar_analisis_boe(boe_id)
    
    # 3. Insertar en BD
    print("  💾 Insertando en BD...")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO leyes_catalogo (
                boe_id,
                nombre_corto,
                titulo,
                tipo_norma,
                departamento_nombre,
                fecha_publicacion,
                fecha_entrada_vigor,
                url_boe,
                url_eli,
                url_pdf,
                url_pdf_consolidado,
                url_xml,
                url_html,
                analisis_modificaciones,
                metadata_xml,
                vigente,
                consolidado,
                created_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (boe_id) DO UPDATE SET
                titulo = EXCLUDED.titulo,
                metadata_xml = EXCLUDED.metadata_xml,
                updated_at = NOW();
        """, (
            boe_id,
            nombre_corto,
            metadatos.get('titulo', ''),
            metadatos.get('tipo', ''),
            metadatos.get('departamento', ''),
            metadatos.get('fecha_publicacion'),
            metadatos.get('fecha_vigencia'),
            f'https://www.boe.es/buscar/doc.php?id={boe_id}',
            metadatos.get('url_eli'),
            metadatos.get('url_pdf'),
            metadatos.get('url_pdf_consolidado'),
            metadatos.get('url_xml'),
            metadatos.get('url_html'),
            json.dumps(analisis.get('modificaciones', []) if analisis else []),
            json.dumps(metadatos),
            True,
            True,
            datetime.now()
        ))
        
        conn.commit()
        print(f"  ✅ {nombre_corto} insertado correctamente")
        return True
        
    except Exception as e:
        print(f"  ❌ Error insertando en BD: {e}")
        conn.rollback()
        return False

def main():
    print("\n" + "="*70)
    print("POBLACIÓN DE TABLA leyes_catalogo")
    print("="*70)
    
    # Conectar a BD
    print("\n📊 Conectando a PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("✅ Conectado")
    
    # Poblar leyes
    total = len(LEYES_TEMARIO)
    exitosas = 0
    
    for i, ley in enumerate(LEYES_TEMARIO, 1):
        print(f"\n[{i}/{total}]")
        if poblar_ley(conn, ley):
            exitosas += 1
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"Total leyes procesadas: {total}")
    print(f"Exitosas: {exitosas}")
    print(f"Fallidas: {total - exitosas}")
    
    conn.close()
    print("\n✅ Proceso completado")

if __name__ == "__main__":
    main()
