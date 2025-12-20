#!/usr/bin/env python3
"""
Generador de 10 Q&A usando Mistral Agent Studio
CON MANEJO CORRECTO DE TOOL_CALLS según docs oficiales
"""

import os
import json
from datetime import datetime
from mistralai import Mistral

# Configuración
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"

# Temas para generar Q&A (3 TEST, 2 COMPARACIÓN, 2 PROCEDIMIENTO, 1 RAZONAMIENTO, 2 RELACIÓN)
TEMAS = [
    {"tipo": "test", "tema": "incapacidad temporal duración máxima"},
    {"tipo": "test", "tema": "jubilación ordinaria requisitos 2024"},
    {"tipo": "test", "tema": "prestación desempleo cuantía"},
    {"tipo": "comparacion", "tema": "incapacidad permanente parcial vs total"},
    {"tipo": "comparacion", "tema": "moción de censura vs cuestión de confianza"},
    {"tipo": "procedimiento", "tema": "solicitar pensión jubilación pasos"},
    {"tipo": "procedimiento", "tema": "tramitación recurso de alzada"},
    {"tipo": "razonamiento", "tema": "trabajador IT supera 365 días qué pasa"},
    {"tipo": "relacion", "tema": "LGSS y Constitución derechos sociales"},
    {"tipo": "relacion", "tema": "Ley 39/2015 y LGSS procedimiento administrativo"}
]

def ejecutar_tool_call(tool_call):
    """Simula la ejecución de una tool call"""
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    print(f"      🔧 Tool call: {function_name}({arguments})")
    
    # Simular respuesta de la herramienta
    # En producción, aquí llamarías a tu backend/MCP
    if function_name == "buscar_rag":
        return json.dumps({
            "results": [
                {"text": "Contexto legal relevante de Qdrant y PostgreSQL", "score": 0.85}
            ]
        })
    elif function_name == "verificar_url":
        return json.dumps({"verified": True, "source": "Qdrant+BD"})
    else:
        return json.dumps({"status": "ok"})

def generar_qa(client, tema_info):
    """Genera una Q&A usando el agente Mistral Studio con manejo de tool_calls"""
    tipo = tema_info["tipo"]
    tema = tema_info["tema"]
    
    # Prompt adaptado al tipo
    prompt = f"""Genera UNA pregunta tipo {tipo} sobre: {tema}

Formato JSON:
{{
  "pregunta": "...",
  "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "respuesta_correcta": "A",
  "explicacion": "...",
  "referencias": ["art. X Ley Y"]
}}

IMPORTANTE: Devuelve SOLO el JSON, sin texto adicional."""
    
    try:
        print(f"   📤 Llamando al agente...")
        
        # Mensajes iniciales
        messages = [{
            "role": "user",
            "content": prompt
        }]
        
        # Llamar al agente
        response = client.agents.complete(
            agent_id=AGENT_ID,
            messages=messages
        )
        
        # Loop para manejar tool_calls (según docs oficiales)
        max_iterations = 5
        iteration = 0
        
        while response.choices[0].message.tool_calls and iteration < max_iterations:
            iteration += 1
            print(f"      🔄 Iteración {iteration}: Procesando tool_calls...")
            
            # Añadir mensaje del asistente con tool_calls
            messages.append(response.choices[0].message)
            
            # Ejecutar cada tool_call
            for tool_call in response.choices[0].message.tool_calls:
                result = ejecutar_tool_call(tool_call)
                
                # Añadir resultado de la tool
                messages.append({
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": result,
                    "tool_call_id": tool_call.id
                })
            
            # Llamar al agente de nuevo con los resultados
            response = client.agents.complete(
                agent_id=AGENT_ID,
                messages=messages
            )
        
        # Extraer respuesta final
        content = response.choices[0].message.content
        
        if not content or content.strip() == "":
            print(f"   ⚠️  Respuesta vacía después de {iteration} iteraciones")
            return None
        
        print(f"   📥 Respuesta recibida (después de {iteration} iteraciones)")
        print(f"   📝 Contenido: {str(content)[:200]}...")
        
        # Intentar extraer JSON
        content_str = str(content)
        if "```json" in content_str:
            json_str = content_str.split("```json")[1].split("```")[0]
        elif "```" in content_str:
            json_str = content_str.split("```")[1].split("```")[0]
        elif "{" in content_str:
            start = content_str.find("{")
            end = content_str.rfind("}") + 1
            json_str = content_str[start:end]
        else:
            json_str = content_str
        
        qa = json.loads(json_str.strip())
        qa["tipo"] = tipo
        qa["generated_at"] = datetime.now().isoformat()
        qa["created_by"] = "mistral_agent_studio_v2"
        
        return qa
        
    except json.JSONDecodeError as e:
        print(f"   ❌ Error parseando JSON: {e}")
        print(f"   📄 Contenido: {content}")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("\n" + "="*70)
    print("GENERACIÓN DE 10 Q&A CON MISTRAL AGENT STUDIO V2")
    print("CON MANEJO DE TOOL_CALLS")
    print("="*70)
    print(f"\nAgent ID: {AGENT_ID}")
    
    client = Mistral(api_key=MISTRAL_API_KEY)
    qa_generadas = []
    
    for i, tema_info in enumerate(TEMAS, 1):
        tipo = tema_info["tipo"]
        tema = tema_info["tema"]
        
        print(f"\n{'─'*70}")
        print(f"[{i}/10] Tipo: {tipo.upper()}")
        print(f"       Tema: {tema}")
        print('─'*70)
        
        qa = generar_qa(client, tema_info)
        
        if qa:
            qa["id"] = f"MISTRAL-STUDIO-V2-{i:03d}"
            qa_generadas.append(qa)
            print(f"   ✅ Generada: {qa.get('pregunta', '')[:55]}...")
        else:
            print(f"   ❌ Error generando Q&A")
    
    # Guardar resultados
    if qa_generadas:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"qa_mistral_studio_v2_{timestamp}.jsonl"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for qa in qa_generadas:
                f.write(json.dumps(qa, ensure_ascii=False) + '\n')
        
        print("\n" + "="*70)
        print(f"✅ COMPLETADO: {len(qa_generadas)}/10 Q&A generadas")
        print("="*70)
        
        # Estadísticas
        from collections import Counter
        tipos_count = Counter(qa["tipo"] for qa in qa_generadas)
        print("\n📊 TIPOS GENERADOS:")
        for tipo, count in sorted(tipos_count.items()):
            print(f"   {tipo}: {count}")
        
        print(f"\n📁 Guardado en: {output_file}")
        
        # Mostrar muestra
        if qa_generadas:
            print("\n" + "="*70)
            print("📋 MUESTRA (primera pregunta):")
            print("="*70)
            print(json.dumps(qa_generadas[0], indent=2, ensure_ascii=False))
        
        return output_file
    else:
        print("\n❌ No se generaron Q&A")
        return None

if __name__ == "__main__":
    main()
