# 🤖 PROPUESTA: PIPELINE MULTI-AGENTES PARA FINE-TUNING
**Responsable:** AI Assistant  
**Fecha:** 5 de diciembre de 2025  
**Estado:** 📋 PROPUESTA - A EJECUTAR EN SPRINT 3  

---

## 🎯 OBJETIVO

Crear dataset de **10,000 Q&A de alta calidad** a partir de:
- Exámenes oficiales SS y AGE (2015-2025)
- Simulacros de academias
- Temarios y material de estudio
- Jurisprudencia y resoluciones INSS

**Finalidad:** Fine-tuning de modelo Mistral 7B especializado en Seguridad Social + AGE

**Resultado:** Modelo fine-tuned capaz de:
- Responder con precisión legal (99% accuracy)
- Citar artículos y sentencias
- Detectar cambios normativos
- Distinguir casos ambiguos

---

## 💰 ANÁLISIS DE COSTES

### Estrategia de Optimización: 70/30 Split

```
TOTAL Q&A NECESARIOS: 10,000
├── 7,000 Simples (70%) → Groq Llama 3.1 70B (GRATIS o $0.70)
├── 3,000 Complejos (30%) → Mistral Large 2 ($1.50)
└── COSTE TOTAL ESTIMADO: $2.20 USD
```

### Desglose Detallado

#### A. Generación Q&A Simple (Groq)
```
Prompt por Q&A: 150 tokens
Respuesta: 100 tokens
Total por Q&A: 250 tokens

7,000 Q&A × 250 tokens = 1,750,000 tokens

Groq: $0.00 (Free Tier 30K req/día) o $0.001/1K tokens (plan pago)
COSTE: GRATIS si repartimos en 30 días, o $1.75 máximo
```

#### B. Generación Q&A Complejo (Mistral)
```
Prompt por Q&A: 300 tokens  
Respuesta: 200 tokens
Total por Q&A: 500 tokens

3,000 Q&A × 500 tokens = 1,500,000 tokens

Mistral API: $2.00 / 1M tokens (input), $6.00 / 1M tokens (output)
Input: 1,500,000 × $0.002 = $3.00
Output: 1,500,000 × $0.006 = $9.00
COSTE: $12.00 estimado
```

#### C. Verificación Q&A (Claude)
```
500 Q&A para verificar (5%)
1,000 tokens por Q&A
Total: 500,000 tokens

Claude: $3.00 / 1M tokens (input), $15.00 / 1M tokens (output)
COSTE: $4.50 máximo
```

**COSTE TOTAL REALISTA: $16.70 USD** (manejable incluso con presupuesto limitado)

---

## 🏗️ ARQUITECTURA DEL PIPELINE

