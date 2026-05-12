# Auditoría OpositAIA v14.5 — 04/05/2026

> Trabajo de campo: smoke test caso v14.5 (BP-S12+S10+S11+S16) + revisión cruzada con BOE oficial (MCP) + Neo4j + análisis local de 6 supuestos de referencia externa (uso interno del autor, NO ingestados).
>
> **Conclusión global**: el redactor v14 (Mistral) es sólido. **Los fallos detectados son del LADO de los blueprints + Prose Validator**, no del LLM ni de la ingesta BOE.

---

## 0 · ⚠️ Reglas Capitales (LEER ANTES DE TODO)

### 0.1 — Anonimización TOTAL en Neo4j (derechos de autor)

**PROHIBIDO** en cualquier nodo, propiedad, relación o índice del grafo:

- Nombres de academias o autores externos.
- Identificadores de supuestos externos (`S_22`, `Simul Nº1`, etc.).
- Nombres propios de personajes copiados de fuentes externas.
- Enunciados literales de preguntas de fuentes externas.
- Rutas de PDFs / archivos de fuentes externas.
- Cualquier campo que insinúe origen externo (`fuente_dm`, `pdf_path`, `tipo: "supuesto_dm"`, etc.).

**OBLIGATORIO**:

- Casos en Neo4j son **siempre `CasoEntrenamiento`** creados internamente por nuestro pipeline. Nunca importados de fuentes externas.
- Personajes son **`RolPersonaje`** genéricos (`trabajador_autonomo`, `socio_administrador_societario`, `pensionista_jubilacion_anticipada`, etc.). Sin nombres propios.
- Preguntas guardan `tematica` (qué se pregunta, descrito en términos genéricos) pero **NUNCA enunciado literal**.
- Las trampas se describen por mecánica genérica (`ejemplo_canonico`), nunca con cita o referencia a fuente externa.
- La LLM debe poder **entender** la mecánica de cada trampa sin acceder a información sobre su origen.

### 0.2 — Veracidad y proceso de validación (sin prisa)

Antes de marcar un `CasoEntrenamiento` como `validado=true` y permitir su uso productivo:

1. **Generación con IA principal** (p.ej. Mistral large latest).
2. **Cross-check con IA secundaria** (Gemini, Groq, DeepSeek vía LiteLLM wrapper) — comparar respuestas a las mismas preguntas.
3. **Verificación cifras** contra Neo4j BOE consolidado (calculadoras de blueprints — ya verificadas).
4. **Verificación artículos** citados ⊆ `articulos_obligatorios` de los blueprints involucrados ∪ `contexto_legal` provisto.
5. **Supervisión humana** (Cascade + autor) revisando: coherencia normativa, vigencia, ausencia de alucinaciones, calidad pedagógica.
6. Solo entonces `validado=true` y se ingiere en Neo4j como `CasoEntrenamiento`.

**Sin prisa**. Es preferible 5 casos validados a 50 sin verificar. La calidad pedagógica del producto depende de esto.

### 0.3 — Material externo: solo memoria de trabajo del autor

Los textos analizados HOY (en `/tmp/dm_*.txt` y carpeta `academias/`) son **material de estudio LOCAL del autor**, exclusivamente para:

- Detectar **patrones narrativos genéricos** (A, B, C) — abstractos, sin contenido.
- Catalogar **mecánicas de trampa** (TPL, TCM, TCT, TRQ, TEC, TCP, TSE, TAR, TIN) — codificadas sin texto literal.
- Diseñar la **taxonomía** del grafo.

**Estos textos NO se ingieren en Neo4j, NI se citan en código productivo, NI se exponen a ningún LLM en runtime**. Permanecen como referencia del autor en su disco local. La inferencia de patrones se queda en el catálogo abstracto (sección 4 + sección 5 de este documento).

---

## 1 · Verificación BOE — la ingesta NO está mal

Comprobación directa contra `mcp_boe_get_law_text_block(BOE-A-2015-11724, a190)`:

