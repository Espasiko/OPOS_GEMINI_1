#!/usr/bin/env python3
"""
COMPARACIÓN HÍBRIDA EXCELENTE - 2026 Best Practices
Siguiendo recomendaciones oficiales Qdrant y literatura 2026
"""

import os, sys, json, pickle
from pathlib import Path
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from collections import Counter
from tabulate import tabulate
import re

sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env.backend")

print("=" * 90)
print("COMPARACIÓN HÍBRIDA CLOUD vs LOCAL - 2026 BEST PRACTICES")
print("=" * 90)

# === QUERIES LEGALES EXPANDIDAS (30 queries) ===
QUERIES = [
    # LGSS y prestaciones
    "artículo 217 LGSS prestación por desempleo",
    "TRLGSS cotización empresarial obligaciones",
    "artículo 113 LGSS incapacidad temporal",
    "LGSS prestación maternidad requisitos",
    "incapacidad permanente total grado",
    
    # Derecho laboral
    "despido objetivo causas económicas",
    "contrato temporal causas justificadas",
    "convenio colectivo aplicación territorial",
    "permiso maternidad duración semanas",
    "horas extraordinarias límites legales",
    "período de prueba duración máxima",
    "salario mínimo interprofesional SMI",
    
    # Derecho administrativo
    "RD-ley 463/2020 estado de alarma competencias",
    "recurso contencioso administrativo plazos",
    "silencio administrativo positivo negativo",
    "responsabilidad patrimonial administración",
    
    # Derecho constitucional
    "tribunal supremo jurisprudencia unificación doctrina",
    "artículo 14 constitución igualdad ante ley",
    "recurso de amparo tribunal constitucional",
    "derechos fundamentales suspensión individual",
    
    # Derecho civil
    "usufructo derechos obligaciones usufructuario",
    "prescripción adquisitiva requisitos",
    "comunidad de bienes administración",
    
    # Derecho procesal
    "recurso de casación civil requisitos",
    "medidas cautelares proceso civil",
    "costas procesales imposición criterios",
    
    # Específico seguridad social
    "pensión jubilación contributiva requisitos edad",
    "prestación por nacimiento hijo",
    "cotización autónomos base mínima",
    "subsidio desempleo mayores 52 años"
]

# === SETUP ===
print(f"\n1. Setup ({len(QUERIES)} queries de test)...")

# Cargar BM25 vocab
with open('backend/data/bm25_vocab.pkl', 'rb') as f:
    bm25_data = pickle.load(f)
vocab, idf_dict, avgdl = bm25_data['vocab'], bm25_data['idf'], bm25_data['avgdl']
k1, b = bm25_data['k1'], bm25_data['b']

print(f"   BM25: {len(vocab):,} términos, avgdl={avgdl:.1f}")

# Tokenizer
def tokenize_legal(text):
    text = text.lower()
    tokens = re.findall(r'[a-záéíóúñ0-9]+', text)
    stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'se', 'por', 'para', 'con', 'un', 'una', 'al', 'lo', 'su', 'sus'}
    return [t for t in tokens if len(t) > 2 and t not in stopwords]

# Sparse generator
def gen_sparse(text):
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
    return models.SparseVector(indices=indices, values=values)

# Clientes
cloud = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"), timeout=60.0)
local = QdrantClient(url="http://localhost:6333", timeout=60.0)

# Embedder
embedder = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
print(f"   ✅ Embedder cargado")

# Verificar colecciones
cloud_info = cloud.get_collection("opositaia_knowledge")
local_info = local.get_collection("opositaia_knowledge_hybrid")
print(f"   Cloud: {cloud_info.points_count:,} points")
print(f"   Local: {local_info.points_count:,} points")

# === COMPARACIÓN ===
print(f"\n2. Ejecutando {len(QUERIES)} queries...")
print("=" * 90)

PREFETCH_LIMIT = 100  # 2026 best practice: high prefetch
FINAL_LIMIT = 5

results = []

