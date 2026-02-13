💬 DISCUSIÓN PREVIA: Hallazgos Investigación + Actualizaciones Plan
Fecha: 26 Enero 2026 16:00
Objetivo: Discutir hallazgos ANTES de modificar plan
Estado: ⏸️ PENDIENTE APROBACIÓN USUARIO

🔍 HALLAZGOS INVESTIGACIÓN WEB (Enero 2026)
1. MEJORES MODELOS LLM CON CoT NATIVO
Modelos Propietarios TOP:
Modelo	Proveedor	CoT Nativo	Contexto	Coste	Disponibilidad
Gemini 3 Pro	Google	✅ Thinking Mode	1M tokens	Medio	✅ API
Gemini 2.5 Flash	Google	✅	1M tokens	GRATIS	✅ API Free Tier
Claude Opus 4.5	Anthropic	✅ Thinking Mode	1M tokens	Alto	✅ API
GPT-5.2-high	OpenAI	✅	200K tokens	Alto	✅ API
Grok 4.1 Thinking	xAI	✅ Thinking Mode	128K tokens	Medio	✅ API
Modelos Open-Source TOP:
Modelo	Parámetros	CoT Nativo	Benchmark	Disponibilidad
DeepSeek V3.2	670B (41B activos)	✅	MMLU-Pro: 86%	✅ Groq, Ollama
DeepSeek V3.2-Speciale	670B	✅ Extended Thinking	IMO Gold	✅ Ollama
Kimi K2 Thinking	1T (MoE)	✅	GPT-4 level	✅ API, Groq
Qwen3-235B	235B (22B activos)	✅	ArenaHard: 91.0	✅ Groq
QwQ-32B	32B	✅ Reasoning	SWE-Bench: 69.6	✅ Groq
GLM-4.7 Thinking	4.7B	✅ Hybrid Reasoning	Top open-source	✅ Ollama
LFM2.5-1.2B-Thinking	1.2B	✅ Thinking Traces	On-device	✅ Ollama
Modelos en Groq API (Enero 2026):
python
GROQ_MODELS_2026 = {
    # DeepSeek
    "groq/deepseek-r1-distill-llama-70b": "DeepSeek R1 Distill (70B)",
    "groq/deepseek-r1-distill-qwen-32b": "DeepSeek R1 Distill (32B)",
    
    # Llama 4
    "meta-llama/llama-4-maverick-17b-128e-instruct": "Llama 4 Maverick (10M context)",
    "meta-llama/llama-4-scout-17b-16e-instruct": "Llama 4 Scout",
    "llama-3.3-70b-versatile": "Llama 3.3 70B (tool use)",
    
    # Qwen
    "qwen/qwen3-32b": "Qwen3 32B",
    "groq/qwen-qwq-32b": "Qwen QwQ 32B (reasoning)",
    
    # OpenAI OSS
    "openai/gpt-oss-120b": "GPT-OSS 120B (456 tok/s)",
    "openai/gpt-oss-20b": "GPT-OSS 20B",
    
    # Kimi
    "moonshot/kimi-k2": "Kimi K2 (1T params, 128K context)"
}
Gemini 2.5 Flash FREE TIER:
python
GEMINI_FREE_TIER = {
    "modelo": "gemini-2.5-flash",
    "rpm": 10,  # Requests per minute
    "tpm": 250_000,  # Tokens per minute
    "rpd": 250,  # Requests per day
    "context": "1M tokens",
    "coste": "$0.00",  # ✅ GRATIS
    "calidad": "9/10"
}
💡 RECOMENDACIÓN: Usar Gemini 2.5 Flash para 250 casos/día GRATIS

2. BOE API OFICIAL - VERIFICACIÓN URLs
✅ API OFICIAL EXISTE: https://www.boe.es/datosabiertos/api/

