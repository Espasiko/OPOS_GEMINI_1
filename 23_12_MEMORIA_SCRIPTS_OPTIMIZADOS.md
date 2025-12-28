# 📋 MEMORIA TÉCNICA: Scripts de Generación Optimizados

**Fecha:** 23 Diciembre 2025  
**Proyecto:** OpositAIA - Dataset Generator  
**Objetivo:** Implementar scripts de generación premium con verificación BOE/RAG integrada

---

## 🎯 RESUMEN EJECUTIVO

Se han creado **4 scripts optimizados** para generar contenido premium de alta calidad con verificación automática de citas legales y URLs BOE durante el proceso de generación (no post-procesamiento).

### ✅ Scripts Creados

1. **`generate_razonamiento_deepseek_verified.py`** - Razonamientos jurídicos complejos
2. **`generate_dialogos_mistral_verified.py`** - Diálogos con citas BOE
3. **`generate_simulacros_groq_twopass.py`** - Simulacros de examen
4. **`audit_generated_pilot.py`** - Auditor automático de calidad

---

## 📁 UBICACIÓN DE LOS SCRIPTS

### Scripts de Generación

```
/home/spas/OPOS_GEMINI_1/dataset_generator/
├── generate_razonamiento_deepseek_verified.py  (🔴 DeepSeek V3.2)
├── generate_dialogos_mistral_verified.py       (🟡 Mistral Agents)
├── generate_simulacros_groq_twopass.py         (🟢 Groq 2-pass)
└── audit_generated_pilot.py                    (🔍 Auditor)
```

### Directorio de Salida

```
/home/spas/OPOS_GEMINI_1/dataset_generator/golden_dataset/pilot_verified_23_12/
├── razonamientos_deepseek_YYYYMMDD_HHMMSS.jsonl
├── dialogos_mistral_YYYYMMDD_HHMMSS.jsonl
├── simulacros_groq_YYYYMMDD_HHMMSS.jsonl
└── AUDIT_REPORT_YYYYMMDD_HHMMSS.md
```

---

## 🔧 SCRIPT 1: Razonamientos Jurídicos (DeepSeek V3.2)

### Características Técnicas

- **Modelo:** `deepseek-chat` (DeepSeek V3.2)
- **Capacidades:**
  - ✅ Reasoning nativo (Chain-of-Thought integrado)
  - ✅ Prompt caching (ahorro ~70% en tokens de contexto)
  - ✅ Tools: `buscar_rag` + `verificar_articulo`
  - ✅ Verificación DURANTE generación

### Contenido Generado

- **Tipo:** Razonamientos jurídicos complejos
- **Cantidad Piloto:** 10 casos
- **Formato JSON:**
  ```json
  {
    "id": "DEEPSEEK-RAZON-001",
    "tema": "...",
    "escenario": "...",
    "pregunta": "...",
    "razonamiento": [
      {
        "paso": 1,
        "titulo": "...",
        "contenido": "...",
        "citas": ["Art. X Ley Y"]
      }
    ],
    "solucion": "...",
    "articulos_citados": [
      {
        "articulo": "X",
        "ley": "Y",
        "url_boe": "https://..."
      }
    ],
    "generated_at": "...",
    "model": "deepseek-v3.2",
    "iterations": 3
  }
  ```

### Estrategia de Verificación

1. **Antes de generar:** Llama a `buscar_rag` para obtener contexto legal con URLs BOE reales
2. **Durante generación:** Llama a `verificar_articulo` para cada artículo citado
3. **Resultado:** Solo puede citar artículos que existen en PostgreSQL

### Temas del Piloto

1. Trabajador con IT que supera 365 días y pasa a IP
2. Compatibilidad entre pensión de jubilación parcial y trabajo
3. Cálculo de base reguladora en jubilación anticipada
4. Extinción de prestación por desempleo por sanción
5. Incapacidad permanente total vs absoluta
6. Prestación de maternidad y paternidad 2024
7. Recargo de prestaciones por falta de medidas
8. Jubilación activa: requisitos y compatibilidad
9. Prestación por cese de actividad de autónomos
10. Revisión de grado de incapacidad

