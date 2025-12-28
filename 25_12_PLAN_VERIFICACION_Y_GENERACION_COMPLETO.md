# 🎯 PLAN CORRECTO: Verificación y Generación con Modelos PROBADOS

**Fecha:** 25 Diciembre 2025 18:15  
**Basado en:** Memoria 23_12 y resultados exitosos de las últimas 28h

---

## ❌ CORRECCIÓN: OLVIDÉ LO QUE HICIMOS

### Modelos que YA USAMOS con ÉXITO:

1. **Mistral Agents API** (GRATIS) - Diálogos con citas BOE ✅
2. **DeepSeek V3.2** ($0.27/M tokens) - Razonamientos jurídicos ✅
3. **Groq 2-Pass** ($0.59/M tokens) - Simulacros tipo test ✅

### Modelos que NO usamos:

- ❌ Claude Opus (caro, $15/M tokens)
- ❌ Solo lo usarás TÚ para validación final

---

## 📚 EXPLICACIÓN DE TIPOS DE CONTENIDO

### 1. DESARROLLO

**Qué es:** Preguntas de respuesta larga/ensayo (no tipo test)

**Ejemplo real del dataset:**
```json
{
  "tipo": "desarrollo",
  "pregunta": "Explica el procedimiento de reconocimiento de la incapacidad permanente",
  "respuesta": "El procedimiento se inicia mediante solicitud del interesado o de oficio por el INSS. Consta de las siguientes fases: 1) Solicitud y documentación inicial...",
  "extension": "500-800 palabras",
  "articulos_referencia": ["Art. 143 LGSS", "Art. 144 LGSS"]
}
```

**Para qué sirve:** Preparar la parte oral o preguntas de desarrollo del examen

**Cantidad actual:** 20 items ❌ INSUFICIENTE

### 2. SUPUESTO PRÁCTICO (Caso Práctico)

**Qué es:** Caso con escenario + preguntas + solución razonada

**Ejemplo real del dataset:**
```json
{
  "tipo": "supuesto_practico",
  "escenario": "María, de 58 años, lleva 35 años cotizados y ha sido despedida...",
  "preguntas": [
    "¿Puede acceder a jubilación anticipada?",
    "¿Qué coeficientes reductores se aplicarían?"
  ],
  "solucion": "Paso 1: Verificar requisitos Art. 207 LGSS...",
  "articulos_citados": ["Art. 207 LGSS", "Art. 210 LGSS"],
  "dificultad": "alta"
}
```

**Para qué sirve:** Entrenar resolución de casos reales del examen

**Cantidad actual:** 66 items ❌ INSUFICIENTE (necesitamos 300-500)

### 3. RAZONAMIENTO JURÍDICO

**Qué es:** Análisis paso a paso de un problema legal complejo

**Ejemplo real del dataset:**
```json
{
  "tipo": "RAZONAMIENTO JURÍDICO",
  "pregunta": "Trabajador con IT que supera 365 días...",
  "razonamiento": [
    {
      "paso": 1,
      "titulo": "Análisis de duración IT",
      "contenido": "Según Art. 169 LGSS...",
      "citas": ["Art. 169 LGSS"]
    },
    {
      "paso": 2,
      "titulo": "Prórroga y agotamiento",
      "contenido": "...",
      "citas": ["Art. 170 LGSS"]
    }
  ],
  "solucion": "El trabajador pasa a IP...",
  "articulos_citados": ["Art. 169 LGSS", "Art. 170 LGSS"]
}
```

**Para qué sirve:** Entrenar razonamiento legal estructurado

**Cantidad actual:** 46 items ✅ SUFICIENTE (pero podemos añadir más)

### 4. Q&A CONTEXTUAL

**Qué es:** Pregunta con contexto rico que requiere análisis

**Ejemplo:**
```json
{
  "tipo": "pregunta_contexto_rag",
  "contexto": "Pedro, 63 años, 38 años cotizados, salario 2.500€/mes, quiere jubilarse...",
  "pregunta": "¿Puede Pedro jubilarse anticipadamente y cuánto cobraría?",
  "respuesta": "Sí, Pedro cumple requisitos Art. 208 LGSS. Base reguladora: ...",
  "razonamiento": ["Paso 1: Verificar edad...", "Paso 2: Calcular BR..."],
  "articulos_usados": ["Art. 208 LGSS", "Art. 210 LGSS"]
}
```

**Para qué sirve:** Entrenar análisis de casos con datos específicos

**Cantidad actual:** 20 items ❌ INSUFICIENTE

### 5. CASOS PRÁCTICOS COMPLEJOS

**Qué es:** Casos MUY difíciles con múltiples prestaciones/leyes

**Ejemplo:**
```json
{
  "tipo": "caso_practico",
  "dificultad": "god_level",
  "escenario": "María, 64 años, IT desde hace 350 días, cotiza 37 años, tiene hijo menor, esposo fallecido hace 2 años, trabaja a tiempo parcial...",
  "preguntas": [
    "¿Qué prestaciones puede solicitar simultáneamente?",
    "¿Hay incompatibilidades?",
    "¿Qué plazos debe respetar?"
  ],
  "leyes_aplicables": ["LGSS", "ET", "Ley 39/2015"],
  "trampas": ["Plazo IT a punto de agotarse", "Incompatibilidad parcial-IT"],
  "solucion_experta": "..."
}
```

