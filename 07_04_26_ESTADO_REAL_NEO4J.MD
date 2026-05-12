# ESTADO REAL NEO4J — ANÁLISIS COMPLETO
**Fecha original:** 07/04/2026 (v16) | **ACTUALIZADO:** 09/04/2026 (v17) ✅ RESUELTO

---

## ✅ ACTUALIZACIÓN 09/04/2026 — TODOS LOS PROBLEMAS RESUELTOS (v17)

| Métrica | v16 (07/04/2026) | v17 (09/04/2026) |
|---------|-----------------|-----------------|
| Leyes | 95 (con basura) | **84** ✅ |
| Leyes vacías | **22** ❌ | **0** ✅ |
| BOE IDs incorrectos | **6+** ❌ | **0** ✅ |
| Preceptos | 5.554 (corruptos) | **4.877** ✅ |
| Con embedding | 5.554 (corruptos) | **4.877 (100%)** ✅ |
| Metadatos Ley | VACÍOS ❌ | **Completos** ✅ |
| Relaciones MODIFICA | 6 ⚠️ | **66** ✅ |
| Relaciones DEROGA | 1 ⚠️ | **48** ✅ |
| Relaciones SIGUIENTE | 0 | **22** (chunks) |
| Fuente datos | Caché v16 (ene 2026) ❌ | **API BOE real** ✅ |
| Vector search | ❌ índice roto | **✅ ONLINE** |
| Fulltext search | ⚠️ | **✅ ONLINE** |

**Solución:** Purge de Neo4j + reingestión completa con `ingest_neo4j_v17.py` + `catalog_v17.json`  
**Referencia completa:** `09_04_26_NEO4J_MEMORIA.md`

---

## 1. RESUMEN EJECUTIVO (HISTÓRICO v16 — 07/04/2026)

> ⚠️ **Este apartado es histórico y documenta el estado problemático de v16 ya resuelto**

| Métrica | Valor | Estado |
|---------|-------|--------|
| Leyes (nodos Ley) | 95 | ⚠️ Incluye irrelevantes y erróneas |
| Preceptos totales | 5.554 | ✅ Todos con embedding |
| Preceptos Artículo | 4.361 | ✅ |
| Preceptos Disposición | 1.193 | ✅ |
| **Leyes SIN preceptos** | **22** | ❌ CRÍTICO |
| Leyes con <6 preceptos | 3 | ❌ Incompletas |
| BOE IDs incorrectos confirmados | 6+ | ❌ CRÍTICO |
| Leyes irrelevantes/erróneas | 8+ | ❌ Contaminación |
| Metadatos Ley (fecha_pub, tipo, etc.) | VACÍOS | ❌ Todos a '' o 0 |
| Relaciones MODIFICA | 6 | ⚠️ Muy escasas |
| Relaciones DEROGA | 1 | ⚠️ Muy escasas |

**Diagnóstico:** La base de datos v16 está **funcionalmente operativa** para RAG básico (embeddings OK), pero contiene contaminación por leyes irrelevantes, 22 leyes completamente vacías, BOE IDs incorrectos y metadatos de nodo vacíos. **Necesita reingestión completa v17.**

---

## 2. ESTRUCTURA DE NODOS Y PROPIEDADES

### 2.1 Nodo `Ley` (95 nodos)
```
Propiedades: boe_id, siglas, titulo, historica, tipo, tiene_xml_api,
             fecha_pub, fecha_consolidacion, num_articulos_boe, num_disposiciones_boe
```
**Problemas detectados:**
- `tipo`: vacío (`''`) en los 95 nodos — campo no poblado
- `fecha_pub`: vacío (`''`) en los 95 nodos
- `fecha_consolidacion`: vacío en los 95 nodos
- `num_articulos_boe`: `0` en los 95 nodos — no poblado
- `num_disposiciones_boe`: `0` en los 95 nodos — no poblado
- `tiene_xml_api`: `True` en los 95 nodos — **ERRÓNEO**, muchas no tienen XML API

