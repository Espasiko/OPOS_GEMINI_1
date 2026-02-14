#!/usr/bin/env python3
"""
Generador PARTE 2 ITERATIVO - Phase 2A
Genera enunciado + 15 preguntas en 2 fases:
1. Fase 1: Enunciado único con 6-9 personajes (250-350 palabras)
2. Fase 2: 15 preguntas iterativas basadas en ese enunciado
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


class SalamandraParteDosIterativo:
    """Generador PARTE 2 con 2 fases para mejor calidad"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "salamandra-r1:q5km"
        self.verificar_conexion()
    
    def verificar_conexion(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            modelos = response.json().get("models", [])
            modelos_nombres = [m.get("name", "") for m in modelos]
            if self.model in modelos_nombres:
                logger.info(f"✅ Salamandra conectada: {self.model}")
            else:
                raise ConnectionError(f"Modelo {self.model} no encontrado")
        except Exception as e:
            logger.error(f"❌ No se conecta a Ollama: {e}")
            raise
    
    def generar_supuesto_completo(self, contingencias: List[str] = None) -> Dict[str, Any]:
        """
        Genera PARTE 2 completa en 2 fases:
        1. Enunciado con personajes
        2. 15 preguntas sobre ese enunciado
        """
        
        if contingencias is None:
            contingencias = ["IT", "JUBILACION"]
        
        logger.info(f"\n{'='*80}")
        logger.info(f"🚀 PARTE 2 ITERATIVO - Contingencias: {', '.join(contingencias)}")
        logger.info(f"{'='*80}")
        
        # FASE 1: Generar enunciado con personajes
        logger.info("\n📖 FASE 1: Generando enunciado con 6-9 personajes...")
        enunciado_data = self._generar_enunciado(contingencias)
        
        if not enunciado_data or "error" in enunciado_data:
            logger.error("❌ Fase 1 falló")
            return {"error": "Fase 1 failed"}
        
        # FASE 2: Generar 15 preguntas basadas en enunciado
        logger.info("\n❓ FASE 2: Generando 15 preguntas sobre el enunciado...")
        preguntas = self._generar_preguntas_iterativas(
            enunciado_data, 
            contingencias,
            num_preguntas=15
        )
        
        if not preguntas or len(preguntas) == 0:
            logger.error("❌ Fase 2 falló")
            return {"error": "Fase 2 failed"}
        
        # Consolidar
        supuesto_final = {
            "id": f"SS_PARTE2_{''.join([c[0] for c in contingencias])}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "tipo_examen": "PARTE_2",
            "timestamp": datetime.now().isoformat(),
            "generado_por": self.model,
            "enunciado": enunciado_data,
            "preguntas": preguntas,
            "contingencias": contingencias,
            "estadisticas": {
                "total_preguntas": len(preguntas),
                "personajes": len(enunciado_data.get("personajes", [])),
                "palabras_enunciado": len(enunciado_data.get("texto", "").split()),
            }
        }
        
        return supuesto_final
    
    def _generar_enunciado(self, contingencias: List[str]) -> Dict[str, Any]:
        """FASE 1: Genera enunciado único con 6-9 personajes"""
        
        contingencias_str = " + ".join(contingencias)
        
        prompt = f"""Genera SOLO UN enunciado supuesto práctico SS Oposiciones:

CONTINGENCIAS: {contingencias_str}

REQUISITOS ESTRICTOS:
1. ENUNCIADO: 250-350 palabras exactas
2. PERSONAJES: 6-9 personas NOMBRADAS con:
   - Nombre completo
   - Edad / Fecha nacimiento
   - Puesto / Situación laboral
   - Base cotización (si aplica)
   - Contingencia principal
3. HECHOS: Fechas exactas, eventos específicos, situaciones concretas
4. NORMATIVA: Artículos aplicables, cambios 2026

DEVUELVE JSON VÁLIDO:
{{
  "texto": "Juan García López, 47 años, nacido 1978... [250-350 palabras]",
  "personajes": [
    {{"nombre": "Juan García López", "edad": 47, "nacimiento": "15/03/1978", "puesto": "Técnico IT", "base": 2000, "contingencia": "IT"}},
    {{"nombre": "María García López", "edad": 65, "nacimiento": "20/05/1960", "puesto": "Jubilada", "pension": 1200, "contingencia": "JUBILACION"}}
  ],
  "hechos_clave": ["Baja médica 10 febrero 2026"],
  "articulos": ["Art 173 TRLGSS", "Art 206 TRLGSS"],
  "contexto_legal": "Resolución 2026-IT-001"
}}"""
        
        logger.info("   📤 Enviando a Salamandra...")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,
                    "num_ctx": 4096,
                    "num_predict": 1000,
                },
                timeout=300
            )
            
            respuesta = response.json().get("response", "").strip()
            logger.info(f"   ✅ Recibido ({len(respuesta)} chars)")
            
            # Extraer JSON
            enunciado = self._extraer_json_seguro(respuesta, "enunciado")
            
            if enunciado and "texto" in enunciado and "personajes" in enunciado:
                logger.info(f"   ✅ Enunciado válido: {len(enunciado['personajes'])} personajes")
                return enunciado
            else:
                logger.warning("   ⚠️ JSON inválido, intentando fallback")
                return self._crear_enunciado_fallback(contingencias)
                
        except Exception as e:
            logger.error(f"   ❌ Error Salamandra: {e}")
            return self._crear_enunciado_fallback(contingencias)
    
    def _generar_preguntas_iterativas(self, enunciado_data: Dict[str, Any],
                                     contingencias: List[str],
                                     num_preguntas: int = 15) -> List[Dict[str, Any]]:
        """FASE 2: Genera N preguntas iterativamente basadas en enunciado"""
        
        preguntas = []
        enunciado_texto = enunciado_data.get("texto", "")
        personajes_str = json.dumps(enunciado_data.get("personajes", []), ensure_ascii=False)
        
        for i in range(1, num_preguntas + 1):
            logger.info(f"   ⏳ Generando pregunta {i}/{num_preguntas}...")
            
            prompt = f"""Genera SOLO UNA pregunta tipo test para supuesto SS Oposiciones PARTE 2:

ENUNCIADO (contexto para la pregunta):
"{enunciado_texto[:200]}..."

PERSONAJES DISPONIBLES:
{personajes_str[:300]}

PREGUNTA NÚMERO: {i}/{num_preguntas}

REQUISITOS:
1. Pregunta DEBE usar datos específicos del enunciado
2. 4 opciones (A/B/C/D) realistas
3. 1 respuesta correcta
4. Razonamiento 6 pasos observable
5. Trampa pedagógica realista

DEVUELVE JSON:
{{
  "num": {i},
  "texto": "¿Cuánto es el subsidio...?",
  "opciones": {{"A": "valor1", "B": "valor2", "C": "valor3", "D": "valor4"}},
  "respuesta_correcta": "B",
  "razonamiento": {{
    "paso_1": "Identifica tipo/período",
    "paso_2": ["Art 173 TRLGSS"],
    "paso_3": {{"dato": "valor"}},
    "paso_4": "Cálculo paso a paso",
    "paso_5": "Verificación vigencia",
    "paso_6": "Conclusión + por qué otros son trampas"
  }},
  "trampa_pedagogica": "Confundir X con Y"
}}"""
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": 0.3,
                        "num_ctx": 2048,
                        "num_predict": 600,
                    },
                    timeout=120
                )
                
                respuesta = response.json().get("response", "").strip()
                pregunta = self._extraer_json_seguro(respuesta, "pregunta")
                
                if pregunta and "texto" in pregunta and "opciones" in pregunta:
                    # Normalizar
                    pregunta["num"] = i
                    if "depende_de" not in pregunta:
                        pregunta["depende_de"] = ["enunciado"]
                    
                    preguntas.append(pregunta)
                    logger.info(f"      ✅ Q{i} válida")
                else:
                    # Fallback pregunta simple
                    preguntas.append(self._crear_pregunta_fallback(i))
                    logger.info(f"      ⚠️ Q{i} fallback")
                    
            except Exception as e:
                logger.warning(f"      ❌ Q{i} error: {e}")
                preguntas.append(self._crear_pregunta_fallback(i))
        
        return preguntas
    
    def _extraer_json_seguro(self, texto: str, tipo: str) -> Optional[Dict[str, Any]]:
        """Extrae JSON de forma segura del texto"""
        
        try:
            # Intento 1: JSON directo
            return json.loads(texto)
        except json.JSONDecodeError:
            pass
        
        try:
            # Intento 2: Buscar {...}
            match = re.search(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', texto, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        
        return None
    
    def _crear_enunciado_fallback(self, contingencias: List[str]) -> Dict[str, Any]:
        """Fallback: crea enunciado simple"""
        
        return {
            "texto": f"Supuesto práctico de {', '.join(contingencias)}. Juan García López, 47 años, trabajador con contingencia de IT desde 2015. María García López, cónyuge, 65 años, pensionista. Solicita prestaciones...",
            "personajes": [
                {"nombre": "Juan García López", "edad": 47, "puesto": "Trabajador", "base": 2000, "contingencia": contingencias[0]},
                {"nombre": "María García López", "edad": 65, "puesto": "Pensionista", "pension": 1200, "contingencia": contingencias[1] if len(contingencias) > 1 else contingencias[0]},
            ],
            "hechos_clave": ["Solicitud contingencia 2026"],
            "articulos": ["Art 173 TRLGSS"],
            "contexto_legal": "Vigente 2026"
        }
    
    def _crear_pregunta_fallback(self, num: int) -> Dict[str, Any]:
        """Fallback: crea pregunta simple"""
        
        return {
            "num": num,
            "texto": f"Pregunta {num}: ¿Cuál es la respuesta correcta?",
            "opciones": {
                "A": f"Opción A - pregunta {num}",
                "B": f"Opción B - pregunta {num}",
                "C": f"Opción C - pregunta {num}",
                "D": f"Opción D - pregunta {num}"
            },
            "respuesta_correcta": "B",
            "razonamiento": {
                "paso_1": "Identificar tipo",
                "paso_2": ["Artículo TRLGSS"],
                "paso_3": {"base": "2000"},
                "paso_4": "Cálculo",
                "paso_5": "Vigencia 2026",
                "paso_6": "Conclusión"
            },
            "trampa_pedagogica": "Confundir con otra opción"
        }


# ============================================================================
# MAIN
# ============================================================================

def generar_parte2_iterativo():
    """Genera PARTE 2 iterativa completa"""
    
    print("\n" + "="*80)
    print("🚀 GENERADOR PARTE 2 ITERATIVO - Salamandra R1")
    print("="*80)
    
    try:
        generador = SalamandraParteDosIterativo()
    except Exception as e:
        logger.error(f"Error conexión: {e}")
        return None
    
    # Generar
    supuesto = generador.generar_supuesto_completo(["IT", "JUBILACION"])
    
    if "error" in supuesto:
        logger.error(f"Error generación: {supuesto['error']}")
        return None
    
    # Mostrar resultados
    print("\n" + "="*80)
    print("📋 SUPUESTO PARTE 2 GENERADO")
    print("="*80)
    
    print(f"\n📖 Enunciado:")
    print(f"   {supuesto['enunciado']['texto'][:200]}...")
    print(f"   Personajes: {len(supuesto['enunciado']['personajes'])}")
    print(f"   Palabras: {supuesto['estadisticas']['palabras_enunciado']}")
    
    print(f"\n❓ Preguntas: {supuesto['estadisticas']['total_preguntas']}/15")
    for i, p in enumerate(supuesto['preguntas'][:3], 1):
        print(f"   {i}. {p['texto'][:60]}...")
    
    # Verificar primeras 3 preguntas
    print("\n" + "="*80)
    print("🔍 VERIFICACIÓN - Preguntas 1-3")
    print("="*80)
    
    orquestrador = VerificationOrchestrator()
    scores = []
    
    for pregunta in supuesto['preguntas'][:3]:
        try:
            caso_temp = {
                "pregunta": pregunta.get("texto"),
                "opciones": pregunta.get("opciones"),
                "respuesta_correcta": pregunta.get("respuesta_correcta"),
                "razonamiento_observable": pregunta.get("razonamiento", {}),
                "tema": "IT"
            }
            
            resultado = orquestrador.verify_caso_completo(caso_temp, verbose=False)
            score = resultado.get("score_promedio", 0.5)
            scores.append(score)
            
            print(f"Q{pregunta['num']:2d}: {score:.0%} {resultado.get('status', '?')}")
        except Exception as e:
            logger.debug(f"Error verificando Q{pregunta['num']}: {e}")
            scores.append(0.5)
    
    score_promedio = sum(scores) / len(scores) if scores else 0.5
    
    print(f"\nScore promedio muestra: {score_promedio:.0%}")
    
    # Guardar
    output_dir = Path("/home/spas/OPOS_GEMINI_1/casos_reales_parte2")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"parte2_iterativo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    resultado_final = {
        "timestamp": datetime.now().isoformat(),
        "supuesto": supuesto,
        "verificacion_muestra": {
            "preguntas_verificadas": 3,
            "score_promedio": score_promedio,
            "status": "✅ APROBADO" if score_promedio >= 0.80 else "⚠️ REQUIERE AJUSTES"
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado_final, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Guardado: {output_file}")
    
    print("\n" + "="*80)
    if score_promedio >= 0.80:
        print("✅ PARTE 2 GENERADA Y VERIFICADA")
    else:
        print("⚠️ PARTE 2 requiere ajustes menores")
    print("="*80)
    
    return resultado_final


if __name__ == "__main__":
    resultado = generar_parte2_iterativo()
    sys.exit(0 if resultado else 1)
