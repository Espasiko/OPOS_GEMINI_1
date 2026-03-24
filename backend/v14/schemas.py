"""
OpositAIA V14 — Dataclasses base del Schema-First Pipeline
Fuente de verdad: Python genera hechos legales, LLM escribe prosa alrededor.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ArticuloVerificado:
    """Artículo legal verificado — existencia y vigencia confirmadas."""
    id: str                      # "Art. 173.1 TRLGSS"
    ley: str                     # "TRLGSS"
    texto_literal: str           # Primer párrafo del artículo (del BOE / Qdrant)
    vigente: bool = True
    url_boe: str = ""
    fecha_vigencia: str = ""     # "2026-01-01"
    derogado_por: Optional[str] = None


@dataclass
class Calculadora:
    """Resultado de una calculadora Python — determinístico, no alucinable."""
    nombre: str                  # "it_ec_subsidio"
    parametros: Dict[str, Any] = field(default_factory=dict)
    resultado: Optional[Any] = None
    formula_python: str = ""     # Representación textual de la fórmula
    verificado: bool = False


@dataclass
class TrampaSchema:
    """Trampa del catálogo — datos precisos para construir la pregunta engañosa."""
    trampa_id: str               # "C4", "DM-T4-001"
    trampa: str                  # Descripción de la trampa
    valor_correcto: str          # Lo que realmente dice la ley
    distractor_tipico: str       # El error que suele cometerse
    articulo: str                # Artículo que la sustenta
    url_boe: str = ""
    mnemonico: str = ""          # Máx. 15 palabras
    origen: str = "catalogo"     # "catalogo" | "temario-DM-2026" | "simulacro-academia"
    obsoleto: bool = False       # True si la fórmula/dato cambió en 2026
    cambio_dm_2026: bool = False # True si es un cambio legislativo específico 2026


@dataclass
class QuestionSchema:
    """Schema de una pregunta — hechos fijados antes de que el LLM escriba nada."""
    pregunta_id: str             # "P1" ... "P18"
    tipo: str                    # "calculo" | "trampa" | "critica" | "normativa"
    articulo_clave: str          # "Art. 173.1 TRLGSS" (verificado)
    trampa: Optional[TrampaSchema] = None
    calculadora: Optional[Calculadora] = None
    calculo_resultado: Optional[str] = None   # resultado final para Prose Validator
    url_boe: str = ""
    mnemonico: str = ""          # Máx. 15 palabras
    opciones_abcd: Optional[List[str]] = None
    respuesta_correcta: Optional[str] = None
    verified: bool = False


@dataclass
class PersonajeSchema:
    """Personaje del caso — datos fijados en el schema."""
    nombre: str
    regimen: str                 # "RG" | "RETA" | "SE_HOGAR"
    situacion_laboral: str       # "alta" | "baja" | "desempleo"
    datos: Dict[str, Any] = field(default_factory=dict)  # bc, años_cotizados, etc.
    aparece_en_preguntas: List[str] = field(default_factory=list)  # ["P1", "P3", "P7"]


@dataclass
class CaseSchema:
    """Schema completo del caso — generado 100% por Python antes de llamar al LLM."""
    case_id: str
    blueprint_id: str            # "BP-S12" | "jubilacion"
    personajes: List[PersonajeSchema] = field(default_factory=list)  # mín. 7
    empresa_sector: str = ""
    fecha_caso: str = "2026-03-01"
    fecha_corte: str = "2026-03-04"
    questions: List[QuestionSchema] = field(default_factory=list)
    articulos_verificados: List[ArticuloVerificado] = field(default_factory=list)
    validated: bool = False      # True solo si pasa todos los sieves
    score_boe: float = 0.0
    score_math: float = 0.0
    score_pedagogy: float = 0.0
    score_trampas: float = 0.0
    score_interdependencia: float = 0.0


@dataclass
class TopicBlueprint:
    """
    Blueprint de un tema — especifica los artículos, calculadoras y trampas
    obligatorias para ese blueprint. El CaseSchemaBuilder lo usa para generar
    el CaseSchema sin depender del LLM en ningún momento.
    """
    id: str                      # "BP-S12"
    tema: str                    # "Jubilación ordinaria 2026"
    temas_oficiales: List[str] = field(default_factory=list)   # ["TE10"]
    normativa_base: List[str] = field(default_factory=list)    # leyes que cubre

    articulos_obligatorios: List[str] = field(default_factory=list)
    # Artículos que DEBEN verificarse en Qdrant/Neo4j. Si no existen → caso inválido.

    articulos_forbidden: List[str] = field(default_factory=list)
    # Artículos que NO deben aparecer (ej: "Art. 206 bis" — no existe).

    calculadoras: List[str] = field(default_factory=list)
    # Nombres de las calculadoras del dispatcher que aplican.

    trampas_tipicas: List[str] = field(default_factory=list)
    # IDs de trampas del catálogo que suelen aparecer en este tema.

    cambios_dm_2026: List[Dict[str, str]] = field(default_factory=list)
    # Cambios legislativos DM 2026 que aplican a este blueprint.
    # Formato: {"campo": "mei_pct", "valor_2025": "0.80", "valor_2026": "0.90",
    #           "trampa_id": "DM-T4-001", "mnemonico": "MEI sube a 0,90% en 2026"}

    eval_questions: List[Dict[str, str]] = field(default_factory=list)
    # 5 preguntas de evaluación CI para este blueprint.

    num_preguntas_caso: int = 18      # 15 + 3 reserva
    min_personajes: int = 7
    version: str = "2026.1"
    notas: str = ""
