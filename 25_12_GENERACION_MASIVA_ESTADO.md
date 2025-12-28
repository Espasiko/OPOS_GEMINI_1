# 🚀 GENERACIÓN MASIVA EN CURSO - 25 Diciembre 2025

**Fecha:** 25 Diciembre 2025 07:20  
**Estado:** ⏳ 3 SCRIPTS EJECUTÁNDOSE EN PARALELO

---

## 📊 SCRIPTS ACTIVOS

### 1. DeepSeek V3.2 - 20 Razonamientos Jurídicos

**Script:** `generate_razonamiento_deepseek_verified.py`  
**Estado:** ⏳ Ejecutándose  
**Log:** `/tmp/deepseek_20_razonamientos.log`

**Configuración:**
- Modelo: DeepSeek V3.2 (deepseek-chat)
- Temas: 20 (ampliados desde 10)
- RAG integrado: ✅
- Verificación BOE: ✅
- Temperatura: 0.2 (precisión)

**Tiempo estimado:** 30-40 minutos  
**Coste estimado:** ~$0.40

### 2. Mistral API - 50 Diálogos con Citas BOE

**Script:** `generate_dialogos_mistral_verified.py`  
**Estado:** ⏳ Ejecutándose  
**Log:** `/tmp/mistral_50_dialogos.log`

**Configuración:**
- Modelo: Mistral Agents (mistral-large-latest)
- Preguntas: 50 (ampliadas desde 20)
- RAG integrado: ✅
- Verificación BOE: ✅
- Agent ID: ag_019ad601946d7323a81c544229de40a1

**Tiempo estimado:** 25-35 minutos  
**Coste estimado:** $0.00 (API gratuita)

### 3. Groq - 50 Preguntas de Simulacro (5 bloques)

**Script:** `generate_simulacros_groq_twopass.py`  
**Estado:** ⏳ Ejecutándose  
**Log:** `/tmp/groq_simulacros.log`

**Configuración:**
- Modelo: Groq (llama-3.3-70b-versatile)
- Estrategia: 2-pass (Arquitecto → Redactor)
- Bloques: 5 temas x 10 preguntas = 50 total
- RAG integrado: ✅
- Verificación artículos: ✅

**Temas:**
1. Incapacidad temporal: duración, requisitos y extinción
2. Jubilación ordinaria y anticipada: requisitos y cálculo
3. Prestación por desempleo: requisitos, cuantía y duración
4. Incapacidad permanente: grados y procedimiento
5. Prestaciones de maternidad, paternidad y cuidado de menores

**Tiempo estimado:** 20-30 minutos  
**Coste estimado:** ~$0.10

---

## 📈 RESUMEN TOTAL

| Script | Items | Tiempo | Coste |
|--------|-------|--------|-------|
| DeepSeek | 20 razonamientos | 30-40 min | ~$0.40 |
| Mistral API | 50 diálogos | 25-35 min | $0.00 |
| Groq | 50 preguntas | 20-30 min | ~$0.10 |
| **TOTAL** | **120 items** | **40-50 min** | **~$0.50** |

---

## 🎯 OBJETIVOS DE GENERACIÓN

### Distribución por Tipo

**Razonamientos Jurídicos (20):**
- Análisis paso a paso de casos complejos
- Citas a artículos LGSS
- Solución fundamentada
- Formato: JSON con escenario + razonamiento + solución

**Diálogos Q&A (50):**
- Preguntas frecuentes de usuarios
- Respuestas con citas BOE
- Verificación de artículos
- Formato: JSON con pregunta + respuesta + metadata

**Simulacros de Examen (50):**
- Preguntas tipo test (4 opciones)
- Artículos BOE verificados
- Opciones trampa realistas
- Formato: JSON con preguntas + respuestas + justificación

---

## 📁 ARCHIVOS DE SALIDA

**Directorio:** `golden_dataset/pilot_verified_23_12/`

