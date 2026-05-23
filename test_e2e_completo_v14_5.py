#!/usr/bin/env python3
"""
TEST E2E COMPLETO V14.5 - Caso Complejo DM + LLM Narrator + Prose Validator
Genera un caso completo y valida todo el flujo end-to-end
"""

import sys
import os
import json

# ── CWD guard + path ─────────────────────────────────────────────────
_PROJ_ROOT = os.path.abspath(os.path.dirname(__file__))
if os.getcwd() != _PROJ_ROOT:
    os.chdir(_PROJ_ROOT)
    print(f"ℹ️  CWD cambiado a: {_PROJ_ROOT}")
sys.path.insert(0, _PROJ_ROOT)

from dotenv import load_dotenv
load_dotenv()

from mistralai import Mistral
import yaml
from backend.v14.case_schema_builder import CaseSchemaBuilder
from backend.v14.prose_validator import validar_prose_vs_schema

def analizar_casos_dm():
    """Analiza casos reales de DM para extraer patrones"""
    casos_dm = {
        "caso_19": {
            "personajes": ["José Manuel Garmendia", "Alicia Sierra"],
            "roles": ["trabajador", "trabajadora"],
            "temas": ["jubilacion", "cotizacion"],
            "conflictos": ["jubilacion_anticipada", "base_cotizacion"],
            "complejidad": "medio"  # 2 personajes, 2 temas
        },
        "caso_18": {
            "personajes": ["María Ángeles", "José Alberto"],
            "roles": ["funcionario", "funcionario"],
            "temas": ["recaudacion", "encuadramiento"],
            "conflictos": ["impago_empresa", "deuda_AAPP"],
            "complejidad": "alto"  # 2 personajes, 2 temas + conflicto
        }
    }
    
    print("📊 ANÁLISIS DE CASOS DM REALES:")
    print("=" * 50)
    
    for caso, datos in casos_dm.items():
        print(f"\n📋 {caso.upper()}:")
        print(f"   - Personajes: {len(datos['personajes'])} ({', '.join(datos['personajes'])})")
        print(f"   - Roles: {', '.join(datos['roles'])}")
        print(f"   - Temas: {', '.join(datos['temas'])}")
        print(f"   - Conflictos: {', '.join(datos['conflictos'])}")
        print(f"   - Complejidad: {datos['complejidad']}")
    
    return casos_dm

