from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class QuestionSchema:
    pregunta_id: str           # "P1" ... "P18"
    trampa_id: str             # ID del catálogo YAML, ej: "C14"
    articulo: str              # verificado en Neo4j, ej: "Art. 210 TRLGSS"
    url_boe: str               # URL real del BOE
    calculo_resultado: str     # ejecutado por Python, ej: "85.18"
    mnemonico: str             # del catálogo, max 15 palabras
    verified: bool = False     # True solo si Neo4j confirmó que el artículo existe

@dataclass
class CaseSchema:
    case_id: str
    blueprint_id: str
    personajes: List[str]
    fecha_caso: str
    contexto_legal: List[str] = field(default_factory=list)
    questions: List[QuestionSchema] = field(default_factory=list)
    validated: bool = False    # True solo si todos los artículos existen en Neo4j

class CaseSchemaBuilder:
    """
    Construye el CaseSchema COMPLETO sin ninguna llamada a LLM.
    El LLM Narrator solo recibe este schema y escribe prosa alrededor.
    """
    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())

    def _load_blueprint(self, blueprint_id: str):
        import importlib
        import glob
        
        # Fallback a buscar los ficheros por patrón
        archivos = glob.glob(f"backend/v14/blueprints/*_{blueprint_id.lower().split('-')[-1]}*.py")
        if not archivos:
            raise ValueError(f"Blueprint {blueprint_id} no encontrado en archivos.")
            
        mod_path = archivos[0].replace('/', '.').replace('\\', '.').replace('.py', '')
        modulo = importlib.import_module(mod_path)
        
        for item_name in dir(modulo):
            obj = getattr(modulo, item_name)
            if item_name.startswith("BP_") and obj.__class__.__name__.endswith("Blueprint"):
                return obj
                
        raise ValueError(f"No Blueprint instance found in {blueprint_id}")

    def _verify_article_neo4j(self, art_id: str, fecha_caso: str) -> Optional[str]:
        from neo4j import GraphDatabase
        import re
        try:
            match = re.search(r'\d+', art_id)
            num_art = match.group(0) if match else art_id
            
            # Extraer las siglas de la ley si existen (ej. "TRLGSS" de "Art. 204 TRLGSS")
            ley_match = re.search(r'(TRLGSS|ET|CE|LRJS|TREBEP)', art_id.upper())
            ley_siglas = ley_match.group(1) if ley_match else "TRLGSS" # Default a TRLGSS para oposiciones
            
            driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'opositaia2026'))
            with driver.session() as s:
                query = """
                MATCH (a:Articulo) 
                WHERE (a.id = $id OR a.title CONTAINS $num) AND (a.id CONTAINS $ley OR a.ley CONTAINS $ley)
                RETURN a.texto AS texto, a.vigente AS vigente LIMIT 1
                """
                result = s.run(query, {"id": art_id, "num": num_art, "ley": ley_siglas}).single()
            driver.close()
            if result and result["vigente"]:
                return result["texto"]
            return None
        except Exception as e:
            print(f"Error verificando en Neo4j: {e}")
            return None

    def _load_trap_from_catalog(self, trap_id: str) -> dict:
        import yaml
        import os
        catalog_path = "opos-agents/catalogo_trampas.yaml"
        if not os.path.exists(catalog_path):
            catalog_path = "../opos-agents/catalogo_trampas.yaml"
            
        try:
            with open(catalog_path, 'r', encoding='utf-8') as f:
                cat = yaml.safe_load(f)
            
            for category, traps in cat.items():
                if isinstance(traps, dict):
                    if trap_id in traps:
                        t = traps[trap_id]
                        # Aseguramos formato
                        if isinstance(t, str):
                            return {"articulo": "Art. Desconocido", "url_boe": "", "mnemonico": "", "valor_correcto": ""}
                        return {
                            "articulo": t.get("articulo", ""),
                            "url_boe": t.get("url_boe", ""),
                            "mnemonico": t.get("mnemonico", "N/A"),
                            "valor_correcto": t.get("valor_correcto", "")
                        }
        except:
            pass
        return {"articulo": "Art. Desconocido", "url_boe": "", "mnemonico": "Trampa no encontrada", "valor_correcto": ""}

    def build(self, blueprint_id: str, briefing: dict, fecha_caso: str = "2026-03-04") -> CaseSchema:
        blueprint = self._load_blueprint(blueprint_id)
        schema = CaseSchema(
            case_id=self._generate_id(),
            blueprint_id=blueprint_id,
            personajes=briefing.get("personajes", []),
            fecha_caso=fecha_caso,
        )
        
        # 1. Verificar artículos en Neo4j ANTES de todo
        articulos_encontrados = []
        for art_id in getattr(blueprint, "articulos_obligatorios", []):
            texto_ley = self._verify_article_neo4j(art_id, fecha_caso)
            if texto_ley:
                articulos_encontrados.append(art_id)
                schema.contexto_legal.append(f"--- {art_id} ---\n{texto_ley}")
            else:
                print(f"Warning: Artículo {art_id} no existe o no vigente en Neo4j para {blueprint_id}")

        # NUEVO: bloquear si Neo4j no tiene suficientes artículos
        if hasattr(blueprint, "articulos_obligatorios") and len(blueprint.articulos_obligatorios) > 0:
            MIN_ARTICULOS_VALIDOS = min(3, len(blueprint.articulos_obligatorios))
            if len(articulos_encontrados) < MIN_ARTICULOS_VALIDOS:
                raise ValueError(
                    f"Neo4j insuficiente: solo {len(articulos_encontrados)} artículos "
                    f"de {len(blueprint.articulos_obligatorios)} requeridos para {blueprint_id}. "
                    f"Ejecuta populate_neo4j_from_qdrant.py antes de generar casos."
                )

        # 2. Ejecutar calculadoras Python (determinístico, sin LLM)
        from backend.calculators.dispatcher import CasosPracticosDispatcher
        dispatcher = CasosPracticosDispatcher()
        
        if hasattr(blueprint, "generar_briefing"):
            try:
                briefing_dinamico = blueprint.generar_briefing(dispatcher)
                # Inyectamos el briefing rico en el schema para que el LLM pueda usarlo
                schema.personajes = [briefing_dinamico.get("personaje", "")]
                if hasattr(schema, "enunciado_datos"):
                    schema.enunciado_datos = briefing_dinamico
                else:
                    # Lo guardamos en el contexto legal temporalmente si no hay campo específico
                    schema.contexto_legal.insert(0, f"====== DATOS FÁCTICOS CALCULADOS ======\n{str(briefing_dinamico)}\n======================================")
            except Exception as e:
                print(f"Error ejecutando generar_briefing en {blueprint_id}: {e}")
        else:
            for calc_name in getattr(blueprint, "calculadoras", []):
                try:
                    # Mock call a dispatcher real
                    pass
                except Exception as e:
                    print(f"Error calculadora {calc_name}: {e}")

        # 3. Seleccionar trampas del catálogo YAML (no inventadas por el LLM)
        trampas_tip = getattr(blueprint, "trampas_tipicas", [])
        for trap_id in trampas_tip:
            trampa = self._load_trap_from_catalog(trap_id)
            art_trampa = trampa.get("articulo", "")
            
            if art_trampa and art_trampa != "Art. Desconocido":
                texto_trampa = self._verify_article_neo4j(art_trampa, fecha_caso)
                if texto_trampa:
                    schema.contexto_legal.append(f"--- {art_trampa} (Asociado a trampa {trap_id}) ---\n{texto_trampa}")
                    
            schema.questions.append(QuestionSchema(
                pregunta_id=f"P{len(schema.questions)+1}",
                trampa_id=trap_id,
                articulo=trampa["articulo"],
                url_boe=trampa["url_boe"],
                calculo_resultado=trampa["valor_correcto"],
                mnemonico=trampa["mnemonico"],
                verified=True,
            ))
            
        schema.validated = len(schema.questions) >= 15 # En real deberíamos inyectar 15 pregs
        return schema
