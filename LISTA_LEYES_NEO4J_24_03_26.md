# LISTA LEYES NEO4J — Auditoría cruzada 30/03/2026

> Cruce triple: **Neo4j** (ingested) vs **catalog_FINAL_v2.json** (68 entradas) vs **PLAN_MAESTRO v3** (47 normas)
> Fecha de corte normativa: 04/03/2026

---

## ✅ SECCIÓN 1: En Neo4j Y necesarias para PLAN_MAESTRO (25 — núcleo OK)

| # | Siglas | Nombre completo | En Catálogo |
|---|--------|----------------|-------------|
| 1 | **TRLGSS** | RDL 8/2015, Ley General de la Seguridad Social | No (ya en Neo4j) |
| 2 | **CE** | Constitución Española | No (ya en Neo4j) |
| 3 | **ET** | RDL 2/2015, Estatuto de los Trabajadores | No (ya en Neo4j) |
| 4 | **TREBEP** | RDL 5/2015, Estatuto Básico del Empleado Público | No (ya en Neo4j) |
| 5 | **LPAC** | Ley 39/2015, Procedimiento Administrativo Común | No (ya en Neo4j) |
| 6 | **LRJSP** | Ley 40/2015, Régimen Jurídico del Sector Público | No (ya en Neo4j) |
| 7 | **LCSP** | Ley 9/2017, Contratos del Sector Público | No (ya en Neo4j) |
| 8 | **LETA** | Ley 20/2007, Estatuto del Trabajo Autónomo | Sí (BOE-A-2007-13409) |
| 9 | **RD 84/1996** | Reglamento General Afiliación | No (ya en Neo4j) |
| 10 | **RD 2064/1995** | Reglamento General Cotización | No (ya en Neo4j) |
| 11 | **RD 1415/2004** | Reglamento General Recaudación SS | No (ya en Neo4j) |
| 12 | **RD 1300/1995** | Desarrollo IP/EVI (Ley 42/1994) | No (ya en Neo4j) |
| 13 | **RD 625/2014** | Gestión y control IT (primeros 365 días) | No (ya en Neo4j) |
| 14 | **RD 295/2009** | Prestaciones maternidad/paternidad/riesgo embarazo | No (ya en Neo4j) |
| 15 | **RD 1430/2009** | Desarrollo Ley 40/2007 — IT | No (ya en Neo4j) |
| 16 | **RDL 2/2023** | MEI + solidaridad + BR dual | No (ya en Neo4j) |
| 17 | **RDL 11/2024** | Compatibilidad jubilación-trabajo | No (ya en Neo4j) |
| 18 | **RDL 13/2022** | Cotización autónomos por ingresos reales | No (ya en Neo4j) |
| 19 | **LO 1/2023** | Salud sexual y reproductiva (IT menstruación) | No (ya en Neo4j) |
| 20 | **Ley 19/2021** | Ingreso Mínimo Vital | No (ya en Neo4j) |
| 21 | **Ley 27/2011** | Actualización y modernización SS | No (ya en Neo4j) |
| 22 | **Ley 21/2021** | Garantía poder adquisitivo pensiones | No (ya en Neo4j) |
| 23 | **RD 1148/2011** | CUME (cáncer/enfermedad grave menor) | No (ya en Neo4j) |
| 24 | **RD 504/2022** | Modifica RD 84/1996 y RD 2064/1995 (autónomos) | Sí (BOE-A-2022-10656) |
| 25 | **RD 1009/2023** | Estructura orgánica ministerios | No (ya en Neo4j) |

---

## ⏳ SECCIÓN 2: En Catálogo PENDIENTES de ingestar a Neo4j (necesarias para PLAN_MAESTRO) (17)

