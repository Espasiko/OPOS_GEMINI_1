# ⚡ Instrucciones Rápidas: Configurar Agente en Mistral Studio

## 🎯 Lo que vas a hacer (5 minutos)

Vas a crear un agente en Mistral Studio que puede:
- ✅ Buscar en tu base de datos de leyes (Qdrant)
- ✅ Verificar URLs del BOE
- ✅ Generar preguntas de examen
- ✅ Responder consultas legales con referencias

---

## 📝 Paso 1: Abrir Mistral Studio

1. Ve a: **https://console.mistral.ai/**
2. Inicia sesión
3. Click en **"Agents"** en el menú lateral
4. Click en **"Create Agent"** o **"New Agent"**

---

## 📝 Paso 2: Configuración Básica

**Nombre del agente:**
```
Experto Oposiciones Seguridad Social
```

**Modelo:**
```
mistral-large-latest
```

**Temperature:**
```
0.3
```

---

## 📝 Paso 3: System Prompt

**Copia y pega esto en el campo "System Instructions":**

```
Eres un experto en oposiciones de Seguridad Social en España. Tu objetivo es ayudar a opositores a prepararse para exámenes oficiales.

## Tu conocimiento base

Tienes acceso a una base de datos vectorial (Qdrant) con:
- Constitución Española
- Ley General de la Seguridad Social (LGSS)
- Ley de Infracciones y Sanciones (LISOS)
- Ley de Prevención de Riesgos Laborales (LPRL)
- Estatuto de los Trabajadores
- Ley 39/2015 de Procedimiento Administrativo
- Ley 40/2015 de Régimen Jurídico
- Reglamentos y Reales Decretos relacionados

## Cómo debes trabajar (DATASET FINETUNING)

1. **USA `buscar_rag`** para obtener información legal
2. **Genera UNA pregunta con UNA respuesta correcta** (SIN opciones múltiples)
3. **VERIFICA ley y artículos** - deben existir en BOE
4. **Devuelve SOLO**: pregunta + respuesta + ley + artículos
5. **NO resúmenes, NO explicaciones largas**

## IMPORTANTE: Variación en respuestas

❌ NO empieces SIEMPRE con "Según el artículo X..." o "La ley Y establece..."
✅ VARÍA el inicio de tus respuestas:
- "La edad de jubilación es..."
- "Para acceder a esta prestación se requiere..."
- "En 2024, los requisitos son..."
- "El artículo 205 LGSS establece..." (solo a veces)

## Formato de respuestas (DATASET FINETUNING)

### Para preguntas de examen - FORMATO EXACTO:
```
PREGUNTA: [Pregunta directa sobre legislación]
RESPUESTA: [Respuesta correcta verificada]
LEY: [Nombre de la ley]
ARTÍCULO: [Art. X, Y, Z]
```

### EJEMPLO CORRECTO:
```
PREGUNTA: ¿Cuál es la edad ordinaria de jubilación en 2024?
RESPUESTA: 66 años y 6 meses
LEY: Ley General de la Seguridad Social
ARTÍCULO: Art. 205.1.a
```

### REGLAS:
- ❌ NO opciones múltiples (A, B, C, D)
- ❌ NO resúmenes
- ❌ NO explicaciones largas
- ✅ UNA pregunta, UNA respuesta correcta verificada
- ✅ Ley y artículos VERIFICADOS en BOE

### Para consultas legales:
```
[Respuesta directa y clara - VARÍA el inicio, no uses siempre "Según el artículo..."]

**Fundamento legal:**
- [Ley X, Art. Y]: [Texto relevante o resumen]
- [Ley Z, Art. W]: [Texto relevante o resumen]

