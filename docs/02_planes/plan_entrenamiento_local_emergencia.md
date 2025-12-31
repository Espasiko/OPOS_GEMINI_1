
# 🆘 Plan de Emergencia: Fine-Tuning Local (16GB RAM)

**Situación:** Colab agotado. Dataset V9 listo.
**Objetivo:** Entrenar Mistral 7B en tu portátil y cargarlo en Ollama.
**Restricción:** 16GB RAM (Esto es ajustado, pero con Unsloth es posible si tienes GPU dedicada).

---

## 🛑 REQUISITO CRÍTICO: TARJETA GRÁFICA (GPU)

Para usar **Unsloth** (la opción rápida y eficiente), **NECESITAS una GPU NVIDIA**.
*   **Sí tienes NVIDIA (RTX 3060, 4060, etc. con 6GB+ VRAM):** ✅ SE PUEDE.
*   **No tienes NVIDIA (Solo CPU, Intel Iris, AMD):** ❌ Unsloth no funciona. Habría que usar `llama.cpp` (muy lento) o MLX (si fuera Mac).

*Asumiremos que tienes una NVIDIA (común en portátiles Linux/WSL).*

---

## 🛠️ Fase 1: Instalación del Entorno (WSL/Linux)

No ensucies tu entorno global. Crearemos uno específico.

```bash
# 1. Crear entorno aislado con Python 3.10/3.11
conda create --name unsloth_env python=3.10 -y
conda activate unsloth_env

# 2. Instalar Pytorch (Compatible con CUDA)
pip install --upgrade pip
pip install "unsloth[cu121-ampere] @ git+https://github.com/unslothai/unsloth.git" 
# NOTA: Si tu GPU es más antigua (GTX 10XX), usa [cu121] a secas.

# 3. Dependencias extra
pip install --no-deps "xformers<0.0.27" "trl<0.9.0" peft accelerate bitsandbytes
```

---

## 📜 Fase 2: Script de Entrenamiento "Low Memory"

Crearemos `train_local_v9_supreme.py` optimizado para no explotar tu RAM.

**Ajustes Clave para 16GB RAM:**
1.  `load_in_4bit = True` (Obligatorio).
2.  `gradient_accumulation_steps = 8` (Para simular batch grande gastando poca VRAM).
3.  `per_device_train_batch_size = 1` (Mínimo consumo).
4.  `max_seq_length = 2048` (No subir a 4096 o explotará).

---

## 🏃 Fase 3: Ejecución y Monitorización

```bash
# Ejecutar entrenamiento
python train_local_v9_supreme.py
```

*   **Tiempo estimado:** En una RTX 3060 Mobile, tardará unas **5-8 horas** para 1 epoch (11k items).
*   **Peligro:** El portátil se calentará. Asegura ventilación.

---

## 📦 Fase 4: Exportar a Ollama (GGUF)

El script incluirá la conversión automática al final:
1.  Guardará `mistral_v9_supreme.gguf` (versión q4_k_m).
2.  Tú crearás un `Modelfile` para Ollama:

```dockerfile
FROM ./mistral_v9_supreme.gguf
SYSTEM "Eres un experto en oposiciones jurídicas..."
```

3.  Y lo importas: `ollama create oposita_v9 -f Modelfile`

---

## 🚀 PASO INMEDIATO

Voy a generarte el script `train_local_v9_supreme.py` ya configurado para este escenario de bajos recursos.
**¿Me confirmas que tienes GPU NVIDIA?** (Si no, el plan cambia a `llama.cpp`).
