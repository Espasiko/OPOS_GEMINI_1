"""
OpositAIA V14 — Blueprint BP-S10
Tema: IP — IPP + IPT + IPA + Gran Incapacidad
Temas oficiales: TE08 — IT + IP
Fuente: Arts. 193-200 TRLGSS; Ley 15/2022

⚠️ CAMBIO DM 2026 INCORPORADO:
  - DM26-T8-01: Gran Invalidez → Gran Incapacidad (sin extinción automática; 3 pasos empresa)
"""
import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
from v14.schemas import TopicBlueprint
from v14.cambios_dm_2026 import get_cambios_para_blueprint

BP_S10 = TopicBlueprint(
    id="BP-S10",
    tema="Incapacidad Permanente: IPP, IPT, IPA, Gran Incapacidad (2026)",
    temas_oficiales=["TE08"],
    normativa_base=[
        "Art. 193 TRLGSS — Concepto IP",
        "Art. 194 TRLGSS — Clases de IP",
        "Art. 196 TRLGSS — IPP",
        "Art. 197 TRLGSS — IPT",
        "Art. 198 TRLGSS — IPA",
        "Art. 199 TRLGSS — Gran Incapacidad (antes Gran Invalidez)",
        "Art. 200 TRLGSS — BR y cuantía pensión IP",
        "Ley 15/2022 — Cambio Gran Invalidez → Gran Incapacidad",
    ],

    articulos_obligatorios=[
        "Art. 174 TRLGSS",  # Extinción IT y propuesta IP (545 días)
        "Art. 194 TRLGSS",
        "Art. 196 TRLGSS",  # IPP — cuantía y subsidio
        "Art. 199 TRLGSS",
        "Art. 200 TRLGSS",
    ],
    articulos_forbidden=[
        "Art. 194 bis",  # No existe
        "Art. 173 bis",  # No existe (confundir con IT)
    ],

    calculadoras=[
        "ip_subsidio(bc, grado, anios_cotizados)",
        "gran_incapacidad_complemento(bc_minima, ultima_bc)",  # 50%BMin + 25%última BC
        "br_ip(cotizaciones, tipo_contingencia)",
    ],

    trampas_tipicas=[
        "DM26-T8-01",  # Gran Incapacidad — extinción automática FALSO
        "C8",          # Confundir grados de IP
        "C9",          # Complemento GI: 50% BMin + 25% última BC (no 45%)
        "C10",         # HC IP = alta médica con propuesta IP (no solicitud)
        "C11",         # Tanto alzado IPT — escala por edad (OM 31-01-1970)
    ],

    cambios_dm_2026=get_cambios_para_blueprint("BP-S10"),

    eval_questions=[
        {
            "pregunta": "Cuando se reconoce la Gran Incapacidad a un trabajador, el contrato:",
            "respuesta_correcta": "NO se extingue automáticamente. La empresa debe: (1) adaptar el puesto, (2) si no puede, reubicar, (3) solo si nada es posible y lo demuestra, puede extinguir.",
            "distractores": [
                "Se extingue automáticamente desde la fecha de resolución del INSS",
                "El trabajador puede optar entre extinción o adaptación",
                "Se suspende durante 3 años máximo",
            ],
            "articulo": "Art. 199 TRLGSS (modificado Ley 15/2022)",
            "trampa_id": "DM26-T8-01",
            "mnemonico": "Gran Incapacidad: adaptar, reubicar, y solo después tal vez extinguir",
        },
        {
            "pregunta": "La denominación oficial en 2026 de lo que antes se llamaba 'Gran Invalidez' es:",
            "respuesta_correcta": "Gran Incapacidad",
            "distractores": ["Gran Discapacidad", "Incapacidad Total Absoluta", "Sigue llamándose Gran Invalidez"],
            "articulo": "Art. 199 TRLGSS",
            "trampa_id": "DM26-T8-01",
            "mnemonico": "2026: Invalidez → Incapacidad. Gran Invalidez → Gran Incapacidad.",
        },
        {
            "pregunta": "El complemento de Gran Incapacidad (Art. 200.4 TRLGSS) se calcula como:",
            "respuesta_correcta": "50% de la base mínima de cotización + 25% de la última base de cotización del trabajador",
            "distractores": [
                "45% de la base reguladora",
                "50% de la última base de cotización",
                "El 100% de la pensión de IPA",
            ],
            "articulo": "Art. 200.4 TRLGSS",
            "trampa_id": "C9",
            "mnemonico": "Complemento GI: 50% BMin más 25% última BC (no 45%)",
        },
        {
            "pregunta": "Para que nazca la situación de Incapacidad Permanente, el trabajador debe haber agotado:",
            "respuesta_correcta": "El período máximo de IT (545 días para EC / sin límite para AT), tras propuesta del INSS o Mutua",
            "distractores": [
                "12 meses de IT",
                "El trabajador puede solicitar la IP en cualquier momento",
                "Solo tras 24 meses consecutivos de IT",
            ],
            "articulo": "Art. 174 + Art. 193 TRLGSS",
            "trampa_id": "C10",
            "mnemonico": "Alta médica con propuesta IP = Hecho Causante de la IP",
        },
        {
            "pregunta": "La Incapacidad Permanente Parcial se determina en relación con:",
            "respuesta_correcta": "La profesión habitual del trabajador — disminuye el rendimiento en ≥33%",
            "distractores": [
                "Cualquier trabajo adecuado a sus capacidades",
                "La profesión habitual — disminuye el rendimiento en ≥50%",
                "Cualquier trabajo del grupo profesional del trabajador",
            ],
            "articulo": "Art. 194.2 TRLGSS",
            "trampa_id": "C8",
            "mnemonico": "IPP: profesión habitual, ≥33%. IPT: profesión habitual, cualquier tarea. IPA: cualquier trabajo.",
        },
        {
            "pregunta": "Un trabajador de 58 años tiene reconocida una IPT. ¿A cuántas mensualidades de la base reguladora equivale la indemnización a tanto alzado si decide sustituir la pensión vitalicia?",
            "respuesta_correcta": "24 mensualidades de la base reguladora (escala O.M. 31-01-1970: tramo 58 años = 24 mensualidades)",
            "distractores": [
                "No tiene derecho; el tanto alzado solo se aplica a trabajadores menores de 54 años",
                "60 mensualidades, cuantía estándar fijada para toda IPT sin distinción de edad",
                "36 mensualidades, por aplicación del tramo de 57 años de la escala",
            ],
            "articulo": "O.M. 15-04-1969 y O.M. 31-01-1970 (escala tanto alzado IPT)",
            "trampa_id": "C11",
            "mnemonico": (
                "ESCALA TANTO ALZADO IPT (O.M. 31-01-1970): "
                "<54 años=84m | 54=72m | 55=60m | 56=48m | 57=36m | 58=24m | 59=12m | ≥60=NO. "
                "Trampa DM: confundir el valor del caso con 55 años (60m) aplicándolo a otro tramo de edad."
            ),
        },
    ],

    notas=(
        "SPRINT 0 — cambio DM 2026 Gran Incapacidad incorporado el 22/03/2026. "
        "TRAMPA CRÍTICA T8-01: 'extinción automática' es la trampa favorita de DM en T8. "
        "Mnemónico: 'adaptar → reubicar → extinguir (solo si imposible)'. "
        "TRAMPA C11 — TANTO ALZADO IPT (O.M. 31-01-1970, vigente): "
        "la escala decrementa de 12 en 12 por cada año desde los 54: "
        "<54=84m, 54=72m, 55=60m, 56=48m, 57=36m, 58=24m, 59=12m, >=60=no elegible. "
        "Solo aplica a IPT (no IPA, no IPP). "
        "Plazo para solicitarlo: antes de cumplir 60 años."
    ),
)


