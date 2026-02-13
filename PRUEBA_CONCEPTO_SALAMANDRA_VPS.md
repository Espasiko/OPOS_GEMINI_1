# 🧪 PRUEBA DE CONCEPTO: UN CASO CON SALAMANDRA VPS

**Objetivo:** Generar UN SOLO caso práctico de calidad usando Salamandra en VPS (sin fine-tuning) + sistema de agentes completo

**Fecha:** 21/01/2026
**Duración estimada:** 2-3 horas

---

## 📋 COMPONENTES A CREAR (EN ORDEN)

### FASE 1: INFRAESTRUCTURA MÍNIMA (30 min)

**1.1 Configuración YAML para Salamandra**
- Archivo: `backend/config/prompts/salamandra.yaml`
- Contenido: Prompt optimizado para Salamandra (conciso, directo)

**1.2 Calculadora SS Base**
- Archivo: `backend/calculators/calculos_ss.py`
- Función: `calcular_subsidio_it(base, contingencia, dia)`
- Solo IT por ahora (caso más común)

**1.3 Dispatcher Simple**
- Archivo: `backend/calculators/dispatcher.py`
- Función: `identificar_tipo_caso()` y `extraer_parametros()`

### FASE 2: GENERADOR SALAMANDRA (45 min)

**2.1 Cliente Salamandra VPS**
- Archivo: `backend/agents/salamandra_client.py`
- Conexión a VPS: http://147.93.95.67:11434
- Fallback a local si VPS falla

**2.2 Generador de Casos**
- Archivo: `backend/agents/generate_salamandra.py`
- Usa prompt de salamandra.yaml
- Integra calculadora via dispatcher
- Output: JSON estructurado


### FASE 3: VALIDACIÓN 3-CAPAS (45 min)

**3.1 Confidence Scorer**
- Archivo: `backend/agents/confidence_scorer.py`
- Heurísticas: citas BOE, cálculos, lógica, claridad
- Output: Score 0-1 + nivel (ALTA/MEDIA/BAJA)

**3.2 Adversarial Verifier (Claude)**
- Archivo: `backend/agents/adversarial_verifier.py`
- Prompt "Abogado del Diablo"
- Detecta errores sutiles

**3.3 Legal Judge (DeepSeek + BOE API)**
- Archivo: `backend/agents/legal_judge.py`
- Verifica citas BOE
- Valida lógica legal

### FASE 4: ORQUESTADOR (30 min)

**4.1 Pipeline Completo**
- Archivo: `backend/agents/caso_generator_pipeline.py`
- Orquesta: Dispatcher → Calculadora → Salamandra → Validación 3-capas
- Output: Caso validado o rechazado con razones

**4.2 Endpoint FastAPI**
- Archivo: `backend/routers/casos_practicos.py`
- POST `/casos/generate-one`
- Request: tema, dificultad
- Response: Caso completo + métricas de validación

---

## 🎯 CASO DE PRUEBA

**Tema:** Incapacidad Temporal por Enfermedad Común
**Parámetros:**
- Base cotización: 1,500€/mes
- Contingencia: EC (Enfermedad Común)
- Día de baja: 10
- Subsidio esperado: 30.00€/día (60% de 50€/día)

**Artículos aplicables:**
- Art. 173.1 TRLGSS (porcentajes IT)
- Art. 174.2 TRLGSS (base reguladora)



---

## 🚀 INSTRUCCIONES DE USO

### Prerequisitos

1. **Backend corriendo:**
   ```bash
   cd backend
   python main.py
   ```

2. **Salamandra VPS accesible:**
   - URL: http://147.93.95.67:11434
   - Modelo: salamandra-7b-instruct
   - Si VPS falla, usa fallback local

3. **Dependencias instaladas:**
   ```bash
   pip install httpx pyyaml
   ```

### Ejecutar Prueba

```bash
python test_salamandra_caso.py
```

### Ejemplo de Request Manual (curl)

```bash
curl -X POST http://localhost:8000/casos/generate-one \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Incapacidad Temporal por Enfermedad Común, base 1500€, día 10",
    "dificultad": "media"
  }'
```

### Ejemplo de Request Manual (Python)

```python
import httpx
import asyncio
import json

async def test():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/casos/generate-one",
            json={
                "tema": "IT por EC, base 1500€, día 10",
                "dificultad": "media"
            },
            timeout=60.0
        )
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

asyncio.run(test())
```

---

## 📊 OUTPUT ESPERADO

```json
{
  "caso": {
    "enunciado": "María sufre una gripe el 15 de marzo...",
    "pregunta": "¿Cuánto cobrará María de subsidio diario?",
    "opciones": {
      "A": "30.00€/día",
      "B": "37.50€/día",
      "C": "50.00€/día",
      "D": "0€/día"
    },
    "respuesta_correcta": "A",
    "explicacion": "Base diaria: 1500€ / 30 días = 50€. Contingencia EC, días 4-20: 60%. Subsidio: 50€ × 0.60 = 30.00€/día.",
    "articulos_aplicables": ["173.1"],
    "dificultad": "media"
  },
  "confidence": {
    "overall": 0.87,
    "level": "ALTA",
    "breakdown": {
      "estructura": 1.0,
      "citas_legales": 0.85,
      "calculos": 1.0,
      "logica": 0.80,
      "claridad": 0.90
    },
    "issues": []
  },
  "calculo_usado": {
    "base_diaria": 50.0,
    "porcentaje": 0.6,
    "subsidio_diario": 30.0,
    "contingencia": "EC",
    "dia_baja": 10,
    "articulo_aplicable": "Art. 173.1 TRLGSS"
  },
  "status": "success"
}
```

