# 📋 PLAN AGENTIC RAG v3 - FINAL COMPLETO

**Fecha:** 16/01/2026 17:50  
**Estado:** PLAN FINAL - 6 FASES (APROBADO)

---

## 📊 LO QUE YA TENEMOS IMPLEMENTADO

| Componente | Archivo | Estado |
|------------|---------|--------|
| **Qdrant Local** | Docker `opositaia-qdrant` | ✅ 610MB, 48,866 puntos |
| **PostgreSQL** | Docker `opositaia-postgres` | ✅ 54 leyes, 50 columnas (metadata solo) |
| **Generador IT** | `deepseek_COMPLETE.py` | ✅ 9.0/10, 1 intento |
| **Embeddings** | `bge-m3-spa-law-qa-trained-2` | ✅ 1024D |
| **MCP Server** | `mcp-server/` | ✅ search_rag, get_legal_bases, verify_boe |
| **JSONs BOE** | `data/boe_xml/*.json` | ✅ 55 archivos con análisis completo |
| **VPS Hostinger** | `147.93.95.67` | ✅ Salamandra 7B, llama-server |
| **Dominio** | `electroyhogarpelotazo.tienda` | ✅ SSL activo |

---

## ❌ LO QUE FALTA (6 FASES)

```
FASE 0: Re-ingest + Colección Master │ 4-6h │ 🔴 BLOQUEANTE
FASE 1: Infraestructura              │ 2h   │
FASE 2: Componentes RAG              │ 5h   │ + Hybrid + VPS fallback
FASE 3: Legal Judge + BOE API        │ 3h   │
FASE 4: Pipeline + FastAPI           │ 4h   │
FASE 5: Testing + Benchmark          │ 3h   │
─────────────────────────────────────────────
TOTAL                                │ 21-23h │ (3-4 días)
```

---

## 🔴 FASE 0: RE-INGESTIÓN + COLECCIÓN MASTER [4-6h]

### Crear 2 colecciones en Qdrant:

#### COLECCIÓN 1: `opositaia_knowledge_v2` (RAG semántico)

**Payload enriquecido por chunk:**
```json
{
  "boe_id": "BOE-A-2015-11724",
  "law_name": "TRLGSS",
  "article_number": "173",
  "apartado": "2",
  "titulo_articulo": "Nacimiento del derecho al subsidio",
  "texto": "...",
  "layer": "article_chunk",
  "hash_texto": "md5_abc123",
  
  // CAMPOS NUEVOS DE ANÁLISIS
  "vigente": true,
  "fecha_vigencia": "2016-01-01",
  "ultima_modificacion": "2022-03-15",
  "modificado_por": ["BOE-A-2022-xxxx"],
  "deroga_a": [],
  "derogado_por": null,
  
  // URLS
  "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a173",
  "url_eli": "https://www.boe.es/eli/es/rdlg/2015/10/30/8/con"
}
```

**Puntos:** ~48,866 (con embeddings 1024D + sparse)  
**Tamaño estimado:** ~320 MB

---

#### COLECCIÓN 2: `opositaia_leyes_master` (Referencia completa)

**Payload completo por ley (SIN embeddings):**
```json
{
  "boe_id": "BOE-A-2015-11724",
  "titulo": "Real Decreto Legislativo 8/2015, TRLGSS",
  "tipo_norma": "Real Decreto Legislativo",
  "fecha_publicacion": "2015-10-31",
  "fecha_entrada_vigor": "2016-01-01",
  "vigente": true,
  
  // ANÁLISIS COMPLETO (de JSONs BOE)
  "analisis": {
    "materias": ["Seguridad Social", "Pensiones", ...],
    "referencias": {
      "anteriores": [
        {"id_norma": "BOE-A-1994-14960", "relacion": "DEROGA", "texto": "RD Legislativo 1/1994"},
        {"id_norma": "BOE-A-2013-xxxx", "relacion": "MODIFICA"}
      ],
      "posteriores": [
        {"id_norma": "BOE-A-2022-xxxx", "relacion": "MODIFICA", "texto": "RD 2/2022"}
      ]
    }
  },
  
  // URLS
  "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
  "url_pdf": "https://www.boe.es/boe/dias/2015/10/31/pdfs/BOE-A-2015-11724.pdf",
  "url_xml": "https://www.boe.es/...",
  
  // TEXTO COMPLETO (opcional, para Legal Judge)
  "indice_articulos": ["Art. 1", "Art. 2", ..., "Art. 373"],
  "num_articulos": 373
}
```

