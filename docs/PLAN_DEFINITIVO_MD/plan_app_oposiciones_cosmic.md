**PLAN DE DESARROLLO**

App de Oposiciones AGE & Seguridad Social

***Estrategia Create Once, Serve Many (COSMIC)***

Versión 1.0 \| Febrero 2026 \| Basado en BOE dic 2025 -- ene 2026

**0. El Mercado Real: Convocatorias 2026 Verificadas (BOE)**

Esta sección resume los datos oficiales publicados en el BOE entre
diciembre de 2025 y enero de 2026. TODOS los formatos de examen y plazas
son datos verificados, no estimaciones.

**0.1 Mapa de Oposiciones Objetivo (Turno Libre, sin Promoción
Interna)**

  ---------------------------------------------------------------------------------------------
  **Cuerpo**       **Grupo**   **Plazas   **Exam. Nº   **Formato**   **Temas**   **Fecha
                               TL**       Preg.**                                Examen**
  ---------------- ----------- ---------- ------------ ------------- ----------- --------------
  Auxiliar         C2          1.700      60 test +    4 opciones /  28          23 may 2026
  Administrativo                          prác.        práctica                  
  AGE (C2)                                ofimática    Office                    

  Administrativo   C1          2.512      70 test + 20 4 opciones    45          23 may 2026
  AGE (C1)                                supuesto     ambas partes              

  Administrativo   C1          1.056      70 test + 15 4 opciones    36          TBD 2026
  Seg. Social (C1)                        supuesto     ambas partes,             
                                                       120 min                   

  Gestión Seg.     A2          526        90 test +    3 opciones    \~52        TBD 2026
  Social (A2)                             desarrollo   (test) +                  
                                          escrito      respuesta                 
                                                       abierta                   
                                                       (práctico)                
  ---------------------------------------------------------------------------------------------

> *📌 DATO CLAVE: La normativa con fecha límite de estudio es la
> publicada en el BOE hasta el fin del plazo de inscripción de cada
> convocatoria. Para AGE cuerpos generales: 22 enero 2026. Para SS
> Administrativo: 30 enero 2026. Para SS Gestión: 29 enero 2026.*

**0.2 Solapamiento de Contenidos Entre Cuerpos (La Base del COSMIC)**

Este solapamiento es el ACTIVO más valioso de tu estrategia. Contenido
creado una vez que sirve para múltiples cuerpos:

  --------------------------------------------------------------------------------
  **Bloque de            **Aux     **Adm     **Adm     **Gest    **%
  Contenido**            AGE**     AGE**     SS**      SS**      Reutilización**
  ---------------------- --------- --------- --------- --------- -----------------
  Constitución Española  ✅        ✅        ✅        ✅        100%

  Organización del       ✅        ✅        ✅        ✅        100%
  Estado y AGE                                                   

  Derecho Administrativo ✅        ✅        ✅        ✅        100%
  (Ley 39/2015 y                                                 
  40/2015)                                                       

  EBEP / Personal        ✅        ✅        ✅        ✅        100%
  Público                                                        

  Gestión Financiera /   ❌        ✅        ✅        ✅        75%
  Presupuestos                                                   

  Contratación Pública / ❌        ✅        ✅        ✅        75%
  Responsabilidad                                                

  Ofimática /            ✅        ✅        ❌        ❌        50%
  Informática básica                                             

  Seguridad Social       ❌        ❌        ✅        ✅        50%
  específico (LGSS,                                              
  TGSS, prestaciones)                                            

  Recaudación SS /       ❌        ❌        ✅        ✅        50%
  Gestión Recaudatoria                                           
  --------------------------------------------------------------------------------

> *📌 Conclusión: Más del 60% del contenido total es compartido entre
> los 4 cuerpos. Crear una vez y etiquetar es la clave de la
> rentabilidad del proyecto.*

**1. La Estrategia COSMIC en Detalle**

