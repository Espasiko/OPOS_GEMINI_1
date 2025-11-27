#!/usr/bin/env python3
"""
RE-INDEXAR LEY 19/2021 (IMV) - VERSIÓN COMPLETA
Buscar y descargar la versión completa de la ley del BOE
"""
import os
import sys
import requests
import pypdf
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
import torch
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
import uuid
import re
import time
from dotenv import load_dotenv

# Cargar variables de entorno
env_path = Path(__file__).parent.parent / '.env.backend'
load_dotenv(env_path)

print("="*80)
print("📚 RE-INDEXACIÓN LEY 19/2021 (IMV) - VERSIÓN COMPLETA")
print("="*80)

# Configuración Qdrant Cloud
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print(f"\n🔌 Configuración:")
print(f"   Qdrant URL: {QDRANT_URL}")
print(f"   Colección: {COLLECTION_NAME}")

# URLs alternativas para la Ley IMV
URLS_IMV = [
    {
        "tipo": "PDF consolidado",
        "url": "https://www.boe.es/buscar/pdf/2021/BOE-A-2021-9155-consolidado.pdf"
    },
    {
        "tipo": "HTML consolidado",
        "url": "https://www.boe.es/eli/es/l/2021/05/20/19/con"
    },
    {
        "tipo": "PDF original",
        "url": "https://www.boe.es/boe/dias/2021/05/21/pdfs/BOE-A-2021-9155.pdf"
    },
    {
        "tipo": "HTML original",
        "url": "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2021-9155"
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
    puntos_iniciales = collection_info.points_count
    print(f"✅ Colección existe: {puntos_iniciales:,} puntos")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Eliminar chunks antiguos de IMV
print(f"\n🗑️  Eliminando chunks antiguos de Ley_19_2021_IMV...")
try:
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="norma",
                    match=MatchValue(value="Ley_19_2021_IMV")
                )
            ]
        )
    )
    print(f"✅ Chunks antiguos eliminados")
    time.sleep(2)  # Esperar a que se complete la eliminación
except Exception as e:
    print(f"⚠️  Error eliminando chunks antiguos: {e}")

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

def descargar_pdf(url, filename):
    """Descargar PDF"""
    print(f"\n⏳ Descargando PDF...")
    print(f"   URL: {url}")
    
    filepath = output_dir / filename
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=180, headers=headers)
        response.raise_for_status()
        filepath.write_bytes(response.content)
        size_mb = len(response.content) / (1024 * 1024)
        print(f"✅ Descargado: {size_mb:.2f} MB")
        return filepath
    except Exception as e:
        print(f"❌ Error descargando: {e}")
        return None

def extraer_texto_pdf(filepath):
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
            if (page_num + 1) % 10 == 0:
                print(f"   Procesadas {page_num+1}/{total_pages} páginas...")
        
        print(f"✅ Texto extraído: {len(full_text):,} caracteres")
        return full_text
    except Exception as e:
        print(f"❌ Error extrayendo texto: {e}")
        return None

def crear_chunks(text):
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

def indexar_chunks(chunks):
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
                "tipo": "ley",
                "norma": "Ley_19_2021_IMV",
                "norma_completa": "Ley 19/2021 - Ingreso Mínimo Vital",
                "articulo": chunk['articulo'],
                "nivel_jerarquia": 1,
                "fecha": "2021-05-20",
                "chunk_id": chunk['chunk_num'],
                "total_chunks": len(chunks),
                "boe_id": "BOE-A-2021-9155",
                "fuente": "BOE",
                "prioridad": "media"
            }
        )
        points.append(point)
        
        # Mostrar progreso cada 10 chunks
        if (j + 1) % 10 == 0:
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
            if len(points) > BATCH_SIZE:
                print(f"   Indexados {total_indexados:,}/{len(points):,} chunks...")
        except Exception as e:
            print(f"⚠️  Error indexando batch {j//BATCH_SIZE + 1}: {e}")
    
    print(f"✅ Indexación completada: {total_indexados:,} chunks")
    return total_indexados

