# 🚀 Guía Completa: Configurar Agente Mistral con Qdrant Local

## 📋 Índice
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Recursos Disponibles](#recursos-disponibles)
4. [Configuración del Agente en Mistral Studio](#configuración-del-agente)
5. [Funciones (Tools) del Agente](#funciones-tools)
6. [Ejemplos de Uso](#ejemplos-de-uso)
7. [Troubleshooting](#troubleshooting)

---

## 📊 Resumen Ejecutivo

### ¿Qué es este agente?
Un agente especializado en oposiciones de Seguridad Social que utiliza:
- **Mistral Large 2** como modelo base
- **Qdrant Cloud** como base de datos vectorial
- **BGE-M3** como modelo de embeddings
- **RAG (Retrieval Augmented Generation)** para respuestas precisas basadas en legislación

### Capacidades principales
✅ Búsqueda semántica en legislación española (Constitución, LGSS, LISOS, etc.)
✅ Generación de preguntas de examen tipo test
✅ Explicaciones detalladas con referencias legales
✅ Verificación de URLs del BOE
✅ Respuestas contextualizadas para oposiciones

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                  MISTRAL STUDIO AGENT                    │
│                  (Mistral Large 2)                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Function Calling
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐         ┌──────────────┐
│  buscar_rag   │         │ verificar_url│
│   (Qdrant)    │         │    (BOE)     │
└───────┬───────┘         └──────────────┘
        │
        │ Vector Search
        │
        ▼
┌─────────────────────────────────────────┐
│         QDRANT CLOUD                     │
│  Collection: leyes_seguridad_social      │
│  - 15,234 chunks de legislación          │
│  - Embeddings BGE-M3 (1024 dims)         │
│  - Metadata: ley, artículo, título, etc. │
└─────────────────────────────────────────┘
```

---

## 📚 Recursos Disponibles

### Base de Datos Qdrant Cloud

**Colección:** `leyes_seguridad_social`
**Contenido indexado:**
- ✅ Constitución Española (52 artículos)
- ✅ Ley General de la Seguridad Social (LGSS) - 368 artículos
- ✅ Ley de Infracciones y Sanciones (LISOS) - 40 artículos
- ✅ Ley de Prevención de Riesgos Laborales (LPRL) - 54 artículos
- ✅ Estatuto de los Trabajadores (ET) - 92 artículos
- ✅ Ley de Procedimiento Administrativo (Ley 39/2015) - 180 artículos
- ✅ Ley del Régimen Jurídico (Ley 40/2015) - 86 artículos
- ✅ Reglamentos y Reales Decretos relacionados

**Total:** ~15,234 chunks vectorizados

### Materiales de Academia (Disponibles para indexar)

**Ubicación:** `elemplos_leyes_info/de_mi_hija/`

**Contenido:**
- 📁 **2024 opos ss y advo** (158 archivos, 337.69 MB)
  - Exámenes oficiales 2024
  - Simulacros de examen
  - Temarios actualizados
  - Plantillas de respuesta
  
- 📁 **AÑOS ANTERIORES** 
  - Exámenes históricos
  - Recopilaciones de preguntas
  - Correcciones y explicaciones

- 📁 **Simulacros**
  - Tests completos
  - Ejercicios prácticos
  - Casos supuestos

**Archivos destacados:**
- `Medalleros ...` (25.89 MB) - Recopilación completa
- `TEMAS ESPEC...` (22.84 MB) - Temario específico
- `8023-Recopi...` (múltiples versiones) - Recopilaciones oficiales
- Exámenes AEAT, AGE, y otros organismos

---

## ⚙️ Configuración del Agente en Mistral Studio

### 1. Información Básica

**Nombre del Agente:** `Experto Oposiciones Seguridad Social`

**Modelo:** `Mistral Medium` (mistral-medium-latest)

**Temperatura:** `0.2` (para respuestas precisas y consistentes)

### 2. System Prompt (Instrucciones del Agente)

```markdown
FORMATO OBLIGATORIO - RESPONDE EXACTAMENTE ASI:

PREGUNTA: [pregunta corta y directa]
RESPUESTA: [respuesta en 1-2 lineas maximo]
LEY: [nombre de la ley]
ARTICULO: [Art. X]

REGLAS ESTRICTAS:
- NO explicaciones largas
- NO opciones A/B/C/D
- NO resúmenes
- SOLO el formato indicado
- Respuesta CORTA y DIRECTA
- Ley y artículos VERIFICADOS en BOE

EJEMPLO CORRECTO:
PREGUNTA: ¿Cuál es la edad ordinaria de jubilación en 2024?
RESPUESTA: 66 años y 6 meses
LEY: Ley General de la Seguridad Social
ARTICULO: Art. 205.1.a

EJEMPLO CORRECTO 2:
PREGUNTA: ¿Cuántos días de cotización se requieren para la prestación por desempleo contributiva?
RESPUESTA: 360 días en los 6 años anteriores
LEY: Ley General de la Seguridad Social
ARTICULO: Art. 269

HERRAMIENTAS DISPONIBLES:
- buscar_rag: Buscar información legal en Qdrant
- verificar_url: Verificar URLs del BOE

USA buscar_rag SIEMPRE antes de responder preguntas legales.
```

### 3. Configuración de Funciones

Las funciones se configuran en la sección "Tools" de Mistral Studio. Ver sección siguiente para el JSON completo.

---

## 🔧 Funciones (Tools) del Agente

### Función 1: buscar_rag

**Propósito:** Buscar información en la base de datos de legislación

**Cuándo usarla:**
- Cuando necesites citar un artículo específico
- Para verificar información legal
- Al generar preguntas de examen
- Para responder consultas sobre legislación

**Parámetros:**
- `query` (string, requerido): La consulta de búsqueda
- `top_k` (integer, opcional): Número de resultados (default: 5, max: 20)

**Ejemplo de uso interno:**
```json
{
  "query": "prestación por desempleo requisitos",
  "top_k": 5
}
```

### Función 2: verificar_url

**Propósito:** Verificar si una URL del BOE es válida, accesible y contiene el contenido esperado

**Cuándo usarla:**
- SIEMPRE antes de proporcionar una URL del BOE
- Para validar que el documento es una ley real (no resoluciones de ayuntamientos, nombramientos, etc.)
- Al citar un artículo específico, para verificar que existe en el documento

**Parámetros:**
- `url` (string, requerido): URL del BOE a verificar
- `articulo_citado` (string, opcional pero RECOMENDADO): Número del artículo que citas (ej: "205", "267.1")
- `ley_esperada` (string, opcional pero RECOMENDADO): Nombre de la ley esperada (ej: "LGSS", "LISOS")

**Ejemplo de uso interno:**
```json
{
  "url": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
  "articulo_citado": "205",
  "ley_esperada": "LGSS"
}
```

**La función devuelve:**
- ✅ Título real del documento
- ✅ Si el artículo citado existe
- ✅ Si el título coincide con la ley esperada
- ❌ Alerta si es una resolución de ayuntamiento, nombramiento, etc.

### Función 3: generar_pregunta_test (NUEVA)

**Propósito:** Generar UNA pregunta con UNA respuesta correcta verificada (SIN opciones múltiples)

**Cuándo usarla:**
- Cuando el usuario pida una pregunta de examen
- Para practicar temas específicos
- Al crear material de estudio para dataset de finetuning

**Parámetros:**
- `tema` (string, requerido): Tema sobre el que generar la pregunta
- `dificultad` (string, opcional): "basica", "intermedia", "avanzada", "truco"

**Ejemplo de uso interno:**
```json
{
  "tema": "prestación por desempleo",
  "dificultad": "avanzada"
}
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Consulta Legal Simple

**Usuario:** "¿Cuáles son los requisitos para la prestación por desempleo?"

**Agente:**
1. Llama a `buscar_rag` con query: "prestación por desempleo requisitos"
2. Analiza los resultados
3. Responde:

```
Para acceder a la prestación por desempleo, según la LGSS, se requiere:

1. **Situación legal de desempleo** (Art. 267 LGSS)
2. **Período mínimo de cotización:** 360 días en los 6 años anteriores (Art. 269 LGSS)
3. **Inscripción como demandante de empleo**
4. **No haber cumplido la edad de jubilación**
5. **Suscribir el compromiso de actividad**

**Fundamento legal:**
- LGSS, Art. 267: Define la situación legal de desempleo
- LGSS, Art. 269: Establece el período de cotización mínimo
- LGSS, Art. 270: Regula la duración de la prestación

**Duración:** Entre 4 y 24 meses según días cotizados.
```

### Ejemplo 2: Generar Pregunta de Examen

**Usuario:** "Genera una pregunta tipo test sobre infracciones laborales"

**Agente:**
1. Llama a `buscar_rag` con query: "infracciones laborales LISOS clasificación"
2. Analiza la información
3. Genera UNA pregunta con 4 opciones:

```
**Pregunta:** ¿Cuál de las siguientes conductas constituye una infracción muy grave según la LISOS?

A) No comunicar la apertura del centro de trabajo en plazo
B) No entregar el recibo de salarios en el plazo establecido
C) Emplear a trabajadores extranjeros sin autorización para trabajar
D) No informar a los trabajadores sobre los riesgos del puesto

**Respuesta correcta:** C

**Explicación:** El empleo de trabajadores extranjeros sin autorización para trabajar está tipificado como infracción muy grave en el artículo 23.1.a) de la LISOS. Las opciones A y B son infracciones leves, y la D es grave.

**Fuente:** LISOS, Art. 23.1.a) - Infracciones muy graves en materia de relaciones laborales
```

### Ejemplo 3: Verificar Referencia Legal

**Usuario:** "¿Es válida esta URL del BOE? https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"

**Agente:**
1. Llama a `verificar_url` con:
   - url: "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
   - articulo_citado: "205" (si está citando ese artículo)
   - ley_esperada: "LGSS"
2. Responde según el resultado:

```
✅ **URL válida y verificada**

**Título del documento:** Real Decreto Legislativo 8/2015, de 30 de octubre, por el que se aprueba el texto refundido de la Ley General de la Seguridad Social

**Verificaciones:**
- ✅ El título corresponde con LGSS
- ✅ El artículo 205 existe en el documento
- ✅ Es una ley oficial (NO es resolución de ayuntamiento ni nombramiento)

**Información:**
- Fecha: 30 de octubre de 2015
- Estado: Vigente (con modificaciones)
```

### Ejemplo 4: URL INVÁLIDA (Caso de error)

**Usuario:** "Verifica https://www.boe.es/buscar/doc.php?id=BOE-A-2024-12345"

**Agente:**
1. Llama a `verificar_url` con ley_esperada: "LGSS"
2. Detecta que NO es una ley:

```
❌ **URL NO VÁLIDA para citar como ley**

**Título del documento:** Resolución de 15 de marzo de 2024, del Ayuntamiento de...

**Problema detectado:**
- ❌ Este documento es una RESOLUCIÓN DE AYUNTAMIENTO, no una ley
- ❌ No corresponde con la LGSS que esperabas citar

**Acción:** Busca la URL correcta de la ley que quieres citar.
```

---

## 🔍 Troubleshooting

### Problema: El agente no encuentra información

**Posibles causas:**
1. La consulta es demasiado específica o usa términos incorrectos
2. La información no está en la base de datos
3. El `top_k` es muy bajo

**Soluciones:**
- Reformula la consulta con términos más generales
- Aumenta el `top_k` a 10-15
- Busca por conceptos relacionados

### Problema: Las respuestas no son precisas

**Posibles causas:**
1. Temperatura demasiado alta
2. No se está usando la función `buscar_rag`
3. El prompt del sistema no es claro

**Soluciones:**
- Ajusta temperatura a 0.2-0.3
- Refuerza en el prompt que DEBE usar las funciones
- Proporciona ejemplos más específicos

### Problema: El agente inventa información

**Posibles causas:**
1. No está usando las funciones correctamente
2. Temperatura muy alta
3. Prompt permite "creatividad"

**Soluciones:**
- Temperatura a 0.2
- Refuerza: "NO inventes información legal"
- Añade: "Si no encuentras información, dilo claramente"

### Problema: Errores de conexión con Qdrant

**Verificar:**
1. Credenciales de Qdrant Cloud correctas
2. Colección `leyes_seguridad_social` existe
3. API key válida

**Solución:**
- Verifica en el código de las funciones que las credenciales sean correctas
- Prueba la conexión directamente con el script de Python

---

## 📝 Notas Finales

### Mejoras Futuras

1. **Indexar materiales de academia** (337 MB disponibles)
   - Exámenes oficiales 2024
   - Simulacros y tests
   - Temarios específicos

2. **Añadir más funciones:**
   - `generar_examen_completo`: Crear exámenes de 100 preguntas
   - `explicar_articulo`: Análisis detallado de artículos
   - `comparar_leyes`: Comparar versiones de normativa

3. **Optimizaciones:**
   - Caché de consultas frecuentes
   - Reranking de resultados
   - Filtros por tipo de norma

### Recursos Adicionales

- **Documentación Mistral:** https://docs.mistral.ai/capabilities/function_calling
- **Documentación Qdrant:** https://qdrant.tech/documentation/
- **BOE:** https://www.boe.es/

---

## 🎯 Checklist de Configuración

- [ ] Crear agente en Mistral Studio
- [ ] Configurar modelo: Mistral Large 2
- [ ] Establecer temperatura: 0.3
- [ ] Copiar System Prompt (formato: UNA pregunta, UNA respuesta)
- [ ] Añadir función `buscar_rag`
- [ ] Añadir función `verificar_url`
- [ ] Añadir función `generar_pregunta_test`
- [ ] Probar con consulta simple
- [ ] Probar generación de UNA pregunta con UNA respuesta (SIN opciones múltiples)
- [ ] Verificar que cita ley y artículos correctamente
- [ ] Validar que NO empieza siempre con "Según el artículo..."
- [ ] Validar formato: PREGUNTA + RESPUESTA + LEY + ARTÍCULO

---

**Última actualización:** 4 de diciembre de 2025
**Versión:** 2.2 - Formato correcto: UNA pregunta, UNA respuesta
**Autor:** Sistema OpositAI

## 📋 Cambios en v2.2
- ✅ **FORMATO CORRECTO**: UNA pregunta, UNA respuesta (SIN opciones múltiples A/B/C/D)
- ✅ Formato: PREGUNTA + RESPUESTA + LEY + ARTÍCULO
- ✅ Verifica ley y artículos en BOE
- ✅ Instrucciones para variar inicio de respuestas (no siempre "Según el artículo...")
- ✅ NUNCA inventa datos - TODO verificado en BOE