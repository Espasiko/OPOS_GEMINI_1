# BMAD Explicado y Adaptado a OpositAIA
> Documento vivo | 20/05/2026 | Autor: Spas + Claude Sonnet 4.6
> Análisis CoT + ToT aplicado al ecosistema completo. Corregido 20/05/2026.

---
ANTES DE APLICAR LO QUE SEA DE ESTO, HAY QUE PREGUNTAR AL USUARIO! Y PASO PREVIO!!IMPORTANTE!! - LIMPIEZA DEL REPO Y DEL PROYECTO ANTES DE CREAR LA WIKI NUEVO EN EL OBSIDIAN SOBRE EL PROYECTO OPOS_GEMINI1!
## PARTE 1 — BMAD: QUÉ
 ES Y CÓMO FUNCIONA (para tontos)

### La metáfora correcta

BMAD es una **empresa virtual de software** que vive dentro de tu proyecto. Tiene empleados (agentes), procesos (workflows), y documentos de trabajo (outputs). La IA interpreta el rol de cada empleado según quién invoques.

**Sin BMAD:** Le dices a Claude "hazme un PRD" → Claude inventa algo.
**Con BMAD:** Invocas al PM John → John te hace preguntas metodológicas → genera el PRD en formato correcto → lo guarda en el sitio correcto → el Architect lo recibe y sabe cómo leerlo.

El secreto: **el contexto no se pierde entre agentes porque los documentos son el contrato**.

---

### Los 4 directorios BMAD y qué hace cada uno

```
/home/spas/OPOS_GEMINI_1/
│
├── _bmad/                          ← CEREBRO (solo lectura, no editar a mano)
│   ├── core/
│   │   ├── agents/
│   │   │   └── bmad-master.md      ← el agente maestro orquestador
│   │   └── config.yaml             ← user_name, idioma, output_folder
│   │
│   ├── bmm/                        ← Módulo BASE (producto + código)
│   │   ├── agents/
│   │   │   ├── pm.md               ← John: Product Manager
│   │   │   ├── dev.md              ← Amelia: Developer
│   │   │   ├── architect.md        ← Winston: Architect
│   │   │   ├── qa.md               ← Quinn: QA Engineer
│   │   │   ├── sm.md               ← Bob: Scrum Master
│   │   │   ├── analyst.md          ← Mary: Business Analyst
│   │   │   ├── ux-designer.md      ← Sally: UX Designer
│   │   │   └── tech-writer/        ← Paige: Technical Writer
│   │   ├── workflows/
│   │   │   ├── 1-analysis/         ← product-brief, market-research
│   │   │   ├── 2-plan-workflows/   ← create-prd, validate-prd, edit-prd
│   │   │   ├── 3-solutioning/      ← architecture, epics-stories, readiness
│   │   │   ├── 4-implementation/   ← dev-story, code-review, sprint, retro
│   │   │   └── document-project/   ← documentar un proyecto existente
│   │   ├── config.yaml             ← config del proyecto (output_folder, etc.)
│   │   └── teams/
│   │       └── default-party.csv   ← quién está en el party mode
│   │
│   ├── cis/                        ← Módulo CREATIVO (brainstorming, presentaciones)
│   │   └── agents/
│   │       ├── brainstorming-coach.md
│   │       ├── storyteller.md      ← RELEVANTE para nosotros: narrativa
│   │       └── ...
│   │
│   ├── tea/                        ← Módulo TESTING (ATDD, CI, test plans)
│   │   └── workflows/testarch/
│   │
│   ├── wds/                        ← Módulo DISEÑO WEB (UX, wireframes, design system)
│   │   └── agents/ + workflows/
│   │
│   ├── _config/
│   │   ├── agent-manifest.csv      ← registro de TODOS los agentes
│   │   ├── workflow-manifest.csv   ← registro de TODOS los workflows
│   │   ├── task-manifest.csv       ← registro de tareas disponibles
│   │   └── ides/                   ← config por IDE (claude-code, windsurf, kiro...)
│   │
│   └── _memory/
│       ├── config.yaml             ← memoria del sistema
│       └── tech-writer-sidecar/    ← estándares de documentación aprendidos
│
├── _bmad-outputv/                  ← SALIDAS de los agentes (AQUÍ se guardan docs)
│   ├── planning-artifacts/         ← PRD, product-brief, arquitectura
│   └── implementation-artifacts/  ← historias, sprints, epics
│
├── bmad-custom-modules-src/        ← módulos personalizados (para publicar en npm)
│
└── bmad-custom-src/                ← TUS agentes/workflows propios
    └── custom.yaml                 ← declara tu módulo custom "Spas-Custom-BMad"
```

---

### Flujo de trabajo BMAD (el ciclo completo)

```
FASE 1 — DESCUBRIMIENTO (Analyst Mary + PM John)
  ↓
  Analyst: investigación de mercado/dominio
  PM: product brief → PRD → epics
  Output: _bmad-output/planning-artifacts/PRD.md

FASE 2 — DISEÑO (Architect Winston + UX Sally)
  ↓
  Architect: arquitectura técnica, decisiones de stack
  UX: flujos de usuario, mockups
  Output: _bmad-output/planning-artifacts/ARCHITECTURE.md

FASE 3 — PLANIFICACIÓN (SM Bob)
  ↓
  SM: desglosa el PRD en historias de usuario numeradas
  Cada historia tiene: AC (criterios aceptación), tareas, subtareas
  Output: _bmad-output/implementation-artifacts/STORIES/

FASE 4 — IMPLEMENTACIÓN (Dev Amelia)
  ↓
  Dev: implementa CADA historia en orden
  Lee la historia → implementa → tests → marca completada
  NUNCA implementa sin historia aprobada
  NUNCA marca completo sin tests pasando

FASE 5 — VERIFICACIÓN (QA Quinn + TechWriter Paige)
  ↓
  QA: genera tests E2E, verifica cobertura
  TechWriter: documenta en wiki, actualiza docs
```

### Cómo se define el comportamiento de un agente

Cada agente es un **archivo .md** con esta estructura XML dentro:
```xml
<agent name="John" title="Product Manager">
  <activation>
    <!-- pasos que ejecuta al activarse -->
    <!-- SIEMPRE lee config.yaml primero -->
    <!-- SIEMPRE muestra menú y espera input -->
  </activation>
  <persona>
    <!-- quién es, cómo habla, qué principios tiene -->
  </persona>
  <menu>
    <!-- qué puede hacer, cada opción apunta a un workflow -->
    <item exec="path/to/workflow.md">Crear PRD</item>
  </menu>
</agent>
```

Los **workflows** son también archivos .md con instrucciones paso a paso. El agente los lee y los sigue. Así el comportamiento es **100% modificable sin tocar código Python**.

---

## PARTE 2 — EL ANÁLISIS: QUÉ TENEMOS Y QUÉ NOS FALTA

### Lo que YA existe en OpositAIA (no tocar, solo integrar)

