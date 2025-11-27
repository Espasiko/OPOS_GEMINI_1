# 🚀 SPRINT 11 - Cloudflare Workers + MCP Server

**Fecha Inicio**: 25 Noviembre 2025  
**Sprint**: 11 - Infraestructura Cloud  
**Duración**: 2 semanas  
**Estado**: 📋 **PLANIFICADO**

---

## 🎯 OBJETIVO PRINCIPAL

Migrar backend a Cloudflare Workers, implementar MCP Server propio, y conectar con Qdrant Cloud (ya configurado).

---

## 📊 CONTEXTO

### Estado Actual
- ✅ Backend FastAPI en VPS
- ✅ Qdrant Cloud configurado (credenciales listas)
- ✅ Cuenta Cloudflare activa
- ✅ Workers ahora GRATIS (antes de pago)

### Objetivo
- 🎯 Backend en Cloudflare Workers
- 🎯 MCP Server funcionando
- 🎯 Conectado a Qdrant Cloud
- 🎯 Autenticación OAuth con Auth0

---

## 📋 PLAN DE EJECUCIÓN

### FASE 1: Setup Cloudflare Workers (Día 1-2)

#### 1.1 Instalar Wrangler CLI
```bash
# Instalar globalmente
npm install -g wrangler

# Verificar instalación
wrangler --version

# Login a Cloudflare
wrangler login
```

#### 1.2 Crear Proyecto Worker
```bash
# Crear proyecto
wrangler init opositaia-backend
cd opositaia-backend

# Estructura
opositaia-backend/
├── src/
│   ├── index.ts          # Entry point
│   ├── router.ts         # Routing
│   └── handlers/         # Request handlers
├── wrangler.toml         # Configuración
└── package.json
```

#### 1.3 Configurar wrangler.toml
```toml
name = "opositaia-backend"
main = "src/index.ts"
compatibility_date = "2025-01-01"

# Variables de entorno
[vars]
ENVIRONMENT = "production"

# Secrets (configurar con wrangler secret put)
# QDRANT_URL
# QDRANT_API_KEY
# AUTH0_DOMAIN
# AUTH0_CLIENT_ID

# Durable Objects
[[durable_objects.bindings]]
name = "SESSIONS"
class_name = "SessionManager"
script_name = "opositaia-backend"

# KV para caché
[[kv_namespaces]]
binding = "CACHE"
id = "tu-kv-namespace-id"
```

---

### FASE 2: Implementar Worker Básico (Día 2-3)

#### 2.1 Entry Point
```typescript
// src/index.ts
export { SessionManager } from './durable-objects/SessionManager';

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // CORS
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }

    // Router
    const url = new URL(request.url);
    
    // Health check
    if (url.pathname === '/health') {
      return Response.json({ status: 'healthy', timestamp: Date.now() });
    }

    // RAG endpoints
    if (url.pathname.startsWith('/api/rag')) {
      return handleRAG(request, env);
    }

    // AI functions
    if (url.pathname.startsWith('/api/ai')) {
      return handleAI(request, env);
    }

    return Response.json({ error: 'Not found' }, { status: 404 });
  },
};
```

#### 2.2 RAG Handler
```typescript
// src/handlers/rag.ts
import { QdrantClient } from '@qdrant/js-client-rest';

export async function handleRAG(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  
  // POST /api/rag/search
  if (url.pathname === '/api/rag/search' && request.method === 'POST') {
    const { query, top_k = 5 } = await request.json();
    
    // Conectar a Qdrant Cloud
    const qdrant = new QdrantClient({
      url: env.QDRANT_URL,
      apiKey: env.QDRANT_API_KEY,
    });
    
    // Buscar (usando embeddings pre-calculados o llamar a API)
    const results = await qdrant.search('opositaia_leyes_seguridad_social', {
      vector: await generateEmbedding(query, env),
      limit: top_k,
    });
    
    return Response.json({
      query,
      results: results.map(r => ({
        id: r.id,
        score: r.score,
        content: r.payload.text,
        metadata: r.payload,
      })),
    });
  }
  
  return Response.json({ error: 'Invalid endpoint' }, { status: 404 });
}
```

---

### FASE 3: MCP Server Implementation (Día 3-5)

#### 3.1 Estructura MCP
```typescript
// src/mcp/server.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server(
  {
    name: 'opositaia-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

// Tool: RAG Search
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'rag_search') {
    const { query, top_k } = request.params.arguments;
    
    // Llamar a Qdrant
    const results = await searchQdrant(query, top_k);
    
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(results, null, 2),
      }],
    };
  }
  
  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Tool: BOE Search
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'boe_search') {
    const { query, fecha_desde, fecha_hasta } = request.params.arguments;
    
    // Llamar a API BOE
    const results = await searchBOE(query, fecha_desde, fecha_hasta);
    
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(results, null, 2),
      }],
    };
  }
});

// Resource: RAG Stats
server.setRequestHandler('resources/read', async (request) => {
  if (request.params.uri === 'opositaia://rag/stats') {
    const stats = await getQdrantStats();
    
    return {
      contents: [{
        uri: request.params.uri,
        mimeType: 'application/json',
        text: JSON.stringify(stats, null, 2),
      }],
    };
  }
});

export { server };
```

