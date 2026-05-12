# 💡 ESTRATEGIA: MITIGACIÓN DE ALUCINACIONES CAUSALES Y LÓGICAS EN EL LLM
*(Documento extraído de la sesión de Elicitación y Red Team del 24/04/2026)*

## El Problema Central
El LLM tiene una alta tendencia a "rellenar" vacíos narrativos inventando relaciones de causa-efecto que no están fundamentadas en la ley.
Aunque los datos duros (fechas, cuotas, meses) que se inyectan a través del `CaseSchemaBuilder` sean precisos (gracias a calcular todo estadísticamente en Python), el modelo generativo (ej. Mistral Large) al interpretar el JSON puede escribir una conclusión absurda. 

**Ejemplo de Alucinación:**
* JSON (Verdad): `{"prestacion": "jubilacion_anticipada", "concedida": false}`
* Texto alucinado: *"La pensión ha sido denegada a Jorge debido a que está casado en régimen de gananciales, lo cual anula el derecho al anticipo."* (El dato "denegada" es correcto, pero la causa inventada jurídicamente es una aberración).

---

## 🛡️ Mi Propuesta de Mitigación en 3 Fases

### 1. Inyección de Rationale Explícito (Restringir la Creatividad)
El LLM inventa motivos ("Causas") cuando el JSON solo suministra los eventos o resultados ("Efectos").

**Solución:** Modificar el `CaseSchemaBuilder.py` y los diccionarios de trampas YAML para incluir siempre el porqué jurídico explícito ("Rationale Obligatorio").
*   **JSON Anterior:** `{"personaje": "Juan", "trampa": "D2", "resultado_it": "Denegada"}`
*   **JSON Nuevo:** `{"personaje": "Juan", "trampa": "D2", "resultado_it": "Denegada", "rationale_obligatorio": "Denegada EXACTAMENTE porque no alcanza el periodo de carencia de 180 días en los últimos 5 años estipulado en el Art. X"}`

**Ajuste del Prompt del Modelo:** *"Tienes PROHIBIDO INVENTAR razones jurídicas para los eventos generados. Estás obligado a parafrasear literalmente el campo `rationale_obligatorio` sin alterar ni expandir la causalidad jurídica expuesta."*

### 2. El Agente "Patcher" (Bucle de Refactorización Quirúrgica)
Si el validador principal (`verification_agents.py` o `prose_validator.py`) levanta un "Causal Issue", el fallo actual asume detener o descartar por completo el borrador del caso (desperdicio alto de tokens/tiempo).

**Solución:**
*   El Juez emite el error detectado en un dict.
*   Paso de la excepción a un `patcher_agent` enfocado únicamente en **arreglar el párrafo defectuoso**.
*   Prompt para este micro-agente: *"En este texto generaste una causalidad falsa: [X]. La ley y los datos dictan: [Y]. Por favor, reescribe solamente esa frase para adaptarla al JSON sin cambiar la longitud del relato."*
*   Este método re-ensambla la redacción de manera escalable, como un cirujano.

### 3. Inyección de Ley vía RAG Inverso Estricto
La otra barrera para el LLM "narrador" es proporcionarle no solo los datos calculados, sino **el contexto legal** con el que debe revestirlo.
*   Antes de delegar la escritura, se extrae del pipeline de Neo4j / MCP el bloque de texto exacto del BOE aplicable a las trampas de ese caso de prueba.
*   Se deposita este texto en el `System Prompt` del escritor como "Texto de Consulta Fijo", lo que provoca que su probabilidad del next-token se ancle firmemente en las frases y la lógica del legislador, sofocando la temperatura creativa de la red neuronal hacia el lado procedimental.

---

> [!TIP]
> Al reducir la responsabilidad interpretativa ("Razonamiento Legal") del agente Narrador al del mero "Traductor de JSON a Párrafo", bloqueamos drásticamente el espacio donde un Transformer de lenguaje puede inventar falacias.
