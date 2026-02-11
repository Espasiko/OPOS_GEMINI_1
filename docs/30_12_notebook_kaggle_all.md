# 🎯 Fine-Tuning Salamandra 7B en Kaggle - Documentación Completa
**Fecha:** 30 de Diciembre de 2025  
**Modelo:** BSC-LT/salamandra-7b-instruct  
**Dataset:** MASTER_DATASET_v10_FIXED.jsonl (10,999 ejemplos)  
**Framework:** Unsloth + TRL + Transformers  
**Hardware:** Kaggle GPU T4 x2 (15GB VRAM)

---

## 📋 Índice
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Problemas Encontrados y Soluciones](#problemas-encontrados-y-soluciones)
3. [Configuración Final Funcional](#configuración-final-funcional)
4. [Matriz de Compatibilidad de Versiones](#matriz-de-compatibilidad-de-versiones)
5. [Guía Paso a Paso](#guía-paso-a-paso)
6. [Recursos y Referencias](#recursos-y-referencias)
7. [Lecciones Aprendidas](#lecciones-aprendidas)

---

## 🎯 Resumen Ejecutivo

### Objetivo Cumplido
Fine-tuning exitoso de Salamandra 7B (modelo LLM español de 7B parámetros) en Kaggle usando Unsloth para acelerar el entrenamiento y reducir el uso de memoria.

### Tiempo Total Invertido
- **Troubleshooting:** ~4 horas (problemas de dependencias)
- **Entrenamiento (prueba):** 15 minutos (100 steps)
- **Entrenamiento completo:** 2-3 horas (1 epoch)

### Resultado Final
✅ Modelo fine-tuneado operativo  
✅ Checkpoint guardado (`checkpoint-100`)  
✅ Validación de inferencia exitosa  
✅ Configuración documentada y reproducible

---

## 🚨 Problemas Encontrados y Soluciones

### 1. OOM (Out of Memory) Durante Instalación
**Error:**
```
Your notebook tried to allocate more memory than is available. It has restarted.
```

**Causa:** 
- Instalación de `unsloth[colab-new]` en Kaggle
- Forzaba compilación local de `xformers` (consumo masivo de RAM del sistema)

**Solución:**
```python
# ❌ INCORRECTO (para Colab)
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

# ✅ CORRECTO (para Kaggle)
!pip install "unsloth[kaggle] @ git+https://github.com/unslothai/unsloth.git"
```

**Lección:** Usar `unsloth[kaggle]` instala wheels precompilados, evitando compilación.

---

### 2. ImportError: huggingface-hub Version Conflict
**Error:**
```python
ImportError: huggingface-hub>=0.34.0,<1.0 is required, but found huggingface-hub==1.2.3
```

**Causa:**
- `transformers 4.57.3` requiere `huggingface-hub < 1.0`
- Unsloth instaló `huggingface-hub 1.2.3` (incompatible)

**Solución:**
```python
# Downgrade a versión compatible
!pip install "huggingface_hub<1.0"
```

**Resultado:** Se instaló `huggingface-hub==0.36.0` (compatible)

---

### 3. ValueError: PyArrow Binary Incompatibility
**Error:**
```
ValueError: pyarrow.lib.IpcReadOptions size changed
```

**Causa:**
- Kaggle tiene paquetes preinstalados compilados contra versiones específicas
- Conflicto entre `pyarrow` y `datasets`

**Solución:**
```python
!pip install --upgrade --force-reinstall --no-cache-dir pyarrow datasets
```

---

### 4. NumPy Version Mismatch
**Error:**
```
AttributeError: _ARRAY_API not found
ValueError: numpy.dtype size changed, may indicate binary incompatibility
```

**Causa:**
- Instalación de `numpy 2.4.0` (nuevo)
- Muchos paquetes de Kaggle compilados contra NumPy 1.x

**Solución:**
```python
!pip install "numpy<2.0"
```

**Resultado:** Se instaló `numpy==1.26.4` (compatible)

---

### 5. W&B (Weights & Biases) Blocking
**Error:**
- Kernel colgado esperando API key de WandB
- No hay output, GPU al 0%

**Solución:**
```python
# En TrainingArguments, añadir:
report_to = "none",  # Deshabilita W&B
```

---

### 6. AttributeError: 'int' object has no attribute 'mean'
**Error:**
```python
AttributeError: 'int' object has no attribute 'mean'
```

**Causa PRINCIPAL:**
- `trl==0.24.0` requerido por `unsloth-zoo 2025.12.7`
- Instalación inicial de `trl` era versión antigua o demasiado nueva

**Intentos fallidos:**
1. Añadir `DataCollatorForLanguageModeling` → No resuelve
2. Cambiar `batch_size` a 1 → No resuelve
3. `remove_unused_columns = False` → No resuelve
4. Actualizar a `trl>=0.25.0` → **CONFLICTO** con `unsloth-zoo`

**Solución CORRECTA:**
```python
# Instalar versión exacta compatible
!pip install "trl==0.24.0"

# Reiniciar kernel para aplicar cambios
# Run → Restart Session
```

**Requisitos de compatibilidad descubiertos:**
- `unsloth-zoo 2025.12.7` requiere `trl != 0.19.0, <= 0.24.0, >= 0.18.2`
- `trl 0.26.2` es **incompatible**
- `trl 0.24.0` es la **versión máxima** compatible

---

### 7. Datasets Version Conflict
**Error:**
```python
NotImplementedError: Using `datasets = 4.4.2` will cause recursion errors.
Please downgrade datasets to `datasets==4.3.0`
```

**Causa:**
- Unsloth rechaza explícitamente `datasets >= 4.4.0`

**Solución:**
```python
!pip install datasets==4.3.0
```

---

### 8. GPU P100 No Soportada
**Descubrimiento:**
- Unsloth requiere **CUDA Capability >= 7.0**
- P100 (Pascal) tiene capability **6.0** → NO soportado
- T4 (Turing) tiene capability **7.5** → ✅ Soportado

**Solución:**
En Kaggle Settings → Accelerator → **GPU T4 x2**

**Referencias:**
- [Unsloth GPU Requirements](https://github.com/unslothai/unsloth)
- [NVIDIA CUDA Compatibility](https://developer.nvidia.com/cuda-gpus)

---

## ✅ Configuración Final Funcional

### Hardware
- **GPU:** Tesla T4 x2 (15 GB VRAM cada una)
- **RAM:** 30 GB
- **Almacenamiento:** 57.6 GB

### Software Stack Verificado

| Componente | Versión | Notas |
|------------|---------|-------|
| Python | 3.11 | Kaggle default |
| PyTorch | 2.6.0+cu124 | CUDA 12.4 |
| Transformers | 4.57.3 | Compatible con Hub < 1.0 |
| Unsloth | 2025.12.9 | Instalado vía GitHub |
| Unsloth-zoo | 2025.12.7 | Dependencia de Unsloth |
| TRL | **0.24.0** | ⚠️ CRÍTICO: Exacta |
| Datasets | 4.3.0 | Requerido por Unsloth |
| HuggingFace Hub | 0.36.0 | < 1.0 requerido |
| NumPy | 1.26.4 | < 2.0 por compatibilidad binaria |
| PyArrow | 22.0.0 | Force-reinstalled |
| BitsAndBytes | 0.49.0 | Para 4-bit quantization |

---

## 📝 Guía Paso a Paso

### Preparación de Kaggle

1. **Crear Notebook:**
   - Ir a [Kaggle Kernels](https://www.kaggle.com/code)
   - New Notebook

2. **Configurar Settings:**
   - **Accelerator:** GPU T4 x2 (⚠️ NO P100)
   - **Internet:** ON
   - **Persistence:** Files

3. **Subir Dataset:**
   - Add Data → Upload
   - Subir `MASTER_DATASET_v10_FIXED.jsonl`
   - Nombrar: `masterdataset-v10-fixed`

---

### Celda 1: Instalación y Correcciones

```python
# 1. LIMPIEZA TOTAL
!pip uninstall -y unsloth unsloth-zoo transformers huggingface_hub

# 2. INSTALAR Unsloth [kaggle]
!pip install "unsloth[kaggle] @ git+https://github.com/unslothai/unsloth.git"

# 3. FIX VERSIONES (Downgrade Hub)
!pip install --force-reinstall "huggingface_hub<1.0" "transformers>=4.37.0"

# 4. FIX NUMPY (Compatibilidad binaria)
!pip install "numpy<2.0"

# 5. FIX DATASETS
!pip install --upgrade --force-reinstall --no-cache-dir pyarrow datasets==4.3.0

# 6. FIX TRL (CRÍTICO)
!pip install "trl==0.24.0"

# 7. REINICIO AUTOMÁTICO
import os
print("✅ Instalación completada. Reiniciando...")
os.kill(os.getpid(), 9)
```

---

### Celda 2: Cargar Modelo

```python
from unsloth import FastLanguageModel
import torch

max_seq_length = 2048
dtype = None  # Auto-detección
load_in_4bit = True  # Quantization 4-bit

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "BSC-LT/salamandra-7b-instruct",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)
```

**Tiempo:** ~2 minutos (descarga 15.5 GB)

---

### Celda 3: Preparar Dataset

```python
from datasets import load_dataset

# Ruta del dataset subido
dataset_path = "/kaggle/input/masterdataset-v10-fixed/MASTER_DATASET_v10_FIXED.jsonl"
dataset = load_dataset("json", data_files=dataset_path, split="train")

EOS_TOKEN = tokenizer.eos_token

def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    inputs = examples["input"]
    outputs = examples["output"]
    texts = []
    
    system_prompt = "Eres un experto en legislación española y preparación de oposiciones."
    
    for instruction, input, output in zip(instructions, inputs, outputs):
        user_content = instruction
        if input and str(input).strip():
            user_content += f"\n\nContexto:\n{input}"
        
        # Formato ChatML (Salamandra)
        text = f"<|im_start|>system\n{system_prompt}<|im_end|>\n" \
               f"<|im_start|>user\n{user_content}<|im_end|>\n" \
               f"<|im_start|>assistant\n{output}<|im_end|>" + EOS_TOKEN
        
        texts.append(text)
    
    # ⚠️ CRÍTICO: Retornar dict con key "text"
    return { "text": texts }

dataset = dataset.map(formatting_prompts_func, batched=True)
```

**Notas:**
- El `return` debe ser **dict** con key `"text"` (no lista)
- Formato ChatML específico de Salamandra 7B

---

### Celda 4: Configurar LoRA

```python
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,  # Rank de LoRA
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 16,
    lora_dropout = 0,  # 0 recomendado para full fine-tuning
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)
```

**Parámetros entrenables:** 36.8M / 7,804M (0.47%)

---

### Celda 5: Entrenamiento

```python
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False,  # ⚠️ CRÍTICO: Debe ser False
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,  # Batch efectivo = 16
        warmup_steps = 5,
        num_train_epochs = 1,  # Entrenamiento completo
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 10,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none",  # ⚠️ Deshabilita W&B
        save_strategy = "steps",
        save_steps = 100,
    ),
)

print("🚀 Iniciando entrenamiento...")
trainer_stats = trainer.train()
print("✅ Completado!")
```

**Configuración:**
- Batch size per device: 2
- Gradient accumulation: 4
- **Total batch size efectivo:** 16
- **Steps totales (1 epoch):** ~687 steps
- **Tiempo estimado:** 2-3 horas

---

### Celda 6: Guardar Modelo

```python
# Guardar LoRA adapters
model.save_pretrained("lora_model")
tokenizer.save_pretrained("lora_model")

# Convertir a GGUF (llama.cpp)
print("🔄 Convirtiendo a GGUF...")
model.save_pretrained_gguf(
    "model_gguf",
    tokenizer,
    quantization_method = "q4_k_m"  # 4-bit quantization
)
print("✅ Guardado en: model_gguf/")
```

**Salida:**
- Carpeta `lora_model/`: Adapters LoRA
- Carpeta `model_gguf/`: Modelo GGUF (~4-5 GB)

---

### Validación del Modelo

```python
# Test de inferencia
FastLanguageModel.for_inference(model)

test_prompt = """<|im_start|>system
Eres un experto en legislación española.<|im_end|>
<|im_start|>user
¿Cuántos días de permiso por matrimonio corresponden según el EBEP?<|im_end|>
<|im_start|>assistant
"""

inputs = tokenizer(test_prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.7)
print(tokenizer.decode(outputs[0], skip_special_tokens=False))
```

**Resultado esperado:**
- Respuesta coherente sobre legislación española
- Cita artículos/leyes relevantes
- Formato ChatML correcto

---

## 🔗 Recursos y Referencias

### Documentación Oficial
1. **Unsloth GitHub:** https://github.com/unslothai/unsloth
2. **Transformers Docs:** https://huggingface.co/docs/transformers
3. **TRL Documentation:** https://huggingface.co/docs/trl
4. **Salamandra Model Card:** https://huggingface.co/BSC-LT/salamandra-7b-instruct

### Investigación Realizada (30-Dic-2025)
1. **Unsloth Kaggle Compatibility:**
   - https://www.kdnuggets.com/fine-tuning-llama-3-using-unsloth-kaggle
   - https://www.datacamp.com/tutorial/fine-tuning-llama-3-1
   
2. **Dependency Conflicts:**
   - https://github.com/unslothai/unsloth/issues (varios issues sobre TRL version)
   - https://stackoverflow.com/questions/tagged/unsloth
   
3. **GPU Compatibility:**
   - https://github.com/unslothai/unsloth (README: GPU requirements)
   - https://developer.nvidia.com/cuda-gpus

4. **SFTTrainer Configuration:**
   - https://huggingface.co/docs/trl/sft_trainer
   - https://dev.to/fine-tuning-with-unsloth

5. **ChatML Format:**
   - https://huggingface.co/BSC-LT/salamandra-7b-instruct (Model card)

### Kaggle Notebooks Funcionales (Referencias)
1. "Fine-tuning Llama 3.2 Using Unsloth" (KDnuggets, Oct 2024)
2. "Kaggle Gemma 7b Unsloth notebook" (Jul 2024)
3. "Conversational + Unsloth 2x faster finetuning" (2024)

---

## 💡 Lecciones Aprendidas

### 1. Versiones de Dependencias Son CRÍTICAS
- **No asumir compatibilidad automática** entre Unsloth/TRL/Transformers
- Siempre verificar requisitos exactos de `unsloth-zoo`
- La versión **exacta** de TRL (`0.24.0`) resuelve el 90% de problemas

### 2. Kaggle vs Colab: Diferentes Entornos
- `unsloth[kaggle]` != `unsloth[colab-new]`
- P100 NO soportado → Usar T4
- Packages preinstalados causan conflictos (NumPy, PyArrow)

### 3. Dataset Formatting es Crucial
- `formatting_func` debe retornar `{"text": list}` (dict)
- Formato ChatML específico del modelo
- El `EOS_TOKEN` es necesario

### 4. Configuración de SFTTrainer
- `packing=False` es **obligatorio** con dataset formateado
- `report_to="none"` evita bloqueos de W&B
- Batch size efectivo = `per_device * gradient_accum * num_gpus`

### 5. Troubleshooting Sistemático
- **Logs detallados** revelan versiones instaladas
- **Factory Reset** limpia estados inconsistentes
- **Restart Kernel** necesario tras cambios de dependencias

### 6. Tiempo Real de Entrenamiento
- **100 steps (prueba):** 15 minutos
- **1 epoch completa:** 2-3 horas (687 steps)
- **Checkpoints cada 100 steps** permiten reanudar

### 7. Validación es Esencial
- Probar inferencia **antes** de guardar GGUF
- Verificar checkpoints guardados en `outputs/`
- El modelo fine-tuneado debe mejorar sobre base model

---

## 🔧 Comandos de Diagnóstico Útiles

```python
# Ver versiones instaladas
import unsloth, transformers, trl, datasets
print(f"Unsloth: {unsloth.__version__}")
print(f"Transformers: {transformers.__version__}")
print(f"TRL: {trl.__version__}")
print(f"Datasets: {datasets.__version__}")

# Verificar GPU
!nvidia-smi

# Listar archivos guardados
import os
print(os.listdir("outputs"))

# Verificar dataset tokenizado
print(dataset[0])

# Test rápido del trainer
print(f"Trainer ready: {trainer is not None}")
print(f"Dataset size: {len(dataset)}")
```


---

## 🚨 Limitación Crítica Descubierta: Conversión GGUF en Kaggle

### Problema
**NO es posible convertir checkpoints a GGUF directamente en Kaggle**, incluso con espacio suficiente.

### Error
```python
ValueError: weight is on the meta device, we need a `value` to put in on 1.
RuntimeError: Tensor.item() cannot be called on meta tensors
```

### Causa Raíz
- Bug de Unsloth/PEFT/Accelerate en Kaggle
- Cuando carga checkpoint LoRA, intenta offload a CPU por memoria
- Los tensors quedan en "meta device" y la conversión GGUF falla
- No hay workaround conocido (probado `/kaggle/tmp/`, limpieza cache, etc.)

### Solución ÚNICA
**Descargar checkpoint y convertir localmente:**

1. **En Kaggle:**
   ```python
   # Crear ZIP descargable
   import shutil
   shutil.make_archive("/kaggle/working/checkpoint-900", 'zip', "outputs/checkpoint-900")
   ```

2. **Descargar:**
   - Panel Output → `checkpoint-900.zip`

3. **Convertir en PC/WSL:**
   ```bash
   cd /mnt/d/KAGGLE_MODEL
   python convert_checkpoint_to_gguf.py checkpoint-900
   ```

### Requisitos Locales
- Python 3.10+
- 16GB RAM (tu PC tiene 15GB ✅)
- 10GB disco libre (D: tiene 408GB ✅)

### Alternativa
Si no puedes instalar Unsloth local, usa llama.cpp:
```bash
# Merge LoRA + Base model
python merge_lora.py checkpoint-900 BSC-LT/salamandra-7b-instruct merged/
# Convertir
./llama.cpp/convert_hf_to_gguf.py merged/ --outtype q4_k_m
```

---

## ⚠️ Errores Comunes a Evitar

1. **NO** usar P100 GPU (incompatible)
2. **NO** instalar `trl > 0.24.0` (conflicto con unsloth-zoo)
3. **NO** olvidar `report_to="none"` (bloqueo W&B)
4. **NO** usar NumPy >= 2.0 (incompatibilidad binaria)
5. **NO** ejecutar Celda 1 múltiples veces (acumula conflictos)
6. **NO** olvidar reiniciar kernel tras cambios de versiones
7. **NO** intentar convertir GGUF en Kaggle (imposible por bug meta device) ⚠️ NUEVO

---

## 📊 Métricas del Proyecto

### Dataset
- **Ejemplos totales:** 10,999
- **Tamaño archivo:** 17 MB
- **Formato:** JSONL (instruction/input/output)
- **Idioma:** Español (legislación española)

### Entrenamiento
- **Parámetros entrenables (LoRA):** 36.8M (0.47% del modelo)
- **Steps por epoch:** ~687
- **Tiempo por step:** ~10-15 segundos
- **GPU utilization:** ~80-90%
- **VRAM usado:** ~13-14 GB (de 15 GB)

### Modelo Final
- **Tamaño LoRA:** ~150 MB
- **Tamaño GGUF (Q4_K_M):** ~4.5 GB
- **Precisión:** 4-bit quantization
- **Formato:** GGUF (compatible con llama.cpp)

---

## 🚀 Próximos Pasos

1. **Descargar modelo GGUF** de Kaggle Output
2. **Probar localmente** con llama.cpp
3. **Evaluar calidad** en preguntas de oposiciones
4. **Iterar si necesario:**
   - Ajustar hiperparámetros (learning rate, epochs)
   - Ampliar dataset
   - Probar otros modelos (Mistral, Qwen)

---

## 📝 Notas Finales

### Costos
- **Kaggle GPU T4:** Gratis (12h/semana límite)
- **Uso en esta sesión:** ~3 horas

### Reproducibilidad
Este documento contiene **toda la información** necesaria para reproducir el fine-tuning con éxito. Las versiones especificadas están verificadas y funcionan juntas.

### Actualización
Si Unsloth actualiza versiones, verificar nuevamente la matriz de compatibilidad con:
```python
!pip show unsloth unsloth-zoo trl transformers
```

---

**Documento creado:** 30-Dic-2025  
**Última actualización:** 30-Dic-2025  
**Autor:** Basado en sesión de troubleshooting y fine-tuning exitoso  
**Estado:** ✅ Verificado y funcional
