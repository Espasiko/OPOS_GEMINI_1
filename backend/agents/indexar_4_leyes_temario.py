#!/usr/bin/env python3
"""
INDEXAR 4 LEYES FALTANTES DEL TEMARIO OFICIAL
- LO 6/1985 (LOPJ) - Poder Judicial
- LO 2/1979 (LOTC) - Tribunal Constitucional  
- LO 5/1985 (LOREG) - Régimen Electoral General
- Ley 34/2014 - Liquidación e ingreso de cuotas SS
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
from bs4 import BeautifulSoup

# Cargar variables de entorno
env_path = Path(__file__).parent.parent / '.env.backend'
load_dotenv(env_path)

print("="*80)
print("📚 INDEXACIÓN DE 4 LEYES FALTANTES DEL TEMARIO OFICIAL")
print("="*80)

# Configuración Qdrant Cloud
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

# 4 Leyes faltantes
LEYES_FALTANTES = [
    {
        "nombre": "Ley_34_2014",
        "nombre_completo": "Ley 34/2014 - Liquidación e ingreso de cuotas SS",
        "boe_id": "BOE-A-2014-13517",
        "url": "https://www.boe.es/eli/es/l/2014/12/26/34/con",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2014-12-26",
        "prioridad": "alta",
        "bloque": "Seguridad Social"
    },
    {
        "nombre": "LO_6_1985_LOPJ",
        "nombre_completo": "LO 6/1985 - Poder Judicial",
        "boe_id": "BOE-A-1985-12666",
        "url": "https://www.boe.es/eli/es/lo/1985/07/01/6/con",
        "tipo": "ley_organica",
        "nivel_jerarquia": 1,
        "fecha": "1985-07-01",
        "prioridad": "alta",
        "bloque": "General"
    },
    {
        "nombre": "LO_2_1979_LOTC",
        "nombre_completo": "LO 2/1979 - Tribunal Constitucional",
        "boe_id": "BOE-A-1979-23709",
        "url": "https://www.boe.es/eli/es/lo/1979/10/05/2/con",
        "tipo": "ley_organica",
        "nivel_jerarquia": 1,
        "fecha": "1979-10-05",
        "prioridad": "alta",
        "bloque": "General"
    },
    {
        "nombre": "LO_5_1985_LOREG",
        "nombre_completo": "LO 5/1985 - Régimen Electoral General",
        "boe_id": "BOE-A-1985-11672",
        "url": "https://www.boe.es/eli/es/lo/1985/06/19/5/con",
        "tipo": "ley_organica",
        "nivel_jerarquia": 1,
        "fecha": "1985-06-19",
        "prioridad": "media",
        "bloque": "General"
    }
]

# Directorio de salida
output_dir = Path(__file__).parent.parent / "data" / "leyes"
output_dir.mkdir(parents=True, exist_ok=True)

# Conectar a Qdrant Cloud
print(f"\n🔌 Conectando a Qdrant Cloud...")
try:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=60)
    collection_info = client.get_collection(COLLECTION_NAME)
    puntos_iniciales = collection_info.points_count
    print(f"✅ Conectado - Puntos iniciales: {puntos_iniciales:,}")
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
    print(f"❌ Error: {e}")
    sys.exit(1)

def generate_embedding(text):
    """Generar embedding con RoBERTalex"""
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    except Exception as e:
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

def descargar_html(url):
    """Descargar HTML del BOE"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, timeout=180, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Error descargando: {e}")
        return None

