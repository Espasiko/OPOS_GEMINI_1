"""
Calculadora de Seguridad Social - Precisión 100%
Basado en normativa vigente 2024-2025
"""
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from typing import Literal


@dataclass
class ResultadoIT:
    """Resultado del cálculo de subsidio IT"""
    base_diaria: Decimal
    porcentaje: Decimal
    subsidio_diario: Decimal
    contingencia: str
    dia_baja: int
    articulo_aplicable: str
    explicacion: str


class CalculadoraSS:
    """
    Calculadora de Seguridad Social
    Usa Decimal para precisión exacta
    """
    
    # Configuración 2024
    DIAS_MES = 30
    
    # Porcentajes IT según Art. 173.1 TRLGSS
    PORCENTAJES_IT = {
        "EC": {  # Enfermedad Común
            "dias_1_3": Decimal("0.00"),    # No se cobra
            "dias_4_20": Decimal("0.60"),   # 60%
            "dias_21_plus": Decimal("0.75") # 75%
        },
        "AT": {  # Accidente de Trabajo
            "dia_1": Decimal("0.00"),       # No se cobra
            "dia_2_plus": Decimal("0.75")   # 75%
        },
        "EP": {  # Enfermedad Profesional
            "dia_1": Decimal("0.00"),       # No se cobra
            "dia_2_plus": Decimal("0.75")   # 75%
        }
    }
    
    @staticmethod
    def calcular_subsidio_it(
        base_cotizacion: float,
        contingencia: Literal["EC", "AT", "EP"],
        dia_baja: int
    ) -> ResultadoIT:
        """
        Calcula subsidio diario de Incapacidad Temporal
        
        Args:
            base_cotizacion: Base de cotización mensual en euros
            contingencia: Tipo (EC/AT/EP)
            dia_baja: Día de baja (1-545)
        
        Returns:
            ResultadoIT con cálculo detallado
        """
        # Convertir a Decimal para precisión
        base_mensual = Decimal(str(base_cotizacion))
        
        # Calcular base diaria (Art. 174.2 TRLGSS)
        base_diaria = (base_mensual / Decimal(str(CalculadoraSS.DIAS_MES))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        # Determinar porcentaje según contingencia y día
        if contingencia == "EC":
            if dia_baja <= 3:
                porcentaje = CalculadoraSS.PORCENTAJES_IT["EC"]["dias_1_3"]
                periodo = "días 1-3"
            elif dia_baja <= 20:
                porcentaje = CalculadoraSS.PORCENTAJES_IT["EC"]["dias_4_20"]
                periodo = "días 4-20"
            else:
                porcentaje = CalculadoraSS.PORCENTAJES_IT["EC"]["dias_21_plus"]
                periodo = "día 21+"
        elif contingencia in ["AT", "EP"]:
            if dia_baja == 1:
                porcentaje = CalculadoraSS.PORCENTAJES_IT[contingencia]["dia_1"]
                periodo = "día 1"
            else:
                porcentaje = CalculadoraSS.PORCENTAJES_IT[contingencia]["dia_2_plus"]
                periodo = "día 2+"
        else:
            raise ValueError(f"Contingencia inválida: {contingencia}")
        
        # Calcular subsidio diario
        subsidio_diario = (base_diaria * porcentaje).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        # Artículo aplicable
        articulo = "Art. 173.1 TRLGSS"
        
        # Explicación
        explicacion = (
            f"Base diaria: {base_mensual}€ / {CalculadoraSS.DIAS_MES} días = {base_diaria}€. "
            f"Contingencia {contingencia}, {periodo}: {porcentaje * 100}%. "
            f"Subsidio: {base_diaria}€ × {porcentaje} = {subsidio_diario}€/día."
        )
        
        return ResultadoIT(
            base_diaria=base_diaria,
            porcentaje=porcentaje,
            subsidio_diario=subsidio_diario,
            contingencia=contingencia,
            dia_baja=dia_baja,
            articulo_aplicable=articulo,
            explicacion=explicacion
        )


# Función helper para uso directo
def calcular_subsidio_it(base: float, contingencia: str, dia: int) -> dict:
    """
    Wrapper para uso fácil
    Retorna dict en vez de dataclass
    """
    resultado = CalculadoraSS.calcular_subsidio_it(base, contingencia, dia)
    
    return {
        "base_diaria": float(resultado.base_diaria),
        "porcentaje": float(resultado.porcentaje),
        "subsidio_diario": float(resultado.subsidio_diario),
        "contingencia": resultado.contingencia,
        "dia_baja": resultado.dia_baja,
        "articulo_aplicable": resultado.articulo_aplicable,
        "explicacion": resultado.explicacion
    }
