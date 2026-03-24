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
from v14.config.convocatorias import CONVOCATORIAS

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("V14_SilentSieve")

def extract_json_from_md(content: str) -> Dict[str, Any]:
    """Intenta extraer un objeto JSON del texto Markdown generado por el Redactor."""
    try:
        # Busca el bloque ```json ... ```
        pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return json.loads(match.group(1))
        # Si no hay bloque, intenta parsear todo
        return json.loads(content)
    except Exception as e:
        logger.warning(f"No se pudo extraer JSON estructurado del caso generado: {e}")
        return {}

class SilentSieveOrchestratorV14:
    def __init__(self):
        self.engine = AgentEngine()
        self.orchestrator = VerificationOrchestrator()
        self.cache_dir = os.path.join(root_dir, "backend", "cache", "v14_normative")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.rag = get_rag_helper()
        self._load_catalogs()

    def _load_catalogs(self):
        """Carga los catálogos de trampas master (V14)."""
        self.trap_catalogs = ""
        for filename in ["catalogo_trampas.yaml", "catalogo_trampas_adicional.yaml"]:
            path = os.path.join(root_dir, "academias", "1_casos_recientes_2026_DM", filename)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self.trap_catalogs += f"\n--- {filename} ---\n{f.read()}"
        logger.info("📚 Catálogos de trampas cargados (V14).")

    async def _execute_mandatory_searches(self, agent_id: str, oposicion: str = "SS") -> str:
        """Efectúa las búsquedas mandatorias ANTES de llamar al agente invocando la KB completa."""
        # Se asume manifest _v14 si existe, sino fallback al v13 standard
        manifest_path = os.path.join(root_dir, "opos-agents", "agents", f"{agent_id}.yaml")
        if not os.path.exists(manifest_path):
            manifest_path = manifest_path.replace("_v14", "_v13")
            if not os.path.exists(manifest_path): return ""
            
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
        
        # Opos-agents a veces envuelven la data en una llave 'agent'
        data = manifest.get("agent", manifest)
        mandatory = data.get("mandatory_searches", [])
        if not mandatory: return ""

        # En V14 consideramos la oposición para filtrar por Neo4j o fecha de corte del config si es necesario
        conf = CONVOCATORIAS.get(oposicion, CONVOCATORIAS["SS"])
        fecha_corte = conf["fecha_corte"]
        
        results_block = f"### RESULTADOS DE BÚSQUEDA MANDATORIA ({oposicion} - {fecha_corte})\n"
        for item in mandatory:
            query = item["query"]
            logger.info(f"🔍 Búsqueda Mandataria: {query}")
            
            # 1. Buscar en RAG sin recortes del texto
            articles = self.rag.search_articles(query, limit=5)
            rag_txt = self.rag.format_articles_for_prompt(articles)
            
            # 2. Calculadora predictiva
            calc_res = ""
            if any(k in query.lower() for k in ["cálculo", "base", "jubilación", "it", "nacimiento"]):
                calc_res = CasosPracticosDispatcher.ejecutar(query)
            
            results_block += f"\n- **Query**: {query}\n- **RAG**: {rag_txt}\n- **Calc**: {calc_res}\n"
            await asyncio.sleep(1) 

        return results_block

    async def run_pipeline(self, briefing: str, oposicion: str = "SS", blueprint: str = "") -> Dict[str, Any]:
        """
        Flujo Core V14: Investigator -> Redactor genérico -> Verification Orchestrator (Agentes reales 1 al 8)
        """
        job_id = hashlib.sha1(f"{datetime.now()}{briefing}".encode()).hexdigest()[:8]
        logger.info(f"🚀 Iniciando Job V14 {job_id} [{oposicion}]")

        # --- FASE 0: INVESTIGATOR ---
        logger.info("🔎 [FASE 0] Fact-Mining (Investigator V14)...")
        truth_block = await self._execute_mandatory_searches("investigator_v14", oposicion)
        
        investigator_input = f"{truth_block}\n\nBLUEPRINT DE REFERENCIA: {blueprint}\n\nBRIEFING USUARIO:\n{briefing}"
        res = await self.engine.execute("investigator_v14", {"query": investigator_input})
        if "error" in res:
            res = await self.engine.execute("investigator_v13", {"query": investigator_input})
            
        fact_sheet = res.get("content", "ERROR: No Fact Sheet generated")
        await asyncio.sleep(2)

        # --- FASE 1: REDACTOR (Caso en Formato JSON/MD) ---
        logger.info("✍️ [FASE 1] Redactando y Estructurando el Caso (Redactor V14)...")
        redactor_input = (
            f"CATÁLOGO DE TRAMPAS MAESTRO:\n{self.trap_catalogs}\n\n"
            f"FACT SHEET VERIFICADO:\n{fact_sheet}\n\n"
            f"REQUISITO: EL OUTPUT DEBE INCLUIR UN BLOQUE ```json CON LA ESTRUCTURA DEL CASO PARA LA MÁQUINA DE VALIDACIÓN.\n\n"
            f"BRIEFING USUARIO:\n{briefing}"
        )
        
        draft_content = ""
        max_retries = 3
        for i in range(max_retries):
            # Intentar primero con el redactor_v14 si existe
            redactor_res = await self.engine.execute("redactor_v14", {"query": redactor_input})
            if "error" in redactor_res:
                redactor_res = await self.engine.execute("redactor_v13", {"query": redactor_input})
                
            draft_content = redactor_res.get("content", "")
            if draft_content and not draft_content.startswith("ERROR"):
                break
            logger.warning(f"⚠️ Reintento {i+1}/{max_retries} por error en Redactor...")
            await asyncio.sleep(10) 
        
        if not draft_content:
            logger.error("❌ ERROR CRÍTICO: El Redactor no generó contenido.")
            return {"job_id": job_id, "score": 0.0, "status": "FAIL"}

        caso_json = extract_json_from_md(draft_content)
        
        if not caso_json:
            logger.warning("No se pudo extraer dict JSON. Se construirá un dict dummy para evitar caídas completas del orchestrator.")
            caso_json = {"enunciado": {"texto": draft_content, "personajes": []}, "preguntas": []}

        # --- NUEVO V14: LLAMAR AL VALIDATOR YAML Y REPORT.MD ---
        logger.info("⚖️ [FASE 1.5] Llamando a Validator (LLM Prose)...")
        try:
            validator_result = await self.engine.execute("validator", {
                "query": draft_content,
                "fecha_corte": CONVOCATORIAS.get(oposicion, CONVOCATORIAS["SS"])["fecha_corte"]
            })
            validator_content = validator_result.get("content", "")
        except Exception as e:
            logger.error(f"Error llamando al validator.yaml: {e}")
            validator_content = "ERROR en validación LLM Prose"

        # --- FASE 2: AUDITORÍA CON ORQUESTRADOR DE AGENTES REALES (1 al 8) ---
        logger.info("🛡️ [FASE 2] Verification Orchestrator V14 (Ejecutando Sieves 1-8)...")
        
        # Ejecutar los agentes de la V14 reales que conectan a Neo4j, Qdrant y Python
        orq_score, orq_results = await self.orchestrator.verify(caso_json)

        # Determinar si aprueba o reflow
        status = "PASS" if orq_score >= 0.88 else "REFLOW"
        
        # --- SALIDA ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(root_dir, "dataset_output", "v14", f"caso_{job_id}_{timestamp}.md")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# SUPUESTO V14 [{job_id}] - {oposicion}\n")
            f.write(f"Score Auditoría Agentes 1-8: {orq_score:.2f} ({status})\n\n")
            f.write(f"## Contenido Redactado\n{draft_content}\n\n---\n")
            f.write(f"## Auditoría Completa de los Agentes Independientes\n")
            f.write(f"```json\n{json.dumps(orq_results, indent=2, ensure_ascii=False)}\n```\n\n---\n")
            f.write(f"## Reporte LLM Validator (Prose/Style)\n{validator_content}\n")

        return {
            "job_id": job_id,
            "score": orq_score,
            "agent_reports": orq_results,
            "output_path": output_path,
            "status": status
        }

async def main():
    briefing = """
    ENTORNO: Criterio DUAL 2026. 
    PERSONAJES: Jorge (Socio 60%, Base 1200€ antes del cese de actividad por IT, Base 1500€ tras cese), Andrea (Hermana, convive).
    TEMAS: Regímenes de SS y Nueva Jubilación DUAL S5a.
    """
    blueprint = "bp_s12_jubilacion_2026"
    orchestrator = SilentSieveOrchestratorV14()
    result = await orchestrator.run_pipeline(briefing, oposicion="SS", blueprint=blueprint)
    print(f"\n✅ Pipeline V14 Completado con Status {result['status']} y Score {result['score']}\nGuardado en: {result['output_path']}")

if __name__ == "__main__":
    asyncio.run(main())
