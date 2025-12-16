# 🎯 ESTRATEGIA DE DATASET GENERATION - DECISIÓN FINAL

**Fecha:** 5 de Diciembre 2025  
**Estado:** ✅ READY FOR IMPLEMENTATION  
**Objetivo:** Generar 5,000-10,000 Q&A de máxima calidad para fine-tuning de Mistral Small 24B

---

## 📊 ANÁLISIS DE DATASETS EXISTENTES

### ✅ Dataset Consolidado (YA GENERADO)
- **Total:** 126 Q&A válidas
- **Top 100 seleccionadas** para fine-tuning
- **Fuente:** 13 archivos de 10 modelos diferentes

**Distribución de calidad:**
```
🥇 Claude (100/100)           - 5 Q&A (máxima calidad)
🥈 Mistral MaxDif (100/100)   - 10 Q&A
🥉 Kiro Quality (97.5/100)    - 10 Q&A
🔹 Groq Llama 3.3 (61.7/100)  - 20 Q&A
🔹 Cohere (73.8/100)          - 20 Q&A
🔹 DeepSeek (79.2/100)        - 3 Q&A
🔹 Kimi K2 (77.2/100)         - 9 Q&A
🔹 Otros                      - 33 Q&A
```

**Archivo:** `dataset_generator/dataset_output/dataset_consolidado_top100.jsonl`

---

## 💰 ANÁLISIS DE COSTOS APIs

### 1. GEMINI API (RECOMENDADO PARA DESKTOP)

**Ventajas:**
- ✅ **FREE TIER GENEROSO**: 15 requests/min, 1.5M tokens/mes
- ✅ Ya tienes API key configurada
- ✅ 1.5-Flash: Rápido y barato
- ✅ Desktop-compatible (API-based)
- ✅ Excelente para dataset generation

**Pricing:**
- 1.5-Flash: $0.075/M input, $0.30/M output
- Para 10K Q&A (avg 100 tokens input + 200 output): ~$0.60

**Capacidad mensual gratis:**
- 1.5M tokens ÷ 300 tokens/Q&A = **5,000 Q&A gratis**

**Conclusión:** ✅ **PERFECTA PARA GENERAR 5K Q&A SIN COSTO**

---

### 2. GROQ API (DESCARTADO)

**Problemas:**
- ❌ **NO HAY FREE TIER**: Pay-as-you-go desde el primer token
- ❌ Llama 3.3 70B: $0.59/M input, $0.79/M output
- ❌ Para 10K Q&A: ~$10-15
- ❌ Más caro que Gemini

**Uso anterior:**
- Ya usaste ayer para generar 20 Q&A
- Resultados: calidad media (61.7/100)

**Conclusión:** ❌ **INNECESARIO** - Gemini es más barato y gratis

---

### 3. COHERE API (ALTERNATIVA RERANKING)

**Uso:** 
- No para generación, sino para **reranking** de Q&A
- Mejorar calidad del dataset consolidado

**Pricing:** 
- Free trial: $10 crédito
- Production: $1/M tokens

**Conclusión:** ⚠️ **FUTURO** - Para optimizar ranking, no generación

---

### 4. DEEPSEEK API (DESCARTADO)

**Calidad:** 79.2/100 (media-alta)
**Pricing:** Similar a Gemini pero menos documentado
**Conclusión:** ❌ **NO NECESARIO** - Gemini es mejor

---

### 5. CLAUDE/ANTHROPIC (DESCARTADO)

**Calidad:** 100/100 pero solo 5 Q&A (datos limitados)
**Pricing:** $3/M input, $15/M output = $2-3 por Q&A
**Conclusión:** ❌ **MUY CARO** - 60x más que Gemini

---

## 🎯 PLAN DE EJECUCIÓN RECOMENDADO

### FASE 1: Consolidación (YA COMPLETADA ✅)
- ✅ Dataset consolidado: 100 Q&A de máxima calidad
- ✅ Archivo: `dataset_consolidado_top100.jsonl`
- ✅ Calidad promedio: 85.3/100

### FASE 2: Generación Masiva (5,000 Q&A ADICIONALES)

**Opción A: Gemini API (RECOMENDADA)**
```
Proceso:
1. Usar Gemini 1.5-Flash
2. 5,000 Q&A × 300 tokens = 1.5M tokens (GRATIS)
3. Tiempo estimado: 2-3 horas
4. Costo: $0 (free tier)
5. Calidad esperada: 70-80/100

Script: generar_qa_gemini_5k.py (crear)
```

**Opción B: Híbrida (Si quieres maximizar variedad)**
```
- 3,000 Q&A con Gemini (gratis)
- 2,000 Q&A con Groq ($10, para variedad)
- Total: 5,000 Q&A
- Costo total: $10
- Ganancia: Más diversidad de modelos
```

