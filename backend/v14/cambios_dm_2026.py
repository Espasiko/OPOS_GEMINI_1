"""
OpositAIA V14 — Cambios Legislativos DM 2026
Fuente: Esquema-Resumen DM (ESQUEMA_RESUMEN_CAMBIOS_LEGISLATIVOS_BLOQUE_ESPECÍFICO_DM.pdf)
Fecha de corte normativa: 2026-03-04

Este módulo es la FUENTE DE VERDAD para los cambios DM 2026.
Al llegar un nuevo temario, SOLO se actualizan los campos que cambian aquí
y los blueprints los leen de este módulo automáticamente (sin duplicar datos).
"""

# ─── DATOS VERIFICADOS 2026 (BOE + DM) ─────────────────────────────────────

# TEMA 4 — COTIZACIÓN
MEI_2025 = 0.80    # % anterior
MEI_2026 = 0.90    # % correcto para el examen 2026
MEI_EMPRESA_2026 = 0.75
MEI_TRABAJADOR_2026 = 0.15

BASE_MAXIMA_CC_2025 = 4909.50   # €/mes
BASE_MAXIMA_CC_2026 = 5101.20   # €/mes — sube en 2026

# Adicional de Solidaridad 2026 (NUEVO — no existía en 2025)
SOLIDARIDAD_2026 = {
    "tramo_1": {
        "descripcion": "Retribución entre base máxima y +10% (5.101,20€ – 5.611,32€)",
        "total_pct": 1.15,
        "empresa_pct": 0.96,
        "trabajador_pct": 0.19,
        "limite_inferior": 5101.20,
        "limite_superior": 5611.32,
    },
    "tramo_2": {
        "descripcion": "Retribución entre +10% y +50% sobre base máxima (5.611,32€ – 7.651,80€)",
        "total_pct": 1.25,
        "empresa_pct": 1.04,
        "trabajador_pct": 0.21,
        "limite_inferior": 5611.32,
        "limite_superior": 7651.80,
    },
    "tramo_3": {
        "descripcion": "Retribución que supera el +50% sobre base máxima (>7.651,80€)",
        "total_pct": 1.46,
        "empresa_pct": 1.22,
        "trabajador_pct": 0.24,
        "limite_inferior": 7651.80,
        "limite_superior": None,  # sin techo
    },
}

# TEMA 8 — INCAPACIDAD PERMANENTE
GRAN_INCAPACIDAD_2026 = {
    "nombre_anterior": "Gran Invalidez",
    "nombre_nuevo": "Gran Incapacidad",  # Cambio de denominación
    "extincion_automatica": False,        # FALSO — trampa clave de examen
    "protocolo_empresa": [
        "1. Adaptar el puesto de trabajo",
        "2. Si no puede adaptar → reubicar en puesto vacante compatible",
        "3. Solo si nada es posible (empresa lo demuestra) → posible extinción",
    ],
    "articulo": "Ley 15/2022 (modificación TRLGSS) — en vigor 2026",
    "trampa_examen": "El contrato se extingue automáticamente al reconocerse la Gran Incapacidad → FALSO",
}

# TEMA 9 — NACIMIENTO Y CUIDADO DEL MENOR
NACIMIENTO_2026 = {
    "semanas_madre": 19,          # antes 16
    "semanas_otro_progenitor": 19,  # antes 16 (equiparación total)
    "semanas_monoparental": 32,   # antes estaba restringido
    "semanas_obligatorias_parto": 6,   # jornada completa, inmediatas tras parto
    "semanas_flexibles_12m": 11,  # a jornada parcial o completa hasta 12 meses
    "semanas_monoparental_12m": 22,
    "semanas_hasta_8anios": 2,
    "semanas_monoparental_8anios": 4,
    "subsidio_nc_tambien_hombres": True,  # NUEVO 2026 — antes solo mujeres
    "subsidio_nc_descripcion": (
        "Trabajadores y trabajadoras afiliados en alta/asimilada que cumplan todos "
        "los requisitos para la prestación de nacimiento salvo el período mínimo de "
        "cotización. Cubre nacimiento y adopción."
    ),
    "trampa_examen": "El subsidio no contributivo de nacimiento solo es para mujeres → FALSO desde 2026",
}

