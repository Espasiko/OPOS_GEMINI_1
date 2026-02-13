#!/usr/bin/env python3
"""
PRUEBA OPCIÓN 3 HÍBRIDA: Qdrant + PostgreSQL + Salamandra R1
=============================================================

Arquitectura:
1. Búsqueda RÁPIDA en Qdrant (hybrid search)
2. Enriquecimiento con PostgreSQL leyes_catalogo (50+ metadatos)
3. Razonamiento con Salamandra R1 local (Ollama)

Caso de prueba: María, 61 años, jubilación anticipada
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
import psycopg2
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import requests

# Cargar variables de entorno
load_dotenv("/home/spas/OPOS_GEMINI_1/backend/.env.backend")

# Configuración
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION = "opositaia_knowledge_hybrid"
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
OLLAMA_URL = "http://localhost:11434"
SALAMANDRA_MODEL = "salamandra-r1"

# Cargar modelo de embeddings
print("🤖 Cargando modelo de embeddings...")
model = SentenceTransformer(EMBEDDING_MODEL)
print(f"✅ Modelo cargado: {EMBEDDING_MODEL}")

# Conectar a Qdrant
print(f"\n🔗 Conectando a Qdrant: {QDRANT_URL}")
qdrant = QdrantClient(url=QDRANT_URL, timeout=120)  # 120s timeout
print("✅ Conectado a Qdrant")

# Conectar a PostgreSQL
print("\n🐘 Conectando a PostgreSQL...")
conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD')
)
cur = conn.cursor()
print("✅ Conectado a PostgreSQL")


def search_qdrant_hybrid(query: str, limit: int = 10) -> List[Dict]:
    """Búsqueda híbrida en Qdrant (dense + sparse)"""
    print(f"\n🔍 Búsqueda Qdrant: '{query}' (limit={limit})")
    
    # Generar embedding
    embedding = model.encode(query, convert_to_tensor=False).tolist()
    
    # Búsqueda híbrida (solo dense por ahora, sparse requiere más config)
    results = qdrant.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=("dense", embedding),
        limit=limit,
        with_payload=True
    )
    
    print(f"✅ Encontrados {len(results)} resultados")
    return results


def enrich_with_postgres(boe_id: str) -> Optional[Dict]:
    """Enriquece con metadatos completos de PostgreSQL"""
    print(f"   📊 Enriqueciendo {boe_id} con PostgreSQL...")
    
    cur.execute("""
        SELECT 
            boe_id,
            titulo,
            organismo_emisor,
            departamento_nombre,
            fecha_publicacion,
            fecha_entrada_vigor,
            fecha_derogacion,
            vigente,
            consolidado,
            version_consolidada,
            url_boe,
            url_eli,
            url_pdf,
            url_pdf_consolidado,
            analisis_modificaciones,
            analisis_afecta_a,
            analisis_afectada_por,
            num_articulos,
            indice_estructurado,
            leyes_relacionadas,
            materias,
            palabras_clave,
            tags,
            notas,
            observaciones
        FROM leyes_catalogo
        WHERE boe_id = %s
    """, (boe_id,))
    
    row = cur.fetchone()
    if not row:
        print(f"   ⚠️ No encontrado en leyes_catalogo")
        return None
    
    # Convertir a dict
    metadata = {
        'boe_id': row[0],
        'titulo': row[1],
        'organismo_emisor': row[2],
        'departamento_nombre': row[3],
        'fecha_publicacion': str(row[4]) if row[4] else None,
        'fecha_entrada_vigor': str(row[5]) if row[5] else None,
        'fecha_derogacion': str(row[6]) if row[6] else None,
        'vigente': row[7],
        'consolidado': row[8],
        'version_consolidada': row[9],
        'url_boe': row[10],
        'url_eli': row[11],
        'url_pdf': row[12],
        'url_pdf_consolidado': row[13],
        'analisis_modificaciones': row[14],
        'analisis_afecta_a': row[15],
        'analisis_afectada_por': row[16],
        'num_articulos': row[17],
        'indice_estructurado': row[18],
        'leyes_relacionadas': row[19],
        'materias': row[20],
        'palabras_clave': row[21],
        'tags': row[22],
        'notas': row[23],
        'observaciones': row[24],
    }
    
    print(f"   ✅ Enriquecido con {len([k for k, v in metadata.items() if v])} campos")
    return metadata


def ask_salamandra(prompt: str, context: List[Dict]) -> Dict:
    """Pregunta a Salamandra R1 con contexto enriquecido"""
    print(f"\n🦎 Consultando Salamandra R1...")
    
    # Construir prompt con contexto
    context_str = "\n\n".join([
        f"### FUENTE {i+1}: {c['boe_id']} - {c.get('titulo', 'N/A')}\n"
        f"**Artículo:** {c.get('article_title', 'N/A')}\n"
        f"**Texto:** {c.get('text_snippet', 'N/A')[:500]}...\n"
        f"**Organismo:** {c.get('organismo_emisor', 'N/A')}\n"
        f"**Vigente:** {c.get('vigente', 'N/A')}\n"
        f"**Modificaciones:** {len(c.get('analisis_modificaciones') or []) if isinstance(c.get('analisis_modificaciones'), list) else 0} encontradas\n"
        f"**Leyes relacionadas:** {', '.join((c.get('leyes_relacionadas') or [])[:3]) if isinstance(c.get('leyes_relacionadas'), list) else 'N/A'}\n"
        f"**URL BOE:** {c.get('url_boe', 'N/A')}"
        for i, c in enumerate(context[:5])  # Solo top 5
    ])
    
    full_prompt = f"""Eres un experto en Seguridad Social española. Responde usando SOLO la información proporcionada.

