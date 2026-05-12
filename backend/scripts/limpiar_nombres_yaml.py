#!/usr/bin/env python3
"""
limpiar_nombres_yaml.py — Preprocesa el YAML maestro de trampas antes de
regenerar el vault Obsidian público.

OBJETIVO:
  Eliminar cualquier huella de material externo (academias, preparadores,
  simulacros específicos) y mover la trazabilidad a campos privados con
  prefijo `_` que el generador de vault ignora.

OPERACIONES (en orden):
  1. Sustituciones textuales simples
       - Empresas del pool externo → pool propio memorable
       - Topónimo "Dénia" → "Almería"
       - Referencias "Diego de Miguel" / "Radi" / "CEF/opoadmins/laboroteca"
       - Tags "[SIMULACRO-PRIVADO]" / "[DM-SIMULACRO]" → "[ANÁLISIS-INTERNO]"
       - Claves YAML raíz renombradas con prefijo `_` (privado)
  2. Migración de `confirmado_en:` → bloque `_trazabilidad_interna:` con
     fuente opaca (SIM-ENERO, SIM-EJ19...), pregunta_original y nota.
  3. Escaneo de menciones embebidas ("Ejercicio 19 P1: ...", "Simulacro
     Diciembre ...") dentro de `trampa_tipica` / `regla` → solo reporta,
     NO modifica (requiere revisión humana para preservar sentido).

USO:
    python3 limpiar_nombres_yaml.py              # DRY-RUN (por defecto)
    python3 limpiar_nombres_yaml.py --apply      # aplica + backup datado

SEGURIDAD:
  - El script NUNCA escribe sin flag --apply.
  - Al aplicar crea siempre `<archivo>.bak-YYYYMMDD-HHMMSS` antes de tocar.
  - No usa PyYAML: opera sobre texto con regex para preservar comentarios
    y formato exactos del YAML original.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

YAML_PATH = Path(
    "/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/"
    "trampas_unificadas_v2_CURADO.yaml"
)

# (tag, regex, reemplazo). Se aplican línea a línea, en orden.
SIMPLE_REPLACEMENTS: List[Tuple[str, str, str]] = [
    # ─── Comentarios de cabecera / footer ─────────────────────────────────
    (
        "cabecera-fuente",
        r"# Fuente: Análisis acumulado de ejercicios 17-19 \+ casos simulacro privado",
        "# Fuente: Análisis interno + BOE consolidado",
    ),
    (
        "metodologia-dm-comment",
        r"# METODOLOGÍA PEDAGÓGICA DIEGO DE MIGUEL — 5 MARCAS",
        "# METODOLOGÍA PEDAGÓGICA INTERNA — 5 MARCAS",
    ),
    (
        "fuentes-academias",
        r"# Fuentes: web, foros oposiciones, BOE, academias CEF/opoadmins/laboroteca,",
        "# Fuentes: BOE, legislación consolidada, jurisprudencia, doctrina,",
    ),
    (
        "academias-generic",
        r"academias CEF/opoadmins/laboroteca",
        "doctrina consolidada",
    ),
    # ─── Claves YAML → prefijo privado ────────────────────────────────────
    (
        "clave-metodologia-raiz",
        r"^metodologia_simulacros_privados:",
        "_metodologia_interna:",
    ),
    (
        "clave-ejercicios-fuente",
        r"^  ejercicios_fuente:",
        "  _ejercicios_fuente_interno:",
    ),
    # ─── Referencias a notas / preparador ────────────────────────────────
    (
        "notas-radi",
        r"\bNotas Radi\b",
        "notas internas",
    ),
    (
        "casos-simulacro-privado-texto",
        r"casos simulacro privado",
        "casos internos",
    ),
    # ─── Empresas pool externo → pool propio memorable ────────────────────
    # Nido del Alba → Bodegas Dionisios S.A.
    (
        "empresa-nido-upper-sl",
        r"\bNIDO DEL ALBA\s+S\.?L\.?\b",
        "BODEGAS DIONISIOS S.A.",
    ),
    (
        "empresa-nido-upper",
        r"\bNIDO DEL ALBA\b",
        "BODEGAS DIONISIOS",
    ),
    (
        "empresa-nido-cap-sl",
        r"\bNido del Alba\s+S\.?L\.?\b",
        "Bodegas Dionisios S.A.",
    ),
    (
        "empresa-nido-cap",
        r"\bNido del Alba\b",
        "Bodegas Dionisios",
    ),
    # Cookie Coffee → Cafetería Eterno Despertar
    (
        "empresa-cookie-upper",
        r"\bCOOKIE COFFEE\b",
        "CAFETERÍA ETERNO DESPERTAR",
    ),
    (
        "empresa-cookie",
        r"\bCookie Coffee\b",
        "Cafetería Eterno Despertar",
    ),
    # Garmendia → Construcciones Dedal de Oro
    (
        "empresa-garmendia-upper",
        r"\bGARMENDIA\b",
        "CONSTRUCCIONES DEDAL DE ORO",
    ),
    (
        "empresa-garmendia",
        r"\bGarmendia\b",
        "Construcciones Dedal de Oro",
    ),
    # ─── Topónimo ─────────────────────────────────────────────────────────
    (
        "topo-denia",
        r"\bDénia\b",
        "Almería",
    ),
    (
        "topo-denia-upper",
        r"\bDÉNIA\b",
        "ALMERÍA",
    ),
    # ─── Tags de origen ───────────────────────────────────────────────────
    (
        "origen-simulacro-privado",
        r'origen:\s*"\[SIMULACRO-PRIVADO\]"',
        'origen: "[ANÁLISIS-INTERNO]"',
    ),
    (
        "origen-dm-simulacro",
        r'origen:\s*"\[DM-SIMULACRO\]"',
        'origen: "[ANÁLISIS-INTERNO]"',
    ),
    (
        "origen-dm-maestro",
        r'origen:\s*"\[DM-MAESTRO\]"',
        'origen: "[ANÁLISIS-INTERNO]"',
    ),
    # [INVESTIGACION — <autor/anexo/pregunta privada>] → [INVESTIGACION-INTERNA]
    (
        "origen-investigacion-opaco",
        r'origen:\s*"\[INVESTIGACION\s+—\s+[^"]*\]"',
        'origen: "[INVESTIGACION-INTERNA]"',
    ),
    # [WEB] — <url/foro/academia> → [DOCTRINA-CONSOLIDADA]
    (
        "origen-web-opaco",
        r'origen:\s*"\[WEB\]\s+—\s+[^"]*"',
        'origen: "[DOCTRINA-CONSOLIDADA]"',
    ),
    # [CORREGIDA — <referencia examen/simulacro>] → [ANÁLISIS-INTERNO]
    (
        "origen-corregida-opaco",
        r'origen:\s*"\[CORREGIDA\s+—\s+[^"]*\]"',
        'origen: "[ANÁLISIS-INTERNO]"',
    ),
    # [NUEVA — confirmada con respuesta oficial PNN simulacro X] → [ANÁLISIS-INTERNO]
    (
        "origen-nueva-opaco",
        r'origen:\s*"\[NUEVA\s+—\s+[^"]*\]"',
        'origen: "[ANÁLISIS-INTERNO]"',
    ),
    # [CRÍTICA-RDL-2-2023 — REESCRITA COMO TRAMPA INVERSA] → [ANÁLISIS-INTERNO]
    (
        "origen-critica-reescrita",
        r'origen:\s*"\[CRÍTICA-RDL-2-2023\s+—\s+REESCRITA COMO TRAMPA INVERSA\]"',
        'origen: "[ANÁLISIS-INTERNO]"',
    ),
    # [VERIFICADA-BOE-2026-04-18 — gemini_c19 reformulada] → quitar el sufijo privado
    (
        "origen-verificada-gemini-cNN",
        r'origen:\s*"\[VERIFICADA-BOE-2026-04-18\s+—\s+gemini_c\d+[^"]*\]"',
        'origen: "[VERIFICADA-BOE-2026-04-18]"',
    ),
    # [gemini_cXX — t_xxx] → [ANÁLISIS-INTERNO]
    (
        "origen-gemini-cNN-solo",
        r'origen:\s*"\[gemini_c\d+\s+—\s+[^"]*\]"',
        'origen: "[ANÁLISIS-INTERNO]"',
    ),
    # [BOE-DIRECTO + TEMARIO-PRIVADO] → [BOE-DIRECTO]
    (
        "origen-temario-privado",
        r'origen:\s*"\[BOE-DIRECTO\s+\+\s+TEMARIO-PRIVADO\]"',
        'origen: "[BOE-DIRECTO]"',
    ),
    # [GROK — fórmula X ...] → [ANÁLISIS-INTERNO]
    (
        "origen-grok-opaco",
        r'origen:\s*"\[GROK\s+—\s+[^"]*\]"',
        'origen: "[ANÁLISIS-INTERNO]"',
    ),
    # ─── Paréntesis embebidos con leaks ──────────────────────────────────
    # "(P22 simulacro enero 2026)" / "(Supuesto 2022 C1 PI P1)" / "(examen PI 2023)"
    # Se eliminan por completo (paréntesis incluido).
    (
        "parentesis-leak-examen-simulacro",
        r"\s*\([^)]*?(?:[Ss]imulacro\s+\w+(?:\s+\d{4})?|examen\s+PI|Supuesto\s+\d{4}|examen\s+real\s+P\d+)[^)]*?\)",
        "",
    ),
    # Prefijo "Ejemplo P25 examen PI 2023:" al inicio de un escalar
    (
        "prefijo-ejemplo-examen-pi",
        r"\bEjemplo\s+P\d+\s+examen\s+PI\s+\d{4}\s*:\s*",
        "",
    ),
]

# =============================================================================
# MIGRACIÓN confirmado_en → _trazabilidad_interna
# =============================================================================

CONFIRMADO_EN_RE = re.compile(
    r'^(?P<indent>\s+)confirmado_en:\s*"(?P<valor>.+)"\s*$'
)

# Patrones para parsear el valor de confirmado_en
# (ref admite multi-palabra: "Enero 2026", "NIDO DEL ALBA", "19", etc.)
TRAZA_SINGLE = re.compile(
    r"^\s*(?P<tipo>Simulacro|Ejercicio)\s+(?P<ref>.+?)"
    r"\s+P(?P<preg>\d+)(?:\s*[—\-]\s*(?P<nota>.+))?\s*$"
)

TRAZA_MULTI = re.compile(
    r"^\s*(?P<tipo>Simulacro|Ejercicio)\s+(?P<ref>.+?)"
    r"\s+P(?P<preg1>\d+)\s+y\s+P(?P<preg2>\d+)(?:\s*[—\-]\s*(?P<nota>.+))?\s*$"
)


def fuente_opaca(tipo: str, ref: str) -> str:
    """Convierte 'Ejercicio 19' → 'SIM-EJ19', 'Simulacro Enero' → 'SIM-ENERO'."""
    ref_u = ref.upper().replace(" ", "-")
    if tipo == "Ejercicio":
        return f"SIM-EJ{ref_u}"
    return f"SIM-{ref_u}"


def parse_traza(valor: str) -> dict:
    """Parsea el valor textual y devuelve dict para _trazabilidad_interna."""
    m = TRAZA_MULTI.match(valor)
    if m:
        return {
            "fuente": fuente_opaca(m.group("tipo"), m.group("ref")),
            "pregunta_original": f"{m.group('preg1')} y {m.group('preg2')}",
            "nota": (m.group("nota") or "").strip(),
        }
    m = TRAZA_SINGLE.match(valor)
    if m:
        return {
            "fuente": fuente_opaca(m.group("tipo"), m.group("ref")),
            "pregunta_original": int(m.group("preg")),
            "nota": (m.group("nota") or "").strip(),
        }
    # Fallback: no se pudo parsear
    return {"fuente": "INTERNO", "nota": valor.strip()}


def render_trazabilidad(indent: str, traza: dict) -> List[str]:
    """Convierte un dict de traza en líneas YAML bien formateadas."""
    sub = indent + "  "
    out = [f"{indent}_trazabilidad_interna:\n"]
    for key in ("fuente", "pregunta_original", "nota"):
        if key not in traza:
            continue
        val = traza[key]
        if val in ("", None):
            continue
        if isinstance(val, int):
            out.append(f"{sub}{key}: {val}\n")
        else:
            v_str = str(val).replace("\\", "\\\\").replace('"', '\\"')
            out.append(f'{sub}{key}: "{v_str}"\n')
    return out


# =============================================================================
# REPORTE
# =============================================================================


@dataclass
class Reporte:
    cambios: List[dict] = field(default_factory=list)
    warnings: List[dict] = field(default_factory=list)

    def add_cambio(self, linea: int, tipo: str, antes: str, despues: str):
        self.cambios.append(
            {"linea": linea, "tipo": tipo, "antes": antes, "despues": despues}
        )

    def add_warning(self, linea: int, tipo: str, texto: str):
        self.warnings.append({"linea": linea, "tipo": tipo, "texto": texto})


# =============================================================================
# PIPELINE
# =============================================================================


def apply_simple_replacements(lines: List[str], rep: Reporte) -> List[str]:
    """Aplica SIMPLE_REPLACEMENTS línea a línea."""
    out = []
    for i, line in enumerate(lines, start=1):
        new_line = line
        for tag, pattern, repl in SIMPLE_REPLACEMENTS:
            prev = new_line
            new_line = re.sub(pattern, repl, new_line)
            if new_line != prev:
                rep.add_cambio(i, tag, prev.rstrip("\n"), new_line.rstrip("\n"))
        out.append(new_line)
    return out


def transform_confirmado_en(lines: List[str], rep: Reporte) -> List[str]:
    """Sustituye líneas `confirmado_en:` por bloque `_trazabilidad_interna:`."""
    out = []
    for i, line in enumerate(lines, start=1):
        m = CONFIRMADO_EN_RE.match(line)
        if not m:
            out.append(line)
            continue
        indent = m.group("indent")
        valor = m.group("valor")
        traza = parse_traza(valor)
        new_lines = render_trazabilidad(indent, traza)
        rep.add_cambio(
            i,
            "confirmado_en→_trazabilidad",
            line.rstrip("\n"),
            "".join(ln.rstrip("\n") + " ↵ " for ln in new_lines).rstrip(" ↵ "),
        )
        out.extend(new_lines)
    return out


# =============================================================================
# FASE 2 — Limpieza de menciones embebidas en texto libre
# =============================================================================

# Prefijo "Ejercicio N: ...", "Ejercicio N P_N: ...", "Ejercicio N P_N y Simulacro X P_M: ..."
# al inicio de una línea dentro de bloques escalares (trampa_tipica:, regla:, etc.)
EJERCICIO_PREFIX_RE = re.compile(
    r"^(?P<indent>\s+)"
    r"(?P<prefix>(?:Ejercicio\s+\d+|Simulacro\s+(?:Enero|Diciembre|Febrero|Marzo|Noviembre|Octubre)(?:\s+\d{4})?)"
    r"(?:\s+P\d+)?"
    # continuación opcional: " y/vs (Ejercicio N|Simulacro X|P_N)" con P_N opcional
    r"(?:\s+(?:y|vs)\s+(?:(?:Ejercicio\s+\d+|Simulacro\s+(?:Enero|Diciembre|Febrero|Marzo|Noviembre|Octubre)(?:\s+\d{4})?)(?:\s+P\d+)?|P\d+))?"
    r")"
    r":\s*"
    r"(?P<rest>\S.*)$"
)

# Mención "Simulacro Enero 2026 PNN," / "simulacro enero P11" dentro de un valor
# escalar en línea (verificado:, verificado_pNN:, correccion:, etc.). Elimina la
# frase manteniendo el resto de la oración legible. Acepta mayúsculas y minúsculas.
SIMULACRO_EMBED_RE = re.compile(
    r"(?:[Ss]imulacro\s+(?:[Ee]nero|[Dd]iciembre|[Ff]ebrero|[Mm]arzo|[Nn]oviembre|[Oo]ctubre)(?:\s+\d{4})?|[Ee]jercicio\s+\d+)"
    r"(?:\s+P\d+)?,?\s*"
)


def transform_ejercicio_prefix(lines: List[str], rep: Reporte) -> List[str]:
    """Elimina prefijos del tipo 'Ejercicio 19 P1: ' al inicio de frases escalares.

    Mantiene la indentación y capitaliza la primera letra del resto.
    Solo actúa sobre líneas que NO son claves YAML (no terminan en ':').
    """
    out = []
    for i, line in enumerate(lines, start=1):
        # No tocar claves YAML puras (que terminan con ':')
        stripped = line.rstrip("\n").rstrip()
        if stripped.endswith(":"):
            out.append(line)
            continue

        m = EJERCICIO_PREFIX_RE.match(line)
        if not m:
            out.append(line)
            continue

        rest = m.group("rest").strip()
        if not rest:
            out.append(line)
            continue

        # Capitalizar primera letra del resto (respetando tildes)
        first_char = rest[0]
        new_text = first_char.upper() + rest[1:]
        new_line = f"{m.group('indent')}{new_text}\n"

        rep.add_cambio(
            i,
            "limpiar-prefijo-ejercicio",
            line.rstrip("\n"),
            new_line.rstrip("\n"),
        )
        out.append(new_line)
    return out


def transform_verificado_embed(lines: List[str], rep: Reporte) -> List[str]:
    """Elimina menciones 'Simulacro Enero 2026 P39' / 'Ejercicio 19 P5' embebidas
    en valores de campos tipo verificado_pNN: "✅ VERIFICADO — Simulacro ... P39, ..."."""
    # Solo actúa en líneas cuyo key indica verificación
    target_key_re = re.compile(
        r'^(?P<pre>\s+(?:verificado(?:_p\d+)?|verificado_boe|correccion|nota_adicional|error_corregido|correccion_sesion|ley_pendiente_ingesta):\s*)'
        r'(?P<val>.+)$'
    )
    out = []
    for i, line in enumerate(lines, start=1):
        m = target_key_re.match(line)
        if not m:
            out.append(line)
            continue
        pre = m.group("pre")
        val = m.group("val")
        new_val = SIMULACRO_EMBED_RE.sub("", val)
        # Limpiar artefactos dobles: "  " o " , " o comas huérfanas al inicio
        new_val = re.sub(r"\s{2,}", " ", new_val)
        new_val = re.sub(r"^\s*[—\-,]\s*", "", new_val)
        new_val = re.sub(r'"\s*,\s*', '"', new_val)
        if new_val != val:
            new_line = f"{pre}{new_val}\n"
            rep.add_cambio(
                i,
                "limpiar-simulacro-embebido",
                line.rstrip("\n"),
                new_line.rstrip("\n"),
            )
            out.append(new_line)
        else:
            out.append(line)
    return out


# Detector de menciones embebidas NO migradas (solo warning)
EMBED_REGEX = re.compile(
    r"\b(Ejercicio\s+\d+|Simulacro\s+(?:Enero|Diciembre|Febrero|Marzo|Noviembre|Octubre)(?:\s+\d{4})?)\b"
)

# Estas claves contienen metadata privada legítima (no son warnings tras limpieza)
KEYS_WHITELIST_WARNINGS = (
    "_trazabilidad_interna:",
    "_ejercicios_fuente_interno:",
    "_metodologia_interna:",
)


def scan_embed_mentions(lines: List[str], rep: Reporte) -> None:
    """Reporta menciones embebidas de Ejercicio/Simulacro fuera de campos privados."""
    in_private_block = False
    private_block_indent = -1
    for i, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        current_indent = len(line) - len(stripped)

        # Detectar entrada/salida de bloque privado (prefijo `_`)
        if stripped.startswith("_") and stripped.endswith(":\n"):
            in_private_block = True
            private_block_indent = current_indent
            continue
        if in_private_block:
            # Si la indentación vuelve al nivel del bloque privado o menor y la línea
            # no empieza con espacio → salimos del bloque
            if line.strip() == "":
                continue
            if current_indent <= private_block_indent and not stripped.startswith("_"):
                in_private_block = False
                private_block_indent = -1

        if in_private_block:
            continue

        # Línea dentro del YAML "público" — buscar menciones sensibles
        m = EMBED_REGEX.search(line)
        if m:
            rep.add_warning(
                i,
                "mencion-embebida",
                f"{m.group(0)!r} en: {line.rstrip()[:110]}",
            )


# =============================================================================
# SALIDA / IMPRESIÓN
# =============================================================================


def imprimir_reporte(rep: Reporte, dry_run: bool) -> None:
    modo = "DRY-RUN" if dry_run else "APPLY"
    print("\n" + "=" * 78)
    print(f"LIMPIEZA YAML — {modo}")
    print(f"Archivo:  {YAML_PATH}")
    print(f"Cambios:  {len(rep.cambios)}")
    print(f"Warnings: {len(rep.warnings)} (menciones embebidas no migradas)")
    print("=" * 78)

    # --- Cambios ---
    if rep.cambios:
        print("\n── CAMBIOS APLICADOS ──")
        for c in rep.cambios:
            print(f"\n[L{c['linea']:>4}] {c['tipo']}")
            ant = c["antes"].strip()
            des = c["despues"].strip()
            print(f"  − {ant[:110]}{'…' if len(ant) > 110 else ''}")
            print(f"  + {des[:110]}{'…' if len(des) > 110 else ''}")

    # --- Warnings ---
    if rep.warnings:
        print("\n── WARNINGS (revisar a mano) ──")
        for w in rep.warnings:
            print(f"[L{w['linea']:>4}] {w['tipo']}: {w['texto']}")

    # --- Resumen ---
    print("\n" + "─" * 78)
    print("RESUMEN POR TIPO DE CAMBIO:")
    for tipo, n in Counter(c["tipo"] for c in rep.cambios).most_common():
        print(f"  {n:>4}  {tipo}")
    if rep.warnings:
        print("\nRESUMEN POR TIPO DE WARNING:")
        for tipo, n in Counter(w["tipo"] for w in rep.warnings).most_common():
            print(f"  {n:>4}  {tipo}")
    print("=" * 78)


# =============================================================================
# ENTRY POINT
# =============================================================================


def run(dry_run: bool) -> None:
    if not YAML_PATH.exists():
        sys.exit(f"ERROR: No existe el YAML en {YAML_PATH}")

    content = YAML_PATH.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)

    rep = Reporte()
    # ── FASE 1 — Migración estructural ───────────────────────────────────
    # Orden importante: confirmado_en PRIMERO (para que el parser vea los
    # nombres originales y genere fuentes opacas correctas antes de que las
    # sustituciones textuales alteren los valores).
    lines = transform_confirmado_en(lines, rep)
    lines = apply_simple_replacements(lines, rep)
    # ── FASE 2 — Limpieza de menciones embebidas ────────────────────────
    lines = transform_ejercicio_prefix(lines, rep)
    lines = transform_verificado_embed(lines, rep)
    # ── FASE 3 — Escaneo residual (warnings) ────────────────────────────
    scan_embed_mentions(lines, rep)

    imprimir_reporte(rep, dry_run)

    if dry_run:
        print("\n⚪ DRY-RUN: no se ha escrito ningún archivo.")
        print("   Para aplicar: python3 limpiar_nombres_yaml.py --apply")
        return

    # Backup + escritura
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = YAML_PATH.with_suffix(YAML_PATH.suffix + f".bak-{ts}")
    shutil.copy2(YAML_PATH, backup)
    YAML_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"\n✅ APLICADO. Backup: {backup}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Limpia nombres y trazas externas del YAML de trampas."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplica los cambios (por defecto DRY-RUN).",
    )
    args = parser.parse_args()
    run(dry_run=not args.apply)


if __name__ == "__main__":
    main()
