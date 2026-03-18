**APÉNDICE VI**

App Oposiciones AGE & SS --- Actualización Integral

*AGE vs SS --- qué cambia en los casos prácticos · Calculadoras AGE
procedimentales · Mistral (precios verificados, cuándo usarlo) · IDEs
con IA para desarrollar · BMAD como metodología · Function calling entre
modelos · Plan V2 revisado*

**1. El Error Crítico que Faltaba: AGE y SS Tienen Casos Prácticos
Completamente Distintos**

+-----------------------------------------------------------------------+
| **⚠️ DESCUBRIMIENTO IMPORTANTE --- El Apéndice V cubría solo SS**     |
|                                                                       |
| Los 27 tipos de calculadora del Apéndice V corresponden al examen de  |
| SEGURIDAD SOCIAL. El examen de AGE tiene un caso práctico             |
| completamente diferente: no calcula prestaciones, sino que aplica     |
| procedimiento administrativo. Son dos exámenes distintos que          |
| requieren dos tipos de calculadoras distintas.                        |
+-----------------------------------------------------------------------+

  ------------------------------------------------------------------------------------
                     **Cuerpo Administrativo      **Cuerpo Administrativo Seguridad
                     AGE**                        Social**
  ------------------ ---------------------------- ------------------------------------
  Parte 1            70 preguntas teóricas:       70 preguntas teóricas: mismas + 13
                     Constitución, Ley 39/2015,   temas específicos TRLGSS (Seguridad
                     Ley 40/2015, TREBEP, RGPD,   Social)
                     Igualdad                     

  Parte 2            15 preguntas CASO PRÁCTICO   15 preguntas CASO PRÁCTICO de
                     de PROCEDIMIENTO             PRESTACIONES SS: IT, jubilación,
                     ADMINISTRATIVO: plazos,      desempleo, IP, viudedad --- cálculos
                     recursos, silencio,          con números reales
                     notificaciones, régimen      
                     disciplinario                

  **Calculadoras**   **Calculadoras de plazos y   **Calculadoras de prestaciones
                     procedimiento (Ley 39/2015,  (TRLGSS) --- ya en Apéndice V**
                     TREBEP)**                    
  ------------------------------------------------------------------------------------

**1.1 Los Tipos de Caso Práctico AGE --- Qué Puede Caer**

El caso práctico de AGE describe una situación administrativa
(funcionario sancionado, solicitud con silencio, recurso presentado
fuera de plazo\...) y hace 15 preguntas sobre qué recursos proceden, en
qué plazo, qué órgano es competente, qué efecto tiene el silencio, etc.
No hay aritmética compleja, pero sí hay plazos que calcular con
precisión:

  -----------------------------------------------------------------------------
  **\#**   **Cálculo / Decisión   **Norma**     **Frecuencia en examen**
           procedimental**                      
  -------- ---------------------- ------------- -------------------------------
  1        Plazo para interponer  Art. 121 Ley  MUY ALTA --- en casi todos los
           recurso de alzada      39/2015       casos

  2        Plazo para interponer  Art. 124 Ley  MUY ALTA
           recurso de reposición  39/2015       
           potestativo                          

  3        Silencio               Art. 24 Ley   MUY ALTA --- trampa favorita
           administrativo         39/2015       
           positivo o negativo                  
           (distinción                          
           regla/excepción)                     

  4        Plazo máximo de        Arts. 21-25   ALTA
           resolución del         Ley 39/2015   
           procedimiento y                      
           silencio por caducidad               
           vs por falta de                      
           resolución                           

  5        Cómputo de plazos en   Art. 30 Ley   ALTA --- es la trampa más
           días hábiles vs días   39/2015       frecuente
           naturales (quién                     
           decide cada tipo)                    

  6        Notificaciones: 2      Arts. 40-44   ALTA
           intentos fallidos →    Ley 39/2015   
           publicación BOE;                     
           plazos para intentar                 

  7        Procedimiento          Art. 90 Ley   MEDIA
           sancionador: caducidad 39/2015       
           a los 3 meses sin                    
           resolución                           

  8        Prescripción de        Art. 30 Ley   MEDIA
           infracciones: leve 1   40/2015       
           año / grave 2 años /                 
           muy grave 3 años                     

  9        Prescripción de        Art. 30 Ley   MEDIA
           sanciones: leve 1 año  40/2015       
           / grave 2 años / muy                 
           grave 3 años                         

  10       Régimen disciplinario  Arts. 93-98   MEDIA
           TREBEP: faltas         TREBEP        
           graves/muy graves,                   
           suspensión, separación               

  11       Competencia para       Art. 121.2    MEDIA
           resolver el recurso de Ley 39/2015   
           alzada (órgano                       
           superior jerárquico)                 

  12       Ejecutividad del acto  Art. 98 +     MEDIA
           y efecto suspensivo    Art. 117 Ley  
           del recurso            39/2015       

  13       Caducidad del          Arts. 25 y 95 BAJA-MEDIA
           procedimiento iniciado Ley 39/2015   
           de oficio vs a                       
           instancia de parte                   

  14       Responsabilidad        Art. 67 Ley   BAJA
           patrimonial: plazo 1   39/2015       
           año para reclamar                    
           (art. 67 Ley 39/2015)                

  15       Revisión de oficio de  Art. 106 Ley  BAJA
           actos nulos de pleno   39/2015       
           derecho (sin plazo)                  
  -----------------------------------------------------------------------------

**1.2 Calculadora Procedimental AGE --- calculadora_age.py**

