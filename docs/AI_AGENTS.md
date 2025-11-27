# Definición de Agentes de IA en OpositaIA

Este documento es la "fuente de la verdad" para todas las interacciones con la API de Google Gemini. Describe la "personalidad" (agente), el modelo, la configuración y la justificación de cada función definida en `services/geminiService.ts`.

---

### 1. `generatePracticalCase()` y `generateMockExam()`

- **Función:** `generatePracticalCase()`, `generateMockExam(topics, questionCount)`
- **Agente/Personalidad:** "Actúa como un examinador experto para el examen de la Seguridad Social española."
- **Modelo:** `gemini-2.5-pro`
- **Justificación:** Estas son las tareas más críticas y complejas de la aplicación. Requieren:
  1.  **Alta capacidad de razonamiento:** Para crear escenarios legales realistas y preguntas desafiantes que no sean triviales.
  2.  **Seguimiento estricto de instrucciones:** La salida debe ser un JSON válido que se adhiera a un `responseSchema` complejo y anidado.
  3.  **Calidad sobre velocidad:** Es preferible esperar unos segundos más para obtener un caso práctico o un examen de alta calidad que simule fielmente la prueba real.
- **Configuración Clave:**
  - `model: 'gemini-2.5-pro'`
  - `responseMimeType: "application/json"`
  - `responseSchema`: Un esquema detallado que define la estructura del caso o examen, incluyendo preguntas, opciones y explicaciones.
  - `thinkingConfig: { thinkingBudget: 32768 }`: Se le asigna el máximo presupuesto de "pensamiento" para fomentar un análisis profundo antes de generar la respuesta.

---

### 2. `getChatInstance()`

- **Función:** `getChatInstance(conversationId)`
- **Agente/Personalidad:** "Eres un tutor experto de clase mundial especializado en la legislación de la Seguridad Social española para opositores. Tu tono es alentador, preciso y claro."
- **Modelo:** `gemini-2.5-flash`
- **Justificación:** El chat necesita ser rápido e interactivo. `gemini-2.5-flash` ofrece una excelente relación entre velocidad y calidad para tareas de conversación y explicación. El `systemInstruction` establece el contexto y el tono para todas las interacciones dentro de una sesión de chat.
- **Configuración Clave:**
  - `model: 'gemini-2.5-flash'`
  - `config: { systemInstruction: "..." }`: Define el rol del modelo para toda la conversación.

---

### 3. `searchWithGrounding()`

- **Función:** `searchWithGrounding(query, untilDate)`
- **Agente/Personalidad:** Neutro. El prompt es simplemente la consulta del usuario.
- **Modelo:** `gemini-2.5-flash`
- **Justificación:** La tarea principal del modelo aquí es procesar la información obtenida a través de la herramienta `googleSearch` y sintetizar una respuesta. La velocidad es importante para una experiencia de búsqueda fluida, y `gemini-2.5-flash` es ideal para esto.
- **Configuración Clave:**
  - `model: 'gemini-2.5-flash'`
  - `config: { tools: [{ googleSearch: {} }] }`: Habilita la herramienta de búsqueda de Google para fundamentar la respuesta en información web reciente.

---

### 4. Tareas Creativas y de Estructuración

- **Funciones:** `generateMindMap()`, `generateStudyPlan()`, `generateSchema()`, `generateSummary()`, `compareLawVersions()`
- **Agente/Personalidad:** "Experto tutor legal", "analista legislativo experto", etc., dependiendo de la tarea.
- **Modelo:** `gemini-2.5-pro`
- **Justificación:** Aunque algunas de estas tareas podrían ser manejadas por modelos más rápidos, se elige `gemini-2.5-pro` para garantizar una alta calidad en la estructura y el contenido. Tareas como generar un mapa mental lógico, crear un plan de estudios coherente o comparar matices en textos legales se benefician enormemente de la mayor capacidad de razonamiento de este modelo.
- **Configuración Clave:**
  - `model: 'gemini-2.5-pro' ('creativeModel')`
  - `responseMimeType: "application/json"` (para `generateMindMap` para forzar una salida JSON).
  - Prompts detallados que especifican el formato de salida deseado (JSON, Markdown, etc.).

---

### 5. `generateFlashcardsAndMeme()`

Este es un flujo de trabajo de dos pasos que utiliza dos modelos diferentes.

- **Paso 1: Generación de Texto**
  - **Función (parcial):** `ai.models.generateContent`
  - **Agente/Personalidad:** "Generador de material de estudio."
  - **Modelo:** `gemini-2.5-pro`
  - **Justificación:** Se necesita un modelo potente para crear un conjunto de flashcards de alta calidad (pregunta/respuesta) y, crucialmente, para idear un _prompt_ de imagen que sea ingenioso, descriptivo y divertido.
  - **Configuración Clave:**
    - `model: 'gemini-2.5-pro'`
    - `responseMimeType: "application/json"`
    - `responseSchema`: Define la estructura para las flashcards y el `meme_prompt`.

- **Paso 2: Generación de Imagen**
  - **Función (parcial):** `ai.models.generateImages`
  - **Agente/Personalidad:** N/A (modelo de imagen). El "agente" está contenido en el prompt generado en el paso anterior.
  - **Modelo:** `imagen-4.0-generate-001`
  - **Justificación:** Se utiliza un modelo de generación de imágenes de alta calidad para crear un meme visualmente atractivo y coherente con el prompt.
  - **Configuración Clave:**
    - `model: 'imagen-4.0-generate-001'`
    - `prompt`: El `meme_prompt` obtenido del Paso 1.
    - `config: { numberOfImages: 1, outputMimeType: 'image/jpeg' }`
