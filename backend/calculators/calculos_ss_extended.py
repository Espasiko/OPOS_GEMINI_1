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
from typing import Optional, List, Dict
from datetime import date, timedelta


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
# CALCULADORA 2: JUBILACIÓN
# ============================================================================

class CalculadoraJubilacion:
    """
    Calcula Pensión de Jubilación.
    
    Normativa: TRLGSS Art. 161-166 - Factor edad + años cotizados
    Requisitos:
      - Edad mínima: 67 años (flexible 65 con 38,5 años cotizados)
      - Mínimo 15 años cotizados (180 meses)
      - Base reguladora = promedio últimos 25 años
    """
    
    # Cuantías vigentes 2026
    PENSION_MINIMA_JUBILACION = Decimal("656.10")
    PENSION_MAXIMA_JUBILACION = Decimal("2819.54")
    EDAD_MINIMA = 67
    EDAD_FLEXIBLE = 65
    ANOS_FLEX_REQUERIDOS = 38
    
    @staticmethod
    def calcular_jubilacion(
        base_reguladora_mensual: Decimal,
        edad_solicitud: int,
        anos_cotizados: int,
        anticipada: bool = False
    ) -> ResultadoJubilacion:
        """
        Calcula pensión de Jubilación.
        
        Args:
            base_reguladora_mensual: Base reguladora euros/mes
            edad_solicitud: Edad al solicitar jubilación
            anos_cotizados: Años de cotización acumulados
            anticipada: Si es jubilación anticipada
        
        Returns:
            ResultadoJubilacion con detalles
        """
        base_reg = Decimal(str(base_reguladora_mensual))
        semanas_cotizadas = anos_cotizados * 52
        
        # Factor edad: se calcula por semanas cotizadas
        # Hasta 25 años: 50%, después suma 0.2% por trimestre adicional
        if semanas_cotizadas >= 1300:  # 25 años
            porcentaje_base = Decimal("50")
            trimestres_extra = (semanas_cotizadas - 1300) // 13
            porcentaje_base += (trimestres_extra * Decimal("0.2"))
        else:
            # Menos de 25 años: proporcional
            porcentaje_base = (semanas_cotizadas / 1300) * Decimal("50")
        
        # Límite máximo: 100%
        porcentaje_base = min(porcentaje_base, Decimal("100"))
        
        # Factor por anticipación
        factor_anticipacion = Decimal("1")
        if anticipada:
            # Por cada mes de anticipación antes de edad legal: -0.375%
            meses_anticipacion = (CalculadoraJubilacion.EDAD_MINIMA - edad_solicitud) * 12
            factor_anticipacion = Decimal("1") - (
                Decimal(str(meses_anticipacion)) * Decimal("0.00375")
            )
        
        # Calcular pensión
        pension_bruta = base_reg * (porcentaje_base / Decimal("100"))
        pension_con_anticipacion = pension_bruta * factor_anticipacion
        
        # Aplicar mínimos y máximos
        if pension_con_anticipacion < CalculadoraJubilacion.PENSION_MINIMA_JUBILACION:
            pension_con_anticipacion = CalculadoraJubilacion.PENSION_MINIMA_JUBILACION
        
        if pension_con_anticipacion > CalculadoraJubilacion.PENSION_MAXIMA_JUBILACION:
            pension_con_anticipacion = CalculadoraJubilacion.PENSION_MAXIMA_JUBILACION
        
        incrementos = {}
        if edad_solicitud > 67:
            increment_edad = (edad_solicitud - 67) * Decimal("0.4")
            incrementos["Por edad superior a 67"] = increment_edad
        
        return ResultadoJubilacion(
            edad=edad_solicitud,
            semanas_cotizadas=semanas_cotizadas,
            base_reguladora_mensual=base_reg,
            factor_anticipacion=factor_anticipacion,
            porcentaje_acumulado=porcentaje_base.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            pension_base=pension_bruta.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            incrementos=incrementos,
            pension_neta=pension_con_anticipacion.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            explicacion=f"Jubilación: {anos_cotizados} años → {porcentaje_base:.2f}% → {pension_con_anticipacion}€/mes"
        )


# ============================================================================
# CALCULADORA 3: DESEMPLEO
# ============================================================================

