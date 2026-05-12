"""
BOE Service - Servicio unificado para fetch de leyes BOE
Extracción completa de XML (excepto metadata-eli) con 4 fallbacks
"""

import httpx
import logging
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import re

logger = logging.getLogger(__name__)


@dataclass
class Referencia:
    """Referencia normativa (relación entre leyes)"""
    id_norma: str
    relacion: str  # DEROGA, MODIFICA, AÑADE, etc.
    codigo: str    # Código numérico del BOE
    texto: str
    
    def to_dict(self) -> Dict:
        return {
            "id_norma": self.id_norma,
            "relacion": self.relacion,
            "codigo": self.codigo,
            "texto": self.texto
        }


@dataclass
class AnalisisData:
    """Datos completos del análisis BOE"""
    materias: List[str] = field(default_factory=list)
    notas: str = ""
    referencias_anteriores: List[Referencia] = field(default_factory=list)
    referencias_posteriores: List[Referencia] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "materias": self.materias,
            "notas": self.notas,
            "referencias_anteriores": [r.to_dict() for r in self.referencias_anteriores],
            "referencias_posteriores": [r.to_dict() for r in self.referencias_posteriores]
        }


@dataclass
class Metadatos:
    """Metadatos de una ley BOE"""
    boe_id: str
    titulo: str
    departamento: str
    rango: str
    numero_oficial: str
    fecha_disposicion: str
    fecha_publicacion: str
    fecha_vigencia: str
    estado_consolidacion: str
    estatus_derogacion: str
    ambito: str = ""
    url_html: str = ""
    url_eli: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "boe_id": self.boe_id,
            "titulo": self.titulo,
            "departamento": self.departamento,
            "rango": self.rango,
            "numero_oficial": self.numero_oficial,
            "fecha_disposicion": self.fecha_disposicion,
            "fecha_publicacion": self.fecha_publicacion,
            "fecha_vigencia": self.fecha_vigencia,
            "estado_consolidacion": self.estado_consolidacion,
            "estatus_derogacion": self.estatus_derogacion,
            "ambito": self.ambito,
            "url_html": self.url_html,
            "url_eli": self.url_eli
        }


@dataclass
class LawData:
    """Datos completos de una ley (texto + análisis + metadatos)"""
    boe_id: str
    texto_xml: Optional[str]  # XML completo del texto
    texto_html: Optional[str]  # Texto scrapeado del HTML
    metadatos: Metadatos
    analisis: AnalisisData
    source: str  # Origen de los datos
    
    def to_dict(self) -> Dict:
        return {
            "boe_id": self.boe_id,
            "texto_xml": self.texto_xml,
            "texto_html": self.texto_html,
            "metadatos": self.metadatos.to_dict(),
            "analisis": self.analisis.to_dict(),
            "source": self.source
        }


