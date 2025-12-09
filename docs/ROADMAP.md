# Hoja de Ruta Evolutiva de OpositaIA (Rama `con_rag`)

**Última actualización:** 5 de diciembre de 2025  
**Sprint actual:** Sprint 2 - RAG Avanzado con BOE API  

Este documento describe el plan de desarrollo por fases para transformar OpositaIA de una aplicación puramente frontend a una plataforma de estudio avanzada con backend, RAG y modelos afinados.

---

### Fase 0: El Puente - Creación del Backend Monolítico Inteligente ✅ COMPLETADO

**Objetivo:** Establecer una base sólida y segura para futuras funcionalidades.

- **Acciones Clave:**
  1. ✅ Desarrollar un backend usando **FastAPI**.
  2. ✅ Crear endpoints (`/generate-case`, `/chat`, etc.) que repliquen la funcionalidad que estaba en `geminiService.ts`.
  3. ✅ Refactorizar el frontend para que use `frontend/services/backendService.ts` apuntando al backend (ya hecho, `geminiService.ts` eliminado).
  4. ✅ Configurar **Qdrant** (vector DB local + cloud) y **SQLite** (datos operacionales).
  5. ✅ Integrar **API oficial BOE** para descarga de legislación consolidada (ver `docs/BOE_API_INTEGRATION.md`).

- **Resultado:** ✅ La aplicación funciona igual pero ahora es segura, escalable y está lista para el RAG. La API Key ya no está en el cliente. Backend FastAPI corriendo en puerto 8000, Qdrant en puerto 6333.

---

### Fase 1: La Memoria Experta - Implementación de RAG Avanzado 🔄 EN PROGRESO

**Objetivo:** Dotar a la aplicación de un conocimiento profundo y preciso del temario oficial.

- **Acciones Completadas:**
  1. ✅ Integrar **API oficial BOE** (cliente Python + FastAPI router con 10 endpoints).
  2. ✅ Descargar legislación consolidada (LGSS, 3.4MB XML, 567 bloques).
  3. ✅ Parsear XML de BOE y extraer artículos/bloques.
  4. ✅ Configurar embeddings con modelos especializados en español legal:
     - `pablosi/bge-m3-spa-law-qa-trained-2` (✅ sin restricciones, recomendado)
     - `littlejohn-ai/bge-m3-spa-law-qa` (⚠️ requiere aceptar términos en HF)
     - `BAAI/bge-m3` (fallback multilingual, menos especializado)
  5. ✅ Indexar primeros 50 bloques LGSS en Qdrant local (colección `opositaia_lgss_test`).

- **Acciones Pendientes:**
  1. 🔄 Indexar todos los 567 bloques de LGSS completa.
  2. 🔄 Indexar 16 leyes adicionales desde BOE API (Constitución, EBEP, Ley 39/2015, etc.).
  3. 🔄 Modificar endpoint `/chat` para recuperar contexto relevante desde Qdrant.
  4. 🔄 Implementar "augmented prompting" con contexto legal recuperado.
  5. 🔄 Validar calidad de búsqueda semántica con queries legales de prueba.

- **Resultado esperado:** Las respuestas del chat y otras herramientas serán drásticamente más precisas y estarán basadas en el temario real, eliminando alucinaciones.

**Opciones de embeddings evaluadas:**
- 🥇 **pablosi/bge-m3-spa-law-qa-trained-2**: Fine-tuned desde littlejohn-ai, 567M parámetros, dataset BOE sintético 5K, Apache 2.0, **SIN RESTRICCIONES** ✅
- 🥈 **littlejohn-ai/bge-m3-spa-law-qa**: Original especializado, 23.7K dataset legal, gated (requiere aceptación) ⚠️
- 🥉 **BAAI/bge-m3**: Base multilingual, 1024 dims, funciona pero menos especializado 📊

---

### Fase 2: El Sello de Experto - Fine-Tuning de Modelos ⏳ PLANIFICADO

**Objetivo:** Crear un modelo de lenguaje especializado en el dominio de la Seguridad Social española que supere a los modelos genéricos.

- **Acciones Clave:**
  1. 📋 Crear un **dataset de alta calidad** con formato `instrucción -> respuesta` (preguntas de test, resúmenes, explicaciones de artículos).
  2. 📋 Utilizar **Unsloth** para hacer fine-tuning de un modelo base como `Mistral-7B-Instruct`.
  3. 📋 Desplegar el modelo afinado en **Ollama local** (0€/mes).
  4. 📋 Integrar las llamadas al modelo afinado en el backend para las tareas más críticas (generación de casos, simulacros).

- **Resultado esperado:** La aplicación ofrecerá una calidad de contenido inalcanzable para la competencia, con un "sello" de experto único.

**Estimación:** Sprint 5-8 (semanas 9-16)

---

### Fase 3: El Futuro - Expansión a Multi-Agente ⏳ FUTURO

