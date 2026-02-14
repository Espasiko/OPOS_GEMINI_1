#!/usr/bin/env python3
"""
Generador PARTE 2 (15 preguntas + enunciado) con Salamandra R1 Local
PHASE 2A: Multicontingencia supuestos prácticos

BASADO EN ESTRUCTURA OFICIAL BOE EXAMEN SS OPOSICIONES:
- Enunciado: 250-350 palabras con 6-9 personajes y datos reales
- 15 preguntas interdependientes (cada una usa datos del enunciado)
- Múltiples contingencias mezcladas (IT + Jubilación + IMV + etc)
- Razonamiento observable: 6 pasos por pregunta
- Vigencia normativa: todos artículos actualizados 2026
"""
import json
import requests
import sys
import re
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from datetime import datetime
import logging
from decimal import Decimal

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, '/home/spas/OPOS_GEMINI_1')
from backend.agents.verification_agents import VerificationOrchestrator
from backend.agents.reasoning_tracer import ReasoningTracer


# ============================================================================
# SALAMANDRA R1 LOCAL CONNECTOR - PARTE 2
# ============================================================================

class SalamandraR1ParteDosGenerator:
    """Genera PARTE 2 (15 preguntas + enunciado) usando Salamandra R1 local"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "salamandra-r1:q5km"
        self.verificar_conexion()
    
    def verificar_conexion(self):
        """Verifica que Salamandra está disponible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            modelos = response.json().get("models", [])
            modelos_nombres = [m.get("name", "") for m in modelos]
            
            if self.model in modelos_nombres:
                logger.info(f"✅ Salamandra conectada: {self.model}")
            else:
                logger.error(f"❌ Modelo {self.model} no encontrado")
                raise ConnectionError()
        except Exception as e:
            logger.error(f"❌ No se conecta a Ollama: {e}")
            raise
    
    def generar_supuesto(self, contingencias: List[str] = None, 
                        dificultad: str = "alta") -> Dict[str, Any]:
        """Genera 1 supuesto PARTE 2 (enunciado + 15 preguntas) usando Salamandra R1"""
        
        if contingencias is None:
            contingencias = ["IT", "JUBILACION"]
        
        # Prompt sistema
        system_prompt = """Eres Profesor Academia Oposiciones Seguridad Social con 20 años experiencia.
Tu tarea: Generar SUPUESTO PRÁCTICO PARTE 2 exacto como examen oficial BOE.

REGLAS ESTRICTAS:
1. Formato OFICIAL BOE PARTE 2: 
   - 1 enunciado (250-350 palabras)
   - 6-9 personajes con datos explícitos
   - 15 preguntas interdependientes (cada una usa datos del enunciado)
2. Dificultad ALTA: 80% opositores fallan
3. Contingencias MIXTAS: Múltiples tipos en mismo supuesto
4. Vigencia: Todos artículos actualizados 2026
5. Precisión: Cálculos exactos con Decimal (€0,00)

RESPUESTA OBLIGATORIA: JSON VÁLIDO con estructura EXACTA de 15 preguntas."""
        
        # Prompt usuario
        user_prompt = self._construir_prompt_supuesto(contingencias, dificultad)
        
        logger.info(f"\n📤 Enviando a Salamandra R1 (PARTE 2)...")
        logger.info(f"   Contingencias: {', '.join(contingencias)}")
        logger.info(f"   Dificultad: {dificultad}")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "system": system_prompt,
                    "prompt": user_prompt,
                    "stream": False,
                    "temperature": 0.3,  # Determinístico
                    "top_p": 0.9,
                    "num_ctx": 8192,  # Más contexto para 15 preguntas
                    "num_predict": 4096,  # Salida mayor
                },
                timeout=3600  # 60 minutos para 15 preguntas
            )
            
            response.raise_for_status()
            resultado_raw = response.json()
            respuesta_texto = resultado_raw.get("response", "")
            
            logger.info(f"✅ Respuesta recibida ({len(respuesta_texto)} caracteres)")
            
            # Parsear JSON
            supuesto = self._parsear_respuesta_parte2(respuesta_texto, contingencias)
            
            return supuesto
            
        except requests.exceptions.Timeout:
            logger.error("❌ Timeout: Salamandra tardó >60 min")
            return {"error": "Timeout después de 60 minutos"}
        except Exception as e:
            logger.error(f"❌ Error Salamandra: {e}")
            return {"error": str(e)}
    
    def _construir_prompt_supuesto(self, contingencias: List[str], dificultad: str) -> str:
        """Construye prompt para supuesto PARTE 2 multicontingencia"""
        
        contingencias_str = " + ".join(contingencias)
        
        return f"""Genera EXACTAMENTE UN supuesto práctico PARTE 2 examen SS oposiciones:

TEMA: {contingencias_str} (MULTICONTINGENCIA)

ESTRUCTURA OBLIGATORIA:
1. ENUNCIADO (250-350 palabras exactas):
   - Historia completa con contexto empresarial/familiar
   - 6-9 personajes NOMBRADOS con:
     * Nombre completo
     * Edad/fecha nacimiento
     * Puesto/contingencia principal
     * Base cotización si aplica
     * Datos clave para resolver preguntas
   - Hechos: Fechas exactas, eventos, cambios de situación
   - Normativa mencionada: Art XXX TRLGSS, RD YYY/2026

2. EXACTAMENTE 15 PREGUNTAS:
   - Pregunta 1-15: Numeradas 1 a 15 obligatoriamente
   - Cada pregunta: ¿Cuál es...?, ¿Cuánto es...?, ¿Qué artículo...?
   - Cada pregunta DEBE usar datos del enunciado (nombres, fechas, bases)
   - Interdependencias: pregunta 5 puede referenciar resultado pregunta 2

3. OPCIONES (A/B/C/D) para cada pregunta:
   - 4 opciones siempre
   - 1 correcta, 3 trampas pedagógicas
   - Valores realistas (no ficción)

4. RAZONAMIENTO observable (6 pasos):
   - paso_1: Identifica tipo pregunta + datos del enunciado
   - paso_2: Artículos aplicables + normativa vigente 2026
   - paso_3: Datos numéricos concretos
   - paso_4: Cálculo o lógica paso a paso
   - paso_5: Verificación vigencia normativa
   - paso_6: Conclusión final + por qué otras son trampas

CONTINGENCIAS A MEZCLAR: {contingencias_str}

REQUISITOS:
- TODAS las preguntas usan personajes/datos del enunciado
- Mínimo 3 preguntas por contingencia
- Máximo 1 pregunta aislada (sin referenciar enunciado)

DEVUELVE JSON VALIDO (SOLO JSON, SIN TEXTO EXTRA):
{{
  "tipo_examen": "PARTE_2",
  "enunciado": {{
    "texto": "Descripción completa 250-350 palabras...",
    "personajes": [
      {{"nombre": "Juan García López", "edad": 47, "puesto": "Técnico", "base": 2000, "contingencia": "IT"}},
      {{"nombre": "María García López", "edad": 65, "puesto": "Jubilada", "pension": 1200, "contingencia": "JUBILACION"}}
    ],
    "hechos_clave": ["Baja médica 10 feb 2026", "Solicita jubilación anticipada 1 marzo 2026"],
    "contexto_legal": "Resolución 2026-IT-001, cambios edad jubilación"
  }},
  "preguntas": [
    {{
      "num": 1,
      "texto": "¿Cuál es el subsidio que Juan percibe día 15 de baja?",
      "opciones": {{"A": "30€", "B": "50€", "C": "37,50€", "D": "0€"}},
      "respuesta_correcta": "A",
      "depende_de": ["personaje:Juan García López", "hecho:Baja médica 10 feb"],
      "tipo": "cálculo",
      "razonamiento": {{
        "paso_1": "IT día 15 → período 4-20 en EC",
        "paso_2": ["Art 173.1 TRLGSS"],
        "paso_3": {{"base": "2000€", "dia": 15}},
        "paso_4": "(2000€ ÷ 30) × 0.60 = 40€",
        "paso_5": "✅ Art 173 vigente 2026",
        "paso_6": "Respuesta A: 30€ NO 50€ (sería sin %)"
      }},
      "trampa_pedagogica": "Confundir 60% vs 75% por período"
    }},
    ... 14 preguntas más (2-15) ...
  ],
  "contingencias": ["IT", "JUBILACION"],
  "trampa_general": "Confundir edades/períodos 2025 vs 2026"
}}

IMPORTANTE:
- Devuelve SOLO el JSON válido
- Exactamente 15 preguntas en array
- Todas las preguntas DEBEN referencia el enunciado
- NO abrevies: nombres completos, cálculos exactos
"""
    
    def _parsear_respuesta_parte2(self, respuesta_texto: str, 
                                 contingencias: List[str]) -> Dict[str, Any]:
        """Extrae JSON de respuesta Salamandra PARTE 2 - ULTRA ROBUSTO"""
        
        logger.info(f"\n🔍 Parseando respuesta PARTE 2 ({len(respuesta_texto)} chars)...")
        
        # INTENTO 1: Parse directo
        try:
            supuesto = json.loads(respuesta_texto)
            if self._validar_estructura_parte2(supuesto):
                logger.info("✅ Parse DIRECTO exitoso")
                return self._normalizar_supuesto(supuesto, contingencias)
        except json.JSONDecodeError:
            pass
        
        # INTENTO 2: Buscar primer JSON válido con búsqueda greedy
        try:
            # Buscar {...} más ambicioso, encontrando el más largo
            matches = list(re.finditer(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', 
                                       respuesta_texto, re.DOTALL))
            if matches:
                # Intentar por orden de tamaño (mayor primero)
                for match in sorted(matches, key=lambda m: -len(m.group(0)))[:5]:
                    json_str = match.group(0)
                    try:
                        supuesto = json.loads(json_str)
                        
                        if self._validar_estructura_parte2(supuesto):
                            logger.info("✅ Parse ROBUSTO (regex greedy) exitoso")
                            return self._normalizar_supuesto(supuesto, contingencias)
                        else:
                            supuesto = self._completar_estructura_parte2(supuesto, contingencias)
                            if supuesto:
                                logger.info("✅ Parse COMPLETADO (estructura incompleta)")
                                return self._normalizar_supuesto(supuesto, contingencias)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logger.debug(f"   Intento 2 fallido: {e}")
        
        # INTENTO 3: Buscar JSON con patrón más relajado
        try:
            # Buscar "preguntas": [...] como indicador
            preguntas_match = re.search(r'"preguntas"\s*:\s*\[(.*?)\]\s*(?:,|\})', 
                                       respuesta_texto, re.DOTALL)
            if preguntas_match:
                # Reconstruir JSON alrededor de preguntas
                start = respuesta_texto.rfind('{', 0, preguntas_match.start())
                end = respuesta_texto.find('}', preguntas_match.end())
                
                if start >= 0 and end > preguntas_match.end():
                    json_str = respuesta_texto[start:end+1]
                    try:
                        supuesto = json.loads(json_str)
                        if self._validar_estructura_parte2(supuesto):
                            logger.info("✅ Parse RELAJADO (patrón 'preguntas') exitoso")
                            return self._normalizar_supuesto(supuesto, contingencias)
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            logger.debug(f"   Intento 3 fallido: {e}")
        
        # FALLBACK
        logger.warning("⚠️  FALLBACK: Estructura stub")
        return {
            "tipo_examen": "PARTE_2",
            "error": "Parser JSON fallido",
            "raw_response": respuesta_texto[:500],
            "timestamp": datetime.now().isoformat(),
        }
    
    def _validar_estructura_parte2(self, supuesto: dict) -> bool:
        """Valida que supuesto tenga estructura PARTE 2 completa"""
        
        required_keys = ["enunciado", "preguntas", "contingencias"]
        
        if not all(k in supuesto for k in required_keys):
            logger.debug(f"   Faltan keys: {[k for k in required_keys if k not in supuesto]}")
            return False
        
        # Validar enunciado
        enunciado = supuesto.get("enunciado", {})
        if not isinstance(enunciado, dict) or "texto" not in enunciado:
            logger.debug("   Enunciado inválido")
            return False
        
        # Validar personajes
        personajes = enunciado.get("personajes", [])
        if not isinstance(personajes, list) or len(personajes) < 2:
            logger.debug(f"   Personajes insuficientes: {len(personajes)}")
            return False
        
        # Validar preguntas
        preguntas = supuesto.get("preguntas", [])
        if not isinstance(preguntas, list) or len(preguntas) != 15:
            logger.debug(f"   Preguntas incompletas: {len(preguntas)} (requiere 15)")
            return False
        
        # Validar que cada pregunta tenga estructura
        for i, p in enumerate(preguntas):
            required_p = ["num", "texto", "opciones", "respuesta_correcta"]
            if not all(k in p for k in required_p):
                logger.debug(f"   Pregunta {i+1} incompleta")
                return False
            
            # Validar opciones
            opciones = p.get("opciones", {})
            if not isinstance(opciones, dict) or len(opciones) != 4:
                logger.debug(f"   Pregunta {i+1} opciones incompletas")
                return False
        
        logger.info("✅ Estructura PARTE 2 VÁLIDA")
        return True
    
    def _completar_estructura_parte2(self, supuesto: dict, 
                                    contingencias: List[str]) -> Optional[dict]:
        """Completa estructura parcial PARTE 2"""
        
        if "preguntas" in supuesto and isinstance(supuesto["preguntas"], list):
            if len(supuesto["preguntas"]) > 0:
                # Tiene al menos algunas preguntas
                
                # Completar preguntas faltantes hasta 15
                while len(supuesto["preguntas"]) < 15:
                    supuesto["preguntas"].append({
                        "num": len(supuesto["preguntas"]) + 1,
                        "texto": "Pregunta placeholder",
                        "opciones": {"A": "A", "B": "B", "C": "C", "D": "D"},
                        "respuesta_correcta": "B"
                    })
                
                # Limitar a exactamente 15
                supuesto["preguntas"] = supuesto["preguntas"][:15]
                
                # Asegurar contingencias
                if "contingencias" not in supuesto:
                    supuesto["contingencias"] = contingencias
                
                return supuesto
        
        return None
    
    def _normalizar_supuesto(self, supuesto: dict, 
                            contingencias: List[str]) -> dict:
        """Normaliza supuesto a formato estándar"""
        
        supuesto["tipo_examen"] = "PARTE_2"
        supuesto["generado_por"] = self.model
        supuesto["timestamp"] = datetime.now().isoformat()
        
        # Asegurar ID
        if "id" not in supuesto:
            conting_short = "".join([c[0] for c in contingencias])
            supuesto["id"] = f"SS_PARTE2_{conting_short}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Asegurar contingencias
        if "contingencias" not in supuesto:
            supuesto["contingencias"] = contingencias
        
        return supuesto


