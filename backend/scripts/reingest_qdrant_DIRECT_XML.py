#!/usr/bin/env python3
"""
Ingesta Qdrant DIRECTA desde XML BOE
Sin PostgreSQL, chunking híbrido inteligente
Parámetros optimizados: 1200 tokens, overlap 150
"""

import os
import json
import re
import pickle
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import argparse

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    SparseVectorParams, SparseVector, OptimizersConfigDiff
)
import numpy as np

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Modelo embeddings (CONFIRMADO)
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
EMBEDDING_DIM = 1024

# Chunking híbrido inteligente
MAX_TOKENS_PER_CHUNK = 1200  # Artículos <1200 tokens completos
OVERLAP_TOKENS = 150         # 12.5% overlap (balance)

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"

# Datos
XML_DIR = Path("/home/spas/OPOS_GEMINI_1/data/boe_xml")
BM25_VOCAB_PATH = Path("/home/spas/OPOS_GEMINI_1/backend/data/bm25_vocab.pkl")

# Modelos globales
_embedding_model = None
_bm25_vocab = None

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def load_embedding_model():
    """Carga modelo de embeddings"""
    global _embedding_model
    if _embedding_model is None:
        print(f"🤖 Cargando modelo {EMBEDDING_MODEL}...")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        print(f"✅ Modelo cargado")
    return _embedding_model

def load_bm25_vocab():
    """Carga vocabulario BM25"""
    global _bm25_vocab
    if _bm25_vocab is None and BM25_VOCAB_PATH.exists():
        print(f"📚 Cargando vocabulario BM25...")
        with open(BM25_VOCAB_PATH, 'rb') as f:
            bm25_data = pickle.load(f)
        
        # El pickle contiene un dict con 'vocab', 'idf', 'avgdl', etc.
        # Necesitamos solo el vocabulario {token: índice}
        if isinstance(bm25_data, dict) and 'vocab' in bm25_data:
            _bm25_vocab = bm25_data['vocab']
        else:
            # Formato antiguo: el pickle es directamente el vocabulario
            _bm25_vocab = bm25_data
        
        print(f"✅ Vocabulario BM25 cargado ({len(_bm25_vocab)} tokens)")
    return _bm25_vocab

def tokenize_simple(text: str) -> List[str]:
    """Tokenización simple por palabras"""
    return text.lower().split()

def count_tokens(text: str) -> int:
    """Cuenta tokens aproximados"""
    return len(tokenize_simple(text))

def generate_sparse_vector(text: str, vocab: Dict) -> SparseVector:
    """Genera vector sparse BM25-like"""
    if not vocab:
        return SparseVector(indices=[], values=[])
    
    tokens = tokenize_simple(text)
    token_counts = {}
    for token in tokens:
        token_counts[token] = token_counts.get(token, 0) + 1
    
    indices = []
    values = []
    
    for token, count in token_counts.items():
        if token in vocab:
            idx = vocab[token]
            # TF-IDF simplificado
            tf = count / len(tokens) if tokens else 0
            # CORRECCIÓN: Convertir índice a int (Qdrant requiere enteros)
            indices.append(int(idx))
            values.append(float(tf))
    
    return SparseVector(indices=indices, values=values)

def safe_get_text(obj, default=""):
    """Extrae texto de objeto XML"""
    if isinstance(obj, dict):
        return obj.get('_text', default)
    return str(obj) if obj else default

def safe_get_codigo(obj, default=""):
    """Extrae código de objeto XML"""
    if isinstance(obj, dict):
        return obj.get('codigo', default)
    return default

# ============================================================================
# CHUNKING HÍBRIDO
# ============================================================================

def extract_text_from_bloque(bloque: Dict) -> str:
    """
    Extrae texto de un bloque del XML BOE
    Maneja estructura recursiva de bloques
    """
    text_parts = []
    
    def extract_recursive(obj):
        if isinstance(obj, dict):
            # Extraer _text si existe
            if '_text' in obj:
                text_parts.append(obj['_text'])
            
            # Recursivo en todos los valores
            for value in obj.values():
                extract_recursive(value)
        
        elif isinstance(obj, list):
            for item in obj:
                extract_recursive(item)
        
        elif isinstance(obj, str):
            text_parts.append(obj)
    
    extract_recursive(bloque)
    return '\n'.join(text_parts)

