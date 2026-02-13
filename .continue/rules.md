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
