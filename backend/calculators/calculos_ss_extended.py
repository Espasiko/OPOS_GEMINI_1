"""
CALCULADORAS EXTENDIDAS SEGURIDAD SOCIAL
=========================================
Implementa 9 tipos de cálculos adicionales a los ya existentes (IT, IMV).

Tipos de cálculos (11 TOTAL):
  ✅ 1. Subsidio IT (Incapacidad Temporal) - En calculos_ss.py
  ✅ 2. IMV (Ingreso Mínimo Vital) - En calculos_imv.py
  📋 3. Pensión IPT (Incapacidad Permanente Total)
  📋 4. Jubilación (con anticipos, incrementos por edad)
  📋 5. Subsidio Desempleo (70%/60% según semanas cotizadas)
  📋 6. Cuota Cotización (aportaciones empresario/trabajador)
  📋 7. Complementos a pensiones (complementos mínimos)
  📋 8. Devoluciones por no derecho (cálculo de reembolsos)
  📋 9. Maternidad/Paternidad (16-18 semanas)
  📋 10. Ayuda hijo a cargo (por descendientes)
  📋 11. Bonificaciones en cuotas (reducciones cotización)

Fuentes normativas:
  - TRLGSS (Texto Refundido Ley General SS): Art. 133-225
  - RD 1993/1995: Cálculos y cuantías
  - RD 1109/2018: Pensiones no contributivas
  - Orden SSI/2926/2017: Incrementos aplicables

Precisión: Centavos (0,01€) - uso de Decimal
Autor: OpositaIA - Viabilidad Phase 1.1
Fecha: 13/02/2026
"""

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import date, timedelta
import calendar


# ============================================================================
# ENUMS Y TIPOS
# ============================================================================

class TipoIncapacidad(Enum):
    """Clasificación de incapacidad permanente."""
    PARCIAL = "Parcial"
    TOTAL = "Total"
    ABSOLUTA = "Absoluta"
    GRAN_INVALIDEZ = "Gran Invalidez"


class TipoDesempleo(Enum):
    """Niveles de subsidio de desempleo."""
    NIVEL_70 = Decimal("0.70")  # 70% base 180 días
    NIVEL_60 = Decimal("0.60")  # 60% base 180 días
    PROLONGADO_60 = Decimal("0.60")  # 60% prolongado 90 días


class TipoComplemento(Enum):
    """Tipos de complementos a pensiones."""
    MINIMO = "Complemento Mínimo"
    HIJO_CARGO = "Por Hijo a Cargo"
    CONYUGE_CARGO = "Por Cónyuge a Cargo"
    ASCENDIENTE = "Por Ascendiente"


# ============================================================================
# DATACLASSES - RESULTADOS
# ============================================================================

@dataclass
class ResultadoIPT:
    """Resultado cálculo Incapacidad Permanente Total."""
    tipo_incapacidad: TipoIncapacidad
    base_reguladora_diaria: Decimal
    porcentaje_pension: Decimal  # 55% para IPT
    pension_mensual: Decimal
    pension_anual: Decimal
    vigencia_desde: date
    aplicacion_ley: str
    explicacion: str


@dataclass
class ResultadoJubilacion:
    """Resultado cálculo Jubilación."""
    edad: int
    edad_ordinaria: float  # Edad legal de jubilación ordinaria calculada
    semanas_cotizadas: int
    base_reguladora_mensual: Decimal
    factor_anticipacion: Decimal  # <0.8 si anticipada
    porcentaje_acumulado: Decimal  # Hasta 100%
    pension_base: Decimal
    incrementos: Dict[str, Decimal] = field(default_factory=dict)
    pension_neta: Decimal = Decimal("0")
    complemento_minimo: Decimal = Decimal("0")
    explicacion: str = ""


@dataclass
class ResultadoDesempleo:
    """Resultado cálculo Subsidio Desempleo."""
    base_reguladora_diaria: Decimal
    porcentaje_aplicable: Decimal
    duracion_dias: int
    subsidio_diario: Decimal
    subsidio_total: Decimal
    tipo_subsidio: TipoDesempleo
    vigencia_desde: date
    vigencia_hasta: date
    explicacion: str


@dataclass
class ResultadoCuota:
    """Resultado cálculo Cuota Cotización."""
    salario_base: Decimal
    tipo_contrato: str  # "Indefinido" / "Temporal"
    aportacion_empleado: Decimal
    aportacion_empresario: Decimal
    aportacion_total: Decimal
    reducciones_aplicadas: Dict[str, Decimal] = field(default_factory=dict)
    porcentaje_efectivo_empresario: Decimal = Decimal("0")
    explicacion: str = ""


@dataclass
class ResultadoMaternidad:
    """Resultado cálculo Maternidad/Paternidad."""
    tipo_prestacion: str  # "Maternidad" / "Paternidad"
    semanas_disponibles: int
    semanas_utilizadas: int
    base_reguladora_diaria: Decimal
    prestacion_diaria: Decimal
    prestacion_total: Decimal
    fecha_inicio: date
    fecha_fin: date
    explicacion: str


@dataclass
class ResultadoComplemento:
    """Resultado cálculo Complementos a Pensiones."""
    tipo_complemento: TipoComplemento
    cantidad_dependientes: int
    importe_unitario: Decimal
    importe_total: Decimal
    aplicacion_desde: date
    compatibilidad_otras_prestaciones: bool
    explicacion: str


# ============================================================================
# CALCULADORA 1: INCAPACIDAD PERMANENTE TOTAL
# ============================================================================

class CalculadoraIPT:
    """
    Calcula Pensión de Incapacidad Permanente Total (IPT).
    
    Normativa: TRLGSS Art. 194.1 - 55% de base reguladora
    Requisitos:
      - Incapacidad permanente y total para profesión habitual
      - Base reguladora = promedio últimos 24 meses cotizados
      - Mínimo 300 semanas cotizadas (enfermedad) o accidente
    """
    
    # Cuantías vigentes 2026
    PENSION_MINIMA_IPT = Decimal("676.00")
    BASE_REGULADORA_MINIMA = Decimal("1229.09")
    PORCENTAJE_IPT = Decimal("0.55")
    
    @staticmethod
    def calcular_ipt(
        base_reguladora_mensual: Decimal,
        tipo_incapacidad: TipoIncapacidad = TipoIncapacidad.TOTAL,
        edad_al_reconocimiento: int = 35,
        vigencia_desde: Optional[date] = None
    ) -> ResultadoIPT:
        """
        Calcula pensión de Incapacidad Permanente Total.
        
        Args:
            base_reguladora_mensual: Base reguladora en euros/mes
            tipo_incapacidad: Tipo de incapacidad
            edad_al_reconocimiento: Edad cuando se reconoce la IPT
            vigencia_desde: Fecha de inicio de la pensión
        
        Returns:
            ResultadoIPT con cálculo y detalles
        """
        base_reg = Decimal(str(base_reguladora_mensual))
        base_reg_diaria = base_reg / Decimal("30")
        
        # IPT: 55% de base reguladora
        pension_mensual = base_reg * CalculadoraIPT.PORCENTAJE_IPT
        
        # Aplicar mínimo
        if pension_mensual < CalculadoraIPT.PENSION_MINIMA_IPT:
            pension_mensual = CalculadoraIPT.PENSION_MINIMA_IPT
        
        vigencia = vigencia_desde or date.today()
        
        return ResultadoIPT(
            tipo_incapacidad=tipo_incapacidad,
            base_reguladora_diaria=base_reg_diaria.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            porcentaje_pension=CalculadoraIPT.PORCENTAJE_IPT,
            pension_mensual=pension_mensual.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            pension_anual=pension_mensual * Decimal("12") + Decimal("0"),  # Prorrateos
            vigencia_desde=vigencia,
            aplicacion_ley="TRLGSS Art. 194.1 - Pensión IPT 55%",
            explicacion=f"IPT: Base reguladora {base_reg}€ × 55% = {pension_mensual}€/mes (mínimo aplicable)"
        )

# ============================================================================
# CALCULADORA 1.1: INCAPACIDAD PERMANENTE PARCIAL (IPP)
# ============================================================================

class CalculadoraIPP:
    """
    Calcula la indemnización a tanto alzado de la IPP.
    
    Normativa: TRLGSS Art. 194.1.a y Art. 196.1
    Requisitos:
      - Disminución no inferior al 33% en rendimiento normal para profesión habitual.
      - NO impide la realización de las tareas fundamentales de la misma.
    Cuantía: 24 mensualidades de la base reguladora.
    """
    
    @staticmethod
    def calcular_ipp(base_reguladora_mensual: Decimal) -> Dict[str, Any]:
        base_reg = Decimal(str(base_reguladora_mensual))
        indemnizacion = base_reg * Decimal("24")
        
        return {
            "grado": "Parcial (IPP)",
            "requisito_principal": "Disminución rendimiento >= 33%",
            "cuantia_indemnizacion": float(indemnizacion.quantize(Decimal("0.01"))),
            "mensualidades": 24,
            "articulo": "Art. 196.1 TRLGSS",
            "explicacion": f"IPP: Pago único de 24 mensualidades (Base {base_reg}€ × 24 = {indemnizacion}€)."
        }


# ============================================================================
# CALCULADORA 2: JUBILACIÓN
# ============================================================================

class CalculadoraJubilacion:
    """
    Calcula Pensión de Jubilación Ordinaria y Anticipada con tabla transitoria 2026.
    
    Normativa: TRLGSS Art. 161-166 y Disposición Transitoria 4ª.
    Requisitos 2026:
      - Edad legal: 67 años si < 38 años y 6 meses cotizados.
      - Edad legal: 65 años si >= 38 años y 6 meses cotizados.
      - Carencia mínima: 15 años (2 de ellos en los últimos 15 años).
      - BR: Promedio bases últimos 300 meses (25 años) / 350.
    """
    
    # Valores 2026
    PENSION_MINIMA_JUBILACION = Decimal("783.10") # Con cónyuge no a cargo
    PENSION_MAXIMA_JUBILACION = Decimal("3359.60") # Tope máximo 2026 (RDL 3/2026 + Orden PJC/297/2026)
    IPREM_2026_MENSUAL = Decimal("610.00")
    
    @staticmethod
    def obtener_edad_legal_2026(anos_cotizados: float) -> float:
        """
        Determina la edad legal de jubilación según la DT 7ª del TRLGSS para el año 2026.
        Umbral Crítico: 38 años y 3 meses (38.25 años).
        """
        if anos_cotizados >= 38.25: 
            # >= 38 años y 3 meses
            return 65.0
        # < 38 años y 3 meses -> 66 años y 10 meses
        return 66.83333333333333 

    @staticmethod
    def calcular_porcentaje_por_anos(anos: float) -> Decimal:
        """
        Calcula el porcentaje de la BR según años cotizados (TRLGSS Art. 210).
        - Primeros 15 años: 50%
        - Por cada mes adicional entre el mes 1 y el 49: +0.21%
        - Por cada mes adicional a partir del mes 50: +0.19%
        """
        if anos < 15:
            return Decimal("0")
        
        porcentaje = Decimal("50.0")
        meses_adicionales = int((anos - 15) * 12)
        
        if meses_adicionales <= 0:
            return porcentaje
            
        # Tramo 1: Meses 1 al 49 adicionales (+0.21% cada uno)
        tramo1 = min(meses_adicionales, 49)
        porcentaje += Decimal(str(tramo1)) * Decimal("0.21")
        
        # Tramo 2: Meses 50 en adelante (+0.19% cada uno)
        if meses_adicionales > 49:
            tramo2 = meses_adicionales - 49
            porcentaje += Decimal(str(tramo2)) * Decimal("0.19")
            
        return min(porcentaje, Decimal("100.0"))

    @staticmethod
    def calcular_jubilacion(
        base_reguladora_mensual: Decimal,
        edad_solicitud: float,
        anos_cotizados: float,
        es_anticipada: bool = False,
        tipo_anticipada: str = "voluntaria" # "voluntaria" o "involuntaria"
    ) -> ResultadoJubilacion:
        """
        Calcula pensión de Jubilación real con coeficientes reductores por mes.
        """
        base_reg = Decimal(str(base_reguladora_mensual))
        edad_legal = CalculadoraJubilacion.obtener_edad_legal_2026(anos_cotizados)
        
        # 1. Porcentaje por años cotizados
        porcentaje_base = CalculadoraJubilacion.calcular_porcentaje_por_anos(anos_cotizados)
        pension_inicial = base_reg * (porcentaje_base / Decimal("100"))
        
        # 2. Coeficientes reductores si es anticipada (Cómputo por meses)
        factor_reductivo = Decimal("1.0")
        if es_anticipada and edad_solicitud < edad_legal:
            meses_anticipo = int((edad_legal - edad_solicitud) * 12)
            if tipo_anticipada == "voluntaria":
                # Escalas de la Ley 21/2021 (simplificado lineal mensual entre max y min)
                if anos_cotizados < 38.25:
                    max_red, min_red = 0.21, 0.0281
                elif anos_cotizados < 41.5:
                    max_red, min_red = 0.19, 0.0267
                elif anos_cotizados < 44.5:
                    max_red, min_red = 0.17, 0.0253
                else:
                    max_red, min_red = 0.13, 0.0188
                
                # Interpolación lineal para 24 meses
                reduccion = max_red - ((24 - meses_anticipo) * ((max_red - min_red) / 23)) if meses_anticipo <= 24 else max_red
            else: # involuntaria
                if anos_cotizados < 38.25:
                    max_red, min_red = 0.30, 0.005
                elif anos_cotizados < 41.5:
                    max_red, min_red = 0.28, 0.0047
                elif anos_cotizados < 44.5:
                    max_red, min_red = 0.26, 0.0044
                else:
                    max_red, min_red = 0.24, 0.004
                
                # Interpolación para 48 meses
                reduccion = max_red - ((48 - meses_anticipo) * ((max_red - min_red) / 47)) if meses_anticipo <= 48 else max_red

            reduccion = max(Decimal(str(min_red)), min(Decimal(str(max_red)), Decimal(str(reduccion))))
            factor_reductivo = Decimal("1.0") - reduccion
        
        pension_final = pension_inicial * factor_reductivo
        
        # 3. Límites Mínimo/Máximo
        complemento_minimo = Decimal("0")
        if pension_final < CalculadoraJubilacion.PENSION_MINIMA_JUBILACION:
            complemento_minimo = CalculadoraJubilacion.PENSION_MINIMA_JUBILACION - pension_final
            pension_final = CalculadoraJubilacion.PENSION_MINIMA_JUBILACION
            
        pension_final = min(pension_final, CalculadoraJubilacion.PENSION_MAXIMA_JUBILACION)
        
        explicacion = (
            f"Jubilación 2026: Edad legal {edad_legal} años. Solicitada a los {edad_solicitud}. "
            f"Cotizados {anos_cotizados} años → {porcentaje_base}% de la BR. "
        )
        if es_anticipada:
            explicacion += f"Anticipo de {int((edad_legal - edad_solicitud)*12)} meses aplica coeficiente {factor_reductivo:.4f}. "
        
        return ResultadoJubilacion(
            edad=int(edad_solicitud),
            edad_ordinaria=float(edad_legal),
            semanas_cotizadas=int(anos_cotizados * 52),
            base_reguladora_mensual=base_reg,
            factor_anticipacion=factor_reductivo,
            porcentaje_acumulado=porcentaje_base,
            pension_base=pension_inicial.quantize(Decimal("0.01")),
            pension_neta=pension_final.quantize(Decimal("0.01")),
            complemento_minimo=complemento_minimo.quantize(Decimal("0.01")),
            explicacion=explicacion
        )

