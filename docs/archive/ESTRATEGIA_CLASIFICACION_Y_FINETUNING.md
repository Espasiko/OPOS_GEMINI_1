# 📊 ESTRATEGIA: CLASIFICACIÓN Y FINE-TUNING

**Fecha**: 2 Diciembre 2025  
**Objetivo**: Definir cuándo clasificar Q&A y estrategia de fine-tuning  

---

## 🎯 RESPUESTA A TU PREGUNTA: ¿CUÁNDO CLASIFICAR?

### **OPCIÓN RECOMENDADA: CLASIFICAR ANTES DEL FINE-TUNING** ✅

**Razones:**

1. **Mejor organización del dataset**
   - Puedes balancear temas (mismo número de Q&A por tema)
   - Detectas gaps (temas con pocas Q&A)
   - Identificas duplicados o similares

2. **Fine-tuning más efectivo**
   - Puedes hacer fine-tuning por tema (modelos especializados)
   - O un modelo general con dataset balanceado
   - Mejor control de calidad por categoría

3. **Análisis de calidad**
   - Detectas qué temas tienen más errores
   - Puedes priorizar revisión humana por tema
   - Métricas de calidad por categoría

4. **Flexibilidad**
   - Puedes crear múltiples datasets (uno por tema)
   - O un dataset único bien estructurado
   - Facilita A/B testing de modelos

---

## 📋 FLUJO COMPLETO RECOMENDADO

### **FASE 1: GENERACIÓN (Días 1-3)**

```yaml
Paso 1: Obtener contexto
  - Función: buscar_rag_qdrant()
  - Input: Tema general (ej: "jubilación")
  - Output: Chunks relevantes de leyes

Paso 2: Generar Q&A
  - Función: generar_qa_legal()
  - Input: Contexto de RAG
  - Output: Q&A sin verificar

Paso 3: Verificación automática
  - Función: verificar_qa_completa()
  - Verifica: BOE, cálculos, URLs
  - Output: Q&A + score de confianza

Resultado: 10,000 Q&A con scores
```

### **FASE 2: CLASIFICACIÓN (Día 4)**

```yaml
Paso 1: Clasificar todas las Q&A
  - Función: clasificar_qa_tema()
  - Input: Cada Q&A generada
  - Output: Taxonomía completa

Paso 2: Análisis del dataset
  - Contar Q&A por tema
  - Detectar desbalances
  - Identificar gaps

Paso 3: Balanceo (si necesario)
  - Generar más Q&A de temas con pocas
  - Eliminar duplicados
  - Ajustar distribución

Resultado: Dataset balanceado y clasificado
```

### **FASE 3: REVISIÓN HUMANA (Día 5)**

```yaml
Criterio de revisión:
  - Confidence < 0.7: REVISAR TODAS (prioridad alta)
  - Confidence 0.7-0.9: REVISAR MUESTRA (20%)
  - Confidence > 0.9: REVISAR MUESTRA (5%)

Por tema:
  - Temas críticos (jubilación, IMV): Revisar más
  - Temas simples (definiciones): Revisar menos

Resultado: Dataset verificado por humanos
```

### **FASE 4: PREPARACIÓN FINE-TUNING (Día 6)**

```yaml
Formato Mistral:
  {
    "messages": [
      {"role": "system", "content": "Eres experto en SS..."},
      {"role": "user", "content": "Pregunta..."},
      {"role": "assistant", "content": "Respuesta..."}
    ]
  }

Splits:
  - Training: 80% (8,000 Q&A)
  - Validation: 10% (1,000 Q&A)
  - Test: 10% (1,000 Q&A)

Resultado: 3 archivos .jsonl listos
```

### **FASE 5: FINE-TUNING (Día 7)**

```yaml
Opción A: Modelo único general
  - Fine-tune Mistral 7B con todo el dataset
  - Coste: ~$9 (1M tokens training)
  - Resultado: 1 modelo que sabe de todo

Opción B: Modelos especializados
  - Fine-tune por tema (jubilación, IMV, etc.)
  - Coste: ~$2-3 por modelo
  - Resultado: 5-6 modelos especializados

Recomendación: Empezar con Opción A
```

---

## 🏗️ ESTRUCTURA DE CLASIFICACIÓN

### **Taxonomía Propuesta:**

```json
{
  "tema_principal": "jubilacion",
  "subtema": "edad_ordinaria",
  "tipo_pregunta": "conceptual",
  "dificultad": "medio",
  "requiere_calculo": false,
  "leyes_referenciadas": ["LGSS"],
  "articulos": ["205.1.a"],
  "año_vigencia": 2024,
  "tags": ["edad", "requisitos", "2024"]
}
```

### **Temas Principales:**

1. **Jubilación** (30% del dataset)
   - Edad ordinaria
   - Jubilación anticipada
   - Jubilación parcial
   - Cálculo de pensión

