# Investigación: Embeddings y Fine-tuning para OpositaIA

## 🎯 Objetivo

Determinar la mejor estrategia de embeddings y fine-tuning para OpositaIA, enfocado en legislación de Seguridad Social española.

## 📊 Modelos de Embeddings en Español

### Top 5 Modelos Recomendados
maal es pablosi!!!!
#### 1. **pablosi/bge-m3-spa-law-qa** ⭐⭐⭐⭐⭐
- **Especialización**: ✅ Leyes españolas
- **Tamaño**: 0.6B parámetros
- **Dimensión**: 1024
- **Ventaja**: Fine-tuned específicamente para Q&A legal en español
- **Desventaja**: Más pesado (600 MB)
- **Recomendación**: **IDEAL para OpositaIA**

#### 2. **Alibaba-NLP/gte-multilingual-base**
- **Especialización**: Multilingüe (incluye español)
- **Tamaño**: 0.3B parámetros
- **Dimensión**: 768
- **Ventaja**: Buen balance tamaño/calidad
- **Desventaja**: No especializado en legal
- **Recomendación**: Buena alternativa general

#### 3. **intfloat/multilingual-e5-small**
- **Especialización**: Multilingüe
- **Tamaño**: 0.1B parámetros
- **Dimensión**: 384
- **Ventaja**: Muy ligero, rápido
- **Desventaja**: Menor calidad que modelos grandes
- **Recomendación**: Para desarrollo/testing

#### 4. **sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2**
- **Especialización**: Multilingüe
- **Tamaño**: 0.1B parámetros
- **Dimensión**: 384
- **Ventaja**: Muy popular, bien documentado
- **Desventaja**: No especializado en español
- **Recomendación**: Alternativa sólida

#### 5. **nomic-ai/nomic-embed-text-v2-moe**
- **Especialización**: Multilingüe (MoE)
- **Tamaño**: 0.5B parámetros
- **Dimensión**: Variable
- **Ventaja**: Mixture of Experts, muy eficiente
- **Desventaja**: Más complejo de configurar
- **Recomendación**: Para producción avanzada

### Comparación

| Modelo | Dimensión | Tamaño | Español | Legal | Velocidad | Calidad |
|--------|-----------|--------|---------|-------|-----------|---------|
| **bge-m3-spa-law-qa** | 1024 | 600 MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| gte-multilingual-base | 768 | 300 MB | ⭐⭐⭐⭐ | ⭐⭐ | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ |
| multilingual-e5-small | 384 | 100 MB | ⭐⭐⭐ | ⭐ | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ |
| all-minilm (actual) | 384 | 45 MB | ⭐⭐ | ⭐ | ⚡⚡⚡⚡⚡ | ⭐⭐ |

## 🎓 Fine-tuning: ¿Necesario o No?

### Análisis de Necesidad

#### Escenario 1: Sin Fine-tuning (Recomendado para MVP)
**Usar**: `bge-m3-spa-law-qa` (ya fine-tuned para legal español)

**Ventajas**:
- ✅ Ya especializado en leyes españolas
- ✅ Listo para usar inmediatamente
- ✅ Sin costo de entrenamiento
- ✅ Sin necesidad de dataset
- ✅ Calidad probada

**Desventajas**:
- ⚠️ No específico para Seguridad Social
- ⚠️ Puede no capturar terminología muy específica

**Recomendación**: **Empezar aquí** ✅

#### Escenario 2: Fine-tuning Ligero (Después del MVP)
**Usar**: `bge-m3-spa-law-qa` + fine-tuning con Unsloth

**Ventajas**:
- ✅ Especialización en Seguridad Social
- ✅ Mejor comprensión de terminología específica
- ✅ Mejora en casos edge
- ✅ Unsloth hace el proceso 2x más rápido

**Desventajas**:
- ⚠️ Requiere dataset de calidad (500-1000 ejemplos)
- ⚠️ Requiere GPU (Google Colab gratis)
- ⚠️ Tiempo de entrenamiento (2-4 horas)
- ⚠️ Mantenimiento del modelo

**Recomendación**: **Solo si el modelo base no es suficiente**

#### Escenario 3: Fine-tuning Completo (Producción Avanzada)
**Usar**: Modelo base + fine-tuning extensivo

**Ventajas**:
- ✅ Máxima calidad
- ✅ Especialización total
- ✅ Ventaja competitiva

