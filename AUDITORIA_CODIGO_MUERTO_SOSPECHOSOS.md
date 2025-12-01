# Auditoría de Código Muerto y Basura - Lista de Sospechosos

**Fecha:** 30 de noviembre de 2025  
**Estado:** 🔍 ANÁLISIS COMPLETO - SIN CAMBIOS REALIZADOS

## ⚠️ IMPORTANTE
Esta es solo una lista de archivos SOSPECHOSOS. NO se han realizado cambios todavía.
Requiere revisión manual antes de eliminar cualquier archivo.

---

## 🔴 ALTA PRIORIDAD - Muy Probablemente Obsoletos

### Backend Routers - Duplicados

#### 1. `backend/routers/rag.py` vs `backend/routers/rag_v2.py`
**Sospecha:** Versión antigua vs nueva
- ✅ `rag_v2.py` - Versión actual (prefix="/api/v2/rag")
- ⚠️ `rag.py` - Versión antigua (prefix="/api/rag")
- **Acción sugerida:** Verificar si `rag.py` todavía se usa en main.py

### Scripts de Indexación - Múltiples Versiones

#### 2. Scripts de descarga/indexación en `backend/agents/`
**Sospecha:** Múltiples scripts que hacen lo mismo

Scripts de descarga:
- ⚠️ `download_constitucion.py` - Script específico
- ⚠️ `download_lgss_only.py` - Script específico
- ⚠️ `download_and_index_3_leyes_criticas.py` - Script específico
- ⚠️ `download_and_index_leyes_restantes.py` - Script específico
- ⚠️ `boe_downloader.py` - ¿Downloader genérico?

Scripts de indexación:
- ⚠️ `indexar_4_leyes_temario.py` - Script específico
- ⚠️ `indexar_leyes_faltantes.py` - Script específico
- ✅ `indexar_todas_las_leyes.py` - **Probablemente el único necesario**
- ⚠️ `reindexar_imv.py` - Script específico

Scripts de corrección:
- ⚠️ `fix_rd_cotizacion.py` - Fix específico
- ⚠️ `index_rd_cotizacion_final.py` - Fix específico

**Acción sugerida:** Consolidar en un solo script genérico o mover a carpeta `scripts/one-time/`

#### 3. `backend/agents/rag_agent.py` vs `backend/agents/rag_agent_v2.py`
**Sospecha:** Versión antigua vs nueva
- ✅ `rag_agent_v2.py` - Versión actual
- ⚠️ `rag_agent.py` - Versión antigua
- **Acción sugerida:** Verificar imports en routers

### Scripts de Testing en Raíz

#### 4. Scripts de test en raíz del proyecto
**Sospecha:** Tests antiguos o de desarrollo

- ⚠️ `test_e2e_simple.py` - Test E2E
- ⚠️ `test_e2e_completo.py` - Test E2E
- ⚠️ `test_qdrant_cloud_e2e.py` - Test específico
- ⚠️ `test_rag_simple.py` - Test específico
- ⚠️ `test_rag_leyes_nuevas.py` - Test específico
- ⚠️ `test_imv_final.py` - Test específico
- ⚠️ `test_mock_exam_generation.py` - Test específico

**Acción sugerida:** Mover a `backend/tests/` o eliminar si están obsoletos

### Scripts de Utilidad en Raíz

#### 5. Scripts de utilidad/verificación en raíz
**Sospecha:** Scripts de desarrollo temporal

- ⚠️ `check_database.sh` - Script de verificación
- ⚠️ `check_qdrant_status.py` - Script de verificación
- ⚠️ `comparar_qdrant_local_vs_cloud.py` - Script de comparación
- ⚠️ `limpiar_qdrant_cloud.py` - Script de limpieza
- ⚠️ `verificar_qdrant_cloud.py` - Script de verificación
- ⚠️ `verificar_estado_completo.py` - Script de verificación
- ⚠️ `verificar_leyes_temario_oficial.py` - Script de verificación
- ⚠️ `verificacion_completa_qdrant.py` - Script de verificación
- ⚠️ `monitorear_indexacion.py` - Script de monitoreo
- ⚠️ `detectar_leyes_faltantes.py` - Script de detección
- ⚠️ `crear_indice_norma.py` - Script de creación

**Acción sugerida:** Mover a `backend/scripts/` o `tools/`

---

## 🟡 MEDIA PRIORIDAD - Posiblemente Obsoletos

### Documentos de Sesiones Antiguas

#### 6. Documentos de resumen de sesiones
**Sospecha:** Documentación histórica que podría archivarse

