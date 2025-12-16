# 📋 Plan de Ampliación Dataset Premium

**Fecha:** 8 de diciembre de 2025  
**Estado:** 🚧 EN PROGRESO

## 🎯 Objetivo

Ampliar el dataset actual (801 registros) con **250 registros premium adicionales** de tipos especializados basados en materiales oficiales de oposiciones.

## 📊 Estado Actual

### Dataset Existente
- **Total:** 801 registros
- **Archivo:** `dataset_output/qa_completo_unificado_CORREGIDO_20251208.jsonl`
- **Tipos:** 10 tipos diferentes
- **Temas:** 17 temas cubiertos

### Materiales Disponibles
1. ✅ **Esquemas oficiales** - `elemplos_leyes_info/de_mi_hija/ESQUEMAS-20250327T124016Z-001/ESQUEMAS/buenos/`
2. ✅ **Simulacros oficiales** - `elemplos_leyes_info/de_mi_hija/Simulacros-20250327T124008Z-001/Simulacros/`
3. ✅ **Constitución Española** - `elemplos_leyes_info/de_mi_hija/ce 1-39.pdf`

## 🆕 Nuevos Tipos a Generar

### 1. Razonamiento Legal Verificado ⭐⭐⭐ (PRIORIDAD ALTA)

**Objetivo:** 100 registros  
**Estado:** 🚧 25/100 generados  
**Script:** `generar_razonamiento_legal_verificado.py`

**Características:**
- Razonamiento paso a paso (4 pasos mínimo)
- Verificación BOE obligatoria
- Referencias a artículos específicos
- Casos realistas con solución fundamentada
- Nivel de dificultad: media-alta

**Distribución:**
- Campo de Aplicación: 20
- Jornada y Descansos: 20
- Modificación Sustancial: 20
- Suspensión y Excedencias: 20
- Presupuestos Generales: 20

**Pendiente:**
- [ ] Ampliar de 25 a 100 registros
- [ ] Añadir más variaciones por tema
- [ ] Incluir casos más complejos

### 2. Simulacros de Examen Oficial ⭐⭐⭐ (PRIORIDAD ALTA)

**Objetivo:** 50 registros (5 bloques de 10 preguntas)  
**Estado:** ⏳ PENDIENTE  
**Script:** `generar_simulacros_examen.py` (por crear)

**Características:**
- Formato oficial de oposiciones AGE y SSSS
- 10 preguntas por bloque
- 4 opciones por pregunta
- Tiempo estimado por bloque
- Penalización por errores (0.33)
- Explicación de respuesta correcta
- Referencias BOE

**Bloques a generar:**
1. Bloque Constitución Española (10 preguntas)
2. Bloque Seguridad Social (10 preguntas)
3. Bloque Estatuto Trabajadores (10 preguntas)
4. Bloque Procedimiento Administrativo (10 preguntas)
5. Bloque Mixto (10 preguntas)

### 3. Esquemas Estructurados ⭐⭐ (PRIORIDAD MEDIA)

**Objetivo:** 50 registros  
**Estado:** ⏳ PENDIENTE  
**Script:** `generar_esquemas_estructurados.py` (por crear)

**Características:**
- Representación jerárquica de conceptos
- Basados en esquemas oficiales
- Estructura multinivel
- Referencias a artículos
- Ejemplos prácticos

**Temas prioritarios:**
- Organización judicial española
- Estructura AGE
- Procedimientos administrativos
- Plazos importantes CE
- Tipos de contratos sector público
- Retribuciones funcionarios
- Jornada de trabajo ET
- Indemnizaciones por extinción

### 4. Comparativas Legales ⭐ (PRIORIDAD MEDIA)

**Objetivo:** 30 registros  
**Estado:** ⏳ PENDIENTE  
**Script:** `generar_comparativas_legales.py` (por crear)

**Características:**
- Comparación entre conceptos similares
- Tabla comparativa
- Diferencias clave
- Ejemplos de cada concepto
- Referencias BOE

**Comparativas a generar:**
- Decreto-ley vs Decreto legislativo
- Moción de censura España vs UE
- Recurso inconstitucionalidad vs amparo
- Excedencia voluntaria vs forzosa
- Suspensión vs extinción contrato
- Régimen General vs Regímenes Especiales
- Funcionario carrera vs interino
- Contrato indefinido vs temporal

