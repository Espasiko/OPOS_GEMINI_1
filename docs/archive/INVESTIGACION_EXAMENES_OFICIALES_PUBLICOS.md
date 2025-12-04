# 🔍 INVESTIGACIÓN: Exámenes Oficiales Públicos de Oposiciones

**Fecha**: 1 Diciembre 2025  
**Objetivo**: Verificar disponibilidad real de exámenes oficiales para dataset

---

## ❌ REALIDAD: EXÁMENES OFICIALES SON ESCASOS

### **Hallazgos:**

**1. BOE - Convocatorias (NO exámenes completos)**
```
✅ Publica: Convocatorias, bases, temarios
❌ NO publica: Exámenes completos con preguntas
❌ NO publica: Respuestas correctas
❌ NO publica: Casos prácticos resueltos
```

**2. Lo que SÍ se publica en BOE:**
- Convocatorias de oposiciones
- Bases reguladoras
- Temarios oficiales (lista de temas)
- Listas de aprobados
- Recursos y resoluciones

**3. Lo que NO se publica:**
- ❌ Preguntas del examen tipo test
- ❌ Casos prácticos completos
- ❌ Respuestas correctas oficiales
- ❌ Criterios de corrección

---

## 📊 DISPONIBILIDAD REAL DE EXÁMENES PÚBLICOS

### **Fuentes Oficiales:**

**INSS (Instituto Nacional de la Seguridad Social)**
```
URL: https://www.seg-social.es
Contenido disponible:
├─ Guías de prestaciones ✅
├─ Manuales de procedimiento ✅
├─ Criterios de aplicación ✅
└─ Exámenes completos ❌ (NO disponibles)
```

**Ministerio de Inclusión, Seguridad Social y Migraciones**
```
URL: https://www.mites.gob.es
Contenido disponible:
├─ Convocatorias ✅
├─ Temarios oficiales ✅
├─ Estadísticas ✅
└─ Exámenes completos ❌ (NO disponibles)
```

**CENDOJ (Jurisprudencia)**
```
URL: https://www.poderjudicial.es
Contenido disponible:
├─ Sentencias completas ✅
├─ Casos reales resueltos ✅
├─ Doctrina jurisprudencial ✅
└─ Formato Q&A ❌ (requiere procesamiento)
```

---

## 🎯 ESTIMACIÓN REALISTA DE Q&A PÚBLICAS

### **Fuentes Reales Disponibles:**

**1. Temarios Oficiales BOE (100-200 Q&A)**
```
Contenido: Lista de temas oficiales
Uso: Generar preguntas teóricas básicas
Ejemplo:
  Tema 1: "La Seguridad Social en España"
  → Pregunta: "¿Cuáles son los principios de la Seguridad Social?"
  → Respuesta: Basada en legislación LGSS

Estimación: 100-200 Q&A básicas
```

**2. Resoluciones INSS (200-300 Q&A)**
```
Contenido: Resoluciones de casos reales
Uso: Extraer casos prácticos
Ejemplo:
  Resolución: "Denegación pensión jubilación por falta cotización"
  → Caso práctico: Situación + pregunta + resolución

Estimación: 200-300 casos prácticos
```

**3. Sentencias CENDOJ (300-500 Q&A)**
```
Contenido: Sentencias del Tribunal Supremo
Uso: Casos jurisprudenciales
Ejemplo:
  Sentencia: "Interpretación art. 205 LGSS sobre edad jubilación"
  → Q&A: Pregunta jurídica + doctrina aplicable

Estimación: 300-500 Q&A jurisprudenciales
```

**4. Guías y Manuales INSS (200-300 Q&A)**
```
Contenido: Procedimientos oficiales
Uso: Preguntas procedimentales
Ejemplo:
  Guía: "Cómo solicitar prestación IT"
  → Q&A: Pasos + requisitos + documentación

Estimación: 200-300 Q&A procedimentales
```

---

## 📊 COMPOSICIÓN REALISTA DEL DATASET

### **NUEVA PROPUESTA (10,000 Q&A):**

```
📊 DISTRIBUCIÓN REAL:

85% - Generadas con IA desde fuentes públicas ($5-7):
├─ 5,000 Q&A desde legislación BOE (Groq Llama 3.1)
├─ 2,000 Q&A desde Qdrant Cloud (Groq Llama 3.1)
└─ 1,500 Q&A variaciones (Mistral local)

10% - Fuentes públicas adaptadas (GRATIS):
├─ 200 Q&A de temarios oficiales BOE
├─ 300 Q&A de resoluciones INSS
├─ 300 Q&A de sentencias CENDOJ
└─ 200 Q&A de guías oficiales

5% - Revisión y creación humana:
├─ 300 Q&A creadas por especialistas
└─ 200 Q&A revisadas y mejoradas

💰 COSTE: ~$5-7 + tiempo especialistas
⚖️ LEGAL: 100% seguro
📈 CALIDAD: 90%+ con revisión
```

---

## ✅ FUENTES 100% LEGALES Y GRATUITAS (REALISTAS)

