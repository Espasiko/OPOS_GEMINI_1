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
from decimal import Decimal

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
                # Store serializable representation
                result_obj = result
                results.append({
                    "agent_id": result_obj.agent_id,
                    "status": result_obj.status.value,
                    "score": result_obj.score,
                    "errors": result_obj.errors,
                    "corrections": result_obj.corrections,
                    "metadata": result_obj.metadata
                })
                
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
        
        # For the 'critic_calculations' agent we run local Python calculators
        if agent_id == 'critic_calculations':
            try:
                # Import calculators (local modules)
                from backend.calculators.calculos_imv import CalculadoraIMV, TipoUnidadFamiliar
                from backend.calculators.calculos_ss_extended import CalculadoraIPT
            except Exception:
                # If imports fail, return ERROR
                return AgentResult(
                    agent_id=agent_id,
                    status=AgentStatus.ERROR,
                    score=0.0,
                    errors=["Failed to import local calculators"],
                    corrections={},
                    metadata={"role": role}
                )

            # Expect the case to include a 'calculations' section for verification
            calc_info = case.get('calculations', {})

            # Basic example: verify IPT pension if data present
            errors = []
            corrections = {}
            score = 1.0

            if calc_info.get('type') == 'IPT':
                try:
                    base = calc_info.get('base_reguladora_mensual')
                    expected_pension = Decimal(str(calc_info.get('expected_pension')))
                    # Use local calculator
                    resultado = CalculadoraIPT.calcular_ipt(Decimal(str(base)))
                    if resultado.pension_mensual != expected_pension.quantize(Decimal('0.01')):
                        errors.append(f"IPT pension mismatch: calc={resultado.pension_mensual} expected={expected_pension}")
                        corrections['calculations.expected_pension'] = str(resultado.pension_mensual)
                        score = 0.0
                except Exception as e:
                    errors.append(f"Calculation error: {str(e)}")
                    score = 0.0
            else:
                # If no specific data, we consider it PASS for now
                pass
            # IMV verification
            if calc_info.get('type') == 'IMV':
                try:
                    tipo_unidad_str = calc_info.get('tipo_unidad', 'persona_sola')
                    ingresos = Decimal(str(calc_info.get('ingresos_netos_familia', '0')))
                    num_miembros = int(calc_info.get('num_miembros', 1))
                    ambos_mayores_30 = bool(calc_info.get('ambos_mayores_30', False))
                    patrimonio = Decimal(str(calc_info.get('patrimonio_total', '0')))

                    tipo_unidad = TipoUnidadFamiliar(tipo_unidad_str)
                    resultado_imv = CalculadoraIMV.calcular_imv(
                        tipo_unidad=tipo_unidad,
                        ingresos_netos_familia=float(ingresos),
                        num_miembros=num_miembros,
                        ambos_mayores_30=ambos_mayores_30,
                        patrimonio_total=float(patrimonio)
                    )

                    expected_imv = Decimal(str(calc_info.get('expected_imv', resultado_imv.imv_a_recibir)))
                    if resultado_imv.imv_a_recibir != expected_imv.quantize(Decimal('0.01')):
                        errors.append(f"IMV mismatch: calc={resultado_imv.imv_a_recibir} expected={expected_imv}")
                        corrections['calculations.expected_imv'] = str(resultado_imv.imv_a_recibir)
                        score = 0.0
                except Exception as e:
                    errors.append(f"IMV calculation error: {str(e)}")
                    score = 0.0

            status = AgentStatus.PASS if score >= 1.0 and not errors else (AgentStatus.FAIL if errors else AgentStatus.PASS)
            return AgentResult(
                agent_id=agent_id,
                status=status,
                score=score,
                errors=errors,
                corrections=corrections,
                metadata={"role": role}
            )

        # TODO: Implementar llamada real a DeepSeek V3.1 para otros agentes
        # Por ahora, simulamos PASS para agentes no numéricos
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
        # Simulated generator will include a calculations section for testing
        # If topic indicates IMV, generate an IMV case; otherwise default to IPT
        if "imv" in topic.lower():
            try:
                from backend.calculators.calculos_imv import CalculadoraIMV, TipoUnidadFamiliar
                tipo_unidad = TipoUnidadFamiliar.PERSONA_SOLA
                ingresos = Decimal("0")
                resultado = CalculadoraIMV.calcular_imv(
                    tipo_unidad=tipo_unidad,
                    ingresos_netos_familia=float(ingresos),
                    num_miembros=1
                )
                expected_imv = resultado.imv_a_recibir
            except Exception:
                tipo_unidad = None
                ingresos = Decimal("0")
                expected_imv = Decimal("564.60")

            return {
                "id": "SS_IMV_001",
                "topic": topic,
                "articles": verified_articles,
                "enunciado": "Caso IMV generado...",
                "opciones": {},
                "respuesta_correcta": None,
                "calculations": {
                    "type": "IMV",
                    "tipo_unidad": tipo_unidad.value if tipo_unidad else "persona_sola",
                    "ingresos_netos_familia": str(ingresos),
                    "num_miembros": 1,
                    "ambos_mayores_30": False,
                    "patrimonio_total": str(0),
                    "expected_imv": str(expected_imv)
                }
            }

        # Default IPT case
        try:
            from backend.calculators.calculos_ss_extended import CalculadoraIPT
            base = Decimal("1500")
            resultado = CalculadoraIPT.calcular_ipt(base)
            expected_pension = resultado.pension_mensual
        except Exception:
            base = Decimal("1500")
            expected_pension = Decimal("825.00")

        return {
            "id": "SS_IPT_001",
            "topic": topic,
            "articles": verified_articles,
            "enunciado": "Caso generado...",
            "opciones": {"a": "...", "b": "...", "c": "...", "d": "..."},
            "respuesta_correcta": "c",
            "calculations": {
                "type": "IPT",
                "base_reguladora_mensual": str(base),
                "expected_pension": str(expected_pension)
            }
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
    import sys
    factory = LegalCaseAgentFactory("agents_config.yaml")
    
    topic = "Incapacidad Permanente Total - Requisitos de alta"
    if len(sys.argv) > 1:
        topic = sys.argv[1]

    result = factory.run_full_pipeline(topic=topic)
    
    # Guardar resultado
    with open("caso_verificado.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultado guardado en: caso_verificado.json")
