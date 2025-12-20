# 📊 Evaluación de Ideas para Dataset Q&A de Calidad Suprema

**Fecha**: 3 de Diciembre 2025  
**Contexto**: Generación de 5,000 Q&A para fine-tuning de modelo open-source (Mistral 7B) especializado en oposiciones de Seguridad Social y AGE

---

## ✅ **FORTALEZAS CLAVE** (Mantener y Aplicar)

### 1. **Enfoque "Quality First" (LIMA)**
- ✅ **EXCELENTE**: Priorizar 2,000-10,000 pares de alta calidad sobre millones con ruido
- ✅ **VALIDADO**: Paper LIMA (2023) demuestra que dataset pequeño pero perfecto > dataset masivo ruidoso
- ✅ **APLICABLE**: Reduce costes, tiempo y riesgo de catastrophic forgetting
- **Recomendación**: Mantener objetivo de 5,000 Q&A con validación estricta

### 2. **Pipeline Agentic (Extractor → Generador → Filtro)**
- ✅ **ARQUITECTURA SÓLIDA**: Separación clara de responsabilidades
- ✅ **TRAZABILIDAD**: Cada agente tiene función específica
- ✅ **ESCALABLE**: Batching de 50 artículos reduce latencia
- **Recomendación**: Implementar tal cual, añadiendo Agente de Diversidad

### 3. **Optimización de Costes**
- ✅ **BRILLANTE**: Usar DeepSeek V3 ($0.016 por 100 pares) vs GPT-4o
- ✅ **INFRAESTRUCTURA**: Aprovechar Qdrant + embeddings `littlejohn-ai/bge-m3-spa-law-qa`
- ✅ **BOE API**: Usar XML/JSON gratis vs parsear PDFs
- **Coste estimado total**: ~5-6€ para 5,000 Q&A

### 4. **Chain of Thought (CoT) Obligatorio**
- ✅ **CRÍTICO**: Razonamiento jurídico es más valioso que respuesta corta
- ✅ **BEST PRACTICE**: Mejora generalización del modelo
- **Recomendación**: Exigir 150-200 palabras de rationale antes de answer

### 5. **Formato JSONL Compatible**
- ✅ **ESTÁNDAR**: Compatible con Axolotl/Unsloth
- ✅ **CAMPOS MÍNIMOS**: question, answer, rationale, citations, source_articles, difficulty
- **Recomendación**: Usar script de conversión proporcionado

---

## ⚠️ **RIESGOS IDENTIFICADOS** (Mitigar)

### 1. **Sesgo en Generación de Preguntas**
- ❌ **PROBLEMA**: Modelos generan preguntas demasiado literales
- ✅ **SOLUCIÓN**: 
  - Incluir ejemplos de alto valor pedagógico en prompts
  - Añadir Agente de Diversidad para revisar distribución de tipos
  - Clasificar por nivel (fácil/medio/avanzado) y tipo (literal/aplicada/trampa/comparativa)

### 2. **Filtro RAG (Falsos Positivos/Negativos)**
- ❌ **PROBLEMA**: Puede aprobar preguntas ambiguas si embedding es similar pero no idéntico
- ✅ **SOLUCIÓN**:
  - Umbral de similitud estricto (score > 0.95)
  - Segundo filtro con modelo diferente (bge-m3)
  - Comparación semántica adicional

### 3. **Falta de Validación Humana**
- ❌ **PROBLEMA**: Depender solo de modelos perpetúa errores sistemáticos
- ✅ **SOLUCIÓN**:
  - Validación humana de muestra (100-250 preguntas)
  - Usar Label Studio o Argilla
  - Active learning: priorizar revisión de preguntas con menor confianza

### 4. **Catastrophic Forgetting en Fine-Tuning**
- ❌ **PROBLEMA**: Fine-tuning puede degradar rendimiento en tareas generales
- ✅ **SOLUCIÓN**:
  - Usar LoRA/QLoRA para limitar impacto en pesos originales
  - Evaluar en benchmark general (MMLU) antes y después
  - Monitorizar degradación

---

## 💡 **MEJORAS PROPUESTAS** (Implementar)

### 1. **Generación de Preguntas Multinivel**
```
Distribución sugerida:
- 40% Aplicadas (casos prácticos)
- 30% Literales (conocimiento directo)
- 20% Trampas (errores comunes)
- 10% Comparativas (relacionar artículos)
```

