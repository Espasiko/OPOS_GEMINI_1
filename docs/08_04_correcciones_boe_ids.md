# Correcciones BOE-IDs - Verificación Manual

## RESUMEN DE CORRECCIONES ENCONTRADAS

### Grupo CRÍTICO (2 leyes)

| # | BOE-ID Catálogo | Ley | BOE-ID CORRECTO | Estado |
|---|-----------------|-----|-----------------|--------|
| 1 | BOE-A-2025-8567 | Ley 2/2025 (incapacidad permanente) | **BOE-A-2025-8567** | ✅ CORRECTO |
| 2 | BOE-A-2022-10656 | RD 504/2022 (afiliación autónomos) | **BOE-A-2022-10677** | ❌ ERRÓNEO |

**Verificación BOE-A-2022-10656:**
- ID 10656 = Resolución convenio Ministerio Cultura/Badajoz (BASURA)
- ID 10677 = RD 504/2022 REAL sobre afiliación autónomos ✅

---

### Grupo IMPORTANTE (5 leyes)

| # | BOE-ID Catálogo | Ley | BOE-ID CORRECTO | Estado |
|---|-----------------|-----|-----------------|--------|
| 3 | BOE-A-2013-11881 | RD 1196/2013 (convenios especiales) | **PENDIENTE** | ⚠️ VERIFICAR |
| 4 | BOE-A-2009-20412 | RD 1851/2009 (jubilación discapacidad) | **BOE-A-2009-20652** | ❌ ERRÓNEO |
| 5 | BOE-A-2003-21147 | Orden TAS/2865/2003 (sistema RED) | **BOE-A-2003-19281** | ❌ ERRÓNEO |
| 6 | BOE-A-2007-8419 | RD 504/2007 (baremo dependencia) | **BOE-A-2007-8350** | ❌ ERRÓNEO |
| 7 | BOE-A-2019-4676 | RDL 8/2019 (protección social) | **BOE-A-2019-3481** | ❌ ERRÓNEO |

**Verificaciones detalladas:**

**BOE-A-2009-20412:**
- 20412 = Anuncio adjudicación contrato SAS Andalucía (BASURA)
- 20652 = RD 1851/2009 REAL sobre jubilación anticipada discapacidad ✅

**BOE-A-2003-21147:**
- 21147 = RD 1679/2007 Gran Cruz póstuma (BASURA)
- 19281 = Orden TAS/2865/2003 REAL sobre convenio especial ✅

**BOE-A-2007-8419:**
- 8419 = Anuncios contratos suministro (BASURA)
- 8350 = RD 504/2007 REAL sobre baremo dependencia ✅

**BOE-A-2019-4676:**
- 4676 = RD 217/2019 subvención Canarias desalación (BASURA)
- 3481 = RDL 8/2019 REAL protección social/precariedad ✅

---

### Grupo HISTÓRICO (14 leyes)

| # | BOE-ID Catálogo | Ley | Estado |
|---|-----------------|-----|--------|
| 8 | BOE-A-1963-22667 | Ley 193/1963 (Bases SS) | ⚠️ PENDIENTE |
| 9 | BOE-A-1972-907 | Ley 24/1972 | ⚠️ PENDIENTE |
| 10 | BOE-A-1985-16119 | Ley 26/1985 | ⚠️ PENDIENTE |
| 11 | BOE-A-1960-12344 | Ley 45/1960 | ⚠️ PENDIENTE |
| 12 | BOE-A-1969-123 | Ley 45/1969 | ⚠️ PENDIENTE |
| 14 | BOE-A-1966-10707 | Decreto 907/1966 | ⚠️ PENDIENTE |
| 15 | BOE-A-1983-15758 | RD 1451/1983 | ⚠️ PENDIENTE |
| 16 | BOE-A-1990-29784 | RD 1576/1990 | ⚠️ PENDIENTE |
| 17 | BOE-A-2010-12628 | Ley 32/2010 CATA | ⚠️ PENDIENTE |
| 18 | BOE-A-1973-51 | Decreto 3772/1972 | ⚠️ PENDIENTE |
| 19 | BOE-A-2008-1067 | RD 8/2008 | ⚠️ PENDIENTE |
| 20 | BOE-A-1985-18544 | RD 625/1985 | ⚠️ PENDIENTE |
| 21 | BOE-A-1969-8263 | Orden IT 1969 | ⚠️ PENDIENTE |

---

## ACCIÓN REQUERIDA

**De las 7 leyes CRÍTICO+IMPORTANTE:**
- ✅ 1 correcto
- ❌ 5 con IDs erróneos (basura en lugar de leyes SS)
- ⚠️ 1 pendiente de verificación (RD 1196/2013)

**Las leyes históricas/específicas** necesitan verificación individual.

## CÓDIGOS DE BASURA ENCONTRADOS

Los siguientes IDs del catálogo son documentos administrativos NO relacionados con Seguridad Social:

- BOE-A-2022-10656 → Convenio cultura (no es RD 504/2022)
- BOE-A-2009-20412 → Anuncio licitación SAS (no es RD 1851/2009)
- BOE-A-2003-21147 → Gran Cruz póstuma (no es Orden TAS/2865/2003)
- BOE-A-2007-8419 → Anuncio contrato (no es RD 504/2007)
- BOE-A-2019-4676 → Subvención Canarias (no es RDL 8/2019)

---

## IDs CORRECTOS CONFIRMADOS

```json
{
  "correcciones": [
    {"boe_id_incorrecto": "BOE-A-2022-10656", "boe_id_correcto": "BOE-A-2022-10677", "ley": "RD 504/2022"},
    {"boe_id_incorrecto": "BOE-A-2009-20412", "boe_id_correcto": "BOE-A-2009-20652", "ley": "RD 1851/2009"},
    {"boe_id_incorrecto": "BOE-A-2003-21147", "boe_id_correcto": "BOE-A-2003-19281", "ley": "Orden TAS/2865/2003"},
    {"boe_id_incorrecto": "BOE-A-2007-8419", "boe_id_correcto": "BOE-A-2007-8350", "ley": "RD 504/2007"},
    {"boe_id_incorrecto": "BOE-A-2019-4676", "boe_id_correcto": "BOE-A-2019-3481", "ley": "RDL 8/2019"}
  ]
}
```
