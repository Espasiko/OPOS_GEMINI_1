# 🧠 MEMORIA TÉCNICA: BASE DE DATOS & RAG (01/01/2026)

**Estado:** Auditoría Forense Realizada  
**Objetivo:** Identificar activos reutilizables y validar alucinaciones.

---

## 1. 🕵️‍♂️ VERIFICACIÓN "ALUCINACIÓN" (STS 15/03/2023)

**La Cita:** "STS 15/03/2023 sobre indemnización interinos".  
**El Veredicto:** ⚠️ **SEMI-ALUCINACIÓN (TIC - True in Context, False in Direction)**.

*   **Lo Real (✅):** Existe la **Sentencia del TS 926/2023 de 15 de marzo**. El tema ES "indemnización de funcionarios interinos".
*   **Lo Falso (❌):** El modelo dijo que "puede considerarse nulo... y aplica indemnización". **La sentencia real DESESTIMÓ** el recurso, alineándose con el TJUE en que la normativa española (no indemnizar) no es contraria a la UE salvo abuso flagrante demostrado.
*   **Conclusión:** El modelo acertó la fecha y el tema (increíble para un 7B), pero "alucinó" una interpretación favorable al trabajador (sesgo común en LLMs afinados con datos web pro-laborales).

---

## 2. 🗄️ AUDITORÍA POSTGRESQL (Local)

Hemos encontrado el "Tesoro Perdido": la tabla **`leyes_catalogo`**.

### Tablas Críticas Detectadas:
1.  **`leyes_catalogo` (EL CATÁLOGO REAL):** 
    *   Contiene la metadata oficial.
    *   **Uso:** Ideal para que el Agente "Researcher" valide fechas de vigencia sin buscar en Google.
2.  **`laws`:** Contenido texto plano de las leyes (backup del vector store).

**Recomendación:** No borrar. Usar `leyes_catalogo` como "Source of Truth" para fechas y URLs oficiales.

---

## 3. 🧩 AUDITORÍA QDRANT (Vectores)

Estado: **Caótico pero recuperable.**

### Colección: `leyes_espana` (768 dimensiones)
*   **Contenido:** Segmentos de leyes básicas (Constitución, LRJSP).
*   **Estado:** 🗑️ **Descartable** (Modelo obsoleto).

### Colección: `opositaia_knowledge` (Dimensiones desconocidas)
*   **Contenido:** Leyes masivas con metadatos ricos (`prioridad: CRÍTICA`).
*   **Material "Académico":** ❌ **NO ENCONTRADO.** Los muestreos solo muestran BOE puro.
*   **Problema Crítico:** Incompatibilidad de dimensiones con `pablosi` (1024).

---

## 4. 🚀 PROXIMOS PASOS (Plan de Acción)

1.  **Limpieza Radical (Punto 14):**
    *   Borrar colecciones Qdrant corruptas.
    *   Mantener `leyes_catalogo` en Postgres.
2.  **Re-Ingesta Controlada:**
    *   Ingestar de nuevo usando `pablosi` (1024 dims).
3.  **Corrección de Prompt:**
    *   Educar al modelo sobre la jurisprudencia restrictiva (STS 926/2023).

---
**Firmado:** Antigravity (Auditoría Técnica)
