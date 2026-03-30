"""
OpositAIA V14 — Blueprint BP-S04
Tema: Afiliación, altas, bajas y variaciones de datos
Temas oficiales: TE04 — Afiliación y alta en la Seguridad Social
Fuente: Arts. 15-17, 139-140 TRLGSS; RD 84/1996 (Reglamento Afiliación)

Cubre: plazos de alta/baja (3 días naturales siguientes, previas al inicio),
efectos del alta, situaciones asimiladas al alta, alta de oficio, alta presunta.
"""
import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
from v14.schemas import TopicBlueprint
import random
from datetime import date, timedelta

BP_S04 = TopicBlueprint(
    id="BP-S04",
    tema="Afiliación + Alta + Baja: plazos, efectos y situaciones asimiladas",
    temas_oficiales=["TE04"],
    normativa_base=[
        "Art. 15 TRLGSS — Afiliación al sistema",
        "Art. 16 TRLGSS — Altas y bajas de los trabajadores",
        "Art. 139 TRLGSS — Situaciones asimiladas al alta",
        "Art. 140 TRLGSS — Efectos del alta",
        "Art. 36 RD 84/1996 — Plazo alta previa RG (hasta 60 días antes)",
        "Art. 35.3 RD 84/1996 — Plazo baja RG: 3 días naturales siguientes al cese",
        "Art. 32 RD 84/1996 — Alta de oficio por la TGSS o ITSS",
        "Art. 166 TRLGSS — Alta presunta o de pleno derecho (AT/EP)",
    ],

    articulos_obligatorios=[
        "Art. 16 TRLGSS",
        "Art. 139 TRLGSS",
        "Art. 36 RD 84/1996",
        "Art. 35.3 RD 84/1996",
    ],
    articulos_forbidden=[],

    calculadoras=[],

    trampas_tipicas=["A1", "A2", "A3"],

    eval_questions=[
        {
            "pregunta": "El empresario comunica el alta de un trabajador el día 5 de junio de 2026, siendo el inicio de actividad el 7 de junio. ¿Está tramitando el alta en plazo reglamentario?",
            "respuesta_correcta": "Sí, el alta debe ser previa al inicio de actividad con antelación máxima de 60 días naturales. Al comunicarla 2 días antes del inicio, está en plazo (Art. 36 RD 84/1996)",
            "distractores": [
                "No, debería haberla presentado con al menos 10 días de antelación",
                "Sí, pero los efectos del alta serán desde el día siguiente, 6 de junio",
                "No, el alta debe comunicarse el mismo día del inicio de actividad, no antes"
            ],
            "articulo": "Art. 36 RD 84/1996",
            "trampa_id": "A1",
            "mnemonico": "Alta RG: PREVIA al inicio, máx 60 días antes. Efectos desde inicio actividad."
        },
        {
            "pregunta": "Un contrato temporal finaliza el viernes 14 de junio de 2026. ¿Hasta qué día tiene el empresario para tramitar la baja del trabajador?",
            "respuesta_correcta": "Hasta el martes 17 de junio de 2026. Plazo: 3 días NATURALES siguientes al cese. 15 (sábado) + 16 (domingo) + 17 (lunes) = 17 de junio (Art. 35.3 RD 84/1996)",
            "distractores": [
                "Hasta el 14 de junio (el mismo día del cese)",
                "Hasta el 19 de junio (3 días hábiles siguientes, excluyendo fin de semana)",
                "Hasta el 15 de junio (día siguiente al cese)"
            ],
            "articulo": "Art. 35.3 RD 84/1996",
            "trampa_id": "A2",
            "mnemonico": "Baja RG: 3 días NATURALES siguientes al cese. Naturales = cuentan sábado y domingo."
        },
        {
            "pregunta": "Un trabajador solicita una excedencia voluntaria y no inicia nueva actividad. ¿En qué situación queda respecto a la Seguridad Social?",
            "respuesta_correcta": "Baja. La excedencia voluntaria NO es situación asimilada al alta (Art. 139 TRLGSS no la incluye). Solo la excedencia por cuidado de hijo/familiar sí lo es.",
            "distractores": [
                "Asimilada al alta durante los 2 primeros años",
                "Alta especial, como en huelga legal",
                "Alta, porque la excedencia mantiene el vínculo con la empresa"
            ],
            "articulo": "Art. 139 TRLGSS",
            "trampa_id": "A3",
            "mnemonico": "Excedencia voluntaria = BAJA. Solo cuidado hijo/familiar = asimilada al alta."
        },
        {
            "pregunta": "Un trabajador sufre un accidente de trabajo y se descubre que no estaba dado de alta en la Seguridad Social. ¿Tiene derecho a prestaciones?",
            "respuesta_correcta": "Sí, por el principio de alta presunta o alta de pleno derecho en caso de AT/EP (Art. 166 TRLGSS). El trabajador se considera en alta a efectos de prestaciones por contingencias profesionales.",
            "distractores": [
                "No, sin alta no hay derecho a ninguna prestación",
                "Solo si el trabajador demuestra que comunicó personalmente su alta",
                "Solo tiene derecho a asistencia sanitaria, no a prestaciones económicas"
            ],
            "articulo": "Art. 166 TRLGSS",
            "trampa_id": "A1",
            "mnemonico": "AT/EP sin alta = alta presunta (Art. 166). Responsabilidad del empresario."
        },
        {
            "pregunta": "¿En qué plazo debe el empresario comunicar la variación de datos de un trabajador a la TGSS?",
            "respuesta_correcta": "3 días naturales siguientes a la variación (Art. 28 RD 84/1996)",
            "distractores": [
                "6 días naturales",
                "3 días hábiles",
                "10 días naturales desde la variación"
            ],
            "articulo": "Art. 28 RD 84/1996",
            "trampa_id": "A2",
            "mnemonico": "Variación datos: 3 días NATURALES. Mismo plazo que la baja. No confundir con hábiles."
        },
    ],
)


