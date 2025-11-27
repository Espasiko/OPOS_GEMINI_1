# Hoja de Ruta Evolutiva de OpositaIA (Rama `con_rag`)

Este documento describe el plan de desarrollo por fases para transformar OpositaIA de una aplicación puramente frontend a una plataforma de estudio avanzada con backend, RAG y modelos afinados.

---

### Fase 0: El Puente - Creación del Backend Monolítico Inteligente

**Objetivo:** Establecer una base sólida y segura para futuras funcionalidades.

- **Acciones Clave:**
  1.  Desarrollar un backend usando **FastAPI**.
  2.  Crear endpoints (`/generate-case`, `/chat`, etc.) que repliquen la funcionalidad actual de `geminiService.ts`.
  3.  Refactorizar el `geminiService.ts` del frontend para que llame a nuestro nuevo backend en lugar de directamente a la API de Google.
  4.  Configurar **Qdrant** (vector DB) y **SQLite/PostgreSQL** (datos operacionales).

- **Resultado:** La aplicación funciona igual pero ahora es segura, escalable y está lista para el RAG. La API Key ya no está en el cliente.

---

### Fase 1: La Memoria Experta - Implementación de RAG Avanzado

**Objetivo:** Dotar a la aplicación de un conocimiento profundo y preciso del temario oficial.

- **Acciones Clave:**
  1.  Crear scripts de **ingesta de datos** para procesar el temario (PDFs, texto), generar embeddings y almacenarlos en Qdrant.
  2.  Modificar el endpoint `/chat` para que, antes de llamar a Gemini, recupere contexto relevante desde Qdrant.
  3.  "Aumentar" el prompt del usuario con la información recuperada para obtener respuestas fundamentadas.

- **Resultado:** Las respuestas del chat y otras herramientas serán drásticamente más precisas y estarán basadas en el temario real, eliminando alucinaciones.

---

### Fase 2: El Sello de Experto - Fine-Tuning de Modelos

**Objetivo:** Crear un modelo de lenguaje especializado en el dominio de la Seguridad Social española que supere a los modelos genéricos.

- **Acciones Clave:**
  1.  Crear un **dataset de alta calidad** con formato `instrucción -> respuesta` (preguntas de test, resúmenes, explicaciones de artículos).
  2.  Utilizar **Unsloth** para hacer fine-tuning de un modelo base como `Mistral-7B-Instruct`.
  3.  Desplegar el modelo afinado en un servicio de inferencia (ej. Hugging Face Endpoints).
  4.  Integrar las llamadas al modelo afinado en el backend para las tareas más críticas (generación de casos, simulacros).

- **Resultado:** La aplicación ofrecerá una calidad de contenido inalcanzable para la competencia, con un "sello" de experto único.

---

### Fase 3: El Futuro - Expansión a Multi-Agente

**Objetivo:** Escalar la complejidad del sistema si el producto tiene éxito, dividiendo la lógica en agentes especializados.

- **Acciones Clave:**
  1.  Refactorizar el backend monolítico en microservicios o módulos lógicos (Agente RAG, Agente de Tests, etc.).
  2.  Implementar un orquestador que dirija las peticiones del usuario al agente adecuado.

- **Resultado:** Una arquitectura robusta y mantenible a largo plazo, capaz de crecer y añadir nuevas capacidades de forma modular.
