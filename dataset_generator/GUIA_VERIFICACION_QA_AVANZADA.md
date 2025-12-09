# 🔍 Guía de Verificación Avanzada de Q&A

Dos herramientas complementarias para verificar la calidad de datasets Q&A antes de fine-tuning.

---

## 📋 Resumen Ejecutivo

| Herramienta | Uso Principal | Costo | Velocidad | Mejor Para |
|-------------|---------------|-------|-----------|------------|
| **Nemotron Reward** | Scoring automático de calidad | **GRATIS** (100k calls) | ⚡ Rápido | Filtrado masivo inicial |
| **Claude + Cache** | Verificación profunda legal | ~$2-3 / 1000 items | 🐢 Lento | Validación final crítica |

---

## 🎯 Estrategia Recomendada (Pipeline de 2 Fases)

```
Dataset Crudo (5,000 Q&A)
    ↓
[FASE 1] Nemotron Reward (GRATIS, 10 min)
    ↓ Filtrar score > -3.5
Dataset Filtrado (3,500 Q&A)
    ↓
[FASE 2] Claude + Cache ($2-3, 2 horas)
    ↓ Verificar exactitud legal
Dataset Final (2,500 Q&A de calidad suprema)
```

**Resultado**: Dataset de alta calidad por ~$3 total

---

## 🚀 Herramienta 1: Nemotron Reward

### ¿Qué es?

NVIDIA Llama-3.1-Nemotron-70B-Reward es el modelo **#1 en RewardBench** (94.1% accuracy), superando a GPT-4o y Claude 3.5 en evaluación de calidad de respuestas.

### Ventajas

- ✅ **100% GRATIS**: 100,000 llamadas API gratis en build.nvidia.com
- ✅ **Rápido**: ~0.5 segundos por Q&A
- ✅ **Objetivo**: Score numérico consistente
- ✅ **Escalable**: Perfecto para miles de items

### Instalación

```bash
# Registrarse en build.nvidia.com (gratis)
# Obtener API key

# Configurar
export NVIDIA_API_KEY="nvapi-xxxxx"

# Instalar dependencias
pip install requests tqdm
```

### Uso Básico

```bash
# Verificar 5,000 Q&A (GRATIS)
python verificar_qa_nemotron_reward.py \
    --input dataset_raw.jsonl \
    --output dataset_filtered.jsonl \
    --min-quality good

# Probar con muestra pequeña
python verificar_qa_nemotron_reward.py \
    --input dataset_raw.jsonl \
    --output test.jsonl \
    --sample 50
```

### Umbrales de Calidad

```python
# Scores típicos (más alto = mejor)
-2.5  # Excelente (top 10%)
-3.5  # Bueno (recomendado para fine-tuning)
-4.5  # Aceptable
-5.5  # Pobre (rechazar)
```

### Ejemplo de Salida

```json
{
  "question": "¿Cuál es el plazo de prescripción...?",
  "answer": "El plazo es de 4 años según...",
  "nemotron_score": -3.2,
  "quality_level": "good",
  "verified_at": "2025-12-05T10:30:00"
}
```

### Estadísticas Generadas

```
📊 RESULTADOS DE VERIFICACIÓN
✅ Verificados: 3,500/5,000 (70.0%)
❌ Rechazados: 1,500

📈 Distribución de Calidad:
  excellent   :  500 (10.0%)
  good        : 2000 (40.0%)
  acceptable  : 1000 (20.0%)
  poor        : 1000 (20.0%)
  rejected    :  500 (10.0%)

🔧 API Calls usadas: 5,000 / 100,000 (5%)
```

---

## 🧠 Herramienta 2: Claude + Prompt Caching

### ¿Qué es?

Claude 3.5 Sonnet con **Prompt Caching** para verificación profunda de exactitud legal, cacheando el contexto de leyes para ahorrar 85-90% en tokens.

### Ventajas

- ✅ **Verificación Legal Profunda**: Detecta errores sutiles
- ✅ **Ahorro Masivo**: 85-90% menos tokens con cache
- ✅ **Explicaciones**: Razonamiento detallado de cada evaluación
- ✅ **Múltiples Métricas**: Exactitud, pedagogía, completitud, claridad

### Costos

```
SIN Prompt Caching:
- Input: $3.00 / 1M tokens
- 1,000 Q&A ≈ $15

CON Prompt Caching:
- Cache Read: $0.30 / 1M tokens (90% descuento)
- Cache Write: $3.75 / 1M tokens (primera vez)
- 1,000 Q&A ≈ $2-3 (85% ahorro)
```