### **1. Legislación BOE (Ilimitado)**
```
✅ Ley General de Seguridad Social
✅ Reglamentos de desarrollo
✅ Reales Decretos
✅ Órdenes Ministeriales
✅ Códigos consolidados

Uso: Base para generar 7,000+ Q&A con IA
```

### **2. Resoluciones INSS (200-300 casos)**
```
✅ Resoluciones publicadas
✅ Criterios de aplicación
✅ Casos reales anonimizados

Uso: Casos prácticos reales
```

### **3. Jurisprudencia CENDOJ (300-500 casos)**
```
✅ Sentencias Tribunal Supremo
✅ Sentencias Tribunales Superiores
✅ Doctrina consolidada

Uso: Casos jurisprudenciales
```

### **4. Materiales Oficiales (200-300 Q&A)**
```
✅ Guías del INSS
✅ Manuales de procedimiento
✅ FAQs oficiales
✅ Informes anuales

Uso: Preguntas procedimentales
```

---

## 🚀 ESTRATEGIA FINAL RECOMENDADA

### **Enfoque Híbrido Realista:**

**FASE 1: Contenido Público (1,000 Q&A) - GRATIS**
```python
# Extraer de fuentes oficiales
sources = {
    "temarios_boe": 200,      # Preguntas teóricas básicas
    "resoluciones_inss": 300,  # Casos prácticos
    "sentencias_cendoj": 300,  # Jurisprudencia
    "guias_oficiales": 200,    # Procedimientos
}
```

**FASE 2: Generación IA (8,500 Q&A) - $5-7**
```python
# Usar Groq Llama 3.1 70B
# Input: Legislación de Qdrant + BOE
# Output: Q&A estilo oposición

topics = extract_topics_from_qdrant()  # 200+ temas
for topic in topics:
    legal_context = get_legal_context(topic)
    qa_batch = generate_qa_groq(topic, legal_context, count=40)
    # 200 temas × 40 Q&A = 8,000 Q&A
```

**FASE 3: Revisión Humana (500 Q&A) - Tiempo especialistas**
```python
# 10% del total para revisión
# Especialistas revisan y mejoran
# Crean Q&A específicas que falten
```

---

## 💰 COSTE REAL ACTUALIZADO

```
📊 Groq Llama 3.1 70B:

Generar 8,500 Q&A:
├─ Input: ~4M tokens (contexto legal) = $2.36
├─ Output: ~1.7M tokens (Q&A) = $1.34
└─ TOTAL: ~$3.70

Margen de seguridad (+50%): ~$5-7

⏱️ Tiempo generación: 2-3 horas
👥 Tiempo revisión: 15-20 horas
💰 Coste total: $5-7
```

---

## 🎯 CONCLUSIÓN

### **Realidad vs Expectativa:**

**❌ NO EXISTE:**
- 2,000 exámenes oficiales completos públicos
- Preguntas tipo test publicadas en BOE
- Casos prácticos oficiales con soluciones

**✅ SÍ EXISTE:**
- ~1,000 Q&A extraíbles de fuentes públicas
- Legislación completa para generar Q&A con IA
- Casos reales en resoluciones y sentencias

### **Estrategia Correcta:**

```
10% Fuentes públicas (1,000 Q&A) - GRATIS
85% Generación IA (8,500 Q&A) - $5-7
5% Revisión humana (500 Q&A) - Tiempo

Total: 10,000 Q&A de calidad
Coste: $5-7 + 15-20h revisión
Legal: 100% seguro
```

---

**Creado**: 1 Diciembre 2025  
**Actualizado**: 2 Diciembre 2025  

---

## 🔄 ACTUALIZACIÓN 2 DICIEMBRE 2025

### ¡HALLAZGO IMPORTANTE!

Tras revisar los materiales disponibles en `elemplos_leyes_info/de_mi_hija/`, se encontró:

**EXÁMENES OFICIALES REALES (bajados_academia/):**
- 12+ exámenes oficiales C1 SS (2022-2025) con respuestas
- Gestión Libre y Promoción Interna
- Exámenes extraordinarios

**SIMULACROS DE ACADEMIA (tests cortes/):**
- 7+ simulacros de Las Cortes con respuestas
- Cuadernillos de preguntas oficiales

**MATERIAL POR PRESTACIONES:**
- IT, IP, Jubilación, Muerte y Supervivencia
- Encuadramiento, Cotización
- Casos prácticos resueltos

**Ver documento completo**: `INVENTARIO_MATERIALES_OPOSICIONES_SS.md`

### Nueva Estimación:
- **~2,700 Q&A reales** de exámenes y simulacros
- **~1,500 Q&A** generables desde esquemas
- **~6,000 Q&A** generables desde Qdrant
- **Total: 10,000+ Q&A** de alta calidad

### Conclusión Actualizada:
**SÍ tenemos acceso a exámenes oficiales reales** a través de materiales de academia. Esto cambia completamente la estrategia del dataset, permitiendo un enfoque basado en material real de máxima calidad.

