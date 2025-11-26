#!/usr/bin/env python3
"""
Test User Router - Sprint 11
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv('.env.backend')

import requests

BASE_URL = "http://localhost:8000"

print("="*60)
print("🧪 TEST USER ROUTER - SPRINT 11")
print("="*60)

# Test 1: Register user
print("\n📍 Test 1: Registrar usuario")
try:
    response = requests.post(f"{BASE_URL}/user/register", json={
        "username": "test_sprint11",
        "email": "sprint11@test.com"
    })
    
    if response.status_code == 200:
        data = response.json()
        user_id = data["user_id"]
        print(f"✅ Usuario registrado: {data['username']}")
        print(f"   ID: {user_id}")
    elif response.status_code == 400:
        print(f"ℹ️  Usuario ya existe")
        # Get user_id from DB
        from database.db import db
        with db.get_cursor() as cursor:
            cursor.execute(
                "SELECT user_id FROM user_progress WHERE email = 'sprint11@test.com'"
            )
            user_id = str(cursor.fetchone()[0])
            print(f"   Usando ID existente: {user_id}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 2: Get progress
print("\n📍 Test 2: Obtener progreso")
try:
    response = requests.get(f"{BASE_URL}/user/{user_id}/progress")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Progreso obtenido:")
        print(f"   Preguntas: {data['total_preguntas']}")
        print(f"   Precisión: {data['precision_global']}%")
        print(f"   Días estudiados: {data['dias_estudiados']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 3: Update session
print("\n📍 Test 3: Actualizar sesión")
try:
    response = requests.put(f"{BASE_URL}/user/{user_id}/session", json={
        "duracion": 1800,  # 30 minutos
        "preguntas_respondidas": 20,
        "preguntas_correctas": 15,
        "temas_estudiados": [1, 2, 3]
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sesión actualizada:")
        print(f"   Session ID: {data['session_id']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 4: Get stats
print("\n📍 Test 4: Obtener estadísticas")
try:
    response = requests.get(f"{BASE_URL}/user/{user_id}/stats")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Estadísticas obtenidas:")
        print(f"   Tiempo total: {data['tiempo_total_horas']:.2f} horas")
        print(f"   Simulacros: {data['simulacros_realizados']}")
        print(f"   Casos creados: {data['casos_creados']}")
        print(f"   Mapas creados: {data['mapas_creados']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✅ TODOS LOS TESTS PASARON")
print("="*60)
print("\n📊 Sprint 11 completado:")
print("   - Router de usuarios: ✅")
print("   - Registro: ✅")
print("   - Progreso: ✅")
print("   - Sesiones: ✅")
print("   - Estadísticas: ✅")
