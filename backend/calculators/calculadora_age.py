"""
Calculadora AGE - Cómputos procedimentales Ley 39/2015 y TREBEP
==============================================================
Implementación determinística para casos prácticos de la AGE.
"""

from decimal import Decimal, ROUND_HALF_UP
from datetime import date, datetime, timedelta
from typing import Optional, Dict, Any, List

# Helper para redondear a 2 decimales si fuera necesario (aunque AGE es más de plazos)
D = lambda x: Decimal(str(x))
R2 = lambda x: x.quantize(D('0.01'), rounding=ROUND_HALF_UP)

def calcular_plazo_alzada(fecha_notificacion: Optional[str] = None) -> Dict[str, Any]:
    """
    Calcula plazo para recurso de alzada (Art. 121 LPAC)
    1 mes si el acto es expreso.
    """
    return {
        "plazo": "1 mes",
        "tipo_dias": "Días hábiles / De fecha a fecha",
        "inicio_computo": f"Desde el día siguiente a la notificación ({fecha_notificacion})" if fecha_notificacion else "Desde el día siguiente a la notificación",
        "organo_competente": "Superior jerárquico del que dictó el acto",
        "efecto_silencio": "Desestimatorio (negativo) - Art. 122.1 LPAC",
        "articulo": "Art. 121-122 Ley 39/2015"
    }

def calcular_plazo_reposicion(fecha_notificacion: Optional[str] = None) -> Dict[str, Any]:
    """
    Calcula plazo para recurso de reposición (Art. 124 LPAC)
    1 mes (potestativo).
    """
    return {
        "plazo": "1 mes",
        "tipo_dias": "Días hábiles / De fecha a fecha",
        "caracter": "POTESTATIVO - previo al contencioso-administrativo",
        "efecto_silencio": "Desestimatorio (negativo) - Art. 124.3 LPAC",
        "plazo_silencio": "1 mes para resolver",
        "articulo": "Art. 124 Ley 39/2015"
    }

def calcular_silencio_administrativo(tipo_procedimiento: str = "solicitud", es_recurso: bool = False) -> Dict[str, Any]:
    """
    Identifica el sentido del silencio administrativo según Art. 24 y 25 LPAC.
    """
    if es_recurso:
        return {
            "silencio": "NEGATIVO (desestimatorio)",
            "razon": "Los recursos siempre producen silencio negativo (excepción: doble silencio en ciertos casos)",
            "articulo": "Arts. 122.1 y 124.3 Ley 39/2015"
        }

    SILENCIO_MAP = {
        "solicitud": {
            "silencio": "POSITIVO (estimatorio) - Regla General",
            "excepciones": ["Derecho de petición", "Normas de rango legal", "Medio ambiente", "Dominio público"],
            "articulo": "Art. 24 Ley 39/2015"
        },
        "oficio_efectos_favorables": {
            "silencio": "NEGATIVO (desestimatorio)",
            "razon": "Procedimientos de los que pudieran derivarse derechos (Art. 25.1.a)",
            "articulo": "Art. 25.1.a Ley 39/2015"
        },
        "oficio_gravamen": {
            "silencio": "CADUCIDAD",
            "razon": "Procedimientos sancionadores o de intervención (Art. 25.1.b)",
            "articulo": "Art. 25.1.b Ley 39/2015"
        },
        "sancionador": {
            "silencio": "CADUCIDAD",
            "razon": "Caducidad si no hay resolución en plazo máximo (3 o 6 meses)",
            "articulo": "Art. 90 Ley 39/2015"
        }
    }

    return SILENCIO_MAP.get(tipo_procedimiento, {
        "error": f"Tipo de procedimiento desconocido: {tipo_procedimiento}",
        "opciones": list(SILENCIO_MAP.keys())
    })

def tipo_computo_plazo(unidad: str = "dias") -> Dict[str, Any]:
    """
    Determina cómo se computa un plazo según la unidad (Art. 30 LPAC).
    """
    if unidad.lower() in ["horas"]:
        return {
            "regla": "De hora en hora, de minuto en minuto",
            "inicio": "Desde la notificación o publicación",
            "articulo": "Art. 30.1 LPAC"
        }
    elif unidad.lower() in ["dias", "días"]:
        return {
            "regla": "HÁBILES por defecto (excluye sábados, domingos y festivos)",
            "excepcion": "NATURALES si la ley o convocatoria lo indica",
            "articulo": "Art. 30.2 LPAC"
        }
    elif unidad.lower() in ["meses", "años", "mes", "año"]:
        return {
            "regla": "De fecha a fecha",
            "fin_plazo": "Si el último día es inhábil, se entiende prorrogado al primer día hábil siguiente",
            "articulo": "Art. 30.4 LPAC"
        }
    
    return {"error": "Unidad de tiempo no reconocida"}

def calcular_fecha_vencimiento(fecha_inicio: str, cantidad: int, unidad: str = "dias", habiles: bool = True) -> Dict[str, Any]:
    """
    Calcula la fecha de vencimiento de un plazo (Ley 39/2015).
    """
    try:
        notif_date = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    except:
        return {"error": "Formato de fecha inválido. Usar AAAA-MM-DD"}
    
    if unidad.lower() in ["dias", "días"]:
        # El cómputo empieza el día siguiente
        current_date = notif_date + timedelta(days=1)
        added = 0
        while added < cantidad:
            if habiles:
                # Sábado es 5, Domingo es 6
                if current_date.weekday() < 5:
                    added += 1
            else:
                added += 1
            
            if added < cantidad:
                current_date += timedelta(days=1)
        
        # Si el último día es fin de semana (inhábil), se prorroga
        while current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            
    elif unidad.lower() in ["meses", "mes"]:
        # Art. 30.4: De fecha a fecha. Vence el mismo día del mes siguiente.
        import calendar
        month = notif_date.month - 1 + cantidad
        year = notif_date.year + month // 12
        month = month % 12 + 1
        # El día de vencimiento es el mismo que el de la notificación (Art. 30.4)
        # Si ese día no existe en el mes de destino, es el último del mes.
        day = min(notif_date.day, calendar.monthrange(year, month)[1])
        current_date = date(year, month, day)
        
        # Prórroga si el día de vencimiento es inhábil
        while current_date.weekday() >= 5:
            current_date += timedelta(days=1)

    return {
        "fecha_notificacion": notif_date.isoformat(),
        "fecha_inicio_computo": (notif_date + timedelta(days=1)).isoformat(),
        "fecha_vencimiento": current_date.isoformat(),
        "dias_totales_naturales": (current_date - notif_date).days,
        "advertencia": "No se han computado festivos locales/nacionales. Solo fines de semana.",
        "normativa": "Art. 30 Ley 39/2015"
    }

