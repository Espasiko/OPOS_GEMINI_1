# 🌙 GENERACIÓN NOCTURNA - Estado de Ejecución

**Fecha:** 24 Diciembre 2025 23:10  
**Estado:** ⏳ EN EJECUCIÓN

---

## 🚀 SCRIPTS EN EJECUCIÓN

### 1. DeepSeek V3 - Razonamientos Jurídicos

**Script:** `generate_razonamiento_deepseek_verified.py`  
**Objetivo:** 10 razonamientos legales complejos  
**Estado:** ⏳ Ejecutándose en background  
**Log:** `/tmp/deepseek_razonamientos.log`

**Características:**
- Modelo: DeepSeek V3.2
- RAG integrado (Qdrant + PostgreSQL)
- Verificación BOE durante generación
- Tools: `buscar_rag`, `verificar_articulo`

**Tiempo estimado:** 15-20 minutos

### 2. Mistral API - Diálogos con Citas BOE

**Script:** `generate_dialogos_mistral_verified.py`  
**Objetivo:** 20 diálogos usuario-asistente  
**Estado:** ⏳ Ejecutándose en background  
**Log:** `/tmp/mistral_dialogos.log`

**Características:**
- Modelo: Mistral Agents (API gratuita)
- RAG integrado (Qdrant + PostgreSQL)
- Verificación BOE durante generación
- Tools: `buscar_rag`, `verificar_url`

**Tiempo estimado:** 10-15 minutos

### 3. Mistral Local - Casos Prácticos (Test)

**Script:** `generate_premium_mistral_local.py`  
**Objetivo:** 1 caso práctico (test)  
**Estado:** ✅ Test completado  
**Modelo:** Mistral:latest (4.4 GB local)

**Características:**
- Estrategia 2-pass (Arquitecto → Redactor)
- Sin RAG (test básico)
- Timeout: 20 minutos por caso

---

## 📊 CONFIGURACIÓN DE GENERACIÓN

### DeepSeek V3.2

```python
MODEL = "deepseek-chat"
TEMPERATURE = 0.2
MAX_TOKENS = 4000
TOOLS = ["buscar_rag", "verificar_articulo"]
```

**Temas de razonamientos:**
1. IT que supera 365 días → IP
2. Jubilación anticipada vs ordinaria
3. Compatibilidad pensión + trabajo
4. Recargos por falta de medidas de seguridad
5. Prestaciones no contributivas
6. IMV + otras prestaciones
7. Cotización en pluriempleo
8. Afiliación en regímenes especiales
9. Recaudación ejecutiva
10. Recursos administrativos en SS

### Mistral API (Agents)

```python
MODEL = "mistral-large-latest"
AGENT_ID = os.getenv("AGENT_ID")
TOOLS = ["buscar_rag", "verificar_url"]
```

**Preguntas de diálogos:**
1. ¿Puedo jubilarme a los 63 años?
2. ¿Qué es la incapacidad permanente?
3. ¿Cómo solicito la prestación por desempleo?
4. ¿Puedo cobrar pensión y trabajar?
5. ¿Qué es el IMV?
6. ¿Cómo funciona la cotización?
7. ¿Qué pasa si no pago la Seguridad Social?
8. ¿Cuándo puedo solicitar la jubilación anticipada?
9. ¿Qué es la incapacidad temporal?
10. ¿Cómo se calcula la pensión?
... (20 total)

---

## ⏱️ TIEMPO ESTIMADO TOTAL

| Script | Items | Tiempo |
|--------|-------|--------|
| DeepSeek | 10 | 15-20 min |
| Mistral API | 20 | 10-15 min |
| **TOTAL** | **30** | **25-35 min** |

---

## 💰 COSTE ESTIMADO

| Script | Modelo | Coste |
|--------|--------|-------|
| DeepSeek | DeepSeek V3.2 | ~$0.20 |
| Mistral API | Mistral Large | $0.00 (gratis) |
| Mistral Local | Mistral:latest | $0.00 (local) |
| **TOTAL** | - | **~$0.20** |

---

## 📁 ARCHIVOS DE SALIDA

**Directorio:** `golden_dataset/pilot_verified_23_12/`

**Archivos esperados:**
- `razonamientos_deepseek_YYYYMMDD_HHMMSS.jsonl` (10 items)
- `dialogos_mistral_YYYYMMDD_HHMMSS.jsonl` (20 items)

**Formato:**
```json
{
  "tipo": "razonamiento" | "dialogo",
  "contenido": {...},
  "metadata": {
    "modelo": "deepseek-chat" | "mistral-large-latest",
    "generado_en": "2025-12-24T23:10:00",
    "verificado": true,
    "iteraciones": 3
  }
}
```

---

## 🔍 MONITOREO

### Comandos de Seguimiento

**DeepSeek:**
```bash
tail -f /tmp/deepseek_razonamientos.log
```

**Mistral API:**
```bash
tail -f /tmp/mistral_dialogos.log
```

**Verificar procesos:**
```bash
ps aux | grep -E "python.*generate_(razonamiento|dialogos)" | grep -v grep
```

---

## ✅ VERIFICACIÓN POST-GENERACIÓN

### 1. Verificar Archivos Generados

```bash
ls -lh golden_dataset/pilot_verified_23_12/
```

### 2. Contar Items

```bash
wc -l golden_dataset/pilot_verified_23_12/*.jsonl
```

### 3. Validar JSON

```bash
cat golden_dataset/pilot_verified_23_12/razonamientos_deepseek_*.jsonl | jq '.' | head -50
```

### 4. Ejecutar Auditor

```bash
cd dataset_generator
python3 audit_generated_pilot.py
```

---

## 🌙 PRÓXIMA FASE: MODO NOCTURNO COMPLETO

**Objetivo:** 200-300 items/noche con Mistral Local

**Configuración necesaria:**
1. Modificar `generate_premium_mistral_local.py`:
   - Integrar RAG (backend API)
   - Añadir CoT forzado
   - Implementar pausas cada 50 items (5 min)
   - Loop para generar múltiples casos

2. Ejecutar en background:
   ```bash
   nohup python3 generate_premium_mistral_local_nocturno.py > /tmp/mistral_nocturno.log 2>&1 &
   ```

3. Monitorear temperatura GPU:
   ```bash
   watch -n 60 nvidia-smi
   ```

---

**Estado:** ⏳ Generación en curso  
**Próximo paso:** Esperar finalización (25-35 min) y ejecutar auditoría
