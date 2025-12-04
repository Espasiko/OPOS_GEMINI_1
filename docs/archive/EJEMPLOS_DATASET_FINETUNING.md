# 📚 Ejemplos de Dataset para Fine-tuning

## 🎯 Formato Recomendado: MIXTO (70% examen + 30% consulta)

---

## 📝 Formato 1: Pregunta Tipo Test (70% del dataset)

### Ejemplo 1: Jubilación

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Genera una pregunta tipo test sobre la edad ordinaria de jubilación en 2024"
    },
    {
      "role": "assistant",
      "content": "**Pregunta 1:** ¿Cuál es la edad ordinaria de jubilación en 2024 para una persona con menos de 37 años cotizados?\n\nA) 65 años\nB) 66 años\nC) 66 años y 6 meses\nD) 67 años\n\n**Respuesta correcta:** D\n\n**Explicación:** Según el artículo 205.1.a) de la LGSS, en 2024 la edad ordinaria de jubilación es de 67 años para quienes tengan cotizados menos de 37 años. Solo se puede jubilar a los 65 años quien tenga cotizados 37 años o más.\n\n**Fuente:** LGSS, Art. 205.1.a) (Real Decreto Legislativo 8/2015)"
    }
  ]
}
```

### Ejemplo 2: Infracciones Laborales

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Genera una pregunta sobre infracciones muy graves en materia laboral"
    },
    {
      "role": "assistant",
      "content": "**Pregunta 2:** Según la LISOS, ¿cuál de las siguientes conductas constituye una infracción muy grave?\n\nA) No comunicar la apertura del centro de trabajo en el plazo establecido\nB) No entregar el recibo de salarios en el plazo reglamentario\nC) Emplear a trabajadores extranjeros sin autorización para trabajar\nD) No informar a los trabajadores sobre los riesgos del puesto de trabajo\n\n**Respuesta correcta:** C\n\n**Explicación:** El empleo de trabajadores extranjeros sin autorización para trabajar está tipificado como infracción muy grave en el artículo 23.1.a) de la LISOS. La opción A es infracción leve (art. 21), la B es infracción leve (art. 21), y la D es infracción grave (art. 22).\n\n**Fuente:** LISOS, Art. 23.1.a) - Infracciones muy graves en materia de relaciones laborales"
    }
  ]
}
```

### Ejemplo 3: Prestación por Desempleo

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Crea una pregunta sobre los requisitos de la prestación por desempleo"
    },
    {
      "role": "assistant",
      "content": "**Pregunta 3:** ¿Cuál es el período mínimo de cotización requerido para acceder a la prestación contributiva por desempleo?\n\nA) 180 días en los últimos 4 años\nB) 360 días en los últimos 6 años\nC) 365 días en los últimos 6 años\nD) 720 días en los últimos 6 años\n\n**Respuesta correcta:** B\n\n**Explicación:** Según el artículo 269.1 de la LGSS, para tener derecho a la prestación contributiva por desempleo se requiere haber cotizado al menos 360 días dentro de los 6 años anteriores a la situación legal de desempleo o al momento en que cesó la obligación de cotizar.\n\n**Fuente:** LGSS, Art. 269.1 - Período mínimo de cotización"
    }
  ]
}
```

---

## 💬 Formato 2: Consulta Directa (30% del dataset)

### Ejemplo 1: Consulta sobre Base Reguladora

```json
{
  "messages": [
    {
      "role": "user",
      "content": "¿Qué es la base reguladora de la pensión de jubilación?"
    },
    {
      "role": "assistant",
      "content": "La base reguladora de la pensión de jubilación es la cantidad que sirve de referencia para calcular el importe de la pensión. Se calcula dividiendo las bases de cotización de un período determinado entre el número de meses de ese período.\n\n**Fundamento legal:**\n- LGSS, Art. 209: Establece que la base reguladora se calcula con las bases de cotización de los últimos años de cotización\n- LGSS, Art. 210: Regula el cálculo específico, actualmente se toman las bases de los últimos 25 años (300 meses)\n\n**Contexto adicional:** Las bases se actualizan según el IPC antes de hacer el cálculo, para reflejar el valor real del dinero en cada momento."
    }
  ]
}
```

### Ejemplo 2: Consulta sobre Incapacidad Permanente

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Explícame los grados de incapacidad permanente"
    },
    {
      "role": "assistant",
      "content": "La incapacidad permanente se clasifica en cuatro grados según la reducción de la capacidad laboral:\n\n**Fundamento legal:**\n- LGSS, Art. 193: Define los grados de incapacidad permanente\n\n**1. Incapacidad Permanente Parcial (IPP):**\nDisminución no inferior al 33% del rendimiento normal para la profesión habitual, sin impedir las tareas fundamentales.\n\n**2. Incapacidad Permanente Total (IPT):**\nInhabilita al trabajador para realizar todas o las fundamentales tareas de su profesión habitual, pero puede dedicarse a otra distinta.\n\n**3. Incapacidad Permanente Absoluta (IPA):**\nInhabilita por completo al trabajador para toda profesión u oficio.\n\n**4. Gran Invalidez (GI):**\nCuando el trabajador con incapacidad permanente necesita la asistencia de otra persona para los actos más esenciales de la vida.\n\n**Contexto adicional:** Cada grado tiene una prestación económica diferente, siendo la Gran Invalidez la que otorga mayor cuantía."
    }
  ]
}
```

