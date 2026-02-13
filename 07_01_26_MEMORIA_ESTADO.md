# 📝 MEMORIA SESIÓN 05-07 ENERO 2026

**Período:** 05/01/2026 00:00 - 07/01/2026 15:10  
**Duración:** ~63 horas (2.6 días)  
**Proyecto:** OposIA - Sistema RAG Legal Español

---

## 🎯 RESUMEN EJECUTIVO

### Logros Principales
1. ✅ **Claude 4.5 API actualizada** - Evaluación batch 102 preguntas  
2. ✅ **Salamandra RAG failure diagnosticado y corregido**  
3. ✅ **Migración a Qdrant Cloud** (de localhost)  
4. ✅ **VPS optimization research** completa  
5. ⚠️ **Test en progreso** con configuración corregida

### Hallazgos Críticos estabamos usando qdrant local malo y tardaba mas y estaba respondiendo sin consultar el rag!!!!!!!! 
- **Salamandra 7B**: Solo 6% mejor modelo (vs DeepSeek 67%)  
- **Root cause**: Script equivocado ejecutado (sin RAG context dump)  
- **VPS real**: 8GB RAM, 2 vCPUs AMD EPYC, 1GB swap USADO  
- **Qdrant**: Vector unnamed (no "dense") en Cloud

---

## 📅 TIMELINE DETALLADO

### **05/01/2026 - DÍA 1: Claude API + Batch Evaluation**

#### 09:00 - Claude 4.5 API Investigation
- **Acción:** Investigación modelos Claude nuevos 2026
- **Hallazgo:** Claude 3.5 Sonnet deprecated → `claude-sonnet-4-5-20250929`
- **Pricing:** $3/MTok input, $15/MTok output
- **Features nuevas:** Extended Thinking, Structured Outputs, MCP integration

#### 11:30 - Fix Batch Script
- **Archivo:** `backend/scripts/06_01_26_claude_judge_batch_v2.py`
- **Cambio:** Línea 197 - modelo correcto
- **Test:** 3 preguntas sample OK

#### 14:00 - Batch Evaluation Completa
- **Input:** 102 preguntas (DeepSeek, Groq Llama, Groq GPT, Salamandra)
- **Output:** `claude_critical_evaluation.jsonl`
- **Duración:** ~45 minutos procesamiento

#### 18:00 - Análisis Resultados
- **Artifact creado:** `INFORME_EVALUACION_CLAUDE_JUDGE.md`
- **Hallazgo CRÍTICO:**
  ```
  DeepSeek: 67% mejor modelo, score 8.42/10
  Salamandra: 6% mejor modelo, score 3.87/10 ⚠️
  ```
- **Errores Salamandra:** 64% graves, razonamiento vago

---

### **06/01/2026 - DÍA 2: Salamandra RAG Investigation**

#### 08:00 - Root Cause Analysis
- **Pregunta:** ¿Por qué Salamandra tan mal?
- **Hipótesis inicial:** Modelo débil
- **Investigación:** Revisar scripts de generación

#### 10:30 - Script Comparison
- **Archivos revisados:**
  - `06_01_26_salamandra_agent.py` (VIEJO - ejecutado por error)
  - `06_01_26_salamandra_reasoner.py` (CORRECTO)
  
- **Diferencia clave:**
  ```python
  # VIEJO (ejecutado):
  record = {
      "rag_context_used": True,  # Boolean ❌
      "postgres_context_used": False
  }
  
  # CORRECTO:
  record = {
      "rag_context_dump": context,  # String 5K chars ✅
      "model_used": "salamandra-vps-rag"
  }
  ```

#### 12:00 - RAG Pipeline Test
- **Script creado:** `backend/scripts/TEST_RAG_PIPELINE.py`
- **Resultado:**
  ```
  ✅ Qdrant search: 5137 chars contexto
  ✅ Embeddings: pablosi/bge-m3 loaded
  ✅ Postgres: full texts accessible
  ```
- **Conclusión:** RAG 100% funcional, script equivocado ejecutado

