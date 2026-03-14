"""
Calculadora de Presupuesto — Gestión Financiera AGE
====================================================
Implementa los 7 tipos de cálculo presupuestario del bloque V del docx
Mapa_Calculos_Examenes_AGE_v1.

Fuentes normativas:
  - Ley 47/2003 General Presupuestaria (LGP)
  - Ley 38/2003 General de Subvenciones (LGS)
  - RD 725/1989 Anticipos de Caja Fija (ACF)
  - RD 640/1987 Régimen de Pagos a Justificar (PJ)
  - RD 2188/1995 Fiscalización interna IGAE
  - PGCP Plan General de Contabilidad Pública
"""

from decimal import Decimal, ROUND_HALF_UP
from datetime import date, datetime, timedelta
from typing import Optional, Dict, Any, List

D  = lambda x: Decimal(str(x))
R2 = lambda x: x.quantize(D("0.01"), rounding=ROUND_HALF_UP)
R4 = lambda x: x.quantize(D("0.0001"), rounding=ROUND_HALF_UP)

# ---------------------------------------------------------------------------
# CONSTANTES
# ---------------------------------------------------------------------------

# Tipos de interés de demora 2026 (art. 26 LGP) — BOE 2026
INTERES_DEMORA_2026 = D("0.05125")  # 5,125% (referencia legal vigente)

# Tramos de reintegro de subvenciones — art. 36 bis LGS (escalonado)
# pct_incumplimiento → pct_reintegro
TABLA_REINTEGRO_SUBVENCIONES: List[Dict[str, Any]] = [
    {"min": 0,    "max": 10,  "pct_reintegro": 10},
    {"min": 10,   "max": 25,  "pct_reintegro": 25},
    {"min": 25,   "max": 50,  "pct_reintegro": 50},
    {"min": 50,   "max": 75,  "pct_reintegro": 75},
    {"min": 75,   "max": 100, "pct_reintegro": 100},
]


# ===========================================================================
# 1. DISPONIBILIDAD DE CRÉDITO — Gestión presupuestaria (AD-O-P)
# ===========================================================================

def calcular_credito_disponible(
    credito_inicial: float,
    ampliaciones: float = 0.0,
    suplementos: float = 0.0,
    transferencias_entrada: float = 0.0,
    transferencias_salida: float = 0.0,
    incorporaciones: float = 0.0,
    generaciones: float = 0.0,
    obligaciones_reconocidas: float = 0.0,
    compromisos: float = 0.0,
) -> Dict[str, Any]:
    """
    Calcula el crédito disponible en una partida presupuestaria.
    
    Crédito definitivo = CI + Ampliaciones + Suplementos ± Transferencias
                          + Incorporaciones + Generaciones
    Crédito disponible = Crédito definitivo − Obligaciones reconocidas − Compromisos

    Fuente: Arts. 43-55 Ley 47/2003 LGP; art. 26 RD 2188/1995
    """
    ci   = D(str(credito_inicial))
    amp  = D(str(ampliaciones))
    sup  = D(str(suplementos))
    t_en = D(str(transferencias_entrada))
    t_sa = D(str(transferencias_salida))
    inc  = D(str(incorporaciones))
    gen  = D(str(generaciones))
    ob   = D(str(obligaciones_reconocidas))
    com  = D(str(compromisos))

    credito_definitivo = ci + amp + sup + t_en - t_sa + inc + gen
    credito_disponible = credito_definitivo - ob - com

    return {
        "credito_inicial": float(ci),
        "modificaciones": {
            "ampliaciones": float(amp),
            "suplementos": float(sup),
            "transferencias_entrada": float(t_en),
            "transferencias_salida": float(t_sa),
            "incorporaciones": float(inc),
            "generaciones": float(gen),
            "TOTAL_modificaciones": float(amp + sup + t_en - t_sa + inc + gen),
        },
        "CREDITO_DEFINITIVO": float(credito_definitivo),
        "obligaciones_reconocidas": float(ob),
        "compromisos_adquiridos": float(com),
        "CREDITO_DISPONIBLE": float(R2(credito_disponible)),
        "superavit_deficit": "SUPERÁVIT" if credito_disponible >= 0 else "DÉFICIT DE CRÉDITO",
        "articulo": "Arts. 43-55 Ley 47/2003 LGP",
    }


