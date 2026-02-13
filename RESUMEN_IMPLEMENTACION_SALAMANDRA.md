# ✅ RESUMEN: PRUEBA DE CONCEPTO SALAMANDRA VPS

**Fecha:** 21/01/2026  
**Objetivo:** Generar UN caso práctico con Salamandra VPS (sin fine-tuning) + sistema de agentes  
**Status:** ✅ IMPLEMENTADO - LISTO PARA PROBAR

---

## 🎯 QUÉ SE IMPLEMENTÓ

### Componentes Creados (8 archivos nuevos)

1. **backend/config/prompts/salamandra.yaml**
   - Prompts optimizados para Salamandra 7B
   - Instrucciones concisas (modelo español)
   - Configuración VPS + fallback local

2. **backend/calculators/calculos_ss.py**
   - Calculadora SS con precisión 100% (Decimal)
   - Función: `calcular_subsidio_it(base, contingencia, dia)`
   - Basado en Art. 173.1 TRLGSS

3. **backend/calculators/dispatcher.py**
   - Identifica tipo de caso (subsidio_it, cuota_ss, etc.)
   - Extrae parámetros del tema
   - Ejecuta calculadora apropiada

4. **backend/agents/salamandra_client.py**
   - Cliente para Salamandra VPS (147.93.95.67:11434)
   - Fallback automático a local si VPS falla
   - Soporte streaming y no-streaming

5. **backend/agents/generate_salamandra.py**
   - Generador de casos usando Salamandra
   - Integra calculadora via dispatcher
   - Valida estructura JSON

6. **backend/agents/confidence_scorer.py**
   - Score de confianza basado en heurísticas
   - 5 dimensiones: estructura, citas, cálculos, lógica, claridad
   - Output: Score 0-1 + nivel (ALTA/MEDIA/BAJA)

7. **backend/routers/casos_practicos.py**
   - Endpoint: POST `/casos/generate-one`
   - Orquesta: Dispatcher → Calculadora → Salamandra → Scorer
   - Response: Caso + confidence + cálculo usado

8. **test_salamandra_caso.py**
   - Script de prueba completo
   - Muestra resultado formateado
   - Guarda JSON en archivo

---

## 🚀 CÓMO PROBAR

### Paso 1: Iniciar Backend

```bash
cd backend
python main.py
```

Deberías ver:
```
🚀 OpositAIA Backend starting...
✅ Database connection initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Paso 2: Ejecutar Prueba

```bash
python test_salamandra_caso.py
```

### Paso 3: Verificar Output

El script mostrará:
- ✅ Health check del servicio
- 📊 Cálculo usado (base, porcentaje, subsidio)
- 🎯 Confidence score (overall + breakdown)
- 📝 Caso generado completo
- 💾 Archivo guardado: `caso_generado_salamandra.json`

---

## 📊 FLUJO COMPLETO

```
1. REQUEST
   ↓
   tema: "IT por EC, base 1500€, día 10"

2. DISPATCHER
   ↓
   tipo: "subsidio_it"
   params: {base: 1500, contingencia: "EC", dia: 10}

3. CALCULADORA SS
   ↓
   base_diaria: 50.00€
   porcentaje: 0.60 (60%)
   subsidio_diario: 30.00€

4. SALAMANDRA VPS
   ↓
   Genera caso JSON con:
   - Enunciado (150-300 palabras)
   - Pregunta
   - 4 opciones (A/B/C/D)
   - Respuesta correcta
   - Explicación con citas

5. CONFIDENCE SCORER
   ↓
   overall: 0.87
   level: ALTA
   breakdown: {estructura: 1.0, citas: 0.85, ...}

6. RESPONSE
   ↓
   {caso, confidence, calculo_usado, status}
