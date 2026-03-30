"""
OpositAIA V14 — Blueprint BP-S07
Tema: SLD, Recaudación ejecutiva, URE, Embargo de bienes
Temas oficiales: TE07 — Recaudación en vía ejecutiva
Fuente: Arts. 33-39 TRLGSS; RD 1415/2004 (Reglamento Recaudación)

Cubre: Sistema Liquidación Directa (SILTRA), documentos de cobro
(reclamación deuda vs acta liquidación vs providencia apremio),
URE competente, embargo (orden prelación bienes, valoración contradictoria,
tercería), fecha de pago (transferencia = entrada en cuenta).
"""
import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
from v14.schemas import TopicBlueprint
import random
from datetime import date, timedelta

BP_S07 = TopicBlueprint(
    id="BP-S07",
    tema="Recaudación ejecutiva: SLD, URE, embargo y documentos de cobro",
    temas_oficiales=["TE07"],
    normativa_base=[
        "Art. 33 TRLGSS — Reclamación de deuda",
        "Art. 34 TRLGSS — Actas de liquidación (ITSS)",
        "Art. 35 TRLGSS — Providencia de apremio",
        "Art. 37 TRLGSS — Ejecución forzosa: embargo de bienes",
        "Art. 38 TRLGSS — Orden de embargo (dinero, créditos, inmuebles...)",
        "Art. 22.4 RD 1415/2004 — SLD: plazo TGSS para informar errores de liquidación",
        "Art. 22.6 RD 1415/2004 — SLD: plazo empresa para corregir datos tras rechazo",
        "Art. 85 RD 1415/2004 — URE competente para embargo de inmuebles",
        "Art. 90 RD 1415/2004 — Valoración contradictoria de bienes embargados",
        "Art. 96 RD 1415/2004 — Pago por transferencia: se entiende pagado cuando entra en cuenta",
    ],

    articulos_obligatorios=[
        "Art. 33 TRLGSS",
        "Art. 34 TRLGSS",
        "Art. 35 TRLGSS",
        "Art. 37 TRLGSS",
    ],
    articulos_forbidden=[],

    calculadoras=[],

    trampas_tipicas=["U1", "U2", "U3"],

    eval_questions=[
        {
            "pregunta": "La Inspección de Trabajo acude a una empresa el 8 de abril de 2026 y descubre un trabajador sin alta desde el 1 de marzo. ¿Qué mecanismo debe utilizar la ITSS para reclamar las cuotas?",
            "respuesta_correcta": "Acta de liquidación. Cuando la ITSS constata trabajadores sin alta, el instrumento es el acta de liquidación, no la reclamación de deuda (Art. 34 TRLGSS)",
            "distractores": [
                "Reclamación de deuda emitida por la TGSS",
                "Providencia de apremio directamente",
                "Liquidación complementaria de cuotas"
            ],
            "articulo": "Art. 34 TRLGSS",
            "trampa_id": "U1",
            "mnemonico": "ITSS descubre sin alta → Acta liquidación (Art. 34). TGSS reclama cuotas normales → Reclamación deuda (Art. 33)."
        },
        {
            "pregunta": "La empresa realiza una transferencia por el importe total de la deuda a la cuenta habilitada por la TGSS el 9 de septiembre de 2026. El importe entra en la cuenta el 11 de septiembre. ¿En qué fecha se entiende pagada la deuda?",
            "respuesta_correcta": "El 11 de septiembre de 2026. El pago por transferencia se entiende realizado en la fecha en que tiene entrada en la cuenta bancaria (Art. 96 RD 1415/2004)",
            "distractores": [
                "El 9 de septiembre (fecha de la orden de transferencia)",
                "El 10 de septiembre (día hábil siguiente a la orden)",
                "El 12 de septiembre (día siguiente a la entrada en cuenta)"
            ],
            "articulo": "Art. 96 RD 1415/2004",
            "trampa_id": "U2",
            "mnemonico": "Transferencia = pagado cuando ENTRA en cuenta, no cuando se ordena."
        },
        {
            "pregunta": "La URE de Madrid persigue una deuda de 125.000€ de un autónomo. Se localiza un inmueble en Alicante valorado en 105.000€. ¿Qué URE es competente para el embargo del inmueble?",
            "respuesta_correcta": "La Unidad de Recaudación Ejecutiva de Alicante (Art. 85 RD 1415/2004: para embargo de inmuebles, es competente la URE de la provincia donde radique el bien)",
            "distractores": [
                "La URE de Madrid, por ser la que persigue la deuda",
                "La Dirección General de la TGSS",
                "Comisión mixta URE Madrid + URE Alicante"
            ],
            "articulo": "Art. 85 RD 1415/2004",
            "trampa_id": "U3",
            "mnemonico": "Embargo inmueble: URE de la PROVINCIA del bien, no la que persigue la deuda."
        },
        {
            "pregunta": "Se embarga una finca a nombre de la sociedad valorada por la TGSS en 40.000€. La empresa presenta una valoración contradictoria de 70.000€. ¿Qué valoración se utilizará?",
            "respuesta_correcta": "55.000€ (media aritmética de ambas valoraciones). Cuando la diferencia entre ambas no excede un tercio de la mayor, se aplica la media (Art. 90 RD 1415/2004)",
            "distractores": [
                "40.000€ (prevalece la valoración de la Administración)",
                "70.000€ (prevalece la del interesado por ser más favorable)",
                "Se designa un tercer perito tasador independiente"
            ],
            "articulo": "Art. 90 RD 1415/2004",
            "trampa_id": "U2",
            "mnemonico": "Valoración contradictoria: si diferencia ≤1/3 mayor → media aritmética. Si >1/3 → perito tercero."
        },
        {
            "pregunta": "La empresa utiliza SLD (SILTRA) para liquidar cuotas de marzo de 2026 pero la TGSS comunica que faltan datos de 2 trabajadores. ¿De qué plazo máximo dispone la empresa para aportar los datos correctos?",
            "respuesta_correcta": "Hasta el último día del plazo reglamentario de ingreso de cuotas (Art. 22.6 RD 1415/2004). Para cuotas de marzo, hasta el 30 de abril de 2026.",
            "distractores": [
                "48 horas desde la comunicación del error",
                "10 días hábiles desde la comunicación del error",
                "Hasta el 29 de abril de 2026 (día anterior al vencimiento)"
            ],
            "articulo": "Art. 22.6 RD 1415/2004",
            "trampa_id": "U1",
            "mnemonico": "SLD error → corregir hasta fin plazo reglamentario (último día del mes siguiente). No hay plazo extra."
        },
    ],
)