2. **Incapacidad** (20%)
   - Temporal
   - Permanente (parcial, total, absoluta, gran invalidez)
   - Requisitos
   - Cálculos

3. **Desempleo** (15%)
   - Contributivo
   - Asistencial
   - Requisitos
   - Duración

4. **IMV** (10%)
   - Requisitos
   - Cuantías
   - Compatibilidades

5. **Cotización** (15%)
   - Bases
   - Tipos
   - Bonificaciones

6. **Otros** (10%)
   - Maternidad/Paternidad
   - Riesgo embarazo
   - Cuidado menores
   - etc.

---

## 💰 COSTES ESTIMADOS

### **Plan Free (Actual):**
```yaml
Límites:
  - Requests: Limitados
  - Tokens: Limitados
  - Agentes: Funciona pero con límites

Recomendación:
  - Generar 100-200 Q&A de prueba
  - Verificar calidad
  - Luego pasar a plan de pago
```

### **Plan de Pago (Recomendado):**
```yaml
Generación 10K Q&A:
  - Mistral Medium: ~€7-10
  - Web search: Incluido
  - Code execution: Incluido

Fine-tuning:
  - Training: $9/1M tokens (~€8.5)
  - Storage: $4/mes por modelo (~€3.8)
  - Inference: $2/1M tokens (~€1.9)

Total estimado: €20-25 para todo el proceso
```

---

## 🎯 ESTRATEGIA RECOMENDADA

### **FASE ACTUAL (Plan Free):**

1. **Generar 100 Q&A de prueba**
   - 10 por cada tema principal
   - Verificar calidad manualmente
   - Ajustar instrucciones del agente

2. **Probar clasificación**
   - Clasificar las 100 Q&A
   - Verificar taxonomía
   - Ajustar categorías si necesario

3. **Evaluar resultados**
   - ¿Calidad suficiente?
   - ¿Clasificación correcta?
   - ¿Listo para escalar?

### **SIGUIENTE FASE (Plan de Pago):**

1. **Generar 10,000 Q&A**
   - Usar funciones del agente
   - Verificación automática
   - Clasificación automática

2. **Revisión humana selectiva**
   - Según scores de confianza
   - Por tema crítico
   - Muestra estadística

3. **Fine-tuning**
   - Preparar dataset
   - Fine-tune Mistral 7B
   - Evaluar modelo

4. **Producción**
   - Desplegar modelo
   - Integrar en app
   - Monitorear calidad

---

## 📊 MÉTRICAS DE ÉXITO

### **Generación:**
- ✅ 10,000 Q&A generadas
- ✅ 95%+ con confidence > 0.7
- ✅ 80%+ con confidence > 0.9
- ✅ 0% URLs inválidas
- ✅ 0% cálculos incorrectos

### **Clasificación:**
- ✅ 100% Q&A clasificadas
- ✅ Distribución balanceada por tema
- ✅ Sin duplicados
- ✅ Taxonomía consistente

### **Fine-tuning:**
- ✅ Training loss < 0.5
- ✅ Validation accuracy > 90%
- ✅ Test accuracy > 85%
- ✅ Sin overfitting

### **Producción:**
- ✅ Latencia < 2s por Q&A
- ✅ Coste < €0.01 por Q&A
- ✅ Calidad humana > 95%
- ✅ Sin alucinaciones

---

## 🚀 PRÓXIMOS PASOS INMEDIATOS

### **HOY:**
1. ✅ Funciones del agente definidas
2. ⏳ Añadir funciones en Mistral Studio
3. ⏳ Probar con 10 Q&A

### **MAÑANA:**
1. Generar 100 Q&A de prueba
2. Clasificar automáticamente
3. Revisar manualmente
4. Ajustar si necesario

### **ESTA SEMANA:**
1. Pasar a plan de pago
2. Generar 10,000 Q&A
3. Clasificar y balancear
4. Revisión humana selectiva

### **PRÓXIMA SEMANA:**
1. Preparar dataset fine-tuning
2. Fine-tune Mistral 7B
3. Evaluar modelo
4. Desplegar en producción

---

## 📝 NOTAS IMPORTANTES

### **Sobre Clasificación:**
- ✅ **SÍ, clasificar ANTES de fine-tuning**
- Permite mejor organización
- Facilita balanceo del dataset
- Mejora calidad del modelo final

### **Sobre Fine-tuning:**
- Empezar con modelo único general
- Si funciona bien, considerar modelos especializados
- Monitorear métricas de calidad
- Iterar según resultados

### **Sobre Costes:**
- Plan free: Suficiente para pruebas (100-200 Q&A)
- Plan de pago: Necesario para producción (10K Q&A)
- Coste total estimado: €20-25
- ROI: Alto (10K Q&A de calidad profesional)

---

**Conclusión**: Clasifica ANTES del fine-tuning. Genera primero 100 Q&A de prueba en plan free, verifica calidad, luego escala a 10K en plan de pago. 🎯
