# 🎯 Configurar Agente en Mistral Studio - Paso a Paso

## 📋 Requisitos Previos

- ✅ Cuenta en Mistral AI (https://console.mistral.ai/)
- ✅ Acceso a Mistral Studio
- ✅ Qdrant Cloud configurado con la colección `leyes_seguridad_social`
- ✅ Archivos preparados:
  - `FUNCIONES_AGENTE_MISTRAL_CORRECTO.json` (funciones/tools)
  - `GUIA_CONFIGURAR_AGENTE_MISTRAL_CON_QDRANT.md` (system prompt)

---

## 🚀 Paso 1: Crear Nuevo Agente

1. Ve a **Mistral Studio**: https://console.mistral.ai/
2. En el menú lateral, selecciona **"Agents"**
3. Haz clic en **"Create Agent"** o **"New Agent"**
4. Asigna un nombre: **"Experto Oposiciones Seguridad Social"**

---

## ⚙️ Paso 2: Configurar Modelo Base

En la sección de configuración del agente:

1. **Model**: Selecciona `mistral-large-latest` o `mistral-large-2411`
   - Este es el modelo más potente y preciso de Mistral
   - Ideal para tareas que requieren razonamiento complejo

2. **Temperature**: Establece en `0.3`
   - Valores bajos (0.2-0.3) = respuestas más deterministas y precisas
   - Perfecto para información legal que debe ser exacta

3. **Max Tokens**: Deja el valor por defecto o ajusta según necesites
   - Recomendado: 4096 para respuestas completas

---

## 📝 Paso 3: Configurar System Prompt

Copia y pega el siguiente prompt en el campo **"System Instructions"** o **"System Prompt"**:

```markdown
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

## Cómo debes trabajar

1. **SIEMPRE usa la función `buscar_rag`** cuando necesites información legal específica
2. **Cita las fuentes** con formato: [Ley X, Art. Y]
3. **Genera preguntas tipo test** con 4 opciones (A, B, C, D) cuando te lo pidan
4. **Explica el razonamiento** de las respuestas correctas
5. **Verifica URLs** del BOE cuando sea necesario usando `verificar_url`

## Formato de respuestas

### Para preguntas de examen:
```
**Pregunta X:** [Enunciado claro y preciso]

A) [Opción incorrecta pero plausible]
B) [Opción correcta]
C) [Opción incorrecta pero plausible]
D) [Opción incorrecta pero plausible]

**Respuesta correcta:** B

**Explicación:** [Justificación con referencia legal]
**Fuente:** [Ley X, Art. Y, apartado Z]
```

### Para consultas legales:
```
[Respuesta directa y clara]

**Fundamento legal:**
- [Ley X, Art. Y]: [Texto relevante o resumen]
- [Ley Z, Art. W]: [Texto relevante o resumen]

**Contexto adicional:** [Si es relevante]
```

## Reglas importantes

❌ NO inventes información legal
❌ NO cites artículos sin haberlos buscado en la base de datos
✅ SI no encuentras información, dilo claramente
✅ SI hay dudas, busca en múltiples fuentes
✅ SIEMPRE prioriza la precisión sobre la velocidad
```

---

## 🔧 Paso 4: Añadir Funciones (Tools)

### Opción A: Copiar JSON completo

1. Ve a la sección **"Tools"** o **"Functions"**
2. Haz clic en **"Add Tool"** o **"Import JSON"**
3. Abre el archivo `FUNCIONES_AGENTE_MISTRAL_CORRECTO.json`
4. Copia TODO el contenido del archivo
5. Pégalo en el campo de importación
6. Haz clic en **"Import"** o **"Save"**

### Opción B: Añadir función por función

#### Función 1: buscar_rag

1. Haz clic en **"Add Tool"** o **"New Function"**
2. Rellena los campos:

**Name:** `buscar_rag`

**Description:**
```
Busca información relevante en la base de datos vectorial de legislación española (Qdrant). Utiliza esta función SIEMPRE que necesites información legal específica, citar artículos, verificar datos normativos o generar preguntas de examen. La base de datos contiene: Constitución Española, LGSS, LISOS, LPRL, Estatuto de los Trabajadores, Ley 39/2015, Ley 40/2015 y reglamentos relacionados.
```

**Parameters Schema:**
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

3. Guarda la función

#### Función 2: verificar_url

1. Haz clic en **"Add Tool"** o **"New Function"** nuevamente
2. Rellena los campos:

**Name:** `verificar_url`

**Description:**
```
Verifica si una URL del Boletín Oficial del Estado (BOE) es válida, accesible y está activa. Utiliza esta función cuando proporciones enlaces al BOE, cuando necesites validar referencias legales o cuando cites normativa específica con su URL oficial.
```

