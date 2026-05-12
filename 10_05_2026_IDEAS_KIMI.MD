# 💡 MEMORIA CONSOLIDADA DE IDEAS Y ARQUITECTURA - OPOSITAIA 2026

**Fecha:** 10 de Mayo de 2026  
**Estado:** Consolidación de ideas maestras, plan de implementación y arquitectura del vault

---

## 📋 INFORME DE ESTADO 03/05/2026 - ESTRUCTURAS DE LA BOVEDA

### 1. 🚀 Solución de Red y Backend (El fin del ERR_CONNECTION_REFUSED)

*   **Problema Original:** Windows portproxy fallaba al intentar enrutar tráfico hacia la IP nativa de WSL (`172.26.252.107:8000`). Esto causaba bloqueos (connection refused) en los plugins de Obsidian.
*   **Solución Definitiva:** Se movió el backend de Python (Chandra) a escuchar en el puerto `8080`. Gracias a la arquitectura de WSL2, el localhost se reenvía de forma automática.
*   **Configuración Final:**
    *   **BMO Chatbot:** Se accede vía `http://127.0.0.1:8080/opos/v1`. Se creó el perfil dedicado `Chandra_Opos.md` en la carpeta `BMO/Profiles/` con el prompt del sistema.
    *   **Copilot:** Se accede vía `http://127.0.0.1:8080/v1` configurado **explícitamente** como `baseUrl` dentro del modelo personalizado (`agente-escritor` o `chandra`) en el `data.json`, esquivando el bug nativo de Copilot que ignoraba proxies globales.

### 2. 📅 Solución a la Alucinación Temporal

*   **Problema:** Al no poseer reloj interno, Mistral (LLM) alucinaba fechas pasadas al pedírsele información de "hoy".
*   **La Solución (Inyección Dinámica):** El script `opos_chat.py` ha sido modificado para que **antes de cada envío a la API**, se obtenga la fecha real del sistema operativo (`datetime.datetime.now()`) y se inyecte por la fuerza en el mensaje de sistema:
    `[SISTEMA - IMPORTANTE: LA FECHA ACTUAL DE HOY ES {YYYY-MM-DD}. Basa todas tus búsquedas temporales estrictamente en esta fecha real.]`

### 3. 🛠️ Las 7 Herramientas (Tools) de Chandra

Chandra es un agente de "7 brazos":

1.  `tavily_search`: Búsqueda en internet en tiempo real para temas de actualidad.
2.  `search_boe`: Búsqueda de legislación consolidada usando la API abierta del Gobierno.
3.  `get_law_text_block`: Extracción de un artículo específico de una ley con su texto exacto en una fecha de corte concreta.
4.  `consultar_neo4j`: Consultas directas al grafo de conocimiento legal y relaciones normativas.
5.  `calcular_ss`: Conjunto de calculadoras paramétricas (jubilación, viudedad, brecha de género) hechas en Python puro.
6.  `buscar_vault`: Búsqueda local en tu propia bóveda de Obsidian (notas, simulacros, casos de academia).
7.  `escribir_vault`: **NUEVA (01/05/2026)** - Crea o añade contenido a notas en el vault Obsidian automáticamente.

### 4. 🗺️ Arquitectura del Vault y Plugins

**Plugins Instalados en BOVEDA_OPOS:**
*   **BMO Chatbot:** Conector principal para Chandra (backend propio en puerto 8080)
*   **Copilot:** Plugin alternativo con conexión al mismo backend
*   **obsidian-local-rest-api:** Permite que el backend Python escriba/lea notas del vault
*   **Obsidian-to-Anki:** Para exportar flashcards a Anki (integración futura)

**Estructura del Vault:**
*   `BMO/Profiles/` - Perfiles de agentes (Chandra_Opos.md, etc.)
*   `BMO/Chats/` - Historiales de conversaciones
*   `wiki/` - Knowledge base (temario, trampas, preceptos)
*   `academias/` - Materiales de academias (pendientes de filtrar por Muro de Abstracción)

---

## 🧠 IDEAS MAESTRAS Y ESTRATÉGICAS

### 1. Estrategia Multi-Agente y Flujos

