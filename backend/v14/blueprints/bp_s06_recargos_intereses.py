"""
OpositAIA V14 — Blueprint BP-S06
Tema: Recargos e intereses de demora en Seguridad Social
Temas oficiales: TE06 — Recaudación: recargos e intereses
Fuente: Arts. 30-32 TRLGSS; RD 1415/2004 (Reglamento Recaudación)

Cubre: recargo del 10%/20%/35% según momento de pago, intereses de demora
sobre principal y sobre recargo, devengo de intereses, plazos reglamentarios.
"""
import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
from v14.schemas import TopicBlueprint
import random
from datetime import date, timedelta

BP_S06 = TopicBlueprint(
    id="BP-S06",
    tema="Recargos e intereses de demora: doble nivel y plazos",
    temas_oficiales=["TE06"],
    normativa_base=[
        "Art. 30 TRLGSS — Recargos e interés de demora",
        "Art. 30.1 TRLGSS — Recargo 10% si pago dentro del primer mes natural siguiente al vencimiento",
        "Art. 30.1 TRLGSS — Recargo 20% si pago después del primer mes pero antes de reclamación/acta",
        "Art. 30.1 TRLGSS — Recargo 20% si pago en plazo de reclamación de deuda",
        "Art. 30.1 TRLGSS — Recargo 35% si pago fuera de plazo de reclamación",
        "Art. 30.3 TRLGSS — Intereses de demora sobre el PRINCIPAL: desde vencimiento plazo reglamentario",
        "Art. 30.4 TRLGSS — Intereses de demora sobre el RECARGO: desde notificación providencia de apremio",
        "Art. 31 TRLGSS — Aplazamiento y fraccionamiento",
        "RD 1415/2004 — Reglamento General de Recaudación SS",
    ],

    articulos_obligatorios=[
        "Art. 30 TRLGSS",
        "Art. 30.1 TRLGSS",
        "Art. 30.3 TRLGSS",
        "Art. 30.4 TRLGSS",
    ],
    articulos_forbidden=[],

    calculadoras=[],

    trampas_tipicas=["R1", "R2", "R3"],

    eval_questions=[
        {
            "pregunta": "Un empresario no paga las cuotas del mes de marzo de 2026 (plazo reglamentario: hasta el 30 de abril). El 15 de mayo realiza el pago voluntariamente, sin que la TGSS haya emitido reclamación de deuda. ¿Qué recargo corresponde?",
            "respuesta_correcta": "Recargo del 10%. El pago se realiza dentro del primer mes natural siguiente al vencimiento del plazo reglamentario (Art. 30.1.a TRLGSS)",
            "distractores": [
                "Recargo del 20% por no pagar en plazo reglamentario",
                "Recargo del 35% por pago extemporáneo",
                "Sin recargo, al ser pago voluntario antes de la reclamación"
            ],
            "articulo": "Art. 30.1 TRLGSS",
            "trampa_id": "R1",
            "mnemonico": "Pago en 1er mes tras vencimiento = 10%. Después sin reclamación = 20%. Con reclamación en plazo = 20%. Fuera plazo reclamación = 35%."
        },
        {
            "pregunta": "La TGSS notifica una reclamación de deuda el 12 de abril de 2026. El empresario paga dentro del plazo concedido en la reclamación. ¿Qué recargo se aplica?",
            "respuesta_correcta": "Recargo del 20%. El pago dentro del plazo de la reclamación de deuda siempre es 20% (Art. 30.1.b TRLGSS)",
            "distractores": [
                "Recargo del 10% por pago voluntario",
                "Recargo del 35% por haber llegado a la fase de reclamación",
                "Sin recargo adicional si paga dentro del plazo de la reclamación"
            ],
            "articulo": "Art. 30.1 TRLGSS",
            "trampa_id": "R1",
            "mnemonico": "Reclamación deuda + pago en plazo = siempre 20%. No baja a 10% ni sube a 35%."
        },
        {
            "pregunta": "¿Desde qué fecha se devengan los intereses de demora sobre el PRINCIPAL de la deuda cuando el empresario no paga las cuotas de marzo de 2026?",
            "respuesta_correcta": "Desde el día siguiente al vencimiento del plazo reglamentario de ingreso, es decir, desde el 1 de mayo de 2026 (Art. 30.3 TRLGSS)",
            "distractores": [
                "Desde la fecha de notificación de la reclamación de deuda",
                "Desde la fecha de notificación de la providencia de apremio",
                "Desde el 1 de abril de 2026 (primer día del mes de la deuda)"
            ],
            "articulo": "Art. 30.3 TRLGSS",
            "trampa_id": "R2",
            "mnemonico": "Intereses PRINCIPAL: desde día siguiente al vencimiento plazo reglamentario. Intereses RECARGO: desde notificación providencia apremio."
        },
        {
            "pregunta": "La TGSS notifica providencia de apremio el 27 de junio de 2026. ¿Desde qué fecha son exigibles los intereses de demora sobre el RECARGO?",
            "respuesta_correcta": "Desde el 27 de junio de 2026, fecha de notificación de la providencia de apremio (Art. 30.4 TRLGSS: intereses del recargo se devengan desde notificación PA)",
            "distractores": [
                "Desde el 1 de mayo (mismo día que los intereses del principal)",
                "Desde el 12 de julio (15 días tras notificación)",
                "Desde el 28 de junio (día siguiente a la notificación)"
            ],
            "articulo": "Art. 30.4 TRLGSS",
            "trampa_id": "R3",
            "mnemonico": "Intereses RECARGO: desde notificación PA (no desde el día siguiente). Doble nivel: principal e intereses tienen fechas distintas."
        },
        {
            "pregunta": "Un trabajador autónomo no paga la cuota de enero de 2026. Realiza el pago el 4 de octubre de 2026, habiendo recibido providencia de apremio en agosto. ¿Qué recargo corresponde?",
            "respuesta_correcta": "Recargo del 35%. El pago se realiza fuera del plazo concedido en la reclamación de deuda y con providencia de apremio notificada (Art. 30.1.d TRLGSS)",
            "distractores": [
                "Recargo del 20% porque ya se notificó providencia de apremio",
                "Recargo del 10% por pago voluntario sin necesidad de embargo",
                "Sin recargo, porque los autónomos no están sujetos a recargos"
            ],
            "articulo": "Art. 30.1 TRLGSS",
            "trampa_id": "R1",
            "mnemonico": "PA notificada + pago fuera plazo = 35% siempre. Los autónomos SÍ tienen recargos."
        },
    ],
)


