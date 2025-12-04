# ✅ Revisión del Código del Agente Mistral

## 📊 Estado General: **CASI PERFECTO** ⭐⭐⭐⭐½

Tu configuración está **muy bien**, solo hay algunos ajustes menores.

---

## ✅ Lo que está BIEN

### 1. Estructura General ✅
```python
from mistralai import Mistral
client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
```
- ✅ Importación correcta
- ✅ API key desde variable de entorno (seguro)

### 2. Funciones Configuradas ✅
```python
{
    "type": "function",
    "function": {
        "name": "buscar_rag",
        "description": "...",
        "strict": true,  # ✅ Buena práctica
        "parameters": {...}
    }
}
```
- ✅ Las 2 funciones están correctamente definidas
- ✅ `strict: true` es buena práctica
- ✅ Parámetros bien estructurados

### 3. System Prompt ✅
- ✅ Muy completo y detallado
- ✅ Incluye reglas claras
- ✅ Formato JSON estructurado

---

## ⚠️ Ajustes Recomendados

### 1. Temperature muy baja
```python
"temperature": 0.03,  # ⚠️ DEMASIADO BAJO
```

**Problema:** Con 0.03 el modelo será extremadamente determinista y puede ser repetitivo.

**Recomendación:**
```python
"temperature": 0.3,  # ✅ MEJOR para respuestas legales
```

**Razón:** 0.3 mantiene precisión pero permite algo de variabilidad natural.


### 2. Top_p muy bajo
```python
"top_p": 0.01,  # ⚠️ DEMASIADO RESTRICTIVO
```

**Problema:** Con top_p=0.01 solo considera el 1% de tokens más probables.

**Recomendación:**
```python
"top_p": 1.0,  # ✅ MEJOR (valor por defecto)
# O elimina este parámetro si usas temperature
```

**Razón:** Cuando usas `temperature`, no necesitas `top_p` tan bajo. Son métodos alternativos de sampling.

### 3. Herramientas adicionales
```python
{
    "type": "code_interpreter"  # ⚠️ ¿Lo necesitas?
},
{
    "type": "web_search",  # ⚠️ ¿Lo necesitas?
    "open_results": false
}
```

**Pregunta:** ¿Realmente necesitas estas herramientas?

**Recomendación:**
- Si solo quieres usar tus funciones personalizadas → **Elimínalas**
- Si quieres que el agente pueda buscar en web → **Déjalas**

**Para dataset Q&A:** Probablemente NO las necesites. Solo `buscar_rag` y `verificar_url`.

---

## 🔧 Código Optimizado Recomendado

```python
import os
from mistralai import Mistral

client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))

inputs = [
    {"role": "user", "content": "Hello!"}
]

completion_args = {
    "temperature": 0.3,      # ✅ Ajustado
    "max_tokens": 4096,      # ✅ OK
    # "top_p": 1.0           # ✅ Opcional, puedes omitirlo
}

tools = [
    # ⚠️ Elimina estas si no las necesitas:
    # {
    #     "type": "code_interpreter"
    # },
    # {
    #     "type": "web_search",
    #     "open_results": false
    # },
    
    # ✅ Tus funciones personalizadas:
    {
        "type": "function",
        "function": {
            "name": "buscar_rag",
            "description": "Busca información relevante en la base de datos vectorial...",
            "strict": true,
            "parameters": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "La consulta de búsqueda semántica..."
                    },
                    "top_k": {
                        "type": "integer",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20,
                        "description": "Número de resultados a devolver..."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "verificar_url",
            "description": "Verifica si una URL del BOE es válida...",
            "strict": true,
            "parameters": {
                "type": "object",
                "required": ["url"],
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "La URL completa del BOE a verificar..."
                    }
                }
            }
        }
    }
]

response = client.beta.conversations.start(
    inputs=inputs,
    model="mistral-large-latest",
    instructions="""[TU SYSTEM PROMPT AQUÍ]""",
    completion_args=completion_args,
    tools=tools,
)

print(response)
```

---

## 📝 Respuesta a tu Pregunta sobre Dataset Q&A

### ¿4 opciones o solo la correcta para fine-tuning?

**Respuesta corta:** Depende del objetivo del fine-tuning.

### Opción 1: Solo respuesta correcta (Recomendado para fine-tuning general)