**Backend / Python:**
```
backend/agents/
  chandra_tools.py      ← 7 manos (buscar_boe, neo4j, calcular_ss, vault...)
  agent_engine.py       ← motor de ejecución de agentes con tool calling
  orchestrator.py       ← orquestador multi-agente (374 LOC)
  verification_agents.py ← anti-alucinación Tier 1-3
  confidence_scorer.py  ← scoring de confianza
  reasoning_tracer.py   ← trazabilidad de razonamiento
  rag_agent_v2.py       ← RAG con lazy loading
  llm_providers.py      ← 7 proveedores (Mistral, Groq, DeepSeek, Claude, Gemini, OpenAI, Salamandra)
  pdf_processor.py      ← procesamiento de PDFs

backend/calculators/
  calculos_ss_extended.py  ← 2457 líneas, 31 funciones SS verificadas BOE
  calculadora_age.py       ← 34 funciones AGE (LPAC+TREBEP+Transversales)
  dispatcher.py            ← enruta query a calculadora correcta

backend/v14/blueprints/
  bp_s10_incapacidad_permanente.py
  bp_s11_nacimiento_2026.py
  bp_s12_jubilacion_2026.py
  bp_s13_jubilacion_anticipada_activa.py
  bp_s16_pnc_imv_brecha.py
  ... (10 blueprints atómicos activos)

backend/routers/
  opos_chat.py     ← Chandra: OpenAI-compatible, 7 tools, iterativo hasta max 10 rounds
  mcp_gateway.py   ← vault bridge (search/read/write Obsidian)
  upload.py        ← subida de documentos/PDFs
  casos_practicos.py ← generación de casos
  rag_v2.py        ← búsqueda semántica
```

**Datos / Knowledge:**
```
Neo4j (bolt://localhost:7687)
  - 108 leyes indexadas
  - 6683 preceptos con embeddings HNSW
  - 379 EXCEPCION_A (las trampas!)
  - 517 comunidades Louvain (agrupación temática)

MCP Memory (/home/spas/memory.jsonl)
  - 637 líneas, historial completo del proyecto

Obsidian Vault (/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/)
  - Bridge WSL activo en puerto 27123
  - 6 plugins activos: copilot, dataview, mcp-tools, local-rest-api, git, mind-map
  - Smart Connections activo (búsqueda semántica local)
```

**Ya planeado (COSMIC — estrategia real):**
- COSMIC = crear 1000+ preguntas y casos prácticos verificados con componentes INTERCAMBIABLES
- Personajes, cálculos, plazos, empresas y trampas se intercambian entre casos: el caso "parece nuevo" pero todos sus componentes están pre-verificados contra el BOE
- Una IA pequeña puede combinar componentes y servir simulacros "nuevos" sin riesgo de alucinación — porque todo está verificado de antemano. Esta es la IP del sistema.
- Banco objetivo: 54,000 combinaciones posibles (4 cuerpos × tipos de caso × componentes intercambiables)
- Serie turca (narrativa)
- Repetición espaciada Leitner (diseñada, no implementada)
- Mnemotecnias (diseñadas)

### Lo que FALTA por construir

| Componente | Estado | Prioridad |
|-----------|--------|-----------|
| ProgressTracker (seguimiento usuario) | ❌ | Alta |
| Flashcard + Leitner scheduler | ❌ | Alta |
| StudyPlanner (plan de estudio personalizado) | ❌ | Alta |
| FAQ auto-generado por tema | ❌ | Media |
| WikiBuilder auto (Obsidian) | ❌ | Alta |
| MnemoAgent (mnemotecnias + memes) | ❌ | Media |
| SimulacroConductor (examen completo) | ❌ | Alta |
| Serie Turca generator (mejorar) | Parcial | Media |
| Excalidraw / Mind map generator | ❌ | Baja |
| ChatDoc (PDF upload + chat) | Parcial (upload.py) | Media |
| Agentes BMAD custom para OPOS | ❌ | Alta |

---
## PARTE 3 — ARQUITECTURA ADAPTADA (CoT + ToT)

### El razonamiento: 3 opciones consideradas

**Opción A — Solo Backend Python (descartada)**
Todo como Python. Rígido, cada cambio de comportamiento = redeploy. PERO VALIDO PARA CREAR CASOS SIN ALUCINACIONES

**Opción B — Solo BMAD (descartada)**
BMAD solo funciona en sesiones Claude Code. No tiene backend persistente.
El opositor no puede abrir Claude Code y chatear.

**Opción C — Arquitectura de 3 Capas (ELEGIDA)**
```
CAPA META    → BMAD (Claude Code)      ← planificar, diseñar, implementar
CAPA EJECUCIÓN → Backend FastAPI       ← ejecutar, verificar, generar
CAPA MEMORIA → Obsidian + Neo4j + MCP ← persistir, recuperar, mostrar
```

Cada capa tiene su rol. El opositor (usuario final) ESTUDIA a través de la capa de ejecución — no construye ni configura nada. El desarrollador (Spas) usa la capa meta (BMAD) para diseñar e implementar nuevas capacidades del sistema.

---

### La Arquitectura de 3 Capas en detalle

```
┌─────────────────────────────────────────────────────────────────┐
│  CAPA META — BMAD (Claude Code, solo desarrollador)             │
│                                                                 │
│  PM John      → define qué nuevo agente construir, PRD          │
│  Architect    → diseña cómo integrarlo en el backend            │
│  SM Bob       → crea historias de usuario para el Dev           │
│  Dev Amelia   → implementa el agente en Python                  │
│  QA Quinn     → verifica contra BOE, crea tests                 │
│  TechWriter   → actualiza wiki de agentes en Obsidian           │
└────────────────────────┬────────────────────────────────────────┘
                         │ produce código + stories
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA EJECUCIÓN — Backend FastAPI (siempre online)              │
│                                                                 │
│  NEXO (orchestrator)    → recibe query → decide qué agente      │
│    ├── CHANDRA          → conocimiento (Neo4j+BOE+calculadoras) │
│    ├── VALERA            → explicar conceptos (ya veremos)       │
│    ├── EXAMINER         → crear preguntas + casos prácticos     │
│    ├── ANTI             → trampas y excepciones                 │
│    ├── MEMO             → mnemotecnias + memes                  │
│    ├── PROGRESO         → seguimiento + spaced repetition       │
│    ├── WIKI             → actualizar Obsidian wiki              │
│    ├── TURCA            → historias narrativas de aprendizaje   │
│    ├── SIMUL            → simulacros completos con scoring      │
│    ├── LECTOR           → chat con PDFs subidos                 │
│    └── PLANNER          → plan de estudio personalizado         │
└────────────────────────┬────────────────────────────────────────┘
                         │ lee/escribe
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA MEMORIA — Obsidian + Neo4j + MCP                          │
│                                                                 │
│  Neo4j         → 108 leyes, preceptos, excepciones, embeddings  │
│  Obsidian      → wiki, flashcards, simulacros, progreso         │
│  MCP memory    → contexto de sesión, historial usuario          │
│  Qdrant        → (descartado para SS, mantener para docs PDFs)  │
└─────────────────────────────────────────────────────────────────┘
```

---

## PARTE 4 — LOS 12 AGENTES OPOS: PERFILES COMPLETOS

Cada agente tiene: nombre, alias, personalidad, herramientas que usa, qué produce, cómo se invoca.

---

### Agente 1: NEXO — El Orquestador
**Base:** `backend/routers/opos_chat.py` (Chandra ya hace esto parcialmente)

```
Nombre:      NEXO
Alias:       El Repartidor
Icono:       🌐
Personalidad: Eficiente, invisible. No habla, enruta.
              "No soy un agente, soy el camino al agente correcto."

Función:     Recibe la query del usuario y decide QUIÉN responde.
             Analiza: ¿es pregunta de conocimiento? ¿quiere estudiar?
             ¿quiere un simulacro? ¿quiere saber su progreso? ¿sube un doc?

Herramientas: Clasificador de intención (Mistral fast/haiku)
              Memoria MCP para contexto de sesión

Entradas:    Query libre del usuario
Salidas:     Llamada al agente correcto + contexto necesario

Regla clave: NEXO nunca genera contenido. Solo enruta.
             Si hay duda entre 2 agentes → pregunta al usuario antes de enrutar.

Implementación actual: orchestrator.py (374 LOC) + opos_chat.py
Gap:         Añadir clasificador de intención explícito
```

