"""
Metadata Schema for OpositaIA RAG System
Defines structure for 3-layer architecture
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field
from datetime import date

class DocumentMetadata(BaseModel):
    """
    Schema de metadata para documentos indexados en Qdrant
    
    3 Capas:
    - Layer 1: Normativa Oficial (leyes, RD, órdenes)
    - Layer 2: Jurisprudencia y Doctrina (STS, TSJ, comentarios)
    - Layer 3: Materiales de Estudio (tests, casos, temarios)
    """
    
    # ===== IDENTIFICACIÓN DE CAPA =====
    layer: Literal[1, 2, 3] = Field(
        description="1=Normativa, 2=Jurisprudencia, 3=Materiales"
    )
    nivel_jerarquia: Literal[1, 2, 3] = Field(
        description="Para reranking: 1=más importante, 3=menos"
    )
    
    # ===== TIPO DE DOCUMENTO =====
    tipo: str = Field(
        description="ley, real_decreto, sentencia_sts, test, caso_practico, etc."
    )
    
    # ===== INFORMACIÓN TEMPORAL =====
    fecha: Optional[date] = Field(
        None,
        description="Fecha de publicación/creación"
    )
    fecha_vigencia: Optional[date] = Field(
        None,
        description="Fecha de entrada en vigor"
    )
    fecha_derogacion: Optional[date] = Field(
        None,
        description="Fecha de derogación (si aplica)"
    )
    
    # ===== REFERENCIAS NORMATIVAS =====
    norma_id: Optional[str] = Field(
        None,
        description="ID BOE: BOE-A-2015-11724"
    )
    articulo: Optional[str] = Field(
        None,
        description="Número de artículo: 212"
    )
    norma_modificadora: Optional[str] = Field(
        None,
        description="Norma que modifica este documento"
    )
    
    # ===== JURISPRUDENCIA =====
    tribunal: Optional[str] = Field(
        None,
        description="Tribunal Supremo, TSJ Madrid, etc."
    )
    superada_por: Optional[str] = Field(
        None,
        description="Sentencia que supera esta doctrina"
    )
    
    # ===== MATERIALES DE ESTUDIO =====
    fuente: Optional[str] = Field(
        None,
        description="Academia Las Cortes, Ediciones Rodio, etc."
    )
    tema: Optional[str] = Field(
        None,
        description="Número de tema: 8"
    )
    formato: Optional[str] = Field(
        None,
        description="pregunta_respuesta, caso_completo, esquema, etc."
    )
    
    # ===== CONTENIDO =====
    text: str = Field(
        description="Texto del chunk"
    )
    chunk_id: int = Field(
        description="ID del chunk dentro del documento"
    )
    total_chunks: int = Field(
        description="Total de chunks del documento"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "layer": 1,
                "nivel_jerarquia": 1,
                "tipo": "ley",
                "fecha": "2015-10-30",
                "fecha_vigencia": "2016-01-02",
                "norma_id": "BOE-A-2015-11724",
                "articulo": "212",
                "text": "Artículo 212. Jubilación ordinaria. 1. Tendrán derecho...",
                "chunk_id": 1,
                "total_chunks": 5
            }
        }

# ===== EJEMPLOS DE USO =====

# Ejemplo 1: Ley (Capa 1)
metadata_ley = DocumentMetadata(
    layer=1,
    nivel_jerarquia=1,
    tipo="ley",
    fecha=date(2015, 10, 30),
    fecha_vigencia=date(2016, 1, 2),
    norma_id="BOE-A-2015-11724",
    articulo="212",
    text="Artículo 212. Jubilación ordinaria...",
    chunk_id=1,
    total_chunks=5
)

# Ejemplo 2: Sentencia STS (Capa 2)
metadata_sentencia = DocumentMetadata(
    layer=2,
    nivel_jerarquia=2,
    tipo="sentencia_sts",
    fecha=date(2024, 6, 15),
    tribunal="Tribunal Supremo",
    text="El Tribunal Supremo establece que...",
    chunk_id=1,
    total_chunks=3
)

# Ejemplo 3: Test (Capa 3)
metadata_test = DocumentMetadata(
    layer=3,
    nivel_jerarquia=3,
    tipo="test",
    fecha=date(2024, 11, 1),
    fuente="Academia Las Cortes",
    tema="8",
    formato="pregunta_respuesta",
    text="PREGUNTA 1: ¿Cuál es la edad mínima para jubilación ordinaria?",
    chunk_id=1,
    total_chunks=1
)
