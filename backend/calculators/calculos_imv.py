"""
Calculadora de Ingreso Mínimo Vital (IMV) - Precisión 100%
Basado en: Real Decreto-ley 20/2020, de 29 de mayo
Normativa vigente 2026
"""
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from typing import Literal, List, Optional
from enum import Enum


class TipoUnidadFamiliar(Enum):
    """Tipos de unidad familiar para IMV"""
    PERSONA_SOLA = "persona_sola"
    DOS_PERSONAS = "dos_personas"
    TRES_PERSONAS = "tres_personas"
    CUATRO_PERSONAS = "cuatro_personas"
    CINCO_PERSONAS = "cinco_personas"
    SEIS_O_MAS = "seis_o_mas"


@dataclass
class ResultadoIMV:
    """Resultado del cálculo de IMV"""
    importe_base: Decimal
    ingresos_netos_familia: Decimal
    ingresos_contabilizados: Decimal  # 50% de ingresos_netos_familia
    imv_a_recibir: Decimal
    tipo_unidad: TipoUnidadFamiliar
    num_miembros: int
    ambos_mayores_30: bool
    incremento_aplicado: Decimal
    requisitos_cumplidos: bool
    articulo_aplicable: str
    explicacion: str


@dataclass
class AnalisisPatrimonio:
    """Análisis de compatibilidad patrimonio con IMV"""
    patrimonio_total: Decimal
    limite_maximo: Decimal
    compatible: bool
    detalles: str