CONTEXTO LEGAL (Top 5 fuentes más relevantes):
{context_str}

PREGUNTA:
{prompt}

INSTRUCCIONES:
1. Analiza TODAS las fuentes proporcionadas
2. Cita SIEMPRE el BOE-ID y artículo específico
3. Menciona si hay modificaciones o leyes relacionadas
4. Indica si la norma está vigente
5. Proporciona la URL del BOE para verificación

RESPUESTA:"""
    
    # Llamar a Ollama
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": SALAMANDRA_MODEL,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_ctx": 8192,
                "num_predict": 2048
            }
        },
        timeout=120
    )
    
    if response.status_code != 200:
        print(f"❌ Error Ollama: {response.status_code}")
        return {"error": response.text}
    
    result = response.json()
    print(f"✅ Respuesta recibida ({len(result.get('response', ''))} chars)")
    
    return {
        "response": result.get("response", ""),
        "model": result.get("model", ""),
        "total_duration": result.get("total_duration", 0) / 1e9,  # ns -> s
        "load_duration": result.get("load_duration", 0) / 1e9,
        "prompt_eval_count": result.get("prompt_eval_count", 0),
        "eval_count": result.get("eval_count", 0),
    }


def main():
    print("=" * 80)
    print("🧪 PRUEBA OPCIÓN 3 HÍBRIDA: Qdrant + PostgreSQL + Salamandra R1")
    print("=" * 80)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Caso de prueba
    caso = {
        "nombre": "María",
        "edad": 61,
        "años_cotizados": 38,
        "discapacidad": 35,
        "mutualista_años": 10,
        "base_reguladora": 2800
    }
    
    print(f"\n📋 CASO: {caso['nombre']}, {caso['edad']} años, {caso['años_cotizados']} años cotizados")
    
    # Pregunta
    pregunta = f"""
María tiene {caso['edad']} años, ha cotizado {caso['años_cotizados']} años, 
tiene una discapacidad del {caso['discapacidad']}%, fue mutualista durante {caso['mutualista_años']} años,
y su base reguladora es de {caso['base_reguladora']}€.