- **Art. 190 TRLGSS** tiene 4 apartados (1, 2, 3, 4). Idéntico a Neo4j. **NO existe `190.5`**.
- Última versión vigente: 17/03/2023 (RDL 2/2023, BOE-A-2023-6967). Sin reformas posteriores que añadan apartados.
- **Veredicto**: la ingesta del BOE es **correcta**. La cita "Art. 190.5 TRLGSS" en el caso v14.5 es **alucinación pura del LLM** (Mistral inventó el apartado).

## 2 · Auditoría de los 10 blueprints v14

### 2.1 — Blueprints CON FALLO

| Blueprint | Fallo | Corrección |
|---|---|---|
| **BP-S11** `nacimiento_2026` | Tema declara `"19 semanas"` en su título, pero la duración legal vigente 2026 es **16 semanas obligatorias** (Art. 48 ET + RDL 5/2023). 19 no aparece en ningún texto BOE. | Cambiar título y `articulos_obligatorios` para incluir `Art. 48 ET` + `Art. 177 TRLGSS`. Eliminar mención "19". |
| **BP-S11** `nacimiento_2026` | `articulos_forbidden=["Art. 237 TRLGSS (para IT)"]` — el paréntesis ES un comentario en mitad del valor → match string fallará. | Limpiar a `["Art. 237 TRLGSS"]` y mover el comentario a un campo `notas`. |
| **BP-S16** `pnc_imv_brecha` | Mezcla en el mismo blueprint: `Art. 369` (PNC jub), `Art. 363` (PNC IPP) **y** IMV (`Ley 19/2021`), pero NO declara explícitamente la `Ley 19/2021` en `articulos_obligatorios`. Esto induce al LLM a confundir IMV con PNC. | Separar: declarar `["Art. 11 Ley 19/2021", "Art. 369 TRLGSS", "Art. 60 TRLGSS"]` y mover Art. 363 a un blueprint distinto BP-S16b o eliminar de aquí. |
| **BP-S10** `incapacidad_permanente` | Falta `Art. 174 TRLGSS` (extinción IT 545 días) y `Art. 196 TRLGSS` (cuantías IPP/IPT/IPA/GI). El caso v14.5 los citó por intuición, pero no estaban obligatorios. | Añadir ambos a `articulos_obligatorios`. |
| **BP-S12** `jubilacion_2026` | `articulos_obligatorios` no incluye `Art. 205 TRLGSS` (acceso jubilación), aunque sí menciona `204` (anticipada) y `209/210` (cálculo). Mezcla "ordinaria" con "anticipada" sin separar. | Añadir `Art. 205 TRLGSS`. Considerar separar en BP-S12a (ordinaria) y BP-S12b (anticipada). |

### 2.2 — Blueprints OK (sin fallos detectados)

- BP-S02 `encuadramiento_reta` ✅
- BP-S04 `afiliacion_alta_baja` ✅
- BP-S05 `cotizacion_2026` ✅ (con MEI + Adicional Solidaridad bien declarados)
- BP-S06 `recargos_intereses` ✅
- BP-S07 `recaudacion_ejecutiva` ✅
- BP-S13 `jubilacion_anticipada_activa` ✅

### 2.3 — Anti-alucinación: regla nueva en redactor

Añadir al `system_prompt` de `redactor_v14.yaml`:

> **REGLA 8 (NUEVA)**: NO PUEDES citar apartados específicos de un artículo (Art. X.5, Art. X.2.b) salvo que aparezcan literalmente en `articulos_obligatorios` o `contexto_legal`. Si necesitas precisar apartado y no lo tienes, cita el artículo entero.

---

## 3 · Patrones narrativos DM — son TRES, no uno

Tu intuición era correcta: **NO siempre hay trama familiar entrelazada**. Confirmado tras leer 6 casos:

### Patrón A · "Cronología vital de un protagonista" (S_21 María Trinidad)

- **1 personaje protagonista** que vive todos los eventos.
- Cronología larga (2007 → 2026): empleo → maternidad → desempleo → cese → segunda maternidad → COVID → 65 años.
- Las preguntas siguen la línea temporal en orden.
- **Sin más personajes** (o aparece el cónyuge/hijo solo como dato).

