import sys
import os
import asyncio
import json
import logging

# Añadir el path del backend para imports relativos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import Orchestrator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_generation():
    print("\n" + "="*80)
    print("TEST DE GENERACIÓN DE PREGUNTAS COSMIC (DeepSeek R1 + Mistral Large)")
    print("="*80)
    
    orchestrator = Orchestrator()
    
    # Simular una consulta de usuario sobre la Ley 39/2015 (Plazos de Recurso)
    query = "Genera una pregunta difícil sobre los plazos del recurso de alzada en la Ley 39/2015"
    
    print(f"\n🚀 Procesando consulta: '{query}'...")
    
    try:
        # Llamar al flujo de generación
        result = await orchestrator.generate_exam_question(query)
        
        print("\n✅ PREGUNTA GENERADA:")
        print("-" * 40)
        print(f"ENUNCIADO: {result.get('enunciado')}")
        print("\nOPCIONES:")
        for k, v in result.get('opciones', {}).items():
            print(f"  {k}) {v}")
        
        print(f"\nRESPUESTA CORRECTA: {result.get('respuesta_correcta').upper()}")
        print(f"JUSTIFICACIÓN: {result.get('justificacion')}")
        
        print("\n🧠 LÓGICA DE LA TRAMPA (COSMIC TRAP):")
        print(result.get('logica_trampa'))
        
        print("\n⚖️ VALIDACIÓN JURÍDICA (Mistral Large):")
        validacion = result.get('validacion', {})
        status = "✅ VÁLIDA" if validacion.get('valido') else "❌ ERROR"
        print(f"STATUS: {status}")
        print(f"COMENTARIOS: {validacion.get('comentarios')}")
        
    except Exception as e:
        logger.error(f"❌ Error en el test: {str(e)}")
        if 'raw' in locals() or 'result' in locals():
            print(f"Debug Raw: {result}")

if __name__ == "__main__":
    asyncio.run(test_generation())