### Coste Estimado

- **Tokens por caso:** ~8,000 tokens
- **Coste por caso:** ~$0.02
- **Total 10 casos:** **$0.20**

---

## 🔧 SCRIPT 2: Diálogos con Citas BOE (Mistral Agents)

### Características Técnicas

- **Modelo:** Mistral Agents API
- **Agent ID:** `ag_019ad601946d7323a81c544229de40a1`
- **Capacidades:**
  - ✅ Agents API con tools pre-configurados
  - ✅ Pausas automáticas (rate limiting)
  - ✅ **Gratis** (por ahora)
  - ✅ Ya probado con éxito en `generate_qa_mistral_real.py`

### Contenido Generado

- **Tipo:** Diálogos usuario-asistente con citas BOE
- **Cantidad Piloto:** 20 diálogos
- **Formato JSON:**
  ```json
  {
    "id": "MISTRAL-DIALOG-001",
    "pregunta_usuario": "¿Puedo jubilarme a los 63 años?",
    "respuesta_asistente": "Sí, mediante jubilación anticipada voluntaria (Art. 207 LGSS, BOE: https://...)",
    "iterations": 2,
    "generated_at": "...",
    "model": "mistral-agent"
  }
  ```

### Estrategia de Verificación

1. **Automática:** El agente usa `buscar_rag` automáticamente
2. **Nosotros ejecutamos:** La tool y devolvemos resultado con URLs
3. **Resultado:** El agente solo puede citar lo que está en el resultado RAG

### Por Qué Diálogos

- ✅ Tipo de contenido que **FALTA** en el dataset actual
- ✅ Requiere URLs y citas (verificables)
- ✅ Mistral es excelente en conversación
- ✅ Útil para fine-tuning de chatbot

### Temas del Piloto

1. ¿Puedo jubilarme a los 63 años?
2. ¿Cuánto dura la incapacidad temporal?
3. ¿Qué diferencia hay entre IP parcial y total?
4. ¿Cómo se calcula la base reguladora de jubilación?
5. ¿Puedo cobrar paro si renuncio voluntariamente?
6. ¿Qué es la jubilación activa?
7. ¿Cuándo puedo solicitar la pensión de viudedad?
8. ¿Qué requisitos tiene la prestación de maternidad?
9. ¿Puedo compatibilizar pensión y trabajo?
10. ¿Qué es el recargo de prestaciones?
11. ¿Cómo funciona la jubilación parcial?
12. ¿Qué pasa si supero los 365 días de IT?
13. ¿Cuánto cobro de prestación por desempleo?
14. ¿Qué es la incapacidad permanente absoluta?
15. ¿Puedo revisar mi grado de incapacidad?
16. ¿Qué es la prestación por cese de actividad?
17. ¿Cómo se calcula la pensión de orfandad?
18. ¿Qué es la jubilación anticipada voluntaria?
19. ¿Puedo cobrar dos pensiones a la vez?
20. ¿Qué requisitos tiene la pensión no contributiva?

### Coste Estimado

- **Total 20 diálogos:** **$0.00 (GRATIS)**

---

## 🔧 SCRIPT 3: Simulacros de Examen (Groq 2-Pass)

### Características Técnicas

- **Modelo:** `llama-3.3-70b-versatile` (Groq)
- **Estrategia:** 2-Pass (Arquitecto → Redactor)
- **Capacidades:**
  - ✅ Muy rápido (tokens/segundo)
  - ✅ Muy barato ($0.001/pregunta)
  - ✅ Tools: `buscar_rag` + `verificar_articulo`

### Contenido Generado