# ===========================================================================
# 2. MODIFICACIONES PRESUPUESTARIAS
# ===========================================================================

TIPOS_MODIFICACION = {
    "ampliacion": {
        "descripcion": "Aumenta los créditos de un programa hasta el importe reconocible legalmente",
        "origen": "Ingresos afectados o habilitación normativa",
        "aprobacion": "Ministerio de Hacienda (o Consejo de Ministros si > cuantía reglamentaria)",
        "articulo": "Art. 54 LGP",
    },
    "suplemento": {
        "descripcion": "Aumenta créditos no ampliables por insuficiencia sobrevenida",
        "origen": "Requiere Ley de Crédito Suplementario o se hace vía PGE modificado",
        "aprobacion": "Cortes Generales (Ley)",
        "articulo": "Art. 55 LGP",
    },
    "transferencia": {
        "descripcion": "Traslado de crédito de un concepto/programa a otro",
        "origen": "Crédito existente en otra partida",
        "aprobacion": "Ministerio según cuantía; CM si implica cambio de sección",
        "articulo": "Art. 52 LGP",
        "limitaciones": "No puede trasladar créditos de personal a otros capítulos ni de cap. 6 a corrientes salvo excepciones",
    },
    "incorporacion": {
        "descripcion": "Reserva para ejercicio siguiente de créditos no utilizados",
        "origen": "Remanentes comprometidos por contratos, proyectos, etc.",
        "aprobacion": "Ministerio de Hacienda",
        "articulo": "Art. 58 LGP",
    },
    "generacion": {
        "descripcion": "Crédito generado por ingresos sobrevenidos no previstos",
        "origen": "Ingresos reales > las previsiones del PGE",
        "aprobacion": "Ministerio de Hacienda con habilitación en LGP",
        "articulo": "Art. 53 LGP",
    },
    "distribucion_temporal": {
        "descripcion": "Distribución del crédito en trimestres para su libración",
        "origen": "Gestión interna por Intervención",
        "aprobacion": "No requiere autorización externa",
        "articulo": "Art. 59 LGP",
    },
}


def calcular_modificacion_presupuestaria(
    tipo: str,
    importe: float,
    credito_actual: float,
    justificacion: str = "",
) -> Dict[str, Any]:
    """
    Informa sobre una modificación presupuestaria y sus efectos.
    
    Tipos válidos: ampliacion, suplemento, transferencia, incorporacion,
                   generacion, distribucion_temporal
    
    Fuente: Arts. 52-59 Ley 47/2003 LGP
    """
    tipo_norm = tipo.lower().replace("ó", "o").replace("á", "a").replace("é", "e")
    # Alias comunes
    aliases = {
        "ampliacion_credito": "ampliacion",
        "suplemento_credito": "suplemento",
        "incorporacion_credito": "incorporacion",
        "generacion_credito": "generacion",
    }
    tipo_norm = aliases.get(tipo_norm, tipo_norm)

    if tipo_norm not in TIPOS_MODIFICACION:
        return {
            "error": f"Tipo '{tipo}' no reconocido",
            "tipos_validos": list(TIPOS_MODIFICACION.keys()),
        }

    info = TIPOS_MODIFICACION[tipo_norm]
    nuevo_credito = D(str(credito_actual)) + D(str(importe))

    return {
        "tipo_modificacion": tipo_norm,
        "descripcion": info["descripcion"],
        "importe_modificacion": importe,
        "credito_anterior": credito_actual,
        "credito_resultante": float(R2(nuevo_credito)),
        "origen_credito": info["origen"],
        "organo_aprobacion": info["aprobacion"],
        "limitaciones": info.get("limitaciones", "Ver art. referenciado"),
        "justificacion": justificacion or "---",
        "articulo": info["articulo"],
    }