Endpoints Clave:
python
BOE_API_ENDPOINTS = {
    # Legislación Consolidada
    "consolidado": "https://www.boe.es/datosabiertos/api/legislacion/consolidado/{boe_id}",
    
    # Verificar vigencia
    "vigencia": "https://www.boe.es/datosabiertos/api/legislacion/vigencia/{boe_id}",
    
    # Buscar por artículo
    "articulo": "https://www.boe.es/buscar/act.php?id={boe_id}#a{articulo}",
    
    # Estado consolidación
    "estado": "campo 'estado de consolidación' → 'Finalizado' o 'Desactualizado'"
}
Ejemplo Verificación:
python
def verificar_articulo_boe_api(ley_id, articulo, fecha_limite):
    """Verifica artículo con BOE API oficial"""
    
    # 1. Obtener consolidado
    url = f"https://www.boe.es/datosabiertos/api/legislacion/consolidado/{ley_id}"
    response = requests.get(url, params={"formato": "json"})
    
    # 2. Verificar estado
    estado = response.json().get("estado_consolidacion")
    if estado != "Finalizado":
        return {"vigente": False, "motivo": "Versión desactualizada"}
    
    # 3. Verificar fecha
    ultima_mod = response.json().get("ultima_modificacion")
    if ultima_mod > fecha_limite:
        return {"vigente": False, "motivo": f"Modificado después de {fecha_limite}"}
    
    # 4. Construir URL artículo
    url_articulo = f"https://www.boe.es/buscar/act.php?id={ley_id}#a{articulo.replace('.', '-')}"
    
    return {
        "vigente": True,
        "url_oficial": url_articulo,
        "fecha_verificacion": datetime.now().isoformat()
    }
💡 SOLUCIÓN SESGO OPCIÓN C: Añadir agente verificador Mistral con BOE API

3. FECHAS CORTE NORMATIVA (OFICIALES)
yaml
Fechas Límite por Oposición:
Cuerpo Administrativo SS:
  fecha_publicacion_boe: "2025-12-31"
  fecha_corte_normativa: "2025-12-31"
  plazo_inscripcion: "2026-01-29/30"
  
Cuerpo Gestión SS:
  fecha_publicacion_boe: "2025-12-31"
  fecha_corte_normativa: "2025-12-31"
  
AGE (Administrativos/Auxiliares):
  fecha_publicacion_boe: "2025-12-22"
  fecha_corte_normativa: "2025-12-22"
  fecha_examen: "2026-05-23"
  
Subinspectores Laborales:
  fecha_publicacion_boe: "2025-12-30"
  fecha_corte_normativa: "2025-12-30"
⚠️ IMPORTANTE:

❌ NO usar fecha fija "2024-12-30"
✅ Parametrizar por oposición
✅ Permitir al usuario elegir fecha límite
4. GraphRAG + FalkorDB (Búsqueda Fractal)
Concepto GraphRAG:
Vector RAG (Actual)          GraphRAG (Propuesto)
─────────────────            ──────────────────────
Qdrant Dense Search    →     Qdrant + Grafo Relaciones
Similitud semántica    →     Similitud + Jerarquía legal
                             
Ejemplo:
Query: "Art. 205 LGSS"
Vector RAG:
  → Encuentra Art. 205 (score 0.95)
  
GraphRAG:
  → Encuentra Art. 205 (score 0.95)
  → Navega relaciones:
      - MODIFICADO_POR: RD 5/2023
      - DESARROLLADO_POR: RD 1698/2011
      - DEROGA_A: Art. 161 Ley 1994
      - AFECTA_A: Arts. 206-210
Arquitectura Propuesta:
┌────────────────────────────────────────┐
│  CAPA 1: Qdrant (Vector Search)       │
│  - Búsqueda semántica                  │
│  - Top 30 resultados                   │
└──────────────┬─────────────────────────┘
               │
               ↓
┌────────────────────────────────────────┐
│  CAPA 2: FalkorDB (Graph Traversal)    │
│  - Verificar vigencia                  │
│  - Navegar relaciones                  │
│  - Detectar derogaciones               │
└──────────────┬─────────────────────────┘
               │
               ↓
