# 🎯 PLAN COMPLETO: PRUEBA DE VIABILIDAD OpositaIA

**Fecha:** 13 de Febrero de 2026  
**Objetivo:** Verificar si OpositaIA puede generar casos prácticos SS/AGE con:
- ✅ 100% respuestas correctas (no 90%)
- ✅ 100% razonamiento experto observable
- ✅ 100% confianza del sistema (no 85%)
- ✅ Cálculos SS 100% exactos
- ✅ Trampas pedagógicas realistas

---

## 📋 FASE 0: TIPOS DE CÁLCULOS REALES (INVESTIGACIÓN COMPLETADA)

### Cálculos SS que funcionarios usan REALMENTE:

**1. Incapacidad Temporal (IT)**
- Base diaria = Base cotización / 30
- Subsidio diario según contingencia (EC/AT/EP) y día baja
- Fechas: días 1-3, 4-20, 21+
- Artículos: 173.1, 174.2 TRLGSS

**2. Pensión Incapacidad Permanente Total**
- Base reguladora = media de 24 últimos meses
- Porcentaje: 100% de base reguladora
- Edad: 55+ años → incremento (50% + 5% por año>55)
- Cálculo: Base × (1 + 0.05 × años_exceso)

**3. Jubilación**
- Base reguladora = media 25 últimos años
- Coeficiente reductor por anticipo
- Complemento por cargas familiares
- Cálculo: Base × coeficiente × (1 + complemento)

**4. Subsidio por Desempleo**
- % de base cotización: 70% (primeros 6 meses), 60% (después)
- Duración: 6-24 meses según edad y cotización
- Cálculo: Base × % × duración_meses

**5. Cuota de Cotización (Aportación Empresario)**
- % según afiliación (Grupo 1-9)
- Base cotización máxima y mínima
- Tipo: Empresario + Trabajador
- Cálculo: Base × % grupo

**6. Complementos a Pensiones**
- Complemento mínimo
- Complemento por ser discapacitado
- Complemento por cargas familiares
- Cálculo: Base × factor según tipo

**7. Devoluciones de Aportaciones**
- Caso: Muerte, no derecho a pensión
- Devuelve: Aportaciones trabajador + intereses
- Plazos y condiciones según causa

**8. Prestación por Maternidad/Paternidad**
- Subsidio 16-18 semanas
- % del salario base
- Duración según tipo

**9. Ayudas por Hijo a Cargo**
- Importe mensual fijo
- Condiciones: edad, ingresos, situación laboral
- Combinable con pensión

**10. Bonificaciones en Cuotas**
- Trabajadores 30+ años desempleados de larga duración
- Bonificación 100% aportación empresario
- Período máximo

**11. Ingreso Mínimo Vital (IMV)**
- Importe base según composición unidad familiar (2026):
  - 1 persona: 564,60€/mes
  - 2 personas: 847,15€/mes
  - 3 personas: 1.102,80€/mes
  - 4 personas: 1.356,45€/mes
  - 5+ personas: 1.610,10€/mes
- Incremento 50% si ambos > 30 años
- Fórmula: IMV = importe_base - (ingresos_netos × 50%)
- Requisitos: Nacionalidad, empadronamiento 12 meses, patrimonio < 15.965,50€
- Artículos: Real Decreto-ley 20/2020, Art. 8

--- 
## 🏗️ FASE 1: EXPANDIR CALCULADORA SS (Archivo: `backend/calculators/calculos_ss_extended.py`)

### Estructura nueva:

```python
class CalculadoraSS:
    # Existente
    ✅ calcular_subsidio_it()
    
    # NUEVOS (implementar):
    ❌ calcular_pension_ipt()           # Incapacidad Permanente Total
    ❌ calcular_pension_jubilacion()    # Jubilación con anticipos/incrementos
    ❌ calcular_subsidio_desempleo()    # Desempleo 70%/60% según semanas
    ❌ calcular_cuota_cotizacion()      # Aportaciones empresario/trabajador
    ❌ calcular_complementos()          # Mínimo, discapacitado, cargas familiares
    ❌ calcular_devoluciones()          # Reembolsos por no derecho
    ❌ calcular_maternidad_paternidad() # Subsidios 16-18 semanas
    ❌ calcular_ayuda_hijo_cargo()      # Importe fijo + condiciones
    ❌ calcular_bonificacion_cuotas()   # 100% desempleados larga duración
    ❌ calcular_coeficiente_reductor()  # Anticipos jubilación
    ❌ calcular_ingreso_minimo_vital()  # IMV: base - (ingresos × 50%)
```

