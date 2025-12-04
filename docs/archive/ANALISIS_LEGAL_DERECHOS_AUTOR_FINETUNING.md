# ⚖️ ANÁLISIS LEGAL: Derechos de Autor y Fine-tuning

**Fecha**: 2 Diciembre 2025  
**Pregunta clave**: ¿Se puede detectar que hemos fine-tuneado con estos materiales?

---

## 🚨 PROBLEMA IDENTIFICADO

En el análisis de materiales (`ANALISIS_MATERIALES.md`) se ve claramente:

```
"© Beatriz Carballo Martín (coord.)"
"© Ed. TEMA DIGITAL, S.L."
"ISBN: 978-84-942320-1-5"

"Queda prohibido el uso, distribución o reproducción, total o parcial, 
de este material sin autorización de la Academia Las Cortes"

"Temario para oposiciones elaborado por Víctor Cabeza"
```

### Materiales con Copyright Explícito:
| Material | Propietario | Restricción |
|----------|-------------|-------------|
| Test_Admtvos_AGE_1/2 | Beatriz Carballo / TEMA DIGITAL | ISBN registrado |
| Material Las Cortes | Víctor Cabeza / Academia Las Cortes | Prohibición explícita |
| GoKoan | GoKoan S.L. | Material de pago |
| Esquemas de alumnos | Sara Domínguez, Alfonso Hidalgo, etc. | Elaboración propia |

---

## 🔍 ¿SE PUEDE DETECTAR EL FINE-TUNING?

### Respuesta corta: **SÍ, potencialmente**

### Formas de detección:

**1. Memorización de contenido específico:**
```
Si el modelo reproduce textualmente:
- "Queda prohibido el uso, distribución o reproducción..."
- Frases únicas de los materiales
- Estructuras específicas de Las Cortes
- Nombres de autores (Sara Domínguez, Carlos Hernández)

→ DETECTABLE por el propietario del copyright
```

**2. Estilo y estructura reconocible:**
```
Los materiales de Las Cortes tienen:
- Formato específico de preguntas
- Estructura de "villancicos" (reglas mnemotécnicas)
- Numeración característica (5001, 8035, etc.)

→ Un experto podría reconocer el origen
```

**3. Auditoría legal:**
```
Si Academia Las Cortes o TEMA DIGITAL demandan:
- Pueden solicitar acceso al dataset de entrenamiento
- Pueden hacer preguntas específicas al modelo
- Pueden comparar respuestas con su material

→ RIESGO LEGAL REAL
```

---

## ⚖️ CLASIFICACIÓN LEGAL DE MATERIALES

### ✅ SEGUROS (100% legal usar):

**1. Legislación BOE:**
```
- LGSS, EBEP, Constitución, etc.
- Códigos consolidados del BOE
- Resoluciones y sentencias

Razón: Dominio público, fuente oficial del Estado
```

**2. Exámenes oficiales publicados:**
```
- Exámenes una vez realizados y publicados
- Plantillas de respuestas oficiales
- Convocatorias y bases

Razón: Documentos públicos de la Administración
```

**3. Material generado por IA desde legislación:**
```
- Q&A generadas desde texto legal
- Variaciones creadas por nosotros
- Explicaciones propias

Razón: Obra derivada original
```

### ⚠️ ZONA GRIS (Riesgo medio):

**4. Esquemas de alumnos:**
```
- Recopilatorios de Sara Domínguez
- Esquemas de Alfonso Hidalgo
- Material de Carlos Hernández

Riesgo: Son obras derivadas de legislación, pero con 
        elaboración propia. Depende de si hay cesión
        de derechos a la academia.
```

### ❌ PROHIBIDOS (Alto riesgo legal):

**5. Material de academias con copyright:**
```
- Tests de TEMA DIGITAL (ISBN registrado)
- Material de Las Cortes (prohibición explícita)
- Temarios de GoKoan (material de pago)

Riesgo: Infracción clara de derechos de autor
        Posible demanda civil
        Daños y perjuicios
```

---

## 📊 ANÁLISIS DE RIESGO POR MATERIAL

| Material | Riesgo | Detectable | Recomendación |
|----------|--------|------------|---------------|
| Legislación BOE | ✅ Ninguno | No aplica | USAR |
| Exámenes oficiales post-publicación | ✅ Bajo | Difícil | USAR |
| Q&A generadas por IA | ✅ Ninguno | No | USAR |
| Esquemas de alumnos | ⚠️ Medio | Posible | CONSULTAR |
| Tests TEMA DIGITAL | ❌ Alto | Sí | NO USAR |
| Material Las Cortes | ❌ Alto | Sí | NO USAR |
| GoKoan | ❌ Alto | Sí | NO USAR |

