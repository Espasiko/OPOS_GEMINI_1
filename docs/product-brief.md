# OpositAIA V2 — Product Brief

> **Fecha:** 28/02/2026  
> **Versión:** 1.1 — Decisiones PO integradas  
> **Estado:** ✅ APROBADO POR PO  
> **Fuentes:** Plan Cósmico Maestro + Apéndices II–VIII + Brainstorming 12/2025 + Auditoría Brownfield 27/02/2026

---

## 1. Visión del Producto

**OpositAIA** es una plataforma de preparación para oposiciones de la Administración General del Estado (AGE) y Seguridad Social (SS) que combina inteligencia artificial, contenido legal verificado y herramientas de estudio adaptativo para ofrecer una experiencia de aprendizaje personalizada, precisa y escalable.

### Propuesta de Valor Única

> *"La única plataforma donde un LLM NUNCA calcula: extrae parámetros del enunciado, ejecuta la función Python correspondiente y narra la respuesta con el artículo citado. Si no tiene herramienta, dice 'no puedo calcular esto automáticamente'."*

**Diferenciadores clave:**
- **Cero alucinaciones numéricas** — Motor determinístico Python (Decimal) para todos los cálculos legales
- **64 calculadoras verificadas** — 31 SS + 33 AGE, validadas contra exámenes reales 2024-2025
- **Estrategia COSMIC** — "Create Once, Serve Many": un concepto → 6+ formatos derivados automáticamente
- **RAG legal verificado** — 48.866 chunks en Qdrant + BOE XML para verificar vigencia en tiempo real
- **Multi-cuerpo** — C2 Auxiliar, C1 Administrativo AGE, C1 Administrativo SS, A2 Gestión SS *(lanzamiento inicial: C1 SS → después expandir)*

---

## 2. Público Objetivo

| Segmento | Descripción | Tamaño estimado |
|---|---|---|
| **Opositores activos AGE/SS** | Personas preparando oposiciones C1/C2 AGE y C1/A2 SS | ~200.000 en España |
| **Academias de oposiciones** | Centros que buscan contenido de calidad y herramientas digitales | ~500 academias |
| **Opositores autodidactas** | Sin academia, buscan herramientas de práctica accesibles | ~40% del total |

**Persona principal:** María, 32 años, opositando a C1 Administrativo SS. Trabaja a jornada parcial, estudia por las noches. Necesita practicar casos prácticos con cálculos reales y obtener feedback inmediato sobre sus errores.

---

## 3. Análisis Brownfield: Estado Actual vs. Propuesto

### 3.1 Qué YA existe y funciona ✅

| Componente | Estado | Detalle |
|---|---|---|
| Backend FastAPI | ✅ Operativo | 9 routers, CORS, health checks |
| 31 calculadoras SS | ✅ Operativo | `calculos_ss_extended.py`, `imv.py`, `ss.py` |
| 33 calculadoras AGE | ✅ Operativo | `calculadora_age.py` completa (LPAC + TREBEP) |
| Qdrant RAG | ✅ Operativo | 48.866 chunks indexados, búsqueda semántica |
| PostgreSQL | ✅ Schema existe | Tablas definidas, poco uso real |
| Frontend React 19 | ✅ Operativo | Chat, MindMap, CaseGenerator, Progress, Settings |
| MCP Server | ✅ Operativo | 9 tools registradas, ingestion pipeline |
| Chat con LLM | ✅ Operativo | Multi-modelo (Groq, DeepSeek, Gemini, Ollama) |
| Generador de casos | ✅ Operativo | Casos prácticos con corrección automática |
| Docker Compose | ✅ Operativo | Qdrant + Postgres + Backend |
| 25 agentes diseñados | ⚠️ Parcial | `opos-agents/` — algunos operativos, otros solo diseñados |

### 3.2 Qué FALTA implementar ❌ (Extraído del Plan Definitivo)

