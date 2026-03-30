# PLAN OpositAIA — 26/03/2026
## Análisis de Calidad, Test de Modelos y Desarrollo COSMIC

> **Redactado:** Windsurf/Cascade · 26 Marzo 2026  
> **Prioridad absoluta del proyecto:** CALIDAD y VERACIDAD > velocidad. No podemos enseñar mal a los opositores.

---

## ⚠️ CORRECCIONES CRÍTICAS DE TERMINOLOGÍA

Antes de cualquier acción, estas confusiones deben estar claras:

| Término | Realidad |
|---------|----------|
| **Diego de Miguel (DM)** | Temario Bloque Específico `08.01.2026` — el archivo de ~500 páginas: `academias/1_casos_recientes_2026_DM/criticas18__03_26/Temario_Bloque_Específico_08.01.2026.md` |
| **Academia Las Cortes** | Archivo `8019-RecopilatorioDeLosVillancicosDeLosSupuestosPracticos-Signed_EnDesarrollo_ANONIMIZADO.txt` ("los Villancicos"). Es valioso pero NO es DM. |
| **Gemelos DM** | Los casos del directorio `academias/1_casos_recientes_2026_DM/` son los ejercicios prácticos de DM (Ejercicio 19, etc.), no el temario teórico |
| **Salamandra** | Descartada. No se usa. Modelos actuales: Mistral Large, DeepSeek R1, Groq, Gemini |

---

## 🔢 INVENTARIO DE RECURSOS DE ACADEMIAS

### Archivos SS — Casos Prácticos y Simulacros (242 total en `textos_limpios/`)

| Archivo | Academia | Tipo | Relevancia |
|---------|----------|------|------------|
| `8019-RecopilatorioVillancicos...` | **Las Cortes** | Supuestos prácticos SS | ⭐⭐⭐⭐ MUY ALTA |
| `5001-SimulacroSegSoc11julio24` | Academia SD | Simulacro SS 70 preguntas | ⭐⭐⭐⭐ |
| `5003-SimulacroSegSoc26sep24` | Academia AQ | Simulacro SS + respuestas | ⭐⭐⭐⭐ |
| `5004-SimulacroSegSoc_24oct24` | Academia SD | Simulacro SS | ⭐⭐⭐ |
| `5005-PuertasAbiertas-SegSoc31oct24` | Academia AQ | Simulacro "puertas abiertas" | ⭐⭐⭐ |
| `5006-SimulacroSegSoc-4nov-24` | Academia SD | Simulacro SS | ⭐⭐⭐ |
| `5007-SimulacroSegSoc-18nov24` | Academia SD | Simulacro SS | ⭐⭐⭐ |
| `Medalleros y supuestos ss...` | Mixta | Plantillas supuestos | ⭐⭐⭐ |
| `8038/8039/8040-Esquemas SS` | Sara D./Hidalgo/Hernández | Esquemas SS | ⭐⭐ |

### Archivos AGE (para COSMIC overlap)

| Prefijo | Tipo |
|---------|------|
| `4095, 4100, 4105-4110` | Simulacros AGE C1 (7 simulacros) |
| `8014, 8023 (x5)` | Exámenes reales + simulacros AGE C1 |
| `8024, 8029` | AEAT exámenes y simulacros |

### El Temario DM — Bloque Específico (13 TEMAs, 17.662 líneas)

