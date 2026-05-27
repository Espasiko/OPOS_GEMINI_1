import sys
import os
from decimal import Decimal

# Asegurar que el path incluye el proyecto
sys.path.append('/home/spas/OPOS_GEMINI_1')

from backend.calculators.calculos_ss import CalculadoraSS
from backend.calculators.calculos_ss_extended import CalculadoraJubilacion, CalculadoraIPP

def test_v12_fixes():
    print("=== TEST DE VERIFICACIÓN LEGAL V12 ===")
    
    # 1. Test Jubilación 2026 (Caso Juan: 36.33 años cotizados < 38.25)
    print("\n1. Verificando Jubilación 2026 (DT 7ª):")
    años_juan = 36.33 # 36 años y 4 meses aprox
    edad_legal = CalculadoraJubilacion.obtener_edad_legal_2026(años_juan)
    print(f"Años cotizados: {años_juan}")
    print(f"Edad legal calculada: {edad_legal:.4f} (Debe ser ~66.83)")
    assert 66.8 < edad_legal < 66.9, "Error en edad legal jubilación"
    
    # 2. Test Base Reguladora IT RDL 11/2024 (Promedio 3 meses)
    print("\n2. Verificando Base Reguladora IT (RDL 11/2024):")
    bases = [2000.0, 2100.0, 2200.0]
    dias = 91
    br_nueva = CalculadoraSS.calcular_base_reguladora_it_2026(bases, dias)
    br_esperada = (Decimal("6300") / Decimal("91")).quantize(Decimal("0.01"))
    print(f"Bases: {bases}, Días: {dias}")
    print(f"BR calculada: {br_nueva}")
    assert br_nueva == br_esperada, "Error en cálculo BR RDL 11/2024"
    
    # 3. Test Pagadores AT (Día 2+)
    print("\n3. Verificando Pagadores Accidentes de Trabajo (AT):")
    res_at = CalculadoraSS.calcular_subsidio_it(2000.0, "AT", 5) # Día 5 de baja
    print(f"Día 5 AT - Pagador: {res_at.pagador}")
    assert "INSS/Mutua" in res_at.pagador, "Error: En AT el día 5 debe pagar Mutua/INSS, no empresa delegado"
    
    # 4. Test IPP (Indemnización 24 meses)
    print("\n4. Verificando IPP (Art. 196.1):")
    res_ipp = CalculadoraIPP.calcular_ipp(Decimal("2000.0"))
    print(f"Base 2000€ - Indemnización: {res_ipp['cuantia_indemnizacion']}€")
    assert res_ipp['cuantia_indemnizacion'] == 48000.0, "Error en indemnización IPP"
    
    print("\n✅ TODOS LOS TESTS PASADOS - SISTEMA ALINEADO CON BOE 2026/RDL 11/2024")

if __name__ == "__main__":
    test_v12_fixes()
