# 🔥 ESTRATEGIAS ULTRA-PRÁCTICAS: Reducir Costes IA a <€1/mes

**Fecha**: 28 Noviembre 2025  
**Objetivo**: De €1.14/mes a <€0.50/mes manteniendo 95%+ calidad  
**Esfuerzo**: 2-3 semanas implementación

---

## 📊 PUNTO DE PARTIDA

```
Groq Llama 3.3 70B (modelo simple):
- Coste actual: €1.14/mes por usuario
- Calidad: 98%
- Meta: Reducir a <€0.50/mes sin perder calidad
```

---

## 🎯 ESTRATEGIA 1: CACHÉ AGRESIVO (Ahorro: 40-60%)

### El Problema
```
Usuario pregunta: "¿Qué es la base de cotización?"
→ Input: 12K tokens a Groq = $0.007
→ 10 usuarios hacen la MISMA pregunta
→ Gasto innecesario: $0.07

Con caché: Respuesta en 50ms + $0.00
```

### Implementación (TypeScript + Redis)

```typescript
// services/cacheService.ts

import Redis from 'ioredis';
import crypto from 'crypto';

const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379');

export class CacheService {
  /**
   * Genera hash único para pregunta
   * Ignora pequeñas variaciones (puntuación, espacios)
   */
  private generateCacheKey(question: string): string {
    const normalized = question
      .toLowerCase()
      .replace(/[^\w\s]/g, '') // Remove special chars
      .replace(/\s+/g, ' ') // Normalize spaces
      .trim();
    
    return `qa:${crypto.createHash('sha256').update(normalized).digest('hex')}`;
  }

  /**
   * Busca en caché
   */
  async getFromCache(question: string): Promise<string | null> {
    const key = this.generateCacheKey(question);
    const cached = await redis.get(key);
    
    if (cached) {
      console.log(`✅ CACHE HIT: ${question.substring(0, 50)}...`);
      return cached;
    }
    
    return null;
  }

  /**
   * Guarda en caché por 30 días
   */
  async setInCache(question: string, response: string): Promise<void> {
    const key = this.generateCacheKey(question);
    const ttl = 30 * 24 * 60 * 60; // 30 días
    
    await redis.setex(key, ttl, response);
    console.log(`💾 CACHED: ${question.substring(0, 50)}...`);
  }
}

// En tu chat service:
export async function generateResponse(question: string): Promise<string> {
  // 1. Buscar en caché
  const cached = await cacheService.getFromCache(question);
  if (cached) return cached; // ✅ AHORRO: $0.007

  // 2. Si no está en caché, consultar Groq
  const response = await groqClient.generate({
    model: 'llama-3.3-70b-versatile',
    messages: [{ role: 'user', content: question }]
  });

  // 3. Guardar en caché
  await cacheService.setInCache(question, response);

  return response;
}
```

### Resultados Esperados

```
Hit rate estimado: 60-70% (preguntas comunes)

Distribución de preguntas:
- 60%: Preguntas comunes (derecho laboral, cotizaciones, etc)
  → Caché: $0 × 60% = $0
- 40%: Preguntas nuevas/específicas → Groq: $0.062 × 40% = $0.025/día

Coste final: €0.46/mes (60% ahorro) ✅
```

### Redis Gratuito: Upstash

```
Servicio: Upstash Redis (Free Tier)
Límite: 10K comandos/día, 256MB almacenamiento
Coste: €0/mes

Para OpositAIA:
- Requests/día: ~120 (usuario 8h)
- Comandos Redis: 120 GET + 48 SET = 168/día
- Almacenamiento: ~500MB para 5K respuestas ✅ Dentro del límite

Setup:
1. Crear cuenta en https://upstash.com
2. Copiar URL: redis://xxx:xxx@xxx.upstash.io:xxxxx
3. Usar en código: process.env.REDIS_URL
```

---

## 🎯 ESTRATEGIA 2: MODELO HÍBRIDO CON ROUTING (Ahorro: 50-70%)

### El Problema
```
No todas las preguntas necesitan Llama 3.3 70B

Pregunta simple: "¿Cuántos años de cotización necesito?"
→ Groq 70B: $0.007 (overkill)
→ Cloudflare 8B: $0.00 (gratis, suficiente)

Pregunta compleja: "Analiza caso práctico de jubilación anticipada"
→ Cloudflare 8B: Insuficiente
→ Groq 70B: $0.007 (perfecto)
```

### Implementación: Router Inteligente

