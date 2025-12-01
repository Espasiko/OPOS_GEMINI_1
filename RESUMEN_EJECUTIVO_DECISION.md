# Resumen Ejecutivo para Decisión
## Fecha: 30 Noviembre 2025

---

## TU SITUACIÓN ACTUAL

### Hardware Disponible:
- ✅ Portátil: 16GB RAM (para fine-tuning)
- ✅ VPS: 8GB RAM (para inferencia)
- ✅ Tiempo: No importa (puedes dejar 1 semana fine-tuning)

### Proveedores que Funcionan:
- ✅ **Groq** (llama-3.3-70b): $3.97 por 1K simulacros + 1K casos
- ✅ **DeepSeek**: $1.36 por 1K simulacros + 1K casos (66% más barato)
- ✅ **Cohere**: $30.75 (MUY CARO - no usar)
- ✅ **Mistral VPS**: Gratis pero lento y no especializado

### Proveedores con Problemas:
- ❌ **Gemini 3 Pro**: Error 429 (quota exceeded)
- ⚠️ **Gemini 2.5 Pro**: Errores de parsing JSON
- ❌ **Mistral API**: NO implementado

---

## LAS 3 MEJORES OPCIONES (ORDENADAS POR PRECIO)

### 🥇 OPCIÓN 1: FINE-TUNE MISTRAL 7B LOCAL

**Coste**: **$0/mes** (después de setup inicial)

**Proceso**:
1. Generar 10K ejemplos con DeepSeek: **$13.60** (one-time)
2. Fine-tune en tu portátil: **5-7 días** (sin supervisión)
3. Quantize a 4-bit: **~7GB** (cabe en VPS de 8GB)
4. Subir a Hugging Face: **Gratis**
5. Desplegar en VPS: **$0** (VPS ya pagado)

**Ventajas**:
- ✅ Coste $0/mes (vs $13.60/mes DeepSeek)
- ✅ Especializado en Seguridad Social española
- ✅ Sin límites de uso
- ✅ Privacidad total
- ✅ Latencia baja (VPS en Europa)
- ✅ Puedes dejarlo 1 semana sin problema

**Desventajas**:
- ⏳ Requiere 5-7 días de fine-tuning (pero no importa)
- 🔧 Requiere trabajo técnico inicial
- 📊 Necesita dataset de calidad

**ROI**:
- Inversión: $13.60 (dataset)
- Ahorro: $13.60/mes (vs DeepSeek)
- Break-even: **1 mes**
- Ahorro año 1: **$149.60**

**Modelo recomendado**: `mistralai/Mistral-7B-Instruct-v0.3`
- Tamaño: ~7GB en 4-bit
- Calidad: 9/10 en español legal
- Contexto: 8192 tokens

---

### 🥈 OPCIÓN 2: DEEPSEEK API

**Coste**: **$1.36** por 1K simulacros + 1K casos

**Ventajas**:
- ✅ Ya implementado y funcionando
- ✅ 66% más barato que Groq
- ✅ Caché inteligente (50% hit rate)
- ✅ Sin setup técnico
- ✅ Calidad buena

**Desventajas**:
- 💰 Coste recurrente ($13.60/mes para 10K)
- 🌐 Dependencia de API externa
- 🔒 Datos enviados a terceros

**Coste mensual** (10K simulacros + 10K casos):
- **$13.60/mes**
- **$163.20/año**

---

### 🥉 OPCIÓN 3: MISTRAL SMALL API

**Coste**: **$1.42** por 1K simulacros + 1K casos

**Ventajas**:
- ✅ Mejor español legal que DeepSeek
- ✅ Opción de fine-tuning oficial
- ✅ Soporte de Mistral

**Desventajas**:
- ❌ NO implementado (requiere desarrollo)
- 💰 Coste recurrente ($14.20/mes para 10K)
- 💰 Fine-tuning caro ($40 + $2/mes storage)

**Coste mensual** (10K simulacros + 10K casos):
- **$14.20/mes**
- **$170.40/año**

**Coste con fine-tuning oficial**:
- Training: $40 (one-time)
- Storage: $2/mes
- **NO vale la pena** vs fine-tuning local

---

## COMPARACIÓN DIRECTA

| Opción | Coste Inicial | Coste Mensual | Coste Año 1 | Calidad | Privacidad |
|--------|---------------|---------------|-------------|---------|------------|
| **Fine-tune Local** | $13.60 | **$0** | **$13.60** | ⭐⭐⭐⭐⭐ | ✅ Total |
| **DeepSeek API** | $0 | $13.60 | $163.20 | ⭐⭐⭐⭐ | ❌ Externa |
| **Mistral Small API** | $0 | $14.20 | $170.40 | ⭐⭐⭐⭐⭐ | ❌ Externa |
| **Groq API** | $0 | $39.70 | $476.40 | ⭐⭐⭐⭐ | ❌ Externa |

---

## MI RECOMENDACIÓN

### Estrategia Híbrida (Lo Mejor de Ambos Mundos):

#### FASE 1 (Esta semana): Usar DeepSeek
- Ya está implementado
- Generar 10,000 ejemplos de calidad
- Coste: $13.60 (one-time)
- Validar y limpiar dataset

