# 🏛️ PLAN WIKI NEXO — v5.2 AJUSTADO

> **Fecha**: 20/04/2026 (17:50) · **Base**: patrón LLM-Wiki Karpathy + WikiForge + Método NEXO propio  
> **Estado**: aprobado, **pendiente de ejecución** del preproceso (limpiar YAML) + regeneración vault.  
> **Principio rector**: *"Dos preparadores veteranos que leen materiales de la competencia en privado, pero todo lo que publican es suyo: verificado contra BOE, con su nomenclatura, su orden, su estilo. No se obsesionan con nombres comunes españoles — solo evitan conjuntos reconocibles (nombre+empresa+caso específico)."*

---

## ✅ CORRECCIONES INCORPORADAS (v5 → v5.1 → v5.2)

### Cambios v5 → v5.1
| v5 (error mío) | v5.1 corregido |
|----------------|----------------|
| Renombrar carpeta a `senales-trampa/` | **Se queda `trampas/`** (genérico, no copyrightable) |
| Reescribir 184 trampas desde cero | **NO se reescriben**. Reglas, títulos, artículos, mnemónicos, `trampa_tipica` → se quedan |
| "Carnicería Apocalipto" fuera | **Se queda** (invención del usuario, pool memorable) |
| `fuentes/` con simulacros DM | **Solo BOE + simulacros V14.5 + apuntes spas** |
| Verificación BOE = último paso del wiki | **Ya no es paso del wiki**. Se hace durante extracción de trampas y en Neo4j |
| Arranque sin casos | **Caso semilla**: Gaviotas del Sur reparado |

### Cambios v5.1 → v5.2 (tras consulta usuario 20/04 17:40)
| v5.1 (demasiado rígido) | v5.2 realista |
|-------------------------|---------------|
| Lista negra con nombres comunes: Manuel, Andrea, Jorge, Amaia, Francisca, Miguel, Soraya, Roberta, Angélica | **Solo se prohíben CONJUNTOS reconocibles** (nombre+empresa+caso específico trazable al simulacro original). Nombres propios españoles sueltos son verosímiles → OK |
| Crear `seed_vault_v5_nexo.py` nuevo | **Usar `regenerar_vault_trampas.py` existente** (ya probado, generó 249 archivos el 19/04) |
| Muro de Abstracción aplicado a cada escritura del vault | **Muro aplica SOLO al ingestar material externo nuevo** (academias, nuevos PDFs). La operación diaria del vault ya limpio no lo necesita |
| "Análisis lotes 1-7 ya hecho" (confusión mía) | **Realidad**: los lotes 1-5 son VERIFICACIÓN BOE de las 184 trampas (ya hecha, YAML curado). Los 200+ materiales de academias (Las Cortes 792p, Carlos Hernández 3 temas, Sara Domínguez 5 archivos, Víctor Cabeza, simulacros 2024) **SIGUEN PENDIENTES** de procesamiento |
| Preproceso nombres dentro del script principal | **Preproceso aparte**: `limpiar_nombres_yaml.py` genera YAML limpio antes de regenerar |

---

## 🎯 ESTADO REAL DEL PROYECTO (actualizado 20/04/2026)

### Ya hecho ✅

| Entregable | Estado | Evidencia |
|------------|--------|-----------|
| 184 trampas verificadas BOE | ✅ YAML curado por Claude 4.7 en lotes 1-5 (→ 100% según usuario) | `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml` |
| Script regeneración vault | ✅ probado, generó 249 archivos | `@/home/spas/OPOS_GEMINI_1/scripts/maintenance/regenerar_vault_trampas.py` |
| Vault con trampas | ✅ 249 archivos en `wiki/trampas/` | `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/trampas/` |
| Caso ejemplo Gaviotas | ✅ reparado, listo | `@/home/spas/OPOS_GEMINI_1/CASO_EJEMPLO_1.md` (antes `caso_febrerov2_DM_STYLE.md`) |
| Pool nombres propio | ✅ 70+ nombres + 34 empresas memorables | `@/home/spas/OPOS_GEMINI_1/backend/v14/nombres_pool.py` |
| 17 esquemas mentales extraídos | ✅ | `.../esquemas_DM_fotos/extraidos_md/` |
| Neo4j BOE consolidado | ✅ 103 leyes + 4742 preceptos + embeddings | - |
| 60+ calculadoras Python | ✅ | `@/home/spas/OPOS_GEMINI_1/backend/calculators/` |