# ===========================================================================
# 3. ANTICIPO DE CAJA FIJA (ACF)
# ===========================================================================

def calcular_anticipo_caja_fija(
    dotacion_acf: float,
    importe_pago: float,
    concepto: str = "",
) -> Dict[str, Any]:
    """
    Verifica si un pago puede realizarse vía Anticipo de Caja Fija (ACF)
    y determina el remanente disponible.
    
    El ACF es una excepción al principio de caja única — art. 79 LGP.
    Límites: cada pago ≤ importe máximo fijado en la resolución de dotación.
    Los gastos tienen que ser gastos de importe menor (cap. 2 y 6 corrientes).
    
    Fuente: Art. 79 Ley 47/2003 LGP; RD 725/1989
    """
    dot = D(str(dotacion_acf))
    pag = D(str(importe_pago))

    if pag > dot:
        status = "DENEGADO — el pago supera la dotación ACF disponible"
        remanente = D("0")
    else:
        status = "APROBADO — pago factible con ACF"
        remanente = R2(dot - pag)

    return {
        "dotacion_acf": float(dot),
        "importe_pago_solicitado": float(pag),
        "concepto": concepto,
        "STATUS": status,
        "remanente_tras_pago": float(remanente),
        "procedimiento": "El cajero pagador tramita directamente; justifica a Intervención antes de reposición",
        "gastos_admitidos": "Capítulo 2 (gastos corrientes) e importe menor; NO contratos mayores",
        "reposicion": "Mediante nómina de cargo al PGE periódicamente",
        "articulo": "Art. 79 Ley 47/2003 LGP | RD 725/1989",
    }


# ===========================================================================
# 4. PAGOS A JUSTIFICAR (PJ)
# ===========================================================================

def calcular_plazo_justificacion_pj(
    fecha_pago_str: str,
    tipo_exterior: bool = False,
) -> Dict[str, Any]:
    """
    Calcula el plazo para justificar Pagos a Justificar (PJ).
    
    Plazo interior:  3 meses (art. 73.4 LGP)  
    Plazo exterior:  6 meses (pagos en el extranjero)
    
    Reintegro si no se justifica: el habilitado responde personalmente.
    
    Fuente: Art. 73 Ley 47/2003 LGP; RD 640/1987
    """
    try:
        fecha_pago = date.fromisoformat(fecha_pago_str)
    except ValueError:
        return {"error": "fecha_pago_str debe ser 'YYYY-MM-DD'"}

    meses = 6 if tipo_exterior else 3
    # Calcular fecha límite (por meses exactos — de fecha a fecha)
    from dateutil.relativedelta import relativedelta  # type: ignore
    try:
        fecha_limite = fecha_pago + relativedelta(months=meses)
    except ImportError:
        # Fallback sin dateutil: aproximación 30 días/mes
        fecha_limite = fecha_pago + timedelta(days=meses * 30)

    return {
        "fecha_pago": fecha_pago_str,
        "tipo": "Exterior" if tipo_exterior else "Interior",
        "plazo_meses": meses,
        "fecha_limite_justificacion": str(fecha_limite),
        "consecuencia_retraso": "Responsabilidad del habilitado/cajero pagador — reintegro con intereses de demora",
        "documentos_justificativos": "Facturas, recibos, cuentas justificativas según arts. 72-74 LGP",
        "articulo": "Art. 73.4 Ley 47/2003 LGP | RD 640/1987",
    }


# ===========================================================================
# 5. REINTEGRO DE SUBVENCIONES
# ===========================================================================

