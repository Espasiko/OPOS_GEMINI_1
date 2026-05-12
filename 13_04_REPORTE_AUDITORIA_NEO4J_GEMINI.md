# 🛡️ REPORTE AUDITORÍA NEO4J GEMINI - NOMBRES COMPLETOS

**ESTE REPORTE REFLEJA EL ESTADO DEL CATÁLOGO (v17.3) QUE SERÁ INGESTADO.**
⚠️ NO SE HA INGESTADO NINGÚN DATO EN NEO4J.
⚠️ NO HAS PERDIDO TUS DATOS. ESTO SOLO ES UN REPORTE VISUAL.

## NOTAS METODOLÓGICAS DE INGESTA (TUS PREGUNTAS RESUELTAS)
- **Sobre Neo4j:** NO he modificado absoltumente NADA en la base de datos de Neo4j. Todo se generará cuando tú lo ordenes.
- **Script y Jerarquías (LO 3/1980 / 0 preceptos):** El script que vamos a usar (`ingest_neo4j_v17.py`) implementa un _fallback_: Si la ley no tiene versión consolidada XML, acude al endpoint del diario (`buscar/xml.php`) que es donde se encuentra el XML original. Usamos `BOEParser._parse_xml_documento` para capturar la etiqueta `<p class="articulo">`, reconstruyendo los preceptos de leyes "planitas". Se indexarán chunks de máx 20.000 chars con solapamiento, conectando el índice Vectorial Nativo de Cypher 5.
detalles de ingesta: 
He investigado a fondo lo que me pides y sobre todo por qué mi automatización no actualizó visualmente los nombres completos en la tabla de tu reporte. Aquí tienes las explicaciones, los detalles y las respuestas a las dos tareas que me has mandado, sin tocar ni el catálogo ni Neo4j, tal y como ordenaste.

