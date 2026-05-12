#!/usr/bin/env python3
"""
Genera notas Obsidian desde el YAML maestro de trampas.

Crea en `/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/trampas/`:
  - `_INDICE.md`                     : índice maestro con las 184 trampas (wiki-links)
  - `_PENDIENTES_VERIFICAR.md`       : dashboard de trampas con estado de verificación
  - `{CATEGORIA}_{nombre}.md`        : 22 índices por categoría
  - `{CATEGORIA}/{ID}_{slug}.md`     : 184 notas individuales con frontmatter COSMIC

Frontmatter COSMIC por nota:
  - id, titulo, categoria, articulos, origen, tags, peso_examen, verificado_boe

Uso: python3 trampas_yaml_to_obsidian.py [--dry-run] [--vault-path PATH]

Autor: Cascade | 2026-04-18
"""
from __future__ import annotations
import argparse
import re
import sys
import unicodedata
from pathlib import Path

import yaml

YAML_PATH = Path("/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml")
DEFAULT_VAULT = Path("/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/trampas")

# Secciones del YAML que contienen trampas reales (no metadata)
SECCIONES_TRAMPAS = {
    "categoria_A_encuadramiento": ("A", "Encuadramiento (RGSS / RETA / MUFACE / SE Hogar)"),
    "categoria_B_IT": ("B", "Incapacidad Temporal"),
    "categoria_C_jubilacion": ("C", "Jubilación"),
    "categoria_D_IP": ("D", "Incapacidad Permanente"),
    "categoria_E_procedimiento": ("E", "Procedimiento administrativo"),
    "categoria_F_bases_cotizacion": ("F", "Bases de cotización"),
    "categoria_G_recargos": ("G", "Recargos"),
    "categoria_H_plazos": ("H", "Plazos SS"),
    "categoria_I_otras": ("I", "Otras (recaudación, pluriactividad)"),
    "categoria_N_automaticidad": ("N_AUTO", "Automaticidad y responsabilidad"),
    "categoria_J_muerte_supervivencia": ("J", "Muerte y supervivencia"),
    "categoria_K_desempleo": ("K", "Desempleo"),
    "categoria_L_complementos_no_contributivas": ("L", "Complementos / No contributivas"),
    "categoria_M_jubilacion_parcial_relevo": ("M", "Jubilación parcial y relevo"),
    "categoria_N_procedimiento_LPAC": ("N", "Procedimiento LPAC"),
    "categoria_O_IMV": ("O", "Ingreso Mínimo Vital"),
    "categoria_P_tiempo_parcial_fijos_discontinuos": ("P", "Tiempo parcial y fijos discontinuos"),
    "categoria_Q_funcion_publica_AGE": ("Q", "Función pública AGE"),
    "trampas_calculo_avanzado": ("CA", "Cálculo avanzado"),
    "categoria_R_RETA_sistemas_especiales": ("R", "RETA y sistemas especiales"),
    "categoria_A_encuadramiento_ampliacion": ("A", "Encuadramiento — ampliación v2"),
    "categoria_B_IT_ampliacion": ("B", "IT — ampliación v2"),
    "categoria_D_IP_ampliacion": ("D", "IP — ampliación v2"),
    "categoria_F_bases_cotizacion_ampliacion": ("F", "Bases — ampliación v2"),
    "categoria_G_recargos_ampliacion": ("G", "Recargos — ampliación v2"),
    "categoria_J_muerte_supervivencia_ampliacion": ("J", "MS — ampliación v2"),
    "categoria_K_desempleo_ampliacion": ("K", "Desempleo — ampliación v2"),
    "categoria_Q_funcion_publica_AGE_ampliacion": ("Q", "Función pública — ampliación v2"),
    "categoria_R_RETA_ampliacion": ("R", "RETA — ampliación v2"),
    "trampas_calculo_avanzado_ampliacion": ("CA", "Cálculo avanzado — ampliación v2"),
}


def slugify(texto: str, maxlen: int = 60) -> str:
    """Convierte texto a slug lowercase-con-guiones."""
    if not texto:
        return "sin-titulo"
    # Quitar tildes
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    # Minúsculas, alfanuméricos y guiones
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    texto = texto.strip("-")
    return texto[:maxlen] or "sin-titulo"


def extraer_articulos(articulo_str: str) -> list[str]:
    """Extrae lista de artículos legales citados."""
    if not articulo_str:
        return []
    # Split por ; , y
    partes = re.split(r"[;,]", articulo_str)
    return [p.strip() for p in partes if p.strip()]