### 5. Plazos y Procedimientos ⭐ (PRIORIDAD BAJA)

**Objetivo:** 20 registros  
**Estado:** ⏳ PENDIENTE  
**Script:** `generar_plazos_procedimientos.py` (por crear)

**Características:**
- Esquema de fases del procedimiento
- Plazos específicos (días hábiles/naturales)
- Consecuencias de incumplimiento
- Diagrama de flujo textual
- Referencias normativas

**Procedimientos a cubrir:**
- Procedimiento administrativo común (Ley 39/2015)
- Recurso de alzada
- Recurso potestativo de reposición
- Procedimiento de contratación pública
- Modificación sustancial condiciones trabajo
- Despido disciplinario
- Reclamación previa a la vía judicial

## 📈 Cronograma

### Fase 1: Razonamiento Legal (HOY)
- [x] Crear script base
- [x] Generar 25 registros iniciales
- [ ] Ampliar a 100 registros
- [ ] Verificar calidad

### Fase 2: Simulacros (MAÑANA)
- [ ] Analizar simulacros oficiales
- [ ] Crear script generador
- [ ] Generar 50 registros (5 bloques)
- [ ] Verificar formato oficial

### Fase 3: Esquemas (PRÓXIMOS DÍAS)
- [ ] Analizar esquemas oficiales
- [ ] Crear plantillas estructuradas
- [ ] Generar 50 registros
- [ ] Validar jerarquías

### Fase 4: Comparativas y Plazos
- [ ] Generar 30 comparativas
- [ ] Generar 20 plazos
- [ ] Unificar todo

### Fase 5: Integración Final
- [ ] Unificar 250 nuevos con 801 existentes
- [ ] Verificar duplicados
- [ ] Validar JSON
- [ ] Generar estadísticas finales

## 🎯 Resultado Esperado

### Dataset Final
- **Total registros:** 1,051 (801 + 250)
- **Tipos de contenido:** 15 tipos
- **Temas cubiertos:** 17+ temas
- **Calidad:** Premium verificado

### Distribución Final Esperada
| Tipo | Actual | Nuevos | Total |
|------|--------|--------|-------|
| QA Test | 173 | 0 | 173 |
| Flashcard | 129 | 0 | 129 |
| Razonamiento Legal Verificado | 0 | 100 | 100 |
| Caso Práctico | 72 | 0 | 72 |
| QA Simple | 67 | 0 | 67 |
| Diálogo | 66 | 0 | 66 |
| RAG Contexto | 60 | 0 | 60 |
| Supuesto Práctico | 59 | 0 | 59 |
| Diálogo Conversacional | 59 | 0 | 59 |
| Flashcard Resumen | 58 | 0 | 58 |
| Pregunta Contexto Respuesta | 58 | 0 | 58 |
| **Simulacro Examen** | **0** | **50** | **50** |
| **Esquema Estructurado** | **0** | **50** | **50** |
| **Comparativa Legal** | **0** | **30** | **30** |
| **Plazos Procedimiento** | **0** | **20** | **20** |
| **TOTAL** | **801** | **250** | **1,051** |

## 🚀 Próximos Pasos Inmediatos

1. **Completar razonamiento legal** (75 registros más)
2. **Crear generador de simulacros** (50 registros)
3. **Crear generador de esquemas** (50 registros)
4. **Unificar todo el dataset**
5. **Verificación final**

## 📝 Notas Importantes

### Sobre Razonamiento Legal
- Cada caso debe tener 4 pasos mínimo
- Verificación BOE obligatoria
- Incluir artículos específicos
- Casos realistas y variados
- Nivel medio-alto de complejidad

### Sobre Simulacros
- Seguir formato oficial exacto
- Incluir penalización por errores
- Tiempo estimado realista
- Mezclar dificultades
- Cubrir todos los temas importantes

### Sobre Esquemas
- Basarse en esquemas oficiales existentes
- Estructura jerárquica clara
- Máximo 3-4 niveles de profundidad
- Incluir ejemplos prácticos
- Referencias normativas completas

---

**Estado:** 🚧 EN PROGRESO  
**Última actualización:** 8 de diciembre de 2025  
**Progreso:** 25/250 (10%)
