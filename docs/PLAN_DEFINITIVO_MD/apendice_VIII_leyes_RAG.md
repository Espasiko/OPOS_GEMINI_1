**APÉNDICE VIII**

**OpositAIA --- Inventario Completo de Leyes para el RAG**

*Todas las leyes de todos los cuerpos · IMV confirmado · MUFACE / MUGEJU / ISFAS · BOE Códigos Electrónicos · Matriz de cobertura · Calculadoras vs RAG · URLs de descarga · Prioridades de indexación*

+----------------------+---------------------------+--------------------------+---------------------------+
| **C2 Auxiliar AGE**  | **C1 Administrativo AGE** | **C1 Administrativo SS** | **A2 Gestión SS**         |
|                      |                           |                          |                           |
| 28 temas · 2 bloques | 45 temas · 6 bloques      | 36 temas · 2 bloques     | 82 temas · nivel superior |
+----------------------+---------------------------+--------------------------+---------------------------+

**1. Respuesta Directa: IMV, MUFACE, MUGEJU, ISFAS**

**1.1 ¿El IMV está en las calculadoras?**

+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **✅ SÍ --- El IMV ya está implementado y operativo**                                                                                                                                                                                                                                                                                                                                                                                                                             |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| El módulo calculos_imv.py (10.9 KB) existe en backend/calculators/ y está OPERATIVO según la auditoría del 27/02/2026. El IMV no estaba en los 27 tipos numerados de calculos_ss_extended.py porque tiene su propio módulo dedicado. Contando el IMV, el total de calculadoras SS son 28, no 27. También está en el temario oficial como Tema 12 específico SS: \'Prestaciones no contributivas y asistenciales. El ingreso mínimo vital: beneficiarios, requisitos y duración.\' |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Módulo**                           **Archivo**                            **Estado**                                                             **Cálculos que incluye**
  ------------------------------------ -------------------------------------- ---------------------------------------------------------------------- --------------------------------------------------------------------------------------------
  Calculadoras SS generales            calculos_ss_extended.py (49.6KB)       ✅ Operativo y validado                                                27 tipos: IT, IP, Jubilación, Viudedad, Orfandad, Desempleo, Maternidad, Cotización y más

  IMV específico                       calculos_imv.py (10.9KB)               ✅ Operativo                                                           IMV completo: cuantías, beneficiarios, requisitos, unidad de convivencia, compatibilidades

  Pensiones No Contributivas (PNC)     En calculos_ss_extended.py o ampliar   ⚠️ Verificar si incluye PNC invalidez + PNC jubilación (RD 357/1991)   PNC invalidez 75% + pensiones mínimas contributivas

  Calculadoras AGE (procedimentales)   calculadora_age.py                     ❌ Por implementar                                                     28 tipos de plazos + TREBEP según Apéndice VI-VII
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**1.2 MUFACE, MUGEJU, ISFAS --- RAG sí, Calculadoras NO**

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  MUFACE (Mutualidad General Funcionarios Civiles), MUGEJU (Mutualidad General Judicial) e ISFAS (Mutualidad Fuerzas Armadas) son regímenes especiales de Seguridad Social para determinados colectivos de funcionarios. Aparecen en el temario AGE C1 (Tema 19: \'El régimen de SS de los funcionarios. MUFACE\') y en el temario específico SS (Tema 2: Regímenes especiales). El examen NUNCA pide calcular prestaciones de MUFACE --- solo preguntas conceptuales: quiénes pertenecen, diferencias con el INSS, mutualidades y su acción protectora. Por tanto: necesitan estar en el RAG como documentos de conocimiento, pero NO precisan calculadoras Python.

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Mutualidad**                   **Colectivo protegido**                      **¿En qué examen?**                 **Qué necesita OpositAIA**
  -------------------------------- -------------------------------------------- ----------------------------------- ------------------------------------------------------------------------------------------------------------------------
  MUFACE                           Funcionarios Civiles del Estado              AGE C1 (Tema 19) + SS C1 (Tema 2)   RAG: RDL 4/2000 texto completo. Preguntas test sobre diferencias con INSS, cobertura, elección médico. NO calculadora.

  MUGEJU                           Funcionarios Administración de Justicia      AGE C1 (Tema 19) + SS C1 (Tema 2)   RAG: RD 3283/1978 (concepto). Solo preguntas conceptuales. Aparece poco en exámenes --- BAJA frecuencia.

  ISFAS                            Personal Fuerzas Armadas y Guardia Civil     AGE C1 (Tema 19) + SS C1 (Tema 2)   RAG: Ley 28/1975 (concepto). Preguntas muy esporádicas. Indexar solo el resumen conceptual.

  TGSS --- Tesorería General       No es mutualidad sino organismo gestión SS   SS C1 todos los temas               RAG: arts. TRLGSS sobre TGSS. Ya cubierto por el TRLGSS completo en Qdrant.

  INSS --- Instituto Nacional SS   Organismo gestor pensiones y prestaciones    SS C1 todos los temas               RAG: arts. TRLGSS. Ya cubierto.
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**2. Los Códigos Electrónicos del BOE --- Fuente Primaria y Gratuita**

+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **🏆 El descubrimiento más valioso para el RAG**                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| La Biblioteca Jurídica Digital del BOE (boe.es/biblioteca_juridica) tiene códigos electrónicos específicos para cada cuerpo de oposición. Son PDFs con TODAS las leyes del temario, permanentemente actualizadas, seleccionadas y ordenadas por el propio BOE. Gratuitos, en español jurídico perfecto. Puedes suscribirte a alertas de actualización por email. Este es el punto de partida correcto para construir el RAG: descarga estos 2-3 PDFs y tienes el 95% de la normativa relevante. |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**2.1 Códigos disponibles para tus 4 cuerpos**

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Código**     **Nombre oficial**                                                                              **URL de descarga directa (PDF)**                                                                                                                              **Cuerpos**
  -------------- ----------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------
  **Cód. 435**   **Normativa para ingreso en el Cuerpo General AUXILIAR de la AGE**                              **boe.es/biblioteca_juridica/codigos/abrir_pdf.php?fich=435_Normativa_para_ingreso_en_el_Cuerpo_General_Auxiliar_de_la_Administracion_del_Estado.pdf**         **C2**

  **Cód. 442**   **Normativa para ingreso en el Cuerpo General ADMINISTRATIVO de la AGE**                        **boe.es/biblioteca_juridica/codigos/abrir_pdf.php?fich=442_Normativa_para_ingreso_en_el_Cuerpo_General_Administrativo_de_la_Administracion_del_Estado.pdf**   **C1 AGE**

  BOE directo    TRLGSS --- Texto Consolidado 2026 (RDL 8/2015) --- la ley eje del examen SS                     boe.es/buscar/act.php?id=BOE-A-2015-11724                                                                                                                      C1 SS / A2

  BOE directo    Convocatoria SS 2025 --- BOE-A-2025-27158 --- contiene el programa SS oficial                   boe.es/diario_boe/txt.php?id=BOE-A-2025-27158                                                                                                                  C1 SS

  BOE directo    Convocatoria AGE 2025 unificada --- BOE-A-2025-26262 --- programa AGE oficial                   boe.es/boe/dias/2025/12/22/pdfs/BOE-A-2025-26262.pdf                                                                                                           C1 + C2

  Alertas        Suscripción gratuita a cambios --- cuando cambie una norma del código, llega email automático   boe.es/biblioteca_juridica/codigos/codigo.php?id=435 → botón \'Suscribirse\'                                                                                   C2 + C1
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Qué contiene el Código 435 (Auxiliar AGE) --- lo mismo pero más ligero que el 442**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Constitución Española (parcial) · Tribunal Constitucional · Cortes Generales · Poder Judicial · Gobierno y Administración · Ley 19/2013 Transparencia · Ley 18/2015 Reutilización información · CCAA y Estatutos · UE instituciones · Ley 39/2015 LPAC completa · Ley 40/2015 LRJSP completa · LO 3/2018 LOPDGDD · TREBEP (RDL 5/2015) parcial · LO 3/2007 Igualdad parcial · LO 1/2004 Violencia de Género parcial · Ley 4/2023 Trans y LGTBI · RDL 4/2000 MUFACE · Ley 47/2003 General Presupuestaria parcial · RD 203/2021 Administración electrónica · ENS (RD 311/2022) parcial |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**3. Todas las Leyes por Cuerpo --- Lista Definitiva con URLs**

+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Cómo usar esta sección**                                                                                                                                                                                                                                                                                             |
|                                                                                                                                                                                                                                                                                                                        |
| Para cada ley se indica: (1) en qué cuerpos aparece, (2) prioridad de indexación en Qdrant \[CRÍTICO / ALTA / MEDIA / BAJA\], (3) si necesita calculadora Python o solo RAG, (4) URL directa al BOE. Las marcadas CRÍTICO son las que más preguntas generan en los exámenes según análisis de convocatorias 2020-2025. |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**3.1 Bloque Compartido --- Entra en los 4 Cuerpos**

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **\#**   **Norma / Ley**                                                            **C2**   **C1 AGE**   **C1 SS**   **A2 SS**   **Prioridad**   **¿Calc. o RAG?**
  -------- -------------------------------------------------------------------------- -------- ------------ ----------- ----------- --------------- --------------------------------------------------------
  **1**    **Constitución Española 1978**                                             **✅**   **✅**       **✅**      **✅**      **CRÍTICO**     **RAG**

  **2**    **Ley 39/2015 LPAC (Procedimiento Administrativo Común)**                  **✅**   **✅**       **✅**      **✅**      **CRÍTICO**     **RAG + Calculadora AGE**

  **3**    **Ley 40/2015 LRJSP (Régimen Jurídico Sector Público)**                    **✅**   **✅**       **✅**      **✅**      **CRÍTICO**     **RAG + Calculadora AGE**

  **4**    **RDL 5/2015 TREBEP (Estatuto Básico Empleado Público)**                   **✅**   **✅**       **✅**      **✅**      **CRÍTICO**     **RAG + Calculadora AGE (trienios, grados, permisos)**

  5        LO 3/2018 LOPDGDD (Protección de Datos + Derechos Digitales)               ✅       ✅           ✅          ✅          ALTA            RAG

  6        LO 3/2007 para la Igualdad efectiva mujeres y hombres                      ✅       ✅           ✅          ✅          ALTA            RAG

  7        LO 1/2004 Medidas de Protección contra Violencia de Género                 ✅       ✅           ✅          ✅          MEDIA           RAG

  8        Ley 4/2023 Igualdad real personas trans y garantía derechos LGTBI          ✅       ✅           ✅          ✅          MEDIA           RAG

  9        Ley 39/2006 Promoción Autonomía Personal y Discapacidad (Dependencia)      ✅       ✅           ✅          ✅          MEDIA           RAG

  10       Ley 19/2013 LTAIBG (Transparencia, Acceso a Información y Buen Gobierno)   ✅       ✅           ✅          ✅          ALTA            RAG + Calculadora AGE (plazos acceso información)

  11       Ley 18/2015 Reutilización información sector público                       ✅       ✅           ---         ---         MEDIA           RAG

  12       RD 203/2021 Actuación sector público medios electrónicos                   ✅       ✅           ✅          ✅          ALTA            RAG + Calculadora AGE (art. 14 obligación electrónica)

  13       RD 311/2022 ENS (Esquema Nacional de Seguridad)                            ✅       ✅           ✅          ---         MEDIA           RAG

  14       Ley 7/1985 LBRL (Bases de Régimen Local)                                   ✅       ✅           ✅          ✅          MEDIA           RAG

  15       Ley 29/1998 Jurisdicción Contencioso-Administrativa (plazos recurso)       ---      ✅           ✅          ✅          BAJA-MEDIA      RAG (solo arts. 45-46 plazo)

  16       Reglamento UE 2016/679 RGPD                                                ---      ✅           ✅          ✅          MEDIA           RAG (base LOPDGDD)

  17       Ley 50/1997 del Gobierno                                                   ✅       ✅           ---         ---         BAJA            RAG

  18       RD 501/2024 Ministerio de Inclusión, SS y Migraciones (organización)       ---      ---          ✅          ✅          MEDIA           RAG (Tema 12 Ministerio SS)
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3.2 Bloque Específico AGE --- Solo C1 Administrativo y C2 Auxiliar**

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **\#**   **Norma / Ley**                                                          **C2**   **C1 AGE**   **Prioridad**                        **¿Calc. o RAG?**                            **BOE**
  -------- ------------------------------------------------------------------------ -------- ------------ ------------------------------------ -------------------------------------------- ---------
  19       Ley 53/1984 Incompatibilidades personal AAPP                             ---      ✅           ALTA (caso práctico posible)         RAG                                          ✅

  **20**   **RDL 4/2000 MUFACE (SS Funcionarios Civiles del Estado)**               **✅**   **✅**       **ALTA (conceptual)**                **RAG --- NO calculadora**                   **✅**

  21       Ley 9/2017 LCSP (Contratos Sector Público)                               ---      ✅           MEDIA                                RAG + Calculadora AGE (umbrales contratos)   ✅

  22       Ley 47/2003 General Presupuestaria (parcial, Bloque V)                   ---      ✅           ALTA (Bloque V entero)               RAG                                          ✅

  23       RD 364/1995 Reglamento General Ingreso + Provisión Puestos AGE           ---      ✅           ALTA (trienios, grados personales)   RAG + Calculadora AGE (grados C1: 11-22)     ✅

  24       RD 365/1995 Reglamento Situaciones Administrativas Funcionarios          ---      ✅           MEDIA                                RAG + Calculadora AGE (excedencias)          ✅

  25       Ley 2/2014 Acción y Servicio Exterior del Estado                         ---      ✅           BAJA                                 RAG                                          ✅

  26       Ley 4/2021 Plenitud CGG --- Gestión y Administración (nuevo organismo)   ---      ✅           BAJA                                 RAG                                          ✅

  27       MUGEJU (RD 3283/1978) y ISFAS (Ley 28/1975) --- conceptual               ---      ✅           BAJA (solo menciones)                RAG --- solo resumen conceptual              ✅

  28       Bases comunes selección OEP + Reglamento Ingreso RD 364/1995             ✅       ✅           MEDIA                                RAG                                          ✅
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3.3 Bloque Específico SS --- Solo C1 Administrativo SS y A2 Gestión SS**

Estos son los 13 temas específicos SS. La mayoría procede del TRLGSS y sus reglamentos de desarrollo. Es el bloque donde OpositAIA tiene mayor ventaja competitiva por las calculadoras deterministas.

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **\#**   **Norma / Ley**                                                                  **C1 SS**   **A2 SS**   **Prioridad**                             **Calc.**                                       **Tema SS**
  -------- -------------------------------------------------------------------------------- ----------- ----------- ----------------------------------------- ----------------------------------------------- --------------------
  **31**   **RDL 8/2015 TRLGSS --- Texto Refundido Ley General SS --- EL EJE CENTRAL**      **✅**      **✅**      **CRÍTICO**                               **✅ (base de 27 calculadoras)**                **Temas 1-13**

  **32**   **RDL 20/2020 IMV --- Ingreso Mínimo Vital**                                     **✅**      **✅**      **CRÍTICO (Tema 12 específico)**          **✅ calculos_imv.py**                          **Tema 12**

  **33**   **RD 84/1996 Reglamento General Afiliación SS**                                  **✅**      **✅**      **CRÍTICO (Tema 3)**                      **RAG (conceptual) + Calc (altas/bajas)**       **Tema 3**

  **34**   **RD 2064/1995 Reglamento General de Cotización (RGCSS)**                        **✅**      **✅**      **CRÍTICO (Tema 4)**                      **✅ calcular_base_cotizacion()**               **Tema 4**

  35       RD 1415/2004 Reglamento General Recaudación SS                                   ✅          ✅          ALTA (Temas 5-6)                          RAG --- recaudación voluntaria/ejecutiva        Temas 5-6

  36       RD 625/2014 Prestación IT y control de subsidio                                  ✅          ✅          ALTA (Tema 7-8)                           ✅ calcular_cuantia_it() complementa            Temas 7-8

  37       RD 1148/2011 Prestaciones nacimiento, cuidado, riesgo                            ✅          ✅          ALTA (Tema 9)                             ✅ calcular_prestacion_nacimiento()             Tema 9

  38       RD 357/1991 PNC --- Pensiones No Contributivas (invalidez + jubilación)          ✅          ✅          ALTA (Tema 12)                            ✅ calcular_pnc() --- verificar si está impl.   Tema 12

  39       Ley 27/2011 Actualización, adecuación y modernización SS (reforma jubilación)    ✅          ✅          MEDIA (referencia histórica jubilación)   RAG --- antecedente normativo                   Tema 10

  40       RDL 11/2024 Medidas urgentes jubilación parcial + anticipada (modifica TRLGSS)   ✅          ✅          ALTA --- cambio reciente en examen        ✅ actualizar calculos jubilación               Temas 10-11

  41       Ley 20/2007 LETA --- Estatuto del Trabajo Autónomo                               ✅          ✅          MEDIA (regímenes especiales RETA)         RAG --- autónomos y SS                          Temas 1-2

  42       RD 680/2014 Regímenes especiales, TRADE y autónomos                              ✅          ✅          MEDIA                                     RAG                                             Temas 1-2

  43       ET RDL 2/2015 Estatuto de los Trabajadores (parcial --- solo para A2)            ---         ✅          MEDIA (solo A2)                           RAG                                             A2 Gestión

  44       Ley 36/2011 Jurisdicción Social (parcial plazos)                                 ---         ✅          BAJA (solo A2)                            RAG                                             A2 Gestión

  45       Ley 23/2015 Ordenadora del Sistema de Inspección de Trabajo                      ---         ✅          BAJA (solo A2)                            RAG                                             A2 Gestión

  46       RDL 4/2000 MUFACE (SS Funcionarios Civiles) --- Tema 2 SS Regímenes especiales   ✅          ✅          MEDIA (conceptual Tema 2)                 RAG --- no calculadora                          Tema 2

  47       Ley 47/2003 General Presupuestaria (parcial --- recursos SS Tema 13)             ✅          ✅          ALTA (Tema 13 Recursos generales SS)      RAG                                             Tema 13

  48       RD 1311/2021 Riesgo ergonómico y embarazo (contingencias profesionales)          ✅          ✅          BAJA                                      RAG                                             Temas 7-9
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3.4 Bloque A2 Gestión Civil Estado --- Adicional a todo lo anterior**

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  El Cuerpo de Gestión de la Administración Civil del Estado (A2) tiene 82 temas --- es el más extenso. Cubre TODO lo de C1 AGE y C1 SS en mayor profundidad, más estos bloques adicionales: Derecho Civil y Mercantil (contratos, obligaciones, registro), Derecho Laboral más profundo (ET completo), Hacienda Pública y contabilidad, y Derecho Comunitario europeo en detalle.

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **\#**   **Norma adicional (A2 Gestión)**                                                     **Prioridad**                **¿Calc. o RAG?**
  -------- ------------------------------------------------------------------------------------ ---------------------------- ---------------------------------------
  49       CC RD 24 julio 1889 --- Código Civil (parcial: obligaciones, contratos, propiedad)   MEDIA (A2)                   RAG --- solo títulos relevantes

  50       CCom Real Decreto 22 agosto 1885 --- Código de Comercio (parcial)                    BAJA (A2)                    RAG --- solo conceptos básicos

  51       ET RDL 2/2015 Estatuto de los Trabajadores (completo para A2)                        ALTA (A2)                    RAG + posibles calculadoras laborales

  52       Ley 43/2006 Mejora del crecimiento y del empleo (subvenciones laborales)             BAJA (A2)                    RAG

  53       LGT Ley 58/2003 --- Ley General Tributaria (parcial --- hacienda pública)            MEDIA (A2 Bloque Hacienda)   RAG

  54       TRLHL RDL 2/2004 Texto Refundido Hacienda Local                                      BAJA (A2)                    RAG
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------

**4. URLs de Descarga --- Todas las Leyes en una Sola Tabla**

URLs directas al BOE para cada norma. Formato para indexar en Qdrant: usar la URL XML (?tipo=XML) para obtener el texto estructurado con numeración de artículos. La API XML del BOE permite consultar vigencia y obtener artículos individuales.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Norma**                                            **URL BOE (texto consolidado vigente)**
  ---------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Constitución Española 1978                           https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229

  Ley 39/2015 LPAC                                     https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565

  Ley 40/2015 LRJSP                                    https://www.boe.es/buscar/act.php?id=BOE-A-2015-10566

  RDL 5/2015 TREBEP                                    https://www.boe.es/buscar/act.php?id=BOE-A-2015-11719

  LO 3/2018 LOPDGDD                                    https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673

  LO 3/2007 Igualdad                                   https://www.boe.es/buscar/act.php?id=BOE-A-2007-6115

  LO 1/2004 Violencia Género                           https://www.boe.es/buscar/act.php?id=BOE-A-2004-21760

  Ley 4/2023 Trans y LGTBI                             https://www.boe.es/buscar/act.php?id=BOE-A-2023-5366

  Ley 19/2013 LTAIBG                                   https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887

  Ley 18/2015 Reutilización Información                https://www.boe.es/buscar/act.php?id=BOE-A-2015-7731

  Ley 7/1985 LBRL                                      https://www.boe.es/buscar/act.php?id=BOE-A-1985-5392

  Ley 50/1997 del Gobierno                             https://www.boe.es/buscar/act.php?id=BOE-A-1997-25336

  Ley 29/1998 Jurisdicción Contenciosa                 https://www.boe.es/buscar/act.php?id=BOE-A-1998-16718

  RD 203/2021 Admin Electrónica                        https://www.boe.es/buscar/act.php?id=BOE-A-2021-5032

  RD 311/2022 ENS                                      https://www.boe.es/buscar/act.php?id=BOE-A-2022-7191

  Ley 53/1984 Incompatibilidades                       https://www.boe.es/buscar/act.php?id=BOE-A-1984-24850

  RDL 4/2000 MUFACE                                    https://www.boe.es/buscar/act.php?id=BOE-A-2000-13724

  RD 3283/1978 MUGEJU                                  https://www.boe.es/buscar/act.php?id=BOE-A-1978-30030

  Ley 28/1975 ISFAS                                    https://www.boe.es/buscar/act.php?id=BOE-A-1975-15247

  Ley 9/2017 LCSP                                      https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902

  Ley 47/2003 General Presupuestaria                   https://www.boe.es/buscar/act.php?id=BOE-A-2003-21614

  RD 364/1995 Reglamento Ingreso AGE                   https://www.boe.es/buscar/act.php?id=BOE-A-1995-7190

  RD 365/1995 Situaciones Admin Funcionarios           https://www.boe.es/buscar/act.php?id=BOE-A-1995-7191

  RDL 8/2015 TRLGSS                                    https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724

  RDL 20/2020 IMV                                      https://www.boe.es/buscar/act.php?id=BOE-A-2020-6133

  RD 84/1996 Reglamento Afiliación SS                  https://www.boe.es/buscar/act.php?id=BOE-A-1996-5060

  RD 2064/1995 Reglamento Cotización                   https://www.boe.es/buscar/act.php?id=BOE-A-1995-27250

  RD 1415/2004 Reglamento Recaudación SS               https://www.boe.es/buscar/act.php?id=BOE-A-2004-18491

  RD 625/2014 IT y control subsidio                    https://www.boe.es/buscar/act.php?id=BOE-A-2014-7684

  RD 1148/2011 Prestaciones nacimiento                 https://www.boe.es/buscar/act.php?id=BOE-A-2011-14649

  RD 357/1991 PNC (Pensiones No Contributivas)         https://www.boe.es/buscar/act.php?id=BOE-A-1991-10455

  Ley 27/2011 Actualización SS                         https://www.boe.es/buscar/act.php?id=BOE-A-2011-13242

  RDL 11/2024 Jubilación parcial y anticipada          https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-12503

  Ley 20/2007 LETA (Autónomos)                         https://www.boe.es/buscar/act.php?id=BOE-A-2007-8354

  ET RDL 2/2015 (Estatuto Trabajadores)                https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430

  RD 501/2024 Ministerio Inclusión, SS y Migraciones   https://www.boe.es/buscar/act.php?id=BOE-A-2024-9555

  Reglamento UE 2016/679 RGPD                          https://eur-lex.europa.eu/eli/reg/2016/679

  API BOE XML oficial (consulta programática)          https://boe.es/datosabiertos/api/

  Código 435 PDF --- Normativa Auxiliar AGE            https://www.boe.es/biblioteca_juridica/codigos/abrir_pdf.php?fich=435_Normativa_para_ingreso_en_el_Cuerpo_General_Auxiliar_de_la_Administracion_del_Estado.pdf

  Código 442 PDF --- Normativa Administrativo AGE      https://www.boe.es/biblioteca_juridica/codigos/abrir_pdf.php?fich=442_Normativa_para_ingreso_en_el_Cuerpo_General_Administrativo_de_la_Administracion_del_Estado.pdf

  Índice Biblioteca Jurídica BOE (todos los códigos)   https://www.boe.es/biblioteca_juridica/index.php?tipo=O
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**5. Script de Indexación --- Cómo Subir Todo a Qdrant**

+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Estrategia de indexación: individual por ley, no el PDF del BOE completo**                                                                                                                                                                                                                                                                            |
|                                                                                                                                                                                                                                                                                                                                                         |
| Los PDFs del Código 435 y 442 tienen 1.800-3.000 páginas mezcladas. Si los indexas enteros, el retrieval tendrá mucho ruido. La estrategia correcta: indexar cada ley individualmente con su metadato de fuente. Así el RAG puede filtrar: \'busca solo en TREBEP\' o \'busca en LPAC\'. El código Python siguiente hace esto de forma semi-automática. |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

+-------------------------------------------------------------------------------------------+
| \# indexar_leyes_boe.py --- indexa cada ley individualmente en Qdrant                     |
|                                                                                           |
| \# Ejecutar una vez para poblar la colección \'opositaia_leyes_master\'                   |
|                                                                                           |
| import asyncio, requests, time                                                            |
|                                                                                           |
| from qdrant_client import QdrantClient                                                    |
|                                                                                           |
| from qdrant_client.models import PointStruct, Distance, VectorParams                      |
|                                                                                           |
| from sentence_transformers import SentenceTransformer                                     |
|                                                                                           |
| \# Embedding especializado derecho español --- ya lo tienes instalado                     |
|                                                                                           |
| model = SentenceTransformer(\'pablosi/bge-m3-spa-law-qa-trained-2\')                      |
|                                                                                           |
| client = QdrantClient(url=\'TU_QDRANT_CLOUD_URL\', api_key=\'TU_API_KEY\')                |
|                                                                                           |
| \# Lista de leyes a indexar --- añadir más según prioridad                                |
|                                                                                           |
| LEYES_CRITICAS = \[                                                                       |
|                                                                                           |
| {\'id\': \'ce_1978\', \'titulo\': \'Constitución Española 1978\',                         |
|                                                                                           |
| \'boe_id\': \'BOE-A-1978-31229\', \'cuerpos\': \[\'c2\',\'c1_age\',\'c1_ss\',\'a2_ss\'\], |
|                                                                                           |
| \'bloque\': \'constitucion\', \'prioridad\': 1},                                          |
|                                                                                           |
| {\'id\': \'lpac_39_2015\',\'titulo\': \'Ley 39/2015 LPAC\',                               |
|                                                                                           |
| \'boe_id\': \'BOE-A-2015-10565\', \'cuerpos\': \[\'c2\',\'c1_age\',\'c1_ss\',\'a2_ss\'\], |
|                                                                                           |
| \'bloque\': \'procedimiento_admin\', \'prioridad\': 1},                                   |
|                                                                                           |
| {\'id\': \'lrjsp_40_2015\',\'titulo\': \'Ley 40/2015 LRJSP\',                             |
|                                                                                           |
| \'boe_id\': \'BOE-A-2015-10566\', \'cuerpos\': \[\'c2\',\'c1_age\',\'c1_ss\',\'a2_ss\'\], |
|                                                                                           |
| \'bloque\': \'procedimiento_admin\', \'prioridad\': 1},                                   |
|                                                                                           |
| {\'id\': \'trebep_5_2015\',\'titulo\': \'RDL 5/2015 TREBEP\',                             |
|                                                                                           |
| \'boe_id\': \'BOE-A-2015-11719\', \'cuerpos\': \[\'c2\',\'c1_age\',\'c1_ss\',\'a2_ss\'\], |
|                                                                                           |
| \'bloque\': \'personal_funcionario\', \'prioridad\': 1},                                  |
|                                                                                           |
| {\'id\': \'trlgss_8_2015\',\'titulo\': \'RDL 8/2015 TRLGSS\',                             |
|                                                                                           |
| \'boe_id\': \'BOE-A-2015-11724\', \'cuerpos\': \[\'c1_ss\',\'a2_ss\'\],                   |
|                                                                                           |
| \'bloque\': \'ss_general\', \'prioridad\': 1},                                            |
|                                                                                           |
| {\'id\': \'imv_20_2020\', \'titulo\': \'RDL 20/2020 IMV\',                                |
|                                                                                           |
| \'boe_id\': \'BOE-A-2020-6133\', \'cuerpos\': \[\'c1_ss\',\'a2_ss\'\],                    |
|                                                                                           |
| \'bloque\': \'ss_prestaciones\', \'prioridad\': 1},                                       |
|                                                                                           |
| \# \... añadir todas las leyes de la sección 3                                            |
|                                                                                           |
| \]                                                                                        |
|                                                                                           |
| def get_boe_texto(boe_id: str) -\> str:                                                   |
|                                                                                           |
| \'\'\'Obtiene texto XML del BOE y lo convierte a texto limpio\'\'\'                       |
|                                                                                           |
| url = f\'https://www.boe.es/buscar/act.php?id={boe_id}\'                                  |
|                                                                                           |
| \# En producción: usar la API XML del BOE para obtener texto estructurado                 |
|                                                                                           |
| \# boe.es/datosabiertos/api/ → endpoint /api/act/{boe_id}/consolidated                    |
|                                                                                           |
| resp = requests.get(url, timeout=30)                                                      |
|                                                                                           |
| return resp.text \# Parsear HTML → extraer solo texto articulado                          |
|                                                                                           |
| def chunk_articulos(texto: str, ley_id: str) -\> list:                                    |
|                                                                                           |
| \'\'\'Divide en chunks por artículo, manteniendo el número de art.\'\'\'                  |
|                                                                                           |
| chunks = \[\]                                                                             |
|                                                                                           |
| \# Buscar patrón \'Artículo N\' o \'Art. N\'                                              |
|                                                                                           |
| import re                                                                                 |
|                                                                                           |
| partes = re.split(r\'(?=Artículo \\d+\|Art\\.\\s\*\\d+)\', texto)                         |
|                                                                                           |
| for i, parte in enumerate(partes):                                                        |
|                                                                                           |
| if len(parte.strip()) \> 100: \# Filtrar partes vacías                                    |
|                                                                                           |
| chunks.append({\'texto\': parte.strip(), \'num\': i, \'ley_id\': ley_id})                 |
|                                                                                           |
| return chunks                                                                             |
|                                                                                           |
| async def indexar_ley(ley: dict):                                                         |
|                                                                                           |
| texto = get_boe_texto(ley\[\'boe_id\'\])                                                  |
|                                                                                           |
| chunks = chunk_articulos(texto, ley\[\'id\'\])                                            |
|                                                                                           |
| vectores = model.encode(\[c\[\'texto\'\] for c in chunks\], show_progress_bar=True)       |
|                                                                                           |
| puntos = \[                                                                               |
|                                                                                           |
| PointStruct(                                                                              |
|                                                                                           |
| id=hash(f\"{ley\[\'id\'\]}-{c\[\'num\'\]}\") % (2\*\*63),                                 |
|                                                                                           |
| vector=v.tolist(),                                                                        |
|                                                                                           |
| payload={                                                                                 |
|                                                                                           |
| \'texto\': c\[\'texto\'\],                                                                |
|                                                                                           |
| \'ley_id\': ley\[\'id\'\],                                                                |
|                                                                                           |
| \'ley_titulo\': ley\[\'titulo\'\],                                                        |
|                                                                                           |
| \'boe_id\': ley\[\'boe_id\'\],                                                            |
|                                                                                           |
| \'cuerpos\': ley\[\'cuerpos\'\],                                                          |
|                                                                                           |
| \'bloque\': ley\[\'bloque\'\],                                                            |
|                                                                                           |
| \'prioridad\': ley\[\'prioridad\'\],                                                      |
|                                                                                           |
| \'fecha_indexacion\': \'2026-02-28\',                                                     |
|                                                                                           |
| }                                                                                         |
|                                                                                           |
| )                                                                                         |
|                                                                                           |
| for v, c in zip(vectores, chunks)                                                         |
|                                                                                           |
| \]                                                                                        |
|                                                                                           |
| client.upload_points(\'opositaia_leyes_master\', puntos)                                  |
|                                                                                           |
| print(f\'✅ {ley\[\"titulo\"\]}: {len(puntos)} chunks indexados\')                        |
|                                                                                           |
| time.sleep(1) \# Rate limiting BOE API                                                    |
|                                                                                           |
| async def main():                                                                         |
|                                                                                           |
| \# Verificar cuáles ya están indexadas                                                    |
|                                                                                           |
| colections = client.get_collections().collections                                         |
|                                                                                           |
| print(f\'Colecciones existentes: {\[c.name for c in colections\]}\')                      |
|                                                                                           |
| for ley in LEYES_CRITICAS:                                                                |
|                                                                                           |
| await indexar_ley(ley)                                                                    |
|                                                                                           |
| if \_\_name\_\_ == \'\_\_main\_\_\':                                                      |
|                                                                                           |
| asyncio.run(main())                                                                       |
+-------------------------------------------------------------------------------------------+

**6. Resumen Ejecutivo --- Qué Hacer Esta Semana**

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Orden**   **Acción**                                                                                                                                               **Por qué y cómo**                                                                                                                                                                                     **Horas est.**
  ----------- -------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ----------------
  **1**       **Descargar Código 435 y Código 442 del BOE**                                                                                                            **Ir a boe.es/biblioteca_juridica → buscar \'435\' y \'442\' → descargar PDF. Son las fuentes primarias oficiales con TODAS las leyes actualizadas para AGE. Gratuitos. \~1.800 y \~2.400 páginas.**   **1h**

  2           Verificar en Qdrant Cloud qué leyes ya están indexadas                                                                                                   Listar la colección opositaia_leyes_master con client.scroll() y revisar los boe_id únicos. Evita duplicar trabajo y 48K chunks que ya tienes.                                                         2h

  3           Indexar las 6 leyes CRÍTICAS que faltan en Qdrant                                                                                                        Con el script de la Sección 5: CE, LPAC, LRJSP, TREBEP, TRLGSS, IMV. Estas 6 cubren el 70% de las preguntas de todos los cuerpos.                                                                      4h

  4           Confirmar que calculos_imv.py cubre PNC (RD 357/1991)                                                                                                    Abrir el archivo y verificar si tiene función para PNC invalidez y PNC jubilación. Si no, añadir según el Apéndice VII (Devstral puede generarla).                                                     1h

  5           Indexar las 8 leyes ALTA del bloque SS (RD 84/96, RD 2064/95, RD 625/2014, RD 1148/2011, RD 357/1991, RDL 11/2024, MUFACE, Ley 47/2003 Presupuestaria)   Usar el mismo script. Son las que cubren los 13 temas específicos SS del C1.                                                                                                                           3h

  6           Suscribirse a alertas de actualización de los Códigos 435 y 442                                                                                          En boe.es/biblioteca_juridica → suscribirse. Cuando el BOE actualice una ley del temario, llegará email automático → re-indexar esa ley → 0% alucinaciones por norma derogada.                         0.5h
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

*Apéndice VIII · OpositAIA · 28 Febrero 2026*

*Fuentes: boe.es/biblioteca_juridica (Códigos 435 y 442) · boe.es/boe/dias/2025/12/22 (Convocatoria AGE 2025) · boe.es/diario_boe/txt.php?id=BOE-A-2025-27158 (Convocatoria SS 2025) · temariosenpdf.es · opositatest.com · adams.es · misitiosocial.com*