### Patrón B · "Bloques bruscos sin conexión" (S_22 Fernando, S_20 Silvia)

- **3-5 personajes diferentes** introducidos uno tras otro.
- Cada bloque es independiente; transición brusca con párrafo nuevo: *"Por su parte..."* / *"José Martínez nació..."* / *"Luis y Katrina conviven..."* / *"María Luisa tiene 14 años..."*.
- 3-4 preguntas por personaje.
- **Ningún vínculo entre los personajes** (ni familiar ni laboral).

### Patrón C · "Empresa eje + entorno laboral/familiar" (Simul Nº1 Manuel, casos NIDO DEL ALBA, ZENITH-CONTINENTAL nuestro)

- 1 empresa central + protagonista (administrador/socio) + trabajadores + asesor.
- Personajes secundarios pueden ser familia, pero **no es obligatorio**.
- Eventos: alta empresa, contrataciones, viajes/dietas, cotización adicional.

### Implicación para nuestro pipeline

El `CaseSchemaBuilder` actual y el `redactor_v14` solo generan **Patrón C**. Debe permitir elegir patrón:

```python
schema = builder.build_complex(
    blueprint_ids=[...],
    fecha_caso="2026-03-04",
    patron_narrativo="A" | "B" | "C",   # NUEVO PARÁMETRO
)
```

Y el `redactor_v14.yaml` debe tener **3 few-shots distintos** (uno por patrón), seleccionados según el campo del schema.

---

## 4 · Catálogo de trampas — mecánicas genéricas

Patrones de inducción al error catalogados a partir de análisis abstracto de mecánicas (sin texto literal). Codificación: `T<categoría>-<nº>`. Cada trampa describe un patrón cognitivo que la pregunta puede activar; el grafo Neo4j almacenará solo la mecánica, nunca su origen ni ejemplos literales.

### TPL · Trampas de PLAZO (las más frecuentes)

| ID | Trampa | Ejemplo canónico |
|---|---|---|
| TPL-01 | Día hábil vs natural en cómputos de plazo en festivo | Plazo natural en festivo desplaza al siguiente día hábil. |
| TPL-02 | Cómputo desde día cese vs día siguiente | Algunos plazos cuentan desde día efectos, otros desde día siguiente al hecho. |
| TPL-03 | Plazo máximo IT 545 días naturales por contingencias comunes | Art. 174 TRLGSS. |
| TPL-04 | Plazo evaluación IP tras agotar IT (3 meses para calificación) | Posterior a Art. 174 TRLGSS. |
| TPL-05 | Prescripción pensiones: imprescriptible vs 5 años + efectos retroactivos | Distinción según contributiva/no contributiva. |
| TPL-06 | Plazo subsanación recurso: 10 vs 15 días | Art. 115 LPACAP. |
| TPL-07 | Vencimiento documento asociación mutua: 31/12 vs 31/01 vs 1/10 | RGRSS. |

### TCM · Trampas de COMPETENCIA

| ID | Trampa | Ejemplo |
|---|---|---|
| TCM-01 | INSS vs TGSS vs Mutua vs SEPE: gestión vs entidad gestora | Cobertura IT puede separarse de cobertura CC profesionales. |
| TCM-02 | Director provincial INSS vs Presidente EVI vs Inspector Médico vs Facultativo SPS | Resolución expediente IP. |
| TCM-03 | URE provincia origen vs URE provincia bien embargado | Recaudación ejecutiva. |
| TCM-04 | Cobertura IT obligatoria conjunta o separada de CC | Régimen de opciones por mutua. |

### TCT · Trampas de CUANTÍAS / PORCENTAJES

