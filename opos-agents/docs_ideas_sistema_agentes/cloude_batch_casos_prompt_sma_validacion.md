"""
SISTEMA DE GENERACIÓN DE DATASET PERFECTO
Usa este script para generar 50 casos con Claude Batch API
"""

import anthropic
import json
from datetime import datetime

client = anthropic.Anthropic(api_key="tu_api_key_aqui")

# ============================================================================
# PROMPT MAESTRO PARA CLAUDE
# ============================================================================

SYSTEM_PROMPT = """Eres un preparador experto de oposiciones de Seguridad Social y AGE en España con 20 años de experiencia. Tu especialidad es crear casos prácticos tipo examen oficial que:

1. Enseñen razonamiento jurídico profundo (no solo memorización)
2. Incluyan trampas realistas como en los examentes oficiakles que confundan los opositores
3. TUS casos estén 100% verificados con la normativa del BOE
4. Sigan un formato estructurado de máxima calidad didáctica y estricta informacion contrastada y real 

REGLAS ESTRICTAS:
- NUNCA inventes artículos, conceptos, fechas , cantidades o leyes
- SIEMPRE cita el BOE con URL verificada
- Fechas ESPECÍFICAS (dd/mm/aaaa), no genéricas
- Cantidades EXACTAS (años, meses, euros)
- Sin contradicciones internas
- Razonamiento paso a paso completo
- distinges siempre dias habiles y naturales, validas y usas las formulas correctas cuando es necesario
- aplicas correctamente salario y cotizacion, porcentajes reales y bases imponibles, reguladoras etc. detalles importantes
-siempre usas la posicion de la respuesta correcta equilibradamente, por ej. a-25% b-25% c-25% y d-25%
"""

USER_PROMPT_TEMPLATE = """Genera un caso práctico de oposición siguiendo EXACTAMENTE este formato JSON:

TEMA: {tema}
MATERIA: {materia}
DIFICULTAD: {dificultad}
TIPO DE TRAMPA: {tipo_trampa}

FORMATO OBLIGATORIO:
{{
  "id": "{categoria}_{subtema}_{numero}",
  "categoria": "{categoria_completa}",
  "subcategoria": "{subcategoria_especifica}",
  "dificultad": "{nivel_dificultad}",
  "tipo_trampa": "{nombre_descriptivo_trampa}",
  "fuente": "Caso creado basado en {normativa_base}",
  "fecha_creacion": "{fecha_hoy}",
  
  "enunciado": "REDACTA UN CASO COMPLETO con:
    - Contexto personal (nombre, edad, situación laboral)
    - Fechas ESPECÍFICAS (ej: 15 de marzo de 2025)
    - Cantidades EXACTAS (ej: 22 años 6 meses y 3 dias cotizados, 1.800€)
    - Hechos cronológicos ordenados
    - Pregunta final clara
    
    REQUISITOS:
    - Mínimo 150 palabras
    - Sin ambigüedades
    - Sin contradicciones
    - Datos suficientes para resolver",
  
  "opciones": {{
    "a": "Opción con trampa común tipo 1 (confusión de requisitos)",
    "b": "Opción con trampa común tipo 2 (aplicación incorrecta norma)",
    "c": "Respuesta CORRECTA (debe ser la más difícil de identificar)",
    "d": "Distractor obvio (error fácil de descartar)"
  }},
  
  "respuesta_correcta": "c",
  
  "razonamiento_completo": {{
    "paso_1_identificacion_cuestion": "¿Cuál es la pregunta jurídica específica que debemos responder?",
    
    "paso_2_marco_normativo": [
      "Art. X de Ley Y (cita EXACTA)",
      "Art. Z de RD W (cita EXACTA)"
    ],
    
    "paso_3_analisis_hechos_relevantes": {{
      "dato_clave_1": "Valor o situación",
      "dato_clave_2": "Valor o situación",
      "dato_clave_3": "Valor o situación"
    }},
    
    "paso_4_subsuncion_juridica": {{
      "norma_general": "Explicación de la regla general aplicable",
      "excepcion_si_aplica": "Explicación de excepciones relevantes",
      "aplicacion_al_caso": "Cómo se aplica la norma a los hechos concretos"
    }},
    
    "paso_5_descarte_opciones_incorrectas": {{
      "opcion_a": {{
        "error": "Descripción del error jurídico",
        "por_que_seduce": "Razón psicológica por la que se marca"
      }},
      "opcion_b": {{
        "error": "Descripción del error jurídico",
        "por_que_seduce": "Razón psicológica por la que se marca"
      }},
      "opcion_d": {{
        "error": "Descripción del error jurídico",
        "por_que_seduce": "Razón psicológica por la que se marca"
      }}
    }},
    
    "paso_6_conclusion_fundamentada": "Explicación completa y clara de por qué la opción correcta es la c, integrando todos los pasos anteriores."
  }},
  
  "trampa_pedagogica": {{
    "tipo": "Clasificación técnica de la trampa (ej: confusion_grados_ip)",
    "explicacion": "Explicación detallada de por qué el opositor marca la opción incorrecta (mínimo 100 palabras)",
    "concepto_clave": "Concepto fundamental que debe dominar para evitar el error",
    "como_evitarla": "Técnica mnemotécnica o regla práctica para recordar"
  }},
  
  "normativa_verificada": [
    {{
      "norma": "Nombre completo oficial de la ley",
      "articulo": "Número exacto del artículo",
      "texto_literal": "Fragmento literal del artículo (mínimo 50 palabras)",
      "url_boe": "https://www.boe.es/buscar/act.php?id=BOE-A-YYYY-XXXXX#aXXX",
      "fecha_verificacion": "{fecha_hoy}",
      "status_url": "✅ Verificada"
    }}
  ],
  
  "metadata_calidad": {{
    "validado_por": "Claude Sonnet 4",
    "precision_tecnica": 0.98,
    "claridad_enunciado": 0.95,
    "utilidad_didactica": 0.97,
    "nivel_confianza_respuesta": 0.99
  }}
}}

IMPORTANTE:
1. Responde SOLO con el JSON válido, sin texto adicional y en formato correcto
2. URLs del BOE deben ser reales y verificables
3. Citas textuales de artículos deben ser LITERALES
4. El razonamiento legal explicativo debe ser completo y educativo
5. La trampa debe ser realista (basada en errores reales de opositores)
"""

