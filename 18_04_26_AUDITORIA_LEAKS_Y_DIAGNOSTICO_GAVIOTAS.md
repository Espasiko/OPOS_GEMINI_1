# 🔍 Auditoría completa 18/04/2026 — leaks + diagnóstico GAVIOTAS

> **Objetivo**: inventariar todos los leaks de nombres de academias/preparadores, diagnosticar por qué el caso GAVIOTAS no salió bien con V14.5, y proponer plan de acción con aprobación del usuario.

---

## 1. 🚨 Mapa de LEAKS en el proyecto

### 1.1 ZONA CRÍTICA (se propaga al producto final / wiki)

| Ubicación | Tipo de leak | Líneas / archivos | Impacto |
|---|---|---|---|
| `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml` | Contenido: tags origen + textos reglas | 20 líneas: `DM`, `El preparador DM`, `DM temario`, `Simulacro Enero DM`, `metodologia_DM`, `[DM-SIMULACRO]`, `[INVENTADA-DM]`, `[DM-TEMARIO]` | 🔴 MÁXIMO — se replica al vault |
| `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/trampas/` | Contenido propagado del YAML | 8 notas + 2 índices (CA3, D2, H7, I8, I16, I17, I18, `_INDICE.md`, `_PENDIENTES_VERIFICAR.md`) | 🔴 MÁXIMO — vault expuesto |
| YAML maestro + vault (A8) | **Nombre de empresa "LANDSCAPE MR SL" + persona "Manuel"** | Caso A8 en vault Obsidian — línea literal | 🔴 MÁXIMO — posible empresa real |

### 1.2 ZONA ALTA (documentación propia del proyecto)

Archivos con `DM` o similar **en el nombre** (nuestros, no materiales fuente):

```
./16_04_26_VERIFICACION_VALERA_MD_IDEAS.md
./ANALISIS_RESULTADOS_FEBRERO_GEMINI_VS_DM.md
./ANALISIS_SOFISTICACION_DM_VS_V14.md
./CASOS_TRAMPAS_DM_2026.md
./caso_23_DM_STYLE.md
./caso_febrerov2_DM_STYLE.md
./analisis_comparativo_casos_DM.md
./preguntas_para_tests_simulacros_de_DM.md
./backend/v14/cambios_dm_2026.py                 ← código
./academias/CRITICAS_PLANES/CLAUDE_VALERA+MD_16_03_PLAN.md
./academias/1_casos_recientes_2026_DM/*          ← carpeta entera (15+ archivos)
```

Archivos con `Valera` **en contenido** (nuestros): 28 archivos de docs/planes.

Archivos con `Sara Domínguez` / `SaraDominguez` **en contenido**: 10 archivos nuestros.

### 1.3 ZONA BAJA (materiales fuente — quedan locales, no se publican)

Estos sí pueden tener nombres porque son **material de estudio privado del usuario**, no salen al vault ni al producto:

```
./academias/Opos de Radi todo/.../SEGURIDAD SOCIAL LAS CORTES/...
./academias/textos_limpios/Anexo*-SaraDomínguez*.txt
./academias/textos_anonimizados/*.txt
./academias/temario_oficial/...
./gastos_ tokens/...   (logs del usuario)
```

**Política sugerida**: NO tocar estas carpetas. Solo limpiar lo que se propaga al producto.

### 1.4 ZONA NEUTRA (falsos positivos — ignorar)

- `.agents/skills/bmad-domain-research/domain-steps/step-03-competitive-landscape.md` → "LANDSCAPE" en sentido de "panorama competitivo", no la empresa
- `llama.cpp/.../dropdown-menu-radio-item.svelte` → matches de `-dm-` por "dropdown-menu"

---

## 2. 🧩 Plan de limpieza propuesto (pendiente de tu aprobación)

### Opción A — Limpieza mínima (solo lo que llega al vault)

