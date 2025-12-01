# 📋 Esquema de Metadata para Dataset Q&A

**Fecha**: 1 Diciembre 2025  
**Formato**: JSONL (JSON Lines)

---

## 🎯 Campos del Esquema

### **Campos Obligatorios:**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `id` | String | Identificador único | `"qa_00001"` |
| `question` | String | Texto de la pregunta | `"¿Qué es la LGSS?"` |
| `answer` | String | Texto de la respuesta | `"La Ley General..."` |
| `source_document` | String | Documento origen | `"lgss_2024.txt"` |
| `content_type` | Enum | Tipo de contenido | `"normativa"` |
| `risk_level` | Enum | Nivel de riesgo | `"high"` |
| `generated_by` | String | Modelo generador | `"groq-llama-3.1-70b"` |
| `created_at` | Date | Fecha creación | `"2025-12-01"` |
| `version` | String | Versión del dataset | `"1"` |

### **Campos de Verificación:**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `verified_by_ia` | Boolean | Verificado por IA | `true` |
| `verified_by_human` | Boolean | Revisado por humano | `true` |
| `human_reviewer` | String | ID del revisor | `"juan_experto_ss"` |
| `review_date` | Date | Fecha de revisión | `"2025-12-01"` |
| `review_notes` | String | Notas del revisor | `"Verificado art. 205"` |
| `final_status` | Enum | Estado final | `"accepted"` |

### **Campos Opcionales:**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `source_location` | String | Ubicación en documento | `"Art. 205, pág. 45"` |
| `difficulty_level` | Enum | Nivel de dificultad | `"medium"` |
| `last_modified` | Date | Última modificación | `"2025-12-01"` |
| `tags` | Array[String] | Etiquetas | `["jubilación","cálculo"]` |
| `notes` | String | Notas adicionales | `"Revisar en 2026"` |
| `referencia` | String | Referencia legal | `"Art. 205.1.a) LGSS"` |
| `complexity` | Enum | Complejidad técnica | `"complex"` |
| `confidence` | Float | Confianza IA (0-1) | `0.92` |
| `needs_human_review` | Boolean | Requiere revisión | `true` |
| `review_priority` | Enum | Prioridad revisión | `"critical"` |
| `verification_issues` | Array[String] | Problemas detectados | `["referencia ambigua"]` |

---

## 📝 Valores Permitidos (Enums)

### **content_type:**
- `"definicion"` - Definiciones básicas
- `"normativa"` - Leyes, artículos, RD
- `"jurisprudencia"` - Sentencias, TS
- `"calculo_legal"` - Bases, cuantías
- `"caso_practico"` - Supuestos complejos
- `"caso_practico_complejo"` - Casos multi-paso
- `"test_multiple_choice"` - Opciones a/b/c/d
- `"procedimiento"` - Trámites
- `"explicacion"` - Explicaciones largas
- `"resumen"` - Resúmenes normativos
- `"general"` - Otros

### **risk_level:**
- `"high"` - Alto riesgo (normativa, leyes, jurisprudencia)
- `"medium"` - Medio riesgo (procedimientos)
- `"low"` - Bajo riesgo (definiciones)

### **difficulty_level:**
- `"easy"` - Fácil
- `"medium"` - Medio
- `"hard"` - Difícil

### **final_status:**
- `"accepted"` - Aceptada
- `"rejected"` - Rechazada
- `"needs_review"` - Necesita revisión
- `"modified"` - Modificada

### **review_priority:**
- `"critical"` - Crítica (revisar inmediatamente)
- `"high"` - Alta
- `"medium"` - Media
- `"low"` - Baja

---

## 📄 Ejemplo Completo JSONL

```jsonl
{"id":"qa_00001","question":"¿Cuál es la edad ordinaria de jubilación en 2024?","answer":"La edad ordinaria de jubilación en 2024 es de 66 años y 6 meses, según el artículo 205.1.a) de la LGSS. Esta edad se incrementa progresivamente hasta alcanzar los 67 años en 2027.","source_document":"lgss_2024.txt","source_location":"Art. 205.1.a), pág. 142","content_type":"normativa","difficulty_level":"medium","risk_level":"high","generated_by":"groq-llama-3.1-70b","verified_by_ia":true,"verified_by_human":true,"human_reviewer":"juan_experto_ss","review_date":"2025-12-01","review_notes":"Verificado con LGSS actualizada 2024","final_status":"accepted","version":"1","created_at":"2025-12-01","last_modified":"2025-12-01","tags":["jubilación","edad","LGSS"],"referencia":"Art. 205.1.a) LGSS","complexity":"simple","confidence":0.95,"needs_human_review":true,"review_priority":"critical","verification_issues":[],"notes":"Actualizar cuando cambie normativa"}

{"id":"qa_00002","question":"¿Qué es la base reguladora?","answer":"La base reguladora es la cantidad que se utiliza como referencia para calcular el importe de las prestaciones de la Seguridad Social, como pensiones o subsidios.","source_document":"conceptos_basicos.txt","source_location":"Sección 2.3","content_type":"definicion","difficulty_level":"easy","risk_level":"low","generated_by":"groq-llama-3.1-70b","verified_by_ia":true,"verified_by_human":false,"human_reviewer":null,"review_date":"2025-12-01","review_notes":"","final_status":"accepted","version":"1","created_at":"2025-12-01","last_modified":"2025-12-01","tags":["definición","base reguladora","prestaciones"],"referencia":"","complexity":"simple","confidence":0.88,"needs_human_review":false,"review_priority":"low","verification_issues":[],"notes":""}

{"id":"qa_00003","question":"Supuesto: Un trabajador con 35 años cotizados y 63 años solicita jubilación anticipada. ¿Cumple requisitos?","answer":"Sí, cumple los requisitos mínimos. Según el art. 207 LGSS, para jubilación anticipada voluntaria se requieren al menos 35 años cotizados y tener entre 63-65 años. Sin embargo, se aplicará un coeficiente reductor a la pensión.","source_document":"lgss_2024.txt","source_location":"Art. 207","content_type":"caso_practico_complejo","difficulty_level":"hard","risk_level":"high","generated_by":"claude-3.5-sonnet","verified_by_ia":true,"verified_by_human":true,"human_reviewer":"maria_experta","review_date":"2025-12-01","review_notes":"Verificado cálculo de coeficiente reductor","final_status":"accepted","version":"1","created_at":"2025-12-01","last_modified":"2025-12-01","tags":["jubilación anticipada","caso práctico","cálculo"],"referencia":"Art. 207 LGSS","complexity":"complex","confidence":0.92,"needs_human_review":true,"review_priority":"critical","verification_issues":[],"notes":"Revisar coeficientes reductores actualizados"}
```