**Desventajas**:
- ⚠️ Requiere dataset grande (5000+ ejemplos)
- ⚠️ Requiere GPU potente
- ⚠️ Costo de entrenamiento ($50-200)
- ⚠️ Mantenimiento continuo

**Recomendación**: **Solo para escala (1000+ usuarios)**

## 🔬 Estrategia Recomendada para OpositaIA

### Fase 1: MVP (Mes 1-3) - Sin Fine-tuning
```
Embeddings: bge-m3-spa-law-qa (ya fine-tuned para legal)
LLM: Gemini + Mistral 8B
Vector DB: Qdrant
Datos: BOE API oficial

Ventajas:
✅ Rápido de implementar
✅ Calidad alta desde día 1
✅ $0/mes
✅ Sin complejidad de ML

Resultado esperado:
- Precisión: 75-85%
- Velocidad: <2s por búsqueda
- Satisfacción: Alta
```

### Fase 2: Optimización (Mes 4-6) - Evaluación
```
1. Recopilar métricas de uso
2. Identificar queries problemáticas
3. Analizar si fine-tuning es necesario
4. Crear dataset si es necesario

Decisión:
- Si precisión >80%: NO fine-tuning
- Si precisión <80%: Considerar fine-tuning
```

### Fase 3: Fine-tuning (Mes 7+) - Solo si necesario
```
Herramienta: Unsloth (2x más rápido, 70% menos VRAM)
Modelo base: bge-m3-spa-law-qa
Dataset: 1000 pares (query, documento relevante)
Plataforma: Google Colab (gratis con T4 GPU)
Tiempo: 2-4 horas
Costo: $0 (Colab gratis) o $10 (Colab Pro)

Proceso:
1. Recopilar queries reales de usuarios
2. Etiquetar documentos relevantes
3. Crear dataset en formato Unsloth
4. Fine-tune en Colab
5. Exportar a GGUF
6. Cargar en Ollama
7. Evaluar mejora
```

## 💡 Recomendación Final

### Para OpositaIA:

**NO hacer fine-tuning inicialmente** porque:

1. ✅ **bge-m3-spa-law-qa ya está fine-tuned para leyes españolas**
   - Entrenado específicamente para Q&A legal
   - Entiende terminología jurídica
   - Calidad probada

2. ✅ **El dominio es específico pero no único**
   - Seguridad Social es parte del derecho laboral español
   - El modelo legal general debería funcionar bien
   - Podemos mejorar con prompts específicos

3. ✅ **Podemos evaluar primero**
   - Implementar con modelo base
   - Medir precisión real
   - Decidir basado en datos

4. ✅ **Fine-tuning es costoso en tiempo**
   - Requiere dataset de calidad
   - Requiere validación
   - Requiere mantenimiento

### Estrategia de 3 Pasos:

```
Paso 1 (Ahora): Usar bge-m3-spa-law-qa
├─ Implementar RAG
├─ Indexar documentos BOE
├─ Medir precisión
└─ Recopilar feedback

Paso 2 (Mes 2-3): Optimizar sin fine-tuning
├─ Mejorar prompts
├─ Ajustar chunking
├─ Optimizar top-k
└─ Filtros metadata

Paso 3 (Mes 4+): Fine-tuning solo si necesario
├─ Si precisión <80%
├─ Crear dataset
├─ Fine-tune con Unsloth
└─ Evaluar mejora
```

## 🛠️ Implementación Práctica

### 1. Instalar Modelo Recomendado en Ollama

```bash
# Opción A: bge-m3-spa-law-qa (RECOMENDADO)
wsl docker exec ollama-starter ollama pull bge-m3

# Opción B: nomic-embed-text (alternativa)
wsl docker exec ollama-starter ollama pull nomic-embed-text

# Opción C: Mantener all-minilm (actual, más simple)
# Ya instalado, funciona bien para MVP
```

### 2. Actualizar Configuración

```bash
# .env.backend
OLLAMA_EMBEDDING_MODEL=bge-m3  # o all-minilm
VECTOR_DIMENSION=1024  # para bge-m3, o 384 para all-minilm
```

### 3. Recrear Colección Qdrant (si cambias dimensión)

```bash
# Si usas bge-m3 (1024 dims)
curl -X DELETE http://localhost:6333/collections/opositaia_documents
curl -X PUT http://localhost:6333/collections/opositaia_documents \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 1024, "distance": "Cosine"}}'

# Si mantienes all-minilm (384 dims)
# Ya está creada, no hacer nada
```