Acciones:
1. Sustituir en `trampas_unificadas_v2_CURADO.yaml`:
   - `DM` → `PRIV` (tags de origen)
   - `[INVENTADA-DM]` → `[PEDAGOGICA-INTERNA]`
   - `[DM-SIMULACRO]` → `[SIMULACRO-PRIVADO]`
   - `[BOE-DIRECTO + DM-TEMARIO]` → `[BOE-DIRECTO + TEMARIO-PRIVADO]`
   - `El preparador DM` → `El preparador privado`
   - `DM temario` / `DM 2026` → `temario externo` / `nomenclatura 2026`
   - `metodologia_DM` → `metodologia_simulacros_privados`
   - `Simulacro Enero DM` → `Simulacro Enero (ed. privada)`
   - `Landscape MR SL` / `LANDSCAPE MR SL` → `EMPRESA EJEMPLO S.L.` (propuesta)
   - `Manuel` / `Soraya` / `Miguel` / `Angélica` → `Socio A / Socia B / ...`
2. Regenerar vault con `trampas_yaml_to_obsidian.py` (ya existe)
3. Dejar docs internos (`CASOS_TRAMPAS_DM_2026.md`, etc.) tal cual — son notas de trabajo locales

**Tiempo estimado**: 10 min | **Riesgo**: bajo

### Opción B — Limpieza profunda (renombrar archivos propios)

Además de A:
- Renombrar `caso_febrerov2_DM_STYLE.md` → `caso_febrerov2_estilo_simulacro.md`
- Renombrar `caso_23_DM_STYLE.md` → `caso_23_estilo_simulacro.md`
- Renombrar `CASOS_TRAMPAS_DM_2026.md` → `CASOS_TRAMPAS_2026.md`
- Renombrar `backend/v14/cambios_dm_2026.py` → `backend/v14/cambios_2026_simulacros.py` (ojo imports)
- **NO** renombrar todavía la carpeta `academias/1_casos_recientes_2026_DM/` (demasiados paths dependen de ella)

**Tiempo estimado**: 30 min | **Riesgo**: medio (hay que actualizar imports)

### Opción C — Limpieza total

Además de A+B:
- Renombrar carpeta `academias/1_casos_recientes_2026_DM/` → `academias/1_casos_recientes_2026_privados/`
- Actualizar todos los scripts que apuntan a esa ruta

**Tiempo estimado**: 1-2 h | **Riesgo**: alto (muchos scripts afectados)

---

## 3. 🔬 Comparación GAVIOTAS (nuestro) vs HORIZONTE SOLIDARIO (caso real DM)

### 3.1 Tabla comparativa

| Aspecto | GAVIOTAS (V14.5 → Claude → yo) | HORIZONTE SOLIDARIO (real, BOE) |
|---|---|---|
| Empresa | GAVIOTAS DEL SUR | Horizonte Solidario |
| Socio | Leandro | Jorge |
| P2 tipo responsabilidad | Solidaria ✅ | Solidaria ✅ |
| P2 cita | Art. 335 + DA 4ª TRLGSS + Art. 72 LCoop | Art. 15.3 LGSS + Ley Coop |
| **P3 alcance** | **B: principal + recargo** | **D: principal + recargo + intereses + costas** |
| P3 cita | Art. 15.3 TRLGSS | **Art. 104 LGSS (Derivación)** |
| P1 (plazo estatutos) | B: 5 años (Art. 24.2) ✅ | D: 5 años (Art. 14 TRLGSS) ✅ |

### 3.2 🚨 DISCREPANCIA en P3 — ¿quién tiene razón?

**Posición DM (preparador)**: responsabilidad solidaria cubre **TODO** (principal + recargos + intereses + costas), cita `Art. 104 LGSS`.

**Mi corrección previa (18/04)**: solidaria solo cubre principal + recargo; intereses/costas solo en subsidiaria. Cita `Art. 15.3 TRLGSS`.

**Análisis normativo**:

- En el **TRLGSS vigente (RDLeg 8/2015)**, el **Art. 104** regula la **"incapacidad permanente parcial"**, NO derivación de deuda. Eso es un error de cita del preparador DM (o referencia a la antigua LGSS-1994 donde sí había un precepto de derivación).
- El **Art. 15 TRLGSS** regula responsables solidarios y subsidiarios. En doctrina hay dos posturas:
  - Estricta: solidaria = principal + recargo (como yo corregí)
  - Amplia: solidaria = todo el débito (como dice DM)
