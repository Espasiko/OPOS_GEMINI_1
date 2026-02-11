import httpx
import logging
from typing import Optional, AsyncGenerator
import yaml
from pathlib import Path
import json
import requests

logger = logging.getLogger(__name__)

class SalamandraClient:
    """
    Cliente para Salamandra 7B
    Prioridad: VPS (llama.cpp OpenAI API) → Local (Ollama)
    """
    
    def __init__(self):
        # Cargar config
        config_path = Path(__file__).parent.parent / "config" / "prompts" / "salamandra.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        self.vps_url = config['salamandra_config']['vps_url']
        self.local_url = config['salamandra_config']['local_url']
        self.model_name = config['salamandra_config']['model_name']
        self.settings = config['salamandra_config']['optimal_settings']
        self.timeout = config['salamandra_config']['timeout']
        
        logger.info(f"SalamandraClient initialized: VPS={self.vps_url}, Local={self.local_url}")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Genera respuesta con Salamandra
        
        Args:
            prompt: Prompt del usuario
            system_prompt: System prompt (opcional)
            temperature: Override temperature
            max_tokens: Override max tokens
        
        Returns:
            Respuesta completa
        """
        # Intentar VPS primero (llama.cpp con OpenAI API)
        try:
            logger.info(f"Trying VPS llama.cpp: {self.vps_url}/v1/chat/completions")
            
            # Preparar mensajes para OpenAI API
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            vps_payload = {
                "model": "salamandra-7b-instruct-Q4_K_M.gguf",  # Nombre real del modelo en VPS
                "messages": messages,
                "temperature": temperature or self.settings['temperature'],
                "max_tokens": max_tokens or self.settings['max_tokens'],
                "top_p": self.settings['top_p']
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.vps_url}/v1/chat/completions",
                    json=vps_payload
                )
                response.raise_for_status()
                result = response.json()
                
                # Extraer respuesta de formato OpenAI
                content = result['choices'][0]['message']['content']
                logger.info("✅ VPS llama.cpp response received")
                return content
        except Exception as e:
            logger.warning(f"VPS failed: {e}, trying local Ollama...")
            
            # Fallback a local Ollama
            try:
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature or self.settings['temperature'],
                        "num_predict": max_tokens or self.settings['max_tokens'],
                        "top_p": self.settings['top_p'],
                        "repeat_penalty": self.settings['repeat_penalty']
                    }
                }
                
                if system_prompt:
                    payload["system"] = system_prompt
                
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.local_url}/api/generate",
                        json=payload
                    )
                    response.raise_for_status()
                    result = response.json()
                    logger.info("✅ Local Ollama response received")
                    return result.get("response", "")
            except Exception as e2:
                logger.error(f"Both VPS and Local failed: {e2}")
                raise Exception(f"Salamandra unavailable: VPS={e}, Local={e2}")
    
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[str, None]:
        """
        Genera respuesta con streaming
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature or self.settings['temperature'],
                "num_predict": max_tokens or self.settings['max_tokens'],
                "top_p": self.settings['top_p'],
                "repeat_penalty": self.settings['repeat_penalty']
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        # Intentar VPS primero
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.vps_url}/api/generate",
                    json=payload
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]
        except Exception as e:
            logger.warning(f"VPS streaming failed: {e}, trying local...")
            
            # Fallback a local
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.local_url}/api/generate",
                    json=payload
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]

    def generate_case(self, prompt: str) -> Optional[str]:
        """
        Genera un caso legal específico
        """
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a legal assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(
                f"{self.vps_url}/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating case: {e}")
            return None

# Singleton
_salamandra_client: Optional[SalamandraClient] = None

def get_salamandra_client() -> SalamandraClient:
    """Get or create Salamandra client singleton"""
    global _salamandra_client
    if _salamandra_client is None:
        _salamandra_client = SalamandraClient()
    return _salamandra_client

