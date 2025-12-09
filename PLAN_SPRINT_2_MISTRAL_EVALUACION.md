# 🎯 PLAN COMPLETAR SPRINT 2 + EVALUACIÓN MISTRAL SMALL 24B

**Fecha:** 5 de diciembre de 2025  
**Objetivo:** Completar indexación RAG + Evaluar modelo Mistral Small + Implementar caché  
**Duración estimada:** 3-4 horas

---

## 📊 Análisis Mistral-Small-24B-Instruct-2501

### ✅ Información del Modelo

**Características principales:**
- **Parámetros:** 24B (24 mil millones)
- **Licencia:** Apache 2.0 ✅ **OPEN SOURCE y GRATIS**
- **Context window:** 32K tokens
- **Idiomas:** Español nativo incluido (10 idiomas)
- **Tokenizer:** Tekken 131K vocab

### 💾 Requisitos de Hardware

**VRAM/RAM necesarios:**

| Configuración | VRAM/RAM | Uso |
|---------------|----------|-----|
| **FP16/BF16** | ~55-60 GB | Producción (precisión completa) |
| **Q8 (8-bit)** | ~30-32 GB | Buena calidad, RAM factible |
| **Q4 (4-bit)** | ~15-16 GB | ✅ **FACTIBLE en tu laptop 16GB** |
| **Ollama Q4_K_M** | ~14 GB | ✅ **RECOMENDADO para local** |

**Tu hardware:**
- 16GB RAM laptop ✅
- CPU inference (sin GPU dedicada)
- Ollama instalado ✅

### 🎯 ¿Para qué es bueno?

**Fortalezas documentadas:**

1. **Reasoning & Knowledge** (Razonamiento legal perfecto):
   - MMLU Pro: 66.3% (supera GPT-4o mini)
   - GPQA: 45.3% (razonamiento complejo)

2. **Math & Coding** (Casos prácticos con cálculos):
   - HumanEval: 84.8%
   - Math: 70.6%

3. **Instruction Following** (Seguir formato legal):
   - IFEval: 82.9%
   - Arena Hard: 87.3%

4. **Agentic capabilities** (Function calling para RAG):
   - Native function calling
   - JSON output nativo

### 💡 Casos de uso en OpositaIA

#### ✅ IDEAL PARA:

1. **Generación de respuestas finales RAG** (Tu pregunta principal)
   - Recibe contexto de Qdrant → genera respuesta fundamentada
   - 32K context permite meter muchos artículos LGSS
   - Multilingüe (responde en español legal formal)

2. **Evaluación de calidad de dataset Q&A**
   - Puede revisar pares pregunta-respuesta generados
   - Detectar inconsistencias en dataset fine-tuning
   - Verificar referencias legales correctas

3. **Fine-tuning base** (Futuro Sprint 5-8)
   - Más pequeño que 70B, más factible fine-tune
   - Apache 2.0 permite comercialización
   - Unsloth compatible

#### ❌ NO ÓPTIMO PARA:

1. **Embeddings** (ya tenemos pablosi/bge-m3 especializado)
2. **Generación dataset inicial** (mejor Groq gratis + rápido)
3. **Ejecución tiempo real frontend** (demasiado grande)

### 🚀 Recomendación de uso

**ESTRATEGIA PROPUESTA:**

```
RAG Pipeline Optimizado:
┌─────────────────────────────────────────────────┐
│ 1. Usuario hace pregunta                        │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 2. pablosi/bge-m3 → embedding pregunta          │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 3. Qdrant → recupera top-10 artículos LGSS     │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 4. Mistral Small 24B (Ollama Q4)                │
│    - Input: pregunta + 10 artículos             │
│    - Output: respuesta legal fundamentada       │
│    - Tiempo: ~5-10 seg (CPU i7)                 │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 5. Cache Redis (30 días TTL)                    │
│    - Preguntas repetidas → 0 seg                │
└─────────────────────────────────────────────────┘
```

