# Enhanced Claude Judge - Batch API Implementation Notes

## Descubrimientos Clave

### 1. Batch API de Anthropic (Oct 2024 - GA)

**Ventajas:**
- 💰 **50% de descuento** vs API normal
- 📦 Hasta 10,000 requests por batch
- ⏱️ Procesamiento en < 24h (usualmente < 1h)
- 📊 Límite: 100,000 mensajes o 256MB

**Modelo Correcto:**
- `claude-3-5-sonnet-20240620` ✅ (válido en enero 2026)
- `claude-3-5-sonnet-latest` (siempre apunta a última versión)
- ❌ NO: `claude-3-5-sonnet-20241022` (no existe)

### 2. Implementación Recomendada

**Para 50 preguntas:**
- Costo con API normal: ~$3-4
- Costo con Batch API: **~$1.50-2** (50% ahorro)
- Tiempo de espera: 30-60 minutos (aceptable)

**Endpoint:**
```
POST https://api.anthropic.com/v1/messages/batches
```

**Formato:**
```json
{
  "requests": [
    {
      "custom_id": "question_1",
      "params": {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 3000,
        "messages": [{"role": "user", "content": "..."}]
      }
    }
  ]
}
```

### 3. Workflow Batch

1. **Create Batch** → Recibe `batch_id`
2. **Poll Status** → Check cada 30s hasta `processing_status=ended`
3. **Retrieve Results** → GET `/v1/messages/batches/{batch_id}/results`
4. **Parse JSONL** → Cada línea es un resultado

### 4. Decisión de Implementación

**Opción A:** Batch API (Recomendado)
- Pro: 50% más barato
- Pro: Mejor para 50+ requests
- Con: Espera 30-60 min

**Opción B:** API Síncrona (Actual)
- Pro: Resultados inmediatos
- Con: 2x más caro
- Con: Rate limiting más estricto

**Compromiso sugerido:**
Implementar ambas con flag `--use-batch` para que el usuario elija según urgencia vs costo.
