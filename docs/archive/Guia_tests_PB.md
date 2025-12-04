Guía de Calidad, Seguridad y Despliegue "Bulletproof" para OpositaIA
Esta guía define la estrategia integral para asegurar que el código de OpositaIA sea robusto, seguro y esté listo para producción, respondiendo a tu solicitud de "todo y todo y todo".

1. Estrategia de Revisión de Código y Calidad (Code Review)
Para un proyecto híbrido (React + Python/FastAPI), recomendamos la siguiente combinación de herramientas:

Herramientas Recomendadas
SonarQube (Self-Hosted):

Por qué: Es el estándar de oro para análisis estático. Detecta "code smells", bugs y vulnerabilidades en JS/TS y Python.
Implementación: Correr un contenedor Docker de SonarQube localmente.
Coste: Gratis (Community Edition).
Snyk (Seguridad):

Por qué: Especialista en vulnerabilidades de dependencias (SCA) y código (SAST).
Implementación: CLI local (snyk test) y extensión de VS Code.
Coste: Gratis para proyectos open source/personales (limitado).
Qodo (antes Codium):

Por qué: Excelente para generar tests unitarios automáticamente y explicar código complejo.
Implementación: Extensión de VS Code.
Flujo de Trabajo de Calidad
Pre-Commit (Local):
Husky (Frontend) para correr eslint y prettier antes de cada commit.
Black y Ruff (Backend) para formateo y linting de Python.
Análisis Diario:
Correr escaneo de Snyk semanalmente para detectar nuevas vulnerabilidades en librerías.
2. Estrategia de Testing "A Prueba de Balas"
Frontend (React/Vite)
Unit Testing: Vitest + React Testing Library.
Objetivo: Probar componentes aislados (ej: que 
ModelSelector
 renderice las opciones correctas).
E2E Testing: Playwright.
Objetivo: Simular un usuario real (Login -> Chat -> Respuesta). Es más rápido y fiable que Cypress.
Backend (FastAPI)
Unit Testing: Pytest.
Objetivo: Probar funciones puras (ej: lógica de reranking en 
rag_agent_v2.py
).
Integration Testing: Pytest + TestClient.
Objetivo: Probar endpoints completos (/chat/stream) con base de datos de prueba.
Smoke Tests (Producción)
Scripts ligeros que corren cada hora para verificar que los servicios críticos (Groq, Qdrant, Mistral) responden.
3. Seguridad Ofensiva y Defensiva
Defensiva (Shields Up)
Llama Guard: Implementar un modelo "guardrail" antes del LLM principal para filtrar inputs maliciosos (jailbreaks) y outputs tóxicos.
Rate Limiting: Configurar fastapi-limiter para evitar abusos de API.
Secret Management: NUNCA subir 
.env
 al repo. Usar git-secret o gestores de secretos en CI/CD.
Ofensiva (Red Teaming)
Garak: Herramienta open-source para escanear vulnerabilidades en LLMs (alucinaciones, inyección de prompt, fugas de datos).
Acción: Correr Garak contra tu endpoint de chat.
ZAP (OWASP Zed Attack Proxy): Escaneo de vulnerabilidades web clásicas (XSS, CSRF) en el frontend.
4. Estrategia de Despliegue (Deployment)
Arquitectura Híbrida Optimizada
Frontend: Vercel.
Ventaja: Global CDN, HTTPS automático, CI/CD integrado con GitHub.
Backend: VPS (Hetzner/OVH) + Docker Compose.
Ventaja: Control total, barato para correr Python pesado.
Seguridad: Cloudflare Tunnel para no exponer puertos (8000) a internet. Solo Cloudflare ve tu servidor.
Base de Datos: Supabase (Postgres) o Vercel Postgres.
Ventaja: Gestionado, backups automáticos. No gestiones DBs en Docker para producción si puedes evitarlo.
Pipeline CI/CD (GitHub Actions)
Crear un archivo .github/workflows/main.yml que:

Instale dependencias.
Corra Linter (ESLint/Ruff).
Corra Tests (Vitest/Pytest).
Si todo pasa -> Despliegue automático a Vercel (Frontend) y Reinicio de Docker en VPS (Backend).
5. Plan de Acción Inmediato
Instalar Husky: Asegurar calidad antes de commit.
Configurar Cloudflare Tunnel: Cerrar puertos del VPS ya.
Escribir Tests E2E: Un test crítico que haga todo el flujo (Usuario pregunta -> RAG busca -> LLM responde).
Auditoría Snyk: Correr snyk test en backend y frontend hoy mismo.

