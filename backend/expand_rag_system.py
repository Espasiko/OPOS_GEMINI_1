#!/usr/bin/env python3
"""
Análisis detallado del contenido en Qdrant y expansión con más leyes
"""

import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import requests
import xml.etree.ElementTree as ET

def analyze_current_content():
    """Analizar el contenido actual en Qdrant"""
    print("🔍 ANALIZANDO CONTENIDO ACTUAL EN QDRANT")
    print("="*60)
    
    client = QdrantClient(host="localhost", port=6333)
    collection_name = "opositaia_knowledge"
    
    # Obtener información de la colección
    collection_info = client.get_collection(collection_name)
    print(f"✅ Total vectores: {collection_info.points_count}")
    
    # Obtener todos los puntos
    points = client.scroll(
        collection_name=collection_name,
        limit=100,  # Obtener todos
        with_payload=True,
        with_vectors=True
    )[0]
    
    print(f"\n📊 ANÁLISIS DETALLADO DE {len(points)} VECTORES:")
    print("-" * 60)
    
    total_text_size = 0
    laws_summary = {}
    
    for i, point in enumerate(points):
        payload = point.payload
        vector_size = len(point.vector) if point.vector else 0
        text = payload.get('text', '')
        text_size = len(text)
        total_text_size += text_size
        law_name = payload.get('law_name', payload.get('source', 'Desconocido'))
        
        if law_name not in laws_summary:
            laws_summary[law_name] = {
                'vectors': 0,
                'total_text': 0,
                'avg_text_size': 0
            }
        
        laws_summary[law_name]['vectors'] += 1
        laws_summary[law_name]['total_text'] += text_size
        
        print(f"[{i+1:2d}] Vector: {vector_size}D | Text: {text_size:,}chars | Law: {law_name[:50]}")
    
    # Resumen por ley
    print(f"\n📋 RESUMEN POR LEY:")
    print("-" * 60)
    for law, stats in laws_summary.items():
        stats['avg_text_size'] = stats['total_text'] // stats['vectors'] if stats['vectors'] > 0 else 0
        print(f"📄 {law[:40]:40} | Vectors: {stats['vectors']:2d} | Text: {stats['total_text']:,}chars | Avg: {stats['avg_text_size']:,}")
    
    print(f"\n🔢 ESTADÍSTICAS GLOBALES:")
    print(f"   Total texto indexado: {total_text_size:,} caracteres")
    print(f"   Promedio por vector: {total_text_size // len(points) if points else 0:,} caracteres")
    print(f"   Número de leyes: {len(laws_summary)}")
    
    return laws_summary

def get_additional_laws():
    """Obtener lista de leyes adicionales importantes para oposiciones"""
    additional_laws = [
        # Leyes fundamentales adicionales
        ("LEY_FUNCIONPUBLICA", "BOE-A-1964-4796"),  # Ley de Funcionarios Civiles del Estado
        ("RD_FUNCIONARIOS", "BOE-A-2007-8152"),     # RD 364/2007 Funcionarios
        ("LEY_CONTRATOS", "BOE-A-2017-12902"),      # Ley 9/2017 Contratos Sector Público
        ("LEY_TRANSPARENCIA", "BOE-A-2013-12887"),  # Ley 19/2013 Transparencia
        ("LEY_IGUALDAD", "BOE-A-2007-6115"),        # Ley Orgánica 3/2007 Igualdad
        ("LEY_VIOLENCIA_GENERO", "BOE-A-2004-21760"), # Ley Orgánica 1/2004 Violencia de Género
        ("LEY_PREVENCION_RIESGOS", "BOE-A-1995-24292"), # Ley 31/1995 Prevención de Riesgos Laborales
        ("LEY_HACIENDAS_LOCALES", "BOE-A-2004-4214"),   # Ley 2/2004 Haciendas Locales
        ("LEY_BASES_REGIMEN_LOCAL", "BOE-A-1985-5392"), # Ley 7/1985 Bases Régimen Local
        ("LEY_GOBIERNO_LOCAL", "BOE-A-2003-8931"),      # Ley 57/2003 Gobierno Local
        ("CODIGO_PENAL", "BOE-A-1995-25444"),           # Código Penal
        ("LEY_ENJUICIAMIENTO_CIVIL", "BOE-A-2000-323"), # LEC 1/2000
        ("LEY_ENJUICIAMIENTO_CRIMINAL", "BOE-A-1882-6036"), # LECrim
        ("LEY_SOCIEDADES_CAPITAL", "BOE-A-2010-10544"), # Ley Sociedades de Capital
        ("LEY_SEGURIDAD_CIUDADANA", "BOE-A-2015-3442"), # Ley Orgánica 4/2015 Seguridad Ciudadana
    ]
    
    return additional_laws

