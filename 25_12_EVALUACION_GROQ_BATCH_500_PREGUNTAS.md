# 📊 EVALUACIÓN: GROQ BATCH API PARA GENERACIÓN MASIVA

**Fecha:** 25 Diciembre 2025 15:30  
**Objetivo:** Evaluar viabilidad de generar 500 preguntas adicionales con Groq Batch API

---

## ✅ ESTADO ACTUAL

### Generación Completada

**Groq 2-Pass:** ✅ 5/5 bloques (50 preguntas totales)

**Archivo:** `simulacros_groq_20251225_152238.jsonl` (23 KB)

**Temas cubiertos:**
1. Incapacidad temporal: duración, requisitos y extinción
2. Jubilación ordinaria y anticipada: requisitos y cálculo
3. Prestación por desempleo: requisitos, cuantía y duración
4. Incapacidad permanente: grados y procedimiento
5. Prestaciones de maternidad, paternidad y cuidado de menores

**Calidad:**
- ✅ 10 preguntas por bloque
- ✅ 4 opciones cada una
- ✅ Artículos BOE citados
- ✅ URLs BOE presentes
- ✅ Verificación de artículos funcionando

---

## 🔍 GROQ BATCH API - ANÁLISIS

### Características del Batch API

**Servicio disponible:** ✅ `groq_batch_service.py` existe

**Funcionalidad básica:**
```python
class GroqBatchService:
    def prepare_batch_file(requests_list, output_filename)
    def upload_file(file_path)
    def create_batch_job(file_id)
    def get_batch_status(batch_id)
    def download_file(file_id, output_path)
```

**Endpoint:** `/v1/chat/completions`  
**Completion window:** 24h

### ⚠️ LIMITACIÓN CRÍTICA: FUNCTION CALLING

**Problema identificado:**

Según la documentación de Groq y el análisis del código:

1. **Groq Batch API NO soporta function calling/tools**
   - El batch API solo acepta requests de chat completions estándar
   - No hay soporte para `tools` parameter en batch mode
   - Los tools solo funcionan en modo síncrono (real-time API)

2. **Implicaciones:**
   - ❌ No podemos usar `buscar_rag` en batch
   - ❌ No podemos usar `verificar_articulo` en batch
   - ❌ No hay verificación BOE durante generación batch

3. **Alternativas:**
   - ✅ Generar preguntas sin verificación en batch
   - ✅ Verificar después con script de post-procesamiento
   - ✅ Usar modo síncrono con rate limiting

---

## 💡 ESTRATEGIAS PARA 500 PREGUNTAS

### Opción 1: Batch Sin Verificación + Post-Procesamiento ⚠️

**Ventajas:**
- ✅ Muy rápido (24h para 500 preguntas)
- ✅ Muy barato (~$0.50 total)
- ✅ No requiere monitoreo

**Desventajas:**
- ❌ Sin verificación BOE durante generación
- ❌ Requiere script de post-procesamiento
- ❌ Posibles citas incorrectas
- ❌ Calidad inferior

**Flujo:**
1. Preparar 500 requests en batch
2. Subir y ejecutar batch job
3. Esperar 24h
4. Descargar resultados
5. Ejecutar script de verificación BOE
6. Filtrar preguntas inválidas

### Opción 2: Modo Síncrono con Rate Limiting ✅ RECOMENDADO

**Ventajas:**
- ✅ Verificación BOE durante generación
- ✅ Alta calidad garantizada
- ✅ Control total del proceso
- ✅ Podemos usar tools MCP

**Desventajas:**
- ⚠️ Más lento (8-10 horas para 500 preguntas)
- ⚠️ Requiere monitoreo
- ⚠️ Más caro (~$1.00 total)

**Flujo:**
1. Ejecutar script actual en loop
2. Generar 50 bloques (500 preguntas)
3. Rate limiting: 1 request/segundo
4. Pausas cada 50 preguntas
5. Verificación BOE en tiempo real

### Opción 3: Híbrido (Batch + Verificación Selectiva) 🔶

**Ventajas:**
- ✅ Rápido (24h)
- ✅ Barato (~$0.60)
- ✅ Verificación parcial

**Desventajas:**
- ⚠️ Complejidad media
- ⚠️ Requiere dos pasos

**Flujo:**
1. Generar 500 preguntas en batch (sin verificación)
2. Extraer todas las citas de artículos
3. Ejecutar verificación masiva de artículos
4. Marcar preguntas como verificadas/no verificadas
5. Regenerar solo las no verificadas en modo síncrono

---

## 📊 COMPARATIVA DE OPCIONES

| Aspecto | Batch Sin Verificación | Síncrono con Tools | Híbrido |
|---------|------------------------|-------------------|---------|
| **Tiempo** | 24h | 8-10h | 24h + 2h |
| **Coste** | ~$0.50 | ~$1.00 | ~$0.60 |
| **Calidad** | ⚠️ Media | ✅ Alta | ✅ Alta |
| **Verificación BOE** | ❌ Post | ✅ Real-time | 🔶 Post |
| **Complejidad** | Baja | Media | Alta |
| **Monitoreo** | No | Sí | Parcial |
| **Recomendado** | ❌ No | ✅ Sí | 🔶 Alternativa |