| Funcionalidad | Prioridad | Complejidad | Fuente |
|---|---|---|---|
| **Sistema de agentes BMAD** orquestados | ✅ COMPLETADO | BMAD V6 operando en YAML |
| **Repetición espaciada** (Leitner/Anki-style) | 🟠 ALTA | MEDIA | Plan Cósmico §6.6 |
| **Neo4j** grafo de conocimiento | 🟠 ALTA | ALTA | Plan Cósmico §3 |
| **Pipeline COSMIC** (1 concepto → 6 formatos) | 🟠 ALTA | ALTA | Plan Cósmico §4 |
| **Banco de 54K preguntas** pre-generado | 🟠 ALTA | MEDIA | Plan Cósmico §2 |
| **Simulacros cronometrados** (70/20 preguntas) | 🟠 ALTA | MEDIA | Apéndice VII §3.1 |
| **Autenticación** (Clerk) | 🟡 MEDIA | BAJA | Plan Cósmico §5.8 |
| **Pagos** (Stripe) | 🟡 MEDIA | MEDIA | Plan Cósmico §5.8 |
| **PWA / Modo offline** | 🟡 MEDIA | MEDIA | Plan Cósmico §6.3 |
| **Psicotécnicos** (series, matrices) | 🟡 MEDIA | MEDIA | Plan Cósmico §6.5 |
| **Memes educativos** con IA | 🟢 BAJA | BAJA | Plan Cósmico §6.7 |
| **Mini foro comunitario** | 🟢 BAJA | MEDIA | Feedback usuario |
| **Devstral** calculadoras dinámicas | 🟢 BAJA | ALTA | Apéndice VII §3.3 |
| **Mistral OCR** procesamiento PDFs | 🟢 BAJA | MEDIA | Apéndice VII §3.3 |
| **Analytics predictivo** (probabilidad aprobado) | 🟢 BAJA | ALTA | Plan Cósmico §6.8 |

---

## 4. Funcionalidades Clave (Agrupadas por Épica)

### ÉPICA 1: Motor de Calculadoras Completo
> **Meta:** 55 calculadoras determinísticas = cero error numérico

**Alcance:**
- **31 calculadoras SS** — ✅ Ya implementadas (IT, IP, Jubilación, Viudedad, Desempleo, Cotización, IMV, PNC, Mínimos)
- **33 calculadoras AGE** — ✅ Ya implementadas:
  - **Bloque A** (18): LPAC (plazos, recursos, silencio, notificaciones, subsanación, audiencia, presentación electrónica)
  - **Bloque B** (7): TREBEP (trienios, grados personales, permisos con días exactos, excedencias, complementos, prescripción)
  - **Bloque C** (3): Transversales (RGPD brecha 72h, contratación pública umbrales, acceso información 1 mes)

**Regla de oro:** El LLM NUNCA calcula. Extrae parámetros → llama a Python → narra con artículo citado.

---

### ÉPICA 2: RAG Legal Expandido
> **Meta:** Cobertura normativa 100% de los 4 cuerpos

**Alcance:**
- **Códigos Electrónicos BOE** como fuente primaria:
  - Código 435 (Auxiliar AGE C2) — PDF gratuito BOE
  - Código 442 (Administrativo AGE C1) — PDF gratuito BOE
  - TRLGSS texto consolidado (SS C1/A2)
- **54 normas identificadas** con prioridad de indexación (CRÍTICO/ALTA/MEDIA/BAJA)
- **Alertas BOE** por email cuando cambie una norma
- **MUFACE/MUGEJU/ISFAS** — Solo RAG conceptual, sin calculadoras
- **Verificación vigencia** vía BOE XML API en tiempo real

**Brownfield aprovechable:** Qdrant ya tiene 48.866 chunks + MCP pipeline de ingestion operativo.

---

### ÉPICA 3: Estrategia COSMIC (Create Once, Serve Many)
> **Meta:** 1 concepto atómico → 6+ formatos pedagógicos automáticos

**Pipeline de 3 capas:**

```
CAPA 1 (Átomo)          CAPA 2 (Derivados)           CAPA 3 (Experiencias)
─────────────           ──────────────────           ─────────────────────
Concepto atómico   →    Test tipo examen         →   Simulacro completo
con metadata:           Flashcard Anki-style          Caso práctico integrador
- ID único              Mapa mental                   Rankings de competición
- Cuerpo(s)             Esquema/resumen               Plan de repaso personalizado
- Tema/ley              Caso práctico simple
- Artículo              Mnemotecnia
- Dificultad
- Tags COSMIC
```

**Metadata por átomo:**
- `id`, `cuerpo[]`, `tema`, `ley`, `articulo`, `dificultad` (1-5)
- `formato_origen`, `formatos_derivados[]`, `calidad_score`, `fecha_verificacion`
- `tags_trampa[]` (conceptos que el examen explota como error frecuente)

---

### ÉPICA 4: Sistema de Agentes Inteligentes
> **Meta:** Orquestación multi-agente para generación y verificación de contenido

**Agentes propuestos (basados en BMAD V6):**

