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
        "Art. 190.5 TRLGSS — Cotización durante reducción jornada cuidado menor",
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
        "DM26-T11-01", # Art. 190.5: Cotización al 100% durante reducción jornada cuidado menor
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
            "pregunta": "Durante la reducción de jornada por cuidado de menor con cáncer (Art. 190.5 TRLGSS), la cotización se calcula sobre:",
            "respuesta_correcta": "El 100% de la base reguladora anterior a la reducción (no se reduce proporcionalmente)",
            "distractores": [
                "Se reduce proporcionalmente a la jornada reducida",
                "Se calcula sobre la base mínima de cotización",
                "Se exonera totalmente durante el cuidado",
                "Se calcula sobre el 50% de la base anterior",
            ],
            "articulo": "Art. 190.5 TRLGSS",
            "trampa_id": "DM26-T11-01",
            "mnemonico": "Reducción jornada cuidado menor: cotización 100% base anterior",
        },
        {
            "pregunta": "El Art. 237.3 TRLGSS (asimilación a cotizado de períodos de excedencia) aplica a:",
            "respuesta_correcta": "La prestación de NACIMIENTO y cuidado del menor — NO a la Incapacidad Temporal",
            "distractores": [
                "La Incapacidad Temporal en todos sus grados",
                "Solo a la IT por enfermedad común",
                "A la IT por accidente de trabajo",
                "A las prestaciones por desempleo",
            ],
            "articulo": "Art. 237.3 TRLGSS",
            "trampa_id": "C11",
            "mnemonico": "Art. 237.3: solo aplica a NACIMIENTO, no a IT",
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


def generar_briefing_s11(dispatcher) -> dict:
    """
    Genera un caso de nacimiento/cuidado del menor con situación familiar aleatoria.
    """
    import random
    import sys
    sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
    from v14.nombres_pool import (nombre_completo_aleatorio, nombre_empresa,
                                   ciudad)

    rng = random.Random()

    nombre, genero = nombre_completo_aleatorio(rng)
    empresa = nombre_empresa(rng)
    ciudad_caso = ciudad(rng)
    edad = rng.randint(26, 42)

    tipo_familia = rng.choice(["biparental", "monoparental", "multiple_biparental"])
    num_hijos = 1 if tipo_familia != "multiple_biparental" else rng.choice([2, 3])
    discapacidad = rng.random() < 0.25
    discapacidad_pct = rng.choice([33, 45, 65]) if discapacidad else 0

    if tipo_familia == "monoparental":
        semanas = 32
        desc_familia = "familia monoparental"
    elif tipo_familia == "multiple_biparental":
        semanas_base = 19
        semanas_extra = (num_hijos - 1) * 2
        semanas = semanas_base + semanas_extra
        desc_familia = f"parto múltiple ({num_hijos} hijos)"
    else:
        semanas = 19
        desc_familia = "familia biparental"

    semanas_disc = semanas + 2 if discapacidad and discapacidad_pct >= 33 else semanas

    return {
        "personaje": nombre,
        "empresa": empresa,
        "ciudad": ciudad_caso,
        "genero": genero,
        "edad": edad,
        "tipo_familia": tipo_familia,
        "num_hijos": num_hijos,
        "discapacidad_hijo": discapacidad,
        "discapacidad_pct": discapacidad_pct,
        "tema": "nacimiento_cuidado_menor",
        "descripcion": (
            f"{nombre}, de {edad} años, empleada/o en {empresa} ({ciudad_caso}), "
            f"tiene un {'parto' if num_hijos == 1 else f'parto múltiple de {num_hijos} hijos'} "
            f"en situación de {desc_familia}."
            + (f" Uno de los recién nacidos tiene una discapacidad reconocida del {discapacidad_pct}%." if discapacidad else "")
        ),
        "calculos_verificados": {
            "semanas_prestacion": semanas_disc,
            "tipo_familia": desc_familia,
            "semanas_base_2026": "19 semanas (Art. 182 TRLGSS)",
            "semanas_monoparental_2026": "32 semanas",
        }
    }


BP_S11.generar_briefing = generar_briefing_s11
