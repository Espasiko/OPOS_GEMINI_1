"""
Dispatcher - Identifica tipo de caso y extrae parámetros
"""
import re
from typing import Dict, Any, Optional
from .calculos_ss import calcular_subsidio_it


class CasosPracticosDispatcher:
    """
    Dispatcher para casos prácticos
    Identifica tipo y ejecuta calculadora apropiada
    """
    
    TIPOS_CASO = {
        "subsidio_it": ["incapacidad temporal", "it", "baja", "subsidio"],
        "cuota_ss": ["cuota", "cotización", "empresa"],
        "pension": ["pensión", "jubilación"],
        "base_reguladora": ["base reguladora"],
    }
    
    @staticmethod
    def identificar_tipo_caso(tema: str) -> str:
        """
        Identifica el tipo de caso según el tema
        
        Args:
            tema: Descripción del tema
        
        Returns:
            Tipo de caso identificado
        """
        tema_lower = tema.lower()
        
        for tipo, keywords in CasosPracticosDispatcher.TIPOS_CASO.items():
            if any(kw in tema_lower for kw in keywords):
                return tipo
        
        # Default
        return "subsidio_it"
    
    @staticmethod
    def extraer_parametros(tema: str, tipo_caso: str) -> Dict[str, Any]:
        """
        Extrae parámetros del tema
        
        Args:
            tema: Descripción del tema
            tipo_caso: Tipo de caso identificado
        
        Returns:
            Dict con parámetros extraídos
        """
        params = {}
        
        if tipo_caso == "subsidio_it":
            # Buscar base de cotización
            match_base = re.search(r'(\d+(?:\.\d+)?)\s*€?\s*(?:euros?)?', tema)
            if match_base:
                params["base_cotizacion"] = float(match_base.group(1))
            else:
                params["base_cotizacion"] = 1500.0  # Default
            
            # Buscar contingencia
            if any(word in tema.lower() for word in ["enfermedad común", "ec", "enfermedad"]):
                params["contingencia"] = "EC"
            elif any(word in tema.lower() for word in ["accidente trabajo", "at"]):
                params["contingencia"] = "AT"
            elif any(word in tema.lower() for word in ["enfermedad profesional", "ep"]):
                params["contingencia"] = "EP"
            else:
                params["contingencia"] = "EC"  # Default
            
            # Buscar día de baja
            match_dia = re.search(r'día\s*(\d+)', tema.lower())
            if match_dia:
                params["dia_baja"] = int(match_dia.group(1))
            else:
                params["dia_baja"] = 10  # Default
        
        return params
    
    @staticmethod
    def calcular(tipo_caso: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Ejecuta el cálculo apropiado
        
        Args:
            tipo_caso: Tipo de caso
            params: Parámetros del cálculo
        
        Returns:
            Resultado del cálculo o None
        """
        if tipo_caso == "subsidio_it":
            return calcular_subsidio_it(
                base=params.get("base_cotizacion", 1500.0),
                contingencia=params.get("contingencia", "EC"),
                dia=params.get("dia_baja", 10)
            )
        
        # Otros tipos no implementados aún
        return None
    
    @staticmethod
    def procesar_tema(tema: str) -> Dict[str, Any]:
        """
        Procesa un tema completo: identifica, extrae y calcula
        
        Args:
            tema: Descripción del tema
        
        Returns:
            Dict con tipo, params y resultado del cálculo
        """
        tipo = CasosPracticosDispatcher.identificar_tipo_caso(tema)
        params = CasosPracticosDispatcher.extraer_parametros(tema, tipo)
        resultado = CasosPracticosDispatcher.calcular(tipo, params)
        
        return {
            "tipo_caso": tipo,
            "parametros": params,
            "calculo": resultado
        }
