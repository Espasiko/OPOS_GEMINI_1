# 🎯 PLAN CORRECTO: Agente Mistral con Herramientas

**Fecha**: 1 Diciembre 2025  
**Objetivo**: Agente Mistral que genera Q&A de máxima calidad usando herramientas reales

---

## ✅ CORRECCIONES FUNDAMENTALES

### **El Agente Mistral:**
- ✅ **SÍ genera Q&A** (es su función principal)
- ✅ **SÍ verifica** (función secundaria)
- ✅ **USA herramientas** para mejorar calidad:
  - Web search (buscar en BOE)
  - Code execution (validar cálculos)
  - Function calling (API BOE, scraping)

---

## 🔧 CÓMO DAR HERRAMIENTAS AL AGENTE

### **Opción 1: Web Search (YA DISPONIBLE)**

El agente Mistral **YA TIENE** web search activado:

```python
# Cuando usas el agente, automáticamente puede buscar en web
response = client.agents.complete(
    agent_id="ag_019ad601946d7323a81c544229de40a1",
    messages=[{
        "role": "user",
        "content": "Genera Q&A sobre artículo 205 LGSS"
    }]
)

# El agente automáticamente:
# 1. Busca "artículo 205 LGSS" en Google
# 2. Encuentra BOE
# 3. Lee el artículo
# 4. Genera Q&A basada en contenido real
```

**Ventaja**: ✅ Ya funciona, no requiere configuración  
**Desventaja**: ⚠️ Puede encontrar fuentes no oficiales

---

### **Opción 2: Function Calling (RECOMENDADO)**

Darle funciones específicas al agente:

```python
# dataset_generator/mistral_agent_with_tools.py

# 1. Definir herramientas
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
                        "description": "Nombre de la ley (ej: LGSS, Constitución)"
                    },
                    "articulo": {
                        "type": "string",
                        "description": "Número del artículo (ej: 205, 14)"
                    }
                },
                "required": ["ley", "articulo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scrape_url",
            "description": "Extrae contenido de una URL específica",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL a scrapear"
                    }
                },
                "required": ["url"]
            }
        }
    }
]

# 2. Llamar al agente con herramientas
response = client.agents.complete(
    agent_id=AGENT_ID,
    messages=[{
        "role": "user",
        "content": "Genera Q&A sobre artículo 205 LGSS"
    }],
    tools=tools  # ← Aquí le das las herramientas
)

# 3. Si el agente quiere usar una herramienta
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        if tool_call.function.name == "buscar_articulo_boe":
            # Ejecutar tu función
            args = json.loads(tool_call.function.arguments)
            result = buscar_articulo_boe(args["ley"], args["articulo"])
            
            # Devolver resultado al agente
            response = client.agents.complete(
                agent_id=AGENT_ID,
                messages=[
                    {"role": "user", "content": "Genera Q&A sobre artículo 205 LGSS"},
                    {"role": "assistant", "content": None, "tool_calls": [tool_call]},
                    {"role": "tool", "tool_call_id": tool_call.id, "content": result}
                ]
            )
```

---

## 🛠️ IMPLEMENTACIÓN DE HERRAMIENTAS

### **Herramienta 1: API BOE**

```python
# dataset_generator/tools/boe_api.py

import requests
from pathlib import Path

class BOEApi:
    """API para buscar artículos en BOE"""
    
    LEYES_INDEXADAS = {
        "LGSS": "BOE-A-2015-11724",
        "Constitución": "BOE-A-1978-31229",
        "Ley 39/2015": "BOE-A-2015-10565",
        "Ley 40/2015": "BOE-A-2015-10566",
        "EBEP": "BOE-A-2015-11719"
    }
    
    def buscar_articulo(self, ley: str, articulo: str) -> str:
        """
        Busca un artículo específico en el BOE
        
        Ejemplo:
        >>> api = BOEApi()
        >>> texto = api.buscar_articulo("LGSS", "205")
        >>> print(texto)
        "Artículo 205. Edad ordinaria de jubilación.
        1. La edad ordinaria de jubilación será..."
        """
        # 1. Obtener ID del BOE
        boe_id = self.LEYES_INDEXADAS.get(ley)
        if not boe_id:
            return f"Error: Ley '{ley}' no encontrada"
        
        # 2. Descargar PDF consolidado
        url = f"https://www.boe.es/buscar/pdf/consolidado/{boe_id}.pdf"
        pdf_path = self._download_pdf(url, boe_id)
        
        # 3. Extraer artículo específico
        texto = self._extract_article(pdf_path, articulo)
        
        return texto
    
    def _download_pdf(self, url: str, boe_id: str) -> Path:
        """Descarga PDF del BOE (con caché)"""
        cache_dir = Path("cache/boe")
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        pdf_path = cache_dir / f"{boe_id}.pdf"
        
        if not pdf_path.exists():
            response = requests.get(url)
            pdf_path.write_bytes(response.content)
        
        return pdf_path
    
    def _extract_article(self, pdf_path: Path, articulo: str) -> str:
        """Extrae artículo específico del PDF"""
        import PyPDF2
        
        with open(pdf_path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            
            # Buscar artículo en todas las páginas
            for page in pdf.pages:
                text = page.extract_text()
                
                # Buscar patrón "Artículo XXX"
                if f"Artículo {articulo}." in text or f"Art. {articulo}." in text:
                    # Extraer desde el artículo hasta el siguiente
                    start = text.find(f"Artículo {articulo}.")
                    if start == -1:
                        start = text.find(f"Art. {articulo}.")
                    
                    # Buscar siguiente artículo
                    next_art = text.find("Artículo", start + 10)
                    if next_art == -1:
                        next_art = len(text)
                    
                    return text[start:next_art].strip()
        
        return f"Artículo {articulo} no encontrado"
```