# ============================================================================
# CASOS A GENERAR (50 casos distribuidos)
# ============================================================================

CASOS_DISTRIBUCIÓN = [
    # SEGURIDAD SOCIAL (30 casos = 60%)
    
    # Incapacidad Permanente (8 casos)
    {"tema": "Incapacidad Permanente Total", "materia": "Seguridad Social", "dificultad": "alta", 
     "tipo_trampa": "confusion_requisitos_alta_vs_no_alta", "categoria": "SS", "subtema": "IPT", "numero": "001"},
    {"tema": "Incapacidad Permanente Absoluta", "materia": "Seguridad Social", "dificultad": "media",
     "tipo_trampa": "confusion_grados_ip", "categoria": "SS", "subtema": "IPA", "numero": "002"},
    {"tema": "Gran Invalidez", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "requisito_tercera_persona", "categoria": "SS", "subtema": "GI", "numero": "003"},
    {"tema": "Revisión de grado IP", "materia": "Seguridad Social", "dificultad": "muy_alta",
     "tipo_trampa": "plazos_revision_mejoria", "categoria": "SS", "subtema": "REV_IP", "numero": "004"},
    {"tema": "IP derivada de IT", "materia": "Seguridad Social", "dificultad": "media",
     "tipo_trampa": "calculo_base_reguladora", "categoria": "SS", "subtema": "IP_IT", "numero": "005"},
    {"tema": "IP por accidente no laboral", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "periodo_carencia_contingencia_comun", "categoria": "SS", "subtema": "IP_CNL", "numero": "006"},
    {"tema": "IP en situación asimilada alta", "materia": "Seguridad Social", "dificultad": "muy_alta",
     "tipo_trampa": "situaciones_asimiladas_especificas", "categoria": "SS", "subtema": "IP_ASIM", "numero": "007"},
    {"tema": "Compatibilidad IPT con trabajo", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "limites_compatibilidad_ipa", "categoria": "SS", "subtema": "COMPAT_IPT", "numero": "008"},
    
    # Jubilación (6 casos)
    {"tema": "Jubilación anticipada voluntaria", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "coeficientes_reductores_edad", "categoria": "SS", "subtema": "JUB_ANT", "numero": "009"},
    {"tema": "Jubilación anticipada involuntaria", "materia": "Seguridad Social", "dificultad": "media",
     "tipo_trampa": "diferencia_voluntaria_involuntaria", "categoria": "SS", "subtema": "JUB_ANTINV", "numero": "010"},
    {"tema": "Cálculo base reguladora jubilación", "materia": "Seguridad Social", "dificultad": "muy_alta",
     "tipo_trampa": "divisor_350_integracion_lagunas", "categoria": "SS", "subtema": "BR_JUB", "numero": "011"},
    {"tema": "Jubilación parcial", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "requisitos_contrato_relevo", "categoria": "SS", "subtema": "JUB_PARC", "numero": "012"},
    {"tema": "Complemento por maternidad", "materia": "Seguridad Social", "dificultad": "media",
     "tipo_trampa": "brecha_genero_vs_maternidad", "categoria": "SS", "subtema": "COMP_MAT", "numero": "013"},
    {"tema": "Jubilación activa", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "compatibilidad_trabajo_pension", "categoria": "SS", "subtema": "JUB_ACT", "numero": "014"},
    
    # Prestaciones contributivas (8 casos)
    {"tema": "Prestación por desempleo - Plazo solicitud", "materia": "Seguridad Social", "dificultad": "media",
     "tipo_trampa": "dias_habiles_vs_naturales", "categoria": "SS", "subtema": "DESEMP_PLAZO", "numero": "015"},
    {"tema": "Prestación por desempleo - Duración", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "tabla_cotizacion_duracion", "categoria": "SS", "subtema": "DESEMP_DUR", "numero": "016"},
    {"tema": "Desempleo - Suspensión vs extinción", "materia": "Seguridad Social", "dificultad": "media",
     "tipo_trampa": "causas_suspension_derecho", "categoria": "SS", "subtema": "DESEMP_SUSP", "numero": "017"},
    {"tema": "Incapacidad Temporal - Contingencia profesional", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "porcentajes_it_profesional", "categoria": "SS", "subtema": "IT_PROF", "numero": "018"},
    {"tema": "IT - Duración máxima y prórrogas", "materia": "Seguridad Social", "dificultad": "muy_alta",
     "tipo_trampa": "365_180_plazos", "categoria": "SS", "subtema": "IT_DUR", "numero": "019"},
    {"tema": "Maternidad - Permisos y prestaciones", "materia": "Seguridad Social", "dificultad": "media",
     "tipo_trampa": "semanas_obligatorias_vs_opcionales", "categoria": "SS", "subtema": "MAT", "numero": "020"},
    {"tema": "Riesgo durante embarazo", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "diferencia_maternidad_riesgo", "categoria": "SS", "subtema": "RIESGO_EMB", "numero": "021"},
    {"tema": "Muerte y supervivencia - Viudedad", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "requisitos_union_hecho", "categoria": "SS", "subtema": "VIUD", "numero": "022"},
    
    # Cotización y afiliación (4 casos)
    {"tema": "Obligación de cotizar", "materia": "Seguridad Social", "dificultad": "media",
     "tipo_trampa": "bases_minimas_maximas", "categoria": "SS", "subtema": "COT_OBLIG", "numero": "023"},
    {"tema": "Pluriactividad", "materia": "Seguridad Social", "dificultad": "muy_alta",
     "tipo_trampa": "cotizacion_simultanea_regimenes", "categoria": "SS", "subtema": "PLURAL", "numero": "024"},
    {"tema": "Afiliación de extranjeros", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "requisitos_trabajadores_ue_vs_terceros", "categoria": "SS", "subtema": "AFIL_EXTR", "numero": "025"},
    {"tema": "Trabajadores autónomos RETA", "materia": "Seguridad Social", "dificultad": "media",
     "tipo_trampa": "obligacion_alta_reta", "categoria": "SS", "subtema": "RETA", "numero": "026"},
    
    # Procedimiento SS (4 casos)
    {"tema": "Silencio administrativo en SS", "materia": "Seguridad Social", "dificultad": "muy_alta",
     "tipo_trampa": "silencio_negativo_vs_lpac", "categoria": "SS", "subtema": "SILENC_SS", "numero": "027"},
    {"tema": "Recursos en vía administrativa SS", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "plazos_recurso_reposicion_previo", "categoria": "SS", "subtema": "REC_SS", "numero": "028"},
    {"tema": "Prescripción derechos SS", "materia": "Seguridad Social", "dificultad": "media",
     "tipo_trampa": "5_años_vs_4_años", "categoria": "SS", "subtema": "PRESC_SS", "numero": "029"},
    {"tema": "Responsabilidad empresarial prestaciones", "materia": "Seguridad Social", "dificultad": "alta",
     "tipo_trampa": "recargo_prestaciones_falta_medidas", "categoria": "SS", "subtema": "RESP_EMP", "numero": "030"},
    
    # AGE / PROCEDIMIENTO ADMINISTRATIVO (20 casos = 40%)
    
    # Procedimiento Administrativo Común - Ley 39/2015 (10 casos)
    {"tema": "Silencio administrativo positivo", "materia": "AGE - Ley 39/2015", "dificultad": "alta",
     "tipo_trampa": "excepciones_silencio_positivo", "categoria": "AGE", "subtema": "SILENC_POS", "numero": "031"},
    {"tema": "Silencio en recursos - Alzada", "materia": "AGE - Ley 39/2015", "dificultad": "muy_alta",
     "tipo_trampa": "silencio_sobre_silencio", "categoria": "AGE", "subtema": "SILENC_ALZADA", "numero": "032"},
    {"tema": "Recurso de reposición", "materia": "AGE - Ley 39/2015", "dificultad": "media",
     "tipo_trampa": "potestativo_vs_obligatorio", "categoria": "AGE", "subtema": "REC_REPOS", "numero": "033"},
    {"tema": "Notificaciones defectuosas", "materia": "AGE - Ley 39/2015", "dificultad": "alta",
     "tipo_trampa": "efectos_notificacion_irregular", "categoria": "AGE", "subtema": "NOTIF_DEF", "numero": "034"},
    {"tema": "Caducidad del procedimiento", "materia": "AGE - Ley 39/2015", "dificultad": "muy_alta",
     "tipo_trampa": "caducidad_vs_silencio", "categoria": "AGE", "subtema": "CADUC", "numero": "035"},
    {"tema": "Nulidad vs anulabilidad actos", "materia": "AGE - Ley 39/2015", "dificultad": "alta",
     "tipo_trampa": "causas_nulidad_pleno_derecho", "categoria": "AGE", "subtema": "NULIDAD", "numero": "036"},
    {"tema": "Responsabilidad patrimonial Administración", "materia": "AGE - Ley 39/2015", "dificultad": "media",
     "tipo_trampa": "requisitos_nexo_causal", "categoria": "AGE", "subtema": "RESP_PATR", "numero": "037"},
    {"tema": "Revocación actos favorables", "materia": "AGE - Ley 39/2015", "dificultad": "alta",
     "tipo_trampa": "limites_revocacion", "categoria": "AGE", "subtema": "REVOC", "numero": "038"},
    {"tema": "Rectificación errores materiales", "materia": "AGE - Ley 39/2015", "dificultad": "media",
     "tipo_trampa": "error_material_vs_derecho", "categoria": "AGE", "subtema": "RECTIF", "numero": "039"},
    {"tema": "Ejecutividad y ejecución forzosa", "materia": "AGE - Ley 39/2015", "dificultad": "alta",
     "tipo_trampa": "suspension_ejecutividad", "categoria": "AGE", "subtema": "EJEC", "numero": "040"},
    
    # Constitución Española (5 casos)
    {"tema": "Derechos fundamentales - Tutela judicial", "materia": "AGE - Constitución", "dificultad": "media",
     "tipo_trampa": "art_24_vs_art_117", "categoria": "AGE", "subtema": "CONST_TUTELA", "numero": "041"},
    {"tema": "Organización territorial del Estado", "materia": "AGE - Constitución", "dificultad": "alta",
     "tipo_trampa": "competencias_exclusivas_vs_compartidas", "categoria": "AGE", "subtema": "CONST_TERR", "numero": "042"},
    {"tema": "Recurso de inconstitucionalidad", "materia": "AGE - Constitución", "dificultad": "muy_alta",
     "tipo_trampa": "legitimacion_activa_recurso", "categoria": "AGE", "subtema": "CONST_REC", "numero": "043"},
    {"tema": "Reforma constitucional", "materia": "AGE - Constitución", "dificultad": "alta",
     "tipo_trampa": "procedimientos_reforma_ordinaria_agravada", "categoria": "AGE", "subtema": "CONST_REF", "numero": "044"},
    {"tema": "Principio de legalidad administrativa", "materia": "AGE - Constitución", "dificultad": "media",
     "tipo_trampa": "reserva_ley_vs_remision", "categoria": "AGE", "subtema": "CONST_LEG", "numero": "045"},
    
    # Ley 40/2015 Sector Público (3 casos)
    {"tema": "Órganos colegiados - Quórum", "materia": "AGE - Ley 40/2015", "dificultad": "media",
     "tipo_trampa": "mayoria_simple_vs_absoluta", "categoria": "AGE", "subtema": "COLEG_QUOR", "numero": "046"},
    {"tema": "Delegación de competencias", "materia": "AGE - Ley 40/2015", "dificultad": "alta",
     "tipo_trampa": "delegacion_vs_avocacion", "categoria": "AGE", "subtema": "DELEG", "numero": "047"},
    {"tema": "Conflictos de atribuciones", "materia": "AGE - Ley 40/2015", "dificultad": "alta",
     "tipo_trampa": "organos_competentes_resolucion", "categoria": "AGE", "subtema": "CONFL_ATRIB", "numero": "048"},
    
    # Función Pública (2 casos)
    {"tema": "Situaciones administrativas funcionarios", "materia": "AGE - EBEP", "dificultad": "alta",
     "tipo_trampa": "servicio_activo_vs_excedencia", "categoria": "AGE", "subtema": "SIT_ADMIN", "numero": "049"},
    {"tema": "Régimen disciplinario - Faltas", "materia": "AGE - EBEP", "dificultad": "media",
     "tipo_trampa": "graduacion_faltas_muy_graves", "categoria": "AGE", "subtema": "DISC", "numero": "050"},
]