def calcular_prescripcion_disciplinaria(gravedad: str = "muy_grave", tipo_sujeto: str = "funcionario") -> Dict[str, Any]:
    """
    Plazos de prescripción de infracciones y sanciones (TREBEP o Ley 40).
    """
    if tipo_sujeto == "funcionario":
        # TREBEP Arts. 97 y 98
        PRESCRIPCION = {
            "muy_grave": {"infraccion": "3 años", "sancion": "3 años"},
            "grave": {"infraccion": "2 años", "sancion": "2 años"},
            "leve": {"infraccion": "6 meses", "sancion": "1 año (sanción) / 6 meses (infracción)"}
        }
    else:
        # Ley 40/2015 Art. 30 (Administrativa general)
        PRESCRIPCION = {
            "muy_grave": {"infraccion": "3 años", "sancion": "3 años"},
            "grave": {"infraccion": "2 años", "sancion": "2 años"},
            "leve": {"infraccion": "6 meses", "sancion": "1 año"}
        }

    return PRESCRIPCION.get(gravedad.lower(), {"error": "Gravedad no válida"})

def calcular_plazo_extraordinario_revision(motivo: str = "error_hecho") -> Dict[str, Any]:
    """
    Art. 125 LPAC - Recurso extraordinario de revisión.
    """
    if "error" in motivo.lower() or "hecho" in motivo.lower():
        plazo = "4 años"
        explicacion = "Error de hecho al dictar el acto (4 años desde notificación)"
    else:
        plazo = "3 meses"
        explicacion = "Aparición de documentos, prevaricación, testimonio falso, etc. (3 meses desde conocimiento)"
        
    return {
        "plazo": plazo,
        "motivo": motivo,
        "organo": "Mismo órgano que dictó el acto",
        "silencio": "Desestimatorio (3 meses sin resolución)",
        "articulo": "Art. 125 y 126 Ley 39/2015",
        "explicacion": explicacion
    }

def calcular_abstencion_recusacion(tipo: str = "recusacion") -> Dict[str, Any]:
    """
    Arts. 23 y 24 Ley 40/2015.
    """
    return {
        "plazo": "En cualquier momento (recusación)",
        "tramite": "10 días para que el recusado se manifieste",
        "resolucion": "3 días para que el superior resuelva",
        "efecto": "No suspende el procedimiento principal (salvo decisión motivada)",
        "articulo": "Arts. 23-24 Ley 40/2015"
    }

def calcular_subsanacion(fecha_notificacion: Optional[str] = None) -> Dict[str, Any]:
    """
    Art. 68 LPAC - Subsanación y mejora de la solicitud.
    """
    return {
        "plazo_general": "10 días hábiles",
        "ampliacion": "Hasta 5 días adicionales si la dificultad lo justifica (excepto procesos selectivos)",
        "consecuencia": "Se le tiene por desistido si no subsana",
        "articulo": "Art. 68 Ley 39/2015"
    }

def calcular_vacaciones_trebep(antiguedad_anos: int = 0) -> Dict[str, Any]:
    """
    Art. 50 TREBEP - Vacaciones de los funcionarios.
    """
    dias_base = 22 # Días hábiles
    adicionales = 0
    if antiguedad_anos >= 15: adicionales = 1
    if antiguedad_anos >= 20: adicionales = 2
    if antiguedad_anos >= 25: adicionales = 3
    if antiguedad_anos >= 30: adicionales = 4
    
    return {
        "dias_habiles": dias_base + adicionales,
        "detalle": f"22 base + {adicionales} por antigüedad ({antiguedad_anos} años)",
        "articulo": "Art. 50 TREBEP",
        "nota": "Se pueden disfrutar en periodos de mínimo 5 días hábiles consecutivos"
    }

def calcular_asuntos_propios_trebep(antiguedad_anos: int = 0) -> Dict[str, Any]:
    """
    Art. 48.k TREBEP - Permisos por asuntos particulares.
    """
    dias_base = 6
    adicionales = 0
    if antiguedad_anos >= 18: adicionales += 2 # Al trienio de los 18
    # Cada 3 años adicionales desde los 18, 1 día más
    if antiguedad_anos > 18:
        adicionales += (antiguedad_anos - 18) // 3
        
    return {
        "dias_totales": dias_base + adicionales,
        "detalle": f"6 base + {adicionales} por antigüedad",
        "articulo": "Art. 48.k TREBEP",
        "advertencia": "Sujeto a necesidades del servicio"
    }

def calcular_intentos_notificacion(primer_intento_hora: str) -> Dict[str, Any]:
    """
    Art. 42.2 LPAC - Intentos de notificación.
    """
    return {
        "segundo_intento": "En los 3 días siguientes",
        "margen_horario": "Diferencia de al menos 3 horas respecto al primero",
        "ejemplo": f"Si el 1º fue a las {primer_intento_hora}, el 2º debe variar al menos 3h",
        "articulo": "Art. 42.2 Ley 39/2015"
    }

def calcular_ejecutividad_suspension(es_sancion: bool = False) -> Dict[str, Any]:
    """
    Art. 98 y 117 LPAC - Ejecutividad y suspensión.
    """
    return {
        "regla_general": "Los actos son ejecutivos de inmediato",
        "excepcion_sancion": "No ejecutivos hasta que finalice la vía administrativa" if es_sancion else "N/A",
        "suspension_por_recurso": "1 mes de silencio sin respuesta a la solicitud de suspensión = SUSPENSIÓN AUTOMÁTICA",
        "articulo": "Arts. 90.3, 98 y 117.3 Ley 39/2015"
    }

def calcular_responsabilidad_patrimonial(fecha_hecho: str) -> Dict[str, Any]:
    """
    Art. 67 LPAC - Plazo para reclamar responsabilidad patrimonial.
    """
    return {
        "plazo": "1 año",
        "inicio": "Desde que se produjo el hecho o se manifestó su efecto lesivo",
        "articulo": "Art. 67 Ley 39/2015"
    }

def calcular_revision_oficio(vicio: str = "nulo") -> Dict[str, Any]:
    """
    Art. 106 y 107 LPAC - Revisión de oficio.
    """
    if vicio.lower() == "nulo":
        return {
            "plazo": "En cualquier momento (no prescribe)",
            "tipo": "Actos nulos de pleno derecho",
            "articulo": "Art. 106 Ley 39/2015"
        }
    else:
        return {
            "plazo": "4 años",
            "tipo": "Declaración de lesividad (actos anulables)",
            "articulo": "Art. 107 Ley 39/2015"
        }

