# Análisis de Costes Reales y Estrategia de Fine-tuning
## Fecha: 30 Noviembre 2025

---

## RESUMEN EJECUTIVO

Este documento analiza:
1. **Costes reales** de APIs actuales (Groq, DeepSeek, Gemini, Mistral)
2. **Coste de generar 1000 simulacros** (75 preguntas) + 1000 casos prácticos
3. **Modelos para fine-tuning** que caben en 16GB RAM (portátil) y 8GB VPS
4. **3 mejores opciones** ordenadas por precio (no por tiempo)

---

## 1. ESTADO ACTUAL DE PROVEEDORES

### Proveedores Implementados ✅
- **Groq** (llama-3.3-70b-versatile) - ✅ Funcionando
- **DeepSeek** (deepseek-chat) - ✅ Funcionando
- **Cohere** (command-r-plus) - ✅ Funcionando
- **Mistral VPS** (modelo local) - ✅ Funcionando

### Proveedores con Problemas ❌
- **Gemini 3 Pro** - ❌ Error 429: Quota exceeded (free tier agotado)
- **Gemini 2.5 Pro** - ⚠️ Error parsing JSON (respuestas mal formateadas)
- **Mistral API** - ❌ NO implementado (solo VPS local)

---

## 2. COSTES REALES ACTUALES

### 2.1 Groq (Llama-3.3-70B)

**Datos reales del CSV** (29-30 Nov 2025):
- 14 requests en 1 día
- Input promedio: ~297 tokens/request
- Output promedio: ~3000 tokens/request (generación de exámenes)
- Total: ~46,000 tokens en 14 requests

**Precios Groq**:
- Input: $0.59/1M tokens
- Output: $0.79/1M tokens

**Cálculo para 1000 simulacros** (75 preguntas cada uno):
```
Estimación por simulacro:
- Input: ~300 tokens (prompt + contexto RAG)
- Output: ~3000 tokens (75 preguntas con opciones y explicaciones)

1000 simulacros:
- Input: 300K tokens × $0.59/1M = $0.177
- Output: 3M tokens × $0.79/1M = $2.37
- TOTAL: $2.55 por 1000 simulacros
```

**Cálculo para 1000 casos prácticos**:
```
Estimación por caso práctico:
- Input: ~400 tokens (prompt + contexto RAG + caso)
- Output: ~1500 tokens (análisis + solución + referencias)

1000 casos prácticos:
- Input: 400K tokens × $0.59/1M = $0.236
- Output: 1.5M tokens × $0.79/1M = $1.185
- TOTAL: $1.42 por 1000 casos prácticos
```

**TOTAL GROQ: $3.97 (1000 simulacros + 1000 casos prácticos)**

---

### 2.2 DeepSeek (deepseek-chat)

**Datos reales del CSV** (25-30 Nov 2025):
- 23 requests totales
- Input cache miss: 9,098 tokens
- Input cache hit: 4,032 tokens (caché funcionando!)
- Output: 25,966 tokens
- **Coste real**: $0.0136 USD (23 requests)

**Precios DeepSeek**:
- Input: $0.14/1M tokens ($0.28/1M sin caché)
- Output: $0.28/1M tokens
- Cache hit: $0.014/1M tokens (10x más barato)

**Cálculo para 1000 simulacros**:
```
Con caché (50% hit rate estimado):
- Input cache miss: 150K tokens × $0.28/1M = $0.042
- Input cache hit: 150K tokens × $0.014/1M = $0.0021
- Output: 3M tokens × $0.28/1M = $0.84
- TOTAL: $0.88 por 1000 simulacros
```

**Cálculo para 1000 casos prácticos**:
```
Con caché (50% hit rate):
- Input cache miss: 200K tokens × $0.28/1M = $0.056
- Input cache hit: 200K tokens × $0.014/1M = $0.0028
- Output: 1.5M tokens × $0.28/1M = $0.42
- TOTAL: $0.48 por 1000 casos prácticos
```

**TOTAL DEEPSEEK: $1.36 (1000 simulacros + 1000 casos prácticos)**
**AHORRO vs Groq: 66%** 🎯

---

### 2.3 Mistral API (NO implementado actualmente)

**Precios Mistral** (según archivo de precios):

