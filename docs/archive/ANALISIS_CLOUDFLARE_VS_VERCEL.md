# 🔍 Análisis: Cloudflare vs Vercel para OpositaIA

**Fecha:** 24 Nov 2025  
**Contexto:** Evaluación de plataformas para producción

---

## 📊 Comparativa Técnica

### Cloudflare Workers

**✅ Ventajas:**
- **Edge Computing** - Latencia ultra-baja (50ms global)
- **Free Tier generoso** - 100,000 req/día gratis
- **Durable Objects** - Estado persistente en edge
- **Workers KV** - Key-value storage gratis
- **R2 Storage** - Almacenamiento S3-compatible sin egress fees
- **Tunnel** - HTTPS gratis + protección IP del VPS
- **DDoS Protection** - Incluido gratis
- **Analytics** - Incluido gratis
- **WebSockets** - Soporte nativo

**❌ Desventajas:**
- **Límite de CPU** - 10ms por request (puede ser poco)
- **Cold starts** - Aunque mínimos
- **Vendor lock-in** - Código específico de Workers
- **Debugging** - Más complejo que servidor tradicional
- **PostgreSQL** - Necesita Hyperdrive (€5/mes) o externo

---

### Vercel

**✅ Ventajas:**
- **Next.js optimizado** - Si usas React/Next
- **Vercel Postgres** - PostgreSQL integrado (gratis hasta 256MB)
- **Edge Functions** - Similar a Workers
- **Serverless Functions** - Node.js completo (no límite 10ms)
- **Preview Deployments** - Por cada PR
- **Analytics** - Incluido
- **Zero config** - Deploy automático desde Git

**❌ Desventajas:**
- **Free Tier limitado** - 100GB bandwidth/mes
- **Funciones** - 10s timeout (vs ilimitado en Workers)
- **Egress fees** - Después del free tier
- **No DDoS protection** - Necesitas Cloudflare delante
- **No Tunnel** - VPS queda expuesto

---

## 🎯 Recomendación para OpositaIA

### **Opción Híbrida (MEJOR)** ⭐⭐⭐⭐⭐

```
Frontend: Vercel (React/Vite)
Backend: VPS con FastAPI (ya tienes)
Protección: Cloudflare Tunnel (gratis)
Database: PostgreSQL Docker local → Vercel Postgres en producción
Vectorial: Qdrant Cloud (ya migrado)
```

**Por qué:**
1. ✅ **Aprovechas tu VPS** - Ya lo tienes pagado
2. ✅ **FastAPI completo** - Sin límites de CPU/tiempo
3. ✅ **Cloudflare Tunnel** - Protege VPS + HTTPS gratis
4. ✅ **Vercel para frontend** - Deploy automático
5. ✅ **PostgreSQL flexible** - Local dev, Vercel prod

---

## 💰 Costes Comparados

### Opción 1: Todo en Cloudflare Workers
```
Cloudflare Workers: €0 (< 100K req/día)
Hyperdrive (PostgreSQL): €5/mes
R2 Storage: €0 (< 10GB)
TOTAL: €5/mes
```

### Opción 2: Todo en Vercel
```
Vercel Hobby: €0 (< 100GB bandwidth)
Vercel Postgres: €0 (< 256MB)
TOTAL: €0/mes (pero sin DDoS protection)
```

### Opción 3: Híbrida (RECOMENDADA)
```
VPS: €0 (ya pagado)
Cloudflare Tunnel: €0 (gratis)
Vercel Frontend: €0 (< 100GB)
Vercel Postgres: €0 (< 256MB)
Qdrant Cloud: €0 (< 1GB)
TOTAL: €0/mes
```

---

## 🚀 Plan de Implementación Recomendado

### Fase 1: Cloudflare Tunnel (1 hora)
```bash
# Instalar cloudflared en VPS
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/

# Autenticar
cloudflared tunnel login

# Crear túnel
cloudflared tunnel create opositaia-backend

# Configurar
cat > ~/.cloudflared/config.yml << EOF
tunnel: <UUID>
credentials-file: /root/.cloudflared/<UUID>.json

ingress:
  - hostname: api.opositaia.com
    service: http://localhost:8000
  - service: http_status:404
EOF

# Ejecutar
cloudflared tunnel run opositaia-backend
```

**Resultado:**
- ✅ VPS protegido (IP oculta)
- ✅ HTTPS automático
- ✅ DDoS protection
- ✅ €0 coste

### Fase 2: Frontend en Vercel (30 min)
```bash
# Conectar repo a Vercel
vercel link

# Configurar env vars
vercel env add VITE_BACKEND_URL
# Valor: https://api.opositaia.com

# Deploy
vercel --prod
```

**Resultado:**
- ✅ Frontend en CDN global
- ✅ Deploy automático por Git
- ✅ Preview deployments
- ✅ €0 coste

### Fase 3: Migrar PostgreSQL a Vercel (1 hora)
```bash
# Crear Vercel Postgres
vercel postgres create opositaia-db

# Obtener DATABASE_URL
vercel env pull

# Migrar datos
pg_dump -h localhost -U postgres opositaia > backup.sql
psql $DATABASE_URL < backup.sql

# Actualizar .env.backend en VPS
DATABASE_URL=<vercel-postgres-url>
```

**Resultado:**
- ✅ PostgreSQL en la nube
- ✅ Backups automáticos
- ✅ €0 coste (< 256MB)

---

## 🎯 Decisión Final

### **Usar Cloudflare Tunnel + Vercel** ✅

**Razones:**
1. **Mejor de ambos mundos**
   - Cloudflare: Protección + Tunnel
   - Vercel: Frontend + PostgreSQL
   - VPS: Backend FastAPI completo

2. **Coste: €0/mes**
   - Todo en free tiers
   - Sin límites artificiales
   - Escalable hasta 100 usuarios

3. **Flexibilidad**
   - FastAPI sin restricciones
   - PostgreSQL real (no Hyperdrive)
   - Fácil debugging

4. **Seguridad**
   - DDoS protection (Cloudflare)
   - IP VPS oculta (Tunnel)
   - HTTPS automático

---

## ❌ Por qué NO migrar todo a Cloudflare Workers

1. **Límite de CPU (10ms)** - Tu RAG puede tardar más
2. **Vendor lock-in** - Código específico de Workers
3. **PostgreSQL caro** - Hyperdrive €5/mes vs Vercel gratis
4. **Ya tienes VPS** - Desperdicio no usarlo
5. **Debugging complejo** - Workers es más difícil

---

## ✅ Conclusión

**Implementa la Opción Híbrida:**

```
┌─────────────────────────────────────────┐
│         Usuario (Navegador)             │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│      Vercel (Frontend React/Vite)       │
│              opositaia.com              │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│    Cloudflare Tunnel (Protección)       │
│         api.opositaia.com               │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│      VPS (FastAPI Backend)              │
│         147.93.95.67:8000               │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  PostgreSQL (local dev)         │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│      Vercel Postgres (producción)       │
└─────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│         Qdrant Cloud (RAG)              │
└─────────────────────────────────────────┘
```

**Próximo paso:** Implementar Cloudflare Tunnel (1 hora)

---

**Fecha de decisión:** 24 Nov 2025  
**Revisión:** Cada 3 meses o al alcanzar 100 usuarios