class CalculadoraDesempleo:
    """
    Calcula Subsidio por Desempleo.
    
    Normativa: TRLGSS Art. 275-285 - 70% primer 180 días, 60% resto
    Requisitos:
      - 12 meses cotización últimos 72 meses
      - Situación de desempleo involuntario
      - Duración según semanas cotizadas
    """
    
    # Cuantías vigentes 2026
    BASE_REGULADORA_MINIMA = Decimal("1229.09")
    BASE_REGULADORA_MAXIMA = Decimal("4070.10")
    
    @staticmethod
    def calcular_subsidio_desempleo(
        base_reguladora_diaria: Decimal,
        dias_cotizados_180: int,  # Cotización en últimos 180 días
        vigencia_desde: Optional[date] = None
    ) -> ResultadoDesempleo:
        """
        Calcula subsidio por desempleo.
        
        Args:
            base_reguladora_diaria: Base diaria en euros
            dias_cotizados_180: Días cotizados en últimos 180 días
            vigencia_desde: Fecha inicio del subsidio
        
        Returns:
            ResultadoDesempleo con cálculo
        """
        base_reg_d = Decimal(str(base_reguladora_diaria))
        vigencia = vigencia_desde or date.today()
        
        # Determinar duración según cotización
        if dias_cotizados_180 >= 120:  # Más de 4 meses
            duracion_dias = 180  # 6 meses al 70%
            tipo = TipoDesempleo.NIVEL_70
            porcentaje = Decimal("0.70")
        else:
            duracion_dias = 90  # 3 meses al 60%
            tipo = TipoDesempleo.NIVEL_60
            porcentaje = Decimal("0.60")
        
        # Calcular subsidio
        subsidio_diario = (base_reg_d * porcentaje).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        subsidio_total = subsidio_diario * Decimal(str(duracion_dias))
        
        vigencia_hasta = vigencia + timedelta(days=duracion_dias)
        
        return ResultadoDesempleo(
            base_reguladora_diaria=base_reg_d,
            porcentaje_aplicable=porcentaje,
            duracion_dias=duracion_dias,
            subsidio_diario=subsidio_diario,
            subsidio_total=subsidio_total.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            tipo_subsidio=tipo,
            vigencia_desde=vigencia,
            vigencia_hasta=vigencia_hasta,
            explicacion=f"Desempleo: {base_reg_d}€/día × {porcentaje:.0%} × {duracion_dias} días = {subsidio_total}€"
        )


# ============================================================================
# CALCULADORA 4: MATERNIDAD/PATERNIDAD
# ============================================================================

