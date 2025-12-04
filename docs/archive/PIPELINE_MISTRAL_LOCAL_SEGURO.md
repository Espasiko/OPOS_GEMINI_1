# 🔒 Pipeline Seguro con Mistral Local (Ollama)

**Fecha**: 3 Diciembre 2025  
**Objetivo**: Crear pipeline seguro para análisis de duplicados y generación Q&A con Mistral local

---

## 🎯 ESTRATEGIA PIPELINE SEGURO

### Ventajas Mistral Local:
✅ **Privacidad total** - Los datos no salen del equipo  
✅ **Sin costes** - Procesamiento ilimitado  
✅ **Control total** - Instrucciones específicas  
✅ **Análisis profundo** - Detección de duplicados y similitudes  

---

## 📊 MATERIALES DISPONIBLES

Según el inventario previo:
- **~2,700 Q&A reales** de exámenes oficiales
- **~300 Q&A** de simulacros de academia
- **14 esquemas** de prestaciones (PDF)
- **Temario oficial** completo

---

## 🛠️ COMPONENTES DEL PIPELINE

### 1. Analizador de Duplicados
**Archivo**: `analyze_academy_duplicates.py`
- Extrae preguntas de PDFs
- Normaliza texto (elimina nombres, fechas, cantidades)
- Detecta similitudes con Mistral
- Clasifica: EXACTA, ALTA, MEDIA, BAJA, NINGUNA

### 2. Generador desde Esquemas
**Archivo**: `generate_qa_from_schemas.py`
- Procesa esquemas de prestaciones
- Genera 5 Q&A por esquema
- Valida calidad con Mistral
- Crea variaciones de las mejores

### 3. Detector de Patrones
**Archivo**: `detect_question_patterns.py`
- Identifica estructuras repetitivas
- Detecta academias que reutilizan preguntas
- Analiza conceptos clave
- Genera recomendaciones

---

## 📋 FLUJO DEL PIPELINE

```
1. EXTRACCIÓN
   ├─ PDFs exámenes oficiales → JSON
   ├─ PDFs simulacros → JSON  
   └─ PDFs esquemas → Texto

2. ANÁLISIS DUPLICADOS
   ├─ Comparar preguntas
   ├─ Clasificar similitudes
   └─ Identificar patrones

3. GENERACIÓN
   ├─ Desde esquemas (1,500 Q&A)
   ├─ Variaciones de reales (2,000 Q&A)
   └─ Desde Qdrant (4,000 Q&A)

4. VALIDACIÓN
   ├─ Revisar calidad
   ├─ Verificar precisión legal
   └─ Filtrar duplicados

5. EXPORTACIÓN
   └─ Dataset final JSONL
```

---

## 💻 INSTALACIÓN Y USO

### Requisitos:
```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar Mistral
ollama pull mistral

# Instalar dependencias Python
pip install ollama PyPDF2 pandas
```

### Ejecución:
```bash
# 1. Analizar duplicados
python analyze_academy_duplicates.py

# 2. Generar desde esquemas
python generate_qa_from_schemas.py

# 3. Detectar patrones
python detect_question_patterns.py
```

---

## 📊 ESTIMACIÓN

### Procesamiento con Mistral Local:
- Análisis duplicados: ~2 horas (3,000 preguntas)
- Generación desde esquemas: ~3 horas (1,500 Q&A)
- Variaciones de reales: ~4 horas (2,000 Q&A)
- Validación calidad: ~2 horas

**TOTAL**: ~11 horas de procesamiento  
**COSTE**: $0 (solo electricidad)

### Dataset Final Estimado:
- Q&A reales únicas: ~2,000
- Q&A generadas desde esquemas: ~1,500
- Variaciones: ~2,000
- Desde Qdrant: ~4,000

**TOTAL**: ~9,500 Q&A de alta calidad

---

## ✅ PRÓXIMOS PASOS

1. ✅ Configurar Ollama con Mistral
2. ⏳ Crear scripts de análisis
3. ⏳ Probar con muestra pequeña
4. ⏳ Ejecutar pipeline completo
5. ⏳ Validar calidad del dataset

---

**Ventaja clave**: Control total, privacidad absoluta y coste cero.
