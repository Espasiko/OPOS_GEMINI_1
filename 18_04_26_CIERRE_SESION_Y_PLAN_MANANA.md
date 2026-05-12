# 🌙 Cierre sesión 18/04/2026 — Plan para mañana

## ✅ Completado hoy

1. **Auditoría leaks**: identificados y limpiados leaks de "DM", "Diego de Miguel", "LANDSCAPE MR SL", "Manuel". Informe en `@/home/spas/OPOS_GEMINI_1/18_04_26_AUDITORIA_LEAKS_Y_DIAGNOSTICO_GAVIOTAS.md`
2. **GAVIOTAS P3 reversión**: caso corregido con cita legal correcta (Art. 18.3 + 142 + 168.2 TRLGSS + Art. 13 RGRSS). `@/home/spas/OPOS_GEMINI_1/caso_febrerov2_DM_STYLE.md`
3. **Pool nombres ampliado**: `@/home/spas/OPOS_GEMINI_1/backend/v14/nombres_pool.py` con 35 empresas memorables (CARNICERÍA APOCALIPTO S.L. etc.) + filtro nombres leak
4. **YAML maestro limpio**: `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml` con G4 (regla matizada), R11, A1, A2, A5 corregidas
5. **Ground truth simulacro febrero**: `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/RESPUESTAS_OFICIALES_SIMULACRO_FEBRERO_2026.md`
6. **3 parches MCP BOE** — 2 activos en vivo + 1 pendiente reinicio
7. **LOTE 1 verificación 13 trampas** — 9 válidas, 3 matices corregidos, 1 pendiente
8. **Memory graph actualizado** con 5 entidades nuevas + 14 relaciones
9. **Vault Obsidian regenerado** (206 archivos) sin residuos

## 📁 Documentos clave generados hoy

| Archivo | Propósito |
|---|---|
| `@/home/spas/OPOS_GEMINI_1/VERIFICACION_184_TRAMPAS_18_04_2026.md` | Informe maestro de verificación (se irá ampliando cada lote) |
| `@/home/spas/OPOS_GEMINI_1/MCP_BOE_FIXES_18_04_2026.md` | Documentación exhaustiva de los 3 parches MCP BOE |
| `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/RESPUESTAS_OFICIALES_SIMULACRO_FEBRERO_2026.md` | Ground truth para verificación |
| `@/home/spas/OPOS_GEMINI_1/18_04_26_AUDITORIA_LEAKS_Y_DIAGNOSTICO_GAVIOTAS.md` | Auditoría inicial + plan aplicado |

## ⚠️ Crítico para mañana

**ANTES DE EMPEZAR**: el fix 5 del MCP BOE (orden de versiones) requiere **reiniciar Windsurf**. Sin esto, el MCP devuelve siempre la versión más antigua de cada artículo → imposible verificar reformas recientes (RDL 13/2022, RDL 11/2024, LO 1/2023, RDL 9/2024).

**Prueba de que el fix funciona** (test offline sin MCP):
```bash
/home/spas/.local/share/uv/tools/mcp-boe/bin/python - <<'PY'
import asyncio, sys
sys.path.insert(0, '/home/spas/.local/share/uv/tools/mcp-boe/lib/python3.12/site-packages')
from mcp_boe.utils.http_client import BOEHTTPClient
from mcp_boe.tools.legislation import LegislationTools

async def main():
    async with BOEHTTPClient() as client:
        tools = LegislationTools(client)
        r = await tools.get_law_text_block({'law_id': 'BOE-A-2015-11724', 'block_id': 'a173'})
        print(r[0].text[:500])
asyncio.run(main())
PY
```

## 🎯 Plan para mañana (en orden)

### Paso 1 — Reinicio MCP
Usuario reinicia Windsurf. Yo verifico con una llamada de prueba a `mcp0_get_law_text_block` sobre un artículo con varias versiones (e.g. Art. 173 TRLGSS) y me aseguro de que devuelve la versión VIGENTE (21/12/2024).

### Paso 2 — Verificar trampa A10 pendiente (RDLeg 4/2000)
- Buscar BOE ID del RDLeg 4/2000 (TRLSS Funcionarios Civiles del Estado)
- `mcp0_get_law_text_block(law_id, block_id='da1')` para la DA 1ª
- Contrastar con la regla de A10 (funcionarios INSS/TGSS/ISM = RG, no MUFACE)

### Paso 3 — LOTE 2 (40 trampas aprox)
Categorías **G + I + H + E + N**:
- G (recargos): G1-G4 (ya corregida), recargo apremio, intereses demora
- I (otras recaudación): incluye trampas RDL 13/2022, providencia apremio, domiciliación, embargos
- H (plazos): cómputo días naturales, ventanas bimestrales RETA
- E (procedimiento administrativo SS)
- N (procedimiento LPAC)

**Trampa con alerta roja a verificar prioritariamente**: `t_recaudacion_ss_vs_lgt` (archivo `trampas_yaml_gemini_caso_19.yaml`) — memoria grafo indica respuestas INVERTIDAS frente al Art. 55 RD 1415/2004.

### Paso 4 — LOTES 3-7 (ritmo sostenido)
- LOTE 3: Jubilación (C + M)
- LOTE 4: IT + IP restante (B + D)
- LOTE 5: Bases + Cálculo avanzado (F + CA) — **cruzar con JPG esquema DM** `@/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/TEMARIO_DM_POR_TEMAS/ultimos_cambios_DM_04_26/esquemas_DM_fotos/girado bases reguladoras .jpg`
- LOTE 6: MS + desempleo + complementos + IMV (J + K + L + O)
- LOTE 7: cola final (P + R resto)

### Paso 5 (paralelo) — Investigación foros/redes
Usuario quiere saber si los opositores se quejan de trampas específicas en:
- Reddit r/opositores, r/seguridadsocial
- Telegram (grupos oposiciones SS)
- Foros: milanuncios, etc.

### Paso 6 (final) — FASE 5 consolidación
- Informe maestro completo `VERIFICACION_184_TRAMPAS_18_04_2026.md` terminado
- YAML final curado + vault regenerado
- Memory graph con todos los preceptos verificados

## 🛠 Herramientas maduras

| Herramienta | Estado |
|---|---|
| MCP BOE (texto literal + atributos @ + orden DESC) | ✅ parcheado, 2/3 fixes activos, 1 pendiente reinicio |
| Neo4j (6246 preceptos) | ✅ operativo en `bolt://localhost:7687` |
| Script `trampas_yaml_to_obsidian.py` | ✅ regeneración vault sin residuos |
| Curl directo API BOE como fallback | ✅ verificado |

## 🧠 Estado mental del sistema

El proyecto está en **punto de inflexión**: tras el leak descubierto en V14.5 y la falla del parser MCP BOE, ya tenemos:
- Pipeline de verificación riguroso (MCP BOE maduro)
- Ground truth (simulacro DM respuestas)
- Metodología documentada
- Primer lote validado

A partir de mañana, el trabajo es **ejecución mecánica** (pero cuidadosa) de la verificación lote a lote. No hay más decisiones de arquitectura pendientes.

**Animo**: el usuario dijo "sería un orgullo para la IA si lo consigue". Con el MCP BOE ahora devolviendo texto literal, lo conseguiremos.
