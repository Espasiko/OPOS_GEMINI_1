"""
OpositAIA V14 — Blueprint BP-S13
Tema: Jubilación anticipada (voluntaria e involuntaria) + Jubilación activa
Temas oficiales: TE13 — Jubilación anticipada y activa
Fuente: Arts. 206-208 TRLGSS (anticipada); Art. 214 TRLGSS (activa); RDL 2/2023

Cubre: anticipada involuntaria (causas legales, coeficientes reductores, edad mínima),
anticipada voluntaria (35 años cotizados, coeficiente por trimestre),
jubilación activa (% compatible, cotización solidaridad 9%, demora ≥2 años).
"""
import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
from v14.schemas import TopicBlueprint
import random

BP_S13 = TopicBlueprint(
    id="BP-S13",
    tema="Jubilación anticipada involuntaria/voluntaria + Jubilación activa",
    temas_oficiales=["TE13"],
    normativa_base=[
        "Art. 206 TRLGSS — Jubilación anticipada: disposiciones comunes",
        "Art. 207 TRLGSS — Jubilación anticipada por causa NO imputable al trabajador (involuntaria)",
        "Art. 207.1.d TRLGSS — Causas: despido objetivo/colectivo, ERE, jubilación empresario, fuerza mayor",
        "Art. 207.2 TRLGSS — Coeficiente reductor anticipada involuntaria (por trimestre)",
        "Art. 208 TRLGSS — Jubilación anticipada voluntaria (a voluntad del interesado)",
        "Art. 208.1 TRLGSS — Requisitos: ≥2 años antes EOJ, ≥35 años cotizados efectivos",
        "Art. 208.2 TRLGSS — Coeficiente reductor anticipada voluntaria (más severo)",
        "Art. 214 TRLGSS — Jubilación activa (compatibilidad trabajo + pensión)",
        "Art. 214.2.e TRLGSS — Jubilación activa: cotización especial solidaridad 9%",
        "Art. 214.2.d TRLGSS — Porcentaje compatible: 50% base, +5% por año demora (máx 100%)",
    ],

    articulos_obligatorios=[
        "Art. 207 TRLGSS",
        "Art. 208 TRLGSS",
        "Art. 214 TRLGSS",
    ],
    articulos_forbidden=[],

    calculadoras=[
        "coeficiente_anticipada_involuntaria(trimestres_anticipacion, años_cotizados)",
        "coeficiente_anticipada_voluntaria(trimestres_anticipacion, años_cotizados)",
        "porcentaje_jubilacion_activa(años_demora)",
    ],

    trampas_tipicas=["J1", "J2", "J3"],

    eval_questions=[
        {
            "pregunta": "José Manuel, de 63 años con 33 años cotizados, cesa por jubilación del empresario individual. ¿Puede acceder a jubilación anticipada involuntaria?",
            "respuesta_correcta": "Sí. La jubilación del empresario individual es causa legal del Art. 207.1.d TRLGSS. Cumple la edad mínima (4 años antes de EOJ) y el mínimo de 33 años cotizados.",
            "distractores": [
                "No, necesita al menos 35 años cotizados para cualquier anticipada",
                "No, la jubilación del empresario no es causa de anticipada involuntaria",
                "Solo si se inscribe como demandante de empleo durante 6 meses previos"
            ],
            "articulo": "Art. 207 TRLGSS",
            "trampa_id": "J1",
            "mnemonico": "Anticipada involuntaria: 33 años mínimo + causa legal (207.1.d). Voluntaria: 35 años + 2 años antes EOJ."
        },
        {
            "pregunta": "¿Cuál de las siguientes causas NO da derecho a jubilación anticipada involuntaria (Art. 207)?",
            "respuesta_correcta": "Despido disciplinario declarado procedente. El Art. 207.1.d incluye despido colectivo, objetivo, ERE, fuerza mayor, jubilación empresario, pero NO el despido disciplinario procedente.",
            "distractores": [
                "Despido por causas objetivas (Art. 52 ET)",
                "Despido colectivo por causas económicas (Art. 51 ET)",
                "Extinción por voluntad del trabajador por incumplimiento grave del empresario (Art. 50 ET)"
            ],
            "articulo": "Art. 207.1.d TRLGSS",
            "trampa_id": "J1",
            "mnemonico": "Disciplinario procedente = NO causa involuntaria. Disciplinario IMprocedente = SÍ (equiparado a objetivo)."
        },
        {
            "pregunta": "Un trabajador accede a jubilación anticipada involuntaria. ¿Cuál será el importe de su pensión MÁXIMA posible?",
            "respuesta_correcta": "El resultado de aplicar el coeficiente reductor correspondiente al importe de la pensión máxima (Art. 207.2 TRLGSS). La pensión máxima se ve reducida proporcionalmente.",
            "distractores": [
                "La pensión máxima general de 3.175,04€/mes sin reducción",
                "La base máxima de cotización (4.909,50€/mes en 2026)",
                "Un 0,50% fijo de reducción por cada trimestre de anticipación sobre la pensión máxima"
            ],
            "articulo": "Art. 207.2 TRLGSS",
            "trampa_id": "J2",
            "mnemonico": "Anticipada: la pensión máxima TAMBIÉN se reduce con el coeficiente. No hay tope sin reducir."
        },
        {
            "pregunta": "Candela, de 65 años con 40 años cotizados, quiere jubilación activa. ¿A qué edad podrá acceder por primera vez?",
            "respuesta_correcta": "A la edad ordinaria de jubilación (EOJ). Con 40 años cotizados ≥38a3m, su EOJ es 65 años. Puede acceder desde ya si cumple el resto de requisitos (Art. 214 TRLGSS).",
            "distractores": [
                "A los 66 años (EOJ + 1 año de demora obligatoria)",
                "A los 67 años (edad general sin cotización suficiente)",
                "A los 68 años (edad mínima para jubilación activa)"
            ],
            "articulo": "Art. 214 TRLGSS",
            "trampa_id": "J3",
            "mnemonico": "Jubilación activa: desde EOJ (no requiere demora para acceder). La demora mejora el % compatible."
        },
        {
            "pregunta": "Pedro accede a jubilación activa tras demorar 2 años completos el acceso a su pensión. ¿Qué porcentaje de pensión es compatible con el trabajo?",
            "respuesta_correcta": "El 60%. Base 50% + 5% por cada año completo de demora. Con 2 años: 50% + 10% = 60% (Art. 214.2.d TRLGSS).",
            "distractores": [
                "50% (porcentaje base sin incremento)",
                "55% (solo se cuenta 1 año de demora)",
                "45% (se reduce por trabajar por cuenta ajena)"
            ],
            "articulo": "Art. 214.2.d TRLGSS",
            "trampa_id": "J3",
            "mnemonico": "Activa: 50% base + 5%/año demora. Cotización solidaridad 9% durante activa."
        },
        {
            "pregunta": "Durante la jubilación activa, ¿qué cotización especial se aplica?",
            "respuesta_correcta": "Cotización especial de solidaridad del 9% sobre la base de cotización por contingencias comunes (Art. 214.2.e TRLGSS)",
            "distractores": [
                "1,15% sobre la base de contingencias comunes (cotización adicional solidaridad general)",
                "9% sobre la base de cotización de contingencias profesionales",
                "No se cotiza durante la jubilación activa"
            ],
            "articulo": "Art. 214.2.e TRLGSS",
            "trampa_id": "J2",
            "mnemonico": "Jubilación activa: 9% solidaridad sobre BC CC. No confundir con el 1,15% adicional general."
        },
    ],
)


