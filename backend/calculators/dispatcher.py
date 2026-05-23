"""
Dispatcher Consolidados - Motor de Cálculo OpositAIA
Unifica Seguridad Social (SS) y Procedimiento Administrativo (AGE)

Incluye tablas históricas de IPC, IPREM y SMI para resolver casos
prácticos de años anteriores con las cuantías legalmente correctas.
"""
import re
from decimal import Decimal
from typing import Dict, Any, Optional, List

# ============================================================================
# TABLAS HISTÓRICAS — Fuente: BOE y Decretos anuales de SS
# ============================================================================

# Factor de revalorización IPC acumulado (tasa interanual de diciembre, %)
# Fuente: INE + BOE (Ley de Presupuestos General del Estado / RD cuantías SS)
HISTORICO_IPC: Dict[int, float] = {
    2000: 4.0,   # BOE RD pcuantías 2001
    2001: 2.7,
    2002: 4.0,
    2003: 2.6,
    2004: 3.2,
    2005: 3.7,
    2006: 2.7,
    2007: 4.2,
    2008: 1.4,
    2009: 0.8,
    2010: 3.0,
    2011: 2.4,
    2012: 2.9,
    2013: 0.3,
    2014: -1.0,  # Deflación
    2015: 0.0,
    2016: 1.6,
    2017: 1.1,
    2018: 1.2,
    2019: 0.8,
    2020: -0.5,  # COVID
    2021: 6.5,
    2022: 5.5,   # RD-L 2/2022 revalorización pensiones
    2023: 8.5,   # Revalorización récord
    2024: 2.8,
    2025: 2.4,
    2026: 2.7,   # RD cuantías SS 2026 (BOE ene-2026)
}

# IPREM mensual por año (€/mes)
# Fuente: Ley de Presupuestos / RD de cuantías anuales
HISTORICO_IPREM: Dict[int, float] = {
    2004: 460.50,
    2005: 469.80,
    2006: 479.10,
    2007: 499.20,
    2008: 516.90,
    2009: 527.24,
    2010: 532.51,
    2011: 532.51,  # Congelado
    2012: 532.51,
    2013: 532.51,
    2014: 532.51,
    2015: 532.51,
    2016: 532.51,
    2017: 537.84,
    2018: 537.84,
    2019: 537.84,
    2020: 564.90,
    2021: 564.90,
    2022: 570.60,
    2023: 600.00,  # RD-L 2023
    2024: 607.05,
    2025: 608.33,
    2026: 610.00,  # RD cuantías SS 2026
}

# SMI mensual por año (€/mes) — 14 pagas
# Fuente: RD de SMI anual
HISTORICO_SMI: Dict[int, float] = {
    2000: 433.20,
    2004: 460.50,
    2008: 600.00,
    2010: 633.30,
    2012: 641.40,
    2014: 645.30,
    2016: 655.20,
    2017: 707.60,
    2018: 735.90,
    2019: 900.00,  # Subida histórica
    2020: 950.00,
    2021: 965.00,
    2022: 1000.00,
    2023: 1080.00,
    2024: 1134.00,
    2025: 1157.00,
    2026: 1221.00,  # RD 126/2026 (confirmado Orden PJC/297/2026: base_min = SMI×7/6 = 1.424,40€)
}

# Base mínima cotización RETA por año
HISTORICO_BASE_MINIMA_RETA: Dict[int, float] = {
    2015: 884.40,
    2016: 893.10,
    2017: 919.80,
    2018: 932.70,
    2019: 944.40,
    2020: 944.40,
    2021: 960.60,
    2022: 960.60,
    2023: 1000.80,  # Nuevo sistema ingresos reales RDL 13/2022
    2024: 1000.80,
    2025: 1035.00,
    2026: 1048.50,
}


