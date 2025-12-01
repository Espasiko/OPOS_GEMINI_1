# 🔍 AUDITORÍA COMPLETA: IDEAS, PROPUESTAS E INVESTIGACIONES - OPOSITAIA

**Fecha Auditoría**: 29 Noviembre 2025  
**Scope**: Últimos 20 commits + Todos los documentos .md del proyecto  
**Objetivo**: Inventario completo de ideas para brainstorming multi-agente y decisión estratégica

---

## 📋 ÍNDICE

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Ideas de Arquitectura y Tech Stack](#arquitectura)
3. [Propuestas de Monetización](#monetizacion)
4. [Investigaciones de Mercado](#mercado)
5. [Optimizaciones de Costes](#costes)
6. [Mejoras de UX/UI](#ux)
7. [Fine-tuning y ML](#ml)
8. [Seguridad y Legal](#legal)
9. [Deployment y DevOps](#deployment)
10. [Marketing y Go-to-Market](#marketing)
11. [Próximos Pasos para Brainstorming](#next-steps)

---

## 🎯 RESUMEN EJECUTIVO {#resumen-ejecutivo}

### Últimos 20 Commits (Progreso Reciente)

```
29 Nov: Mistral 7B GGUF local funcionando (sin Ollama)
29 Nov: CPU LoRA finetune config + runner script
27 Nov: Indexación completa leyes temario oficial
27 Nov: Merge main into gemini_wsl
25 Nov: Frontend fix + RAG 3 capas + 13 leyes
23 Nov: Investigación Groq + Agentes + BYOK + B2B
23 Nov: Planificación Sprints 11-14
22 Nov: Investigación producción y comercialización
22 Nov: Auditoría seguridad completa
22 Nov: Tests automatizados implementados
22 Nov: Limpieza masiva (60 archivos a basura)
21 Nov: Sprint 8 - Endpoints AI multi-proveedor
21 Nov: Sistema multi-proveedor LLM completo
19 Nov: RAG system con 21 leyes + Sprint 7
```

### Documentos Estratégicos Clave (101 archivos .md analizados)

| Categoría | # Docs | Estado | Impacto |
|-----------|--------|--------|---------|
| Estrategia Negocio | 12 | ✅ Completo | Alto |
| Arquitectura Tech | 18 | ⚠️ En progreso | Alto |
| Fine-tuning ML | 8 | 🟡 Investigación | Medio |
| Costes/Optimización | 15 | ✅ Analizado | Alto |
| Legal/Seguridad | 6 | ✅ Resuelto | Crítico |
| UX/UI | 4 | 📝 Propuesto | Medio |
| Marketing | 3 | 🔴 Pendiente | Alto |
| Deployment | 9 | ⚠️ En progreso | Alto |

---

## 🏗️ IDEAS DE ARQUITECTURA Y TECH STACK {#arquitectura}

### 1. ✅ IMPLEMENTADO: Stack Multi-Proveedor LLM

**Documento**: `SPRINT8_COMPLETADO.md`

```typescript
// Backend FastAPI con soporte para:
- Groq (Mistral 7B)
- Google Gemini (Flash, Pro)
- OpenAI (opcional BYOK)
- Anthropic Claude (opcional)
- Mistral AI (API directa)
```

**Estado**: ✅ PRODUCTIVO (Sprint 8 completado 21 Nov)  
**Impacto**: Alto - permite cambiar de modelo sin romper app  
**Próximos pasos**: Añadir Cohere Command R, DeepSeek-V3

---

### 2. ⚠️ PROPUESTA: Cloudflare Workers + Durable Objects

**Documento**: `EVALUACION_CLOUDFLARE_WORKERS_DURABLE_OBJECTS.md`

**Idea**: Migrar agentes de Python FastAPI a Cloudflare Workers (TypeScript)

**Viabilidad**:
| Componente | Viabilidad | Esfuerzo |
|------------|-----------|----------|
| Agentes Stateless | ✅ 100% | Bajo |
| MCP Tools | ✅ 100% | Bajo |
| Orquestación Multi-Agente | ⚠️ 70% | Medio |
| Durable Objects Estado | ⚠️ 60% | Alto |
| Real-time Coordination | ⚠️ 50% | Alto |

**Beneficios**:
- 🚀 30% mejor performance (150ms → 50ms TTFB)
- 💰 27% menos costos ($30 → $22/mes)
- 🌍 200+ ciudades (geo-distribution)

**Riesgos**:
- 🔴 Complejidad aumenta
- 🔴 Lock-in en Cloudflare
- 🔴 20-40% cambios en backend

**Recomendación**: ⚠️ **HYBRID APPROACH**
- ✅ Usar Workers para stateless agents (MCP tools)
- ⚠️ Mantener Python FastAPI para orquestación compleja
- ✅ Cloudflare Static Assets para frontend

**Estado**: 📋 PLAN COMPLETO (27 Nov)  
**Decisión**: PENDIENTE  
**Impacto**: Alto - afecta toda la arquitectura

---

### 3. ⚠️ PROPUESTA: Sistema de Agentes Multi-Capa YAML

**Documento**: `PROPUESTA_SISTEMA_AGENTES_YAML.md`

**Idea**: Arquitectura de 8 agentes especializados con manifests CSV centralizados

```
Agent Tier (8 agentes)
├── Core (Orchestrator, Validator, Synthesizer)
├── Legal (Examiner, CaseAnalyzer, LawResearcher, JurisprudenceExpert)
├── Educational (Tutor, ContentCreator, AssessmentExpert, StudyPlanner)
└── Verification (FactChecker, ConsistencyValidator, LegalAuditor)

Workflow Tier (4 workflows)
├── exam-generation (7 steps paralelos)
├── case-analysis (RAG + verificación)
├── study-planning (personalización)
└── legal-research (investigación)

Tool Tier (MCP Server)
├── rag_search (Qdrant)
├── boe_verify (BOE official)
├── jurisprudence_search (sentencias)
├── content_generator (LLM)
└── output_validator (QA)

Verification Tier (3-capas)
├── Layer 1: Validación estructural (JSON schema)
├── Layer 2: Verificación de hechos (legal accuracy)
└── Layer 3: Generación de tests (regression)
```

**Ventajas**:
- ✅ Reutilización de código 100% (YAML)
- ✅ Testing automático
- ✅ Validación 3-capas
- ✅ Similar a BMAD Method (ya conocido)

**Desventajas**:
- 🔴 Complejidad inicial alta
- 🔴 Curva de aprendizaje equipo
- 🔴 4-6 semanas implementación

**Estado**: 📋 PROPUESTA COMPLETA (27 Nov)  
**Decisión**: PENDIENTE  
**Impacto**: Alto - redefine arquitectura agentes

---

### 4. ✅ IMPLEMENTADO: RAG Sistema 3 Capas

**Documento**: `DIAGNOSTICO_COMPLETO_RAG_3_CAPAS.md`

```
Capa 1: Normativa Oficial (BOE)
├── LGSS (Ley General Seguridad Social)
├── RD Afiliación
├── RD Recaudación
├── Ley IMV
└── 10+ RDs complementarios

Capa 2: Jurisprudencia (CENDOJ)
├── Sentencias TS (Tribunal Supremo)
├── Sentencias AN (Audiencia Nacional)
├── Sentencias JCA (Contencioso-Administrativo)
└── Doctrina Fiscalía

Capa 3: Materiales Estudio
├── Tests oficiales oposiciones
├── Esquemas personales
├── FAQ administrativos
└── Simulacros CCAFYDE
```

**Estado**: ✅ PRODUCTIVO (25 Nov - 13 leyes indexadas)  
**Métricas**:
- 7,833 chunks indexados
- 768 dimensiones (RoBERTalex)
- Qdrant Cloud Free Tier

**Próximos pasos**: 
- [ ] Migrar a SBERT Spanish (384 dims)
- [ ] Añadir 40+ leyes más (objetivo: 10,000 chunks)
- [ ] Indexar jurisprudencia CENDOJ (2,700 chunks)

---

### 5. ✅ IMPLEMENTADO: Mistral 7B Local con GGUF

**Documento**: `SOLUCION_MISTRAL_LOCAL_GGUF.md`

**Idea**: Modelo local cuantizado Q4 para inferencia sin Ollama

**Implementación**:
```python
# backend/agents/mistral_gguf_local.py
from llama_cpp import Llama

model = Llama(
    model_path="~/mistral_models/mistral-7b-instruct-q4.gguf",
    n_ctx=2048,
    n_threads=4,  # Intel i5-3470
    n_gpu_layers=0,  # CPU-only
)
```

**Métricas**:
- Tamaño: 4.07 GB (vs 7GB Ollama)
- Velocidad: ~10-15 tokens/seg (CPU)
- RAM usada: ~4.2GB

**Ventajas**:
- ✅ Sin dependencia Ollama
- ✅ Descarga directa HuggingFace
- ✅ Más eficiente en CPU

**Estado**: ✅ FUNCIONANDO (29 Nov)  
**Test**: Generación coherente sobre derecho español ✅

---

## 💰 PROPUESTAS DE MONETIZACIÓN {#monetizacion}

### 0. Corrección importante (costes reales)

- El coste fijo de «€50/mes» para un freemium clásico no es representativo. El coste operativo depende de uso real de tokens y del mix de modelos. Con el stack actual (Groq + caché + contenido reutilizable) el coste medio por usuario activo intensivo puede situarse en €0.20–€1.50/mes. Para la mayoría de usuarios ligeros (chat + lectura) el coste tiende a ~€0,00–€0,30/mes, especialmente con BYOK.
- Implicación: Freemium clásico es viable si controlamos generación de contenidos (COSM) y activamos caché agresiva en prompts del sistema. BYOK reduce a cero el coste IA del plano gratuito.

### 1. ✅ ESTRATEGIA BYOK (Bring Your Own Key)

**Documento**: `ESTRATEGIA_BYOK_Y_B2B.md`

**Modelo 3 Tiers**:

#### TIER 1: FREEMIUM (BYOK) 🆓
```
✅ Usuario trae API key Groq (gratis)
✅ 14,400 requests/día (Groq free tier)
✅ Acceso a TODAS las features
✅ Sin límite de tiempo
✅ Coste para OpositAIA: €0
```

#### TIER 2: PREMIUM (Managed) ⚡
```
✅ Nosotros proveemos las API keys
✅ Sin límites (10K req/mes)
✅ Soporte prioritario (24h)
Precio: €9.99/mes
Margen: €9.53/mes (95%)
```

#### TIER 3: ENTERPRISE (B2B) 🏢
```
✅ White-label academias
✅ SSO + Reporting
✅ Custom branding
✅ Soporte dedicado
Precio: €299/mes (50 usuarios)
Margen: €275/mes (92%)
```

**Ventajas**:
- ✅ Coste CERO infraestructura IA (users BYOK)
- ✅ Escalabilidad infinita
- ✅ Margen 100% en freemium
- ✅ Diferenciador de mercado

**Target Perfecto**:
- 🎓 Opositores Gen Z (técnicamente capaces)
- 📚 Academias (control de costes)
- 👨‍🏫 Preparadores (escalabilidad)

**Estado**: 📋 ESTRATEGIA COMPLETA (23 Nov)  
**Decisión**: ⚠️ PENDIENTE VALIDACIÓN MERCADO

---

### 2. ⚠️ ALTERNATIVA: Freemium Clásico + COSM (Simulacros/Tests reutilizables)

**Fuente**: `components/SettingsView.tsx`

```typescript
// Plan Gratuito:
- 10 mensajes chat/día
- 2 casos prácticos/día
- 1 mapa mental/día

// Plan PRO:
- Acceso ilimitado
- Historial extendido
- Modelos más potentes (Gemini 2.5 Pro)
Precio: €9-15/mes
```

**Ajuste clave (COSM)**:
- Pre-generar y versionar 1,000 simulacros/casos/tests curatoriales (recombinables) que servimos a múltiples usuarios con ligeras variaciones + una burbuja de chat IA para dudas. Esto traslada consumo a contenido estático y minimiza tokens.

**Micropagos propuestos**:
- Packs de casos prácticos: 2 casos = €5, 10 casos = €19, 50 casos = €79. Incluye tutor IA en burbuja para preguntas durante la práctica (consumo de tokens acotado y cacheable).

**Ventajas**:
- ✅ Familiar para usuarios
- ✅ Fácil implementación
- ✅ Coste IA muy bajo con COSM + caché

**Desventajas**:
- 🔴 Requiere curación inicial de 1,000+ items
- 🔴 Riesgo de canibalizar personalizaciones 100% IA si el pack cubre casi todo

**Estado**: 📝 MENCIÓN EN UI  
**Decisión**: ⚠️ PENDIENTE (evaluar vs BYOK)

---

## 📊 INVESTIGACIONES DE MERCADO {#mercado}

### 0. Panorama España (competidores a revisar y precios reales)

Competidores directos (test/simulacros + mobile) con precios verificados:
- OpositaTest (tests + esquemas + app iOS/Android)
   - Planes de test: desde `6,39 €/mes` con promoción BF (-20%); precio base indicado como `7,99 €/mes`.
      URL: `https://www.opositatest.com/subscribir/oposicion/administrativos-seguridad-social-tl` y página oposición: `https://www.opositatest.com/oposiciones/administrativos-seguridad-social-tl`
   - Curso “Todo incluido” (material + soporte): desde `63,00 €/mes` en BF; precio tachado `78,75 €/mes`.
      URL: `https://www.opositatest.com/productos/curso-administrativos-seguridad-social-turno-libre`

- Opolex (academia online con plataforma propia)
   - Precio público genérico en home: "Todo por un solo pago de `399 €`" (único pago; opción 3 cuotas sin intereses vía PayPal). Campaña BF30 -30% visible.
      URL: `https://www.opolex.es/` (sección precio en home). Otras rutas de planes devuelven 404 actualmente.

- Testopos (apps móviles por oposición)
   - No muestra precios web centralizados; monetiza vía apps en Google Play por categoría. No hay `€/mes` en web corporativa.
      URL: `https://testopos.com/`

 - Opositas.com (academia online con 30+ años experiencia)
    - Sin precios públicos en web; requiere carrito/contacto para ver precio final. Black Friday muestra "Hasta -50% descuentos en cientos de productos" ya aplicados en carrito.
    - Estructura: Preparación integral (temario + materiales didácticos), cursos por leyes, temarios con resolución de dudas, esquemas, supuestos prácticos, simulacros.
       URL: `https://www.opositas.com/tienda/`

 - MasterD (academia con 30 años, 40 centros, 90k alumnos)
    - Sin precios públicos en landing; requiere solicitar info personalizada (900 30 40 30). Ofrecen metodología online/semipresencial con tutores especializados, campus virtual, clases en directo.
    - Estructura: Preparación personalizada con entrenador personal, preparador especializado, orientador laboral. Simulacros reales, test online, vídeos, repaso espaciado.
       URL: `https://www.masterd.es/oposiciones/`

 - CampusTraining (con Flou, colaboración para prep. oposiciones)
    - Sin precios públicos en web; requiere formulario de info (910 32 37 90). Ofrecen tutorías individuales, plataforma con test/simulacros, formación online con apoyo presencial.
    - Estructura: Entrenador personal, sesiones one-to-one, temarios actualizados, preparadores expertos.
       URL: `https://www.campustraining.es/oposiciones/`

Observaciones y estructura de planes a comparar:
- Mensual/anual; por oposición vs. multi-oposición; add-ons (esquemas, campeonatos, tutorización).
- Free trial: OpositaTest muestra test gratuitos con registro; Opolex ofrece demo/prueba gratis 7 días.
- ESG-social: OpositaTest/Opolex muestran campañas promocionales (BF -20% / -30%); MasterD/CampusTraining destacan metodología personalizada y seguimiento continuo. Ninguna comunica explícitamente becas sociales ni accesibilidad WCAG en landing.

Acción completada: 6 competidores principales verificados. Observación clave: **solo OpositaTest y Opolex publican precios directos**; el resto (Opositas, MasterD, CampusTraining) requieren solicitar info personalizada, sugiriendo modelo B2C con pricing variable por oposición y pack seleccionado.

**Conclusión preliminar de mercado**:
- Modelos dominantes: (1) SaaS mensual transparente (OpositaTest 6-8 €/mes), (2) Pago único por curso (Opolex 399 €), (3) Pricing personalizado post-contacto (MasterD, Opositas, CampusTraining).
- Diferenciadores: apps móviles (OpositaTest, Testopos), tutorización 1-on-1 (MasterD, Flou), contenido curatorial (Opositas), comunidades y campeonatos (OpositaTest).
- Oportunidad OpositAIA: BYOK (coste €0 para usuario freemium) + COSM (packs simulacros €5-19) + chat IA especializado en legal (diferenciador técnico claro vs. competencia generalista).

---

### 1. ✅ Análisis Competidores + Costes (modelo de uso/tokens)

**Documento**: `NUMEROS_FINALES_COSTES_IA.md`

**Usuario Normal 8h/día** (Tu Medida Real):
```
Input:  96,000 tokens
Output: 6,400 tokens
TOTAL:  102,400 tokens/día

Coste actual: $0.88/día = €26.40/mes
```

**Opciones Optimización**:

| Opción | €/mes | Margen vs €30 | Tiempo | Calidad |
|--------|-------|---------------|--------|---------|
| Groq 70B Simple | €1.14 | €28.85 (96%) | NOW | 98% |
| Groq + Caché | €0.46 | €29.53 (98.5%) | 1 sem | 98% |
| Stack Completo | €0.18 | €29.81 (99.4%) | 5 sem | 95% |
| BYOK | €0.00 | €9.89 (99%) | 1 sem | User |

**Recomendación**: ⭐ **Caché + Contenido Reutilizable**
```
€1.14 → €0.22/mes (94% ahorro) 🚀
4-5 semanas de trabajo

Incluye:
├─ 1000 simulacros reutilizables
├─ 500 casos prácticos
├─ 200 esquemas legales
└─ Caché prompt (60% ahorro)
```

**Estado**: ✅ ANÁLISIS COMPLETO (28 Nov)  
**Decisión**: ⚠️ IMPLEMENTAR CACHÉ (Sprint 11)

---

### 2. ✅ Hallazgo: BOE Materiales Oposiciones

**Documento**: `HALLAZGO_BOE_MATERIALES_OPOSICIONES.md`

**Descubrimiento**: BOE publica materiales oficiales para oposiciones

```
Fuentes oficiales gratuitas:
├─ PDFs temario oficial
├─ Tests anteriores convocatorias
├─ Esquemas legislativos
└─ Material complementario

Licencia: Dominio público
Calidad: ⭐⭐⭐⭐⭐ (oficial)
Coste: €0
```

**Impacto**: ✅ POSITIVO
- Fuente legal 100% segura
- Contenido de alta calidad
- Sin coste licencias
- Diferenciador vs competencia

**Estado**: ✅ VALIDADO  
**Acción**: ✅ USAR como base Capa 3 RAG

---

## ⚡ OPTIMIZACIONES DE COSTES {#costes}

### 1. ✅ PROPUESTA: Contenido Reutilizable Database

**Documento**: `ESTRATEGIA_CONTENIDO_REUTILIZABLE_DATABASE.md`

**Idea**: Pre-generar contenido compartido entre usuarios

```sql
CREATE TABLE simulacros_reutilizables (
    id UUID PRIMARY KEY,
    tema VARCHAR(255),
    preguntas JSONB,  -- 5 preguntas tipo test
    metadata JSONB,
    created_at TIMESTAMP,
    times_used INT DEFAULT 0
);

-- Ejemplo: 1000 simulacros pre-generados
-- Ahorro: 1000 usuarios × €0.05/simulacro = €50/día
```

**Métricas Esperadas**:
- 80% usuarios usan contenido compartido
- 20% usuarios generan custom (pagan)
- Ahorro: 60-80% costes IA

**Beneficios**:
- ✅ Calidad consistente (curado)
- ✅ Latencia CERO (pre-generado)
- ✅ Escalabilidad perfecta

**Desventajas**:
- 🔴 Menos personalización
- 🔴 Setup inicial (crear 1000+ items)

**Estado**: 📋 PROPUESTA (28 Nov)  
**Decisión**: ⚠️ EVALUAR para Sprint 12

---

### 2. ✅ PROPUESTA: Caché de Prompts

**Documento**: `GUIA_IMPLEMENTACION_CACHE_PASO_A_PASO.md`

**Idea**: Reutilizar prompts largos con Groq cache

```python
# Antes (sin caché):
prompt = f"{SYSTEM_PROMPT_5000_TOKENS}\n\n{user_query}"
cost = 0.05 * (5000 + 200) / 1M = $0.00026

# Después (con caché):
prompt = f"{SYSTEM_PROMPT_CACHED}\n\n{user_query}"
cost = 0.01 * 200 / 1M = $0.000002

Ahorro: 99% en prompts repetidos
```

**Implementación**:
```typescript
// backend/services/groq_service.ts
const response = await groq.chat.completions.create({
  model: "llama-3.3-70b-versatile",
  messages: [
    { role: "system", content: CACHED_PROMPT },  // ← cached
    { role: "user", content: userQuery }
  ],
  cache: { enabled: true, ttl: 3600 }
});
```

**Ahorro Esperado**: 60% costes prompts  
**Tiempo Implementación**: 1 semana  
**Riesgo**: Bajo

**Estado**: 📋 GUÍA COMPLETA  
**Decisión**: ✅ **IMPLEMENTAR Sprint 11**

---

## 🎨 MEJORAS DE UX/UI {#ux}

### 1. ⚠️ PROPUESTA: Mapas Mentales Interactivos

**Documento**: `CORRECCION_UX_MAPAS_MENTALES.md`

**Problema**: Mapas mentales estáticos (solo visualización)

**Propuesta**: Interactividad completa
```
✅ Edición inline (click para editar)
✅ Drag & drop (reorganizar nodos)
✅ Añadir/eliminar nodos
✅ Exportar editable (JSON, Markdown)
✅ Compartir mapas entre usuarios
```

**Herramientas Sugeridas**:
- Excalidraw (diagramas)
- Mermaid.js (flowcharts)
- D3.js (custom interactivo)

**Impacto**: Medio - mejora engagement  
**Esfuerzo**: 2-3 semanas  
**Estado**: 📝 PROPUESTA

---

### 2. ⚠️ PROPUESTA: Modo Oscuro Completo

**Fuente**: Código actual (`dark:` classes en Tailwind)

**Estado**: ⚠️ PARCIAL (algunos componentes)

**Acción**: Completar en todos los componentes  
**Esfuerzo**: 1 semana  
**Impacto**: Bajo - nice to have

---

## 🤖 FINE-TUNING Y ML {#ml}

### 1. ✅ PLAN: Mistral 8B Fine-tuned en VPS (para pruebas)

**Documento**: `PLAN_IMPLEMENTACION_COMPLETO_10K_CHUNKS.md`

**Objetivo**: Fine-tune Mistral 8B en CPU con 10,000 chunks legales

**Dataset**:
```
1️⃣ LEYES SS (~890 chunks)
2️⃣ LEGISLACIÓN COMPLEMENTARIA (~1,080 chunks)
3️⃣ JURISPRUDENCIA (~2,700 chunks)
4️⃣ TESTS/Q&A (~1,600 chunks)
5️⃣ RESOLUCIONES/CIRCULARES (~3,000 chunks)

TOTAL: ~9,270 chunks
```

**Mejora Esperada**:
```
MÉTRICA                  | Actual | Con FT   | MEJORA
─────────────────────────┼────────┼──────────┼────────
Precisión RAG            | 65-70% | 85-90%   | +20-25%
Veracidad respuestas     | 70%    | 85%      | +15%
Hallucinations           | 15-20% | 5-8%     | -60%
```

**Implementación**:
```bash
# Fine-tune LoRA en CPU (gratis, lento)
cd ~/mistral-finetune
bash tools/finetune/run_finetune_cpu.sh

# Servir con adaptador
mistral-chat ~/mistral_models/7B \
  --instruct \
  --lora_path ~/mistral_runs/7B_cpu_lora/checkpoints/checkpoint_300/lora.safetensors
```

**Infra**: VPS Hostinger 8GB RAM (disponible). Sirve como entorno de prueba para FT/inferencia con LoRA. Para producción general, mantener Groq 70B para chat generalista y usar el FT sólo en rutas legales críticas.

**Costes**: €0–€8/mes (VPS ya pagado; electricidad/tiempo)  
**Tiempo**: 3-4 semanas (dataset + entrenamiento CPU)  
**Riesgo**: Medio (ops en VPS + tuning rendimiento)

**Estado**: 📋 PLAN COMPLETO (29 Nov)  
**Decisión**: ⚠️ EVALUAR (prioridad media)

---

### 2. ⚠️ ALTERNATIVA: Fine-tune en Hugging Face Spaces

**Documento**: `EXPLICACION_HUGGINGFACE_SPACES.md`

**Idea**: Usar GPU gratuito HF Spaces para fine-tune

**Ventajas**:
- ✅ GPU gratis (15GB VRAM T4)
- ✅ No requiere hardware local
- ✅ Más rápido que CPU

**Desventajas**:
- 🔴 Límite 48h por sesión
- 🔴 Cola de espera
- 🔴 Puede pausarse

**Estado**: 📝 INVESTIGADO  
**Decisión**: ⚠️ BACKUP si CPU falla

---

## 🔒 SEGURIDAD Y LEGAL {#legal}

### 1. ✅ COMPLETADO: Auditoría Seguridad

**Documento**: `INVESTIGACION_PRODUCCION_Y_SEGURIDAD.md`

**Tareas Completadas**:
- ✅ TAREA 1: Migración RAG a Qdrant Cloud (27 Nov)
- ✅ TAREA 2: Cloudflare + MCP + Seguridad (análisis completo)
- ✅ TAREA 3: Agente BOE + Jurisprudencia (investigación)
- ✅ TAREA 4: MCP Server Propio Seguro (implementado)
- ✅ TAREA 5: GDPR + Legislación Española (completo)

**Estado**: ✅ **TODO SEGURO**  
**Veredicto**: `VEREDICTO_LEGAL_FINAL.md`

```
✅ DATOS PERSONALES: No almacenamos (LocalStorage)
✅ GDPR: Cumplimiento 100%
✅ CONTENIDO: Fuentes públicas oficiales
✅ API KEYS: Encriptadas (.env.backend)
✅ MCP SERVER: Seguro (sin network exposure)
```

**Próximos pasos**: 
- [ ] Política de privacidad (plantilla legal)
- [ ] Términos de servicio (plantilla SaaS)
- [ ] Cookie banner (EU compliance)

---

### 2. ✅ ANÁLISIS: Riesgo Legal Fine-tuning

**Documento**: `ANALISIS_LEGAL_FINE_TUNING_ESPAÑA.md`

**Conclusión**: ✅ **LEGAL y SEGURO**

```
Fuentes datos:
✅ BOE: Dominio público
✅ CENDOJ: Acceso libre sentencias
✅ Tests oficiales: Uso educativo permitido

Licencias modelos:
✅ Mistral 8B: Apache 2.0 (comercial OK)
✅ Llama 3: Llama 3 License (comercial OK)
✅ SBERT: MIT License (comercial OK)
```

**Riesgo**: ✅ BAJO (fuentes públicas)  
**Estado**: ✅ VALIDADO

---

## 🚀 DEPLOYMENT Y DEVOPS {#deployment}

### 1. ✅ ACTUAL: Vercel (Frontend + Backend)

**Configuración Actual**:
```
Frontend: Vercel Static
Backend: Vercel Serverless Functions (Python)
Database: Qdrant Cloud (1GB free)
Storage: LocalStorage (browser)
```

**Costes**:
```
Vercel Free Tier:
├─ 100 GB bandwidth/mes
├─ Serverless invocations ilimitadas
└─ €0/mes

Qdrant Cloud Free:
├─ 1 GB storage
├─ 10M requests/mes
└─ €0/mes

TOTAL: €0/mes (bajo tráfico)
```

**Límites**:
- ⚠️ 10s timeout serverless functions
- ⚠️ 50MB size límit deploys
- ⚠️ No persistent storage

**Estado**: ✅ PRODUCTIVO  
**Escalabilidad**: ⚠️ Limitada (necesita upgrade a Pro)

---

### 2. ⚠️ ALTERNATIVA: Cloudflare Workers

**Documento**: `ANALISIS_CLOUDFLARE_VS_VERCEL.md`

**Comparativa**:

| Característica | Vercel | Cloudflare Workers |
|----------------|--------|-------------------|
| Free Tier | 100GB/mes | Ilimitado |
| Timeout | 10s | 30s (CPU) |
| Cold Start | ~200ms | ~5ms |
| Edge Locations | ~100 | 200+ |
| Precio Paid | $20/mes | $5/mes |

**Ventajas Cloudflare**:
- ✅ 95% más rápido (cold start)
- ✅ 75% más barato (paid tier)
- ✅ Más edge locations

**Desventajas**:
- 🔴 Lock-in (vendor)
- 🔴 Migración requiere refactor
- 🔴 No Python (solo JS/TS/Rust)

**Recomendación**: ⚠️ **Evaluar si escalamos >1000 users**

**Estado**: 📋 ANÁLISIS COMPLETO  
**Decisión**: ⏸️ PAUSADO (Vercel suficiente ahora)

---

### 3. ⚠️ PROPUESTA: VPS Dedicado

**Documento**: Múltiples menciones en investigaciones

**Caso de uso**: Fine-tuned model serving

**Opciones**:

| Provider | CPU | RAM | Disco | Precio/mes |
|----------|-----|-----|-------|-----------|
| Hetzner | 2 vCPU | 8GB | 160GB | €8 |
| Contabo | 4 vCPU | 8GB | 200GB | €7 |
| OVH | 2 vCPU | 8GB | 160GB | €10 |

**Uso**:
```bash
# Servir Mistral 7B Q4 GGUF con LoRA
mistral-inference \
  --model ~/models/mistral-7b-q4.gguf \
  --lora_path ~/lora/checkpoint_300/lora.safetensors \
  --port 8080

# API endpoint: http://vps-ip:8080/v1/chat/completions
```

**Beneficios**:
- ✅ Control total
- ✅ Costes fijos (€8/mes)
- ✅ No vendor lock-in

**Desventajas**:
- 🔴 Mantenimiento manual
- 🔴 No autoscaling
- 🔴 Seguridad (responsabilidad propia)

**Estado**: 📝 OPCIÓN FUTURA  
**Decisión**: ⏸️ SOLO si fine-tune avanza

---

### 4. ✅ Despliegue «gratis» de Landing/App en tu VPS (España)

Objetivo: Landing pública y UI accesible desde España en el VPS Hostinger (8GB RAM) minimizando costes (sin servicios de pago adicionales).

Pasos sugeridos (estáticos + proxy API si procede):
1) Nginx + Certbot
   - `sudo apt update && sudo apt install -y nginx certbot python3-certbot-nginx`
   - DNS A → IP del VPS; `sudo certbot --nginx -d tu-dominio.es`
2) Build estático frontend
   - `npm ci && npm run build` (output en `dist/` o `build/`)
   - `sudo rsync -av --delete dist/ /var/www/opositaia/`
3) Nginx server block (gzip + cache)
   - `sudo nano /etc/nginx/sites-available/opositaia`
   - root `/var/www/opositaia`; activar gzip estático, long-term cache para assets; proxy_pass a backend si hace falta.
4) Activar sitio
   - `sudo ln -s /etc/nginx/sites-available/opositaia /etc/nginx/sites-enabled/`
   - `sudo nginx -t && sudo systemctl reload nginx`

Resultado: Landing y SPA servidas desde VPS (latencia baja en España), coste 0 adicional.

—

## 🧩 ESQUEMA FACTORÍA DE AGENTES YAML (propuesta breve)

Objetivo: Orquestador delega a subagentes especializados con herramientas MCP compartidas, validación 3 capas y workflows declarativos.

Elementos clave:
- `agents/*.agent.yaml`: definición de cada agente (rol, objetivos, restricciones, herramientas permitidas, parámetros por defecto).
- `manifests/*.csv`: catálogos centrales (agentes, tools, workflows, reglas de verificación) para trazabilidad y versión.
- `workflows/*.workflow.yaml`: orquestaciones multi-agente (steps, paralelismo, handoffs, entradas/salidas, políticas de retries).
- `verification/*.yaml`: reglas L1 (schema), L2 (fact-check legal), L3 (auto-tests/regression).
- MCP Server: `tools/*` registrados (rag_search, boe_verify, jurisprudence_search, content_generator, output_validator).

Ejemplo mínimo de `agents/examiner.agent.yaml`:
```yaml
id: examiner
persona: "Legal Examiner"
goals:
   - generar simulacros basados en BOE y CENDOJ
   - seleccionar preguntas por dificultad y tema
constraints:
   - respuestas justificadas con fuentes oficiales
tools:
   - mcp:rAG_search
   - mcp:boe_verify
outputs:
   schema: schemas/mock_exam.json
   validate: verification/structure.yaml
```

Ejemplo mínimo de `workflows/exam-generation.workflow.yaml`:
```yaml
id: exam-generation
inputs:
   opposition: string
   topics: [string]
steps:
   - agent: examiner
      run: generate_mock_exam
      parallel: 3
   - agent: validator
      run: validate_structure
   - agent: synthesizer
      run: package_exam_bundle
verification:
   - layer: L2
      rule_set: verification/legal_accuracy.yaml
outputs:
   - file: outputs/exams/${opposition}/${date}.json
```

Integración:
- Frontend sigue igual; backend orquesta leyendo YAMLs y llamando MCP tools.
- Compatible con Cloudflare Workers para agentes stateless; mantener FastAPI para rutas complejas.

Estado: propuesta concisa para arrancar Fase 1. Implementación detallada en `PROPUESTA_SISTEMA_AGENTES_YAML.md`.

---

## 📢 MARKETING Y GO-TO-MARKET {#marketing}

### 1. 🔴 PENDIENTE: Estrategia Marketing

**Estado**: ❌ **NO DOCUMENTADO**

**Áreas a desarrollar**:
```
1. Posicionamiento de marca
   - ¿Qué somos? (Asistente IA para oposiciones)
   - ¿Diferenciador? (BYOK, legal sources, RAG 3 capas)
   - ¿Target? (Gen Z opositores técnicos)

2. Canales de adquisición
   - Orgánico: SEO, blog, YouTube
   - Pagado: Google Ads, Facebook Ads
   - Partnerships: Academias, preparadores

3. Pricing strategy
   - Freemium BYOK: €0 (lead magnet)
   - Premium Managed: €9.99/mes
   - Enterprise B2B: €299/mes (50 users)

4. Content marketing
   - Blog: "Cómo usar IA para estudiar oposiciones"
   - YouTube: Tutoriales, cases de éxito
   - Podcast: Entrevistas aprobados

5. Launch plan
   - Beta privada (50 users)
   - Product Hunt launch
   - Prensa especializada oposiciones
   - Influencers educativos
```

**Próximos pasos**:
- [ ] Crear landing page MVP
- [ ] Validar pricing con encuestas
- [ ] Preparar material marketing (screenshots, videos)
- [ ] Identificar canales adquisición

**Prioridad**: 🔴 **ALTA** (sin marketing, sin usuarios)

---

### 2. 🔴 PENDIENTE: Validación de Mercado

**Preguntas a responder**:
```
1. ¿Quién es el usuario ideal?
   - ¿Edad? (Gen Z = 20-30 años)
   - ¿Perfil? (técnico, no técnico)
   - ¿Presupuesto? (€0-30/mes)

2. ¿Qué dolor resolvemos?
   - ¿Estudiar es aburrido? → Gamificación
   - ¿Material disperso? → RAG centralizado
   - ¿Dudas sin resolver? → Chat 24/7
   - ¿Práctica insuficiente? → Casos ilimitados

3. ¿Competencia?
   - Academias online (€100-300/mes)
   - Apps móviles (€10-20/mes)
   - ChatGPT general (€20/mes)
   - Nuestra ventaja: especialización + BYOK

4. ¿Dispuestos a pagar?
   - Encuesta: ¿Cuánto pagarías?
   - A/B testing: €9.99 vs €14.99
   - Lifetime deal: €99 (early adopters)
```

**Métodos validación**:
- [ ] Encuestas Google Forms (50 respuestas)
- [ ] Landing page + email signup
- [ ] Entrevistas 1-on-1 (10 opositores)
- [ ] Beta privada (medir engagement)

**Prioridad**: 🔴 **ALTA**

---

## 🎯 PRÓXIMOS PASOS PARA BRAINSTORMING {#next-steps}

### BRAINSTORMING SESSION: Decisión Estratégica

**Objetivo**: Decidir qué ideas implementar primero

**Participantes (Agentes BMAD)**:
1. **Innovation Strategist** (líder) - evalúa viabilidad
2. **Creative Problem Solver** - genera alternativas
3. **Design Thinking Coach** - UX/usabilidad
4. **Presentation Master** - pitchdeck final
5. **Storyteller** - narrativa de marca

**Temas a Brainstorm**:

#### 1. ARQUITECTURA TECH
```
Decisión: ¿Cloudflare Workers o mantener Vercel?
Opciones:
A) Quedarse en Vercel (simple, funciona)
B) Migrar a Cloudflare Workers (mejor perf, lock-in)
C) Hybrid (Workers para MCP, Vercel para orquestación)

Criterios:
- Tiempo de implementación
- Costes a 1 año
- Mantenibilidad
- Escalabilidad
```

#### 2. MONETIZACIÓN
```
Decisión: ¿BYOK Freemium o Freemium clásico?
Opciones:
A) BYOK (usuarios traen keys) - €0 costes IA
B) Freemium clásico + COSM (packs de simulacros/tests + chat IA) – coste muy bajo por usuario
C) Hybrid (BYOK + Managed tiers + micropagos packs)

Criterios:
- Adquisición usuarios (facilidad signup)
- Costes operativos
- Conversión a pago
- Diferenciación mercado
```

#### 3. FINE-TUNING
```
Decisión: ¿Fine-tune Mistral 8B o usar modelos generales?
 Opciones:
 A) Fine-tune en VPS (Hostinger 8GB) para pruebas legales específicas
 B) Groq 70B sin FT para generalista (rápido y barato)
 C) Híbrido (FT en endpoints legales, Groq para el resto)

Criterios:
- Precisión legal (crítico)
- Tiempo de respuesta
- Costes
- Complejidad mantenimiento
```

#### 4. MARKETING
```
Decisión: ¿Cómo lanzar al mercado?
Opciones:
A) Product Hunt + Beta privada
B) Partnerships con academias (B2B)
C) Influencers educativos + contenido viral
D) SEO + Blog + YouTube orgánico

Criterios:
- Coste adquisición (CAC)
- Tiempo hasta primeros usuarios
- Escalabilidad canal
- Fit con producto
```

---

## 📊 MÉTRICAS CLAVE A DECIDIR

### 1. ⏰ Tiempo de Implementación

| Idea | Tiempo | Prioridad |
|------|--------|-----------|
| Caché prompts | 1 semana | 🔴 Alta |
| Contenido reutilizable (COSM) | 4-5 semanas | 🟡 Media |
| Cloudflare Workers | 2-3 semanas | 🟢 Baja |
| Fine-tune Mistral 8B | 3-4 semanas | 🟡 Media |
| Sistema Agentes YAML | 4-6 semanas | 🟢 Baja |
| Marketing strategy | 2 semanas | 🔴 Alta |

### 2. 💰 Impacto en Costes

| Idea | Ahorro/mes | ROI |
|------|-----------|-----|
| Caché prompts | €0.68 (60%) | Alto |
| Contenido reutilizable | €0.92 (80%) | Alto |
| BYOK Freemium | €26.40 (100%) | Crítico |
| Cloudflare Workers | €8 (27%) | Medio |

### 3. 📈 Impacto en Calidad

| Idea | Mejora | Crítico? |
|------|--------|----------|
| Fine-tune Mistral 8B | +20-25% precisión | ✅ Sí |
| RAG 10K chunks | +15% veracidad | ✅ Sí |
| UX mapas mentales | +engagement | ⚠️ Nice to have |
| Modo oscuro | +estética | ⚠️ Nice to have |

---

## 🚨 DECISIONES CRÍTICAS PENDIENTES

### INMEDIATAS (Esta semana)
1. [ ] **Monetización**: ¿BYOK o Freemium clásico?
2. [ ] **Validación mercado**: Encuestas o beta privada
3. [ ] **Marketing**: Landing page o Product Hunt

### CORTO PLAZO (2-4 semanas)
4. [ ] **Caché prompts**: Implementar (Sprint 11)
5. [ ] **Contenido reutilizable**: Prototipar (Sprint 12)
6. [ ] **Fine-tune**: Comenzar preparar dataset

### MEDIANO PLAZO (1-3 meses)
7. [ ] **Cloudflare Workers**: Evaluar migración
8. [ ] **Sistema Agentes YAML**: Diseñar arquitectura
9. [ ] **B2B partnerships**: Contactar academias

---

## 📝 CONCLUSIONES AUDITORÍA

### ✅ FORTALEZAS
1. **Tech Stack sólido**: Multi-proveedor LLM, RAG 3 capas, MCP Server
2. **Seguridad validada**: GDPR compliant, fuentes legales, APIs seguras
3. **Costes optimizados**: €0.46/mes con caché (98.5% margen)
4. **Arquitectura escalable**: Stateless agents, Qdrant Cloud

### ⚠️ ÁREAS DE MEJORA
1. **Marketing inexistente**: Sin estrategia go-to-market
2. **Validación mercado**: No hemos hablado con usuarios reales
3. **Monetización indefinida**: BYOK vs Freemium + COSM (decidir mix y pricing real)
4. **UX mejorable**: Mapas mentales estáticos, modo oscuro parcial

### 🔴 RIESGOS
1. **Complejidad técnica**: Demasiadas ideas en paralelo
2. **Falta foco**: Arquitectura vs Marketing vs Fine-tuning
3. **Sin usuarios**: Construyendo sin feedback mercado
4. **Burnout**: Muchas tareas, pocas priorizadas


## 🎯 RECOMENDACIONES PARA BRAINSTORMING

### 1. PRIORIZAR IMPACTO vs ESFUERZO

```
IMPACTO ALTO + ESFUERZO BAJO (hacer YA):
✅ Caché prompts (1 semana, 60% ahorro)
✅ Landing page MVP (1 semana, validación)
✅ Encuestas mercado (3 días, feedback)

IMPACTO ALTO + ESFUERZO ALTO (planificar):
⏰ Contenido reutilizable (5 semanas, 80% ahorro)
⏰ Fine-tune Mistral 8B (4 semanas, +25% precisión)
⏰ Estrategia marketing (2 semanas, usuarios)

IMPACTO BAJO + ESFUERZO BAJO (nice to have):
💡 Modo oscuro completo (1 semana, estética)
💡 Exportar mapas PDF (3 días, UX)

IMPACTO BAJO + ESFUERZO ALTO (descartar ahora):
❌ Cloudflare Workers (3 semanas, mejora marginal)
❌ Sistema Agentes YAML (6 semanas, over-engineering)
```

### 2. FOCO EN MVP VALIDATION

**Antes de escalar tech, validar product-market fit**:

```
SPRINT 11 (PRÓXIMAS 2 SEMANAS):
1. Landing page MVP con signup
2. Encuestas a 50 opositores (pricing, features)
3. Beta privada 10 usuarios (medir engagement)
4. Caché prompts (quick win costes)

SPRINT 12 (SEMANAS 3-4):
5. Analizar feedback beta
6. Decidir BYOK vs Freemium
7. Iterar features más solicitadas
8. Preparar material marketing (screenshots, video)

SPRINT 13 (SEMANAS 5-6):
9. Product Hunt launch
10. Primeros 100 usuarios
11. Iterar basado en feedback
12. Decidir siguiente tech mejora (fine-tune?)
```

### 3. EVITAR PARÁLISIS POR ANÁLISIS

**Tenemos suficiente investigación. Ahora: EJECUTAR.**

```
STOP:
❌ Más análisis de arquitectura
❌ Más evaluaciones de modelos
❌ Más documentos de investigación

START:
✅ Hablar con usuarios reales
✅ Lanzar MVP público
✅ Iterar basado en feedback
✅ Generar primeros €
```

---

**FIN AUDITORÍA**

**Próximo paso**: Ejecutar BRAINSTORMING SESSION con agentes BMAD para decidir:
1. Monetización (BYOK vs Freemium)
2. Arquitectura (Vercel vs Cloudflare vs Hybrid)
3. Fine-tuning (Mistral 8B vs Groq 70B vs Hybrid)
4. Marketing (Product Hunt vs B2B vs Influencers)

**Fecha límite decisiones**: 6 Diciembre 2025  
**Responsable**: Spas + Agentes BMAD  
**Output esperado**: Roadmap definitivo Sprints 11-14
