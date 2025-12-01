# 🚀 PRÓXIMOS PASOS - OpositaIA (PLAN DEFINITIVO)

**Fecha**: 2025-11-18  
**Estado**: ✅ Análisis 5 capas completado, arquitectura 3 capas aprobada  
**Decisión**: Implementar 3 CAPAS + 2 SISTEMAS (respaldado por papers académicos)

---

## 🎯 ARQUITECTURA APROBADA: 3 CAPAS + 2 SISTEMAS

### ✅ Decisiones Clave

1. **3 Capas de Contenido** (en Qdrant única colección)
   - Capa 1: Normativa Oficial (BOE, leyes, RD)
   - Capa 2: Jurisprudencia y Doctrina (STS, TSJ)
   - Capa 3: Materiales de Estudio (tests, casos, temarios)

2. **Diferenciación por Metadata** (NO por modelo)
   - RoBERTalex genera embeddings únicos (768 dim)
   - Capas se distinguen por metadata: `layer`, `tipo`, `nivel_jerarquia`

3. **2 Sistemas Auxiliares** (fuera de Qdrant)
   - Sistema 1: Temporal Tracking (PostgreSQL) - ⏸️ FUTURO
   - Sistema 2: Quality Evaluator (CRAG) - ⏸️ FUTURO

4. **Fine-tuning RoBERTalex** - ⏸️ DEJADO PARA MÁS ADELANTE

---

## 📋 PLAN DE IMPLEMENTACIÓN (SCRUM)

### 📋 Plan Completo

**Documento**: `ai-specs/changes/RAG-indexacion-leyes-principales.md`  
**Tiempo estimado**: 2-3 días  
**Estado**: ✅ Planificado, listo para implementar

---

## 📊 RESUMEN EJECUTIVO

### ✅ Lo que YA tenemos:

1. **Test RoBERTalex completado**
   - 🏆 RoBERTalex GANA con +10% calidad (0.76 vs 0.69)
   - Script: `backend/test_robertalex_local.py`
   - Decisión: Usar RoBERTalex en producción

2. **Infraestructura lista**
   - ✅ Qdrant local en WSL
   - ✅ Backend FastAPI estructurado
   - ✅ Docker compose configurado
   - ✅ Script migración Qdrant→Cloud

3. **Materiales disponibles**
   - 📚 2,500+ páginas de temarios
   - 📝 600+ páginas de tests
   - 💼 200+ páginas de casos prácticos
   - 📖 ~100 documentos BOE principales

---

## 🎯 FASE 1: Indexación de Leyes (SIGUIENTE)

### Paso 1: Preparación del Entorno (30 min)

```bash
# 1. Activar venv
cd backend
.\venv\Scripts\activate  # Windows

# 2. Instalar dependencias adicionales
pip install pypdf python-docx beautifulsoup4 lxml

# 3. Verificar Qdrant está corriendo
docker ps | findstr qdrant
# Si no está: docker-compose up -d qdrant
```

**Checklist**:
- [ ] Venv activado
- [ ] Dependencias instaladas
- [ ] Qdrant corriendo en localhost:6333
- [ ] RoBERTalex funcionando (ya testeado)

---

### Paso 2: Crear Colección en Qdrant (15 min)

**Archivo a crear**: `backend/setup_qdrant_collection.py`

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")

# Eliminar colección antigua si existe
try:
    client.delete_collection("opositaia_documents")
    print("✅ Colección antigua eliminada")
except:
    print("ℹ️  No había colección anterior")

