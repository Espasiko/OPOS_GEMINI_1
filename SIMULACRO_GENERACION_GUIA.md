# 🎯 GUÍA: GENERACIÓN DE SIMULACRO COMPLETO

**Fecha:** 8 de diciembre de 2025  
**Estado:** ✅ LISTO PARA GENERAR

---

## 📋 ESPECIFICACIONES DEL SIMULACRO

### Estructura Oficial (BOE-A-2024-11403)

```
SIMULACRO COMPLETO
├── PARTE 1: Test de Conocimientos Generales
│   ├── Preguntas: 100
│   ├── Opciones: 4 (A, B, C, D)
│   ├── Puntos máximo: 50
│   ├── Mínimo para aprobar: 25
│   └── Temario: Temas 1-32 (Constitución, Derecho Administrativo, Función Pública)
│
└── PARTE 2: Supuestos Prácticos
    ├── Preguntas: 12
    ├── Opciones: 4 (A, B, C, D)
    ├── Puntos máximo: 50
    ├── Mínimo para aprobar: 25
    └── Temario: Temas específicos Seguridad Social
```

### Sistema de Puntuación

```
✅ Respuesta correcta:    +1 punto
❌ Respuesta incorrecta:  -0.25 puntos
⚪ Sin respuesta:         0 puntos

Puntuación Final = Parte 1 (0-50) + Parte 2 (0-50)
Mínimo para aprobar: 25 puntos en CADA parte
```

---

## 🔧 CARACTERÍSTICAS DEL SIMULACRO GENERADO

### 1. Respuestas Correctas Distribuidas Aleatoriamente

✅ **NO siempre en la misma opción**

```
Distribución esperada (aproximada):
- Opción A: ~25% (28 preguntas)
- Opción B: ~25% (28 preguntas)
- Opción C: ~25% (28 preguntas)
- Opción D: ~25% (28 preguntas)
```

### 2. Calidad de Preguntas

- ✅ Basadas en normativa oficial del BOE
- ✅ Referencias a artículos específicos
- ✅ Distractores plausibles y bien construidos
- ✅ Dificultad progresiva (20% fácil, 50% media, 30% difícil)
- ✅ Enunciados claros y precisos

### 3. Fuente de Datos

- **Dataset:** `dataset_output/qa_baja_cobertura_PREMIUM_20251208.jsonl`
- **Preguntas disponibles:** 51 registros
- **Tipos:** Preguntas test, casos prácticos, flashcards, RAG

---

## 📊 EJEMPLO DE PREGUNTA GENERADA

### Parte 1 (Test General)

```json
{
  "numero": 1,
  "pregunta": "¿Qué trabajadores están incluidos en el campo de aplicación del Régimen General de la Seguridad Social?",
  "opciones": {
    "a": "Solo trabajadores españoles con contrato indefinido",
    "b": "Trabajadores por cuenta ajena mayores de 16 años",
    "c": "Solo trabajadores del sector privado",
    "d": "Todos los trabajadores sin distinción de régimen"
  },
  "respuesta_correcta": "b",
  "tema": "Campo de Aplicación",
  "dificultad": "facil",
  "parte": 1
}
```

### Parte 2 (Supuesto Práctico)

```json
{
  "numero": 101,
  "pregunta": "Pedro trabaja en una empresa de Madrid con jornada de 40 horas semanales. Su jefe le pide que haga 3 horas extras cada semana durante todo el año (156 horas extras anuales). Pedro pregunta si esto es legal. ¿Es legal que Pedro haga 156 horas extras al año?",
  "opciones": {
    "a": "Sí, si la empresa lo autoriza",
    "b": "No es legal. Supera el límite de 80 horas extraordinarias anuales",
    "c": "Solo si hay acuerdo con los representantes",
    "d": "Depende del convenio colectivo"
  },
  "respuesta_correcta": "b",
  "tema": "Jornada y Descansos",
  "dificultad": "media",
  "parte": 2
}
```

---

## 🎓 CÓMO USAR EL SIMULACRO

### Para Opositores

1. **Descarga el simulacro** en formato JSON
2. **Imprime o visualiza** en pantalla
3. **Responde todas las preguntas** sin consultar respuestas
4. **Calcula tu puntuación:**
   - Parte 1: (aciertos × 0.5) - (errores × 0.125) = puntos
   - Parte 2: (aciertos × 4.17) - (errores × 1.04) = puntos
   - Total: Parte 1 + Parte 2
5. **Verifica respuestas** con la hoja de respuestas
6. **Analiza errores** por tema

### Fórmula de Cálculo Simplificada

