#!/usr/bin/env python3
"""
CHECKLIST DE VERIFICACIÓN PRE-EJECUCIÓN
========================================
SIEMPRE ejecutar ANTES de cualquier script
"""

import requests
import psycopg2
from qdrant_client import QdrantClient
import sys

def verificar_backend():
    """1. Verificar que backend FastAPI está funcionando"""
    print("1️⃣ Verificando Backend FastAPI...")
    try:
        response = requests.get('http://127.0.0.1:8000/health', timeout=120)
        if response.status_code == 200:
            print("   ✅ Backend OK")
            return True
        else:
            print(f"   ❌ Backend responde con status {response.status_code}")
            print("\n   📋 INSTRUCCIONES PARA ARRANCAR BACKEND:")
            print("   1. cd /home/spas/OPOS_GEMINI_1")
            print("   2. docker-compose up -d backend")
            print("   3. Esperar 20 segundos")
            print("   4. Verificar: curl http://127.0.0.1:8000/health")
            return False
    except Exception as e:
        print(f"   ❌ Backend NO responde: {e}")
        print("\n   📋 INSTRUCCIONES PARA ARRANCAR BACKEND:")
        print("   1. cd /home/spas/OPOS_GEMINI_1")
        print("   2. docker-compose ps  # Ver estado de contenedores")
        print("   3. docker-compose up -d backend  # Arrancar backend")
        print("   4. docker-compose logs -f backend  # Ver logs")
        print("   5. Esperar 20 segundos")
        print("   6. Verificar: curl http://127.0.0.1:8000/health")
        return False

def verificar_endpoint_rag():
    """2. Verificar que endpoint RAG devuelve metadata con BOE ID"""
    print("\n2️⃣ Verificando Endpoint RAG...")
    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/rag/search',
            json={'query': 'jubilación', 'top_k': 1, 'min_score': 0.3},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            docs = data.get('documents', [])
            
            if docs and docs[0].get('metadata', {}).get('boe_id'):
                print(f"   ✅ RAG devuelve BOE ID: {docs[0]['metadata']['boe_id']}")
                return True
            else:
                print("   ❌ RAG NO devuelve BOE ID en metadata")
                return False
        else:
            print(f"   ❌ RAG endpoint error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error consultando RAG: {e}")
        return False

def verificar_postgresql():
    """3. Verificar PostgreSQL y tabla leyes_catalogo"""
    print("\n3️⃣ Verificando PostgreSQL...")
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            dbname='opositaia',
            user='postgres',
            password='postgres'
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM leyes_catalogo;")
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print(f"   ✅ PostgreSQL OK ({count} leyes en catálogo)")
        return True
        
    except Exception as e:
        print(f"   ❌ PostgreSQL error: {e}")
        return False

def verificar_qdrant():
    """4. Verificar Qdrant"""
    print("\n4️⃣ Verificando Qdrant...")
    try:
        client = QdrantClient(url='http://localhost:6333')
        collection_info = client.get_collection('opositaia_knowledge')
        
        print(f"   ✅ Qdrant OK ({collection_info.points_count:,} puntos)")
        return True
        
    except Exception as e:
        print(f"   ❌ Qdrant error: {e}")
        return False

def verificar_archivos():
    """5. Verificar que archivos de dataset existen y tienen permisos"""
    print("\n5️⃣ Verificando Archivos...")
    from pathlib import Path
    
    dataset = Path("golden_dataset/consolidated/golden_dataset_cleaned.jsonl")
    output = Path("golden_dataset/consolidated/golden_dataset_enriched.jsonl")
    
    if not dataset.exists():
        print(f"   ❌ Dataset no existe: {dataset}")
        return False
    
    if not dataset.is_file():
        print(f"   ❌ Dataset no es un archivo: {dataset}")
        return False
    
    # Verificar que output directory existe
    output.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"   ✅ Dataset OK ({dataset.stat().st_size / 1024 / 1024:.2f} MB)")
    return True

def main():
    print("="*70)
    print("🔍 CHECKLIST DE VERIFICACIÓN PRE-EJECUCIÓN")
    print("="*70)
    
    checks = [
        ("Backend FastAPI", verificar_backend),
        ("Endpoint RAG", verificar_endpoint_rag),
        ("PostgreSQL", verificar_postgresql),
        ("Qdrant", verificar_qdrant),
        ("Archivos", verificar_archivos)
    ]
    
    resultados = []
    for nombre, check_func in checks:
        resultado = check_func()
        resultados.append((nombre, resultado))
    
    print("\n" + "="*70)
    print("📊 RESUMEN")
    print("="*70)
    
    all_ok = True
    for nombre, resultado in resultados:
        status = "✅" if resultado else "❌"
        print(f"{status} {nombre}")
        if not resultado:
            all_ok = False
    
    print("\n" + "="*70)
    if all_ok:
        print("✅ TODAS LAS VERIFICACIONES PASARON")
        print("="*70)
        return 0
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("="*70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
