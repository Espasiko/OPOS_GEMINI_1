import json
import traceback

catalog_path = '/home/spas/OPOS_GEMINI_1/backend/data/catalog_v17.json'
out_md = '/home/spas/OPOS_GEMINI_1/13_04_REPORTE_AUDITORIA_NEO4J_GEMINI.md'

try:
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    print(f'Catalog loaded. Type: {type(catalog)}')
    if isinstance(catalog, dict) and 'leyes' in catalog:
        leyes = catalog['leyes']
    elif isinstance(catalog, list):
        leyes = catalog
    else:
        leyes = []
        
    print(f'Leyes encontradas: {len(leyes)}')
    
    with open(out_md, 'w', encoding='utf-8') as fout:
        fout.write('# 🛡️ REPORTE AUDITORÍA NEO4J GEMINI - NOMBRES COMPLETOS\n\n')
        fout.write('**ESTE REPORTE REFLEJA EL ESTADO DEL CATÁLOGO (v17.3) QUE SERÁ INGESTADO.**\n')
        fout.write('⚠️ NO SE HA INGESTADO NINGÚN DATO EN NEO4J.\n')
        fout.write('⚠️ NO HAS PERDIDO TUS DATOS. ESTO SOLO ES UN REPORTE VISUAL.\n\n')
        
        fout.write('## NOTAS METODOLÓGICAS DE INGESTA (TUS PREGUNTAS RESUELTAS)\n')
        fout.write('- **Sobre Neo4j:** NO he modificado absoltumente NADA en la base de datos de Neo4j. Todo se generará cuando tú lo ordenes.\n')
        fout.write('- **Script y Jerarquías (LO 3/1980 / 0 preceptos):** El script que vamos a usar (`ingest_neo4j_v17.py`) implementa un _fallback_: Si la ley no tiene versión consolidada XML, acude al endpoint del diario (`buscar/xml.php`) que es donde se encuentra el XML original. Usamos `BOEParser._parse_xml_documento` para capturar la etiqueta `<p class="articulo">`, reconstruyendo los preceptos de leyes "planitas". Se indexarán chunks de máx 20.000 chars con solapamiento, conectando el índice Vectorial Nativo de Cypher 5.\n\n')
        
        fout.write('## VERIFICACIÓN DE LEYES Y TÍTULOS COMPLETOS\n')
        fout.write('| BOE ID | SIGLAS (ALIAS) | TÍTULO COMPLETO OFICIAL (CATÁLOGO) | ESTADO/NOTAS |\n')
        fout.write('|---|---|---|---|\n')
        
        for ley in leyes:
            bid = ley.get('boe_id', '???')
            siglas = ley.get('siglas', '???')
            titulo = ley.get('titulo', '???')
            # Hardcodear la nota que el script anterior detectó de la API HTTP 
            nota = '⚠️ MODIFICADA RECIENTEMENTE (post-corte examen)' if bid == 'BOE-A-2026-7296' else '✅ OK - Sin modificaciones recientes'
            if bid in ['BOE-A-1963-22667', 'BOE-A-1972-907', 'BOE-A-1985-16119', 'BOE-A-2007-8350', 'BOE-A-2013-2309', 'BOE-A-1980-8648']:
                nota = '📜 Histórica/No Consolidada (Ingestión vía diario original fallback)'
                
            fout.write(f'| `{bid}` | {siglas} | **{titulo}** | {nota} |\n')
            
    print('Reporte MD generado exitosamente.')
except Exception as e:
    print('Error:', traceback.format_exc())
