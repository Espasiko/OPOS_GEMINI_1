# 🚀 SPRINT 2: Instrucciones de Ejecución

## ✅ Estado Actual

**Scripts creados**:
- ✅ `backend/agents/pdf_processor.py` - Procesa PDFs y crea chunks
- ✅ `backend/agents/robertalex_embedder.py` - Genera embeddings con RoBERTalex
- ✅ `backend/agents/indexer.py` - Indexa en Qdrant
- ✅ `backend/agents/test_search.py` - Prueba búsquedas
- ✅ `backend/index_lgss_complete.py` - Script maestro

**Datos disponibles**:
- ✅ `backend/data/leyes/LGSS.pdf` (1.69 MB)

**Infraestructura**:
- ✅ Qdrant corriendo en localhost:6333
- ✅ Colección `opositaia_leyes_seguridad_social` creada (768 dim)

---

## 📋 Pasos para Ejecutar

### Paso 1: Instalar Dependencias Nuevas

```bash
# Activar venv
cd elemplos_leyes_info
.\venv\Scripts\activate

# Instalar nuevas dependencias
pip install pypdf==5.1.0 python-docx==1.1.2 tqdm==4.66.0
```

**Tiempo estimado**: 1-2 minutos

---

### Paso 2: Verificar Qdrant

```bash
# Verificar que Qdrant está corriendo
docker ps | findstr qdrant

# Si no está corriendo, iniciarlo:
# wsl -d Ubuntu
# cd /mnt/c/Users/[tu-usuario]/opositaia
# docker-compose up -d qdrant
```

**Tiempo estimado**: 30 segundos

---

### Paso 3: Indexar LGSS (Script Maestro)

```bash
# Desde la raíz del proyecto
python backend/index_lgss_complete.py
```

**Este script hace TODO**:
1. ✅ Verifica que LGSS.pdf existe
2. ✅ Procesa el PDF (extrae texto, detecta artículos)
3. ✅ Crea chunks de 512 tokens con overlap de 50
4. ✅ Genera embeddings con RoBERTalex (768 dim)
5. ✅ Indexa en Qdrant con metadata de Capa 1
6. ✅ Muestra estadísticas finales

**Tiempo estimado**: 10-20 minutos
- Procesamiento PDF: ~2 min
- Generación embeddings: ~5-10 min (depende de tu GPU/CPU)
- Indexación Qdrant: ~2 min

**Output esperado**:
```
✅ INDEXACIÓN COMPLETADA CON ÉXITO

Colección: opositaia_leyes_seguridad_social
Total puntos: ~800-1200
Total chunks: ~800-1200
Estado: ok
```

---

### Paso 4: Probar Búsquedas

```bash
python backend/agents/test_search.py
```

**Este script**:
- Ejecuta 5 queries de prueba
- Muestra Top 3 resultados por query
- Calcula score promedio

**Tiempo estimado**: 1-2 minutos

**Output esperado**:
```
📊 RESUMEN

Queries ejecutadas: 5
Score promedio global: >0.70
Score máximo: >0.80
Score mínimo: >0.60
```

---

### Paso 5: Verificar en Qdrant UI (Opcional)

1. Abrir navegador: http://localhost:6333/dashboard
2. Seleccionar colección: `opositaia_leyes_seguridad_social`
3. Ver puntos indexados
4. Probar búsquedas manuales

---

## 🧪 Tests Individuales (Opcional)

Si quieres probar cada componente por separado:

### Test 1: PDF Processor

```bash
python backend/agents/pdf_processor.py
```

Muestra:
- Páginas extraídas
- Chunks creados
- Artículos detectados
- Ejemplos de chunks

### Test 2: RoBERTalex Embedder

```bash
python backend/agents/robertalex_embedder.py
```

Muestra:
- Modelo cargado
- Embeddings generados
- Dimensión (768)
- Similitud entre textos

### Test 3: Indexer

```bash
python backend/agents/indexer.py
```

Ejecuta el proceso completo de indexación.

---

## ❌ Solución de Problemas

### Error: "No module named 'pypdf'"

```bash
pip install pypdf==5.1.0
```

### Error: "Cannot connect to Qdrant"

```bash
# Verificar Qdrant
docker ps | findstr qdrant

# Si no está, iniciar:
wsl -d Ubuntu
docker-compose up -d qdrant
```

### Error: "Collection not found"

```bash
# Recrear colección
python backend/setup_qdrant_collection.py
```

### Error: "LGSS.pdf not found"

```bash
# Descargar LGSS
python backend/agents/download_lgss_only.py
```

---

## 📊 Métricas de Éxito

✅ **Sprint 2 completado si**:
- LGSS.pdf procesado sin errores
- ~800-1200 chunks indexados en Qdrant
- Búsquedas devuelven resultados relevantes
- Score promedio >0.70 en queries de prueba

---

## 🎯 Próximos Pasos (Sprint 3)

Una vez completado Sprint 2:

1. Descargar 7 leyes restantes del BOE
2. Indexar las 7 leyes con el mismo proceso
3. Probar búsquedas multi-ley
4. Calcular tamaño total de la colección

---

## 💡 Notas Importantes

1. **Primera ejecución es lenta**: RoBERTalex descarga el modelo (~500 MB) la primera vez
2. **GPU acelera**: Si tienes GPU NVIDIA, los embeddings serán 5-10x más rápidos
3. **Memoria**: Necesitas ~4 GB RAM disponible durante la indexación
4. **Disco**: La colección ocupará ~50-100 MB en Qdrant

---

## 📞 ¿Necesitas Ayuda?

Si algo falla:
1. Lee el mensaje de error completo
2. Verifica los pasos de "Solución de Problemas"
3. Revisa que Qdrant está corriendo
4. Verifica que el venv está activado

---

**¡Listo para ejecutar!** 🚀

Comando principal:
```bash
python backend/index_lgss_complete.py
```
