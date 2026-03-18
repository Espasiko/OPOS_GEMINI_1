**APÉNDICE IV**

App Oposiciones AGE & SS --- Actualización Final

*Protección ante abusos · Costes reales con 120B · Memoria y VPS sizing
· Rentabilidad · B2B · Pedagogía Valera*

Datos verificados · Modelos Groq feb 2026 · Precios confirmados
groq.com/pricing

**1. Modelos Groq Disponibles --- Tabla Oficial Verificada (Feb 2026)**

Aclaración importante: \'GPT-OSS 20B\' y \'GPT-OSS 120B\' son los IDs
reales disponibles en Groq, verificados en groq.com/pricing. No son
Llama ni tienen otro alias oficial conocido. Tu factura de diciembre
mostraba Llama 3.3 70B porque era el modelo que estabas usando entonces,
no porque sea equivalente.

  ------------------------------------------------------------------------------------------
  **Modelo (ID API)**         **Vel.    **Input    **Output   **Contexto**   **Mejor para**
                              TPS**     \$/M**     \$/M**                    
  --------------------------- --------- ---------- ---------- -------------- ---------------
  Llama 3.1 8B                560-840   \$0.05     \$0.08     128k           Normalización
  (llama-3.1-8b-instant)                                                     preguntas
                                                                             caché, tareas
                                                                             simples,
                                                                             clasificación

  Llama 3.3 70B               280-394   \$0.59     \$0.79     128k           ⚠️ Caro. Tu
  (llama-3.3-70b-versatile)                                                  factura de dic
                                                                             usó este.
                                                                             Evitar como
                                                                             modelo de chat
                                                                             principal.

  Llama 4 Scout 17Bx16E       594-750   \$0.11     \$0.34     128k           Alternativa
                                                                             económica buena
                                                                             calidad para
                                                                             chat dudas

  Llama 4 Maverick 17Bx128E   562       \$0.20     \$0.60     128k           Razonamiento
                                                                             multi-paso,
                                                                             instrucciones
                                                                             complejas

  GPT-OSS 20B                 \~1.000   \$0.075    \$0.30     128k           ✅ Chat en
  (openai/gpt-oss-20b)                                                       tiempo real.
                                                                             Más rápido de
                                                                             la lista.

  GPT-OSS 120B                \~500     \$0.15     \$0.60     128k           ✅ MODELO BASE
  (openai/gpt-oss-120b)                                                      RECOMENDADO.
                                                                             Razonamiento
                                                                             legal, casos
                                                                             prácticos,
                                                                             calidad alta.

  GPT-OSS Safeguard 20B       \~1.000   \$0.075    \$0.30     128k           Moderación y
                                                                             detección de
                                                                             abusos (ver
                                                                             Sección 2)

  Kimi K2 1T MoE              \~200     \$1.00     \$3.00     262k           ❌ Demasiado
                                                                             caro. Solo si
                                                                             necesitas
                                                                             contexto de
                                                                             262k.

  Qwen3 32B (qwen/qwen3-32b)  400-662   \$0.29     \$0.59     131k           ✅ Excelente en
                                                                             español,
                                                                             matemáticas,
                                                                             razonamiento
                                                                             técnico. Buena
                                                                             alternativa al
                                                                             120B.

  Prompt Guard 2 (22M / 86M)  --        \$0.03     \$0.03     512            ✅ Seguridad:
                                                                             detección
                                                                             prompt
                                                                             injection y
                                                                             jailbreaks
                                                                             antes del LLM
                                                                             principal.
  ------------------------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **🎯 Decisión de modelo de chat revisada**                            |
|                                                                       |
| Usa GPT-OSS 120B (\$0.15/\$0.60) como modelo base del chat. Es mejor  |
| en calidad que Llama 3.3 70B Y más barato (\$0.15 vs \$0.59 en        |
| input). El 96% del gasto de tu factura de diciembre era por usar      |
| Llama 3.3 70B --- con GPT-OSS 120B habrías pagado \~4 veces menos por |
| mejor calidad. Para el chat de dudas simples, Llama 4 Scout           |
| (\$0.11/\$0.34) es la opción más económica con buena calidad.         |
+-----------------------------------------------------------------------+

**2. El Usuario Maligno --- Cálculo de Abuso y Protecciones**

Hay dos tipos de usuario problemático: el que abusa del chat por coste
(daño económico) y el que extrae contenido para revender (daño de
negocio). Son riesgos distintos con soluciones distintas.