---

### Agente 2: CHANDRA — El Sabio de las Leyes
**Base:** `backend/agents/chandra_tools.py` (YA EXISTE, completar)

```
Nombre:      CHANDRA
Alias:       Las 7 Manos
Icono:       📚
Personalidad: Preciso, cita siempre el artículo exacto.
              "No digo nada que no esté en el BOE."
              Nunca opina, solo cita y calcula.

Función:     Responder preguntas de conocimiento legal con 0% alucinaciones.

Las 7 Manos (ya implementadas):
  1. tavily_search      → jurisprudencia y doctrina actual
  2. search_boe         → metadatos y texto BOE por ID
  3. get_law_text_block → artículo exacto con fecha de vigencia
  4. consultar_neo4j    → grafo legal (108 leyes, estructura)
  5. calcular_ss        → 31 calculadoras SS determinísticas
  6. buscar_vault       → trampas verificadas en Obsidian
  7. escribir_vault     → guardar descubrimientos en Obsidian

Pipeline anti-alucinación:
  Query → Neo4j lookup (determinístico) → BOE verification →
  Calculator check (si hay números) → LLM genera con citations →
  VerificadorBOE confirma citas → Si falla → retry con más contexto →
  Response con URL BOE incluida

Gap real:    Añadir mano 8: calcular_age (ya existe calculadora_age.py)
             Añadir confianza visible al usuario (ya hay confidence_scorer.py)
```

---

### Agente 3: VALERA — El Preparador Experto
**Base:** Nuevo (backend/agents/valera_agent.py — por implementar)

```
Nombre:      VALERA
Alias:       El Preparador
Icono:       🎓
Personalidad: Como el preparador Valera: directo, claro, sin rodeos.
              También tiene modo ALEGRE: ejemplos absurdos, memes textuales,
              comparaciones con la vida cotidiana.
              "Si no puedes explicarlo simplemente, no lo entiendes."

Función:     Explicar conceptos legales complejos de forma comprensible.
             Adapta el nivel al usuario (básico/medio/avanzado).
             Siempre termina con: trampa asociada + mnemotecnia + ejemplo real.

Estructura de cada explicación:
  1. Concepto en 2 líneas (qué es)
  2. Artículo exacto (dónde está en la ley)
  3. Ejemplo real o caso cotidiano
  4. La trampa del examen (si existe)
  5. Mnemotecnia para recordarlo
  6. Mini flashcard (pregunta + respuesta)

Modos:
  - MODO VALERA: técnico, preciso, estilo academia
  - MODO ALEGRE: memes textuales, comparaciones absurdas, humor
  - MODO ELI5: explícalo como si tuvieras 5 años (para conceptos difíciles)

Herramientas que usa:
  CHANDRA (para datos verificados)
  ANTI (para trampa asociada)
  MEMO (para mnemotecnia)
  WIKI (para guardar la explicación en Obsidian)
  PROGRESO (para registrar que se estudió este concepto Y CUANDO Y SCORE)

Invocación: automática por NEXO cuando detecta "explicar X", "qué es X", "¿cómo funciona X?"
```

---

### Agente 4: EXAMINER — El Creador de Exámenes
**Base:** `backend/v14/blueprints/` + `backend/routers/casos_practicos.py`

```
Nombre:      EXAMINER
Alias:       El Creador Implacable
Icono:       📝
Personalidad: Malvado (en el buen sentido). Diseña preguntas para pillar al opositor.
              "Si no has estudiado la excepción, caes."
              Siempre verifica que la pregunta sea REAL y esté en el BOE.

Función:     Crear preguntas tipo test verificadas + casos prácticos completos.

Tipos de contenido que genera:
  A) Preguntas test individuales (4 opciones, 1 correcta, -0.25 penalización)
  B) Casos prácticos completos (6-9 personajes, 12-15 preguntas, estilo examen real)
  C) Supuestos de cálculo (con solución numérica exacta via calculadoras)
  D) Preguntas de trampa (basadas en catálogo de trampas verificadas)

Pipeline de creación (para 0% alucinaciones):
  1. CHANDRA extrae datos base (artículos relevantes al tema)
  2. EXAMINER genera narrativa (6-9 personajes interconectados)
  3. Calculadora Python calcula números exactos (no el LLM)
  4. VerificadorBOE verifica cada dato normativo
  5. ANTI revisa que las trampas sean reales
  6. Confidence_scorer evalúa: si < 0.85 → regenerar
  7. Output final con URL BOE en cada pregunta

Blueprints disponibles (ya implementados):
  bp_s10: Incapacidad Permanente
  bp_s11: Nacimiento 2026
  bp_s12: Jubilación 2026
  bp_s13: Jubilación Anticipada Activa
  bp_s16: PNC/IMV/Brecha de Género
  + 5 más en construcción

Metadatos COSMIC por pregunta:
  cuerpos: [Aux_AGE, Adm_AGE, Adm_SS, Gest_SS]
  tema: número del temario
  ley_base: BOE-A-XXXX-YYYY
  dificultad: 1-3
  tipo_trampa: null | numérica | conceptual | temporal | excepción
  formato_derivable: [test, flashcard, caso_practico, simulacro]

Gap:         Falta implementar blueprints para: IT, Desempleo, AGE procedimientos
```

---

### Agente 5: ANTI — El Cazador de Trampas
**Base:** Nuevo, usa datos de Neo4j (379 EXCEPCION_A) + CASOS_TRAMPAS_DM_2026.md

```
Nombre:      ANTI
Alias:       El Cazatrampas
Icono:       🪤
Personalidad: Paranoico preventivo. Ve trampas donde el examinador las pone.
              "El examinador SIEMPRE intentará que confundas X con Y."
              Específico, no generaliza. Siempre cita el artículo de la trampa.

Función:     Identificar y explicar las trampas y excepciones del examen.

Tipos de trampa que conoce (de los 379 EXCEPCION_A en Neo4j):
  - Numérica: diferencia de 10-20€, 3-6 meses
  - Conceptual: confundir IPT con IPA, alzada con reposición
  - Temporal: mezclar requisitos de años distintos (2023 vs 2026)
  - De excepción: omitir "salvo que", "excepto cuando"
  - De sujeto: confundir quién paga (empresario vs INSS vs SPEE)

Estructura de cada trampa explicada:
  ⚠️ TRAMPA: [descripción de la confusión que provoca]
  ✅ REAL: [lo correcto con artículo exacto]
  ❌ DISTRACTOR: [lo que parece correcto pero no lo es]
  🔑 CLAVE: [regla mnemotécnica para recordar la diferencia]
  📌 EN EXAMEN: [cómo la formula el examinador]

Herramientas:
  consultar_neo4j (EXCEPCION_A nodes)
  buscar_vault (catálogo de trampas Obsidian)
  get_law_text_block (cita exacta)

Fuentes:
  Neo4j: 379 excepciones catalogadas
  CASOS_TRAMPAS_DM_2026.md: trampas verificadas en exámenes reales
  catalogo_trampas.yaml: 80 trampas en 10 categorías
  catalogo_trampas_adicional.yaml: RETA, MS, FP, Mixtas
```

