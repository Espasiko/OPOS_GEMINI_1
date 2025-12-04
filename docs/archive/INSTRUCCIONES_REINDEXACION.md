# 📚 INSTRUCCIONES: Re-indexación Completa de Leyes

**Fecha:** 25 Noviembre 2025  
**Objetivo:** Limpiar Qdrant Cloud y re-indexar las 13 leyes correctamente

---

## 🎯 ¿Qué hace este proceso?

1. **Limpia Qdrant Cloud** - Elimina TODOS los datos actuales (7,833 docs mal indexados)
2. **Descarga 13 leyes del BOE** - PDFs consolidados oficiales
3. **Procesa y chunka** - Divide en fragmentos de 512 tokens
4. **Genera embeddings** - Usa RoBERTalex (modelo legal español)
5. **Indexa en Qdrant Cloud** - Con metadatos correctos (norma, artículo, etc.)

---

## ⏱️ Tiempo Estimado

- **Limpieza:** 30 segundos
- **Indexación:** 1-2 horas (depende de conexión)
- **Total:** ~1-2 horas

---

## 📋 Requisitos Previos

✅ Backend corriendo (para mantener el servicio)  
✅ Conexión a internet estable  
✅ Espacio en disco: ~200 MB  
✅ Variables de entorno configuradas en `backend/.env.backend`:
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `COLLECTION_NAME`

---

## 🚀 Opción 1: Script Automático (RECOMENDADO)

### Ejecutar todo de una vez:

```bash
wsl bash reindexar_leyes_completo.sh
```

Este script:
1. Te pedirá confirmación (escribe `SI`)
2. Limpiará Qdrant Cloud
3. Indexará las 13 leyes automáticamente
4. Mostrará progreso en tiempo real

**Ventajas:**
- ✅ Proceso automatizado
- ✅ Manejo de errores
- ✅ Progreso visible

---

## 🔧 Opción 2: Paso a Paso (Manual)

### Paso 1: Limpiar Qdrant Cloud

```bash
wsl bash -c "cd /mnt/e/1/OPOS_GEMINI_1 && source backend/venv/bin/activate && python limpiar_qdrant_cloud.py"
```

**Confirmación requerida:** Escribe `SI` cuando te lo pida

**Output esperado:**
```
🗑️  LIMPIAR QDRANT CLOUD
⚠️  ADVERTENCIA: Esto eliminará TODA la colección
✅ Colección eliminada exitosamente
📊 Documentos eliminados: 7,833
```

### Paso 2: Indexar las 13 leyes

```bash
wsl bash -c "cd /mnt/e/1/OPOS_GEMINI_1 && source backend/venv/bin/activate && python backend/agents/indexar_todas_las_leyes.py"
```

**Output esperado:**
```
📚 INDEXACIÓN COMPLETA DE LEYES Y REGLAMENTOS
Total: 13 leyes (5 críticas + 5 altas + 3 medias)

🔴 PRIORIDAD CRÍTICA (5 leyes)
📄 LEY 1/5: RDL 8/2015 - Ley General Seguridad Social
⏳ Descargando desde BOE...
✅ Descargado: 2.5 MB
📖 Extrayendo texto del PDF...
✅ Texto extraído: 1,234,567 caracteres
✂️  Creando chunks...
✅ Chunks creados: 2,456
💾 Indexando en Qdrant Cloud...
✅ Indexación completada: 2,456 chunks
...
```

---

## 📊 Leyes que se Indexarán

### 🔴 CRÍTICAS (5 leyes)
1. ✅ LGSS (RDL 8/2015)
2. ✅ RD 84/1996 (Afiliación)
3. ✅ RD 2064/1995 (Cotización)
4. ✅ RD 1415/2004 (Recaudación)
5. ✅ Constitución Española

### 🟠 ALTAS (5 leyes)
6. ✅ Ley 39/2015 (Procedimiento Administrativo)
7. ✅ Ley 40/2015 (Régimen Jurídico)
8. ✅ RDL 5/2015 (EBEP)
9. ✅ RD 1430/2009 (Incapacidad Temporal)
10. ✅ RD 1300/1995 (Incapacidad Permanente)

### 🟡 MEDIAS (3 leyes)
11. ✅ Ley 19/2021 (IMV)
12. ✅ LO 3/2018 (LOPDGDD)
13. ✅ Ley 39/2006 (Dependencia)

---

## ✅ Verificación

### Después de la indexación, verifica:

```bash
wsl bash -c "cd /mnt/e/1/OPOS_GEMINI_1 && source backend/venv/bin/activate && python comparar_qdrant_local_vs_cloud.py"
```

**Output esperado:**
```
📊 ESTADÍSTICAS CLOUD
📈 Total de puntos: ~20,000
🔢 DISTRIBUCIÓN POR CAPA:
   Capa 1: ~20,000 docs (100%)
📑 DISTRIBUCIÓN POR TIPO:
   ley: ~12,000 docs
   reglamento: ~7,000 docs
   constitucion: ~1,000 docs
📚 TOP 10 NORMAS:
   LGSS: ~2,500 docs
   RD_84_1996: ~1,800 docs
   ...
```

