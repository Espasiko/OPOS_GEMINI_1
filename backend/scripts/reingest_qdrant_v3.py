#!/usr/bin/env python3
"""
REINGEST QDRANT V3 - FASE 0
===========================
Crea 2 colecciones en Qdrant:
1. opositaia_knowledge_v2 (chunks con embeddings)
2. opositaia_leyes_master (leyes completas sin embeddings)

Fuentes:
- JSONs de data/boe_xml/ → análisis completo
- PostgreSQL laws → chunks de texto

Uso:
    python reingest_qdrant_v3.py --test  # Solo 1 ley
    python reingest_qdrant_v3.py         # Todas las leyes
"""

import asyncio
import json
import hashlib
import re
import os
import sys
from glob import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse

# Añadir path del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncpg
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    CreateCollection, OptimizersConfigDiff,
    SparseVector, SparseVectorParams
)
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import re
from collections import Counter

# Configuración
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
POSTGRES_DSN = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/opositaia"
)
JSON_DIR = Path(__file__).parent.parent.parent / "data" / "boe_xml"
BM25_VOCAB_FILE = Path(__file__).parent.parent / "data" / "bm25_vocab.pkl"

# Modelo de embeddings (el mismo que usas en producción)
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
EMBEDDING_DIM = 1024

# Colecciones
COL_CHUNKS = "opositaia_knowledge_v2"
COL_MASTER = "opositaia_leyes_master"

# Variables globales (singleton)
_embedding_model = None
_bm25_data = None

def load_embedding_model():
    """Carga el modelo de embeddings (singleton)"""
    global _embedding_model
    if _embedding_model is None:
        print(f"🤖 Cargando modelo de embeddings: {EMBEDDING_MODEL}...")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        print(f"✅ Modelo cargado. Dimensión: {_embedding_model.get_sentence_embedding_dimension()}")
    return _embedding_model

def load_bm25_vocab():
    """Carga vocabulario BM25 (singleton)"""
    global _bm25_data
    if _bm25_data is None:
        print(f"📚 Cargando vocabulario BM25 de {BM25_VOCAB_FILE}...")
        with open(BM25_VOCAB_FILE, 'rb') as f:
            _bm25_data = pickle.load(f)
        print(f"✅ BM25 vocab: {len(_bm25_data['vocab']):,} términos, avgdl={_bm25_data['avgdl']:.1f}")
    return _bm25_data

def tokenize_legal(text: str) -> List[str]:
    """Tokeniza texto legal para BM25"""
    text = text.lower()
    tokens = re.findall(r'[a-záéíóúñ0-9]+', text)
    stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'se', 'por', 'para', 'con', 'un', 'una', 'al', 'lo', 'su', 'sus'}
    return [t for t in tokens if len(t) > 2 and t not in stopwords]

def generate_sparse_vector(text: str) -> SparseVector:
    """Genera sparse vector BM25 para un texto"""
    bm25 = load_bm25_vocab()
    vocab = bm25['vocab']
    idf_dict = bm25['idf']
    avgdl = bm25['avgdl']
    k1 = bm25['k1']
    b = bm25['b']
    
    tokens = tokenize_legal(text)
    term_freq = Counter(tokens)
    doc_len = len(tokens)
    
    indices, values = [], []
    for term, freq in term_freq.items():
        if term in vocab:
            idx = vocab[term]
            idf_score = idf_dict.get(idx, 0)
            score = idf_score * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / avgdl))
            if score > 0.01:
                indices.append(idx)
                values.append(float(score))
    
    return SparseVector(indices=indices, values=values)

def generate_embedding(text: str) -> List[float]:
    """Genera embedding para un texto"""
    model = load_embedding_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()



def compute_hash(text: str) -> str:
    """Genera hash MD5 del texto para deduplicación"""
    return hashlib.md5(text.encode()).hexdigest()[:16]


