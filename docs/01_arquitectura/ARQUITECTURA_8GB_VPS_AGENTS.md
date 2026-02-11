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

## 5. IMPLEMENTACIÓN REAL ✅ VERIFICADA 22/01/2026

### ✅ Estado Actual del VPS

**Conexión SSH:**
```bash
ssh root@147.93.95.67
# Hostname: srv838554
# Usuario app: ubuntu
```

**Recursos disponibles:**
- RAM: 7.8 GB total (6.0 GB usados, 1.7 GB libres)
- Disco: 96 GB total (26 GB usados, 71 GB libres)
- Swap: 2.0 GB

### ✅ Paso 1: LLM Server (Llama.cpp) - YA CONFIGURADO

**Servicio activo:** `llama-server.service`

```bash
# Ver estado
ssh root@147.93.95.67 "systemctl status llama-server.service"

# Configuración actual (NO CAMBIAR):
# Comando: /usr/local/bin/llama-server
# Modelo: /home/ubuntu/models/salamandra-7b-instruct-Q4_K_M.gguf (4.6 GB)
# Puerto: 8080 (público en 0.0.0.0)
# Contexto: 8192 tokens
# Memoria: ~5.7 GB
```

**Endpoints disponibles:**
```bash
# Interno (desde VPS)
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/v1/models

# Externo (vía nginx HTTPS)
curl https://electroyhogarpelotazo.tienda/v1/models
curl https://electroyhogarpelotazo.tienda/v1/chat/completions
```

### ✅ Paso 2: FastAPI Wrapper - YA CONFIGURADO

**Servicio activo:** `salamandra-api.service`

```bash
# Ver estado
ssh root@147.93.95.67 "systemctl status salamandra-api.service"

# Configuración:
# Directorio: /home/ubuntu/salamandra-api/
# Puerto: 8001 (solo localhost)
# Memoria: ~37 MB
```

**Endpoints públicos (vía nginx):**
```bash
# Health check
curl https://electroyhogarpelotazo.tienda/health

# Swagger UI
https://electroyhogarpelotazo.tienda/docs

# Razonamiento con Salamandra
curl -X POST https://electroyhogarpelotazo.tienda/salamandra/reason \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuál es el plazo de IT por EC?",
    "context": "Art. 173 LGSS...",
    "options": {"a": "365 días", "b": "545 días"}
  }'
```

### ⚠️ Paso 3: CORRECCIÓN NECESARIA

**Problema detectado:** El código de `salamandra-api` intenta llamar a Ollama (puerto 11434) que NO está instalado.

**Solución:**
```bash
# Conectar al VPS
ssh root@147.93.95.67

# Editar el archivo
nano /home/ubuntu/salamandra-api/main.py

# Cambiar línea 48:
# DE:   "http://127.0.0.1:11434/v1/chat/completions"
# A:    "http://127.0.0.1:8080/v1/chat/completions"

# Cambiar línea 38:
# DE:   "model": "salamandra-opos:optimized"
# A:    "model": "salamandra-7b-instruct-Q4_K_M.gguf"

# Cambiar línea 60 (opcional, para consistencia):
# DE:   "model_used": "salamandra-opos:optimized"
# A:    "model_used": "salamandra-7b-instruct-Q4_K_M.gguf"

# Reiniciar servicio
systemctl restart salamandra-api.service
```


### ✅ Paso 4: Script de Agente (Ejemplo Real)

```python
# backend/agents/micro_simulacro.py
import requests

def generar_pregunta(tema):
    # 1. RAG Híbrido (Qdrant Cloud o local)
    contexto = qdrant.search(tema, filter={"fecha": {"lte": "2024-01-01"}})
    
    # 2. LLM en VPS (Salamandra vía HTTPS)
    payload = {
        "question": f"Genera una pregunta tipo test difícil sobre: {tema}",
        "context": contexto,
        "options": {"a": "", "b": "", "c": "", "d": ""}
    }
    
    resp = requests.post(
        "https://electroyhogarpelotazo.tienda/salamandra/reason",
        json=payload,
        timeout=300
    )
    
    return resp.json()

# Alternativa: Llamar directamente a llama.cpp
def generar_con_llamacpp(tema, contexto):
    payload = {
        "model": "salamandra-7b-instruct-Q4_K_M.gguf",
        "messages": [
            {"role": "system", "content": "Eres experto en oposiciones españolas."},
            {"role": "user", "content": f"Contexto: {contexto}\n\nGenera pregunta sobre: {tema}"}
        ],
        "temperature": 0.1,
        "max_tokens": 1000
    }
    
    resp = requests.post(
        "https://electroyhogarpelotazo.tienda/v1/chat/completions",
        json=payload,
        timeout=300
    )
    
    return resp.json()
```