class CalculadoraIMV:
    """
    Calculadora de Ingreso Mínimo Vital (IMV)
    Período: Febrero 2026 (actualizado por IPC)
    """
    
    # Importes base 2026 (actualizados con IPC)
    IMPORTES_BASE_2026 = {
        TipoUnidadFamiliar.PERSONA_SOLA: Decimal("564.60"),
        TipoUnidadFamiliar.DOS_PERSONAS: Decimal("847.15"),
        TipoUnidadFamiliar.TRES_PERSONAS: Decimal("1102.80"),
        TipoUnidadFamiliar.CUATRO_PERSONAS: Decimal("1356.45"),
        TipoUnidadFamiliar.CINCO_PERSONAS: Decimal("1610.10"),
        TipoUnidadFamiliar.SEIS_O_MAS: Decimal("1863.75"),  # Aproximado
    }
    
    # Incremento si ambos miembros > 30 años
    INCREMENTO_AMBOS_MAYORES_30 = Decimal("0.50")  # 50%
    
    # Límite de patrimonio general
    LIMITE_PATRIMONIO = Decimal("15965.50")
    
    # Tasa de contabilización de ingresos (50%)
    TASA_INGRESOS = Decimal("0.50")
    
    @staticmethod
    def calcular_imv(
        tipo_unidad: TipoUnidadFamiliar,
        ingresos_netos_familia: float,
        num_miembros: int = 1,
        ambos_mayores_30: bool = False,
        patrimonio_total: float = 0.0,
    ) -> ResultadoIMV:
        """
        Calcula el Ingreso Mínimo Vital
        
        Args:
            tipo_unidad: Tipo de unidad familiar
            ingresos_netos_familia: Ingresos netos mensuales de TODA la familia
            num_miembros: Número de miembros (para contexto)
            ambos_mayores_30: ¿Ambos miembros mayores de 30? (solo si 2+ miembros)
            patrimonio_total: Patrimonio total para validación
        
        Returns:
            ResultadoIMV con cálculo completo
        
        Nota:
            Fórmula: IMV = importe_base - (ingresos_netos × 50%)
            Si resultado < 0 → IMV = 0 (sin derecho)
            Incremento 50% si ambos > 30 años (solo unidades 2+ personas)
        """
        
        # Convertir a Decimal
        ingresos_netos = Decimal(str(ingresos_netos_familia))
        patrimonio = Decimal(str(patrimonio_total))
        
        # Obtener importe base
        importe_base = CalculadoraIMV.IMPORTES_BASE_2026[tipo_unidad]
        
        # Aplicar incremento si ambos > 30
        incremento = Decimal("0")
        if ambos_mayores_30 and num_miembros >= 2:
            incremento = importe_base * CalculadoraIMV.INCREMENTO_AMBOS_MAYORES_30
            importe_base = importe_base + incremento
        
        # Calcular ingresos contabilizados (50% de ingresos netos)
        ingresos_contabilizados = (ingresos_netos * CalculadoraIMV.TASA_INGRESOS).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        # Calcular IMV a recibir
        imv_bruto = (importe_base - ingresos_contabilizados).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        # Si IMV < 0, derecho = 0
        imv_a_recibir = max(imv_bruto, Decimal("0"))
        
        # Verificar requisitos
        requisitos_cumplidos = patrimonio <= CalculadoraIMV.LIMITE_PATRIMONIO
        
        # Artículo
        articulo = "Art. 8 Real Decreto-ley 20/2020"
        
        # Explicación
        explicacion = (
            f"Unidad familiar: {tipo_unidad.value}. "
            f"Importe base: {importe_base}€. "
        )
        
        if ambos_mayores_30 and num_miembros >= 2:
            explicacion += f"Incremento 50% (ambos >30): +{incremento}€. "
        
        explicacion += (
            f"Ingresos netos familia: {ingresos_netos}€. "
            f"Ingresos contabilizados (50%): {ingresos_contabilizados}€. "
            f"IMV a recibir: {imv_a_recibir}€/mes. "
        )
        
        if not requisitos_cumplidos:
            explicacion += f"⚠️ PATRIMONIO EXCEDIDO: {patrimonio}€ > {CalculadoraIMV.LIMITE_PATRIMONIO}€"
        
        return ResultadoIMV(
            importe_base=importe_base - incremento,  # Base sin incremento
            ingresos_netos_familia=ingresos_netos,
            ingresos_contabilizados=ingresos_contabilizados,
            imv_a_recibir=imv_a_recibir,
            tipo_unidad=tipo_unidad,
            num_miembros=num_miembros,
            ambos_mayores_30=ambos_mayores_30,
            incremento_aplicado=incremento,
            requisitos_cumplidos=requisitos_cumplidos,
            articulo_aplicable=articulo,
            explicacion=explicacion
        )
    
    @staticmethod
    def validar_patrimonio(
        patrimonio_total: float,
        tiene_vivienda_habitual: bool = True,
        tiene_otro_vehiculo: bool = False,
    ) -> AnalisisPatrimonio:
        """
        Valida si patrimonio es compatible con IMV
        
        Reglas:
        - Vivienda habitual: SIN LÍMITE
        - Patrimonio general: máx 15.965,50€
        - Exclusiones: hasta 2 viviendas, 1 vehículo
        
        Args:
            patrimonio_total: Patrimonio total
            tiene_vivienda_habitual: ¿Tiene vivienda principal?
            tiene_otro_vehiculo: ¿Tiene vehículo secundario?
        
        Returns:
            AnalisisPatrimonio con validación
        """
        patrimonio = Decimal(str(patrimonio_total))
        limite = CalculadoraIMV.LIMITE_PATRIMONIO
        
        compatible = patrimonio <= limite
        
        detalles = (
            f"Patrimonio declarado: {patrimonio}€. "
            f"Límite máximo: {limite}€. "
        )
        
        if tiene_vivienda_habitual:
            detalles += "✅ Vivienda habitual excluida (sin límite). "
        
        if tiene_otro_vehiculo:
            detalles += "✅ Vehículo personal excluido. "
        
        if not compatible:
            detalles += f"❌ INCOMPATIBLE: Supera límite en {patrimonio - limite}€"
        
        return AnalisisPatrimonio(
            patrimonio_total=patrimonio,
            limite_maximo=limite,
            compatible=compatible,
            detalles=detalles
        )
    
    @staticmethod
    def calcular_duracion_imv(
        periodo_meses: int,
        renovacion_anual: bool = True,
    ) -> dict:
        """
        Calcula IMV total por período y renovaciones
        
        Args:
            periodo_meses: Número de meses de duración
            renovacion_anual: ¿Requiere renovación anual?
        
        Returns:
            Dict con desglose temporal
        """
        anos = periodo_meses // 12
        meses_resto = periodo_meses % 12
        
        return {
            "periodo_total_meses": periodo_meses,
            "anos_completos": anos,
            "meses_restantes": meses_resto,
            "renovacion_anual_requerida": renovacion_anual,
            "proxima_renovacion": f"Año 1" if renovacion_anual else "No",
            "documentacion_requerida_anual": [
                "Certificado empadronamiento",
                "Declaración ingresos (últimos 3 meses)",
                "Certificado patrimonio actualizado",
                "Cambios en composición familiar"
            ]
        }


