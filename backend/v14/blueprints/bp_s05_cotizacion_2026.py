"""
OpositAIA V14 — Blueprint BP-S05
Tema: Bases CC + Tipos de cotización 2026
Temas oficiales: TE04 — Cotización normas + bases + tipos
Fuente: Art. 147, 148, 152 TRLGSS; Orden PJC/178/2025

⚠️ CAMBIOS DM 2026 INCORPORADOS:
  - DM26-T4-01: MEI 0,80% → 0,90% (empresa 0,75% + trabajador 0,15%)
  - DM26-T4-02: Adicional de Solidaridad — 3 tramos NUEVOS
  - DM26-T4-03: Base máxima CC 4.909,50€ → 5.101,20€
"""
import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')

from v14.schemas import TopicBlueprint
from v14.cambios_dm_2026 import get_cambios_para_blueprint, SOLIDARIDAD_2026, MEI_2026, BASE_MAXIMA_CC_2026

BP_S05 = TopicBlueprint(
    id="BP-S05",
    tema="Bases de cotización + tipos 2026 (MEI + Adicional Solidaridad)",
    temas_oficiales=["TE04"],
    normativa_base=[
        "Art. 147 TRLGSS — BC general trabajadores por cuenta ajena",
        "Art. 148 TRLGSS — BC contingencias profesionales",
        "Art. 152 TRLGSS — Cuotas y tipos generales",
        "Art. 19 bis TRLGSS — MEI",
        "Art. 19 ter TRLGSS — Cotización adicional de solidaridad (NUEVO 2026)",
        "Orden PJC/178/2025 — Tipos cotización 2026",
    ],

    articulos_obligatorios=[
        "Art. 147 TRLGSS",
        "Art. 19 bis TRLGSS",
    ],
    articulos_forbidden=[
        "Art. 147 bis",   # No existe
        "Art. 19 quarter", # No existe
    ],

    calculadoras=[
        "base_cc(salario_bruto, retribucion_especie, he_estructurales)",
        "vehiculo_especie(valor_mercado_vehiculo)",  # 20% VM/12 meses
        "mei_cuota(bc, tipo=0.90)",
        "adicional_solidaridad(retribucion_mensual, base_max=5101.20)",
    ],

    trampas_tipicas=[
        "C14",   # Confundir MEI con cotizaciones comunes
        "T4-01", # MEI 0,80% (valor 2025) → correcto 0,90%
        "T4-02", # No conocer los 3 tramos del Adicional Solidaridad
        "T4-03", # Usar base máxima 2025 (4.909,50€)
    ],

    cambios_dm_2026=get_cambios_para_blueprint("BP-S05"),

    eval_questions=[
        {
            "pregunta": "En 2026, el MEI es del:",
            "respuesta_correcta": "0,90% (0,75% empresa + 0,15% trabajador)",
            "distractores": ["0,80%", "1,15%", "0,90% a cargo exclusivo de la empresa"],
            "articulo": "Art. 19 bis TRLGSS + Orden PJC/178/2025",
            "trampa_id": "DM26-T4-01",
            "mnemonico": "MEI 0,90 en 2026: empresa 0,75 + trabajador 0,15",
        },
        {
            "pregunta": "El Adicional de Solidaridad para una retribución de 6.000€/mes (base máxima 5.101,20€) aplica:",
            "respuesta_correcta": "Tramo II: 1,25% sobre el exceso de 5.611,32€ hasta 7.651,80€. El exceso hasta 5.611,32€ va por Tramo I (1,15%).",
            "distractores": [
                "El 1,15% sobre toda la retribución",
                "El MEI (0,90%) más el 1,25%",
                "No aplica — la retribución no supera la base máxima",
            ],
            "articulo": "Art. 19 ter TRLGSS",
            "trampa_id": "DM26-T4-02",
            "mnemonico": "Solidaridad: el exceso sobre 5.101,20 va por tramos progresivos",
        },
        {
            "pregunta": "La base máxima de cotización por contingencias comunes en 2026 es:",
            "respuesta_correcta": "5.101,20€/mes",
            "distractores": ["4.909,50€", "5.000€", "4.800€"],
            "articulo": "Orden PJC/178/2025",
            "trampa_id": "DM26-T4-03",
            "mnemonico": "Base máxima 2026: 5.101,20 (no confundir con 4.909,50 de 2025)",
        },
        {
            "pregunta": "Las horas extraordinarias estructurales tienen un tipo de cotización del:",
            "respuesta_correcta": "28,30% (23,60% empresa + 4,70% trabajador)",
            "distractores": ["28,30% a cargo de la empresa", "28,30% a partes iguales", "14% por fuerza mayor"],
            "articulo": "Art. 152.2 TRLGSS",
            "trampa_id": "C14",
            "mnemonico": "HE estructurales: 28,30 total, empresa 23,60 más trab 4,70",
        },
        {
            "pregunta": "El vehículo de empresa para uso particular se incluye en la BC valorado como:",
            "respuesta_correcta": "20% del valor de mercado del vehículo, dividido entre 12 meses",
            "distractores": ["El coste de adquisición / 12", "El 20% de la retribución bruta", "No se computa en la BC"],
            "articulo": "Art. 147.2 TRLGSS",
            "trampa_id": "C15",
            "mnemonico": "Vehículo en BC: 20% VM / 12 meses",
        },
    ],

    notas=(
        "SPRINT 0 — cambios DM 2026 incorporados el 22/03/2026. "
        "La calculadora `adicional_solidaridad()` es NUEVA — no existía en V13. "
        "Los 3 tramos del Adicional de Solidaridad son una trampa clásica de examen 2026."
    ),
)


