"""
Wrapper para Mistral 7B Instruct Q4 GGUF - Inferencia local CPU
Usa llama-cpp-python (más eficiente que Ollama en CPU)
"""

import os
from typing import Optional, Dict, Any

# Lazy import - solo cargar si se usa
_llama_model = None

MODEL_PATH = os.path.expanduser("~/mistral_models/mistral-7b-instruct-q4.gguf")

def get_model():
    """Singleton pattern - carga el modelo solo una vez"""
    global _llama_model
    
    if _llama_model is None:
        try:
            from llama_cpp import Llama
            
            print(f"⏳ Cargando Mistral 7B Q4 desde {MODEL_PATH}...")
            _llama_model = Llama(
                model_path=MODEL_PATH,
                n_ctx=2048,           # Context window (2K tokens - ajustable)
                n_threads=4,          # Usar los 4 cores del i5-3470
                n_batch=512,          # Batch size para inferencia
                n_gpu_layers=0,       # CPU-only (sin GPU)
                verbose=False,
                seed=-1,              # Random seed
            )
            print("✅ Modelo cargado correctamente en RAM")
            
        except ImportError:
            raise ImportError(
                "llama-cpp-python no instalado. Ejecuta:\n"
                "pip install llama-cpp-python"
            )
        except Exception as e:
            raise RuntimeError(f"Error cargando modelo: {e}")
    
    return _llama_model


def generate(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.7,
    top_p: float = 0.9,
    top_k: int = 40,
    repeat_penalty: float = 1.1,
    stop: Optional[list] = None,
    stream: bool = False,
) -> str:
    """
    Genera texto con Mistral 7B Q4 GGUF
    
    Args:
        prompt: Texto de entrada (puede incluir [INST] tags para instruct format)
        max_tokens: Máximo de tokens a generar
        temperature: Creatividad (0.0 = determinista, 1.0 = creativo)
        top_p: Nucleus sampling
        top_k: Top-k sampling
        repeat_penalty: Penalización por repetición
        stop: Lista de strings que detienen la generación
        stream: Si True, devuelve generador (para streaming)
    
    Returns:
        Texto generado (str)
    """
    
    model = get_model()
    
    # Formatear prompt con Mistral Instruct format si no está ya formateado
    if not prompt.startswith("[INST]"):
        formatted_prompt = f"[INST] {prompt} [/INST]"
    else:
        formatted_prompt = prompt
    
    # Parámetros de generación
    gen_params = {
        "prompt": formatted_prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "repeat_penalty": repeat_penalty,
        "stop": stop or ["[INST]", "</s>"],
        "stream": stream,
        "echo": False,  # No incluir el prompt en la salida
    }
    
    if stream:
        # Retornar generador para streaming
        return model(**gen_params)
    else:
        # Generación completa (blocking)
        response = model(**gen_params)
        return response["choices"][0]["text"].strip()


def chat(
    messages: list[Dict[str, str]],
    max_tokens: int = 512,
    temperature: float = 0.7,
) -> str:
    """
    Formato chat compatible con OpenAI/Gemini
    
    Args:
        messages: Lista de mensajes [{"role": "user", "content": "..."}, ...]
        max_tokens: Máximo de tokens a generar
        temperature: Creatividad
    
    Returns:
        Respuesta del modelo (str)
    
    Example:
        >>> chat([
        ...     {"role": "user", "content": "¿Qué es el recurso de casación?"},
        ... ])
    """
    
    # Convertir formato chat a Mistral Instruct format
    # Mistral format: [INST] user message [/INST] assistant message [INST] user message [/INST]
    
    formatted_parts = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        
        if role == "user":
            formatted_parts.append(f"[INST] {content} [/INST]")
        elif role == "assistant":
            formatted_parts.append(f" {content} ")
    
    prompt = "".join(formatted_parts)
    
    return generate(
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )


def verify_installation() -> Dict[str, Any]:
    """
    Verifica que todo esté correctamente instalado
    
    Returns:
        Dict con estado de instalación
    """
    status = {
        "llama_cpp_installed": False,
        "model_exists": False,
        "model_path": MODEL_PATH,
        "model_size_gb": 0.0,
        "can_load": False,
        "errors": [],
    }
    
    # Check llama-cpp-python
    try:
        import llama_cpp
        status["llama_cpp_installed"] = True
    except ImportError:
        status["errors"].append("llama-cpp-python no instalado")
    
    # Check model file
    if os.path.exists(MODEL_PATH):
        status["model_exists"] = True
        size_bytes = os.path.getsize(MODEL_PATH)
        status["model_size_gb"] = round(size_bytes / (1024**3), 2)
    else:
        status["errors"].append(f"Modelo no encontrado en {MODEL_PATH}")
    
    # Try loading (only if previous checks pass)
    if status["llama_cpp_installed"] and status["model_exists"]:
        try:
            _ = get_model()
            status["can_load"] = True
        except Exception as e:
            status["errors"].append(f"Error cargando modelo: {e}")
    
    return status


if __name__ == "__main__":
    print("🔍 Verificando instalación de Mistral 7B Q4 GGUF...")
    print("=" * 60)
    
    status = verify_installation()
    
    print(f"llama-cpp-python instalado: {'✅' if status['llama_cpp_installed'] else '❌'}")
    print(f"Modelo existe: {'✅' if status['model_exists'] else '❌'}")
    print(f"Ruta: {status['model_path']}")
    print(f"Tamaño: {status['model_size_gb']} GB")
    print(f"Puede cargar: {'✅' if status['can_load'] else '❌'}")
    
    if status["errors"]:
        print("\n⚠️  Errores encontrados:")
        for err in status["errors"]:
            print(f"  - {err}")
    else:
        print("\n✅ Todo listo - probando generación...")
        print("=" * 60)
        
        # Test simple
        response = generate(
            prompt="¿Qué es el recurso de casación? Responde en máximo 3 frases.",
            max_tokens=150,
            temperature=0.7,
        )
        
        print("\n📝 Respuesta del modelo:")
        print(response)
        print("\n" + "=" * 60)
        print("✅ Test completado exitosamente")