*   **Pipeline Secuencial en Obsidian:** En lugar de un solo agente complejo, usar un flujo lineal:
    1.  *Agente Researcher (El sabueso):* Busca en Neo4j y en el Vault (trampas).
    2.  *Agente Generador Creativo:* Crea el caso usando Groq OSS 120B o Llama 3.3.
    3.  *Agente Revisor Crítico (El destructor):* Temperatura 0. Verifica excepciones y trampas.
    4.  *Agente Calculador:* Delega las matemáticas exclusivamente a scripts Python.
*   **Enrutador Universal con LiteLLM:** Implementar LiteLLM para saltar entre Mistral, Gemini y Groq. Si Mistral da error 429, el sistema usa Groq como "Fallback" automático usando *Exponential Backoff*.

### 2. Arquitectura de Bases de Datos (Neo4j y Obsidian)

*   **Etiqueta de Excepciones `[:EXCEPCION_A]` en Neo4j:** Crear relación explícita entre normas generales y sus excepciones (ej. "salvo lo dispuesto en...").
*   **Extracción de Trampas con Cypher:** Usar consultas en los 6.300 preceptos buscando frases como "No obstante", "Sin perjuicio de", "Excepcionalmente".
*   **Muro de Abstracción Legal:** Los materiales de terceros (academias) nunca entran crudos al Vault. Se reescriben para evitar problemas de derechos de autor.

### 3. Ideas de Producto y Empaquetado

*   **Chandra Desktop App (Tauri + Sidecar):** Empaquetar el frontend React junto al backend Python usando Tauri. Resultado: un único instalador `.exe` de Windows.
*   **BYOV (Bring Your Own Vault):** Para evitar problemas legales, la app se distribuye limpia. El usuario se baja Obsidian gratis y mete nuestro Vault ZIP por separado.
*   **Modelo de Negocio "Freemium BYOK":**
    *   Gratis: Límite diario de consultas.
    *   Premium (9,99€/19,99€).
    *   Premium BYOK (Bring Your Own Key): El usuario mete su propia clave de API.

### 4. "Gánale a mi IA" (Mini App Foros / Crowdsourcing)

*   **El Concepto:** App gamificada donde la IA responde preguntas de examen, y los opositores debaten si la IA acertó o se equivocó.
*   **El Truco (Crowdsourcing):** Al evaluar las respuestas de la IA, los usuarios validan gratuitamente los datos que alimentan la base COSMIC. Es verificación humana gratis.

### 5. "Las 12 Ideas Creativas" para la Wiki

1.  **Árbol de leyes con backlinks inversos:** Abrir un artículo y ver conectadas sus trampas, temas, personajes y jurisprudencia.
2.  **Matriz 13x13 (Puentes entre temas):** Mostrar relaciones explícitas cruzadas entre temas.
3.  **Error Museum:** Ranking de las 100 trampas que más caen en exámenes.
4.  **Timeline Legal 1966-2026:** Evolución de leyes clave de la Seguridad Social.
5.  **Calculadoras Embebidas:** Conectar el Vault visualmente a los scripts de cálculo del backend.
6.  **Flowcharts de Decisión (Mermaid):** Gráficos visuales interactivos.
7.  **Diccionario de Falsos Amigos:** "Subsidio vs Pensión", "Hecho causante vs Solicitud".
8.  **Mapa Mental Maestro:** SVG enorme con los 13 temas de la oposición.
9.  **Glosario de Siglas con Hover:** Definiciones automáticas al pasar el ratón.
10. **Wiki de Tropos (TVTropes style):** Explicaciones con humor y rigor.
11. **Biblioteca de Formularios:** TA.1, TA.2, TC.1 con errores frecuentes marcados.
12. **Spaced Repetition (Anki/Mochi):** Scripts automáticos que exporten trampas a CSV para Anki.

### 6. Pedagogía y COSMIC

*   **Sistema Socratic y Leitner:** OpositAIA no da las respuestas masticadas de inicio, aplica repetición espaciada (1→3→7→14→30→90 días).
*   **Mnemotecnias:** Acrónimos, rimas, "palacios de la memoria" y *chunking* para cada dato duro.
*   **Base COSMIC (Conceptos Múltiples):** Cada concepto legal se almacena y presenta en 6 formatos (literal, caso práctico, test, resumen, esquema, trampa).

---

