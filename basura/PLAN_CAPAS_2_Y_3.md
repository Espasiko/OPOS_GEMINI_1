# 📋 PLAN: Capas 2 y 3 del Sistema RAG

**Fecha**: 2025-11-18  
**Estado Actual**: Capa 1 completada (2,016 chunks)  
**Pendiente**: Capas 2 y 3

---

## 🎯 ARQUITECTURA DE 3 CAPAS

### ✅ Capa 1: Normativa Oficial (COMPLETADA)
**Estado**: ✅ 100% Indexada  
**Contenido**: 9 normas del BOE  
**Chunks**: 2,016  
**Artículos**: 526  

**Normas indexadas**:
1. Constitución Española (62 chunks)
2. LGSS (521 chunks)
3. Ley 39/2015 (270 chunks)
4. Ley 40/2015 (476 chunks)
5. EBEP (214 chunks)
6. RD Recaudación (141 chunks)
7. RD Afiliación (91 chunks)
8. Ley IMV (115 chunks)
9. LOPDGDD (126 chunks)

---

## 📚 Capa 2: Jurisprudencia y Doctrina (PENDIENTE)

### Objetivo:
Indexar sentencias y doctrina administrativa relevante para oposiciones de Seguridad Social.

### Contenido Propuesto:

#### A. Jurisprudencia (Prioridad ALTA)
**Fuente**: Sentencias del Tribunal Supremo (STS)

**Top 50 Sentencias Relevantes**:
- Incapacidad permanente (10-15 sentencias)
- Jubilación anticipada (5-10 sentencias)
- Prestaciones por desempleo (5-10 sentencias)
- Cotización y bases (5-10 sentencias)
- Régimen especial autónomos (5-10 sentencias)

**Metadata adicional**:
- `tipo`: "sentencia_sts", "sentencia_tsj"
- `tribunal`: "Tribunal Supremo", "TSJ Madrid"
- `fecha_sentencia`: Fecha
- `superada_por`: ID de sentencia que la supera (si aplica)
- `doctrina_unificadora`: true/false

**Estimación**:
- 50 sentencias × ~20 páginas = 1,000 páginas
- ~2,000 chunks estimados
- Tiempo: 2-3 horas de indexación

#### B. Doctrina Administrativa (Prioridad MEDIA)
**Fuente**: Resoluciones TGSS, Criterios INSS

**Contenido**:
- Criterios de interpretación INSS
- Resoluciones TGSS relevantes
- Circulares y consultas vinculantes

**Estimación**:
- ~500 chunks estimados
- Tiempo: 1 hora de indexación

### Desafío Principal:
⚠️ **Obtención de sentencias**: No hay API pública del CENDOJ. Opciones:
1. Scraping manual de CENDOJ
2. Usar bases de datos comerciales (vLex, Aranzadi)
3. Recopilar manualmente las Top 50
4. **ALTERNATIVA**: Usar materiales de jurisprudencia de tu hija (si existen)

---

## 📖 Capa 3: Materiales de Estudio (PENDIENTE)

### Objetivo:
Indexar materiales de academia para entrenamiento y práctica.

### Contenido Disponible:

#### A. Tests (Prioridad ALTA)
**Archivos disponibles**:
- `Test_Admtvos_AGE_1contestando.pdf` (273 páginas)
- `Test_Admtvos_AGE_2contestando.pdf` (321 páginas)
- `Medalleros y supuestos ss con casilleros.pdf` (1,410 páginas)
- Otros 11 archivos de tests

**Total estimado**: ~2,500 páginas de tests

**Metadata adicional**:
- `tipo`: "test", "pregunta_respuesta"
- `fuente`: "Academia Las Cortes", etc.
- `tema`: Número de tema
- `formato`: "multiple_choice", "verdadero_falso"
- `respuesta_correcta`: Letra correcta (si disponible)
- `explicacion`: Explicación de la respuesta (si disponible)

**Estimación**:
- ~5,000 chunks estimados
- Tiempo: 3-4 horas de indexación

#### B. Casos Prácticos (Prioridad ALTA)
**Archivos disponibles**:
- `Muestra-Supuestos-Practicos-C1-Administrativo-Seguridad-Social-2024.pdf` (28 páginas)
- Otros 11 archivos de casos prácticos

**Total estimado**: ~200 páginas de casos

**Metadata adicional**:
- `tipo`: "caso_practico"
- `tema`: Tema relacionado
- `dificultad`: "facil", "medio", "dificil"
- `tiene_solucion`: true/false

**Estimación**:
- ~400 chunks estimados
- Tiempo: 30 minutos de indexación

#### C. Temarios (Prioridad MEDIA)
**Archivos disponibles**:
- `SS Temario Unificado - Parte específica (1).pdf` (989 páginas)
- Otros 5 archivos de temarios

**Total estimado**: ~2,500 páginas de temarios

