#!/usr/bin/env python3
"""
REINGEST QDRANT FULL XML - VERSIÓN COMPLETA CON TODOS LOS METADATOS BOE
========================================================================

Crea colección opositaia_knowledge_FULL_XML con:
- Búsqueda híbrida: Dense (BGE-M3) + Sparse (BM25)
- TODOS los metadatos XML del BOE (50+ campos)
- Estructura optimizada para LLMs

Diferencias vs reingest_qdrant_v3.py:
- ✅ Incluye organismo_emisor, departamento_codigo
- ✅ Incluye fecha_actualizacion, estado_consolidacion
- ✅ Incluye analisis_modificaciones completo (anteriores/posteriores)
- ✅ Incluye analisis_afecta_a y analisis_afectada_por
- ✅ Incluye materias completas con códigos
- ✅ Incluye URLs completas (PDF, XML, consolidado)
- ✅ Incluye metadata_xml completo para LLMs

Uso:
    python reingest_qdrant_FULL_XML.py --test  # Solo 1 ley
    python reingest_qdrant_FULL_XML.py         # Todas las leyes
    python reingest_qdrant_FULL_XML.py --recreate  # Borrar y recrear
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

# Modelo de embeddings
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
EMBEDDING_DIM = 1024

# Colección NUEVA con metadatos completos
COL_FULL_XML = "opositaia_knowledge_FULL_XML"

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
    doc_len = len(tokens)
    
    if doc_len == 0:
        return SparseVector(indices=[], values=[])
    
    term_freq = Counter(tokens)
    
    indices = []
    values = []
    
    for term, freq in term_freq.items():
        if term in vocab:
            idx = vocab[term]
            idf = idf_dict.get(term, 0.0)
            
            # BM25 score
            score = idf * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / avgdl))
            
            indices.append(idx)
            values.append(float(score))
    
    return SparseVector(indices=indices, values=values)

def compute_hash(text: str) -> str:
    """Genera hash SHA256 de un texto"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

