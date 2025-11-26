# 🔍 DIAGNÓSTICO COMPLETO: Sistema RAG de 3 Capas

**Fecha:** 25 Noviembre 2025  
**Problema:** Solo hay 2 capas funcionando, falta indexación correcta de leyes

---

## 📊 Estado Actual

### Qdrant Local vs Cloud

| Métrica | Local | Cloud | Estado |
|---------|-------|-------|--------|
| **Total puntos** | 7,861 | 7,833 | ⚠️ Diferencia: 28 |
| **Capas presentes** | 1, 3 | 1, 3 | ❌ Falta Capa 2 |
| **Tipos** | 7 tipos | 7 tipos | ✅ Iguales |

### Distribución por Capa

```
Capa 1 (44.7%): 447 docs
├── Tipo: ley, reglamento, constitucion
├── Problema: norma = "N/A" ❌
└── Fuente: N/A

Capa 2: ❌ NO EXISTE
└── Debería tener: Leyes del BOE estructuradas con campo "norma"

Capa 3 (55.3%): 553 docs
├── Tipo: temario, test
├── Material: PDFs de academias
└── Fuente: Academia ✅
```

### Distribución por Tipo

| Tipo | Documentos | Porcentaje |
|------|------------|------------|
| temario | 452 | 45.2% |
| ley | 327 | 32.7% |
| test | 101 | 10.1% |
| reglamento | 51 | 5.1% |
| real_decreto | 35 | 3.5% |
| ley_organica | 29 | 2.9% |
| constitucion | 5 | 0.5% |

---

## 🎯 Sistema de 3 Capas (Diseño Original)

### Capa 1: Leyes Oficiales del BOE
**Propósito:** Fuente de verdad legal  
**Contenido:**
- LGSS (Ley General Seguridad Social)
- RD 84/1996 (Afiliación)
- RD 2064/1995 (Cotización)
- RD 1415/2004 (Recaudación)
- Constitución Española
- Ley 39/2015 (Procedimiento Administrativo)
- Ley 40/2015 (Régimen Jurídico)

**Metadatos requeridos:**
```json
{
  "layer": 1,
  "tipo": "ley" | "reglamento" | "constitucion",
  "norma": "LGSS" | "RD 84/1996" | etc.,
  "articulo": "Art. 123",
  "nivel_jerarquia": 1,
  "fuente": "BOE",
  "fecha": "2015-10-30"
}
```

**Estado actual:** ❌ Tiene 447 docs pero con `norma: "N/A"`

### Capa 2: Interpretaciones y Jurisprudencia
**Propósito:** Contexto y aplicación práctica  
**Contenido:**
- Sentencias del Tribunal Supremo
- Resoluciones INSS
- Criterios interpretativos
- Doctrina administrativa

**Estado actual:** ❌ NO EXISTE

### Capa 3: Material de Estudio
**Propósito:** Preparación de oposiciones  
**Contenido:**
- Temarios de academias
- Tests con respuestas
- Casos prácticos
- Resúmenes

**Estado actual:** ✅ FUNCIONANDO (553 docs)

---

## 🚨 Problemas Identificados

### 1. Capa 1 mal indexada
**Problema:** Los 447 documentos de la Capa 1 tienen `norma: "N/A"`  
**Causa:** Se indexaron sin el campo `norma` correctamente  
**Impacto:** El RAG no puede buscar por norma específica

**Ejemplo de documento actual:**
```json
{
  "layer": 1,
  "tipo": "ley",
  "norma": "N/A",  // ❌ Debería ser "LGSS", "RD 84/1996", etc.
  "fuente": "N/A"
}
```

### 2. Capa 2 no existe
**Problema:** No hay jurisprudencia ni interpretaciones  
**Causa:** Nunca se indexó  
**Impacto:** Falta contexto para aplicación práctica

