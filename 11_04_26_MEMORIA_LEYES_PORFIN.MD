# 📋 MEMORIA DE SESIÓN — 11/04/2026
## OPOS_GEMINI_1 — Ingesta Neo4j + Análisis DM + Rearquitectura V14

---

## 1. ESTADO ACTUAL NEO4J (al cierre de sesión)

| Métrica | Valor |
|---------|-------|
| **Nodos Ley** | 101 |
| **Nodos Precepto** | 6.246 |
| **Índice vectorial** | HNSW cosine, dim=1024, m=16, ef=100 |
| **Modelo embedding** | `pablosi/bge-m3-spa-law-qa-trained-2` |
| **Catálogo** | `catalog_v17.json` → versión **v17.3** (102 entradas) |

---

## 2. LEYES INGRESADAS EN ESTA SESIÓN (15 nuevas AGE)

| Siglas | BOE ID (verificado) | Preceptos |
|--------|-------------------|-----------|
| LO 3/2018 (LOPDGDD) | BOE-A-2018-16673 | 141 |
| LO 3/2007 (Igualdad) | BOE-A-2007-6115 | 120 |
| LO 1/2004 (Violencia género) | BOE-A-2004-21760 | 106 |
| Ley 50/1997 (Ley Gobierno) | BOE-A-1997-25336 | 34 |
| LO 2/1979 (Tribunal Constitucional) | BOE-A-1979-23709 | 10 |
| LO 6/1985 (Poder Judicial) | BOE-A-1985-12666 | 46 |
| LO 3/1981 (Defensor del Pueblo) | BOE-A-1981-10325 | 2 |
| Ley 7/1985 (Bases Régimen Local) | BOE-A-1985-5392 | 192 |
| Ley 19/2013 (Transparencia) | BOE-A-2013-12887 | 58 |
| RD 364/1995 (Reglamento Ingreso AGE) | BOE-A-1995-8729 | 97 |
| RD 365/1995 (Cuerpos y Escalas AGE) | BOE-A-1995-8730 | 33 |
| RD 203/2021 (e-Administración) | BOE-A-2021-5032 | 84 |
| RD 311/2022 (ENS) | BOE-A-2022-7191 | 49 |
| Ley 36/2011 (LRJS) | BOE-A-2011-15936 | 326 |
| **LO 3/1980 (Consejo de Estado)** | BOE-A-1980-8648 | **0 ⚠️ RE-INGESTAR** |

> ⚠️ **LO 3/1980** ingresó el nodo `Ley` pero 0 `Precepto`. Necesita fallback HTML:
> ```bash
> .venv/bin/python backend/scripts/ingest_boe_html_historico.py \
>   --boe-id BOE-A-1980-8648 --ingest
> ```

**LEC (Ley 1/2000):** Cancelada — NO es temario AGE/SS. Es derecho procesal civil (Letrados AJ, Gestión Procesal). Marcada `prioridad: baja` en catálogo.

---

## 3. LEYES FALTANTES — EL USUARIO BUSCA LOS IDs

### 3.1 Reglamentos SS Críticos (bloque específico examen SS)

> **⚠️ La API consolidada BOE devuelve 404 para todos. Posiblemente no consolidados o IDs distintos. Buscar manualmente en https://www.boe.es/buscar/legislacion.php**

| Nº | Nombre oficial | Sigla | ¿Dónde buscar? |
|----|---------------|-------|----------------|
| 1 | **Real Decreto 84/1996, de 26 de enero**, por el que se aprueba el Reglamento General sobre inscripción de empresas y afiliación, altas, bajas y variaciones de datos de trabajadores en la Seguridad Social | RD 84/1996 | BOE ~enero-febrero 1996 |
| 2 | **Real Decreto 2064/1995, de 22 de diciembre**, por el que se aprueba el Reglamento General sobre Cotización y Liquidación de otros Derechos de la Seguridad Social | RD 2064/1995 | BOE ~diciembre 1995 |
| 3 | **Real Decreto 1415/2004, de 11 de junio**, por el que se aprueba el Reglamento General de Recaudación de la Seguridad Social | RD 1415/2004 | BOE ~junio 2004 |
| 4 | **Real Decreto 1430/2009, de 11 de septiembre** (gestión financiera SS / IT) | RD 1430/2009 | BOE ~septiembre 2009 |
| 5 | **Real Decreto 1300/1995, de 21 de julio**, por el que se desarrolla en materia de incapacidades laborales del sistema de la SS | RD 1300/1995 | BOE ~agosto 1995 |
| 6 | **Ley 39/2006, de 14 de diciembre**, de Promoción de la Autonomía Personal y Atención a las personas en situación de dependencia | Ley 39/2006 | BOE 15 diciembre 2006 |

### 3.2 Una vez tengas los IDs — cómo añadirlos al catálogo