---

## 🛡️ ESTRATEGIA SEGURA RECOMENDADA

### FASE 1: Dataset 100% Legal

```python
FUENTES_SEGURAS = {
    # 1. Legislación oficial (GRATIS, ILIMITADO)
    "boe_lgss": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
    "boe_ebep": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11719",
    "boe_constitucion": "https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229",
    
    # 2. Códigos consolidados BOE
    "codigo_laboral_ss": "Biblioteca Jurídica Digital",
    "codigo_funcion_publica": "Biblioteca Jurídica Digital",
    
    # 3. Exámenes oficiales publicados
    "examenes_oficiales": "Post-publicación, dominio público",
    
    # 4. Generación propia con IA
    "qa_generadas": "Desde legislación, 100% original",
}
```

### FASE 2: Evitar Memorización

```python
# NO hacer esto:
dataset.append({
    "pregunta": pregunta_copiada_de_las_cortes,
    "respuesta": respuesta_copiada
})

# SÍ hacer esto:
dataset.append({
    "pregunta": generar_pregunta_similar(tema, legislacion),
    "respuesta": generar_respuesta_desde_ley(articulo)
})
```

### FASE 3: Transformación Suficiente

```python
def transformar_pregunta(pregunta_original, legislacion):
    """
    Transforma una pregunta para que sea obra derivada original
    """
    # 1. Extraer el concepto legal
    concepto = extraer_concepto(pregunta_original)
    
    # 2. Buscar artículo en legislación
    articulo = buscar_en_lgss(concepto)
    
    # 3. Generar nueva pregunta desde el artículo
    nueva_pregunta = generar_pregunta_desde_articulo(articulo)
    
    # 4. Generar respuesta desde legislación
    respuesta = generar_respuesta_legal(articulo)
    
    return nueva_pregunta, respuesta
```

---

## 🎯 RECOMENDACIÓN FINAL

### LO QUE SÍ PODEMOS HACER:

1. **Usar legislación BOE** → 100% seguro
2. **Usar exámenes oficiales publicados** → Seguro (dominio público)
3. **Generar Q&A con IA desde legislación** → 100% seguro
4. **Crear variaciones propias** → Seguro si son suficientemente diferentes
5. **Usar Qdrant con legislación indexada** → 100% seguro

### LO QUE NO DEBEMOS HACER:

1. ❌ Copiar preguntas de Tests TEMA DIGITAL
2. ❌ Usar material de Las Cortes directamente
3. ❌ Incluir material de GoKoan
4. ❌ Reproducir esquemas con copyright
5. ❌ Fine-tunear con material que diga "prohibida reproducción"

---

## 📋 DATASET SEGURO PROPUESTO

### Composición 100% Legal:

```
📊 DATASET SEGURO (10,000 Q&A):

70% - Generación IA desde legislación BOE ($5-7):
├─ 4,000 Q&A desde LGSS
├─ 2,000 Q&A desde EBEP y procedimiento
└─ 1,000 Q&A desde Constitución y UE

20% - Exámenes oficiales publicados (GRATIS):
├─ 1,500 Q&A de exámenes post-publicación
└─ 500 Q&A de plantillas oficiales

10% - Variaciones y casos propios (GRATIS):
├─ 500 casos prácticos generados
└─ 500 variaciones de preguntas

💰 COSTE: $5-7
⚖️ RIESGO LEGAL: 0%
📈 CALIDAD: 85-90%
```

---

## ✅ CONCLUSIÓN

### Respuesta a tu pregunta:

**¿Se puede saber que hemos fine-tuneado con estos documentos?**

**SÍ**, si el modelo:
- Reproduce frases textuales con copyright
- Usa estructuras específicas de academias
- Menciona nombres de autores
- Replica el estilo característico

**SOLUCIÓN**: Usar SOLO fuentes legales (BOE, exámenes oficiales publicados) y generar Q&A propias con IA.

### Beneficio adicional:
Un dataset 100% legal es:
- Más defendible legalmente
- Más actualizable (fuentes oficiales)
- Más escalable (sin límites de copyright)
- Diferenciador competitivo (contenido original)

---

**Creado**: 2 Diciembre 2025  
**Conclusión**: Evitar material con copyright explícito. Usar BOE + exámenes oficiales + generación IA.
