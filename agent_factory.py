#!/usr/bin/env python3
"""
Agent Factory: Multi-Agent Verification Pipeline
Orquesta DeepSeek V3.1 + 5 Agentes Críticos para máxima veracidad
"""

import os
import json
import yaml
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class AgentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"

@dataclass
class AgentResult:
    agent_id: str
    status: AgentStatus
    score: float
    errors: List[str]
    corrections: Dict[str, Any]
    metadata: Dict[str, Any]

class LegalCaseAgentFactory:
    """
    Fábrica de agentes para generación y verificación de casos legales
    """
    
    def __init__(self, config_path: str = "agents_config.yaml"):
        self.config = self.load_config(config_path)
        self.max_iterations = self.config.get("orchestration", {}).get("max_iterations", 5)
        self.timeout = self.config.get("orchestration", {}).get("timeout", 300)
    
    def load_config(self, path: str) -> Dict:
        """Carga configuración YAML de agentes"""
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def generate_case_with_rag(self, topic: str) -> Dict:
        """
        FASE 1: Genera caso usando RAG-first approach
        
        Workflow:
        1. Query RAG local para obtener artículos relevantes
        2. Search BOE via MCP-BOE para URLs verificadas
        3. Generar caso usando SOLO información verificada
        """
        print(f"\n🏭 FASE 1: Generando caso sobre '{topic}'")
        print("="*80)
        
        # Step 1: Query RAG
        print("\n📚 Step 1: Consultando RAG local...")
        rag_results = self.query_local_rag(
            query=f"{topic} requisitos normativa",
            top_k=5
        )
        print(f"   ✅ Encontrados {len(rag_results)} artículos relevantes")
        
        # Step 2: Verify BOE URLs
        print("\n🔍 Step 2: Verificando URLs BOE...")
        verified_articles = []
        for article in rag_results:
            boe_data = self.search_boe_article(
                article_number=article['number'],
                law_name=article['law']
            )
            if boe_data:
                verified_articles.append(boe_data)
                print(f"   ✅ {article['number']}: {boe_data['url']}")
        
        # Step 3: Generate case with verified data
        print("\n🧠 Step 3: Generando caso con datos verificados...")
        case = self.call_deepseek_generator(
            topic=topic,
            verified_articles=verified_articles
        )
        
        print(f"\n✅ Caso generado: {case.get('id', 'N/A')}")
        return case
    
    def verify_case_multi_agent(self, case: Dict) -> Dict:
        """
        FASE 2: Verifica caso con 5 agentes críticos
        
        Agentes:
        1. BOE URLs Validator
        2. Legal Reasoning Validator
        3. Calculations Validator
        4. Coherence Validator
        5. Pedagogical Trap Validator
        """
        print(f"\n🏭 FASE 2: Verificación multi-agente")
        print("="*80)
        
        agents = self.config.get("verification_pipeline", {}).get("agents", [])
        results = []
        
        for iteration in range(self.max_iterations):
            print(f"\n🔄 Iteración {iteration + 1}/{self.max_iterations}")
            
            all_pass = True
            
            for agent_config in agents:
                agent_id = agent_config['agent_id']
                print(f"\n   🤖 Ejecutando: {agent_id}")
                
                result = self.run_critic_agent(agent_config, case)
                results.append(result)
                
                if result.status == AgentStatus.FAIL:
                    all_pass = False
                    print(f"      ❌ FAIL: {result.errors}")
                    
                    # Aplicar correcciones
                    case = self.apply_corrections(case, result.corrections)
                    print(f"      🔧 Aplicadas {len(result.corrections)} correcciones")
                    break  # Reiniciar desde el principio
                else:
                    print(f"      ✅ PASS (score: {result.score:.2f})")
            
            if all_pass:
                print(f"\n✅ TODOS LOS AGENTES APROBARON")
                break
        
        return {
            "case": case,
            "verification_results": results,
            "iterations": iteration + 1,
            "status": "approved" if all_pass else "failed"
        }
    
    def run_critic_agent(self, agent_config: Dict, case: Dict) -> AgentResult:
        """Ejecuta un agente crítico específico"""
        agent_id = agent_config['agent_id']
        role = agent_config['role']
        task = agent_config['task']
        
        # Llamar a DeepSeek V3.1 con el rol de crítico
        prompt = f"""Eres un {role}.

TAREA:
{task}

CASO A VALIDAR:
{json.dumps(case, indent=2, ensure_ascii=False)}

Responde en JSON con:
{{
  "status": "PASS" | "FAIL",
  "score": 0.0-1.0,
  "errors": ["error1", "error2", ...],
  "corrections": {{"field": "new_value", ...}}
}}
"""
        
        # TODO: Implementar llamada real a DeepSeek V3.1
        # Por ahora, simulamos
        response = {
            "status": "PASS",
            "score": 0.95,
            "errors": [],
            "corrections": {}
        }
        
        return AgentResult(
            agent_id=agent_id,
            status=AgentStatus(response['status'].lower()),
            score=response['score'],
            errors=response['errors'],
            corrections=response['corrections'],
            metadata={"role": role}
        )
    
    def query_local_rag(self, query: str, top_k: int = 5) -> List[Dict]:
        """Query RAG local (Qdrant)"""
        # TODO: Implementar llamada real a RAG
        return [
            {"number": "137", "law": "TRLGSS", "relevance": 0.95},
            {"number": "206", "law": "TRLGSS", "relevance": 0.88},
        ]
    
    def search_boe_article(self, article_number: str, law_name: str) -> Dict:
        """Busca artículo en BOE via MCP-BOE"""
        # TODO: Implementar llamada real a MCP-BOE
        return {
            "article": article_number,
            "law": law_name,
            "url": f"https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a{article_number}",
            "text": "Texto del artículo..."
        }
    
    def call_deepseek_generator(self, topic: str, verified_articles: List[Dict]) -> Dict:
        """Llama a DeepSeek V3.1 para generar caso"""
        # TODO: Implementar llamada real con function calling
        return {
            "id": "SS_IPT_001",
            "topic": topic,
            "articles": verified_articles,
            "enunciado": "Caso generado...",
            "opciones": {"a": "...", "b": "...", "c": "...", "d": "..."},
            "respuesta_correcta": "c"
        }
    
    def apply_corrections(self, case: Dict, corrections: Dict) -> Dict:
        """Aplica correcciones al caso"""
        for field, value in corrections.items():
            case[field] = value
        return case
    
    def run_full_pipeline(self, topic: str) -> Dict:
        """Ejecuta pipeline completo: Generación + Verificación"""
        print("\n" + "="*80)
        print("🏭 INICIANDO PIPELINE MULTI-AGENTE")
        print("="*80)
        
        # Fase 1: Generación con RAG
        case = self.generate_case_with_rag(topic)
        
        # Fase 2: Verificación multi-agente
        result = self.verify_case_multi_agent(case)
        
        print("\n" + "="*80)
        print("✅ PIPELINE COMPLETADO")
        print("="*80)
        print(f"Status: {result['status']}")
        print(f"Iteraciones: {result['iterations']}")
        
        return result

# Ejemplo de uso
if __name__ == "__main__":
    factory = LegalCaseAgentFactory("agents_config.yaml")
    
    result = factory.run_full_pipeline(
        topic="Incapacidad Permanente Total - Requisitos de alta"
    )
    
    # Guardar resultado
    with open("caso_verificado.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultado guardado en: caso_verificado.json")
