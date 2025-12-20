#!/usr/bin/env python3
"""
Generador de Q&A con Mistral Agent Studio
CONECTADO A BACKEND REAL (Qdrant + PostgreSQL)
"""

import os
import json
import requests
from datetime import datetime
from mistralai import Mistral

# Configuración
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("❌ MISTRAL_API_KEY no encontrada en variables de entorno")
AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"
BACKEND_URL = "http://127.0.0.1:8000"  # FastAPI corriendo

# Temas (3 TEST, 2 COMPARACIÓN, 2 PROCEDIMIENTO, 1 RAZONAMIENTO, 2 RELACIÓN)
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

def ejecutar_tool_call_real(tool_call):
    """Ejecuta tool_call llamando al backend REAL (Qdrant + PostgreSQL)"""
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    print(f"      🔧 Ejecutando: {function_name}({arguments})")
    
    try:
        if function_name == "buscar_rag":
            # Llamar a tu endpoint RAG REAL
            response = requests.post(
                f"{BACKEND_URL}/api/rag/search",
                json={
                    "query": arguments.get("query", ""),
                    "top_k": arguments.get("top_k", 5),
                    "min_score": 0.1
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"      ✅ RAG: {len(data.get('documents', []))} resultados de Qdrant+PostgreSQL")
                return json.dumps(data, ensure_ascii=False)
            else:
                print(f"      ⚠️  RAG error: {response.status_code}")
                return json.dumps({"error": f"RAG error: {response.status_code}"})
        
        elif function_name == "verificar_url":
            # Verificar en BD local (Qdrant + PostgreSQL)
            articulo = arguments.get("articulo", "")
            ley = arguments.get("ley", "")
            
            # Buscar el artículo en RAG
            response = requests.post(
                f"{BACKEND_URL}/api/rag/search",
                json={
                    "query": f"artículo {articulo} {ley}",
                    "top_k": 3,
                    "min_score": 0.3
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                exists = len(data.get('documents', [])) > 0
                print(f"      ✅ Verificación: Art. {articulo} {ley} {'encontrado' if exists else 'no encontrado'}")
                return json.dumps({
                    "exists": exists,
                    "articulo": articulo,
                    "ley": ley,
                    "results": data.get('documents', [])[:1]  # Solo el mejor resultado
                }, ensure_ascii=False)
            else:
                return json.dumps({"exists": False, "error": "Verificación falló"})
        
        else:
            return json.dumps({"status": "ok", "message": f"Función {function_name} no implementada"})
    
    except Exception as e:
        print(f"      ❌ Error ejecutando {function_name}: {e}")
        return json.dumps({"error": str(e)})

def generar_qa_real(client, tema_info):
    """Genera Q&A usando el agente con backend REAL"""
    tipo = tema_info["tipo"]
    tema = tema_info["tema"]
    
    prompt = f"Genera una pregunta tipo {tipo.upper()} sobre: {tema}"
    
    try:
        print(f"   📤 Llamando al agente...")
        
        messages = [{"role": "user", "content": prompt}]
        
        # Llamar al agente
        response = client.agents.complete(
            agent_id=AGENT_ID,
            messages=messages
        )
        
        # Loop para manejar tool_calls con backend REAL
        max_iterations = 5
        iteration = 0
        
        while response.choices[0].message.tool_calls and iteration < max_iterations:
            iteration += 1
            print(f"      🔄 Iteración {iteration}: {len(response.choices[0].message.tool_calls)} tool_calls")
            
            # Añadir mensaje del asistente
            messages.append(response.choices[0].message)
            
            # Ejecutar cada tool_call con backend REAL
            for tool_call in response.choices[0].message.tool_calls:
                result = ejecutar_tool_call_real(tool_call)  # ← BACKEND REAL
                
                messages.append({
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": result,
                    "tool_call_id": tool_call.id
                })
            
            # Llamar al agente de nuevo
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
        
        # Extraer JSON
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
        qa["created_by"] = "mistral_agent_real_backend"
        
        return qa
        
    except json.JSONDecodeError as e:
        print(f"   ❌ Error parseando JSON: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("\n" + "="*70)
    print("GENERACIÓN CON MISTRAL AGENT + BACKEND REAL")
    print("Qdrant (17,403 puntos) + PostgreSQL (10,901 leyes)")
    print("="*70)
    print(f"\nAgent ID: {AGENT_ID}")
    print(f"Backend: {BACKEND_URL}")
    
    # Verificar que el backend está corriendo
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        print(f"✅ Backend: {response.status_code}")
    except:
        print(f"⚠️  Backend no responde en {BACKEND_URL}")
        print("   Asegúrate de que FastAPI está corriendo:")
        print("   cd backend && source .venv/bin/activate && uvicorn main:app")
        return
    
    client = Mistral(api_key=MISTRAL_API_KEY)
    qa_generadas = []
    
    for i, tema_info in enumerate(TEMAS, 1):
        tipo = tema_info["tipo"]
        tema = tema_info["tema"]
        
        print(f"\n{'─'*70}")
        print(f"[{i}/10] Tipo: {tipo.upper()}")
        print(f"       Tema: {tema}")
        print('─'*70)
        
        qa = generar_qa_real(client, tema_info)
        
        if qa:
            qa["id"] = f"MISTRAL-REAL-{i:03d}"
            qa_generadas.append(qa)
            print(f"   ✅ Generada: {qa.get('pregunta', '')[:55]}...")
        else:
            print(f"   ❌ Error generando Q&A")
    
    # Guardar resultados
    if qa_generadas:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"qa_mistral_real_backend_{timestamp}.jsonl"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for qa in qa_generadas:
                f.write(json.dumps(qa, ensure_ascii=False) + '\n')
        
        print("\n" + "="*70)
        print(f"✅ COMPLETADO: {len(qa_generadas)}/10 Q&A generadas")
        print("="*70)
        
        from collections import Counter
        tipos_count = Counter(qa["tipo"] for qa in qa_generadas)
        print("\n📊 TIPOS GENERADOS:")
        for tipo, count in sorted(tipos_count.items()):
            print(f"   {tipo}: {count}")
        
        print(f"\n📁 Guardado en: {output_file}")
        
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
