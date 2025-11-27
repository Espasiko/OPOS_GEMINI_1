# Modelo de Datos de OpositaIA

Este documento describe las principales estructuras de datos y tipos utilizados en toda la aplicación, definidos en el fichero `types.ts`.

## Enumeraciones (Enums)

### `AppView`

Controla qué vista o herramienta se muestra en el área de contenido principal de la aplicación. Es el estado central que gestiona la navegación.

- **Valores:** `CHAT`, `CASE_GENERATOR`, `SEARCH`, `SYLLABUS`, `MIND_MAP`, etc.

## Interfaces Principales

### `ChatMessage` y `Conversation`

- **`ChatMessage`**: Representa un único mensaje en el chat.
  - `id`: Identificador único.
  - `role`: `'user'` o `'model'`, para diferenciar quién envió el mensaje.
  - `text`: El contenido del mensaje.
- **`Conversation`**: Representa una sesión de chat completa.
  - `id`: Identificador único de la conversación.
  - `title`: Un título corto, generalmente extraído del primer mensaje del usuario.
  - `messages`: Un array de objetos `ChatMessage`.

### Estructura de Casos Prácticos y Exámenes

Estas interfaces definen la estructura de los casos prácticos y las preguntas de los simulacros, que es generada por la IA.

- **`PracticalCaseOption`**: Una opción de respuesta en una pregunta tipo test.
  - `id`: Identificador de la opción (ej: 'A', 'B').
  - `text`: El texto de la opción.
- **`PracticalCaseQuestion`**: Una pregunta completa.
  - `id`: Identificador único de la pregunta (ej: 'q1').
  - `question`: El enunciado de la pregunta.
  - `options`: Un array de 4 `PracticalCaseOption`.
  - `correct_option_id`: El `id` de la opción correcta.
  - `explanation`: Una explicación detallada que justifica la respuesta correcta.
- **`PracticalCase`**: Un caso práctico completo.
  - `topic`: El tema legal sobre el que trata el caso.
  - `scenario`: El texto descriptivo del supuesto práctico.
  - `questions`: Un array de `PracticalCaseQuestion`.
- **`MockExam`**: Un simulacro de examen completo.
  - `title`: El título del examen.
  - `questions`: Un array de `PracticalCaseQuestion`.

### `CaseAnswer`

Almacena el estado de las respuestas del usuario para un caso práctico o examen. Es un objeto donde las claves son los `questionId`.

- **`[questionId]`**:
  - `selectedOptions`: Un array de los `id` de las opciones que el usuario ha seleccionado.
  - `attempts`: El número de intentos que el usuario ha realizado.
  - `showExplanation`: Un booleano que indica si la explicación debe mostrarse.

### `GroundingSource`

Representa una fuente web citada por la herramienta de "Búsqueda Actualizada".

- `uri`: La URL del sitio web.
- `title`: El título de la página.

### `MindMapNode`

Define la estructura recursiva de un nodo en el mapa mental.

- `id`: Identificador único del nodo.
- `text`: El contenido del nodo.
- `children`: Un array de otros objetos `MindMapNode`, creando la estructura de árbol.

### `Flashcard`

Representa una tarjeta de memoria individual.

- `id`: Identificador único.
- `front`: El texto del anverso (pregunta o término).
- `back`: El texto del reverso (respuesta o definición).