def generar_briefing(dispatcher=None):
    from v14.nombres_pool import nombre_completo_aleatorio, nombre_empresa, ciudad

    nombre, _ = nombre_completo_aleatorio()
    empresa = nombre_empresa()
    ciudad_val = ciudad()

    # Generar fechas concretas para cálculo de plazos
    año = 2026
    mes = random.randint(1, 11)
    dia_inicio = random.randint(1, 25)
    fecha_inicio = date(año, mes, dia_inicio)
    fecha_alta_comunicada = fecha_inicio - timedelta(days=random.randint(1, 5))

    dia_cese = random.randint(5, 28)
    mes_cese = min(mes + random.randint(1, 6), 12)
    fecha_cese = date(año, mes_cese, dia_cese)
    dia_semana_cese = fecha_cese.strftime("%A")

    tipo_contrato = random.choice([
        "temporal de 8 días", "temporal de obra", "indefinido",
        "a tiempo parcial", "de interinidad", "de formación"
    ])

    situacion = random.choice([
        "excedencia voluntaria",
        "excedencia por cuidado de hijo",
        "huelga legal",
        "desempleo involuntario",
        "traslado al extranjero"
    ])

    descripcion = (
        f"{nombre} trabaja en '{empresa}' ({ciudad_val}) con contrato {tipo_contrato}. "
        f"Inicio de actividad previsto: {fecha_inicio.strftime('%d/%m/%Y')}. "
        f"La empresa comunica el alta el {fecha_alta_comunicada.strftime('%d/%m/%Y')}. "
        f"La relación laboral finaliza el {fecha_cese.strftime('%d/%m/%Y')} ({dia_semana_cese})."
    )

    return {
        "personaje": nombre,
        "empresa": empresa,
        "ciudad": ciudad_val,
        "tema": "afiliación y altas",
        "edad": random.randint(20, 60),
        "descripcion": descripcion,
        "tipo_contrato": tipo_contrato,
        "fecha_inicio": fecha_inicio.isoformat(),
        "fecha_alta_comunicada": fecha_alta_comunicada.isoformat(),
        "fecha_cese": fecha_cese.isoformat(),
        "situacion_posterior": situacion,
    }

BP_S04.generar_briefing = generar_briefing