### PENDIENTES reales (no exagerar el "ya hecho")

| Pendiente | Fuente | Volumen |
|-----------|--------|---------|
| Limpieza nombres/empresas reconocibles en YAML | YAML curado | ~10-20 ocurrencias estimadas |
| Regenerar vault limpio tras limpieza | YAML limpio → 249+ archivos | 1 script run |
| Ingesta preceptos Neo4j → `wiki/preceptos/` | Neo4j | ~200 artículos clave |
| Ingesta docstrings calculadoras → `wiki/calculos/` | `.py` en `backend/calculators/` | 60+ |
| Procesar 200+ materiales de academias | `academias/` (lista en `28_03_26_lista_material_academias_radi.md`) | 1410+6300+6100 págs etc |
| Generar nuevos simulacros propios V14.5 | `backend/v14/` | N según tiempo |
| Crystallize QAs | Sesiones futuras | continuo |

> ⚠️ **El siguiente trabajo grande real** tras regenerar el vault es **procesar los 200+ materiales** de Radi/Las Cortes/Sara Domínguez/Carlos Hernández/Víctor Cabeza. Eso ampliará temario, patrones, casos propios.

---

## 🧱 ARQUITECTURA FÍSICA DEFINITIVA

```
/home/spas/OPOS_GEMINI_1/                        ← proyecto root
│
│ ═════════════════════════ ZONA 1: PRIVADO, FUERA DEL VAULT ═════════════════════════
│ (nunca se sincroniza con Syncthing, nunca sale al exterior)
│
├── academias/                                   ← materiales de terceros (intacto, solo lectura)
│   ├── 1_casos_recientes_2026_DM/
│   ├── Opos de Radi todo/
│   └── ...                                      ← ya está en .gitignore del root
│
├── raw_privado/                                 ← 🆕 trabajo de extracción (nuevo directorio)
│   ├── simulacros_DM_analizados/                ← nuestro análisis de sus simulacros
│   ├── patrones_narrativos_9/                   ← los 9 patrones abstractos
│   └── notas_trabajo/
│
├── meta_auditoria/                              ← 🆕 auditoría privada (gitignored)
│   ├── mapa-calor-academias.md                  ← "DM pregunta IT recaída 3/3 veces"
│   ├── nombres-evitar.md                        ← blacklist PII
│   ├── muro-abstraccion.md                      ← regla explícita
│   └── verificaciones-boe.md                    ← log de qué se verificó y cuándo
│
│ ═════════════════════════ MURO DE ABSTRACCIÓN ═════════════════════════
│
│ ═════════════════════════ ZONA 2: VAULT OBSIDIAN PÚBLICO ═════════════════════════
│ (sí se sincroniza con Syncthing, sí puede leerlo cualquier IA externa)
│
└── /mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/              ← ubicación del vault (Windows via Syncthing)
    │
    ├── CLAUDE.md                                ← schema: reglas para IAs que editen el vault
    ├── README.md
    │
    ├── index.md                                 ← catálogo maestro (Dataview queries)
    ├── log.md                                   ← cronológico append-only
    │
    ├── fuentes/                                 ← 🔑 SOLO fuentes propias o públicas
    │   ├── boe-trlgss-2015.md                   ← texto literal (Art. 13 LPI, dominio público)
    │   ├── boe-trebep.md
    │   ├── boe-rd-84-1996.md
    │   ├── jurisprudencia-ts.md
    │   ├── simulacro-propio-v14-001.md          ← generados por V14.5 (nuestros)
    │   └── apuntes-spas.md                      ← apuntes personales del usuario
    │
    ├── preceptos/                               ← artículos BOE desde Neo4j
    │   ├── trlgss-art-170.md
    │   └── ...
    │
    ├── trampas/                                 ← 184 reutilizadas del YAML CURADO
    │   ├── _INDICE.md
    │   ├── A/                                   ← A1-A10 Encuadramiento
    │   ├── B/                                   ← IT
    │   ├── C/ D/ E/ ... R/                      ← resto categorías
    │   └── ...
    │
    ├── conceptos/                               ← entidades clave (BR, IT, IPA, CAISS...)
    │
    ├── temas/                                   ← 13 temas del temario oficial (nombre propio OK)
    │   ├── 01-constitucion-trlgss.md
    │   └── ...
    │
    ├── mapas-legales/                           ← Mermaid generados desde JSON BOE
    │
    ├── casos/                                   ← casos prácticos propios (V14.5 + manuales)
    │   └── gaviotas-del-sur-cooperativa.md      ← 🌱 PRIMER CASO SEMILLA
    │
    ├── calculos/                                ← fórmulas extraídas de docstrings calculadoras
    │
    ├── cambios-legislativos-2026/               ← reformas (RDL 2/2023, 11/2024, etc.)
    │
    ├── huecos-ley/                              ← flashcards (cloze) propias
    │
    ├── fichas-vivas/                            ← repaso FSRS
    │
    ├── anclas-memoria/                          ← mnemotecnias propias o más ingenuas
    │
    ├── faq/                                     ← preguntas frecuentes verificadas
    │
    ├── qa/                                      ← tus Q&A con Cascade (siempre tuyas)
    │
    └── lagunas/                                 ← detectadas por el lint
```