**1.1 Qué Significa Create Once, Serve Many en este Contexto**

COSMIC no significa crear una sola app genérica. Significa crear los
contenidos base (preguntas, temas, esquemas, flashcards) UNA SOLA VEZ
con un sistema de etiquetado inteligente, y que el motor de la app los
sirva automáticamente filtrados para cada cuerpo, perfil de usuario y
momento del estudio.

**El flujo COSMIC tiene 3 capas:**

-   CAPA 1 -- Producción de Contenido: Un humano experto (tú + revisor)
    o IA supervisada genera la pregunta/caso base con metadatos de
    etiquetado.

-   CAPA 2 -- Almacenamiento Etiquetado: Una base de datos relacional
    almacena cada ítem con sus etiquetas de cuerpo, tema, dificultad,
    ley, tipo y formato derivable.

-   CAPA 3 -- Servicio Dinámico: La app sirve el contenido filtrado y
    transformado en tiempo real: un mismo enunciado puede aparecer como
    test, flashcard, meme, o fragmento de simulacro según el módulo
    activo.

**1.2 El Átomo de Contenido: La Unidad Mínima Etiquetada**

Cada pregunta o caso que crees tiene que tener estos metadatos para
funcionar en el sistema COSMIC:

  -----------------------------------------------------------------------------------------------------
  **Campo Metadato**      **Descripción**                **Ejemplo**
  ----------------------- ------------------------------ ----------------------------------------------
  id                      Identificador único            AGE-CONST-00342

  cuerpos\[\]             Array de cuerpos donde aplica  \[\"aux_age\",\"adm_age\",\"adm_ss\"\]

  bloque                  Bloque temático de referencia  BloqueI_Constitucion

  tema_num                Número de tema del programa    3

  ley_base                Ley o artículo que sustenta    CE Art. 14

  dificultad              1=fácil, 2=media, 3=difícil    2

  tipo_examen             test_3op / test_4op /          test_4op
                          desarrollo / calculo           

  formato_derivable\[\]   Formatos que puede adoptar     \[\"test\",\"flashcard\",\"meme_concepto\"\]

  fecha_vigencia          Fecha hasta la que la norma es 2026-01-30
                          válida                         

  revisado_por            Nombre del revisor experto     Preparadora_Maria
  -----------------------------------------------------------------------------------------------------

**2. Formato Real de los Exámenes por Cuerpo (Datos BOE 2025-2026)**

Esta sección es la referencia de diseño para los módulos de tu app. Cada
cuerpo tiene su propio formato de examen y las preguntas deben adaptarse
a él.

**2.1 Auxiliar Administrativo AGE (C2) --- 1.700 plazas --- Examen: 23
mayo 2026**

  -----------------------------------------------------------------------
  **Parámetro**      **Detalle**
  ------------------ ----------------------------------------------------
  Tiempo total       90 minutos

  Parte 1 -- Test    30 preguntas temario + 30 preguntas psicotécnicas =
                     60 preguntas. 4 respuestas alternativas.
                     Penalización: -1/4 por error.

  Parte 2 --         Ejercicio práctico de Word y/o Excel 365 (incluye
  Ofimática          Windows 11 y Copilot desde conv. 2025-2026). No es
                     test, es tarea práctica real.

  Temario            28 temas: Bloque I (16 temas legislación) + Bloque
                     II (12 temas ofimática e informática básica)

  Novedad 2026       Se sustituye Windows 10 por Windows 11. Se añade
                     Microsoft Copilot al Tema 6.
  -----------------------------------------------------------------------

> *📌 IMPLICACIÓN PARA LA APP: Necesitas un módulo de psicotécnicos
> específico (series numéricas, figuras, tablas de datos). No son
> preguntas de temario, son habilidades cognitivas. Además, el módulo de
> ofimática debe ser interactivo o basado en capturas de pantalla.*

**2.2 Administrativo AGE (C1) --- 2.512 plazas --- Examen: 23 mayo
2026**

  -----------------------------------------------------------------------
  **Parámetro**      **Detalle**
  ------------------ ----------------------------------------------------
  Tiempo total       100 minutos (ejercicio único con 2 partes)

  Parte 1 -- Test    70 preguntas. 4 respuestas alternativas.
                     Penalización: -1/4 por error.

  Parte 2 --         20 preguntas sobre supuesto práctico administrativo.
  Supuesto           4 alternativas. Penalización: -1/4.

  Temario            45 temas en 6 bloques: I (11 org. Estado), II (4
                     oficinas), III (7 derecho adm.), IV (9 personal), V
                     (6 fin.), VI (8 informática)

  Dificultad media   Alta. El supuesto práctico requiere aplicar
                     procedimiento y normativa a situaciones concretas.
  -----------------------------------------------------------------------

**2.3 Administrativo Seguridad Social (C1) --- 1.056 plazas**

  -----------------------------------------------------------------------
  **Parámetro**      **Detalle**
  ------------------ ----------------------------------------------------
  Tiempo total       120 minutos (ejercicio único con 2 partes)

  Parte 1 -- Test    70 preguntas. 4 respuestas alternativas.
                     Penalización: -1/4 por error.

  Parte 2 --         15 preguntas sobre supuesto práctico de Seguridad
  Supuesto SS        Social. 4 alternativas. Penalización: -1/4. ⚠️ SON
                     TEST, no desarrollo escrito.

  Temario            36 temas: bloque general (legislación
                     administrativa) + bloque específico SS
                     (prestaciones, recaudación, TGSS)

  Importante         Solo oposición, SIN fase de concurso. Solo cuenta la
                     nota del examen.
  -----------------------------------------------------------------------

**2.4 Gestión Seguridad Social (A2) --- 526 plazas**

  -----------------------------------------------------------------------
  **Parámetro**      **Detalle**
  ------------------ ----------------------------------------------------
  Ejercicio 1 --     90 preguntas. ⚠️ 3 RESPUESTAS ALTERNATIVAS (no 4).
  Test               Penalización activa.

  Ejercicio 2 --     Parte A: 4 preguntas a elegir de 5, sobre Bloque
  Desarrollo         VIII SS. RESPUESTA ESCRITA, no test. Parte B: 1
                     supuesto práctico con 8 preguntas de desarrollo. 180
                     minutos.

  Ejercicio 3 --     Inglés o francés. Opcional para nota pero
  Idioma             obligatorio presentarse.

  Temario            \~52 temas divididos en 8 bloques. El Bloque VIII
                     (SS específico) es el más importante y el único que
                     entra en el Ejercicio 2.

  Implicación app    Necesitas 2 tipos de respuesta: test 3 opciones
                     (Ej. 1) y campo de texto libre / cálculo numérico
                     (Ej. 2).
  -----------------------------------------------------------------------

**3. Plan de Contenido: Cuánto Crear y Cómo Estructurarlo**

**3.1 Cálculo del Banco de Preguntas Test Necesario**

El cálculo parte de las necesidades del opositor tipo que estudia 8-10h
diarias durante 10-14 meses de preparación intensiva:

  -----------------------------------------------------------------------------------
  **Actividad del        **Frecuencia**   **Preguntas/sesión**   **Total en
  Opositor**                                                     preparación**
  ---------------------- ---------------- ---------------------- --------------------
  Tests por tema         2-3 temas/día, 5 20-30 preg.            \~6.000 preg.
  (estudio diario)       días/semana                             

  Simulacros semanales   1/semana, 50     70-90 preg.            \~3.750 preg.
  completos              semanas                                 

  Repaso y revisión (3   Vuelta a todos   variable               \~5.000 preg.
  ciclos)                los temas ×3                            

  TOTAL EXPOSICIÓN                                               \~14.000-15.000
  ESTIMADA                                                       preguntas
  -----------------------------------------------------------------------------------

Para que la repetición perceptible sea inferior a 1,5 veces por
pregunta, el banco mínimo es:

**BANCO MÍNIMO VIABLE = 14.000 preguntas únicas por cuerpo (ratio
repetición \<1,5x)**

**3.2 Distribución de Preguntas por Cuerpo y por Tema**

  -----------------------------------------------------------------------------------------------------------
  **Cuerpo**        **Temas**   **Preg. Test **Preg./tema   **Preg./tema   **Psicot./Práctica**   **TOTAL**
                                TL**         (media)**      bloq. clave**                         
  ----------------- ----------- ------------ -------------- -------------- ---------------------- -----------
  Auxiliar AGE (C2) 28          30 preg.     300 base       500            2.000 psicotéc.        10.400
                                test/exam                   (ofimática)                           test +
                                                                                                  2.000 psic.

  Administrativo    45          70+20        300 base       400 (bloq.     Supuestos prácticos    14.000 test
  AGE (C1)                      preg./exam                  adm.)                                 

  Administrativo SS 36          70+15        350 base       500 (bloq. SS) Supuestos SS (test     14.000 test
  (C1)                          preg./exam                                 4op)                   

  Gestión SS (A2)   \~52        90 preg. (3  280 base       450 (Bloque    Desarrollo escrito     14.000 test
                                op)/exam                    VIII)                                 (3 op)
  -----------------------------------------------------------------------------------------------------------

**3.3 Distribución de Dificultad (El Listón Alto)**

Las academias de éxito trabajan con esta distribución. Tu app debe
replicarla y etiquetarla:

  -----------------------------------------------------------------------
  **Nivel**     **% del       **Descripción**        **Ejemplo tipo**
                banco**                              
  ------------- ------------- ---------------------- --------------------
  1 -- Básico   20%           Definición directa,    ¿Cuántos magistrados
                              concepto aislado, un   tiene el TC?
                              solo artículo.         

  2 -- Medio    50%           Aplicación de norma,   ¿Qué plazo tiene el
                              distinción entre       interesado para
                              artículos similares,   subsanar una
                              plazos.                solicitud incompleta
                                                     según la Ley
                                                     39/2015?

  3 -- Difícil  30%           Cruces entre leyes,    Caso: empresa con 3
                              excepciones a la       trabajadores, 2 de
                              regla, casos con       baja IT y 1 en
                              múltiples variables.   maternidad. ¿Cuál es
                                                     la cotización
                                                     aplicable en el mes
                                                     X?
  -----------------------------------------------------------------------

> *📌 REGLA DE ORO: El nivel 3 (30% de las preguntas) es el que decide
> quién aprueba con plaza y quién no. Prioriza la calidad de estas
> preguntas. Son el diferencial de tu app frente a la competencia.*

**3.4 Banco de Casos Prácticos**

Los casos prácticos son el contenido más valorado y el más difícil de
producir. Se aplican solo a los cuerpos C1 y A2 que tienen segundo
ejercicio práctico:

  ---------------------------------------------------------------------------------------
  **Cuerpo**         **Casos     **Variantes   **Preg./caso**   **Tipología de casos**
                     base**      IA**                           
  ------------------ ----------- ------------- ---------------- -------------------------
  Administrativo AGE 60          180           20 preg.         Procedimiento,
  (C1)                                                          notificaciones, plazos,
                                                                personal, presupuesto

  Administrativo SS  80          240           15 preg. (test   Jubilación, IT,
  (C1)                                         4op)             desempleo, recaudación,
                                                                cotización, IMV

  Gestión SS (A2) -- 60 bloques  --            4 preg.          Epígrafes de desarrollo
  Ej.2 Parte A       temáticos                 desarrollo       del Bloque VIII: teoría
                                                                aplicada

  Gestión SS (A2) -- 100         300+          8 preg. abiertas Supuestos integrales:
  Ej.2 Parte B                                                  empresa con trabajadores,
                                                                prestaciones múltiples,
                                                                deudas con TGSS,
                                                                conflictos laborales
  ---------------------------------------------------------------------------------------

**3.5 Plantilla JSON para Generación de Casos con IA**

Esta estructura permite que una IA pequeña genere variantes
parametrizadas sin inventar normativa. El experto define la estructura
legal, la IA cambia los números y fechas:

+-----------------------------------------------------------------------+
| {                                                                     |
|                                                                       |
| \"id\": \"SS-GEST-047\",                                              |
|                                                                       |
| \"tipo\": \"jubilacion_anticipada_voluntaria\",                       |
|                                                                       |
| \"cuerpos\": \[\"adm_ss\", \"gest_ss\"\],                             |
|                                                                       |
| \"bloque_tema\": \"VIII_Prestaciones_Contributivas\",                 |
|                                                                       |
| \"parametros_variables\": {                                           |
|                                                                       |
| \"fecha_nacimiento\": \"\[\[FECHA\]\]\",                              |
|                                                                       |
| \"anos_cotizados\": \[\[NUM_ANOS\]\],                                 |
|                                                                       |
| \"base_reguladora\": \[\[IMPORTE\]\],                                 |
|                                                                       |
| \"tiene_discapacidad_33\": \[\[BOOL\]\],                              |
|                                                                       |
| \"empresa_con_deuda\": \[\[BOOL\]\]                                   |
|                                                                       |
| },                                                                    |
|                                                                       |
| \"preguntas\": \[                                                     |
|                                                                       |
| { \"id\": 1, \"tipo\": \"calculo\", \"formula\":                      |
| \"edad_jubilacion(cotizados, discapacidad)\", \"articulo\": \"TRLGSS  |
| Art. 208\" },                                                         |
|                                                                       |
| { \"id\": 2, \"tipo\": \"plazo\", \"formula\":                        |
| \"plazo_reclamacion_previa(60_dias_habiles)\", \"articulo\": \"TRLGSS |
| Art. 71\" },                                                          |
|                                                                       |
| { \"id\": 3, \"tipo\": \"normativa\", \"respuesta_fija\": \"Juzgado   |
| de lo Social\", \"articulo\": \"LJS Art. 2\" }                        |
|                                                                       |
| \]                                                                    |
|                                                                       |
| }                                                                     |
+-----------------------------------------------------------------------+

**4. Formatos Derivados: Cómo Servir el Mismo Contenido de 6 Formas**

Esta es la magia del COSMIC. De cada pregunta base con sus metadatos, tu
app genera automáticamente 6 formatos distintos. El contenido se crea
una vez pero se multiplica en valor.

  --------------------------------------------------------------------------
  **Formato**   **Cómo se         **Cuando se usa**    **Complejidad
                genera**                               técnica**
  ------------- ----------------- -------------------- ---------------------
  Test 4        Directo desde la  Estudio por temas,   ⭐ Baja
  opciones      pregunta base     simulacros           

  Test 3        Se elimina el     Exclusivo Gestión SS ⭐⭐ Media
  opciones      distractor más    Ej.1                 
                débil                                  
                automáticamente                        

  Flashcard     Anverso:          Repaso rápido,       ⭐ Baja
                enunciado sin     espacio de memoria   
                opciones.                              
                Reverso:                               
                respuesta                              
                correcta +                             
                explicación.                           

  Esquema /     La IA agrupa      Inicio del tema,     ⭐⭐⭐ Alta
  Mapa Mental   preguntas de un   repaso global        
                tema y genera un                       
                árbol de                               
                conceptos                              

  Meme          La IA toma el     Gamificación,        ⭐⭐⭐ Alta
  educativo     concepto clave de viralidad,           
                la pregunta y     engagement           
                genera una                             
                comparación                            
                humorística o                          
                visual para fijar                      
                el dato difícil                        

  Caso Práctico Plantilla JSON +  Segundo ejercicio,   ⭐⭐⭐ Alta
  Paramétrico   parámetros        simulacros completos 
                aleatorios = caso                      
                único diferente                        
                cada vez                               
  --------------------------------------------------------------------------

> *📌 PRIORIDAD DE IMPLEMENTACIÓN: Empieza con Test 4 opciones y
> Flashcard (más baratos de implementar y más demandados). Añade Mapa
> Mental y Casos Prácticos en la v2. Los Memes en v3 como
> diferenciador.*

**5. Arquitectura de Datos Recomendada**

**5.1 Esquema Relacional Principal**

El sistema debe soportar el etiquetado multidimensional del COSMIC. Este
es el esquema mínimo viable:

  ----------------------------------------------------------------------------
  **Entidad**        **Campos Principales**       **Relaciones Clave**
  ------------------ ---------------------------- ----------------------------
  Cuerpo             id, nombre, grupo            HAS MANY Tema, PreguntaTest
                     (C2/C1/A2), num_temas,       
                     formato_test                 

  Tema               id, cuerpo_id\[\], num_tema, BELONGS TO many Cuerpos, HAS
                     titulo, bloque,              MANY Preguntas
                     leyes_base\[\]               

  PreguntaTest       id, tema_id, enunciado,      BELONGS TO Tema, HAS MANY
                     opcion_a/b/c/d, correcta,    EjecucionUsuario
                     explicacion, dificultad      
                     (1-3), tipo_opciones (3/4),  
                     formatos_derivables\[\],     
                     fecha_vigencia, revisado     

  CasoPractico       id, cuerpos\[\], titulo,     HAS MANY PreguntaCaso, HAS
                     enunciado_base,              MANY VarianteCaso
                     parametros_json, tipo_caso   

  PreguntaCaso       id, caso_id, tipo            BELONGS TO CasoPractico
                     (calculo/plazo/normativa),   
                     enunciado_plantilla,         
                     formula, articulo,           
                     respuesta_modelo             

  Usuario            id, cuerpo_objetivo,         HAS MANY EjecucionUsuario
                     nivel_actual,                
                     historial_preguntas\[\],     
                     racha_dias                   

  EjecucionUsuario   id, usuario_id, pregunta_id, Permite analytics,
                     respuesta_dada, correcta,    repetición inteligente,
                     tiempo_seg, fecha            spaced repetition

  Flashcard          id, pregunta_id (FK),        Derivado automático de
                     anverso, reverso,            PreguntaTest
                     intervalo_repaso,            
                     next_review                  
  ----------------------------------------------------------------------------

**5.2 Regla de Repetición Inteligente (Anti-Saturación)**

El motor de la app no debe servir preguntas al azar. Implementa estas
reglas mínimas desde el día 1:

-   Una pregunta no se repite hasta haber pasado al menos X días
    (configurable por el usuario, mínimo 7).

-   Las preguntas falladas vuelven antes (spaced repetition tipo Anki:
    intervalo corto al principio, se alarga con cada acierto).

-   El simulacro completo nunca repite preguntas vistas en los últimos
    30 días.

-   El usuario puede ver qué porcentaje del banco ha consumido por tema
    (dashboard de progreso).

**6. Pipeline de Generación de Contenido con IA**

**6.1 El Proceso en 5 Pasos**

La IA genera el volumen. El experto garantiza la calidad. Nunca al
revés.

  ---------------------------------------------------------------------------------
  **\#**   **Paso**          **Quién lo hace**          **Output**
  -------- ----------------- -------------------------- ---------------------------
  1        Definición del    Tú + preparador experto    Prompt específico por tema
           Prompt Master                                con artículos de
                                                        referencia, ejemplos de
                                                        preguntas válidas y lista
                                                        de errores a evitar

  2        Generación masiva LLM (Claude Sonnet /       500-1000 preguntas
                             GPT-4o)                    candidatas por tema en
                                                        formato JSON

  3        Revisión y        Revisor experto            Elimina errores normativos,
           filtrado          (preparador o funcionario) preguntas ambiguas,
                                                        distractores imposibles.
                                                        Meta: validar \~60% de las
                                                        generadas.

  4        Enriquecimiento   Script automatizado +      Añade metadatos:
                             revisión manual            dificultad, leyes,
                                                        artículos, formatos
                                                        derivables, fecha vigencia

  5        Carga en BD + QA  Tu pipeline de datos       Test automatizado de
                                                        duplicados, incoherencias,
                                                        preguntas sin respuesta
                                                        correcta clara. Badge:
                                                        Validated.
  ---------------------------------------------------------------------------------

**6.2 Prompt Master de Ejemplo (Para Derecho Administrativo)**

+-----------------------------------------------------------------------+
| **SYSTEM: Eres un experto en preparación de oposiciones a la          |
| Administración General del Estado.**                                  |
|                                                                       |
| TASK: Genera 20 preguntas tipo test sobre el Tema 5 del temario de    |
| Administrativo AGE (C1): Derecho Administrativo -- El acto            |
| administrativo (Ley 39/2015, arts. 34-46).                            |
|                                                                       |
| REGLAS: 1) Cada pregunta tiene exactamente 4 respuestas alternativas, |
| solo una correcta. 2) Los distractores deben ser plausibles           |
| (artículos cercanos, plazos parecidos). 3) Distribución: 4 preguntas  |
| nivel 1, 10 nivel 2, 6 nivel 3. 4) Incluye el artículo concreto de la |
| Ley 39/2015 en la explicación. 5) NO inventes artículos. 6) Formato   |
| JSON estricto.                                                        |
|                                                                       |
| *EVITA: Preguntas con \'Todas las anteriores\' o \'Ninguna de las     |
| anteriores\'. Evita preguntas de memorización de listas largas. Evita |
| preguntas sobre la exposición de motivos.*                            |
+-----------------------------------------------------------------------+

