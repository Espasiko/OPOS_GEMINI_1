# 📊 Análisis de Nuevos Tipos de Contenido Premium

**Fecha:** 8 de diciembre de 2025

## 🎯 Objetivo

Ampliar el dataset con tipos de contenido premium adicionales basados en materiales oficiales de oposiciones.

## 📚 Materiales Analizados

### 1. Esquemas Oficiales
**Ubicación:** `elemplos_leyes_info/de_mi_hija/ESQUEMAS-20250327T124016Z-001/ESQUEMAS/buenos/`

**Tipos encontrados:**
- Esquemas visuales de la Constitución Española (CE)
- Esquemas del Estatuto de los Trabajadores (ET)
- Esquemas de Ley de Contratos del Sector Público (LCSP)
- Esquemas de procedimientos administrativos
- Esquemas de estructura de la AGE
- Esquemas de plazos y procedimientos

**Características:**
- Formato visual jerárquico
- Información condensada
- Referencias a artículos específicos
- Comparativas (ej: "Diferencia decreto-ley y decreto-legislativo")
- Plazos importantes destacados

### 2. Simulacros Oficiales
**Ubicación:** `elemplos_leyes_info/de_mi_hija/Simulacros-20250327T124008Z-001/Simulacros/` y E:\1\OPOS_GEMINI_1\elemplos_leyes_info\de_mi_hija\bajados_academia

**Tipos encontrados:**
- Exámenes tipo test oficiales
- Plantillas de respuestas
- Ejercicios únicos de convocatorias reales
- Modelos de años anteriores (2017, 2019, 2020)

**Características:**
- 100 preguntas tipo test
- 4 opciones por pregunta
- Plantilla de respuestas oficial
- Tiempo limitado (90-100 minutos)
- Penalización por errores

### 3. Constitución Española (Artículos 1-39)
**Ubicación:** `elemplos_leyes_info/de_mi_hija/ce 1-39.pdf`

**Contenido:**
- Artículos fundamentales de la CE
- Derechos y libertades fundamentales
- Base para muchas preguntas de oposición

## 🆕 Nuevos Tipos de Contenido a Generar

### 1. Razonamiento Legal con Verificación BOE ⭐⭐⭐

**Descripción:** Casos que requieren razonamiento paso a paso con verificación en fuentes oficiales.

**Estructura:**
```json
{
  "type": "razonamiento_legal_verificado",
  "caso": "Descripción del caso o situación",
  "pregunta": "¿Qué solución legal aplica?",
  "razonamiento_paso_a_paso": [
    {
      "paso": 1,
      "descripcion": "Identificar la normativa aplicable",
      "normativa": "art. X de Ley Y",
      "boe_reference": "BOE-A-XXXX-XXXXX",
      "verificado": true
    },
    {
      "paso": 2,
      "descripcion": "Analizar los requisitos",
      "requisitos": ["req1", "req2"],
      "cumplimiento": "análisis"
    },
    {
      "paso": 3,
      "descripcion": "Aplicar la norma al caso",
      "aplicacion": "explicación"
    },
    {
      "paso": 4,
      "descripcion": "Conclusión fundamentada",
      "conclusion": "respuesta final"
    }
  ],
  "verificacion_boe": {
    "articulos_consultados": ["art. X", "art. Y"],
    "fuentes": ["BOE-A-XXXX-XXXXX"],
    "fecha_verificacion": "2025-12-08",
    "correcto": true
  },
  "theme": "tema",
  "difficulty": "alta",
  "verified": true
}
```

**Ejemplo:**
```json
{
  "type": "razonamiento_legal_verificado",
  "caso": "María trabaja 42 horas semanales. Su empresa quiere aumentar a 45 horas sin modificar contrato.",
  "pregunta": "¿Es legal? ¿Qué puede hacer María?",
  "razonamiento_paso_a_paso": [
    {
      "paso": 1,
      "descripcion": "Identificar jornada máxima legal",
      "normativa": "art. 34.1 ET - Jornada máxima 40h semanales promedio anual",
      "boe_reference": "BOE-A-2015-11430",
      "verificado": true
    },
    {
      "paso": 2,
      "descripcion": "Analizar situación actual",
      "requisitos": ["Jornada actual: 42h", "Propuesta: 45h", "Ambas superan 40h"],
      "cumplimiento": "Ya está en situación irregular, empeora con propuesta"
    },
    {
      "paso": 3,
      "descripcion": "Determinar legalidad",
      "aplicacion": "Superar 40h solo es legal con: 1) Convenio colectivo que lo permita, 2) Compensación con descanso, 3) Horas extraordinarias pagadas"
    },
    {
      "paso": 4,
      "descripcion": "Opciones de María",
      "conclusion": "María puede: 1) Negarse (derecho a jornada legal), 2) Denunciar a Inspección de Trabajo, 3) Exigir compensación por horas extra"
    }
  ],
  "verificacion_boe": {
    "articulos_consultados": ["art. 34.1 ET", "art. 35 ET"],
    "fuentes": ["BOE-A-2015-11430"],
    "fecha_verificacion": "2025-12-08",
    "correcto": true
  }
}
```

