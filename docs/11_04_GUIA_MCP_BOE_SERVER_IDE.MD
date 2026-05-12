 Guía Completa MCP-BOE
📁 Directorio de Instalación
El servidor MCP-BOE está instalado en las siguientes rutas:

Ruta	Descripción
/home/spas/.local/share/uv/tools/mcp-boe/	Raíz de la instalación (entorno virtual uv)
/home/spas/.local/share/uv/tools/mcp-boe/lib/python3.12/site-packages/mcp_boe/	Código fuente del servidor
/home/spas/.local/bin/mcp-boe	Ejecutable
Archivos clave del código fuente
mcp_boe/
├── server.py              # Servidor MCP principal (dispatcher de herramientas)
├── __init__.py
├── models/
│   └── boe_models.py      # Modelos de datos + APIError ← PARCHEADO ✅
├── tools/
│   ├── legislation.py     # Búsqueda/lectura de leyes ← PARCHEADO ✅
│   ├── summaries.py       # Sumarios diarios BOE/BORME
│   └── auxiliary.py       # Tablas auxiliares (departamentos, rangos, etc.)
└── utils/
    └── http_client.py     # Cliente HTTP asíncrono
🌐 API Oficial del BOE — Referencia Completa
Base URL: https://www.boe.es/datosabiertos/api

1️⃣ Legislación Consolidada
Búsqueda
GET /legislacion-consolidada?query=<JSON>&limit=20&offset=0
Parámetros de query (JSON serializado):

json
{
  "query": {
    "query_string": {
      "query": "(titulo:(Seguridad Social) OR texto:(Seguridad Social)) AND departamento@codigo:7723"
    },
    "range": {
      "fecha_publicacion": { "gte": "20150101", "lte": "20251231" }
    }
  }
}
Respuesta:

json
{
  "status": { "code": "200", "text": "ok" },
  "data": [
    {
      "identificador": "BOE-A-2015-10566",
      "titulo": "Ley 39/2015, de 1 de octubre...",
      "fecha_publicacion": "20151002",
      "departamento": { "codigo": "7723", "texto": "Jefatura del Estado" },
      "rango": { "codigo": "1300", "texto": "Ley" },
      "estatus_derogacion": "N",
      "vigencia_agotada": "N",
      "estado_consolidacion": { "texto": "Finalizado" },
      "url_html_consolidada": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-10566"
    }
  ]
}
Obtener norma por ID
Todos los endpoints siguen el patrón:

GET /legislacion-consolidada/id/{BOE-A-YYYY-NNNNN}/{seccion}
Endpoint	Qué devuelve
.../metadatos	Metadatos completos (fechas, departamento, estado)
.../analisis	Referencias cruzadas (normas que modifica/deroga)
.../metadatos-eli	Metadatos ELI (European Legislation Identifier)
.../texto/indice	Índice de bloques (estructura de la norma)
.../texto/bloque/{id}	Texto de un artículo/disposición específica
2️⃣ Estructura del Texto (Índice) — Respuesta Detallada
GET /legislacion-consolidada/id/BOE-A-2015-10566/texto/indice
json
{
  "status": { "code": "200", "text": "ok" },
  "data": [
    {
      "bloque": [
        {
          "id": "preambulo",
          "titulo": "",
          "fecha_actualizacion": "20151002",
          "url": "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2015-10566/texto/bloque/preambulo"
        },
        {
          "id": "a1",
          "titulo": "Artículo 1",
          "fecha_actualizacion": "20151002",
          "url": "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2015-10566/texto/bloque/a1"
        },
        {
          "id": "da1",
          "titulo": "Disposición adicional primera",
          "fecha_actualizacion": "20220101",
          "url": "..."
        },
        {
          "id": "dt1",
          "titulo": "Disposición transitoria primera",
          "fecha_actualizacion": "20200101",
          "url": "..."
        },
        {
          "id": "dd",
          "titulo": "Disposición derogatoria",
          "fecha_actualizacion": "20151002",
          "url": "..."
        },
        {
          "id": "df1",
          "titulo": "Disposición final primera",
          "fecha_actualizacion": "20151002",
          "url": "..."
        }
      ]
    }
  ]
}
IMPORTANT

data es una lista con un solo elemento (data[0]), y dentro está la clave bloque. Este es el bug que estaba causando el error y ya está corregido.

3️⃣ Texto de un Bloque Específico
GET /legislacion-consolidada/id/BOE-A-2015-10566/texto/bloque/a1
Accept: application/json
json
{
  "data": {
    "bloque": {
      "id": "a1",
      "titulo": "Artículo 1",
      "tipo": "precepto",
      "version": [
        {
          "fecha_publicacion": "20151002",
          "id_norma": "BOE-A-2015-10566",
          "contenido_html": "<p>El objeto de esta ley es...</p>"
        },
        {
          "fecha_publicacion": "20210101",
          "id_norma": "BOE-A-2020-12567",
          "contenido_html": "<p>Texto modificado por la ley X...</p>"
        }
      ]
    }
  }
}
TIP

El campo version es una lista en orden cronológico inverso: el primero es el texto vigente, los siguientes son las versiones históricas. Puedes ver el historial completo de modificaciones de cualquier artículo.