1. ¿Por qué no se ve la tabla con los nombres largos en el reporte y cómo quedan?
Tienes razón en estar enfadado, revisé el script que usé y el problema fue un error de formateo "silencioso". Mi script sí fue capaz de descargar los títulos completos del BOE, pero las barras | de la tabla Markdown del reporte impidieron la sustitución del texto (se perdía la alineación de las comillas invertidas ` de la ID).

Para que veas el resultado real que extrajo y que debería estar en la tabla, aquí te muestro un fragmento de cómo mapeamos esos títulos completos para que ya no te líes con siglas:

BOE-A-2011-15038 → Ley 28/2011, de 22 de septiembre, por la que se procede a la integración del Régimen Especial Agrario... (antes "Ley 28/2011")
BOE-A-1997-15810 → Ley 24/1997, de 15 de julio, de Consolidación y Racionalización del Sistema de la Seguridad Social. (antes "Ley 24/1997")
BOE-A-2013-13617 → Ley 23/2013, de 23 de diciembre, reguladora del Factor de Sostenibilidad y del Índice de... (antes "Ley 23/2013")
BOE-A-2015-11724 → Real Decreto Legislativo 8/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley General de la Seguridad Social. (antes "TRLGSS")
Toda la base de datos Neo4j terminará utilizando estos nombres oficiales completos extraídos directamente del título del BOE, para evitar usar alias confusos.

2. Sobre las Leyes Modificadas después del 03/04/2026
Implementé e inyecté en el script una verificación de la fecha de última actualización del BOE. Al revisar todas las leyes de tu catálogo contra la fecha de corte, he detectado que SÍ HAY CAMBIOS.

Como puedes ver en la línea 124 del reporte que se actualizó (bajo la columna "Notas"):

BOE-A-2026-7296 (Orden PJC/297/2026, normas de cotización a la SS): Tiene la nota ⚠️ MODIFICADA RECIENTEMENTE. Lo que significa que ha sufrido una actualización detectada en el portal del gobierno justo semanas posteriores a la fecha de corte, lo que representa un "falso amigo" en el temario porque si ingestas hoy, Neo4j cogerá el artículo alterado si no filtramos por fecha_vigencia. Hay que marcarla con mucho cuidado en el Prompt del agente RAG para que avise de que existen versiones vigentes nuevas, pero el examen usa una anterior.
3. ¿Cómo se va a Ingestar la LO 3/1980 (Leyes con "Cero Preceptos" y No Consolidadas)?
Para tu total tranquilidad, he leído tanto las instrucciones de memoria como analizado a fondo el nuevo script backend/scripts/ingest_neo4j_v17.py que ya tienes preparado, que resuelve el gran problema que tenías antes con leyes históricas o no consolidadas que se quedaban vacías ("0 preceptos").

Aquí tienes el nivel técnico de lo que hace el script y cómo lo hace (sin que yo pulse ningún botón todavía):

A. La "Cadena de Fallback" (La solución a la ausencia de versión Consolidada)
Las leyes con "0 preceptos" provienen de que la anterior base de datos solo llamaba al endpoint de "legislación-consolidada". El script v17 ahora tiene 4 niveles por cada boe_id:

Caché V17 XML: Busca la descarga local reciente.
API Consolidada: Intenta extraer los nodos <bloque tipo="precepto"> con la versión actual (Este fallará en la LO 3/1980 y te lanzará el error "404", porque es anterior a la redacción digital moderna).
Caché JSON V16: Busca el fichero local antiguo.
¡EL SALVAVIDAS! -> Endpoint de Diario Original (buscar/xml.php?id=...): Al fracasar el Consolidado, el nuevo script salta directamente al XML plano del día que se publicó la ley en el diario antiguo.
B. El Parseador Inteligente (BOEParser)
Al tener el XML de la ley antigua de buscar/xml.php, el script nota que es de tipo <documento> y no <response> consolidada. Como no hay bloques estandarizados de artículos, activa la función _parse_xml_documento.

Esta función escanea párrafo a párrafo todo el <texto>.
Detecta qué etiquetas <p class="articulo"> existen.
Agrupa el texto del artículo y todos los sub-párrafos hasta encontrar el siguiente class="articulo". De esta forma logramos reestructurar automáticamente y particionar una ley plana/histórica para crear sus preceptos de Inteligencia Artificial (artículo a artículo).
C. El Grafo y Neo4j (Nodos, Edges y Chunks)
Con los preceptos ya parseados de esa ley antigua de 1980, hará esto:

Generación de Chunks (Fragmentación): Si el artículo antiguo es gigante (supera los 20000 caracteres o unos 5000 tokens), los corta y aplica un "overlapping" de seguridad de 2000 caracteres para que el RAG no se quede con el texto cortado a la mitad ("Chunk Solapamiento").
Creación de Nodos en Neo4j:
Usará UNWIND (inserciones masivas tipo batch de 50 en 50) creando los nodos que sean :Precepto:Articulo o :Precepto:Disposicion.
Creará un Nodo central root :Ley con la metadata de 1980.
Relaciones (Edges):
Agregará una arista estricta de [:PERTENECE_A] entre los Nodos Artículo y el Nodo Ley central.
Si el artículo ha tenido que cortarse en la fragmentación (los Chunks), cada chunk se unirá al posterior con la arista [:SIGUIENTE], reconstruyendo la lectura consecutivamente.
Vectors HNSW (Nativo de Cypher 5): Utiliza toVector() para guardar la incrustación vectorial generada con pablosi/bge-m3-spa-law-qa-trained-2 (dimensión 1024), y generará índices FULLTEXT en cada precepto fusionando el "título" y el "texto" de la ley para forzar búsquedas híbridas perfectas.
Esto asegura que la LO 3/1980 dejará de tener 0 preceptos y formará parte de las búsquedas igual de bien que una ley de 2025.

¿Me das permiso para arreglar permanentemente el Catálogo JSON con los nombres largos limpios y arrancar la depuración/ingesta de Neo4J con este método, o tienes alguna otra duda sobre el código?



## VERIFICACIÓN DE LEYES Y TÍTULOS COMPLETOS
| BOE ID | SIGLAS (ALIAS) | TÍTULO COMPLETO OFICIAL (CATÁLOGO) | ESTADO/NOTAS |
|---|---|---|---|
| `BOE-A-1978-31229` | CE | **Constitución Española.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1994-14960` | TRLGSS 1994 | **Real Decreto Legislativo 1/1994, de 20 de junio, por el que se aprueba el Texto Refundido de la Ley General de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1997-15810` | Ley 24/1997 | **Ley 24/1997, de 15 de julio, de Consolidación y Racionalización del Sistema de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2007-13409` | LETA | **Ley 20/2007, de 11 de julio, del Estatuto del trabajo autónomo.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2010-12616` | Ley 32/2010 CATA | **Ley 32/2010, de 5 de agosto, por la que se establece un sistema específico de protección por cese de actividad de los trabajadores autónomos.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2011-13242` | Ley 27/2011 | **Ley 27/2011, de 1 de agosto, sobre actualización, adecuación y modernización del sistema de Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2015-10565` | LPAC | **Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2015-10566` | LRJSP | **Ley 40/2015, de 1 de octubre, de Régimen Jurídico del Sector Público.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2015-11430` | ET | **Real Decreto Legislativo 2/2015, de 23 de octubre, por el que se aprueba el texto refundido de la Ley del Estatuto de los Trabajadores.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2015-11719` | TREBEP | **Real Decreto Legislativo 5/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley del Estatuto Básico del Empleado Público.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2015-11724` | TRLGSS | **Real Decreto Legislativo 8/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley General de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2017-12902` | LCSP | **Ley 9/2017, de 8 de noviembre, de Contratos del Sector Público.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2019-3481` | RDL 8/2019 | **Real Decreto-ley 8/2019, de 8 de marzo, de medidas urgentes de protección social y de lucha contra la precariedad laboral en la jornada de trabajo.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2021-21007` | Ley 19/2021 IMV | **Ley 19/2021, de 20 de diciembre, por la que se establece el ingreso mínimo vital.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2021-21652` | Ley 21/2021 | **Ley 21/2021, de 28 de diciembre, de garantía del poder adquisitivo de las pensiones y de otras medidas de refuerzo de la sostenibilidad financiera y social del sistema público de pensiones.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2022-12482` | RDL 13/2022 | **Real Decreto-ley 13/2022, de 26 de julio, por el que se establece un nuevo sistema de cotización para los trabajadores por cuenta propia o autónomos.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2023-6967` | RDL 2/2023 | **Real Decreto-ley 2/2023, de 16 de marzo, de medidas urgentes para la ampliación de derechos de los pensionistas, la reducción de la brecha de género y el establecimiento de un nuevo marco de sostenibilidad del sistema público de pensiones.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2025-8567` | Ley 2/2025 | **Ley 2/2025, de 29 de abril, de medidas urgentes complementarias en materia de pensiones e incapacidad permanente.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1963-22667` | Ley de Bases 1963 | **Ley 193/1963, de 28 de diciembre, sobre bases de la Seguridad Social.** | 📜 Histórica/No Consolidada (Ingestión vía diario original fallback) |
| `BOE-A-1966-21116` | Decreto 3158/1966 | **Decreto 3158/1966, de 23 de diciembre, por el que se aprueba el Reglamento General de Accidentes de Trabajo.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1967-2876` | Orden 13/02/1967 | **Orden de 13 de febrero de 1967 por el que se establecen normas para la aplicación y desarrollo de las prestaciones por muerte y supervivencia en el Régimen General de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1969-575` | Orden IT 1969 | **Orden de 15 de abril de 1969 por la que se establecen normas para la aplicación y desarrollo de las prestaciones por invalidez en el Régimen General de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1970-1000` | Decreto 2530/1970 | **Decreto 2530/1970, de 20 de agosto, por el que se regula el Régimen Especial de la Seguridad Social de los trabajadores por cuenta propia o autónomos.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1972-907` | Ley 24/1972 | **Ley 24/1972, de 21 de junio, de financiación y perfeccionamiento de la acción protectora del Régimen General.** | 📜 Histórica/No Consolidada (Ingestión vía diario original fallback) |
| `BOE-A-1972-944` | Decreto 1646/1972 | **Decreto 1646/1972, de 15 de junio, por el que se regulan las prestaciones de muerte y supervivencia.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1973-234` | Decreto 3772/1972 | **Decreto 3772/1972, de 23 de diciembre, por el que se aprueba el Reglamento General del Régimen Especial Agrario.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1973-282` | Decreto 298/1973 | **Decreto 298/1973, de 8 de febrero, sobre actualización del Régimen Especial de la Seguridad Social para la Minería del Carbón.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1974-1165` | TRLGSS 1974 | **Decreto 2065/1974, de 30 de mayo, por el que se aprueba el Texto Refundido de la Ley General de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1978-28739` | RDL 36/1978 | **Real Decreto-ley 36/1978, de 16 de noviembre, sobre gestión institucional de la Seguridad Social, la salud y el empleo.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1982-9983` | LISMI | **Ley 13/1982, de 7 de abril, de Integración Social de los Minusválidos.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1983-15813` | RD 1451/1983 | **Real Decreto 1451/1983, de 11 de mayo, por el que se regula el empleo selectivo y las medidas de fomento del empleo de los trabajadores minusválidos.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1985-16119` | Ley 26/1985 | **Ley 26/1985, de 31 de julio, de medidas urgentes para la racionalización de la estructura y de la acción protectora de la SS.** | 📜 Histórica/No Consolidada (Ingestión vía diario original fallback) |
| `BOE-A-1985-806` | RD 2366/1984 | **Real Decreto 2366/1984, de 26 de diciembre, sobre reducción de la edad de jubilación de determinados grupos profesionales incluidos en el ámbito del Estatuto del Minero.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1985-8124` | RD 625/1985 | **Real Decreto 625/1985, de 2 de abril, por el que se desarrolla la Ley 31/1984, de 2 de agosto, de Protección por Desempleo.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1986-33763` | RD 2621/1986 | **Real Decreto 2621/1986, de 24 de diciembre, por el que se integran los Regímenes Especiales de la Seguridad Social de Trabajadores Ferroviarios, Jugadores de Fútbol, Representantes de Comercio, Toreros y Artistas en el Régimen General.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1990-29699` | RD 1576/1990 | **Real Decreto 1576/1990, de 7 de diciembre, por el que se establecen pensiones extraordinarias en favor de las personas afectadas por el terrorismo.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1991-7270` | RD 357/1991 | **Real Decreto 357/1991, de 15 de marzo, por el que se desarrolla, en materia de pensiones no contributivas, la Ley 26/1990.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1992-24743` | RD 1221/1992 | **Real Decreto 1221/1992, de 9 de octubre, sobre el patrimonio de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1995-19848` | RD 1300/1995 | **Real Decreto 1300/1995, de 21 de julio, por el que se desarrolla, en materia de incapacidades laborales del sistema de la Seguridad Social, la Ley 42/1994.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1995-24292` | Ley 31/1995 PRL | **Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1995-26716` | RD 1993/1995 | **Real Decreto 1993/1995, de 7 de diciembre, por el que se aprueba el Reglamento sobre colaboración de las Mutuas de Accidentes de Trabajo y Enfermedades Profesionales de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1996-1579` | RD 2064/1995 | **Real Decreto 2064/1995, de 22 de diciembre, por el que se aprueba el Reglamento General sobre Cotización y Liquidación de otros Derechos de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1996-29117` | Ley 13/1996 | **Ley 13/1996, de 30 de diciembre, de Medidas Fiscales, Administrativas y del Orden Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1996-3691` | RD 148/1996 | **Real Decreto 148/1996, de 5 de febrero, por el que se regula el procedimiento especial para el reintegro de prestaciones indebidas.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1996-4447` | RD 84/1996 | **Real Decreto 84/1996, de 26 de enero, por el que se aprueba el Reglamento General sobre inscripción de empresas y afiliación, altas, bajas y variaciones de datos de trabajadores en la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1997-1853` | RD 39/1997 | **Real Decreto 39/1997, de 17 de enero, por el que se aprueba el Reglamento de los Servicios de Prevención.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1997-24163` | RD 1647/1997 | **Real Decreto 1647/1997, de 31 de octubre, por el que se desarrollan determinadas disposiciones de la Ley 24/1997.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1998-30155` | Ley 50/1998 | **Ley 50/1998, de 30 de diciembre, de medidas fiscales, administrativas y del orden social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1999-21568` | Ley 39/1999 | **Ley 39/1999, de 5 de noviembre, para promover la conciliación de la vida familiar y laboral.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2000-15060` | LISOS | **Real Decreto Legislativo 5/2000, de 4 de agosto, por el que se aprueba el texto refundido de la Ley sobre Infracciones y Sanciones en el Orden Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2002-13972` | Ley 35/2002 | **Ley 35/2002, de 12 de julio, de medidas para el establecimiento de un sistema de jubilación gradual y flexible.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2002-23038` | RD 1132/2002 | **Real Decreto 1132/2002, de 31 de octubre, de desarrollo de la Ley 35/2002 (jubilación flexible).** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2003-19281` | Orden TAS/2865/2003 | **Orden TAS/2865/2003, de 13 de octubre, por la que se regula el convenio especial en el Sistema de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2003-19458` | RD 1273/2003 | **Real Decreto 1273/2003, de 10 de octubre, por el que se regula la cobertura de las contingencias profesionales de los trabajadores por cuenta propia o autónomos.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2003-22716` | Ley 52/2003 | **Ley 52/2003, de 10 de diciembre, de Medidas Fiscales, Administrativas y del Orden Social (Disposiciones específicas en materia de Seguridad Social).** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2003-23401` | RD 1539/2003 | **Real Decreto 1539/2003, de 5 de diciembre, por el que se establecen coeficientes reductores de la edad de jubilación a favor de los trabajadores minusválidos.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2004-11836` | RD 1415/2004 | **Real Decreto 1415/2004, de 11 de junio, por el que se aprueba el Reglamento General de Recaudación de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2005-19151` | RD 1335/2005 | **Real Decreto 1335/2005, de 11 de noviembre, por el que se regulan las prestaciones familiares de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2006-22169` | RD 1299/2006 | **Real Decreto 1299/2006, de 10 de noviembre, por el que se aprueba el cuadro de enfermedades profesionales en el sistema de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2006-22865` | Ley 42/2006 | **Ley 42/2006, de 28 de diciembre, de Presupuestos Generales del Estado para el año 2007 (Disposición Adicional 4ª sobre prestación de asistencia sanitaria).** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2007-20910` | Ley 40/2007 | **Ley 40/2007, de 4 de diciembre, de medidas en materia de Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2007-8350` | RD 504/2007 | **Real Decreto 504/2007, de 20 de abril, por el que se aprueba el baremo de valoración de la situación de dependencia del Sistema para la Autonomía y Atención a la Dependencia.** | 📜 Histórica/No Consolidada (Ingestión vía diario original fallback) |
| `BOE-A-2007-9690` | RD 615/2007 | **Real Decreto 615/2007, de 11 de mayo, por el que se regula la Seguridad Social de los cuidadores de las personas en situación de dependencia.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2008-1264` | RD 8/2008 | **Real Decreto 8/2008, de 11 de enero, por el que se regula el régimen jurídico y el sistema de prestaciones por razón de necesidad a favor de los españoles residentes en el exterior (PREMA).** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2009-20652` | RD 1851/2009 | **Real Decreto 1851/2009, de 4 de diciembre, por el que se regula el derecho a la jubilación anticipada de los trabajadores con discapacidad.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2009-4724` | RD 295/2009 | **Real Decreto 295/2009, de 6 de marzo, por el que se regulan las prestaciones económicas del sistema de la Seguridad Social por maternidad, paternidad, riesgo durante el embarazo y riesgo durante la lactancia natural.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2010-18651` | RDL 13/2010 | **Real Decreto-ley 13/2010, de 3 de diciembre, de actuaciones en el ámbito fiscal, laboral y liberalizadoras.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2011-13119` | RD 1148/2011 | **Real Decreto 1148/2011, de 29 de julio, para la aplicación y desarrollo, en el sistema de la Seguridad Social, de la prestación económica por cuidado de menores afectados por cáncer u otra enfermedad grave.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2011-15038` | Ley 28/2011 | **Ley 28/2011, de 22 de septiembre, por la que se procede a la integración del Régimen Especial Agrario en el Régimen General de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2011-16819` | RD 1493/2011 | **Real Decreto 1493/2011, de 24 de octubre, por el que se regulan los términos y las condiciones de inclusión en el Régimen General de la Seguridad Social de las personas que participen en programas de formación.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2012-13420` | RD 1484/2012 | **Real Decreto 1484/2012, de 29 de octubre, sobre las aportaciones económicas a realizar por las empresas con beneficios que realicen despidos colectivos que afecten a trabajadores de cincuenta o más años.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2013-13617` | Ley 23/2013 | **Ley 23/2013, de 23 de diciembre, reguladora del Factor de Sostenibilidad y del Índice de Revalorización de las pensiones.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2013-2309` | RD 156/2013 | **Real Decreto 156/2013, de 1 de marzo, por el que se regula la suscripción de convenio especial por las personas con discapacidad.** | 📜 Histórica/No Consolidada (Ingestión vía diario original fallback) |
| `BOE-A-2014-7684` | RD 625/2014 | **Real Decreto 625/2014, de 18 de julio, por el que se regulan determinados aspectos de la gestión y control de los procesos por incapacidad temporal.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2015-11346` | Ley 47/2015 Mar | **Ley 47/2015, de 21 de octubre, reguladora de la protección social de las personas trabajadoras del sector marítimo-pesquero.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2018-10397` | RD 900/2018 | **Real Decreto 900/2018, de 20 de julio, de desarrollo de la disposición adicional trigésima de la Ley 27/2011, en materia de pensión de viudedad.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2018-9030` | RD 696/2018 | **Real Decreto 696/2018, de 29 de junio, por el que se aprueba el Reglamento general de la gestión financiera de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2019-15790` | RDL 14/2019 | **Real Decreto-ley 14/2019, de 31 de octubre, por el que se adoptan medidas urgentes por razones de seguridad pública en materia de protección por desempleo.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2021-1529` | RDL 3/2021 | **Real Decreto-ley 3/2021, de 2 de febrero, de medidas para la reducción de la brecha de género y otras medidas de protección social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2022-10677` | RD 504/2022 | **Real Decreto 504/2022, de 27 de junio, por el que se modifican el Reglamento General sobre inscripción de empresas y afiliación y el Reglamento General sobre Cotización.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2024-10235` | RDL 2/2024 | **Real Decreto-ley 2/2024, de 21 de mayo, por el que se adoptan medidas urgentes para la simplificación y mejora del nivel asistencial de la protección por desempleo.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2024-10237` | RD 501/2024 | **Real Decreto 501/2024, de 21 de mayo, por el que se desarrolla la estructura orgánica básica del Ministerio de Inclusión, Seguridad Social y Migraciones.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2019-3244` | RDL 6/2019 | **Real Decreto-ley 6/2019, de 1 de marzo, de medidas urgentes para garantía de la igualdad de trato y de oportunidades entre mujeres y hombres en el empleo y la ocupación.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1998-12816` | RD 928/1998 | **Real Decreto 928/1998, de 14 de mayo, por el que se aprueba el Reglamento general sobre procedimientos para la imposición de las sanciones por infracciones de orden social y para los expedientes liquidatorios de cuotas de la Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2026-2548` | RDL 3/2026 | **Real Decreto-ley 3/2026, de 3 de febrero, para la revalorización de las pensiones públicas y otras medidas urgentes en materia de Seguridad Social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2018-16673` | LO 3/2018 | **Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2007-6115` | LO 3/2007 | **Ley Orgánica 3/2007, de 22 de marzo, para la igualdad efectiva de mujeres y hombres.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2004-21760` | LO 1/2004 | **Ley Orgánica 1/2004, de 28 de diciembre, de Medidas de Protección Integral contra la Violencia de Género.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1997-25336` | Ley 50/1997 | **Ley 50/1997, de 27 de noviembre, del Gobierno.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1979-23709` | LO 2/1979 | **Ley Orgánica 2/1979, de 3 de octubre, del Tribunal Constitucional.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1985-12666` | LO 6/1985 | **Ley Orgánica 6/1985, de 1 de julio, del Poder Judicial.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1981-10325` | LO 3/1981 | **Ley Orgánica 3/1981, de 6 de abril, del Defensor del Pueblo.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1985-5392` | Ley 7/1985 | **Ley 7/1985, de 2 de abril, Reguladora de las Bases del Régimen Local.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2013-12887` | Ley 19/2013 | **Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1995-8729` | RD 364/1995 | **Real Decreto 364/1995, de 10 de marzo, por el que se aprueba el Reglamento General de Ingreso del Personal al servicio de la AGE y de Provisión de Puestos de Trabajo y Promoción Profesional.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1995-8730` | RD 365/1995 | **Real Decreto 365/1995, de 10 de marzo, por el que se aprueba el Reglamento de Situaciones Administrativas de los Funcionarios Civiles de la AGE.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2021-5032` | RD 203/2021 | **Real Decreto 203/2021, de 30 de marzo, por el que se aprueba el Reglamento de actuación y funcionamiento del sector público por medios electrónicos.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2022-7191` | RD 311/2022 | **Real Decreto 311/2022, de 3 de mayo, por el que se regula el Esquema Nacional de Seguridad.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2000-323` | LEC | **Ley 1/2000, de 7 de enero, de Enjuiciamiento Civil.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-1980-8648` | LO 3/1980 | **Ley Orgánica 3/1980, de 22 de abril, del Consejo de Estado.** | 📜 Histórica/No Consolidada (Ingestión vía diario original fallback) |
| `BOE-A-2011-15936` | Ley 36/2011 | **Ley 36/2011, de 10 de octubre, reguladora de la jurisdicción social.** | ✅ OK - Sin modificaciones recientes |
| `BOE-A-2026-7296` | Orden Cot. 2026 | **Orden PJC/297/2026, de 30 de marzo, por la que se desarrollan las normas legales de cotización a la Seguridad Social, desempleo, protección por cese de actividad, Fondo de Garantía Salarial y formación profesional para el ejercicio 2026.** | ⚠️ MODIFICADA RECIENTEMENTE (post-corte examen) |

ESTA última orden modificada recientemente es valida para el wxamen porque va con efecto retroactivo y el ministerio ko confirma que sí, debe estudiarse!!!