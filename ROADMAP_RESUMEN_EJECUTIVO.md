# 🚀 ROADMAP EJECUTIVO: COMPLETAR RAG + FINE-TUNING
**Fecha:** 5 de diciembre de 2025  
**Versión:** 1.0  
**Estado:** 🟢 APROBADO PARA INICIO

---

## 📊 PANORAMA ACTUAL (5 DIC 2025)

### Capa 3 - CRÍTICO ❌
```
Estado Actual: 553 documentos (11% de lo necesario)
Necesario: 5,000+ documentos
DÉFICIT: 4,447 documentos
BLOQUEADOR: ⚠️ NO SE PUEDE AVANZAR SIN ESTO
```

### Capa 1 - LISTA PERO NO INDEXADA ⏳
```
Estado: Leyes identificadas, scripts listos, NO indexadas
Leyes: 13 principales + 4 faltantes
Acción requerida: Ejecutar `indexar_todas_las_leyes.py`
Tiempo estimado: 2-3 horas
```

### Capa 2 - NO EXISTE ❌
```
Estado: No implementada
Requerido: CENDOJ API, INSS scraper, BOE circulares
Prioritario: DESPUÉS de Capas 1 y 3
```

---

## 🎯 PLAN DE ACCIÓN: 8 SPRINTS (8 SEMANAS)

### **BLOQUER 1️⃣: SPRINT 0 - AUDITORÍA MATERIAL (1 semana) [INICIA AHORA]**

**🔴 CRÍTICO - Debe hacerse primero**

**Objetivo:** Identificar exactamente qué exámenes oficiales faltanTarea) y fuentes

**Entregas:**
- [ ] `FUENTES_EXAMENES_OFICIALES.md` (50+ URLs)
- [ ] `exam_downloader.py` (descarga automática)
- [ ] `GUIA_INTEGRACION_CAPA_3.md` (procedimientos)
- [ ] Mínimo 20 exámenes oficiales descargados

**Resultado:** Base de datos de todos los exámenes a indexar

**Siguiente paso:** Sprint 1

---

### **BLOQUER 2️⃣: SPRINT 1 - INTEGRACIÓN EXÁMENES OFICIALES (1 semana)**

**Objetivo:** Indexar exámenes descargados en Capa 3

**Tareas:**
- [ ] Procesar PDFs a JSON estructurado
- [ ] Extraer respuestas oficiales
- [ ] Indexar en Qdrant con metadatos
- [ ] Verificar búsquedas funcionan

**Entregas:**
- [ ] 40+ exámenes indexados
- [ ] Búsqueda por año/convocatoria funcionando
- [ ] Tests pasando

**Impacto:** Capa 3 pasa de 553 a 600+ documentos

**Siguiente paso:** Sprint 2

---

### **SPRINT 2: INDEXACIÓN CAPA 1 - LEYES BOE (2 semanas)**

**Objetivo:** Indexar 13 leyes principales en Capa 1

**Tareas:**
- [ ] Ejecutar `indexar_todas_las_leyes.py`
- [ ] Validar metadatos (artículos, títulos)
- [ ] Testing de búsqueda semántica
- [ ] Indexar las 4 leyes faltantes (LOPJ, LOTC, LOREG, Ley 34/2014)

**Entregas:**
- [ ] 13 leyes indexadas + 4 faltantes = 17 leyes totales
- [ ] Búsqueda por artículo funcionando
- [ ] Tests de precisión pasando

**Impacto:** Capa 1 completa

**Siguiente paso:** Sprint 3

---

### **SPRINT 3: FINE-TUNING DATASET GENERATOR (2 semanas)**

**Objetivo:** Generar 10K Q&A para fine-tuning con multi-agentes

**Tareas (Ver PROPUESTA_MULTI_AGENTES_FINETUNING.md):**
- [ ] Extractor de contenido (`content_extractor.py`)
- [ ] Clasificador de riesgo (`classifier.py`)
- [ ] Generador Q&A multi-agente:
  - Groq para simple (70%, gratis/económico)
  - Mistral para complejo (30%, legal)
  - Claude para verificar (5% muestra)
- [ ] Deduplicación y filtrado
- [ ] Output: `dataset_qa_10k_final.jsonl`

**Entregas:**
- [ ] 10,000 Q&A generadas
- [ ] Dataset verificado (92% confidence)
- [ ] Coste total < $20 USD
- [ ] Análisis de calidad completo

**Impacto:** Dataset listo para fine-tuning

**Siguiente paso:** Sprint 4 (paralelo con Sprint 2)

---

### **SPRINT 4: API JSON BOE (1 semana - OPCIONAL)**

