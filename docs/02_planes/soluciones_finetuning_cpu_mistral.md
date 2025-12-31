# 🛠️ Soluciones para Fine-Tuning CPU Local (Diciembre 2025)

## 📋 Resumen del Problema

El error `GGML_ASSERT(!node->view_src...)` que encontramos indica que **Mistral 7B v0.3** tiene operaciones de grafo (Sliding Window Attention) que la herramienta `llama-finetune` **no soporta completamente** en su pase hacia atrás.

---

## 📊 Tu Investigación Ya Tiene la Respuesta

He leído tu documento `modelos perplexity research pequeños.md` COMPLETO (495 líneas). Aquí el resumen de TUS conclusiones:

### Conclusión de tu investigación:
> "Mistral 7B v0.3 no está deprecated—sigue siendo viable. Pero **Qwen3-8B y Qwen2.5-7B son evoluciones significativas** diseñadas específicamente para tu caso"

### Benchmark que incluiste:
| Modelo | Ganancia post-fine-tuning | Tool calling (AgentFlux) | Español |
|--------|---------------------------|--------------------------|----------|
| Mistral 7B v0.3 | Baseline | ~62% | Variable |
| **Qwen2.5-7B** | **+46%** | **74-82%** | **98%+** |
| Qwen3-8B | +42% | Similar a Qwen2.5 | ~98% |

---

## ✅ SOLUCIÓN 1: Qwen2.5-7B-Instruct (TU RECOMENDACIÓN)

Tu propia investigación dice:
> "Corto plazo (prototipo): Qwen2.5-7B + AgentFlux LoRA + n8n evaluation (ruta más estable)"

### Parámetros LoRA Óptimos (de tu doc):

| Parámetro | Valor |
|-----------|-------|
| LoRA Rank | 8 (o 32 para máxima calidad) |
| Alpha | 16 |
| Learning Rate | 5e-4 |
| Batch Size | 1 |
| Gradient Accumulation | 8 |
| Target Modules | q_proj, v_proj, k_proj |
| Epochs | 3 |

### Descarga GGUF:
```bash
# Q4_K_M para balance velocidad/calidad (95-97% de FP16)
wget -O /home/spas/OPOS_GEMINI_1/Mistral_guuf/Qwen2.5-7B-Instruct-Q4_K_M.gguf \
  "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf"
```

### Comando de entrenamiento llama.cpp:
```bash
./llama.cpp/build/bin/llama-finetune \
    --model "/home/spas/OPOS_GEMINI_1/Mistral_guuf/Qwen2.5-7B-Instruct-Q4_K_M.gguf" \
    --file "dataset_generator/training_data_v9_llama_cpp.txt" \
    --output-file "oposita_v9_qwen25.gguf" \
    --ctx-size 1024 --threads 4 --batch-size 1 --ubatch-size 1 --epochs 1
```

---

## ✅ SOLUCIÓN 2: Qwen3-8B (TU RECOMENDACIÓN LARGO PLAZO)

Tu propia investigación dice:
> "Largo plazo (producción): Qwen3-8B con thinking mode optional + custom evaluator agent (máxima flexibilidad)"

### Características clave (de tu doc):
- **Thinking Mode**: Razonamiento paso-a-paso con `/think`
- **Non-Thinking Mode**: Respuestas directas para tareas simples
- **32K tokens nativo**, extendible a 131K con YaRN
- **Mantiene AMBOS modos** durante fine-tuning LoRA Rank 8

### Hardware para 8GB (de tu doc):
| Quantización | Tamaño | RAM Requerido | Calidad |
|--------------|--------|---------------|----------|
| Q4_K_M (recomendado) | ~5-5.5GB | ~6.8GB | 95-97% |
| Q5_K_M | ~6.8GB | ~7.9GB | 98-99% |

### Descarga:
```bash
# Q4_K_M de Unsloth (ya soportado por llama.cpp)
wget -O /home/spas/OPOS_GEMINI_1/Mistral_guuf/Qwen3-8B-Q4_K_M.gguf \
  "https://huggingface.co/unsloth/Qwen3-8B-GGUF/resolve/main/Qwen3-8B-Q4_K_M.gguf"
```

---

## 🔬 ANÁLISIS DETALLADO: ¿Qwen3-8B en VPS 8GB? (Investigación Web Dic 2025)

### ✅ RESPUESTA CORTA: SÍ, ES POSIBLE (con condiciones)

Según mi investigación web actualizada:

### 📊 Requisitos de Memoria Qwen3-8B GGUF

| Quantización | Tamaño Archivo | RAM Total Necesaria | ¿Cabe en 8GB? |
|--------------|----------------|---------------------|---------------|
| **Q4_K_M** | ~5.03 GB | ~6.5-7.2 GB | ✅ **SÍ** (ajustado) |
| Q5_K_M | ~5.7 GB | ~7.5-8.0 GB | ⚠️ Límite |
| Q3_K_M | ~4.12 GB | ~5.5-6.0 GB | ✅ **SÍ** (cómodo) |
| Q3_K_S | ~3.77 GB | ~5.0-5.5 GB | ✅ **SÍ** (muy cómodo) |

**Fuente**: HuggingFace, Unsloth, hardware-corner.net (2025)

### 🧠 Thinking Mode en VPS 8GB

