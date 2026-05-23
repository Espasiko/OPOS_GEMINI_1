"""
OpositAIA V14 — Pool de nombres, apellidos y empresas para casos diversos.
Cada llamada a las funciones produce valores distintos usando random.

NOTA IMPORTANTE 18/04/2026: filtrados nombres que aparecen literalmente en simulacros
conocidos (Jorge, Manuel, Amaia, Andrea, Roberta, Francisca, HORIZONTE+SOLIDARIO,
NEBULA+BYTE). Se añade pool de empresas memorables/cómicas para que el alumno
retenga mejor el caso (gen. "CARNICERÍA APOCALIPTO S.L.", "AÉREA CRASH TOTAL S.A.").
"""
import random
from typing import Optional

# Nombres filtrados: se evita coincidencia con simulacros DM (febrero/enero/diciembre 2026)
# Eliminados: Jorge, Manuel, Pedro (jubilación activa), Miguel (caso A8)
NOMBRES_MASCULINOS = [
    "Antonio", "Carlos", "Francisco", "José",
    "Roberto", "Luis", "Alejandro", "David", "Javier", "Fernando",
    "Rafael", "Sergio", "Pablo", "Alberto", "Raúl", "Ignacio", "Enrique",
    "Tomás", "Adrián", "Marcos", "Rubén", "Iván", "Víctor", "Óscar",
    "Hugo", "Álvaro", "Lucas", "Héctor", "Darío", "Bruno", "Gabriel",
    "Diego", "Samuel", "Joaquín", "Esteban", "Eduardo", "Mateo",
]

# Eliminados: Amaia, Andrea, Francisca, Roberta, Soraya, Angélica
NOMBRES_FEMENINOS = [
    "María", "Ana", "Laura", "Carmen", "Elena", "Sofía", "Lucía", "Patricia",
    "Marta", "Cristina", "Isabel", "Rosa", "Nuria", "Beatriz", "Rocío",
    "Silvia", "Pilar", "Alicia", "Natalia", "Raquel",
    "Amparo", "Dolores", "Concepción", "Verónica",
    "Valeria", "Clara", "Julia", "Inés", "Olga", "Eva", "Celia",
    "Aitana", "Daniela", "Paula", "Irene", "Leire", "Noelia", "Claudia",
]

APELLIDOS = [
    "García", "Martínez", "López", "Sánchez", "Pérez", "González", "Gómez",
    "Fernández", "Díaz", "Torres", "Ramírez", "Flores", "Ruiz", "Moreno",
    "Jiménez", "Romero", "Herrera", "Medina", "Castro", "Vargas", "Ortega",
    "Delgado", "Mendoza", "Vázquez", "Campos", "Guerrero", "Ramos", "Molina",
    "Serrano", "Blanco", "Cuesta", "Navarro", "Prieto", "Vidal", "Mora",
    "Iglesias", "Fuentes", "Leal", "Pardo", "Bravo", "Galván", "Montero",
]

PREFIJOS_EMPRESA = [
    "SOLARIS", "AURORA", "MERIDIAN", "VEGA",
    "ATLAS", "SIGMA", "ALTAIR", "NEXUS", "KRONOS", "ORION", "ZENITH",
    "ALTEA", "IBERIA", "CELTA", "NUMANCIA", "ALCAZAR", "TORREON",
    "LEVANTE", "PONENT", "TRAMUNTANA", "MESTRAL", "LLEVANT", "GARBI",
    "HELIOS", "SELENE", "GEMINIS", "CENTAURI", "ANDROMEDA", "FENIX",
]

SUFIJOS_EMPRESA = [
    "TECH", "GROUP", "SOLUTIONS", "SYSTEMS",
    "CONSULTING", "SERVICES", "GLOBAL", "DIGITAL", "NETWORKS",
    "LOGISTICS", "CARGO", "METAL", "BUILD", "CONSTRUCT", "AGRO",
    "FOODS", "HEALTH", "CARE", "LEGAL", "INVEST", "CAPITAL",
    "IBERICA", "EUROPA", "CONTINENTAL", "PACIFICO", "ATLANTICO",
]

# Pool de empresas memorables/cómicas (formato completo con tipo societario)
# Filosofía pedagógica: un nombre divertido o extravagante ayuda al alumno a retener
# el caso y sus trampas. Se usa para casos prácticos donde el nombre no debe ser
# confundible con una empresa real.
EMPRESAS_MEMORABLES = [
    "CARNICERÍA APOCALIPTO S.L.",
    "AÉREA CRASH TOTAL S.A.",
    "BAR LA ÚLTIMA RONDA S.L.",
    "CLÍNICA DR. FRANKENSTEIN S.L.",
    "PASTELERÍA SIN GLUTEN NI ALMA S.L.",
    "LIMPIEZAS TITANIC S.L.",
    "RESTAURANTE EL BUEN PROVECHO S.L.",
    "TAXIS TURBOCADOS S. Coop.",
    "FLORISTERÍA ETERNIDAD S.L.",
    "PELUQUERÍA TIJERAS DE EDWARD S.L.",
    "BODEGAS DIONISIOS S.A.",
    "ACADEMIA DE BAILE EL SALTO MORTAL S.L.",
    "SASTRERÍA EL HILO DE ARIADNA S.L.",
    "FRUTERÍA LOS SIETE MARES S. Coop.",
    "LIBRERÍA DE BORGES S.L.",
    "PANADERÍA EL HORNO DE VULCANO S.L.",
    "DROGUERÍA MALAS PULGAS S.L.",
    "TINTORERÍA EL LAVADO PROFUNDO S.L.",
    "PESCADERÍA POSEIDÓN S. Coop.",
    "ZAPATERÍA ZAPATONES DEL REY S.L.",
    "JARDINERÍA LAS MALAS HIERBAS S.L.",
    "CERRAJERÍA HOUDINI S.L.",
    "CAFETERÍA ETERNO DESPERTAR S.L.",
    "AGENCIA DE VIAJES NUNCA JAMÁS S.L.",
    "MUDANZAS HÉRCULES S.A.",
    "FERRETERÍA MARTILLO DE THOR S.L.",
    "ÓPTICA OJOS DE ARGOS S.L.",
    "GIMNASIO LAS 12 PRUEBAS S.L.",
    "AUTOESCUELA CHOQUE SEGURO S.L.",
    "CONSULTORÍA MATRIX REVOLUTIONS S.L.",
    "FUNERARIA VIDA DESPUÉS DE S.L.",
    "EMPRESA DE MUDANZAS PISA FUERTE S.L.",
    "CONSTRUCCIONES DEDAL DE ORO S.A.",
    "COOPERATIVA AGRÍCOLA CAMPOS DE SIRIA S. Coop.",
    "TALLER MECÁNICO EL TURBO LOCO S.L.",
]