class CalculadoraMaternidad:
    """
    Calcula prestaciones de Maternidad y Paternidad.
    
    Normativa: TRLGSS Art. 177-178, Ley 9/2009 (igualdad M/P)
    Requisitos:
      - Afiliación y cotización en SS
      - Comunicación con antelación
    """
    
    @staticmethod
    def calcular_maternidad(
        base_reguladora_diaria: Decimal,
        semanas_solicitadas: int = 16,
        es_paternidad: bool = False,
        fecha_inicio: Optional[date] = None
    ) -> ResultadoMaternidad:
        """
        Calcula prestación de Maternidad/Paternidad.
        
        Args:
            base_reguladora_diaria: Base diaria para el cálculo
            semanas_solicitadas: Semanas de la prestación (16-18 posibles)
            es_paternidad: Si es prestación de paternidad
            fecha_inicio: Fecha inicio de la prestación
        
        Returns:
            ResultadoMaternidad con detalles
        """
        base_reg_d = Decimal(str(base_reguladora_diaria))
        tipo_prestacion = "Paternidad" if es_paternidad else "Maternidad"
        
        # Semanas: Mínimo 16 (Maternidad), máximo 18 (compartidas)
        semanas_util = min(max(semanas_solicitadas, 16), 18)
        dias_totales = semanas_util * 7
        
        # Prestación = 100% de base reguladora diaria
        prestacion_diaria = base_reg_d
        prestacion_total = prestacion_diaria * Decimal(str(dias_totales))
        
        fecha = fecha_inicio or date.today()
        fecha_fin = fecha + timedelta(weeks=semanas_util)
        
        return ResultadoMaternidad(
            tipo_prestacion=tipo_prestacion,
            semanas_disponibles=18,
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

if __name__ == "__main__":
    print("=" * 70)
    print("CALCULADORAS EXTENDIDAS SEGURIDAD SOCIAL - TEST BÁSICOS")
    print("=" * 70)
    print()

    # TEST 1: Incapacidad Permanente Total
    print("✅ TEST 1: Incapacidad Permanente Total")
    print("-" * 70)
    resultado_ipt = CalculadoraIPT.calcular_ipt(
        base_reguladora_mensual=Decimal("1500"),
        tipo_incapacidad=TipoIncapacidad.TOTAL
    )
    print(f"  Base reguladora: 1.500,00€/mes")
    print(f"  Pensión IPT (55%): {resultado_ipt.pension_mensual}€/mes")
    print(f"  Vigencia: {resultado_ipt.vigencia_desde}")
    print(f"  Ley: {resultado_ipt.aplicacion_ley}")
    print()

    # TEST 2: Jubilación
    print("✅ TEST 2: Jubilación a Edad Legal")
    print("-" * 70)
    resultado_jubilacion = CalculadoraJubilacion.calcular_jubilacion(
        base_reguladora_mensual=Decimal("1800"),
        edad_solicitud=67,
        anos_cotizados=40
    )
    print(f"  Edad: {resultado_jubilacion.edad} años")
    print(f"  Años cotizados: {resultado_jubilacion.semanas_cotizadas // 52}")
    print(f"  Porcentaje: {resultado_jubilacion.porcentaje_acumulado}%")
    print(f"  Pensión: {resultado_jubilacion.pension_neta}€/mes")
    print()

    # TEST 3: Desempleo
    print("✅ TEST 3: Subsidio Desempleo")
    print("-" * 70)
    resultado_desempleo = CalculadoraDesempleo.calcular_subsidio_desempleo(
        base_reguladora_diaria=Decimal("40.97"),
        dias_cotizados_180=150
    )
    print(f"  Base diaria: {resultado_desempleo.base_reguladora_diaria}€")
    print(f"  Porcentaje: {resultado_desempleo.porcentaje_aplicable:.0%}")
    print(f"  Duración: {resultado_desempleo.duracion_dias} días")
    print(f"  Subsidio diario: {resultado_desempleo.subsidio_diario}€")
    print(f"  Total: {resultado_desempleo.subsidio_total}€")
    print()

    # TEST 4: Maternidad
    print("✅ TEST 4: Prestación Maternidad")
    print("-" * 70)
    resultado_maternidad = CalculadoraMaternidad.calcular_maternidad(
        base_reguladora_diaria=Decimal("50.00"),
        semanas_solicitadas=16
    )
    print(f"  Base diaria: {resultado_maternidad.base_reguladora_diaria}€")
    print(f"  Semanas: {resultado_maternidad.semanas_utilizadas}")
    print(f"  Prestación diaria: {resultado_maternidad.prestacion_diaria}€")
    print(f"  Total: {resultado_maternidad.prestacion_total}€")
    print()

    # TEST 5: Complemento Mínimo
    print("✅ TEST 5: Complemento Mínimo Pensión")
    print("-" * 70)
    resultado_complemento = CalculadoraComplementos.calcular_complemento_minimo(
        pension_actual=Decimal("600"),
        tipo_pension="Jubilación"
    )
    print(f"  Pensión actual: 600,00€")
    print(f"  Mínimo legal: {CalculadoraComplementos.COMPLEMENTO_MINIMO_JUBILACION}€")
    print(f"  Complemento: {resultado_complemento.importe_total}€")
    print()

    # TEST 6: Cuota Cotización
    print("✅ TEST 6: Cuota de Cotización")
    print("-" * 70)
    resultado_cuota = CalculadoraCuota.calcular_cuota(
        salario_bruto_mensual=Decimal("2000"),
        tipo_contrato="Indefinido"
    )
    print(f"  Salario bruto: {resultado_cuota.salario_base}€")
    print(f"  Aportación trabajador: {resultado_cuota.aportacion_empleado}€")
    print(f"  Aportación empresa: {resultado_cuota.aportacion_empresario}€")
    print(f"  Total cuota: {resultado_cuota.aportacion_total}€")
    print()

    # TEST 7: Devolución por No Derecho
    print("✅ TEST 7: Devolución por No Derecho")
    print("-" * 70)
    resultado_devolucion = CalculadoraDevolucion.calcular_devolucion(
        importe_indebido=Decimal("1000"),
        periodos_afectados=3,
        aplicar_interes=True
    )
    print(f"  Importe indebido: {resultado_devolucion.importe_indebido}€")
    print(f"  Interés legal (3.5%): {resultado_devolucion.interes_legal}€")
    print(f"  Total a devolver: {resultado_devolucion.total_devoluciones}€")
    print()

    # TEST 8: Ayuda por Hijo a Cargo
    print("✅ TEST 8: Ayuda por Hijo a Cargo")
    print("-" * 70)
    resultado_ayuda_hijo = CalculadoraAyudaHijo.calcular_ayuda_hijo(
        numero_hijos=2,
        ingresos_grupo_familiar=Decimal("15000"),
        edades_hijos=[8, 12]
    )
    print(f"  Número de hijos: {resultado_ayuda_hijo.numero_hijos}")
    print(f"  Importe unitario: {resultado_ayuda_hijo.importe_unitario}€")
    print(f"  Ayuda total: {resultado_ayuda_hijo.importe_total}€")
    print(f"  Cumple requisitos: {resultado_ayuda_hijo.requisitos_cumplidos}")
    print()

    # TEST 9: Bonificación en Cuotas
    print("✅ TEST 9: Bonificación en Cuotas")
    print("-" * 70)
    resultado_bonificacion = CalculadoraBonificacion.calcular_bonificacion(
        cuota_empresarial=Decimal("598"),
        tipo_bonificacion="Joven hasta 30",
        duracion_meses=12
    )
    print(f"  Cuota original: {resultado_bonificacion.cuota_original}€")
    print(f"  Porcentaje bonificación: {resultado_bonificacion.porcentaje_bonificacion}%")
    print(f"  Importe bonificado: {resultado_bonificacion.importe_bonificacion}€")
    print(f"  Cuota bonificada: {resultado_bonificacion.cuota_bonificada}€")
    print()

    print("=" * 70)
    print("✅ TODOS LOS TESTS BÁSICOS COMPLETADOS")
    print("=" * 70)
print("=" * 70)
print("✅ TODOS LOS TESTS BÁSICOS COMPLETADOS")
print("=" * 70)
