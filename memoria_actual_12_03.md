# MEMORIA DEL PROYECTO OPOSITAIA — 12/03/2026
*Documento generado y verificado directamente desde el código real a las 20:10 (hora Madrid)*

---

## 1. ESTADO DOCKER — TODOS LOS SERVICIOS

| Contenedor | Imagen | Puerto | Estado | Notas |
|---|---|---|---|---|
| `opositaia-qdrant` | `qdrant/qdrant:v1.12.0` | 6333/6334 | ✅ Up | Volumen: `opos_gemini_1_qdrant_storage` |
| `opositaia-postgres` | `postgres:15-alpine` | 5432 | ✅ Up (healthy) | DB: opositaia / user: postgres |
| `opositaia-neo4j` | `neo4j:5-community` | 7474/7687 | ✅ Up (healthy) | **HOY REPARADO**: healthcheck añadió credenciales `-u neo4j -p opositaia2026` |
| `opositaia-postgres` (sweet_chatelet) | — | — | ✅ Up | Contenedor Antigravity propio |

**IMPORTANTE**: Contenedor `qdrant` (vacío, sin datos) creado accidentalmente hoy → **ELIMINADO**.
El original siempre fue `opositaia-qdrant` (desde `docker-compose.yml`).

---

## 2. QDRANT LOCAL — COLECCIONES Y DATOS

| Colección | Puntos | Uso |
|---|---|---|
| `opositaia_knowledge_FULL_XML` | **25.273** | RAG principal — Leyes con metadata XML BOE |
| `opositaia_knowledge_hybrid` | 48.866 | RAG híbrido (anterior, kept como backup) |
| `opositaia_leyes_master` | 54 | Índice de leyes |
| `opositaia_memory_mcp` | 3 | Memoria del MCP server local |

**⚠️ Pendiente**: El `INVENTARIO_QDRANT_RAW.md` dice 24.697 puntos — desactualizado. Hoy hay 25.273.

---

## 3. FASTAPI BACKEND — ESTADO Y CONFIG

- **Proceso**: `uvicorn main:app --host 0.0.0.0 --port 8000` (PID 508987, sin contenedor, en venv local)
- **Embedding model**: `pablosi/bge-m3-spa-law-qa-trained-2` (local, 1024 dims)
- **HOY CORREGIDO** en `.env.backend`:
  - ANTES: `QDRANT_URL=https://b554ceb5-...gcp.cloud.qdrant.io` ← CLOUD (mal en dev)
  - AHORA: `QDRANT_URL=http://localhost:6333  # DESARROLLO (Docker local)` ✅

---

## 4. MCP SERVERS

| Servidor | Tipo | Estado | Función |
|---|---|---|---|
| `/home/spas/OPOS_GEMINI_1/mcp-server` | TypeScript (Node.js) | ✅ Nuestro MCP de la app | RAG search_rag, verify_boe, ingest_new_law, list_collections, search_jurisprudence |
| `github-mcp-server` (Docker) | Go binary | ✅ Activo (Antigravity IDE) | GitHub API para el IDE |
| `mcp-remote` Kaggle | Node.js | ✅ Activo (Antigravity IDE) | Kaggle API para el IDE |

**ACLARACIÓN**: El MCP de GitHub y Kaggle son para el IDE Antigravity, **NO para la app OpositAIA**.
El MCP de la app es exclusivamente `/home/spas/OPOS_GEMINI_1/mcp-server/src/index.ts`.

**Herramientas del MCP propio** (verificadas en `src/index.ts`):
- `search_rag` — Búsqueda semántica en Qdrant (modelo pablosi vía HuggingFace o Mistral fallback)
- `verify_boe` — Verifica vigencia de ley en BOE.es
- `list_collections` — Lista colecciones Qdrant
- `search_jurisprudence` — Búsqueda sentencias
- `get_law_summary` — Resumen de ley
- `ingest_new_law` — Ingesta nueva ley vía BOE ID

---

## 5. CALCULADORAS — ESTADO REAL (calculos_ss_extended.py)