### 2. **Incorporar Datos Reales de Exámenes**
- Parsear exámenes pasados con OCR
- Usar como ejemplos en prompts del Generador
- Mantener estilo de preguntas oficiales

### 3. **Evaluación Automática del Dataset**
**Métricas propuestas**:
- **Diversidad**: Distancia semántica media entre preguntas
- **Coherencia**: Verificar que respuestas no contradigan texto legal
- **Utilidad**: Predicción de relevancia para examen AGE

### 4. **Pipeline de Mejora Continua**
- Modelo fine-tuneado genera nuevas preguntas
- Revisión humana con Argilla
- Añadir mejores al dataset
- Re-entrenar periódicamente

---

## 💰 **PLAN DE COSTES CON CRÉDITOS ACTUALES**

| Servicio | Crédito | Uso Propuesto | Coste Real |
|----------|---------|---------------|------------|
| **DeepSeek V3** | 2€ | Bulk generation (5,000 ítems) | ~1.5€ |
| **Mistral API** | - | 200 ítems difíciles | ~0.33€ |
| **Anthropic Claude** | 5€ | Validación final 50 ítems | ~3.5€ |
| **Nemotron Reward** | - | Scoring 5,000 ítems | ~0.5€ |
| **Fine-tuning local** | - | CPU 15-20h | ~0.3€ (electricidad) |
| **TOTAL** | | | **~6€** |

### Asignación Óptima de Créditos:
1. **DeepSeek (2€)**: Generar 5,000 Q&A base + distractores
2. **Mistral API**: 200 preguntas más complejas
3. **Anthropic (5€)**: Validación crítica de 50 ítems más difíciles
4. **Nemotron**: Scoring automático de todos los ítems

---

## 🖥️ **ENTRENAMIENTO LOCAL SIN GPU**

### ✅ **ES VIABLE** (Portátil 16GB RAM, CPU-only)

**Configuración Recomendada**:
- **Modelo**: Mixtral 8x7B Instruct (Q4_K_M)
- **Técnica**: QLoRA (reduce memoria a <8GB)
- **Herramienta**: Unsloth (acelera y reduce RAM 50%)
- **Tiempo**: 15-20 horas
- **Coste eléctrico**: ~0.3€

**Requisitos**:
```yaml
- bitsandbytes (cuantización 4-bit)
- Unsloth + QLoRA
- accelerate + deepspeed
- Batch size: 1
- Gradient accumulation: 4
```

**Rendimiento Esperado**:
- 0.3-0.5 tokens/s por core
- 2-3 tokens/s total
- Pérdida de accuracy: <2% vs GPU

---

## 🤖 **MODELOS OPEN-SOURCE RECOMENDADOS**

| Modelo | Tamaño | Ventajas | RAM Necesaria | Recomendación |
|--------|--------|----------|---------------|---------------|
| **Mixtral 8x7B** | 8×7B | ⭐⭐⭐ Mejor razonamiento español | 8GB (Q4) | **#1 OPCIÓN** |
| **Llama 3 8B** | 8B | ⭐⭐ Base sólida, comunidad grande | 8GB (Q4) | Alternativa segura |
| **Qwen 2.5 7B** | 7B | ⭐⭐ Buen español, 32k context | 7GB (Q4) | Opción eficiente |
| **Phi-3 Medium** | 3.8B | ⭐ Ultra-eficiente | 4GB (Q4) | Si RAM es crítica |

**Recomendación Final**: **Mixtral 8x7B Instruct (Q4_K_M)** como opción #1

---

## 📋 **HOJA DE RUTA RECOMENDADA**

### Fase 1: Preparación (1 día)
- ✅ Configurar pipeline BOE → Qdrant
- ✅ Indexar con bge-m3-spa-law-qa
- ✅ Crear prompts maestros

### Fase 2: Generación (2-3 horas)
- ✅ Batch de 500 ítems de prueba (DeepSeek)
- ✅ Scoring con Nemotron Reward
- ✅ Calibrar umbral de calidad

### Fase 3: Validación (4-6 horas)
- ✅ Revisión humana de 250 ítems
- ✅ Crítico con Mistral Large (200 ítems)
- ✅ Validación final con Claude (50 ítems)

### Fase 4: Expansión (2 horas)
- ✅ Generar 5,000 ítems completos
- ✅ Aplicar filtros y conversión a JSONL

