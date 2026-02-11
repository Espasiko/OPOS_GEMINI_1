# 🏗️ RESPUESTAS Y DECISIONES DE ARQUITECTURA (04/01/2026)

Aquí tienes las respuestas técnicas detalladas y evaluaciones para tus decisiones, mientras la ingesta de datos (17k chunks) sigue su curso.

## 1. 🏭 FACTORY vs. CHAT RÁPIDO
> **Decisión Usuario:** "Factoría mejor, podemos crear agente chat aparte uno para rapidez... pero la factoria SE DEBE HACER!"

**ANÁLISIS TÉCNICO:**
Es la arquitectura correcta. Separamos los flujos por "Velocidad de Pensamiento":

*   **Agente "Factory" (Slow Thinking):**
    *   **Uso:** Crear temarios, exámenes completos, resúmenes profundos.
    *   **Verificación:** **EXTREMA**. 3 Capas (Planificador -> Escritor -> Validador Legal). El Validador comprueba cada artículo citado contra la BD vectorial.
    *   **Tiempo:** Minutos.

*   **Agente "Chat Rápido" (Fast Thinking):**
    *   **Uso:** Dudas puntuales ("¿Plazo recurso alzada?").
    *   **¿Está Verificado?** **SÍ, pero diferente.**
        *   No hay un "Validador" humanoide separado.
        *   La verificación es **intrínseca al RAG**: El sistema te muestra las **CITAS** (Fuentes) de donde sacó la respuesta.
        *   **Garantía:** Si el RAG recupera el artículo correcto del BOE (que ahora tenemos 100% ingestado), la respuesta será correcta. El usuario verifica leyendo la fuente citada.

---

## 2. ⚡ CLOUDFLARE WORKERS (Backend)
> **Pregunta Usuario:** "¿Migrar backend? necesito discutirlo... cuanto espacio ocuparia en el vps en terminos de memoria y ram?"

**EVALUACIÓN DE IMPACTO (VPS vs. WORKERS):**

Esta es la clave: **Migrar a Cloudflare Workers AHORRA RAM en tu VPS.**

*   **ESCENARIO A (Actual - VPS Todo en Uno):**
    *   Tu VPS ejecuta: LLM (Cerebro) + Base de Datos + **Backend API (Python/FastAPI)**.
    *   El Backend API consume ~300-500MB de RAM solo por estar encendido esperando peticiones.
    *   **RAM Disponible para LLM:** Menos.

*   **ESCENARIO B (Propuesto - Workers):**
    *   El Backend (lógica de negocio, autenticación, llamar a la BD, router) se mueve a la red de Cloudflare.
    *   **Consumo en TU VPS:** **0 MB**.
    *   Tu VPS solo ejecuta el LLM (Ollama) y quizás Qdrant.
    *   **RAM Disponible para LLM:** **MÁXIMA**.
    *   **Coste:** Gratis (hasta 100k peticiones/día).

**Veredicto:** Si tu cuello de botella es la RAM del VPS para correr modelos más listos, Cloudflare Workers es la mejor inversión técnica.

---

## 3. 📱 BASE DE DATOS LOCAL (SQLite/IndexedDB)
> **Decisión Usuario:** "Vamos a informar y desidir segun investigacion!!"

**PLAN DE INVESTIGACIÓN (Fase 2):**
Lo que evaluaremos antes de implementar:
1.  **Sincronización:** ¿Qué pasa si usas el móvil y luego el PC? SQLite local en navegador **NO** sincroniza entre dispositivos automáticamente. Necesitaríamos un "Sync Server" (complejo).
2.  **Alternativa PWA:** Quizás `TanStack Query` (cache inteligente en frontend) sea suficiente sin montar una BD local completa.
3.  **Veredicto Preliminar:** Para un MVP (Producto Mínimo Viable), mejor usar **PostgreSQL Central (Supabase o VPS)**. Es más simple y garantiza que tus datos están en todos tus dispositivos. Investigaremos "Local-First" para la versión 2.0.

---

## 4. 🧠 FEEDBACK LOOP & MEMORIA
> **Pregunta Usuario:** "Para que el modelo reaprenda... y en el chat, que no se pierda el hilo."

Aquí hay dos conceptos diferentes:

**A. Memoria de Conversación (El Hilo):**
*   **Problema:** Que el bot olvide lo que dijiste hace 3 mensajes.
*   **Solución:** Se usa **Redis** o una tabla SQL simple. Se guardan los últimos 10-20 mensajes y se envían de nuevo al LLM en cada nueva pregunta ("Context Window").
*   **Impacto VPS:** Mínimo (texto puro pesa KBs).

**B. "Reaprender" (Mejorar el modelo a largo plazo):**
*   **Mito:** El modelo se "entrena" en tiempo real mientras chateas. (Esto es carísimo y lento).
*   **Realidad (RAG Dinámico):**
    *   Cuando el usuario corrige al bot ("No, el plazo es 1 mes, no 15 días") y marca "**Feedback Positivo**".
    *   Guardamos ese par Pregunta-Respuesta Correcta en **Qdrant** (no solo PostgreSQL).
    *   La próxima vez, el RAG buscará en esa "Memoria de Correcciones" antes de mirar la Ley.
    *   **Impacto PostgreSQL:** Una tabla de texto. 1 millón de feedbacks ocuparían ~500MB. **Insignificante** para discos modernos.

---

## 5. 🌐 FALLBACK A FUENTES EXTERNAS (CRAG)
> **Pregunta Usuario:** "¿Que agente lo haria? ¿En que casos?"

**MECANISMO "CRAG" (Corrective RAG):**
1.  **Usuario:** "¿Cuál es la jurisprudencia sobre despidos nulos en 2025?"
2.  **Sistema:** Busca en Qdrant (Leyes + Sentencias ingestadas).
3.  **Evaluador (Mini-LLM):** Mira lo encontrado. Asigna nota de confianza (Score 0-100).
4.  **TRIGGER:** Si **Score < 60** (La información es pobre o vieja):
    *   **Agente Investigador (Buscador):** Se activa.
    *   Usa herramienta `search_web` (Google/Tavily).
    *   Busca en "boe.es", "poderjudicial.es".
    *   Descarga la info fresca.
    *   Responde al usuario Y (opcionalmente) guarda la info en Qdrant para el futuro.

---

## RESUMEN DE ACCIONES INMEDIATAS

1.  ✅ **Factory:** Procedemos con el diseño de 3 agentes (Planificador, Escritor, Validador).
2.  ✅ **Feedback:** Crearemos tabla `chat_history` y `feedback_logs` en PostgreSQL (coste espacio ~0).
3.  🔍 **Investigación:**
    *   Cloudflare Workers (Prioridad Media - Optimización RAM).
    *   Local DB (Prioridad Baja - Complejidad Sync).