- **Tipo:** Bloques de simulacro (10 preguntas tipo test)
- **Cantidad Piloto:** 5 bloques = **50 preguntas**
- **Formato JSON:**
  ```json
  {
    "id": "GROQ-SIMUL-001",
    "tema": "...",
    "preguntas": [
      {
        "numero": 1,
        "pregunta": "...",
        "opciones": {
          "a": "...",
          "b": "...",
          "c": "...",
          "d": "..."
        },
        "respuesta_correcta": "a",
        "articulo_boe": "Art. X Ley Y",
        "url_boe": "https://..."
      }
    ],
    "generated_at": "...",
    "model": "groq-2pass",
    "iterations_p1": 2,
    "iterations_p2": 3
  }
  ```

### Estrategia 2-Pass

#### PASS 1: Arquitecto (Thinking)

- **Objetivo:** Diseñar las 10 preguntas
- **Tools:** `buscar_rag` (obtiene contexto legal)
- **Output:** Texto plano con diseño de preguntas
- **Temperature:** 0.8 (creativo)

#### PASS 2: Redactor (Execution)

- **Objetivo:** Convertir diseño a JSON
- **Tools:** `verificar_articulo` (verifica cada cita)
- **Output:** JSON estructurado
- **Temperature:** 0.3 (preciso)

### Temas del Piloto

1. Incapacidad temporal: duración, requisitos y extinción
2. Jubilación ordinaria y anticipada: requisitos y cálculo
3. Prestación por desempleo: requisitos, cuantía y duración
4. Incapacidad permanente: grados y procedimiento
5. Prestaciones de maternidad, paternidad y cuidado de menores

### Coste Estimado

- **Tokens por bloque:** ~2,000 tokens
- **Coste por bloque:** ~$0.01
- **Total 5 bloques (50 preguntas):** **$0.05**

---

## 🔧 SCRIPT 4: Auditor Automático

### Características Técnicas

- **Archivo:** `audit_generated_pilot.py`
- **Función:** Verificar calidad del contenido generado

### Verificaciones Realizadas

1. **Extracción de citas legales** (regex + NER)
2. **Verificación en PostgreSQL** (cada artículo citado)
3. **Verificación de URLs BOE** (HTTP HEAD request)
4. **Cálculo de score de calidad** (0-100)

### Formato del Reporte

```markdown
# 🔍 REPORTE DE AUDITORÍA

## 📊 RESUMEN GLOBAL

- Total items auditados: 80
- Total citas encontradas: 150
- Citas verificadas en BD: 145 (96.7%)
- Total URLs BOE: 120
- URLs válidas: 118 (98.3%)

### 🎯 SCORE DE CALIDAD: 97.2/100

✅ EXCELENTE - Dataset listo para fine-tuning

## 📁 DETALLES POR ARCHIVO

### razonamientos_deepseek_20251223_210000.jsonl
- Items: 10
- Citas verificadas: 45/47 (95.7%)
- URLs válidas: 40/40 (100%)

...
```

### Criterios de Calidad

- ✅ **90-100:** EXCELENTE - Listo para fine-tuning
- ⚠️ **70-89:** BUENO - Revisar citas no verificadas
- ❌ **<70:** INSUFICIENTE - Requiere regeneración

---

## 🏗️ ARQUITECTURA RAG CONFIRMADA

### Endpoint: `/api/rag/search`

**Backend:** FastAPI corriendo en `http://127.0.0.1:8000`

**Request:**
```json
{
  "query": "artículo 215 LGSS",
  "top_k": 5,
  "min_score": 0.3
}
```

**Response:**
```json
{
  "query": "...",
  "documents": [
    {
      "id": "uuid",
      "score": 0.95,
      "content": "Texto del artículo...",
      "metadata": {
        "norma_nombre": "Ley General de la Seguridad Social",
        "url": "https://www.boe.es/...",
        "articulo": "215",
        "titulo": "..."
      }
    }
  ],
  "context": "Contexto formateado para LLM",
  "metadata": {
    "top_score": 0.95,
    "search_time_ms": 45
  }
}
```

### Infraestructura

- **Qdrant:** `localhost:6333` (Docker local)
  - **Puntos indexados:** 17,403
  - **Embedding Model:** `pablosi/bge-m3-spa-law-qa-trained-2`
