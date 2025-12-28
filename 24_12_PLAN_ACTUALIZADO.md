# 🎯 PLAN CORREGIDO FINAL - Oposiciones AGE y Seguridad Social 2025-2026

**Fecha:** 23 Diciembre 2025 23:30  
**Documento fuente:** [`Plan_age_ss_perpl_2025.txt`](file:///home/spas/OPOS_GEMINI_1/gastos_%20tokens/Plan_age_ss_perpl_2025.txt)  
**Estado:** Plan corregido con verificaciones reales

---

## ⚠️ CORRECCIONES CRÍTICAS APLICADAS

### 1. Modelo de Embeddings - CORREGIDO ✅

**❌ INCORRECTO (en plan anterior):** RoBERTalex  
**✅ CORRECTO:** `pablosi/bge-m3-spa-law-qa-trained-2`

- **Dimensiones:** 1024
- **Ubicación local:** `~/.cache/huggingface/hub/models--pablosi--bge-m3-spa-law-qa-trained-2`
- **Tiempo de carga:** 2.22s
- **Usado en:** Backend RAG Agent v2, MCP Server, todos los scripts de generación
- **Fuente:** [RESUMEN_SESION_RAG_19_12.md](file:///home/spas/OPOS_GEMINI_1/RESUMEN_SESION_RAG_19_12.md)

### 2. Arquitectura RAG Actual - VERIFICADA ✅

**Sistema RAG de 4 Capas** (no 5 capas como se sugirió):

1. **Capa 1:** Constituciones y marcos legales
2. **Capa 2:** Leyes específicas BOE (13 leyes principales)
3. **Capa 3:** Jurisprudencia y resoluciones
4. **Capa 4:** Material de estudio y exámenes oficiales

**Estrategia de indexación:**
- ✅ **Embeddings por artículos/chunks** (no leyes completas)
- ✅ **XML + metadatos** en PostgreSQL
- ✅ **Vectores** en Qdrant (1024 dims con pablosi)
- ✅ **Leyes completas** en PostgreSQL para contexto

**Fuente:** [1_PLAN_DESARROLLO_RAG_COMPLETO.md](file:///home/spas/OPOS_GEMINI_1/docs/02_planes/1_PLAN_DESARROLLO_RAG_COMPLETO.md)

### 3. Scripts de Mistral Local - ENCONTRADOS ✅

**Scripts disponibles para trabajo nocturno:**

1. **`generar_qa_mistral_local.py`**
   - Generador de Q&A con Ollama
   - Usa Mistral local

2. **`generar_qa_mistral_local_20.py`**
   - Genera 20 Q&A con Mistral Local

3. **`generate_premium_mistral_local.py`**
   - Generación premium con estrategia 2-pass
   - Arquitecto + Redactor
   - Incluye RAG y verificación

**Ubicación:** `/home/spas/OPOS_GEMINI_1/dataset_generator/`

**Modificaciones necesarias:**
- ✅ Integrar RAG (ya tienen estructura)
- ✅ Añadir CoT forzado
- ✅ Implementar pausas para no quemar equipo
- ✅ Usar verificación BOE/Qdrant

---

## 📊 ESTADO REAL DEL SISTEMA

### Leyes Indexadas - VERIFICACIÓN PENDIENTE

**⚠️ IMPORTANTE:** No se pudo verificar directamente en PostgreSQL (tabla `leyes` no existe con esa estructura).

**Según documentación:**
- ✅ 13 leyes principales indexadas
- ✅ 2,433 chunks totales
- ⚠️ Estructura real en PostgreSQL puede ser diferente

**Acción requerida:**
1. Verificar estructura real de PostgreSQL
2. Consultar Qdrant directamente para ver colecciones
3. Confirmar qué leyes están realmente indexadas

### Dataset Premium - ESTADO REAL

**Según `analyze_dataset_gaps.py`:**
- ❌ **0/250 items** en `golden_dataset/`
- ⏳ **80 items en generación** (piloto actual)
- 🎯 **Objetivo:** 2,500-5,500 items (según presupuesto)

**Nota:** Puede haber items sin verificar que se pueden enriquecer.

---

## 🚀 ROADMAP CORREGIDO

### Fase 1: Verificación y Preparación (1-2 días)

**1.1. Verificar Estado Real del RAG**
- [ ] Consultar Qdrant: `curl http://localhost:6333/collections`
- [ ] Verificar estructura PostgreSQL real
- [ ] Listar leyes realmente indexadas
- [ ] Verificar tamaño actual de Qdrant (no crear uno enorme)

**1.2. Identificar Leyes Faltantes**
- [ ] Comparar con temario oficial
- [ ] Priorizar según frecuencia en exámenes
- [ ] **Indexar TODAS las leyes faltantes** (no solo prioritarias)

**1.3. Identificar Reglamentos Faltantes**
- [ ] Revisar temario para reglamentos necesarios
- [ ] Añadir a lista de indexación

### Fase 2: Indexación Completa (1 semana)

**2.1. Leyes Principales Faltantes (10 leyes)**

1. 🔴 **Ley 47/2003** - General Presupuestaria
2. 🔴 **RDL 2/2015** - Estatuto Trabajadores
3. 🔴 **Ley 31/1995** - Prevención Riesgos Laborales
4. 🟠 **Ley 9/2017** - LCSP (Contratos)
5. 🟠 **LO 2/2012** - Estabilidad Presupuestaria
6. 🟡 **Ley 4/2023** - Igualdad Trans LGTBI
7. 🟡 **LO 3/2007** - Igualdad
8. 🟡 **LO 2/1982** - Tribunal de Cuentas
9. 🟡 **Ley 20/2007** - Estatuto Autónomo
10. 🟡 **LO 6/1985** - LOPJ

**2.2. Reglamentos Adicionales**
- [ ] Identificar reglamentos necesarios del temario
- [ ] Indexar con misma estrategia (chunks + metadatos)

### Fase 3: Generación de Dataset (2-3 semanas)

**3.1. Completar Piloto (EN CURSO)**
- ⏳ 10 razonamientos (DeepSeek) - EJECUTÁNDOSE
- ⏳ 20 diálogos (Mistral) - EJECUTÁNDOSE
- ⏳ 50 preguntas simulacro (Groq) - PENDIENTE

**3.2. Auditar Piloto**
- [ ] Ejecutar `audit_generated_pilot.py`
- [ ] Validación manual (3 items aleatorios)
- [ ] Decisión: ¿Escalar o ajustar?

**3.3. Generación Masiva (Objetivo: 2,500-5,500 items)**

**Distribución por tipo:**
- 500-1,000 razonamientos legales (DeepSeek)
- 500-1,000 diálogos Q&A (Mistral)
- 500-1,000 simulacros (Groq)
- 500-1,000 esquemas (Groq/DeepSeek)
- 500-1,000 comparativas (DeepSeek)
- 0-500 plazos (Groq)

**Trabajo Nocturno con Mistral Local:**
- [ ] Modificar `generate_premium_mistral_local.py`
- [ ] Integrar RAG + verificación BOE
- [ ] Añadir CoT forzado
- [ ] Implementar pausas (cada 50 items, esperar 5 min)
- [ ] Ejecutar por la noche (8-10 horas)
- [ ] Generar 200-300 items/noche

**Presupuesto:**
- DeepSeek: ~$10-15
- Groq: ~$5-8
- Mistral API: $0 (gratis)
- Mistral Local: $0 (gratis)
- **TOTAL: $15-25**

### Fase 4: Fine-tuning y Selección de Modelo (1 semana)

**4.1. Candidatos de Modelos**

**Modelos a evaluar:**
1. **Mistral 7B** (actual)
2. **Llama 3.1 8B** (nuevo)
3. **Qwen 2.5 7B** (nuevo)
4. **Gemma 2 9B** (nuevo)
5. **DeepSeek V3** (si es viable localmente)

**Criterios de selección:**
- Tamaño (debe caber en GPU local)
- Calidad en español legal
- Velocidad de inferencia
- Facilidad de fine-tuning con Unsloth

**4.2. Fine-tuning**
- [ ] Preparar dataset en formato Alpaca
- [ ] Fine-tuning con Unsloth (LoRA/QLoRA)
- [ ] Validación en conjunto de test (10% del dataset)
- [ ] Métricas: Perplexity, BLEU, ROUGE, validación humana

### Fase 5: Validación Humana (1 semana)

**5.1. Validación por Humanos**
- [ ] Seleccionar 100 items aleatorios
- [ ] Validar respuestas del modelo fine-tuneado
- [ ] Comparar con modelo base
- [ ] Identificar errores y patrones

**5.2. Iteración**
- [ ] Corregir errores identificados
- [ ] Re-fine-tuning si es necesario
- [ ] Validación final

### Fase 6: Preparación para Producción (1 semana)

**6.1. Revisión de Código**
- [ ] Refactorizar scripts de generación
- [ ] Limpiar código legacy
- [ ] Documentar funciones críticas

**6.2. Dockerización**
- [ ] Dockerizar backend
- [ ] Dockerizar frontend
- [ ] Dockerizar modelo fine-tuneado
- [ ] Docker Compose para todo el stack

**6.3. Testing**
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Tests de carga
- [ ] Tests de seguridad

**6.4. Deployment**
- [ ] Configurar CI/CD
- [ ] Deploy a staging
- [ ] Validación en staging
- [ ] Deploy a producción

---

## ❌ CAPAS NO VIABLES (Eliminadas del Plan)

### Capa 3 - Doctrina Administrativista

**Problema:** ¿CÓMO DIABLOS VAS A CONSEGUIR ESTA INFORMACIÓN?

- Alonso Olea, Tortuero Plaza → Libros con copyright
- Comentarios desactualizados → No hay fuente pública

**Solución:** **ELIMINAR** de roadmap. No es viable sin violar copyright.

### Capa 4 - Procesos Selectivos Históricos

**Problema:** ¿DE DÓNDE VAS A SACAR ESTO?

- Exámenes 2023, 2024, 2025 → No están publicados oficialmente
- Qué se anuló y POR QUÉ → Información interna de tribunales

**Solución:** **ELIMINAR** de roadmap. Solo usar exámenes que tengamos legalmente.

**Alternativa viable:**
- Usar exámenes de academias (ya tenemos)
- Generar simulacros sintéticos con RAG
- Validar con opositores reales

---

## 📋 CHECKLIST FINAL

### Verificaciones Inmediatas (Mañana)

- [ ] Verificar Qdrant: `curl http://localhost:6333/collections`
- [ ] Verificar PostgreSQL: estructura real de tablas
- [ ] Listar leyes indexadas realmente
- [ ] Verificar tamaño actual de Qdrant
- [ ] Revisar scripts de Mistral local
- [ ] Verificar estado de piloto (80 items)

### Indexación (Próxima Semana)

- [ ] Indexar 10 leyes faltantes
- [ ] Indexar reglamentos necesarios
- [ ] Verificar chunks + metadatos
- [ ] Validar búsqueda en Qdrant

### Generación de Dataset (2-3 Semanas)

- [ ] Completar piloto (80 items)
- [ ] Auditar piloto
- [ ] Escalar a 2,500-5,500 items
- [ ] Trabajo nocturno con Mistral local
- [ ] Validar calidad continuamente

### Fine-tuning (1 Semana)

- [ ] Evaluar 5 modelos candidatos
- [ ] Seleccionar mejor modelo
- [ ] Fine-tuning con Unsloth
- [ ] Validación en test set

### Validación Humana (1 Semana)

- [ ] 100 items aleatorios
- [ ] Comparar con modelo base
- [ ] Iteración si es necesario

### Producción (1 Semana)

- [ ] Refactorizar código
- [ ] Dockerizar todo
- [ ] Testing completo
- [ ] Deploy a producción

---

## 💰 PRESUPUESTO REALISTA

| Fase | Coste |
|------|-------|
| Indexación | $0 (scripts propios) |
| Piloto (80 items) | $0.25 |
| Generación masiva (2,500-5,500 items) | $15-25 |
| Fine-tuning | $0 (local con Unsloth) |
| Validación | $0 (manual) |
| Infraestructura | $0 (local) |
| **TOTAL** | **$15-25** |

**Nota:** Presupuesto muy ajustado gracias a Mistral local (gratis) y Groq (muy barato).

---

## 🎯 OBJETIVOS REALISTAS

### Corto Plazo (1 Mes)

- ✅ 13 leyes principales indexadas
- ✅ 10 leyes adicionales indexadas
- ✅ 2,500-5,500 items de dataset verificados
- ✅ Modelo fine-tuneado y validado

### Medio Plazo (3 Meses)

- ✅ App en producción
- ✅ 100 usuarios beta
- ✅ Feedback y mejoras iterativas

### Largo Plazo (6 Meses)

- ✅ 1,000+ usuarios activos
- ✅ Modelo v2 con más datos
- ✅ Expansión a otras oposiciones

---

## 📚 DOCUMENTOS DE REFERENCIA

- [Plan_age_ss_perpl_2025.txt](file:///home/spas/OPOS_GEMINI_1/gastos_%20tokens/Plan_age_ss_perpl_2025.txt) - Plan oficial completo
- [1_PLAN_DESARROLLO_RAG_COMPLETO.md](file:///home/spas/OPOS_GEMINI_1/docs/02_planes/1_PLAN_DESARROLLO_RAG_COMPLETO.md) - Arquitectura RAG 4 capas
- [RESUMEN_SESION_RAG_19_12.md](file:///home/spas/OPOS_GEMINI_1/RESUMEN_SESION_RAG_19_12.md) - Modelo pablosi
- [23_12_ACTUAL_OPOS_PLAN.md](file:///home/spas/OPOS_GEMINI_1/23_12_ACTUAL_OPOS_PLAN.md) - Plan anterior (con errores)

---

**Estado:** ✅ Plan corregido y listo para revisión mañana  
**Próximo paso:** Verificar Qdrant y PostgreSQL, luego ejecutar indexación  
**Convocatoria objetivo:** 2026 - Tiempo suficiente para preparación completa
