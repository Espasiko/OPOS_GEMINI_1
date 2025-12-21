# Mapa Arquitectónico del Proyecto OPOSITAIA (21_12_25)

Este documento detalla la estructura física del repositorio, explicando la función de cada carpeta principal y su contenido.

## __pycache__
📂 Carpeta del Proyecto


---
## __tests__
📂 Carpeta del Proyecto

> **Contenido Detectado:** 1 JS/TS files

**Subcarpetas Clave:**
*   `accessibility/`: 1 JS/TS files
*   `integration/`: 2 JS/TS files

---
## ai-specs_no_usar
📂 Carpeta del Proyecto


**Subcarpetas Clave:**
*   `changes/`: 
*   `specs/`: 

---
## backend
🧠 **API Server**: Núcleo FastAPI que conecta con Qdrant (RAG) y PostgreSQL. Maneja usuarios, autenticación y búsquedas.

> **Contenido Detectado:** 🐍 Python Env (requirements.txt), 🐳 Dockerized, 16 Python scripts

**Subcarpetas Clave:**
*   `agents/`: 13 Python scripts
*   `data/`: 
*   `database/`: 2 Python scripts
*   `docs/`: 
*   `examples/`: 
*   `models/`: 1 Python scripts
*   `routers/`: 9 Python scripts
*   `scripts/`: 9 Python scripts
*   `tests/`: 5 Python scripts
*   `utils/`: 2 Python scripts

---
## bmad-custom-modules-src
📂 Carpeta del Proyecto


---
## bmad-custom-src
📂 Carpeta del Proyecto


---
## conceptual_materials
📂 **Textos Base**: Contiene PDFs y textos jurídicos extraídos con OCR (Tesseract) para ser indexados.


**Subcarpetas Clave:**
*   `extracted_texts/`: 
*   `pdfs/`: 17 PDFs
*   `qa_generated/`: 5 JSON datasets

---
## dataset_generator
⚙️ **Motor de IA**: Scripts Python para generar preguntas (QA) y casos prácticos. Aquí viven los scripts de Mistral, DeepSeek y Groq.

> **Contenido Detectado:** 🐍 Python Env (requirements.txt), 47 Python scripts, 3 JSON datasets

**Subcarpetas Clave:**
*   `agents/`: 1 Python scripts
*   `dataset_output/`: 21 JSON datasets
*   `dataset_output_CLEAN/`: 5 JSON datasets
*   `multi_model_20_12/`: 
*   `multi_model_v3_2_20_12/`: 
*   `premium_content/`: 
*   `qa_mistral_batches_20_12/`: 

---
## docs
📚 **Documentación**: Informes técnicos, memorias, y guías de desarrollo (.md).


**Subcarpetas Clave:**
*   `01_arquitectura/`: 
*   `02_planes/`: 
*   `03_investigacion/`: 
*   `04_datasets/`: 
*   `05_sprints/`: 
*   `06_auditorias/`: 
*   `07_sesiones/`: 
*   `08_guias/`: 
*   `09_simulacros/`: 
*   `10_memoria/`: 
*   `11_configuracion/`: 
*   `12_problemas/`: 
*   `13_formato/`: 
*   `14_funciones/`: 3 JSON datasets
*   `Iideas_rama_gemini/`: 
*   `archive/`: 
*   `sprint-artifacts/`: 

---
## extracted_texts
📂 **Staging Area**: Zona temporal donde se guardan los textos procesados antes de ir a Base de Datos (JSONs, TXTs).


**Subcarpetas Clave:**
*   `examenes_oficiales/`: 

---
## frontend
🎨 **UI Web**: Interfaz de usuario React/Next.js para opositores (Tests, Temario, Chat con IA).

> **Contenido Detectado:** 📦 Node Env (package.json), 7 JS/TS files, 4 JSON datasets

**Subcarpetas Clave:**
*   `components/`: 20 JS/TS files
*   `contexts/`: 1 JS/TS files
*   `hooks/`: 1 JS/TS files
*   `services/`: 2 JS/TS files
*   `utils/`: 3 JS/TS files

---
## gastos_ tokens
📂 Carpeta del Proyecto


**Subcarpetas Clave:**
*   `usage_data_2025_11_DEEPSEEK/`: 

---
## golden_dataset
🏆 **Ground Truth**: Preguntas y respuestas verificadas manualmente (Dataset Oro) para evaluación de modelos.


**Subcarpetas Clave:**
*   `consolidated/`: 
*   `premium/`: 1 JSON datasets

---
## mcp-server
🔌 **MCP Gateway**: Servidor de Protocolo de Contexto de Modelo para conectar Claude Desktop con nuestras herramientas locales.

> **Contenido Detectado:** 📦 Node Env (package.json), 1 JS/TS files, 3 JSON datasets

**Subcarpetas Clave:**
*   `dist/`: 4 JS/TS files
*   `src/`: 2 JS/TS files

---
## node_modules
📦 **Librerías Node**: Dependencias instaladas (ignoradas en git).

> **Contenido Detectado:** 1 JSON datasets

---
## powers
📂 Carpeta del Proyecto


**Subcarpetas Clave:**
*   `opositaia-rag/`: 1 JSON datasets

---
## scripts
🛠️ **Utilidades**: Scripts de mantenimiento (backups, limpieza, migraciones).


**Subcarpetas Clave:**
*   `maintenance/`: 14 Python scripts
*   `tests/`: 23 Python scripts, 6 JSON datasets

---
## scripts_20_12
📜 **Legado (Dec 20)**: Scripts de generación específicos de la fase 'Multi-Modelo' (Mistral Agent SDK v1).

> **Contenido Detectado:** 2 Python scripts

---
## vscode_mcp_backup
📂 Carpeta del Proyecto

> **Contenido Detectado:** 2 JSON datasets

**Subcarpetas Clave:**
*   `extension_settings/`: 2 JSON datasets

---

## Archivos en Raíz
*   `.env`: Configuración global de entorno y secretos.
*   `docker-compose.yml`: Orquestador de servicios (Postgres + Qdrant).
*   `pnpm-lock.yaml`: Gestor de dependencias global (Monorepo).