**6.3 Regla de Oro para la Revisión**

+-----------------------------------------------------------------------+
| **⚠️ El Error más Costoso: La Pregunta con Respuesta Correcta         |
| Incorrecta**                                                          |
|                                                                       |
| Si una pregunta tiene marcada como correcta una respuesta que en      |
| realidad es falsa según la ley vigente, el daño no es solo            |
| reputacional: el opositor aprende algo incorrecto, lo lleva al        |
| examen, y pierde puntos. Ese usuario probablemente no renueva. La     |
| revisión por experto no es opcional.                                  |
+-----------------------------------------------------------------------+

**7. Roadmap de Desarrollo por Fases**

**FASE 0 -- Infraestructura y Validación (Semanas 1-4)**

-   Diseño y creación de la base de datos con el esquema de la Sección
    5.

-   Contratar revisor experto: un preparador activo o funcionario del
    cuerpo objetivo. Presupuesto: 300-500€ por cuerpo para revisión del
    lote inicial.

-   Crear los Prompts Master para los 4 cuerpos objetivo.

-   Generar y revisar un lote piloto de 500 preguntas del Tema 1 del
    Auxiliar AGE (Constitución Española). Este lote es el test de
    viabilidad.

-   Definir y probar el pipeline de datos: generación → revisión → carga
    → QA automatizado.

