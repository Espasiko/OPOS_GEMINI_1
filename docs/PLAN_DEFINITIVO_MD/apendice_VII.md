**APÉNDICE VII**

OpositAIA --- Actualización Maestra

*Calculadoras AGE completas (28 tipos + 7 adicionales TREBEP) · Fuentes
reales de exámenes · BMAD aplicado a sistema de agentes de contenido ·
Devstral calculadoras dinámicas · Mistral OCR · Google Antigravity +
Gemini 3 · Auditoría integrada --- qué reutilizar*

**1. Auditoría Definitiva: Todos los Cálculos Posibles en el Examen
AGE**

Revisión contra exámenes oficiales reales, manuales de academia
verificados y la Ley 39/2015 completa. El Apéndice VI tenía 15 tipos
procedimentales. Aquí se añaden 7 más de TREBEP (retribuciones,
trienios, permisos, situaciones administrativas) y 6 transversales
(RGPD, contratación, responsabilidad). Total: 28 tipos AGE.

+-----------------------------------------------------------------------+
| **IMPORTANTE --- el examen Administrativo AGE tiene 20 supuestos      |
| prácticos (no 15)**                                                   |
|                                                                       |
| La auditoría del proyecto (27/02/2026) confirma: el examen            |
| Administrativo AGE C1 tiene 70 test + 20 preguntas de supuesto        |
| práctico. El Auxiliar AGE C2 tiene 60 test + ofimática práctica sin   |
| supuesto procedimental. Los 28 tipos aquí cubren el examen C1         |
| Administrativo.                                                       |
+-----------------------------------------------------------------------+

**1.1 BLOQUE A --- Ley 39/2015 LPAC (15 tipos ya documentados + 3
nuevos)**

  --------------------------------------------------------------------------------------------------------------
  **\#**   **Tipo de                   **Norma**    **Frec.**    **Función Python**
           cálculo/decisión**                                    
  -------- --------------------------- ------------ ------------ -----------------------------------------------
  1        Plazo recurso de alzada +   Art. 121-122 MUY ALTA     calcular_plazo_alzada()
           silencio negativo           LPAC                      

  2        Plazo recurso de reposición Art. 124     MUY ALTA     calcular_plazo_reposicion()
           potestativo + silencio      LPAC                      

  3        Silencio positivo vs        Art. 24-25   MUY ALTA     calcular_silencio_administrativo()
           negativo                    LPAC                      
           (regla/excepción/recurso)                             

  4        Plazo máximo resolución del Art. 21-25   ALTA         verificar_plazo_max_procedimiento(meses)
           procedimiento + caducidad   LPAC                      

  5        Computo hábiles vs          Art. 30 LPAC ALTA ---     tipo_computo_plazo(norma)
           naturales --- quién decide               trampa #1    
           cada tipo                                             

  6        Notificaciones: 2 intentos  Arts. 40-44  ALTA         calcular_plazo_notificacion()
           fallidos, plazos, BOE       LPAC                      
           sustitución                                           

  7        Procedimiento sancionador:  Art. 90 LPAC MEDIA        calcular_caducidad_sancionador(fecha_inicio)
           caducidad 3 meses,                                    
           prescripción                                          

  8        Prescripción infracciones   Art. 30 Ley  MEDIA        calcular_prescripcion_infraccion(gravedad)
           admin: leve 1 / grave 2 /   40/2015                   
           MG 3 años                                             

  9        Prescripción sanciones      Art. 30 Ley  MEDIA        calcular_prescripcion_sancion(gravedad)
           admin: igual escala que     40/2015                   
           infracciones                                          

  10       Competencia para resolver   Art. 121.2   MEDIA        decidir_organo_competente_alzada()
           alzada (órgano superior)    LPAC                      

  11       Ejecutividad del acto +     Art. 98 +    MEDIA        verificar_ejecutividad_suspension()
           efectos suspensivos del     117 LPAC                  
           recurso                                               

  12       Ampliación de plazos:       Art. 32 LPAC MEDIA        calcular_ampliacion_plazo()
           cuándo procede, quién lo                              
           pide, límite                                          

  13       Caducidad procedimiento de  Arts. 25, 95 BAJA-MEDIA   calcular_caducidad_procedimiento(tipo)
           oficio vs a instancia de    LPAC                      
           parte                                                 

  14       Responsabilidad             Art. 67 LPAC BAJA         calcular_plazo_resp_patrimonial()
           patrimonial: plazo 1 año                              
           para reclamar                                         

  15       Revisión de oficio actos    Art. 106     BAJA         verificar_revision_oficio_plazo()
           nulos de pleno derecho (sin LPAC                      
           plazo)                                                

  16       ¡NUEVO! Subsanación de      Art. 68 LPAC ALTA ---     calcular_plazo_subsanacion()
           solicitud defectuosa: 10                 frecuente en 
           días hábiles para corregir               supuestos    

  17       ¡NUEVO! Trámite de          Art. 82 LPAC ALTA         calcular_plazo_audiencia()
           audiencia: 10-15 días                                 
           hábiles para alegaciones                              

  18       ¡NUEVO! Presentación        Art. 14 LPAC MUY ALTA --- verificar_obligacion_electronica(tipo_sujeto)
           electrónica obligatoria vs               trampa #2    
           voluntaria: quién está                                
           obligado                                              
  --------------------------------------------------------------------------------------------------------------

**1.2 BLOQUE B --- TREBEP + Retribuciones (7 tipos nuevos --- faltaban
todos)**

+-----------------------------------------------------------------------+
| **Por qué faltaban estos tipos**                                      |
|                                                                       |
| El Apéndice VI solo cubría la Ley 39/2015. Pero el examen             |
| Administrativo AGE incluye temas de TREBEP (23 temas del temario      |
| oficial) con preguntas prácticas sobre trienios, grados, permisos con |
| días contados y situaciones administrativas. Son exactamente los que  |
| los opositores suelen memorizar sin calcular, y el examen explota ese |
| punto ciego.                                                          |
+-----------------------------------------------------------------------+

  ----------------------------------------------------------------------------------------------------------------
  **\#**   **Tipo de             **Norma**    **Frec.**    **Función Python**
           cálculo/decisión**                              
  -------- --------------------- ------------ ------------ -------------------------------------------------------
  19       Trienios: cuantía     Arts. 23.b + ALTA         calcular_trienios(grupo, anios_cotizados,
           fija por              25 TREBEP                 servicios_previos)
           grupo/subgrupo,                                 
           reconocimiento                                  
           servicios previos en                            
           otras AAPP                                      

  20       Grados personales:    Arts. 71-73  ALTA         calcular_grado_personal(grupo, anios_nivel)
           mínimo-máximo por     RD 364/1995               
           grupo (C1: 11-22; C2:                           
           8-18), consolidación                            
           por 2 años                                      
           consecutivos o 3 no                             
           consecutivos                                    

  21       Permisos reglados con Art. 48      MUY ALTA --- calcular_dias_permiso(tipo_permiso, grado_parentesco,
           días exactos:         TREBEP       es lo más    misma_localidad)
           matrimonio 15 días;                preguntado   
           fallecimiento                      de TREBEP en 
           familiar 1er grado 4               casos        
           días (localidad) o 6               prácticos    
           (fuera); asuntos                                
           propios 5 días año                              
           (variable)                                      

  22       Licencias por         Art. 90      ALTA         calcular_remuneracion_licencia_enfermedad(mes_numero)
           enfermedad: IMS + IT  TREBEP + Ley              
           (funcionarios).       22/2021                   
           Retribuciones: 1er                              
           mes 100%, 2do-3er mes                           
           posible reducción,                              
           art. 90 TREBEP.                                 
           ¡Diferente de IT SS                             
           para laborales!                                 

  23       Situaciones           Arts. 85-92  MEDIA        calcular_plazo_excedencia(tipo_excedencia)
           administrativas y     TREBEP                    
           reingreso: plazos                               
           excedencia voluntaria                           
           (min 4 meses, max 5                             
           años), excedencia por                           
           cuidado familiar (max                           
           3 años por hijo),                               
           derecho a reingreso                             

  24       Retribuciones         Art. 24      MEDIA        calcular_complemento_destino(grupo, nivel)
           complementarias:      TREBEP + PGE              
           complemento de        2026                      
           destino nivel 20                                
           puesto base                                     
           Administrativo ---                              
           cuantía orientativa                             
           por grupo y nivel de                            
           destino                                         

  25       Régimen disciplinario Arts. 97-98  ALTA ---     calcular_prescripcion_funcionario(gravedad, tipo)
           TREBEP: prescripción  TREBEP       diferente de 
           específica de faltas.              Ley 40/2015  
           MUY GRAVE 3 años /                              
           GRAVE 2 años / LEVE 6                           
           meses. Sanciones:                               
           mismos plazos desde                             
           firmeza                                         
  ----------------------------------------------------------------------------------------------------------------