TIPOS_EMPRESA = [
    "SL", "SA", "SLU", "S. Coop.", "SAL", "SLL",
]

CIUDADES = [
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Bilbao",
    "Málaga", "Valladolid", "Murcia", "Palma", "Las Palmas", "Alicante",
    "Córdoba", "Granada", "Vitoria", "A Coruña", "Pamplona", "San Sebastián",
    "Santander", "Logroño", "Oviedo", "Gijón", "Vigo", "Badajoz", "Cáceres",
]

SECTORES = [
    "construcción", "hostelería", "comercio al por menor", "transporte",
    "industria manufacturera", "servicios financieros", "sanidad privada",
    "tecnología", "enseñanza privada", "logística", "agricultura",
    "administración de fincas", "consultoría", "servicios de limpieza",
]


def nombre_masculino(rng: Optional[random.Random] = None) -> str:
    r = rng or random
    return r.choice(NOMBRES_MASCULINOS)


def nombre_femenino(rng: Optional[random.Random] = None) -> str:
    r = rng or random
    return r.choice(NOMBRES_FEMENINOS)


def apellidos(rng: Optional[random.Random] = None) -> str:
    r = rng or random
    return f"{r.choice(APELLIDOS)} {r.choice(APELLIDOS)}"


def nombre_completo_masculino(rng: Optional[random.Random] = None) -> str:
    r = rng or random
    return f"{nombre_masculino(r)} {apellidos(r)}"


def nombre_completo_femenino(rng: Optional[random.Random] = None) -> str:
    r = rng or random
    return f"{nombre_femenino(r)} {apellidos(r)}"


def nombre_empresa(rng: Optional[random.Random] = None) -> str:
    """Combina prefijo + sufijo + tipo societario. Estilo neutro/corporativo."""
    r = rng or random
    tipo = r.choice(TIPOS_EMPRESA)
    nombre = f"{r.choice(PREFIJOS_EMPRESA)}-{r.choice(SUFIJOS_EMPRESA)} {tipo}"
    return nombre


def empresa_memorable(rng: Optional[random.Random] = None) -> str:
    """Devuelve una empresa del pool de nombres memorables/cómicos.
    Útil para casos prácticos donde se quiere alta retención pedagógica."""
    r = rng or random
    return r.choice(EMPRESAS_MEMORABLES)


def empresa_aleatoria(rng: Optional[random.Random] = None,
                       prob_memorable: float = 0.6) -> str:
    """Devuelve empresa: con prob. prob_memorable usa pool memorable,
    en caso contrario genera neutra tipo PREFIJO-SUFIJO S.L.

    Por defecto 60% memorables (para máxima retención pedagógica)."""
    r = rng or random
    if r.random() < prob_memorable:
        return empresa_memorable(r)
    return nombre_empresa(r)


def ciudad(rng: Optional[random.Random] = None) -> str:
    r = rng or random
    return r.choice(CIUDADES)


def sector(rng: Optional[random.Random] = None) -> str:
    r = rng or random
    return r.choice(SECTORES)


def genero_aleatorio(rng: Optional[random.Random] = None) -> str:
    r = rng or random
    return r.choice(["masculino", "femenino"])


def nombre_completo_aleatorio(rng: Optional[random.Random] = None) -> tuple:
    """Devuelve (nombre_completo, genero)"""
    r = rng or random
    genero = genero_aleatorio(r)
    if genero == "masculino":
        return nombre_completo_masculino(r), "masculino"
    return nombre_completo_femenino(r), "femenino"


def base_cotizacion_aleatoria(rng: Optional[random.Random] = None,
                               minimo: float = 1323.0,
                               maximo: float = 4000.0) -> float:
    """Base de cotización aleatoria en rango realista, redondeada a 2 decimales."""
    r = rng or random
    opciones = [1323.0, 1400.0, 1500.0, 1600.0, 1700.0, 1800.0,
                1900.0, 2000.0, 2100.0, 2200.0, 2400.0, 2500.0,
                2700.0, 2800.0, 3000.0, 3200.0, 3500.0, 3800.0, 4000.0]
    opciones_filtradas = [b for b in opciones if minimo <= b <= maximo]
    return r.choice(opciones_filtradas) if opciones_filtradas else 2000.0
