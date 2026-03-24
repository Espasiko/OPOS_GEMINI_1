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
