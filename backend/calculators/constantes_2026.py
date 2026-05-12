"""
Constantes numéricas anuales 2026 para el Sistema de Seguridad Social español.
Verificadas contra fuentes BOE oficiales.

⚠️ FECHA DE CORTE LEGAL DEL EXAMEN: 04/03/2026.
   Solo se incluyen normas publicadas en BOE ≤ 04/03/2026 sin efecto retroactivo.
   La Orden PJC/297/2026 (BOE 31/03/2026) NO se cita: es POSTERIOR al corte.

Fuentes vigentes a 04/03/2026:
  - RDL 16/2025, de 23 de diciembre (BOE 24/12/2025) — fija cuantías SS 2026
    (SMI, pensión máxima, MEI 0,90%, topes cotización, revalorización 2,7%)
  - Orden PJC/178/2025, de 24 de febrero (BOE 26/02/2025) — desarrollo cotización
    (prorrogada con ajustes por RDL 16/2025 hasta nueva Orden 2026)
  - RDL 3/2026, de 3 de febrero (BOE-A-2026-1481) — revalorización pensiones detallada
  - RD 126/2026, de 11 de febrero (BOE-A-2026-1968) — SMI 2026 (1.221,00 €/mes)
  - RDL 2/2023 (vigencia 1/1/2026) — lagunas RETA post-cese actividad (Art. 322 TRLGSS)
  - RDL 11/2024 (vigente desde 01/04/2025) — escala jubilación activa, BR IT
"""

from decimal import Decimal

# ─── SMI ─────────────────────────────────────────────────────────────────────
SMI_MENSUAL_2026: Decimal = Decimal("1221.00")          # RD 126/2026
SMI_DIARIO_2026: Decimal = Decimal("40.70")             # 1221 / 30
SMI_ANUAL_14_PAGAS_2026: Decimal = Decimal("17094.00")  # 1221 × 14

# ─── BASES DE COTIZACIÓN ──────────────────────────────────────────────────────
TOPE_MAXIMO_COTIZACION_2026: Decimal = Decimal("5101.20")   # Art. 5 Orden PJC/297/2026
BASE_MIN_GRUPO10_2026: Decimal = Decimal("1424.40")         # SMI × 7/6 (Art. 2.2 Orden)

# ─── TIPOS DE COTIZACIÓN CONTINGENCIAS COMUNES ───────────────────────────────
TIPO_CC_EMPRESA_2026: Decimal = Decimal("23.60")     # %
TIPO_CC_TRABAJADOR_2026: Decimal = Decimal("4.70")   # %
TIPO_CC_TOTAL_2026: Decimal = Decimal("28.30")       # %

# ─── MEI (Mecanismo de Equidad Intergeneracional) ────────────────────────────
MEI_EMPRESA_2026: Decimal = Decimal("0.72")    # % — 0.90 × 0.80
MEI_TRABAJADOR_2026: Decimal = Decimal("0.18") # % — 0.90 × 0.20
MEI_TOTAL_2026: Decimal = Decimal("0.90")      # % total (Art. 6 Orden PJC/297/2026)

# ─── DESEMPLEO ────────────────────────────────────────────────────────────────
TIPO_DESEMPLEO_CONTRATO_INDEFINIDO_EMPRESA_2026: Decimal = Decimal("5.50")
TIPO_DESEMPLEO_CONTRATO_INDEFINIDO_TRABAJADOR_2026: Decimal = Decimal("1.55")
TIPO_DESEMPLEO_CONTRATO_TEMPORAL_EMPRESA_2026: Decimal = Decimal("6.70")
TIPO_DESEMPLEO_CONTRATO_TEMPORAL_TRABAJADOR_2026: Decimal = Decimal("1.60")

# ─── FOGASA ───────────────────────────────────────────────────────────────────
TIPO_FOGASA_2026: Decimal = Decimal("0.20")   # % (empresa)

# ─── FORMACIÓN PROFESIONAL ───────────────────────────────────────────────────
TIPO_FP_EMPRESA_2026: Decimal = Decimal("0.60")    # %
TIPO_FP_TRABAJADOR_2026: Decimal = Decimal("0.10") # %

# ─── PENSIÓN MÁXIMA ───────────────────────────────────────────────────────────
PENSION_MAXIMA_MENSUAL_2026: Decimal = Decimal("3359.60")   # RDL 3/2026
PENSION_MAXIMA_ANUAL_2026: Decimal = Decimal("47034.40")    # × 14 pagas

# ─── PENSIONES MÍNIMAS (referencia, indexadas a IPREM) ───────────────────────
PENSION_MINIMA_JUBILACION_CONYUGUE_NO_CARGO_2026: Decimal = Decimal("783.10")

# ─── REVALORIZACIÓN 2026 ─────────────────────────────────────────────────────
REVALORIZACION_PENSIONES_2026: Decimal = Decimal("2.7")  # % (IPC medio 2025)

