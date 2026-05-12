# MEMORIA SISTEMA DE GENERACIÓN DE CASOS PRÁCTICOS — OpositAIA V14
> **Fecha:** 09/04/2026 · **Estado verificado en código real**
> **Objetivo:** Generar casos prácticos al nivel de Diego de Miguel (DM) para monetizar en packs verificados.

---

## 1. FILOSOFÍA CENTRAL: "Schema-First"

El principio fundacional del sistema: **el LLM nunca calcula ni inventa datos legales**. Python prepara un JSON hermético con todos los números, artículos y cálculos verificados. El LLM solo escribe la narrativa alrededor de ese JSON.

> "El LLM es el escritor, Python es el abogado."

---

## 2. PIPELINE E2E COMPLETO

```
[BLUEPRINT (tema)]
      ↓
[CaseSchemaBuilder.build_complex()] ← Python puro, 0 llamadas LLM
      ↓  Lee: catálogo YAML trampas
      ↓  Ejecuta: calculadoras Python
      ↓  Consulta: Neo4j (texto íntegro artículos BOE)
      ↓  Randomiza: nombres/empresas desde nombres_pool.py
      ↓
[JSON Hermético = CaseSchema]
  - personajes[] (nombres únicos, roles, datos calculados)
  - questions[] (opciones A/B/C/D barajadas, letra_correcta, mnemónico)
  - contexto_legal[] (texto real BOE de los artículos)
      ↓
[Mistral Large — redactor_v14.yaml] ← Solo redacta prosa
  - Temperatura: 0.3
  - Max tokens: 8000
  - Few-shot: caso real DM "NIDO DEL ALBA SL"
  - Regla: TODOS los números del JSON, ni uno inventado
      ↓
[ProseValidator] ← Barrera anti-alucinación
  - Extrae todos los números del texto LLM
  - Compara contra CaseSchema
  - Bloqueo automático si hay discrepancia
      ↓
[VerificationOrchestrator] ← 7+ agentes
  - agent_1: BOE/Qdrant (desactivado temporalmente por timeout)
  - agent_4: Coherencia jurídica ✅ funcional
  - agent_5: Solucionario con razonamiento por distractor
  - agent_7: Pedagogía y cruces de roles
  - agent_8: Plausibilidad de distractores
      ↓
[Caso Práctico Final] → /tmp/narrativa_e2e_v14.md
```

**Script de ejecución:**
```bash
cd /home/spas/OPOS_GEMINI_1
source .venv/bin/activate
python backend/scripts/test_e2e_v14_mistral.py
```

---

## 3. BLUEPRINTS — 10 TEMAS ACTIVOS

Directorio: `/home/spas/OPOS_GEMINI_1/backend/v14/blueprints/`

| Blueprint | Tema | Trampas clave |
|-----------|------|---------------|
| `bp_s02` | Encuadramiento RETA | Control efectivo 25%/33%/50%, socios gerentes |
| `bp_s04` | Afiliación/Alta/Baja | Plazos RD 84/1996, efectos alta tardía |
| `bp_s05` | Cotización 2026 | MEI 0.90%, solidaridad, base máx 5.101,20€ |
| `bp_s06` | Recargos e intereses | Tramos 10%/20%/35%, RD 1415/2004 |
| `bp_s07` | Recaudación ejecutiva | URE, embargo, aplazamiento |
| `bp_s10` | Incapacidad Permanente | Grados, carencias, GI=Gran Incapacidad 2026 |
| `bp_s11` | Nacimiento 2026 | 19sem biparental, 32sem monoparental, prematuros |
| `bp_s12` | Jubilación ordinaria 2026 | EOJ 38a3m/66a10m, BR Dual, DT9ª 36a6m |
| `bp_s13` | Jubilación anticipada+activa | Voluntaria/involuntaria, escala RDL 11/2024 |
| `bp_s16` | PNC + IMV + Brecha género | Cuantías 2026, umbral ingresos, 36,90€/mes |

