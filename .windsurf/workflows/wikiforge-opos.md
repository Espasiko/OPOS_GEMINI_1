---
description: Forja y mantiene la Bóveda OPOS SS siguiendo el patrón LLM-Wiki de Karpathy y el Método NEXO. Detecta intención (setup / ingest / query / lint / crystallize) y ejecuta la operación correcta respetando el Muro de Abstracción.
---

# WikiForge OPOS — Método NEXO

Este workflow transforma materiales verificados (BOE, YAML curado de trampas, docstrings de calculadoras, simulacros y casos propios V14.5, apuntes del usuario) en una wiki de conocimiento viva en Obsidian, sin exponer jamás las fuentes originales.

**Principio rector**: somos dos preparadores veteranos que leen a la competencia en privado, pero todo lo que publicamos es nuestro: verificado contra BOE, con nomenclatura propia y estilo propio.

**Vault destino**: `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/`  
**Plan maestro**: `@/home/spas/OPOS_GEMINI_1/20_04_26_PLAN_WIKI_NEXO_v5_1.md`

---

## 🧭 Detección de intención

Detecta cuál de estas 5 operaciones pide el usuario y salta a la sección correspondiente:

| Intención | Palabras clave | Ir a |
|-----------|----------------|------|
| **SETUP** | "crea el vault", "inicializa la bóveda", "regenera desde cero" | §1 |
| **INGEST** | "añade esta fuente", "ingresa este artículo", "mete en la wiki", "procesa este PDF" | §2 |
| **QUERY** | "qué dice la wiki sobre X", "búscame X", "explícame Y con la wiki" | §3 |
| **LINT** | "revisa la wiki", "check de calidad", "lint" | §4 |
| **CRYSTALLIZE** | "guarda esta respuesta", "archiva esto en la wiki" | §5 |

---

## 🛡️ MURO DE ABSTRACCIÓN — cuándo aplica y cuándo no

**Principio realista**: el problema legal aparece cuando un tercero puede **identificar el material original**. Los nombres propios españoles sueltos (Manuel, Andrea, Jorge…) son **verosímiles** y están por todas partes — no son prohibidos por sí mismos. Lo que prohibe es el **conjunto reconocible**: mismo nombre + misma empresa + mismo caso específico que aparezca en un simulacro concreto de una academia.

### ✅ Muro SE aplica

Sólo al ingestar **material externo nuevo de academias** (Las Cortes, Carlos Hernández, Sara Domínguez, Víctor Cabeza, Radi, DM, Valera…) procedente de `/home/spas/OPOS_GEMINI_1/academias/`:

1. **Leer en privado**. El material queda en `academias/` (gitignored, fuera del vault).
2. **Extraer hechos/patrones** a `meta_auditoria/mapa-calor-academias.md`. Hechos, no texto literal.
3. **Reformular** con redacción propia + nomenclatura NEXO + pool de nombres/empresas.
4. **Verificar contra BOE**.
5. **Solo entonces** la nota entra en el vault.

### ❌ Muro NO se aplica

En operación diaria del vault **ya limpio**:
- Editar trampas, preceptos, casos, conceptos, QAs → normal, sin paranoia
- Ingestar BOE/jurisprudencia/apuntes personales/simulacros V14.5 → fuentes propias o públicas
- Los nombres españoles comunes en nuevos casos propios → permitidos

### 🔴 Blacklist REAL (lo único prohibido)

Consultar `@/home/spas/OPOS_GEMINI_1/meta_auditoria/nombres-evitar.md` (cuando exista). Solo incluye:

1. **Empresas inventadas por academias** que al leerlas se reconocen:
   - `HORIZONTE+SOLIDARIO` · `NEBULA+BYTE` · `LANDSCAPE MR SL` · `LANDSCAPE MR`
2. **Personas reales de academias** (preparadores, autores):
   - `Diego de Miguel` · `Sara Domínguez` · `Carlos Hernández` · `Víctor Cabeza` · `Silvia Pastor` (si es personaje recurrente)
3. **Combinaciones específicas** (solo como tupla, no los nombres sueltos):
   - `Manuel` + empresa concreta + caso A8 tal y como apareció en un simulacro específico
