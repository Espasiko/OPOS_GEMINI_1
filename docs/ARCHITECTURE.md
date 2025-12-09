# Arquitectura de OpositaIA

## 1. Visión General

OpositaIA es una **Aplicación de Página Única (SPA - Single Page Application)** construida con React y TypeScript. Actualmente usa un backend FastAPI como router multi-proveedor (Gemini, Mistral, Groq, etc.) y el frontend llama a ese backend para toda la generación de contenido.

La aplicación no utiliza un _bundler_ como Vite o Webpack. En su lugar, carga las dependencias (React, TailwindCSS, etc.) a través de una red de distribución de contenidos (CDN) y utiliza un `importmap` en `index.html` para gestionar los módulos de ES6, lo que simplifica el entorno de desarrollo.

## 2. Diagrama de Arquitectura

El siguiente diagrama ilustra el flujo principal de la aplicación:

```mermaid
graph TD
    subgraph Browser (Client-Side)
        A[Usuario] --> B{Interfaz de Usuario (React Components)};
        B --> C[frontend/services/backendService.ts];
        C --> D[FastAPI backend (router multi-proveedor)];
        D --> E[LLM providers];
        E --> D;
        D --> C;
        C --> B;
        B --> A;
        B -- Persistencia de Estado --> F[LocalStorage];
    end

    subgraph Google Cloud
        D;
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#fb5,stroke:#333,stroke-width:2px
    style E fill:#dfd,stroke:#333,stroke-width:2px
```

## 3. Flujo de Datos y Gestión de Estado

- **Componente Principal (`App.tsx`):** Actúa como el orquestador principal. Gestiona el estado de la vista actual (`currentView`) para determinar qué herramienta se muestra al usuario.

- **Estado Persistente (`usePersistentState`):** Un _custom hook_ en `App.tsx` se encarga de la persistencia de datos. Cuando el estado de una herramienta cambia (por ejemplo, se genera un nuevo caso práctico), este hook lo serializa a JSON y lo guarda en `window.localStorage`. Al iniciar la aplicación, el hook lee los datos de `localStorage` para restaurar el estado anterior, permitiendo al usuario continuar donde lo dejó.

- **Servicio de backend (`frontend/services/backendService.ts`):** Punto único de contacto del frontend con el backend FastAPI. Encapsula rutas `/chat`, `/generate-case`, `/upload`, etc., y pasa el `provider` seleccionado.

- **Componentes de Vista (`*View.tsx`):** Cada componente de vista gestiona su estado local y, cuando necesita IA, llama a `backendService` (no hay `geminiService`).

## 4. Dependencias Externas (vía CDN)

La aplicación depende de varias librerías de terceros cargadas a través de CDN en `index.html`:

- **React y ReactDOM:** La biblioteca principal para construir la interfaz de usuario.
- **TailwindCSS:** Un framework de CSS "utility-first" para un diseño rápido y responsivo.
- **@google/genai:** El SDK oficial para interactuar con la API de Gemini.
- **pdf.js:** La librería de Mozilla, utilizada en el componente `InputSourceSelector` para leer y extraer texto de archivos PDF subidos por el usuario.
- **html-to-image:** Utilizada en la vista `MindMapView` para convertir el mapa mental (que es un elemento del DOM) en una imagen PNG para su descarga.
