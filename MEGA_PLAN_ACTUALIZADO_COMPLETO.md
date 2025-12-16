# 🚀 MEGA PLAN ACTUALIZADO - RAG + FINE-TUNING COMPLETO
**Fecha:** 15 de diciembre de 2025  
**Versión:** 2.2 - MCP KIRO INTEGRADO  
**Estado:** 🟢 EN EJECUCIÓN - MCP OPERATIVO

---

## 🎉 ACTUALIZACIÓN 15-DIC-2025: MCP OPOSITAIA EN KIRO

**¡HITO COMPLETADO!** El servidor MCP de Opositaia está 100% funcional en Kiro:

| Colección | Chunks Indexados | Estado |
|-----------|------------------|--------|
| opositaia_knowledge | 17,403 | 🟢 GREEN |
| leyes_espana | 1,067 | 🟢 GREEN |
| **TOTAL** | **18,470** | ✅ OPERATIVO |

**Herramientas MCP disponibles:**
- `search_rag` - Búsqueda semántica en leyes SS
- `list_collections` - Listar colecciones Qdrant
- `verify_boe` - Verificar vigencia en BOE
- `search_jurisprudence` - Buscar jurisprudencia
- `get_law_summary` - Resumen de leyes
- `ingest_new_law` - Ingestar nuevas leyes

**Modelo de embeddings:** `pablosi/bge-m3-spa-law-qa-trained-2` (1024 dims)

Ver detalles en: `MEMORIA_15_12_KIRO.md`

---

## 📊 RESUMEN EJECUTIVO

Después de leer **TODOS** los documentos en `docs/` y `docs/archive/`, este es el plan DEFINITIVO que integra:

✅ ACTUALIZACION_DOCS_11_DIC_2025.md - Estado actual real (Smart Chunking)  
✅ MULTI_AGENT_ARCHITECTURE.md - Arquitectura multi-agente  
✅ RAG_INTEGRATION_PLAN.md - Plan de integración completo  
✅ EMBEDDINGS_FINETUNING_RESEARCH.md - Investigación embeddings  
✅ DECISIONES_CLAVE.md - Decisiones técnicas críticas  
✅ LISTA_COMPLETA_LEYES_A_INDEXAR.md - 13 leyes + 4 faltantes  
✅ LEYES_FALTANTES_TEMARIO_OFICIAL.md - Cobertura del temario  
✅ HALLAZGO_BOE_MATERIALES_OPOSICIONES.md - Códigos BOE  
✅ PROPUESTA_MULTI_AGENTES_FINETUNING.md - Pipeline dataset  
✅ LOCAL_INFRASTRUCTURE_STATUS.md - Estado infraestructura  
✅ VPS_INFRASTRUCTURE_AUDIT.md - Audit VPS Hostinger  
✅ MISTRAL_8B_EVALUATION.md - Evaluación Mistral 8B  
✅ ROADMAP.md - Hoja de ruta evolutiva  
✅ COMPETITIVE_ANALYSIS.md - Análisis competitivo  
✅ TESTING_STRATEGY.md - Estrategia de testing  
✅ IMPLEMENTATION_STATUS.md - Estado implementación

---

## 🔗 RECURSOS API BOE OFICIAL (DATOS ABIERTOS)

**Documentación oficial:**
- 📘 API Legislación Consolidada: https://www.boe.es/datosabiertos/documentos/APIconsolidada.pdf
- 📘 API Sumarios BOE: https://www.boe.es/datosabiertos/documentos/APIsumarioBOE.pdf
- 🌐 Portal datos abiertos: https://www.boe.es/datosabiertos/api/api.php

**Endpoints principales:**

```bash
# Datos auxiliares
GET /datosabiertos/api/datos-auxiliares/materias
GET /datosabiertos/api/datos-auxiliares/ambitos
GET /datosabiertos/api/datos-auxiliares/estados-consolidacion
GET /datosabiertos/api/datos-auxiliares/departamentos
GET /datosabiertos/api/datos-auxiliares/rangos
GET /datosabiertos/api/datos-auxiliares/relaciones-anteriores
GET /datosabiertos/api/datos-auxiliares/relaciones-posteriores

# Legislación consolidada
GET /datosabiertos/api/legislacion/consolidada
GET /datosabiertos/api/legislacion/documento/{id}

# Sumarios BOE
GET /datosabiertos/api/boe/sumario/{fecha}
GET /datosabiertos/api/boe/documento/{id}
```