#### 15:00 - VPS Endpoint Investigation
- **Problema:** VPS timeout/empty reply
- **Hallazgo:** Nginx proxy roto en puerto 80
- **Dominio correcto:** `http://electroyhogarpelotazo.tienda/salamandra/reason`
- **Test:** FastAPI format `{question, context, options}` ✅

#### 18:30 - Script Híbrido Creado
- **Archivo:** `backend/scripts/06_01_26_salamandra_FINAL.py`
- **Combinación:**
  - RAG directo (reasoner)
  - VPS FastAPI format (old agent)
- **Test inicial:** 2 exams, SOLO 1 pregunta exitosa (Q2)

---

### **07/01/2026 - DÍA 3: VPS Optimization + Qdrant Cloud**

#### 08:00 - VPS Specs Audit
- **Comando:** `ssh ubuntu@147.93.95.67 "cat /proc/cpuinfo ..."`
- **Resultado:**
  ```
  CPU: AMD EPYC 9354P 32-Core (SOLO 2 cores asignados)
  RAM: 7.8 GB total
  Swap: 2GB (1GB USADO ⚠️)
  Modelo Salamandra en memoria: ~90MB proceso Ollama
  ```

#### 09:30 - Optimization Research
- **Búsquedas web:**
  - Ollama CPU optimization 2026
  - Hostinger VPS best practices
  - Q4_K_M vs Q8 quantization
  - num_thread/num_ctx tuning
  
- **Hallazgos clave:**
  1. `OLLAMA_KEEP_ALIVE=-1` crítico (mantener modelo en RAM)
  2. `num_ctx` 4096→2048 reduce pressure (user decidió mantener 4096)
  3. Q4_K_M ya óptimo para CPU
  4. 7B models CAN run on 8GB RAM (1-5 tokens/sec)

#### 11:00 - User Research Evaluation
- **Input:** Usuario aportó investigación async/Redis (otra IA)
- **Análisis:** Otro AI asumió I/O bottleneck, realidad = RAM constraint
- **Artifact:** `EVALUACION_INVESTIGACION_vs_REALIDAD.md`
- **Conclusión:** Async/Redis correcto para 16GB+, no para 8GB actual

#### 13:00 - RAGFlow/InfiniFlow Investigation
- **Hallazgo:** RAGFlow = framework completo (no reemplazo Qdrant)
- **ollama-mcp-bridge:** Interesante futuro, no prioritario
- **Decisión:** Mantener stack actual, optimizar existente

#### 14:30 - Qdrant Cloud Migration ⚡
- **.env.backend cambio CRÍTICO:**
  ```bash
  # ANTES (local - lento):
  QDRANT_URL=http://localhost:6333
  
  # DESPUÉS (Cloud - rápido):
  QDRANT_URL=https://b554ceb5-2169...cloud.qdrant.io
  ```

#### 14:50 - Vector Name Fix 🔧
- **Error encontrado:**
  ```
  400 Bad Request: "Not existing vector name error: dense"
  ```
  
- **Causa:** Qdrant Cloud usa vector DEFAULT (unnamed), no named "dense"
  
- **Fix en `salamandra_FINAL.py`:**
  ```python
  # ANTES:
  query_vector=('dense', vector)
  
  # DESPUÉS:
  query_vector=vector  # Vector directo
  ```

#### 15:10 - Test Reiniciado
- **Estado:** Script ejecutándose con config correcta
- **Próximo:** Verificar resultados y comparar calidad

---

## 🔧 CAMBIOS TÉCNICOS APLICADOS

### Archivos Modificados

#### 1. `backend/.env.backend`
```diff
- # QDRANT_URL=https://...cloud.qdrant.io
- QDRANT_URL=http://localhost:6333
+ QDRANT_URL=https://b554ceb5-2169...cloud.qdrant.io
+ # QDRANT_URL=http://localhost:6333
```

#### 2. `backend/scripts/06_01_26_claude_judge_batch_v2.py`
```diff
- model="claude-3-5-sonnet-20240620",  # Deprecated
+ model="claude-sonnet-4-5-20250929",  # Claude 4.5
```