### Validaciones:
- ✅ Decimales exactos (Decimal class, no float)
- ✅ Citas de artículos TRLGSS
- ✅ Normativa vigente 2026
- ✅ Explicaciones paso a paso

---

## 🎯 FASE 2: ORQUESTADOR + QUERY VALIDATOR (Archivos nuevos)

### `backend/agents/orchestrator.py`

**Responsabilidades:**

```
Usuario: "Genera 10 casos SS sobre subsidios de alta dificultad"
         ↓
[NORMALIZACIÓN]
  - Limpia entrada: "subsidios" → "subsidio_incapacidad_temporal"
  - Extrae: tema="IT", dificultad="alta", tipo="SS", cantidad=10
         ↓
[ENRIQUECIMIENTO]  (Query Validator)
  - Busca en opositaia_leyes_master: 54 leyes relevantes
  - Busca en opositaia_knowledge_FULL_XML: artículos contexto
  - Extrae metadatos BOE: vigencias, derogaciones, modificaciones
         ↓
[DELEGACIÓN]
  - Pasa contexto a Generator (Salamandra)
  - Generator crea caso con tools
  - Pasa a Verifiers (5 agentes)
  - Retorna con score 0-1.0
```

**Métodos principales:**

```python
class Orchestrator:
    def normalize_query(query: str) -> Dict
        # Mapear tema natural → código interno
        # "subsidios" → "subsidio_it" | "subsidio_desempleo"
        # "pensión" → "pension_jubilacion" | "pension_ipt"
    
    def validate_query(normalized: Dict) -> bool
        # Verificar: tema válido, dificultad en rango, cantidad reasonble
    
    def enrich_context(tema: str) -> Dict
        # RAG: buscar artículos Qdrant
        # LEY: buscar en opositaia_leyes_master
        # BOE: buscar vigencias, derogaciones
        # Return: contexto con metadatos BOE completos
    
    def delegate_to_factory(tema, contexto) -> factory_result
        # Enviar a agent_factory_real.py con contexto enriquecido
```

### `backend/agents/query_validator.py`

```python
class QueryValidator:
    def map_tema_to_articles(tema: str, leyes_master) -> List[Article]
        # Tema "subsidio_it" → [Art 173, 174, 175 TRLGSS]
        # Incluir: vigencia_inicio, vigencia_fin, derogaciones
    
    def map_tema_to_qdrant_collections() -> List[str]
        # "subsidio_it" → opositaia_knowledge_FULL_XML + chunks
    
    def validate_boe_metadata(articles: List) -> bool
        # ¿Todos los artículos son vigentes en 2026?
        # ¿Hay derogaciones?
        # ¿Hay modificaciones recientes?
```

---

## 🧠 FASE 3: CHAIN-OF-THOUGHT OBSERVABLE (Archivo: `backend/agents/reasoning_tracer.py`)

**¿Por qué?** Necesitas ver CÓMO razona Salamandra, no solo respuesta final

```python
class ReasoningTracer:
    """Captura el razonamiento paso-a-paso de Salamandra"""
    
    def trace_salamandra_reasoning(prompt: str, tools: List) -> ReasoningLog:
        """
        Llamar Salamandra con instrucción especial:
        "Divide el problema en pasos. Explica CADA paso."
        """
        
        system_prompt = """
        Eres experto en Seguridad Social. Resuelve como profesor de academia:
        
        1. IDENTIFICAR: ¿Qué tipo de caso es? (IT/Jubilación/etc)
        2. BUSCAR NORMA: ¿Qué artículos aplican? (usar tool search_qdrant)
        3. ANALIZAR DATOS: ¿Qué datos da el enunciado?
        4. APLICAR FÓRMULA: Aplicar cálculo paso-a-paso (usar tool calculate_ss)
        5. VERIFICAR BOE: ¿Es la norma vigente? (usar tool search_boe)
        6. CONCLUIR: Explicar por qué SOLO una respuesta es correcta
        
        Output en JSON:
        {
          "paso_1_identificacion": "...",
          "paso_2_normas": ["Art 173", "Art 174"],
          "paso_3_datos": {"base": 1500, "dia": 25, "contingencia": "EC"},
          "paso_4_calculo": "1500/30 = 50€/día × 0.75 = 37.5€",
          "paso_5_vigencia": "Art 173 vigente hasta 2026-12-31",
          "paso_6_conclusion": "Respuesta correcta: C (37.50€)"
        }
        """
```