**Estructura de cada Blueprint:**
```python
TopicBlueprint(
    id="BP-S12",
    tema="...",
    normativa_base=["Art. 204 TRLGSS", ...],
    articulos_obligatorios=["Art. 204 TRLGSS", "Art. 209 TRLGSS", ...],
    articulos_forbidden=["Art. 209 bis"],  # No existen — guardia anti-alucinación
    calculadoras=["eoj_2026()", "br_dual()", "porcentaje_pension()"],
    trampas_tipicas=["C1", "C2", "C3", "C4", "C6"],  # IDs del catálogo YAML
    eval_questions=[{...}],  # Banco hardcoded verificado
    notas="..."
)
```

---

## 4. CaseSchemaBuilder — MOTOR CENTRAL

Archivo: `/home/spas/OPOS_GEMINI_1/backend/v14/case_schema_builder.py` (586 líneas)

### Método `build_complex()` — flujo real verificado:
1. **Selecciona 4 blueprints** al azar de los 10 disponibles
2. **Ejecuta `generar_briefing(dispatcher)`** de cada blueprint → datos aleatorios legalmente correctos
3. **Crea empresa central** (del primer blueprint) como eje narrativo
4. **Verifica artículos en Neo4j** → inyecta texto íntegro en `contexto_legal`
5. **Round-robin de preguntas**: 1 pregunta de cada blueprint, repite hasta 18
6. **Baraja A/B/C/D** con `random.shuffle()` y guarda `letra_correcta`
7. **Valida prerrequisitos** (ej. 60 años con <15 cotizados → ajusta automáticamente)
8. Devuelve `CaseSchema` con `validated=True` si ≥15 preguntas

### DataClasses principales:
```python
PersonajeSchema: nombre, rol, edad, datos{}, relaciones[]
QuestionSchema: pregunta_id, trampa_id, articulo, url_boe, calculo_resultado,
                mnemonico, pregunta, distractores[], opciones_ordenadas[],
                letra_correcta, razonamiento, personaje_ref, verified, blueprint_origen
CaseSchema: case_id, blueprint_ids[], personajes[], fecha_caso,
            contexto_legal[], questions[], conflictos_cruzados[], validated
```

---

## 5. CATÁLOGO DE TRAMPAS YAML

Archivos:
- `/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/catalogo_trampas.yaml`
- `/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/catalogo_trampas_adicional.yaml`

**Estado a 09/04/2026:** ~80 trampas en catálogo principal (categorías A-I) + categorías adicionales R (RETA), J (MS), Q (FP), S (Mixtas). PLAN_MAESTRO tiene 300+ trampas identificadas de simulacros DM + Las Cortes.

**Fecha de corte normativa SS: 04/03/2026**

---

## 6. AGENTES — 11 YAMLs

Directorio: `/home/spas/OPOS_GEMINI_1/opos-agents/agents/`

| Agente | Rol | Modelo |
|--------|-----|--------|
| `orchestrator.yaml` | Enrutador CALC/EXAM/SUMM | Groq Llama-3 |
| `redactor_v14.yaml` | **Narrador principal** — schema-bound | Mistral Large (temp=0.3) |
| `examiner.yaml` | Responde preguntas con RAG+calc | DeepSeek V3 CoT |
| `generator.yaml` | Generador tool-first (alternativo) | cloud_reasoning (temp=1.0) |
| `generator_r1.yaml` | Variante R1 | — |
| `validator.yaml` | Validación 2 capas: estructura+semántica | — |
| `resumidor.yaml` | Esquemas, resúmenes, mnemotecnias | — |
| `investigator_v13.yaml` | Investigador (legado V13) | — |
| `compile.yaml` | Utilidad compilación | — |
| `intent.yaml` | Clasificador de intención | — |

---

## 7. CALCULADORAS

Directorio: `/home/spas/OPOS_GEMINI_1/backend/calculators/`

| Archivo | Tamaño | Contenido |
|---------|--------|-----------|
| `calculos_ss_extended.py` | **83KB** | Motor SS: IT, IP, Jubilación, BR Dual, MEI, nacimiento, viudedad, orfandad, IMV, Gran Incapacidad, jubilación activa escala RDL 11/2024 |
| `calculadora_age.py` | **46KB** | AGE/TREBEP: plazos procedimentales, trienios, situaciones administrativas |
| `dispatcher.py` | **31KB** | Router: recibe query lenguaje natural → llama función correcta |
| `calculos_imv.py` | 10KB | IMV completo: cuantías, unidades de convivencia |
| `calculos_ss.py` | 9KB | SS básico |
| `calculadora_presupuesto.py` | 18KB | Presupuesto |