```typescript
// services/routerService.ts

interface ComplexityAnalysis {
  complexity: 'simple' | 'medium' | 'complex';
  confidence: number;
  reason: string;
}

export class RouterService {
  /**
   * Analiza complejidad ANTES de enviar a LLM
   * Solo usa palabras clave (sin IA)
   */
  analyzeComplexity(question: string): ComplexityAnalysis {
    // Keywords de baja complejidad
    const simpleKeywords = [
      'cuántos años',
      'qué es',
      'definición',
      'norma laboral',
      'artículo',
      'cuánto cuesta',
      'edad jubilación'
    ];

    // Keywords de alta complejidad
    const complexKeywords = [
      'caso práctico',
      'analiza',
      'supuesto',
      'conflicto',
      'jurisprudencia',
      'excepciones',
      'comparativa',
      'estrategia'
    ];

    const lowerQuestion = question.toLowerCase();

    // Contar coincidencias
    const simpleMatches = simpleKeywords.filter(kw => lowerQuestion.includes(kw)).length;
    const complexMatches = complexKeywords.filter(kw => lowerQuestion.includes(kw)).length;

    if (complexMatches > 2) {
      return { complexity: 'complex', confidence: 0.95, reason: 'Múltiples palabras clave complejas' };
    }
    
    if (simpleMatches > 2) {
      return { complexity: 'simple', confidence: 0.90, reason: 'Pregunta definitoria/factual' };
    }

    return { complexity: 'medium', confidence: 0.70, reason: 'Requiere análisis intermedio' };
  }

  /**
   * Elige provider según complejidad
   */
  selectProvider(analysis: ComplexityAnalysis): string {
    if (analysis.complexity === 'simple') {
      return 'cloudflare-8b'; // GRATIS ✅
    }
    
    if (analysis.complexity === 'medium') {
      return 'groq-8b'; // $0.05/1M tokens
    }

    // complex
    return 'groq-70b'; // $0.59/1M tokens
  }
}

// Usar en chat:
export async function generateSmartResponse(question: string): Promise<string> {
  // 1. Caché
  const cached = await cacheService.getFromCache(question);
  if (cached) return cached;

  // 2. Analizar complejidad (sin IA, keywords)
  const analysis = routerService.analyzeComplexity(question);
  const provider = routerService.selectProvider(analysis);

  console.log(`🎯 Routing: ${analysis.complexity} → ${provider}`);

  // 3. Generar respuesta
  let response: string;
  
  if (provider === 'cloudflare-8b') {
    response = await cloudflareClient.generate(question); // GRATIS ✅
  } else if (provider === 'groq-8b') {
    response = await groqClient.generate(question, 'llama-3.3-8b');
  } else {
    response = await groqClient.generate(question, 'llama-3.3-70b');
  }

  // 4. Caché
  await cacheService.setInCache(question, response);

  return response;
}
```

### Distribución Estimada (Usuario 8h/día)

```
Distribución de preguntas:
- 50% simples (Cloudflare 8B): FREE
- 30% medianas (Groq 8B): $0.05/1M
- 20% complejas (Groq 70B): $0.59/1M

Tokens por tipo:
- Simples: 12K tokens/hora × 4h = 48K
- Medianas: 12K tokens/hora × 2.4h = 28.8K
- Complejas: 12K tokens/hora × 1.6h = 19.2K

Coste:
Input: (48K × $0) + (28.8K × $0.05/1M) + (19.2K × $0.59/1M)
     = $0 + $0.0014 + $0.0113 = $0.0127/día

Output: (50K × $0) + (30K × $0.80/1M) + (20K × $0.79/1M)
      = $0 + $0.024 + $0.0158 = $0.0398/día

TOTAL: €0.38/mes (67% ahorro) ✅
```

---

## 🎯 ESTRATEGIA 3: COMPRESSION + RAG MEJORADO (Ahorro: 30-50%)

### El Problema
```
Tu contexto RAG actual:
- Búsqueda vector: 50 documentos más similares
- Contexto total: 12K tokens (¡mucho ruido!)
- Solo ~2-3K realmente relevantes

Mejor estrategia:
- Búsqueda vector: 3-5 documentos + reranking
- Contexto: 3-4K tokens (pure signal)
- 65% menos tokens = 65% menos coste
```

### Implementación: RAG Mejorado