**Output esperado:**

```json
{
  "razonamiento_observable": {
    "paso_1": "Es un caso de Incapacidad Temporal (IT) por Enfermedad Común (EC)",
    "paso_2": "Aplican: Art 173.1 (porcentajes), Art 174.2 (base diaria)",
    "paso_3": "Datos: Base=1500€, Día=25, Contingencia=EC",
    "paso_4": "Base diaria = 1500/30 = 50€. Día 25 → 75% → 50×0.75 = 37.50€",
    "paso_5": "Vigencia: Art 173-174 vigentes en 2026 ✅",
    "paso_6": "Respuesta: C (No es A=25€, ni B=30€, ni D=40€)"
  },
  "confianza": 1.0,
  "articulos_usados": ["Art 173.1 TRLGSS", "Art 174.2 TRLGSS"],
  "calculos_verificados": true
}
```

---

## 🤖 FASE 4: ARQUITECTURA MULTI-AGENTE VERIFICACIÓN (100% Confianza)

### 5 Agentes con Validación Automática:

```
[GENERATOR] (Salamandra)
  Input: tema, contexto BOE enriquecido
  Tools: search_qdrant, search_boe, calculate_ss
  Output: caso_bruto { pregunta, opciones, respuesta_correcta, razonamiento }
    ↓
[AGENT 1: BOE Verifier] ← AUTOMÁTICO
  Valida: ¿URLs BOE reales? ¿Vigentes en 2026? ¿No derogados?
  Score: 0-1.0 (meta: 1.0)
    ↓
[AGENT 2: Legal Reasoner] ← AUTOMÁTICO
  Valida: ¿Subsunción correcta? ¿Excepciones aplicadas? ¿Lógica OK?
  Score: 0-1.0 (meta: 0.98+)
    ↓
[AGENT 3: Calculator] ← AUTOMÁTICO
  Ejecuta: calculos_ss_extended.py verificando CADA paso
  Score: 0-1.0 (meta: 1.0)
    ↓
[AGENT 4: Coherence] ← AUTOMÁTICO
  Detecta: fechas contradictorias, datos inconsistentes
  Score: 0-1.0 (meta: 0.98+)
    ↓
[AGENT 5: Trap Pedagogy] ← AUTOMÁTICO
  Evalúa: ¿Trampa es realista? ¿Educativa? ¿Sutil?
  Score: 0-1.0 (meta: 0.95+)
    ↓
[RESULTADO] → JSON verificado + razonamiento observable
  Score final = PROMEDIO(Agent1-5) = "Confianza: X%"
  Si score >= 0.95 → ✅ Aprobado
  Si score < 0.95 → 🔄 Regenerar
```

---

## 📝 FASE 5: GENERADORES CON PROMPTS EXPERTOS

### `backend/agents/ss_case_generator.py`

```python
class SSCaseGenerator:
    """Generador casos SS con Salamandra + prompts expertos"""
    
    def generate_caso_subsidio_it(self, dificultad: str, tema_especifico: str) -> Dict:
        """
        Genera caso IT de alta dificultad con trampa pedagógica
        
        Prompt:
        - Eres profesor academia Oposiciones SS con 20 años experiencia
        - Crea 1 caso test tipo examen sobre: {tema_especifico}
        - Dificultad: {dificultad} (80% opositores fallan)
        - Trampa: diseñada sobre error TÍPICO de opositores
        - Usa SOLO artículos vigentes en 2026
        - Tools: search_qdrant(tema), search_boe(articulo), calculate_ss(params)
        - Output: JSON completo con razonamiento observable
        """
        pass
    
    def generate_caso_pension_jubilacion(...) -> Dict:
        pass
    
    def generate_caso_desempleo(...) -> Dict:
        pass
```

### Temas específicos SS (20 combinaciones):

```
Subsidio IT:
  ✅ Cálculo base diaria EC días 1-3 (no se cobra)
  ✅ Cálculo base diaria EC días 4-20 (60%)
  ✅ Cálculo base diaria EC día 21+ (75%)
  ✅ Cálculo AT/EP día 1 (no se cobra) vs día 2+ (75%)
  ✅ Cambio de contingencia a mitad del período

Pensión Jubilación:
  ✅ Anticipos con coeficiente reductor
  ✅ Incrementos por edad 55+
  ✅ Complementos por cargas familiares

Desempleo:
  ✅ Cambio 70% → 60% en semana 7
  ✅ Duración según edad y cotización
```

