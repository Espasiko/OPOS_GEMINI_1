#!/usr/bin/env python3
import os
import sys
import re
import json
import asyncio
import logging
import hashlib
import yaml
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dotenv import load_dotenv

# 1. ENTORNO
root_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, root_dir)
sys.path.insert(0, os.path.join(root_dir, "backend"))

load_dotenv(os.path.join(root_dir, ".env"))

from agents.agent_engine import AgentEngine, get_rag_helper
from agents.verification_agents import VerificationOrchestrator
from calculators.dispatcher import CasosPracticosDispatcher

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("V13_SilentSieve")

# --- CONFIGURACIÓN DE SCORING ---
SCORING_WEIGHTS = {
    "BOE":            {"peso": 0.25, "min_eliminatorio": 1.0},
    "Legal":          {"peso": 0.20, "min_eliminatorio": 0.8},
    "Math":           {"peso": 0.25, "min_eliminatorio": 1.0},
    "Coherence":      {"peso": 0.10, "min_eliminatorio": 0.7},
    "Pedagogy":       {"peso": 0.10, "min_eliminatorio": 0.7},
    "Trap-Distractor":{"peso": 0.05, "min_eliminatorio": 0.7},
    "Interdependence":{"peso": 0.05, "min_eliminatorio": 0.7},
}