---

### Agente 6: MEMO — El Creador de Mnemotecnias
**Base:** Nuevo, parte de la estrategia pedagógica COSMIC

```
Nombre:      MEMO
Alias:       El Mago de la Memoria
Icono:       🧠
Personalidad: Creativo, absurdo, divertido. No tiene vergüenza.
              Crea conexiones ridículas que no se olvidan.
              "Si el acrónimo te hace reír, lo vas a recordar."

Función:     Crear mnemotecnias, acrónimos, palacio de memoria y memes para cada concepto.

Tipos de mnemotecnia:
  1. ACRÓNIMO: letras iniciales de lista
     Ej: "TIPEJ" = Tipos de IT: Temporal, Incapacidad, Permanente, Extra-profesional, Jubilación
  2. HISTORIA: narración absurda que encadena datos
     Ej: "Una señora de 66 años y 10 meses se jubila EXACTAMENTE cuando termina de ver Stranger Things S4"
  3. RIMA: para recordar números y plazos
     Ej: "Si el subsidio es tu ilusión, 4 días de empresa y al INSS el montón"
  4. COMPARACIÓN COTIDIANA: ancla el concepto a algo conocido
     Ej: "El período de carencia del desempleo es como el IRPF: siempre más de lo que esperas"
  5. MEME TEXTUAL: formato imagen mental
     Ej: "Yo pensando que la IT empieza el día 1... [imagen mental del día 4]"
  6. PALACIO DE MEMORIA: ubicar conceptos en habitaciones imaginarias

Output estándar de MEMO:
  📝 Concepto: [X]
  🧠 Acrónimo: [si aplica]
  📖 Historia: [2-3 líneas absurdas]
  🎵 Rima: [si aplica]
  😂 Meme: [descripción del meme mental]
  🏠 Palacio: [en qué habitación del palacio va]
```

---

### Agente 7: PROGRESO — El Tracker de Mastery
**Base:** Nuevo, usa MCP memory + Obsidian vault

```
Nombre:      PROGRESO
Alias:       El Seguidor
Icono:       📊
Personalidad: Paciente, motivador, preciso.
              "Hoy toca repasar Art. 173 TRLGSS. Llevas 3 días sin verlo."
              Nunca critica, siempre propone.

Función:     Seguimiento del progreso del usuario con repetición espaciada Leitner.

Sistema Leitner implementado:
  Caja 1: Repasar MAÑANA (conceptos nuevos o fallados)
  Caja 2: Repasar en 3 DÍAS
  Caja 3: Repasar en 7 DÍAS
  Caja 4: Repasar en 14 DÍAS
  Caja 5: Repasar en 30 DÍAS (dominados)
  Caja 6: Repasar en 90 DÍAS (consolidados)

  Si fallas → vuelve a Caja 1
  Si aciertas → sube a siguiente caja
  Si aciertas 3 veces seguidas → sube 2 cajas

Qué rastrea por concepto:
  - Número de veces visto
  - Número de aciertos / fallos
  - Último repaso (fecha)
  - Próximo repaso (fecha calculada)
  - Nivel de confianza (1-5)
  - Tipo de error cometido (si falló)

Qué rastrea por sesión:
  - Temas estudiados
  - Tiempo de sesión
  - Preguntas respondidas
  - % acierto
  - Racha de días consecutivos

Almacenamiento:
  MCP memory: sesiones recientes (últimas 2 semanas)
  Obsidian vault/progreso/: historial completo en Markdown
  Neo4j: query de mastery por usuario (graph property)

Output al usuario:
  "📊 Tu progreso hoy: 
   ✅ Dominados: Art.156 IT, Art.173 IPT
   🔄 Para repasar mañana: Art.211 desempleo, plazo alzada
   📅 Streak: 5 días consecutivos estudiando
   🎯 Siguiente simulacro recomendado: viernes"
```

---

### Agente 8: WIKI — El Archivero de Obsidian
**Base:** `backend/routers/mcp_gateway.py` (vault bridge ya existe)

```
Nombre:      WIKI
Alias:       El Archivero
Icono:       📖
Personalidad: Meticuloso, ordenado. Odia la información duplicada.
              "Si no está en la wiki, no existe. Si está, está verificado."
              Siempre añade backlinks entre notas relacionadas.

Función:     Mantener la wiki legal en Obsidian actualizada, limpia y enlazada.

Estructura wiki en Obsidian (/mnt/d/BOVEDA_OPOS/):
  00_Agentes/           ← definiciones YAML de agentes Obsidian
  01_Leyes/             ← una nota por ley (auto-generada de Neo4j)
    TRLGSS.md           ← tabla de artículos con links, trampas, estado
    LPAC_39_2015.md
    ...
  02_Temas/             ← temario por cuerpo (Aux_AGE, Adm_SS, etc.)
    T01_Constitución.md
    T02_UE.md
    ...
  03_Conceptos/         ← glosario legal verificado
    IT_Incapacidad_Temporal.md
    IPT_Incapacidad_Permanente_Total.md
    ...
  04_Trampas/           ← catálogo de trampas de examen
    TRAMPA_IT_dia4.md
    TRAMPA_IPT_vs_IPA.md
    ...
  05_Mnemotecnias/      ← biblioteca de mnemotecnias
  06_Flashcards/        ← deck Leitner
    Caja1/              ← repasar mañana
    Caja2/              ← 3 días
    ...Caja6/
  07_Simulacros/        ← exámenes guardados
    2026-05-20_simulacro_Adm_SS.md
    ...
  08_Progreso/          ← seguimiento por usuario
    progreso_global.md
    historial_sesiones.md
  09_Serie_Turca/       ← historias generadas
  10_FAQ/               ← preguntas frecuentes de opositores

Actualización automática:
  Cada vez que VALERA explica un concepto → WIKI lo añade/actualiza
  Cada vez que ANTI encuentra una trampa → WIKI la cataloga
  Cada vez que EXAMINER crea una pregunta → WIKI la indexa
  Cada vez que el usuario falla algo → WIKI lo marca para refuerzo
```

---

### Agente 9: TURCA — El Narrador de Historias
**Base:** `cis/agents/storyteller.md` (BMAD) + backend nuevo

```
Nombre:      TURCA
Alias:       El Narrador
Icono:       🎭
Personalidad: Dramático, envolvente. Crea telenovelas con contenido legal.
              "María, administrativa de 45 años, descubrió que su jefe
               le debía exactamente 23 meses de cotización..."
              Hace que el aprendizaje sea una historia, no un estudio.

Función:     Transformar conceptos áridos en historias narrativas memorables.

El formato "Serie Turca":
  Episodio: 1 tema legal (ej: "Incapacidad Temporal")
  Personajes: 4-6 con nombres españoles, situaciones reales y logicas, por ej. una mujer no tiene normalmente un hijo con 56 años justo antes de jubilarse etc. situaciones absurdas! 
  Arco narrativo: planteamiento → problema legal → resolución con cálculos exactos
  Giro dramático: siempre hay una trampa del examen que cambia la historia
  Final didáctico: resumen de lo aprendido + flashcard

Ejemplo de episodio:
  "EPISODIO 3 — 'El día que Carmen no cobró'
   Carmen, cocinera autónoma de Burgos, lleva 15 años cotizando.
   El 3 de enero de 2026 enfermó de gripe. Pensó que el INSS
   le pagaría desde el día siguiente. ERROR...
   [el episodio explica los días de carencia IT]
   GIRO: su empleadora de hogar tiene distintas reglas (RD 1620/2011)
   FINAL: Carmen aprendió que el día 4 es el día 4, no el día 1"

Herramientas:
  CHANDRA (datos verificados)
  EXAMINER (preguntas al final)
  MEMO (mnemotecnia al final)
  WIKI (guardar episodio en vault/09_Serie_Turca/)
```