def calcular_reintegro_subvencion(
    importe_subvencion: float,
    pct_incumplimiento: float,
    fecha_cobro_str: str = "",
    fecha_reintegro_str: str = "",
) -> Dict[str, Any]:
    """
    Calcula el importe a reintegrar por incumplimiento de subvención.
    
    Proporcionalidad: arts. 36-37 LGS + RD 887/2006 (Reglamento).
    Intereses de demora: devengados desde el cobro hasta el reintegro.
    
    Fuente: Arts. 36-37 Ley 38/2003 LGS; RD 887/2006 Reglamento
    """
    subv = D(str(importe_subvencion))
    inc_pct = D(str(pct_incumplimiento))

    # Buscar tramo de reintegro
    pct_r = D("100")  # por defecto 100% si no se encuentra tramo
    tramo_desc = "Incumplimiento total (100%)"
    for t in TABLA_REINTEGRO_SUBVENCIONES:
        if D(str(t["min"])) <= inc_pct < D(str(t["max"])):
            pct_r = D(str(t["pct_reintegro"]))
            tramo_desc = f"Incumplimiento {t['min']}%–{t['max']}% → reintegro del {t['pct_reintegro']}%"
            break

    importe_reintegrar = R2(subv * pct_r / D("100"))

    # Intereses de demora (si se proporcionan fechas)
    interes_info: Dict[str, Any] = {}
    if fecha_cobro_str and fecha_reintegro_str:
        try:
            f_cobro    = date.fromisoformat(fecha_cobro_str)
            f_reintegro = date.fromisoformat(fecha_reintegro_str)
            dias_demora  = (f_reintegro - f_cobro).days
            tasa_diaria  = INTERES_DEMORA_2026 / D("365")
            interes      = R2(importe_reintegrar * tasa_diaria * D(str(dias_demora)))
            total_con_interes = R2(importe_reintegrar + interes)
            interes_info = {
                "dias_demora": dias_demora,
                "tasa_anual": f"{float(INTERES_DEMORA_2026*100):.4f}%",
                "interes_demora": float(interes),
                "TOTAL_A_REINTEGRAR_CON_INTERESES": float(total_con_interes),
            }
        except ValueError:
            interes_info = {"error": "Fechas en formato incorrecto (YYYY-MM-DD)"}

    return {
        "importe_subvencion": importe_subvencion,
        "pct_incumplimiento": float(inc_pct),
        "tramo_aplicado": tramo_desc,
        "pct_reintegro": float(pct_r),
        "IMPORTE_A_REINTEGRAR": float(importe_reintegrar),
        "intereses_demora": interes_info or "Proporcionar fechas para calcular",
        "plazo_reintegro": "Voluntario: plazo concedido en resolución. Ejecutivo: vía apremio (art. 17 RGR)",
        "articulo": "Arts. 36-37 Ley 38/2003 LGS | Art. 26 LGP (intereses)",
    }


# ===========================================================================
# 6. VERIFICACIÓN CONTABLE — Asientos PGCP
# ===========================================================================

def identificar_asiento_pgcp(
    operacion: str,
) -> Dict[str, Any]:
    """
    Identifica la cuenta del PGCP y el tipo de asiento para operaciones
    habituales en exámenes AGE.
    
    operacion: 'obligacion_presupuestaria' | 'cobro_recurso' | 'pago_proveedor'
               | 'dotacion_acf' | 'reposicion_acf' | 'reconocimiento_derecho'
               | 'anulacion_credito' | 'devolucion_ingreso'
    
    Fuente: Plan General de Contabilidad Pública (PGCP 2010, adaptación AGE 2021)
    """
    ASIENTOS = {
        "obligacion_presupuestaria": {
            "haber": "400 - Acreedores por obligaciones reconocidas",
            "debe": "Cuentas de gasto del presupuesto (capítulo correspondiente)",
            "nota": "Fase 'O' del ciclo presupuestario",
        },
        "pago_proveedor": {
            "haber": "400 - Acreedores",
            "debe": "570/571 - Caja/Bancos",
            "nota": "Fase 'P' — libramiento y pago material",
        },
        "cobro_recurso": {
            "debe": "570/571 - Caja/Bancos",
            "haber": "430 - Deudores por derechos reconocidos",
            "nota": "Cobro de derechos previamente reconocidos",
        },
        "dotacion_acf": {
            "debe": "553 - Anticipos de caja fija",
            "haber": "570 - Caja",
            "nota": "Dotación o reposición del ACF desde Tesoro Público",
        },
        "reposicion_acf": {
            "debe": "Cuentas de gasto presupuestario",
            "haber": "400 - Acreedores",
            "nota": "Formalización contable de los pagos realizados con ACF",
        },
        "reconocimiento_derecho": {
            "debe": "430 - Deudores",
            "haber": "Cta. ingresos presupuestarios",
            "nota": "Fase 'DR' — liquidación del recurso",
        },
        "devolucion_ingreso": {
            "debe": "Cta. ingresos (minoración)",
            "haber": "400 Acreedores / 570 Caja",
            "nota": "Devolución de ingresos indebidos — art. 31 LGP",
        },
    }

    op_norm = operacion.lower().replace(" ", "_")
    if op_norm not in ASIENTOS:
        return {
            "error": f"Operación '{operacion}' no reconocida",
            "operaciones_validas": list(ASIENTOS.keys()),
        }

    return {
        "operacion": operacion,
        **ASIENTOS[op_norm],
        "fuente": "PGCP 2010 (adaptación AGE 2021)",
    }


