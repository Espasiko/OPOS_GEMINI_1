
import os
import time
import json
import logging
import asyncio
import glob
import requests
from mistralai import Mistral
# from backend.agents.rag_agent_v2 import get_rag_agent_v2 # REMOVED: Use HTTP
import psycopg2

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración - HARDCODED KEY VALIDADA
API_KEY = "xeE9w6vpnlANxBU9T90sC62zQnM0AYhZ"
AGENT_ID = "ag_019ad601946d7323a81c544229de40a1"

BATCH_SIZE = 10
TOTAL_BATCHES = 26 # Cobertura total + Igualdad (26 temas)
PAUSE_SECONDS = 20 # Pausa segura para evitar 429
DATA_DIR = "dataset_generator/qa_mistral_batches_20_12"
BACKEND_URL = "http://127.0.0.1:8000"

# Inicializar cliente Mistral
client = Mistral(api_key=API_KEY)

def get_law_context():
    """Obtiene el mapa de leyes disponibles de PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            database=os.getenv("POSTGRES_DB", "opositaia"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres")
        )
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT law_name FROM laws ORDER BY law_name LIMIT 100")
        laws = [l[0] for l in cur.fetchall()]
        cur.close()
        conn.close()
        return ", ".join(laws)
    except Exception:
        return "Constitución Española, Estatuto de los Trabajadores, LGSS, Ley 39/2015"

async def buscar_rag(query: str, top_k: int = 5, layer_filter: int = None) -> str:
    logger.info(f"🔎 BUSCAR_RAG (HTTP): '{query}'")
    try:
        # Use HTTP Request to Backend
        payload = {
            "query": query,
            "top_k": top_k,
            "min_score": 0.1 # Bajo score para asegurar resultados
        }
        if layer_filter:
            payload["layer_filter"] = layer_filter
            
        resp = requests.post(f"{BACKEND_URL}/api/rag/search", json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        docs = data.get('documents', [])
        if not docs:
            return "No se encontraron documentos relevantes en el RAG."
            
        docs_text = "\n\n".join([f"[DOC {i+1}] {d.get('content','')}..." for i, d in enumerate(docs)])
        return f"Documentos encontrados ({len(docs)}):\n{docs_text}"
        
    except Exception as e:
        return f"Error en RAG (HTTP): {e}"

async def verificar_url(articulo: str, ley: str) -> str:
    query = f"{articulo} {ley}".strip()
    logger.info(f"🛡️ VERIFICAR_FUENTE (HTTP): '{query}'")
    try:
         # Reutilizamos search endpoint para verificación
        payload = {
            "query": query,
            "top_k": 1,
            "min_score": 0.1
        }
        resp = requests.post(f"{BACKEND_URL}/api/rag/search", json=payload, timeout=10)
        data = resp.json() if resp.status_code == 200 else {}
        docs = data.get('documents', [])
        
        if docs:
             return f"VERIFICADO: Existe en BD. ID: {docs[0].get('id')}"
        else:
             return "NO VERIFICADO: No encontrado en BD."
    except Exception as e:
        return f"Error check: {e}"

tools_map = {
    "buscar_rag": buscar_rag,
    "verificar_url": verificar_url
}

async def ejecutar_tool_call(tool_call):
    name = tool_call.function.name
    try:
        args = json.loads(tool_call.function.arguments)
        if name in tools_map:
            # Note: synchronous requests inside async function blocks event loop, 
            # but for this script it's fine (sequential execution)
            if name == "buscar_rag":
                return await buscar_rag(args.get("query"), args.get("top_k", 5), args.get("tema_filter"))
            elif name == "verificar_url":
                return await verificar_url(args.get("articulo", ""), args.get("ley", ""))
        return f"Error: Tool {name} no encontrada localmente"
    except Exception as e:
        return f"Error ejecutando tool {name}: {e}"

def get_output_file():
    """Encuentra el archivo más reciente para continuar o crea uno nuevo"""
    os.makedirs(DATA_DIR, exist_ok=True)
    files = glob.glob(os.path.join(DATA_DIR, "qa_mass_verified_*.jsonl"))
    if files:
        latest_file = max(files, key=os.path.getctime)
        count = 0
        try:
            with open(latest_file, 'r') as f:
                for line in f: count += 1
        except: pass
        
        logger.info(f"📁 Continuando en: {latest_file} ({count} items existentes)")
        starting_batch = (count // BATCH_SIZE) + 1
        return latest_file, starting_batch
    else:
        new_file = os.path.join(DATA_DIR, f"qa_mass_verified_{int(time.time())}.jsonl")
        logger.info(f"📁 Nuevo archivo: {new_file}")
        return new_file, 1

async def generate_batch(batch_num, law_context, output_file):
    logger.info(f"🚀 Iniciando Batch {batch_num}/{TOTAL_BATCHES}...")
    # Temas expandidos para cobertura TOTAL (AGE + SS)
    topics = [
        "La Corona: Sucesión, Regencia y Funciones del Rey",
        "Las Cortes Generales: Composición y atribuciones de Congreso y Senado",
        "El Gobierno y la Administración: El Presidente y el Consejo de Ministros",
        "Gobierno Abierto y Ley 19/2013 de Transparencia",
        "Agenda 2030 y Objetivos de Desarrollo Sostenible (ODS)",
        "La Administración General del Estado: Órganos Centrales y Territoriales",
        "Las Comunidades Autónomas: Constitución y Competencias",
        "La Administración Local: Provincia, Municipio e Isla",
        "Atención al Ciudadano y personas con discapacidad en la Administración",
        "Registro, Archivo y Administración Electrónica (Ley 39/2015)",
        "El Estatuto Básico del Empleado Público (EBEP): Clases de Personal",
        "EBEP: Derechos, Deberes y Código de Conducta",
        "EBEP: Carrera Profesional y Retribuciones",
        "EBEP: Situaciones Administrativas de los Funcionarios",
        "EBEP: Régimen Disciplinario y Faltas",
        "Los Presupuestos Generales del Estado (PGE): Elaboración y Aprobación",
        "Gestión del Gasto Público y Control por la IGAE",
        "Sistema No Contributivo de la Seguridad Social",
        "Ingreso Mínimo Vital (IMV): Requisitos y Cuantía",
        "Entidades Gestoras de la Seguridad Social (INSS, TGSS, ISM)",
        "Mutuas Colaboradoras con la Seguridad Social",
        "Regímenes Especiales de la Seguridad Social: Mar, Minería, etc.",
        "La Protección de Datos (LOPDGDD) en el Sector Público",
        "El Acto Administrativo: Motivación, Notificación y Silencio Administrativo",
        "Contratos del Sector Público (LCSP): Clasificación y Adjudicación",
        "Políticas de Igualdad y Violencia de Género (Ley Orgánica 3/2007)"
    ]
    topic = topics[(batch_num - 1) % len(topics)]
    
    prompt = f"""
    Eres un experto en oposiciones de AGE y Seguridad Social. Genera 10 preguntas de NIVEL EXPERTO sobre: '{topic}'.
    
    OBJETIVO: Crear un dataset diversificado y veraz.
    
    ESTRUCTURA OBLIGATORIA DEL BATCH (10 preguntas en total):
    - 2 preguntas de tipo TEST (Normal): Directas sobre el temario.
    - 2 preguntas de tipo COMPARACIÓN: Contrastar dos conceptos legales parecidos.
    - 2 preguntas de tipo PROCEDIMIENTO: Pasos de un trámite o gestión administrativa.
    - 2 preguntas de tipo RAZONAMIENTO JURÍDICO: Mini-caso práctico de aplicación de la norma.
    - 2 preguntas de tipo RELACIÓN: Vincular artículos, órganos o plazos.

    FLUJO DE TRABAJO DEL AGENTE:
    - Primero, usa 'buscar_rag(query="{topic}")' para obtener la base legal.
    - Segundo, usa 'verificar_url(articulo="...", ley="...")' para cada referencia citada.
    - No inventes. Si el RAG no da el dato, búscalo de nuevo con 'buscar_rag'.

    FORMATO DE SALIDA (JSON ESTRICTO):
    Devuelve un ARRAY JSON con 10 objetos. Ejemplo:
    [
      {{
        "pregunta": "...",
        "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "respuesta_correcta": "A/B/C/D",
        "explicacion": "Explicación detallada citando el artículo exacto.",
        "referencias": ["Art. X de la Ley Y"],
        "tema": "{topic}",
        "tipo": "RAZONAMIENTO/TEST/COMPARACION/PROCEDIMIENTO/RELACION"
      }}
    ]
    NO incluyas texto fuera del JSON.
    """
    
    messages = [{"role": "user", "content": prompt}]
    
    # Loop de Agente con retry
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 1. Llamada inicial
            response = client.agents.complete(agent_id=AGENT_ID, messages=messages)
            if not response.choices: 
                raise Exception("Respuesta vacía de Mistral")
                
            choice = response.choices[0]
            
            # 2. Iterar herramientas (Máx 5 pasos)
            for _ in range(5):
                if not choice.message.tool_calls:
                    break
                    
                tool_calls = choice.message.tool_calls
                messages.append(choice.message) 
                
                for tc in tool_calls:
                    # Execute tool synchronously (since requests is sync)
                    result = await ejecutar_tool_call(tc)
                    messages.append({
                        "role": "tool", 
                        "name": tc.function.name, 
                        "content": str(result), 
                        "tool_call_id": tc.id
                    })
                
                response = client.agents.complete(agent_id=AGENT_ID, messages=messages)
                choice = response.choices[0]
                
            # 3. Guardar si hay JSON
            content = choice.message.content
            
            # Handle list content (Mistral API edge case)
            if isinstance(content, list):
                logger.info(f"ℹ️ Content es lista, uniendo texto...")
                # Try to extract text from items (assuming they have .text or are strings)
                text_parts = []
                for item in content:
                    if hasattr(item, 'text'):
                        text_parts.append(item.text)
                    elif isinstance(item, str):
                        text_parts.append(item)
                    elif isinstance(item, dict) and 'text' in item:
                        text_parts.append(item['text'])
                content = "".join(text_parts)
            
            if content is None: content = ""
            
            # Limpieza básica de Markdown
            content_clean = content.replace("```json", "").replace("```", "").strip()
            
            if "[" in content_clean and "]" in content_clean:
                try:
                    start = content_clean.find('[')
                    end = content_clean.rfind(']') + 1
                    json_str = content_clean[start:end]
                    data = json.loads(json_str)
                    
                    with open(output_file, 'a', encoding='utf-8') as f:
                        for item in data:
                            item['meta_batch'] = batch_num
                            f.write(json.dumps(item, ensure_ascii=False) + "\n")
                    logger.info(f"✅ Batch {batch_num} guardado ({len(data)} items)")
                    return True # Éxito
                except json.JSONDecodeError as je:
                     logger.warning(f"⚠️ Error decodificando JSON: {je}")
            
            # Si llegamos aqui, falló el JSON
            logger.warning(f"⚠️ Batch {batch_num} sin JSON válido. Contenido raw:\n{content[:500]}...")
            await asyncio.sleep(5)
                
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "too many requests" in error_msg.lower():
                logger.warning(f"⚠️ API 429 (Límite excedido). Esperando 60s antes de reintentar...")
                await asyncio.sleep(60)
            else:
                logger.error(f"❌ Error en Batch {batch_num} (Intento {attempt+1}): {e}")
                await asyncio.sleep(5) 
            
    return False 

async def main():
    logger.info("🏁 Script Masivo V2 (Refactored: HTTP + Debug)")
    
    ctx = get_law_context()
    file_path, start_batch = get_output_file()
    
    # if start_batch > TOTAL_BATCHES:
    #     print("✅ Generación ya completada anteriormente.")
    #     return

    # Resume normal logic
    for i in range(start_batch, TOTAL_BATCHES + 1):
        success = await generate_batch(i, ctx, file_path)
        if success:
            logger.info(f"⏳ Pausa de seguridad ({PAUSE_SECONDS}s)...")
            time.sleep(PAUSE_SECONDS)
        else:
            logger.error(f"⛔ Batch {i} falló definitivamente. Saltando...")

if __name__ == "__main__":
    asyncio.run(main())