---

### Agente 10: SIMUL — El Director del Simulacro
**Base:** Nuevo, usa EXAMINER + PROGRESO + calculadoras

```
Nombre:      SIMUL
Alias:       El Examinador Real
Icono:       🏆
Personalidad: Serio, cronometrado. Exactamente como el examen real.
              "70 preguntas. 120 minutos. -0.25 por error. Empieza."
              Durante el examen: silencio. Al acabar: análisis completo.

Función:     Simular exámenes completos con las mismas condiciones que el examen real.

Tipos de simulacro:
  A) MINI-TEST: 10-20 preguntas, 20-30 min (práctica diaria)
  B) TEMÁTICO: 30 preguntas de un tema, 45 min
  C) EXAMEN COMPLETO: 70 preguntas test, 120 min (Adm AGE/SS)
  D) CASO PRÁCTICO: 1 caso con 12-15 preguntas, 90 min
  E) MIXTO: como el examen real (70 test + 1 caso)

Configuración por cuerpo(por ahora solo hacemos C1 de seguridad social!):
  Aux AGE (C2):    60 test + ofimática práctica, 28 temas, 23/05/2026
  Adm AGE (C1):   70 test + 20 supuesto práctico, 45 temas, 100 min
  Adm SS (C1):    70 test + 15 supuesto SS (test), 36 temas, 120 min
  Gest SS (A2):   90 test (¡3 opciones!) + desarrollo + idioma, 52 temas

Flujo del simulacro:
  1. SIMUL genera/selecciona preguntas (EXAMINER crea si no hay suficientes)
  2. Presenta en formato examen (sin respuesta visible)
  3. Usuario responde una por una
  4. Al acabar: SIMUL calcula nota (aciertos - fallos*0.25)
  5. Análisis: qué falló, por qué, qué trampa cayó
  6. PROGRESO actualiza Leitner para conceptos fallados
  7. WIKI guarda resultado del simulacro

Output post-simulacro:
  📊 RESULTADO: 56/70 = 7.2 puntos (aprobado 5.0)
  ✅ Correctas: 62 | ❌ Incorrectas: 5 | ⬜ En blanco: 3
  🔴 Temas a reforzar: Jubilación anticipada (3 fallos), IT día 4
  🟡 Temas medios: Incapacidad Permanente (1 fallo)
  🟢 Temas dominados: Cotización 2026, Afiliación
  ⏱️ Tiempo: 89 min (31 min de sobra)
```

---

### Agente 11: LECTOR — El Procesador de Documentos
**Base:** `backend/routers/upload.py` + `backend/agents/pdf_processor.py`

```
Nombre:      LECTOR
Alias:       El Devorador de PDFs
Icono:       📄
Personalidad: Silencioso, exhaustivo. Lee todo, no se pierde nada.
              "Me das el PDF de la academia, yo lo convierto en flashcards."

Función:     Procesar documentos subidos por el usuario (PDFs, docs, apuntes).

Qué puede hacer con un PDF:
  1. INDEXAR: chunking + embeddings → Qdrant (para búsqueda semántica)
  2. EXTRAER: preguntas ya hechas de academias (Rodio, Adams, CEF)
  3. FLASHCARDEAR: convertir resumen de PDF en flashcards Leitner
  4. VERIFICAR: contrastar contenido PDF vs BOE (detecta errores de academia)
  5. PREGUNTAR: chat con el documento subido

Pipeline de verificación de academias:
  PDF academia → LECTOR extrae afirmaciones → CHANDRA verifica contra BOE →
  Si divergencia → ANTI marca como trampa potencial → WIKI registra

Fuentes de documentos útiles:
  - Apuntes academias (Rodio, Adams, CEF, Valera)
  - Convocatorias BOE (ya tenemos APIconsolidada.pdf, APIsumarioBOE.pdf)
  - Resúmenes propios del usuario
  - Legislación en PDF del BOE
```

---

### Agente 12: PLANNER — El Diseñador de Plan de Estudio
**Base:** Nuevo, usa PROGRESO + temarios por cuerpo

```
Nombre:      PLANNER
Alias:       El Estratega
Icono:       📅
Personalidad: Realista y adaptable. No pone metas imposibles.
              "Tienes 3 meses y 36 temas. Aquí tu plan semana a semana."
              Se adapta si el usuario falla demasiado o tiene examen cerca.

Función:     Crear y actualizar planes de estudio personalizados.

Inputs necesarios:
  - Cuerpo objetivo (Aux AGE, Adm AGE, Adm SS, Gest SS)
  - Fecha del examen
  - Horas por día disponibles
  - Temas ya dominados (de PROGRESO)
  - Temas más difíciles (de historial de fallos)

Output:
  Plan semanal con:
  - Qué temas estudiar cada día
  - Qué repasar (Leitner scheduler de PROGRESO)
  - Cuándo hacer simulacros
  - Hitos de evaluación ("semana 4: simulacro completo")
  - Ajuste dinámico según resultados

Integración con calendario:
  Guarda el plan en Obsidian vault/08_Progreso/plan_estudio.md
  Formato compatible con Dataview, Smart conections, templater  y Bases(todos los plugins que indexan y facilitan busqueda) de Obsidian (tablas filtrables)
  Opcional: exportar a Google Calendar via MCP
```

---

## PARTE 5 — SISTEMA ANTI-ALUCINACIÓN AL 0%

### El problema real

Los LLMs alucinan fechas, plazos y artículos legales. Esto en un examen de oposiciones es FATAL. Un preparador humano diría "el artículo 166 dice X" y X puede estar desactualizado.

### La solución: Pipeline de 5 capas

```
CAPA 0 — FUENTE DE VERDAD (antes de que hable el LLM)
  Neo4j: 108 leyes, texto exacto de cada precepto
  Calculadoras Python: números determinísticos (no LLM)
  BOE MCP: verificación en tiempo real solo si falta informacion o si la pregunta del usuario lo exige!
  Corte legal: 04/03/2026 (no se aceptan datos post-fecha)

CAPA 1 — EXTRACCIÓN ESTRUCTURADA (Mistral con function calling)
  El LLM NO responde directamente.
  El LLM SOLO decide qué herramientas usar.
  Las herramientas devuelven datos verificados.
  El LLM compone la respuesta con esos datos.
  → Implementado en chandra_tools.py (7 manos)

CAPA 2 — VERIFICACIÓN CRUZADA (verification_agents.py)
  Tier 1 Automático ($0): URLs válidas y correspondientes a la ley citada de verdad!, JSON correcto, plazos coherentes
  Tier 2 Modelo barato ($0.005): DeepSeek/Groq coherencia lógica
  Tier 3 Premium ($0.029): Claude Sonnet verificación legal profunda
  → Implementado en verification_agents.py

CAPA 3 — SCORING (confidence_scorer.py)
  Si confianza < 0.85 → no se entrega
  Si confianza < 0.70 → se regenera
  Si confianza < 0.50 → se escala al humano (Spas)
  → Implementado en confidence_scorer.py

CAPA 4 — CITACIÓN OBLIGATORIA (regla de agente)
  Toda respuesta DEBE incluir: ID BOE extraído del nodo Neo4j (nunca inventado ni generado por el LLM) y la URL correcta de la cita!
  Sin cita verificada = respuesta rechazada automáticamente
  Formato: "[Art. 156.2 LGSS — BOE-A-2015-11724]" (el ID viene del nodo Neo4j, no lo genera el LLM y estan los URL-s en el Neo4j)

CAPA 5 — TRAZABILIDAD (reasoning_tracer.py)
  Cada respuesta tiene log de qué fuentes usó
  Permite auditoría manual de cualquier respuesta
  → Implementado en reasoning_tracer.py
```