---

## 🔧 Ventajas del Formato JSONL

### **1. Procesamiento Eficiente:**
```python
# Leer línea por línea (eficiente para datasets grandes)
with open('dataset.jsonl', 'r') as f:
    for line in f:
        qa = json.loads(line)
        process(qa)
```

### **2. Append Fácil:**
```python
# Añadir nuevas Q&A sin reescribir todo
with open('dataset.jsonl', 'a') as f:
    f.write(json.dumps(new_qa) + '\n')
```

### **3. Filtrado Rápido:**
```python
# Filtrar por riesgo alto
high_risk = [json.loads(line) for line in open('dataset.jsonl') 
             if json.loads(line)['risk_level'] == 'high']
```

### **4. Compatible con Herramientas:**
- Pandas: `pd.read_json('dataset.jsonl', lines=True)`
- jq: `cat dataset.jsonl | jq '.[] | select(.risk_level == "high")'`
- Streaming: Procesa archivos gigantes sin cargar en memoria

---

## 📊 Trazabilidad Completa

### **Ciclo de Vida de una Q&A:**

```
1. GENERACIÓN
   ├─ id: "qa_00001"
   ├─ generated_by: "groq-llama-3.1-70b"
   ├─ created_at: "2025-12-01"
   ├─ risk_level: "high"
   └─ needs_human_review: true

2. VERIFICACIÓN IA
   ├─ verified_by_ia: true
   ├─ confidence: 0.92
   ├─ verification_issues: []
   └─ review_date: "2025-12-01"

3. REVISIÓN HUMANA
   ├─ verified_by_human: true
   ├─ human_reviewer: "juan_experto_ss"
   ├─ review_notes: "Verificado art. 205"
   ├─ final_status: "accepted"
   └─ last_modified: "2025-12-01"

4. AUDITORÍA
   ├─ version: "1"
   ├─ tags: ["jubilación", "LGSS"]
   └─ notes: "Actualizar en 2026"
```

---

## ✅ Buenas Prácticas

### **1. IDs Únicos:**
```python
# Formato recomendado: qa_XXXXX
id = f"qa_{counter:05d}"  # qa_00001, qa_00002, ...
```

### **2. Fechas ISO 8601:**
```python
from datetime import datetime
created_at = datetime.now().strftime("%Y-%m-%d")  # 2025-12-01
```

### **3. Tags Consistentes:**
```python
# Usar minúsculas y guiones
tags = ["jubilación", "edad-ordinaria", "lgss-2024"]
```

### **4. Notas Descriptivas:**
```python
review_notes = "Verificado con LGSS actualizada 2024. Coeficiente reductor correcto."
```

### **5. Versionado:**
```python
# Incrementar cuando actualices normativa
version = "2"  # Nueva versión del dataset
```

---

## 🎯 Uso en el Pipeline

El sistema genera automáticamente este formato:

```bash
# Generar con metadata completa
python generate_qa.py --input data_txt/ --output output/qa_raw.jsonl

# Verificar
python verify_qa.py --input output/qa_raw.jsonl --output output/qa_verified.jsonl

# Revisar
python human_review.py --input output/qa_verified.jsonl --output output/qa_final.jsonl

# Exportar para fine-tuning
python export_dataset.py --input output/qa_final.jsonl --output output/dataset_train.jsonl --split
```

---

## 📚 Referencias

- JSONL Format: https://jsonlines.org/
- Metadata Best Practices: guiasbib.upo.es
- Dataset Reproducibility: arXiv

---

**Creado**: 1 Diciembre 2025  
**Formato**: JSONL  
**Campos**: 25 (9 obligatorios, 16 opcionales)  
**Compatible**: Pandas, jq, streaming

