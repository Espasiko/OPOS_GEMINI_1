# 🎯 ESTRATEGIA EXTRACCIÓN SABIDURÍA — OPOS-WIKI-SS · v1.2

> **Fecha**: 18/04/2026 · **Autor**: Spas + Cascade  
> **Reemplaza**: `17_04_26_ESTRATEGIA_EXTRACCION_SABIDURIA.md` (v1.0)  
> **Añade respecto a v1.0**: núcleo de 43 notas, evaluación `caso_febrerov2_DM_STYLE.md` (7 bugs), inventario 200+ archivos `/academias/`, decisiones tomadas 17-18 abr.

---

## 0. Resumen ejecutivo

**Qué**: bóveda Obsidian en `D:\BOVEDA_OPOS\BOVEDA_OPOS_SS\` con sabiduría SS C1 2026 (trampas + preceptos + fórmulas + patrones). Memoria viva editable por Cascade + lectura por cualquier IA.

**Quién la usa**: Spas + Cascade (desarrollo) · hija de Spas (beta) · **NO los usuarios finales** (ellos ven solo la web React — modelo A confirmado).

**Por qué**: unificar 50+ archivos dispersos (`catalogo_trampas.yaml`, docstrings calculadoras, `INVESTIGACION_MATERIALES_30_03`, `GROK_TRAMPAS`, `PLAN_MAESTRO`, etc.) en un grafo navegable con wikilinks. Anti-repetición.

---

## 1. NÚCLEO de 43 notas (el centro de la bóveda)

> **Regla**: el centro = conjunto mínimo que TODO lo demás referencia. Nunca se duplica, solo se enlaza.

### A. 8 fórmulas cruzadas (ADN de todo cálculo SS)

1. Base cotización (min/max/prorrata) — `calcular_base_cotizacion_completa`
2. Cuota total (CC + MEI + Des + FP + FOGASA) — `constantes_2026.py`
3. Solidaridad art. 19 bis (3 tramos 2026)
4. Recargo art. 30 (10/20/35%) — `calcular_recargo_apremio`
5. Pluriempleo (tope proporcional) — ⚠️ pendiente
6. Pluriactividad (devolución 50%) — `calcular_pluriactividad_reta_rgss`
7. BR prestaciones (IT / IP / Jubi / Viudedad)
8. Bonificaciones (pérdida proporcional) — ⚠️ pendiente

### B. 15 preceptos troncales

```
TRLGSS: arts. 15-17 · 19 + 19bis · 30 · 142 · 168 · 196 · 205 · 216 · 305
RD 84/1996:   arts. 10 · 22 · 33
RD 1415/2004: arts. 1-5 · 30
Orden PJC/297/2026 (tipos cotización 2026)
```

### C. 20 trampas radiadoras (cruzan ≥2 preceptos)

```
G4 · Solidaria SOLO principal+recargo (art. 15 bis)
H7 · RETA ventanas bimestrales
I12 · Contratos ≤8d = 32,60€ FIJO
I19 · Cuotas inaplazables 1 mes
     · Afiliación (única) vs Alta (por relación)
     · Solidaria vs subsidiaria
     · Días naturales vs hábiles
     · Retroactividad afiliación vs alta
     · Base mín Grupo 1 > salario real
     · Estructurales ≠ fuerza mayor
     · "Mero socio" (no alta)
     · "Familiar que no convive" (RGSS, no excluido)
     · "Empleados hogar vía empresa" (→ RGSS)
     · Pluriempleo vs pluriactividad
     · Recargo art. 30 vs interés demora
     · IPP en RETA por EC = NO protegida
     · Viudedad + orfandad = límite 100/118%
     · IT recaída 180d = competencia INSS
     · LPNI SOLO AT/EP
     · Jubilación demorada = 4% fijo (post-reforma)
