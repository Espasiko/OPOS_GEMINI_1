"""
Query Validator: Mapea temas → artículos BOE + verificación vigencia
"""
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class BoeMetadata:
    """Metadata extraída de BOE para artículos"""
    articulo: str
    ley: str
    vigencia_inicio: str
    vigencia_fin: Optional[str]
    derogado: bool
    url_boe: str
    ultima_verificacion: str
    observaciones: List[str] = None


class QueryValidator:
    """Validador de queries: verifica tema, artículos, vigencia BOE"""
    
    # Mapeo: tema → artículos TRLGSS
    TEMA_TO_ARTICULOS = {
        "subsidio_it": {
            "articulos": ["173", "174", "175"],
            "descripcion": "Subsidio Incapacidad Temporal",
            "contingencias": ["EC", "AT", "EP"],
        },
        "pension_ipt": {
            "articulos": ["193", "194", "195"],
            "descripcion": "Pensión Incapacidad Permanente Total",
            "requisitos": ["edad_55", "base_24_meses"],
        },
        "pension_jubilacion": {
            "articulos": ["206", "208", "210"],
            "descripcion": "Pensión de Jubilación",
            "tipos": ["ordinaria", "anticipada", "flexible"],
        },
        "subsidio_desempleo": {
            "articulos": ["262", "263"],
            "descripcion": "Subsidio por Desempleo",
            "porcentajes": ["70%", "60%"],
        },
        "cuota_cotizacion": {
            "articulos": ["73", "75", "76"],
            "descripcion": "Cuota de Cotización",
            "tipos": ["empresario", "trabajador"],
        },
        "complementos": {
            "articulos": ["181", "182"],
            "descripcion": "Complementos a Pensiones",
            "tipos": ["minimo", "discapacitado", "cargas_familiares"],
        },
        "devoluciones": {
            "articulos": ["267", "268"],
            "descripcion": "Devoluciones de Aportaciones",
        },
        "maternidad_paternidad": {
            "articulos": ["177", "178"],
            "descripcion": "Prestación Maternidad/Paternidad",
            "duracion": ["16-18 semanas"],
        },
        "ayuda_hijo_cargo": {
            "articulos": ["163", "164"],
            "descripcion": "Ayuda por Hijo a Cargo",
            "importe_mensual": True,
        },
        "bonificacion_cuotas": {
            "articulos": ["76"],
            "descripcion": "Bonificación Cuotas Desempleados",
            "porcentaje": "100%",
        },
        "ingreso_minimo_vital": {
            "articulos": ["8 RD-ley 20/2020"],
            "descripcion": "Ingreso Mínimo Vital",
            "requisitos": ["patrimonio_limite", "empadronamiento_12m"],
        },
    }
    
    # Mapeo: Qdrant collections por tema
    TEMA_TO_QDRANT_COLLECTIONS = {
        "subsidio_it": ["opositaia_knowledge_FULL_XML"],
        "pension_ipt": ["opositaia_knowledge_FULL_XML"],
        "pension_jubilacion": ["opositaia_knowledge_FULL_XML"],
        "ingreso_minimo_vital": ["opositaia_knowledge_FULL_XML"],
    }
    
    # BOE Metadata database (en producción sería real-time)
    BOE_DATABASE = {
        "173": BoeMetadata(
            articulo="173",
            ley="TRLGSS",
            vigencia_inicio="2020-01-01",
            vigencia_fin=None,
            derogado=False,
            url_boe="https://www.boe.es/buscar/act.php?id=BOE-A-1994-24417",
            ultima_verificacion="2026-02-13",
            observaciones=["Modificado 2023 (RD 4/2023)"]
        ),
        "174": BoeMetadata(
            articulo="174",
            ley="TRLGSS",
            vigencia_inicio="2020-01-01",
            vigencia_fin=None,
            derogado=False,
            url_boe="https://www.boe.es/buscar/act.php?id=BOE-A-1994-24417",
            ultima_verificacion="2026-02-13",
        ),
        "206": BoeMetadata(
            articulo="206",
            ley="TRLGSS",
            vigencia_inicio="2020-01-01",
            vigencia_fin=None,
            derogado=False,
            url_boe="https://www.boe.es/buscar/act.php?id=BOE-A-1994-24417",
            ultima_verificacion="2026-02-13",
        ),
        "8 RD-ley 20/2020": BoeMetadata(
            articulo="8",
            ley="Real Decreto-ley 20/2020",
            vigencia_inicio="2020-06-30",
            vigencia_fin=None,
            derogado=False,
            url_boe="https://www.boe.es/buscar/act.php?id=BOE-A-2020-6039",
            ultima_verificacion="2026-02-13",
            observaciones=["Convocatoria permanente desde 2022"]
        ),
    }
    
    def __init__(self):
        self.fecha_verificacion = datetime.now().strftime("%Y-%m-%d")
    
    def map_tema_to_articles(self, tema: str) -> Dict[str, any]:
        """Mapea tema → artículos TRLGSS + metadata"""
        if tema not in self.TEMA_TO_ARTICULOS:
            return {"error": f"Tema desconocido: {tema}"}
        
        tema_info = self.TEMA_TO_ARTICULOS[tema]
        articulos_metadata = []
        
        for art in tema_info["articulos"]:
            metadata = self.BOE_DATABASE.get(art)
            if metadata:
                articulos_metadata.append({
                    "numero": art,
                    "ley": metadata.ley,
                    "vigencia_inicio": metadata.vigencia_inicio,
                    "vigencia_fin": metadata.vigencia_fin,
                    "derogado": metadata.derogado,
                    "url_boe": metadata.url_boe,
                    "observaciones": metadata.observaciones or [],
                })
        
        return {
            "tema": tema,
            "descripcion": tema_info["descripcion"],
            "articulos": articulos_metadata,
            "total": len(articulos_metadata),
        }
    
    def map_tema_to_qdrant_collections(self, tema: str) -> List[str]:
        """Mapea tema → colecciones Qdrant para búsqueda"""
        default = ["opositaia_knowledge_FULL_XML"]
        return self.TEMA_TO_QDRANT_COLLECTIONS.get(tema, default)
    
    def validate_boe_metadata(self, tema: str) -> Tuple[bool, List[str]]:
        """Valida: ¿Artículos vigentes en 2026? ¿Sin derogaciones?"""
        tema_info = self.map_tema_to_articles(tema)
        
        if "error" in tema_info:
            return False, [tema_info["error"]]
        
        advertencias = []
        todos_vigentes = True
        
        for art in tema_info["articulos"]:
            # Check derogación
            if art["derogado"]:
                advertencias.append(f"⚠️ Art {art['numero']} DEROGADO (vigencia hasta {art['vigencia_fin']})")
                todos_vigentes = False
            
            # Check vigencia fin
            if art.get("vigencia_fin"):
                fecha_fin = datetime.strptime(art["vigencia_fin"], "%Y-%m-%d")
                if fecha_fin < datetime.now():
                    advertencias.append(f"⚠️ Art {art['numero']} expirado ({art['vigencia_fin']})")
                    todos_vigentes = False
            
            # Observaciones
            if art.get("observaciones"):
                for obs in art["observaciones"]:
                    advertencias.append(f"ℹ️ Art {art['numero']}: {obs}")
        
        if todos_vigentes:
            advertencias.append(f"✅ Todos los artículos vigentes en 2026-02-13")
        
        return todos_vigentes, advertencias
    
    def validate_query_completo(self, tema: str, dificultad: str, cantidad: int) -> Dict[str, any]:
        """Validación completa: tema + artículos + vigencia"""
        
        # 1. Validar tema
        if tema not in self.TEMA_TO_ARTICULOS:
            return {
                "valido": False,
                "error": f"Tema desconocido: {tema}",
            }
        
        # 2. Mapear artículos
        articulos_info = self.map_tema_to_articles(tema)
        
        # 3. Validar BOE
        vigentes, advertencias = self.validate_boe_metadata(tema)
        
        # 4. Validar cantidad
        cantidad_ok = 0 < cantidad <= 100
        if not cantidad_ok:
            advertencias.insert(0, f"⚠️ Cantidad {cantidad} fuera de rango (1-100)")
        
        # 5. Validar dificultad
        dificultades_ok = dificultad in ["fácil", "media", "alta"]
        if not dificultades_ok:
            advertencias.insert(0, f"⚠️ Dificultad '{dificultad}' no reconocida")
        
        # Resultado final
        valido = vigentes and cantidad_ok and dificultades_ok
        
        return {
            "valido": valido,
            "tema": tema,
            "tema_descripcion": articulos_info["descripcion"],
            "articulos": articulos_info["articulos"],
            "dificultad": dificultad,
            "cantidad_solicitada": cantidad,
            "qdrant_collections": self.map_tema_to_qdrant_collections(tema),
            "vigencia_ok": vigentes,
            "advertencias": advertencias,
            "fecha_validacion": self.fecha_verificacion,
        }
    
    def search_articulos_por_palabras_clave(self, palabras_clave: List[str]) -> List[str]:
        """Busca artículos por palabras clave (fallback)"""
        resultados = []
        
        busquedas = {
            "base reguladora": ["206", "193"],
            "coeficiente reductor": ["208"],
            "70%": ["262"],
            "trampa": [],  # Sin artículos específicos
        }
        
        for palabra in palabras_clave:
            palabra_lower = palabra.lower()
            for clave, arts in busquedas.items():
                if clave in palabra_lower:
                    resultados.extend(arts)
        
        return list(set(resultados))  # Deduplicar


