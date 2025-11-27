"""
DESCARGAR E INDEXAR LEYES RESTANTES
Total: 9 leyes pendientes
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
print("📥 DESCARGA E INDEXACIÓN DE LEYES RESTANTES")
print("="*80)

# Definir las leyes restantes
LEYES_RESTANTES = [
    # PRIORIDAD MEDIA
    {
        "nombre": "Ley_General_Presupuestaria",
        "nombre_completo": "Ley 47/2003 General Presupuestaria",
        "boe_id": "BOE-A-2003-21614",
        "url": "https://www.boe.es/buscar/pdf/2003/BOE-A-2003-21614-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2003-11-26",
        "descripcion": "Ley General Presupuestaria",
        "prioridad": "MEDIA"
    },
    {
        "nombre": "Ley_Contratos_Sector_Publico",
        "nombre_completo": "Ley 9/2017 Contratos del Sector Público",
        "boe_id": "BOE-A-2017-12902",
        "url": "https://www.boe.es/buscar/pdf/2017/BOE-A-2017-12902-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2017-11-08",
        "descripcion": "Ley de Contratos del Sector Público",
        "prioridad": "MEDIA"
    },
    {
        "nombre": "RD_Cotizacion_Liquidacion",
        "nombre_completo": "RD 2064/1995 Cotización y Liquidación",
        "boe_id": "BOE-A-1995-26769",
        "url": "https://www.boe.es/buscar/pdf/1995/BOE-A-1995-26769-consolidado.pdf",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "1995-12-22",
        "descripcion": "Reglamento General sobre Cotización y Liquidación",
        "prioridad": "MEDIA"
    },
    # PRIORIDAD BAJA
    {
        "nombre": "Ley_Igualdad_Trans",
        "nombre_completo": "Ley 4/2023 Igualdad Trans y LGTBI",
        "boe_id": "BOE-A-2023-5366",
        "url": "https://www.boe.es/buscar/pdf/2023/BOE-A-2023-5366-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2023-02-28",
        "descripcion": "Ley para la igualdad real y efectiva de las personas trans",
        "prioridad": "BAJA"
    },
    {
        "nombre": "Ley_Transparencia",
        "nombre_completo": "Ley 19/2013 Transparencia",
        "boe_id": "BOE-A-2013-12887",
        "url": "https://www.boe.es/buscar/pdf/2013/BOE-A-2013-12887-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2013-12-09",
        "descripcion": "Ley de Transparencia, Acceso a la Información Pública y Buen Gobierno",
        "prioridad": "BAJA"
    },
    {
        "nombre": "Ley_General_Subvenciones",
        "nombre_completo": "Ley 38/2003 General de Subvenciones",
        "boe_id": "BOE-A-2003-20977",
        "url": "https://www.boe.es/buscar/pdf/2003/BOE-A-2003-20977-consolidado.pdf",
        "tipo": "ley",
        "nivel_jerarquia": 1,
        "fecha": "2003-11-17",
        "descripcion": "Ley General de Subvenciones",
        "prioridad": "BAJA"
    },
    {
        "nombre": "ENS_Esquema_Nacional_Seguridad",
        "nombre_completo": "RD 311/2022 Esquema Nacional de Seguridad",
        "boe_id": "BOE-A-2022-7191",
        "url": "https://www.boe.es/buscar/pdf/2022/BOE-A-2022-7191-consolidado.pdf",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "2022-05-03",
        "descripcion": "Esquema Nacional de Seguridad",
        "prioridad": "BAJA"
    },
    {
        "nombre": "ENI_Esquema_Nacional_Interoperabilidad",
        "nombre_completo": "RD 4/2010 Esquema Nacional de Interoperabilidad",
        "boe_id": "BOE-A-2010-1331",
        "url": "https://www.boe.es/buscar/pdf/2010/BOE-A-2010-1331-consolidado.pdf",
        "tipo": "reglamento",
        "nivel_jerarquia": 2,
        "fecha": "2010-01-08",
        "descripcion": "Esquema Nacional de Interoperabilidad",
        "prioridad": "BAJA"
    },
    {
        "nombre": "Ley_Igualdad_Efectiva",
        "nombre_completo": "Ley Orgánica 3/2007 Igualdad Efectiva",
        "boe_id": "BOE-A-2007-6115",
        "url": "https://www.boe.es/buscar/pdf/2007/BOE-A-2007-6115-consolidado.pdf",
        "tipo": "ley_organica",
        "nivel_jerarquia": 1,
        "fecha": "2007-03-22",
        "descripcion": "Ley Orgánica para la igualdad efectiva de mujeres y hombres",
        "prioridad": "BAJA"
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
leyes_exitosas = []
leyes_fallidas = []

for i, ley in enumerate(LEYES_RESTANTES, 1):
    print("\n" + "="*80)
    print(f"📄 LEY {i}/{len(LEYES_RESTANTES)}: {ley['nombre_completo']}")
    print(f"   Prioridad: {ley['prioridad']}")
    print("="*80)
    
    # PASO 1: Descargar
    print(f"\n⏳ Descargando desde BOE...")
    print(f"   URL: {ley['url']}")
    
    filepath = output_dir / f"{ley['nombre']}.pdf"
    
    try:
        response = requests.get(ley['url'], timeout=180)
        response.raise_for_status()
        filepath.write_bytes(response.content)
        size_mb = len(response.content) / (1024 * 1024)
        print(f"✅ Descargado: {size_mb:.2f} MB")
    except Exception as e:
        print(f"❌ Error descargando: {e}")
        leyes_fallidas.append({"ley": ley['nombre_completo'], "error": str(e), "paso": "descarga"})
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
            if (page_num + 1) % 50 == 0:
                print(f"   Procesadas {page_num+1}/{len(pdf.pages)} páginas...")
        
        print(f"✅ Texto extraído: {len(full_text)} caracteres")
    except Exception as e:
        print(f"❌ Error extrayendo texto: {e}")
        leyes_fallidas.append({"ley": ley['nombre_completo'], "error": str(e), "paso": "extraccion"})
        continue
    
    # PASO 3: Chunking
    print(f"\n✂️  Creando chunks...")
    CHUNK_SIZE = 512
    OVERLAP = 50
    
    try:
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
            
            if chunk_num % 50 == 0:
                print(f"   Creados {chunk_num} chunks...")
        
        print(f"✅ Chunks creados: {len(chunks)}")
        
        # Estadísticas de artículos
        articulos_detectados = [c['articulo'] for c in chunks if c['articulo']]
        articulos_unicos = sorted(set(articulos_detectados), key=lambda x: int(x) if x.isdigit() else 999)
        print(f"   Artículos detectados: {len(articulos_unicos)}")
        if articulos_unicos:
            print(f"   Rango: {articulos_unicos[0]} - {articulos_unicos[-1]}")
    except Exception as e:
        print(f"❌ Error en chunking: {e}")
        leyes_fallidas.append({"ley": ley['nombre_completo'], "error": str(e), "paso": "chunking"})
        continue
    
    # PASO 4: Generar embeddings
    print(f"\n🧠 Generando embeddings...")
    try:
        embeddings = []
        for j, chunk in enumerate(chunks):
            emb = generate_embedding(chunk['text'])
            embeddings.append(emb)
            
            if (j + 1) % 50 == 0:
                print(f"   Generados {j+1}/{len(chunks)} embeddings...")
        
        print(f"✅ Embeddings generados: {len(embeddings)}")
    except Exception as e:
        print(f"❌ Error generando embeddings: {e}")
        leyes_fallidas.append({"ley": ley['nombre_completo'], "error": str(e), "paso": "embeddings"})
        continue
    
    # PASO 5: Indexar en Qdrant
    print(f"\n💾 Indexando en Qdrant...")
    try:
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
            if (j + BATCH_SIZE) % 200 == 0:
                print(f"   Indexados {min(j+BATCH_SIZE, len(points))}/{len(points)} chunks...")
        
        print(f"✅ Indexación completada: {len(points)} chunks")
        total_chunks_indexados += len(points)
        leyes_exitosas.append({
            "ley": ley['nombre_completo'],
            "chunks": len(points),
            "articulos": len(articulos_unicos)
        })
    except Exception as e:
        print(f"❌ Error indexando: {e}")
        leyes_fallidas.append({"ley": ley['nombre_completo'], "error": str(e), "paso": "indexacion"})
        continue
    
    # Pequeña pausa entre leyes
    if i < len(LEYES_RESTANTES):
        print(f"\n⏸️  Pausa de 3 segundos antes de la siguiente ley...")
        time.sleep(3)

# RESUMEN FINAL
print("\n" + "="*80)
print("📊 RESUMEN FINAL DE INDEXACIÓN")
print("="*80)

print(f"\n✅ LEYES EXITOSAS ({len(leyes_exitosas)}/{len(LEYES_RESTANTES)}):")
for ley_info in leyes_exitosas:
    print(f"   ✅ {ley_info['ley']}: {ley_info['chunks']} chunks, {ley_info['articulos']} artículos")

if leyes_fallidas:
    print(f"\n❌ LEYES FALLIDAS ({len(leyes_fallidas)}/{len(LEYES_RESTANTES)}):")
    for ley_info in leyes_fallidas:
        print(f"   ❌ {ley_info['ley']}: Error en {ley_info['paso']} - {ley_info['error'][:100]}")

print(f"\n📊 Total chunks indexados: {total_chunks_indexados}")
print(f"📚 Leyes procesadas exitosamente: {len(leyes_exitosas)}/{len(LEYES_RESTANTES)}")
print("="*80)

# Verificar estadísticas finales
print("\n📊 ESTADÍSTICAS FINALES DE LA COLECCIÓN")
print("="*80)

collection_info = client.get_collection(collection_name)
print(f"Total puntos en colección: {collection_info.points_count}")
print(f"Vector size: {collection_info.config.params.vectors.size}")
print("="*80)
