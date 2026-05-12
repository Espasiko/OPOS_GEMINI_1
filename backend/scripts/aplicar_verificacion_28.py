#!/usr/bin/env python3
"""
Aplica las correcciones del MD VERIFICACION_28_INVENTADAS.md al YAML v2.

Política:
  - 20 trampas VERIFICADAS → origen: "[INVENTADA-DM]" reemplazado por "[VERIFICADA-POST-FUSION-2026-04]"
  - 7 trampas REFORMULADAS → origen cambia a "[VERIFICADA-CON-CORRECCION-2026-04]" + campo 'correccion:' añadido
  - 1 trampa OBSOLETA (P4) → origen marcado "[OBSOLETA-RDL-2-2023]" + aviso

Uso: python3 aplicar_verificacion_28.py [--dry-run]

Autor: Cascade | Fecha: 2026-04-18
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

YAML_PATH = Path("/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml")

# -----------------------------------------------------------------------------
# Veredicto por ID de trampa
# -----------------------------------------------------------------------------
VERIFICADAS = {
    # 20 trampas que quedan tal cual, solo cambia el tag de origen
    "C14", "J2", "J3", "J5", "J6",
    "K1", "K3", "K4", "K5",
    "L1", "L2", "L3",
    "N5", "N6",
    "P1",
    "Q1", "Q4",
    "CA1", "CA2", "CA4",
}

REFORMULADAS = {
    "J4": {
        "articulo_nuevo": 'Art. 219, Art. 221 bis TRLGSS; RD 900/2018; DF 27ª Ley 40/2007',
        "correccion": (
            "Art. 231 TRLGSS NO regula las condiciones del 60%/70%. "
            "Son reglas repartidas: 52% base en Art. 219 TRLGSS; 60% por Art. 221 bis TRLGSS + RD 900/2018; "
            "70% por DF 27ª Ley 40/2007. Verificado 2026-04-18."
        ),
    },
    "N7": {
        "sustitucion_texto": [
            ("10 DÍAS HÁBILES", "10 DÍAS NATURALES"),
            ("10 días hábiles", "10 días naturales"),
            ("diez días hábiles", "diez días naturales"),
        ],
        "correccion": (
            "Corregido 2026-04-18: el Art. 43.2 LPAC establece 10 días NATURALES (no hábiles) "
            "desde la puesta a disposición. La redacción anterior decía 'hábiles' por error."
        ),
    },
    "Q2": {
        "campo_extra": (
            "actualizacion_2026",
            "RDL 9/2025 (30/07/2025): permisos ampliados por Directiva UE 2019/1158. "
            "Verificar duración actualizada para AGE 2026 — la regla de 16 semanas de 2021 "
            "puede haberse modificado."
        ),
    },
    "Q3": {
        "articulo_nuevo": 'Art. 22 y 23.2 EBEP; LPGE anual',
        "correccion": (
            "Art. 22 EBEP clasifica retribuciones; el detalle operativo de pagas extras "
            "(sueldo base + trienios) está en Art. 23.2.a y 23.2.b EBEP + LPGE anual."
        ),
    },
    "CA5": {
        "articulo_nuevo": 'Art. 315 TRLGSS; RD 1273/2003; Orden TAS/1040/2005',
        "correccion": (
            "Art. 308 TRLGSS solo enumera la acción protectora del RETA. "
            "El devengo específico de la IT (día 4 EC / día siguiente AT) está en el "
            "desarrollo reglamentario del Art. 315 TRLGSS + RD 1273/2003."
        ),
    },
    "CA6": {
        "articulo_nuevo": 'Art. 280.4 TRLGSS; Art. 274 TRLGSS',
        "correccion": (
            "El Art. 274.4 TRLGSS citado no existe con ese contenido. "
            "La cotización del SEPE al 125% del grupo 7 durante el subsidio +52 está en "
            "Art. 280.4 TRLGSS. Art. 274 regula beneficiarios."
        ),
    },
    "K6": {
        "campo_extra": (
            "actualizacion_2024",
            "RDL 2/2024 (mayo 2024) modificó el Art. 282 TRLGSS para mejorar compatibilidad "
            "desempleo+TP. Verificar nueva redacción antes de publicar. La regla general "
            "(reducción proporcional) sigue siendo válida."
        ),
    },
}

OBSOLETAS = {
    "P4": {
        "nuevo_origen": "[OBSOLETA-RDL-2-2023-COEFICIENTE-PARCIALIDAD-DEROGADO]",
        "correccion_critica": (
            "⚠️ REGLA OBSOLETA desde 01/10/2023. "
            "El RDL 2/2023 DEROGÓ el coeficiente global de parcialidad. "
            "Ahora cada día de alta a tiempo parcial computa como 1 día cotizado completo "
            "a efectos de carencia, jubilación, IP y muerte y supervivencia. "
            "DECISIÓN PENDIENTE: ¿eliminar esta trampa o reescribirla como 'trampa inversa' "
            "para capturar al opositor que use la regla antigua?"
        ),
    },
}


# -----------------------------------------------------------------------------
# Procesamiento
# -----------------------------------------------------------------------------
def procesar(contenido: str, dry_run: bool = False) -> tuple[str, list[str]]:
    """Devuelve (nuevo_contenido, lista_de_cambios_realizados)."""
    cambios = []
    lineas = contenido.split("\n")

    # Iteramos por cada bloque de trampa (identificado por "  XX:" al nivel 2)
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        # Detecta cabecera de trampa: "  ID:" o "    ID:" — buscamos "^  [A-Z]+\d+:$"
        m = re.match(r"^(  |    )([A-Z]+\d+):\s*$", linea)
        if not m:
            i += 1
            continue

        tid = m.group(2)

        # ¿Esta trampa está en nuestra lista de cambios?
        if tid not in VERIFICADAS and tid not in REFORMULADAS and tid not in OBSOLETAS:
            i += 1
            continue

        # Encontrar el final del bloque (siguiente línea que empiece con "  [A-Z]" o sección nueva)
        fin_bloque = i + 1
        while fin_bloque < len(lineas):
            l = lineas[fin_bloque]
            # Siguiente trampa o sección nueva
            if re.match(r"^(  |    )[A-Z]+\d+:\s*$", l):
                break
            if re.match(r"^[a-z]", l) and ":" in l:  # sección top-level
                break
            if re.match(r"^# =", l):  # separador de sección
                break
            fin_bloque += 1

        # Aplicar cambios al bloque
        nuevo_bloque = aplicar_cambios_a_bloque(tid, lineas[i:fin_bloque])
        if nuevo_bloque != lineas[i:fin_bloque]:
            cambios.append(f"✏️  {tid} modificada")
            lineas[i:fin_bloque] = nuevo_bloque
            # Ajustar el índice porque el bloque puede haber crecido (campos añadidos)
            fin_bloque = i + len(nuevo_bloque)

        i = fin_bloque

    return "\n".join(lineas), cambios


def aplicar_cambios_a_bloque(tid: str, bloque: list[str]) -> list[str]:
    """Aplica cambios al bloque de una trampa según su ID."""
    nuevo = list(bloque)

    # Regex flexible que capta [INVENTADA-DM] y [INVENTADA-DM con base ...] etc.
    pat_inv = re.compile(r'origen:\s*"\[INVENTADA-DM[^"]*"')

    # Caso 1: VERIFICADA tal cual
    if tid in VERIFICADAS:
        for j, linea in enumerate(nuevo):
            if pat_inv.search(linea):
                nuevo[j] = pat_inv.sub(
                    'origen: "[VERIFICADA-POST-FUSION-2026-04]"',
                    linea
                )
                break
        return nuevo

    # Caso 2: REFORMULADA con cambios puntuales
    if tid in REFORMULADAS:
        cfg = REFORMULADAS[tid]

        # Cambiar tag origen a VERIFICADA-CON-CORRECCION
        for j, linea in enumerate(nuevo):
            if pat_inv.search(linea):
                nuevo[j] = pat_inv.sub(
                    'origen: "[VERIFICADA-CON-CORRECCION-2026-04]"',
                    linea
                )
                break

        # Sustituir artículo si procede
        if "articulo_nuevo" in cfg:
            for j, linea in enumerate(nuevo):
                if re.match(r'^\s+articulo:\s+"', linea):
                    indent = re.match(r'^(\s+)', linea).group(1)
                    nuevo[j] = f'{indent}articulo: "{cfg["articulo_nuevo"]}"'
                    break

        # Sustituir texto si procede (N7)
        if "sustitucion_texto" in cfg:
            for j, linea in enumerate(nuevo):
                for viejo, nuevo_txt in cfg["sustitucion_texto"]:
                    if viejo in linea:
                        nuevo[j] = linea.replace(viejo, nuevo_txt)

        # Añadir campo correccion al final del bloque (antes de línea en blanco)
        if "correccion" in cfg:
            # Encuentra la indentación del bloque (4 espacios = nivel 2)
            indent = "    "
            for linea in nuevo:
                m = re.match(r'^(\s+)titulo:', linea)
                if m:
                    indent = m.group(1)
                    break
            # Texto de corrección multi-línea
            correccion_lines = [
                f'{indent}correccion: >',
            ]
            for chunk in cfg["correccion"].split(". "):
                if chunk.strip():
                    correccion_lines.append(f'{indent}  {chunk.strip()}.')
            # Insertar antes de la línea en blanco final (si existe) o al final
            # Buscar la última línea no vacía
            ult_no_vacia = len(nuevo) - 1
            while ult_no_vacia > 0 and not nuevo[ult_no_vacia].strip():
                ult_no_vacia -= 1
            nuevo = nuevo[:ult_no_vacia + 1] + correccion_lines + nuevo[ult_no_vacia + 1:]

        # Añadir campo extra si procede (actualizacion_2024, actualizacion_2026...)
        if "campo_extra" in cfg:
            nombre_campo, valor_campo = cfg["campo_extra"]
            indent = "    "
            for linea in nuevo:
                m = re.match(r'^(\s+)titulo:', linea)
                if m:
                    indent = m.group(1)
                    break
            campo_lines = [
                f'{indent}{nombre_campo}: >',
            ]
            for chunk in valor_campo.split(". "):
                if chunk.strip():
                    campo_lines.append(f'{indent}  {chunk.strip()}.')
            ult_no_vacia = len(nuevo) - 1
            while ult_no_vacia > 0 and not nuevo[ult_no_vacia].strip():
                ult_no_vacia -= 1
            nuevo = nuevo[:ult_no_vacia + 1] + campo_lines + nuevo[ult_no_vacia + 1:]

        return nuevo

    # Caso 3: OBSOLETA
    if tid in OBSOLETAS:
        cfg = OBSOLETAS[tid]

        # Cambiar tag origen a OBSOLETA
        for j, linea in enumerate(nuevo):
            if pat_inv.search(linea):
                nuevo[j] = pat_inv.sub(
                    f'origen: "{cfg["nuevo_origen"]}"',
                    linea
                )
                break

        # Añadir correccion_critica al final
        indent = "    "
        for linea in nuevo:
            m = re.match(r'^(\s+)titulo:', linea)
            if m:
                indent = m.group(1)
                break
        correccion_lines = [
            f'{indent}correccion_critica: >',
        ]
        for chunk in cfg["correccion_critica"].split(". "):
            if chunk.strip():
                correccion_lines.append(f'{indent}  {chunk.strip()}.')
        ult_no_vacia = len(nuevo) - 1
        while ult_no_vacia > 0 and not nuevo[ult_no_vacia].strip():
            ult_no_vacia -= 1
        nuevo = nuevo[:ult_no_vacia + 1] + correccion_lines + nuevo[ult_no_vacia + 1:]

        return nuevo

    return nuevo


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="No escribe cambios, solo muestra")
    args = ap.parse_args()

    if not YAML_PATH.exists():
        print(f"❌ No existe: {YAML_PATH}", file=sys.stderr)
        return 1

    contenido_original = YAML_PATH.read_text(encoding="utf-8")
    contenido_nuevo, cambios = procesar(contenido_original, dry_run=args.dry_run)

    print(f"📊 Total de cambios aplicados: {len(cambios)}")
    for c in cambios:
        print(f"   {c}")

    if args.dry_run:
        print("\n[DRY RUN] No se escribe. Usa sin --dry-run para aplicar.")
        return 0

    # Validar YAML antes de sobrescribir
    try:
        import yaml
        yaml.safe_load(contenido_nuevo)
    except Exception as e:
        print(f"❌ YAML resultante NO VÁLIDO: {e}", file=sys.stderr)
        print("   No se ha escrito. Revisa el script.", file=sys.stderr)
        # Guardar diff en archivo temporal para depuración
        debug_path = YAML_PATH.with_suffix(".yaml.DEBUG")
        debug_path.write_text(contenido_nuevo, encoding="utf-8")
        print(f"   Debug volcado en: {debug_path}", file=sys.stderr)
        return 2

    # Backup
    backup_path = YAML_PATH.with_suffix(".yaml.bak-antes-verificacion-28")
    backup_path.write_text(contenido_original, encoding="utf-8")
    print(f"💾 Backup: {backup_path}")

    # Escribir
    YAML_PATH.write_text(contenido_nuevo, encoding="utf-8")
    print(f"✅ Escrito: {YAML_PATH}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