**NOTA:** Todos los agentes del proyecto deben usar la API oficial de datos abiertos del BOE en lugar de scraping HTML/PDF directo  

---

## 🎯 OBJETIVO FINAL

Sistema RAG + IA **100% LOCAL** con:

```
CAPAS DEL RAG:
├─ CAPA 1: LEYES (17 leyes + códigos BOE)
│  ├─ 13 leyes principales LGSS
│  ├─ 4 leyes faltantes (LOPJ, LOTC, LOREG, Ley 34/2014)
│  └─ Códigos BOE (Laboral SS, Función Pública, MUFACE)
│
├─ CAPA 2: JURISPRUDENCIA (1,500+ documentos)
│  ├─ CENDOJ: 1,000 sentencias relevantes SS+AGE
│  ├─ INSS: 500 resoluciones + circulares
│  └─ BOE: Circulares interpretativas
│
└─ CAPA 3: MATERIAL PRÁCTICO (13,000+ documentos)
   ├─ Exámenes oficiales SS 2015-2025
   ├─ Exámenes oficiales AGE 2015-2025
   ├─ 1,000 simulacros generados (multi-agente)
   ├─ 1,000 tests rápidos generados
   └─ 1,000 casos prácticos generados

DATASET FINE-TUNING:
└─ 10,000 Q&A de alta calidad (70% Groq + 30% Mistral)

📁 UBICACIÓN DATASETS Q&A (ACTUALIZADO 6-DIC-2025):
├─ dataset_generator/dataset_output/dataset_consolidado_top30_calidad.jsonl
│  └─ 30 Q&A de alta calidad (score >= 70) - AUDITADO Y LIMPIO ✅
│  └─ Modelos: Claude Sonnet 4.5, Mistral Large Agent, Kiro Max Quality
├─ dataset_generator/dataset_output/dataset_consolidado_top100.jsonl
│  └─ 100 Q&A original multi-IA - BACKUP (incluye 70 de baja calidad)
├─ dataset_output/qa_verificadas_boe_10_20251206.jsonl
│  └─ 20 Q&A verificadas directamente contra BOE real (MÁXIMA CALIDAD) ✅
│  └─ Temas: Jubilación, IT, IP, Desempleo, PNC, Base cotización
├─ dataset_generator/example_dataset.jsonl
│  └─ 3 ejemplos de formato
└─ test_dataset.jsonl / test_dataset_verified.jsonl
   └─ Tests básicos del sistema

📊 RESUMEN DATASETS CALIDAD:
├─ BOE verificado: 20 Q&A (puntuación máxima)
├─ Multi-IA filtrado: 30 Q&A (score >= 70)
└─ TOTAL ALTA CALIDAD: 50 Q&A listas para fine-tuning

MODELO FINE-TUNED:
└─ Mistral 7B Instruct especializado SS+AGE

DESPLIEGUE:
├─ Ollama local (modelo fine-tuned)
├─ Qdrant local (vector DB 3 capas)
├─ FastAPI + React (funcionando)
└─ 0€/mes de costes recurrentes
```

**Coste total:** $18-22 USD  
**Timeline:** 16 semanas (4 meses)  
**ROI:** 90x vs soluciones comerciales  

---

## 💎 HALLAZGOS CRÍTICOS DE LA DOCUMENTACIÓN

### 1. CÓDIGOS BOE (HALLAZGO_BOE_MATERIALES_OPOSICIONES.md)

**DESCUBRIMIENTO:** El BOE tiene códigos actualizados PERMANENTEMENTE:

- **Código Laboral y SS** (id=355): LGSS + normativa completa
- **Código Función Pública** (id=173): EBEP + acceso + disciplinario
- **Código MUFACE/ISFAS** (id=174): Mutualidades funcionarios

**IMPACTO:** No necesitas descargar leyes individuales, ¡el BOE ya tiene compilaciones!

