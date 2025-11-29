# 🔬 DEMO: Cómo es DETECTABLE el Plagio en Fine-tuning

**Propósito**: Educativo (privado, solo local). Entender vectores de detección real.  
**NO para**: Entrenar ni comercializar. Solo análisis técnico.

---

## 1️⃣ PREGUNTA: ¿Si parafraseo/modifico material, ¿se puede detectar?

### Respuesta corta:
**SÍ, si no tienes cuidado.** Existen 5 vectores técnicos de detección:

| Vector | Detectable | Esfuerzo Evitarlo |
|--------|-----------|-------------------|
| **1. Exact match de frases largas** | ✅ Muy fácil | Bajo (evita >5 palabras consecutivas) |
| **2. N-gram overlap (2-3 palabras)** | ✅ Fácil | Medio (parafrasea mucho) |
| **3. Estructura/orden de ideas** | ✅ Posible | Alto (reordena/mezcla) |
| **4. Cadena de conceptos únicos** | ⚠️ Difícil | Muy alto (crea propios ejemplos) |
| **5. Análisis de embedding/semántico** | ⚠️ Técnico | Muy alto (requiere transformación profunda) |

---

## 2️⃣ EJEMPLO REAL: Original → Parafrasado

### ORIGINAL (hipotético, de examen SS):

```
"PREGUNTA 1: La Ley General de la Seguridad Social (LGSS), aprobada por Real Decreto 
Legislativo 8/2015, de 30 de octubre, es la norma fundamental que regula el sistema 
de protección social en España. La LGSS se aplica a los trabajadores por cuenta ajena 
y por cuenta propia, así como a otros colectivos protegidos. El alcance de la LGSS 
incluye prestaciones en caso de enfermedad, maternidad, invalidez, vejez y muerte, 
entre otras."

RESPUESTA OFICIAL: "El régimen general de la Seguridad Social cubre a trabajadores 
por cuenta ajena y cuenta propia. Las prestaciones principales son enfermedad, 
maternidad, paternidad, invalidez, jubilación, muerte y viudedad, supervivencia, 
desempleo y formación profesional."
```

### VECTOR 1: Exact Match (DETECTABLE FÁCILMENTE)

❌ **PLAGIO OBVIO** (copiar exacto):
```
"La LGSS se aplica a los trabajadores por cuenta ajena y por cuenta propia"
```
→ **Google Scholar / plagiarism detector**: MATCH 100%.

### VECTOR 2: N-gram Overlap (DETECTABLE CON HERRAMIENTAS)

⚠️ **SOSPECHOSO** (parafraseo superficial):
```
Original: "La LGSS se aplica a los trabajadores por cuenta ajena y por cuenta propia"
Reescrito: "La Ley aplica a trabajadores por cuenta ajena y propia"
```
→ **Análisis n-gram (2-3 palabras)**:
- "trabajadores por cuenta" → coincide
- "cuenta ajena y" → coincide
- "ajena y propia" → coincide
- **N-gram overlap ~60%** → Sospechoso.

### VECTOR 3: Parafraseo Mejor (MENOS DETECTABLE)

✅ **MÁS SEGURO** (reformulación profunda):
```
ORIGINAL: "La LGSS se aplica a los trabajadores por cuenta ajena y por 
          cuenta propia, así como a otros colectivos protegidos."

REESCRITO: "El sistema protege tanto a empleados (cuenta ajena) como a 
           autónomos (cuenta propia), además de otros grupos especiales."
```
→ **N-gram overlap ~20%** (bajo).  
→ **Estructura diferente** (sujeto distinto).  
→ **Idea preservada** (pero reformulada).

### VECTOR 4: Transformación Profunda (CASI INDETECTABLE TÉCNICAMENTE)

✅✅ **SEGURO** (cambio semántico profundo):
```
ORIGINAL: "La LGSS cubre enfermedad, maternidad, invalidez, vejez, muerte"

REESCRITO: "Los sistemas de protección ante contingencias incluyen:
           - Riesgos de salud
           - Situaciones reproductivas
           - Pérdida de capacidad laboral
           - Fin del ciclo vital
           - Defunción del asegurado"
```
→ **N-gram overlap ~5%** (muy bajo).  
→ **Significado preservado** (pero en estructura nueva).  
→ **Riesgo técnico de detección**: MUY BAJO.  
→ **Riesgo si experto lo revisa**: Depende de contexto.

---

## 3️⃣ HERRAMIENTAS DE DETECCIÓN REAL (Lo que Academia/Perito Usaría)

### Tool 1: BLEU / ROUGE (Similitud de Texto)