### 2.2 Nodo `Precepto` (5.554 nodos, etiquetas: `Precepto+Articulo` o `Precepto+Disposicion`)
```
Propiedades: id, ley_id, ley_siglas, title, numero, sufijo, texto,
             vigente, url_boe, fecha_vigencia, source, embedding
```
**Stats:**
- `embedding`: 1024 dimensiones, **todos los 5.554** tienen embedding ✅
- `texto`: min=23 chars, max=53.509 chars, avg=1.848 chars
- `source`: `BOE_XML_v16` (3.176 preceptos) + `BOE_JSON_CACHE_v16` (2.378 preceptos)

### 2.3 Relaciones
| Tipo | Count | Dirección | Notas |
|------|-------|-----------|-------|
| `PERTENECE_A` | 5.554 | Precepto → Ley | Única relación estructural |
| `MODIFICA` | 6 | Ley → Ley | Muy escasas |
| `DEROGA` | 1 | Ley → Ley | Solo TRLGSS→TRLGSS 1994 |

**Relaciones MODIFICA existentes:**
- Ley 2/2025 → TRLGSS, ET, Ley 47/2015 Mar
- RDL 2/2023 → TRLGSS
- Ley 21/2021 → TRLGSS
- RDL 13/2022 → TRLGSS

### 2.4 Índices
| Nombre | Tipo | Campo | Estado |
|--------|------|-------|--------|
| `ley_boe_id` | RANGE | Ley.boe_id | ONLINE ✅ |
| `precepto_id` | RANGE | Precepto.id | ONLINE ✅ |
| `precepto_embedding` | VECTOR | Precepto.embedding | ONLINE ✅ (1024D, COSINE, HNSW) |
| `precepto_fulltext` | FULLTEXT | Precepto.(texto,title) | ONLINE ✅ |

---

## 3. LAS 95 LEYES — LISTA COMPLETA CON PRECEPTOS

