# 📋 FORMATO OFICIAL OPOSICIONES - RESUMEN EJECUTIVO

**Fecha:** 8 de diciembre de 2025  
**Fuente:** BOE-A-2024-11403 (Convocatoria oficial junio 2024)  
**Estado:** ✅ VERIFICADO

---

## 🎯 FORMATO OFICIAL CONFIRMADO

### Estructura del Examen

**EJERCICIO ÚNICO** con **DOS PARTES**:

#### PARTE 1: Test General (100 preguntas)
- **Preguntas:** 100 tipo test
- **Opciones:** 4 (A, B, C, D)
- **Temario:** 32 temas generales
- **Puntos:** 50 máximo, 25 mínimo para aprobar

#### PARTE 2: Supuestos Prácticos (12 preguntas)
- **Preguntas:** 12 tipo test sobre casos prácticos
- **Opciones:** 4 (A, B, C, D)
- **Temario:** 18 temas específicos Seguridad Social
- **Puntos:** 50 máximo, 25 mínimo para aprobar

### Sistema de Puntuación

```
✅ Correcta:    +1.00 punto
❌ Incorrecta:  -0.25 puntos (penalización 1/4)
⚪ En blanco:   0.00 puntos

TOTAL = Parte 1 + Parte 2
REQUISITO: Mínimo 25 puntos en CADA parte
```

---

## 📊 DISTRIBUCIÓN TEMÁTICA

### Parte 1 - Temario General (32 temas → 100 preguntas)

**Bloque 1: Constitución y Organización (Temas 1-12) - ~30%**
- Constitución Española
- Organización del Estado
- Poderes del Estado
- Unión Europea
- Ministerio de Inclusión, SS y Migraciones

**Bloque 2: Derecho Administrativo (Temas 13-18) - ~20%**
- Fuentes del Derecho
- Actos administrativos
- Procedimiento administrativo
- Recursos administrativos

**Bloque 3: Función Pública y Gestión (Temas 19-32) - ~50%**
- Personal al servicio de AAPP
- Igualdad y violencia de género
- Transparencia y protección de datos
- Contratos y presupuestos
- Administración electrónica
- Prevención riesgos laborales
- Informática y ofimática

### Parte 2 - Temario Específico (18 temas → 12 preguntas)

**Seguridad Social:**
- Sistema de Seguridad Social
- Régimen General y Especiales
- Inscripción, afiliación, cotización
- Prestaciones (IT, IP, Jubilación, Muerte/Supervivencia)
- Desempleo y prestaciones familiares
- Procedimiento administrativo SS
- Infracciones y sanciones
- Mutuas y convenios internacionales

---

## 🎯 IMPLICACIONES PARA NUESTRO DATASET

### Ratio Oficial: 89% General / 11% Práctico

```python
# Para 500 registros:
DISTRIBUCION_RECOMENDADA = {
    "parte_1_general": 445,      # 89% - Preguntas de temario general
    "parte_2_practicos": 55       # 11% - Supuestos prácticos
}

# Subdistribución Parte 1:
BLOQUES_PARTE_1 = {
    "constitucion_organizacion": 134,  # 30% de 445
    "derecho_administrativo": 89,      # 20% de 445
    "funcion_publica": 222             # 50% de 445
}
```

### Características de Preguntas Parte 1 (General)

**Tipo:** Preguntas directas sobre normativa
**Formato:**
```
Según [normativa], ¿[pregunta específica]?

a) [Opción plausible]
b) [Opción plausible]
c) [Opción correcta]
d) [Opción plausible]
```

**Características:**
- Referencias a artículos específicos
- Plazos, requisitos, procedimientos
- Definiciones legales precisas
- Competencias y organización

### Características de Preguntas Parte 2 (Prácticos)

**Tipo:** Casos prácticos con cálculos y aplicación normativa
**Formato:**
```
[Contexto: 2-4 líneas describiendo situación]
[Datos específicos: fechas, importes, situaciones]
¿[Pregunta sobre aplicación de normativa]?

a) [Cálculo/procedimiento opción 1]
b) [Cálculo/procedimiento opción 2]
c) [Cálculo/procedimiento correcto]
d) [Cálculo/procedimiento opción 4]
```

**Características:**
- Situaciones reales de Seguridad Social
- Cálculos de prestaciones
- Aplicación de porcentajes y plazos
- Procedimientos administrativos específicos
- Requieren conocimiento preciso de normativa

---

## ✅ AJUSTES NECESARIOS EN SCRIPTS

### 1. Distribución de Preguntas

**ANTES:**
- Sin distinción clara entre general y práctico
- Distribución uniforme por temas

**AHORA:**
```python
# Configuración para generación:
CONFIG_OFICIAL = {
    "total_registros": 500,
    "parte_1_general": {
        "cantidad": 445,
        "tipo": "test_directo",
        "temas": range(1, 33),  # Temas 1-32
        "distribucion": {
            "constitucion": 0.30,
            "administrativo": 0.20,
            "funcion_publica": 0.50
        }
    },
    "parte_2_practicos": {
        "cantidad": 55,
        "tipo": "supuesto_practico",
        "temas": "seguridad_social",  # 18 temas específicos
        "caracteristicas": [
            "contexto_situacion",
            "datos_especificos",
            "calculos",
            "aplicacion_normativa"
        ]
    }
}
```

