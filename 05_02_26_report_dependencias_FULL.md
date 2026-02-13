# Inventario Maestro de Infraestructura y Dependencias (05_02_26)

Este documento refleja la **realidad completa** del proyecto OPOSITAIA, incluyendo todos los subsistemas (Python, Node, Docker, AI).

## 1. Mapa de Infraestructura (Docker & Servicios) 🐳
El núcleo del sistema corre sobre contenedores definidos en `docker-compose.yml`.

### Servicios Activos:
*   **PostgreSQL 15 (Alpine)**: Puerto 5432.
    *   *Volume*: `postgres_data`
*   **Qdrant v1.12.0**: Puerto 6333 (Vector DB).
    *   *Volume*: `qdrant_data`
*   **Ollama (Local AI)**: Puerto 11434.
    *   *Modelos*: llama3, mistral, deepseek-r1 (según disponibilidad local).

---

## 2. Subsistema Backend & AI (Python) 🐍
**Gestor de Paquetes:** `pip` en entorno virtual.

### Entornos Virtuales (.venv)
*   **Principal:** `/home/spas/OPOS_GEMINI_1/.venv` (Activo).
*   **Configuración:** `pyvenv.cfg` indica Python 3.12+.

### Dependencias Declaradas (`backend/requirements.txt`):
```text
# FastAPI & Web Framework
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.0
pydantic-settings==2.6.0

# Vector Database
qdrant-client==1.12.0

# Embeddings & LLM
sentence-transformers==3.3.0
ollama==0.4.0

# Gemini & AI Providers
google-generativeai==0.8.0

# Text Processing & RAG
# langchain==0.3.0  # REMOVED: Not used in project (saves ~2GB)
# langchain-community==0.3.0  # REMOVED: Not used in project 
beautifulsoup4==4.12.0
lxml==5.3.0
pypdf==5.1.0
python-docx==1.1.2
tqdm==4.66.0

# BOE API & Web
requests==2.31.0
xmltodict==0.13.0

# Configuration & Utilities
... (truncated)
```

### Variables de Entorno (`backend/.env.backend`):
*   Gestión de secretos para API Keys (Mistral, Groq, DeepSeek, Claude).
*   Configuración de DB (Postgres DSN, Qdrant URL).

---

## 3. Subsistema Frontend (Node.js / React) ⚛️
**Gestor de Paquetes:** `pnpm`.

### Dependencias (`frontend/package.json`):
```text
- @excalidraw/excalidraw: ^0.18.0
- @google/genai: ^1.29.0
- html-to-image: ^1.11.13
- react: ^19.2.0
- react-dom: ^19.2.0
- @testing-library/jest-dom: ^6.5.0
- @testing-library/react: ^16.0.0
- @testing-library/user-event: ^14.5.0
- @types/node: ^22.14.0
- @types/react: ^19.0.0
- @types/react-dom: ^19.0.0
- @typescript-eslint/eslint-plugin: ^8.0.0
- @typescript-eslint/parser: ^8.0.0
- @vitejs/plugin-react: ^5.0.0
- @vitest/coverage-v8: latest
- @vitest/ui: latest
- eslint: ^9.0.0
- eslint-plugin-react: ^7.35.0
- eslint-plugin-react-hooks: ^5.0.0
- jsdom: ^25.0.0
- prettier: ^3.3.0
- typescript: ~5.8.2
- vite: ^6.2.0
- vite-plugin-pwa: ^0.21.1
- vitest: latest
```

---

## 4. Subsistema MCP Server (Node.js) 🔌
Servidor para integración con Claude Desktop / Herramientas externas.
**Gestor de Paquetes:** `pnpm`.

### Dependencias (`mcp-server/package.json`):
```text
- @modelcontextprotocol/sdk: ^0.5.0
- @qdrant/js-client-rest: ^1.9.0
- axios: ^1.6.0
- dotenv: ^16.3.1
- express: ^5.2.1
- @types/express: ^5.0.6
- @types/node: ^20.19.27
- typescript: ^5.3.0
```

---

## 5. Raíz del Proyecto (Orquestación) 🎼
Archivos de configuración global encontrados:
*   `pnpm-lock.yaml`: Indica que se usa pnpm workspaces o monorepo parcial.
*   `.env`: Variables globales del usuario (User Settings).

## 6. Resumen de Tecnologías Detectadas
| Categoría | Tecnologías | Notas |
| :--- | :--- | :--- |
| **Lenguajes** | Python 3.12, TypeScript, SQL | Híbrido |
| **Frameworks** | FastAPI (Backend), Next.js (Frontend), MCP SDK | |
| **Bases de Datos** | PostgreSQL (Relacional), Qdrant (Vectorial) | Dockerizadas |
| **AI / LLMs** | Ollama (Local), Groq, DeepSeek, Mistral, Claude | Multi-Provider |
| **DevOps** | Docker Compose, PNPM, Venv | |