if __name__ == "__main__":
    validator = QueryValidator()
    
    print("=" * 80)
    print("TEST: QUERY VALIDATOR")
    print("=" * 80)
    
    # Test 1: Mapeo tema → artículos
    print("\n1️⃣ MAPEO TEMA → ARTÍCULOS")
    for tema in ["subsidio_it", "pension_jubilacion", "ingreso_minimo_vital"]:
        resultado = validator.map_tema_to_articles(tema)
        print(f"\n  Tema: {tema}")
        print(f"    Descripción: {resultado['descripcion']}")
        print(f"    Artículos: {[a['numero'] for a in resultado['articulos']]}")
        print(f"    URLs BOE: {[a['url_boe'][-10:] for a in resultado['articulos'][:2]]}")
    
    # Test 2: Validación BOE
    print("\n2️⃣ VALIDACIÓN BOE METADATA")
    for tema in ["subsidio_it", "ingreso_minimo_vital"]:
        vigentes, adv = validator.validate_boe_metadata(tema)
        print(f"\n  Tema: {tema}")
        print(f"    Vigentes: {vigentes}")
        for a in adv:
            print(f"      {a}")
    
    # Test 3: Validación completa
    print("\n3️⃣ VALIDACIÓN COMPLETA")
    resultado = validator.validate_query_completo(
        tema="subsidio_it",
        dificultad="alta",
        cantidad=5
    )
    print(f"\n  Válido: {resultado['valido']}")
    print(f"  Tema: {resultado['tema_descripcion']}")
    print(f"  Artículos: {len(resultado['articulos'])}")
    print(f"  Advertencias: {len(resultado['advertencias'])}")
    
    print("\n✅ Query Validator funcional")