| ID | Trampa | Ejemplo |
|---|---|---|
| TCT-01 | BR Dual jubilación 2026 (300/348/360 mejores meses según años) | BP-S12. |
| TCT-02 | % pensión por años (50 % base + 0,21 %·48m + 0,19 %·…) | BP-S12. |
| TCT-03 | Recargos: 10 % / 20 % / 35 % según mora | BP-S06. |
| TCT-04 | Tanto alzado IPT por edad: 24 (58 a) / 36 (57) / 60 (55) mensualidades | BP-S10 + OM 31-01-1970. |
| TCT-05 | % jubilación activa: 45 % / 55 % / 65 % / 75 % según supuesto | BP-S13. |
| TCT-06 | Complemento demora jubilación: 4 % / 8 % / 10 % / 12 % por años extra | BP-S13. |
| TCT-07 | Brecha género cuantía LPGE 2026 (varía año) | Verificar contra LPGE 2026 vigente. |
| TCT-08 | Pensión orfandad: % BR mín / LPGE / viudedad no asignada | Múltiples preceptos. |
| TCT-09 | Subasta SS: depósito 20/25/30/35 % del tipo | Art. 118 RGRSS. |
| TCT-10 | Cotización adicional solidaridad 2026: 1,15 % distribución empresario/trabajador | BP-S05. |

### TRQ · Trampas de REQUISITOS

| ID | Trampa | Ejemplo |
|---|---|---|
| TRQ-01 | Años cotizados desde **alta** vs desde **no-alta** (15 vs 5 últimos) | Diferencia clave para causar viudedad/orfandad. |
| TRQ-02 | Edad mínima jub anticipada: voluntaria vs involuntaria | BP-S13. |
| TRQ-03 | Residencia: 5 años (PNC IPP) vs 10 años + 2 inmediatos (PNC jub) vs IMV | BP-S16 + Ley 19/2021. |
| TRQ-04 | Discapacidad: 33 % / 45 % / 65 % / 75 % | Art. 3 RD 1539/2003. |
| TRQ-05 | Período de cotización mínimo causante (100 días, 500 días, 24 meses) | Carencia variable según contingencia. |
| TRQ-06 | Pareja de hecho: inscripción ≥1 año + convivencia ≥5 | Requisitos viudedad pareja de hecho. |

### TEC · Trampas de ENCUADRAMIENTO

| ID | Trampa | Ejemplo |
|---|---|---|
| TEC-01 | Socio administrador con retribución: RG asimilado vs RETA según % | Suma de % cónyuges/familiares conviventes ≥50 % → RETA. |
| TEC-02 | Familiar conviviente con hijo del socio: cómputo participación | Art. 305.2 TRLGSS. |
| TEC-03 | Administrador único 100 % SL → RETA obligatorio | BP-S02. |
| TEC-04 | Autónomo societario: deducción gastos genéricos 3/5/7/9 % | Régimen RETA societarios. |
| TEC-05 | Asimilado a CCAA vs CCPP: exclusiones (desempleo, FOGASA) | Art. 12.2 + 305 TRLGSS. |

### TCP · Trampas de COMPATIBILIDAD

| ID | Trampa | Ejemplo |
|---|---|---|
| TCP-01 | Pensión jubilación + IP: optar por una u otra | Incompatibilidad relativa. |
| TCP-02 | IMV incompatible administrador SL ≥50 % control | Art. 11 Ley 19/2021. |
| TCP-03 | Jubilación activa + trabajo: % depende de demora y trabajadores | BP-S13. |
| TCP-04 | Brecha género: solo mujeres salvo casos hombres (viudedad / IP por interrupción carrera) | Art. 60 TRLGSS. |

### TSE · Trampas de SUPUESTO ESPECIAL

| ID | Trampa | Ejemplo |
|---|---|---|
| TSE-01 | Jub anticipada por discapacidad: coef. 0,25/0,50 | Art. 3 RD 1539/2003. |
| TSE-02 | Familias monoparentales: ampliación nacimiento hasta 32 semanas | Art. 48 ET + RDL 5/2023. |
| TSE-03 | Hijos con cáncer/enfermedad grave: extensión hasta 23/26 años | Art. 190.3 TRLGSS. |
| TSE-04 | Días cotización ficticios: 112 días/parto + 270 días/cuidado | Beneficios cotización por hijos. |
| TSE-05 | Empleados de hogar / agrarios / artistas: especialidades | Regímenes especiales SS. |

### TAR · Trampas de ARTÍCULO INVENTADO o INCORRECTO