### 2. Esquemas Estructurados ⭐⭐

**Descripción:** Representación jerárquica de conceptos legales complejos.

**Estructura:**
```json
{
  "type": "esquema_estructurado",
  "titulo": "Título del esquema",
  "tema": "tema principal",
  "estructura": {
    "nivel_1": {
      "titulo": "Concepto principal",
      "contenido": "Explicación",
      "articulo": "art. X",
      "subniveles": {
        "nivel_2_1": {
          "titulo": "Subconcepto 1",
          "contenido": "Detalle",
          "ejemplos": ["ej1", "ej2"]
        },
        "nivel_2_2": {
          "titulo": "Subconcepto 2",
          "contenido": "Detalle"
        }
      }
    }
  },
  "referencias": ["art. X", "art. Y"],
  "boe_source": "BOE-A-XXXX-XXXXX",
  "verified": true
}
```

### 3. Simulacro de Examen Oficial ⭐⭐⭐

**Descripción:** Bloques de preguntas tipo examen real de oposición.

**Estructura:**
```json
{
  "type": "simulacro_examen",
  "titulo": "Simulacro AGE - Bloque X",
  "num_preguntas": 25,
  "tiempo_estimado": "22 minutos",
  "penalizacion": "0.33 por error",
  "preguntas": [
    {
      "numero": 1,
      "pregunta": "texto",
      "opciones": ["A", "B", "C", "D"],
      "respuesta_correcta": "B",
      "explicacion": "fundamentación",
      "articulo": "art. X",
      "tema": "tema",
      "dificultad": "media"
    }
  ],
  "temas_cubiertos": ["tema1", "tema2"],
  "nivel": "oficial",
  "año_referencia": "2024",
  "verified": true
}
```

### 4. Comparativas Legales ⭐

**Descripción:** Comparación entre conceptos similares que se confunden.

**Estructura:**
```json
{
  "type": "comparativa_legal",
  "titulo": "Diferencia entre X e Y",
  "concepto_a": {
    "nombre": "Concepto A",
    "definicion": "def",
    "articulo": "art. X",
    "caracteristicas": ["c1", "c2"],
    "ejemplos": ["ej1"]
  },
  "concepto_b": {
    "nombre": "Concepto B",
    "definicion": "def",
    "articulo": "art. Y",
    "caracteristicas": ["c1", "c2"],
    "ejemplos": ["ej1"]
  },
  "diferencias_clave": [
    "diferencia 1",
    "diferencia 2"
  ],
  "tabla_comparativa": {
    "criterio_1": {"A": "valor", "B": "valor"},
    "criterio_2": {"A": "valor", "B": "valor"}
  },
  "boe_sources": ["BOE-A-X", "BOE-A-Y"],
  "verified": true
}
```

### 5. Plazos y Procedimientos ⭐⭐

**Descripción:** Esquemas de plazos legales importantes.

**Estructura:**
```json
{
  "type": "plazos_procedimiento",
  "procedimiento": "Nombre del procedimiento",
  "normativa": "Ley X",
  "fases": [
    {
      "fase": 1,
      "nombre": "Inicio",
      "plazo": "X días",
      "computo": "hábiles/naturales",
      "articulo": "art. X",
      "acciones": ["acción 1", "acción 2"],
      "consecuencias_incumplimiento": "qué pasa si no se cumple"
    }
  ],
  "diagrama_flujo": "descripción textual del flujo",
  "plazos_criticos": ["plazo 1: X días", "plazo 2: Y días"],
  "boe_source": "BOE-A-XXXX",
  "verified": true
}
```

## 🎯 Prioridades de Generación

### Alta Prioridad (Generar YA)
1. **Razonamiento Legal Verificado** - 100 registros
   - 20 por cada tema de baja cobertura
   - Verificación BOE obligatoria
   - Razonamiento paso a paso

2. **Simulacros de Examen** - 50 registros
   - 5 bloques de 10 preguntas cada uno
   - Estilo oficial de oposiciones
   - Temas variados

### Media Prioridad
3. **Esquemas Estructurados** - 50 registros
   - Basados en esquemas oficiales
   - Temas complejos simplificados

4. **Comparativas Legales** - 30 registros
   - Conceptos que se confunden
   - Tablas comparativas

### Baja Prioridad
5. **Plazos y Procedimientos** - 20 registros
   - Procedimientos administrativos
   - Plazos críticos

## 📊 Total Nuevos Registros

- **Razonamiento Legal Verificado:** 100
- **Simulacros de Examen:** 50
- **Esquemas Estructurados:** 50
- **Comparativas Legales:** 30
- **Plazos y Procedimientos:** 20

**TOTAL:** 250 registros premium adicionales

## 🚀 Próximos Pasos

1. Crear script `generar_razonamiento_legal_verificado.py`
2. Crear script `generar_simulacros_examen.py`
3. Crear script `generar_esquemas_estructurados.py`
4. Crear script `generar_comparativas_legales.py`
5. Crear script `generar_plazos_procedimientos.py`
6. Unificar con dataset existente

---

**Estado:** 📝 PLANIFICADO
**Próxima acción:** Generar razonamiento legal verificado
