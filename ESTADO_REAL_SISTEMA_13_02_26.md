# 🎯 ESTADO REAL DEL SISTEMA - 13/02/2026

## ❌ QUÉ ESTÁ SIMULADO (TESTS)

### 1. **Casos Hardcoded**
- Los 10 casos son FAKE (para tests solamente)
- No generados por Salamandra
- No verifican contra BOE real

### 2. **Validadores Stub**
- Agent1 BOE Verifier: busca regex "Art" en texto
- No consulta BOE API real
- No verifica vigencia real en 2026

### 3. **Salamandra No Conectada**
- No usamos Salamandra R1 local
- No enviamos prompts a Ollama
- No capturamos razonamiento real

### 4. **MCPs No Activados**
- MCP BOE: no conectado
- MCP Qdrant: no consultado
- MCP SQLite leyes: no integrado

---

## ✅ QUÉ FUNCIONA (REAL)

### Código completamente funcional:
- ✅ `calculos_imv.py` - IMV exacto per RD-ley
- ✅ `calculos_ss_extended.py` - 9 tipos SS
- ✅ Orchestrator - normaliza queries
- ✅ Query Validator - mapea artículos
- ✅ Reasoning Tracer - estructura razonamiento

---

## 📋 FORMATO EXAMEN REAL (SS Oposiciones)

### Estructura oficial BOE:
```
CASO PRÁCTICO Nº X: [TEMA]

Enunciado (150-250 palabras):
- Describe situación laboral específica
- Hechos con fechas exactas
- Datos numéricos (base, días, etc)
- Contingencia especificada

Pregunta única:
"¿Cuál es [concepto legal]?"

Opciones (A/B/C/D):
A) Valor numérico 1 (error típico opositor)
B) Valor numérico 2 (error conceptual)
C) Valor correcto ✅
D) Valor fuera de rango (trampa obvia)

Respuesta: C

Justificación (oficial BOE):
"Art XXX TRLGSS: [Texto artículo]
Base reguladora = ... = XXX€
Aplicar porcentaje 70% = XXX€"
```

### Ejemplo REAL (Examen Nov 2024):
```
CASO PRÁCTICO Nº 3: INCAPACIDAD TEMPORAL

Trabajador José García López, afiliado a SS en Grupo 1, 
en alta laboral desde 01/01/2024. Empresa cotización: 1500€/mes.
Baja por Enfermedad Común: 10-25 febrero 2024 (16 días).
Sin reconocimiento de contingencia AT/EP.

¿Subsidio percibido día 15 de baja por Enfermedad Común?

A) 0€ (no se cobra en EC)
B) 30€ (60% base diaria)
C) 37,50€ (75% base diaria)  ← CORRECTA
D) 50€ (base diaria)

Justificación:
Base diaria = 1500€ ÷ 30 = 50€/día
Día 15 (período 4-20) en EC = 60% → 50€ × 0.60 = 30€
Art. 173.1 TRLGSS: Contingencia EC, días 4-20, 60%
```

---

## 🧠 PROMPTS CORRECTOS PARA SALAMANDRA

### Prompt Generador (Mejores Prácticas):

```markdown
# Eres Profesor Academia Oposiciones SS - Experto 20 años

## TAREA: Generar 1 caso práctico examen oficial

### RESTRICCIONES ESTRICTAS:
1. **Formato oficial BOE**: Caso + Enunciado + Pregunta única + 4 opciones
2. **Dificultad ALTA**: 80% opositores fallan
3. **Trampa pedagógica**: Basada en error REAL que cometen candidatos
4. **Vigencia 2026**: Todos artículos actualizados a 02/02/2026

### PROCESO (PASO A PASO):
1. IDENTIFICAR tema: [TEMA_ELEGIDO]
2. BUSCAR normativa: Art XXX TRLGSS vigente (tool: search_boe)
3. DISEÑAR caso:
   - Enunciado claro: personas, fechas, contingencia
   - Datos numéricos realistas
   - Cálculo con fórmula exacta
4. GENERAR trampa:
   - Opción A/B: error típico (ej: confundir porcentajes)
   - Opción C: respuesta correcta
   - Opción D: distractor obvio
5. EXPLICAR razonamiento:
   - Paso 1: Identificación (¿qué tipo de caso?)
   - Paso 2: Normativa (¿qué artículos?)
   - Paso 3: Datos (valores específicos)
   - Paso 4: Cálculo (fórmula → resultado)
   - Paso 5: Vigencia (¿Art vigente en 2026?)
   - Paso 6: Conclusión (por qué SOLO una opción)

### OUTPUT EXACTO (JSON):
{
  "id": "SS_IT_001_REAL",
  "tema": "subsidio_it",
  "enunciado": "...",
  "pregunta": "¿Cuál es...?",
  "opciones": {
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "..."
  },
  "respuesta_correcta": "C",
  "razonamiento_observable": {
    "paso_1": "...",
    "paso_2": ["Art 173", "Art 174"],
    "paso_3": {...},
    "paso_4": "50€ ÷ 2 = 25€",
    "paso_5": "✅ Vigentes",
    "paso_6": "..."
  },
  "trampa_pedagogica": "Error típico: confundir 60% con 75%"
}
```

### Prompt Verificador (5 Agentes):

