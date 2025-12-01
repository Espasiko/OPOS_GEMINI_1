# 📊 PLAN: Sistema de Tracking de Tokens y Costos

**Fecha**: 30 Noviembre 2025  
**Objetivo**: Implementar conteo preciso de tokens y cálculo de costos por modelo  
**Prioridad**: 🔴 ALTA (esencial para monetización BYOK + COSM)

---

## 🎯 OBJETIVOS

1. **Conteo preciso** de tokens input/output por request
2. **Cálculo automático** de costos según proveedor y modelo
3. **Tracking histórico** por usuario y sesión
4. **Dashboard** de métricas en tiempo real
5. **Alertas** de cuotas y límites

---

## 📋 ARQUITECTURA PROPUESTA

### 1. **Backend: Token Counter Service**

```python
# backend/services/token_counter.py

from typing import Dict, List, Optional
from datetime import datetime
import tiktoken  # OpenAI tokenizer (compatible con la mayoría)

class TokenCounter:
    """Servicio centralizado para conteo de tokens y costos"""
    
    # Tabla de precios (€/M tokens)
    PRICING = {
        'groq-8b': {'input': 0.00, 'output': 0.00},  # Gratis
        'groq-70b': {'input': 0.00, 'output': 0.00},  # Gratis
        'deepseek': {'input': 0.18, 'output': 0.18},  # $0.21/M
        'gemini-pro': {'input': 0.00, 'output': 0.00},  # Gratis tier
        'cohere-command-r': {'input': 0.42, 'output': 0.42},  # $0.50/M
        'cohere-command-r-plus': {'input': 2.50, 'output': 2.50},  # $3/M
        'mistral-agent': {'input': 0.09, 'output': 0.09},  # €0.10/M aprox
        'mistral-vps': {'input': 0.00, 'output': 0.00},  # Self-hosted
    }
    
    def __init__(self):
        # Usar tokenizer de OpenAI (compatible mayoría de modelos)
        self.encoder = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Cuenta tokens en un texto"""
        return len(self.encoder.encode(text))
    
    def count_messages_tokens(self, messages: List[Dict]) -> int:
        """Cuenta tokens en array de mensajes"""
        total = 0
        for msg in messages:
            # 4 tokens por mensaje de overhead
            total += 4
            total += self.count_tokens(msg.get('content', ''))
            # Role también cuenta
            total += self.count_tokens(msg.get('role', ''))
        total += 2  # Overhead de completion
        return total
    
    def calculate_cost(
        self,
        provider_id: str,
        input_tokens: int,
        output_tokens: int
    ) -> Dict[str, float]:
        """Calcula costo de un request"""
        
        pricing = self.PRICING.get(provider_id, {'input': 0, 'output': 0})
        
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        total_cost = input_cost + output_cost
        
        return {
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
            'input_cost_eur': round(input_cost, 6),
            'output_cost_eur': round(output_cost, 6),
            'total_cost_eur': round(total_cost, 6),
            'provider': provider_id
        }

# Singleton global
token_counter = TokenCounter()
```

### 2. **Database Schema: Usage Tracking**

```sql
-- backend/migrations/001_usage_tracking.sql

CREATE TABLE usage_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255),  -- UUID o 'anonymous' para BYOK
    session_id VARCHAR(255),
    provider_id VARCHAR(50) NOT NULL,
    model_name VARCHAR(100),
    
    -- Tokens
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    
    -- Costos (€)
    input_cost_eur DECIMAL(10, 6),
    output_cost_eur DECIMAL(10, 6),
    total_cost_eur DECIMAL(10, 6),
    
    -- Contexto
    endpoint VARCHAR(100),  -- /chat, /generate-exam, etc
    request_type VARCHAR(50),  -- 'chat', 'exam', 'case', etc
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    request_duration_ms INTEGER,
    success BOOLEAN DEFAULT true,
    error_message TEXT
);

-- Índices para queries rápidas
CREATE INDEX idx_usage_user_date ON usage_logs(user_id, created_at DESC);
CREATE INDEX idx_usage_provider ON usage_logs(provider_id, created_at DESC);
CREATE INDEX idx_usage_session ON usage_logs(session_id);

-- Vista agregada por usuario
CREATE VIEW usage_summary_by_user AS
SELECT 
    user_id,
    DATE(created_at) as date,
    provider_id,
    COUNT(*) as requests,
    SUM(input_tokens) as total_input_tokens,
    SUM(output_tokens) as total_output_tokens,
    SUM(total_tokens) as total_tokens,
    SUM(total_cost_eur) as total_cost_eur
FROM usage_logs
GROUP BY user_id, DATE(created_at), provider_id;
```

