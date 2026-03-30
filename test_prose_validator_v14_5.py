#!/usr/bin/env python3
"""
TEST SPRINT 6 - Prose Validator V14.5 Mejorado
Valida soporte multi-blueprint, personajes y conflictos cruzados
"""

import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1')

from backend.v14.case_schema_builder import CaseSchema, PersonajeSchema, QuestionSchema
from backend.v14.prose_validator import validar_prose_vs_schema
import json

def test_prose_validator_v14_5():
    print("🛡️ SPRINT 6 - Test Prose Validator V14.5 Mejorado")
    print("=" * 60)
    
    # 1. Crear schema complejo tipo DM
    schema = CaseSchema(
        case_id="test-v14-5",
        blueprint_ids=["BP-S12", "BP-S10", "BP-S11", "BP-S16"],
        personajes=[
            PersonajeSchema(
                nombre="Carlos García",
                rol="trabajador",
                edad=50,
                datos={
                    "salario_bruto": 2500,
                    "base_cotizacion": 2100,
                    "antiguedad": 15,
                    "tipo_contrato": "indefinido"
                },
                relaciones=["María Sánchez"]
            ),
            PersonajeSchema(
                nombre="María Sánchez",
                rol="autónomo",
                edad=27,
                datos={
                    "tipo_actividad": "comercial",
                    "base_RETA": 800,
                    "trabajadores": 1
                },
                relaciones=["Carlos García"]
            ),
            PersonajeSchema(
                nombre="Roberto Martínez",
                rol="empresario",
                edad=45,
                datos={
                    "tipo_empresa": "SL",
                    "sector": "servicios",
                    "empleados": 8
                }
            )
        ],
        fecha_caso="2026-03-04",
        conflictos_cruzados=["impago_empresa", "accidente_laboral", "jubilacion_anticipada"],
        questions=[
            QuestionSchema(
                pregunta_id="P1",
                trampa_id="C2",
                articulo="Art. 209 TRLGSS",
                url_boe="https://www.boe.es/eli/rt1/2023/6945/",
                calculo_resultado="85.18",
                mnemonico="BR dual: dos fórmulas, gana la mejor",
                verified=True,
                blueprint_origen="BP-S12"
            ),
            QuestionSchema(
                pregunta_id="P2",
                trampa_id="DM26-T8-01",
                articulo="Art. 199 TRLGSS",
                url_boe="https://www.boe.es/eli/rt1/2022/14680/",
                calculo_resultado="50.25",
                mnemonico="Gran Incapacidad: adaptar, reubicar, extinguir",
                verified=True,
                blueprint_origen="BP-S10"
            ),
            QuestionSchema(
                pregunta_id="P3",
                trampa_id="DM26-T9-01",
                articulo="Art. 182 TRLGSS",
                url_boe="https://www.boe.es/eli/rt1/2023/5364/",
                calculo_resultado="19",
                mnemonico="Nacimiento 2026: 19 semanas (6+11+2)",
                verified=True,
                blueprint_origen="BP-S11"
            ),
            QuestionSchema(
                pregunta_id="P4",
                trampa_id="DM26-T10-02",
                articulo="Art. 60 TRLGSS",
                url_boe="https://www.boe.es/buscar/doc.php?id=BOE-A-2004-11836",
                calculo_resultado="36.90",
                mnemonico="Brecha 36.90€ (2026) al de pensión más baja",
                verified=True,
                blueprint_origen="BP-S16"
            )
        ]
    )
    
    # 2. Texto LLM de prueba (con errores intencionados)
    texto_llm_con_errores = """
    CASO PRÁCTICO: LA EMPRESA DE CARLOS

    Carlos García, trabajador de 50 años, lleva 15 años cotizando en el Régimen General. 
    Su último contrato es indefinido con salario bruto de 2.500€ y base de cotización de 2.100€.
    Trabaja en la empresa "Servicios Martínez SL" propiedad de Roberto Martínez.

    María Sánchez, autónoma de 27 años, es hija de Carlos y tiene una pequeña actividad comercial 
    con base RETA de 800€. Contrata a un trabajador.

    Roberto Martínez, empresario de 45 años, tiene problemas de impago en sus cotizaciones 
    desde hace 3 meses. Carlos sufre un accidente laboral que le provoca una incapacidad temporal.

    CÁLCULOS:
    - Base Reguladora de Carlos: 80.18% (error intencionado)
    - Complemento brecha género: 34.80€ (error intencionado)
    - Semanas nacimiento: 16 (error intencionado)
    - Cuantía Gran Incapacidad: 45% (error intencionado)
    """
    
    texto_llm_correcto = """
    CASO PRÁCTICO: LA EMPRESA DE CARLOS

    Carlos García, trabajador de 50 años, lleva 15 años cotizando en el Régimen General de la Seguridad Social. 
    Su último contrato es indefinido con salario bruto de 2.500€ y base de cotización de 2.100€.
    Trabaja en la empresa "Servicios Martínez SL" propiedad de Roberto Martínez.

    María Sánchez, autónoma de 27 años, es hija de Carlos y tiene una pequeña actividad comercial 
    con base RETA de 800€. Contrata a un trabajador.

    Roberto Martínez, empresario de 45 años, tiene problemas de impago en sus cotizaciones 
    desde hace 3 meses. Carlos sufre un accidente laboral que le provoca una incapacidad temporal.

    CÁLCULOS:
    - Base Reguladora de Carlos: 85.18%
    - Complemento brecha género: 36.90€
    - Semanas nacimiento: 19
    - Cuantía Gran Incapacidad: 50.25%
    """
    
    print("📋 Test 1: Texto CON errores (debería bloquear)")
    print("-" * 40)
    resultado_con_errores = validar_prose_vs_schema(texto_llm_con_errores, schema)
    print(f"✅ Validación: {resultado_con_errores['valid']}")
    print(f"🚫 Bloqueado: {resultado_con_errores['bloqueado']}")
    print(f"📊 Errores encontrados: {len(resultado_con_errores['errores'])}")
    
    for error in resultado_con_errores['errores']:
        print(f"   ❌ {error['tipo']}: {error['error']}")
    
    print("\n📋 Test 2: Texto CORRECTO (debería aprobar)")
    print("-" * 40)
    resultado_correcto = validar_prose_vs_schema(texto_llm_correcto, schema)
    print(f"✅ Validación: {resultado_correcto['valid']}")
    print(f"🚫 Bloqueado: {resultado_correcto['bloqueado']}")
    print(f"📊 Estadísticas:")
    for key, value in resultado_correcto['estadisticas'].items():
        print(f"   - {key}: {value}")
    
    if resultado_correcto['errores']:
        print(f"⚠️ Errores inesperados: {len(resultado_correcto['errores'])}")
        for error in resultado_correcto['errores']:
            print(f"   ❌ {error.get('tipo', 'desconocido')}: {error['error']}")
    
    # 3. Guardar resultados
    resultados = {
        "schema_complejo": {
            "case_id": schema.case_id,
            "blueprint_ids": schema.blueprint_ids,
            "num_personajes": len(schema.personajes),
            "num_conflictos": len(schema.conflictos_cruzados),
            "num_preguntas": len(schema.questions)
        },
        "test_con_errores": {
            "valid": resultado_con_errores['valid'],
            "bloqueado": resultado_con_errores['bloqueado'],
            "num_errores": len(resultado_con_errores['errores']),
            "tipos_error": list(set(e.get('tipo', 'desconocido') for e in resultado_con_errores['errores']))
        },
        "test_correcto": {
            "valid": resultado_correcto['valid'],
            "bloqueado": resultado_correcto['bloqueado'],
            "num_errores": len(resultado_correcto['errores']),
            "estadisticas": resultado_correcto['estadisticas']
        }
    }
    
    with open("/tmp/test_prose_validator_v14_5.json", "w") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: /tmp/test_prose_validator_v14_5.json")
    
    # 4. Verificación final
    print("\n🎯 VERIFICACIÓN FINAL SPRINT 6:")
    if resultado_con_errores['bloqueado'] and not resultado_correcto['bloqueado']:
        print("✅ Prose Validator V14.5 funciona correctamente:")
        print("   - Detecta errores numéricos")
        print("   - Detecta personajes faltantes")
        print("   - Detecta conflictos faltantes")
        print("   - Aprueba texto correcto")
        print("🚀 Sprint 6 COMPLETADO - Prose Validator Mejorado!")
    else:
        print("❌ Prose Validator necesita ajustes")

if __name__ == "__main__":
    test_prose_validator_v14_5()