# ============================================================================
# PROCESO PRINCIPAL
# ============================================================================

print(f"\n{'='*80}")
print(f"🚀 INICIANDO RE-INDEXACIÓN DE LEY IMV")
print(f"{'='*80}")

# Probar cada URL hasta encontrar una que funcione
texto_completo = None
url_exitosa = None

for i, url_info in enumerate(URLS_IMV, 1):
    print(f"\n{'-'*80}")
    print(f"INTENTO {i}/{len(URLS_IMV)}: {url_info['tipo']}")
    print(f"{'-'*80}")
    
    if url_info['url'].endswith('.pdf'):
        # Descargar PDF
        filepath = descargar_pdf(url_info['url'], f"Ley_19_2021_IMV_v{i}.pdf")
        if filepath:
            texto_completo = extraer_texto_pdf(filepath)
            if texto_completo and len(texto_completo) > 10000:  # Al menos 10KB
                url_exitosa = url_info
                print(f"\n✅ Versión completa encontrada!")
                break
            else:
                print(f"⚠️  Texto muy corto, probando siguiente URL...")
    else:
        # Descargar HTML
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            print("\n⚠️  BeautifulSoup no instalado, saltando HTML...")
            continue
        
        print(f"\n⏳ Descargando HTML...")
        print(f"   URL: {url_info['url']}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url_info['url'], timeout=180, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar contenido
            content = None
            for selector in ['div.documento', 'div.texto', 'div#texto', 'article']:
                content = soup.select_one(selector)
                if content:
                    break
            
            if not content:
                content = soup.find('body')
            
            if content:
                texto_completo = content.get_text(separator='\n', strip=True)
                print(f"✅ Descargado: {len(texto_completo):,} caracteres")
                
                if len(texto_completo) > 10000:
                    url_exitosa = url_info
                    print(f"\n✅ Versión completa encontrada!")
                    break
                else:
                    print(f"⚠️  Texto muy corto, probando siguiente URL...")
        except Exception as e:
            print(f"❌ Error: {e}")

if not texto_completo or not url_exitosa:
    print(f"\n❌ No se pudo descargar ninguna versión completa de la ley")
    sys.exit(1)

print(f"\n{'='*80}")
print(f"✅ VERSIÓN COMPLETA OBTENIDA")
print(f"{'='*80}")
print(f"   Fuente: {url_exitosa['tipo']}")
print(f"   URL: {url_exitosa['url']}")
print(f"   Tamaño: {len(texto_completo):,} caracteres")

# Crear chunks
chunks = crear_chunks(texto_completo)
if not chunks or len(chunks) == 0:
    print(f"\n❌ No se pudieron crear chunks")
    sys.exit(1)

# Indexar
chunks_indexados = indexar_chunks(chunks)

# Verificar resultado
print(f"\n{'='*80}")
print(f"📊 VERIFICACIÓN FINAL")
print(f"{'='*80}")

try:
    collection_info = client.get_collection(COLLECTION_NAME)
    puntos_finales = collection_info.points_count
    incremento = puntos_finales - puntos_iniciales
    
    print(f"   Puntos iniciales: {puntos_iniciales:,}")
    print(f"   Puntos finales: {puntos_finales:,}")
    print(f"   Incremento: +{incremento:,}")
    print(f"   Chunks indexados: {chunks_indexados:,}")
    
    if incremento == chunks_indexados:
        print(f"\n✅ Verificación exitosa: todos los chunks fueron indexados")
    else:
        print(f"\n⚠️  Discrepancia: esperados {chunks_indexados}, incremento real {incremento}")
        
except Exception as e:
    print(f"⚠️  Error en verificación: {e}")

print(f"\n{'='*80}")
print(f"✅ RE-INDEXACIÓN COMPLETADA")
print(f"{'='*80}")
print(f"\n💡 Próximo paso: Ejecutar 'python test_rag_simple.py' para verificar búsqueda")