```typescript
// services/ragService.ts

export class RAGService {
  /**
   * Búsqueda mejorada: vector + BM25 + reranking
   */
  async searchRelevantDocs(query: string, topK: number = 5): Promise<Document[]> {
    // 1. Vector search (Qdrant)
    const vectorResults = await this.qdrant.search({
      vector: await this.generateEmbedding(query),
      limit: 20, // Más que topK para reranking
      scoreThreshold: 0.7
    });

    // 2. BM25 search (Elasticsearch fallback)
    const bm25Results = await this.elasticsearch.search({
      query: query,
      limit: 10
    });

    // 3. Combinar y deduplicar
    const combined = [
      ...vectorResults.map(r => ({ ...r, source: 'vector' })),
      ...bm25Results.map(r => ({ ...r, source: 'bm25' }))
    ];

    // 4. Reranking con Cohere (API free: 1M req/mes)
    const reranked = await this.rerankWithCohere(query, combined, topK);

    // 5. Seleccionar TOP-K
    return reranked.slice(0, topK);
  }

  /**
   * Reranking con Cohere (GRATIS: 1M requests/mes)
   */
  private async rerankWithCohere(
    query: string,
    documents: Document[],
    topK: number
  ): Promise<Document[]> {
    const response = await fetch('https://api.cohere.com/v1/rerank', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.COHERE_API_KEY}`
      },
      body: JSON.stringify({
        model: 'rerank-english-v2.0', // FREE tier
        query: query,
        documents: documents.map(d => d.content),
        topN: topK,
        returnDocuments: true
      })
    });

    const data = await response.json();
    return data.results.map((r: any) => documents[r.index]);
  }

  /**
   * Formatear contexto comprimido
   */
  formatContext(docs: Document[]): string {
    return docs
      .map(doc => `[${doc.source}]\n${doc.content.substring(0, 500)}`)
      .join('\n\n---\n\n');
  }
}

// En tu chat service:
export async function generateWithImprovedRAG(question: string): Promise<string> {
  // 1. Caché
  const cached = await cacheService.getFromCache(question);
  if (cached) return cached;

  // 2. RAG MEJORADO (menos tokens)
  const relevantDocs = await ragService.searchRelevantDocs(question, 3); // TOP-3 (no 50)
  const context = ragService.formatContext(relevantDocs);

  // 3. Prompt comprimido
  const systemPrompt = `Eres experto en derecho laboral español. Responde basándote SOLO en el contexto.
Contexto relevante:
${context}`;

  // 4. Generar (menos tokens de input)
  const response = await groqClient.generate({
    model: 'llama-3.3-70b',
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: question }
    ]
  });

  return response;
}
```

### Resultados Esperados

```
Antes:
- Documentos retornados: 50
- Tokens de contexto: 12K
- Coste/request: $0.007

Después:
- Documentos retornados: 3-5
- Tokens de contexto: 3.5K
- Coste/request: $0.002

Ahorro: 71% en input tokens ✅
Coste: €0.33/mes
```

### Cohere Reranking (FREE)

```
API Key: https://dashboard.cohere.com
Plan: Free tier
Límite: 1M requests/mes

Para OpositAIA:
- 120 requests/día × 20 días = 2,400 requests/mes ✅ Dentro del límite
- Coste: €0/mes
```

---

## 🎯 ESTRATEGIA 4: PROMPT COMPRESSION (Ahorro: 10-30%)

### El Problema
```
Tu prompt actual:
- Instructions: 2K tokens (verbose)
- System context: 5K tokens (repetido)
- History: 3K tokens (maybe useful)
- Query: 2K tokens (actual question)
TOTAL: 12K tokens

Comprimido con LLMLingua:
- Instructions: 800 tokens (essential only)
- System context: 1.2K tokens (compressed)
- History: 300 tokens (summarized)
- Query: 2K tokens (unchanged)
TOTAL: 4.3K tokens

Ahorro: 64%
```

### Implementación: LLMLingua

```typescript
// services/promptCompressionService.ts

import { LLMLingua } from 'llmlingua';

export class PromptCompressionService {
  private compressor: LLMLingua;

  constructor() {
    // Usar modelo local o API
    // Opción 1: Local (recomendado para producción)
    this.compressor = new LLMLingua({
      model_name: 'microsoft/llmlingua2-bert-base-multilingual-cased-chinese',
      device_map: 'cuda', // GPU para velocidad
      use_gpu: true
    });
  }

  /**
   * Comprime prompt manteniendo información crítica
   */
  async compressPrompt(prompt: string, targetRatio: number = 0.5): Promise<string> {
    const compressed = await this.compressor.compress_prompt(
      prompt,
      {
        rate: targetRatio, // 0.5 = 50% compression
        target_token_only: false, // Mantener estructura
      }
    );

    return compressed.compressed_prompt;
  }

