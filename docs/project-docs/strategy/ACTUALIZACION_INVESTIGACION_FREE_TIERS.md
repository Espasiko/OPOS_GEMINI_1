# 🆓 ACTUALIZACIÓN: FREE TIERS Y HERRAMIENTAS GRATUITAS

**Fecha**: 23 Noviembre 2025  
**Actualización de**: INVESTIGACION_PRODUCCION_Y_SEGURIDAD.md

---

## 🎉 BUENAS NOTICIAS

### 1. ✅ Ya tienes Qdrant Cloud
- Credenciales listas
- No necesitas migración manual
- **Ahorro**: 3 horas de trabajo

### 2. ✅ Ya tienes cuenta Cloudflare
- Workers ahora **GRATIS** (antes de pago)
- Durable Objects incluido en free tier
- **Ahorro**: €5-25/mes

### 3. ✅ Tu hija es abogada
- Consultoría legal gratis
- Solo necesitas plantillas base
- **Ahorro**: €500 en asesoría

---

## 🛠️ HERRAMIENTAS CLOUDFLARE

### Wrangler CLI (Oficial y Gratis)

**¿Qué es?**
- CLI oficial de Cloudflare
- Gestiona Workers desde terminal
- **NO necesitas copiar/pegar código en web**

**Instalación**:
```bash
npm install -g wrangler

# Login
wrangler login

# Crear proyecto
wrangler init opositaia-mcp
cd opositaia-mcp

# Desarrollar localmente
wrangler dev

# Deploy a producción
wrangler deploy
```

**Ventajas**:
- ✅ Desarrollo local
- ✅ Hot reload
- ✅ Deploy automático
- ✅ Gestión de secrets
- ✅ Logs en tiempo real

**No hay MCP específico de Cloudflare**, pero Wrangler es la herramienta oficial y es excelente.

---

## 🌐 DEPLOYMENT: VERCEL VS ALTERNATIVAS

### OPCIÓN A: Vercel (Recomendada para Frontend) ⭐⭐⭐⭐⭐

**Free Tier (Hobby)**:
```
✅ GRATIS PARA SIEMPRE

Incluye:
- Deployments ilimitados
- 100 GB bandwidth/mes
- Automatic CI/CD
- SSL automático
- CDN global
- Preview deployments
- Analytics básico

Límites:
- 1 usuario (tú)
- 100 GB bandwidth/mes (suficiente para 10K usuarios)
- 100 GB-hours serverless functions
```

**Cómo usar**:
```bash
# Instalar Vercel CLI
npm install -g vercel

# Deploy
cd tu-proyecto
vercel

# Producción
vercel --prod
```

**Integración con GitHub**:
- Push a main → Deploy automático
- Pull Request → Preview deployment
- Rollback con 1 click

### OPCIÓN B: Cloudflare Pages (Alternativa) ⭐⭐⭐⭐

**Free Tier**:
```
✅ GRATIS ILIMITADO

Incluye:
- Deployments ilimitados
- Bandwidth ilimitado
- 500 builds/mes
- SSL automático
- CDN global
```

**Ventaja**: Mismo ecosistema que Workers

### OPCIÓN C: Netlify (Alternativa) ⭐⭐⭐

**Free Tier**:
```
✅ GRATIS

Incluye:
- 100 GB bandwidth/mes
- 300 build minutes/mes
- SSL automático
```

### 🎯 RECOMENDACIÓN

**Frontend**: **Vercel** (mejor DX, más features)  
**Backend Workers**: **Cloudflare** (ya tienes cuenta)

**Arquitectura Final**:
```
Frontend (React) → Vercel
Backend (Workers) → Cloudflare
Database (Qdrant) → Qdrant Cloud
Payments (Stripe) → Stripe
```

---

## 💳 STRIPE: PAGOS

### Pricing Stripe España

**Sin costes fijos**:
- ✅ €0 setup
- ✅ €0 mensual
- ✅ Solo pagas por transacción

