---
name: workflow-status
description: Lightweight status checker - answers what should I do now? for any agent. Reads YAML status file for workflow tracking. Use workflow-init for new projects.
invokable: true
---

Ejecuta el workflow **workflow-status**.

**Descripción**: Lightweight status checker - answers what should I do now? for any agent. Reads YAML status file for workflow tracking. Use workflow-init for new projects.

**Instrucciones de ejecución**:

1. Lee el archivo completo del workflow: `/home/spas/OPOS_GEMINI_1/.bmad/.bmad/bmm/workflows/workflow-status/workflow.yaml`
2. Sigue TODOS los pasos del workflow en el orden especificado
3. Usa los recursos, templates y datos definidos en el workflow
4. Genera los artefactos en la carpeta de salida configurada

**IMPORTANTE**: NO improvises. Ejecuta el workflow completo tal como está definido.

**Módulo**: bmm
