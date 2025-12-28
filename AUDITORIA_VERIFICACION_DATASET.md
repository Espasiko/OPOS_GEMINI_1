# 🔍 AUDITORÍA COMPLETA: VERIFICACIÓN Y CALIDAD DEL DATASET

**Fecha:** 23 Diciembre 2025 19:55  
**Objetivo:** Asegurar que TODO el dataset está verificado contra BOE real y Qdrant

---

## 📊 RESUMEN EJECUTIVO

### ❌ **PROBLEMA CRÍTICO DETECTADO**

Los **293 items premium generados** (Razonamientos, Simulacros, Esquemas, etc.) **NO están verificados** contra BOE ni Qdrant:

- ✅ **Existen scripts de verificación** (17 encontrados)
- ❌ **NO se usaron** en la generación premium reciente
- ⚠️ **Riesgo de alucinaciones** en artículos, URLs y citas legales

---

## 🗂️ INVENTARIO DE SCRIPTS DE VERIFICACIÓN

### 1. **Verificación de URLs BOE** (3 scripts)

| Script | Función | Estado |
|--------|---------|--------|
| `dataset_generator/verify_boe_links.py` | Busca artículos en BOE.es via web scraping | ✅ Funcional |
| `dataset_generator/url_verifier.py` | Verifica URLs con HEAD requests + dominios confiables | ✅ Funcional (Rich UI) |
| `scripts/maintenance/url_verifier.py` | Versión mantenimiento | ✅ Funcional |

**Capacidades:**
- ✅ Verifica existencia de URLs (HTTP 200)
- ✅ Detecta dominios confiables (boe.es, noticias.juridicas.com)
- ✅ Marca URLs inventadas
- ❌ **NO verifica contenido** (solo que la URL existe)

### 2. **Verificación de Calidad Q&A** (2 scripts)

| Script | Función | LLM Usado |
|--------|---------|-----------|
| `dataset_generator/verify_qa.py` | Verifica calidad con agente LLM | Groq (Llama 3.3) |
| `verify_dataset_quality.py` | Valida estructura JSON de casos premium | N/A (validación sintáctica) |

**Capacidades:**
- ✅ Verifica longitud mínima/máxima
- ✅ Usa LLM para detectar errores factuales
- ✅ Calcula confianza (0-1)
- ⚠️ **NO verifica contra BOE real** (solo conocimiento del LLM)

### 3. **Verificación de Qdrant** (7 scripts)

| Script | Función |
|--------|---------|
| `backend/verificar_qdrant.py` | Verifica estado de colecciones |
| `scripts/maintenance/verificacion_completa_qdrant.py` | Auditoría completa de Qdrant |
| `scripts/maintenance/verificar_leyes_temario_oficial.py` | Verifica leyes del temario en Qdrant |
| `check_qdrant.py` | Check rápido de conectividad |
| `dataset_generator/check_collections.py` | Lista colecciones |
| `dataset_generator/check_payload_structure.py` | Verifica estructura de payloads |

**Capacidades:**
- ✅ Verifica que Qdrant está activo
- ✅ Cuenta documentos por colección
- ✅ Verifica estructura de metadatos
- ❌ **NO verifica que las citas en el dataset existen en Qdrant**

### 4. **Verificación de Ingesta BOE** (2 scripts)

| Script | Función |
|--------|---------|
| `backend/scripts/verify_ingestion_universal.py` | Verifica ingesta de leyes en PostgreSQL + Qdrant |
| `backend/scripts/verify_ingestion_rd84.py` | Verifica ingesta específica de RD 84/1996 |

**Capacidades:**
- ✅ Verifica que las leyes están en PostgreSQL
- ✅ Verifica que los chunks están en Qdrant
- ✅ Compara URLs BOE con BD
- ✅ **ESTE ES EL SCRIPT CLAVE** para verificación real

---

## 📋 ESTADO ACTUAL DEL DATASET (según memorias 20-21 dic)

### Dataset Consolidado: `golden_dataset/final_v1_train.jsonl`

**Composición (1,228 items):**
- **Thinking Cases (Groq):** Casos con razonamiento oculto
- **Enriched Exams (Mistral API):** Preguntas oficiales con referencias
- **Extreme Cases (DeepSeek):** Casos de dificultad experta
- **Standard QA:** Preguntas verificadas

**Problemas Detectados:**
1. ❌ **NO hay evidencia** de verificación BOE en memorias
2. ❌ **NO se menciona** uso de `verify_ingestion_universal.py`
3. ⚠️ Las "referencias" fueron **inyectadas por Mistral API** (no verificadas)

### Dataset Premium Reciente (293 items)

**Generado el 22 dic con:**
- `generate_razonamiento.py` → 118 items
- `generate_simulacros.py` → 50 items
- `generate_esquemas.py` → 50 items
- Etc.

**Problemas:**
- ❌ **NO usan RAG** (solo prompts directos a Groq)
- ❌ **NO verifican URLs** BOE
- ❌ **NO consultan PostgreSQL** para validar artículos

---

## 🚨 GAPS CRÍTICOS IDENTIFICADOS

### 1. **Falta Verificación Post-Generación**

**Problema:**  
Los scripts de generación premium **NO llaman** a los verificadores después de generar.

**Solución:**  
Crear pipeline: `Generar → Verificar URLs → Verificar Artículos en BD → Filtrar`

### 2. **Falta Integración RAG en Generación**

**Problema:**  
Scripts como `generate_razonamiento.py` **NO usan** `buscar_rag` del backend.