def calcular_caducidad_procedimiento(iniciado: str = "oficio", efectos: str = "favorables") -> Dict[str, Any]:
    """
    Art. 25 y 95 LPAC - Caducidad.
    """
    if iniciado == "oficio":
        if efectos == "favorables":
            return {"resultado": "SILENCIO NEGATIVO", "articulo": "Art. 25.1.a"}
        else:
            return {"resultado": "CADUCIDAD", "articulo": "Art. 25.1.b"}
    else:
        return {
            "plazo": "3 meses de paralización por causa imputable al interesado",
            "resultado": "CADUCIDAD (archivo de actuaciones)",
            "articulo": "Art. 95 LPAC"
        }

def calcular_rectificacion_errores() -> Dict[str, Any]:
    """
    Art. 109.2 LPAC.
    """
    return {
        "plazo": "En cualquier momento",
        "tipo": "Errores materiales, de hecho o aritméticos",
        "procedimiento": "De oficio o a instancia de parte",
        "articulo": "Art. 109.2 Ley 39/2015"
    }

def calcular_tramite_audiencia() -> Dict[str, Any]:
    """
    Art. 82 LPAC.
    """
    return {
        "plazo": "No inferior a 10 ni superior a 15 días",
        "momento": "Instruido el procedimiento e inmediatamente antes de redactar la propuesta de resolución",
        "articulo": "Art. 82 Ley 39/2015"
    }

def calcular_informes(tipo: str = "facultativo") -> Dict[str, Any]:
    """
    Art. 79 y 80 LPAC.
    """
    return {
        "plazo_general": "10 días (salvo que una norma o la petición fijen otro)",
        "caracter": "Facultativos y no vinculantes (salvo disposición en contrario)",
        "efecto_falta_informe": "Se podrán proseguir las actuaciones",
        "articulo": "Arts. 79-80 Ley 39/2015"
    }

def calcular_medidas_provisionales(momento: str = "antes_inicio") -> Dict[str, Any]:
    """
    Art. 56 LPAC - Medidas provisionales.
    """
    if momento == "antes_inicio":
        return {
            "plazo_confirmacion": "15 días para iniciar el procedimiento tras la medida",
            "efecto": "Si no se inicia en 15 días, las medidas quedan sin efecto",
            "articulo": "Art. 56.2 Ley 39/2015"
        }
    else:
        return {
            "regla": "Se pueden adoptar en cualquier momento del procedimiento",
            "articulo": "Art. 56.1 Ley 39/2015"
        }

def calcular_desistimiento_renuncia() -> Dict[str, Any]:
    """
    Art. 93 y 94 LPAC.
    """
    return {
        "desistimiento": "El interesado abandona su solicitud (puede volver a pedir)",
        "renuncia": "El interesado abandona su derecho (no puede volver a pedir)",
        "efecto": "La Administración debe dictar resolución aceptándolo y declarando el fin",
        "articulo": "Arts. 93-94 Ley 39/2015"
    }

def calcular_identificacion_firma(tipo: str = "firma") -> Dict[str, Any]:
    """
    Art. 9-11 LPAC.
    """
    return {
        "identificacion": "Solo para trámites simples",
        "firma": "Obligatoria para: formular solicitudes, presentar declaraciones responsables, interponer recursos y desistir de acciones",
        "articulo": "Arts. 9, 10 y 11 Ley 39/2015"
    }

# ============================================================================
# BLOQUE B — TREBEP AVANZADO (Nuevas funciones Apéndice VII)
# ============================================================================

def calcular_trienios(anos_servicio: int = 0, grupo: str = "A1") -> Dict[str, Any]:
    """
    Art. 25 TREBEP — Complemento de antigüedad por trienios.
    Constantes aproximadas basadas en PGE 2024/2026.
    """
    importes_por_grupo = {"A1": 50.07, "A2": 40.64, "B": 35.00, "C1": 30.61, "C2": 20.84, "E": 15.68}
    periodo_trienio = 3  # años
    num_trienios = anos_servicio // periodo_trienio
    importe_unitario = importes_por_grupo.get(grupo.upper(), 30.61)
    total_mensual = num_trienios * importe_unitario
    return {
        "anos_servicio": anos_servicio,
        "grupo": grupo.upper(),
        "num_trienios": num_trienios,
        "importe_unitario_euros": round(importe_unitario, 2),
        "total_mensual_euros": round(total_mensual, 2),
        "proximo_trienio_en_anos": periodo_trienio - (anos_servicio % periodo_trienio),
        "articulo": "Art. 25 TREBEP + Ley PGE"
    }


def calcular_grado_personal(nivel_puesto: int = 15, anos_en_nivel: int = 0) -> Dict[str, Any]:
    """
    Arts. 21-22 TREBEP + RD 364/1995 — Grado personal consolidado.
    Se consolida el grado al desempeñar un puesto de nivel superior
    durante 2 años continuos o 3 alternos.
    Niveles: del 1 (mínimo) al 30 (máximo).
    """
    continuos_requeridos = 2
    alternos_requeridos = 3
    consolidado = anos_en_nivel >= continuos_requeridos
    return {
        "nivel_puesto_actual": nivel_puesto,
        "anos_en_nivel": anos_en_nivel,
        "grado_consolidado": nivel_puesto if consolidado else max(nivel_puesto - 2, 1),
        "requiere_anos_continuos": continuos_requeridos,
        "requiere_anos_alternos": alternos_requeridos,
        "consolidacion_alcanzada": consolidado,
        "rango_grado_cuerpo_C1": "Niveles 15 a 20 (RD 369/1999)",
        "articulo": "Arts. 21-22 TREBEP + RD 364/1995 Art. 46"
    }


def calcular_remuneracion_licencia_enfermedad(salario_bruto_mensual: float = 2000.0,
                                              dia_baja: int = 1) -> Dict[str, Any]:
    """
    Arts. 49 y 93 TREBEP — Retribuciones durante IT/licencia por enfermedad.
    - Días 1-20: 80% de las retribuciones.
    - Día 21 en adelante: 100% de las retribuciones.
    (Mejora sobre el régimen general SS que aplica el TRLGSS).
    """
    if dia_baja <= 20:
        porcentaje = 0.80
        periodo = "Días 1-20: 80%"
    else:
        porcentaje = 1.00
        periodo = "Día 21+: 100%"
    importe_diario = (salario_bruto_mensual / 30) * porcentaje
    return {
        "salario_mensual": salario_bruto_mensual,
        "dia_de_baja": dia_baja,
        "porcentaje_aplicado": f"{int(porcentaje*100)}%",
        "periodo": periodo,
        "retribucion_diaria": round(importe_diario, 2),
        "retribucion_mensual_estimada": round(importe_diario * 30, 2),
        "articulo": "Arts. 49.b) y 93 TREBEP"
    }