def ingest_additional_law(law_id, boe_id, model, client):
    """Ingestar una ley adicional"""
    print(f"\n🔄 Procesando {law_id} ({boe_id})...")
    
    try:
        # Intentar obtener metadatos
        metadata_url = f"https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{boe_id}/metadatos"
        response = requests.get(metadata_url, timeout=10)
        
        if response.status_code == 404:
            print(f"   ⚠️ {law_id}: No disponible en API consolidada (404)")
            return False
            
        if response.status_code != 200:
            print(f"   ❌ {law_id}: Error {response.status_code}")
            return False
            
        # Obtener texto consolidado
        text_url = f"https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{boe_id}/texto"
        text_response = requests.get(text_url, timeout=15)
        
        if text_response.status_code != 200:
            print(f"   ❌ {law_id}: Error obteniendo texto {text_response.status_code}")
            return False
            
        # Procesar texto
        law_content = text_response.text
        if len(law_content) < 100:  # Muy corto
            print(f"   ⚠️ {law_id}: Contenido muy corto ({len(law_content)} chars)")
            return False
            
        # Generar embedding
        print(f"   🧠 Generando embedding para {law_id}...")
        embedding = model.encode(law_content[:8000]).tolist()  # Limitar a 8k chars
        
        # Crear punto en Qdrant
        point = models.PointStruct(
            id=f"{boe_id}_{law_id}",
            vector=embedding,
            payload={
                "text": law_content[:8000],
                "source": boe_id,
                "law_name": law_id,
                "law_id": boe_id,
                "content_size": len(law_content),
                "indexed_at": "2025-12-08"
            }
        )
        
        # Insertar en Qdrant
        client.upsert(
            collection_name="opositaia_knowledge",
            points=[point],
            wait=True
        )
        
        print(f"   ✅ {law_id}: Indexada ({len(law_content):,} chars, embedding: {len(embedding)}D)")
        return True
        
    except Exception as e:
        print(f"   ❌ {law_id}: Error - {str(e)[:100]}")
        return False

def main():
    # 1. Analizar contenido actual
    current_laws = analyze_current_content()
    
    print("\n" + "="*80)
    print("🚀 EXPANDIENDO SISTEMA CON LEYES ADICIONALES")
    print("="*80)
    
    # 2. Preparar modelo y cliente
    print("🔄 Inicializando modelo y cliente...")
    model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
    client = QdrantClient(host="localhost", port=6333)
    
    # 3. Obtener leyes adicionales
    additional_laws = get_additional_laws()
    
    print(f"\n📋 PROCESANDO {len(additional_laws)} LEYES ADICIONALES:")
    print("-" * 60)
    
    successful = 0
    failed = 0
    
    for law_id, boe_id in additional_laws:
        success = ingest_additional_law(law_id, boe_id, model, client)
        if success:
            successful += 1
        else:
            failed += 1
    
    # 4. Verificar resultado final
    print(f"\n📊 RESULTADOS DE LA EXPANSIÓN:")
    print("-" * 60)
    
    final_info = client.get_collection("opositaia_knowledge")
    print(f"✅ Vectores totales: {final_info.points_count}")
    print(f"✅ Leyes añadidas exitosamente: {successful}")
    print(f"⚠️ Leyes que fallaron: {failed}")
    print(f"📈 Incremento: +{final_info.points_count - sum(stats['vectors'] for stats in current_laws.values())} vectores")
    
    print(f"\n🎯 SISTEMA RAG EXPANDIDO COMPLETADO")
    print(f"   Total leyes en sistema: {len(current_laws) + successful}")
    print(f"   Cobertura legal ampliada para oposiciones españolas")

if __name__ == "__main__":
    main()