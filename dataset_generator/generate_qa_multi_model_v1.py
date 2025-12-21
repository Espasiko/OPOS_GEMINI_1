
import os
import time
import json
import logging
import requests
from datetime import datetime
from typing import List, Dict, Any

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de APIs (Cargadas desde .env de backend si es posible)
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

# Modelos seleccionados
MODELS = {
    "groq": "llama-3.3-70b-versatile",
    "deepseek": "deepseek-chat",
    "deepseek-reasoner": "deepseek-reasoner"
}

# Temas (Enfoque SS + AGE Diversidad)
TOPICS = [
    "La protección social de los trabajadores autónomos (RETA)",
    "Régimen Especial de la Minería del Carbón y del Mar",
    "Gestión Económico-Financiera de la Seguridad Social",
    "El presupuesto de la Seguridad Social: Elaboración y Ejecución",
    "Pensiones de Muerte y Supervivencia: Viudedad y Orfandad",
    "El Seguro Obligatorio de Vejez e Invalidez (SOVI)",
    "Asistencia Sanitaria: Competencias y Gestión",
    "Incapacidad Permanente: Grados y Prestaciones",
    "Lesiones Permanentes No Invalidantes",
    "Convenios Internacionales de Seguridad Social"
]

def buscar_rag(query: str, top_k: int = 5) -> str:
    """Herramienta RAG conectada al backend con Reranking"""
    try:
        resp = requests.post(f"{BACKEND_URL}/api/v2/rag/search", 
                             json={"query": query, "top_k": top_k, "apply_reranking": True},
                             timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            docs = data.get("documents", [])
            context = "\n\n".join([f"[DOC {i+1}] (Score: {d['score']:.2f}) {d['content']}" for i, d in enumerate(docs)])
            return context if context else "No se encontraron documentos."
        return f"Error en RAG: Status {resp.status_code}"
    except Exception as e:
        return f"Error conectando al RAG: {e}"

def verificar_url(articulo: str, ley: str) -> str:
    """Verifica si un artículo existe en la base de datos legal local"""
    query = f"{articulo} {ley}"
    try:
        resp = requests.post(f"{BACKEND_URL}/api/v2/rag/search", 
                             json={"query": query, "top_k": 1, "min_score": 0.1},
                             timeout=10)
        if resp.status_code == 200:
            docs = resp.json().get("documents", [])
            return f"VERIFICADO: {docs[0]['metadata'].get('norma_nombre', 'Ley')} Art {articulo}" if docs else "NO ENCONTRADO"
        return "ERROR DE VERIFICACIÓN"
    except Exception as e:
        return f"Error verificando: {e}"

# Definición de herramientas para OpenAI-Compatible APIs
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "buscar_rag",
            "description": "Busca legislación oficial y materiales de estudio en la base de datos local (RAG). Úsala para obtener el texto exacto de las leyes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Consulta de búsqueda legal (ej. 'artículo 14 constitución')"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "verificar_url",
            "description": "Verifica si una referencia legal específica (artículo y ley) existe realmente en la base de datos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "articulo": {"type": "string", "description": "Número de artículo"},
                    "ley": {"type": "string", "description": "Nombre de la ley o norma"}
                },
                "required": ["articulo", "ley"]
            }
        }
    }
]

