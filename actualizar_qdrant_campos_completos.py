#!/usr/bin/env python3
"""
Script para actualizar Qdrant con TODOS los campos faltantes del XML
SIN re-ingestar (extrayendo de metadata_xml existente)
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Filter
import re
from typing import List, Dict, Any
from datetime import datetime

print("=" * 80)
print("🔄 ACTUALIZACIÓN QDRANT - TODOS LOS CAMPOS FALTANTES")
print("=" * 80)

# Conectar a Qdrant
client = QdrantClient(url="http://localhost:6333", timeout=120)
COLLECTION = "opositaia_knowledge_FULL_XML"

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def safe_get_text(obj: Any, default: str = '') -> str:
    """Extrae texto de objeto XML"""
    if isinstance(obj, dict):
        return obj.get('_text', obj.get('#text', str(obj)))
    return str(obj) if obj else default

def safe_get_codigo(obj: Any, default: str = '') -> str:
    """Extrae código de objeto XML"""
    if isinstance(obj, dict):
        return obj.get('codigo', default)
    return default

def extract_boe_id(texto: str) -> str:
    """Extrae BOE-A-XXXX del texto"""
    if not texto:
        return ''
    match = re.search(r'BOE-A-\d{4}-\d+', texto)
    return match.group(0) if match else ''

def extract_tipo_referencia(texto: str) -> str:
    """Identifica tipo de referencia"""
    if not texto:
        return 'otra'
    
    texto_lower = texto.lower()
    
    if 'deroga' in texto_lower:
        return 'derogado' if 'derogado' in texto_lower else 'deroga'
    elif 'modifica' in texto_lower:
        return 'modificado' if 'modificado' in texto_lower else 'modifica'
    elif 'añade' in texto_lower:
        return 'añade'
    elif 'sustituye' in texto_lower:
        return 'sustituye'
    elif 'transpone' in texto_lower:
        return 'transpone'
    elif 'desarrolla' in texto_lower:
        return 'desarrolla'
    else:
        return 'otra'

def extract_referencias(refs_obj: Dict, tipo_buscar: str) -> List[str]:
    """Extrae BOE IDs de referencias de un tipo específico"""
    if not refs_obj or 'referencia' not in refs_obj:
        return []
    
    refs = refs_obj['referencia']
    if not isinstance(refs, list):
        refs = [refs]
    
    result = []
    for ref in refs:
        if isinstance(ref, dict):
            texto = safe_get_text(ref)
            tipo = extract_tipo_referencia(texto)
            
            if tipo == tipo_buscar:
                boe_id = extract_boe_id(texto)
                if boe_id and boe_id not in result:
                    result.append(boe_id)
    
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
    
    meta = metadata_xml.get('metadatos', {})
    anal = metadata_xml.get('analisis', {})
    refs = anal.get('referencias', {})
    
    # Referencias anteriores y posteriores
    anteriores = refs.get('anteriores', {})
    posteriores = refs.get('posteriores', {})
    
    # Extraer por tipo
    deroga_a = extract_referencias(anteriores, 'deroga')
    modifica_a = extract_referencias(anteriores, 'modifica')
    añade_a = extract_referencias(anteriores, 'añade')
    sustituye_a = extract_referencias(anteriores, 'sustituye')
    transpone_a = extract_referencias(anteriores, 'transpone')
    desarrolla_a = extract_referencias(anteriores, 'desarrolla')
    
    derogado_por = extract_referencias(posteriores, 'derogado')
    modificado_por = extract_referencias(posteriores, 'modificado')
    añadido_por = extract_referencias(posteriores, 'añade')
    sustituido_por = extract_referencias(posteriores, 'sustituye')
    
    # Construir payload con TODOS los campos
    new_fields = {
        # METADATOS FALTANTES
        'fecha_derogacion': safe_get_text(meta.get('fecha_derogacion', {})),
        'fecha_actualizacion': safe_get_text(meta.get('fecha_actualizacion', {})),
        'estatus_anulacion': safe_get_text(meta.get('estatus_anulacion', {})),
        'vigencia_agotada': safe_get_text(meta.get('vigencia_agotada', {})),
        'ambito': safe_get_text(meta.get('ambito', {})),
        'ambito_codigo': safe_get_codigo(meta.get('ambito', {})),
        'numero_oficial': safe_get_text(meta.get('numero_oficial', {})),
        'diario': safe_get_text(meta.get('diario', {})),
        'diario_numero': safe_get_text(meta.get('diario_numero', {})),
        
        # REFERENCIAS ANTERIORES (qué hace esta ley)
        'deroga_a': deroga_a,
        'modifica_a': modifica_a,
        'añade_a': añade_a,
        'sustituye_a': sustituye_a,
        'transpone_a': transpone_a,
        'desarrolla_a': desarrolla_a,
        
        # REFERENCIAS POSTERIORES (qué le han hecho a esta ley)
        'derogado_por': derogado_por,
        'modificado_por': modificado_por,
        'añadido_por': añadido_por,
        'sustituido_por': sustituido_por,
        
        # NOTAS
        'notas': extract_notas(anal),
        
        # CONTADORES (útiles para queries)
        'num_deroga': len(deroga_a),
        'num_modifica': len(modifica_a),
        'num_derogado_por': len(derogado_por),
        'num_modificado_por': len(modificado_por),
        
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
        
        # Mostrar resumen
        print(f"  Campos nuevos:")
        print(f"    - deroga_a: {len(new_fields['deroga_a'])}")
        print(f"    - modifica_a: {len(new_fields['modifica_a'])}")
        print(f"    - derogado_por: {len(new_fields['derogado_por'])}")
        print(f"    - modificado_por: {len(new_fields['modificado_por'])}")
        print(f"    - notas: {len(new_fields['notas'])}")
        print(f"    - ambito: {new_fields['ambito']}")
        print(f"    - numero_oficial: {new_fields['numero_oficial']}")
        
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
print(f"  Errores: {error_count}")

print("\n📋 CAMPOS AÑADIDOS:")
print("  METADATOS:")
print("    - fecha_derogacion, fecha_actualizacion")
print("    - estatus_anulacion, vigencia_agotada")
print("    - ambito, ambito_codigo")
print("    - numero_oficial, diario, diario_numero")
print("\n  REFERENCIAS ANTERIORES:")
print("    - deroga_a, modifica_a, añade_a")
print("    - sustituye_a, transpone_a, desarrolla_a")
print("\n  REFERENCIAS POSTERIORES:")
print("    - derogado_por, modificado_por")
print("    - añadido_por, sustituido_por")
print("\n  OTROS:")
print("    - notas")
print("    - num_deroga, num_modifica, num_derogado_por, num_modificado_por")
print("    - fecha_actualizacion_payload")

print("\n" + "=" * 80)