def estado_emoji(origen: str) -> tuple[str, str]:
    """Devuelve (emoji, texto_estado) según tag de origen."""
    if "BOE-DIRECTO" in origen or "VERIFICADA" in origen or "LEG-CONSOLIDADA" in origen:
        return ("✅", "verificada")
    if "OBSOLETA" in origen:
        return ("❌", "obsoleta")
    if "INVENTADA-DM" in origen:
        return ("🔴", "sin verificar")
    if "INVESTIGACION" in origen or "DM-SIMULACRO" in origen or "NUEVA" in origen or "CORREGIDA" in origen:
        return ("🟢", "de examen real")
    if "WEB" in origen or "GROK" in origen or "gemini" in origen:
        return ("🟡", "doctrina secundaria")
    return ("⚪", "sin clasificar")


def peso_examen(origen: str, articulo: str) -> str:
    """Heurística para estimar el peso pedagógico."""
    if "DM-SIMULACRO" in origen or "INVESTIGACION" in origen:
        return "alto"
    if "BOE-DIRECTO" in origen or "VERIFICADA" in origen:
        return "alto"
    if "TRLGSS" in articulo:
        return "medio"
    return "bajo"


def generar_tags(tid: str, categoria: str, origen: str, articulo: str) -> list[str]:
    """Genera tags Obsidian para la nota."""
    tags = ["trampa", f"categoria_{categoria}"]
    emoji, estado = estado_emoji(origen)
    tags.append(f"estado/{estado.replace(' ', '_')}")
    # Tag por norma principal citada
    for patron, tag in [
        ("TRLGSS", "TRLGSS"),
        ("LPAC", "LPAC"),
        ("EBEP", "EBEP"),
        (" ET", "ET"),
        ("Ley 27/1999", "LCoop"),
        ("Orden PJC", "Orden_cuantias"),
        ("RD 1415/2004", "Reglamento_recaudacion"),
    ]:
        if patron in articulo:
            tags.append(f"norma/{tag}")
    return tags


def construir_frontmatter(tid: str, trampa: dict, categoria_letra: str, categoria_nombre: str) -> str:
    """Genera el bloque YAML frontmatter de la nota Obsidian."""
    articulo = trampa.get("articulo", "")
    origen = trampa.get("origen", "")
    emoji, estado = estado_emoji(origen)
    tags = generar_tags(tid, categoria_letra, origen, articulo)

    # Escapar comillas en título
    titulo_escaped = trampa.get("titulo", "").replace('"', '\\"')

    lines = [
        "---",
        f'id: "{tid}"',
        f'titulo: "{titulo_escaped}"',
        f'categoria: "{categoria_letra} - {categoria_nombre}"',
        f'estado: "{estado}"',
        f'estado_emoji: "{emoji}"',
        f'origen: "{origen}"',
        f'articulos: {extraer_articulos(articulo)}',
        f'peso_examen: "{peso_examen(origen, articulo)}"',
        f'tags: {tags}',
    ]

    # Campos opcionales
    if "verificado_boe" in trampa:
        lines.append(f'verificado_boe: "{trampa["verificado_boe"]}"')
    if "verificado" in trampa:
        lines.append(f'verificado: "{trampa["verificado"]}"')
    if "confirmado_en" in trampa:
        lines.append(f'confirmado_en: "{trampa["confirmado_en"]}"')

    lines.append("---")
    return "\n".join(lines)


