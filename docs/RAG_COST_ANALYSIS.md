# 💰 Análisis de Costos - RAG Integration OpositaIA

## 🎯 Objetivo: Minimizar Costos, Maximizar Recursos Gratuitos

## 📊 Recursos Disponibles (GRATIS)

### 1. Infraestructura Local (WSL)
- ✅ **Docker**: Gratis, ya instalado
- ✅ **Ollama**: Gratis, corriendo
  - `tinyllama` (637 MB) - Embeddings rápidos
  - `all-minilm` (45 MB) - Embeddings ligeros
- ✅ **Qdrant**: Gratis (self-hosted), instalado
- ✅ **PostgreSQL + pgvector**: Gratis, corriendo

**Costo mensual**: $0

### 2. VPS Hostinger (Ya pagado)
- ✅ **Mistral 8B GGUF**: Ya instalado en `root@147.93.95.67`
- ✅ **SSH Access**: Disponible
- ✅ **Recursos**: Suficientes para Mistral 8B

**Costo mensual**: $0 (ya pagado)

### 3. API BOE (Datos Abiertos)
- ✅ **API Oficial BOE**: Sin API key, gratis
- ✅ **Endpoints disponibles**: 
  - `/diario/{fecha}/sumario`
  - `/buscar/doc`
  - `/datos/pdfs/{id}`
- ✅ **Sin límites de rate**: Uso razonable

**Costo mensual**: $0

### 4. GitHub (Free Tier)
- ✅ **GitHub Actions**: 2,000 minutos/mes gratis
- ✅ **GitHub Pages**: Hosting estático gratis
- ✅ **Private repos**: Ilimitados

**Costo mensual**: $0

## 💸 Servicios de Pago (Opcionales)

### 1. Google Gemini API
**Tier Gratuito**:
- ✅ 15 requests/minuto
- ✅ 1,500 requests/día
- ✅ 1 millón tokens/mes gratis

**Tier de Pago** (si excedes):
- Gemini 1.5 Flash: $0.075 / 1M tokens input
- Gemini 1.5 Pro: $1.25 / 1M tokens input

**Estimación para OpositaIA**:
- 100 usuarios/día × 10 requests = 1,000 requests/día
- Promedio 500 tokens/request = 500K tokens/día
- **Total mes**: 15M tokens = $1.13/mes (Flash)

**Costo mensual estimado**: $0 - $5 (dentro del free tier)

### 2. Hosting Backend (Opciones)

#### Opción A: Render.com (Recomendado)
**Free Tier**:
- ✅ 750 horas/mes gratis
- ✅ 512 MB RAM
- ✅ Sleep después de 15 min inactividad
- ❌ Lento al despertar (cold start)

**Starter Plan** ($7/mes):
- ✅ Siempre activo
- ✅ 512 MB RAM
- ✅ Sin cold starts

**Costo mensual**: $0 - $7

#### Opción B: Railway.app
**Free Tier**:
- ✅ $5 crédito/mes gratis
- ✅ Pay-as-you-go después

**Costo mensual**: $0 - $5

#### Opción C: Fly.io
**Free Tier**:
- ✅ 3 VMs pequeñas gratis
- ✅ 160 GB bandwidth/mes

**Costo mensual**: $0

#### Opción D: Self-hosted en VPS Hostinger (Ya pagado)
- ✅ Ya tienes el VPS
- ✅ Puedes correr FastAPI ahí
- ✅ Mistral 8B ya instalado

**Costo mensual**: $0 (ya pagado)

### 3. Qdrant Cloud (Opcional)

#### Free Tier:
- ✅ 1 GB storage
- ✅ 1M vectors
- ✅ Suficiente para empezar

#### Paid Tier ($25/mes):
- 10 GB storage
- 10M vectors
- Mejor performance

**Recomendación**: Usar Qdrant self-hosted (gratis) en WSL o VPS

**Costo mensual**: $0 (self-hosted)

### 4. Frontend Hosting

#### Opción A: Vercel (Recomendado)
**Free Tier**:
- ✅ 100 GB bandwidth/mes
- ✅ Builds ilimitados
- ✅ SSL gratis
- ✅ CDN global

**Costo mensual**: $0

#### Opción B: Netlify
**Free Tier**:
- ✅ 100 GB bandwidth/mes
- ✅ 300 build minutos/mes

**Costo mensual**: $0

#### Opción C: GitHub Pages
**Free Tier**:
- ✅ Hosting estático gratis
- ✅ SSL gratis
- ❌ Solo sitios estáticos

**Costo mensual**: $0

## 📊 Resumen de Costos

### Escenario 1: 100% Gratis (Recomendado para MVP)
```
Infraestructura:
- Ollama (local): $0
- Qdrant (local/VPS): $0
- Mistral 8B (VPS): $0
- PostgreSQL (local): $0

Backend:
- FastAPI en VPS Hostinger: $0 (ya pagado)
- O Render Free Tier: $0 (con cold starts)

Frontend:
- Vercel Free Tier: $0

APIs:
- BOE API: $0 (datos abiertos)
- Gemini API: $0 (dentro free tier)

GitHub Actions: $0 (2,000 min/mes)

TOTAL: $0/mes
```

### Escenario 2: Producción Básica (100-500 usuarios)
```
Infraestructura:
- Ollama (local): $0
- Qdrant (self-hosted VPS): $0
- Mistral 8B (VPS): $0

Backend:
- Render Starter: $7/mes
- O Railway: $5/mes

Frontend:
- Vercel Free: $0

APIs:
- BOE API: $0
- Gemini API: $5/mes (si excedes free tier)

TOTAL: $7-12/mes
```