**Puntos:** 54 (1 por ley)  
**Tamaño estimado:** ~25 MB

---

### Tareas FASE 0:

```bash
# 1. Leer JSONs de data/boe_xml/
ls data/boe_xml/*.json | wc -l  # 55 archivos

# 2. Extraer análisis de cada JSON
python backend/scripts/extract_analisis_from_json.py

# 3. Crear colección v2 con schema enriquecido
curl -X PUT "http://localhost:6333/collections/opositaia_knowledge_v2" ...

# 4. Crear colección master
curl -X PUT "http://localhost:6333/collections/opositaia_leyes_master" ...

# 5. Re-ingestar chunks con metadata de análisis
python backend/scripts/reingest_qdrant_v3.py

# 6. Verificar
curl "http://localhost:6333/collections"
```

### Resultado esperado:
- ✅ Colección v2: 48,866 chunks con 15+ campos
- ✅ Colección master: 54 leyes con análisis completo
- ✅ Campos modificado_por, derogado_por funcionando
- ✅ Total ~350 MB (cabe en 1GB)

---

## FASE 1: INFRAESTRUCTURA [2h]

```bash
# 1. Crear estructura
mkdir -p backend/rag
touch backend/rag/__init__.py
mkdir -p backend/models

# 2. Descargar BGE Reranker (350MB)
wget https://huggingface.co/BAAI/bge-reranker-v2-m3-GGUF/resolve/main/bge-reranker-v2-m3-q8_0.gguf \
  -O backend/models/bge-reranker-v2-m3-q8_0.gguf

# 3. Instalar dependencias
pip install llama-cpp-python httpx
```

---

## FASE 2: COMPONENTES RAG [5h]

### 2.1 Query Expansion con VPS fallback

```python
# backend/rag/query_expansion.py

import os
import httpx

# PRIORIDAD: VPS primero, local fallback
SALAMANDRA_URLS = [
    os.getenv("VPS_SALAMANDRA_URL", "http://147.93.95.67:8080"),
    os.getenv("LOCAL_OLLAMA_URL", "http://localhost:11434")
]

async def call_salamandra(prompt: str) -> str:
    """Intenta VPS, si falla usa local"""
    for url in SALAMANDRA_URLS:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{url}/v1/chat/completions",
                    json={
                        "model": "salamandra-base",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.3
                    }
                )
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"⚠️ {url} falló: {e}, intentando siguiente...")
            continue
    raise Exception("❌ No hay Salamandra disponible (ni VPS ni local)")

async def expand_query(query: str) -> List[str]:
    prompt = f"""Genera 3 variaciones de esta consulta legal:
    Original: {query}
    
    Variaciones (JSON):"""
    
    result = await call_salamandra(prompt)
    return json.loads(result)
```

### 2.2 Relevance Filter - CÓDIGO PROPORCIONADO ✅

### 2.3 Re-ranker (BGE) - CÓDIGO PROPORCIONADO ✅

### 2.4 Hybrid Search

```python
# backend/rag/hybrid_search.py

async def hybrid_search(
    qdrant_client,
    query: str,
    collection: str = "opositaia_knowledge_v2",
    alpha: float = 0.7,  # 70% dense, 30% sparse
    limit: int = 15
) -> List[Dict]:
    # Dense (embeddings semánticos)
    dense_results = await qdrant_client.search(
        collection_name=collection,
        query_vector=("dense", embed(query)),
        limit=limit
    )
    
    # Sparse (BM25 keywords)
    sparse_results = await qdrant_client.search(
        collection_name=collection,
        query_vector=("text", bm25_encode(query)),
        limit=limit
    )
    
    # Merge normalizado
    return merge_with_weights(dense_results, sparse_results, alpha)
```

---

## FASE 3: LEGAL JUDGE + BOE API [3h]

### Legal Judge con verificación BOE

