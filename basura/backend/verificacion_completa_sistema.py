"""
VERIFICACIÓN COMPLETA DEL SISTEMA RAG
- Verificar todas las leyes indexadas
- Comprobar mejores prácticas RAG
- Calcular tamaño real de Qdrant
- Validar calidad de indexación
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import os
from pathlib import Path

print("="*80)
print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA RAG OPOSITAIA")
print("="*80)

client = QdrantClient(url="http://localhost:6333")
collection_name = "opositaia_leyes_seguridad_social"

# ============================================================================
# 1. ESTADÍSTICAS GENERALES
# ============================================================================
print("\n" + "="*80)
print("📊 1. ESTADÍSTICAS GENERALES DE LA COLECCIÓN")
print("="*80)

collection_info = client.get_collection(collection_name)
total_points = collection_info.points_count
vector_size = collection_info.config.params.vectors.size
distance = collection_info.config.params.vectors.distance

print(f"\n✅ Colección: {collection_name}")
print(f"📊 Total puntos (chunks): {total_points:,}")
print(f"📏 Dimensión vectores: {vector_size}")
print(f"📐 Métrica de distancia: {distance}")
print(f"🔧 Estado: {collection_info.status}")

# ============================================================================
# 2. DISTRIBUCIÓN POR TIPO DE NORMA
# ============================================================================
print("\n" + "="*80)
print("📋 2. DISTRIBUCIÓN POR TIPO DE NORMA")
print("="*80)

all_points = client.scroll(collection_name=collection_name, limit=10000)[0]

tipos = {}
capas = {}
jerarquias = {}

for point in all_points:
    # Por tipo
    tipo = point.payload.get('tipo', 'unknown')
    if tipo not in tipos:
        tipos[tipo] = 0
    tipos[tipo] += 1
    
    # Por capa
    capa = point.payload.get('layer', 'unknown')
    if capa not in capas:
        capas[capa] = 0
    capas[capa] += 1
    
    # Por jerarquía
    jerarquia = point.payload.get('nivel_jerarquia', 'unknown')
    if jerarquia not in jerarquias:
        jerarquias[jerarquia] = 0
    jerarquias[jerarquia] += 1

print(f"\n📊 Por tipo de norma:")
for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
    porcentaje = (count / total_points) * 100
    print(f"   {tipo:20s}: {count:5,} chunks ({porcentaje:5.2f}%)")

print(f"\n📊 Por capa:")
for capa, count in sorted(capas.items()):
    porcentaje = (count / total_points) * 100
    print(f"   Capa {capa}: {count:5,} chunks ({porcentaje:5.2f}%)")

print(f"\n📊 Por nivel jerárquico:")
for jerarquia, count in sorted(jerarquias.items()):
    porcentaje = (count / total_points) * 100
    nivel_nombre = {1: "Constitución/Leyes", 2: "Reglamentos", "unknown": "Materiales"}
    print(f"   Nivel {jerarquia} ({nivel_nombre.get(jerarquia, 'Otros')}): {count:5,} chunks ({porcentaje:5.2f}%)")

# ============================================================================
# 3. LEYES INDEXADAS (CAPA 1)
# ============================================================================
print("\n" + "="*80)
print("📚 3. LEYES INDEXADAS (CAPA 1 - NORMATIVA)")
print("="*80)

normas = {}
for point in all_points:
    if point.payload.get('layer') == 1:
        norma = point.payload.get('norma_nombre', 'unknown')
        if norma not in normas:
            normas[norma] = {
                'chunks': 0,
                'articulos': set(),
                'tipo': point.payload.get('tipo', 'unknown'),
                'nombre_completo': point.payload.get('norma_completa', norma),
                'boe_id': point.payload.get('boe_id', 'N/A')
            }
        normas[norma]['chunks'] += 1
        art = point.payload.get('articulo')
        if art:
            normas[norma]['articulos'].add(art)

print(f"\n✅ Total leyes indexadas: {len(normas)}")
print(f"\n{'Norma':<40} {'Chunks':>8} {'Arts':>6} {'Tipo':<15} {'BOE ID':<20}")
print("-" * 100)

for norma, info in sorted(normas.items(), key=lambda x: x[1]['chunks'], reverse=True):
    nombre = info['nombre_completo'][:38]
    print(f"{nombre:<40} {info['chunks']:>8,} {len(info['articulos']):>6} {info['tipo']:<15} {info['boe_id']:<20}")

total_chunks_capa1 = sum(info['chunks'] for info in normas.values())
total_articulos = sum(len(info['articulos']) for info in normas.values())
print("-" * 100)
print(f"{'TOTAL':<40} {total_chunks_capa1:>8,} {total_articulos:>6}")

# ============================================================================
# 4. VERIFICACIÓN DE MEJORES PRÁCTICAS RAG
# ============================================================================
print("\n" + "="*80)
print("✅ 4. VERIFICACIÓN DE MEJORES PRÁCTICAS RAG")
print("="*80)

# 4.1 Tamaño de chunks
chunk_sizes = []
for point in all_points[:100]:  # Muestra de 100
    content = point.payload.get('content', '')
    chunk_sizes.append(len(content))

avg_chunk_size = sum(chunk_sizes) / len(chunk_sizes) if chunk_sizes else 0
min_chunk_size = min(chunk_sizes) if chunk_sizes else 0
max_chunk_size = max(chunk_sizes) if chunk_sizes else 0

print(f"\n📏 Tamaño de chunks (muestra de 100):")
print(f"   Promedio: {avg_chunk_size:.0f} caracteres")
print(f"   Mínimo: {min_chunk_size} caracteres")
print(f"   Máximo: {max_chunk_size} caracteres")
print(f"   ✅ Recomendado: 500-2000 caracteres")

if 500 <= avg_chunk_size <= 2000:
    print(f"   ✅ CORRECTO: Tamaño promedio dentro del rango óptimo")
else:
    print(f"   ⚠️  ADVERTENCIA: Tamaño promedio fuera del rango óptimo")

# 4.2 Metadata completa
metadata_completa = 0
metadata_incompleta = 0

campos_requeridos = ['content', 'layer', 'tipo', 'norma_nombre']

for point in all_points[:100]:  # Muestra de 100
    tiene_todos = all(point.payload.get(campo) for campo in campos_requeridos)
    if tiene_todos:
        metadata_completa += 1
    else:
        metadata_incompleta += 1

print(f"\n📋 Metadata:")
print(f"   Completa: {metadata_completa}/100")
print(f"   Incompleta: {metadata_incompleta}/100")

if metadata_completa >= 95:
    print(f"   ✅ EXCELENTE: >95% de chunks con metadata completa")
elif metadata_completa >= 80:
    print(f"   ✅ BUENO: >80% de chunks con metadata completa")
else:
    print(f"   ⚠️  MEJORABLE: <80% de chunks con metadata completa")

# 4.3 Distribución de capas
print(f"\n🔄 Reranking jerárquico:")
capa1_percent = (capas.get(1, 0) / total_points) * 100
capa3_percent = (capas.get(3, 0) / total_points) * 100

print(f"   Capa 1 (Normativa): {capa1_percent:.1f}%")
print(f"   Capa 3 (Materiales): {capa3_percent:.1f}%")

if 20 <= capa1_percent <= 40:
    print(f"   ✅ CORRECTO: Balance adecuado entre normativa y materiales")
else:
    print(f"   ⚠️  ADVERTENCIA: Desbalance entre capas")

# 4.4 Detección de artículos
articulos_detectados = sum(1 for p in all_points[:100] if p.payload.get('articulo'))
print(f"\n🔍 Detección de artículos:")
print(f"   Detectados: {articulos_detectados}/100 (muestra)")
print(f"   Porcentaje: {articulos_detectados}%")

if articulos_detectados >= 40:
    print(f"   ✅ BUENO: Alta tasa de detección de artículos")
elif articulos_detectados >= 20:
    print(f"   ✅ ACEPTABLE: Tasa moderada de detección")
else:
    print(f"   ⚠️  MEJORABLE: Baja tasa de detección de artículos")

# ============================================================================
# 5. TAMAÑO REAL DE QDRANT
# ============================================================================
print("\n" + "="*80)
print("💾 5. TAMAÑO REAL DE QDRANT")
print("="*80)

# Calcular tamaño estimado
# Cada vector: 768 floats * 4 bytes = 3,072 bytes
# Metadata promedio: ~500 bytes por chunk
# Total por chunk: ~3,572 bytes

bytes_por_vector = vector_size * 4  # 4 bytes por float32
bytes_metadata_promedio = 500
bytes_por_chunk = bytes_por_vector + bytes_metadata_promedio

tamaño_estimado_bytes = total_points * bytes_por_chunk
tamaño_estimado_mb = tamaño_estimado_bytes / (1024 * 1024)
tamaño_estimado_gb = tamaño_estimado_mb / 1024

print(f"\n📊 Cálculo estimado:")
print(f"   Bytes por vector: {bytes_por_vector:,} bytes")
print(f"   Bytes metadata (promedio): {bytes_metadata_promedio:,} bytes")
print(f"   Bytes por chunk: {bytes_por_chunk:,} bytes")
print(f"   Total chunks: {total_points:,}")
print(f"\n💾 Tamaño estimado:")
print(f"   {tamaño_estimado_bytes:,} bytes")
print(f"   {tamaño_estimado_mb:.2f} MB")
print(f"   {tamaño_estimado_gb:.4f} GB")

# Comparar con Free Tier de Qdrant Cloud
free_tier_gb = 1.0
uso_porcentaje = (tamaño_estimado_gb / free_tier_gb) * 100

print(f"\n☁️  Qdrant Cloud Free Tier:")
print(f"   Límite: {free_tier_gb} GB")
print(f"   Uso estimado: {uso_porcentaje:.2f}%")
print(f"   Margen disponible: {(free_tier_gb - tamaño_estimado_gb)*1024:.2f} MB")

if uso_porcentaje < 50:
    print(f"   ✅ EXCELENTE: Amplio margen disponible")
elif uso_porcentaje < 80:
    print(f"   ✅ BUENO: Margen suficiente")
elif uso_porcentaje < 95:
    print(f"   ⚠️  ADVERTENCIA: Acercándose al límite")
else:
    print(f"   🚨 CRÍTICO: Muy cerca o sobre el límite")

# ============================================================================
# 6. RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("🎯 6. RESUMEN FINAL DE VERIFICACIÓN")
print("="*80)

print(f"\n✅ SISTEMA RAG OPOSITAIA - ESTADO GENERAL")
print(f"\n📊 Contenido:")
print(f"   Total chunks: {total_points:,}")
print(f"   Leyes indexadas: {len(normas)}")
print(f"   Artículos detectados: {total_articulos:,}")
print(f"   Capa 1 (Normativa): {capas.get(1, 0):,} chunks ({capa1_percent:.1f}%)")
print(f"   Capa 3 (Materiales): {capas.get(3, 0):,} chunks ({capa3_percent:.1f}%)")

print(f"\n💾 Almacenamiento:")
print(f"   Tamaño estimado: {tamaño_estimado_mb:.2f} MB ({tamaño_estimado_gb:.4f} GB)")
print(f"   Uso Free Tier: {uso_porcentaje:.2f}%")
print(f"   Margen: {(free_tier_gb - tamaño_estimado_gb)*1024:.2f} MB")

print(f"\n✅ Mejores prácticas RAG:")
print(f"   Tamaño chunks: {'✅ CORRECTO' if 500 <= avg_chunk_size <= 2000 else '⚠️  MEJORABLE'}")
print(f"   Metadata completa: {'✅ EXCELENTE' if metadata_completa >= 95 else '✅ BUENO' if metadata_completa >= 80 else '⚠️  MEJORABLE'}")
print(f"   Balance capas: {'✅ CORRECTO' if 20 <= capa1_percent <= 40 else '⚠️  ADVERTENCIA'}")
print(f"   Detección artículos: {'✅ BUENO' if articulos_detectados >= 40 else '✅ ACEPTABLE' if articulos_detectados >= 20 else '⚠️  MEJORABLE'}")

print(f"\n🎉 VEREDICTO FINAL:")
if uso_porcentaje < 80 and metadata_completa >= 80 and 500 <= avg_chunk_size <= 2000:
    print(f"   ✅ SISTEMA EN ÓPTIMAS CONDICIONES")
    print(f"   ✅ Listo para producción")
    print(f"   ✅ Siguiendo mejores prácticas RAG")
else:
    print(f"   ✅ SISTEMA OPERATIVO")
    print(f"   ⚠️  Algunas áreas mejorables")

print("="*80)
