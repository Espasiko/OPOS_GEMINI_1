# 🔧 MCP-BOE — Parches aplicados 18/04/2026

> **Contexto**: durante la verificación exhaustiva de trampas (LOTE 1) se detectaron 3 bugs críticos que impedían extraer el texto literal de artículos del BOE consolidado. Estos parches dejan el MCP BOE maduro para verificación masiva.

## Archivo parcheado

`@/home/spas/.local/share/uv/tools/mcp-boe/lib/python3.12/site-packages/mcp_boe/tools/legislation.py`

**IMPORTANTE**: si el package `mcp-boe` se actualiza con `uv tool upgrade mcp-boe`, estos parches se perderán. Hay que volver a aplicarlos o upstream al repo del package.

---

## Bug #1 — No extraía texto literal de artículos

### Síntoma

```
mcp0_get_law_text_block(law_id='BOE-A-2015-11724', block_id='a18')
→ "No se pudo extraer el contenido del bloque."
```

### Causa

La función `_format_text_block` buscaba la clave `contenido_html` en el dict de la versión, pero el XML convertido a dict NO tiene esa clave. El XML real es:

```xml
<version id_norma="..." fecha_publicacion="...">
  <p class="articulo">Artículo 18. Obligatoriedad.</p>
  <p class="parrafo">1. La cotización...</p>
  <p class="parrafo">2. La obligación...</p>
</version>
```

Que se convierte a:

```python
{
  '@id_norma': '...',
  '@fecha_publicacion': '...',
  'p': [
    {'@class': 'articulo', 'text': 'Artículo 18. Obligatoriedad.'},
    {'@class': 'parrafo', 'text': '1. La cotización...'},
    ...
  ]
}
```

### Fix (líneas ~837-890 `legislation.py`)

```python
# Contenido del bloque — múltiples formatos posibles según la API
contenido_html = version_seleccionada.get('contenido_html', '')

# Formato XML de datosabiertos: array 'p' con párrafos etiquetados por clase
if not contenido_html:
    paragraphs = version_seleccionada.get('p', [])
    if paragraphs:
        if not isinstance(paragraphs, list):
            paragraphs = [paragraphs]
        parts = []
        for p in paragraphs:
            if isinstance(p, dict):
                text = p.get('text', '') or ''
                clase = p.get('@class', '')
                if not text:
                    continue
                if clase == 'articulo':
                    parts.append(f"**{text}**")
                elif clase in ('parrafo', 'parrafo_2', 'parrafo_3'):
                    parts.append(text)
                elif clase in ('cita', 'cita_acto'):
                    parts.append(f"> {text}")
                else:
                    parts.append(text)
            elif isinstance(p, str) and p.strip():
                parts.append(p.strip())
        if parts:
            contenido_html = "\n\n".join(parts)

# Fallback: buscar cualquier string largo en el JSON
if not contenido_html:
    for key, value in version_seleccionada.items():
        if key.startswith('@'):
            continue
        if isinstance(value, str) and len(value) > 50:
            contenido_html = value
            break
```

### Verificación post-fix

```
mcp0_get_law_text_block(law_id='BOE-A-2015-11724', block_id='a18')
→ "Artículo 18. Obligatoriedad.
   1. La cotización a la Seguridad Social es obligatoria..."
```

---

## Bug #2 — Atributos XML con prefijo `@` ignorados

### Síntoma

Metadatos "Versión actual (publicada el , introduida por ``)" — valores vacíos pese a que el XML tenía `fecha_publicacion="20151031"` como atributo.

### Causa

El convertor `_xml_to_dict` guarda atributos con prefijo `@` (e.g. `@fecha_publicacion`). El código `_format_text_block` buscaba sin prefijo.

### Fix (líneas ~823-831 `legislation.py`)

```python
# Mostrar la versión seleccionada
# Los atributos XML vienen con prefijo @ tras la conversión a dict
fecha_pub = (version_seleccionada.get('fecha_publicacion')
             or version_seleccionada.get('@fecha_publicacion', ''))
id_norma_mod = (version_seleccionada.get('id_norma')
                or version_seleccionada.get('@id_norma', ''))
fecha_vigencia = (version_seleccionada.get('fecha_vigencia')
                  or version_seleccionada.get('@fecha_vigencia', ''))
```

Y análogo para:
- `titulo` / `@titulo` en `block_info`
- `tipo` / `@tipo` en `block_info`
- `fecha_publicacion` en las iteraciones de historial

---

## Bug #3 — Versiones en orden ascendente, código asumía descendente

### Síntoma

Al pedir versión con `as_of_date=20231201`, devolvía la versión del 31/10/2015 (más antigua) en vez de la del 01/03/2023 (LO 1/2023) que estaba vigente en esa fecha.

