"""
INDEXAR RD COTIZACIÓN Y LIQUIDACIÓN - URL CORRECTA
BOE-A-1996-1579
"""
import requests
import pypdf
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
import torch
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
import re

print("="*80)
print("📥 INDEXAR RD COTIZACIÓN Y LIQUIDACIÓN")
print("="*80)

# Datos correctos del RD
ley = {
    "nombre": "RD_Cotizacion_Liquidacion",
    "nombre_completo": "RD 2064/1995 Cotización y Liquidación",
    "boe_id": "BOE-A-1996-1579",
    "url": "https://www.boe.es/buscar/pdf/1996/BOE-A-1996-1579-consolidado.pdf",
    "tipo": "reglamento",
    "nivel_jerarquia": 2,
    "fecha": "1996-01-26",
    "descripcion": "Reglamento General sobre Cotización y Liquidación de la Seguridad Social"
}

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
    exit(1)

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
    exit(1)

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
    
    if chunk_num % 20 == 0:
        print(f"   Creados {chunk_num} chunks...")

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
    if (j + BATCH_SIZE) % 100 == 0:
        print(f"   Indexados {min(j+BATCH_SIZE, len(points))}/{len(points)} chunks...")

print(f"✅ Indexación completada: {len(points)} chunks")

# RESUMEN FINAL
print("\n" + "="*80)
print("✅ RD COTIZACIÓN INDEXADO EXITOSAMENTE")
print("="*80)
print(f"📄 Ley: {ley['nombre_completo']}")
print(f"📊 Chunks: {len(chunks)}")
print(f"📋 Artículos: {len(articulos_unicos)}")
print(f"🆔 BOE ID: {ley['boe_id']}")
print("="*80)

# Verificar estadísticas finales
collection_info = client.get_collection(collection_name)
print(f"\n📊 ESTADÍSTICAS FINALES DE LA COLECCIÓN")
print(f"Total puntos en colección: {collection_info.points_count:,}")
print("="*80)