```json
{
  "boe_id": "BOE-A-XXXX-XXXXX",
  "siglas": "RD 84/1996",
  "titulo": "Real Decreto 84/1996...",
  "url": "https://www.boe.es/buscar/act.php?id=BOE-A-XXXX-XXXXX",
  "parte": "2-SS",
  "cuerpos": ["A1", "A2", "C1"],
  "boe_id_verificado": true,
  "historica": false,
  "tiene_xml": true,
  "prioridad": "critica",
  "notas": "Reglamento General Afiliación. Temas 15-18 examen SS."
}
```

Luego ingestar:
```bash
.venv/bin/python backend/scripts/ingest_neo4j_v17.py \
  --only-law BOE-A-XXXX-XXXXX --skip-purge
```

### 3.3 Resto de leyes faltantes del Código Laboral SS (id=093) — NO examen

Hay ~100 normas en el código de las que solo tenemos las principales. El listado completo de faltantes lo genera:
```bash
.venv/bin/python check_codigo_ss.py
```

---

## 4. CAMBIOS EN EL CATÁLOGO (catalog_v17.json)

| Versión | Fecha | Cambios |
|---------|-------|---------|
| v17.0 | anterior | 84 leyes base (SS, CE, LPAC, LRJSP, TREBEP…) |
| v17.1 | 07/04/2026 | Añadidas `Orden PJC/297/2026` y `RD-ley 3/2026` (valores SS 2026) |
| v17.2 | 10/04/2026 | +15 leyes AGE generales (ver tabla §2). LEC incluida por error. Total: 101 |
| **v17.3** | **11/04/2026** | LEC → `prioridad: baja` + nota "NO es temario AGE/SS". LO 3/1980 (Consejo de Estado, BOE-A-1980-8648) añadida. Total: **102** |

**Campos de cada entrada:**
```
boe_id, siglas, titulo, url, parte, cuerpos, boe_id_verificado,
historica, tiene_xml, prioridad, notas
```

**Partes usadas:**
- `"1-AGE"` — temas administrativos generales
- `"2-SS"` — temas Seguridad Social específicos
- `"3-laboral"` — laboral / ET / autónomos

---

## 5. SCRIPTS CREADOS EN ESTA SESIÓN

### 5.1 `backend/scripts/ingest_boe_html_historico.py` ⭐ NUEVO
Parser BeautifulSoup para versiones HTML históricas del BOE (`?p=YYYYMMDD`).

**Uso:**
```bash
# Dry-run (solo parsear, no ingestar)
.venv/bin/python backend/scripts/ingest_boe_html_historico.py \
  --boe-id BOE-A-1980-8648 --fecha 20251216 --dry-run

# Ingestar / actualizar en Neo4j
.venv/bin/python backend/scripts/ingest_boe_html_historico.py \
  --boe-id BOE-A-1980-8648 --ingest
```

**Estructura HTML que parsea:**
- `div.bloque` → precepto
- `h5.articulo` → título del artículo
- `p.parrafo` → texto del precepto
- Extrae título de la ley de `<h2>` o `<h3>`

**Probado con:** LRJSP → 219 preceptos extraídos correctamente.

---

### 5.2 `backend/scripts/load_valores_2026.py` ⭐ NUEVO
Crea nodos `ValorLegal` en Neo4j con los datos numéricos de la SS para 2026.

**Tablas que carga:**

| Tabla | Contenido |
|-------|-----------|
| Bases cotización RGSS 2026 | Mínima: 1.381,20 €/mes. Máxima: 4.909,50 €/mes |
| MEI 2026 | 0,80% (trabajador 0,67% + empresa 0,13%) |
| Cotización adicional solidaridad 2026 | Tramo >1x base máx.: +0,92% / +5,5% empresa |
| Desempleo RGSS | 1,55% trabajador + 5,50% empresa (contrato indefinido) |
| FOGASA | 0,20% empresa |
| Formación profesional | 0,10% trabajador + 0,60% empresa |
| Pensión máxima 2026 | 3.267,60 €/mes (14 pagas) |
| Revalorización pensiones 2026 | +2,8% (IPC media 2025) |
| SMI 2026 | 1.184 €/mes (14 pagas) = 16.576 €/año |
| Edad jubilación ordinaria 2026 | 66 años y 8 meses (sin 38 años y 3 meses cotizados) |
| Edad jubilación con cotización completa | 65 años (con ≥38 años y 3 meses) |

**Uso:**
```bash
.venv/bin/python backend/scripts/load_valores_2026.py
```

---

### 5.3 `check_new_laws.py` — Check rápido de ingesta
```bash
.venv/bin/python check_new_laws.py
```
Muestra preceptos por ley y estado OK/PENDIENTE.