### Instalación

```bash
# Instalar SDK de Anthropic
pip install anthropic tqdm

# Configurar API key
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
```

### Uso Básico

```bash
# Verificar con contexto legal (SE CACHEA)
python verificar_qa_claude_knowledge.py \
    --input dataset_filtered.jsonl \
    --output dataset_verified.jsonl \
    --context leyes/lgss.txt leyes/trlgss.txt \
    --min-score 7.0

# Probar con muestra
python verificar_qa_claude_knowledge.py \
    --input dataset_filtered.jsonl \
    --output test.jsonl \
    --context leyes/lgss.txt \
    --sample 20
```

### Preparar Archivos de Contexto

```bash
# Extraer leyes principales a texto plano
# Estos archivos se CACHEAN (solo se pagan una vez)

# Opción 1: Desde PDFs
pdftotext leyes/LGSS.pdf leyes/lgss.txt

# Opción 2: Desde BOE (ya tienes scripts)
python backend/agents/download_lgss_only.py

# Opción 3: Desde materiales de academia
cat elemplos_leyes_info/*.txt > leyes/materiales_completos.txt
```

### Métricas de Evaluación

Claude evalúa 4 dimensiones (0-10 cada una):

1. **Exactitud Legal**: ¿Es correcta según la ley?
2. **Calidad Pedagógica**: ¿Es útil para aprender?
3. **Completitud**: ¿Incluye toda la info necesaria?
4. **Claridad**: ¿Es fácil de entender?

### Ejemplo de Salida

```json
{
  "question": "¿Cuál es el plazo de prescripción...?",
  "answer": "El plazo es de 4 años según...",
  "claude_verification": {
    "exactitud_legal": 9.0,
    "calidad_pedagogica": 8.5,
    "completitud": 8.0,
    "claridad": 9.0,
    "score_total": 8.6,
    "aprobado": true,
    "errores_detectados": [],
    "sugerencias_mejora": ["Podría mencionar excepciones..."],
    "razonamiento": "Respuesta correcta y bien fundamentada...",
    "tokens_used": {
      "input": 150,
      "output": 200,
      "cache_read": 5000  // ¡Tokens leídos del cache!
    },
    "cache_hit": true
  }
}
```

### Estadísticas de Cache

```
💾 Estadísticas de Cache (Ahorro de Tokens):
  Cache Hits:   980
  Cache Misses: 20
  Hit Rate:     98.0%
  Tokens Saved: 4,900,000
  💰 Ahorro:    ~$13.23
```

---

## 🎯 Pipeline Completo Recomendado

### Paso 1: Generación (Ya tienes esto)

```bash
# Generar Q&A con tus métodos actuales
python generar_qa_mistral_api.py  # Barato
python generar_qa_groq.py         # Rápido
python generar_qa_kimi.py         # Buena calidad
```

### Paso 2: Filtrado Rápido con Nemotron (GRATIS)

```bash
# Filtrar 5,000 → 3,500 items
python verificar_qa_nemotron_reward.py \
    --input dataset_raw_5000.jsonl \
    --output dataset_filtered_3500.jsonl \
    --min-quality good

# Resultado: 3,500 Q&A con score > -3.5
# Costo: $0 (gratis)
# Tiempo: ~10 minutos
```

### Paso 3: Verificación Profunda con Claude ($2-3)

```bash
# Preparar contexto legal (una sola vez)
cat leyes/*.txt > leyes/contexto_completo.txt

# Verificar con Claude + Cache
python verificar_qa_claude_knowledge.py \
    --input dataset_filtered_3500.jsonl \
    --output dataset_final_2500.jsonl \
    --context leyes/contexto_completo.txt \
    --min-score 7.5

# Resultado: 2,500 Q&A verificadas legalmente
# Costo: ~$2-3 (con cache)
# Tiempo: ~2 horas
```

### Paso 4: Revisión Humana (Opcional)

```bash
# Revisar solo casos dudosos (score 7.0-7.5)
python human_review.py \
    --input dataset_final_2500.jsonl \
    --filter-score-range 7.0 7.5

# Revisar ~200 items manualmente
# Tiempo: 2-3 horas
```

---

## 💡 Tips y Trucos

### Optimizar Costos de Claude

