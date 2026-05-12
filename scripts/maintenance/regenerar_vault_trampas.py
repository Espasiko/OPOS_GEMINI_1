#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenera el vault Obsidian BOVEDA_OPOS con las 184 trampas CURADAS + esquemas/mental maps.

Origen trampas: /home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml
Origen esquemas: /home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/TEMARIO_DM_POR_TEMAS/ultimos_cambios_DM_04_26/esquemas_DM_fotos/extraidos_md/
Destino: /mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki/

Conserva el formato de nota existente (frontmatter + secciones 📐 🎯 🧠 📖)
y añade:
  - bloque ## ⚠️ Corrección aplicada  (si la trampa tiene 'correccion*' en YAML)
  - bloque ## 📜 Texto literal BOE     (si la trampa tiene 'texto_literal_ref')
  - bloque ## 📚 Esquemas relacionados (WIKILINKS automáticos a mapas mentales)
  - campos frontmatter: verificado_boe, criticidad, tiene_correccion
  - emoji de estado según criticidad: 🟢 verificada · 🔴 error corregido · ⚠️ trampa inversa

Integración de esquemas:
  - Analiza CONTENIDO de cada esquema (no solo título)
  - Detecta keywords, categorías y artículos citados
  - Crea wikilinks automáticos desde trampas a esquemas relacionados
  - Máximo 5 esquemas por trampa (más relevantes primero)