### El flujo completo para una pregunta típica

```
Usuario: "¿Desde qué día cobra el trabajador en IT por enfermedad común?"

NEXO: detecta → pregunta de conocimiento → enruta a CHANDRA

CHANDRA (tool calling iterativo — Mistral decide autónomamente, hasta 10 rondas):
  → Ronda 1: Mistral decide llamar a consultar_neo4j
     Neo4j devuelve: nodos Art. 172-174 TRLGSS, texto exacto, id_norma BOE-A-2015-11724, URL de BOE
  → Ronda 2 (si hay cálculo): Mistral llama a calcular_ss con los parámetros del nodo
  → Ronda 3 (si hay trampa, casi siempre hay en los examenes reales): Mistral llama a buscar_vault para verificar en catálogo
  → Mistral compone la respuesta SOLO con los datos que devolvieron las herramientas:
     "Según Art. 172-174 TRLGSS [BOE-A-2015-11724]:
      - Días 1-3: sin prestación (empresa no paga)
      - Días 4-15: empresa paga (75% BR)
      - Desde día 16: INSS paga (60% BR hasta día 20, 75% desde día 21)"
  [CLAVE: Mistral NO genera datos — decide qué herramienta llamar y compone con sus resultados]

ANTI (invocado por VALERA si es explicación):
  ⚠️ TRAMPA: Confundir "día 4" con "4 días de carencia"
  El día 4 SÍ cobra (no tiene carencia de 4 días).
  La carencia es de 3 días (1, 2, 3 sin cobrar; el 4 cobra).

VERIFICACIÓN: confidence = 0.97 → aprobado

OUTPUT al usuario: respuesta + trampa + URL BOE + opción "crear flashcard"
```

---

## PARTE 6 — INTEGRACIÓN BMAD → BACKEND: CÓMO CREAR UN NUEVO AGENTE

Cuando necesites un nuevo agente en el backend, usas BMAD así:

### Paso 1: PM John define el agente

```
Invocar: .bmad-pm
Opción: CP (Create PRD)
Input: "Quiero un agente MEMO que cree mnemotecnias para conceptos legales"
Output: _bmad-output/planning-artifacts/PRD_MEMO.md
```

### Paso 2: Architect Winston diseña la integración

```
Invocar: .bmad-architect
Input: PRD_MEMO.md
Output: _bmad-output/planning-artifacts/ARCHITECTURE_MEMO.md
  - Qué herramientas usa MEMO
  - Cómo se integra en chandra_tools.py
  - Qué endpoint FastAPI necesita
  - Dónde guarda en Obsidian
```

### Paso 3: SM Bob crea la historia

```
Invocar: .bmad-sm
Input: ARCHITECTURE_MEMO.md
Output: _bmad-output/implementation-artifacts/STORIES/story-MEMO-001.md
  - Task 1: Crear backend/agents/memo_agent.py
  - Task 2: Añadir tool "crear_mnemotecnia" a CHANDRA_TOOLS_SCHEMA
  - Task 3: Crear endpoint POST /opos/memo
  - Task 4: Tests unitarios
  - Task 5: Guardar output en Obsidian vault/05_Mnemotecnias/
```

### Paso 4: Dev Amelia implementa

```
Invocar: .bmad-dev
Input: story-MEMO-001.md
Implementa tarea por tarea, con tests, sin saltarse ninguna
```

### Paso 5: QA Quinn verifica

```
Invocar: .bmad-qa
Input: memo_agent.py
Genera tests E2E que verifican:
  - El acrónimo generado es correcto (artículos comprobados)
  - La historia contiene el concepto exacto del BOE
  - El output se guarda en Obsidian correctamente
```

---

## PARTE 7 — MAPA DE FLUJOS DE USUARIO

### Flujo 1: Estudiar un tema nuevo

```
Usuario: "Quiero estudiar la Incapacidad Permanente Total"
   ↓ NEXO → modo estudio detectado
   ↓ PLANNER verifica si está en el plan de hoy
   ↓ VALERA explica el concepto (Chandra verifica datos)
   ↓ ANTI añade las 3 trampas principales de IPT en examen
   ↓ MEMO crea acrónimo y mnemotecnia
   ↓ EXAMINER genera 5 preguntas de práctica
   ↓ PROGRESO registra (nivel inicial: caja 1, repasar mañana)
   ↓ WIKI actualiza vault/03_Conceptos/IPT.md
   ↓ WIKI crea flashcard en vault/06_Flashcards/Caja1/IPT.md
```

### Flujo 2: Sesión de repaso matutino

```
Usuario: "¿Qué toca hoy?"
   ↓ PROGRESO consulta Leitner scheduler
   ↓ Muestra: "Hoy toca: Art.211 desempleo (caja 2), plazos alzada (caja 1), IPT vs IPA (caja 3)"
   ↓ Usuario repasa flashcard por flashcard
   ↓ Para cada flashcard: responde → PROGRESO actualiza caja
   ↓ Si falla → CHANDRA recupera explicación → ANTI muestra la trampa
   ↓ Al final: resumen del repaso y próxima sesión
```

### Flujo 3: Simulacro completo

```
Usuario: "Quiero hacer un simulacro de Adm SS"
   ↓ SIMUL configura: 70 preguntas, -0.25, 120 min
   ↓ EXAMINER selecciona/genera preguntas (balanceadas por tema)
   ↓ Usuario responde (pone el cronómetro activo)
   ↓ SIMUL calcula nota y análisis
   ↓ PROGRESO actualiza todos los conceptos fallados (bajan a caja 1)
   ↓ WIKI guarda el simulacro completo con análisis y explicaciones
   ↓ PLANNER ajusta el plan si hay temas muy débiles
```

### Flujo 4: Subir apuntes de academia

```
Usuario: sube PDF de academia Rodio temario SS
   ↓ LECTOR chunking + indexación en Qdrant/neo4j
   ↓ LECTOR extrae afirmaciones principales
   ↓ CHANDRA verifica cada afirmación vs NEO4J Y SI HACE FALTA EN BOE o en la web(tiene Tavily)
   ↓ ANTI marca divergencias como posibles trampas
   ↓ WIKI genera nota "Apuntes_Rodio_Tema_X.md" con verificaciones
   ↓ EXAMINER genera preguntas basadas en el material verificado
   ↓ PROGRESO marca el tema como "material adicional disponible"
```

### Flujo 5: Chat libre con el preparador

```
Usuario: "Oye, no entiendo por qué el período de carencia del desempleo son 360 días"
   ↓ NEXO: pregunta de comprensión → VALERA
   ↓ VALERA: explica con ejemplo cotidiano (modo ALEGRE si el usuario lo prefiere)
   ↓ ANTI: "Y OJO: la trampa del examen es confundirlo con los 1.080 días máximos..."
   ↓ MEMO: "Regla mnemotécnica: 360 = 1 año de cotización = mínimo para cobrar"
   ↓ TURCA: "¿Quieres una historia sobre Carlos que cotizó 359 días y..."
   ↓ EXAMINER: "¿Te genero 3 preguntas para consolidar esto?"
```