```python
# backend/rag/legal_judge.py

class LegalJudgeAgent:
    def __init__(self, qdrant_client):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.qdrant = qdrant_client
    
    async def validate(self, caso: dict) -> dict:
        # 1. Extraer artículos citados
        articulos_citados = self._extract_articles(caso)
        
        # 2. Verificar cada artículo en colección master
        errores_vigencia = []
        for art in articulos_citados:
            info = await self._get_article_info(art['boe_id'], art['article'])
            
            if info.get('derogado_por'):
                errores_vigencia.append({
                    "tipo": "articulo_derogado",
                    "articulo": art,
                    "derogado_por": info['derogado_por'],
                    "severidad": "critica"
                })
            
            if info.get('modificado_por'):
                errores_vigencia.append({
                    "tipo": "articulo_modificado",
                    "articulo": art,
                    "modificado_por": info['modificado_por'],
                    "severidad": "moderada"
                })
        
        # 3. Verificar con BOE API (obligatorio, para todos los casos)
        if errores_vigencia:
            for error in errores_vigencia:
                boe_check = await self._verify_boe_api(error['articulo']['boe_id'])
                error['boe_api_verificado'] = boe_check
        
        # 4. Validar con DeepSeek Reasoner
        prompt = self._build_validation_prompt(caso, errores_vigencia)
        response = await self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def _get_article_info(self, boe_id: str, article: str) -> dict:
        """Consulta colección master para info de vigencia"""
        results = await self.qdrant.scroll(
            collection_name="opositaia_leyes_master",
            scroll_filter={"must": [{"key": "boe_id", "match": {"value": boe_id}}]},
            limit=1,
            with_payload=True
        )
        if results[0]:
            return results[0][0].payload.get('analisis', {})
        return {}
    
    async def _verify_boe_api(self, boe_id: str) -> dict:
        """Verificación en tiempo real con BOE API"""
        url = f"https://www.boe.es/datosabiertos/api/boe/documento/{boe_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "existe": True,
                    "vigente": data.get('vigente'),
                    "fecha_actualizacion": data.get('fecha_actualizacion')
                }
        return {"existe": False}
```

---

## FASE 4: PIPELINE + FASTAPI [4h]

### Pipeline integrado

```python
# backend/rag/agentic_pipeline.py

class AgenticRAGPipeline:
    def __init__(self, qdrant_client, enable_all=True):
        self.qdrant = qdrant_client
        self.expander = QueryExpander()      # Salamandra VPS/local
        self.filter = RelevanceFilter()       # Salamandra VPS/local
        self.reranker = BGEReranker()         # Local 350MB
        self.hybrid = HybridSearch()          # Dense + Sparse
    
    async def search(self, query: str, top_k_final: int = 5) -> List[Dict]:
        # 1. Expandir query (3 variaciones)
        queries = await self.expander.expand(query)  # VPS → local fallback
        
        # 2. Búsqueda híbrida paralela
        all_results = []
        for q in queries:
            results = await self.hybrid.search(self.qdrant, q, limit=15)
            all_results.extend(results)
        
        # 3. Dedup por hash
        unique = self._deduplicate(all_results)
        
        # 4. Filtrar irrelevantes (Salamandra)
        filtered = await self.filter.filter(unique, query)
        
        # 5. Re-rank (BGE local)
        ranked = self.reranker.rank(filtered, query)
        
        return ranked[:top_k_final]
```

### Integración FastAPI

```python
# backend/main.py (añadir)

@app.on_event("startup")
async def startup():
    print("🚀 Cargando sistema agentic...")
    
    qdrant = QdrantClient(url="http://localhost:6333")
    
    # Pipeline con todos los componentes
    app.state.rag = AgenticRAGPipeline(
        qdrant_client=qdrant,
        enable_all=True
    )
    
    # Legal Judge con acceso a colección master
    app.state.judge = LegalJudgeAgent(qdrant_client=qdrant)
    
    print("✅ Sistema listo")

@app.post("/generate-case")
async def generate_case_endpoint(tema: str = "Incapacidad Temporal"):
    # 1. Búsqueda agentic
    docs = await app.state.rag.search(
        query=f"casos prácticos {tema} artículos requisitos",
        top_k_final=5
    )
    
    # 2. Generar caso
    caso = await generate_case_BEST(tema, context=docs)
    
    # 3. Validar con Legal Judge (incluye BOE API)
    validation = await app.state.judge.validate(caso)
    
    if not validation['valido']:
        return {"error": "Rechazado", "validation": validation, "caso_raw": caso}
    
    return {"caso": caso, "score": validation['puntuacion'], "docs_used": len(docs)}
```

