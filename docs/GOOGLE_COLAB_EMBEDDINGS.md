# 🔬 Investigación: Google Colab para Generación de Embeddings

**Fecha:** 5 de diciembre de 2025  
**Estado:** 📋 Investigación preliminar  
**Prioridad:** BAJA (CPU local funciona)

---

## 🎯 Objetivo

Evaluar si Google Colab Free Tier puede acelerar la generación de embeddings para indexación masiva de legislación (17 leyes, ~10,000 bloques estimados).

---

## 💡 Concepto

### Flujo propuesto:

```
┌─────────────────────────────────────────────────────────┐
│  1. PREPARACIÓN LOCAL                                    │
│  ├─ Descargar XMLs BOE (17 leyes)                        │
│  ├─ Parsear bloques/artículos                            │
│  └─ Exportar textos a JSON/CSV                           │
└───────────────────────┬─────────────────────────────────┘
                        │ Upload a Google Drive
┌───────────────────────▼─────────────────────────────────┐
│  2. GOOGLE COLAB (GPU T4 gratis)                         │
│  ├─ Montar Google Drive                                  │
│  ├─ Cargar modelo pablosi/bge-m3-spa-law-qa-trained-2   │
│  ├─ Leer textos desde Drive                              │
│  ├─ Generar embeddings en batch (GPU)                    │
│  └─ Guardar embeddings en Drive (numpy/pickle)           │
└───────────────────────┬─────────────────────────────────┘
                        │ Download desde Drive
┌───────────────────────▼─────────────────────────────────┐
│  3. INDEXACIÓN LOCAL                                     │
│  ├─ Leer embeddings pre-computados                       │
│  ├─ Cargar en Qdrant (sin generar embeddings)           │
│  └─ Solo metadata + vectores                             │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 Hallazgos Investigación

### Notebook HuggingFace Mencionado

**URL documentada:**
```
https://colab.research.google.com/#fileId=https://huggingface.co/littlejohn-ai/bge-m3-spa-law-qa.ipynb
```

**Estado:** ❌ **No encontrado** (error 404)

**Motivo probable:**
- Notebook no publicado en el repo HF
- URL placeholder en documentación
- Autor no creó demo Colab público

### Google Colab Free Tier - Especificaciones

**GPU disponible:**
- Tesla T4 (16GB VRAM)
- 12GB RAM sistema
- 78GB disco temporal

**Límites:**
- 12 horas max por sesión
- Desconexión tras 90 min inactividad
- Uso acumulado semanal limitado (no especificado)

**Ventajas:**
- ✅ GPU gratis (10-50x más rápido que CPU)
- ✅ No consume recursos locales
- ✅ Ideal para batch procesamiento

**Desventajas:**
- ❌ No persistente (datos se pierden al cerrar)
- ❌ Upload/download manual via Drive
- ❌ No automatizable (requiere interacción UI)
- ❌ No apto para actualizaciones incrementales

---

## 📊 Comparación: CPU Local vs GPU Colab

### Escenario: Indexar 17 leyes (~10,000 bloques)

#### Opción A: CPU Local (actual)

**Hardware:**
- 16GB RAM
- CPU Intel/AMD estándar
- Modelo: pablosi/bge-m3-spa-law-qa-trained-2

**Rendimiento medido:**
- ~4 minutos / 50 bloques LGSS
- Estimación: **~800 minutos (13 horas)** para 10,000 bloques

**Ventajas:**
- ✅ Automatizable con scripts Python
- ✅ Puede ejecutarse background/overnight
- ✅ No requiere upload/download
- ✅ Apto para updates incrementales

**Desventajas:**
- ❌ Lento (13 horas estimadas)
- ❌ Bloquea laptop durante ejecución

#### Opción B: GPU Google Colab

**Hardware:**
- Tesla T4 GPU (16GB VRAM)
- Colab Pro: A100/V100 disponibles ($10/mes)

**Rendimiento estimado:**
- GPU T4: **10-20x más rápido** que CPU
- Estimación: **40-80 minutos** para 10,000 bloques
- Con A100 (Colab Pro): **15-30 minutos**

**Ventajas:**
- ✅ 10-20x más rápido
- ✅ No consume recursos locales
- ✅ Ideal para indexación inicial masiva

**Desventajas:**
- ❌ Requiere upload XMLs a Drive (~50MB)
- ❌ Requiere download embeddings (~400MB para 10K bloques)
- ❌ No automatizable (UI Colab manual)
- ❌ Límite 12h por sesión
- ❌ No apto para updates diarios incrementales

---

## 🛠️ Implementación Propuesta

### Notebook Colab a Crear

**Archivo:** `notebooks/generar_embeddings_colab.ipynb`

```python
# Celda 1: Setup
!pip install sentence-transformers qdrant-client