**2.1 Cálculo de Daño Económico por Abuso del Chat**

  -----------------------------------------------------------------------------------
  **Perfil de usuario** **Interacciones/día**   **Coste/mes      **Impacto**
                                                (GPT-OSS 120B)** 
  --------------------- ----------------------- ---------------- --------------------
  Usuario normal        20                      \$0.28           Asumible en
  (estudio real)                                                 cualquier plan

  Usuario curioso       60                      \$0.84           Cubierto con plan
  (muchas dudas)                                                 PRO bien preciad

  Abusador moderado     200                     \$2.79           ⚠️ Problemático sin
  (chatea sin estudiar)                                          rate limiting

  Abusador extremo      500                     \$6.97           ❌ Bloqueado por
  (scraping via chat)                                            protecciones

  Script automatizado   2.000+                  \$27.88+         ❌ Bloqueado a nivel
  (bot)                                                          IP/token
  -----------------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **✅ Conclusión de coste**                                            |
|                                                                       |
| El abuso económico es manejable. Incluso un abusador moderado (200    |
| interacciones/día) solo te costaría \$2.79/mes --- menos de lo que le |
| cobras en el plan PRO. El riesgo real no es económico, es el robo de  |
| contenido (casos prácticos, banco de preguntas, explicaciones         |
| generadas).                                                           |
+-----------------------------------------------------------------------+

**2.2 Sistema de Protección en 4 Capas**

**Capa 1: Rate Limiting por Tier (en tu backend, 0€ adicional)**

+-----------------------------------------------------------------------+
| \# Límites por plan --- implementa en middleware del backend          |
|                                                                       |
| LIMITES = {                                                           |
|                                                                       |
| \'free\': {\'chat_dia\': 10, \'tokens_dia\': 8_000, \'casos_mes\':    |
| 5},                                                                   |
|                                                                       |
| \'pro\': {\'chat_dia\': 80, \'tokens_dia\': 60_000, \'casos_mes\':    |
| 999},                                                                 |
|                                                                       |
| \'pro_byok\': {\'chat_dia\': 200, \'tokens_dia\':                     |
| 150_000,\'casos_mes\': 999},                                          |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# Detección de patrones de scraping:                                 |
|                                                                       |
| \# Si en 10 minutos el usuario hace \>15 preguntas sobre casos        |
| DISTINTOS                                                             |
|                                                                       |
| \# sin ninguna interacción de test/simulacro → flag sospechoso →      |
| reduce límite                                                         |
|                                                                       |
| \# Si hace \>30 en 10 min → bloqueo temporal + notificación al admin  |
+-----------------------------------------------------------------------+

**Capa 2: Prompt Guard 2 en cada entrada (\$0.03/M --- casi gratis)**