**ACCIÓN:** 
```python
# Descargar códigos compilados del BOE
url = "https://www.boe.es/biblioteca_juridica/codigos/codigo.php?id=355&modo=2"
# Esto te da TODA la normativa de SS actualizada
```

### 2. EMBEDDINGS ESPECIALIZADOS (EMBEDDINGS_FINETUNING_RESEARCH.md)

**RECOMENDACIÓN FINAL:**
- ✅ **MVP:** `bge-m3-spa-law-qa` (768 dims, legal español, gratis)
- ❌ **NO hacer fine-tuning** hasta tener métricas <80% precisión
- ✅ **Alternativa:** `all-minilm` (384 dims, más ligero)

**DECISIÓN:** Empezar con `bge-m3`, solo fine-tune si es necesario

### 3. MULTI-AGENT COST OPTIMIZATION (PROPUESTA_MULTI_AGENTES_FINETUNING.md)

**ESTRATEGIA 70/30:**
```
7,000 Q&A simples → Groq Llama 3.1 70B (GRATIS o $0.70)
3,000 Q&A complejos → Mistral Large 2 ($12)
500 verificaciones → Claude ($2.50)
───────────────────────────────────────────
TOTAL: $15.20 USD (vs $500+ agencias)
```

### 4. LEYES FALTANTES (LEYES_FALTANTES_TEMARIO_OFICIAL.md)

**COBERTURA ACTUAL:** 63.6% (7/11 leyes del temario oficial)

**FALTANTES CRÍTICOS:**
1. **LO 6/1985 - LOPJ** (Poder Judicial) → Organización judicial
2. **LO 2/1979 - LOTC** (Tribunal Constitucional) → Recursos inconstitucionalidad
3. **LO 5/1985 - LOREG** (Régimen Electoral) → Sistema electoral
4. **Ley 34/2014** (Liquidación cuotas SS) → Sistema RED, liquidación

**ACCIÓN:** Indexar estas 4 leyes en Sprint 1

### 5. RAG BEST PRACTICES 2025 (RAG_BEST_PRACTICES_NOV2025.md)

**TOP 5 TÉCNICAS COMPROBADAS:**

1. **Query Expansion** ⭐⭐⭐⭐⭐
   - Generar 2-3 variaciones de la pregunta
   - +30-50% recall
   - Coste: $0 (Groq NO es gratis!!!)

2. **Corrective RAG (CRAG)** ⭐⭐⭐⭐⭐
   - Evaluar calidad de docs recuperados
   - Si score <7 → buscar en web (Gemini + Google Search)
   - +40-60% accuracy

3. **Metadata Filtering** ⭐⭐⭐⭐⭐
   - Filtrar por tema_id, fecha antes de búsqueda
   - Reduce 50% de docs irrelevantes
   - Velocidad: 2x más rápido

4. **Hybrid Search (Semantic + BM25)** ⭐⭐⭐⭐
   - Combinar búsqueda vectorial + keywords
   - Mejor para términos técnicos exactos
   - +15-25% precision

5. **Self-Reflective RAG** ⭐⭐⭐⭐
   - LLM evalúa docs antes de generar respuesta
   - Filtra docs con score <7/10
   - -50% hallucinations

### 6. CHUNKING STRATEGY (RAG_BEST_PRACTICES_NOV2025.md)

**ANÁLISIS DE TAMAÑO:**

```
LGSS: ~300,000 tokens

Opción 1: 512 tokens, 50 overlap → 650 chunks → 2.6 GB Qdrant
Opción 2: 1024 tokens, 100 overlap → 330 chunks → 1.3 GB Qdrant
Opción 3: 256 tokens, 25 overlap → 1,200 chunks → 4.8 GB Qdrant
```

**RECOMENDACIÓN:**
- **MVP:** 512 tokens, 50 overlap (10%)
- **Producción:** Semantic chunking por artículos
- **NO usar:** Overlap >100 tokens (desperdicio)

### 7. INFRAESTRUCTURA LOCAL (LOCAL_INFRASTRUCTURE_STATUS.md)