```
TEMA  1: líneas    11 –    795  (~785 líneas)   ← EXCLUIR del análisis Claude
TEMA  2: líneas   796 –  2.922  (~2.127 líneas) ← EXCLUIR del análisis Claude
TEMA  3: líneas 2.923 –  4.089  (~1.167 líneas) ← INCLUIR
TEMA  4: líneas 4.090 –  5.550  (~1.461 líneas) ← INCLUIR ⭐ CRÍTICO
TEMA  5: líneas 5.551 –  7.082  (~1.532 líneas) ← INCLUIR
TEMA  6: líneas 7.083 –  8.507  (~1.425 líneas) ← INCLUIR
TEMA  7: líneas 8.508 –  9.802  (~1.295 líneas) ← INCLUIR
TEMA  8: líneas 9.803 – 11.669  (~1.867 líneas) ← INCLUIR ⭐ CRÍTICO
TEMA  9: líneas 11.670 – 12.990 (~1.321 líneas) ← INCLUIR
TEMA 10: líneas 12.991 – 14.432 (~1.442 líneas) ← INCLUIR
TEMA 11: líneas 14.433 – 15.706 (~1.274 líneas) ← INCLUIR
TEMA 12: líneas 15.707 – 17.101 (~1.395 líneas) ← INCLUIR
TEMA 13: líneas 17.102 – 17.662 (~561 líneas)   ← INCLUIR
```

**Justificación de exclusiones:**
- **TEMA 1** (SS en Constitución + TRLGSS introductorio): Solo teoría conceptual. NO aparece en supuestos prácticos de examen. Sin cálculos ni trampas de cálculo.
- **TEMA 2** (Campo de aplicación, estructura del sistema): Conceptual. El encuadramiento específico (altas, bajas, sistemas especiales) está en TEMA 3 con más detalle.
- **TEMAs 3-13**: TODOS contienen secciones de "PREGUNTAS DE OTRAS CONVOCATORIAS" y reglas con cálculos. Son los temas que aparecen en el supuesto práctico C1 SS.

---

## 💰 ANÁLISIS DE COSTES: CLAUDE OPUS

### Capacidad técnica
- **Ventana de contexto Claude Opus 4**: 1.000.000 tokens
- **Tamaño archivo DM completo**: ~1.197.040 bytes ≈ **~300.000 tokens**
- **TEMAs 3-13 únicamente** (líneas 2923-17662): ~83% del archivo ≈ **~250.000 tokens**
- **El archivo SÍ cabe en una sola llamada** con Claude Opus (con margen de sobra)

### Estimación de coste (Claude Opus 3 como referencia: $15/M input)
| Escenario | Tokens aprox. | Coste input | Coste output (~5K tokens) | Total |
|-----------|--------------|------------|--------------------------|-------|
| Archivo completo (T1-T13) | 300.000 | $4,50 | $0,37 | **~$5** |
| Solo TEMAs 3-13 (relevantes) | 250.000 | $3,75 | $0,37 | **~$4** |
| Análisis por lotes de 3 temas | 65.000 x4 | $0,97 x4 | $0,37 x4 | **~$5** |

> **Recomendación**: Enviar TEMAs 3-13 en UNA sola llamada (~$4 total). La ventaja es que Claude ve las interdependencias entre temas (por ejemplo, cotización en TEMA 4 se conecta con jubilación en TEMA 8). Fragmentar destruye ese contexto.

### Estrategia de uso de Claude Opus (CARA → solo para lo que merece la pena)
1. **Una sola llamada**: TEMAs 3-13 DM → extraer trampas, cálculos, estilo, porcentajes por tema
2. **No usar Claude para**: análisis de simulacros test (Groq/Gemini son suficientes y mucho más baratos)
3. **Usar Claude para verificación final**: antes de entregar cualquier caso al usuario → 1 llamada por caso

---

## 🤖 FASE 0 — TEST DEL MOTOR V14

### Modelos a evaluar (en orden de prueba)

| # | Modelo | Coste aprox. | Disponibilidad |
|---|--------|-------------|----------------|
| 1 | **Mistral Large** | ~$2/M | API Mistral (ya integrado) |
| 2 | **DeepSeek R1** | ~$0,55/M | API DeepSeek (ya integrado) |
| 3 | **Groq (LLaMA 3.3 70B / Gemma)** | ~$0,06/M | API Groq (muy barato, NO gratis) |
| 4 | **Gemini 1.5 Pro** | ~$1,25/M | API Google |
| 5 | **Claude Opus** | ~$15/M | Solo para QA final si otros fallan |

### Criterios de evaluación (0–10 por criterio)

