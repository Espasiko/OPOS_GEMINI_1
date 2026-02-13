#!/usr/bin/env python3
"""
Script de prueba para generar UN caso con Salamandra VPS
"""
import asyncio
import httpx
import json
import sys


async def test_generate_case():
    """Prueba la generación de un caso"""
    
    print("=" * 80)
    print("🧪 PRUEBA DE CONCEPTO: SALAMANDRA VPS + SISTEMA DE AGENTES")
    print("=" * 80)
    print()
    
    # Configuración
    base_url = "http://localhost:8000"
    endpoint = f"{base_url}/casos/generate-one"
    
    # Request
    request_data = {
        "tema": "Incapacidad Temporal por Enfermedad Común, base 1500€, día 10",
        "dificultad": "media"
    }
    
    print("📋 REQUEST:")
    print(json.dumps(request_data, indent=2, ensure_ascii=False))
    print()
    
    try:
        # Health check primero
        print("🔍 Verificando health del servicio...")
        async with httpx.AsyncClient(timeout=5.0) as client:
            health_response = await client.get(f"{base_url}/casos/health")
            if health_response.status_code == 200:
                print("✅ Servicio healthy")
                print(json.dumps(health_response.json(), indent=2))
            else:
                print(f"❌ Health check failed: {health_response.status_code}")
                return
        
        print()
        print("🚀 Generando caso con Salamandra VPS...")
        print("   (Esto puede tomar 10-30 segundos)")
        print()
        
        # Generar caso
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(endpoint, json=request_data)
            
            if response.status_code == 200:
                result = response.json()
                
                print("=" * 80)
                print("✅ CASO GENERADO EXITOSAMENTE")
                print("=" * 80)
                print()
                
                # Mostrar cálculo usado
                print("📊 CÁLCULO USADO:")
                print(json.dumps(result['calculo_usado'], indent=2, ensure_ascii=False))
                print()
                
                # Mostrar confidence
                print("🎯 CONFIDENCE SCORE:")
                confidence = result['confidence']
                print(f"  Overall: {confidence['overall']:.2f}")
                print(f"  Level: {confidence['level']}")
                print(f"  Breakdown:")
                for key, value in confidence['breakdown'].items():
                    print(f"    - {key}: {value:.2f}")
                if confidence['issues']:
                    print(f"  Issues:")
                    for issue in confidence['issues']:
                        print(f"    ⚠️  {issue}")
                print()
                
                # Mostrar caso
                caso = result['caso']
                print("📝 CASO GENERADO:")
                print()
                print(f"ENUNCIADO:")
                print(caso['enunciado'])
                print()
                print(f"PREGUNTA:")
                print(caso['pregunta'])
                print()
                print(f"OPCIONES:")
                for key, value in caso['opciones'].items():
                    marker = "✓" if key == caso['respuesta_correcta'] else " "
                    print(f"  [{marker}] {key}) {value}")
                print()
                print(f"RESPUESTA CORRECTA: {caso['respuesta_correcta']}")
                print()
                print(f"EXPLICACIÓN:")
                print(caso['explicacion'])
                print()
                
                if 'articulos_aplicables' in caso:
                    print(f"ARTÍCULOS APLICABLES:")
                    for art in caso['articulos_aplicables']:
                        print(f"  - {art}")
                    print()
                
                print(f"DIFICULTAD: {caso.get('dificultad', 'N/A')}")
                print()
                
                # Status final
                print("=" * 80)
                print(f"STATUS: {result['status']}")
                print("=" * 80)
                
                # Guardar resultado
                output_file = "caso_generado_salamandra.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print()
                print(f"💾 Resultado guardado en: {output_file}")
                
            else:
                print(f"❌ ERROR: {response.status_code}")
                print(response.text)
                sys.exit(1)
    
    except httpx.ConnectError:
        print("❌ ERROR: No se pudo conectar al servidor")
        print("   Asegúrate de que el backend esté corriendo:")
        print("   cd backend && python main.py")
        sys.exit(1)
    
    except httpx.TimeoutException:
        print("❌ ERROR: Timeout esperando respuesta")
        print("   El servidor puede estar sobrecargado o Salamandra VPS no responde")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print()
    asyncio.run(test_generate_case())
    print()