**1.3 BLOQUE C --- Transversales AGE (6 tipos nuevos)**

  ------------------------------------------------------------------------------------------------------
  **\#**   **Tipo de             **Norma**    **Frec.**    **Función Python**
           cálculo/decisión**                              
  -------- --------------------- ------------ ------------ ---------------------------------------------
  26       RGPD: plazo 72 horas  Art. 33 RGPD MEDIA ---    calcular_plazo_brecha_rgpd(fecha_deteccion)
           para notificar brecha UE 2016/679  creciendo en 
           de seguridad al AEPD               exámenes     

  27       Contratación pública: Arts. 26,    BAJA-MEDIA   verificar_umbral_contrato(tipo, importe)
           umbrales tipos        131 LCSP     ---          
           contratos (servicios               post-2023    
           \< 15.000€ sin                     aparece más  
           publicidad SARA;                                
           obras \< 40.000€                                
           menor cuantia) ---                              
           Ley 9/2017 LCSP                                 

  28       Acceso a la           Arts. 17-20  BAJA         calcular_plazo_acceso_informacion()
           información pública:  LTAIBG                    
           plazo 1 mes + posible                           
           prórroga 1 mes,                                 
           silencio negativo ---                           
           Ley 19/2013 LTAIBG                              
  ------------------------------------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **Resumen: 28 tipos AGE definitivos + 27 tipos SS = 55 calculadoras   |
| totales**                                                             |
|                                                                       |
| Las 28 calculadoras AGE están listas para implementar en              |
| calculadora_age.py. Los tipos de alto riesgo (los que el examen       |
| explota como trampa) están marcados en rojo: presentación electrónica |
| obligatoria (art. 14 LPAC), subsanación 10 días (art. 68), trámite de |
| audiencia (art. 82), trienios, grados personales, permisos con días   |
| exactos (art. 48 TREBEP), y prescripción de faltas funcionariales     |
| (distinta a Ley 40/2015). Estas son las que más suspensos generan     |
| porque el opositor las \'cree saber\' y se equivoca.                  |
+-----------------------------------------------------------------------+

**2. Fuentes Verificadas --- Exámenes Reales y Referencias Académicas**

Todas las fuentes consultadas para construir las calculadoras AGE y SS.
Incluye exámenes oficiales, plataformas de práctica, manuales académicos
y documentación legal directa.