| # | Criterio | Descripción | Peso |
|---|----------|-------------|------|
| A | **Veracidad legal** | ¿Cita artículos correctos? ¿Los datos normativos son exactos? | 25% |
| B | **No-alucinación numérica** | ¿El ProseValidator lo bloquea? ¿Los números coinciden con el Schema? | 25% |
| C | **Estilo narrativo DM** | ¿Suena como Diego de Miguel? Trama, nombres, complejidad | 20% |
| D | **Similitud a casos DM reales** | ¿Podría confundirse con un caso auténtico de DM? Estructura, interconexión, "veneno" entre preguntas | 20% |
| E | **Veracidad y realismo** | ¿El caso es posible en la vida real? ¿Las situaciones son verosímiles (personas reales con contratos reales)? ¿Nada fantástico ni imposible? | 10% |

**Umbral mínimo para uso en producción**: ≥8,0/10 promedio ponderado  
**Umbral para uso sin QA Claude**: ≥9,0/10 en criterios A+B combinados

### Cómo ejecutar el test

```bash
# 1. Ejecutar test E2E con Mistral (ya configurado)
cd /home/spas/OPOS_GEMINI_1
python backend/scripts/test_e2e_v14_mistral.py

# 2. Para otros modelos: cambiar la variable MODEL_PROVIDER en .env.backend
# y re-ejecutar. Evaluar output manualmente con la rúbrica de 5 criterios.
```

### Decisión post-test

```
SI modelo X supera 8.0/10 → usar X como modelo principal de generación
SI ninguno supera 8.0/10 → arquitectura híbrida:
    - Draft con Groq (barato, rápido)
    - Validación/reescritura con Claude Opus ($15/M)
    - Solo así sale al usuario
```

---

## 🔬 FASE 1A — ANÁLISIS DEL TEMARIO DM CON CLAUDE OPUS

### Objetivo
Extraer del Temario DM Bloque Específico (TEMAs 3-13):
1. **Inventario de trampas** por tema (nuevas, para el catálogo YAML)
2. **Cálculos y fórmulas** por tema (para nuevas calculadoras Python)
3. **Porcentaje de aparición** de cada tema en supuestos prácticos de convocatorias anteriores
4. **Reglas con excepciones** (las que DM usa como "veneno" entre preguntas)
5. **Mnemónicos y organizadores** del propio DM (así sabremos cómo enseña él)

### Prompt a usar con Claude Opus (TEMAs 3-13)

```
Eres un experto en preparación de oposiciones de Seguridad Social (C1 SS España).
Analiza este temario de Diego de Miguel (Bloque Específico, versión 08.01.2026).
Extrae para cada tema:
1. Lista de TRAMPAS pedagógicas (normas que se confunden frecuentemente)
2. CÁLCULOS que aparecen con sus fórmulas y artículos de ley
3. REGLAS CON EXCEPCIONES que pueden usarse en preguntas interdependientes
4. % estimado de aparición en supuestos prácticos (basado en preguntas de convocatorias incluidas)
5. Casos de examen de convocatorias anteriores mencionados

Devuelve el resultado en JSON estructurado.
```

### Output esperado
- Nuevo lote de 50+ trampas para `catalogo_trampas.yaml`
- 10+ nuevas calculadoras identificadas (a implementar en Python)
- Tabla de frecuencia por tema para priorizar blueprints

---

## 🔬 FASE 1B — ANÁLISIS DE SIMULACROS Y CASOS DE ACADEMIAS

### Archivos a analizar (por orden de prioridad)

| Prioridad | Archivo | Por qué |
|-----------|---------|---------|
| ⭐⭐⭐⭐⭐ | `8019-Villancicos (Las Cortes)` | Supuestos prácticos completos con solución. Estructura narrativa. |
| ⭐⭐⭐⭐ | `5001-5007 Simulacros SS` | Estadísticas reales de qué temas aparecen y con qué frecuencia |
| ⭐⭐⭐ | `Medalleros y supuestos SS` | Plantillas de práctica → estructura típica de caso |

