
import os
import time
import json
import logging
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from mistralai import Mistral # Correct SDK usage
from mistralai.models import UserMessage, ToolMessage, AssistantMessage

# Load env from backend config
load_dotenv("backend/.env.backend")

# --- CONFIG ---
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
AGENT_ID = "ag_019ad601946d7323a81c544229de40a1" 
BACKEND_URL = "http://127.0.0.1:8000"
OUTPUT_DIR = "dataset_generator/premium_content/mistral_extreme"
MAX_RETRIES = 3

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY env var not set")

os.makedirs(OUTPUT_DIR, exist_ok=True)

METHODS = [
    "Jubilación Anticipada por Discapacidad 45% vs 65%",
    "Complemento de Brecha de Género: Criterios hombres y concurrencia",
    "Incapacidad Permanente: Revisión por mejoría y efectos en compatibilidad laboral",
    "Desempleo: Pago Único y Mantenimiento de Actividad (Criterios SEPE vs Hacienda)",
    "Ingreso Mínimo Vital: Unidad de Convivencia Compleja y Rentas Exentas",
    "Recargo de Prestaciones: Responsabilidad Solidaria, Sucesión y Aseguramiento",
    "Régimen del Mar: Coeficientes Reductores en Pesca de Altura",
    "Convenios Internacionales: Totalización y Prorrata (Bilaterales vs UE)",
    "Viudedad: Parejas de Hecho y Pensión Compensatoria",
    "Jubilación Activa vs Flexible: Cotización y Requisitos Autónomos"
]

def ejecutar_tool_call_real(tool_call):
    """Ejecuta tool_call llamando al backend REAL (Qdrant + PostgreSQL)"""
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    logger.info(f"   🔧 Ejecutando Tool: {function_name}({arguments})")
    
    try:
        if function_name == "buscar_rag":
            response = requests.post(
                f"{BACKEND_URL}/api/rag/search",
                json={
                    "query": arguments.get("query", ""),
                    "top_k": arguments.get("top_k", 5),
                    "min_score": 0.1
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"      ✅ RAG: {len(data.get('documents', []))} resultados")
                return json.dumps(data, ensure_ascii=False)
            else:
                logger.error(f"      ⚠️  RAG error: {response.status_code}")
                return json.dumps({"error": f"RAG error: {response.status_code}"})
                
        elif function_name == "verificar_url":
           return json.dumps({"status": "ok", "message": "Simulated URL check ok"})

        else:
            return json.dumps({"status": "error", "message": f"Function {function_name} not implemented"})
    
    except Exception as e:
        logger.error(f"      ❌ Error ejecutando {function_name}: {e}")
        return json.dumps({"error": str(e)})

def generate_mistral_case(client: Mistral, topic: str) -> Optional[Dict[str, Any]]:
    prompt = f"""
    Genera un CASO PRÁCTICO EXTREMO sobre: {topic}.

    INSTRUCCIONES CLAVE:
    1. USA la herramienta 'buscar_rag' para encontrar detalles legales precisos (artículos, plazos, excepciones).
    2. Piensa paso a paso sobre la normativa encontrada.
    3. Genera el JSON final con 15 preguntas EXTREMAS.
    
    ESTRUCTURA JSON:
    {{
      "topic": "{topic}",
      "scenario": "...",
      "questions": [
        {{ "id": "q1", "question": "...", "options": [ ... ], "correct_option_id": "a", "explanation": "..." }}
      ]
    }}
    """
    
    messages = [UserMessage(content=prompt)]

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Generating case for '{topic}' (Attempt {attempt+1})...")
            
            # 1. Initial Call
            response = client.agents.complete(
                agent_id=AGENT_ID,
                messages=messages
            )
            
            # 2. Tool Loop
            max_loops = 5
            loop = 0
            
            while response.choices[0].message.tool_calls and loop < max_loops:
                loop += 1
                logger.info(f"   🔄 Loop {loop}: Processing Tool Calls...")
                
                # Append Assistant Message with Tool Calls
                messages.append(response.choices[0].message)
                
                for tool_call in response.choices[0].message.tool_calls:
                    tool_result = ejecutar_tool_call_real(tool_call)
                    
                    messages.append(ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_call.id,
                        name=tool_call.function.name
                    ))
                
                # Call Agent again with tool results
                response = client.agents.complete(
                    agent_id=AGENT_ID,
                    messages=messages
                )

            # 3. Final Content
            content = response.choices[0].message.content
            
            # Clean JSON
            json_str = str(content)
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]
            
            if json_str.strip().startswith("Here is") or json_str.strip().startswith("Vale"):
                 start = json_str.find("{")
                 end = json_str.rfind("}") + 1
                 if start >= 0: json_str = json_str[start:end]

            case_data = json.loads(json_str.strip())
            return case_data

        except Exception as e:
            logger.error(f"Error Mistral SDK: {e}")
            time.sleep(10)
            
    return None

def main():
    logger.info(f"Starting Tool-Enabled Mistral Generation...")
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    for i, topic in enumerate(METHODS):
        filename = f"{OUTPUT_DIR}/case_extreme_mistral_v{i+1}.json"
        if os.path.exists(filename): continue
            
        case_data = generate_mistral_case(client, topic)
        
        if case_data:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(case_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved: {filename}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()
