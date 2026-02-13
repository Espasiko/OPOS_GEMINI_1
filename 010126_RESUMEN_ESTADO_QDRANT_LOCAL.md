# Estado Qdrant Local - 07 Enero 2026

## Containers Docker Encontrados

### 1. Container Principal (ACTIVO)
```
Nombre: opositaia-qdrant
Imagen: qdrant/qdrant:v1.12.0
Estado: Up 5 days ✅
Volumen: opos_gemini_1_qdrant_storage
Mountpoint: /var/lib/docker/volumes/opos_gemini_1_qdrant_storage/_data
```

**Este es el Qdrant local que se está usando actualmente**

### 2. Container Antiguo (STOPPED)
```
Nombre: qdrant-local  
Imagen: qdrant/qdrant:latest
Estado: Exited (stopped 4 weeks ago)
Volumen: qdrant_storage
```

---

## Plan Qdrant Híbrido

### Opción A: Usar Container Existente
```bash
# 1. Verificar colecciones actuales
curl http://localhost:6333/collections

# 2. NO recrear - Añadir collection NUEVA con sparse
# (Mantener opositaia_knowledge actual)

# 3. Crear "opositaia_knowledge_hybrid" en paralelo
```

**Ventaja:** No perder data actual  
**Desventaja:** Requiere snapshot + re-ingestion para nueva colección

### Opción B: Nuevo Container Híbrido
```bash
# 1. Detener actual
docker stop opositaia-qdrant

# 2. Levantar Qdrant v1.16.3 NUEVO
docker run -d -p 6334:6333 \
  -v qdrant_hybrid:/qdrant/storage \
  qdrant/qdrant:v1.16.3

# 3. Crear colección híbrida + cargar snapshot
```

**Ventaja:** Clean slate, latest version  
**Desventaja:** Requiere cambiar puerto scripts

---

## Recomendación

**Opción A (más segura):**  
Mantener Qdrant local actual (puerto 6333) para desarrollo normal.  
Crear colección NUEVA híbrida en paralelo para testing comparativo.

**Próximos pasos:**
1. Verificar qué hay en colección actual
2. Cargar snapshot con sparse vectors en colección nueva
3. Comparar búsquedas: dense vs híbrido
snapshot en :  /home/spas/OPOS_GEMINI_1/gastos_ tokens/opositaia_knowledge-7212264562315011-2026-01-07-13-08-55.snapshot
---

**Test Salamandra en progreso:** Q26/140+ procesando...
