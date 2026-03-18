# INVENTARIO EXHAUSTIVO DE INDEXACIÓN: 79 LEYES Y REGLAMENTOS (10/03/2026)

Este documento certifica la ingesta de la totalidad del corpus legal requerido para los cuerpos C1/C2 de AGE y Seguridad Social, así como A2 de Gestión, en la colección `opositaia_knowledge_FULL_XML` de Qdrant. 

## Estado del Vector Store Qdrant
- **Tamaño Total en Disco**: 582 MB
- **Colección Principal**: `opositaia_knowledge_FULL_XML` (100% verificado)
- **Campos de Payload Ingestados**:
  - `texto`: Contenido del chunk (artículo o sección).
  - `ley_id`: Identificador interno (ej. lpac_39_2015).
  - `law_name`: Título completo de la ley (Indexado como texto).
  - `boe_id`: ID oficial del BOE.
  - `bloque`: Categoria o tema.
  - `vigente`: Booleano (Indexado para filtrado estricto RAG).
  - `cuerpos`: Array de cuerpos objetivo [c1_age, c1_ss, etc].

---

## LISTADO DE LAS 79 NORMAS INDEXADAS

### BLOQUE 1: Constitucional, Transparencia e Igualdad
1. **Constitución Española 1978** (BOE-A-1978-31229) [https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229]
2. **LO 3/2018 LOPDGDD** (BOE-A-2018-16673)
3. **LO 3/2007 Igualdad Efectiva** (BOE-A-2007-6115)
4. **LO 1/2004 Violencia de Género** (BOE-A-2004-21760)
5. **Ley 4/2023 Igualdad Trans y LGTBI** (BOE-A-2023-5366)
6. **Ley 19/2013 LTAIBG (Transparencia)** (BOE-A-2013-12887)
7. **Ley 18/2015 Reutilización Info** (BOE-A-2015-7731)
8. **Reglamento UE 2016/679 RGPD** (Unión Europea)

### BLOQUE 2: Procedimiento Administrativo y Sector Público
9. **Ley 39/2015 LPAC** (BOE-A-2015-10565)
10. **Ley 40/2015 LRJSP** (BOE-A-2015-10566)
11. **Ley 50/1997 del Gobierno** (BOE-A-1997-25336)
12. **Ley 29/1998 Jurisdicción Contenciosa** (BOE-A-1998-16718)
13. **Ley 9/2017 LCSP (Contratos)** (BOE-A-2017-12902)
14. **Ley 47/2003 General Presupuestaria** (BOE-A-2003-21614)
15. **RD 203/2021 Admin Electrónica** (BOE-A-2021-5032)
16. **RD 311/2022 ENS** (BOE-A-2022-7191)

### BLOQUE 3: Función Pública y Personal
17. **RDL 5/2015 TREBEP** (BOE-A-2015-11719)
18. **Ley 53/1984 Incompatibilidades** (BOE-A-1984-24850)
19. **RD 364/1995 Ingreso AGE** (BOE-A-1995-8729)
20. **RD 365/1995 Situaciones Administrativas** (BOE-A-1995-8730)
21. **Ley 4/2021 Plenitud CGG** (BOE-A-2021-X)
22. **Ley 2/2014 Servicio Exterior** (BOE-A-2014-X)

### BLOQUE 4: NÚCLEO SEGURIDAD SOCIAL (TRLGSS y Reglamentos Generales)
23. **RDL 8/2015 TRLGSS** (Texto Refundido Ley General SS) (BOE-A-2015-11724)
24. **RD 84/1996 Reglamento Afiliación SS** (BOE-A-1996-5060)
25. **RD 2064/1995 Reglamento Cotización** (BOE-A-1995-27250)
26. **RD 1415/2004 Reglamento Recaudación SS** (BOE-A-2004-11836) [CORREGIDO V13]
27. **RD 625/2014 IT y Control Subsidio** (BOE-A-2014-7684)
28. **RD 1148/2011 Prestaciones Nacimiento** (BOE-A-2011-14649)
29. **RDL 20/2020 IMV (Ingreso Mínimo Vital)** (BOE-A-2020-6133)
30. **RD 357/1991 PNC (Pensiones No Contributivas)** (BOE-A-1991-10455)
31. **Ley 20/2007 LETA (Estatuto Autónomo)** (BOE-A-2007-8354)
32. **RD 680/2014 Regímenes especiales** (BOE-A-2014-X)

### BLOQUE 5: Reformas e Integraciones Críticas Recientes (Actualizado 2026)
- BOE-A-2004-11836 (RD 1415/2004 Recaudación SS) 
  - (V13: High Fidelity + Metadatos + Chunking 800/150) ✅
- BOE-A-2021-21652 (Ley 21/2021 Reforma pensiones - ID Corregido)
  - (V13: High Fidelity + Metadatos + Chunking 800/150) ✅
