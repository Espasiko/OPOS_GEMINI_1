# 📋 Instrucciones Actualizadas para Agente Mistral - Con Herramientas Reales

**Fecha**: 4 Diciembre 2025  
**Agent ID**: ag_019ad601946d7323a81c544229de40a1  
**Actualización**: Integración con herramientas reales de OpositAIA

---

## 🎯 CAMBIOS PRINCIPALES

1. ✅ Usa `buscar_rag_qdrant` de tu backend
2. ✅ Usa API BOE en formato **JSON** (más fácil de parsear)
3. ✅ Integración con tu FastAPI backend
4. ✅ Integración con tu MCP server

---

## 📝 INSTRUCCIONES PARA MISTRAL STUDIO

### **Copia y pega esto en https://console.mistral.ai/ → Agents → Instructions:**

```markdown
# AGENTE VERIFICADOR Y GENERADOR DE Q&A LEGAL - SEGURIDAD SOCIAL ESPAÑOLA

## IDENTIDAD Y MISIÓN
Eres un experto en legislación española de Seguridad Social con 20 años de experiencia.
Tu misión es generar y verificar preguntas y respuestas de máxima calidad para opositores.

**REGLA DE ORO**: NUNCA JAMÁS TE INVENTAS DATOS O URLs. NUNCA JAMÁS PRESUPONGAS NADA.
COMPRUEBAS MINUCIOSAMENTE TODOS LOS DATOS REALES Y ACTUALES PARA DICIEMBRE DE 2025.

## HERRAMIENTAS DISPONIBLES

Tienes acceso a herramientas especializadas para:
1. **Buscar en base de conocimiento** (Qdrant RAG)
2. **Consultar BOE oficial** (API JSON)
3. **Verificar URLs del BOE**
4. **Calcular prestaciones** (jubilación, IMV, etc.)
5. **Clasificar Q&A** por tema y dificultad

## PROCESO DE TRABAJO

### MODO 1: GENERACIÓN DE Q&A

Cuando te pidan generar Q&A:

1. **Busca contexto legal**
   - USA la herramienta de búsqueda RAG
   - Busca artículos relevantes en la base de conocimiento
   - Identifica conceptos clave

2. **Consulta BOE si es necesario**
   - Si necesitas verificar un artículo específico
   - USA la API del BOE para obtener texto oficial
   - Cita siempre la fuente exacta

3. **Genera pregunta tipo test**
   - Formato: 1 pregunta + 4 opciones (a, b, c, d)
   - Una sola respuesta correcta
   - Distractores plausibles pero incorrectos
   - Nivel oposición: medio-alto

4. **Crea respuesta explicada**
   - Justifica por qué es correcta
   - Explica por qué las otras son incorrectas
   - Cita artículos específicos (ej: "art. 205.1.a LGSS")
   - Añade contexto legal relevante

5. **Verifica automáticamente**
   - Si mencionas artículos → busca en BOE
   - Si hay cálculos → valida con herramienta de cálculo
   - Comprueba que la info está actualizada

### MODO 2: VERIFICACIÓN DE Q&A

Cuando te den una Q&A para verificar:

1. **Análisis inicial**
   - Lee pregunta y respuesta
   - Identifica tema legal
   - Detecta referencias a artículos

2. **Verificación automática**
   
   **A) Referencias legales:**
   - Si menciona artículos → USA herramienta BOE
   - Verifica que existe y dice lo correcto
   - Comprueba vigencia actual
   
   **B) Cálculos numéricos:**
   - Si hay números → USA herramienta de cálculo
   - Valida fórmulas de prestaciones
   - Comprueba porcentajes y bases
   
   **C) Contexto legal:**
   - USA herramienta RAG para buscar contexto
   - Verifica coherencia con legislación

3. **Asignación de confianza**
   
   **Score 0.9-1.0 (ALTA CONFIANZA):**
   - Verificado en BOE oficial
   - Cálculos correctos
   - Referencias precisas
   - Sin ambigüedades
   
   **Score 0.7-0.9 (MEDIA-ALTA):**
   - Info correcta pero sin fuente directa BOE
   - Cálculos correctos
   - Pequeñas imprecisiones de formato
   
   **Score 0.5-0.7 (MEDIA):**
   - Info probablemente correcta
   - No se pudo verificar completamente
   - Necesita revisión humana
   
   **Score 0.0-0.5 (BAJA):**
   - Errores detectados
   - Info desactualizada
   - Cálculos incorrectos
   - RECHAZAR o CORREGIR

4. **Formato de respuesta**
   
   SIEMPRE devuelve JSON estructurado:
   ```json
   {
     "verified": true/false,
     "confidence": 0.95,
     "issues": [
       "Artículo 205.1.a) verificado en BOE",
       "Cálculo validado: (2000*24)/24 = 2000"
     ],
     "corrections": "Si hay errores, indica cómo corregir",
     "sources": [
       "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
     ],
     "recommendation": "APROBAR/CORREGIR/RECHAZAR",
     "reasoning": "Explicación detallada de tu decisión"
   }
   ```

## REGLAS ESTRICTAS

### BÚSQUEDA DE INFORMACIÓN:
1. SIEMPRE usa las herramientas disponibles
2. NUNCA inventes información
3. Si no puedes verificar → confidence = 0.5
4. Cita siempre la fuente exacta

### FUENTES OFICIALES:
1. BOE (www.boe.es) - PRIORITARIO
2. Base de conocimiento (Qdrant RAG)
3. INSS (www.seg-social.es)
4. NUNCA uses fuentes no oficiales (blogs, foros)

### CÁLCULOS:
1. USA la herramienta de cálculo para validar
2. Muestra la fórmula usada
3. Explica cada paso
4. Redondea según normativa (2 decimales para euros)

### CALIDAD:
1. Sé preciso con artículos (ej: "205.1.a" no solo "205")
2. Usa terminología legal correcta
3. Formato profesional de oposición
4. Si tienes duda → marca para revisión humana

## FORMATO DE SALIDA

### Para generación de Q&A:
```json
{
  "question": "¿Cuál es la edad ordinaria de jubilación en 2024?",
  "options": {
    "a": "65 años",
    "b": "66 años",
    "c": "66 años y 6 meses",
    "d": "67 años"
  },
  "correct_answer": "c",
  "explanation": "Según el art. 205.1.a) LGSS, en 2024 la edad ordinaria es 66 años y 6 meses.",
  "legal_references": ["art. 205.1.a LGSS (RDLeg 8/2015)"],
  "difficulty": "medio",
  "topic": "jubilación",
  "verified": true,
  "confidence": 0.95,
  "sources": ["https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"]
}
```

### Para verificación:
```json
{
  "verified": true/false,
  "confidence": 0.0-1.0,
  "issues": ["lista de verificaciones realizadas"],
  "corrections": "correcciones si hay errores",
  "sources": ["URLs consultadas"],
  "recommendation": "APROBAR/CORREGIR/RECHAZAR",
  "reasoning": "explicación detallada"
}
```

## PRIORIDADES

1. **VERACIDAD** - La información DEBE ser correcta
2. **ACTUALIZACIÓN** - Verificar que está vigente
3. **PRECISIÓN** - Referencias legales exactas
4. **CLARIDAD** - Explicaciones comprensibles
5. **FORMATO** - Profesional y consistente

## TU OBJETIVO FINAL

Generar y verificar Q&A de tal calidad que:
- ✅ Un opositor pueda confiar 100% en la información
- ✅ Pase cualquier revisión de expertos
- ✅ Esté actualizada según BOE vigente
- ✅ Tenga referencias legales precisas
- ✅ Los cálculos sean matemáticamente correctos

**RECUERDA: La calidad es más importante que la cantidad. Mejor 1 Q&A perfecta que 10 mediocres.**
```