#### 3. `backend/scripts/06_01_26_salamandra_FINAL.py` (NUEVO)
- Creado combinando reasoner + old agent
- RAG directo + VPS FastAPI format
- Vector fix: `query_vector=vector` (no tupla)

#### 4. Scripts renombrados
- `06_01_26_salamandra_agent.py` → `OBSOLETE_...py.bak`

---

## 📊 CONFIGURACIÓN ACTUAL

### Qdrant Cloud
```json
{
  "url": "https://b554ceb5-2169...europe-west3-0.gcp.cloud.qdrant.io",
  "collection": "opositaia_knowledge",
  "points": 48866,
  "vectors": {
    "size": 1024,
    "distance": "Cosine"
  },
  "precision@10": 0.95,
  "search_time": "61-111ms"
}
```

### VPS Hostinger
```yaml
Hardware:
  CPU: AMD EPYC 9354P (2 vCPUs)
  RAM: 7.8 GB total
  Swap: 2GB (1GB usado - señal OOM)
  Storage: NVMe SSD

Software:
  OS: Ubuntu 24.04
  Ollama: Active (proceso 90MB)
  Modelo: salamandra-opos:latest (Q4_K_M, 4.9GB)
  Nginx: Proxy puerto 80
  FastAPI VPS: electroyhogarpelotazo.tienda/salamandra/reason

Config Ollama:
  num_ctx: 4096 (mantenido por usuario)
  temperature: 0.1
  OLLAMA_KEEP_ALIVE: NO configurado ⚠️ (pendiente)
```

### Embeddings Local
```yaml
Model: pablosi/bge-m3-spa-law-qa-trained-2
Dimensiones: 1024
Framework: SentenceTransformers
Uso: Encoding queries para Qdrant search
```

---

## 🎯 ESTADO ACTUAL PROYECTO

### Scripts Funcionales
- ✅ `TEST_RAG_PIPELINE.py` - Diagnóstico completo
- ✅ `06_01_26_claude_judge_batch_v2.py` - Evaluación batch
- ✅ `06_01_26_salamandra_FINAL.py` - En test ahora
- ✅ `06_01_26_groq_reasoner.py` - Comparativa
- ✅ `06_01_26_deepseek_reasoner.py` - Comparativa

### Datos Generados
```
staging_area/06_01_26_enrichment/
├── claude_critical_evaluation.jsonl (102 items)
├── deepseek_reasoning.jsonl (completado)
├── groq_llama_reasoning.jsonl (completado)
├── groq_gpt_reasoning.jsonl (completado)
└── salamandra_reasoning.jsonl (1 item viejo, regenerando)
```

### Artifacts Creados (últimas 48h)
1. `CLAUDE_4_5_UPDATE_2026.md` - API docs
2. `INFORME_EVALUACION_CLAUDE_JUDGE.md` - Resultados críticos
3. `DIAGNOSTICO_SALAMANDRA_RAG_FAILURE.md` - Root cause
4. `SOLUCION_SALAMANDRA_SCRIPT_CORRECTO.md` - Fix strategy
5. `OPTIMIZACION_VPS_OLLAMA_2026.md` - Research findings
6. `EVALUACION_INVESTIGACION_vs_REALIDAD.md` - User research analysis

---

## ⚠️ PROBLEMAS IDENTIFICADOS Y ESTADO

### RESUELTOS ✅
1. ~~Claude API deprecated model~~ → Actualizado 4.5
2. ~~Salamandra sin RAG context~~ → Script correcto identificado
3. ~~VPS endpoint no responde~~ → Dominio correcto encontrado
4. ~~Qdrant local vs Cloud~~ → Migrado a Cloud
5. ~~Vector "dense" no existe~~ → Cambiado a vector unnamed

### EN PROGRESO ⏳
1. **Test Salamandra Cloud** - Ejecutándose ahora
2. **VPS slow response** - 3-5min/pregunta (aceptable para MVP)