def split_by_apartados(text: str) -> List[str]:
    """
    Split por apartados (1., 2., 3., etc.)
    Preserva semántica legal
    """
    # Regex para detectar apartados
    apartado_regex = r'^\s*(\d+)\.\s+'
    
    lines = text.split('\n')
    apartados = []
    current_apartado = []
    
    for line in lines:
        if re.match(apartado_regex, line.strip()):
            # Nuevo apartado
            if current_apartado:
                apartados.append('\n'.join(current_apartado))
            current_apartado = [line]
        else:
            if line.strip():  # Ignorar líneas vacías
                current_apartado.append(line)
    
    # Último apartado
    if current_apartado:
        apartados.append('\n'.join(current_apartado))
    
    return apartados if apartados else [text]

def chunk_article_hybrid(
    article_text: str,
    article_title: str,
    max_tokens: int = MAX_TOKENS_PER_CHUNK,
    overlap: int = OVERLAP_TOKENS
) -> List[Dict]:
    """
    Chunking híbrido inteligente:
    - Artículos <1200 tokens: 1 chunk completo
    - Artículos >1200 tokens: chunking semántico por apartados
    """
    if not article_text or not article_text.strip():
        return []
    
    tokens = tokenize_simple(article_text)
    
    # Si artículo pequeño, devolver completo
    if len(tokens) <= max_tokens:
        return [{
            "text": article_text,
            "article_title": article_title,
            "chunk_index": 0,
            "total_chunks": 1,
            "tokens": len(tokens)
        }]
    
    # Si artículo grande, chunking semántico por apartados
    apartados = split_by_apartados(article_text)
    
    if len(apartados) == 1:
        # No se pudo dividir por apartados, dividir por tokens
        chunks = []
        words = article_text.split()
        current_chunk = []
        current_tokens = 0
        
        for word in words:
            current_chunk.append(word)
            current_tokens += 1
            
            if current_tokens >= max_tokens:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    "text": chunk_text,
                    "article_title": article_title,
                    "chunk_index": len(chunks),
                    "total_chunks": "TBD",
                    "tokens": current_tokens
                })
                
                # Overlap
                current_chunk = current_chunk[-overlap:] if overlap < len(current_chunk) else current_chunk
                current_tokens = len(current_chunk)
        
        # Último chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "article_title": article_title,
                "chunk_index": len(chunks),
                "total_chunks": len(chunks) + 1,
                "tokens": len(current_chunk)
            })
        
        # Actualizar total_chunks
        for chunk in chunks:
            chunk["total_chunks"] = len(chunks)
        
        return chunks
    
    # Chunking por apartados
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for apartado in apartados:
        apartado_tokens = tokenize_simple(apartado)
        
        # Si apartado cabe en chunk actual, añadir
        if current_tokens + len(apartado_tokens) <= max_tokens:
            current_chunk.append(apartado)
            current_tokens += len(apartado_tokens)
        else:
            # Guardar chunk actual
            if current_chunk:
                chunk_text = '\n'.join(current_chunk)
                chunks.append({
                    "text": chunk_text,
                    "article_title": article_title,
                    "chunk_index": len(chunks),
                    "total_chunks": "TBD",
                    "tokens": count_tokens(chunk_text)
                })
            
            # Iniciar nuevo chunk con overlap
            if chunks and overlap > 0:
                # Overlap: últimos N tokens del chunk anterior
                last_chunk_text = chunks[-1]["text"]
                last_words = last_chunk_text.split()
                overlap_text = ' '.join(last_words[-overlap:]) if len(last_words) > overlap else last_chunk_text
                current_chunk = [overlap_text, apartado]
                current_tokens = len(tokenize_simple(overlap_text)) + len(apartado_tokens)
            else:
                current_chunk = [apartado]
                current_tokens = len(apartado_tokens)
    
    # Guardar último chunk
    if current_chunk:
        chunk_text = '\n'.join(current_chunk)
        chunks.append({
            "text": chunk_text,
            "article_title": article_title,
            "chunk_index": len(chunks),
            "total_chunks": len(chunks) + 1,
            "tokens": count_tokens(chunk_text)
        })
    
    # Actualizar total_chunks
    for chunk in chunks:
        chunk["total_chunks"] = len(chunks)
    
    return chunks

# ============================================================================
# PROCESAMIENTO XML
# ============================================================================