```json
{
  "messages": [
    {
      "role": "user",
      "content": "¿Cuál es la edad ordinaria de jubilación en 2024?"
    },
    {
      "role": "assistant",
      "content": "La edad ordinaria de jubilación en 2024 es de 66 años y 6 meses, según el artículo 205.1.a) de la LGSS (Real Decreto Legislativo 8/2015)."
    }
  ]
}
```

**Ventajas:**
- ✅ Más simple
- ✅ Enfoca el modelo en dar respuestas correctas
- ✅ Menos tokens por ejemplo
- ✅ Más ejemplos con el mismo presupuesto

**Desventajas:**
- ❌ No entrena al modelo a generar distractores
- ❌ No aprende formato de examen

### Opción 2: Con 4 opciones (Recomendado para generar exámenes)

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Genera una pregunta tipo test sobre edad de jubilación en 2024"
    },
    {
      "role": "assistant",
      "content": "**Pregunta:** ¿Cuál es la edad ordinaria de jubilación en 2024?\n\nA) 65 años\nB) 66 años\nC) 66 años y 6 meses\nD) 67 años\n\n**Respuesta correcta:** C\n\n**Explicación:** Según el art. 205.1.a) LGSS, en 2024 la edad ordinaria es 66 años y 6 meses.\n\n**Fuente:** LGSS, Art. 205.1.a)"
    }
  ]
}
```

**Ventajas:**
- ✅ Entrena al modelo a generar exámenes completos
- ✅ Aprende a crear distractores plausibles
- ✅ Formato profesional de oposición

**Desventajas:**
- ❌ Más tokens por ejemplo
- ❌ Más complejo de generar
- ❌ Menos ejemplos con el mismo presupuesto

---

## 🎯 Recomendación Final

### Para tu caso (OpositAI):

**Usa AMBOS formatos en tu dataset:**

1. **70% con 4 opciones** (formato examen)
   - Para entrenar generación de preguntas tipo test
   - Con distractores plausibles
   - Formato completo de oposición

2. **30% solo respuesta correcta** (formato consulta)
   - Para entrenar respuestas directas
   - Explicaciones con referencias legales
   - Consultas de estudio

### Ejemplo de dataset mixto:

```jsonl
{"messages": [{"role": "user", "content": "Genera pregunta sobre jubilación"}, {"role": "assistant", "content": "**Pregunta:** ¿Cuál es la edad...?\n\nA) 65 años\nB) 66 años\nC) 66 años y 6 meses\nD) 67 años\n\n**Respuesta correcta:** C..."}]}
{"messages": [{"role": "user", "content": "¿Qué es la base reguladora?"}, {"role": "assistant", "content": "La base reguladora es la cantidad que sirve de referencia para calcular prestaciones..."}]}
{"messages": [{"role": "user", "content": "Genera pregunta sobre LISOS"}, {"role": "assistant", "content": "**Pregunta:** ¿Cuál es infracción muy grave?\n\nA)...\nB)...\nC)...\nD)...\n\n**Respuesta correcta:** B..."}]}
```

---

## 📊 Comparación de Enfoques

| Aspecto | Solo Correcta | Con 4 Opciones | Mixto (70/30) |
|---------|---------------|----------------|---------------|
| Tokens/ejemplo | ~200 | ~400 | ~340 |
| Ejemplos con 1M tokens | ~5,000 | ~2,500 | ~2,940 |
| Genera exámenes | ❌ | ✅ | ✅ |
| Responde consultas | ✅ | ⚠️ | ✅ |
| Crea distractores | ❌ | ✅ | ✅ |
| Versatilidad | ⚠️ | ⚠️ | ✅✅✅ |
| **Recomendación** | 🟡 | 🟡 | 🟢 **MEJOR** |

---

## 🎓 Conclusión

### Tu código está **95% correcto**. Solo ajusta:

1. ✅ `temperature: 0.3` (en vez de 0.03)
2. ✅ Elimina `top_p` o ponlo en 1.0
3. ✅ Considera eliminar `code_interpreter` y `web_search` si no los necesitas

### Para el dataset:

**Usa formato MIXTO:**
- 70% con 4 opciones (para generar exámenes)
- 30% solo respuesta (para consultas directas)

Esto te dará un modelo versátil que puede:
- ✅ Generar preguntas tipo test completas
- ✅ Responder consultas directas
- ✅ Crear distractores plausibles
- ✅ Explicar con referencias legales

---

**¿Necesitas que te ayude a ajustar el código o a crear el dataset mixto?**