# ─── IPREM ────────────────────────────────────────────────────────────────────
IPREM_MENSUAL_2026: Decimal = Decimal("610.00")
IPREM_DIARIO_2026: Decimal = Decimal("20.33")
IPREM_ANUAL_2026: Decimal = Decimal("7320.00")       # × 12
IPREM_ANUAL_14_PAGAS_2026: Decimal = Decimal("8540.00") # × 14

# ─── ADICIONAL DE SOLIDARIDAD 2026 (Art. 19 ter TRLGSS) ─────────────────────
# Norma: RDL 2/2023, vigencia desde 01/01/2025+; cuantías/tramos 2026 según
# RDL 16/2025 (BOE 24/12/2025) y desarrollo Orden cotización 2026.
# Aplica solo a la retribución que SUPERE la base máxima de cotización (5.101,20€).
# CORRECCIÓN 29/04/2026: los % anteriores (5.5/6/7) eran INCORRECTOS.
# Fuente verificada: cambios_dm_2026.py (FUENTE DE VERDAD academia DM).

CUOTA_SOLIDARIDAD_TRAMO_1_LIMITES = (Decimal("5101.20"), Decimal("5611.32"))
CUOTA_SOLIDARIDAD_TRAMO_1_TIPO_TOTAL: Decimal = Decimal("1.15")     # % total (10% sobre tope)
CUOTA_SOLIDARIDAD_TRAMO_1_TIPO_EMPRESA: Decimal = Decimal("0.96")   # % empresa
CUOTA_SOLIDARIDAD_TRAMO_1_TIPO_TRABAJADOR: Decimal = Decimal("0.19")# % trabajador

CUOTA_SOLIDARIDAD_TRAMO_2_LIMITES = (Decimal("5611.32"), Decimal("7651.80"))
CUOTA_SOLIDARIDAD_TRAMO_2_TIPO_TOTAL: Decimal = Decimal("1.25")     # % total (10-50% sobre tope)
CUOTA_SOLIDARIDAD_TRAMO_2_TIPO_EMPRESA: Decimal = Decimal("1.04")   # % empresa
CUOTA_SOLIDARIDAD_TRAMO_2_TIPO_TRABAJADOR: Decimal = Decimal("0.21")# % trabajador

CUOTA_SOLIDARIDAD_TRAMO_3_LIMITES = (Decimal("7651.80"), None)      # >50% sobre tope, sin techo
CUOTA_SOLIDARIDAD_TRAMO_3_TIPO_TOTAL: Decimal = Decimal("1.46")     # % total (>50% sobre tope)
CUOTA_SOLIDARIDAD_TRAMO_3_TIPO_EMPRESA: Decimal = Decimal("1.22")   # % empresa
CUOTA_SOLIDARIDAD_TRAMO_3_TIPO_TRABAJADOR: Decimal = Decimal("0.24")# % trabajador

# Aliases legacy para compatibilidad (si algún código antiguo los usa, ahora correctos):
CUOTA_SOLIDARIDAD_TRAMO_1_DESDE: Decimal = TOPE_MAXIMO_COTIZACION_2026
CUOTA_SOLIDARIDAD_TRAMO_1_TIPO: Decimal = CUOTA_SOLIDARIDAD_TRAMO_1_TIPO_TOTAL
CUOTA_SOLIDARIDAD_TRAMO_2_TIPO: Decimal = CUOTA_SOLIDARIDAD_TRAMO_2_TIPO_TOTAL
CUOTA_SOLIDARIDAD_TRAMO_3_TIPO: Decimal = CUOTA_SOLIDARIDAD_TRAMO_3_TIPO_TOTAL

# ─── EDAD LEGAL JUBILACIÓN 2026 ───────────────────────────────────────────────
EDAD_JUBILACION_ORDINARIA_2026_COTIZADOS_SUFICIENTES: int = 65  # con >= 38a 3m cotizados
EDAD_JUBILACION_ORDINARIA_2026_SIN_SUFICIENTES: str = "66 años y 10 meses"  # < 38a 3m (DT 7ª TRLGSS, trampa C2)
ANOS_COTIZADOS_UMBRAL_JUBILACION_2026: float = 38.25  # 38 años y 3 meses

# ─── RECAUDACIÓN SS — Plazos (Art. 55 RD 1415/2004) ─────────────────────────
# Reclamación de deuda: último día hábil del mes siguiente a la notificación
# (DISTINTO del sistema LGT donde el plazo es el día 20 del mes siguiente)
PLAZO_RECLAMACION_DEUDA_SS: str = "último día hábil del mes siguiente a la notificación"

# ─── PRESTACIÓN POR CESE DE ACTIVIDAD (RETA) ────────────────────────────────
# Tras RDL 2/2023 (vigente 1/1/2026): integración de lagunas de cotización
# en los 6 meses SIGUIENTES a la extinción del cese de actividad.
# (Art. 322 TRLGSS)
MESES_INTEGRACION_LAGUNAS_RETA_POST_CESE_2026: int = 6