4. **Nombres de academias**: `DM` · `Diego de Miguel` · `Valera` · `Las Cortes` · `GoKoan` · `Adams` · `CEF` → **jamás** en una nota del vault (ni siquiera en `origen:`).

### 🔄 Sustitución cuando detecte coincidencia

- Empresas reconocibles → `EMPRESAS_MEMORABLES` de `@/home/spas/OPOS_GEMINI_1/backend/v14/nombres_pool.py`
- Combinaciones reconocibles → cambiar **sólo la empresa** (no hace falta cambiar el nombre común)
- `origen:` tipo `[DM-SIMULACRO]` → `[ANÁLISIS-INTERNO]` o `[SIMULACRO-PROPIO]`

### Tags origen permitidos en el vault

`[BOE-DIRECTO]` · `[ANÁLISIS-INTERNO]` · `[SIMULACRO-PROPIO]` · `[JURISPRUDENCIA]` · `[CALCULADORA-DOCSTRING]` · `[APUNTE-SPAS]` · `[LEG-CONSOLIDADA]` · `[VERIFICADA-POST-FUSION-2026-04]` · `[VERIFICADA-CON-CORRECCION-2026-04]` · `[VERIFICADA-BOE-2026-04-18]`

---

## §1 SETUP — Crear la bóveda desde cero

Ejecutar **solo** cuando el usuario confirme explícitamente. Nunca destructivo sin confirmación.

### Precondiciones

1. Verificar que `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/` está vacío o se puede vaciar.
2. Verificar que existe `academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml`.
3. Verificar que Neo4j está levantado en `bolt://localhost:7687`.
4. Verificar que existe `backend/v14/nombres_pool.py`.
5. Verificar que existe `caso_febrerov2_DM_STYLE.md`.

### Pasos

1. **Crear estructura de directorios privados** (fuera del vault):
   - `/home/spas/OPOS_GEMINI_1/raw_privado/` (con README explicando uso)
   - `/home/spas/OPOS_GEMINI_1/meta_auditoria/` (con README + `nombres-evitar.md` + `muro-abstraccion.md`)

2. **Actualizar `.gitignore`** del root con:
   ```
   raw_privado/
   meta_auditoria/
   ```
   (academias/ ya debería estar ignorado)

3. **Crear estructura del vault** `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/`:
   ```
   CLAUDE.md
   README.md
   index.md
   log.md
   fuentes/
   preceptos/
   trampas/{A,B,C,D,E,F,G,H,I,J,K,L,M,N,N_AUTO,O,P,Q,R,CA}/
   conceptos/
   temas/
   mapas-legales/
   casos/
   calculos/
   cambios-legislativos-2026/
   huecos-ley/
   fichas-vivas/
   anclas-memoria/
   faq/
   qa/
   lagunas/
   ```

4. **Escribir `CLAUDE.md`** del vault con: Muro de Abstracción + Ingest/Query/Lint + convenciones (copiar del §7 de `@/home/spas/OPOS_GEMINI_1/20_04_26_PLAN_WIKI_NEXO_v5_1.md`).

5. **Ejecutar** en orden:
   a. **`backend/scripts/limpiar_nombres_yaml.py`** (preproceso único):  
      Detecta y sustituye SOLO conjuntos reconocibles en el YAML curado. Dry-run previo al usuario.
   b. **`scripts/maintenance/regenerar_vault_trampas.py`** (ya existe, probado):  
      Lee YAML limpio → genera 249+ archivos en `wiki/trampas/` con frontmatter COSMIC + wikilinks a 17 esquemas + secciones Regla/Trampa/Mnemónico/Texto BOE.
   c. **Consulta Neo4j** → `wiki/preceptos/` (~200 artículos clave, texto literal BOE).
   d. **Parsea docstrings** `backend/calculators/calculos_ss_extended.py` + `calculadora_age.py` → `wiki/calculos/`.
   e. **Copia `CASO_EJEMPLO_1.md`** → `wiki/casos/gaviotas-del-sur-cooperativa.md` con frontmatter + wikilinks densos a trampas (G4, R11, etc.) + preceptos (TRLGSS Art. 18.3, 142, 168.2).
   f. **Genera `CLAUDE.md`, `index.md`, `log.md`** iniciales del vault.

6. **Obligatorio**: ejecutar LINT (§4) al terminar.