---

## 🔧 HERRAMIENTAS PARA EL AGENTE

### **Opción 1: Llamar a tu FastAPI Backend**

El agente Mistral puede llamar a tu FastAPI si:
1. Tu backend está expuesto públicamente (o via ngrok/cloudflare tunnel)
2. Defines las herramientas como funciones que hacen HTTP requests

**Ejemplo de herramienta que llama a tu FastAPI:**

```json
{
  "type": "function",
  "function": {
    "name": "buscar_rag_qdrant",
    "description": "Busca contexto legal relevante en la base de conocimiento Qdrant de OpositAIA",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "Consulta en lenguaje natural sobre legislación de Seguridad Social"
        },
        "top_k": {
          "type": "integer",
          "description": "Número de resultados a devolver (1-10)",
          "default": 5
        },
        "filter_ley": {
          "type": "string",
          "description": "Filtrar por ley específica (LGSS, RD_IMV, etc.)",
          "enum": ["LGSS", "RD_IMV", "Constitución", "Ley 39/2015", "EBEP"]
        }
      },
      "required": ["query"]
    }
  }
}
```

**Implementación en tu código:**

```python
# backend/agents/mistral_agent_with_fastapi.py

import requests
from mistralai import Mistral

class MistralAgentWithFastAPI:
    def __init__(self):
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.agent_id = "ag_019ad601946d7323a81c544229de40a1"
        self.backend_url = "http://localhost:8000"  # o tu URL pública
        
        # Definir herramientas que llaman a tu FastAPI
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "buscar_rag_qdrant",
                    "description": "Busca en Qdrant",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "top_k": {"type": "integer", "default": 5}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "buscar_boe_json",
                    "description": "Busca en BOE usando JSON",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "boe_id": {"type": "string"},
                            "articulo": {"type": "string"}
                        },
                        "required": ["boe_id"]
                    }
                }
            }
        ]
    
    def execute_tool(self, tool_call):
        """Ejecuta herramienta llamando a tu FastAPI"""
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        
        if name == "buscar_rag_qdrant":
            # Llamar a tu endpoint FastAPI
            response = requests.post(
                f"{self.backend_url}/api/rag/search",
                json={
                    "query": args["query"],
                    "top_k": args.get("top_k", 5)
                }
            )
            return response.json()
        
        elif name == "buscar_boe_json":
            # Llamar a tu endpoint BOE
            response = requests.get(
                f"{self.backend_url}/api/boe/documento/{args['boe_id']}",
                params={"articulo": args.get("articulo")}
            )
            return response.json()
    
    def chat(self, message: str):
        """Chat con herramientas de FastAPI"""
        messages = [{"role": "user", "content": message}]
        
        response = self.client.chat.complete(
            model=self.agent_id,
            messages=messages,
            tools=self.tools
        )
        
        # Procesar tool calls
        while response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                # Ejecutar herramienta (llama a tu FastAPI)
                result = self.execute_tool(tool_call)
                
                # Añadir resultado
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call]
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            
            # Nueva llamada con resultados
            response = self.client.chat.complete(
                model=self.agent_id,
                messages=messages,
                tools=self.tools
            )
        
        return response.choices[0].message.content
```

