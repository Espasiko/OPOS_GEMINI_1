"""
Integración MCP con Salamandra
Usa los MCPs locales para memoria y grafo de conocimiento
"""

import sys
import json
import logging
from typing import Dict, Any, List
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_servers.qdrant_memory_local import QdrantMemoryLocal
from mcp_servers.legal_graph_mcp import LegalGraphMCP

logger = logging.getLogger(__name__)


class SalamandraMemoryIntegration:
    """
    Integración de memoria persistente con Salamandra
    """
    
    def __init__(self):
        """Inicializar MCPs"""
        try:
            self.memory_mcp = QdrantMemoryLocal()
            self.graph_mcp = LegalGraphMCP()
            logger.info("✅ MCPs inicializados correctamente")
        except Exception as e:
            logger.error(f"❌ Error inicializando MCPs: {e}")
            self.memory_mcp = None
            self.graph_mcp = None
    
    def save_successful_case(self, caso: Dict[str, Any], coherencia_score: float = 0.95):
        """
        Guarda un caso exitoso en memoria
        
        Args:
            caso: Caso generado por Salamandra
            coherencia_score: Score de coherencia (0-1)
        """
        if not self.memory_mcp or coherencia_score < 0.95:
            return None
        
        try:
            # Extraer info relevante
            enunciado = caso.get('enunciado', '')
            metadata = caso.get('metadata', {})
            calculo = metadata.get('calculo_usado', {})
            
            # Preparar metadata para memoria
            memory_metadata = {
                'base_cotizacion': calculo.get('base_cotizacion', 0),
                'contingencia': calculo.get('contingencia', ''),
                'subsidio_diario': calculo.get('subsidio_diario', 0),
                'coherencia_score': coherencia_score,
                'tema': metadata.get('tema', ''),
                'dificultad': metadata.get('dificultad', 'media')
            }
            
            # Guardar en memoria
            memory_id = self.memory_mcp.add_memory(
                text=enunciado,
                metadata=memory_metadata
            )
            
            logger.info(f"✅ Caso guardado en memoria: {memory_id}")
            return memory_id
        
        except Exception as e:
            logger.error(f"❌ Error guardando caso en memoria: {e}")
            return None
    
    def find_similar_cases(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Busca casos similares en memoria
        
        Args:
            query: Query de búsqueda (ej: "Base 1500€ contingencia EC")
            limit: Número de resultados
        
        Returns:
            Lista de casos similares
        """
        if not self.memory_mcp:
            return []
        
        try:
            results = self.memory_mcp.search_memory(query, limit=limit)
            logger.info(f"✅ Encontrados {len(results)} casos similares")
            return results
        
        except Exception as e:
            logger.error(f"❌ Error buscando casos similares: {e}")
            return []
    
    def get_related_articles(self, article_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene artículos relacionados del grafo legal
        
        Args:
            article_id: ID del artículo (ej: "Art. 173")
        
        Returns:
            Lista de artículos relacionados
        """
        if not self.graph_mcp:
            return []
        
        try:
            related = self.graph_mcp.get_related(article_id)
            logger.info(f"✅ Encontrados {len(related)} artículos relacionados con {article_id}")
            return related
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo artículos relacionados: {e}")
            return []
    
    def enrich_prompt_with_memory(self, base_prompt: str, tema: str, calculo: Dict[str, Any]) -> str:
        """
        Enriquece el prompt con casos similares de memoria
        
        Args:
            base_prompt: Prompt base
            tema: Tema del caso
            calculo: Datos del cálculo
        
        Returns:
            Prompt enriquecido
        """
        if not self.memory_mcp:
            return base_prompt
        
        try:
            # Construir query de búsqueda
            base_cot = calculo.get('base_cotizacion', 0)
            contingencia = calculo.get('contingencia', '')
            query = f"Base {base_cot}€ contingencia {contingencia} {tema}"
            
            # Buscar casos similares
            similar_cases = self.find_similar_cases(query, limit=2)
            
            if not similar_cases:
                return base_prompt
            
            # Añadir casos al prompt
            enriched_prompt = base_prompt + "\n\n## CASOS SIMILARES EXITOSOS (para referencia):\n\n"
            
            for i, case in enumerate(similar_cases, 1):
                enriched_prompt += f"### Caso {i} (Score: {case['score']:.2f}):\n"
                enriched_prompt += f"{case['text'][:300]}...\n"
                enriched_prompt += f"Metadata: {case['metadata']}\n\n"
            
            enriched_prompt += "---\n\nGenera un caso SIMILAR en estructura pero con datos diferentes.\n"
            
            logger.info(f"✅ Prompt enriquecido con {len(similar_cases)} casos similares")
            return enriched_prompt
        
        except Exception as e:
            logger.error(f"❌ Error enriqueciendo prompt: {e}")
            return base_prompt


# Singleton
_memory_integration = None

def get_memory_integration() -> SalamandraMemoryIntegration:
    """Obtener instancia singleton de memoria"""
    global _memory_integration
    if _memory_integration is None:
        _memory_integration = SalamandraMemoryIntegration()
    return _memory_integration


if __name__ == "__main__":
    # Test
    print("=== TEST SALAMANDRA MEMORY INTEGRATION ===\n")
    
    integration = get_memory_integration()
    
    # Test 1: Guardar caso
    print("Test 1: Guardar caso exitoso")
    caso_test = {
        'enunciado': 'María García, trabajadora del Grupo 3, base 1800€, IT por EC, subsidio 36€',
        'metadata': {
            'tema': 'Incapacidad Temporal',
            'dificultad': 'media',
            'calculo_usado': {
                'base_cotizacion': 1800,
                'contingencia': 'EC',
                'subsidio_diario': 36
            }
        }
    }
    
    memory_id = integration.save_successful_case(caso_test, coherencia_score=0.98)
    print(f"Memory ID: {memory_id}\n")
    
    # Test 2: Buscar similares
    print("Test 2: Buscar casos similares")
    similares = integration.find_similar_cases("Base 1800€ contingencia EC", limit=3)
    print(f"Encontrados: {len(similares)} casos")
    for caso in similares:
        print(f"  - Score: {caso['score']:.2f}, Text: {caso['text'][:80]}...\n")
    
    # Test 3: Artículos relacionados
    print("Test 3: Artículos relacionados")
    related = integration.get_related_articles("Art. 173")
    print(f"Relacionados con Art. 173: {len(related)}")
    for art in related[:3]:
        print(f"  - {art['id']} ({art['relation_type']}): {art['name']}\n")
    
    print("✅ TESTS COMPLETADOS")