def calcular_plazo_excedencia(tipo: str = "voluntaria", anos_servicio: int = 0) -> Dict[str, Any]:
    """
    Arts. 85-91 TREBEP — Excedencias de funcionarios.
    Tipos: voluntaria (mín 4 meses, máx 5 años),
    por cuidado hijos (máx 3 años), por cuidado familiar (máx 2 años),
    por razón de violencia (máx 6 meses prorrogable).
    """
    tipos = {
        "voluntaria": {"min_meses": 4, "max_anos": 5, "reserva_puesto": False, "requiere_anos": 2},
        "hijos": {"min_meses": 0, "max_anos": 3, "reserva_puesto": True, "requiere_anos": 0},
        "familiar": {"min_meses": 0, "max_anos": 2, "reserva_puesto": True, "requiere_anos": 0},
        "violencia_genero": {"min_meses": 0, "max_meses": 6, "reserva_puesto": True, "requiere_anos": 0, "prorrogable": True},
        "servicio_publico": {"min_meses": 0, "max_anos": None, "reserva_puesto": True, "requiere_anos": 0}
    }
    t = tipos.get(tipo.lower().replace(" ", "_"), tipos["voluntaria"])
    cumple_requisitos = anos_servicio >= t.get("requiere_anos", 0)
    return {
        "tipo_excedencia": tipo,
        "cumple_requisito_antiguedad": cumple_requisitos,
        "anos_servicio_requeridos": t.get("requiere_anos", 0),
        "duracion_minima_meses": t.get("min_meses", 0),
        "duracion_maxima_anos": t.get("max_anos", "Indefinida"),
        "reserva_puesto_trabajo": t.get("reserva_puesto", False),
        "computo_servicios": tipo in ["hijos", "familiar", "violencia_genero"],
        "articulo": "Arts. 85-91 TREBEP"
    }


def calcular_complemento_destino(nivel_puesto: int = 15, grupo: str = "C1") -> Dict[str, Any]:
    """
    Art. 25 TREBEP + RD 469/2000 — Complemento de destino.
    Cuantías anuales por nivel (vigentes 2026, 14 pagas).
    """
    # Cuantías anuales pactadas en Acuerdo Gobierno-Sindicatos (aproximadas 2026)
    cuantias_anuales = {
        12: 3887.64, 13: 4072.94, 14: 4270.48, 15: 4479.76,
        16: 4724.51, 17: 4969.15, 18: 5213.99, 19: 5482.36,
        20: 5764.81, 21: 6094.75, 22: 6432.16, 23: 6801.19,
        24: 7170.54, 25: 7572.46, 26: 8017.74, 27: 8463.27,
        28: 8932.05, 29: 9448.42, 30: 9988.75
    }
    importe_anual = cuantias_anuales.get(nivel_puesto, 4479.76)
    importe_mensual = importe_anual / 14  # 12 mensualidades + 2 pagas extras
    return {
        "nivel_puesto": nivel_puesto,
        "grupo": grupo,
        "complemento_destino_anual": round(importe_anual, 2),
        "complemento_destino_mensual": round(importe_mensual, 2),
        "num_pagas": 14,
        "articulo": "Art. 25 TREBEP + RD 469/2000"
    }


# ============================================================================
# BLOQUE C — TRANSVERSALES (Nuevas funciones Apéndice VII)
# ============================================================================

def calcular_plazo_brecha_rgpd(tipo_brecha: str = "alta") -> Dict[str, Any]:
    """
    Art. 33 RGPD (UE 2016/679) + Art. 37 LOPDGDD (Ley 3/2018).
    Notificación de brechas de seguridad a la AEPD:
    - Alta/media: 72 horas desde que se tiene conocimiento.
    - Brecha con riesgo: Notificar también a los interesados SIN dilación INDEBIDA.
    """
    tipos = {
        "alta": {"horas_aepd": 72, "notificar_interesados": True, "tramite_aepd": "Obligatorio"},
        "media": {"horas_aepd": 72, "notificar_interesados": False, "tramite_aepd": "Obligatorio"},
        "baja": {"horas_aepd": None, "notificar_interesados": False, "tramite_aepd": "Solo registro interno"}
    }
    t = tipos.get(tipo_brecha.lower(), tipos["alta"])
    return {
        "tipo_brecha": tipo_brecha,
        "plazo_notificacion_aepd_horas": t["horas_aepd"],
        "notificar_interesados": t["notificar_interesados"],
        "tramite_aepd": t["tramite_aepd"],
        "registro_actividades": "Obligatorio siempre (Art. 30 RGPD)",
        "dpo_obligatorio": "Sí para Administraciones Públicas (Art. 37 RGPD)",
        "articulo": "Arts. 33-34 RGPD + Arts. 37-38 LOPDGDD (LO 3/2018)"
    }


def verificar_umbral_contrato(importe_euros: float = 0, tipo_contrato: str = "suministros") -> Dict[str, Any]:
    """
    Arts. 4, 131 y 316 LCSP (Ley 9/2017) — Umbrales de contratación pública.
    Umbrales para contrato menor (sin licitación) 2026:
    - Obras: < 40.000€
    - Suministros/Servicios: < 15.000€
    Umbrales armonizados UE (DOUE): Obras 5.382.000€, Servicios/Suministros 221.000€.
    """
    umbrales_menor = {"obras": 40000, "suministros": 15000, "servicios": 15000}
    umbrales_arm = {"obras": 5382000, "suministros": 221000, "servicios": 221000}
    menor = umbrales_menor.get(tipo_contrato.lower(), 15000)
    arm = umbrales_arm.get(tipo_contrato.lower(), 221000)
    es_menor = importe_euros < menor
    es_armonizado = importe_euros >= arm
    return {
        "importe": importe_euros,
        "tipo_contrato": tipo_contrato,
        "es_contrato_menor": es_menor,
        "es_contrato_armonizado": es_armonizado,
        "umbral_contrato_menor": menor,
        "umbral_armonizado_ue": arm,
        "procedimiento_requerido": (
            "Contrato menor (sin licitación)" if es_menor
            else ("Licitación abierta armonizada (DOUE)" if es_armonizado
                  else "Procedimiento abierto simplificado")
        ),
        "articulo": "Arts. 4, 131 y 316 LCSP (Ley 9/2017) + Reglamento UE 2020/1081"
    }