### **Opción 2: Usar tu MCP Server**

Tu MCP server puede ser llamado por el agente si:
1. Expones el MCP como HTTP API
2. O usas el agente desde un cliente que tiene acceso al MCP

**Modificar tu MCP para que sea accesible:**

```typescript
// mcp-server/src/http-wrapper.ts

import express from 'express';
import { scrapeUrl } from './index';

const app = express();
app.use(express.json());

// Endpoint para scraping
app.post('/api/scrape', async (req, res) => {
  try {
    const { url, selector } = req.body;
    const result = await scrapeUrl(url, selector);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Endpoint para BOE
app.get('/api/boe/:boeId', async (req, res) => {
  try {
    const { boeId } = req.params;
    const { articulo } = req.query;
    
    // Llamar a API BOE en JSON
    const boeUrl = `https://www.boe.es/datosabiertos/api/boe/documento/${boeId}`;
    const response = await fetch(boeUrl, {
      headers: { 'Accept': 'application/json' }
    });
    
    const data = await response.json();
    
    // Si se especifica artículo, filtrar
    if (articulo) {
      const articuloData = data.articulos?.find(a => a.numero === articulo);
      res.json(articuloData || { error: 'Artículo no encontrado' });
    } else {
      res.json(data);
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => {
  console.log('MCP HTTP wrapper running on port 3000');
});
```

---

## 🌐 API BOE - FORMATOS DISPONIBLES

Según la documentación oficial del BOE, la API soporta:

### **Formatos Disponibles:**

1. ✅ **XML** (por defecto)
2. ✅ **JSON** (recomendado para el agente)
3. ✅ **PDF**
4. ✅ **HTML**

### **Cómo Solicitar JSON:**

```bash
# Opción 1: Header Accept
curl -H "Accept: application/json" \
  "https://www.boe.es/datosabiertos/api/boe/documento/BOE-A-2015-11724"

# Opción 2: Parámetro en URL (si está disponible)
curl "https://www.boe.es/datosabiertos/api/boe/documento/BOE-A-2015-11724?formato=json"

# Opción 3: Extensión en URL
curl "https://www.boe.es/datosabiertos/api/boe/documento/BOE-A-2015-11724.json"
```

### **Ejemplo de Respuesta JSON:**

```json
{
  "metadatos": {
    "identificador": "BOE-A-2015-11724",
    "titulo": "Real Decreto Legislativo 8/2015, de 30 de octubre...",
    "fecha_publicacion": "2015-10-31",
    "fecha_vigencia": "2016-01-01",
    "rango": "Real Decreto Legislativo"
  },
  "texto": {
    "articulos": [
      {
        "numero": "205",
        "titulo": "Edad ordinaria de jubilación",
        "apartados": [
          {
            "numero": "1",
            "contenido": "La edad ordinaria de jubilación será..."
          }
        ]
      }
    ]
  }
}
```

---

## 📋 ENDPOINTS DE TU FASTAPI PARA EL AGENTE

### **Crear estos endpoints en tu backend:**

```python
# backend/routers/agent_tools.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.mistral_tools import get_mistral_tools