#### Mistral Small (mistral-small-latest):
- Input: $0.10/1M tokens
- Output: $0.30/1M tokens
- **Fine-tuning**: $4/1M tokens training, $2/mes storage

**Cálculo para 1000 simulacros**:
```
- Input: 300K × $0.10/1M = $0.03
- Output: 3M × $0.30/1M = $0.90
- TOTAL: $0.93 por 1000 simulacros
```

**Cálculo para 1000 casos prácticos**:
```
- Input: 400K × $0.10/1M = $0.04
- Output: 1.5M × $0.30/1M = $0.45
- TOTAL: $0.49 por 1000 casos prácticos
```

**TOTAL MISTRAL SMALL: $1.42**

#### Mistral Medium (mistral-medium-latest):
- Input: $0.40/1M tokens
- Output: $2.00/1M tokens

**TOTAL MISTRAL MEDIUM: $6.72** (más caro que Groq)

#### Mistral Large (mistral-large-latest):
- Input: $2.00/1M tokens
- Output: $6.00/1M tokens
- **Fine-tuning**: $9/1M tokens training, $4/mes storage

**TOTAL MISTRAL LARGE: $18.60** (muy caro)

---

### 2.4 Cohere (command-r-plus)

**Precios Cohere**:
- Input: $2.50/1M tokens
- Output: $10.00/1M tokens

**TOTAL COHERE: $30.75** (MUY CARO - no recomendado para producción)

---

### 2.5 Gemini (problemas actuales)

**Gemini 2.0 Flash** (free tier):
- ❌ Quota exceeded - No disponible
- Precio si funcionara: ~$0.15/1M tokens (muy barato)

**Gemini 2.5 Pro**:
- ⚠️ Problemas de parsing JSON
- Precio: $1.25/1M input, $5.00/1M output
- **TOTAL estimado: $15.38** (si funcionara correctamente)

---

## 3. COMPARACIÓN DE COSTES PARA PRODUCCIÓN

| Proveedor | 1000 Simulacros | 1000 Casos | TOTAL | vs Groq | Estado |
|-----------|----------------|------------|-------|---------|--------|
| **DeepSeek** | $0.88 | $0.48 | **$1.36** | -66% | ✅ Funcionando |
| **Mistral Small** | $0.93 | $0.49 | **$1.42** | -64% | ❌ No implementado |
| **Groq 70B** | $2.55 | $1.42 | **$3.97** | Baseline | ✅ Funcionando |
| **Mistral Medium** | $2.72 | $4.00 | **$6.72** | +69% | ❌ No implementado |
| **Gemini 2.5 Pro** | $9.75 | $5.63 | **$15.38** | +287% | ⚠️ Errores JSON |
| **Mistral Large** | $12.60 | $6.00 | **$18.60** | +369% | ❌ No implementado |
| **Cohere R+** | $19.50 | $11.25 | **$30.75** | +675% | ✅ Muy caro |

### 🏆 GANADOR ACTUAL: DeepSeek ($1.36 total)
- 66% más barato que Groq
- Ya implementado y funcionando
- Caché inteligente reduce costes aún más

---

## 4. MODELOS PARA FINE-TUNING

### 4.1 Requisitos de Hardware

**Portátil disponible**: 16GB RAM
**VPS disponible**: 8GB RAM

### 4.2 Modelos que Caben en 16GB RAM (Fine-tuning)

#### Opción 1: Mistral 7B (RECOMENDADO) ⭐
- **Tamaño**: ~14GB en FP16, ~7GB en 4-bit quantization
- **Contexto**: 8192 tokens
- **Calidad**: Excelente para español
- **Fine-tuning**: LoRA en 16GB RAM ✅
- **Inferencia**: Cabe en 8GB VPS con quantization ✅
- **Licencia**: Apache 2.0 (comercial)
- **Hugging Face**: `mistralai/Mistral-7B-Instruct-v0.3`

**Estimación de fine-tuning**:
```
Dataset: 10,000 ejemplos (simulacros + casos prácticos)
Tiempo en CPU (16GB RAM): ~5-7 días
Coste: $0 (local)
```