# Celda 2: Montar Drive
from google.colab import drive
drive.mount('/content/drive')

# Celda 3: Cargar modelo
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")

# Celda 4: Leer textos desde Drive
import json
with open('/content/drive/MyDrive/opositaia/bloques_leyes.json', 'r') as f:
    bloques = json.load(f)  # [{id, texto, titulo, ley}, ...]

# Celda 5: Generar embeddings en batch
embeddings = []
batch_size = 32

for i in range(0, len(bloques), batch_size):
    batch = bloques[i:i+batch_size]
    textos = [b['texto'] for b in batch]
    batch_embeddings = model.encode(textos, show_progress_bar=True)
    embeddings.extend(batch_embeddings)
    
    if i % 500 == 0:
        print(f"Procesados {i}/{len(bloques)} bloques")

# Celda 6: Guardar embeddings
import numpy as np
np.save('/content/drive/MyDrive/opositaia/embeddings.npy', np.array(embeddings))

# Celda 7: Guardar metadata
with open('/content/drive/MyDrive/opositaia/metadata.json', 'w') as f:
    json.dump(bloques, f, ensure_ascii=False, indent=2)

print(f"✅ {len(embeddings)} embeddings guardados en Drive")
```

### Script Local Indexación

**Archivo:** `backend/agents/index_from_precomputed_embeddings.py`

```python
import numpy as np
import json
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

# Leer embeddings pre-computados desde Colab
embeddings = np.load('data/embeddings_colab.npy')
with open('data/metadata_colab.json', 'r') as f:
    bloques = json.load(f)

# Conectar Qdrant
client = QdrantClient("http://localhost:6333")

# Crear colección
client.create_collection(
    collection_name="opositaia_leyes_completa",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

# Indexar solo metadata + vectores (sin generar embeddings)
points = []
for i, (bloque, embedding) in enumerate(zip(bloques, embeddings)):
    points.append(PointStruct(
        id=i,
        vector=embedding.tolist(),
        payload=bloque
    ))
    
    if len(points) >= 100:
        client.upsert(collection_name="opositaia_leyes_completa", points=points)
        points = []
        print(f"Indexados {i+1}/{len(bloques)} bloques")

# Indexar restantes
if points:
    client.upsert(collection_name="opositaia_leyes_completa", points=points)

print(f"✅ Indexación completada: {len(bloques)} bloques")
```

---

## 🎯 Recomendación

### Para Sprint 2 (actual): ❌ NO usar Colab

**Razones:**
1. Solo 567 bloques LGSS (estimación: 25 min CPU local)
2. Overhead upload/download no justifica ahorro de tiempo
3. Automatización más valiosa que velocidad pura
4. CPU local puede ejecutarse overnight sin supervisión

### Para Sprint 3 (indexación masiva 17 leyes): ✅ CONSIDERAR Colab

**Razones:**
1. 10,000+ bloques estimados (13h CPU vs 1h GPU)
2. Ahorro de 12 horas justifica 30 min setup
3. Colab Free suficiente (no requiere Pro)
4. Script Python reutilizable para futuras leyes

---

## 📋 Tareas Pendientes (Si se decide usar Colab)

1. **Crear notebook Colab** `generar_embeddings_colab.ipynb`
2. **Exportar bloques a JSON** desde XMLs BOE
3. **Upload JSON a Google Drive** (~50MB)
4. **Ejecutar notebook** en Colab (1-2h con T4)
5. **Download embeddings** desde Drive (~400MB)
6. **Crear script indexación** pre-computed embeddings
7. **Indexar en Qdrant** local/cloud

**Estimación total:** 3-4 horas (vs 13h CPU directo)

---

## 🔗 Referencias

- **Colab Free Tier:** https://colab.research.google.com/
- **Colab Pro:** https://colab.research.google.com/signup (GPU A100/V100, $10/mes)
- **Sentence Transformers en Colab:** https://www.sbert.net/docs/training/overview.html
- **Qdrant Batch Indexing:** https://qdrant.tech/documentation/concepts/points/

---

## ✅ Conclusión

**Estado actual:** No urgente, CPU local suficiente para desarrollo

**Cuándo usar Colab:**
- Indexación masiva (>5,000 bloques)
- Re-indexación completa necesaria
- Experimentos con múltiples modelos embedding
- Dataset fine-tuning generation (fase 2 proyecto)

**Cuándo NO usar Colab:**
- Updates incrementales diarios
- <1,000 bloques
- Automatización crítica
- Pipeline CI/CD

---

**Fecha:** 5 de diciembre de 2025  
**Autor:** AI Assistant  
**Revisión:** Pendiente validar con prueba real Colab