**Comisiones**:
```
Tarjetas EEA (España): 1.5% + €0.25 por transacción
Tarjetas UK: 2.5% + €0.25 por transacción
Tarjetas internacionales: 3.25% + €0.25 por transacción
```

**Ejemplo**:
```
Precio OpositAIA: €29.99/mes

Comisión Stripe: €0.70 (1.5% + €0.25)
Recibes: €29.29

Margen: 97.7%
```

### Implementación Stripe

**1. Stripe Checkout (Más fácil)**:
```typescript
// No necesitas frontend complejo
// Stripe proporciona página de pago

import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// Crear sesión de pago
const session = await stripe.checkout.sessions.create({
  payment_method_types: ['card'],
  line_items: [{
    price_data: {
      currency: 'eur',
      product_data: {
        name: 'OpositAIA Pro',
        description: 'Acceso mensual a OpositAIA',
      },
      unit_amount: 2999, // €29.99 en centavos
      recurring: {
        interval: 'month',
      },
    },
    quantity: 1,
  }],
  mode: 'subscription',
  success_url: 'https://opositaia.com/success',
  cancel_url: 'https://opositaia.com/cancel',
});

// Redirigir a Stripe
return redirect(session.url);
```

**2. Stripe Payment Links (Más fácil aún)**:
```
1. Crear producto en dashboard Stripe
2. Generar Payment Link
3. Compartir link: https://buy.stripe.com/xxx

✅ Sin código
✅ Listo en 5 minutos
```

### Webhooks para Suscripciones

```typescript
// pages/api/stripe-webhook.ts
import { buffer } from 'micro';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  const buf = await buffer(req);
  const sig = req.headers['stripe-signature'];

  let event;

  try {
    event = stripe.webhooks.constructEvent(
      buf,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Manejar eventos
  switch (event.type) {
    case 'checkout.session.completed':
      // Usuario pagó → Activar cuenta
      const session = event.data.object;
      await activateUserAccount(session.customer);
      break;
      
    case 'customer.subscription.deleted':
      // Suscripción cancelada → Desactivar cuenta
      const subscription = event.data.object;
      await deactivateUserAccount(subscription.customer);
      break;
  }

  res.json({ received: true });
}
```

---

## 📄 PLANTILLAS LEGALES GRATUITAS

### Generadores Gratuitos (Recomendados)

#### 1. **AEPD (Agencia Española de Protección de Datos)** ⭐⭐⭐⭐⭐

**URL**: https://www.aepd.es/es/documento/facilita-rgpd.pdf

**Qué ofrece**:
- ✅ Guía oficial GRATUITA
- ✅ Plantillas adaptadas a RGPD
- ✅ Específico para España
- ✅ Avalado por autoridad oficial

**Incluye**:
- Política de Privacidad
- Información básica
- Cláusulas de consentimiento
- Ejercicio de derechos

#### 2. **GetTerms.io** (Gratis con atribución)

**URL**: https://getterms.io/

**Qué ofrece**:
- ✅ Generador gratuito
- ✅ Política de Privacidad
- ✅ Términos y Condiciones
- ✅ Política de Cookies

**Limitación**: Incluye link "Generated by GetTerms.io" (puedes quitarlo pagando)

#### 3. **PrivacyPolicies.com** (Gratis básico)

**URL**: https://www.privacypolicies.com/

**Qué ofrece**:
- ✅ Generador básico gratis
- ✅ Descarga en HTML
- ✅ Actualizable

#### 4. **Plantilla Propia Personalizada** (Recomendado)

**Estrategia**:
1. Usar plantilla AEPD como base
2. Personalizar con tu hija (abogada)
3. Revisar puntos específicos de OpositAIA
4. **Coste**: €0

**Ventajas**:
- ✅ Totalmente gratis
- ✅ Adaptado a tu caso específico
- ✅ Revisado por abogada
- ✅ Sin dependencias externas

---

## 🎨 LANDING PAGE

### Opción 1: Vercel + Next.js (Recomendado)