- **PostgreSQL:** `localhost:5432`
  - **Leyes completas:** 10,901
  - **Con metadatos y URLs BOE**

---

## 🔒 ESTRATEGIA DE VERIFICACIÓN INTEGRADA

### Concepto Clave: Tools que Fallan

```python
def verificar_articulo_boe(articulo: str, ley: str) -> dict:
    """
    Verifica artículo en PostgreSQL.
    Si NO existe, devuelve error que el modelo ve.
    """
    response = requests.post(
        f"{BACKEND_URL}/api/rag/search",
        json={"query": f"artículo {articulo} {ley}", "top_k": 1, "min_score": 0.5}
    )
    
    docs = response.json().get("documents", [])
    
    if not docs:
        return {
            "error": f"❌ Artículo {articulo} de {ley} NO ENCONTRADO en BD",
            "exists": False
        }
    
    return {
        "exists": True,
        "articulo": articulo,
        "ley": ley,
        "url_boe": docs[0]["metadata"]["url"],
        "content_preview": docs[0]["content"][:200]
    }
```

### Resultado

- ✅ Si el modelo intenta citar un artículo inventado, la tool devuelve **error**
- ✅ El modelo **ve el error** y NO puede continuar con ese artículo
- ✅ Solo puede usar artículos que **existen en BD**

### Diferencia con Verificación Post-Procesamiento

| Aspecto | Post-Procesamiento | Verificación Integrada |
|---------|-------------------|------------------------|
| **Cuándo** | Después de generar | Durante generación |
| **Coste** | Paga por alucinaciones | Solo paga por contenido válido |
| **Calidad** | Requiere regenerar | Genera correcto desde el inicio |
| **Eficiencia** | Baja (2 pasos) | Alta (1 paso) |

---

## 💰 COSTE TOTAL DEL PILOTO

| Script | Items | Modelo | Coste |
|--------|-------|--------|-------|
| DeepSeek | 10 razonamientos | deepseek-v3.2 | **$0.20** |
| Mistral | 20 diálogos | mistral-agent | **$0.00** |
| Groq | 50 preguntas | llama-3.3-70b | **$0.05** |
| **TOTAL** | **80 items** | - | **$0.25** |

**Conclusión:** Piloto muy económico (<$0.30)

---

## 📋 INSTRUCCIONES DE EJECUCIÓN

### Paso 1: Instalar Dependencias

```bash
cd /home/spas/OPOS_GEMINI_1
source .venv/bin/activate
pip install openai mistralai groq python-dotenv
```

### Paso 2: Verificar Backend

```bash
# Verificar que FastAPI está corriendo
curl http://127.0.0.1:8000/health

# Si no está corriendo:
cd /home/spas/OPOS_GEMINI_1/backend
source .venv/bin/activate
uvicorn main:app --reload
```

### Paso 3: Ejecutar Scripts de Generación

```bash
cd /home/spas/OPOS_GEMINI_1/dataset_generator

# Script 1: DeepSeek (10 razonamientos)
python3 generate_razonamiento_deepseek_verified.py

# Script 2: Mistral (20 diálogos)
python3 generate_dialogos_mistral_verified.py

# Script 3: Groq (50 preguntas)
python3 generate_simulacros_groq_twopass.py
```

### Paso 4: Auditar Resultados

```bash
# Ejecutar auditor automático
python3 audit_generated_pilot.py

# Ver reporte
cat golden_dataset/pilot_verified_23_12/AUDIT_REPORT_*.md
```

---

## ✅ CRITERIOS DE ÉXITO

1. ✅ **100% de artículos verificados** en PostgreSQL
2. ✅ **100% de URLs BOE válidas** (HTTP 200)
3. ✅ **Score de calidad >90%** en auditoría
4. ✅ **0 alucinaciones** detectadas
5. ✅ **Contenido diverso** (razonamientos + diálogos + simulacros)

---

## 🚀 PRÓXIMOS PASOS

### Fase 1: Validación del Piloto (AHORA)