**Costos:**
- Embeddings: Local (0€)
- Qdrant: Local Docker (0€)
- Mistral Small: Ollama local (0€) ✅
- Cache: Upstash free tier (0€)

**TOTAL: 0€/mes** 🎉

---

## 📋 PLAN EJECUCIÓN SPRINT 2 COMPLETADO

### Tarea 1: Instalar Mistral Small en Ollama (10 min)

```bash
# Instalar Ollama si no está
# Windows: https://ollama.com/download

# Descargar modelo (14GB, ~20 min primera vez)
ollama pull mistral-small:24b-instruct-2501-q4_K_M

# Verificar
ollama list
```

**Resultado esperado:**
```
NAME                               SIZE
mistral-small:24b-instruct-2501-q4_K_M  14GB
```

---

### Tarea 2: Re-indexar LGSS con modelo pablosi (25 min)

```bash
cd /mnt/e/1/OPOS_GEMINI_1/backend
source venv/bin/activate

# Eliminar colección antigua
python -c "from qdrant_client import QdrantClient; client = QdrantClient('http://localhost:6333'); client.delete_collection('opositaia_lgss_test'); print('✅ Colección eliminada')"

# Indexar 567 bloques LGSS con pablosi
python agents/index_lgss_boe_api.py
```

**Progreso esperado:**
```
🔄 Descargando modelo pablosi/bge-m3-spa-law-qa-trained-2...
✅ Modelo cargado (1024 dims)
📦 Indexando 567 bloques...
  [1/567] Artículo 1. Objeto... → ✅
  [2/567] Artículo 2. Campo de aplicación... → ✅
  ...
  [567/567] Disposición final... → ✅
⏱️ Tiempo total: ~20-25 minutos
✅ 567 bloques LGSS indexados
```

---

### Tarea 3: Cargar datasets Q&A existentes (5 min)

**Datasets encontrados:**

1. **`test_dataset.jsonl`** (2 preguntas básicas):
   - TEST_001: Edad jubilación art. 205
   - TEST_002: Base reguladora

2. **`dataset_generator/example_dataset.jsonl`** (3 preguntas):
   - qa_00001: Edad jubilación 2024 (medium)
   - qa_00002: Base reguladora (easy)
   - qa_00003: Jubilación anticipada caso práctico (hard)

**Script para cargar:**

```python
# backend/scripts/load_test_questions.py
import json
from pathlib import Path

def load_test_questions():
    """Carga preguntas de test para evaluar RAG"""
    
    datasets = [
        "test_dataset.jsonl",
        "dataset_generator/example_dataset.jsonl"
    ]
    
    questions = []
    for dataset_file in datasets:
        file_path = Path(__file__).parent.parent / dataset_file
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    questions.append({
                        'id': data.get('id'),
                        'pregunta': data.get('pregunta') or data.get('question'),
                        'respuesta_esperada': data.get('respuesta') or data.get('answer'),
                        'difficulty': data.get('difficulty_level', 'unknown'),
                        'risk_level': data.get('risk_level', 'unknown'),
                        'fuentes': data.get('fuentes', []),
                        'dataset': dataset_file
                    })
    
    return questions

if __name__ == "__main__":
    questions = load_test_questions()
    print(f"✅ Cargadas {len(questions)} preguntas de test")
    for q in questions:
        print(f"  - [{q['difficulty']}] {q['pregunta'][:60]}...")
```

---

### Tarea 4: Crear script evaluación RAG + Mistral (30 min)