def extract_article_number(article_title: str) -> str:
    """Extrae número de artículo del título
    
    Ejemplos:
        "Artículo 173. Nacimiento..." → "173"
        "Art. 25 bis. ..." → "25 bis"
        "Disposición final segunda" → "DF2"
    """
    if not article_title:
        return ""
    
    # Patrón: Artículo/Art. seguido de número
    match = re.search(r'Art[íi]culo\s+(\d+(?:\s*bis)?)', article_title, re.IGNORECASE)
    if match:
        return match.group(1).replace(' ', '')
    
    # Disposiciones
    if 'Disposición' in article_title:
        if 'adicional' in article_title.lower():
            match = re.search(r'(primera|segunda|tercera|cuarta|quinta|\d+)', article_title.lower())
            return f"DA{match.group(1)[:3] if match else ''}"
        elif 'final' in article_title.lower():
            match = re.search(r'(primera|segunda|tercera|cuarta|quinta|\d+)', article_title.lower())
            return f"DF{match.group(1)[:3] if match else ''}"
        elif 'transitoria' in article_title.lower():
            return "DT"
        elif 'derogatoria' in article_title.lower():
            return "DD"
    
    return ""


def load_json_analysis(json_dir: Path) -> Dict[str, Dict]:
    """Carga análisis de todos los JSONs del BOE"""
    analisis_por_ley = {}
    
    json_files = list(json_dir.glob("*.json"))
    print(f"📂 Encontrados {len(json_files)} archivos JSON en {json_dir}")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extraer boe_id
            metadatos = data.get('data', {}).get('metadatos', {})
            boe_id = metadatos.get('identificador', {}).get('_text', '')
            
            if not boe_id:
                # Intentar extraer del nombre del archivo
                boe_id = json_file.stem
            
            # Extraer análisis
            analisis = data.get('data', {}).get('analisis', {})
            
            # Extraer referencias anteriores/posteriores
            referencias = analisis.get('referencias', {})
            anteriores = referencias.get('anteriores', {}).get('anterior', [])
            posteriores = referencias.get('posteriores', {}).get('posterior', [])
            
            # Normalizar a listas
            if isinstance(anteriores, dict):
                anteriores = [anteriores]
            if isinstance(posteriores, dict):
                posteriores = [posteriores]
            
            # Extraer materias
            materias_raw = analisis.get('materias', {}).get('materia', [])
            if isinstance(materias_raw, dict):
                materias_raw = [materias_raw]
            materias = [m.get('_text', '') for m in materias_raw if isinstance(m, dict)]
            
            # Calcular última modificación
            ultima_mod = None
            modificado_por = []
            for post in posteriores:
                if isinstance(post, dict):
                    id_norma = post.get('id_norma', {})
                    if isinstance(id_norma, dict):
                        mod_id = id_norma.get('_text', '')
                        if mod_id:
                            modificado_por.append(mod_id)
            
            analisis_por_ley[boe_id] = {
                'metadatos': {
                    'titulo': metadatos.get('titulo', {}).get('_text', ''),
                    'rango': metadatos.get('rango', {}).get('_text', ''),
                    'departamento': metadatos.get('departamento', {}).get('_text', ''),
                    'fecha_publicacion': metadatos.get('fecha_publicacion', {}).get('_text', ''),
                    'fecha_vigencia': metadatos.get('fecha_vigencia', {}).get('_text', ''),
                    'estatus_derogacion': metadatos.get('estatus_derogacion', {}).get('_text', 'N'),
                    'vigencia_agotada': metadatos.get('vigencia_agotada', {}).get('_text', 'N'),
                    'url_eli': metadatos.get('url_eli', {}).get('_text', ''),
                    'url_html': metadatos.get('url_html_consolidada', {}).get('_text', ''),
                },
                'analisis': {
                    'anteriores': anteriores,
                    'posteriores': posteriores,
                    'materias': materias,
                },
                'modificado_por': modificado_por,
                'ultima_modificacion': ultima_mod,
            }
            
        except Exception as e:
            print(f"⚠️ Error procesando {json_file}: {e}")
            continue
    
    print(f"✅ Cargados análisis de {len(analisis_por_ley)} leyes")
    return analisis_por_ley