---

## 🔒 MURO DE ABSTRACCIÓN — regla operativa

Antes de que cualquier IA (Cascade, Claude Desktop, Gemini, Ollama) escriba en el vault, debe cumplir:

### Prohibido
- ❌ Copiar texto literal de materiales de academias (DM, Valera, Las Cortes, GoKoan)
- ❌ Usar nombres de personajes o empresas reconocibles de simulacros de academias  
  → Lista negra en `meta_auditoria/nombres-evitar.md` (ej.: *Silvia Pastor, Manuel, Landscape MR SL, Jorge, Amaia, HORIZONTE+SOLIDARIO, NEBULA+BYTE*)
- ❌ Replicar orden de temario, secuencia pedagógica o diseño visual de sus esquemas
- ❌ Citar el nombre de academias o preparadores en cualquier nota del vault
- ❌ Incluir en `origen:` referencias del tipo `[DM-SIMULACRO]`, `[VALERA-NOTAS]`

### Permitido
- ✅ Texto literal BOE (Art. 13 LPI, dominio público)
- ✅ Datos oficiales (SMI, PNC, topes cotización, escalas IPT)
- ✅ Jurisprudencia pública (STS, STC)
- ✅ Nuestra nomenclatura pedagógica (Hueco de Ley, Ancla de Memoria, Fichas Vivas, Mapa Legal, Caso Vivo, Ruta Adaptativa, Curva de Dominio)
- ✅ Pool de nombres/empresas propio → `backend/v14/nombres_pool.py` (Antonio García, Carnicería Apocalipto, Bar La Última Ronda…)
- ✅ Nuestros simulacros V14.5 generados
- ✅ Regla/título de trampa escritos por nosotros (conservados del YAML curado)
- ✅ Mnemónicos del YAML si ya son nuestros. Si son flojos, sustituir por otros más ingenuos  
  > Ej.: *"después del día 15 el Estado se preocupa por ti, antes la empresa-madre te cuida y paga"*

---

## ✍️ NOMENCLATURA PROPIA (confirmada, se mantiene)

| Término académico genérico | Nuestro término |
|----------------------------|-----------------|
| Cloze deletion | **Hueco de Ley** |
| Mnemónico | **Ancla de Memoria** |
| Spaced repetition | **Repaso Inteligente** |
| Flashcard | **Ficha Viva** |
| Retention 90% | **Curva de Dominio** |
| Ruta de 55 días | **Ruta Adaptativa** |
| Esquema mental | **Mapa Legal** |
| Test de 18 preguntas | **Caso Vivo** |
| Trampa | **Trampa** ✅ (se queda; término genérico) |

---

## 🔁 FLUJO "PREPARADOR VETERANO" (v5.2)

