# 📋 ANÁLISIS COMPLETO RAG + PLAN DE MEJORAS (CORREGIDO)

**Fecha:** 15/01/2026  
**Objetivo:** Investigar configuración COMPLETA del sistema RAG (Qdrant + PostgreSQL)

---

## 📊 RESUMEN EJECUTIVO

| Componente | Valor |
|------------|-------|
| **Qdrant Storage** | **610 MB** |
| **Qdrant Puntos** | ~98,000 |
| **Qdrant Vectores** | ~188,000 |
| **PostgreSQL laws** | 48,866 rows |
| **PostgreSQL leyes_catalogo** | 54 leyes |
| **Modelo embeddings de pablosi/...** | bge-m3-spa-law-qa-trained-2 (1024D) |

---

## 🐳 INFRAESTRUCTURA DOCKER

### Qdrant:
```
Container: opositaia-qdrant
Imagen: qdrant/qdrant:v1.12.0
Storage: 610 MB
Puerto: 6333 (HTTP), 6334 (gRPC)
Volumen: opos_gemini_1_qdrant_storage
```

### PostgreSQL:
```
Container: opositaia-postgres
BD: opositaia
Tablas: laws, leyes_catalogo
```

---

## 📚 COLECCIONES QDRANT

| Colección | Puntos | Vectores | Dim | Tipo |
|-----------|--------|----------|----:|------|
| opositaia_knowledge_hybrid | 48,866 | 95,132 | 1024 | Dense + Sparse |
| opositaia_knowledge_hybrid_FULL | 48,329 | 93,329 | 1024 | Dense + Sparse |
| leyes_espana | 1,067 | 0 | 768 | Dense only |

### Configuración HNSW:
```json
{
  "m": 16,
  "ef_construct": 100,
  "full_scan_threshold": 10000,
  "on_disk": false
}
```

---

## 🗄️ ESQUEMA POSTGRESQL COMPLETO

### Tabla: `leyes_catalogo` (54 filas, 51 columnas)

#### Identificación:
| Campo | Tipo | Ejemplo |
|-------|------|---------|
| boe_id | text | BOE-A-2015-11724 |
| identificador_eli | text | /es/ley/2015/11724 |
| nombre_corto | text | LGSS |
| titulo | text | Ley General de la Seguridad Social |

#### Clasificación:
| Campo | Tipo | Ejemplo |
|-------|------|---------|
| tipo_norma | text | Ley, Ley Orgánica, RD, Orden |
| rango_codigo | integer | 1-10 |
| rango_nombre | text | Ley, Real Decreto |
| departamento_nombre | text | Ministerio de Trabajo |

#### Fechas y Vigencia:
| Campo | Tipo | Ejemplo |
|-------|------|---------|
| fecha_publicacion | date | 2015-10-31 |
| fecha_entrada_vigor | date | 2016-01-01 |
| fecha_derogacion | date | NULL (vigente) |
| vigente | boolean | true |
| consolidado | boolean | true |

#### URLs (5 tipos):
| Campo | Ejemplo |
|-------|---------|
| url_boe | https://www.boe.es/buscar/doc.php?id=BOE-A-2015-11724 |
| url_eli | /eli/es/ley/2015/11724 |
| url_pdf | https://www.boe.es/boe/dias/2015/10/31/pdfs/BOE-A-2015-11724.pdf |
| url_xml | https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724&tn=0 |
| url_html | https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724 |

#### Análisis de Modificaciones (JSONB):
| Campo | Contenido |
|-------|-----------|
| analisis_modificaciones | Array de leyes que la modifican |
| analisis_afecta_a | Leyes afectadas por esta |
| analisis_afectada_por | Leyes que afectan a esta |

#### Estructura:
| Campo | Tipo |
|-------|------|
| num_articulos | integer |
| num_disposiciones_adicionales | integer |
| num_disposiciones_transitorias | integer |
| num_disposiciones_finales | integer |
| num_disposiciones_derogatorias | integer |
| tiene_anexos | boolean |
| num_anexos | integer |

#### Contenido:
| Campo | Tipo |
|-------|------|
| texto_completo | text (XML parseado) |
| xml_original | text (XML crudo) |
| indice_estructurado | jsonb |
| metadata_xml | jsonb |

#### Clasificación Temática:
| Campo | Tipo |
|-------|------|
| materias | text[] |
| palabras_clave | text[] |
| tags | text[] |
| leyes_relacionadas | text[] |

---

### Tabla: `laws` (48,866 filas - chunks)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | text | UUID del chunk |
| law_id | text | BOE-ID de la ley |
| law_name | text | Nombre de la ley |
| title | text | Título del artículo/bloque |
| content | text | Contenido del chunk |
| xml_content | text | XML original (solo documentos) |
| metadata | text | Metadatos serializados |
| created_at | timestamp | Fecha de creación |

#### Ejemplo de datos:
```
law_id: BOE-A-1978-31229
title: Artículo 1 | Artículo 2 | Bloque preambulo (Chunk 1)
content: ~400-800 caracteres
xml_content: NULL (para chunks) | XML completo (para documentos)
```