router = APIRouter(prefix="/api/agent", tags=["agent"])
tools = get_mistral_tools()

class RAGSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    filter_ley: str = None

class BOESearchRequest(BaseModel):
    boe_id: str
    articulo: str = None

@router.post("/rag/search")
async def rag_search(request: RAGSearchRequest):
    """Endpoint para búsqueda RAG en Qdrant"""
    result = tools.buscar_rag_qdrant(
        query=request.query,
        top_k=request.top_k,
        filter_ley=request.filter_ley
    )
    return result

@router.get("/boe/{boe_id}")
async def boe_search(boe_id: str, articulo: str = None):
    """Endpoint para búsqueda en BOE (JSON)"""
    import requests
    
    # Llamar a API BOE solicitando JSON
    url = f"https://www.boe.es/datosabiertos/api/boe/documento/{boe_id}"
    response = requests.get(url, headers={"Accept": "application/json"})
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Documento BOE no encontrado")
    
    data = response.json()
    
    # Si se especifica artículo, filtrar
    if articulo:
        articulos = data.get("texto", {}).get("articulos", [])
        art_data = next((a for a in articulos if a["numero"] == articulo), None)
        if not art_data:
            raise HTTPException(status_code=404, detail=f"Artículo {articulo} no encontrado")
        return art_data
    
    return data

@router.post("/calculate")
async def calculate_prestacion(
    tipo: str,
    bases: list[float] = None,
    años: float = None
):
    """Endpoint para cálculos de prestaciones"""
    result = tools.calcular_prestacion_ss(
        tipo_prestacion=tipo,
        bases_cotizacion=bases,
        años_cotizados=años
    )
    return result
```

### **Registrar en main.py:**

```python
# backend/main.py

from routers import agent_tools

app.include_router(agent_tools.router)
```

---

## 🚀 PLAN DE IMPLEMENTACIÓN

### **Fase 1: Exponer tu Backend (1 hora)**

```bash
# Opción 1: Ngrok (desarrollo)
ngrok http 8000

# Opción 2: Cloudflare Tunnel (producción)
cloudflared tunnel --url http://localhost:8000

# Opción 3: Usar tu VPS
# Ya tienes 147.93.95.67, configurar nginx reverse proxy
```

### **Fase 2: Actualizar Instrucciones del Agente (30 min)**

1. Ve a https://console.mistral.ai/
2. Agents → ag_019ad601946d7323a81c544229de40a1
3. Instructions → Pega las instrucciones de arriba
4. Guarda

### **Fase 3: Configurar Herramientas (1 hora)**

```python
# Crear backend/agents/mistral_agent_with_fastapi.py
# (código de arriba)

# Test
python backend/agents/test_agent_with_fastapi.py
```

### **Fase 4: Test E2E (30 min)**

```python
# Test completo
agent = MistralAgentWithFastAPI()

# Test 1: Búsqueda RAG
response = agent.chat("¿Cuál es la edad de jubilación ordinaria?")
print(response)

# Test 2: Verificación
qa = {
    "pregunta": "¿Edad de jubilación en 2024?",
    "respuesta": "66 años y 6 meses"
}
verification = agent.chat(f"Verifica esta Q&A: {json.dumps(qa)}")
print(verification)
```

---

## ✅ RESUMEN

### **Cambios Realizados:**

1. ✅ Instrucciones actualizadas para usar tus herramientas
2. ✅ API BOE configurada para usar **JSON** (más fácil)
3. ✅ Integración con tu **FastAPI backend**
4. ✅ Integración con tu **MCP server** (opcional)
5. ✅ Endpoints creados para el agente

### **Ventajas:**

- ✅ El agente usa TU base de conocimiento (Qdrant)
- ✅ El agente usa TU lógica de negocio (FastAPI)
- ✅ JSON es más fácil de parsear que XML
- ✅ Todo centralizado en tu backend
- ✅ Control total sobre las herramientas

### **Próximos Pasos:**

1. Exponer tu backend (ngrok o VPS)
2. Actualizar instrucciones en Mistral Studio
3. Crear endpoints en FastAPI
4. Test E2E

---

**Fecha**: 4 Diciembre 2025  
**Estado**: ✅ Listo para implementar  
**Tiempo estimado**: 3-4 horas
