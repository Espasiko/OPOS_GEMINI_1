# LISTA LEYES NEO4J — ESTADO ACTUALIZADO (09/04/2026)

> **⚠️ ESTE FICHERO ERA EL TRACKING DE LEYES PENDIENTES (v16)**
> **✅ RESUELTO COMPLETAMENTE con ingestión v17 — 09/04/2026**
> **Estado actual**: 84/84 leyes ingestadas, 0 pendientes, 0 vacías, 4.877 preceptos con embedding

---

## ✅ ESTADO v17 — 09/04/2026

| Métrica | v16 (04/04/2026) | v17 (09/04/2026) |
|---------|-----------------|-----------------|
| Leyes | 95 (con basura) | **84 (limpias)** |
| Leyes vacías | 22 ❌ | **0** ✅ |
| BOE IDs incorrectos | 6+ ❌ | **0** ✅ |
| Preceptos con embedding | 5.554 (corruptos) | **4.877 (100% frescos)** |
| Fuente datos | Caché v16 (ene 2026) | **API BOE real** |
| Leyes irrelevantes | 8+ (LEC, LO 10/2022…) | **0** (eliminadas) |

**Catálogo activo**: `/home/spas/OPOS_GEMINI_1/backend/data/catalog_v17.json`
**Referencia completa**: `09_04_26_NEO4J_MEMORIA.md`

---

## ✅ LAS 84 LEYES v17 — TODAS INGESTADAS

### Alta Prioridad (18 — núcleo del temario SS)

| Siglas | BOE-ID | Preceptos | Estado |
|--------|--------|-----------|--------|
| CE | BOE-A-1978-31229 | 184 | ✅ |
| TRLGSS 1994 | BOE-A-1994-14960 | 314 | ✅ |
| Ley 24/1997 | BOE-A-1997-15810 | 18 | ✅ |
| LETA | BOE-A-2007-13409 | 76 | ✅ |
| Ley 32/2010 CATA | BOE-A-2010-12616 | 43 | ✅ |
| Ley 27/2011 | BOE-A-2011-13242 | 75 | ✅ |
| LPAC | BOE-A-2015-10565 | 155 | ✅ |
| LRJSP | BOE-A-2015-10566 | 214 | ✅ |
| ET | BOE-A-2015-11430 | 140 | ✅ |
| TREBEP | BOE-A-2015-11719 | 136 | ✅ |
| TRLGSS | BOE-A-2015-11724 | 443 | ✅ PRINCIPAL |
| LCSP | BOE-A-2017-12902 | 393 | ✅ |
| RDL 8/2019 | BOE-A-2019-3481 | 24 | ✅ |
| Ley 19/2021 IMV | BOE-A-2021-21007 | 76 | ✅ |
| Ley 21/2021 | BOE-A-2021-21652 | 19 | ✅ |
| RDL 13/2022 | BOE-A-2022-12482 | 17 | ✅ |
| RDL 2/2023 | BOE-A-2023-6967 | 23 | ✅ |
| Ley 2/2025 | BOE-A-2025-8567 | — | ✅ nodo Ley OK |
| RDL 6/2019 | BOE-A-2019-3244 | 12 | ✅ |

### Media — resto (62 leyes vigentes + 2 históricas sin XML)

Todas las leyes del catálogo v17 están ingestadas.
Solo **2 históricas** sin preceptos (sin XML en API BOE — comportamiento esperado):
- `Ley de Bases 1963` (BOE-A-1963-22667) — nodo Ley insertado sin preceptos
- `TRLGSS 1974` (BOE-A-1974-1165) — nodo Ley insertado sin preceptos

---

## ⚠️ PENDIENTE FUTURO (próximas versiones de catálogo)

| Norma | Motivo pendiente | Estado BOE |
|-------|-----------------|------------|
| Ley 5/2025 (IPREM 2026) | Pendiente BOE consolidado | Sin XML aún |
| RD 126/2026 (SMI 2026) | Pendiente BOE consolidado | Sin XML aún |
| RD 3/2026 (Bases cotización 2026) | Pendiente BOE consolidado | Sin XML aún |

> Estas normas no se pueden ingestar hasta que el BOE publique su XML consolidado.

---

## HISTORIAL

| Fecha | Evento |
|-------|--------|
| 31/03/2026 | Identificadas 22 leyes vacías en v16 |
| 04/04/2026 | Verificación BOE: 0% correctos, 19 errores críticos |
| 07/04/2026 | Análisis completo v16 — decisión reingestar con v17 |
| 08/04/2026 | Purge Neo4j v16, ingesta v17 iniciada (cache borrado) |
| 09/04/2026 | **84/84 leyes OK, 4.877 preceptos, 0 errores** ✅ |

---

*Fichero actualizado 09/04/2026 — Ver `09_04_26_NEO4J_MEMORIA.md` para referencia completa*