#### Opción 2: Llama 3.2 3B (MÁS RÁPIDO) ⚡
- **Tamaño**: ~6GB en FP16, ~3GB en 4-bit
- **Contexto**: 8192 tokens
- **Calidad**: Buena, pero inferior a Mistral 7B
- **Fine-tuning**: LoRA en 16GB RAM ✅
- **Inferencia**: Cabe perfectamente en 8GB VPS ✅
- **Licencia**: Llama 3.2 Community License
- **Hugging Face**: `meta-llama/Llama-3.2-3B-Instruct`

**Estimación de fine-tuning**:
```
Dataset: 10,000 ejemplos
Tiempo en CPU (16GB RAM): ~2-3 días
Coste: $0 (local)
```

#### Opción 3: Qwen 2.5 7B (MEJOR MULTILINGÜE) 🌍
- **Tamaño**: ~14GB en FP16, ~7GB en 4-bit
- **Contexto**: 32768 tokens (4x más que Mistral!)
- **Calidad**: Excelente en español y chino
- **Fine-tuning**: LoRA en 16GB RAM ✅
- **Inferencia**: Cabe en 8GB VPS con quantization ✅
- **Licencia**: Apache 2.0
- **Hugging Face**: `Qwen/Qwen2.5-7B-Instruct`

**Estimación de fine-tuning**:
```
Dataset: 10,000 ejemplos
Tiempo en CPU (16GB RAM): ~5-7 días
Coste: $0 (local)
```

---

### 4.3 Modelos que Caben en 8GB VPS (Inferencia)

Todos los modelos anteriores caben en 8GB con quantization:

| Modelo | Tamaño 4-bit | Tokens/seg (CPU) | Calidad Español |
|--------|--------------|------------------|-----------------|
| **Llama 3.2 3B** | ~3GB | ~15 tok/s | 7/10 |
| **Mistral 7B** | ~7GB | ~8 tok/s | 9/10 |
| **Qwen 2.5 7B** | ~7GB | ~8 tok/s | 8.5/10 |

---

## 5. ESTRATEGIA DE FINE-TUNING

### 5.1 Dataset de Entrenamiento

**Fuentes**:
1. Simulacros generados con Groq/DeepSeek (1000+)
2. Casos prácticos generados (1000+)
3. Preguntas reales de exámenes (si disponibles)
4. Contenido del BOE indexado en Qdrant

**Formato**:
```json
{
  "instruction": "Genera un simulacro de examen de Seguridad Social española",
  "input": "Tema: Incapacidad Temporal, Dificultad: Intermedia",
  "output": "1. ¿Cuál es la duración máxima de la IT?..."
}
```

**Tamaño objetivo**: 10,000-20,000 ejemplos

---

### 5.2 Proceso de Fine-tuning (Portátil 16GB)

```bash
# 1. Instalar dependencias
pip install transformers datasets peft bitsandbytes accelerate

# 2. Preparar dataset
python prepare_dataset.py --input simulacros.json --output dataset/

# 3. Fine-tuning con LoRA (eficiente en memoria)
python finetune_lora.py \
  --model mistralai/Mistral-7B-Instruct-v0.3 \
  --dataset dataset/ \
  --output models/mistral-7b-ss-finetuned \
  --lora_r 16 \
  --lora_alpha 32 \
  --batch_size 4 \
  --epochs 3 \
  --learning_rate 2e-4

# 4. Merge LoRA weights
python merge_lora.py \
  --base mistralai/Mistral-7B-Instruct-v0.3 \
  --lora models/mistral-7b-ss-finetuned \
  --output models/mistral-7b-ss-merged

# 5. Quantize para VPS (4-bit)
python quantize_model.py \
  --model models/mistral-7b-ss-merged \
  --output models/mistral-7b-ss-4bit \
  --bits 4
```

**Tiempo estimado**: 5-7 días en CPU (portátil 16GB)

---

### 5.3 Despliegue en VPS (8GB)

```bash
# 1. Subir modelo a Hugging Face
huggingface-cli upload opositaia/mistral-7b-ss-4bit models/mistral-7b-ss-4bit

# 2. En VPS, descargar y servir con llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# 3. Convertir a GGUF (formato llama.cpp)
python convert.py models/mistral-7b-ss-4bit --outtype q4_0

# 4. Servir con API
./server -m models/mistral-7b-ss-4bit.gguf -c 8192 --port 8080
```