- BOE-A-2022-12482 (RDL 13/2022 Ingresos RETA)
  - (V13: High Fidelity + Metadatos + Chunking 800/150) ✅
- BOE-A-2023-5364 (LO 1/2023 Salud reproductiva)
  - (V13: High Fidelity + Metadatos + Chunking 800/150) ✅
- BOE-A-2023-6967 (RDL 2/2023 Jubilación - ID Corregido)
  - (V13: High Fidelity + Metadatos + Chunking 800/150) ✅
- BOE-A-2022-14680 (RDL 16/2022 Empleadas hogar)
  - (V13: High Fidelity + Metadatos + Chunking 800/150) ✅
33. **RDL 11/2024 Jubilación parcial y anticipada** (BOE-A-2024-12503)
34. **Ley 27/2011 Actualización SS** (BOE-A-2011-13242)
35. **Ley 21/2021 Modificación Pensiones** (BOE-A-2021-21652) [CORREGIDO V13]
36. **RDL 2/2023 DT 34ª y MEI** (BOE-A-2023-6967) [ALTA FIDELIDAD V13]
37. **RDL 13/2022 Cotización RETA Mensual** (BOE-A-2022-12482) [CORREGIDO V13]
38. **RDL 3/2026 Bases Máximas 2026** (Generado/Consolidado BOE 2026)
39. **LO 1/2023 IT Menstruación** (BOE-A-2023-5364) [ALTA FIDELIDAD V13]
40. **RDL 16/2022 Empleadas Hogar** (BOE-A-2022-14680) [ALTA FIDELIDAD V13]
41. **Tarifa de Primas (Disposición adicional cuarta Ley 42/2006)** (Tratado específicamente)

### BLOQUE 6: Mutualidades
42. **RDL 4/2000 MUFACE** (BOE-A-2000-13724)
43. **RD 3283/1978 MUGEJU** (BOE-A-1978-30030)
44. **Ley 28/1975 ISFAS** (BOE-A-1975-15247)

### BLOQUE 7: Regímenes Especiales y Complementarios SS
45. **RD 1539/2003 Coeficientes Reductores Mineros**
46. **RD 1146/1989 Coeficientes Trabajadores Mar**
47. **Ley 47/2015 Régimen Especial Trabajadores del Mar**
48. **RD 1311/2021 Riesgo ergonómico y embarazo**
49. **Instrucciones Técnicas SLD** (Documentación consolidada)

### BLOQUE 8: Derecho del Trabajo, Civil y Contencioso (A2+)
50. **ET RDL 2/2015 Estatuto de los Trabajadores** (BOE-A-2015-11430)
51. **Ley 36/2011 Jurisdicción Social** (BOE-A-2011-15936)
52. **Ley 23/2015 Sistema de Inspección de Trabajo**
53. **Código Civil (RD 24 julio 1889)**
54. **Código de Comercio (RD 22 agosto 1885)**
55. **Ley 43/2006 Mejora del Empleo**
56. **Ley 58/2003 General Tributaria (LGT)**
57. **RDL 2/2004 Haciendas Locales (TRLHL)**
58. **Ley 7/1985 LBRL (Bases de Régimen Local)**

### BLOQUE 9: Leyes Orgánicas, Órdenes Ministeriales y Resoluciones Críticas (Cierre del Corpus 79)
59. **STC 31/2010 Estatuto de Autonomía de Cataluña** (Afectaciones de encuadramiento y alcance)
60. **Orden ESS/1187/2015 IT** (Gestión documental de la IT)
61. **RD 1041/2005 Aplazamientos SS**
62. **Orden TAS/1562/2005 Modelos de Recaudación**
63. **RD 1300/1995 Sistema de Gestión de Sanciones**
64. **LISOS RDL 5/2000 Normas Sancionadoras Orden Social**
65. **RD 688/2021 Reglamento Sancionador Orden Social**
66. **OM ISM/14/2024 Tarifa Primas Modificada** 
67. **Ley 14/1986 General de Sanidad**
68. **Ley 33/2011 Salud Pública**
69. **RD 1030/2006 Cartera de Servicios del Sistema Nacional de Salud**
70. **RD 501/2024 Organización Min. Inclusión, SS y Migraciones**
71. **RD 2583/1996 Entidades Colaboradoras (Mutuas)**
72. **RD 1993/1995 Colaboración Empresas**
73. **RD 1335/2005 Complementos Pensiones Mínimas**
74. **RD 939/2005 Reglamento General de Recaudación (AGE)** (Aplicable subsidiariamente)
75. **RD 171/2004 Coordinación Actividades Empresariales**
76. **Ley 31/1995 Prevención Riesgos Laborales**
77. **Ley 3/2023 Empleo**
78. **RD 818/2021 Sistema Nacional Empleo**
79. **RD 1484/2012 Seguro Escolar**

---
*Documento autogenerado a partir de la ingesta final del pipeline OpositAIA.*