# TEMA 10 — JUBILACIÓN
JUBILACION_2026 = {
    # Edad Ordinaria de Jubilación
    "eoj_65_anios": {"condicion": "≥ 38 años y 3 meses cotizados"},
    "eoj_ordinaria": {"condicion": "< 38a3m", "edad_anios": 66, "edad_meses": 10},

    # Base Reguladora DUAL (NUEVO 2026)
    "br_dual": {
        "descripcion": "Se calcula por DOS fórmulas y se elige la MÁS BENEFICIOSA",
        "opcion_1": {
            "nombre": "Fórmula tradicional (300 meses / divisor 350)",
            "bases_computadas": 300,
            "divisor": 350,
            "doctrina_parentesis": False,  # NO aplica
            "pagas_extraordinarias": False,  # NO se tienen en cuenta días-cuota
            "libre_eleccion_periodo": False,
        },
        "opcion_2": {
            "nombre": "Fórmula nueva (mejores 302 de las últimas 304 / divisor 352,33)",
            "bases_computadas": 302,
            "de_las_ultimas": 304,
            "divisor": 352.33,
            "doctrina_parentesis": True,   # puede aplicar
            "pagas_extraordinarias": True,  # incluye días-cuota
            "libre_eleccion_periodo": False,  # TRAMPA: no hay libre elección
        },
        "trampa_examen": "El trabajador elige libremente cualquier período para la BR → FALSO (solo entre las 2 fórmulas)",
    },

    # Umbral 100% pensión (DT 9ª TRLGSS)
    "umbral_100pct_pension": {"anios": 36, "meses": 6},
    "umbral_100pct_nombre": "36 años y 6 meses (Disposición Transitoria 9ª)",

    # Límites pensiones 2026
    "pension_max_contributiva_mensual": 3359.60,   # €/mes
    "pension_max_contributiva_anual": 47034.40,    # € 14 pagas
    "pension_min_nc_mensual": 628.80,              # €/mes
    "pension_min_nc_anual": 8803.20,               # € 14 pagas

    # Complemento brecha de género
    "complemento_brecha_genero": {
        "cuantia_2025": 34.80,       # € anterior
        "cuantia_2026": 36.90,       # € correcto para el examen
        "titular": "progenitor con la PENSIÓN MÁS BAJA (no necesariamente la madre)",
        "naturaleza": "CONTRIBUTIVA a todos los efectos (Art. 60.4 TRLGSS)",
        "trampa_examen": [
            "Decir que el complemento es siempre para la madre → FALSO (es para quien tiene la pensión más baja)",
            "Usar la cuantía 2025 (34,80€) → en 2026 son 36,90€",
        ],
    },
}

# ─── REGISTRO OFICIAL DE CAMBIOS DM 2026 ───────────────────────────────────
# Lista usada para:
# 1. Generar los campos `cambios_dm_2026` de los blueprints
# 2. Añadir deltas cuando llegue nuevo temario (solo añadir entradas aquí)
# 3. Generar las trampas nuevas del catálogo

