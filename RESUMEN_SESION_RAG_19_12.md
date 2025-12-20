# RESUMEN SESIÓN - Configuración RAG Agent

## PROBLEMA PRINCIPAL
El RAG Agent no puede conectarse a Qdrant local debido a incompatibilidad de dimensiones de embeddings.

## ESTADO ACTUAL

### ✅ COMPLETADO:
1. **MCP Gateway** arreglado (línea 49 con path absoluto)
2. **Modelo pablosi** descargado localmente: `~/.cache/huggingface/hub/models--pablosi--bge-m3-spa-law-qa-trained-2`
   - Carga en 2.22s
   - Genera embeddings de 1024 dimensiones
3. **Script generador** con 5 tipos de contenido:
   - TEST (4)
   - COMPARACIÓN (2)
   - PROCEDIMIENTO (2)
   - RAZONAMIENTO (1)
   - RELACIÓN (1)

### ❌ BLOQUEADOR:
**Incompatibilidad de dimensiones de embeddings:**

| Colección | Puntos | Dimensiones | Modelo usado |
|-----------|--------|-------------|--------------|
| `leyes_espana` | 1,067 | 768 | all-MiniLM-L6-v2 (probablemente) |
| `opositaia_knowledge` | 17,403 | ? | Desconocido |

**Modelo actual:** `pablosi/bge-m3-spa-law-qa-trained-2` (1024 dims)

**Error:** Las colecciones locales fueron indexadas con un modelo diferente (768 dims), por lo que pablosi (1024 dims) no puede buscar en ellas.

## SOLUCIONES POSIBLES

### Opción 1: Usar modelo compatible con colecciones existentes
- Cambiar temporalmente a `sentence-transformers/all-MiniLM-L6-v2` (768 dims)
- **Ventaja:** Funciona inmediatamente
- **Desventaja:** No es el modelo especializado en legislación española

### Opción 2: Reindexar con pablosi
- Crear nueva colección con pablosi (1024 dims)
- Reindexar todas las leyes
- **Ventaja:** Usa el modelo especializado
- **Desventaja:** Requiere tiempo de reindexación

### Opción 3: Usar Qdrant Cloud
- Cambiar a Qdrant Cloud (si tiene colección con pablosi)
- **Ventaja:** Puede tener datos ya indexados con pablosi
- **Desventaja:** Requiere conexión a internet, costes

### Opción 4: Generar SIN RAG
- Generar 10 Q&A solo con Groq y ejemplo de calidad
- **Ventaja:** Funciona inmediatamente para test
- **Desventaja:** Sin contexto legal del RAG

## RECOMENDACIÓN
**Para test inmediato:** Opción 4 (generar sin RAG)
**Para producción:** Opción 2 (reindexar con pablosi)

## ARCHIVOS MODIFICADOS
- `backend/.env.backend`: Modelo pablosi, Qdrant local
- `backend/agents/rag_agent_v2.py`: Fallbacks a pablosi
- `backend/routers/mcp_gateway.py`: Path absoluto MCP
- `backend/routers/rag.py`: tema_filter → layer_filter
- `generate_qa_agentic_direct.py`: Script generador completo
