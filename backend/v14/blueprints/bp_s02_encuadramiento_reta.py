"""
OpositAIA V14 — Blueprint BP-S02
Tema: Encuadramiento en Régimen de SS (RETA, RG, asimilados, excluidos)
Temas oficiales: TE02 — Encuadramiento y campo de aplicación
Fuente: Arts. 7, 12, 136, 305-306 TRLGSS; RD 84/1996; RDL 13/2022

Cubre: socios de SL con funciones dirección, familiares convivientes,
cooperativas (opción estatutos), TRADE, SE Hogar, asimilados al alta.
"""
import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')
from v14.schemas import TopicBlueprint
import random

BP_S02 = TopicBlueprint(
    id="BP-S02",
    tema="Encuadramiento: ¿RG, RETA, asimilado o excluido?",
    temas_oficiales=["TE02"],
    normativa_base=[
        "Art. 7 TRLGSS — Campo de aplicación del sistema SS",
        "Art. 12 TRLGSS — Regímenes del sistema SS",
        "Art. 136 TRLGSS — Normas aplicables al RETA",
        "Art. 305 TRLGSS — Campo de aplicación RETA",
        "Art. 305.2.b TRLGSS — Socios de SL con ≥25% + funciones dirección → RETA",
        "Art. 305.2.e TRLGSS — Familiares del trabajador autónomo hasta 2º grado que convivan",
        "Art. 305.2.k TRLGSS — Socios cooperativa con opción RETA en estatutos",
        "DA 27ª TRLGSS — Familiar conviviente ≤30 años: contrato RG con bonificación",
        "Art. 12.2 TRLGSS — Asimilados a trabajadores por cuenta ajena",
    ],

    articulos_obligatorios=[
        "Art. 305 TRLGSS",
        "Art. 305.2.b TRLGSS",
        "Art. 305.2.e TRLGSS",
        "Art. 12.2 TRLGSS",
    ],
    articulos_forbidden=[
        "Art. 305 bis",
    ],

    calculadoras=[],

    trampas_tipicas=[
        "E1", "E2", "E3", "E4",
    ],

    eval_questions=[
        {
            "pregunta": "¿En qué régimen debe encuadrarse el socio administrador con funciones de dirección y gerencia que posee el 30% del capital de una SL?",
            "respuesta_correcta": "Régimen Especial de Trabajadores Autónomos (Art. 305.2.b TRLGSS: ≥25% + funciones dirección/gerencia → RETA obligatorio)",
            "distractores": [
                "Régimen General como trabajador por cuenta ajena",
                "Régimen General como asimilado, sin desempleo ni FOGASA",
                "A elección del socio, RG o RETA"
            ],
            "articulo": "Art. 305.2.b TRLGSS",
            "trampa_id": "E1",
            "mnemonico": "Socio SL ≥25% + dirección = RETA siempre. No importa si cobra nómina."
        },
        {
            "pregunta": "El cónyuge del trabajador autónomo trabaja en el negocio familiar y convive con él. No tiene participación en la sociedad. ¿En qué régimen debe encuadrarse?",
            "respuesta_correcta": "RETA (Art. 305.2.e: familiares hasta 2º grado que convivan y trabajen habitualmente → RETA, salvo que sean asalariados de una SL)",
            "distractores": [
                "Régimen General como trabajador por cuenta ajena",
                "Excluido del sistema de Seguridad Social al no tener participación",
                "Sistema Especial de Empleados del Hogar"
            ],
            "articulo": "Art. 305.2.e TRLGSS",
            "trampa_id": "E2",
            "mnemonico": "Familiar conviviente autónomo = RETA. Excepción: hijo ≤30a → puede RG (DA 27ª)."
        },
        {
            "pregunta": "Una cooperativa de trabajo asociado establece en sus estatutos que asimila a sus socios trabajadores a trabajadores por cuenta propia. ¿En qué régimen quedarán encuadrados?",
            "respuesta_correcta": "RETA (Art. 305.2.k: cooperativas cuyo estatuto opte por asimilar a cuenta propia → RETA)",
            "distractores": [
                "Régimen General de la Seguridad Social obligatoriamente",
                "RG o RETA, a elección individual de cada socio trabajador",
                "Excluidos del sistema hasta que la cooperativa cambie los estatutos"
            ],
            "articulo": "Art. 305.2.k TRLGSS",
            "trampa_id": "E3",
            "mnemonico": "Cooperativa: depende de estatutos. Si opta cuenta propia → RETA. Cambio: 5 años mínimo."
        },
        {
            "pregunta": "El hijo de 28 años de un trabajador autónomo convive con él y trabaja en su negocio. ¿Puede ser contratado como trabajador por cuenta ajena en el Régimen General?",
            "respuesta_correcta": "Sí, al ser menor de 30 años y familiar conviviente, puede ser contratado en RG con bonificación (DA 27ª TRLGSS)",
            "distractores": [
                "No, debe encuadrarse obligatoriamente en RETA como familiar conviviente",
                "Solo si no convive con el autónomo",
                "Solo si tiene reconocida una discapacidad del 33% o superior"
            ],
            "articulo": "DA 27ª TRLGSS",
            "trampa_id": "E4",
            "mnemonico": "Hijo ≤30 años conviviente: excepción DA 27ª → puede RG. Si >30 → RETA obligatorio."
        },
        {
            "pregunta": "Un socio de una SL que posee el 20% del capital social y NO ejerce funciones de dirección ni gerencia, pero trabaja como empleado de la empresa. ¿En qué régimen se encuadra?",
            "respuesta_correcta": "Régimen General como trabajador por cuenta ajena (no alcanza el 25% ni ejerce dirección → no aplica Art. 305.2.b)",
            "distractores": [
                "RETA, por ser socio de la SL",
                "RG como asimilado a cuenta ajena, sin desempleo",
                "Excluido del sistema al no alcanzar el 25%"
            ],
            "articulo": "Art. 305.2.b TRLGSS",
            "trampa_id": "E1",
            "mnemonico": "Socio SL <25% sin dirección = RG normal. Solo ≥25% + dirección fuerza RETA."
        },
    ],
)

