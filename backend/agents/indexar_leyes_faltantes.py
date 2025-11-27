#!/usr/bin/env python3
"""
INDEXAR LAS 4 LEYES FALTANTES CON URLs CORREGIDAS
- RD 84/1996 (Afiliación)
- RD 2064/1995 (Cotización)
- RD 1415/2004 (Recaudación)
- Ley 19/2021 (IMV)
"""
import os
import sys
import requests
import pypdf
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
import torch
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
import re
import time
from dotenv import load_dotenv

# Cargar variables de entorno
env_path = Path(__file__).parent.parent / '.env.backend'
load_dotenv(env_path)

print("="*80)
print("📚 INDEXACIÓN DE LEYES FALTANTES (4 leyes)")
print("="*80)

# Configuración Qdrant Cloud
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print(f"\n🔌 Configuración:")
print(f"   Qdrant URL: {QDRANT_URL}")
print(f"   Colección: {COLLECTION_NAME}")

# Leyes faltantes con URLs corregidas
LEYES_FALTANTES = [
    {
        "nombre": "RD_84_1996",
        "nombre_completo": "RD 84/1996 - Afiliación, Altas y Bajas",
        "boe_id": "BOE-A-1996-3981",
        "url": "https://www.boe.es/eli/es/rd/1996/01/26/84/con",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "1996-02-26",
        "prioridad": "critica"
    },
    {
        "nombre": "RD_2064_1995",
        "nombre_completo": "RD 2064/1995 - Cotización y Liquidación",
        "boe_id": "BOE-A-1995-26497",
        "url": "https://www.boe.es/eli/es/rd/1995/12/22/2064/con",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "1995-12-22",
        "prioridad": "critica"
    },
    {
        "nombre": "RD_1415_2004",
        "nombre_completo": "RD 1415/2004 - Recaudación",
        "boe_id": "BOE-A-2004-11607",
        "url": "https://www.boe.es/eli/es/rd/2004/06/11/1415/con",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "2004-06-11",
        "prioridad": "critica"
    },
    {
        "nombre": "Ley_19_2021_IMV",
        "nombre_completo": "Ley 19/2021 - Ingreso Mínimo Vital",
        "boe_id": "BOE-A-2021-9155",
        "url": "https://www.boe.es/eli/es/l/2021/05/20/19/con",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2021-05-20",
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

# Verificar colección
print(f"\n📦 Verificando colección '{COLLECTION_NAME}'...")
try:
    collection_info = client.get_collection(COLLECTION_NAME)
    print(f"✅ Colección existe: {collection_info.points_count} puntos")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

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

def descargar_ley_html(ley):
    """Descargar HTML de una ley desde BOE"""
    print(f"\n⏳ Descargando desde BOE (formato HTML)...")
    print(f"   URL: {ley['url']}")
    
    filepath = output_dir / f"{ley['nombre']}.html"
    
    # Si ya existe, no descargar de nuevo
    if filepath.exists():
        size_kb = filepath.stat().st_size / 1024
        print(f"✅ Ya existe: {size_kb:.2f} KB (usando archivo existente)")
        return filepath
    
    try:
        # Agregar headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(ley['url'], timeout=180, headers=headers)
        response.raise_for_status()
        filepath.write_text(response.text, encoding='utf-8')
        size_kb = len(response.text) / 1024
        print(f"✅ Descargado: {size_kb:.2f} KB")
        return filepath
    except Exception as e:
        print(f"❌ Error descargando: {e}")
        return None

def extraer_texto_html(filepath):
    """Extraer texto de un HTML del BOE"""
    print(f"\n📖 Extrayendo texto del HTML...")
    try:
        from bs4 import BeautifulSoup
        
        html_content = filepath.read_text(encoding='utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Buscar el contenido principal
        # El BOE usa diferentes estructuras, intentar varias
        content = None
        
        # Intentar encontrar el div con el texto consolidado
        for selector in ['div.documento', 'div.texto', 'div#texto', 'article']:
            content = soup.select_one(selector)
            if content:
                break
        
        if not content:
            # Si no encuentra estructura específica, usar todo el body
            content = soup.find('body')
        
        if content:
            text = content.get_text(separator='\n', strip=True)
            print(f"✅ Texto extraído: {len(text):,} caracteres")
            return text
        else:
            print(f"❌ No se pudo extraer texto del HTML")
            return None
            
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
        articulos_unicos = sorted(set(articulos_detectados), key=lambda x: int(x.split()[1]) if x else 0)
        if articulos_unicos:
            print(f"   Artículos detectados: {len(articulos_unicos)}")
            if len(articulos_unicos) > 0:
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
print(f"🚀 INICIANDO INDEXACIÓN DE LEYES FALTANTES")
print(f"{'='*80}")

# Instalar BeautifulSoup si no está instalado
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("\n⚠️  BeautifulSoup no está instalado. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "lxml"])
    from bs4 import BeautifulSoup
    print("✅ BeautifulSoup instalado")

total_leyes = len(LEYES_FALTANTES)
leyes_exitosas = 0
leyes_fallidas = 0
total_chunks_indexados = 0

for i, ley in enumerate(LEYES_FALTANTES, 1):
    print(f"\n{'-'*80}")
    print(f"📄 LEY {i}/{total_leyes}: {ley['nombre_completo']}")
    print(f"{'-'*80}")
    
    try:
        # Paso 1: Descargar HTML
        filepath = descargar_ley_html(ley)
        if filepath is None:
            leyes_fallidas += 1
            continue
        
        # Paso 2: Extraer texto
        text = extraer_texto_html(filepath)
        if text is None or len(text) < 100:
            print(f"⚠️  Texto muy corto o vacío, saltando...")
            leyes_fallidas += 1
            continue
        
        # Paso 3: Crear chunks
        chunks = crear_chunks(text, ley)
        if chunks is None or len(chunks) == 0:
            leyes_fallidas += 1
            continue
        
        # Paso 4: Indexar
        chunks_indexados = indexar_chunks(chunks, ley)
        total_chunks_indexados += chunks_indexados
        
        leyes_exitosas += 1
        print(f"\n✅ {ley['nombre_completo']} - COMPLETADA")
        
        # Pausa entre leyes
        if i < total_leyes:
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

print(f"\n📚 Leyes procesadas:")
for ley in LEYES_FALTANTES:
    status = "✅" if leyes_exitosas > 0 else "❌"
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
