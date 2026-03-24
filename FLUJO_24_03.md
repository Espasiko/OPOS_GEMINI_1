# ARQUITECTURA Y FLUJO V14 (24 DE MARZO DE 2026)

Este documento detalla el ciclo vital completo de un Caso Práctico desde su concepción hasta su validación en la V14 "Schema-First", incluyendo los archivos, las bases de datos y el flujo de información.

## 1. El Catálogo del Conocimiento (Los Cimientos)
*Archivos:*
- `/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/catalogo_trampas.yaml`
- `/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/catalogo_trampas_adicional.yaml`
*Función:* Es el cerebro humano de Diego de Miguel destilado. Contiene cientos de trampas (ej. `C1`, `C2`, `H2`) con sus reglas, artículos exactos, mnemónicos y el "por qué" fallan los alumnos. NUNCA DEBEN SER INVENTADAS POR LA IA.

## 2. Bases de Datos Híbridas (El Cerebro Legal)
Existen dos bases de datos complementarias que se alimentan entre sí (`populate_neo4j_from_qdrant.py` y `rag_helper.py`):
- **Qdrant (Base Vectorial):** Contiene miles de fragmentos de ley (chunks) vectorizados. Su función principal es la **Búsqueda Semántica**. Permite preguntar "leyes sobre incapacidad en embarazos" y el motor vectorial escupe los fragmentos más similiares.
- **Neo4j (Base de Grafos):** Contiene los Artículos como NODOS inmutables interconectados mediante relaciones (`MODIFICA_A`, `DEROGA_A`, `DESARROLLA_A`). Aquí SÍ hay texto íntegro (la propiedad `a.texto`). 
*En el E2E usamos Neo4j porque no queremos similitud semántica, queremos extraer el MATCH EXACTO (`a.id = "Art. 204 TRLGSS"`) para inyectarlo literal al LLM.*
*¿Leyes Locales?* Neo4j y Qdrant contienen más de 59 leyes (Constitución, TREBEP, Jurisprudencia, Decretos... y Sí, la Ley de Bases de Régimen Local - LBRL). Por eso la búsqueda debe exigir `ley = TRLGSS`.

## 3. El Esqueleto del Examen (Blueprints)
*Archivos:* `/home/spas/OPOS_GEMINI_1/backend/v14/blueprints/bp_s12_jubilacion_2026.py`
*Función:* Define el tema (ej. Jubilación 2026) y exige el conocimiento obligatorio:
- Artículos clave.
- Funciones matemáticas que Python debe calcular.
- Las `trampas_tipicas` específicas (lista de IDs del catálogo) para llegar a las **15 preguntas** oficiales.

## 4. El Orfebre de Datos (CaseSchemaBuilder)
*Archivos:* `/home/spas/OPOS_GEMINI_1/backend/v14/case_schema_builder.py`
*Flujo:*
1. Carga el Blueprint.
2. Extrae las trampas desde el Catálogo YAML.
3. Se conecta a **Neo4j** y vuelca el `texto` completo de los artículos BOE en la variable `contexto_legal`.
4. Devuelve un **JSON Hermético** de solo lectura. (Ej: "Juan y Ana / Art 204 / Trampa C1 / Valor Matemático X").

## 5. El Actor y su Guion (LLM + Prompt)
*Archivos:* `/home/spas/OPOS_GEMINI_1/opos-agents/agents/redactor_v14.yaml` y script lanzador `test_e2e_v14_mistral.py`.
*Flujo:* Mistral Large consume el JSON hermético. Instrucciones del prompt:
- Eres Diego de Miguel.
- Crea una narrativa entrelazada.
- Distribuye A, B, C, D (25% c/u).
- NO INVENTES NADA QUE NO ESTÉ EN EL JSON.
- Mistral escupe la obra literaria (el Markdown final con 15 preguntas).

## 6. Los Jueces y Verdugos (Validación)
*Archivos:* 
- `/home/spas/OPOS_GEMINI_1/backend/v14/prose_validator.py`
- `/home/spas/OPOS_GEMINI_1/backend/agents/verification_agents.py`
*Flujo:*
1. **Prose Validator:** Compara las matemáticas y detecta intrusión de léxico (Filtro Anti-Alucinaciones o "Domain Check").
2. **Orquestador de 7 dimensiones:** Audita la pedagogía, coherencia BOE y cruza los roles.
3. **Guardado Final:** Todo se exporta al directorio de Academias o a `/tmp/`.
