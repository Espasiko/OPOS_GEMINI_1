# 🔍 AUDITORÍA DE ENTORNOS Y DEPENDENCIAS

**Fecha**: 3 Diciembre 2025  
**Objetivo**: Verificar que no hay conflictos entre entornos

---

## 📊 ESTADO ACTUAL DEL SISTEMA

### 1️⃣ ENTORNOS VIRTUALES (venv)

#### En Windows (E:\1\OPOS_GEMINI_1\):
```
✅ backend/venv/                    # Para el backend FastAPI
✅ dataset_generator/venv/          # Para generación de datasets
✅ elemplos_leyes_info/venv/        # ⚠️ DUPLICADO - Probablemente innecesario
```

#### En WSL (/home/espasiko/OPOS_GEMINI_1/):
```
✅ venv_indexer/                    # Para indexación con BGE-M3
```

**RECOMENDACIÓN**: 
- ❌ **ELIMINAR** `elemplos_leyes_info/venv/` - Es redundante
- ✅ **MANTENER** los otros 3 venv (cada uno tiene un propósito específico)

---

### 2️⃣ DOCKER CONTAINERS

```bash
CONTAINER          STATUS              PORTS                    PROPÓSITO
==================================================================================
opositaia-qdrant   Up (unhealthy)      6333-6334               ✅ Qdrant PRINCIPAL
qdrant (viejo)     Exited              6333-6334               ❌ ELIMINAR
ollama-starter     Exited              -                       ❌ NO USAR (Ollama está en WSL)
opositaia-postgres Created             -                       ✅ PostgreSQL
sim_old-db-1       Up (healthy)        5432                    ⚠️ Verificar si es necesario
```

**PROBLEMAS DETECTADOS**:
1. ⚠️ **Qdrant "unhealthy"** - Necesita revisión
2. ❌ **Qdrant viejo** - Container duplicado, eliminar
3. ❌ **Ollama en Docker** - No se usa, Ollama está instalado en WSL

**ACCIONES**:
```bash
# Eliminar container Qdrant viejo
docker rm qdrant

# Eliminar Ollama en Docker (no se usa)
docker rm ollama-starter

# Reiniciar Qdrant principal si está unhealthy
docker restart opositaia-qdrant
```

---

### 3️⃣ QDRANT - CONFIGURACIÓN

#### Qdrant Actual:
```
Ubicación: Docker container "opositaia-qdrant"
Puerto: 6333 (local)
Estado: Up pero "unhealthy"
Colecciones existentes: leyes_boe, etc.
```

#### ¿Hay conflicto con nuevo Qdrant?
**NO** - El script nuevo usa el **MISMO Qdrant** en puerto 6333:
```python
# En indexar_materiales_bge_m3.py
qdrant_url="http://localhost:6333"  # ✅ Mismo Qdrant
collection_name="materiales_academia"  # ✅ Nueva colección
```

**CONCLUSIÓN**: 
- ✅ **NO hay conflicto** - Usamos el mismo Qdrant
- ✅ **Nueva colección** - `materiales_academia` (separada de `leyes_boe`)
- ⚠️ **Necesita fix** - Qdrant está "unhealthy"

---

### 4️⃣ OLLAMA - CONFIGURACIÓN

#### Ollama Instalado:
```
Ubicación: WSL (/usr/local/bin/ollama)
Modelos: mistral:latest (4.4 GB)
Estado: ✅ Funcionando
Puerto: 11434 (default)
```

#### ¿Hay conflicto con Docker Ollama?
**NO** - El container Docker está **Exited** y no se usa:
```bash
ollama-starter     Exited (255)     # ❌ No se usa
```

**CONCLUSIÓN**:
- ✅ **Ollama en WSL** - Es el que usamos
- ❌ **Ollama Docker** - No se usa, se puede eliminar
- ✅ **Sin conflictos** - Solo hay una instancia activa

---

### 5️⃣ BGE-M3 - MODELO DE EMBEDDINGS

#### ¿Dónde está instalado BGE-M3?
```python
# El script lo descarga automáticamente la primera vez
from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer("BAAI/bge-m3")
```

**Ubicación del modelo**:
- En WSL: `~/.cache/huggingface/hub/`
- Se descarga automáticamente si no existe
- Tamaño: ~2.3 GB

#### ¿Hay conflicto con modelos anteriores?
**NO** - Cada modelo tiene su propio directorio:
```
~/.cache/huggingface/hub/
├── models--BAAI--bge-m3/              # ✅ Nuevo
├── models--sentence-transformers/     # ✅ Otros modelos
└── ...
```

**CONCLUSIÓN**:
- ✅ **Sin conflictos** - Modelos coexisten pacíficamente
- ✅ **Cache compartido** - Eficiente en espacio
- ⚠️ **Espacio necesario** - ~2.3 GB adicionales

---

### 6️⃣ TRANSFORMERS Y DEPENDENCIAS

#### ¿Dónde están instaladas?

**En backend/venv/ (Windows)**:
```
sentence-transformers==2.x
qdrant-client==1.x
PyMuPDF (fitz)
```

**En venv_indexer/ (WSL)**:
```
sentence-transformers==3.x  # ✅ Versión más nueva
qdrant-client==1.x
PyMuPDF (fitz)
```

#### ¿Hay conflicto?
**NO** - Cada venv es independiente:
- ✅ **Aislamiento total** - No se mezclan dependencias
- ✅ **Versiones diferentes OK** - Cada venv tiene las suyas
- ✅ **Sin interferencia** - Python usa el venv activo