**✅ Verificar que NO hay `norma: "N/A"`**

---

## 🧪 Probar el RAG

### Prueba 1: LGSS
```bash
# En el frontend, hacer pregunta:
"¿Qué dice el artículo 161 de la LGSS sobre incapacidad temporal?"
```

**Resultado esperado:**
- ✅ Devuelve artículo 161 de LGSS
- ✅ Fuente: "LGSS - Art. 161"
- ✅ Contenido correcto sobre IT

### Prueba 2: Constitución
```bash
"¿Qué dice el artículo 41 de la Constitución?"
```

**Resultado esperado:**
- ✅ Devuelve artículo 41 CE
- ✅ Fuente: "Constitución - Art. 41"
- ✅ Contenido sobre derecho a Seguridad Social

### Prueba 3: Reglamento
```bash
"¿Cómo funciona la afiliación según el RD 84/1996?"
```

**Resultado esperado:**
- ✅ Devuelve artículos del RD 84/1996
- ✅ Fuente: "RD_84_1996 - Art. X"
- ✅ Contenido sobre afiliación

---

## 🐛 Troubleshooting

### Error: "No module named 'pypdf'"
```bash
wsl bash -c "cd backend && source venv/bin/activate && pip install pypdf"
```

### Error: "Connection timeout"
**Causa:** Conexión lenta o BOE caído  
**Solución:** Esperar y reintentar

### Error: "API key invalid"
**Causa:** API key incorrecta en `.env.backend`  
**Solución:** Verificar `QDRANT_API_KEY`

### Error: "Out of memory"
**Causa:** RoBERTalex consume mucha RAM  
**Solución:** Cerrar otras aplicaciones

### Indexación muy lenta
**Normal:** Cada ley tarda 5-15 minutos  
**Solución:** Dejar corriendo y esperar pacientemente

---

## 📝 Archivos Creados

| Archivo | Propósito |
|---------|-----------|
| `limpiar_qdrant_cloud.py` | Elimina colección de Qdrant Cloud |
| `backend/agents/indexar_todas_las_leyes.py` | Indexa las 13 leyes |
| `reindexar_leyes_completo.sh` | Script automático completo |
| `comparar_qdrant_local_vs_cloud.py` | Verifica contenido |

---

## 🎯 Resultado Final Esperado

```
📊 Qdrant Cloud después de indexación:
   Total puntos: ~20,000
   Capa 1: 100% (leyes del BOE)
   Capa 2: 0% (jurisprudencia - futuro)
   Capa 3: 0% (temarios - re-añadir después)
   
   Distribución por norma:
   - LGSS: ~2,500 docs
   - RD 84/1996: ~1,800 docs
   - RD 2064/1995: ~1,600 docs
   - RD 1415/2004: ~1,400 docs
   - Constitución: ~1,000 docs
   - Ley 39/2015: ~2,200 docs
   - Ley 40/2015: ~2,000 docs
   - RDL 5/2015: ~1,800 docs
   - RD 1430/2009: ~1,200 docs
   - RD 1300/1995: ~1,100 docs
   - Ley 19/2021: ~900 docs
   - LO 3/2018: ~1,000 docs
   - Ley 39/2006: ~1,500 docs
```

---

## 💡 Añadir Más Leyes Después

**Sí, puedes añadir más leyes sin duplicados** porque cada documento tiene un ID único.

Para añadir una ley nueva:

1. Añade la ley a la lista `LEYES_TODAS` en `indexar_todas_las_leyes.py`
2. Ejecuta solo esa ley (modifica el script para procesar solo la nueva)
3. O ejecuta todo el script (detectará las existentes y las saltará)

**Ejemplo:**
```python
# Añadir al final de LEYES_TODAS
{
    "nombre": "Nueva_Ley",
    "nombre_completo": "Ley XX/YYYY",
    "boe_id": "BOE-A-YYYY-XXXXX",
    "url": "https://www.boe.es/...",
    "tipo": "ley",
    "nivel_jerarquia": 1,
    "fecha": "YYYY-MM-DD",
    "prioridad": "media"
}
```

---

## ✅ Checklist

- [ ] Backend corriendo
- [ ] Variables de entorno configuradas
- [ ] Ejecutar `limpiar_qdrant_cloud.py`
- [ ] Confirmar limpieza (escribir `SI`)
- [ ] Ejecutar `indexar_todas_las_leyes.py`
- [ ] Esperar 1-2 horas
- [ ] Verificar con `comparar_qdrant_local_vs_cloud.py`
- [ ] Probar RAG con 3 preguntas diferentes
- [ ] Verificar que NO hay `norma: "N/A"`
- [ ] Documentar resultados

---

**Estado:** ⏳ LISTO PARA EJECUTAR  
**Tiempo estimado:** 1-2 horas  
**Prioridad:** 🔴 ALTA