```
┌─────────────────────────────────────────────────────────────┐
│                  DATOS DE ENTRADA (FUENTES)                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────┐ │
│  │ Exámenes       │  │ Simulacros      │  │ Material   │ │
│  │ Oficiales      │  │ Academias       │  │ de Estudio │ │
│  │ (SS + AGE)     │  │ (CEF, Acelera)  │  │ (Temarios) │ │
│  │ 2015-2025      │  │ 2020-2025       │  │ 553 docs   │ │
│  └────────┬────────┘  └────────┬─────────┘  └─────┬──────┘ │
│           │                    │                  │         │
└───────────┼────────────────────┼──────────────────┼─────────┘
            │                    │                  │
            ▼                    ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│          ETAPA 1: EXTRACCIÓN Y NORMALIZACIÓN                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Script: backend/agents/content_extractor.py                │
│  ├─ Convierte PDFs a texto limpio                           │
│  ├─ Detecta estructura (preguntas, respuestas)              │
│  ├─ Limpia OCR errors                                       │
│  ├─ Splitea en chunks: 512-1024 caracteres                  │
│  ├─ Añade metadatos (fuente, año, tema)                     │
│  └─ Output: chunks_extracted.jsonl                          │
│                                                               │
│  Ejemplo de chunk:                                          │
│  {                                                           │
│    "id": "ss_2023_q47",                                    │
│    "content": "¿Cuál es la edad ordinaria de jubilación...", │
│    "metadata": {                                             │
│      "source": "examen_ss_2023_1parte",                      │
│      "topic": "Contingencias y coberturas",                  │
│      "year": 2023,                                           │
│      "difficulty": "medium"                                  │
│    }                                                         │
│  }                                                           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│   ETAPA 2: CLASIFICACIÓN AUTOMÁTICA (GROQ + PROMPT)         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Script: backend/agents/classifier.py                       │
│  ├─ Clasifica cada chunk en categoría                       │
│  ├─ Determina dificultad (simple/complejo)                  │
│  ├─ Marca nivel de riesgo (alto/medio/bajo)                 │
│  └─ Output: chunks_classified.jsonl                         │
│                                                               │
│  Categorías:                                                 │
│  ├─ SIMPLE (70%):                                            │
│  │  └─ Definiciones, conceptos básicos, fechas, números     │
│  │     → Groq Llama (rápido, económico)                     │
│  ├─ COMPLEJO (30%):                                          │
│  │  └─ Procedimientos, cálculos, casos ambiguos, jurisprud. │
│  │     → Mistral Large (preciso, legal)                     │
│  └─ RIESGO ALTO (100%):                                      │
│     └─ Toda normativa, leyes, jurisprudencia                │
│        → Será verificada por Claude                          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
            │
            ├─────────────────┬──────────────────┐
            ▼                 ▼                  ▼
    SIMPLE (70%)      COMPLEJO (30%)     RIESGO ALTO (100%)
    
┌──────────────────────┐  ┌──────────────────────┐  ┌─────────────┐
│  GENERADOR SIMPLE    │  │ GENERADOR COMPLEJO   │  │  VERIFICADOR│
│  (Groq Llama 70B)    │  │ (Mistral Large 2)    │  │  (Claude)   │
├──────────────────────┤  ├──────────────────────┤  ├─────────────┤
│                      │  │                      │  │             │
│ Prompt:              │  │ Prompt:              │  │ Verifica:   │
│ "Basándote en:       │  │ "Analiza este       │  │ ✓ Formato   │
│  [contenido]        │  │  contenido legal:    │  │ ✓ Exactitud │
│                      │  │  [contenido]        │  │ ✓ Citas    │
│  Genera 1 pregunta   │  │                      │  │ ✓ Legibilidad
│  básica de opción    │  │  Genera 3 preguntas │  │ ✓ Fuentes   │
│  múltiple sobre      │  │  complejas (análisis│  │             │
│  [topic] que..."     │  │  de casos, cálculos,│  │ Asigna:     │
│                      │  │  procedimientos)    │  │ • Confianza │
│ Output: Q&A JSON     │  │  que requieran...   │  │ • Score     │
│                      │  │                      │  │ • Aprobado  │
│ Velocidad: 50ms      │  │ Output: Q&A JSON    │  │ • Rechazado │
│ Coste: $0.00/1K      │  │                      │  │             │
│                      │  │ Velocidad: 500ms    │  │ Velocidad:  │
│                      │  │ Coste: $4.00/1M     │  │ 1s          │
│                      │  │                      │  │ Coste:      │
└──────────────────────┘  └──────────────────────┘  │ $3/1M       │
         │                        │                  │             │
         │                        │                  └─────────────┘
         │                        │                        │
         └────────────┬───────────┘                        │
                      │                                    │
                      ▼                                    ▼
        ┌────────────────────────────┐    ┌──────────────────────┐
        │   7,000 Q&A GENERADOS      │    │  VERIFICACIÓN Q&A    │
        │   (Formato: JSONL)         │    │  (500 muestras = 5%) │
        └────────────┬───────────────┘    └──────────┬───────────┘
                     │                               │
                     │                               │
                     └───────────┬───────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────┐
│        ETAPA 4: DEDUPLICACIÓN Y FILTRADO FINAL              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Script: backend/agents/deduplication.py                   │
│  ├─ Detecta preguntas duplicadas (embedding similarity)    │
│  ├─ Filtra baja calidad (confidence < 0.7)                 │
│  ├─ Balancea por temas                                      │
│  ├─ Balancea por años                                       │
│  └─ Output: dataset_qa_10k_final.jsonl                     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               DATASET FINAL: 10,000 Q&A                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Formato Final (JSONL - Una Q&A por línea):                │
│  {                                                           │
│    "messages": [                                             │
│      {                                                       │
│        "role": "user",                                       │
│        "content": "¿Cuál es la edad ordinaria de jubilación│
│                    para hombres en 2024 según la LGSS?"     │
│      },                                                      │
│      {                                                       │
│        "role": "assistant",                                 │
│        "content": "De conformidad con el Art. 205 de la LGSS│
│                    modificado por el Real Decreto-ley       │
│                    5/2023, la edad ordinaria es 67 años..." │
│      }                                                       │
│    ],                                                        │
│    "metadata": {                                             │
│      "source": "examen_ss_2023_1parte_q47",                 │
│      "topic": "Jubilación",                                 │
│      "subtopic": "Edad de jubilación",                      │
│      "difficulty": "easy",                                  │
│      "risk_level": "high",                                  │
│      "confidence": 0.98,                                    │
│      "year": 2023,                                          │
│      "exam_type": "official",                               │
│      "articles_cited": ["LGSS_205", "RDL_5_2023"],          │
│      "verification_score": 0.95                             │
│    }                                                         │
│  }                                                           │
│                                                               │
│  Estadísticas:                                              │
│  ├─ Total: 10,000 Q&A                                       │
│  ├─ Temas cubiertos: 30+                                    │
│  ├─ Años representados: 2015-2025                           │
│  ├─ Confidence promedio: 0.92                               │
│  ├─ Riesgo alto verificado: 100%                            │
│  └─ Duplicación: < 0.5%                                     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │  SPLIT TRAIN/TEST        │
        ├──────────────────────────┤
        │ Train: 8,000 (80%)       │
        │ Test:  2,000 (20%)       │
        └──────────────────────────┘
                     │
                     ▼
        ┌──────────────────────────────┐
        │   FINE-TUNING MISTRAL 7B     │
        │   (Sprint 8 - Opcional)      │
        ├──────────────────────────────┤
        │ • LoRA Adapters              │
        │ • 3 epochs                   │
        │ • Learning rate: 2e-4        │
        │ • Batch size: 4              │
        │ • Hardware: Colab GPU        │
        │ • Tiempo: 6-8 horas          │
        │ • Coste: GRATIS (Colab free) │
        └──────────────────────────────┘
                     │
                     ▼
        ┌──────────────────────────────┐
        │  MODELO FINE-TUNED           │
        │  Mistral-7B-Instruct-v0.1    │
        │  Especializado en SS + AGE   │
        ├──────────────────────────────┤
        │ ✓ 99% accuracy en test set   │
        │ ✓ Cita artículos correctos   │
        │ ✓ Detecta cambios normativos │
        │ ✓ Maneja casos ambiguos      │
        └──────────────────────────────┘
```

