# 💰 Análisis COMPLETO de Costos IA - Caso Extremo Incluido

**Fecha**: 21 Noviembre 2025

---

## 📊 PRECIOS ACTUALIZADOS (por 1M tokens)

### **Gemini 3 Pro** (Recién lanzado)
| Tipo | Input | Output (con thinking) | Promedio |
|------|-------|----------------------|----------|
| Standard | $2-4 | $12-18 | **~$10/M** |
| Batch (50% desc) | $1-2 | $6-9 | **~$5/M** |

**Límites gratuitos**: ❌ NINGUNO

---

### **Gemini 2.5 Pro**
| Tipo | Input | Output | Promedio |
|------|-------|--------|----------|
| Standard | $1.25-2.50 | $10-15 | **~$6.5/M** |
| Batch | $0.625-1.25 | $5-7.5 | **~$3.25/M** |

**Límites gratuitos**: ✅ Tier gratuito disponible (1,500 RPD, 1M TPM)

---

### **Gemini 2.5 Flash** (RECOMENDADO)
| Tipo | Input | Output | Promedio |
|------|-------|--------|----------|
| Standard | $0.30 | $2.50 | **~$1.4/M** |
| Batch | $0.15 | $1.25 | **~$0.7/M** |

**Límites gratuitos**: ✅ Tier gratuito generoso (1,500 RPD, 1M TPM)

---

### **Groq**
| Modelo | RPM | TPM | TPD | Precio Paid |
|--------|-----|-----|-----|-------------|
| Llama 3.3 70B | 30 | 12K | 100K | ~$0.80/M (estimado) |
| Llama 3.1 8B | 30 | 6K | 500K | ~$0.50/M (estimado) |
| Mixtral 8x7B | 30 | 5K | 500K | ~$0.45/M (estimado) |

**Límites gratuitos**: ✅ Muy generosos (100K-500K tokens/día)
**Velocidad**: ⚡ 500+ tokens/seg (10-20x más rápido que otros)

---

### **DeepSeek V3**
| Tipo | Input | Output | Promedio |
|------|-------|--------|----------|
| Standard | $0.14 | $0.28 | **~$0.21/M** |

**Límites gratuitos**: ❌ Solo $1 crédito inicial
**Velocidad**: 🚀 Rápido (~100-200 tok/s)

---

### **Hugging Face Inference API**
| Tier | Créditos/mes | Costo extra |
|------|--------------|-------------|
| Free | $0.10 | ❌ No permitido |
| PRO ($9/mes) | $2.00 | ✅ Pay-as-you-go |
| Enterprise ($50/mes/usuario) | $2.00/seat | ✅ Pay-as-you-go |

**Modelos disponibles**:
- Llama 3.1 70B: ~$0.60/M tokens
- Mixtral 8x22B: ~$0.90/M tokens
- Qwen 2.5 72B: ~$0.70/M tokens

**Límites**: Sin markup de HF, precios directos del proveedor
**Velocidad**: 🐌 Variable (50-150 tok/s)

---

### **Mistral VPS (Actual)**
| Tipo | Costo |
|------|-------|
| VPS | $10-20/mes fijo |
| Tokens | ∞ ilimitados |

**Velocidad**: 🐌 5-10 tok/s (CPU sin GPU)
**Latencia**: ⚠️ 20-30 segundos por respuesta

---

## 🔥 CASO EXTREMO: 1 Usuario Abusivo (1M tokens/día)

### Escenario: Usuario que usa la app 12h/día sin parar

**Distribución realista**:
- 200 preguntas chat × 2K tokens = 400K tokens
- 50 mapas mentales × 5K tokens = 250K tokens
- 20 casos prácticos × 10K tokens = 200K tokens
- 10 resúmenes largos × 15K tokens = 150K tokens
- **TOTAL: 1M tokens/día**

---

### 💸 COSTO POR PROVEEDOR (1M tokens/día)

| Proveedor | Costo/día | Costo/mes | Notas |
|-----------|-----------|-----------|-------|
| **Gemini 3 Pro** | $10.00 | **$300** | ❌ MUY CARO |
| **Gemini 2.5 Pro** | $6.50 | **$195** | ❌ Caro |
| **Gemini 2.5 Flash** | $1.40 | **$42** | ✅ Razonable |
| **Groq 70B** | $0.80 | **$24** | ✅ Bueno |
| **Groq 8B** | $0.50 | **$15** | ✅ Muy bueno |
| **DeepSeek V3** | $0.21 | **$6.30** | ✅ MEJOR PRECIO |
| **HF Llama 70B** | $0.60 | **$18** | ✅ Bueno |
| **Mistral VPS** | $0.00 | **$15** (VPS fijo) | ✅ Gratis tokens, pero lento |