async def get_chunks_from_postgres(
    pool: asyncpg.Pool,
    boe_ids: Optional[List[str]] = None
) -> List[Dict]:
    """Obtiene chunks de la tabla laws"""
    
    # Columnas reales: id, law_id, law_name, title, content, created_at, xml_content, metadata
    query = """
        SELECT 
            id,
            law_id as boe_id,
            law_name,
            title as article_title,
            content as text_snippet,
            'article_chunk' as layer
        FROM laws
    """
    
    if boe_ids:
        query += " WHERE law_id = ANY($1)"
        rows = await pool.fetch(query, boe_ids)
    else:
        rows = await pool.fetch(query)
    
    return [dict(row) for row in rows]


async def create_collection_v2(client: QdrantClient, recreate: bool = False):
    """Crea colección para chunks con embeddings"""
    
    collections = [c.name for c in client.get_collections().collections]
    
    if COL_CHUNKS in collections:
        if recreate:
            print(f"🗑️ Borrando colección existente {COL_CHUNKS}...")
            client.delete_collection(COL_CHUNKS)
        else:
            print(f"⚠️ Colección {COL_CHUNKS} ya existe, saltando creación")
            return
    
    print(f"📦 Creando colección {COL_CHUNKS}...")
    client.create_collection(
        collection_name=COL_CHUNKS,
        vectors_config={
            "dense": VectorParams(
                size=1024,  # BGE-M3
                distance=Distance.COSINE
            )
        },
        # Sparse vectors para hybrid search
        sparse_vectors_config={
            "text": {}
        },
        optimizers_config=OptimizersConfigDiff(
            indexing_threshold=20000
        )
    )
    print(f"✅ Colección {COL_CHUNKS} creada")


async def create_collection_master(client: QdrantClient, recreate: bool = False):
    """Crea colección para leyes completas SIN embeddings"""
    
    collections = [c.name for c in client.get_collections().collections]
    
    if COL_MASTER in collections:
        if recreate:
            print(f"🗑️ Borrando colección existente {COL_MASTER}...")
            client.delete_collection(COL_MASTER)
        else:
            print(f"⚠️ Colección {COL_MASTER} ya existe, saltando creación")
            return
    
    print(f"📦 Creando colección {COL_MASTER} (sin embeddings)...")
    # Colección sin vectores - solo para almacenar payload
    client.create_collection(
        collection_name=COL_MASTER,
        vectors_config={}  # Sin vectores
    )
    print(f"✅ Colección {COL_MASTER} creada")