### Escenario 3: Producción Escalada (1000+ usuarios)
```
Infraestructura:
- Ollama (local): $0
- Qdrant Cloud: $25/mes
- Mistral 8B (VPS): $0

Backend:
- Render Standard: $25/mes
- O Railway: $20/mes

Frontend:
- Vercel Pro: $20/mes (si excedes bandwidth)

APIs:
- BOE API: $0
- Gemini API: $20/mes

TOTAL: $65-90/mes
```

## 🎯 Recomendación: Arquitectura Híbrida Gratuita

### Fase 1: MVP (0-100 usuarios) - $0/mes
```
┌─────────────────────────────────────────────────┐
│         Frontend (Vercel Free)                  │
│         - React + TypeScript                    │
│         - $0/mes                                │
└────────────────┬────────────────────────────────┘
                 │
                 ├──────────────┬─────────────────┐
                 │              │                 │
         ┌───────▼──────┐  ┌───▼────┐     ┌─────▼─────┐
         │   Gemini     │  │ Ollama │     │  FastAPI  │
         │   (Free)     │  │ (WSL)  │     │   (VPS)   │
         │   $0/mes     │  │ $0/mes │     │   $0/mes  │
         └──────────────┘  └───┬────┘     └─────┬─────┘
                               │                 │
                          ┌────▼─────────────────▼────┐
                          │  Mistral 8B + Qdrant      │
                          │  (VPS Hostinger)          │
                          │  $0/mes (ya pagado)       │
                          └───────────────────────────┘
```

### Ventajas:
- ✅ **Costo total**: $0/mes
- ✅ **Escalable**: Puedes migrar componentes según crezcas
- ✅ **Flexible**: Múltiples proveedores de IA
- ✅ **Legal**: API BOE oficial, sin scraping

### Desventajas:
- ⚠️ Cold starts en Render Free (15 min inactividad)
- ⚠️ Latencia VPS → WSL (si están separados)
- ⚠️ Mantenimiento manual de infraestructura

## 🔧 Optimizaciones de Costo

### 1. Caché Inteligente
```python
# Cachear respuestas frecuentes
@lru_cache(maxsize=1000)
def get_boe_document(doc_id: str):
    # Reduce llamadas a API
    pass
```

### 2. Batch Processing
```python
# Procesar múltiples queries en un batch
async def batch_embed(texts: List[str]):
    # 1 llamada en lugar de N
    return await ollama.embed_batch(texts)
```

### 3. Rate Limiting
```python
# Limitar requests por usuario
@limiter.limit("10/minute")
async def search_endpoint():
    pass
```

### 4. Lazy Loading
```typescript
// Cargar componentes solo cuando se necesiten
const HeavyComponent = lazy(() => import('./Heavy'));
```

## 📈 Proyección de Costos

### Año 1 (0-1000 usuarios)
```
Mes 1-3 (MVP): $0/mes
Mes 4-6 (100 usuarios): $0-7/mes
Mes 7-9 (500 usuarios): $7-12/mes
Mes 10-12 (1000 usuarios): $12-25/mes

Total Año 1: ~$100-200
```

### Año 2 (1000-10000 usuarios)
```
Mes 1-6: $25-50/mes
Mes 7-12: $50-90/mes

Total Año 2: ~$450-840
```

## 🎓 Comparación con Competencia

### Competidor A (SaaS típico):
- Hosting: $50/mes
- Database: $25/mes
- APIs: $100/mes
- CDN: $20/mes
**Total**: $195/mes

### OpositaIA (Optimizado):
- Hosting: $0-7/mes
- Database: $0/mes (self-hosted)
- APIs: $0-5/mes (free tiers)
- CDN: $0/mes (Vercel)
**Total**: $0-12/mes

**Ahorro**: 94-100% 🎉

## ✅ Decisión Final: Arquitectura Recomendada

### Para MVP (Primeros 6 meses):
```yaml
Frontend:
  - Vercel Free Tier
  - Costo: $0/mes

Backend:
  - FastAPI en VPS Hostinger (ya pagado)
  - Costo: $0/mes

AI Models:
  - Gemini (free tier): Tareas complejas
  - Mistral 8B (VPS): Tareas medianas
  - Ollama (WSL): Embeddings
  - Costo: $0/mes

Vector DB:
  - Qdrant self-hosted (VPS o WSL)
  - Costo: $0/mes

Data Source:
  - BOE API oficial (datos abiertos)
  - Costo: $0/mes

CI/CD:
  - GitHub Actions (free tier)
  - Costo: $0/mes

TOTAL: $0/mes ✅
```

### Cuando escalar (>500 usuarios):
1. Migrar backend a Render Starter ($7/mes)
2. Considerar Qdrant Cloud ($25/mes)
3. Upgrade Gemini si excedes free tier ($5-20/mes)

**Total escalado**: $37-52/mes

## 🚀 Conclusión

**Podemos empezar con $0/mes** usando:
- ✅ VPS Hostinger (ya pagado) para Mistral + FastAPI
- ✅ WSL local para Ollama + Qdrant (desarrollo)
- ✅ Vercel Free para frontend
- ✅ Gemini Free Tier para IA cloud
- ✅ BOE API oficial (gratis)
- ✅ GitHub Actions (gratis)

**No nos estamos excediendo en costos** 🎉

---

**Última actualización**: 2025-01-16  
**Versión**: 1.0.0  
**Aprobado para implementación**: ✅