#### 3.2 Integrar MCP en Worker
```typescript
// src/index.ts
import { server as mcpServer } from './mcp/server';

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // MCP endpoint
    if (url.pathname === '/mcp') {
      // Handle MCP requests
      return handleMCPRequest(request, env);
    }
    
    // ... resto de endpoints
  },
};

async function handleMCPRequest(request: Request, env: Env): Promise<Response> {
  const body = await request.json();
  
  // Process MCP request
  const response = await mcpServer.handleRequest(body);
  
  return Response.json(response);
}
```

---

### FASE 4: Autenticación OAuth (Día 5-6)

#### 4.1 Setup Auth0
```bash
# 1. Crear cuenta en Auth0 (free tier)
# 2. Crear aplicación
# 3. Configurar callback URLs
# 4. Obtener credenciales
```

#### 4.2 Middleware de Autenticación
```typescript
// src/middleware/auth.ts
import { jwtVerify } from 'jose';

export async function verifyToken(token: string, env: Env): Promise<any> {
  try {
    const JWKS = await fetch(`https://${env.AUTH0_DOMAIN}/.well-known/jwks.json`);
    const keys = await JWKS.json();
    
    const { payload } = await jwtVerify(token, keys, {
      issuer: `https://${env.AUTH0_DOMAIN}/`,
      audience: env.AUTH0_CLIENT_ID,
    });
    
    return payload;
  } catch (error) {
    throw new Error('Invalid token');
  }
}

export async function requireAuth(request: Request, env: Env): Promise<any> {
  const authHeader = request.headers.get('Authorization');
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    throw new Error('Missing authorization header');
  }
  
  const token = authHeader.substring(7);
  return await verifyToken(token, env);
}
```

#### 4.3 Proteger Endpoints
```typescript
// src/handlers/rag.ts
export async function handleRAG(request: Request, env: Env): Promise<Response> {
  try {
    // Verificar autenticación
    const user = await requireAuth(request, env);
    
    // Procesar request
    // ...
    
  } catch (error) {
    return Response.json(
      { error: error.message },
      { status: 401 }
    );
  }
}
```

---

### FASE 5: Deploy y Testing (Día 6-7)

#### 5.1 Configurar Secrets
```bash
# Configurar secrets
wrangler secret put QDRANT_URL
wrangler secret put QDRANT_API_KEY
wrangler secret put AUTH0_DOMAIN
wrangler secret put AUTH0_CLIENT_ID
wrangler secret put AUTH0_CLIENT_SECRET
```

#### 5.2 Deploy
```bash
# Deploy a producción
wrangler deploy

# Ver logs
wrangler tail
```

#### 5.3 Testing
```bash
# Test health
curl https://opositaia-backend.tu-usuario.workers.dev/health

# Test RAG (con auth)
curl -X POST https://opositaia-backend.tu-usuario.workers.dev/api/rag/search \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "incapacidad temporal", "top_k": 5}'
```

---

## 🔧 ARCHIVOS A CREAR

```
opositaia-backend/
├── src/
│   ├── index.ts                    # Entry point
│   ├── router.ts                   # Routing
│   ├── handlers/
│   │   ├── rag.ts                  # RAG endpoints
│   │   ├── ai.ts                   # AI functions
│   │   └── boe.ts                  # BOE integration
│   ├── mcp/
│   │   ├── server.ts               # MCP server
│   │   ├── tools.ts                # MCP tools
│   │   └── resources.ts            # MCP resources
│   ├── middleware/
│   │   ├── auth.ts                 # Authentication
│   │   ├── cors.ts                 # CORS
│   │   └── rate-limit.ts           # Rate limiting
│   ├── durable-objects/
│   │   └── SessionManager.ts       # Session management
│   └── utils/
│       ├── qdrant.ts               # Qdrant client
│       ├── embeddings.ts           # Embedding generation
│       └── errors.ts               # Error handling
├── wrangler.toml                   # Configuración
├── package.json
└── tsconfig.json
```

---

## 📊 MÉTRICAS DE ÉXITO

### Funcionales
- [ ] Worker desplegado y funcionando
- [ ] MCP Server respondiendo
- [ ] Conectado a Qdrant Cloud
- [ ] Autenticación OAuth funcionando
- [ ] Todos los endpoints migrados

### Performance
- [ ] Latencia < 200ms (p95)
- [ ] 99.9% uptime
- [ ] Sin cold starts perceptibles

### Costes
- [ ] €0/mes (free tier)
- [ ] < 100K requests/día

---

## ⏱️ TIMELINE

**Total**: 2 semanas (7 días laborables)

- **Día 1-2**: Setup Cloudflare + Worker básico
- **Día 2-3**: Implementar endpoints
- **Día 3-5**: MCP Server
- **Día 5-6**: Autenticación
- **Día 6-7**: Deploy + Testing

---

## ✅ CRITERIOS DE COMPLETADO

- [ ] Worker desplegado en producción
- [ ] MCP Server funcionando
- [ ] Qdrant Cloud conectado
- [ ] Auth0 configurado
- [ ] Tests E2E pasando
- [ ] Documentación actualizada
- [ ] Frontend conectado al nuevo backend

---

## 🚀 PRÓXIMO SPRINT

**Sprint 12**: Agentes BOE + Jurisprudencia

---

**Documento creado**: 23 Noviembre 2025  
**Estado**: Listo para empezar  
**Prerequisitos**: Qdrant Cloud configurado ✅, Cuenta Cloudflare ✅