def generar_briefing_s10(dispatcher) -> dict:
    """
    Genera un caso de IP con grado, contingencia y datos aleatorios legalmente válidos.
    """
    import random
    import sys
    sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
    from v14.nombres_pool import (nombre_completo_aleatorio, nombre_empresa,
                                   base_cotizacion_aleatoria, ciudad)

    rng = random.Random()

    nombre, genero = nombre_completo_aleatorio(rng)
    empresa = nombre_empresa(rng)
    ciudad_caso = ciudad(rng)

    grado = rng.choice(["IPP", "IPT", "IPA", "Gran Incapacidad"])
    contingencia = rng.choice(["contingencias comunes", "accidente de trabajo"])
    anos_cotizados = rng.randint(8, 40)
    edad = rng.randint(30, 58)
    ultima_bc = base_cotizacion_aleatoria(rng, minimo=1323.0, maximo=3500.0)
    base_minima = 1323.0

    if grado == "IPP":
        pension_desc = f"Indemnización a tanto alzado: 24 mensualidades de la BR"
    elif grado == "IPT":
        br = round(ultima_bc * 12 / 14, 2)
        pension_mensual = round(br * 0.55, 2)
        pension_desc = f"55% de la BR ({pension_mensual:.2f}€/mes)"
    elif grado == "IPA":
        br = round(ultima_bc * 12 / 14, 2)
        pension_mensual = round(br * 1.00, 2)
        pension_desc = f"100% de la BR ({pension_mensual:.2f}€/mes)"
    else:
        br = round(ultima_bc * 12 / 14, 2)
        complemento = round(base_minima * 0.50 + ultima_bc * 0.25, 2)
        pension_desc = (
            f"100% de la BR + complemento GI: "
            f"50% BMin ({base_minima*0.50:.2f}€) + 25% última BC ({ultima_bc*0.25:.2f}€) "
            f"= complemento {complemento:.2f}€/mes"
        )

    articulo_trabajador = "El trabajador" if genero == "masculino" else "La trabajadora"

    return {
        "personaje": nombre,
        "empresa": empresa,
        "ciudad": ciudad_caso,
        "genero": genero,
        "edad": edad,
        "anos_cotizados": anos_cotizados,
        "ultima_bc": ultima_bc,
        "grado_ip": grado,
        "tipo_contingencia": contingencia,
        "tema": "incapacidad_permanente",
        "descripcion": (
            f"{nombre}, de {edad} años, trabaja en {empresa} ({ciudad_caso}) "
            f"y acredita {anos_cotizados} años de cotización. "
            f"Tras agotar el período máximo de IT por {contingencia}, "
            f"el INSS emite dictamen-propuesta reconociendo una {grado}."
        ),
        "calculos_verificados": {
            "grado_reconocido": grado,
            "contingencia": contingencia,
            "pensión_descripcion": pension_desc,
        }
    }


BP_S10.generar_briefing = generar_briefing_s10
