#!/usr/bin/env python3
"""
MONITOR EN TIEMPO REAL DE INDEXACIÓN DE LEYES
Muestra progreso en vivo de la indexación en Qdrant Cloud
"""
import os
import sys
import time
from pathlib import Path
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
env_path = Path(__file__).parent / 'backend' / '.env.backend'
load_dotenv(env_path)

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print("="*80)
print("📊 MONITOR DE INDEXACIÓN EN TIEMPO REAL")
print("="*80)
print(f"Colección: {COLLECTION_NAME}")
print(f"Qdrant URL: {QDRANT_URL}")
print("="*80)

# Conectar a Qdrant
try:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=30)
    print("✅ Conectado a Qdrant Cloud\n")
except Exception as e:
    print(f"❌ Error conectando: {e}")
    sys.exit(1)

# Estado inicial
try:
    info = client.get_collection(COLLECTION_NAME)
    puntos_iniciales = info.points_count
    print(f"📍 Puntos iniciales: {puntos_iniciales:,}\n")
except Exception as e:
    print(f"❌ Error obteniendo colección: {e}")
    sys.exit(1)

# Leyes esperadas (13 total)
LEYES_ESPERADAS = {
    # Críticas (5)
    "LGSS": {"prioridad": "🔴", "chunks_estimados": 2000},
    "RD_84_1996": {"prioridad": "🔴", "chunks_estimados": 800},
    "RD_2064_1995": {"prioridad": "🔴", "chunks_estimados": 800},
    "RD_1415_2004": {"prioridad": "🔴", "chunks_estimados": 600},
    "Constitucion": {"prioridad": "🔴", "chunks_estimados": 200},
    # Altas (5)
    "Ley_39_2015": {"prioridad": "🟠", "chunks_estimados": 500},
    "Ley_40_2015": {"prioridad": "🟠", "chunks_estimados": 500},
    "RDL_5_2015_EBEP": {"prioridad": "🟠", "chunks_estimados": 400},
    "RD_1430_2009": {"prioridad": "🟠", "chunks_estimados": 300},
    "RD_1300_1995": {"prioridad": "🟠", "chunks_estimados": 300},
    # Medias (3)
    "Ley_19_2021_IMV": {"prioridad": "🟡", "chunks_estimados": 200},
    "LO_3_2018_LOPDGDD": {"prioridad": "🟡", "chunks_estimados": 300},
    "Ley_39_2006_Dependencia": {"prioridad": "🟡", "chunks_estimados": 400}
}

print("="*80)
print("📚 LEYES A INDEXAR (13 total)")
print("="*80)
for ley, info in LEYES_ESPERADAS.items():
    print(f"{info['prioridad']} {ley:30} ~{info['chunks_estimados']:,} chunks")
print("="*80)
print("\n⏳ Monitoreando cada 10 segundos... (Ctrl+C para salir)\n")

puntos_anterior = puntos_iniciales
tiempo_inicio = time.time()
iteracion = 0

try:
    while True:
        iteracion += 1
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio
        
        # Obtener estadísticas actuales
        try:
            info = client.get_collection(COLLECTION_NAME)
            puntos_actuales = info.points_count
            
            # Calcular incremento
            incremento = puntos_actuales - puntos_anterior
            incremento_total = puntos_actuales - puntos_iniciales
            
            # Calcular velocidad
            if tiempo_transcurrido > 0:
                velocidad = incremento_total / tiempo_transcurrido
            else:
                velocidad = 0
            
            # Timestamp
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Mostrar progreso
            print(f"[{timestamp}] Puntos: {puntos_actuales:,} | "
                  f"Incremento: +{incremento:,} | "
                  f"Total nuevo: +{incremento_total:,} | "
                  f"Velocidad: {velocidad:.1f} chunks/seg")
            
            # Intentar obtener distribución por norma
            if iteracion % 6 == 0:  # Cada minuto
                try:
                    # Scroll para obtener muestras
                    scroll_result = client.scroll(
                        collection_name=COLLECTION_NAME,
                        limit=100,
                        with_payload=True,
                        with_vectors=False
                    )
                    
                    # Contar por norma
                    normas_encontradas = {}
                    for point in scroll_result[0]:
                        norma = point.payload.get('norma', 'N/A')
                        normas_encontradas[norma] = normas_encontradas.get(norma, 0) + 1
                    
                    if normas_encontradas:
                        print(f"\n{'='*80}")
                        print(f"📊 DISTRIBUCIÓN POR NORMA (muestra de 100 puntos)")
                        print(f"{'='*80}")
                        for norma, count in sorted(normas_encontradas.items(), key=lambda x: x[1], reverse=True):
                            emoji = LEYES_ESPERADAS.get(norma, {}).get('prioridad', '⚪')
                            print(f"{emoji} {norma:30} {count:3} puntos")
                        print(f"{'='*80}\n")
                except Exception as e:
                    pass  # Ignorar errores de scroll
            
            puntos_anterior = puntos_actuales
            
        except Exception as e:
            print(f"⚠️  Error obteniendo estadísticas: {e}")
        
        # Esperar 10 segundos
        time.sleep(10)
        
except KeyboardInterrupt:
    print(f"\n\n{'='*80}")
    print("🛑 MONITOREO DETENIDO")
    print("="*80)
    
    # Estadísticas finales
    try:
        info = client.get_collection(COLLECTION_NAME)
        puntos_finales = info.points_count
        incremento_total = puntos_finales - puntos_iniciales
        tiempo_total = time.time() - tiempo_inicio
        
        print(f"\n📊 RESUMEN:")
        print(f"   Puntos iniciales: {puntos_iniciales:,}")
        print(f"   Puntos finales: {puntos_finales:,}")
        print(f"   Incremento total: +{incremento_total:,}")
        print(f"   Tiempo transcurrido: {tiempo_total/60:.1f} minutos")
        if tiempo_total > 0:
            print(f"   Velocidad promedio: {incremento_total/tiempo_total:.1f} chunks/seg")
        
        print(f"\n{'='*80}")
        print("✅ Monitor finalizado")
        print("="*80)
    except Exception as e:
        print(f"⚠️  Error obteniendo estadísticas finales: {e}")
