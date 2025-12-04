# 🔒 Pipeline Seguro con Mistral Local

Pipeline completo para análisis de duplicados y generación de Q&A usando Mistral local (Ollama).

## 🎯 Ventajas

✅ **Privacidad total** - Los datos no salen de tu equipo  
✅ **Sin costes** - Procesamiento ilimitado  
✅ **Control total** - Instrucciones específicas  
✅ **Análisis profundo** - Detección de duplicados y similitudes  

---

## 📦 Instalación

### 1. Instalar Ollama

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Descarga desde: https://ollama.ai/download

### 2. Descargar Mistral

```bash
ollama pull mistral
```

### 3. Verificar instalación

```bash
ollama list
```

Deberías ver `mistral` en la lista.

### 4. Instalar dependencias Python

```bash
pip install ollama PyPDF2 pandas
```

---

## 🚀 Uso Rápido

### Test inicial

```bash
python test_mistral_pipeline.py
```

Este script verifica:
- ✅ Conexión con Ollama
- ✅ Generación de Q&A
- ✅ Análisis de similitud

### 1. Analizar duplicados

```bash
python analyze_academy_duplicates.py
```

**Qué hace:**
- Extrae preguntas de PDFs de exámenes
- Normaliza texto (elimina nombres, fechas, cantidades)
- Detecta similitudes con Mistral
- Clasifica: EXACTA, ALTA, MEDIA, BAJA, NINGUNA

**Output:**
- `analisis_duplicados_academia.json` - Resultados completos

### 2. Generar Q&A desde esquemas

```bash
python generate_qa_from_schemas.py
```

**Qué hace:**
- Procesa esquemas de prestaciones (PDFs)
- Genera 3-5 Q&A por esquema
- Valida calidad
- Exporta en formato JSONL

**Output:**
- `resultados_generacion_schemas.json` - Resultados completos
- `dataset_schemas_qa.jsonl` - Dataset listo para fine-tuning

---

## 📊 Estructura del Pipeline

```
📁 Pipeline Mistral Local
├── 📄 test_mistral_pipeline.py          # Test inicial
├── 📄 analyze_academy_duplicates.py     # Análisis de duplicados
├── 📄 generate_qa_from_schemas.py       # Generación desde esquemas
├── 📄 PIPELINE_MISTRAL_LOCAL_SEGURO.md  # Documentación completa
└── 📄 README_PIPELINE_MISTRAL.md        # Esta guía
```

---

## 🔧 Configuración

### Cambiar modelo

Por defecto usa `mistral`. Para usar otro modelo:

```python
analyzer = DuplicateAnalyzer(model="llama2")
generator = SchemaQAGenerator(model="llama2")
```

### Ajustar cantidad de preguntas

En `generate_qa_from_schemas.py`:

```python
# Cambiar de 3 a 5 preguntas por esquema
generated_qa = self.generate_qa_from_schema(
    schema_content, topic, filename, count=5  # <-- Aquí
)
```

### Limitar archivos procesados

En `analyze_academy_duplicates.py`:

```python
# Procesar solo 5 PDFs por carpeta
pdf_files = list(folder_path.rglob("*.pdf"))[:5]  # <-- Aquí
```

---

## 📈 Estimaciones

### Tiempo de procesamiento

Con Mistral local en hardware medio:
- Análisis de duplicados: ~2 horas (3,000 preguntas)
- Generación desde esquemas: ~3 horas (1,500 Q&A)
- Total: ~5 horas

### Dataset esperado

- Q&A reales únicas: ~2,000
- Q&A generadas desde esquemas: ~1,500
- Variaciones: ~2,000
- **Total**: ~5,500 Q&A de alta calidad

### Coste

**$0** - Solo electricidad de tu equipo

---

## 🐛 Troubleshooting

### Error: "Ollama no disponible"

**Solución:**
```bash
# Verificar que Ollama esté corriendo
ollama list

# Si no responde, reiniciar
ollama serve
```

### Error: "Model not found"

**Solución:**
```bash
# Descargar Mistral
ollama pull mistral

# Verificar
ollama list
```

### Error al extraer PDFs

**Solución:**
```bash
# Instalar PyPDF2
pip install PyPDF2

# Si persiste, verificar que los PDFs no estén corruptos
```

### Respuestas muy lentas

**Solución:**
- Mistral es un modelo grande (~7B parámetros)
- Considera usar `mistral:7b-instruct-q4_0` (versión cuantizada)
- O usa un modelo más pequeño como `llama2:7b`

```bash
ollama pull mistral:7b-instruct-q4_0
```

---

## 📝 Formato del Dataset

El dataset generado usa formato JSONL estándar:

```json
{
  "instruction": "¿Cuál es el período mínimo de cotización para...?",
  "input": "a) 15 años\nb) 25 años\nc) 35 años\nd) 37 años",
  "output": "Respuesta: a\n\nExplicación: Según la LGSS...",
  "metadata": {
    "tema": "Jubilación Ordinaria",
    "fuente": "jubilacion_ordinaria.pdf",
    "dificultad": "media"
  }
}
```

Compatible con:
- Hugging Face Trainer
- OpenAI fine-tuning
- Mistral fine-tuning
- LLaMA fine-tuning

---

## ✅ Próximos Pasos

1. ✅ Ejecutar `test_mistral_pipeline.py`
2. ⏳ Ejecutar `analyze_academy_duplicates.py`
3. ⏳ Revisar `analisis_duplicados_academia.json`
4. ⏳ Ejecutar `generate_qa_from_schemas.py`
5. ⏳ Revisar `dataset_schemas_qa.jsonl`
6. ⏳ Validar calidad manualmente (muestra)
7. ⏳ Ejecutar pipeline completo con todos los materiales

---

## 🔗 Referencias

- **Ollama**: https://ollama.ai
- **Mistral**: https://mistral.ai
- **PyPDF2**: https://pypdf2.readthedocs.io

---

## 💡 Tips

1. **Empieza con una muestra pequeña** - Prueba con 2-3 PDFs primero
2. **Revisa la calidad** - Valida manualmente algunas Q&A generadas
3. **Ajusta los prompts** - Modifica las instrucciones según tus necesidades
4. **Usa GPU si tienes** - Ollama detecta automáticamente GPU y acelera
5. **Monitorea recursos** - Mistral usa ~8GB RAM, asegúrate de tener suficiente

---

**¿Preguntas?** Revisa `PIPELINE_MISTRAL_LOCAL_SEGURO.md` para más detalles.