def construir_cuerpo_nota(tid: str, trampa: dict) -> str:
    """Genera el cuerpo markdown de la nota."""
    secciones = []

    # Título H1
    titulo = trampa.get("titulo", f"Trampa {tid}")
    secciones.append(f"# {tid} — {titulo}\n")

    # Regla
    if "regla" in trampa:
        secciones.append(f"## 📐 Regla\n\n{trampa['regla'].strip()}\n")

    # Trampa típica
    if "trampa_tipica" in trampa:
        secciones.append(f"## 🎯 Trampa típica\n\n{trampa['trampa_tipica'].strip()}\n")

    # Mnemónico
    if "mnemonico" in trampa:
        secciones.append(f"## 🧠 Mnemónico\n\n> {trampa['mnemonico'].strip()}\n")

    # Artículo (con wiki-links si posible)
    if "articulo" in trampa:
        arts = extraer_articulos(trampa["articulo"])
        if arts:
            arts_md = " · ".join(f"`{a}`" for a in arts)
            secciones.append(f"## 📖 Artículos aplicables\n\n{arts_md}\n")

    # Corrección si existe
    if "correccion" in trampa:
        secciones.append(f"## ⚠️ Corrección aplicada\n\n{trampa['correccion'].strip()}\n")
    if "correccion_critica" in trampa:
        secciones.append(f"## 🚨 Corrección crítica\n\n{trampa['correccion_critica'].strip()}\n")

    # Actualización legislativa si existe
    for key in ["actualizacion_2024", "actualizacion_2026"]:
        if key in trampa:
            secciones.append(f"## 📅 {key.replace('_', ' ').title()}\n\n{trampa[key].strip()}\n")

    # URL BOE si existe
    if "url_boe" in trampa:
        secciones.append(f"## 🔗 Enlace BOE\n\n{trampa['url_boe']}\n")

    # Ley pendiente
    if "ley_pendiente_ingesta" in trampa:
        secciones.append(f"## 📌 Ley pendiente de ingesta en RAG\n\n{trampa['ley_pendiente_ingesta']}\n")

    # Enunciado ejemplo
    if "enunciado_ejemplo" in trampa:
        secciones.append(f"## 📝 Enunciado de ejemplo\n\n{trampa['enunciado_ejemplo'].strip()}\n")

    # Metadatos de origen
    origen = trampa.get("origen", "sin especificar")
    emoji, estado = estado_emoji(origen)
    secciones.append(f"\n---\n\n**Origen**: {origen} · **Estado**: {emoji} {estado}\n")

    return "\n".join(secciones)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="No escribe archivos, solo simula")
    ap.add_argument("--vault-path", type=Path, default=DEFAULT_VAULT)
    args = ap.parse_args()

    if not YAML_PATH.exists():
        print(f"❌ No existe YAML: {YAML_PATH}", file=sys.stderr)
        return 1

    with open(YAML_PATH) as f:
        data = yaml.safe_load(f)

    vault_path = args.vault_path
    if not args.dry_run:
        vault_path.mkdir(parents=True, exist_ok=True)

    # Agrupar trampas por letra de categoría (uniendo bloques "ampliacion" con los principales)
    trampas_por_categoria: dict[str, list[tuple[str, dict, str]]] = {}
    nombre_por_letra: dict[str, str] = {}

    for seccion_key, (letra, nombre) in SECCIONES_TRAMPAS.items():
        seccion = data.get(seccion_key)
        if not isinstance(seccion, dict):
            continue
        for tid, trampa in seccion.items():
            if not isinstance(trampa, dict):
                continue
            trampas_por_categoria.setdefault(letra, []).append((tid, trampa, seccion_key))
            # Preferir nombre "principal" sobre "ampliacion"
            if letra not in nombre_por_letra or "ampliacion" not in nombre:
                nombre_por_letra[letra] = nombre.replace(" — ampliación v2", "")

    total_trampas = sum(len(v) for v in trampas_por_categoria.values())
    print(f"📊 Total trampas a generar: {total_trampas}")

    if args.dry_run:
        for letra, trampas in sorted(trampas_por_categoria.items()):
            print(f"  {letra}: {len(trampas)} notas")
        print(f"\n[DRY-RUN] Destino: {vault_path}")
        return 0

    # Generar notas individuales y índices
    rutas_creadas = []
    for letra, trampas in sorted(trampas_por_categoria.items()):
        nombre_cat = nombre_por_letra[letra]
        dir_cat = vault_path / f"{letra}_{slugify(nombre_cat, maxlen=30)}"
        dir_cat.mkdir(parents=True, exist_ok=True)

        # Ordenar trampas por ID numérico dentro de la letra
        def sort_key(item):
            tid = item[0]
            m = re.match(r"([A-Z]+)(\d+)", tid)
            return (m.group(1), int(m.group(2))) if m else (tid, 0)

        trampas_sorted = sorted(trampas, key=sort_key)

        indice_items = []
        for tid, trampa, _seccion in trampas_sorted:
            titulo = trampa.get("titulo", f"Trampa {tid}")
            slug = slugify(titulo, maxlen=55)
            nombre_nota = f"{tid}_{slug}.md"
            ruta_nota = dir_cat / nombre_nota

            frontmatter = construir_frontmatter(tid, trampa, letra, nombre_cat)
            cuerpo = construir_cuerpo_nota(tid, trampa)
            ruta_nota.write_text(f"{frontmatter}\n\n{cuerpo}\n", encoding="utf-8")
            rutas_creadas.append(ruta_nota)

            emoji, _ = estado_emoji(trampa.get("origen", ""))
            wiki_link = f"[[{dir_cat.name}/{nombre_nota[:-3]}|{tid} — {titulo[:70]}]]"
            indice_items.append(f"- {emoji} {wiki_link}")

        # Índice por categoría
        indice_cat = vault_path / f"_{letra}_{slugify(nombre_cat, maxlen=30)}.md"
        contenido_indice_cat = [
            f"# Categoría {letra} — {nombre_cat}",
            "",
            f"*{len(trampas_sorted)} trampas. Fuente: `trampas_unificadas_v2_CURADO.yaml`*",
            "",
            "## Trampas",
            "",
            *indice_items,
            "",
            "---",
            "[[_INDICE|← Volver al índice maestro]]",
        ]
        indice_cat.write_text("\n".join(contenido_indice_cat), encoding="utf-8")
        rutas_creadas.append(indice_cat)

    # Índice maestro
    contenido_maestro = [
        "# 📘 Índice Maestro de Trampas — OPOS SS 2026",
        "",
        f"**{total_trampas} trampas** organizadas en {len(trampas_por_categoria)} categorías.",
        "",
        "**Fuente única de verdad**: `~/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml`",
        "",
        "## Categorías",
        "",
    ]
    for letra, trampas in sorted(trampas_por_categoria.items()):
        nombre_cat = nombre_por_letra[letra]
        slug = slugify(nombre_cat, maxlen=30)
        contenido_maestro.append(f"- **[[_{letra}_{slug}|{letra} — {nombre_cat}]]** ({len(trampas)} trampas)")

    contenido_maestro.extend([
        "",
        "## Leyenda de estados",
        "",
        "- ✅ verificada BOE / legislación consolidada",
        "- 🟢 extraída de examen o simulacro DM",
        "- 🟡 doctrina secundaria (web / foros)",
        "- 🔴 sin verificar",
        "- ❌ obsoleta (reforma legal posterior)",
        "",
        "## Ver también",
        "",
        "- [[_PENDIENTES_VERIFICAR|Dashboard de trampas pendientes de verificar]]",
    ])
    ruta_maestro = vault_path / "_INDICE.md"
    ruta_maestro.write_text("\n".join(contenido_maestro), encoding="utf-8")
    rutas_creadas.append(ruta_maestro)

    # Dashboard de pendientes de verificar
    pendientes = []
    obsoletas = []
    for letra, trampas in sorted(trampas_por_categoria.items()):
        for tid, trampa, _s in trampas:
            origen = trampa.get("origen", "")
            if "INVENTADA-DM" in origen:
                pendientes.append((tid, trampa, letra))
            elif "OBSOLETA" in origen:
                obsoletas.append((tid, trampa, letra))

    dashboard = [
        "# 🔍 Dashboard — Trampas pendientes o con estado no-verificado",
        "",
        f"**Actualizado**: 2026-04-18 tras verificación completa.",
        "",
        f"## 🔴 Pendientes [INVENTADA-DM]: {len(pendientes)}",
        "",
    ]
    if not pendientes:
        dashboard.append("> 🎉 ¡Ninguna! Todas las trampas inventadas han sido verificadas.")
    else:
        for tid, trampa, letra in pendientes:
            dashboard.append(f"- **{tid}** ({letra}): {trampa.get('titulo', '')}")

    dashboard.extend([
        "",
        f"## ❌ Obsoletas: {len(obsoletas)}",
        "",
    ])
    if not obsoletas:
        dashboard.append("> Ninguna trampa marcada como obsoleta.")
    else:
        for tid, trampa, letra in obsoletas:
            dashboard.append(f"- **{tid}** ({letra}): {trampa.get('titulo', '')}")
            if "correccion_critica" in trampa:
                dashboard.append(f"  > {trampa['correccion_critica'][:200]}...")

    dashboard.extend([
        "",
        "---",
        "[[_INDICE|← Volver al índice maestro]]",
    ])
    ruta_dashboard = vault_path / "_PENDIENTES_VERIFICAR.md"
    ruta_dashboard.write_text("\n".join(dashboard), encoding="utf-8")
    rutas_creadas.append(ruta_dashboard)

    print(f"✅ {len(rutas_creadas)} archivos creados en {vault_path}")
    print(f"   - 1 índice maestro (_INDICE.md)")
    print(f"   - 1 dashboard pendientes (_PENDIENTES_VERIFICAR.md)")
    print(f"   - {len(trampas_por_categoria)} índices por categoría")
    print(f"   - {total_trampas} notas individuales")
    return 0


if __name__ == "__main__":
    sys.exit(main())