def calcular_plazo_acceso_informacion(tipo_solicitud: str = "estimacion") -> Dict[str, Any]:
    """
    Arts. 14-22 Ley 19/2013 de Transparencia, Acceso a la Información y Buen Gobierno.
    Plazo máximo de resolución: 1 mes, prorrogable 1 mes más.
    Silencio: DESESTIMATORIO (salvo norma especial).
    """
    return {
        "tipo_solicitud": tipo_solicitud,
        "plazo_resolucion_dias": 30,
        "prorroga_posible_dias": 30,
        "plazo_total_max_dias": 60,
        "silencio_administrativo": "Desestimatorio",
        "recurso_silencio": "Reclamación ante Consejo de Transparencia y Buen Gobierno (CTBG)",
        "plazo_reclamacion_ctbg_dias": 30,
        "plazo_recurso_contencioso": "2 meses desde notificación o silencio",
        "articulo": "Arts. 17-22 Ley 19/2013 de Transparencia"
    }


def verificar_plazo_max_procedimiento(tipo_procedimiento: str = "general",
                                      meses_transcurridos: int = 0) -> Dict[str, Any]:
    """
    Arts. 21-25 Ley 39/2015 — Plazo máximo de resolución (por defecto 3 meses).
    Efectos del transcurso del plazo (caducidad vs silencio):
    - Iniciados de oficio efectos desfavorables: CADUCIDAD.
    - Iniciados de oficio efectos favorables: SILENCIO DESESTIMATORIO.
    - Iniciados a instancia: SILENCIO (positivo/negativo según norma).
    """
    plazos = {
        "general": 3,              # meses
        "sancionador": 6,
        "tributario": 6,
        "obra": 3,
        "licencia_actividad": 3,
        "recurso_alzada": 3,
        "recurso_reposicion": 1,
    }
    plazo_max = plazos.get(tipo_procedimiento.lower(), 3)
    superado = meses_transcurridos > plazo_max
    return {
        "tipo_procedimiento": tipo_procedimiento,
        "plazo_max_meses": plazo_max,
        "meses_transcurridos": meses_transcurridos,
        "plazo_superado": superado,
        "efecto_si_oficio_desfavorable": "Caducidad (Art. 25.1.b LPAC)",
        "efecto_si_instancia": "Silencio administrativo (Art. 24 LPAC)",
        "responsabilidad_funcionario": "Posible responsabilidad disciplinaria (Art. 20 LPAC)",
        "articulo": "Arts. 21-25 Ley 39/2015 (LPAC)"
    }


def verificar_obligacion_electronica(tipo_sujeto: str = "persona_juridica") -> Dict[str, Any]:
    """
    Art. 14 Ley 39/2015 — Obligación de relacionarse electrónicamente con la AP.
    Sujetos OBLIGADOS: personas jurídicas, entidades sin personalidad jurídica,
    quienes ejerzan actividad profesional con colegiación obligatoria,
    empleados de las AAPP para trámites con su empleadora.
    """
    obligados = ["persona_juridica", "entidad_sin_personalidad", "profesional_colegiado",
                 "empleado_publico", "representante"]
    voluntario = ["persona_fisica"]
    es_obligado = tipo_sujeto.lower().replace(" ", "_") in obligados
    return {
        "tipo_sujeto": tipo_sujeto,
        "obligacion_electronica": es_obligado,
        "fundamento": "Obligado por Art. 14.2 LPAC" if es_obligado else "Opcional (Art. 14.1 LPAC)",
        "canal_preferente": "Sede electrónica + cl@ve",
        "excepciones": "Circunstancias extraordinarias acreditadas que impidan acceso electrónico (Art. 14.3)",
        "articulo": "Art. 14 Ley 39/2015 (LPAC)"
    }


# Dispatcher interno para AGE (COMPLETO — 32 funciones)

# =============================================================================
# BLOQUE II: RETRIBUCIONES E NÓMINAS (Añadido 05/03/2026)
# Fuentes: TREBEP art. 22-25, LPGEx vigente, RD 462/2002 Dietas,
#          RD 2064/1995 cotización RG
# =============================================================================

# Sueldos base 2026 (LPGEx) — €/mes × 14 pagas
SUELDO_BASE_2026 = {
    "A1": Decimal("1045.49"),
    "A2": Decimal("864.14"),
    "C1": Decimal("718.85"),
    "C2": Decimal("658.25"),
    "E":  Decimal("611.56"),
}

# Trienios 2026 (€/mes por trienio) — TREBEP art. 23 + Ley PGE
TRIENIOS_2026 = {
    "A1": Decimal("50.07"),
    "A2": Decimal("40.64"),
    "C1": Decimal("30.61"),
    "C2": Decimal("20.84"),
    "E":  Decimal("15.68"),
}

# Dietas (RD 462/2002) — actualizado con valores vigentes
DIETAS_GRUPO1 = {"dieta_completa": Decimal("91.35"), "media_dieta": Decimal("45.70")}
DIETAS_GRUPO2 = {"dieta_completa": Decimal("53.34"), "media_dieta": Decimal("26.67")}
KM_COCHE = Decimal("0.26")  # €/km (RD 462/2002 + actualización)

# Tipos cotización SS (Régimen General 2026) — RD 2064/1995
COTIZACION_CC_TRAB   = Decimal("0.0470")  # CC trabajador
COTIZACION_DESEMP    = Decimal("0.0155")  # Desempleo indefinido
COTIZACION_FP        = Decimal("0.0010")  # Formación Profesional
COTIZACION_CC_EMP    = Decimal("0.2360")  # Cuota empresa

# Umbrales contratación pública LCSP (Regl. Delegado UE 2023/2496, vigente 2026)
UMBRAL_UE_OBRAS       = Decimal("5_382_000")
UMBRAL_UE_SUMINISTROS = Decimal("221_000")
UMBRAL_UE_SERVICIOS   = Decimal("221_000")
UMBRAL_CONTRATO_MENOR_OBRAS = Decimal("40_000")
UMBRAL_CONTRATO_MENOR_RESTO = Decimal("15_000")