| ID | Trampa | Ejemplo |
|---|---|---|
| TAR-01 | Cita apartado inexistente (X.5 cuando solo hay 4) | Verificable contra Neo4j BOE. |
| TAR-02 | Cita Art. X bis inexistente | Listado en `articulos_forbidden` de cada blueprint. |
| TAR-03 | Mezcla artículo de norma ≠ con materia (p.ej. Art. 363 TRLGSS para IMV cuando IMV está en Ley 19/2021) | Detectable por cross-check norma↔materia. |

### TIN · Trampas de ¡INVERSIÓN! (propuesta nueva interna)

Trampas donde damos resultado y piden reconstruir datos. No vistas en corpus de referencia, son innovación nuestra. Encajan en arquitectura schema-first sin gran refactor (un agente `inverter_v14.yaml` que oculta 1-2 campos del briefing y reformula la pregunta).

---

## 5 · Diseño de taxonomía Neo4j para trampas + relaciones

### 5.1 — Etiquetas (labels) propuestas — ANONIMIZADAS (cf. sección 0.1)

```cypher
// Trampa: catalogada por mecánica genérica, sin referencia a fuente
(:Trampa {
  id: "TPL-01",                      // identificador estable interno
  categoria: "PLAZO",                // PLAZO | COMPETENCIA | CUANTIA | REQUISITO | ENCUADRAMIENTO | COMPATIBILIDAD | SUPUESTO_ESPECIAL | ARTICULO_INVENTADO | INVERSION
  patron_error: "dia_habil_vs_natural",
  descripcion: "Confunde plazo en días hábiles con días naturales",
  ejemplo_canonico: "Plazo natural que cae en festivo se desplaza al siguiente día hábil",  // descripción genérica, sin cita
  severidad: "alta",                 // alta | media | baja
  frecuencia_estimada: "alta"        // alta | media | baja (sin números asociables a corpus externo)
})

// Caso: SIEMPRE creado internamente por nuestro pipeline. Sin referencia externa.
(:CasoEntrenamiento {
  id: "CE-2026-0001",                // codificación interna
  fecha_creacion: "2026-05-04",
  patron_narrativo: "B",             // A | B | C (cf. sección 3)
  num_personajes: 5,
  num_preguntas: 15,
  ia_generadora: "mistral-large-latest",   // qué modelo lo generó
  ia_validadora: "gemini-2.5-pro",         // qué modelo cross-check
  validado: false,                    // true solo tras supervisión humana (cf. 0.2)
  fecha_validacion: null,
  blueprints_usados: ["BP-S12","BP-S10","BP-S11","BP-S16"]
})

// Rol de personaje: tipo funcional, sin nombres propios
(:RolPersonaje {
  id: "RP-CE-2026-0001-01",
  tipo: "trabajador_cuenta_ajena_jubilable",   // p.ej. trabajador_autonomo, socio_administrador, pensionista_IP, etc.
  edad_aprox: 67,
  caracteristicas: ["35a_cotizados","base_cotizacion_alta"],   // listas genéricas
  caso_id: "CE-2026-0001"
})

// Pregunta: temática descrita, NO enunciado literal
(:Pregunta {
  id: "Q-CE-2026-0001-01",
  numero: 1,
  tematica: "requisitos_acceso_jubilacion_ordinaria_2026",   // qué se pregunta, en términos genéricos
  letra_correcta: "C",
  caso_id: "CE-2026-0001"
  // NO `enunciado` literal
})
```

### 5.2 — Relaciones (relationships)