- La jurisprudencia del TS en recaudación SS **tiende a la postura amplia**: si el título ejecutivo incluye recargos/intereses, el responsable solidario responde por el total (SSTS Sala Contencioso, múltiples 2018-2022).

**Conclusión**: la respuesta DM (D = todo) es **más prudente** pedagógicamente porque es la que el preparador marca. Mi corrección a B era técnicamente defendible pero rompe el estilo DM. **Recomiendo revertir P3 a D**, actualizando la cita a `Art. 18.1 TRLGSS + Art. 15 TRLGSS` (no Art. 104).

### 3.3 🧪 Diagnóstico V14.5 — ¿por qué falló GAVIOTAS?

Causas identificadas en cadena:

1. **Blueprint sin ground truth**: El generador no tenía el caso real (Horizonte) como patrón para imitar. Inventó preguntas "estilo DM" sin anclaje concreto.
2. **Mistral alucinó Art. 104**: el modelo confundió TRLGSS-2015 con LGSS-1994 y puso "Art. 104 TRLGSS" por "derivación". El agente verificador no detectó el error porque no consulta BOE en tiempo real.
3. **Claude intentó corregir sin contexto DM**: al ver "Art. 104 = IP parcial" en BOE, asumió que toda la pregunta estaba mal y reescribió sin conocer la postura DM.
4. **Yo añadí una 3ª interpretación** (solidaria = solo principal + recargo), rompiendo coherencia con el estilo del preparador original.
5. **Ausencia de verificación cruzada con casos DM anteriores**: no hay un "corpus DM" cargado en RAG para que el agente tenga el estilo del preparador como referencia.
6. **Reutilización literal de nombres**: `LANDSCAPE MR SL`, `Manuel`, etc. vienen del simulacro diciembre y se copiaron sin anonimizar.
7. **Sin auditor de leaks**: ningún agente comprueba que los nombres propios no coincidan con empresas reales ni que no aparezcan nombres de academias en el output.

### 3.4 🎯 Dónde falla V14.5 exactamente

| Agente V14.5 | ¿Qué falla? | Propuesta de fix |
|---|---|---|
| **Blueprint-generator** | No consulta simulacros DM previos como ground-truth | Cargar los 5 últimos simulacros DM en contexto |
| **Narrador** | Reutiliza personajes/empresas del caso diciembre | Generador aleatorio de nombres ficticios + validador anti-coincidencia |
| **Trampas-injector** | Inyecta trampas sin verificar que el artículo citado realmente regula lo que dice | Cruzar con YAML `trampas_unificadas_v2_CURADO.yaml` (catálogo verificado) |
| **Verificador** | No consulta BOE en tiempo real ni el catálogo de trampas | Añadir MCP `boe` obligatorio + grep en YAML de trampas |
| **Auditor de leaks (NO EXISTE)** | — | Añadir paso final que grep-ee los nombres sensibles en el output |
| **Consistencia P2↔P3** | No detecta contradicciones internas (solidaria/subsidiaria) | Check explícito: si P2=solidaria, P3 debe ser coherente con doctrina solidaria |

---

## 4. 🔧 AGE Administrativo — ¿tiene casos prácticos?

**Pendiente de verificar** con búsqueda web. Hipótesis del usuario: sí, con enfoque distinto a SS (parte 1 común teórica; parte 2 específica con casos). Si se confirma, las trampas con tag `categoria_Q_funcion_publica_AGE` deberían marcarse explícitamente como `aplica_AGE: true` en el frontmatter.

---

## 5. 🔄 Edición bidireccional Obsidian ↔ YAML — ¿viable?

### 5.1 Respuesta corta

Sí, pero con cuidado. Hay tres modelos posibles:

### 5.2 Modelo A — **YAML como única fuente de verdad** (actual, recomendado)

```
YAML maestro → script → vault Obsidian
```