### Fase 5: Fine-tuning (15-20 horas)
- ✅ Entrenar Mixtral 8x7B con Unsloth
- ✅ Evaluar en benchmark
- ✅ Ajustar hiperparámetros si necesario

### Fase 6: Despliegue (2 horas)
- ✅ FastAPI + Qdrant en VPS
- ✅ Arquitectura de agentes (Router, RAG, Critic)
- ✅ Monitoreo y mejora continua

---

## 🎯 **DECISIONES CLAVE**

### ✅ **MANTENER**:
1. Enfoque "Quality First" (5,000 Q&A)
2. Pipeline agentic (Extractor → Generador → Filtro)
3. DeepSeek para bulk generation
4. Nemotron Reward para scoring automático
5. Mixtral 8x7B como modelo base
6. Fine-tuning local con QLoRA
7. BOE API como fuente de verdad

### ⚠️ **MODIFICAR**:
1. Añadir Agente de Diversidad
2. Implementar segundo filtro RAG
3. Incluir validación humana (5-10%)
4. Clasificar preguntas por nivel y tipo
5. Usar active learning para priorizar revisión

### ❌ **EVITAR**:
1. Cambiar modelo de embeddings (ya tienes bge-m3-spa-law-qa)
2. Usar GPT-4o para bulk generation (muy caro)
3. Entrenar sin LoRA/QLoRA (riesgo de catastrophic forgetting)
4. Depender 100% de validación automática

---

## 📊 **COMPARATIVA DE OPCIONES**

### Opción A: Plan Propuesto (RECOMENDADO)
- **Coste**: ~6€
- **Calidad**: ⭐⭐⭐⭐⭐ (Suprema)
- **Tiempo**: 20-25 horas totales
- **Viabilidad**: ✅ Excelente

### Opción B: Solo Mistral API
- **Coste**: ~15-20€
- **Calidad**: ⭐⭐⭐⭐⭐ (Suprema)
- **Tiempo**: 5-10 horas
- **Viabilidad**: ✅ Buena (si presupuesto permite)

### Opción C: Solo Local (Mistral 7B)
- **Coste**: ~0.5€ (electricidad)
- **Calidad**: ⭐⭐⭐ (Media-Alta)
- **Tiempo**: 30-40 horas
- **Viabilidad**: ⚠️ Lento pero viable

---

## 🚀 **PRÓXIMOS PASOS INMEDIATOS**

1. **Configurar pipeline de ingestión** (BOE → Qdrant)
2. **Crear prompt maestro** para DeepSeek con few-shot
3. **Batch de prueba** (500 ítems) con DeepSeek
4. **Scoring con Nemotron** y calibrar umbral
5. **Revisión manual** de 50 ítems para ajustar prompts
6. **Expandir a 5,000 ítems** usando mismo flujo
7. **Validación con Mistral + Claude** en muestras complejas
8. **Fine-tuning con Unsloth** en portátil
9. **Despliegue en VPS** con FastAPI + Qdrant

---

## 📝 **CONCLUSIÓN**

La estrategia propuesta es **EXCELENTE y VIABLE**. Con las modificaciones sugeridas (Agente de Diversidad, segundo filtro RAG, validación humana), el plan es **óptimo** para generar 5,000 Q&A de calidad suprema con presupuesto mínimo (~6€).

**Puntos Fuertes**:
- ✅ Arquitectura sólida y escalable
- ✅ Costes ultra-optimizados
- ✅ Aprovecha infraestructura existente (Qdrant, BOE API)
- ✅ Fine-tuning local viable sin GPU
- ✅ Modelo final (Mixtral 8x7B) competitivo con comerciales

**Riesgos Mitigados**:
- ✅ Sesgo de generación → Agente de Diversidad
- ✅ Falsos positivos → Doble filtro RAG
- ✅ Errores sistemáticos → Validación humana
- ✅ Catastrophic forgetting → LoRA/QLoRA

**Recomendación Final**: **PROCEDER CON EL PLAN** tal como está diseñado, implementando las mejoras sugeridas.

---

**Estado Actual del Proyecto**:
- ✅ Indexación completada (1,390 chunks de exámenes oficiales)
- ✅ Qdrant funcionando con bge-m3-spa-law-qa
- ⏳ Generación Q&A pendiente (Mistral local tiene problemas de memoria)
- 🎯 **Siguiente paso**: Usar Mistral API o DeepSeek para generación

**¿Proceder con generación usando Mistral API/DeepSeek?** ✅ SÍ