1. **Cachea TODO el contexto legal**:
   ```bash
   # Combinar todas las leyes en un solo archivo
   cat leyes/*.txt > leyes/todo.txt
   
   # Usar --context con archivo grande
   # Se cachea una vez, se reutiliza 1000 veces
   ```

2. **Procesa en batches grandes**:
   - Cache dura 5 minutos
   - Procesa 100+ items seguidos para maximizar hits

3. **Reutiliza el cache**:
   - Si interrumpes, continúa dentro de 5 min
   - El cache se mantiene activo

### Ajustar Umbrales

```python
# Para dataset de entrenamiento (más estricto)
--min-score 8.0  # Solo lo mejor

# Para dataset de evaluación (más permisivo)
--min-score 6.5  # Incluir casos difíciles

# Para dataset de producción (balanceado)
--min-score 7.5  # Calidad alta pero realista
```

### Debugging

```bash
# Ver items rechazados
cat dataset_filtered_rejected.jsonl | jq '.reason' | sort | uniq -c

# Ver distribución de scores
cat dataset_filtered.jsonl | jq '.nemotron_score' | \
    python -c "import sys; import statistics; \
    scores = [float(x) for x in sys.stdin]; \
    print(f'Mean: {statistics.mean(scores):.2f}'); \
    print(f'Median: {statistics.median(scores):.2f}')"
```

---

## 📊 Comparación de Herramientas

| Característica | Nemotron | Claude + Cache |
|----------------|----------|----------------|
| **Costo** | GRATIS | $2-3 / 1000 items |
| **Velocidad** | 0.5 seg/item | 5-10 seg/item |
| **Profundidad** | Score numérico | Análisis detallado |
| **Exactitud Legal** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Explicaciones** | ❌ No | ✅ Sí |
| **Escalabilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Mejor para** | Filtrado inicial | Validación final |

---

## 🎓 Casos de Uso

### Caso 1: Dataset Grande (10,000+ items)

```bash
# 1. Nemotron para filtrar rápido
python verificar_qa_nemotron_reward.py \
    --input dataset_10k.jsonl \
    --output filtered_7k.jsonl \
    --min-quality good

# 2. Claude solo para top items
head -n 2000 filtered_7k.jsonl > top_2k.jsonl
python verificar_qa_claude_knowledge.py \
    --input top_2k.jsonl \
    --output final_1500.jsonl \
    --context leyes/todo.txt
```

### Caso 2: Dataset Pequeño pero Crítico (500 items)

```bash
# Ir directo a Claude (vale la pena)
python verificar_qa_claude_knowledge.py \
    --input dataset_500.jsonl \
    --output verified_400.jsonl \
    --context leyes/todo.txt \
    --min-score 8.0
```

### Caso 3: Presupuesto Cero

```bash
# Solo Nemotron (100% gratis)
python verificar_qa_nemotron_reward.py \
    --input dataset.jsonl \
    --output verified.jsonl \
    --min-quality excellent  # Más estricto
```

---

## 🔧 Troubleshooting

### Error: "NVIDIA_API_KEY no configurada"

```bash
# Registrarse en https://build.nvidia.com
# Copiar API key
export NVIDIA_API_KEY="nvapi-xxxxx"
```

### Error: "ANTHROPIC_API_KEY no configurada"

```bash
# Obtener key en https://console.anthropic.com
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
```

### Cache no funciona (Claude)

- Verifica que el contexto sea > 1024 tokens
- Procesa items seguidos (cache dura 5 min)
- Usa mismo archivo de contexto siempre

### Nemotron devuelve scores raros

- Scores son negativos (normal)
- Más alto = mejor (-2.5 > -4.5)
- Ajusta umbrales según tu dataset

---

## 📚 Referencias

- **Nemotron**: https://huggingface.co/nvidia/Llama-3.1-Nemotron-70B-Reward-HF
- **Claude Prompt Caching**: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- **RewardBench**: https://huggingface.co/spaces/allenai/reward-bench

---

## ✅ Checklist de Verificación

- [ ] Generar dataset crudo (5,000+ Q&A)
- [ ] Filtrar con Nemotron (gratis, 10 min)
- [ ] Preparar contexto legal para Claude
- [ ] Verificar con Claude + Cache ($2-3, 2h)
- [ ] Revisar estadísticas y ajustar umbrales
- [ ] (Opcional) Revisión humana de casos dudosos
- [ ] Exportar dataset final para fine-tuning

---

**Resultado Final**: Dataset de 2,000-3,000 Q&A de calidad suprema por ~$3 total 🎉
