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


class MistralAgentProvider(LLMProvider):
    """Mistral AI Agent - Medium con web access y code generation"""
    
    def __init__(self, agent_id: str = None):
        self.api_key = os.getenv('MISTRAL_API_KEY')
        self.agent_id = agent_id or os.getenv('AGENTE_ID')
        self.base_url = 'https://api.mistral.ai/v1'
        
        if not self.api_key:
            logger.warning("MISTRAL_API_KEY not found in environment")
        if not self.agent_id:
            logger.warning("AGENTE_ID not found in environment")
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta usando Mistral Agent API"""
        
        if not self.api_key or not self.agent_id:
            raise ValueError("MISTRAL_API_KEY and AGENTE_ID must be configured")
        
        # Agregar system prompt si no existe (el agente necesita instrucciones)
        if not any(msg.get('role') == 'system' for msg in messages):
            messages.insert(0, {
                "role": "system",
                "content": "Eres un asistente experto en derecho español de Seguridad Social. Responde de forma precisa citando siempre fuentes legales oficiales."
            })
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                # Mistral Agents API NO acepta temperature ni max_tokens cuando usas agent_id
                response = await client.post(
                    f"{self.base_url}/agents/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "agent_id": self.agent_id,
                        "messages": messages
                        # NO temperature, NO max_tokens con agents
                    }
                )
                
                if response.status_code != 200:
                    error_text = response.text
                    raise Exception(f"Mistral Agent API error: {response.status_code} - {error_text}")
                
                result = response.json()
                if result.get('choices'):
                    content = result['choices'][0]['message'].get('content', '')
                    yield content
                    
            except Exception as e:
                logger.error(f"Mistral Agent error: {e}")
                raise
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "name": "Agent Medium",
            "provider": "mistral-agent",
            "model": "mistral-medium",
            "speed": "medium",
            "cost": "€0.10/M",
            "features": ["web-access", "code-generation"],
            "configured": bool(self.api_key and self.agent_id)
        }


class MistralVPSProvider(LLMProvider):
    """Mistral en VPS - Fallback siempre disponible"""
    
    def __init__(self):
        self.model = 'mistral'
        self.base_url = os.getenv('MISTRAL_URL', 'http://localhost:8080')
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta usando Mistral VPS"""
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/v1/chat/completions",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": True,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    if response.status_code != 200:
                        raise Exception(f"Mistral VPS error: {response.status_code}")
                    
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
                raise Exception(f"Mistral VPS streaming error: {e}")
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "mistral-vps",
            "model": self.model,
            "speed": "slow",
            "cost": "free",
            "configured": True
        }


# Registry de proveedores disponibles
PROVIDERS = {
    # Groq (Ultra rápido) ⚡
    'groq-8b': GroqProvider('llama-3.1-8b-instant'),
    'groq-70b': GroqProvider('llama-3.3-70b-versatile'),
    # 'groq-mixtral': GroqProvider('mixtral-8x7b-32768'),  # DEPRECADO
    
    # DeepSeek (Barato) 💰
    'deepseek': DeepSeekProvider(),
    
    # Google Gemini (Multimodal) 🌟
    # 'gemini-flash': GeminiProvider('gemini-2.0-flash-exp'),  # Quota issues
    'gemini-pro': GeminiProvider('gemini-2.5-pro'),
    'gemini-3-pro': GeminiProvider('gemini-3-pro-preview'),
    
    # Hugging Face (DESHABILITADO - API migrada) 🤗
    # 'hf-llama-70b': HuggingFaceProvider('meta-llama/Llama-3.1-70B-Instruct'),
    # 'hf-mixtral': HuggingFaceProvider('mistralai/Mixtral-8x7B-Instruct-v0.1'),
    # 'hf-qwen': HuggingFaceProvider('Qwen/Qwen2.5-72B-Instruct'),
    
    # Cohere (Producción) 🔷
    'cohere-command-r': CohereProvider('command-r-08-2024'),
    'cohere-command-r-plus': CohereProvider('command-r-plus-08-2024'),
    
    # Mistral AI 🟣
    'mistral-agent': MistralAgentProvider(),  # Agent Medium con web + code
    
    # Mistral VPS (Fallback siempre disponible) 🐌
    'mistral-vps': MistralVPSProvider()
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