def build_chunk_payload(chunk: Dict, analisis_data: Optional[Dict]) -> Dict:
    """Construye payload enriquecido para un chunk"""
    
    boe_id = chunk['boe_id']
    article_number = extract_article_number(chunk['article_title'] or '')
    
    # Extraer apartado del título si existe (ej: "173.2" -> apartado="2")
    apartado = ""
    if article_number and '.' in str(article_number):
        parts = str(article_number).split('.')
        if len(parts) > 1:
            apartado = parts[1]
            article_number = parts[0]
    
    # Datos base
    payload = {
        # IDENTIDAD
        "boe_id": boe_id,
        "hash_texto": compute_hash(chunk['text_snippet'] or ''),
        
        # ESTRUCTURA - SEGÚN PLAN L49-53
        "law_name": chunk['law_name'] or '',
        "article_number": article_number,
        "apartado": apartado,  # NUEVO según plan L50
        "titulo_articulo": chunk['article_title'] or '',
        
        # CONTENIDO
        "texto": chunk['text_snippet'] or '',
        
        # LAYER
        "layer": chunk['layer'] or 'article_chunk',
    }
    
    # Enriquecer con datos del JSON si existe
    if analisis_data:
        meta = analisis_data.get('metadatos', {})
        anal = analisis_data.get('analisis', {})
        
        # Extraer deroga_a de anteriores (relacion = DEROGA)
        deroga_a = []
        for ant in anal.get('anteriores', []):
            if isinstance(ant, dict):
                relacion = ant.get('relacion', {})
                if isinstance(relacion, dict) and relacion.get('codigo') == '210':  # 210 = DEROGA
                    id_norma = ant.get('id_norma', {})
                    if isinstance(id_norma, dict):
                        deroga_a.append(id_norma.get('_text', ''))
        
        # Extraer derogado_por de posteriores (relacion = SE DEROGA)
        derogado_por = None
        for post in anal.get('posteriores', []):
            if isinstance(post, dict):
                relacion = post.get('relacion', {})
                if isinstance(relacion, dict) and 'DEROGA' in relacion.get('_text', '').upper():
                    id_norma = post.get('id_norma', {})
                    if isinstance(id_norma, dict):
                        derogado_por = id_norma.get('_text', '')
                        break  # Solo el primero
        
        payload.update({
            # VIGENCIA - SEGÚN PLAN L57-62
            "vigente": meta.get('estatus_derogacion', 'N') == 'N',
            "fecha_vigencia": meta.get('fecha_vigencia', ''),
            "ultima_modificacion": analisis_data.get('ultima_modificacion', ''),
            "modificado_por": analisis_data.get('modificado_por', []),
            "deroga_a": deroga_a,  # NUEVO según plan L61
            "derogado_por": derogado_por,  # NUEVO según plan L62
            
            # NORMATIVA
            "rango": meta.get('rango', ''),
            "departamento": meta.get('departamento', ''),
            
            # NAVEGACIÓN - SEGÚN PLAN L65-66
            "url_boe": f"{meta.get('url_html', '')}#a{article_number}" if meta.get('url_html') else '',
            "url_eli": meta.get('url_eli', ''),
            
            # MATERIAS
            "materias": anal.get('materias', []),
        })
    else:
        # Valores por defecto si no hay JSON
        payload.update({
            "vigente": True,
            "fecha_vigencia": "",
            "ultima_modificacion": "",
            "modificado_por": [],
            "deroga_a": [],
            "derogado_por": None,
            "rango": "",
            "departamento": "",
            "url_boe": "",
            "url_eli": "",
            "materias": [],
        })
    
    return payload


def build_master_payload(boe_id: str, analisis_data: Dict) -> Dict:
    """Construye payload completo para colección master"""
    
    meta = analisis_data.get('metadatos', {})
    anal = analisis_data.get('analisis', {})
    
    return {
        # IDENTIDAD
        "boe_id": boe_id,
        "titulo": meta.get('titulo', ''),
        
        # VIGENCIA
        "vigente": meta.get('estatus_derogacion', 'N') == 'N',
        "fecha_publicacion": meta.get('fecha_publicacion', ''),
        "fecha_vigencia": meta.get('fecha_vigencia', ''),
        "estatus_derogacion": meta.get('estatus_derogacion', 'N'),
        "vigencia_agotada": meta.get('vigencia_agotada', 'N'),
        
        # NORMATIVA
        "rango": meta.get('rango', ''),
        "departamento": meta.get('departamento', ''),
        
        # NAVEGACIÓN
        "url_boe": meta.get('url_html', ''),
        "url_eli": meta.get('url_eli', ''),
        
        # ANÁLISIS COMPLETO
        "analisis_completo": {
            "anteriores": anal.get('anteriores', []),
            "posteriores": anal.get('posteriores', []),
            "materias": anal.get('materias', []),
        },
        
        # CONTADORES
        "num_anteriores": len(anal.get('anteriores', [])),
        "num_posteriores": len(anal.get('posteriores', [])),
        "modificado_por": analisis_data.get('modificado_por', []),
    }


