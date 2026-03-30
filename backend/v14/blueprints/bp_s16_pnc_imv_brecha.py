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
        "RD 1415/2004 Art. 10 — Recargos en cuotas de Seguridad Social",
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
            "pregunta": "Los recargos por impago de cuotas de Seguridad Social (RD 1415/2004 Art. 10) son:",
            "respuesta_correcta": "10% si se paga dentro del plazo de reclamación y 20% si se paga después de la providencia",
            "distractores": [
                "3% dentro del primer mes, 5% hasta 3 meses, 10% hasta 12 meses, 20% después",
                "5% siempre que se pague voluntariamente",
                "15% si se paga antes de la providencia y 25% después",
                "30% si el impago es superior a 6 meses",
            ],
            "articulo": "RD 1415/2004 Art. 10",
            "trampa_id": "DM26-T12-01",
            "mnemonico": "Recargos: 10% dentro plazo, 20% después providencia (no escala 3/5/10/20)",
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
        {
            "pregunta": "Cuando el empresario no cotiza al trabajador, el principio de automaticidad (Art. 167 TRLGSS) establece que:",
            "respuesta_correcta": "El trabajador NO pierde el derecho a prestaciones. El INSS anticipa y luego reclama al empresario.",
            "distractores": [
                "El trabajador pierde el derecho a todas las prestaciones hasta que el empresario regularice",
                "El trabajador debe esperar a que el empresario pague para poder solicitar prestaciones",
                "El trabajador solo tiene derecho a asistencia sanitaria, no a prestaciones económicas",
            ],
            "articulo": "Art. 167 TRLGSS",
            "trampa_id": "N1",
            "mnemonico": "Automaticidad: No pierden prestaciones. INSS anticipa y reclama.",
        },
    ],

    notas=(
        "SPRINT 0 — cambios DM 2026 incorporados el 22/03/2026: "
        "complemento brecha 36,90€ (no 34,80€) y cuantías PNC actualizadas. "
        "TRAMPA CRÍTICA: el complemento brecha es para quien tiene la pensión MÁS BAJA, "
        "no necesariamente la madre. Su naturaleza es CONTRIBUTIVA (Art. 60.4 TRLGSS)."
    ),
)


def generar_briefing_s16(dispatcher) -> dict:
    """
    Genera un caso PNC/IMV/brecha de género con situación personal aleatoria.
    """
    import random
    import sys
    sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
    from v14.nombres_pool import (nombre_completo_aleatorio, ciudad)

    rng = random.Random()

    tipo_caso = rng.choice(["pnc_jubilacion", "imv", "complemento_brecha"])

    nombre, genero = nombre_completo_aleatorio(rng)
    ciudad_caso = ciudad(rng)

    if tipo_caso == "pnc_jubilacion":
        edad = rng.randint(65, 80)
        anios_residencia = rng.choice([10, 12, 15, 20, 25, 30])
        ingresos_anuales = rng.choice([0, 1500, 3000, 5000, 6000])
        cuantia_pnc_mensual = 628.80
        elegible = anios_residencia >= 10
        descripcion = (
            f"{nombre}, de {edad} años, residente en {ciudad_caso} "
            f"con {anios_residencia} años de residencia legal acreditada en España. "
            f"Nunca ha cotizado a la Seguridad Social. "
            f"Solicita pensión no contributiva de jubilación."
        )
        calculos = {
            "tipo": "PNC Jubilación",
            "anios_residencia": anios_residencia,
            "cuantia_mensual_2026": f"{cuantia_pnc_mensual:.2f}€ × 14 pagas = {cuantia_pnc_mensual*14:.2f}€/año",
            "elegible": str(elegible),
            "requisito_residencia": "10 años (2 inmediatos anteriores a solicitud)",
        }

    elif tipo_caso == "imv":
        num_miembros = rng.randint(1, 5)
        ingresos_unidad = rng.choice([0, 2000, 4000, 6000, 8000])
        es_administrador_sl = rng.random() < 0.3
        descripcion = (
            f"{nombre}, en {ciudad_caso}, solicita el Ingreso Mínimo Vital "
            f"para una unidad de convivencia de {num_miembros} miembro(s). "
            f"Ingresos anuales de la unidad: {ingresos_unidad}€."
            + (" Es administrador/a de una SL con participación superior al 50%." if es_administrador_sl else "")
        )
        calculos = {
            "tipo": "IMV",
            "num_miembros": num_miembros,
            "ingresos_unidad_anual": ingresos_unidad,
            "incompatibilidad_sl": str(es_administrador_sl),
            "nota": "IMV incompatible con ser administrador SL con retribución o control ≥50%",
        }

    else:
        pension_progenitor_1 = round(rng.uniform(700, 2500), 2)
        pension_progenitor_2 = round(rng.uniform(700, 2500), 2)
        quien_cobra = "progenitor/a con pensión más baja"
        pension_baja = min(pension_progenitor_1, pension_progenitor_2)
        descripcion = (
            f"{nombre} y su pareja, ambos con pensión contributiva en {ciudad_caso}. "
            f"Pensión de {nombre}: {pension_progenitor_1:.2f}€/mes. "
            f"Pensión de la pareja: {pension_progenitor_2:.2f}€/mes. "
            f"Han tenido hijos en común."
        )
        calculos = {
            "tipo": "Complemento Brecha de Género",
            "complemento_2026": "36,90€/mes",
            "a_quien_corresponde": f"{quien_cobra} ({pension_baja:.2f}€/mes)",
            "naturaleza": "CONTRIBUTIVA (Art. 60.4 TRLGSS)",
            "trampa_clasica": "No es siempre la madre — es quien tenga la pensión más baja",
        }

    return {
        "personaje": nombre,
        "ciudad": ciudad_caso,
        "genero": genero,
        "tipo_caso": tipo_caso,
        "tema": "pnc_imv_brecha",
        "descripcion": descripcion,
        "calculos_verificados": calculos,
    }


BP_S16.generar_briefing = generar_briefing_s16
