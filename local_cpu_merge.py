#!/usr/bin/env python3
"""
Script de Merge CPU-Only para Salamandra + LoRA
Usa transformers + peft en lugar de unsloth para evitar requerir GPU.
"""

import os
import sys
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Rutas
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
CHECKPOINT_PATH = BASE_DIR / "kaggle_dataset" / "checkpoint-900"
MERGED_DIR = BASE_DIR / "model_merged"
BASE_MODEL_ID = "BSC-LT/salamandra-7b-instruct"

def merge_cpu():
    print(f"🚀 Iniciando Merge en CPU (Lento pero seguro)...")
    print(f"📍 Checkpoint: {CHECKPOINT_PATH}")
    print(f"📍 Base Model: {BASE_MODEL_ID}")
    
    if not CHECKPOINT_PATH.exists():
        print(f"❌ No encuentro el checkpoint en {CHECKPOINT_PATH}")
        sys.exit(1)

    # 1. Cargar Base Model
    print("\n⏳ Cargando modelo base (esto descargará ~14GB)...")
    try:
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_ID,
            device_map="cpu",  # Forzar CPU
            torch_dtype=torch.float16, # Usar FP16 para ahorrar algo de RAM si es posible, sino float32
            low_cpu_mem_usage=True,
            trust_remote_code=True
        )
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)
    except Exception as e:
        print(f"❌ Error cargando base model: {e}")
        sys.exit(1)

    # 2. Cargar Adapter
    print("\n🔗 Cargando LoRA adapters...")
    try:
        model = PeftModel.from_pretrained(
            base_model,
            str(CHECKPOINT_PATH),
            device_map="cpu"
        )
    except Exception as e:
        print(f"❌ Error cargando adapters: {e}")
        sys.exit(1)

    # 3. Merge
    print("\n🔄 Fusionando (Merge and Unload)...")
    model = model.merge_and_unload()

    # 4. Guardar
    print(f"\n💾 Guardando modelo fusionado en {MERGED_DIR}...")
    model.save_pretrained(str(MERGED_DIR))
    tokenizer.save_pretrained(str(MERGED_DIR))

    print("\n✅ Merge completado!")
    print(f"Ahora puedes ejecutar: python3 llama.cpp/convert_hf_to_gguf.py {MERGED_DIR} --outtype q4_k_m")

if __name__ == "__main__":
    merge_cpu()