# ============================================================================
# GENERAR BATCH REQUESTS PARA CLAUDE
# ============================================================================

def generar_batch_requests():
    """
    Genera las 50 requests para Claude Batch API
    """
    batch_requests = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    for idx, caso in enumerate(CASOS_DISTRIBUCIÓN, 1):
        # Completar parámetros del prompt
        prompt_completado = USER_PROMPT_TEMPLATE.format(
            tema=caso["tema"],
            materia=caso["materia"],
            dificultad=caso["dificultad"],
            tipo_trampa=caso["tipo_trampa"],
            categoria=caso["categoria"],
            subtema=caso["subtema"],
            numero=caso["numero"],
            categoria_completa=f"{caso['materia']} - {caso['tema']}",
            subcategoria_especifica=caso["tema"],
            nivel_dificultad=caso["dificultad"],
            nombre_descriptivo_trampa=caso["tipo_trampa"],
            normativa_base="normativa española vigente 2025",
            fecha_hoy=fecha_hoy
        )
        
        # Crear request para Batch API
        batch_request = {
            "custom_id": f"caso_{idx:03d}_{caso['subtema']}",
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 4000,
                "temperature": 0.3,  # Baja temperatura para precisión
                "system": SYSTEM_PROMPT,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt_completado
                    }
                ]
            }
        }
        
        batch_requests.append(batch_request)
    
    return batch_requests