### 3. **Middleware: Auto-logging de Tokens**

```python
# backend/middleware/usage_tracker.py

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid

class UsageTrackingMiddleware(BaseHTTPMiddleware):
    """Middleware para tracking automático de uso"""
    
    async def dispatch(self, request: Request, call_next):
        # Generar session ID si no existe
        session_id = request.headers.get('X-Session-ID') or str(uuid.uuid4())
        
        # Guardar en request state
        request.state.session_id = session_id
        request.state.start_time = time.time()
        
        # Procesar request
        response = await call_next(request)
        
        # Log de uso se hace en el endpoint específico
        # (aquí solo agregamos metadata)
        
        return response

# En main.py:
# app.add_middleware(UsageTrackingMiddleware)
```

### 4. **Integration en Endpoints**

```python
# backend/routers/chat.py (ejemplo)

from services.token_counter import token_counter
from database import db  # SQLAlchemy/asyncpg

@router.post("/chat")
async def chat(
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    provider_id = request.provider or 'groq-8b'
    provider = get_provider(provider_id)
    
    # 1. Contar tokens INPUT
    input_tokens = token_counter.count_messages_tokens(request.messages)
    
    # 2. Generar respuesta
    response_text = ""
    async for chunk in provider.generate_stream(
        messages=request.messages,
        temperature=request.temperature
    ):
        response_text += chunk
        yield chunk
    
    # 3. Contar tokens OUTPUT
    output_tokens = token_counter.count_tokens(response_text)
    
    # 4. Calcular costo
    usage = token_counter.calculate_cost(
        provider_id=provider_id,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )
    
    # 5. Guardar en DB
    await db.execute(
        """
        INSERT INTO usage_logs (
            user_id, session_id, provider_id, model_name,
            input_tokens, output_tokens, total_tokens,
            input_cost_eur, output_cost_eur, total_cost_eur,
            endpoint, request_type, request_duration_ms, success
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            request.user_id or 'anonymous',
            request.state.session_id,
            provider_id,
            provider.get_info()['model'],
            usage['input_tokens'],
            usage['output_tokens'],
            usage['total_tokens'],
            usage['input_cost_eur'],
            usage['output_cost_eur'],
            usage['total_cost_eur'],
            '/chat',
            'chat',
            int((time.time() - request.state.start_time) * 1000),
            True
        ]
    )
    
    # 6. Retornar metadata de uso en headers
    yield f"\n\n[USAGE: {usage['total_tokens']} tokens, €{usage['total_cost_eur']}]"
```

---

## 🎨 FRONTEND: Dashboard de Uso

### 1. **UsageStats Component**

```tsx
// frontend/components/UsageStats.tsx

interface UsageData {
  totalRequests: number;
  totalTokens: number;
  totalCost: number;
  byProvider: Record<string, {
    tokens: number;
    cost: number;
    requests: number;
  }>;
}

export function UsageStats() {
  const [usage, setUsage] = useState<UsageData | null>(null);
  
  useEffect(() => {
    fetch('/api/usage/summary')
      .then(r => r.json())
      .then(setUsage);
  }, []);
  
  if (!usage) return <div>Cargando...</div>;
  
  return (
    <div className="usage-dashboard">
      <h3>📊 Uso del Mes</h3>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Requests</div>
          <div className="stat-value">{usage.totalRequests}</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-label">Tokens</div>
          <div className="stat-value">
            {(usage.totalTokens / 1000).toFixed(1)}K
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-label">Costo Total</div>
          <div className="stat-value">
            €{usage.totalCost.toFixed(4)}
          </div>
        </div>
      </div>
      
      <h4>Por Modelo</h4>
      <table className="usage-table">
        <thead>
          <tr>
            <th>Proveedor</th>
            <th>Requests</th>
            <th>Tokens</th>
            <th>Costo €</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(usage.byProvider).map(([provider, stats]) => (
            <tr key={provider}>
              <td>{provider}</td>
              <td>{stats.requests}</td>
              <td>{(stats.tokens / 1000).toFixed(1)}K</td>
              <td>€{stats.cost.toFixed(4)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### 2. **Real-time Token Counter**

```tsx
// frontend/components/ChatView.tsx (agregar)

const [currentUsage, setCurrentUsage] = useState({
  tokens: 0,
  cost: 0
});

// Al recibir respuesta, parsear metadata de tokens
useEffect(() => {
  if (lastMessage?.includes('[USAGE:')) {
    const match = lastMessage.match(/\[USAGE: (\d+) tokens, €([\d.]+)\]/);
    if (match) {
      setCurrentUsage({
        tokens: parseInt(match[1]),
        cost: parseFloat(match[2])
      });
    }
  }
}, [lastMessage]);