### Datos a extraer por cada caso/simulacro

```
Para cada CASO PRÁCTICO:
  - Temas cubiertos (cotización, jubilación, IT, encuadramiento, etc.)
  - Número de preguntas por tema
  - Tipos de trampa (numérica / conceptual / plazo / jurisprudencial / asesor erróneo)
  - Dificultad (1-5)
  - ¿Preguntas interdependientes? (la respuesta de P3 cambia P7)
  - Nº de personajes y tipo de relación (familia, empresa, empleador)
  - Temas "veneno" (la excepción que nadie recuerda)

Para cada SIMULACRO TEST:
  - Distribución de preguntas por tema (generar tabla de frecuencias)
  - Preguntas de trampa identificadas (para catalogo_trampas.yaml)
  - Dificultad media
```

### Output esperado: "Fingerprint DM"

```yaml
fingerprint_DM:
  distribucion_temas_supuesto_practico:
    encuadramiento_altas_bajas: 25%
    cotizacion_bases_cuotas: 30%
    jubilacion: 15%
    IT_maternidad_nacimiento: 10%
    IP: 10%
    recaudacion_recargos: 10%
  num_personajes_tipico: 3-5
  preguntas_interdependientes: true
  temas_veneno_frecuentes:
    - Art. 237.3 TRLGSS (IT vs nacimiento)
    - Sistemas especiales (hogar, agrario)
    - Gran Incapacidad (55% + 45%)
    - Automaticidad Art. 167
```

---

## 🏗️ FASE 2 — 20 BLUEPRINTS RESTANTES

### Estado actual (5 blueprints operativos)
- `bp_s05_encuadramiento.py` → Encuadramiento/altas
- `bp_s10_desempleo.py` → Desempleo
- `bp_s11_muerte_supervivencia.py` → Muerte y supervivencia
- `bp_s12_jubilacion_2026.py` → Jubilación (con BR Dual, Gran Incapacidad)
- `bp_s16_pnc_imv_brecha.py` → PNC + IMV

### 20 pendientes — Orden de prioridad (basado en fingerprint, ajustar tras FASE 1B)

| Orden | Blueprint | Tema DM | % estimado en casos |
|-------|-----------|---------|---------------------|
| 1 | `bp_s01_cotizacion_base.py` | TEMA 4 — Cotización general | 30% |
| 2 | `bp_s02_cotizacion_he_especial.py` | TEMA 4 — HE, sistemas especiales | 20% |
| 3 | `bp_s03_it_contingencias.py` | TEMA 6 — IT CC y CP | 15% |
| 4 | `bp_s04_maternidad_nacimiento.py` | TEMA 6 — Nacimiento, cuidado menor | 10% |
| 5 | `bp_s06_ip_grados.py` | TEMA 7 — IP (grados, cuantías) | 10% |
| 6 | `bp_s07_recaudacion.py` | TEMA 5 — Recaudación, recargos, embargo | 10% |
| 7 | `bp_s08_reta_autonomos.py` | TEMA 10 — RETA | 8% |
| 8 | `bp_s09_sistema_hogar.py` | TEMA 11 — SE Empleados Hogar | 5% |
| 9-20 | Regímenes especiales, viudedad, orfandad, FOGASA... | TEMAs 9-13 | resto |

> **Nota**: El orden exacto se revisará tras obtener el fingerprint real de FASE 1B.

---

## 🌌 FASE 3 — COSMIC: 100 Casos + 1000 Preguntas

### Arquitectura COSMIC (Create Once, Serve Many)

```
25 Blueprints (tras FASE 2)
    ↓
CaseSchemaBuilder orquesta 2-4 blueprints → 1 CaseSchema JSON
    ↓
LLM genera narrativa (modelo validado en FASE 0)
    ↓
ProseValidator + 7 sieves → bloquea cualquier alucinación
    ↓
100 casos validados
    ↓
Cada caso: 15 preguntas + 3 reserva = 1.800 preguntas base
    ↓
Ensamblaje de simulacros por nivel:
  - Básico (1 blueprint, 1 personaje, 10 preguntas)
  - Medio (2 blueprints, 3 personajes, 15 preguntas)
  - DM-Style (3-4 blueprints, 5+ personajes, interdependencias, 18 preguntas)
```

