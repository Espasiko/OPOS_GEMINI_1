# 📘 CASOS Y TRAMPAS DM 2026 — Índice Maestro

> **Fuente única de verdad**: `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml`
>
> **Última actualización**: 18/04/2026 (18:57) | **Total trampas**: 184 | **Verificadas BOE**: 55 | **Con corrección aplicada**: 7 | **Obsoletas marcadas**: 1
>
> ✅ **Estado**: **0 trampas `[INVENTADA-DM]` restantes** — todas verificadas y procesadas el 18/04/2026.

---

## 🎯 Cómo usar este documento

Este documento es un **índice ejecutivo**. Las trampas completas (con regla, artículo, mnemónico) viven en el YAML. Para navegar:

1. **Buscar trampa por tema**: usa la tabla de categorías ↓
2. **Buscar por artículo legal**: `grep "Art. 233" trampas_unificadas_v2_CURADO.yaml`
3. **Ver pendientes de verificar**: sección §4 de este documento
4. **Integrar en Obsidian**: usar script `scripts/trampas_yaml_to_obsidian.py` (pendiente Y HAY MAS SCRIPTS REGENERAR VAULT. PY ETC. )

---

## 1. 🗂️ Las 22 categorías (184 trampas)

### Base principal (160 trampas — 🟢 fiables)

| Cat | Nombre | Nº | Foco temático |
|---|---|---|---|
| **A** | Encuadramiento | 10 | RGSS vs RETA vs MUFACE vs SE Hogar |
| **B** | Incapacidad Temporal | 8 | Pagadores, carencias, huelga, LO 1/2023 |
| **C** | Jubilación | 15 | Edad ordinaria, anticipada, demorada, activa, DT 7ª/34ª |
| **D** | Incapacidad Permanente | 4 | IPP vs IPT, BR, revisión grado |
| **E** | Procedimiento administrativo | 8 | Alzada, silencio, vía social, URE |
| **F** | Bases de cotización y recargos | 12 | Prorrata, HE, suplidos, base solidaridad |
| **G** | Recargos | 4 | 10/20/35%, intereses vs recargo |
| **H** | Plazos SS | 8 | Días naturales vs hábiles, alta previa |
| **I** | Otras (recaudación, pluriactividad) | 19 | Subastas, embargo, IGSS, automaticidad |
| **J** | Muerte y supervivencia | 14 | Viudedad 52/60/70%, orfandad, pareja hecho |
| **K** | Desempleo | 6 | BR, duración máxima, excedencia voluntaria |
| **L** | Complementos / No contributivas | 4 | Mínimos, PNC, brecha género |
| **M** | Jubilación parcial y relevo | 4 | Relevista 65%, fijos discontinuos ×1,5 |
| **N** | Procedimiento LPAC | 7 | Nulidad/anulabilidad, revisión oficio |
| **O** | Ingreso Mínimo Vital | 5 | Renta año anterior, administrador SL |
| **P** | Tiempo parcial y fijos discontinuos | 4 | Horas complementarias, SE Hogar <60h |
| **Q** | Función pública AGE | 11 | Trienios, exámenes, IT, servicios especiales |
| **R** | RETA y sistemas especiales | 16 | No IPP, IPT cualificada +20%, grupos Mar |
| **CA** | Cálculo avanzado | 6 | GI complemento, recargo AT/EP, subsidio +52 |
| **N₂** | Automaticidad (solo 1 trampa) | 1 | Empresario no cotiza → INSS anticipa |

### Ampliación v2 curada (25 trampas — mezcla de estados)

| Cat_+ | Origen | Nº | Estado |
|---|---|---|---|
| A+ (A11-A15) | INVESTIGACION | 5 | 🟡 Extraída de exámenes reales |
| B+ (B9) | INVESTIGACION | 1 | 🟡 |
| D+ (D5-D7) | INVESTIGACION | 3 | 🟡 |
| F+ (F13-F14) | INVESTIGACION | 2 | 🟡 |
| G+ (G5-G7) | INVESTIGACION + GROK | 3 | 🟡 |
| J+ (J15-J18) | INVESTIGACION + gemini_c19 | 4 | 🟡 |
| K+ (K7) | INVESTIGACION | 1 | 🟡 |
| Q+ (Q12) | INVESTIGACION | 1 | 🟡 |
| R+ (R11-R12) | **gemini_c19** (cooperativas) + INV | 2 | ⚠️ R11 corregida — ver §3 |
| CA+ (CA7-CA8) | GROK (pluriempleo/pluriactividad) | 2 | 🟡 |

---

## 2. 🏷️ Leyenda de orígenes (tras verificación 18/04/2026)

La etiqueta `origen:` en el YAML indica la fiabilidad de cada trampa:

| Tag | Significado | Nº | ¿Usar tal cual? |
|---|---|---|---|
| `[BOE-DIRECTO]` | Verificada contra texto BOE literal (04/03/2026) | 23 | ✅ Sí |
| **`[VERIFICADA-POST-FUSION-2026-04]`** | **Verificada con BOE + Iberley + doctrina el 18/04/2026 (estaban etiquetadas [INVENTADA-DM])** | **20** | ✅ **Sí** |
| `[LEG-CONSOLIDADA]` | Verificada contra legislación consolidada BOE | 11 | ✅ Sí |
| `[WEB]` | Doctrina, Iberley, foros, STS citadas | 17 | 🟡 Verificar artículo |
| `[INVESTIGACION]` | Extraída con referencia de línea del doc `INVESTIGACION_MATERIALES_ACADEMIAS` (exámenes AGE 2011-2023) | 19 | 🟡 Fiable — revisar 1-1 |
| **`[VERIFICADA-CON-CORRECCION-2026-04]`** | **Verificada pero con ajuste de artículo/matiz el 18/04/2026** | **7** | 🟡 **Sí, con `correccion:` anotada** |
| `[VERIFICADA-BOE-2026-04-18]` | R11 cooperativas, reformulada completamente tras hallazgo GAVIOTAS | 1 | ✅ Sí |
| `[DM-SIMULACRO]` | Confirmada con respuesta oficial en simulacro DM | 3 | ✅ Sí |
| `[gemini_c19]`, `[GROK]`, `[NUEVA]`, `[CORREGIDA]` | Orígenes específicos | 14 | ⚠️ Ver detalle en YAML |
| **`[OBSOLETA-RDL-2-2023-COEFICIENTE-PARCIALIDAD-DEROGADO]`** | **P4 — derogada por RDL 2/2023 (01/10/2023)** | **1** | 🔴 **NO USAR** — decisión pendiente |

> 🎉 **0 trampas `[INVENTADA-DM]` pendientes** tras la verificación del 18/04/2026.

---

## 3. ✅ HALLAZGO CASO GAVIOTAS — CORREGIDO (18/04/2026)

**Archivo**: `@/home/spas/OPOS_GEMINI_1/caso_febrerov2_DM_STYLE.md:1-189`
**Estado**: Simulacro **local** (no existe URL externa). Generado por V14.5 + Claude.

### 3.1 Errores detectados originalmente

1. **Error de cita**: P2 y P3 citaban `Art. 104 TRLGSS` → **INCORRECTO** (Art. 104 regula IP parcial, no cooperativas).
2. **Contradicción interna**: P2 decía "solidaria" pero P3 tenía respuesta D = alcance de la SUBSIDIARIA (principal + recargos + intereses + costas).

### 3.2 Correcciones aplicadas (18/04/2026)

En `@/home/spas/OPOS_GEMINI_1/caso_febrerov2_DM_STYLE.md`:

| Elemento | Antes | Ahora |
|---|---|---|
| P2 cita legal | `Art. 104 TRLGSS` | `Art. 335 TRLGSS + DA 4ª TRLGSS + Art. 72 Ley 27/1999` ✅ |
| P3 cita legal | `Art. 104 TRLGSS` | `Art. 15.3 TRLGSS` (alcance solidaria) ✅ |
| P3 respuesta correcta | **D** (principal + recargos + intereses + costas) | **B** (principal + recargo, coherente con la solidaria) ✅ |

Fuentes consultadas: **FEVECTA** (blog cooperativas); **vLex** ("responsable solidario"); **Iberley** (Art. 72 LCoop); **BOE** (texto TRLGSS consolidado 04/02/2026).

### 3.3 Trampa R11 del YAML también corregida

Antes:
```yaml
articulo: "Art. 80.4 Ley 27/1999; Art. 15 bis TRLGSS (alcance)"
origen: "[gemini_c19 — t_cooperativa_reta_solidaria]"
```

Ahora:
```yaml
articulo: "Art. 335 TRLGSS; DA 4ª TRLGSS; Art. 72 Ley 27/1999; Art. 15.3 TRLGSS (alcance)"
origen: "[VERIFICADA-BOE-2026-04-18 — gemini_c19 reformulada]"
```

Incluye `correccion:` anotando la trazabilidad del cambio.

---

## 4. ✅ Verificación completada (18/04/2026) — las 28 trampas `[INVENTADA-DM]` procesadas

**Documento detallado**: `@/home/spas/OPOS_GEMINI_1/VERIFICACION_28_INVENTADAS.md`
**Script trazable**: `@/home/spas/OPOS_GEMINI_1/backend/scripts/aplicar_verificacion_28.py`
**Backup previo**: `trampas_unificadas_v2_CURADO.yaml.bak-antes-verificacion-28`