```python
# backend/scripts/evaluate_rag_mistral.py

"""
Evalúa calidad del RAG usando:
1. Qdrant (búsqueda semántica con pablosi embeddings)
2. Mistral Small 24B (generación respuesta)
3. Comparación con respuesta esperada del dataset
"""

import json
import time
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import ollama
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.load_test_questions import load_test_questions

# Configuración
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_lgss_test"
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
LLM_MODEL = "mistral-small:24b-instruct-2501-q4_K_M"
TOP_K = 5  # Top 5 artículos más relevantes

def init_rag():
    """Inicializa componentes RAG"""
    print("🔄 Inicializando RAG...")
    
    # Embedding model
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    print(f"  ✅ Modelo embeddings: {EMBEDDING_MODEL}")
    
    # Qdrant client
    qdrant = QdrantClient(url=QDRANT_URL)
    collections = qdrant.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        raise ValueError(f"❌ Colección {COLLECTION_NAME} no existe. Ejecuta index_lgss_boe_api.py primero")
    print(f"  ✅ Qdrant conectado: {COLLECTION_NAME}")
    
    # Verificar Ollama
    try:
        models = ollama.list()
        if not any(LLM_MODEL in m['name'] for m in models['models']):
            raise ValueError(f"❌ Modelo {LLM_MODEL} no encontrado. Ejecuta: ollama pull mistral-small")
        print(f"  ✅ Ollama modelo: {LLM_MODEL}")
    except Exception as e:
        raise ValueError(f"❌ Ollama no disponible: {e}")
    
    return embedder, qdrant


def search_qdrant(pregunta: str, embedder, qdrant, top_k: int = TOP_K):
    """Busca artículos relevantes en Qdrant"""
    
    # Generar embedding de la pregunta
    query_vector = embedder.encode(pregunta).tolist()
    
    # Buscar en Qdrant
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        score_threshold=0.3  # Filtrar resultados poco relevantes
    )
    
    # Extraer contexto
    contexto = []
    for hit in results:
        contexto.append({
            'titulo': hit.payload.get('titulo', ''),
            'texto': hit.payload.get('texto', ''),
            'score': hit.score,
            'id_bloque': hit.payload.get('id_bloque', '')
        })
    
    return contexto


def generate_response_mistral(pregunta: str, contexto: list):
    """Genera respuesta con Mistral Small usando contexto RAG"""
    
    # Construir prompt
    contexto_str = "\n\n".join([
        f"**{c['titulo']}** (relevancia: {c['score']:.3f})\n{c['texto']}"
        for c in contexto
    ])
    
    system_prompt = """Eres un experto en legislación de Seguridad Social española.
Tu tarea es responder preguntas de oposiciones basándote ÚNICAMENTE en los artículos de ley proporcionados.

REGLAS:
1. Solo usa información de los artículos proporcionados
2. Cita el artículo específico (ej: "según el art. 205.1.a) LGSS...")
3. Si la información no está en el contexto, di "No encuentro información suficiente en los artículos proporcionados"
4. Responde de forma clara, precisa y formal
5. Si hay cálculos, muéstralos paso a paso"""

    user_prompt = f"""**PREGUNTA:**
{pregunta}

**ARTÍCULOS DE LEY RELEVANTES:**

{contexto_str}

**RESPUESTA:**"""

    # Llamar a Mistral via Ollama
    start_time = time.time()
    
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        options={
            'temperature': 0.15,  # Bajo para respuestas consistentes
            'top_p': 0.9,
            'top_k': 40
        }
    )
    
    elapsed = time.time() - start_time
    
    return {
        'respuesta': response['message']['content'],
        'tiempo_generacion': elapsed,
        'tokens_generados': response.get('eval_count', 0)
    }


def evaluate_quality(respuesta_rag: str, respuesta_esperada: str):
    """Evalúa similitud entre respuesta RAG y esperada (métrica simple)"""
    
    # Métricas básicas
    palabras_rag = set(respuesta_rag.lower().split())
    palabras_esperada = set(respuesta_esperada.lower().split())
    
    interseccion = palabras_rag & palabras_esperada
    union = palabras_rag | palabras_esperada
    
    jaccard_similarity = len(interseccion) / len(union) if union else 0
    
    # Detectar citas de artículos
    tiene_cita_articulo = any(keyword in respuesta_rag.lower() 
                              for keyword in ['art.', 'artículo', 'lgss', 'según'])
    
    return {
        'jaccard_similarity': jaccard_similarity,
        'tiene_cita_articulo': tiene_cita_articulo,
        'palabras_comunes': len(interseccion),
        'longitud_respuesta': len(respuesta_rag.split())
    }


def run_evaluation():
    """Ejecuta evaluación completa"""
    
    print("\n" + "="*70)
    print("🧪 EVALUACIÓN RAG + MISTRAL SMALL 24B")
    print("="*70 + "\n")
    
    # Inicializar
    embedder, qdrant = init_rag()
    
    # Cargar preguntas
    questions = load_test_questions()
    print(f"\n📚 Preguntas de test cargadas: {len(questions)}\n")
    
    # Evaluar cada pregunta
    results = []
    
    for i, q in enumerate(questions, 1):
        print(f"\n{'─'*70}")
        print(f"📝 PREGUNTA {i}/{len(questions)}")
        print(f"{'─'*70}")
        print(f"ID: {q['id']}")
        print(f"Dificultad: {q['difficulty']}")
        print(f"Pregunta: {q['pregunta']}")
        print(f"\n🔍 Buscando en Qdrant...")
        
        # Paso 1: Búsqueda RAG
        contexto = search_qdrant(q['pregunta'], embedder, qdrant)
        print(f"  ✅ Encontrados {len(contexto)} artículos relevantes")
        for c in contexto[:3]:
            print(f"    - {c['titulo'][:50]}... (score: {c['score']:.3f})")
        
        # Paso 2: Generación con Mistral
        print(f"\n🤖 Generando respuesta con Mistral Small...")
        mistral_output = generate_response_mistral(q['pregunta'], contexto)
        
        print(f"  ✅ Respuesta generada ({mistral_output['tiempo_generacion']:.1f}s)")
        print(f"\n📄 RESPUESTA MISTRAL:")
        print(f"{mistral_output['respuesta']}\n")
        
        print(f"📄 RESPUESTA ESPERADA:")
        print(f"{q['respuesta_esperada']}\n")
        
        # Paso 3: Evaluar calidad
        quality = evaluate_quality(mistral_output['respuesta'], q['respuesta_esperada'])
        
        print(f"📊 MÉTRICAS:")
        print(f"  - Similitud Jaccard: {quality['jaccard_similarity']:.2%}")
        print(f"  - Tiene cita artículo: {'✅' if quality['tiene_cita_articulo'] else '❌'}")
        print(f"  - Palabras comunes: {quality['palabras_comunes']}")
        print(f"  - Longitud respuesta: {quality['longitud_respuesta']} palabras")
        print(f"  - Tiempo generación: {mistral_output['tiempo_generacion']:.1f}s")
        
        # Guardar resultado
        results.append({
            'pregunta_id': q['id'],
            'pregunta': q['pregunta'],
            'difficulty': q['difficulty'],
            'contexto_encontrado': len(contexto),
            'mejor_score_qdrant': contexto[0]['score'] if contexto else 0,
            'respuesta_mistral': mistral_output['respuesta'],
            'respuesta_esperada': q['respuesta_esperada'],
            'tiempo_generacion': mistral_output['tiempo_generacion'],
            'jaccard_similarity': quality['jaccard_similarity'],
            'tiene_cita_articulo': quality['tiene_cita_articulo']
        })
    
    # Resumen final
    print(f"\n{'='*70}")
    print("📊 RESUMEN EVALUACIÓN")
    print(f"{'='*70}\n")
    
    avg_similarity = sum(r['jaccard_similarity'] for r in results) / len(results)
    avg_time = sum(r['tiempo_generacion'] for r in results) / len(results)
    citas_correctas = sum(1 for r in results if r['tiene_cita_articulo'])
    
    print(f"Total preguntas evaluadas: {len(results)}")
    print(f"Similitud promedio: {avg_similarity:.2%}")
    print(f"Tiempo generación promedio: {avg_time:.1f}s")
    print(f"Respuestas con cita artículo: {citas_correctas}/{len(results)} ({citas_correctas/len(results):.1%})")
    
    # Guardar resultados
    output_file = Path(__file__).parent.parent / "evaluation_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'fecha_evaluacion': time.strftime('%Y-%m-%d %H:%M:%S'),
            'modelo_embeddings': EMBEDDING_MODEL,
            'modelo_llm': LLM_MODEL,
            'coleccion_qdrant': COLLECTION_NAME,
            'metricas_resumen': {
                'total_preguntas': len(results),
                'similitud_promedio': avg_similarity,
                'tiempo_promedio_seg': avg_time,
                'citas_articulo': citas_correctas
            },
            'resultados_detallados': results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    print("\n✅ Evaluación completada\n")


if __name__ == "__main__":
    run_evaluation()
```