┌────────────────────────────────────────┐
│  CAPA 3: Cohere Reranker               │
│  - Reordenar por relevancia            │
│  - Top 10 final                        │
└────────────────────────────────────────┘
Implementación con Metadatos XML:
python
# Ya tienes los metadatos XML del BOE con <referencias>
def crear_grafo_legal(xml_files):
    """Crea grafo de conocimiento desde XMLs BOE"""
    
    import networkx as nx
    G = nx.DiGraph()
    
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        
        # Nodo principal
        ley_id = tree.find(".//identificador").text
        G.add_node(ley_id, tipo="ley")
        
        # Relaciones
        for ref in tree.findall(".//referencias/referencia"):
            tipo = ref.get("tipo")  # MODIFICA, DEROGA, DESARROLLA
            target = ref.text
            G.add_edge(ley_id, target, relacion=tipo)
    
    return G
# Consulta con grafo
def buscar_con_grafo(query, grafo):
    """Búsqueda híbrida: Vector + Grafo"""
    
    # 1. Búsqueda vectorial
    resultados_vector = qdrant.search(query, top_k=30)
    
    # 2. Expandir con grafo
    resultados_expandidos = []
    for res in resultados_vector:
        ley_id = res.metadata.get("boe_id")
        
        # Verificar vigencia en grafo
        if grafo.has_node(ley_id):
            derogado = any(
                grafo[ley_id][target]["relacion"] == "DEROGADO_POR"
                for target in grafo.neighbors(ley_id)
            )
            if not derogado:
                resultados_expandidos.append(res)
    
    return resultados_expandidos
💡 DECISIÓN: Evaluar GraphRAG en fase posterior (no bloquea dataset)

5. MISTRAL TOOLS COMPLETOS
✅ Script más completo encontrado: 
backend/agents/mistral_tools.py
 (1002 líneas)

9 Herramientas Implementadas:
python
class MistralTools:
    1. buscar_rag_qdrant(query, top_k, filter_ley)
    2. buscar_boe_oficial(tipo, identificador, articulo, ley)
    3. verificar_url_boe(url, articulo_esperado)
    4. calcular_prestacion_ss(tipo, bases, años)
    5. generar_qa_legal(contexto, tema, dificultad)
    6. verificar_qa_completa(pregunta, respuesta, refs)
    7. clasificar_qa_tema(pregunta, respuesta)
    8. extraer_articulos_texto(texto)
    9. obtener_normativa_vigente(identificador, fecha)
Caché Semántica:
python
class SemanticCache:
    """Ahorra 60-70% llamadas LLM"""
    
    def get(self, query, threshold=0.95):
        # 1. Buscar en memoria (rápido)
        # 2. Buscar en Qdrant (persistente)
        # 3. Devolver respuesta cacheada
💡 USAR: Este script como base para agente verificador

6. ANÁLISIS PEDAGÓGICO (CRÍTICO)
✅ Documento encontrado: 
academias/25_01_hallazgos_data_casos.md

Hallazgos Clave:
Aspecto	Valor Real	Claude Actual	Gap
Longitud enunciado	100-120 palabras	200 palabras	-80
Distractores numéricos	40% (8/10)	30% (3/10)	-50%
Cálculos incluidos	20% (2/10)	0% (0/10)	-100%
Múltiples personajes	6-9 personajes	1 personaje	-88%
Trampa pedagógica	9/10	9/10	✅ OK
Técnicas de Distractores Reales:
yaml
Distractores Numéricos (40%):
  - Diferencias mínimas: 10-20€, 3-6 meses, 5-10%
  - Errores cálculo comunes:
      * Olvidar prorrateo pagas
      * No aplicar topes
      * Incluir conceptos excluidos
  
  Ejemplo:
    Salario: 1.200€ + Pagas: 1.200€×2
    a) 1.400€  ← CORRECTA (1.200 + 2.400/12)
    b) 1.200€  ← Error: olvidar prorrateo
    c) 1.600€  ← Error: sumar sin prorratear
    d) 1.300€  ← Error: prorratear mal (÷24)