**Objetivo:** Explorar API JSON de BOE para enriquecimiento de metadatos

**Tareas:**
- [ ] Investigar endpoints disponibles
- [ ] Crear parser de respuestas JSON
- [ ] Comparar PDF vs JSON
- [ ] Decidir estrategia de enriquecimiento

**Entregas:**
- [ ] POC con API JSON funcionando
- [ ] Documento de decisión arquitectónica
- [ ] (Puede omitirse si PDF es suficiente)

**Impacto:** Metadatos más ricos y confiables

**Siguiente paso:** Sprint 5

---

### **SPRINT 5: CAPA 2 - JURISPRUDENCIA (2 semanas)**

**Objetivo:** Indexar jurisprudencia y resoluciones

**Tareas:**
- [ ] Conectar API CENDOJ (sentencias)
- [ ] Scraper INSS (resoluciones, circulares)
- [ ] Procesar y chunking adaptado
- [ ] Indexar en Qdrant con referencias a Capa 1

**Entregas:**
- [ ] 1,000+ resoluciones indexadas
- [ ] Búsqueda cruzada (ley + jurisprudencia)
- [ ] Ejemplos de queries complejas

**Impacto:** Capa 2 implementada

**Siguiente paso:** Sprint 6

---

### **SPRINT 6: OPTIMIZACIÓN BÚSQUEDA (1 semana)**

**Objetivo:** Afinar sistema RAG para máxima precisión

**Tareas:**
- [ ] Implementar Hybrid Search (semántico + BM25)
- [ ] Ponderación de capas
- [ ] Re-ranking inteligente
- [ ] Testing de calidad con métricas MRR, NDCG

**Entregas:**
- [ ] Sistema búsqueda híbrida funcionando
- [ ] Métricas de evaluación
- [ ] Benchmarks de mejora

**Impacto:** +20-30% en precisión de búsqueda

**Siguiente paso:** Sprint 7

---

### **SPRINT 7: INTEGRACIÓN CON CHAT (1 semana)**

**Objetivo:** Conectar RAG con endpoints de chat

**Tareas:**
- [ ] Query expansion (reformular preguntas)
- [ ] Buscar en RAG antes de llamar LLM
- [ ] Prompt engineering mejorado
- [ ] Testing A/B con usuarios

**Entregas:**
- [ ] Chat con RAG funcionando
- [ ] Referencias correctas a leyes
- [ ] Feedback positivo de users

**Impacto:** Usuario final ve mejora dramática

**Siguiente paso:** Sprint 8

---

### **SPRINT 8: FINE-TUNING MODELO (2-3 semanas - OPCIONAL)**

**Objetivo:** Crear modelo Mistral especializado en SS+AGE

**Tareas:**
- [ ] Preparar dataset (del Sprint 3)
- [ ] Fine-tuning con LoRA en Colab
- [ ] Evaluación vs modelos base
- [ ] Deployment en Hugging Face

**Entregas:**
- [ ] Modelo fine-tuned publicado
- [ ] Endpoint funcionando
- [ ] 99% accuracy en test set

**Impacto:** Máxima precisión, modelo propietario

**Siguiente paso:** COMPLETADO ✅

---

## 📈 TIMELINE CONSOLIDADO

```
DICIEMBRE 2025:
├─ Semana 1 (5-12 dic): SPRINT 0 ⚠️ CRÍTICO
├─ Semana 2 (12-19 dic): SPRINT 1 ⚠️ CRÍTICO
└─ Semana 3 (19-26 dic): SPRINT 2 + 3 (paralelo)

ENERO 2026:
├─ Semana 1 (2-9 ene): SPRINT 3 (continuación) + 4
├─ Semana 2 (9-16 ene): SPRINT 5
├─ Semana 3 (16-23 ene): SPRINT 6
├─ Semana 4 (23-30 ene): SPRINT 7
└─ Semana 5+ (31 ene+): SPRINT 8 (opcional)

DURACIÓN TOTAL: 8 semanas (paralelos), 12 semanas (secuencial)
```

---

## 💰 ANÁLISIS ECONÓMICO COMPLETO

### Inversión por Sprint

```
SPRINT 0: $0 (solo desarrollo)
SPRINT 1: $0 (solo desarrollo)
SPRINT 2: $0 (solo desarrollo)
SPRINT 3: $16-20 USD (Groq Free + Mistral API + Claude)
SPRINT 4: $0 (solo investigación)
SPRINT 5: $0 (solo desarrollo, APIs públicas)
SPRINT 6: $0 (solo desarrollo)
SPRINT 7: $0 (solo desarrollo)
SPRINT 8: $0 (Colab gratuito, Hugging Face free)

TOTAL INVERSIÓN: ~$20 USD
```

