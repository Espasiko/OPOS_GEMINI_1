# 🤖 ANÁLISIS DE CAPACIDADES DE MODELOS Y ESTRATEGIA ÓPTIMA

**Fecha:** 23 Diciembre 2025 20:25  
**Objetivo:** Determinar la mejor estrategia para cada modelo según sus capacidades

---

## 📊 COMPARATIVA DE CAPACIDADES POR MODELO

### 1. **DeepSeek V3.2 / V3.2-Speciale** (Diciembre 2025)

#### ✅ **Capacidades Únicas**
- **Reasoning Integrado:** "Thinking in Tool-Use" nativo
- **Modos Duales:** Thinking (CoT) y Non-Thinking (directo)
- **Tool-Use Optimizado:** Post-training específico para agentes
- **Contexto:** 128K tokens
- **API:** Compatible OpenAI

#### 🎯 **Mejor Uso**
```python
# DeepSeek V3.2 NO necesita estrategia 2-pass
# El reasoning ya está integrado

{
  "model": "deepseek-chat",  # V3.2 es el chat actual
  "messages": [...],
  "tools": [...],  # Soporta tools nativamente
  "temperature": 0.3
}
```

#### ⚠️ **Limitaciones**
- ❌ **NO soporta Batch API** (solo chat síncrono)
- ❌ **NO soporta MCP remoto** (solo function calling estándar)
- ✅ **SÍ soporta JSON mode** y tool calls

#### 💰 **Coste**
- Muy económico (~$0.27/M tokens input, $1.10/M output)

---

### 2. **Groq (Llama 3.3 70B + OSS 120B)**

#### ✅ **Capacidades Únicas**
- **Velocidad Extrema:** 3-5x más rápido que otros
- **Batch API:** Procesamiento asíncrono masivo
- **MCP Remoto:** Soporte nativo para MCP servers
- **Modelos Múltiples:**
  - `llama-3.3-70b-versatile` (general)
  - `llama-3.3-70b-specdec` (razonamiento)
  - `gpt-oss-120b` (juez/auditor)

#### 🎯 **Mejor Uso**
```python
# Groq es IDEAL para generación masiva con MCP

# 1. Con MCP Remoto (RECOMENDADO)
{
  "model": "llama-3.3-70b-versatile",
  "messages": [...],
  "tools": [
    {
      "type": "mcp",
      "mcp": {
        "server_url": "http://localhost:3000/mcp",
        "tools": ["buscar_rag", "consultar_boe"]
      }
    }
  ]
}

# 2. Con Batch API (para 100+ items)
# Subir archivo JSONL → Procesar async → Descargar resultados
```

#### ⚠️ **Limitaciones**
- ⚠️ **Reasoning limitado** (necesita 2-pass para casos complejos)
- ✅ **Excelente con tools** y MCP

#### 💰 **Coste**
- Muy económico (~$0.05-0.10/M tokens)

---

### 3. **Mistral (Agents API)**

#### ✅ **Capacidades Únicas**
- **Agents API:** Agentes pre-configurados con tools
- **Function Calling:** Muy robusto
- **Pausas Automáticas:** Rate limiting inteligente
- **Modelos:**
  - `mistral-small-latest` (rápido, barato)
  - `mistral-large-latest` (calidad alta)

#### 🎯 **Mejor Uso**
```python
# Mistral con Agents API (YA PROBADO CON ÉXITO)

from mistralai import Mistral
from mistralai.models import UserMessage, ToolMessage

client = Mistral(api_key=MISTRAL_API_KEY)

# Usar AGENT_ID pre-configurado con tools
response = client.agents.complete(
    agent_id="ag_019ad601946d7323a81c544229de40a1",
    messages=[UserMessage(content=prompt)]
)

# El agente llama automáticamente a buscar_rag
# Nosotros ejecutamos la tool y devolvemos resultado
```

#### ⚠️ **Limitaciones**
- ⚠️ **Rate Limits estrictos** (necesita pausas)
- ❌ **NO tiene Batch API**
- ✅ **Excelente con tools** (mejor que Groq)

