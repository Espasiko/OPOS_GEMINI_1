# 📖 Guía de Uso - Pipeline de Generación de Dataset

## 🚀 Inicio Rápido

### 1. Instalación

```bash
cd dataset_generator
pip install -r requirements.txt
```

### 2. Configuración

```bash
# Copiar ejemplo de configuración
cp .env.example .env

# Editar .env con tus API keys
nano .env
```

### 3. Ejecutar Pipeline Completo

```bash
# Opción A: Todo automático (desde PDFs)
python run_pipeline.py --input ../elemplos_leyes_info/de_mi_hija/

# Opción B: Si ya tienes textos extraídos
python run_pipeline.py --input data_txt/ --skip-extract

# Opción C: Sin verificación (más rápido, menos calidad)
python run_pipeline.py --input data_txt/ --skip-verify
```

---

## 📋 Uso Paso a Paso

### Paso 1: Extraer Texto de PDFs

```bash
python extract_text.py \
  --input ../elemplos_leyes_info/de_mi_hija/ \
  --output data_txt/ \
  --method pdfplumber
```

**Opciones:**
- `--method pdfplumber`: Más preciso, maneja tablas (recomendado)
- `--method pypdf2`: Más rápido, menos preciso

**Salida:** Archivos `.txt` en `data_txt/`

---

### Paso 2: Generar Q&A

```bash
python generate_qa.py \
  --input data_txt/ \
  --output output/qa_raw.json \
  --config config.json
```

**Qué hace:**
- Divide textos en chunks manejables
- Clasifica complejidad (simple/complejo)
- Usa Groq para contenido simple (70%)
- Usa Claude para contenido complejo (20%)
- Genera 3-5 Q&A por chunk

**Salida:** `output/qa_raw.json` con todas las Q&A generadas

---

### Paso 3: Verificar Calidad

```bash
python verify_qa.py \
  --input output/qa_raw.json \
  --output output/qa_verified.json \
  --config config.json
```

**Qué hace:**
- Verifica longitud y formato
- Usa LLM verificador para evaluar corrección
- Asigna puntuación de confianza
- Filtra Q&A de baja calidad
- Marca Q&A que necesitan revisión humana

**Salida:** `output/qa_verified.json` con Q&A validadas

---

### Paso 4: Exportar para Fine-tuning

```bash
python export_dataset.py \
  --input output/qa_verified.json \
  --output output/dataset_final.jsonl \
  --split \
  --train-ratio 0.8 \
  --val-ratio 0.1
```

**Qué hace:**
- Formatea a formato JSONL (OpenAI/Mistral)
- Divide en train/val/test
- Añade system prompt
- Incluye metadata

**Salida:**
- `dataset_final_train.jsonl` (80%)
- `dataset_final_val.jsonl` (10%)
- `dataset_final_test.jsonl` (10%)

---

## ⚙️ Configuración Avanzada

### Ajustar Modelos

Edita `config.json`:

```json
{
  "models": {
    "generator_simple": {
      "provider": "groq",
      "model": "llama-3.1-70b-versatile",
      "temperature": 0.1
    },
    "generator_complex": {
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20241022",
      "temperature": 0.2
    }
  }
}
```

### Ajustar Clasificación de Complejidad

```json
{
  "complexity_keywords": {
    "simple": ["definición", "concepto", "qué es"],
    "complex": ["caso práctico", "jurisprudencia", "cálculo"]
  }
}
```

### Ajustar Umbrales de Calidad

```json
{
  "quality_thresholds": {
    "min_question_length": 20,
    "max_question_length": 200,
    "min_answer_length": 50,
    "max_answer_length": 500,
    "min_confidence": 0.7
  }
}
```

---

## 💰 Estimación de Costes

### Para 10,000 Q&A:

**Opción 1: Solo Groq (más barato)**
```
Generación: $5-7
Verificación: $2-3
Total: ~$7-10
Calidad: 85-88%
```

**Opción 2: Híbrido Groq + Claude (recomendado)**
```
Generación simple (70%): $5
Generación compleja (20%): $10
Verificación: $2
Total: ~$17
Calidad: 92-95%
```

**Opción 3: Solo Claude (máxima calidad)**
```
Generación: $50-60
Verificación: $3
Total: ~$53-63
Calidad: 96-98%
```

---

## 📊 Métricas de Calidad

El pipeline genera estadísticas automáticas:

```
Estadísticas:
  Total: 10,000
  ✓ Verificadas: 8,500 (85%)
  ⚠ Necesitan revisión: 1,000 (10%)
  ✗ Rechazadas: 500 (5%)

Distribución:
  Simple: 7,000 (70%)
  Complejo: 3,000 (30%)

Confianza promedio: 0.87
```

---

## 🔧 Troubleshooting

### Error: "GROQ_API_KEY not found"

```bash
# Verifica que .env existe y tiene la key
cat .env | grep GROQ_API_KEY

# Si no existe, añádela
echo "GROQ_API_KEY=tu_key_aqui" >> .env
```

### Error: "No se encontraron PDFs"

```bash
# Verifica la ruta
ls -la ../elemplos_leyes_info/de_mi_hija/*.pdf

# Usa ruta absoluta si es necesario
python extract_text.py --input /ruta/completa/a/pdfs --output data_txt/
```

### Calidad baja en Q&A generadas

1. Ajusta `temperature` en `config.json` (más bajo = más determinista)
2. Aumenta `min_confidence` en quality_thresholds
3. Usa Claude para más contenido (ajusta complexity_keywords)

### Verificación muy lenta

```bash
# Salta verificación para pruebas rápidas
python run_pipeline.py --input data_txt/ --skip-verify

# O reduce el dataset de prueba
head -n 100 output/qa_raw.json > output/qa_sample.json
python verify_qa.py --input output/qa_sample.json --output output/qa_verified.json
```

---

## 🎯 Mejores Prácticas

1. **Empieza pequeño**: Prueba con 1-2 PDFs primero
2. **Revisa muestras**: Inspecciona `qa_raw.json` antes de verificar
3. **Ajusta configuración**: Itera en `config.json` según resultados
4. **Revisión humana**: Revisa Q&A marcadas con `needs_human_review`
5. **Backup**: Guarda versiones intermedias por si necesitas revertir

---

## 📝 Ejemplo Completo

```bash
# 1. Setup
cd dataset_generator
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tus keys

# 2. Preparar datos
mkdir -p data_raw
cp ../elemplos_leyes_info/de_mi_hija/*.pdf data_raw/

# 3. Ejecutar pipeline
python run_pipeline.py --input data_raw/ --output-dir output/

# 4. Revisar resultados
cat output/dataset_final_train.jsonl | head -n 5

# 5. Usar para fine-tuning
# (siguiente paso: subir a Mistral/OpenAI para fine-tuning)
```

---

## 🚀 Siguiente Paso: Fine-tuning

Una vez tengas `dataset_final_train.jsonl`:

```bash
# Subir a Mistral para fine-tuning
# (ver documentación de Mistral API)

# O usar localmente con Unsloth/Axolotl
# (ver guías de fine-tuning local)
```

---

¿Preguntas? Revisa los logs en `logs/` o abre un issue.