**Contexto adicional:** [Si es relevante]
```

## Verificación de URLs del BOE

Cuando cites una URL del BOE:
1. **USA la función `verificar_url`** con los parámetros `articulo_citado` y `ley_esperada`
2. **VERIFICA el título del documento** - debe corresponder con la ley que citas
3. **SI citas un artículo específico**, la función verificará que ese artículo existe
4. **RECHAZA URLs** que sean de ayuntamientos, resoluciones de nombramientos, o documentos que NO sean leyes

Ejemplo de uso correcto:
```
verificar_url(
  url="https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
  articulo_citado="205",
  ley_esperada="LGSS"
)
```

## Reglas importantes

❌ NO inventes información legal
❌ NO inventes URLs
❌ NO resúmenes ni explicaciones largas
❌ NO uses URLs sin verificar
❌ NO cites artículos que no existan
✅ UNA pregunta + respuesta + URL + artículos
✅ URL VERIFICADA (título = ley citada)
✅ Artículos VERIFICADOS
✅ Rechaza URLs de ayuntamientos/nombramientos
```

---

## 📝 Paso 4: Añadir Funciones

### Opción A: Importar JSON (MÁS RÁPIDO) ⭐

1. Abre el archivo: **`FUNCIONES_AGENTE_MISTRAL_CORRECTO.json`**
2. Selecciona TODO el contenido (Ctrl+A)
3. Copia (Ctrl+C)
4. En Mistral Studio, ve a la sección **"Tools"**
5. Click en **"Import JSON"** o **"Add from JSON"**
6. Pega el contenido (Ctrl+V)
7. Click en **"Import"** o **"Save"**

### Opción B: Copiar manualmente (si no hay opción de importar)

#### Función 1: buscar_rag

**Name:**
```
buscar_rag
```

**Description:**
```
Busca información relevante en la base de datos vectorial de legislación española (Qdrant). Utiliza esta función SIEMPRE que necesites información legal específica, citar artículos, verificar datos normativos o generar preguntas de examen. La base de datos contiene: Constitución Española, LGSS, LISOS, LPRL, Estatuto de los Trabajadores, Ley 39/2015, Ley 40/2015 y reglamentos relacionados.
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "La consulta de búsqueda semántica. Debe ser específica y clara. Ejemplos: 'prestación por desempleo requisitos', 'infracciones muy graves LISOS', 'artículo 267 LGSS', 'cotización autónomos'. Usa términos legales precisos cuando sea posible."
    },
    "top_k": {
      "type": "integer",
      "description": "Número de resultados a devolver. Valores recomendados: 5 para consultas específicas, 10-15 para temas amplios, 20 para búsquedas exhaustivas. Por defecto: 5. Máximo: 20.",
      "default": 5,
      "minimum": 1,
      "maximum": 20
    }
  },
  "required": ["query"]
}
```

#### Función 2: verificar_url

**Name:**
```
verificar_url
```

**Description:**
```
Verifica si una URL del BOE es válida y contiene el contenido esperado. CRÍTICO: Extrae el TÍTULO REAL del documento para verificar que es una ley (NO resoluciones de ayuntamientos, nombramientos, etc.). Si citas un artículo, verifica que existe en el documento.
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "url": {
      "type": "string",
      "description": "La URL completa del BOE a verificar. Debe comenzar con 'https://www.boe.es/'."
    },
    "articulo_citado": {
      "type": "string",
      "description": "OBLIGATORIO si citas un artículo. Número del artículo (ej: '205', '267.1'). Verifica que existe en el documento."
    },
    "ley_esperada": {
      "type": "string",
      "description": "RECOMENDADO. Nombre de la ley esperada (ej: 'LGSS', 'LISOS'). Compara con el título real del documento."
    }
  },
  "required": ["url"]
}
```

#### Función 3: generar_pregunta_test (NUEVA)

**Name:**
```
generar_pregunta_test
```

**Description:**
```
Genera UNA pregunta con UNA respuesta correcta verificada (SIN opciones múltiples). Para dataset de finetuning.
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "tema": {
      "type": "string",
      "description": "El tema sobre el que generar la pregunta."
    },
    "dificultad": {
      "type": "string",
      "enum": ["basica", "intermedia", "avanzada", "truco"],
      "description": "Nivel de dificultad de la pregunta."
    }
  },
  "required": ["tema"]
}
```

---

## 📝 Paso 5: Configurar Tool Choice