def calcular_nomina_mensual(
    subgrupo: str,
    nivel_cd: int,
    ce_mensual: float,
    trienios: int = 0,
    irpf_pct: float = 15.0,
    incluir_ss_empresa: bool = False,
) -> Dict[str, Any]:
    """
    Calcula nómina mensual completa de funcionario AGE.

    Retribuciones brutas = Sueldo base + Trienios + Complemento Destino + Complemento Específico
    Descuentos = IRPF + SS trabajador (CC 4,70% + Desempleo 1,55% + FP 0,10%)
    
    Args:
        subgrupo: A1/A2/C1/C2/E
        nivel_cd: Nivel complemento de destino (1–30)
        ce_mensual: Complemento específico mensual en €
        trienios: Número de trienios reconocidos
        irpf_pct: Porcentaje de retención IRPF
        incluir_ss_empresa: Si True, muestra también el coste empresa (CC 23,60%)
    
    Fuentes: TREBEP art. 22-23, Orden 30/07/1992 nóminas, TRLGSS art. 147
    """
    subgrupo = subgrupo.upper()
    if subgrupo not in SUELDO_BASE_2026:
        return {"error": f"Subgrupo '{subgrupo}' no válido. Usa: A1/A2/C1/C2/E"}

    # --- RETRIBUCIONES BRUTAS ---
    sueldo_base = SUELDO_BASE_2026[subgrupo]
    importe_trienios = TRIENIOS_2026[subgrupo] * D(trienios)

    # Complemento de Destino: calculamos el valor mensual real por nivel
    # NOTA: el CD real lo fija la LPGEx. Usamos el mismo método que calcular_complemento_destino()
    valor_cd_mensual = calcular_complemento_destino(nivel_cd).get("valor_mensual_euros", D("0"))
    if isinstance(valor_cd_mensual, str):
        valor_cd_mensual = D("0")
    cd = D(str(valor_cd_mensual))

    ce = D(str(ce_mensual))
    bruto_total = sueldo_base + importe_trienios + cd + ce

    # --- BASE COTIZACIÓN SS (misma que retrib. básicas + trienios; CE se excluye si < tope) ---
    base_cotizacion = bruto_total  # Simplificación: BC = retrib. brutas mensual

    # --- DESCUENTOS ---
    irpf   = R2(bruto_total * D(str(irpf_pct)) / D("100"))
    ss_cc  = R2(base_cotizacion * COTIZACION_CC_TRAB)
    ss_des = R2(base_cotizacion * COTIZACION_DESEMP)
    ss_fp  = R2(base_cotizacion * COTIZACION_FP)
    total_ss = ss_cc + ss_des + ss_fp
    total_descuentos = irpf + total_ss
    neto = bruto_total - total_descuentos

    resultado = {
        "subgrupo": subgrupo,
        "nivel_cd": nivel_cd,
        "trienios_reconocidos": trienios,
        "retribuciones_brutas": {
            "sueldo_base": float(sueldo_base),
            "trienios": float(importe_trienios),
            "complemento_destino": float(cd),
            "complemento_especifico": float(ce),
            "TOTAL_BRUTO": float(bruto_total),
        },
        "descuentos": {
            "IRPF": {"pct": irpf_pct, "importe": float(irpf)},
            "SS_CC_trabajador": {"pct": 4.70, "importe": float(ss_cc)},
            "SS_desempleo": {"pct": 1.55, "importe": float(ss_des)},
            "SS_FP": {"pct": 0.10, "importe": float(ss_fp)},
            "TOTAL_descuentos": float(total_descuentos),
        },
        "NETO_A_PERCIBIR": float(neto),
        "articulos": "Art. 22-23 TREBEP | Orden 30/07/1992 | TRLGSS art. 147",
    }

    if incluir_ss_empresa:
        ss_empresa = R2(base_cotizacion * COTIZACION_CC_EMP)
        resultado["coste_empresa"] = {
            "SS_empresa_CC": float(ss_empresa),
            "coste_total": float(bruto_total + ss_empresa),
            "nota": "CC empresa 23,60% + 1,55% desempleo emp. + más recargos FOGASA/MEP",
        }

    return resultado


def calcular_pagas_extra(
    subgrupo: str,
    nivel_cd: int,
    ce_mensual: float = 0.0,
) -> Dict[str, Any]:
    """
    Calcula las 2 pagas extraordinarias anuales (junio y diciembre).
    
    Importe paga extra = Sueldo base mensual + Complemento Destino mensual.
    El CE NO se incluye salvo que el Convenio/RPT lo reconozca (art. 22.4 TREBEP).
    
    Fuente: Art. 22.4 TREBEP
    """
    subgrupo = subgrupo.upper()
    if subgrupo not in SUELDO_BASE_2026:
        return {"error": f"Subgrupo '{subgrupo}' no válido"}

    sueldo_base = SUELDO_BASE_2026[subgrupo]
    cd_info = calcular_complemento_destino(nivel_cd)
    cd = D(str(cd_info.get("valor_mensual_euros", 0)))

    importe_paga = R2(sueldo_base + cd)
    total_anual_pagas = R2(importe_paga * D("2"))

    return {
        "subgrupo": subgrupo,
        "importe_paga_extra": float(importe_paga),
        "composicion": {
            "sueldo_base_mensual": float(sueldo_base),
            "complemento_destino": float(cd),
            "nota_CE": "CE NO incluido en paga extra salvo reconocimiento específico (art. 22.4 TREBEP)",
        },
        "total_anual_2_pagas": float(total_anual_pagas),
        "fechas": "Junio (con nómina junio) y Diciembre (con nómina diciembre)",
        "articulo": "Art. 22.4 TREBEP",
    }


def calcular_indemnizacion_dietas(
    grupo: int,
    dias_completos: int = 0,
    medias_dietas: int = 0,
    km: float = 0.0,
) -> Dict[str, Any]:
    """
    Calcula indemnizaciones por razón de servicio (desplazamientos).
    
    Grupo 1: Personal A1/A2/cargos directivos
    Grupo 2: Personal C1/C2/E y demás
    
    Fuente: RD 462/2002, actualización DGF 2023
    """
    if grupo not in (1, 2):
        return {"error": "grupo debe ser 1 ó 2"}

    tarifas = DIETAS_GRUPO1 if grupo == 1 else DIETAS_GRUPO2
    importe_dietas_completas = R2(D(str(dias_completos)) * tarifas["dieta_completa"])
    importe_medias_dietas    = R2(D(str(medias_dietas)) * tarifas["media_dieta"])
    importe_km               = R2(D(str(km)) * KM_COCHE)
    total = importe_dietas_completas + importe_medias_dietas + importe_km

    return {
        "grupo": grupo,
        "dieta_completa_unitaria": float(tarifas["dieta_completa"]),
        "media_dieta_unitaria": float(tarifas["media_dieta"]),
        "km_unitario": float(KM_COCHE),
        "calculo": {
            "dias_completos": dias_completos,
            "importe_dietas": float(importe_dietas_completas),
            "medias_dietas": medias_dietas,
            "importe_medias": float(importe_medias_dietas),
            "km_recorridos": km,
            "importe_km": float(importe_km),
        },
        "TOTAL_INDEMNIZACION": float(total),
        "articulo": "RD 462/2002 indemnizaciones razón servicio",
    }