**ESTADO ACTUAL:**
```
✅ Qdrant: Running (puerto 6333)
   - Colección: boe_docs (3 documentos, 384 dims)
   - Colección: justicio (0 documentos, 768 dims)

✅ Ollama: Running (puerto 11434)
   - tinyllama:latest (637 MB)
   - all-minilm:latest (45 MB)

✅ PostgreSQL: Running (puerto 5432)
   - sim_old-db-1 (healthy)
```

**ACCIÓN:** Limpiar colecciones antiguas, crear nueva `opositaia_documents`

### 8. VPS HOSTINGER (VPS_INFRASTRUCTURE_AUDIT.md)

**SERVICIOS ACTIVOS:**
```
✅ Opositor Agent API (FastAPI) - Puerto 8001
   - 3 semanas uptime
   - 831.9 MB memoria
   - 2 workers

✅ Configuración:
   - LLM_MODEL=ollama:mistral
   - EMBEDDING_MODEL=ollama:nomic-embed-text
   - FALLBACK_MODEL=ollama:phi3:mini

❌ Ollama NO instalado (esperaba localhost:11434)
❌ Mistral 8B GGUF NO encontrado
```

**DECISIÓN:** 
- Opción A: Instalar Ollama en VPS (requiere 8-10 GB espacio)
- Opción B: Usar API existente del VPS (FastAPI ya funcionando)
- **RECOMENDADO:** Opción B (reutilizar API existente)

### 9. MISTRAL 8B EVALUATION (MISTRAL_8B_EVALUATION.md)

**VEREDICTO:** ✅ **SÍ ES SUFICIENTE**

| Tarea | Complejidad | Mistral 8B | Recomendación |
|-------|-------------|------------|---------------|
| Casos prácticos | Alta | ⭐⭐⭐⭐ | Suficiente (usar Gemini Pro para muy complejos) |
| Chat explicativo | Media | ⭐⭐⭐⭐⭐ | Excelente (modelo principal) |
| Búsqueda RAG | Media | ⭐⭐⭐⭐⭐ | Excelente (32K contexto) |
| Mapas mentales | Media-Alta | ⭐⭐⭐⭐ | Suficiente |
| Resúmenes legales | Media | ⭐⭐⭐⭐⭐ | Excelente |
| Flashcards | Baja | ⭐⭐⭐⭐⭐ | Excelente |

**ESTRATEGIA RECOMENDADA:**
- Tier 1 (Simple): Ollama (TinyLlama) → Gratis
- Tier 2 (Medio): Mistral 8B (VPS) → Gratis  
- Tier 3 (Complejo): Gemini Pro → Gratis (con límites)

### 10. ROADMAP EVOLUTIVO (ROADMAP.md)

**FASES ORIGINALES:**
- Fase 0: Backend monolítico (FastAPI) ✅
- Fase 1: RAG avanzado (Qdrant + embeddings) 🔄
- Fase 2: Fine-tuning modelos 📋
- Fase 3: Multi-agente 📋

**INTEGRACIÓN CON ESTE PLAN:**
- Sprint 0-2 = Fase 1 (RAG)
- Sprint 3-5 = Fase 2 (Dataset + Fine-tuning)
- Sprint 6-8 = Fase 3 (Multi-agente + Deploy)

---

## 🗺️ PLAN DE 16 SEMANAS ACTUALIZADO

### 🔴 SPRINT 0: AUDITORÍA Y PREPARACIÓN (Semana 1)

**Objetivo:** Inventario completo de materiales y limpieza de infraestructura

- ✅ 1,000 sentencias CENDOJ indexadas
- ✅ 500 resoluciones INSS indexadas
- ✅ **Capa 1 + 2 completa:** ~3,000-5,000 chunks en Qdrant

---

### 🟡 SPRINT 2: DESCARGA CAPA 3 (Semanas 5-6)

**Objetivo:** Descargar exámenes oficiales (Capa 3)

#### Semana 5: Exámenes SS 2015-2025

**Fuente:** BOE (sección concursos-oposiciones)

**Script:** `backend/agents/exams_ss_downloader.py`

```python
# Buscar en BOE:
# - "Seguridad Social" + "convocatoria" + "examen"
# - Años 2015-2025
# - Descargar PDFs o JSONs si disponibles
```

**Target:** 50-100 exámenes SS

#### Semana 6: Exámenes AGE 2015-2025 + Indexación