**FASE 1 -- MVP: Auxiliar AGE (Semanas 5-14)**

**Cuerpo objetivo:** Auxiliar Administrativo AGE (C2) --- 1.700 plazas
--- Examen 23 mayo 2026

-   Generar y revisar las 10.400 preguntas test del banco completo (28
    temas × 300-500 preg.)

-   Generar 2.000 preguntas psicotécnicas (series, figuras, tablas).

-   Implementar módulo de test con anti-repetición y penalización
    configurable.

-   Implementar módulo de flashcards (derivado automático del banco).

-   Implementar 5 simulacros completos de examen (60 preguntas: 30
    temario + 30 psicotécnicos).

-   Módulo básico de ofimática: capturas de pantalla de ejercicios
    Word/Excel 365 con respuesta múltiple.

> *📌 VENTANA DE MERCADO: El examen es el 23 de mayo de 2026. Con el MVP
> listo en marzo-abril, tienes 6-8 semanas de venta intensa. Los
> opositores están en modo pánico-compra.*

**FASE 2 -- Cuerpos C1: Administrativo AGE y Administrativo SS (Semanas
10-22)**

-   Reutilizar el 60% del banco de Auxiliar AGE (Bloque I es casi
    idéntico). Solo crear contenido nuevo para Bloques II-VI.