- ⚠️ `RESUMEN_SESION_23_NOV_2025.md`
- ⚠️ `RESUMEN_SESION_24_NOV_2025.md`
- ⚠️ `RESUMEN_SESION_25_NOV_2025.md`
- ⚠️ `RESUMEN_FINAL_SESION_27NOV.md`
- ⚠️ `RESUMEN_INDEXACION_COMPLETA_27NOV.md`
- ⚠️ `COMMIT_EXITOSO_25_NOV.md`

**Acción sugerida:** Mover a `docs/sesiones/` o `docs/historico/`

### Documentos de Análisis Completados

#### 7. Análisis y evaluaciones completadas
**Sospecha:** Documentación de decisiones ya tomadas

- ⚠️ `ANALISIS_CODIGO_PRE_CORRECCION.md`
- ⚠️ `ANALISIS_CLOUDFLARE_VS_VERCEL.md`
- ⚠️ `ANALISIS_COSTES_REALES_Y_FINETUNING.md`
- ⚠️ `ANALISIS_MODELOS_EMBEDDINGS_LEGAL_ES.md`
- ⚠️ `COMPARACION_PROPUESTAS_GEMINI_VS_ACTUAL.md`
- ⚠️ `EVALUACION_CLOUDFLARE_WORKERS_AI_DETALLADA.md`
- ⚠️ `EVALUACION_HERRAMIENTAS_AUDITORIA_CODIGO.md`
- ⚠️ `EVALUACION_MEJORAS_PROPUESTAS.md`

**Acción sugerida:** Mover a `docs/analisis/` o `docs/decisiones/`

### Documentos de Correcciones Completadas

#### 8. Documentos de correcciones ya aplicadas
**Sospecha:** Documentación de trabajo ya completado

- ⚠️ `CORRECCIONES_CODIGO_COMPLETADAS.md`
- ⚠️ `CORRECCION_PLAN_INCONSISTENCIAS.md`
- ⚠️ `CORRECCION_UX_MAPAS_MENTALES.md`
- ⚠️ `AUDITORIA_ESTADO_REAL_Y_CORRECCIONES.md`

**Acción sugerida:** Mover a `docs/correcciones/` o archivar

### Documentos de Sprints Completados

#### 9. Documentos de sprints antiguos
**Sospecha:** Documentación histórica

- ⚠️ `SPRINT8_COMPLETADO.md`
- ⚠️ `SPRINT9_COMPLETADO.md`
- ⚠️ `SPRINT10_COMPLETADO.md`
- ⚠️ `SPRINT11_COMPLETADO.md`

**Acción sugerida:** Mover a `docs/sprints/` o mantener solo el más reciente

### Documentos de Problemas Resueltos

#### 10. Documentos de problemas ya solucionados
**Sospecha:** Documentación de issues cerrados

- ⚠️ `PROBLEMA_QDRANT_CLOUD_SIN_LEYES.md`
- ⚠️ `SOLUCION_PROBLEMA_MODELOS.md`
- ⚠️ `DIAGNOSTICO_COMPLETO_RAG_3_CAPAS.md`
- ⚠️ `DIAGNOSTICO_FRONTEND.md`

**Acción sugerida:** Mover a `docs/problemas-resueltos/`

### Documentos de Verificaciones Completadas

#### 11. Documentos de verificaciones ya hechas
**Sospecha:** Documentación de checks completados

- ⚠️ `VERIFICACION_INTEGRACION_DB.md`
- ⚠️ `VERIFICACION_LEYES_TEMARIO.md`
- ⚠️ `VERIFICACION_PRE_COMMIT.md`
- ⚠️ `REINDEXACION_IMV_COMPLETADA.md`

**Acción sugerida:** Mover a `docs/verificaciones/`

---

## 🟢 BAJA PRIORIDAD - Revisar Manualmente

### Archivos de Configuración Duplicados

#### 12. Archivos .env de ejemplo
**Sospecha:** Múltiples ejemplos

- ⚠️ `.env.example`
- ⚠️ `.env.backend.example`
- ⚠️ `backend/.env.example`
- ⚠️ `backend/.env.backend.example`
- ⚠️ `backend/.env.production.example`

**Acción sugerida:** Consolidar en uno solo o documentar diferencias

### Archivos de Metadata

#### 13. Archivos de metadata/tracking
**Sospecha:** Archivos de desarrollo

- ⚠️ `metadata.json` - ¿Qué contiene?
- ⚠️ `archivos_en_git.txt` - Lista de archivos
- ⚠️ `test_chat_request.json` - Request de ejemplo
- ⚠️ `test_request.json` - Request de ejemplo
- ⚠️ `test_e2e_results.json` - Resultados de test

