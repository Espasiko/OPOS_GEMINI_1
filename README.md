# OpositaIA: Asistente de Examen para la Seguridad Social

## 1. Descripción General

OpositaIA es una aplicación web de página única (SPA) construida con React y TypeScript, diseñada como un asistente de estudio integral para opositores al Cuerpo Administrativo de la Administración de la Seguridad Social en España. La aplicación utiliza la API de Google Gemini para ofrecer un conjunto de herramientas inteligentes que ayudan a los usuarios a comprender la legislación, practicar con casos realistas y organizar su estudio de manera eficiente.

El objetivo principal es proporcionar una ventaja competitiva al opositor, combinando la potencia de los modelos de IA generativa con las necesidades específicas del temario y el formato del examen.

---

## 2. Características Principales

La aplicación se organiza en torno a un panel de navegación lateral que da acceso a las siguientes herramientas:

*   **Chat Explicativo:** Un tutor IA disponible 24/7 para resolver dudas sobre legislación, explicar conceptos y analizar textos legales.
*   **Generador de Casos Prácticos:** Crea supuestos prácticos complejos y realistas con 5 preguntas tipo test, imitando el formato del examen oficial. Utiliza el modo de pensamiento avanzado de Gemini 2.5 Pro.
*   **Simulacros de Examen:** Permite al usuario configurar y realizar exámenes completos sobre temas específicos del temario, con control de tiempo y una revisión final detallada.
*   **Búsqueda Actualizada:** Realiza búsquedas en la web utilizando `Google Search grounding` para proporcionar respuestas actualizadas y citar fuentes fiables.
*   **Temario Oficial:** Un índice interactivo del temario oficial con enlaces directos a la legislación clave en el BOE.
*   **Mapas Mentales:** Genera mapas mentales interactivos y visuales sobre cualquier tema legal para facilitar la memorización y la estructuración de ideas.
*   **Esquemas:** Crea esquemas jerárquicos y detallados en formato Markdown.
*   **Resúmenes:** Sintetiza textos largos (pegados, subidos desde archivo PDF/TXT o desde una URL) en resúmenes concisos.
*   **Comparador de Leyes:** Analiza dos versiones de un texto legal y resalta las modificaciones, adiciones y eliminaciones.
*   **Tarjetas y Memes:** Una herramienta de estudio lúdica que genera flashcards interactivas y un meme visual relacionado con un tema para reforzar el aprendizaje.
*   **Plan de Estudios:** Crea planes de estudio personalizados (semanales, mensuales, etc.) basados en la disponibilidad del usuario.
*   **Mi Progreso:** Monitoriza el rendimiento del usuario en los casos prácticos y simulacros, mostrando estadísticas de aciertos y fallos.

---

## 3. Estructura del Proyecto

El proyecto sigue una estructura modular y organizada, separando la lógica de la presentación y los servicios.

```
/
├── components/
│   ├── icons/
│   │   ├── BrainIcon.tsx
│   │   ├── ... (resto de iconos SVG como componentes React)
│   ├── CaseGeneratorView.tsx
│   ├── ChatView.tsx
│   ├── ComparatorView.tsx
│   ├── FlashcardsView.tsx
│   ├── InputSourceSelector.tsx  (Componente reutilizable para entrada de datos)
│   ├── MindMapView.tsx
│   ├── MockExamView.tsx
│   ├── ProgressView.tsx
│   ├── SchemaView.tsx
│   ├── SearchGroundingView.tsx
│   ├── SettingsView.tsx
│   ├── Sidebar.tsx
│   ├── StudyPlanView.tsx
│   ├── SummaryView.tsx
│   ├── SyllabusView.tsx
│   └── UserGuideView.tsx
├── services/
│   └── geminiService.ts       (Centraliza todas las llamadas a la API de Gemini)
├── App.tsx                    (Componente principal, gestiona el estado y las vistas)
├── index.html                 (Punto de entrada HTML, carga de CDNs y script principal)
├── index.tsx                  (Renderiza la aplicación React en el DOM)
├── metadata.json              (Metadatos de la aplicación)
├── types.ts                   (Definiciones de tipos de TypeScript para todo el proyecto)
└── README.md                  (Este archivo)
```

