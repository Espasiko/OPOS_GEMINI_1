import re
with open('/home/spas/OPOS_GEMINI_1/backend/agents/verification_agents.py', 'r') as f:
    text = f.read()

# 1. Reemplazamos Agent5
idx5 = text.find('class Agent5_TrapPedagogy(VerificationAgent):')
idx7 = text.find('class Agent7_InterdependenciaValidator(VerificationAgent):')
if idx5 == -1 or idx7 == -1:
    print('No se encontró Agent5 o Agent7')
    exit(1)

agent5_new = '''class Agent5_TrapPedagogy(VerificationAgent):
    """Verifica: ¿La explicación / razonamiento revela dónde está la trampa?"""
    
    def __init__(self):
        super().__init__("agent_5", "Trap Pedagogy (Explicación)")
    
    def verify(self, caso: Dict[str, Any]) -> VerificationResult:
        feedback = []
        detalles = {}
        
        preguntas = caso.get("preguntas", [])
        if not preguntas:
            return self._crear_resultado(1.0, ["⚠️ Sin preguntas - saltando"])
            
        preguntas_con_explicacion = 0
        
        for q in preguntas:
            razonamiento = str(q.get("razonamiento", "")).lower()
            if not razonamiento:
                continue
                
            is_pedagogico = any(kw in razonamiento for kw in [
                "no es", "sino", "trampa", "confusión", "falso", "incorrecto", 
                "excepción", "sin embargo", "a diferencia de", "ojo", "cuidado"
            ])
            if is_pedagogico:
                preguntas_con_explicacion += 1
                
        ratio = preguntas_con_explicacion / max(len(preguntas), 1)
        detalles["preguntas_pedagogicas"] = preguntas_con_explicacion
        
        if ratio >= 0.7:
            feedback.append(f"✅ Excelente pedagogía ({ratio:.0%} explican la trampa)")
        elif ratio >= 0.4:
            feedback.append(f"⚠️ Pedagogía media ({ratio:.0%} explican la trampa)")
        else:
            feedback.append(f"❌ Pedagogía pobre ({ratio:.0%} de explicaciones). Razonamientos planos.")
            
        return self._crear_resultado(ratio, feedback, detalles)

# ============================================================================
# AGENT 7: INTERDEPENDENCIA VALIDATOR - Valida que preguntas usen enunciado
# ============================================================================

'''

text = text[:idx5] + agent5_new + text[idx7:]

# 2. Add Agent8 & update Orchestrator
idx_orch = text.find('class VerificationOrchestrator:')

tail_new = '''# ============================================================================
# AGENT 8: TRAP DISTRACTOR - Evalúa la calidad de las opciones incorrectas
# ============================================================================

class Agent8_TrapDistractorValidator(VerificationAgent):
    """Verifica: ¿Los distractores son plausibles tipológicamente?"""
    
    def __init__(self):
        super().__init__("agent_8", "Trap Distractor (Opciones)")
        
    def verify(self, caso: Dict[str, Any]) -> VerificationResult:
        feedback = []
        detalles = {}
        
        preguntas = caso.get("preguntas", [])
        if not preguntas:
            return self._crear_resultado(1.0, ["⚠️ Sin preguntas"])
            
        preguntas_plausibles = 0
        
        import re
        for q in preguntas:
            correcta = str(q.get("respuesta_correcta", "")).lower()
            distractores = [str(d).lower() for d in q.get("distractores", [])]
            
            if not distractores:
                continue
                
            tiene_numeros = bool(re.search(r"\\d+", correcta))
            tiene_porcentajes = "%" in correcta
            
            distractores_homogeneos = 0
            for d in distractores:
                d_tiene_num = bool(re.search(r"\\d+", d))
                d_tiene_pct = "%" in d
                if (tiene_numeros == d_tiene_num) and (tiene_porcentajes == d_tiene_pct):
                    distractores_homogeneos += 1
                    
            if distractores_homogeneos >= len(distractores) / 2:
                preguntas_plausibles += 1
                
        ratio = preguntas_plausibles / max(len(preguntas), 1)
        detalles["preguntas_plausibles"] = preguntas_plausibles
        
        if ratio >= 0.8:
            feedback.append(f"✅ Distractores plausibles ({ratio:.0%})")
        else:
            feedback.append(f"⚠️ Distractores de plausibilidad baja ({ratio:.0%})")
            
        return self._crear_resultado(ratio, feedback, detalles)

# ============================================================================
# ORQUESTADOR DE VERIFICADORES (V14 Unificado)
# ============================================================================

class VerificationOrchestrator:
    """Ejecuta los agentes V14 y consolida resultados"""
    
    def __init__(self):
        self.agentes = [
            Agent1_BOEVerifier(),
            Agent2_LegalReasoner(),
            Agent3_Calculator(),
            Agent4_Coherence(),
            Agent5_TrapPedagogy(),
            Agent7_InterdependenciaValidator(),
            Agent8_TrapDistractorValidator()
        ]
    
    def verify_caso_completo(self, caso: Dict[str, Any], verbose: bool = True) -> Dict[str, Any]:
        resultados = {}
        scores = []
        
        import logging
        logger = logging.getLogger(__name__)
        
        for agente in self.agentes:
            try:
                resultado = agente.verify(caso)
                resultados[agente.agent_id] = resultado.to_dict()
                scores.append(resultado.score)
                
                if verbose:
                    status_icon = "✅" if resultado.status == "PASS" else ("⚠️" if resultado.score >= 0.5 else "❌")
                    logger.info(f"{status_icon} {resultado.agent_name}: {resultado.score:.0%}")
                    for fb in resultado.feedback[:2]:
                        logger.info(f"   {fb}")
            except Exception as e:
                logger.error(f"Error en {agente.agent_name}: {e}")
                scores.append(0.0)
        
        score_promedio = sum(scores) / len(scores) if scores else 0.0
        todos_pasaron = all(s >= 0.70 for s in scores)
        
        return {
            "resultados_agentes": resultados,
            "score_promedio": score_promedio,
            "todos_pasaron": todos_pasaron,
            "status": "APROBADO" if todos_pasaron else "PENDIENTE_REVISION",
        }
        
if __name__ == "__main__":
    print("Módulo verification_agents.py V14 refactorizado OK")
'''

text = text[:idx_orch] + tail_new

with open('/home/spas/OPOS_GEMINI_1/backend/agents/verification_agents.py', 'w') as f:
    f.write(text)
print("Patch OK")