| Agente | Modelo sugerido | Función |
|---|---|---|
| **Orchestrator** | GPT-OSS 120B (Groq) | Analiza petición → activa pipeline correcto |
| **Intent Agent** | Mistral Nemo ($0.02/M) | Clasifica cuerpo + tipo + nivel usuario |
| **RAG Agent** | GPT-OSS 120B | Busca Qdrant + verifica BOE XML + caché semántico |
| **Calculator Agent** | Python directo | Ejecuta calculadora_ss.py o calculadora_age.py |
| **Generator Agent** | DeepSeek V3 | Genera contenido educativo en formato COSMIC |
| **Verify Agent** | Claude Sonnet | Verifica corrección legal + cálculos + 0 alucinaciones |
| **Compile Agent** | GPT-OSS 120B | Ensambla respuesta final adaptada al nivel del usuario |
| **OCR Agent** | Mistral Pixtral | Procesa PDFs subidos por el usuario |
| **Devstral Agent** | Devstral Small | Genera calculadoras dinámicas para cálculos no cubiertos |

**Pipelines por tipo de petición:**
- `pregunta_conceptual` → Intent → RAG → Chat → Verify → Compile
- `cálculo_ss` → Intent → Calculator → Chat
- `simulacro` → Intent → Retrieval → Simulacro
- `caso_práctico` → Intent → RAG → Generator → Verify → Compile
- `flashcard` → Intent → RAG → Flashcard → Verify
- `pdf_usuario` → OCR → Intent → PDF RAG → Chat

---

### ÉPICA 5: Estudio Adaptativo
> **Meta:** Aprendizaje personalizado que se adapta al nivel del opositor

**Componentes:**
- **Repetición espaciada** (algoritmo Leitner/SM-2): intervalos crecientes para conceptos dominados, refuerzo inmediato para errores
- **Perfil de opositor**: cuerpo, temas fuertes/débiles, historial de respuestas, predicción de aprobado
- **Plan de estudio dinámico**: prioriza temas con peor rendimiento y mayor peso en examen
- **Simulacros adaptativos**: ajustan dificultad según rendimiento previo

**Brownfield aprovechable:** `ProgressView.tsx` ya muestra estadísticas básicas (aciertos/fallos/porcentaje). `usePersistentState` almacena progreso en localStorage → migrar a PostgreSQL.

---

### ÉPICA 6: Monetización
> **Meta:** Modelo premium B2C sostenible

| Tier | Precio | Incluye |
|---|---|---|
| **Trial** | €1 / 3 días | Acceso completo durante 3 días, con límites de uso |
| **Pro** | €69/mes | Ilimitado: preguntas, simulacros, casos, flashcards, repetición espaciada, soporte |

> [!NOTE]
> **Estrategia B2C primero.** Las academias (B2B) se abordarán en una fase posterior con un modelo diferente que el PO tiene en mente. No se incluyen Kits de contenido ni API pública en esta versión.

**Conversión esperada:** Trial €1 → Pro €69/mes con tasa de conversión objetivo 15-25%

---

## 5. Stack Tecnológico Propuesto

### Mantener del brownfield
- **Backend:** FastAPI + PostgreSQL + Qdrant + Docker
- **Frontend:** React 19 + Vite + TypeScript
- **LLMs:** Groq (GPT-OSS), DeepSeek V3, Gemini, Ollama, mistral etc. mas llm-s

### Añadir
- **Neo4j Community** — Grafo de conocimiento COSMIC (relaciones tema-ley-artículo-pregunta)
- **Redis** — Caché semántico + rate limiting + sesiones
- **Clerk** — Autenticación (SSO, magic links, 10K MAU free)
- **Stripe** — Pagos y suscripciones
- **Mistral API** — Nemo (clasificador barato), Large (verificación legal EU/RGPD), OCR (PDFs)
- **Cloudflare Pages** — Frontend CDN + HTTPS automático

### Infraestructura
- **Desarrollo:** Docker Compose local (Postgres + Qdrant + **Neo4j Community local** + Redis + Backend)
- **Producción:** Fly.io Frankfurt (Backend) + Cloudflare Pages (Frontend) + **Neo4j local en VPS** (decisión PO: local primero) + Qdrant Cloud Free

---

## 6. Roadmap por Fases

### Fase 1: Consolidación Base (4-6 semanas)
> Prioridad: hacer funcionar lo que ya existe correctamente · **Scope: C1 SS primero**

