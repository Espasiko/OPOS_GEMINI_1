#!/usr/bin/env python3
"""
Script CORREGIDO con TIMEOUT MÁXIMO para actualizar Qdrant
Solo procesa las leyes que fallaron (23-54)
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Filter
import re
from typing import List, Dict, Any
from datetime import datetime

print("=" * 80)
print("🔄 ACTUALIZACIÓN QDRANT - REINTENTO LEYES FALLIDAS (TIMEOUT 600s)")
print("=" * 80)

# Conectar a Qdrant con TIMEOUT MÁXIMO
client = QdrantClient(url="http://localhost:6333", timeout=600)  # 10 MINUTOS
COLLECTION = "opositaia_knowledge_FULL_XML"

# Leyes que fallaron (23-54)
LEYES_FALLIDAS = [
    "BOE-A-2003-21614", "BOE-A-2004-11836", "BOE-A-2004-21760",
    "BOE-A-2006-13371", "BOE-A-2006-21239", "BOE-A-2006-21990",
    "BOE-A-2007-12352", "BOE-A-2007-6115", "BOE-A-2009-15442",
    "BOE-A-2009-15931", "BOE-A-2009-4724", "BOE-A-2010-1330",
    "BOE-A-2010-1331", "BOE-A-2011-13242", "BOE-A-2012-5730",
    "BOE-A-2013-12632", "BOE-A-2013-12887", "BOE-A-2013-13756",
    "BOE-A-2015-10565", "BOE-A-2015-10566", "BOE-A-2015-11430",
    "BOE-A-2015-11719", "BOE-A-2015-11724", "BOE-A-2017-12902",
    "BOE-A-2018-16673", "BOE-A-2019-3244", "BOE-A-2020-5493",
    "BOE-A-2021-21007", "BOE-A-2022-10677", "BOE-A-2023-24842",
    "BOE-A-2023-5366", "BOE-A-2024-26917"
]

# ============================================================================
# FUNCIONES AUXILIARES (MISMAS QUE ANTES)
# ============================================================================

def safe_get_text(obj: Any, default: str = '') -> str:
    if isinstance(obj, dict):
        return obj.get('_text', obj.get('#text', str(obj)))
    return str(obj) if obj else default

def extract_boe_id_from_ref(ref: Dict) -> str:
    if not isinstance(ref, dict):
        return ''
    id_norma = ref.get('id_norma', {})
    if id_norma:
        boe_id = safe_get_text(id_norma)
        if boe_id and boe_id.startswith('BOE-A-'):
            return boe_id
    texto = ref.get('texto', {})
    texto_str = safe_get_text(texto)
    match = re.search(r'BOE-A-\d{4}-\d+', texto_str)
    return match.group(0) if match else ''

def get_relacion_tipo(ref: Dict) -> str:
    if not isinstance(ref, dict):
        return ''
    relacion = ref.get('relacion', {})
    if relacion:
        return safe_get_text(relacion).upper()
    return ''

def extract_referencias_anteriores(anteriores: Dict) -> Dict[str, List[str]]:
    result = {
        'deroga_a': [], 'modifica_a': [], 'añade_a': [],
        'sustituye_a': [], 'transpone_a': [], 'desarrolla_a': [],
        'otras_anteriores': []
    }
    if not anteriores or 'anterior' not in anteriores:
        return result
    refs = anteriores['anterior']
    if not isinstance(refs, list):
        refs = [refs]
    for ref in refs:
        boe_id = extract_boe_id_from_ref(ref)
        if not boe_id:
            continue
        relacion = get_relacion_tipo(ref)
        if 'DEROGA' in relacion:
            if boe_id not in result['deroga_a']:
                result['deroga_a'].append(boe_id)
        elif 'MODIFICA' in relacion or 'MODIF' in relacion:
            if boe_id not in result['modifica_a']:
                result['modifica_a'].append(boe_id)
        elif 'AÑADE' in relacion or 'ANADE' in relacion:
            if boe_id not in result['añade_a']:
                result['añade_a'].append(boe_id)
        elif 'SUSTITUYE' in relacion:
            if boe_id not in result['sustituye_a']:
                result['sustituye_a'].append(boe_id)
        elif 'TRANSPONE' in relacion:
            if boe_id not in result['transpone_a']:
                result['transpone_a'].append(boe_id)
        elif 'DESARROLLA' in relacion:
            if boe_id not in result['desarrolla_a']:
                result['desarrolla_a'].append(boe_id)
        else:
            if boe_id not in result['otras_anteriores']:
                result['otras_anteriores'].append(boe_id)
    return result

def extract_referencias_posteriores(posteriores: Dict) -> Dict[str, List[str]]:
    result = {
        'derogado_por': [], 'modificado_por': [],
        'añadido_por': [], 'sustituido_por': [],
        'otras_posteriores': []
    }
    if not posteriores or 'posterior' not in posteriores:
        return result
    refs = posteriores['posterior']
    if not isinstance(refs, list):
        refs = [refs]
    for ref in refs:
        boe_id = extract_boe_id_from_ref(ref)
        if not boe_id:
            continue
        relacion = get_relacion_tipo(ref)
        if 'DEROGA' in relacion:
            if boe_id not in result['derogado_por']:
                result['derogado_por'].append(boe_id)
        elif 'MODIFICA' in relacion or 'MODIF' in relacion:
            if boe_id not in result['modificado_por']:
                result['modificado_por'].append(boe_id)
        elif 'AÑADE' in relacion or 'ANADE' in relacion:
            if boe_id not in result['añadido_por']:
                result['añadido_por'].append(boe_id)
        elif 'SUSTITUYE' in relacion:
            if boe_id not in result['sustituido_por']:
                result['sustituido_por'].append(boe_id)
        else:
            if boe_id not in result['otras_posteriores']:
                result['otras_posteriores'].append(boe_id)
    return result

def extract_notas(anal: Dict) -> List[str]:
    if not anal or 'notas' not in anal:
        return []
    notas_obj = anal['notas']
    if not notas_obj or 'nota' not in notas_obj:
        return []
    notas = notas_obj['nota']
    if not isinstance(notas, list):
        notas = [notas]
    return [safe_get_text(n) for n in notas if n]

def build_new_fields(metadata_xml: Dict) -> Dict:
    data = metadata_xml.get('data', metadata_xml)
    meta = data.get('metadatos', {})
    anal = data.get('analisis', {})
    refs = anal.get('referencias', {})
    anteriores = refs.get('anteriores', {})
    posteriores = refs.get('posteriores', {})
    refs_ant = extract_referencias_anteriores(anteriores)
    refs_post = extract_referencias_posteriores(posteriores)
    new_fields = {
        'fecha_derogacion': safe_get_text(meta.get('fecha_derogacion', {})),
        'fecha_actualizacion': safe_get_text(meta.get('fecha_actualizacion', {})),
        'estatus_anulacion': safe_get_text(meta.get('estatus_anulacion', {})),
        'vigencia_agotada': safe_get_text(meta.get('vigencia_agotada', {})),
        'ambito': safe_get_text(meta.get('ambito', {})),
        'ambito_codigo': meta.get('ambito', {}).get('codigo', '') if isinstance(meta.get('ambito', {}), dict) else '',
        'numero_oficial': safe_get_text(meta.get('numero_oficial', {})),
        'diario': safe_get_text(meta.get('diario', {})),
        'diario_numero': safe_get_text(meta.get('diario_numero', {})),
        'deroga_a': refs_ant['deroga_a'],
        'modifica_a': refs_ant['modifica_a'],
        'añade_a': refs_ant['añade_a'],
        'sustituye_a': refs_ant['sustituye_a'],
        'transpone_a': refs_ant['transpone_a'],
        'desarrolla_a': refs_ant['desarrolla_a'],
        'otras_anteriores': refs_ant['otras_anteriores'],
        'derogado_por': refs_post['derogado_por'],
        'modificado_por': refs_post['modificado_por'],
        'añadido_por': refs_post['añadido_por'],
        'sustituido_por': refs_post['sustituido_por'],
        'otras_posteriores': refs_post['otras_posteriores'],
        'notas': extract_notas(anal),
        'num_deroga': len(refs_ant['deroga_a']),
        'num_modifica': len(refs_ant['modifica_a']),
        'num_derogado_por': len(refs_post['derogado_por']),
        'num_modificado_por': len(refs_post['modificado_por']),
        'fecha_actualizacion_payload': datetime.now().isoformat()
    }
    return new_fields

# ============================================================================
# PROCESO PRINCIPAL
# ============================================================================

print(f"\n📊 Procesando {len(LEYES_FALLIDAS)} leyes fallidas...")
print("-" * 80)

updated_count = 0
error_count = 0
leyes_con_referencias = 0

for i, boe_id in enumerate(LEYES_FALLIDAS, 1):
    try:
        print(f"\n[{i}/{len(LEYES_FALLIDAS)}] {boe_id}")
        
        result = client.scroll(
            collection_name=COLLECTION,
            scroll_filter={
                "must": [{"key": "boe_id", "match": {"value": boe_id}}]
            },
            limit=1,
            with_payload=True
        )
        
        if not result[0]:
            print(f"  ⚠️  No se encontraron chunks")
            continue
        
        point = result[0][0]
        metadata_xml = point.payload.get('metadata_xml', {})
        
        if not metadata_xml:
            print(f"  ⚠️  Sin metadata_xml")
            continue
        
        new_fields = build_new_fields(metadata_xml)
        
        total_refs = (new_fields['num_deroga'] + new_fields['num_modifica'] + 
                     new_fields['num_derogado_por'] + new_fields['num_modificado_por'])
        
        if total_refs > 0:
            leyes_con_referencias += 1
        
        print(f"  Campos nuevos:")
        print(f"    - deroga_a: {new_fields['num_deroga']}")
        print(f"    - modifica_a: {len(new_fields['modifica_a'])}")
        print(f"    - derogado_por: {new_fields['num_derogado_por']}")
        print(f"    - modificado_por: {new_fields['num_modificado_por']}")
        print(f"    - notas: {len(new_fields['notas'])}")
        
        client.set_payload(
            collection_name=COLLECTION,
            payload=new_fields,
            points=Filter(
                must=[{"key": "boe_id", "match": {"value": boe_id}}]
            )
        )
        
        updated_count += 1
        print(f"  ✅ Actualizado")
        
    except Exception as e:
        error_count += 1
        print(f"  ❌ Error: {e}")

print("\n\n" + "=" * 80)
print("✅ ACTUALIZACIÓN COMPLETA")
print("=" * 80)
print(f"\n  Leyes procesadas: {len(LEYES_FALLIDAS)}")
print(f"  Actualizadas: {updated_count}")
print(f"  Leyes CON referencias: {leyes_con_referencias}")
print(f"  Errores: {error_count}")
print("\n" + "=" * 80)
