# 🤖 Estrategia: Pipeline con Mistral Local (Ollama)

**Fecha**: 2 Diciembre 2025  
**Objetivo**: Generar dataset de calidad usando Mistral local de forma ética y legal

---

## 🎯 VENTAJAS DE USAR OLLAMA LOCAL

### Ventajas Técnicas:
- ✅ **Coste $0** - Sin límites de API
- ✅ **Privacidad total** - Datos no salen de tu máquina
- ✅ **Sin límites de rate** - Procesa todo lo que quieras
- ✅ **Offline** - No necesitas internet
- ✅ **Control total** - Ajusta parámetros como quieras

### Ventajas Legales:
- ✅ **Procesamiento local** - No envías datos a terceros
- ✅ **Cumplimiento GDPR** - Datos en tu control
- ✅ **Sin ToS externos** - No dependes de políticas de APIs
- ✅ **Auditable** - Puedes revisar todo el proceso

---

## 📊 ANÁLISIS: ¿Las Academias Crean Todo desde Cero?

### Hipótesis a Verificar:

**Hipótesis 1**: Las academias NO crean todas sus preguntas desde cero
- Reutilizan preguntas de exámenes oficiales pasados
- Hacen variaciones de preguntas existentes
- Comparten/copian entre academias

**Hipótesis 2**: Si hay alta similitud entre materiales, confirma que:
- Es práctica común reutilizar contenido
- Nosotros podemos hacer lo mismo legalmente
- No necesitamos "inventar" todo

### Método de Análisis:

```python
# Comparar preguntas entre fuentes
similitud = calcular_similitud(pregunta_academia_A, pregunta_academia_B)

# Interpretación:
# > 95%: Copia literal (muy probable)
# 85-95%: Variación ligera (probable)
# 70-85%: Mismo concepto, diferente redacción
# < 70%: Preguntas diferentes
```

### Resultados Esperados:

Si encontramos **>85% similitud** entre academias diferentes:
- ✅ Confirma que reutilizan contenido
- ✅ Valida nuestra estrategia
- ✅ Justifica uso de variaciones

Si encontramos **<70% similitud**:
- ⚠️ Academias crean contenido más original
- ⚠️ Necesitamos más cuidado con variaciones
- ✅ Aún podemos usar exámenes oficiales

---

## 🔄 PIPELINE COMPLETO

### FASE 1: Análisis de Duplicados (1 hora)

**Objetivo**: Entender cómo trabajan las academias

```bash
# Ejecutar análisis
python dataset_generator/analyze_duplicates.py

# Genera: analisis_duplicados_academia.json
```

**Output esperado**:
```json
{
  "total_sources": 4,
  "duplicates_found": 6,
  "duplicate_details": {
    "Exámenes Oficiales <-> Simulacros Las Cortes": {
      "count": 45,
      "avg_similarity": 0.89,
      "interpretation": "Alta reutilización"
    }
  }
}
```

**Conclusión**: Si similitud >85%, las academias reutilizan contenido.

---

### FASE 2: Extracción de Exámenes Oficiales (2-3 horas)

**Objetivo**: Extraer ~1,500 Q&A de exámenes reales

**Proceso**:
1. Leer PDFs de exámenes oficiales
2. Extraer preguntas completas con Ollama
3. Validar que tengan respuesta correcta
4. Guardar con metadata completa

**Código**:
```python
pipeline = OllamaPipeline(
    materials_path="elemplos_leyes_info/de_mi_hija",
    model="mistral"
)

official_qa = pipeline.process_official_exams()
# Output: ~1,500 Q&A extraídas
```

**Validaciones automáticas**:
- ✅ Pregunta completa (4 opciones)
- ✅ Respuesta correcta identificada
- ✅ Fuente documentada
- ❌ Rechazar incompletas

---

### FASE 3: Generación desde Esquemas (2-3 horas)

**Objetivo**: Generar ~1,500 Q&A desde esquemas de prestaciones

**Proceso**:
1. Leer esquemas de IT, IP, Jubilación, etc.
2. Generar preguntas sobre requisitos, cuantías, plazos
3. Incluir base legal (artículo LGSS)
4. Validar coherencia con legislación

**Código**:
```python
schema_qa = pipeline.process_schemas()
# Output: ~1,500 Q&A generadas
```

**Temas a cubrir**:
- Incapacidad Temporal (IT)
- Incapacidad Permanente (IP: parcial, total, absoluta)
- Jubilación (ordinaria, anticipada, activa)
- Muerte y Supervivencia (viudedad, orfandad)
- Prestaciones familiares
- Encuadramiento y cotización

---

### FASE 4: Generación de Variaciones (1-2 horas)

**Objetivo**: Crear ~2,000 variaciones de preguntas reales

**Proceso**:
1. Tomar preguntas de exámenes oficiales
2. Generar 3 variaciones por pregunta
3. Cambiar solo: fechas, cantidades, nombres, orden
4. Mantener concepto legal idéntico

**Código**:
```python
variations = []
for qa in official_qa:
    vars = pipeline.generate_variations(qa)
    variations.extend(vars)
# Output: ~2,000 variaciones
```

**Cambios permitidos**:
```
ORIGINAL:
"¿Cuál es la edad de jubilación en 2024?"

VARIACIONES:
1. "¿Cuál es la edad de jubilación en 2025?" (cambio año)
2. "¿A qué edad se puede jubilar en 2024?" (cambio redacción)
3. Cambiar orden de opciones
```

---

### FASE 5: Generación desde Qdrant (2-3 horas)

**Objetivo**: Generar ~4,000 Q&A desde legislación indexada