# Crear nueva colección
client.create_collection(
    collection_name="opositaia_documents",
    vectors_config=VectorParams(
        size=768,  # RoBERTalex dimension
        distance=Distance.COSINE
    )
)
print("✅ Colección 'opositaia_documents' creada")
```

**Ejecutar**:
```bash
python backend/setup_qdrant_collection.py
```

**Checklist**:
- [ ] Script creado
- [ ] Colección creada exitosamente
- [ ] Verificado en Qdrant UI (http://localhost:6333/dashboard)

---

### Paso 3: Descargar Leyes del BOE (2-3 horas)

**Archivo a crear**: `backend/agents/boe_scraper.py`

**Leyes a descargar** (8 principales):
1. LGSS (RDL 8/2015)
2. Ley 39/2015 (Procedimiento Administrativo)
3. Ley 40/2015 (Régimen Jurídico)
4. RDL 5/2015 (EBEP)
5. RD 1415/2004 (Recaudación SS)
6. RD 84/1996 (Afiliación)
7. Ley 19/2021 (Ingreso Mínimo Vital)
8. LO 3/2018 (Protección de Datos)

**URLs BOE**:
```python
LEYES_PRINCIPALES = [
    {
        "nombre": "LGSS",
        "boe_id": "BOE-A-2015-11724",
        "url": "https://www.boe.es/eli/es/rdlg/2015/10/30/8/con"
    },
    {
        "nombre": "Ley 39/2015",
        "boe_id": "BOE-A-2015-10565",
        "url": "https://www.boe.es/eli/es/l/2015/10/01/39/con"
    },
    # ... resto
]
```

**Ejecutar**:
```bash
python backend/agents/boe_scraper.py
```

**Output esperado**: PDFs guardados en `backend/data/leyes/`

**Checklist**:
- [ ] Script `boe_scraper.py` creado
- [ ] 8 PDFs descargados exitosamente
- [ ] Carpeta `backend/data/leyes/` creada
- [ ] Verificar tamaño total (~50-100 MB)

---

### Paso 4: Procesar y Chunkear (1-2 horas)

**Archivos a crear**:
1. `backend/agents/pdf_processor.py` - Procesa PDFs del BOE
2. `backend/agents/materials_processor.py` - Procesa materiales de academia

**Estrategia de chunking**:
- **Tamaño**: 512 tokens
- **Overlap**: 50-75 tokens
- **Respeto de estructura**: Detectar artículos y no cortarlos

**Funcionalidades**:
- Detectar artículos (regex: `Artículo \d+` o `Art\. \d+`)
- Extraer texto limpio
- Crear chunks con metadata (artículo, ley, fecha)

**Checklist**:
- [ ] `pdf_processor.py` creado
- [ ] `materials_processor.py` creado
- [ ] Testeado con 1 PDF
- [ ] Chunks generados correctamente

---

### Paso 5: Generar Embeddings e Indexar (3-4 horas)

**Archivo a crear**: `backend/agents/indexer.py`

**Proceso**:
1. Cargar RoBERTalex
2. Generar embeddings en batches (100 chunks/vez)
3. Subir a Qdrant con metadata
4. Mostrar progreso

**Estimación de tiempo**:
- 8 leyes BOE: ~1,000 chunks → ~30 min
- Temarios: ~5,000 chunks → ~2 horas
- Tests: ~1,200 chunks → ~30 min
- Casos: ~400 chunks → ~10 min
- **TOTAL**: ~3-4 horas

**Comando**:
```bash
python backend/index_all_materials.py
```

**Checklist**:
- [ ] `indexer.py` creado
- [ ] Script principal `index_all_materials.py` creado
- [ ] Leyes BOE indexadas
- [ ] Temarios indexados
- [ ] Tests indexados
- [ ] Casos prácticos indexados
- [ ] Verificar en Qdrant UI (~7,600 puntos)

---

### Paso 6: Testing de Calidad (1 hora)

**Archivo a crear**: `backend/test_queries.py`

**100 queries de test** (ejemplos):
```python
QUERIES_TEST = [
    # Incapacidad
    "Diferencia entre incapacidad temporal y permanente según LGSS",
    "Requisitos para incapacidad permanente total Art. 194",
    "Duración máxima de la incapacidad temporal",
    
    # Jubilación
    "Edad mínima para jubilación ordinaria 2025",
    "Requisitos jubilación anticipada voluntaria Art. 208",
    
    # Cotización
    "Bases de cotización Régimen General 2025",
    
    # ... 94 más
]
```

**Métricas a medir**:
- Score promedio de similitud
- Top 5 mejores queries
- Top 5 peores queries
- Distribución de scores

**Objetivo**: Score promedio >0.75

**Checklist**:
- [ ] 100 queries creadas
- [ ] Script de testing ejecutado
- [ ] Score promedio calculado
- [ ] Resultados analizados
- [ ] Decisión: ¿Calidad suficiente?

---

### Paso 7: Calcular Tamaño Real (15 min)

**Usar script**: `backend/migrate_qdrant_to_cloud.py`

```bash
python backend/migrate_qdrant_to_cloud.py --calculate-only
```

**Estimación teórica**: ~33 MB
**Verificar**: Tamaño real en Qdrant

**Decisión**:
- Si <500 MB → ✅ Usar Qdrant Cloud Free (1GB)
- Si >500 MB → Evaluar Qdrant Cloud Paid ($25/mes)

**Checklist**:
- [ ] Tamaño calculado
- [ ] Decisión tomada (Free vs Paid)
- [ ] Documentado en `docs/DECISIONES_CLAVE.md`

---

## 🎯 FASE 2: Integración con Backend (DESPUÉS)

### Una vez indexado todo:

1. **Actualizar RAG Agent** (`backend/agents/rag_agent.py`)
   - Conectar a colección `opositaia_documents`
   - Implementar búsqueda semántica
   - Formatear contexto para LLM

2. **Crear Endpoints API** (`backend/routers/rag.py`)
   - `POST /api/rag/search` - Búsqueda semántica
   - `GET /api/rag/stats` - Estadísticas
   - `POST /api/rag/test` - Testing rápido

3. **Testing End-to-End**
   - Probar desde frontend
   - Verificar latencia (<2s)
   - Verificar calidad de respuestas

---

## 🎯 FASE 3: Prompts Basados en Ejemplos (FUTURO)

### Una vez tengamos RAG funcionando:

1. **Analizar materiales indexados**
   - Extraer patrones de preguntas tipo test
   - Extraer estructura de casos prácticos
   - Identificar formato de respuestas

2. **Crear prompts mejorados**
   - Generador de tests (basado en ejemplos reales)
   - Generador de casos (basado en ejemplos reales)
   - Evaluador de respuestas (basado en criterios reales)

3. **Actualizar `docs/AI_AGENTS.md`**
   - Documentar nuevos prompts
   - Justificar decisiones
   - Incluir ejemplos

---

## 📊 ESTIMACIÓN DE TIEMPO TOTAL

| Fase | Tiempo | Prioridad |
|------|--------|-----------|
| **Fase 1: Indexación** | 2-3 días | 🔴 ALTA |
| Paso 1: Preparación | 30 min | - |
| Paso 2: Crear colección | 15 min | - |
| Paso 3: Descargar BOE | 2-3 horas | - |
| Paso 4: Procesar/Chunkear | 1-2 horas | - |
| Paso 5: Indexar | 3-4 horas | - |
| Paso 6: Testing | 1 hora | - |
| Paso 7: Calcular tamaño | 15 min | - |
| **Fase 2: Integración Backend** | 1-2 días | 🟡 MEDIA |
| **Fase 3: Prompts Mejorados** | 2-3 días | 🟢 BAJA |

**TOTAL**: ~5-8 días de trabajo

---

## 🚀 COMANDOS PARA EJECUTAR SPRINT 2

```bash
# 1. Activar entorno
cd elemplos_leyes_info
.\venv\Scripts\activate

