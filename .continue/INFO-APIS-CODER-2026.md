# 📋 INFORMACIÓN COMPLETA - APIs de Modelos Coder (Enero 2026)

## 🎯 RESUMEN EJECUTIVO

**Problema**: Codestral local en Ollama está lento o no responde bien.

**Solución**: Configuré múltiples alternativas con prioridades:
1. **Ollama Local** (más rápido)
2. **Mistral API** (Codestral oficial)
3. **Alternativas Gratis** (OpenRouter, etc.)
4. **Claude** (backup)

---

## 🔑 MISTRAL API - Codestral Oficial

### 📍 Endpoint Principal
```
https://api.mistral.ai/v1/chat/completions
```

### 🔐 API Key
- **Obtener**: https://console.mistral.ai/api-keys
- **Variable**: `MISTRAL_API_KEY`
- **Formato**: Comienza con `sk-`

### 📊 Modelos Disponibles
| Modelo | Descripción | Contexto | Precio |
|--------|-------------|----------|--------|
| `codestral-latest` | Modelo principal de código | 32K | $0.20/M input, $0.60/M output |
| `codestral-mamba-latest` | Versión Mamba optimizada | 256K | $0.20/M input, $0.60/M output |
| `mistral-large-latest` | Modelo general grande | 128K | $2.00/M input, $6.00/M output |
| `mistral-medium-latest` | Modelo general mediano | 32K | $0.15/M input, $0.45/M output |

### 💻 Ejemplo de Uso
```python
import os
from mistralai import Mistral

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

response = client.chat.complete(
    model="codestral-latest",
    messages=[{"role": "user", "content": "Escribe una función factorial en Python"}]
)
```

### ⚙️ Configuración en Continue
```yaml
- name: Codestral API (Mistral)
  provider: mistral
  model: codestral-latest
  apiKey: ${MISTRAL_API_KEY}
  roles: [chat, edit, apply, autocomplete]
  capabilities: [tool_use]
```

---

## 🎁 ALTERNATIVAS GRATIS (2026)

### 🥤 LiquidAI (COMPLETAMENTE GRATIS)
**Proveedor**: OpenRouter
**API Key**: Necesaria (gratuita)
**Obtener**: https://openrouter.ai/keys

#### Modelos Disponibles
| Modelo | Descripción | Contexto | Costo |
|--------|-------------|----------|-------|
| `liquid/lfm-2.5-1.2b-thinking:free` | Pensamiento estructurado | 32K | **$0.00** |
| `liquid/lfm-2.5-1.2b-instruct:free` | Instrucciones directas | 32K | **$0.00** |

#### Configuración
```yaml
- name: LiquidAI LFM2.5 Thinking (GRATIS)
  provider: openrouter
  model: liquid/lfm-2.5-1.2b-thinking:free
  apiKey: ${OPENROUTER_API_KEY}
  roles: [chat, edit]
  capabilities: [tool_use]
```

### ⚡ GLM 4.7 Flash (MUY BARATO)
**Proveedor**: OpenRouter
**Modelo**: `z-ai/glm-4.7-flash`
**Costo**: $0.07/M input, $0.40/M output
**Contexto**: 200K tokens

#### Configuración
```yaml
- name: GLM 4.7 Flash (BARATO)
  provider: openrouter
  model: z-ai/glm-4.7-flash
  apiKey: ${OPENROUTER_API_KEY}
  roles: [chat, edit, apply]
  capabilities: [tool_use]
```

### 🤗 Hugging Face (Inference Gratis)
**Proveedor**: Hugging Face
**API Key**: Opcional (algunos modelos requieren)
**Obtener**: https://huggingface.co/settings/tokens

#### Modelos Recomendados
| Modelo | Descargas | Contexto | Inference |
|--------|-----------|----------|-----------|
| Qwen/Qwen2.5-Coder-7B-Instruct | 1.09M | 32K | ✅ Gratis |
| Qwen/Qwen2.5-Coder-1.5B | 541K | 32K | ✅ Gratis |
| codellama/CodeLlama-7b-hf | 2.1M | 16K | ✅ Gratis |
| deepseek-ai/deepseek-coder-6.7b-base | 890K | 32K | ✅ Gratis |

#### Configuración
```yaml
- name: Qwen2.5 Coder (HF Gratis)
  provider: huggingface
  model: Qwen/Qwen2.5-Coder-7B-Instruct
  apiKey: ${HF_API_KEY}  # Opcional
  roles: [chat, edit]
```

---

## 🏆 RANKING DE OPCIONES (2026)

### ⭐⭐⭐⭐⭐ EXCELENTE
1. **Codestral Local (Ollama)** - Más rápido si funciona bien
2. **Codestral API (Mistral)** - Oficial, mejor calidad
3. **LiquidAI LFM2.5 (Gratis)** - Completamente gratis, buena calidad

### ⭐⭐⭐⭐ BUENO
4. **GLM 4.7 Flash** - Muy barato, buen rendimiento
5. **Qwen2.5 Coder (HF)** - Gratis, probado
6. **Claude Sonnet** - Excelente pero pago