---

## FASE 5: TESTING + BENCHMARK [3h]

```python
# tests/benchmark_agentic.py
# tests/benchmark_judge.py
# tests/data/gold_standard.json (30 preguntas)
```

---

## 💰 COSTES ESTIMADOS

| Componente | Coste mensual |
|------------|---------------|
| Legal Judge (DeepSeek) | ~$18 |
| VPS Hostinger | $0 (ya pagado) |
| BGE Reranker | $0 (local) |
| Salamandra | $0 (VPS/local) |
| **TOTAL** | **~$18/mes** |

---

## 📊 TAMAÑOS ESTIMADOS

| Colección | Puntos | Tamaño |
|-----------|--------|--------|
| opositaia_knowledge_v2 | 48,866 | ~320 MB |
| opositaia_leyes_master | 54 | ~25 MB |
| **TOTAL** | | **~350 MB** |

✅ Cabe en 1GB

---

## 📋 CHECKLIST COMPLETO FINAL

### FASE 0: Re-ingest + Master 🔴
- [ ] Leer JSONs de `data/boe_xml/*.json`
- [ ] Extraer `analisis.referencias` de cada ley
- [ ] Crear script `extract_analisis_from_json.py`
- [ ] Crear colección `opositaia_knowledge_v2` con payload rico
- [ ] Crear colección `opositaia_leyes_master` con análisis completo
- [ ] Añadir campos: `modificado_por`, `derogado_por`, `ultima_modificacion`
- [ ] Re-ingestar 48,866 chunks
- [ ] Insertar 54 leyes en master
- [ ] Verificar ambas colecciones

### FASE 1: Infraestructura
- [ ] Crear `backend/rag/`
- [ ] Descargar BGE (350MB)
- [ ] Instalar `llama-cpp-python`
- [ ] Configurar variables VPS/local

### FASE 2: Componentes RAG
- [ ] `query_expansion.py` con VPS → local fallback
- [ ] `relevance_filter.py` con VPS → local fallback
- [ ] `reranker.py` (BGE local)
- [ ] `hybrid_search.py` (dense + sparse)

### FASE 3: Legal Judge + BOE API
- [ ] `legal_judge.py`
- [ ] Consulta a colección master
- [ ] Integración BOE API
- [ ] Validación de vigencia

### FASE 4: Pipeline + FastAPI
- [ ] `agentic_pipeline.py`
- [ ] Startup con carga de modelos
- [ ] Endpoint `/generate-case`

### FASE 5: Testing
- [ ] Gold standard 30 preguntas
- [ ] Benchmarks

### FASE 6: MEJORAS POST-INGESTA [4h] *(SIN reingestar)*

#### 6.1 Parent-Child Retrieval (-35% errores)
- [ ] Crear `backend/rag/parent_child.py`
- [ ] Al buscar apartado, recuperar artículo completo de PostgreSQL
- [ ] Enviar contexto ampliado al LLM
```python
# Búsqueda encuentra "Art. 173.2" → Recupera Art. 173 completo
enriched = await get_parent_article(boe_id, article_number)
```

#### 6.2 Confidence Scoring + Escalation
- [ ] Crear `backend/rag/confidence.py`
- [ ] Auto-evaluar confianza: ALTA/MEDIA/BAJA
- [ ] BAJA → Escalar a humano
- [ ] MEDIA → Añadir disclaimer
```python
if confidence == "BAJA":
    return {"action": "HUMAN_REVIEW", "warning": "⚠️ Revisar"}
```

#### 6.3 Agente Planificador Explícito
- [ ] Crear `backend/rag/query_planner.py`
- [ ] Descomponer preguntas complejas en pasos
- [ ] Múltiples búsquedas coordinadas
```python
# "¿Puede autónomo cobrar IT con 2 meses sin cotizar?"
plan = [
    "1. Buscar requisitos cotización IT TRLGSS",
    "2. Verificar periodo carencia Art. 172", 
    "3. Comprobar situación asimilada alta"
]
```