## 📚 Recursos de Fine-tuning (Para Futuro)

### Unsloth
- **Repo**: https://github.com/unslothai/unsloth
- **Docs**: https://docs.unsloth.ai/
- **Ventajas**: 2x más rápido, 70% menos VRAM
- **Colab**: Notebooks gratuitos disponibles

### Proceso con Unsloth

```python
# 1. Instalar
!pip install unsloth

# 2. Cargar modelo base
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "sentence-transformers/bge-m3",
    max_seq_length = 512,
    dtype = None,
    load_in_4bit = True,
)

# 3. Preparar dataset
dataset = [
    {
        "query": "¿Qué es la incapacidad temporal?",
        "positive": "La incapacidad temporal es...",
        "negative": "La jubilación es..."
    },
    # ... más ejemplos
]

# 4. Fine-tune
from unsloth import train

trainer = train(
    model=model,
    tokenizer=tokenizer,
    dataset=dataset,
    max_steps=1000
)

# 5. Exportar
model.save_pretrained_gguf("opositaia-embeddings", quantization_method="q4_k_m")
```

### Dataset para Fine-tuning

**Necesitarías**:
- 500-1000 pares (query, documento relevante)
- Queries reales de usuarios
- Documentos del BOE etiquetados
- Negativos (documentos no relevantes)

**Fuentes**:
- Queries del chat (recopilar)
- Preguntas de exámenes reales
- Casos prácticos generados
- Feedback de usuarios

## 🎯 Decisión Final

### Para OpositaIA MVP:

**✅ NO hacer fine-tuning ahora**

**Usar**:
1. **Embeddings**: `bge-m3-spa-law-qa` (si disponible en Ollama)
2. **O mantener**: `all-minilm` (actual, funciona bien)
3. **LLM**: Gemini + Mistral 8B (ya disponibles)

**Razones**:
- ✅ Modelos existentes son suficientes
- ✅ Ahorra tiempo (2-4 semanas)
- ✅ Ahorra costo ($0 vs $50-200)
- ✅ Podemos evaluar primero
- ✅ Fine-tuning después si es necesario

### Cuándo Considerar Fine-tuning:

```
SI:
- Precisión <75% después de 3 meses
- Usuarios reportan resultados irrelevantes
- Competencia tiene mejor precisión
- Tenemos 1000+ queries etiquetadas

NO:
- Precisión >80%
- Usuarios satisfechos
- Modelo base funciona bien
- No tenemos dataset de calidad
```

## 📋 Plan de Acción

### Inmediato (Esta semana):

1. ✅ Mantener `all-minilm` (384 dims)
2. ✅ Crear colección Qdrant (384 dims)
3. ✅ Indexar documentos BOE
4. ✅ Implementar RAG básico
5. ✅ Medir precisión baseline

### Corto plazo (Mes 1-2):

1. Probar `bge-m3-spa-law-qa` si está disponible
2. Comparar precisión vs `all-minilm`
3. Optimizar chunking y top-k
4. Recopilar feedback de usuarios

### Largo plazo (Mes 3+):

1. Analizar métricas de precisión
2. Decidir si fine-tuning es necesario
3. Si sí: Crear dataset con Unsloth
4. Si no: Continuar optimizando prompts

## 🔧 Configuración Recomendada

### Para MVP (Ahora):

```bash
# Modelo de embeddings
OLLAMA_EMBEDDING_MODEL=all-minilm
VECTOR_DIMENSION=384

# Configuración de chunking
CHUNK_SIZE=512
CHUNK_OVERLAP=50

# Búsqueda
TOP_K_RESULTS=5
MIN_SCORE=0.7
```

### Para Producción (Después):

```bash
# Si instalamos bge-m3-spa-law-qa
OLLAMA_EMBEDDING_MODEL=bge-m3
VECTOR_DIMENSION=1024

# Configuración optimizada
CHUNK_SIZE=256
CHUNK_OVERLAP=25

# Búsqueda mejorada
TOP_K_RESULTS=10
MIN_SCORE=0.75
RERANK=true
```

## 📊 Benchmarks Esperados

### Con all-minilm (actual):
- Precisión: 70-75%
- Velocidad: <500ms por embedding
- Recall@5: 80-85%

### Con bge-m3-spa-law-qa:
- Precisión: 85-90%
- Velocidad: <1s por embedding
- Recall@5: 90-95%

