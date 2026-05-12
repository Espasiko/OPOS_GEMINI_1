# PLAN DE CONTINGENCIA: CERO ERRORES LEGALES EN IA (MINIMIZACIÓN DE ALUCINACIONES)

El análisis cruzado y las críticas evidencian un problema troncal de los modelos fundacionales (incluido este): **la soberbia algorítmica**. A pesar de tener acceso al MCP del BOE, cuando la IA cree "saberse" la norma (o deduce la tabla paramétrica, como las mensualidades de la IP), tiende a redactar la justificación de memoria para ahorrar llamadas a la API, introduciendo sub-artículos falsos (ej. 15.3 en lugar de 15.1) o malinterpretando restricciones de edad (ej. excluir a los 54 años cuando la exclusión real de la O.M. de 1969 es a los 60).

Para llevar los fallos a **CERO**, el sistema debe dejar de comportarse como un "estudiante listillo" y empezar a comportarse como un **Auditor Informático del BOE**. Este es el plan de choque arquitectónico y procedimental:

## 1. Obligatoriedad de "Consulta Fría" (Zero-Trust)
**Diagnóstico:** El error en la Pregunta 7 (Tanto alzado a los 58 años = 24 mensualidades) se debió a que inferí la exclusión sin bajarme el texto literal de la O.M. 15/04/1969.
**Solución Inmediata:** 
*   **Regla de Sistema (Prompting):** Queda *estrictamente prohibido* que cualquier agente o workflow genere una justificación legal sin haber ejecutado previamente la herramienta `mcp_boe_get_law_text_block` para extraer la cita literal.
*   **Implementación:** En todos los prompts de creación de casos, añadir: *"Para CADA pregunta, es obligatorio extraer el artículo exacto usando el MCP. Si no extraes el bloque, el intento será fallido"*.

## 2. Refactorización de las Respuestas (Separación de Preocupaciones)
**Diagnóstico:** Como apuntaba el análisis externo, mezclar la solución (A, B, C, D) con la cita legal en el mismo bloque contamina el aprendizaje si la IA comete un lapsus en el número del artículo, haciendo que el opositor dude de que la letra sea correcta.
**Solución Inmediata:**
*   Se generarán siempre **dos archivos distintos**:
    1.  `PLANTILLA_RESPUESTAS_X.md`: Estrictamente un listado (ej: 1-B, 2-C, 3-D).
    2.  `JUSTIFICACIONES_LEGALES_X.md`: Un documento de investigación con las citas exactas copiadas del BOE, con el enlace al artículo.

## 3. Revisión Adversaria Obligatoria (Doble Agente)
**Diagnóstico:** La IA que escribe el examen sufre sesgo de confirmación. Da sus respuestas por válidas sin escrutarlas.
**Solución Inmediata:**
*   Antes de entregar un caso finalizado, invocar sistemáticamente el skill `bmad-review-adversarial-general` o una pasada iterativa propia, diciéndole al modelo: *"Adopta el rol de Inspector de Trabajo. Intenta tumbar y demostrar que las 18 respuestas que acabas de escribir son ilegales según el BOE"*.
*   Si la IA no puede respaldar su propia respuesta con un artículo extraído tras la revisión, la pregunta se reforma.

## 4. Ingestión de "Criterios Trampa" en el Knowledge Graph
**Diagnóstico:** Cuestiones como los "15 años hacia atrás desde el mes previo" en viudedad o el devengo de intereses "al día siguiente del apremio" son heurísticas de examen, no simples artículos.
**Solución Inmediata:**
*   Crear nodos especiales en `Neo4j` tipificados como `EXAM_TRAP`.
*   Asociar estos nodos a los artículos raíz. Ejemplo: El *Art. 218* (Viudedad ANL) se enlaza con `[EXAM_TRAP]: El recuento de 15 años SIEMPRE excluye el mes del hecho causante. No contar desde el mismo día`.
*   Cuando la IA utilice el RAG, leerá simultáneamente la Ley pura y el "Cepo" asociado a ella detectado por David de Miguel (u otras academias).

## 5. Control de Calidad de Versiones Clónicas
* Al generar "Casos Clon", el modelo ya no alterará las edades o fechas paramétricamente sin pasar por una calculadora de Seguridad Social o validar la tabla. (Hacer pasar a alguien de 55 a 58 años en una IP altera la tabla de indemnizaciones de 60 a 24 mensualidades. Yo lo sabía, pero forcé una exclusión que no procedía). A partir de ahora, toda alteración paramétrica requiere recálculo justificado.

> [!IMPORTANT]
> **Acción Inmediata Realizada:** Procedo a enmendar el archivo `respuestas_caso_febrerov2_NUEVO.md` para corregir la atrocidad de la Pregunta 7 (Mariana sí percibe el tanto alzado en 24 mensualidades) y repasar la pulcritud de los artículos citados (como el 15.1 en la pregunta 2).