7. **Reportar**: nº archivos creados, nº trampas filtradas, nº nombres sustituidos, nº wikilinks, ruta vault.

### Parada obligatoria

Antes de empezar el SETUP, mostrar al usuario:
- Ruta del vault y que se va a vaciar
- Lista de directorios que se crearán
- Sample de 5 notas generadas (dry-run)
- **Esperar "adelante" explícito del usuario**.

---

## §2 INGEST — Añadir una fuente al vault

Para cualquier fuente nueva (BOE novedoso, apunte spas, transcripción, simulacro V14.5).

### Pasos

1. **Clasificar la fuente**. Tipo: `boe` / `jurisprudencia` / `simulacro_propio` / `apunte_personal` / `docstring_calculadora` / `yaml_trampa` / `material_academia`.
2. **Si es material de academia** → aplicar Muro de Abstracción completo (§ superior). El material queda en `academias/`. Solo entra al vault la extracción/reformulación propia.
3. **Si es fuente propia o pública** → proceder directo, sin fricción.
4. **Crear página en `fuentes/`** con frontmatter COSMIC:
   ```yaml
   ---
   id: fuente-<slug>
   tipo: fuente
   tipo_fuente: boe | jurisprudencia | simulacro_propio | apunte | docstring
   tags: [fuente, <dominio>]
   articulos: [<lista-articulos-citados>]
   fecha_creacion: YYYY-MM-DD
   fecha_actualizacion: YYYY-MM-DD
   origen: "[BOE-DIRECTO]" | "[JURISPRUDENCIA]" | "[SIMULACRO-PROPIO]" | "[APUNTE-SPAS]"
   ---
   ```
5. **Extraer entidades** del contenido: conceptos, artículos citados, plazos, fórmulas, casos.
6. **Actualizar / crear páginas temáticas**:
   - Si ya existe → amplía, no duplica
   - Enlaza con `[[wikilinks]]` mínimo 8, distribuidos en el cuerpo
7. **Actualizar `index.md`** con la nueva entrada.
8. **Registrar en `log.md`**:
   ```
   ## [YYYY-MM-DD] ingest | <Título fuente>
   - Páginas creadas: X
   - Páginas actualizadas: Y
   - Entidades extraídas: <lista breve>
   - Origen: <tipo>
   ```

### Frontmatter COSMIC universal

```yaml
---
id: <slug-kebab-case>
titulo: "Título humano"
tipo: precepto | trampa | concepto | tema | caso | fuente | flashcard | faq | mapa-legal | calculo | cambio-legislativo
categoria: A | B | ... | R | CA | null
articulos: ["Art. 170.3 TRLGSS", "Art. 13 RGRSS"]
tags: [<tema>, <norma>, <subtema>]
peso_examen: alto | medio | bajo
verificado_boe: YYYY-MM-DD  # solo si aplica
confidence: 0.0 - 1.0
fuentes: ["id-fuente-1"]
fecha_creacion: YYYY-MM-DD
fecha_actualizacion: YYYY-MM-DD
origen: "[BOE-DIRECTO]" | "[ANÁLISIS-INTERNO]" | "[SIMULACRO-PROPIO]" | "[JURISPRUDENCIA]" | "[CALCULADORA-DOCSTRING]" | "[APUNTE-SPAS]"
---
```

---

## §3 QUERY — Responder preguntas con el vault

1. Leer `index.md` para localizar páginas relevantes.
2. Leer las páginas encontradas (seguir wikilinks si hace falta).
3. Sintetizar respuesta con **citas a páginas wiki** usando el formato `@/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/trampas/B/B09-recaida-it.md:1-30`.
4. Si la respuesta genera contenido valioso → ofrecer al usuario archivarla como nueva página (ir a §5 Crystallize).
5. Si hay laguna (tema mencionado sin página propia) → añadir entrada a `lagunas/<tema>.md`.

---

## §4 LINT — Mantenimiento obligatorio post-batch

Ejecutar tras cada ingesta grande (>5 páginas) y periódicamente.

### Checklist

