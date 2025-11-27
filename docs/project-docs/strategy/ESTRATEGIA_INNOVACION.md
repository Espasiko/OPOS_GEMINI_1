# 🚀 Estrategia de Innovación y Auditoría del Proyecto OpositaIA

**Fecha:** 25 Noviembre 2025
**Estado:** Planificación Estratégica
**Basado en:** BMad Innovation Strategy & Brownfield Guide

## 1. Correcciones Inmediatas (Realizadas)

### ✅ Fix `tsconfig.json`
Se ha corregido el error `Cannot find type definition file for 'node'`.
- **Causa:** Conflicto al especificar explícitamente `types: ["node"]` cuando ya estaba incluido en `package.json`.
- **Solución:** Se eliminó la línea conflictiva para permitir la resolución automática de tipos.

## 2. Estado de la Base de Datos (PostgreSQL Local)

### 🔍 Diagnóstico
- **Infraestructura:** El contenedor Docker `sim_old-db-1` (PostgreSQL) está corriendo en el puerto 5432.
- **Código Backend:**
    - Existe `backend/database/init_db.py` preparado para conectar y crear tablas.
    - Existe `backend/database/schema.sql` con la definición de tablas.
    - **PROBLEMA:** El archivo principal `backend/main.py` **NO** está importando ni inicializando la base de datos. Actualmente, la API funciona "en el aire" sin persistencia de historial.

### 🛠️ Acción Requerida (Para guardar historial)
Para guardar el historial del "único usuario" (tú), necesitamos:
1.  Conectar `main.py` con `init_db.py` en el arranque.
2.  Crear un endpoint/servicio que guarde cada interacción de chat en la tabla `chat_history` (definida en el schema).
3.  **Veredicto:** Sí, se puede y se debe usar la BD local del Docker para esto.

## 3. Estrategia de Innovación (Futuro del Desarrollo)

Basado en los workflows de BMad (`innovation-strategy`) y tus peticiones, aquí está la hoja de ruta para un código "funcional, eficiente y elegante":

### 🌟 Experiencia de Usuario (UI/UX) "Premium"

1.  **Modo "Examen Real" vs "Progreso":**
    -   Implementar un *toggle* global en el frontend.
    -   **Modo Progreso:** El agente tiene memoria infinita, te anima y adapta la dificultad.
    -   **Modo Examen:** El agente es estricto, sin pistas, tiempo limitado, simula presión.

2.  **Panel Lateral Colapsable:**
    -   Mejora crítica de UX para pantallas pequeñas o concentración total. Fácil de implementar con estado global en React (`isSidebarOpen`).

3.  **Vista Dividida (Split View) para Casos Prácticos:**
    -   **Esencial:** Panel izquierdo con el texto del caso (scroll independiente). Panel derecho con las preguntas/chat.
    -   Evita el "scroll de la muerte" de subir y bajar constantemente.

4.  **Burbuja de Chat Contextual (Fab Button):**
    -   Un botón flotante en las vistas de Test/Simulacro. Al pulsarlo, abre un mini-chat que *ya sabe* qué pregunta estás mirando (contexto inyectado) para resolver dudas puntuales sin salir del flujo.

### 🧠 Inteligencia Artificial Avanzada (Orquestación)

5.  **Sincronización de Agentes (Orquestador):**
    -   Usar un patrón **"Router-Solver"**. Un agente principal (Router) recibe tu *input* y decide qué sub-agente activar (Buscador, Jurista, Motivador).
    -   **Memoria Compartida:** Usar Redis o la misma Postgres para que lo que le digas al "Motivador" lo sepa el "Jurista" (ej: "estoy cansado hoy, dame leyes cortas").

6.  **RAG Completo + Web Search:**
    -   Integrar `Tavily` o `SerpApi` para búsquedas en tiempo real (BOE del día, noticias).
    -   **Hybrid Search:** Mezclar resultados de tu Qdrant (temario estático) con resultados web (novedades).

7.  **Gestión de Archivos y Enlaces:**
    -   El agente debe "ver" lo que subes. Al subir un PDF, se debe vectorizar al vuelo (en segundo plano) y añadir a una colección temporal "UserUploads" en Qdrant para consultarlo inmediatamente.

### 💰 Eficiencia y Control

8.  **Monitor de Tokens y Costes:**
    -   Crear un *middleware* en FastAPI que intercepte cada llamada a LLM.
    -   Calcular tokens (entrada/salida) y coste estimado según el modelo usado.
    -   Mostrar un "Ticker" discreto en el dashboard: "Coste sesión: $0.002".

9.  **Mistral API (Plan NYOK):**
    -   Integrar como opción "Low Cost / Free Tier" para tareas sencillas, reservando GPT-4/Gemini Pro para razonamiento complejo.

### 🛡️ Seguridad y DevOps

10. **Snyk Security Scanning:**
    -   Integrar Snyk en el pipeline de CI/CD (o pre-commit hook) para detectar vulnerabilidades en dependencias de Python y Node antes de que lleguen a producción.

11. **Cloudflare Workers + Durable Objects:**
    -   **Experimento:** Mover el "Estado de la Sesión" (chat history reciente) a un Durable Object. Esto reduce latencia brutalmente y quita carga a la BD principal.
    -   Ideal para la funcionalidad de "Burbuja de Chat" (respuestas instantáneas).

12. **Google Colab Fine-Tuning:**
    -   Usar Colab (GPU gratis/barata) para entrenar un adaptador (LoRA) de Llama-3 o Mistral con tus propios tests y casos prácticos. Luego, servir ese modelo "experto en Oposiciones" vía Ollama o Hugging Face.

---

## Próximos Pasos Recomendados

1.  **Activar Persistencia:** Conectar `main.py` a Postgres para empezar a guardar tu historial YA.
2.  **UI Split View:** Implementar la vista dividida para casos prácticos (mejora inmediata de calidad de vida).
3.  **Orquestador Básico:** Modificar el backend para que el Router decida si usar RAG, Web o Chat simple.