**SÍ funciona**, pero con consideraciones:

1. **El thinking mode** (`/think`) genera tokens extra → más memoria KV cache
2. **Contexto recomendado**: Limitar a 4096-8192 tokens (no usar 32K completo)
3. **Overhead sistema**: Dejar ~500MB-1GB para SO y procesos

### 📈 Rendimiento Esperado (CPU-only en VPS 8GB)

| Métrica | Valor Estimado |
|---------|----------------|
| Tokens/segundo | 2-5 t/s (CPU i5/Ryzen) |
| Latencia primera respuesta | 10-30 segundos |
| Uso RAM pico | 6.5-7.5 GB |
| Estable para producción | ⚠️ Ajustado pero viable |

### 🎯 Alternativas Si 8GB No Es Suficiente

Si ves problemas de memoria, considera:

| Modelo | Tamaño | Thinking Mode | RAM Necesaria |
|--------|--------|---------------|---------------|
| **Qwen3-4B** | 4B | ✅ SÍ | ~3.5-4.5 GB |
| Qwen2.5-3B | 3B | ❌ No nativo | ~2.5-3.5 GB |
| Phi-3 Mini (3.8B) | 3.8B | ❌ No nativo | ~2.5-3.5 GB |
| DeepSeek-R1-Distill-7B | 7B | ✅ Nativo | ~5.5-6.5 GB |

### ⚙️ Configuración Óptima para VPS 8GB

```bash
# Ollama con límites de contexto
OLLAMA_NUM_CTX=4096 ollama run qwen3:8b-q4_k_m

# O llama.cpp con parámetros optimizados
./llama-server \
    --model Qwen3-8B-Q4_K_M.gguf \
    --ctx-size 4096 \
    --n-gpu-layers 0 \
    --threads 4
```

### 💡 Mi Recomendación Para Tu VPS 8GB

1. **Empezar con Q4_K_M** (balance calidad/memoria)
2. **Limitar contexto a 4096** tokens
3. **Si hay problemas** → bajar a Q3_K_M o usar Qwen3-4B
4. **Monitorear RAM** con `htop` durante uso

### 🔗 Soporte Confirmado

- **llama.cpp**: ✅ Requiere versión b5401+
- **Ollama**: ✅ `ollama run qwen3:8b`
- **vLLM**: ✅ Soporte completo

---

## ✅ SOLUCIÓN 3: Mistral v0.1 (Si Insistes en Mistral)

**Por qué funciona:** Mistral v0.1 tiene arquitectura más simple (sin SWA problemático).

### Descarga:
```bash
wget -O /home/spas/OPOS_GEMINI_1/Mistral_guuf/Mistral-7B-Instruct-v0.1-Q4_K_M.gguf \
  "https://huggingface.co/bartowski/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/Mistral-7B-Instruct-v0.1-Q4_K_M.gguf"
```

### Comando:
```bash
./llama.cpp/build/bin/llama-finetune \
    --model "/home/spas/OPOS_GEMINI_1/Mistral_guuf/Mistral-7B-Instruct-v0.1-Q4_K_M.gguf" \
    --file "dataset_generator/training_data_v9_llama_cpp.txt" \
    --output-file "oposita_v9_mistral_v01.gguf" \
    --ctx-size 1024 --threads 4 --batch-size 1 --ubatch-size 1 --epochs 1
```

---

## ✅ SOLUCIÓN 4: Intel Extension for Transformers (QLoRA CPU)

Opción flexible pero MÁS LENTA (Python puro en CPU).

### Instalación:
```bash
pip install intel-extension-for-transformers transformers peft accelerate
```

### Script básico:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    load_in_4bit=True,
    device_map="cpu"
)

lora_config = LoraConfig(
    r=8, lora_alpha=16,
    target_modules=["q_proj", "v_proj", "k_proj"],
    lora_dropout=0.05,
)
model = get_peft_model(model, lora_config)
```

---

## 📊 Comparativa Final (De Tu Propia Investigación)

| Tu Prioridad | Recomendación | Por Qué |
|--------------|---------------|----------|
| **Máxima flexibilidad** | Qwen3-8B | Thinking/non-thinking, fine-tuning preserva |
| **Máximo rendimiento probado** | **Qwen2.5-7B** | **46% ganancia AgentFlux, 98%+ español** |
| **Razonamiento sin fine-tuning** | DeepSeek-R1-Distill-7B | Razonamiento destilado |
| **Presupuesto ultra-ajustado** | Mistral v0.1 | Compatible, pero inferior |

---

## 🎯 Mi Recomendación (Alineada con tu investigación)

1. **AHORA:** Descarga **Qwen2.5-7B-Instruct-Q4_K_M** → Es lo que TU investigación recomienda
2. **Si Qwen2.5 falla con llama.cpp:** Prueba **Qwen3-8B** o **Mistral v0.1**
3. **Intel QLoRA** solo como último recurso (muy lento)

---

## ⏳ Expectativas de Tiempo

Con tu CPU Intel Core Ultra y 16GB RAM:
- **1 época, batch=1, ctx=1024:** 24-72 horas
- **Checkpoints periódicos:** Puedes pausar/retomar

---

## 🚀 Siguiente Paso

¿Procedo a descargar Qwen2.5-7B-Instruct y lanzar el entrenamiento?