def generar_briefing(dispatcher=None):
    from v14.nombres_pool import nombre_completo_aleatorio, nombre_empresa, ciudad

    nombre, _ = nombre_completo_aleatorio()
    empresa = nombre_empresa()
    ciudad_val = ciudad()

    año = 2026
    mes_deuda = random.randint(1, 9)
    fecha_vencimiento = date(año, mes_deuda + 1, 30 if mes_deuda + 1 in [4, 6, 9, 11] else 28 if mes_deuda + 1 == 2 else 31)
    try:
        fecha_vencimiento = date(año, mes_deuda + 1, 30)
    except ValueError:
        fecha_vencimiento = date(año, mes_deuda + 1, 28)

    dias_retraso = random.choice([15, 25, 45, 90, 150])
    fecha_pago = fecha_vencimiento + timedelta(days=dias_retraso)

    if dias_retraso <= 30:
        recargo = "10%"
    elif dias_retraso <= 60:
        recargo = "20%"
    else:
        recargo = "35%"

    notifica_reclamacion = dias_retraso > 30
    fecha_reclamacion = fecha_vencimiento + timedelta(days=random.randint(35, 60)) if notifica_reclamacion else None
    notifica_apremio = dias_retraso > 90
    fecha_apremio = fecha_reclamacion + timedelta(days=random.randint(30, 60)) if notifica_apremio and fecha_reclamacion else None

    mes_nombres = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                   "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

    descripcion = (
        f"La empresa '{empresa}' no paga las cuotas de sus trabajadores correspondientes a "
        f"{mes_nombres[mes_deuda - 1]} de {año} (plazo reglamentario: {fecha_vencimiento.strftime('%d/%m/%Y')}). "
        f"{'La TGSS notifica reclamación de deuda el ' + fecha_reclamacion.strftime('%d/%m/%Y') + '. ' if fecha_reclamacion else ''}"
        f"{'La TGSS notifica providencia de apremio el ' + fecha_apremio.strftime('%d/%m/%Y') + '. ' if fecha_apremio else ''}"
        f"El pago se realiza el {fecha_pago.strftime('%d/%m/%Y')}."
    )

    return {
        "personaje": nombre,
        "empresa": empresa,
        "ciudad": ciudad_val,
        "tema": "recargos e intereses",
        "edad": random.randint(35, 60),
        "descripcion": descripcion,
        "mes_deuda": mes_nombres[mes_deuda - 1],
        "fecha_vencimiento": fecha_vencimiento.isoformat(),
        "fecha_pago": fecha_pago.isoformat(),
        "dias_retraso": dias_retraso,
        "recargo_aplicable": recargo,
        "fecha_reclamacion": fecha_reclamacion.isoformat() if fecha_reclamacion else None,
        "fecha_apremio": fecha_apremio.isoformat() if fecha_apremio else None,
        "calculos_verificados": {
            "recargo": recargo,
            "intereses_principal_desde": (fecha_vencimiento + timedelta(days=1)).isoformat(),
        }
    }

BP_S06.generar_briefing = generar_briefing