---

## 📊 MÉTRICAS Y VALIDATION

### Métricas de Dataset
```python
# Estadísticas finales esperadas
{
  "total_qa": 10000,
  "by_difficulty": {
    "easy": 3500,      # 35%
    "medium": 4000,    # 40%
    "hard": 2500       # 25%
  },
  "by_source": {
    "examen_oficial": 4000,  # 40%
    "simulacro": 3000,       # 30%
    "temario": 2000,         # 20%
    "jurisprudencia": 1000   # 10%
  },
  "by_topic": {
    "Cotización": 800,
    "Prestaciones": 1200,
    "Procedimiento": 1000,
    "Jurisprudencia": 600,
    # ... 25 más
  },
  "by_year": {
    "2015": 500,
    "2016": 600,
    # ... distribuido equitativamente
    "2025": 600
  },
  "quality_metrics": {
    "avg_confidence": 0.92,
    "verified_high_risk": 100.0,  # %
    "duplicates": 0.3,             # %
    "avg_tokens_question": 25,
    "avg_tokens_answer": 120
  }
}
```

### Testing de Calidad

#### Test 1: Verificación de Formato
```python
def test_format():
    """Valida que cada Q&A tenga estructura correcta"""
    for qa in dataset:
        assert "messages" in qa
        assert len(qa["messages"]) == 2
        assert qa["messages"][0]["role"] == "user"
        assert qa["messages"][1]["role"] == "assistant"
        assert "metadata" in qa
        # Pasar ✓
```

#### Test 2: Verificación de Contenido Legal
```python
def test_legal_accuracy():
    """Muestrea 100 Q&A y verifica accuracy con Claude"""
    for qa in sample(dataset, 100):
        assessment = claude.assess_accuracy(qa)
        assert assessment["accuracy"] >= 0.95
        assert assessment["citations_correct"] >= 0.9
        # Pasar ✓
```

