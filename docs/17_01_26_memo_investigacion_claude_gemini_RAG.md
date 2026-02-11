# 📋 MEMORIA DE INVESTIGACIÓN: AGENTIC RAG LEGAL
## Proyecto OposITAIA - Enero 2026

**Fecha:** 17/01/2026  
**Autor:** Investigación Claude + Gemini  
**Estado:** Implementación en curso

---

## 🎯 OBJETIVO DEL PROYECTO

Construir un sistema **Agentic RAG** especializado en legislación española (Seguridad Social, TRLGSS, LPAC) capaz de:
- Generar casos prácticos con **<5% alucinaciones**
- Citar artículos de forma verificable con **trazabilidad jurídica**
- Detectar automáticamente artículos derogados o modificados
- Funcionar con costes mínimos (~$18/mes)

---

## 📚 FASE 1: INVESTIGACIÓN

### Documentos Analizados

1. **claude_gemini_rag_oposiciones_2026.md** - Guía RAG 2026 de Stanford, NVIDIA, Anthropic
2. **Inventario del sistema existente** - Docker, PostgreSQL, Qdrant, MCP
3. **JSONs BOE** - 54 leyes con análisis de modificaciones/derogaciones

### Hallazgos Clave

| Fuente | Hallazgo | Impacto |
|--------|----------|---------|
| Stanford 2025 | 17-33% alucinaciones en RAG comerciales legales | Justifica sistema multi-agente |
| Vietnam Legal Text 2026 | +14% NDCG con GraphRAG | Descartamos Neo4j, usamos payload enriquecido |
| Swift Flutter 2025 | 71-89% reducción alucinaciones con guardrails | Implementamos 4 capas verificación |
| Fintech 2025 | 14.2% → 2.1% con confidence scoring | Añadido a FASE 6 |

---

## ⚙️ DECISIONES DE ARQUITECTURA

### ✅ LO QUE IMPLEMENTAMOS

#### 1. Búsqueda Híbrida (Dense + Sparse BM25)
```
Decisión: Combinar embeddings semánticos + keywords exactos
Razón: Mejora recall legal donde términos técnicos son críticos
Implementación: 
  - Dense: BGE-M3 1024D (pablosi/bge-m3-spa-law-qa-trained-2)
  - Sparse: BM25 con vocabulario 14,666 términos
```

#### 2. Dos Colecciones Qdrant Separadas
```
opositaia_knowledge_v2 (RAG):
  - 48,866 chunks con embeddings
  - Payload: 19 campos (vigente, modificado_por, deroga_a, etc.)
  - Vectores: dense 1024D + sparse BM25

opositaia_leyes_master (Referencia):
  - 54 leyes SIN embeddings
  - Payload completo: análisis, anteriores, posteriores
  - Para Legal Judge y verificación de vigencia
```

#### 3. Payload Enriquecido por Chunk
```json
{
  "boe_id": "BOE-A-2015-11724",
  "article_number": "173",
  "apartado": "2",
  "vigente": true,
  "fecha_vigencia": "20160102",
  "modificado_por": ["BOE-A-2024-10235", ...],
  "deroga_a": ["BOE-A-2013-13617", ...],
  "derogado_por": null,
  "url_boe": "https://...",
  "materias": ["Seguridad Social", ...]
}
```

#### 4. Modelo de Razonamiento: DeepSeek Reasoner
```
Rol: Generador principal de casos prácticos
Coste: ~$0.55/M input, $2.19/M output
Resultado: 9.0/10 en evaluación de calidad
```

---

### ❌ LO QUE DESCARTAMOS

| Propuesta | Razón del Descarte |
|-----------|-------------------|
| **Neo4j/GraphRAG** | Sobrecarga para 54 leyes. Relaciones ya en payload |
| **Voyage-3.5-Lite embeddings** | Tenemos BGE-M3 fine-tuned gratis |
| **GPT-5.1/o3-mini** | Modelos ficticios o muy caros. DeepSeek suficiente |
| **Chunking naive (500 tokens)** | Rompe artículos. Usamos chunking estructural |
| **Colección única** | Separamos RAG (ligero) de Master (análisis completo) |