def generar_briefing(dispatcher=None):
    from v14.nombres_pool import nombre_completo_aleatorio, nombre_empresa, ciudad

    nombre, _ = nombre_completo_aleatorio()
    empresa = nombre_empresa()
    ciudad_val = ciudad()

    tipo = random.choice(["anticipada_involuntaria", "anticipada_voluntaria", "activa"])

    if tipo == "anticipada_involuntaria":
        edad = random.randint(61, 64)
        años_cotizados = random.randint(33, 42)
        causa = random.choice([
            "despido colectivo por causas económicas",
            "despido objetivo (Art. 52 ET)",
            "jubilación del empresario individual",
            "fuerza mayor",
            "extinción por voluntad del trabajador (Art. 50 ET)"
        ])
        descripcion = (
            f"{nombre} ({edad} años, {años_cotizados} años cotizados) trabajaba en '{empresa}' ({ciudad_val}). "
            f"Su relación laboral finaliza por {causa}. Se inscribe como demandante de empleo al día siguiente. "
            f"Acude al CAISS para informarse sobre jubilación anticipada."
        )
    elif tipo == "anticipada_voluntaria":
        edad = random.randint(63, 65)
        años_cotizados = random.randint(35, 42)
        descripcion = (
            f"{nombre} ({edad} años, {años_cotizados} años cotizados) trabaja en '{empresa}' ({ciudad_val}). "
            f"Decide voluntariamente solicitar la jubilación anticipada."
        )
    else:  # activa
        edad = random.choice([65, 66, 67])
        años_cotizados = random.randint(36, 44)
        años_demora = random.randint(0, 4)
        pct_compatible = min(100, 50 + 5 * años_demora)
        sector = random.choice(["banca", "consultoría", "asesoría fiscal", "docencia", "arquitectura"])
        descripcion = (
            f"{nombre} ({edad} años, {años_cotizados} años cotizados) es empleado de {sector} en '{empresa}' ({ciudad_val}). "
            f"Ha demorado el acceso a su pensión {años_demora} año(s) completo(s). "
            f"Quiere compatibilizar trabajo y pensión mediante jubilación activa."
        )

    return {
        "personaje": nombre,
        "empresa": empresa,
        "ciudad": ciudad_val,
        "tema": "jubilación anticipada/activa",
        "edad": edad,
        "años_cotizados": años_cotizados,
        "tipo_jubilacion": tipo,
        "descripcion": descripcion,
    }

BP_S13.generar_briefing = generar_briefing
