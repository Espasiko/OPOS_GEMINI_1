"""
LLM Providers - Sistema multi-proveedor
Soporta: Groq, DeepSeek, Gemini, Mistral VPS
"""
from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Any, Optional
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

    @abstractmethod
    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Genera respuesta con soporte para herramientas (Function Calling)"""
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

    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Implementación de Tool Calling para Groq"""
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not configured")
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "tools": tools,
                    "tool_choice": "auto",
                    "temperature": temperature
                }
            )
            if response.status_code != 200:
                raise Exception(f"Groq Tool Error: {response.text}")
            return response.json()
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "groq",
            "model": self.model,
            "speed": "ultra",
            "cost": "paid",  # Actualizado: Tier gratuito agotado
            "configured": bool(self.api_key)
        }


class DeepSeekProvider(LLMProvider):
    """DeepSeek V3 / R1 - El motor de razonamiento eficiente"""
    
    def __init__(self, model: str = 'deepseek-reasoner'):
        self.model = model
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        # Usar beta para strict mode y mejores tools en R1
        self.base_url = 'https://api.deepseek.com/beta'
        
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
                        "temperature": 1.0 if "reasoner" in self.model else temperature,
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

    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Implementación de Tool Calling para DeepSeek (compatible OpenAI)"""
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not configured")
        
        async with httpx.AsyncClient(timeout=900.0) as client:  # 900s para R1 (Thinking denso + Tools)
            payload = {
                "model": self.model,
                "messages": self._normalize_messages(messages)
            }
            
            patched_tools = self._patch_tools_strict(tools)
            if patched_tools:
                payload["tools"] = patched_tools
                payload["tool_choice"] = "auto"
            
            # DeepSeek Reasoner recomienda NO usar temperature != 1.0 en algunos endpoints, 
            # pero el chat-completion estándar permite 0-2. Ajustamos según modelo.
            if "reasoner" not in self.model:
                payload["temperature"] = temperature
            
            if max_tokens:
                payload["max_tokens"] = max_tokens
                
            if response_format:
                payload["response_format"] = response_format
            
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            if response.status_code != 200:
                raise Exception(f"DeepSeek Tool Error: {response.status_code} - {response.text}")
            return response.json()

    def _normalize_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Asegura que los mensajes para DeepSeek R1 incluyan reasoning_content correctamente"""
        normalized = []
        for msg in messages:
            # DeepSeek R1 requiere que el reasoning_content se pase en un campo específico
            # para no romper el hilo de pensamiento si se sigue conversando
            norm_msg = {k: v for k, v in msg.items() if v is not None}
            normalized.append(norm_msg)
        return normalized

    def _patch_tools_strict(self, tools: Optional[List[Dict[str, Any]]]) -> Optional[List[Dict[str, Any]]]:
        """Añade strict: true a todas las herramientas para el modo beta de DeepSeek"""
        if not tools:
            return None
        patched = []
        for t in tools:
            if t.get("type") == "function":
                new_t = json.loads(json.dumps(t)) # Deep copy
                new_t["function"]["strict"] = True
                # DeepSeek strict mode requiere additionalProperties: false
                # y que TODAS las propiedades estén en el array 'required'
                if "parameters" in new_t["function"]:
                    params = new_t["function"]["parameters"]
                    params["additionalProperties"] = False
                    if "properties" in params:
                        params["required"] = list(params["properties"].keys())
                patched.append(new_t)
            else:
                patched.append(t)
        return patched
    
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
    
    def __init__(self, model: str = 'gemini-1.5-flash'):
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

    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Implementación de Tool Calling para Gemini"""
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        # Convertir mensajes y herramientas al formato Gemini
        contents = []
        for msg in messages:
            role = "user" if msg["role"] in ["user", "system"] else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
            
        # Convertir tools (formato OpenAI) a Gemini declaration
        gemini_tools = [{"function_declarations": []}]
        for t in tools:
            func = t["function"]
            gemini_tools[0]["function_declarations"].append({
                "name": func["name"],
                "description": func.get("description", ""),
                "parameters": func.get("parameters", {})
            })

        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{self.base_url}/models/{self.model}:generateContent",
                params={"key": self.api_key},
                json={
                    "contents": contents,
                    "tools": gemini_tools,
                    "generationConfig": {"temperature": temperature}
                }
            )
            if response.status_code != 200:
                raise Exception(f"Gemini Tool Error: {response.text}")
            return response.json()
    
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

    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Hugging Face Inference API no soporta Tool Calling nativo fácilmente"""
        raise NotImplementedError("HuggingFace provider does not support native tool calling yet.")
    
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

    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Implementación de Tool Calling para Cohere v1"""
        if not self.api_key:
            raise ValueError("COHERE_API_KEY not configured")
        
        # Convertir mensajes y herramientas al formato Cohere
        message = ""
        chat_history = []
        for msg in messages:
            if msg["role"] == "user":
                message = msg["content"]
            elif msg["role"] == "assistant":
                chat_history.append({"role": "CHATBOT", "message": msg["content"]})
        
        # Convertir tools (OpenAI format) a Cohere tools
        cohere_tools = []
        for t in tools:
            func = t["function"]
            cohere_tools.append({
                "name": func["name"],
                "description": func.get("description", ""),
                "parameter_definitions": {
                    name: {
                        "description": p.get("description", ""),
                        "type": p.get("type", "string"),
                        "required": name in func.get("parameters", {}).get("required", [])
                    }
                    for name, p in func.get("parameters", {}).get("properties", {}).items()
                }
            })

        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{self.base_url}/chat",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "message": message,
                    "chat_history": chat_history,
                    "tools": cohere_tools,
                    "temperature": temperature
                }
            )
            if response.status_code != 200:
                raise Exception(f"Cohere Tool Error: {response.text}")
            return response.json()
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "cohere",
            "model": self.model,
            "speed": "fast",
            "cost": "medium",
            "configured": bool(self.api_key)
        }


class MistralAPIProvider(LLMProvider):
    """Mistral AI API - Modelos potentes como Mistral Large 3"""
    
    def __init__(self, model: str = 'mistral-large-3-latest'):
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

    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 4000,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Implementación de Tool Calling para Mistral"""
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not configured")
        
        payload = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if response_format:
            payload["response_format"] = response_format

        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            if response.status_code != 200:
                raise Exception(f"Mistral Tool Error: {response.text}")
            return response.json()
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "mistral",
            "model": self.model,
            "speed": "fast",
            "cost": "cheap",
            "configured": bool(self.api_key)
        }