---

## 🧪 FASE 6: PRUEBA PILOTO REAL (20 casos observables)

### Script: `test_viabilidad_piloto_completo.py`

```python
#!/usr/bin/env python3
"""
PRUEBA PILOTO: 20 casos (10 SS + 10 AGE)
Observar razonamiento en tiempo real
"""

# PART 1: PREPARACIÓN
orchestrator = Orchestrator()
generator = SSCaseGenerator()
verifiers = [Agent1_BOE(), Agent2_Legal(), Agent3_Calculator(), 
             Agent4_Coherence(), Agent5_Pedagogical()]

# PART 2: GENERAR 10 CASOS SS
casos_ss = []
for i in range(10):
    tema = sample_ss_topics()[i]
    
    print(f"\n{'='*80}")
    print(f"📝 CASO SS #{i+1}: {tema}")
    print(f"{'='*80}")
    
    # Step 1: Orquestar
    contexto = orchestrator.enrich_context(tema)
    print(f"✅ Contexto: {len(contexto['articulos'])} artículos BOE enriquecidos")
    
    # Step 2: Generar
    caso = generator.generate_caso_subsidio_it(
        dificultad="alta",
        tema_especifico=tema
    )
    print(f"\n📋 Caso generado:")
    print(f"  Pregunta: {caso['pregunta'][:80]}...")
    print(f"  Respuesta correcta: {caso['respuesta_correcta']}")
    
    # Step 3: Observar razonamiento
    print(f"\n🧠 Razonamiento Salamandra:")
    print(f"{json.dumps(caso['razonamiento_observable'], indent=2, ensure_ascii=False)}")
    
    # Step 4: Verificar automáticamente
    resultados_agentes = {}
    for agent in verifiers:
        resultado = agent.verify(caso)
        resultados_agentes[agent.id] = resultado.score
        print(f"  {agent.nombre}: {resultado.score:.2f} ✅" if resultado.status == "PASS" else f"  {agent.nombre}: {resultado.score:.2f} ❌")
    
    # Step 5: Puntuación final
    score_promedio = sum(resultados_agentes.values()) / len(resultados_agentes)
    caso['confianza_sistema'] = score_promedio
    
    print(f"\n📊 Confianza Final: {score_promedio:.1%}")
    
    casos_ss.append(caso)

# PART 3: ANÁLISIS
print(f"\n{'='*80}")
print("📊 ANÁLISIS RESULTADOS SS")
print(f"{'='*80}")
print(f"Total generados: {len(casos_ss)}")
print(f"Confianza promedio: {mean([c['confianza_sistema'] for c in casos_ss]):.1%}")
print(f"Casos 100% confianza: {len([c for c in casos_ss if c['confianza_sistema'] == 1.0])}")
print(f"Razonamientos 100% expertos: {len([c for c in casos_ss if c['razonamiento_completo'] == True])}")

# PART 4: EXPORTAR RESULTADOS
with open("resultados/casos_ss_piloto.json", "w", encoding="utf-8") as f:
    json.dump(casos_ss, f, indent=2, ensure_ascii=False)

print(f"\n💾 Resultados guardados en: resultados/casos_ss_piloto.json")
```

---

## 📊 FASE 7: VALIDACIÓN MANUAL (TÚ VERIFICAS)

Para CADA caso piloto, revisar:

```
✅ RESPUESTA CORRECTA:
   ¿Es realmente la correcta según normativa 2026?

✅ RAZONAMIENTO OBSERVABLE:
   ¿Cada paso es lógico? ¿Explica por qué A y no B/C/D?
   ¿Cita artículos correctos?

✅ CÁLCULOS:
   ¿Verificar con calculos_ss_extended.py?
   ¿Base diaria correcta?
   ¿Porcentaje aplicado correctamente?

✅ TRAMPA PEDAGÓGICA:
   ¿Es realista? (basada en error típico opositor)
   ¿Es educativa? (enseña concepto clave)
   ¿No es obvia?

✅ VIGENCIA TEMPORAL:
   ¿Todos artículos vigentes en 31/01/2026?
   ¿Sin derogaciones posteriores?
```

---

## 📈 FASE 8: ANÁLISIS FINAL + REPORTE VIABILIDAD

### Métricas:

| Métrica | Target | Cálculo |
|---------|--------|---------|
| Precisión respuesta | 100% | (casos correctos / total) × 100 |
| Razonamiento experto | 100% | (razonamientos lógicos / total) × 100 |
| Confianza sistema | 100% | (score promedio agentes) × 100 |
| Cálculos exactos | 100% | (sin errores decimales/fórmula) × 100 |
| Vigencia BOE | 100% | (artículos vigentes / total) × 100 |
| Trampas pedagógicas | 100% | (realistas + educativas) × 100 |

### Reporte:

```markdown
# REPORTE VIABILIDAD OpositaIA - 13/02/2026

## RESUMEN EJECUTIVO
✅ Viable | ❌ No viable | ⚠️ Parcialmente viable

## RESULTADOS PRUEBA PILOTO SS (10 casos)
- Precisión: X%
- Razonamiento: X%
- Confianza: X%
- Cálculos: X%

## RESULTADOS PRUEBA PILOTO AGE (10 casos)
- Precisión: X%
- Razonamiento: X%
- Confianza: X%

## MEJORAS NECESARIAS
1. (Si score < 100%)
2. (Si score < 100%)

## ROADMAP SIGUIENTE FASE
- Escalar a 550 casos
- Fine-tuning Salamandra R1
- API de casos expuesto
```

---

## ⏱️ CRONOGRAMA ESTIMADO

| Fase | Tareas | Tiempo |
|------|--------|--------|
| **SETUP** | Verificar Salamandra + Qdrant + BOE | 30 min |
| **1** | Expandir calculos_ss.py (9 tipos nuevos) | 45 min |
| **2** | Orquestador + Query Validator | 60 min |
| **3** | Chain-of-Thought tracer | 30 min |
| **4** | 5 Agentes verificadores | 90 min |
| **5** | Generadores SS/AGE con prompts | 60 min |
| **6** | Prueba piloto 20 casos | 120 min |
| **7** | Validación manual | 60 min |
| **8** | Análisis + reporte | 30 min |
| **TOTAL** | | **~525 min = ~8.75 horas** |

---

## � ANEXO: INGRESO MÍNIMO VITAL (IMV) - YA IMPLEMENTADO ✅

**Archivo creado:** `backend/calculators/calculos_imv.py` (COMPLETAMENTE FUNCIONAL)

### Implementación:

```python
class CalculadoraIMV:
    # Importes base 2026 (actualizados con IPC):
    PERSONA_SOLA: 564,60€
    DOS_PERSONAS: 847,15€
    TRES_PERSONAS: 1.102,80€
    CUATRO_PERSONAS: 1.356,45€
    CINCO_PERSONAS: 1.610,10€
    
    # Incremento 50% si ambos > 30 años
    # Fórmula: IMV = importe_base - (ingresos_netos × 50%)
    # Requisitos: patrimonio < 15.965,50€, empadronamiento 12 meses
    # Normativa: Real Decreto-ley 20/2020, Art. 8
```

### Funcionalidades incluidas:

✅ Cálculo IMV por tipo unidad familiar  
✅ Incremento automático si ambos > 30 años  
✅ Contabilización ingresos (50%)  
✅ Validación patrimonio  
✅ Análisis requisitos cumplimiento  
✅ Manejo Decimal para precisión exacta  
✅ Explicaciones paso-a-paso  

### Métodos disponibles:

```python
calcular_imv(tipo_unidad, ingresos_netos_familia, num_miembros, ambos_mayores_30)
validar_patrimonio(patrimonio_total, tiene_vivienda_habitual)
calcular_duracion_imv(periodo_meses, renovacion_anual)
calcular_imv_simple(tipo_unidad_str, ingresos_netos, num_miembros)  # Wrapper
```

### Casos de prueba incorporados:

- Persona sola sin ingresos → 564,60€/mes
- 2 personas >30 años, 300€ ingresos → incremento + cálculo correcto
- Validación patrimonio con vivienda habitual

### Integración con agentes:

El Calculator Verifier (Agent 3) usará `calculos_imv.py` para validar casos IMV en la prueba piloto.

---

## �🚀 COMENZAMOS?

**OPCIÓN A:** Empezar SETUP + FASE 1 (75 min)
**OPCIÓN B:** Saltar SETUP, asumir Salamandra OK → FASE 1 (45 min)
**OPCIÓN C:** Comenzar ya (pero necesito confirmación de recursos)

**¿Adelante?**