| BOE ID | Siglas | Preceptos | Estado |
|--------|--------|-----------|--------|
| BOE-A-1960-12344 | Ley 45/1960 | 0 | ❌ VACÍA |
| BOE-A-1963-22667 | Ley de Bases 1963 | 0 | ❌ VACÍA |
| BOE-A-1966-10707 | Decreto 907/1966 | 0 | ❌ VACÍA + BOE ID ERRÓNEO |
| BOE-A-1966-21116 | Decreto 3158/1966 | 1 | ❌ CASI VACÍA |
| BOE-A-1967-2876 | Orden 13/02/1967 | 35 | ✅ |
| BOE-A-1969-123 | Ley 45/1969 | 0 | ❌ VACÍA |
| BOE-A-1969-8263 | Orden IT 1969 | 0 | ❌ VACÍA |
| BOE-A-1970-1000 | Decreto 2530/1970 | 11 | ⚠️ Pocos |
| BOE-A-1972-907 | Ley 24/1972 | 0 | ❌ VACÍA |
| BOE-A-1972-944 | Decreto 1646/1972 | 6 | ⚠️ Pocos |
| BOE-A-1973-282 | Decreto 298/1973 | 12 | ⚠️ |
| BOE-A-1973-51 | Decreto 3772/1972 | 0 | ❌ VACÍA |
| BOE-A-1974-1165 | TRLGSS 1974 | 236 | ✅ (histórica) |
| BOE-A-1977-24931 | Ley 46/1977 | 0 | ❌ VACÍA + IRRELEVANTE |
| BOE-A-1978-28739 | RDL 36/1978 | 12 | ⚠️ |
| BOE-A-1978-31229 | CE | 184 | ✅ |
| BOE-A-1981-16216 | Ley 30/1981 | 14 | ⚠️ IRRELEVANTE (matrimonio CC) |
| BOE-A-1982-9983 | LISMI | 11 | ⚠️ Pocos |
| BOE-A-1983-15758 | RD 1451/1983 | 0 | ❌ VACÍA + BOE ID ERRÓNEO |
| BOE-A-1985-16119 | Ley 26/1985 | 0 | ❌ VACÍA |
| BOE-A-1985-18544 | RD 625/1985 Desempleo | 0 | ❌ VACÍA + BOE ID ERRÓNEO |
| BOE-A-1985-806 | RD 2366/1984 | 9 | ⚠️ |
| BOE-A-1986-33763 | RD 2621/1986 | 36 | ✅ |
| BOE-A-1990-29784 | RD 1576/1990 | 0 | ❌ VACÍA + BOE ID ERRÓNEO |
| BOE-A-1991-7270 | RD 357/1991 | 37 | ✅ |
| BOE-A-1992-24743 | RD 1221/1992 | 49 | ✅ |
| BOE-A-1994-1565 | TRLGSS 1994 | 5 | ❌ CASI VACÍA |
| BOE-A-1995-19848 | RD 1300/1995 | 18 | ✅ |
| BOE-A-1995-24292 | Ley 31/1995 PRL | 78 | ✅ |
| BOE-A-1995-26716 | RD 1993/1995 | 148 | ✅ |
| BOE-A-1996-1579 | RD 2064/1995 | 105 | ✅ |
| BOE-A-1996-29117 | Ley 13/1996 | 220 | ⚠️ Solo D.A. relevante |
| BOE-A-1996-3691 | RD 148/1996 | 11 | ⚠️ Pocos |
| BOE-A-1996-4447 | RD 84/1996 | 75 | ✅ |
| BOE-A-1997-15688 | Ley 24/1997 | 0 | ❌ VACÍA + BOE ID SOSPECHOSO |
| BOE-A-1997-1853 | RD 39/1997 | 62 | ✅ |
| BOE-A-1997-24163 | RD 1647/1997 | 19 | ✅ |
| BOE-A-1998-12816 | RD 928/1998 | 55 | ⚠️ Relevancia parcial |
| BOE-A-1998-30155 | Ley 50/1998 | 164 | ⚠️ Solo arts. SS relevantes |
| BOE-A-1999-15681 | Ley 27/1999 Cooperativas | 147 | ❌ IRRELEVANTE para C1 SS |
| BOE-A-1999-21568 | Ley 39/1999 | 8 | ⚠️ Pocos |
| BOE-A-2000-15060 | LISOS | 66 | ✅ |
| BOE-A-2000-323 | LEC | 901 | ❌ IRRELEVANTE (901 preceptos!) |
| BOE-A-2002-13972 | Ley 35/2002 | 21 | ✅ |
| BOE-A-2002-23038 | RD 1132/2002 | 21 | ✅ |
| BOE-A-2003-19281 | Orden TAS/2865/2003 | 39 | ✅ |
| BOE-A-2003-19458 | RD 1273/2003 | 5 | ❌ CASI VACÍA |
| BOE-A-2003-21147 | Orden RED | 0 | ❌ VACÍA |
| BOE-A-2003-22716 | Ley 52/2003 | 31 | ✅ |
| BOE-A-2003-23401 | RD 1539/2003 | 9 | ⚠️ |
| BOE-A-2004-11836 | RD 1415/2004 | 151 | ✅ |
| BOE-A-2005-19151 | RD 1335/2005 | 40 | ✅ |
| BOE-A-2006-22169 | RD 1299/2006 | 12 | ⚠️ Pocos |
| BOE-A-2006-22865 | Ley 42/2006 | 163 | ⚠️ Solo D.A. 4ª relevante |
| BOE-A-2007-13409 | LETA | 76 | ✅ |
| BOE-A-2007-21092 | Ley 40/2007 | 17 | ✅ |
| BOE-A-2007-8419 | RD 504/2007 | 0 | ❌ VACÍA |
| BOE-A-2007-9690 | RD 615/2007 | 14 | ⚠️ |
| BOE-A-2008-1067 | RD 8/2008 | 0 | ❌ VACÍA |
| BOE-A-2009-20412 | RD 1851/2009 | 0 | ❌ VACÍA + BOE ID ERRÓNEO |
| BOE-A-2009-20652 | RD 1855/2009 | 13 | ❌ LEY EQUIVOCADA (SAAD) |
| BOE-A-2009-4724 | RD 295/2009 | 69 | ✅ |
| BOE-A-2010-12628 | Ley 32/2010 CATA | 0 | ❌ VACÍA |
| BOE-A-2010-18651 | RDL 13/2010 | 31 | ✅ |
| BOE-A-2011-13119 | RD 1148/2011 | 17 | ✅ |
| BOE-A-2011-13242 | Ley 27/2011 | 46 | ✅ |
| BOE-A-2011-15038 | Ley 28/2011 | 21 | ✅ |
| BOE-A-2012-13420 | RD 1191/2012 | 19 | ⚠️ SIGLAS INCORRECTAS (es RD 1484/2012) |
| BOE-A-2013-11881 | RD 1196/2013 | 0 | ❌ VACÍA |
| BOE-A-2013-13617 | Ley 23/2013 | 18 | ✅ |
| BOE-A-2014-7684 | RD 625/2014 | 25 | ✅ |
| BOE-A-2015-10565 | LPAC | 155 | ✅ |
| BOE-A-2015-10566 | LRJSP | 211 | ✅ |
| BOE-A-2015-11346 | Ley 47/2015 Mar | 63 | ✅ |
| BOE-A-2015-11430 | ET | 132 | ✅ |
| BOE-A-2015-11719 | EBEP | 134 | ✅ |
| BOE-A-2015-11724 | TRLGSS | 442 | ✅ PRINCIPAL |
| BOE-A-2017-12902 | LCSP | 393 | ✅ |
| BOE-A-2018-10397 | RD 900/2018 | 12 | ✅ |
| BOE-A-2018-9030 | RD 696/2018 | 39 | ✅ |
| BOE-A-2019-15790 | RDL 14/2019 | 14 | ✅ |
| BOE-A-2019-3244 | Ley 3/2019 Orfandad | 11 | ✅ |
| BOE-A-2019-4676 | RDL 8/2019 | 0 | ❌ VACÍA |
| BOE-A-2021-1529 | RDL 3/2021 | 18 | ✅ |
| BOE-A-2021-21007 | Ley 19/2021 IMV | 75 | ✅ |
| BOE-A-2021-21652 | Ley 21/2021 | 17 | ✅ |
| BOE-A-2022-10656 | RD 504/2022 | 0 | ❌ VACÍA |
| BOE-A-2022-12482 | RDL 13/2022 | 17 | ✅ |
| BOE-A-2022-14630 | LO 10/2022 | 88 | ❌ IRRELEVANTE (libertad sexual) |
| BOE-A-2023-11645 | Orden Cotización 2023 | 9 | ⚠️ Desactualizada (existe 2025) |
| BOE-A-2023-5364 | RDL 2/2023 | 18 | ⚠️ BOE ID SOSPECHOSO |
| BOE-A-2024-10235 | RDL 2/2024 | 25 | ✅ |
| BOE-A-2024-10237 | RD 501/2024 | 29 | ✅ |
| BOE-A-2025-3780 | Orden PJC/178/2025 | 59 | ✅ |
| BOE-A-2025-8567 | Ley 2/2025 | 0 | ❌ VACÍA (CRÍTICA — gran incapacidad) |

