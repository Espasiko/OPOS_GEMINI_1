# 🔧 SOLUCIÓN: Error httpx y Configuración Agente Mistral

**Fecha**: 4 Diciembre 2025  
**Problema**: `ModuleNotFoundError: No module named 'httpx'`  
**Causa**: Venv creado en WSL, ejecutando desde Windows PowerShell

---

## 🎯 PROBLEMA IDENTIFICADO

### Error Original:
```
Traceback (most recent call last):
  File "e:\1\OPOS_GEMINI_1\backend\agents\test_agent_completo.py", line 25, in <module>
    from agents.mistral_tools import get_mistral_tools
  File "e:\1\OPOS_GEMINI_1\backend\agents\__init__.py", line 5, in <module>
    from .rag_agent import RAGAgent, get_rag_agent
  File "e:\1\OPOS_GEMINI_1\backend\agents\rag_agent.py", line 10, in <module>
    import httpx
ModuleNotFoundError: No module named 'httpx'
```

### Causa Raíz:
El venv de `backend/` fue creado en **WSL** (tiene estructura `bin/` en lugar de `Scripts/`), pero estás intentando ejecutar el script desde **Windows PowerShell**.

---

## ✅ SOLUCIONES

### Opción 1: Ejecutar desde WSL (RECOMENDADO)

```bash
# 1. Abrir WSL
wsl

# 2. Navegar al proyecto
cd /home/espasiko/OPOS_GEMINI_1

# 3. Activar venv del backend
source backend/venv/bin/activate

# 4. Verificar que httpx está instalado
python3 -c "import httpx; print('httpx OK')"

# 5. Ejecutar el test
python3 backend/agents/test_agent_completo.py
```

### Opción 2: Recrear venv en Windows

```powershell
# 1. Eliminar venv actual (creado en WSL)
Remove-Item -Recurse -Force backend\venv

# 2. Crear nuevo venv en Windows
cd backend
python -m venv venv

# 3. Activar venv
.\venv\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar test
python agents\test_agent_completo.py
```

### Opción 3: Instalar httpx en el venv existente desde WSL

```bash
# En WSL
cd /home/espasiko/OPOS_GEMINI_1
source backend/venv/bin/activate
pip install httpx==0.27.0
```

---

## 🤖 AGENTE MISTRAL - CONFIGURACIÓN CORRECTA

### Según Documentación Oficial (docs.mistral.ai/capabilities/agents/)

El Agente Mistral Studio tiene capacidades integradas:
- ✅ **Web Search**: Búsqueda en internet (incluyendo BOE)
- ✅ **Code Interpreter**: Ejecución de código Python
- ✅ **Image Generation**: Generación de imágenes
- ✅ **Document Library (Beta)**: RAG integrado
- ✅ **Function Calling**: Herramientas personalizadas
- ✅ **MCP Servers**: Integración con servidores MCP

### Cómo Usar el Agente:

**❌ INCORRECTO** (da error 400 "Invalid model"):
```python
from mistralai import Mistral

client = Mistral(api_key="FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF")

# ❌ NO FUNCIONA - Da error 400
response = client.chat.complete(
    model="ag_019ad601946d7323a81c544229de40a1",  # ❌ Error
    messages=[
        {"role": "user", "content": "¿Cuál es la edad de jubilación en España?"}
    ]
)
```

**✅ CORRECTO** (API de Agentes):
```python
from mistralai import Mistral

client = Mistral(api_key="FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF")

# ✅ USAR ESTO - API de Agentes
response = client.agents.complete(
    agent_id="ag_019ad601946d7323a81c544229de40a1",
    messages=[
        {"role": "user", "content": "¿Cuál es la edad de jubilación en España?"}
    ]
)

# Extraer respuesta (puede incluir "thinking")
if response.choices:
    content = response.choices[0].message.content
    print(content)
```

### Configurar Instrucciones del Agente:

**Opción A: En Mistral Studio (Web) - RECOMENDADO**
1. Ir a https://console.mistral.ai/
2. Agents → Seleccionar tu agente
3. Sección "Instructions" o "System Prompt"
4. Pegar las instrucciones (ver INSTRUCCIONES_AGENTE_MISTRAL.md)
5. Guardar

**Ventajas**:
- ✅ Instrucciones persistentes
- ✅ No cuentan como tokens de input
- ✅ Más económico

**Opción B: Desde Código**
```python
response = client.chat.complete(
    model="ag_019ad601946d7323a81c544229de40a1",
    messages=[
        {
            "role": "system",
            "content": "Eres un experto en Seguridad Social española..."
        },
        {
            "role": "user",
            "content": "Tu pregunta"
        }
    ]
)
```

**Desventajas**:
- ⚠️ Cuentan como tokens de input
- ⚠️ Más caro

---

## 🛠️ HERRAMIENTAS DEL AGENTE

### Herramientas Built-in (Ya disponibles):
1. **Web Search**: El agente puede buscar en internet automáticamente
2. **Code Interpreter**: Puede ejecutar código Python para cálculos
3. **Image Generation**: Puede generar imágenes
4. **Document Library**: RAG integrado (si subes documentos)

### Herramientas Personalizadas (Function Calling):

Para dar herramientas personalizadas al agente:

```python
# Definir herramientas
tools = [
    {
        "type": "function",
        "function": {
            "name": "buscar_articulo_boe",
            "description": "Busca un artículo específico en el BOE oficial",
            "parameters": {
                "type": "object",
                "properties": {
                    "ley": {
                        "type": "string",
                        "description": "Nombre de la ley (ej: LGSS)"
                    },
                    "articulo": {
                        "type": "string",
                        "description": "Número del artículo (ej: 205)"
                    }
                },
                "required": ["ley", "articulo"]
            }
        }
    }
]

# Llamar al agente con herramientas
response = client.chat.complete(
    model="ag_019ad601946d7323a81c544229de40a1",
    messages=[{"role": "user", "content": "Busca artículo 205 LGSS"}],
    tools=tools,
    tool_choice="auto"
)

# Si el agente quiere usar la herramienta
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        # Ejecutar tu función
        result = buscar_articulo_boe(...)
        
        # Devolver resultado al agente
        response = client.chat.complete(
            model="ag_019ad601946d7323a81c544229de40a1",
            messages=[
                {"role": "user", "content": "Busca artículo 205 LGSS"},
                {"role": "assistant", "tool_calls": [tool_call]},
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            ]
        )
```

---

## 🎯 ESTRATEGIA ÓPTIMA PARA TU CASO

### Para Generación de Q&A:

**Opción 1: Agente Studio con Web Search (SIMPLE)**
```python
# El agente automáticamente:
# 1. Busca "artículo 205 LGSS" en Google
# 2. Encuentra BOE
# 3. Lee el artículo
# 4. Genera Q&A basada en contenido real

response = client.chat.complete(
    model="ag_019ad601946d7323a81c544229de40a1",
    messages=[{
        "role": "user",
        "content": "Genera una pregunta tipo test sobre el artículo 205 LGSS"
    }]
)
```

**Ventajas**:
- ✅ Muy simple, sin código extra
- ✅ Web search automático
- ✅ Verifica fuentes oficiales

**Desventajas**:
- ⚠️ Puede encontrar fuentes no oficiales
- ⚠️ Más caro ($0.03 por búsqueda web)

**Opción 2: Herramientas Personalizadas + RAG Local (ÓPTIMO)**
```python
# Combinar:
# 1. RAG local (Qdrant) - Gratis, rápido
# 2. Herramienta BOE - Solo cuando necesite verificar
# 3. Code Interpreter - Para cálculos

tools = [
    buscar_rag_qdrant,      # Tu Qdrant local
    buscar_boe_oficial,     # API BOE
    calcular_prestacion_ss  # Calculadora SS
]

response = client.chat.complete(
    model="ag_019ad601946d7323a81c544229de40a1",
    messages=[{
        "role": "user",
        "content": "Genera Q&A sobre jubilación"
    }],
    tools=tools,
    tool_choice="auto"
)
```

**Ventajas**:
- ✅ Más económico (usa RAG local primero)
- ✅ Más rápido
- ✅ Más control sobre fuentes
- ✅ Verificación automática con BOE

---

## 📊 COSTES ESTIMADOS

### Con Web Search (Opción 1):
```
Por Q&A:
- LLM: ~1000 tokens × $2/1M = $0.002
- Web Search: 1-2 búsquedas × $0.03 = $0.03-0.06
TOTAL: $0.032-0.062 por Q&A

10,000 Q&A: $320-620
```

### Con Herramientas Locales (Opción 2):
```
Por Q&A:
- LLM: ~1000 tokens × $2/1M = $0.002
- RAG local: GRATIS
- BOE API: GRATIS
- Code Interpreter: $0.03 (solo si necesita)
TOTAL: $0.002-0.032 por Q&A

10,000 Q&A: $20-320
```

**AHORRO: 84-94% usando herramientas locales**

---

## 🚀 PLAN DE ACCIÓN

### Paso 1: Solucionar httpx (5 min)
```bash
# En WSL
wsl
cd /home/espasiko/OPOS_GEMINI_1
source backend/venv/bin/activate
pip install httpx==0.27.0
```

### Paso 2: Probar Agente Simple (5 min)
```bash
# Crear test simple
cat > test_agente_simple.py << 'EOF'
from mistralai import Mistral

client = Mistral(api_key="FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF")

response = client.chat.complete(
    model="ag_019ad601946d7323a81c544229de40a1",
    messages=[{
        "role": "user",
        "content": "¿Cuál es la edad de jubilación ordinaria en España en 2024?"
    }]
)

print(response.choices[0].message.content)
EOF

# Ejecutar
python3 test_agente_simple.py
```

### Paso 3: Configurar Instrucciones en Web (10 min)
1. Ir a https://console.mistral.ai/
2. Agents → Tu agente
3. Copiar instrucciones de INSTRUCCIONES_AGENTE_MISTRAL.md
4. Pegar y guardar

### Paso 4: Probar con Herramientas (15 min)
```bash
# Ejecutar test completo
python3 backend/agents/test_agent_completo.py
```

---

## ✅ RESUMEN

### Problema:
- ❌ Venv de WSL, ejecutando desde Windows
- ❌ httpx no encontrado

### Solución:
- ✅ Ejecutar desde WSL
- ✅ O recrear venv en Windows

### Agente Mistral:
- ✅ Usar agent_id como modelo
- ✅ Web search automático disponible
- ✅ Configurar instrucciones en web
- ✅ Añadir herramientas personalizadas para ahorrar

### Próximos Pasos:
1. Solucionar httpx
2. Probar agente simple
3. Configurar instrucciones
4. Integrar herramientas locales
5. Generar Q&A de prueba

---

**Creado**: 4 Diciembre 2025  
**Estado**: ✅ Documentado - Listo para implementar