#### 6.4 Agente Verificador "Abogado del Diablo" *(Claude Opus 4.5 Thinking)*
- [ ] Crear `backend/rag/adversarial_verifier.py`
- [ ] Segunda pasada adversarial post-generación con **Claude Opus 4.5 Thinking**
- [ ] Detectar contradicciones, omisiones, leyes derogadas
- [ ] Si hay errores → Regenerar con correcciones
- [ ] Nota: Modelo puede cambiar a uno más barato en el futuro
```python
# Usar Claude Opus 4.5 Thinking para verificación adversarial
critic = await claude_opus_thinking.verify_adversarial(response, sources)
if not critic["is_valid"]:
    response = await regenerate_with_corrections(critic["errors"])
```

---

## 🎯 PRÓXIMO PASO

**FASE 0 EN CURSO:**
```bash
# Ingesta completa 54 leyes (~48k chunks híbridos)
python backend/scripts/reingest_qdrant_v3.py
# Progreso: 11/54 leyes (14:48h)
```

---

## 🚀 ROADMAP COMPLETO POST-AGENTIC RAG

### FASE 7: COMPARATIVA DE MODELOS DE GENERACIÓN [8-12h]

Tras tener el Agentic RAG perfecto (reranking, guardrails, Cohere, etc.), **evaluar alternativas al generador**:

| Modelo | API | Ventaja | Coste Estimado |
|--------|-----|---------|----------------|
| **Groq (Llama 3.1 70B)** | REST | Ultra-rápido (~500 tok/s) | ~$0.59/M |o deepseek sso 120B 
| **Claude Batch** | Batch API | -50% coste | ~$1.50/M |
| **Mistral Large 2** | REST | Europeo, GDPR | ~$2/M |
| **Gemini 2.5 Pro** | REST | Largo contexto 1M | ~$3.50/M | o gemini 3
| **DeepSeek Reasoner** (actual) deepseek reasoner 3.2 | REST | CoT nativo | ~$2.19/M |

**Tareas:**
- [ ] Configurar APIs de todos los modelos todos en .env.backend 
- [ ] Ejecutar mismo dataset (30 casos) con cada modelo
- [ ] Medir: precisión, veracidad, logica legal, coste/caso
- [ ] Usar sistema de 9-10 agentes orquestado para , o funciones , sino permiten agentes
- [ ] Calcular costes finales del dataset completo
- [ ] **Decisión final**: modelo para producción y uso diario con usuarios de prueba!!! 

---

### FASE 8: FINE-TUNING SALAMANDRA [10-15h]

**Objetivo:** Fine-tunear Salamandra 7B con datos propios para:
- Query expansion legal
- Relevance filtering
- Posible reemplazo de DeepSeek para generación

**Tareas:**
- [ ] Preparar dataset de fine-tuning (pares pregunta-respuesta legal)
- [ ] Formato: JSONL con prompt templates
- [ ] Fine-tune con LoRA/QLoRA (menor VRAM)
- [ ] Evaluar en benchmark legal propio
- [ ] Desplegar en VPS Hostinger
- [ ] Comparar con modelo base

---

### FASE 9: EVALUACIÓN AUTOMÁTICA + HUMANA [8-10h]

#### 9.1 Evaluación Automática con Claude Opus 4.5
```python
# Rubric automática para cada caso generado
eval_prompt = """
Evalúa este caso práctico legal en escala 1-10:
-logica legal impecable?
- Precisión jurídica: ¿Artículos citados correctos?
- Coherencia: ¿Lógica del caso consistente?
- Completitud: ¿Faltan elementos críticos?
- Trazabilidad: ¿Citas verificables?
"""
```

**Tareas:**
- [ ] Crear rubric de evaluación legal (10 criterios)
- [ ] Script de evaluación batch con Claude Opus
- [ ] Generar 500 casos y evaluar automáticamente
- [ ] Identificar patrones de error

#### 9.2 Verificación Humana (Abogados/Opositores)
- [ ] Seleccionar 100 casos para revisión humana
- [ ] Crear formulario de evaluación
- [ ] Contratar 2-3 revisores expertos
- [ ] Correlacionar eval. automática vs. humana
- [ ] **Objetivo**: >95% precisión final

---

### FASE 10: GENERACIÓN MASIVA DE CONTENIDO [20-30h]

