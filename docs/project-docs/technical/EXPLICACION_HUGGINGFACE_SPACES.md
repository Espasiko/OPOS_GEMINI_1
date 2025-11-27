# 🤗 Hugging Face Spaces - Explicación Completa

## ¿Qué son los Spaces?

**Hugging Face Spaces** son aplicaciones web interactivas que puedes crear y desplegar gratuitamente en la plataforma de Hugging Face. Son como mini-aplicaciones que corren en la nube.

### Características:
- 🆓 **Gratis** con CPU básico (2 vCPU, 16GB RAM)
- 🚀 **Fácil deploy**: Git push y listo
- 🔧 **Frameworks soportados**: Gradio, Streamlit, Docker
- 🎯 **Uso común**: Demos de modelos, herramientas IA, apps interactivas

---

## Ejemplos de Spaces para Opositores

### 1. **Mind Map Generator**
- URL: https://huggingface.co/spaces/username/mindmap-generator
- Modelo: GPT-3.5 Turbo (via OpenAI API)
- Input: Tema o URL
- Output: Mapa mental en formato Mermaid/SVG

**Cómo funciona**:
```python
# app.py en el Space
import gradio as gr
import openai

def generate_mindmap(topic):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"Crea un mapa mental sobre: {topic}"
        }]
    )
    return response.choices[0].message.content

interface = gr.Interface(
    fn=generate_mindmap,
    inputs="text",
    outputs="text"
)
interface.launch()
```

---

### 2. **PDF Summarizer**
- Input: PDF file
- Output: Resumen estructurado
- Modelo: Llama 3.1 70B (via Groq API)

---

### 3. **Legal Document Analyzer**
- Input: Texto legal
- Output: Análisis + artículos relevantes
- Modelo: Mixtral 8x7B (via HF Inference API)

---

## Cómo Cambiar de Modelo en un Space

### Opción 1: Usar Variables de Entorno

En el Space, ve a **Settings** → **Repository secrets**:

```python
# app.py
import os

# Cambiar modelo fácilmente
MODEL = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("API_KEY")
PROVIDER = os.getenv("PROVIDER", "openai")  # openai, groq, deepseek

if PROVIDER == "openai":
    client = OpenAI(api_key=API_KEY)
elif PROVIDER == "groq":
    client = Groq(api_key=API_KEY)
elif PROVIDER == "deepseek":
    client = DeepSeek(api_key=API_KEY)
```

---

### Opción 2: Dropdown en la UI

```python
import gradio as gr

MODELS = {
    "GPT-3.5": ("openai", "gpt-3.5-turbo"),
    "GPT-4": ("openai", "gpt-4"),
    "Llama 70B": ("groq", "llama-3.1-70b"),
    "Mixtral": ("groq", "mixtral-8x7b"),
    "DeepSeek": ("deepseek", "deepseek-chat")
}

def generate(text, model_choice):
    provider, model = MODELS[model_choice]
    # Usar el modelo seleccionado
    ...

interface = gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(label="Texto"),
        gr.Dropdown(choices=list(MODELS.keys()), label="Modelo")
    ],
    outputs="text"
)
```

---

### Opción 3: Usar HF Inference API (Múltiples Modelos)

```python
from huggingface_hub import InferenceClient

client = InferenceClient(token=HF_TOKEN)

# Cambiar modelo es solo cambiar el nombre
def generate(text, model):
    response = client.text_generation(
        text,
        model=model,  # "meta-llama/Llama-3.1-70B", "mistralai/Mixtral-8x7B", etc.
        max_new_tokens=500
    )
    return response

# En Gradio
models = [
    "meta-llama/Llama-3.1-70B-Instruct",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "Qwen/Qwen2.5-72B-Instruct",
    "google/gemma-2-27b-it"
]

gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(),
        gr.Dropdown(choices=models, label="Modelo")
    ],
    outputs="text"
).launch()
```

---

## Modelos Disponibles en HF Inference API