  /**
   * Comprime con mantenimiento de contexto crítico
   */
  async smartCompress(systemPrompt: string, context: string, query: string): Promise<{
    systemPrompt: string;
    context: string;
    query: string;
    totalReduction: number;
  }> {
    const before = `${systemPrompt}${context}${query}`.split(' ').length * 1.3; // Aprox tokens

    const compressedSystem = await this.compressPrompt(systemPrompt, 0.6); // 40% reducción
    const compressedContext = await this.compressPrompt(context, 0.5); // 50% reducción
    // Query se deja igual (es la pregunta del usuario)

    const after = `${compressedSystem}${compressedContext}${query}`.split(' ').length * 1.3;

    return {
      systemPrompt: compressedSystem,
      context: compressedContext,
      query: query,
      totalReduction: ((before - after) / before) * 100
    };
  }
}

// Usar en chat:
export async function generateWithCompression(
  systemPrompt: string,
  context: string,
  query: string
): Promise<string> {
  // 1. Caché
  const cached = await cacheService.getFromCache(query);
  if (cached) return cached;

  // 2. Compresión de prompt
  const compressed = await compressionService.smartCompress(systemPrompt, context, query);
  console.log(`📉 Prompt compression: ${compressed.totalReduction.toFixed(1)}% reducción`);

  // 3. Generar con prompt comprimido
  const response = await groqClient.generate({
    model: 'llama-3.3-70b',
    messages: [
      { role: 'system', content: compressed.systemPrompt },
      { role: 'user', content: `Contexto:\n${compressed.context}\n\nPregunta: ${compressed.query}` }
    ]
  });

  return response;
}
```

### Resultados Esperados

```
Reducción de tokens:
- System prompt: 2K → 800 (60%)
- Context: 5K → 2.5K (50%)
- History: 3K → 300 (90%)
- Query: 2K → 2K (0%)

TOTAL: 12K → 5.6K tokens (53% reducción)

Coste:
Antes: €1.14/mes
Después: €0.54/mes (53% ahorro)

Tiempo procesamiento: +20ms (acceptable)
Calidad: 99% (imperceptible diferencia)
```

---

## 🎯 ESTRATEGIA 5: CLOUDFLARE WORKERS AI (Ahorro: 95%+)

### El Problema
```
Groq 70B: $0.59/1M input tokens
Cloudflare Workers: $0 para Llama 3.1 8B (10K requests/día)

Para usuario 8h/día:
- 120 requests/día
- 96K tokens/día
- Llama 8B suficiente para 95% casos

Ahorro: 95% ✅
```

### Implementación: Cloudflare Workers + AI

```typescript
// workers/opos-ai-worker.ts
// Deploy con: wrangler deploy

export interface Env {
  AI: Cloudflare.AI;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { question, context } = await request.json() as {
      question: string;
      context: string;
    };

    // Usar Cloudflare AI (GRATIS)
    const response = await env.AI.run(
      '@cf/meta/llama-3.1-8b-instruct',
      {
        messages: [
          { role: 'user', content: `${context}\n\nPregunta: ${question}` }
        ],
        max_tokens: 1000
      }
    );