### 📋 Comandos de Verificación

```bash
# Verificar servicios activos
ssh root@147.93.95.67 "systemctl list-units --type=service --state=running | grep -E 'llama|salamandra'"

# Ver uso de recursos
ssh root@147.93.95.67 "free -h && df -h | grep -E 'Filesystem|/$'"

# Ver procesos de IA
ssh root@147.93.95.67 "ps aux | grep -E 'llama-server|uvicorn' | grep -v grep"

# Test completo
curl https://electroyhogarpelotazo.tienda/health
curl https://electroyhogarpelotazo.tienda/v1/models
```

---

## CONCLUSIÓN - ESTADO REAL ✅

### ✅ Lo que YA funciona (Verificado 22/01/2026):

1. **Coste:** 0€ extra (solo el VPS de Hostinger ya pagado)
2. **Modelo:** Salamandra 7B Q4_K_M (4.6 GB) corriendo en llama.cpp
3. **Estabilidad:** Sistema estable con 1.7 GB RAM libres (22% margen)
4. **Endpoints HTTPS:** Accesibles vía `electroyhogarpelotazo.tienda`
5. **Certificado SSL:** Válido (Let's Encrypt)

### 🔧 Correcciones Necesarias:

1. **Arreglar salamandra-api:** Cambiar puerto 11434 → 8080 (Ollama no existe)
2. **Actualizar nombre del modelo:** `salamandra-opos:optimized` → `salamandra-7b-instruct-Q4_K_M.gguf`
3. **Limpiar servicio roto:** Deshabilitar `opositor-api.service`

### 📋 Quick Start - Usar Salamandra AHORA:

```python
import requests

# Opción 1: Vía FastAPI wrapper (una vez corregido)
response = requests.post(
    "https://electroyhogarpelotazo.tienda/salamandra/reason",
    json={
        "question": "¿Cuál es el plazo de IT por EC?",
        "context": "Art. 173 LGSS: La IT por EC dura máximo 365 días prorrogables 180 más.",
        "options": {"a": "365 días", "b": "545 días", "c": "730 días"}
    },
    timeout=300
)

# Opción 2: Directo a llama.cpp (funciona YA)
response = requests.post(
    "https://electroyhogarpelotazo.tienda/v1/chat/completions",
    json={
        "model": "salamandra-7b-instruct-Q4_K_M.gguf",
        "messages": [
            {"role": "system", "content": "Eres experto en legislación española."},
            {"role": "user", "content": "Pregunta sobre IT..."}
        ],
        "temperature": 0.1,
        "max_tokens": 1000
    },
    timeout=300
)
```

### 📊 Arquitectura Real Simplificada:

```
Local (tu laptop)
    ↓ HTTPS
electroyhogarpelotazo.tienda (Nginx)
    ├─→ /salamandra/reason → FastAPI (puerto 8001) → llama.cpp (8080)
    └─→ /v1/* → llama.cpp directo (puerto 8080)
                    ↓
            Salamandra 7B Q4_K_M (4.6 GB)
```

### 🎯 Próximos Pasos:

1. **Aplicar correcciones** (5 minutos)
2. **Integrar RAG** con Qdrant Cloud
3. **Crear agentes** especializados (simulacro, mapas mentales, etc.)
4. **Fine-tuning** de Salamandra con dataset validado

### 📖 Documentación Completa:

Ver archivo detallado: [`VPS_CONEXION_REAL_22_01_26.md`](file:///home/spas/OPOS_GEMINI_1/docs/01_arquitectura/VPS_CONEXION_REAL_22_01_26.md)

---

**Última actualización:** 22/01/2026 16:28 CET  
**Estado:** ✅ Operativo (con correcciones menores pendientes)  
**Conexión SSH:** `ssh root@147.93.95.67`  
**Dominio:** `https://electroyhogarpelotazo.tienda`

