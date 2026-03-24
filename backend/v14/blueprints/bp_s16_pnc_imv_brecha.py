"""
OpositAIA V14 — Blueprint BP-S16
Tema: PNC + IMV + Complemento brecha de género
Temas oficiales: TE12 — Prestaciones no contributivas + IMV
Fuente: Arts. 363-376 TRLGSS; Art. 60 TRLGSS; Ley 19/2021

⚠️ CAMBIOS DM 2026 INCORPORADOS:
  - DM26-T10-02: Complemento brecha género 34,80€ → 36,90€ (al progenitor con pensión más baja)
  - DM26-T10-03: PNC mín 628,80€/mes; Máx contrib 3.359,60€/mes
"""
import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
from v14.schemas import TopicBlueprint
from v14.cambios_dm_2026 import get_cambios_para_blueprint, JUBILACION_2026

_j = JUBILACION_2026

BP_S16 = TopicBlueprint(
    id="BP-S16",
    tema="PNC + IMV + Complemento brecha de género 2026",
    temas_oficiales=["TE12"],
    normativa_base=[
        "Arts. 363-376 TRLGSS — Prestaciones no contributivas SS",
        "Art. 60 TRLGSS — Complemento brecha de género",
        "Ley 19/2021 — Ingreso Mínimo Vital",
        "RD límites revalorización pensiones 2026",
    ],

    articulos_obligatorios=[
        "Art. 369 TRLGSS",  # Jubilación NC — 10 años residencia
        "Art. 60 TRLGSS",   # Complemento brecha de género
        "Art. 363 TRLGSS",  # Invalidez NC — ≥65% discapacidad
    ],
    articulos_forbidden=[
        "Art. 60 bis",  # No existe
        "Art. 376 bis", # No existe
    ],

    calculadoras=[
        "complemento_brecha_genero(pension_progenitor_1, pension_progenitor_2)",
        "pnc_jubilacion(ingresos, residencia_anios)",
        "imv_compatible(ingresos_unidad, num_miembros)",
    ],

    trampas_tipicas=[
        "DM26-T10-02",  # Complemento brecha: a quien tiene pensión más BAJA (no necesariamente la madre)
        "DM26-T10-03",  # Cuantías 2026: PNC mín 628,80€; Máx contrib 3.359,60€
        "C30",          # PNC jubilación: 10 años residencia (no 5)
        "C31",          # Invalidez NC: ≥65% discapacidad (no 33%)
        "C32",          # IMV + administrador de SL: incompatible
        "C33",          # Complemento brecha: naturaleza CONTRIBUTIVA (no no contributiva)
    ],

    cambios_dm_2026=get_cambios_para_blueprint("BP-S16"),

    eval_questions=[
        {
            "pregunta": "En 2026, el complemento por brecha de género (Art. 60 TRLGSS) es de:",
            "respuesta_correcta": f"{_j['complemento_brecha_genero']['cuantia_2026']}€/mes, reconocido al progenitor que tenga la pensión más baja de los dos",
            "distractores": [
                "34,80€/mes, siempre a la madre",
                "36,90€/mes, siempre a la madre",
                "36,90€/mes a ambos progenitores si ambos cobran pensión",
            ],
            "articulo": "Art. 60 TRLGSS",
            "trampa_id": "DM26-T10-02",
            "mnemonico": "Brecha 36.90€ (2026) al de pensión más baja — NO siempre a la madre",
        },
        {
            "pregunta": "La naturaleza jurídica del complemento por brecha de género (Art. 60.4 TRLGSS) es:",
            "respuesta_correcta": "CONTRIBUTIVA a todos los efectos",
            "distractores": [
                "No contributiva, por eso no computa para la base reguladora",
                "Asistencial, financiada íntegramente por el Estado",
                "Mixta — tiene carácter contributivo y no contributivo",
            ],
            "articulo": "Art. 60.4 TRLGSS",
            "trampa_id": "C33",
            "mnemonico": "Complemento brecha: CONTRIBUTIVO aunque parezca asistencial. Art 60.4.",
        },
        {
            "pregunta": f"La cuantía mínima de la pensión no contributiva en 2026 es:",
            "respuesta_correcta": f"{_j['pension_min_nc_mensual']}€/mes × 14 pagas = {_j['pension_min_nc_anual']}€/año",
            "distractores": [
                "592,32€/mes",
                "628,80€/mes × 12 pagas",
                "600€/mes",
            ],
            "articulo": "RD revalorización pensiones 2026",
            "trampa_id": "DM26-T10-03",
            "mnemonico": "PNC mín 2026: 628,80 × 14 pagas = 8.803,20€/año. No 12 pagas.",
        },
        {
            "pregunta": "Para acceder a la pensión no contributiva de jubilación, el requisito de residencia es:",
            "respuesta_correcta": "10 años de residencia legal en territorio español, de los cuales 2 de forma inmediata anterior a la solicitud",
            "distractores": [
                "5 años de residencia",
                "10 años continuos inmediatamente anteriores a la solicitud",
                "Residencia mínima de 1 año antes de cumplir los 65 años",
            ],
            "articulo": "Art. 369.1 TRLGSS",
            "trampa_id": "C30",
            "mnemonico": "PNC jubilación: 10 años residencia (2 inmediatos). No son 5 años.",
        },
        {
            "pregunta": "El Ingreso Mínimo Vital es incompatible con:",
            "respuesta_correcta": "Ser administrador de una sociedad de capital (SL, SA) con retribución o con control del 50%+",
            "distractores": [
                "Ser trabajador por cuenta ajena a tiempo parcial",
                "Cobrar una pensión de viudedad",
                "Tener una pensión no contributiva inferior al umbral de renta",
            ],
            "articulo": "Art. 11 Ley 19/2021",
            "trampa_id": "C32",
            "mnemonico": "IMV incompatible con administrador SL con retribución. Trampa clásica.",
        },
    ],

    notas=(
        "SPRINT 0 — cambios DM 2026 incorporados el 22/03/2026: "
        "complemento brecha 36,90€ (no 34,80€) y cuantías PNC actualizadas. "
        "TRAMPA CRÍTICA: el complemento brecha es para quien tiene la pensión MÁS BAJA, "
        "no necesariamente la madre. Su naturaleza es CONTRIBUTIVA (Art. 60.4 TRLGSS)."
    ),
)