**Archivo**: `backend/calculators/calculos_ss_extended.py` — **1982 líneas, sintaxis OK** ✅

### CORRECCIONES APLICADAS HOY (Ejercicio 19 Diego de Miguel)

#### ⚠️ Error crítico corregido: Taxonomía HE
```python
# ANTES (MAL — confundía estructurales con fuerza mayor):
# HE estructurales al 14% -- ERROR SISTEMÁTICO

# AHORA (CORRECTO — dict TIPOS_HE verificado en código):
TIPOS_HE = {
    "fuerza_mayor":      (0.12,   0.02,   0.14),   # Solo prevenir/reparar siniestros urgentes
    "estructurales":     (0.2360, 0.0470, 0.2830), # Habituales producción → 28,30%
    "no_estructurales":  (0.2360, 0.0470, 0.2830), # Esporádicas → 28,30%
}
```

#### ⚠️ Escala Jubilación Activa actualizada a RDL 11/2024 (vigente 01/04/2025)
```python
# ANTES (MAL — escala derogada):
# calcular_jubilacion_demorada() con 4% por año → INCORRECTO

# AHORA (CORRECTO — nueva función):
ESCALA_JUBILACION_ACTIVA_RDL11_2024 = {
    1: Decimal("0.45"),   # 1 año → 45%
    2: Decimal("0.55"),   # 2 años → 55%
    3: Decimal("0.65"),   # 3 años → 65%
    4: Decimal("0.80"),   # 4 años → 80% ← Caso Candela P15 (acertada)
    5: Decimal("1.00"),   # ≥5 años → 100%
}
```

### CALCULADORAS COMPLETAS (13 total, verificadas en código):

| # | Función | Estado |
|---|---|---|
| 1 | `calcular_recargo_ss()` | ✅ Lógica 10%/35%/20% corregida |
| 2 | `calcular_intereses_demora_ss()` | ✅ Principal (día 1) vs Recargo (día 16) |
| 3 | `calcular_it_situaciones_especiales_lo1_2023()` | ✅ LO 1/2023 carencias correctas |
| 4 | `calcular_base_cotizacion_completa()` | ✅ TIPOS_HE dict corregido |
| 5 | `calcular_integracion_lagunas_jubilacion()` | ✅ RETA=0, DA 37ª mujer |
| 6 | `calcular_br_jubilacion_dt34()` | ✅ 302 mejores / 352,33 (DT 34ª) |
| 7 | `calcular_fecha_efectos_cambio_base_reta()` | ✅ 1 del mes siguiente (RDL 13/2022) |
| 8 | `calcular_tipo_enajenacion()` | ✅ Solo cargas anteriores al embargo |
| 9 | `calcular_jubilacion_activa_escala_rdl11_2024()` | ✅ **NUEVA ESCALA** RDL 11/2024 |
| 10 | `calcular_derivacion_responsabilidad_ss()` | ✅ Solidaria: principal+recargo sin costas |
| 11 | `calcular_cuota_contrato_corta_duracion()` | ✅ 32,60€ fijo (≤8 días) |
| 12 | `calcular_pension_maxima_anticipada_involuntaria()` | 🆕 **NUEVA** Art.207.2 — 0,5%/trim sobre TOPE |
| 13 | `calcular_retribucion_especie_vehiculo()` | 🆕 **NUEVA** 20%/12 si uso particular (DEFAULT incluir) |

### Otros archivos de calculadoras en `/backend/calculators/`:
- `calculos_ss.py` — IT, cotizaciones base
- `calculos_imv.py` — Ingreso Mínimo Vital
- `calculadora_age.py` — Función Pública AGE (nóminas, dietas, LCSP)
- `calculadora_presupuesto.py` — Presupuesto, créditos, modificaciones
- `dispatcher.py` — Router central que llama a todas las calculadoras

---

## 6. CATÁLOGO DE TRAMPAS — ESTADO

