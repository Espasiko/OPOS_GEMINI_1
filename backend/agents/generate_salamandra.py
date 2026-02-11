"""
Generador de Casos Prácticos con Salamandra
Con integración de memoria MCP para aprendizaje
"""
import json
import logging
import yaml
from pathlib import Path
from typing import Dict, Any
from .salamandra_client import get_salamandra_client
from .salamandra_memory import get_memory_integration

logger = logging.getLogger(__name__)


class SalamandraGenerator:
    """
    Generador de casos prácticos usando Salamandra
    """
    
    def __init__(self):
        self.client = get_salamandra_client()
        
        # Integración de memoria MCP
        try:
            self.memory = get_memory_integration()
            logger.info("✅ Memoria MCP integrada")
        except Exception as e:
            logger.warning(f"⚠️ Memoria MCP no disponible: {e}")
            self.memory = None
        
        # Cargar prompts desde YAML
        config_path = Path(__file__).parent.parent / "config" / "prompts" / "salamandra.yaml"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        self.prompts = config['prompts']
        logger.info(f"✅ SalamandraGenerator initialized")
    
    async def generate_case(
        self,
        tema: str,
        articulos_texto: str = None,
        calculo_json: Dict[str, Any] = None,
        dificultad: str = "media"
    ) -> Dict[str, Any]:
        """
        Genera un caso práctico
        
        Args:
            tema: Tema del caso
            articulos_texto: Artículos legales (opcional, se buscan en RAG si no se proveen)
            calculo_json: Resultado de la calculadora
            dificultad: Nivel de dificultad
        
        Returns:
            Caso práctico en formato JSON
        """
        # Si no hay artículos, buscar en RAG
        if not articulos_texto:
            logger.info("No articles provided, searching in RAG...")
            from .rag_helper import get_rag_helper
            
            rag = get_rag_helper()
            articles = rag.search_articles(tema, limit=3)
            articulos_texto = rag.format_articles_for_prompt(articles)
            logger.info(f"Found {len(articles)} articles from RAG")
        
        # Preparar prompts
        system_prompt = self.prompts['generate_case']['system']
        
        user_prompt = self.prompts['generate_case']['user'].format(
            tema=tema,
            articulos_texto=articulos_texto,
            calculo_json=json.dumps(calculo_json, indent=2, ensure_ascii=False)
        )
        
        # Enriquecer con memoria MCP si está disponible
        if self.memory:
            user_prompt = self.memory.enrich_prompt_with_memory(
                user_prompt, tema, calculo_json
            )
            logger.info("✅ Prompt enriquecido con memoria MCP")
        
        logger.info(f"Generating case for tema: {tema}")
        
        # Generar con Salamandra
        try:
            response_text = await self.client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=1500
            )
            
            logger.info(f"Raw response (first 500 chars): {response_text[:500]}")
            
            # Limpiar respuesta
            clean_text = self._clean_json_response(response_text)
            
            # Parsear JSON
            caso = json.loads(clean_text)
            
            # Validar estructura
            self._validate_case_structure(caso)
            
            # Añadir metadata
            caso['metadata'] = {
                'modelo': 'salamandra-7b-instruct',
                'tema': tema,
                'dificultad': dificultad,
                'calculo_usado': calculo_json
            }
            
            logger.info("✅ Case generated successfully")
            return caso
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            logger.error(f"Clean text: {clean_text[:1000]}")
            raise ValueError(f"Salamandra no generó JSON válido: {e}")
        
        except Exception as e:
            logger.error(f"Error generating case: {e}")
            raise
    
    def _clean_json_response(self, response: str) -> str:
        """Limpia la respuesta para extraer JSON válido"""
        clean = response.strip()
        
        # Remover markdown
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0]
        elif "```" in clean:
            parts = clean.split("```")
            if len(parts) >= 3:
                clean = parts[1]
        
        clean = clean.strip()
        
        # Buscar inicio y fin de JSON
        if not clean.startswith("{"):
            start_idx = clean.find("{")
            if start_idx != -1:
                clean = clean[start_idx:]
        
        if not clean.endswith("}"):
            end_idx = clean.rfind("}")
            if end_idx != -1:
                clean = clean[:end_idx+1]
        
        return clean
    
    def _validate_case_structure(self, caso: Dict[str, Any]) -> None:
        """Valida que el caso tenga la estructura correcta"""
        required_fields = [
            'enunciado',
            'pregunta',
            'opciones',
            'respuesta_correcta',
            'explicacion'
        ]
        
        for field in required_fields:
            if field not in caso:
                raise ValueError(f"Campo requerido faltante: {field}")
        
        # Validar opciones
        if not isinstance(caso['opciones'], dict):
            raise ValueError("'opciones' debe ser un dict")
        
        if set(caso['opciones'].keys()) != {'A', 'B', 'C', 'D'}:
            raise ValueError("'opciones' debe tener exactamente A, B, C, D")
        
        # Validar respuesta correcta
        if caso['respuesta_correcta'] not in ['A', 'B', 'C', 'D']:
            raise ValueError("'respuesta_correcta' debe ser A, B, C o D")


def get_salamandra_generator() -> SalamandraGenerator:
    """
    Get a new generator instance.
    
    NOTE: Durante desarrollo, creamos una nueva instancia cada vez
    para evitar problemas de caché de Python. En producción,
    se puede volver a usar el patrón singleton si es necesario.
    """
    return SalamandraGenerator()
