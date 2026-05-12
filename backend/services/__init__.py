"""
Backend services package
"""

from .boe_service import BOEService, get_boe_service, LawData, Metadatos, AnalisisData, Referencia

__all__ = [
    "BOEService",
    "get_boe_service", 
    "LawData",
    "Metadatos",
    "AnalisisData",
    "Referencia"
]