class ClaudeProvider(LLMProvider):
    """Anthropic Claude 3.5 Sonnet - El estándar de oro real"""
    
    def __init__(self, model: str = 'claude-3-5-sonnet-20241022'):
        self.model = model
        self.api_key = os.getenv('CLAUDE_API_KEY')
        self.base_url = 'https://api.anthropic.com/v1'
        
        if not self.api_key:
            logger.warning("CLAUDE_API_KEY not found in environment")
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 1.0, # Claude suele preferir temp mas alta
        max_tokens: int = 4000
    ) -> AsyncGenerator[str, None]:
        """Genera respuesta usando Anthropic API (Streaming)"""
        
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY not configured")
        
        # Convertir mensajes (OpenAI -> Anthropic)
        system_prompt = ""
        anthropic_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                anthropic_messages.append({
                    "role": "user" if msg["role"] == "user" else "assistant",
                    "content": msg["content"]
                })
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "system": system_prompt,
                        "messages": anthropic_messages,
                        "stream": True,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        raise Exception(f"Claude API error: {response.status_code} - {error_text}")
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                event = json.loads(line[6:])
                                if event.get("type") == "content_block_delta":
                                    delta = event.get("delta", {})
                                    if delta.get("type") == "text_delta":
                                        yield delta.get("text", "")
                            except json.JSONDecodeError:
                                continue
            
            except Exception as e:
                raise Exception(f"Claude streaming error: {e}")

    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 1.0
    ) -> Dict[str, Any]:
        """Implementación de Tool Calling para Claude"""
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY not configured")
        
        system_prompt = ""
        anthropic_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                anthropic_messages.append({
                    "role": "user" if msg["role"] == "user" else "assistant",
                    "content": msg["content"]
                })
        
        # Formatear tools para Anthropic
        anthropic_tools = []
        for t in tools:
            func = t["function"]
            anthropic_tools.append({
                "name": func["name"],
                "description": func.get("description", ""),
                "input_schema": {
                    "type": "object",
                    "properties": func.get("parameters", {}).get("properties", {}),
                    "required": func.get("parameters", {}).get("required", [])
                }
            })

        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "system": system_prompt,
                    "messages": anthropic_messages,
                    "tools": anthropic_tools,
                    "temperature": temperature,
                    "max_tokens": 4000
                }
            )
            if response.status_code != 200:
                raise Exception(f"Claude Tool Error: {response.text}")
            
            # Normalizar respuesta al formato OpenAI para el Bridge
            data = response.json()
            tool_calls = []
            content = ""
            
            for block in data.get("content", []):
                if block["type"] == "text":
                    content = block["text"]
                elif block["type"] == "tool_use":
                    tool_calls.append({
                        "id": block["id"],
                        "type": "function",
                        "function": {
                            "name": block["name"],
                            "arguments": json.dumps(block["input"])
                        }
                    })
            
            return {
                "choices": [{
                    "message": {
                        "content": content,
                        "tool_calls": tool_calls if tool_calls else None,
                        "role": "assistant"
                    }
                }]
            }
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "claude",
            "model": self.model,
            "speed": "medium",
            "cost": "expensive",
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

    async def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Salamandra VPS no soporta Tool Calling nativo aún"""
        raise NotImplementedError("Salamandra provider does not support native tool calling yet.")
    
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
    'groq-405b': GroqProvider('llama-3.1-405b-instruct-v1:0'), # El "GPT-OSS 120B" de gran escala
    'llama-3.3-70b': GroqProvider('llama-3.3-70b-versatile'),
    
    # DeepSeek (Razonamiento) 🧠
    'deepseek': DeepSeekProvider('deepseek-chat'), 
    'deepseek-reasoner': DeepSeekProvider('deepseek-reasoner'), # DeepSeek R1 (Thinking)
    'deepseek-v3.2': DeepSeekProvider('deepseek-v3.2'), # El nuevo estándar para agentes
    'deepseek-v3': DeepSeekProvider('deepseek-chat'),
    
    # Gemini 🌟
    'gemini-flash': GeminiProvider('gemini-1.5-flash'),
    'gemini-2-flash': GeminiProvider('gemini-2.0-flash-exp'),
    'gemini-pro': GeminiProvider('gemini-1.5-pro'),
    
    # Mistral AI API 🔮 (Prioridad Europea)
    'mistral-large': MistralAPIProvider('mistral-large-latest'),
    'mistral-small': MistralAPIProvider('mistral-small-latest'),
    'mistral-codestral': MistralAPIProvider('codestral-latest'),
    
    # CLAUDE (Anthropic) 🏆
    'claude-4-6-sonnet': ClaudeProvider('claude-3-5-sonnet-20241022'),
    'claude-3-5-haiku': ClaudeProvider('claude-3-5-haiku-20241022'),
    
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