**Parameters Schema:**
```json
{
  "type": "object",
  "properties": {
    "url": {
      "type": "string",
      "description": "La URL completa del BOE a verificar. Debe ser una URL válida que comience con 'https://www.boe.es/'. Ejemplos: 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724' (LGSS), 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-10566' (Ley 39/2015)."
    }
  },
  "required": ["url"]
}
```

3. Guarda la función

---

## 🎛️ Paso 5: Configurar Tool Choice

En la configuración del agente:

1. **Tool Choice**: Selecciona `"auto"`
   - Permite al modelo decidir cuándo usar las funciones
   - Alternativas:
     - `"any"`: Fuerza el uso de al menos una función
     - `"none"`: Desactiva el uso de funciones

2. **Parallel Tool Calls**: Deja en `true` (activado)
   - Permite al modelo llamar múltiples funciones simultáneamente
   - Mejora la eficiencia en consultas complejas

---

## ✅ Paso 6: Guardar y Probar

1. Haz clic en **"Save Agent"** o **"Create Agent"**
2. Ve a la sección de **"Test"** o **"Playground"**
3. Prueba con estas consultas:

### Prueba 1: Consulta Simple
```
¿Cuáles son los requisitos para la prestación por desempleo?
```

**Resultado esperado:**
- El agente debe llamar a `buscar_rag`
- Debe proporcionar información con citas legales
- Formato: [LGSS, Art. X]

### Prueba 2: Generar Pregunta
```
Genera una pregunta tipo test sobre infracciones laborales graves
```

**Resultado esperado:**
- El agente debe llamar a `buscar_rag`
- Debe generar una pregunta con 4 opciones
- Debe incluir respuesta correcta y explicación

### Prueba 3: Verificar URL
```
¿Es válida esta URL? https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724
```

**Resultado esperado:**
- El agente debe llamar a `verificar_url`
- Debe confirmar si la URL es válida
- Debe proporcionar información sobre el documento

---

## 🔍 Verificación de Configuración

Usa este checklist para asegurarte de que todo está correcto:

- [ ] Agente creado con nombre descriptivo
- [ ] Modelo: `mistral-large-latest` o `mistral-large-2411`
- [ ] Temperature: `0.3`
- [ ] System Prompt copiado correctamente
- [ ] Función `buscar_rag` añadida con parámetros correctos
- [ ] Función `verificar_url` añadida con parámetros correctos
- [ ] Tool Choice: `auto`
- [ ] Parallel Tool Calls: `true`
- [ ] Prueba 1 (consulta simple) funciona ✅
- [ ] Prueba 2 (generar pregunta) funciona ✅
- [ ] Prueba 3 (verificar URL) funciona ✅

---

## 🐛 Troubleshooting

### Problema: El agente no llama a las funciones

**Solución:**
1. Verifica que Tool Choice esté en `"auto"` o `"any"`
2. Asegúrate de que las funciones estén guardadas correctamente
3. Revisa que el System Prompt incluya instrucciones para usar las funciones
4. Prueba con una consulta más explícita: "Usa la función buscar_rag para encontrar información sobre..."

### Problema: Error en el formato de las funciones

**Solución:**
1. Verifica que el JSON esté bien formado (sin comas extras, comillas correctas)
2. Asegúrate de que `"type": "object"` esté en `parameters`
3. Verifica que `"required"` sea un array: `["query"]`
4. Comprueba que no haya caracteres especiales mal escapados

### Problema: El agente inventa información

**Solución:**
1. Reduce la temperatura a `0.2`
2. Refuerza en el System Prompt: "NO inventes información legal"
3. Añade: "Si no encuentras información con buscar_rag, dilo claramente"
4. Verifica que el agente esté usando las funciones correctamente

### Problema: Las respuestas son muy cortas o incompletas

**Solución:**
1. Aumenta Max Tokens a 4096 o más
2. Ajusta `top_k` en las consultas a 10-15
3. Pide explícitamente respuestas detalladas en el System Prompt

---

## 📚 Recursos Adicionales

- **Documentación Mistral Function Calling:** https://docs.mistral.ai/capabilities/function_calling
- **Mistral Studio:** https://console.mistral.ai/
- **Guía completa del proyecto:** Ver `GUIA_CONFIGURAR_AGENTE_MISTRAL_CON_QDRANT.md`

---

## 🎯 Próximos Pasos

Una vez configurado el agente:

1. **Prueba exhaustiva:** Realiza múltiples consultas de diferentes tipos
2. **Ajusta el prompt:** Refina el System Prompt según los resultados
3. **Optimiza parámetros:** Ajusta temperatura y top_k según necesites
4. **Añade más funciones:** Considera añadir funciones adicionales como:
   - `generar_examen_completo`
   - `explicar_articulo_detallado`
   - `comparar_versiones_ley`

---

**Última actualización:** 4 de diciembre de 2025
**Versión:** 1.0
**Autor:** Sistema OpositAI