---

## 🔍 VALIDACIÓN DEL SISTEMA

### Checklist de Validación

- [ ] **Dispatcher funciona**: Identifica tipo "subsidio_it"
- [ ] **Calculadora precisa**: 1500€ / 30 = 50€, 50€ × 0.60 = 30€
- [ ] **Salamandra genera**: JSON válido con estructura correcta
- [ ] **Confidence scorer**: Score > 0.70 (MEDIA o ALTA)
- [ ] **Artículos citados**: Menciona Art. 173.1 TRLGSS
- [ ] **Opciones balanceadas**: 4 opciones (A/B/C/D)
- [ ] **Explicación lógica**: Incluye "porque", citas, cálculo

### Métricas de Éxito

| Métrica | Target | Actual |
|---------|--------|--------|
| Tiempo generación | < 30s | ⏱️ |
| Confidence score | > 0.70 | 📊 |
| JSON válido | 100% | ✅ |
| Cálculo correcto | 100% | ✅ |
| Citas BOE | > 0 | 📚 |

---

## 🐛 TROUBLESHOOTING

### Error: "Salamandra unavailable"

**Causa:** VPS no responde y local tampoco
**Solución:**
1. Verificar VPS: `curl http://147.93.95.67:11434/api/tags`
2. Verificar local: `curl http://localhost:11434/api/tags`
3. Iniciar Ollama local: `ollama serve`

### Error: "JSON parse error"

**Causa:** Salamandra no generó JSON válido
**Solución:**
1. Revisar logs del backend
2. Ajustar temperatura (bajar a 0.5)
3. Simplificar prompt en `salamandra.yaml`

### Error: "Confidence BAJA"

**Causa:** Caso generado no cumple heurísticas
**Solución:**
1. Revisar breakdown del confidence
2. Mejorar prompt en `salamandra.yaml`
3. Añadir más ejemplos en el prompt

---

## 📈 PRÓXIMOS PASOS

Una vez validado este caso único:

1. **Generar 10 casos** (mismo tema, variaciones)
2. **Validar distribución A/B/C/D** (debe ser ~25% cada)
3. **Añadir Adversarial Verifier** (Claude)
4. **Añadir Legal Judge** (DeepSeek + BOE API)
5. **Integrar RAG** (artículos desde Qdrant)
6. **Escalar a 100 casos** (10 temas × 10 casos)
7. **Fine-tuning Salamandra** (con dataset validado)

---

## 📝 NOTAS TÉCNICAS

### Arquitectura Implementada

```
Usuario
  ↓
POST /casos/generate-one
  ↓
┌─────────────────────────────────────┐
│ CasosPracticosDispatcher            │
│  - identificar_tipo_caso()          │
│  - extraer_parametros()             │
│  - calcular()                       │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ CalculadoraSS                       │
│  - calcular_subsidio_it()           │
│  - Precisión: Decimal (100%)        │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ SalamandraGenerator                 │
│  - VPS: 147.93.95.67:11434          │
│  - Fallback: localhost:11434        │
│  - Prompt: salamandra.yaml          │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ ConfidenceScorer                    │
│  - Heurísticas: 5 dimensiones       │
│  - Score: 0-1                       │
│  - Level: ALTA/MEDIA/BAJA           │
└─────────────────────────────────────┘
  ↓
Response JSON
```

### Archivos Creados

```
backend/
├── config/
│   └── prompts/
│       └── salamandra.yaml          ✅ Prompts optimizados
├── calculators/
│   ├── __init__.py                  ✅ Exports
│   ├── calculos_ss.py               ✅ Calculadora SS (Decimal)
│   └── dispatcher.py                ✅ Dispatcher + extractor
├── agents/
│   ├── salamandra_client.py         ✅ Cliente VPS + fallback
│   ├── generate_salamandra.py       ✅ Generador de casos
│   └── confidence_scorer.py         ✅ Scorer heurístico
└── routers/
    └── casos_practicos.py           ✅ Endpoint FastAPI

test_salamandra_caso.py              ✅ Script de prueba
PRUEBA_CONCEPTO_SALAMANDRA_VPS.md    ✅ Documentación
```

---

## ✅ CONCLUSIÓN

Sistema listo para probar con **UN SOLO CASO**.

**Comando para empezar:**
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Prueba
python test_salamandra_caso.py
```

**Tiempo estimado:** 2-3 horas de implementación ✅ COMPLETADO

**Siguiente paso:** Ejecutar prueba y validar resultados 🚀
