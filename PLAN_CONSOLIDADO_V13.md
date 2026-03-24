# PLAN CONSOLIDADO - VERSIÓN 13 (OPOSITAIA)

Este documento centraliza la estrategia de mejora para la V13, integrando las críticas de Claude, la metodología pedagógica de Diego de Miguel y la auditoría técnica realizada los días 13 y 14 de marzo de 2026.

## 1. Núcleo Estratégico: Críticas de Claude y Respuesta V13
Basándonos en el documento `resumen_criticas_y_metodo_V13.md`, el sistema debe corregir:

*   **RAG Estricto:** Implementar filtrado dinámico por fecha y vigencia para evitar el uso de normativa derogada o transitoria (DANA RDL 11/2024).
*   **Precisión 2026:** El umbral de jubilación se fija en **38.25 años (38 años y 3 meses)**.
    *   > [!IMPORTANT]
    *   **Fecha Límite AGE/SS:** Consultar umbrales específicos solo hasta el **04/03/2026** para la inyección de contexto.
*   **Dispatcher (Error E8):** Eliminación definitiva del sesgo del "día 15" en cálculos de IT.
*   **Protocolo Claude:** Forzar el uso de herramientas (`verify_boe`, `dispatcher`, `rag_search`) ANTES de que el modelo gene una respuesta razonada.

## 2. Metodología Pedagógica (Método Diego de Miguel)
Para replicar el nivel de las mejores academias, la V13 integrará:
*   **Fase 0 de Consulta Obligatoria:** Antes de escribir la trama del caso, el agente debe verificar las constantes del año solicitado.
*   **Trampas de Doble Capa:** Diseño de casos donde la respuesta obvia es un distractor basado en una excepción oculta.
*   **Explicaciones Psicológicas:** No solo dar la respuesta correcta, sino explicar por qué el alumno falló si marcó la trampa.

## 3. Documentación y Auditoría Consultada
Este plan es el resultado de la revisión y actualización de los siguientes documentos clave:

*   **[SINTESIS_PLAN_DEFINITIVO](file:///home/spas/.gemini/antigravity/brain/73b0d458-fe80-4e40-a5ba-6e978ea39346/SINTESIS_PLAN_DEFINITIVO.md):** Mapa general del proyecto.
*   **[AUDITORIA_IMPLEMENTADO_VS_DISEÑO](file:///home/spas/.gemini/antigravity/brain/73b0d458-fe80-4e40-a5ba-6e978ea39346/AUDITORIA_IMPLEMENTADO_VS_DISEÑO.md):** Comparativa técnica de deudas del sistema.
*   **[13_03_26_deepseekV3_memoria.md](file:///home/spas/OPOS_GEMINI_1/13_03_26_deepseekV3_memoria.md):** Grafo de memoria actualizado hoy con el "Protocolo Claude".
*   **[implementation_plan_v13.md](file:///home/spas/.gemini/antigravity/brain/73b0d458-fe80-4e40-a5ba-6e978ea39346/implementation_plan_v13.md):** El plan de desarrollo técnico actual.
*   **[PLAN_13_03_DEFINITIVO.md](file:///home/spas/OPOS_GEMINI_1/PLAN_13_03_DEFINITIVO.md):** Documento persistente de la sesión.
*   **[resumen_criticas_y_metodo_V13.md](file:///home/spas/.gemini/antigravity/brain/73b0d458-fe80-4e40-a5ba-6e978ea39346/resumen_criticas_y_metodo_V13.md):** Análisis profundo de las críticas de Claude.
*   **[plan_pruebas_max.md](file:///home/spas/.gemini/antigravity/brain/73b0d458-fe80-4e40-a5ba-6e978ea39346/plan_pruebas_max.md):** Verificación determinística de calculadoras.
*   **[walkthrough_v13_ss.md](file:///home/spas/.gemini/antigravity/brain/73b0d458-fe80-4e40-a5ba-6e978ea39346/walkthrough_v13_ss.md):** Resumen de pruebas ejecutadas satisfactoriamente.

---
**Firmado:** Antigravity (Bmad Agent) - 14/03/2026
