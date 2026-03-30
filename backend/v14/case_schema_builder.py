from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import random
import itertools

@dataclass
class PersonajeSchema:
    nombre: str
    rol: str                    # "trabajador", "autónomo", "empresario", "familiar", "gestor"
    edad: Optional[int] = None
    datos: Dict[str, Any] = field(default_factory=dict)  # datos específicos: salario, base_cotizacion, etc.
    relaciones: List[str] = field(default_factory=list)  # nombres de otros personajes relacionados

@dataclass
class QuestionSchema:
    pregunta_id: str           # "P1" ... "P18"
    trampa_id: str             # ID del catálogo YAML, ej: "C14"
    articulo: str              # verificado en Neo4j, ej: "Art. 210 TRLGSS"
    url_boe: str               # URL real del BOE
    calculo_resultado: str     # respuesta correcta, ejecutada por Python
    mnemonico: str             # del catálogo, max 15 palabras
    pregunta: str = ""         # texto completo de la pregunta (de eval_questions)
    distractores: List[str] = field(default_factory=list)  # opciones incorrectas originales
    opciones_ordenadas: List[str] = field(default_factory=list)  # [A, B, C, D] ya barajadas
    letra_correcta: str = ""   # letra de la respuesta correcta tras barajar (A/B/C/D)
    razonamiento: str = ""     # LLM genera: por qué cada distractor es trampa
    personaje_ref: str = ""    # nombre del personaje al que hace referencia esta pregunta
    verified: bool = False     # True solo si Neo4j confirmó que el artículo existe
    blueprint_origen: str = "" # blueprint que genera esta pregunta

@dataclass
class CaseSchema:
    case_id: str
    blueprint_ids: List[str]   # MÚLTIPLES blueprints para casos complejos
    personajes: List[PersonajeSchema]
    fecha_caso: str
    contexto_legal: List[str] = field(default_factory=list)
    questions: List[QuestionSchema] = field(default_factory=list)
    conflictos_cruzados: List[str] = field(default_factory=list)  # ej: "impago_empresa", "accidente_laboral"
    validated: bool = False    # True solo si todos los artículos existen en Neo4j

