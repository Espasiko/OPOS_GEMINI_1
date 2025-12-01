# 🏭 Propuesta: "Document Factory" para OpositAIA

**Referencia**: Basado en [Agent Factory with Subagents](https://github.com/coleam00/context-engineering-intro/tree/main/use-cases/agent-factory-with-subagents) y adaptado a `PROPUESTA_SISTEMA_AGENTES_YAML.md`.

## 💡 Concepto Clave
El patrón "Agent Factory" utiliza sub-agentes especializados (Planner, Builder, Validator) para construir software complejo.
Para **OpositAIA**, adaptaremos este patrón para construir **Documentos de Estudio Complejos** (Temarios, Simulacros, Resúmenes Legales) en lugar de código.

En lugar de un solo agente intentando escribir todo un tema, usamos una "Fábrica de Documentos" orquestada.

---

## 1. Arquitectura "Document Factory"

Imagina que el usuario pide: *"Générame el Tema 1 de la Constitución con test y casos prácticos"*.

En lugar de un solo prompt gigante, activamos la **Factory**:

### 🏗️ Los Sub-Agentes (Roles)

1.  **📋 Document Planner (El Arquitecto)**
    *   **Función**: No escribe contenido. Solo diseña la *estructura* del documento.
    *   **Output**: Un "esqueleto" en JSON/YAML que define las secciones necesarias.
    *   *Ejemplo*: "Sección 1: Artículos clave (Writer A)", "Sección 2: Jurisprudencia (Writer B)", "Sección 3: Test (Examiner)".

2.  **✍️ Content Writers (Los Redactores - Ejecución en Paralelo)**
    *   **Función**: Agentes especializados que escriben *partes específicas* del plan.
    *   *Variantes*:
        *   `LegalWriter`: Redacta teoría legal.
        *   `Examiner`: Crea preguntas de test (ya definido en tu propuesta).
        *   `CaseDesigner`: Crea casos prácticos.

3.  **⚖️ Legal Validator (El Auditor)**
    *   **Función**: Revisa que las citas legales (Art. X) existan y estén vigentes (usando `boe_verify`).
    *   **Acción**: Si falla, devuelve la sección al Writer para corrección.

4.  **🎨 Format Assembler (El Editor)**
    *   **Función**: Recopila todos los fragmentos aprobados y les da formato final (Markdown, PDF, HTML) con estilos consistentes.

---

## 2. Implementación en YAML (Compatible con tu Sistema)

Podemos definir esta "Factory" como un **Workflow Avanzado** en tu sistema actual.

### Definición del Workflow (Factory)

```yaml
# opos-agents/workflows/document-factory/topic-generation.yaml
name: "generate-study-topic"
description: "Factory pattern to generate a complete study topic"

steps:
  # FASE 1: PLANIFICACIÓN
  - id: "plan-structure"
    agent: "study-planner"
    action: "create_topic_outline"
    params:
      topic: "{{user_topic}}"
      level: "{{user_level}}"
    output: "topic_blueprint" # JSON con la estructura de secciones

  # FASE 2: EJECUCIÓN (PARALELA - "FAN OUT")
  # El sistema itera sobre las secciones definidas en el blueprint
  - id: "write-sections"
    type: "map" # Itera sobre una lista
    items: "{{topic_blueprint.sections}}"
    concurrency: 5
    steps:
      - id: "route-to-specialist"
        # Router dinámico: elige el agente según el tipo de sección
        agent: "{{item.recommended_agent}}" 
        action: "generate_content"
        params:
          instructions: "{{item.instructions}}"
          context: "{{item.context}}"
        output: "draft_content"

      - id: "verify-section"
        agent: "validator"
        action: "verify_legal_accuracy"
        params:
          content: "{{draft_content}}"
        retry_on_failure: true # Bucle de auto-corrección

  # FASE 3: ENSAMBLAJE ("FAN IN")
  - id: "assemble-document"
    agent: "content-creator"
    action: "assemble_final_doc"
    params:
      fragments: "{{write-sections.results}}"
      format: "markdown"
    output: "final_document"
```

---

## 3. Ejemplo de Flujo Real

**Usuario**: "Quiero un resumen del Título Preliminar de la CE".

1.  **Planner**: Genera el `topic_blueprint`:
    ```json
    {
      "sections": [
        {"type": "theory", "agent": "legal-writer", "topic": "Definición de España (Art 1)"},
        {"type": "theory", "agent": "legal-writer", "topic": "Valores Superiores"},
        {"type": "quiz", "agent": "examiner", "topic": "Test de 5 preguntas sobre Art 1-9"},
        {"type": "case", "agent": "case-analyzer", "topic": "Caso práctico: Bandera y Capitalidad"}
      ]
    }
    ```
2.  **Execution**:
    *   `legal-writer` escribe la teoría (en paralelo).
    *   `examiner` genera el test (en paralelo).
    *   `case-analyzer` crea el caso (en paralelo).
3.  **Validation**:
    *   El `validator` detecta que el `legal-writer` citó el "Art 9.4" (que no existe, es hasta el 9.3).
    *   Rechaza el borrador y pide corrección automática.
4.  **Assembly**:
    *   Une todo en un documento Markdown bonito con índices y tablas.

## 4. ¿Por qué usar este patrón?

1.  **Calidad Superior**: Un solo agente se "pierde" en documentos largos. Dividir el trabajo garantiza que el experto en tests haga los tests y el experto en leyes haga la teoría.
2.  **Auto-Corrección**: La fase de validación evita alucinaciones legales antes de que el usuario vea el documento.
3.  **Velocidad**: Al paralelizar las secciones, generas un tema de 20 páginas en el tiempo que tarda una sección.

## 5. Siguientes Pasos para Aplicarlo

1.  **Define el "Planner Agent"**: Entrénalo (vía System Prompt) para que no responda al usuario, sino que genere **planes de trabajo JSON**.
2.  **Crea el "Assembler Agent"**: Un agente simple experto en Markdown/LaTeX que sepa unir piezas.
3.  **Actualiza tu `workflow.yaml`**: Añade soporte para pasos tipo `map` (iteración paralela) si tu orquestador lo permite (o simúlalo con pasos fijos).

---

## 6. 💰 Análisis de Viabilidad y Costes (Tokens)

Es natural pensar que "más agentes = más gasto", pero en generación de documentos largos, **el patrón Factory suele ser MÁS BARATO**.

### ¿Por qué disminuye el coste?

1.  **Ahorro en Input Tokens (Contexto)**:
    *   **Enfoque Monolítico**: Tienes que enviar un "System Prompt" gigante (instrucciones de estilo, legales, formato, tests, etc.) en *cada interacción*.
    *   **Enfoque Factory**:
        *   Al `Examiner` solo le envías instrucciones de tests (Prompt pequeño).
        *   Al `LegalWriter` solo instrucciones de redacción (Prompt pequeño).
        *   **Resultado**: Reduces drásticamente la cantidad de "basura" que envías en cada llamada.

2.  **Ahorro por "Aislamiento de Errores"**:
    *   **Monolítico**: Si generas un tema de 20 páginas y el modelo alucina en la página 18, a menudo tienes que regenerar **todo el documento** (o hacer "cortar y pegar" manual complejo).
    *   **Factory**: Si el `Examiner` falla en una pregunta, el `Validator` lo detecta y solo regeneras *esa pregunta*. El resto del documento (que costó dinero generar) se salva.

3.  **Context Window más limpio**:
    *   Los modelos cobran por el tamaño de la ventana de contexto. Al dividir la tarea, cada sub-agente trabaja con una ventana limpia y corta, lo que es más barato y produce mejores resultados (menos "olvidos").

### Comparativa Estimada (Ejemplo: Tema de 10 páginas)

| Concepto | Enfoque Monolítico (1 Agente) | Enfoque Factory (Multi-Agente) | Diferencia |
| :--- | :--- | :--- | :--- |
| **Input Tokens** | 1 Prompt Gigante x 5 llamadas (para completar) | 5 Prompts Pequeños x 1 llamada | **Factory Gana** (Menos repetición) |
| **Output Tokens** | ~5,000 tokens (contenido) | ~5,200 tokens (contenido + JSON overhead) | **Empate** (Similar) |
| **Re-intentos** | Alto riesgo (regenerar bloques grandes) | Bajo riesgo (regenerar fragmentos pequeños) | **Factory Gana** (Mucho ahorro) |
| **Calidad** | Variable (se degrada al final) | Constante (cada agente está fresco) | **Factory Gana** |

### Veredicto Financiero
*   Para **respuestas cortas** (chat rápido): El Factory es **más caro** (overhead innecesario).
*   Para **generar Temarios/Documentos** (tu caso): El Factory es **más barato y viable**, porque el ahorro en re-generaciones y limpieza de contexto supera el coste de orquestación.
