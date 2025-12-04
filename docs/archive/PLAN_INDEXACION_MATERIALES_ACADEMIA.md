# 🎯 PLAN DE INDEXACIÓN DE MATERIALES DE ACADEMIA

**Fecha**: 3 Diciembre 2025  
**Objetivo**: Indexar materiales de academia en Qdrant local con BGE-M3 y generar Q&A con Mistral

---

## 📊 RESUMEN DEL INVENTARIO

### Total de Materiales Escaneados:
- **340 PDFs** encontrados
- **645.76 MB** de contenido
- **Categorías identificadas**: 8

### Distribución por Categoría:

| Prioridad | Categoría | Cantidad | Tamaño (MB) | Acción |
|-----------|-----------|----------|-------------|--------|
| 🔴 **ALTA** | **Exámenes Oficiales** | **27** | **35.06** | **Indexar primero** |
| 🟡 MEDIA | Esquemas | 42 | 75.82 | Indexar segundo |
| 🟡 MEDIA | Simulacros | 28 | 69.00 | Análisis de patrones |
| 🟢 BAJA | Tests | 9 | 23.56 | Análisis de patrones |
| 🟢 BAJA | Temarios | 38 | 59.26 | Referencia |
| 🟢 BAJA | Casos Prácticos | 15 | 48.27 | Referencia |
| 🟢 BAJA | Resúmenes | 7 | 1.76 | Referencia |
| ⚪ INFO | Otros | 174 | 333.03 | Revisar manualmente |

---

## 🎯 FASE 1: EXÁMENES OFICIALES (PRIORIDAD ALTA)

### Archivos Identificados (27 PDFs):

#### 📁 bajados_academia/ (26 archivos)

**Exámenes C1 Seguridad Social:**
1. `01._examen_c1_ss_26-03-2022.pdf` (8.75 MB) + respuestas
2. `04._examen_c1_3-4-23.pdf` (1.05 MB) + respuestas
3. `09._examen_c1_parte_1_noviembre_2024.pdf` (1.67 MB) + parte 2 + respuestas
4. `10._examen_c1_pi_parte_1_noviembre_2024.pdf` (2.31 MB) + parte 2 + respuestas
5. `11._examen_c1_pi_extraord_enero_25.pdf` (0.33 MB) + respuestas
6. `12._examen_c1_extraord_enero_25.pdf` (0.42 MB) + respuestas

**Exámenes Gestión (Libre y PI):**
7. `02._gestion_libre_2022.pdf` (0.82 MB) + respuestas
8. `03._gestion_pi_2022.pdf` (0.70 MB) + respuestas
9. `05._gestion_libre_2023.pdf` (7.71 MB) + respuestas
10. `06._gestion_pi_2023.pdf` (6.70 MB) + respuestas
11. `07._gestion_pi_extraordinaria_2023.pdf` (0.25 MB) + respuestas
12. `08._gestion_libre_extraordinaria_2023.pdf` (0.32 MB) + respuestas

#### 📁 Oficial/ (1 archivo)
13. `Resolución+convocatoria+ADMINISTRATIVOS+2023+BOE.pdf` (0.32 MB)

### Características de los Exámenes Oficiales:
- ✅ **Documentos públicos** - Sin restricciones de derechos de autor
- ✅ **Preguntas reales** - De convocatorias oficiales del INSS
- ✅ **Con respuestas** - Incluyen soluciones oficiales
- ✅ **Años 2022-2025** - Contenido actualizado
- ✅ **Estimación**: ~3,000 preguntas reales

---

## 🎯 FASE 2: ESQUEMAS DE PRESTACIONES (PRIORIDAD MEDIA)

### Archivos Identificados (42 PDFs):

#### 📁 bajados_academia/ (14 esquemas de prestaciones)

**Prestaciones por Incapacidad:**
- `it.pdf` - Incapacidad Temporal
- `ip_absoluta.pdf` - IP Absoluta
- `ip_parcial.pdf` - IP Parcial
- `ip_total.pdf` - IP Total

**Prestaciones por Jubilación:**
- `jubilacion_ordinaria.pdf`
- `jubilacion_anticipada_involuntaria.pdf`
- `jubilacion_anticipada_voluntaria.pdf`
- `jubilacion_activa.pdf`

**Prestaciones por Muerte y Supervivencia:**
- `mys_-_viudedad.pdf`
- `mys_-_orfandad.pdf`

**Otras Prestaciones:**
- `nycm.pdf` - Nacimiento y Cuidado del Menor
- `prestaciones_familiares_nc.pdf`
- `encuadramiento.pdf`
- `cotizacion_2025_1.pdf`

#### 📁 Otros esquemas (28 archivos adicionales)
- Esquemas de procedimiento administrativo
- Esquemas de UE
- Esquemas de Constitución
- Esquemas de TREBEP