def generar_briefing_s05(dispatcher) -> dict:
    """
    Genera un caso de cotización 2026 con salario, HE y beneficios en especie aleatorios.
    """
    import random
    import sys
    sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
    from v14.nombres_pool import (nombre_completo_aleatorio, nombre_empresa,
                                   base_cotizacion_aleatoria, ciudad, sector)

    rng = random.Random()

    nombre, genero = nombre_completo_aleatorio(rng)
    empresa = nombre_empresa(rng)
    ciudad_caso = ciudad(rng)
    sector_empresa = sector(rng)
    edad = rng.randint(25, 55)

    salario_base = base_cotizacion_aleatoria(rng, minimo=1500.0, maximo=4500.0)
    tiene_he = rng.random() < 0.5
    tipo_he = rng.choice(["estructurales", "fuerza_mayor"]) if tiene_he else None
    horas_he = rng.choice([4, 8, 12, 16, 20]) if tiene_he else 0
    valor_he = round(horas_he * rng.choice([10.0, 12.0, 14.0, 16.0]), 2) if tiene_he else 0

    tiene_vehiculo = rng.random() < 0.35
    valor_vehiculo = rng.choice([18000, 22000, 25000, 30000, 35000, 40000]) if tiene_vehiculo else 0
    retribucion_especie_vehiculo = round(valor_vehiculo * 0.20 / 12, 2) if tiene_vehiculo else 0

    bc_total = round(salario_base + valor_he + retribucion_especie_vehiculo, 2)
    base_max = 5101.20
    bc_computable = min(bc_total, base_max)

    mei_empresa = round(bc_computable * 0.0075, 2)
    mei_trabajador = round(bc_computable * 0.0015, 2)
    mei_total = round(bc_computable * 0.009, 2)

    solidaridad_desc = None
    if bc_total > base_max:
        exceso = bc_total - base_max
        solidaridad_desc = (
            f"Exceso sobre base máxima: {exceso:.2f}€/mes → "
            f"Adicional Solidaridad Tramo I (hasta 5.611,32€): 1,15%"
        )

    tipo_he_desc = (
        f"HE {tipo_he}: {horas_he}h × tarifa = {valor_he:.2f}€ "
        f"(tipo cotización: {'28,30%' if tipo_he == 'estructurales' else '14%'})"
    ) if tiene_he else "Sin horas extraordinarias"

    return {
        "personaje": nombre,
        "empresa": empresa,
        "ciudad": ciudad_caso,
        "sector": sector_empresa,
        "genero": genero,
        "edad": edad,
        "salario_base_mensual": salario_base,
        "horas_extraordinarias": {"tipo": tipo_he, "valor": valor_he} if tiene_he else None,
        "vehiculo_empresa": {"valor_mercado": valor_vehiculo, "retribucion_especie": retribucion_especie_vehiculo} if tiene_vehiculo else None,
        "tema": "cotizacion",
        "descripcion": (
            f"{nombre}, de {edad} años, trabaja en {empresa} ({ciudad_caso}), "
            f"sector {sector_empresa}. Salario base: {salario_base:.2f}€/mes."
            + (f" Realiza {horas_he}h de HE {tipo_he} valoradas en {valor_he:.2f}€." if tiene_he else "")
            + (f" Dispone de vehículo de empresa (VM: {valor_vehiculo}€)." if tiene_vehiculo else "")
        ),
        "calculos_verificados": {
            "bc_contingencias_comunes": bc_computable,
            "mei_empresa": mei_empresa,
            "mei_trabajador": mei_trabajador,
            "mei_total": mei_total,
            "base_maxima_2026": base_max,
            "he_descripcion": tipo_he_desc,
            "solidaridad": solidaridad_desc,
        }
    }


BP_S05.generar_briefing = generar_briefing_s05
