# 🤖 Arquitectura Multi-Agente para OpositAIA

**Fecha**: 2024-11-16  
**Estado**: Diseño Completo  
**Prioridad**: CRÍTICA

---

## 🎯 Problema Actual

1. **RAG desconectado**: FastAPI endpoint no funcional, Gemini no tiene acceso al RAG
2. **Sin arquitectura de agentes**: Falta orquestador + subagentes especializados
3. **Sin contexto del usuario**: Historial, progreso, debilidades, casos creados → inaccesible para la IA
4. **Sin personalización**: La IA no puede sugerir "fallas mucho en incapacidad temporal, repasa tema 3 y 22"

---

## 🏗️ Arquitectura Propuesta

```
┌─────────────────────────────────────────────────────────────┐
│              ORQUESTADOR PRINCIPAL (Gemini 2.0)             │
│  - Decide qué agente usar según la consulta del usuario     │
│  - Mantiene contexto conversacional                         │
│  - Coordina respuestas de múltiples agentes                 │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│   AGENTE RAG     │ │ AGENTE ANÁLISIS  │ │  AGENTE QUIZ     │
│   (Búsqueda)     │ │   (Progreso)     │ │  (Evaluación)    │
└──────────────────┘ └──────────────────┘ └──────────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Qdrant Vector DB │ │ PostgreSQL       │ │ Gemini Flash     │
│ + Embeddings     │ │ (User Progress)  │ │ (Generación)     │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## 🧠 Modelos Pre-entrenados GRATIS (Open Source)

### 1. **Embeddings: littlejohn-ai/bge-m3-spa-law-qa** ⭐ RECOMENDADO

**Características**:
- ✅ **Especializado en legislación española** (BOE)
- ✅ **1024 dimensiones** (alta precisión)
- ✅ **8192 tokens max** (documentos largos)
- ✅ **62.5% accuracy@1** en legal español
- ✅ **83% accuracy@10** 
- ✅ **Gratis y open source** (Apache 2.0)
- ✅ **Compatible con Ollama/HuggingFace**

**Métricas**:
```
cosine_accuracy@1:  62.5%
cosine_accuracy@3:  74.5%
cosine_accuracy@10: 83.1%
cosine_ndcg@10:     72.8%
cosine_mrr@10:      69.5%
```

**Instalación**:
```bash
# Opción 1: HuggingFace (Python)
pip install sentence-transformers
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("littlejohn-ai/bge-m3-spa-law-qa")

