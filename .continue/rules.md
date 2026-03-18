# Reglas Personalizadas para Continue IDE
# Estas reglas se aplican a todas las interacciones con el agente

## Generales
- Responde siempre en español
- Proporciona explicaciones claras y concisas
- Pregunta si hay ambigüedad en los requisitos

## Código
- Sigue las convenciones de estilo del proyecto
- Prefiere legibilidad sobre compresión
- Añade comentarios para lógica compleja
- Considera performance y seguridad

## Documentación
- Documenta cambios importantes
- Incluye ejemplos prácticos
- Actualiza README cuando sea necesario

## Testing
- Sugiere pruebas unitarias para código nuevo
- Considera casos edge y errores
- Verifica compatibilidad con versiones anteriores

## Seguridad
- NUNCA incluyas credentials o keys en código
- Usa variables de entorno para datos sensibles
- Valida entrada de usuarios
- Revisa dependencias por vulnerabilidades

## Performance
- Prefiere soluciones O(n) sobre O(n²)
- Evita loops anidados cuando sea posible
- Considera memoria y CPU
- Usa lazy loading cuando aplique

## Arquitectura
- Sigue patrones SOLID
- Separa concerns claramente
- Mantén módulos independientes
- Documenta decisiones arquitectónicas

## Específico del Proyecto OPOS GEMINI
- Mantén compatibilidad con RAG (Retrieval-Augmented Generation)
- Integra con sistemas MCP cuando sea posible
- Respeta la estructura de base de datos Qdrant
- Considera latencia en operaciones de búsqueda

## BMAD Method

### Activación de Agentes
- Cuando se invoque un agente BMAD (ej: `/bmad-master`), LEE el archivo del agente completo
- NUNCA improvises el comportamiento de agentes
- Sigue EXACTAMENTE las instrucciones de activación de cada agente
- Respeta la estructura XML y los pasos de activación

### Ejecución de Workflows
- Cuando se invoque un workflow BMAD (ej: `/create-prd`), LEE el archivo del workflow completo
- Sigue TODOS los pasos del workflow en orden
- Usa los recursos y templates definidos en el workflow
- Genera artefactos en la carpeta de salida configurada

### Variables de Configuración
- `{user_name}`: Spas
- `{communication_language}`: Spanish
- `{document_output_language}`: Spanish
- `{output_folder}`: {project-root}/docs
- `{project-root}`: /home/spas/OPOS_GEMINI_1

### Comunicación
- Los agentes BMAD se comunican en **español** (según {communication_language})
- Mantén el carácter y estilo de comunicación de cada agente
- Respeta los menús numerados y la estructura de interacción