---

## 6. COMPARACIÓN DE COSTES: API vs Fine-tuned

### Escenario: 10,000 simulacros/mes + 10,000 casos prácticos/mes

| Opción | Coste Mensual | Coste Inicial | Coste Año 1 |
|--------|---------------|---------------|-------------|
| **DeepSeek API** | $13.60 | $0 | $163.20 |
| **Mistral Small API** | $14.20 | $0 | $170.40 |
| **Groq API** | $39.70 | $0 | $476.40 |
| **Mistral 7B Fine-tuned** | $0 | $0 (local) | **$0** |
| **Mistral API Fine-tuned** | $0 | $40 (training) | $64 (storage) |

### 🏆 GANADOR A LARGO PLAZO: Modelo Fine-tuned Local
- Coste inicial: $0 (fine-tuning en portátil)
- Coste mensual: $0 (VPS ya pagado)
- Break-even: Inmediato
- **Ahorro año 1**: $163-476 vs APIs

---

## 7. LAS 3 MEJORES OPCIONES (ORDENADAS POR PRECIO)

### 🥇 OPCIÓN 1: Fine-tune Mistral 7B Local (GRATIS)

**Ventajas**:
- ✅ Coste $0 (fine-tuning en portátil, inferencia en VPS)
- ✅ Especializado en Seguridad Social española
- ✅ Sin límites de uso
- ✅ Privacidad total (datos no salen del VPS)
- ✅ Latencia baja (VPS en Europa)

**Desventajas**:
- ⏳ Requiere 5-7 días de fine-tuning
- 🔧 Requiere trabajo técnico inicial
- 📊 Necesita dataset de calidad (10K+ ejemplos)

**Coste total**:
- Fine-tuning: $0 (portátil)
- Inferencia: $0 (VPS ya pagado)
- **TOTAL: $0/mes**

**Proceso**:
1. Generar 10K ejemplos con DeepSeek ($13.60 one-time)
2. Fine-tune en portátil (5-7 días)
3. Quantize a 4-bit (~7GB)
4. Subir a Hugging Face
5. Desplegar en VPS con llama.cpp
6. Reemplazar Mistral VPS actual

---

### 🥈 OPCIÓN 2: DeepSeek API ($1.36 por 1K simulacros + 1K casos)

**Ventajas**:
- ✅ Ya implementado y funcionando
- ✅ 66% más barato que Groq
- ✅ Caché inteligente reduce costes
- ✅ Sin setup técnico
- ✅ Calidad buena

**Desventajas**:
- 💰 Coste recurrente ($13.60/mes para 10K)
- 🌐 Dependencia de API externa
- 🔒 Datos enviados a terceros

**Coste total**:
- **$1.36 por 1000 simulacros + 1000 casos**
- **$13.60/mes** para 10K de cada
- **$163.20/año**

---

### 🥉 OPCIÓN 3: Mistral Small API ($1.42 por 1K simulacros + 1K casos)

**Ventajas**:
- ✅ Ligeramente más caro que DeepSeek pero mejor español
- ✅ Opción de fine-tuning ($4/1M tokens)
- ✅ Calidad superior en legal español
- ✅ Soporte oficial de Mistral

**Desventajas**:
- ❌ NO implementado actualmente (requiere desarrollo)
- 💰 Coste recurrente ($14.20/mes para 10K)
- 💰 Fine-tuning caro ($40 + $2/mes storage)

**Coste total**:
- **$1.42 por 1000 simulacros + 1000 casos**
- **$14.20/mes** para 10K de cada
- **$170.40/año**

**Coste con fine-tuning**:
- Training: $40 (one-time)
- Storage: $2/mes
- Inferencia: $0.10/1M input, $0.30/1M output (mismo precio)
- **No vale la pena** vs fine-tuning local

---

## 8. RECOMENDACIÓN FINAL

### Estrategia Híbrida Óptima:

#### FASE 1 (Inmediato): Usar DeepSeek
- Coste: $1.36 por 1K simulacros + 1K casos
- Ya implementado
- Generar dataset de 10K ejemplos ($13.60)

#### FASE 2 (1-2 semanas): Fine-tune Mistral 7B
- Usar dataset generado en Fase 1
- Fine-tune en portátil (5-7 días)
- Quantize a 4-bit
- Subir a Hugging Face