4️⃣ Análisis Jurídico — Referencias Cruzadas
GET /legislacion-consolidada/id/BOE-A-2015-10566/analisis
json
{
  "data": {
    "materias": [
      { "codigo": "2120", "texto": "Procedimiento administrativo" },
      { "codigo": "1090", "texto": "Administración pública" }
    ],
    "referencias": {
      "anteriores": [
        {
          "id_norma": "BOE-A-1992-26318",
          "relacion": { "codigo": "R", "texto": "DEROGA" },
          "texto": "art. 4.2 y 5 de la Ley 30/1992"
        }
      ],
      "posteriores": [
        {
          "id_norma": "BOE-A-2020-12572",
          "relacion": { "codigo": "M", "texto": "MODIFICA" },
          "texto": "Modifica art. 10, 11 y 12"
        }
      ]
    },
    "notas": [
      { "texto": "Texto consolidado actualizado a 01/01/2024" }
    ]
  }
}
5️⃣ Metadatos ELI (European Legislation Identifier)
GET /legislacion-consolidada/id/BOE-A-2015-10566/metadatos-eli
Accept: application/json
Sigue el estándar europeo para identificación única de legislación. Útil para integraciones con sistemas EU y bases de datos jurídicas supranacionales.

json
{
  "data": {
    "eli": "http://data.boe.es/eli/es/l/2015/10/01/39",
    "title": { "es": "Ley 39/2015..." },
    "date_publication": "2015-10-02",
    "type_document": "http://data.boe.es/eli/es/l",
    "passed_by": "Jefatura del Estado"
  }
}
6️⃣ Sumarios Diarios
GET /boe/sumario/{AAAAMMDD}
Accept: application/json
Estructura del sumario:

data.diarios[0].secciones[] → Secciones (I, II, III, IV, V)
.departamentos[] → Ministerios/organismos
.epigrafes[] → Subsecciones temáticas
.documentos[] → Documentos individuales (ID, título, url_pdf, url_html, url_xml)
TIP

Cada documento tiene url_pdf, url_html y url_xml. El XML es el más completo y estructurado para procesamiento automático.

🛠️ Cómo Usar las Herramientas MCP Mejor
Flujo de trabajo óptimo para una norma
1. search_consolidated_legislation(query="Ley 8/2015 Seguridad Social")
   → Obtener el ID: BOE-A-2015-XXXXX
2. get_consolidated_law(law_id="BOE-A-2015-XXXXX", include_analysis=true)
   → Ver metadatos + referencias cruzadas
3. get_law_structure(law_id="BOE-A-2015-XXXXX")
   → Ver índice completo de artículos y disposiciones
4. get_law_text_block(law_id="BOE-A-2015-XXXXX", block_id="a1")
   → Leer artículo específico con historial de versiones
5. find_related_laws(law_id="BOE-A-2015-XXXXX", relation_type="modified_by")
   → Ver qué normas posteriores lo han modificado
IDs de bloque más habituales
ID	Contenido
preambulo	Preámbulo/Exposición de motivos
co	Encabezamiento/Comienzo
a1, a2, ...	Artículos
t1, t2, ...	Títulos
c1, c2, ...	Capítulos
da1, da2, ...	Disposiciones adicionales
dt1, dt2, ...	Disposiciones transitorias
dd, dd1, ...	Disposiciones derogatorias
df1, df2, ...	Disposiciones finales
anexo1, ...	Anexos
🐛 Bugs Corregidos (resumen)
Bug	Estado	Fichero
APIError no hereda de Exception — no se podía capturar	✅ Corregido	models/boe_models.py
get_law_structure: data es list pero se trataba como dict	✅ Corregido	tools/legislation.py
 
 EXPLICASIONES ADICIONALES : 
 Cómo funciona la API del BOE — Todo el panorama
El MCP es solo un "traductor"
TÚ (o el agente)
    │
    ▼
MCP-BOE (herramienta)
    │  traduce tu petición a una llamada HTTP GET
    ▼
API REST del BOE (boe.es/datosabiertos/api)
    │  que es un Elasticsearch expuesto públicamente
    ▼
Datos de vuelta en JSON o XML
El MCP no tiene acceso especial. Solo usa los mismos endpoints públicos que cualquier persona puede usar con curl. No hay "búsqueda secreta" ni acceso al motor interno del BOE.

📅 El problema con los filtros de fecha: hay dos campos distintos
Aquí está la clave que probablemente te confundía:

Campo	Qué es	Cuándo cambia
fecha_publicacion	Fecha en que la norma salió en el BOE original	Nunca (es histórica)
fecha_actualizacion	Fecha de la última consolidación del texto	Cada vez que otra norma la modifica
El bug de duplicación en el MCP actual
El build_search_query envía las fechas DOS veces de forma contradictoria:

Como parámetros URL (?from=...&to=...) → filtran por fecha_actualizacion
Dentro del JSON Elasticsearch (range.fecha_publicacion) → filtran por fecha_publicacion
Esto puede hacer que los resultados sean raros o vacíos.

