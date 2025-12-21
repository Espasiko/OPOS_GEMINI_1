
import os
import time
import json
import logging
import requests
from datetime import datetime
from typing import List, Dict, Any
from verify_boe_links import verify_on_boe

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de APIs
def load_env_vars():
    env_path = "backend/.env.backend"
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)
        logger.info(f"✅ Variables cargadas desde {env_path}")

load_env_vars()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
BACKEND_URL = "http://127.0.0.1:8000"

# Modelos Avanzados Seleccionados
MODELS = {
    "groq_fast": "llama-3.3-70b-versatile",
    "deepseek_reasoner": "deepseek-reasoner", # DeepSeek R1 / V3.2 Speciale (según alias API)
    "deepseek_v3_2": "deepseek-chat",        # DeepSeek V3.2 (según alias API)
    "deepseek_speciale": "deepseek-reasoner", # Alias para razonamiento superior
    "deepseek_chat": "deepseek-chat"
}

# Temas (Cobertura Total 26 temas)
TOPICS = [
    "La protección social de los trabajadores autónomos (RETA)",
    "Régimen Especial de la Minería del Carbón y del Mar",
    "Pensión de Jubilación: Requisitos, Cuantía y Modalidades",
    "Incapacidad Temporal: Concepto, Duración y Subsidio",
    "El presupuesto de la Seguridad Social: Elaboración y Ejecución",
    "Ingreso Mínimo Vital: Requisitos y Beneficiarios",
    "La Corona: Sucesión, Regencia y Funciones del Rey",
    "Las Cortes Generales: Composición y atribuciones",
    "Políticas de Igualdad y Violencia de Género",
    "Derechos y Deberes Fundamentales",
    "El Gobierno y la Administración",
    "Organización Territorial del Estado",
    "El Acto Administrativo: Concepto y Clases",
    "El Procedimiento Administrativo Común",
    "Contratos del Sector Público: Clasificación",
    "El Personal al Servicio de las Administraciones Públicas",
    "Gestión Económico-Financiera de la SS",
    "Pensiones de Muerte y Supervivencia",
    "El Seguro Obligatorio de Vejez e Invalidez (SOVI)",
    "Asistencia Sanitaria: Competencias y Gestión",
    "Incapacidad Permanente: Grados",
    "Lesiones Permanentes No Invalidantes",
    "Convenios Internacionales de SS",
    "Protección por Desempleo",
    "Servicios Sociales: El IMSERSO",
    "Infracciones y Sanciones en el Orden Social"
]

def buscar_rag(query: str, top_k: int = 5) -> str:
    """RAG con Reranking para contexto legal preciso"""
    try:
        resp = requests.post(f"{BACKEND_URL}/api/v2/rag/search", 
                             json={"query": query, "top_k": top_k, "apply_reranking": True},
                             timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            docs = data.get("documents", [])
            context = "\n\n".join([f"[DOC {i+1}] (Score: {d['score']:.2f}) {d['content']}" for i, d in enumerate(docs)])
            return context if context else "No se encontraron documentos relevantes."
        return f"Error en RAG: Status {resp.status_code}"
    except Exception as e:
        return f"Error en RAG: {e}"

def verificar_referencia(articulo: str, ley: str) -> str:
    """Doble verificación: Local (RAG) + Externa (BOE)"""
    # 1. Verificación local
    query = f"{articulo} {ley}"
    local_found = False
    try:
        resp = requests.post(f"{BACKEND_URL}/api/v2/rag/search", json={"query": query, "top_k": 1}, timeout=5)
        if resp.status_code == 200 and resp.json().get("documents"):
            local_found = True
    except: pass

    # 2. Verificación externa (BOE Real)
    boe_res = verify_on_boe(articulo, ley)
    
    status = "✅ VERIFICADO (DB + BOE)" if (local_found and boe_res["valid"]) else \
             "⚠️ VERIFICADO (Sólo BOE)" if boe_res["valid"] else \
             "❌ NO ENCONTRADO EN BOE"
             
    message = f"{status}. {boe_res.get('message', '')}"
    if boe_res.get("url"):
        message += f" Link: {boe_res['url']}"
    return message

# Herramientas (TOOLS) - Formato OpenAI
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "buscar_rag",
            "description": "Obtiene legislación oficial y materiales de estudio actualizados. Úsala SIEMPRE antes de responder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Consulta legal detallada"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "verificar_referencia",
            "description": "Valida si un artículo existe realmente en la base de datos local y en la web del BOE.",
            "parameters": {
                "type": "object",
                "properties": {
                    "articulo": {"type": "string", "description": "Número de artículo"},
                    "ley": {"type": "string", "description": "Nombre de la ley"}
                },
                "required": ["articulo", "ley"]
            }
        }
    }
]