for i, query in enumerate(QUERIES, 1):
    print(f"\n[{i}/{len(QUERIES)}] {query[:70]}...")
    
    # Vectores
    dense_vec = embedder.encode(query).tolist()
    sparse_vec = gen_sparse(query)
    
    print(f"   Sparse: {len(sparse_vec.indices)} términos, score total={sum(sparse_vec.values):.2f}")
    
    # CLOUD: dense only
    cloud_results = cloud.search(
        collection_name="opositaia_knowledge",
        query_vector=dense_vec,
        limit=FINAL_LIMIT,
        with_payload=True
    )
    
    # LOCAL: HÍBRIDO con RRF (siguiendo ejemplo oficial Qdrant)
    local_results = local.query_points(
        collection_name="opositaia_knowledge_hybrid",
        prefetch=[
            models.Prefetch(
                query=sparse_vec,
                using="text",  # sparse vector name
                limit=PREFETCH_LIMIT  # HIGH limit per best practices
            ),
            models.Prefetch(
                query=dense_vec,
                using="dense",
                limit=PREFETCH_LIMIT
            )
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),  # RRF fusion
        limit=FINAL_LIMIT,
        with_payload=True
    )
    
    # Comparar top-1
    cloud_top = cloud_results[0] if cloud_results else None
    local_top = local_results.points[0] if local_results.points else None
    
    cloud_score = cloud_top.score if cloud_top else 0
    local_score = local_top.score if local_top else 0
    
    cloud_law = cloud_top.payload.get('law_name', 'N/A')[:45] if cloud_top else 'N/A'
    local_law = local_top.payload.get('law_name', 'N/A')[:45] if local_top else 'N/A'
    
    same_top = (cloud_top.id == local_top.id) if (cloud_top and local_top) else False
    
    print(f"   Cloud: score={cloud_score:.4f} - {cloud_law}")
    print(f"   Local: score={local_score:.4f} - {local_law}")
    print(f"   Match: {'✅ SÍ' if same_top else '❌ NO'}")
    
    results.append({
        'query': query,
        'cloud_score': cloud_score,
        'local_score': local_score,
        'cloud_law': cloud_law,
        'local_law': local_law,
        'same_top': same_top,
        'sparse_terms': len(sparse_vec.indices),
        'sparse_score': sum(sparse_vec.values)
    })

# === ANÁLISIS ===
print("\n" + "=" * 90)
print("ANÁLISIS DE RESULTADOS")
print("=" * 90)

same_count = sum(1 for r in results if r['same_top'])
avg_cloud = sum(r['cloud_score'] for r in results) / len(results)
avg_local = sum(r['local_score'] for r in results) / len(results)
avg_sparse_terms = sum(r['sparse_terms'] for r in results) / len(results)

print(f"\n📊 ESTADÍSTICAS GENERALES:")
print(f"   Total queries: {len(results)}")
print(f"   Coincidencia top-1: {same_count}/{len(results)} ({same_count/len(results)*100:.1f}%)")
print(f"   Score promedio Cloud: {avg_cloud:.4f}")
print(f"   Score promedio Local (híbrido): {avg_local:.4f}")
print(f"   Términos sparse promedio: {avg_sparse_terms:.1f}")

# Distribución de scores
cloud_scores = [r['cloud_score'] for r in results]
local_scores = [r['local_score'] for r in results]

print(f"\n📈 DISTRIBUCIÓN SCORES:")
print(f"   Cloud - min:{min(cloud_scores):.4f} max:{max(cloud_scores):.4f} std:{(sum((x-avg_cloud)**2 for x in cloud_scores)/len(cloud_scores))**0.5:.4f}")
print(f"   Local - min:{min(local_scores):.4f} max:{max(local_scores):.4f} std:{(sum((x-avg_local)**2 for x in local_scores)/len(local_scores))**0.5:.4f}")

# Top 10 para tabla
print(f"\n📋 SAMPLE RESULTS (primeras 10):")
table = []
for r in results[:10]:
    table.append([
        r['query'][:40] + "..." if len(r['query']) > 40 else r['query'],
        f"{r['cloud_score']:.4f}",
        f"{r['local_score']:.4f}",
        r['sparse_terms'],
        '✅' if r['same_top'] else '❌'
    ])

print(tabulate(table, headers=['Query', 'Cloud', 'Local', 'Sparse', 'Match'], tablefmt='grid'))

# Guardar
output = {
    'config': {
        'prefetch_limit': PREFETCH_LIMIT,
        'final_limit': FINAL_LIMIT,
        'vocab_size': len(vocab),
        'total_queries': len(QUERIES)
    },
    'stats': {
        'same_top1': same_count,
        'match_rate': same_count / len(results),
        'avg_score_cloud': avg_cloud,
        'avg_score_local': avg_local,
        'avg_sparse_terms': avg_sparse_terms
    },
    'results': results
}

with open('comparacion_hibrida_EXCELENTE_2026.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 90)
print("✅ COMPLETADO - Resultados guardados: comparacion_hibrida_EXCELENTE_2026.json")
print("=" * 90)