## 🏛️ PLAN DE IMPLEMENTACIÓN Y ARQUITECTURA TÉCNICA

### 1. Auditoría GROQ (02.05.2026) y Resiliencia LiteLLM

**Modelos Groq Oficiales por Categoría (Mayo 2026):**

*   **Function Calling / Tool Use:**
    *   `GPT OSS 120B`
    *   `GPT OSS 20B`
    *   `Llama 4 Scout`
    *   `Qwen 3 32B`
*   **Reasoning (Para deducciones legales complejas):**
    *   `GPT OSS 120B`
    *   `GPT OSS 20B`
    *   `Qwen 3 32B`
*   **Text to Text (Generación general):**
    *   `GPT OSS 120B` / `GPT OSS 20B`
    *   `Llama 4 Scout`
    *   `Llama 3.3 70B`

**Batch API de Groq:**
*   Procesa archivos JSONL asíncronos con **50% de descuento**.
*   No consume límites diarios de Rate Limit gratuitos.
*   Perfecta para crear masivamente los 54.000 test del banco de preguntas.

**Resiliencia Multi-Cloud (LiteLLM Fallback):**
1.  Intenta enviar a `Mistral`.
2.  Si da error 429, salta a `Gemini`.
3.  Si Gemini falla, salta a `Groq (Llama 3.3)`.

### 2. LiteLLM: Consideraciones

**Pegas:**
*   Añade una dependencia más.
*   Si OpenAI lanza funcionalidad revolucionaria, LiteLLM puede tardar en darle soporte.

**Otros Usos:**
*   Podemos sustituir todos los scripts dispersos en `opos-agents/` por una única llamada limpia de LiteLLM.

### 3. Separación Legal de Obsidian

**Ubicación de Herramientas:** Las herramientas van alojadas **EXCLUSIVAMENTE en el Backend de Python (Chandra)** en `chandra_tools.py`.

**El Vault Aparte:** El `.exe` que creará **solo incluirá tu Frontend en React y tu Backend en Python**. Obsidian es de terceros. El cliente final se baja tu App, y como extra le dirás: *"Bájate Obsidian gratis de su web oficial, y mete este .zip (tu Vault) dentro"*. Cero problemas legales.

### 4. TAURI: Usando TU propio Frontend React

Tauri cogerá tu carpeta `/frontend` y la compilará tal cual en un ejecutable ligerísimo de escritorio, junto a tu backend empaquetado (`chandra.exe` usando la arquitectura Sidecar). Cuando el opositor haga doble click, se levantará el servidor local y verá tu interfaz actual convertida en una app de escritorio nativa.

---

## 📅 PLAN DE FASES DE DESARROLLO

### FASE 2 · Chandra Robustecido (3-5 días)

#### 2.A · Nuevas manos (8-11):

*   🆕 `tool_generar_flashcards_anki` → genera MD con formato `::` compatible con obsidian-to-anki-plugin
*   🆕 `tool_generar_mermaid` → produce bloque Mermaid validado desde un tema
*   🆕 `tool_simulacro_test` → 10 preguntas test con solución y cita BOE verificada
*   🆕 `tool_resumir_nota` → lee una nota del vault, genera esquema CoT y la guarda como resumen_X.md

#### 2.B · Chain-of-Verification (CoVe) — PRIORIDAD ALTA

Tras la respuesta final, Chandra genera 3 preguntas internas de verificación ("¿el artículo citado existe? ¿la cuantía es correcta? ¿la fecha aplica a corte 04/03/2026?") y las responde antes de devolverla. Reduce alucinaciones ~40% en tareas legales.

#### 2.C · Few-shot calibración en system prompt

Incorporar los 3 ejemplos de Para_Dudas.md (IT días 4-15, jubilación 66a6m con 37 años, IPT vs IPA) directamente a CHANDRA_SYSTEM_PROMPT.

#### 2.D · Auto-RAG pre-respuesta

Antes de llamar a Mistral, el backend ejecuta `buscar_vault(query=user_msg, carpeta='wiki/trampas')` y inyecta las 3 trampas más relevantes como contexto extra.

#### 2.E · Self-consistency (OPCIONAL, caro)

Solo para preguntas marcadas confianza_baja: 2 llamadas con T=0.7 + voting de respuesta mayoritaria.

