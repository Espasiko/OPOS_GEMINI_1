#!/usr/bin/env python3
"""
Test PostgreSQL Database Connection
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

# Load env
env_path = Path(__file__).parent / '.env.backend'
load_dotenv(env_path)

print("="*60)
print("🔍 TEST POSTGRESQL DATABASE")
print("="*60)

# Get connection params
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "opositaia")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

print(f"\n📍 Conexión:")
print(f"   Host: {POSTGRES_HOST}")
print(f"   Port: {POSTGRES_PORT}")
print(f"   Database: {POSTGRES_DB}")
print(f"   User: {POSTGRES_USER}")

try:
    # Connect
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    cursor = conn.cursor()
    
    print("\n✅ Conexión exitosa")
    
    # Test 1: List tables
    print("\n📋 Tablas disponibles:")
    cursor.execute("""
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public'
        ORDER BY tablename
    """)
    tables = cursor.fetchall()
    for table in tables:
        print(f"   - {table[0]}")
    
    # Test 2: Check user_progress
    print("\n👤 Tabla user_progress:")
    cursor.execute("SELECT COUNT(*) FROM user_progress")
    count = cursor.fetchone()[0]
    print(f"   Usuarios: {count}")
    
    if count > 0:
        cursor.execute("""
            SELECT username, email, total_preguntas, precision_global 
            FROM user_progress 
            LIMIT 5
        """)
        users = cursor.fetchall()
        for user in users:
            print(f"   - {user[0]} ({user[1]}): {user[2]} preguntas, {user[3]}% precisión")
    
    # Test 3: Insert test user
    print("\n➕ Insertando usuario de prueba...")
    try:
        cursor.execute("""
            INSERT INTO user_progress (username, email)
            VALUES ('test_opositaia', 'test@opositaia.local')
            ON CONFLICT (email) DO NOTHING
            RETURNING user_id, username
        """)
        result = cursor.fetchone()
        if result:
            print(f"   ✅ Usuario creado: {result[1]} (ID: {result[0]})")
        else:
            print(f"   ℹ️  Usuario ya existe")
        conn.commit()
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
        conn.rollback()
    
    # Test 4: Check answer_history
    print("\n📝 Tabla answer_history:")
    cursor.execute("SELECT COUNT(*) FROM answer_history")
    count = cursor.fetchone()[0]
    print(f"   Respuestas registradas: {count}")
    
    # Test 5: Check simulacros
    print("\n🎯 Tabla simulacros:")
    cursor.execute("SELECT COUNT(*) FROM simulacros")
    count = cursor.fetchone()[0]
    print(f"   Simulacros realizados: {count}")
    
    # Test 6: Check mind_maps
    print("\n🗺️ Tabla mind_maps:")
    cursor.execute("SELECT COUNT(*) FROM mind_maps")
    count = cursor.fetchone()[0]
    print(f"   Mapas mentales: {count}")
    
    # Test 7: Database size
    print("\n💾 Tamaño de la base de datos:")
    cursor.execute("""
        SELECT pg_size_pretty(pg_database_size('opositaia'))
    """)
    size = cursor.fetchone()[0]
    print(f"   Tamaño: {size}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ TODOS LOS TESTS PASARON")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    sys.exit(1)