#### FASE 3 (Después de fine-tuning): Modelo Local
- Desplegar en VPS
- Coste: $0/mes
- Calidad: Superior (especializado)
- Mantener DeepSeek como fallback

### ROI:
```
Inversión inicial: $13.60 (generar dataset)
Ahorro mensual: $13.60 (vs DeepSeek)
Break-even: 1 mes
Ahorro año 1: $149.60
```

---

## 9. MODELOS DISPONIBLES EN HUGGING FACE (GGUF para VPS)

### Modelos Pre-quantized (listos para usar):

1. **TheBloke/Mistral-7B-Instruct-v0.2-GGUF**
   - Tamaño: 4.37GB (Q4_K_M)
   - Cabe en 8GB VPS ✅
   - Descarga directa

2. **TheBloke/Llama-2-7B-Chat-GGUF**
   - Tamaño: 3.83GB (Q4_0)
   - Cabe en 8GB VPS ✅
   - Menos calidad que Mistral

3. **TheBloke/Qwen2.5-7B-Instruct-GGUF**
   - Tamaño: 4.68GB (Q4_K_M)
   - Cabe en 8GB VPS ✅
   - Excelente multilingüe

### Despliegue Rápido (sin fine-tuning):

```bash
# Opción rápida: Usar modelo pre-quantized
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf

# Servir inmediatamente
./llama.cpp/server -m mistral-7b-instruct-v0.2.Q4_K_M.gguf -c 8192 --port 8080
```

**Ventaja**: Disponible en minutos
**Desventaja**: No especializado en Seguridad Social

---

## 10. PLAN DE ACCIÓN RECOMENDADO

### Semana 1: Preparación
- [ ] Mantener DeepSeek como proveedor principal
- [ ] Generar 10,000 ejemplos de calidad con DeepSeek
- [ ] Validar y limpiar dataset
- [ ] Preparar entorno de fine-tuning en portátil

### Semana 2-3: Fine-tuning
- [ ] Fine-tune Mistral 7B con LoRA (5-7 días)
- [ ] Evaluar calidad del modelo
- [ ] Quantize a 4-bit
- [ ] Subir a Hugging Face

### Semana 4: Despliegue
- [ ] Desplegar modelo en VPS
- [ ] Testing A/B vs DeepSeek
- [ ] Migrar tráfico gradualmente
- [ ] Mantener DeepSeek como fallback

### Resultado Final:
- ✅ Coste $0/mes (vs $13.60 con DeepSeek)
- ✅ Calidad superior (especializado)
- ✅ Privacidad total
- ✅ Sin límites de uso

---

## 11. CORRECCIONES AL DOCUMENTO ANTERIOR

### Errores Identificados:

1. **Gemini 3 Pro**: ❌ NO funciona (quota exceeded)
2. **Gemini 2.5 Pro**: ⚠️ Errores de parsing JSON
3. **Mistral API**: ❌ NO implementado (solo VPS local)
4. **Costes estimados**: Actualizados con datos reales de CSV

### Estado Real de Proveedores:

| Proveedor | Estado | Problema |
|-----------|--------|----------|
| Groq 70B | ✅ OK | Ninguno |
| DeepSeek | ✅ OK | Ninguno |
| Cohere | ✅ OK | Muy caro |
| Mistral VPS | ✅ OK | Lento, no fine-tuned |
| Gemini 3 Pro | ❌ ERROR | Quota exceeded |
| Gemini 2.5 Pro | ⚠️ ERROR | JSON parsing |
| Mistral API | ❌ NO | No implementado |

---

## CONCLUSIÓN

**La mejor estrategia es**:
1. **Corto plazo** (ahora): DeepSeek API ($1.36 por 1K+1K)
2. **Medio plazo** (2-3 semanas): Fine-tune Mistral 7B local ($0/mes)
3. **Largo plazo**: Modelo especializado en VPS + DeepSeek fallback

**Ahorro proyectado**: $163/año vs DeepSeek, $476/año vs Groq

**Inversión requerida**: $13.60 (generar dataset) + 5-7 días de fine-tuning

**ROI**: Inmediato (modelo local es gratis)