CAMBIOS_DM_2026 = [
    {
        "id": "DM26-T4-01",
        "tema": "T4",
        "concepto": "MEI — Mecanismo de Equidad Intergeneracional",
        "blueprint": "BP-S05",
        "campo": "mei_pct",
        "valor_2025": "0,80%",
        "valor_2026": "0,90% (empresa 0,75% + trabajador 0,15%)",
        "trampa": "Usar el 0,80% del año anterior o repartir de forma incorrecta empresa/trabajador",
        "mnemonico": "MEI sube a 0,90 en 2026: empresa 0,75 más trab 0,15",
        "articulo": "Art. 19 bis TRLGSS + Orden PJC/178/2025",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2025-3524",
    },
    {
        "id": "DM26-T4-02",
        "tema": "T4",
        "concepto": "Adicional de Solidaridad — 3 tramos NUEVOS",
        "blueprint": "BP-S05",
        "campo": "adicional_solidaridad",
        "valor_2025": "No existía",
        "valor_2026": "3 tramos (1,15% / 1,25% / 1,46%) sobre retribución >base máxima",
        "trampa": "Confundir con el MEI (que va sobre BC normal) o con las cotizaciones comunes (28,30%)",
        "mnemonico": "Solidaridad aplica AL EXCESO sobre base máxima, en 3 tramos progresivos",
        "articulo": "Art. 19 ter TRLGSS (nuevo)",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2025-3524",
    },
    {
        "id": "DM26-T4-03",
        "tema": "T4",
        "concepto": "Base de cotización máxima",
        "blueprint": "BP-S05",
        "campo": "base_maxima_cc",
        "valor_2025": "4.909,50€/mes",
        "valor_2026": "5.101,20€/mes",
        "trampa": "Usar la base máxima de 2025 en cálculos de 2026",
        "mnemonico": "Base máxima 2026: 5.101,20 (sube aprox. +4%)",
        "articulo": "Orden PJC/178/2025",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2025-3524",
    },
    {
        "id": "DM26-T8-01",
        "tema": "T8",
        "concepto": "Gran Invalidez → Gran Incapacidad + Protocolo empresa",
        "blueprint": "BP-S10",
        "campo": "gran_incapacidad",
        "valor_2025": "Gran Invalidez — el contrato podía extinguirse al reconocerse",
        "valor_2026": "Gran Incapacidad — 3 pasos obligatorios (adaptar → reubicar → solo si imposible: extinguir)",
        "trampa": "El contrato se extingue automáticamente cuando se reconoce la Gran Incapacidad → FALSO",
        "mnemonico": "Gran Incapacidad: 3 pasos antes de extinguir. Sin pasos, sin extinción.",
        "articulo": "Ley 15/2022 (LO igualdad real) + TRLGSS mod.",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2022-11036",
    },
    {
        "id": "DM26-T9-01",
        "tema": "T9",
        "concepto": "Nacimiento y cuidado — 19 semanas + monoparental 32",
        "blueprint": "BP-S11",
        "campo": "semanas_nacimiento",
        "valor_2025": "16 semanas (ambos progenitores)",
        "valor_2026": "19 semanas (madre y otro progenitor); 32 semanas monoparental",
        "trampa": "Usar 16 semanas o no saber la distribución de las 19 (6+11+2)",
        "mnemonico": "19 semanas: 6 obligatorias + 11 hasta 12m + 2 hasta 8 años",
        "articulo": "Art. 177-190 TRLGSS (modificados)",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
    },
    {
        "id": "DM26-T9-02",
        "tema": "T9",
        "concepto": "Subsidio NC nacimiento — ahora también hombres",
        "blueprint": "BP-S11",
        "campo": "subsidio_nc_nacimiento",
        "valor_2025": "Solo para mujeres",
        "valor_2026": "Trabajadores y trabajadoras (ambos). Sin mínimo de cotización.",
        "trampa": "Decir que el subsidio no contributivo de nacimiento sigue siendo solo para mujeres",
        "mnemonico": "Subsidio NC nacimiento: también hombres desde 2026. Sin cotización mínima.",
        "articulo": "Art. 184 TRLGSS (modificado)",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
    },
    {
        "id": "DM26-T10-01",
        "tema": "T10",
        "concepto": "Base Reguladora DUAL jubilación",
        "blueprint": "BP-S12",
        "campo": "br_dual_jubilacion",
        "valor_2025": "Solo fórmula 300 bases / divisor 350",
        "valor_2026": "DOS fórmulas — se elige SIEMPRE la más beneficiosa: {300/350} o {mejores 302 de 304 / 352,33}",
        "trampa": "El trabajador elige libremente cualquier período para la BR → FALSO (solo entre las 2 fórmulas fijas)",
        "mnemonico": "BR dual: elige la mejor entre la vieja (350) y la nueva (302 de 304 / 352,33)",
        "articulo": "Art. 209 TRLGSS (modificado RDL 2/2023)",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
    },
    {
        "id": "DM26-T10-02",
        "tema": "T10",
        "concepto": "Complemento brecha de género — cuantía 2026",
        "blueprint": "BP-S16",
        "campo": "complemento_brecha_genero",
        "valor_2025": "34,80€/mes",
        "valor_2026": "36,90€/mes — al progenitor con la PENSIÓN MÁS BAJA",
        "trampa": "Usar 34,80€ (2025) o decir que siempre es para la madre",
        "mnemonico": "Brecha 36.90€ al de la pensión más baja — no siempre a la madre",
        "articulo": "Art. 60 TRLGSS",
        "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
    },
    {
        "id": "DM26-T10-03",
        "tema": "T10",
        "concepto": "PNC cuantías 2026 + pensión máxima contributiva",
        "blueprint": "BP-S16",
        "campo": "cuantias_pensiones_2026",
        "valor_2025": "PNC mín 592,32€/mes; Máx contrib 3.175,04€/mes",
        "valor_2026": "PNC mín 628,80€/mes (8.803,20€/año); Máx contrib 3.359,60€/mes (47.034,40€/año)",
        "trampa": "Usar las cuantías de 2025 en un caso fechado en 2026",
        "mnemonico": "PNC mín 2026: 628,80. Máx contrib: 3.359,60 × 14 = 47.034",
        "articulo": "RD límites revalorización 2026",
        "url_boe": "https://www.boe.es/boe/dias/2026/01/",
    },
]


def get_cambios_para_blueprint(blueprint_id: str) -> list:
    """Devuelve los cambios DM 2026 que aplican a un blueprint concreto."""
    return [c for c in CAMBIOS_DM_2026 if c["blueprint"] == blueprint_id]


def aplicar_delta_temario(nuevos_cambios: list) -> None:
    """
    Punto de entrada para añadir cambios de una NUEVA VERSIÓN del temario.
    Solo añade los cambios que no existan ya (por 'id').
    Llámalo cuando llegue una actualización del temario DM.

    Uso:
        from backend.v14.cambios_dm_2026 import aplicar_delta_temario
        aplicar_delta_temario([
            {
                "id": "DM26-T5-01",
                "tema": "T5",
                "concepto": "Nuevo cambio del nuevo temario",
                ...
            }
        ])
    """
    ids_existentes = {c["id"] for c in CAMBIOS_DM_2026}
    nuevos = [c for c in nuevos_cambios if c["id"] not in ids_existentes]
    if nuevos:
        CAMBIOS_DM_2026.extend(nuevos)
        print(f"✅ {len(nuevos)} nuevos cambios DM añadidos al registro.")
    else:
        print("ℹ️  Sin cambios nuevos — todos los IDs ya estaban registrados.")