def process_law_xml(xml_path: Path) -> List[Dict]:
    """
    Procesa un archivo XML BOE y extrae chunks
    """
    print(f"\n📄 Procesando {xml_path.name}...")
    
    with open(xml_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    boe_id = xml_path.stem
    metadatos = data.get('data', {}).get('metadatos', {})
    analisis = data.get('data', {}).get('analisis', {})
    texto = data.get('data', {}).get('texto', {})
    
    law_name = safe_get_text(metadatos.get('titulo', {}))
    
    print(f"   Ley: {law_name[:80]}...")
    
    # Extraer bloques de texto
    bloques = texto.get('bloque', [])
    if not isinstance(bloques, list):
        bloques = [bloques]
    
    all_chunks = []
    article_count = 0
    
    for bloque in bloques:
        # Extraer texto del bloque
        bloque_text = extract_text_from_bloque(bloque)
        
        if not bloque_text or len(bloque_text.strip()) < 50:
            continue
        
        # Intentar extraer título del artículo
        article_title = f"Artículo {article_count + 1}"
        
        # Chunking híbrido
        chunks = chunk_article_hybrid(bloque_text, article_title)
        
        for chunk in chunks:
            chunk['boe_id'] = boe_id
            chunk['law_name'] = law_name
            chunk['metadatos'] = metadatos
            chunk['analisis'] = analisis
        
        all_chunks.extend(chunks)
        article_count += 1
    
    print(f"   ✅ {len(all_chunks)} chunks generados ({article_count} artículos)")
    
    return all_chunks

# ============================================================================
# QDRANT
# ============================================================================

def create_collection(client: QdrantClient, recreate: bool = False):
    """Crea colección Qdrant con búsqueda híbrida"""
    
    collections = [c.name for c in client.get_collections().collections]
    
    if COLLECTION_NAME in collections:
        if recreate:
            print(f"🗑️  Eliminando colección {COLLECTION_NAME}...")
            client.delete_collection(COLLECTION_NAME)
        else:
            print(f"✅ Colección {COLLECTION_NAME} ya existe")
            return
    
    print(f"📦 Creando colección {COLLECTION_NAME}...")
    
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "dense": VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE
            )
        },
        sparse_vectors_config={
            "text": SparseVectorParams()  # BM25
        },
        optimizers_config=OptimizersConfigDiff(
            indexing_threshold=10000
        )
    )
    
    print(f"✅ Colección {COLLECTION_NAME} creada")

def build_chunk_payload(chunk: Dict, analisis_data: Dict) -> Dict:
    """Construye payload con TODOS los metadatos XML"""
    
    boe_id = chunk['boe_id']
    meta = analisis_data.get('metadatos', {})
    anal = analisis_data.get('analisis', {})
    
    # Payload base
    payload = {
        "boe_id": boe_id,
        "law_name": chunk['law_name'],
        "article_title": chunk['article_title'],
        "text_snippet": chunk['text'][:500],
        "chunk_index": chunk['chunk_index'],
        "total_chunks": chunk['total_chunks'],
        "tokens": chunk['tokens'],
        
        # ORGANISMO EMISOR
        "organismo_emisor": safe_get_text(meta.get('departamento', {})),
        "departamento_codigo": safe_get_codigo(meta.get('departamento', {})),
        
        # FECHAS
        "fecha_publicacion": safe_get_text(meta.get('fecha_publicacion', {})),
        "fecha_vigencia": safe_get_text(meta.get('fecha_vigencia', {})),
        "fecha_disposicion": safe_get_text(meta.get('fecha_disposicion', {})),
        
        # VIGENCIA
        "vigente": safe_get_text(meta.get('estatus_derogacion', {}), 'N') == 'N',
        "estatus_derogacion": safe_get_text(meta.get('estatus_derogacion', {}), 'N'),
        "estado_consolidacion": safe_get_text(meta.get('estado_consolidacion', {})),
        
        # NORMATIVA
        "rango": safe_get_text(meta.get('rango', {})),
        "rango_codigo": safe_get_codigo(meta.get('rango', {})),
        
        # URLS
        "url_boe": safe_get_text(meta.get('url_html_consolidada', {})),
        "url_eli": safe_get_text(meta.get('url_eli', {})),
        
        # MATERIAS
        "materias": [safe_get_text(m) for m in anal.get('materias', {}).get('materia', [])],
        
        # METADATA XML COMPLETO
        "metadata_xml": {
            "metadatos": meta,
            "analisis": anal,
            "boe_id": boe_id,
            "fecha_ingesta": datetime.now().isoformat()
        }
    }
    
    return payload

