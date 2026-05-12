# 📚 MEMORIA FIN DE CONFIGURACIÓN: CHANDRA FUNCIONAL (01.05.2026)

> **Fecha y Estado:** 01 de Mayo de 2026. Backend Chandra plenamente funcional, enrutamiento arreglado y problemas de alucinación temporal solventados.

Esta memoria documenta los hitos alcanzados para asegurar la conectividad y funcionamiento del Agente Chandra en el entorno de Obsidian del usuario, tras esquivar los bloqueos de red de Windows.

---

## 1. 🚀 Solución de Red y Backend (El fin del ERR_CONNECTION_REFUSED)

*   **Problema Original:** Windows portproxy fallaba al intentar enrutar tráfico hacia la IP nativa de WSL (`172.26.252.107:8000`). Esto causaba bloqueos (connection refused) en los plugins de Obsidian.
*   **Solución Definitiva:** Se movió el backend de Python (Chandra) a escuchar en el puerto `8080`. Gracias a la arquitectura de WSL2, el localhost se reenvía de forma automática.
*   **Configuración Final:**
    *   **BMO Chatbot:** Se accede vía `http://127.0.0.1:8080/opos/v1`. Se creó el perfil dedicado `Chandra_Opos.md` en la carpeta `BMO/Profiles/` con el prompt del sistema.
    *   **Copilot:** Se accede vía `http://127.0.0.1:8080/v1` configurado **explícitamente** como `baseUrl` dentro del modelo personalizado (`agente-escritor` o `chandra`) en el `data.json`, esquivando el bug nativo de Copilot que ignoraba proxies globales.

## 2. 📅 Solución a la Alucinación Temporal ("Hoy es 15 de octubre de 2024")

*   **Problema:** Al no poseer reloj interno, Mistral (LLM) alucinaba fechas pasadas al pedírsele información de "hoy", provocando que la herramienta de búsqueda en el BOE fallase buscando días incorrectos.
*   **La Solución (Inyección Dinámica):** El script `opos_chat.py` ha sido modificado para que **antes de cada envío a la API**, se obtenga la fecha real del sistema operativo (`datetime.datetime.now()`) y se inyecte por la fuerza en el mensaje de sistema:
    `[SISTEMA - IMPORTANTE: LA FECHA ACTUAL DE HOY ES {YYYY-MM-DD}. Basa todas tus búsquedas temporales estrictamente en esta fecha real.]`
*   *Nota para el usuario:* No es necesario decirle al agente que actualice su fecha. ¡El servidor de Python le incrusta la fecha atómica actual cada vez que le das al "Enter"! Mañana, el código le dirá automáticamente que es 2 de mayo.

## 3. 🛠️ Las 7 Herramientas (Tools) de Chandra

Chandra es un agente de "7 brazos". Si Mistral detecta la necesidad, dispara de forma automática código en Python para:

1.  `tavily_search`: Búsqueda en internet en tiempo real para temas de actualidad.
2.  `search_boe`: Búsqueda de legislación consolidada usando la API abierta del Gobierno.
3.  `get_law_text_block`: Extracción de un artículo específico de una ley con su texto exacto en una fecha de corte concreta.
4.  `consultar_neo4j`: Consultas directas al grafo de conocimiento legal y relaciones normativas.
5.  `calcular_ss`: Conjunto de calculadoras paramétricas (jubilación, viudedad, brecha de género) hechas en Python puro sin depender de que el LLM invente matemáticas.
6.  `buscar_vault`: Búsqueda local en tu propia bóveda de Obsidian (notas, simulacros, casos de academia).
7.  `escribir_vault`: **NUEVA (01/05/2026)** - Crea o añade contenido a notas en el vault Obsidian automáticamente. Permite guardar respuestas de casos prácticos, esquemas o resúmenes sin copiar/pegar manualmente.

## 4. 🆕 Implementación de la 7ª Mano (01/05/2026)