def obtener_constantes_anio(anio: int) -> Dict[str, Any]:
    """
    Devuelve las constantes legales correctas para el año del caso práctico.
    Usa interpolación hacia el año más cercano si el año exacto no está en la tabla.
    """
    # Buscar el año más próximo en cada tabla
    def _buscar_mas_cercano(tabla: Dict[int, float], anio_buscado: int) -> float:
        if anio_buscado in tabla:
            return tabla[anio_buscado]
        # Encontrar año más cercano hacia abajo
        anos_disponibles = sorted([a for a in tabla.keys() if a <= anio_buscado])
        if anos_disponibles:
            return tabla[anos_disponibles[-1]]
        # Si el año es anterior a todos, devolver el mínimo
        return tabla[min(tabla.keys())]
    
    ipc = _buscar_mas_cercano(HISTORICO_IPC, anio)
    iprem = _buscar_mas_cercano(HISTORICO_IPREM, anio)
    smi = _buscar_mas_cercano(HISTORICO_SMI, anio)
    base_reta = _buscar_mas_cercano(HISTORICO_BASE_MINIMA_RETA, anio)
    
    return {
        "anio": anio,
        "factor_revalorizacion": ipc / 100.0,
        "iprem_mensual": Decimal(str(iprem)),
        "smi_mensual": Decimal(str(smi)),
        "base_minima_reta": Decimal(str(base_reta)),
        "fuente": f"Datos BOE/INE para el año {anio}"
    }

from .calculos_ss import calcular_subsidio_it
from .calculos_ss_extended import (
    CalculadoraIPT, CalculadoraJubilacion, CalculadoraJubilacionParcial,
    CalculadoraDesempleo, CalculadoraMaternidad, CalculadoraCuota, 
    CalculadoraAyudaHijo, CalculadoraViudedad, CalculadoraOrfandad,
    CalculadoraIPA, CalculadoraRiesgoEmbarazo, CalculadoraLPNI,
    CalculadoraIPP, CalculadoraSupervivencia, CalculadoraCUME,
    CalculadoraBeneficiosHijos,
    calcular_recargo_ss, calcular_intereses_demora_ss,
    calcular_it_situaciones_especiales_lo1_2023, calcular_base_cotizacion_completa,
    calcular_integracion_lagunas_jubilacion, calcular_br_jubilacion_dt34,
    calcular_fecha_efectos_cambio_base_reta, calcular_tipo_enajenacion,
    calcular_jubilacion_activa_escala_rdl11_2024, calcular_derivacion_responsabilidad_ss,
    calcular_cuota_contrato_corta_duracion, calcular_pension_maxima_anticipada_involuntaria,
    calcular_retribucion_especie_vehiculo
)
from .calculos_imv import CalculadoraIMV, TipoUnidadFamiliar
from .calculadora_age import ejecutar_calculo_age, TOOLS_AGE
from .calculadora_presupuesto import ejecutar_calculo_presupuesto, TOOLS_PRESUPUESTO

