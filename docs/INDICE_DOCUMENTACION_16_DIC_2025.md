# 📚 ÍNDICE MAESTRO DE DOCUMENTACIÓN - 31 DIC 2025

**Proyecto:** OpositaIA  
**Estado:** 🟢 VPS DESPLEGADO + SALAMANDRA OPERATIVO + ARQUITECTURA DISTRIBUIDA  
**Última actualización:** 31 Diciembre 2025

---

## 🌟 FUENTE DE VERDAD (LEER PRIMERO)

| Documento | Ubicación | Descripción |
|-----------|-----------|-------------|
| **MEGA_PLAN_ACTUALIZADO_COMPLETO.md** | `docs/02_planes/` | Plan Maestro v3.0 (VPS + Distribuido) |
| **PLAN_ARQUITECTURA_DISTRIBUIDA_2025.md** | `docs/` | Nueva estrategia: Vercel + Supabase + VPS |
| **26_12_ESTRATEGIA_FINAL_RAG.md** | `Raíz` | Reglas de verificación y diseño técnico del Buscador |
| **RAG_COST_ANALYSIS.md** | `docs/` | Estudio de costes ($0/mes) que justifica el diseño |

---

## 🚀 ESTADO DE INFRAESTRUCTURA (31/12/2025)

### ✅ Completado (VPS Hostinger)
*   **Modelo:** `salamandra-7b-instruct-unsloth.Q4_K_M.gguf` (4.6GB) en `/home/ubuntu`
*   **Motor:** Ollama (Systemd Service, Puerto 11434)
*   **API:** Opositor-Agent (FastAPI) conectado a Ollama local
*   **Seguridad:** Puertos 8080/8000 cerrados (Zombie matado), solo SSH y Web.

---

## 📁 ESTRUCTURA DE DOCUMENTACIÓN ACTUALIZADA

### 01_arquitectura/
- `ARQUITECTURA_8GB_VPS_AGENTS.md` - (Referencia Histórica VPS)

### 02_planes/ (ESTRATÉGICOS)
- **`MEGA_PLAN_ACTUALIZADO_COMPLETO.md`** - **PLAN MAESTRO V3.0** ⭐
- `SPECS_PRODUCTO_FINAL.md` - Especificaciones de Producto (Funcionalidades)
- `ROADMAP_RESUMEN_EJECUTIVO.md` - Visión global

### 03_investigacion/
- `INVESTIGACION_FORMATO_OPOSICIONES_OFICIAL.md` - Formato BOE-A-2024-11403
- `PARTY_MODE_SCAMPER_ANALYSIS.md` - Ideas creativas (Gamificación)

### 04_datasets/ & dataset_generator/
- `dataset_generator/INSTRUCCIONES_MODELO_OLLAMA.md` - Guía de Prompting
- `dataset_generator/GUIA_VERIFICACION_QA_AVANZADA.md` - Protocolos de Calidad
- `23_12_MEMORIA_SCRIPTS_OPTIMIZADOS.md` - Memoria Técnica de Generación

### 08_guias/
- `GUIA_SEGURIDAD_DESARROLLO_AGENTES.md` - Seguridad
- `INDICE_DOCUMENTACION_11_DIC_2025.md` - (Actualizado a 31 Dic)

### 10_memoria/
- `MEMORIA_15_12_KIRO.md` - Estado MCP anterior
- `26_12_ANALISIS_PILOTO_Y_PLAN_FASE3.md` - Resultados Piloto

---

## 🔧 MCP OPOSITAIA - ESTADO ACTUAL

**Herramientas MCP Activas:**
1. `search_rag` - Búsqueda semántica (Qdrant)
2. `verify_boe` - Verificación de vigencia
3. `ingest_new_law` - Ingesta de leyes

**Modelo Embeddings:** `pablosi/bge-m3-spa-law-qa-trained-2` (1024 dims)

---

## 📝 NOTAS DE EJECUCIÓN (31 DIC)

1.  **Frontend:** Se inicia desarrollo en **Next.js + Tailwind** (Fase D).
2.  **Base de Datos:** Migración programada a **Supabase** (Fase A).
3.  **Vectores:** Migración programada a **Qdrant Cloud** (Fase B).
4.  **VPS:** Exclusivo para inferencia Salamandra (Fase C).

---

**Creado:** 16 Diciembre 2025 (Actualizado 31/12/2025)