```cypher
// Estructura caso → preguntas (todo interno)
(:CasoEntrenamiento)-[:CONTIENE]->(:Pregunta)
(:CasoEntrenamiento)-[:PROTAGONIZA]->(:RolPersonaje)

// Pregunta → trampas activadas
(:Pregunta)-[:USA_TRAMPA]->(:Trampa)

// Pregunta → preceptos involucrados
(:Pregunta)-[:CITA_PRECEPTO]->(:Precepto)

// Trampas relacionadas entre sí (confusión típica)
(:Trampa)-[:CONFUNDE_CON]->(:Trampa)
// p.ej. (TPL-01)-[:CONFUNDE_CON]->(TPL-02) "días hábiles vs cómputo desde día siguiente"

// Trampa → blueprint donde aplica
(:Trampa)-[:APLICA_EN]->(:Blueprint)

// Confusión típica entre preceptos (clave para socratismo)
(:Precepto)-[:CONFUNDIBLE_CON {motivo: "ambos PNC pero requisitos distintos"}]->(:Precepto)
// p.ej. (Art. 363 TRLGSS)-[:CONFUNDIBLE_CON]->(Art. 369 TRLGSS)
//        (Art. 363 TRLGSS)-[:CONFUNDIBLE_CON]->(Art. 11 Ley 19/2021)

// Roles relacionados dentro del mismo caso (para Patrón A y C, sin nombres)
(:RolPersonaje)-[:CONYUGE_DE]->(:RolPersonaje)
(:RolPersonaje)-[:HIJO_DE]->(:RolPersonaje)
(:RolPersonaje)-[:EMPLEADO_DE]->(:Empresa)
(:Empresa)-[:FILIAL_DE]->(:Empresa)
// Las empresas son entidades funcionales ("empresa_constructora_mediana", "sociedad_limitada_consultoria")
```

### 5.3 — Queries útiles que esto habilita

```cypher
// 1. ¿Qué trampas existen para Art. 369 TRLGSS?
MATCH (p:Precepto {id:"Art. 369 TRLGSS"})<-[:CITA_PRECEPTO]-(q:Pregunta)-[:USA_TRAMPA]->(t:Trampa)
RETURN DISTINCT t.id, t.descripcion;

// 2. Pares de preceptos confundibles (alimenta árbol socrático)
MATCH (p1:Precepto)-[r:CONFUNDIBLE_CON]->(p2:Precepto)
RETURN p1.id, p2.id, r.motivo;

// 3. Frecuencia de cada trampa en corpus interno validado
MATCH (q:Pregunta)-[:USA_TRAMPA]->(t:Trampa)
MATCH (c:CasoEntrenamiento {validado:true})-[:CONTIENE]->(q)
RETURN t.id, t.categoria, count(q) as frecuencia
ORDER BY frecuencia DESC;

// 4. Casos validados por patrón narrativo
MATCH (c:CasoEntrenamiento {validado:true})
RETURN c.patron_narrativo, count(c);
```

### 5.4 — Plan de carga (anonimizado, sin ingesta externa)

1. **Fase 1**: nodos `:Trampa` (52 IDs catálogados arriba con descripciones genéricas) — script `scripts/seed_trampas_neo4j.py` idempotente.
2. **Fase 2**: nodos `:CasoEntrenamiento` + `:RolPersonaje` + `:Pregunta` **generados internamente** por nuestro pipeline (Builder + Redactor). Cada caso pasa por el flujo de validación de la sección 0.2 (multi-IA + supervisión humana) antes de marcar `validado=true`.
3. **Fase 3**: relaciones `:USA_TRAMPA`, `:CITA_PRECEPTO` — etiquetado asistido por LLM sobre los casos validados (no sobre material externo).
4. **Fase 4**: relaciones `:CONFUNDIBLE_CON` entre preceptos — derivado automáticamente de las trampas categorizadas + revisión humana.
5. **Fase 5**: sync blueprints↔Neo4j (`scripts/sync_blueprints_to_neo4j.py`) → relaciones `:APLICA_EN`.

**NO se implementa** ningún script de ingesta de fuentes externas. Repetir: el grafo solo contiene casos creados internamente.

---

## 6 · Plan de acción priorizado (orden CONFIRMADO con autor — 04/05/2026)

### 6.1 — Bloque inmediato: arreglos de los 3 fallos detectados (P1)

