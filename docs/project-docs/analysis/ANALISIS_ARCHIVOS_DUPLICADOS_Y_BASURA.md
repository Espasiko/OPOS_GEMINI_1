# 🗑️ ANÁLISIS DE ARCHIVOS DUPLICADOS Y BASURA

**Fecha**: 22 Noviembre 2025

## 📋 ARCHIVOS RAÍZ - CANDIDATOS PARA BASURA

### ✅ Sprints Antiguos Completados (Ya en basura según contexto)
```
SPRINT2_COMPLETADO.md
SPRINT2_RESUMEN.md
SPRINT3_COMPLETADO.md
SPRINT5_CAPA3_EN_PROGRESO.md
SPRINT7_ESTADO_ACTUAL.md
SPRINT7_FASE1_BACKEND_COMPLETADO.md
SPRINT7_FASE2_FRONTEND_COMPLETADO.md
SPRINT7_INTEGRACION_FRONTEND_BACKEND.md
SPRINT9_FASE1_Y_FASE2_COMPLETADAS.md
SPRINT9_FASE3_COMPLETADA.md
```

### ⚠️ Análisis Temporales (Pueden moverse)
```
ANALISIS_5_CAPAS_RAG.md
ANALISIS_COMPLETO_COSTOS_IA.md
ANALISIS_OPCIONES_IA.md
CONTEXTO_COMPLETO_PROYECTO.md
EXPLICACION_CAMBIOS_INMEDIATOS.md
PLAN_CAPAS_2_Y_3.md
PLAN_DESARROLLO_20_NOV_2025.md
```

### ✅ Verificaciones Completadas (Pueden moverse)
```
VERIFICACION_CONSTITUCION_Y_TEST_CAPA1.md
VERIFICACION_FINAL_SISTEMA_COMPLETO.md
VERIFICACION_REPO.md
INDEXACION_3_LEYES_CRITICAS_COMPLETADA.md
LEYES_NECESARIAS_VS_INDEXADAS.md
RESUMEN_REINDEXACION_CONSTITUCION.md
SISTEMA_RAG_100_COMPLETO.md
```

### ✅ Resúmenes de Sesión (Pueden moverse)
```
RESUMEN_DIA_2025-11-18.md
RESUMEN_SESION_20_NOV.md
MIGRACION_CHATVIEW_COMPLETADA.md
INFRAESTRUCTURA_REAL_VERIFICADA.md
REPORTE_ESLINT_TYPES_TS.md
```

## 🔧 BACKEND - SCRIPTS DE TEST TEMPORALES

### ✅ Scripts de Verificación Antiguos (Pueden moverse)
```
backend/check_articulo_168.py
backend/delete_and_reindex_constitucion.py
backend/verify_3_leyes_criticas.py
backend/verify_and_setup.py
backend/verify_articulo_168_final.py
backend/verify_before_sprint3.py
backend/verify_constitucion_pdf.py
backend/verify_constitucion.py
backend/verify_pdf_constitucion.py
backend/verify_rd_cotizacion.py
backend/verificacion_completa_sistema.py
```

### ✅ Scripts de Indexación Antiguos (Pueden moverse)
```
backend/download_sprint3.py
backend/download_sprint4.py
backend/index_capa3_restantes.py
backend/index_capa3_tests.py
backend/index_constitucion.py
backend/index_lgss_complete.py
backend/index_sprint3.py
backend/index_sprint4.py
```

### ✅ Tests Temporales (Pueden moverse)
```
backend/test_articulo168.json
backend/test_capa1_query.json
backend/test_chat_completo.py
backend/test_chat_frontend.py
backend/test_constitucion.py
backend/test_import.py
backend/test_incapacidad_temporal.json
backend/test_mistral_rag.py
backend/test_rag_completo.py
backend/test_reranking.py
backend/test_robertalex_local.py
backend/test_setup.py
backend/test_sprint7_endpoints.sh
backend/test_titulo_decimo.json
```

### ⚠️ Documentación Antigua (Pueden moverse)
```
backend/INSTRUCCIONES_TEST_ROBERTALEX.md
backend/SPRINT2_INSTRUCCIONES.md
```

## 🔥 ARCHIVOS A MANTENER (IMPORTANTES)

### Documentación Principal
```
README.md
SETUP.md
AGENTS.md
AI_SPECS_QUICKSTART.md
COMO_OBTENER_API_KEYS.md
```

### Estado Actual
```
SPRINT8_COMPLETADO.md
SPRINT9_COMPLETADO.md
SPRINT10_COMPLETADO.md
ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md
RESUMEN_EJECUTIVO_PLAN.md
PROXIMOS_PASOS.md
```

### Referencia
```
CLAUDE.md
GEMINI.md
EXPLICACION_HUGGINGFACE_SPACES.md
codex.md
```

### Backend Activo
```
backend/main.py
backend/requirements.txt
backend/README.md
backend/Dockerfile
backend/test_ai_functions.py
backend/test_all_providers.py
backend/calcular_tamano_rag.py
backend/monitor_live.py
backend/monitor_qdrant.py
backend/stats_por_norma.py
backend/setup_qdrant_collection.py
backend/migrate_qdrant_to_cloud.py
```

## 📊 RESUMEN

**Total archivos para mover a basura**:
- Raíz: ~25 archivos
- Backend: ~35 archivos
- **Total**: ~60 archivos

**Beneficios**:
- ✅ Proyecto más limpio y organizado
- ✅ Más fácil encontrar archivos importantes
- ✅ Historial preservado por si acaso
- ✅ Reduce confusión en el equipo

## 🎯 ACCIÓN RECOMENDADA

1. Crear carpeta `basura/` en raíz
2. Crear carpeta `basura/backend/` para scripts backend
3. Mover archivos temporales preservando estructura
4. Commit y push a GitHub
