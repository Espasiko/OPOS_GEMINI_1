# 🚨 PROBLEMA: Qdrant Cloud Sin Leyes

**Fecha:** 25 Noviembre 2025  
**Problema:** Los modelos solo tienen acceso a temarios/tests, NO a las leyes del BOE

---

## 🔍 Diagnóstico

### Estado Actual de Qdrant Cloud

```
✅ Colección: opositaia_leyes_seguridad_social
📊 Total de puntos: 7,833
📚 Contenido: SOLO temarios y tests
❌ Falta: Leyes del BOE (LGSS, RD, Constitución, etc.)
```

### Ejemplo de Documento Actual

```json
{
  "layer": 3,
  "nivel_jerarquia": 3,
  "tipo": "temario",
  "fuente": "Academia",
  "material_nombre": "Temario2_Administrativos_Acceso_Libre_AGE.pdf",
  "tiene_respuestas": false,
  "page_num": 677,
  "chunk_id": 910
}
```

**❌ Falta el campo `norma`** que el RAG necesita para buscar leyes.

---

## 🎯 Causa Raíz

Cuando migraste a Qdrant Cloud (24 Nov 2025), solo migraste el contenido que tenías en Qdrant local en ese momento, que eran **temarios y tests**, pero **NO las leyes del BOE**.

Las leyes necesitan ser descargadas e indexadas desde cero en Qdrant Cloud.

---

## ✅ Solución

### Opción 1: Indexar Leyes en Qdrant Cloud (RECOMENDADO)

**Paso 1: Descargar e indexar las 3 leyes críticas**

```bash
wsl bash -c "cd backend && source venv/bin/activate && python agents/download_and_index_3_leyes_criticas.py"
```

Esto descargará e indexará:
- LGSS (Ley General de Seguridad Social)
- RD 84/1996 (Afiliación)
- RD 2064/1995 (Cotización)

**Tiempo estimado:** 10-15 minutos

**Paso 2: Descargar e indexar leyes restantes**

```bash
wsl bash -c "cd backend && source venv/bin/activate && python agents/download_and_index_leyes_restantes.py"
```

Esto descargará e indexará:
- RD 1415/2004 (Recaudación)
- Constitución Española
- Ley 39/2015 (Procedimiento Administrativo)
- Ley 40/2015 (Régimen Jurídico)
- Otras leyes relevantes

**Tiempo estimado:** 20-30 minutos

**Paso 3: Verificar contenido**

```bash
wsl bash -c "cd /mnt/e/1/OPOS_GEMINI_1 && source backend/venv/bin/activate && python verificar_qdrant_cloud.py"
```

Deberías ver:
```
📊 Total de puntos: ~15,000-20,000 (depende de las leyes)
📚 Normas encontradas:
  - LGSS
  - RD 84/1996
  - RD 2064/1995
  - RD 1415/2004
  - Constitución Española
  - ...
```

### Opción 2: Volver a Qdrant Local (NO RECOMENDADO)

Si prefieres volver a usar Qdrant local:

1. Cambiar `.env.backend`:
```bash
# Comentar Qdrant Cloud
# QDRANT_URL=https://...
# QDRANT_API_KEY=...

# Descomentar Qdrant Local
QDRANT_URL=http://localhost:6333
```

2. Reiniciar contenedor Qdrant local:
```bash
wsl docker restart opositaia-qdrant
```

3. Verificar que esté healthy:
```bash
wsl docker ps | grep qdrant
```

**Desventaja:** Pierdes los beneficios de Qdrant Cloud (backup automático, escalabilidad, etc.)

---

## 📊 Comparativa

| Aspecto | Qdrant Local | Qdrant Cloud |
|---------|--------------|--------------|
| **Coste** | €0 | €0 (free tier 1GB) |
| **Backup** | Manual | Automático |
| **Escalabilidad** | Limitada | Automática |
| **Mantenimiento** | Manual | Gestionado |
| **Latencia** | ~10-20ms | ~50-100ms |
| **Disponibilidad** | Depende de Docker | 99.9% SLA |

---

## 🚀 Plan Recomendado

### Inmediato (Hoy)

1. ✅ **Indexar 3 leyes críticas** en Qdrant Cloud (15 min)
   ```bash
   wsl bash -c "cd backend && source venv/bin/activate && python agents/download_and_index_3_leyes_criticas.py"
   ```

2. ✅ **Verificar** que el RAG funciona con las leyes
   - Hacer pregunta sobre LGSS
   - Verificar que devuelve artículos correctos

### Corto Plazo (Esta Semana)

3. ✅ **Indexar leyes restantes** (30 min)
   ```bash
   wsl bash -c "cd backend && source venv/bin/activate && python agents/download_and_index_leyes_restantes.py"
   ```

4. ✅ **Verificar contenido completo**
   ```bash
   python verificar_qdrant_cloud.py
   ```

### Medio Plazo (Próxima Semana)

5. ✅ **Automatizar actualización** de leyes del BOE
   - Crear cron job para descargar nuevas leyes
   - Actualizar índice automáticamente

---

## 🐛 Troubleshooting

### Error: "Collection already exists"
**Solución:** El script debería añadir a la colección existente, no crear una nueva.

### Error: "API key invalid"
**Solución:** Verificar que `QDRANT_API_KEY` en `.env.backend` es correcto.

### Error: "Timeout connecting to Qdrant"
**Solución:** Verificar conexión a internet y que la URL de Qdrant Cloud es correcta.

### Indexación muy lenta
**Solución:** Normal, las leyes son grandes. Esperar pacientemente.

---

## 📝 Archivos Relevantes

- `backend/.env.backend` - Configuración de Qdrant
- `backend/agents/download_and_index_3_leyes_criticas.py` - Indexar leyes críticas
- `backend/agents/download_and_index_leyes_restantes.py` - Indexar leyes restantes
- `verificar_qdrant_cloud.py` - Verificar contenido

---

## ✅ Checklist

- [ ] Ejecutar `download_and_index_3_leyes_criticas.py`
- [ ] Verificar que se indexaron correctamente
- [ ] Probar RAG con pregunta sobre LGSS
- [ ] Ejecutar `download_and_index_leyes_restantes.py`
- [ ] Verificar contenido completo con `verificar_qdrant_cloud.py`
- [ ] Probar RAG con diferentes leyes

---

**Estado:** ⚠️ PENDIENTE INDEXACIÓN  
**Prioridad:** 🔴 ALTA  
**Tiempo estimado:** 45 minutos total