1. ✅ Ejecutar los 3 scripts de generación
2. ✅ Ejecutar auditor automático
3. ✅ Revisar reporte de calidad
4. ✅ Validación manual de 3 items aleatorios

### Fase 2: Escalado a Producción (SI CALIDAD >90%)

1. **Expandir temas:**
   - Razonamientos: 10 → 236 casos
   - Diálogos: 20 → 200 diálogos
   - Simulacros: 50 → 1000 preguntas

2. **Ejecutar en batch:**
   - Usar Groq Batch API para simulacros
   - Usar DeepSeek con prompt caching para razonamientos
   - Usar Mistral Agents para diálogos

3. **Auditoría continua:**
   - Ejecutar auditor después de cada batch
   - Monitorear score de calidad
   - Regenerar si score <90%

### Fase 3: Consolidación Final

1. **Unificar datasets:**
   - Consolidar piloto + producción
   - Deduplicar por hash
   - Normalizar a formato Alpaca

2. **Crear Golden Dataset:**
   - `GOLDEN_DATASET_VERIFIED_2025.jsonl`
   - Solo contenido con score >95%
   - Listo para fine-tuning

---

## 📊 ESTADO ACTUAL DEL PROYECTO

### ✅ Completado

- [x] Análisis de capacidades de modelos (DeepSeek, Groq, Mistral)
- [x] Diseño de arquitectura de verificación integrada
- [x] Creación de 3 scripts de generación optimizados
- [x] Creación de auditor automático
- [x] Documentación completa (plan + memoria)

### ⏳ Pendiente

- [ ] Instalar dependencias (`openai`, `mistralai`, `groq`)
- [ ] Ejecutar scripts de generación piloto
- [ ] Auditar resultados
- [ ] Validar calidad (score >90%)
- [ ] Escalar a producción si calidad es buena

### 🎯 Objetivo Final

**Dataset Golden Verificado:**
- **Cantidad:** ~2,500 items de alta calidad
- **Tipos:** Razonamientos + Diálogos + Simulacros + Q&A + Esquemas
- **Calidad:** 100% artículos verificados, 0 alucinaciones
- **Listo para:** Fine-tuning de modelo especializado en Seguridad Social

---

## 📚 REFERENCIAS

### Scripts Creados

1. [`generate_razonamiento_deepseek_verified.py`](file:///home/spas/OPOS_GEMINI_1/dataset_generator/generate_razonamiento_deepseek_verified.py)
2. [`generate_dialogos_mistral_verified.py`](file:///home/spas/OPOS_GEMINI_1/dataset_generator/generate_dialogos_mistral_verified.py)
3. [`generate_simulacros_groq_twopass.py`](file:///home/spas/OPOS_GEMINI_1/dataset_generator/generate_simulacros_groq_twopass.py)
4. [`audit_generated_pilot.py`](file:///home/spas/OPOS_GEMINI_1/dataset_generator/audit_generated_pilot.py)

### Documentación

- [Plan de Implementación](file:///home/spas/.gemini/antigravity/brain/cbbd51fa-e58b-4fa9-b13f-dcbd5697c4e9/implementation_plan.md)
- [Análisis de Capacidades de Modelos](file:///home/spas/OPOS_GEMINI_1/ANALISIS_CAPACIDADES_MODELOS.md)
- [Auditoría de Verificación](file:///home/spas/OPOS_GEMINI_1/AUDITORIA_VERIFICACION_DATASET.md)

### Scripts de Referencia

- [`generate_qa_mistral_real.py`](file:///home/spas/OPOS_GEMINI_1/dataset_generator/archive/scripts_root/generate_qa_mistral_real.py) - Script exitoso con Mistral Agents
- [`consolidate_FORENSIC_MASTER.py`](file:///home/spas/OPOS_GEMINI_1/dataset_generator/consolidate_FORENSIC_MASTER.py) - Consolidación forense

---

**Fin de la Memoria Técnica**  
**Fecha:** 23 Diciembre 2025 21:15  
**Estado:** ✅ Scripts creados y documentados - Listos para ejecutar