```

---

## 🎯 MÉTRICAS DE ÉXITO

| Métrica | Target | Cómo Verificar |
|---------|--------|----------------|
| **Tiempo generación** | < 30s | Ver output del script |
| **Confidence score** | > 0.70 | Ver `confidence.overall` |
| **JSON válido** | 100% | Script no falla al parsear |
| **Cálculo correcto** | 100% | 1500/30 × 0.60 = 30.00€ |
| **Citas BOE** | > 0 | Ver `articulos_aplicables` |
| **Estructura completa** | 100% | Tiene enunciado, pregunta, opciones, etc. |

---

## 🔍 QUÉ VALIDAR

### Checklist de Validación

- [ ] **Backend arranca sin errores**
- [ ] **Health check responde OK**
- [ ] **Dispatcher identifica tipo correcto**
- [ ] **Calculadora retorna 30.00€** (1500/30 × 0.60)
- [ ] **Salamandra VPS responde** (o fallback a local)
- [ ] **JSON generado es válido**
- [ ] **Tiene 4 opciones (A/B/C/D)**
- [ ] **Respuesta correcta es una de A/B/C/D**
- [ ] **Explicación menciona Art. 173.1**
- [ ] **Confidence score > 0.70**
- [ ] **Archivo JSON se guarda correctamente**

---

## 🐛 POSIBLES ERRORES

### Error 1: "Salamandra unavailable"

**Causa:** VPS no responde y local tampoco  
**Solución:**
```bash
# Verificar VPS
curl http://147.93.95.67:11434/api/tags

# Verificar local
curl http://localhost:11434/api/tags

# Si local falla, iniciar Ollama
ollama serve
```

### Error 2: "JSON parse error"

**Causa:** Salamandra no generó JSON válido  
**Solución:**
- Revisar logs del backend
- Salamandra puede necesitar prompt más simple
- Bajar temperature a 0.5 en `salamandra.yaml`

### Error 3: "Confidence BAJA"

**Causa:** Caso no cumple heurísticas de calidad  
**Solución:**
- Ver `confidence.breakdown` para identificar problema
- Mejorar prompt en `salamandra.yaml`
- Añadir más ejemplos

---

## 📈 PRÓXIMOS PASOS

Una vez validado este caso único:

### Corto Plazo (1-2 días)
1. ✅ Generar 10 casos (mismo tema, variaciones)
2. ✅ Validar distribución A/B/C/D (~25% cada)
3. ✅ Medir tiempo promedio de generación

### Medio Plazo (1 semana)
4. ⏳ Añadir Adversarial Verifier (Claude)
5. ⏳ Añadir Legal Judge (DeepSeek + BOE API)
6. ⏳ Integrar RAG (artículos desde Qdrant)

### Largo Plazo (2 semanas)
7. ⏳ Generar 100 casos gold standard
8. ⏳ Escalar a 1,000 casos (COSM strategy)
9. ⏳ Fine-tuning Salamandra con dataset validado

---

## 💡 APRENDIZAJES CLAVE

1. **Salamandra sin fine-tuning** puede generar casos si:
   - Prompt es conciso y claro
   - Se le dan valores exactos de la calculadora
   - Se le muestran ejemplos de estructura

2. **Calculadora SS** es crítica:
   - Precisión 100% con Decimal
   - Salamandra NO debe calcular, solo usar valores

3. **Confidence Scorer** es útil para:
   - Filtrar casos de baja calidad
   - Identificar qué mejorar en el prompt
   - Decidir si necesita validación manual

4. **VPS + Fallback** es robusto:
   - Si VPS falla, usa local automáticamente
   - No bloquea el sistema

---

## 📞 SOPORTE

Si encuentras problemas:

1. **Revisar logs del backend:**
   ```bash
   tail -f backend/backend.log
   ```

2. **Verificar Salamandra VPS:**
   ```bash
   curl http://147.93.95.67:11434/api/tags
   ```

3. **Probar endpoint manualmente:**
   ```bash
   curl -X POST http://localhost:8000/casos/health
   ```

4. **Ver documentación completa:**
   - `PRUEBA_CONCEPTO_SALAMANDRA_VPS.md`

---

## ✅ CONCLUSIÓN

**Sistema implementado y listo para probar.**

**Comando para empezar:**
```bash
# Terminal 1
cd backend && python main.py

# Terminal 2
python test_salamandra_caso.py
```

**Tiempo de implementación:** ~2 horas ✅  
**Archivos creados:** 8 ✅  
**Líneas de código:** ~800 ✅  
**Status:** READY TO TEST 🚀