# Opción 2: Ollama (más fácil)
ollama pull bge-m3
```

**Tamaño**: ~600 MB  
**Uso**: Embeddings para RAG (búsqueda semántica en BOE)

---

### 2. **Embeddings Alternativo: wilfredomartel/embeddinggemma-300m-legal-spanish-100k**

**Características**:
- ✅ **Especializado en legal español** (100k ejemplos)
- ✅ **768 dimensiones** (más ligero)
- ✅ **2048 tokens max**
- ✅ **45.5% accuracy@1** (menor que bge-m3)
- ✅ **99.4% accuracy@10** (excelente recall)
- ✅ **Gratis y open source**

**Métricas**:
```
cosine_accuracy@1:  45.5%
cosine_accuracy@10: 99.4%
cosine_ndcg@10:     78.8%
cosine_mrr@10:      71.6%
```

**Tamaño**: ~300 MB (más ligero)  
**Uso**: Alternativa si bge-m3 es muy pesado

---

### 3. **LLM Legal: Narrativa/legal-longformer-base-4096-spanish**

**Características**:
- ✅ **Entrenado en corpus legal español** (Plan Nacional de Tecnologías del Lenguaje)
- ✅ **4096 tokens de contexto** (documentos largos)
- ✅ **Basado en RoBERTa** (arquitectura probada)
- ✅ **Gratis y open source**
- ✅ **Compatible con HuggingFace Transformers**

**Uso**: 
- Clasificación de textos legales
- Extracción de entidades (NER)
- Question Answering sobre legislación

**Instalación**:
```python
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("Narrativa/legal-longformer-base-4096-spanish")
model = AutoModel.from_pretrained("Narrativa/legal-longformer-base-4096-spanish")
```

**Tamaño**: ~500 MB

---

### 4. **LLM Legal Grande: joelniklaus/legal-spanish-roberta-large**

**Características**:
- ✅ **300M parámetros** (más potente)
- ✅ **Entrenado en MultiLegalPile** (689GB corpus legal multilingüe)
- ✅ **Incluye español**
- ✅ **Gratis y open source**

**Tamaño**: ~1.2 GB  
**Uso**: Tareas complejas de NLP legal

---

## 🔧 Fine-tuning GRATIS con Unsloth + Google Colab

### ✅ Ventajas de Unsloth

- **2x más rápido** que métodos tradicionales
- **70% menos VRAM** (cabe en GPU gratis de Colab)
- **Gratis con Google Colab** (Tesla T4 GPU)
- **Compatible con LoRA/QLoRA** (fine-tuning eficiente)
- **Soporta Gemma, Llama, Mistral, Qwen**

### 📋 Proceso de Fine-tuning (GRATIS)

1. **Abrir Google Colab** (GPU Tesla T4 gratis)
2. **Instalar Unsloth**:
   ```python
   !pip install unsloth
   ```
3. **Cargar modelo base** (ej: Gemma 2B, Llama 3.2 3B)
4. **Preparar dataset** (preguntas BOE + respuestas)
5. **Fine-tuning con LoRA** (5-15 minutos)
6. **Guardar en HuggingFace** o local

### 💰 Costo: $0 (100% GRATIS)

**Tiempo**: 10-30 minutos por experimento  
**GPU**: Tesla T4 (gratis en Colab)  
**Límite**: ~12 horas/día de GPU gratis

---

## 🗄️ Base de Datos de Usuario (PostgreSQL)

### Tablas Necesarias

```sql
-- Progreso del usuario
CREATE TABLE user_progress (
  user_id UUID PRIMARY KEY,
  temas_completados INTEGER[],
  temas_debiles INTEGER[],
  precision_global FLOAT,
  total_preguntas INTEGER,
  total_correctas INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Historial de respuestas
CREATE TABLE answer_history (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES user_progress(user_id),
  pregunta_id UUID,
  tema_id INTEGER,
  respuesta_usuario TEXT,
  respuesta_correcta TEXT,
  es_correcta BOOLEAN,
  tiempo_respuesta INTEGER, -- segundos
  created_at TIMESTAMP
);

-- Casos creados por el usuario
CREATE TABLE user_cases (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES user_progress(user_id),
  titulo TEXT,
  descripcion TEXT,
  tema_id INTEGER,
  solucion TEXT,
  created_at TIMESTAMP
);

-- Simulacros realizados
CREATE TABLE simulacros (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES user_progress(user_id),
  tipo TEXT, -- 'oficial', 'personalizado'
  puntuacion FLOAT,
  tiempo_total INTEGER,
  preguntas_correctas INTEGER,
  preguntas_totales INTEGER,
  temas_evaluados INTEGER[],
  created_at TIMESTAMP
);

-- Mapas mentales
CREATE TABLE mind_maps (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES user_progress(user_id),
  tema_id INTEGER,
  contenido JSONB, -- estructura del mapa
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

---

## 🤖 Agentes Especializados

### 1. **Agente RAG (Búsqueda BOE)**

**Responsabilidad**: Buscar información en documentos BOE

**Tecnologías**:
- **Embeddings**: `littlejohn-ai/bge-m3-spa-law-qa`
- **Vector DB**: Qdrant
- **LLM**: Gemini 2.0 Flash (gratis)

**Flujo**:
```
Usuario: "¿Qué dice el BOE sobre incapacidad temporal?"
   ↓
1. Generar embedding de la pregunta (bge-m3)
2. Buscar en Qdrant (top-k=5)
3. Reranking con contexto
4. Enviar a Gemini con contexto BOE
5. Respuesta fundamentada en legislación
```

**Endpoint**: `POST /api/rag/search`

---

### 2. **Agente de Análisis (Progreso del Usuario)**

**Responsabilidad**: Analizar debilidades y sugerir mejoras

**Tecnologías**:
- **DB**: PostgreSQL
- **LLM**: Gemini 2.0 Flash

**Flujo**:
```
Usuario: "¿En qué debo mejorar?"
   ↓
1. Consultar answer_history (últimas 100 respuestas)
2. Agrupar por tema_id
3. Calcular precisión por tema
4. Identificar temas <70% precisión
5. Generar recomendaciones personalizadas
```

**Ejemplo de respuesta**:
```
"Fallas mucho en:
- Tema 3 (Incapacidad Temporal): 45% precisión
- Tema 22 (Prestaciones): 58% precisión

Recomendaciones:
1. Repasa el BOE sobre IT (artículos 128-173)
2. Practica 20 preguntas del Tema 3
3. Crea un mapa mental de IT"
```

**Endpoint**: `GET /api/analysis/weaknesses`

---

### 3. **Agente de Quiz (Generación y Evaluación)**

**Responsabilidad**: Generar preguntas y evaluar respuestas

**Tecnologías**:
- **LLM**: Gemini 2.0 Flash
- **RAG**: Para contexto BOE
- **DB**: PostgreSQL (guardar historial)

**Flujo de Generación**:
```
Usuario: "Genera 10 preguntas del Tema 3"
   ↓
1. Consultar temas_debiles del usuario
2. Buscar en RAG contenido del Tema 3
3. Generar preguntas con Gemini
4. Validar que sean únicas (no repetidas)
5. Guardar en DB
```

**Flujo de Evaluación**:
```
Usuario responde pregunta
   ↓
1. Comparar con respuesta correcta
2. Analizar razonamiento (si es abierta)
3. Actualizar answer_history
4. Actualizar user_progress
5. Sugerir siguiente pregunta (adaptativa)
```

**Endpoint**: 
- `POST /api/quiz/generate`
- `POST /api/quiz/evaluate`

---

### 4. **Agente de Recomendaciones (Personalización)**

**Responsabilidad**: Sugerencias proactivas basadas en contexto

**Tecnologías**:
- **DB**: PostgreSQL
- **LLM**: Gemini 2.0 Flash

**Ejemplos de Recomendaciones**:
```
- "Llevas 3 días sin practicar Tema 5, ¿repasamos?"
- "Tu precisión en simulacros subió 15% esta semana 🎉"
- "Tema 12 es tu fuerte (92%), úsalo como base para Tema 13"
- "Crea un caso práctico de IT para consolidar conocimiento"
```

**Endpoint**: `GET /api/recommendations`

---

## 🔄 Orquestador Principal (Gemini 2.0)

### Responsabilidad

Decidir qué agente(s) usar según la consulta del usuario

### Lógica de Decisión

```python
def orquestador(user_query: str, user_context: dict):
    # Clasificar intención
    intencion = clasificar_intencion(user_query)
    
    if "buscar" in intencion or "qué dice" in intencion:
        # Usar Agente RAG
        return agente_rag.search(user_query)
    
    elif "mejorar" in intencion or "debilidades" in intencion:
        # Usar Agente de Análisis
        return agente_analisis.get_weaknesses(user_context['user_id'])
    
    elif "genera" in intencion or "pregunta" in intencion:
        # Usar Agente de Quiz
        return agente_quiz.generate(user_query, user_context)
    
    elif "recomendación" in intencion:
        # Usar Agente de Recomendaciones
        return agente_recomendaciones.get_suggestions(user_context['user_id'])
    
    else:
        # Conversación general (Gemini directo)
        return gemini_chat(user_query, user_context)
```

### Contexto Compartido

```typescript
interface UserContext {
  user_id: string;
  temas_completados: number[];
  temas_debiles: number[];
  precision_global: number;
  ultima_sesion: Date;
  historial_chat: Message[];
}
```

---

## 📊 Flujo Completo de Ejemplo

### Caso: Usuario pregunta sobre su progreso

```
Usuario: "¿Cómo voy en el estudio? ¿Qué me falta?"

1. Orquestador detecta: intención = "análisis de progreso"
2. Llama a Agente de Análisis
3. Agente consulta PostgreSQL:
   - user_progress
   - answer_history (últimas 200 respuestas)
   - simulacros (últimos 5)
4. Agente calcula:
   - Precisión por tema
   - Temas débiles (<70%)
   - Tendencia (mejorando/empeorando)
5. Agente llama a Agente RAG para obtener recursos BOE
6. Gemini genera respuesta personalizada:

"📊 Tu Progreso:
- Precisión global: 78% (+5% vs semana pasada) 🎉
- Temas dominados: 5, 8, 12, 15 (>85%)
- Temas débiles: 3, 22 (<70%)

🎯 Recomendaciones:
1. Tema 3 (IT): 45% precisión
   → Repasa BOE artículos 128-173
   → Practica 20 preguntas
   
2. Tema 22 (Prestaciones): 58% precisión
   → Crea mapa mental
   → Resuelve 3 casos prácticos

📚 Recursos:
- [BOE IT] Real Decreto 625/2014
- [Casos prácticos] 10 ejemplos de IT

¿Empezamos con Tema 3?"
```

---

## 🚀 Plan de Implementación (Fases)

### Fase 1: Infraestructura Base (1-2 semanas)

- [ ] Configurar PostgreSQL (user_progress, answer_history)
- [ ] Instalar Qdrant Vector DB
- [ ] Instalar embeddings `bge-m3-spa-law-qa`
- [ ] Crear FastAPI endpoints básicos
- [ ] Conectar Gemini 2.0 Flash

### Fase 2: Agente RAG (1 semana)

- [ ] Indexar documentos BOE en Qdrant
- [ ] Implementar búsqueda semántica
- [ ] Integrar con Gemini para respuestas
- [ ] Testing con 100 preguntas BOE

### Fase 3: Agente de Análisis (1 semana)

- [ ] Implementar cálculo de precisión por tema
- [ ] Detectar temas débiles
- [ ] Generar recomendaciones personalizadas
- [ ] Dashboard de progreso (frontend)

### Fase 4: Agente de Quiz (1 semana)

- [ ] Generación de preguntas con Gemini
- [ ] Evaluación de respuestas
- [ ] Sistema adaptativo (dificultad dinámica)
- [ ] Guardar historial en DB

### Fase 5: Orquestador (1 semana)

- [ ] Clasificación de intenciones
- [ ] Routing a agentes correctos
- [ ] Manejo de contexto compartido
- [ ] Testing end-to-end

### Fase 6: Fine-tuning (Opcional, 1 semana)

- [ ] Crear dataset de 1000+ ejemplos BOE
- [ ] Fine-tuning con Unsloth (Google Colab)
- [ ] Evaluar mejora vs modelo base
- [ ] Desplegar modelo fine-tuned

---

## 💰 Costos Estimados

### Opción 1: Sin Fine-tuning (MVP)

| Componente | Costo |
|------------|-------|
| Gemini 2.0 Flash | $0 (1M tokens/día gratis) |
| Embeddings (bge-m3) | $0 (local/Ollama) |
| Qdrant | $0 (self-hosted) |
| PostgreSQL | $0 (self-hosted) |
| **TOTAL** | **$0/mes** |

### Opción 2: Con Fine-tuning

| Componente | Costo |
|------------|-------|
| Fine-tuning (Unsloth + Colab) | $0 (GPU gratis) |
| Hosting modelo fine-tuned | $0 (HuggingFace gratis) |
| Resto igual | $0 |
| **TOTAL** | **$0/mes** |

---

## 🎯 Métricas de Éxito

### KPIs Técnicos

- **Precisión RAG**: >80% en respuestas BOE
- **Latencia**: <2s por consulta
- **Uptime**: >99%

### KPIs de Usuario

- **Precisión del usuario**: Mejora >15% en 1 mes
- **Engagement**: >3 sesiones/semana
- **Satisfacción**: >4.5/5 estrellas

---

## 🔐 Seguridad y Privacidad

- **Datos del usuario**: Encriptados en PostgreSQL
- **API Keys**: Variables de entorno (.env)
- **Autenticación**: JWT tokens
- **GDPR**: Derecho al olvido (borrar datos)

---

## 📚 Recursos y Referencias

### Modelos Pre-entrenados

- [bge-m3-spa-law-qa](https://huggingface.co/littlejohn-ai/bge-m3-spa-law-qa)
- [embeddinggemma-legal-spanish](https://huggingface.co/wilfredomartel/embeddinggemma-300m-legal-spanish-100k)
- [legal-longformer-spanish](https://huggingface.co/Narrativa/legal-longformer-base-4096-spanish)
- [legal-spanish-roberta-large](https://huggingface.co/joelniklaus/legal-spanish-roberta-large)

### Fine-tuning

- [Unsloth GitHub](https://github.com/unslothai/unsloth)
- [Unsloth Colab Notebooks](https://github.com/unslothai/unsloth#-colab-notebooks)
- [Google Colab](https://colab.research.google.com/)

### Documentación

- [Gemini API](https://ai.google.dev/gemini-api/docs)
- [Qdrant](https://qdrant.tech/documentation/)
- [Sentence Transformers](https://www.sbert.net/)

---

## ✅ Próximos Pasos Inmediatos

1. **Instalar `bge-m3-spa-law-qa`** en Ollama o HuggingFace
2. **Configurar PostgreSQL** con tablas de usuario
3. **Crear FastAPI endpoint** para RAG
4. **Indexar 100 documentos BOE** en Qdrant (prueba)
5. **Conectar Gemini** al RAG
6. **Testing**: 10 preguntas BOE → medir precisión

---

**Decisión**: Empezar con modelos pre-entrenados (bge-m3), NO hacer fine-tuning hasta tener 1000+ ejemplos etiquetados y medir precisión baseline.

**Fine-tuning**: Solo si precisión <80% después de optimizaciones (chunking, prompts, reranking).

**Herramienta de fine-tuning**: Unsloth + Google Colab (100% GRATIS).