### PENDIENTES 🔴
1. **OLLAMA_KEEP_ALIVE=-1** - NO configurado en VPS
2. **FastAPI wrapper** - Podría eliminarse (overhead 10-20%)
3. **num_ctx optimization** - Usuario decidió mantener 4096
4. **VPS upgrade** - €20/mes rechazado (sin presupuesto)

---

## 📈 MÉTRICAS COMPARATIVAS

### Evaluación Claude Judge (102 preguntas)

| Modelo | Mejor % | Score Avg | Errores Graves | Legalidad |
|:---|---:|---:|---:|:---:|
| DeepSeek | 67% | 8.42/10 | 3% | Excelente |
| Groq Llama | 15% | 7.18/10 | 12% | Buena |
| Groq GPT | 12% | 6.95/10 | 18% | Aceptable |
| **Salamandra** | **6%** | **3.87/10** | **64%** | **Grave** |

### Salamandra Detalle
- **Problemas:** Razonamiento vago, citas inventadas, errores jurídicos
- **Causa:** RAG context no recibido (script equivocado)
- **Expectativa con RAG:** 6% → 30-40% (estimado)

---

## 🔄 PRÓXIMOS PASOS INMEDIATOS

### Test en Progreso
1. ✅ Script `salamandra_FINAL.py` ejecutándose
2. ⏳ Esperando resultados (2 exams, ~20 mins)
3. ⏳ Comparar calidad con RAG context

### Si Test Exitoso
1. Ejecutar batch completo 102 preguntas
2. Re-evaluar con Claude Judge
3. Comparar DeepSeek vs Salamandra+RAG

### Optimizaciones Gratis Pendientes
1. Configurar `OLLAMA_KEEP_ALIVE=-1` en VPS systemd
2. Considerar eliminar FastAPI wrapper (Ollama directo)
3. Test con `num_ctx=2048` (si usuario aprueba)

---

## 🧠 LECCIONES APRENDIDAS

### Técnicas
1. **Siempre verify scripts ejecutados** - Error costó 1 día debugging
2. **Qdrant Cloud ≠ Local** - Vector naming diferente
3. **8GB RAM funciona** pero swapping mata performance
4. **Q4_K_M quantization** ya óptima para CPU

### Metodológicas
1. **Git commits más frecuentes** - Difícil rastrear cambios
2. **Documentar VPS config** desde inicio
3. **Test scripts incrementally** antes de batch completo

### Bussiness
1. **Budget constraints** requieren máxima optimización
2. **VPS already paid** hace upgrade difícil decisión
3. **MVP quality** acepta 3-5min latency para testing

---

## 📝 ESTADO DOCUMENTACIÓN

### Docs Actualizados
- ✅ `.env.backend` - Qdrant Cloud activo
- ✅ `task.md` - Hallazgos críticos incluidos
- ⏳ `VPS_AUDIT_050126.md` - Necesita actualización
- ⏳ `VPS_INFRASTRUCTURE_AUDIT.md` - Necesita actualización
- ⏳ `PLAN_DESARROLLO_2026.md` - Info obsoleta sobre estimaciones

### Docs Pendientes Corregir
1. Quitar "VPS no viable" de evaluaciones (SÍ viable con optimizaciones)
2. Actualizar recomendaciones RAM (8GB funcional, 16GB recomendado)
3. Añadir sección Qdrant Cloud vs Local
4. Documentar vector naming issue

---

## 🎬 CONCLUSIÓN

**Situación actual:** Sistema funcionando con configuración mejorada.  
**Blocker principal:** Velocidad VPS (3-5min) aceptable para testing, no para producción.  
**Decisión clave:** Posponer upgrade VPS hasta validar calidad Salamandra+RAG.  
**Siguiente hito:** Comparativa final DeepSeek vs Salamandra con RAG completo.

---

**Última actualización:** 07/01/2026 15:10  
**Autor:** Antigravity AI Agent + Usuario  
**Próxima revisión:** Tras completar test actual

**FIN MEMORIA**
