# 🎯 Pipeline de Generación de Dataset Q&A Legal

Sistema multi-agente profesional para generar datasets de alta calidad desde documentos legales.

## 📋 Características

- **Generación automática** de Q&A desde textos/PDFs
- **Clasificación de riesgo** automática (Alto/Medio/Bajo)
- **Verificación multi-agente** para asegurar calidad
- **Revisión humana selectiva** (solo contenido crítico)
- **Modelos híbridos** (Groq para básico, Claude para complejo)
- **Metadata completa** con trazabilidad total
- **Formato JSONL estándar** con 25 campos
- **Exportación lista para fine-tuning**

## 🏗️ Arquitectura

```
Documentos → Extracción → Generación → Verificación → Curación → Dataset Final
                ↓            ↓            ↓            ↓           ↓
              .txt       Groq/Claude   Agente 2    Humano      JSONL
```

## 📦 Instalación

```bash
cd dataset_generator
pip install -r requirements.txt
```

## ⚙️ Configuración

1. Copia `.env.example` a `.env`
2. Añade tus API keys:
   ```
   GROQ_API_KEY=tu_key_aqui
   ANTHROPIC_API_KEY=tu_key_aqui  # opcional
   QDRANT_URL=tu_url_qdrant
   QDRANT_API_KEY=tu_key_qdrant
   ```

## 🚀 Uso Rápido

```bash
# 1. Extraer texto de PDFs
python extract_text.py --input data_raw/ --output data_txt/

# 2. Generar Q&A
python generate_qa.py --input data_txt/ --output output/qa_raw.json

# 3. Verificar calidad
python verify_qa.py --input output/qa_raw.json --output output/qa_verified.json

# 4. Exportar para fine-tuning
python export_dataset.py --input output/qa_verified.json --output output/dataset_final.jsonl
```

## 📊 Estructura de Carpetas

```
dataset_generator/
├── data_raw/           # PDFs y documentos originales
├── data_txt/           # Textos extraídos
├── output/             # Datasets generados
│   ├── qa_raw.json
│   ├── qa_verified.json
│   └── dataset_final.jsonl
├── config.json         # Configuración global
└── logs/              # Logs de ejecución
```

## 🎯 Calidad Esperada

- **Sin verificación**: 75-80% calidad
- **Con verificación**: 90-95% calidad
- **Con curación humana**: 95-98% calidad

## 💰 Costes Estimados

- 10,000 Q&A con Groq: ~$5-7
- 10,000 Q&A híbrido (Groq + Claude): ~$15
- 10,000 Q&A solo Claude: ~$50-60


## 📋 Esquema de Metadata

Cada Q&A incluye **25 campos** con trazabilidad completa:

### Campos Principales:
- `id`, `question`, `answer`
- `source_document`, `source_location`
- `content_type`, `risk_level`, `difficulty_level`

### Verificación:
- `verified_by_ia`, `verified_by_human`
- `human_reviewer`, `review_date`, `review_notes`
- `confidence`, `verification_issues`

### Trazabilidad:
- `version`, `created_at`, `last_modified`
- `tags`, `notes`, `referencia`

Ver `METADATA_SCHEMA.md` para detalles completos.

## 📄 Formato JSONL

Ejemplo de Q&A exportada:

```jsonl
{"id":"qa_00001","question":"¿Cuál es la edad ordinaria de jubilación en 2024?","answer":"La edad ordinaria de jubilación en 2024 es de 66 años y 6 meses...","source_document":"lgss_2024.txt","content_type":"normativa","risk_level":"high","verified_by_ia":true,"verified_by_human":true,"human_reviewer":"juan_experto_ss","confidence":0.95,"tags":["jubilación","LGSS"],"version":"1"}
```

Ver `example_dataset.jsonl` para más ejemplos.