---

## 4. PROBLEMAS CRÍTICOS DETALLADOS

### 4.1 BOE IDs INCORRECTOS (confirmados/sospechosos)

| Siglas | BOE ID en Neo4j | BOE ID correcto | Problema |
|--------|----------------|----------------|---------|
| Decreto 907/1966 | BOE-A-1966-10707 | ❓ DESCONOCIDO | Confirmado erróneo (verificación previa) |
| Ley 24/1997 | BOE-A-1997-15688 | BOE-A-1997-15810 | Sospechoso, debería ser -15810 |
| RD 1451/1983 | BOE-A-1983-15758 | BOE-A-1983-15813 | Difiere del catalogo_PARTE2_SS |
| RD 1576/1990 | BOE-A-1990-29784 | BOE-A-1990-29699 | Difiere del catalogo_PARTE2_SS |
| RD 625/1985 | BOE-A-1985-18544 | BOE-A-1985-8124 | Difiere del catalogo_PARTE2_SS |
| RD 1851/2009 | BOE-A-2009-20412 | BOE-A-2009-20652 | BOE_ID apunta a ley diferente |
| RDL 2/2023 | BOE-A-2023-5364 | BOE-A-2023-6967 | Difiere del catalogo_PARTE2_SS |

### 4.2 SIGLAS/LEY EQUIVOCADAS en el nodo