**Objetivo:** Escalar la complejidad del sistema si el producto tiene éxito, dividiendo la lógica en agentes especializados.

- **Acciones Clave:**
  1. 📋 Refactorizar el backend monolítico en microservicios o módulos lógicos (Agente RAG, Agente de Tests, etc.).
  2. 📋 Implementar un orquestador que dirija las peticiones del usuario al agente adecuado.

- **Resultado esperado:** Una arquitectura robusta y mantenible a largo plazo, capaz de crecer y añadir nuevas capacidades de forma modular.

**Estimación:** Post-lanzamiento (semana 17+)

---

## 📊 Progreso General del Proyecto

### Sprint 1 (Semanas 1-2): Backend y API BOE ✅ COMPLETADO
- ✅ Backend FastAPI funcional en puerto 8000
- ✅ Cliente API BOE oficial (8 métodos, 48 páginas doc analizadas)
- ✅ 10 endpoints FastAPI para legislación BOE
- ✅ Qdrant local configurado (puerto 6333)
- ✅ Documentación completa (`BOE_API_INTEGRATION.md`, `WSL_POWERSHELL_GUIDE.md`)

### Sprint 2 (Semanas 3-4): Embeddings y Primeras Indexaciones 🔄 EN PROGRESO
- ✅ Descarga LGSS consolidada (3.4MB XML, 567 bloques)
- ✅ Parser XML BOE funcional
- ✅ RAGAgentV2 actualizado con soporte `use_local_embeddings`
- ✅ Modelo embedding seleccionado: `pablosi/bge-m3-spa-law-qa-trained-2`
- ✅ Primeros 50 bloques LGSS indexados en Qdrant
- 🔄 Indexar 517 bloques LGSS restantes (SIGUIENTE)
- 🔄 Validar calidad de búsqueda semántica (SIGUIENTE)

### Sprint 3 (Semanas 5-6): Indexación Completa CAPA 1 📋 PENDIENTE
- 📋 Indexar 16 leyes adicionales (Constitución, EBEP, Ley 39/2015, etc.)
- 📋 Integrar RAG en endpoint `/chat` de FastAPI
- 📋 Tests de calidad de recuperación

### Sprint 4 (Semanas 7-8): UI Qdrant Cloud y Optimización 📋 PENDIENTE
- 📋 Migrar a Qdrant Cloud con UI web (decisión: usar cloud en lugar de dashboard local)
- 📋 Optimizar búsqueda semántica (filtros, re-ranking)
- 📋 Métricas de calidad RAG

---

## 🔧 Infraestructura Actual

### Servicios Activos
- ✅ **FastAPI Backend**: `http://localhost:8000` (WSL Python 3.12.3, PID 70015)
- ✅ **Qdrant Local**: `http://localhost:6333` (Docker `opositaia-qdrant`)
- ✅ **Qdrant Cloud**: `https://b554ceb5-...gcp.cloud.qdrant.io` (configurado, no usado aún)
- ✅ **Frontend React**: `http://localhost:3000` (cuando se ejecuta `npm run dev`)

### Datos Indexados
- **Colección**: `opositaia_lgss_test`
- **Vectores**: 50 bloques LGSS (9% del total)
- **Dimensiones**: 1024 (bge-m3)
- **Distancia**: Cosine
- **Modelo actual**: `BAAI/bge-m3` (temporal, cambiar a `pablosi/bge-m3-spa-law-qa-trained-2`)

### Alternativas de Embeddings Investigadas
1. **Google Colab Free Tier**: Posibilidad de generar embeddings en Colab con GPU gratis (investigar notebook HF)
2. **HF Inference API**: API gratuita de HuggingFace con límites (investigar)
3. **Local CPU**: Actual, funcional pero lento (16GB RAM laptop)

---

## 📚 Referencias Clave

- **API BOE Oficial**: https://www.boe.es/datosabiertos/documentos/APIconsolidada.pdf
- **Modelo Embeddings (recomendado)**: https://huggingface.co/pablosi/bge-m3-spa-law-qa-trained-2
- **Modelo Embeddings (original gated)**: https://huggingface.co/littlejohn-ai/bge-m3-spa-law-qa
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **Documentación Proyecto**: `docs/BOE_API_INTEGRATION.md`, `MEGA_PLAN_ACTUALIZADO_COMPLETO.md`

---

## 🎯 Próximos Pasos Inmediatos

1. **Cambiar modelo embedding** a `pablosi/bge-m3-spa-law-qa-trained-2` ✅ (sin restricciones)
2. **Indexar LGSS completa** (567 bloques) 🔄
3. **Validar búsqueda** con queries legales de prueba
4. **Decidir**: ¿Continuar con Qdrant local o migrar a cloud con UI?
5. **Indexar Constitución** como segunda ley (BOE-A-1978-31229)