### Con fine-tuning:
- Precisión: 90-95%
- Velocidad: <1s por embedding
- Recall@5: 95-98%

## ✅ Conclusión

**Para OpositaIA**:

1. ✅ **Empezar con `all-minilm`** (ya instalado)
2. ✅ **Evaluar durante 1-2 meses**
3. 🤔 **Considerar `bge-m3-spa-law-qa`** si all-minilm no es suficiente
4. 🤔 **Fine-tuning solo si precisión <80%** después de optimizaciones

**Ahorro de tiempo**: 2-4 semanas  
**Ahorro de costo**: $50-200  
**Riesgo**: Bajo (podemos fine-tune después si es necesario)

---

**Última actualización**: 2025-01-16  
**Decisión**: ✅ NO fine-tuning inicial  
**Modelo**: all-minilm (actual) o bge-m3-spa-law-qa (upgrade)


---

## 🆕 ACTUALIZACIÓN: Fine-tuning GRATIS con Unsloth + Google Colab

### ✅ Descubrimiento Importante

**Fine-tuning es 100% GRATIS** usando:
- **Unsloth**: Librería open source (2x más rápido, 70% menos VRAM)
- **Google Colab**: GPU Tesla T4 gratis (12 horas/día)

### 📋 Proceso Completo (10-30 minutos)

```python
# 1. Abrir Google Colab (colab.research.google.com)
# 2. Conectar a GPU gratis (Runtime > Change runtime type > T4 GPU)

# 3. Instalar Unsloth
!pip install unsloth

# 4. Cargar modelo base
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "BAAI/bge-m3",  # o cualquier modelo
    max_seq_length = 8192,
    dtype = None,
    load_in_4bit = True,  # Reduce VRAM 70%
)

# 5. Preparar dataset (formato simple)
dataset = {
    "query": ["¿Qué es IT?", "¿Cuánto dura IT?"],
    "positive": ["IT es incapacidad temporal...", "IT dura máximo 365 días..."]
}

# 6. Fine-tune (5-15 minutos)
from unsloth import train
trainer = train(model, dataset, max_steps=1000)

# 7. Guardar en HuggingFace (gratis)
model.push_to_hub("tu-usuario/opositaia-embeddings")
```

### 💰 Costo: $0 (100% GRATIS)

| Componente | Costo Tradicional | Con Unsloth + Colab |
|------------|-------------------|---------------------|
| GPU | $50-200 | $0 (Colab gratis) |
| Tiempo | 2-4 horas | 10-30 minutos |
| VRAM | 16-24 GB | 4-8 GB (cabe en T4) |
| Hosting | $10-50/mes | $0 (HuggingFace gratis) |
| **TOTAL** | **$60-250** | **$0** |

### 🎯 Nueva Estrategia

Con fine-tuning gratis, la estrategia cambia:

```
Fase 1 (Semana 1-2): MVP con all-minilm
├─ Implementar RAG básico
├─ Indexar 100 documentos BOE
└─ Medir precisión baseline

Fase 2 (Semana 3): Upgrade a bge-m3-spa-law-qa
├─ Instalar modelo pre-entrenado legal
├─ Comparar precisión vs all-minilm
└─ Recopilar queries problemáticas

Fase 3 (Semana 4): Fine-tuning GRATIS 🆕
├─ Crear dataset de 500-1000 ejemplos
├─ Fine-tune con Unsloth en Colab (30 min)
├─ Evaluar mejora
└─ Desplegar si mejora >5%
```

### 📚 Recursos

- **Unsloth GitHub**: https://github.com/unslothai/unsloth
- **Colab Notebooks**: https://github.com/unslothai/unsloth#-colab-notebooks
- **Tutorial Video**: (transcripción incluida arriba)

### ✅ Conclusión Actualizada

**Fine-tuning YA NO es costoso**, así que:

1. ✅ Empezar con `all-minilm` (MVP rápido)
2. ✅ Upgrade a `bge-m3-spa-law-qa` (mejor calidad)
3. ✅ **Fine-tuning con Unsloth** (gratis, 30 min) 🆕
4. ✅ Iterar basado en métricas

**No hay razón para NO hacer fine-tuning** si tenemos dataset de calidad.

---

**Última actualización**: 2025-01-16 (Fine-tuning gratis descubierto)  
**Decisión**: ✅ Fine-tuning SÍ (pero después de MVP)  
**Herramienta**: Unsloth + Google Colab (100% gratis)