```
═══════════════════════ YA HECHO ═══════════════════════

✅ FASE 0 — Verificación BOE de 184 trampas
    YAML: academias/.../trampas_unificadas_v2_CURADO.yaml
    Verificación: Claude 4.7 lotes 1-5 (→ 100% según usuario)
    Resultado: reglas/títulos/mnemónicos/artículos → TODO correcto

═══════════════════════ AHORA (hoy) ═══════════════════════

1️⃣  LIMPIEZA NOMBRES (preproceso único)
    Script: limpiar_nombres_yaml.py (a crear)
    - Lee trampas_unificadas_v2_CURADO.yaml
    - Detecta SOLO conjuntos reconocibles:
      · Empresas: HORIZONTE+SOLIDARIO, NEBULA+BYTE, LANDSCAPE MR SL, etc.
      · Combinaciones específicas nombre+empresa+caso que sean trazables
        al simulacro original
    - NO prohibe nombres españoles comunes sueltos (Manuel, Andrea, Jorge...)
      en contextos distintos — son verosímiles
    - Sustituye usando pool propio (nombres_pool.py)
    - Guarda YAML limpio + backup trampas_unificadas_v2_CURADO.yaml.bak
    - Reporta: nº sustituciones, qué cambió

2️⃣  REGENERAR VAULT LIMPIO
    Script: regenerar_vault_trampas.py (YA EXISTE, ya probado)
    - Lee YAML limpio → genera 249+ archivos
    - Frontmatter COSMIC (id, titulo, categoria, estado, criticidad, etc.)
    - Wikilinks automáticos a 17 esquemas
    - Secciones: Regla · Trampa · Mnemónico · Texto BOE · Esquemas relacionados
    - El vault nace limpio (YAML ya se limpió en paso 1)

3️⃣  COMPLETAR VAULT INICIAL
    - Copiar CASO_EJEMPLO_1.md → casos/gaviotas-del-sur-cooperativa.md
      con frontmatter COSMIC + wikilinks a trampas relacionadas
    - Ingestar Neo4j → preceptos/ (~200 artículos clave)
    - Parsear docstrings → calculos/
    - Crear CLAUDE.md del vault + index.md + log.md iniciales

═══════════════════════ DESPUÉS ═══════════════════════

4️⃣  WIKI VIVA (uso diario, sin fricción)
    - INGEST: nueva fuente BOE, apunte spas, simulacro V14.5 → directo al vault
      (NO hace falta Muro de Abstracción porque son fuentes propias/públicas)
    - QUERY: Cascade responde citando wiki
    - LINT periódico (orphans, gaps, contradicciones, densidad wikilinks)
    - CRYSTALLIZE: QAs valiosas → wiki permanente

5️⃣  PROCESAR 200+ MATERIALES DE ACADEMIAS (trabajo grande pendiente)
    Para cada material en `academias/` (Las Cortes, Carlos Hernández, Sara D.,
    Víctor Cabeza, Radi, simulacros 2024):
    ═══ MURO DE ABSTRACCIÓN AQUÍ SÍ ES CRÍTICO ═══
    - Leer en privado
    - Extraer hechos/patrones a meta_auditoria/mapa-calor-academias.md
    - Reformular con nuestra nomenclatura + pool nombres
    - Verificar contra BOE
    - Solo entonces entra al vault como contenido propio
```

---

## 🌱 PRIMER CASO SEMILLA: "Gaviotas del Sur"

Lo tenemos listo y reparado: `@/home/spas/OPOS_GEMINI_1/caso_febrerov2_DM_STYLE.md`

Se copiará como `casos/gaviotas-del-sur-cooperativa.md` con:
- **Frontmatter COSMIC** (tema, trampas asociadas, artículos, nivel)
- **Wikilinks densos** a: `[[trampa-G4-alcance-solidaria]]`, `[[precepto-trlgss-art-18-3]]`, `[[precepto-trlgss-art-142]]`, `[[precepto-trlgss-art-168]]`, `[[rd-1415-2004-art-13]]`, `[[concepto-derivacion-responsabilidad]]`, `[[tema-06-recaudacion-ejecutiva]]`, `[[caso-vivo-cooperativa-trabajo-asociado]]`
- **Notas metodológica** conservada (confirma que es generación propia verificada)
- **Bloques** I-IV con las 14 preguntas y respuestas + explicaciones

Este caso semilla ancla las relaciones iniciales del grafo. A medida que crees más casos con V14.5, se irán uniendo al cluster.

---

## 📜 SCHEMA (`CLAUDE.md` del vault) — contenido esperado