**Fuente:** BOE (Administración General del Estado)

**Script:** Similar a SS pero filtrado por AGE

**Target:** 50-100 exámenes AGE

**Indexación:**
```python
# backend/agents/indexar_capa_3.py

# Convertir PDFs a texto (si es PDF)
# Detectar preguntas y respuestas
# Chunking: 256-512 tokens (preguntas más cortas)
# Indexar en Qdrant con metadata: tipo=examen, año, convocatoria
```

**Entregables Sprint 2:**
- ✅ 50-100 exámenes SS indexados
- ✅ 50-100 exámenes AGE indexados
- ✅ **Capa 3 parcial:** ~1,000-2,000 chunks adicionales

**Estado Qdrant:** 4,000-7,000 chunks totales (Capa 1+2+3 parcial)

---

### 🔵 SPRINT 3: GENERACIÓN DATASET MULTI-AGENTE (Semanas 7-10)

**Objetivo:** Generar 10,000 Q&A de alta calidad con pipeline multi-agente

#### Semana 7: Implementar Pipeline Extracción + Clasificación

**Scripts:**
1. `backend/agents/content_extractor.py`
   - Lee PDFs/JSONs de backend/data/
   - Detecta estructura (preguntas, respuestas, artículos)
   - Limpia OCR errors
   - Output: chunks_extracted.jsonl

2. `backend/agents/classifier.py`
   - Clasifica cada chunk: simple (70%) vs complejo (30%)
   - Marca nivel de riesgo: alto (normativa), medio, bajo
   - Output: chunks_classified.jsonl

**Test:** 100 chunks clasificados correctamente

#### Semana 8: Implementar Generadores Q&A

**Scripts:**
1. `backend/agents/qa_generator_groq.py`
   - Genera Q&A simples con Groq Llama 3.1 70B
   - 7,000 Q&A target
   - Prompt optimizado para definiciones, conceptos básicos
   - Output: qa_simple_groq.jsonl

2. `backend/agents/qa_generator_mistral.py`
   - Genera Q&A complejos con Mistral Large 2
   - 3,000 Q&A target
   - Prompt optimizado para procedimientos, cálculos, jurisprudencia
   - Output: qa_complex_mistral.jsonl

**Test:** 50 Q&A de cada tipo, validar calidad

#### Semana 9: Verificación con Claude

**Script:** `backend/agents/qa_verifier_claude.py`

```python
# Verificar muestra del 5% (500 Q&A)
# Claude evalúa:
# - Formato correcto
# - Exactitud legal
# - Citas correctas
# - Confianza score >0.9

# Marcar Q&A problemáticas para revisión manual
```

**Test:** 100% de la muestra verificada

#### Semana 10: Deduplicación + Dataset Final

**Script:** `backend/agents/deduplication.py`

```python
# 1. Detectar duplicados por embeddings (similarity >0.95)
# 2. Filtrar Q&A con confidence <0.7
# 3. Balancear por temas (cada tema ~300-400 Q&A)
# 4. Balancear por años (2015-2025 equitativo)
# 5. Output: dataset_qa_10k_final.jsonl

# 6. Split train/test (80/20)
# - train: 8,000 Q&A
# - test: 2,000 Q&A
```

**Entregables Sprint 3:**
- ✅ dataset_qa_10k_final.jsonl (10,000 Q&A)
- ✅ dataset_train.jsonl (8,000 Q&A)
- ✅ dataset_test.jsonl (2,000 Q&A)
- ✅ Métricas de calidad (avg_confidence: 0.92+)
- ✅ Coste total: $15-20 USD

---

### 🟢 SPRINT 4: GENERACIÓN MATERIAL ADICIONAL (Semanas 11-12)

**Objetivo:** Generar 1,000 simulacros + 1,000 tests + 1,000 casos prácticos

#### Semana 11: Simulacros (100 preguntas cada uno)

**Script:** `backend/agents/simulacro_generator_mistral.py`

```python
# Generar 1,000 simulacros de 100 preguntas
# Usar Mistral para calidad legal
# Basados en temario real + exámenes pasados
# Formato: JSONL con metadata (tema, dificultad)
```

**Coste:** ~$8 (Mistral API)

