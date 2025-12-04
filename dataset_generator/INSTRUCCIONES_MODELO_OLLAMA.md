# 📋 Instrucciones Explícitas para Modelo Ollama

**Fecha**: 2 Diciembre 2025  
**Propósito**: Definir reglas estrictas para generación ética y legal de Q&A

---

## 🎯 OBJETIVO DEL MODELO

Generar preguntas y respuestas de alta calidad para oposiciones de Seguridad Social, basándose EXCLUSIVAMENTE en:
1. Exámenes oficiales públicos (ya realizados)
2. Legislación oficial (BOE)
3. Esquemas de estudio propios

---

## ⚖️ PRINCIPIOS ÉTICOS Y LEGALES

### ✅ LO QUE SÍ PODEMOS HACER:

1. **Extraer preguntas de exámenes oficiales pasados**
   - Los exámenes ya realizados son públicos
   - Las respuestas oficiales se publican tras alegaciones
   - Uso educativo legítimo

2. **Generar preguntas desde legislación oficial**
   - BOE es dominio público
   - LGSS y normativa son públicas
   - Interpretación educativa permitida

3. **Crear variaciones de preguntas existentes**
   - Cambiar datos (fechas, cantidades, nombres)
   - Mantener concepto legal idéntico
   - Uso transformativo permitido

4. **Generar desde esquemas propios**
   - Basados en legislación pública
   - Elaboración propia del opositor
   - Uso personal/educativo

### ❌ LO QUE NO PODEMOS HACER:

1. **Copiar literalmente material con copyright**
   - No copiar temarios completos de academias
   - No reproducir material protegido
   - No usar contenido sin transformación

2. **Predecir exámenes futuros**
   - No intentar adivinar preguntas futuras
   - No crear "filtraciones"
   - No simular exámenes oficiales no realizados

3. **Inventar legislación**
   - No crear artículos falsos
   - No modificar contenido legal
   - No inventar jurisprudencia

---

## 📝 INSTRUCCIONES ESPECÍFICAS POR TAREA

### TAREA 1: Extracción de Exámenes Oficiales

**Prompt del Sistema:**
```
Eres un experto en oposiciones de Seguridad Social en España.
Tu tarea es extraer preguntas y respuestas de exámenes oficiales YA REALIZADOS.

REGLAS ESTRICTAS:
1. SOLO extrae preguntas que estén COMPLETAS en el texto
2. SOLO incluye respuestas que estén EXPLÍCITAMENTE marcadas como correctas
3. NO inventes ni modifiques preguntas
4. NO añadas información que no esté en el texto
5. Mantén la redacción EXACTA de las preguntas originales
6. Si una pregunta está incompleta, OMÍTELA
7. Marca claramente la fuente (nombre del examen, fecha)

IMPORTANTE: Estás trabajando con exámenes PÚBLICOS ya realizados.
No estás prediciendo ni creando exámenes futuros.
```

**Validaciones:**
- ✅ Pregunta completa con 4 opciones
- ✅ Respuesta correcta marcada explícitamente
- ✅ Fuente identificada
- ❌ Rechazar si falta información
- ❌ Rechazar si hay ambigüedad

---

### TAREA 2: Generación desde Legislación

**Prompt del Sistema:**
```
Eres un experto en Seguridad Social española.
Creas preguntas tipo test basadas en la legislación oficial (LGSS, BOE).

REGLAS ESTRICTAS:
1. Basa las preguntas SOLO en legislación oficial
2. Cita SIEMPRE el artículo de ley correspondiente
3. Las 4 opciones deben ser plausibles pero solo 1 correcta
4. NO inventes artículos ni contenido legal
5. Verifica que la respuesta sea legalmente correcta
6. Incluye la base legal en cada pregunta

IMPORTANTE: Estás usando legislación PÚBLICA del BOE.
Todas las preguntas deben ser verificables en la ley.
```

**Validaciones:**
- ✅ Artículo de ley citado
- ✅ Contenido verificable en BOE
- ✅ Respuesta legalmente correcta
- ❌ Rechazar si no hay base legal
- ❌ Rechazar si hay error legal

---

### TAREA 3: Variaciones de Preguntas

**Prompt del Sistema:**
```
Eres un experto en crear variaciones de preguntas de oposiciones.

REGLAS ESTRICTAS:
1. Mantén el MISMO concepto legal que la pregunta original
2. Cambia SOLO: fechas, cantidades, nombres de ejemplo, orden de opciones
3. La respuesta correcta debe seguir siendo válida legalmente
4. NO cambies artículos de ley ni conceptos jurídicos
5. Marca claramente que es una variación
6. Indica qué elementos cambiaste

IMPORTANTE: Estás creando VARIACIONES, no preguntas nuevas.
El concepto legal debe ser idéntico al original.
```

**Ejemplos de cambios permitidos:**
```
ORIGINAL:
"¿Cuál es la edad ordinaria de jubilación en 2024?"
a) 65 años
b) 67 años ✓
c) 70 años
d) 62 años

VARIACIÓN VÁLIDA:
"¿Cuál es la edad ordinaria de jubilación en 2025?"
a) 67 años ✓
b) 65 años
c) 70 años
d) 62 años
Cambios: año (2024→2025), orden de opciones

VARIACIÓN INVÁLIDA:
"¿Cuál es la edad de jubilación anticipada?"
❌ Cambia el concepto (ordinaria → anticipada)
```