En la configuración del agente:

**Tool Choice:**
```
auto
```

**Parallel Tool Calls:**
```
true (activado)
```

---

## 📝 Paso 6: Guardar

Click en **"Save Agent"** o **"Create Agent"**

---

## ✅ Paso 7: Probar

Ve a la sección **"Test"** o **"Playground"** y prueba con:

### Prueba 1:
```
¿Cuáles son los requisitos para la prestación por desempleo?
```

**Debe:**
- ✅ Llamar a `buscar_rag`
- ✅ Responder con información legal
- ✅ Citar fuentes: [LGSS, Art. X]

### Prueba 2:
```
Genera una pregunta sobre infracciones laborales graves
```

**Debe:**
- ✅ Llamar a `buscar_rag`
- ✅ Generar UNA pregunta con UNA respuesta correcta (SIN opciones múltiples)
- ✅ Incluir ley y artículo verificados
- ✅ NO empezar con "Según el artículo..."

### Prueba 3:
```
¿Es válida esta URL? https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724
```

**Debe:**
- ✅ Llamar a `verificar_url`
- ✅ Confirmar si es válida
- ✅ Proporcionar información del documento

---

## 🎉 ¡Listo!

Si las 3 pruebas funcionan, tu agente está correctamente configurado.

---

## 🐛 Si algo no funciona

### El agente no llama a las funciones
- Verifica que Tool Choice esté en `auto`
- Asegúrate de que las funciones estén guardadas
- Prueba con: "Usa la función buscar_rag para buscar información sobre..."

### Error en el JSON
- Copia el JSON exactamente como está
- Verifica que no haya caracteres extra
- Usa la Opción A (importar JSON completo)

### El agente inventa información
- Reduce temperature a `0.2`
- Verifica que el System Prompt esté completo
- Añade al prompt: "NUNCA inventes información legal"

---

## 📚 Archivos de Referencia

Si necesitas más información, consulta:

1. **FUNCIONES_AGENTE_MISTRAL_CORRECTO.json** - Las funciones para copiar
2. **CONFIGURAR_AGENTE_MISTRAL_STUDIO.md** - Guía detallada paso a paso
3. **GUIA_CONFIGURAR_AGENTE_MISTRAL_CON_QDRANT.md** - Documentación completa
4. **DIAGRAMA_FLUJO_AGENTE_MISTRAL.md** - Cómo funciona todo
5. **RESUMEN_CONFIGURACION_AGENTE_MISTRAL.md** - Resumen ejecutivo

---

## ⏱️ Tiempo Total

- Configuración básica: 2 minutos
- Copiar System Prompt: 1 minuto
- Añadir funciones: 2 minutos
- Probar: 2 minutos

**Total: ~7 minutos**

---

## 🎯 Resultado Final

Tendrás un agente que:
- 🔍 Busca en 15,234 chunks de legislación
- 📚 Cita fuentes legales correctamente
- ❓ Genera UNA pregunta con UNA respuesta correcta VERIFICADA (SIN opciones múltiples)
- ✅ Verifica ley y artículos en BOE
- ❌ Rechaza URLs falsas (ayuntamientos, nombramientos, resoluciones)
- 🔄 Varía el inicio de respuestas (no siempre "Según el artículo...")
- 🎓 Ayuda a preparar oposiciones de Seguridad Social
- 🔒 NUNCA inventa datos - TODO verificado en BOE

---

## 📋 Cambios v2.2 (4 dic 2025)
- ✅ Formato correcto: UNA pregunta, UNA respuesta (SIN opciones múltiples A/B/C/D)
- ✅ Verifica ley y artículos en BOE
- ✅ Instrucciones para variar inicio de respuestas (no siempre "Según el artículo...")
- ✅ NUNCA inventa datos - TODO debe ser verificado en BOE
- ✅ Formato: PREGUNTA + RESPUESTA + LEY + ARTÍCULO

---

**¿Listo? ¡Adelante!** 🚀

Abre Mistral Studio y sigue los pasos. En menos de 10 minutos tendrás tu agente funcionando.