**Evidencia:**
```python
# generate_razonamiento.py (Línea 115)
def generate_caso_razonado(tema):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""Genera un CASO PRÁCTICO..."""  # ❌ NO hay contexto RAG
```

**Solución:**  
Modificar para que llame a `/api/rag/search` ANTES de generar.

### 3. **Falta Verificación de Artículos Citados**

**Problema:**  
El dataset tiene citas como "Art. 215 LGSS" pero **NO se verifica** que:
1. El artículo existe en PostgreSQL
2. El contenido del artículo coincide con lo citado
3. La URL BOE es correcta

**Solución:**  
Usar `verify_ingestion_universal.py` como base para crear `verify_dataset_citations.py`

---

## ✅ PLAN DE ACCIÓN INMEDIATO

### FASE 1: AUDITORÍA DEL DATASET ACTUAL (1-2 horas)

**Script a crear:** `audit_dataset_citations.py`

```python
# Pseudocódigo
for item in dataset:
    articulos_citados = extract_citations(item['output'])
    for art in articulos_citados:
        # 1. Verificar en PostgreSQL
        exists_in_db = query_postgres(art['articulo'], art['ley'])
        if not exists_in_db:
            mark_as_hallucination(item, art)
        
        # 2. Verificar URL BOE
        if 'url' in art:
            url_valid = verify_url_exists(art['url'])
            if not url_valid:
                mark_as_broken_link(item, art)
        
        # 3. Verificar contenido
        if exists_in_db:
            db_content = get_article_content(art['articulo'], art['ley'])
            similarity = compare_content(item['output'], db_content)
            if similarity < 0.7:
                mark_as_inconsistent(item, art)
```

**Output:**  
- `dataset_audit_report.json` con lista de items problemáticos
- `dataset_verified_clean.jsonl` solo con items 100% verificados

### FASE 2: REGENERACIÓN CON VERIFICACIÓN (2-3 horas)

**Modificar scripts existentes:**

1. **`generate_razonamiento.py`** → **`generate_razonamiento_verified.py`**
   - ✅ Añadir llamada a `/api/rag/search`
   - ✅ Extraer artículos del contexto RAG
   - ✅ Verificar cada artículo citado en PostgreSQL
   - ✅ Incluir URLs BOE reales en metadata

2. **`generate_simulacros.py`** → **`generate_simulacros_verified.py`**
   - ✅ Igual que arriba

### FASE 3: PIPELINE AUTOMATIZADO (1 hora)

**Script maestro:** `generate_and_verify_pipeline.py`

```python
def pipeline(tema):
    # 1. RAG
    context = buscar_rag_exhaustivo(tema)
    
    # 2. Generar
    item = generate_with_context(tema, context)
    
    # 3. Verificar
    citations = extract_citations(item)
    verification = verify_all_citations(citations)
    
    # 4. Filtrar
    if verification['all_valid']:
        return item
    else:
        log_failure(item, verification['errors'])
        return None
```

---

## 🛠️ SCRIPTS A CREAR/MODIFICAR

### Scripts Nuevos (Prioridad ALTA)

1. **`audit_dataset_citations.py`** 🔴
   - Audita dataset actual
   - Extrae todas las citas
   - Verifica contra PostgreSQL
   - Genera reporte

2. **`verify_dataset_citations.py`** 🔴
   - Función reutilizable
   - Verifica un item individual
   - Devuelve score de confianza

3. **`extract_citations.py`** 🔴
   - Extrae artículos citados de texto
   - Usa regex + NER
   - Normaliza formato

### Scripts a Modificar (Prioridad ALTA)

1. **`generate_razonamiento.py`** → Añadir RAG + verificación
2. **`generate_simulacros.py`** → Añadir RAG + verificación
3. **`generate_esquemas.py`** → Añadir RAG + verificación
4. **`generate_comparativas.py`** → Añadir RAG + verificación
5. **`generate_plazos.py`** → Añadir RAG + verificación

---

## 📈 MÉTRICAS DE CALIDAD PROPUESTAS

Para cada item del dataset, calcular:

```json
{
  "quality_score": 0.95,
  "verification": {
    "rag_used": true,
    "citations_verified": true,
    "urls_verified": true,
    "content_consistency": 0.92,
    "hallucination_risk": "low"
  },
  "citations": [
    {
      "text": "Art. 215 LGSS",
      "verified_in_db": true,
      "url_boe": "https://www.boe.es/...",
      "url_valid": true,
      "content_match": 0.95
    }
  ]
}
```

---

## 🎯 RECOMENDACIÓN FINAL

### ❌ **NO EJECUTAR** generación masiva hasta:

1. ✅ Auditar dataset actual (FASE 1)
2. ✅ Crear scripts de verificación (FASE 1)
3. ✅ Modificar scripts de generación (FASE 2)
4. ✅ Probar pipeline con 5 casos (FASE 2)
5. ✅ Validar que TODO está verificado (FASE 3)

### ✅ **SÍ EJECUTAR** ahora:

1. **Auditoría del dataset actual** con `audit_dataset_citations.py`
2. **Limpiar dataset** eliminando items no verificables
3. **Crear versión GOLD** solo con items 100% verificados

---

## 📝 PRÓXIMOS PASOS CONCRETOS

¿Quieres que:

1. **Cree `audit_dataset_citations.py`** para auditar el dataset actual?
2. **Modifique `generate_razonamiento.py`** para añadir RAG + verificación?
3. **Ejecute auditoría** en los 2,119 items de `MEGA_DATASET_v3_MASTER.jsonl`?

**Mi recomendación:** Empezar por (1) para saber el estado real del dataset antes de generar más datos.
