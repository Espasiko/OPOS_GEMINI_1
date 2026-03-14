"""
Calculadora de Seguridad Social - Precisión 100%
Basado en normativa vigente 2024-2025
"""
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from typing import Literal, List, Optional


@dataclass
class ResultadoIT:
    """Resultado del cálculo de subsidio IT"""
    base_diaria: Decimal
    porcentaje: Decimal
    subsidio_diario: Decimal
    contingencia: str
    dia_baja: int
    pagador: str  # "Empresa", "INSS", "Mutua"
    articulo_aplicable: str
    explicacion: str


class CalculadoraSS:
    """
    Calculadora de Seguridad Social
    Usa Decimal para precisión exacta
    """
    
    # Configuración 2024-2026
    DIAS_MES_OBSOLETO = 30
    
    # Porcentajes IT según Art. 173.1 TRLGSS
    PORCENTAJES_IT = {
        "EC": {  # Enfermedad Común
            "dias_1_3": Decimal("0.00"),    # No se cobra subsidio (Art. 173.1)
            "dias_4_20": Decimal("0.60"),   # 60%
            "dias_21_plus": Decimal("0.75") # 75%
        },
        "AT": {  # Accidente de Trabajo (SIN pago empresarial 4-15)
            "dia_1": Decimal("0.00"),       # El día del accidente lo paga la empresa íntegro como salario (Art. 173.2)
            "dia_2_plus": Decimal("0.75")   # 75% subsidio desde día 2 a cargo de Mutua/INSS
        },
        "EP": {  # Enfermedad Profesional
            "dia_1": Decimal("0.00"),       # El día de la baja lo paga la empresa íntegro como salario (Art. 173.3)
            "dia_2_plus": Decimal("0.75")   # 75% subsidio desde día 2 a cargo de Mutua/INSS
        }
    }

    @staticmethod
    def calcular_base_reguladora_it_2026(
        bases_3_meses: List[float],
        dias_periodo: int = 91 # 3 meses naturales promedio
    ) -> Decimal:
        """
        Calcula la Base Reguladora según RDL 11/2024 (Vigente desde abril 2025).
        Fórmula: Suma de bases de cotización de los 3 meses anteriores / días naturales del período.
        """
        suma_bases = sum([Decimal(str(b)) for b in bases_3_meses])
        if dias_periodo <= 0:
            dias_periodo = 91
        return (suma_bases / Decimal(str(dias_periodo))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    @staticmethod
    def calcular_subsidio_it(
        base_cotizacion: float, # Se mantiene para compatibilidad v1, pero se prefiere bases_3_meses
        contingencia: Literal["EC", "AT", "EP"],
        dia_baja: int,
        bases_3_meses: Optional[List[float]] = None,
        dias_periodo: int = 90
    ) -> ResultadoIT:
        """
        Calcula subsidio diario de Incapacidad Temporal.
        Aplica RDL 11/2024 para la Base Reguladora si se proveen las 3 bases.
        """
        # 1. Calcular base diaria (RDL 11/2024 vs Art. 174.2 TRLGSS antiguo)
        if bases_3_meses and len(bases_3_meses) >= 3:
            base_diaria = CalculadoraSS.calcular_base_reguladora_it_2026(bases_3_meses, dias_periodo)
            regla_usada = "RDL 11/2024 (Suma 3 meses / días naturales)"
        else:
            base_mensual = Decimal(str(base_cotizacion))
            base_diaria = (base_mensual / Decimal("30")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            regla_usada = "Art. 174.2 TRLGSS (Mes anterior / 30) - OBSOLETO PARA 2026"
        
        # 2. Determinar porcentaje y pagador según contingencia y día
        if contingencia == "EC":
            if dia_baja <= 3:
                porcentaje = CalculadoraSS.PORCENTAJES_IT["EC"]["dias_1_3"]
                pagador = "Ninguno (Días 1-3 son carencia)"
                periodo = "días 1-3"
            elif dia_baja <= 15:
                porcentaje = CalculadoraSS.PORCENTAJES_IT["EC"]["dias_4_20"]
                pagador = "Empresa (pago delegado del 4 al 15)"
                periodo = "días 4-15"
            elif dia_baja <= 20:
                porcentaje = CalculadoraSS.PORCENTAJES_IT["EC"]["dias_4_20"]
                pagador = "INSS/Mutua"
                periodo = "días 16-20"
            else:
                porcentaje = CalculadoraSS.PORCENTAJES_IT["EC"]["dias_21_plus"]
                pagador = "INSS/Mutua"
                periodo = "día 21+"
        elif contingencia in ["AT", "EP"]:
            if dia_baja == 1:
                porcentaje = CalculadoraSS.PORCENTAJES_IT[contingencia]["dia_1"]
                pagador = "Empresa (paga salario íntegro día del accidente)"
                periodo = "día 1"
            else:
                porcentaje = CalculadoraSS.PORCENTAJES_IT[contingencia]["dia_2_plus"]
                # CORRECCIÓN V12: En AT/EP NO hay periodo empresarial 4-15
                pagador = "INSS/Mutua (Desde el día siguiente al accidente)"
                periodo = f"día {dia_baja}"
        else:
            raise ValueError(f"Contingencia inválida: {contingencia}")
        
        # Calcular subsidio diario
        subsidio_diario = (base_diaria * porcentaje).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        # Explicación técnica para el agente
        explicacion = (
            f"Regla BR: {regla_usada}. Base diaria calculada: {base_diaria}€. "
            f"Contingencia {contingencia}, {periodo}: {porcentaje * 100}%. "
            f"Pagador: {pagador}. "
            f"Subsidio: {base_diaria}€ × {porcentaje} = {subsidio_diario}€/día."
        )
        
        return ResultadoIT(
            base_diaria=base_diaria,
            porcentaje=porcentaje,
            subsidio_diario=subsidio_diario,
            contingencia=contingencia,
            dia_baja=dia_baja,
            pagador=pagador,
            articulo_aplicable="Art. 173 y 174 TRLGSS / RDL 11/2024",
            explicacion=explicacion
        )

# Función helper para uso directo
def calcular_subsidio_it(base: float, contingencia: str, dia: int, bases_3_meses: Optional[List[float]] = None) -> dict:
    """Wrapper para uso fácil desde herramientas."""
    resultado = CalculadoraSS.calcular_subsidio_it(base, contingencia, dia, bases_3_meses)
    
    return {
        "base_diaria": float(resultado.base_diaria),
        "porcentaje": float(resultado.porcentaje),
        "subsidio_diario": float(resultado.subsidio_diario),
        "contingencia": resultado.contingencia,
        "dia_baja": resultado.dia_baja,
        "pagador": resultado.pagador,
        "articulo_aplicable": resultado.articulo_aplicable,
        "explicacion": resultado.explicacion,
        "regla_br": "RDL 11/2024" if bases_3_meses else "Obsoleta"
    }