---

## 🏗️ ARQUITECTURA FINAL

### Flow del Sistema Agentic RAG

```
┌─────────────────────────────────────────────────────────┐
│                    CONSULTA USUARIO                      │
│  "María, 38 años, IT por lumbalgia, ¿subsidio?"         │
└────────────────────────┬────────────────────────────────┘
                         │
           ┌─────────────▼─────────────┐
           │ AGENTE PLANIFICADOR       │ (Salamandra/DeepSeek)
           │ Descompone en pasos       │
           └─────────────┬─────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    ▼                    ▼                    ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│Búsqueda     │    │Búsqueda      │    │Verificación  │
│Dense BGE-M3 │    │Sparse BM25   │    │Vigencia      │
└──────┬──────┘    └──────┬───────┘    └──────┬───────┘
       │                  │                   │
       └──────────────────┼───────────────────┘
                          │
              ┌───────────▼───────────┐
              │ FUSION RRF + Rerank   │
              │ (BGE Reranker local)  │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │ PARENT-CHILD          │
              │ Recupera art. completo│
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │ GENERADOR             │ (DeepSeek Reasoner)
              │ Genera caso IT        │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │ CONFIDENCE SCORE      │
              │ ALTA/MEDIA/BAJA       │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │ ABOGADO DEL DIABLO    │ (Claude Opus 4.5 Thinking)
              │ Busca contradicciones │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │ LEGAL JUDGE           │
              │ + BOE API verify      │
              └───────────┬───────────┘
                          │
                    ┌─────▼─────┐
                    │ VÁLIDO?   │
                    │ SI → USER │
                    │ NO → LOOP │
                    └───────────┘
```

---

## 🤖 MODELOS UTILIZADOS

| Rol | Modelo | Coste | Razón |
|-----|--------|-------|-------|
| **Embeddings** | pablosi/bge-m3-spa-law-qa-trained-2 | $0 | Fine-tuned para legal español |
| **Generador** | DeepSeek Reasoner | ~$18/mes | Chain-of-thought nativo, barato |
| **Query Expansion** | Salamandra 7B (VPS) | $0 | Local, fallback a Ollama |
| **Relevance Filter** | Salamandra 7B | $0 | Filtro pre-rerank |
| **Reranker** | BGE Reranker v2 m3 | $0 | Local GGUF 350MB |
| **Adversarial Verifier** | Claude Opus 4.5 Thinking | Variable | Máxima calidad verificación |

---

## 📋 MEJORES PRÁCTICAS IMPLEMENTADAS

### 1. Anti-Alucinación (4 Capas)
```
Capa 1: System prompt estricto ("SOLO cita del contexto")
Capa 2: Citations obligatorias con verificación
Capa 3: Confidence scoring + escalation
Capa 4: Adversarial verification (Abogado del Diablo)
```

### 2. Trazabilidad Jurídica
```
- Cada chunk tiene boe_id + article_number + url_boe
- URLs verificables: https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a173
- Campo modificado_por[] lista todas las normas modificadoras
```

### 3. Detección de Derogaciones
```python
# En payload:
"vigente": True/False
"derogado_por": "BOE-A-2024-xxxx" | null
"estatus_derogacion": "N" | "S"
```

### 4. Verificación BOE API (Obligatoria)
```python
url = f"https://www.boe.es/datosabiertos/api/boe/documento/{boe_id}"
# Verifica en tiempo real si norma sigue vigente
```

---

## 📊 ORDEN DE EJECUCIÓN (FASES)

