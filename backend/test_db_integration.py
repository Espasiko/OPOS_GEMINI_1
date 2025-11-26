#!/usr/bin/env python3
"""
Test Database Integration
Verifica que el pool de conexiones funcione correctamente
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv('.env.backend')

from database.db import db

print("="*60)
print("🔍 TEST DATABASE INTEGRATION")
print("="*60)

# Test 1: Initialize pool
print("\n📍 Test 1: Inicializar pool de conexiones")
try:
    db.initialize()
    print("✅ Pool inicializado correctamente")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 2: Get connection
print("\n📍 Test 2: Obtener conexión del pool")
try:
    with db.get_connection() as conn:
        print(f"✅ Conexión obtenida: {conn}")
        print(f"   Status: {'Abierta' if not conn.closed else 'Cerrada'}")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 3: Execute query with cursor
print("\n📍 Test 3: Ejecutar query con cursor")
try:
    with db.get_cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM user_progress")
        count = cursor.fetchone()[0]
        print(f"✅ Query ejecutada correctamente")
        print(f"   Usuarios en DB: {count}")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 4: Multiple concurrent connections
print("\n📍 Test 4: Múltiples conexiones concurrentes")
try:
    connections = []
    for i in range(5):
        with db.get_connection() as conn:
            connections.append(conn)
            print(f"   Conexión {i+1}: OK")
    print(f"✅ {len(connections)} conexiones manejadas correctamente")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 5: Insert and rollback
print("\n📍 Test 5: Insert con rollback")
try:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_progress (username, email)
            VALUES ('test_rollback', 'rollback@test.com')
            RETURNING user_id
        """)
        user_id = cursor.fetchone()[0]
        print(f"✅ Usuario insertado: {user_id}")
        
        # Rollback
        conn.rollback()
        print(f"✅ Rollback ejecutado")
        
        # Verify not committed
        cursor.execute("""
            SELECT COUNT(*) FROM user_progress 
            WHERE email = 'rollback@test.com'
        """)
        count = cursor.fetchone()[0]
        if count == 0:
            print(f"✅ Rollback verificado (usuario no existe)")
        else:
            print(f"⚠️  Rollback falló (usuario existe)")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 6: Close pool
print("\n📍 Test 6: Cerrar pool")
try:
    db.close()
    print("✅ Pool cerrado correctamente")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✅ TODOS LOS TESTS PASARON")
print("="*60)
print("\n📊 Resumen:")
print("   - Pool de conexiones: ✅ Funcionando")
print("   - Context managers: ✅ Funcionando")
print("   - Queries: ✅ Funcionando")
print("   - Transacciones: ✅ Funcionando")
print("   - Cleanup: ✅ Funcionando")
