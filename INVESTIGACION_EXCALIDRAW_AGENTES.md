# 🎨 Investigación: Excalidraw para Agentes de OpositAIA

**Objetivo**: Permitir que los agentes generen mapas mentales y diagramas **editables** y visualmente atractivos, usando Excalidraw (versión Free/Open Source).

---

## 1. Hallazgos Clave

1.  **Formato Editable (.excalidraw)**:
    *   Excalidraw usa un formato JSON abierto. Si generamos este JSON, el usuario puede abrir el archivo en `excalidraw.com` (o en una versión self-hosted) y **editarlo libremente**.
    *   Esto es una ventaja enorme sobre generar imágenes estáticas (PNG/JPG).

2.  **Conversión Mermaid → Excalidraw**:
    *   Existe una librería oficial: `@excalidraw/mermaid-to-excalidraw`.
    *   **Flujo Mágico**:
        1.  El Agente genera código **Mermaid** (los LLMs son excelentes en esto).
        2.  Una herramienta (MCP) convierte ese Mermaid a JSON de Excalidraw.
        3.  El usuario recibe un archivo `.excalidraw` listo para editar.

3.  **Coste y Licencia**:
    *   La librería y el formato son Open Source (MIT).
    *   No requiere suscripción "Plus" para generar o editar estos archivos.
    *   La IA de Excalidraw+ es de pago, pero **nosotros usamos nuestra propia IA (Gemini)** para generar el diagrama, así que no la necesitamos.

---

## 2. Propuesta de Implementación: `excalidraw_generator` MCP Tool

Crearemos una nueva herramienta en el MCP Server que encapsule la librería de conversión.

### Flujo de Trabajo

1.  **Usuario**: "Hazme un mapa mental de la Constitución".
2.  **Agente (Content Creator)**: Genera un diagrama en sintaxis Mermaid (`graph TD...`).
3.  **Agente**: Llama a la tool `excalidraw_generator` con el código Mermaid.
4.  **MCP Tool**:
    *   Usa `@excalidraw/mermaid-to-excalidraw` para parsear.
    *   Genera el JSON con los "elements" (cajas, flechas, estilo "hand-drawn").
    *   Guarda el archivo `mapa_constitucion.excalidraw`.
5.  **Usuario**: Recibe el archivo y lo abre para estudiar/editar.

### Definición de la Tool (MCP)

```typescript
// Tool Schema
{
  name: "generate_excalidraw",
  description: "Convert Mermaid diagram code into an editable Excalidraw file",
  inputSchema: {
    type: "object",
    properties: {
      mermaid_code: { type: "string", description: "Mermaid syntax code (graph, flowchart, etc)" },
      filename: { type: "string", description: "Output filename without extension" }
    },
    required: ["mermaid_code", "filename"]
  }
}
```

---

## 3. Integración con "Document Factory"

Este componente encaja perfectamente en la arquitectura de agentes propuesta:

*   **Nuevo Rol**: `VisualDesigner Agent`.
*   **Responsabilidad**: Recibe texto/resúmenes y los convierte a Mermaid optimizado para mapas mentales.
*   **Uso en Factory**:
    *   El `Planner` decide: "La Sección 3 necesita un diagrama explicativo".
    *   El `VisualDesigner` genera el `.excalidraw`.
    *   El `Assembler` adjunta el archivo o un link en el documento final.

## 4. Ejemplo de Prompt para el Agente

```yaml
# System Prompt para VisualDesigner
role: "Expert Visual Communicator"
instructions: |
  You transform complex legal concepts into clear Mermaid diagrams.
  
  RULES FOR MIND MAPS:
  1. Use `graph TD` or `mindmap` syntax.
  2. Keep node text short (max 5 words).
  3. Use distinct shapes for different hierarchy levels.
  4. OUTPUT ONLY valid Mermaid code.
```

## 5. Conclusión y Siguientes Pasos

*   **Viabilidad**: ✅ Alta. Coste cero en licencias.
*   **Calidad**: ✅ Alta. Estilo "hand-drawn" amigable para estudiantes.
*   **Acción**:
    1.  Añadir `@excalidraw/mermaid-to-excalidraw` al `package.json` del MCP Server.
    2.  Implementar la tool `generate_excalidraw`.
    3.  Crear el agente `VisualDesigner`.