def generate_with_agent(provider: str, topic: str, count: int = 10):
    """Lógica de agente genérica para Groq/DeepSeek"""
    api_key = GROQ_API_KEY if provider == "groq" else DEEPSEEK_API_KEY
    base_url = "https://api.groq.com/openai/v1" if provider == "groq" else "https://api.deepseek.com/v1"
    model = MODELS[provider]

    if not api_key:
        logger.error(f"❌ API Key para {provider} no configurada.")
        return []

    prompt = f"""
    Eres un experto en oposiciones de España (AGE y Seguridad Social).
    Genera {count} preguntas de NIVEL EXPERTO sobre el tema: '{topic}'.
    
    OBJETIVO: Crear un dataset diversificado y veraz.
    
    ESTRUCTURA OBLIGATORIA DEL BATCH (Mezcla estos tipos):
    - TEST (Normal)
    - COMPARACIÓN (Conceptos legales)
    - PROCEDIMIENTO (Trámites administrativos)
    - RAZONAMIENTO JURÍDICO (Caso práctico breve)
    - RELACIÓN (Vínculo entre normas/órganos)

    INSTRUCCIONES TÉCNICAS:
    1. Usa la herramienta 'buscar_rag(query="{topic}")' para obtener la base legal real. No inventes artículos.
    2. Usa 'verificar_url(articulo="...", ley="...")' para confirmar cada referencia antes de escribirla.
    3. Tu respuesta final DEBE SER ÚNICAMENTE UN ARRAY JSON VÁLIDO.
    
    FORMATO JSON (ESTRICTO):
    [
      {{
        "pregunta": "texto de la pregunta",
        "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "respuesta_correcta": "A/B/C/D",
        "explicacion": "Explicación detallada citando el artículo exacto.",
        "referencias": ["Art. X de la Ley Y"],
        "tema": "{topic}",
        "tipo": "RAZONAMIENTO/TEST/COMPARACION/PROCEDIMIENTO/RELACION"
      }}
    ]
    NO incluyas texto fuera del JSON (ni ```json, ni explicaciones adicionales).
    """

    messages = [{"role": "user", "content": prompt}]
    
    try:
        # 1. Llamada inicial
        resp = requests.post(f"{base_url}/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json={
            "model": model,
            "messages": messages,
            "tools": TOOLS,
            "tool_choice": "auto"
        }, timeout=60)
        
        data = resp.json()
        if "choices" not in data:
            logger.error(f"❌ Error API ({provider}). Response: {data}")
            return None
            
        choice = data["choices"][0]
        if "message" not in choice:
            logger.error(f"❌ No message in choice: {choice}")
            return None
            
        logger.info(f"   [{provider}] Initial response received. Content length: {len(choice['message'].get('content', '') or '')}")
        
        # 2. Manejo de Tool Calls
        while choice["message"].get("tool_calls"):
            tool_calls = choice["message"]["tool_calls"]
            logger.info(f"   [{provider}] Tool Calls detected: {len(tool_calls)}")
            messages.append(choice["message"])
            
            for tool_call in tool_calls:
                func_name = tool_call["function"]["name"]
                args = json.loads(tool_call["function"]["arguments"])
                
                if func_name == "buscar_rag":
                    result = buscar_rag(args["query"])
                elif func_name == "verificar_url":
                    result = verificar_url(args["articulo"], args["ley"])
                else:
                    result = "Error: Función desconocida"
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": func_name,
                    "content": result
                })
            
            # Re-prolongar conversación (IMPORTANTE: enviar tools de nuevo si el modelo lo requiere)
            resp = requests.post(f"{base_url}/chat/completions", 
                                 headers={"Authorization": f"Bearer {api_key}"}, 
                                 json={
                                    "model": model,
                                    "messages": messages,
                                    "tools": TOOLS,
                                    "tool_choice": "auto"
                                 }, timeout=60)
            data = resp.json()
            if "choices" not in data:
                logger.error(f"❌ Error API ({provider}) en loop Herramientas: {data}")
                return None
            choice = data["choices"][0]
            logger.info(f"   [{provider}] Next response received. Content length: {len(choice['message'].get('content', '') or '')}")

        # 3. Extraer contenido final
        content = choice["message"]["content"]
        return content
    except Exception as e:
        logger.error(f"Error en {provider}: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    provider = sys.argv[1] if len(sys.argv) > 1 else "groq"
    output_dir = "dataset_generator/multi_model_20_12"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/qa_{provider}_master_100.jsonl"
    
    print(f"🚀 Iniciando Generación Masiva con {provider.upper()}...")
    print(f"📁 Salida: {output_file}")
    
    total_generated = 0
    for i, topic in enumerate(TOPICS * 10): # 10 topics x 10 items each = 100
        if total_generated >= 100: break
        
        logger.info(f"🔄 Processing Batch {total_generated//10 + 1}/10: {topic}")
        result_json = generate_with_agent(provider, topic, 10)
        
        if result_json:
            try:
                # Limpiar Markdown si existe
                clean_json = result_json.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)
                
                with open(output_file, "a", encoding="utf-8") as f:
                    for item in data:
                        item["model_provider"] = provider
                        item["timestamp"] = datetime.now().isoformat()
                        f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
                total_generated += len(data)
                logger.info(f"✅ {len(data)} items guardados. Total: {total_generated}")
                
                # Pausa entre batches para evitar Rate Limits
                time.sleep(15)
            except Exception as e:
                logger.error(f"❌ Error parseando JSON en batch {i}: {e}")
                time.sleep(5)
        else:
            logger.error(f"⚠️ Batch {i} falló.")
            time.sleep(10)

    print(f"\n✨ Generación Finalizada: {total_generated} items en {output_file}")