async def ingest_all_laws(
    qdrant: QdrantClient,
    pool: asyncpg.Pool,
    analisis_por_ley: Dict
):
    """Ingesta TODAS las leyes (54) con embeddings híbridos"""
    
    print(f"\n📤 INGESTA COMPLETA - {len(analisis_por_ley)} leyes")
    
    # 1. Obtener lista de BOE-IDs
    boe_ids = list(analisis_por_ley.keys())
    print(f"   BOE-IDs: {len(boe_ids)}")
    
    # 2. Crear colecciones
    await create_collection_v2(qdrant, recreate=True)
    await create_collection_master(qdrant, recreate=True)
    
    # 3. Cargar modelos
    print(f"\n🤖 Cargando modelos...")
    load_embedding_model()
    load_bm25_vocab()
    
    # 4. Obtener TODOS los chunks de PostgreSQL
    print(f"\n📚 Obteniendo chunks de PostgreSQL...")
    all_chunks = await get_chunks_from_postgres(pool, boe_ids)
    print(f"   Total chunks: {len(all_chunks)}")
    
    # 5. Agrupar chunks por ley para enriquecer con análisis
    chunks_by_law = {}
    for chunk in all_chunks:
        boe_id = chunk['boe_id']
        if boe_id not in chunks_by_law:
            chunks_by_law[boe_id] = []
        chunks_by_law[boe_id].append(chunk)
    
    print(f"   Leyes con chunks: {len(chunks_by_law)}")
    
    # 6. Ingestar chunks en colección v2
    print(f"\n📤 Ingesta en {COL_CHUNKS}...")
    
    points = []
    global_id = 0
    batch_size = 50
    
    for law_idx, (boe_id, chunks) in enumerate(chunks_by_law.items()):
        analisis_data = analisis_por_ley.get(boe_id, {})
        
        # Procesar chunks de esta ley en batches
        for batch_start in range(0, len(chunks), batch_size):
            batch_chunks = chunks[batch_start:batch_start + batch_size]
            
            # Generar embeddings dense
            texts = [c['text_snippet'] or '' for c in batch_chunks]
            dense_embeddings = load_embedding_model().encode(texts, normalize_embeddings=True)
            
            for j, (chunk, dense_vec) in enumerate(zip(batch_chunks, dense_embeddings)):
                payload = build_chunk_payload(chunk, analisis_data)
                text = chunk['text_snippet'] or ''
                sparse_vec = generate_sparse_vector(text)
                
                points.append(PointStruct(
                    id=global_id,
                    vector={
                        "dense": dense_vec.tolist(),
                        "text": sparse_vec
                    },
                    payload=payload
                ))
                global_id += 1
        
        # Mostrar progreso por ley
        print(f"   [{law_idx + 1}/{len(chunks_by_law)}] {boe_id}: {len(chunks)} chunks", end='\r')
    
    print(f"\n   ✅ {len(points)} embeddings (dense+sparse) generados")
    
    # 7. Subir en lotes a Qdrant
    print(f"   Subiendo a Qdrant...")
    upload_batch_size = 100
    for i in range(0, len(points), upload_batch_size):
        batch = points[i:i+upload_batch_size]
        qdrant.upsert(
            collection_name=COL_CHUNKS,
            points=batch
        )
        print(f"   [{min(i+upload_batch_size, len(points))}/{len(points)}] subidos...", end='\r')
    
    print(f"\n✅ Ingesta {len(points)} chunks (híbrido) en {COL_CHUNKS}")
    
    # 8. Ingestar en colección master
    print(f"\n📤 Ingesta en {COL_MASTER}...")
    master_points = []
    
    for idx, (boe_id, analisis_data) in enumerate(analisis_por_ley.items()):
        master_payload = build_master_payload(boe_id, analisis_data)
        master_points.append(PointStruct(
            id=idx,
            vector={},
            payload=master_payload
        ))
    
    qdrant.upsert(
        collection_name=COL_MASTER,
        points=master_points
    )
    print(f"✅ Ingesta {len(master_points)} leyes en {COL_MASTER}")
    
    # 9. Verificar
    print("\n📊 VERIFICACIÓN:")
    
    col_info = qdrant.get_collection(COL_CHUNKS)
    print(f"\n{COL_CHUNKS}:")
    print(f"  - Puntos: {col_info.points_count}")
    print(f"  - Vectores indexados: {col_info.indexed_vectors_count}")
    
    col_info_master = qdrant.get_collection(COL_MASTER)
    print(f"\n{COL_MASTER}:")
    print(f"  - Puntos: {col_info_master.points_count}")


