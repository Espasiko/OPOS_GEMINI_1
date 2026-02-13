
# 🗺️ PLAN MAESTRO DE MEJORA DATASET v12 (Genspark Enhanced)

**Estado:** 🟢 PLANIFICACIÓN DE ALTO NIVEL
**Objetivo:** Crear el **Dataset v12 "PLATINUM"** (2,500 - 3,000 items) para Fine-Tuning de Salamandra 7B con QLoRA.
**Filosofía:** "Veracidad Absoluta (0% Alucinaciones) y Razonamiento Legal de Nivel Experto (Claude 3.5 Level)."

---

## 1. 🧬 ADN del Dataset v12

Siguiendo el **Genspark Plan 2026**, el dataset no es solo una lista de preguntas; es una arquitectura de conocimiento equilibrada.

### 📊 Distribución Estratégica (The Golden Ratio)
Debemos asegurar esta composición exacta para evitar sesgos y maximizar el razonamiento:

| Tipo de Item | % del Dataset | Cantidad (~2500) | Objetivo Pedagógico | Dificultad |
| :--- | :---: | :---: | :--- | :--- |
| **🎓 Aplicación Directa** | **40%** | 1,000 | Precisión en citas y plazos (Memoria Factual) | Básico |
| **🧠 Casos Prácticos** | **35%** | 875 | Razonamiento multi-variable y lógica jurídica (CoT) | Alto |
| **❌ Trampas / Negativos** | **15%** | 375 | Detección de errores y "Edge Cases" (Anti-Hallucination) | Medio |
| **⚖️ Comparación Normas** | **10%** | 250 | Análisis contrastado (e.g., Silencio Positivo vs Negativo) | Experto |

### ⚖️ Balance Temático (50/50)
El modelo no debe olvidar la Administración General del Estado (AGE) por centrarse en Seguridad Social.

*   **50% Seguridad Social:** Prestaciones, Cotización, Afiliación, Infracciones.
*   **50% AGE:** Constitución, Ley 39/2015 (Procedimiento), Ley 40/2015, TREBEP.

---

## 2. 🛠️ Ingeniería de Prompts (Chain of Thought Legal)

Cada item generado debe seguir rigurosamente estos templates para enseñar al modelo a **pensar**, no solo a predecir tokens.

### A. Estructura de Razonamiento (CoT)
El campo `explanation` o `reasoning` del dataset debe estructurarse así:

```markdown
### 1. Marco Normativo
[Citas textuales del BOE: Ley + Art. + Núm. BOE]

### 2. Análisis del Supuesto de Hecho
[Desglose de variables clave: Fechas, Requisitos, Excepciones]

### 3. Cadena Lógica (Chain of Thought)
- Premisa Mayor: La ley X exige Y.
- Premisa Menor: El sujeto Z cumple Y.
- Subsunción: Por tanto, se aplica la consecuencia W.

### 4. Conclusión Fundamentada
[Respuesta final inequívoca]
```

### B. Protocolo Anti-Alucinación (Prompt Defensivo)
En el entrenamiento, penalizaremos severamente la invención de datos.
*   **Prompt System:** *"Si NO conoces el dato con 100% certeza o falta contexto, responde: 'Necesito consultar fuentes actualizadas'. NUNCA inventes artículos."*
*   **Items Negativos:** Incluiremos preguntas sobre leyes inexistentes (e.g., "Ley de Ciberseguridad Social de 1990") donde la respuesta correcta sea **identificar el error**.

---

## 3. 🛡️ Pipeline de Validación: "La Muralla de Calidad"

No entra ni un solo item al dataset v12 sin pasar por este filtro de 3 Capas.

### Capa 1: Validación Automática (RAG Check)
*   **Motor:** Qdrant + RoBERTalex (Embeddings Legales).
*   **Logic:** Para cada pregunta generada, recuperamos el chunk del BOE. Si la similitud semántica < 0.85, el item se **descarta**.

### Capa 2: Detección de Contradicciones
*   Usar un LLM juez (Gemini 2.5 Flash / Claude 3.5) para verificar:
    *   ¿La opción correcta (A) coincide con la explicación?
    *   ¿La cita legal (Art. X) existe realmente en el texto de la ley?

### Capa 3: Revisión Manual (Muestreo Estratégico)
*   Revisión humana del **10% de los Casos Prácticos** (los más propensos a errores sutiles).
*   Revisión del **100% de los Items Comparativos**.

---

## 4. 🚀 Hoja de Ruta de Ejecución (Sin Código Nuevo)

Como la orden es **NO EJECUTAR CÓDIGO AHORA**, este es el plan para cuando se levante el bloqueo:

1.  **Frenar Scripts Actuales:** Detener el script `generate_platinum_supplement.py` (PID 2499005) si su calidad no cumple con el nuevo estándar "Genspark" (probablemente le falte el balance 50/50 y los items negativos).
2.  **Auditoría del Dataset Actual (v12 Platinum):**
    *   Analizar cuántos items tenemos de cada categoría (Casos vs Directos).
    *   Verificar el balance SS vs AGE.
3.  **Generación Quirúrgica:**
    *   No generar "a bulto". Generar específicamente lo que falte para cumplir el **Ratio Dorado** (ej. "Faltan 200 items de TRAMPAS sobre Ley 39/2015").
4.  **Fusión Final:** Crear `MASTER_DATASET_v13_DIAMOND.jsonl` solo con lo verificado.

---

> **Nota del Arquitecto:** Este dataset v12 no solo servirá para fine-tuning; será la "memoria a largo plazo" de Salamandra, evitando el Catastrophic Forgetting mediante la inclusión estratégica de conceptos generales (AGE) junto con la especialización (SS).