---

### Tarea 5: Implementar caché Redis (30 min)

**Basado en `docs/Iideas_rama_gemini/GUIA_IMPLEMENTACION_CACHE_PASO_A_PASO.md`:**

```bash
# 1. Instalar Redis local (testing)
wsl sudo apt update
wsl sudo apt install redis-server -y
wsl sudo service redis-server start

# 2. Instalar dependencias Python
cd backend
source venv/bin/activate
pip install redis hiredis
```

**Crear `backend/services/cache_service.py`:**

```python
import redis
import hashlib
import json
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.ttl = int(os.getenv('CACHE_TTL_SECONDS', 2592000))  # 30 días
        self.key_prefix = 'opositaia:rag:'
        
        try:
            self.client = redis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.client.ping()
            logger.info("✅ Redis conectado")
        except Exception as e:
            logger.warning(f"⚠️ Redis no disponible: {e}. Cache deshabilitado.")
            self.client = None
    
    def _make_key(self, pregunta: str) -> str:
        """Genera key único para pregunta"""
        normalized = pregunta.lower().strip()
        hash_key = hashlib.md5(normalized.encode()).hexdigest()
        return f"{self.key_prefix}{hash_key}"
    
    def get(self, pregunta: str) -> Optional[dict]:
        """Obtiene respuesta cacheada"""
        if not self.client:
            return None
        
        try:
            key = self._make_key(pregunta)
            cached = self.client.get(key)
            if cached:
                logger.info(f"✅ CACHE HIT: {pregunta[:50]}...")
                return json.loads(cached)
        except Exception as e:
            logger.error(f"❌ Cache GET error: {e}")
        
        return None
    
    def set(self, pregunta: str, respuesta: dict):
        """Guarda respuesta en cache"""
        if not self.client:
            return
        
        try:
            key = self._make_key(pregunta)
            value = json.dumps(respuesta, ensure_ascii=False)
            self.client.setex(key, self.ttl, value)
            logger.info(f"💾 CACHED: {pregunta[:50]}... (TTL: 30 días)")
        except Exception as e:
            logger.error(f"❌ Cache SET error: {e}")

# Singleton
cache = RedisCache()
```