| Fase | Descripción | Estado | Tiempo |
|------|-------------|--------|--------|
| **0** | Re-ingesta Qdrant (híbrido + payload rico) | ✅ EN CURSO | 4-6h |
| **1** | Infraestructura (BGE Reranker, estructura) | Pendiente | 2h |
| **2** | Componentes RAG (expansion, filter, rerank) | Pendiente | 5h |
| **3** | Legal Judge + BOE API | Pendiente | 3h |
| **4** | Pipeline + FastAPI integrado | Pendiente | 4h |
| **5** | Testing + Benchmark (30 preguntas gold) | Pendiente | 3h |
| **6** | Mejoras Post-ingesta (sin reingestar) | Pendiente | 4h |

---

## 🆕 FASE 6: MEJORAS SIN REINGESTAR

Añadidas tras análisis del documento de investigación:

### 6.1 Parent-Child Retrieval (-35% errores)
```python
# Búsqueda encuentra apartado → Recupera artículo completo
enriched = await get_parent_article(boe_id, article_number)
```

### 6.2 Confidence Scoring + Escalation
```python
if confidence == "BAJA":
    return {"action": "HUMAN_REVIEW"}
elif confidence == "MEDIA":
    return {"disclaimer": "Verificar manualmente"}
```

### 6.3 Agente Planificador Explícito
```python
# Descompone consulta compleja en pasos de búsqueda
plan = [
    "1. Buscar requisitos IT en TRLGSS",
    "2. Verificar periodo carencia Art. 172"
]
```

### 6.4 Abogado del Diablo (Claude Opus 4.5 Thinking)
```python
# Segunda pasada adversarial
critic = await claude_opus_thinking.verify_adversarial(response, sources)
if not critic["is_valid"]:
    response = await regenerate_with_corrections(critic["errors"])
```

---

## 💰 COSTES ESTIMADOS

| Componente | Coste Mensual |
|------------|---------------|
| DeepSeek Reasoner | ~$18 |
| VPS Hostinger (Salamandra) | $0 (ya pagado) |
| Modelos locales | $0 |
| **TOTAL** | **~$18/mes** |

---

## 📈 MÉTRICAS OBJETIVO

| Métrica | Objetivo | Método Medición |
|---------|----------|-----------------|
| **Alucinaciones** | <5% | Eval manual 30 casos |
| **Recall@10** | >85% | Gold standard |
| **Latencia** | <5s primera respuesta | Prometheus |
| **Calidad generación** | >8.5/10 | Rubric legal |

---

## 🔗 ARCHIVOS RELEVANTES

```
docs/
├── 16_01_26_AGENTIC_RAG_PLAN.md       # Plan detallado v4
├── 16_01_26_INVENTARIO_SISTEMA.md     # Inventario Docker/VPS
└── 17_01_26_memo_investigacion...     # Este documento

backend/scripts/
├── reingest_qdrant_v3.py              # Ingesta híbrida
├── ingest_full_db_MAXIMUM.py          # Referencia BM25
└── deepseek_COMPLETE.py               # Generador 9.0/10

backend/rag/ (por crear)
├── query_expansion.py
├── relevance_filter.py
├── reranker.py
├── hybrid_search.py
├── parent_child.py
├── confidence.py
├── query_planner.py
├── adversarial_verifier.py
└── agentic_pipeline.py
```

---

## ✅ CONCLUSIONES

1. **Arquitectura híbrida** (Dense+BM25) es óptima para legal
2. **Payload enriquecido** elimina necesidad de Neo4j
3. **Multi-agente** con verificación adversarial reduce alucinaciones
4. **DeepSeek Reasoner** es suficiente como generador principal, usando MCP-s y el sistema de 9-10 agentes implementados para la creacion verificada y logica legal, reiteracion y calidad de 95+ % final!!! 
5. **Claude Opus 4.5** reservado para verificación por ahorro!
6. **Costes mínimos** (~$18/mes) gracias a modelos 
7. **FALTAN TODAVIA!!** prueba con otros modelos de generacion, de groq, de batch de calude, de mistral y de gemini 3 

---

*Documento generado: 17/01/2026 13:28*  
*Ingesta en curso: 48,866 chunks híbridos*