- Flujo: editas YAML, ejecutas `trampas_yaml_to_obsidian.py`, se regenera todo.
- **Ventaja**: un solo sitio, sin conflictos, fácil diff git.
- **Desventaja**: no puedes editar en Obsidian sin perder cambios al regenerar.

### 5.3 Modelo B — **Obsidian como fuente de verdad**

```
vault Obsidian → script → YAML (derivado)
```

- Flujo: editas notas en Obsidian, ejecutas `obsidian_to_yaml.py` (por escribir), se actualiza el YAML.
- **Ventaja**: UX muy cómoda (editor Obsidian, plugins, backlinks).
- **Desventaja**: requiere un parser robusto MD→YAML; frágil si rompes frontmatter.

### 5.4 Modelo C — **Bidireccional con metadato de "última edición"** ⭐

```
YAML maestro ⇄ vault Obsidian (con timestamp de última edición)
```

- Cada nota tiene `last_edited: 2026-04-18T19:30` en frontmatter.
- Script "merge" compara timestamps: la fuente más reciente gana.
- **Ventaja**: puedes editar en cualquiera.
- **Desventaja**: complejidad; posibles conflictos.

### 5.5 Recomendación

**Hoy**: Modelo A (YAML fuente única). Edita en Obsidian para **lectura y navegación**, no para cambios.

**Mañana (v2 del flujo)**: Modelo C con script `sync_yaml_vault.py` + campo `last_edited`. Lo escribo cuando decidas.

**A mano puedes editar el YAML directamente** (es legible) o los `.md` del vault si aceptas perder los cambios al regenerar — te vendría bien un plugin Obsidian de "git push on save" para respaldar.

---

## 6. ❓ Preguntas clave para ti (necesito respuesta antes de seguir)

1. **¿Qué nivel de limpieza quieres?** → Opción A / B / C
2. **¿Revierto P3 de GAVIOTAS a D (estilo DM, todo el débito)?** → Sí / No / Dejar ambas opciones documentadas
3. **¿Cómo anonimizar "LANDSCAPE MR SL"?** → Sugerencias: `VERDE JARDÍN S.L.` / `PAISAJES DEL SUR S.L.` / `EMPRESA EJEMPLO S.L.`
4. **¿Renombrar personajes del caso A8?** → Manuel, Soraya, Miguel, Angélica → Socio A/B/C/D o nombres frescos
5. **¿Renombrar archivos propios con `_DM_` en el nombre?** → Sí / No / Solo los públicos
6. **¿Cuándo hacemos la verificación exhaustiva de las 31 `[WEB]/[GROK]/...`?** → Hoy / otro día

---

## 7. 📋 Plan de acción sugerido (una vez apruebes)

1. ⏱️ 15 min — Aplicar limpieza Opción A (YAML + regenerar vault)
2. ⏱️ 5 min — Revertir P3 GAVIOTAS a coherencia con caso real DM
3. ⏱️ 10 min — Anonimizar LANDSCAPE MR SL + personajes (YAML + vault)
4. ⏱️ 5 min — Actualizar grafo MCP memory con el trabajo de hoy
5. ⏱️ 30-45 min — Clasificar "sin clasificar" + añadir marca AGE si procede
6. ⏱️ 1-2 h — Auditoría exhaustiva de las 31 trampas `[WEB]/[GROK]/etc.`
7. ⏱️ Más tarde — Opción B de renombrados (si quieres)

---

*Informe generado 18/04/2026 19:30. Siguiente paso: esperar respuestas a §6 para iniciar acciones.*

---

## ADDENDUM v2 — 20:00 — verdad normativa sobre P3 (verificado en Neo4j + fuentes internas)

### Correcciones a mi análisis del §3.2

**Yo había escrito**: "la respuesta DM (D = todo) es más prudente pedagógicamente". **MAL**. Revisando las fuentes internas del propio proyecto encuentro tres apoyos coherentes de que la respuesta correcta es **A (principal + recargo)** y D es la **TRAMPA que DM pone para que caigas**:

1. `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/conversacion_claude_full_resumen_10_03_26.md:2059` → *"solidaria por derivación → afecta a **principal + recargo únicamente**; nunca a intereses ni costas"*
2. `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/PLAN_MAESTRO_CASOS_SIMULACROS.md:898` → *"R23: Responsabilidad solidaria: **principal + recargo SOLO** (trampa: incluir intereses)"*
3. Docstring de `@/home/spas/OPOS_GEMINI_1/backend/calculators/calculos_ss_extended.py` → *"TRAMPA G4: Solidaria = SOLO principal + recargo. NUNCA intereses ni costas."*

El caso `caso_febrerov2_DM_STYLE.md` (generado por IA imitando estilo DM) **cayó en la trampa D** → porque la IA no consultó las fuentes internas del proyecto. Esto es el fallo nº 1 del pipeline V14.5: **el narrador/verificador no cruza con el catálogo de trampas propio**.

### La cita legal correcta (no es Art. 15 bis)

Verifiqué directamente en Neo4j (6246 preceptos ingresados del TRLGSS BOE-A-2015-11724):

- **Art. 15 bis TRLGSS NO EXISTE en el vigente** (Art. 15 salta a Art. 16). La cita "Art. 15 bis TRLGSS" que aparece en docstrings del proyecto es **herencia obsoleta de la LGSS-1994** y debería corregirse en todo el proyecto.

- **Art. 18.3 TRLGSS** (vigente) dice textualmente:
  > *"Son responsables del cumplimiento de la obligación de cotizar [...] los que resulten **responsables solidarios, subsidiarios o sucesores mortis causa** [...]. Dicha responsabilidad [...] se declarará y exigirá mediante el **procedimiento recaudatorio** establecido en esta ley."*

- **Art. 142 TRLGSS** ("Sujeto responsable") remite al Art. 18 y al Art. 168.1 y 2.

- **Art. 168.2 TRLGSS** regula sucesión empresa solidaria.

- El **alcance concreto** (principal + recargo) viene del **RD 1415/2004 (Reglamento General de Recaudación SS)** y la jurisprudencia TS.

**Cita correcta para P3 de un caso estilo DM**: `Art. 18.3 + Art. 142 TRLGSS + Art. 13 RGRSS (RD 1415/2004)`. No `Art. 15 bis`, no `Art. 104` (que en el TRLGSS vigente regula IP parcial), ni `Art. 15.3` (que no trata la derivación).

### Consecuencias operativas

1. **Mi corrección previa de P3 GAVIOTAS fue ACERTADA en fondo** (B = principal + recargo), pero la cita `Art. 15.3 TRLGSS` hay que cambiarla por `Art. 18.3 + 142 TRLGSS`.
2. **El caso `caso_febrerov2_DM_STYLE.md` tiene origen IA** (no lo generó DM) → es un artefacto del pipeline V14.5 que cayó en la trampa; el simulacro original de DM está en `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/caso-simulacro_febrero_DM.md` (enunciado limpio, sin respuestas porque éstas están en PDF ilegible por OCR).
3. **Hay que corregir `Art. 15 bis` → `Art. 18.3 + 142 TRLGSS` en todo el proyecto**:
   - `backend/calculators/calculos_ss_extended.py` (docstring G4)
   - `trampas_unificadas_v2_CURADO.yaml` (si aparece)
   - documentos internos

### Siguiente paso aprobado: Opción C + arreglo P3 + anonimización

Plan de ejecución inmediato (confirmado por el usuario):

1. Reescribir P3 de `caso_febrerov2_DM_STYLE.md` con cita correcta (Art. 18.3 + 142 TRLGSS) y alcance A (principal + recargo)
2. Renombrar `Art. 15 bis` → `Art. 18.3 + 142 TRLGSS` en todo el proyecto (grep + edit)
3. Limpieza YAML + regenerar vault (Opción A)
4. Renombrar archivos propios con `_DM_` (Opción B)
5. Renombrar carpeta `academias/1_casos_recientes_2026_DM/` (Opción C) + actualizar imports
6. Anonimizar `LANDSCAPE MR SL` y personajes de casos A8/otros