+-----------------------------------------------------------------------+
| \# calculadora_age.py --- Cálculos procedimentales para examen AGE    |
|                                                                       |
| \# Norma principal: Ley 39/2015 LPAC + Ley 40/2015 LRJSP + TREBEP     |
|                                                                       |
| \# El LLM NUNCA decide plazos de memoria. Siempre llama a estas       |
| funciones.                                                            |
|                                                                       |
| from datetime import date, timedelta                                  |
|                                                                       |
| from typing import Optional                                           |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| \# TIPO AGE-1: RECURSO DE ALZADA                                      |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| def calcular_plazo_alzada(fecha_notificacion: str) -\> dict:          |
|                                                                       |
| \'\'\'1 mes en días hábiles desde notificación --- Art. 121           |
| LPAC\'\'\'                                                            |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'plazo\': \'1 mes en días hábiles\',                                 |
|                                                                       |
| \'tipo_dias\': \'HÁBILES (excluyen domingos, festivos nacionales y    |
| del municipio)\',                                                     |
|                                                                       |
| \'inicio_computo\': f\'Día siguiente a la notificación                |
| ({fecha_notificacion})\',                                             |
|                                                                       |
| \'organo_competente\': \'Superior jerárquico del que dictó el acto\', |
|                                                                       |
| \'efecto_silencio\': \'Desestimatorio (negativo) --- Art. 122.1       |
| LPAC\',                                                               |
|                                                                       |
| \'articulo\': \'Art. 121-122 Ley 39/2015\'                            |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| \# TIPO AGE-2: RECURSO DE REPOSICIÓN                                  |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| def calcular_plazo_reposicion(fecha_notificacion: str) -\> dict:      |
|                                                                       |
| \'\'\'1 mes en días hábiles (potestativo, previo al contencioso) ---  |
| Art. 124 LPAC\'\'\'                                                   |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'plazo\': \'1 mes en días hábiles\',                                 |
|                                                                       |
| \'tipo_dias\': \'HÁBILES\',                                           |
|                                                                       |
| \'caracter\': \'POTESTATIVO --- no es obligatorio antes de recurrir   |
| al TS\',                                                              |
|                                                                       |
| \'efecto_silencio\': \'Desestimatorio (negativo) --- Art. 124.3       |
| LPAC\',                                                               |
|                                                                       |
| \'plazo_silencio\': \'1 mes sin resolución = desestimado por          |
| silencio\',                                                           |
|                                                                       |
| \'articulo\': \'Art. 124 Ley 39/2015\'                                |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| \# TIPO AGE-3: SILENCIO ADMINISTRATIVO                                |
|                                                                       |
| \# La trampa más frecuente del examen AGE                             |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| def calcular_silencio_administrativo(tipo_procedimiento: str,         |
|                                                                       |
| es_recurso: bool = False) -\> dict:                                   |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| REGLA GENERAL (Art. 24 LPAC):                                         |
|                                                                       |
| --- Procedimientos iniciados a SOLICITUD: silencio POSITIVO (salvo    |
| excepciones)                                                          |
|                                                                       |
| --- Procedimientos iniciados DE OFICIO: silencio NEGATIVO             |
|                                                                       |
| --- RECURSOS: siempre NEGATIVO (art. 122 y 124)\',                    |
|                                                                       |
| tipo_procedimiento: \'solicitud_particular\' \| \'oficio\' \|         |
| \'recurso\' \| \'sancionador\'                                        |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| if es_recurso:                                                        |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'silencio\': \'NEGATIVO (desestimatorio)\',                          |
|                                                                       |
| \'razon\': \'Los recursos siempre producen silencio negativo (arts.   |
| 122, 124 LPAC)\',                                                     |
|                                                                       |
| \'articulo\': \'Arts. 122.1 y 124.3 Ley 39/2015\'                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| SILENCIO_POR_TIPO = {                                                 |
|                                                                       |
| \'solicitud_particular\': {                                           |
|                                                                       |
| \'silencio\': \'POSITIVO (estimatorio) --- REGLA GENERAL\',           |
|                                                                       |
| \'excepciones\': \[\'Derecho de petición\', \'Silencio negativo       |
| establecido por norma de rango legal\', \'Actos de transferencia al   |
| solicitante de facultades de dominio público\', \'Actos que impliquen |
| ejercicio de actividades que puedan dañar el medio ambiente\'\],      |
|                                                                       |
| \'articulo\': \'Art. 24 Ley 39/2015\'                                 |
|                                                                       |
| },                                                                    |
|                                                                       |
| \'oficio\': {                                                         |
|                                                                       |
| \'silencio\': \'NEGATIVO (desestimatorio) --- CADUCIDAD\',            |
|                                                                       |
| \'razon\': \'Procedimientos iniciados de oficio: caducidad si no se   |
| resuelve en plazo máximo\',                                           |
|                                                                       |
| \'articulo\': \'Art. 25 Ley 39/2015\'                                 |
|                                                                       |
| },                                                                    |
|                                                                       |
| \'sancionador\': {                                                    |
|                                                                       |
| \'silencio\': \'CADUCIDAD del procedimiento (no silencio)\',          |
|                                                                       |
| \'razon\': \'Procedimientos sancionadores: caducidad a los 3 meses    |
| sin resolución\',                                                     |
|                                                                       |
| \'efecto\': \'Archivo de actuaciones. La prescripción puede seguir    |
| corriendo.\',                                                         |
|                                                                       |
| \'articulo\': \'Art. 90 Ley 39/2015\'                                 |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| return SILENCIO_POR_TIPO.get(tipo_procedimiento,                      |
|                                                                       |
| {\'error\': f\'Tipo desconocido: {tipo_procedimiento}.\',             |
|                                                                       |
| \'tipos_validos\': list(SILENCIO_POR_TIPO.keys())})                   |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| \# TIPO AGE-5: CÓMPUTO DE PLAZOS --- la trampa más frecuente          |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| def tipo_computo_plazo(norma_o_acto: str) -\> dict:                   |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| Art. 30 LPAC: días hábiles por defecto para plazos en días.           |
|                                                                       |
| Dias naturales: cuando la norma LO DICE EXPRESAMENTE.                 |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| \# Plazos que son NATURALES (la ley lo dice expresamente)             |
|                                                                       |
| PLAZOS_NATURALES = {                                                  |
|                                                                       |
| \'plazo_maximo_procedimiento\': (\'3 meses naturales como regla       |
| general (o el que fije la norma)\', \'Art. 21 LPAC\'),                |
|                                                                       |
| \'plazo_resoluciones_convocatoria_selectiva\': (\'variable, en        |
| naturales si así lo dice la convocatoria\', \'Art. 55 TREBEP\'),      |
|                                                                       |
| \'plazo_presentacion_instancias\': (\'días naturales --- lo fija la   |
| convocatoria\', \'Convocatoria BOE\'),                                |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# Plazos que son HÁBILES (la regla general)                          |
|                                                                       |
| PLAZOS_HABILES = {                                                    |
|                                                                       |
| \'recurso_alzada\': (\'1 mes (días hábiles)\', \'Art. 121 LPAC\'),    |
|                                                                       |
| \'recurso_reposicion\': (\'1 mes (días hábiles)\', \'Art. 124         |
| LPAC\'),                                                              |
|                                                                       |
| \'contestacion_audiencia\': (\'10 días hábiles\', \'Art. 82 LPAC\'),  |
|                                                                       |
| }                                                                     |
|                                                                       |
| if norma_o_acto in PLAZOS_NATURALES:                                  |
|                                                                       |
| d, a = PLAZOS_NATURALES\[norma_o_acto\]                               |
|                                                                       |
| return {\'tipo\': \'DÍAS NATURALES\', \'descripcion\': d,             |
| \'articulo\': a}                                                      |
|                                                                       |
| if norma_o_acto in PLAZOS_HABILES:                                    |
|                                                                       |
| d, a = PLAZOS_HABILES\[norma_o_acto\]                                 |
|                                                                       |
| return {\'tipo\': \'DÍAS HÁBILES\', \'descripcion\': d, \'articulo\': |
| a}                                                                    |
|                                                                       |
| return {\'regla_general\': \'Si la norma no especifica, los plazos en |
| DÍAS son HÁBILES (art. 30.2 LPAC). Los plazos en MESES o AÑOS se      |
| computan de fecha a fecha (art. 30.4).\',                             |
|                                                                       |
| \'articulo\': \'Art. 30 Ley 39/2015\'}                                |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| \# TIPO AGE-8/9: PRESCRIPCIÓN INFRACCIONES Y SANCIONES                |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| def calcular_prescripcion_disciplinaria(gravedad: str, tipo: str =    |
| \'infraccion\') -\> dict:                                             |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| Infracciones administrativas: Art. 30 Ley 40/2015.                    |
|                                                                       |
| Funcionarios (TREBEP): Arts. 97-98 --- plazos distintos.              |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| PRESCRIPCION_ADMIN = { \# Ley 40/2015 art. 30                         |
|                                                                       |
| \'muy_grave\': (\'3 años\', \'Art. 30 Ley 40/2015\'),                 |
|                                                                       |
| \'grave\': (\'2 años\', \'Art. 30 Ley 40/2015\'),                     |
|                                                                       |
| \'leve\': (\'6 meses\', \'Art. 30 Ley 40/2015\'),                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| PRESCRIPCION_TREBEP = { \# para funcionarios --- Arts. 97-98 TREBEP   |
|                                                                       |
| \'muy_grave\': (\'3 años desde firmeza\', \'Art. 97 TREBEP\'),        |
|                                                                       |
| \'grave\': (\'2 años desde firmeza\', \'Art. 97 TREBEP\'),            |
|                                                                       |
| \'leve\': (\'1 mes desde firmeza\', \'Art. 97 TREBEP\'),              |
|                                                                       |
| }                                                                     |
|                                                                       |
| tabla = PRESCRIPCION_TREBEP if tipo == \'funcionario\' else           |
| PRESCRIPCION_ADMIN                                                    |
|                                                                       |
| result = tabla.get(gravedad.lower())                                  |
|                                                                       |
| if not result:                                                        |
|                                                                       |
| return {\'error\': f\'Gravedad desconocida: {gravedad}\',             |
| \'opciones\': list(tabla.keys())}                                     |
|                                                                       |
| plazo, art = result                                                   |
|                                                                       |
| return {\'gravedad\': gravedad, \'tipo\': tipo,                       |
| \'plazo_prescripcion\': plazo, \'articulo\': art}                     |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| \# DISPATCHER AGE                                                     |
|                                                                       |
| \# ─────────────────────────────────────────────────────────          |
|                                                                       |
| TOOLS_AGE = {                                                         |
|                                                                       |
| \'calcular_plazo_alzada\': calcular_plazo_alzada,                     |
|                                                                       |
| \'calcular_plazo_reposicion\': calcular_plazo_reposicion,             |
|                                                                       |
| \'calcular_silencio_administrativo\':                                 |
| calcular_silencio_administrativo,                                     |
|                                                                       |
| \'tipo_computo_plazo\': tipo_computo_plazo,                           |
|                                                                       |
| \'calcular_prescripcion_disciplinaria\':                              |
| calcular_prescripcion_disciplinaria,                                  |
|                                                                       |
| }                                                                     |
|                                                                       |
| def ejecutar_calculo_age(nombre_tool: str, params: dict) -\> dict:    |
|                                                                       |
| if nombre_tool not in TOOLS_AGE:                                      |
|                                                                       |
| return {\'error\': f\'Herramienta AGE no disponible: {nombre_tool}\', |
|                                                                       |
| \'disponibles\': list(TOOLS_AGE.keys()),                              |
|                                                                       |
| \'nota\': \'Para casos prácticos SS, usar ejecutar_calculo() de       |
| calculadora_ss.py\'}                                                  |
|                                                                       |
| try:                                                                  |
|                                                                       |
| return TOOLS_AGE\[nombre_tool\](\*\*params)                           |
|                                                                       |
| except Exception as e:                                                |
|                                                                       |
| return {\'error\': str(e)}                                            |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **💡 Resumen: dos módulos, dos exámenes**                             |
|                                                                       |
| Tu app necesita DOS módulos de calculadora: calculadora_ss.py para el |
| examen de Seguridad Social (27 tipos de prestaciones), y              |
| calculadora_age.py para el examen de AGE (plazos, recursos,           |
| silencio). El LLM detecta en el system prompt cuál usar según el      |
| examen del usuario. Esto también afecta a cómo generas las preguntas  |
| y qué pipeline usa cada cuerpo.                                       |
+-----------------------------------------------------------------------+

**2. Mistral AI --- Evaluación Completa (Precios Verificados Febrero
2026)**

Mistral es una empresa francesa fundada en 2023. Todos sus servidores
están en Europa (Francia). RGPD nativo sin configurar transferencias
internacionales. Esto es una ventaja real para tu app española.

**2.1 Tabla de Modelos y Precios Verificados**

  ------------------------------------------------------------------------------
  **Modelo**         **Input    **Output   **Contexto**   **Uso óptimo para tu
                     \$/M**     \$/M**                    app**
  ------------------ ---------- ---------- -------------- ----------------------
  Mistral Nemo (12B) \$0.02     \$0.04     128K           Clasificador de
                                                          complejidad,
                                                          normalización de
                                                          queries para caché
                                                          semántico.
                                                          Prácticamente gratis.

  Mistral Small 3.2  \$0.06     \$0.18     128K           Alternativa a Llama 4
  (24B)                                                   Scout para chat
                                                          simple. 60% más barato
                                                          que Scout en output.

  Devstral Small 1.1 \$0.10     \$0.30     128K           Modelo especializado
                                                          en código. Para
                                                          generar scripts Python
                                                          de la calculadora SS
                                                          automáticamente.

  Mistral Medium 3 / \$0.40     \$2.00     128K           Chat complejo de
  3.1                                                     calidad. Precio
                                                          similar a GPT-OSS 120B
                                                          con ventaja EU.

  Codestral 2508     \$0.30     \$0.90     256K           Generación de código.
                                                          Para la etapa offline
                                                          de generar preguntas y
                                                          scripts. Contexto
                                                          256K.

  Mistral Large 3    \$0.50     \$1.50     128K           Revisión de calidad
  (dic 2025)                                              Claude-alternativa.
                                                          Razonamiento profundo.
                                                          Úsalo en pipeline de
                                                          generación, no en
                                                          chat.
  ------------------------------------------------------------------------------

**2.2 El Tier Gratuito de Mistral --- Lo Que Realmente Tienes**

  -----------------------------------------------------------------------
  Mistral tiene un \'experiment tier\' gratuito con acceso rate-limited a
  todos sus modelos. No requiere tarjeta de crédito para empezar. Los
  límites son: \~2 requests/segundo, \~500.000 tokens/mes en total entre
  modelos. Suficiente para desarrollar y hacer pruebas. Para producción
  necesitas añadir tarjeta --- los precios son tan bajos que el gasto es
  mínimo. También hay hasta \$30.000 en créditos para startups (requiere
  solicitud a través de su programa oficial).

  -----------------------------------------------------------------------

**2.3 Document Library de Mistral --- Aclaración (Sí Tiene API)**

El documento que subiste marcaba como desventaja \'sin API
programática\'. Esto ya no es correcto. Mistral Agent Studio tiene API
programática completa:

+-----------------------------------------------------------------------+
| \# Mistral Agents API --- Document Library (verificado                |
| docs.mistral.ai febrero 2026)                                         |
|                                                                       |
| from mistralai import Mistral                                         |
|                                                                       |
| client = Mistral(api_key=\'\...\')                                    |
|                                                                       |
| \# 1. Subir documento a la librería                                   |
|                                                                       |
| with open(\'temario_ss.pdf\', \'rb\') as f:                           |
|                                                                       |
| file_response = client.files.upload(file={\'file_name\':              |
| \'temario_ss.pdf\', \'content\': f})                                  |
|                                                                       |
| file_id = file_response.id                                            |
|                                                                       |
| \# 2. Crear agente con Document Library                               |
|                                                                       |
| agent = client.beta.agents.create(                                    |
|                                                                       |
| model=\'mistral-large-latest\',                                       |
|                                                                       |
| instructions=\'Eres un validador de preguntas de oposición AGE y SS.  |
| Comprueba la exactitud jurídica y el formato usando los documentos de |
| referencia.\',                                                        |
|                                                                       |
| tools=\[{\'type\': \'document_search\'}\],                            |
|                                                                       |
| document_ids=\[file_id\] \# Hasta 100 documentos                      |
|                                                                       |
| )                                                                     |
|                                                                       |
| \# 3. Consultar al agente (con RAG automático sobre los documentos)   |
|                                                                       |
| response = client.beta.agents.complete(                               |
|                                                                       |
| agent_id=agent.id,                                                    |
|                                                                       |
| messages=\[{\'role\': \'user\', \'content\': \'¿Es correcta esta      |
| pregunta sobre IT? \[JSON\]\'}\]                                      |
|                                                                       |
| )                                                                     |
|                                                                       |
| print(response.choices\[0\].message.content)                          |
+-----------------------------------------------------------------------+

**2.4 Cuándo Usar Mistral en Tu Stack**

  -----------------------------------------------------------------------
  **Tarea**              **Modelo Mistral** **vs alternativa actual**
  ---------------------- ------------------ -----------------------------
  Clasificar si pregunta Mistral Nemo       ✅ Más barato que Llama 3.1
  es simple/compleja     (\$0.02/M)         8B de Groq (\$0.05)

  Normalizar queries     Mistral Nemo       ✅ Más barato que Groq Llama
  para caché semántico   (\$0.02/M)         8B

  Generar código Python  Devstral Small     ⚖️ Similar precio/calidad a
  (calculadoras,         (\$0.10/0.30)      GPT-OSS 20B
  scripts)                                  

  Validación legal de    Mistral Large 3 +  ✅ VENTAJA REAL: EU, RGPD
  preguntas generadas    Document Library   nativo, Document Library con
  (agente con temarios                      API
  como documentos)                          

  Chat en tiempo real    Mistral Small 3.2  ⚖️ Similar a Llama 4 Scout
  con opositor           (\$0.06/0.18)      (\$0.11/0.34) --- Mistral más
                                            barato en output

  Generación masiva      Codestral          ⚖️ Similar a DeepSeek V3
  offline de banco de    (\$0.30/0.90) o    (\$0.27/1.10)
  preguntas              Mistral Large 3    
                         (\$0.50/1.50)      

  Chat complejo (casos   Mistral Medium 3   ⚠️ Más caro en output que
  prácticos integrales)  (\$0.40/2.00)      GPT-OSS 120B (\$0.60). Usar
                                            GPT-OSS 120B.
  -----------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **🔑 Mistral: cuándo conviene realmente**                             |
|                                                                       |
| La ventaja real de Mistral es triple: (1) Servidores en Europa ---    |
| RGPD nativo sin configuraciones adicionales, (2) Mistral Nemo a       |
| \$0.02/M --- el modelo más barato del mercado para clasificación, (3) |
| Document Library con API programática --- útil para el pipeline de    |
| validación de preguntas con los temarios como referencia. Para el     |
| chat en tiempo real con el opositor, GPT-OSS 120B en Groq sigue       |
| siendo la mejor opción (calidad, velocidad, precio combinados).       |
| Mistral se integra como segundo proveedor en el pipeline offline de   |
| generación y validación.                                              |
+-----------------------------------------------------------------------+

**3. IDEs con IA para Desarrollar la App --- Comparativa 2026**

Si nunca has desplegado una app con estos servicios, la IA en el IDE es
literalmente tu copiloto técnico. Te explica qué hacer, genera el
código, lo revisa, detecta errores y te guía paso a paso. No necesitas
experiencia previa si usas las herramientas correctamente.

**3.1 Comparativa de IDEs con IA**

  -------------------------------------------------------------------------------------------
  **IDE**       **Precio**       **Modelo IA** **Curva**    **Para tu caso**
  ------------- ---------------- ------------- ------------ ---------------------------------
  Cursor        \$20/mes         GPT-4.1,      Baja ---     ✅ RECOMENDADO. Si ya usas VS
                                 Claude,       similar a VS Code, es el salto más natural.
                                 Gemini        Code         Agent mode genera código, te
                                 (eliges)                   explica errores, despliega con tu
                                                            guía. Elige Claude Sonnet como
                                                            modelo para mejor razonamiento
                                                            legal.

  Windsurf      \$10-15/mes      Cascade       Media        Muy bueno para proyectos
                                 (modelo                    multi-archivo. Cascade observa tu
                                 propio) +                  flujo y sugiere sin que le pidas.
                                 Claude                     Más \'mágico\' que Cursor pero
                                                            menos predecible.

  Kiro (AWS)    Gratis (50       Claude Sonnet Alta ---     Spec-driven: primero escribe los
                tareas/mes)      4 (Anthropic) requiere     requisitos, luego genera el
                                               escribir     código. Excelente para tu caso
                                               specs        por la estructura, pero tiene
                                                            curva de aprendizaje. Útil en
                                                            Fase 2+.

  Claude Code   \$100/mes Pro (o Claude        Baja ---     CLI que entiende tu codebase
                pay-as-you-go)   (Anthropic)   terminal +   completo. Perfecto para generar
                                               VS Code      el calculadora_ss.py completo de
                                               extension    golpe o configurar fly.io. Muy
                                                            potente para tareas de una sola
                                                            sesión.

  Trae          Gratis           DeepSeek V3 / Baja         Alternativa gratuita a Cursor.
  (ByteDance)                    Claude                     Basado en VS Code. Vale para
                                                            empezar sin gastar. OJO: empresa
                                                            china --- no uses con código
                                                            sensible (lógica de pagos,
                                                            claves).

  VS Code +     \$10/mes         GPT-4.1 /     Muy baja --- Si ya tienes VS Code, añadir
  GitHub                         Claude        ya lo        Copilot es el cambio mínimo.
  Copilot                                      conoces      Menor capacidad agente que
                                                            Cursor, pero suficiente para tu
                                                            nivel inicial.

  Antigravity   Gratis           Gemini 2.5    Media        Web-based IDE de Google. Muy
  (Firebase     (Firebase)       Pro                        bueno si vas a usar Firebase como
  Studio)                                                   backend. Si tu stack es Fly.io +
                                                            Postgres + Neo4j, tiene menos
                                                            ventajas específicas.
  -------------------------------------------------------------------------------------------

**3.2 Flujo Práctico: Cómo Usar Cursor para Desplegar Todo**

Este es el flujo real para alguien sin experiencia en despliegue que
quiere construir la app con IA como guía:

+-----------------------------------------------------------------------+
| \# PASO 1 --- Instalar Cursor y configurar el contexto del proyecto   |
|                                                                       |
| \# Descarga: cursor.sh                                                |
|                                                                       |
| \# Al abrir: Settings → Models → seleccionar \'claude-sonnet-4-6\'    |
|                                                                       |
| \# PASO 2 --- Crear el repositorio del proyecto                       |
|                                                                       |
| \# En Cursor, abre la terminal integrada y escribe:                   |
|                                                                       |
| mkdir oposiciones-app && cd oposiciones-app                           |
|                                                                       |
| git init                                                              |
|                                                                       |
| \# Cursor IA: describe tu proyecto en el chat:                        |
|                                                                       |
| \# \'Quiero crear una app web para preparar oposiciones AGE y SS.     |
|                                                                       |
| \# Backend: Python FastAPI. BD: PostgreSQL + Neo4j + Redis.           |
|                                                                       |
| \# Auth: Clerk. Pagos: Stripe. Deploy: Fly.io (backend) + Cloudflare  |
| Pages (frontend).                                                     |
|                                                                       |
| \# Crea la estructura de carpetas y los archivos base.\'              |
|                                                                       |
| \# PASO 3 --- Cursor genera la estructura de tu proyecto:             |
|                                                                       |
| \# /backend                                                           |
|                                                                       |
| \# /app                                                               |
|                                                                       |
| \# main.py ← FastAPI app                                              |
|                                                                       |
| \# /routes ← endpoints                                                |
|                                                                       |
| \# /models ← schemas                                                  |
|                                                                       |
| \# /services ← lógica de negocio                                      |
|                                                                       |
| \# /calculadoras ← calculadora_ss.py + calculadora_age.py             |
|                                                                       |
| \# /frontend                                                          |
|                                                                       |
| \# /src ← React/Vue/Svelte                                            |
|                                                                       |
| \# fly.toml ← configuración de Fly.io                                 |
|                                                                       |
| \# docker-compose.yml ← para desarrollo local                         |
|                                                                       |
| \# PASO 4 --- Configurar servicios uno por uno con IA:                |
|                                                                       |
| \# En el chat de Cursor: \'Configura la conexión a Neo4j Community    |
|                                                                       |
| \# con la URI bolt://mi-vps:7687. Genera el código de conexión,       |
|                                                                       |
| \# el modelo de grafo para las preguntas, y una función de test.\'    |
|                                                                       |
| \# PASO 5 --- Deploy en Fly.io (Cursor guía cada comando):            |
|                                                                       |
| \# Cursor chat: \'Ayúdame a desplegar este backend en Fly.io          |
| Frankfurt.                                                            |
|                                                                       |
| \# Genera el fly.toml, el Dockerfile, y los comandos exactos.\'       |
|                                                                       |
| \# Cursor genera algo así:                                            |
|                                                                       |
| \# fly launch \--name oposiciones-backend \--region fra               |
|                                                                       |
| \# fly secrets set GROQ_API_KEY=gsk\_\... NEO4J_URI=bolt://\...       |
|                                                                       |
| \# fly deploy                                                         |
|                                                                       |
| \# PASO 6 --- Si hay un error (siempre los hay), pega el error en     |
| Cursor:                                                               |
|                                                                       |
| \# \'Tengo este error al hacer fly deploy: \[pegar error aquí\].      |
|                                                                       |
| \# ¿Qué está mal y cómo lo soluciono?\'                               |
|                                                                       |
| \# Cursor diagnostica y te da los cambios exactos                     |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **💡 El secreto para usar la IA en el IDE efectivamente**             |
|                                                                       |
| No le digas \'haz toda la app\'. Dile una cosa concreta a la vez.     |
| \'Configura la conexión a Redis con rate limiting de 10 requests/min  |
| por IP\'. \'Genera el endpoint POST /api/chat que llame a Groq con el |
| sistema de contexto del usuario\'. \'Escribe el webhook de Stripe que |
| actualiza el plan del usuario en PostgreSQL\'. La IA es mejor cuando  |
| las instrucciones son específicas y verificables.                     |
+-----------------------------------------------------------------------+

**4. BMAD Method --- Para Qué Sirve Realmente en Tu Caso**

+-----------------------------------------------------------------------+
| **Conclusión directa antes de explicar**                              |
|                                                                       |
| BMAD no es una feature de tu app. Es una metodología de trabajo TU →  |
| IA para construir la app. Es como Scrum, pero donde el equipo de      |
| desarrollo es tú y múltiples instancias de IA.                        |
+-----------------------------------------------------------------------+

Habiéndolo investigado directamente en el repositorio
(github.com/bmad-code-org/BMAD-METHOD), la descripción que hace Gemini
es correcta en esencia pero exagerada en complejidad. Lo que BMAD
propone es simple:

-   Antes de escribir código, escribe una especificación (PRD,
    architecture doc) --- un Markdown que describe exactamente qué vas a
    construir.

-   Asigna un \'rol\' a la IA para cada tarea. No la misma IA para todo.
    \'Actúa como Arquitecto y revisa este diseño de BD\'. \'Actúa como
    desarrollador backend y escribe el endpoint según esta spec\'.

-   Los docs de especificación son tu memoria. Cuando cierras el IDE y
    abres al día siguiente, la IA no recuerda nada. Pegas el doc de
    arquitectura y continúa donde lo dejó.

-   \'Spec-driven development\' = menos código incorrecto. La IA genera
    mejor código cuando tiene un contrato claro que seguir.

**4.1 BMAD Aplicado a Tu App --- Lo Que Realmente Harías**

  ------------------------------------------------------------------------
  **Fase    **Artefacto**      **Cómo lo aplicas tú en Cursor**
  BMAD**                       
  --------- ------------------ -------------------------------------------
  Fase 0    project_brief.md   Un doc con: qué es la app, quiénes son los
                               usuarios, qué cuerpos cubre, qué hace la
                               calculadora SS, qué hace el chat. Ya lo
                               tienes --- son los Apéndices I-VI.

  Fase 1    prd.md (Product    Lista de todas las funcionalidades en
            Requirements)      historias de usuario. \'Como opositor,
                               quiero hacer un simulacro de 70 preguntas
                               cronometrado.\' Cursor te ayuda a
                               generarlo.

  Fase 2    architecture.md    La arquitectura del Apéndice V: Cloudflare
                               Pages + Fly.io + VPS. Este doc lo pegas en
                               cada nueva sesión de Cursor para que
                               \'sepa\' cómo está organizado el proyecto.

  Fase 3    epics/ (stories)   Divide el proyecto en tickets:
                               \'Implementar endpoint /api/chat\'. \'Crear
                               calculadora_ss.py con 27 funciones\'.
                               \'Configurar Clerk auth\'. Cada ticket es
                               una sesión de Cursor.

  Fase 4    Código             Ejecutas cada ticket en Cursor. La IA
                               genera el código según la spec. Tú revisas
                               y apruebas.
  ------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **💡 La utilidad real de BMAD para alguien sin equipo**               |
|                                                                       |
| El beneficio principal para ti (desarrollador solo sin experiencia en |
| deploy) es el \'context management\': el problema número uno de la IA |
| en IDE es que pierde el contexto al cabo de unos exchanges. BMAD      |
| soluciona esto con los docs de especificación. Al empezar cada        |
| sesión, pegas el architecture.md y la IA sabe exactamente cómo está   |
| la app. Esto solo ya vale el aprendizaje.                             |
+-----------------------------------------------------------------------+

**5. Function Calling y Tools en los Distintos Proveedores --- Cómo
Funciona**

Todos los modelos de producción 2026 soportan function calling (llamar a
funciones Python desde el LLM). Se llama diferente en cada proveedor
pero el concepto es idéntico. Esto es lo que permite que el LLM llame a
tus calculadoras en lugar de inventarse los números.

  --------------------------------------------------------------------------------------
  **Proveedor**   **Cómo se llama**  **Fiabilidad   **Cómo lo usas en tu app**
                                     JSON**         
  --------------- ------------------ -------------- ------------------------------------
  Groq (GPT-OSS   tools /            Alta           Para el chat en tiempo real: el LLM
  120B, Llama 4)  function_calling                  detecta que necesita calcular y
                                                    llama a calculadora_ss.py o
                                                    calculadora_age.py. Respuesta \<1
                                                    segundo.

  Anthropic       tool_use           Muy alta ---   Para el pipeline de revisión
  (Claude)                           mejor del      offline: Claude usa tools para
                                     mercado        verificar artículos en el BOE,
                                                    llamar a calculadoras, generar JSON
                                                    estructurado de preguntas.

  Mistral         function_calling   Alta           Para el pipeline de validación con
                                                    Document Library: el agente Mistral
                                                    usa function calling para buscar en
                                                    los temarios y comparar con la
                                                    pregunta generada.

  DeepSeek V3     tools /            Media-Alta     Para generación offline masiva de
  (API)           function_calling                  preguntas. Contexto largo. Pedir
                                                    JSON estructurado con las 4 opciones
                                                    y el artículo.

  Groq Llama 4    tools              Alta           Alternativa de reserva si GPT-OSS
  Maverick                                          120B no está disponible. Misma
                                                    interfaz de tools.
  --------------------------------------------------------------------------------------

**5.1 Código Unificado --- Cómo Conectar Tools con Groq**

+-----------------------------------------------------------------------+
| \# tools_config.py --- definición de tools para el LLM principal      |
| (Groq)                                                                |
|                                                                       |
| \# El LLM llama a estas tools, tu backend ejecuta las funciones       |
| Python                                                                |
|                                                                       |
| from calculadora_ss import TOOLS as TOOLS_SS, ejecutar_calculo        |
|                                                                       |
| from calculadora_age import TOOLS_AGE, ejecutar_calculo_age           |
|                                                                       |
| \# Definición de tools en formato OpenAI/Groq                         |
|                                                                       |
| TOOLS_GROQ = \[                                                       |
|                                                                       |
| {                                                                     |
|                                                                       |
| \'type\': \'function\',                                               |
|                                                                       |
| \'function\': {                                                       |
|                                                                       |
| \'name\': \'calcular_it\',                                            |
|                                                                       |
| \'description\': \'Calcula base reguladora y cuantía diaria de        |
| Incapacidad Temporal\',                                               |
|                                                                       |
| \'parameters\': {                                                     |
|                                                                       |
| \'type\': \'object\',                                                 |
|                                                                       |
| \'properties\': {                                                     |
|                                                                       |
| \'bases_6_meses\': {\'type\': \'array\', \'items\': {\'type\':        |
| \'number\'}, \'description\': \'Lista de 6 bases mensuales de         |
| cotización\'},                                                        |
|                                                                       |
| \'tipo\': {\'type\': \'string\', \'enum\': \[\'comun\',               |
| \'profesional\'\]},                                                   |
|                                                                       |
| \'dia_numero\': {\'type\': \'integer\', \'description\': \'Número de  |
| día de IT (ej: 25)\'}                                                 |
|                                                                       |
| },                                                                    |
|                                                                       |
| \'required\': \[\'bases_6_meses\'\]                                   |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| },                                                                    |
|                                                                       |
| \# \... (repetir para todos los tipos)                                |
|                                                                       |
| \]                                                                    |
|                                                                       |
| \# Backend: dispatcher que ejecuta la tool que el LLM eligió          |
|                                                                       |
| async def ejecutar_tool_llm(tool_name: str, tool_args: dict,          |
|                                                                       |
| examen: str = \'ss\') -\> dict:                                       |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| El LLM devuelve tool_name + tool_args.                                |
|                                                                       |
| Tu backend ejecuta la función Python real.                            |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| if examen == \'age\':                                                 |
|                                                                       |
| return ejecutar_calculo_age(tool_name, tool_args)                     |
|                                                                       |
| else:                                                                 |
|                                                                       |
| return ejecutar_calculo(tool_name, tool_args)                         |
|                                                                       |
| \# Loop completo de chat con tools (Groq)                             |
|                                                                       |
| async def chat_con_calculadora(user_message: str, user_context: dict) |
| -\> str:                                                              |
|                                                                       |
| response = groq_client.chat.completions.create(                       |
|                                                                       |
| model=\'gpt-4o\', \# GPT-OSS 120B                                     |
|                                                                       |
| messages=\[                                                           |
|                                                                       |
| {\'role\': \'system\', \'content\': SYSTEM_PROMPT_WITH_TOOLS},        |
|                                                                       |
| {\'role\': \'user\', \'content\': user_message}                       |
|                                                                       |
| \],                                                                   |
|                                                                       |
| tools=TOOLS_GROQ,                                                     |
|                                                                       |
| tool_choice=\'auto\'                                                  |
|                                                                       |
| )                                                                     |
|                                                                       |
| msg = response.choices\[0\].message                                   |
|                                                                       |
| \# ¿El LLM quiere llamar a una calculadora?                           |
|                                                                       |
| if msg.tool_calls:                                                    |
|                                                                       |
| results = \[\]                                                        |
|                                                                       |
| for tc in msg.tool_calls:                                             |
|                                                                       |
| import json                                                           |
|                                                                       |
| args = json.loads(tc.function.arguments)                              |
|                                                                       |
| result = await ejecutar_tool_llm(tc.function.name, args)              |
|                                                                       |
| results.append({\'tool_call_id\': tc.id, \'content\':                 |
| json.dumps(result)})                                                  |
|                                                                       |
| \# Segunda llamada: el LLM narra el resultado exacto del cálculo      |
|                                                                       |
| final = groq_client.chat.completions.create(                          |
|                                                                       |
| model=\'gpt-4o\',                                                     |
|                                                                       |
| messages=\[                                                           |
|                                                                       |
| {\'role\': \'system\', \'content\': SYSTEM_PROMPT_WITH_TOOLS},        |
|                                                                       |
| {\'role\': \'user\', \'content\': user_message},                      |
|                                                                       |
| msg,                                                                  |
|                                                                       |
| \*\[{\'role\': \'tool\', \*\*r} for r in results\]                    |
|                                                                       |
| \]                                                                    |
|                                                                       |
| )                                                                     |
|                                                                       |
| return final.choices\[0\].message.content                             |
|                                                                       |
| return msg.content                                                    |
+-----------------------------------------------------------------------+

**5.2 Qué Modelo Usar para Cada Tarea con Agentes/Tools**

  ------------------------------------------------------------------------
  **Tarea**                   **Modelo + Tools   **Justificación**
                              recomendado**      
  --------------------------- ------------------ -------------------------
  Chat en tiempo real +       Groq GPT-OSS       Velocidad \<1s, tools
  calculadoras SS/AGE         120B + tools       fiables,
                                                 \$0.28/usuario/mes

  Generar banco de preguntas  DeepSeek V3 API +  Contexto 64K, barato,
  (offline, lento)            structured output  calidad alta para
                                                 generación

  Revisar y validar preguntas Claude Sonnet +    tool_use más fiable del
  generadas                   tool_use           mercado, razonamiento
                                                 profundo

  Validar contra temarios de  Mistral Large 3 +  EU servers, Document
  referencia                  Document Library   Library con API, búsqueda
                                                 semántica sobre PDFs

  Clasificar complejidad de   Mistral Nemo (sin  \$0.02/M, clasificación
  preguntas                   tools)             binaria no necesita tools

  Generar código              Claude Code o      Contexto de codebase
  (calculadoras, scripts)     Cursor+Claude      completo, revisión
                                                 automática

  Razonamiento en cadena      GPT-OSS 120B o     Necesita multi-step +
  (casos prácticos            Qwen3 32B con      tools para calcular bien
  integrales)                 tools              
  ------------------------------------------------------------------------

**6. Revisión del Plan V2 --- Cambios Necesarios**

Con todo lo aprendido en los Apéndices IV, V y VI, estos son los cambios
que afectan al Plan V2 original:

  ------------------------------------------------------------------------
  **Elemento del     **Estado**      **Acción recomendada**
  Plan V2**                          
  ------------------ --------------- -------------------------------------
  Salamandra como    ❌ ELIMINADO    Verificado por tus pruebas reales:
  modelo principal                   Fly.io CPU demasiado lento, 7B
  de chat                            cuantizado no fiable para
                                     razonamiento. Usar GPT-OSS 120B en
                                     Groq.

  Sistema de agentes ❌ ELIMINADO    Tools/function calling no funcionó
  con Salamandra                     con 7B cuantizado. El sistema de
                                     agentes funciona bien con GPT-OSS
                                     120B + tools.

  Calculadoras SS: 9 ✅ ACTUALIZADO  Apéndice V tiene los 27 tipos.
  tipos              a 27 tipos      Apéndice VI añade los 15 tipos
                                     procedimentales AGE.

  Solo calculadoras  ✅ COMPLETADO   Los casos prácticos AGE son de
  para SS            con AGE         procedimiento, no de prestaciones.
                                     Apéndice VI tiene calculadora_age.py.

  Proveedores de IA: ✅ AÑADIR       Mistral Nemo como clasificador más
  solo Groq +        Mistral         barato (\$0.02/M) + Mistral Large 3 +
  Claude + DeepSeek                  Document Library para validación con
                                     temarios.

  IDE de desarrollo: ✅ AÑADIDO      Cursor como principal (Claude Sonnet
  no mencionado                      como modelo). Metodología BMAD para
                                     gestión del contexto entre sesiones.

  Stack              ✅ COMPLETADO   Cloudflare Pages (frontend) + Fly.io
  fronend/backend:                   Frankfurt (backend) + VPS Hostinger
  solo Fly.io                        (Neo4j + PG + Redis).
  mencionado                         

  Auth y pagos: no   ✅ COMPLETADO   Clerk.com (auth, gratis hasta 10K) +
  especificados                      Stripe (pagos 1.4%+0.25€/EU).

  RGPD y seguridad   ✅ COMPLETADO   Apéndice V sección 4: documentos
                                     legales obligatorios, tratamiento de
                                     datos, transferencias
                                     internacionales, checklist técnico.

  Pedagogía Valera:  ✅ COMPLETADA   Apéndice IV: Socratic scaffolding,
  mencionada         técnicamente    caso inverso, mapa de errores
                                     colectivos, detección de fatiga.

  B2B con            ⚠️ PENDIENTE de La estrategia está en Apéndice IV.
  preparadores:      acciones        Queda pendiente el ejecutarlo:
  mencionado                         contactar 5 preparadores, beta
                                     cerrada, kit white-label.

  Neo4j modelo de    ✅ REDISEÑADO   Opciones como JSON en nodo Pregunta →
  grafo: 270K nodos                  70K nodos (cabe en AuraDB Free y
                                     Community).

  Gamificación:      ✅ DETALLADA    Apéndice IV suplemento: streak +
  mencionada                         freeze + ligas segmentadas + XP. Sin
                                     corazones/vidas.

  Lanzamiento: Mayo  ⚠️ REVISAR      Beta cerrada antes de Mayo (30
  2026 como objetivo                 usuarios). Lanzamiento real en
                                     convocatoria 2027. Primero solo
                                     Auxiliar AGE (28 temas).
  ------------------------------------------------------------------------

**6.1 Priorización Actualizada --- Qué Hacer Primero**

  -----------------------------------------------------------------------------
  **Sem**   **Tarea**                **Descripción y herramientas**
  --------- ------------------------ ------------------------------------------
  1         Configurar entorno de    Instalar Cursor + elegir Claude Sonnet.
            desarrollo               Crear repositorio GitHub. Crear estructura
                                     BMAD: project_brief.md + architecture.md
                                     con el contenido de los Apéndices.

  2         VPS: Neo4j +             En Cursor: \'Ayúdame a instalar Neo4j
            PostgreSQL + Redis       Community en Ubuntu 24, configurar PG y
                                     Redis, y crear el esquema de preguntas con
                                     opciones como JSON.\' Seguir paso a paso.

  3         Calculadoras + tests     Implementar calculadora_ss.py (27 tipos) y
                                     calculadora_age.py (15 tipos) en el
                                     repositorio. Crear 50 tests unitarios con
                                     casos reales del examen.

  4         Backend FastAPI en       Endpoint /api/chat con GPT-OSS 120B +
            Fly.io                   tools, rate limiting Redis, verificación
                                     Clerk JWT. Deploy en Frankfurt.

  5         Frontend en Cloudflare   React/Vue básico: login con Clerk,
            Pages                    pantalla de chat, barra de progreso. Sin
                                     gamificación todavía.

  6         Pipeline generación      DeepSeek V3 genera 500 preguntas Auxiliar
            offline                  AGE → Claude las revisa → se cargan en
                                     Neo4j. Verificar calidad manualmente en 50
                                     de ellas.

  7-8       Beta cerrada --- 20      Reclutar 20-30 opositores reales. 0€. A
            opositores               cambio de feedback semanal y testimonios.
                                     Detectar bugs y mejoras antes de lanzar.

  9-10      Stripe + plan PRO +      Configurar productos en Stripe (9€/mes
            Clerk roles              PRO). Webhook que actualiza rol de usuario
                                     en Clerk. Plan free con límites reales.

  11-12     Contactar 5 preparadores Email frío + demo de 30 minutos. Ofrecer
                                     acceso gratuito 3 meses a cambio de
                                     feedback y testimonios públicos.
  -----------------------------------------------------------------------------

*Apéndice VI · Fuentes: docs.mistral.ai (verificado 27/02/2026) ·
kearai.com/kiro-review (enero 2026) · morphllm.com/kiro-vs-cursor
(febrero 2026) · pricepertoken.com/mistral (25/02/2026)*

*Casos prácticos AGE: plazos y procedimiento (Ley 39/2015). Casos
prácticos SS: prestaciones TRLGSS. Dos exámenes distintos, dos módulos
de calculadoras.*