# 2. Instalar dependencias nuevas
pip install pypdf==5.1.0 python-docx==1.1.2 tqdm==4.66.0

# 3. Verificar Qdrant
docker ps | findstr qdrant

# 4. INDEXAR LGSS (Script maestro - hace todo)
cd ..
python backend/index_lgss_complete.py

# 5. Probar búsquedas
python backend/agents/test_search.py
```

**📖 Instrucciones detalladas**: `backend/SPRINT2_INSTRUCCIONES.md`

---

## 📝 NOTAS IMPORTANTES

### ⚠️ Antes de empezar:

1. **Qdrant debe estar corriendo**
   ```bash
   docker-compose up -d qdrant
   ```

2. **RoBERTalex ya está testeado** ✅
   - Funciona correctamente
   - +10% mejor que all-minilm
   - Listo para usar

3. **Materiales en `elemplos_leyes_info/`**
   - ❌ NO están en GitHub (ignorados)
   - ✅ Están en tu PC local
   - ✅ Listos para procesar

4. **Tiempo de indexación**
   - Primera vez: 3-4 horas
   - Actualizaciones: 30 min (solo nuevos docs)

---

## 🎯 DECISIÓN: ¿Empezamos con Fase 1?

**Opción A**: Empezar ahora con indexación
```
Kiro, empecemos con la Fase 1: Indexación de Leyes.
Crea el script setup_qdrant_collection.py
```

**Opción B**: Revisar plan primero
```
Kiro, explícame más detalles sobre [paso específico]
```

**Opción C**: Hacer algo diferente
```
Kiro, prefiero trabajar en [otra cosa]
```

---

## 📚 DOCUMENTOS DE REFERENCIA

- **Plan completo**: `ai-specs/changes/RAG-indexacion-leyes-principales.md`
- **Decisiones técnicas**: `docs/DECISIONES_CLAVE.md`
- **Estado implementación**: `docs/IMPLEMENTATION_STATUS.md`
- **Roadmap**: `docs/ROADMAP.md`
- **Test RoBERTalex**: `backend/test_robertalex_local.py`

---

**¿Con qué empezamos?** 🚀


### 🎯 SPRINT 1: Setup Infraestructura (Día 1) ✅ COMPLETADO

**Objetivo**: Preparar entorno para indexación con 3 capas

**Tareas**:
- [x] 1.1: Verificar venv existente (`elemplos_leyes_info/venv`)
- [x] 1.2: Instalar qdrant-client en venv
- [x] 1.3: Verificar Qdrant corriendo (puerto 6333)
- [x] 1.4: Limpiar TODAS las colecciones existentes
- [x] 1.5: Crear colección `opositaia_leyes_seguridad_social` (768 dim)
- [x] 1.6: Definir schema de metadata (Pydantic)
- [x] 1.7: Descargar LGSS (1.69 MB) para testing

**Resultados**:
- ✅ Qdrant limpio y corriendo en localhost:6333
- ✅ Colección creada: `opositaia_leyes_seguridad_social` (768 dim, COSINE)
- ✅ Schema metadata documentado en `backend/models/metadata_schema.py`
- ✅ LGSS.pdf descargado en `backend/data/leyes/`
- ✅ Scripts creados: `verify_and_setup.py`, `download_lgss_only.py`

---

### 🎯 SPRINT 2: Indexar Capa 1 - Normativa (Día 2-3) ✅ COMPLETADO

**Objetivo**: Indexar LGSS primero, luego 7 leyes más del BOE

**Tareas**:
- [x] 2.1: Crear `backend/agents/boe_downloader.py` ✅
- [x] 2.2: Descargar LGSS (1.69 MB) ✅
- [x] 2.3: Crear `backend/agents/pdf_processor.py` ✅
- [x] 2.4: Crear `backend/agents/robertalex_embedder.py` ✅
- [x] 2.5: Crear `backend/agents/indexer.py` ✅
- [x] 2.6: Crear `backend/agents/test_search.py` ✅
- [x] 2.7: Crear script maestro `backend/index_lgss_complete.py` ✅
- [x] 2.8: **EJECUTADO**: Indexar LGSS completo (17 min) ✅
- [x] 2.9: **EJECUTADO**: Probar búsquedas con test_search.py ✅
- [x] 2.10: Descargar Constitución Española ✅
- [x] 2.11: Indexar Constitución Española ✅

### 🎯 SPRINT 3: Leyes Prioritarias (Día 3) ✅ COMPLETADO

- [x] 3.1: Descargar Ley 39/2015, Ley 40/2015, EBEP ✅
- [x] 3.2: Indexar las 3 leyes prioritarias ✅
- [x] 3.3: Verificar calidad de indexación ✅

**Resultados Sprint 3**:
- ✅ 3 leyes indexadas (Ley 39/2015, Ley 40/2015, EBEP)
- ✅ 960 nuevos chunks indexados
- ✅ Total colección: 1,543 chunks
- ✅ 5 normas completas en sistema
- ✅ Tiempo: 13 minutos

### 🎯 SPRINT 4: Completar Capa 1 (Día 3) ✅ COMPLETADO

- [x] 4.1: Descargar 4 leyes restantes ✅
- [x] 4.2: Indexar RD Recaudación, RD Afiliación, Ley IMV, LOPDGDD ✅
- [x] 4.3: Verificar colección completa ✅

**Resultados Sprint 4**:
- ✅ 4 leyes indexadas
- ✅ 473 nuevos chunks indexados
- ✅ Total colección: 2,016 chunks
- ✅ 9 normas completas (Capa 1 COMPLETA)
- ✅ Tiempo: 14 minutos

### 🎯 SPRINT 5: Capa 3 - Materiales de Estudio (Día 3-4) ⏳ EN PROGRESO

- [x] 5.1: Crear procesador para materiales de estudio ✅
- [x] 5.2: Iniciar indexación de tests y temarios ✅
- [ ] 5.3: Completar indexación (corriendo en background) ⏳
- [ ] 5.4: Verificar calidad de Capa 3 ⏸️

**Progreso Sprint 5**:
- ✅ Test 1 AGE indexado (391 chunks)
- ⏳ Test 2 AGE en progreso (~500 chunks)
- ⏸️ Temarios pendientes (~4,000 chunks)
- ⏸️ Casos prácticos pendientes (~200 chunks)
- **Total estimado**: ~5,000 chunks Capa 3

**Resultados Obtenidos**:
- ✅ LGSS procesado: 269 páginas → 521 chunks
- ✅ 167 artículos detectados automáticamente
- ✅ Embeddings generados con RoBERTalex (768 dim)
- ✅ 521 puntos indexados en Qdrant con metadata Capa 1
- ✅ Búsquedas funcionando con score promedio: **0.64**
- ✅ Score máximo: 0.71 | Score mínimo: 0.55
- ✅ Tiempo total: ~17 minutos

---

### 🎯 SPRINT 3: Indexar Capa 2 - Jurisprudencia (Día 4)

**Objetivo**: Indexar Top 50 sentencias STS relevantes

**Tareas**:
- [ ] 3.1: Identificar Top 50 sentencias STS (manual)
- [ ] 3.2: Descargar sentencias (si disponibles)
- [ ] 3.3: Procesar sentencias → chunks
- [ ] 3.4: Indexar con metadata Capa 2
- [ ] 3.5: Testing: Búsqueda por jerarquía

**Criterios de Aceptación**:
- 50 sentencias identificadas
- Procesadas y chunkeadas
- Indexadas con `layer=2`, `tipo=sentencia_sts`
- Búsqueda prioriza Capa 1 > Capa 2

---

### 🎯 SPRINT 4: Indexar Capa 3 - Materiales (Día 5-6)

**Objetivo**: Indexar materiales de tu hija (tests, casos, temarios)

**Tareas**:
- [ ] 4.1: Seleccionar archivos clave de `elemplos_leyes_info/`
- [ ] 4.2: Procesar tests con respuestas
- [ ] 4.3: Procesar casos prácticos
- [ ] 4.4: Procesar temarios (primeras 100 páginas)
- [ ] 4.5: Indexar con metadata Capa 3
- [ ] 4.6: Testing: Búsqueda multi-capa

**Criterios de Aceptación**:
- Tests indexados con formato detectado
- Casos prácticos con soluciones
- Temarios principales indexados
- Búsqueda funciona en las 3 capas
- Total ~7,600 chunks indexados

---

### 🎯 SPRINT 5: API RAG Básica (Día 7)

**Objetivo**: Crear endpoints FastAPI para búsqueda

**Tareas**:
- [ ] 5.1: Actualizar `backend/agents/rag_agent.py`
- [ ] 5.2: Implementar búsqueda con filtros por capa
- [ ] 5.3: Implementar reranking por jerarquía
- [ ] 5.4: Crear endpoint `POST /api/rag/search`
- [ ] 5.5: Crear endpoint `GET /api/rag/stats`
- [ ] 5.6: Testing: 100 queries de prueba

**Criterios de Aceptación**:
- Endpoint `/api/rag/search` funciona
- Filtros por capa funcionan
- Reranking por jerarquía implementado
- 100 queries testeadas con score >0.75

---

### 🎯 SPRINT 6: Integración Frontend (Día 8)

**Objetivo**: Conectar frontend con nuevo RAG

**Tareas**:
- [ ] 6.1: Actualizar `services/ragService.ts`
- [ ] 6.2: Crear componente `RAGSearch.tsx`
- [ ] 6.3: Integrar con chat existente
- [ ] 6.4: Testing E2E
- [ ] 6.5: Documentar en `docs/`

**Criterios de Aceptación**:
- Frontend puede buscar en RAG
- Resultados se muestran correctamente
- Metadata visible (capa, tipo, fecha)
- Testing E2E exitoso

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### Paso 1.4: Crear Colección Qdrant

```python
# backend/setup_qdrant_collection.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