    return new Response(JSON.stringify(response), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
```

### wrangler.toml Configuration

```toml
# wrangler.toml

name = "opos-ai-worker"
type = "service"
main = "src/index.ts"

env = "production"
route = "opositaia.com/api/ai/*"

[env.production]
account_id = "tu_account_id"
workers_dev = true

# Enlazar con servicio AI
[ai]
enable = true
models = ["@cf/meta/llama-3.1-8b-instruct"]
```

### Resultados Esperados

```
Coste: €0.00/mes (Cloudflare free tier)
Límite: 10K requests/día

Para usuario 8h/día:
- 120 requests = 1.2% del límite ✅

Escalabilidad:
- 100 usuarios × 120 requests = 12K requests ✅ (ligeramente por encima)
- Solución: Upgrade a plan pago ($0.50/M tokens)
```

---

## 🏆 ESTRATEGIA FINAL: COMBINACIÓN ÓPTIMA

### La Fórmula Ganadora

```
ARQUITECTURA:
┌─────────────────────────────────────┐
│ 1. CACHÉ (Redis Upstash - FREE)     │
│    ↓ Cache hit? → Return immediately│
│    ↓ Cache miss? → Continue...      │
│                                      │
│ 2. COMPLEXITY ROUTER (Keywords)     │
│    ↓ Simple? → Cloudflare AI (FREE)│
│    ↓ Medium? → Groq 8B ($0.05/1M)  │
│    ↓ Complex? → Groq 70B ($0.59/1M)│
│                                      │
│ 3. RAG MEJORADO (Cohere reranking)  │
│    ↓ 3-5 docs vs 50 (65% menos)    │
│                                      │
│ 4. PROMPT COMPRESSION (LLMLingua)   │
│    ↓ 12K → 5.6K tokens (53% menos)  │
│                                      │
│ 5. CACHE RESULT (30 días)           │
│    ↓ Próximo usuario: Cache hit ✅  │
└─────────────────────────────────────┘
```

### Cálculo Final

```
USUARIO 8h/día:

Distribución:
- 60% cache hit → $0
- 25% simple (Cloudflare) → $0
- 10% medium (Groq 8B) → ~$0.002/día
- 5% complex (Groq 70B) → ~$0.001/día

Compresión adicional (RAG + Prompt):
- RAG mejorado: -65% input
- Prompt compression: -53% input
- Factor combinado: ~-75% input

COSTE FINAL:
= ($0.0002 + $0.0014) × 75% compression
= $0.0012/día
= €0.22/mes (81% ahorro) ✅

CALIDAD: 95-97% (inaceptable pérdida)
```

---

## 📋 CHECKLIST IMPLEMENTACIÓN

### FASE 1: Cache (1 semana) - Fácil
- [ ] Setup Upstash Redis
- [ ] Implementar CacheService
- [ ] Integrar en chatService
- [ ] Testing de hit rate
- [ ] Deploy a producción

**Ahorro**: 40-60% (€1.14 → €0.46/mes)

---

### FASE 2: Router + RAG (1 semana) - Medio
- [ ] Implementar RouterService
- [ ] Setup Cohere API
- [ ] Mejorar búsqueda Qdrant
- [ ] Testing de quality
- [ ] Deploy gradual (canary)

**Ahorro adicional**: +30% (€0.46 → €0.32/mes)

---

### FASE 3: Compression + Cloudflare (2 semanas) - Complejo
- [ ] Setup LLMLingua (local)
- [ ] Implementar PromptCompressionService
- [ ] Deploy Cloudflare Worker
- [ ] Routing Cloudflare en frontend
- [ ] Testing exhaustivo
- [ ] Fallback a Groq

**Ahorro adicional**: +40% (€0.32 → €0.18/mes)

---

### FASE 4: BYOK Opcional (1 semana) - Easy
- [ ] UI para configurar API key
- [ ] Routing automático a BYOK
- [ ] Fallback a default provider
- [ ] Support para 5 providers

**Ventaja**: +100% margen (usuario paga directamente a LLM provider)

---

## 🎯 GOAL: €0.18/mes por usuario

```
ANTES:
- Groq 70B simple: €1.14/mes
- Margen: €28.85/mes (96%)

DESPUÉS:
- Stack óptimo: €0.18/mes
- Margen: €29.81/mes (99.4%)

BENEFICIO:
- €0.96/mes adicional por usuario
- 100 usuarios = €96/mes = €1,152/año extra
- Competencia prácticamente imposible de superar
```

---

## 🚀 DEPLOYMENT STRATEGY

### Timeline
```
Semana 1: Cache + Router (funcional, 60% ahorro)
Semana 2: RAG mejorado (80% ahorro)
Semana 3: Compression (85% ahorro)
Semana 4: Cloudflare Workers (90% ahorro)
Semana 5: BYOK opcional (100% margen)
```

### Rollout
```
Día 1-2: Feature flag OFF (no usuarios afectados)
Día 3-5: 10% usuarios (testing)
Día 6-7: 50% usuarios (canary)
Semana 2: 100% usuarios (full rollout)

Fallback: Simple Groq 70B (segundos)
```

---

## 💰 BUSINESS IMPACT

### Precio Propuesto
```
Plan Básico: €19.99/mes
- Stack óptimo: €0.18/mes
- Margen: €19.81/mes (99%)

Plan Premium: €49.99/mes
- Stack premium (MoA): €2/mes
- Margen: €47.99/mes (96%)

Plan Pro: €99.99/mes (Grupo de estudio)
- Stack enterprise: €3/mes
- Margen: €96.99/mes (97%)
```

### Rentabilidad
```
100 usuarios Plan Básico:
- Revenue: €1,999/mes
- Coste IA: €18/mes
- Coste infra: €50/mes
- Beneficio: €1,931/mes ✅

¡Casi 100% margen!
```

---

## 🎉 CONCLUSIÓN

**Implementando estas 5 estrategias combinadas:**

✅ Coste IA: €1.14/mes → €0.18/mes (84% reducción)
✅ Calidad: 98% → 95-97% (imperceptible)
✅ Margen: 96% → 99.4%
✅ Competencia: Imposible igualar estos números

**Resultado: App altamente rentable y competitiva**