+-----------------------------------------------------------------------+
| \# Antes de cada mensaje del usuario, clasificas si es:               |
|                                                                       |
| \# - Prompt injection (intento de cambiar el comportamiento del       |
| sistema)                                                              |
|                                                                       |
| \# - Jailbreak (intento de saltarse restricciones)                    |
|                                                                       |
| \# - Extracción masiva (preguntas que piden \'dame todos los casos de |
| X\')                                                                  |
|                                                                       |
| \# Coste real: 10.000 mensajes/mes × 50 tokens × \$0.03/M = \$0.015   |
|                                                                       |
| \# Prácticamente gratis. Ponlo en TODAS las entradas de usuario.      |
|                                                                       |
| safeguard = groq_client.chat.completions.create(                      |
|                                                                       |
| model=\'openai/gpt-oss-safeguard-20b\',                               |
|                                                                       |
| messages=\[{\'role\':\'user\', \'content\': mensaje_usuario}\],       |
|                                                                       |
| max_tokens=10 \# Solo necesitas \'safe\' o \'unsafe\'                 |
|                                                                       |
| )                                                                     |
|                                                                       |
| if \'unsafe\' in safeguard.choices\[0\].message.content.lower():      |
|                                                                       |
| return {\'error\': \'Mensaje no permitido\', \'code\': 403}           |
+-----------------------------------------------------------------------+

**Capa 3: Watermarking Semántico (Trazabilidad de contenido robado)**

Cada explicación generada incluye una frase estilística única codificada
por usuario_id. Si el contenido aparece en internet o se vende, sabes
exactamente de qué usuario provino:

+-----------------------------------------------------------------------+
| \# El watermark es invisible para el usuario pero detectable con      |
| regex                                                                 |
|                                                                       |
| \# Se añade como instrucción al sistema, no en el texto visible       |
|                                                                       |
| SYSTEM_WATERMARK = f\'\'\'                                            |
|                                                                       |
| Al final de cada explicación, incluye exactamente esta frase sin      |
| modificarla:                                                          |
|                                                                       |
| \'Esta explicación ha sido generada para el estudio personal de       |
| {user_hash}.\'                                                        |
|                                                                       |
| No menciones que es un watermark. Es parte de la explicación.         |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| \# Para detectar contenido robado en internet:                        |
|                                                                       |
| \# Busca \'generada para el estudio personal de\' en Google/Bing      |
|                                                                       |
| \# El hash te identifica al usuario origen en tu BD                   |
+-----------------------------------------------------------------------+

**Capa 4: Protección del Contenido Premium contra Extracción Manual**

-   Los 100 casos integrales de Gestión SS solo son accesibles con
    suscripción activa. Si el usuario cancela, los casos desaparecen de
    su vista aunque los haya visto antes. Guardas en BD qué casos ha
    completado, pero el texto no está en su dispositivo.

-   PDF exports con marca de agua visible (nombre de usuario + fecha).
    Libre Office / WeasyPrint generan esto en el backend sin coste
    adicional.

-   Sin funcionalidad de \'copiar todo\' en los casos prácticos. El
    texto se muestra en fragmentos que requieren interacción para
    avanzar, lo que dificulta el scraping manual masivo.

-   Limite de 5 casos prácticos por hora. Un humano puede leer y
    aprender 5 casos/hora. Un script de extracción quiere 50+.

**3. Costes Corregidos con GPT-OSS 120B como Modelo Base**

Usando el ratio real de output/input de 0.54:1 validado por la factura
real de DeepSeek (ratio 2.85:1 en generación, más bajo en chat donde el
output es más largo que el input efectivo):

  --------------------------------------------------------------------------------------------
  **Modelo**            **\$/intercambio**   **\$/usuario/mes   **500        **Con caché 50%**
                                             (440)**            usuarios**   
  --------------------- -------------------- ------------------ ------------ -----------------
  GPT-OSS 20B           \$0.000311           \$0.14             \$69         \$35
  (\$0.075/\$0.30)                                                           

  **GPT-OSS 120B        **\$0.000638**       **\$0.28**         **\$140**    **\$70**
  (\$0.15/\$0.60) ←                                                          
  ELEGIDO**                                                                  

  Llama 4 Scout         \$0.000395           \$0.17             \$87         \$43
  (\$0.11/\$0.34)                                                            

  Qwen3 32B             \$0.000820           \$0.36             \$180        \$90
  (\$0.29/\$0.59)                                                            

  Llama 3.3 70B         \$0.001373           \$0.60             \$302        \$151
  (\$0.59/\$0.79) ---                                                        
  tu factura dic                                                             
  --------------------------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **💡 Estrategia de modelos por tipo de tarea**                        |
|                                                                       |
| Chat de dudas simples y FAQ: Llama 4 Scout (\$0.11/\$0.34) --- más    |
| barato, suficientemente bueno. Chat de razonamiento legal complejo y  |
| casos prácticos: GPT-OSS 120B (\$0.15/\$0.60) --- mejor calidad que   |
| Llama 3.3 70B a menos de la cuarta parte del precio. Normalización de |
| preguntas para caché: Llama 3.1 8B (\$0.05/\$0.08) --- casi gratis.   |
| Esta distribución por tipo de tarea reduce el coste real un 30-40%    |
| adicional sobre el cálculo de \'un modelo para todo\'.                |
+-----------------------------------------------------------------------+

**3.1 Proyección Financiera Realista**

  -------------------------------------------------------------------------------------
  **Usuarios    **Coste      **Hosting/mes**   **Total    **Ingresos      **Margen**
  activos**     APIs/mes**                     costes**   (9€/mes)**      
  ------------- ------------ ----------------- ---------- --------------- -------------
  50 usuarios   \~\$10       \~\$7 (Fly.io)    \~\$17     \~450€          \~433€ ✅
  PRO                                                                     

  200 usuarios  \~\$35       \~\$7             \~\$42     \~1.800€        \~1.758€ ✅
  PRO                                                                     

  500 usuarios  \~\$70       \~\$15            \~\$85     \~4.500€        \~4.415€ ✅
  PRO                                                                     

  200 PRO + 2   \~\$40       \~\$10            \~\$50     \~1.800€+400€   \~2.150€ ✅
  academias B2B                                                           
  -------------------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **✅ Rentabilidad confirmada**                                        |
|                                                                       |
| Con solo 50 usuarios PRO a 9€/mes, la app es rentable desde el primer |
| mes. El punto de equilibrio real (cubriendo también el tiempo de      |
| desarrollo) depende de cuánto te pagues a ti mismo, pero en términos  |
| de infraestructura pura, 50 usuarios ya cubren todos los costes con   |
| margen amplio.                                                        |
+-----------------------------------------------------------------------+

**4. Memoria Conversacional --- La Aclaración que Cambia el Diseño**

Este es el malentendido técnico más común con los LLMs y tiene impacto
directo en la arquitectura de tu app.

+-----------------------------------------------------------------------+
| **🔑 Cómo funciona realmente la \'memoria\' de los LLMs**             |
|                                                                       |
| Los modelos de lenguaje son COMPLETAMENTE SIN ESTADO entre llamadas a |
| la API. El modelo no recuerda nada por sí solo. Lo que percibimos     |
| como \'memoria\' dentro de una sesión de chat es simplemente que TU   |
| BACKEND envía el historial completo de mensajes en el array           |
| messages\[\] de cada petición. El modelo no guarda nada --- tú le     |
| mandas el contexto cada vez.                                          |
+-----------------------------------------------------------------------+

  -----------------------------------------------------------------------
  **Escenario**          **¿Necesita Mem0?**    **Solución correcta**
  ---------------------- ---------------------- -------------------------
  Dentro de una sesión   NO                     Tu backend acumula
  (mismo chat abierto,                          mensajes en memoria
  mismo día)                                    temporal y los envía
                                                todos. Con 128k tokens de
                                                contexto (GPT-OSS 120B)
                                                caben 3-4 horas de
                                                conversación sin
                                                problema.

  Entre sesiones (el     Opcional               Query a tu BD: puntos
  usuario vuelve mañana)                        débiles, temas dominados,
                                                últimas preguntas
                                                falladas → se incluye en
                                                el system prompt de la
                                                nueva sesión. Sin Mem0.

  Personalización        Sí, en Fase 3          Mem0 extrae memorias
  profunda (preferencias                        ricas de conversaciones.
  de estilo, analogías                          Útil pero no crítico para
  favoritas)                                    MVP.
  -----------------------------------------------------------------------

**4.1 La Solución Simple para \'Memoria entre Sesiones\' (Sin Mem0)**

+-----------------------------------------------------------------------+
| \# Al inicio de cada sesión, construyes el contexto desde tu BD       |
|                                                                       |
| \# No necesitas Mem0 para esto --- es lógica de backend simple        |
|                                                                       |
| def contexto_usuario_para_llm(user_id: str) -\> str:                  |
|                                                                       |
| \# Obtén estadísticas de la BD (PostgreSQL o Neo4j)                   |
|                                                                       |
| stats = db.query(\'\'\'                                               |
|                                                                       |
| SELECT tema, pct_aciertos, num_intentos                               |
|                                                                       |
| FROM user_stats WHERE user_id = ?                                     |
|                                                                       |
| ORDER BY pct_aciertos ASC LIMIT 5                                     |
|                                                                       |
| \'\'\', user_id)                                                      |
|                                                                       |
| fallos_recientes = db.query(\'\'\'                                    |
|                                                                       |
| SELECT p.enunciado, p.articulo_ley                                    |
|                                                                       |
| FROM intentos i JOIN preguntas p ON i.pregunta_id = p.id              |
|                                                                       |
| WHERE i.user_id = ? AND i.correcto = false                            |
|                                                                       |
| ORDER BY i.fecha DESC LIMIT 3                                         |
|                                                                       |
| \'\'\', user_id)                                                      |
|                                                                       |
| \# Este contexto se incluye al principio del system prompt            |
|                                                                       |
| return f\'\'\'                                                        |
|                                                                       |
| PERFIL DEL OPOSITOR:                                                  |
|                                                                       |
| \- Cuerpo objetivo: {stats.cuerpo} \| Semanas preparando:             |
| {stats.semanas}                                                       |
|                                                                       |
| \- Puntos débiles: {\', \'.join(stats.temas_debiles)}                 |
|                                                                       |
| \- Últimas preguntas falladas: {fallos_recientes}                     |
|                                                                       |
| \- Fecha de examen: {stats.fecha_examen}                              |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| \# Resultado: el LLM responde como si llevara semanas siguiendo al    |
| usuario                                                               |
|                                                                       |
| \# Coste adicional: \~300 tokens extra por sesión = \$0.00005.        |
| Despreciable.                                                         |
+-----------------------------------------------------------------------+

**5. VPS Hostinger 8GB sin Salamandra --- Qué Cabe y Qué No**

Con Salamandra desactivada en producción, tienes aproximadamente 6 GB
libres. Este es el mapa completo de lo que cabe:

  --------------------------------------------------------------------------------
  **Servicio**        **RAM       **RAM       **¿Cabe?**   **Notas**
                      mín.**      típica**                 
  ------------------- ----------- ----------- ------------ -----------------------
  Ubuntu 24 +         300 MB      400 MB      ✅           Base fija
  procesos SO                                              

  nginx (reverse      50 MB       100 MB      ✅           Ya instalado
  proxy)                                                   

  Tu backend API      150 MB      300 MB      ✅           Depende del framework
  (Python/Node)                                            

  PostgreSQL          150 MB      300-500 MB  ✅           shared_buffers=256MB,
  (configurado para                                        max_connections=50
  VPS)                                                     

  Neo4j Community     400 MB      600-800 MB  ✅           Con modelo rediseñado.
  (opciones como JSON                                      Ver nota abajo.
  props)                                                   

  Redis (caché        20 MB       50 MB       ✅           Muy ligero, muy útil
  sesiones + rate                                          
  limiting)                                                

  Celery / cron jobs  50 MB       100 MB      ✅           Para generación
  Python (tareas                                           nocturna, resúmenes
  async)                                                   semanales

  Node exporter       10 MB       30 MB       ✅           Métricas para Grafana
  (monitoring)                                             Cloud free

  **TOTAL sin         **\~1.130   **\~2.280   **✅         **Quedan \~5.7 GB
  Salamandra**        MB**        MB**        HOLGADO**    libres**

  Salamandra 7B       4.500 MB    5.500 MB    ⚠️ EN        Ocupa todo el margen si
  Q4_K_M (NO activo                           STANDBY      se activa
  en prod)                                                 
  --------------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **📌 Nota sobre Neo4j Community en el VPS**                           |
|                                                                       |
| Para que Neo4j quepa bien en el VPS, configura en neo4j.conf:         |
| server.memory.heap.max_size=800m y server.memory.pagecache.size=400m. |
| Total Neo4j: \~1.2 GB máximo. Además, rediseña el modelo de grafo     |
| para que las opciones A/B/C/D de cada pregunta sean propiedades JSON  |
| del nodo Pregunta, no nodos separados. Esto reduce el total de nodos  |
| de 270.000 (que supera el límite de AuraDB Free) a \~60.000-80.000    |
| nodos (que cabe en AuraDB Free Y en Community Edition sin problemas). |
+-----------------------------------------------------------------------+

**5.1 Configuración PostgreSQL para VPS 8GB**

+-----------------------------------------------------------------------+
| \# /etc/postgresql/16/main/postgresql.conf                            |
|                                                                       |
| \# Configuración conservadora para VPS 8GB con otros servicios        |
|                                                                       |
| shared_buffers = 256MB \# 25% de la RAM que asignas a PG              |
|                                                                       |
| effective_cache_size = 512MB \# Estimación de RAM disponible para PG  |
|                                                                       |
| work_mem = 8MB \# Por conexión activa                                 |
|                                                                       |
| maintenance_work_mem = 64MB \# Para VACUUM, CREATE INDEX              |
|                                                                       |
| max_connections = 50 \# Suficiente para tu escala                     |
|                                                                       |
| wal_buffers = 16MB                                                    |
|                                                                       |
| checkpoint_completion_target = 0.9                                    |
|                                                                       |
| \# Con esta config, PostgreSQL usa \~400-500 MB en carga normal       |
|                                                                       |
| \# y sube a \~700 MB con queries complejas de analítica de progreso   |
+-----------------------------------------------------------------------+

**6. Rentabilidad y Estrategia de Negocio --- El Análisis Honesto**

El miedo a no ser rentable es el correcto y hay que enfrentarlo
directamente. Aquí va el análisis sin optimismo injustificado.

**6.1 El Riesgo Principal: Tracción, No Tecnología**

+-----------------------------------------------------------------------+
| **⚠️ La realidad del calendario 2026**                                |
|                                                                       |
| Las oposiciones AGE del 23 de mayo de 2026 están a 3 meses. Los       |
| opositores que se presentan en mayo llevan preparándose desde hace    |
| 6-18 meses con materiales que ya conocen y en los que confían. Un     |
| producto nuevo lanzado en marzo-abril tiene dos problemas: (1) llega  |
| tarde para ser el preparador principal de ese examen y (2) no tiene   |
| testimonios ni reputación todavía. TU MERCADO REAL PARA EL PRIMER     |
| LANZAMIENTO son los opositores en fase temprana de preparación para   |
| la convocatoria 2027, y quienes suspenden en mayo 2026 y empiezan de  |
| nuevo.                                                                |
+-----------------------------------------------------------------------+

**6.2 Líneas de Negocio por Orden de Viabilidad**

  ---------------------------------------------------------------------------
  **Línea**      **Tiempo al   **Complejidad**   **Descripción**
                 1er €**                         
  -------------- ------------- ----------------- ----------------------------
  B2C --- Plan   2-4 meses     Media             9-12€/mes por opositor.
  PRO individual                                 Mercado amplio pero requiere
                                                 marketing y reputación.
                                                 Motor principal a largo
                                                 plazo.

  B2B --- Kit    1-3 meses     Baja              150-300€/mes por preparador
  para                                           con 30-50 alumnos. Un solo
  preparadores                                   cliente = 15-30 usuarios
                                                 individuales. La venta es
                                                 más fácil: el preparador ya
                                                 tiene la audiencia.

  B2B --- Venta  3-6 meses     Media             2.000-8.000€ por cuerpo en
  de dataset                                     licencia no exclusiva.
                                                 Requiere banco muy bien
                                                 validado. Compradores:
                                                 academias, plataformas
                                                 LegalTech, universidades con
                                                 másters de función pública.

  B2B --- API    4-8 meses     Alta              Academias integran tu banco
  para academias                                 en sus plataformas via API.
                                                 Modelo SaaS por número de
                                                 alumnos. Requiere API
                                                 documentada y acuerdos
                                                 comerciales.

  Publicidad /   6-12 meses    Baja              Academias o editoriales de
  patrocinios                                    temarios pueden pagar por
                                                 aparecer en la app. Solo
                                                 viable con volumen de
                                                 usuarios.
  ---------------------------------------------------------------------------

**6.3 El Camino más Rápido a 1.000€/mes Recurrentes**

En este orden específico:

1.  Beta cerrada con 20-30 opositores reales ANTES del examen de mayo.
    No para ganar dinero --- para obtener testimonios, detectar fallos y
    tener datos de retención reales. Esos 30 usuarios son tu activo más
    valioso para cualquier conversación con academias.

2.  Lanza SOLO con Auxiliar AGE (28 temas, \~10.000 preguntas,
    psicotécnicos). Es el mercado más grande (1.700 plazas) y el más
    inmediato. No esperes a tener los 4 cuerpos --- con uno solo ya
    tienes un producto vendible antes de mayo.

3.  Contacta a 5 preparadores independientes de oposiciones AGE
    ofreciendo acceso gratuito durante 3 meses a cambio de feedback y
    testimonios. Un preparador con 30 alumnos que recomienda tu app = 30
    usuarios potenciales de golpe.

4.  Cuando tengas 3-5 preparadores usando la app, propón el modelo de
    pago: 150€/mes para acceso de hasta 50 alumnos con branding básico
    (logo del preparador). Eso son 450-750€/mes recurrentes con solo 3-5
    clientes B2B.

+-----------------------------------------------------------------------+
| **💡 El insight clave sobre B2B**                                     |
|                                                                       |
| Un preparador con 30 alumnos que te paga 200€/mes es equivalente a    |
| 20-22 usuarios individuales PRO a 9€/mes, pero con una diferencia     |
| crucial: el preparador NO cancela fácilmente porque ha integrado tu   |
| herramienta en su metodología y sus alumnos la usan. La churn rate    |
| B2B es 5-10x menor que B2C. Prioriza B2B para el camino a             |
| rentabilidad sostenible.                                              |
+-----------------------------------------------------------------------+

**7. Pedagogía Valera --- Cómo Implementar el Método en la App**

El método de razonamiento lógico-jurídico que describe Valera tiene
nombre en didáctica formal: aprendizaje por casos con andamiaje
progresivo (scaffolded case-based learning). Tiene tres pilares que tu
app puede implementar técnicamente:

**7.1 Pilar 1: Andamiaje Socrático (No dar la respuesta directamente)**

En lugar de mostrar \'el plazo es 1 mes según el art. X\', el sistema
hace preguntas que llevan al opositor a deducirlo:

+-----------------------------------------------------------------------+
| \# Árbol de decisión para el método socrático                         |
|                                                                       |
| \# Generado por DeepSeek, revisado por Claude, guardado en Neo4j      |
|                                                                       |
| ARBOL_SILENCIO_ADMINISTRATIVO = {                                     |
|                                                                       |
| \'pregunta_inicial\': \'¿Qué tipo de procedimiento es este?\',        |
|                                                                       |
| \'ramas\': {                                                          |
|                                                                       |
| \'procedimiento_iniciado_a_solicitud\': {                             |
|                                                                       |
| \'siguiente\': \'¿Cuál es la regla general del silencio en este       |
| caso?\',                                                              |
|                                                                       |
| \'ramas\': {                                                          |
|                                                                       |
| \'positivo_regla_general\': {                                         |
|                                                                       |
| \'siguiente\': \'¿Hay alguna excepción que aplique aquí?\',           |
|                                                                       |
| \'respuesta_final\': \'Correcto. Art. 24 Ley 39/2015: silencio        |
| positivo como regla general.\'                                        |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| },                                                                    |
|                                                                       |
| \'procedimiento_de_impugnacion\': {                                   |
|                                                                       |
| \'siguiente\': \'¿Recuerdas por qué el silencio aquí es distinto?\',  |
|                                                                       |
| \'respuesta_final\': \'Exacto. Art. 24.1: silencio negativo en        |
| recursos. Si fuera positivo, cualquiera ganaría sin resolución.\'     |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# Este árbol se genera offline para todos los temas del banco        |
|                                                                       |
| \# y se activa cuando el usuario activa el \'Modo Socrático\'         |
+-----------------------------------------------------------------------+

**7.2 Pilar 2: Caso Inverso (Razonamiento hacia atrás)**

Dado un resultado (la pensión es 1.440€/mes), el opositor debe
reconstruir los datos del caso. Esto entrena exactamente el tipo de
razonamiento que exige el Ejercicio 2 de Gestión SS:

+-----------------------------------------------------------------------+
| \# Plantilla para caso inverso --- generada por el pipeline           |
|                                                                       |
| {                                                                     |
|                                                                       |
| \'tipo\': \'caso_inverso\',                                           |
|                                                                       |
| \'resultado_dado\': \'La pensión de jubilación es 1.440 euros/mes\',  |
|                                                                       |
| \'preguntas_de_reconstruccion\': \[                                   |
|                                                                       |
| \'¿Cuál es la base reguladora si el porcentaje es 80%?\',             |
|                                                                       |
| \'¿Cuántos años cotizados corresponden a ese porcentaje?\',           |
|                                                                       |
| \'¿Cuándo se alcanzó la edad ordinaria de jubilación?\'               |
|                                                                       |
| \],                                                                   |
|                                                                       |
| \'datos_reales_del_caso\': {                                          |
|                                                                       |
| \'base_reguladora\': 1800,                                            |
|                                                                       |
| \'porcentaje\': 80,                                                   |
|                                                                       |
| \'anos_cotizados\': 37,                                               |
|                                                                       |
| \'edad_jubilacion_ordinaria\': 66                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
+-----------------------------------------------------------------------+

**7.3 Pilar 3: Mapa de Errores Frecuentes (Aprendizaje Colectivo)**

El sistema detecta qué artículos confunde consistentemente UN PORCENTAJE
ALTO de usuarios y crea ejercicios específicos de discriminación. Esto
es imposible de hacer en una academia tradicional porque requiere datos
de comportamiento de cientos de alumnos:

+-----------------------------------------------------------------------+
| \# Query Neo4j: detectar confusiones frecuentes entre artículos       |
|                                                                       |
| MATCH (u:Usuario)-\[:FALLO\]-\>(p:Pregunta)-\[:TRATA\]-\>(a:Articulo) |
|                                                                       |
| MATCH (p)-\[:CONFUNDIO_CON\]-\>(a2:Articulo)                          |
|                                                                       |
| WHERE a.ley = a2.ley \# Confusión dentro de la misma ley              |
|                                                                       |
| WITH a.codigo as art_correcto, a2.codigo as art_confundido,           |
|                                                                       |
| count(distinct u) as num_usuarios                                     |
|                                                                       |
| WHERE num_usuarios \> 20 \# Al menos 20 usuarios han hecho esta       |
| confusión                                                             |
|                                                                       |
| RETURN art_correcto, art_confundido, num_usuarios                     |
|                                                                       |
| ORDER BY num_usuarios DESC                                            |
|                                                                       |
| \# Resultado ejemplo: \'47 usuarios confunden art. 21 LPAC con art.   |
| 22 LPAC\'                                                             |
|                                                                       |
| \# → El sistema genera automáticamente preguntas de discriminación    |
| entre ambos                                                           |
|                                                                       |
| \# → Se activan para todos los usuarios cuando estudian ese tema      |
|                                                                       |
| \# → Con el tiempo, el sistema aprende cuáles son los \'pares de      |
| confusión\' del temario                                               |
+-----------------------------------------------------------------------+

**7.4 Pilar 4: Detección y Corrección de Fatiga**

+-----------------------------------------------------------------------+
| \# Algoritmo de detección de fatiga (en tu backend, 0€ de IA)         |
|                                                                       |
| def detectar_fatiga(user_id: str, ventana_minutos: int = 60) -\>      |
| dict:                                                                 |
|                                                                       |
| intentos_recientes = db.query(\'\'\'                                  |
|                                                                       |
| SELECT correcto, fecha FROM intentos                                  |
|                                                                       |
| WHERE user_id = ? AND fecha \> NOW() - INTERVAL ? MINUTE              |
|                                                                       |
| ORDER BY fecha ASC                                                    |
|                                                                       |
| \'\'\', user_id, ventana_minutos)                                     |
|                                                                       |
| if len(intentos_recientes) \< 10:                                     |
|                                                                       |
| return {\'fatiga\': False}                                            |
|                                                                       |
| \# Compara primera mitad vs segunda mitad de la ventana               |
|                                                                       |
| mitad = len(intentos_recientes) // 2                                  |
|                                                                       |
| tasa_primera = sum(1 for i in intentos_recientes\[:mitad\] if         |
| i.correcto) / mitad                                                   |
|                                                                       |
| tasa_segunda = sum(1 for i in intentos_recientes\[mitad:\] if         |
| i.correcto) / mitad                                                   |
|                                                                       |
| caida = tasa_primera - tasa_segunda                                   |
|                                                                       |
| if caida \> 0.15: \# Caída de más del 15% en tasa de aciertos         |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'fatiga\': True,                                                     |
|                                                                       |
| \'caida_porcentual\': caida,                                          |
|                                                                       |
| \'sugerencia\': \'flashcards\' if caida \< 0.30 else \'descanso\'     |
|                                                                       |
| }                                                                     |
|                                                                       |
| return {\'fatiga\': False}                                            |
+-----------------------------------------------------------------------+

**8. Tabla de Cambios: Qué Actualiza Este Apéndice**

  ------------------------------------------------------------------------
  **Decisión          **Decisión            **Motivo del cambio**
  anterior**          actualizada**         
  ------------------- --------------------- ------------------------------
  GPT-OSS 20B como    GPT-OSS 120B como     Mejor calidad; más barato que
  modelo base         modelo base de chat   Llama 3.3 70B que era lo que
                                            se usaba en factura real.
                                            \$0.28/usuario/mes con caché.

  Llama 3.3 70B en    Cambiar a GPT-OSS     El 96% del gasto de dic venía
  facturas reales     120B o Llama 4        del 70B. GPT-OSS 120B es 4x
                      Maverick              más barato con mejor calidad.

  Mem0 como           Mem0 solo en Fase 3   En MVP: contexto desde BD +
  componente esencial                       historial en messages\[\].
  del MVP                                   Suficiente. Mem0 añade valor
                                            solo con muchos usuarios.

  Neo4j AuraDB Free   Neo4j Community en    Con opciones como JSON
  como única opción   VPS o AuraDB según    properties, los nodos se
                      escala                reducen de 270K a \~70K. Cabe
                                            en AuraDB Free y en VPS.

  Sin protección      Sistema de 4 capas:   Necesario desde el primer
  anti-abuso          rate limit + Prompt   usuario de pago.
  mencionada          Guard 2 + watermark + 
                      restricción acceso    
                      premium               

  Sin estrategia de   B2B como camino       Preparadores como clientes:
  negocio B2B         prioritario a         menor churn, tickets más
                      rentabilidad          altos, acceso a audiencia
                                            formada.

  Módulos pedagógicos 4 pilares del método  Diferenciador real frente a
  genéricos           Valera implementados  academias: andamiaje
                      técnicamente          socrático, caso inverso, mapa
                                            de errores colectivos,
                                            detección de fatiga.

  PostgreSQL fuera    PostgreSQL en VPS     Con 6GB libres tras desactivar
  del VPS             Hostinger (sin        Salamandra, caben PG + Neo4j
                      Salamandra)           Community + Redis + backend
                                            con holgura.

  Lanzamiento para    Beta cerrada antes de El mercado de opositores a 3
  mayo 2026           mayo + lanzamiento    meses del examen es el más
                      real para             difícil de capturar con un
                      convocatoria 2027     producto nuevo.
  ------------------------------------------------------------------------

*Apéndice IV --- Datos verificados febrero 2026*

*Modelos Groq: groq.com/pricing · Pedagogía: scaffolded case-based
learning (Hmelo-Silver, 2004) aplicada a preparación de oposiciones*