| Prio | Acción | Coste | Impacto |
|---|---|---|---|
| 🔴 **P1.1** | Fix BP-S11 (eliminar "19 semanas", añadir `Art. 48 ET` + `Art. 177 TRLGSS`) | 5 min | Elimina alucinación nº1 (duración nacimiento) |
| 🔴 **P1.2** | Fix BP-S16 (separar PNC IPP de IMV, añadir `Art. 11 Ley 19/2021` explícita) | 10 min | Elimina alucinación nº2 (mezcla PNC↔IMV) |
| 🔴 **P1.3** | Añadir REGLA 8 anti-alucinación apartados al `redactor_v14.yaml` | 5 min | Elimina alucinación nº3 (`Art. X.5` inventado) |

### 6.2 — Auditoría completa de los 24 blueprints restantes (BLOQUE GRANDE)

Las calculadoras y URLs Neo4j de cada blueprint están **verificadas**. La auditoría se centra en:

- `articulos_obligatorios` ⊆ artículos realmente vigentes en BOE.
- `articulos_forbidden` correctamente formulados (sin comentarios entre paréntesis que rompan match).
- `tema` y descripciones internas no contienen valores legales incorrectos (como las "19 semanas" de BP-S11).
- Coherencia entre `personaje_tipo`, `conflictos_cruzados` y `articulos_obligatorios`.

### 6.3 — Otros fixes (P2)

| Prio | Acción | Coste | Impacto |
|---|---|---|---|
| 🟡 **P2.1** | Fix Prose Validator: extraer `art_id` citados en texto LLM y verificar contra `articulos_obligatorios` ∪ `contexto_legal` | 30 min | Detección automática TAR-01/02/03 |
| 🟡 **P2.2** | Añadir parámetro `patron_narrativo: A/B/C` al `CaseSchemaBuilder` + 3 few-shots distintos en `redactor_v14.yaml` | 1 h | Variedad de casos generados |
| 🟡 **P2.3** | LiteLLM wrapper (Mistral → Gemini → Groq → DeepSeek) — necesario para flujo cross-check 0.2 | 1 h | Habilita validación multi-IA |

### 6.4 — Carga Neo4j + sincronización (P3) — ORDEN CONFIRMADO

1. ✅ Calculadoras blueprints — verificadas.
2. ✅ URLs Neo4j de cada blueprint — verificadas.
3. ⏳ **Auditoría 24 blueprints restantes** (sección 6.2).
4. ⏳ **Sync blueprints ↔ Neo4j** (`scripts/sync_blueprints_to_neo4j.py`).
5. ⏳ **Seed Trampas Neo4j** (`scripts/seed_trampas_neo4j.py` con los 52 IDs).
6. ⏳ **Generación casos validados** internamente (multi-IA + supervisión humana, cf. 0.2).
7. ⏳ **Carga `:CasoEntrenamiento` + `:RolPersonaje` + `:Pregunta`** solo de los validados.
8. ⏳ **Etiquetado relaciones `:USA_TRAMPA` + `:CITA_PRECEPTO`**.
9. ⏳ **Derivación relaciones `:CONFUNDIBLE_CON`** entre preceptos.

**Sin prisa**. Cada paso requiere verificación antes del siguiente.

---

## 7 · Anexos

### 7.1 — Material productivo (entra en pipeline)

- `/tmp/narrativa_compleja_v14_5.md` — caso v14.5 generado por nuestro pipeline (smoke test, **aún sin validar**).
- `/tmp/caso_v14_5.html` — render HTML para revisión humana del caso anterior.
- Verificación BOE Art. 190 TRLGSS: `mcp_boe_get_law_text_block(BOE-A-2015-11724, a190)` el 04/05/2026 — apartados 1-4 confirmados.

### 7.2 — Material de estudio LOCAL del autor (NO entra en pipeline ni Neo4j)

> Estos archivos son referencia personal del autor para detectar patrones genéricos. **No se citan, no se ingieren, no se exponen a ningún LLM en runtime**.

- `/tmp/dm_*.txt` (memoria temporal de trabajo del 04/05/2026 — borrar tras consolidar el catálogo de trampas en sección 4 de este documento).
- Carpeta `academias/` — material físico del autor.

Una vez extraídas las mecánicas genéricas (sección 4) y diseñada la taxonomía (sección 5), estos archivos **se pueden borrar de `/tmp/`**. La inteligencia se queda en el catálogo abstracto, no en los archivos.