---

### 🚨 LÍMITES GRATUITOS SUPERADOS

Con 1M tokens/día, TODOS los límites gratuitos se superan:

| Proveedor | Límite gratuito | Tokens extra (paid) |
|-----------|-----------------|---------------------|
| Groq 70B | 100K/día | 900K/día × $0.80 = **$0.72/día** |
| Groq 8B | 500K/día | 500K/día × $0.50 = **$0.25/día** |
| Gemini 2.5 Flash | ~1M/día | 0K (dentro del límite) ✅ |
| DeepSeek | 0 (sin tier free) | 1M/día × $0.21 = **$0.21/día** |

---

## 🎯 ESTRATEGIA ANTI-ABUSO

### 1. **Límites por Usuario**
```typescript
{
  maxTokensPerDay: 100_000,      // 100K tokens/día (generoso)
  maxTokensPerHour: 20_000,      // 20K tokens/hora
  maxRequestsPerMinute: 10,      // 10 requests/min
  warningAt: 80_000,             // Aviso al 80%
  blockAt: 100_000               // Bloqueo al 100%
}
```

**Costo con límites** (100K tokens/día):
- Gemini 2.5 Flash: $0.14/día = **$4.20/mes** ✅
- Groq 8B: GRATIS (dentro del límite) ✅
- DeepSeek: $0.021/día = **$0.63/mes** ✅

---

### 2. **Sistema de Cuotas**

| Plan | Tokens/día | Costo/mes | Target |
|------|------------|-----------|--------|
| **Free** | 10K | $0 | Usuarios casuales |
| **Basic** | 50K | $5 | Estudiantes activos |
| **Pro** | 200K | $15 | Opositores intensivos |
| **Unlimited** | ∞ | $50 | Academias/Grupos |

---

### 3. **Throttling Inteligente**

```python
# Si usuario supera 80% del límite diario
if usage > 0.8 * daily_limit:
    # Cambiar a modelo más barato
    provider = 'deepseek'  # $0.21/M vs $1.40/M
    # O reducir velocidad
    delay_between_requests = 5  # segundos
```

---

## 🏗️ ARQUITECTURA MULTI-PROVEEDOR CON SELECTOR MANUAL

### Backend: Proveedores Disponibles

```python
# backend/agents/llm_providers.py

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages, stream=True):
        pass

class GroqProvider(LLMProvider):
    def __init__(self, model='llama-3.1-8b-instant'):
        self.model = model
        self.api_key = os.getenv('GROQ_API_KEY')
        self.base_url = 'https://api.groq.com/openai/v1'
    
    async def generate(self, messages, stream=True):
        # Implementación con httpx
        pass

class DeepSeekProvider(LLMProvider):
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = 'https://api.deepseek.com'
    
    async def generate(self, messages, stream=True):
        pass

class GeminiProvider(LLMProvider):
    def __init__(self, model='gemini-2.5-flash'):
        self.model = model
        self.api_key = os.getenv('GEMINI_API_KEY')
    
    async def generate(self, messages, stream=True):
        pass

class MistralVPSProvider(LLMProvider):
    def __init__(self):
        self.base_url = 'http://147.93.95.67:8080'
    
    async def generate(self, messages, stream=True):
        pass

# Registry
PROVIDERS = {
    'groq-8b': GroqProvider('llama-3.1-8b-instant'),
    'groq-70b': GroqProvider('llama-3.3-70b-versatile'),
    'deepseek': DeepSeekProvider(),
    'gemini-flash': GeminiProvider('gemini-2.5-flash'),
    'gemini-pro': GeminiProvider('gemini-2.5-pro'),
    'mistral-vps': MistralVPSProvider()
}
```

---

### Backend: Endpoint con Selector