---

## 🔧 CHUNKING ACTUAL

### Parámetros (process_and_chunk.py):
```python
PARAMS = {
    "chunk_size": 800,        # caracteres
    "overlap": 150,           # caracteres (18.75%)
    "min_chunk_size": 200,    # mínimo
}
```

### Lógica:
1. Parsea JSON del BOE
2. Extrae bloques/artículos
3. Divide en chunks de 800 chars máximo
4. Aplica overlap de 150 chars
5. Respeta límites de frases (`.` `?` `!`)

### Layers:
- `document`: Metadatos de la ley completa
- `article_chunk`: Chunks de artículos individuales
- `article_full`: Artículo completo si <800 chars

---

## ✅ LO QUE YA TENEMOS (NO TOCAR)

| Aspecto | Estado | Detalle |
|---------|--------|---------|
| Búsqueda híbrida | ✅ | Dense (1024D) + Sparse |
| Metadatos vigencia | ✅ | En PostgreSQL leyes_catalogo |
| URLs completas | ✅ | BOE, ELI, PDF, XML, HTML |
| XMLs originales | ✅ | En xml_original |
| Análisis modificaciones | ✅ | JSONB en leyes_catalogo |
| Estructura artículos | ✅ | num_articulos, disposiciones |
| Materias/tags | ✅ | Arrays en leyes_catalogo |
| Reranker BGE | ✅ | Modelo entrenado |
| Query expansion | ✅ | Salamandra |

---

## 🟡 GAPS IDENTIFICADOS (MEJORABLES)

### 1. Metadatos NO sincronizados con Qdrant

**Problema:** PostgreSQL tiene 51 campos de metadatos, pero Qdrant solo guarda:
- boe_id
- law_name
- article_title
- text_snippet
- layer

**Solución propuesta:** Sincronizar metadatos críticos:
- vigente
- fecha_entrada_vigor
- tipo_norma
- rango_nombre
- url_html

---

### 2. Chunking por caracteres, no semántico

**Actual:**
```
"Bloque preambulo" → 833 chars
"Bloque preambulo (Chunk 1)" → 412 chars
```

**Problema:** Corta texto a mitad de frase/concepto

**Solución propuesta:** Chunking por:
- Artículo completo si <1500 tokens
- Apartados si >1500 tokens
- Preservar contexto normativo

---

### 3. Sin Legal Judge Agent

**Actual:** Solo reranker juzga relevancia textual

**Propuesto:** Agente que valide:
- ¿Artículo correcto para el caso?
- ¿Porcentajes legales correctos?
- ¿Fechas y carencias correctas?

---

## 📋 PLAN DE MEJORAS (PRIORIZADO)

### FASE 1: Legal Judge Agent [4-6 horas] 🔴 CRÍTICA
- Implementar agente validador jurídico
- Usar DeepSeek Reasoner con prompt restringido
- Integrar en pipeline de generación
- **Impacto:** 9.0 → 9.5/10

### FASE 2: Sincronizar metadatos Qdrant ← PostgreSQL [2-3 horas] 🟠 ALTA
- Añadir vigencia, rango, url_html a payload Qdrant
- Permite filtrado por vigencia en búsqueda
- **Impacto:** +10% precision

### FASE 3: Chunking semántico BOE [8-12 horas] 🟡 MEDIA
- Parsear por artículos completos
- Preservar apartados como unidad
- Re-ingestar colección
- **Impacto:** +20% recall

---

## 📊 ESTADO FINAL DEL SISTEMA

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA RAG ACTUAL                       │
├─────────────────────────────────────────────────────────────┤
│ QDRANT:                                                     │
│   - Storage: 610 MB                                         │
│   - Colecciones: 3                                          │
│   - Puntos: ~98,000                                         │
│   - Vectores: ~188,000 (dense + sparse)                     │
│   - Modelo: bge-m3-spa-law-qa-trained-2 (1024D)             │
│   - HNSW: m=16, ef_construct=100                            │
│   - Chunking: 800 chars + 150 overlap                       │
├─────────────────────────────────────────────────────────────┤
│ POSTGRESQL:                                                 │
│   - laws: 48,866 chunks                                     │
│   - leyes_catalogo: 54 leyes con 51 campos de metadatos     │
│   - Incluye: vigencia, URLs, XMLs, análisis, materias       │
├─────────────────────────────────────────────────────────────┤
│ EVALUACIÓN: 8.0/10 (Muy bueno, mejorable)                   │
├─────────────────────────────────────────────────────────────┤
│ GAPS:                                                       │
│ 1. Metadatos PostgreSQL no están en Qdrant                  │
│ 2. Chunking por chars, no semántico                         │
│ 3. Sin Legal Judge Agent                                    │
└─────────────────────────────────────────────────────────────┘
```

---

*Informe CORREGIDO el 15/01/2026 - SOLO ANÁLISIS, SIN CAMBIOS EN CÓDIGO*