def run_agent_v2(provider_key: str, model_id: str, topic: str, count: int = 10):
    """
    Agente optimizado para Groq Prompt Caching y Native DeepSeek CoT.
    """
    api_key = GROQ_API_KEY if "groq" in provider_key else DEEPSEEK_API_KEY
    base_url = "https://api.groq.com/openai/v1" if "groq" in provider_key else "https://api.deepseek.com/v1"

    # Caso especial para DeepSeek Reasoner (CoT Native)
    is_reasoner = (model_id == "deepseek-reasoner")

    if not api_key:
        logger.error(f"❌ API Key no encontrada para {provider_key}")
        return None

    # ESTRUCTURA PARA PROMPT CACHING (GROQ):
    # 1. System Prompt (Estático)
    # 2. Tool Definitions (Estático)
    # 3. User query (Dinámico)
    
    system_prompt = f"""
    Eres un experto en oposiciones de Seguridad Social de España. 
    Tu objetivo es generar un dataset de alta precisión legal para entrenamiento de IA.
    
    REGLAS DE ORO:
    1. PROHIBIDO ALUCINAR: Si no encuentras el dato exacto con 'buscar_rag', di que no lo sabes.
    2. REFERENCIAS REALES: Usa 'verificar_referencia' para cada artículo citado.
    3. FORMATO: Responde SIEMPRE en un ARRAY JSON puro.
    
    Genera {count} preguntas sobre: '{topic}'.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Inicia la generación para el tema: {topic}"}
    ]

    try:
        # Llamada inicial
        r = requests.post(f"{base_url}/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json={
            "model": model_id,
            "messages": messages,
            "tools": TOOLS,
            "tool_choice": "auto",
            "temperature": 0.1 # Menor temperatura para mayor precisión legal
        }, timeout=120)
        
        data = r.json()
        if "choices" not in data:
            logger.error(f"Error API: {data}")
            return None
            
        choice = data["choices"][0]
        
        # Guardar razonamiento si existe (DeepSeek Native)
        reasoning = choice["message"].get("reasoning_content", "")
        if reasoning:
            logger.info(f"🧠 Reasoning Content Capturado ({len(reasoning)} chars)")
        
        while choice["message"].get("tool_calls"):
            tool_calls = choice["message"]["tool_calls"]
            messages.append(choice["message"])
            
            for call in tool_calls:
                func_name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"])
                logger.info(f"🛠️ Tool Call: {func_name}({args})")
                
                if func_name == "buscar_rag":
                    result = buscar_rag(args["query"])
                elif func_name == "verificar_referencia":
                    result = verificar_referencia(args["articulo"], args["ley"])
                else:
                    result = "Error: Función desconocida"

                messages.append({
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "name": func_name,
                    "content": result
                })

            # Siguiente turno de conversación
            r = requests.post(f"{base_url}/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json={
                "model": model_id,
                "messages": messages,
                "tools": TOOLS
            }, timeout=120)
            data = r.json()
            choice = data["choices"][0]

        # 3. Extraer contenido final
        content = choice["message"]["content"]
        return {
            "content": content,
            "reasoning": reasoning
        }
    except Exception as e:
        logger.error(f"Error en ejecución del agente: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    provider = sys.argv[1] if len(sys.argv) > 1 else "deepseek"
    model_key = sys.argv[2] if len(sys.argv) > 2 else "deepseek_reasoner"
    
    output_dir = "dataset_generator/multi_model_v3_2_20_12"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/qa_{model_key}_master_500.jsonl"
    
    print(f"🚀 Iniciando Generación Masiva (V3.2/R1 compatible) con {model_key}...")
    print(f"📁 Salida: {output_file}")
    
    total_generated = 0
    batch_size = 10
    total_target = 500
    
    # Loop de generación masiva
    while total_generated < total_target:
        topic = TOPICS[ (total_generated // batch_size) % len(TOPICS) ]
        batch_num = (total_generated // batch_size) + 1
        
        logger.info(f"🔄 Processing Batch {batch_num}/50: {topic}")
        resp = run_agent_v2(provider, MODELS[model_key], topic, batch_size)
        
        if resp and resp.get("content"):
            try:
                # Limpiar Markdown si existe
                clean_json = resp["content"].replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)
                
                with open(output_file, "a", encoding="utf-8") as f:
                    for item in data:
                        item["model_provider"] = f"{provider}_{model_key}"
                        item["reasoning_chain"] = resp.get("reasoning", "")
                        item["timestamp"] = datetime.now().isoformat()
                        f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
                total_generated += len(data)
                logger.info(f"✅ {len(data)} items guardados en batch {batch_num}. Total: {total_generated}")
                
                # Pausa estratégica para estabilidad de API
                time.sleep(10)
            except Exception as e:
                logger.error(f"❌ Error parseando JSON en batch {batch_num}: {e}")
                time.sleep(5)
        else:
            logger.error(f"⚠️ Batch {batch_num} falló o devolvió vacío.")
            time.sleep(15)

    print(f"\n✨ Generación Masiva Finalizada: {total_generated} items en {output_file}")