1. **Frontmatter**. 100% de notas con los campos COSMIC requeridos. Reportar nº conformes y nº a corregir.
2. **Idioma**. 100% en español.
3. **Fantasmas** (wikilinks rotos). Listar todos los targets de `[[...]]` y verificar que existen como `.md`. Crear páginas faltantes o corregir links.
4. **Densidad**. Cada página temática (no índice, no log) con ≥8 wikilinks. Reportar las que incumplen.
5. **Entrantes**. Cada página temática con ≥5 enlaces entrantes. Añadir links desde páginas relacionadas si alguna queda aislada.
6. **Fuentes vinculadas**. Toda página en `fuentes/` debe referenciarse desde al menos una nota temática.
7. **Orphans**. Páginas sin enlaces entrantes → conectarlas o marcar para revisión.
8. **Gaps**. Conceptos mencionados 3+ veces sin página propia → crearlos.
9. **Muro de Abstracción**. Grep global contra lista `meta_auditoria/nombres-evitar.md` + palabras prohibidas (`DM`, `Valera`, `Las Cortes`, `GoKoan`, `Adams`, `CEF`). Si aparece alguna → corregir.
10. **Contradicciones**. Claims sobre el mismo artículo con versiones distintas → marcar para revisión humana.

Registrar en `log.md`:
```
## [YYYY-MM-DD] lint
- Frontmatter OK: X/Y
- Idioma OK: X/Y
- Fantasmas: N corregidos
- Densidad <8: N corregidos
- Orphans: N conectados
- Muro de Abstracción: N violaciones corregidas
- Gaps detectados: <lista>
```

---

## §5 CRYSTALLIZE — Archivar respuesta valiosa

Cuando el usuario o tú detectáis que una respuesta merece quedarse:

1. Generar slug a partir del título.
2. Elegir carpeta destino (`conceptos/` / `faq/` / `casos/` / etc.).
3. Crear página con frontmatter COSMIC completo.
4. Densidad wikilinks ≥8, distribuidos.
5. Aplicar Muro de Abstracción.
6. Actualizar `index.md` + `log.md`.
7. Si ya existe página relacionada → **amplía**, no dupliques.

---

## 📋 Plantilla base de página temática

```markdown
---
id: <slug>
titulo: "<Título humano>"
tipo: <tipo>
categoria: <letra o null>
articulos: []
tags: []
peso_examen: <nivel>
verificado_boe: YYYY-MM-DD
confidence: 0.0
fuentes: []
fecha_creacion: YYYY-MM-DD
fecha_actualizacion: YYYY-MM-DD
origen: "<tag>"
---

# <Título>

Descripción clara en 2-3 párrafos con [[wikilinks]] a páginas relacionadas directamente en el texto.

## Regla

Enunciado preciso de la regla legal con cita BOE. Usa [[precepto-trlgss-art-X]] para enlazar al artículo.

## Ancla de Memoria

> Mnemónico ingenuo y memorable. Ej.: *"Después del día 15 el Estado se preocupa por ti; antes, la empresa-madre te cuida y paga."*

## Ejemplo / Caso Vivo

> Caso breve con nombres del pool propio. [[caso-<slug>]] para el caso completo.

## Trampa típica

Qué confusión induce el examen. Wiki-link a [[trampa-<categoria>-<numero>]] si procede.

## Relaciones

- Precepto base: [[precepto-<slug>]]
- Tema: [[tema-<num>-<slug>]]
- Conceptos: [[concepto-<slug>]]
- Caso: [[caso-<slug>]]
- Trampa relacionada: [[trampa-<slug>]]

## Fuentes

- [[fuente-boe-trlgss-2015]]
```

---

## 🚫 Qué NO hace este workflow

- No toca `/academias/`
- No genera casos prácticos nuevos (eso lo hace V14.5 del backend)
- No verifica BOE (ya está hecho en los lotes 1-7)
- No recalcula fórmulas (ya están en calculadoras Python)
- No sustituye al frontend React (la wiki es estudio personal, no UI de usuarios)

## ✅ Qué SÍ garantiza este workflow

- Coherencia estructural (mismo frontmatter en todas las notas)
- Muro de Abstracción aplicado sistemáticamente
- Grafo denso (mín 8 wikilinks por página)
- Acumulación de conocimiento (crystallize) en vez de pérdida en chats
- Detección automática de lagunas y gaps
- Compatibilidad con Dataview, Graph view, Syncthing