# =============================================================================
# BLOQUE III: CONTRATACIÓN PÚBLICA — LCSP Ley 9/2017 (Añadido 05/03/2026)
# =============================================================================

def calcular_vec(
    importe_anual_sin_iva: float,
    anos_duracion: float,
    anos_prorroga: float = 0.0,
    pct_modificaciones: float = 0.0,
) -> Dict[str, Any]:
    """
    Calcula el Valor Estimado del Contrato (VEC) — Art. 101 LCSP.
    
    VEC = Importe anual × (duración + prórrogas) × (1 + % modificaciones)
    NO incluye IVA. NO incluye opciones no previstas.
    
    Fuente: Art. 101 Ley 9/2017 LCSP
    """
    importe = D(str(importe_anual_sin_iva))
    duracion_total = D(str(anos_duracion)) + D(str(anos_prorroga))
    factor_mod = D("1") + D(str(pct_modificaciones)) / D("100")

    vec = R2(importe * duracion_total * factor_mod)

    # Determinar procedimiento y publicidad
    if vec > UMBRAL_UE_OBRAS:
        procedimiento = "Regulación Armonizada — publicación DOUE obligatoria"
        umbral_ref = "Obras > 5.382.000 €"
    elif vec > UMBRAL_CONTRATO_MENOR_OBRAS:
        procedimiento = "Procedimiento Abierto / Negociado sin publicidad"
        umbral_ref = f"Obras entre {float(UMBRAL_CONTRATO_MENOR_OBRAS):,.0f} € y {float(UMBRAL_UE_OBRAS):,.0f} €"
    elif vec > UMBRAL_UE_SUMINISTROS:
        procedimiento = "Regulación Armonizada — publicación DOUE"
        umbral_ref = "Suministros/Servicios > 221.000 €"
    else:
        procedimiento = "Sin publicidad comunitaria obligatoria"
        umbral_ref = "Por debajo de umbral UE"

    return {
        "importe_anual_sin_iva": importe_anual_sin_iva,
        "anos_duracion": anos_duracion,
        "anos_prorroga": anos_prorroga,
        "pct_modificaciones": pct_modificaciones,
        "duracion_total_anos": float(duracion_total),
        "VEC": float(vec),
        "VEC_formatted": f"{float(vec):,.2f} €",
        "procedimiento_aplicable": procedimiento,
        "umbral_referencia": umbral_ref,
        "NOTA_IVA": "El VEC NO incluye IVA — art. 101.3 LCSP",
        "articulo": "Art. 101 Ley 9/2017 LCSP",
    }


def calcular_pbl(
    costes_directos: float,
    costes_indirectos: float,
    beneficio_industrial_pct: float = 6.0,
    iva_pct: float = 21.0,
) -> Dict[str, Any]:
    """
    Calcula el Presupuesto Base de Licitación (PBL) — Art. 100 LCSP.
    
    PBL = (Costes directos + Costes indirectos) × (1 + BI%) × (1 + IVA%)
    
    Fuente: Art. 100 Ley 9/2017 LCSP
    """
    cd = D(str(costes_directos))
    ci = D(str(costes_indirectos))
    bi_pct = D(str(beneficio_industrial_pct)) / D("100")
    iv_pct = D(str(iva_pct)) / D("100")

    base = cd + ci
    bi   = R2(base * bi_pct)
    pbl_sin_iva = R2(base + bi)
    iva_importe = R2(pbl_sin_iva * iv_pct)
    pbl_con_iva = R2(pbl_sin_iva + iva_importe)

    return {
        "costes_directos": costes_directos,
        "costes_indirectos": costes_indirectos,
        "beneficio_industrial_pct": beneficio_industrial_pct,
        "beneficio_industrial_importe": float(bi),
        "PBL_sin_IVA": float(pbl_sin_iva),
        "IVA_pct": iva_pct,
        "IVA_importe": float(iva_importe),
        "PBL_CON_IVA": float(pbl_con_iva),
        "nota": "El tipo de obra/servicio determina si aplica IVA 21%/10%/4%",
        "articulo": "Art. 100 Ley 9/2017 LCSP",
    }


def calcular_garantia_contrato(
    pbl_sin_iva: float,
    tipo: str = "definitiva",
) -> Dict[str, Any]:
    """
    Calcula garantías provisionales y definitivas — Arts. 106-107 LCSP.
    
    - Garantía definitiva: 5% del PBL sin IVA (obligatoria, salvo excepciones)
    - Garantía complementaria: hasta 5% adicional (max 10% total)
    - Garantía provisional: máx 3% del VEC (potestativa, casi en desuso)
    
    Fuente: Arts. 106-107 Ley 9/2017 LCSP
    """
    pbl = D(str(pbl_sin_iva))

    if tipo == "definitiva":
        pct = D("0.05")
        importe = R2(pbl * pct)
        return {
            "tipo": "Garantía DEFINITIVA",
            "base": float(pbl),
            "pct": "5%",
            "importe": float(importe),
            "plazo_devolución": "Al término del contrato y transcurrido el plazo de garantía",
            "forma": "Aval bancario / Seguro de caución / Retención de precio / Depósito en Caja General",
            "articulo": "Art. 107 Ley 9/2017 LCSP",
        }
    elif tipo == "complementaria":
        pct = D("0.05")
        importe = R2(pbl * pct)
        total_max = R2(pbl * D("0.10"))
        return {
            "tipo": "Garantía COMPLEMENTARIA",
            "base": float(pbl),
            "pct": "hasta 5% adicional",
            "importe_max": float(importe),
            "total_maximo_con_definitiva": float(total_max),
            "articulo": "Art. 107.1 Ley 9/2017 LCSP",
        }
    elif tipo == "provisional":
        pct = D("0.03")  # máximo 3% del VEC
        importe = R2(pbl * pct)
        return {
            "tipo": "Garantía PROVISIONAL (potestativa)",
            "base": float(pbl),
            "pct_max": "3% del VEC",
            "importe_estimado": float(importe),
            "nota": "Casi en desuso desde LCSP 2017; solo para contratos de obra de especial complejidad",
            "articulo": "Art. 106 Ley 9/2017 LCSP",
        }
    else:
        return {"error": "tipo debe ser 'definitiva', 'complementaria' o 'provisional'"}