#### 10.1 Casos Prácticos (1,000+)
```
📦 Objetivo: 1,000 casos prácticos verificados
├── Incapacidad Temporal: 200 casos
├── Jubilación: 200 casos
├── Maternidad/Paternidad: 150 casos
├── Desempleo: 150 casos
├── Viudedad/Orfandad: 100 casos
├── Accidentes de Trabajo: 100 casos
└── Casos mixtos/complejos: 100 casos
```

#### 10.2 Preguntas Tipo Test (3,000-4,000) primero evaluar los %-jes de presencia/dificultad de las  preguntas por tema en los examnes oficiales anteriores!!!
```
📦 Objetivo: 3,500 preguntas tipo simulacro
├── TRLGSS: 1,500 preguntas
├── LPAC: 500 preguntas
├── TREBEP: 400 preguntas
├── Constitución: 400 preguntas
├── Ley 40/2015 LRJSP: 300 preguntas
└── Otras leyes: 400 preguntas
```

#### 10.3 Material Complementario
- [ ] **Flashcards**: 2,000 tarjetas Anki/Quizlet
- [ ] **Mapas mentales**: 50 mapas por temario principal, conceptos, relaciones etc. (ver estrategias de enseñañza de Gemini y valera y otros!!!)
- [ ] **Esquemas**: Diagramas de flujo procedimientos
- [ ] **Resúmenes**: 1-2 páginas por ley (usar modelos de resumenes BOE-XSUM u otros)

---

### FASE 11: COSM + PRODUCCIÓN [15-20h]

**COSM = Create Once, Serve Many** no se trata de formatos , es combinar los items que ya tenemos creadoas , cambiando pocos detelles , nombres etc. pero conservando el problema y la logica, para que los usuarios no puedan distigui los tests, verlos como nuevos , pero entrenar masivamente... esto es COSM = Create Once, Serve Many (TYMES) 

#### 11.1 Formatos de Salida
```
Mismo contenido → Múltiples formatos:
├── JSON (API)
├── PDF (descarga)
├── Web (frontend React)
├── Anki (flashcards)
├── Audio (TTS para estudio)
├── Email (newsletter diaria)
└── Telegram/Discord (bots)
```

#### 11.2 Infraestructura Producción -POR DESIDIR TODAVIA
- [ ] Frontend Next.js/React con UI premium
- [ ] Backend FastAPI con endpoints RAG
- [ ] CDN para PDFs y assets
- [ ] Base de datos usuarios (Supabase/Postgres)
- [ ] Sistema de suscripción/pagos
- [ ] Analytics y métricas de uso

#### 11.3 Monetización empezar con packs pdf-s+chat explicativo con IA (investigar!!!)
```
💰 Estrategia de monetización:
├── Freemium: 10 casos/mes gratis
├── Basic: €19/mes (100 casos + tests)
├── Pro: €39/mes (ilimitado + simulacros)
└── Enterprise: Academias/empresas
```

---

## 📊 RESUMEN ROADMAP COMPLETO

| Fase | Descripción | Tiempo | Prioridad |
|------|-------------|--------|-----------|
| 0 | Re-ingesta Qdrant | 4-6h | ✅ EN CURSO |
| 1 | Infraestructura | 2h | 🔴 ALTA |
| 2 | Componentes RAG | 5h | 🔴 ALTA |
| 3 | Legal Judge + BOE API | 3h | 🔴 ALTA |
| 4 | Pipeline + FastAPI | 4h | 🔴 ALTA |
| 5 | Testing | 3h | 🟡 MEDIA |
| 6 | Mejoras post-ingesta | 4h | 🟡 MEDIA |
| 7 | Comparativa modelos | 8-12h | 🟡 MEDIA |
| 8 | Fine-tuning Salamandra | 10-15h | 🟢 BAJA |
| 9 | Evaluación auto+humana | 8-10h | 🟡 MEDIA |
| 10 | Generación contenido | 20-30h | 🟡 MEDIA |
| 11 | COSM + Producción | 15-20h | 🟢 BAJA |

**TOTAL ESTIMADO: 85-120 horas (~3-4 semanas)**

---

*Plan v5 FINAL - 17/01/2026 14:48 - Roadmap completo hasta producción*