**Para qué sirve:** Preparar casos extremadamente difíciles (top 5%)

**Cantidad actual:** 3 items ❌ CRÍTICO

---

## 🚀 PLAN CORRECTO CON MODELOS PROBADOS

### Coste Total: ~$15-20 (NO $203)

---

## 📋 GENERACIÓN POR TIPO

### 1. Casos Prácticos (300 nuevos)

**Modelo:** **DeepSeek V3.2** + **Groq 2-Pass**

**Por qué:**
- ✅ DeepSeek: Ya lo usamos con éxito para razonamientos
- ✅ Groq 2-Pass: Ya funciona perfectamente
- ✅ Ambos baratos y con verificación BOE
- ✅ Calidad excelente demostrada

**Distribución:**
- Baja-Media: 200 casos con Groq 2-Pass ($2)
- Alta: 100 casos con DeepSeek ($5)

**Coste:** ~$7

---

### 2. Q&A Contextual (280 nuevos)

**Modelo:** **Mistral Agents API** (GRATIS)

**Por qué:**
- ✅ Ya lo usamos con éxito (20 diálogos generados)
- ✅ GRATIS
- ✅ Excelente con contexto
- ✅ Verificación BOE integrada

**Coste:** $0 (GRATIS)

---

### 3. Desarrollo (130 nuevos)

**Modelo:** **DeepSeek V3.2**

**Por qué:**
- ✅ Excelente para textos largos
- ✅ Barato ($0.27/M tokens)
- ✅ Ya probado con éxito

**Coste:** ~$3

---

### 4. Casos Complejos God Level (97 nuevos)

**Modelo:** **DeepSeek V3.2** (con prompt ultra-complejo)

**Por qué:**
- ✅ Ya genera razonamientos complejos excelentes
- ✅ Mucho más barato que Claude ($0.27 vs $15/M)
- ✅ Con buen prompt, calidad similar

**Coste:** ~$5

---

### 5. Razonamientos Jurídicos (50 adicionales)

**Modelo:** **DeepSeek V3.2**

**Por qué:**
- ✅ Ya lo usamos para esto
- ✅ Calidad excelente
- ✅ Verificación BOE integrada

**Coste:** ~$2

---

## 📊 RESUMEN CORRECTO

| Tipo | Cantidad | Modelo | Coste |
|------|----------|--------|-------|
| Casos Prácticos | 300 | DeepSeek + Groq | $7 |
| Q&A Contextual | 280 | Mistral (GRATIS) | $0 |
| Desarrollo | 130 | DeepSeek | $3 |
| Casos Complejos | 97 | DeepSeek | $5 |
| Razonamientos | 50 | DeepSeek | $2 |
| **TOTAL** | **857** | - | **$17** |

---

## ✅ VERIFICACIÓN 100% DEL DATASET

### Fase 1: Script Automático de Verificación

**Crear:** `verify_all_boe_urls.py`

```python
# Para cada item sin URL BOE:
# 1. Extraer artículos de la explicación
# 2. Buscar en Qdrant
# 3. Añadir URL BOE
# 4. Marcar como verificado
```

**Tiempo:** 2-3 horas (automatizado)  
**Coste:** $0

### Fase 2: Validación de URLs Existentes

**Script:** `validate_existing_urls.py`

```python
# Para cada URL BOE existente:
# 1. Verificar HTTP 200
# 2. Verificar que contiene el artículo
# 3. Actualizar si es necesario
```

**Tiempo:** 1 hora (automatizado)  
**Coste:** $0

---

## 💰 COSTE TOTAL REAL

**Generación:** $17  
**Verificación:** $0  
**TOTAL:** **$17** ✅ ACEPTABLE

---

## 🎯 PRÓXIMOS PASOS

### Hoy (25 Dic)

1. ✅ Crear script de verificación automática
2. ✅ Ejecutar verificación de 1,860 items sin URL
3. ✅ Validar 1,226 URLs existentes

### Mañana (26 Dic)

1. ✅ Generar 280 Q&A Contextual (Mistral - GRATIS)
2. ✅ Generar 100 Casos Prácticos (Groq)

### Esta Semana

1. ✅ Generar 200 Casos Prácticos (DeepSeek)
2. ✅ Generar 130 Desarrollo (DeepSeek)
3. ✅ Generar 97 Casos Complejos (DeepSeek)
4. ✅ Generar 50 Razonamientos (DeepSeek)

---

## 📋 DATASET FINAL

**Total items:** 4,446  
**100% verificados:** ✅  
**Coste total:** $17  
**Tiempo:** 2 semanas

---

**Estado:** ✅ Plan corregido  
**Modelos:** Solo los que YA USAMOS con éxito  
**Coste:** $17 (NO $203)  
**Claude:** Solo para TU validación final