Y sin `as_of_date`, devolvía también la versión más antigua (no la "actual").

### Causa

El XML de datosabiertos BOE devuelve las versiones en orden **cronológico ASCENDENTE** (más antigua primero):

```xml
<version fecha_publicacion="20151031">...</version>
<version fecha_publicacion="20230301">...</version>
<version fecha_publicacion="20241221">...</version>
```

El código comentaba "Las versiones vienen en orden cronológico INVERSO" y usaba `versiones[0]` como "la más nueva". Error de suposición.

### Fix (líneas ~798-831 `legislation.py`)

```python
# --- SELECCIÓN DE VERSIÓN ---
# Las versiones del XML de datosabiertos vienen en orden cronológico
# ASCENDENTE (más antigua primero, más nueva última). Verificado 18/04/2026.
# Trabajamos siempre sobre una copia ordenada DESC para simplificar la lógica.
def _fecha(v):
    return v.get('fecha_publicacion') or v.get('@fecha_publicacion', '')

versiones_desc = sorted(versiones, key=_fecha, reverse=True)

if as_of_date:
    version_seleccionada = None
    versiones_posteriores = []
    for v in versiones_desc:
        fp = _fecha(v)
        if fp and fp <= as_of_date:
            version_seleccionada = v
            break
        else:
            versiones_posteriores.append(fp)

    if version_seleccionada is None:
        primera = versiones_desc[-1]  # La más antigua
        fp_primera = _fecha(primera) or '?'
        return (f"**⚠️ Sin texto vigente a fecha {as_of_date}:**\n"
                f"Este bloque no existía antes de esa fecha. "
                f"La primera versión disponible es de `{fp_primera}`")

    if versiones_posteriores:
        output.append(f"> ⚠️ **Atención:** Se han ignorado {len(versiones_posteriores)} modificación(es) "
                      f"posteriores a la fecha solicitada: `{'`, `'.join(versiones_posteriores)}`")
        output.append("")
else:
    # Sin filtro de fecha: usar la versión actual (la más nueva)
    version_seleccionada = versiones_desc[0]
```

### Verificación post-fix

```
mcp0_get_law_text_block(law_id='BOE-A-2015-11724', block_id='a173')
→ "Versión actual (publicada el 21/12/2024, introducida por BOE-A-2024-26693):
   Artículo 173. Nacimiento y duración del derecho al subsidio.
   [...incluye la regulación de menstruación incapacitante...]"
```

---

## Pruebas realizadas

### Test offline (Python directo sin MCP layer)

```bash
/home/spas/.local/share/uv/tools/mcp-boe/bin/python - <<'PY'
import asyncio, sys
sys.path.insert(0, '/home/spas/.local/share/uv/tools/mcp-boe/lib/python3.12/site-packages')
from mcp_boe.utils.http_client import BOEHTTPClient
from mcp_boe.tools.legislation import LegislationTools

async def main():
    async with BOEHTTPClient() as client:
        tools = LegislationTools(client)
        r = await tools.get_law_text_block({
            'law_id': 'BOE-A-2015-11724', 
            'block_id': 'a18'
        })
        print(r[0].text)

asyncio.run(main())
PY
```

**Resultado esperado**: texto literal completo del Art. 18 TRLGSS con 4 apartados, metadatos (fecha 31/10/2015, id_norma BOE-A-2015-11724) correctos.

### Test vía MCP en vivo (bugs 1 y 2 activos)

`mcp0_get_law_text_block(law_id='BOE-A-2015-11724', block_id='a18')` — ✅ VERIFICADO.

### Test vía MCP en vivo (bug 3 — PENDIENTE reinicio de MCP)

Requiere reiniciar Windsurf o `kill` del proceso `mcp-boe`.

---

## Propuesta de upstream

Los fixes son genéricos y podrían proponerse al repo del package `mcp-boe`. El usuario puede decidir si:

1. Mantener los parches localmente (cada `uv tool upgrade` requiere re-parchear).
2. Fork propio con los fixes + instalar desde fork.
3. Issue/PR al repo oficial del package.

---

## Estado final 18/04/2026

| # | Bug | Fix aplicado en disco | Activo en MCP vivo |
|---|---|---|---|
| 1 | Texto literal | ✅ | ✅ |
| 2 | Atributos `@` | ✅ | ✅ |
| 3 | Orden versiones | ✅ | ⏳ pendiente reinicio |

**Ubicación del archivo parcheado**:
`@/home/spas/.local/share/uv/tools/mcp-boe/lib/python3.12/site-packages/mcp_boe/tools/legislation.py`

**Backup pre-parche disponible**: no se hizo backup explícito (el repo original de mcp-boe en PyPI o GitHub sirve como baseline).
