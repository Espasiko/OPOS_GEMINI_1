"""
Agente Mistral Optimizado para Generación de Q&A Legal
Configuración corregida y optimizada
"""

import os
from mistralai import Mistral

# Inicializar cliente
client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))

# Mensaje inicial
inputs = [
    {"role": "user", "content": "Hello!"}
]

# Parámetros de completado OPTIMIZADOS
completion_args = {
    "temperature": 0.3,      # ✅ Ajustado de 0.03 a 0.3 (mejor balance)
    "max_tokens": 4096,      # ✅ OK
    # "top_p": 1.0           # ✅ Opcional - puedes omitirlo cuando usas temperature
}

# Herramientas/Funciones
tools = [
    # ⚠️ OPCIONAL: Descomenta si necesitas estas herramientas
    # {
    #     "type": "code_interpreter"
    # },
    # {
    #     "type": "web_search",
    #     "open_results": False
    # },
    
    # ✅ Función 1: Buscar en RAG (Qdrant)
    {
        "type": "function",
        "function": {
            "name": "buscar_rag",
            "description": "Busca información relevante en la base de datos vectorial de legislación española (Qdrant). Utiliza esta función SIEMPRE que necesites información legal específica, citar artículos, verificar datos normativos o generar preguntas de examen. La base de datos contiene: Constitución Española, LGSS, LISOS, LPRL, Estatuto de los Trabajadores, Ley 39/2015, Ley 40/2015 y reglamentos relacionados.",
            "strict": True,
            "parameters": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "La consulta de búsqueda semántica. Debe ser específica y clara. Ejemplos: 'prestación por desempleo requisitos', 'infracciones muy graves LISOS', 'artículo 267 LGSS', 'cotización autónomos'. Usa términos legales precisos cuando sea posible."
                    },
                    "top_k": {
                        "type": "integer",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20,
                        "description": "Número de resultados a devolver. Valores recomendados: 5 para consultas específicas, 10-15 para temas amplios, 20 para búsquedas exhaustivas. Por defecto: 5. Máximo: 20."
                    }
                }
            }
        }
    },
    
    # ✅ Función 2: Verificar URL del BOE
    {
        "type": "function",
        "function": {
            "name": "verificar_url",
            "description": "Verifica si una URL del Boletín Oficial del Estado (BOE) es válida, accesible y está activa. Utiliza esta función cuando proporciones enlaces al BOE, cuando necesites validar referencias legales o cuando cites normativa específica con su URL oficial.",
            "strict": True,
            "parameters": {
                "type": "object",
                "required": ["url"],
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "La URL completa del BOE a verificar. Debe ser una URL válida que comience con 'https://www.boe.es/'. Ejemplos: 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724' (LGSS), 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-10566' (Ley 39/2015)."
                    }
                }
            }
        }
    }
]

# System Prompt
system_instructions = """
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
"""

# Iniciar conversación
response = client.beta.conversations.start(
    inputs=inputs,
    model="mistral-large-latest",
    instructions=system_instructions,
    completion_args=completion_args,
    tools=tools,
)

print(response)
