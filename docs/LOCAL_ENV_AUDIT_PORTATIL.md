# 🖥️ Auditoría Entorno Técnico – Portátil (WSL)

Fecha: 9 de diciembre de 2025

## 1. Hardware detectado (dentro de WSL)

- **CPU**: Intel Core Ultra 5 125U (14 hilos, 7 cores lógicos en WSL, 1 socket)
- **Arquitectura**: x86_64, 64‑bit
- **RAM total (host visible desde WSL)**: ~15 GiB
  - Usada al momento de la auditoría: ~9.1 GiB
  - Libre: ~4.9 GiB
- **Swap (host)**: 8 TiB configurados virtualmente por WSL (no es RAM física real, pero ayuda a evitar OOM)
- **Disco**:
  - WSL root (`/`): ~1 TB (dispositivo `/dev/sdd`), 25% usado (230G usados / 726G libres)
  - Disco C: 444G totales, 331G libres (26% usado)
  - Disco D: 932G totales, 436G libres (54% usado)

**Conclusión hardware**: portátil equilibrado con buena CPU multi‑hilo y 15 GiB de RAM compartidos con Windows. Suficiente para:
- Qdrant local
- Backend FastAPI
- Frontend dev server
- Modelos Ollama ligeros y de tamaño medio (ej. Mistral 7B cuantizado) si se gestiona bien la RAM

Para modelos gigantes (70B) o entrenos intensivos, sigue siendo mejor usar VPS/Cloud.

---

## 2. GPU / VRAM

Comando `nvidia-smi` dentro de WSL:

- Resultado: `no-nvidia` (comando no disponible, se sugiere instalar `nvidia-utils-XXX`)

Interpretación probable:
- Esta instancia WSL no tiene una GPU NVIDIA conectada/visible.
- O la GPU no está compartida desde Windows hacia WSL.

**Conclusión GPU**:
- No se puede asumir acceso a GPU tipo CUDA desde WSL ahora mismo.
- Cualquier carga pesada de entrenamiento/fine‑tuning (ej. Unsloth + Mistral 7B) debe hacerse en **Colab/VPS** como ya contempla el mega‑plan.
- Para inferencia local, Ollama funcionará en CPU (más lento pero viable con modelos cuantizados).

---

## 3. Ollama local

Salida:

```bash
/usr/local/bin/ollama

NAME                       ID              SIZE    MODIFIED
nomic-embed-text:latest    0a109f422b47    274 MB  3 months ago
mistral:latest             6577803aa9a0    4.4 GB  3 months ago
```

- **Ollama está instalado** en `/usr/local/bin/ollama` (visible desde WSL).
- Modelos presentes:
  - `nomic-embed-text:latest` (~274 MB)
  - `mistral:latest` (~4.4 GB)

**Conclusión Ollama**:
- Ya puedes usar Ollama para:
  - Embeddings con `nomic-embed-text`.
  - LLM general `mistral` como modelo principal para agente local.
- Encaja perfectamente con tu estrategia de:
  - Tier 1: TinyLlama (si decides descargarlo después)
  - Tier 2: Mistral (este `mistral:latest`)
  - Tier 3: Gemini/Groq/Cloud para casos complejos.

---

## 4. Docker y contenedores activos

Salida:

```bash
Docker version 27.5.1

CONTAINER ID   IMAGE                               COMMAND                  STATUS                   PORTS
7622c641f1cd   ghcr.io/simstudioai/simstudio:latest   ...   Up (healthy)   0.0.0.0:3000->3000/tcp
8974ed9dec3e   ghcr.io/simstudioai/realtime:latest   ...   Up (healthy)   0.0.0.0:3002->3002/tcp
34c8fe2c7a99   pgvector/pgvector:pg17                ...   Up (healthy)   0.0.0.0:5432->5432/tcp
```

- **Docker está instalado y operativo** dentro de WSL.
- Actualmente hay contenedores corriendo: SimStudio (puertos 3000, 3002) y PostgreSQL con `pgvector` en 5432.

**Conclusión Docker**:
- El portátil está preparado para levantar servicios adicionales en Docker si lo necesitas (por ejemplo, Qdrant en contenedor).
- Ojo a puertos ocupados (3000, 3002, 5432 ya en uso por otro stack), pero puedes usar otros puertos (ej. 8000 para FastAPI, 6333 para Qdrant, 5173/4173 para Vite, etc.).

---

## 5. Python y paquetes

Salida resumida:

```bash
Python 3.12.3

Name: requests
Version: 2.31.0
Location: /usr/lib/python3/dist-packages
```

- **Python 3.12.3 instalado** a nivel sistema.
- Paquete `requests` está presente.
- No se ha verificado aún en este comando si `qdrant-client` y `python-dotenv` están en el **venv del proyecto** (recomendado crearlo y usarlos allí).

**Recomendación Python para el proyecto**:

1. Crear un entorno virtual en la raíz del repo:
   ```bash
   cd /home/spas/OPOS_GEMINI_1
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instalar dependencias mínimas para RAG local + scripts dataset:
   ```bash
   pip install qdrant-client python-dotenv requests fastapi uvicorn[standard]
   ```

3. Usar siempre este venv para ejecutar:
   - `backend` (FastAPI)
   - scripts tipo `dataset_generator/generar_qa_deepseek.py`

---

## 6. Node, npm y pnpm

Salida:

```bash
node -v   # v22.17.1
npm -v    # 10.9.2
pnpm -v   # 10.19.0
```

- **Node.js**: v22.17.1 (muy reciente, suficiente para Vite/React, etc.).
- **npm** disponible.
- **pnpm** ya instalado (v10.19.0).

**Conclusión stack JS**:
- Estás preparado para utilizar **pnpm** como gestor principal en frontend (lo que mejora espacio y velocidad), siempre que lo dejes claro en la documentación y scripts.
- El mega‑plan no se rompe por usar pnpm; es una decisión de ergonomía. Puedes migrar progresivamente:
  - Actualizar `README`/docs de frontend para decir "usar pnpm".
  - Sustituir comandos `npm install` por `pnpm install` en tus guías.

---

## 7. Resumen de capacidades locales

- **CPU**: suficiente para RAG 4 capas + backend + agentes + indexaciones moderadas.
- **RAM**: 15 GiB, razonable para Qdrant local + backend + Mistral 7B en Ollama (cuantizado), sin excederse en concurrencia.
- **GPU**: no visible en WSL → entrenamiento pesado siempre en Colab/VPS (como dice el mega‑plan).
- **Ollama**: instalado con `mistral:latest` y `nomic-embed-text` → perfecto para agente local + embeddings.
- **Docker**: operativo, ya usado para otros servicios → viable para Qdrant local o servicios auxiliares.
- **Python 3.12**: correcto; falta consolidar un venv del proyecto y paquetes específicos.
- **Node/npm/pnpm**: stack moderno; pnpm listo si decides adoptarlo oficialmente.

---

## 8. Recomendaciones prácticas alineadas con el mega‑plan

1. **Definir venv del proyecto** y documentarlo en un `BACKEND_SETUP.md` o similar.
2. **Decidir Qdrant local vs Cloud** para este portátil:
   - Local en Docker si prefieres control total.
   - Cloud si quieres simplificar el portátil.
3. **Mantener fine‑tuning en Colab** (sin cambios): sin GPU en WSL, no tiene sentido moverlo local.
4. **Estandarizar gestor JS (pnpm)** si lo adoptas: actualizar docs de frontend.
5. **Usar este informe** como referencia rápida para que agentes/LLMs sepan qué se puede ejecutar en local sin reventar el portátil.
