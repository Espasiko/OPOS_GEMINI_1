"""
OpositAIA V14 — Configuración de Convocatorias
Fuente de verdad para fechas de corte, temarios y blueprints por oposición.

IMPORTANTE: Actualizar FECHA_CORTE_AGE cuando salga la convocatoria.
"""

# ─── FECHAS DE CORTE NORMATIVA ──────────────────────────────────────────────
FECHA_CORTE_SS  = "2026-03-04"   # Confirmada BOE — Administrativos SS C1 2025/2026
FECHA_CORTE_AGE = None           # Pendiente — definir cuando salga la convocatoria AGE

# ─── TEMARIOS POR OPOSICIÓN ─────────────────────────────────────────────────
# Solo blueprints generales (comunes AGE + SS)
TEMARIO_AGE = [
    "BP-G01",  # CE Estructura + Reforma
    "BP-G02",  # Derechos + Estados excepcionales
    "BP-G03",  # TC + CGPJ
    "BP-G04",  # Corona + Gobierno
    "BP-G05",  # LPAC: Actos + Nulidad + Recursos
    "BP-G06",  # LPAC: Procedimiento + Notificación electrónica
    "BP-G07",  # TREBEP: Funcionarios
    "BP-G08",  # UE + Fuentes del derecho
]

# Todos los blueprints (generales + específicos SS)
TEMARIO_SS = TEMARIO_AGE + [
    "BP-S01",  # Estructura SS + Regímenes
    "BP-S02",  # Encuadramiento RETA
    "BP-S03",  # SE Hogar + SE Mar + SE Agrario
    "BP-S04",  # Afiliación + Alta + Baja
    "BP-S05",  # Bases CC + tipos cotización 2026 (MEI + Adicional Solidaridad)
    "BP-S06",  # Recargos + intereses doble nivel
    "BP-S07",  # SLD + Recaudación ejecutiva + Embargo
    "BP-S08",  # IT-EC: tramos + LO 1/2023
    "BP-S09",  # IT-AT + RETA IT
    "BP-S10",  # IP: IPP + IPT + IPA + Gran Incapacidad (2026)
    "BP-S11",  # Nacimiento + Art. 237.3 + Riesgo (2026: 19 semanas)
    "BP-S12",  # Jubilación ordinaria 2026 (BR Dual)
    "BP-S13",  # Jubilación anticipada + activa
    "BP-S14",  # Jubilación parcial + relevo
    "BP-S15",  # Muerte + supervivencia
    "BP-S16",  # PNC + IMV + Complemento brecha (2026: 36,90€)
    "BP-S17",  # RETA: cotización + ingresos reales + IT
]

# ─── NEO4J — LABELS POR CONVOCATORIA ────────────────────────────────────────
# NOTA: Neo4j Community Edition solo tiene una base de datos activa.
# La separación SS/AGE se hace con LABELS en el mismo grafo — NO con "colecciones"
# (ese término es de Qdrant/MongoDB).
#
# Esquema de labels Neo4j:
#   (a:Articulo:SS)      → artículo exclusivo de SS (ej: Art. 173.1 TRLGSS)
#   (a:Articulo:AGE)     → artículo exclusivo de AGE (ej: Art. 47 LPAC)
#   (a:Articulo:SS:AGE)  → artículo compartido (ej: Art. 22 CE — aparece en AMBAS)
#
# Ventaja: no se duplican artículos comunes + se pueden hacer queries cruzadas.
# Propiedad `temario: ["SS", "AGE"]` para filtrar fácilmente.

NEO4J_LABEL_SS  = "SS"
NEO4J_LABEL_AGE = "AGE"
NEO4J_LABEL_COMPARTIDO = "COMPARTIDO"  # :Articulo:SS:AGE

# Leyes exclusivas SS
LEYES_SS = [
    "TRLGSS",     # RDLeg 8/2015
    "LGSS",
    "RD 1415/2004",  # Recaudación
    "RD 84/1996",    # Afiliación
    "RDL 13/2022",   # RETA ingresos reales
]

# Leyes exclusivas AGE
LEYES_AGE = [
    "LPAC",        # Ley 39/2015
    "LRJSP",       # Ley 40/2015
    "TREBEP",      # RDLeg 5/2015
]

# Leyes compartidas SS + AGE
LEYES_COMPARTIDAS = [
    "CE",          # Constitución Española
    "TUE",         # Tratado UE
    "TFUE",        # Tratado funcionamiento UE
    "LO 3/2007",   # Igualdad
    "LO 4/2023",   # LGTBI
    "RGPD",        # Protección de datos
    "LO 3/2018",   # LOPD
]

# ─── QDRANT — COLECCIONES POR OPOSICIÓN ─────────────────────────────────────
# En Qdrant SÍ se pueden tener colecciones separadas (coste cero, simplicidad)
QDRANT_COLLECTION_SS  = "opositaia_knowledge_FULL_XML"   # Ya existe ✅
QDRANT_COLLECTION_AGE = "opositaia_knowledge_AGE"         # Crear cuando se lance AGE

# ─── URLs BOE — SNAPSHOT CON FECHA DE CORTE ─────────────────────────────────
# Usar `?p=AAAAMMDD` para obtener el texto de la ley TAL COMO ESTABA en esa fecha
# Esto incluye todas las modificaciones anteriores a esa fecha (snapshot consolidado)
BOE_SNAPSHOT_TRLGSS_SS = (
    f"https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
    f"&p={FECHA_CORTE_SS.replace('-', '')}&tn=1"
)

def get_fecha_corte(oposicion: str) -> str:
    """Devuelve la fecha de corte para la oposición indicada."""
    if oposicion.upper() == "SS":
        return FECHA_CORTE_SS
    elif oposicion.upper() == "AGE":
        if FECHA_CORTE_AGE is None:
            raise ValueError(
                "FECHA_CORTE_AGE no definida — actualizar cuando salga la convocatoria AGE"
            )
        return FECHA_CORTE_AGE
    raise ValueError(f"Oposición desconocida: {oposicion}. Usar 'SS' o 'AGE'.")


def get_temario(oposicion: str) -> list:
    """Devuelve la lista de blueprint IDs para la oposición indicada."""
    if oposicion.upper() == "SS":
        return TEMARIO_SS
    elif oposicion.upper() == "AGE":
        return TEMARIO_AGE
    raise ValueError(f"Oposición desconocida: {oposicion}. Usar 'SS' o 'AGE'.")
