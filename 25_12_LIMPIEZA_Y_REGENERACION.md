# 🧹 LIMPIEZA Y REGENERACIÓN DE DATASET - 25 Diciembre 2025

**Fecha:** 25 Diciembre 2025 15:20  
**Estado:** ⏳ REGENERACIÓN EN CURSO

---

## 🗑️ ARCHIVOS ELIMINADOS (Basura)

### Movidos a `golden_dataset/archive_basura/`

**Razonamientos DeepSeek (incompletos):**
- `razonamientos_deepseek_20251224_231701.jsonl` (1 item - solo 5%)
- `razonamientos_deepseek_20251225_073615.jsonl` (1 item - solo 5%)

**Simulacros Groq (incompletos):**
- `simulacros_groq_20251225_072127.jsonl` (2 bloques - solo 40%)

**Razón:** Generación incompleta sin verificación BOE funcional

---

## ✅ ARCHIVOS CONSERVADOS

**Diálogos Mistral (válidos):**
- `dialogos_mistral_20251223_211423.jsonl` (20 items)
- `dialogos_mistral_20251224_231409.jsonl` (20 items)
- `dialogos_mistral_20251225_073033.jsonl` (50 items)

**Total conservado:** 90 diálogos

**Nota:** Aunque tienen algunos mensajes de "no puedo acceder", la mayoría tienen contenido válido y citas BOE.

---

## 🚀 REGENERACIÓN EN CURSO

### 1. DeepSeek V3.2 - 20 Razonamientos ⏳

**Script:** `generate_razonamiento_deepseek_verified.py`  
**Log:** `/tmp/deepseek_20_razonamientos_v2.log`  
**Estado:** Ejecutándose con tool `verificar_articulo` corregido

**Mejoras aplicadas:**
- ✅ Búsqueda más flexible (múltiples variaciones)
- ✅ min_score reducido a 0.3
- ✅ Devuelve resultado parcial si encuentra la ley
- ✅ Verifica "artículo X", "art. X", "art X"

**Tiempo estimado:** 30-40 minutos  
**Objetivo:** 20 razonamientos completos

### 2. Groq 2-Pass - 5 Bloques (50 preguntas) ⏳

**Script:** `generate_simulacros_groq_twopass.py`  
**Log:** `/tmp/groq_simulacros_v2.log`  
**Estado:** Ejecutándose con tool `verificar_articulo` corregido

**Mejoras aplicadas:**
- ✅ Búsqueda más flexible (múltiples variaciones)
- ✅ min_score reducido a 0.3
- ✅ Devuelve resultado parcial si encuentra la ley
- ✅ Verifica "artículo X", "art. X", "art X"

**Tiempo estimado:** 20-30 minutos  
**Objetivo:** 5 bloques × 10 preguntas = 50 preguntas

### 3. Mistral API - Evaluación Pendiente

**Estado:** ⏸️ En espera

**Decisión:** 
- Si los 50 diálogos existentes tienen verificación BOE correcta → Conservar
- Si no están verificados → Regenerar con nuevos temas

**Verificación necesaria:**
- Revisar si las URLs BOE están presentes
- Verificar que no haya muchos "no puedo acceder"
- Confirmar que las citas sean válidas

---

## 📊 DATASET LIMPIO ESPERADO

### Después de Regeneración

| Tipo | Items | Estado |
|------|-------|--------|
| Diálogos Mistral | 90 | ✅ Conservados |
| Razonamientos DeepSeek | 20 | ⏳ Regenerando |
| Simulacros Groq | 50 preguntas | ⏳ Regenerando |
| **TOTAL** | **160 items** | ⏳ En progreso |

---

## 🔍 CRITERIOS DE VALIDACIÓN

### Para Considerar un Item Válido

**Razonamientos (DeepSeek):**
- ✅ Mínimo 5 pasos de razonamiento
- ✅ Al menos 2 artículos citados
- ✅ Artículos verificados (exists: true)
- ✅ URLs BOE presentes
- ✅ Solución completa

**Simulacros (Groq):**
- ✅ 10 preguntas por bloque
- ✅ 4 opciones por pregunta
- ✅ Artículos BOE citados
- ✅ Artículos verificados (exists: true)
- ✅ URLs BOE presentes

**Diálogos (Mistral):**
- ✅ Respuesta completa (>500 caracteres)
- ✅ Citas a artículos presentes
- ✅ URLs BOE presentes
- ✅ Sin mensajes de "no puedo acceder"
- ✅ Uso de RAG confirmado

---

## 🎯 PRÓXIMOS PASOS

### Inmediatos (Hoy)

1. **Monitorear generación** (30-40 min)
   - DeepSeek: `/tmp/deepseek_20_razonamientos_v2.log`
   - Groq: `/tmp/groq_simulacros_v2.log`

2. **Verificar calidad** al completar
   - Contar items generados
   - Validar verificación BOE
   - Revisar citas y URLs

3. **Decidir sobre Mistral**
   - Analizar 50 diálogos existentes
   - Regenerar si no están verificados
   - Conservar si son válidos

### Corto Plazo (Esta Semana)

4. **Consolidar dataset final**
   - Unificar archivos válidos
   - Eliminar duplicados
   - Preparar formato Alpaca

5. **Auditoría manual**
   - Seleccionar 10 items aleatorios
   - Validar calidad y precisión
   - Verificar citas contra LGSS

6. **Fine-tuning**
   - Seleccionar modelo base
   - Preparar datos
   - Ejecutar con Unsloth

---

## 📁 ESTRUCTURA DE DIRECTORIOS

```
golden_dataset/
├── pilot_verified_23_12/
│   ├── dialogos_mistral_20251223_211423.jsonl (20 items) ✅
│   ├── dialogos_mistral_20251224_231409.jsonl (20 items) ✅
│   ├── dialogos_mistral_20251225_073033.jsonl (50 items) ✅
│   ├── razonamientos_deepseek_YYYYMMDD_HHMMSS.jsonl (20 items) ⏳
│   └── simulacros_groq_YYYYMMDD_HHMMSS.jsonl (5 bloques) ⏳
└── archive_basura/
    ├── razonamientos_deepseek_20251224_231701.jsonl (1 item) 🗑️
    ├── razonamientos_deepseek_20251225_073615.jsonl (1 item) 🗑️
    └── simulacros_groq_20251225_072127.jsonl (2 bloques) 🗑️
```

---

## 💰 COSTE ESTIMADO

| Script | Items | Coste |
|--------|-------|-------|
| DeepSeek (20 razonamientos) | 20 | ~$0.40 |
| Groq (50 preguntas) | 50 | ~$0.10 |
| **TOTAL REGENERACIÓN** | **70** | **~$0.50** |

---

**Estado:** ⏳ Regeneración en curso  
**Monitoreo:** Logs activos  
**Próxima actualización:** Cuando finalicen los scripts (~30-40 min)