---

## 4. Desglose de Ficheros y Componentes

#### Ficheros Raíz

*   **`index.html`**: Punto de entrada de la aplicación. Carga las dependencias externas a través de CDN (TailwindCSS, PDF.js, React-Force-Graph-2D, HTML-to-Image) y el script principal de la aplicación. Utiliza un `importmap` para gestionar las dependencias de JavaScript.
*   **`index.tsx`**: Monta el componente principal `App` en el elemento `#root` del DOM.
*   **`App.tsx`**: Es el corazón de la aplicación.
    *   Gestiona la vista activa (`currentView`).
    *   Utiliza el custom hook `usePersistentState` (definido en este mismo fichero) para mantener el estado de las herramientas (casos prácticos, mapas mentales, etc.) en `localStorage`, permitiendo que los datos persistan entre sesiones.
    *   Funciona como un enrutador, renderizando el componente de la vista correspondiente según el estado `currentView`.
*   **`types.ts`**: Define todas las interfaces y enumeraciones de TypeScript utilizadas en la aplicación (`AppView`, `PracticalCase`, `ChatMessage`, etc.), garantizando la seguridad de tipos y la claridad del código.
*   **`metadata.json`**: Contiene información básica sobre la aplicación.

#### `services/`

*   **`geminiService.ts`**: Módulo crucial que encapsula toda la interacción con la API de Google Gemini.
    *   Inicializa el cliente de `GoogleGenAI`.
    *   Define y exporta funciones asíncronas para cada herramienta que requiere IA:
        *   `generatePracticalCase()`: Usa `gemini-2.5-pro` con un esquema JSON estricto y `thinkingConfig` para alta calidad.
        *   `getChatInstance()`: Gestiona instancias de chat para mantener el historial de conversaciones.
        *   `searchWithGrounding()`: Usa `gemini-2.5-flash` con la herramienta `googleSearch`.
        *   `generateMindMap()`, `generateSchema()`, `generateSummary()`, `compareLawVersions()`: Usan `gemini-2.5-pro` (`creativeModel`) para tareas que requieren mayor creatividad y estructura.
        *   `generateMockExam()`: Similar al generador de casos, pero con un esquema y prompt dinámicos según la configuración del usuario.
        *   `generateFlashcardsAndMeme()`: Un flujo de dos pasos. Primero llama a `gemini-2.5-pro` para obtener el contenido de las tarjetas y un prompt para el meme. Luego, llama a `imagen-4.0-generate-001` con ese prompt para generar la imagen.

#### `components/`

*   **`Sidebar.tsx`**: La barra de navegación lateral. Muestra los botones para cambiar de vista y resalta la vista activa.
*   **`InputSourceSelector.tsx`**: Un componente reutilizable y clave que ofrece una interfaz unificada (pestañas para Texto, Subir Archivo, URL) para que el usuario introduzca datos. Contiene la lógica para extraer texto de archivos PDF y TXT usando `pdf.js` y `FileReader`.
*   **Componentes de Vista (`*View.tsx`)**: Cada uno de estos ficheros corresponde a una herramienta principal de la aplicación. Son responsables de:
    *   Renderizar la interfaz específica de la herramienta.
    *   Gestionar el estado local (ej: el `topic` en `MindMapView`).
    *   Llamar a las funciones correspondientes de `geminiService.ts`.
    *   Mostrar los resultados, estados de carga y errores al usuario.

---

## 5. Dependencias y Herramientas

La aplicación se construye sin un bundler (como Vite o Webpack) y carga sus dependencias directamente en el navegador a través de CDNs, lo cual es ideal para este entorno de desarrollo.