### Características de los Esquemas:
- ✅ **Contenido estructurado** - Fácil de procesar
- ✅ **Información legal** - Requisitos, cuantías, plazos
- ✅ **Ideal para Q&A** - Preguntas conceptuales
- ✅ **Estimación**: ~500-1,000 Q&A generables

---

## 🔧 CONFIGURACIÓN TÉCNICA

### 1. Modelo de Embeddings: BGE-M3

```python
# Configuración BGE-M3
EMBEDDING_CONFIG = {
    "model_name": "BAAI/bge-m3",
    "device": "cuda",  # o "cpu" si no hay GPU
    "normalize_embeddings": True,
    "batch_size": 32,
    "max_length": 512
}
```

**Ventajas de BGE-M3:**
- ✅ Multilingüe (excelente para español)
- ✅ Alta precisión en textos legales
- ✅ Soporta documentos largos
- ✅ Open source y gratuito

### 2. Qdrant Local (Docker WSL)

```bash
# Verificar que Qdrant está corriendo
docker ps | grep qdrant

# Si no está corriendo, iniciar:
docker start qdrant
```

**Configuración de colección:**
```python
COLLECTION_CONFIG = {
    "collection_name": "materiales_academia",
    "vector_size": 1024,  # BGE-M3
    "distance": "Cosine",
    "on_disk_payload": True  # Para optimizar memoria
}
```

### 3. Mistral Local (Ollama)

```bash
# Verificar modelo instalado
ollama list | grep mistral

# Si no está, instalar:
ollama pull mistral:7b-instruct
```

---

## 📋 ESTRATEGIA DE INDEXACIÓN RAG 3 CAPAS

### Capa 1: Chunking Inteligente

```python
CHUNKING_STRATEGY = {
    "method": "semantic",  # Basado en significado, no solo tamaño
    "chunk_size": 512,     # Tokens por chunk
    "chunk_overlap": 50,   # Overlap para contexto
    "separators": [
        "\n\n",  # Párrafos
        "\n",    # Líneas
        ". ",    # Oraciones
        ", "     # Frases
    ]
}
```

**Chunking específico por tipo:**
- **Exámenes**: Por pregunta individual (pregunta + opciones + respuesta)
- **Esquemas**: Por sección temática (prestación completa)
- **Temarios**: Por apartado legal

### Capa 2: Metadata Enriquecida

```python
METADATA_SCHEMA = {
    "doc_id": "string",
    "filename": "string",
    "category": "string",  # examenes_oficiales, esquemas, etc.
    "subcategory": "string",  # tipo de prestación, año, etc.
    "source": "string",  # bajados_academia, oficial, etc.
    "year": "integer",
    "topic": "string",  # IT, IP, Jubilación, etc.
    "has_answers": "boolean",
    "question_count": "integer",
    "page_number": "integer",
    "chunk_index": "integer",
    "is_official": "boolean"  # Importante para filtrar
}
```

### Capa 3: Búsqueda Híbrida

```python
SEARCH_STRATEGY = {
    "methods": [
        "dense_vector",  # BGE-M3 embeddings
        "sparse_bm25",   # Keyword matching
        "metadata_filter"  # Filtros específicos
    ],
    "reranking": True,  # Reordenar resultados
    "top_k": 10,
    "score_threshold": 0.7
}
```

---

## 🚀 SCRIPT DE INDEXACIÓN

Voy a crear el script completo en el siguiente paso...

---

## 📊 ESTIMACIÓN DE RESULTADOS

### Exámenes Oficiales (27 PDFs):
- **Preguntas reales**: ~3,000
- **Variaciones generables**: ~6,000 (2x por pregunta)
- **Total Q&A**: ~9,000

### Esquemas (42 PDFs):
- **Preguntas generables**: ~1,000
- **Variaciones**: ~2,000
- **Total Q&A**: ~3,000

### **TOTAL ESTIMADO: ~12,000 Q&A de alta calidad**

---

## 🔒 MEDIDAS DE PRIVACIDAD

1. ✅ **Todo en local** - Qdrant en Docker WSL
2. ✅ **Mistral local** - Ollama sin conexión externa
3. ✅ **BGE-M3 local** - Embeddings sin APIs
4. ✅ **Transformación sustancial** - Variaciones que no dejan rastro
5. ✅ **Sin datos personales** - Anonimización automática

---

## ⏭️ PRÓXIMOS PASOS

1. ✅ **Inventario completado** - 340 PDFs categorizados
2. 🔄 **Crear script de indexación** - Con BGE-M3 y Qdrant
3. ⏳ **Indexar exámenes oficiales** - Fase 1 (27 PDFs)
4. ⏳ **Generar variaciones con Mistral** - 20 preguntas de prueba
5. ⏳ **Validar calidad** - Revisión manual
6. ⏳ **Escalar a todos los materiales** - Fases 2 y 3

---

**Creado**: 3 Diciembre 2025  
**Estado**: ✅ Inventario completado - Listo para indexación
