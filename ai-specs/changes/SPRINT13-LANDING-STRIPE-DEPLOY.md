# 🚀 SPRINT 13 - Landing Page + Stripe + Deploy

**Fecha Inicio**: 16 Diciembre 2025  
**Sprint**: 13 - Comercialización  
**Duración**: 1 semana  
**Estado**: 📋 **PLANIFICADO**

---

## 🎯 OBJETIVO

Crear landing page, integrar pagos con Stripe, y desplegar en Vercel.

---

## 📋 PLAN DE EJECUCIÓN

### FASE 1: Landing Page (Día 1-2)

#### 1.1 Crear Proyecto Next.js
```bash
npx create-next-app@latest opositaia-landing --typescript --tailwind --app
cd opositaia-landing
```

#### 1.2 Estructura
```
opositaia-landing/
├── app/
│   ├── page.tsx              # Home
│   ├── pricing/page.tsx      # Precios
│   ├── privacy/page.tsx      # Privacidad
│   ├── terms/page.tsx        # Términos
│   └── api/
│       └── stripe-webhook/route.ts
├── components/
│   ├── Hero.tsx
│   ├── Features.tsx
│   ├── Pricing.tsx
│   ├── CTA.tsx
│   └── Footer.tsx
└── lib/
    └── stripe.ts
```

#### 1.3 Hero Section
```typescript
// components/Hero.tsx
export function Hero() {
  return (
    <section className="py-20 px-4">
      <div className="max-w-6xl mx-auto text-center">
        <h1 className="text-5xl font-bold mb-6">
          Prepara tus Oposiciones de Seguridad Social con IA
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Resúmenes, esquemas, flashcards y más. Todo generado con IA.
        </p>
        <div className="flex gap-4 justify-center">
          <a href="/pricing" className="btn-primary">
            Empezar Gratis
          </a>
          <a href="#features" className="btn-secondary">
            Ver Características
          </a>
        </div>
      </div>
    </section>
  );
}
```

#### 1.4 Pricing Section
```typescript
// components/Pricing.tsx
export function Pricing() {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl font-bold text-center mb-12">Precios</h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          {/* Free */}
          <div className="card">
            <h3>Gratis</h3>
            <p className="text-3xl font-bold">€0<span className="text-sm">/mes</span></p>
            <ul>
              <li>✅ 10 consultas/día</li>
              <li>✅ Resúmenes básicos</li>
              <li>✅ Acceso a leyes</li>
            </ul>
            <button>Empezar</button>
          </div>
          
          {/* Pro */}
          <div className="card featured">
            <h3>Pro</h3>
            <p className="text-3xl font-bold">€29.99<span className="text-sm">/mes</span></p>
            <ul>
              <li>✅ Consultas ilimitadas</li>
              <li>✅ Todas las herramientas</li>
              <li>✅ Verificación BOE</li>
              <li>✅ Jurisprudencia</li>
              <li>✅ Soporte prioritario</li>
            </ul>
            <a href="/api/checkout">Suscribirse</a>
          </div>
          
          {/* Enterprise */}
          <div className="card">
            <h3>Academias</h3>
            <p className="text-3xl font-bold">Personalizado</p>
            <ul>
              <li>✅ Todo de Pro</li>
              <li>✅ Usuarios ilimitados</li>
              <li>✅ Personalización</li>
              <li>✅ Soporte dedicado</li>
            </ul>
            <button>Contactar</button>
          </div>
        </div>
      </div>
    </section>
  );
}
```

---

### FASE 2: Integración Stripe (Día 2-3)

#### 2.1 Setup Stripe
```bash
npm install stripe @stripe/stripe-js
```

#### 2.2 Crear Productos en Stripe Dashboard
```
1. Ir a https://dashboard.stripe.com/products
2. Crear producto "OpositAIA Pro"
3. Precio: €29.99/mes recurrente
4. Copiar Price ID
```

#### 2.3 Checkout API
```typescript
// app/api/checkout/route.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const { priceId } = await req.json();
  
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{
      price: priceId,
      quantity: 1,
    }],
    mode: 'subscription',
    success_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
    customer_email: req.headers.get('x-user-email') || undefined,
  });
  
  return Response.json({ url: session.url });
}
```

#### 2.4 Webhook Handler
```typescript
// app/api/stripe-webhook/route.ts
import { headers } from 'next/headers';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get('stripe-signature')!;
  
  let event: Stripe.Event;
  
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    return Response.json({ error: 'Invalid signature' }, { status: 400 });
  }
  
  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object as Stripe.Checkout.Session;
      // Activar cuenta del usuario
      await activateSubscription(session.customer as string);
      break;
      
    case 'customer.subscription.deleted':
      const subscription = event.data.object as Stripe.Subscription;
      // Desactivar cuenta
      await deactivateSubscription(subscription.customer as string);
      break;
  }
  
  return Response.json({ received: true });
}
```

---

### FASE 3: Deploy en Vercel (Día 3-4)

#### 3.1 Configurar Vercel
```bash
# Instalar CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Producción
vercel --prod
```

#### 3.2 Variables de Entorno
```bash
# En Vercel Dashboard
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
NEXT_PUBLIC_URL=https://opositaia.com
```

#### 3.3 Configurar Dominio
```
1. Ir a Vercel Dashboard
2. Settings > Domains
3. Agregar opositaia.com
4. Configurar DNS según instrucciones
```

---

### FASE 4: Deploy App Principal (Día 4-5)

#### 4.1 Preparar App React
```bash
cd tu-app-react
npm run build
```

#### 4.2 Deploy en Vercel
```bash
vercel

# Configurar variables
vercel env add VITE_API_URL
# https://opositaia-backend.tu-usuario.workers.dev

vercel --prod
```

#### 4.3 Configurar Subdominios
```
Landing: opositaia.com
App: app.opositaia.com
API: api.opositaia.com (Cloudflare Worker)
```

---

### FASE 5: Testing E2E (Día 5)

#### 5.1 Test Flujo Completo
```
1. Usuario visita opositaia.com
2. Ve pricing
3. Click "Suscribirse"
4. Paga con Stripe (test mode)
5. Redirige a app.opositaia.com
6. Login con Auth0
7. Acceso completo a features
```

#### 5.2 Test Webhook
```bash
# Usar Stripe CLI
stripe listen --forward-to localhost:3000/api/stripe-webhook

# Trigger evento
stripe trigger checkout.session.completed
```

---

## 📊 MÉTRICAS DE ÉXITO

- [ ] Landing desplegada en opositaia.com
- [ ] App desplegada en app.opositaia.com
- [ ] Stripe funcionando (test mode)
- [ ] Webhooks configurados
- [ ] Flujo completo de pago funciona
- [ ] SSL configurado
- [ ] Analytics configurado

---

## 💰 COSTES

**Vercel**: €0/mes (Hobby tier)  
**Stripe**: €0 setup, 1.5% + €0.25 por transacción  
**Dominio**: €12/año  

**Total mensual**: €1/mes

---

## ⏱️ TIMELINE

**Total**: 1 semana (5 días)

---

## 🚀 PRÓXIMO SPRINT

**Sprint 14**: Legal (GDPR + Plantillas)

---

**Prerequisitos**: Sprint 12 completado ✅