¿Puede María jubilarse anticipadamente? ¿Cuál sería su pensión estimada?
Explica los requisitos legales, coeficientes reductores aplicables, y cita las fuentes legales exactas.
"""
    
    # PASO 1: Búsqueda en Qdrant
    print("\n" + "=" * 80)
    print("PASO 1: BÚSQUEDA EN QDRANT")
    print("=" * 80)
    
    queries = [
        "jubilación anticipada edad mínima discapacidad",
        "coeficientes reductores jubilación anticipada",
        "mutualista cómputo años cotizados",
        "base reguladora pensión jubilación",
    ]
    
    all_results = []
    seen_boe_ids = set()
    
    for query in queries:
        results = search_qdrant_hybrid(query, limit=5)
        for r in results:
            boe_id = r.payload.get('boe_id')
            if boe_id and boe_id not in seen_boe_ids:
                all_results.append(r)
                seen_boe_ids.add(boe_id)
    
    print(f"\n✅ Total resultados únicos: {len(all_results)}")
    
    # PASO 2: Enriquecimiento con PostgreSQL
    print("\n" + "=" * 80)
    print("PASO 2: ENRIQUECIMIENTO CON POSTGRESQL")
    print("=" * 80)
    
    enriched_results = []
    for r in all_results[:10]:  # Top 10
        payload = dict(r.payload)
        boe_id = payload.get('boe_id')
        
        if boe_id:
            pg_metadata = enrich_with_postgres(boe_id)
            if pg_metadata:
                # Merge Qdrant + PostgreSQL
                payload.update(pg_metadata)
        
        enriched_results.append(payload)
    
    print(f"\n✅ Enriquecidos {len(enriched_results)} resultados")
    
    # Mostrar ejemplo de enriquecimiento
    if enriched_results:
        ejemplo = enriched_results[0]
        print(f"\n📊 EJEMPLO ENRIQUECIDO:")
        print(f"   BOE ID: {ejemplo.get('boe_id')}")
        print(f"   Título: {ejemplo.get('titulo', 'N/A')[:80]}...")
        print(f"   Artículo: {ejemplo.get('article_title', 'N/A')[:60]}...")
        print(f"   Organismo: {ejemplo.get('organismo_emisor', 'N/A')}")
        print(f"   Vigente: {ejemplo.get('vigente', 'N/A')}")
        mods = ejemplo.get('analisis_modificaciones') or []
        print(f"   Modificaciones: {len(mods) if isinstance(mods, list) else 0}")
        rels = ejemplo.get('leyes_relacionadas') or []
        print(f"   Leyes relacionadas: {len(rels) if isinstance(rels, list) else 0}")
        print(f"   URL BOE: {ejemplo.get('url_boe', 'N/A')}")
    
    # PASO 3: Razonamiento con Salamandra R1
    print("\n" + "=" * 80)
    print("PASO 3: RAZONAMIENTO CON SALAMANDRA R1")
    print("=" * 80)
    
    salamandra_response = ask_salamandra(pregunta, enriched_results)
    
    # Mostrar respuesta
    print("\n" + "=" * 80)
    print("📝 RESPUESTA DE SALAMANDRA R1:")
    print("=" * 80)
    print(salamandra_response.get('response', 'ERROR'))
    
    # Estadísticas
    print("\n" + "=" * 80)
    print("📊 ESTADÍSTICAS:")
    print("=" * 80)
    print(f"Modelo: {salamandra_response.get('model', 'N/A')}")
    print(f"Tiempo total: {salamandra_response.get('total_duration', 0):.2f}s")
    print(f"Tiempo carga: {salamandra_response.get('load_duration', 0):.2f}s")
    print(f"Tokens prompt: {salamandra_response.get('prompt_eval_count', 0)}")
    print(f"Tokens generados: {salamandra_response.get('eval_count', 0)}")
    
    # Guardar resultados
    output = {
        "caso": caso,
        "pregunta": pregunta,
        "fecha_ejecucion": datetime.now().isoformat(),
        "qdrant": {
            "url": QDRANT_URL,
            "collection": QDRANT_COLLECTION,
            "queries": queries,
            "resultados_totales": len(all_results)
        },
        "postgresql": {
            "enriquecidos": len(enriched_results),
            "ejemplo": enriched_results[0] if enriched_results else None
        },
        "salamandra": salamandra_response,
    }
    
    output_file = "/home/spas/OPOS_GEMINI_1/prueba_hibrida_salamandra_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    
    # Cerrar conexiones
    cur.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 80)


if __name__ == "__main__":
    main()