def create_collection():
    client = QdrantClient(url="http://localhost:6333")
    
    # Eliminar si existe
    try:
        client.delete_collection("opositaia_unified")
        print("✅ Colección anterior eliminada")
    except:
        print("ℹ️  No había colección anterior")
    
    # Crear nueva
    client.create_collection(
        collection_name="opositaia_unified",
        vectors_config=VectorParams(
            size=768,  # RoBERTalex dimension
            distance=Distance.COSINE
        )
    )
    print("✅ Colección 'opositaia_unified' creada (768 dim)")

if __name__ == "__main__":
    create_collection()
```

### Paso 1.5: Schema de Metadata

```python
# backend/models/metadata_schema.py
from typing import Literal, Optional
from pydantic import BaseModel
from datetime import date

class DocumentMetadata(BaseModel):
    """Schema de metadata para documentos indexados"""
    
    # Identificación de capa
    layer: Literal[1, 2, 3]  # 1=Normativa, 2=Jurisprudencia, 3=Materiales
    nivel_jerarquia: Literal[1, 2, 3]  # Para reranking
    
    # Tipo de documento
    tipo: str  # "ley", "real_decreto", "sentencia_sts", "test", etc.
    
    # Información temporal
    fecha: Optional[date] = None
    fecha_vigencia: Optional[date] = None
    fecha_derogacion: Optional[date] = None
    
    # Referencias
    norma_id: Optional[str] = None  # "BOE-A-2015-11724"
    articulo: Optional[str] = None  # "212"
    norma_modificadora: Optional[str] = None
    
    # Jurisprudencia
    tribunal: Optional[str] = None  # "Tribunal Supremo"
    superada_por: Optional[str] = None  # "STS 1250/2024"
    
    # Materiales
    fuente: Optional[str] = None  # "Academia Las Cortes"
    tema: Optional[str] = None  # "8"
    formato: Optional[str] = None  # "pregunta_respuesta"
    
    # Contenido
    text: str
    chunk_id: int
    total_chunks: int

