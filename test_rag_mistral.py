#!/usr/bin/env python3
"""
Script simple para probar el RAG de Qdrant con Mistral
"""

import requests
import json
import os
from typing import List, Dict, Any

def test_qdrant_connection():
    """Prueba la conexión con Qdrant local"""
    try:
        response = requests.get("http://localhost:6333/collections", timeout=5)
        if response.status_code == 200:
            collections = response.json()
            print("✅ Qdrant conectado correctamente")
            print(f"📊 Colecciones disponibles: {len(collections.get('result', {}).get('collections', []))}")
            
            for collection in collections.get('result', {}).get('collections', []):
                print(f"  - {collection['name']}")
            
            return collections
        else:
            print(f"❌ Error conectando a Qdrant: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error conectando a Qdrant: {e}")
        return None

def get_collection_info(collection_name: str):
    """Obtiene información detallada de una colección"""
    try:
        response = requests.get(f"http://localhost:6333/collections/{collection_name}", timeout=5)
        if response.status_code == 200:
            info = response.json()
            result = info.get('result', {})
            
            print(f"\n📋 Información de la colección '{collection_name}':")
            print(f"  - Vectores: {result.get('points_count', 0)}")
            print(f"  - Estado: {result.get('status', 'unknown')}")
            print(f"  - Segmentos: {result.get('segments_count', 0)}")
            
            # Configuración de vectores
            config = result.get('config', {})
            params = config.get('params', {})
            vectors_config = params.get('vectors', {})
            
            if isinstance(vectors_config, dict):
                print(f"  - Dimensiones: {vectors_config.get('size', 'unknown')}")
                print(f"  - Distancia: {vectors_config.get('distance', 'unknown')}")
            
            return result
        else:
            print(f"❌ Error obteniendo info de colección: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error obteniendo info de colección: {e}")
        return None

def sample_collection_content(collection_name: str, limit: int = 3):
    """Obtiene una muestra del contenido de la colección"""
    try:
        payload = {
            "limit": limit,
            "with_payload": True,
            "with_vector": False
        }
        
        response = requests.post(
            f"http://localhost:6333/collections/{collection_name}/points/scroll",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            points = data.get('result', {}).get('points', [])
            
            print(f"\n📄 Muestra de contenido de '{collection_name}' ({len(points)} elementos):")
            
            for i, point in enumerate(points, 1):
                payload_data = point.get('payload', {})
                print(f"\n  {i}. ID: {point.get('id')}")
                
                # Mostrar campos de payload más relevantes
                for key, value in payload_data.items():
                    if isinstance(value, str) and len(value) > 100:
                        print(f"     {key}: {value[:100]}...")
                    else:
                        print(f"     {key}: {value}")
            
            return points
        else:
            print(f"❌ Error obteniendo muestra: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error obteniendo muestra: {e}")
        return None

def main():
    """Función principal"""
    print("🔍 Probando RAG de Opositaia con Qdrant local\n")
    
    # 1. Probar conexión
    collections = test_qdrant_connection()
    if not collections:
        return
    
    # 2. Analizar cada colección
    collection_names = [c['name'] for c in collections.get('result', {}).get('collections', [])]
    
    for collection_name in collection_names:
        print(f"\n{'='*50}")
        get_collection_info(collection_name)
        sample_collection_content(collection_name, limit=2)
    
    print(f"\n{'='*50}")
    print("✅ Análisis completado")

if __name__ == "__main__":
    main()