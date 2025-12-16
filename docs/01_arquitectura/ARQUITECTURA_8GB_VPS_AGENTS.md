# 🏗️ ARQUITECTURA "LOW-RESOURCE" PARA VPS 8GB
**Objetivo:** RAG Perfecto + Agentes Locales + Web App sin coste extra.
**Restricción:** 8GB RAM Total.

---

## 1. EL PROBLEMA DE LOS 8GB (Presupuesto de RAM)

| Componente | Consumo Estándar | Consumo Optimizado | Notas |
|------------|------------------|--------------------|-------|
| **Sistema Operativo** | 0.5 GB | **0.3 GB** | Ubuntu Server Minimal |
| **PostgreSQL** | 0.5 GB | **0.2 GB** | `shared_buffers=128MB` |
| **Qdrant (Vector DB)** | 1.0 GB | **0.5 GB** | Storage en Disco (`mmap`) | o api del qdrant cloud
| **Backend (FastAPI)** | 0.5 GB | **0.3 GB** | Workers limitados |
| **Frontend (Serve)** | 0.1 GB | **0.1 GB** | Nginx (Static) |
| **LLM (El "Gordo")** | 5.0 GB | **4.5 GB** | **Phi-3 Mini** o **Mistral v0.3 Q4** |
| **TOTAL** | **7.6 GB** | **5.9 GB** | **VIABLE ✅** |

---

## 2. EL "RAG PERFECTO" (Sin gastar tokens)

Para no depender de LLMs externos (tokens $$$), la búsqueda debe ser tan precisa que el modelo local (más tonto que GPT-4, pero finetuneado!!!!) entienda el contexto a la primera.

### Estrategia: Hybrid Search + Re-ranking Ligero

1.  **Búsqueda Híbrida (Qdrant):**
    *   **Vectores (Semántico):** Encuentra "conceptos" (ej: "jubilación anticipada").
    *   **Keyword (BM25):** Encuentra "términos exactos" (ej: "Art. 161 LGSS").
    *   *Resultado:* Recuperación robusta incluso si el modelo de embeddings falla.

2.  **Re-ranking (Cross-Encoder Local):**
    *   Usar un modelo *diminuto* (`ms-marco-TinyBERT-L-2-v2`, ~100MB RAM) para reordenar los top-10 resultados.
    *   Garantiza que lo que llega al LLM es lo mejor de lo mejor. INVESTIGAR si vale y modelos y si los hay fuera del VPS gratis

3.  **Filtro de Fechas (CRÍTICO):**
    *   **Lógica de Examen:** `WHERE fecha_vigencia <= FECHA_CORTE_EXAMEN`.
    *   El RAG *ignora* leyes posteriores a la convocatoria (evita alucinaciones con leyes nuevas que no entran).

---

## 3. SISTEMA DE AGENTES "MICRO" (Stateless)

En lugar de tener agentes corriendo siempre (comiendo RAM), usamos **Scripts Ejecutables** bajo demanda. no creo que es bueno, pero podemos intentarlo, hay que compararlos dos modos.

### Arquitectura de Agentes
*   **Orquestador:** FastAPI (recibe petición del frontend).
*   **Cola de Tareas:** Redis (muy ligero) + Worker (Python). o clowdflare?
*   **Ejecución:** Solo 1 agente corre a la vez para no saturar la CPU/RAM.

### Catálogo de Agentes (Productos Finales)

#### A. Agente Simulacro (`agent_simulacro.py`)
1.  **Input:** Temas + Nº Preguntas + Fecha Corte.
2.  **Acción:**
    *   Busca en Qdrant preguntas similares (Few-Shot Learning).
    *   Busca en Postgres leyes vigentes a la fecha de corte.
    *   Invoca LLM Local: "Genera 1 pregunta difícil sobre X basada en el Art Y".
3.  **Output:** JSON con preguntas.

#### B. Agente Mapa Mental (`agent_mindmap.py`)
1.  **Input:** Concepto Central.
2.  **Acción:**
    *   Recupera jerarquía de leyes (Títulos/Capítulos) de Postgres.
    *   Invoca LLM Local: "Convierte esta estructura en formato MermaidJS".
3.  **Output:** Código Mermaid para el frontend. y descargable para usar el excalibur!

#### C. Agente "Cante" (Oral Exam) Olvidate de oral!!!!(`agent_oral.py`)
1.  **Input:** Audio del usuario (transcrito por Whisper API o local pequeño a ver si mistarl 7b es capaz, creo que no).
2.  **Acción:**
    *   Compara transcripción con texto literal de la ley.
    *   Calcula % de similitud.
    *   Invoca LLM Local: "Dime qué artículos se ha saltado".
3.  **Output:** Feedback de audio/texto.

---

## 4. SELECCIÓN DE MODELO LOCAL (El Corazón)

Para 8GB de RAM, **Mistral 7B** es arriesgado (puede hacer OOM si hay picos). Por ahora tendremos menos de 50 usuarios, no pasa nada!
NO vamos a cambiar de MODELO! OLVIDATE DEL RESO DE ESTE FICHER!!!- escrito por el usuario!
**Recomendación: Microsoft Phi-3 Mini (3.8B)**
*   **Calidad:** Sorprendentemente cercana a Llama 3 8B en razonamiento.
*   **RAM:** ~2.5 GB (Q4).
*   **Contexto:** 4k (suficiente para RAG preciso).
*   **Ventaja:** Deja 2GB libres para el sistema y caché de disco.

**Alternativa: Qwen 2.5 3B**
*   Muy bueno en español y lógica.
*   Aún más ligero.
los probaremos y los fienetunearemos, si hace falta! 
---

## 5. IMPLEMENTACIÓN INMEDIATA 
!!!lea los docs de VPS ya hay mucho de esto hecho con ssh!!!

### Paso 1: Configurar LLM Server (Llama.cpp)
```bash
# En el VPS
./llama-server -m models/Phi-3-mini-4k-instruct-q4.gguf --port 8080 --host 0.0.0.0 --n-gpu-layers 0
```

### Paso 2: Optimizar Qdrant
```yaml
storage:
  type: mmap # Usa disco, no RAM
optimizers:
  memmap_threshold_kb: 10000
```

### Paso 3: Script de Agente (Ejemplo)
```python
# backend/agents/micro_simulacro.py
import requests

def generar_pregunta(tema):
    # 1. RAG Híbrido
    contexto = qdrant.search(tema, filter={"fecha": {"lte": "2024-01-01"}})
    
    # 2. LLM Local
    prompt = f"Contexto: {contexto}\nGenera una pregunta tipo test difícil."
    resp = requests.post("http://localhost:8080/completion", json={"prompt": prompt})
    
    return resp.json()
```

---

## CONCLUSIÓN
Con esta arquitectura:
1.  **Coste:** 0€ extra (solo el VPS actual).
2.  **Calidad:** RAG Híbrido asegura precisión.
3.  **Estabilidad:** Phi-3 Mini evita caídas por falta de RAM.
4.  **Funcionalidad:** Agentes especializados para cada producto del frontend.