-   Crear banco específico de Seguridad Social para Administrativo SS:
    36 temas × 350-500 preg.

-   Implementar módulo de supuesto práctico con formato test 4 opciones
    (Parte 2 de ambos C1).

-   Crear 60 casos prácticos para Administrativo AGE y 80 para
    Administrativo SS.

-   Añadir módulo de mapas mentales generados por IA.

**FASE 3 -- Gestión SS A2 y Funcionalidades Premium (Semanas 20-30)**

-   Generar banco de 14.000 preguntas tipo test de 3 opciones para
    Gestión SS.

-   Implementar módulo de respuesta abierta/numérica para el Ejercicio 2
    (campo de texto + validación).

-   Crear 100 casos prácticos integrales con sistema de variantes
    paramétricas.

-   Añadir módulo de memes educativos (generación IA de imagen + texto
    para conceptos difíciles).

-   Implementar analytics avanzado: predictor de nota, porcentaje de
    banco consumido, temas débiles.

**8. Resumen Ejecutivo: Los Números del Proyecto**

  ------------------------------------------------------------------------
  **Concepto**             **MVP (Fase 1)**        **Producto Completo
                                                   (Fase 3)**
  ------------------------ ----------------------- -----------------------
  Cuerpos cubiertos        1 (Auxiliar AGE C2)     4 (Aux AGE, Adm AGE,
                                                   Adm SS, Gest SS)

  Plazas del mercado       1.700                   5.794 plazas turno
  cubierto                                         libre

  Preguntas test en banco  12.400 (10.4k + 2k      \~54.000 preguntas
                           psic.)                  únicas

  Casos prácticos          0                       340 casos base + 720
                                                   variantes IA

  Formatos por contenido   2 (test + flashcard)    6 (test, flashcard,
                                                   esquema, meme, caso,
                                                   simulacro)

  Tiempo estimado de       10-14 semanas           28-32 semanas
  desarrollo                                       

  Inversión en revisión    \~500€                  \~2.500-3.500€
  experta                                          

  Ventaja diferencial vs.  Banco más grande +      \+ Variantes
  academias                anti-repetición         paramétricas
                           inteligente             infinitas + analytics
                                                   predictivo
  ------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **🎯 La Propuesta de Valor en Una Frase**                             |
|                                                                       |
| Mientras una academia de pago te da 8.000 preguntas recicladas y te   |
| cobra 800€/año, tu app te ofrece 54.000 preguntas únicas con          |
| repetición inteligente, 6 formatos de aprendizaje, casos prácticos    |
| parametrizados y analytics predictivo --- por una fracción del        |
| precio.                                                               |
+-----------------------------------------------------------------------+

*Documento elaborado con datos verificados del BOE (dic 2025 -- ene
2026)*

*Convocatorias de referencia: Res. 18/12/2025 (AGE) \| BOE 31/12/2025
(Adm SS) \| BOE 30/12/2025 (Gest SS)*
