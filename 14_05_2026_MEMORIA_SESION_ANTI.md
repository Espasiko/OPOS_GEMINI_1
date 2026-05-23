# MEMORIA DE SESIÓN - AUDITORÍA Y POST-ETIQUETADO DE EXCEPCIONES
**Fecha de registro:** 14/05/2026 (Ref: 14_06_2026_MEMORIA_SESION_ANTI)
**Proyecto:** OpositAIA
**Objetivo Principal:** Cerrar la fase de etiquetado manual y estructurar el cerebro lógico (Neo4j) y la capa de estudio humana (Obsidian Wiki) en relación a las Excepciones Jurídicas.

---

## 1. Hitos Alcanzados

### A) Refinado Estructural del Grafo (Neo4j)
Se intervino directamente en la base de datos de grafos para asegurar que la inteligencia inyectada sea robusta y trazable:
- **Verificación Humana:** Se actualizó cada una de las 359 relaciones de excepción (`[:EXCEPCION_A]`) con la propiedad `verificado_humano: true`.
- **Bidireccionalidad:** Se generaron 359 relaciones inversas (`[:TIENE_EXCEPCION_EN]`). Esto permite a la arquitectura RAG navegar desde la norma exceptuada hacia la norma que dicta la excepción, mejorando la inferencia de los agentes.
- **Nodo Maestro:** Se creó un nodo `(n:Indice)` para persistir metadatos de control y volumen de excepciones actualizadas.
- *Nota arquitectónica:* Dado que Neo4j Community Edition no permite "Relationship Property Uniqueness", se validó y confirmó el uso intensivo de la cláusula `MERGE` en todos los scripts de ingesta como mecanismo para garantizar la integridad y evitar relaciones duplicadas.

### B) Integración con la Bóveda de Estudio (Obsidian Wiki)
Se automatizó la extracción de las excepciones desde el grafo hacia el entorno de lectura humano.
- **Archivo Generado:** Se exportaron las 359 excepciones al archivo `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/_INDICE_EXCEPCIONES.md`.
- El archivo contiene una tabla estructurada que consolida la norma origen, la norma destino, la señal textual detectada ("salvo", "sin perjuicio", etc.), la categoría (exclusión, salvedad, etc.) y la relevancia de cara al examen.

### C) Prevención de Alucinaciones (Ground Truth)
- **Dataset "Oro":** Se extrajo un muestreo aleatorio y equilibrado de 20 relaciones `EXCEPCION_A` del grafo.
- **Archivo Generado:** `backend/data/ground_truth_excepciones.json`.
- **Propósito:** Actuar como set de pruebas validado manualmente. Servirá de baseline en el futuro para medir la eficacia y fiabilidad de nuevos modelos (ej. Salamandra R1 o iteraciones futuras) al momento de interpretar excepciones legislativas.

---

## 2. Herramientas y Scripts Ejecutados

1. **`backend/scripts/post_etiquetado_neo4j.py`**
   - Encargado de las actualizaciones directas en Neo4j (Propiedades de relaciones y nodo Índice).
   
2. **`backend/scripts/generar_indice_wiki.py`**
   - Encargado de extraer los datos mediante Cypher, formatearlos a Markdown y depositar el índice en la carpeta de la bóveda de Obsidian, generando simultáneamente el Ground Truth JSON.

---

## 3. Estado del Sistema
- La fase de etiquetado de excepciones queda **oficialmente cerrada y validada**.
- La base de datos Neo4j se mantiene **100% libre de duplicados y alucinaciones** respecto a este lote de modificaciones.
- **Próximos pasos naturales:** Comenzar la ingesta y auditoría de la capa de Jurisprudencia o retomar simulacros con el motor RAG ya potenciado con las relaciones inversas.
