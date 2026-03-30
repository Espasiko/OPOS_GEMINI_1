"""
OpositAIA V14 — Pool de nombres, apellidos y empresas para casos diversos.
Cada llamada a las funciones produce valores distintos usando random.
"""
import random
from typing import Optional

NOMBRES_MASCULINOS = [
    "Jorge", "Antonio", "Carlos", "Manuel", "Francisco", "Pedro", "José",
    "Roberto", "Luis", "Miguel", "Alejandro", "David", "Javier", "Fernando",
    "Rafael", "Sergio", "Pablo", "Alberto", "Raúl", "Ignacio", "Enrique",
    "Tomás", "Adrián", "Marcos", "Rubén", "Iván", "Víctor", "Óscar",
]

NOMBRES_FEMENINOS = [
    "María", "Ana", "Laura", "Carmen", "Elena", "Sofía", "Lucía", "Patricia",
    "Marta", "Cristina", "Isabel", "Rosa", "Nuria", "Beatriz", "Rocío",
    "Amaia", "Silvia", "Pilar", "Andrea", "Alicia", "Natalia", "Raquel",
    "Amparo", "Dolores", "Francisca", "Concepción", "Roberta", "Verónica",
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
    "HORIZONTE", "NEBULA", "SOLARIS", "AURORA", "MERIDIAN", "VEGA",
    "ATLAS", "SIGMA", "ALTAIR", "NEXUS", "KRONOS", "ORION", "ZENITH",
    "ALTEA", "IBERIA", "CELTA", "NUMANCIA", "ALCAZAR", "TORREON",
    "LEVANTE", "PONENT", "TRAMUNTANA", "MESTRAL", "LLEVANT", "GARBI",
]

SUFIJOS_EMPRESA = [
    "SOLIDARIO", "BYTE", "TECH", "GROUP", "SOLUTIONS", "SYSTEMS",
    "CONSULTING", "SERVICES", "GLOBAL", "DIGITAL", "NETWORKS",
    "LOGISTICS", "CARGO", "METAL", "BUILD", "CONSTRUCT", "AGRO",
    "FOODS", "HEALTH", "CARE", "LEGAL", "INVEST", "CAPITAL",
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
    r = rng or random
    tipo = r.choice(TIPOS_EMPRESA)
    nombre = f"{r.choice(PREFIJOS_EMPRESA)}-{r.choice(SUFIJOS_EMPRESA)} {tipo}"
    return nombre


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