| BOE ID en Neo4j | Siglas en Neo4j | Ley real en ese BOE ID |
|-----------------|----------------|------------------------|
| BOE-A-2009-20652 | "RD 1855/2009" | Es el RD sobre Consejo Territorial SAAD — IRRELEVANTE |
| BOE-A-2012-13420 | "RD 1191/2012" | El catálogo dice RD 1484/2012 en ese ID |

### 4.3 LEYES IRRELEVANTES para examen SS C1

| Siglas | Preceptos | Por qué es un problema |
|--------|-----------|----------------------|
| LEC | 901 | Ley Enjuiciamiento Civil — NO está en el temario SS C1 |
| Ley 27/1999 Cooperativas | 147 | No está en temario SS C1 |
| LO 10/2022 | 88 | Ley libertad sexual — no en temario SS C1 |
| Ley 30/1981 | 14 | Matrimonio Código Civil — no en temario |
| Ley 46/1977 | 0 | Amnistía — no en temario |
| RD 1855/2009 | 13 | Consejo Territorial SAAD — no directamente en temario |
| Orden Cotización 2023 | 9 | Desactualizada, existe Orden PJC/178/2025 |

### 4.4 LEYES VACÍAS (22 normas — fallo v16)

Exactamente las 22 normas que el CONSEJOS_30_03_2026.md documentaba como fallidas en v16:

**Grupo A — Críticas para el examen (SIN contenido):**
1. `Ley 2/2025` — Gran Incapacidad (modificación más reciente del TRLGSS)
2. `Ley 24/1997` — Consolidación y Racionalización SS
3. `Ley 32/2010 CATA` — Cese de actividad autónomos
4. `RD 1196/2013` — Convenios especiales SS
5. `RD 1451/1983` — Empleo selectivo minusválidos
6. `Decreto 3772/1972` — REA (Régimen Especial Agrario)
7. `RD 625/1985` — Protección por Desempleo
8. `RDL 8/2019` — Medidas urgentes protección social
9. `RD 504/2022` — Modificación Reglamento afiliación/cotización autónomos
10. `Orden RED` — Sistema remisión electrónica datos

**Grupo B — Históricas/menor criticidad (SIN contenido):**
11. `Ley 26/1985` — Racionalización estructura SS (histórica)
12. `Ley 24/1972` — Financiación Régimen General (histórica)
13. `Ley de Bases 1963` — Base fundacional SS (histórica)
14. `Decreto 907/1966` — Texto articulado Ley Bases (BOE ID erróneo además)
15. `Ley 45/1960` — Fondos Nacionales (histórica)
16. `Ley 45/1969` — Fondo Nacional Asistencia Social (histórica)
17. `Ley 46/1977` — Amnistía (histórica + irrelevante)
18. `Orden IT 1969` — IT Régimen General (histórica)