def ingest_chunks(client: QdrantClient, chunks: List[Dict], model, vocab):
    """Ingesta chunks en Qdrant con batches pequeños"""
    
    BATCH_SIZE = 50
    total_chunks = len(chunks)
    
    print(f"\n📤 Ingesta de {total_chunks} chunks en batches de {BATCH_SIZE}...")
    
    for batch_start in range(0, total_chunks, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total_chunks)
        batch_chunks = chunks[batch_start:batch_end]
        batch_num = (batch_start // BATCH_SIZE) + 1
        total_batches = (total_chunks + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"\n📦 Batch {batch_num}/{total_batches} ({batch_start+1}-{batch_end}/{total_chunks})")
        
        points = []
        
        for i, chunk in enumerate(batch_chunks):
            # Generar embeddings
            dense_vector = model.encode(chunk['text']).tolist()
            sparse_vector = generate_sparse_vector(chunk['text'], vocab)
            
            # Payload
            payload = build_chunk_payload(chunk, {
                'metadatos': chunk['metadatos'],
                'analisis': chunk['analisis']
            })
            
            # ID único
            chunk_id = hashlib.md5(
                f"{chunk['boe_id']}_{chunk['article_title']}_{chunk['chunk_index']}".encode()
            ).hexdigest()
            
            point = PointStruct(
                id=chunk_id,
                vector={
                    "dense": dense_vector,
                    "text": sparse_vector
                },
                payload=payload
            )
            
            points.append(point)
        
        # Upsert batch con confirmación
        try:
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=points,
                wait=True  # Esperar confirmación
            )
            print(f"   ✅ Batch {batch_num} ingresado ({len(points)} chunks)")
        except Exception as e:
            print(f"   ❌ Error en batch {batch_num}: {e}")
            raise
    
    print(f"\n✅ Total ingresado: {total_chunks} chunks en {total_batches} batches")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Ingesta Qdrant directa desde XML BOE")
    parser.add_argument("--test", action="store_true", help="Modo prueba (1 ley)")
    parser.add_argument("--recreate", action="store_true", help="Recrear colección")
    parser.add_argument("--law", type=str, help="BOE-ID específico para test")
    args = parser.parse_args()
    
    print("=" * 80)
    print("🚀 INGESTA QDRANT DIRECTA DESDE XML BOE")
    print("=" * 80)
    print(f"Modelo: {EMBEDDING_MODEL}")
    print(f"Chunk size: {MAX_TOKENS_PER_CHUNK} tokens")
    print(f"Overlap: {OVERLAP_TOKENS} tokens ({OVERLAP_TOKENS/MAX_TOKENS_PER_CHUNK*100:.1f}%)")
    print(f"Modo: {'PRUEBA (1 ley)' if args.test else 'COMPLETO (54 leyes)'}")
    print("=" * 80)
    
    # Conectar Qdrant
    print(f"\n🔗 Conectando a Qdrant: {QDRANT_URL}")
    client = QdrantClient(url=QDRANT_URL, timeout=300)  # Timeout aumentado
    print("✅ Conectado a Qdrant")
    
    # Cargar modelos
    model = load_embedding_model()
    vocab = load_bm25_vocab()
    
    # Crear colección
    create_collection(client, recreate=args.recreate)
    
    # Obtener archivos XML
    xml_files = list(XML_DIR.glob("*.json"))
    
    # Filtrar archivos no válidos (que empiecen con _ o no sean BOE-A-*)
    xml_files = [f for f in xml_files if not f.stem.startswith('_') and f.stem.startswith('BOE-A-')]
    
    print(f"\n📂 Encontrados {len(xml_files)} archivos XML válidos")
    
    if args.test:
        # Modo prueba: 1 ley
        test_law = args.law or "BOE-A-2015-11724"  # LGSS por defecto
        xml_files = [f for f in xml_files if f.stem == test_law]
        
        if not xml_files:
            print(f"❌ No se encontró {test_law}")
            return
        
        print(f"\n🧪 MODO PRUEBA: {test_law}")
    
    # Procesar leyes
    total_chunks = 0
    
    for xml_file in xml_files:
        chunks = process_law_xml(xml_file)
        
        if chunks:
            ingest_chunks(client, chunks, model, vocab)
            total_chunks += len(chunks)
    
    # Resumen
    print("\n" + "=" * 80)
    print("✅ INGESTA COMPLETADA")
    print("=" * 80)
    print(f"Leyes procesadas: {len(xml_files)}")
    print(f"Chunks totales: {total_chunks}")
    print(f"Colección: {COLLECTION_NAME}")
    print("=" * 80)

if __name__ == "__main__":
    main()