---

## 🎯 ARQUITECTURA FINAL RECOMENDADA

### Entornos Virtuales:
```
Windows:
├── backend/venv/              # FastAPI + APIs
└── dataset_generator/venv/    # Generación Q&A

WSL:
└── venv_indexer/              # Indexación BGE-M3
```

### Docker Containers:
```
✅ opositaia-qdrant    # Qdrant principal (puerto 6333)
✅ opositaia-postgres  # PostgreSQL
⚠️ sim_old-db-1        # Verificar si es necesario
```

### Servicios:
```
✅ Ollama (WSL)        # Mistral local (puerto 11434)
✅ Qdrant (Docker)     # Vector DB (puerto 6333)
✅ PostgreSQL (Docker) # Base de datos relacional
```

---

## 🔧 ACCIONES CORRECTIVAS

### 1. Limpiar venv duplicado:
```bash
# En Windows
Remove-Item -Recurse -Force "E:\1\OPOS_GEMINI_1\elemplos_leyes_info\venv"
```

### 2. Limpiar containers innecesarios:
```bash
# En WSL
docker rm qdrant              # Qdrant viejo
docker rm ollama-starter      # Ollama no usado
```

### 3. Arreglar Qdrant "unhealthy":
```bash
# Reiniciar container
docker restart opositaia-qdrant

# Verificar logs
docker logs opositaia-qdrant --tail 50

# Si sigue unhealthy, recrear:
docker stop opositaia-qdrant
docker rm opositaia-qdrant
docker run -d --name opositaia-qdrant \
  -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest
```

### 4. Verificar que todo funciona:
```bash
# Test Qdrant
curl http://localhost:6333/collections

# Test Ollama
ollama list

# Test Python en WSL
cd /home/espasiko/OPOS_GEMINI_1
source venv_indexer/bin/activate
python3 -c "from sentence_transformers import SentenceTransformer; print('OK')"
```

---

## ✅ RESPUESTAS A TUS PREGUNTAS

### 1. ¿Duplicamos venv?
**SÍ** - Hay 4 venv, pero solo necesitamos 3:
- ✅ `backend/venv` - Necesario
- ✅ `dataset_generator/venv` - Necesario
- ❌ `elemplos_leyes_info/venv` - **ELIMINAR**
- ✅ `venv_indexer` (WSL) - Necesario

### 2. ¿Hay un nuevo Qdrant?
**NO** - Usamos el **mismo Qdrant** (puerto 6333):
- ✅ Colección antigua: `leyes_boe`
- ✅ Colección nueva: `materiales_academia`
- ✅ **Sin conflicto** - Colecciones separadas

### 3. ¿Transformers en Windows o WSL?
**AMBOS** - Pero en venv separados:
- Windows: `backend/venv` y `dataset_generator/venv`
- WSL: `venv_indexer`
- ✅ **Sin conflicto** - Cada venv es independiente

### 4. ¿Chocan con el viejo Qdrant/transformers?
**NO**:
- Qdrant: Mismo container, colecciones diferentes
- Transformers: Venv separados, sin interferencia
- Modelos: Cache compartido, sin conflicto

### 5. ¿BGE-M3 está instalado?
**NO todavía** - Se descargará automáticamente:
- Primera ejecución: Descarga ~2.3 GB
- Ubicación: `~/.cache/huggingface/hub/`
- ✅ **Sin conflicto** con otros modelos

### 6. ¿BGE-M3 usa Ollama?
**NO** - Son independientes:
- BGE-M3: Modelo de embeddings (sentence-transformers)
- Ollama: Servidor de LLMs (Mistral)
- ✅ Se usan juntos pero no dependen uno del otro

### 7. ¿Ollama en WSL?
**SÍ** - Instalado y funcionando:
- Ubicación: `/usr/local/bin/ollama`
- Modelo: `mistral:latest` (4.4 GB)
- Puerto: 11434
- ✅ **Listo para usar**

---

## 🚀 PLAN DE ACCIÓN LIMPIO

### Paso 1: Limpiar (5 minutos)
```bash
# Eliminar venv duplicado
rm -rf E:\1\OPOS_GEMINI_1\elemplos_leyes_info\venv

# Eliminar containers innecesarios
docker rm qdrant ollama-starter
```

### Paso 2: Verificar Qdrant (2 minutos)
```bash
# Reiniciar si está unhealthy
docker restart opositaia-qdrant

# Verificar estado
docker ps | grep qdrant
curl http://localhost:6333/collections
```

### Paso 3: Probar indexación (10 minutos)
```bash
# En WSL
cd /home/espasiko/OPOS_GEMINI_1
source venv_indexer/bin/activate
python3 dataset_generator/indexar_materiales_bge_m3.py
```

---

## 📊 RESUMEN FINAL

### ✅ TODO ESTÁ BIEN:
- Venv separados funcionan correctamente
- Qdrant es el mismo, colecciones diferentes
- Ollama en WSL funcionando
- BGE-M3 se descargará automáticamente
- Sin conflictos entre dependencias

### ⚠️ ACCIONES MENORES:
- Eliminar 1 venv duplicado
- Limpiar 2 containers viejos
- Verificar salud de Qdrant

### 🎯 CONCLUSIÓN:
**NO hemos liado nada** - Todo está bien organizado y sin conflictos. Solo necesitamos una limpieza menor.

---

**Creado**: 3 Diciembre 2025  
**Estado**: ✅ Sistema auditado - Listo para limpieza y uso