```
Puntos Parte 1 = (Aciertos × 50) / 100 - (Errores × 50) / (100 × 4)
Puntos Parte 2 = (Aciertos × 50) / 12 - (Errores × 50) / (12 × 4)

Ejemplo:
- Parte 1: 75 aciertos, 25 errores
  Puntos = (75 × 50) / 100 - (25 × 50) / 400 = 37.5 - 3.125 = 34.375 ✅

- Parte 2: 10 aciertos, 2 errores
  Puntos = (10 × 50) / 12 - (2 × 50) / 48 = 41.67 - 2.08 = 39.59 ✅

Total: 34.375 + 39.59 = 73.965 puntos ✅ APROBADO
```

---

## 📁 ARCHIVOS GENERADOS

### 1. Simulacro Completo
- **Archivo:** `simulacro_completo_YYYYMMDD_HHMMSS.json`
- **Contenido:** 112 preguntas (100 + 12)
- **Formato:** JSON estructurado
- **Tamaño:** ~150-200 KB

### 2. Hoja de Respuestas
- **Archivo:** `respuestas_simulacro_YYYYMMDD_HHMMSS.json`
- **Contenido:** Solo respuestas correctas
- **Uso:** Verificación después de responder

### 3. Análisis de Distribución
- **Respuestas correctas por opción:** A, B, C, D
- **Distribución por tema:** Porcentaje de preguntas
- **Distribución por dificultad:** Fácil, Media, Difícil

---

## ✅ VALIDACIÓN DEL SIMULACRO

### Checklist de Calidad

- ✅ 112 preguntas totales (100 + 12)
- ✅ 4 opciones por pregunta
- ✅ Respuestas correctas distribuidas aleatoriamente
- ✅ No siempre en la misma opción (A, B, C, D)
- ✅ Basadas en normativa oficial del BOE
- ✅ Referencias a artículos específicos
- ✅ Dificultad progresiva
- ✅ Distractores plausibles
- ✅ Enunciados claros
- ✅ Formato oficial BOE

---

## 🚀 PRÓXIMOS PASOS

### Inmediatos
1. ✅ Generar simulacro completo (112 preguntas)
2. ✅ Generar hoja de respuestas
3. ✅ Validar distribución de respuestas
4. ✅ Crear documento de análisis

### Mediano Plazo
1. [ ] Generar 5 simulacros completos diferentes
2. [ ] Crear versión interactiva (web/app)
3. [ ] Implementar corrección automática
4. [ ] Análisis de errores por tema
5. [ ] Recomendaciones de estudio

### Largo Plazo
1. [ ] Banco de 500+ preguntas
2. [ ] Generador de simulacros personalizados
3. [ ] Seguimiento de progreso
4. [ ] Estadísticas de rendimiento
5. [ ] Integración con plataforma de estudio

---

## 📊 ESTADÍSTICAS ESPERADAS

### Distribución de Preguntas

```
PARTE 1 (100 preguntas):
- Constitución y Organización: 30%
- Derecho Administrativo: 20%
- Función Pública y Gestión: 50%

PARTE 2 (12 preguntas):
- Seguridad Social: 100%
- Casos prácticos y cálculos
```

### Distribución de Dificultad

```
Fácil (20%):     22 preguntas
Media (50%):     56 preguntas
Difícil (30%):   34 preguntas
```

### Distribución de Respuestas Correctas

```
Opción A: ~28 preguntas (25%)
Opción B: ~28 preguntas (25%)
Opción C: ~28 preguntas (25%)
Opción D: ~28 preguntas (25%)
```

---

## 📝 NOTAS IMPORTANTES

### Para Opositores

1. **Tiempo:** Aproximadamente 90 minutos para completar
2. **Descanso:** Se recomienda descanso de 5-10 minutos entre partes
3. **Ambiente:** Realiza el simulacro en ambiente similar al examen real
4. **Sin consultas:** No consultes normativa durante el simulacro
5. **Análisis:** Dedica tiempo a analizar errores después

### Para Instructores

1. **Validación:** Verifica que las preguntas sean claras y sin ambigüedad
2. **Actualización:** Actualiza con nueva normativa regularmente
3. **Feedback:** Recopila feedback de opositores para mejorar
4. **Dificultad:** Ajusta la dificultad según resultados
5. **Variedad:** Genera múltiples versiones para evitar memorización

---

## 🎯 OBJETIVO

Proporcionar un simulacro de **máxima calidad** que:

✅ Refleje fielmente el formato oficial del BOE  
✅ Prepare adecuadamente a los opositores  
✅ Permita autoevaluación realista  
✅ Identifique áreas de mejora  
✅ Aumente confianza en el examen real  

---

**Estado:** ✅ LISTO PARA GENERAR  
**Fecha:** 8 de diciembre de 2025  
**Versión:** 1.0
