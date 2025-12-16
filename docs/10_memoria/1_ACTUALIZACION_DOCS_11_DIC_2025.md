# 📝 ACTUALIZACIÓN DOCUMENTACIÓN - 11 DICIEMBRE 2025

**Estado del Proyecto:** 🟢 ACTIVO - FASE DE CONSOLIDACIÓN RAG

---

## 1. 🏗️ ARQUITECTURA ACTUAL (REAL)

### Infraestructura Híbrida
*   **VPS (147.93.95.67):**
    *   **LLM Principal:** Mistral 8B (vía Ollama/Llama.cpp) en puerto 8001/11434.
    *   **Función:** Inferencia pesada y acceso remoto.
*   **Entorno Local (WSL/Laptop):**
    *   **LLM Local:** Ollama (`mistral:latest`) en puerto 11434.
    *   **Vector DB:** Qdrant (Docker) en puerto 6333.
        *   *Colección:* `opositaia_knowledge`
        *   *Embeddings:* `pablosi/bge-m3-spa-law-qa-trained-2` (1024 dims).
    *   **Base de Datos:** PostgreSQL (Docker) en puerto 5432.
    *   **Backend:** FastAPI (Python).

### Componentes Clave
*   **Ingesta:** Script `ingest_boe_4layers_extended.py` con **Smart Chunking** (BeautifulSoup) para respetar estructura de artículos.
*   **RAG:** Búsqueda semántica en Qdrant + Generación con Mistral.
*   **Frontend:** React (Pendiente de integración final con nuevo backend).

---

## 2. ✅ LOGROS RECIENTES (Últimas 24h)

1.  **Smart Chunking Implementado:**
    *   Se ha sustituido el chunking arbitrario por un parseo inteligente de XML del BOE.
    *   Ahora se extraen `<articulo>` individuales, mejorando drásticamente la precisión del contexto legal.
    *   *Fallback:* Si el XML no tiene estructura, se usa chunking simple.

2.  **Limpieza de Datos (Data Quality):**
    *   Identificadas y aisladas ~15 leyes con errores 404 en la API del BOE (ver `docs/LEYES_PENDIENTES_SCRAPING.md`).
    *   La ingesta automática ahora corre sin interrupciones.

3.  **Verificación RAG:**
    *   Script de prueba `test_rag_mistral.py` creado.
    *   Conexión Qdrant <-> Embeddings <-> Ollama verificada.

---

## 3. 📋 PLAN DE ACCIÓN INMEDIATO (ROADMAP)

### Fase 1: Consolidación (En curso)
- [x] Reparar script de ingesta.
- [x] Validar RAG local.
- [ ] Scraping manual de leyes en cuarentena (SMI 2024, ETT, etc.).
- [ ] Actualizar `MEGA_PLAN` e Índices.

### Fase 2: Expansión de Dataset
- [ ] Generar 1,000 pares Q&A usando el sistema multi-agente.
- [ ] Validar calidad con `agent_judge`.

### Fase 3: Producto Final
- [ ] Integrar "Agente Simulacro" y "Agente Mapa Mental" en la Web App.
- [ ] Desplegar versión beta para usuarios de prueba.

---

## 4. 🛡️ REGLAS DE SEGURIDAD Y MEJORES PRÁCTICAS

1.  **Embeddings:** SIEMPRE usar `pablosi/bge-m3-spa-law-qa-trained-2`. No mezclar con `all-minilm`.
2.  **Modelos:** Preferir modelos cuantizados (Q4_K_M) para latencia/memoria en local.
3.  **Datos:** Las leyes fallidas (404) NO deben ser ignoradas, sino procesadas por vía alternativa (Scraping/OCR).
4.  **Agentes:** Diseño *stateless* para minimizar consumo de RAM. Ejecución bajo demanda.

---

**Nota:** Este documento reemplaza a las actualizaciones del 5 de diciembre y sirve como nueva fuente de verdad para el estado del sistema.
