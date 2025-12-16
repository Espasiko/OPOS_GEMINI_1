# 🎓 Agente Generador de Simulacros - OpositaIA

Agente que genera simulacros y tests de oposiciones usando el MCP de OpositaIA y el RAG de Qdrant.

## 📋 Características

- ✅ **Consultar RAG** - Buscar información legal en Qdrant via MCP
- ✅ **Generar Simulacro 112 preguntas** - Formato oficial BOE-A-2024-11403
- ✅ **Generar Test 80 preguntas** - Tests rápidos personalizables
- ✅ **Modo Chat** - Interacción conversacional con el RAG
- ✅ **Mezcla de opciones** - Las respuestas se mezclan aleatoriamente

## 🚀 Uso Rápido

```bash
# Desde el directorio dataset_generator/agents/simulacro_agent/

# Generar simulacro completo de 112 preguntas
python simulacro_agent.py --simulacro

# Generar test de 80 preguntas
python simulacro_agent.py --test

# Modo chat interactivo
python simulacro_agent.py --chat

# Consulta única al RAG
python simulacro_agent.py --query "¿Cuáles son los requisitos de jubilación anticipada?"

# Personalizar número de preguntas
python simulacro_agent.py --simulacro --num 50
python simulacro_agent.py --test --num 40
```

## 📁 Estructura de Archivos

```
simulacro_agent/
├── agent.yaml           # Configuración del agente
├── simulacro_agent.py   # Script principal
├── mcp_client.py        # Cliente para MCP OpositaIA
├── test_generator.py    # Generador de tests personalizados
└── README.md            # Esta documentación
```

## 🔧 Configuración

### Variables de Entorno Requeridas

El agente usa las variables del MCP server (`mcp-server/.env`):

```env
QDRANT_URL=https://xxx.cloud.qdrant.io
QDRANT_API_KEY=tu_api_key
HUGGINGFACE_TOKEN=tu_hf_token
MISTRAL_API_KEY=tu_mistral_key  # Opcional, para fallback
```

### Dataset de Origen

El agente usa el dataset principal:
- `dataset_generator/DATASET_FINAL_300_SS_AGE.jsonl`

Si no existe, busca alternativas en `dataset_output/`.

## 📊 Formatos de Salida

### Simulacro (112 preguntas)

```json
{
  "metadata": {
    "titulo": "SIMULACRO COMPLETO OFICIAL - Cuerpo Administrativo AGE",
    "total_preguntas": 112,
    "duracion_estimada_minutos": 90,
    "formato_oficial": "BOE-A-2024-11403"
  },
  "parte_1": {
    "nombre": "Test de Conocimientos Generales",
    "preguntas": 25
  },
  "parte_2": {
    "nombre": "Supuestos Prácticos",
    "preguntas": 87
  },
  "preguntas": [
    {
      "numero": 1,
      "parte": 1,
      "pregunta": "...",
      "opciones": {"a": "...", "b": "...", "c": "...", "d": "..."},
      "respuesta_correcta": "b",
      "tema": "...",
      "dificultad": "media"
    }
  ]
}
```

### Test (80 preguntas)

```json
{
  "metadata": {
    "titulo": "TEST RÁPIDO - Seguridad Social y AGE",
    "total_preguntas": 80,
    "duracion_estimada_minutos": 60
  },
  "preguntas": [...]
}
```

## 🎯 Modo Chat - Comandos

| Comando | Descripción |
|---------|-------------|
| `/simulacro` | Generar simulacro de 112 preguntas |
| `/test` | Generar test de 80 preguntas |
| `/colecciones` | Ver colecciones Qdrant |
| `/salir` | Salir del chat |

Cualquier otro texto se interpreta como consulta al RAG.

## 📈 Test Generator Avanzado

Para tests más personalizados:

```python
from test_generator import TestGenerator

gen = TestGenerator()

# Ver temas disponibles
print(gen.get_temas_disponibles())

# Test de un tema específico
test = gen.generar_test_por_tema("Jubilación", num_preguntas=20)

# Test con distribución de dificultad
test = gen.generar_test_mixto(
    num_facil=20,
    num_media=40,
    num_alta=20
)

# Test filtrado
test = gen.generar_test(
    num_preguntas=50,
    temas=["Jubilación", "Incapacidad"],
    dificultad="alta"
)
```

## 🔗 Integración con MCP

El agente usa el MCP de OpositaIA para:

1. **search_rag** - Búsqueda semántica en leyes de Seguridad Social
2. **list_collections** - Ver colecciones disponibles en Qdrant
3. **get_law_summary** - Obtener resúmenes de leyes

### Modelo de Embeddings

- **Modelo**: `pablosi/bge-m3-spa-law-qa-trained-2`
- **Dimensiones**: 1024
- **Provider**: HuggingFace

## 📝 Ejemplo de Sesión

```
$ python simulacro_agent.py --chat

============================================================
🎓 AGENTE OPOSITAIA - Modo Chat
============================================================
Comandos especiales:
  /simulacro - Generar simulacro de 112 preguntas
  /test      - Generar test de 80 preguntas
  /colecciones - Ver colecciones Qdrant
  /salir     - Salir del chat
============================================================

📝 Tu pregunta: ¿Cuántos años de cotización se necesitan para jubilación?

⏳ Buscando en el RAG...

📚 Resultados para: '¿Cuántos años de cotización se necesitan para jubilación?'

**1. (Score: 0.89)**
Según el artículo 205 del TRLGSS, para acceder a la pensión de jubilación 
se requiere un período mínimo de cotización de 15 años...

📝 Tu pregunta: /simulacro

⏳ Generando simulacro de 112 preguntas...
✓ Simulacro guardado en: dataset_output/SIMULACRO_GENERADO_20251216_123456.json

📝 Tu pregunta: /salir
👋 ¡Hasta luego!
```

## 🛠️ Dependencias

```
qdrant-client
requests
python-dotenv
```

Instalar con:
```bash
pip install qdrant-client requests python-dotenv
```

---

**Versión**: 1.0.0  
**Fecha**: 16 Diciembre 2025  
**Autor**: OpositaIA