# ============================================================================
# EJECUTAR GENERACIÓN
# ============================================================================

if __name__ == "__main__":
    print("🚀 Generando 50 requests para Claude Batch API...")
    
    batch_requests = generar_batch_requests()
    
    # Guardar en archivo JSON
    with open("batch_requests_dataset_oposiciones.json", "w", encoding="utf-8") as f:
        json.dump(batch_requests, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generadas {len(batch_requests)} requests")
    print("📁 Archivo guardado: batch_requests_dataset_oposiciones.json")
    
    # ENVIAR A BATCH API
    print("\n📤 Enviando a Claude Batch API...")
    
    try:
        batch_job = client.messages.batches.create(
            requests=batch_requests
        )
        
        print(f"✅ Batch creado exitosamente!")
        print(f"📋 Batch ID: {batch_job.id}")
        print(f"💰 Coste estimado: ${len(batch_requests) * 0.10:.2f} (con descuento 90%)")
        print(f"⏰ Tiempo estimado: 12-24 horas")
        print(f"\n🔍 Consulta el estado en: https://console.anthropic.com/batches")
        
        # Guardar ID del batch para recuperar después
        with open("batch_job_id.txt", "w") as f:
            f.write(batch_job.id)
        
    except Exception as e:
        print(f"❌ Error al crear batch: {e}")
        print("\n💡 Puedes enviar el archivo manualmente desde la consola de Anthropic:")
        print("   https://console.anthropic.com/batches")