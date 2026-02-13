
import json
import time
import requests
import random
import os
import google.generativeai as genai
from qdrant_client import QdrantClient

# Config
TARGET_COUNT = 400
OUTPUT_FILE = "/home/spas/OPOS_GEMINI_1/MASTER_DATASET_v12_SUPPLEMENT.jsonl"
ENV_FILE = "/home/spas/OPOS_GEMINI_1/backend/.env.backend"

# System Prompt adjusted for Gemini
SYSTEM_PROMPT = """Eres un experto redactor de exámenes de oposición para la Seguridad Social (Cuerpo Administrativo/Gestión).
Tu tarea es crear UNA pregunta tipo test de ALTA DIFICULTAD basada EXCLUSIVAMENTE en el texto legal proporcionado.

REGLAS:
1. La pregunta debe ser compleja (caso práctico breve o concepto difícil).
2. Genera 4 opciones (A, B, C, D). Solo una es correcta.
3. Las opciones incorrectas deben ser plausibles (distractores fuertes).
4. El razonamiento debe citar el artículo/ley del texto proporcionado.
5. DEBES responder ÚNICAMENTE con un objeto JSON válido con este formato:
{
  "pregunta": "...",
  "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "respuesta_correcta": "C",
  "explicacion": "..."
}
"""

def load_gemini_key():
    """Load GEMINI_API_KEY from .env.backend"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key: return api_key
    
    try:
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.strip().startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1].strip()
    except Exception as e:
        print(f"Error loading env file: {e}")
    return None

def get_random_law_chunks(limit=100):
    """Retrieve random chunks from Qdrant."""
    try:
        client = QdrantClient(url="http://localhost:6333", timeout=20)
        # Use scroll to get points. Limit is max result, but we might loop if needed.
        points, _ = client.scroll(
            collection_name="opositaia_knowledge_hybrid_FULL",
            limit=limit,
            with_payload=True,
            with_vectors=False
        )
        return points
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        return []

def generate_item_gemini(model, context_text, context_source):
    """Generate a QA item using Gemini API."""
    prompt = f"""
    TEXTO LEGAL DE REFERENCIA:
    Fuente: {context_source}
    Contenido: "{context_text[:2500]}..."

    Genera una pregunta tipo test difícil basada en este texto.
    Recuerda: Alto nivel, formato JSON, opciones A/B/C/D.
    """
    
    try:
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\n{prompt}",
            generation_config={"response_mime_type": "application/json"}
        )
        return response.text
    except Exception as e:
        print(f"Gemini generation error: {e}")
        time.sleep(2) # Backoff
    return None

def format_as_chat(item_json):
    """Convert generated JSON to Chat format (v12 standard)."""
    try:
        # Clean potential markdown fences
        clean_json = item_json.replace("```json", "").replace("```", "").strip()
        d = json.loads(clean_json)
        
        q = d.get('pregunta')
        opts = d.get('opciones')
        ans = d.get('respuesta_correcta')
        exp = d.get('explicacion')
        
        if not (q and opts and ans and exp): return None
        
        opts_str = "\n".join(opts) if isinstance(opts, list) else str(opts)
        
        user = f"{q}\n\nOpciones:\n{opts_str}"
        asst = f"selected_option: {ans}\n\nRazonamiento:\n{exp}"
        
        return {
            "messages": [
                {"role": "system", "content": "Eres un experto en oposiciones. Responde citando normativa."},
                {"role": "user", "content": user},
                {"role": "assistant", "content": asst}
            ]
        }
    except Exception as e:
        return None

def main():
    print("🚀 Iniciando Generador Platinum (Powered by Gemini)...")
    
    key = load_gemini_key()
    if not key:
        print("❌ No se encontró GEMINI_API_KEY en .env.backend")
        return

    genai.configure(api_key=key)
    # Using gemini-1.5-flash for speed and high capacity
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print("📥 Obteniendo contextos legales de Qdrant...")
    chunks = get_random_law_chunks(limit=TARGET_COUNT+50) # Buffer
    print(f"✅ Recuperados {len(chunks)} fragmentos legales reales.")
    
    generated_count = 0
    errors = 0
    
    open_mode = 'a' if os.path.exists(OUTPUT_FILE) else 'w'
    
    with open(OUTPUT_FILE, open_mode) as f:
        for i, chunk in enumerate(chunks):
            if generated_count >= TARGET_COUNT: break
            
            # FIXED: text_snippet instead of text
            text = chunk.payload.get('text_snippet', '')
            source = chunk.payload.get('law_name', 'Ley desconocida')
            
            if len(text) < 200: continue 
            
            if i % 10 == 0: print(f"⚡ Generando item {generated_count+1}/{TARGET_COUNT}...")
            
            json_str = generate_item_gemini(model, text, source)
            
            if json_str:
                chat_item = format_as_chat(json_str)
                if chat_item:
                    f.write(json.dumps(chat_item, ensure_ascii=False) + '\n')
                    f.flush()
                    generated_count += 1
                else:
                    errors += 1
            else:
                errors += 1
                
            time.sleep(0.5)
                
    print(f"✅ Generación completada. Items válidos: {generated_count}. Errores: {errors}")
    print(f"📁 Guardado en {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
