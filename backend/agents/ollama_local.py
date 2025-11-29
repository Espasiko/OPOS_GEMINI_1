"""Wrapper ligero para usar Ollama localmente desde el backend.

Proporciona `generate_with_ollama(prompt, model, timeout)` que intenta usar
la librería `ollama_client` si está instalada, y si no, usa la API HTTP
en `OLLAMA_URL` (por defecto `http://localhost:11434/api/generate`).

Diseñado para ser fácil de importar desde otros agentes:

    from agents.ollama_local import generate_with_ollama

"""
import os
import json
import requests
from typing import Optional


def _get_ollama_url():
    return os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')


def generate_with_ollama(prompt: str, model: Optional[str] = None, max_tokens: int = 512, timeout: int = 300) -> str:
    """Genera texto usando Ollama local.

    - `model`: si se proporciona, se envía en el payload; también se puede
      configurar con la variable `OLLAMA_MODEL`.
    - Retorna la cadena de texto resultante.
    """
    # Preferir el cliente oficial si está disponible
    try:
        from ollama_client import OllamaClient
        client = OllamaClient()
        chosen = model or os.getenv('OLLAMA_MODEL') or 'mi-modelo-legal'
        resp = client.generate(chosen, prompt)
        # Intentar extraer texto según la API del cliente
        if isinstance(resp, dict):
            # puede variar según versión
            return resp.get('text') or resp.get('output') or json.dumps(resp)
        return str(resp)
    except Exception:
        # Fallback a la API HTTP simple
        url = _get_ollama_url()
        chosen = model or os.getenv('OLLAMA_MODEL') or 'mi-modelo-legal'
        payload = {
            'model': chosen,
            'prompt': prompt,
            'max_tokens': max_tokens,
        }
        try:
            r = requests.post(url, json=payload, timeout=timeout)
            r.raise_for_status()
            data = r.json()
            # La respuesta de Ollama HTTP puede tener varias formas;
            # buscar campos comunes.
            if isinstance(data, dict):
                if 'text' in data:
                    return data['text']
                if 'output' in data and isinstance(data['output'], list):
                    # salida en bloques
                    outs = [o.get('text') or o.get('content') for o in data['output']]
                    return '\n'.join([o for o in outs if o])
                # si la clave 'choices' existe (estilo OpenAI), concatenar
                if 'choices' in data:
                    texts = []
                    for c in data['choices']:
                        if isinstance(c, dict) and 'text' in c:
                            texts.append(c['text'])
                    if texts:
                        return '\n'.join(texts)
            # Fallback: devolver la representación JSON
            return json.dumps(data)
        except Exception as e:
            raise RuntimeError(f"Error llamando a Ollama ({url}): {e}")


if __name__ == '__main__':
    # Prueba rápida desde línea de comandos
    import sys
    prompt = ' '.join(sys.argv[1:]) or 'Di: hola desde Ollama local'
    print(generate_with_ollama(prompt))
