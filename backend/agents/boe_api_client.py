"""
Cliente Python para la API oficial de datos abiertos del BOE.
Documentación: https://www.boe.es/datosabiertos/api/api.php

Endpoints disponibles:
- Legislación consolidada: /datosabiertos/api/legislacion/*
- Sumarios BOE: /datosabiertos/api/boe/sumario/*
- Documentos BOE: /datosabiertos/api/boe/documento/*
- Datos auxiliares: /datosabiertos/api/datos-auxiliares/*
"""

import httpx
import logging
from typing import Optional, Dict, List
from datetime import datetime
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class BOEApiClient:
    """Cliente para interactuar con la API oficial de datos abiertos del BOE."""
    
    BASE_URL = "https://www.boe.es/datosabiertos/api"
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        # Headers requeridos por la API de datos abiertos del BOE
        headers = {
            "Accept": "application/xml",
            "User-Agent": "OpositaIA-Bot/1.0 (Spanish Law Study App)"
        }
        self.client = httpx.Client(timeout=timeout, headers=headers)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
    
    # ==========================================
    # LEGISLACIÓN CONSOLIDADA
    # ==========================================
    
    def get_legislacion_consolidada(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        query: Optional[Dict] = None,
        offset: int = 0,
        limit: int = 50
    ) -> Dict:
        """
        Obtiene lista de legislación consolidada.
        
        Args:
            from_date: Fecha inicio en formato YYYYMMDD
            to_date: Fecha fin en formato YYYYMMDD
            query: Diccionario con criterios de búsqueda
            offset: Primer resultado a devolver
            limit: Número máximo de resultados (-1 para todos)
        
        Returns:
            Dict con la respuesta de la API (XML parseado a dict)
        """
        url = f"{self.BASE_URL}/legislacion-consolidada"
        params = {
            "offset": offset,
            "limit": limit
        }
        
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if query:
            import json
            params["query"] = json.dumps(query)
        
        headers = {"Accept": "application/xml"}
        
        logger.info(f"Consultando legislación consolidada: {params}")
        response = self.client.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        return self._parse_xml_response(response.text)
    
    def get_documento_consolidado(self, id_norma: str) -> Dict:
        """
        Obtiene un documento consolidado completo (metadatos + análisis + texto).
        
        Args:
            id_norma: Identificador BOE (ej: "BOE-A-2015-11724")
        
        Returns:
            Dict con metadatos, análisis, metadata-eli y texto consolidado
        """
        url = f"{self.BASE_URL}/legislacion-consolidada/id/{id_norma}"
        
        logger.info(f"Descargando documento consolidado completo: {id_norma}")
        response = self.client.get(url)
        response.raise_for_status()
        
        return self._parse_xml_response(response.text)
    
    def get_metadatos(self, id_norma: str, formato: str = "xml") -> Dict:
        """
        Obtiene solo los metadatos de un documento consolidado.
        
        Args:
            id_norma: Identificador BOE (ej: "BOE-A-2015-11724")
            formato: "xml" o "json"
        
        Returns:
            Dict con los metadatos del documento
        """
        url = f"{self.BASE_URL}/legislacion-consolidada/id/{id_norma}/metadatos"
        
        headers = {}
        if formato == "json":
            headers["Accept"] = "application/json"
        else:
            headers["Accept"] = "application/xml"
        
        logger.info(f"Descargando metadatos de {id_norma} en formato {formato}")
        response = self.client.get(url, headers=headers)
        response.raise_for_status()
        
        if formato == "json":
            return response.json()
        else:
            return self._parse_xml_response(response.text)
    
    def get_texto_consolidado(self, id_norma: str) -> str:
        """
        Obtiene el texto consolidado completo de un documento (todas las versiones).
        
        Args:
            id_norma: Identificador BOE (ej: "BOE-A-2015-11724")
        
        Returns:
            XML con el texto consolidado completo
        """
        url = f"{self.BASE_URL}/legislacion-consolidada/id/{id_norma}/texto"
        
        headers = {"Accept": "application/xml"}
        
        logger.info(f"Descargando texto consolidado de {id_norma}")
        response = self.client.get(url, headers=headers)
        response.raise_for_status()
        
        return response.text
    
    def get_indice_texto(self, id_norma: str, formato: str = "xml") -> Dict:
        """
        Obtiene el índice del texto consolidado (lista de bloques/artículos).
        
        Args:
            id_norma: Identificador BOE (ej: "BOE-A-2015-11724")
            formato: "xml" o "json"
        
        Returns:
            Dict con el índice de bloques del texto
        """
        url = f"{self.BASE_URL}/legislacion-consolidada/id/{id_norma}/texto/indice"
        
        headers = {}
        if formato == "json":
            headers["Accept"] = "application/json"
        else:
            headers["Accept"] = "application/xml"
        
        logger.info(f"Descargando índice de {id_norma} en formato {formato}")
        response = self.client.get(url, headers=headers)
        response.raise_for_status()
        
        if formato == "json":
            return response.json()
        else:
            return self._parse_xml_response(response.text)
    
    def get_bloque_texto(self, id_norma: str, id_bloque: str) -> str:
        """
        Obtiene un bloque específico del texto consolidado.
        
        Args:
            id_norma: Identificador BOE (ej: "BOE-A-2015-11724")
            id_bloque: ID del bloque (ej: "a1", "a2", "pr")
        
        Returns:
            XML con el bloque específico (todas sus versiones)
        """
        url = f"{self.BASE_URL}/legislacion-consolidada/id/{id_norma}/texto/bloque/{id_bloque}"
        
        logger.info(f"Descargando bloque {id_bloque} de {id_norma}")
        response = self.client.get(url)
        response.raise_for_status()
        
        return response.text
    
    # ==========================================
    # SUMARIOS BOE
    # ==========================================
    
    def get_sumario(self, fecha: str) -> Dict:
        """
        Obtiene el sumario del BOE para una fecha específica.
        
        Args:
            fecha: Fecha en formato YYYYMMDD
        
        Returns:
            Dict con el sumario del día
        """
        url = f"{self.BASE_URL}/boe/sumario/{fecha}"
        
        logger.info(f"Consultando sumario BOE del {fecha}")
        response = self.client.get(url)
        response.raise_for_status()
        
        return self._parse_xml_response(response.text)
    
    def get_documento_boe(self, id_documento: str, formato: str = "xml") -> str:
        """
        Descarga un documento del BOE.
        
        Args:
            id_documento: Identificador del documento (ej: "BOE-A-2015-11724")
            formato: "xml", "json" o "pdf"
        
        Returns:
            Contenido del documento
        """
        url = f"{self.BASE_URL}/boe/documento/{id_documento}"
        
        logger.info(f"Descargando documento BOE {id_documento} en formato {formato}")
        
        if formato == "json":
            response = self.client.get(f"{url}.json")
        elif formato == "pdf":
            response = self.client.get(f"{url}.pdf")
        else:
            response = self.client.get(url)  # XML por defecto
        
        response.raise_for_status()
        
        if formato == "json":
            return response.json()
        elif formato in ["xml", "pdf"]:
            return response.content if formato == "pdf" else response.text
    
    # ==========================================
    # UTILIDADES
    # ==========================================
    
    def _parse_xml_response(self, xml_text: str) -> Dict:
        """
        Parsea una respuesta XML de la API del BOE.
        
        Args:
            xml_text: Texto XML de la respuesta
        
        Returns:
            Dict con los datos parseados
        """
        try:
            root = ET.fromstring(xml_text)
            return self._element_to_dict(root)
        except ET.ParseError as e:
            logger.error(f"Error parseando XML: {e}")
            return {"raw_xml": xml_text, "error": str(e)}
    
    def _element_to_dict(self, element: ET.Element) -> Dict:
        """Convierte un elemento XML a diccionario."""
        result = {}
        
        # Atributos
        if element.attrib:
            result.update(element.attrib)
        
        # Texto
        if element.text and element.text.strip():
            result["_text"] = element.text.strip()
        
        # Hijos
        for child in element:
            child_data = self._element_to_dict(child)
            
            if child.tag in result:
                # Si ya existe, convertir a lista
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result