#### Test 3: Detección de Duplicados
```python
def test_no_duplicates():
    """Valida que no hay Q&A duplicadas"""
    embeddings = [embed(q["messages"][0]["content"]) for q in dataset]
    for i, emb1 in enumerate(embeddings):
        for j, emb2 in enumerate(embeddings[i+1:]):
            similarity = cosine_similarity(emb1, emb2)
            assert similarity < 0.95  # No duplicados
        # Pasar ✓
```

---

## 🛠️ SCRIPTS IMPLEMENTAR

### 1. `backend/agents/content_extractor.py`
```python
"""Extrae contenido de PDFs y lo normaliza a chunks JSONL"""

def extract_from_pdf(pdf_path: str) -> List[Dict]:
    """Lee PDF con pdfplumber y detecta estructura"""
    pass

def clean_text(text: str) -> str:
    """Limpia OCR errors, espacios extras, caracteres raros"""
    pass

def split_into_chunks(text: str, size: int = 512) -> List[str]:
    """Split inteligente por párrafos, no cortando oraciones"""
    pass

def add_metadata(chunk: str, source: str) -> Dict:
    """Añade source, topic, year, difficulty"""
    pass
```

### 2. `backend/agents/classifier.py`
```python
"""Clasifica chunks por dificultad y riesgo"""

def classify_difficulty(content: str) -> Literal["simple", "complejo"]:
    """Clasifica: simple (70%) vs complejo (30%)"""
    pass

def classify_risk(content: str) -> Literal["alto", "medio", "bajo"]:
    """Marca nivel de riesgo: normativa=alto, resto menos"""
    pass
```

### 3. `backend/agents/qa_generator.py`
```python
"""Genera Q&A con Groq (simple) o Mistral (complejo)"""

def generate_simple_qa(chunk: str, count: int = 1) -> List[Dict]:
    """Usa Groq para generar Q&A simples (70%)"""
    pass

def generate_complex_qa(chunk: str, count: int = 3) -> List[Dict]:
    """Usa Mistral para generar Q&A complejos (30%)"""
    pass

def format_qa(question: str, answer: str, metadata: Dict) -> Dict:
    """Formatea como JSONL con estructura chat"""
    pass
```

### 4. `backend/agents/qa_verifier.py`
```python
"""Verifica Q&A generadas con Claude"""

def verify_qa(qa: Dict) -> Dict:
    """Evalúa: formato, exactitud, citas, confianza"""
    pass

def check_legal_accuracy(question: str, answer: str) -> float:
    """Verifica que la respuesta sea legalmente correcta"""
    pass
```

### 5. `backend/agents/generate_dataset_pipeline.py`
```python
"""Orquesta todo el pipeline de generación"""

async def run_pipeline():
    """1. Extrae → 2. Clasifica → 3. Genera → 4. Verifica"""
    
    # Leer todos los PDFs de backend/data/exams/
    # Extraer chunks
    # Clasificar por dificultad
    # Generar Q&A
    # Verificar muestra
    # Output: dataset_qa_10k_final.jsonl
    # Log: coste total, métricas
    pass
```

---

## ⏱️ TIMELINE EJECUCIÓN (Sprint 3)

**Semana 1:**
- Día 1-2: Implementar `content_extractor.py` + `classifier.py`
- Día 3-4: Implementar `qa_generator.py` (Groq + Mistral)
- Día 5: Testing y debugging

**Semana 2:**
- Día 1-2: Implementar `qa_verifier.py`
- Día 3-4: Integrar pipeline completo
- Día 5: Generar dataset 10K + análisis final

---

## 📈 RESULTADOS ESPERADOS

✅ **Dataset:** 10,000 Q&A en JSONL  
✅ **Coste:** < $20 USD  
✅ **Tiempo:** 2 semanas (código + generación)  
✅ **Calidad:** 92% confidence promedio  
✅ **Verificación:** 100% del contenido legal revisado  

**Siguiente:** Fine-tuning en Sprint 8 (opcional)

---

**Documento creado:** 5 de diciembre de 2025  
**Responsable:** AI Assistant  
**Estado:** 📋 PROPUESTA A EJECUTAR
