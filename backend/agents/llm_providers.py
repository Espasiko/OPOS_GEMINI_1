"""
LLM Providers - Sistema multi-proveedor
Soporta: Groq, DeepSeek, Gemini, Mistral VPS
"""
from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Any
import httpx
import json
import os
import logging

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Base class para proveedores de LLM"""
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta en streaming"""
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Retorna información del proveedor"""
        pass


class GroqProvider(LLMProvider):
    """Groq - Ultra rápido con Llama models"""
    
    def __init__(self, model: str = 'llama-3.1-8b-instant'):
        self.model = model
        self.api_key = os.getenv('GROQ_API_KEY')
        self.base_url = 'https://api.groq.com/openai/v1'
        
        if not self.api_key:
            logger.warning("GROQ_API_KEY not found in environment")
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta usando Groq API"""
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not configured")
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": True,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        raise Exception(f"Groq API error: {response.status_code} - {error_text}")
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            chunk = line[6:]
                            if chunk == "[DONE]":
                                break
                            
                            try:
                                data = json.loads(chunk)
                                content = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue
            
            except httpx.ConnectError as e:
                raise Exception(f"Cannot connect to Groq: {e}")
            except Exception as e:
                raise Exception(f"Groq streaming error: {e}")
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "groq",
            "model": self.model,
            "speed": "ultra",
            "cost": "free",
            "configured": bool(self.api_key)
        }


class DeepSeekProvider(LLMProvider):
    """DeepSeek V3 - Mejor precio/calidad"""
    
    def __init__(self):
        self.model = 'deepseek-chat'
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = 'https://api.deepseek.com'
        
        if not self.api_key:
            logger.warning("DEEPSEEK_API_KEY not found in environment")
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta usando DeepSeek API"""
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not configured")
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": True,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        raise Exception(f"DeepSeek API error: {response.status_code} - {error_text}")
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            chunk = line[6:]
                            if chunk == "[DONE]":
                                break
                            
                            try:
                                data = json.loads(chunk)
                                content = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue
            
            except Exception as e:
                raise Exception(f"DeepSeek streaming error: {e}")
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "deepseek",
            "model": self.model,
            "speed": "fast",
            "cost": "cheap",
            "configured": bool(self.api_key)
        }


class GeminiProvider(LLMProvider):
    """Google Gemini - Multimodal"""
    
    def __init__(self, model: str = 'gemini-2.0-flash-exp'):
        self.model = model
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = 'https://generativelanguage.googleapis.com/v1beta'
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment")
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta usando Gemini API"""
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        # Convertir mensajes de OpenAI format a Gemini format
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            if msg["role"] == "system":
                # System message se agrega como primer user message
                contents.insert(0, {
                    "role": "user",
                    "parts": [{"text": msg["content"]}]
                })
            else:
                contents.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/models/{self.model}:streamGenerateContent",
                    params={"key": self.api_key, "alt": "sse"},
                    json={
                        "contents": contents,
                        "generationConfig": {
                            "temperature": temperature,
                            "maxOutputTokens": max_tokens
                        }
                    }
                )
                
                if response.status_code != 200:
                    error_text = response.text
                    raise Exception(f"Gemini API error: {response.status_code} - {error_text}")
                
                for line in response.text.split('\n'):
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            if 'candidates' in data:
                                for candidate in data['candidates']:
                                    if 'content' in candidate:
                                        for part in candidate['content'].get('parts', []):
                                            if 'text' in part:
                                                yield part['text']
                        except json.JSONDecodeError:
                            continue
            
            except Exception as e:
                raise Exception(f"Gemini streaming error: {e}")
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "gemini",
            "model": self.model,
            "speed": "fast",
            "cost": "free" if "flash" in self.model else "expensive",
            "configured": bool(self.api_key)
        }


class HuggingFaceProvider(LLMProvider):
    """Hugging Face Inference API - Múltiples modelos"""
    
    def __init__(self, model: str = 'meta-llama/Llama-3.1-70B-Instruct'):
        self.model = model
        self.api_key = os.getenv('HF_TOKEN')
        # Nueva URL de HuggingFace
        self.base_url = 'https://api-inference.huggingface.co/models'
        
        if not self.api_key:
            logger.warning("HF_TOKEN not found in environment")
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta usando HF Inference API"""
        
        if not self.api_key:
            raise ValueError("HF_TOKEN not configured")
        
        # Convertir mensajes a prompt
        prompt = self._messages_to_prompt(messages)
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/{self.model}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "temperature": temperature,
                            "max_new_tokens": max_tokens,
                            "return_full_text": False
                        },
                        "stream": False  # HF no soporta streaming bien, usar respuesta completa
                    }
                )
                
                if response.status_code != 200:
                    error_text = response.text
                    raise Exception(f"HF API error: {response.status_code} - {error_text}")
                
                # HF devuelve la respuesta completa, no streaming
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    text = data[0].get('generated_text', '')
                    # Simular streaming enviando la respuesta en chunks
                    chunk_size = 50
                    for i in range(0, len(text), chunk_size):
                        yield text[i:i+chunk_size]
                else:
                    yield str(data)
            
            except Exception as e:
                raise Exception(f"HuggingFace error: {e}")
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convierte mensajes a prompt para HF"""
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt += f"System: {content}\n\n"
            elif role == "user":
                prompt += f"User: {content}\n\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n\n"
        prompt += "Assistant: "
        return prompt
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "huggingface",
            "model": self.model.split('/')[-1],
            "speed": "medium",
            "cost": "cheap",
            "configured": bool(self.api_key)
        }