### Ejemplo 3: Consulta sobre Cotización

```json
{
  "messages": [
    {
      "role": "user",
      "content": "¿Cuáles son las bases de cotización mínimas y máximas en 2024?"
    },
    {
      "role": "assistant",
      "content": "Las bases de cotización para 2024 están establecidas en el Real Decreto de bases de cotización que se publica anualmente.\n\n**Fundamento legal:**\n- LGSS, Art. 147: Regula las bases de cotización\n- RD anual: Establece las cuantías concretas para cada año\n\n**Bases 2024 (Régimen General):**\n- Base mínima: 1.323 € mensuales\n- Base máxima: 4.720,50 € mensuales\n\n**Contexto adicional:** Estas bases se actualizan anualmente según el IPC y otros factores económicos. Los autónomos tienen bases diferentes que pueden elegir dentro de unos límites."
    }
  ]
}
```

---

## 📊 Estructura del Dataset Completo

### Archivo: `dataset_finetuning.jsonl`

```jsonl
{"messages": [{"role": "user", "content": "Genera pregunta sobre jubilación"}, {"role": "assistant", "content": "**Pregunta 1:** ¿Cuál es la edad...?\n\nA)...\nB)...\nC)...\nD)...\n\n**Respuesta correcta:** D\n\n**Explicación:**...\n\n**Fuente:**..."}]}
{"messages": [{"role": "user", "content": "Genera pregunta sobre LISOS"}, {"role": "assistant", "content": "**Pregunta 2:** Según la LISOS...?\n\nA)...\nB)...\nC)...\nD)...\n\n**Respuesta correcta:** C\n\n**Explicación:**...\n\n**Fuente:**..."}]}
{"messages": [{"role": "user", "content": "¿Qué es la base reguladora?"}, {"role": "assistant", "content": "La base reguladora es...\n\n**Fundamento legal:**\n- LGSS, Art. 209:...\n\n**Contexto adicional:**..."}]}
{"messages": [{"role": "user", "content": "Genera pregunta sobre desempleo"}, {"role": "assistant", "content": "**Pregunta 3:** ¿Cuál es el período...?\n\nA)...\nB)...\nC)...\nD)...\n\n**Respuesta correcta:** B\n\n**Explicación:**...\n\n**Fuente:**..."}]}
{"messages": [{"role": "user", "content": "Explícame los grados de incapacidad"}, {"role": "assistant", "content": "La incapacidad permanente se clasifica...\n\n**Fundamento legal:**...\n\n**Contexto adicional:**..."}]}
```

---

## 🎯 Distribución Recomendada

### Para 1,000 ejemplos:

```
📊 DATASET COMPLETO (1,000 ejemplos)
│
├── 📝 FORMATO EXAMEN (700 ejemplos - 70%)
│   ├── Jubilación: 150 ejemplos
│   ├── Incapacidad: 100 ejemplos
│   ├── Desempleo: 100 ejemplos
│   ├── Cotización: 100 ejemplos
│   ├── LISOS (Infracciones): 100 ejemplos
│   ├── Procedimiento Administrativo: 75 ejemplos
│   ├── Prestaciones familiares: 50 ejemplos
│   └── Otros temas: 25 ejemplos
│
└── 💬 FORMATO CONSULTA (300 ejemplos - 30%)
    ├── Conceptos básicos: 100 ejemplos
    ├── Cálculos y fórmulas: 75 ejemplos
    ├── Procedimientos: 75 ejemplos
    └── Casos prácticos: 50 ejemplos
```

---

## 📏 Métricas de Calidad

### Cada ejemplo debe tener:

✅ **Referencias legales precisas**
- Artículo específico (ej: "Art. 205.1.a LGSS")
- Ley completa (ej: "Real Decreto Legislativo 8/2015")

✅ **Información verificada**
- Datos actualizados a 2024
- Verificados en BOE o base de datos

✅ **Formato consistente**
- Estructura uniforme
- Markdown correcto
- Numeración clara

✅ **Distractores plausibles** (para formato examen)
- Opciones incorrectas pero creíbles
- Basadas en confusiones comunes
- No obviamente falsas

✅ **Explicaciones completas**
- Justifica la respuesta correcta
- Explica por qué las otras son incorrectas
- Añade contexto relevante

---

## 🔧 Script para Generar Dataset

```python
import json

def crear_ejemplo_examen(pregunta, opciones, correcta, explicacion, fuente):
    """Crea un ejemplo en formato examen"""
    return {
        "messages": [
            {
                "role": "user",
                "content": f"Genera una pregunta tipo test sobre {pregunta}"
            },
            {
                "role": "assistant",
                "content": f"""**Pregunta:** {pregunta}

A) {opciones['a']}
B) {opciones['b']}
C) {opciones['c']}
D) {opciones['d']}

**Respuesta correcta:** {correcta}

**Explicación:** {explicacion}

**Fuente:** {fuente}"""
            }
        ]
    }

def crear_ejemplo_consulta(pregunta, respuesta, fundamento, contexto=""):
    """Crea un ejemplo en formato consulta"""
    content = f"""{respuesta}

**Fundamento legal:**
{fundamento}"""
    
    if contexto:
        content += f"\n\n**Contexto adicional:** {contexto}"
    
    return {
        "messages": [
            {
                "role": "user",
                "content": pregunta
            },
            {
                "role": "assistant",
                "content": content
            }
        ]
    }

# Ejemplo de uso
ejemplo1 = crear_ejemplo_examen(
    pregunta="la edad ordinaria de jubilación en 2024",
    opciones={
        'a': '65 años',
        'b': '66 años',
        'c': '66 años y 6 meses',
        'd': '67 años'
    },
    correcta='D',
    explicacion="Según el artículo 205.1.a) de la LGSS...",
    fuente="LGSS, Art. 205.1.a)"
)

ejemplo2 = crear_ejemplo_consulta(
    pregunta="¿Qué es la base reguladora?",
    respuesta="La base reguladora es la cantidad que sirve de referencia...",
    fundamento="- LGSS, Art. 209: Establece que...\n- LGSS, Art. 210: Regula el cálculo...",
    contexto="Las bases se actualizan según el IPC..."
)

# Guardar en JSONL
with open('dataset_finetuning.jsonl', 'w', encoding='utf-8') as f:
    f.write(json.dumps(ejemplo1, ensure_ascii=False) + '\n')
    f.write(json.dumps(ejemplo2, ensure_ascii=False) + '\n')
```

---

## 📈 Tamaño Recomendado del Dataset

| Objetivo | Ejemplos Mínimos | Ejemplos Óptimos | Tokens Aprox. |
|----------|------------------|------------------|---------------|
| Prueba | 100 | 200 | 80K |
| Básico | 500 | 1,000 | 400K |
| Intermedio | 1,000 | 2,500 | 1M |
| Avanzado | 2,500 | 5,000 | 2M |
| Producción | 5,000 | 10,000+ | 4M+ |

---

**Recomendación:** Empieza con 1,000 ejemplos (70% examen + 30% consulta) y evalúa resultados antes de escalar.
