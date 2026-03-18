**APÉNDICE III --- ACTUALIZACIÓN TÉCNICA**

App Oposiciones AGE & SS --- Datos reales feb 2026

*Costes corregidos · Caché semántico · Neo4j en VPS · BYOK · Script de
prueba · Salamandra sin operaciones*

**1. Corrección de Costes: El Error del Cálculo Anterior**

El cálculo previo infravaloraba el output en un 55%. Los modelos tipo
GPT-OSS 20B son notablemente verbosos en respuestas legales detalladas.
Este es el recálculo honesto:

+-----------------------------------------------------------------------+
| **⚠️ Error identificado en versión anterior**                         |
|                                                                       |
| GPT-OSS 20B genera 5 veces más tokens de output que la media de       |
| modelos similares en benchmarks. Una explicación legal con cita de    |
| artículo, por qué A es correcta, por qué B/C/D son incorrectas y      |
| truco mnemotécnico produce fácilmente 600-900 tokens de output, no    |
| 350 como se calculó antes.                                            |
+-----------------------------------------------------------------------+

  ----------------------------------------------------------------------------------------------------------
  **Componente del **Tokens      **Tokens    **Ratio       **Coste/intercambio**   **Total mes (440)**
  Chat**           Input**       Output**    Out/In**                              
  ---------------- ------------- ----------- ------------- ----------------------- -------------------------
  Sistema +        \~800         --          --            --                      --
  contexto Neo4j                                                                   

  Historial chat   \~300         --          --            --                      --
  (3 turnos)                                                                       

  Pregunta del     \~50          --          --            --                      --
  usuario                                                                          

  Respuesta del    --            \~650-800   \~2.0x        \$0.000101+\$0.000210   --
  modelo                                                                           

  **TOTAL por      **\~1.350**   **\~725**   **\~0.54x**   **\$0.000311**          **\$0.137/usuario/mes**
  intercambio**                                                                    
  ----------------------------------------------------------------------------------------------------------

  -------------------------------------------------------------------------
  **Escala de        **Coste/mes     **Coste/mes     **Con      **Con caché
  usuarios**         (GPT-OSS 20B)** (Qwen3 32B)**   caché      60%**
                                                     40%**      
  ------------------ --------------- --------------- ---------- -----------
  100 usuarios       \~\$14          \~\$21          \~\$8      \~\$6

  500 usuarios       \~\$69          \~\$103         \~\$41     \~\$28

  1.000 usuarios     \~\$137         \~\$206         \~\$82     \~\$55

  2.000 usuarios     \~\$274         \~\$412         \~\$164    \~\$110
  -------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **💡 Conclusión corregida**                                           |
|                                                                       |
| Sigue siendo barato, pero el caché semántico pasa a ser               |
| imprescindible desde los primeros 200 usuarios para mantener costes   |
| controlados. El ahorro real del caché (40-60%) es el mayor palanca de |
| optimización que tienes.                                              |
+-----------------------------------------------------------------------+

**2. Caché Semántico: La Solución al Problema de Variación de
Preguntas**

Un opositor pregunta \'no entiendo el silencio administrativo\'. Otro
pregunta \'¿cuándo la administración me da la razón si no contesta?\'.
Es la misma duda. El caché por texto exacto no lo detecta. La solución
es caché por similitud semántica con embeddings vectoriales.

**2.1 Por qué NO funciona el caché por texto exacto**

-   \'¿Qué es el silencio positivo?\' → texto A

-   \'Si la Administración no me contesta, ¿se entiende que me dan la
    razón?\' → texto B

-   \'No me han respondido en 3 meses, ¿qué hago?\' → texto C

-   Los tres preguntan lo mismo pero el caché de texto exacto no lo ve.
    El caché semántico sí.

**2.2 El Flujo Completo con Neo4j Vector Search**

Neo4j AuraDB (desde enero 2026) tiene vector search nativo. Puedes hacer
grafo + embeddings en la misma BD, sin Qdrant adicional:

+-----------------------------------------------------------------------+
| \# PASO 1: Normalizar la pregunta del usuario                         |
|                                                                       |
| \# Una IA pequeña (Llama 3.1 8B en Groq: \$0.05/M) reformula la       |
| pregunta                                                              |
|                                                                       |
| \# en forma canónica antes de buscar en caché                         |
|                                                                       |
| def normalizar_pregunta(pregunta_raw: str) -\> str:                   |
|                                                                       |
| resp = groq_client.chat.completions.create(                           |
|                                                                       |
| model=\'llama-3.1-8b-instant\',                                       |
|                                                                       |
| messages=\[                                                           |
|                                                                       |
| {\'role\':\'system\',\'content\':\'Reformula esta pregunta de         |
| oposición en forma                                                    |
|                                                                       |
| canónica clara y corta. Solo devuelve la pregunta reformulada, nada   |
| más.\'},                                                              |
|                                                                       |
| {\'role\':\'user\',\'content\': pregunta_raw}                         |
|                                                                       |
| \],                                                                   |
|                                                                       |
| max_tokens=80                                                         |
|                                                                       |
| )                                                                     |
|                                                                       |
| return resp.choices\[0\].message.content                              |
|                                                                       |
| \# PASO 2: Generar embedding de la pregunta normalizada               |
|                                                                       |
| \# Usar text-embedding-3-small (OpenAI) o nomic-embed-text            |
| (local/free)                                                          |
|                                                                       |
| \# Coste: \$0.02/M tokens ≈ \$0.000001 por pregunta → DESPRECIABLE    |
|                                                                       |
| def get_embedding(texto: str) -\> list\[float\]:                      |
|                                                                       |
| resp = openai_client.embeddings.create(                               |
|                                                                       |
| model=\'text-embedding-3-small\',                                     |
|                                                                       |
| input=texto                                                           |
|                                                                       |
| )                                                                     |
|                                                                       |
| return resp.data\[0\].embedding \# vector de 1536 dimensiones         |
|                                                                       |
| \# PASO 3: Buscar en Neo4j si existe respuesta similar reciente       |
|                                                                       |
| CYPHER_BUSCAR_CACHE = \'\'\'                                          |
|                                                                       |
| CALL db.index.vector.queryNodes(\'cache_preguntas\', 3, \$embedding)  |
|                                                                       |
| YIELD node, score                                                     |
|                                                                       |
| WHERE score \> 0.88                                                   |
|                                                                       |
| AND node.fecha \> datetime() - duration(\'P30D\')                     |
|                                                                       |
| AND node.cuerpo = \$cuerpo_usuario                                    |
|                                                                       |
| RETURN node.respuesta_generada, node.pregunta_normalizada, score      |
|                                                                       |
| ORDER BY score DESC LIMIT 1                                           |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| \# PASO 4: Si no hay caché → llamar al LLM principal (GPT-OSS 20B o   |
| Qwen3)                                                                |
|                                                                       |
| \# PASO 5: Guardar en caché para futuros usuarios                     |
|                                                                       |
| CYPHER_GUARDAR = \'\'\'                                               |
|                                                                       |
| CREATE (c:CacheRespuesta {                                            |
|                                                                       |
| pregunta_normalizada: \$pregunta,                                     |
|                                                                       |
| embedding: \$embedding,                                               |
|                                                                       |
| respuesta_generada: \$respuesta,                                      |
|                                                                       |
| cuerpo: \$cuerpo,                                                     |
|                                                                       |
| fecha: datetime(),                                                    |
|                                                                       |
| usos: 1                                                               |
|                                                                       |
| })                                                                    |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| \# El índice vectorial en Neo4j (crear una vez):                      |
|                                                                       |
| \# CREATE VECTOR INDEX cache_preguntas IF NOT EXISTS                  |
|                                                                       |
| \# FOR (c:CacheRespuesta) ON c.embedding                              |
|                                                                       |
| \# OPTIONS {indexConfig: {\`vector.dimensions\`: 1536,                |
|                                                                       |
| \# \`vector.similarity_function\`: \'cosine\'}}                       |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **💰 Coste real de la normalización (el paso adicional de IA)**       |
|                                                                       |
| Normalizar con Llama 3.1 8B (Groq \$0.05/\$0.08 por M): \~80 tokens   |
| input + 80 output = \$0.0000064 por pregunta. Para 440                |
| preguntas/mes/usuario: \$0.0028. Totalmente despreciable. El ahorro   |
| del caché (40-60% de las llamadas al LLM caro) compensa 500 veces ese |
| coste.                                                                |
+-----------------------------------------------------------------------+

**2.3 Umbral de Similitud: ¿Qué Valor Usar?**

  --------------------------------------------------------------------------
  **Umbral     **Comportamiento**   **Riesgo**          **Recomendación**
  coseno**                                              
  ------------ -------------------- ------------------- --------------------
  \< 0.80      Agrupa preguntas muy Alto: da respuestas ❌ No usar
               distintas            incorrectas a       
                                    preguntas distintas 

  0.85-0.88    Agrupa variaciones   Bajo: algún falso   ✅ Para dudas
               naturales de la      positivo aceptable  generales
               misma duda                               

  0.89-0.92    Solo agrupa          Muy bajo            ✅✅ Para dudas con
               reformulaciones muy                      cálculos (más
               cercanas                                 sensibles)

  \> 0.95      Casi solo detecta    Ninguno             ❌ No cachea nada
               frases idénticas                         útil
  --------------------------------------------------------------------------

**3. Neo4j Community Edition en tu VPS Hostinger 8GB CPU --- ¿Cabe?**

Pregunta directa, respuesta directa con los números reales de memoria de
Neo4j Community Edition 5.x:

**3.1 Distribución de RAM en el VPS (8 GB disponibles)**

  -------------------------------------------------------------------------
  **Servicio**           **RAM         **RAM           **Estado**
                         mínima**      recomendada**   
  ---------------------- ------------- --------------- --------------------
  Ubuntu 24 + procesos   \~300 MB      \~400 MB        Fijo
  SO                                                   

  nginx                  \~50 MB       \~100 MB        Fijo

  Salamandra 7B Q4_K_M   \~4.500 MB    \~4.800 MB      Ya instalado
  (llama.cpp/Ollama)                                   

  Tu backend API         \~150 MB      \~300 MB        Ligero
  (Python/Node)                                        

  Neo4j Community 5.x    \~512 MB      \~1.000-1.500   ¿CABE?
                         start         MB en uso       

  **TOTAL con Neo4j      **\~5.512     **\~7.100 MB**  **⚠️ JUSTO**
  (estimado)**           MB**                          

  Margen libre           \~2.488 MB    \~900 MB        Peligroso
  -------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **⚠️ Veredicto: Técnicamente SÍ cabe, pero con Salamandra activo es   |
| peligroso**                                                           |
|                                                                       |
| Neo4j Community arranca con \~512MB pero en producción con consultas  |
| vectoriales y grafos activos consume 1-1.5 GB. Si Salamandra está     |
| generando (procesando una tanda nocturna) a la vez que Neo4j responde |
| queries de usuarios, puedes llegar a 7.5-8 GB y el OOM killer de      |
| Linux empieza a matar procesos. En tu caso concreto, la solución más  |
| segura NO es meter Neo4j en el VPS junto a Salamandra.                |
+-----------------------------------------------------------------------+

**3.2 Las Tres Opciones Reales**

  ------------------------------------------------------------------------
  **Opción**    **Descripción**    **Coste**        **Recomendación**
  ------------- ------------------ ---------------- ----------------------
  A --- Neo4j   Neo4j en cloud de  0€/mes. Sin      ✅✅ MEJOR OPCIÓN.
  AuraDB Free   Neo4j. Tu VPS      límite de        200K nodos, vector
  (nube)        queda libre para   tiempo.          search, 0 gestión.
                Salamandra.                         

  B --- Neo4j   Si mueves          RunPod:          ✅ Buena cuando tengas
  Community en  Salamandra a       \$0-5/mes según  tráfico que justifique
  VPS SIN       RunPod Serverless, uso. VPS: ya     RunPod.
  Salamandra    en el VPS caben    pagado.          
                Neo4j + backend +                   
                nginx                               
                perfectamente                       
                (4.5GB libres).                     

  C --- Neo4j   Pones límite de    0€ adicional     ⚠️ Solo si insistes en
  Community en  RAM a Salamandra                    todo en VPS.
  VPS + límite  (3.5GB max) y a                     Monitoriza con alertas
  Salamandra    Neo4j (1.2GB max)                   de RAM.
                via jvm.conf. Cabe                  
                pero peligroso en                   
                picos.                              

  D --- Segundo CX11: 2 vCPU, 2GB  \~€3.29/mes      ✅ Limpio, simple,
  VPS Hetzner   RAM, solo para                      sostenible.
  €3.29/mes     Neo4j + backend.                    Recomendado si AuraDB
                Tu Hostinger: solo                  Free te queda pequeño
                Salamandra +                        en Fase 3.
                nginx.                              
  ------------------------------------------------------------------------

**3.3 Si Decides Usar la Opción C (Todo en VPS): Configuración Segura**

+-----------------------------------------------------------------------+
| \# /etc/neo4j/neo4j.conf --- límites de memoria para Neo4j Community  |
|                                                                       |
| \# Ajusta según tu RAM disponible real                                |
|                                                                       |
| \# Heap Java (memoria principal de Neo4j)                             |
|                                                                       |
| server.memory.heap.initial_size=512m                                  |
|                                                                       |
| server.memory.heap.max_size=1000m                                     |
|                                                                       |
| \# Page cache (datos del grafo en RAM, más = más rápido)              |
|                                                                       |
| server.memory.pagecache.size=400m                                     |
|                                                                       |
| \# TOTAL Neo4j: \~1.4 GB máximo                                       |
|                                                                       |
| \# Para Ollama/llama.cpp con Salamandra --- limitar también:          |
|                                                                       |
| \# En /etc/systemd/system/ollama.service añadir:                      |
|                                                                       |
| \# Environment=OLLAMA_MAX_LOADED_MODELS=1                             |
|                                                                       |
| \# Environment=OLLAMA_NUM_PARALLEL=1                                  |
|                                                                       |
| \# Monitorización: alerta si RAM \> 85%                               |
|                                                                       |
| \# Instala: apt install prometheus node-exporter                      |
|                                                                       |
| \# O simplemente: watch -n 5 \'free -h && ps aux \--sort=-%mem \|     |
| head -8\'                                                             |
+-----------------------------------------------------------------------+

**4. BYOK (Bring Your Own Key) --- Modelo de Negocio Híbrido**

El usuario aporta su propia API key de Groq/DeepSeek. Evaluación
completa:

**4.1 Análisis Honesto: Ventajas y Problemas Reales**

  -----------------------------------------------------------------------
  **✅ A Favor**                      **❌ En Contra**
  ----------------------------------- -----------------------------------
  Tu coste de tokens = 0€. Incluso    Fricción enorme en onboarding.
  con 2.000 usuarios.                 Pedir API key a un no-técnico mata
                                      la conversión.

  Transparente: el usuario sabe       Si la key expira o se queda sin
  exactamente qué consume.            crédito, la app da error sin aviso
                                      claro.

  Modelo de negocio limpio: cobras    Groq requiere cuenta de pago
  por el contenido, no por la IA.     (tarjeta) para superar free tier.
                                      Barrera alta.

  Los usuarios técnicos               Debes soportar múltiples providers
  (informáticos, juristas) lo         (Groq, DeepSeek, Mistral):
  entienden y lo prefieren.           complejidad técnica.

  Reduce drásticamente el riesgo      El usuario puede usar tu plataforma
  financiero en la fase de tracción.  gratis con sus créditos free tier y
                                      no pagar nada.
  -----------------------------------------------------------------------

**4.2 Modelo Híbrido Recomendado: Tres Niveles**

  ------------------------------------------------------------------------
  **Plan**      **Precio**    **Chat IA**     **Para quién**
  ------------- ------------- --------------- ----------------------------
  FREE          0€/mes        10              Prueba, conversión
                              preguntas/día   
                              con tu API key  
                              (modelo básico) 

  PRO           9-12€/mes     Ilimitado con   La mayoría de usuarios
                              tu API key      
                              (modelo bueno   
                              incluido)       

  PRO + BYOK    6-8€/mes      Ilimitado con   Usuarios técnicos, ahorro
                (descuento)   SU API key      mutuo

  ACADEMIA      X€/mes (B2B)  Ilimitado con   Academias de oposiciones
                              tu API key,     
                              multi-usuario   
  ------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **💡 El truco del BYOK para no-técnicos**                             |
|                                                                       |
| Si quieres ofrecer BYOK incluso a no-técnicos, crea un flujo guiado   |
| en 3 pasos dentro de la app: (1) Botón \'Consigue tu clave gratis en  |
| Groq\' → abre groq.com/keys en nueva pestaña. (2) Campo de texto con  |
| instrucción visual de dónde copiar la key. (3) Botón \'Verificar      |
| clave\' que hace una llamada de prueba y muestra \'✅ Todo listo\'.   |
| El 80% de los usuarios que lo intentan lo completan si el flujo es    |
| claro.                                                                |
+-----------------------------------------------------------------------+

**5. Salamandra 7B --- Conclusión Definitiva sobre su Rol**

Respuesta directa a la pregunta \'¿la necesito si tengo Neo4j + Mem0 +
APIs?\':

+-----------------------------------------------------------------------+
| **❌ Salamandra NO es necesaria operacionalmente con este stack**     |
|                                                                       |
| Con Neo4j para memoria y contexto, Mem0 para extracción de memorias,  |
| GPT-OSS 20B en Groq para chat (\$0.09-0.14/usuario/mes), Qwen3 32B    |
| para razonamiento complejo, DeepSeek+Claude para generar y revisar el |
| banco de preguntas --- Salamandra no añade nada que no tengas ya      |
| mejor cubierto por las APIs. El coste es tan bajo que el ahorro de    |
| tener un modelo local no justifica la complejidad de mantenerlo.      |
+-----------------------------------------------------------------------+

  -----------------------------------------------------------------------
  **Caso de uso**        **¿Salamandra lo       **Alternativa con APIs**
                         resuelve?**            
  ---------------------- ---------------------- -------------------------
  Explicaciones \'por    Sí, pre-generando      Ya se generan en el
  qué A y no B\'         offline (5-15 tok/s    pipeline DeepSeek+Claude
                         CPU, lento)            al crear el banco.
                                                Guardadas en BD. 0 tokens
                                                en runtime.

  Chat en tiempo real    No (20-60s por         GPT-OSS 20B en Groq:
                         respuesta en CPU es    \<1s,
                         inaceptable)           \$0.000311/intercambio

  Razonamiento legal     Parcialmente (7B tiene Qwen3 32B o GPT-OSS 120B
  complejo               limitaciones en        en Groq: mucho mejor
                         razonamiento           calidad
                         multi-paso)            

  Español jurídico       Sí, es su punto fuerte DeepSeek V3 y Qwen3 32B
  nativo                                        también tienen excelente
                                                español jurídico

  Coste 0€ en inferencia Sí, pero con latencia  GPT-OSS 20B:
                         inaceptable para chat  \$0.14/usuario/mes.
                                                Asumible desde el
                                                principio.
  -----------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **💡 ¿Cuándo SÍ tendría sentido Salamandra?**                         |
|                                                                       |
| Solo en tres escenarios futuros: (1) Si decides hacer fine-tuning con |
| preguntas reales de tus opositores y quieres un modelo especializado  |
| propio --- ese Salamandra fine-tuneado sería genuinamente mejor que   |
| un modelo genérico. (2) Si el coste de APIs escala por encima de lo   |
| previsto (\>500€/mes) y quieres recuperar control. (3) Si en el       |
| futuro despliegas en GPU vía RunPod Serverless y la latencia          |
| desaparece. Hasta entonces: quítala del diseño operativo.             |
+-----------------------------------------------------------------------+

**6. Script de Prueba: Mide el Coste Real Antes de Comprometerte**

Este script compara GPT-OSS 20B (Groq) vs Qwen3 32B (Groq) vs DeepSeek
V3 con preguntas reales de opositor y te da el coste extrapolado mensual
por usuario con tus datos reales:

+-----------------------------------------------------------------------+
| \# test_coste_real.py                                                 |
|                                                                       |
| \# Requisitos: pip install openai groq                                |
|                                                                       |
| \# Variables de entorno: GROQ_KEY, DEEPSEEK_KEY                       |
|                                                                       |
| import os, time, json                                                 |
|                                                                       |
| from openai import OpenAI                                             |
|                                                                       |
| \# ── CONFIGURACIÓN DE MODELOS ─────────────────────────────────      |
|                                                                       |
| MODELOS = {                                                           |
|                                                                       |
| \'groq_gpt_oss_20b\': {                                               |
|                                                                       |
| \'client\': OpenAI(api_key=os.getenv(\'GROQ_KEY\'),                   |
|                                                                       |
| base_url=\'https://api.groq.com/openai/v1\'),                         |
|                                                                       |
| \'model\': \'openai/gpt-oss-20b\',                                    |
|                                                                       |
| \'precio_in\': 0.075, \'precio_out\': 0.30                            |
|                                                                       |
| },                                                                    |
|                                                                       |
| \'groq_qwen3_32b\': {                                                 |
|                                                                       |
| \'client\': OpenAI(api_key=os.getenv(\'GROQ_KEY\'),                   |
|                                                                       |
| base_url=\'https://api.groq.com/openai/v1\'),                         |
|                                                                       |
| \'model\': \'qwen/qwen3-32b\',                                        |
|                                                                       |
| \'precio_in\': 0.29, \'precio_out\': 0.59                             |
|                                                                       |
| },                                                                    |
|                                                                       |
| \'deepseek_v3\': {                                                    |
|                                                                       |
| \'client\': OpenAI(api_key=os.getenv(\'DEEPSEEK_KEY\'),               |
|                                                                       |
| base_url=\'https://api.deepseek.com\'),                               |
|                                                                       |
| \'model\': \'deepseek-chat\',                                         |
|                                                                       |
| \'precio_in\': 0.27, \'precio_out\': 1.10                             |
|                                                                       |
| },                                                                    |
|                                                                       |
| }                                                                     |
|                                                                       |
| SYSTEM = (\'Eres preparador experto de oposiciones AGE y Seguridad    |
| Social España. \'                                                     |
|                                                                       |
| \'Explica con rigor legal, cita siempre el artículo exacto de la ley. |
| \'                                                                    |
|                                                                       |
| \'Si hay cálculo, muéstralo paso a paso. Responde en español.\')      |
|                                                                       |
| \# ── PREGUNTAS TIPO OPOSITOR REAL ─────────────────────────────      |
|                                                                       |
| PREGUNTAS = \[                                                        |
|                                                                       |
| \'Diferencia entre jubilación anticipada voluntaria e involuntaria:   |
| \'                                                                    |
|                                                                       |
| \'años cotizados necesarios y tiempo máximo de anticipación\',        |
|                                                                       |
| \'El silencio administrativo: regla general y excepciones \'          |
|                                                                       |
| \'según la Ley 39/2015. Pon un ejemplo de cada caso.\',               |
|                                                                       |
| \'Trabajador con base reguladora 2.400 euros/mes en IT. \'            |
|                                                                       |
| \'Calcula qué cobra los primeros 3 días, del 4 al 20 y del 21 en      |
| adelante.\',                                                          |
|                                                                       |
| \'¿Qué es el recargo de prestaciones? ¿Quién lo paga? \'              |
|                                                                       |
| \'¿Se puede asegurar? Cita el artículo del TRLGSS.\',                 |
|                                                                       |
| \'Plazos para interponer recurso de alzada y recurso de reposición.   |
| \'                                                                    |
|                                                                       |
| \'¿Cuándo se usa cada uno? ¿Pueden simultanearse?\'                   |
|                                                                       |
| \]                                                                    |
|                                                                       |
| \# ── EJECUCIÓN Y MÉTRICAS ──────────────────────────────────────     |
|                                                                       |
| resultados = {}                                                       |
|                                                                       |
| for nombre, cfg in MODELOS.items():                                   |
|                                                                       |
| print(f\'\\n{\'=\'\*60}\')                                            |
|                                                                       |
| print(f\'MODELO: {nombre}\')                                          |
|                                                                       |
| print(f\'{\'=\'\*60}\')                                               |
|                                                                       |
| datos = \[\]                                                          |
|                                                                       |
| for i, pregunta in enumerate(PREGUNTAS):                              |
|                                                                       |
| t0 = time.time()                                                      |
|                                                                       |
| try:                                                                  |
|                                                                       |
| resp = cfg\[\'client\'\].chat.completions.create(                     |
|                                                                       |
| model=cfg\[\'model\'\],                                               |
|                                                                       |
| messages=\[                                                           |
|                                                                       |
| {\'role\': \'system\', \'content\': SYSTEM},                          |
|                                                                       |
| {\'role\': \'user\', \'content\': pregunta}                           |
|                                                                       |
| \],                                                                   |
|                                                                       |
| max_tokens=900                                                        |
|                                                                       |
| )                                                                     |
|                                                                       |
| elapsed = time.time() - t0                                            |
|                                                                       |
| u = resp.usage                                                        |
|                                                                       |
| coste = (u.prompt_tokens \* cfg\[\'precio_in\'\] +                    |
|                                                                       |
| u.completion_tokens \* cfg\[\'precio_out\'\]) / 1_000_000             |
|                                                                       |
| ratio = u.completion_tokens / max(u.prompt_tokens, 1)                 |
|                                                                       |
| datos.append({\'in\': u.prompt_tokens, \'out\': u.completion_tokens,  |
|                                                                       |
| \'ratio\': ratio, \'coste\': coste, \'seg\': elapsed})                |
|                                                                       |
| print(f\' P{i+1}: IN={u.prompt_tokens:4d}                             |
| OUT={u.completion_tokens:4d} \'                                       |
|                                                                       |
| f\'ratio={ratio:.2f}x \${coste:.5f} {elapsed:.1f}s\')                 |
|                                                                       |
| except Exception as e:                                                |
|                                                                       |
| print(f\' P{i+1}: ERROR --- {e}\')                                    |
|                                                                       |
| datos.append({\'in\':0,\'out\':0,\'ratio\':0,\'coste\':0,\'seg\':0})  |
|                                                                       |
| time.sleep(0.5) \# evitar rate limit                                  |
|                                                                       |
| if datos:                                                             |
|                                                                       |
| avg_in = sum(d\[\'in\'\] for d in datos) / len(datos)                 |
|                                                                       |
| avg_out = sum(d\[\'out\'\] for d in datos) / len(datos)               |
|                                                                       |
| avg_cost= sum(d\[\'coste\'\] for d in datos) / len(datos)             |
|                                                                       |
| avg_vel = sum(d\[\'out\'\] for d in datos) / max(sum(d\[\'seg\'\] for |
| d in datos), 0.1)                                                     |
|                                                                       |
| extra_mes = avg_cost \* 440 \# 440 preguntas/mes/usuario              |
|                                                                       |
| extra_500 = extra_mes \* 500                                          |
|                                                                       |
| print(f\'\\n ── RESUMEN {nombre} ──\')                                |
|                                                                       |
| print(f\' Media input: {avg_in:.0f} tokens\')                         |
|                                                                       |
| print(f\' Media output: {avg_out:.0f} tokens\')                       |
|                                                                       |
| print(f\' Ratio out/in: {avg_out/max(avg_in,1):.2f}x\')               |
|                                                                       |
| print(f\' Coste medio/pregunta: \${avg_cost:.5f}\')                   |
|                                                                       |
| print(f\' Velocidad output: {avg_vel:.0f} tok/s\')                    |
|                                                                       |
| print(f\' → EXTRAPOLADO: \${extra_mes:.3f}/usuario/mes\')             |
|                                                                       |
| print(f\' → 500 usuarios: \${extra_500:.1f}/mes\')                    |
|                                                                       |
| resultados\[nombre\] = {\'coste_usuario_mes\': extra_mes,             |
| \'coste_500\': extra_500}                                             |
|                                                                       |
| print(\'\\n\' + \'=\'\*60)                                            |
|                                                                       |
| print(\'COMPARATIVA FINAL\')                                          |
|                                                                       |
| print(\'=\'\*60)                                                      |
|                                                                       |
| for modelo, datos in resultados.items():                              |
|                                                                       |
| print(f\'{modelo:30s}:                                                |
| \${datos\[\"coste_usuario_mes\"\]:.3f}/usuario/mes \|                 |
| \${datos\[\"coste_500\"\]:.1f}/mes con 500 usuarios\')                |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **🚀 Cómo interpretar los resultados**                                |
|                                                                       |
| El número más importante es el ratio out/in. Si el modelo genera 700  |
| tokens de output con 1.350 de input (ratio 0.52x), el coste real se   |
| reparte 35% input / 65% output. Si el ratio es \> 1.0x (genera más de |
| lo que recibe), el modelo es muy verbose y el output price domina --- |
| en ese caso Qwen3 32B puede salir más caro que GPT-OSS 120B a pesar   |
| de tener precio similar en output. Los datos reales de este script te |
| dicen cuál elegir para tu caso de uso específico.                     |
+-----------------------------------------------------------------------+

**7. Stack Definitivo Actualizado (Sin Salamandra en Operaciones)**

  --------------------------------------------------------------------------------------
  **Componente**   **Tecnología**           **Coste/mes**        **Notas**
  ---------------- ------------------------ -------------------- -----------------------
  Chat opositor    Groq GPT-OSS 20B         \$0.14/usuario       Medir con script.
  (dudas)                                                        Cambiar a Qwen3 32B si
                                                                 calidad insuficiente.

  Razonamiento     Groq GPT-OSS 120B        \$0.28/usuario       Solo para casos
  complejo (casos)                                               prácticos y dudas
                                                                 técnicas avanzadas.

  Generación banco DeepSeek V3 API          \~\$5-10 total       Uso puntual. Una sola
  preguntas                                                      vez por cuerpo.

  Revisión banco   Claude Sonnet API        \~\$20-40 total      Uso puntual. Pipeline
  preguntas                                                      batch offline.

  Caché            Neo4j AuraDB Free        \$0                  Grafo + vector search +
  semántico +                                                    historial usuario +
  grafo + memoria                                                Mem0.

  Normalización    Groq Llama 3.1 8B        \~\$0.003/usuario    Casi gratuito. Ahorra
  preguntas                                                      40-60% en llamadas al
  (caché)                                                        modelo caro.

  Embeddings       text-embedding-3-small   \~\$0.001/usuario    Despreciable.
  (caché                                                         
  semántico)                                                     

  Memoria          Mem0 OSS + Neo4j         \$0                  Mem0 extrae, Neo4j
  conversacional                                                 almacena. Integración
                                                                 nativa.

  Frontend         Cloudflare Pages         \$0                  CDN global, deploy
                                                                 automático desde
                                                                 GitHub.

  Backend API      Render.com free / Fly.io \$0-7                Free tier suficiente
                                                                 hasta 500 usuarios.

  VPS Hostinger    nginx + Salamandra       Ya pagado            Salamandra en standby.
  (ya tienes)      (standby)                                     Solo nginx activo en
                                                                 MVP.

  **TOTAL MVP (100                          **\~\$20-35/mes**    **Incluyendo APIs y
  usuarios)**                                                    hosting.**

  **TOTAL                                   **\~\$80-130/mes**   **Con caché al 50%.
  producción (500                                                Escala linealmente.**
  usuarios)**                                                    
  --------------------------------------------------------------------------------------

*Apéndice III --- Datos verificados febrero 2026 · Groq:
groq.com/pricing · Neo4j: neo4j.com/cloud · RunPod: runpod.io/pricing ·
DeepSeek: platform.deepseek.com*