Distractores Temporales (20%):
  - Confusión años vigencia
  - Confusión plazos procedimientos
  
Distractores Conceptuales (30%):
  - Artículos relacionados pero incorrectos
  - Mezcla de regímenes
  
Distractores Excepción (10%):
  - Omitir "salvo que..."
  - Invertir "excepto..."
Estructura Casos Prácticos Reales:
markdown
# CASO PRÁCTICO REAL (100-120 palabras)
Empresa "Logística S.L."
Personajes (6-9):
1. Julián (58): IT artrosis, 22 años RETA
2. Elena (45): Embarazada, 15 años cotizados
3. Manuel (62): Jubilación anticipada
4. Carmen (35): Riesgo embarazo
5. Pedro (50): AT, recargo 40%
6. Ana (40): Excedencia
7. Luis (55): IP absoluta
8. María (38): Maternidad
9. Jorge (60): Jubilación ordinaria
Preguntas (15 + 3 reserva):
- 2-3 encuadramiento
- 2-3 bases cotización (CON CÁLCULOS)
- 1-2 sistemas liquidación
- 2-3 prestaciones
- 1-2 procedimiento
- 1-2 excepciones
💡 CRÍTICO: Prompts actuales NO siguen estos patrones

7. REPARACIÓN SESGO OPCIÓN C
Problema Detectado:
Caso Claude v1:
  a = 2 (13%)
  b = 3 (20%)
  c = 7 (47%)  ← SESGO
  d = 3 (20%)
Distribución ideal:
  a = 25% ± 5%
  b = 25% ± 5%
  c = 25% ± 5%
  d = 25% ± 5%
Solución Propuesta:
python
def reparar_sesgo_casos_existentes(casos_json):
    """Repara sesgo opción C en casos ya generados"""
    
    # 1. Detectar sesgo
    dist = Counter([c["respuesta_correcta"] for c in casos])
    if dist["c"] / len(casos) > 0.30:
        print(f"⚠️ SESGO C: {dist['c']/len(casos)*100:.1f}%")
        
        # 2. Identificar casos a modificar
        casos_c = [c for c in casos if c["respuesta_correcta"] == "c"]
        n_modificar = int(dist["c"] - len(casos) * 0.25)
        
        # 3. Usar Mistral Agent para regenerar
        for caso in casos_c[:n_modificar]:
            prompt = f"""
            Modifica este caso para que la respuesta correcta sea 'a' o 'b' o 'd'
            (NO 'c'). Mantén la calidad y dificultad.
            
            Caso original:
            {json.dumps(caso, indent=2)}
            
            IMPORTANTE: La nueva respuesta correcta debe ser a, b o d.
            """
            
            nuevo_caso = mistral_agent.complete(prompt)
            # Reemplazar en dataset