def extraer_texto_html(html_content):
    """Extraer texto de HTML del BOE"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Buscar contenido
        content = None
        for selector in ['div.documento', 'div.texto', 'div#texto', 'article', 'body']:
            content = soup.select_one(selector)
            if content:
                break
        
        if content:
            text = content.get_text(separator='\n', strip=True)
            return text
        return None
    except Exception as e:
        print(f"❌ Error extrayendo: {e}")
        return None

def crear_chunks(text, ley):
    """Crear chunks del texto"""
    CHUNK_SIZE = 512
    OVERLAP = 50
    
    try:
        tokens = tokenizer.encode(text, add_special_tokens=False)
        total_tokens = len(tokens)
        
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
        
        return chunks
    except Exception as e:
        print(f"❌ Error creando chunks: {e}")
        return None

def indexar_chunks(chunks, ley):
    """Indexar chunks en Qdrant Cloud"""
    points = []
    
    for chunk in chunks:
        embedding = generate_embedding(chunk['text'])
        if embedding is None:
            continue
        
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
                "prioridad": ley['prioridad'],
                "bloque": ley['bloque']
            }
        )
        points.append(point)
    
    # Indexar en batches
    BATCH_SIZE = 100
    total_indexados = 0
    
    for j in range(0, len(points), BATCH_SIZE):
        batch = points[j:j+BATCH_SIZE]
        try:
            client.upsert(collection_name=COLLECTION_NAME, points=batch)
            total_indexados += len(batch)
        except Exception as e:
            print(f"⚠️  Error indexando batch: {e}")
    
    return total_indexados

# PROCESO PRINCIPAL
print(f"\n{'='*80}")
print(f"🚀 INICIANDO INDEXACIÓN")
print(f"{'='*80}")

total_chunks_indexados = 0
leyes_exitosas = 0

for i, ley in enumerate(LEYES_FALTANTES, 1):
    print(f"\n{'-'*80}")
    print(f"📄 LEY {i}/4: {ley['nombre_completo']}")
    print(f"   Bloque: {ley['bloque']}")
    print(f"{'-'*80}")
    
    try:
        # Descargar
        print(f"\n⏳ Descargando desde BOE...")
        print(f"   URL: {ley['url']}")
        html_content = descargar_html(ley['url'])
        if not html_content:
            continue
        
        # Extraer texto
        print(f"\n📖 Extrayendo texto...")
        text = extraer_texto_html(html_content)
        if not text or len(text) < 1000:
            print(f"⚠️  Texto muy corto ({len(text) if text else 0} caracteres)")
            continue
        
        print(f"✅ Texto extraído: {len(text):,} caracteres")
        
        # Crear chunks
        print(f"\n✂️  Creando chunks...")
        chunks = crear_chunks(text, ley)
        if not chunks:
            continue
        
        print(f"✅ Chunks creados: {len(chunks):,}")
        
        # Detectar artículos
        articulos = [c['articulo'] for c in chunks if c['articulo']]
        if articulos:
            articulos_unicos = sorted(set(articulos), key=lambda x: int(x.split()[1]) if x else 0)
            print(f"   Artículos detectados: {len(articulos_unicos)}")
            if len(articulos_unicos) > 0:
                print(f"   Rango: {articulos_unicos[0]} - {articulos_unicos[-1]}")
        
        # Indexar
        print(f"\n💾 Indexando en Qdrant Cloud...")
        chunks_indexados = indexar_chunks(chunks, ley)
        total_chunks_indexados += chunks_indexados
        
        print(f"✅ Indexados: {chunks_indexados:,} chunks")
        leyes_exitosas += 1
        
        print(f"\n✅ {ley['nombre_completo']} - COMPLETADA")
        
        if i < len(LEYES_FALTANTES):
            print(f"\n⏸️  Pausa de 2 segundos...")
            time.sleep(2)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

# RESUMEN FINAL
print(f"\n{'='*80}")
print(f"✅ INDEXACIÓN COMPLETADA")
print(f"{'='*80}")

print(f"\n📊 Estadísticas:")
print(f"   Leyes procesadas: {leyes_exitosas}/4")
print(f"   Total chunks indexados: {total_chunks_indexados:,}")

try:
    collection_info = client.get_collection(COLLECTION_NAME)
    puntos_finales = collection_info.points_count
    incremento = puntos_finales - puntos_iniciales
    
    print(f"\n📈 Qdrant Cloud:")
    print(f"   Puntos iniciales: {puntos_iniciales:,}")
    print(f"   Puntos finales: {puntos_finales:,}")
    print(f"   Incremento: +{incremento:,}")
except Exception as e:
    print(f"⚠️  Error obteniendo estadísticas: {e}")

print(f"\n{'='*80}")
print(f"✅ PROCESO COMPLETADO")
print(f"{'='*80}")
print(f"\n💡 Próximo paso: Ejecutar 'python verificar_leyes_temario_oficial.py' para verificar")