*   **React (v19.2.0)**: Biblioteca principal para construir la interfaz de usuario.
*   **TailwindCSS (CDN)**: Framework de CSS "utility-first" para un diseño rápido y responsivo.
*   **@google/genai (v1.29.0)**: SDK oficial de Google para interactuar con la API de Gemini.
*   **pdf.js (CDN)**: Librería de Mozilla para parsear y extraer texto de archivos PDF en el cliente.
*   **react-force-graph-2d (CDN)**: Componente para renderizar grafos interactivos, utilizado en los Mapas Mentales.
*   **html-to-image (CDN)**: Librería para convertir elementos del DOM en imágenes (PNG), utilizada para la función de exportación de los mapas mentales.

---

## 6. Modelos de IA y Agentes

Se ha realizado una selección estratégica de modelos para optimizar el coste y la calidad según la tarea.

| Característica              | Modelo de IA Utilizado      | Agente / System Instruction / Justificación                                                                                             |
| --------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Generador de Casos/Exámenes** | `gemini-2.5-pro`            | **Agente:** "Experto examinador". Se necesita la máxima capacidad de razonamiento (`thinkingBudget`) y seguimiento de instrucciones complejas (esquema JSON) para crear escenarios legales de alta calidad. |
| **Chat Explicativo**        | `gemini-2.5-flash`          | **Agente:** "Tutor experto en legislación". Optimizado para conversaciones rápidas y de baja latencia. Su rendimiento es excelente para responder preguntas directas. |
| **Búsqueda Actualizada**    | `gemini-2.5-flash`          | **Agente:** Neutro. La tarea principal es procesar la información de la herramienta `googleSearch`, donde la velocidad es clave. |
| **Mapas, Esquemas, Planes** | `gemini-2.5-pro`            | **Agente:** "Tutor experto/analista". Tareas creativas que se benefician de una mayor capacidad para estructurar información y generar contenido bien organizado. |
| **Generación de Memes**     | `imagen-4.0-generate-001`   | Modelo de generación de imágenes de alta calidad para crear contenido visual atractivo a partir de un prompt de texto. |

---

## 7. Flujos de Datos Clave

*   **Persistencia de Datos**: El hook `usePersistentState` en `App.tsx` es fundamental. Serializa el estado de las herramientas (el último caso generado, el último mapa mental, etc.) a formato JSON y lo guarda en `window.localStorage`. Al recargar la aplicación, lee este valor para que el usuario no pierda su trabajo.
*   **Gestión de Estado**: El estado global (como la vista actual o los datos de progreso) se gestiona en el componente `App.tsx` y se pasa a los componentes hijos a través de props. Esto sigue un patrón de "levantar el estado" (lifting state up). El estado local de cada vista (como el `userInput` en el chat) se gestiona dentro del propio componente.

---

## 8. Cómo Continuar el Desarrollo

Esta base de código es robusta y modular, permitiendo futuras expansiones.

*   **Backend y Cuentas de Usuario**: Para una aplicación de producción, sería ideal desarrollar un backend (ej: con Node.js/Express o Firebase) para:
    *   Gestionar cuentas de usuario y persistir datos en una base de datos (Firestore, PostgreSQL).
    *   Implementar un proxy para las llamadas a la API de Gemini, ocultando la clave de API y gestionando la autenticación. Esto también solucionaría cualquier problema de CORS con la función `getTextFromUrl`.
*   **Mejorar el Seguimiento de Progreso**: El componente `ProgressView` podría expandirse para mostrar gráficos más detallados, filtrar por temas específicos y mostrar la evolución a lo largo del tiempo.
*   **Gamificación**: Añadir elementos como logros, rachas de estudio o insignias para aumentar la motivación del usuario.
*   **Integración con Calendario**: Permitir que el "Plan de Estudios" se sincronice con Google Calendar u otros servicios.
*   **Modelo de Monetización**: Implementar un sistema de suscripción (ej: con Stripe) para desbloquear funcionalidades ilimitadas, siguiendo el modelo Freemium descrito en `SettingsView.tsx`.
