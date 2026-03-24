"""
OpositAIA V14 — Blueprint BP-S11
Tema: Nacimiento + cuidado del menor + riesgo durante embarazo
Temas oficiales: TE09
Fuente: Arts. 177-190 TRLGSS

⚠️ CAMBIOS DM 2026 INCORPORADOS:
  - DM26-T9-01: Nacimiento 19 semanas (antes 16); monoparental 32 semanas
  - DM26-T9-02: Subsidio NC nacimiento — ahora también hombres
"""
import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
from v14.schemas import TopicBlueprint
from v14.cambios_dm_2026 import get_cambios_para_blueprint, NACIMIENTO_2026

BP_S11 = TopicBlueprint(
    id="BP-S11",
    tema="Nacimiento y cuidado del menor 2026 (19 semanas + subsidio NC hombres)",
    temas_oficiales=["TE09"],
    normativa_base=[
        "Art. 177 TRLGSS — Prestación nacimiento y cuidado del menor",
        "Art. 178 TRLGSS — Situaciones protegidas",
        "Art. 179 TRLGSS — Beneficiarios",
        "Art. 182 TRLGSS — Duración",
        "Art. 184 TRLGSS — Subsidio no contributivo nacimiento",
        "Art. 186 TRLGSS — Riesgo durante embarazo",
        "Art. 188 TRLGSS — Riesgo durante lactancia",
        "Art. 237.3 TRLGSS — (aplica a nacimiento, NO a IT)",
    ],

    articulos_obligatorios=[
        "Art. 182 TRLGSS",
        "Art. 184 TRLGSS",
    ],
    articulos_forbidden=[
        "Art. 177 bis",  # No existe
        "Art. 237 TRLGSS (para IT)",  # Error clásico — el 237.3 es solo para nacimiento
    ],

    calculadoras=[
        "br_nacimiento(bc_mes_anterior)",
        "carencia_nacimiento(cotizaciones_vida_laboral, edad)",
        "duracion_nacimiento(tipo_familia, num_hijos, discapacidad_pct)",
    ],

    trampas_tipicas=[
        "DM26-T9-01",  # 19 semanas (no 16)
        "DM26-T9-02",  # Subsidio NC también hombres
        "C11",         # Art. 237.3 aplica a NACIMIENTO, NO a IT
        "C12",         # Lactancia: extinción a 9 meses (no 12)
        "C13",         # Riesgo embarazo: NO pago delegado
    ],

    cambios_dm_2026=get_cambios_para_blueprint("BP-S11"),

    eval_questions=[
        {
            "pregunta": "En 2026, la duración de la prestación de nacimiento y cuidado del menor para la madre biológica es de:",
            "respuesta_correcta": f"{NACIMIENTO_2026['semanas_madre']} semanas",
            "distractores": ["16 semanas", "18 semanas", "21 semanas"],
            "articulo": "Art. 182 TRLGSS",
            "trampa_id": "DM26-T9-01",
            "mnemonico": "Nacimiento 2026: 19 semanas (6+11+2). Antes eran 16.",
        },
        {
            "pregunta": "En un familia monoparental, la prestación de nacimiento en 2026 es de:",
            "respuesta_correcta": f"{NACIMIENTO_2026['semanas_monoparental']} semanas (6+22+4)",
            "distractores": ["19 semanas", "24 semanas", "16 semanas + 3 semanas adicionales"],
            "articulo": "Art. 182 TRLGSS",
            "trampa_id": "DM26-T9-01",
            "mnemonico": "Monoparental 2026: 32 semanas (6 obligatorias + 22 flexibles hasta 12m + 4 hasta 8 años)",
        },
        {
            "pregunta": "Desde 2026, el subsidio no contributivo de nacimiento y cuidado del menor:",
            "respuesta_correcta": "También lo pueden percibir los hombres (trabajadores y trabajadoras afiliados y en alta/asimilada que cumplan todos los requisitos salvo el período mínimo de cotización)",
            "distractores": [
                "Sigue siendo exclusivo de las mujeres",
                "Solo lo perciben los hombres cuando la madre ha fallecido",
                "Lo perciben solo parejas de hecho registradas",
            ],
            "articulo": "Art. 184 TRLGSS",
            "trampa_id": "DM26-T9-02",
            "mnemonico": "Subsidio NC nacimiento 2026: también hombres. Sin mínimo cotización.",
        },
        {
            "pregunta": "El Art. 237.3 TRLGSS (asimilación a cotizado de períodos de excedencia) aplica a:",
            "respuesta_correcta": "La prestación de NACIMIENTO y cuidado del menor — NO a la IT",
            "distractores": [
                "La Incapacidad Temporal en todos sus grados",
                "Tanto a la IT como al nacimiento",
                "Solo al desempleo contributivo",
            ],
            "articulo": "Art. 237.3 TRLGSS",
            "trampa_id": "C11",
            "mnemonico": "Art 237.3: para NACIMIENTO, nunca para IT. Trampa clásica.",
        },
        {
            "pregunta": "La prestación por riesgo durante la lactancia natural se extingue cuando:",
            "respuesta_correcta": "El lactante cumpla 9 meses (no 12)",
            "distractores": [
                "El lactante cumpla 12 meses",
                "La madre cese en la lactancia natural",
                "Transcurran 6 meses desde el nacimiento",
            ],
            "articulo": "Art. 188 TRLGSS",
            "trampa_id": "C12",
            "mnemonico": "Riesgo lactancia: extinción a los 9 meses del bebé (no 12).",
        },
    ],

    notas=(
        "SPRINT 0 — cambios DM 2026 incorporados el 22/03/2026. "
        "TRAMPAS CRÍTICAS: 19 semanas (no 16), Art. 237.3 para NACIMIENTO (no IT), "
        "lactancia 9 meses (no 12), subsidio NC también hombres."
    ),
)