# ==========================================
# FUNCIONES DE UTILIDAD
# ==========================================

def descargar_lgss_consolidada(guardar_en: str = "backend/data/leyes/LGSS_consolidada.xml") -> str:
    """
    Descarga la Ley General de la Seguridad Social consolidada desde la API del BOE.
    
    Args:
        guardar_en: Ruta donde guardar el archivo XML
    
    Returns:
        Ruta del archivo guardado
    """
    LGSS_BOE_ID = "BOE-A-2015-11724"
    
    with BOEApiClient() as client:
        xml_content = client.get_texto_consolidado(LGSS_BOE_ID)
        
        with open(guardar_en, "w", encoding="utf-8") as f:
            f.write(xml_content)
        
        logger.info(f"LGSS consolidada descargada en {guardar_en}")
        return guardar_en


if __name__ == "__main__":
    # Test básico
    logging.basicConfig(level=logging.INFO)
    
    print("=== Test API BOE ===\n")
    
    with BOEApiClient() as client:
        # Test 1: Obtener lista de legislación consolidada
        print("1. Obteniendo lista de legislación consolidada (primeras 5)...")
        legislacion = client.get_legislacion_consolidada(limit=5)
        print(f"   Lista obtenida: {bool(legislacion)}\n")
        
        # Test 2: Descargar metadatos LGSS
        print("2. Descargando metadatos LGSS...")
        metadatos = client.get_metadatos("BOE-A-2015-11724", formato="json")
        print(f"   Metadatos obtenidos: {bool(metadatos)}\n")
        
        # Test 3: Descargar índice LGSS
        print("3. Obteniendo índice de artículos LGSS...")
        indice = client.get_indice_texto("BOE-A-2015-11724", formato="json")
        print(f"   Índice obtenido con {len(indice.get('data', {}))} bloques\n")
        
        # Test 4: Descargar texto consolidado completo
        print("4. Descargando texto consolidado LGSS...")
        texto_xml = client.get_texto_consolidado("BOE-A-2015-11724")
        print(f"   Tamaño XML texto: {len(texto_xml)} caracteres\n")
    
    print("=== Tests completados ===")
    
    # Test 5: Guardar LGSS completa
    print("\n5. Guardando LGSS consolidada en archivo...")
    ruta = descargar_lgss_consolidada()
    print(f"   Guardado en: {ruta}")