**Archivos esperados:**
- `razonamientos_deepseek_YYYYMMDD_HHMMSS.jsonl` (20 items)
- `dialogos_mistral_YYYYMMDD_HHMMSS.jsonl` (50 items)
- `simulacros_groq_YYYYMMDD_HHMMSS.jsonl` (5 bloques, 50 preguntas)

---

## 🔍 MONITOREO EN TIEMPO REAL

### Comandos de Seguimiento

**DeepSeek:**
```bash
tail -f /tmp/deepseek_20_razonamientos.log
```

**Mistral API:**
```bash
tail -f /tmp/mistral_50_dialogos.log
```

**Groq:**
```bash
tail -f /tmp/groq_simulacros.log
```

**Ver todos:**
```bash
watch -n 5 'tail -20 /tmp/deepseek_20_razonamientos.log && echo "---" && tail -20 /tmp/mistral_50_dialogos.log && echo "---" && tail -20 /tmp/groq_simulacros.log'
```

**Verificar procesos:**
```bash
ps aux | grep -E "python.*(deepseek|mistral|groq)" | grep -v grep
```

---

## ⏱️ ESTIMACIÓN DE FINALIZACIÓN

**Inicio:** 07:20 (25 Dic 2025)  
**Finalización estimada:** 08:00-08:10 (25 Dic 2025)

**Tiempo total:** 40-50 minutos

---

## 💰 COSTE TOTAL ESTIMADO

| Componente | Coste |
|------------|-------|
| DeepSeek V3.2 (20 items) | $0.40 |
| Mistral API (50 items) | $0.00 |
| Groq (50 preguntas) | $0.10 |
| **TOTAL** | **$0.50** |

**Coste por item:** $0.004 (muy eficiente)

---

## ✅ VERIFICACIÓN POST-GENERACIÓN

### 1. Contar Items Generados

```bash
cd /home/spas/OPOS_GEMINI_1/dataset_generator
wc -l golden_dataset/pilot_verified_23_12/*.jsonl
```

### 2. Verificar Calidad JSON

```bash
# DeepSeek
cat golden_dataset/pilot_verified_23_12/razonamientos_deepseek_*.jsonl | jq '.' | head -100

# Mistral
cat golden_dataset/pilot_verified_23_12/dialogos_mistral_*.jsonl | jq '.' | head -100

# Groq
cat golden_dataset/pilot_verified_23_12/simulacros_groq_*.jsonl | jq '.' | head -100
```

### 3. Ejecutar Auditoría

```bash
cd dataset_generator
python3 audit_generated_pilot.py
```

---

## 📊 PROGRESO ACUMULADO

### Generación Anterior (24 Dic)

- DeepSeek: 1 razonamiento
- Mistral: 20 diálogos
- **Total anterior:** 21 items

### Generación Actual (25 Dic)

- DeepSeek: 20 razonamientos
- Mistral: 50 diálogos
- Groq: 50 preguntas
- **Total actual:** 120 items

### TOTAL ACUMULADO

**141 items** en dataset verificado

---

## 🎯 PRÓXIMOS PASOS

### Después de Completar Generación

1. **Verificar archivos generados**
   - Contar items
   - Validar JSON
   - Revisar calidad

2. **Ejecutar auditoría automática**
   - `audit_generated_pilot.py`
   - Verificar citas BOE
   - Validar artículos

3. **Validación manual**
   - Seleccionar 5 items aleatorios
   - Revisar calidad y precisión
   - Verificar citas contra LGSS

4. **Consolidar dataset**
   - Unificar todos los archivos
   - Eliminar duplicados
   - Preparar para fine-tuning

5. **Fine-tuning**
   - Seleccionar modelo base
   - Preparar formato Alpaca
   - Ejecutar fine-tuning con Unsloth

---

**Estado:** ⏳ Generación en curso  
**Monitoreo:** Logs activos  
**Próxima actualización:** 08:00-08:10 (cuando finalice)
