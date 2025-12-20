# 🎯 DECISIONES CLAVE - OpositaIA

**Última actualización**: 2025-01-18

---

## 🏗️ ARQUITECTURA

### IMPORTANTE!!! Infraestructura Real:

**VPS Hostinger (147.93.95.67)**:
- ✅ Mistral 8B GGUF instalado
- ✅ FastAPI corriendo en puerto 8001
- ❌ Ollama NO instalado (pendiente)
- **Uso**: Producción, LLM primario

**Local (WSL en PC)**:
- ✅ Ollama (tinyllama, all-minilm)
- ✅ Qdrant
- ✅ PostgreSQL
- **Uso**: Desarrollo, embeddings

---

## 💰 COSTOS Y LÍMITES

### IMPORTANTE!!! Límites de Gemini:

**Free Tier**:
- 1,500 requests/día
- 1M tokens/mes

**Con 100 usuarios**:
- 2,000 requests/día (EXCEDE)
- 30M tokens/mes (EXCEDE)

**DECISIÓN**: Usar Mistral (VPS) como primario, Gemini como fallback.

---

## 🤖 MODELOS

### IMPORTANTE!!! Stack de Modelos:

**Embeddings** (búsqueda semántica):
- **Primario**: RoBERTalex vía HuggingFace API (gratis)
- **Alternativo**: all-minilm local (WSL)
- **Uso**: Indexación (1/día) + Búsqueda (cada request)

**Generación** (respuestas):
- **Primario**: Mistral 8B en VPS (gratis, 90% requests)
- **Fallback**: Gemini 2.0 Flash (gratis, 10% requests)
- **Uso**: Cada respuesta al usuario

---

## 📊 EMBEDDINGS

### IMPORTANTE!!! Cuándo se usan:

**A) Indexación** (OFFLINE):
- Frecuencia: 1 vez al día
- Documentos: ~7,100 chunks
- Tiempo: ~2 horas con HF API
- Recursos: Alto

**B) Búsqueda** (ONLINE):
- Frecuencia: Cada request del usuario
- Documentos: 1 query corta
- Tiempo: <500ms
- Recursos: Bajo

**DECISIÓN**: HuggingFace API es suficiente para ambos.

---

## 🔄 SCRAPER BOE

### IMPORTANTE!!! Actualización automática:

**Cron job diario**:
- Hora: 8:00 AM
- Fuente: API oficial BOE (gratis)
- Filtro: Palabras clave SS
- Acción: Descargar → Embedear → Indexar

**Palabras clave**:
- "seguridad social"
- "lgss"
- "prestación"
- "cotización"
- "incapacidad"
- "jubilación"

---

## 💾 CAPACIDAD LOCAL

### IMPORTANTE!!! Recursos disponibles:

**RAM**: 7.7 GB total
- RoBERTalex: 420 MB modelo + 2-3 GB inferencia 
- **Veredicto**: ✅ Puede correr localmente (lento sin GPU)
- **Mejor**: Usar HuggingFace API

---

## 📝 NOTAS PARA FUTURAS CONVERSACIONES

Cuando empieces una nueva conversación, lee este documento primero para recordar:
- Mistral está en VPS, no local
- Gemini tiene límites estrictos
- Embeddings se usan en 2 momentos diferentes
- HuggingFace Free Tier es suficiente
- Scraper BOE debe ser automático

---

**Añade aquí nuevas decisiones importantes con "IMPORTANTE!!!"**

---

## 🎯 PRIORIDADES DE DESARROLLO

### IMPORTANTE!!! Orden de Implementación:

**Prioridad 1**: ✅ Alineación con proyecto (COMPLETADA)
- Leídos todos los .md del proyecto
- Entendido spec-driven development
- Usuarios finales: Opositores C1 Seguridad Social

**Prioridad 2**: 🔄 Arquitectura RAG 3 Capas (EN CURSO)
- ✅ Análisis 5 capas de Perplexity completado
- ✅ Decisión: 3 CAPAS + 2 SISTEMAS (respaldado por papers)
- ✅ Scripts creados: setup_qdrant, metadata_schema, boe_downloader
- 🔄 Sprint 1: Setup infraestructura
- Tiempo estimado: 7-8 días

**Prioridad 3**: Crear Prompts Basados en Ejemplos Reales
- Una vez leídos los exámenes, crear:
  - Prompts para generar preguntas tipo test
  - Prompts para casos prácticos
  - Prompts para análisis de respuestas
  - Prompts para feedback personalizado

**Prioridad 4**: Implementar Upload de Documentos
- Endpoint FastAPI para subir PDFs/imágenes
- Procesamiento con Gemini Vision
- Indexación en Qdrant
- Testing

---

## 🧪 TESTING ROBERTALEX

### IMPORTANTE!!! Decisión Pendiente:

**Archivos creados**:
- `backend/test_robertalex_local.py` - Script de prueba
- `backend/INSTRUCCIONES_TEST_ROBERTALEX.md` - Instrucciones

**Próximo paso**: Ejecutar test para decidir:
- RoBERTalex local (si rápido y mejor calidad)
- HuggingFace API (si lento o similar calidad)

**Comando**:
```bash
cd backend
.\venv\Scripts\activate
python test_robertalex_local.py
```

---

## 📦 MIGRACIÓN QDRANT

### IMPORTANTE!!! Copiar Local → Cloud es POSIBLE:

**Archivo creado**: `backend/migrate_qdrant_to_cloud.py`

**Funcionalidades**:
- Descarga todos los puntos de Qdrant local
- Calcula tamaño real de almacenamiento
- Crea colección en Qdrant Cloud
- Sube puntos en batches
- Verifica migración

**Uso**:
1. Indexar todo en local primero
2. Calcular tamaño real
3. Decidir si usar Cloud Free (1GB) o Paid ($25/mes)
4. Migrar si necesario

**Estimación**: ~33 MB total → ✅ Cabe en Free Tier

