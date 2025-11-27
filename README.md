# OpositaIA: Asistente de Examen para la Seguridad Social

[![Installation Guide](https://img.shields.io/badge/📦-Installation_Guide-blue)](./INSTALLATION.md)
[![Setup Guide](https://img.shields.io/badge/⚙️-Setup_Guide-green)](./SETUP.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

> 🚀 **¿Primera vez aquí?** Lee la [Guía de Instalación Completa](./INSTALLATION.md) para configurar el proyecto desde cero.

## 1. Descripción General

OpositaIA es una aplicación web de página única (SPA) construida con React y TypeScript, diseñada como un asistente de estudio integral para opositores al Cuerpo Administrativo de la Administración de la Seguridad Social en España. La aplicación utiliza la API de Google Gemini para ofrecer un conjunto de herramientas inteligentes que ayudan a los usuarios a comprender la legislación, practicar con casos realistas y organizar su estudio de manera eficiente.

El objetivo principal es proporcionar una ventaja competitiva al opositor, combinando la potencia de los modelos de IA generativa con las necesidades específicas del temario y el formato del examen.

---

## 2. Características Principales

La aplicación se organiza en torno a un panel de navegación lateral que da acceso a las siguientes herramientas:

- **Chat Explicativo:** Un tutor IA disponible 24/7 para resolver dudas sobre legislación, explicar conceptos y analizar textos legales.
- **Generador de Casos Prácticos:** Crea supuestos prácticos complejos y realistas con 5 preguntas tipo test, imitando el formato del examen oficial. Utiliza el modo de pensamiento avanzado de Gemini 2.5 Pro.
- **Simulacros de Examen:** Permite al usuario configurar y realizar exámenes completos sobre temas específicos del temario, con control de tiempo y una revisión final detallada.
- **Búsqueda Actualizada:** Realiza búsquedas en la web utilizando `Google Search grounding` para proporcionar respuestas actualizadas y citar fuentes fiables.
- **Temario Oficial:** Un índice interactivo del temario oficial con enlaces directos a la legislación clave en el BOE.
- **Mapas Mentales:** Genera mapas mentales interactivos y visuales sobre cualquier tema legal para facilitar la memorización y la estructuración de ideas.
- **Esquemas:** Crea esquemas jerárquicos y detallados en formato Markdown.
- **Resúmenes:** Sintetiza textos largos (pegados, subidos desde archivo PDF/TXT o desde una URL) en resúmenes concisos.
- **Comparador de Leyes:** Analiza dos versiones de un texto legal y resalta las modificaciones, adiciones y eliminaciones.
- **Tarjetas y Memes:** Una herramienta de estudio lúdica que genera flashcards interactivas y un meme visual relacionado con un tema para reforzar el aprendizaje.
- **Plan de Estudios:** Crea planes de estudio personalizados (semanales, mensuales, etc.) basados en la disponibilidad del usuario.
- **Mi Progreso:** Monitoriza el rendimiento del usuario en los casos práctácticos y simulacros, mostrando estadísticas de aciertos y fallos.

---

## 3. Estructura del Proyecto

El proyecto sigue una estructura modular y organizada, separando la lógica de la presentación y los servicios.

```
/
├── components/
│   ├── ... (Componentes de la interfaz de usuario)
├── docs/
│   ├── AI_AGENTS.md           (Especificación de los prompts y modelos de IA)
│   ├── ARCHITECTURE.md        (Visión general de la arquitectura)
│   └── DATA_MODEL.md          (Descripción del modelo de datos y tipos)
├── services/
│   └── geminiService.ts       (Centraliza todas las llamadas a la API de Gemini)
├── App.tsx                    (Componente principal, gestiona el estado y las vistas)
├── index.html                 (Punto de entrada HTML)
├── index.tsx                  (Renderiza la aplicación React en el DOM)
├── metadata.json              (Metadatos de la aplicación)
├── types.ts                   (Definiciones de tipos de TypeScript)
└── README.md                  (Este archivo)
```

---

## 4. Arquitectura y Documentación (AI Specs)

Este proyecto sigue una estrategia de **"AI Spec Driven Development"**. La documentación no es solo para humanos, sino que está estructurada para que los asistentes de IA puedan entender el contexto del proyecto, su arquitectura y sus objetivos. Esto permite una colaboración más eficiente y precisa.

La documentación principal se encuentra en la carpeta `/docs`:

- **[Arquitectura del Sistema](./docs/ARCHITECTURE.md):** Una visión de alto nivel de la aplicación, su flujo de datos y dependencias.
- **[Definición de Agentes de IA](./docs/AI_AGENTS.md):** El documento más importante. Detalla cada llamada a la API de Gemini, explicando el "agente" o "personalidad" que se le pide al modelo, la configuración específica, el modelo utilizado y la justificación de esa elección.
- **[Modelo de Datos](./docs/DATA_MODEL.md):** Una explicación clara de las estructuras de datos y tipos definidos en `types.ts`.

---

## 5. Despliegue y Desarrollo Local

Dado que la aplicación no utiliza un _bundler_ (como Vite o Webpack), el despliegue en un entorno local es muy sencillo y solo requiere un servidor web estático.

**Pasos:**

1.  **Obtén el código:** Clona o descarga todos los archivos del proyecto en una carpeta local.

2.  **Inicia un servidor web local:** No puedes abrir `index.html` directamente en el navegador (`file:///...`) debido a las políticas de seguridad (CORS) que bloquean las importaciones de módulos. Necesitas servir los archivos a través de un servidor.
    - **Opción A (Recomendada con Node.js):** Usa `live-server`, un paquete de `npm` que crea un servidor de desarrollo con recarga automática.

      ```bash
      # Instala live-server globalmente (solo la primera vez)
      npm install -g live-server

      # Desde la carpeta raíz del proyecto, inicia el servidor
      live-server
      ```

      Se abrirá automáticamente una pestaña en tu navegador en `http://127.0.0.1:8080`.

    - **Opción B (Alternativa con Python):** Si tienes Python instalado.

      ```bash
      # Desde la carpeta raíz del proyecto (para Python 3)
      python -m http.server

      # O para Python 2
      # python -m SimpleHTTPServer
      ```

      Abre tu navegador y ve a `http://localhost:8000`.

3.  **¡Listo!** La aplicación ya está funcionando en tu máquina local. La clave de API de Gemini es gestionada por el entorno de desarrollo y no requiere configuración manual en un fichero `.env`.

---

## 6. Modelos de IA y Agentes

Se ha realizado una selección estratégica de modelos para optimizar el coste y la calidad según la tarea.

| Característica                                     | Modelo de IA Utilizado    | Agente / System Instruction / Justificación                                                                                                                                                                 |
| -------------------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Generador de Casos/Exámenes**                    | `gemini-2.5-pro`          | **Agente:** "Experto examinador". Se necesita la máxima capacidad de razonamiento (`thinkingBudget`) y seguimiento de instrucciones complejas (esquema JSON) para crear escenarios legales de alta calidad. |
| **Chat Explicativo**                               | `gemini-2.5-flash`        | **Agente:** "Tutor experto en legislación". Optimizado para conversaciones rápidas y de baja latencia. Su rendimiento es excelente para responder preguntas directas.                                       |
| **Búsqueda Actualizada**                           | `gemini-2.5-flash`        | **Agente:** Neutro. La tarea principal es procesar la información de la herramienta `googleSearch`, donde la velocidad es clave.                                                                            |
| **Mapas, Esquemas, Planes, Resúmenes, Comparador** | `gemini-2.5-pro`          | **Agente:** "Tutor experto/analista". Tareas creativas que se benefician de una mayor capacidad para estructurar información y generar contenido bien organizado.                                           |
| **Flashcards (texto)**                             | `gemini-2.5-pro`          | **Agente:** "Generador de material de estudio". Crea preguntas y respuestas concisas y un prompt creativo para el meme.                                                                                     |
| **Generación de Memes (imagen)**                   | `imagen-4.0-generate-001` | Modelo de generación de imágenes de alta calidad para crear contenido visual atractivo a partir de un prompt de texto.                                                                                      |