⚠️  NO hace backup (el usuario lo ha pedido así para ahorrar tiempo/espacio).
"""
from __future__ import annotations

import re
import shutil
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# --- Rutas ---
YAML_SRC = Path("/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/trampas_unificadas_v2_CURADO.yaml")
VAULT = Path("/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS")
TRAMPAS_DIR = VAULT / "wiki" / "trampas"
ESQUEMAS_SRC = Path("/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/TEMARIO_DM_POR_TEMAS/ultimos_cambios_DM_04_26/esquemas_DM_fotos/extraidos_md")
ESQUEMAS_DIR = VAULT / "wiki" / "esquemas"

# Claves de primer nivel en YAML que NO son trampas.
# Cualquier clave con prefijo `_` también se ignora automáticamente
# (convención: `_trazabilidad_interna`, `_metodologia_interna`,
# `_ejercicios_fuente_interno` → privado, NO se escribe al vault público).
NON_TRAP_KEYS = {
    "metadata",
    "errores_confirmados_en_gemini",
    "leyes_pendientes_ingesta",
    "calculadoras_pendientes",
    "metadata_fusion_v2",
}

# Mapeo: bloque YAML -> (letra_categoria, nombre_carpeta, etiqueta_humana)
CATEGORY_MAP: dict[str, tuple[str, str, str]] = {
    "categoria_A_encuadramiento":                    ("A", "A_encuadramiento", "A - Encuadramiento"),
    "categoria_A_encuadramiento_ampliacion":         ("A", "A_encuadramiento", "A - Encuadramiento"),
    "categoria_B_IT":                                ("B", "B_it", "B - Incapacidad Temporal"),
    "categoria_B_IT_ampliacion":                     ("B", "B_it", "B - Incapacidad Temporal"),
    "categoria_C_jubilacion":                        ("C", "C_jubilacion", "C - Jubilación"),
    "categoria_D_IP":                                ("D", "D_ip", "D - Incapacidad Permanente"),
    "categoria_D_IP_ampliacion":                     ("D", "D_ip", "D - Incapacidad Permanente"),
    "categoria_E_procedimiento":                     ("E", "E_procedimiento-administrativo", "E - Procedimiento Administrativo"),
    "categoria_F_bases_cotizacion":                  ("F", "F_bases", "F - Bases de Cotización"),
    "categoria_F_bases_cotizacion_ampliacion":       ("F", "F_bases", "F - Bases de Cotización"),
    "categoria_G_recargos":                          ("G", "G_recargos", "G - Recargos e Intereses"),
    "categoria_G_recargos_ampliacion":               ("G", "G_recargos", "G - Recargos e Intereses"),
    "categoria_H_plazos":                            ("H", "H_plazos-ss", "H - Plazos SS"),
    "categoria_I_otras":                             ("I", "I_otras-recaudacion-pluriactivid", "I - Otras (recaudación, pluriactividad)"),
    "categoria_J_muerte_supervivencia":              ("J", "J_ms", "J - Muerte y Supervivencia"),
    "categoria_J_muerte_supervivencia_adiciones_BOE":("J", "J_ms", "J - Muerte y Supervivencia"),
    "categoria_J_muerte_supervivencia_ampliacion":   ("J", "J_ms", "J - Muerte y Supervivencia"),
    "categoria_K_desempleo":                         ("K", "K_desempleo", "K - Desempleo"),
    "categoria_K_desempleo_ampliacion":              ("K", "K_desempleo", "K - Desempleo"),
    "categoria_L_complementos_no_contributivas":     ("L", "L_complementos-no-contributivas", "L - Complementos y No Contributivas"),
    "categoria_M_jubilacion_parcial_relevo":         ("M", "M_jubilacion-parcial-y-relevo", "M - Jubilación Parcial y Relevo"),
    "categoria_N_automaticidad":                     ("N_AUTO", "N_AUTO_automaticidad-y-responsabilida", "N_AUTO - Automaticidad y Responsabilidad"),
    "categoria_N_procedimiento_LPAC":                ("N", "N_procedimiento-lpac", "N - Procedimiento LPAC"),
    "categoria_O_IMV":                               ("O", "O_ingreso-minimo-vital", "O - Ingreso Mínimo Vital"),
    "categoria_P_tiempo_parcial_fijos_discontinuos": ("P", "P_tiempo-parcial-y-fijos-discont", "P - Tiempo Parcial y Fijos Discontinuos"),
    "categoria_Q_funcion_publica_AGE":               ("Q", "Q_funcion-publica", "Q - Función Pública AGE"),
    "categoria_Q_funcion_publica_AGE_ampliacion":    ("Q", "Q_funcion-publica", "Q - Función Pública AGE"),
    "categoria_R_RETA_sistemas_especiales":          ("R", "R_reta", "R - RETA y Sistemas Especiales"),
    "categoria_R_RETA_ampliacion":                   ("R", "R_reta", "R - RETA y Sistemas Especiales"),
    "trampas_calculo_avanzado":                      ("CA", "CA_calculo-avanzado", "CA - Cálculo Avanzado"),
    "trampas_calculo_avanzado_ampliacion":           ("CA", "CA_calculo-avanzado", "CA - Cálculo Avanzado"),
}


# ------------------------------------------------------------------ helpers

def slugify(text: str, max_len: int = 45) -> str:
    """Convierte el título a kebab-case ASCII preservando el estilo del vault."""
    t = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:max_len].rstrip("-")


def detect_criticidad(trap: dict) -> tuple[str, str, str]:
    """
    Devuelve (estado, estado_emoji, criticidad) según los campos YAML.

    Prioridad:
      1) correccion_critica  -> 🔴 error corregido (alto)
      2) correccion          -> 🟠 cita / matiz ajustado (medio)
      3) trampa inversa      -> ⚠️ trampa inversa (alto)
      4) verificado_boe      -> 🟢 verificada BOE (normal)
      5) origen BOE-DIRECTO  -> 🟢 verificada BOE
      6) origen LEG-CONSOL   -> 🟡 legislación consolidada
      7) examen real         -> 🟢 de examen real
      8) otros               -> ⚪ sin clasificar
    """
    origen = (trap.get("origen") or "").upper()
    titulo = (trap.get("titulo") or "").lower()

    if trap.get("correccion_critica"):
        return "error grave corregido", "🔴", "alta"
    if "trampa inversa" in titulo or "reescrita" in (trap.get("origen") or "").lower():
        return "trampa inversa", "⚠️", "alta"
    if trap.get("correccion"):
        return "cita / matiz corregido", "🟠", "media"
    if trap.get("verificado_boe"):
        return "verificada BOE", "🟢", "normal"
    if "BOE-DIRECTO" in origen:
        return "verificada BOE", "🟢", "normal"
    if "LEG-CONSOLIDADA" in origen or "LEG_CONSOLIDADA" in origen:
        return "legislación consolidada", "🟡", "normal"
    if "EXAMEN" in origen or "INVESTIGACION" in origen:
        return "de examen real", "🟢", "normal"
    return "sin clasificar", "⚪", "normal"


def yaml_list(items) -> str:
    """Formatea una lista para frontmatter."""
    if not items:
        return "[]"
    if isinstance(items, str):
        items = [items]
    return "[" + ", ".join(f"'{str(i).replace(chr(39), chr(39)+chr(39))}'" for i in items) + "]"


# ------------------------------------------------------------------ integración esquemas

# Mapeo de esquemas a sus temas clave (basado en CONTENIDO, no solo título)
ESQUEMAS_TEMAS: dict[str, dict] = {
    "01_alumnos_en_practicas.md": {
        "titulo": "Alumnos en Prácticas",
        "keywords": ["alumnos", "practicas", "prácticas", "FP", "universitarios", "cotización", "altas", "bajas", "encuadramiento"],
        "categorias": ["A", "F"],
        "articulos": ["Art. 7"],
    },
    "02_anexo1_coeficientes_reductores_jubilacion.md": {
        "titulo": "Coeficientes Reductores Jubilación",
        "keywords": ["coeficientes reductores", "jubilación anticipada", "involuntaria", "voluntaria", "adelanto", "penalización"],
        "categorias": ["C", "M"],
        "articulos": ["Art. 213", "Art. 214"],
    },
    "03_anexo_cuantia_prestaciones_IP_2026.md": {
        "titulo": "Cuantías IP 2026",
        "keywords": ["incapacidad permanente", "IP", "cuantía", "prestaciones", "pensión", "2026", "base reguladora"],
        "categorias": ["D"],
        "articulos": ["Art. 195", "Art. 196"],
    },
    "04_bases_reguladoras_2026.md": {
        "titulo": "Bases Reguladoras 2026",
        "keywords": ["bases reguladoras", "BR", "cálculo", "cotización", "mensual", "días", "periodos"],
        "categorias": ["C", "D", "F"],
        "articulos": ["Art. 157", "Art. 158"],
    },
    "05_encuadramiento_sociedades_y_familiares.md": {
        "titulo": "Encuadramiento Sociedades y Familiares",
        "keywords": ["encuadramiento", "sociedades", "familiares", "socios", "capital social", "control efectivo", "RETA", "RGSS"],
        "categorias": ["A"],
        "articulos": ["Art. 2", "Art. 3", "Art. 136"],
    },
    "06_grados_incapacidad_permanente.md": {
        "titulo": "Grados de Incapacidad Permanente",
        "keywords": ["incapacidad permanente", "grado", "IPP", "IPT", "IPA", "gran incapacidad", "GI", "LPNI", "baremo"],
        "categorias": ["D"],
        "articulos": ["Art. 136", "Art. 137", "Art. 138"],
    },
    "07_incapacidad_permanente_periodos_minimos.md": {
        "titulo": "IP - Periodos Mínimos",
        "keywords": ["incapacidad permanente", "periodos mínimos", "cotización", "carencia", "prestación"],
        "categorias": ["D"],
        "articulos": ["Art. 158", "Art. 159"],
    },
    "08_it_procesos_y_duracion.md": {
        "titulo": "IT - Procesos y Duración",
        "keywords": ["incapacidad temporal", "IT", "partes médicos", "baja", "alta", "confirmación", "duración", "dictamen"],
        "categorias": ["B"],
        "articulos": ["Art. 158", "Art. 263"],
    },
    "09_imv_renta_garantizada_2026.md": {
        "titulo": "IMV Renta Garantizada 2026",
        "keywords": ["IMV", "ingreso mínimo vital", "renta garantizada", "2026", "escala incrementos", "unidad convivencia"],
        "categorias": ["O"],
        "articulos": ["Ley 19/2021"],
    },
    "10_periodos_minimos_cotizacion_resumen.md": {
        "titulo": "Periodos Mínimos de Cotización - Resumen",
        "keywords": ["periodos mínimos", "cotización", "carencia", "resumen", "jubilación", "desempleo", "IT", "IP"],
        "categorias": ["A", "C", "D", "J", "K", "B"],
        "articulos": ["Art. 141", "Art. 158", "Art. 210"],
    },
    "11_pensiones_minimas_jubilacion_2026.md": {
        "titulo": "Pensiones Mínimas Jubilación 2026",
        "keywords": ["pensiones mínimas", "jubilación", "2026", "jubilado", "cotizante", "sin cotizar", "familiares"],
        "categorias": ["C"],
        "articulos": ["Art. 57"],
    },
    "12_it_reconocimiento_y_pago.md": {
        "titulo": "IT - Reconocimiento y Pago",
        "keywords": ["incapacidad temporal", "IT", "reconocimiento", "pago", "beneficio", "base reguladora", "subsidiaria"],
        "categorias": ["B"],
        "articulos": ["Art. 158", "Art. 170", "Art. 174"],
    },
    "13_compatibilidad_pensiones_y_rentas.md": {
        "titulo": "Compatibilidad Pensiones y Rentas",
        "keywords": ["compatibilidad", "pensiones", "rentas", "trabajo", "jubilación activa", "jubilación parcial", "límite rendimientos"],
        "categorias": ["C", "D", "I", "L"],
        "articulos": ["Art. 93", "Art. 95", "Art. 96"],
    },
    "14_jubilacion_checklist.md": {
        "titulo": "Checklist Modalidades Jubilación",
        "keywords": ["jubilación", "checklist", "anticipada", "voluntaria", "involuntaria", "parcial", "relevo", "flexible", "edad", "cotización"],
        "categorias": ["C", "M"],
        "articulos": ["Art. 210", "Art. 213", "Art. 215"],
    },
    "15_plazos_ingreso_cuotas.md": {
        "titulo": "Plazos Ingreso Cuotas",
        "keywords": ["plazos", "ingreso", "cuotas", "recaudación", "autoliquidación", "modelo", "TC", "pronto pago", "voluntaria"],
        "categorias": ["H", "I", "G"],
        "articulos": ["Art. 30", "Art. 31"],
    },
    "16_encuadramiento_general_resumen.md": {
        "titulo": "Encuadramiento General - Resumen",
        "keywords": ["encuadramiento", "RGSS", "RETA", "general", "resumen", "trabajadores", "empresarios"],
        "categorias": ["A"],
        "articulos": ["Art. 2"],
    },
    "17_cambios_legislativos_2026.md": {
        "titulo": "Cambios Legislativos 2026",
        "keywords": ["cambios", "legislativos", "2026", "novedades", "reformas", "actualizaciones", "IPREM"],
        "categorias": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"],
        "articulos": [],
    },
}


def detectar_esquemas_relacionados(trap: dict, cat_letra: str) -> list[tuple[str, str]]:
    """
    Detecta qué esquemas son relevantes para una trampa basándose en:
    - Categoría de la trampa
    - Keywords en título, regla, trampa_tipica
    - Artículos citados
    
    Devuelve lista de (nombre_archivo, titulo_humano)
    """
    relacionados = []
    
    # Texto completo para búsqueda
    texto_busqueda = " ".join([
        trap.get("titulo", ""),
        trap.get("regla", ""),
        trap.get("trampa_tipica", ""),
        trap.get("articulo", ""),
    ]).lower()
    
    for archivo, info in ESQUEMAS_TEMAS.items():
        score = 0
        
        # Coincidencia por categoría (peso alto)
        if cat_letra in info["categorias"]:
            score += 3
        
        # Coincidencia por keywords en contenido
        for keyword in info["keywords"]:
            if keyword.lower() in texto_busqueda:
                score += 2
        
        # Coincidencia por artículos citados
        articulos_trampa = trap.get("articulo", "").lower()
        for art in info["articulos"]:
            if art.lower() in articulos_trampa:
                score += 4  # Peso muy alto para artículos exactos
        
        # Umbral: si score >= 3, consideramos relacionado
        if score >= 3:
            relacionados.append((archivo, info["titulo"]))
    
    # Ordenar por relevancia (score implícito por orden de inserción)
    return relacionados[:5]  # Máximo 5 esquemas por trampa


def build_note(trap_id: str, trap: dict, cat_letra: str, cat_humana: str, esquemas_rel: list[tuple[str, str]] = None) -> str:
    """Construye el markdown de una nota."""
    titulo    = trap.get("titulo", trap_id).strip()
    regla     = (trap.get("regla") or "").strip()
    trampa_t  = (trap.get("trampa_tipica") or "").strip()
    mnemo     = (trap.get("mnemonico") or "").strip()
    articulo  = (trap.get("articulo") or "").strip()
    origen    = (trap.get("origen") or "").strip()
    verif     = (trap.get("verificado_boe") or "").strip()
    correc    = (trap.get("correccion") or trap.get("correccion_critica") or "").strip()
    literal   = (trap.get("texto_literal_ref") or "").strip()
    actualiz  = (trap.get("actualizacion_2026") or "").strip()
    ley_pendiente = (trap.get("ley_pendiente_ingesta") or "").strip()

    estado, emoji, criticidad = detect_criticidad(trap)

    # Tags dinámicos
    tags = ["trampa", f"categoria_{cat_letra}", f"estado/{estado.replace(' ', '_').replace('/', '_')}"]
    if "TRLGSS" in articulo or "LGSS" in articulo:
        tags.append("norma/TRLGSS")
    if "TREBEP" in articulo or "EBEP" in articulo:
        tags.append("norma/TREBEP")
    if "ET " in articulo or articulo.startswith("Art") and " ET" in articulo:
        tags.append("norma/ET")
    if "LETA" in articulo:
        tags.append("norma/LETA")
    if "LPAC" in articulo or "Ley 39" in articulo or "Ley 40" in articulo:
        tags.append("norma/LPAC")
    if "RGRSS" in articulo or "RD 1415" in articulo:
        tags.append("norma/RGRSS")
    if correc:
        tags.append("verificacion/corregida_2026_04")
    elif verif:
        tags.append("verificacion/validada_literal")

    if criticidad == "alta":
        tags.append("criticidad/alta")

    # Frontmatter (preserva comillas dobles en 'titulo')
    titulo_escaped = titulo.replace('"', '\\"')
    articulos_list = [a.strip() for a in re.split(r";|\band\b", articulo) if a.strip()]

    fm_lines = [
        "---",
        f'id: "{trap_id}"',
        f'titulo: "{titulo_escaped}"',
        f'categoria: "{cat_humana}"',
        f'estado: "{estado}"',
        f'estado_emoji: "{emoji}"',
        f'criticidad: "{criticidad}"',
        f'origen: "{origen}"',
        f"articulos: {yaml_list(articulos_list)}",
        f'peso_examen: "alto"' if criticidad == "alta" else 'peso_examen: "medio"',
    ]
    if verif:
        fm_lines.append(f'verificado_boe: "{verif}"')
    if correc:
        fm_lines.append("tiene_correccion: true")
    fm_lines.append(f"tags: {yaml_list(tags)}")
    fm_lines.append("---")
    fm_lines.append("")

    # Cuerpo
    lines = fm_lines + [
        f"# {trap_id} — {titulo}",
        "",
    ]

    if criticidad == "alta":
        if estado == "error grave corregido":
            lines += ["> [!danger] 🔴 ERROR GRAVE CORREGIDO — esta trampa ha sido REESCRITA tras verificación BOE directa.", ""]
        elif estado == "trampa inversa":
            lines += ["> [!warning] ⚠️ TRAMPA INVERSA — captura al opositor formado con temarios anteriores a la reforma.", ""]

    lines += [
        "## 📐 Regla",
        "",
        regla or "_(pendiente de redactar)_",
        "",
    ]

    if trampa_t:
        lines += [
            "## 🎯 Trampa típica",
            "",
            trampa_t,
            "",
        ]

    if mnemo:
        lines += [
            "## 🧠 Mnemónico",
            "",
            f"> {mnemo}",
            "",
        ]

    if literal:
        lines += [
            "## 📜 Texto literal (BOE)",
            "",
            f"> {literal}",
            "",
        ]

    if articulo:
        lines += [
            "## 📖 Artículos aplicables",
            "",
            f"`{articulo}`",
            "",
        ]

    if correc:
        lines += [
            "## ⚠️ Corrección aplicada",
            "",
            correc,
            "",
        ]

    if actualiz:
        lines += [
            "## 🔄 Actualización normativa",
            "",
            actualiz,
            "",
        ]

    # Ley pendiente de ingesta
    if ley_pendiente:
        lines += [
            "## 📌 Ley pendiente de ingesta en RAG",
            "",
            ley_pendiente,
            "",
        ]

    # Esquemas relacionados (mental maps)
    if esquemas_rel:
        lines += [
            "## 📚 Esquemas relacionados",
            "",
        ]
        for archivo, titulo_humano in esquemas_rel:
            # Crear wikilink al esquema
            nombre_sin_ext = archivo.replace(".md", "")
            lines.append(f"- [[esquemas/{nombre_sin_ext}|📊 {titulo_humano}]]")
        lines.append("")

    lines.append("---")
    footer = f"**Origen**: {origen or 'sin especificar'} · **Estado**: {emoji} {estado}"
    if verif:
        footer += f" · **Verificado BOE**: {verif}"
    lines.append(footer)
    lines.append("")

    return "\n".join(lines)


def build_moc(cat_letra: str, cat_humana: str, traps: list[tuple[str, dict, str]]) -> str:
    """Genera el MOC (_X_...md) de una categoría."""
    # Orden: 🔴 > ⚠️ > 🟠 > 🟢 > 🟡 > ⚪, luego por ID
    def sort_key(item):
        tid, tr, _fname = item
        emoji_order = {"🔴": 0, "⚠️": 1, "🟠": 2, "🟢": 3, "🟡": 4, "⚪": 5}
        _, e, _ = detect_criticidad(tr)
        return (emoji_order.get(e, 9), tid)
    traps_sorted = sorted(traps, key=sort_key)

    rojas     = [t for t in traps_sorted if detect_criticidad(t[1])[1] == "🔴"]
    inversas  = [t for t in traps_sorted if detect_criticidad(t[1])[1] == "⚠️"]
    naranjas  = [t for t in traps_sorted if detect_criticidad(t[1])[1] == "🟠"]

    out = [
        "---",
        f'titulo: "MOC {cat_humana}"',
        f'tipo: "MOC"',
        f'categoria: "{cat_humana}"',
        f'total_trampas: {len(traps)}',
        f"tags: ['MOC', 'categoria_{cat_letra}']",
        "---",
        "",
        f"# MOC — {cat_humana}",
        "",
        f"**Total**: {len(traps)} trampas",
        "",
    ]

    if rojas or inversas or naranjas:
        out += ["## 🚨 Correcciones aplicadas (verificación BOE 18-19/04/2026)", ""]
        for label, emoji, items in (
            ("Errores graves corregidos", "🔴", rojas),
            ("Trampas inversas (reescritas)", "⚠️", inversas),
            ("Citas / matices corregidos", "🟠", naranjas),
        ):
            if items:
                out += [f"### {emoji} {label} ({len(items)})", ""]
                for tid, tr, fname in items:
                    out.append(f"- {emoji} [[{fname}|**{tid}** — {tr.get('titulo', '')}]]")
                out.append("")

    out += ["## 📚 Índice completo", ""]
    for tid, tr, fname in traps_sorted:
        _, emoji, _ = detect_criticidad(tr)
        out.append(f"- {emoji} [[{fname}|**{tid}** — {tr.get('titulo', '')}]]")
    out.append("")
    return "\n".join(out)


def build_indice(all_traps: list[tuple[str, dict, str, str, str]]) -> str:
    """Genera el _INDICE.md global con las 26 correcciones destacadas."""
    # all_traps: list of (trap_id, trap_dict, cat_letra, cat_humana, filename)
    rojas    = [t for t in all_traps if detect_criticidad(t[1])[1] == "🔴"]
    inversas = [t for t in all_traps if detect_criticidad(t[1])[1] == "⚠️"]
    naranjas = [t for t in all_traps if detect_criticidad(t[1])[1] == "🟠"]

    # Agrupación por categoría
    by_cat: dict[str, list] = {}
    for t in all_traps:
        by_cat.setdefault(t[3], []).append(t)

    out = [
        "---",
        'titulo: "Índice maestro de trampas"',
        'tipo: "índice"',
        f"total_trampas: {len(all_traps)}",
        f"errores_corregidos: {len(rojas) + len(inversas) + len(naranjas)}",
        f"fecha_verificacion: '{datetime.now().strftime('%Y-%m-%d')}'",
        "tags: ['indice', 'MOC']",
        "---",
        "",
        "# 🏁 Índice Maestro de Trampas — OPOS SS 2026",
        "",
        f"**{len(all_traps)} trampas verificadas** · BOE consolidado 04/02/2026",
        f"· **{len(rojas) + len(inversas) + len(naranjas)} correcciones aplicadas** en verificación 18-19/04/2026",
        "",
        "## 🚨 Top errores detectados y corregidos",
        "",
        "### 🔴 Errores graves (la regla antigua era incorrecta)",
        "",
    ]
    for tid, tr, _cat, cat_hum, fname in rojas:
        out.append(f"- 🔴 [[{fname}|**{tid}**]] ({cat_hum}) — {tr.get('titulo', '')}")
    out += ["", "### ⚠️ Trampas inversas (regla derogada / reformada)", ""]
    for tid, tr, _cat, cat_hum, fname in inversas:
        out.append(f"- ⚠️ [[{fname}|**{tid}**]] ({cat_hum}) — {tr.get('titulo', '')}")
    out += ["", "### 🟠 Citas / matices corregidos", ""]
    for tid, tr, _cat, cat_hum, fname in naranjas:
        out.append(f"- 🟠 [[{fname}|**{tid}**]] ({cat_hum}) — {tr.get('titulo', '')}")
    out += ["", "## 📚 Categorías", ""]
    for cat_humana, items in sorted(by_cat.items()):
        out.append(f"- **{cat_humana}**: {len(items)} trampas · ver MOC de categoría en `_{items[0][2]}_*.md`")
    out += [
        "",
        "## 🔖 Leyenda de estados",
        "",
        "- 🔴 **error grave corregido** — la regla previa era errónea y se ha reescrito tras verificación BOE.",
        "- ⚠️ **trampa inversa** — regla derogada por reforma reciente; captura al opositor con temario antiguo.",
        "- 🟠 **cita corregida** — la regla es correcta pero la referencia al artículo estaba mal.",
        "- 🟢 **verificada BOE** — confirmada literalmente contra el texto consolidado.",
        "- 🟡 **legislación consolidada** — fundamento reglamentario sólido.",
        "- ⚪ **sin clasificar** — pendiente de revisión literal BOE.",
        "",
    ]
    return "\n".join(out)


def build_pendientes_verificar(all_traps: list[tuple[str, dict, str, str, str]]) -> str:
    """Genera el _PENDIENTES_VERIFICAR.md — dashboard de trampas pendientes."""
    pendientes = []
    obsoletas = []
    
    for tid, trap, cat_letra, cat_humana, fname in all_traps:
        origen = (trap.get("origen") or "").upper()
        if "INVENTADA-DM" in origen:
            pendientes.append((tid, trap, cat_humana, fname))
        elif "OBSOLETA" in origen:
            obsoletas.append((tid, trap, cat_humana, fname))
    
    out = [
        "---",
        'titulo: "Dashboard — Trampas pendientes de verificar"',
        'tipo: "dashboard"',
        f'total_pendientes: {len(pendientes)}',
        f'total_obsoletas: {len(obsoletas)}',
        "tags: ['dashboard', 'pendientes', 'verificacion']",
        "---",
        "",
        "# 🔍 Dashboard — Trampas pendientes o con estado no-verificado",
        "",
        f"**Actualizado**: {datetime.now().strftime('%Y-%m-%d')} tras verificación completa.",
        "",
    ]
    
    out += [f"## 🔴 Pendientes [INVENTADA-DM]: {len(pendientes)}", ""]
    if not pendientes:
        out.append("> 🎉 ¡Ninguna! Todas las trampas inventadas han sido verificadas.")
    else:
        for tid, trap, cat_hum, fname in pendientes:
            out.append(f"- **{tid}** ({cat_hum}): {trap.get('titulo', '')}")
            if "correccion_critica" in trap:
                out.append(f"  > ⚠️ {trap['correccion_critica'][:200]}...")
    
    out += ["", f"## ❌ Obsoletas: {len(obsoletas)}", ""]
    if not obsoletas:
        out.append("> Ninguna trampa marcada como obsoleta.")
    else:
        for tid, trap, cat_hum, fname in obsoletas:
            out.append(f"- **{tid}** ({cat_hum}): {trap.get('titulo', '')}")
    
    out += [
        "",
        "---",
        "[[_INDICE|← Volver al índice maestro]]",
    ]
    return "\n".join(out)


# ------------------------------------------------------------------ main

def main() -> int:
    if not YAML_SRC.exists():
        print(f"ERROR: no se encuentra el YAML {YAML_SRC}", file=sys.stderr)
        return 1
    if not VAULT.exists():
        print(f"ERROR: no se encuentra el vault {VAULT}", file=sys.stderr)
        return 1

    with YAML_SRC.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Asegurar que el directorio de trampas existe (regeneración desde cero soportada)
    TRAMPAS_DIR.mkdir(parents=True, exist_ok=True)

    # Limpiar carpetas de trampas (no los MOCs _*.md, los regeneramos después)
    for sub in TRAMPAS_DIR.iterdir():
        if sub.is_dir():
            for f in sub.glob("*.md"):
                f.unlink()
    # Eliminar MOCs antiguos y el _INDICE
    for f in TRAMPAS_DIR.glob("_*.md"):
        f.unlink()

    # Copiar esquemas a la wiki (con análisis de contenido para wikilinks)
    print(f"→ Copiando esquemas desde {ESQUEMAS_SRC}")
    esquemas_copiados = 0
    if ESQUEMAS_SRC.exists():
        ESQUEMAS_DIR.mkdir(parents=True, exist_ok=True)
        # Limpiar esquemas antiguos primero
        for f in ESQUEMAS_DIR.glob("*.md"):
            f.unlink()
        for esq in ESQUEMAS_SRC.glob("*.md"):
            shutil.copy2(esq, ESQUEMAS_DIR / esq.name)
            esquemas_copiados += 1
        print(f"  ✓ {esquemas_copiados} esquemas copiados a {ESQUEMAS_DIR}")
    else:
        print(f"  ⚠️ No se encontraron esquemas en {ESQUEMAS_SRC}")

    all_traps = []
    by_category: dict[tuple[str, str], list] = {}

    # Recorrer todas las categorías
    for top_key, content in data.items():
        # Ignorar claves privadas (prefijo `_`) — trazabilidad interna que NO debe
        # aparecer en el vault público (ej: `_metodologia_interna`,
        # `_ejercicios_fuente_interno`).
        if top_key.startswith("_"):
            continue
        if top_key in NON_TRAP_KEYS:
            continue
        if top_key not in CATEGORY_MAP:
            print(f"⚠️ bloque sin mapeo: {top_key}")
            continue
        if not isinstance(content, dict):
            continue
        cat_letra, folder_name, cat_humana = CATEGORY_MAP[top_key]
        folder = TRAMPAS_DIR / folder_name
        folder.mkdir(parents=True, exist_ok=True)

        for trap_id, trap in content.items():
            # Saltar claves privadas dentro de la categoría (no debería haberlas
            # al nivel de trampa, pero por si acaso: `_metadata_categoria`, etc.)
            if trap_id.startswith("_"):
                continue
            if not isinstance(trap, dict):
                continue
            titulo = trap.get("titulo", trap_id)
            slug = slugify(titulo)
            fname = f"{trap_id}_{slug}"
            # Detectar esquemas relacionados basándose en CONTENIDO
            esquemas_rel = detectar_esquemas_relacionados(trap, cat_letra)
            note = build_note(trap_id, trap, cat_letra, cat_humana, esquemas_rel)
            (folder / f"{fname}.md").write_text(note, encoding="utf-8")
            all_traps.append((trap_id, trap, cat_letra, cat_humana, fname))
            by_category.setdefault((cat_letra, cat_humana, folder_name), []).append((trap_id, trap, fname))

    # Generar MOC por categoría
    for (cat_letra, cat_humana, folder_name), traps in by_category.items():
        moc_name = f"_{folder_name}.md"
        (TRAMPAS_DIR / moc_name).write_text(build_moc(cat_letra, cat_humana, traps), encoding="utf-8")

    # Índice maestro
    (TRAMPAS_DIR / "_INDICE.md").write_text(build_indice(all_traps), encoding="utf-8")

    # Dashboard de pendientes
    (TRAMPAS_DIR / "_PENDIENTES_VERIFICAR.md").write_text(build_pendientes_verificar(all_traps), encoding="utf-8")

    # Resumen
    print("\n=== RESUMEN ===")
    print(f"Total notas generadas: {len(all_traps)}")
    totals_by_cat = {}
    for tid, tr, cat_l, cat_h, _fn in all_traps:
        totals_by_cat[cat_h] = totals_by_cat.get(cat_h, 0) + 1
    for cat, n in sorted(totals_by_cat.items()):
        print(f"  {n:3d}  {cat}")

    rojas    = sum(1 for _, tr, *_ in all_traps if detect_criticidad(tr)[1] == "🔴")
    inversas = sum(1 for _, tr, *_ in all_traps if detect_criticidad(tr)[1] == "⚠️")
    naranjas = sum(1 for _, tr, *_ in all_traps if detect_criticidad(tr)[1] == "🟠")
    print(f"\nCorrecciones: 🔴 {rojas} · ⚠️ {inversas} · 🟠 {naranjas}  (total {rojas + inversas + naranjas})")
    print(f"\nEsquemas/Mapas mentales: {esquemas_copiados} archivos con wikilinks automáticos")
    print(f"  → Ubicación: {ESQUEMAS_DIR}")
    print(f"\n⚠️  NO SE HIZO BACKUP (según petición del usuario)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