| # | Siglas catálogo | BOE-ID catálogo | Histórica | Uso en PLAN_MAESTRO |
|---|----------------|-----------------|-----------|---------------------|
| 1 | Decreto 1646/1972 | BOE-A-1972-1262 | Sí | MS prestaciones muerte/supervivencia |
| 2 | Decreto 298/1973 | BOE-A-1973-282 | Sí | RE Minería Carbón |
| 3 | Decreto 3158/1966 | BOE-A-1966-21116 | Sí | AT reglamento prestaciones |
| 4 | Ley 42/2006 | BOE-A-2006-22874 | No | DA 4ª tarifa primas AT/EP |
| 5 | Ley 47/2015 Mar | BOE-A-2015-11346 | No | RE Mar protección social |
| 6 | Ley 2/2025 | BOE-A-2025-8567 | No | Reforma IP/gran invalidez |
| 7 | Orden PJC/178/2025 | BOE-A-2025-1393 | No | Cotización 2025 |
| 8 | Orden RED | BOE-A-2003-21147 | No | Sistema RED (TAS/2865/2003) |
| 9 | RD 1221/1992 | BOE-A-1992-17154 | No | Patrimonio SS |
| 10 | RD 1273/2003 | BOE-A-2003-19281 | No | Contingencias profesionales autónomos |
| 11 | RD 1299/2006 | BOE-A-2006-22169 | No | Cuadro enfermedades profesionales |
| 12 | RD 1335/2005 | BOE-A-2005-19151 | No | Prestaciones familiares |
| 13 | RD 1539/2003 | BOE-A-2003-23363 | No | Jubilación anticipada discapacidad |
| 14 | RD 1647/1997 | BOE-A-1997-24163 | No | Desarrollo Ley 24/1997 |
| 15 | RD 501/2024 | BOE-A-2024-10237 | No | Estructura MISSMI |
| 16 | RD 615/2007 | BOE-A-2007-9878 | No | SS cuidadores dependencia |
| 17 | Decreto 2530/1970 | BOE-A-1970-1066 | Sí | RETA original |

---

## ❌ SECCIÓN 3: FALTAN en Neo4j Y en Catálogo — HAY QUE AÑADIR AL CATÁLOGO (5)

| # | Norma | Por qué la necesita PLAN_MAESTRO | Acción |
|---|-------|----------------------------------|--------|
| 1 | **LO 10/2022** — Garantía integral libertad sexual | Bloque LO (LO01-LO08 trampas) | Añadir al catálogo |
| 2 | **Ley 27/1999** — Cooperativas | Bloque COOP (COOP01-COOP08 trampas) | Añadir al catálogo |
| 3 | **Ley 40/2007** — Medidas MS/IT | RD 1430/2009 la desarrolla (está en Neo4j), pero la ley misma no | Añadir al catálogo |
| 4 | **RD 900/2018** — Partes médicos IT (nuevo regl.) | Trampas IT en PLAN_MAESTRO | Añadir al catálogo |
| 5 | **LISOS (RDL 5/2000)** — Infracciones y Sanciones Orden Social | Trampas recaudación/sanciones | Ya en catálogo (BOE-A-2000-15060) pero NO en Neo4j → ingestar |

---

## ⚠️ SECCIÓN 4: Legislación 2025/2026 — pendiente publicación BOE consolidado

| # | Norma | Estado |
|---|-------|--------|
| 1 | **Ley 5/2025** (IPREM 2026) | Pendiente BOE consolidado |
| 2 | **RD 126/2026** (SMI 2026) | Pendiente BOE consolidado |
| 3 | **RD 3/2026** (Bases cotización 2026) | Pendiente BOE consolidado |

> Estas normas se referencian en COR01/COR02 del PLAN_MAESTRO pero no se pueden ingestar hasta tener XML BOE.

---

## 🗑️ SECCIÓN 5: En Neo4j pero NO relevantes / BASURA (limpiar)