**Metadata adicional**:
- `tipo`: "temario"
- `fuente`: "Academia"
- `tema`: Número de tema
- `seccion`: Sección del temario

**Estimación**:
- ~5,000 chunks estimados
- Tiempo: 3-4 horas de indexación

#### D. Esquemas (Prioridad BAJA)
**Archivos disponibles**: 27 archivos de esquemas

**Estimación**:
- ~500 chunks estimados
- Tiempo: 30 minutos de indexación

---

## 📊 ESTIMACIÓN TOTAL CAPAS 2 Y 3

### Capa 2: Jurisprudencia
- **Chunks estimados**: 2,500
- **Tiempo indexación**: 3-4 horas
- **Desafío**: Obtención de sentencias

### Capa 3: Materiales de Estudio
- **Chunks estimados**: 11,000
- **Tiempo indexación**: 8-10 horas
- **Desafío**: Procesamiento de formatos variados

### TOTAL:
- **Chunks totales**: ~13,500 nuevos
- **Total sistema**: ~15,500 chunks
- **Tiempo total**: 11-14 horas
- **Tamaño estimado**: ~45 MB en Qdrant

---

## 🚀 PLAN DE IMPLEMENTACIÓN

### Sprint 5: Capa 3 - Tests y Casos (Prioridad ALTA)
**Duración**: 1 día  
**Objetivo**: Indexar tests y casos prácticos

**Tareas**:
1. Crear procesador de tests (detectar preguntas/respuestas)
2. Crear procesador de casos prácticos
3. Indexar tests principales (2,500 páginas)
4. Indexar casos prácticos (200 páginas)
5. Testing de calidad

**Resultado esperado**: ~5,400 chunks nuevos

### Sprint 6: Capa 3 - Temarios (Prioridad MEDIA)
**Duración**: 1 día  
**Objetivo**: Indexar temarios de academia

**Tareas**:
1. Procesar temario unificado (989 páginas)
2. Procesar otros temarios
3. Indexar con metadata de tema/sección
4. Testing de calidad

**Resultado esperado**: ~5,000 chunks nuevos

### Sprint 7: Capa 2 - Jurisprudencia (Prioridad ALTA)
**Duración**: 2-3 días  
**Objetivo**: Indexar Top 50 sentencias STS

**Tareas**:
1. Recopilar Top 50 sentencias (manual o scraping)
2. Procesar sentencias
3. Indexar con metadata de jurisprudencia
4. Implementar detección de sentencias superadas
5. Testing de calidad

**Resultado esperado**: ~2,000 chunks nuevos

### Sprint 8: Optimización y Reranking
**Duración**: 1 día  
**Objetivo**: Implementar reranking por jerarquía

**Tareas**:
1. Implementar reranking por `nivel_jerarquia`
2. Implementar filtros por `layer`
3. Testing de calidad con 3 capas
4. Ajustar pesos de cada capa

---

## 🎯 DECISIÓN INMEDIATA

### Opción A: Continuar con Capa 3 (Tests y Casos)
**Ventajas**:
- ✅ Materiales ya disponibles
- ✅ No requiere obtención externa
- ✅ Alto valor para estudiantes
- ✅ Rápido de implementar

**Desventajas**:
- ⚠️ Requiere procesador especializado para tests

### Opción B: Empezar con Capa 2 (Jurisprudencia)
**Ventajas**:
- ✅ Completa la jerarquía normativa
- ✅ Alto valor legal
- ✅ Diferenciación del producto

**Desventajas**:
- ❌ Requiere obtención de sentencias
- ❌ Más complejo de implementar
- ❌ Tiempo de obtención incierto

### Opción C: Integrar Backend primero
**Ventajas**:
- ✅ Sistema funcional end-to-end
- ✅ Permite testing real
- ✅ Valor inmediato

**Desventajas**:
- ⚠️ Capa 1 sola puede ser insuficiente

---

## 💡 RECOMENDACIÓN

**Orden sugerido**:
1. **Sprint 5**: Capa 3 - Tests y Casos (1 día)
2. **Integración Backend**: Endpoints FastAPI (1 día)
3. **Sprint 6**: Capa 3 - Temarios (1 día)
4. **Sprint 7**: Capa 2 - Jurisprudencia (2-3 días)
5. **Sprint 8**: Optimización y Reranking (1 día)

**Justificación**:
- Maximiza valor inmediato (tests para estudiantes)
- Permite integración temprana con backend
- Deja tiempo para obtener sentencias
- Progreso incremental y testeable

---

## 📞 ¿Qué hacemos ahora?

**Opciones**:
1. 🚀 **Empezar Sprint 5** (Indexar tests y casos)
2. 🔧 **Integrar con Backend** (Crear endpoints FastAPI)
3. 📊 **Analizar materiales** (Ver qué tests/casos tenemos exactamente)
4. 🔍 **Buscar sentencias** (Empezar con Capa 2)

**¿Cuál prefieres?**