# ===========================================================================
# 7. INFORME DE AUDITORÍA — Revisión de cuentas
# ===========================================================================

def calcular_plazo_rendicion_cuentas(
    ejercicio: int,
) -> Dict[str, Any]:
    """
    Calcula los plazos de rendición de cuentas al Tribunal de Cuentas.
    
    - Entidades del sector público estatal: Cuenta General antes del 31/10/año+1
    - Tribunales y demás organismos: 30/06 del año siguiente al cierre
    - Plazo rendición departamental al IGAE: 30/04
    
    Fuente: Art. 137 LGP; Ley 7/1988 Funcionamiento Tribunal de Cuentas
    """
    return {
        "ejercicio": ejercicio,
        "plazo_rendicion_IGAE": f"30 de abril de {ejercicio + 1}",
        "plazo_cuenta_general": f"31 de octubre de {ejercicio + 1}",
        "plazo_tribunal_cuentas": f"Las cuentas individuales: 30 de junio de {ejercicio + 1}",
        "nota_IGAE": "La IGAE consolida la Cuenta General del Estado",
        "nota_TCu": "El Tribunal de Cuentas aprueba la Cuenta General y emite Declaración definitiva",
        "articulo": "Art. 137 Ley 47/2003 LGP | Ley 7/1988 Funcionamiento TCu",
    }


# ===========================================================================
# DISPATCHER INTERNO PRESUPUESTO
# ===========================================================================

TOOLS_PRESUPUESTO = {
    "calcular_credito_disponible": calcular_credito_disponible,
    "calcular_modificacion_presupuestaria": calcular_modificacion_presupuestaria,
    "calcular_anticipo_caja_fija": calcular_anticipo_caja_fija,
    "calcular_plazo_justificacion_pj": calcular_plazo_justificacion_pj,
    "calcular_reintegro_subvencion": calcular_reintegro_subvencion,
    "identificar_asiento_pgcp": identificar_asiento_pgcp,
    "calcular_plazo_rendicion_cuentas": calcular_plazo_rendicion_cuentas,
}


def ejecutar_calculo_presupuesto(nombre_tool: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Router para las calculadoras de presupuesto y gestión financiera."""
    if nombre_tool not in TOOLS_PRESUPUESTO:
        return {
            "error": f"Tool '{nombre_tool}' no encontrada en calculadora_presupuesto",
            "disponibles": list(TOOLS_PRESUPUESTO.keys()),
        }

    import inspect
    func = TOOLS_PRESUPUESTO[nombre_tool]
    sig  = inspect.signature(func)
    filtered = {k: v for k, v in (params or {}).items() if k in sig.parameters}

    try:
        return func(**filtered)
    except Exception as e:
        return {"error": f"Error ejecutando {nombre_tool}: {str(e)}"}
