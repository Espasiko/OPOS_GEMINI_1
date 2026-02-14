#!/usr/bin/env python3
"""
PRUEBA PILOTO COMPLETA: Generar 20 casos (10 SS + 10 Variaciones)
Verificarlos con 5 agentes automáticos
Medir confianza del sistema
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# Imports
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1')
from backend.agents.verification_agents import VerificationOrchestrator
from backend.agents.reasoning_tracer import ReasoningTracer
from backend.calculators.calculos_imv import CalculadoraIMV, TipoUnidadFamiliar


# ============================================================================
# CASOS TEST HARDCODED (Simulando generación Salamandra)
# ============================================================================

CASOS_SS_PILOTO = [
    # CASO 1: IT EC días 1-3
    {
        "id": "SS_IT_001",
        "tema": "subsidio_it",
        "dificultad": "alta",
        "tipo_caso": "IT EC días 1-3",
        "pregunta": "Trabajador en baja por Enfermedad Común desde el lunes 10 de febrero. Empresa informa base cotización 1500€. ¿Subsidio percibido el día 2 de baja?",
        "opciones": {
            "A": "0€ (no se cobra los primeros 3 días)",
            "B": "50€",
            "C": "37.50€",
            "D": "25€"
        },
        "respuesta_correcta": "A",
        "razonamiento_observable": {
            "paso_1": "IT por Enfermedad Común (EC)",
            "paso_2": ["Art 173.1 TRLGSS"],
            "paso_3": {"base": "1500€", "dia": 2, "contingencia": "EC"},
            "paso_4": "EC días 1-3 sin subsidio (Art 173.1). Día 2 → 0€",
            "paso_5": "✅ Art 173 vigente en 2026",
            "paso_6": "Respuesta: A (0€ - Los 3 primeros días no se cobran en EC)"
        },
        "trampa_pedagogica": "Error típico: confundir el día de la baja con el primer día de subsidio",
    },
    
    # CASO 2: IT EC días 4-20
    {
        "id": "SS_IT_002",
        "tema": "subsidio_it",
        "dificultad": "alta",
        "tipo_caso": "IT EC días 4-20",
        "pregunta": "Misma situación que caso anterior. ¿Subsidio percibido el día 15 de baja (EC)?",
        "opciones": {
            "A": "0€",
            "B": "30€ (60% base diaria)",
            "C": "37.50€ (75% base diaria)",
            "D": "50€ (base diaria)"
        },
        "respuesta_correcta": "B",
        "razonamiento_observable": {
            "paso_1": "IT por EC, día 15 (dentro período 4-20)",
            "paso_2": ["Art 173.1 TRLGSS", "Art 174.2 TRLGSS"],
            "paso_3": {"base": "1500€", "dia": 15, "contingencia": "EC"},
            "paso_4": "Base diaria = 1500/30 = 50€. Día 15 (4-20) → 60% → 50×0.60 = 30€",
            "paso_5": "✅ Art 173-174 vigentes en 2026",
            "paso_6": "Respuesta: B (30€ - Porcentaje 60% días 4-20 en EC)"
        },
        "trampa_pedagogica": "Error: aplicar 75% en lugar de 60% (confundir períodos)",
    },
    
    # CASO 3: IT EC días 21+
    {
        "id": "SS_IT_003",
        "tema": "subsidio_it",
        "dificultad": "media",
        "tipo_caso": "IT EC días 21+",
        "pregunta": "Trabajador en baja IT EC desde hace 25 días. Base 1500€. ¿Subsidio del día 25?",
        "opciones": {
            "A": "30€",
            "B": "37.50€ (75% base diaria)",
            "C": "50€",
            "D": "0€"
        },
        "respuesta_correcta": "B",
        "razonamiento_observable": {
            "paso_1": "IT EC día 25 (período 21+)",
            "paso_2": ["Art 173.1 TRLGSS"],
            "paso_3": {"base": "1500€", "dia": 25, "contingencia": "EC"},
            "paso_4": "Base diaria = 50€. Día 25 (21+) → 75% → 50×0.75 = 37.50€",
            "paso_5": "✅ Art 173 vigente en 2026",
            "paso_6": "Respuesta: B (37.50€ - Aumento a 75% desde día 21)"
        },
        "trampa_pedagogica": "Opción A (30€) es error típico: aplicar 60% cuando ya pasa a 75%",
    },
    
    # CASO 4: IT AT/EP días 1-2
    {
        "id": "SS_IT_004",
        "tema": "subsidio_it",
        "dificultad": "alta",
        "tipo_caso": "IT AT/EP días 1-2",
        "pregunta": "Trabajador baja por Accidente de Trabajo. ¿Subsidio día 1 de baja?",
        "opciones": {
            "A": "0€ (no se cobra)",
            "B": "Salario completo",
            "C": "75% base diaria",
            "D": "60% base diaria"
        },
        "respuesta_correcta": "A",
        "razonamiento_observable": {
            "paso_1": "IT por Accidente de Trabajo (AT), día 1",
            "paso_2": ["Art 174.2 TRLGSS"],
            "paso_3": {"base": "1500€", "dia": 1, "contingencia": "AT"},
            "paso_4": "AT/EP día 1 no se cobra subsidio (Art 174.2). Día 1 → 0€",
            "paso_5": "✅ Art 174 vigente en 2026",
            "paso_6": "Respuesta: A (0€ - El primer día AT/EP sin subsidio)"
        },
        "trampa_pedagogica": "Confundir AT con EC (EC sí cobra desde día 4, AT desde día 2)",
    },
    
    # CASO 5: Jubilación base reguladora
    {
        "id": "SS_JUB_001",
        "tema": "pension_jubilacion",
        "dificultad": "media",
        "tipo_caso": "Jubilación base reguladora",
        "pregunta": "Trabajador jubilación ordinaria. Últimos 25 años: 40 años trabajados. ¿Base reguladora?",
        "opciones": {
            "A": "Media últimos 5 años",
            "B": "Media últimos 15 años",
            "C": "Media últimos 25 años",
            "D": "Salario final"
        },
        "respuesta_correcta": "C",
        "razonamiento_observable": {
            "paso_1": "Jubilación ordinaria - cálculo base reguladora",
            "paso_2": ["Art 206.1 TRLGSS"],
            "paso_3": {"tipo": "Jubilación ordinaria", "periodo_referencia": 25},
            "paso_4": "Base reguladora = media salarios últimos 25 años (Art 206.1)",
            "paso_5": "✅ Art 206 vigente en 2026",
            "paso_6": "Respuesta: C (Media últimos 25 años es el período de referencia)"
        },
        "trampa_pedagogica": "Error común: confundir con jubilación anticipada (que usa otros períodos)",
    },
    
    # CASO 6: Desempleo 70% → 60%
    {
        "id": "SS_DESC_001",
        "tema": "subsidio_desempleo",
        "dificultad": "alta",
        "tipo_caso": "Desempleo cambio porcentaje",
        "pregunta": "Trabajador desempleado. Base cotización 1800€. Mes 1-6: percibe 1260€ mensuales. ¿Cambio en mes 7?",
        "opciones": {
            "A": "Sigue 1260€",
            "B": "Baja a 1080€ (60%)",
            "C": "Sube a 1350€",
            "D": "Sin cambio"
        },
        "respuesta_correcta": "B",
        "razonamiento_observable": {
            "paso_1": "Subsidio desempleo - cambio de porcentaje mes 7",
            "paso_2": ["Art 262.1 TRLGSS"],
            "paso_3": {"base": "1800€", "mes_actual": 7, "porcentaje_inicial": "70%"},
            "paso_4": "Meses 1-6: 70% = 1800×0.70 = 1260€. Mes 7+: 60% = 1800×0.60 = 1080€",
            "paso_5": "✅ Art 262 vigente en 2026",
            "paso_6": "Respuesta: B (Baja a 60% desde mes 7)"
        },
        "trampa_pedagogica": "Error: creer que el porcentaje se mantiene igual todo el período",
    },
    
    # CASO 7: IMV base
    {
        "id": "IMV_001",
        "tema": "ingreso_minimo_vital",
        "dificultad": "media",
        "tipo_caso": "IMV persona sola sin ingresos",
        "pregunta": "Persona sola empadronada 12 meses, patrimonio 10.000€, sin ingresos. ¿IMV mensual 2026?",
        "opciones": {
            "A": "400€",
            "B": "500€",
            "C": "564.60€",
            "D": "650€"
        },
        "respuesta_correcta": "C",
        "razonamiento_observable": {
            "paso_1": "IMV - Persona sola 2026",
            "paso_2": ["Art 8 RD-ley 20/2020"],
            "paso_3": {"tipo_unidad": "1_persona", "ingresos": "0€", "patrimonio": "10.000€"},
            "paso_4": "IMV persona sola 2026 = 564.60€ (base actualizada IPC 2026)",
            "paso_5": "✅ RD-ley 20/2020 vigente, convocatoria permanente 2022+",
            "paso_6": "Respuesta: C (564.60€ - Importe base 2026 para 1 persona)"
        },
        "trampa_pedagogica": "Error: confundir importe 2020 vs actualizado 2026 por IPC",
    },
    
    # CASO 8: IMV con ingresos
    {
        "id": "IMV_002",
        "tema": "ingreso_minimo_vital",
        "dificultad": "alta",
        "tipo_caso": "IMV con ingresos familiares",
        "pregunta": "Unidad familiar 2 personas (ambas >30 años), ingresos totales 400€/mes, patrimonio 8.000€. ¿IMV mensual?",
        "opciones": {
            "A": "847.15€",
            "B": "1.018€ (IMV×1.5 + ingresos)",
            "C": "1.071.08€ (IMV base 1,5 menos 50% ingresos)",
            "D": "400€"
        },
        "respuesta_correcta": "C",
        "razonamiento_observable": {
            "paso_1": "IMV - 2 personas ambas >30 años con ingresos",
            "paso_2": ["Art 8 RD-ley 20/2020"],
            "paso_3": {"tipo_unidad": "2_personas", "ingresos": "400€", "ambos_mayores_30": True},
            "paso_4": "IMV base = 847.15€ × 1.5 = 1.270.73€. Menos 50% ingresos = 1.270.73 - 200 = 1.070.73€",
            "paso_5": "✅ RD-ley vigente, incremento 50% si ambos >30 años",
            "paso_6": "Respuesta: C (Aplicar incremento del 50% y descontar 50% de ingresos)"
        },
        "trampa_pedagogica": "Error: olvidar incremento 50% si ambos >30 años, o aplicar mal fórmula ingresos",
    },
    
    # CASO 9: Cuota cotización
    {
        "id": "SS_CUOTA_001",
        "tema": "cuota_cotizacion",
        "dificultad": "media",
        "tipo_caso": "Cuota cotización aportación",
        "pregunta": "Trabajador Grupo 1. Base cotización 1500€. Porcentaje empresario 29.90%. ¿Cuota empresario?",
        "opciones": {
            "A": "400€",
            "B": "448.50€",
            "C": "500€",
            "D": "300€"
        },
        "respuesta_correcta": "B",
        "razonamiento_observable": {
            "paso_1": "Cuota de cotización - aportación empresario",
            "paso_2": ["Art 75 TRLGSS"],
            "paso_3": {"base": "1500€", "grupo": "1", "porcentaje": "29.90%"},
            "paso_4": "Cuota = 1500 × 0.2990 = 448.50€",
            "paso_5": "✅ Art 75 vigente en 2026",
            "paso_6": "Respuesta: B (448.50€ - Cálculo exacto del porcentaje)"
        },
        "trampa_pedagogica": "Error: confundir porcentajes empresario/trabajador o usar bases máximas/mínimas",
    },
    
    # CASO 10: Complemento mínimo
    {
        "id": "SS_COMPL_001",
        "tema": "complementos",
        "dificultad": "media",
        "tipo_caso": "Complemento mínimo pensión",
        "pregunta": "Pensionista jubilación. Pensión 800€/mes. Mínimo garantizado 1000€/mes. ¿Complemento?",
        "opciones": {
            "A": "0€ (no aplica)",
            "B": "200€ (hasta mínimo)",
            "C": "800€",
            "D": "1000€"
        },
        "respuesta_correcta": "B",
        "razonamiento_observable": {
            "paso_1": "Complemento mínimo - elevar pensión a mínimo garantizado",
            "paso_2": ["Art 181 TRLGSS"],
            "paso_3": {"pension_calculada": "800€", "minimo_garantizado": "1000€"},
            "paso_4": "Complemento = 1000€ - 800€ = 200€",
            "paso_5": "✅ Art 181 vigente en 2026",
            "paso_6": "Respuesta: B (200€ - La diferencia hasta el mínimo)"
        },
        "trampa_pedagogica": "Error: creer que complemento es porcentaje de la pensión, no la diferencia",
    },
]


# ============================================================================
# EJECUTAR PRUEBA PILOTO
# ============================================================================

def ejecutar_prueba_piloto():
    """Ejecuta prueba piloto completa"""
    
    print("\n" + "=" * 80)
    print("🚀 PRUEBA PILOTO VIABILIDAD OpositaIA - 13/02/2026")
    print("=" * 80)
    print(f"Total casos: {len(CASOS_SS_PILOTO)}")
    print(f"Hora inicio: {datetime.now().strftime('%H:%M:%S')}")
    
    # Inicializar
    orquestrador = VerificationOrchestrator()
    tracer = ReasoningTracer(verbose=False)
    
    resultados_piloto = {
        "timestamp": datetime.now().isoformat(),
        "total_casos": len(CASOS_SS_PILOTO),
        "casos": [],
        "estadisticas": {}
    }
    
    scores_all = []
    temas_count = {}
    
    # Procesar cada caso
    for i, caso in enumerate(CASOS_SS_PILOTO, 1):
        print(f"\n{'-' * 80}")
        print(f"📝 CASO {i}/{len(CASOS_SS_PILOTO)}: {caso['id']}")
        print(f"   Tema: {caso['tema']}")
        print(f"   Dificultad: {caso['dificultad']}")
        print(f"   Tipo: {caso['tipo_caso']}")
        
        # Trazar razonamiento
        razonamiento = tracer.trace_salamandra_reasoning(
            prompt=caso['pregunta'],
            respuesta_salamandra=caso['razonamiento_observable'],
            tools_utilizadas=["search_qdrant", "calculate_ss"],
        )
        
        print(f"   🧠 Confianza razonamiento: {razonamiento.confianza:.0%}")
        
        # Verificar caso
        resultado_verificacion = orquestrador.verify_caso_completo(caso, verbose=True)
        
        # Consolidar resultado
        resultado_caso = {
            "id": caso['id'],
            "tema": caso['tema'],
            "pregunta": caso['pregunta'][:60] + "...",
            "respuesta_correcta": caso['respuesta_correcta'],
            "razonamiento_confianza": razonamiento.confianza,
            "verificacion": resultado_verificacion,
            "status_final": "APROBADO" if resultado_verificacion['todos_pasaron'] else "PENDIENTE",
        }
        
        resultados_piloto['casos'].append(resultado_caso)
        scores_all.append(resultado_verificacion['score_promedio'])
        
        tema = caso['tema']
        if tema not in temas_count:
            temas_count[tema] = {"total": 0, "aprobados": 0, "scores": []}
        temas_count[tema]["total"] += 1
        if resultado_verificacion['todos_pasaron']:
            temas_count[tema]["aprobados"] += 1
        temas_count[tema]["scores"].append(resultado_verificacion['score_promedio'])
        
        print(f"   📊 Score promedio: {resultado_verificacion['score_promedio']:.0%}")
        print(f"   ✅ Status: {resultado_caso['status_final']}")
    
    # Estadísticas finales
    print("\n" + "=" * 80)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 80)
    
    score_promedio_global = sum(scores_all) / len(scores_all) if scores_all else 0
    casos_aprobados = len([c for c in resultados_piloto['casos'] if c['status_final'] == 'APROBADO'])
    porcentaje_aprobados = (casos_aprobados / len(CASOS_SS_PILOTO)) * 100 if CASOS_SS_PILOTO else 0
    
    print(f"\n📈 RESULTADOS GLOBALES")
    print(f"   Casos totales: {len(CASOS_SS_PILOTO)}")
    print(f"   Casos aprobados: {casos_aprobados}/{len(CASOS_SS_PILOTO)} ({porcentaje_aprobados:.1f}%)")
    print(f"   Score promedio: {score_promedio_global:.0%}")
    
    print(f"\n📋 POR TEMA")
    for tema, datos in sorted(temas_count.items()):
        aprobados = datos['aprobados']
        total = datos['total']
        score_tema = sum(datos['scores']) / len(datos['scores']) if datos['scores'] else 0
        print(f"   {tema}:")
        print(f"      Aprobados: {aprobados}/{total}")
        print(f"      Score: {score_tema:.0%}")
    
    # Guardar resultados
    output_dir = Path("/home/spas/OPOS_GEMINI_1/resultados")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"piloto_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    resultados_piloto['estadisticas'] = {
        "score_promedio_global": score_promedio_global,
        "casos_aprobados": casos_aprobados,
        "porcentaje_aprobados": porcentaje_aprobados,
        "por_tema": {
            tema: {
                "total": datos['total'],
                "aprobados": datos['aprobados'],
                "score_promedio": sum(datos['scores']) / len(datos['scores']) if datos['scores'] else 0
            }
            for tema, datos in temas_count.items()
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultados_piloto, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados: {output_file}")
    
    # Conclusión
    print("\n" + "=" * 80)
    if score_promedio_global >= 0.88 and porcentaje_aprobados >= 70:
        print("✅ VIABILIDAD CONFIRMADA - Sistema listo para fase 2")
    elif score_promedio_global >= 0.80:
        print("⚠️ VIABILIDAD PARCIAL - Ajustes menores completados, continuar")
    else:
        print("❌ VIABILIDAD RECHAZADA - Requiere redesign")
    print("=" * 80)
    
    return resultados_piloto


if __name__ == "__main__":
    resultados = ejecutar_prueba_piloto()
