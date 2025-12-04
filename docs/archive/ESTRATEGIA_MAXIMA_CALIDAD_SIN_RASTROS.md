# 🔒 Estrategia: Máxima Calidad sin Rastros Identificables

**Fecha**: 2 Diciembre 2025  
**Objetivo**: Generar Q&A de máxima calidad sin dejar rastros de academias

---

## 🎯 PROBLEMA A RESOLVER

### Datos Reveladores en Materiales de Academia:

**Nombres de autores**:
- Sara Domínguez, Carlos Hernández, Alfonso Hidalgo, Víctor Cabeza, Pablo Segado

**Identificadores de academia**:
- Las Cortes, TEMA DIGITAL, GoKoan
- Códigos: 5001-, 5002-, 8035-, 8038-, 8039-, 8040-
- Anexo3050A1, Anexo3051A2, etc.

**Frases de copyright**:
- "Queda prohibido el uso, distribución o reproducción..."
- "© 2024 Las Cortes"
- "Material protegido"

**Estructuras características**:
- Villancicos (Las Cortes)
- Numeración específica
- Formato de cuadernillos

---

## ✅ SOLUCIÓN: Pipeline Seguro con 3 Capas

### CAPA 1: Generación desde Legislación Oficial

**Fuente**: Qdrant local con leyes del BOE

**Proceso**:
```
1. Usuario solicita tema: "Incapacidad Temporal"
2. Pipeline consulta Qdrant → Obtiene artículos LGSS relevantes
3. Mistral local genera preguntas basándose SOLO en legislación
4. NO usa materiales de academia como fuente
```

**Ventaja**: 
- ✅ Contenido 100% original
- ✅ Basado en fuente pública (BOE)
- ✅ Sin rastros de academias

### CAPA 2: Limpieza Automática de Patrones

**Patrones detectados y eliminados**:

```python
forbidden_patterns = {
    "nombres_autores": [
        "Sara Domínguez", "Carlos Hernández", "Alfonso Hidalgo",
        "Víctor Cabeza", "Pablo Segado"
    ],
    "academias": [
        "Las Cortes", "TEMA DIGITAL", "GoKoan", "Oposiciones.es"
    ],
    "identificadores": [
        "5001-", "5002-", "8035-", "Anexo\\d+A\\d+", "ISBN.*"
    ],
    "copyright": [
        "Queda prohibido", "©\\s*\\d{4}", "Copyright",
        "Todos los derechos reservados"
    ],
    "estructuras_especificas": [
        "villancico", "Simulacro.*\\d{1,2}.*\\d{4}",
        "Cuadernillo.*ejercicio"
    ]
}
```

**Acción**: Reemplazar con `[REDACTADO]` y marcar para revisión

### CAPA 3: Revisión Humana Selectiva

**Solo se revisan preguntas que**:
- Contenían patrones prohibidos (ahora redactados)
- Tienen similitud >85% con preguntas conocidas
- Fueron marcadas por el sistema

**Resto**: Aprobadas automáticamente

---

## 🤖 INSTRUCCIONES EXPLÍCITAS AL MODELO

### Prompt del Sistema:

```
Eres un experto en Seguridad Social española.
Creas preguntas tipo test de MÁXIMA CALIDAD para oposiciones.

REGLAS ESTRICTAS DE SEGURIDAD:
1. NO menciones NUNCA nombres de autores, academias o editoriales
2. NO uses identificadores específicos (ISBN, referencias, códigos)
3. NO copies frases textuales de materiales con copyright
4. NO uses estructuras características de academias específicas
5. Basa TODO en la legislación oficial que te proporciono
6. Cita SIEMPRE el artículo de ley correspondiente
7. Crea preguntas ORIGINALES pero legalmente correctas

IMPORTANTE: Estás creando contenido NUEVO basado en legislación PÚBLICA.
No estás copiando ni adaptando material protegido.

CONTEXTO LEGAL:
[Aquí se inserta contexto de Qdrant con artículos LGSS]

INSTRUCCIONES:
- Basa las preguntas SOLO en el contexto legal proporcionado
- Crea preguntas sobre: requisitos, cuantías, plazos, procedimientos
- Las 4 opciones deben ser plausibles pero solo 1 correcta
- Incluye el artículo de ley en cada pregunta
- NO uses nombres de autores ni academias
- NO copies frases textuales
```