def test_e2e_completo():
    print("🚀 TEST E2E COMPLETO V14.5 - Caso Complejo DM")
    print("=" * 60)

    # ── Check MISTRAL_API_KEY antes de empezar ─────────────────────────────
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("❌ MISTRAL_API_KEY no encontrada en .env ni en entorno. Abortando.")
        return
    
    # 1. Analizar casos DM reales
    casos_dm = analizar_casos_dm()
    
    # 2. Generar caso complejo con nuestro builder
    print("\n🛠️ [1/5] GENERANDO CASO COMPLEJO V14.5...")
    try:
        builder = CaseSchemaBuilder()
        # fecha_caso=2026-03-04: fecha de corte del examen (legislación vigente a esa fecha)
        schema = builder.build_complex(
            blueprint_ids=["BP-S12", "BP-S10", "BP-S11", "BP-S16"],
            fecha_caso="2026-03-04"
        )
        print(f"✅ Schema generado: {schema.case_id}")
        print(f"📊 Estadísticas:")
        print(f"   - Blueprints: {schema.blueprint_ids}")
        print(f"   - Personajes: {len(schema.personajes)}")
        print(f"   - Conflictos: {schema.conflictos_cruzados}")
        print(f"   - Preguntas: {len(schema.questions)}")
        
        # Convertir schema a JSON para el LLM
        import dataclasses
        schema_dict = dataclasses.asdict(schema)
        schema_json = json.dumps(schema_dict, indent=2, ensure_ascii=False)
        
    except Exception as e:
        print(f"❌ Error generando schema: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 3. Cargar LLM Narrator V14
    print("\n🤖 [2/5] CARGANDO LLM NARRATOR V14...")
    try:
        with open("opos-agents/agents/redactor_v14.yaml", "r") as f:
            config = yaml.safe_load(f)["agent"]
        
        system_prompt = config["system_prompt"].replace("{schema_json}", schema_json)
        model = config["model"]
        temperature = config["temperature"]
        
        client = Mistral(api_key=api_key)
        print(f"✅ Modelo: {model} | Temperatura: {temperature}")
        
    except Exception as e:
        print(f"❌ Error cargando LLM: {e}")
        return
    
    # 4. Generar narrativa con LLM
    print("\n✍️ [3/5] GENERANDO NARRATIVA CON LLM...")
    try:
        response = client.chat.complete(
            model=model,
            temperature=temperature,
            max_tokens=8000,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""
                Genera un caso práctico complejo tipo Diego de Miguel con las siguientes características:
                
                PERSONAJES: {len(schema.personajes)} personajes entrelazados
                TEMAS: {', '.join(schema.blueprint_ids)}
                CONFLICTOS: {', '.join(schema.conflictos_cruzados)}
                
                Usa el estilo DM: narrativa fluida, personajes con nombres propios, 
                situaciones laborales y familiares entrelazadas, datos numéricos exactos del schema.
                
                Incluye 15 preguntas tipo test con opciones A, B, C, D distribuidas equitativamente.
                """}
            ]
        )
        
        narrativa = response.choices[0].message.content
        print("✅ Narrativa generada")
        print(f"   - Longitud: {len(narrativa)} caracteres")
        
        # Guardar narrativa
        with open("/tmp/narrativa_compleja_v14_5.md", "w", encoding='utf-8') as f:
            f.write(narrativa)
        print("   -> Guardada en /tmp/narrativa_compleja_v14_5.md")
        
    except Exception as e:
        print(f"❌ Error generando narrativa: {e}")
        return
    
    # 5. Validar con Prose Validator V14.5
    print("\n🛡️ [4/5] VALIDANDO CON PROSE VALIDATOR V14.5...")
    try:
        validacion = validar_prose_vs_schema(narrativa, schema)
        
        print(f"📊 Resultado Validación:")
        print(f"   - Válido: {validacion['valid']}")
        print(f"   - Bloqueado: {validacion['bloqueado']}")
        print(f"   - Errores: {len(validacion['errores'])}")
        
        if validacion['errores']:
            print("\n❌ ERRORES DETECTADOS:")
            for error in validacion['errores']:
                tipo = error.get('tipo', 'desconocido')
                print(f"   - {tipo.upper()}: {error['error']}")
        
        # Estadísticas
        if 'estadisticas' in validacion:
            print(f"\n📈 ESTADÍSTICAS:")
            stats = validacion['estadisticas']
            for key, value in stats.items():
                print(f"   - {key}: {value}")
        
        # Guardar validación
        with open("/tmp/validacion_compleja_v14_5.json", "w", encoding='utf-8') as f:
            json.dump(validacion, f, indent=2, ensure_ascii=False)
        print("   -> Guardada en /tmp/validacion_compleja_v14_5.json")
        
    except Exception as e:
        print(f"❌ Error en validación: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 6. Comparar con casos DM reales
    print("\n📈 [5/5] COMPARANDO CON CASOS DM REALES...")
    
    # Métricas de complejidad
    metricas_nuestro = {
        "personajes": len(schema.personajes),
        "blueprints": len(schema.blueprint_ids),
        "conflictos": len(schema.conflictos_cruzados),
        "preguntas": len(schema.questions),
        "complejidad_total": len(schema.personajes) + len(schema.blueprint_ids) + len(schema.conflictos_cruzados)
    }
    
    print(f"\n📊 NUESTRAS MÉTRICAS:")
    for key, value in metricas_nuestro.items():
        print(f"   - {key}: {value}")
    
    print(f"\n📊 COMPARATIVA CON DM:")
    for caso, datos in casos_dm.items():
        metricas_dm = {
            "personajes": len(datos['personajes']),
            "temas": len(datos['temas']),
            "conflictos": len(datos['conflictos']),
            "complejidad_total": len(datos['personajes']) + len(datos['temas']) + len(datos['conflictos'])
        }
        
        print(f"\n   {caso.upper()}:")
        for key in ['personajes', 'blueprints', 'conflictos', 'complejidad_total']:
            nuestro = metricas_nuestro.get(key, 0)
            dm = metricas_dm.get(key.replace('blueprints', 'temas'), 0)  # Mapeo para comparación
            status = "✅ SUPERAMOS" if nuestro > dm else "⚠️ IGUALAMOS" if nuestro == dm else "❌ INFERIORES"
            print(f"      - {key}: Nosotros {nuestro} vs DM {dm} {status}")
    
    # 7. Veredicto final
    print("\n🎯 VEREDICTO FINAL SPRINT 6:")
    if validacion['valid'] and metricas_nuestro['complejidad_total'] >= 8:
        print("✅ ÉXITO TOTAL:")
        print("   - Prose Validator V14.5 funciona")
        print("   - LLM Narrator genera casos complejos")
        print("   - Superamos complejidad de casos DM reales")
        print("   - Sistema listo para producción")
        print("🚀 SPRINT 6 COMPLETADO - SISTEMA V14.5 OPERATIVO!")
    else:
        print("⚠️ PARCIAL:")
        if not validacion['valid']:
            print("   - Prose Validator necesita ajustes")
        if metricas_nuestro['complejidad_total'] < 8:
            print("   - Complejidad inferior a casos DM")
    
    # 8. Guardar resultados completos
    resultados_finales = {
        "test_e2e_v14_5": {
            "timestamp": "2026-03-25",
            "schema_generado": {
                "case_id": schema.case_id,
                "personajes": len(schema.personajes),
                "blueprints": len(schema.blueprint_ids),
                "conflictos": len(schema.conflictos_cruzados),
                "preguntas": len(schema.questions)
            },
            "narrativa_generada": {
                "longitud": len(narrativa),
                "archivo": "/tmp/narrativa_compleja_v14_5.md"
            },
            "validacion": {
                "valida": validacion['valid'],
                "bloqueado": validacion['bloqueado'],
                "errores": len(validacion['errores'])
            },
            "comparacion_dm": {
                "nuestro_complejidad": metricas_nuestro['complejidad_total'],
                "caso_19_complejidad": casos_dm['caso_19']['complejidad'],
                "caso_18_complejidad": casos_dm['caso_18']['complejidad']
            }
        }
    }
    
    with open("/tmp/test_e2e_completo_v14_5.json", "w", encoding='utf-8') as f:
        json.dump(resultados_finales, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados completos guardados en: /tmp/test_e2e_completo_v14_5.json")

if __name__ == "__main__":
    test_e2e_completo()