```markdown
# Eres Inspector Jurídico SS - Valida casos examen

## CASO PARA VERIFICAR:
[INSERT_CASO_JSON]

## VALIDA (score 0-1):

### Agent 1: BOE Verifier
- ¿Artículos existen en TRLGSS? (tool: search_boe)
- ¿Vigentes en 02/02/2026? 
- ¿Sin derogaciones?
→ Score: articulos_vigentes / total_articulos

### Agent 2: Legal Reasoner
- ¿Subsunción correcta? (hechos → artículos)
- ¿Lógica jurídica válida?
- ¿Cita exacta del artículo?
→ Score: coherencia_logica × tiene_referencias

### Agent 3: Calculator
- Ejecutar: calculos_ss_extended.py
- Verificar cada paso
- Precisión Decimal (no float)
→ Score: calculo_correcto (0 o 1)

### Agent 4: Coherence
- ¿Fechas coherentes? (no futuro, lógica temporal)
- ¿Datos consistentes? (no contradicciones)
- ¿Números realistas?
→ Score: coherencia_general

### Agent 5: Trap Pedagogy
- ¿Trampa basada en error real?
- ¿Educativa? (enseña concepto)
- ¿Sutil? (no obvia)
→ Score: realismo_trampa × valor_educativo
```

---

## 🔌 MCPs NECESARIOS (Estado actual)

### MCP 1: BOE Search ✅ (LISTO crear)
```yaml
mcp-boe:
  type: "http"
  url: "https://api.boe.es/buscar"
  methods:
    - search_articles(ley, articulo)
    - get_vigencia(articulo, fecha)
    - get_derogaciones(articulo)
```

### MCP 2: Qdrant RAG ✅ (LISTO conectar)
```yaml
mcp-qdrant:
  type: "local"
  url: "http://localhost:6333"
  collections:
    - opositaia_knowledge_FULL_XML (12,090 vectores)
    - opositaia_leyes_master (conocimiento BOE)
  methods:
    - search(query, collection, limit=5)
```

### MCP 3: SQLite Leyes ✅ (LISTO crear)
```yaml
mcp-leyes:
  type: "local_db"
  db: "backend/data/leyes_master.db"
  tables:
    - articulos (numero, ley, texto, vigencia_inicio, vigencia_fin)
    - derogaciones (articulo_origen, articulo_derogatorio)
  methods:
    - get_articulo(numero)
    - check_vigencia(numero, fecha)
```

---

## 🤖 SALAMANDRA R1 - CONEXIÓN REAL

### Estado actual:
```bash
✅ Ollama running: http://localhost:11434
✅ Modelo: salamandra-r1:q5km (verificado)
```

### Integración necesaria:

```python
import requests

def generar_caso_salamandra(tema: str, prompt_sistema: str) -> Dict:
    """Genera caso usando Salamandra R1 local"""
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "salamandra-r1:q5km",
            "system": prompt_sistema,
            "prompt": f"Genera 1 caso práctico SS: {tema}",
            "stream": False,
            "temperature": 0.3,  # Determinístico
            "top_p": 0.9,
            "num_ctx": 4096,
        },
        timeout=300
    )
    
    resultado_raw = response.json()["response"]
    
    # Parser JSON robustizado
    try:
        return json.loads(resultado_raw)
    except:
        return {"error": "Parser JSON fallido", "raw": resultado_raw}
```

---

## ✅ VALIDACIÓN DE LÓGICA LEGAL

### ¿Quién la valida? 5 Agentes en paralelo:

1. **BOE Verifier**: Normativa vigente
2. **Legal Reasoner**: Subsunción jurídica
3. **Calculator**: Exactitud numérica
4. **Coherence**: Consistencia datos
5. **Trap Pedagogy**: Valor educativo

### Cada agente:
- Recibe caso JSON
- Ejecuta verificaciones
- Retorna score 0-1 + feedback
- Score promedio = confianza sistema

**Umbral aprobación**: ≥ 0.80 en promedio (80 puntos)

---

## 🎯 CASO REAL COMPLETO (PARA HOY)

### Plan:
1. **Conectar Salamandra** → generar 1 caso
2. **Consultar BOE real** (via MCP o API)
3. **Verificar con 5 agentes**
4. **Output**: caso_real_verificado.json

### Ejemplo esperado:

```json
{
  "id": "SS_IT_001_SALAMANDRA_20260213",
  "generado_por": "salamandra-r1:q5km",
  "timestamp": "2026-02-13T19:30:00Z",
  "caso": {
    "tema": "subsidio_it",
    "enunciado": "Trabajador José García, baja EC 10-25 feb. Base 1500€...",
    "pregunta": "¿Subsidio día 15?",
    "opciones": {...},
    "respuesta_correcta": "C"
  },
  "verificacion": {
    "agent_1_boe": 0.95,
    "agent_2_legal": 0.88,
    "agent_3_calculator": 1.0,
    "agent_4_coherence": 0.92,
    "agent_5_pedagogy": 0.85,
    "score_promedio": 0.92,
    "status": "APROBADO ✅"
  }
}
```

---

## 📌 SIGUIENTE PASO

¿Hago YA el caso real con Salamandra o primero:
1. **Crear MCPs** (BOE + Qdrant + Leyes DB)
2. **Conectar Salamandra**
3. **Generar 1 caso real**

?