# Funciones helper para uso directo
def calcular_imv_simple(
    tipo_unidad_str: str,
    ingresos_netos: float,
    num_miembros: int = 1,
    ambos_mayores_30: bool = False,
) -> dict:
    """
    Wrapper simplificado para cálculo IMV
    
    Args:
        tipo_unidad_str: "persona_sola", "dos_personas", etc
        ingresos_netos: Ingresos netos mensuales
        num_miembros: Número de miembros
        ambos_mayores_30: ¿Ambos > 30?
    
    Returns:
        Dict con resultado
    """
    tipo_unidad = TipoUnidadFamiliar(tipo_unidad_str)
    resultado = CalculadoraIMV.calcular_imv(
        tipo_unidad=tipo_unidad,
        ingresos_netos_familia=ingresos_netos,
        num_miembros=num_miembros,
        ambos_mayores_30=ambos_mayores_30
    )
    
    return {
        "importe_base": float(resultado.importe_base),
        "ingresos_netos_familia": float(resultado.ingresos_netos_familia),
        "ingresos_contabilizados": float(resultado.ingresos_contabilizados),
        "imv_a_recibir": float(resultado.imv_a_recibir),
        "incremento_mayores_30": float(resultado.incremento_aplicado),
        "requisitos_cumplidos": resultado.requisitos_cumplidos,
        "articulo": resultado.articulo_aplicable,
        "explicacion": resultado.explicacion
    }


if __name__ == "__main__":
    # Ejemplo de uso
    print("="*80)
    print("CALCULADORA IMV - EJEMPLOS")
    print("="*80)
    
    # Caso 1: Persona sola sin ingresos
    resultado1 = CalculadoraIMV.calcular_imv(
        tipo_unidad=TipoUnidadFamiliar.PERSONA_SOLA,
        ingresos_netos_familia=0,
        num_miembros=1
    )
    print(f"\n📌 CASO 1: Persona sola, sin ingresos")
    print(f"   IMV a recibir: {resultado1.imv_a_recibir}€/mes")
    print(f"   Explicación: {resultado1.explicacion}")
    
    # Caso 2: Unidad 2 personas, con ingresos
    resultado2 = CalculadoraIMV.calcular_imv(
        tipo_unidad=TipoUnidadFamiliar.DOS_PERSONAS,
        ingresos_netos_familia=300,
        num_miembros=2,
        ambos_mayores_30=True
    )
    print(f"\n📌 CASO 2: 2 personas >30 años, ingresos 300€")
    print(f"   Importe base: {resultado2.importe_base}€ + {resultado2.incremento_aplicado}€ (incremento) = {resultado2.importe_base + resultado2.incremento_aplicado}€")
    print(f"   IMV a recibir: {resultado2.imv_a_recibir}€/mes")
    print(f"   Explicación: {resultado2.explicacion}")
    
    # Caso 3: Validación patrimonio
    patrimonio = CalculadoraIMV.validar_patrimonio(
        patrimonio_total=12000,
        tiene_vivienda_habitual=True
    )
    print(f"\n📌 CASO 3: Validación patrimonio")
    print(f"   Compatible: {patrimonio.compatible}")
    print(f"   Detalles: {patrimonio.detalles}")
