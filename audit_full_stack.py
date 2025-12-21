
import os
import datetime
import pathlib
import json

ROOT = pathlib.Path("/home/spas/OPOS_GEMINI_1")

def get_file_tree():
    # Simulated structure based on 'find' output
    return {
        "ROOT": ["package.json", "pnpm-lock.yaml", "docker-compose.yml", ".env"],
        "Backend (Python)": ["backend/requirements.txt", "backend/Dockerfile", "backend/.env.backend", ".venv/pyvenv.cfg"],
        "Frontend (Node/Next)": ["frontend/package.json", "frontend/pnpm-lock.yaml", "frontend/.env"],
        "MCP Server (Node)": ["mcp-server/package.json", "mcp-server/pnpm-lock.yaml", "mcp-server/.env"]
    }

def read_file_safely(path, limit=20):
    try:
        if not (ROOT / path).exists(): return "*File not found*"
        content = (ROOT / path).read_text()
        if path.endswith("json"):
            # Parse JSON to just get 'dependencies'
            data = json.loads(content)
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            return "\n".join([f"- {k}: {v}" for k,v in deps.items()])
        else:
            lines = content.splitlines()
            return "\n".join(lines[:limit]) + ("\n... (truncated)" if len(lines) > limit else "")
    except Exception as e:
        return f"Error reading: {e}"

def main():
    date_str = datetime.datetime.now().strftime("%d_%m_%y")
    filename = f"{date_str}_report_dependencias_FULL.md"
    
    tree = get_file_tree()
    
    content = f"""# Inventario Maestro de Infraestructura y Dependencias ({date_str})

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
{read_file_safely('backend/requirements.txt', 30)}
```

### Variables de Entorno (`backend/.env.backend`):
*   Gestión de secretos para API Keys (Mistral, Groq, DeepSeek, Claude).
*   Configuración de DB (Postgres DSN, Qdrant URL).

---

## 3. Subsistema Frontend (Node.js / React) ⚛️
**Gestor de Paquetes:** `pnpm`.

### Dependencias (`frontend/package.json`):
```text
{read_file_safely('frontend/package.json')}
```

---

## 4. Subsistema MCP Server (Node.js) 🔌
Servidor para integración con Claude Desktop / Herramientas externas.
**Gestor de Paquetes:** `pnpm`.

### Dependencias (`mcp-server/package.json`):
```text
{read_file_safely('mcp-server/package.json')}
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

"""

    with open(filename, "w") as f:
        f.write(content)
        
    print(f"Report generated: {filename}")

if __name__ == "__main__":
    main()
