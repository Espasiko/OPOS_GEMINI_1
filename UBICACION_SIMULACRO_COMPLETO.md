# 📍 UBICACIÓN DEL SIMULACRO COMPLETO

**Fecha:** 8 de diciembre de 2025

---

## 🎯 SIMULACROS DISPONIBLES

### 1. ✅ SIMULACRO COMPLETO (112 preguntas)

**Archivo:** `dataset_output/SIMULACRO_COMPLETO_112_OFICIAL_BOE.json`

**Características:**
- ✅ **112 preguntas** (formato oficial BOE)
- ✅ **Parte 1:** 100 preguntas generales
- ✅ **Parte 2:** 12 supuestos prácticos
- ✅ **Respuestas distribuidas aleatoriamente**
- ✅ **Basado en normativa oficial del BOE**
- ✅ **Incluye instrucciones de calificación**

### 2. ✅ SIMULACRO MINI (40 preguntas)

**Archivo:** `dataset_output/SIMULACRO_MINI_5_40_PREGUNTAS.json`

**Características:**
- ✅ **40 preguntas** (versión reducida)
- ✅ **Parte 1:** 30 preguntas generales
- ✅ **Parte 2:** 10 supuestos prácticos
- ✅ **Respuestas distribuidas aleatoriamente**
- ✅ **Completamente terminado**

### 3. ✅ SIMULACRO EJEMPLO (20 preguntas)

**Archivo:** `dataset_output/SIMULACRO_EJEMPLO_20_PREGUNTAS.json`

**Características:**
- ✅ **20 preguntas** (ejemplo pequeño)
- ✅ **Parte 1:** 15 preguntas generales
- ✅ **Parte 2:** 5 supuestos prácticos
- ✅ **Completamente terminado**

---

## 📊 COMPARACIÓN DE SIMULACROS

| Simulacro | Preguntas | Parte 1 | Parte 2 | Estado | Uso Recomendado |
|-----------|-----------|---------|---------|--------|-----------------|
| **COMPLETO 112** | 112 | 100 | 12 | ✅ Listo | Simulacro oficial completo |
| **MINI 40** | 40 | 30 | 10 | ✅ Terminado | Práctica rápida |
| **EJEMPLO 20** | 20 | 15 | 5 | ✅ Terminado | Demostración |

---

## 🎯 RECOMENDACIÓN

### Para Simulacro Oficial Completo:

**Usa:** `dataset_output/SIMULACRO_COMPLETO_112_OFICIAL_BOE.json`

Este archivo contiene:
- ✅ Estructura oficial del BOE
- ✅ 112 preguntas (100 + 12)
- ✅ Instrucciones de calificación
- ✅ Fórmulas de cálculo
- ✅ Estadísticas esperadas
- ✅ Referencias normativas

### Para Práctica Rápida:

**Usa:** `dataset_output/SIMULACRO_MINI_5_40_PREGUNTAS.json`

Este archivo contiene:
- ✅ 40 preguntas completas
- ✅ Todas las preguntas con 4 opciones
- ✅ Respuestas distribuidas aleatoriamente
- ✅ Cálculo de puntuación incluido

---

## 📋 CÓMO USAR EL SIMULACRO COMPLETO

### Paso 1: Abrir el archivo
```
dataset_output/SIMULACRO_COMPLETO_112_OFICIAL_BOE.json
```

### Paso 2: Leer las instrucciones
- Duración: 90 minutos
- Penalización: -0.25 por error
- Mínimo: 25 puntos por parte

### Paso 3: Responder las preguntas
- Parte 1: Preguntas 1-100 (Test General)
- Parte 2: Preguntas 101-112 (Supuestos Prácticos)

### Paso 4: Calcular puntuación
```
Parte 1: (Aciertos × 50) / 100 - (Errores × 50) / 400
Parte 2: (Aciertos × 50) / 12 - (Errores × 50) / 48
Total: Parte 1 + Parte 2
```

### Paso 5: Verificar aprobado
- ✅ Mínimo 25 puntos en Parte 1
- ✅ Mínimo 25 puntos en Parte 2
- ✅ Total mínimo: 50 puntos

---

## 🔧 GENERACIÓN AUTOMÁTICA

Si necesitas generar más simulacros:

**Script:** `dataset_generator/crear_simulacro_112_completo.py`

**Comando:**
```bash
python dataset_generator/crear_simulacro_112_completo.py
```

**Resultado:**
- Genera simulacro completo de 112 preguntas
- Respuestas distribuidas aleatoriamente
- Basado en dataset verificado
- Incluye estadísticas

---

## ✅ ESTADO ACTUAL

### Simulacros Terminados:

1. ✅ **SIMULACRO_COMPLETO_112_OFICIAL_BOE.json** - Simulacro oficial completo
2. ✅ **SIMULACRO_MINI_5_40_PREGUNTAS.json** - Simulacro de 40 preguntas
3. ✅ **SIMULACRO_EJEMPLO_20_PREGUNTAS.json** - Simulacro de ejemplo

### Documentación Completa:

1. ✅ **INVESTIGACION_FORMATO_OPOSICIONES_OFICIAL.md** - Investigación BOE
2. ✅ **SIMULACRO_GENERACION_GUIA.md** - Guía de generación
3. ✅ **RESUMEN_SIMULACRO_GENERADO.md** - Resumen detallado
4. ✅ **UBICACION_SIMULACRO_COMPLETO.md** - Este documento

---

## 🎯 CONCLUSIÓN

**El simulacro completo de 112 preguntas está disponible en:**

```
dataset_output/SIMULACRO_COMPLETO_112_OFICIAL_BOE.json
```

✅ **Formato oficial BOE verificado**  
✅ **Respuestas distribuidas aleatoriamente**  
✅ **Basado en normativa oficial**  
✅ **Listo para usar**  

---

**Estado:** ✅ COMPLETADO  
**Fecha:** 8 de diciembre de 2025  
**Versión:** 1.0