### FASE 3 · Fork BMO Chandra Edition (5-7 días)

Clonar https://github.com/longy2k/obsidian-bmo-chatbot (MIT). Features a añadir:

| Feature | Descripción |
|---------|-------------|
| Multi-chat | Sidebar con lista de conversaciones (guardar/cargar .md de BMO/History/) |
| Autocompletado @ | `@chandra_opos`, `@examinador`, `@bmo` → carga perfil al vuelo |
| Autocompletado / | `/flashcards`, `/simulacro`, `/caso_practico`, `/mermaid` → dispara plantilla + tool |
| Autocompletado * | `*ejecutar` → pasa bloque python a execute-code y devuelve output |
| Selector modelo inline | Dropdown abajo-izquierda [Mistral ▾] que cambia solo modelo sin tocar perfil |
| Context toggles | 3 botones junto al input: [Nota] [Vault] [Solo prompt] |

**Publicación:** obsidian-bmo-chandra-edition, misma licencia MIT.

### FASE 4 · Templates AI Generativas (2-3 días)

En `/templates/AI/` con Templater + llamadas a Chandra:

*   **T1_Caso_Practico.md** → input tema, output: hechos → análisis BOE → resultado + cita
*   **T2_Simulacro_10.md** → usa tool_simulacro_test
*   **T3_Flashcards_Anki.md** → usa tool_generar_flashcards_anki → export
*   **T4_Mermaid_Concepto.md** → usa tool_generar_mermaid
*   **T5_Mapa_Mental_Markmap.md** → bloque markmap + obsidian-mind-map
*   **T6_Esquema_Tema.md** → CoT: bullets → resumen → trampas

### FASE 5 · Repoblado del vault (7-10 días)

**Estructura wiki/temario/TEMA_XX/:**
*   Troceado + Muro de Abstracción (pseudonimizar academias DM/Cortes/Sara)

**Estructura wiki/preceptos/BOE-A-.../art_NNN.md:**
*   YAML (ley, rango, vigencia, materias, tags, neo4j_id)

**Estructura wiki/indices/:**
*   Generados por materia A-Z

**Script regenerador:**
*   Filtro PII + validación Mermaid/Markmap

**Sync Neo4j:**
*   Cada preceptos.md tiene neo4j_id que mapea al nodo Article

---

## 🔬 Mejores Prácticas LLM (Resumen)

| Técnica | ¿Vale la pena? | Cuándo usar |
|---------|----------------|-------------|
| Few-shot examples | ✅ Sí (fácil ROI) | En system prompt, 3-5 ejemplos calibrados |
| Chain-of-Thought | ✅ Sí | Ya implícito en tool-use iterativo. Reforzar con Thought: explícito |
| Chain-of-Verification (CoVe) | ⭐ PRIORIDAD | Reduce alucinaciones legales ~40%. Fase 2.B |
| Tree-of-Thoughts | ⚠️ Solo casos complejos | Encuadramiento dudoso, múltiples hipótesis. Coste O(n^k) |
| Self-consistency voting | ⚠️ Caro (2x API) | Solo confianza_baja |
| ReAct estructurado | ✅ Ya lo hacemos | Los tool_calls ya son Thought→Action→Observation |
| Auto-RAG previo | ⭐ Alto ROI | Fase 2.D. Inyectar trampas del vault antes del primer token |

---

## ❓ Decisiones Pendientes

*   ¿Clono ya BMO repo al workspace `/home/spas/obsidian-bmo-chatbot-fork/` para empezar Fase 3?
*   ¿Orden de fases? Recomendado: 1 → 2 → 4 → 3 → 5 (limpieza → Chandra robusto → templates usando tools existentes → fork BMO con todo estable → repoblado masivo)
*   ¿Copilot lo arreglamos (8000→8080) o lo dejamos roto mientras avanzamos con BMO?
*   ¿Borro ya la basura de vault (11 archivos + 3 carpetas) o prefieres hacerlo tú manualmente?
*   ¿Mantenemos MISTRAL_URL obsoleta o la limpio de .env.backend ya?

---

*Documento consolidado el 10/05/2026. Incluye ideas de sessiones previas de Antigravity AI + Spas (OPOSITAIA).*