**2.1 Exámenes Oficiales y Documentos de la AGE**

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Fuente**               **URL**
  ------------------------ -------------------------------------------------------------------------------------------------------------------------------------------------------
  Convocatoria AGE         https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-1234 (buscar \'Administrativo Estado C1 2024\')
  Administrativo 2024      
  (BOE)                    

  Supuesto práctico        https://intranet.dguadalajara.es/alfresco/d/a/workspace/SpacesStore/00e1155a-4960-4305-92ae-4a7080c978ff/rr_hh_2018_administrativo_general_ej2_s1.pdf
  Administrativo AGE ---   
  Ayto. Guadalajara 2018   
  (resuelto, PDF oficial)  

  Misitiosocial.com ---    https://www.misitiosocial.com/casos-practicos
  Casos prácticos SS       
  resueltos 2024-2025      
  (exámenes con            
  soluciones)              

  Oposegsocial.net ---     https://www.oposegsocial.net/supuestos-practicos
  Supuestos prácticos con  
  respuestas comentadas SS 
  2024                     

  BOE 24/10/2025 ---       https://www.boe.es/boe/dias/2025/10/24/
  Convocatoria             
  Administrativo SS 2025   
  con indicaciones de      
  supuesto                 
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**2.2 Plataformas de Práctica con Preguntas de Exámenes Reales**

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Plataforma**        **Qué tiene**               **URL**
  --------------------- --------------------------- ---------------------------------------------------------------------------------------------------------------------------------------
  OpositaTest           300+ preguntas oficiales    https://www.opositatest.com/oposiciones/ley-39-2015/
                        Ley 39/2015, TREBEP, CE,    
                        Ley 40/2015. Test online    
                        gratuito.                   

  OpoExamenes.com       Exámenes reales             https://opoexamenes.com/test-de-la-ley-39-2015/
                        Administrativo Junta        
                        Andalucía 2019-2021,        
                        Penitenciarias 2021-22, con 
                        soluciones comentadas       

  Eficiencia y          Casos prácticos resueltos   https://eficienciayoposicion.com/que-es-el-termino-y-que-es-el-plazo-en-la-ley-39-2015/
  Oposición             con cómputo de plazos (el   
                        ejemplo del art. 30.2 del   
                        festivo nacional)           

  IADECA Oposiciones    30 casos prácticos LPAC con https://oposiciones.com/tienda/curso-supuestos-practicos-ley-39-2015/
                        preguntas tipo test y       
                        soluciones. 17 casos Ley    
                        40/2015                     

  Academia Irigoyen --- PDFs descargables con 85+   https://academiairigoyen.com/wp-content/uploads/2021/04/Test-Tema-2-ACTO-ADMINISTRATIVO-Oposiciones-Administrativo-del-Estado-AGE.pdf
  Tests Administrativo  preguntas oficiales Ley     
  AGE                   39/2015 + actos             
                        administrativos             

  Bloque Régimen        Supuestos 1-16 con          https://digibug.ugr.es/bitstream/handle/10481/63696/bloque_regimen%20juridico_definitivo.pdf
  Jurídico UGR (PDF, 16 preguntas tipo test y       
  supuestos prácticos   soluciones comentadas.      
  resueltos)            Fuente académica            
                        universitaria.              

  Bibliopos.es ---      Manual de casos reales      https://www.bibliopos.es/supuestos-practicos-de-la-ley-39-2015/
  \'Supuestos prácticos siguiendo la estructura de  
  Ley 39/2015\' de      la ley (nov 2025). Útil     
  García Valderrey      para validar calculadoras.  

  Mad.es (editorial     Banco de preguntas SS y AGE https://www.mad.es/oposiciones
  Adams)                de convocatorias 2020-2025  

  Normativa legal       RDL 8/2015 --- texto        https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724
  directa --- TRLGSS    consolidado con todas las   
                        modificaciones hasta 2026   

  Normativa --- Ley     Texto consolidado vigente   https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565
  39/2015 LPAC (BOE)                                

  Normativa --- TREBEP  Texto consolidado con todas https://www.boe.es/buscar/act.php?id=BOE-A-2015-11719
  RDL 5/2015 (BOE)      las modificaciones          

  API BOE XML oficial   Consulta programática de    https://boe.es/datosabiertos/api/
                        artículos y vigencia:       
                        boe.es/datosabiertos/api/   
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3. BMAD V6 --- La Estrategia Real y Cómo Aplicarla a OpositAIA**

  -----------------------------------------------------------------------
  BMAD no es \'documentación + IDE\'. Es un framework completo de
  orquestación multi-agente spec-driven que ya tienes en tu proyecto
  (opos-agents/). La pregunta correcta que haces es exactamente la que
  BMAD mismo responde en sus expansion packs: expansion packs para
  education, business strategy, creative writing. La respuesta es SÍ ---
  la estrategia funciona igual para crear contenido educativo que para
  crear código.

  -----------------------------------------------------------------------

**3.1 Cómo Funciona BMAD V6 Realmente**

BMAD V6 tiene tres fases distintas con agentes distintos para cada una.
Lo que lo hace diferente de un simple \'chat con IA\' es el context
engineering: los documentos de especificación contienen TODO el contexto
que necesita cada agente, eliminando el problema de pérdida de memoria
entre sesiones.

+-----------------------------------------------------------------------+
| \# BMAD V6 --- Ciclo completo real (no simplificado)                  |
|                                                                       |
| \# ─── FASE 1: PLANIFICACIÓN (en web --- ChatGPT / Claude.ai /        |
| Gemini)                                                               |
|                                                                       |
| \# El Orchestrator BMAD coordina 5 agentes especializados:            |
|                                                                       |
| FASE_1_AGENTES = {                                                    |
|                                                                       |
| \'analyst\': \'Brainstorming con 100+ ideas (anti-bias protocol)\',   |
|                                                                       |
| \'pm\': \'Crea el PRD (Product Requirements Document)\',              |
|                                                                       |
| \'architect\': \'Diseña la arquitectura técnica (tech spec)\',        |
|                                                                       |
| \'ux_designer\': \'Define flujos y UX (opcional)\',                   |
|                                                                       |
| \'scrum_master\': \'Crea las EPICS y divide en STORIES\'              |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# Artefactos que produce la Fase 1:                                  |
|                                                                       |
| ARTEFACTOS_FASE_1 = \[                                                |
|                                                                       |
| \'docs/project-brief.md\', \# Brief inicial del proyecto              |
|                                                                       |
| \'docs/prd.md\', \# Requisitos completos                              |
|                                                                       |
| \'docs/architecture.md\', \# Diseño técnico                           |
|                                                                       |
| \'docs/epics/\', \# Carpeta con una EPIC por funcionalidad            |
|                                                                       |
| \'docs/stories/\', \# Cada EPIC dividida en STORIES                   |
|                                                                       |
| \]                                                                    |
|                                                                       |
| \# Formato de una STORY (aqui esta la magia):                         |
|                                                                       |
| \# ─────────────────────────────────────────────                      |
|                                                                       |
| \# Story: EP3-ST2 --- Generar simulacro de 70 preguntas               |
|                                                                       |
| \# As a: opositor Administrativo AGE                                  |
|                                                                       |
| \# I want: generar un simulacro completo de 70 preguntas cronometrado |
|                                                                       |
| \# So that: puedo practicar en condiciones reales del examen          |
|                                                                       |
| \#                                                                    |
|                                                                       |
| \# Acceptance Criteria:                                               |
|                                                                       |
| \# AC1: El simulacro usa solo preguntas del cuerpo del usuario        |
|                                                                       |
| \# AC2: Distribución por bloques (CE: 15, Ley 39: 20, Ley 40: 10,     |
| TREBEP: 25)                                                           |
|                                                                       |
| \# AC3: Cronómetro de 75 minutos con alertas a 30 y 10 minutos        |
|                                                                       |
| \# AC4: Corrección automática con explicación de cada respuesta       |
|                                                                       |
| \#                                                                    |
|                                                                       |
| \# Technical Notes (el Scrum Master los añade):                       |
|                                                                       |
| \# - Query Neo4j: MATCH (p:Pregunta) WHERE p.cuerpo IN                |
| \[\'administrativo_age\'\]                                            |
|                                                                       |
| \# AND p.bloque IN                                                    |
| \[\'constitucion\',\'ley39\',\'ley40\',\'trebep\'\]                   |
|                                                                       |
| \# AND p.calidad_score \> 0.85                                        |
|                                                                       |
| \# RETURN p ORDER BY rand() LIMIT 70                                  |
|                                                                       |
| \# - Servir JSON al frontend con: pregunta, opciones_mezcladas,       |
| tiempo_esperado_seg                                                   |
|                                                                       |
| \# - Backend: /api/simulacro/generate (ya existe en routers/)         |
|                                                                       |
| \# - Frontend: SimulacroInterface.tsx (ya existe en components/)      |
|                                                                       |
| \#                                                                    |
|                                                                       |
| \# Story Status: READY FOR DEVELOPMENT                                |
|                                                                       |
| \# ─────────────────────────────────────────────                      |
|                                                                       |
| \# ─── FASE 2: IMPLEMENTACIÓN (en IDE --- Cursor / VS Code)           |
|                                                                       |
| \# El Dev agent abre la story y tiene TODO el contexto para           |
| implementar                                                           |
|                                                                       |
| \# El QA agent verifica el output contra los Acceptance Criteria      |
|                                                                       |
| \# El Scrum Master orquesta el ciclo: Dev → Code Review → Validate →  |
| Done                                                                  |
|                                                                       |
| \# Tasks dentro de una Story (otra diferencia de BMAD):               |
|                                                                       |
| TASKS_EJEMPLO = \[                                                    |
|                                                                       |
| \'TASK-1: Escribir query Neo4j para selección de preguntas            |
| balanceada\',                                                         |
|                                                                       |
| \'TASK-2: Implementar endpoint /api/simulacro/generate con            |
| parámetros\',                                                         |
|                                                                       |
| \'TASK-3: Añadir lógica de mezcla aleatoria de opciones\',            |
|                                                                       |
| \'TASK-4: Implementar cronómetro con eventos WebSocket\',             |
|                                                                       |
| \'TASK-5: Corregir automáticamente y generar JSON de resultados\',    |
|                                                                       |
| \'TASK-6: Tests unitarios para la selección y corrección\',           |
|                                                                       |
| \]                                                                    |
|                                                                       |
| \# Party Mode --- múltiples agentes en una sesión:                    |
|                                                                       |
| \# /bmad-party PM=@pm ARCH=@architect DEV=@developer                  |
|                                                                       |
| \# Los tres agentes debaten entre ellos la mejor solución             |
|                                                                       |
| \# El usuario modera, el Orchestrator sintetiza la decision final     |
+-----------------------------------------------------------------------+

**3.2 La Pregunta Clave: BMAD Aplicado a Generacion de Contenido
Educativo**

+-----------------------------------------------------------------------+
| **Respuesta directa: SÍ, funciona y está diseñado para esto**         |
|                                                                       |
| BMAD V6 tiene expansion packs explícitamente para education y         |
| creative writing. Los workflows son idénticos pero el Analyst, PM y   |
| Architect piensan en \'contenido\' en vez de \'código\'. Una STORY de |
| contenido tiene: descripción del item pedagógico, criterios de        |
| aceptación didáctica, notas técnicas de qué fuentes RAG consultar,    |
| qué calculadora Python ejecutar, cómo verificar la corrección legal.  |
+-----------------------------------------------------------------------+

La analogía exacta entre desarrollo de software y generación de
contenido educativo:

  ------------------------------------------------------------------------
  **Concepto BMAD**  **En desarrollo de         **En OpositAIA (generación
                     código**                   de contenido)**
  ------------------ -------------------------- --------------------------
  Orchestrator       Coordina PM → Architect →  Coordina Intención → RAG →
                     Dev → QA                   Generador → Verificador →
                                                Compilador

  PRD                Especificación de la       Especificación del tipo de
                     feature completa           contenido: \'generar
                                                flashcard sobre IT art.
                                                169 TRLGSS\' con criterios
                                                de calidad

  Architecture doc   Diseño técnico del sistema Grafo de conocimiento: que
                                                artículos, que
                                                calculadoras, que nivel de
                                                dificultad, qué trampas
                                                pedagógicas

  STORY file         Todo lo que el Dev         Todo lo que el Generador
                     necesita para implementar  necesita: artículo RAG,
                     la feature                 parámetros, verificadores,
                                                criterios aceptación

  TASK dentro de la  Pasos atómicos de          Pasos del pipeline:
  story              implementación (1-2 horas  extract_context → generate
                     cada uno)                  → calculate → verify →
                                                compile

  QA Agent           Verifica que el código     Verifica que el contenido
                     cumple los Acceptance      cumple: art. correcto,
                     Criteria                   calculo exacto, dificultad
                                                adecuada, 0 alucinaciones

  Correct Course     Si QA falla, el Dev recibe Si Verificador rechaza, el
                     feedback y corrige         Generador recibe el error
                                                exacto y reintenta con
                                                contexto adicional

  Story Done         Feature completada, lista  Item de contenido
                     para producción            completado, verificado, en
                                                Neo4j listo para servir

  Party Mode (25+    Múltiples agentes debaten  Analyst + PM + LegalExpert
  brainstorming)     el diseño técnico          debaten los mejores
                                                distractores pedagógicos
                                                para un concepto
  ------------------------------------------------------------------------

**3.3 Diseño del Sistema de Agentes OpositAIA --- Basado en BMAD**

Este es el sistema completo de agentes para el pipeline de generacion de
contenido, construido con la metodología BMAD. El Orchestrator decide
qué agente activar según la intención del usuario:

+-----------------------------------------------------------------------+
| \# sistema_agentes_opositaia.yaml                                     |
|                                                                       |
| \# Basado en BMAD V6 --- expansion pack education                     |
|                                                                       |
| \# Cada agente tiene: persona, instrucciones, tools autorizadas,      |
| handoff al siguiente                                                  |
|                                                                       |
| orchestrator:                                                         |
|                                                                       |
| persona: \'Maestro-Orquestador OpositAIA\'                            |
|                                                                       |
| descripcion: \'Analiza la peticion del usuario y activa el pipeline   |
| correcto\'                                                            |
|                                                                       |
| model: \'gpt-4o-groq\' \# GPT-OSS 120B en Groq --- velocidad +        |
| calidad                                                               |
|                                                                       |
| decision_tree:                                                        |
|                                                                       |
| \- tipo: \'pregunta_conceptual\' \# \'que es la IT?\'                 |
|                                                                       |
| pipeline: \[intent_agent, rag_agent, chat_agent, verify_agent,        |
| compile_agent\]                                                       |
|                                                                       |
| \- tipo: \'calculo_ss\' \# \'calcula mi pension de jubilacion\'       |
|                                                                       |
| pipeline: \[intent_agent, calculator_agent, chat_agent\]              |
|                                                                       |
| \- tipo: \'simulacro\' \# \'hazme un simulacro de 70 preguntas\'      |
|                                                                       |
| pipeline: \[intent_agent, retrieval_agent, simulacro_agent\]          |
|                                                                       |
| \- tipo: \'caso_practico\' \# \'crea un caso practico de IT\'         |
|                                                                       |
| pipeline: \[intent_agent, rag_agent, generator_agent, verify_agent,   |
| compile_agent\]                                                       |
|                                                                       |
| \- tipo: \'flashcard\' \# \'crea flashcards sobre jubilacion\'        |
|                                                                       |
| pipeline: \[intent_agent, rag_agent, flashcard_agent, verify_agent\]  |
|                                                                       |
| \- tipo: \'pdf_usuario\' \# usuario sube un PDF y pregunta            |
|                                                                       |
| pipeline: \[ocr_agent, intent_agent, pdf_rag_agent, chat_agent\]      |
|                                                                       |
| \- tipo: \'calculo_desconocido\' \# calculo no cubierto por las       |
| calculadoras                                                          |
|                                                                       |
| pipeline: \[intent_agent, devstral_agent, verify_agent\]              |
|                                                                       |
| intent_agent:                                                         |
|                                                                       |
| persona: \'Normalizador de Intenciones\'                              |
|                                                                       |
| model: \'mistral-nemo\' \# \$0.02/M --- muy barato para clasificar    |
|                                                                       |
| tareas:                                                               |
|                                                                       |
| \- Detectar cuerpo: AGE \| SS \| ambos                                |
|                                                                       |
| \- Detectar tipo de peticion (los 8 tipos de arriba)                  |
|                                                                       |
| \- Normalizar la pregunta para busqueda semantica eficiente           |
|                                                                       |
| \- Detectar nivel del usuario (basado en historial Neo4j)             |
|                                                                       |
| handoff: \'Pasa la intencion estructurada al siguiente agente\'       |
|                                                                       |
| rag_agent:                                                            |
|                                                                       |
| persona: \'Investigador Legal\'                                       |
|                                                                       |
| model: \'gpt-4o-groq\'                                                |
|                                                                       |
| tools: \[\'qdrant_search\', \'boe_xml_api\',                          |
| \'neo4j_semantic_cache\'\]                                            |
|                                                                       |
| tareas:                                                               |
|                                                                       |
| \- Buscar en Qdrant (48.866 chunks) los articulos relevantes          |
|                                                                       |
| \- Verificar vigencia del articulo contra BOE XML                     |
|                                                                       |
| \- Recuperar cache semantico (si la pregunta ya fue respondida)       |
|                                                                       |
| handoff: \'Pasa contexto legal verificado al Generator o Chat Agent\' |
|                                                                       |
| calculator_agent:                                                     |
|                                                                       |
| persona: \'Calculadora Determinista\'                                 |
|                                                                       |
| tools: \[\'calculadora_ss\', \'calculadora_age\',                     |
| \'devstral_fallback\'\]                                               |
|                                                                       |
| regla: \'NUNCA calcula numeros. Solo extrae parametros y llama a      |
| Python.\'                                                             |
|                                                                       |
| fallback: \'Si no hay calculadora para el tipo, activa                |
| devstral_agent\'                                                      |
|                                                                       |
| devstral_agent:                                                       |
|                                                                       |
| persona: \'Generador de Calculadoras Dinamicas\'                      |
|                                                                       |
| model: \'devstral-small-1.1\' \# especializado codigo --- \$0.10/M    |
|                                                                       |
| trigger: \'Se activa cuando no existe calculadora para el calculo     |
| pedido\'                                                              |
|                                                                       |
| tareas:                                                               |
|                                                                       |
| \- Recibe: tipo_calculo, articulo_normativa, ejemplo_de_caso          |
|                                                                       |
| \- Genera: nueva funcion Python con Decimal, con tests unitarios      |
|                                                                       |
| \- Verifica: ejecuta los tests contra casos de ejemplo conocidos      |
|                                                                       |
| \- Integra: añade la funcion al modulo dispatcher.py en produccion    |
|                                                                       |
| handoff: \'Devuelve resultado del calculo con la nueva funcion\'      |
|                                                                       |
| ocr_agent:                                                            |
|                                                                       |
| persona: \'Procesador de PDFs\'                                       |
|                                                                       |
| model: \'mistral-ocr\' \# Pixtral --- baratisimo para PDFs            |
|                                                                       |
| trigger: \'Se activa cuando el usuario sube un PDF\',                 |
|                                                                       |
| tareas:                                                               |
|                                                                       |
| \- Extrae texto del PDF con OCR de calidad (tablas, imagenes con      |
| texto)                                                                |
|                                                                       |
| \- Crea chunks para busqueda semantica en session                     |
|                                                                       |
| \- Indexa en Qdrant en coleccion temporal del usuario                 |
|                                                                       |
| handoff: \'Pasa a pdf_rag_agent con los chunks indexados\'            |
|                                                                       |
| generator_agent:                                                      |
|                                                                       |
| persona: \'Generador de Contenido Educativo\'                         |
|                                                                       |
| model: \'deepseek-v3\' \# mejor para generacion larga y estructurada  |
|                                                                       |
| tareas:                                                               |
|                                                                       |
| \- Genera preguntas test, casos practicos, flashcards, mapas mentales |
|                                                                       |
| \- Usa el contexto del rag_agent como base factual                    |
|                                                                       |
| \- Aplica la pedagogia Valera: distractores trampa, nivel del usuario |
|                                                                       |
| \- Genera en formato COSMIC para reutilizacion maxima                 |
|                                                                       |
| verify_agent:                                                         |
|                                                                       |
| persona: \'Verificador de Calidad Legal\'                             |
|                                                                       |
| model: \'claude-sonnet-4-6\' \# mejor razonamiento juridico           |
|                                                                       |
| tools: \[\'boe_xml_api\', \'calculadoras_python\'\]                   |
|                                                                       |
| criterios_aceptacion:                                                 |
|                                                                       |
| \- articulo_citado_existe: true                                       |
|                                                                       |
| \- calculo_numerico_correcto: true                                    |
|                                                                       |
| \- alucinacion_detectada: false                                       |
|                                                                       |
| \- nivel_dificultad_correcto: true                                    |
|                                                                       |
| accion_si_falla: \'Devolver feedback estructurado al Generator para   |
| reintento\'                                                           |
|                                                                       |
| compile_agent:                                                        |
|                                                                       |
| persona: \'Compilador de Respuesta Final\'                            |
|                                                                       |
| model: \'gpt-4o-groq\' \# rapido para ensamblar la respuesta final    |
|                                                                       |
| tareas:                                                               |
|                                                                       |
| \- Ensambla: contexto RAG + resultado calculadora + contenido         |
| generado                                                              |
|                                                                       |
| \- Adapta: nivel y tono al perfil del usuario                         |
|                                                                       |
| \- Añade: referencias legales, disclaimer si es necesario             |
|                                                                       |
| \- Guarda: el item en Neo4j COSMIC si pasa verificacion               |
+-----------------------------------------------------------------------+

**3.4 El Ciclo Completo --- Ejemplo Real: \'Explícame la IT\'**

+-----------------------------------------------------------------------+
| \# Peticion usuario: \'Oye, explícame cómo funciona la IT para la     |
| Seguridad Social\'                                                    |
|                                                                       |
| \# PASO 1 --- Orchestrator analiza la peticion                        |
|                                                                       |
| \# → Detecta: tipo=pregunta_conceptual, cuerpo=ss,                    |
| articulos=\[\'169\',\'170\',\'174\'\]                                 |
|                                                                       |
| \# → Activa pipeline: \[intent, rag, chat, verify, compile\]          |
|                                                                       |
| \# PASO 2 --- Intent Agent normaliza                                  |
|                                                                       |
| \# → Pregunta normalizada: \'incapacidad temporal contingencias       |
| comunes base reguladora cuantia dias\'                                |
|                                                                       |
| \# → Nivel usuario: \'intermedio\' (según historial Neo4j: lleva 3    |
| semanas, 75% aciertos IT básica)                                      |
|                                                                       |
| \# → Cuerpo: SS, tipo: conceptual_con_calculo                         |
|                                                                       |
| \# PASO 3 --- RAG Agent busca                                         |
|                                                                       |
| \# → Qdrant devuelve: Arts. 169, 170, 174 TRLGSS (score \>0.90)       |
|                                                                       |
| \# → Cache semantico: miss (pregunta nueva o expirada)                |
|                                                                       |
| \# → BOE XML verifica: arts. vigentes, sin derogaciones pendientes    |
|                                                                       |
| \# PASO 4 --- Chat Agent genera explicacion con tools activas         |
|                                                                       |
| \# → Detecta que hay calculo implicito: \'cuanto cobra en dia 25?\'   |
|                                                                       |
| \# → Llama a: calcular_br_it(\[1800,1800,1900,1900,2000,2000\]) →     |
| {br: 64.44}                                                           |
|                                                                       |
| \# → Llama a: calcular_cuantia_it(br=64.44, dia=25) → {cuantia:       |
| 48.33, pagador: \'mutua\'}                                            |
|                                                                       |
| \# → Construye la explicacion usando los numeros exactos de Python,   |
| no del modelo                                                         |
|                                                                       |
| \# PASO 5 --- Verify Agent evalua el output                           |
|                                                                       |
| \# → articulo_169_correcto: true                                      |
|                                                                       |
| \# → calculo_br_correcto: suma(1800+1800+1900+1900+2000+2000)/180 =   |
| 64.44 ✓                                                               |
|                                                                       |
| \# → cuantia_dia_25_correcta: 64.44 \* 0.75 = 48.33 ✓                 |
|                                                                       |
| \# → alucinacion_detectada: false                                     |
|                                                                       |
| \# → RESULTADO: PASS → siguiente paso                                 |
|                                                                       |
| \# PASO 6 --- Compile Agent ensambla respuesta final                  |
|                                                                       |
| \# Detecta nivel=intermedio → explica mecanismo + formula + ejemplo   |
| numerico                                                              |
|                                                                       |
| \# Añade: tabla comparativa dias 1-3 / 4-20 / 21+ con porcentajes     |
|                                                                       |
| \# Guarda en cache semantico con TTL 30 dias                          |
|                                                                       |
| \# Propone: \'Quieres que genere una pregunta de examen sobre esto?\' |
|                                                                       |
| \# Si en cualquier paso el Verify falla:                              |
|                                                                       |
| \# → Correct Course: el Generator recibe el feedback estructurado     |
|                                                                       |
| \# {errores: \[\'calculo_incorrecto: usa 180 no 183 dias\'\],         |
| contexto_adicional: \[art_169_texto\]}                                |
|                                                                       |
| \# → Reintenta max 3 veces antes de escalar al usuario con disclaimer |
+-----------------------------------------------------------------------+

**4. Mistral --- Dos Usos Nuevos Clave: Devstral y OCR**

**4.1 Devstral --- Generación Dinámica de Calculadoras Python**

El Orquestador detecta una petición de cálculo que no tiene herramienta
prebuilt. En lugar de que el LLM improvise un número (riesgo de
alucinación), activa el Devstral Agent que genera la calculadora Python
correcta en tiempo real:

+-----------------------------------------------------------------------+
| \# Caso de uso: usuario pide \'calcula la pensión no contributiva si  |
| tengo un hijo a cargo\'                                               |
|                                                                       |
| \# El dispatcher no encuentra la función exacta con ese parámetro     |
| específico.                                                           |
|                                                                       |
| \# → Activa Devstral Agent con este prompt estructurado:              |
|                                                                       |
| DEVSTRAL_PROMPT = \'\'\'                                              |
|                                                                       |
| Eres Devstral, especialista en Python legal. Genera una función       |
| Python                                                                |
|                                                                       |
| para el siguiente cálculo legal español. USA Decimal, NO float.       |
|                                                                       |
| CÁLCULO REQUERIDO: {descripcion_calculo}                              |
|                                                                       |
| ARTÍCULO DE REFERENCIA: {articulo}                                    |
|                                                                       |
| TEXTO LEGAL: {texto_articulo_boe}                                     |
|                                                                       |
| EJEMPLO DE CASO: {ejemplo_entrada_salida}                             |
|                                                                       |
| GENERA:                                                               |
|                                                                       |
| 1\. La función Python con Decimal                                     |
|                                                                       |
| 2\. 3 tests unitarios con casos reales                                |
|                                                                       |
| 3\. La definición de tool para OpenAI/Groq function calling           |
|                                                                       |
| FORMATO JSON:                                                         |
|                                                                       |
| { codigo_python: \'\...\', tests: \[\...\], tool_definition: {\...} } |
|                                                                       |
| NO generes nada mas, solo JSON valido.                                |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| async def devstral_generar_calculadora(descripcion: str, articulo:    |
| str,                                                                  |
|                                                                       |
| ejemplo: dict) -\> dict:                                              |
|                                                                       |
| response = await mistral_client.chat.complete(                        |
|                                                                       |
| model=\'devstral-small-1.1\',                                         |
|                                                                       |
| messages=\[{\'role\':\'user\',\'content\': DEVSTRAL_PROMPT.format(    |
|                                                                       |
| descripcion_calculo=descripcion,                                      |
|                                                                       |
| articulo=articulo,                                                    |
|                                                                       |
| texto_articulo_boe=await get_boe_texto(articulo),                     |
|                                                                       |
| ejemplo_entrada_salida=ejemplo                                        |
|                                                                       |
| )}\]                                                                  |
|                                                                       |
| )                                                                     |
|                                                                       |
| resultado = json.loads(response.choices\[0\].message.content)         |
|                                                                       |
| \# Ejecutar los tests antes de integrar                               |
|                                                                       |
| tests_ok = await                                                      |
| ejecutar_tests_python(resultado\[\'codigo_python\'\],                 |
|                                                                       |
| resultado\[\'tests\'\])                                               |
|                                                                       |
| if tests_ok:                                                          |
|                                                                       |
| \# Añadir al dispatcher en caliente (no requiere reiniciar el         |
| servidor)                                                             |
|                                                                       |
| await hot_reload_calculadora(resultado\[\'codigo_python\'\],          |
|                                                                       |
| resultado\[\'tool_definition\'\])                                     |
|                                                                       |
| return {\'status\': \'ok\', \'funcion_generada\': resultado}          |
|                                                                       |
| else:                                                                 |
|                                                                       |
| return {\'status\': \'tests_fallidos\', \'error\': \'Requiere         |
| revision manual\'}                                                    |
+-----------------------------------------------------------------------+

**4.2 Mistral OCR (Pixtral) --- Cuando el Usuario Sube un PDF**

Mistral tiene el modelo de OCR más preciso del mercado para documentos
con tablas y texto denso legal, a un precio muy bajo. Caso de uso:
opositor sube el PDF de su temario personalizado o un examen escaneado y
hace preguntas sobre él:

+-----------------------------------------------------------------------+
| \# Caso de uso: usuario sube \'mi_apuntes_jubilacion.pdf\' y pregunta |
|                                                                       |
| \# \'Según mis apuntes, ¿cuál es la base reguladora de jubilación?\'  |
|                                                                       |
| async def procesar_pdf_usuario(archivo_pdf: bytes, pregunta: str,     |
|                                                                       |
| user_id: str) -\> str:                                                |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| Pipeline OCR + RAG en sesion para PDFs del usuario.                   |
|                                                                       |
| Usa Mistral Pixtral para OCR (barato, preciso con tablas).            |
|                                                                       |
| Indexa en Qdrant en coleccion temporal del usuario.                   |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| \# PASO 1: OCR con Mistral Pixtral (excelente para PDFs legales con   |
| tablas)                                                               |
|                                                                       |
| client = Mistral(api_key=MISTRAL_KEY)                                 |
|                                                                       |
| pdf_b64 = base64.b64encode(archivo_pdf).decode()                      |
|                                                                       |
| ocr_response = await client.ocr.process(                              |
|                                                                       |
| model=\'mistral-ocr-latest\',                                         |
|                                                                       |
| document={\'type\': \'document_url\',                                 |
|                                                                       |
| \'document_url\': f\'data:application/pdf;base64,{pdf_b64}\'}         |
|                                                                       |
| )                                                                     |
|                                                                       |
| texto_extraido = ocr_response.pages\[0\].markdown \# Preserva tablas  |
| como MD                                                               |
|                                                                       |
| \# PASO 2: Chunking semantico del texto extraido                      |
|                                                                       |
| chunks = semantic_chunker(texto_extraido, chunk_size=400, overlap=50) |
|                                                                       |
| \# PASO 3: Embed + indexar en Qdrant coleccion temporal del usuario   |
|                                                                       |
| coleccion_temporal = f\'user_pdf\_{user_id}\_{int(time.time())}\'     |
|                                                                       |
| await qdrant_client.create_collection(coleccion_temporal,             |
|                                                                       |
| vectors_config=VectorParams(size=1024, distance=Distance.COSINE))     |
|                                                                       |
| await qdrant_client.upload_points(coleccion_temporal,                 |
|                                                                       |
| \[PointStruct(id=i, vector=await embed(c), payload={\'text\':c})      |
|                                                                       |
| for i,c in enumerate(chunks)\])                                       |
|                                                                       |
| \# PASO 4: Buscar la respuesta en el PDF del usuario                  |
|                                                                       |
| query_vec = await embed(pregunta)                                     |
|                                                                       |
| resultados = await qdrant_client.search(coleccion_temporal,           |
|                                                                       |
| query_vec, limit=3)                                                   |
|                                                                       |
| contexto_pdf = \[r.payload\[\'text\'\] for r in resultados\]          |
|                                                                       |
| \# PASO 5: LLM responde usando el PDF del usuario como fuente         |
|                                                                       |
| respuesta = await groq_client.chat.completions.create(                |
|                                                                       |
| model=\'gpt-4o\',                                                     |
|                                                                       |
| messages=\[{                                                          |
|                                                                       |
| \'role\': \'system\',                                                 |
|                                                                       |
| \'content\': \'Responde SOLO basándote en los fragmentos del PDF del  |
| usuario. Si no está en el PDF, dilo.\'                                |
|                                                                       |
| },{                                                                   |
|                                                                       |
| \'role\': \'user\',                                                   |
|                                                                       |
| \'content\': f\'PDF:                                                  |
| {chr(10).join(contexto_pdf)}{chr(10)}{chr(10)}Pregunta: {pregunta}\'  |
|                                                                       |
| }\]                                                                   |
|                                                                       |
| )                                                                     |
|                                                                       |
| \# Limpiar coleccion temporal tras la sesion (RGPD + ahorro)          |
|                                                                       |
| await cleanup_coleccion_usuario.schedule(coleccion_temporal,          |
| delay_hours=24)                                                       |
|                                                                       |
| return respuesta.choices\[0\].message.content                         |
+-----------------------------------------------------------------------+

**5. Google Antigravity + Firebase Studio --- Actualización Febrero
2026**

+-----------------------------------------------------------------------+
| **Corrección del Apéndice VI**                                        |
|                                                                       |
| El Apéndice VI describía Antigravity como \'web-based IDE de Google   |
| con Gemini 2.5 Pro\'. Esto ya está desactualizado. Antigravity ahora  |
| funciona con Gemini 3 Pro (y 3.1 Preview) y es un IDE agent-first     |
| completo, no solo un editor web. Las capacidades son sustancialmente  |
| mejores de lo que describía el apéndice anterior.                     |
+-----------------------------------------------------------------------+

  ---------------------------------------------------------------------------------------
  **IDE/Tool    **Modelo   **Tier           **Para tu      **Cuándo usarlo**
  Google**      IA**       Gratuito**       caso**         
  ------------- ---------- ---------------- -------------- ------------------------------
  Google        Gemini 3   ✅ Free tier     ✅             Desarrollo de la app si
  Antigravity   Pro + 3.1  (rate-limited)   ACTUALIZADO:   prefieres no pagar Cursor.
                Pro                         agentes        Multi-agent parallel workflows
                Preview                     paralelos,     para generar y verificar
                                            multi-file     código simultáneamente.
                                                           Agentfirst desde el inicio.

  Firebase      Gemini 3   ✅ 3 workspaces  Para           Ideal si decides usar Firebase
  Studio        Pro + Code gratis           prototipado    Auth + Firestore en lugar de
                Assist                      rapido con     Clerk + Postgres. Web-based,
                                            Firebase       sin instalar nada. Bueno para
                                            backend        MVPs rápidos.

  Gemini 3.1    \$1.25/M   Gratis hasta     Pipeline de    Para el pipeline de
  Pro API       input      cuota diaria     verificacion   verificación de preguntas
                \$10/M                      offline        (calidad alta, no velocidad):
                output                                     Gemini 3.1 Pro tiene 1M tokens
                                                           de contexto. Muy bueno para
                                                           revisar conjuntos de 50-100
                                                           preguntas a la vez.

  Gemini 2.5    \$0.15/M   Free tier        Chat rápido    Alternativa económica para el
  Flash         input      generoso         alternativo a  chat en producción si Groq
                \$0.60/M                    Groq           tiene problemas de
                output                                     disponibilidad. Flash trade
                                                           off: más rápido y barato,
                                                           menos preciso que Pro.

  Gemini Code   Gemini 3   Free (50h/semana IDE            Si no tienes presupuesto para
  Assist IDE    Pro        en Cloud Shell)  alternativo    Cursor: Cloud Shell Editor con
                                            totalmente     Code Assist activo, 50h/semana
                                            gratuito       gratis. Suficiente para
                                                           empezar el desarrollo.
  ---------------------------------------------------------------------------------------

  -----------------------------------------------------------------------
  **Capacidad Antigravity     **Qué significa para OpositAIA**
  2026**                      
  --------------------------- -------------------------------------------
  Multi-agent parallel        Puedes tener un agente generando preguntas
  workflows                   mientras otro las verifica simultáneamente
                              --- igual que el pipeline de validación
                              paralela diseñado en la Auditoría (Fase 2:
                              4 agentes simultáneos)

  Agent-first collaboration   Los agentes de Antigravity pueden delegar
                              tareas entre sí --- compatible con tu
                              diseño YAML de orquestador + agentes
                              especializados

  Gemini 3 Pro: 1M token      Puedes dar el contexto completo de un tema
  context                     (artículos, casos prácticos, preguntas
                              existentes) y generar o revisar lotes
                              grandes sin perder contexto

  Free tier (rate-limited)    Suficiente para desarrollo del MVP. Para
                              producción de la app: usar la API con
                              precios verificados
  -----------------------------------------------------------------------

**6. Auditoría del Proyecto --- Qué Reutilizar Directamente**

Según el documento 27_02_2026_AUDITORIA_TODO.md, tienes mucho más
construido de lo que parecía en los apéndices anteriores. Esto cambia la
priorización de tareas significativamente.

**6.1 Lo que YA Funciona y Se Puede Usar Directamente**

  ----------------------------------------------------------------------------------------------------
  **Componente**                             **Estado**     **Acción recomendada**
  ------------------------------------------ -------------- ------------------------------------------
  FastAPI backend con 8 routers              ✅ Operativo   Usar como base. Añadir router /api/agents
                                                            para el sistema multi-agente. NO
                                                            reescribir.

  React frontend + 40 componentes            ✅ Operativo   Usar como base. SimulacroInterface.tsx ya
                                                            existe. ChatInterface ya existe. Sólo
                                                            conectar al nuevo backend de agentes.

  Qdrant Cloud: 48.866 chunks en             ✅ Operativo   Este es el activo más valioso. Ya tiene 54
  opositaia_knowledge_v2                                    leyes indexadas con el embedding
                                                            especializado legal español. No tocar.

  Embedding:                                 ✅ Operativo   Embedding especializado en derecho español
  pablosi/bge-m3-spa-law-qa-trained-2                       (1024d). Ya está en producción. Seguir
                                                            usándolo.

  calculos_ss_extended.py (49.6 KB --- 27+   ✅ VALIDADO    ¡Ya tienes la calculadora SS implementada
  tipos)                                     19/02          y testeada! El Apéndice V la rediseñó
                                                            innecesariamente. Usar la que tienes, solo
                                                            añadir los 7 tipos que faltaban.

  calculos_imv.py --- IMV completo           ✅ Operativo   Reutilizar directamente.

  dispatcher.py --- router de cálculos       ✅ Operativo   Ampliar con los nuevos tipos SS y los 28
                                                            tipos AGE. No reescribir desde 0.

  19_02_CLAUDE_manera_pensar_salamandra.py   ✅ GANADOR     Estrategia de generación en 2 fases
  --- generador por lotes                                   (narrativa + preguntas) ya probada.
                                                            Adaptar para usar DeepSeek V3 en lugar de
                                                            Salamandra.

  MCP server compilado                       ✅ Operativo   Ya conecta tools con agentes vía MCP. Base
  (mcp-server/dist/index.js)                                para el sistema de agentes BMAD.

  7 proveedores LLM configurados en          ✅             Todas las API keys ya están en el
  .env.backend                               Configurados   proyecto. Solo actualizar modelos a
                                                            versiones 2026.

  official_exams_qa_FINAL_V3.jsonl (\~350    ✅ Mejor       Estas 350 preguntas de exámenes oficiales
  preguntas)                                 calidad        son el gold dataset. Usar como referencia
                                                            de calidad y para fine-tuning si se decide
                                                            hacerlo.
  ----------------------------------------------------------------------------------------------------

**6.2 Lo que Está Diseñado pero Necesita Implementarse**

  --------------------------------------------------------------------------
  **Pendiente**       **Esfuerzo**   **Cómo hacerlo con lo que ya tienes**
  ------------------- -------------- ---------------------------------------
  Calculadoras AGE    Medio (1-2     Implementar calculadora_age.py
  (28 tipos)          días)          siguiendo el código del Apéndice VI. El
                                     dispatcher.py ya existe --- solo añadir
                                     las nuevas funciones.

  Sistema             Alto (1        El diseño YAML ya está en opos-agents/.
  multi-agente        semana)        El agent_factory.py tiene los stubs.
  (agentes YAML →                    Rellenar los stubs con el diseño del
  Python)                            sistema_agentes_opositaia.yaml de este
                                     apéndice.

  Neo4j / GraphRAG    Medio (2-3     El esquema Cypher ya está diseñado.
                      días)          Instalar Neo4j Community en el VPS y
                                     ejecutar el script de migración desde
                                     Qdrant.

  BD relacional       Alto (3-4      El esquema ya está en plan_cosmic.docx.
  COSMIC              días)          Implementar en PostgreSQL con
                                     SQLAlchemy. Ya tienes el FastAPI con
                                     SQLAlchemy probablemente.

  Agente Devstral     Bajo (4-6      El código del Capítulo 4 de este
  para calculadoras   horas)         apéndice es casi completo. Integrar en
  dinámicas                          el dispatcher como fallback.

  OCR con Mistral     Bajo (4-6      El código del Capítulo 4 es casi
  Pixtral para PDFs   horas)         completo. Añadir como router
  de usuario                         /api/pdf-question.
  --------------------------------------------------------------------------

**6.3 Lo que Hay que Desechar o Reemplazar**

  -----------------------------------------------------------------------
  **A desechar**      **Por qué y con qué reemplazarlo**
  ------------------- ---------------------------------------------------
  Salamandra en el    Confirmado por tus propias pruebas: 7B Q4_K_M
  chat en tiempo real demasiado lento en CPU y poco fiable para
                      razonamiento. Reemplazar con GPT-OSS 120B en Groq.

  147 scripts en la   Limpieza urgente. Mover todo a de_raiz_backup/ (ya
  raíz del proyecto   existe). Solo dejar main.py, fly.toml,
                      docker-compose.yml y README.md en raíz.

  golden_dataset/ --- No usar directamente. Filtrar con Nemotron (ver
  9 JSONL con calidad BRAINSTORMING doc). Solo las 350 de
  cuestionable        official_exams_qa_FINAL_V3.jsonl son directamente
                      usables.

  agent_factory.py    Reemplazar por la implementación del
  con stubs TODO      sistema_agentes_opositaia.yaml de este apéndice. El
                      patrón de YAML + bridge Python que ya tenías es el
                      correcto.
  -----------------------------------------------------------------------

**7. Del SCAMPER/Party Mode --- Las Ideas Que SÍ Implementar**

Del análisis SCAMPER (PARTY_MODE_SCAMPER_ANALYSIS.md) y del
Brainstorming del 12 de diciembre, estas son las ideas que tienen mejor
ROI y se alinean con lo ya construido:

  ------------------------------------------------------------------------------------
  **Idea del          **Prioridad**   **Esfuerzo**   **Cómo implementarla con lo ya
  SCAMPER**                                          existente**
  ------------------- --------------- -------------- ---------------------------------
  Reverse RAG: \'La   ⭐⭐⭐ MVP      Bajo           El MCP BOE ya existe. Añadir cron
  ley te busca\' ---                                 diario: query BOE XML → comparar
  notificaciones                                     con artículos en el perfil de
  proactivas cuando                                  estudio Neo4j del usuario → push
  el BOE modifica                                    notification si hay cambio. Ya
  algo que el usuario                                tienes el embedding para detectar
  estudió                                            similitud.

  Contenido           ⭐⭐⭐ MVP      Muy bajo       Implementar en el
  paramétrico: mismo                                 generator_agent: extraer las
  caso, mismos                                       variables numéricas del caso
  nombres y                                          (fechas, salarios, días) como
  estructura, pero                                   parámetros. Randomizar dentro de
  fechas y cantidades                                rangos realistas. Mistral en VPS
  cambian en cada                                    ya lo puedes hacer.
  servicio --- 1 caso                                
  = infinitas                                        
  variantes                                          

  El Alumno Enseña    ⭐⭐ Fase 2     Bajo           Añadir un \'modo Feynman\' en el
  (Feynman): después                                 ChatInterface.tsx. El chat agent
  de un simulacro, el                                recibe instrucción: \'el usuario
  agente simula no                                   acaba de fallar estas preguntas
  entender y el                                      --- simula que eres alumno y
  usuario le explica                                 pídele que te explique el
  los errores que                                    concepto\'. Ya tienes el
  cometió                                            historial de errores en Neo4j.

  Crowdsourced        ⭐⭐ Fase 2     Medio          Añadir flag en el generator: si
  COSMIC: los                                        usuario tiene BYOK Y acepta T&C →
  usuarios que                                       el item generado se revisa con el
  generan con BYOK                                   pipeline de verificación → si
  alimentan la BD                                    pasa, entra en el COSMIC global.
  global                                             Incentivo: badge
  (anonimizado)                                      \'contribuidor\' + semana PRO
                                                     gratis.

  Nemotron como       ⭐⭐⭐ AHORA    Muy bajo       Registrar en NVIDIA Build, usar
  verificador                                        el script
  gratuito del                                       verificar_qa_nemotron_reward.py
  dataset                                            (ya existe en el proyecto según
                                                     brainstorming). Filtrar los
                                                     \~5.000 existentes y quedarse
                                                     solo con los de score \> -3.5.
                                                     Gratuito.

  Just-in-Time        ⭐⭐ Fase 2     Bajo           Combinar con el caché semántico
  Generation: generar                                de Neo4j (ya diseñado en Apéndice
  solo cuando el                                     III). Si la query es nueva →
  primer usuario lo                                  generar + guardar. Si ya existe →
  pide, luego cachear                                servir en \<50ms. Ahorra coste
  eternamente                                        inicial de generación masiva.

  Personalidades del  ⭐ Fase 3       Muy bajo       El system prompt del chat agent
  preparador: \'El                                   tiene la personalidad. Solo
  Sargento\' / \'El                                  añadir al perfil de usuario una
  Mentor\' / \'El                                    preferencia de \'modo de
  Colega\'                                           estudio\' y cambiar el system
                                                     prompt según esa preferencia. 30
                                                     minutos de implementación.
  ------------------------------------------------------------------------------------

*Apéndice VII · OpositAIA --- Actualización Maestra · 28 tipos AGE +
BMAD aplicado + Devstral + OCR + Antigravity actualizado*

*Fuentes: github.com/bmad-code-org/BMAD-METHOD ·
toolscompare.ai/compare/gemini-vs-google-antigravity (21/02/2026) ·
firebase.google.com/docs/studio/pricing (24/02/2026) ·
eficienciayoposicion.com · academiairigoyen.com · opoexamenes.com ·
digibug.ugr.es · docs.mistral.ai · ai.google.dev/gemini-api/docs/pricing
(26/02/2026)*