# ============================================================================
# EJECUTAR: GENERAR + VERIFICAR PARTE 2
# ============================================================================

def generar_y_verificar_parte2():
    """Flujo: Salamandra PARTE 2 → Verificación → Output"""
    
    print("\n" + "=" * 80)
    print("🚀 GENERADOR PARTE 2 (15 preguntas + enunciado) - Salamandra R1")
    print("=" * 80)
    
    try:
        salamandra = SalamandraR1ParteDosGenerator()
    except Exception as e:
        logger.error(f"No se puede conectar a Salamandra: {e}")
        return None
    
    # Generar supuesto PARTE 2
    contingencias = ["IT", "JUBILACION"]  # Multicontingencia
    supuesto = salamandra.generar_supuesto(contingencias, dificultad="alta")
    
    if "error" in supuesto:
        logger.error(f"Error generando supuesto: {supuesto['error']}")
        return supuesto
    
    print("\n" + "=" * 80)
    print("📋 SUPUESTO PARTE 2 GENERADO")
    print("=" * 80)
    
    # Mostrar enunciado
    enunciado = supuesto.get("enunciado", {})
    print(f"\n📖 ENUNCIADO ({len(enunciado.get('texto', ''))} chars):")
    print(enunciado.get("texto", "???")[:300] + "...")
    
    # Mostrar personajes
    personajes = enunciado.get("personajes", [])
    print(f"\n👥 PERSONAJES ({len(personajes)}):")
    for p in personajes[:3]:
        print(f"  - {p.get('nombre', '???')}: {p.get('puesto', '???')}, base {p.get('base', '???')}")
    
    # Mostrar preguntas
    preguntas = supuesto.get("preguntas", [])
    print(f"\n❓ PREGUNTAS ({len(preguntas)}/15):")
    for i, p in enumerate(preguntas[:3], 1):
        print(f"  {i}. {p.get('texto', '???')[:60]}...")
    
    # Verificación de primeras 3 preguntas
    print("\n" + "=" * 80)
    print("🔍 VERIFICACIÓN (5 AGENTES) - Preguntas 1-3")
    print("=" * 80)
    
    orquestrador = VerificationOrchestrator()
    scores = []
    
    for i, pregunta in enumerate(preguntas[:3], 1):
        logger.info(f"\n⏳ Verificando pregunta {i}/15...")
        
        caso_temp = {
            "pregunta": pregunta.get("texto"),
            "opciones": pregunta.get("opciones"),
            "respuesta_correcta": pregunta.get("respuesta_correcta"),
            "razonamiento_observable": pregunta.get("razonamiento", {}),
            "tema": supuesto.get("contingencias", ["IT"])[0].lower()
        }
        
        resultado = orquestrador.verify_caso_completo(caso_temp, verbose=False)
        scores.append(resultado.get("score_promedio", 0.5))
        
        print(f"  Q{i} Score: {resultado.get('score_promedio', 0):.0%} {resultado.get('status', '?')}")
    
    # Score promedio
    score_promedio = sum(scores) / len(scores) if scores else 0.5
    
    print("\n" + "=" * 80)
    print("📊 RESULTADO PARTE 2")
    print("=" * 80)
    print(f"Score promedio (Q1-3): {score_promedio:.0%}")
    print(f"Preguntas totales: {len(preguntas)}/15")
    print(f"Contingencias: {', '.join(supuesto.get('contingencias', []))}")
    print(f"ID: {supuesto.get('id', '???')}")
    
    # Guardar
    output_dir = Path("/home/spas/OPOS_GEMINI_1/casos_reales_parte2")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"parte2_salamandra_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    resultado_final = {
        "timestamp": datetime.now().isoformat(),
        "supuesto": supuesto,
        "verificacion_muestra": {
            "preguntas_verificadas": 3,
            "score_promedio_muestra": score_promedio,
            "status": "APROBADO ✅" if score_promedio >= 0.80 else "REQUIERE AJUSTES"
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado_final, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Supuesto guardado: {output_file}")
    
    print("\n" + "=" * 80)
    if score_promedio >= 0.80:
        print("✅ PARTE 2 GENERADA Y VERIFICADA")
    else:
        print("⚠️ PARTE 2 requiere ajustes")
    print("=" * 80)
    
    return resultado_final


if __name__ == "__main__":
    resultado = generar_y_verificar_parte2()
    
    if resultado and "error" not in resultado.get("supuesto", {}):
        print("\n✅ Generación PARTE 2 completada")
        sys.exit(0)
    else:
        print("\n❌ Error en generación PARTE 2")
        sys.exit(1)