### 4.1 Resumen del veredicto

| Estado | Nº | % | Acción aplicada |
|---|---|---|---|
| ✅ **VERIFICADAS tal cual** | 20 | 71% | Tag `[VERIFICADA-POST-FUSION-2026-04]` |
| ⚠️ **CON CORRECCIÓN aplicada** | 7 | 25% | Tag `[VERIFICADA-CON-CORRECCION-2026-04]` + campo `correccion:` |
| ❌ **OBSOLETA** (P4 por RDL 2/2023) | 1 | 4% | Tag `[OBSOLETA-RDL-2-2023-COEFICIENTE-PARCIALIDAD-DEROGADO]` |

### 4.2 Las 20 ✅ VERIFICADAS (mantener)

C14, J2, J3, J5, J6, K1, K3, K4, K5, L1, L2, L3, N5, N6, P1, Q1, Q4, CA1, CA2, CA4

### 4.3 Las 7 ⚠️ REFORMULADAS (con ajuste puntual)

| ID | Ajuste | Motivo |
|---|---|---|
| **J4** | `articulo:` actualizado a `Art. 219, Art. 221 bis TRLGSS; RD 900/2018; DF 27ª Ley 40/2007` | Art. 231 no regula 60%/70% (regula "impedimento beneficiario") |
| **N7** | `regla:` cambia "10 días hábiles" → "10 días NATURALES" | Art. 43.2 LPAC literal |
| **Q2** | Añadido `actualizacion_2026:` | RDL 9/2025 amplió el permiso de nacimiento (Directiva UE 2019/1158) |
| **Q3** | `articulo:` actualizado a `Art. 22 y 23.2 EBEP; LPGE anual` | Detalle operativo está en Art. 23.2 |
| **CA5** | `articulo:` actualizado a `Art. 315 TRLGSS; RD 1273/2003; Orden TAS/1040/2005` | Art. 308 solo enumera; devengo específico en desarrollo reglamentario |
| **CA6** | `articulo:` actualizado a `Art. 280.4 TRLGSS; Art. 274 TRLGSS` | Art. 274.4 no existía; regulación en Art. 280 |
| **K6** | Añadido `actualizacion_2024:` | RDL 2/2024 modificó Art. 282 — verificar |

### 4.4 La 1 ❌ OBSOLETA (decisión pendiente)

**P4** — "Coeficiente global de parcialidad: solo carencia, no BR (Art. 247.1 TRLGSS)"

**Problema**: desde el **01/10/2023** el **RDL 2/2023** DEROGÓ el coeficiente de parcialidad. Ahora cada día de alta a TP computa como 1 día cotizado completo.

**Opciones**:
- **A**: Borrar la trampa (regla ya no aplica).
- **B**: Reescribirla como "trampa inversa" — para capturar al opositor que siga usando el coeficiente viejo.

Actualmente el YAML la tiene marcada como `[OBSOLETA-RDL-2-2023-COEFICIENTE-PARCIALIDAD-DEROGADO]` con un campo `correccion_critica:` esperando decisión.

### 4.5 Hallazgos metodológicos

- **Claude 4.5 acertó al 71%** inventando trampas con base legal real.
- **Errores más frecuentes**: cita de artículo específico (4 casos) y obsolescencia por reformas 2023-2025 (3 casos).
- **0 trampas fueron "invención pura sin base legal"** — todas tenían fundamento, solo necesitaban precisión.

---

## 5. 📐 Arquitectura recomendada (pendiente de ejecutar)

```
/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/
    ├── trampas_unificadas_v2_CURADO.yaml   🔒 FUENTE ÚNICA (única que se edita)
    └── README_TRAMPAS.md                    📘 Manual de uso

/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/trampas/   (via Syncthing a Windows)
    ├── _INDICE.md                           📋 184 trampas con [[wiki-links]]
    ├── A_encuadramiento.md                  📂 Índice categoría (15 trampas)
    ├── B_IT.md                              📂 Índice categoría (9 trampas)
    ├── [... 18 índices más ...]
    ├── A01_funcionarios_AGE_MUFACE.md       📝 1 nota Obsidian por trampa
    │                                            con frontmatter COSMIC
    ├── A02_capital_25pct_sin_cargo.md
    ├── [... 184 notas trampa ...]
    └── PENDIENTES_VERIFICAR.md              ⚠️ Dashboard de las 28 inventadas

/home/spas/OPOS_GEMINI_1/
    └── CASOS_TRAMPAS_DM_2026.md             📊 Este documento (índice ejecutivo)
```