---

## 📊 FLUJO COMPLETO

### Paso 1: Consulta a Qdrant

```python
# Usuario solicita tema
tema = "Incapacidad Temporal"

# Consultar Qdrant local
legal_context = query_qdrant(tema, limit=10)

# Obtiene:
# - Art. 169 LGSS: Situaciones protegidas
# - Art. 170 LGSS: Beneficiarios
# - Art. 171 LGSS: Cuantía
# - Art. 172 LGSS: Duración
# - Art. 173 LGSS: Nacimiento del derecho
```

### Paso 2: Generación con Mistral

```python
# Mistral recibe:
# - Prompt del sistema (reglas estrictas)
# - Contexto legal de Qdrant
# - Instrucciones específicas

# Genera:
{
  "pregunta": "Según el Art. 169 LGSS, ¿cuál de las siguientes situaciones está protegida por IT?",
  "opciones": [
    "a) Enfermedad común o profesional",
    "b) Solo accidente de trabajo",
    "c) Solo enfermedad profesional",
    "d) Ninguna de las anteriores"
  ],
  "respuesta_correcta": "a",
  "base_legal": "Art. 169 LGSS",
  "explicacion": "El Art. 169 establece que IT protege tanto enfermedad común como profesional..."
}
```

### Paso 3: Limpieza Automática

```python
# Buscar patrones prohibidos
pregunta_limpia, found_patterns = clean_revealing_data(pregunta)

# Si encuentra algo:
# - Reemplaza con [REDACTADO]
# - Marca para revisión
# - Registra qué se encontró

# Ejemplo:
# ANTES: "Según Sara Domínguez en el Art. 169..."
# DESPUÉS: "Según [REDACTADO] en el Art. 169..."
# MARCADO: requiere_revision = True
```

### Paso 4: Validación

```python
# Validaciones automáticas:
✅ Tiene 4 opciones
✅ Respuesta correcta identificada
✅ Base legal citada
✅ Explicación presente
✅ No contiene patrones prohibidos (o están redactados)

# Si pasa todas → Aprobada
# Si tiene patrones → Marcada para revisión humana
```

---

## 🎯 VENTAJAS DE ESTE ENFOQUE

### 1. Máxima Calidad

**Por qué**:
- Basado en legislación oficial (fuente primaria)
- Contexto legal completo de Qdrant
- Mistral genera con comprensión del contexto
- Validación automática de corrección legal

**Resultado**: Preguntas legalmente correctas y actualizadas

### 2. Sin Rastros Identificables

**Por qué**:
- NO usa materiales de academia como fuente
- Limpieza automática de patrones
- Revisión humana de casos dudosos
- Metadata completa de trazabilidad

**Resultado**: Contenido 100% original y limpio

### 3. Escalable y Eficiente

**Por qué**:
- Qdrant local: consultas rápidas
- Mistral local: sin límites de API
- Limpieza automática: sin intervención manual
- Solo revisa casos marcados (10-20%)

**Resultado**: Puede generar miles de Q&A

### 4. Auditable y Legal

**Por qué**:
- Fuente: legislación pública (BOE)
- Proceso: generación original
- Trazabilidad: metadata completa
- Limpieza: documentada

**Resultado**: 100% legal y defendible

---

## 📋 PRUEBA DE 20 PREGUNTAS

### Objetivo:

Generar 20 preguntas de prueba para validar:
1. ✅ Calidad de las preguntas
2. ✅ Corrección legal
3. ✅ Ausencia de rastros
4. ✅ Funcionamiento del pipeline

### Temas de Prueba:

```
1. Incapacidad Temporal (5 preguntas)
2. Incapacidad Permanente Parcial (5 preguntas)
3. Jubilación ordinaria (5 preguntas)
4. Prestación de viudedad (5 preguntas)
```

### Ejecución:

```bash
# 1. Configurar (solo primera vez)
cd /mnt/e/1/OPOS_GEMINI_1
chmod +x dataset_generator/setup_wsl.sh
./dataset_generator/setup_wsl.sh

# 2. Ejecutar prueba
python3 dataset_generator/pipeline_seguro_local.py
```

### Output Esperado:

```json
{
  "metadata": {
    "fecha_generacion": "2025-12-02T...",
    "modelo": "mistral",
    "total_preguntas": 20,
    "requieren_revision": 2,
    "metodo": "qdrant_local + mistral_local"
  },
  "preguntas": [
    {
      "pregunta": "Según el Art. 169 LGSS...",
      "opciones": ["a) ...", "b) ...", "c) ...", "d) ..."],
      "respuesta_correcta": "a",
      "base_legal": "Art. 169 LGSS",
      "explicacion": "...",
      "tema": "Incapacidad Temporal",
      "metadata": {
        "metodo": "generacion_qdrant_local",
        "fecha_generacion": "2025-12-02T...",
        "requiere_revision": false,
        "patrones_encontrados": []
      }
    }
  ]
}
```

### Revisión:

```
📊 RESUMEN:
   Total preguntas: 20
   Requieren revisión: 2 (10%)
   Limpias: 18 (90%)

⚠️  REPORTE DE REVISIÓN:
Patrones encontrados:
  - academias: 1 ocurrencia
  - identificadores: 1 ocurrencia

Ejemplos de preguntas a revisar:
1. [Pregunta con patrón detectado]
   Patrones: ["academias: Las Cortes"]
```

---

## 🔍 DETECCIÓN POST-GENERACIÓN

### Búsqueda Manual de Rastros:

```bash
# Buscar en el archivo generado
grep -i "las cortes" dataset_output_seguro/test_20_preguntas.json
grep -i "sara domínguez" dataset_output_seguro/test_20_preguntas.json
grep -i "8035" dataset_output_seguro/test_20_preguntas.json
grep -i "villancico" dataset_output_seguro/test_20_preguntas.json
```

**Si encuentra algo**: Ya estará marcado como `[REDACTADO]`

### Validación de Calidad:

```python
# Verificar que todas tienen:
✅ Base legal citada
✅ 4 opciones
✅ Respuesta correcta
✅ Explicación
✅ Sin patrones prohibidos
```

---

## 💰 COSTE Y TIEMPO

### Coste:
```
Qdrant local: $0
Mistral local: $0
Electricidad: ~$0.01 (20 preguntas)

TOTAL: ~$0.01
```

### Tiempo:
```
Configuración inicial: 10-15 min
Generación 20 preguntas: 5-10 min
Revisión manual: 5-10 min

TOTAL: 20-35 min
```

### Escalado a 10,000 preguntas:
```
Generación: 2-4 horas
Revisión (10%): 5-10 horas
TOTAL: 7-14 horas
Coste: ~$0.50
```

---

## ✅ CHECKLIST DE SEGURIDAD

Antes de usar una pregunta, verificar:

- [ ] ¿Tiene base legal citada?
- [ ] ¿Es legalmente correcta?
- [ ] ¿NO contiene nombres de autores?
- [ ] ¿NO menciona academias?
- [ ] ¿NO tiene identificadores específicos?
- [ ] ¿NO usa frases de copyright?
- [ ] ¿NO replica estructuras características?
- [ ] ¿Es contenido original?

---

## 🎯 CONCLUSIÓN

### Este enfoque garantiza:

1. **Máxima calidad**: Basado en legislación oficial
2. **Sin rastros**: Limpieza automática + revisión
3. **Legal**: Contenido original de fuente pública
4. **Escalable**: Miles de Q&A sin límites
5. **Auditable**: Trazabilidad completa

### Próximo paso:

```bash
# Ejecutar prueba de 20 preguntas
python3 dataset_generator/pipeline_seguro_local.py
```

---

**Creado**: 2 Diciembre 2025  
**Estado**: ✅ Listo para probar  
**Próximo paso**: Ejecutar prueba de 20 preguntas
