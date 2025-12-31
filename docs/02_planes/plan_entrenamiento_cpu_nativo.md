
# 🐢 Plan de Entrenamiento "CPU NATIVA" (GGUF)

**Situación:** Confirmado "Solo CPU" (Intel Core Ultra).
**Implicación:** Unsloth/Transformers **NO FUNCIONAN** (exigen NVIDIA CUDA). Se romperían o tardarían semanas.
**Solución:** Usar **llama.cpp** directamente. Es la única herramienta capaz de entrenar sobre un GGUF cuantizado usando solo RAM y CPU.

---

## 🛠️ Paso 1: Compilar la Herramienta (llama.cpp)

Tienes `g++` y `make`, así que esto es fácil en WSL:

```bash
# 1. Clonar repo oficial (versión ligera)
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# 2. Compilar (Tardará 2-3 min)
make
```
*Esto generará un binario llamado `finetune` (o `train-text-from-scratch` en versiones viejas, pero ahora usamos `finetune`).*

---

## 📄 Paso 2: Preparar Datos (JSONL -> Texto)

`llama.cpp` no come JSONL. Necesita un `.txt` con formato Alpaca pegado.
Crearé un script `convert_v9_to_txt.py` para esto.

*Formato esperado:*
```text
<s>[INST] Pregunta... [/INST] Respuesta... </s>
```

---

## 🧠 Paso 3: Conseguir el Modelo Base (GGUF)

No uses el de Ollama (es difícil de extraer limpio). Baja uno fresco:
*   Mistral 7B v0.3 (Instruct) en Q4_K_M.
*   Pesa ~4.5GB.
*   Guárdalo en `/mnt/d/models/` (tu disco externo) para no llenar el SSD.

---

## 🏋️ Paso 4: El Comando de Entrenamiento (FINAL CONFIRMADO)

Ejecuta esto desde la carpeta raíz `OPOS_GEMINI_1`:

```bash
# Versión compilada con CMake (ruta correcta)
./llama.cpp/build/bin/llama-finetune \
    --model "/home/spas/OPOS_GEMINI_1/Mistral_guuf/Mistral-7B-Instruct-v0.3.Q4_K_M.gguf" \
    --file "dataset_generator/training_data_v9_llama_cpp.txt" \
    --output-file "oposita_v9_cpu_adapter.gguf" \
    --ctx-size 1024 --rope-freq-base 10000 --rope-freq-scale 1.0 \
    --threads 4 --batch-size 1 --ubatch-size 1 --epochs 1
```

*   **Nota:** `--file` carga tu dataset de texto. `--output-file` es donde guardará el resultado.
*   **Tiempo:** Va a tardar. Es CPU. Déjalo correr.

---

## 🔗 Paso 5: Unir y Usar

1.  Generará `oposita_v9_adapter.gguf` (son solo los cambios).
2.  Usamos `./export-lora` para mezclarlo con el base.
3.  Resultado: Un GGUF final listo para Ollama.

**¿Procedemos?**
Voy a generar el script conversor de datos ahora mismo.