def clasificar_contrato_lcsp(
    vec: float,
    tipo_objeto: str = "servicios",
) -> Dict[str, Any]:
    """
    Clasifica el tipo de contrato y procedimiento según VEC y objeto.
    
    tipo_objeto: 'obras' | 'servicios' | 'suministros'
    
    Fuente: Arts. 118, 131, 159 Ley 9/2017 LCSP
    """
    vec_d = D(str(vec))
    obj = tipo_objeto.lower()

    if obj == "obras":
        if vec_d <= UMBRAL_CONTRATO_MENOR_OBRAS:
            tipo = "CONTRATO MENOR (Obras ≤ 40.000 €)"
            procedimiento = "Directo, sin publicidad ni concurrencia"
            art = "Art. 118 LCSP"
        elif vec_d <= UMBRAL_UE_OBRAS:
            tipo = "Contrato ordinario sin regulación armonizada"
            procedimiento = "Abierto, restringido o negociado s/publicidad según cuantía"
            art = "Art. 131 LCSP"
        else:
            tipo = "SUJETO A REGULACIÓN ARMONIZADA — publicación DOUE"
            procedimiento = "Abierto o Restringido (obligatorio); anuncio en DOUE"
            art = "Art. 20 LCSP + Regl. UE 2023/2496"
    else:  # servicios / suministros
        if vec_d <= UMBRAL_CONTRATO_MENOR_RESTO:
            tipo = "CONTRATO MENOR (Servicios/Suministros ≤ 15.000 €)"
            procedimiento = "Directo, sin publicidad ni concurrencia"
            art = "Art. 118 LCSP"
        elif vec_d <= UMBRAL_UE_SERVICIOS:
            tipo = "Contrato ordinario sin regulación armonizada"
            procedimiento = "Simplificado o Abierto según cuantía"
            art = "Art. 131 / 159 LCSP"
        else:
            tipo = "SUJETO A REGULACIÓN ARMONIZADA — publicación DOUE"
            procedimiento = "Abierto (obligatorio); anuncio previo en DOUE"
            art = "Art. 22 LCSP + Regl. UE 2023/2496"

    return {
        "VEC": float(vec_d),
        "objeto": obj,
        "tipo_contrato": tipo,
        "procedimiento": procedimiento,
        "umbral_obras_UE": float(UMBRAL_UE_OBRAS),
        "umbral_SS_UE": float(UMBRAL_UE_SUMINISTROS),
        "umbral_menor_obras": float(UMBRAL_CONTRATO_MENOR_OBRAS),
        "umbral_menor_resto": float(UMBRAL_CONTRATO_MENOR_RESTO),
        "articulo": art,
    }


TOOLS_AGE = {
    # Bloque A — Ley 39/2015 (LPAC)
    "calcular_plazo_alzada": calcular_plazo_alzada,
    "calcular_plazo_reposicion": calcular_plazo_reposicion,
    "calcular_silencio_administrativo": calcular_silencio_administrativo,
    "tipo_computo_plazo": tipo_computo_plazo,
    "calcular_prescripcion_disciplinaria": calcular_prescripcion_disciplinaria,
    "calcular_fecha_vencimiento": calcular_fecha_vencimiento,
    "calcular_plazo_extraordinario_revision": calcular_plazo_extraordinario_revision,
    "calcular_abstencion_recusacion": calcular_abstencion_recusacion,
    "calcular_subsanacion": calcular_subsanacion,
    "calcular_intentos_notificacion": calcular_intentos_notificacion,
    "calcular_ejecutividad_suspension": calcular_ejecutividad_suspension,
    "calcular_responsabilidad_patrimonial": calcular_responsabilidad_patrimonial,
    "calcular_revision_oficio": calcular_revision_oficio,
    "calcular_caducidad_procedimiento": calcular_caducidad_procedimiento,
    "calcular_rectificacion_errores": calcular_rectificacion_errores,
    "calcular_tramite_audiencia": calcular_tramite_audiencia,
    "calcular_informes": calcular_informes,
    "calcular_medidas_provisionales": calcular_medidas_provisionales,
    "calcular_desistimiento_renuncia": calcular_desistimiento_renuncia,
    "calcular_identificacion_firma": calcular_identificacion_firma,
    "verificar_plazo_max_procedimiento": verificar_plazo_max_procedimiento,
    "verificar_obligacion_electronica": verificar_obligacion_electronica,
    # Bloque B — TREBEP
    "calcular_vacaciones_trebep": calcular_vacaciones_trebep,
    "calcular_asuntos_propios_trebep": calcular_asuntos_propios_trebep,
    "calcular_trienios": calcular_trienios,
    "calcular_grado_personal": calcular_grado_personal,
    "calcular_remuneracion_licencia_enfermedad": calcular_remuneracion_licencia_enfermedad,
    "calcular_plazo_excedencia": calcular_plazo_excedencia,
    "calcular_complemento_destino": calcular_complemento_destino,
    # Bloque C — Transversales
    "calcular_plazo_brecha_rgpd": calcular_plazo_brecha_rgpd,
    "verificar_umbral_contrato": verificar_umbral_contrato,
    "calcular_plazo_acceso_informacion": calcular_plazo_acceso_informacion,
    # Bloque D — Retribuciones y Nóminas (05/03/2026)
    "calcular_nomina_mensual": calcular_nomina_mensual,
    "calcular_pagas_extra": calcular_pagas_extra,
    "calcular_indemnizacion_dietas": calcular_indemnizacion_dietas,
    # Bloque E — Contratación Pública LCSP (05/03/2026)
    "calcular_vec": calcular_vec,
    "calcular_pbl": calcular_pbl,
    "calcular_garantia_contrato": calcular_garantia_contrato,
    "clasificar_contrato_lcsp": clasificar_contrato_lcsp,
}

def ejecutar_calculo_age(nombre_tool: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if nombre_tool not in TOOLS_AGE:
        return {"error": f"Herramienta AGE '{nombre_tool}' no encontrada"}
    
    import inspect
    func = TOOLS_AGE[nombre_tool]
    sig = inspect.signature(func)
    
    # Filtrar solo los parámetros que la función acepta
    # Mapear fecha_inicio -> fecha_notificacion si la función lo espera
    p = (params or {}).copy()
    if "fecha_inicio" in p and "fecha_notificacion" in sig.parameters:
        p["fecha_notificacion"] = p["fecha_inicio"]

    filtered_params = {
        k: v for k, v in p.items() 
        if k in sig.parameters
    }
    
    try:
        return func(**filtered_params)
    except Exception as e:
        return {"error": f"Error ejecutando {nombre_tool}: {str(e)}"}
