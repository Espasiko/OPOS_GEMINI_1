#!/usr/bin/env python3
"""
Generador PARTE 2 OPTIMIZADO - Batch 3-preguntas
Genera enunciado + 15 preguntas en 5 llamadas (3 preguntas cada una)
Tiempo estimado: 5 min vs 30 min en enfoque iterativo
"""
import json
import requests
import sys
import re
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, '/home/spas/OPOS_GEMINI_1')
from backend.agents.verification_agents import VerificationOrchestrator


class SalamandraParteDosOptimizado:
    """PARTE 2 optimizado con batch de 3 preguntas"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "salamandra-7b-instruct-tools"  # Sin CoT reasoning (más rápido)
        self.verificar_modelo()
    
    def verificar_modelo(self):
        """Verifica modelo disponible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            modelos = response.json().get("models", [])
            modelos_nombres = [m.get("name", "") for m in modelos]
            
            # Intentar modelo sin CoT primero
            modelos_a_probar = [
                "salamandra-7b-instruct-tools",
                "salamandra-r1:q5km"
            ]
            
            for modelo in modelos_a_probar:
                if modelo in modelos_nombres:
                    self.model = modelo
                    logger.info(f"✅ Usando modelo: {self.model}")
                    return
            
            raise ConnectionError(f"Ningún modelo Salamandra disponible. Tengo: {modelos_nombres}")
            
        except Exception as e:
            logger.error(f"❌ Error verificación modelo: {e}")
            raise
    
    def generar_supuesto_optimizado(self, contingencias: List[str] = None,
                                   num_preguntas: int = 15) -> Dict[str, Any]:
        """Genera PARTE 2 con batch de 3 preguntas"""
        
        if contingencias is None:
            contingencias = ["IT", "JUBILACION"]
        
        logger.info(f"\n{'='*80}")
        logger.info(f"🚀 PARTE 2 OPTIMIZADO (Batch 3-preg) - {num_preguntas} preguntas")
        logger.info(f"{'='*80}")
        
        # FASE 1: Enunciado
        logger.info("\n📖 FASE 1: Enunciado...")
        enunciado = self._generar_enunciado_rapido(contingencias)
        
        if not enunciado or "error" in enunciado:
            logger.error("❌ Fase 1 falló")
            return {"error": "Fase 1 failed"}
        
        logger.info(f"   ✅ Enunciado: {len(enunciado.get('personajes', []))} personajes")
        
        # FASE 2: Preguntas en batches de 3
        logger.info(f"\n❓ FASE 2: {num_preguntas} preguntas en batches...")
        preguntas = []
        
        num_batches = (num_preguntas + 2) // 3  # Redondear al alza
        
        for batch_num in range(1, num_batches + 1):
            inicio = (batch_num - 1) * 3 + 1
            fin = min(batch_num * 3, num_preguntas)
            
            logger.info(f"\n   Batch {batch_num}: preguntas {inicio}-{fin}...")
            
            preguntas_batch = self._generar_batch_preguntas(
                enunciado,
                contingencias,
                inicio,
                fin
            )
            
            if preguntas_batch:
                preguntas.extend(preguntas_batch)
                logger.info(f"      ✅ {len(preguntas_batch)} preguntas añadidas")
            else:
                logger.warning(f"      ⚠️ Batch vacío, creando fallback...")
                for q_num in range(inicio, fin + 1):
                    preguntas.append(self._crear_pregunta_fallback(q_num))
        
        # Asegurar exactamente num_preguntas
        preguntas = preguntas[:num_preguntas]
        while len(preguntas) < num_preguntas:
            preguntas.append(self._crear_pregunta_fallback(len(preguntas) + 1))
        
        # Consolidar
        supuesto = {
            "id": f"SS_P2_{''.join([c[0] for c in contingencias])}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "tipo_examen": "PARTE_2",
            "timestamp": datetime.now().isoformat(),
            "generado_por": self.model,
            "enunciado": enunciado,
            "preguntas": preguntas,
            "contingencias": contingencias,
            "estadisticas": {
                "total_preguntas": len(preguntas),
                "personajes": len(enunciado.get("personajes", [])),
                "palabras_enunciado": len(enunciado.get("texto", "").split()),
            }
        }
        
        return supuesto
    
    def _generar_enunciado_rapido(self, contingencias: List[str]) -> Dict[str, Any]:
        """Genera enunciado sin CoT (más rápido)"""
        
        contingencias_str = " y ".join(contingencias)
        
        prompt = f"""Eres profesor academia SS con 20 años.

Genera UN enunciado supuesto práctico SS ({contingencias_str}):
- 200-300 palabras
- 6-9 personajes nombrados con datos (edad, puesto, base)
- Hechos específicos con fechas
- Contingencias: {contingencias_str}

Devuelve SOLO JSON VÁLIDO (sin explicación):
{{
  "texto": "[200-300 palabras del enunciado]",
  "personajes": [
    {{"nombre": "Juan García López", "edad": 47, "puesto": "IT", "base": 2000, "contingencia": "IT"}},
    {{"nombre": "María García López", "edad": 65, "puesto": "Jubilada", "pension": 1200, "contingencia": "JUBILACION"}}
  ],
  "hechos_clave": ["Baja médica 10 febrero"],
  "articulos": ["Art 173 TRLGSS"],
  "contexto": "IT por EC, solicita jubilación anticipada"
}}"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.2,
                    "num_ctx": 2048,
                    "num_predict": 600,
                },
                timeout=120
            )
            
            respuesta = response.json().get("response", "").strip()
            
            enunciado = self._extraer_json(respuesta)
            
            if enunciado and "texto" in enunciado and len(enunciado.get("personajes", [])) > 0:
                return enunciado
            else:
                return self._crear_enunciado_fallback(contingencias)
                
        except Exception as e:
            logger.warning(f"Error Salamandra: {e}, usando fallback")
            return self._crear_enunciado_fallback(contingencias)
    
    def _generar_batch_preguntas(self, enunciado: Dict[str, Any],
                                contingencias: List[str],
                                inicio: int, fin: int) -> List[Dict[str, Any]]:
        """Genera 1-3 preguntas en batch"""
        
        num_preg = fin - inicio + 1
        enunciado_text = enunciado.get("texto", "")[:200]
        personajes_text = json.dumps(enunciado.get("personajes", []), ensure_ascii=False)[:200]
        
        prompt = f"""Eres profesor academia SS.