# Ejemplo de uso
metadata_ley = DocumentMetadata(
    layer=1,
    nivel_jerarquia=1,
    tipo="ley",
    fecha=date(2015, 10, 30),
    fecha_vigencia=date(2016, 1, 2),
    norma_id="BOE-A-2015-11724",
    articulo="212",
    text="Artículo 212. Jubilación ordinaria...",
    chunk_id=1,
    total_chunks=5
)
```

### Paso 2.1: BOE Downloader

```python
# backend/agents/boe_downloader.py
import requests
from pathlib import Path
from typing import List, Dict

class BOEDownloader:
    """Descarga PDFs del BOE"""
    
    LEYES_PRINCIPALES = [
        {
            "nombre": "LGSS",
            "boe_id": "BOE-A-2015-11724",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-11724-consolidado.pdf"
        },
        {
            "nombre": "Ley_39_2015",
            "boe_id": "BOE-A-2015-10565",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-10565-consolidado.pdf"
        },
        {
            "nombre": "Ley_40_2015",
            "boe_id": "BOE-A-2015-10566",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-10566-consolidado.pdf"
        },
        {
            "nombre": "EBEP",
            "boe_id": "BOE-A-2015-11719",
            "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-11719-consolidado.pdf"
        },
        {
            "nombre": "RD_Recaudacion",
            "boe_id": "BOE-A-2004-11836",
            "url": "https://www.boe.es/buscar/pdf/2004/BOE-A-2004-11836-consolidado.pdf"
        },
        {
            "nombre": "RD_Afiliacion",
            "boe_id": "BOE-A-1996-4447",
            "url": "https://www.boe.es/buscar/pdf/1996/BOE-A-1996-4447-consolidado.pdf"
        },
        {
            "nombre": "Ley_IMV",
            "boe_id": "BOE-A-2021-21007",
            "url": "https://www.boe.es/buscar/pdf/2021/BOE-A-2021-21007-consolidado.pdf"
        },
        {
            "nombre": "LOPDGDD",
            "boe_id": "BOE-A-2018-16673",
            "url": "https://www.boe.es/buscar/pdf/2018/BOE-A-2018-16673-consolidado.pdf"
        }
    ]
    
    def __init__(self, output_dir: str = "backend/data/leyes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download_all(self) -> List[Dict]:
        """Descarga todas las leyes principales"""
        results = []
        
        for ley in self.LEYES_PRINCIPALES:
            print(f"📥 Descargando {ley['nombre']}...")
            
            try:
                response = requests.get(ley['url'], timeout=30)
                response.raise_for_status()
                
                # Guardar PDF
                filepath = self.output_dir / f"{ley['nombre']}.pdf"
                filepath.write_bytes(response.content)
                
                results.append({
                    "nombre": ley['nombre'],
                    "boe_id": ley['boe_id'],
                    "filepath": str(filepath),
                    "size_mb": len(response.content) / (1024 * 1024),
                    "status": "success"
                })
                
                print(f"✅ {ley['nombre']} descargado ({results[-1]['size_mb']:.2f} MB)")
                
            except Exception as e:
                print(f"❌ Error descargando {ley['nombre']}: {e}")
                results.append({
                    "nombre": ley['nombre'],
                    "status": "error",
                    "error": str(e)
                })
        
        return results

if __name__ == "__main__":
    downloader = BOEDownloader()
    results = downloader.download_all()
    
    print(f"\n📊 Resumen:")
    print(f"✅ Exitosos: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"❌ Errores: {sum(1 for r in results if r['status'] == 'error')}")
```

---

## 📊 ESTIMACIÓN DE TIEMPO

| Sprint | Duración | Prioridad |
|--------|----------|-----------|
| Sprint 1: Setup | 4 horas | 🔴 CRÍTICA |
| Sprint 2: Capa 1 | 2 días | 🔴 CRÍTICA |
| Sprint 3: Capa 2 | 1 día | 🟡 ALTA |
| Sprint 4: Capa 3 | 2 días | 🟡 ALTA |
| Sprint 5: API | 1 día | 🟡 ALTA |
| Sprint 6: Frontend | 1 día | 🟢 MEDIA |

**TOTAL**: 7-8 días de trabajo

---

## ✅ CRITERIOS DE ÉXITO

1. **Funcionalidad**:
   - ✅ Búsqueda funciona en 3 capas
   - ✅ Reranking por jerarquía implementado
   - ✅ Metadata correcta en todos los documentos

2. **Calidad**:
   - ✅ Score promedio >0.75 en 100 queries
   - ✅ Top-5 resultados relevantes
   - ✅ Sin errores en indexación

3. **Performance**:
   - ✅ Búsqueda <2s
   - ✅ Indexación completa <4 horas
   - ✅ Qdrant <1GB storage

4. **Documentación**:
   - ✅ README actualizado
   - ✅ API documentada
   - ✅ Tests documentados

---

## 🚀 COMANDO PARA EMPEZAR

```bash
# 1. Activar venv
cd backend
.\venv\Scripts\activate  # Windows

# 2. Instalar dependencias
pip install pypdf python-docx sentence-transformers

# 3. Verificar Qdrant
docker ps | findstr qdrant
# Si no está: docker-compose up -d qdrant

# 4. Crear colección
python setup_qdrant_collection.py
```

---

**¿Empezamos con Sprint 1?** 🚀