**Template gratuito**:
```bash
npx create-next-app@latest opositaia-landing --example with-stripe

# Incluye:
- Landing page
- Integración Stripe
- Pricing page
- Dashboard básico
```

**Deploy**:
```bash
vercel
```

### Opción 2: Cloudflare Pages + Astro

**Template**:
```bash
npm create astro@latest opositaia-landing -- --template saas

# Deploy
wrangler pages deploy dist
```

### Opción 3: HTML Estático (Más simple)

**Estructura**:
```
landing/
├── index.html          # Home
├── pricing.html        # Precios
├── privacy.html        # Privacidad
├── terms.html          # Términos
├── styles.css          # Estilos
└── script.js           # JS mínimo
```

**Deploy en Vercel**:
```bash
vercel landing/
```

---

## 💰 COSTES ACTUALIZADOS

### Costes Iniciales

| Concepto | Antes | Ahora | Ahorro |
|----------|-------|-------|--------|
| Qdrant Cloud | Setup | ✅ Ya tienes | 3h trabajo |
| Cloudflare | Setup | ✅ Ya tienes | 1h trabajo |
| Plantillas Legales | €300 | **€0** | **€300** |
| Asesoría Legal | €500 | **€0** | **€500** |
| **TOTAL** | **€800** | **€0** | **€800** |

### Costes Mensuales

| Concepto | Coste/mes |
|----------|-----------|
| Qdrant Cloud | €0 (free tier) |
| Cloudflare Workers | €0 (free tier) |
| Vercel | €0 (hobby) |
| Stripe | €0 (solo comisiones) |
| Dominio | €1 |
| Email | €5 (Google Workspace) |
| **TOTAL** | **€6/mes** |

### Comisiones por Venta

```
Precio: €29.99/mes
Stripe: -€0.70 (2.3%)
Recibes: €29.29

100 usuarios = €2,929/mes
1,000 usuarios = €29,290/mes
```

---

## 🎯 PLAN ACTUALIZADO

### Tiempo de Implementación

**ANTES**: 10 semanas  
**AHORA**: **6 semanas** (40% más rápido)

**Reducción por**:
- ✅ Qdrant ya configurado (-1 semana)
- ✅ Cloudflare ya configurado (-1 semana)
- ✅ Plantillas legales gratis (-1 semana)
- ✅ Asesoría legal gratis (-1 semana)

### Nuevo Timeline

```
Semana 1-2: Cloudflare Workers + MCP
Semana 3: Agentes BOE + Jurisprudencia
Semana 4: Landing + Stripe
Semana 5: Legal (plantillas + revisión con tu hija)
Semana 6: Testing + Deploy

TOTAL: 6 semanas
COSTE: €0 inicial + €6/mes
```

---

## ✅ RESUMEN DE MEJORAS

### Lo que ya tienes
1. ✅ Qdrant Cloud configurado
2. ✅ Cuenta Cloudflare
3. ✅ Asesoría legal gratis (tu hija)

### Lo que usarás gratis
1. ✅ Wrangler CLI (Cloudflare)
2. ✅ Vercel Hobby (Frontend)
3. ✅ Stripe (sin costes fijos)
4. ✅ Plantillas AEPD (legales)

### Ahorro total
- **Inicial**: €800 → €0
- **Tiempo**: 10 semanas → 6 semanas
- **Mensual**: €6/mes (sin cambios)

---

## 🚀 PRÓXIMOS PASOS INMEDIATOS

1. **Hoy**:
   - [ ] Instalar Wrangler: `npm install -g wrangler`
   - [ ] Login Cloudflare: `wrangler login`
   - [ ] Instalar Vercel CLI: `npm install -g vercel`

2. **Esta semana**:
   - [ ] Crear primer Worker
   - [ ] Deploy landing en Vercel
   - [ ] Configurar Stripe

3. **Próxima semana**:
   - [ ] Implementar MCP Server
   - [ ] Integrar pagos
   - [ ] Plantillas legales con tu hija

¡Vamos mucho mejor! 🎉