**Acción sugerida:** Verificar si son necesarios o mover a carpeta temporal

### Carpetas Sospechosas

#### 14. Carpetas que podrían estar obsoletas
**Sospecha:** Contenido antiguo o temporal

- ⚠️ `pdf-forge-exports/` - Vacía según listado
- ⚠️ `elemplos_leyes_info/de_mi_hija/` - ¿Archivos personales?
- ⚠️ `docs/Iideas_rama_gemini/` - ¿Rama antigua?
- ⚠️ `.qodo/` - ¿Qué es esto?

**Acción sugerida:** Revisar contenido y decidir

### Archivos de Documentación Genérica

#### 15. Documentos que podrían consolidarse
**Sospecha:** Información duplicada

- ⚠️ `CLAUDE.md` - ¿Instrucciones para Claude?
- ⚠️ `GEMINI.md` - ¿Instrucciones para Gemini?
- ⚠️ `codex.md` - ¿Qué es esto?
- ⚠️ `AGENTS.md` - ¿Duplicado con docs/AI_AGENTS.md?

**Acción sugerida:** Consolidar o mover a docs/

---

## 📊 Resumen Estadístico

### Por Categoría

| Categoría | Archivos Sospechosos | Prioridad |
|-----------|---------------------|-----------|
| Backend Routers Duplicados | 2 | 🔴 Alta |
| Scripts de Indexación | 11 | 🔴 Alta |
| Scripts de Test en Raíz | 7 | 🔴 Alta |
| Scripts de Utilidad en Raíz | 11 | 🔴 Alta |
| Documentos de Sesiones | 6 | 🟡 Media |
| Documentos de Análisis | 8 | 🟡 Media |
| Documentos de Correcciones | 4 | 🟡 Media |
| Documentos de Sprints | 4 | 🟡 Media |
| Documentos de Problemas | 4 | 🟡 Media |
| Documentos de Verificaciones | 4 | 🟡 Media |
| Archivos de Configuración | 5 | 🟢 Baja |
| Archivos de Metadata | 5 | 🟢 Baja |
| Carpetas Sospechosas | 4 | 🟢 Baja |
| Documentación Genérica | 4 | 🟢 Baja |

**Total de archivos sospechosos:** ~79 archivos

---

## 🎯 Recomendaciones de Acción

### Fase 1: Limpieza Inmediata (Alta Prioridad)
1. ✅ Verificar qué router RAG se usa en main.py
2. ✅ Verificar qué rag_agent se usa en routers
3. ✅ Consolidar scripts de indexación o mover a `backend/scripts/one-time/`
4. ✅ Mover tests de raíz a `backend/tests/`
5. ✅ Mover scripts de utilidad a `backend/scripts/` o `tools/`

### Fase 2: Organización (Media Prioridad)
1. 📁 Crear estructura de carpetas:
   - `docs/sesiones/`
   - `docs/analisis/`
   - `docs/correcciones/`
   - `docs/sprints/`
   - `docs/problemas-resueltos/`
   - `docs/verificaciones/`
   - `backend/scripts/one-time/`
   - `backend/scripts/maintenance/`

2. 📦 Mover documentos a carpetas apropiadas

### Fase 3: Revisión Manual (Baja Prioridad)
1. 🔍 Revisar contenido de carpetas sospechosas
2. 🔍 Consolidar archivos de configuración
3. 🔍 Limpiar archivos de metadata temporales

---

## ⚠️ ADVERTENCIAS

1. **NO ELIMINAR SIN VERIFICAR:** Algunos archivos pueden ser necesarios
2. **HACER BACKUP:** Antes de eliminar cualquier cosa
3. **VERIFICAR IMPORTS:** Buscar referencias antes de eliminar código
4. **REVISAR GIT:** Algunos archivos pueden estar en .gitignore pero ser necesarios
5. **CONSULTAR EQUIPO:** Algunos archivos pueden tener contexto que desconocemos

---

## 📝 Próximos Pasos

1. ✅ Revisar esta lista con el equipo
2. ✅ Priorizar qué limpiar primero
3. ✅ Hacer backup antes de cualquier cambio
4. ✅ Verificar imports y dependencias
5. ✅ Ejecutar tests después de cada limpieza
6. ✅ Documentar cambios realizados

---

**Auditoría realizada por:** Kiro AI  
**Método:** Análisis exhaustivo de estructura de archivos, imports y duplicados  
**Estado:** Lista completa - Pendiente de revisión y acción