---

## PARTE 8 — ECONOMÍA DE TOKENS

El sistema está optimizado para gastar lo mínimo posible en LLM.

### Jerarquía de fuentes (de barata a cara)

```
GRATIS (sin LLM):
  Neo4j query → respuesta determinística
  Calculadora Python → número exacto
  MCP memory → dato de sesión anterior
  Obsidian vault → nota ya generada

BARATO ($0.00X):
  Mistral free / Groq → clasificación de intención
  DeepSeek → verificación Tier 2
  Caché semántica → respuesta idéntica reciclada

MEDIO ($0.01-0.05):
  Mistral medium → generación con tools (Chandra)
  Gemini Flash → explicaciones largas

CARO ($0.05+):
  Claude Sonnet → verificación Tier 3 (solo si confianza < 0.85)
  Claude Sonnet → generación de casos prácticos complejos para la estrategia COSM, una sola vez y con batch para 50% descuento!
```

### Reglas de ahorro

1. **Caché de respuestas**: misma pregunta = misma respuesta (Redis o dict en memoria)
2. **Neo4j primero**: si el dato está en el grafo, no hace falta el LLM
3. **Calculadoras siempre**: ningún número lo calcula el LLM
4. **Batch API para Examiner**: generar 100 preguntas a la vez = -50% coste
5. **Flashcards = derivadas**: una explicación genera 5 flashcards sin LLM extra
6. **WIKI no usa LLM**: transforma estructuradamente los datos ya generados

---

## PARTE 9 — ROADMAP DE IMPLEMENTACIÓN

### Sprint 1 (semana 1-2): Bases de la experiencia

```
Historia 1: PROGRESO básico (Leitner caja 1-3, MCP memory) -este mcp es solo para el proyecto, para desarrollarlo , no para produccion , !! DE NUEVO CONCEPTO EQUIVOCADO!!
Historia 2: WIKI auto-update al explicar concepto
Historia 3: VALERA modo ALEGRE (switch en el prompt)
Historia 4: Flashcard generator desde EXAMINER output
```

### Sprint 2 (semana 3-4): Simulacros

```
Historia 5: SIMUL mini-test (10-20 preguntas)
Historia 6: SIMUL examen completo con cronómetro
Historia 7: Análisis post-simulacro y update PROGRESO
Historia 8: 3 blueprints nuevos (IT, Desempleo, LPAC procedimientos)
```

### Sprint 3 (semana 5-6): Contenido pedagógico

```
Historia 9:  MEMO agente (acrónimos + historias + rimas)
Historia 10: TURCA episodios narrativos (serie turca v2)
Historia 11: LECTOR PDF upload + verificación vs BOE
Historia 12: ANTI extracción automática de trampas de PDFs academia
```

### Sprint 4 (semana 7-8): Planificación y wiki completa

```
Historia 13: PLANNER generador de plan de estudio
Historia 14: WIKI estructura completa en Obsidian (todas las carpetas)
Historia 15: FAQ auto-generado por tema (Dataview Obsidian)
Historia 16: Mind maps Excalidraw (via API o MCP)
```

### Sprint 5 (semana 9-10): Integración y pulido

```
Historia 17: NEXO clasificador de intención explícito
Historia 18: Agentes BMAD custom en bmad-custom-src/ para desarrollo
Historia 19: Dashboard de progreso (Dataview Obsidian)
Historia 20: Tests E2E del pipeline completo (QA Quinn)
```

---

## PARTE 10 — ESTRUCTURA DE ARCHIVOS A CREAR

```
backend/agents/
  valera_agent.py          ← NUEVO: explicador con modos
  memo_agent.py            ← NUEVO: mnemotecnias y memes
  progreso_agent.py        ← NUEVO: Leitner + tracking
  wiki_agent.py            ← NUEVO: actualizar Obsidian
  turca_agent.py           ← NUEVO: historias narrativas
  simul_agent.py           ← NUEVO: conductor simulacros
  planner_agent.py         ← NUEVO: plan de estudio
  nexo_agent.py            ← NUEVO: clasificador de intención
  [chandra_tools.py]       ← EXISTE: añadir mano 8 (calcular_age)

backend/routers/
  [opos_chat.py]           ← EXISTE: añadir rutas de nuevos agentes
  flashcard_router.py      ← NUEVO: CRUD flashcards + Leitner
  simulacro_router.py      ← NUEVO: simulacro endpoints
  progreso_router.py       ← NUEVO: progreso endpoints

bmad-custom-src/
  agents/
    opos-pm.md             ← PM adaptado a OPOS (John versión OPOS)
    opos-dev.md            ← Dev adaptado (implementa agentes OPOS)
    opos-qa.md             ← QA legal (verifica vs BOE)
  workflows/
    create-opos-agent/     ← workflow para crear nuevo agente OPOS
    verify-legal-content/  ← workflow anti-alucinación

Obsidian vault/
  (estructura en PARTE 8 arriba)
```

---

## Resumen ejecutivo para no olvidar

**BMAD** = la empresa virtual que te ayuda a CONSTRUIR el sistema.
**Los 12 agentes** = el sistema que los opositores USAN para estudiar.
**La regla de oro**: ningún dato legal sale sin pasar por Neo4j o BOE.
**El secreto pedagógico**: COSMIC — componentes verificados (personajes, cálculos, plazos, trampas) intercambiables para generar simulacros únicos sin riesgo de alucinación.
**La economía**: Neo4j y calculadoras gratis, LLM solo cuando no hay alternativa.
**El objetivo**: que el opositor sienta que tiene un preparador experto disponible 24/7 que además es divertido, no miente nunca, y sabe exactamente qué necesita repasar hoy.

---

## PARTE 11 — LITELLM, CONTENT GATE, CACHÉ Y DUAL INTERFACE

> Sección añadida 21/05/2026. Cubre los gaps arquitectónicos no contemplados en las Partes 1-10.

---

### 11.1 — V14.5 y V17: las dos versiones internas del sistema

| Versión | Qué es | Ubicación | Estado |
|---------|--------|-----------|--------|
| **V14.5** "Narrativa en Red" | Motor de generación de casos prácticos con redes de personajes entrelazados. Blueprints + CaseSchemaBuilder + prose_validator. | `backend/v14/` | ✅ 10 blueprints activos (S02-S16). Pendientes: S17 Mar/Minería, S18 Cese RETA |
| **V17** Ingesta Neo4j | Script que indexa leyes en Neo4j desde `catalog_FINAL_v2.json`. Soporta `--skip-purge` para añadir sin borrar. | `backend/scripts/ingest_neo4j_v17.py` | ✅ Activo. 108 leyes, 6683 preceptos, 6683 embeddings |

---

### 11.2 — LiteLLM: el proxy unificado de modelos

**El problema actual**: cada agente llama a su proveedor directamente. Si Mistral falla → error total. Si necesitas cambiar de modelo → modificar código de cada agente.

**La solución**: LiteLLM como capa de abstracción única entre el backend y todos los modelos.