class CohereProvider(LLMProvider):
    """Cohere - Modelos optimizados para producción (API v1)"""
    
    def __init__(self, model: str = 'command-r-plus-08-2024'):
        self.model = model
        self.api_key = os.getenv('COHERE_API_KEY')
        self.base_url = 'https://api.cohere.com/v1'  # Usar v1, no v2
        
        if not self.api_key:
            logger.warning("COHERE_API_KEY not found in environment")
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta usando Cohere API v1"""
        
        if not self.api_key:
            raise ValueError("COHERE_API_KEY not configured")
        
        # Convertir mensajes a formato Cohere v1
        chat_history = []
        message = ""
        preamble = ""
        
        for msg in messages:
            if msg["role"] == "system":
                preamble = msg["content"]
            elif msg["role"] == "user":
                if chat_history:  # Si hay historial, agregar como USER_NAME
                    chat_history.append({
                        "role": "USER",
                        "message": msg["content"]
                    })
                else:
                    message = msg["content"]
            elif msg["role"] == "assistant":
                chat_history.append({
                    "role": "CHATBOT",
                    "message": msg["content"]
                })
        
        payload = {
            "model": self.model,
            "message": message,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        if preamble:
            payload["preamble"] = preamble
        if chat_history:
            payload["chat_history"] = chat_history
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                ) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        raise Exception(f"Cohere API error: {response.status_code} - {error_text}")
                    
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                if data.get('event_type') == 'text-generation':
                                    yield data.get('text', '')
                            except json.JSONDecodeError:
                                continue
            
            except Exception as e:
                raise Exception(f"Cohere streaming error: {e}")
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "cohere",
            "model": self.model,
            "speed": "fast",
            "cost": "medium",
            "configured": bool(self.api_key)
        }


class MistralAPIProvider(LLMProvider):
    """Mistral AI API - Modelos potentes y baratos"""
    
    def __init__(self, model: str = 'mistral-small-latest'):
        self.model = model
        self.api_key = os.getenv('MISTRAL_API_KEY')
        self.base_url = 'https://api.mistral.ai/v1'
        
        if not self.api_key:
            logger.warning("MISTRAL_API_KEY not found in environment")
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta usando Mistral API"""
        
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not configured")
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": True,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        raise Exception(f"Mistral API error: {response.status_code} - {error_text}")
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            chunk = line[6:]
                            if chunk == "[DONE]":
                                break
                            
                            try:
                                data = json.loads(chunk)
                                content = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue
            
            except Exception as e:
                raise Exception(f"Mistral API streaming error: {e}")
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "mistral",
            "model": self.model,
            "speed": "fast",
            "cost": "cheap",
            "configured": bool(self.api_key)
        }


class SalamandraVPSProvider(LLMProvider):
    """Salamandra 7B Instruct (VPS) - Modelo Propio"""
    
    def __init__(self):
        self.model = 'salamandra' # Nombre interno
        # Mantenemos MISTRAL_URL por retrocompatibilidad del .env, pero la logica es Salamandra
        self.base_url = os.getenv('MISTRAL_URL', 'http://147.93.95.67:8080')
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta usando Salamandra (protocolo OpenAI/Llama.cpp)"""
        
        async with httpx.AsyncClient(timeout=300.0, verify=False) as client: # Timeout ajustado, SSL ignorado (cert expirado)
            try:
                # Llama.cpp server usa formato OpenAI compatible
                async with client.stream(
                    "POST",
                    f"{self.base_url}/v1/chat/completions",
                    json={
                        "model": "salamandra-7b-instruct", # Nombre para el server
                        "messages": messages,
                        "stream": True,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    if response.status_code != 200:
                        raise Exception(f"Salamandra VPS error: {response.status_code}")
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            chunk = line[6:]
                            if chunk == "[DONE]":
                                break
                            
                            try:
                                data = json.loads(chunk)
                                content = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue
            
            except Exception as e:
                raise Exception(f"Salamandra VPS streaming error: {e}")
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "salamandra",
            "model": self.model,
            "speed": "cpu-slow",
            "cost": "free",
            "configured": True
        }

# Registry de proveedores disponibles
PROVIDERS = {
    # Groq (Ultra rápido) ⚡
    'groq-8b': GroqProvider('llama-3.1-8b-instant'),
    'groq-70b': GroqProvider('llama-3.3-70b-versatile'),
    
    # DeepSeek (Barato) 💰
    'deepseek': DeepSeekProvider(),
    
    # Gemini 🌟
    'gemini-pro': GeminiProvider('gemini-2.5-pro'),
    'gemini-3-pro': GeminiProvider('gemini-3-pro-preview'),
    
    # Mistral AI API 🔮
    'mistral-small': MistralAPIProvider('mistral-small-latest'),
    'mistral-medium': MistralAPIProvider('mistral-medium-latest'),
    
    # Cohere 🔷
    'cohere-command-r': CohereProvider('command-r-08-2024'),
    
    # SALAMANDRA (VPS Propio) 🦎
    'salamandra': SalamandraVPSProvider()
}


def get_provider(provider_id: str) -> LLMProvider:
    """Obtiene un proveedor por ID"""
    if provider_id not in PROVIDERS:
        logger.warning(f"Provider {provider_id} not found, using groq-8b")
        return PROVIDERS['groq-8b']
    return PROVIDERS[provider_id]


def list_providers() -> List[Dict[str, Any]]:
    """Lista todos los proveedores disponibles"""
    return [
        {
            "id": provider_id,
            **provider.get_info()
        }
        for provider_id, provider in PROVIDERS.items()
    ]