- [ ] Implementar 28 calculadoras AGE (`calculadora_age.py`)
- [ ] Expandir RAG con Códigos Electrónicos BOE (TRLGSS consolidado + Código 442 para C1)
- [ ] Migrar localStorage → PostgreSQL (persistencia real de progreso)
- [ ] Implementar autenticación con Clerk
- [ ] Simulacros cronometrados (70 preguntas + temporizador) — solo C1 SS
- [ ] Tests automatizados para todas las calculadoras

### Fase 2: COSMIC + Adaptativo (6-8 semanas)
> Prioridad: el diferenciador pedagógico

- [ ] Neo4j Community **local en Docker** (decisión PO: local primero, después evaluar cloud)
- [ ] Pipeline COSMIC (1 átomo → test + flashcard + mapa mental + caso)
- [ ] Sistema de repetición espaciada (Leitner/SM-2)
- [ ] Generación masiva de banco de preguntas (objetivo: 10K verificadas)
- [ ] Perfil adaptativo del opositor
- [ ] Sistema de agentes orquestados (Orchestrator → Intent → RAG → Generator → Verify)

### Fase 3: Monetización + Escala (4-6 semanas)
> Prioridad: modelo de negocio viable · **B2C primero**

- [ ] Integración Stripe (Trial €1/3 días + Pro €69/mes)
- [ ] PWA / modo offline (Service Worker + caché local)
- [ ] Mini-foro comunitario (solo DESPUÉS de tener preguntas listas + E2E probado + desplegado)
- [ ] Psicotécnicos (series numéricas, matrices, verbal)
- [ ] Analytics predictivo (probabilidad de aprobado)
- [ ] Deploy producción: Fly.io + Cloudflare Pages
- [ ] Expandir a otros cuerpos (C2, C1 AGE, A2 SS) tras validar con C1 SS

---

## 7. Riesgos y Mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **Alucinaciones legales** | 🔴 CRÍTICO | Motor determinístico Python + Verify Agent + BOE XML |
| **Normativa desactualizada** | 🔴 CRÍTICO | Alertas BOE + Códigos Electrónicos actualizados + verificación vigencia |
| **Costes LLM excesivos** | 🟠 ALTO | Caché semántico Redis + Mistral Nemo ($0.02/M) para clasificación + COSMIC pre-generado |
| **Complejidad multi-cuerpo** | 🟠 ALTO | Selector de cuerpo al inicio + calculadoras separadas (SS vs AGE) |
| **Dependencia de APIs externas** | 🟡 MEDIO | Multi-proveedor (Groq + DeepSeek + Gemini) + Ollama local como fallback |
| **Competencia de academias** | 🟡 MEDIO | Diferenciador: cálculos exactos + IA adaptativa (algo que las academias tradicionales no tienen) |

---

## 8. Métricas de Éxito

| Métrica | Objetivo Fase 1 | Objetivo Fase 3 |
|---|---|---|
| Precisión calculadoras | 100% (0 errores numéricos) | 100% |
| Cobertura normativa RAG | 100% temario (leyes CRÍTICAS) | 100% temario completo |
| Preguntas verificadas en banco | 5.000 | 54.000 |
| Usuarios registrados | 10 beta testers | 1.000 |
| Tasa de retención semanal | 70% | 90% |
| NPS opositores | >50 | >70 |
| Ingresos mensuales | €100 (beta) | €5.000 MRR |

---

## 9. Decisiones del Product Owner (28/02/2026) ✅

> [!TIP]
> Todas las decisiones han sido tomadas. Este brief está listo para alimentar el PRD.

| # | Decisión | Respuesta PO |
|---|---|---|
| 1 | Priorización 3 fases | ✅ **Confirmadas tal cual** |
| 2 | Neo4j local vs cloud | ✅ **Local primero** (Docker) |
| 3 | Scope inicial | ✅ **Un solo cuerpo: C1 SS** → expandir después |
| 4 | Modelo de precios | ✅ **Trial €1 / 3 días + Pro €69/mes** (sin tier Academy por ahora) |
| 5 | Mini-foro comunitario | ✅ **Sí, pero después** de tener preguntas E2E + app desplegada |
| 6 | B2C vs B2B | ✅ **B2C primero** — el PO tiene otras ideas para academias en el futuro |

---

*Documento generado a partir del análisis de: `plan_app_oposiciones_cosmic.md` (728 líneas), Apéndices II-VIII, `BRAINSTORMING_RECOPILACION_IDEAS_12_DIC_2025.md`, `28_02_2026_SINTESIS_PLAN_DEFINITIVO.md`, Auditoría Brownfield 27/02/2026, `project-overview.md`, `project-scan-report.json`.*