### 5.4 `check_codigo_ss.py` — Comparar códigos BOE con Neo4j
```bash
.venv/bin/python check_codigo_ss.py
```
Compara los códigos BOE id=082 (AGE), id=093 (SS/Laboral) y id=003 (Función Pública) contra Neo4j.

### 5.5 `check_ss_exam_laws.py` — Leyes clave examen SS
```bash
.venv/bin/python check_ss_exam_laws.py
```
Lista de 31 leyes clave del examen con estado ✅/❌ y prioridad.

---

## 6. BUG ARREGLADO — `mcp0_find_related_laws`

**Fichero:** `/home/spas/.local/share/uv/tools/mcp-boe/lib/python3.12/site-packages/mcp_boe/tools/legislation.py`

**Bug:** La función `_format_law_analysis` y `_format_law_relations` asumían que `referencias` era siempre un `dict`, y que `anteriores`/`posteriores` eran siempre `list`. La API BOE devuelve ambos en formatos variables.

**Fix aplicado (líneas 586-620 y 1037-1049):**
```python
# Antes:
refs = analisis.get('referencias', {})
anteriores = refs.get('anteriores', [])

# Después:
refs = analisis.get('referencias', {})
if isinstance(refs, list):
    refs = {}  # normalizar
anteriores = refs.get('anteriores', [])
if isinstance(anteriores, dict):
    anteriores = [anteriores]  # normalizar a lista
```

---

## 7. PROBLEMA BUCLE INFINITO — CaseSchemaBuilder V14

### 7.1 Contexto
Durante el análisis de **3 casos DM reales** (enero, febrero, diciembre 2025) para comparar con V14.5, se detectó un problema de **bucle infinito** en la generación de casos complejos.

### 7.2 Causa raíz
El flujo `build_complex()` → `ProseValidator.validate()` → reintento generaba un bucle:

```
generate_schema → validate_prose → FAIL → regenerate → validate → FAIL → ∞
```

Causas específicas:
1. **`ProseValidator` con matching exacto** de nombres de personajes → falsos negativos
2. **`conflictos_cruzados`** no se generaba antes de validar → siempre fallaba
3. **`_validar_prerrequisitos_personajes`** no se llamaba → personajes incoherentes (edad vs años cotizados)
4. **Ausencia de `max_retries`** en el loop de generación

### 7.3 Fixes aplicados

**`CaseSchemaBuilder.build_complex()`** (`backend/v14/case_schema_builder.py`):
```python
# Añadido después de generar personajes:
personajes = self._validar_prerrequisitos_personajes(personajes, blueprint_ids)
# ...
schema.conflictos_cruzados = self._generar_conflictos_cruzados(personajes, blueprint_ids)
```

**`ProseValidator`** (`backend/v14/prose_validator.py`):
```python
# Antes: matching exacto
if personaje.nombre not in texto:

# Después: matching parcial (cualquier palabra ≥4 letras)
words = [w for w in personaje.nombre.split() if len(w) >= 4]
if not any(w.lower() in texto.lower() for w in words):
```

**Validación de conflictos:** normalización de slugs a texto plano sin acentos + verificación de palabras significativas.

---

## 8. ANÁLISIS 3 CASOS DM REALES + REARQUITECTURA V14

### 8.1 Patrones detectados en los casos DM

| Caso | Mes | Patrón principal |
|------|-----|-----------------|
| Enero 2025 | Enero | Empresa + personajes con cotizaciones exactas. Bloque único coherente |
| Febrero 2025 | Febrero | Bloques independientes: cooperativa, IT/IP, no contributiva, RETA, IT menstrual |
| Diciembre 2025 | Diciembre | Empresa + cotización + recaudación (embargos, deudas, plazos) |

**Características DM:**
- Fechas exactas para cálculo de plazos (días naturales vs hábiles)
- Personajes con doble encuadramiento (RGSS + RETA)
- Preguntas calculadoras con fórmulas exactas
- Bloques independientes por tema (no siempre un hilo narrativo central)

### 8.2 Comparativa V14.5 vs DM

| Métrica | DM Real | V14.5 |
|---------|---------|-------|
| Personajes/caso | 2-4 | 3-6 ✅ |
| Temas entrelazados | 2-3 | 4-7 ✅ |
| Preguntas | 18 | 12-15 ❌ |
| Validación OK | ~manual | 95%+ ✅ |
| Diversidad nombres | Alta | Baja ❌ |
| Formato tabla | HTML | Markdown ❌ |
| Citas BOE | Raras | Frecuentes (¿demasiadas?) |

### 8.3 Rearquitectura propuesta (plan `.windsurf/plans/diversidad-casos-v14-332554.md`)

**Problema 1 — Nombres hardcodeados en blueprints**
```python
# Fix: pool de nombres aleatorios
NOMBRES_POOL = ["Elena Vega", "Carlos Ruiz", "Ana Moreno", ...]
personaje.nombre = random.choice(NOMBRES_POOL)
```

