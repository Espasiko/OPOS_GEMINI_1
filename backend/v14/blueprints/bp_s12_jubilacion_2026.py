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
        "Art. 205 TRLGSS",  # Acceso a la jubilación ordinaria — requisitos
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

def _calcular_porcentaje_pension(anos_cotizados: float) -> float:
    """Art. 210 TRLGSS: escala de porcentaje según años cotizados."""
    meses = int(anos_cotizados * 12)
    if meses < 180:
        return 50.0
    adicionales = meses - 180
    pct = 50.0 + min(adicionales, 49) * 0.21
    if adicionales > 49:
        pct += (adicionales - 49) * 0.19
    return min(round(pct, 2), 100.0)


def _calcular_eoj(anos_cotizados: float) -> str:
    """DT 7ª TRLGSS: EOJ 2026."""
    return "65 años" if anos_cotizados * 12 >= 459 else "66 años y 10 meses"


def generar_briefing_s12(dispatcher) -> dict:
    """
    Genera un caso de jubilación con datos aleatorios pero legalmente correctos.
    Cada llamada produce un caso diferente.
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

    opciones_anos = [15, 18, 20, 22, 25, 27, 30, 32, 35, 37, 38.5, 40, 42, 45]
    anos_cotizados = rng.choice(opciones_anos)
    bc_mensual = base_cotizacion_aleatoria(rng, minimo=1323.0, maximo=4000.0)
    edad_jubilacion = 65 if anos_cotizados * 12 >= 459 else 67

    pct = _calcular_porcentaje_pension(anos_cotizados)
    br = round(bc_mensual * 300 / 350, 2)
    pension = round(br * (pct / 100), 2)
    eoj = _calcular_eoj(anos_cotizados)

    pronombre = "él" if genero == "masculino" else "ella"
    articulo = "El trabajador" if genero == "masculino" else "La trabajadora"

    return {
        "personaje": nombre,
        "empresa": empresa,
        "ciudad": ciudad_caso,
        "genero": genero,
        "edad": edad_jubilacion,
        "anos_cotizados": anos_cotizados,
        "bc_mensual": bc_mensual,
        "tema": "jubilacion",
        "descripcion": (
            f"{nombre}, de {edad_jubilacion} años, ha trabajado {anos_cotizados} años "
            f"en el Régimen General como empleado/a de {empresa} en {ciudad_caso}. "
            f"Su base de cotización mensual es de {bc_mensual:.2f}€. "
            f"Acude al CAISS para informarse sobre su pensión de jubilación."
        ),
        "calculos_verificados": {
            "eoj_aplicable": eoj,
            "br_calculada": br,
            "porcentaje_pension": pct,
            "pension_resultante": pension,
            "umbral_100pct": "36 años y 6 meses (DT 9ª 2026)",
        }
    }


BP_S12.generar_briefing = generar_briefing_s12
