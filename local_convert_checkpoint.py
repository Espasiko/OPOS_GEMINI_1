#!/usr/bin/env python3
"""
Convierte Checkpoint descargado de Kaggle a GGUF
Ruta del Checkpoint: /home/spas/OPOS_GEMINI_1/kaggle_dataset/checkpoint-900
"""

import sys
import os
from pathlib import Path

# Ajustar rutas
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
CHECKPOINT_PATH = BASE_DIR / "kaggle_dataset" / "checkpoint-900"
OUTPUT_DIR = BASE_DIR / "model_gguf"

def convert_now():
    print(f"🚀 Iniciando conversión local...")
    print(f"📍 Checkpoint: {CHECKPOINT_PATH}")
    print(f"📂 Salida: {OUTPUT_DIR}")

    if not CHECKPOINT_PATH.exists():
        print(f"❌ Error: No encuentro el checkpoint en {CHECKPOINT_PATH}")
        sys.exit(1)

    try:
        from unsloth import FastLanguageModel
    except ImportError:
        print("\n❌ Error: 'unsloth' no está instalado.")
        print("Instálalo ejecutando:")
        print('pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"')
        print('pip install --no-deps "trl<0.9.0" peft accelerate bitsandbytes')
        sys.exit(1)

    # Crear directorio salida
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    print("\n⏳ Cargando modelo (Esto puede descargar el modelo base Salamandra 7B)...")
    try:
        model, tokenizer = FastLanguageModel.from_pretrained(
            str(CHECKPOINT_PATH),
            max_seq_length = 2048,
            dtype = None,
            load_in_4bit = True,
        )
    except Exception as e:
        print(f"\n❌ Error cargando modelo: {e}")
        sys.exit(1)

    print("\n🔄 Convirtiendo a GGUF (q4_k_m)...")
    print("   Esto tomará unos minutos...")

    try:
        model.save_pretrained_gguf(
            str(OUTPUT_DIR),
            tokenizer,
            quantization_method = "q4_k_m"
        )
    except Exception as e:
        print(f"\n❌ Error durante la conversión: {e}")
        sys.exit(1)

    print(f"\n✅ ¡ÉXITO! Modelo guardado en: {OUTPUT_DIR}")
    print(f"   Archivo GGUF listo para usar con llama.cpp u Ollama.")

if __name__ == "__main__":
    convert_now()
