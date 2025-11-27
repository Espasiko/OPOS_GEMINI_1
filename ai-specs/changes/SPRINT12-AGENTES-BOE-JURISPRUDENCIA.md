# 🚀 SPRINT 12 - Agentes BOE + Jurisprudencia

**Fecha Inicio**: 9 Diciembre 2025  
**Sprint**: 12 - Agentes Externos  
**Duración**: 1 semana  
**Estado**: 📋 **PLANIFICADO**

---

## 🎯 OBJETIVO

Implementar agentes para verificar información en BOE y buscar jurisprudencia relevante.

---

## 📋 PLAN DE EJECUCIÓN

### FASE 1: Cliente API BOE (Día 1-2)

```typescript
// src/agents/boe-agent.ts
export class BOEAgent {
  private baseURL = 'https://www.boe.es/datosabiertos/api';
  
  async search(query: string, fechaDesde?: string, fechaHasta?: string) {
    const params = new URLSearchParams({
      texto: query,
      ...(fechaDesde && { fecha_desde: fechaDesde }),
      ...(fechaHasta && { fecha_hasta: fechaHasta }),
    });
    
    const response = await fetch(`${this.baseURL}/boe/buscar?${params}`);
    return await response.json();
  }
  
  async getSumario(fecha: string) {
    const response = await fetch(`${this.baseURL}/boe/sumario/${fecha}`);
    return await response.json();
  }
  
  async checkUpdates(area: string = 'seguridad_social', days: number = 7) {
    const fechaHasta = new Date().toISOString().split('T')[0].replace(/-/g, '');
    const fechaDesde = new Date(Date.now() - days * 24 * 60 * 60 * 1000)
      .toISOString().split('T')[0].replace(/-/g, '');
    
    return await this.search(area, fechaDesde, fechaHasta);
  }
}
```

### FASE 2: Scraper Jurisprudencia (Día 2-3)

```typescript
// src/agents/jurisprudencia-agent.ts
export class JurisprudenciaAgent {
  private baseURL = 'https://www.poderjudicial.es/search/indexAN.jsp';
  
  async search(query: string, area: string = 'seguridad_social') {
    const params = new URLSearchParams({
      q: `${query} ${area}`,
      site: 'PoderJudicial',
      client: 'PoderJudicial_frontend',
      output: 'xml_no_dtd',
    });
    
    const response = await fetch(`${this.baseURL}?${params}`);
    const html = await response.text();
    
    // Parse HTML (simple)
    return this.parseResults(html);
  }
  
  private parseResults(html: string) {
    // Extraer resultados básicos
    // En producción, usar librería de parsing
    const results = [];
    // ... parsing logic
    return results;
  }
}
```

### FASE 3: Indexar en Qdrant (Día 3-4)

```typescript
// src/agents/jurisprudencia-indexer.ts
export class JurisprudenciaIndexer {
  constructor(
    private qdrant: QdrantClient,
    private embedder: EmbeddingService
  ) {}
  
  async indexSentencias(temas: string[]) {
    for (const tema of temas) {
      const sentencias = await this.jurisprudenciaAgent.search(tema);
      
      for (const sentencia of sentencias) {
        const embedding = await this.embedder.generate(sentencia.resumen);
        
        await this.qdrant.upsert('jurisprudencia_seguridad_social', {
          points: [{
            id: sentencia.id,
            vector: embedding,
            payload: {
              titulo: sentencia.titulo,
              url: sentencia.url,
              resumen: sentencia.resumen,
              fecha: sentencia.fecha,
              tema,
              tipo: 'sentencia',
            },
          }],
        });
      }
      
      await sleep(2000); // Rate limiting
    }
  }
}
```

### FASE 4: Integrar en MCP (Día 4-5)

```typescript
// src/mcp/tools.ts
server.setRequestHandler('tools/call', async (request) => {
  // BOE Search
  if (request.params.name === 'boe_search') {
    const { query, fecha_desde, fecha_hasta } = request.params.arguments;
    const boeAgent = new BOEAgent();
    const results = await boeAgent.search(query, fecha_desde, fecha_hasta);
    
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(results, null, 2),
      }],
    };
  }
  
  // BOE Check Updates
  if (request.params.name === 'boe_check_updates') {
    const { area, days } = request.params.arguments;
    const boeAgent = new BOEAgent();
    const updates = await boeAgent.checkUpdates(area, days);
    
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(updates, null, 2),
      }],
    };
  }
  
  // Jurisprudencia Search
  if (request.params.name === 'jurisprudencia_search') {
    const { query, area } = request.params.arguments;
    const jurisprudenciaAgent = new JurisprudenciaAgent();
    const results = await jurisprudenciaAgent.search(query, area);
    
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(results, null, 2),
      }],
    };
  }
});
```

### FASE 5: Automatización (Día 5-7)

```typescript
// src/cron/update-boe.ts
export async function updateBOE(env: Env) {
  const boeAgent = new BOEAgent();
  const updates = await boeAgent.checkUpdates('seguridad_social', 1);
  
  if (updates.length > 0) {
    // Notificar usuarios
    await notifyUsers(updates);
    
    // Indexar en Qdrant si es relevante
    for (const update of updates) {
      if (isRelevant(update)) {
        await indexDocument(update);
      }
    }
  }
}

// Configurar en wrangler.toml
// [triggers]
// crons = ["0 9 * * *"]  # Diario a las 9am
```

---

## 📊 MÉTRICAS DE ÉXITO

- [ ] API BOE integrada
- [ ] Scraper jurisprudencia funcionando
- [ ] Sentencias indexadas en Qdrant
- [ ] MCP tools expuestos
- [ ] Cron job configurado
- [ ] Tests E2E pasando

---

## ⏱️ TIMELINE

**Total**: 1 semana (5 días)

---

## 🚀 PRÓXIMO SPRINT

**Sprint 13**: Landing Page + Stripe

---

**Prerequisitos**: Sprint 11 completado ✅