def generar_briefing(dispatcher=None):
    from v14.nombres_pool import nombre_completo_aleatorio, nombre_empresa, ciudad

    tipo_empresa = random.choice(["SL", "cooperativa", "autónomo individual"])
    nombre, _ = nombre_completo_aleatorio()
    empresa = nombre_empresa()
    ciudad_val = ciudad()

    if tipo_empresa == "SL":
        participacion = random.choice([15, 20, 25, 30, 40, 50])
        funciones_direccion = random.choice([True, False])
        familiar_nombre, _ = nombre_completo_aleatorio()
        familiar_edad = random.randint(22, 55)
        familiar_parentesco = random.choice(["cónyuge", "hijo/a", "hermano/a"])
        familiar_convive = random.choice([True, False])

        descripcion = (
            f"{nombre} es socio de '{empresa}' con el {participacion}% del capital social"
            f"{' y ejerce funciones de dirección y gerencia' if funciones_direccion else ', sin funciones de dirección'}. "
            f"Su {familiar_parentesco} {familiar_nombre} ({familiar_edad} años) "
            f"{'convive con él/ella y ' if familiar_convive else ''}trabaja en la empresa."
        )
    elif tipo_empresa == "cooperativa":
        opcion_estatutos = random.choice(["cuenta propia", "cuenta ajena"])
        descripcion = (
            f"La cooperativa de trabajo asociado '{empresa}' tiene establecido en sus estatutos "
            f"que asimila a sus socios trabajadores a trabajadores por {opcion_estatutos}. "
            f"{nombre} se adhiere como socio trabajador."
        )
        participacion = 0
        funciones_direccion = False
        familiar_nombre = ""
        familiar_edad = 0
        familiar_parentesco = ""
        familiar_convive = False
    else:
        familiar_nombre, _ = nombre_completo_aleatorio()
        familiar_edad = random.randint(18, 45)
        familiar_parentesco = random.choice(["hijo/a", "cónyuge"])
        familiar_convive = True
        descripcion = (
            f"{nombre} dirige como autónomo una tienda en {ciudad_val}. "
            f"Su {familiar_parentesco} {familiar_nombre} ({familiar_edad} años) "
            f"convive y trabaja en el negocio."
        )
        participacion = 100
        funciones_direccion = True

    return {
        "personaje": nombre,
        "empresa": empresa,
        "ciudad": ciudad_val,
        "tema": "encuadramiento",
        "edad": random.randint(30, 65),
        "descripcion": descripcion,
        "tipo_empresa": tipo_empresa,
        "participacion_pct": participacion,
        "funciones_direccion": funciones_direccion,
        "familiar_nombre": familiar_nombre,
        "familiar_edad": familiar_edad,
        "familiar_parentesco": familiar_parentesco,
        "familiar_convive": familiar_convive,
    }

BP_S02.generar_briefing = generar_briefing