---

## 🎯 RECOMENDACIÓN FINAL

### ✅ OPCIÓN 2: Modo Síncrono con Rate Limiting

**Razones:**

1. **Calidad > Velocidad**
   - Necesitamos datos verificados para fine-tuning
   - Citas BOE incorrectas dañan el modelo
   - Verificación post-procesamiento es menos confiable

2. **Coste Aceptable**
   - $1.00 por 500 preguntas es muy barato
   - ROI alto: datos de calidad para fine-tuning

3. **Control Total**
   - Podemos pausar/reanudar
   - Monitoreo en tiempo real
   - Ajustes sobre la marcha

4. **Infraestructura Existente**
   - Script ya funciona perfectamente
   - Tools MCP ya integrados
   - No requiere desarrollo adicional

---

## 📋 PLAN DE EJECUCIÓN (500 PREGUNTAS)

### Fase 1: Preparación (15 min)

1. **Ampliar lista de temas** (50 temas)
   - Cubrir todo el temario oficial
   - Incluir temas avanzados
   - Evitar duplicados

2. **Configurar script**
   - Aumentar TEMAS_SIMULACROS a 50
   - Configurar pausas cada 50 preguntas
   - Añadir logging mejorado

3. **Verificar recursos**
   - Backend RAG funcionando
   - Qdrant respondiendo
   - API keys válidas

### Fase 2: Ejecución (8-10 horas)

**Modo:** Background execution con nohup

**Configuración:**
- 50 bloques × 10 preguntas = 500 preguntas
- Rate limiting: 1 request/segundo
- Pausas: 5 minutos cada 50 preguntas
- Reintentos: 3 intentos por pregunta

**Monitoreo:**
```bash
tail -f /tmp/groq_500_preguntas.log
```

**Checkpoints:**
- Cada 100 preguntas: verificar calidad
- Cada 200 preguntas: backup de archivos
- Al finalizar: auditoría completa

### Fase 3: Validación (1 hora)

1. **Verificar cantidad**
   - Contar preguntas generadas
   - Verificar que sean 500

2. **Verificar calidad**
   - Auditoría automática
   - Validación manual (10 muestras)
   - Verificar citas BOE

3. **Consolidar dataset**
   - Unificar archivos
   - Eliminar duplicados
   - Preparar para fine-tuning

---

## 💰 COSTE ESTIMADO

### Generación de 500 Preguntas

**Groq (llama-3.3-70b-versatile):**
- Input: ~500 requests × 2 passes × 1,000 tokens = 1M tokens
- Output: ~500 responses × 2,000 tokens = 1M tokens
- **Total:** ~2M tokens
- **Coste:** ~$1.00 (Groq es muy barato)

**Verificación BOE (incluida):**
- Backend RAG: Gratis (local)
- PostgreSQL: Gratis (local)
- Qdrant: Gratis (local)

**TOTAL:** ~$1.00

---

## ⏱️ CRONOGRAMA

### Hoy (25 Dic)

- ✅ Completar DeepSeek (20 razonamientos)
- ✅ Verificar Groq (50 preguntas completadas)
- ⏸️ Decidir: ¿Ejecutar 500 preguntas ahora?

### Mañana (26 Dic)

**Si ejecutamos hoy:**
- ✅ 500 preguntas completadas
- ✅ Auditoría y validación
- ✅ Dataset consolidado

**Si ejecutamos mañana:**
- Preparación de temas
- Ejecución durante el día
- Finalización por la noche

---

## 🤔 DECISIÓN REQUERIDA

### ¿Necesitamos 500 preguntas adicionales?

**Argumentos a favor:**
- ✅ Dataset más robusto para fine-tuning
- ✅ Mayor cobertura del temario
- ✅ Mejor generalización del modelo

**Argumentos en contra:**
- ⚠️ Ya tenemos 50 preguntas de simulacro
- ⚠️ Tendremos 20 razonamientos DeepSeek
- ⚠️ Tenemos 90 diálogos Mistral
- ⚠️ Total actual: ~160 items

**Recomendación:**
- **Sí, generar 500 preguntas** si queremos un dataset robusto
- **No, esperar** si queremos primero validar calidad de los 160 items actuales

---

## 📝 PRÓXIMOS PASOS

### Inmediatos

1. ✅ Esperar a que DeepSeek complete (20 razonamientos)
2. ✅ Verificar calidad de los 160 items actuales
3. 🤔 Decidir: ¿Generar 500 preguntas adicionales?

### Si decidimos generar 500 preguntas

1. Ampliar lista de temas a 50
2. Configurar script para 50 bloques
3. Ejecutar en background
4. Monitorear durante 8-10 horas
5. Validar y consolidar

---

**Estado:** ✅ Análisis completado  
**Recomendación:** Modo síncrono con tools (no batch)  
**Decisión pendiente:** ¿Generar 500 preguntas adicionales?