#### 💰 **Coste**
- Moderado (~$0.30/M tokens small, ~$2/M large)

---

## 🎯 ESTRATEGIA ÓPTIMA POR TIPO DE CONTENIDO

### 📚 **Razonamientos Legales (118 → 236 items)**

**Modelo Recomendado:** **DeepSeek V3.2**

**Por qué:**
- ✅ Reasoning integrado (no necesita 2-pass)
- ✅ Soporta tools para RAG
- ✅ Muy económico
- ✅ Contexto 128K (casos largos)

**Script:** `generate_razonamiento_deepseek_v3.py`

---

### 📝 **Simulacros de Examen (50 → 100 bloques)**

**Modelo Recomendado:** **Groq Batch API**

**Por qué:**
- ✅ Velocidad extrema
- ✅ Batch API (100 bloques en paralelo)
- ✅ MCP remoto para verificación BOE
- ✅ Muy económico

**Script:** `generate_simulacros_groq_batch.py`

---

### 📊 **Esquemas/Comparativas/Plazos (120 items)**

**Modelo Recomendado:** **Mistral Agents**

**Por qué:**
- ✅ Agents API con tools pre-configurados
- ✅ Excelente para contenido estructurado
- ✅ Pausas automáticas (no satura API)
- ✅ Ya probado con éxito

**Script:** `generate_estructurados_mistral_agent.py`

---

### 🎴 **Flashcards (25 → 50 items)**

**Modelo Recomendado:** **Groq (simple)**

**Por qué:**
- ✅ Contenido corto (no necesita reasoning)
- ✅ Muy rápido
- ✅ Muy barato

**Script:** `generate_flashcards_groq.py`

---

## 🔧 HERRAMIENTAS (TOOLS) OPTIMIZADAS

### Tool 1: `buscar_rag` (Para todos los modelos)

```json
{
  "type": "function",
  "function": {
    "name": "buscar_rag",
    "description": "Busca legislación oficial en Qdrant + PostgreSQL. Devuelve texto exacto de leyes con URLs BOE reales.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "Consulta legal (ej: 'artículo 215 LGSS jubilación parcial')"
        },
        "top_k": {
          "type": "integer",
          "description": "Número de documentos a recuperar (default: 5)",
          "default": 5
        }
      },
      "required": ["query"]
    }
  }
}
```

### Tool 2: `verificar_articulo_boe` (Para verificación)

```json
{
  "type": "function",
  "function": {
    "name": "verificar_articulo_boe",
    "description": "Verifica que un artículo existe en PostgreSQL y devuelve su URL BOE real.",
    "parameters": {
      "type": "object",
      "properties": {
        "articulo": {
          "type": "string",
          "description": "Número de artículo (ej: '215')"
        },
        "ley": {
          "type": "string",
          "description": "Nombre de la ley (ej: 'Ley General de la Seguridad Social')"
        }
      },
      "required": ["articulo", "ley"]
    }
  }
}
```

---

## 📋 PROMPTS OPTIMIZADOS POR MODELO

### Prompt para DeepSeek V3.2 (Razonamiento)

```python
PROMPT_DEEPSEEK_RAZONAMIENTO = """
Eres un Magistrado del Tribunal Supremo especializado en Seguridad Social.

TEMA: {topic}

CONTEXTO LEGAL (de Qdrant):
{context_rag}

TAREA:
Genera un CASO PRÁCTICO de razonamiento jurídico complejo.

INSTRUCCIONES:
1. Usa SOLO información del contexto legal proporcionado
2. Cita artículos EXACTOS que aparecen en el contexto
3. Incluye URLs BOE del contexto
4. Razona paso a paso (tu thinking mode se activará automáticamente)

FORMATO JSON:
{{
  "planteamiento": "Hechos del caso con fechas concretas...",
  "cuestion": "Pregunta jurídica compleja...",
  "razonamiento_pasos": [
    "Paso 1: Analizar Art. X de Ley Y (URL: ...)...",
    "Paso 2: Verificar plazo de Z días...",
    "Paso 3: Descartar opción A porque...",
    "Paso 4: Aplicar jurisprudencia..."
  ],
  "solucion_final": "...",
  "articulos_citados": [
    {{"articulo": "Art. 215", "ley": "LGSS", "url_boe": "https://..."}}
  ]
}}
"""
```

