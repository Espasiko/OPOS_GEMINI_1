**APÉNDICE IX**

**OpositAIA --- Arquitectura Técnica Definitiva**

*Neo4j Fractal desde BOE XML · Docker VPS Completo · Códigos
Electrónicos BOE · Plan V4 Integrado · Evaluación PRD BMAD*

+-----------------+-----------------+-----------------+-----------------+
| **Neo4j         | **Docker        | **Códigos BOE** | **Plan V4 +     |
| Fractal**       | Stack**         |                 | PRD**           |
|                 |                 | 435 · 442 · API |                 |
| 6 capas · BOE   | VPS +           |                 | BMAD · Todo     |
| API             | Cloudflare      |                 | integrado       |
+-----------------+-----------------+-----------------+-----------------+

**1. Neo4j Fractal desde la API BOE --- Arquitectura Completa**

**1.1 Lo que nos da la API del BOE (confirmado)**

+-----------------------------------------------------------------------+
| **La API del BOE tiene exactamente lo que necesitamos para un grafo   |
| legal vivo**                                                          |
|                                                                       |
| La Agencia Estatal BOE ofrece una API REST libre sin autenticación    |
| (solo HTTPS GET). El endpoint clave es /análisis que incluye:         |
| REFERENCIAS ANTERIORES (qué leyes previas afecta esta norma, con      |
| texto exacto del efecto) y REFERENCIAS POSTERIORES (qué normas        |
| posteriores la han modificado, con texto como \'SE AÑADE la           |
| disposición adicional 8, por Real Decreto-ley 18/2022\'). Además, el  |
| endpoint /texto descompone cada ley en \<bloque\> con historial de    |
| versiones por fecha de modificación. Esto es un grafo de relaciones   |
| legales ya construido --- solo hay que importarlo a Neo4j.            |
+-----------------------------------------------------------------------+

  ---------------------------------------------------------------------------------------------
  **Endpoint BOE API**                **Qué contiene**             **Para qué sirve en Neo4j**
  ----------------------------------- ---------------------------- ----------------------------
  GET /legislacion-consolidada        Lista todas las normas       Crear los nodos :Ley con
                                      consolidadas con metadatos   propiedades de metadato.
                                      básicos (fecha, rango,       Detectar cambios via
                                      título, vigencia, estado)    fecha_actualizacion.

  GET                                 Norma completa: metadatos +  Bootstrap inicial: todo de
  /legislacion-consolidada/id/{id}    análisis + texto completo de una ley en una llamada
                                      todas las versiones          

  **GET /id/{id}/análisis**           **⭐ El endpoint estrella:   **Crear relaciones
                                      materias, notas, referencias \[:MODIFICA\], \[:DEROGA\],
                                      anteriores Y posteriores con \[:COMPLEMENTA\] entre nodos
                                      texto de la modificación**   :Ley --- el grafo de
                                                                   relaciones**

  GET /id/{id}/texto                  Texto completo estructurado  Crear nodos
                                      en \<bloque\> con tipo       :Bloque/:Articulo y sus
                                      (artículo/título/capítulo) y nodos :Version con fecha de
                                      todas las versiones          cada modificación
                                      históricas                   

  GET /id/{id}/texto/índice           Índice de todos los bloques  Obtener IDs de artículos
                                      de la norma con sus IDs      para llamadas individuales
                                                                   (batch más eficiente)

  GET                                 Todas las versiones de un    Nodo :Articulo con
  /id/{id}/texto/bloque/{id_bloque}   artículo concreto a lo largo relaciones
                                      del tiempo                   \[:TIENE_VERSION\] ordenadas
                                                                   cronológicamente ---
                                                                   historial de cambios

  GET /boe/sumario/{fecha}            Sumario diario del BOE con   Cron diario: detectar si
                                      todas las disposiciones      alguna norma del grafo fue
                                                                   modificada ese día →
                                                                   re-indexar automáticamente
  ---------------------------------------------------------------------------------------------

**1.2 Esquema Neo4j --- 6 Capas Fractales**

+-----------------------------------------------------------------------+
| **La búsqueda fractal significa que puedes entrar por cualquier capa  |
| y navegar en todas direcciones**                                      |
|                                                                       |
| Desde un nodo :Pregunta puedes ir hacia arriba al :Articulo que       |
| evalúa, de ahí a la :Ley que contiene ese artículo, de ahí a las      |
| :Leyes que la modifican o derogan, y también hacia abajo a los        |
| :Concepto y :Calculadora relacionados. Desde una :Ley puedes          |
| descender a todos sus :Articulo, y desde un :Articulo ver todas sus   |
| :Version históricas. Cada nodo tiene un embedding vectorial en Qdrant |
| apuntado desde Neo4j para combinar búsqueda semántica con navegación  |
| estructural.                                                          |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| // === SCHEMA NEO4J FRACTAL --- OPOSITAIA ===                         |
|                                                                       |
| // Capa 0: Cuerpo de oposición                                        |
|                                                                       |
| CREATE CONSTRAINT ON (c:Cuerpo) ASSERT c.id IS UNIQUE;                |
|                                                                       |
| // Capa 1: Ley (nodo raíz del grafo legal)                            |
|                                                                       |
| CREATE CONSTRAINT ON (l:Ley) ASSERT l.boe_id IS UNIQUE;               |
|                                                                       |
| // Capa 2: Bloque/Artículo (subdivisión de ley)                       |
|                                                                       |
| CREATE CONSTRAINT ON (b:Bloque) ASSERT b.bloque_id IS UNIQUE;         |
|                                                                       |
| // Capa 3: Versión de artículo (historial de cambios)                 |
|                                                                       |
| CREATE CONSTRAINT ON (v:Version) ASSERT v.version_id IS UNIQUE;       |
|                                                                       |
| // Capa 4: Concepto pedagógico (abstracción del artículo)             |
|                                                                       |
| CREATE CONSTRAINT ON (c:Concepto) ASSERT c.id IS UNIQUE;              |
|                                                                       |
| // Capa 5: Pregunta (ítem COSMIC del banco de preguntas)              |
|                                                                       |
| CREATE CONSTRAINT ON (p:Pregunta) ASSERT p.id IS UNIQUE;              |
|                                                                       |
| // === ÍNDICES PARA RENDIMIENTO ===                                   |
|                                                                       |
| CREATE INDEX ley_titulo FOR (l:Ley) ON (l.titulo);                    |
|                                                                       |
| CREATE INDEX ley_vigencia FOR (l:Ley) ON (l.vigencia_agotada);        |
|                                                                       |
| CREATE INDEX bloque_tipo FOR (b:Bloque) ON (b.tipo);                  |
|                                                                       |
| CREATE INDEX version_fecha FOR (v:Version) ON (v.fecha_publicacion);  |
|                                                                       |
| CREATE INDEX pregunta_dificultad FOR (p:Pregunta) ON (p.dificultad);  |
|                                                                       |
| CREATE INDEX pregunta_cuerpo FOR (p:Pregunta) ON (p.cuerpos);         |
|                                                                       |
| // === TIPOS DE NODOS ===                                             |
|                                                                       |
| // CAPA 0 --- Cuerpo de oposición                                     |
|                                                                       |
| (:Cuerpo {                                                            |
|                                                                       |
| id: \'c1_ss\', // c2_age \| c1_age \| c1_ss \| a2_ss                  |
|                                                                       |
| nombre: \'C1 Administrativo Seguridad Social\',                       |
|                                                                       |
| nivel: \'C1\',                                                        |
|                                                                       |
| organismo: \'Seguridad Social\',                                      |
|                                                                       |
| num_temas: 36,                                                        |
|                                                                       |
| num_temas_especificos: 13                                             |
|                                                                       |
| })                                                                    |
|                                                                       |
| // CAPA 1 --- Ley (desde /legislacion-consolidada/id/{id})            |
|                                                                       |
| (:Ley {                                                               |
|                                                                       |
| boe_id: \'BOE-A-2015-11724\',                                         |
|                                                                       |
| titulo: \'RDL 8/2015 Texto Refundido Ley General SS\',                |
|                                                                       |
| numero_oficial: \'8/2015\',                                           |
|                                                                       |
| rango: \'Real Decreto Legislativo\',                                  |
|                                                                       |
| rango_codigo: 1350,                                                   |
|                                                                       |
| fecha_disposicion: \'20151030\',                                      |
|                                                                       |
| fecha_publicacion: \'20151031\',                                      |
|                                                                       |
| fecha_vigencia: \'20160202\',                                         |
|                                                                       |
| vigencia_agotada: \'N\', // \'S\' = derogada completamente            |
|                                                                       |
| estado_consolidacion: \'Finalizado\', // o \'En proceso\'             |
|                                                                       |
| url_eli: \'https://www.boe.es/eli/es/rdlg/2015/10/30/8\',             |
|                                                                       |
| url_html: \'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724\',  |
|                                                                       |
| departamento: \'Ministerio de Empleo y Seguridad Social\',            |
|                                                                       |
| materias: \[\'seguridad social\', \'pensiones\', \'prestaciones\'\],  |
|                                                                       |
| ultima_actualizacion: \'20260215T103000Z\',                           |
|                                                                       |
| qdrant_collection: \'opositaia_knowledge_v2\', // para buscar chunks  |
|                                                                       |
| qdrant_filter_key: \'boe_id\'                                         |
|                                                                       |
| })                                                                    |
|                                                                       |
| // CAPA 2 --- Bloque/Artículo (desde /texto/índice + /texto)          |
|                                                                       |
| (:Bloque {                                                            |
|                                                                       |
| bloque_id: \'BOE-A-2015-11724_a169\', // boe_id + \'\_\' +            |
| bloque_id_boe                                                         |
|                                                                       |
| tipo: \'articulo\', // titulo \| capitulo \| seccion \| articulo \|   |
| disposicion                                                           |
|                                                                       |
| numero: \'169\',                                                      |
|                                                                       |
| titulo: \'Artículo 169. Concepto de incapacidad temporal\',           |
|                                                                       |
| texto_vigente: \'Se encontrarán en situación de incapacidad           |
| temporal\...\',                                                       |
|                                                                       |
| num_versiones: 3, // cuántas veces ha sido modificado                 |
|                                                                       |
| fecha_primera_version: \'20151031\',                                  |
|                                                                       |
| fecha_ultima_version: \'20240315\',                                   |
|                                                                       |
| vigente: true,                                                        |
|                                                                       |
| qdrant_chunk_ids: \[\'uuid-1\', \'uuid-2\'\] // chunks en Qdrant      |
|                                                                       |
| })                                                                    |
|                                                                       |
| // CAPA 3 --- Versión histórica de artículo (desde                    |
| /texto/bloque/{id})                                                   |
|                                                                       |
| (:Version {                                                           |
|                                                                       |
| version_id: \'BOE-A-2015-11724_a169_v2\',                             |
|                                                                       |
| texto: \'Se encontrarán en situación de IT los trabajadores\...\',    |
|                                                                       |
| fecha_publicacion: \'20210901\',                                      |
|                                                                       |
| norma_modificadora_boe_id: \'BOE-A-2021-14700\',                      |
|                                                                       |
| norma_modificadora_titulo: \'Ley 4/2021 de medidas urgentes SS\',     |
|                                                                       |
| texto_modificacion: \'SE MODIFICA el apartado 1.b) del artículo 169\' |
|                                                                       |
| })                                                                    |
|                                                                       |
| // CAPA 4 --- Concepto pedagógico                                     |
|                                                                       |
| (:Concepto {                                                          |
|                                                                       |
| id: \'it_cc_definicion\',                                             |
|                                                                       |
| titulo: \'IT por Contingencias Comunes --- Definición y Requisitos\', |
|                                                                       |
| descripcion: \'Situación protegida cuando el trabajador está          |
| impedido\...\',                                                       |
|                                                                       |
| cuerpos: \[\'c1_ss\', \'a2_ss\'\],                                    |
|                                                                       |
| bloque_tema: \'ss_prestaciones\',                                     |
|                                                                       |
| tema_num: 8,                                                          |
|                                                                       |
| dificultad_media: 2,                                                  |
|                                                                       |
| es_trampa_frecuente: true,                                            |
|                                                                       |
| tipo_trampa: \'dias_carencia\', // Los días 1-3 son a cargo del       |
| empresario                                                            |
|                                                                       |
| num_preguntas_relacionadas: 47,                                       |
|                                                                       |
| calidad_score: 0.94                                                   |
|                                                                       |
| })                                                                    |
|                                                                       |
| // CAPA 5 --- Pregunta COSMIC                                         |
|                                                                       |
| (:Pregunta {                                                          |
|                                                                       |
| id: \'preg-uuid-v4\',                                                 |
|                                                                       |
| texto: \'¿Cuál es el porcentaje de la base reguladora en los días 4   |
| al 20 de IT?\',                                                       |
|                                                                       |
| opciones: \[\'50%\', \'60%\', \'75%\', \'100%\'\],                    |
|                                                                       |
| respuesta_correcta: 1, // índice 0-based → \'60%\'                    |
|                                                                       |
| explicacion: \'Arts. 169-170 TRLGSS: días 4-20 → 60% BR a cargo       |
| mutua\...\',                                                          |
|                                                                       |
| articulo_principal: \'Art. 170 TRLGSS\',                              |
|                                                                       |
| cuerpos: \[\'c1_ss\', \'a2_ss\'\],                                    |
|                                                                       |
| dificultad: 2,                                                        |
|                                                                       |
| tipo_trampa: \'porcentaje_exacto\',                                   |
|                                                                       |
| calidad_score: 0.97,                                                  |
|                                                                       |
| verificado_por: \'claude-sonnet-4-6\',                                |
|                                                                       |
| fecha_verificacion: \'20260228\',                                     |
|                                                                       |
| generado_por: \'deepseek-v3\',                                        |
|                                                                       |
| formato_origen: \'pregunta_test\',                                    |
|                                                                       |
| veces_respondida: 0,                                                  |
|                                                                       |
| tasa_acierto: null                                                    |
|                                                                       |
| })                                                                    |
|                                                                       |
| // === TIPOS DE RELACIONES ===                                        |
|                                                                       |
| // Capa 0 → 1: qué cuerpos estudian esta ley                          |
|                                                                       |
| (:Cuerpo)-\[:ESTUDIA {temas_relacionados: \[8,9\], peso_examen:       |
| \'ALTO\'}\]-\>(:Ley)                                                  |
|                                                                       |
| // Capa 1 → 2: ley tiene artículos                                    |
|                                                                       |
| (:Ley)-\[:CONTIENE {orden: 169}\]-\>(:Bloque)                         |
|                                                                       |
| // Capa 2 → 3: artículo tiene versiones históricas                    |
|                                                                       |
| (:Bloque)-\[:TIENE_VERSION {version_num: 2}\]-\>(:Version)            |
|                                                                       |
| // Capa 1 → 1: relaciones entre leyes (desde /análisis)               |
|                                                                       |
| (:Ley)-\[:MODIFICA {                                                  |
|                                                                       |
| texto_efecto: \'SE AÑADE la disposición adicional 8\',                |
|                                                                       |
| fecha: \'20221018\',                                                  |
|                                                                       |
| norma_modificadora: \'BOE-A-2022-17040\'                              |
|                                                                       |
| }\]-\>(:Ley)                                                          |
|                                                                       |
| (:Ley)-\[:DEROGA {parcial: true, articulos_derogados:                 |
| \[\'169\',\'170\'\]}\]-\>(:Ley)                                       |
|                                                                       |
| (:Ley)-\[:DESARROLLA\]-\>(:Ley) // reglamento desarrolla ley          |
|                                                                       |
| (:Ley)-\[:COMPLEMENTA\]-\>(:Ley)                                      |
|                                                                       |
| (:Ley)-\[:SE_BASA_EN\]-\>(:Ley) // referencias anteriores             |
|                                                                       |
| // Capa 2 → 2: artículo referencia a otro artículo                    |
|                                                                       |
| (:Bloque)-\[:REFERENCIA_A {texto: \'véase también Art.                |
| 174\'}\]-\>(:Bloque)                                                  |
|                                                                       |
| (:Bloque)-\[:PADRE\]-\>(:Bloque) // artículo pertenece a capítulo     |
|                                                                       |
| // Capa 2 → 4: artículo explica concepto                              |
|                                                                       |
| (:Bloque)-\[:EXPLICA {es_fuente_primaria: true}\]-\>(:Concepto)       |
|                                                                       |
| // Capa 4 → 5: concepto genera preguntas                              |
|                                                                       |
| (:Concepto)-\[:TIENE_PREGUNTA {dificultad: 2}\]-\>(:Pregunta)         |
|                                                                       |
| // Capa 5 → 2: pregunta se basa en artículo                           |
|                                                                       |
| (:Pregunta)-\[:BASADA_EN {es_trampa: true}\]-\>(:Bloque)              |
|                                                                       |
| // Calculadora: nodo especial conectado a concepto                    |
|                                                                       |
| (:Calculadora {                                                       |
|                                                                       |
| id: \'calcular_cuantia_it\',                                          |
|                                                                       |
| modulo: \'calculos_ss_extended\',                                     |
|                                                                       |
| descripcion: \'Calcula cuantía diaria IT según días transcurridos\',  |
|                                                                       |
| precision: \'Decimal\'                                                |
|                                                                       |
| })-\[:CALCULA\]-\>(:Concepto)                                         |
+-----------------------------------------------------------------------+

**1.3 Código Python --- Importar la API BOE a Neo4j**

+-----------------------------------------------------------------------+
| \# boe_neo4j_importer.py                                              |
|                                                                       |
| \# Importa leyes completas desde la API BOE a Neo4j                   |
|                                                                       |
| \# Incluye: metadatos, artículos por bloque, versiones históricas,    |
| relaciones del análisis                                               |
|                                                                       |
| import asyncio, aiohttp, time                                         |
|                                                                       |
| from datetime import datetime                                         |
|                                                                       |
| from xml.etree import ElementTree as ET                               |
|                                                                       |
| from neo4j import AsyncGraphDatabase                                  |
|                                                                       |
| BOE_API_BASE = \'https://www.boe.es/datosabiertos/api\'               |
|                                                                       |
| NEO4J_URI = \'bolt://localhost:7687\'                                 |
|                                                                       |
| NEO4J_USER = \'neo4j\'                                                |
|                                                                       |
| NEO4J_PASS = \'your_password_here\'                                   |
|                                                                       |
| \# Tipos de relación del endpoint /análisis del BOE                   |
|                                                                       |
| \# Fuente: tablas auxiliares API en                                   |
| boe.es/datosabiertos/faq/datos-auxiliares.php                         |
|                                                                       |
| TIPO_REL_MAP = {                                                      |
|                                                                       |
| \'Modifica\': \'MODIFICA\',                                           |
|                                                                       |
| \'Deroga\': \'DEROGA\',                                               |
|                                                                       |
| \'Añade\': \'ANIADE_A\',                                              |
|                                                                       |
| \'Completa\': \'COMPLEMENTA\',                                        |
|                                                                       |
| \'Desarrolla\': \'DESARROLLA\',                                       |
|                                                                       |
| \'Ejecuta\': \'EJECUTA\',                                             |
|                                                                       |
| \'Se dicta en\': \'SE_DICTA_EN\',                                     |
|                                                                       |
| \'Corrige\': \'CORRIGE\',                                             |
|                                                                       |
| \'Suspende\': \'SUSPENDE\',                                           |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# ─── CAPA 1: Importar metadatos + análisis de la ley ───            |
|                                                                       |
| async def importar_ley(session, boe_id: str, cuerpos: list\[str\],    |
| temas: list\[int\]):                                                  |
|                                                                       |
| async with aiohttp.ClientSession() as http:                           |
|                                                                       |
| \# 1. Metadatos base                                                  |
|                                                                       |
| url_meta = f\'{BOE_API_BASE}/legislacion-consolidada/id/{boe_id}\'    |
|                                                                       |
| async with http.get(url_meta,                                         |
| headers={\'Accept\':\'application/json\'}) as r:                      |
|                                                                       |
| meta = await r.json()                                                 |
|                                                                       |
| ley = meta\[\'data\'\]                                                |
|                                                                       |
| \# Crear o actualizar nodo :Ley                                       |
|                                                                       |
| await session.run(\'\'\'                                              |
|                                                                       |
| MERGE (l:Ley {boe_id: \$boe_id})                                      |
|                                                                       |
| SET l.titulo = \$titulo,                                              |
|                                                                       |
| l.numero_oficial = \$num,                                             |
|                                                                       |
| l.rango = \$rango,                                                    |
|                                                                       |
| l.fecha_disposicion = \$f_disp,                                       |
|                                                                       |
| l.fecha_publicacion = \$f_pub,                                        |
|                                                                       |
| l.vigencia_agotada = \$vigencia,                                      |
|                                                                       |
| l.estado_consolidacion = \$estado,                                    |
|                                                                       |
| l.url_eli = \$eli,                                                    |
|                                                                       |
| l.url_html = \$html,                                                  |
|                                                                       |
| l.ultima_actualizacion = \$upd,                                       |
|                                                                       |
| l.cuerpos = \$cuerpos,                                                |
|                                                                       |
| l.temas = \$temas                                                     |
|                                                                       |
| \'\'\', boe_id=boe_id, titulo=ley\[\'titulo\'\],                      |
|                                                                       |
| num=ley.get(\'numero_oficial\',\'\'),                                 |
| rango=ley\[\'rango\'\]\[\'texto\'\],                                  |
|                                                                       |
| f_disp=ley.get(\'fecha_disposicion\',\'\'),                           |
| f_pub=ley\[\'fecha_publicacion\'\],                                   |
|                                                                       |
| vigencia=ley\[\'vigencia_agotada\'\],                                 |
| estado=ley\[\'estado_consolidacion\'\]\[\'texto\'\],                  |
|                                                                       |
| eli=ley.get(\'url_eli\',\'\'), html=ley\[\'url_html_consolidada\'\],  |
|                                                                       |
| upd=ley\[\'fecha_actualizacion\'\], cuerpos=cuerpos, temas=temas)     |
|                                                                       |
| print(f\'✅ Ley: {boe_id}\')                                          |
|                                                                       |
| \# ─── CAPA 1→1: Importar relaciones del /análisis ───                |
|                                                                       |
| async def importar_relaciones(session, boe_id: str):                  |
|                                                                       |
| async with aiohttp.ClientSession() as http:                           |
|                                                                       |
| url =                                                                 |
| f\'{BOE_API_BASE}/legislacion-consolidada/id/{boe_id}/análisis\'      |
|                                                                       |
| async with http.get(url, headers={\'Accept\':\'application/xml\'}) as |
| r:                                                                    |
|                                                                       |
| xml_text = await r.text()                                             |
|                                                                       |
| root = ET.fromstring(xml_text)                                        |
|                                                                       |
| referencias = root.find(\'.//referencias\')                           |
|                                                                       |
| if referencias is None:                                               |
|                                                                       |
| return                                                                |
|                                                                       |
| \# Procesar referencias posteriores: normas que MODIFICARON a esta    |
| ley                                                                   |
|                                                                       |
| for posterior in referencias.findall(\'.//posterior\'):               |
|                                                                       |
| norm_mod_id = posterior.findtext(\'id\', \'\').strip()                |
|                                                                       |
| texto_efecto = posterior.findtext(\'texto\', \'\').strip()            |
|                                                                       |
| tipo_rel_txt = posterior.findtext(\'tipo\', \'Modifica\').strip()     |
|                                                                       |
| tipo_rel = TIPO_REL_MAP.get(tipo_rel_txt, \'RELACIONADA_CON\')        |
|                                                                       |
| if norm_mod_id:                                                       |
|                                                                       |
| \# La norma modificadora modifica a nuestra ley base                  |
|                                                                       |
| await session.run(f\'\'\'                                             |
|                                                                       |
| MERGE (mod:Ley {{boe_id: \$mod_id}})                                  |
|                                                                       |
| MERGE (base:Ley {{boe_id: \$base_id}})                                |
|                                                                       |
| MERGE (mod)-\[r:{tipo_rel}\]-\>(base)                                 |
|                                                                       |
| SET r.texto_efecto = \$texto, r.fecha = \$fecha                       |
|                                                                       |
| \'\'\', mod_id=norm_mod_id, base_id=boe_id,                           |
|                                                                       |
| texto=texto_efecto, fecha=datetime.now().strftime(\'%Y%m%d\'))        |
|                                                                       |
| \# Procesar referencias anteriores: normas que ESTA ley modifica      |
|                                                                       |
| for anterior in referencias.findall(\'.//anterior\'):                 |
|                                                                       |
| norm_ant_id = anterior.findtext(\'id\', \'\').strip()                 |
|                                                                       |
| texto_efecto = anterior.findtext(\'texto\', \'\').strip()             |
|                                                                       |
| tipo_rel_txt = anterior.findtext(\'tipo\', \'Se basa en\').strip()    |
|                                                                       |
| tipo_rel = TIPO_REL_MAP.get(tipo_rel_txt, \'SE_BASA_EN\')             |
|                                                                       |
| if norm_ant_id:                                                       |
|                                                                       |
| await session.run(f\'\'\'                                             |
|                                                                       |
| MERGE (base:Ley {{boe_id: \$base_id}})                                |
|                                                                       |
| MERGE (ant:Ley {{boe_id: \$ant_id}})                                  |
|                                                                       |
| MERGE (base)-\[r:{tipo_rel}\]-\>(ant)                                 |
|                                                                       |
| SET r.texto_efecto = \$texto                                          |
|                                                                       |
| \'\'\', base_id=boe_id, ant_id=norm_ant_id, texto=texto_efecto)       |
|                                                                       |
| print(f\' 📎 Relaciones: {boe_id}\')                                  |
|                                                                       |
| \# ─── CAPA 2: Importar artículos (bloques) ───                       |
|                                                                       |
| async def importar_articulos(session, boe_id: str):                   |
|                                                                       |
| async with aiohttp.ClientSession() as http:                           |
|                                                                       |
| url_idx =                                                             |
| f\'{BOE_API_BASE}/legislacion-consolidada/id/{boe_id}/texto/índice\'  |
|                                                                       |
| async with http.get(url_idx,                                          |
| headers={\'Accept\':\'application/xml\'}) as r:                       |
|                                                                       |
| xml_idx = await r.text()                                              |
|                                                                       |
| root = ET.fromstring(xml_idx)                                         |
|                                                                       |
| bloques = root.findall(\'.//bloque\')                                 |
|                                                                       |
| print(f\' 📖 {len(bloques)} bloques en {boe_id}\')                    |
|                                                                       |
| for bloque in bloques:                                                |
|                                                                       |
| bloque_id = bloque.get(\'id\', \'\')                                  |
|                                                                       |
| tipo = bloque.get(\'tipo\', \'desconocido\')                          |
|                                                                       |
| titulo = bloque.get(\'titulo\', \'\')                                 |
|                                                                       |
| if not bloque_id:                                                     |
|                                                                       |
| continue                                                              |
|                                                                       |
| node_id = f\'{boe_id}\_{bloque_id}\'                                  |
|                                                                       |
| \# Crear nodo :Bloque y relacionarlo con :Ley                         |
|                                                                       |
| await session.run(\'\'\'                                              |
|                                                                       |
| MERGE (b:Bloque {bloque_id: \$node_id})                               |
|                                                                       |
| SET b.bloque_id_boe = \$bloque_id,                                    |
|                                                                       |
| b.tipo = \$tipo,                                                      |
|                                                                       |
| b.titulo = \$titulo,                                                  |
|                                                                       |
| b.ley_id = \$boe_id                                                   |
|                                                                       |
| WITH b                                                                |
|                                                                       |
| MATCH (l:Ley {boe_id: \$boe_id})                                      |
|                                                                       |
| MERGE (l)-\[:CONTIENE\]-\>(b)                                         |
|                                                                       |
| \'\'\', node_id=node_id, bloque_id=bloque_id, tipo=tipo,              |
|                                                                       |
| titulo=titulo, boe_id=boe_id)                                         |
|                                                                       |
| \# Solo importar versiones de artículos (no títulos/capítulos --- muy |
| grandes)                                                              |
|                                                                       |
| if tipo == \'articulo\':                                              |
|                                                                       |
| await importar_versiones_articulo(session, boe_id, bloque_id,         |
| node_id)                                                              |
|                                                                       |
| await asyncio.sleep(0.1) \# Rate limiting API BOE                     |
|                                                                       |
| \# ─── CAPA 3: Versiones históricas de cada artículo ───              |
|                                                                       |
| async def importar_versiones_articulo(session, boe_id: str,           |
| bloque_id: str, node_id: str):                                        |
|                                                                       |
| async with aiohttp.ClientSession() as http:                           |
|                                                                       |
| url =                                                                 |
| f\'{BOE_API                                                           |
| _BASE}/legislacion-consolidada/id/{boe_id}/texto/bloque/{bloque_id}\' |
|                                                                       |
| async with http.get(url, headers={\'Accept\':\'application/xml\'}) as |
| r:                                                                    |
|                                                                       |
| xml_txt = await r.text()                                              |
|                                                                       |
| root = ET.fromstring(xml_txt)                                         |
|                                                                       |
| versiones = root.findall(\'.//version\')                              |
|                                                                       |
| for i, version in enumerate(versiones):                               |
|                                                                       |
| fecha = version.get(\'fecha_publicacion\', \'\')                      |
|                                                                       |
| texto = \'\'.join(version.itertext()).strip()\[:2000\] \# truncar a   |
| 2000 chars                                                            |
|                                                                       |
| norma_mod = version.get(\'norma_modificadora_id\', \'\')              |
|                                                                       |
| texto_mod = version.get(\'texto_modificacion\', \'\')                 |
|                                                                       |
| ver_id = f\'{node_id}\_v{i}\'                                         |
|                                                                       |
| await session.run(\'\'\'                                              |
|                                                                       |
| MERGE (v:Version {version_id: \$ver_id})                              |
|                                                                       |
| SET v.texto = \$texto,                                                |
|                                                                       |
| v.fecha_publicacion = \$fecha,                                        |
|                                                                       |
| v.norma_modificadora = \$norma_mod,                                   |
|                                                                       |
| v.texto_modificacion = \$texto_mod,                                   |
|                                                                       |
| v.es_version_vigente = \$vigente                                      |
|                                                                       |
| WITH v                                                                |
|                                                                       |
| MATCH (b:Bloque {bloque_id: \$node_id})                               |
|                                                                       |
| MERGE (b)-\[:TIENE_VERSION {num: \$i}\]-\>(v)                         |
|                                                                       |
| \'\'\', ver_id=ver_id, texto=texto, fecha=fecha,                      |
|                                                                       |
| norma_mod=norma_mod, texto_mod=texto_mod,                             |
|                                                                       |
| vigente=(i==len(versiones)-1), node_id=node_id, i=i)                  |
|                                                                       |
| \# ─── CRON DIARIO: detectar cambios en el BOE ───                    |
|                                                                       |
| async def cron_detectar_cambios_boe(session, leyes_monitorizadas:     |
| list):                                                                |
|                                                                       |
| \'\'\'Ejecutar cada día. Detecta si el BOE modificó alguna ley del    |
| temario.\'\'\'                                                        |
|                                                                       |
| hoy = datetime.now().strftime(\'%Y%m%d\')                             |
|                                                                       |
| async with aiohttp.ClientSession() as http:                           |
|                                                                       |
| url =                                                                 |
| f\'                                                                   |
| {BOE_API_BASE}/legislacion-consolidada?from={hoy}&to={hoy}&limit=-1\' |
|                                                                       |
| async with http.get(url, headers={\'Accept\':\'application/json\'})   |
| as r:                                                                 |
|                                                                       |
| cambios = await r.json()                                              |
|                                                                       |
| for item in cambios.get(\'data\', \[\]):                              |
|                                                                       |
| boe_id = item\[\'identificador\'\]                                    |
|                                                                       |
| if boe_id in leyes_monitorizadas:                                     |
|                                                                       |
| print(f\'🚨 CAMBIO DETECTADO: {boe_id} --- {item\[\"titulo\"\]}\')    |
|                                                                       |
| \# Re-importar la ley actualizada                                     |
|                                                                       |
| await importar_relaciones(session, boe_id)                            |
|                                                                       |
| await importar_articulos(session, boe_id)                             |
|                                                                       |
| \# Notificar a usuarios suscritos vía Push API                        |
|                                                                       |
| \# await notificar_usuarios_afectados(boe_id, item\[\'titulo\'\])     |
|                                                                       |
| \# ─── MAIN: importar todas las leyes del temario ───                 |
|                                                                       |
| async def main():                                                     |
|                                                                       |
| driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER,       |
| NEO4J_PASS))                                                          |
|                                                                       |
| async with driver.session() as session:                               |
|                                                                       |
| \# Lista de leyes a importar con sus cuerpos y temas                  |
|                                                                       |
| leyes = \[                                                            |
|                                                                       |
| {\'id\':\'BOE-A-2015-11724\',\'cuerpos\':                             |
| \[\'c1_ss\',\'a2_ss\'\],\'temas\':\[1,2,3,4,5,6,7,8,9,10,11,12,13\]}, |
|                                                                       |
| {\'id\':\'BOE-A-2020-6133\',                                          |
| \'cuerpos\':\[\'c1_ss\',\'a2_ss\'\],\'temas\':\[12\]},                |
|                                                                       |
| {\'id\':\'BOE-A-2015-10565\',\'cuer                                   |
| pos\':\[\'c2\',\'c1_age\',\'c1_ss\',\'a2_ss\'\],\'temas\':\[1,2,3\]}, |
|                                                                       |
| {\'id\':\'BOE-A-2015-10566\',\'cuer                                   |
| pos\':\[\'c2\',\'c1_age\',\'c1_ss\',\'a2_ss\'\],\'temas\':\[1,2,3\]}, |
|                                                                       |
| {\'id\':\'BOE-A-2015-11719\',\'cuer                                   |
| pos\':\[\'c2\',\'c1_age\',\'c1_ss\',\'a2_ss\'\],\'temas\':\[4,5,6\]}, |
|                                                                       |
| {\'id\':\'BOE-A-1978-31229\',\'                                       |
| cuerpos\':\[\'c2\',\'c1_age\',\'c1_ss\',\'a2_ss\'\],\'temas\':\[1\]}, |
|                                                                       |
| \# \... añadir las 54 leyes del Apéndice VIII                         |
|                                                                       |
| \]                                                                    |
|                                                                       |
| for ley in leyes:                                                     |
|                                                                       |
| await importar_ley(session, ley\[\'id\'\], ley\[\'cuerpos\'\],        |
| ley\[\'temas\'\])                                                     |
|                                                                       |
| await importar_relaciones(session, ley\[\'id\'\])                     |
|                                                                       |
| await importar_articulos(session, ley\[\'id\'\])                      |
|                                                                       |
| await asyncio.sleep(0.5) \# Rate limiting                             |
|                                                                       |
| await driver.close()                                                  |
|                                                                       |
| print(\'🎉 Importación completa\')                                    |
|                                                                       |
| if \_\_name\_\_ == \'\_\_main\_\_\':                                  |
|                                                                       |
| asyncio.run(main())                                                   |
+-----------------------------------------------------------------------+

**1.4 Consultas Cypher --- Búsqueda Fractal en Acción**

+-----------------------------------------------------------------------+
| // Q1: ¿Qué leyes han modificado el Art. 169 TRLGSS en los últimos 5  |
| años?                                                                 |
|                                                                       |
| MATCH (l:Ley {boe_id: \'BOE-A-2015-11724\'})                          |
|                                                                       |
| -\[:CONTIENE\]-\>                                                     |
|                                                                       |
| (a:Bloque {tipo: \'articulo\', titulo: \'Artículo 169\'})             |
|                                                                       |
| -\[:TIENE_VERSION\]-\>                                                |
|                                                                       |
| (v:Version)                                                           |
|                                                                       |
| WHERE v.fecha_publicacion \> \'20210101\'                             |
|                                                                       |
| RETURN a.titulo, v.fecha_publicacion, v.norma_modificadora,           |
| v.texto_modificacion                                                  |
|                                                                       |
| ORDER BY v.fecha_publicacion DESC                                     |
|                                                                       |
| // Q2: Búsqueda fractal --- Encuentro el concepto \'IT CC\', voy      |
| hacia arriba (artículos, leyes)                                       |
|                                                                       |
| // y hacia abajo (preguntas de examen relacionadas)                   |
|                                                                       |
| MATCH path =                                                          |
| (p:Pregunta)-\[:BASADA_EN\]-\>(b:Bloque)\<-\[:CONTIENE\]-(l:Ley)      |
|                                                                       |
| WHERE b.titulo CONTAINS \'169\' OR b.titulo CONTAINS \'incapacidad    |
| temporal\'                                                            |
|                                                                       |
| RETURN p.texto, p.dificultad, b.titulo, l.numero_oficial              |
|                                                                       |
| ORDER BY p.dificultad DESC LIMIT 10                                   |
|                                                                       |
| // Q3: ¿Qué conceptos son trampa para el C1 SS y tienen calculadora?  |
|                                                                       |
| MATCH (c:Concepto {es_trampa_frecuente: true})                        |
|                                                                       |
| \<-\[:CALCULA\]-(calc:Calculadora)                                    |
|                                                                       |
| WHERE \'c1_ss\' IN c.cuerpos                                          |
|                                                                       |
| RETURN c.titulo, c.tipo_trampa, calc.id, c.num_preguntas_relacionadas |
|                                                                       |
| ORDER BY c.num_preguntas_relacionadas DESC                            |
|                                                                       |
| // Q4: Grafo de dependencias --- qué leyes afectan a la LPAC          |
|                                                                       |
| MATCH (mod:Ley)-\[r:MODIFICA\]-\>(lpac:Ley {boe_id:                   |
| \'BOE-A-2015-10565\'})                                                |
|                                                                       |
| RETURN mod.titulo, r.texto_efecto, r.fecha                            |
|                                                                       |
| ORDER BY r.fecha DESC                                                 |
|                                                                       |
| // Q5: Plan de repaso personalizado --- artículos que un usuario      |
| falla más                                                             |
|                                                                       |
| MATCH (u:Usuario {id:                                                 |
| \$user_id})-\[:FALLO\]-\>(p:Pregunta)-\[:BASADA_EN\]-\>(b:Bloque)     |
|                                                                       |
| WITH b, COUNT(\*) as veces_fallada                                    |
|                                                                       |
| MATCH (b)\<-\[:CONTIENE\]-(l:Ley)                                     |
|                                                                       |
| RETURN b.titulo, l.titulo, veces_fallada                              |
|                                                                       |
| ORDER BY veces_fallada DESC LIMIT 10                                  |
|                                                                       |
| // Q6: Caché semántico --- ¿Ya se respondió una pregunta similar?     |
|                                                                       |
| // (Combinando Neo4j con Qdrant via bridge)                           |
|                                                                       |
| MATCH (p:Pregunta)                                                    |
|                                                                       |
| WHERE p.qdrant_embedding_id IS NOT NULL                               |
|                                                                       |
| AND \'c1_ss\' IN p.cuerpos                                            |
|                                                                       |
| AND p.calidad_score \> 0.90                                           |
|                                                                       |
| RETURN p.id, p.texto, p.qdrant_embedding_id                           |
|                                                                       |
| // → Con los IDs, buscar en Qdrant los más similares a la query del   |
| usuario                                                               |
+-----------------------------------------------------------------------+

**2. Evaluación Docker --- VPS + Cloudflare + Fly.io**

**2.1 Inventario de RAM Real con Docker Compose Completo**

  ------------------------------------------------------------------------
  **Servicio /       **RAM sin    **RAM con    **Notas**
  Container**        Docker**     Docker**     
  ------------------ ------------ ------------ ---------------------------
  Ubuntu 24 OS +     0.8 GB       0.8 GB       No cambia --- base siempre
  kernel                                       

  Docker daemon      ---          0.25 GB      El proceso Docker en sí ---
  (dockerd)                                    overhead fijo e inevitable

  Qdrant :6333 (ya   0.3 GB       0.35 GB      Ya funciona. Imagen
  en Docker)                                   qdrant/qdrant:v1.12

  Neo4j Community    0.6 GB       0.75 GB      JVM: heap inicial 512m, max
  :7474/:7687                                  1g. Imagen
                                               neo4j:5-community

  PostgreSQL :5432   0.25 GB      0.30 GB      Imagen postgres:16-alpine.
                                               Muy ligero.

  Redis :6379        0.05 GB      0.07 GB      redis:7-alpine + maxmemory
                                               256mb

  FastAPI backend    0.15 GB      0.18 GB      Imagen Python 3.12-slim.
  :8000                                        Incluye todas las
                                               dependencias.

  Nginx :80/:443     0.03 GB      0.05 GB      nginx:alpine para reverse
                                               proxy + SSL termination

  Ollama +           4.85 GB      4.85 GB      NATIVO (no Docker). Solo
  Salamandra (SOLO                             para generación masiva
  offline)                                     puntual.

  **TOTAL SIN OLLAMA **2.18 GB**  **2.75 GB**  **✅ HOLGADO --- 5.25 GB
  (stack                                       libres en un VPS 8 GB**
  operacional)**                               

  **TOTAL CON OLLAMA **7.03 GB**  **7.60 GB**  **🔴 RIESGO OOM --- solo
  cargado**                                    cargarlo puntualmente para
                                               generación**
  ------------------------------------------------------------------------

**2.2 Decisión Definitiva: Arquitectura Híbrida por Capas**

  -------------------------------------------------------------------------------------
  **Componente**   **Dónde**    **¿Docker?**   **Justificación**
  ---------------- ------------ -------------- ----------------------------------------
  Neo4j            VPS local    ✅ SÍ          imagen neo4j:5-community. Datos en
                                               volume Docker. Backup: neo4j-admin dump.
                                               Solo expuesto internamente (127.0.0.1).

  PostgreSQL       VPS local    ✅ SÍ          postgres:16-alpine. Migración con
                                               Alembic. Backup automático con pg_dump
                                               en cron.

  Redis            VPS local    ✅ SÍ          redis:7-alpine. maxmemory-policy
                                               allkeys-lru. Solo cache --- pérdida
                                               tolerable.

  Qdrant           VPS local    ✅ YA FUNCIONA Ya está en Docker. No cambiar. También
                                               Cloud free tier para producción.

  Nginx            VPS local    ✅ SÍ          nginx:alpine. SSL termination + reverse
                                               proxy. Cert via certbot volume.

  FastAPI Backend  Fly.io       ✅ SÍ (Fly usa Fly.io lee directamente el Dockerfile.
                   Frankfurt    Docker)        Deploy: fly deploy. Escala a 0 cuando no
                                               hay tráfico = €0 en idle.

  React Frontend   Cloudflare   ❌ NO          Cloudflare Pages acepta build estático
                   Pages                       (npm run build). No necesita Docker. CDN
                                               global automático.

  Ollama +         VPS nativo   ❌ NO (en      Demasiado RAM. Nativo para generación
  Salamandra                    producción)    masiva offline puntual. En portátil:
                                               Docker Ollama funciona bien en 16GB.

  Bot de           VPS nativo   ❌ NO          Script Python que llama a Ollama local.
  generación       (cron)                      No necesita Docker. Se ejecuta de noche
  masiva                                       cuando el tráfico es bajo.
  -------------------------------------------------------------------------------------

**2.3 docker-compose.yml Completo para el VPS**

+-----------------------------------------------------------------------+
| \# docker-compose.yml --- VPS 8GB --- Stack completo sin Ollama       |
|                                                                       |
| \# Memoria estimada: 2.75 GB → 5.25 GB libres                         |
|                                                                       |
| version: \'3.8\'                                                      |
|                                                                       |
| services:                                                             |
|                                                                       |
| qdrant:                                                               |
|                                                                       |
| image: qdrant/qdrant:v1.12.0                                          |
|                                                                       |
| restart: unless-stopped                                               |
|                                                                       |
| ports: \[\'127.0.0.1:6333:6333\', \'127.0.0.1:6334:6334\'\]           |
|                                                                       |
| volumes: \[\'qdrant_storage:/qdrant/storage\'\]                       |
|                                                                       |
| environment:                                                          |
|                                                                       |
| QDRANT\_\_SERVICE\_\_API_KEY: \'\${QDRANT_API_KEY}\'                  |
|                                                                       |
| mem_limit: 1g                                                         |
|                                                                       |
| healthcheck:                                                          |
|                                                                       |
| test: \[\'CMD-SHELL\', \'curl -f http://localhost:6333/readyz \|\|    |
| exit 1\'\]                                                            |
|                                                                       |
| interval: 30s                                                         |
|                                                                       |
| neo4j:                                                                |
|                                                                       |
| image: neo4j:5-community                                              |
|                                                                       |
| restart: unless-stopped                                               |
|                                                                       |
| ports: \[\'127.0.0.1:7474:7474\', \'127.0.0.1:7687:7687\'\]           |
|                                                                       |
| environment:                                                          |
|                                                                       |
| NEO4J_AUTH: \'neo4j/\${NEO4J_PASSWORD}\'                              |
|                                                                       |
| NEO4J_server_memory_heap_initial\_\_size: \'512m\'                    |
|                                                                       |
| NEO4J_server_memory_heap_max\_\_size: \'1g\'                          |
|                                                                       |
| NEO4J_server_memory_pagecache\_\_size: \'256m\'                       |
|                                                                       |
| volumes:                                                              |
|                                                                       |
| \- neo4j_data:/data                                                   |
|                                                                       |
| \- neo4j_logs:/logs                                                   |
|                                                                       |
| \- neo4j_import:/import \# para importar CSVs con LOAD CSV            |
|                                                                       |
| mem_limit: 1.5g                                                       |
|                                                                       |
| healthcheck:                                                          |
|                                                                       |
| test: \[\'CMD-SHELL\', \'cypher-shell -u neo4j -p \$NEO4J_PASSWORD    |
| \"RETURN 1\" \|\| exit 1\'\]                                          |
|                                                                       |
| interval: 30s                                                         |
|                                                                       |
| postgres:                                                             |
|                                                                       |
| image: postgres:16-alpine                                             |
|                                                                       |
| restart: unless-stopped                                               |
|                                                                       |
| ports: \[\'127.0.0.1:5432:5432\'\]                                    |
|                                                                       |
| environment:                                                          |
|                                                                       |
| POSTGRES_USER: \'\${PG_USER}\'                                        |
|                                                                       |
| POSTGRES_PASSWORD: \'\${PG_PASSWORD}\'                                |
|                                                                       |
| POSTGRES_DB: \'opositaia\'                                            |
|                                                                       |
| PGDATA: \'/var/lib/postgresql/data/pgdata\'                           |
|                                                                       |
| volumes: \[\'pg_data:/var/lib/postgresql/data\'\]                     |
|                                                                       |
| mem_limit: 512m                                                       |
|                                                                       |
| shm_size: \'128mb\'                                                   |
|                                                                       |
| redis:                                                                |
|                                                                       |
| image: redis:7-alpine                                                 |
|                                                                       |
| restart: unless-stopped                                               |
|                                                                       |
| command: \'redis-server \--maxmemory 256mb \--maxmemory-policy        |
| allkeys-lru \--requirepass \${REDIS_PASSWORD}\'                       |
|                                                                       |
| ports: \[\'127.0.0.1:6379:6379\'\]                                    |
|                                                                       |
| mem_limit: 350m                                                       |
|                                                                       |
| nginx:                                                                |
|                                                                       |
| image: nginx:alpine                                                   |
|                                                                       |
| restart: unless-stopped                                               |
|                                                                       |
| ports: \[\'80:80\', \'443:443\'\]                                     |
|                                                                       |
| volumes:                                                              |
|                                                                       |
| \- \'./nginx.conf:/etc/nginx/nginx.conf:ro\'                          |
|                                                                       |
| \- \'certbot_certs:/etc/letsencrypt:ro\'                              |
|                                                                       |
| \- \'certbot_www:/var/www/certbot:ro\'                                |
|                                                                       |
| depends_on: \[qdrant, neo4j, postgres, redis\]                        |
|                                                                       |
| mem_limit: 128m                                                       |
|                                                                       |
| certbot:                                                              |
|                                                                       |
| image: certbot/certbot:latest                                         |
|                                                                       |
| volumes:                                                              |
|                                                                       |
| \- \'certbot_certs:/etc/letsencrypt\'                                 |
|                                                                       |
| \- \'certbot_www:/var/www/certbot\'                                   |
|                                                                       |
| entrypoint: \'/bin/sh -c \"trap exit TERM; while :; do certbot renew; |
| sleep 12h & wait \$\${!}; done\"\'                                    |
|                                                                       |
| volumes:                                                              |
|                                                                       |
| qdrant_storage:                                                       |
|                                                                       |
| neo4j_data:                                                           |
|                                                                       |
| neo4j_logs:                                                           |
|                                                                       |
| neo4j_import:                                                         |
|                                                                       |
| pg_data:                                                              |
|                                                                       |
| certbot_certs:                                                        |
|                                                                       |
| certbot_www:                                                          |
|                                                                       |
| \# NOTA: El backend FastAPI NO está aquí --- está en Fly.io Frankfurt |
|                                                                       |
| \# Fly.io usa Docker internamente y lee el Dockerfile del repo        |
|                                                                       |
| \# fly deploy → construye imagen → despliega en Frankfurt → URL       |
| pública con HTTPS                                                     |
|                                                                       |
| \# Las BD en VPS son accesibles desde Fly.io via SSH tunnel o         |
| Wireguard VPN                                                         |
+-----------------------------------------------------------------------+

**2.4 Conexión Fly.io (Backend) ↔ VPS (BDs) --- Opciones**

  ----------------------------------------------------------------------------
  **Opción**         **Cómo           **Pros**         **Cons**
                     funciona**                        
  ------------------ ---------------- ---------------- -----------------------
  Fly.io + BD en VPS Las BDs en VPS   Simple. Sin      ⚠️ Exponer BDs a
  via IP pública     escuchan en      configuración    internet, aunque con
                     0.0.0.0 (con     extra.           auth fuerte. Riesgo si
                     auth). Fly.io                     credentials filtradas.
                     conecta                           
                     directamente por                  
                     IP.                               

  **Fly.io + BD en   **Fly.io tiene   **✅ BDs nunca   **Requiere configurar
  VPS via Wireguard  Wireguard nativo expuestas.       Wireguard en el VPS
  VPN**              (fly wireguard). Tráfico cifrado. (\~30 min).**
                     El backend se    Recomendado para 
                     conecta al VPS   producción.**    
                     como si                           
                     estuviese en                      
                     LAN.**                            

  Todo en Fly.io     Mover también    Más simple de    Más caro. Fly.io
  (alternativa)      Neo4j y Postgres gestionar. Todo  Volumes son
                     a Fly.io         en un proveedor. \$0.15/GB/mes. Un VPS
                     Volumes.                          8GB ya pagado es €0
                                                       adicional.

  **Recomendación:   **---**          **Cero coste     **Algo más
  Backend en Fly.io                   adicional (VPS   configuración inicial
  Frankfurt + BDs en                  ya pagado). BDs  --- pero estable a
  VPS con                             seguras.         largo plazo.**
  Wireguard**                         Latencia \<5ms   
                                      (ambos en EU).** 
  ----------------------------------------------------------------------------

**3. Códigos Electrónicos del BOE --- Guía Completa**

+-----------------------------------------------------------------------+
| **Los Códigos Electrónicos son la mejor fuente que existe para el RAG |
| --- gratuita, oficial y siempre actualizada**                         |
|                                                                       |
| La Biblioteca Jurídica Digital del BOE (boe.es/biblioteca_juridica)   |
| mantiene \'Códigos Electrónicos\' temáticos: PDFs de cientos de       |
| páginas que reúnen TODAS las normas relevantes sobre un tema,         |
| actualizados en cada cambio legislativo. Puedes suscribirte a alertas |
| por email. Para oposiciones, el BOE mantiene códigos específicos por  |
| cuerpo.                                                               |
+-----------------------------------------------------------------------+

**3.1 Códigos Electrónicos Directamente Relevantes**

  -------------------------------------------------------------------------------------------------------------
  **Cód.**   **Nombre**            **URL Descarga PDF (Gratuito)**                                **Para**
  ---------- --------------------- -------------------------------------------------------------- -------------
  **435**    **Normativa para      **www.boe.es/biblioteca_juridica/codigos/codigo.php?id=435**   **C2
             ingreso Cuerpo                                                                       Auxiliar**
             General AUXILIAR                                                                     
             AGE**                                                                                

  **442**    **Normativa para      **www.boe.es/biblioteca_juridica/codigos/codigo.php?id=442**   **C1 AGE**
             ingreso Cuerpo                                                                       
             General                                                                              
             ADMINISTRATIVO AGE**                                                                 

  **443**    **Normativa para      **www.boe.es/biblioteca_juridica/codigos/codigo.php?id=443**   **A2
             ingreso Cuerpo de                                                                    Gestión**
             GESTIÓN Civil del                                                                    
             Estado (A2)**                                                                        

  ---        TRLGSS directo (SS C1 www.boe.es/buscar/act.php?id=BOE-A-2015-11724                  C1 SS / A2
             --- no hay código                                                                    
             unificado)                                                                           

  ---        Código de Seguridad   www.boe.es/biblioteca_juridica/codigos/codigo.php?id=197       C1 SS / A2
             Social (no oficial                                                                   
             AGE --- completo                                                                     
             TRLGSS + reglamentos)                                                                

  **197**    **Código de Seguridad **www.boe.es/biblioteca_juridica/codigos/codigo.php?id=197**   **C1 SS /
             Social --- Texto                                                                     A2**
             Refundido +                                                                          
             Reglamentos + IMV +                                                                  
             PNC**                                                                                
  -------------------------------------------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **Cómo descargar y suscribirse (paso a paso)**                        |
|                                                                       |
| 1\. Ir a boe.es/biblioteca_juridica → buscar el código (ej: \'435\'). |
| 2. Click en el código → aparece la lista de normas que contiene. 3.   |
| Click en \'Descargar PDF\' (botón azul en la parte superior) → PDF    |
| descargado, gratuito, uso libre. 4. Para alertas: click en            |
| \'Suscribirse\' → email cuando cambie cualquier norma del código.     |
| Estrategia de indexación: NO subir el PDF completo a Qdrant. Usarlo   |
| como índice para saber qué leyes existen, después indexar cada ley    |
| individualmente via API BOE para tener metadata limpia.               |
+-----------------------------------------------------------------------+

**4. Evaluación del PRD --- Product Brief V1.1 (Subido)**

+-----------------------------------------------------------------------+
| **Contexto: El PRD ha sido generado con metodología BMAD V6 y         |
| aprobado por el PO el 28/02/2026**                                    |
|                                                                       |
| El documento product-brief.md subido contiene 6 secciones (Visión,    |
| Público, Brownfield, Épicas, Stack, Roadmap) con las decisiones del   |
| PO integradas. Es un documento sólido. La evaluación identifica lo    |
| que está bien, lo que hay que afinar y lo que falta todavía para      |
| convertirlo en el PRD técnico completo.                               |
+-----------------------------------------------------------------------+

**4.1 Aciertos --- Lo que el PRD hace bien**

  -----------------------------------------------------------------------
  **Aspecto**         **Evaluación**
  ------------------- ---------------------------------------------------
  Análisis Brownfield ✅ Excelente. Distingue claramente qué FUNCIONA vs
  completo            qué FALTA. Esto es exactamente lo que el Dev Agent
                      necesita para no reescribir lo que ya existe.

  Decisiones PO       ✅ Las 6 decisiones (Neo4j local, C1 SS primero,
  integradas          Trial €1/Pro €69, foro después) están claramente
                      marcadas y razonadas. Sin ambigüedad para el
                      equipo.

  Regla de oro de     ✅ \'El LLM NUNCA calcula\' está destacado como
  calculadoras        diferenciador central. Correcto: es la clave
                      técnica que elimina alucinaciones numéricas.

  Épica 4 Sistema de  ✅ La tabla de agentes con modelo, función y
  Agentes             pipeline por tipo es exactamente lo que se
                      necesita. Directamente usable para las stories
                      BMAD.

  Métricas de éxito   ✅ Tener objetivos numéricos (100% precisión
  cuantificadas       calculadoras, 5K preguntas Fase 1, NPS \>50)
                      permite saber cuándo la fase está completa.

  Estrategia COSMIC   ✅ El diagrama de 3 capas (Átomo → Derivados →
  documentada         Experiencias) es claro y escalable. Correcto
                      identificar los tags_trampa como metadata de los
                      ítems.
  -----------------------------------------------------------------------

**4.2 Ajustes Recomendados --- Lo que hay que añadir/refinar**

  ----------------------------------------------------------------------------
  **Punto**        **Impacto**   **Recomendación**
  ---------------- ------------- ---------------------------------------------
  Falta: Grafo     🔴 CRÍTICO    La Fase 2 depende de Neo4j pero no aparece en
  Neo4j en el                    el stack de \'Añadir\' de forma explícita con
  stack                          los detalles del esquema fractal. Incluir la
                                 referencia al Apéndice IX (este doc) con el
                                 esquema de 6 capas.

  Falta: BOE API   🔴 CRÍTICO    El PRD menciona \'Alertas BOE\' pero no
  como fuente viva               especifica el mecanismo técnico. Añadir: cron
                                 diario → sumario BOE → detectar cambios →
                                 re-importar a Neo4j → notificar usuarios
                                 afectados. Diferenciador clave vs
                                 competencia.

  Falta: Conexión  🟠 ALTA       El PRD pone Neo4j en VPS y el backend en
  Fly.io ↔ VPS                   Fly.io pero no explica cómo se conectan.
                                 Añadir: Wireguard VPN (fly wireguard) o la
                                 alternativa de exponer con auth. Sin esto el
                                 equipo queda bloqueado en el primer deploy.

  Falta: PNC       🟠 ALTA       El Apéndice VIII confirma que calculos_imv.py
  (Pensiones No                  puede no incluir PNC (RD 357/1991). El PRD
  Contributivas)                 dice \'27 calculadoras SS\' pero el IMV y PNC
                                 son módulos separados. Verificar y
                                 explicitar.

  Falta: Reverse   🟠 ALTA       La feature de notificación cuando el BOE
  RAG                            cambia algo del temario del usuario es el
  (proactividad)                 diferenciador de marketing más potente y
                                 tiene coste de implementación MUY BAJO. No
                                 aparece en el roadmap de Fase 1.

  Falta: Detalle   🟡 MEDIA      Se menciona Claude Sonnet como Verify Agent
  sobre el Verify                pero no se especifican sus Acceptance
  Agent                          Criteria exactos. Añadir:
                                 artículo_citado_existe, cálculo_correcto,
                                 alucinación_detectada,
                                 nivel_dificultad_correcto. Estos son los
                                 criterios que determinan si un ítem entra o
                                 no al banco.

  Falta: Política  🟡 MEDIA      El PRD dice Trial €1/3 días + Pro €69/mes. Es
  de precios en                  una decisión válida pero inusual (muy caro vs
  euros correctos                mercado). La mayoría de plataformas similares
                                 van a €9-15/mes. Recomendación: evaluar si
                                 €69 no genera fricción excesiva en
                                 conversión. Considerar €29/mes o
                                 €69/trimestre.

  Falta:           🟢 BAJA       El PRD los incluye en Fase 3 pero no
  Psicotécnicos en               especifica qué tipos. Las oposiciones AGE y
  Fase 3                         SS incluyen: series numéricas, series de
                                 letras, matrices 3x3, analogías verbales y
                                 ortografía. Añadir estas categorías para que
                                 Fase 3 esté bien definida.
  ----------------------------------------------------------------------------

**4.3 Valoración Global del PRD**

+-----------------------------------------------------------------------+
| **8.2/10 --- Excelente base, listo para generar historias BMAD tras   |
| los ajustes críticos**                                                |
|                                                                       |
| El PRD está en buen estado para empezar. Las decisiones del PO están  |
| integradas, el análisis brownfield es honesto y correcto, las épicas  |
| tienen suficiente detalle técnico para que un desarrollador pueda     |
| empezar. Los 2 ajustes críticos (Neo4j schema + conexión Fly.io↔VPS)  |
| deben añadirse antes de generar las primeras historias BMAD, porque   |
| sin ellos las primeras stories de Fase 2 quedarán bloqueadas. Los     |
| ajustes de media-baja prioridad pueden irse añadiendo iterativamente  |
| durante el desarrollo.                                                |
+-----------------------------------------------------------------------+

**5. Plan V4 --- Todo Integrado, Nada Perdido**

+-----------------------------------------------------------------------+
| **Este es el punto de verdad del proyecto**                           |
|                                                                       |
| Integra: Plan Cósmico original + Apéndices II-IX + Brainstorming      |
| 12/12/2025 + SCAMPER Party Mode + Análisis BMAD + Auditoría           |
| Brownfield 27/02/2026 + Product Brief V1.1 + Evaluación PRD. Si hay   |
| conflicto entre documentos, este apéndice es la fuente verdadera.     |
+-----------------------------------------------------------------------+

**5.1 Stack Técnico Definitivo (sin ambigüedades)**

  -------------------------------------------------------------------------------------------------------------
  **Capa**       **Tecnología**                        **Coste/mes**         **Notas definitivas**
  -------------- ------------------------------------- --------------------- ----------------------------------
  Frontend       React 19 + Vite + TS + Cloudflare     €0                    CDN global, HTTPS auto. Ya existe
                 Pages                                                       en brownfield.

  Backend        FastAPI (Docker en Fly.io Frankfurt)  \~€5-10               Dockerfile propio. fly deploy.
                                                                             Escala a 0 en idle.

  Vector DB      Qdrant Cloud free tier + Qdrant local €0                    Cloud para prod. Local para dev.
                 VPS                                                         Ya activo con 48.866 chunks.

  Grafo          Neo4j Community (Docker en VPS)       €0 (VPS ya pagado)    Esquema 6 capas del Apéndice IX.
  Knowledge                                                                  Importar via API BOE.

  SQL            PostgreSQL 16-alpine (Docker en VPS)  €0                    Usuarios, progreso, pagos,
                                                                             métricas.

  Cache          Redis 7-alpine (Docker en VPS)        €0                    Semántico + rate limiting +
                                                                             sesiones. maxmemory 256mb.

  Auth           Clerk.com                             €0 (\<10K MAU)        Magic link + Google OAuth + roles.
                                                                             Webhook a FastAPI.

  Pagos          Stripe                                1.4%+0.25€/tx         Trial €1/3d + Pro €69/mes. Webhook
                                                                             actualiza rol Clerk.

  LLM Chat       GPT-OSS 120B vía Groq (\$0.28/M)      \~€0.28/usuario/mes   Principal. Velocidad \<1s.
                                                                             Function calling fiable.

  LLM            Mistral Nemo (\$0.02/M)               \~€0.01/usuario/mes   Intent Agent. El más barato para
  Clasificador                                                               clasificar.

  LLM            Claude Sonnet 4.6 (Batch API          \~€0.03/ítem          Verify Agent. Mejor reasoning
  Verificación   \$1.50/M)                                                   jurídico.

  LLM Generación DeepSeek V3 (\$0.27/M)                Variable              Generator Agent. Generación masiva
  offline                                                                    banco preguntas.

  LLM Calc       Devstral Small 1.1 (\$0.10/M)         Mínimo                Genera calculadoras Python cuando
  dinámicas                                                                  no existe la función.

  OCR PDFs       Mistral Pixtral (OCR)                 Mínimo                PDFs subidos por usuario. Qdrant
                                                                             temporal 24h.

  Seguridad      Groq Prompt Guard 2 (\$0.03/M)        \~€0.01/usuario/mes   Detecta prompt injection antes del
                                                                             LLM principal.

  Embedding      pablosi/bge-m3-spa-law-qa-trained-2   €0 (self-hosted)      Especializado derecho español
                                                                             1024d. Ya en producción.

  Reverse RAG    Cron diario + BOE API + Push API      €0                    BOE gratis. Push API nativa del
                                                                             navegador.

  Dataset        Nemotron-70B (NVIDIA Build, 100K      €0                    Para filtrar banco de preguntas
  verifier       free)                                                       existentes.

  IDE dev        Cursor + Claude Sonnet                €20/mes               BMAD V6 workflow. Context
                                                                             engineering via docs.

  **TOTAL MVP                                          **€25-40/mes + €20    **Cursor + dominio + algo APIs
  FASE 1**                                             Cursor**              LLM + free tiers del resto**
  -------------------------------------------------------------------------------------------------------------

**5.2 Roadmap 16 Semanas --- Con Tasks BMAD**

  -----------------------------------------------------------------------------
  **Sem**   **Fase +          **Tasks concretas (cada una = 1 Story BMAD)**
            Objetivo**        
  --------- ----------------- -------------------------------------------------
  1         Setup + Limpieza  \(1\) Mover 147 archivos de raíz →
                              de_raiz_backup/. (2) Instalar Cursor + configurar
                              BMAD. (3) Crear project-brief.md +
                              architecture.md (este plan). (4)
                              docker-compose.yml completo en VPS.

  2         Docker VPS        \(1\) Añadir Neo4j + PostgreSQL + Redis al
                              compose (Qdrant ya existe). (2) Configurar
                              Wireguard entre VPS y Fly.io. (3) Nginx + Let\'s
                              Encrypt. (4) Verificar health checks de todos los
                              servicios.

  3         Calculadoras AGE  \(1\) calculadora_age.py (28 tipos: LPAC +
                              TREBEP + transversales). (2) Tests unitarios con
                              casos de examen reales. (3) Integrar en
                              dispatcher.py. (4) Endpoint /api/calcular-age.

  4         Neo4j Import      \(1\) Ejecutar boe_neo4j_importer.py con las 6
                              leyes CRÍTICAS. (2) Verificar esquema 6 capas.
                              (3) Tests de las consultas Cypher del §1.4. (4)
                              Importar official_exams_qa_FINAL_V3.jsonl →
                              Neo4j.

  5         Agentes v1        \(1\) Orchestrator.py con decision tree de 8
                              pipelines. (2) Intent Agent (Mistral Nemo). (3)
                              RAG Agent (Qdrant + BOE XML vigencia). (4)
                              Calculator Agent (dispatcher.py).

  6         Agentes v2        \(1\) Generator Agent (DeepSeek V3 + pedagogía
                              Valera). (2) Verify Agent (Claude Sonnet AC:
                              artículo existe + cálculo correcto + 0
                              alucinación). (3) Compile Agent. (4) E2E test:
                              \'Explícame la IT\' → respuesta verificada.

  7         RAG Expandido     \(1\) Indexar Código 197 SS + Código 442 AGE via
                              API BOE. (2) Cron BOE sumario diario. (3) Reverse
                              RAG: detectar cambio → notificar usuario. (4)
                              Suscripción alertas email Códigos 435/442.

  8         COSMIC Pipeline   \(1\) Generator Agent: 1 concepto → 6 formatos.
                              (2) Filtrar \~5K preguntas con Nemotron (gratis).
                              (3) Contenido paramétrico: variables numéricas
                              como parámetros. (4) Banco: 1K preguntas SS
                              verificadas.

  9         Auth + Simulacros \(1\) Clerk.com configurado (magic link + Google
                              OAuth + roles). (2) Simulacros C1 SS: 20
                              preguntas cronometradas. (3) Migrar localStorage
                              → PostgreSQL. (4) ProgressView conectado a PG.

  10        Repetición        \(1\) Algoritmo SM-2 en Neo4j
            espaciada         (fecha_siguiente_repaso por pregunta por
                              usuario). (2) Plan de estudio dinámico. (3)
                              Perfil de opositor con temas fuertes/débiles. (4)
                              Feynman mode.

  11        Monetización      \(1\) Stripe: productos Trial €1/3días + Pro
                              €69/mes. (2) Webhook actualiza rol en Clerk. (3)
                              Free tier limitado (20 queries/día). (4) Pasarela
                              de pago en frontend.

  12        Deploy completo   \(1\) Fly.io deploy FastAPI Frankfurt. (2)
                              Cloudflare Pages deploy React. (3) Wireguard VPN
                              activo. (4) Monitoring + alertas (uptime + error
                              rate).

  13        Beta cerrada      \(1\) Reclutar 20-30 opositores C1 SS. (2) PRO
                              gratis 3 meses. (3) Métricas semanales: acierto
                              por tema. (4) Entrevistas de usuario: 3 preguntas
                              máximo.

  14        Iteración beta    \(1\) Corregir top-5 bugs. (2) Mejorar 10
                              preguntas con peor ratio acierto. (3) Afinar
                              Verify Agent con falsos positivos encontrados.
                              (4) Banco a 5K preguntas SS.

  15        Pre-lanzamiento   \(1\) B2B: demos con 5 preparadores. (2) Landing
                              con testimonios. (3) Posts LinkedIn/X con datos
                              beta. (4) Stripe en producción real (primer
                              cobro).

  16        Lanzamiento       \(1\) Anuncio público. (2) Activar Stripe para
                              nuevos usuarios. (3) Monitoreo 24/7. (4) Backlog
                              Fase 2 priorizado según feedback beta.
  -----------------------------------------------------------------------------

**5.3 Qué hacer MAÑANA (Máximo Impacto, Mínimo Tiempo)**

  -------------------------------------------------------------------------------------
  **\#**   **Tarea**                   **Por qué es la más importante       **Horas**
                                       ahora**                              
  -------- --------------------------- ------------------------------------ -----------
  **1**    **Limpiar los 147 archivos  **Sin esta limpieza el proyecto es   **1h**
           de raíz → de_raiz_backup/** inmanejable y el contexto de Cursor  
                                       se contamina con archivos obsoletos. 
                                       Es técnicamente deuda crítica que    
                                       bloquea todo lo demás.**             

  **2**    **Filtrar \~5K preguntas    **El banco existente ya tiene \~5K   **3h**
           con Nemotron (NVIDIA Build, preguntas pero de calidad variable.  
           gratis)**                   Nemotron las filtra gratuitamente.   
                                       Resultado: gold dataset sin coste.   
                                       Las buenas van directo a Neo4j.**    

  3        docker-compose.yml VPS:     Formalizar la infra. Después cada    2h
           añadir Neo4j + PG + Redis   servicio se gestiona solo con        
           (Qdrant ya existe)          \'docker compose up/down\'. Backup   
                                       trivial con volumes.                 

  4        Descargar Código 197 (SS) y Fuentes primarias para el RAG.       0.5h
           Código 442 (AGE) del BOE +  Gratuitas. Las alertas email son la  
           suscribir alertas           base del Reverse RAG.                

  5        Verificar calculos_imv.py   Si no incluye PNC, el banco de       0.5h
           incluye PNC (RD 357/1991)   preguntas del Tema 12 SS tendrá un   
                                       gap de cobertura.                    

  6        Ejecutar                    CE + LPAC + LRJSP + TREBEP +         3h
           boe_neo4j_importer.py con   TRLGSS + IMV. El grafo base que      
           las 6 leyes CRÍTICAS        alimentará todo el RAG fractal.      
  -------------------------------------------------------------------------------------

*Apéndice IX · OpositAIA · 28 Febrero 2026*

*Integra: Apéndices I-VIII + Product Brief V1.1 + PRD BMAD + Auditoría
Brownfield + BOE API Docs + Brainstorming + SCAMPER + BMAD V6*
