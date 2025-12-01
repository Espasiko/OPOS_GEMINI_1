#!/usr/bin/env python3
"""
Test script para verificar la generación de exámenes simulacro
"""
import requests
import json

BACKEND_URL = "http://localhost:8000"

def test_small_exam():
    """Test con pocas preguntas (sin lotes)"""
    print("\n=== Test 1: Examen pequeño (10 preguntas) ===")
    response = requests.post(
        f"{BACKEND_URL}/ai/mock-exam",
        json={
            "topics": ["Incapacidad Temporal", "Jubilación"],
            "num_questions": 10,
            "provider": "deepseek"
        }
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Título: {data.get('title')}")
        print(f"✓ Preguntas generadas: {len(data.get('questions', []))}")
        print(f"✓ Primera pregunta: {data['questions'][0]['question'][:100]}...")
    else:
        print(f"✗ Error: {response.text}")

def test_large_exam():
    """Test con muchas preguntas (con lotes)"""
    print("\n=== Test 2: Examen grande (75 preguntas - con lotes) ===")
    response = requests.post(
        f"{BACKEND_URL}/ai/mock-exam",
        json={
            "topics": ["Incapacidad Temporal", "Jubilación", "Cotización"],
            "num_questions": 75,
            "provider": "deepseek"
        },
        timeout=300  # 5 minutos timeout
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Título: {data.get('title')}")
        print(f"✓ Preguntas generadas: {len(data.get('questions', []))}")
        
        # Verificar que los IDs son únicos
        ids = [q['id'] for q in data['questions']]
        if len(ids) == len(set(ids)):
            print(f"✓ Todos los IDs son únicos")
        else:
            print(f"✗ Hay IDs duplicados")
        
        # Mostrar algunas preguntas
        print(f"\nPrimera pregunta: {data['questions'][0]['question'][:100]}...")
        print(f"Última pregunta: {data['questions'][-1]['question'][:100]}...")
    else:
        print(f"✗ Error: {response.text}")

def test_medium_exam():
    """Test con cantidad media (20 preguntas - con lotes)"""
    print("\n=== Test 3: Examen mediano (20 preguntas - con lotes) ===")
    response = requests.post(
        f"{BACKEND_URL}/ai/mock-exam",
        json={
            "topics": ["Afiliación y Altas/Bajas"],
            "num_questions": 20,
            "provider": "deepseek"
        },
        timeout=120
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Título: {data.get('title')}")
        print(f"✓ Preguntas generadas: {len(data.get('questions', []))}")
    else:
        print(f"✗ Error: {response.text}")

if __name__ == "__main__":
    print("Iniciando tests de generación de exámenes simulacro...")
    print("=" * 60)
    
    try:
        test_small_exam()
        test_medium_exam()
        # test_large_exam()  # Comentado porque tarda mucho
        
        print("\n" + "=" * 60)
        print("Tests completados!")
        
    except Exception as e:
        print(f"\n✗ Error en tests: {e}")