### **Herramienta 2: Web Scraper**

```python
# dataset_generator/tools/web_scraper.py

import requests
from bs4 import BeautifulSoup

class WebScraper:
    """Scraper para extraer contenido de URLs"""
    
    def scrape(self, url: str, selector: str = None) -> str:
        """
        Extrae contenido de una URL
        
        Ejemplo:
        >>> scraper = WebScraper()
        >>> content = scraper.scrape(
        ...     "https://www.seg-social.es/wps/portal/wss/internet/...",
        ...     selector=".content-main"
        ... )
        """
        try:
            # 1. Fetch URL
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # 2. Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 3. Extraer contenido
            if selector:
                element = soup.select_one(selector)
                if element:
                    return element.get_text(strip=True)
            
            # Si no hay selector, extraer todo el texto
            return soup.get_text(strip=True)
            
        except Exception as e:
            return f"Error scraping {url}: {e}"
```

### **Herramienta 3: Integración con MCP**

```python
# dataset_generator/tools/mcp_client.py

import subprocess
import json

class MCPClient:
    """Cliente para llamar al MCP server"""
    
    def __init__(self, mcp_path: str = "../mcp-server"):
        self.mcp_path = mcp_path
    
    def call_tool(self, tool_name: str, params: dict) -> str:
        """
        Llama a una herramienta del MCP
        
        Ejemplo:
        >>> mcp = MCPClient()
        >>> result = mcp.call_tool("scrape_url", {
        ...     "url": "https://www.seg-social.es/..."
        ... })
        """
        # Llamar al MCP via subprocess
        cmd = [
            "node",
            f"{self.mcp_path}/dist/index.js",
            "call-tool",
            tool_name,
            json.dumps(params)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
```

---

## 🎯 INTEGRACIÓN COMPLETA

### **Script Principal:**

```python
# dataset_generator/generate_with_agent_tools.py

from mistralai.client import MistralClient
from tools.boe_api import BOEApi
from tools.web_scraper import WebScraper
import json

class MistralAgentWithTools:
    def __init__(self):
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
        self.agent_id = "ag_019ad601946d7323a81c544229de40a1"
        
        # Herramientas
        self.boe_api = BOEApi()
        self.scraper = WebScraper()
        
        # Definir herramientas para el agente
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "buscar_articulo_boe",
                    "description": "Busca un artículo específico en el BOE oficial",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ley": {"type": "string"},
                            "articulo": {"type": "string"}
                        },
                        "required": ["ley", "articulo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "scrape_url",
                    "description": "Extrae contenido de una URL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"}
                        },
                        "required": ["url"]
                    }
                }
            }
        ]
    
    def generate_qa(self, topic: str) -> dict:
        """Genera Q&A usando el agente con herramientas"""
        
        messages = [{
            "role": "user",
            "content": f"Genera una pregunta tipo test sobre: {topic}"
        }]
        
        # Primera llamada al agente
        response = self.client.agents.complete(
            agent_id=self.agent_id,
            messages=messages,
            tools=self.tools
        )
        
        # Si el agente quiere usar herramientas
        while response.choices[0].message.tool_calls:
            # Ejecutar herramientas
            for tool_call in response.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                # Ejecutar la función correspondiente
                if function_name == "buscar_articulo_boe":
                    result = self.boe_api.buscar_articulo(
                        arguments["ley"],
                        arguments["articulo"]
                    )
                elif function_name == "scrape_url":
                    result = self.scraper.scrape(arguments["url"])
                
                # Añadir resultado a los mensajes
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call]
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Llamar al agente de nuevo con los resultados
            response = self.client.agents.complete(
                agent_id=self.agent_id,
                messages=messages,
                tools=self.tools
            )
        
        # Extraer Q&A final
        qa_text = response.choices[0].message.content
        return self._parse_qa(qa_text)
```

---

## 📚 ORDEN DE LEYES PARA OPOSICIONES

### **PRIORIDAD 1: Seguridad Social (CORE)**