#### Semana 12: Tests + Casos Prácticos

**Scripts:**
1. `backend/agents/test_generator_groq.py`
   - 1,000 tests rápidos (25 preguntas cada uno)
   - Usar Groq (gratis)
   
2. `backend/agents/casos_practicos_generator.py`
   - 1,000 casos prácticos (análisis completo)
   - Usar Mistral para complejidad legal
   - Basados en jurisprudencia real

**Coste:** ~$4 (Mistral API)

**Entregables Sprint 4:**
- ✅ 1,000 simulacros (100K preguntas)
- ✅ 1,000 tests (25K preguntas)
- ✅ 1,000 casos prácticos
- ✅ **Capa 3 completa:** 13,000+ documentos en Qdrant
- ✅ Coste total Sprint 4: $12 USD

---

### 🟣 SPRINT 5: FINE-TUNING MISTRAL 7B (Semanas 13-14)

**Objetivo:** Fine-tune Mistral 7B con Unsloth en Google Colab (GRATIS)

#### Semana 13: Preparación + Fine-tuning

**Google Colab Notebook:** `fine_tune_mistral_unsloth.ipynb`

```python
# 1. Instalar Unsloth
!pip install unsloth

# 2. Subir dataset_train.jsonl a Colab

# 3. Cargar modelo base
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="mistralai/Mistral-7B-Instruct-v0.3",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True  # QLoRA
)

# 4. Preparar dataset
from datasets import load_dataset
dataset = load_dataset("json", data_files="dataset_train.jsonl")

# 5. Fine-tuning con LoRA
from unsloth import train
trainer = train(
    model=model,
    tokenizer=tokenizer,
    dataset=dataset,
    max_steps=3000,  # 3 epochs aproximadamente
    learning_rate=2e-4,
    per_device_train_batch_size=4
)

# 6. Guardar modelo
model.save_pretrained_gguf("mistral-7b-ss-finetuned", quantization_method="q4_k_m")
```

**Tiempo:** 4-6 horas en GPU T4 (Colab gratis)  
**Coste:** $0 (Colab free tier)

#### Semana 14: Evaluación + Exportación

**Evaluación:**
```python
# Evaluar en test set (2,000 Q&A)
# Métricas: Accuracy, F1, BLEU
# Target: >95% accuracy en test legal
```

**Exportación:**
```python
# Descargar modelo fine-tuned
# Formato: GGUF (compatible con Ollama)
# Tamaño: ~4 GB (q4_k_m cuantizado)
```

**Entregables Sprint 5:**
- ✅ Modelo fine-tuned: `mistral-7b-ss-finetuned.gguf`
- ✅ Métricas evaluación: accuracy >95%
- ✅ Notebook Colab documentado
- ✅ Coste: $0 USD

---

### 🔴 SPRINT 6: DEPLOY LOCAL + INTEGRACIÓN (Semanas 15-16)

**Objetivo:** Desplegar modelo fine-tuned localmente e integrar todo

#### Semana 15: Deploy Ollama + Testing

**1. Instalar modelo en Ollama:**
```bash
# Copiar .gguf a carpeta Ollama
cp mistral-7b-ss-finetuned.gguf ~/.ollama/models/

# Crear Modelfile
cat <<EOF > Modelfile
FROM ./mistral-7b-ss-finetuned.gguf
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM "Eres un experto en Seguridad Social española y AGE. Citas artículos correctamente."
EOF

# Crear modelo Ollama
ollama create mistral-ss-finetuned -f Modelfile

# Verificar
ollama list | grep mistral-ss
```

**2. Integrar con backend:**
```python
# backend/agents/rag_hybrid_search.py

from ollama import Client
ollama = Client()

def search_rag_local(query: str):
    # 1. Query expansion
    queries = expand_query(query)  # 3 variaciones
    
    # 2. Búsqueda en Qdrant (todas las capas)
    results_capa1 = qdrant.search(queries, collection="capa_1_leyes")
    results_capa2 = qdrant.search(queries, collection="capa_2_jurisprudencia")
    results_capa3 = qdrant.search(queries, collection="capa_3_material")
    
    # 3. Metadata filtering
    results_filtered = filter_by_metadata(results, tema_id=query_tema)
    
    # 4. Reranking (opcional)
    results_reranked = rerank(results_filtered)
    
    # 5. Generar respuesta con modelo fine-tuned
    context = format_context(results_reranked[:5])
    prompt = f"Contexto:\n{context}\n\nPregunta: {query}\n\nRespuesta:"
    
    response = ollama.generate(
        model="mistral-ss-finetuned",
        prompt=prompt,
        options={"temperature": 0.3}  # Respuestas más precisas
    )
    
    return {
        "answer": response["response"],
        "sources": results_reranked[:5],
        "confidence": calculate_confidence(response)
    }
```

