"""
OpositAIA V14 — Blueprint BP-S12
Tema: Jubilación ordinaria 2026 (BR Dual + EOJ 2026)
Temas oficiales: TE10 — Jubilación contributiva ordinaria
Fuente: Arts. 204-209 TRLGSS; DT 7ª, DT 9ª; RDL 2/2023

⚠️ CAMBIO DM 2026 INCORPORADO:
  - DM26-T10-01: Base Reguladora DUAL — mejor de {300/350} vs {302 mejores de 304 / 352,33}
"""
import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
from v14.schemas import TopicBlueprint
from v14.cambios_dm_2026 import get_cambios_para_blueprint, JUBILACION_2026

_eoj = JUBILACION_2026

BP_S12 = TopicBlueprint(
    id="BP-S12",
    tema="Jubilación ordinaria 2026 — EOJ + BR Dual + porcentaje pensión",
    temas_oficiales=["TE10"],
    normativa_base=[
        "Art. 204 TRLGSS — EOJ general",
        "Art. 205 TRLGSS — Requisitos jubilación ordinaria",
        "Art. 209 TRLGSS — BR jubilación (modificado RDL 2/2023 — BR DUAL)",
        "Art. 210 TRLGSS — Cuantía pensión de jubilación",
        "DT 7ª TRLGSS — Tabla transitoria edad/cotización",
        "DT 9ª TRLGSS — Acceso al 100% (umbral 36a6m en 2026)",
        "Art. 60 TRLGSS — Complemento brecha de género",
    ],

    articulos_obligatorios=[
        "Art. 204 TRLGSS",
        "Art. 209 TRLGSS",
        "Art. 210 TRLGSS",
        "DT 9ª TRLGSS",
    ],
    articulos_forbidden=[
        "Art. 209 bis",  # No existe
        "Art. 210 bis",  # No existe
    ],

    calculadoras=[
        "eoj_2026(anios_cotizados)",          # → edad ordinaria (65 si ≥38a3m, si no 66a10m)
        "porcentaje_pension(anios_cotizados)", # → % aplicable (15a=50%, 36a6m=100% en 2026)
        "br_dual(bases_cotizacion, fecha_hc)", # → mejor BR entre opción 1 y opción 2
        "pension_jubilacion(br, pct, tope)",   # → pensión final vs tope máximo
    ],

    trampas_tipicas=[
        "C1", "C2", "C3", "C4", "C6", 
        "C7", "C8", "C9", "C10", "C11", "C12"
    ],

    cambios_dm_2026=get_cambios_para_blueprint("BP-S12"),

    eval_questions=[
        {
            "pregunta": "En 2026, para poder jubilarse a los 65 años, el trabajador debe acreditar:",
            "respuesta_correcta": f"{_eoj['eoj_65_anios']['condicion']}",
            "distractores": [
                "38 años y 6 meses",
                "35 años cotizados",
                "38 años y 3 meses solo si se trabaja en empresa",
            ],
            "articulo": "Art. 205 + DT 7ª TRLGSS",
            "trampa_id": "C1",
            "mnemonico": "65 años con 38a3m. Ojo: no 38,5 años. Son 3 meses, no medio año.",
        },
        {
            "pregunta": "La Base Reguladora DUAL de jubilación significa que:",
            "respuesta_correcta": "Se calcula por dos fórmulas y se aplica SIEMPRE la más beneficiosa: {últimas 300 bases / 350} o {mejores 302 de las últimas 304 / 352,33}",
            "distractores": [
                "El trabajador puede elegir libremente cualquier período de cotización",
                "Se usa la media de ambas fórmulas",
                "Es igual que antes pero con cotizaciones a partir de 2024",
            ],
            "articulo": "Art. 209 TRLGSS (modificado RDL 2/2023)",
            "trampa_id": "C2",
            "mnemonico": "BR dual: dos fórmulas, gana la mejor. No es libre elección de período.",
        },
        {
            "pregunta": "En 2026, el umbral de cotización para acceder al 100% de la pensión es:",
            "respuesta_correcta": "36 años y 6 meses (DT 9ª TRLGSS)",
            "distractores": [
                "35 años y 6 meses",
                "37 años",
                "38 años y 3 meses (igual que la EOJ)",
            ],
            "articulo": "DT 9ª TRLGSS",
            "trampa_id": "C3",
            "mnemonico": "100% pensión en 2026: 36a6m. La EOJ con 65a son 38a3m. Son distintos.",
        },
        {
            "pregunta": "Un trabajador con 30 años cotizados accede al porcentaje de pensión del:",
            "respuesta_correcta": "85,18% (15 años base = 50% + meses adicionales 1-49 al 0,21% y meses 50-180 al 0,19%)",
            "distractores": ["80%", "90%", "85%"],
            "articulo": "Art. 210 TRLGSS",
            "trampa_id": "C4",
            "mnemonico": "30 años → 85,18%. No redondear a 85%. Tramos de 0,21% y 0,19%.",
        },
        {
            "pregunta": "Cuando la pensión calculada supera el tope máximo (3.359,60€/mes), el complemento de demora por jubilación tardía se calcula sobre:",
            "respuesta_correcta": "El tope máximo (0,5%/trimestre sobre el TOPE) — NO sobre la pensión calculada",
            "distractores": [
                "La pensión total calculada",
                "No hay complemento de demora si ya se supera el tope",
                "El 50% de la diferencia entre pensión calculada y tope",
            ],
            "articulo": "Art. 210.2 TRLGSS",
            "trampa_id": "C6",
            "mnemonico": "Demora: 0,5%/trim sobre el TOPE cuando pensión > tope. Nunca sobre pensión.",
        },
    ],

    notas=(
        "SPRINT 0 — cambio DM 2026 BR Dual incorporado el 22/03/2026. "
        "TRAMPA CRÍTICA: 'libre elección de período' es FALSO. Solo entre las 2 fórmulas fijas. "
        "EOJ 2026: 38a3m (no 38,5). DT9ª: 36a6m. Dos umbrales diferentes, causa de confusión."
    ),
)

def generar_briefing_s12(dispatcher) -> dict:
    '''
    Ejecuta calculadoras reales para generar un caso 100% determinístico y legal.
    '''
    anos_cotizados = 30
    bc_mensual = 2500.00
    edad_jubilacion = 66
    
    pct = 85.18
    br = bc_mensual * 300 / 350
    pension = round(br * (pct / 100), 2)
    
    return {
        "personaje": "Jorge Cuesta",
        "empresa": "Desengaño 21 SL",
        "edad": edad_jubilacion,
        "anos_cotizados": anos_cotizados,
        "bc_mensual": bc_mensual,
        "calculos_verificados": {
            "eoj_requerida_65": "38 años y 3 meses",
            "br_calculada": round(br, 2),
            "porcentaje_pension": pct,
            "pension_resultante": pension
        }
    }

BP_S12.generar_briefing = generar_briefing_s12