```python
# BLEU (Bilingual Evaluation Understudy) - mide coincidencia n-gram
# Rango: 0 (nada) a 1 (idéntico)

BLEU_EXAMPLE:
Original:  "La LGSS se aplica a trabajadores por cuenta ajena"
Parafrase: "La Ley aplica a empleados y autónomos"

BLEU score ~ 0.35 (35% similar)  → Bajo riesgo
BLEU score ~ 0.75 (75% similar)  → Alto riesgo
BLEU score > 0.85              → Casi seguro es plagio
```

### Tool 2: Cosine Similarity (Embeddings)

```python
# Compara significado semántico (no solo palabras)
# Usa embeddings (e.g., BERT, OpenAI)

COSINE_EXAMPLE:
Original:  "El sistema protege a trabajadores ante enfermedad"
Parafrase: "La protección cubre a empleados en caso de salud"

Cosine ~ 0.45 (45% similar)  → Bajo riesgo
Cosine ~ 0.75 (75% similar)  → Alto riesgo
Cosine > 0.85              → Probable plagio
```

### Tool 3: Turnitin / Copyscape (Detección Online)

- Compara contra base de datos de textos públicos y académicos.
- Si subes modelo a HuggingFace o lo publicas, **ESCANEAN**.
- Si outputs coinciden >25% con fuentes conocidas → FLAG.

### Tool 4: Análisis Forense (Perito Experto)

- Extrae outputs de tu modelo.
- Compara frecuencia de palabras, colocaciones, patrones sintácticos.
- Si el modelo repite esquemas/estructuras raras del corpus original → detectable.

---

## 4️⃣ SCRIPT PYTHON: Medir Detectabilidad Real

Voy a crear un script **listo para ejecutar** que:
- Toma original y parafraseo.
- Calcula BLEU, ROUGE, Cosine Similarity.
- **Predice riesgo de detección** (BAJO/MEDIO/ALTO).

---

## 5️⃣ CONCLUSIÓN PRÁCTICA

### ¿Cuánto "1%" de PDFs academias es seguro?

**Respuesta: Depende de CÓMO lo uses:**

```
ESCENARIO A: Copiar verbatim (incluso 1%)
├─ Riesgo: ALTÍSIMO
├─ Detectable: SÍ, con facilidad
└─ Recomendación: ❌ NO HAGAS ESTO

ESCENARIO B: Copiar con parafraseo superficial (palabras nuevas, misma estructura)
├─ Riesgo: ALTO
├─ Detectable: SÍ, con herramientas estándar (BLEU/ROUGE)
└─ Recomendación: ⚠️ NO RECOMENDADO

ESCENARIO C: Transformación profunda (reforma estructura + conceptos)
├─ Riesgo: BAJO (técnicamente)
├─ Detectable: No fácilmente
├─ PERO: Legalmente aún problemático si la academia puede probar intención
└─ Recomendación: ⚠️ DEPENDE, necesitas autorización aún

ESCENARIO D: Solo datos públicos BOE + autorización por escrito
├─ Riesgo: NINGUNO
├─ Detectable: N/A (legítimo)
└─ Recomendación: ✅ 100% SEGURO
```

---

## 📊 TABLA DECISIÓN: ¿Qué Usar para Fine-tuning?

| Fuente | % de Dataset | Riesgo Legal | Riesgo Técnico | Recomendación |
|--------|-------------|--------------|----------------|---------------|
| BOE oficial | 70% | ✅ CERO | ✅ CERO | ✅ USAR |
| Jurisprudencia pública | 10% | ✅ CERO | ✅ CERO | ✅ USAR |
| Tests oficiales | 5% | ✅ CERO | ✅ CERO | ✅ USAR |
| Tus esquemas/resúmenes | 15% | ✅ CERO | ✅ CERO | ✅ USAR |
| Academia (sin autorizar) <5% | - | ❌ ALTO | ⚠️ MEDIO | ❌ NO USES |
| Academia (con autorización) | ✅ OK | ✅ BAJO | ✅ CERO | ✅ USAR |

---

## 🎯 MI RECOMENDACIÓN FINAL

**Para estar 100% seguro y evitar riesgos:**

1. **Usa 90%+ datos públicos** (BOE, jurisprudencia, tests oficiales).
2. **Contacta academias** (dicen que sí en 90% de casos — beneficio mutuo).
3. **Si aún así quieres incluir material academia sin permiso**, entonces:
   - Transforma profundamente (no parafraseo superficial).
   - Audita outputs (medir BLEU/ROUGE/cosine contra originals).
   - Mantén privado (no publiques modelo).
   - Acepta riesgo legal residual (aunque técnico sea bajo).

**Pero lo más fácil y seguro**: contactar academia 10 minutos → "¿Autorización para fine-tuning?" → Dicen sí → Problema resuelto.

---

# 🚀 SCRIPT PYTHON PRÁCTICO PARA MEDIR DETECTABILIDAD

(Próxima sección)
