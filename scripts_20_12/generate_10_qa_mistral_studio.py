#!/usr/bin/env python3
"""
Generador de 10 Q&A usando Mistral Agent Studio
El agente YA tiene configurado:
- System Prompt en Mistral Studio
- Funciones: buscar_rag (Qdrant + PostgreSQL), verificar_url (Qdrant + BD)
- MCP integrado (search_rag, list_collections)
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

def generar_qa(client, tema_info):
    """Genera una Q&A usando el agente Mistral Studio"""
    tipo = tema_info["tipo"]
    tema = tema_info["tema"]
    
    # Prompt adaptado al tipo
    if tipo == "test":
        prompt = f"""Genera UNA pregunta tipo test sobre: {tema}

Formato JSON:
{{
  "pregunta": "...",
  "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "respuesta_correcta": "A",
  "explicacion": "...",
  "referencias": ["art. X Ley Y"]
}}

Usa tu función buscar_rag para obtener contexto legal preciso de Qdrant y PostgreSQL.
Verifica la respuesta automáticamente en la BD."""
    
    elif tipo == "comparacion":
        prompt = f"""Genera UNA pregunta que compare: {tema}

Formato JSON con pregunta que pida comparar diferencias clave.
Usa buscar_rag para obtener info de ambos conceptos de Qdrant y BD.
Verifica automáticamente."""
    
    elif tipo == "procedimiento":
        prompt = f"""Genera UNA pregunta sobre el procedimiento: {tema}

Formato JSON con pregunta sobre los pasos del procedimiento.
Usa buscar_rag para obtener el procedimiento oficial de Qdrant y BD.
Verifica automáticamente."""
    
    elif tipo == "razonamiento":
        prompt = f"""Genera UN caso práctico: {tema}

Formato JSON con caso práctico que requiera razonamiento legal.
Usa buscar_rag para obtener la normativa aplicable de Qdrant y BD.
Verifica automáticamente."""
    
    else:  # relacion
        prompt = f"""Genera UNA pregunta sobre la relación entre: {tema}

Formato JSON con pregunta sobre cómo se relacionan.
Usa buscar_rag para obtener info de ambas fuentes de Qdrant y BD.
Verifica automáticamente."""
    
    try:
        print(f"   📤 Llamando al agente...")
        
        # Llamar al agente (ÉL maneja las tool_calls automáticamente)
        response = client.agents.complete(
            agent_id=AGENT_ID,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extraer respuesta
        content = response.choices[0].message.content
        
        print(f"   📥 Respuesta recibida")
        print(f"   📝 Contenido (primeros 200 chars): {str(content)[:200]}...")
        
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
        qa["created_by"] = "mistral_agent_studio"
        
        return qa
        
    except json.JSONDecodeError as e:
        print(f"   ❌ Error parseando JSON: {e}")
        print(f"   📄 Contenido completo: {content}")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("\n" + "="*70)
    print("GENERACIÓN DE 10 Q&A CON MISTRAL AGENT STUDIO")
    print("="*70)
    print(f"\nAgent ID: {AGENT_ID}")
    print(f"Funciones: buscar_rag (Qdrant+PostgreSQL), verificar_url (Qdrant+BD)")
    print(f"MCP Tools: search_rag, list_collections")
    
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
            qa["id"] = f"MISTRAL-STUDIO-{i:03d}"
            qa_generadas.append(qa)
            print(f"   ✅ Generada: {qa.get('pregunta', '')[:55]}...")
        else:
            print(f"   ❌ Error generando Q&A")
    
    # Guardar resultados
    if qa_generadas:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"qa_mistral_studio_{timestamp}.jsonl"
        
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