### Ventajas de este modelo
1. **Un solo archivo que se edita** (el YAML). Evita deriva entre versiones.
2. **Obsidian aprovecha al máximo** sus features: backlinks, graph, búsqueda full-text, tags.
3. **Granularidad**: puedes abrir 1 trampa sin cargar las 184.
4. **Diff git limpio** cuando añadas/corrijas trampas.
5. **Regeneración barata**: script Python de ~80 líneas `yaml → md`.

### Script de generación — borrador del flujo
```python
# backend/scripts/trampas_yaml_to_obsidian.py
# Uso: python3 scripts/trampas_yaml_to_obsidian.py
#
# Lee:  trampas_unificadas_v2_CURADO.yaml
# Crea: /mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/trampas/
#       - _INDICE.md (184 links)
#       - A_encuadramiento.md ... R_RETA.md (22 índices categoría)
#       - A01_xxx.md ... CA08_xxx.md (184 notas trampa)
#       - PENDIENTES_VERIFICAR.md (dashboard)
# Frontmatter COSMIC por nota:
#   tags: [trampa, categoria_A, verificado_boe]
#   articulos: [Art. 136 TRLGSS]
#   origen: "[BOE-DIRECTO]"
#   peso_examen: alto
```

---

## 6. 🗺️ Estado actual y próximos pasos

### ✅ Completado (18/04/2026 INFO YA OBSOLETA, SE HIZO LA VERIFICACION COMPLETA!!!)

- [x] **C**: Verificadas las 28 `[INVENTADA-DM]` (20 OK, 7 reformuladas, 1 obsoleta)
- [x] **B**: Corregido caso GAVIOTAS (P2-P3) + trampa R11 del YAML
- [x] **A**: Generadas 206 archivos Obsidian en `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/trampas/`
  - 1 `_INDICE.md` maestro (con wiki-links a las 20 categorías)
  - 1 `_PENDIENTES_VERIFICAR.md` dashboard (🎉 0 pendientes, 1 obsoleta)
  - 20 índices por categoría (`_A_encuadramiento.md`, `_B_it.md`, ...)
  - 184 notas individuales con frontmatter COSMIC + secciones estructuradas
- [x] **Índice maestro**: este documento actualizado al estado real

### ⏳ Pendientes

| Opción | Acción | Tiempo | Prioridad |
|---|---|---|---|
| **D** | Borrar `catalogo_trampas.yaml` y `catalogo_trampas_adicional.yaml` (ya fusionados) | 1 min | 🟡 Media — usuario prefiere esperar |
| **E** | Decidir qué hacer con P4 (borrar o reescribir como trampa inversa) | 2 min | 🟡 Media |
| **H** | Mejorar script Obsidian: clasificar auto trampas sin `origen:` como "[DM-MAESTRO]" | 10 min | 🟡 Media |
| **F** | Auditar las 14 trampas `[gemini_c19/GROK/NUEVA/CORREGIDA]` restantes | 30 min | 🟢 Baja |
| **G** | Auditar las 17 `[WEB]` (verificar que los artículos citados son correctos) | 45 min | 🟢 Baja |
| **I** | Sincronizar el vault via Syncthing al Windows del usuario | 5 min (configuración ya hecha) | 🟢 Baja |

---

## 7. 🎯 Archivos clave de este bloque de trabajo

| Archivo | Rol | Estado |
|---|---|---|
| `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml` | 🔒 Fuente única (184 trampas YA VERIFICADAS CONTRA EL BOE POR CLAUDE 4.7) | ✅ |
| `@/home/spas/OPOS_GEMINI_1/CASOS_TRAMPAS_DM_2026.md` | 📊 Este índice ejecutivo | ✅ |
| `@/home/spas/OPOS_GEMINI_1/VERIFICACION_28_INVENTADAS.md` | 🔍 Veredicto de las 28 verificadas | ✅ |
| `@/home/spas/OPOS_GEMINI_1/backend/scripts/aplicar_verificacion_28.py` | 🐍 Script que aplicó cambios al YAML | ✅ |
| `@/home/spas/OPOS_GEMINI_1/backend/scripts/trampas_yaml_to_obsidian.py` | 🐍 Script `yaml → md` (reutilizable) | ✅ |
| `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/trampas/` | 🌐 Vault Obsidian poblado (206 archivos) | ✅ |
| `@/home/spas/OPOS_GEMINI_1/caso_febrerov2_DM_STYLE.md` | 📝 Caso GAVIOTAS corregido | ✅ |

---

*Documento actualizado el 18/04/2026 (19:05) tras completar tareas C (verificación 28), B (corrección GAVIOTAS + R11) y A (generación 206 archivos Obsidian). Estado: **trampas curadas, verificadas y publicadas en vault**.*