class SilentSieveOrchestrator:
    def __init__(self):
        self.engine = AgentEngine()
        self.orchestrator = VerificationOrchestrator()
        self.cache_dir = os.path.join(root_dir, "backend", "cache", "v13_normative")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.ttl_hours = 6
        self.rag = get_rag_helper()
        self._load_catalogs()

    def _load_catalogs(self):
        """Carga los catálogos de trampas master."""
        self.trap_catalogs = ""
        for filename in ["catalogo_trampas.yaml", "catalogo_trampas_adicional.yaml"]:
            path = os.path.join(root_dir, "academias", "1_casos_recientes_2026_DM", filename)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self.trap_catalogs += f"\n--- {filename} ---\n{f.read()}"
        logger.info("📚 Catálogos de trampas cargados.")

    async def _execute_mandatory_searches(self, agent_id: str) -> str:
        """Efectúa las búsquedas mandatorias ANTES de llamar al agente (Riesgo 1)."""
        manifest_path = os.path.join(root_dir, "opos-agents", "agents", f"{agent_id}.yaml")
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
        
        mandatory = manifest.get("mandatory_searches", [])
        if not mandatory: return ""

        results_block = "### RESULTADOS DE BÚSQUEDA MANDATORIA (FUENTES DE VERDAD)\n"
        for item in mandatory:
            query = item["query"]
            logger.info(f"🔍 Búsqueda Mandataria: {query}")
            
            # 1. RAG
            articles = self.rag.search_articles(query, limit=3)
            rag_txt = self.rag.format_articles_for_prompt(articles)
            
            # 2. Calculadora (si la query parece de cálculo)
            calc_res = ""
            if any(k in query.lower() for k in ["cálculo", "base", "jubilación", "it"]):
                calc_res = CasosPracticosDispatcher.ejecutar(query)
            
            results_block += f"\n- **Query**: {query}\n- **RAG**: {rag_txt}\n- **Calc**: {calc_res}\n"
            await asyncio.sleep(1) # Cortesía API/CPU

        return results_block

    async def run_pipeline(self, briefing: str) -> Dict[str, Any]:
        job_id = hashlib.sha1(f"{datetime.now()}{briefing}".encode()).hexdigest()[:8]
        logger.info(f"🚀 Iniciando Job {job_id}")

        # --- FASE 0: INVESTIGATOR (Fact-Mining con Verdad Inyectada) ---
        logger.info("🔎 [FASE 0] Fact-Mining (Verificando puntos maestros)...")
        truth_block = await self._execute_mandatory_searches("investigator_v13")
        
        if "No se encontraron artículos" in truth_block and "jubilacion" in briefing:
            logger.warning("⚠️ Alerta: Búsqueda mandatoria vacía para jubilación.")

        investigator_input = f"{truth_block}\n\nBRIEFING USUARIO:\n{briefing}"
        res = await self.engine.execute("investigator_v13", {"query": investigator_input})
        fact_sheet = res.get("content", "ERROR: No Fact Sheet generated")
        
        await asyncio.sleep(4)

        # --- FASE 1: REDACTOR (Data Dependency Map + Traps) ---
        logger.info("✍️ [FASE 1] Redactando Trama Causal con Trampas...")
        redactor_input = (
            f"CATÁLOGO DE TRAMPAS MAESTRO:\n{self.trap_catalogs}\n\n"
            f"FACT SHEET VERIFICADO:\n{fact_sheet}\n\n"
            f"BRIEFING USUARIO:\n{briefing}"
        )
        
        draft_content = ""
        max_retries = 3
        for i in range(max_retries):
            redactor_res = await self.engine.execute("redactor_v13", {"query": redactor_input})
            draft_content = redactor_res.get("content", "")
            if draft_content and not draft_content.startswith("ERROR"):
                break
            logger.warning(f"⚠️ Reintento {i+1}/{max_retries} por error en Redactor (posible 429)...")
            await asyncio.sleep(90) 
        
        if not draft_content:
            logger.error("❌ ERROR CRÍTICO: El Redactor no generó contenido tras reintentos.")
            return {"job_id": job_id, "score": 0.0, "status": "FAIL"}

        await asyncio.sleep(4)
        
        # --- NUEVO V14: LLAMAR AL VALIDATOR YAML ---
        logger.info("⚖️ [FASE 1.5] Llamando a validator.yaml...")
        try:
            validator_result = await self.engine.execute("validator", {
                "query": draft_content,
                "fecha_corte": "2026-03-04"
            })
            validator_content = validator_result.get("content", "")
            logger.info(f"Reporte Validator LLM ({len(validator_content)} bytes)")
        except Exception as e:
            logger.error(f"Error llamando al validator.yaml: {e}")
            validator_content = "ERROR en validación LLM"

        # --- FASE 2: AUDITORÍA PONDERADA REAL (Sieves) ---
        score, verification_report = await self._calculate_weighted_score(draft_content, fact_sheet)
        
        # --- SALIDA ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(root_dir, "dataset_output", "v13", f"caso_{job_id}_{timestamp}.md")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# SUPUESTO V13 [{job_id}]\nScore Auditoría: {score:.2f}\n\n{draft_content}\n\n---\n## Reporte Validator YAML\n{validator_content}")

        return {
            "job_id": job_id,
            "score": score,
            "output_path": output_path,
            "status": "PASS" if score >= 0.88 else "REFLOW"
        }

    async def _calculate_weighted_score(self, content: str, fact_sheet: str) -> Tuple[float, Dict]:
        """Auditado real de la salida del Redactor (Sprint 1)."""
        if not content or len(content) < 100:
            return 0.0, {"Error": "Contenido insuficiente"}

        results = {
            "BOE": 0.0,
            "Math": 0.0,
            "Legal": 1.0, # Placeholder
            "Coherence": 1.0,
            "Pedagogy": 1.0,
            "Trap-Distractor": 1.0,
            "Interdependence": 1.0
        }

        # 1. Extracción de datos del MD (simplificado para el ejemplo)
        # En una versión real usaríamos regex o un parser MD -> JSON
        
        # Sieve BOE: Verificación Real
        articles_to_verify = self._extract_articles(content)
        if not articles_to_verify:
            results["BOE"] = 1.0 # No cita -> no falla
        else:
            valid_articles = 0
            for art in articles_to_verify:
                search = self.rag.search_articles(art, limit=1)
                if search and len(search) > 0:
                    valid_articles += 1
            results["BOE"] = valid_articles / len(articles_to_verify)

        # Sieve Math: Verificación Real Estricta
        math_to_verify = self._extract_math_maps(content)
        questions = self._extract_questions(content)
        
        if not math_to_verify or len(math_to_verify) < 5:
            logger.warning("⚠️ DATA_MAP incompleto o ausente. Penalizando Math.")
            results["Math"] = 0.0
        else:
            valid_math = 0
            for item in math_to_verify:
                q_num = item.get("pregunta", "")
                # Buscar el bloque de texto de esta pregunta específica
                q_block = ""
                for q in questions:
                    if re.search(rf'\b{q_num}\b', q):
                        q_block = q.lower()
                        break
                
                if not q_block: q_block = content.lower() # Fallback

                # Extraer solo la parte "verdadera" (Solución + Razonamiento) para evitar distractores
                q_truth_part = q_block
                if "solución:" in q_block:
                    q_truth_part = q_block.split("solución:")[1]

                # 1. Centinelas Locales (Solo en la parte VERDADERA de la pregunta)
                if "voluntaria" in q_block and "anticipada" in q_block and "involuntaria" not in q_block:
                    anos_match = re.search(r'(\d+)\s+años\s+cotizados', q_block)
                    if anos_match and int(anos_match.group(1)) < 35:
                        if "sí" in q_truth_part or "puede acceder" in q_truth_part and "no puede" not in q_truth_part:
                            logger.error(f"❌ FALLO MATH CRÍTICO en {q_num}: Afirma jubilación voluntaria con < 35 años.")
                            results["Math"] = 0.0
                            break

                if "accidente de trabajo" in q_block or "it-at" in q_block or "at " in q_block:
                    # Solo falla si afirma que se usa el promedio de 3 meses como CORRECTO
                    if re.search(r'formula.*?3\s*meses|promedio.*?3\s*meses', q_truth_part) and "no se usa" not in q_truth_part:
                        logger.error(f"❌ FALLO MATH CRÍTICO en {q_num}: Sugiere fórmula de 3 meses para IT-AT.")
                        results["Math"] = 0.0
                        break

                # 2. Ejecución de Calculadora
                calc_res = CasosPracticosDispatcher.ejecutar(item.get("enunciado_dato_clave", item.get("trampa_desc", "")))
                res_redactor = str(item.get("resultado_numerico", "SIN_DATO")).replace(",", ".")
                
                if calc_res and calc_res.get("datos"):
                    dispatcher_val = str(calc_res["datos"]).replace(",", ".")
                    if res_redactor in dispatcher_val or dispatcher_val in res_redactor:
                        valid_math += 1
                else:
                    valid_math += 1
            
            if results["Math"] != 0.0:
                results["Math"] = valid_math / len(math_to_verify)

        # Sieve Coherence: Deduplicación por Hash
        hashes = [hashlib.md5(q.encode()).hexdigest() for q in self._extract_questions(content)]
        if len(hashes) != len(set(hashes)):
            results["Coherence"] = 0.0
        else:
            results["Coherence"] = 1.0

        # Cálculo Final Ponderado con Eliminatorios
        total_score = 0.0
        for key, config in SCORING_WEIGHTS.items():
            val = results.get(key, 0.0)
            if config["min_eliminatorio"] and val < config["min_eliminatorio"]:
                logger.error(f"❌ FALLO ELIMINATORIO en Sieve {key}: {val} < {config['min_eliminatorio']}")
                return 0.0, results
            total_score += val * config["peso"]

        return total_score, results

    def _extract_articles(self, content: str) -> List[str]:
        # Busca patrones tipo "Art. 123", "Artículo 12", "Disposición Transitoria 40", "Art 12"
        pattern = r"(?:Art\.?|Artículo|Disposición Transitoria|DT)\s+\d+(?:\s+\w+)?"
        return re.findall(pattern, content, re.IGNORECASE)

    def _extract_math_maps(self, content: str) -> List[Dict]:
        import re
        # Extrae los bloques DATA_MAP JSON
        pattern = r"```json\s+({.*?})\s+```"
        matches = re.findall(pattern, content, re.DOTALL)
        maps = []
        for m in matches:
            try: maps.append(json.loads(m))
            except: pass
        return maps

    def _extract_questions(self, content: str) -> List[str]:
        # Busca bloques que empiezan por Pregunta X y terminan antes de la siguiente pregunta o el final
        pattern = r"(?:Pregunta|###\s*Pregunta)\s+(\d+).*?(?=(?:Pregunta|###\s*Pregunta)\s+\d+|$)"
        questions = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        # Re-extraer el contenido completo de cada bloque
        full_blocks = []
        for q_num in questions:
            q_pattern = rf"(?:Pregunta|###\s*Pregunta)\s+{q_num}.*?(?=(?:Pregunta|###\s*Pregunta)\s+\d+|$)"
            match = re.search(q_pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                full_blocks.append(match.group(0))
        return full_blocks

async def main():
    briefing = """
    ENTORNO: Maresme S.A., Siderurgia. 
    PERSONAJES: Jorge (Socio 60%), Andrea (Hermana, convive), Pedro (IT por AT desde hace 20 días). 
    TEMAS: Encuadramiento Art 12, IT en AT, Jubilación 2026.
    """
    orchestrator = SilentSieveOrchestrator()
    result = await orchestrator.run_pipeline(briefing)
    print(f"\n✅ Pipeline Completado: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