### 2. Prompts de Generación

**Prompt Parte 1 (General):**
```
Genera una pregunta tipo test para oposiciones C1 AGE:
- Tema: {tema_numero} - {tema_nombre}
- Formato: 4 opciones (A, B, C, D)
- Estilo: Pregunta directa sobre normativa
- Incluir: Referencia a artículo específico
- Dificultad: Media-Alta (aprobar = 50% aciertos)
- Distractores: Plausibles y bien construidos
```

**Prompt Parte 2 (Prácticos):**
```
Genera un supuesto práctico para oposiciones C1 AGE:
- Tema: Seguridad Social - {subtema}
- Formato: 4 opciones (A, B, C, D)
- Estructura:
  1. Contexto (2-4 líneas)
  2. Datos específicos (fechas, importes)
  3. Pregunta sobre aplicación normativa
  4. Opciones con cálculos/procedimientos
- Incluir: Cálculos si aplica
- Referencia: Artículo específico LGSS
- Dificultad: Alta (requiere cálculo + normativa)
```

### 3. Validación de Calidad

**Criterios Parte 1:**
- ✅ Referencia a normativa específica
- ✅ 4 opciones plausibles
- ✅ Distractores bien construidos
- ✅ Pregunta clara y precisa
- ✅ Respuesta verificable en BOE

**Criterios Parte 2:**
- ✅ Contexto realista
- ✅ Datos específicos incluidos
- ✅ Cálculo correcto (si aplica)
- ✅ Aplicación normativa precisa
- ✅ Opciones con procedimientos completos

---

## 📝 EJEMPLOS FORMATO OFICIAL

### Ejemplo Parte 1 (Test General)

```json
{
  "pregunta": "Según la Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas, ¿cuál es el plazo máximo para resolver y notificar un procedimiento administrativo cuando no se establezca plazo específico?",
  "opciones": {
    "a": "Un mes desde la fecha de inicio del procedimiento",
    "b": "Dos meses desde la fecha de inicio del procedimiento",
    "c": "Tres meses desde la fecha de inicio del procedimiento",
    "d": "Seis meses desde la fecha de inicio del procedimiento"
  },
  "respuesta_correcta": "c",
  "justificacion": "Art. 21.3 Ley 39/2015: El plazo máximo es de tres meses",
  "tema": "16 - Procedimiento Administrativo Común",
  "tipo": "parte_1_general",
  "dificultad": "media",
  "referencia_boe": "Ley 39/2015, Art. 21.3"
}
```

### Ejemplo Parte 2 (Supuesto Práctico)

```json
{
  "pregunta": "Un trabajador por cuenta ajena del Régimen General causa baja por incapacidad temporal el 15 de marzo de 2024. Su base de cotización es de 1.800€/mes (30 días). Según el Real Decreto Legislativo 8/2015, ¿qué prestación le corresponde del día 4º al 15º de baja?",
  "opciones": {
    "a": "60% de la base reguladora a cargo de la empresa",
    "b": "60% de la base reguladora a cargo de la Seguridad Social",
    "c": "75% de la base reguladora a cargo de la empresa",
    "d": "75% de la base reguladora a cargo de la Seguridad Social"
  },
  "respuesta_correcta": "a",
  "justificacion": "Art. 173 LGSS: Del 4º al 15º día, 60% BR a cargo de la empresa. Cálculo: (1.800/30) × 60% × 12 días = 432€",
  "tema": "Seguridad Social - Incapacidad Temporal",
  "tipo": "parte_2_practico",
  "dificultad": "alta",
  "referencia_boe": "RDL 8/2015, Art. 173",
  "calculo": {
    "base_diaria": 60.00,
    "porcentaje": 0.60,
    "dias": 12,
    "total": 432.00
  }
}
```

---

## 🚀 PRÓXIMOS PASOS

### Inmediatos:
1. ✅ Formato oficial documentado
2. [ ] Ajustar script `generar_500_premium_completo.py`
3. [ ] Crear script específico para Parte 2 (supuestos prácticos)
4. [ ] Validar distribución 89%/11%
5. [ ] Generar lote de prueba con nuevo formato

### Mediano Plazo:
1. [ ] Crear generador de exámenes completos (112 preguntas)
2. [ ] Implementar validación automática de formato
3. [ ] Sistema de dificultad calibrada (50% para aprobar)
4. [ ] Banco de supuestos prácticos con cálculos
5. [ ] Validación con opositores reales

---

## 📎 REFERENCIAS

- **BOE-A-2024-11403**: Resolución 25 mayo 2024
- **URL**: https://www.boe.es/buscar/doc.php?id=BOE-A-2024-11403
- **Documento completo**: `INVESTIGACION_FORMATO_OPOSICIONES_OFICIAL.md`
- **Fecha verificación**: 8 de diciembre de 2025

---

**Estado:** ✅ INFORMACIÓN OFICIAL VERIFICADA  
**Fiabilidad:** ⭐⭐⭐⭐⭐ MÁXIMA (Fuente BOE)  
**Aplicabilidad:** Inmediata para ajuste de scripts
