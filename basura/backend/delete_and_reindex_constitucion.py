"""
BORRAR Y RE-INDEXAR CONSTITUCIÓN COMPLETA
"""
import sys
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import pypdf
from transformers import AutoTokenizer, AutoModel
import torch
import re

print("="*80)
print("🗑️  PASO 1: BORRAR CONSTITUCIÓN EXISTENTE")
print("="*80)

# Conectar a Qdrant
client = QdrantClient(url="http://localhost:6333")
collection_name = "opositaia_leyes_seguridad_social"

# Contar chunks actuales de Constitución
current_points = client.scroll(
    collection_name=collection_name,
    scroll_filter=Filter(
        must=[
            FieldCondition(
                key="norma_nombre",
                match=MatchValue(value="Constitución_Española")
            )
        ]
    ),
    limit=1000
)[0]

print(f"📊 Chunks actuales de Constitución: {len(current_points)}")

if current_points:
    # Borrar todos los chunks de Constitución
    point_ids = [point.id for point in current_points]
    client.delete(
        collection_name=collection_name,
        points_selector=point_ids
    )
    print(f"✅ Borrados {len(point_ids)} chunks de Constitución")
else:
    print("ℹ️  No hay chunks de Constitución para borrar")

print("\n" + "="*80)
print("📥 PASO 2: CARGAR Y PROCESAR PDF COMPLETO")
print("="*80)

# Usar el PDF correcto
pdf_path = Path("backend/data/leyes/Constitución_Española.pdf")

if not pdf_path.exists():
    print(f"❌ ERROR: No existe {pdf_path}")
    sys.exit(1)

print(f"📄 Archivo: {pdf_path.name}")
print(f"📊 Tamaño: {pdf_path.stat().st_size / (1024*1024):.2f} MB")

# Leer PDF completo
pdf = pypdf.PdfReader(pdf_path)
print(f"📑 Páginas: {len(pdf.pages)}")

# Extraer TODO el texto
full_text = ""
for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    full_text += text + "\n"
    if (i + 1) % 10 == 0:
        print(f"   Procesadas {i+1}/{len(pdf.pages)} páginas...")

print(f"✅ Texto extraído: {len(full_text)} caracteres")

print("\n" + "="*80)
print("✂️  PASO 3: CHUNKING INTELIGENTE")
print("="*80)

# Tokenizer para chunking
tokenizer = AutoTokenizer.from_pretrained("PlanTL-GOB-ES/RoBERTalex")

# Parámetros de chunking
CHUNK_SIZE = 512
OVERLAP = 50

# Función mejorada de detección de artículos
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

# Chunking
chunks = []
tokens = tokenizer.encode(full_text, add_special_tokens=False)
total_tokens = len(tokens)

print(f"📊 Total tokens: {total_tokens}")
print(f"📏 Chunk size: {CHUNK_SIZE} tokens")
print(f"🔄 Overlap: {OVERLAP} tokens")

start = 0
chunk_num = 0

while start < total_tokens:
    end = min(start + CHUNK_SIZE, total_tokens)
    chunk_tokens = tokens[start:end]
    chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
    
    # Detectar artículo
    articulo = detect_articulo(chunk_text)
    
    chunks.append({
        'text': chunk_text,
        'articulo': articulo,
        'chunk_num': chunk_num,
        'start_token': start,
        'end_token': end
    })
    
    chunk_num += 1
    start += (CHUNK_SIZE - OVERLAP)
    
    if chunk_num % 10 == 0:
        print(f"   Creados {chunk_num} chunks...")

print(f"✅ Total chunks creados: {len(chunks)}")

# Estadísticas de artículos detectados
articulos_detectados = [c['articulo'] for c in chunks if c['articulo']]
articulos_unicos = sorted(set(articulos_detectados), key=lambda x: int(x))
print(f"📋 Artículos detectados: {len(articulos_unicos)}")
print(f"   Rango: {articulos_unicos[0] if articulos_unicos else 'N/A'} - {articulos_unicos[-1] if articulos_unicos else 'N/A'}")

print("\n" + "="*80)
print("🧠 PASO 4: GENERAR EMBEDDINGS")
print("="*80)

# Cargar modelo RoBERTalex
print("⏳ Cargando RoBERTalex...")
model = AutoModel.from_pretrained("PlanTL-GOB-ES/RoBERTalex")
model.eval()

def generate_embedding(text):
    """Generar embedding con RoBERTalex"""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

embeddings = []
for i, chunk in enumerate(chunks):
    emb = generate_embedding(chunk['text'])
    embeddings.append(emb)
    
    if (i + 1) % 10 == 0:
        print(f"   Generados {i+1}/{len(chunks)} embeddings...")

print(f"✅ Embeddings generados: {len(embeddings)}")

print("\n" + "="*80)
print("💾 PASO 5: INDEXAR EN QDRANT")
print("="*80)

from qdrant_client.models import PointStruct
import uuid

points = []
for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding.tolist(),
        payload={
            "content": chunk['text'],
            "layer": 1,
            "tipo": "constitucion",
            "norma_nombre": "Constitución_Española",
            "norma_completa": "Constitución Española de 1978",
            "articulo": chunk['articulo'],
            "nivel_jerarquia": 1,
            "fecha": "1978-12-29",
            "chunk_num": chunk['chunk_num'],
            "boe_id": "BOE-A-1978-31229"
        }
    )
    points.append(point)

# Indexar en batches
BATCH_SIZE = 100
for i in range(0, len(points), BATCH_SIZE):
    batch = points[i:i+BATCH_SIZE]
    client.upsert(
        collection_name=collection_name,
        points=batch
    )
    print(f"   Indexados {min(i+BATCH_SIZE, len(points))}/{len(points)} chunks...")

print(f"✅ Indexación completada: {len(points)} chunks")

print("\n" + "="*80)
print("✅ CONSTITUCIÓN RE-INDEXADA COMPLETAMENTE")
print("="*80)
print(f"📊 Total chunks: {len(chunks)}")
print(f"📋 Artículos únicos: {len(articulos_unicos)}")
print(f"📝 Artículos: {', '.join(articulos_unicos[:20])}{'...' if len(articulos_unicos) > 20 else ''}")
print("="*80)