**Grupo C — Casi vacías (1-5 preceptos = ingesta incompleta):**
19. `Decreto 3158/1966` — 1 precepto (Reglamento AT)
20. `TRLGSS 1994` — 5 preceptos (histórica)
21. `RD 1273/2003` — 5 preceptos (contingencias profesionales autónomos)

---

## 5. LO QUE SÍ FUNCIONA

Las siguientes leyes tienen contenido correcto y completo para RAG:

**Pilares principales del examen (bien ingestadas):**
- TRLGSS (442 preceptos) ✅
- LCSP (393 preceptos) ✅
- ET (132 preceptos) ✅
- EBEP (134 preceptos) ✅
- LPAC (155 preceptos) ✅
- LRJSP (211 preceptos) ✅
- CE (184 preceptos) ✅
- LISOS (66 preceptos) ✅
- LETA (76 preceptos) ✅
- Ley 19/2021 IMV (75 preceptos) ✅
- Ley 31/1995 PRL (78 preceptos) ✅
- RDL 2/2023 (18 preceptos) ✅
- Ley 21/2021 (17 preceptos) ✅
- RDL 13/2022 (17 preceptos) ✅
- RD 295/2009 (69 preceptos) ✅
- RD 84/1996 (75 preceptos) ✅
- RD 1415/2004 (151 preceptos) ✅
- RD 1993/1995 (148 preceptos) ✅
- RD 2064/1995 (105 preceptos) ✅
- Ley 27/2011 (46 preceptos) ✅
- Orden PJC/178/2025 (59 preceptos) ✅
- LO 10/2022 (88 preceptos) ⚠️ irrelevante pero tiene contenido

---

## 6. PLAN DE ACCIÓN — QUÉ HACER

### PASO 1: Determinar catálogo base para v17
**Usar: `catalogo_PARTE2_SS.json` + `catalogo_PARTE1_AGE.json`** (fusión)
- Eliminar leyes irrelevantes: LEC, LO 10/2022, Ley 27/1999 Cooperativas, Ley 30/1981, Ley 46/1977, RD 1855/2009
- Eliminar Orden Cotización 2023 (hay 2025 más reciente)
- Corregir BOE IDs erróneos antes de reingestar

### PASO 2: Limpiar Neo4j antes de reingestión
```cypher
// Borrar leyes irrelevantes y sus preceptos
MATCH (l:Ley) WHERE l.siglas IN ['LEC','LO 10/2022','Ley 27/1999 Cooperativas',
  'Ley 30/1981','Ley 46/1977','RD 1855/2009','Orden Cotización 2023']
DETACH DELETE l

// Borrar preceptos huérfanos
MATCH (p:Precepto) WHERE NOT (p)-[:PERTENECE_A]->(:Ley) DELETE p
```

### PASO 3: Seguir plan `v17-maestro-completo-2f78e3.md`
- Crear `boe_service.py` con fallback fetch
- Corregir BOE IDs en catálogo
- Crear `ingest_neo4j_v17.py`
- Re-ingestar las 22 vacías + leyes con pocos preceptos
- Enriquecer metadata de nodos Ley (tipo, fecha_pub, etc.)
- Añadir más relaciones MODIFICA/DEROGA

---

## 7. REFERENCIAS

- Catálogo base: `/home/spas/OPOS_GEMINI_1/backend/data/catalogo_PARTE2_SS.json`
- Catálogo AGE: `/home/spas/OPOS_GEMINI_1/backend/data/catalogo_PARTE1_AGE.json`
- Plan reingestión: `/home/spas/.windsurf/plans/v17-maestro-completo-2f78e3.md`
- Plan casos: `/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/PLAN_MAESTRO_CASOS_SIMULACROS.md`
- Leyes verificadas: `/home/spas/OPOS_GEMINI_1/95_LEYES_INGESTADAS_NEO4J_04_04_2026.MD`