**Opción C: Escalada Premium (Si quieres máxima calidad)**
```
- 2,000 Q&A con Gemini (gratis)
- 2,000 Q&A con Groq ($10)
- 1,000 Q&A con Claude ($2)
- Total: 5,000 Q&A premium
- Costo: $12
- Calidad esperada: 85+/100
```

### FASE 3: Consolidación Final

```python
# Combinar:
dataset_consolidado_top100.jsonl (100 Q&A)
+ nuevas_qa_gemini_5k.jsonl (5,000 Q&A)
= dataset_final_5100.jsonl

# Filtrado por calidad:
- Score > 60: Aceptadas
- Score < 40: Descartadas
- Deduplicación automática

# Formato final:
{
    "pregunta": "...",
    "opciones": [...],
    "respuesta_correcta": "...",
    "explicacion": "...",
    "articulos": [...],
    "dificultad": "...",
    "score": 75.3,
    "source": "gemini_5k"
}
```

---

## 📋 DECISIÓN RECOMENDADA

### ✅ PLAN EJECUTIVO (Opción A - Mejor ROI)

```
SEMANA 1:
├─ Día 1: Generar 5,000 Q&A con Gemini (GRATIS)
├─ Día 2: Consolidar + filtrar
├─ Día 3: Validar calidad
└─ Costo: $0

SEMANA 2:
├─ Día 1-2: Fine-tuning en laptop (Mistral Small Q4, 16GB RAM)
├─ Día 3-4: Evaluación y ajustes
└─ Costo: $0 (local)

TOTAL DATASET FINAL:
├─ Cantidad: 5,100+ Q&A
├─ Calidad promedio: 75+/100
├─ Costo: $0 (completamente gratis)
└─ Tiempo: 1 semana
```

---

## 🛠️ SCRIPTS NECESARIOS

### 1. `generar_qa_gemini_5k.py` (CREAR)
```python
- Usa Gemini 1.5-Flash
- Genera 5K Q&A sobre Seguridad Social
- Distribuidas por temas
- Dificultad variada
- Output: nuevas_qa_gemini_5k.jsonl
- Tiempo: 2-3 horas
```

### 2. `consolidar_dataset_final.py` (CREAR)
```python
- Combina 100 + 5000
- Aplica filtros de calidad
- Deduplicación
- Normalización de formato
- Output: dataset_final_5100.jsonl
```

### 3. `evaluate_rag_gemini.py` (YA EXISTE ✅)
```python
- Evaluación RAG en desktop
- API-based (Gemini)
- No depende de Mistral local
- Funciona ahora
```

---

## 🚀 INSTRUCCIONES DE USO

### En DESKTOP (Ahora):

1. **Generar 5K Q&A:**
```bash
cd dataset_generator
python3 generar_qa_gemini_5k.py
# Esperar 2-3 horas
```

2. **Consolidar:**
```bash
python3 consolidar_dataset_final.py
```

3. **Evaluar RAG:**
```bash
cd ../backend/scripts
python3 evaluate_rag_gemini.py
```

### En LAPTOP (Después):

1. **Fine-tune Mistral Small:**
```bash
python3 finetune_mistral_small_q4.py --dataset dataset_final_5100.jsonl
```

2. **Usar modelo fine-tuned:**
```bash
python3 evaluate_rag_mistral_local.py
# Con cache Redis incluido
```

---

## 📈 MÉTRICAS DE ÉXITO

| Métrica | Target | Status |
|---------|--------|--------|
| Q&A consolidadas | 100 | ✅ 100 |
| Calidad promedio | 75+/100 | ✅ 85.3/100 |
| Q&A a generar | 5,000 | 🔄 Pendiente |
| Costo total | <$15 | ✅ $0 |
| Tiempo total | 1 semana | 🔄 Estimado |
| Fine-tune completado | Semana 2 | 🔄 Estimado |

---

## 💡 CONCLUSIÓN

**Gemini API es la solución óptima porque:**

1. **Gratis:** 5,000 Q&A completamente gratuito
2. **Rápido:** 1.5-Flash es muy rápido
3. **Ya funciona:** API key ya configurada
4. **Desktop-compatible:** API-based, no necesita hardware
5. **Escalable:** Si necesitas más, cuesta solo $0.075/M input

**No necesitas:**
- ❌ Groq (más caro)
- ❌ Claude (muy caro)
- ❌ DeepSeek (redundante)
- ❌ Mistral en desktop (no hay RAM)

**Próximo paso:** Crear script `generar_qa_gemini_5k.py`

---

**Documento generado:** 5 de Diciembre 2025
**Revisor:** GitHub Copilot  
**Aprobación:** ✅ Listo para implementación