Prevención Futura:
python
PROMPT_ANTI_SESGO = """
DISTRIBUCIÓN OBLIGATORIA:
- 25% respuestas correctas en opción A
- 25% respuestas correctas en opción B
- 25% respuestas correctas en opción C
- 25% respuestas correctas en opción D
⚠️ NUNCA uses siempre la misma opción como correcta.
⚠️ Alterna patrones: A, C, B, D, A, D, C, B...
"""
8. PROMPTS MEJORADOS (Prompt Engineering Avanzado)
Problema Actual:
python
# ❌ PROMPT BÁSICO (actual)
prompt = "Genera una pregunta sobre jubilación"
Solución Propuesta:
python
# ✅ PROMPT AVANZADO (mejorado)
PROMPT_ADVANCED = """
Eres un Tribunal de Oposiciones de élite con 20 años experiencia.
CONTEXTO CRÍTICO:
- Fecha límite legislación: {fecha_limite}
- Nivel dificultad: EXTREMO
- Objetivo: Filtrar 95% opositores
METODOLOGÍA CoT (6 PASOS OBLIGATORIOS):
PASO 1 - IDENTIFICAR EXCEPCIONES:
  ¿La pregunta menciona "salvo", "exceptuando"?
  → Buscar normas especiales
PASO 2 - JERARQUÍA NORMATIVA:
  CE > LO > Ley > RD
PASO 3 - TEMPORALIDAD:
  ¿Vigente en {fecha_limite}?
PASO 4 - LITERALIDAD:
  Copiar frase EXACTA del artículo
PASO 5 - DESCARTE:
  Eliminar opciones incorrectas con justificación
PASO 6 - RESPUESTA FINAL:
  Opción + Justificación + Fuente BOE verificada
INSTRUCCIONES ANTI-SESGO:
1. Distribuye respuestas: 25% a, 25% b, 25% c, 25% d
2. NUNCA uses siempre opción C
3. Alterna patrones: A, C, B, D, A, D, C, B...
TÉCNICAS DISTRACTORES (según análisis pedagógico):
- 40% Numéricos: diferencias 10-20€, 3-6 meses
- 30% Conceptuales: artículos relacionados incorrectos
- 20% Temporales: años vigencia diferentes
- 10% Excepciones: omitir "salvo que..."
ESTRUCTURA CASO PRÁCTICO:
- Enunciado: 100-120 palabras (NO 200)
- Personajes: 6-9 (NO 1)
- Cálculos: 2-3 preguntas con números
- Distractores numéricos: 8/10 preguntas
VERIFICACIÓN OBLIGATORIA:
- Cada artículo DEBE tener URL BOE verificada
- Fechas vigencia comprobadas con BOE API
- Razonamiento mínimo 500 caracteres
FEW-SHOT EXAMPLES:
{ejemplos_reales_academias}
OUTPUT JSON:
{{
  "pregunta": "...",
  "opciones": {{"a": "...", "b": "...", "c": "...", "d": "..."}},
  "respuesta_correcta": "b",  // ⚠️ NO SIEMPRE C
  "razonamiento_cot": {{
    "paso_1": "...",
    ...
    "paso_6": "..."
  }},
  "fuentes_verificadas": [
    {{"articulo": "Art. 173 LGSS", "url_boe": "https://...", "vigente": true}}
  ],
  "calculo_incluido": true,
  "distractores_numericos": 3
}}
"""
Few-Shot Examples:
python
EJEMPLOS_REALES = """
EJEMPLO 1 (de academias reales):
Julián, 58 años, autónomo. Última cotización: 15/03/2018.
Total cotizado: 22 años (RETA), 5 en últimos 10 años.
Base reguladora últimos 8 años: 1.200€/mes.
Solicita IP (01/2025) por artrosis. EVI dictamina IPT.
¿Qué prestación le corresponde y cuál sería su cuantía?
a) IPT: 1.200€ × 55% = 660€/mes
b) IPA: 1.200€ × 100% = 1.200€/mes
c) No tiene derecho a prestación  ← CORRECTA
d) IPT reducida: 1.200€ × 27,5% = 330€/mes
Explicación: Art. 195.1 LGSS exige estar en alta o situación asimilada.
Julián lleva 7 años sin cotizar (desde 2018), por lo que NO cumple
el requisito de estar en alta. Respuesta: c)
EJEMPLO 2 (con cálculo):
Carmen: salario 1.000€ + pagas 1.000€×2
Base mínima grupo I: 1.629,30€
¿Base de cotización por CC?
a) 1.629,30€  ← CORRECTA (aplicar tope mínimo)
b) 1.166,67€  ← Error: no aplicar tope
c) 1.000,00€  ← Error: solo salario base
d) 1.175,40€  ← Error: cálculo incorrecto
Cálculo:
Base bruta = 1.000 + (1.000×2/12) = 1.166,67€
Tope mínimo grupo I = 1.629,30€
Base final = max(1.166,67, 1.629,30) = 1.629,30€
Explicación: Art. 147 LGSS + Art. 19 LGSS (topes).
"""
9. VARIACIÓN RESPUESTAS "Según artículo..."
Problema:
❌ ABURRIDO (siempre igual):
"Según el artículo 205 LGSS..."
"Según el artículo 147 LGSS..."
"Según el artículo 173 LGSS..."
Solución:
python
VARIACIONES_CITAS = [
    "De conformidad con el art. {art} {ley}...",
    "El art. {art} {ley} establece que...",
    "Conforme al art. {art} {ley}...",
    "A tenor del art. {art} {ley}...",
    "En virtud del art. {art} {ley}...",
    "El art. {art} {ley} dispone que...",
    "Como indica el art. {art} {ley}...",
    "Tal y como recoge el art. {art} {ley}...",
    "El art. {art} {ley} regula que...",
    "Atendiendo al art. {art} {ley}...",
]
def variar_cita(articulo, ley):
    import random
    template = random.choice(VARIACIONES_CITAS)
    return template.format(art=articulo, ley=ley)