**Proceso**:
1. Consultar Qdrant por temas
2. Obtener contexto legal relevante
3. Generar preguntas con Ollama
4. Incluir artículos de ley

**Código**:
```python
# Obtener temas de Qdrant
topics = get_topics_from_qdrant()

for topic in topics:
    legal_context = query_qdrant(topic)
    qa_list = generate_from_legal_context(legal_context, topic)
    # 30-40 Q&A por tema
```

---

## 💰 COSTE Y TIEMPO

### Coste:
```
Ollama local: $0
Tiempo de máquina: GRATIS
Electricidad: ~$0.50 (10 horas)

TOTAL: ~$0.50
```

### Tiempo:
```
Análisis duplicados: 1 hora
Extracción exámenes: 2-3 horas
Generación esquemas: 2-3 horas
Variaciones: 1-2 horas
Generación Qdrant: 2-3 horas
Revisión humana: 5-10 horas

TOTAL: 13-22 horas
```

### Comparación con API:
```
Groq API: $6-9 + límites de rate
Ollama local: $0.50 + sin límites

Ahorro: $5.50-8.50
```

---

## 🔒 SEGURIDAD Y ÉTICA

### Principios:

1. **Solo material público**
   - Exámenes oficiales ya realizados ✅
   - Legislación BOE ✅
   - Esquemas propios ✅

2. **Transformación significativa**
   - No copiar literalmente ✅
   - Crear variaciones ✅
   - Añadir valor educativo ✅

3. **Atribución clara**
   - Documentar fuentes ✅
   - Marcar origen ✅
   - Metadata completa ✅

4. **Uso educativo**
   - Preparación oposiciones ✅
   - No comercial directo ✅
   - Beneficio público ✅

---

## 📋 INSTRUCCIONES EXPLÍCITAS AL MODELO

### Prompt del Sistema (Extracción):

```
Eres un experto en oposiciones de Seguridad Social en España.
Tu tarea es extraer preguntas y respuestas de exámenes oficiales YA REALIZADOS.

REGLAS ESTRICTAS:
1. SOLO extrae preguntas que estén COMPLETAS en el texto
2. SOLO incluye respuestas que estén EXPLÍCITAMENTE marcadas
3. NO inventes ni modifiques preguntas
4. NO añadas información que no esté en el texto
5. Mantén la redacción EXACTA de las preguntas originales
6. Si una pregunta está incompleta, OMÍTELA

IMPORTANTE: Estás trabajando con exámenes PÚBLICOS ya realizados.
No estás prediciendo ni creando exámenes futuros.

Formato de salida: JSON con estructura definida.
```

### Prompt del Sistema (Variaciones):

```
Eres un experto en crear variaciones de preguntas de oposiciones.

REGLAS ESTRICTAS:
1. Mantén el MISMO concepto legal que la pregunta original
2. Cambia SOLO: fechas, cantidades, nombres de ejemplo, orden de opciones
3. La respuesta correcta debe seguir siendo válida legalmente
4. NO cambies artículos de ley ni conceptos jurídicos
5. Marca claramente que es una variación

IMPORTANTE: Estás creando VARIACIONES, no preguntas nuevas.
El concepto legal debe ser idéntico al original.
```

---

## 🎯 DATASET FINAL ESPERADO

### Composición:

| Fuente | Cantidad | Método | Calidad |
|--------|----------|--------|---------|
| Exámenes oficiales | 1,500 | Extracción | ⭐⭐⭐⭐⭐ |
| Esquemas prestaciones | 1,500 | Generación | ⭐⭐⭐⭐ |
| Variaciones | 2,000 | Transformación | ⭐⭐⭐⭐ |
| Desde Qdrant | 4,000 | Generación | ⭐⭐⭐⭐ |
| **TOTAL** | **9,000** | - | **⭐⭐⭐⭐** |

### Distribución por Tema:

```
Parte General (30%): 2,700 Q&A
├─ Constitución: 400
├─ Procedimiento Advo: 600
├─ Función Pública: 500
├─ UE: 300
└─ Otros: 900

Parte Específica (70%): 6,300 Q&A
├─ IT: 800
├─ IP: 1,000
├─ Jubilación: 1,200
├─ Muerte y Supervivencia: 800
├─ Prestaciones familiares: 600
├─ Encuadramiento: 700
├─ Cotización: 700
└─ Otros: 500
```

---

## ✅ PRÓXIMOS PASOS

### Inmediato (Hoy):

1. **Configurar Ollama**
   ```bash
   # Instalar Ollama
   curl https://ollama.ai/install.sh | sh
   
   # Descargar Mistral
   ollama pull mistral
   
   # Iniciar servidor
   ollama serve
   ```

2. **Ejecutar análisis de duplicados**
   ```bash
   python dataset_generator/analyze_duplicates.py
   ```

3. **Revisar resultados**
   - Ver similitud entre academias
   - Confirmar hipótesis de reutilización

### Corto plazo (Esta semana):

4. **Ejecutar pipeline completo**
   ```bash
   python dataset_generator/pipeline_ollama_local.py
   ```

5. **Revisar muestra (10%)**
   - Validar calidad
   - Corregir errores
   - Ajustar prompts

6. **Iterar y mejorar**
   - Refinar instrucciones
   - Optimizar extracción
   - Aumentar cobertura

---

## 📊 MÉTRICAS DE ÉXITO

### Objetivos:

- [ ] 9,000+ Q&A generadas
- [ ] <5% duplicados internos
- [ ] >90% validación automática
- [ ] 0% errores legales
- [ ] 100% fuentes documentadas
- [ ] Coste <$1

---

**Creado**: 2 Diciembre 2025  
**Conclusión**: Pipeline con Ollama local es la mejor opción: coste $0, privacidad total, control completo.