async def ingest_test_law(
    qdrant: QdrantClient,
    pool: asyncpg.Pool,
    analisis_por_ley: Dict,
    test_boe_id: str = "BOE-A-2015-11724"  # TRLGSS por defecto
):
    """Ingesta UNA ley como prueba"""
    
    print(f"\n🧪 MODO TEST: Ingesta solo {test_boe_id}")
    
    # 1. Obtener chunks de esta ley
    chunks = await get_chunks_from_postgres(pool, [test_boe_id])
    print(f"📄 Encontrados {len(chunks)} chunks para {test_boe_id}")
    
    if not chunks:
        print(f"❌ No hay chunks para {test_boe_id}")
        return
    
    # 2. Obtener análisis
    analisis_data = analisis_por_ley.get(test_boe_id, {})
    if analisis_data:
        print(f"✅ Análisis encontrado para {test_boe_id}")
        meta = analisis_data.get('metadatos', {})
        print(f"   - Título: {meta.get('titulo', 'N/A')[:60]}...")
        print(f"   - Rango: {meta.get('rango', 'N/A')}")
        anal = analisis_data.get('analisis', {})
        print(f"   - Anteriores: {len(anal.get('anteriores', []))}")
        print(f"   - Posteriores: {len(anal.get('posteriores', []))}")
    else:
        print(f"⚠️ No hay análisis JSON para {test_boe_id}")
    
    # 3. Crear colecciones de test
    await create_collection_v2(qdrant, recreate=True)
    await create_collection_master(qdrant, recreate=True)
    
    # 4. Cargar modelos
    print(f"\n🤖 Cargando modelos...")
    load_embedding_model()
    load_bm25_vocab()
    
    # 5. Ingestar chunks en colección v2
    print(f"\n📤 Ingesta en {COL_CHUNKS}...")
    print(f"   Generando embeddings (dense + sparse) para {len(chunks)} chunks...")
    
    points = []
    batch_size = 50  # Procesar en lotes para mostrar progreso
    
    for batch_start in range(0, len(chunks), batch_size):
        batch_chunks = chunks[batch_start:batch_start + batch_size]
        
        # Generar embeddings DENSE para el batch
        texts = [c['text_snippet'] or '' for c in batch_chunks]
        dense_embeddings = load_embedding_model().encode(texts, normalize_embeddings=True)
        
        for j, (chunk, dense_vec) in enumerate(zip(batch_chunks, dense_embeddings)):
            payload = build_chunk_payload(chunk, analisis_data)
            text = chunk['text_snippet'] or ''
            
            # Generar sparse vector BM25
            sparse_vec = generate_sparse_vector(text)
            
            points.append(PointStruct(
                id=batch_start + j,
                vector={
                    "dense": dense_vec.tolist(),
                    "text": sparse_vec  # Sparse BM25
                },
                payload=payload
            ))
        
        # Mostrar progreso
        progress = min(batch_start + batch_size, len(chunks))
        print(f"   [{progress}/{len(chunks)}] embeddings (dense+sparse) generados...", end='\r')
    
    print(f"\n   ✅ {len(points)} embeddings (dense + sparse) generados")
    
    # Subir en lotes a Qdrant
    print(f"   Subiendo a Qdrant...")
    upload_batch_size = 100
    for i in range(0, len(points), upload_batch_size):
        batch = points[i:i+upload_batch_size]
        qdrant.upsert(
            collection_name=COL_CHUNKS,
            points=batch
        )
        print(f"   [{min(i+upload_batch_size, len(points))}/{len(points)}] subidos...", end='\r')
    
    print(f"\n✅ Ingesta {len(points)} chunks (híbrido) en {COL_CHUNKS}")
    
    # 5. Ingestar en colección master
    print(f"\n📤 Ingesta en {COL_MASTER}...")
    if analisis_data:
        master_payload = build_master_payload(test_boe_id, analisis_data)
        
        # Usar upsert con punto sin vector
        qdrant.upsert(
            collection_name=COL_MASTER,
            points=[PointStruct(
                id=0,
                vector={},
                payload=master_payload
            )]
        )
        print(f"✅ Ingesta 1 ley en {COL_MASTER}")
    else:
        print(f"⚠️ Saltando {COL_MASTER} - no hay análisis")
    
    # 6. Verificar
    print("\n📊 VERIFICACIÓN:")
    
    # Colección v2
    col_info = qdrant.get_collection(COL_CHUNKS)
    print(f"\n{COL_CHUNKS}:")
    print(f"  - Puntos: {col_info.points_count}")
    print(f"  - Vectores: {col_info.indexed_vectors_count}")
    
    # Verificar un punto
    sample = qdrant.scroll(
        collection_name=COL_CHUNKS,
        limit=1,
        with_payload=True
    )[0]
    if sample:
        print(f"  - Campos en payload: {list(sample[0].payload.keys())}")
        print(f"  - Ejemplo boe_id: {sample[0].payload.get('boe_id')}")
        print(f"  - Ejemplo article_number: {sample[0].payload.get('article_number')}")
        print(f"  - Ejemplo vigente: {sample[0].payload.get('vigente')}")
    
    # Colección master
    col_info_master = qdrant.get_collection(COL_MASTER)
    print(f"\n{COL_MASTER}:")
    print(f"  - Puntos: {col_info_master.points_count}")
    
    sample_master = qdrant.scroll(
        collection_name=COL_MASTER,
        limit=1,
        with_payload=True
    )[0]
    if sample_master:
        print(f"  - Campos en payload: {list(sample_master[0].payload.keys())}")
        anal = sample_master[0].payload.get('analisis_completo', {})
        print(f"  - Anteriores: {len(anal.get('anteriores', []))}")
        print(f"  - Posteriores: {len(anal.get('posteriores', []))}")