class CasosPracticosDispatcher:
    """
    Dispatcher de alto nivel para casos prácticos.
    Identifica el dominio (AGE/SS) y ejecuta el cálculo determinístico.
    """
    
    # Mapeo de Dominios y Tipos (NLP Robusto)
    DOMINIOS = {
        "SS": [
            "seguridad social", "ss", "pensión", "pension", "jubilación", "jubilacion", "it", "incapacidad", 
            "desempleo", "cotización", "cotizacion", "maternidad", "paternidad", "prestación", "prestacion",
            "subsidio", "baja", "alta", "cae", "ere", "ert", "base reguladora", "br", "imv", "ingreso mínimo", 
            "vital", "hijo", "familiar", "relevo", "manufacturera", "viudedad", "orfandad", "defunción", 
            "muerte", "sepelio", "muerto", "fallecido", "ipp", "parcial permanente"
        ],
        "AGE": [
            "procedimiento", "recurso", "alzada", "reposición", "reposicion", "silencio", "plazo", "prescripción", 
            "prescripcion", "sancionador", "vencimiento", "hábiles", "habiles", "computar", "vence", "caducidad",
            "notificación", "notificacion", "expediente", "administrativo", "ley 39", "ley 40", "lpac", "trebep",
            "vacaciones", "asuntos propios", "moscosos", "canosos", "extraordinario de revisión", "recusacion",
            "abstencion", "subsanacion", "subsanar",
            # Retribuciones / Nóminas
            "nómina", "nomina", "sueldo", "salario", "bruto", "neto", "irpf", "retención",
            "trienio", "complemento destino", "complemento específico", "paga extra", "dietas", "kilómetros",
            "subgrupo a1", "subgrupo a2", "subgrupo c1", "subgrupo c2",
            # Contratación pública LCSP
            "vec", "pbl", "valor estimado", "presupuesto base", "licitación", "licitacion",
            "contrato menor", "garantía definitiva", "garantia definitiva", "lcsp", "contratación",
            # Presupuesto y gestión financiera
            "crédito presupuestario", "credito presupuestario", "modificación presupuestaria",
            "anticipo caja fija", "acf", "pago a justificar", "pj", "reintegro subvención",
            "subvención", "subvencion", "asiento contable", "pgcp", "tribunal de cuentas",
        ]
    }

    TIPOS_CASO_SS = {
        "supervivencia": ["defunción", "muerte", "sepelio", "fallecimiento", "auxilio"],
        "viudedad": ["viudedad", "viudo", "viuda"],
        "orfandad": ["orfandad", "huérfano", "huerfano"],
        "subsidio_it": ["incapacidad temporal", "itp", "lumbago", "gripe", "enfermedad"], # Quitamos 'it' y 'accidente' genéricos
        "ipt": ["ipt", "incapacidad permanente total", "permanente", "invalidez", "pension invalidez", "vension"],
        "ipp": ["ipp", "parcial permanente", "incapacidad parcial"],
        "ipa": ["ipa", "absoluta", "gran invalidez", "gi"],
        "jubilacion_parcial": ["jubilación parcial", "jubilacion parcial", "parcial", "relevo", "parssial", "parcialmente"],
        "jubilacion": ["jubilación", "jubilacion", "retiro", "vejez", "jubila", "jubilasion", "jubilao"],
        "desempleo": ["desempleo", "paro", "subsidio", "desocupa", "inactividad"],
        "maternidad": ["maternidad", "paternidad", "nacimiento", "cuidado", "embarazo", "riesgo", "bebe", "parto"],
        "cuota": ["cuota", "cotización", "cotizacion", "autónomo", "base", "pago ss", "autonomo"],
        "ayuda_hijo": ["hijo a cargo", "ayuda familiar", "puntos", "menor", "descendiente"],
        "imv": ["ingreso mínimo vital", "imv", "renta garantizada", "vital", "ayuda social"],
        "cume": ["cume", "cáncer", "cancer", "menor grave", "enfermedad grave hijo"],
        "beneficios_hijos": ["asimilado", "parto", "excedencia hijos", "cuidado hijos", "art 235", "art 236"],
        "recargo_ss": ["recargo", "apremio", "documentos cotización", "liquidación ss"],
        "intereses_demora": ["intereses", "demora ss", "día 16", "notificación providencia"],
        "it_especial": ["menstruacion", "menstruación", "semana 39", "interrupción embarazo", "salud reproductiva"],
        "base_cotizacion_completa": ["base completa", "suplidos", "dietas", "plus desplazamiento", "horas extras"],
        "lagunas_jubilacion": ["lagunas", "base mínima RETA", "cero lagunas", "da 37"],
        "br_dt34": ["302 meses", "dt 34", "dt34", "bases mejores", "352,33"],
        "efectos_cambio_reta": ["efectos cambio base", "ventana mensual", "solicitud octubre reta"],
        "tipo_enajenacion": ["subasta", "valor tasado", "cargas anteriores", "cargas posteriores"],
        "jubilacion_demorada": ["jubilación demorada", "art 210", "4% adicional", "activa demorada"],
        "derivacion_ss": ["derivación", "solidaria", "subsidiaria", "cooperativa", "grupos"],
        "cuota_corta_duracion": ["contrato corta duración", "menos de 8 días", "extra 32"]
    }

    @staticmethod
    def _normalizar_fecha(texto: str) -> Optional[str]:
        """Extrae y normaliza fechas en formato DD/MM/YYYY o YYYY-MM-DD"""
        # Formato español: DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY
        match_es = re.search(r'(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{2,4})', texto)
        if match_es:
            d, m, y = match_es.groups()
            if len(y) == 2: y = "20" + y  # Asumir siglo 21
            try:
                return f"{y}-{m.zfill(2)}-{d.zfill(2)}"
            except: return None
        
        # Formato ISO: YYYY-MM-DD
        match_iso = re.search(r'(\d{4})-(\d{2})-(\d{2})', texto)
        if match_iso:
            return match_iso.group(0)
        
        return None

    @staticmethod
    def _extraer_anio_caso(texto: str) -> int:
        """
        Extrae el año del caso práctico para aplicar constantes históricas correctas.
        Busca años plausibles (1990-2030) en el texto.
        Si no encuentra ninguno, devuelve 2026 (año actual del sistema).
        """
        # Buscar años de 4 dígitos en rango plausible
        matches = re.findall(r'\b(20[0-2]\d|19[9]\d)\b', texto)
        if matches:
            # Tomar el año más reciente mencionado (el del caso)
            anos = [int(a) for a in matches]
            # Filtrar: descartar años que parezcan artículos (ej. "art 2024")
            anos_probables = [a for a in anos if a >= 1990 and a <= 2030]
            if anos_probables:
                return max(anos_probables)  # El año más reciente del caso
        return 2026  # Default: año actual

    @staticmethod
    def identificar_dominio(texto: str) -> str:
        texto_lower = texto.lower()
        # Contar ocurrencias para decidir dominio si hay solapamiento
        score_ss = sum(1 for kw in CasosPracticosDispatcher.DOMINIOS["SS"] if kw in texto_lower)
        score_age = sum(1 for kw in CasosPracticosDispatcher.DOMINIOS["AGE"] if kw in texto_lower)
        
        # Priorizar AGE si se mencionan leyes administrativas o TREBEP
        if any(x in texto_lower for x in ["ley 39", "ley 40", "lpac", "trebep"]):
            return "AGE"
            
        # Forzar AGE para palabras clave de presupuesto/contratación muy específicas
        if any(x in texto_lower for x in [
            "vec", "pbl", "valor estimado contrato", "presupuesto base de licitación",
            "anticipo de caja fija", "anticipo caja fija", "pago a justificar",
            "crédito presupuestario", "credito presupuestario", "modificación presupuestaria",
            "reintegro subvención", "reintegro subvencion", "pgcp", "tribunal de cuentas",
            "garantía definitiva", "garantia definitiva", "garantía provisional",
            "nómina mensual", "nomina mensual", "paga extra", "paga extraordinaria",
            "complemento específico", "complemento de destino", "trienio",
        ]):
            return "AGE"
            
        if score_age > score_ss:
            return "AGE"
        if score_ss > 0:
            return "SS"
        return "SS" # Default a SS

    @staticmethod
    def identificar_tipo_especifico(texto: str, dominio: str) -> str:
        texto_lower = texto.lower()
        if dominio == "AGE":
            if any(x in texto_lower for x in ["alzada", "superior"]): return "calcular_plazo_alzada"
            if any(x in texto_lower for x in ["reposición", "reposicion", "potestativo"]): return "calcular_plazo_reposicion"
            if any(x in texto_lower for x in ["silencio", "espera", "no contesta"]): return "calcular_silencio_administrativo"
            if any(x in texto_lower for x in ["vencimiento", "vence", "fecha", "termina"]): return "calcular_fecha_vencimiento"
            if any(x in texto_lower for x in ["prescripción", "prescripcion", "sanción", "sancion"]): return "calcular_prescripcion_disciplinaria"
            if any(x in texto_lower for x in ["extraordinario", "revisión", "revision"]): return "calcular_plazo_extraordinario_revision"
            if any(x in texto_lower for x in ["vacaciones", "vacas"]): return "calcular_vacaciones_trebep"
            if any(x in texto_lower for x in ["asuntos propios", "moscosos"]): return "calcular_asuntos_propios_trebep"
            if any(x in texto_lower for x in ["subsanacion", "subsanar"]): return "calcular_subsanacion"
            if any(x in texto_lower for x in ["recusacion", "abstencion"]): return "calcular_abstencion_recusacion"
            # Retribuciones / nóminas
            if any(x in texto_lower for x in ["nómina", "nomina", "sueldo mensual", "neto mensual"]): return "calcular_nomina_mensual"
            if any(x in texto_lower for x in ["paga extra", "paga extraordinaria", "junio", "diciembre"]): return "calcular_pagas_extra"
            if any(x in texto_lower for x in ["dietas", "kilómetros", "desplazamiento servicio"]): return "calcular_indemnizacion_dietas"
            # Contratación pública
            if any(x in texto_lower for x in ["vec", "valor estimado contrato"]): return "calcular_vec"
            if any(x in texto_lower for x in ["pbl", "presupuesto base", "licitación", "licitacion"]): return "calcular_pbl"
            if any(x in texto_lower for x in ["garantía definitiva", "garantia definitiva", "garantía provisional"]): return "calcular_garantia_contrato"
            if any(x in texto_lower for x in ["contrato menor", "regulación armonizada", "doue", "umbral ue"]): return "clasificar_contrato_lcsp"
            # Presupuesto
            if any(x in texto_lower for x in ["crédito disponible", "credito disponible", "partida presupuestaria", "ad-o-p"]): return "calcular_credito_disponible"
            if any(x in texto_lower for x in ["modificación presupuestaria", "transferencia de credito", "ampliación"]): return "calcular_modificacion_presupuestaria"
            if any(x in texto_lower for x in ["anticipo caja fija", "acf"]): return "calcular_anticipo_caja_fija"
            if any(x in texto_lower for x in ["pago a justificar", "pj"]): return "calcular_plazo_justificacion_pj"
            if any(x in texto_lower for x in ["reintegro subvención", "reintegro subvencion", "ley 38"]): return "calcular_reintegro_subvencion"
            if any(x in texto_lower for x in ["asiento", "pgcp", "contable", "cuenta"]): return "identificar_asiento_pgcp"
            return "tipo_computo_plazo"
        else:
            # Priorizar términos más largos/específicos: Jubilación Parcial
            if any(re.search(fr'\b{x}\b', texto_lower) for x in ["parcial", "parssial", "relevo"]):
                if any(re.search(fr'\b{x}\b', texto_lower) for x in ["jubila", "jubilación", "jubilacion", "jubilasion"]):
                    return "jubilacion_parcial"
            
            # Búsqueda general por diccionario
            for tipo, kws in CasosPracticosDispatcher.TIPOS_CASO_SS.items():
                if any(re.search(fr'\b{x}\b', texto_lower) for x in kws):
                    return tipo
            
            # Fallback a IT si hay mención a enfermedad
            if "enfermedad" in texto_lower or "baja" in texto_lower:
                return "subsidio_it"
                
            return "subsidio_it"

    @staticmethod
    def ejecutar(texto: str) -> Dict[str, Any]:
        """
        Punto de entrada principal para los agentes.
        """
        dominio = CasosPracticosDispatcher.identificar_dominio(texto)
        tipo = CasosPracticosDispatcher.identificar_tipo_especifico(texto, dominio)
        
        resultado = {"dominio": dominio, "tipo": tipo, "datos": None}

        # Extracción básica de números (Base Reguladora, Años, etc)
        numbers = re.findall(r'(\d+[\.,]?\d*)', texto)
        # Limpiar puntos de miler si existen (ej 1.500,50 -> 1500.50)
        cleaned_numbers = []
        for n in numbers:
            if ',' in n and '.' in n:
                n = n.replace('.', '').replace(',', '.')
            elif ',' in n:
                n = n.replace(',', '.')
            try:
                val = Decimal(n)
                # Omitir si es un año puro (ej. 2024, 2026) sin decimales y en rango lógico
                if val == int(val) and 1990 <= int(val) <= 2030:
                    continue
                cleaned_numbers.append(val)
            except: continue
        
        base = cleaned_numbers[0] if cleaned_numbers else Decimal("1500")
        cantidad = int(cleaned_numbers[1]) if len(cleaned_numbers) > 1 else 30

        try:
            if dominio == "AGE":
                # Herramientas de presupuesto — dominio PRESUPUESTO dentro de AGE
                TOOLS_PRESUPUESTO_KEYS = set(TOOLS_PRESUPUESTO.keys())
                params = {}
                if tipo in TOOLS_PRESUPUESTO_KEYS:
                    # Extraer parámetros específicos para presupuesto
                    if tipo == "calcular_credito_disponible":
                        params["credito_inicial"] = float(base)
                        if len(cleaned_numbers) > 1:
                            params["ampliaciones"] = float(cleaned_numbers[1])
                    elif tipo == "calcular_modificacion_presupuestaria":
                        tipo_mod = "transferencia"
                        for t in ["ampliacion", "suplemento", "incorporacion", "generacion"]:
                            if t in texto.lower():
                                tipo_mod = t
                                break
                        params = {"tipo": tipo_mod, "importe": float(base), "credito_actual": float(cleaned_numbers[1]) if len(cleaned_numbers) > 1 else 100000}
                    elif tipo == "calcular_anticipo_caja_fija":
                        params = {"dotacion_acf": float(base), "importe_pago": float(cleaned_numbers[1]) if len(cleaned_numbers) > 1 else float(base) * 0.5}
                    elif tipo == "calcular_reintegro_subvencion":
                        params = {"importe_subvencion": float(base), "pct_incumplimiento": float(cleaned_numbers[1]) if len(cleaned_numbers) > 1 else 50.0}
                    elif tipo == "calcular_vec":
                        params = {"importe_anual_sin_iva": float(base), "anos_duracion": float(cleaned_numbers[1]) if len(cleaned_numbers) > 1 else 2.0}
                    elif tipo == "calcular_pbl":
                        ci_val = float(cleaned_numbers[1]) if len(cleaned_numbers) > 1 else float(base) * 0.1
                        params = {"costes_directos": float(base), "costes_indirectos": ci_val}
                    resultado["datos"] = ejecutar_calculo_presupuesto(tipo, params)
                elif tipo in (
                    "calcular_nomina_mensual", "calcular_pagas_extra", "calcular_indemnizacion_dietas",
                    "calcular_garantia_contrato", "clasificar_contrato_lcsp",
                    "calcular_vec", "calcular_pbl",
                ):
                    # Nóminas, contratos LCSP, VEC/PBL
                    subgrupo = "C1"
                    for sg in ["A1", "A2", "C1", "C2"]:
                        if sg.lower() in texto.lower():
                            subgrupo = sg
                            break
                    nivel = int(base) if base < 30 else 18
                    ce = float(cleaned_numbers[1]) if len(cleaned_numbers) > 1 else 600.0
                    trienios_num = int(cleaned_numbers[2]) if len(cleaned_numbers) > 2 else 0
                    if tipo == "calcular_nomina_mensual":
                        params = {"subgrupo": subgrupo, "nivel_cd": nivel, "ce_mensual": ce, "trienios": trienios_num}
                    elif tipo == "calcular_pagas_extra":
                        params = {"subgrupo": subgrupo, "nivel_cd": nivel}
                    elif tipo == "calcular_indemnizacion_dietas":
                        grupo = 1 if subgrupo in ["A1", "A2"] else 2
                        params = {"grupo": grupo, "dias_completos": int(base) if base <= 60 else 3, "km": float(cleaned_numbers[1]) if len(cleaned_numbers) > 1 else 0}
                    elif tipo == "calcular_garantia_contrato":
                        params = {"pbl_sin_iva": float(base), "tipo": "definitiva"}
                    elif tipo == "clasificar_contrato_lcsp":
                        params = {"vec": float(base)}
                    elif tipo == "calcular_vec":
                        # importe_anual: primer número grande; anos_duracion: segundo número
                        nums_grandes = [float(n) for n in cleaned_numbers if n > 100]
                        nums_pequenos = [float(n) for n in cleaned_numbers if n <= 10]
                        params = {
                            "importe_anual_sin_iva": nums_grandes[0] if nums_grandes else float(base),
                            "anos_duracion": nums_pequenos[0] if nums_pequenos else 2.0,
                        }
                    elif tipo == "calcular_pbl":
                        # extraer costes directos e indirectos: primeros dos números grandes
                        nums_grandes = [float(n) for n in cleaned_numbers if n > 100]
                        cd_val = nums_grandes[0] if nums_grandes else float(base)
                        ci_val = nums_grandes[1] if len(nums_grandes) > 1 else cd_val * 0.1
                        pct_b = float(cleaned_numbers[-2]) if len(cleaned_numbers) >= 2 else 6.0
                        iva_v = float(cleaned_numbers[-1]) if len(cleaned_numbers) >= 1 else 21.0
                        # Buscar % bn y %IVA en el texto
                        m_bn = re.search(r'beneficio[\s_]*(\d+)', texto, re.I)
                        m_iva = re.search(r'iva[\s_]*(\d+)', texto, re.I)
                        params = {
                            "costes_directos": cd_val,
                            "costes_indirectos": ci_val,
                            "pct_beneficio_industrial": float(m_bn.group(1)) if m_bn else 6.0,
                            "pct_iva": float(m_iva.group(1)) if m_iva else 21.0,
                        }
                    resultado["datos"] = ejecutar_calculo_age(tipo, params)
                else:
                    # Lógica AGE plazos/procedimientos estándar
                    params = {}
                    fecha_norm = CasosPracticosDispatcher._normalizar_fecha(texto)
                    if fecha_norm: params["fecha_inicio"] = fecha_norm
                    if "vacaciones" in tipo or "asuntos" in tipo:
                        params["antiguedad_anos"] = int(base) if base < 100 else 0
                    else:
                        params["cantidad"] = int(base) if base < 1000 else cantidad
                    if any(x in texto.lower() for x in ["mes", "mensual"]):
                        params["unidad"] = "meses"
                    elif any(x in texto.lower() for x in ["día", "dia", "diario"]):
                        params["unidad"] = "dias"
                    resultado["datos"] = ejecutar_calculo_age(tipo, params)
            else:
                # Lógica SS
                if tipo == "subsidio_it":
                    # Extraer día de baja del texto (ej. "día 45" o "20 días")
                    # re ya está importado a nivel de módulo
                    dia_match = re.search(r'd[íi]a\s*(\d+)', texto.lower())
                    if not dia_match:
                        # Fallback a buscar cualquier número si no hay "día X"
                        dia_match = re.search(r'(\d+)\s*d[íi]a', texto.lower())
                    
                    dia_real = int(dia_match.group(1)) if dia_match else 15
                    
                    # Determinar contingencia (default EC)
                    contingencia = "EC"
                    if any(x in texto.lower() for x in ["accidente", "at", "trabajo"]):
                        contingencia = "AT"
                    elif any(x in texto.lower() for x in ["profesional", "ep"]):
                        contingencia = "EP"
                        
                    resultado["datos"] = calcular_subsidio_it(float(base), contingencia, dia_real)
                elif tipo == "jubilacion":
                    # Si es jubilación ordinaria en 2026, usar la edad variable
                    # Para simplificar, si no se especifica edad en el texto, calculamos la edad legal 2026
                    # basándonos en los años cotizados (cantidad)
                    from calculators.calculos_ss_extended import CalculadoraJubilacion
                    resultado["datos"] = vars(CalculadoraJubilacion.calcular_jubilacion(base, 0, int(cantidad)))
                elif tipo == "ipp":
                    resultado["datos"] = CalculadoraIPP.calcular_ipp(float(base))
                elif tipo == "viudedad":
                    resultado["datos"] = vars(CalculadoraViudedad.calcular_viudedad(float(base), "cargas" in texto.lower()))
                elif tipo == "imv":
                    resultado["datos"] = vars(CalculadoraIMV.calcular_imv(TipoUnidadFamiliar.PERSONA_SOLA, 0.0))
                elif tipo == "cume":
                    resultado["datos"] = CalculadoraCUME.calcular_cume(float(base), float(cantidad)/100.0 if cantidad > 0 else 0.5)
                elif tipo == "beneficios_hijos":
                    resultado["datos"] = CalculadoraBeneficiosHijos.calcular_periodos_asimilados(int(base), int(cantidad))
                elif tipo == "supervivencia":
                    fecha_obj = None
                    try:
                        fecha_str = CasosPracticosDispatcher._normalizar_fecha(texto)
                        if fecha_str:
                            from datetime import date
                            fecha_obj = date.fromisoformat(fecha_str)
                    except: pass
                    
                    if "defunción" in texto.lower() or "auxilio" in texto.lower():
                        resultado["datos"] = vars(CalculadoraSupervivencia.calcular_auxilio_defuncion())
                    else:
                        resultado["datos"] = [vars(r) for r in CalculadoraSupervivencia.calcular_indemnizacion_muerte_at_ep(float(base), int(cantidad), fecha_hecho=fecha_obj)]
                
                # Nuevas 11 calculadoras SS V13
                elif tipo == "recargo_ss":
                    resultado["datos"] = calcular_recargo_ss("presentó" in texto.lower(), "ejecutivo" in texto.lower() or "apremio" in texto.lower(), "voluntario" in texto.lower())
                elif tipo == "intereses_demora":
                    resultado["datos"] = calcular_intereses_demora_ss("principal" in texto.lower(), int(cantidad) if cantidad else 1)
                elif tipo == "it_especial":
                    sit = "menstruacion"
                    if "semana 39" in texto.lower(): sit = "semana_39_gestacion"
                    elif "interrupción" in texto.lower(): sit = "interrupcion_embarazo"
                    resultado["datos"] = calcular_it_situaciones_especiales_lo1_2023(Decimal(str(base)), sit)
                elif tipo == "base_cotizacion_completa":
                    resultado["datos"] = calcular_base_cotizacion_completa(Decimal(str(base)), float(cantidad), 0, Decimal("100"), Decimal(str(base*0.1)), Decimal("0"), Decimal("0"))
                elif tipo == "lagunas_jubilacion":
                    reg = "RETA" if "reta" in texto.lower() or "autónomo" in texto.lower() else "RG"
                    resultado["datos"] = calcular_integracion_lagunas_jubilacion(int(cantidad) if cantidad else 12, reg, "F" if "mujer" in texto.lower() else "H")
                elif tipo == "br_dt34":
                    # Dummy descending array for DT34 logic demonstration
                    bases = [Decimal(str(base))] * 304
                    resultado["datos"] = calcular_br_jubilacion_dt34(bases)
                elif tipo == "efectos_cambio_reta":
                    from datetime import date
                    resultado["datos"] = calcular_fecha_efectos_cambio_base_reta(date.today())
                elif tipo == "tipo_enajenacion":
                    resultado["datos"] = calcular_tipo_enajenacion(Decimal(str(base)), Decimal(str(cantidad)), Decimal("0"))
                elif tipo == "jubilacion_demorada":
                    resultado["datos"] = calcular_jubilacion_demorada(Decimal(str(base)), int(cantidad) if cantidad else 1, "activa" in texto.lower())
                elif tipo == "derivacion_ss":
                    t_d = "socio_cooperativa_hacia_cooperativa" if "cooperativa" in texto.lower() else "solidaria"
                    resultado["datos"] = calcular_derivacion_responsabilidad_ss(t_d, Decimal(str(base)), Decimal(str(cantidad)), Decimal("0"))
                elif tipo == "cuota_corta_duracion":
                    resultado["datos"] = calcular_cuota_contrato_corta_duracion()

    
            if resultado["datos"] and "tipo_unidad" in resultado["datos"]:
                resultado["datos"]["tipo_unidad"] = str(resultado["datos"].get("tipo_unidad"))
        except Exception as e:
            resultado["error"] = str(e)

        return resultado

def procesar_caso(texto: str) -> Dict[str, Any]:
    """Helper para compatibilidad con la API actual"""
    return CasosPracticosDispatcher.ejecutar(texto)