```python
LEYES_PRIORIDAD_1 = [
    {
        "nombre": "LGSS",
        "boe_id": "BOE-A-2015-11724",
        "descripcion": "Ley General de la Seguridad Social",
        "articulos_clave": [
            "7-10",    # Ámbito aplicación
            "136-141", # Acción protectora
            "161-171", # Incapacidad temporal
            "172-198", # Incapacidad permanente
            "205-245", # Jubilación
            "246-252", # Muerte y supervivencia
            "253-261"  # Desempleo
        ],
        "qa_objetivo": 2000  # 20% del total
    },
    {
        "nombre": "RD_Afiliacion",
        "boe_id": "BOE-A-1996-4447",
        "descripcion": "Reglamento de Afiliación, Altas y Bajas",
        "qa_objetivo": 500
    },
    {
        "nombre": "RD_Recaudacion",
        "boe_id": "BOE-A-2004-11836",
        "descripcion": "Reglamento General de Recaudación SS",
        "qa_objetivo": 500
    },
    {
        "nombre": "Ley_IMV",
        "boe_id": "BOE-A-2021-21007",
        "descripcion": "Ley del Ingreso Mínimo Vital",
        "qa_objetivo": 300
    }
]
# TOTAL PRIORIDAD 1: 3,300 Q&A
```

### **PRIORIDAD 2: Administración General del Estado**

```python
LEYES_PRIORIDAD_2 = [
    {
        "nombre": "Constitucion",
        "boe_id": "BOE-A-1978-31229",
        "descripcion": "Constitución Española",
        "articulos_clave": [
            "1-9",     # Título Preliminar
            "10-55",   # Derechos fundamentales
            "97-107",  # Gobierno y Administración
            "117-127"  # Poder Judicial
        ],
        "qa_objetivo": 1000
    },
    {
        "nombre": "Ley_39_2015",
        "boe_id": "BOE-A-2015-10565",
        "descripcion": "Procedimiento Administrativo Común",
        "qa_objetivo": 800
    },
    {
        "nombre": "Ley_40_2015",
        "boe_id": "BOE-A-2015-10566",
        "descripcion": "Régimen Jurídico del Sector Público",
        "qa_objetivo": 800
    },
    {
        "nombre": "EBEP",
        "boe_id": "BOE-A-2015-11719",
        "descripcion": "Estatuto Básico del Empleado Público",
        "qa_objetivo": 700
    }
]
# TOTAL PRIORIDAD 2: 3,300 Q&A
```

### **PRIORIDAD 3: Complementarias**

```python
LEYES_PRIORIDAD_3 = [
    {
        "nombre": "LOPDGDD",
        "boe_id": "BOE-A-2018-16673",
        "descripcion": "Ley Orgánica de Protección de Datos",
        "qa_objetivo": 500
    },
    {
        "nombre": "Ley_Contratos",
        "boe_id": "BOE-A-2017-12902",
        "descripcion": "Ley de Contratos del Sector Público",
        "qa_objetivo": 400
    },
    # Reglamentos específicos
    # Jurisprudencia relevante
    # Casos prácticos
]
# TOTAL PRIORIDAD 3: 3,400 Q&A
```

---

## 🚀 PLAN DE EJECUCIÓN

### **FASE 1: Setup Herramientas (HOY - 3h)**

```bash
# 1. Implementar API BOE
python -c "from tools.boe_api import BOEApi; api = BOEApi(); print(api.buscar_articulo('LGSS', '205'))"

# 2. Implementar Web Scraper
python -c "from tools.web_scraper import WebScraper; s = WebScraper(); print(s.scrape('https://www.boe.es'))"

# 3. Integrar con Agente Mistral
python generate_with_agent_tools.py --test
```

### **FASE 2: Generación Prioridad 1 (2 DÍAS)**

```bash
# Generar 3,300 Q&A de Seguridad Social
python generate_with_agent_tools.py \
  --leyes LGSS,RD_Afiliacion,RD_Recaudacion,Ley_IMV \
  --objetivo 3300 \
  --output output/prioridad1.jsonl
```

### **FASE 3: Generación Prioridad 2 (2 DÍAS)**

```bash
# Generar 3,300 Q&A de Administración
python generate_with_agent_tools.py \
  --leyes Constitucion,Ley_39_2015,Ley_40_2015,EBEP \
  --objetivo 3300 \
  --output output/prioridad2.jsonl
```

### **FASE 4: Generación Prioridad 3 (1 DÍA)**

```bash
# Generar 3,400 Q&A complementarias
python generate_with_agent_tools.py \
  --leyes LOPDGDD,Ley_Contratos \
  --objetivo 3400 \
  --output output/prioridad3.jsonl
```

---

## ✅ RESUMEN

**El Agente Mistral:**
- ✅ **Genera Q&A** (función principal)
- ✅ **Usa herramientas** (BOE API, scraping)
- ✅ **Verifica automáticamente** (web search, code)
- ✅ **Prioriza leyes de oposiciones**

**Herramientas:**
- ✅ API BOE (buscar artículos específicos)
- ✅ Web Scraper (extraer contenido URLs)
- ✅ MCP (opcional, para scraping avanzado)

**Orden de generación:**
1. Seguridad Social (3,300 Q&A)
2. Administración General (3,300 Q&A)
3. Complementarias (3,400 Q&A)

**¿Empezamos implementando las herramientas?** 🛠️
