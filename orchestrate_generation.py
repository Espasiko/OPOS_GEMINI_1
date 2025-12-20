
import subprocess
import time
import sys

def main():
    print("🚀 Iniciando generación masiva de 100 Q&A (10 lotes de 10)...")
    
    total_batches = 10
    
    for i in range(1, total_batches + 1):
        print(f"\n📦 Lote {i}/{total_batches} iniciando...")
        try:
            # Ejecutar el script de generación (asegúrate de usar el entorno virtual)
            result = subprocess.run(
                ["/home/spas/OPOS_GEMINI_1/.venv/bin/python3", "generate_qa_mistral_real.py"],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✅ Lote {i} completado.")
            # Imprimir solo las líneas relevantes de salida (archivos generados)
            for line in result.stdout.splitlines():
                if "Guardado en:" in line:
                    print(f"   📄 {line.strip()}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error en lote {i}: {e}")
            print(e.stderr)
        
        if i < total_batches:
            wait_time = 15
            print(f"⏳ Esperando {wait_time} segundos para enfriar API y no saturar...")
            time.sleep(wait_time)

    print("\n✨ Generación masiva completada.")

if __name__ == "__main__":
    main()