```markdown
# CLAUDE.md — Bóveda OPOS SS (Método NEXO)

Este vault opera bajo el patrón LLM-Wiki de Karpathy adaptado al Método NEXO.
Tres capas: raw (fuentes propias y públicas) + wiki (LLM la mantiene) + schema (este archivo).

## REGLA INVIOLABLE — Muro de Abstracción

Antes de escribir cualquier nota, la IA debe verificar:
1. ¿El texto es texto literal BOE, jurisprudencia pública, nuestros simulacros, 
   nuestro pool de nombres, o redacción propia?  → OK
2. ¿Hay nombres de personas/empresas de la lista `meta_auditoria/nombres-evitar.md`?
   → Sustituir por pool propio (ver `backend/v14/nombres_pool.py`)
3. ¿Menciono "DM", "Valera", "Las Cortes", "GoKoan" o variantes?
   → BORRAR. Solo existe "análisis privado" o "simulacro propio".

## Ingest
- Dropas una fuente en `fuentes/` (solo BOE, jurisprudencia, simulacros V14.5, apuntes spas)
- Yo leo, extraigo entidades, amplío 10-15 páginas con wikilinks densos
- Actualizo `index.md` + `log.md`

## Query
- Leo `index.md` y navego wikilinks
- Sintetizo con citas a páginas wiki
- Archivo respuestas valiosas como nuevas páginas (crystallization)

## Lint
- 0 fantasmas (wikilinks rotos)
- ≥8 wikilinks por página
- ≥5 entrantes por página temática
- 0 orphans
- 100% frontmatter COSMIC: id, titulo, tipo, tags, fuentes, articulos, fecha_creacion, fecha_actualizacion

## Convenciones
- Idioma: español estricto
- Archivos: kebab-case sin tildes
- Páginas: 200-500 palabras
- Wikilinks: [[slug]] sin extensión
```

---

## 📦 PRÓXIMOS PASOS EJECUTABLES

### YA HECHO en esta sesión

1. ✅ Creado plan v5.1 → v5.2 ajustado
2. ✅ Creado skill `.windsurf/workflows/wikiforge-opos.md` (a relajar en v5.2)

### POR HACER tras luz verde del usuario

1. **Relajar skill** `.windsurf/workflows/wikiforge-opos.md`:
   - Muro de Abstracción SOLO al ingestar material externo de academias
   - Quitar blacklist de nombres comunes (Manuel, Andrea, Jorge...)
   - Mantener blacklist de empresas específicas + combinaciones reconocibles

2. **Crear `backend/scripts/limpiar_nombres_yaml.py`** (preproceso único):
   - Input: `trampas_unificadas_v2_CURADO.yaml`
   - Output: mismo archivo con nombres/empresas reconocibles sustituidos
   - Backup: `.bak-<fecha>`
   - Reporte: qué cambió, cuántas veces

3. **Crear `meta_auditoria/`** + `raw_privado/` + `.gitignore` actualizado

4. **🛑 DRY-RUN**: antes de ejecutar `limpiar_nombres_yaml.py`, mostrar al usuario las ~10-20 sustituciones propuestas para validar

5. **Tras aprobación**: ejecutar limpieza YAML → re-ejecutar `regenerar_vault_trampas.py` → completar con preceptos Neo4j + calculos + CASO_EJEMPLO_1 como caso semilla

6. **Post-regeneración**: actualizar `CASOS_TRAMPAS_DM_2026.md` y `index.md`/`log.md` del vault

---

## 🎯 DECISIONES FINALES CONFIRMADAS (v5.2)

| Decisión | Resultado |
|----------|-----------|
| 1. `academias/` y `raw_privado/` | FUERA del vault (en root, gitignored) |
| 2. Regenerar vault | LIMPIO desde cero usando `regenerar_vault_trampas.py` existente |
| 3. `meta_auditoria/` | dentro del root, en `.gitignore`, NUNCA en Syncthing |
| 4. `trampas/` | se queda con ese nombre genérico |
| 5. Nomenclatura pedagógica propia | se mantiene (Hueco de Ley, Mapa Legal, Ancla de Memoria, Ficha Viva…) |
| 6. Trampas ya extraídas y verificadas | se reutilizan SIN reescribir reglas/títulos/mnemónicos/artículos |
| 7. Cambio único en YAML trampas | solo **conjuntos reconocibles** (nombre+empresa+caso específico). Nombres españoles comunes → se quedan |
| 8. Caso semilla | `CASO_EJEMPLO_1.md` (Gaviotas del Sur reparado) → `casos/gaviotas-del-sur-cooperativa.md` |
| 9. Verificación BOE trampas | ya hecha (Claude 4.7), NO se repite |
| 10. Skill/workflow | `.windsurf/workflows/wikiforge-opos.md` — a **relajar** en v5.2 |
| 11. Muro de Abstracción | **aplica al ingestar material externo de academias**, no a cada operación del vault |
| 12. Preproceso limpieza | `limpiar_nombres_yaml.py` aparte del script de regeneración |
| 13. 200+ materiales de academias | siguen pendientes, es el trabajo grande **posterior** |

---

*Plan v5.2 — 20/04/2026 (17:50) — Listo para ejecución previa dry-run del preproceso.*