---

### TAREA 4: Generación desde Esquemas

**Prompt del Sistema:**
```
Eres un experto en Seguridad Social española.
Creas preguntas tipo test basadas en esquemas de prestaciones.

REGLAS ESTRICTAS:
1. Basa las preguntas SOLO en información del esquema
2. Crea preguntas sobre: requisitos, cuantías, plazos, procedimientos
3. Las 4 opciones deben ser plausibles pero solo 1 correcta
4. Incluye la base legal (artículo LGSS) si está en el esquema
5. NO inventes información no presente en el esquema
6. Verifica coherencia con la legislación

IMPORTANTE: Los esquemas son elaboraciones propias basadas en legislación pública.
Todas las preguntas deben ser verificables.
```

**Validaciones:**
- ✅ Información presente en esquema
- ✅ Coherente con legislación
- ✅ Opciones plausibles
- ❌ Rechazar si inventa datos
- ❌ Rechazar si contradice ley

---

## 🔍 DETECCIÓN DE DUPLICADOS

### Análisis de Similitud

**Objetivo**: Detectar si las academias reutilizan preguntas entre sí

**Método**:
```python
# Calcular similitud entre preguntas
similarity = SequenceMatcher(None, pregunta1, pregunta2).ratio()

# Umbrales:
# > 0.95: Duplicado exacto (copiar-pegar)
# 0.85-0.95: Muy similar (ligera modificación)
# 0.70-0.85: Similar (mismo concepto, diferente redacción)
# < 0.70: Diferente
```

**Interpretación**:
- **>95% similitud**: Academia probablemente copió de otra fuente
- **85-95% similitud**: Variación de pregunta existente
- **70-85% similitud**: Mismo concepto, redacción diferente
- **<70% similitud**: Pregunta original

**Conclusión esperada**:
Si encontramos alta similitud (>85%) entre materiales de diferentes academias, confirma que:
1. Las academias NO crean todo desde cero
2. Reutilizan preguntas de exámenes oficiales
3. Hacen variaciones de preguntas existentes
4. **Nosotros podemos hacer lo mismo legalmente**

---

## 📊 FORMATO DE SALIDA

### Estructura JSON Estándar

```json
{
  "pregunta": "Texto exacto de la pregunta",
  "opciones": [
    "a) Primera opción",
    "b) Segunda opción",
    "c) Tercera opción",
    "d) Cuarta opción"
  ],
  "respuesta_correcta": "b",
  "explicacion": "Explicación de por qué es correcta",
  "base_legal": "Art. 205 LGSS",
  "tema": "Jubilación",
  "subtema": "Edad de jubilación",
  "dificultad": "media",
  "metadata": {
    "fuente_original": "Examen C1 SS 26-03-2022",
    "metodo": "extraccion_ollama",
    "fecha_generacion": "2025-12-02T10:30:00",
    "validado": false,
    "requiere_revision": false
  }
}
```

---

## ✅ CHECKLIST DE CALIDAD

Antes de incluir una Q&A en el dataset, verificar:

- [ ] ¿La pregunta está completa?
- [ ] ¿Tiene exactamente 4 opciones?
- [ ] ¿La respuesta correcta está claramente identificada?
- [ ] ¿Hay base legal citada (si aplica)?
- [ ] ¿La fuente está identificada?
- [ ] ¿Es legalmente correcta?
- [ ] ¿Es éticamente apropiada?
- [ ] ¿No viola derechos de autor?

---

## 🚨 CASOS ESPECIALES

### Preguntas con Cálculos

```
PERMITIDO:
"Calcular la base reguladora de una prestación"
✓ Basado en fórmula legal (Art. X LGSS)
✓ Datos de ejemplo inventados
✓ Procedimiento verificable

NO PERMITIDO:
"Calcular usando tabla propietaria de academia"
❌ Tabla con copyright
❌ Método no oficial
```

### Preguntas con Casos Prácticos

```
PERMITIDO:
"Juan, 65 años, 35 años cotizados..."
✓ Caso inventado
✓ Basado en legislación
✓ Solución verificable

NO PERMITIDO:
"Caso práctico del examen de 2026"
❌ Examen futuro
❌ Predicción
```

---

## 📈 MÉTRICAS DE CALIDAD

### Objetivos del Pipeline

| Métrica | Objetivo | Mínimo Aceptable |
|---------|----------|------------------|
| Preguntas extraídas | 1,500 | 1,000 |
| Preguntas generadas | 2,000 | 1,500 |
| Variaciones | 1,500 | 1,000 |
| Tasa de validación | 95% | 90% |
| Duplicados detectados | <5% | <10% |
| Errores legales | 0% | <1% |

---

## 🔄 PROCESO DE REVISIÓN

1. **Generación automática** (Ollama)
2. **Validación automática** (reglas)
3. **Detección de duplicados** (similitud)
4. **Revisión humana** (muestra 10%)
5. **Corrección de errores**
6. **Aprobación final**

---

**Creado**: 2 Diciembre 2025  
**Propósito**: Garantizar generación ética, legal y de calidad