### Criterios de aceptación (OBLIGATORIOS, sin excepción)

```
✅ ProseValidator: 0 alucinaciones numéricas (score = 1.0)
✅ VerificationOrchestrator: 7 sieves, todos ≥ umbral mínimo
✅ Revisión humana: spot-check 1 de cada 5 casos antes de publicar
✅ Realismo: los personajes, empresas y situaciones deben ser verosímiles
✅ Complejidad DM: al menos 3 temas interconectados por caso
```

---

## 📐 ARQUITECTURA V14 ACTUAL (REFERENCIA)

```
Blueprint Python (calculadoras determinísticas)
    ↓
CaseSchemaBuilder → Neo4j (7.106 artículos normalizados) + catálogo_trampas.yaml
    ↓
CaseSchema JSON (BR exacta, pensión exacta, trampas seleccionadas)
    ↓
LLM (solo narra, PROHIBIDO inventar números)
    ↓
ProseValidator → bloquea si LLM cambió cualquier número
    ↓
VerificationOrchestrator (7 sieves: BOE, pedagogía, trampa-distractor, interdependencia...)
    ↓
Caso final → Usuario
```

**Flujo de generación de un caso validado en sesión 24/03/2026:**
- Primer caso blindado: **Jorge Cuesta** — BR: 2.142,86€, Pensión: 1.825,29€ — 0 alucinaciones

---

## 🗂️ ESTADO DE SPRINTS (referencia)

| Sprint | Estado | Descripción |
|--------|--------|-------------|
| S0 | ✅ | 6 cambios DM 2026 en blueprints (BR Dual, Gran Incapacidad, MEI 0.90%, etc.) |
| S1 | ✅ | `verification_agents.py` con 4 sieves reales |
| S2 | ✅ | Neo4j poblado y normalizado (7.106 nodos) |
| S4 | ✅ | `boe_api_client.py` con `verify_article_exact()` |
| S5a | ✅ | `CaseSchemaBuilder` + 2 calculadoras DM 2026 |
| S2.5 | ⏳ | Análisis profundo DM temario con Claude Opus → FASE 1A de este plan |
| S3 | ⏳ | Extracción automática academias → FASE 1B de este plan |
| S5b | ⏳ | 20 blueprints restantes → FASE 2 de este plan |
| S6 | ⏳ | Prose Validator reforzado |
| S7 | ⏳ | Batería CI 125 evaluations |
| S10 | ⏳ | Certificación 10 casos → 0 errores → ≥9.5/10 |

---

## 🚫 OUT OF SCOPE (por ahora)

- ~~Stripe (Trial €1 + Pro €69)~~ → En FASE 3 tardía, después de producto estable
- ~~Autenticación Clerk~~ → Después de producto estable
- ~~App nativa iOS/Android~~ → Muy posterior
- ~~Análisis AGE~~ → Después de SS consolidado

---

## 📋 PRÓXIMAS ACCIONES INMEDIATAS

| # | Acción | Responsable | Coste |
|---|--------|-------------|-------|
| 1 | Ejecutar `test_e2e_v14_mistral.py` y evaluar resultado | Windsurf | Coste API Mistral |
| 2 | Trocear Temario DM en 13 archivos (script bash, líneas exactas conocidas) | Windsurf | $0 |
| 3 | Enviar TEMAs 3-13 DM a Claude Opus para extracción de trampas+cálculos | Manual + Windsurf | ~$4-5 |
| 4 | Analizar `8019-Villancicos (Las Cortes)` para fingerprint de casos prácticos | Windsurf | Coste API barata |
| 5 | Implementar blueprints S01 y S02 (cotización, más frecuente) | Windsurf | $0 |

---

*Firmado: Windsurf/Cascade + Spas · 26/03/2026*