**Integrar en script evaluación:**

```python
# En evaluate_rag_mistral.py, modificar generate_response_mistral:

from services.cache_service import cache

def generate_response_mistral(pregunta: str, contexto: list):
    """Genera respuesta con Mistral Small usando contexto RAG + Cache"""
    
    # 1. Verificar cache
    cached_response = cache.get(pregunta)
    if cached_response:
        return {
            **cached_response,
            'from_cache': True,
            'tiempo_generacion': 0.001  # Prácticamente instantáneo
        }
    
    # 2. Si no está en cache, generar con Mistral
    # ... (código anterior) ...
    
    result = {
        'respuesta': response['message']['content'],
        'tiempo_generacion': elapsed,
        'tokens_generados': response.get('eval_count', 0),
        'from_cache': False
    }
    
    # 3. Guardar en cache
    cache.set(pregunta, result)
    
    return result
```

---

## 📊 Resultados Esperados Sprint 2

### Métricas técnicas

```
✅ LGSS indexada completa:
   - 567 bloques indexados
   - Modelo: pablosi/bge-m3-spa-law-qa-trained-2
   - Dimensiones: 1024
   - Tiempo indexación: ~25 min

✅ Mistral Small 24B instalado:
   - Modelo: mistral-small:24b-instruct-2501-q4_K_M
   - Tamaño: 14GB
   - RAM uso: ~14-16GB
   - Tiempo respuesta: 5-10 seg (CPU)

✅ Evaluación RAG completada:
   - 5 preguntas test evaluadas
   - Similitud Jaccard: >60% esperado
   - Citas artículo: 100% esperado
   - Cache funcionando

✅ Cache Redis implementado:
   - Hit rate: 0% (primera vez), luego >80%
   - TTL: 30 días
   - Ahorro tokens: ~90% en preguntas repetidas
```

