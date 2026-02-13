#!/usr/bin/env python3
"""
Script CORREGIDO para actualizar Qdrant con referencias del BOE
PROBLEMA IDENTIFICADO: Los XMLs usan 'anterior' y 'posterior', NO 'referencia'
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Filter
import re
from typing import List, Dict, Any
from datetime import datetime

print("=" * 80)
print("🔄 ACTUALIZACIÓN QDRANT - REFERENCIAS CORREGIDAS")
print("=" * 80)

# Conectar a Qdrant
client = QdrantClient(url="http://localhost:6333", timeout=120)
COLLECTION = "opositaia_knowledge_FULL_XML"

# ============================================================================
# FUNCIONES AUXILIARES CORREGIDAS
# ============================================================================

def safe_get_text(obj: Any, default: str = '') -> str:
    """Extrae texto de objeto XML"""
    if isinstance(obj, dict):
        return obj.get('_text', obj.get('#text', str(obj)))
    return str(obj) if obj else default

def extract_boe_id_from_ref(ref: Dict) -> str:
    """Extrae BOE-A-XXXX de una referencia"""
    if not isinstance(ref, dict):
        return ''
    
    # Primero intentar con id_norma
    id_norma = ref.get('id_norma', {})
    if id_norma:
        boe_id = safe_get_text(id_norma)
        if boe_id and boe_id.startswith('BOE-A-'):
            return boe_id
    
    # Si no, buscar en el texto
    texto = ref.get('texto', {})
    texto_str = safe_get_text(texto)
    match = re.search(r'BOE-A-\d{4}-\d+', texto_str)
    return match.group(0) if match else ''

def get_relacion_tipo(ref: Dict) -> str:
    """Obtiene el tipo de relación"""
    if not isinstance(ref, dict):
        return ''
    
    relacion = ref.get('relacion', {})
    if relacion:
        return safe_get_text(relacion).upper()
    return ''

def extract_referencias_anteriores(anteriores: Dict) -> Dict[str, List[str]]:
    """Extrae referencias anteriores clasificadas por tipo"""
    result = {
        'deroga_a': [],
        'modifica_a': [],
        'añade_a': [],
        'sustituye_a': [],
        'transpone_a': [],
        'desarrolla_a': [],
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
    """Extrae referencias posteriores clasificadas por tipo"""
    result = {
        'derogado_por': [],
        'modificado_por': [],
        'añadido_por': [],
        'sustituido_por': [],
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
    """Extrae notas del análisis"""
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
    """Construye TODOS los campos nuevos desde metadata_xml"""
    
    # IMPORTANTE: Los XMLs tienen estructura data.metadatos y data.analisis
    data = metadata_xml.get('data', metadata_xml)  # Soporte para ambas estructuras
    
    meta = data.get('metadatos', {})
    anal = data.get('analisis', {})
    refs = anal.get('referencias', {})
    
    # Referencias anteriores y posteriores
    anteriores = refs.get('anteriores', {})
    posteriores = refs.get('posteriores', {})
    
    # Extraer por tipo
    refs_ant = extract_referencias_anteriores(anteriores)
    refs_post = extract_referencias_posteriores(posteriores)
    
    # Construir payload con TODOS los campos
    new_fields = {
        # METADATOS FALTANTES
        'fecha_derogacion': safe_get_text(meta.get('fecha_derogacion', {})),
        'fecha_actualizacion': safe_get_text(meta.get('fecha_actualizacion', {})),
        'estatus_anulacion': safe_get_text(meta.get('estatus_anulacion', {})),
        'vigencia_agotada': safe_get_text(meta.get('vigencia_agotada', {})),
        'ambito': safe_get_text(meta.get('ambito', {})),
        'ambito_codigo': meta.get('ambito', {}).get('codigo', '') if isinstance(meta.get('ambito', {}), dict) else '',
        'numero_oficial': safe_get_text(meta.get('numero_oficial', {})),
        'diario': safe_get_text(meta.get('diario', {})),
        'diario_numero': safe_get_text(meta.get('diario_numero', {})),
        
        # REFERENCIAS ANTERIORES (qué hace esta ley)
        'deroga_a': refs_ant['deroga_a'],
        'modifica_a': refs_ant['modifica_a'],
        'añade_a': refs_ant['añade_a'],
        'sustituye_a': refs_ant['sustituye_a'],
        'transpone_a': refs_ant['transpone_a'],
        'desarrolla_a': refs_ant['desarrolla_a'],
        'otras_anteriores': refs_ant['otras_anteriores'],
        
        # REFERENCIAS POSTERIORES (qué le han hecho a esta ley)
        'derogado_por': refs_post['derogado_por'],
        'modificado_por': refs_post['modificado_por'],
        'añadido_por': refs_post['añadido_por'],
        'sustituido_por': refs_post['sustituido_por'],
        'otras_posteriores': refs_post['otras_posteriores'],
        
        # NOTAS
        'notas': extract_notas(anal),
        
        # CONTADORES (útiles para queries)
        'num_deroga': len(refs_ant['deroga_a']),
        'num_modifica': len(refs_ant['modifica_a']),
        'num_derogado_por': len(refs_post['derogado_por']),
        'num_modificado_por': len(refs_post['modificado_por']),
        
        # TIMESTAMP DE ACTUALIZACIÓN
        'fecha_actualizacion_payload': datetime.now().isoformat()
    }
    
    return new_fields

# ============================================================================
# PROCESO PRINCIPAL
# ============================================================================

print("\n📊 Obteniendo leyes únicas...")

# Obtener todas las leyes únicas
all_boe_ids = set()
offset = None
batch_count = 0

while True:
    batch_count += 1
    print(f"  Batch {batch_count}...", end="\r")
    
    result = client.scroll(
        collection_name=COLLECTION,
        limit=1000,
        offset=offset,
        with_payload=["boe_id"]
    )
    
    points, next_offset = result
    
    if not points:
        break
    
    for point in points:
        all_boe_ids.add(point.payload['boe_id'])
    
    if next_offset is None:
        break
    
    offset = next_offset

print(f"\n✅ Total leyes únicas: {len(all_boe_ids)}")

# Procesar cada ley
print("\n🔄 Actualizando payloads...")
print("-" * 80)

updated_count = 0
error_count = 0
leyes_con_referencias = 0

for i, boe_id in enumerate(sorted(all_boe_ids), 1):
    try:
        print(f"\n[{i}/{len(all_boe_ids)}] {boe_id}")
        
        # Obtener UN chunk de esta ley (metadata_xml es igual para todos)
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
        
        # Construir nuevos campos
        new_fields = build_new_fields(metadata_xml)
        
        # Contar referencias
        total_refs = (new_fields['num_deroga'] + new_fields['num_modifica'] + 
                     new_fields['num_derogado_por'] + new_fields['num_modificado_por'])
        
        if total_refs > 0:
            leyes_con_referencias += 1
        
        # Mostrar resumen
        print(f"  Campos nuevos:")
        print(f"    - deroga_a: {new_fields['num_deroga']}")
        print(f"    - modifica_a: {len(new_fields['modifica_a'])}")
        print(f"    - derogado_por: {new_fields['num_derogado_por']}")
        print(f"    - modificado_por: {new_fields['num_modificado_por']}")
        print(f"    - notas: {len(new_fields['notas'])}")
        print(f"    - ambito: {new_fields['ambito']}")
        
        # Actualizar TODOS los chunks de esta ley
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

# Resumen final
print("\n\n" + "=" * 80)
print("✅ ACTUALIZACIÓN COMPLETA")
print("=" * 80)
print(f"\n  Leyes procesadas: {len(all_boe_ids)}")
print(f"  Actualizadas: {updated_count}")
print(f"  Leyes CON referencias: {leyes_con_referencias}")
print(f"  Leyes SIN referencias: {updated_count - leyes_con_referencias}")
print(f"  Errores: {error_count}")

print("\n📋 CAMPOS AÑADIDOS:")
print("  METADATOS:")
print("    - fecha_derogacion, fecha_actualizacion")
print("    - estatus_anulacion, vigencia_agotada")
print("    - ambito, ambito_codigo")
print("    - numero_oficial, diario, diario_numero")
print("\n  REFERENCIAS ANTERIORES:")
print("    - deroga_a, modifica_a, añade_a")
print("    - sustituye_a, transpone_a, desarrolla_a, otras_anteriores")
print("\n  REFERENCIAS POSTERIORES:")
print("    - derogado_por, modificado_por")
print("    - añadido_por, sustituido_por, otras_posteriores")
print("\n  OTROS:")
print("    - notas")
print("    - num_deroga, num_modifica, num_derogado_por, num_modificado_por")
print("    - fecha_actualizacion_payload")

print("\n" + "=" * 80)