// Mostrar en UI
<div className="usage-indicator">
  <small>
    {currentUsage.tokens} tokens · €{currentUsage.cost.toFixed(4)}
  </small>
</div>
```

---

## 🔧 IMPLEMENTACIÓN POR FASES

### **FASE 1: Backend Core** (1-2 días)
- [ ] Crear `TokenCounter` service
- [ ] Añadir tabla `usage_logs` a DB
- [ ] Implementar logging básico en `/chat`
- [ ] Test con 2-3 modelos diferentes

### **FASE 2: Integration Completa** (2-3 días)
- [ ] Middleware de tracking automático
- [ ] Logging en todos los endpoints (`/generate-exam`, `/case`, etc)
- [ ] Vista agregada `usage_summary_by_user`
- [ ] API endpoint `/usage/summary`

### **FASE 3: Frontend Dashboard** (1-2 días)
- [ ] Componente `UsageStats`
- [ ] Real-time counter en chat
- [ ] Gráficos de uso (opcional: Chart.js)
- [ ] Exportar CSV de uso

### **FASE 4: Features Avanzadas** (1-2 días)
- [ ] Alertas de cuotas (email/notificación)
- [ ] Límites por usuario (BYOK vs Managed)
- [ ] Predicción de costos mensuales
- [ ] Comparativa de costos por modelo

---

## 📊 MÉTRICAS CLAVE A TRACKEAR

| Métrica | Descripción | Uso |
|---------|-------------|-----|
| **Tokens/request** | Promedio por tipo (chat, exam, case) | Optimización prompts |
| **Cost/request** | Costo promedio por feature | Pricing strategy |
| **Provider distribution** | % uso por modelo | Capacity planning |
| **Daily active users** | Usuarios únicos/día | Growth tracking |
| **Token efficiency** | Output/Input ratio | Quality metrics |
| **Error rate** | % requests fallidos | Reliability |

---

## 💰 TABLA DE COSTOS ACTUALIZADA

```python
# Para incluir en TokenCounter.PRICING

PRICING = {
    # GRATIS (Tier Free) 🆓
    'groq-8b': {
        'input': 0.00, 
        'output': 0.00,
        'limit_daily': 500_000  # 500K tokens/día
    },
    'groq-70b': {
        'input': 0.00,
        'output': 0.00,
        'limit_daily': 500_000
    },
    'gemini-pro': {
        'input': 0.00,
        'output': 0.00,
        'limit_daily': 1_500_000  # 1.5M tokens/día
    },
    'mistral-vps': {
        'input': 0.00,
        'output': 0.00,
        'limit_daily': float('inf')  # Ilimitado
    },
    
    # PAGOS 💰
    'deepseek': {
        'input': 0.18,  # €0.18/M ($0.21/M)
        'output': 0.18,
        'cache_discount': 0.10  # 90% descuento con caché
    },
    'cohere-command-r': {
        'input': 0.42,  # €0.42/M ($0.50/M)
        'output': 0.42,
    },
    'cohere-command-r-plus': {
        'input': 2.50,  # €2.50/M ($3/M)
        'output': 2.50,
    },
    'mistral-agent': {
        'input': 0.09,  # €0.09/M (Medium)
        'output': 0.09,
        'features': ['web-search', 'code-gen']
    },
    
    # FINE-TUNED (futuro) 🎯
    'mistral-8b-finetuned': {
        'input': 0.09,
        'output': 0.09,
        'training_cost': 0.90  # €0.90/M tokens training
    }
}
```

---

## 🎯 KPIs DE ÉXITO

1. **Tracking funcionando al 100%** en todos los endpoints
2. **<1% error rate** en conteo de tokens
3. **Dashboard visible** para usuarios BYOK
4. **Alertas activas** antes de límites (90% cuota)
5. **Datos históricos** de al menos 30 días

---

## 🚀 PRÓXIMOS PASOS (INMEDIATOS)

1. **Instalar tiktoken**: `pip install tiktoken`
2. **Crear tabla `usage_logs`** en PostgreSQL
3. **Implementar `TokenCounter`** service
4. **Modificar `/chat`** endpoint con tracking
5. **Test manual** con 3 proveedores diferentes

---

## 📝 NOTAS IMPORTANTES

- **Privacidad**: Para BYOK, user_id puede ser hash/anónimo
- **Performance**: Logging asíncrono (no bloquear request)
- **Caché**: Considerar descuentos por prompt caching
- **Escalabilidad**: Usar TimescaleDB o particiones por fecha

---

**Estado**: 📋 PLAN COMPLETO  
**Prioridad**: 🔴 ALTA  
**Tiempo estimado**: 6-8 días full implementation  
**Owner**: Backend team