def generar_briefing(dispatcher=None):
    from v14.nombres_pool import nombre_completo_aleatorio, nombre_empresa, ciudad

    nombre, _ = nombre_completo_aleatorio()
    empresa = nombre_empresa()
    ciudad_val = ciudad()
    ciudad_inmueble = ciudad()
    while ciudad_inmueble == ciudad_val:
        ciudad_inmueble = ciudad()

    año = 2026
    mes_deuda = random.randint(1, 8)
    mes_nombres = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                   "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

    deuda_total = random.choice([25000, 50000, 75000, 100000, 125000, 180000])
    valor_inmueble = random.choice([40000, 60000, 80000, 105000, 150000])
    valor_admin = int(valor_inmueble * random.uniform(0.55, 0.85))
    hipoteca = random.choice([0, 15000, 25000, 40000])

    fecha_transferencia = date(año, random.randint(6, 11), random.randint(1, 25))
    dias_entrada = random.choice([0, 1, 2, 3])
    fecha_entrada_cuenta = fecha_transferencia + timedelta(days=dias_entrada)

    itss_descubre = random.choice([True, False])
    if itss_descubre:
        fecha_itss = date(año, random.randint(3, 9), random.randint(1, 25))
        meses_sin_alta = random.randint(1, 4)
        fecha_sin_alta = fecha_itss - timedelta(days=meses_sin_alta * 30)

    descripcion = (
        f"La empresa '{empresa}' ({ciudad}) tiene una deuda de {deuda_total:,.0f}€ con la SS "
        f"por cuotas de {mes_nombres[mes_deuda - 1]} de {año}. "
        f"La URE de {ciudad} inicia el embargo. Se localiza un inmueble en {ciudad_inmueble} "
        f"valorado en {valor_inmueble:,.0f}€"
        f"{' con hipoteca de ' + f'{hipoteca:,.0f}€' if hipoteca else ''}. "
        f"La Administración valora el bien en {valor_admin:,.0f}€. "
        f"{'La ITSS descubrió un trabajador sin alta desde ' + fecha_sin_alta.strftime('%d/%m/%Y') + '. ' if itss_descubre else ''}"
        f"Se realiza transferencia el {fecha_transferencia.strftime('%d/%m/%Y')}, "
        f"entrada en cuenta el {fecha_entrada_cuenta.strftime('%d/%m/%Y')}."
    )

    return {
        "personaje": nombre,
        "empresa": empresa,
        "ciudad": ciudad_val,
        "tema": "recaudación ejecutiva",
        "edad": random.randint(40, 65),
        "descripcion": descripcion,
        "deuda_total": deuda_total,
        "ciudad_inmueble": ciudad_inmueble,
        "valor_inmueble": valor_inmueble,
        "valor_admin": valor_admin,
        "hipoteca": hipoteca,
        "fecha_transferencia": fecha_transferencia.isoformat(),
        "fecha_entrada_cuenta": fecha_entrada_cuenta.isoformat(),
        "itss_descubre": itss_descubre,
    }

BP_S07.generar_briefing = generar_briefing
