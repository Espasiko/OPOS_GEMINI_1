"""
DESCARGAR E INDEXAR 3 LEYES CRÍTICAS DE SEGURIDAD SOCIAL
1. RD 1430/2009 - Incapacidad Temporal
2. RD 1300/1995 - Incapacidad Permanente  
3. Ley 39/2006 - Dependencia
"""
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

print("="*80)
print("📥 DESCARGA E INDEXACIÓN DE 3 LEYES CRÍTICAS SS")
print("="*80)

# Definir las 3 leyes
LEYES_CRITICAS = [
    {
        "nombre": "RD_1430_2009_Incapacidad_Temporal",
        "nombre_completo": "RD 1430/2009 Incapacidad Temporal",
        "boe_id": "BOE-A-2009-15442",
        "url": "https://www.boe.es/buscar/pdf/2009/BOE-A-2009-15442-consolidado.pdf",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "2009-09-03",
        "descripcion": "Reglamento de Incapacidad Temporal"
    },
    {
        "nombre": "RD_1300_1995_Incapacidad_Permanente",
        "nombre_completo": "RD 1300/1995 Incapacidad Permanente",
        "boe_id": "BOE-A-1995-19848",
        "url": "https://www.boe.es/buscar/pdf/1995/BOE-A-1995-19848-consolidado.pdf",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "1995-06-01",
        "descripcion": "Reglamento de Incapacidad Permanente"
    },
    {
        "nombre": "Ley_39_2006_Dependencia",
        "nombre_completo": "Ley 39/2006 Dependencia",
        "boe_id": "BOE-A-2006-21990",
        "url": "https://www.boe.es/buscar/pdf/2006/BOE-A-2006-21990-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2006-12-14",
        "descripcion": "Ley de Promoción de la Autonomía Personal y Atención a Personas en Situación de Dependencia"
    }
]

# Directorio de salida
output_dir = Path("backend/data/leyes")
output_dir.mkdir(parents=True, exist_ok=True)

# Conectar a Qdrant
client = QdrantClient(url="http://localhost:6333")
collection_name = "opositaia_leyes_seguridad_social"

# Cargar modelo RoBERTalex
print("\n🧠 Cargando RoBERTalex...")
tokenizer = AutoTokenizer.from_pretrained("PlanTL-GOB-ES/RoBERTalex")
model = AutoModel.from_pretrained("PlanTL-GOB-ES/RoBERTalex")
model.eval()

def generate_embedding(text):
    """Generar embedding con RoBERTalex"""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

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
            return match.group(1)
    return None

# Procesar cada ley
total_chunks_indexados = 0

for i, ley in enumerate(LEYES_CRITICAS, 1):
    print("\n" + "="*80)
    print(f"📄 LEY {i}/3: {ley['nombre_completo']}")
    print("="*80)
    
    # PASO 1: Descargar
    print(f"\n⏳ Descargando desde BOE...")
    print(f"   URL: {ley['url']}")
    
    filepath = output_dir / f"{ley['nombre']}.pdf"
    
    try:
        response = requests.get(ley['url'], timeout=120)
        response.raise_for_status()
        filepath.write_bytes(response.content)
        size_mb = len(response.content) / (1024 * 1024)
        print(f"✅ Descargado: {size_mb:.2f} MB")
    except Exception as e:
        print(f"❌ Error descargando: {e}")
        continue
    
    # PASO 2: Extraer texto
    print(f"\n📖 Extrayendo texto del PDF...")
    try:
        pdf = pypdf.PdfReader(filepath)
        print(f"   Páginas: {len(pdf.pages)}")
        
        full_text = ""
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            full_text += text + "\n"
            if (page_num + 1) % 20 == 0:
                print(f"   Procesadas {page_num+1}/{len(pdf.pages)} páginas...")
        
        print(f"✅ Texto extraído: {len(full_text)} caracteres")
    except Exception as e:
        print(f"❌ Error extrayendo texto: {e}")
        continue
    
    # PASO 3: Chunking
    print(f"\n✂️  Creando chunks...")
    CHUNK_SIZE = 512
    OVERLAP = 50
    
    tokens = tokenizer.encode(full_text, add_special_tokens=False)
    total_tokens = len(tokens)
    print(f"   Total tokens: {total_tokens}")
    
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
    
    print(f"✅ Chunks creados: {len(chunks)}")
    
    # Estadísticas de artículos
    articulos_detectados = [c['articulo'] for c in chunks if c['articulo']]
    articulos_unicos = sorted(set(articulos_detectados), key=lambda x: int(x) if x.isdigit() else 999)
    print(f"   Artículos detectados: {len(articulos_unicos)}")
    if articulos_unicos:
        print(f"   Rango: {articulos_unicos[0]} - {articulos_unicos[-1]}")
    
    # PASO 4: Generar embeddings
    print(f"\n🧠 Generando embeddings...")
    embeddings = []
    for j, chunk in enumerate(chunks):
        emb = generate_embedding(chunk['text'])
        embeddings.append(emb)
        
        if (j + 1) % 20 == 0:
            print(f"   Generados {j+1}/{len(chunks)} embeddings...")
    
    print(f"✅ Embeddings generados: {len(embeddings)}")
    
    # PASO 5: Indexar en Qdrant
    print(f"\n💾 Indexando en Qdrant...")
    points = []
    for j, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding.tolist(),
            payload={
                "content": chunk['text'],
                "layer": 1,
                "tipo": ley['tipo'],
                "norma_nombre": ley['nombre'],
                "norma_completa": ley['nombre_completo'],
                "articulo": chunk['articulo'],
                "nivel_jerarquia": ley['nivel_jerarquia'],
                "fecha": ley['fecha'],
                "chunk_num": chunk['chunk_num'],
                "boe_id": ley['boe_id']
            }
        )
        points.append(point)
    
    # Indexar en batches
    BATCH_SIZE = 100
    for j in range(0, len(points), BATCH_SIZE):
        batch = points[j:j+BATCH_SIZE]
        client.upsert(
            collection_name=collection_name,
            points=batch
        )
        print(f"   Indexados {min(j+BATCH_SIZE, len(points))}/{len(points)} chunks...")
    
    print(f"✅ Indexación completada: {len(points)} chunks")
    total_chunks_indexados += len(points)
    
    # Pequeña pausa entre leyes
    if i < len(LEYES_CRITICAS):
        print(f"\n⏸️  Pausa de 2 segundos antes de la siguiente ley...")
        time.sleep(2)

# RESUMEN FINAL
print("\n" + "="*80)
print("✅ INDEXACIÓN COMPLETADA - RESUMEN FINAL")
print("="*80)

for i, ley in enumerate(LEYES_CRITICAS, 1):
    print(f"{i}. ✅ {ley['nombre_completo']}")

print(f"\n📊 Total chunks indexados: {total_chunks_indexados}")
print(f"📚 Leyes procesadas: {len(LEYES_CRITICAS)}/3")
print("="*80)

# Verificar estadísticas finales
print("\n📊 ESTADÍSTICAS FINALES DE LA COLECCIÓN")
print("="*80)

collection_info = client.get_collection(collection_name)
print(f"Total puntos en colección: {collection_info.points_count}")
print(f"Vector size: {collection_info.config.params.vectors.size}")
print("="*80)