def extract_article_number(title: str) -> str:
    """Extrae número de artículo del título"""
    if not title:
        return ""
    
    patterns = [
        r'Artículo\s+(\d+(?:\.\d+)?)',
        r'Art\.\s+(\d+(?:\.\d+)?)',
        r'Disposición\s+(?:adicional|transitoria|final|derogatoria)\s+(\w+)',
        r'DA\s+(\d+)',
        r'DT\s+(\d+)',
        r'DF\s+(\d+)',
        r'DD\s+(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return ""

def safe_get_text(obj, default=""):
    """Extrae _text de un objeto JSON BOE de forma segura"""
    if isinstance(obj, dict):
        return obj.get('_text', default)
    elif isinstance(obj, str):
        return obj
    return default

def safe_get_codigo(obj, default=""):
    """Extrae codigo de un objeto JSON BOE de forma segura"""
    if isinstance(obj, dict):
        return obj.get('codigo', default)
    return default

def build_chunk_payload_FULL(chunk: Dict, analisis_data: Optional[Dict]) -> Dict:
    """
    Construye payload COMPLETO con TODOS los metadatos XML del BOE
    
    Incluye 50+ campos:
    - Identidad (boe_id, hash, titulo)
    - Estructura (article_number, apartado, layer)
    - Contenido (texto completo)
    - Organismo (organismo_emisor, departamento_codigo, departamento_nombre)
    - Fechas (publicacion, vigencia, actualizacion, derogacion)
    - Vigencia (vigente, consolidado, estado_consolidacion)
    - URLs (BOE, ELI, PDF, PDF consolidado, XML, HTML)
    - Análisis (modificaciones, afecta_a, afectada_por)
    - Materias (con códigos)
    - Relaciones (deroga_a, derogado_por, modificado_por)
    - Metadata XML completo (para LLMs)
    """
    
    boe_id = chunk['boe_id']
    article_number = extract_article_number(chunk['article_title'] or '')
    
    # Extraer apartado del título si existe (ej: "173.2" -> apartado="2")
    apartado = ""
    if article_number and '.' in str(article_number):
        parts = str(article_number).split('.')
        if len(parts) > 1:
            apartado = parts[1]
            article_number = parts[0]
    
    # PAYLOAD BASE (15 campos actuales)
    payload = {
        # IDENTIDAD
        "boe_id": boe_id,
        "hash_texto": compute_hash(chunk['text_snippet'] or ''),
        "postgres_id": chunk.get('id', ''),
        
        # ESTRUCTURA
        "law_name": chunk['law_name'] or '',
        "article_number": article_number,
        "article_title": chunk['article_title'] or '',
        "apartado": apartado,
        "layer": chunk['layer'] or 'article_chunk',
        
        # CONTENIDO
        "text_snippet": chunk['text_snippet'] or '',
        
        # SOURCE
        "source": "hybrid_sync_FULL_XML",
    }
    
    # ENRIQUECIMIENTO CON TODOS LOS METADATOS XML (35+ campos adicionales)
    if analisis_data:
        meta = analisis_data.get('metadatos', {})
        anal = analisis_data.get('analisis', {})
        
        # ORGANISMO EMISOR (3 campos) - NUEVO
        payload.update({
            "organismo_emisor": safe_get_text(meta.get('departamento', {})),
            "departamento_codigo": safe_get_codigo(meta.get('departamento', {})),
            "departamento_nombre": safe_get_text(meta.get('departamento', {})),
        })
        
        # FECHAS COMPLETAS (5 campos)
        payload.update({
            "fecha_publicacion": safe_get_text(meta.get('fecha_publicacion', {})),
            "fecha_vigencia": safe_get_text(meta.get('fecha_vigencia', {})),
            "fecha_disposicion": safe_get_text(meta.get('fecha_disposicion', {})),
            "fecha_actualizacion": safe_get_text(meta.get('fecha_actualizacion', {})),  # NUEVO
            "fecha_derogacion": None,  # Se calcula de analisis posteriores
        })
        
        # VIGENCIA Y CONSOLIDACIÓN (6 campos)
        estatus_derogacion = safe_get_text(meta.get('estatus_derogacion', {}), 'N')
        payload.update({
            "vigente": estatus_derogacion == 'N',
            "estatus_derogacion": estatus_derogacion,
            "estatus_anulacion": safe_get_text(meta.get('estatus_anulacion', {}), 'N'),
            "vigencia_agotada": safe_get_text(meta.get('vigencia_agotada', {}), 'N'),
            "estado_consolidacion": safe_get_text(meta.get('estado_consolidacion', {})),  # NUEVO
            "consolidado": safe_get_text(meta.get('estado_consolidacion', {})) == "Finalizado",  # NUEVO
        })
        
        # NORMATIVA (3 campos)
        payload.update({
            "rango": safe_get_text(meta.get('rango', {})),
            "rango_codigo": safe_get_codigo(meta.get('rango', {})),
            "numero_oficial": safe_get_text(meta.get('numero_oficial', {})),
        })
        
        # URLS COMPLETAS (6 campos) - NUEVO
        url_html = safe_get_text(meta.get('url_html_consolidada', {}))
        payload.update({
            "url_boe": url_html,
            "url_eli": safe_get_text(meta.get('url_eli', {})),
            "url_pdf": f"https://www.boe.es/boe/dias/{safe_get_text(meta.get('fecha_publicacion', {}))[:4]}/{safe_get_text(meta.get('fecha_publicacion', {}))[4:6]}/{safe_get_text(meta.get('fecha_publicacion', {}))[6:8]}/pdfs/{boe_id}.pdf" if meta.get('fecha_publicacion') else "",
            "url_pdf_consolidado": f"https://www.boe.es/buscar/pdf/{safe_get_text(meta.get('fecha_publicacion', {}))[:4]}/{boe_id}-consolidado.pdf" if meta.get('fecha_publicacion') else "",
            "url_xml": f"https://www.boe.es/diario_boe/xml.php?id={boe_id}",
            "url_html_consolidada": url_html,
        })
        
        # MATERIAS COMPLETAS CON CÓDIGOS (1 campo JSONB) - NUEVO
        materias_list = anal.get('materias', {})
        if isinstance(materias_list, dict):
            materias_list = materias_list.get('materia', [])
        if not isinstance(materias_list, list):
            materias_list = [materias_list] if materias_list else []
        
        materias_completas = []
        for mat in materias_list:
            if isinstance(mat, dict):
                materias_completas.append({
                    "codigo": safe_get_codigo(mat),
                    "nombre": safe_get_text(mat)
                })
        
        payload["materias"] = [m["nombre"] for m in materias_completas]  # Lista simple para búsqueda
        payload["materias_completas"] = materias_completas  # NUEVO: Con códigos
        
        # ANÁLISIS MODIFICACIONES (3 campos JSONB) - NUEVO
        anteriores = anal.get('anteriores', [])
        if not isinstance(anteriores, list):
            anteriores = [anteriores] if anteriores else []
        
        posteriores = anal.get('posteriores', [])
        if not isinstance(posteriores, list):
            posteriores = [posteriores] if posteriores else []
        
        # Procesar anteriores (leyes que esta ley afecta)
        analisis_afecta_a = []
        deroga_a = []
        for ant in anteriores:
            if isinstance(ant, dict):
                id_norma = safe_get_text(ant.get('id_norma', {}))
                relacion_text = safe_get_text(ant.get('relacion', {}))
                relacion_codigo = safe_get_codigo(ant.get('relacion', {}))
                
                if id_norma:
                    item = {
                        "boe_id": id_norma,
                        "relacion": relacion_text,
                        "relacion_codigo": relacion_codigo
                    }
                    analisis_afecta_a.append(item)
                    
                    # Si es derogación (código 210), añadir a deroga_a
                    if relacion_codigo == '210' or 'DEROGA' in relacion_text.upper():
                        deroga_a.append(id_norma)
        
        # Procesar posteriores (leyes que afectan a esta)
        analisis_afectada_por = []
        derogado_por = None
        modificado_por = []
        for post in posteriores:
            if isinstance(post, dict):
                id_norma = safe_get_text(post.get('id_norma', {}))
                relacion_text = safe_get_text(post.get('relacion', {}))
                relacion_codigo = safe_get_codigo(post.get('relacion', {}))
                
                if id_norma:
                    item = {
                        "boe_id": id_norma,
                        "relacion": relacion_text,
                        "relacion_codigo": relacion_codigo
                    }
                    analisis_afectada_por.append(item)
                    
                    # Si es derogación, marcar derogado_por
                    if 'DEROGA' in relacion_text.upper() and not derogado_por:
                        derogado_por = id_norma
                    
                    # Si es modificación, añadir a modificado_por
                    if 'MODIFICA' in relacion_text.upper():
                        modificado_por.append(id_norma)
        
        payload.update({
            "analisis_modificaciones": analisis_afectada_por,  # NUEVO: Array completo
            "analisis_afecta_a": analisis_afecta_a,  # NUEVO: Array completo
            "analisis_afectada_por": analisis_afectada_por,  # NUEVO: Alias para claridad
            "deroga_a": deroga_a,  # Lista simple de BOE IDs
            "derogado_por": derogado_por,  # BOE ID único o None
            "modificado_por": modificado_por,  # Lista de BOE IDs que modifican esta ley
        })
        
        # METADATA XML COMPLETO (1 campo JSONB) - NUEVO
        # Incluir TODO el JSON para que LLMs puedan acceder a cualquier campo
        payload["metadata_xml"] = {
            "metadatos": meta,
            "analisis": anal,
            "boe_id": boe_id,
            "fecha_ingesta": datetime.now().isoformat()
        }
        
    else:
        # Valores por defecto si no hay JSON
        payload.update({
            "organismo_emisor": "",
            "departamento_codigo": "",
            "departamento_nombre": "",
            "fecha_publicacion": "",
            "fecha_vigencia": "",
            "fecha_disposicion": "",
            "fecha_actualizacion": "",
            "fecha_derogacion": None,
            "vigente": True,
            "estatus_derogacion": "N",
            "estatus_anulacion": "N",
            "vigencia_agotada": "N",
            "estado_consolidacion": "",
            "consolidado": False,
            "rango": "",
            "rango_codigo": "",
            "numero_oficial": "",
            "url_boe": "",
            "url_eli": "",
            "url_pdf": "",
            "url_pdf_consolidado": "",
            "url_xml": "",
            "url_html_consolidada": "",
            "materias": [],
            "materias_completas": [],
            "analisis_modificaciones": [],
            "analisis_afecta_a": [],
            "analisis_afectada_por": [],
            "deroga_a": [],
            "derogado_por": None,
            "modificado_por": [],
            "metadata_xml": {},
        })
    
    return payload


async def create_collection_full_xml(client: QdrantClient, recreate: bool = False):
    """Crea colección con metadatos XML completos y búsqueda híbrida"""
    
    collections = [c.name for c in client.get_collections().collections]
    
    if COL_FULL_XML in collections:
        if recreate:
            print(f"🗑️ Borrando colección existente {COL_FULL_XML}...")
            client.delete_collection(COL_FULL_XML)
        else:
            print(f"⚠️ Colección {COL_FULL_XML} ya existe, saltando creación")
            return
    
    print(f"📦 Creando colección {COL_FULL_XML} con metadatos XML completos...")
    
    # Named vectors: dense + sparse (BM25)
    client.create_collection(
        collection_name=COL_FULL_XML,
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
    
    print(f"✅ Colección {COL_FULL_XML} creada con búsqueda híbrida (dense + sparse)")


async def ingest_all_laws(qdrant: QdrantClient, pool: asyncpg.Pool, analisis_por_ley: Dict):
    """Ingesta TODAS las leyes con metadatos XML completos"""
    
    print("\n" + "="*80)
    print("📥 INICIANDO INGESTA COMPLETA")
    print("="*80)
    
    # Obtener todas las leyes de PostgreSQL
    async with pool.acquire() as conn:
        laws = await conn.fetch("""
            SELECT 
                id,
                law_id as boe_id,
                law_name,
                title as article_title,
                content as text_snippet,
                'article_chunk' as layer
            FROM laws
            ORDER BY law_id, title
        """)
    
    print(f"📊 Total chunks en PostgreSQL: {len(laws):,}")
    
    # Agrupar por BOE ID
    laws_by_boe = {}
    for law in laws:
        boe_id = law['boe_id']
        if boe_id not in laws_by_boe:
            laws_by_boe[boe_id] = []
        laws_by_boe[boe_id].append(dict(law))
    
    print(f"📚 Total leyes únicas: {len(laws_by_boe)}")
    
    # Cargar modelos
    model = load_embedding_model()
    load_bm25_vocab()
    
    # Procesar cada ley
    total_points = 0
    batch_size = 100
    points_batch = []
    
    for i, (boe_id, chunks) in enumerate(laws_by_boe.items(), 1):
        print(f"\n[{i}/{len(laws_by_boe)}] Procesando {boe_id} ({len(chunks)} chunks)...")
        
        analisis_data = analisis_por_ley.get(boe_id)
        if not analisis_data:
            print(f"  ⚠️ No hay análisis JSON para {boe_id}, usando metadatos básicos")
        
        for chunk in chunks:
            # Construir payload COMPLETO
            payload = build_chunk_payload_FULL(chunk, analisis_data)
            
            # Generar embeddings
            text_for_embedding = f"{payload['law_name']} {payload['article_title']} {payload['text_snippet']}"
            dense_vector = model.encode(text_for_embedding, convert_to_tensor=False).tolist()
            sparse_vector = generate_sparse_vector(text_for_embedding)
            
            # Crear punto
            point = PointStruct(
                id=compute_hash(f"{boe_id}_{chunk['id']}"),  # ID único
                vector={
                    "dense": dense_vector,
                    "text": sparse_vector
                },
                payload=payload
            )
            
            points_batch.append(point)
            total_points += 1
            
            # Upsert en batches
            if len(points_batch) >= batch_size:
                qdrant.upsert(
                    collection_name=COL_FULL_XML,
                    points=points_batch
                )
                print(f"  ✅ Upsert {len(points_batch)} puntos (total: {total_points})")
                points_batch = []
    
    # Upsert batch final
    if points_batch:
        qdrant.upsert(
            collection_name=COL_FULL_XML,
            points=points_batch
        )
        print(f"  ✅ Upsert {len(points_batch)} puntos (total: {total_points})")
    
    print("\n" + "="*80)
    print(f"✅ INGESTA COMPLETA: {total_points:,} puntos en {COL_FULL_XML}")
    print("="*80)


async def ingest_test_law(qdrant: QdrantClient, pool: asyncpg.Pool, analisis_por_ley: Dict, test_boe_id: str = "BOE-A-2015-11724"):
    """Ingesta UNA ley de prueba (LGSS)"""
    
    print("\n" + "="*80)
    print(f"🧪 INGESTA DE PRUEBA: {test_boe_id}")
    print("="*80)
    
    # Obtener chunks de la ley de prueba
    async with pool.acquire() as conn:
        chunks = await conn.fetch("""
            SELECT 
                id,
                law_id as boe_id,
                law_name,
                title as article_title,
                content as text_snippet,
                'article_chunk' as layer
            FROM laws
            WHERE law_id = $1
            ORDER BY title
        """, test_boe_id)
    
    if not chunks:
        print(f"❌ No se encontraron chunks para {test_boe_id}")
        return
    
    print(f"📊 Total chunks: {len(chunks)}")
    
    # Cargar modelos
    model = load_embedding_model()
    load_bm25_vocab()
    
    # Obtener análisis JSON
    analisis_data = analisis_por_ley.get(test_boe_id)
    if not analisis_data:
        print(f"⚠️ No hay análisis JSON para {test_boe_id}")
    
    # Procesar chunks
    points = []
    for chunk in chunks:
        chunk_dict = dict(chunk)
        
        # Construir payload COMPLETO
        payload = build_chunk_payload_FULL(chunk_dict, analisis_data)
        
        # Generar embeddings
        text_for_embedding = f"{payload['law_name']} {payload['article_title']} {payload['text_snippet']}"
        dense_vector = model.encode(text_for_embedding, convert_to_tensor=False).tolist()
        sparse_vector = generate_sparse_vector(text_for_embedding)
        
        # Crear punto
        point = PointStruct(
            id=compute_hash(f"{test_boe_id}_{chunk['id']}"),
            vector={
                "dense": dense_vector,
                "text": sparse_vector
            },
            payload=payload
        )
        
        points.append(point)
    
    # Upsert
    qdrant.upsert(
        collection_name=COL_FULL_XML,
        points=points
    )
    
    print(f"✅ Ingesta completa: {len(points)} puntos")
    
    # Mostrar ejemplo de payload
    if points:
        ejemplo = points[0].payload
        print("\n📋 EJEMPLO DE PAYLOAD COMPLETO:")
        print(f"  BOE ID: {ejemplo.get('boe_id')}")
        print(f"  Artículo: {ejemplo.get('article_title')}")
        print(f"  Organismo: {ejemplo.get('organismo_emisor')}")
        print(f"  Vigente: {ejemplo.get('vigente')}")
        print(f"  Consolidado: {ejemplo.get('consolidado')}")
        print(f"  Materias: {len(ejemplo.get('materias', []))}")
        print(f"  Modificaciones: {len(ejemplo.get('analisis_modificaciones', []))}")
        print(f"  Afecta a: {len(ejemplo.get('analisis_afecta_a', []))}")
        print(f"  URLs: {len([k for k in ejemplo.keys() if k.startswith('url_')])}")
        print(f"  Total campos: {len(ejemplo)}")


async def main():
    parser = argparse.ArgumentParser(description="Ingesta Qdrant con metadatos XML completos")
    parser.add_argument("--test", action="store_true", help="Solo ingestar 1 ley de prueba")
    parser.add_argument("--recreate", action="store_true", help="Borrar y recrear colección")
    args = parser.parse_args()
    
    print("="*80)
    print("🚀 REINGEST QDRANT FULL XML")
    print("="*80)
    print(f"Colección: {COL_FULL_XML}")
    print(f"Modo: {'PRUEBA (1 ley)' if args.test else 'COMPLETO (todas las leyes)'}")
    print(f"Recrear: {'SÍ' if args.recreate else 'NO'}")
    print("="*80)
    
    # Conectar a Qdrant
    print(f"\n🔗 Conectando a Qdrant: {QDRANT_URL}")
    qdrant = QdrantClient(url=QDRANT_URL, timeout=120)
    print("✅ Conectado a Qdrant")
    
    # Conectar a PostgreSQL
    print(f"\n🐘 Conectando a PostgreSQL...")
    pool = await asyncpg.create_pool(POSTGRES_DSN, min_size=1, max_size=5)
    print("✅ Conectado a PostgreSQL")
    
    # Cargar análisis JSON
    print(f"\n📂 Cargando análisis JSON de {JSON_DIR}...")
    analisis_por_ley = {}
    json_files = list(JSON_DIR.glob("BOE-A-*.json"))
    print(f"📄 Encontrados {len(json_files)} archivos JSON")
    
    for json_file in json_files:
        boe_id = json_file.stem
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data.get('status', {}).get('code', {}).get('_text') == '200':
                analisis_por_ley[boe_id] = data.get('data', {})
    
    print(f"✅ Cargados {len(analisis_por_ley)} análisis JSON")
    
    # Crear colección
    await create_collection_full_xml(qdrant, recreate=args.recreate)
    
    # Ingestar
    if args.test:
        await ingest_test_law(qdrant, pool, analisis_por_ley)
    else:
        await ingest_all_laws(qdrant, pool, analisis_por_ley)
    
    # Cerrar conexiones
    await pool.close()
    
    print("\n" + "="*80)
    print("✅ PROCESO COMPLETADO")
    print("="*80)
    print(f"\nColección creada: {COL_FULL_XML}")
    print("Búsqueda híbrida: Dense (BGE-M3) + Sparse (BM25)")
    print("Metadatos: 50+ campos XML BOE completos")
    print("\nPróximo paso: Probar búsqueda híbrida con metadatos completos")


if __name__ == "__main__":
    asyncio.run(main())
