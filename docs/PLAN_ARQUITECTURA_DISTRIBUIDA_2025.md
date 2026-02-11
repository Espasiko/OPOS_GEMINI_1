# 🌍 Plan Maestro: Arquitectura Distribuida "Genial" 2025

**Objetivo:** Sistema de Producción 100% en Nube. Cero dependencia del Portátil Local.
**Filosofía:** "El Portátil solo mira, no trabaja."

---

## 🏗️ La Topología (El "Cuerpo" Digital)

Hemos dividido el sistema en órganos especializados que viven donde mejor funcionan (y más barato salen):

### 1. 🧠 El Cerebro (VPS Hostinger - 8GB RAM)
*   **Rol:** Pensamiento Pesado & Lógica Privada.
*   **Componentes:**
    *   **Ollama + Salamandra-Opos (Q4):** El modelo customizado.
    *   **Opositor-API (FastAPI):** El orquestador que "habla" con el LLM y protege la lógica.
    *   **Nginx:** El portero que protege la API.
*   **Ventaja:** Aprovechamos el hardware ya pagado para lo más caro (GPU/CPU Inference).

### 2. 😊 La Cara (Vercel Global Edge)
*   **Rol:** Interfaz de Usuario & Velocidad Extrema.
*   **Componentes:**
    *   **Next.js 14 (App Router):** Tu Landing Page y la App de Chat.
    *   **Vercel Hosting (Free Tier):** CDN Global, SSL Automático, Anti-DDoS.
*   **Por qué Vercel:** Es gratis para proyectos personales/pro, despliegue con `git push`, y velocidad imbatible.

### 3. 🛡️ La Identidad & Datos (Supabase Cloud)
*   **Rol:** Usuarios, Sesiones y Datos Estructurados.
*   **Componentes:**
    *   **Auth:** Login con Google/Email (Adiós a programar sistemas de login inseguros).
    *   **PostgreSQL (DB):** Guarda perfiles, histrórico de chats y (importante) los artículos de leyes completos.
*   **Por qué Supabase:** Free Tier generoso (500MB DB), API instantánea, Panel de administración visual brutal.

### 4. 📚 La Memoria Rápida (Qdrant Cloud)
*   **Rol:** Búsqueda Vectorial (RAG).
*   **Componentes:**
    *   **Cluster Qdrant (Free Tier):** 1GB de vectores.
*   **Por qué Cloud:** Al sacarlo del VPS, liberamos RAM para Salamandra y permitimos que la API consulte la memoria sin latencia interna.

### 5. 💰 La Caja (Stripe)
*   **Rol:** Cobrar.
*   **Integración:** Directa en la Landing Page de Vercel. "Paga para desbloquear Chat Ilimitado".

---

## 🚦 Flujo de Datos (El "Sistema Nervioso")

1.  **Usuario** entra a `opositaia.com` (Vercel).
2.  **Se Loguea** con Supabase Auth (Vercel habla con Supabase).
3.  **Compra Suscripción** (Vercel habla con Stripe → Stripe actualiza Supabase).
4.  **Chatea:**
    *   Frontend (Vercel) envía mensaje a API (VPS).
    *   API (VPS) valida usuario con Supabase (Token Check).
    *   API (VPS) busca contexto en Qdrant Cloud.
    *   API (VPS) piensa con Salamandra (Localhost VPS).
    *   API (VPS) responde al Frontend.

**Resultado:** Tu portátil está apagado. El sistema vuela. Dinero entra.

---

## 📋 Plan de Migración (Paso a Paso)

### Fase A: La Base de Datos (Supabase)
1.  Crear Proyecto Supabase (Free).
2.  Migrar esquema SQL actual (`laws`, `users`) a Supabase.
3.  Configurar Auth (Google/Email).

### Fase B: La Memoria (Qdrant)
1.  Crear Cluster Qdrant Cloud (Free).
2.  **Script de Migración:** Subir tus datasets (JSON/Qdrant Local) a la nube. *Este es el único paso que harás desde tu PC una vez.*

### Fase C: El Cerebro (VPS)
1.  Actualizar API para que apunte a Supabase (DB) y Qdrant Cloud (Vectores).
2.  Borrar Qdrant local y Postgres local del VPS (¡Más RAM para Salamandra!).

### Fase D: La Cara (Vercel)
1.  Crear Repo GitHub limpio para Frontend.
2.  Desplegar Next.js Landing Page con botón de Login.
3.  Conectar Vercel con API VPS (`https://electroyhogarpelotazo.tienda`).

---

## 🧪 Pruebas de Estrés
Una vez montado, usaremos herramientas de carga (k6) para simular 100 usuarios a la vez y ver si el VPS aguanta o si hay que escalar el "Cerebro".