```
Backend FastAPI
    ↓
LiteLLM Proxy (puerto 4000)
    ├── Mistral medium-latest    ← CHANDRA, VALERA, EXAMINER (por defecto)
    ├── Mistral large-latest     ← Verificación legal profunda (Tier 2)
    ├── Claude Sonnet 4.6        ← Verificación Tier 3 (confidence < 0.85)
    ├── Groq llama-4-scout       ← NEXO clasificación (barato y rápido)
    ├── Groq qwen-3-32b          ← Batch de preguntas COSMIC (50% descuento)
    ├── DeepSeek                 ← Fallback si Mistral falla
    └── Gemini Flash             ← Explicaciones largas TURCA/MEMO
```

**Modelo por tarea** (configurado en LiteLLM, no hardcodeado en el agente):

| Agente/Tarea | Modelo | Razón |
|---|---|---|
| NEXO — clasificar intención | Groq llama-4-scout | <100ms, 0.001$/1K |
| CHANDRA — consulta legal | Mistral medium | Function calling verificado |
| VALERA — explicar concepto | Mistral medium | Calidad narrativa + tools |
| EXAMINER — generar 100 preguntas | Groq batch (50% dto.) | Volumen + coste |
| SIMUL — conducir examen | Mistral medium | Coherencia sesión larga |
| Verificación Tier 2 | DeepSeek | Coherencia lógica barata |
| Verificación Tier 3 | Claude Sonnet 4.6 | Verificación legal profunda |
| TURCA/MEMO — narrativa | Gemini Flash | Creatividad + tokens baratos |

**BMO y selección de modelo**: BMO envía header `X-Model-Preference` (ej. `claude-sonnet`). LiteLLM acepta la preferencia PERO la sobreescribe si la tarea exige mínimo de capacidad (ej. CHANDRA siempre necesita function calling — no se puede bajar a un modelo sin tools).

**Fallback automático**:
```
Mistral falla → Groq (mismo modelo family si es posible)
Groq falla    → DeepSeek
Todo falla    → Error con mensaje claro (nunca silencioso)
```

---

### 11.3 — Content Quality Gate: la puerta de publicación

**Regla absoluta**: el opositor NUNCA recibe contenido de zona draft. Solo recibe contenido de la zona publicada o respuestas de agentes con tools verificadas (CHANDRA, calculadoras).

```
ZONA DRAFT (invisible al opositor)
    ↓
    LLM genera con tools verificadas
    ↓
    confidence_scorer evalúa
    ├── > 0.85 → ZONA VERIFICADA (queue de publicación)
    ├── 0.70-0.85 → retry con más contexto (max 2 reintentos)
    └── < 0.70 → descarta + alerta a Spas
    ↓
ZONA VERIFICADA
    ↓
    VerificadorBOE cruza cada dato con Neo4j
    ├── OK → pasa a publicación automática
    └── Divergencia → pendiente revisión manual
    ↓
ZONA PUBLICADA (Wiki Obsidian + Cache)
    ↓
    Opositor recibe respuesta (0 tokens = viene de wiki)
    O agente en tiempo real con tools (datos verificados)
```

**¿Por qué necesitamos esto?** V14.5 ya encontró que el LLM cita artículos inventados (Art. 190.5 TRLGSS — no existe), cita plazos erróneos (19 semanas nacimiento — tampoco existe en TRLGSS), o confunde leyes. El gate es la barrera entre lo que genera la IA y lo que estudia el opositor.

**Implementación**: `backend/agents/content_gate.py` (por crear) — wraps todas las llamadas de generación con este pipeline.

---

### 11.4 — Caché y ahorro de tokens: jerarquía completa

Cuando el opositor hace una pregunta, la resolución sigue esta jerarquía (de 0 tokens a máximo coste):

```
1. Wiki Obsidian lookup (0 tokens)
   → WIKI agent busca nota verificada en vault
   → Si existe nota con frontmatter verificado:true → servir directamente
   → Sin llamada LLM. Actualización de PROGRESO solamente.

2. FAQ cache (0 tokens)
   → 100 preguntas frecuentes pre-computadas por tema
   → Almacenadas en Redis con TTL 30 días
   → Coste generación: una vez. Coste servicio: 0.

3. Caché semántica Redis (0 tokens)
   → Si cosine_similarity(query, query_cacheada) > 0.92 → reusar respuesta
   → Cubre variaciones de la misma pregunta ("¿cuánto cobra?" ≈ "¿qué importe tiene?")
   → TTL: 7 días (el BOE puede cambiar)

4. Caché exacta (0 tokens)
   → Hash MD5 de la query normalizada
   → TTL: 24 horas

5. Neo4j lookup directo (0 LLM tokens)
   → Para preguntas de estructura legal pura
   → Cypher devuelve el artículo exacto → formateado sin LLM
   → Calculadoras Python → número exacto sin LLM

6. LLM call con tools (coste real)
   → Solo aquí hay coste de LLM
   → Resultado pasa por Content Gate
   → Se cachea en Redis para próximas queries similares
   → Si calidad >0.85: también se guarda en Wiki (enriquece nivel 1)
```

**Ahorro estimado**: en fase madura, el 70-80% de las queries se resuelven en niveles 1-4 (0 tokens). El LLM solo trabaja en preguntas genuinamente nuevas.

---

### 11.5 — Dual Interface: Frontend React + Obsidian

El sistema sirve a DOS tipos de usuarios con DOS interfaces distintas que comparten el mismo backend:

```
┌─────────────────────────────────────────────────────┐
│  OPOSITOR EXTERNO (B2C)                             │
│  Frontend React 19 (ChatView, FlashcardsView,       │
│  ExamView, ProgressView, MindMapView...)             │
│  URL pública: opositaia.com                         │
│  Acceso: solo ZONA PUBLICADA                        │
│  Auth: Clerk (Trial €1 / Pro €69/mes)               │
└──────────────────┬──────────────────────────────────┘
                   │ API REST puerto 8080
                   ▼
┌─────────────────────────────────────────────────────┐
│  BACKEND FASTAPI (siempre online)                   │
│  LiteLLM proxy → modelos                            │
│  Content Gate → zonificación                        │
│  Calculadoras Python → números exactos              │
│  Neo4j → grafo legal                                │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌───────────────┐    ┌────────────────────┐
│ SPAS / BETA   │    │ WIKI OBSIDIAN      │
│ TESTERS       │    │ BOVEDA_OPOS        │
│ BMO Chandra   │    │ Zona publicada     │
│ Obsidian      │    │ Fuente de verdad   │
│ Acceso: draft │    │ 249+ notas         │
│ + published   │    │ verificadas        │
└───────────────┘    └────────────────────┘
```

**Reglas de acceso por zona**:

| Zona | Frontend React | BMO/Obsidian |
|------|---------------|--------------|
| Draft (sin verificar) | ❌ Nunca | ✅ Para desarrollo |
| Verificada (queue) | ❌ Nunca | ✅ Para revisión |
| Publicada (wiki) | ✅ Siempre | ✅ Siempre |
| Respuesta en vivo con tools | ✅ Solo si tools verificadas | ✅ Siempre |

**El FAQ en Obsidian como primera línea de defensa**: cuando se llega a 100 preguntas frecuentes verificadas por tema, el agente WIKI las pre-renderiza como notas Obsidian (`10_FAQ/T01_FAQ.md`, etc.) con frontmatter `verificado: true`. El WIKI agent las sirve antes de invocar ningún LLM. Actualización: solo cuando la ley cambia o hay nueva trampa.

---

*PARTE 11 añadida 21/05/2026.*
*Siguiente acción: `/bmad-sm` → crear historias del Sprint 1*