**3. Testing E2E:**
```python
# 100 queries de prueba
# Medir: latencia, accuracy, confidence
# Target: <2s latencia, >90% accuracy
```

#### Semana 16: Optimización + Cache

**1. Implementar caché Redis:**
```python
import redis
r = redis.Redis()

def search_with_cache(query: str):
    # Check cache
    cached = r.get(query)
    if cached:
        return json.loads(cached)
    
    # If not cached, search
    result = search_rag_local(query)
    
    # Cache result (7 días)
    r.setex(query, 7*24*3600, json.dumps(result))
    
    return result
```

**Ahorro:** 50-70% de búsquedas (queries comunes)

**2. Optimizar Qdrant:**
```python
# HNSW parameters
qdrant.update_collection(
    collection_name="opositaia_documents",
    optimizers_config={
        "indexing_threshold": 20000,
        "default_segment_number": 4
    },
    hnsw_config={
        "m": 16,
        "ef_construct": 100
    }
)
```

**Velocidad:** 2x más rápido

**Entregables Sprint 6:**
- ✅ Modelo fine-tuned corriendo en Ollama local
- ✅ Backend integrado con RAG híbrido (3 capas)
- ✅ Caché Redis funcionando
- ✅ Latencia <2s, accuracy >90%
- ✅ Sistema 100% funcional y local

---

## 💰 RESUMEN DE COSTES REALES

| Fase | Coste |
|------|-------|
| Sprint 0-2: Descarga datos | $0 (APIs públicas) |
| Sprint 3: Dataset Q&A (Groq + Mistral) | $15-20 |
| Sprint 4: Material adicional (Mistral) | $12 |
| Sprint 5: Fine-tuning (Colab gratis) | $0 |
| Sprint 6: Deploy local | $0 |
| **TOTAL** | **$27-32 USD** |

**Nota:** Estimación original $18-22 era optimista, pero $27-32 sigue siendo excelente ROI.

---

## 📊 MÉTRICAS DE ÉXITO

### KPIs Técnicos
- ✅ Qdrant: 13,000+ chunks indexados (3 capas)
- ✅ Dataset: 10,000 Q&A verificadas (92% confidence)
- ✅ Modelo fine-tuned: >95% accuracy en test set
- ✅ Latencia RAG: <2s por búsqueda
- ✅ Cache hit rate: >50%

### KPIs de Negocio
- ✅ Coste: $27-32 USD (vs $500+ mes SaaS)
- ✅ ROI: 150x primer año
- ✅ Independencia: 100% local (0€/mes)
- ✅ Calidad: Mejor que academias comerciales

---

## 🚀 PRÓXIMOS PASOS INMEDIATOS

1. **Leer PLAN_MAESTRO completo** (este documento)
2. **Ejecutar Sprint 0** (limpiar infraestructura)
3. **Iniciar Sprint 1** (descargar códigos BOE)
4. **Seguir cronograma semanal**

**Fecha inicio:** 9 de diciembre de 2025  
**Fecha fin estimada:** 1 de abril de 2026 (16 semanas)

---

## 📚 DOCUMENTACIÓN INTEGRADA

Este plan integra TODA la información de:
- 22 archivos en `docs/`
- 138 archivos en `docs/archive/`
- 25 archivos en raíz del proyecto

**Total:** 185 documentos analizados y consolidados.

---

**Creado:** 5 de diciembre de 2025  
**Responsable:** AI Assistant  
**Estado:** 📋 LISTO PARA EJECUTAR  
**Versión:** 2.0 MEGA-PLAN DEFINITIVO