---

## 8. MCP SERVER (TypeScript)

Directorio: `/home/spas/OPOS_GEMINI_1/mcp-server/`

Tools expuestas: `search_rag`, `verify_boe`, `search_jurisprudence`, `generate_flashcards`, `get_law_summary`. Conecta a Qdrant. **Sin build compilado** — hay TODOs pendientes.

---

## 9. NOMBRES POOL

Archivo: `/home/spas/OPOS_GEMINI_1/backend/v14/nombres_pool.py`

- 28 nombres masculinos + 28 femeninos + 42 apellidos españoles
- 25 prefijos empresa (HORIZONTE, NEBULA, SOLARIS...) × 24 sufijos (SOLIDARIO, BYTE, TECH...)
- 6 tipos (SL, SA, SLU, S.Coop., SAL, SLL)
- Ejemplo: `HORIZONTE-SOLIDARIO SL`, `NEBULA-BYTE SA`, `SOLARIS-TECH SLU`
- 25 ciudades, 14 sectores

---

## 10. ESTADO REAL A 09/04/2026

### ✅ Funcionando
- `build_complex()` genera 4 personajes con datos únicos por ejecución
- Shuffle A/B/C/D correcto — `letra_correcta` almacenada en schema
- Objetivo 18 preguntas implementado correctamente
- ProseValidator anti-alucinación numérica operativo
- agent_4 coherencia jurídica 100%
- Mnemónicos, razonamiento por distractor: implementados en prompt redactor_v14

### 🔴 BUG CRÍTICO — FIX URGENTE
**`_verify_article_neo4j()` en `case_schema_builder.py` ~línea 210**

```python
# CÓDIGO ACTUAL (ROTO con Neo4j v17):
MATCH (a:Articulo) WHERE ...

# FIX NECESARIO (Neo4j v17 usa :Precepto):
MATCH (p:Precepto) WHERE (p.numero CONTAINS $num OR p.titulo CONTAINS $num)
  AND p.ley_id CONTAINS $ley
RETURN p.texto AS texto LIMIT 1
```

**Impacto:** Sin este fix, `contexto_legal` está vacío → el LLM genera sin texto BOE real.

### ⚠️ Pendiente
- agent_8 plausibilidad distractores: 31% (heurística falla con valores numéricos concretos)
- agent_1 BOE/Qdrant: desactivado por timeout
- Plan V14.5: 59 trampas nuevas categorías R/S/T + blueprints Mar/Minería/RETA-cese

---

## 11. PRÓXIMOS PASOS PARA MONETIZACIÓN

1. **FIX URGENTE**: Corregir query Neo4j `:Articulo` → `:Precepto` en `case_schema_builder.py`
2. **Generar primer lote**: Ejecutar `test_e2e_v14_mistral.py` con Neo4j v17 operativo
3. **Evaluación calidad**: Verificar casos generados vs simulacros reales DM y Las Cortes (hija opositora)
4. **Ajuste prompts**: Si la calidad narrativa no es suficiente, afinar few-shot en `redactor_v14.yaml`
5. **Plan V14.5**: Añadir trampas R/S/T y blueprints Mar/Minería
6. **Pack comercial**: 10-20 casos verificados listos para venta

---

## 12. ARCHIVOS CLAVE DE REFERENCIA

| Archivo | Descripción |
|---------|-------------|
| `FLUJO_24_03.md` | Arquitectura V14 documentada |
| `PLAN_MAESTRO_CASOS_SIMULACROS.md` | Plan maestro (actualizar) |
| `PLAN_IMPLEMENTACION_V14_5_TRAMPAS.md` | Plan V14.5 pendiente |
| `docs/AUDITORIA_IMPLEMENTADO_VS_DISEÑO_17_03_26.md` | Auditoría brownfield |
| `09_04_26_NEO4J_MEMORIA.md` | Estado Neo4j v17 |
| `09_04_26_MEMORIA_SISTEMA_CASOS_PY.md` | **Este fichero** |
| `.windsurf/plans/diversidad-casos-v14-332554.md` | Plan diversidad + bugs detectados |