| Documento | Ubicación | Estado |
|---|---|---|
| `CASOS_TRAMPAS_DM_2026.md` | Raíz | Versión anterior (pre ejercicio 19), sin C12, F7, F8 nuevas |
| `12_03_catalogo_trampasYAML.dm_CLAUDE` | `academias/1_casos_recientes_2026_DM/` | ✅ MÁS ACTUALIZADO — 65 trampas A-I con correcciones del Ejercicio 19 |
| `conversacion_12_03_yamlcaso19.md` | `academias/1_casos_recientes_2026_DM/` | ✅ Análisis completo Ejercicio 19 (P1-P15, errores Gemini+DeepSeek) |

**Correcciones del Ejercicio 19 al catálogo** (verificadas en código hoy):
- **C10**: Art. 50 ET SÍ da derecho a jubilación anticipada involuntaria. Lo que NO: despido disciplinario (aunque improcedente)
- **C12 NUEVA**: Pensión > tope máximo → 0,5%/trim sobre el TOPE, no sobre la pensión calculada
- **F7 NUEVA**: Si enunciado no dice "fuerza mayor" → HE ordinarias → 28,30% (4,70% trabajador)
- **F8 NUEVA**: Vehículo empresa + uso particular → INCLUIR en BC. DEFAULT siempre incluir
- **G1 PRECISADA**: 10% = dentro del plazo voluntario reclamación; 35% = DESPUÉS de que venza ese plazo; 20% = providencia de apremio
- **H4 NUEVA** (en YAML): TGSS tiene 48h para notificar incidencia en SLD (Sistema de Liquidación Directa)
- **I12 CONFIRMADA**: ETT + servicio doméstico → Régimen General (no Sistema Especial Hogar)

---

## 7. NEO4J — ESTADO Y CORRECCIÓN

- **Credenciales**: `neo4j` / `opositaia2026`
- **URL**: `bolt://localhost:7687` | Browser: `http://localhost:7474`
- **HOY REPARADO**: healthcheck en `docker-compose.yml` corregido:
  ```yaml
  # ANTES (MAL — sin credenciales → siempre unhealthy):
  test: ["CMD", "cypher-shell", "RETURN 1"]
  
  # AHORA (CORRECTO):
  test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "opositaia2026", "RETURN 1"]
  ```
- Después de `docker-compose up -d neo4j` → estado actual: **✅ healthy**

---

## 8. ARQUITECTURA ACTUALIZADA (resumen `arquitectura_final_plataforma_oposiciones.md`)

- **Principio de trazabilidad** actualizado: "Todo contenido trazable al BOE y verificado con filtrado de fechas. SS: fecha 04/03/2026. AGE: fecha convocatoria."

---

## 9. PENDIENTES INMEDIATOS (sin tocar hoy)

1. **Re-ingestar las leyes con metadatos completos** — Script `backend/scripts/update_qdrant_metadatos_boe.py` creado pero pendiente de ejecutar
2. **Catálogo de trampas en YAML integrado en el generador** — El `12_03_catalogo_trampasYAML` debe cargarse en Fase 0 del prompt de `run_ecosistema_mistral_v12.py`
4. **RDL 11/2024 BR de IT** — Pendiente verificar si el cambio de 3 meses aplica a jornada parcial o a todos los trabajadores (sospecha: solo parcial)
5. **BMAD actualización** — `pnpm dlx bmad-method@next install` para pasar a Beta.7

---

## 10. ARTEFACTOS ANTIGRAVITY VIGENTES

| Artefacto | Estado |
|---|---|
| `PLAN_ACCION_DEFINITIVO_10_03_2026.md` | ✅ El más actualizado — referencia principal |
| `task.md` | ⚠️ Desactualizado con el estado de hoy |
| `walkthrough.md` | ❌ Muy desactualizado (habla de R1 v10) |
| `AUDITORIA_CALCULADORAS_2026.md` | 🗑️ **BORRADO HOY** (era viejo) |
| `AUDITORIA_IMPLEMENTADO_VS_DISEÑO.md` | ⚠️ Pendiente actualizar con hoy |

---

*Generado automáticamente desde código real — 12/03/2026 20:10 (CET)*
