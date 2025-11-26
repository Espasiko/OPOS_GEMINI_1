#!/usr/bin/env python3
"""
INDEXAR TODAS LAS LEYES Y REGLAMENTOS EN QDRANT CLOUD
Total: 13 leyes organizadas por prioridad
- 5 Críticas
- 5 Altas  
- 3 Medias

IMPORTANTE: Ejecutar limpiar_qdrant_cloud.py ANTES de este script
"""
import os
import sys
import requests
import pypdf
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
import torch
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
import uuid
import re
import time
from dotenv import load_dotenv

# Cargar variables de entorno
env_path = Path(__file__).parent.parent / '.env.backend'
load_dotenv(env_path)

print("="*80)
print("📚 INDEXACIÓN COMPLETA DE LEYES Y REGLAMENTOS")
print("="*80)
print(f"Total: 13 leyes (5 críticas + 5 altas + 3 medias)")
print("="*80)

# Configuración Qdrant Cloud
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print(f"\n🔌 Configuración:")
print(f"   Qdrant URL: {QDRANT_URL}")
print(f"   Colección: {COLLECTION_NAME}")

# Definir las 13 leyes organizadas por prioridad
LEYES_TODAS = [
    # ========== CRÍTICAS (5) ==========
    {
        "nombre": "LGSS",
        "nombre_completo": "RDL 8/2015 - Ley General Seguridad Social",
        "boe_id": "BOE-A-2015-11724",
        "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-11724-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2015-10-30",
        "prioridad": "critica"
    },
    {
        "nombre": "RD_84_1996",
        "nombre_completo": "RD 84/1996 - Afiliación, Altas y Bajas",
        "boe_id": "BOE-A-1996-3981",
        "url": "https://www.boe.es/buscar/pdf/1996/BOE-A-1996-3981-consolidado.pdf",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "1996-02-26",
        "prioridad": "critica"
    },
    {
        "nombre": "RD_2064_1995",
        "nombre_completo": "RD 2064/1995 - Cotización y Liquidación",
        "boe_id": "BOE-A-1995-26497",
        "url": "https://www.boe.es/buscar/pdf/1995/BOE-A-1995-26497-consolidado.pdf",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "1995-12-22",
        "prioridad": "critica"
    },
    {
        "nombre": "RD_1415_2004",
        "nombre_completo": "RD 1415/2004 - Recaudación",
        "boe_id": "BOE-A-2004-11607",
        "url": "https://www.boe.es/buscar/pdf/2004/BOE-A-2004-11607-consolidado.pdf",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "2004-06-11",
        "prioridad": "critica"
    },
    {
        "nombre": "Constitucion",
        "nombre_completo": "Constitución Española 1978",
        "boe_id": "BOE-A-1978-31229",
        "url": "https://www.boe.es/buscar/pdf/1978/BOE-A-1978-31229-consolidado.pdf",
        "tipo": "constitucion",
        "nivel_jerarquia": 0,
        "fecha": "1978-12-29",
        "prioridad": "critica"
    },
    
    # ========== ALTAS (5) ==========
    {
        "nombre": "Ley_39_2015",
        "nombre_completo": "Ley 39/2015 - Procedimiento Administrativo Común",
        "boe_id": "BOE-A-2015-10565",
        "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-10565-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2015-10-01",
        "prioridad": "alta"
    },
    {
        "nombre": "Ley_40_2015",
        "nombre_completo": "Ley 40/2015 - Régimen Jurídico Sector Público",
        "boe_id": "BOE-A-2015-10566",
        "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-10566-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2015-10-01",
        "prioridad": "alta"
    },
    {
        "nombre": "RDL_5_2015_EBEP",
        "nombre_completo": "RDL 5/2015 - Estatuto Básico Empleado Público",
        "boe_id": "BOE-A-2015-11719",
        "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-11719-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2015-10-30",
        "prioridad": "alta"
    },
    {
        "nombre": "RD_1430_2009",
        "nombre_completo": "RD 1430/2009 - Incapacidad Temporal",
        "boe_id": "BOE-A-2009-15442",
        "url": "https://www.boe.es/buscar/pdf/2009/BOE-A-2009-15442-consolidado.pdf",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "2009-09-03",
        "prioridad": "alta"
    },
    {
        "nombre": "RD_1300_1995",
        "nombre_completo": "RD 1300/1995 - Incapacidad Permanente",
        "boe_id": "BOE-A-1995-19848",
        "url": "https://www.boe.es/buscar/pdf/1995/BOE-A-1995-19848-consolidado.pdf",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "1995-06-01",
        "prioridad": "alta"
    },
    
    # ========== MEDIAS (3) ==========
    {
        "nombre": "Ley_19_2021_IMV",
        "nombre_completo": "Ley 19/2021 - Ingreso Mínimo Vital",
        "boe_id": "BOE-A-2021-9155",
        "url": "https://www.boe.es/buscar/pdf/2021/BOE-A-2021-9155-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2021-05-20",
        "prioridad": "media"
    },
    {
        "nombre": "LO_3_2018_LOPDGDD",
        "nombre_completo": "LO 3/2018 - Protección de Datos",
        "boe_id": "BOE-A-2018-16673",
        "url": "https://www.boe.es/buscar/pdf/2018/BOE-A-2018-16673-consolidado.pdf",
        "tipo": "ley_organica",
        "nivel_jerarquia": 1,
        "fecha": "2018-12-05",
        "prioridad": "media"
    },
    {
        "nombre": "Ley_39_2006_Dependencia",
        "nombre_completo": "Ley 39/2006 - Dependencia",
        "boe_id": "BOE-A-2006-21990",
        "url": "https://www.boe.es/buscar/pdf/2006/BOE-A-2006-21990-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2006-12-14",
        "prioridad": "media"
    }
]

