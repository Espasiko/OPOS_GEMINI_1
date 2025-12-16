# 🛡️ GUÍA DE SEGURIDAD Y MEJORES PRÁCTICAS DE DESARROLLO (BMAD)

**Contexto:** Desarrollo de Agentes IA para OpositaIA
**Fecha:** 11 Diciembre 2025

---

## 1. PRINCIPIOS DE SEGURIDAD

### A. Gestión de Secretos
*   **NUNCA** hardcodear claves API, contraseñas o tokens en el código fuente.
*   Usar siempre variables de entorno (`.env`) cargadas con `python-dotenv`.
*   El archivo `.env` debe estar en `.gitignore`.

### B. Validación de Inputs (Prompt Injection)
*   Los agentes deben validar y sanitizar la entrada del usuario antes de enviarla al LLM.
*   Limitar la longitud de los inputs para evitar ataques de denegación de servicio (DoS) o consumo excesivo de tokens.
*   Usar delimitadores claros en los prompts (ej. `"""Contexto"""`) para separar instrucciones de datos.

### C. Privacidad de Datos
*   No enviar datos personales identificables (PII) a LLMs externos si no es estrictamente necesario.
*   En arquitectura local (Ollama), los datos no salen del perímetro, pero se deben tratar con cuidado en los logs.

---

## 2. ESTÁNDARES DE DESARROLLO (PYTHON/AGENTS)

### A. Arquitectura de Agentes
*   **Stateless:** Los agentes deben ser "sin estado" siempre que sea posible. Reciben contexto, procesan y devuelven respuesta. El estado se guarda en BD (Postgres), no en memoria del agente.
*   **Modularidad:** Cada agente debe tener una responsabilidad única (ej. `IngestAgent`, `QuizAgent`, `ChatAgent`).
*   **Tipado:** Usar `Type Hints` (Python 3.10+) en todas las funciones.

### B. Manejo de Errores
*   Implementar bloques `try/except` específicos.
*   Los agentes nunca deben fallar silenciosamente. Deben devolver un error estructurado o un mensaje de "No sé" elegante.
*   **Logging:** Usar el módulo `logging` estándar. Niveles: `INFO` para flujo normal, `ERROR` para fallos, `DEBUG` para desarrollo.

### C. Ingesta y RAG
*   **Embeddings:** Usar SIEMPRE `pablosi/bge-m3-spa-law-qa-trained-2` para mantener consistencia vectorial.
*   **Chunking:** Respetar la estructura lógica del documento (Artículos, Capítulos) usando `BeautifulSoup` o similar. No cortar frases a la mitad.
*   **Metadatos:** Cada vector debe tener metadatos ricos (`boe_id`, `fecha`, `titulo`, `articulo_id` y mas) para permitir filtrado preciso.
*   **SOLAPAMIENTO** Se debe implementar un pequeño solapamiento para no perder el sentido de los documentos largos, aunque este seccionado por articulos y titulos.

---
---
## comprobaciones y tests 
## avisos al usuario antes de subir y despues de crear sprints

*    Siempre comprobar si lo creado se ha testado
*    avisar al usuario de los resultados del test o si no se ha hecho! 
----    

## 3. WORKFLOW 
DE GIT Y DESPLIEGUE

### A. Commits
*   Mensajes claros y descriptivos: `feat: añadir agente de simulacro`, `fix: error 404 en ingesta`.
*   No subir archivos grandes (>100MB) ni binarios innecesarios.

### B. Docker
*   Los servicios deben estar contenerizados (`docker-compose.yml`).
*   Usar volúmenes para persistencia de datos (Qdrant, Postgres).
*   Optimizar imágenes (usar versiones `slim` o `alpine` cuando sea posible).
*    Comprobar la red docker  y adecuada
---

## 4. LISTA DE VERIFICACIÓN (CHECKLIST) ANTES DE MERGE

- [ ] ¿El código tiene Type Hints?
- [ ] ¿Se han manejado las excepciones (API errors, timeouts)?
- [ ] ¿No hay claves hardcodeadas?
- [ ] ¿El agente usa el modelo de embeddings correcto?
- [ ] ¿Se ha probado localmente con `test_rag_mistral.py` o similar?