### ⭐⭐⭐ ACEPTABLE
7. **Mistral Medium API** - Bueno para general
8. **CodeLlama (HF)** - Clásico confiable

---

## 🔧 CONFIGURACIÓN DE VARIABLES DE ENTORNO

### Para Linux/Mac
```bash
# Mistral API
export MISTRAL_API_KEY='sk-xxxxxxxxxxxxxxxx'

# OpenRouter (para modelos gratis)
export OPENROUTER_API_KEY='sk-or-v1-xxxxxxxxxxxxxxxx'

# Hugging Face (opcional)
export HF_API_KEY='hf_xxxxxxxxxxxxxxxxxxxx'

# Claude (opcional)
export ANTHROPIC_API_KEY='sk-ant-xxxxxxxxxxxxx'
```

### Para hacer permanente
```bash
# Agregar al ~/.bashrc o ~/.zshrc
echo "export MISTRAL_API_KEY='tu-api-key'" >> ~/.bashrc
echo "export OPENROUTER_API_KEY='tu-api-key'" >> ~/.bashrc
source ~/.bashrc
```

---

## 📊 COMPARACIÓN DE COSTOS (2026)

| Servicio | Modelo | Input/M | Output/M | Gratuito |
|----------|--------|---------|----------|----------|
| **LiquidAI** | LFM2.5 | **$0.00** | **$0.00** | ✅ |
| **GLM** | 4.7 Flash | $0.07 | $0.40 | ❌ |
| **Mistral** | Codestral | $0.20 | $0.60 | ❌ |
| **Mistral** | Medium | $0.15 | $0.45 | ❌ |
| **Anthropic** | Claude Sonnet | $3.00 | $15.00 | ❌ |
| **HuggingFace** | Qwen2.5 | $0.00 | $0.00 | ✅ |

---

## 🚀 RECOMENDACIONES POR ESCENARIO

### 💰 Si quieres GRATIS
1. **LiquidAI LFM2.5** (mejor calidad gratis)
2. **Hugging Face Qwen2.5** (alternativa sólida)

### ⚡ Si quieres VELOCIDAD
1. **Codestral Local (Ollama)** (si funciona bien)
2. **GLM 4.7 Flash** (muy rápido, barato)

### 🎯 Si quieres CALIDAD
1. **Codestral API (Mistral)** (oficial)
2. **Claude Sonnet** (mejor general)

### 🔧 Si quieres CODING ESPECÍFICO
1. **Codestral** (cualquiera de las versiones)
2. **Qwen2.5 Coder** (especializado en código)

---

## 🔍 CÓMO PROBAR CADA OPCIÓN

### 1. LiquidAI (Gratis)
```bash
# Instalar si no tienes
pip install openai

# Probar
python -c "
import openai
client = openai.OpenAI(
    api_key='tu-openrouter-key',
    base_url='https://openrouter.ai/api/v1'
)
response = client.chat.completions.create(
    model='liquid/lfm-2.5-1.2b-thinking:free',
    messages=[{'role': 'user', 'content': 'Hola, ¿funcionas?'}]
)
print(response.choices[0].message.content)
"
```

### 2. Mistral API
```bash
# Instalar
pip install mistralai

# Probar
python -c "
from mistralai import Mistral
client = Mistral(api_key='tu-mistral-key')
response = client.chat.complete(
    model='codestral-latest',
    messages=[{'role': 'user', 'content': 'Hola, ¿funcionas?'}]
)
print(response.choices[0].message.content)
"
```

### 3. Hugging Face
```bash
# Instalar
pip install huggingface_hub

# Probar
python -c "
from huggingface_hub import InferenceClient
client = InferenceClient(model='Qwen/Qwen2.5-Coder-7B-Instruct')
response = client.text_generation('Hola, ¿funcionas?')
print(response)
"
```

---

## 📞 FUENTES Y REFERENCIAS

- **Mistral API**: https://docs.mistral.ai/api
- **OpenRouter**: https://openrouter.ai/models
- **Hugging Face**: https://huggingface.co/models?pipeline_tag=text-generation&search=coder
- **Console Mistral**: https://console.mistral.ai/
- **OpenRouter Keys**: https://openrouter.ai/keys

---

## 🎯 CONCLUSIÓN

**Opción Recomendada**: LiquidAI LFM2.5 (gratis) + Codestral API (Mistral) como backup.

**Por qué**:
- LiquidAI es completamente gratis y tiene buena calidad
- Mistral Codestral es el modelo oficial de código de Mistral
- Combinación perfecta de costo cero + calidad profesional

**Próximos pasos**:
1. Obtener API key de OpenRouter
2. Configurar variable `OPENROUTER_API_KEY`
3. Probar LiquidAI primero
4. Si necesitas más calidad, agregar Mistral API

---

*Información actualizada para enero 2026*
*Basado en documentación oficial de proveedores*