#!/usr/bin/env python3
"""
Monitor de Ingesta Qdrant - Notifica cada 10 minutos y al finalizar
"""

import time
import subprocess
import sys
from datetime import datetime

COMMAND_ID = "510e8399-895b-4662-82c1-2f06d08b71ae"
CHECK_INTERVAL = 600  # 10 minutos en segundos

def get_ingesta_status():
    """Obtiene el estado actual de la ingesta"""
    try:
        # Leer el log de ingesta
        with open('/home/spas/OPOS_GEMINI_1/ingesta_direct_xml_test_FINAL.log', 'r') as f:
            lines = f.readlines()
            
        # Buscar última línea con "Procesados X/Y chunks"
        for line in reversed(lines):
            if "Procesados" in line and "chunks" in line:
                # Extraer números
                parts = line.split()
                for i, part in enumerate(parts):
                    if '/' in part:
                        current, total = part.split('/')
                        return int(current), int(total)
        
        return None, None
    except Exception as e:
        print(f"❌ Error leyendo log: {e}")
        return None, None

def main():
    print("=" * 80)
    print("🔍 MONITOR DE INGESTA QDRANT")
    print("=" * 80)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Intervalo: {CHECK_INTERVAL // 60} minutos")
    print("=" * 80)
    
    last_current = 0
    
    while True:
        current, total = get_ingesta_status()
        
        if current is None or total is None:
            print(f"\n⏳ {datetime.now().strftime('%H:%M:%S')} - Esperando inicio de ingesta...")
        else:
            percentage = (current / total) * 100
            chunks_desde_ultimo = current - last_current
            
            print(f"\n📊 {datetime.now().strftime('%H:%M:%S')} - Progreso:")
            print(f"   Chunks: {current}/{total} ({percentage:.1f}%)")
            print(f"   Nuevos desde último check: {chunks_desde_ultimo}")
            
            if current >= total:
                print("\n" + "=" * 80)
                print("✅ ¡INGESTA COMPLETADA!")
                print("=" * 80)
                print(f"Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Total chunks procesados: {total}")
                
                # Notificar al usuario (puedes añadir notificación de escritorio aquí)
                subprocess.run(['notify-send', 'Ingesta Qdrant', '✅ Ingesta completada!'], 
                             check=False)
                break
            
            last_current = current
        
        # Esperar 10 minutos
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitor detenido por el usuario")
        sys.exit(0)