La solución (sin tocar nada hoy):
Para "normas publicadas en 2015" → el campo correcto es fecha_publicacion dentro del query JSON
Para "normas que se han consolidado recientemente" → los parámetros URL from/to (que = fecha_actualizacion)
Para "todo lo publicado en una fecha exacta" → lo más fiable es get_boe_summary(date='20150101') que devuelve exactamente los documentos de ese día
¿Se puede arreglar en el MCP?
Sí, perfectamente. Lo que habría que hacer es:

Eliminar que las fechas se dupliquen en el query JSON cuando ya van de parámetros URL
O exponer dos parámetros distintos: fecha_publicacion_desde y fecha_actualizacion_desde
Cuando quieras, lo implementamos — pero no hay urgencia si los sumarios diarios cubren el caso de uso.

📁 El grafo de memoria tiene toda esta info guardada para futuras sesiones.

El sistema jurídico español: como una carpeta de apuntes
Paso 1: La ley original (el "borrador"]
Imagina que en 1994 el Gobierno publica la Ley General de la Seguridad Social. Sale en el BOE ese día. Ese es el texto original.

Paso 2: Los retoques (modificaciones)
Con los años, otras leyes van cambiando artículos de esa ley. Por ejemplo:

En 2007 → cambian el artículo 161 (jubilación)
En 2011 → cambian el artículo 163 (cálculo pensión)
En 2021 → cambian el artículo 209 (desempleo)
¿Pero el texto del BOE original de 1994 lo cambian? No. Ese papel queda tal cual.

Lo que hay son varios boletines distintos con los retoques, dispersos en años.

Paso 3: El texto "Consolidado" — el trabajo editorial del BOE
Los técnicos del BOE hacen un trabajo editorial: cogen la ley original y van cosiendo manualmente todos los retoques en un único documento limpio y legible. A eso se llama texto consolidado.

LGSS 1994 (original)     →  Texto consolidado 2026
  + Retoque 2007              = Un solo PDF limpio donde
  + Retoque 2011                el artículo 161 ya aparece
  + Retoque 2021                con la redacción de 2021
  + Retoque 2026
El texto consolidado NO es una ley nueva. Es una edición editorial de servicio público.

📰 ¿Qué aparece en el Sumario diario del BOE?
El sumario del día solo muestra lo que se publica/modifica ESE DÍA:

Una ley nueva
Un decreto que modifica X artículos de una ley existente
Una resolución, un nombramientos, etc.
Sumario 03/04/2026 contiene:
  - Ley nueva A
  - Real Decreto que modifica arts. 5 y 6 de la LGSS
  - Resolución administrativa sobre pensiones
La LGSS en sí (1000 artículos) NO aparece en el sumario ese día. Solo aparece el decreto que la modifica.

🚨 Tu problema real: la API siempre da el texto ACTUAL
Aquí está la clave que te preocupa, y tienes razón en preocuparte:

Hoy (11/04/2026)
   │
   ▼
GET /legislacion-consolidada/id/BOE-A-2015-11724  ← LGSS
   │
   ▼
Texto consolidado con TODOS los cambios hasta hoy
   ^
   │
Incluye cambios del 05/04/2026, 08/04/2026... ← PROBLEMA
(después de tu fecha de corte 03/04/2026)
La API del BOE no tiene una "wayback machine". No puedes decirle "dame la LGSS tal como estaba el 03/04/2026". Solo da la versión más actual.

✅ Pero hay una salida: el historial de versiones por artículo
Cuando pides un artículo concreto con get_law_text_block, la API te devuelve todas las versiones que ha tenido ese artículo con sus fechas:

json
{
  "version": [
    {
      "fecha_publicacion": "20260405",   ← DESPUÉS de tu corte ❌
      "id_norma": "BOE-A-2026-XXXX",
      "contenido_html": "...texto nuevo..."
    },
    {
      "fecha_publicacion": "20210101",   ← ANTES de tu corte ✅
      "id_norma": "BOE-A-2020-YYYY",
      "contenido_html": "...texto válido para tu examen..."
    }
  ]
}
La lista está en orden cronológico inverso (la más nueva primero). Esto significa que:

Para tu examen, el texto válido de cada artículo es la primera versión cuya fecha_publicacion sea ≤ 03/04/2026.

🎯 Resumen de tu situación
Situación	Qué hacer
Quieres saber si una ley existía antes del 03/04	Mira fecha_publicacion en metadatos — si es < 20260403 ✅
Quieres el texto correcto de un artículo	Pide get_law_text_block y usa la versión donde fecha_publicacion ≤ 20260403
Quieres saber qué se publicó el 03/04	get_boe_summary(date='20260403')
Quieres saber qué modificó una ley antigua	find_related_laws + filtrar por fecha de la norma modificadora
💡 Lo que podría mejorar el MCP (cuando quieras)
Podríamos añadir un parámetro as_of_date a get_law_text_block que:

Pida todos los bloques de la norma
Para cada bloque, use automáticamente la versión con fecha_publicacion ≤ as_of_date
Eso sería el equivalente a "dame la LGSS tal como estaba el 03/04/2026". Es técnicamente factible con la API actual porque el historial está ahí. 