# Directorio de salida
output_dir = Path(__file__).parent.parent / "data" / "leyes"
output_dir.mkdir(parents=True, exist_ok=True)

print(f"\n📁 Directorio de salida: {output_dir}")

# Conectar a Qdrant Cloud
print(f"\n🔌 Conectando a Qdrant Cloud...")
try:
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        timeout=60
    )
    print(f"✅ Conectado a Qdrant Cloud")
except Exception as e:
    print(f"❌ Error conectando a Qdrant Cloud: {e}")
    sys.exit(1)

# Crear colección si no existe
print(f"\n📦 Verificando colección '{COLLECTION_NAME}'...")
try:
    collection_info = client.get_collection(COLLECTION_NAME)
    print(f"✅ Colección existe: {collection_info.points_count} puntos")
except:
    print(f"⚠️  Colección no existe, creando...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
    print(f"✅ Colección creada")

# Cargar modelo RoBERTalex
print(f"\n🧠 Cargando RoBERTalex...")
try:
    tokenizer = AutoTokenizer.from_pretrained("PlanTL-GOB-ES/RoBERTalex")
    model = AutoModel.from_pretrained("PlanTL-GOB-ES/RoBERTalex")
    model.eval()
    print(f"✅ RoBERTalex cargado")
except Exception as e:
    print(f"❌ Error cargando RoBERTalex: {e}")
    sys.exit(1)

def generate_embedding(text):
    """Generar embedding con RoBERTalex"""
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    except Exception as e:
        print(f"⚠️  Error generando embedding: {e}")
        return None

def detect_articulo(text):
    """Detectar número de artículo en el texto"""
    patterns = [
        r'Artículo\s+(\d+)',
        r'artículo\s+(\d+)',
        r'ARTÍCULO\s+(\d+)',
        r'Art\.\s+(\d+)',
        r'art\.\s+(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return f"Art. {match.group(1)}"
    return None

def descargar_ley(ley):
    """Descargar PDF de una ley"""
    print(f"\n⏳ Descargando desde BOE...")
    print(f"   URL: {ley['url']}")
    
    filepath = output_dir / f"{ley['nombre']}.pdf"
    
    # Si ya existe, no descargar de nuevo
    if filepath.exists():
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"✅ Ya existe: {size_mb:.2f} MB (usando archivo existente)")
        return filepath
    
    try:
        response = requests.get(ley['url'], timeout=180)
        response.raise_for_status()
        filepath.write_bytes(response.content)
        size_mb = len(response.content) / (1024 * 1024)
        print(f"✅ Descargado: {size_mb:.2f} MB")
        return filepath
    except Exception as e:
        print(f"❌ Error descargando: {e}")
        return None

def extraer_texto(filepath):
    """Extraer texto de un PDF"""
    print(f"\n📖 Extrayendo texto del PDF...")
    try:
        pdf = pypdf.PdfReader(filepath)
        total_pages = len(pdf.pages)
        print(f"   Páginas: {total_pages}")
        
        full_text = ""
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            full_text += text + "\n"
            if (page_num + 1) % 50 == 0:
                print(f"   Procesadas {page_num+1}/{total_pages} páginas...")
        
        print(f"✅ Texto extraído: {len(full_text):,} caracteres")
        return full_text
    except Exception as e:
        print(f"❌ Error extrayendo texto: {e}")
        return None

def crear_chunks(text, ley):
    """Crear chunks del texto"""
    print(f"\n✂️  Creando chunks...")
    CHUNK_SIZE = 512
    OVERLAP = 50
    
    try:
        tokens = tokenizer.encode(text, add_special_tokens=False)
        total_tokens = len(tokens)
        print(f"   Total tokens: {total_tokens:,}")
        
        chunks = []
        start = 0
        chunk_num = 0
        
        while start < total_tokens:
            end = min(start + CHUNK_SIZE, total_tokens)
            chunk_tokens = tokens[start:end]
            chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            
            articulo = detect_articulo(chunk_text)
            
            chunks.append({
                'text': chunk_text,
                'articulo': articulo,
                'chunk_num': chunk_num
            })
            
            chunk_num += 1
            start += (CHUNK_SIZE - OVERLAP)
        
        print(f"✅ Chunks creados: {len(chunks):,}")
        
        # Estadísticas de artículos
        articulos_detectados = [c['articulo'] for c in chunks if c['articulo']]
        articulos_unicos = sorted(set(articulos_detectados))
        if articulos_unicos:
            print(f"   Artículos detectados: {len(articulos_unicos)}")
            print(f"   Rango: {articulos_unicos[0]} - {articulos_unicos[-1]}")
        
        return chunks
    except Exception as e:
        print(f"❌ Error creando chunks: {e}")
        return None

def indexar_chunks(chunks, ley):
    """Indexar chunks en Qdrant Cloud"""
    print(f"\n💾 Indexando en Qdrant Cloud...")
    
    points = []
    embeddings_generados = 0
    
    for j, chunk in enumerate(chunks):
        # Generar embedding
        embedding = generate_embedding(chunk['text'])
        if embedding is None:
            continue
        
        embeddings_generados += 1
        
        # Crear punto
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding.tolist(),
            payload={
                "text": chunk['text'],
                "layer": 1,
                "tipo": ley['tipo'],
                "norma": ley['nombre'],
                "norma_completa": ley['nombre_completo'],
                "articulo": chunk['articulo'],
                "nivel_jerarquia": ley['nivel_jerarquia'],
                "fecha": ley['fecha'],
                "chunk_id": chunk['chunk_num'],
                "total_chunks": len(chunks),
                "boe_id": ley['boe_id'],
                "fuente": "BOE",
                "prioridad": ley['prioridad']
            }
        )
        points.append(point)
        
        # Mostrar progreso cada 50 chunks
        if (j + 1) % 50 == 0:
            print(f"   Procesados {j+1}/{len(chunks)} chunks...")
    
    print(f"✅ Embeddings generados: {embeddings_generados:,}/{len(chunks):,}")
    
    # Indexar en batches
    BATCH_SIZE = 100
    total_indexados = 0
    
    for j in range(0, len(points), BATCH_SIZE):
        batch = points[j:j+BATCH_SIZE]
        try:
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=batch
            )
            total_indexados += len(batch)
            print(f"   Indexados {total_indexados:,}/{len(points):,} chunks...")
        except Exception as e:
            print(f"⚠️  Error indexando batch {j//BATCH_SIZE + 1}: {e}")
    
    print(f"✅ Indexación completada: {total_indexados:,} chunks")
    return total_indexados