### Break-even Analysis
```
Modelo propietario fine-tuned:
├─ Costo desarrollo: ~$20 USD
├─ Tiempo total: 8-12 semanas
├─ Ventaja: Independencia de APIs externas
├─ Ahorro mensual vs APIs: $200-500 USD
├─ Break-even: < 1 mes

ROI: 10-25x en 3 meses
```

---

## 📋 DOCUMENTOS REQUERIDOS (YA CREADOS)

✅ `PLAN_DESARROLLO_RAG_COMPLETO.md` - Plan detallado 8 sprints
✅ `SPRINT_0_AUDIT_5_DIC_2025.md` - Auditoría material Capa 3
✅ `PROPUESTA_MULTI_AGENTES_FINETUNING.md` - Pipeline generación dataset
🔲 `CONTRIBUTING.md` - A crear (Git + setup)
🔲 `GUIA_EXAMEN_OFICIAL.md` - A crear (Cómo usar exámenes)
🔲 `FUENTES_EXAMENES_OFICIALES.md` - A crear en Sprint 0

---

## ✅ CHECKLIST PREPARACIÓN

### Verificación Pre-Sprint
- [x] Backend y frontend corriendo
- [x] Qdrant Cloud accesible
- [x] Bases de datos conectadas
- [x] Ollama corriendo (embeddings locales)
- [x] APIs configuradas (Groq, Mistral, Claude, Gemini)
- [x] Git tracking verificado
- [x] Scripts de indexación listos

### Antes de Iniciar Sprint 0
- [ ] Revisar `SPRINT_0_AUDIT_5_DIC_2025.md`
- [ ] Crear issue en GitHub con tareas
- [ ] Asignar recursos
- [ ] Configurar alertas para descargas

### Antes de Sprint 1
- [ ] Examenes oficiales descargados
- [ ] Fuentes documentadas
- [ ] Permisos de copyright verificados
- [ ] Plan de indexación aprobado

---

## 🎯 OBJETIVOS FINALES

### Al Completar Sprints 0-3 (4 semanas)
```
✅ Capa 3 completa: 643+ documentos
✅ Capa 1 indexada: 17 leyes
✅ Dataset generado: 10K Q&A
✅ Listo para fase de optimización
```

### Al Completar Sprints 4-7 (8 semanas total)
```
✅ Capa 2 implementada: Jurisprudencia
✅ Búsqueda híbrida: +25% precisión
✅ Chat con RAG: Funcionando en producción
✅ Ready para usuarios beta
```

### Al Completar Sprint 8 (12 semanas)
```
✅ Modelo fine-tuned: 99% accuracy
✅ Independencia de APIs externas
✅ Sistema RAG producción-ready
✅ Documentación completa
```

---

## 🚀 PRÓXIMOS PASOS INMEDIATOS

### Hoy (5 de diciembre)
1. ✅ Crear SPRINT_0_AUDIT
2. ✅ Crear PROPUESTA_MULTI_AGENTES
3. ✅ Crear este ROADMAP
4. 👉 **Siguiente: Iniciar SPRINT 0 mañana**

### Semana que viene
1. Completar Sprint 0
2. Publicar lista de exámenes a descargar
3. Crear scripts de descarga
4. Iniciar Sprint 1

### Fin de diciembre
1. Capa 3 con exámenes oficiales ✅
2. Capa 1 indexada ✅
3. Dataset 10K generado ✅
4. Ready para enero optimizaciones

---

## 📞 CONTACTO Y APOYO

**Preguntas sobre el plan:**
- Revisar `PLAN_DESARROLLO_RAG_COMPLETO.md` (404 líneas)

**Detalles técnicos Capa 3:**
- Revisar `SPRINT_0_AUDIT_5_DIC_2025.md`
- Revisar `FUENTES_EXAMENES_OFICIALES.md` (en Sprint 0)

**Pipeline dataset fine-tuning:**
- Revisar `PROPUESTA_MULTI_AGENTES_FINETUNING.md` (600+ líneas)
- Scripts: `backend/agents/qa_generator.py` etc.

**Arquitectura general:**
- Revisar `README.md` (actualizar)
- Revisar diagramas en `PLAN_DESARROLLO_RAG_COMPLETO.md`

---

**Documento creado:** 5 de diciembre de 2025  
**Versión:** 1.0 - Plan ejecutivo completo  
**Estado:** 🟢 LISTO PARA INICIAR SPRINT 0