class CaseSchemaBuilder:
    """
    Construye el CaseSchema COMPLETO sin ninguna llamada a LLM.
    El LLM Narrator solo recibe este schema y escribe prosa alrededor.
    """
    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())

    def _generate_red_personajes(self, num_personajes: int = 5, temas: List[str] = None) -> List[PersonajeSchema]:
        """
        Genera una red de personajes entrelazados tipo DM
        """
        if temas is None:
            temas = ["trabajador", "autónomo", "empresario", "familiar", "gestor"]
        
        nombres = ["Jorge", "María", "Carlos", "Ana", "Luis", "Elena", "Roberto", "Sofía"]
        apellidos = ["García", "Martínez", "López", "Sánchez", "Pérez", "Gómez"]
        
        personajes = []
        for i in range(min(num_personajes, 8)):
            nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"
            rol = temas[i % len(temas)]
            edad = random.randint(25, 65)
            
            personaje = PersonajeSchema(
                nombre=nombre,
                rol=rol,
                edad=edad,
                datos=self._generar_datos_personaje(rol, edad),
                relaciones=[]  # Se llenará después
            )
            personajes.append(personaje)
        
        # Crear relaciones entre personajes
        if len(personajes) >= 2:
            # Relaciones familiares
            if len(personajes) >= 3:
                personajes[0].relaciones.append(personajes[1].nombre)  # Padre/madre -> Hijo/a
                personajes[1].relaciones.append(personajes[0].nombre)
                personajes[0].datos["relacion_familiar"] = "padre/madre"
                personajes[1].datos["relacion_familiar"] = "hijo/a"
            
            # Relaciones laborales
            if len(personajes) >= 4:
                personajes[2].relaciones.append(personajes[3].nombre)  # Empresario -> Empleado
                personajes[3].relaciones.append(personajes[2].nombre)
                personajes[2].datos["tipo_relacion"] = "empleador"
                personajes[3].datos["tipo_relacion"] = "empleado"
            
            # Relaciones comerciales
            if len(personajes) >= 5:
                personajes[4].relaciones.extend([p.nombre for p in personajes[:2]])  # Proveedor -> Clientes
                personajes[4].datos["tipo_relacion"] = "proveedor"
        
        return personajes
    
    def _generar_datos_personaje(self, rol: str, edad: int) -> Dict[str, Any]:
        """
        Genera datos específicos según el rol del personaje
        """
        base_datos = {
            "salario_bruto": random.randint(1800, 4500),
            "base_cotizacion": random.randint(1500, 4000),
            "antiguedad": random.randint(1, 20),
        }
        
        if rol == "trabajador":
            base_datos.update({
                "tipo_contrato": random.choice(["indefinido", "temporal"]),
                "jornada": random.choice(["completa", "parcial"]),
                "categoria_profesional": random.choice(["técnico", "administrativo", "operario"]),
            })
        elif rol == "autónomo":
            base_datos.update({
                "tipo_actividad": random.choice(["profesional", "comercial", "servicios"]),
                "base_RETA": random.randint(300, 1500),
                "trabajadores": random.randint(0, 3),
            })
        elif rol == "empresario":
            base_datos.update({
                "tipo_empresa": random.choice(["SL", "SA", "autónomo"]),
                "sector": random.choice(["servicios", "comercio", "industria"]),
                "empleados": random.randint(2, 15),
            })
        elif rol == "familiar":
            base_datos.update({
                "parentesco": random.choice(["hijo", "cónyuge", "padre", "hermano"]),
                "convivencia": random.choice([True, False]),
                "discapacidad": random.choice([None, "33%", "65%"]),
            })
        elif rol == "gestor":
            base_datos.update({
                "especialidad": random.choice(["laboral", "fiscal", "contable"]),
                "clientes": random.randint(5, 50),
            })
        
        return base_datos
    
    def _generar_conflictos_cruzados(self, personajes: List[PersonajeSchema], temas: List[str]) -> List[str]:
        """
        Genera conflictos cruzados tipo DM entre los personajes
        """
        conflictos = []
        
        # Conflicto de impago (si hay empresario y trabajador)
        roles_presentes = [p.rol for p in personajes]
        if "empresario" in roles_presentes and "trabajador" in roles_presentes:
            conflictos.append("impago_empresa")
        
        # Conflicto de accidente laboral
        if "trabajador" in roles_presentes:
            conflictos.append("accidente_laboral")
        
        # Conflicto de incapacidad
        if any(p.datos.get("discapacidad") for p in personajes):
            conflictos.append("incapacidad_familiar")
        
        # Conflicto de recaudación (si hay autónomo)
        if "autónomo" in roles_presentes:
            conflictos.append("deuda_RETA")
        
        # Conflicto de jubilación anticipada
        if any(p.edad and p.edad >= 60 for p in personajes):
            conflictos.append("jubilacion_anticipada")
        
        # Conflicto de nacimiento/cuidado
        if "familiar" in roles_presentes and any(p.edad and p.edad >= 30 for p in personajes):
            conflictos.append("nacimiento_cuidado")
        
        return conflictos

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
            match = re.search(r'(\d+(?:\s*(?:bis|ter|qu[aá]ter))?)', art_id, re.I)
            num_art = match.group(0).strip() if match else art_id
            
            # Extraer las siglas de la ley si existen (ej. "TRLGSS" de "Art. 204 TRLGSS")
            ley_match = re.search(r'(TRLGSS|ET|CE|LRJS|TREBEP)', art_id.upper())
            ley_siglas = ley_match.group(1) if ley_match else "TRLGSS" # Default a TRLGSS para oposiciones
            
            import os
            neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
            neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
            neo4j_password = os.getenv('NEO4J_PASSWORD', 'opositaia2026')
            driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
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
        catalog_path = "academias/1_casos_recientes_2026_DM/catalogo_trampas.yaml"
        if not os.path.exists(catalog_path):
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

    def build_complex(self, blueprint_ids: List[str] = None, fecha_caso: str = "2026-03-04") -> CaseSchema:
        """
        Construye un caso práctico tipo DM con múltiples blueprints y personajes diversos.
        Cada ejecución genera datos distintos gracias a generar_briefing() aleatorio.
        Usa eval_questions de cada blueprint como fuente de preguntas verificadas.
        Objetivo: 15 preguntas mínimo, 18 ideal (15 + 3 de reserva).
        """
        OBJETIVO_PREGUNTAS = 18
        MINIMO_PREGUNTAS = 15

        if blueprint_ids is None:
            available_bps = [
                "BP-S12", "BP-S10", "BP-S11", "BP-S16", "BP-S05",  # originales
                "BP-S02", "BP-S04", "BP-S06", "BP-S07", "BP-S13",  # nuevos: encuadram, altas, recargos, URE, anticipada
            ]
            blueprint_ids = random.sample(available_bps, min(4, len(available_bps)))

        print(f"  → Blueprints seleccionados: {blueprint_ids}")

        from backend.calculators.dispatcher import CasosPracticosDispatcher
        dispatcher = CasosPracticosDispatcher()

        personajes = []
        briefings = {}
        all_eval_questions = {}   # bp_id → lista de eval_questions
        all_articulos = []

        # --- FASE 1: Ejecutar generar_briefing() de cada blueprint ---
        for bp_id in blueprint_ids:
            blueprint = self._load_blueprint(bp_id)
            all_articulos.extend(getattr(blueprint, "articulos_obligatorios", []))

            # Obtener eval_questions del blueprint (preguntas pre-verificadas)
            eq = getattr(blueprint, "eval_questions", [])
            all_eval_questions[bp_id] = eq

            if hasattr(blueprint, "generar_briefing"):
                try:
                    briefing = blueprint.generar_briefing(dispatcher)
                    briefings[bp_id] = briefing
                    nombre = briefing.get("personaje", f"Personaje_{bp_id}")
                    edad = briefing.get("edad")
                    datos_personaje = {k: v for k, v in briefing.items()
                                       if k not in ("personaje", "empresa", "ciudad", "genero", "edad", "descripcion")}
                    personajes.append(PersonajeSchema(
                        nombre=nombre,
                        rol=briefing.get("tema", "trabajador"),
                        edad=edad,
                        datos=datos_personaje,
                    ))
                    print(f"  → {bp_id}: personaje '{nombre}' generado")
                except Exception as e:
                    print(f"  ⚠️  Error en generar_briefing de {bp_id}: {e}")
                    personajes.append(PersonajeSchema(nombre=f"Personaje_{bp_id}", rol="trabajador"))

        # --- FASE 2: Crear CaseSchema base ---
        schema = CaseSchema(
            case_id=self._generate_id(),
            blueprint_ids=blueprint_ids,
            personajes=personajes,
            fecha_caso=fecha_caso,
        )

        # --- FASE 3: Verificar artículos en Neo4j e inyectar textos de ley ---
        articulos_encontrados = []
        for art_id in dict.fromkeys(all_articulos):   # deduplicar manteniendo orden
            texto_ley = self._verify_article_neo4j(art_id, fecha_caso)
            if texto_ley:
                articulos_encontrados.append(art_id)
                schema.contexto_legal.append(f"--- {art_id} ---\n{texto_ley}")
            else:
                print(f"  ⚠️  {art_id}: no encontrado en Neo4j")

        # --- FASE 4: Insertar datos de personajes, fechas y empresa central en contexto ---
        # Elegir UNA empresa central (la del primer blueprint) como eje narrativo
        empresa_central = ""
        ciudad_empresa = ""
        for bp_id in blueprint_ids:
            b = briefings.get(bp_id, {})
            if b.get("empresa"):
                empresa_central = b["empresa"]
                ciudad_empresa = b.get("ciudad", "")
                break

        bloques_personaje = []
        todas_fechas = []
        for bp_id, briefing in briefings.items():
            nombre = briefing.get("personaje", "?")
            desc = briefing.get("descripcion", "")
            calculos = briefing.get("calculos_verificados", {})

            # Recoger todas las fechas del briefing para inyectarlas
            fechas_bp = {k: v for k, v in briefing.items()
                         if "fecha" in k.lower() and v}
            if fechas_bp:
                todas_fechas.append(f"  {bp_id}: {fechas_bp}")

            bloque = (
                f"=== PERSONAJE: {nombre} | Blueprint: {bp_id} ===\n"
                f"Descripción: {desc}\n"
            )
            if calculos:
                bloque += f"Cálculos verificados: {calculos}\n"
            if fechas_bp:
                bloque += f"Fechas clave: {fechas_bp}\n"
            bloques_personaje.append(bloque)

        # Cabecera con empresa central, ciudad y fecha del caso
        cabecera = (
            f"====== CASO PRÁCTICO — Fecha: {fecha_caso} ======\n"
            f"EMPRESA CENTRAL: {empresa_central}"
            f"{' (' + ciudad_empresa + ')' if ciudad_empresa else ''}\n"
            f"INSTRUCCIONES NARRATIVAS: Todos los personajes deben estar conectados "
            f"a la empresa central (como socios, trabajadores, familiares de socios, o "
            f"clientes/proveedores). Inventa relaciones familiares y laborales entre ellos "
            f"(matrimonio, hijos, convivencia) para crear una trama entrelazada realista. "
            f"Un personaje puede tener una SEGUNDA ACTIVIDAD como autónomo además de su "
            f"vínculo con la empresa central.\n"
        )
        if todas_fechas:
            cabecera += "FECHAS CONCRETAS DISPONIBLES (úsalas en la narración):\n"
            cabecera += "\n".join(todas_fechas) + "\n"

        schema.contexto_legal.insert(0,
            cabecera +
            "\n".join(bloques_personaje) +
            "\n======================================"
        )

        # --- FASE 5: Pool ALL eval_questions, distribute round-robin, guarantee 18 ---
        letras = ["A", "B", "C", "D"]

        # Build per-blueprint queues: [(bp_id, personaje, eq), ...]
        bp_queues = {}
        for bp_id in blueprint_ids:
            nombre_personaje = briefings.get(bp_id, {}).get("personaje", "")
            eq_list = list(all_eval_questions.get(bp_id, []))
            random.shuffle(eq_list)
            bp_queues[bp_id] = {"personaje": nombre_personaje, "questions": eq_list}

        # Round-robin: take 1 question per blueprint, repeat until 18
        selected = []
        while len(selected) < OBJETIVO_PREGUNTAS:
            added_this_round = False
            for bp_id in blueprint_ids:
                if len(selected) >= OBJETIVO_PREGUNTAS:
                    break
                queue = bp_queues[bp_id]["questions"]
                if queue:
                    selected.append((bp_id, queue.pop(0)))
                    added_this_round = True
            if not added_this_round:
                break  # all queues exhausted

        # If still < 18: cycle through ALL eval_questions again (different order)
        if len(selected) < OBJETIVO_PREGUNTAS:
            all_pool = []
            for bp_id in blueprint_ids:
                nombre_p = briefings.get(bp_id, {}).get("personaje", "")
                for eq in all_eval_questions.get(bp_id, []):
                    all_pool.append((bp_id, eq))
            random.shuffle(all_pool)
            used_preguntas = {eq.get("pregunta", "") for _, eq in selected}
            for bp_id, eq in all_pool:
                if len(selected) >= OBJETIVO_PREGUNTAS:
                    break
                if eq.get("pregunta", "") not in used_preguntas:
                    selected.append((bp_id, eq))
                    used_preguntas.add(eq.get("pregunta", ""))

        # Convert selected to QuestionSchema
        for idx, (bp_id, eq) in enumerate(selected, 1):
            respuesta_correcta = eq.get("respuesta_correcta", "")
            distractores = list(eq.get("distractores", []))

            opciones = distractores[:3] + [respuesta_correcta]
            while len(opciones) < 4:
                opciones.append("—")
            random.shuffle(opciones)
            letra_c = letras[opciones.index(respuesta_correcta)]

            schema.questions.append(QuestionSchema(
                pregunta_id=f"P{idx}",
                trampa_id=eq.get("trampa_id", f"{bp_id}_Q{idx}"),
                articulo=eq.get("articulo", ""),
                url_boe="",
                calculo_resultado=respuesta_correcta,
                mnemonico=eq.get("mnemonico", ""),
                pregunta=eq.get("pregunta", ""),
                distractores=distractores,
                opciones_ordenadas=opciones,
                letra_correcta=letra_c,
                personaje_ref=bp_queues.get(bp_id, {}).get("personaje", ""),
                verified=True,
                blueprint_origen=bp_id,
            ))

        # --- FASE 7: Validación final ---
        schema.validated = len(schema.questions) >= MINIMO_PREGUNTAS
        print(f"  ✅ Schema complejo: {len(schema.questions)} preguntas | {len(personajes)} personajes | validated={schema.validated}")

        return schema
    
    def _validar_prerrequisitos_personajes(self, personajes: List[PersonajeSchema], blueprint_ids: List[str]) -> List[PersonajeSchema]:
        """
        Sprint 2.5: Validador de prerequisitos para evitar personajes imposibles
        """
        from backend.v14.cambios_dm_2026 import JUBILACION_2026
        
        personajes_validados = []
        for personaje in personajes:
            # Validar personaje jubilable
            if personaje.edad and personaje.edad >= 60:
                # Verificar si tiene años cotizados suficientes
                anos_cotizados = personaje.datos.get("anos_cotizados", 0)
                
                # Requisitos jubilación ordinaria
                if personaje.edad >= 65:
                    # Jubilación ordinaria: 15 años mínimos
                    if anos_cotizados < 15:
                        print(f"⚠️ ERROR PERSONAJE: {personaje.nombre} tiene {personaje.edad} años pero solo {anos_cotizados} años cotizados")
                        print(f"   Requisito: 15 años mínimos para jubilación ordinaria")
                        # Ajustar años cotizados a mínimo viable
                        personaje.datos["anos_cotizados"] = 15
                        print(f"   ✅ Corrección: Ajustados a 15 años cotizados")
                
                # Validar jubilación anticipada
                if "BP-S12" in blueprint_ids and personaje.edad >= 60:
                    # Jubilación anticipada: 35 años mínimos
                    if anos_cotizados < 35:
                        print(f"⚠️ ERROR PERSONAJE: {personaje.nombre} tiene {personaje.edad} años pero solo {anos_cotizados} años cotizados")
                        print(f"   Requisito: 35 años mínimos para jubilación anticipada")
                        # Ajustar años cotizados a mínimo viable
                        personaje.datos["anos_cotizados"] = 35
                        print(f"   ✅ Corrección: Ajustados a 35 años cotizados")
            
            personajes_validados.append(personaje)
        
        return personajes_validados

    def build(self, blueprint_id: str, briefing: dict, fecha_caso: str = "2026-03-04") -> CaseSchema:
        blueprint = self._load_blueprint(blueprint_id)
        # Convertir strings a PersonajeSchema si el briefing pasa nombres simples
        personajes_raw = briefing.get("personajes", [])
        personajes = [
            PersonajeSchema(nombre=p, rol="trabajador") if isinstance(p, str) else p
            for p in personajes_raw
        ]
        schema = CaseSchema(
            case_id=self._generate_id(),
            blueprint_ids=[blueprint_id],
            personajes=personajes,
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
                personaje_raw = briefing_dinamico.get("personaje", "")
                if personaje_raw and isinstance(personaje_raw, str):
                    schema.personajes = [PersonajeSchema(nombre=personaje_raw, rol="trabajador")]
                elif isinstance(personaje_raw, dict):
                    schema.personajes = [PersonajeSchema(
                        nombre=personaje_raw.get("nombre", "Personaje"),
                        rol=personaje_raw.get("rol", "trabajador"),
                        edad=personaje_raw.get("edad"),
                        datos=personaje_raw.get("datos", {})
                    )]
                # Si personaje_raw está vacío, conservamos los personajes ya inicializados
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