### Comparativa con respuestas esperadas

**Archivo generado:** `backend/evaluation_results.json`

```json
{
  "fecha_evaluacion": "2025-12-05 20:30:00",
  "modelo_embeddings": "pablosi/bge-m3-spa-law-qa-trained-2",
  "modelo_llm": "mistral-small:24b-instruct-2501-q4_K_M",
  "metricas_resumen": {
    "total_preguntas": 5,
    "similitud_promedio": 0.65,
    "tiempo_promedio_seg": 7.2,
    "citas_articulo": 5
  },
  "resultados_detallados": [...]
}
```

---

## 🎯 Decisión: ¿Usar Mistral Small para qué?

### ✅ RECOMENDADO:

1. **Respuestas RAG en producción** (tu pregunta original)
   - Integrar en endpoint `/chat` de FastAPI
   - User pregunta → Qdrant search → Mistral response
   - Cache Redis para ahorrar tokens

2. **Evaluación calidad dataset** (antes de fine-tuning)
   - Revisar pares Q&A generados por Groq
   - Detectar respuestas incorrectas
   - Validar referencias legales

### ❌ NO USAR PARA:

1. **Generación inicial dataset** (mejor Groq gratis + rápido)
2. **Embeddings** (ya tenemos pablosi especializado)
3. **Fine-tuning ahora** (Sprint 5-8, no antes)

---

## ⏱️ Cronograma Ejecución

```
HORA 0:00 - Tarea 1: Instalar Mistral Small (10 min)
HORA 0:10 - Tarea 2: Re-indexar LGSS (25 min)
HORA 0:35 - Tarea 3: Cargar datasets Q&A (5 min)
HORA 0:40 - Tarea 4: Script evaluación (30 min creación + 10 min ejecución)
HORA 1:20 - Tarea 5: Cache Redis (30 min)
HORA 1:50 - Verificación y documentación (10 min)

TOTAL: 2 horas
```

---

## 🚀 Comando Único para Ejecutar Todo

```bash
# Script automatizado completo
cd /mnt/e/1/OPOS_GEMINI_1/backend
source venv/bin/activate

echo "🚀 INICIANDO SPRINT 2 COMPLETADO"

# 1. Verificar Mistral Small
echo "1️⃣ Verificando Mistral Small..."
ollama list | grep mistral-small || ollama pull mistral-small:24b-instruct-2501-q4_K_M

# 2. Re-indexar LGSS
echo "2️⃣ Re-indexando LGSS con pablosi..."
python -c "from qdrant_client import QdrantClient; QdrantClient('http://localhost:6333').delete_collection('opositaia_lgss_test')"
python agents/index_lgss_boe_api.py

# 3. Ejecutar evaluación
echo "3️⃣ Evaluando RAG + Mistral..."
python scripts/evaluate_rag_mistral.py

echo "✅ SPRINT 2 COMPLETADO - Ver resultados en evaluation_results.json"
```

---

**¿Procedemos a ejecutar? Confirma y arrancamos.**
