# Memoria de Sesión — 13 de Marzo de 2026
## Objetivo: Ejecución de DeepSeek R1 (Protocolo Claude) y Generación V3

### 1. Cambios en el Sistema de Agentes
Hoy se ha realizado una re-ingeniería profunda del motor de agentes para soportar modelos de razonamiento avanzado (DeepSeek R1) manteniendo el rigor legal exigido para el escenario 2026.

- **Protocolo de Ruptura de Certeza (Protocolo Claude):**
    - Se ha reescrito el `system_prompt` de `generator.yaml` siguiendo las directrices de Claude para "romper" la confianza del modelo R1 en su memoria interna (desactualizada).
    - El agente ahora tiene prohibido dar datos numéricos o legales sin antes invocar una `tool` (calculator o search_rag).
    - Se ha implementado en `agent_engine.py` una inyección de mensaje obligatoria para modelos R1 que fuerza la ejecución de las herramientas antes de la petición del usuario.

- **Optimización de Estabilidad y Rendimiento:**
    - **Lazy Loading (Carga Perezosa):** Se detectó que la carga masiva de `torch` y `sentence_transformers` en cada arranque del motor provocaba bloqueos y `KeyboardInterrupt`. Se modificaron `rag_agent_v2.py` y `rag_helper.py` para cargar los modelos solo cuando se realiza la primera búsqueda.
    - **Timeouts Extendidos:** Se aumentó el timeout de HTTP en `llm_providers.py` de 360s a **900s (15 minutos)** para permitir que DeepSeek R1 complete sus largos ciclos de "Thinking" y múltiples llamadas a herramientas sin desconexiones.

- **Corrección de Bugs en el Motor:**
    - Se arregló un bug crítico en `AgentEngine` que ignoraba la estructura anidada del manifest YAML del agente.
    - Se mejoró la resolución de variables `{config.key}` para asegurar que el motor apunte siempre al proveedor correcto.

### 2. Problemas Detectados y Resueltos
- **Falla de Resolución:** El motor hacía fallback a `mistral-small` silenciosamente si la variable del modelo tenía espacios o errores de sintaxis en el YAML. (Solucionado con trazabilidad DEBUG).
- **Interrupciones por Carga:** El sistema era inestable al importar librerías ML de 1GB+ en cada comando. (Solucionado con carga perezosa).
- **Timeouts de Razonamiento:** R1 en casos complejos con muchas herramientas excedía los 10 minutos de proceso. (Solucionado con timeout de 15m).

### 3. Scripts Creados y Ejecutados
- `run_generator_v2.py`: Script principal de generación con forzado de `deepseek-reasoner`.
- `verify_final_logic.py`: Validación pura de la lógica de jubilación e IT para 2026 (Umbral 38.25 y pagadores).
- `run_output_v3_r1_definitive.log`: Reporte de la ejecución final exitosa.

### 4. Estado Final
Se ha generado con éxito el archivo:
`dataset_output/golden_standard_v3_claude_protocol.md`

Este caso incluye:
1. **Jubilación 2026 (Juan):** Aplicación correcta del umbral de cotización 38.25 años.
2. **IT Ana (Enfermedad Común, Día 10):** Identificación del pagador correcto (Empresa vs Seguridad Social).
3. **IT Pedro (Accidente Trabajo, Día 45):** Identificación del pagador y porcentajes correctos.


### 5. Cambios 13 03 26 Sesión Antigravity (Actualización Crítica)
- **Validación Determinística de Calculadoras:**
    - Se ha creado y ejecutado `scripts/tests/test_deterministic_calculators.py` para verificar el núcleo de cálculo sin consumo de tokens.
    - **Jubilación 2026:** Confirmado umbral de **38.25 años** (38 años y 3 meses) para jubilación a los 65 años.
    - **IT Enfermedad Común:** Validado que el pagador del día 4 al 15 es la **Empresa (pago delegado)**.
- **Sincronización del Dispatcher:**
    - Se han corregido las importaciones en `backend/calculators/dispatcher.py` para armonizarlas con las funciones reales de `calculos_ss_extended.py` (eliminando `calcular_jubilacion_demorada` por la nueva escala RDL 11/2024).
- **Ajuste de Fallbacks:**
    - Se ha eliminado el hardcodeo de `día_baja = 15` en el dispatcher, forzando a los agentes a investigar el dato real.

---
**Firmado:** AI Assistant (Antigravity)
**Fecha:** 2026-03-13 18:30