```

### Por qué este núcleo

- Cubre 80%+ de preguntas en 3 simulacros DM + 59 trampas `INVESTIGACION` + 45 trampas `GROK`
- Cada trampa ya apunta a ≥2 preceptos + ≥1 fórmula
- 8 fórmulas YA existen en calculadoras (no se construyen)
- Incremental: añadir temario luego → núcleo ya está, solo enlaza
- Anti-repetición: trampas radiadoras = únicas que merecen `.md` propio al inicio

---

## 2. Fuentes REALES (ubicaciones verificadas)

### Primarias ya en repo

| Fuente | Ruta | Aporte núcleo |
|---|---|---|
| `catalogo_trampas*.yaml` | `backend/v14/` | 20 radiadoras base |
| 8 archivos calculadoras Python | `backend/calculators/` | 8 fórmulas cruzadas |
| `INVESTIGACION_MATERIALES_30_03_GEMINI_BMAD.MD` | Raíz | 59 trampas catalogadas |
| `29_03_GROK_TRAMPAS_CALCULADORAS_TEMAS.md_` | `academias/1_casos_recientes_2026_DM/criticas18__03_26/` | 45 trampas + fórmulas |
| `MAPA_MENTAL_CAMBIOS_LEGISLATIVOS_2026.excalidraw + .md` | Misma | 1 mapa a absorber |
| `PLAN_MAESTRO_CASOS_SIMULACROS.md v4` | `academias/1_casos_recientes_2026_DM/` | Distribución 2026 |
| Simulacros DM Dic/Ene/Mar | Idem | Patrones narrativos |
| Temario troceado v2026 | `academias/.../temario_troceado_v2026/` | 13 temas Capa 1 |
| Blueprints V14 (S02-S16) | `backend/v14/blueprints/` | Generador casos |
| Neo4j Docker | Activo | 103 leyes + 4.742 preceptos + 6.334 embeddings |

### Secundarias (lectura dirigida, sin copia)

- `academias/textos_anonimizados/` — **útiles**, contenido legal intacto con `[AUTOR]`/`[ACADEMIA]` tachado
- `academias/textos_limpios/` — ⚠️ rotos (cabeceras vacías). NO borrar todavía (decisión 18/04)
- `academias/Opos de Radi todo/` — PDFs originales (muestreo únicamente)
- **Convocatorias 2024 y anteriores** — ❌ NO usar para análisis (decisión 18/04)

### Academias identificadas

| Academia | Material | Nombres a evitar como personajes |
|---|---|---|
| **DM (David de Miguel)** | 3 simulacros analizados | María Ángeles, José Alberto |
| **Las Cortes** | Muchos anexos SS | Sara Domínguez, Carlos Hernández, Alfonso Hidalgo, Pablo Segado |
| **Valera** | Ninguno (solo web) | — |
| **GoKoan / OpoEsquemas** | PDFs limitados | — |

---

## 3. Pipeline 5 fases

```
FUENTE A: Neo4j (BOE)                  → wiki/preceptos/
FUENTE B: catalogo_trampas*.yaml       → wiki/trampas/
FUENTE C: calculadoras/*.py docstrings → wiki/calculos/ + wiki/trampas/
FUENTE D: INVESTIGACION + GROK         → wiki/trampas/ (fusión)
FUENTE E: temario_troceado_v2026/      → wiki/temas/
FUENTE F: MAPA_MENTAL_CAMBIOS_2026     → wiki/mapas/
          ↓
     Enriquecimiento (Cascade + usuario)
          ↓
  wiki/qa/ · wiki/lagunas/ · usuarios/{id}/
```

### Fase 0 ✅ HECHO
Neo4j activo, mcp-server OK, ~100 trampas YAML, 13 temas troceados, 8 archivos calculadoras.

### Fase 1A — Seed núcleo (Sesión 1A, ~30 min)
Script `backend/scripts/seed_obsidian_vault.py`:
1. Neo4j → 15 preceptos troncales → `wiki/preceptos/`
2. `catalogo_trampas*.yaml` → filtra 20 radiadoras → `wiki/trampas/`
3. AST-parse 8 archivos `calculators/*.py` → 8 fórmulas + docstrings TRAMPA → `wiki/calculos/`
4. Copia `MAPA_MENTAL_CAMBIOS_LEGISLATIVOS_2026` → `wiki/mapas/`
5. Crea `index.md`, `SKILLS.md`, carpetas vacías

**Output**: ~50 archivos (43 núcleo + mapa + índice + skills).

### Fase 1B — Temario + patrones (Sesión 1B, ~30 min)
Si 1A aprobada:
- 13 temas con frontmatter COSMIC (`peso_examen_min`, `peso_examen_max`, `articulos_clave`, `trampas_asociadas`)
- 9 patrones narrativos DM reformulados en estilo propio

**Output**: +22 notas → total ~72 notas.

### Fase 2 — Fusión trampas (Sesión 2, ~60 min)
Cruzar: `INVESTIGACION` (59) + `GROK` (45) + `catalogo_trampas*.yaml` (~100) → dedup + verificación Neo4j + reformulación → `wiki/trampas/` expandido a **120-150 trampas**.

### Fase 3 — Verificación BOE
Cron script por cada `wiki/preceptos/*.md`:
- Llama `mcp-server.verify_boe(ley, articulo)` → compara hash
- Si OK → `verificado_boe: FECHA`
- Si no → `[REVISAR]`

Limitación: BOE API avanza más allá 04/03/2026 → solo para 2ª opinión. **Neo4j = fuente autoritativa** (corte 04/03/2026). Si falta precepto → re-ingesta con `v17.py`, NO con API.

### Fase 4 — Multi-IA
- `SKILLS.md` con reglas generales (lee cualquier IA)
- Vault agnóstico: Cascade / Gemini / Mistral / DeepSeek / Grok / Llama4 leen `.md`
- **NO Claude Desktop** (confirmado)

### Fase 5 — Enriquecimiento continuo
Cada sesión añade:
- `wiki/qa/YYYY-MM-DD_HH-MM-tema.md`
- `wiki/lagunas/*.md` si detecta gap
- `usuarios/{id}/sesiones/*.md`
- Actualiza `usuarios/{id}/perfil.md` y `plan_adaptativo.md`

---

## 4. Decisiones tomadas (consolidado 17-18 abril)

| # | Decisión | Estado |
|---|---|---|
| 1 | Ruta vault | ✅ `D:\BOVEDA_OPOS\BOVEDA_OPOS_SS\` único, NTFS Windows |
| 2 | Acceso WSL | ✅ symlink `ln -s /mnt/d/BOVEDA_OPOS/BOVEDA_OPOS_SS /home/spas/OPOS_GEMINI_1/BOVEDA_OPOS_SS` |
| 3 | Obsidian abre | ✅ directo `D:\...` (NO `\\wsl.localhost\...`) |
| 4 | Usuarios iniciales | ✅ `spas` + beta hija |
| 5 | Centro bóveda | ✅ 43 notas núcleo |
| 6 | Teoría (CE, LPAC, TREBEP) | ✅ FUERA del núcleo (Capa 1) |
| 7 | Golden datasets | 🔒 Bloqueados hasta verificación individual |
| 8 | GitHub para skills | ❌ Todo privado local |
| 9 | Verificación | ✅ Cascade desde IDE, gratis |
| 10 | Claude Desktop | ❌ No necesario |
| 11 | Batch 50% API | 🟡 Solo generación masiva (500+ prompts) |
| 12 | Mapa mental cambios | ✅ Absorber existente tal cual |
| 13 | Pool nombres | ✅ Neutro + grep previo (protocolo §5) |
| 14 | YAML→MD | ✅ Script Python (0€, 0 prompts) |
| 15 | Plugin Syncthing Integration | ❌ No instalar (pide pagar) |
| 16 | `obsidian.md/cli` | ❌ No útil para nosotros |
| 17 | Modelo usuarios finales | ✅ Modelo A (web only) |
| 18 | `textos_limpios/` rotos | ⏸️ NO borrar todavía |
| 19 | Convocatorias 2024 y ant. | ❌ No analizar |
| 20 | Syncthing | ⏸️ Usuario instalará (SyncTrayzor recomendado) |

---

## 5. Protocolo de nombres (evitar fuga academias)

### Pool neutro

```
Nombres: Juan, Ana, Pedro, Laura, Antonio, Carmen, Manuel, Beatriz,
         Javier, Teresa, Francisco, Pilar, Miguel, Elena, Rafael, Rosa
Apellidos: García, Martínez, López, Fernández, Ruiz, Moreno, Jiménez,
           Álvarez, Romero, Navarro (top 10 INE)
```

### Prohibidos (preparadores reales)
- DM: María Ángeles, José Alberto, Sergio+Alba (cooperativa), Carmelo (hijo conviviente), Javier (marido sin actividad), Jacinto (hijo discapacitado), Silvia Pastor
- Las Cortes: Sara Domínguez, Carlos Hernández, Alfonso Hidalgo, Pablo Segado

### Regla previa a uso
```bash
grep -r "Nombre Apellido" /academias/ → si match, descartar combinación
```

### Audit `nombres_pool.py`
Sesión 3 revisa `/backend/v14/nombres_pool.py` y elimina cualquier nombre copiado de academias.

---

## 6. Evaluación `caso_febrerov2_DM_STYLE.md` (generado V14.5 + Claude)

**Puntuación: 34/60 (57%)** — **no apto para publicar sin fix**.

### 7 bugs detectados

| # | Severidad | Bug |
|---|---|---|
| P3 | 🔴 GRAVE | Contradice trampa G4 (solidaria = SOLO principal+recargo). Marca D (incluye intereses y costas), correcta sería B |
| P7 | 🔴 GRAVE | Escala OM 31/01/1970 IPT: 58 años = **36 mensualidades**, no 24. Marca C (24), correcta B (36) |
| P11 | 🟠 ALTA | IT menstruación (LO 1/2023) = pago **DIRECTO**, NO pago delegado. Respuesta B lo pone como pago delegado |
| P17 | 🟠 ALTA | Jubilación activa 50% sin reflejar reforma **RDL 11/2024** (escalado 45/55/65/80/100%) |
| P5 | 🟡 MEDIA | Confunde "prórroga especial" con "prórroga ordinaria" (terminológico) |
| P13 | 🟡 MEDIA | Cita Art. 218.2 TRLGSS → debería ser Art. 219.2 |
| P16 | 🟡 MEDIA | 31/10/2026 fue sábado → no es último día hábil. Ninguna opción recoge 30/10 (viernes) |

### Lo que revela

El motor V14.5 tiene **gaps reales**:
- No conecta trampas YAML con texto final
- No incorpora reformas 2024 (RDL 11/2024)
- No valida fechas hábiles en calendario 2026
- No verifica citas de artículo exactas

### Acción propuesta

Convertir los 7 bugs en **tests unitarios** del Builder V14.5 → mejora del motor a largo plazo (opción 2 recomendada al usuario).

---

## 7. Arquitectura integración (la wiki NO duplica, extiende)

| Componente existente | Rol con la wiki |
|---|---|
| Frontend React (17 vistas) | Sigue igual para usuarios finales. Generadores opcionalmente leen wiki |
| Backend FastAPI (9 routers) | Sigue igual. Nuevo `/wiki/search` opcional |
| 8 calculadoras Python (105 fn) | Fuente de 8 fórmulas núcleo. Docstrings → `wiki/calculos/` |
| mcp-server (6 tools) | Skills llaman a sus endpoints |
| Neo4j | Fuente autoritativa de preceptos |
| V14.5 blueprints | Leen `wiki/patrones_dm/` para casos sofisticados |
| Agentes YAML | Sin cambios |
| PostgreSQL | Vive en paralelo. Wiki = complemento pedagógico |

---

## 8. Anti-alucinación (BOE first)

> **Regla de oro**: ninguna afirmación entra en `wiki/preceptos/` sin verificación contra BOE.

### Frontmatter obligatorio

```yaml
---
ley: TRLGSS
articulo: 196
version_boe: 2026-03-04
verificado_boe: 2026-04-18
hash_texto: abc123def456
modificaciones_pendientes:
  - RDL 11/2024 (jubilación activa)
tags: [IP, porcentajes, trampa_E]
---
```

### Proceso
1. Antes de crear: `mcp-server.verify_boe(ley, articulo)`
2. Cron script revalida todo mensualmente
3. Si cambia → `[DESACTUALIZADO-desde-FECHA]` + notifica
4. Si usuario Q&A sobre precepto desactualizado → IA avisa explícitamente

---

## 9. IA pequeña en CPU (funciona)

Flujo para Ollama + Llama 3.2 3B / Qwen 2.5 1.5B / Mistral Small 3:

```
Pregunta usuario
  ↓
grep en wiki/ por palabras clave
  ↓
Top 5 notas (límite ~3000 tokens)
  ↓
Prompt: "Responde usando SOLO estas notas"
  ↓
Modelo CPU → respuesta con wikilinks
  ↓
(opcional) skill opos-verify valida citas vs Neo4j
```

- Sin embeddings (grep basta si nombres archivo descriptivos)
- Temperatura 0.0 + prompt estricto → alucinación mínima
- Para casos complejos / simulacros → Sonnet/DeepSeek/Mistral Large

---

## 10. Multi-usuario y escalabilidad

### Fase 1 (1-10 usuarios)
Vault local único en `usuarios/{id}/`.

### Fase 2 (10-100 usuarios)
```
/BOVEDA_OPOS_SS_PUBLICO/wiki/   ← compartido read-only (CDN)
/BOVEDA_USUARIOS/{uuid}/         ← privado por usuario
```

### Fase 3 (100+ usuarios)
Backend con PostgreSQL. Usuarios exportables a `.md`.

### Compactación automática
- `sesiones/` >60 días → colapsan en `historial_{año}_Q{trim}.md`
- Lagunas con tasa_acierto>90% 3 veces → archivadas
- Q&A duplicadas (hash idéntico) no se guardan

### Tamaños reales (.md puros, ridículos)
| Usuarios | Notas/año | Total anual |
|---|---|---|
| 10 | ~500/u | 50 MB |
| 100 | ~500/u | 500 MB |
| 1.000 | ~500/u | 5 GB |

---

## 11. QUÉ NO HACEMOS

- ❌ Nuevo frontend (actual vale)
- ❌ Migrar localStorage → PostgreSQL ahora
- ❌ Añadir Stripe / Clerk ahora
- ❌ Reescribir calculadoras
- ❌ Tocar V14.5 ni agentes
- ❌ Publicar material DM/Valera/Las Cortes en vault
- ❌ Instalar Qdrant adicional (Neo4j + embeddings bastan)
- ❌ Mini-foro ahora
- ❌ Analizar convocatorias 2024 y anteriores
- ❌ Usar Claude Desktop
- ❌ Subir skills a GitHub

---

## 12. Riesgos y mitigación

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| Wiki crece inmanejable | Media | Dataview + índices auto |
| Discrepancia Neo4j vs wiki | Alta | Cron diario revalida |
| IA aluciona al reformular | Media | Prompt estricto + validator |
| Syncthing conflictos | Baja | Archivos pequeños + backup diario |
| Obsidian cambia API | Baja | Skills son `.md` puros |
| Motor V14.5 genera casos con bugs | **Alta** | Tests + validator legal previo a publicar |
| Nombres se cuelan de academias | Media | Protocolo §5 + grep previo |

---

## 13. Entregables esperados

Tras Sesiones 1A + 1B + 2:
1. **Vault funcional** en `D:\BOVEDA_OPOS\BOVEDA_OPOS_SS\` con 150+ notas
2. **3 skills** en `/skills/` operativas (opos-query, opos-ingest, opos-session)
3. **Script seed** reutilizable en `backend/scripts/seed_obsidian_vault.py`
4. **Syncthing** replicando a móvil (cuando instales)
5. **Docs actualizados** (`prd.md`, `product-brief.md`)
6. **Plan mantenimiento** (scripts cron por frecuencia)
7. **7 bugs V14.5 documentados** como tests

---

## 14. Próximo paso

### Bloqueado hasta que instales Syncthing:
- **Sesión 1A** (setup D:\ + symlink + seed 43 notas)

### Mientras tanto, posibles:
- Fusionar `INVESTIGACION_MATERIALES_30_03` + `GROK_TRAMPAS` + `catalogo_trampas*.yaml` → producir `trampas_unificadas.yaml` (Fase 2 preparada)
- Documentar los 7 bugs V14.5 como tests unitarios
- Auditar `nombres_pool.py` y purgar nombres academias

👉 **Tú**: instalas Syncthing (SyncTrayzor recomendado) + me avisas.  
👉 **Cascade**: ejecuta Sesión 1A en cuanto avises.
ACTUALIZADO /home/spas/OPOS_GEMINI_1/CASOS_TRAMPAS_DM_2026.md EN 18/04/2026 POR CLAUDE 4.7 MAX
---

*v1.2 · 18/04/2026 · Cascade*