### Prompt para Groq Batch (Simulacros)

```python
PROMPT_GROQ_SIMULACRO = """
Eres un Tribunal de Oposiciones oficial.

TEMA: {topic}

CONTEXTO LEGAL (verificado en BOE):
{context_rag}

TAREA:
Genera 10 preguntas tipo test de nivel ALTO.

REQUISITOS CRÍTICOS:
1. USA SOLO información del contexto legal
2. VERIFICA cada artículo con la tool 'verificar_articulo_boe' ANTES de citarlo
3. Incluye URL BOE real de cada artículo

FORMATO JSON:
{{
  "bloque_preguntas": [
    {{
      "id": 1,
      "pregunta": "¿...?",
      "opciones": [
        {{"letra": "A", "texto": "..."}},
        {{"letra": "B", "texto": "..."}},
        {{"letra": "C", "texto": "..."}},
        {{"letra": "D", "texto": "..."}}
      ],
      "respuesta_correcta": "A",
      "explicacion_juridica": "Según Art. X de Ley Y (verificado en BD)...",
      "referencia_boe": "https://www.boe.es/...",
      "trampa": "Opción B confunde X con Y..."
    }}
  ]
}}
"""
```

### Prompt para Mistral Agent (Esquemas)

```python
PROMPT_MISTRAL_ESQUEMA = """
Eres un experto en Derecho Administrativo.

TEMA: {topic}

INSTRUCCIONES:
1. USA la herramienta 'buscar_rag' para obtener el contexto legal
2. Genera un ESQUEMA ESTRUCTURADO en Markdown
3. Cita artículos EXACTOS del contexto RAG

FORMATO JSON:
{{
  "concepto": "{topic}",
  "esquema_markdown": "# Título\\n- Nivel 1\\n  - Nivel 2 (Art. X)...",
  "puntos_clave": ["Clave 1", "Clave 2"],
  "articulos_citados": [
    {{"articulo": "Art. X", "ley": "Y", "fuente": "RAG"}}
  ]
}}
"""
```

---

## 🚀 SCRIPTS A CREAR (PRIORIDAD)

### 1. `generate_razonamiento_deepseek_v3.py` 🔴 ALTA

```python
# Usa DeepSeek V3.2 con:
# - Reasoning integrado (no 2-pass)
# - Tools: buscar_rag + verificar_articulo_boe
# - Output: 236 razonamientos verificados
```

### 2. `generate_simulacros_groq_batch.py` 🔴 ALTA

```python
# Usa Groq Batch API con:
# - MCP remoto para tools
# - 100 bloques en paralelo
# - Output: 1000 preguntas verificadas
```

### 3. `generate_estructurados_mistral_agent.py` 🟡 MEDIA

```python
# Usa Mistral Agents API con:
# - Agent ID pre-configurado
# - Pausas automáticas
# - Output: 120 esquemas/comparativas/plazos
```

---

## ✅ RECOMENDACIÓN FINAL

### **NO usar** `generate_qa_multi_model_v1.py` porque:
- ❌ Usa modelos antiguos (`deepseek-chat` sin V3.2)
- ❌ NO aprovecha Batch API de Groq
- ❌ NO usa Agents API de Mistral
- ❌ NO tiene verificación BOE integrada

### **SÍ usar** como base:
- ✅ `generate_cases_mistral.py` (Agents API funcional)
- ✅ Modificar para DeepSeek V3.2
- ✅ Crear nuevo para Groq Batch

---

¿Quieres que cree los 3 scripts optimizados ahora?