# ============================================================================
# PROCESO PRINCIPAL
# ============================================================================

print(f"\n{'='*80}")
print(f"🚀 INICIANDO INDEXACIÓN")
print(f"{'='*80}")

total_leyes = len(LEYES_TODAS)
leyes_exitosas = 0
leyes_fallidas = 0
total_chunks_indexados = 0

# Agrupar por prioridad
leyes_por_prioridad = {
    'critica': [l for l in LEYES_TODAS if l['prioridad'] == 'critica'],
    'alta': [l for l in LEYES_TODAS if l['prioridad'] == 'alta'],
    'media': [l for l in LEYES_TODAS if l['prioridad'] == 'media']
}

for prioridad in ['critica', 'alta', 'media']:
    leyes = leyes_por_prioridad[prioridad]
    emoji = '🔴' if prioridad == 'critica' else '🟠' if prioridad == 'alta' else '🟡'
    
    print(f"\n{'='*80}")
    print(f"{emoji} PRIORIDAD {prioridad.upper()} ({len(leyes)} leyes)")
    print(f"{'='*80}")
    
    for i, ley in enumerate(leyes, 1):
        print(f"\n{'-'*80}")
        print(f"📄 LEY {i}/{len(leyes)}: {ley['nombre_completo']}")
        print(f"{'-'*80}")
        
        try:
            # Paso 1: Descargar
            filepath = descargar_ley(ley)
            if filepath is None:
                leyes_fallidas += 1
                continue
            
            # Paso 2: Extraer texto
            text = extraer_texto(filepath)
            if text is None:
                leyes_fallidas += 1
                continue
            
            # Paso 3: Crear chunks
            chunks = crear_chunks(text, ley)
            if chunks is None:
                leyes_fallidas += 1
                continue
            
            # Paso 4: Indexar
            chunks_indexados = indexar_chunks(chunks, ley)
            total_chunks_indexados += chunks_indexados
            
            leyes_exitosas += 1
            print(f"\n✅ {ley['nombre_completo']} - COMPLETADA")
            
            # Pausa entre leyes
            if i < len(leyes):
                print(f"\n⏸️  Pausa de 3 segundos...")
                time.sleep(3)
                
        except Exception as e:
            print(f"\n❌ Error procesando {ley['nombre_completo']}: {e}")
            leyes_fallidas += 1
            import traceback
            traceback.print_exc()

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print(f"\n{'='*80}")
print(f"✅ INDEXACIÓN COMPLETADA - RESUMEN FINAL")
print(f"{'='*80}")

