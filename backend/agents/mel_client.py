"""
Cliente MEL integrado con RAG y agentes
Compatible con tu stack existente (Qdrant, Salamandra, DeepSeek)
"""

import requests
import logging
from typing import Optional, Dict, Any, List
import json

logger = logging.getLogger(__name__)

class MELClient:
    """Cliente para MEL en Colab/Gradio - Integrado con RAG"""
    
    def __init__(self, gradio_url: str):
        """
        Args:
            gradio_url: URL pública de Gradio (ej: https://xxxxx.gradio.live)
        """
        self.base_url = gradio_url.rstrip('/')
        self.api_endpoint = f"{self.base_url}/api/predict"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def generate(
        self, 
        prompt: str, 
        max_length: int = 300,
        temperature: float = 0.7,
        top_p: float = 0.95,
        timeout: int = 60
    ) -> Optional[str]:
        """
        Genera respuesta con MEL
        
        Compatible con tu arquitectura de agentes existente
        """
        try:
            # Payload para Gradio API
            payload = {
                "data": [prompt, max_length, temperature, top_p]
            }
            
            logger.info(f"📤 Enviando a MEL: {prompt[:50]}...")
            
            response = self.session.post(
                self.api_endpoint,
                json=payload,
                timeout=timeout
            )
            
            response.raise_for_status()
            
            # Gradio devuelve: {"data": ["respuesta generada"]}
            result = response.json()
            generated_text = result.get("data", [None])[0]
            
            if generated_text:
                logger.info(f"✅ MEL respondió: {len(generated_text)} caracteres")
                return generated_text
            else:
                logger.error("❌ Respuesta vacía de MEL")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"⏰ Timeout después de {timeout}s")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error de conexión: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            return None
    
    def health_check(self) -> bool:
        """Verifica si MEL está disponible"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_with_rag(
        self,
        question: str,
        rag_context: str,
        max_length: int = 400,
        temperature: float = 0.5
    ) -> Optional[str]:
        """
        Genera respuesta combinando RAG + MEL
        
        Integración con tu sistema Qdrant existente
        """
        # Construir prompt con contexto RAG
        prompt = f"""Responde SOLO en español basándote en el contexto legal proporcionado.

### CONTEXTO LEGAL:
{rag_context}

### PREGUNTA:
{question}

### RESPUESTA (en español, basada en el contexto):"""
        
        return self.generate(
            prompt=prompt,
            max_length=max_length,
            temperature=temperature,
            top_p=0.9
        )
    
    def generate_caso_practico(
        self,
        tema: str,
        contexto_legal: str,
        dificultad: str = "media"
    ) -> Optional[Dict[str, Any]]:
        """
        Genera caso práctico de oposición con MEL
        
        Compatible con tu sistema de generación de casos
        """
        prompt = f"""Responde SOLO en español. Genera un caso práctico de oposición.

TEMA: {tema}
DIFICULTAD: {dificultad}

CONTEXTO LEGAL:
{contexto_legal}

Genera un caso práctico con:
1. Enunciado realista (situación laboral concreta)
2. Pregunta específica
3. 4 opciones (a, b, c, d)
4. Respuesta correcta
5. Explicación detallada con citas legales

Formato JSON:
{{
  "enunciado": "...",
  "pregunta": "...",
  "opciones": {{"a": "...", "b": "...", "c": "...", "d": "..."}},
  "respuesta_correcta": "a/b/c/d",
  "explicacion": "..."
}}

Respuesta en español:"""
        
        respuesta = self.generate(
            prompt=prompt,
            max_length=600,
            temperature=0.8
        )
        
        if respuesta:
            try:
                # Intentar parsear JSON
                caso = json.loads(respuesta)
                return caso
            except json.JSONDecodeError:
                logger.warning("⚠️ MEL no devolvió JSON válido")
                return {
                    "raw_response": respuesta,
                    "modelo": "MEL",
                    "parsed": False
                }
        
        return None


# Ejemplo de uso con tu stack
if __name__ == "__main__":
    import sys
    
    # URL de Gradio (actualizar con la tuya)
    GRADIO_URL = "https://xxxxx.gradio.live"  # 👈 CAMBIAR
    
    mel = MELClient(GRADIO_URL)
    
    # Test 1: Health check
    print("🔍 Verificando conexión a MEL...")
    if not mel.health_check():
        print("❌ No se pudo conectar a MEL")
        print("💡 Asegúrate de:")
        print("   1. Tener Colab corriendo")
        print("   2. Actualizar GRADIO_URL con la URL correcta")
        sys.exit(1)
    
    print("✅ MEL conectado\n")
    
    # Test 2: Pregunta simple
    print("="*60)
    print("🧪 TEST 1: Pregunta simple")
    print("="*60)
    
    respuesta = mel.generate(
        prompt="¿Qué es la incapacidad temporal?",
        max_length=200,
        temperature=0.7
    )
    
    if respuesta:
        print(f"\n🤖 MEL:\n{respuesta}\n")
    
    # Test 3: Con contexto RAG (simulado)
    print("="*60)
    print("🧪 TEST 2: MEL + RAG")
    print("="*60)
    
    contexto_rag = """
    Art. 173 LGSS: La prestación económica por IT consiste en un subsidio 
    que se abonará durante los días de baja. 
    
    Para enfermedad común (EC):
    - Días 1-3: 0% (sin subsidio)
    - Días 4-20: 60% de la base reguladora
    - Día 21 en adelante: 75% de la base reguladora
    
    Base reguladora: Base de cotización del mes anterior / 30 días
    """
    
    respuesta_rag = mel.generate_with_rag(
        question="Un trabajador con base de 1.500€/mes está de baja por EC. ¿Cuánto cobra el día 15?",
        rag_context=contexto_rag,
        temperature=0.3
    )
    
    if respuesta_rag:
        print(f"\n🔍 MEL + RAG:\n{respuesta_rag}\n")
    
    # Test 4: Generar caso práctico
    print("="*60)
    print("🧪 TEST 3: Generar caso práctico")
    print("="*60)
    
    caso = mel.generate_caso_practico(
        tema="Incapacidad Temporal por Enfermedad Común",
        contexto_legal=contexto_rag,
        dificultad="media"
    )
    
    if caso:
        print(f"\n📝 Caso generado:")
        print(json.dumps(caso, indent=2, ensure_ascii=False))
    
    print("\n" + "="*60)
    print("✅ TESTS COMPLETADOS")
    print("="*60)