### Gratis (con límites):
- **Llama 3.1 70B**: ~$0.60/M tokens
- **Mixtral 8x7B**: ~$0.45/M tokens
- **Qwen 2.5 72B**: ~$0.70/M tokens
- **Gemma 2 27B**: ~$0.40/M tokens

### Cómo funciona:
1. **Free tier**: $0.10/mes (muy limitado)
2. **PRO ($9/mes)**: $2/mes créditos + pay-as-you-go
3. **Sin markup**: Precios directos del proveedor

---

## Crear un Space para OpositAIA

### Estructura del Proyecto:

```
opositaia-space/
├── app.py              # Aplicación Gradio
├── requirements.txt    # Dependencias
├── README.md          # Descripción
└── .env.example       # Variables de entorno
```

### app.py Ejemplo:

```python
import gradio as gr
import os
from openai import OpenAI

# Soportar múltiples proveedores
PROVIDERS = {
    "Groq Llama 8B": {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.1-8b-instant",
        "api_key": os.getenv("GROQ_API_KEY")
    },
    "DeepSeek V3": {
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
        "api_key": os.getenv("DEEPSEEK_API_KEY")
    },
    "Gemini Flash": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "model": "gemini-2.0-flash-exp",
        "api_key": os.getenv("GEMINI_API_KEY")
    }
}

def chat(message, provider_name, history):
    provider = PROVIDERS[provider_name]
    
    client = OpenAI(
        base_url=provider["base_url"],
        api_key=provider["api_key"]
    )
    
    messages = [{"role": "system", "content": "Eres un tutor de oposiciones."}]
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": message})
    
    response = client.chat.completions.create(
        model=provider["model"],
        messages=messages,
        stream=True
    )
    
    partial = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            partial += chunk.choices[0].delta.content
            yield partial

# Interfaz
with gr.Blocks() as demo:
    gr.Markdown("# 🎓 OpositAIA - Tutor de Seguridad Social")
    
    with gr.Row():
        provider = gr.Dropdown(
            choices=list(PROVIDERS.keys()),
            value="Groq Llama 8B",
            label="Modelo IA"
        )
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Tu pregunta")
    clear = gr.Button("Limpiar")
    
    msg.submit(chat, [msg, provider, chatbot], [chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
```

---

## Ventajas de Usar Spaces

### ✅ Pros:
1. **Gratis** para demos y prototipos
2. **Fácil compartir**: URL pública automática
3. **Sin servidor**: HF maneja la infraestructura
4. **Integración**: Fácil conectar con HF models

### ❌ Contras:
1. **Límites de recursos**: CPU básico es lento
2. **Cold start**: Si no se usa, se apaga (tarda en arrancar)
3. **No persistencia**: Datos se pierden al reiniciar
4. **Límites de tráfico**: No para producción con muchos usuarios

---

## Alternativa: Usar HF Inference API en Tu App

En lugar de crear un Space, puedes usar HF Inference API directamente en tu backend:

```python
# backend/agents/llm_providers.py

class HuggingFaceProvider(LLMProvider):
    def __init__(self, model: str = 'meta-llama/Llama-3.1-70B-Instruct'):
        self.model = model
        self.api_key = os.getenv('HF_TOKEN')
        self.client = InferenceClient(token=self.api_key)
    
    async def generate_stream(self, messages, temperature=0.7, max_tokens=2000):
        # Convertir mensajes a prompt
        prompt = self._messages_to_prompt(messages)
        
        # Streaming
        for token in self.client.text_generation(
            prompt,
            model=self.model,
            max_new_tokens=max_tokens,
            temperature=temperature,
            stream=True
        ):
            yield token
```

---

## Resumen

**Spaces** son útiles para:
- Demos públicas
- Prototipos rápidos
- Compartir herramientas con otros

**Para OpositAIA** (producción):
- Mejor usar APIs directas (Groq, DeepSeek, Gemini)
- Más control, mejor rendimiento
- Costos predecibles

**HF Inference API** es buena opción si:
- Quieres acceso a muchos modelos
- No te importa pagar ~$0.50-0.70/M tokens
- Necesitas modelos específicos no disponibles en otros proveedores