print(f"\n📊 Estadísticas:")
print(f"   Total leyes procesadas: {leyes_exitosas}/{total_leyes}")
print(f"   Leyes exitosas: {leyes_exitosas}")
print(f"   Leyes fallidas: {leyes_fallidas}")
print(f"   Total chunks indexados: {total_chunks_indexados:,}")

print(f"\n📚 Leyes por prioridad:")
for prioridad in ['critica', 'alta', 'media']:
    leyes = leyes_por_prioridad[prioridad]
    emoji = '🔴' if prioridad == 'critica' else '🟠' if prioridad == 'alta' else '🟡'
    print(f"\n{emoji} {prioridad.upper()}:")
    for ley in leyes:
        status = "✅" if ley in [l for l in LEYES_TODAS[:leyes_exitosas]] else "❌"
        print(f"   {status} {ley['nombre_completo']}")

# Verificar estadísticas finales de Qdrant
print(f"\n{'='*80}")
print(f"📊 ESTADÍSTICAS FINALES DE QDRANT CLOUD")
print(f"{'='*80}")

try:
    collection_info = client.get_collection(COLLECTION_NAME)
    print(f"   Total puntos: {collection_info.points_count:,}")
    print(f"   Colección: {COLLECTION_NAME}")
    print(f"   URL: {QDRANT_URL}")
except Exception as e:
    print(f"⚠️  Error obteniendo estadísticas: {e}")

print(f"\n{'='*80}")
print(f"✅ PROCESO COMPLETADO")
print(f"{'='*80}")
print(f"\n💡 Próximo paso: Ejecutar 'python comparar_qdrant_local_vs_cloud.py' para verificar")