10. REGEX 6 PASOS - EXPLICACIÓN
¿Qué es Regex?
python
import re
# Regex = Regular Expression (expresión regular)
# Patrón para buscar texto
# Ejemplo: Verificar que hay 6 pasos CoT
patron = r"PASO [1-6]:"
texto = "PASO 1: ... PASO 2: ... PASO 3: ..."
matches = re.findall(patron, texto)
if len(matches) == 6:
    print("✅ CoT completo (6 pasos)")
else:
    print(f"❌ Faltan pasos: {6 - len(matches)}")
¿Por qué NO fiarse de Regex?
python
# ❌ PROBLEMA 1: Falsos positivos
texto = "PASO 1: PASO 2: PASO 3: PASO 4: PASO 5: PASO 6:"
# Detecta 6 pasos pero NO hay contenido
# ❌ PROBLEMA 2: Variaciones no detectadas
texto = "Paso 1: ... Paso 2: ..."  # Minúsculas
texto = "1. ... 2. ... 3. ..."      # Sin "PASO"
# ✅ SOLUCIÓN: Validación semántica
def validar_cot_semantico(texto):
    """Valida que hay razonamiento real, no solo formato"""
    
    # 1. Buscar pasos
    pasos = re.findall(r"PASO \d+:(.+?)(?=PASO \d+:|$)", texto, re.DOTALL)
    
    # 2. Verificar contenido mínimo
    for i, paso in enumerate(pasos, 1):
        if len(paso.strip()) < 50:
            return False, f"Paso {i} demasiado corto"
    
    # 3. Verificar keywords esperados
    keywords_esperados = {
        1: ["excepción", "salvo", "exceptuando"],
        2: ["CE", "LO", "Ley", "RD", "jerarquía"],
        3: ["vigente", "fecha", "modificación"],
        4: ["literal", "textual", "exacto"],
        5: ["descarto", "incorrecta", "error"],
        6: ["respuesta", "opción", "justificación"]
    }
    
    for i, keywords in keywords_esperados.items():
        if i <= len(pasos):
            if not any(kw in pasos[i-1].lower() for kw in keywords):
                return False, f"Paso {i} no contiene keywords esperados"
    
    return True, "CoT válido"
📋 PUNTOS CRÍTICOS A DISCUTIR
1. Fechas Límite Normativa
Pregunta: ¿Parametrizar por oposición o usar fecha fija?

Opciones:

A) Parametrizar (usuario elige: 2025-12-22, 2025-12-30, 2025-12-31)
B) Usar 2025-12-31 por defecto (más reciente)
C) Generar dataset SIN fecha límite, aplicar filtro después
Recomendación: Opción A (máxima flexibilidad)

2. GraphRAG / FalkorDB
Pregunta: ¿Implementar ahora o después?

Opciones:

A) Implementar ahora (retrasa dataset 1-2 semanas)
B) Fase posterior (no bloquea dataset)
C) Prototipo mínimo (solo verificación vigencia)
Recomendación: Opción B (evaluar después con 50 casos)

3. Modelos a Probar
Pregunta: ¿Qué modelos incluir en prueba 3 casos?

Propuesta:

yaml
Modelos Prueba (3 casos cada uno):
  1. Gemini 2.5 Flash (GRATIS, 1M context)
  2. DeepSeek V3.2 (Groq, reasoning)
  3. Kimi K2 Thinking (1T params)
  4. Qwen QwQ-32B (Groq, reasoning)
  5. Claude Sonnet 4 (baseline gold)
  6. Salamandra ULTRA (VPS, 6 tools)
  
Total: 6 modelos × 3 casos = 18 casos prueba
¿Aprobar lista?

4. Reparación Casos Claude Existentes
Pregunta: ¿Reparar 10 casos Claude o regenerar?

Opciones:

A) Reparar con Mistral Agent (añadir URLs, balancear respuestas)
B) Regenerar desde cero con prompts mejorados
C) Usar como baseline, generar nuevos
Recomendación: Opción A (aprovechar calidad jurídica)

5. Tipos Contenido Fine-Tuning
Pregunta: ¿Confirmar 4 tipos o añadir más?

Propuesta Actual:

yaml
1. QA Simple (125 casos)
2. Razonamiento CoT (125 casos)
3. Diálogos Verificados (125 casos)
4. Casos Prácticos Extremos (125 casos)
¿Añadir?:

5. Cálculos Numéricos (50 casos)
Jurisprudencia (50 casos)
6. Criterios Verificación
Pregunta: ¿Qué métricas usar para validación?

Propuesta:

yaml
Verificación Automática (Capa 1):
  - URLs BOE verificadas: 100%
  - Distribución respuestas: 25% ± 5% cada opción
  - CoT 6 pasos completo: 100%
  - Fecha vigencia correcta: 100%
  - Distractores numéricos: ≥ 40%
  - Cálculos incluidos: ≥ 20%
Verificación Claude (Capa 2):
  - Calidad jurídica: ≥ 8.5/10
  - Razonamiento coherente: ≥ 9.0/10
  - Trampas pedagógicas: ≥ 8.0/10
Verificación Manual (Capa 3):
  - Muestra aleatoria: 10% (50 casos)
  - Especialista revisa URLs
  - Confirma razonamiento
¿Aprobar métricas?

7. Prompts Mejorados
Pregunta: ¿Aplicar prompt engineering avanzado a todos los modelos?

Cambios:

✅ Añadir CoT 6 pasos obligatorio
✅ Instrucciones anti-sesgo explícitas
✅ Few-shot examples de academias reales
✅ Técnicas distractores (40% numéricos)
✅ Estructura casos (6-9 personajes, 100-120 palabras)
✅ Variaciones citas legales
¿Aprobar cambios?

8. Coste Estimado Actualizado
yaml
Prueba 3 Casos (18 total):
  - Gemini 2.5 Flash: $0.00 (GRATIS)
  - DeepSeek V3.2: $0.00 (Groq)
  - Kimi K2: $0.01
  - Qwen QwQ: $0.00 (Groq)
  - Claude Sonnet 4: $0.30
  - Salamandra ULTRA: $0.00 (VPS)
  Total: $0.31
Producción 500 Casos:
  - 250 Gemini 2.5 Flash: $0.00 (GRATIS)
  - 125 DeepSeek V3.2: $0.00 (Groq)
  - 125 Claude Sonnet 4: $12.50 (gold)
  Total: $12.50
Verificación Claude (500 casos):
  - $0.01 × 500 = $5.00
TOTAL PROYECTO: $17.81
¿Aprobar presupuesto?

9. Scripts Mistral
Pregunta: ¿Usar 
mistral_tools.py
 como base?

Ventajas:

✅ 9 herramientas ya implementadas
✅ Caché semántica (ahorra 60-70%)
✅ Verificación BOE integrada
✅ Cálculos prestaciones
¿Aprobar uso?

10. Análisis Pedagógico
Pregunta: ¿Integrar hallazgos en métricas?

Métricas Nuevas:

yaml
Calidad Pedagógica:
  - Longitud enunciado: 100-120 palabras
  - Distractores numéricos: ≥ 40%
  - Cálculos incluidos: ≥ 20%
  - Múltiples personajes: ≥ 6
  - Trampas pedagógicas: ≥ 8/10
¿Añadir a plan?

11. Velocidad vs Calidad
Usuario dijo: "La velocidad me da igual, solo la calidad importa"

Implicaciones:

✅ Usar modelos lentos pero precisos (Claude, Gemini 3 Pro)
✅ Verificación exhaustiva 3 capas
✅ Revisión manual 10%
❌ NO optimizar por velocidad
¿Confirmar prioridad?

12. Distribución Casos por Modelo
Pregunta: ¿Cómo distribuir 500 casos?

Propuesta:

yaml
Distribución por Calidad:
  - Claude Sonnet 4: 125 casos (gold standard)
  - Gemini 2.5 Flash: 250 casos (gratis, alta calidad)
  - DeepSeek V3.2: 125 casos (reasoning)
  
Distribución por Tipo:
  - QA Simple: Gemini 2.5 Flash (125)
  - Razonamiento CoT: DeepSeek V3.2 (125)
  - Diálogos: Gemini 2.5 Flash (125)
  - Casos Extremos: Claude Sonnet 4 (125)
¿Aprobar distribución?

13. Timeline Actualizado
yaml
Fase 1: Preparación (2 días):
  - Modificar scripts (PostgreSQL → BOE API)
  - Implementar prompts mejorados
  - Configurar Mistral tools
  
Fase 2: Prueba 3 Casos (1 día):
  - 6 modelos × 3 casos = 18 casos
  - Verificación 3 capas
  - Evaluación calidad
  
Fase 3: Selección Modelo (1 día):
  - Análisis resultados
  - Selección mejor modelo por tipo
  
Fase 4: Producción 500 Casos (3-5 días):
  - Generación masiva
  - Verificación automática
  - Verificación Claude
  
Fase 5: Revisión Manual (2 días):
  - Especialista revisa 50 casos (10%)
  - Ajustes finales
  
TOTAL: 9-11 días
¿Aprobar timeline?

14. Reparación Sesgo Opción C
Pregunta: ¿Reparar casos existentes o solo prevenir futuros?

Opciones:

A) Reparar 10 casos Claude + prevenir futuros
B) Solo prevenir futuros
C) Regenerar todos desde cero
Recomendación: Opción A

15. Siguiente Paso Inmediato
Pregunta: ¿Qué hacer AHORA?

Opciones:

A) Actualizar plan con todos los hallazgos
B) Empezar prueba 3 casos directamente
C) Implementar reparación sesgo primero
D) Discutir más puntos antes de decidir
¿Qué prefieres?

✅ RESUMEN EJECUTIVO
Hallazgos Clave:

✅ Gemini 2.5 Flash GRATIS (250 casos/día)
✅ BOE API oficial existe (verificación URLs)
✅ Fechas corte: 2025-12-22 a 2025-12-31 (parametrizar)
✅ Análisis pedagógico: 40% distractores numéricos, 20% cálculos
✅ Mistral tools completo (9 herramientas + caché)
✅ Prompts básicos → avanzados (CoT 6 pasos + anti-sesgo)
✅ GraphRAG: evaluar después (no bloquea)
Decisiones Pendientes:

 Aprobar lista 6 modelos prueba
 Confirmar 4 tipos contenido
 Aprobar métricas verificación
 Confirmar presupuesto $17.81
 Aprobar timeline 9-11 días
 Decidir reparación casos Claude
 revisar por elusuario y aprobar!!! no incluir hasta que no este aprobado!!!