*   **Problema Detectado:** Chandra no podía crear notas automáticamente en el vault. El usuario tenía que copiar/pegar manualmente las respuestas de casos prácticos. Mistral no detectaba la capacidad de escribir en el vault porque la tool no existía en el schema.
*   **Solución Implementada:** Añadida la 7ª herramienta `escribir_vault` a Chandra:
    *   **Archivo modificado:** `backend/agents/chandra_tools.py`
    *   **Schema añadido:** Tool `escribir_vault` con parámetros `path`, `content`, `mode`
    *   **Implementación:** `tool_escribir_vault()` llama a endpoint `/mcp/vault/write` del backend
    *   **Dispatcher actualizado:** Añadido a `TOOL_FUNCTIONS` para que Mistral pueda invocarla
*   **Parámetros de la tool:**
    *   `path`: Ruta del archivo dentro del vault (ej: `casos_practicos/caso_01.md`)
    *   `content`: Contenido en formato Markdown a escribir
    *   `mode`: `"overwrite"` para crear/reemplazar, `"append"` para añadir al final
*   **Backend requerido:** Endpoint `/mcp/vault/write` ya existía en `mcp_gateway.py` (implementado 24/04/2026)
*   **Reinicio necesario:** Backend reiniciado el 01/05/2026 a las 23:13 para cargar la nueva tool
*   **Uso:** Chandra ahora puede guardar automáticamente respuestas de casos prácticos, esquemas o resúmenes en el vault sin intervención manual del usuario.

## 5. 🔍 Resolución de Dudas del Usuario

### A. Neo4j no encuentra "perceptos"
Las búsquedas en base de datos requieren precisión quirúrgica. Legalmente la palabra es **"preceptos"** (con la *R* antes de la *E*). Si en Neo4j se busca textualmente "perceptos", devolverá vacío porque es una falta de ortografía. Además, Neo4j depende de cómo se haya construido el índice (nodos tipo `Article`, `Law`). El repoblado del vault asegurará que los metadatos estén perfectamente alineados.

### B. Uso de contexto forzado (como @ o #) en BMO
Copilot tiene nativo el uso de `@` para adjuntar archivos. BMO Chatbot tiene un enfoque distinto:
*   En los ajustes de BMO (y en el perfil de Chandra) está activado `enableReferenceCurrentNote: true`. BMO lee **siempre** la nota que tienes abierta en pantalla.
*   Puedes crear **Workflows** en BMO creando diferentes archivos de Perfil (`.md` en `BMO/Profiles/`). Puedes tener un `Chandra_Tribunal.md` que le diga que actúe como examinador exigente, o un `Chandra_Resumen.md` que solo haga esquemas. Simplemente cambias el perfil con un click en la barra de BMO.
*   En BMO puedes usar el comando `/append` o la selección de texto para referenciar partes específicas.

### C. Restricciones de Mistral API (Free Tier)
Tras consultar la documentación y la memoria del proyecto, la capa gratuita (Experiment Tier) de Mistral tiene restricciones muy agresivas pensadas solo para desarrollo:
*   **Límite de velocidad:** Normalmente 1 petición por segundo (RPS). Si haces varios clicks rápidos, la API rechazará el mensaje con un error `429 Too Many Requests`.
*   **Límites mensuales:** Rondan el millón de tokens al mes.
*   **Recomendación:** No usar a Chandra para resumir documentos gigantescos (e.g., 200 páginas de academia de golpe), ya que agotará el cupo gratuito en una tarde. Usarlo estrictamente para consultas puntuales, dudas legales y resolución de tests.

## 5. 🗺️ Siguientes Pasos (El Plan WIKI NEXO v5.2)

Habiendo validado la conectividad del Agente, la prioridad técnica vuelve a ser el **Vault y los Datos** (basado en `20_04_26_PLAN_WIKI_NEXO_v5_1.md`):

1.  **Limpieza y Muro de Abstracción:** Aplicar el filtro de nombres reconocibles (PII) a los YAML.
2.  **Regeneración del Vault:** Ejecutar los scripts para generar los 249 archivos limpios de trampas y preceptos.
3.  **Procesado de Materiales Atrasados:** Ingestar los simulacros de las academias (Cortes, Sara Domínguez, etc.) mediante RAG o procesamiento offline (para no gastar la API de Mistral), y convertirlos en nuevos nodos de Neo4j y archivos de la Bóveda.
4.  **Sincronización Total:** Asegurar que la herramienta `buscar_vault` de Chandra tenga acceso a este nuevo tesoro de datos limpios.

---
*Documento autogenerado por Antigravity para Spas. Registrado simultáneamente en el Knowledge Graph MCP.*