### 3. Migración incompleta
**Problema:** Faltan 28 documentos en Cloud vs Local  
**Causa:** Posible error en migración o timeout  
**Impacto:** Menor, pero indica inconsistencia

---

## ✅ Solución

### Opción 1: Re-indexar Capa 1 Correctamente (RECOMENDADO)

**Paso 1: Limpiar Capa 1 actual**
```python
# Eliminar puntos con norma="N/A" y layer=1
# O mejor: eliminar toda la colección y empezar de cero
```

**Paso 2: Indexar leyes del BOE con metadatos correctos**
```bash
# Descargar e indexar LGSS
wsl bash -c "cd backend && source venv/bin/activate && python agents/download_lgss_only.py"

# Descargar e indexar 3 leyes críticas
wsl bash -c "cd backend && source venv/bin/activate && python agents/download_and_index_3_leyes_criticas.py"

# Descargar e indexar leyes restantes
wsl bash -c "cd backend && source venv/bin/activate && python agents/download_and_index_leyes_restantes.py"
```

**Paso 3: Verificar**
```bash
python comparar_qdrant_local_vs_cloud.py
```

**Resultado esperado:**
```
Capa 1: ~5,000-10,000 docs (leyes del BOE con norma correcta)
Capa 2: 0 docs (por ahora)
Capa 3: 553 docs (temarios y tests)
Total: ~5,500-10,500 docs
```

### Opción 2: Mantener actual y añadir leyes nuevas

**Ventaja:** No pierdes lo que tienes  
**Desventaja:** Tendrás duplicados y datos inconsistentes

---

## 🎯 Plan Recomendado

### Inmediato (Hoy - 1 hora)

1. **Decidir estrategia:**
   - A) Limpiar y re-indexar todo (más limpio)
   - B) Añadir leyes nuevas (más rápido)

2. **Si eliges A (Recomendado):**
   ```bash
   # Eliminar colección actual
   # Re-indexar desde cero con scripts correctos
   ```

3. **Si eliges B:**
   ```bash
   # Ejecutar scripts de indexación
   # Aceptar que habrá inconsistencias
   ```

### Corto Plazo (Esta Semana - 2 horas)

4. **Indexar Capa 2** (jurisprudencia)
   - Buscar sentencias relevantes
   - Crear script de indexación
   - Añadir a Qdrant

5. **Verificar sistema completo**
   - Probar RAG con preguntas de cada capa
   - Verificar que devuelve fuentes correctas

---

## 📝 Scripts Disponibles

| Script | Propósito | Tiempo |
|--------|-----------|--------|
| `download_lgss_only.py` | Indexar solo LGSS | 5 min |
| `download_and_index_3_leyes_criticas.py` | 3 leyes críticas | 15 min |
| `download_and_index_leyes_restantes.py` | Resto de leyes | 30 min |
| `comparar_qdrant_local_vs_cloud.py` | Verificar contenido | 2 min |

---

## 🐛 Troubleshooting

### "norma: N/A" en resultados
**Causa:** Capa 1 mal indexada  
**Solución:** Re-indexar con scripts correctos

### "No encuentra artículos de LGSS"
**Causa:** Leyes no indexadas o mal indexadas  
**Solución:** Verificar que existen con `comparar_qdrant_local_vs_cloud.py`

### "Solo devuelve temarios"
**Causa:** Capa 3 tiene más peso que Capa 1  
**Solución:** Ajustar scoring en `rag_agent_v2.py`

---

## ✅ Checklist

- [ ] Decidir estrategia (limpiar vs añadir)
- [ ] Ejecutar scripts de indexación
- [ ] Verificar con `comparar_qdrant_local_vs_cloud.py`
- [ ] Probar RAG con pregunta sobre LGSS
- [ ] Verificar que devuelve artículos correctos
- [ ] Documentar cambios

---

**Estado:** ⚠️ CAPA 1 MAL INDEXADA  
**Prioridad:** 🔴 ALTA  
**Tiempo estimado:** 1-2 horas