class CalculadoraJubilacionParcial:
    """
    Calcula Jubilación Parcial según RDL 11/2024.
    
    Requisitos RDL 11/2024 (Manufacturera):
      - Antigüedad: 6 años en la empresa.
      - Cotización: 33 años (25 en discapacidad >33%).
      - Reducción: 25% a 67% (o 80% si hay contrato de relevo indefinido).
      - Vigencia: Prórroga hasta 2029.
    """
    
    @staticmethod
    def calcular_parcial(
        base_reguladora_mensual: Decimal,
        edad: int,
        anos_cotizados: int,
        antiguedad_empresa: int,
        es_manufacturera: bool = False,
        reduccion_jornada: float = 0.50
    ) -> Dict[str, Any]:
        base_reg = Decimal(str(base_reguladora_mensual))
        reduccion = Decimal(str(reduccion_jornada))
        
        # Validaciones de requisitos
        errores = []
        if antiguedad_empresa < 6:
            errores.append("Antigüedad insuficiente (mínimo 6 años)")
        
        carencia_min = 33
        if es_manufacturera:
            # RDL 11/2024 específico
            if anos_cotizados < 33:
                errores.append("Carencia insuficiente para sector manufacturero RDL 11/2024 (mínimo 33 años)")
        else:
            if anos_cotizados < 15:
                errores.append("Carencia mínima general no alcanzada (15 años)")
                
        # Porcentaje de pensión es el inverso de la reducción (simplificado)
        porcentaje_pension = reduccion * 100
        pension_mensual = base_reg * reduccion
        
        return {
            "pension_mensual": float(pension_mensual.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "reduccion_aplicada": f"{reduccion*100}%",
            "es_manufacturera": es_manufacturera,
            "cumple_requisitos": len(errores) == 0,
            "errores": errores,
            "normativa": "RDL 11/2024" if es_manufacturera else "TRLGSS Art. 215",
            "explicacion": f"Jubilación parcial con reducción del {reduccion*100}%. Cuantía: {pension_mensual}€."
        }


# ============================================================================
# CALCULADORA 2.1: PENSIÓN NO CONTRIBUTIVA (PNC)
# ============================================================================

@dataclass
class ResultadoPNC:
    """Resultado cálculo Pensión No Contributiva."""
    tipo: str # "Jubilación" / "Invalidez"
    cuantia_anual_integra: Decimal
    cuantia_mensual: Decimal
    complemento_alquiler: Decimal
    cumple_requisitos: bool
    explicacion: str

class CalculadoraPNC:
    """
    Calcula Pensión No Contributiva (PNC) - Jubilación e Invalidez 2026.
    
    Normativa: TRLGSS Art. 363-372. Modificación 2026 según previsiones.
    """
    CUANTIA_INTEGRA_2026 = Decimal("8803.20") # Anual 2026
    LIMITE_RENTAS_SOLO = Decimal("8803.20")
    COMPLEMENTO_ALQUILER = Decimal("525.00") # Anual
    
    @staticmethod
    def calcular_pnc(
        tipo: str, 
        ingresos_anuales: Decimal, 
        edad: int, 
        grado_discapacidad: int = 0,
        residencia_anios: int = 0,
        vive_solo: bool = True
    ) -> ResultadoPNC:
        """Calcula PNC atendiendo a edad, residencia y rentas."""
        cumple = True
        motivos = []
        
        # 1. Requisitos de edad y residencia
        if tipo == "Jubilación":
            if edad < 65: cumple = False; motivos.append("Falta edad (min 65)")
            if residencia_anios < 10: cumple = False; motivos.append("Residencia insuficiente (min 10 años)")
        else: # Invalidez
            if edad < 18 or edad > 65: cumple = False; motivos.append("Edad fuera de rango (18-65)")
            if grado_discapacidad < 65: cumple = False; motivos.append("Discapacidad insuficiente (min 65%)")
            if residencia_anios < 5: cumple = False; motivos.append("Residencia insuficiente (min 5 años)")
            
        # 2. Cómputo de rentas
        if ingresos_anuales >= CalculadoraPNC.LIMITE_RENTAS_SOLO:
            cumple = False
            motivos.append(f"Exceso de rentas (max {CalculadoraPNC.LIMITE_RENTAS_SOLO}€)")
            
        if not cumple:
            return ResultadoPNC(tipo, Decimal("0"), Decimal("0"), Decimal("0"), False, "Denegada: " + ", ".join(motivos))
            
        # 3. Cuantía (Mínimo del 25% de la íntegra si hay rentas altas)
        cuantia_mensual = (CalculadoraPNC.CUANTIA_INTEGRA_2026 / Decimal("14")).quantize(Decimal("0.01"))
        
        return ResultadoPNC(
            tipo=tipo,
            cuantia_anual_integra=CalculadoraPNC.CUANTIA_INTEGRA_2026,
            cuantia_mensual=cuantia_mensual,
            complemento_alquiler=CalculadoraPNC.COMPLEMENTO_ALQUILER,
            cumple_requisitos=True,
            explicacion=f"PNC de {tipo} aprobada. Cuantía mensual de {cuantia_mensual}€. Sujeta a revisión anual de rentas."
        )


# ============================================================================
# CALCULADORA 3: DESEMPLEO
# ============================================================================

class CalculadoraDesempleo:
    """
    Calcula Subsidio por Desempleo (Prestación Contributiva) con topes 2026.
    
    Normativa: TRLGSS Art. 262-273.
    Topes IPREM 2026:
      - Sin hijos: Mín 560€ / Máx 1225€
      - 1 hijo: Mín 749€ / Máx 1400€
      - 2 o más: Máx 1575€
    """
    
    # Valores 2026
    IPREM_2026_MENSUAL = Decimal("610.00")
    
    @staticmethod
    def obtener_topes(hijos_a_cargo: int) -> Dict[str, Decimal]:
        """Calcula topes según IPREM y situación familiar."""
        if hijos_a_cargo == 0:
            return {"min": Decimal("560.00"), "max": Decimal("1225.00")}
        elif hijos_a_cargo == 1:
            return {"min": Decimal("749.00"), "max": Decimal("1400.00")}
        else:
            return {"min": Decimal("749.00"), "max": Decimal("1575.00")}

    @staticmethod
    def calcular_subsidio_desempleo(
        base_reguladora_diaria: Decimal,
        dias_cotizados_total: int,
        hijos_a_cargo: int = 0,
        vigencia_desde: Optional[date] = None
    ) -> ResultadoDesempleo:
        """
        Calcula subsidio contributivo atendiendo a la BR y los topes por hijos.
        """
        base_reg_d = Decimal(str(base_reguladora_diaria))
        base_reg_m = base_reg_d * Decimal("30")
        
        # 1. Porcentaje (70% primeros 180 días, 60% después)
        # Se devuelve el cálculo medio para un periodo dado o se especifica el tramo
        porcentaje = Decimal("0.70") 
        prestacion_mensual = base_reg_m * porcentaje
        
        # 2. Aplicación de topes
        topes = CalculadoraDesempleo.obtener_topes(hijos_a_cargo)
        if prestacion_mensual < topes["min"]:
            prestacion_mensual = topes["min"]
        elif prestacion_mensual > topes["max"]:
            prestacion_mensual = topes["max"]
            
        subsidio_diario = (prestacion_mensual / Decimal("30")).quantize(Decimal("0.01"))
        
        # 3. Duración (Cómputo según escala TRLGSS)
        if dias_cotizados_total < 360:
            duracion_dias = 0 # No llega al mínimo contributivo
        else:
            # Escala simplificada: cada 2 años cotizados ~ 8 meses
            duracion_dias = int((dias_cotizados_total / 3) * 0.66) # Aproximación
            duracion_dias = min(duracion_dias, 720) # Máx 2 años
            
        vigencia = vigencia_desde or date.today()
        
        return ResultadoDesempleo(
            base_reguladora_diaria=base_reg_d,
            porcentaje_aplicable=porcentaje,
            duracion_dias=duracion_dias,
            subsidio_diario=subsidio_diario,
            subsidio_total=(subsidio_diario * Decimal(str(duracion_dias))).quantize(Decimal("0.01")),
            tipo_subsidio=TipoDesempleo.NIVEL_70,
            vigencia_desde=vigencia,
            vigencia_hasta=vigencia + timedelta(days=duracion_dias),
            explicacion=f"Desempleo: BR {base_reg_m}€ → {porcentaje*100}% = {prestacion_mensual}€/mes (sujeto a topes: {topes['min']}€-{topes['max']}€ para {hijos_a_cargo} hijos)."
        )


# ============================================================================
# CALCULADORA 4: MATERNIDAD/PATERNIDAD (NACIMIENTO Y CUIDADO MENOR)
# ============================================================================

class CalculadoraMaternidad:
    """
    Calcula prestaciones por Nacimiento y Cuidado de Menor.
    
    Normativa: TRLGSS Art. 177-178
    Requisitos:
      - 16 semanas intransferibles (6 obligatorias ininterrumpidas tras parto)
    """
    
    @staticmethod
    def calcular_maternidad(
        base_reguladora_diaria: Decimal,
        semanas_solicitadas: int = 16,
        es_paternidad: bool = False,
        fecha_inicio: Optional[date] = None
    ) -> ResultadoMaternidad:
        """
        Calcula prestación por nacimiento y cuidado.
        """
        base_reg_d = Decimal(str(base_reguladora_diaria))
        tipo_prestacion = "Cuidado del Menor (Otro progenitor)" if es_paternidad else "Cuidado del Menor (Madre biológica)"
        
        # Semanas: Normal = 16
        semanas_util = min(semanas_solicitadas, 16)
        dias_totales = semanas_util * 7
        
        # Prestación = 100% de base reguladora diaria
        prestacion_diaria = base_reg_d
        prestacion_total = prestacion_diaria * Decimal(str(dias_totales))
        
        fecha = fecha_inicio or date.today()
        fecha_fin = fecha + timedelta(weeks=semanas_util)
        
        return ResultadoMaternidad(
            tipo_prestacion=tipo_prestacion,
            semanas_disponibles=16,
            semanas_utilizadas=semanas_util,
            base_reguladora_diaria=base_reg_d,
            prestacion_diaria=prestacion_diaria.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            prestacion_total=prestacion_total.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            fecha_inicio=fecha,
            fecha_fin=fecha_fin,
            explicacion=f"{tipo_prestacion}: {base_reg_d}€/día × {dias_totales} días = {prestacion_total}€"
        )


# ============================================================================
# CALCULADORA 5: COMPLEMENTOS A PENSIONES
# ============================================================================

class CalculadoraComplementos:
    """
    Calcula Complementos a Pensiones.
    
    Normativa: TRLGSS Art. 196-207, RD 1108/1981 (mínimos)
    Tipos:
      - Complemento mínimo de pensión
      - Complemento por hijo a cargo
      - Complemento por cónyuge a cargo
    """
    
    # Cuantías vigentes 2026
    COMPLEMENTO_MINIMO_JUBILACION = Decimal("270.50")
    COMPLEMENTO_MINIMO_IPT = Decimal("186.50")
    IMPORTE_HIJO_CARGO = Decimal("48.00")  # Por cada hijo
    IMPORTE_CONYUGE_CARGO = Decimal("96.00")
    
    @staticmethod
    def calcular_complemento_minimo(
        pension_actual: Decimal,
        tipo_pension: str = "Jubilación"  # "Jubilación" / "IPT"
    ) -> ResultadoComplemento:
        """
        Calcula complemento mínimo de pensión.
        
        Args:
            pension_actual: Pensión sin complemento
            tipo_pension: Tipo de pensión
        
        Returns:
            ResultadoComplemento
        """
        pension = Decimal(str(pension_actual))
        
        # Determinar mínimo según tipo
        minimo = (
            CalculadoraComplementos.COMPLEMENTO_MINIMO_JUBILACION
            if tipo_pension == "Jubilación"
            else CalculadoraComplementos.COMPLEMENTO_MINIMO_IPT
        )
        
        # Si la pensión es menor que el mínimo, aplicar complemento
        importe_complemento = max(Decimal("0"), minimo - pension)
        
        return ResultadoComplemento(
            tipo_complemento=TipoComplemento.MINIMO,
            cantidad_dependientes=0,
            importe_unitario=Decimal("1"),
            importe_total=importe_complemento.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            aplicacion_desde=date.today(),
            compatibilidad_otras_prestaciones=True,
            explicacion=f"Complemento mínimo: Mínimo {minimo}€ - Pensión {pension}€ = {importe_complemento}€"
        )
    
    @staticmethod
    def calcular_complemento_hijos(
        cantidad_hijos: int,
        edad_minima_hijos: int = 10
    ) -> ResultadoComplemento:
        """
        Calcula complemento por hijos a cargo.
        
        Args:
            cantidad_hijos: Número de hijos a cargo
            edad_minima_hijos: Edad mínima de los hijos
        
        Returns:
            ResultadoComplemento
        """
        importe_total = (
            Decimal(str(cantidad_hijos)) *
            CalculadoraComplementos.IMPORTE_HIJO_CARGO
        )
        
        return ResultadoComplemento(
            tipo_complemento=TipoComplemento.HIJO_CARGO,
            cantidad_dependientes=cantidad_hijos,
            importe_unitario=CalculadoraComplementos.IMPORTE_HIJO_CARGO,
            importe_total=importe_total,
            aplicacion_desde=date.today(),
            compatibilidad_otras_prestaciones=True,
            explicacion=f"Complemento hijos: {cantidad_hijos} × {CalculadoraComplementos.IMPORTE_HIJO_CARGO}€ = {importe_total}€"
        )


# ============================================================================
# (Main tests moved to the end of the file after all calculators)
    
# ============================================================================
# CALCULADORA 6: CUOTA COTIZACIÓN
# ============================================================================

# ============================================================================
# CALCULADORA 5.1: AUTÓNOMOS (RETA) - INGRESOS REALES 2025/2026
# ============================================================================

@dataclass
class ResultadoAutonomos:
    """Resultado cálculo cotización autónomos."""
    tramo_aplicable: str
    ingresos_netos: Decimal
    base_cotizacion_elegida: Decimal
    cuota_mensual: Decimal
    desglose: Dict[str, Decimal]
    explicacion: str

class CalculadoraAutonomos:
    """
    Calcula la cuota de autónomos según el sistema de ingresos reales (RDL 13/2022).
    """
    
    # Tabla reducida de tramos 2025/2026 (Simplificación de los 15 tramos legales)
    TRAMOS_2026 = [
        {"max_ing": Decimal("670.00"), "base_min": Decimal("653.59"), "cuota_min": Decimal("200.00")},
        {"max_ing": Decimal("900.00"), "base_min": Decimal("751.63"), "cuota_min": Decimal("230.00")},
        {"max_ing": Decimal("1166.70"), "base_min": Decimal("849.67"), "cuota_min": Decimal("260.00")},
        {"max_ing": Decimal("1300.00"), "base_min": Decimal("950.98"), "cuota_min": Decimal("291.00")},
        {"max_ing": Decimal("1500.00"), "base_min": Decimal("960.78"), "cuota_min": Decimal("294.00")},
        {"max_ing": Decimal("1700.00"), "base_min": Decimal("960.78"), "cuota_min": Decimal("294.00")},
        {"max_ing": Decimal("1850.00"), "base_min": Decimal("1013.07"), "cuota_min": Decimal("310.00")},
        {"max_ing": Decimal("2030.00"), "base_min": Decimal("1029.41"), "cuota_min": Decimal("315.00")},
        {"max_ing": Decimal("2330.00"), "base_min": Decimal("1045.75"), "cuota_min": Decimal("320.00")},
        {"max_ing": Decimal("2760.00"), "base_min": Decimal("1078.43"), "cuota_min": Decimal("330.00")},
        {"max_ing": Decimal("3190.00"), "base_min": Decimal("1143.79"), "cuota_min": Decimal("350.00")},
        {"max_ing": Decimal("3620.00"), "base_min": Decimal("1209.15"), "cuota_min": Decimal("370.00")},
        {"max_ing": Decimal("4050.00"), "base_min": Decimal("1274.51"), "cuota_min": Decimal("390.00")},
        {"max_ing": Decimal("6000.00"), "base_min": Decimal("1372.55"), "cuota_min": Decimal("420.00")},
        {"max_ing": Decimal("999999.00"), "base_min": Decimal("1633.99"), "cuota_min": Decimal("500.00")}
    ]
    
    TIPO_TOTAL_RETA = Decimal("0.314") # Comunes 28.3% + Prof 1.3% + Cese 0.9% + Formación 0.1% + MEI 2026 (0.9%)
    
    @staticmethod
    def calcular_cuota_autonomo(
        ingresos_brutos_anuales: Decimal,
        gastos_deducibles_anuales: Decimal,
        base_personalizada: Optional[Decimal] = None
    ) -> ResultadoAutonomos:
        """
        Calcula la cuota de autónomos tras aplicar la deducción por gastos genéricos (7%).
        """
        ingr_b = Decimal(str(ingresos_brutos_anuales))
        gastos = Decimal(str(gastos_deducibles_anuales))
        
        # 1. Rendimiento Neto Anual
        rendimiento_neto = ingr_b - gastos
        # 2. Deducción gastos genéricos (7%)
        rendimiento_computable_mensual = (rendimiento_neto * Decimal("0.93")) / Decimal("12")
        
        # 3. Localizar tramo
        tramo_info = CalculadoraAutonomos.TRAMOS_2026[-1]
        for t in CalculadoraAutonomos.TRAMOS_2026:
            if rendimiento_computable_mensual <= t["max_ing"]:
                tramo_info = t
                break
        
        # 4. Base de cotización
        base_basica = tramo_info["base_min"]
        if base_personalizada and base_personalizada > base_basica:
            base_final = base_personalizada
        else:
            base_final = base_basica
            
        # 5. Cuota (Base * 31.4%)
        cuota = (base_final * CalculadoraAutonomos.TIPO_TOTAL_RETA).quantize(Decimal("0.01"))
        
        return ResultadoAutonomos(
            tramo_aplicable=f"Hasta {tramo_info['max_ing']}€",
            ingresos_netos=rendimiento_computable_mensual.quantize(Decimal("0.01")),
            base_cotizacion_elegida=base_final,
            cuota_mensual=cuota,
            desglose={
                "Contingencias Comunes": (base_final * Decimal("0.283")).quantize(Decimal("0.01")),
                "Contingencias Profesionales": (base_final * Decimal("0.013")).quantize(Decimal("0.01")),
                "Cese Actividad": (base_final * Decimal("0.009")).quantize(Decimal("0.01")),
                "Formación Profesional": (base_final * Decimal("0.001")).quantize(Decimal("0.01")),
                "MEI (2026)": (base_final * Decimal("0.009")).quantize(Decimal("0.01"))
            },
            explicacion=f"RETA 2026: Rendimiento mensual computable {rendimiento_computable_mensual:.2f}€. Tramo aplicado: {tramo_info['max_ing']}€. Cuota base: {cuota}€ (31.4%)."
        )


class CalculadoraCuota:
    """
    Calcula Cuota de Cotización a la Seguridad Social.
    
    Normativa: TRLGSS Art. 282-305, RD 2064/1995 (tipos de cotización)
    Componentes:
      - Aportación del trabajador
      - Aportación del empresario
      - Bonificaciones y reducciones aplicables
    """
    
    # Tipos de cotización vigentes 2026 (% sobre base cotizable)
    TIPOS_COTIZACION = {
        "Contingencias Comunes": Decimal("3.60"),  # Trabajador
        "Desempleo": Decimal("1.55"),  # Trabajador (varía empresa)
        "Formación Profesional": Decimal("0.10"),  # Trabajador
        "Fondo Garantía Salarial": Decimal("0.20"),  # Solo empresa
    }
    
    APORTACION_EMPRESARIO_BASE = Decimal("29.90")  # Contingencias comunes
    
    @staticmethod
    def calcular_cuota(
        salario_bruto_mensual: Decimal,
        tipo_contrato: str = "Indefinido",
        grupo_cotizacion: int = 1
    ) -> ResultadoCuota:
        """
        Calcula cuota mensual de cotización.
        
        Args:
            salario_bruto_mensual: Salario bruto mensual
            tipo_contrato: "Indefinido" o "Temporal"
            grupo_cotizacion: Grupo de cotización (1-11)
        
        Returns:
            ResultadoCuota con detalles
        """
        salario = Decimal(str(salario_bruto_mensual))
        
        # Aportación del trabajador
        aportacion_trabajador = salario * (
            Decimal("3.60") +  # Contingencias
            Decimal("1.55") +  # Desempleo
            Decimal("0.10")    # Formación
        ) / Decimal("100")
        
        # Aportación del empresario (simplificado)
        aportacion_empresario = salario * Decimal("29.90") / Decimal("100")
        
        # Reducciones para contrato temporal (si aplica)
        reducciones = {}
        if tipo_contrato == "Temporal" and grupo_cotizacion >= 8:
            reduccion_temporal = aportacion_empresario * Decimal("0.30")  # 30% descuento
            aportacion_empresario -= reduccion_temporal
            reducciones["Reducción contrato temporal"] = reduccion_temporal
        
        aportacion_total = aportacion_trabajador + aportacion_empresario
        
        porcentaje_efectivo = (
            (aportacion_empresario / salario) * Decimal("100")
            if salario > 0 else Decimal("0")
        )
        
        return ResultadoCuota(
            salario_base=salario,
            tipo_contrato=tipo_contrato,
            aportacion_empleado=aportacion_trabajador.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            aportacion_empresario=aportacion_empresario.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            aportacion_total=aportacion_total.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            reducciones_aplicadas=reducciones,
            porcentaje_efectivo_empresario=porcentaje_efectivo.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            explicacion=f"Cuota: Trabajador {aportacion_trabajador:.2f}€ + Empresa {aportacion_empresario:.2f}€ = {aportacion_total:.2f}€"
        )


# ============================================================================
# CALCULADORA 7: DEVOLUCIONES POR NO DERECHO
# ============================================================================

@dataclass
class ResultadoDevolucion:
    """Resultado cálculo de devoluciones."""
    concepto_prestacion: str
    importe_indebido: Decimal
    periodos_afectados: int
    interes_legal: Decimal
    total_devoluciones: Decimal
    fecha_comunicacion: date
    plazo_reembolso_dias: int
    explicacion: str


class CalculadoraDevolucion:
    """
    Calcula Devoluciones por No Derecho.
    
    Normativa: TRLGSS Art. 215-225, RD 1670/1981 (reembolsos)
    Casos:
      - Incompatibilidad con otros ingresos no declarada
      - Exceso de límites de patrimonio
      - Cambios de situación no comunicados
    """
    
    TASA_INTERES_LEGAL = Decimal("3.5")
    PLAZO_REEMBOLSO_DIAS = 60
    
    @staticmethod
    def calcular_devolucion(
        importe_indebido: Decimal,
        periodos_afectados: int = 1,
        aplicar_interes: bool = True
    ) -> ResultadoDevolucion:
        """
        Calcula devolución por prestación indebida.
        
        Args:
            importe_indebido: Cantidad percibida indebidamente
            periodos_afectados: Meses/períodos afectados
            aplicar_interes: Si aplica interés legal
        
        Returns:
            ResultadoDevolucion
        """
        importe = Decimal(str(importe_indebido))
        
        # Calcular interés
        interes_total = Decimal("0")
        if aplicar_interes and periodos_afectados > 0:
            # Interés simple anual del 3.5%
            interes_total = (
                importe *
                (CalculadoraDevolucion.TASA_INTERES_LEGAL / Decimal("100")) *
                (Decimal(str(periodos_afectados)) / Decimal("12"))
            )
        
        total_devolucion = importe + interes_total
        
        return ResultadoDevolucion(
            concepto_prestacion="Prestación indebida",
            importe_indebido=importe.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            periodos_afectados=periodos_afectados,
            interes_legal=interes_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            total_devoluciones=total_devolucion.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            fecha_comunicacion=date.today(),
            plazo_reembolso_dias=CalculadoraDevolucion.PLAZO_REEMBOLSO_DIAS,
            explicacion=f"Devolución: {importe:.2f}€ + Interés 3.5% = {total_devolucion:.2f}€"
        )


# ============================================================================
# CALCULADORA 8: AYUDA POR HIJO A CARGO
# ============================================================================

@dataclass
class ResultadoAyudaHijo:
    """Resultado cálculo ayuda por hijo a cargo."""
    numero_hijos: int
    edad_promedio: int
    importe_unitario: Decimal
    importe_total: Decimal
    requisitos_cumplidos: bool
    vigencia_desde: date
    explicacion: str


class CalculadoraAyudaHijo:
    """
    Calcula Ayuda por Hijo a Cargo.
    
    Normativa: TRLGSS Art. 197, RD 1975/1985 (prestaciones familiares)
    Requisitos:
      - Hijo menor de 18 años (o 25 si discapacidad)
      - En España o UE
      - Límite de ingresos del grupo familiar
    """
    
    IMPORTE_POR_HIJO = Decimal("45.00")  # 2026
    LIMITE_INGRESOS_ANUAL = Decimal("16000.00")
    
    @staticmethod
    def calcular_ayuda_hijo(
        numero_hijos: int,
        ingresos_grupo_familiar: Decimal,
        edades_hijos: List[int] = None
    ) -> ResultadoAyudaHijo:
        """
        Calcula ayuda por hijos a cargo.
        
        Args:
            numero_hijos: Cantidad de hijos
            ingresos_grupo_familiar: Ingresos totales del grupo
            edades_hijos: Lista de edades de los hijos
        
        Returns:
            ResultadoAyudaHijo
        """
        ingresos = Decimal(str(ingresos_grupo_familiar))
        
        # Verificar límite de ingresos
        cumple_requisitos = ingresos <= CalculadoraAyudaHijo.LIMITE_INGRESOS_ANUAL
        
        # Calcular importe
        if cumple_requisitos:
            importe_total = (
                Decimal(str(numero_hijos)) *
                CalculadoraAyudaHijo.IMPORTE_POR_HIJO
            )
        else:
            importe_total = Decimal("0")
        
        edad_promedio = 0
        if edades_hijos:
            edad_promedio = sum(edades_hijos) // len(edades_hijos)
        
        return ResultadoAyudaHijo(
            numero_hijos=numero_hijos,
            edad_promedio=edad_promedio,
            importe_unitario=CalculadoraAyudaHijo.IMPORTE_POR_HIJO,
            importe_total=importe_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            requisitos_cumplidos=cumple_requisitos,
            vigencia_desde=date.today(),
            explicacion=f"Ayuda hijos: {numero_hijos} × {CalculadoraAyudaHijo.IMPORTE_POR_HIJO}€ = {importe_total}€" +
                       ("" if cumple_requisitos else " (NO CUMPLE LÍMITE INGRESOS)")
        )


# ============================================================================
# CALCULADORA 9: BONIFICACIONES EN CUOTAS
# ============================================================================

@dataclass
class ResultadoBonificacion:
    """Resultado cálculo bonificación en cuotas."""
    tipo_bonificacion: str
    cuota_original: Decimal
    porcentaje_bonificacion: Decimal
    importe_bonificacion: Decimal
    cuota_bonificada: Decimal
    periodo_vigencia_meses: int
    explicacion: str


class CalculadoraBonificacion:
    """
    Calcula Bonificaciones en Cuotas.
    
    Normativa: TRLGSS Art. 283-285, Ley 50/1990 (economía social)
    Tipos:
      - Contratación de jóvenes
      - Trabajadores en riesgo de exclusión
      - Cooperativas y sociedades laborales
    """
    
    BONIFICACIONES = {
        "Joven hasta 30": Decimal("45"),  # % descuento
        "Desempleado larga duración": Decimal("60"),
        "Cooperativa": Decimal("50"),
        "Discapacidad": Decimal("75"),
    }
    
    @staticmethod
    def calcular_bonificacion(
        cuota_empresarial: Decimal,
        tipo_bonificacion: str,
        duracion_meses: int = 12
    ) -> ResultadoBonificacion:
        """
        Calcula bonificación en cuota empresarial.
        
        Args:
            cuota_empresarial: Cuota empresarial bruta
            tipo_bonificacion: Tipo de bonificación
            duracion_meses: Meses de aplicación
        
        Returns:
            ResultadoBonificacion
        """
        cuota = Decimal(str(cuota_empresarial))
        porcentaje = CalculadoraBonificacion.BONIFICACIONES.get(
            tipo_bonificacion, Decimal("0")
        )
        
        importe_bonificacion = (cuota * porcentaje / Decimal("100"))
        cuota_bonificada = cuota - importe_bonificacion
        
        return ResultadoBonificacion(
            tipo_bonificacion=tipo_bonificacion,
            cuota_original=cuota.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            porcentaje_bonificacion=porcentaje,
            importe_bonificacion=importe_bonificacion.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            cuota_bonificada=cuota_bonificada.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            periodo_vigencia_meses=duracion_meses,
            explicacion=f"Bonificación {tipo_bonificacion}: {cuota:.2f}€ - {porcentaje:.0f}% = {cuota_bonificada:.2f}€"
        )

# ============================================================================
# CALCULADORA 10: VIUDEDAD
# ============================================================================

@dataclass
class ResultadoViudedad:
    """Resultado cálculo pensión de viudedad."""
    base_reguladora_mensual: Decimal
    porcentaje_aplicado: Decimal
    pension_mensual: Decimal
    tiene_cargas_familiares: bool
    articulo_aplicable: str
    explicacion: str


class CalculadoraViudedad:
    """
    Calcula Pensión de Viudedad.
    
    Normativa: TRLGSS Art. 231 - 52% base reguladora (general)
      - 60% si > 65 años sin otra pensión
      - 70% si cargas familiares + ingresos < umbral
    """
    
    PORCENTAJE_GENERAL = Decimal("0.52")
    PORCENTAJE_MAYOR_65 = Decimal("0.60")
    PORCENTAJE_CARGAS = Decimal("0.70")
    PENSION_MINIMA_VIUDEDAD = Decimal("558.00")  # 2026
    
    @staticmethod
    def calcular_viudedad(
        base_reguladora_mensual: float,
        tiene_cargas_familiares: bool = False,
        mayor_65_sin_otra_pension: bool = False
    ) -> ResultadoViudedad:
        """
        Calcula pensión de viudedad.
        
        Args:
            base_reguladora_mensual: Base reguladora en euros/mes
            tiene_cargas_familiares: Si tiene hijos a cargo + ingresos bajos
            mayor_65_sin_otra_pension: Si > 65 años sin otra pensión
        
        Returns:
            ResultadoViudedad con cálculo
        """
        base_reg = Decimal(str(base_reguladora_mensual))
        
        if tiene_cargas_familiares:
            porcentaje = CalculadoraViudedad.PORCENTAJE_CARGAS
            motivo = "70% (cargas familiares)"
        elif mayor_65_sin_otra_pension:
            porcentaje = CalculadoraViudedad.PORCENTAJE_MAYOR_65
            motivo = "60% (>65 sin otra pensión)"
        else:
            porcentaje = CalculadoraViudedad.PORCENTAJE_GENERAL
            motivo = "52% (general)"
        
        pension = (base_reg * porcentaje).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        # Aplicar mínimo
        if pension < CalculadoraViudedad.PENSION_MINIMA_VIUDEDAD:
            pension = CalculadoraViudedad.PENSION_MINIMA_VIUDEDAD
        
        return ResultadoViudedad(
            base_reguladora_mensual=base_reg,
            porcentaje_aplicado=porcentaje,
            pension_mensual=pension,
            tiene_cargas_familiares=tiene_cargas_familiares,
            articulo_aplicable="Art. 231 TRLGSS",
            explicacion=f"Viudedad: {base_reg}€ × {motivo} = {pension}€/mes"
        )


# ============================================================================
# CALCULADORA 11: ORFANDAD
# ============================================================================

@dataclass
class ResultadoOrfandad:
    """Resultado cálculo pensión de orfandad."""
    base_reguladora_mensual: Decimal
    porcentaje_por_hijo: Decimal
    numero_hijos: int
    pension_por_hijo: Decimal
    pension_total: Decimal
    es_orfandad_absoluta: bool
    articulo_aplicable: str
    explicacion: str


class CalculadoraOrfandad:
    """
    Calcula Pensión de Orfandad.
    
    Normativa: TRLGSS Art. 232-233
      - 20% BR por cada huérfano
      - Orfandad absoluta: 20% + incremento (hasta 52% BR repartido)
      - Suma viudedad+orfandad no puede superar 100% BR
    """
    
    PORCENTAJE_POR_HIJO = Decimal("0.20")
    PENSION_MINIMA_ORFANDAD = Decimal("233.60")  # 2026 por huérfano
    
    @staticmethod
    def calcular_orfandad(
        base_reguladora_mensual: float,
        numero_hijos: int = 1,
        es_orfandad_absoluta: bool = False
    ) -> ResultadoOrfandad:
        """
        Calcula pensión de orfandad.
        
        Args:
            base_reguladora_mensual: Base reguladora del causante
            numero_hijos: Número de hijos huérfanos
            es_orfandad_absoluta: Si ambos progenitores han fallecido
        
        Returns:
            ResultadoOrfandad con cálculo
        """
        base_reg = Decimal(str(base_reguladora_mensual))
        porcentaje = CalculadoraOrfandad.PORCENTAJE_POR_HIJO
        
        pension_por_hijo = (base_reg * porcentaje).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        # Orfandad absoluta: reparto del 52% de viudedad entre huérfanos
        incremento_absoluta = Decimal("0")
        if es_orfandad_absoluta and numero_hijos > 0:
            viudedad_repartida = (base_reg * Decimal("0.52")) / Decimal(str(numero_hijos))
            incremento_absoluta = viudedad_repartida.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            pension_por_hijo += incremento_absoluta
        
        # Aplicar mínimo
        if pension_por_hijo < CalculadoraOrfandad.PENSION_MINIMA_ORFANDAD:
            pension_por_hijo = CalculadoraOrfandad.PENSION_MINIMA_ORFANDAD
        
        pension_total = pension_por_hijo * Decimal(str(numero_hijos))
        
        detalle = f"Orfandad: {base_reg}€ × 20% = {pension_por_hijo}€/hijo"
        if es_orfandad_absoluta:
            detalle += f" (absoluta: +{incremento_absoluta}€ reparto viudedad)"
        
        return ResultadoOrfandad(
            base_reguladora_mensual=base_reg,
            porcentaje_por_hijo=porcentaje,
            numero_hijos=numero_hijos,
            pension_por_hijo=pension_por_hijo,
            pension_total=pension_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            es_orfandad_absoluta=es_orfandad_absoluta,
            articulo_aplicable="Art. 232-233 TRLGSS",
            explicacion=detalle
        )


# ============================================================================
# CALCULADORA 12: INCAPACIDAD PERMANENTE ABSOLUTA (IPA)
# ============================================================================

@dataclass
class ResultadoIPA:
    """Resultado cálculo Incapacidad Permanente Absoluta."""
    base_reguladora_mensual: Decimal
    porcentaje_pension: Decimal
    pension_mensual: Decimal
    es_gran_invalidez: bool
    complemento_gran_invalidez: Decimal
    pension_total_mensual: Decimal
    articulo_aplicable: str
    explicacion: str


class CalculadoraIPA:
    """
    Calcula Pensión de Incapacidad Permanente Absoluta y Gran Invalidez.
    
    Normativa: TRLGSS Art. 196
      - IPA: 100% de base reguladora
      - Gran Invalidez: 100% BR + complemento (mín 45% BR + 30% BR = +50%~)
    """
    
    PORCENTAJE_IPA = Decimal("1.00")  # 100% BR
    # Gran Invalidez: complemento = 45% base mínima cotización + 30% última BR
    # Simplificado: ~50% adicional sobre la pensión
    COMPLEMENTO_GI_MIN_PORCENTAJE = Decimal("0.45")
    COMPLEMENTO_GI_MAX_PORCENTAJE = Decimal("0.30")
    BASE_MINIMA_COTIZACION_2026 = Decimal("1323.00")
    
    @staticmethod
    def calcular_ipa(
        base_reguladora_mensual: float,
        es_gran_invalidez: bool = False
    ) -> ResultadoIPA:
        """
        Calcula pensión de IPA o Gran Invalidez.
        
        Args:
            base_reguladora_mensual: Base reguladora en euros/mes
            es_gran_invalidez: Si es Gran Invalidez (100% + complemento)
        
        Returns:
            ResultadoIPA con cálculo
        """
        base_reg = Decimal(str(base_reguladora_mensual))
        
        # IPA: 100% BR
        pension = (base_reg * CalculadoraIPA.PORCENTAJE_IPA).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        complemento_gi = Decimal("0")
        if es_gran_invalidez:
            # Complemento GI = 45% base mínima cotización + 30% última BR
            parte_a = CalculadoraIPA.BASE_MINIMA_COTIZACION_2026 * CalculadoraIPA.COMPLEMENTO_GI_MIN_PORCENTAJE
            parte_b = base_reg * CalculadoraIPA.COMPLEMENTO_GI_MAX_PORCENTAJE
            complemento_gi = (parte_a + parte_b).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        
        pension_total = pension + complemento_gi
        
        tipo = "Gran Invalidez" if es_gran_invalidez else "IPA"
        detalle = f"{tipo}: {base_reg}€ × 100% = {pension}€/mes"
        if es_gran_invalidez:
            detalle += f" + complemento GI {complemento_gi}€ = {pension_total}€/mes"
        
        return ResultadoIPA(
            base_reguladora_mensual=base_reg,
            porcentaje_pension=CalculadoraIPA.PORCENTAJE_IPA,
            pension_mensual=pension,
            es_gran_invalidez=es_gran_invalidez,
            complemento_gran_invalidez=complemento_gi,
            pension_total_mensual=pension_total,
            articulo_aplicable="Art. 196 TRLGSS",
            explicacion=detalle
        )


# ============================================================================
# CALCULADORA 13: RIESGO DURANTE EL EMBARAZO
# ============================================================================

@dataclass
class ResultadoRiesgoEmbarazo:
    """Resultado cálculo prestación riesgo embarazo/lactancia."""
    base_reguladora_diaria: Decimal
    porcentaje: Decimal
    subsidio_diario: Decimal
    tipo_riesgo: str
    articulo_aplicable: str
    explicacion: str


class CalculadoraRiesgoEmbarazo:
    """
    Calcula prestación por Riesgo durante el Embarazo o Lactancia.
    
    Normativa: TRLGSS Art. 186-187
      - 100% de base reguladora por contingencias profesionales
      - No se exige período mínimo de cotización
    """
    
    PORCENTAJE = Decimal("1.00")  # 100% BR contingencias profesionales
    
    @staticmethod
    def calcular_riesgo_embarazo(
        base_cotizacion_profesional_mensual: float,
        es_lactancia: bool = False
    ) -> ResultadoRiesgoEmbarazo:
        """
        Calcula subsidio por riesgo durante embarazo o lactancia.
        
        Args:
            base_cotizacion_profesional_mensual: Base por cont. profesionales
            es_lactancia: Si es riesgo durante lactancia natural (vs embarazo)
        
        Returns:
            ResultadoRiesgoEmbarazo con cálculo
        """
        base_mensual = Decimal(str(base_cotizacion_profesional_mensual))
        base_diaria = (base_mensual / Decimal("30")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        subsidio_diario = (base_diaria * CalculadoraRiesgoEmbarazo.PORCENTAJE).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        tipo = "Riesgo Lactancia" if es_lactancia else "Riesgo Embarazo"
        
        return ResultadoRiesgoEmbarazo(
            base_reguladora_diaria=base_diaria,
            porcentaje=CalculadoraRiesgoEmbarazo.PORCENTAJE,
            subsidio_diario=subsidio_diario,
            tipo_riesgo=tipo,
            articulo_aplicable="Art. 186-187 TRLGSS",
            explicacion=f"{tipo}: {base_mensual}€/mes ÷ 30 = {base_diaria}€/día × 100% = {subsidio_diario}€/día"
        )


# ============================================================================
# CALCULADORA 14: LESIONES PERMANENTES NO INVALIDANTES (LPNI)
# ============================================================================

@dataclass
class ResultadoLPNI:
    """Resultado cálculo indemnización LPNI."""
    tipo_lesion: str
    indemnizacion: Decimal
    es_baremo: bool
    articulo_aplicable: str
    explicacion: str


class CalculadoraLPNI:
    """
    Calcula Indemnización por Lesiones Permanentes No Invalidantes.
    
    Normativa: TRLGSS Art. 201, Orden ESS/66/2013
      - Indemnización a tanto alzado (pago único)
      - Solo para AT o EP (no contingencia común)
      - Baremo oficial con cantidades fijas por tipo de lesión
    """
    
    # Baremo simplificado (Orden ESS/66/2013, actualizado)
    BAREMO_LPNI = {
        "perdida_falange_distal": Decimal("1080.00"),
        "perdida_falange_media": Decimal("1620.00"),
        "perdida_dedo_mano": Decimal("3240.00"),
        "perdida_dedo_pie": Decimal("1620.00"),
        "anquilosis_dedo": Decimal("1080.00"),
        "cicatriz_cabeza": Decimal("2160.00"),
        "cicatriz_cuerpo": Decimal("1080.00"),
        "perdida_pieza_dental": Decimal("540.00"),
        "hipoacusia_unilateral": Decimal("2700.00"),
        "reduccion_movilidad_hombro": Decimal("3780.00"),
        "reduccion_movilidad_codo": Decimal("2700.00"),
        "reduccion_movilidad_muneca": Decimal("2160.00"),
        "reduccion_movilidad_rodilla": Decimal("3240.00"),
        "reduccion_movilidad_tobillo": Decimal("2160.00"),
    }
    
    @staticmethod
    def calcular_lpni(
        tipo_lesion: str
    ) -> ResultadoLPNI:
        """
        Calcula indemnización por LPNI según baremo.
        
        Args:
            tipo_lesion: Clave del baremo (ver BAREMO_LPNI)
        
        Returns:
            ResultadoLPNI con indemnización
        """
        indemnizacion = CalculadoraLPNI.BAREMO_LPNI.get(
            tipo_lesion, Decimal("0")
        )
        
        en_baremo = tipo_lesion in CalculadoraLPNI.BAREMO_LPNI
        
        return ResultadoLPNI(
            tipo_lesion=tipo_lesion,
            indemnizacion=indemnizacion,
            es_baremo=en_baremo,
            articulo_aplicable="Art. 201 TRLGSS + Orden ESS/66/2013",
            explicacion=f"LPNI '{tipo_lesion}': {indemnizacion}€ (baremo)" if en_baremo
                       else f"LPNI '{tipo_lesion}': no encontrada en baremo"
        )

    @staticmethod
    def listar_baremo() -> Dict[str, Decimal]:
        """Devuelve el baremo completo para consulta."""
        return dict(CalculadoraLPNI.BAREMO_LPNI)


# ============================================================================
# CALCULADORA 15: AUXILIO POR DEFUNCIÓN E INDEMNIZACIONES POR MUERTE
# ============================================================================

@dataclass
class ResultadoMuerte:
    """Resultado cálculo auxilio defunción e indemnizaciones."""
    tipo_prestacion: str
    pago_unico: Decimal
    beneficiarios: str
    articulo_aplicable: str
    explicacion: str

class CalculadoraSupervivencia:
    """
    Calcula Auxilio por Defunción e Indemnizaciones por Muerte (AT/EP).
    
    Normativa: TRLGSS Art. 216-218
      - Auxilio Defunción: Cuantía fija (46.50€).
      - Indemnización Muerte (AT/EP): Pago único adicional a viudedad/orfandad.
        * Viudo/a: 6 mensualidades BR.
        * Huérfano: 1 mensualidad BR.
        * Padres: 9 mensualidades (si 1 coincide) o 12 (si 2 coinciden).
    """
    
    AUXILIO_DEFUNCION_FIJO = Decimal("46.50")
    
    @staticmethod
    def calcular_auxilio_defuncion() -> ResultadoMuerte:
        return ResultadoMuerte(
            tipo_prestacion="Auxilio por Defunción",
            pago_unico=CalculadoraSupervivencia.AUXILIO_DEFUNCION_FIJO,
            beneficiarios="Quien haya soportado los gastos del sepelio",
            articulo_aplicable="Art. 218 TRLGSS",
            explicacion=f"Cuantía fija de {CalculadoraSupervivencia.AUXILIO_DEFUNCION_FIJO}€ para gastos de sepelio."
        )
        
    @staticmethod
    def calcular_indemnizacion_muerte_at_ep(
        base_reguladora_mensual: float,
        cantidad_huerfanos: int = 0,
        tiene_viudo: bool = True,
        fecha_hecho: Optional[date] = None
    ) -> List[ResultadoMuerte]:
        """
        Calcula indemnizaciones a tanto alzado por accidente de trabajo o enf. profesional.
        Incluye factor IPC +2.7% para hechos en 2026 (Ley 5/2025).
        """
        base = Decimal(str(base_reguladora_mensual))
        resultados = []
        
        # Factor IPC 2026 (Ley 5/2025)
        factor_ipc = Decimal("1.0")
        if fecha_hecho and fecha_hecho.year >= 2026:
            factor_ipc = Decimal("1.027")
        
        if tiene_viudo:
            pago = (base * 6 * factor_ipc).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            resultados.append(ResultadoMuerte(
                tipo_prestacion="Indemnización Especial Viudedad (AT/EP)",
                pago_unico=pago,
                beneficiarios="Cónyuge o pareja de hecho",
                articulo_aplicable="Art. 216.2 TRLGSS / Ley 5/2025",
                explicacion=f"6 mensualidades de la base reguladora ({base}€ x 6) + Factor IPC 2026 ({factor_ipc})."
            ))
            
        if cantidad_huerfanos > 0:
            pago_h = (base * Decimal(str(cantidad_huerfanos)) * factor_ipc).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            resultados.append(ResultadoMuerte(
                tipo_prestacion=f"Indemnización Especial Orfandad (AT/EP) x{cantidad_huerfanos}",
                pago_unico=pago_h,
                beneficiarios=f"{cantidad_huerfanos} hijos huérfanos",
                articulo_aplicable="Art. 217 TRLGSS / Ley 5/2025",
                explicacion=f"1 mensualidad de la base reguladora por cada hijo ({base}€ x {cantidad_huerfanos}) + Factor IPC 2026 ({factor_ipc})."
            ))
            
        return resultados

# ============================================================================
# CALCULADORA 16: CUIDADO DE MENORES CON CÁNCER (CUME)
# ============================================================================

class CalculadoraCUME:
    """
    Calcula subsidio por cuidado de menores afectados por cáncer o enf. grave.
    Normativa: Art. 190-192 TRLGSS, RD 1148/2011 (Actualizado 2023).
    """
    @staticmethod
    def calcular_cume(
        base_reguladora_it: float,
        porcentaje_reduccion: float = 0.50, # Mínimo 50%
        edad_menor: int = 10,
        tiene_discapacidad: bool = False
    ) -> Dict[str, Any]:
        base = Decimal(str(base_reguladora_it))
        reduccion = Decimal(str(porcentaje_reduccion))
        
        if reduccion < 0.5:
            return {"error": "La reducción de jornada debe ser de al menos el 50%."}
            
        prestacion_diaria = (base * reduccion).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        vigencia = "Hasta 23 años (general) o 26 años (discapacidad ≥ 65%)"
        
        return {
            "prestacion": "Subsidio Cuidado Menores Cáncer (CUME)",
            "cuantia_diaria": float(prestacion_diaria),
            "cuantia_mensual": float(prestacion_diaria * 30),
            "reduccion_jornada": f"{reduccion*100}%",
            "vigencia_maxima": vigencia,
            "articulo": "Art. 190 TRLGSS / RD 677/2023",
            "explicacion": f"100% de la BR por IT proporcional a la reducción ({reduccion*100}%). Cuantía: {prestacion_diaria}€/día."
        }

# ============================================================================
# CALCULADORA 17: BENEFICIOS POR CUIDADO DE HIJOS (ART. 235-237 LGSS)
# ============================================================================

class CalculadoraBeneficiosHijos:
    """
    Calcula periodos de cotización asimilados por parto y cuidado de hijos.
    """
    @staticmethod
    def calcular_periodos_asimilados(
        num_hijos_parto: int = 1,
        num_total_hijos: int = 1,
        dias_excedencia: int = 0
    ) -> Dict[str, Any]:
        # Art. 235: Parto
        dias_parto = 112 + (14 * max(0, num_hijos_parto - 1))
        
        # Art. 236: Cuidado (Máx 270 por hijo)
        dias_cuidado = min(270 * num_total_hijos, 1825) # Límite total 5 años
        
        # Art. 237: Excedencia (Hasta 3 años por hijo)
        dias_excedencia_comp = min(dias_excedencia, 1095) # 3 años
        
        return {
            "beneficio_parto_dias": dias_parto,
            "beneficio_cuidado_dias": dias_cuidado,
            "beneficio_excedencia_dias": dias_excedencia_comp,
            "limite_total_dias": 1825,
            "articulos": "Art. 235, 236 y 237 TRLGSS",
            "explicacion": f"Asimilación por parto: {dias_parto} días. Cuidado: hasta {dias_cuidado} días. Límite máximo global 5 años."
        }

# ============================================================================

# El motor termina aquí.


# ============================================================================
# BLOQUE CALCULADORAS EXTRA — Ejercicio 19 (12/03/2026)
# ============================================================================

# 1. Recargos SS (Art. 27, 28 y 30 TRLGSS / Art. 10.1.b RD 1415/2004)
def calcular_recargo_ss(cumplio_liquidacion: bool, en_periodo_ejecutivo: bool, pago_en_plazo_voluntario_reclamacion: bool) -> Dict[str, Any]:
    """
    Lógica exacta de recargos de la Seguridad Social.
    
    - 10%: Presentó docs de liquidación Y paga DENTRO del plazo voluntario de la reclamación de deuda.
    - 35%: NO presentó docs de liquidación O paga DESPUÉS de que venza el plazo de la reclamación.
    - 20%: Recargo de apremio estándar (notificada la providencia, aún no pagó).
    
    TRAMPA frecuente: "hasta el vencimiento del plazo" = no pagó en plazo = 35%.
    """
    if not cumplio_liquidacion:
        return {"recargo": "35%", "porcentaje": 0.35, "base": "Cuota principal",
                "explicacion": "35%: No presentó documentos de cotización. Art. 30.1.b TRLGSS / Art. 10.1.b RD 1415/2004."}
    if en_periodo_ejecutivo:
        return {"recargo": "20%", "porcentaje": 0.20, "base": "Cuota principal",
                "explicacion": "20%: Recargo de apremio estándar. Providencia notificada y no pagada en 15 días."}
    if pago_en_plazo_voluntario_reclamacion:
        return {"recargo": "10%", "porcentaje": 0.10, "base": "Cuota principal",
                "explicacion": "10%: Pago dentro del plazo voluntario concedido en la reclamación de deuda. Art. 27.1 TRLGSS."}
    # Por defecto si presentó docs pero no pagó en plazo
    return {"recargo": "35%", "porcentaje": 0.35, "base": "Cuota principal",
            "explicacion": "35%: Presentó documentos pero pagó DESPUÉS de vencer el plazo voluntario de la reclamación."}

# 2. Intereses de Demora SS (Distinción Principal vs Recargo)
def calcular_intereses_demora_ss(sobre_principal: bool, dias_retraso: int) -> Dict[str, Any]:
    """
    Principal: intereses desde el día siguiente al vencimiento del período voluntario de pago.
    Recargo de apremio: intereses desde el día 16 tras la notificación de la providencia
    (los 15 primeros días son el nuevo período voluntario ejecutivo, sin intereses del recargo).
    """
    if sobre_principal:
        return {
            "inicio_devengo": "Día 1 tras finalización periodo voluntario pago principal",
            "inicio_retraso_dias": 1,
            "explicacion": "Intereses sobre el PRINCIPAL empiezan al día siguiente del vencimiento del período voluntario original de ingreso. Art. 27.2 TRLGSS."
        }
    else:
        return {
            "inicio_devengo": "Día 16 tras notificación de la providencia de apremio",
            "inicio_retraso_dias": 16,
            "explicacion": "Intereses sobre el RECARGO DE APREMIO empiezan el día 16, NO el día 1. Los 15 primeros son el plazo voluntario ejecutivo. Art. 28 TRLGSS."
        }

# 3. IT Situaciones Especiales LO 1/2023 (vigente desde 1/06/2023)
def calcular_it_situaciones_especiales_lo1_2023(salario_base: Decimal, situacion: str) -> Dict[str, Any]:
    """
    LO 1/2023 — Tres situaciones especiales de IT:
    
    1. menstruacion: INSS desde día 1 al 60%. Sin carencia. Sin responsabilidad empresarial.
    2. interrupcion_embarazo: Empresa paga día 1 (salario íntegro). INSS desde día 2 al 100%.
    3. semana_39_gestacion: CON carencia general EC. Empresa día 1. INSS desde día 2.
    """
    situaciones_validas = {
        "menstruacion": {
            "carencia": "SIN carencia previa (EC especial)",
            "pagador_dia_1": "INSS (60%)",
            "pagador_posterior": "INSS (60%) - Toda la duración",
            "responsabilidad_empresa": False,
            "articulo": "Art. 173 bis TRLGSS (LO 1/2023)",
            "nota": "B7: INSS desde día 1 al 60%. No hay días a cargo de empresa ni trabajador."
        },
        "semana_39_gestacion": {
            "carencia": "CON carencia ordinaria de EC",
            "pagador_dia_1": "Empresa (salario íntegro)",
            "pagador_posterior": "INSS desde día 2 al 100%",
            "responsabilidad_empresa": True,
            "articulo": "Art. 173 bis TRLGSS (LO 1/2023)"
        },
        "interrupcion_embarazo": {
            "carencia": "SIN carencia",
            "pagador_dia_1": "Empresa (salario íntegro)",
            "pagador_posterior": "INSS desde día 2 al 100%",
            "responsabilidad_empresa": True,
            "articulo": "Art. 173 bis TRLGSS (LO 1/2023)"
        }
    }
    if situacion not in situaciones_validas:
        return {"error": "Situación no reconocida. Use: menstruacion, semana_39_gestacion, interrupcion_embarazo"}
    return situaciones_validas[situacion]

# 4. Base Cotización Completa — Con Taxonomía Corregida de HE
# ⚠️ CORRECCIÓN 12/03/2026: 'Estructurales' ≠ 'Fuerza Mayor'. El error era sistemático.
TIPOS_HE = {
    # Tipo HE : (empresa, trabajador, total)
    "fuerza_mayor":      (0.12,   0.02,   0.14),   # Prevenir/reparar siniestros urgentes. Tipos prorrogados por RDL 16/2025 (BOE 24/12/2025); Art. 5 Orden PJC/178/2025 vigente a 04/03/2026
    "estructurales":     (0.2360, 0.0470, 0.2830), # Habituales para la producción. 28,30% TOTAL.
    "no_estructurales":  (0.2360, 0.0470, 0.2830), # Esporádicas/voluntarias. 28,30% TOTAL.
}
# TRAMPA CONFIRMADA (Ejercicio 19 P5): Si el enunciado NO dice "fuerza mayor" → 28,30%.
# "Estructurales" NO significa "fuerza mayor". La IA (Gemini incluido) lo confundía al 14%.

def calcular_base_cotizacion_completa(
    salario_base: Decimal,
    he_cantidad: float = 0.0,
    tipo_he: str = "no_estructurales",  # 'fuerza_mayor', 'estructurales', 'no_estructurales'
    prorrata_extras: Decimal = Decimal("0"),
    plus_desplazamiento_domicilio_trabajo: Decimal = Decimal("0"),  # Siempre INCLUIR en BC
    suplidos_justificados_inwork: Decimal = Decimal("0"),            # Siempre EXCLUIR de BC
    dietas_desplazamiento_trabajo: Decimal = Decimal("0"),           # Excluir si está dentro del límite normativo
    vehiculo_uso_particular: Decimal = Decimal("0"),                # 20% valor mercado / 12 si uso particular
) -> Dict[str, Any]:
    """
    Calcula la base de cotización completa discriminando correctamente cada concepto.
    
    REGLAS CRÍTICAS DEL EJERCICIO 19:
    - Plus domicilio→trabajo: RETRIBUCIÓN → INCLUIR íntegro en BC (aunque tenga tickets/justificantes)
    - Suplidos in-work (reunión con cliente, viaje empresa): EXCLUIR de BC
    - Vehículo uso particular: INCLUIR (valor_mercado × 20% / 12). DEFAULT: incluir si hay disponibilidad.
    - HE: van en base SEPARADA, no en base de CC.
    """
    if tipo_he not in TIPOS_HE:
        tipo_he = "no_estructurales"
    emp_he, trab_he, total_he = TIPOS_HE[tipo_he]
    
    base_cc = (Decimal(str(salario_base)) 
               + Decimal(str(prorrata_extras)) 
               + Decimal(str(plus_desplazamiento_domicilio_trabajo))  # SÍ suma
               + Decimal(str(vehiculo_uso_particular)))               # SÍ suma si uso particular
    # Suplidos in-work y dietas --> NO suman
    
    base_he_separada = Decimal(str(he_cantidad))
    cuota_he_trabajador = base_he_separada * Decimal(str(trab_he))
    cuota_he_empresa = base_he_separada * Decimal(str(emp_he))
    
    return {
        "base_cotizacion_comunes": float(base_cc.quantize(Decimal("0.01"))),
        "base_horas_extras": float(base_he_separada),
        "tipo_he": tipo_he,
        "cuota_he_trabajador_pct": f"{trab_he*100:.2f}%",
        "cuota_he_trabajador": float(cuota_he_trabajador.quantize(Decimal("0.01"))),
        "cuota_he_empresa_pct": f"{emp_he*100:.2f}%",
        "cuota_he_empresa": float(cuota_he_empresa.quantize(Decimal("0.01"))),
        "excluidos_de_base": {
            "suplidos_inwork": float(suplidos_justificados_inwork),
            "dietas": float(dietas_desplazamiento_trabajo)
        },
        "trampa_detectada": "Plus domicilio→trabajo: INCLUIR SIEMPRE. HE: base separada, no en CC. Vehículo uso particular: 20% valor/12 meses."
    }

# 5. Integración Lagunas RETA vs RG
def calcular_integracion_lagunas_jubilacion(
    meses_laguna: int,
    regimen: str,
    genero: str = "H",
    post_cese_actividad_reta: bool = False,
) -> Dict[str, Any]:
    """Integración de lagunas en BR jubilación según régimen y excepción Art. 322 TRLGSS.

    REGLA GENERAL:
      - RETA: 0% (Art. 313 TRLGSS) — meses sin cotización valen 0€.
      - RG hombre/general (Art. 209.1): meses 1-48 → 100% base mínima; mes 49+ → 50%.
      - RG mujer (DA 37ª): meses 1-60 → 100%; meses 61-84 → 80%.

    EXCEPCIÓN RETA — Art. 322 TRLGSS (RDL 2/2023, vigente desde 01/01/2026):
      Cuando el autónomo ha extinguido la prestación por cese de actividad,
      los 6 MESES SIGUIENTES a esa extinción SÍ se integran (al 100% base mínima
      grupo correspondiente). Activar con post_cese_actividad_reta=True.
    """
    if regimen.upper() == "RETA":
        if post_cese_actividad_reta and meses_laguna <= 6:
            return {
                "integracion": "100%",
                "explicacion": (
                    "EXCEPCIÓN Art. 322 TRLGSS (RDL 2/2023, vigente 01/01/2026): "
                    "los 6 meses siguientes a la extinción de la prestación por cese de "
                    "actividad SÍ se integran al 100% de la base mínima del grupo. "
                    "TRAMPA INVERSA: la regla genérica RETA = 0% NO aplica en esta ventana."
                ),
                "articulo": "Art. 322 TRLGSS (modif. RDL 2/2023)",
            }
        return {
            "integracion": "0%",
            "valor_euros": 0.0,
            "explicacion": (
                "TRAMPA: En el RETA NO existe integración de lagunas (regla general). "
                "Los meses sin base cotizada computan con valor cero (0,00€). Art. 313 TRLGSS. "
                "EXCEPCIÓN: si la laguna está dentro de los 6 meses siguientes a la "
                "extinción de la prestación por cese de actividad → activar post_cese_actividad_reta=True."
            ),
            "articulo": "Art. 313 TRLGSS",
        }
    else:
        if genero.upper() == "F":
            if meses_laguna <= 60:
                return {"integracion": "100%", "explicacion": "RG mujer (DA 37ª TRLGSS): primeros 60 meses laguna → 100% base mínima."}
            elif meses_laguna <= 84:
                return {"integracion": "80%", "explicacion": "RG mujer (DA 37ª TRLGSS): meses 61-84 → 80% base mínima."}
        if meses_laguna <= 48:
            return {"integracion": "100%", "explicacion": "RG hombre/general: primeros 48 meses → 100% base mínima. Art. 209.1 TRLGSS."}
        return {"integracion": "50%", "explicacion": "RG hombre/general: a partir del mes 49 → 50% base mínima. Art. 209.1 TRLGSS."}

# 6. BR Jubilación DT34ª TRLGSS (Ley 21/2021 + RDL 2/2023)
def calcular_br_jubilacion_dt34(bases_ordenadas_descendente: List[Decimal]) -> Dict[str, Any]:
    """Recibe al menos 304 meses (25 años y 4 meses). Toma las 302 mejores / 352,33."""
    if len(bases_ordenadas_descendente) < 304:
        return {"error": f"Se necesitan 304 meses para aplicar DT 34ª. Bases recibidas: {len(bases_ordenadas_descendente)}"}
    mejores_302 = sum(bases_ordenadas_descendente[:302])
    br = mejores_302 / Decimal("352.33")
    return {
        "base_reguladora": float(br.quantize(Decimal("0.01"))),
        "bases_usadas": 302,
        "divisor": 352.33,
        "explicacion": "DT 34ª TRLGSS (RDL 2/2023): Se toman las 302 mejores bases de los últimos 304 meses y se dividen entre el divisor fijo de 352,33 (P2)."
    }

# 7. Efectos Cambio de Base RETA (RDL 13/2022 — sin ventanas trimestrales)
def calcular_fecha_efectos_cambio_base_reta(fecha_solicitud: date) -> Dict[str, Any]:
    """REGLA RDL 13/2022 (H7): El cambio de base en RETA se realiza en 6 ventanas bimestrales."""
    month = fecha_solicitud.month
    if month in (1, 2):
        efecto = date(fecha_solicitud.year, 3, 1)
    elif month in (3, 4):
        efecto = date(fecha_solicitud.year, 5, 1)
    elif month in (5, 6):
        efecto = date(fecha_solicitud.year, 7, 1)
    elif month in (7, 8):
        efecto = date(fecha_solicitud.year, 9, 1)
    elif month in (9, 10):
        efecto = date(fecha_solicitud.year, 11, 1)
    else: # 11, 12
        efecto = date(fecha_solicitud.year + 1, 1, 1)
        
    return {
        "fecha_efectos": efecto.isoformat(),
        "mes_solicitud": f"{fecha_solicitud.year}-{fecha_solicitud.month:02d}",
        "mes_efectos": f"{efecto.year}-{efecto.month:02d}",
        "explicacion": "CORRECCIÓN H7: El RDL 13/2022 establece 6 ventanas bimestrales para cambiar la base. Solicitud Ene-Feb → Efectos 1 Mar, etc."
    }

# 8. Tipo Enajenación Subasta / Embargo Inmueble (Art. 104 RD 1415/2004)
def calcular_tipo_enajenacion(valor_tasado: Decimal, cargas_anteriores: Decimal, cargas_posteriores: Decimal = Decimal("0")) -> Dict[str, Any]:
    """Solo se descuentan cargas ANTERIORES al embargo TGSS. Cargas posteriores y la deuda TGSS NO se restan."""
    tipo = Decimal(str(valor_tasado)) - Decimal(str(cargas_anteriores))
    return {
        "tipo_enajenacion": float(max(tipo, Decimal("0")).quantize(Decimal("0.01"))),
        "cargas_anteriores_deducidas": float(cargas_anteriores),
        "cargas_posteriores_NO_deducidas": float(cargas_posteriores),
        "explicacion": "Art. 103-104 RD 1415/2004: TRAMPA: Solo se descuentan cargas ANTERIORES al embargo. Las posteriores NO. La deuda TGSS tampoco se resta del valor."
    }

# 9. Jubilación Activa — Escala RDL 11/2024 (vigente desde 01/04/2025)
# ⚠️ CORRECCIÓN 12/03/2026: La escala anterior (4% por año) estaba DEROGADA. Esta es la correcta.
ESCALA_JUBILACION_ACTIVA_RDL11_2024 = {
    1: Decimal("0.45"),   # 1 año demora → 45%
    2: Decimal("0.55"),   # 2 años → 55%
    3: Decimal("0.65"),   # 3 años → 65%
    4: Decimal("0.80"),   # 4 años → 80%  ← Caso Candela Ejercicio 19
    5: Decimal("1.00"),   # ≥5 años → 100%
}

def calcular_jubilacion_activa_escala_rdl11_2024(br: Decimal, anios_demora: int, meses_en_activo_adicionales: int = 0) -> Dict[str, Any]:
    """
    Escala jubilación activa Art. 214.2 TRLGSS, tras RDL 11/2024 (vigente 01/04/2025).
    
    Paso 1: Escala por años de demora (máximo 5 años = 100%).
    Paso 2: +5 puntos porcentuales por cada 12 meses ininterrumpidos en activo (acumulativo).
    
    TRAMPA (C8): La escala antigua era 50%/100% por cuenta ajena/autónomo. YA NO EXISTE.
    TRAMPA (C6): Requisito previo = mínimo 1 año desde que se alcanzó la edad ordinaria.
    """
    anios_clamped = min(anios_demora, 5)
    porcentaje_base = ESCALA_JUBILACION_ACTIVA_RDL11_2024.get(anios_clamped, Decimal("1.00"))
    
    # Paso 2: +5pp por cada 12 meses en activo (tras haber empezado la jubilación activa)
    incremento_activo = Decimal("0.05") * (meses_en_activo_adicionales // 12)
    porcentaje_final = min(porcentaje_base + incremento_activo, Decimal("1.00"))
    
    pension = Decimal(str(br)) * porcentaje_final
    return {
        "anios_demora": anios_demora,
        "porcentaje_escala": float(porcentaje_base),
        "incremento_activo_adicional": float(incremento_activo),
        "porcentaje_final": float(porcentaje_final),
        "pension_mensual": float(pension.quantize(Decimal("0.01"))),
        "articulo": "Art. 214.2 TRLGSS (RDL 11/2024, vigente 01/04/2025)",
        "explicacion": f"{anios_demora} años demora → {float(porcentaje_base)*100:.0f}% de la pensión calculada."
    }

# 10. Derivación Responsabilidad (Solidaria vs Subsidiaria)
def calcular_derivacion_responsabilidad_ss(
    tipo_deudor: str,
    cuota: Decimal,
    recargo: Decimal,
    intereses: Decimal = Decimal("0"),
    costas: Decimal = Decimal("0"),
    titulo_ejecutivo_ya_contiene_intereses_costas: bool = False,
) -> Dict[str, Any]:
    """Alcance de la derivación de responsabilidad (Art. 18.3 + 142 + 168 TRLGSS + Art. 13 RGRSS).

    REGLA MATIZADA (actualizada 2026-04-18 tras verificación simulacro febrero DM):
    - Solidaria ORDINARIA (derivación antes de generarse intereses/costas):
        → principal + recargo (no incluye intereses ni costas).
    - Solidaria con TÍTULO EJECUTIVO YA FORMADO (ya existen intereses/costas al momento
      de la derivación, p.ej. tras providencia de apremio):
        → el responsable solidario asume el título ejecutivo COMPLETO.
    - Subsidiaria (cooperativa hacia socio, tras insolvencia del socio):
        → deuda completa incluyendo intereses y costas.

    Citas correctas: Art. 18.3 TRLGSS (responsables cuotas) + Art. 142 TRLGSS
    (sujeto responsable) + Art. 168.2 TRLGSS (supuestos especiales) + Art. 13
    RGRSS (RD 1415/2004) (alcance concreto de la derivación).
    NO es 'Art. 15 bis TRLGSS' — ese precepto no existe en el TRLGSS vigente
    (RDLeg 8/2015); es herencia obsoleta de la LGSS-1994.
    """
    if tipo_deudor.lower() in ("socio_cooperativa", "cooperativa_hacia_socio"):
        return {
            "tipo_derivacion": "Subsidiaria",
            "alcance": float(cuota + recargo + intereses + costas),
            "articulo": "Art. 142 + 168 TRLGSS; Art. 14 RGRSS (RD 1415/2004)",
            "explicacion": "Responsabilidad subsidiaria de cooperativas (tras insolvencia del socio): cuota + recargo + intereses + costas.",
        }
    if titulo_ejecutivo_ya_contiene_intereses_costas:
        return {
            "tipo_derivacion": "Solidaria (título ejecutivo formado)",
            "alcance": float(cuota + recargo + intereses + costas),
            "articulo": "Art. 18.3 + 142 TRLGSS; Art. 13 RGRSS (RD 1415/2004)",
            "explicacion": (
                "El responsable solidario asume el título ejecutivo COMPLETO cuando "
                "la derivación se produce tras generarse intereses y costas "
                "(coincide con la respuesta oficial del simulacro febrero 2026)."
            ),
        }
    return {
        "tipo_derivacion": "Solidaria (ordinaria)",
        "alcance": float(cuota + recargo),
        "intereses_excluidos": float(intereses),
        "costas_excluidas": float(costas),
        "articulo": "Art. 18.3 + 142 TRLGSS; Art. 13 RGRSS (RD 1415/2004)",
        "explicacion": (
            "TRAMPA (G4) regla simplificada: solidaria ordinaria = principal + recargo. "
            "Matiz: si el título ejecutivo ya incluye intereses/costas al derivar, "
            "se reclaman también. Usar titulo_ejecutivo_ya_contiene_intereses_costas=True."
        ),
    }

# 11. Cuota Contrato Corta Duración (≤8 días)
def calcular_cuota_contrato_corta_duracion() -> Dict[str, Any]:
    return {"cuantia_extra_fija_2026": 32.60, "tipo": "FIJO, no porcentaje",
            "articulo": "DA 43ª TRLGSS; cuantías 2026 fijadas por RDL 16/2025 (BOE 24/12/2025)",
            "explicacion": "TRAMPA (I12): Contratos de ≤8 días: recargo fijo de 32,60€ por contrato. No es un porcentaje del salario."}

# --- NUEVA --- 12. Pensión Máxima Anticipada Involuntaria (Art. 207.2 — Regla Especial)
def calcular_pension_maxima_anticipada_involuntaria(
    pension_calculada: Decimal, tope_maximo_2026: Decimal, trimestres_anticipacion: int
) -> Dict[str, Any]:
    """
    REGLA ESPECIAL (C12) Art. 207.2 TRLGSS cuando pensión calculada > tope máximo.
    
    Regla GENERAL (pensión calculada ≤ tope): aplicar coeficiente reductor ordinario sobre pensión calculada.
    Regla ESPECIAL (pensión calculada > tope): aplicar 0,5%/trimestre directamente sobre el TOPE MÁXIMO.
    
    Esta regla protege al trabajador con carreras largas: penalización menor sobre el tope
    en lugar de penalizar sobre una pensión calculada que de todas formas quedaba limitada.
    
    Tope máximo 2026 = 3.359,60€/mes (RDL 3/2026 + RDL 16/2025, vigentes a 04/03/2026).
    """
    REDUCCION_POR_TRIMESTRE_ESPECIAL = Decimal("0.005")
    
    if pension_calculada > tope_maximo_2026:
        reductor_especial = Decimal("1") - (REDUCCION_POR_TRIMESTRE_ESPECIAL * trimestres_anticipacion)
        pension_final = tope_maximo_2026 * max(reductor_especial, Decimal("0"))
        return {
            "aplica_regla_especial": True,
            "pension_calculada": float(pension_calculada),
            "tope_maximo": float(tope_maximo_2026),
            "trimestres_anticipacion": trimestres_anticipacion,
            "reductor_aplicado": f"0,5% x {trimestres_anticipacion} trimestres = {float(REDUCCION_POR_TRIMESTRE_ESPECIAL*trimestres_anticipacion)*100:.1f}%",
            "pension_final": float(pension_final.quantize(Decimal("0.01"))),
            "articulo": "Art. 207.2 TRLGSS (segundo párrafo) — Regla especial pensión > tope",
            "explicacion": f"Pensión calculada ({pension_calculada}€) supera el tope máximo ({tope_maximo_2026}€). Se aplica 0,5%/trimestre SOBRE EL TOPE, no sobre la pensión calculada. Pensión final: {float(pension_final.quantize(Decimal('0.01')))}€"
        }
    else:
        return {"aplica_regla_especial": False, "pension_calculada": float(pension_calculada),
                "explicacion": "Pensión calculada ≤ tope máximo. Usar regla general (coeficientes Art. 207.2 sobre pensión calculada)."}

# --- NUEVA --- 13. Retribución en Especie — Vehículo de Empresa
def calcular_retribucion_especie_vehiculo(valor_mercado: Decimal, tipo_uso: str = "particular") -> Dict[str, Any]:
    """
    Vehículo de empresa y Base de Cotización.
    
    - uso='exclusivo_laboral': EXCLUIR de BC. Solo si hay restricción EXPRESA de uso privado.
    - uso='particular' o 'mixto': INCLUIR en BC = valor_mercado × 20% / 12 meses.
    
    DEFAULT: INCLUIR. La exclusión es la excepción, no la regla.
    Art. 147.3 TRLGSS; Art. 43.1.b) LIRPF (por remisión Art. 23 RD 2064/1995).
    """
    if tipo_uso == "exclusivo_laboral":
        return {"incluir_en_bc": False, "importe_mensual": 0.0,
                "explicacion": "Uso EXCLUSIVAMENTE laboral con restricción expresa → excluir de BC. La exclusión requiere prohibición formal de uso privado."}
    
    importe_mensual = Decimal(str(valor_mercado)) * Decimal("0.20") / Decimal("12")
    return {
        "incluir_en_bc": True,
        "tipo_uso": tipo_uso,
        "valor_mercado": float(valor_mercado),
        "calculo": f"{float(valor_mercado)}€ × 20% / 12 = {float(importe_mensual.quantize(Decimal('0.01')))}€/mes",
        "importe_mensual_bc": float(importe_mensual.quantize(Decimal("0.01"))),
        "articulo": "Art. 147.3 TRLGSS; Art. 43.1.b) LIRPF",
        "explicacion": f"TRAMPA (F8): Si el enunciado dice 'para su uso particular' → SIEMPRE INCLUIR en BC. Importe = {float(importe_mensual.quantize(Decimal('0.01')))}€/mes."
    }

# ============================================================================
# BLOQUE NUEVO — calculadoras añadidas el 29/04/2026 (sesión Spas + Cascade)
# Todas las fuentes BOE ≤ 04/03/2026 (fecha de corte del examen).
# ============================================================================

# 14. Subsidio Cese de Actividad RETA (Art. 339 TRLGSS, RDL 13/2022)
# Trampa R5 del vault: BR 12m, 70%, duración 4-24m, topes IPREM 175%/107%.
def calcular_subsidio_cese_actividad_reta(
    bases_cotizacion_12m: List[Decimal],
    meses_cotizados_48m: int,
    tiene_responsabilidades_familiares: bool = False,
    iprem_2026_mensual: Decimal = Decimal("610.00"),
) -> Dict[str, Any]:
    """Prestación por Cese de Actividad para RETA (Art. 327-339 TRLGSS).

    Reglas vigentes a 04/03/2026 (modif. RDL 13/2022):
      - BR = promedio de 12 bases más recientes.
      - Cuantía = 70% de la BR.
      - Topes IPREM (incrementado en 1/6, igual que subsidio paro Art. 270):
          * Sin responsabilidades familiares: máx 175% IPREM × 7/6.
          * Con 1 hijo: máx 200% IPREM × 7/6.
          * Con ≥2 hijos: máx 225% IPREM × 7/6.
          * Mínimo: 80% IPREM × 7/6 (sin hijos) / 107% IPREM × 7/6 (con).
      - Duración por meses cotizados en últimos 48m:
          12-17m → 4m / 18-23m → 6m / 24-29m → 8m / 30-35m → 10m
          36-42m → 12m / 43-47m → 16m / ≥48m → 24m

    Trampa R5: el RDL 13/2022 cambió el cálculo de la BR — antes era media base
    de cotización fija, ahora es promedio de los rendimientos netos × tablas.
    """
    if len(bases_cotizacion_12m) < 12:
        return {"error": "Se requieren las 12 bases inmediatamente anteriores."}
    if meses_cotizados_48m < 12:
        return {"error": "Carencia mínima incumplida: se exigen 12 meses cotizados en los últimos 48."}

    base_reguladora = sum(bases_cotizacion_12m) / Decimal("12")
    cuantia_bruta = base_reguladora * Decimal("0.70")

    iprem_con_paga_extra = iprem_2026_mensual * Decimal("7") / Decimal("6")  # IPREM × 7/6
    if tiene_responsabilidades_familiares:
        tope_max = iprem_con_paga_extra * Decimal("2.00")  # 200% para 1 hijo
        tope_min = iprem_con_paga_extra * Decimal("1.07")  # 107%
    else:
        tope_max = iprem_con_paga_extra * Decimal("1.75")  # 175%
        tope_min = iprem_con_paga_extra * Decimal("0.80")  # 80%

    cuantia_final = max(min(cuantia_bruta, tope_max), tope_min)

    # Tabla de duración (meses cotizados → meses prestación)
    tabla = [(48, 24), (43, 16), (36, 12), (30, 10), (24, 8), (18, 6), (12, 4)]
    duracion_meses = next((d for c, d in tabla if meses_cotizados_48m >= c), 0)

    return {
        "base_reguladora": float(base_reguladora.quantize(Decimal("0.01"))),
        "porcentaje": "70%",
        "cuantia_bruta": float(cuantia_bruta.quantize(Decimal("0.01"))),
        "tope_min": float(tope_min.quantize(Decimal("0.01"))),
        "tope_max": float(tope_max.quantize(Decimal("0.01"))),
        "cuantia_final_mensual": float(cuantia_final.quantize(Decimal("0.01"))),
        "duracion_meses": duracion_meses,
        "tiene_responsabilidades_familiares": tiene_responsabilidades_familiares,
        "iprem_referencia": float(iprem_2026_mensual),
        "articulo": "Arts. 327-339 TRLGSS (modif. RDL 13/2022)",
        "explicacion": (
            f"Cese actividad RETA: BR {float(base_reguladora):.2f}€ × 70% = "
            f"{float(cuantia_bruta):.2f}€. Topes IPREM × 7/6 "
            f"({'con' if tiene_responsabilidades_familiares else 'sin'} cargas): "
            f"mín {float(tope_min):.2f}€ / máx {float(tope_max):.2f}€. "
            f"Cuantía final {float(cuantia_final):.2f}€/mes durante {duracion_meses} meses."
        ),
    }


# 15. Permiso Nacimiento y Cuidado del Menor 2026 (Art. 177-190 TRLGSS modificado)
# Trampa Q2 del vault: 19 semanas para 2026 (NO 16 del 2025). Aplicable también a RGSS.
# Fuente verificada: cambios_dm_2026.py (academia DM, FUENTE DE VERDAD).
def calcular_permiso_nacimiento_2026(
    progenitor: str = "biologico",        # 'biologico' | 'no_biologico' | 'adopcion'
    familia_monoparental: bool = False,
    parto_multiple_n_hijos: int = 1,      # 1 = parto simple, 2+ = múltiple
    discapacidad_menor: bool = False,     # ≥33% del menor
) -> Dict[str, Any]:
    """Permiso por nacimiento y cuidado de menor 2026 (RGSS y Funcionarios AGE).

    DISTRIBUCIÓN OFICIAL 2026 (cambios_dm_2026.py NACIMIENTO_2026):
      - **19 semanas** estándar para cada progenitor (madre y otro):
          • 6 semanas OBLIGATORIAS tras parto, jornada completa, ininterrumpidas
          • 11 semanas a jornada parcial o completa, hasta los 12 meses del menor
          • 2 semanas adicionales hasta que el menor cumpla 8 años
      - **32 semanas** familia monoparental (acumula los dos permisos):
          • 6 semanas obligatorias tras parto, jornada completa
          • 22 semanas hasta 12 meses
          • 4 semanas hasta 8 años
      - +1 semana adicional por cada hijo a partir del 2º en parto múltiple
      - +1 semana adicional por discapacidad ≥33% del menor

    NORMA: Art. 177-190 TRLGSS (modificados); Art. 49.a EBEP para funcionarios.
    Norma transposición: RDL 5/2023 + RDL 9/2025 (Directiva UE 2019/1158).

    TRAMPA Q2: confundir con las 16 semanas del 2025 (regla anterior).
    """
    if familia_monoparental:
        semanas_total = Decimal("32")
        desglose = {
            "obligatorias_tras_parto_jornada_completa": 6,
            "hasta_12m_jornada_parcial_o_completa": 22,
            "hasta_8_anios": 4,
        }
    else:
        semanas_total = Decimal("19")
        desglose = {
            "obligatorias_tras_parto_jornada_completa": 6,
            "hasta_12m_jornada_parcial_o_completa": 11,
            "hasta_8_anios": 2,
        }

    extras = []
    if parto_multiple_n_hijos > 1:
        extra = parto_multiple_n_hijos - 1
        semanas_total += Decimal(str(extra))
        extras.append(f"+{extra} semana(s) por parto múltiple ({parto_multiple_n_hijos} hijos)")
    if discapacidad_menor:
        semanas_total += Decimal("1")
        extras.append("+1 semana por discapacidad ≥33% del menor")

    return {
        "progenitor": progenitor,
        "tipo_familia": "monoparental" if familia_monoparental else "biparental",
        "semanas_total_2026": float(semanas_total),
        "distribucion": desglose,
        "ampliaciones_aplicadas": extras,
        "trampa_examen": "Usar 16 semanas (regla 2025) en lugar de 19 → FALSO desde 2026",
        "articulos": "Arts. 177-190 TRLGSS (modificado); Art. 49.a EBEP; RDL 5/2023 (BOE 29/06/2023); RDL 9/2025 (BOE 29/07/2025)",
        "explicacion": (
            f"Permiso nacimiento 2026 = {float(semanas_total)} semanas "
            f"({'monoparental' if familia_monoparental else 'biparental'}). "
            f"Distribución: {desglose}."
        ),
    }


# Alias mantenido para compatibilidad con código que llamaba a la función anterior:
def calcular_permiso_nacimiento_funcionarios_age(*args, **kwargs):
    """Alias deprecado — usa calcular_permiso_nacimiento_2026 (aplicable a RGSS y FP)."""
    return calcular_permiso_nacimiento_2026(*args, **kwargs)


# 16. Alias terminológico Ley 2/2025: Gran Invalidez → Gran Incapacidad
# La Ley 2/2025 (BOE 30/04/2025) cambia la terminología en TRLGSS y ET.
# Mantenemos compatibilidad: ambos términos refieren al mismo concepto.
GRADO_GRAN_INCAPACIDAD = "Gran Incapacidad"  # Terminología vigente Ley 2/2025
GRADO_GRAN_INVALIDEZ_LEGACY = "Gran Invalidez"  # Pre-Ley 2/2025 (mantener para outputs antiguos)


def normalizar_grado_incapacidad(grado_legacy: str) -> str:
    """Convierte terminología pre-Ley 2/2025 a la vigente.

    Mapeo:
      'Gran Invalidez' → 'Gran Incapacidad' (Ley 2/2025, BOE 30/04/2025)
      'Invalidez Permanente' → 'Incapacidad Permanente'
      Resto → sin cambios.
    """
    mapping = {
        "Gran Invalidez": GRADO_GRAN_INCAPACIDAD,
        "gran invalidez": GRADO_GRAN_INCAPACIDAD,
        "Invalidez Permanente": "Incapacidad Permanente",
        "invalidez permanente": "Incapacidad Permanente",
    }
    return mapping.get(grado_legacy, grado_legacy)


# 17. Pensión No Contributiva (PNC) — Cuantías 2026 (RDL 16/2025)
# Norma fuente: Real Decreto-ley 16/2025, de 23 de diciembre (BOE 24/12/2025).
def calcular_pnc_jubilacion_invalidez(
    tipo: str = "jubilacion",  # 'jubilacion' | 'invalidez'
    rentas_anuales_unidad_familiar: Decimal = Decimal("0"),
    miembros_unidad_familiar: int = 1,
    tiene_movilidad_reducida: bool = False,  # solo PNC invalidez
) -> Dict[str, Any]:
    """Calcula PNC de jubilación o invalidez (Arts. 363-372 TRLGSS).

    Cuantías 2026 (RDL 16/2025, BOE 24/12/2025):
      - PNC base íntegra mensual: 628,80 €/mes (8.803,20 €/año, 14 pagas).
      - Complemento movilidad reducida (PNC invalidez): 67,15 €/mes adicional.
      - Complemento alquiler vivienda: 525 €/año adicional (si vive de alquiler).

    Requisitos:
      - Edad ≥65 años (jubilación) o discapacidad ≥65% (invalidez).
      - 10 años residencia legal (5 si invalidez).
      - Carencia rentas: la suma rentas + cuantía PNC NO supere el límite
        de acumulación familiar (8.803,20 € individual, escala según miembros).
    """
    pnc_anual_individual = Decimal("8803.20")
    pnc_mensual_base = Decimal("628.80")

    # Límite acumulación familiar: PNC individual + 70% por cada miembro adicional
    limite_acumulacion = pnc_anual_individual * (
        Decimal("1") + Decimal("0.70") * Decimal(str(max(0, miembros_unidad_familiar - 1)))
    )

    # Si la suma de rentas supera el límite, la PNC se reduce o no se cobra
    rentas_totales = rentas_anuales_unidad_familiar + pnc_anual_individual
    if rentas_totales > limite_acumulacion:
        diferencia = rentas_totales - limite_acumulacion
        cuantia_anual_ajustada = max(pnc_anual_individual - diferencia, Decimal("0"))
        cuantia_mensual = (cuantia_anual_ajustada / Decimal("14")).quantize(Decimal("0.01"))
        return {
            "tipo": tipo,
            "cuantia_mensual": float(cuantia_mensual),
            "cuantia_anual": float(cuantia_anual_ajustada.quantize(Decimal("0.01"))),
            "ajuste_aplicado": float(diferencia.quantize(Decimal("0.01"))),
            "limite_acumulacion": float(limite_acumulacion.quantize(Decimal("0.01"))),
            "explicacion": (
                f"PNC ajustada: rentas + PNC ({float(rentas_totales):.2f}€) superan "
                f"el límite ({float(limite_acumulacion):.2f}€). Reducción {float(diferencia):.2f}€."
            ),
        }

    cuantia_final_mensual = pnc_mensual_base
    extras = []
    if tipo == "invalidez" and tiene_movilidad_reducida:
        cuantia_final_mensual += Decimal("67.15")
        extras.append("complemento movilidad reducida +67,15€")

    return {
        "tipo": tipo,
        "cuantia_mensual": float(cuantia_final_mensual.quantize(Decimal("0.01"))),
        "cuantia_anual_14_pagas": float((cuantia_final_mensual * Decimal("14")).quantize(Decimal("0.01"))),
        "complementos": extras,
        "limite_acumulacion_familiar": float(limite_acumulacion.quantize(Decimal("0.01"))),
        "miembros_unidad_familiar": miembros_unidad_familiar,
        "articulos": "Arts. 363-372 TRLGSS; cuantías 2026 fijadas por RDL 16/2025 (BOE 24/12/2025)",
        "explicacion": (
            f"PNC {tipo} 2026: {float(cuantia_final_mensual):.2f}€/mes "
            f"({float(cuantia_final_mensual * 14):.2f}€/año). RDL 16/2025."
        ),
    }


# 18. Subsidio No Contributivo de Nacimiento 2026 (DM26-T9-02)
# Antes 2025: solo mujeres. Ahora 2026: ambos sexos sin mínimo cotización.
# Norma: Art. 184 TRLGSS (modificado); cuantías 2026 RDL 16/2025.
def calcular_subsidio_nc_nacimiento_2026(
    sexo_solicitante: str = "mujer",       # 'mujer' | 'hombre' (NUEVO 2026: ambos)
    es_afiliado_alta_o_asimilada: bool = True,
    cumple_otros_requisitos_no_carencia: bool = True,
    iprem_2026_mensual: Decimal = Decimal("610.00"),
    semanas: int = 19,                     # según calcular_permiso_nacimiento_2026
    es_familia_monoparental: bool = False,
) -> Dict[str, Any]:
    """Subsidio No Contributivo por Nacimiento y Cuidado de Menor 2026.

    NOVEDAD 2026 (DM26-T9-02):
      - Antes 2025: solo trabajadoras MUJERES.
      - Desde 2026: trabajadoras Y trabajadores afiliados en alta/asimilada
        que cumplan TODOS los requisitos de la prestación contributiva
        SALVO el período mínimo de cotización (carencia).
      - Cubre nacimiento y adopción.
      - Cuantía = 100% del IPREM diario × días de duración.

    Trampa DM26-T9-02: decir que el subsidio NC nacimiento sigue siendo solo
    para mujeres → FALSO desde 2026.
    """
    if not es_afiliado_alta_o_asimilada:
        return {"acceso": False, "motivo": "Requisito incumplido: no afiliado en alta o asimilada al alta."}
    if not cumple_otros_requisitos_no_carencia:
        return {"acceso": False, "motivo": "Incumple otros requisitos (residencia legal, edad, etc.)."}

    if semanas < 1 or semanas > 32:
        return {"error": f"Duración fuera de rango (1-32 semanas). Recibido: {semanas}."}

    iprem_diario = iprem_2026_mensual / Decimal("30")
    dias_subsidio = semanas * 7
    if es_familia_monoparental and semanas == 19:
        # Si era una solicitud monoparental con 19 semanas, ajustar a 32
        dias_subsidio = 32 * 7
        semanas_efectivas = 32
    else:
        semanas_efectivas = semanas

    cuantia_total = (iprem_diario * Decimal(str(dias_subsidio))).quantize(Decimal("0.01"))

    return {
        "acceso": True,
        "sexo_solicitante": sexo_solicitante,
        "novedad_2026": "Acceso ampliado a hombres" if sexo_solicitante == "hombre" else "Acceso histórico mujeres + ampliación 2026 a hombres",
        "iprem_diario_2026": float(iprem_diario.quantize(Decimal("0.01"))),
        "semanas": semanas_efectivas,
        "dias_subsidio": dias_subsidio,
        "cuantia_total": float(cuantia_total),
        "cuantia_diaria": float(iprem_diario.quantize(Decimal("0.01"))),
        "trampa": "Decir que el subsidio NC nacimiento sigue siendo solo para mujeres → FALSO desde 2026",
        "articulos": "Art. 184 TRLGSS (modificado); cuantías 2026 RDL 16/2025 (BOE 24/12/2025)",
        "explicacion": (
            f"Subsidio NC nacimiento {sexo_solicitante}: {semanas_efectivas} semanas × 7 días × "
            f"{float(iprem_diario):.2f}€/día (IPREM diario 2026) = {float(cuantia_total):.2f}€ totales."
        ),
    }


# 19. Complemento Brecha de Género 2026 (DM26-T10-02)
# Cuantía 2025: 34,80€ → 2026: 36,90€/mes (subida 6%).
# Trampa: titular = progenitor con pensión MÁS BAJA (NO siempre la madre).
COMPLEMENTO_BRECHA_GENERO_MENSUAL_2026 = Decimal("36.90")
COMPLEMENTO_BRECHA_GENERO_ANUAL_2026 = Decimal("516.60")  # 36.90 × 14 pagas

def calcular_complemento_brecha_genero(
    pension_progenitor_a: Decimal,
    pension_progenitor_b: Decimal,
    n_hijos: int = 1,
    es_progenitor_a_la_madre: bool = True,
) -> Dict[str, Any]:
    """Complemento de pensiones contributivas para reducir la brecha de género.

    Cuantía 2026: **36,90€/mes × 14 pagas = 516,60€/año**, por hijo, hasta 4 hijos máx.

    REGLAS (Art. 60 TRLGSS):
      1. Se reconoce al PROGENITOR CON LA PENSIÓN MÁS BAJA, sea hombre o mujer.
         (Tras STJUE C-450/18 que extendió a hombres lo que antes era solo madres.)
      2. Si ambos progenitores tienen pensión, se da al de menor cuantía.
      3. Aplicable a pensiones contributivas de jubilación, IP o viudedad.
      4. Naturaleza CONTRIBUTIVA a todos los efectos (Art. 60.4 TRLGSS).
      5. Tope: 4 hijos máximo (4 × 36.90€ = 147,60€/mes).

    Trampa DM26-T10-02:
      - Decir que el complemento es siempre para la madre → FALSO.
      - Usar la cuantía 2025 (34,80€) en lugar de 36,90€ → FALSO.
    """
    if n_hijos < 1:
        return {"acceso": False, "motivo": "Requisito incumplido: debe haber ≥1 hijo."}

    n_hijos_efectivos = min(n_hijos, 4)  # tope 4 hijos

    # Determinar el titular = el de menor pensión
    if pension_progenitor_a < pension_progenitor_b:
        titular = "progenitor A"
        es_madre_titular = es_progenitor_a_la_madre
    elif pension_progenitor_b < pension_progenitor_a:
        titular = "progenitor B"
        es_madre_titular = not es_progenitor_a_la_madre
    else:
        # Empate → la madre (regla supletoria)
        titular = "progenitor A" if es_progenitor_a_la_madre else "progenitor B"
        es_madre_titular = True

    cuantia_mensual = COMPLEMENTO_BRECHA_GENERO_MENSUAL_2026 * Decimal(str(n_hijos_efectivos))
    cuantia_anual = COMPLEMENTO_BRECHA_GENERO_ANUAL_2026 * Decimal(str(n_hijos_efectivos))

    return {
        "titular": titular,
        "es_la_madre": es_madre_titular,
        "n_hijos_efectivos": n_hijos_efectivos,
        "n_hijos_solicitados": n_hijos,
        "cuantia_por_hijo_mensual": float(COMPLEMENTO_BRECHA_GENERO_MENSUAL_2026),
        "cuantia_total_mensual": float(cuantia_mensual),
        "cuantia_total_anual_14_pagas": float(cuantia_anual),
        "naturaleza": "contributiva",
        "trampa_examen": [
            "Decir que el complemento es siempre para la madre → FALSO (es para quien tenga la pensión más baja).",
            "Usar 34,80€ (cuantía 2025) en lugar de 36,90€ (cuantía 2026) → FALSO.",
        ],
        "articulos": "Art. 60 TRLGSS; cuantía 2026 RDL 16/2025 (BOE 24/12/2025)",
        "explicacion": (
            f"Complemento brecha género 2026: titular = {titular} "
            f"({'madre' if es_madre_titular else 'padre'}), "
            f"{n_hijos_efectivos} hijo(s) × 36,90€/mes = {float(cuantia_mensual):.2f}€/mes "
            f"({float(cuantia_anual):.2f}€/año en 14 pagas)."
        ),
    }


# ============================================================================
# FIN BLOQUE CALCULADORAS — calculos_ss_extended.py
# Última actualización: 29/04/2026
#   - 4 fixes textuales (constantes:70 jubilación + referencias normativas)
#   - 5 GAPs implementados (cese RETA, permiso 19s, lagunas Art. 322, Gran Inc, PNC)
#   - BUGs #4-#8 detectados al cruzar con cambios_dm_2026.py:
#     #4 Adicional Solidaridad (constantes corregidas: 1.15/1.25/1.46%)
#     #5 BR DUAL ya estaba en calculos_ss.py (verificado funcionando)
#     #6 Distribución 19 semanas corregida (6+11+2 / monoparental 32)
#     #7 Subsidio NC nacimiento ambos sexos (función nueva)
#     #8 Complemento brecha género 36,90€ 2026 (constante + función nuevas)
# ============================================================================