**Problema 2 — Solo 12-15 preguntas (DM siempre tiene 18)**
```python
# Fix: padding de preguntas hasta 18
while len(preguntas) < 18:
    preguntas.extend(fill_questions_from_pool(blueprint_ids))
```

**Problema 3 — Formato markdown vs DM plain text**
```yaml
# redactor_v14.yaml: cambiar
format: markdown  →  format: plain_text_dm_style
```

**Problema 4 — Un solo blueprint por caso (poca diversidad)**
```python
# Fix: usar build_complex con 2-3 blueprints
schema = builder.build_complex(
    blueprint_ids=["BP-S12", "BP-S07", "BP-S15"],  # múltiples
    num_personajes=4
)
```

**Problema 5 — Validación de personajes incoherentes**
Ya arreglado con `_validar_prerrequisitos_personajes()`:
- `anos_cotizados` ≤ `edad - 16`
- Mínimo 15 años para jubilación ordinaria
- Mínimo 35 años para jubilación anticipada (BP-S12)

---

## 9. COMPARATIVA CÓDIGOS BOE vs NEO4J

### Código AGE estructura (id=082) — Resultado

| Ley | Neo4j | Relevancia examen |
|-----|-------|------------------|
| CE | ✅ OK | Crítica |
| LRJSP (Ley 40/2015) | ✅ OK | Crítica |
| LPAC (Ley 39/2015) | ✅ OK | Crítica |
| Ley Gobierno (50/1997) | ✅ OK | Media |
| **LO 3/1980 Consejo de Estado** | ✅ Ingresada (0 preceptos ⚠️) | Media |
| RDs estructura ministerial 2023/2024 | ❌ Falta | **Nula** — no examinable |

### Código Laboral/SS (id=093) — Leyes examen OK

| Ley | Neo4j |
|-----|-------|
| LGSS (RDL 8/2015) | ✅ BOE-A-2015-11724 |
| ET (RDL 2/2015) | ✅ BOE-A-2015-11430 |
| IMV (Ley 19/2021) | ✅ BOE-A-2021-21007 |
| RDL 13/2022 (Autónomos cotización) | ✅ BOE-A-2022-12482 |
| LETA | ✅ BOE-A-2007-13409 |
| Ley 36/2011 LRJS | ✅ BOE-A-2011-15936 |

### Código Función Pública (id=003) — Estado

65 de 74 normas del código faltan en Neo4j — la mayoría son RDs y Órdenes muy específicos (selección, retribuciones, permisos) no directamente examinables en el temario general.

---

## 10. PRÓXIMOS PASOS (T29 pendiente)

### Paso 1 — Buscar IDs BOE manualmente (usuario)
Buscar en https://www.boe.es/buscar/legislacion.php los IDs de las 6 leyes del §3.1.

### Paso 2 — Añadir al catálogo y verificar XML
```bash
# Verificar que el ID es correcto
curl -s -H "Accept: application/xml" \
  "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{BOE_ID}" \
  | grep -E "<(code|titulo|fecha_actualizacion|estatus_derogacion)>"
```

### Paso 3 — Ingestar
```bash
.venv/bin/python backend/scripts/ingest_neo4j_v17.py \
  --only-law {BOE_ID} --skip-purge
```

### Paso 4 — Re-ingestar LO 3/1980 con HTML parser
```bash
.venv/bin/python backend/scripts/ingest_boe_html_historico.py \
  --boe-id BOE-A-1980-8648 --ingest
```

### Paso 5 — Post-ingesta: verificar cobertura completa
```bash
.venv/bin/python check_ss_exam_laws.py
.venv/bin/python check_codigo_ss.py
```

---

## 11. PARÁMETROS DE CHUNKING (ingest_neo4j_v17.py)

| Parámetro | Valor | Equivalencia |
|-----------|-------|-------------|
| `MAX_CHARS_PER_CHUNK` | 20.000 chars | ~5.000 tokens |
| `CHUNK_OVERLAP_CHARS` | 2.000 chars | ~500 tokens solapamiento |
| `BATCH_SIZE_EMBED` | 16 nodos | por batch embedding |
| `BATCH_SIZE_NEO4J` | 50 nodos | por UNWIND a Neo4j |
| `BOE_API_DELAY` | 0,8 s | entre llamadas API |
| `EMBEDDING_DIM` | 1.024 | dimensión vectores |
| `CHECKPOINT_EVERY_N` | 5 leyes | frecuencia checkpoint |

**Fallback chain BOE:** XML API → ELI HTML → `act.php` HTML scraping → `ingest_boe_html_historico.py`

---

*Documento generado: 11/04/2026 — OPOS_GEMINI_1*
