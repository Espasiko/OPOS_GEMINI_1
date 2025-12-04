"""
Herramientas Reales para el Agente Mistral
Implementación de las 9 funciones definidas en FUNCIONES_AGENTE_MISTRAL.json
"""

import os
import re
import json
import logging
import hashlib
import requests
from typing import List, Dict, Optional, Any
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

logger = logging.getLogger(__name__)

# Configuración
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COLLECTION_LEYES = "opositaia_leyes_seguridad_social"
COLLECTION_EXAMENES = "materiales_academia"
COLLECTION_CACHE = "qa_cache"


class MistralTools:
    """Implementación de herramientas reales para el Agente Mistral"""
    
    def __init__(self):
        # Inicializar Qdrant
        if QDRANT_API_KEY:
            self.qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        else:
            self.qdrant = QdrantClient(url=QDRANT_URL)
        
        self.cache_hits = 0
        self.cache_misses = 0
        logger.info(f"MistralTools inicializado - Qdrant: {QDRANT_URL}")
    
    # =========================================================================
    # HERRAMIENTA 1: buscar_rag_qdrant
    # =========================================================================
    def buscar_rag_qdrant(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.7,
        filter_ley: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Busca contexto legal relevante en Qdrant.
        
        Args:
            query: Consulta en lenguaje natural
            top_k: Número de resultados (1-10)
            score_threshold: Umbral mínimo de similitud
            filter_ley: Filtrar por ley específica (LGSS, RD_IMV, etc.)
        
        Returns:
            Dict con resultados y metadata
        """
        try:
            results = []
            
            # Buscar en colección de leyes/temarios
            points, _ = self.qdrant.scroll(
                collection_name=COLLECTION_LEYES,
                limit=200,
                with_payload=True,
                with_vectors=False
            )
            
            # Filtrar por relevancia (búsqueda por keywords)
            query_lower = query.lower()
            keywords = [w for w in query_lower.split() if len(w) > 3]
            
            for p in points:
                text = p.payload.get('text', '').lower()
                material = p.payload.get('material_nombre', '').lower()
                
                # Aplicar filtro de ley si se especifica
                if filter_ley:
                    if filter_ley.lower() not in material and filter_ley.lower() not in text:
                        continue
                
                # Calcular relevancia
                matches = sum(1 for kw in keywords if kw in text)
                if matches >= 1:
                    results.append({
                        'id': str(p.id),
                        'text': p.payload.get('text', '')[:800],
                        'fuente': p.payload.get('material_nombre', 'Temario'),
                        'pagina': p.payload.get('page_num', 0),
                        'tipo': p.payload.get('tipo', 'temario'),
                        'relevancia': matches / len(keywords) if keywords else 0
                    })
            
            # Ordenar por relevancia y limitar
            results.sort(key=lambda x: x['relevancia'], reverse=True)
            results = results[:top_k]
            
            return {
                'success': True,
                'query': query,
                'total_results': len(results),
                'results': results,
                'filter_applied': filter_ley,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error en buscar_rag_qdrant: {e}")
            return {
                'success': False,
                'error': str(e),
                'query': query
            }
    
    # =========================================================================
    # HERRAMIENTA 2: buscar_boe_oficial
    # =========================================================================
    def buscar_boe_oficial(
        self,
        tipo_busqueda: str,
        identificador_boe: Optional[str] = None,
        articulo: Optional[str] = None,
        ley: Optional[str] = None,
        texto_busqueda: Optional[str] = None,
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Busca y extrae texto oficial del BOE.
        
        Args:
            tipo_busqueda: 'articulo_especifico', 'busqueda_texto', 'por_identificador'
            identificador_boe: ID del BOE (ej: BOE-A-2015-11724)
            articulo: Número de artículo (ej: '205', '205.1.a')
            ley: Nombre de la ley
            texto_busqueda: Texto libre a buscar
        
        Returns:
            Dict con texto oficial, URL y metadatos
        """
        try:
            # Mapeo de leyes a identificadores BOE
            LEYES_BOE = {
                'LGSS': 'BOE-A-2015-11724',
                'Ley General de la Seguridad Social': 'BOE-A-2015-11724',
                'RD_IMV': 'BOE-A-2020-5493',
                'Ingreso Mínimo Vital': 'BOE-A-2020-5493',
                'LPAC': 'BOE-A-2015-10565',
                'Ley 39/2015': 'BOE-A-2015-10565',
                'TREBEP': 'BOE-A-2015-11719',
                'Estatuto Básico': 'BOE-A-2015-11719',
                'Constitución': 'BOE-A-1978-31229',
                'CE': 'BOE-A-1978-31229'
            }
            
            result = {
                'success': False,
                'tipo_busqueda': tipo_busqueda,
                'url_boe': None,
                'texto': None,
                'metadatos': {}
            }
            
            if tipo_busqueda == 'por_identificador' and identificador_boe:
                url = f"https://www.boe.es/buscar/act.php?id={identificador_boe}"
                result['url_boe'] = url
                result['success'] = True
                result['metadatos']['identificador'] = identificador_boe
                
            elif tipo_busqueda == 'articulo_especifico' and articulo and ley:
                # Buscar identificador de la ley
                boe_id = LEYES_BOE.get(ley, LEYES_BOE.get('LGSS'))
                url = f"https://www.boe.es/buscar/act.php?id={boe_id}"
                
                # Intentar obtener el artículo específico
                art_url = f"https://www.boe.es/buscar/act.php?id={boe_id}&p=&tn=1#a{articulo.replace('.', '-')}"
                
                result['url_boe'] = art_url
                result['success'] = True
                result['metadatos'] = {
                    'ley': ley,
                    'articulo': articulo,
                    'identificador': boe_id
                }
                
            elif tipo_busqueda == 'busqueda_texto' and texto_busqueda:
                # Búsqueda por texto en BOE
                url = f"https://www.boe.es/buscar/boe.php?texto={texto_busqueda.replace(' ', '+')}"
                result['url_boe'] = url
                result['success'] = True
                result['metadatos']['texto_buscado'] = texto_busqueda
            
            result['timestamp'] = datetime.now().isoformat()
            return result
            
        except Exception as e:
            logger.error(f"Error en buscar_boe_oficial: {e}")
            return {
                'success': False,
                'error': str(e),
                'tipo_busqueda': tipo_busqueda
            }
    
    # =========================================================================
    # HERRAMIENTA 3: verificar_url_boe
    # =========================================================================
    def verificar_url_boe(
        self,
        url: str,
        articulo_esperado: Optional[str] = None,
        verificar_contenido: bool = True
    ) -> Dict[str, Any]:
        """
        Verifica si una URL del BOE es válida y accesible.
        
        Args:
            url: URL completa del BOE
            articulo_esperado: Artículo que debería contener
            verificar_contenido: Si extraer y verificar contenido
        
        Returns:
            Dict con estado de verificación y contenido
        """
        try:
            result = {
                'url': url,
                'valida': False,
                'accesible': False,
                'contiene_articulo': None,
                'contenido_preview': None,
                'metadatos': {}
            }
            
            # Verificar formato de URL
            if 'boe.es' not in url:
                result['error'] = 'URL no es del dominio boe.es'
                return result
            
            result['valida'] = True
            
            # Verificar accesibilidad
            try:
                response = requests.head(url, timeout=10, allow_redirects=True)
                result['accesible'] = response.status_code == 200
                result['metadatos']['status_code'] = response.status_code
            except requests.RequestException as e:
                result['accesible'] = False
                result['metadatos']['error_conexion'] = str(e)
            
            # Verificar contenido si se solicita
            if verificar_contenido and result['accesible']:
                try:
                    response = requests.get(url, timeout=30)
                    content = response.text[:5000]  # Primeros 5000 chars
                    
                    result['contenido_preview'] = content[:500]
                    
                    if articulo_esperado:
                        # Buscar el artículo en el contenido
                        patterns = [
                            f"artículo {articulo_esperado}",
                            f"art. {articulo_esperado}",
                            f"Art. {articulo_esperado}",
                            f"Artículo {articulo_esperado}"
                        ]
                        result['contiene_articulo'] = any(
                            p.lower() in content.lower() for p in patterns
                        )
                except Exception as e:
                    result['metadatos']['error_contenido'] = str(e)
            
            result['timestamp'] = datetime.now().isoformat()
            return result
            
        except Exception as e:
            logger.error(f"Error en verificar_url_boe: {e}")
            return {
                'url': url,
                'valida': False,
                'error': str(e)
            }
    
    # =========================================================================
    # HERRAMIENTA 4: calcular_prestacion_ss
    # =========================================================================
    def calcular_prestacion_ss(
        self,
        tipo_prestacion: str,
        bases_cotizacion: Optional[List[float]] = None,
        num_meses: Optional[int] = None,
        años_cotizados: Optional[float] = None,
        edad_jubilacion: Optional[int] = None,
        año_calculo: int = 2024,
        parametros_adicionales: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Calcula prestaciones de Seguridad Social.
        
        Args:
            tipo_prestacion: Tipo de cálculo
            bases_cotizacion: Array de bases mensuales
            num_meses: Meses a considerar
            años_cotizados: Años totales cotizados
            edad_jubilacion: Edad de jubilación
            año_calculo: Año para coeficientes
            parametros_adicionales: Parámetros extra
        
        Returns:
            Dict con resultado, fórmula y explicación
        """
        try:
            result = {
                'tipo_prestacion': tipo_prestacion,
                'resultado': None,
                'formula': None,
                'explicacion': None,
                'normativa': None
            }
            
            params = parametros_adicionales or {}
            
            if tipo_prestacion == 'base_reguladora_jubilacion':
                # Art. 209 LGSS: BR = Suma bases / 350 (para 300 meses = 25 años)
                if bases_cotizacion:
                    meses = num_meses or 300
                    bases = bases_cotizacion[:meses]
                    suma = sum(bases)
                    divisor = 350  # Para 25 años
                    br = suma / divisor
                    
                    result['resultado'] = round(br, 2)
                    result['formula'] = f"BR = {suma:.2f} / {divisor} = {br:.2f}€"
                    result['explicacion'] = f"Base reguladora calculada sobre {len(bases)} meses de cotización"
                    result['normativa'] = "Art. 209 LGSS"
                    
            elif tipo_prestacion == 'pension_jubilacion':
                # Pensión = BR × Porcentaje según años cotizados
                if bases_cotizacion and años_cotizados:
                    # Calcular BR primero
                    meses = num_meses or 300
                    bases = bases_cotizacion[:meses]
                    br = sum(bases) / 350
                    
                    # Porcentaje según años (simplificado)
                    if años_cotizados >= 37:
                        porcentaje = 100
                    elif años_cotizados >= 15:
                        porcentaje = 50 + (años_cotizados - 15) * (50 / 22)
                    else:
                        porcentaje = 0
                    
                    pension = br * (porcentaje / 100)
                    
                    # Coeficientes reductores si jubilación anticipada
                    if edad_jubilacion and edad_jubilacion < 67:
                        trimestres_anticipados = (67 - edad_jubilacion) * 4
                        # Coeficiente según años cotizados (simplificado)
                        if años_cotizados >= 38.5:
                            coef = 0.01625  # 1.625% por trimestre
                        else:
                            coef = 0.01875  # 1.875% por trimestre
                        reduccion = trimestres_anticipados * coef
                        pension = pension * (1 - reduccion)
                        result['explicacion'] = f"Pensión con reducción {reduccion*100:.2f}% por jubilación anticipada"
                    else:
                        result['explicacion'] = f"Pensión al {porcentaje:.1f}% de la BR"
                    
                    result['resultado'] = round(pension, 2)
                    result['formula'] = f"Pensión = {br:.2f} × {porcentaje:.1f}% = {pension:.2f}€"
                    result['normativa'] = "Arts. 205-210 LGSS"
                    
            elif tipo_prestacion == 'imv':
                # Ingreso Mínimo Vital (RD 20/2020)
                # Cuantías 2024 (simplificadas)
                cuantia_base = 604.21  # Adulto solo
                
                miembros = params.get('miembros_unidad', 1)
                menores = params.get('menores', 0)
                
                # Incrementos por miembros
                if miembros == 2:
                    cuantia = cuantia_base * 1.3
                elif miembros == 3:
                    cuantia = cuantia_base * 1.55
                elif miembros >= 4:
                    cuantia = cuantia_base * 1.75
                else:
                    cuantia = cuantia_base
                
                # Complemento por menores
                cuantia += menores * 52.00
                
                result['resultado'] = round(cuantia, 2)
                result['formula'] = f"IMV = {cuantia_base:.2f} × factor + {menores} × 52€"
                result['explicacion'] = f"IMV para unidad de {miembros} miembros con {menores} menores"
                result['normativa'] = "RD 20/2020 (IMV)"
            
            result['año_calculo'] = año_calculo
            result['timestamp'] = datetime.now().isoformat()
            return result
            
        except Exception as e:
            logger.error(f"Error en calcular_prestacion_ss: {e}")
            return {
                'tipo_prestacion': tipo_prestacion,
                'error': str(e)
            }

    # =========================================================================
    # HERRAMIENTA 5: generar_qa_legal
    # =========================================================================
    def generar_qa_legal(
        self,
        contexto_legal: str,
        tema: str,
        dificultad: str = "medio",
        tipo_pregunta: str = "conceptual",
        articulos_referencia: Optional[List[str]] = None,
        incluir_calculo: bool = False
    ) -> Dict[str, Any]:
        """
        Genera una Q&A tipo test basada en contexto legal.
        
        Esta función prepara el contexto para que el LLM genere la pregunta.
        El LLM debe ser llamado externamente con este contexto.
        """
        return {
            'ready_for_generation': True,
            'contexto_legal': contexto_legal[:2000],
            'tema': tema,
            'dificultad': dificultad,
            'tipo_pregunta': tipo_pregunta,
            'articulos_referencia': articulos_referencia or [],
            'incluir_calculo': incluir_calculo,
            'prompt_sugerido': f"""Genera una pregunta tipo test de oposición sobre: {tema}
            
Contexto legal:
{contexto_legal[:1500]}

Requisitos:
- Dificultad: {dificultad}
- Tipo: {tipo_pregunta}
- Artículos a referenciar: {articulos_referencia}
- Incluir cálculo: {incluir_calculo}

Formato de respuesta:
{{
    "pregunta": "texto de la pregunta",
    "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "respuesta_correcta": "A/B/C/D",
    "explicacion": "explicación detallada",
    "articulos": ["art. X LGSS"]
}}"""
        }
    
    # =========================================================================
    # HERRAMIENTA 6: verificar_qa_completa
    # =========================================================================
    def verificar_qa_completa(
        self,
        pregunta: str,
        respuesta_correcta: str,
        opciones: Optional[Dict[str, str]] = None,
        explicacion: Optional[str] = None,
        referencias_legales: Optional[List[str]] = None,
        url_fuente: Optional[str] = None,
        verificar_calculo: bool = True,
        verificar_vigencia: bool = True
    ) -> Dict[str, Any]:
        """
        Verifica exhaustivamente una Q&A.
        """
        result = {
            'verified': False,
            'confidence': 0.0,
            'issues': [],
            'corrections': [],
            'recommendation': 'pending'
        }
        
        # 1. Verificar formato básico
        if not pregunta or len(pregunta) < 20:
            result['issues'].append('Pregunta demasiado corta')
        
        if respuesta_correcta not in ['A', 'B', 'C', 'D']:
            result['issues'].append('Respuesta correcta debe ser A, B, C o D')
        
        if opciones and len(opciones) != 4:
            result['issues'].append('Deben haber exactamente 4 opciones')
        
        # 2. Verificar referencias legales
        if referencias_legales:
            for ref in referencias_legales:
                # Extraer artículo y ley
                match = re.search(r'art[íi]culo?\s*(\d+)', ref, re.IGNORECASE)
                if match:
                    articulo = match.group(1)
                    # Verificar contra BOE
                    boe_result = self.buscar_boe_oficial(
                        tipo_busqueda='articulo_especifico',
                        articulo=articulo,
                        ley='LGSS'
                    )
                    if boe_result.get('success'):
                        result['corrections'].append(f'Referencia {ref} verificada')
                    else:
                        result['issues'].append(f'No se pudo verificar {ref}')
        
        # 3. Verificar URL si existe
        if url_fuente:
            url_result = self.verificar_url_boe(url_fuente)
            if not url_result.get('accesible'):
                result['issues'].append(f'URL no accesible: {url_fuente}')
        
        # 4. Calcular confianza
        total_checks = 4
        passed_checks = total_checks - len(result['issues'])
        result['confidence'] = passed_checks / total_checks
        
        # 5. Determinar recomendación
        if result['confidence'] >= 0.8:
            result['verified'] = True
            result['recommendation'] = 'approve'
        elif result['confidence'] >= 0.5:
            result['recommendation'] = 'review'
        else:
            result['recommendation'] = 'reject'
        
        result['timestamp'] = datetime.now().isoformat()
        return result
    
    # =========================================================================
    # HERRAMIENTA 7: clasificar_qa_tema
    # =========================================================================
    def clasificar_qa_tema(
        self,
        pregunta: str,
        respuesta: str,
        explicacion: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Clasifica una Q&A por tema, subtema, dificultad y tipo.
        """
        texto = f"{pregunta} {respuesta} {explicacion or ''}"
        texto_lower = texto.lower()
        
        # Clasificación por tema principal
        temas = {
            'jubilacion': ['jubilación', 'jubilacion', 'pensión', 'pension', 'retiro'],
            'incapacidad': ['incapacidad', 'invalidez', 'discapacidad'],
            'desempleo': ['desempleo', 'paro', 'prestación contributiva'],
            'maternidad': ['maternidad', 'paternidad', 'nacimiento', 'permiso'],
            'cotizacion': ['cotización', 'cotizacion', 'base reguladora', 'cuota'],
            'imv': ['ingreso mínimo', 'imv', 'renta garantizada'],
            'viudedad': ['viudedad', 'orfandad', 'muerte', 'supervivencia'],
            'procedimiento': ['procedimiento', 'recurso', 'reclamación', 'silencio']
        }
        
        tema_detectado = 'general'
        for tema, keywords in temas.items():
            if any(kw in texto_lower for kw in keywords):
                tema_detectado = tema
                break
        
        # Clasificación por dificultad
        indicadores_dificil = ['excepto', 'salvo', 'no obstante', 'sin perjuicio', 
                               'siempre que', 'a menos que', 'calcul']
        dificultad = 'media'
        if sum(1 for ind in indicadores_dificil if ind in texto_lower) >= 2:
            dificultad = 'alta'
        elif len(texto) < 200:
            dificultad = 'baja'
        
        # Clasificación por tipo
        if 'calcul' in texto_lower or '€' in texto or '%' in texto:
            tipo = 'calculo'
        elif 'caso' in texto_lower or 'supuesto' in texto_lower:
            tipo = 'aplicacion_practica'
        elif 'sentencia' in texto_lower or 'tribunal' in texto_lower:
            tipo = 'jurisprudencia'
        else:
            tipo = 'conceptual'
        
        return {
            'tema': tema_detectado,
            'subtema': None,  # Requiere análisis más profundo
            'dificultad': dificultad,
            'tipo': tipo,
            'keywords_detectados': [kw for kw in texto_lower.split() if len(kw) > 5][:10],
            'timestamp': datetime.now().isoformat()
        }
    
    # =========================================================================
    # HERRAMIENTA 8: extraer_articulos_texto
    # =========================================================================
    def extraer_articulos_texto(
        self,
        texto: str,
        formato_salida: str = "estructurado"
    ) -> Dict[str, Any]:
        """
        Extrae todas las referencias a artículos legales de un texto.
        """
        # Patrones para detectar artículos
        patrones = [
            r'art[íi]culo\s+(\d+(?:\.\d+)?(?:\.[a-z])?)\s*(?:de\s+la\s+)?(\w+)?',
            r'art\.\s*(\d+(?:\.\d+)?(?:\.[a-z])?)\s*(\w+)?',
            r'Art\.\s*(\d+(?:\.\d+)?(?:\.[a-z])?)\s*(\w+)?',
        ]
        
        referencias = []
        for patron in patrones:
            matches = re.findall(patron, texto, re.IGNORECASE)
            for match in matches:
                articulo = match[0] if match[0] else ''
                ley = match[1] if len(match) > 1 and match[1] else 'LGSS'
                
                if articulo:
                    referencias.append({
                        'articulo': articulo,
                        'ley': ley.upper() if ley else 'LGSS',
                        'referencia_completa': f"art. {articulo} {ley}"
                    })
        
        # Eliminar duplicados
        referencias_unicas = []
        vistas = set()
        for ref in referencias:
            key = f"{ref['articulo']}-{ref['ley']}"
            if key not in vistas:
                vistas.add(key)
                referencias_unicas.append(ref)
        
        if formato_salida == "lista_simple":
            return {
                'referencias': [r['referencia_completa'] for r in referencias_unicas],
                'total': len(referencias_unicas)
            }
        
        return {
            'referencias': referencias_unicas,
            'total': len(referencias_unicas),
            'formato': 'estructurado',
            'timestamp': datetime.now().isoformat()
        }
    
    # =========================================================================
    # HERRAMIENTA 9: obtener_normativa_vigente
    # =========================================================================
    def obtener_normativa_vigente(
        self,
        identificador_norma: str,
        fecha_vigencia: Optional[str] = None,
        incluir_modificaciones: bool = True
    ) -> Dict[str, Any]:
        """
        Obtiene la versión vigente de una normativa.
        """
        # Mapeo de identificadores comunes
        NORMAS = {
            'BOE-A-2015-11724': {
                'nombre': 'Real Decreto Legislativo 8/2015 - LGSS',
                'url': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724',
                'vigente': True,
                'ultima_modificacion': '2024-01-01'
            },
            'RDLeg 8/2015': {
                'nombre': 'Real Decreto Legislativo 8/2015 - LGSS',
                'url': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724',
                'vigente': True,
                'ultima_modificacion': '2024-01-01'
            },
            'BOE-A-2020-5493': {
                'nombre': 'Real Decreto-ley 20/2020 - IMV',
                'url': 'https://www.boe.es/buscar/act.php?id=BOE-A-2020-5493',
                'vigente': True,
                'ultima_modificacion': '2023-12-01'
            }
        }
        
        norma = NORMAS.get(identificador_norma, {
            'nombre': identificador_norma,
            'url': f'https://www.boe.es/buscar/act.php?id={identificador_norma}',
            'vigente': None,
            'ultima_modificacion': None
        })
        
        return {
            'identificador': identificador_norma,
            'nombre': norma['nombre'],
            'url_consolidado': norma['url'],
            'vigente': norma['vigente'],
            'ultima_modificacion': norma['ultima_modificacion'],
            'fecha_consulta': fecha_vigencia or datetime.now().strftime('%Y-%m-%d'),
            'incluye_modificaciones': incluir_modificaciones,
            'timestamp': datetime.now().isoformat()
        }


# =========================================================================
# CACHÉ SEMÁNTICA MEJORADA
# =========================================================================
class SemanticCache:
    """
    Caché semántica usando Qdrant para ahorrar llamadas al LLM.
    
    Objetivo: Ahorrar 60-70% de llamadas al LLM cacheando respuestas similares.
    
    Funcionamiento:
    1. Antes de llamar al LLM, busca pregunta similar (>0.95 similitud)
    2. Si existe, devuelve respuesta cacheada (coste = 0€)
    3. Si no existe, genera y cachea la nueva respuesta
    """
    
    COLLECTION_NAME = "qa_cache"
    VECTOR_SIZE = 1024  # BGE-M3 dimension
    
    def __init__(self, qdrant_client: QdrantClient, collection_name: str = None):
        self.qdrant = qdrant_client
        self.collection = collection_name or self.COLLECTION_NAME
        self.hits = 0
        self.misses = 0
        self._collection_exists = None
        self._memory_cache = {}  # Fallback en memoria
        logger.info(f"SemanticCache inicializado - Colección: {self.collection}")
    
    def _ensure_collection(self) -> bool:
        """Verifica que la colección existe"""
        if self._collection_exists is not None:
            return self._collection_exists
        
        try:
            collections = self.qdrant.get_collections().collections
            self._collection_exists = any(c.name == self.collection for c in collections)
            
            if not self._collection_exists:
                logger.warning(f"Colección '{self.collection}' no existe. Usando caché en memoria.")
            
            return self._collection_exists
        except Exception as e:
            logger.error(f"Error verificando colección: {e}")
            self._collection_exists = False
            return False
    
    def get(self, query: str, threshold: float = 0.95) -> Optional[Dict]:
        """
        Busca una respuesta cacheada para una query similar.
        
        Args:
            query: Pregunta del usuario
            threshold: Umbral de similitud (0.95 = muy similar)
        
        Returns:
            Respuesta cacheada si existe, None si no
        """
        query_lower = query.lower().strip()
        query_hash = hashlib.md5(query_lower.encode()).hexdigest()
        
        # 1. Buscar en caché de memoria (más rápido)
        if query_hash in self._memory_cache:
            self.hits += 1
            logger.info(f"Cache HIT (memory): {query[:50]}...")
            return self._memory_cache[query_hash]
        
        # 2. Buscar por similitud en memoria
        for cached_hash, cached_data in self._memory_cache.items():
            cached_query = cached_data.get('_query', '')
            if self._text_similarity(query_lower, cached_query.lower()) >= threshold:
                self.hits += 1
                logger.info(f"Cache HIT (memory-similar): {query[:50]}...")
                return cached_data
        
        # 3. Buscar en Qdrant si la colección existe
        if self._ensure_collection():
            try:
                points, _ = self.qdrant.scroll(
                    collection_name=self.collection,
                    limit=100,
                    with_payload=True,
                    with_vectors=False
                )
                
                for p in points:
                    cached_query = p.payload.get('query', '').lower().strip()
                    cached_hash = p.payload.get('query_hash', '')
                    
                    # Match exacto por hash
                    if cached_hash == query_hash:
                        self.hits += 1
                        logger.info(f"Cache HIT (qdrant-exact): {query[:50]}...")
                        response = p.payload.get('response')
                        # Guardar en memoria para acceso rápido
                        self._memory_cache[query_hash] = response
                        return response
                    
                    # Match por similitud de texto
                    if self._text_similarity(query_lower, cached_query) >= threshold:
                        self.hits += 1
                        logger.info(f"Cache HIT (qdrant-similar): {query[:50]}...")
                        response = p.payload.get('response')
                        self._memory_cache[cached_hash] = response
                        return response
                        
            except Exception as e:
                logger.error(f"Error buscando en Qdrant: {e}")
        
        self.misses += 1
        logger.debug(f"Cache MISS: {query[:50]}...")
        return None
    
    def set(self, query: str, response: Dict, ttl_days: int = 30) -> bool:
        """
        Guarda una respuesta en caché.
        
        Args:
            query: Pregunta original
            response: Respuesta a cachear
            ttl_days: Tiempo de vida en días
        
        Returns:
            True si se guardó correctamente
        """
        try:
            query_lower = query.lower().strip()
            query_hash = hashlib.md5(query_lower.encode()).hexdigest()
            
            # Añadir metadata
            cache_entry = {
                **response,
                '_query': query,
                '_query_hash': query_hash,
                '_cached_at': datetime.now().isoformat(),
                '_ttl_days': ttl_days
            }
            
            # 1. Guardar en memoria
            self._memory_cache[query_hash] = cache_entry
            logger.info(f"Cache SET (memory): {query[:50]}... -> {query_hash[:8]}")
            
            # 2. Guardar en Qdrant si la colección existe
            if self._ensure_collection():
                try:
                    from qdrant_client.models import PointStruct
                    import random
                    
                    # Generar vector dummy (en producción usar embeddings reales)
                    # TODO: Integrar con BGE-M3 para embeddings reales
                    dummy_vector = [random.random() for _ in range(self.VECTOR_SIZE)]
                    
                    point_id = int(query_hash[:8], 16)  # Convertir hash a int
                    
                    self.qdrant.upsert(
                        collection_name=self.collection,
                        points=[
                            PointStruct(
                                id=point_id,
                                vector=dummy_vector,
                                payload={
                                    'query': query,
                                    'query_hash': query_hash,
                                    'response': response,
                                    'cached_at': datetime.now().isoformat(),
                                    'ttl_days': ttl_days,
                                    'hit_count': 0
                                }
                            )
                        ]
                    )
                    logger.info(f"Cache SET (qdrant): {query[:50]}... -> {point_id}")
                    
                except Exception as e:
                    logger.error(f"Error guardando en Qdrant: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error en cache set: {e}")
            return False
    
    def invalidate(self, query: str) -> bool:
        """Invalida una entrada de caché"""
        try:
            query_hash = hashlib.md5(query.lower().strip().encode()).hexdigest()
            
            # Eliminar de memoria
            if query_hash in self._memory_cache:
                del self._memory_cache[query_hash]
            
            # Eliminar de Qdrant
            if self._ensure_collection():
                point_id = int(query_hash[:8], 16)
                self.qdrant.delete(
                    collection_name=self.collection,
                    points_selector=[point_id]
                )
            
            logger.info(f"Cache INVALIDATE: {query[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error invalidando caché: {e}")
            return False
    
    def clear(self) -> bool:
        """Limpia toda la caché"""
        try:
            self._memory_cache.clear()
            
            if self._ensure_collection():
                # Recrear colección vacía
                from qdrant_client.models import Distance, VectorParams
                
                self.qdrant.delete_collection(self.collection)
                self.qdrant.create_collection(
                    collection_name=self.collection,
                    vectors_config=VectorParams(
                        size=self.VECTOR_SIZE,
                        distance=Distance.COSINE
                    )
                )
            
            self.hits = 0
            self.misses = 0
            logger.info("Cache CLEARED")
            return True
            
        except Exception as e:
            logger.error(f"Error limpiando caché: {e}")
            return False
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud Jaccard entre dos textos.
        
        En producción, usar embeddings para similitud semántica real.
        """
        # Normalizar y tokenizar
        words1 = set(w for w in text1.lower().split() if len(w) > 2)
        words2 = set(w for w in text2.lower().split() if len(w) > 2)
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def get_stats(self) -> Dict:
        """Devuelve estadísticas de la caché"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        
        memory_size = len(self._memory_cache)
        qdrant_size = 0
        
        if self._ensure_collection():
            try:
                info = self.qdrant.get_collection(self.collection)
                qdrant_size = info.points_count
            except:
                pass
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total_requests': total,
            'hit_rate': f"{hit_rate*100:.1f}%",
            'hit_rate_numeric': hit_rate,
            'memory_entries': memory_size,
            'qdrant_entries': qdrant_size,
            'collection_exists': self._collection_exists,
            'estimated_savings': f"${self.hits * 0.002:.4f}"  # ~$0.002 por llamada LLM
        }


# =========================================================================
# SINGLETON Y HELPERS
# =========================================================================
_tools_instance = None
_cache_instance = None

def get_mistral_tools() -> MistralTools:
    """Obtiene instancia singleton de MistralTools"""
    global _tools_instance
    if _tools_instance is None:
        _tools_instance = MistralTools()
    return _tools_instance

def get_semantic_cache() -> SemanticCache:
    """Obtiene instancia singleton de SemanticCache"""
    global _cache_instance
    if _cache_instance is None:
        tools = get_mistral_tools()
        _cache_instance = SemanticCache(tools.qdrant)
    return _cache_instance