| # | Entrada en Neo4j | Problema |
|---|-------------------|----------|
| 1 | RD 842/2002 (Reglamento electrotécnico baja tensión) | NO es SS ni administrativo relevante |
| 2 | Ley 9/1996 (sequía hidráulica) | NO es SS ni administrativo relevante |
| 3 | Resolución emprendedores 2009 (Extremadura) | BASURA — resolución de subvención |
| 4 | Resolución TGSS 1981 (integración funcionarios) | BASURA — resolución administrativa puntual |
| 5 | RD 99/1986 (Gran Cruz San Hermenegildo) | BASURA — concesión de condecoración |
| 6 | STC 31/2010 (Estatut Catalunya) | DUPLICADA (aparece 2 veces) + marginal |
| 7 | Norma BOE-A-2000-12140 | Sin identificar — verificar si es necesaria |
| 8 | Norma BOE-A-1985-16660 | Sin identificar — verificar si es necesaria |
| 9 | Norma BOE-A-2003-7527 | Sin identificar — verificar si es necesaria |
| 10 | Norma BOE-A-2007-19814 | Sin identificar — verificar si es necesaria |
| 11 | Norma BOE-A-2015-8168 | Sin identificar — verificar si es necesaria |
| 12 | Norma BOE-A-2015-7731 | Sin identificar — verificar si es necesaria |
| 13 | Norma BOE-A-2020-5493 | Sin identificar — verificar si es necesaria |
| 14 | Norma BOE-A-2022-7191 | Sin identificar — verificar si es necesaria |
| 15 | Norma BOE-A-1987-14115 | Sin identificar — verificar si es necesaria |
| 16 | Norma BOE-A-1996-1579 | Sin identificar — verificar si es necesaria |
| 17 | Norma BOE-A-2014-7684 | Probablemente RD 625/2014 (ya está con título, duplicado) |

---

## 📊 SECCIÓN 6: Leyes en Neo4j útiles para bloque GENERAL (no SS específico, pero sí oposición)

| # | Siglas | Para qué |
|---|--------|----------|
| 1 | LO 6/1985 (LOPJ) | Bloque General — Poder Judicial |
| 2 | Ley 29/1998 (LJCA) | Bloque General — Contencioso |
| 3 | Ley 36/2011 (LRJS) | Bloque General — Jurisdicción Social |
| 4 | LO 3/2018 (LOPDGDD) | Bloque General — Protección datos |
| 5 | RDL 1/2013 (Discapacidad) | Bloque Específico — inclusión social |
| 6 | Ley 50/1997 (Gobierno) | Bloque General |
| 7 | Ley 4/2023 (Trans/LGTBI) | Bloque General |
| 8 | RDL 16/2022 (Hogar) | Bloque Específico — integración empleadas hogar |
| 9 | Ley 1/2000 (LEC) | Art. 607 embargo salarios |
| 10 | LO 3/2007 (Igualdad) | Bloque General + SS |
| 11 | Ley 31/1995 (PRL) | Bloque Específico — riesgos laborales |
| 12 | RD 39/1997 (Serv. Prevención) | Bloque Específico |
| 13 | RD 357/1991 (PNC) | Bloque Específico — pensiones no contributivas |
| 14 | RD 1369/2006 (RAI) | Bloque Específico — renta activa inserción |
| 15 | LO 1/2004 (Violencia género) | Bloque General + prestaciones |
| 16 | Ley 23/2015 (Inspección Trabajo) | Bloque Específico |
| 17 | RDL 6/2019 (Igualdad empleo) | Bloque General + SS |
| 18 | RDL 20/2020 (IMV primera versión) | Sustituido por Ley 19/2021 (ya en Neo4j) |
| 19 | RDL 4/2000 (SS Funcionarios Civiles) | Bloque Específico |
| 20 | RD 375/2003 (Mutualismo Administrativo) | Bloque Específico |
| 21 | Orden HAC/1517/2025 (Límites contratos) | LCSP actualizado |

---

## RESUMEN EJECUTIVO

| Categoría | Cantidad | Estado |
|-----------|----------|--------|
| ✅ En Neo4j + necesarias PLAN_MAESTRO | **25** | OK — núcleo cubierto |
| ⏳ En catálogo pendientes ingestión | **17** | Ejecutar ingest_neo4j_v15 |
| ❌ Faltan en catálogo (añadir) | **4** | LO 10/2022, Ley 27/1999, Ley 40/2007, RD 900/2018 |
| ❌ En catálogo pero no en Neo4j | **1** | LISOS (BOE-A-2000-15060) → ingestar |
| ⚠️ Legislación 2026 pendiente BOE | **3** | Ley 5/2025, RD 126/2026, RD 3/2026 |
| 🗑️ Basura/duplicados en Neo4j | **5+12** | Limpiar en próxima reingestión |
| 📊 Útiles bloque general | **21** | Mantener |

**Conclusión:** El núcleo SS del PLAN_MAESTRO (25 leyes fundamentales) está en Neo4j. Faltan **4 normas por añadir al catálogo** + **18 del catálogo por ingestar** = **22 normas pendientes** antes de implementación completa.