#### FASE 2 (Próximas 2 semanas): Fine-tune Mistral 7B
- Usar dataset de Fase 1
- Fine-tune en tu portátil (5-7 días sin supervisión)
- Quantize a 4-bit (~7GB)
- Subir a Hugging Face
- Coste: $0

#### FASE 3 (Después): Modelo Local + DeepSeek Fallback
- Desplegar modelo en VPS
- Usar DeepSeek como fallback si VPS cae
- Coste: $0/mes
- Calidad: Superior (especializado)

### Resultado Final:
- ✅ Coste $0/mes (vs $13.60 DeepSeek, $39.70 Groq)
- ✅ Calidad superior (especializado en SS española)
- ✅ Privacidad total (datos no salen del VPS)
- ✅ Sin límites de uso
- ✅ Fallback robusto (DeepSeek si VPS cae)

---

## MODELOS PARA FINE-TUNING (16GB RAM)

### Opción A: Mistral 7B ⭐ RECOMENDADO
- **Tamaño**: ~7GB en 4-bit
- **Calidad**: 9/10 en español legal
- **Contexto**: 8192 tokens
- **Tiempo**: 5-7 días en CPU
- **Licencia**: Apache 2.0 (comercial)
- **HuggingFace**: `mistralai/Mistral-7B-Instruct-v0.3`

### Opción B: Llama 3.2 3B (Más rápido)
- **Tamaño**: ~3GB en 4-bit
- **Calidad**: 7/10 en español
- **Contexto**: 8192 tokens
- **Tiempo**: 2-3 días en CPU
- **Licencia**: Llama 3.2 Community
- **HuggingFace**: `meta-llama/Llama-3.2-3B-Instruct`

### Opción C: Qwen 2.5 7B (Mejor multilingüe)
- **Tamaño**: ~7GB en 4-bit
- **Calidad**: 8.5/10 en español
- **Contexto**: 32768 tokens (4x más!)
- **Tiempo**: 5-7 días en CPU
- **Licencia**: Apache 2.0
- **HuggingFace**: `Qwen/Qwen2.5-7B-Instruct`

**Mi recomendación**: **Mistral 7B** (mejor balance calidad/tamaño/licencia)

---

## PLAN DE ACCIÓN DETALLADO

### Semana 1: Preparación
```bash
# 1. Generar dataset con DeepSeek (ya implementado)
python generate_dataset.py --provider deepseek --count 10000 --output dataset/

# Coste: $13.60
# Tiempo: 2-3 horas
```

### Semana 2-3: Fine-tuning (Portátil 16GB)
```bash
# 2. Instalar dependencias
pip install transformers datasets peft bitsandbytes accelerate

# 3. Fine-tune con LoRA (eficiente en memoria)
python finetune_lora.py \
  --model mistralai/Mistral-7B-Instruct-v0.3 \
  --dataset dataset/ \
  --output models/mistral-7b-ss \
  --epochs 3

# Tiempo: 5-7 días (sin supervisión)
# Coste: $0 (local)
```

### Semana 4: Despliegue (VPS 8GB)
```bash
# 4. Quantize a 4-bit
python quantize_model.py \
  --model models/mistral-7b-ss \
  --output models/mistral-7b-ss-4bit \
  --bits 4

# 5. Subir a Hugging Face
huggingface-cli upload opositaia/mistral-7b-ss-4bit models/mistral-7b-ss-4bit

# 6. Desplegar en VPS con llama.cpp
./llama.cpp/server -m mistral-7b-ss-4bit.gguf -c 8192 --port 8080

# Tiempo: 2-3 horas
# Coste: $0 (VPS ya pagado)
```

---

## PREGUNTAS PARA TI

### 1. ¿Qué opción prefieres?

**A) Fine-tune local** (mi recomendación)
- Coste: $13.60 inicial, luego $0/mes
- Tiempo: 5-7 días fine-tuning
- Calidad: Máxima (especializado)

**B) DeepSeek API**
- Coste: $13.60/mes
- Tiempo: Ya funciona
- Calidad: Buena

**C) Mistral Small API**
- Coste: $14.20/mes
- Tiempo: Requiere desarrollo
- Calidad: Excelente

### 2. ¿Qué modelo para fine-tuning?

**A) Mistral 7B** (recomendado)
- Mejor español legal
- 5-7 días

**B) Llama 3.2 3B** (más rápido)
- Menor calidad
- 2-3 días

**C) Qwen 2.5 7B** (más contexto)
- 32K tokens contexto
- 5-7 días

### 3. ¿Cuándo empezamos?

**A) Ahora** (generar dataset esta semana)
**B) Después** (seguir con DeepSeek por ahora)
**C) Nunca** (solo APIs)

---

## RESUMEN ULTRA-CORTO

**Situación**: Tienes portátil 16GB + VPS 8GB, tiempo no importa

**Mejor opción**: Fine-tune Mistral 7B local
- Coste: $13.60 (dataset) + $0/mes
- Tiempo: 5-7 días (sin supervisión)
- Ahorro: $163/año vs DeepSeek

**Alternativa**: DeepSeek API
- Coste: $13.60/mes
- Ya funciona
- 66% más barato que Groq

**Mi recomendación**: Hacer ambas
1. Usar DeepSeek ahora
2. Fine-tune Mistral 7B en paralelo
3. Migrar a modelo local cuando esté listo
4. Mantener DeepSeek como fallback

**¿Qué decides?** 🤔