async def main():
    parser = argparse.ArgumentParser(description='Reingest Qdrant v3')
    parser.add_argument('--test', action='store_true', help='Solo 1 ley de prueba')
    parser.add_argument('--boe-id', type=str, default='BOE-A-2015-11724',
                        help='BOE-ID para test (default: TRLGSS)')
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 REINGEST QDRANT V3 - FASE 0")
    print("=" * 60)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 JSONs: {JSON_DIR}")
    print(f"🔗 Qdrant: {QDRANT_URL}")
    print(f"🐘 Postgres: {POSTGRES_DSN}")
    print()
    
    # 1. Cargar análisis de JSONs
    analisis_por_ley = load_json_analysis(JSON_DIR)
    
    # 2. Conectar a PostgreSQL
    print("\n🐘 Conectando a PostgreSQL...")
    pool = await asyncpg.create_pool(POSTGRES_DSN)
    print("✅ Conectado a PostgreSQL")
    
    # 3. Conectar a Qdrant
    print("\n🔗 Conectando a Qdrant...")
    qdrant = QdrantClient(url=QDRANT_URL)
    print("✅ Conectado a Qdrant")
    
    try:
        if args.test:
            # Modo test: solo 1 ley
            await ingest_test_law(qdrant, pool, analisis_por_ley, args.boe_id)
        else:
            # Ingesta completa de todas las leyes
            await ingest_all_laws(qdrant, pool, analisis_por_ley)
    
    finally:
        await pool.close()
    
    print("\n" + "=" * 60)
    print("✅ FASE 0 COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