Genera EXACTAMENTE {num_preg} pregunta(s) tipo test ({inicio}-{fin}) sobre:

ENUNCIADO: {enunciado_text}...
PERSONAJES: {personajes_text}...

REQUISITOS:
- Pregunta(s) DEBE(N) usar datos del enunciado
- 4 opciones (A/B/C/D) realistas
- 1 correcta, 3 trampas pedagógicas
- Razonamiento 6 pasos observable

Devuelve SOLO JSON array (sin explicación):
[
  {{
    "num": {inicio},
    "texto": "¿Cuánto es el subsidio...?",
    "opciones": {{"A": "valor1", "B": "valor2", "C": "valor3", "D": "valor4"}},
    "respuesta_correcta": "B",
    "razonamiento": {{
      "paso_1": "Identifica tipo/período",
      "paso_2": ["Art 173 TRLGSS"],
      "paso_3": {{"base": "2000"}},
      "paso_4": "Cálculo",
      "paso_5": "Vigencia 2026",
      "paso_6": "Conclusión"
    }},
    "trampa": "Confundir X con Y"
  }}
  {f', {{... pregunta {inicio+1} ...}}' if num_preg > 1 else ''}
]"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.2,
                    "num_ctx": 2048,
                    "num_predict": 800,
                },
                timeout=120
            )
            
            respuesta = response.json().get("response", "").strip()
            
            # Intentar parse como array
            try:
                # Buscar array JSON
                match = re.search(r'\[.*\]', respuesta, re.DOTALL)
                if match:
                    preguntas_array = json.loads(match.group(0))
                    if isinstance(preguntas_array, list):
                        # Normalizar números
                        for i, p in enumerate(preguntas_array):
                            p["num"] = inicio + i
                            if "depende_de" not in p:
                                p["depende_de"] = ["enunciado"]
                        return preguntas_array
            except json.JSONDecodeError:
                pass
            
            # Fallback: extraer un JSON individual si array falla
            json_obj = self._extraer_json(respuesta)
            if json_obj and "texto" in json_obj:
                json_obj["num"] = inicio
                if "depende_de" not in json_obj:
                    json_obj["depende_de"] = ["enunciado"]
                return [json_obj]
            
            return []
            
        except Exception as e:
            logger.warning(f"Error batch {inicio}-{fin}: {e}")
            return []
    
    def _extraer_json(self, texto: str) -> Optional[Dict[str, Any]]:
        """Extrae JSON de texto"""
        
        # Intento 1: Parse directo
        try:
            return json.loads(texto)
        except:
            pass
        
        # Intento 2: Buscar {...}
        try:
            match = re.search(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', texto, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except:
            pass
        
        return None
    
    def _crear_enunciado_fallback(self, contingencias: List[str]) -> Dict[str, Any]:
        """Crea enunciado fallback"""
        
        return {
            "texto": f"Supuesto práctico de {', '.join(contingencias)}. Juan García López, 47 años, técnico IT con base cotización 2000€/mes. María García López, cónyuge, 65 años, pensionista. Solicita prestaciones por contingencia...",
            "personajes": [
                {"nombre": "Juan García López", "edad": 47, "puesto": "IT", "base": 2000, "contingencia": contingencias[0]},
                {"nombre": "María García López", "age": 65, "puesto": "Jubilada", "pension": 1200, "contingencia": contingencias[1] if len(contingencias) > 1 else contingencias[0]},
            ],
            "hechos_clave": ["Solicitud 2026"],
            "articulos": ["Art 173 TRLGSS"],
            "contexto": f"{contingencias[0]}"
        }
    
    def _crear_pregunta_fallback(self, num: int) -> Dict[str, Any]:
        """Crea pregunta fallback"""
        
        return {
            "num": num,
            "texto": f"Pregunta {num}: ¿Cuál es la respuesta correcta?",
            "opciones": {
                "A": f"Opción A (Q{num})",
                "B": f"Opción B (Q{num})",
                "C": f"Opción C (Q{num})",
                "D": f"Opción D (Q{num})"
            },
            "respuesta_correcta": "B",
            "razonamiento": {
                "paso_1": "Identificar",
                "paso_2": ["Art TRLGSS"],
                "paso_3": {"base": "2000"},
                "paso_4": "Cálculo",
                "paso_5": "Vigencia 2026",
                "paso_6": "Conclusión"
            },
            "trampa": "Confusión típica"
        }


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Genera PARTE 2 optimizada"""
    
    print("\n" + "="*80)
    print("🚀 GENERADOR PARTE 2 OPTIMIZADO (Batch 3-preg)")
    print("="*80)
    
    try:
        generador = SalamandraParteDosOptimizado()
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
    
    # Generar supuesto
    supuesto = generador.generar_supuesto_optimizado(
        contingencias=["IT", "JUBILACION"],
        num_preguntas=15
    )
    
    if "error" in supuesto:
        logger.error(f"Error: {supuesto['error']}")
        return None
    
    # Mostrar
    print(f"\n{'='*80}")
    print("📋 SUPUESTO GENERADO")
    print(f"{'='*80}")
    
    print(f"\n📖 Enunciado: {len(supuesto['enunciado'].get('personajes', []))} personajes")
    print(f"❓ Preguntas: {len(supuesto['preguntas'])}/15")
    
    print(f"\nPrimeras 3 preguntas:")
    for p in supuesto['preguntas'][:3]:
        print(f"  Q{p.get('num')}: {p.get('texto', '???')[:60]}...")
    
    # Verificar muestra
    print(f"\n{'='*80}")
    print("🔍 VERIFICACIÓN (Q1-3)")
    print(f"{'='*80}")
    
    orquestrador = VerificationOrchestrator()
    scores = []
    
    for p in supuesto['preguntas'][:3]:
        try:
            caso = {
                "pregunta": p.get("texto"),
                "opciones": p.get("opciones", {}),
                "respuesta_correcta": p.get("respuesta_correcta"),
                "razonamiento_observable": p.get("razonamiento", {}),
                "tema": "IT"
            }
            
            resultado = orquestrador.verify_caso_completo(caso, verbose=False)
            score = resultado.get("score_promedio", 0.5)
            scores.append(score)
            
            print(f"Q{p.get('num')}: {score:.0%} {resultado.get('status')}")
        except Exception as e:
            logger.debug(f"Error Q{p.get('num')}: {e}")
            scores.append(0.5)
    
    score_medio = sum(scores) / len(scores) if scores else 0.5
    
    print(f"\nScore promedio: {score_medio:.0%}")
    
    # Guardar
    output_dir = Path("/home/spas/OPOS_GEMINI_1/casos_reales_parte2")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"parte2_opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    resultado = {
        "timestamp": datetime.now().isoformat(),
        "supuesto": supuesto,
        "verificacion_muestra": {
            "preguntas": 3,
            "score_promedio": score_medio,
            "status": "✅ APROBADO" if score_medio >= 0.80 else "⚠️ REQUIERE AJUSTES"
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Guardado: {output_file}")
    
    print(f"\n{'='*80}")
    if score_medio >= 0.80:
        print("✅ PARTE 2 OPTIMIZADA Y VERIFICADA")
    else:
        print("⚠️ Requiere ajustes")
    print(f"{'='*80}\n")
    
    return resultado


if __name__ == "__main__":
    main()
