# Prompts Personalizados para Continue IDE
# Usa estos con el comando /nombre-prompt en Continue Chat

---
name: refactor
description: Refactoriza el código seleccionado manteniendo funcionalidad
---

Refactoriza el código seleccionado para mejorar:
- Legibilidad
- Performance
- Mantenibilidad
- Adherencia a patrones SOLID

Mantén exactamente la misma funcionalidad. Explica los cambios realizados.

---
name: document
description: Genera documentación para el código seleccionado
---

Genera documentación completa para este código incluyendo:
- Descripción de qué hace
- Parámetros (si es función)
- Valor retornado (si es función)
- Ejemplos de uso
- Notas sobre edge cases
- Links a recursos relacionados

Usa formato Markdown.

---
name: test
description: Escribe pruebas unitarias para el código
---

Escribe pruebas unitarias completas para esta función usando Jest.

Las pruebas deben:
- Cubrir casos normales
- Cubrir casos edge
- Cubrir errores y excepciones
- Ser independientes entre sí
- Tener nombres descriptivos

Incluye setup/teardown si es necesario.

---
name: security-review
description: Revisa el código por vulnerabilidades de seguridad
---

Realiza una revisión de seguridad del código seleccionado:
- Inyección SQL/NoSQL
- XSS y CSRF
- Manejo de credenciales
- Validación de entrada
- Autenticación/Autorización
- Dependencias inseguras

Reporta cualquier vulnerabilidad encontrada con:
- Severidad (Crítica, Alta, Media, Baja)
- Descripción
- Cómo arreglarlo

---
name: performance-analysis
description: Analiza performance del código
---

Analiza la performance del código:
- Complejidad temporal (Big O)
- Complejidad espacial
- Bottlenecks potenciales
- Oportunidades de optimización
- Impacto en memoria/CPU

Sugiere mejoras con ejemplos concretos.

---
name: explain
description: Explica qué hace el código
---

Explica el código seleccionado de forma clara:
- Propósito general
- Cómo funciona paso a paso
- Patrones utilizados
- Dependencias externas
- Posibles problemas

Ajusta la complejidad de la explicación según sea necesario.

---
name: rag-integration
description: Integra código con sistema RAG
---

Sugiere cómo integrar este código con el sistema RAG (Qdrant):
- Estructura de embeddings necesaria
- Queries necesarias para búsqueda
- Procesamiento de resultados
- Caching estratégico
- Optimizaciones de latencia

Proporciona código de ejemplo.

---
name: mcp-handler
description: Crea un manejador MCP para esta función
---

Crea un handler MCP (Model Context Protocol) para exponer esta función:
- Define el tool/resource
- Especifica inputs y outputs
- Maneja errores apropiadamente
- Incluye validación

Formato: JSON conforme a spec de MCP.

---
name: api-endpoint
description: Crea un endpoint REST para esta función
---

Crea un endpoint REST para exponer esta funcionalidad:
- Especifica método HTTP (GET, POST, etc)
- Define path del endpoint
- Documentación de payload
- Códigos HTTP de respuesta
- Error handling

Usa express.js o framework preferido.

---
name: async-refactor
description: Convierte a operaciones asincrónicas
---

Convierte este código a operaciones asincrónicas/concurrentes:
- Identifica operaciones I/O
- Usa async/await o Promises
- Implementa manejo de errores
- Considera race conditions
- Optimiza concurrencia

Mejora el performance manteniendo legibilidad.