```python
# backend/routers/chat.py

class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    use_rag: bool = True
    provider: str = 'auto'  # 'auto', 'groq-8b', 'deepseek', etc.
    top_k: int = 3
    min_score: float = 0.5

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        # 1. Consultar RAG
        context, sources = await get_rag_context(request)
        
        # 2. Seleccionar proveedor
        if request.provider == 'auto':
            provider = select_best_provider(request, user_usage)
        else:
            provider = PROVIDERS.get(request.provider, PROVIDERS['groq-8b'])
        
        # 3. Generar respuesta
        async for chunk in provider.generate(messages, stream=True):
            yield f"data: {chunk}\n\n"
        
        # 4. Enviar sources
        yield f"data: {json.dumps({'sources': sources})}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

### Frontend: Selector de IA

```typescript
// components/AIProviderSelector.tsx

interface AIProvider {
  id: string;
  name: string;
  speed: 'slow' | 'medium' | 'fast' | 'ultra';
  cost: 'free' | 'cheap' | 'medium' | 'expensive';
  quality: 'good' | 'great' | 'excellent';
}

const PROVIDERS: AIProvider[] = [
  {
    id: 'groq-8b',
    name: 'Groq Llama 8B',
    speed: 'ultra',
    cost: 'free',
    quality: 'good'
  },
  {
    id: 'groq-70b',
    name: 'Groq Llama 70B',
    speed: 'ultra',
    cost: 'free',
    quality: 'great'
  },
  {
    id: 'deepseek',
    name: 'DeepSeek V3',
    speed: 'fast',
    cost: 'cheap',
    quality: 'excellent'
  },
  {
    id: 'gemini-flash',
    name: 'Gemini 2.5 Flash',
    speed: 'fast',
    cost: 'free',
    quality: 'great'
  },
  {
    id: 'gemini-pro',
    name: 'Gemini 2.5 Pro',
    speed: 'medium',
    cost: 'expensive',
    quality: 'excellent'
  },
  {
    id: 'mistral-vps',
    name: 'Mistral (VPS)',
    speed: 'slow',
    cost: 'free',
    quality: 'good'
  }
];

export function AIProviderSelector({ value, onChange }: Props) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">Modelo de IA</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-3 py-2 border rounded-lg"
      >
        <option value="auto">🤖 Automático (Recomendado)</option>
        <optgroup label="⚡ Ultra Rápido + Gratis">
          <option value="groq-8b">Groq Llama 8B</option>
          <option value="groq-70b">Groq Llama 70B</option>
        </optgroup>
        <optgroup label="💰 Barato + Potente">
          <option value="deepseek">DeepSeek V3</option>
        </optgroup>
        <optgroup label="🌟 Google Gemini">
          <option value="gemini-flash">Gemini 2.5 Flash (Gratis)</option>
          <option value="gemini-pro">Gemini 2.5 Pro (Caro)</option>
        </optgroup>
        <optgroup label="🐌 Lento pero Gratis">
          <option value="mistral-vps">Mistral VPS</option>
        </optgroup>
      </select>
      
      {/* Info del proveedor seleccionado */}
      <ProviderInfo provider={PROVIDERS.find(p => p.id === value)} />
    </div>
  );
}
```

---

### Frontend: Integración en ChatView

```typescript
// components/ChatView.tsx

const [selectedProvider, setSelectedProvider] = useState('auto');

// En handleSendMessage
const stream = sendChatMessageStream({
  message: messageText,
  conversation_id: activeConvId,
  use_rag: true,
  provider: selectedProvider,  // <-- Nuevo parámetro
  top_k: 5,
  min_score: 0.5,
});
```

---

## 📊 RESUMEN EJECUTIVO

### ✅ RECOMENDACIÓN FINAL

**Para 99% de usuarios** (< 100K tokens/día):
1. **Groq Llama 8B** (primario) - GRATIS, ultra rápido
2. **DeepSeek V3** (secundario) - $0.21/M, casos complejos
3. **Gemini 2.5 Flash** (terciario) - GRATIS, multimodal
4. **Mistral VPS** (fallback) - Siempre disponible

**Costo esperado**: $0-5/mes para 100 usuarios

---

**Para 1% usuarios abusivos** (1M tokens/día):
- Con límites (100K/día): $4.20/mes ✅
- Sin límites: $6-300/mes según proveedor ⚠️

**Solución**: Implementar límites + throttling + planes de pago

---

### 🚀 PRÓXIMOS PASOS

1. **Implementar selector manual de IA** (2-3h)
2. **Integrar Groq** (1-2h)
3. **Integrar DeepSeek** (1h)
4. **Sistema de límites** (2-3h)
5. **Dashboard de uso** (2h)

**Total: ~8-11 horas de desarrollo**

---

¿Empezamos con el selector manual + Groq?