class BOEService:
    """
    Servicio unificado para fetch de leyes BOE.
    Fallback 4 fuentes: caché → XML consolidado → XML diario → HTML scraping
    Extracción completa del análisis (excepto metadata-eli)
    """
    
    # URLs base
    BASE_URL = "https://www.boe.es/datosabiertos/api"
    BOE_BASE = "https://www.boe.es"
    
    # Caché local
    CACHE_DIR = Path("/home/spas/OPOS_GEMINI_1/data/boe_xml")
    
    # Mapeo códigos BOE → tipo relación
    RELACION_MAP = {
        "210": "DEROGA",
        "270": "MODIFICA",
        "407": "AÑADE",
        "231": "SUSPENDE",
        "470": "DECLARA_INCONSTITUCIONAL",
        "230": "SIN_EFECTO",
        "440": "DESARROLLO",
        "201": "CORRIGE",
        "203": "CORRIGE",
        "331": "RELACION",
        "450": "INTERPRETA"
    }
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            "Accept": "application/xml",
            "User-Agent": "OpositaIA-Bot/1.0 (Spanish Law Study App)"
        }
        # Asegurar que existe el directorio de caché
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    def _extract_text(self, element) -> str:
        """Extrae texto de un elemento XML, manejando _text"""
        if element is None:
            return ""
        if isinstance(element, dict):
            return element.get("_text", "")
        return str(element)
    
    def _normalize_dict(self, data: Any) -> Any:
        """Normaliza estructuras del XML parseado"""
        if isinstance(data, dict):
            # Si solo tiene _text, devolver el texto
            if "_text" in data and len(data) == 1:
                return data["_text"]
            # Si tiene _text y otros campos, devolver dict completo
            return {k: self._normalize_dict(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._normalize_dict(item) for item in data]
        return data
    
    # ==========================================
    # FETCH PRINCIPAL CON FALLBACK
    # ==========================================
    
    async def fetch_law_complete(self, boe_id: str) -> Optional[LawData]:
        """
        Obtiene datos completos de una ley con fallback de 4 fuentes:
        1. Caché local
        2. API XML consolidado
        3. XML diario BOE
        4. HTML scraping
        
        Returns:
            LawData con texto, metadatos y análisis completos
        """
        logger.info(f"🔍 Fetching law {boe_id}...")
        
        # 1. Caché local
        cached = self._load_from_cache(boe_id)
        if cached:
            logger.info(f"✅ {boe_id} loaded from cache")
            return self._parse_cached_json(cached, boe_id)
        
        # 2. API XML consolidado
        try:
            xml_data = await self.fetch_xml_consolidado(boe_id)
            if xml_data:
                law_data = self._parse_xml_completo(xml_data, boe_id, "BOE_XML_CONSOLIDADO")
                self._save_to_cache(boe_id, law_data)
                logger.info(f"✅ {boe_id} fetched from API consolidada")
                return law_data
        except Exception as e:
            logger.warning(f"⚠️ XML consolidado failed for {boe_id}: {e}")
        
        # 3. XML diario BOE (para análisis) + HTML scraping (para texto)
        try:
            # Intentar obtener análisis del diario
            analisis = await self.fetch_analisis_from_diario(boe_id)
            # Scrapear HTML para el texto
            texto_html = await self.scrape_html_consolidado(boe_id)
            if texto_html:
                # Obtener metadatos básicos del diario
                metadatos = self._build_metadatos_from_analisis(boe_id, analisis)
                law_data = LawData(
                    boe_id=boe_id,
                    texto_xml=None,
                    texto_html=texto_html,
                    metadatos=metadatos,
                    analisis=analisis,
                    source="BOE_DIARIO_XML+HTML_SCRAPE"
                )
                self._save_to_cache(boe_id, law_data)
                logger.info(f"✅ {boe_id} fetched from diario+HTML")
                return law_data
        except Exception as e:
            logger.warning(f"⚠️ Diario+HTML fallback failed for {boe_id}: {e}")
        
        # 4. Solo HTML scraping (último recurso)
        try:
            texto_html = await self.scrape_html_consolidado(boe_id)
            if texto_html:
                law_data = LawData(
                    boe_id=boe_id,
                    texto_xml=None,
                    texto_html=texto_html,
                    metadatos=self._build_basic_metadatos(boe_id),
                    analisis=AnalisisData(),
                    source="BOE_HTML_SCRAPE_ONLY"
                )
                self._save_to_cache(boe_id, law_data)
                logger.info(f"✅ {boe_id} fetched from HTML only")
                return law_data
        except Exception as e:
            logger.error(f"❌ All fallbacks failed for {boe_id}: {e}")
        
        return None
    
    # ==========================================
    # FUENTE 1: CACHÉ LOCAL
    # ==========================================
    
    def _load_from_cache(self, boe_id: str) -> Optional[Dict]:
        """Carga ley del caché local JSON"""
        cache_file = self.CACHE_DIR / f"{boe_id}.json"
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
    
    def _save_to_cache(self, boe_id: str, law_data: LawData):
        """Guarda ley en caché local"""
        cache_file = self.CACHE_DIR / f"{boe_id}.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(law_data.to_dict(), f, ensure_ascii=False, indent=2)
    
    def _parse_cached_json(self, data: Dict, boe_id: str) -> LawData:
        """Parsea datos desde JSON cacheado"""
        metadict = data.get("metadatos", {})
        metadatos = Metadatos(
            boe_id=metadict.get("boe_id", boe_id),
            titulo=metadict.get("titulo", ""),
            departamento=metadict.get("departamento", ""),
            rango=metadict.get("rango", ""),
            numero_oficial=metadict.get("numero_oficial", ""),
            fecha_disposicion=metadict.get("fecha_disposicion", ""),
            fecha_publicacion=metadict.get("fecha_publicacion", ""),
            fecha_vigencia=metadict.get("fecha_vigencia", ""),
            estado_consolidacion=metadict.get("estado_consolidacion", ""),
            estatus_derogacion=metadict.get("estatus_derogacion", ""),
            ambito=metadict.get("ambito", ""),
            url_html=metadict.get("url_html", ""),
            url_eli=metadict.get("url_eli", "")
        )
        
        anadict = data.get("analisis", {})
        analisis = AnalisisData(
            materias=anadict.get("materias", []),
            notas=anadict.get("notas", ""),
            referencias_anteriores=[
                Referencia(**r) for r in anadict.get("referencias_anteriores", [])
            ],
            referencias_posteriores=[
                Referencia(**r) for r in anadict.get("referencias_posteriores", [])
            ]
        )
        
        return LawData(
            boe_id=boe_id,
            texto_xml=data.get("texto_xml"),
            texto_html=data.get("texto_html"),
            metadatos=metadatos,
            analisis=analisis,
            source=data.get("source", "CACHE")
        )
    
    # ==========================================
    # FUENTE 2: API XML CONSOLIDADO
    # ==========================================
    
    async def fetch_xml_consolidado(self, boe_id: str) -> Optional[str]:
        """
        Obtiene XML consolidado de la API de datos abiertos.
        Requiere header Accept: application/xml
        """
        url = f"{self.BASE_URL}/legislacion-consolidada/id/{boe_id}"
        
        async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.text
            elif response.status_code == 404:
                logger.warning(f"⚠️ XML consolidado 404 for {boe_id}")
                return None
            else:
                response.raise_for_status()
        return None
    
    # ==========================================
    # FUENTE 3: XML DIARIO BOE
    # ==========================================
    
    async def fetch_analisis_from_diario(self, boe_id: str) -> AnalisisData:
        """
        Obtiene análisis del XML del diario BOE original.
        Este XML suele estar disponible incluso cuando el consolidado no lo está.
        """
        url = f"{self.BOE_BASE}/diario_boe/xml.php?id={boe_id}"
        
        async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return self._parse_xml_analisis(response.text)
            else:
                logger.warning(f"⚠️ Diario XML failed for {boe_id}: {response.status_code}")
                return AnalisisData()
    
    async def fetch_metadatos_api(self, boe_id: str) -> Optional[Dict]:
        """
        Obtiene metadatos desde la API de metadatos del BOE.
        Endpoint alternativo que suele funcionar cuando el texto no está disponible.
        """
        url = f"{self.BOE_BASE}/buscar/api.php"
        params = {"accion": "ObtenerDocumento", "id": boe_id}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                return response.json()
        return None
    
    # ==========================================
    # FUENTE 4: HTML SCRAPING
    # ==========================================
    
    async def scrape_html_consolidado(self, boe_id: str) -> Optional[str]:
        """
        Scrapea texto consolidado del HTML de boe.es/buscar/act.php
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            logger.error("❌ BeautifulSoup not installed")
            return None
        
        url = f"{self.BOE_BASE}/buscar/act.php?id={boe_id}&tn=1&p=20260303"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer título
            titulo = soup.find('h3', class_='documento-titulo')
            title_text = titulo.get_text(strip=True) if titulo else boe_id
            
            # Extraer texto
            texto_div = soup.find('div', id='textoxslt') or soup.find('div', class_='textoxslt')
            
            if not texto_div:
                return None
            
            content = [f"# {title_text}"]
            
            for elem in texto_div.find_all(['p', 'h4', 'h5', 'div']):
                text = elem.get_text(strip=True)
                if not text:
                    continue
                
                # Detectar artículos y disposiciones
                if elem.name in ['h4', 'h5'] or (
                    text.startswith('Artículo') or text.startswith('Disposición')
                ) and len(text) < 200:
                    content.append(f"\n## {text}")
                else:
                    content.append(text)
            
            return "\n\n".join(content)
    
    # ==========================================
    # PARSING XML COMPLETO
    # ==========================================
    
    def _parse_xml_completo(self, xml_text: str, boe_id: str, source: str) -> LawData:
        """Parsea XML completo (metadatos + análisis + texto)"""
        import xmltodict
        
        data = xmltodict.parse(xml_text)
        
        # Normalizar estructura
        data = self._normalize_dict(data)
        
        # Extraer componentes
        metadatos = self._extract_metadatos(data, boe_id)
        analisis = self._extract_analisis(data)
        
        # El texto XML completo se guarda tal cual
        return LawData(
            boe_id=boe_id,
            texto_xml=xml_text,
            texto_html=None,
            metadatos=metadatos,
            analisis=analisis,
            source=source
        )
    
    def _extract_metadatos(self, data: Dict, boe_id: str) -> Metadatos:
        """Extrae metadatos del XML parseado"""
        metadict = data.get("data", {}).get("metadatos", {})
        
        def get_text(field, default=""):
            val = metadict.get(field, {})
            if isinstance(val, dict):
                return val.get("_text", default)
            return str(val) if val else default
        
        return Metadatos(
            boe_id=boe_id,
            titulo=get_text("titulo"),
            departamento=get_text("departamento"),
            rango=get_text("rango"),
            numero_oficial=get_text("numero_oficial"),
            fecha_disposicion=get_text("fecha_disposicion"),
            fecha_publicacion=get_text("fecha_publicacion"),
            fecha_vigencia=get_text("fecha_vigencia"),
            estado_consolidacion=get_text("estado_consolidacion"),
            estatus_derogacion=get_text("estatus_derogacion"),
            ambito=get_text("ambito"),
            url_html=get_text("url_html_consolidada"),
            url_eli=get_text("url_eli")
        )
    
    def _extract_analisis(self, data: Dict) -> AnalisisData:
        """Extrae TODO el análisis del XML (excepto metadata-eli)"""
        analisis_dict = data.get("data", {}).get("analisis", {})
        
        # Materias
        materias = []
        materias_data = analisis_dict.get("materias", {}).get("materia", [])
        if not isinstance(materias_data, list):
            materias_data = [materias_data]
        for m in materias_data:
            if isinstance(m, dict):
                materias.append(m.get("_text", ""))
        
        # Notas
        notas = ""
        notas_data = analisis_dict.get("notas", {}).get("nota", {})
        if isinstance(notas_data, dict):
            notas = notas_data.get("_text", "")
        elif isinstance(notas_data, str):
            notas = notas_data
        
        # Referencias
        ref_dict = analisis_dict.get("referencias", {})
        ref_anteriores = self._extract_referencias(ref_dict.get("anteriores", {}), "anterior")
        ref_posteriores = self._extract_referencias(ref_dict.get("posteriores", {}), "posterior")
        
        return AnalisisData(
            materias=materias,
            notas=notas,
            referencias_anteriores=ref_anteriores,
            referencias_posteriores=ref_posteriores
        )
    
    def _extract_referencias(self, ref_container: Dict, key: str) -> List[Referencia]:
        """Extrae lista de referencias normativas"""
        referencias = []
        
        items = ref_container.get(key, [])
        if not isinstance(items, list):
            items = [items]
        
        for item in items:
            if not isinstance(item, dict):
                continue
            
            id_norma = ""
            id_data = item.get("id_norma", {})
            if isinstance(id_data, dict):
                id_norma = id_data.get("_text", "")
            
            relacion = ""
            codigo = ""
            rel_data = item.get("relacion", {})
            if isinstance(rel_data, dict):
                relacion = rel_data.get("_text", "")
                codigo = rel_data.get("codigo", "")
            
            texto = ""
            txt_data = item.get("texto", {})
            if isinstance(txt_data, dict):
                texto = txt_data.get("_text", "")
            elif isinstance(txt_data, str):
                texto = txt_data
            
            if id_norma and relacion:
                referencias.append(Referencia(
                    id_norma=id_norma,
                    relacion=relacion,
                    codigo=str(codigo),
                    texto=texto
                ))
        
        return referencias
    
    def _parse_xml_analisis(self, xml_text: str) -> AnalisisData:
        """Parsea solo el análisis del XML del diario BOE"""
        try:
            import xmltodict
            data = xmltodict.parse(xml_text)
            data = self._normalize_dict(data)
            return self._extract_analisis({"data": data})
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse diario XML: {e}")
            return AnalisisData()
    
    # ==========================================
    # MÉTODOS UTILIDAD
    # ==========================================
    
    def _build_metadatos_from_analisis(self, boe_id: str, analisis: AnalisisData) -> Metadatos:
        """Construye metadatos básicos cuando solo tenemos análisis"""
        return Metadatos(
            boe_id=boe_id,
            titulo="",
            departamento="",
            rango="",
            numero_oficial="",
            fecha_disposicion="",
            fecha_publicacion="",
            fecha_vigencia="",
            estado_consolidacion="",
            estatus_derogacion="",
            url_html=f"https://www.boe.es/buscar/act.php?id={boe_id}",
            url_eli=""
        )
    
    def _build_basic_metadatos(self, boe_id: str) -> Metadatos:
        """Metadatos mínimos para fallback HTML only"""
        return Metadatos(
            boe_id=boe_id,
            titulo="",
            departamento="",
            rango="",
            numero_oficial="",
            fecha_disposicion="",
            fecha_publicacion="",
            fecha_vigencia="",
            estado_consolidacion="",
            estatus_derogacion="",
            url_html=f"https://www.boe.es/buscar/act.php?id={boe_id}",
            url_eli=""
        )
    
    async def download_and_cache(self, boe_id: str) -> Path:
        """
        Descarga ley completa y la guarda en caché.
        Returns: Path al archivo cacheado
        """
        law_data = await self.fetch_law_complete(boe_id)
        if law_data:
            return self.CACHE_DIR / f"{boe_id}.json"
        raise ValueError(f"Could not fetch law {boe_id}")
    
    async def verify_vigencia(self, boe_id: str) -> bool:
        """
        Verifica si una ley está vigente.
        """
        law_data = await self.fetch_law_complete(boe_id)
        if not law_data:
            return False
        
        # Verificar estatus de derogación
        if law_data.metadatos.estatus_derogacion == "S":
            return False
        
        # Verificar vigencia agotada
        if law_data.metadatos.estado_consolidacion == "Agotada":
            return False
        
        return True
    
    async def fetch_article(self, boe_id: str, article_num: str) -> Optional[str]:
        """
        Extrae texto de un artículo específico del texto XML.
        TODO: Implementar parsing de artículos individuales
        """
        law_data = await self.fetch_law_complete(boe_id)
        if not law_data or not law_data.texto_xml:
            return None
        
        # Parsear XML y buscar el artículo
        # Esto requiere implementación específica del parser de texto BOE
        logger.warning("fetch_article: implementación pendiente del parser de texto")
        return None
    
    def get_relaciones_for_neo4j(self, law_data: LawData) -> List[Tuple[str, str, str, str]]:
        """
        Convierte referencias a tuplas para crear relaciones en Neo4j.
        Returns: [(from_id, to_id, relacion_tipo, detalle)]
        """
        relaciones = []
        boe_id = law_data.boe_id
        
        # Referencias anteriores: esta ley afectó a leyes anteriores
        for ref in law_data.analisis.referencias_anteriores:
            tipo = self.RELACION_MAP.get(ref.codigo, ref.relacion.upper().replace(" ", "_"))
            relaciones.append((boe_id, ref.id_norma, tipo, ref.texto))
        
        # Referencias posteriores: leyes posteriores afectaron a esta
        for ref in law_data.analisis.referencias_posteriores:
            tipo = self.RELACION_MAP.get(ref.codigo, ref.relacion.upper().replace(" ", "_"))
            # Invertir dirección para recíprocas
            if ref.codigo in ["210", "270"]:  # DEROGA, MODIFICA
                tipo_reciproca = f"ES_{tipo}_POR"
                relaciones.append((ref.id_norma, boe_id, tipo, ref.texto))
            else:
                relaciones.append((ref.id_norma, boe_id, tipo, ref.texto))
        
        return relaciones


# Singleton para uso global
_boe_service = None


def get_boe_service() -> BOEService:
    """Obtiene instancia singleton del BOEService"""
    global _boe_service
    if _boe_service is None:
        _boe_service = BOEService()
    return _boe_service
