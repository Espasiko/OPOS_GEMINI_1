# 🔍 SPRINT 0: AUDITORÍA DE MATERIAL - CAPA 3 COMPLETA
**Responsable:** AI Assistant  
**Fecha inicio:** 5 de diciembre de 2025  
**Duración:** 1 semana  
**Estado:** 🔴 BLOQUEADOR - Debe completarse antes de empezar cualquier otro sprint

---

## 📋 OBJETIVO PRINCIPAL

Diagnosticar exactamente QUÉ FALTA en Capa 3 (Material de Academias) para identificar:
1. Exámenes oficiales faltantes (BOE, AGE, INSS)
2. Simulacros de oposiciones reales
3. Material de academias incompleto
4. Procesos de indexación necesarios
5. Fuentes confiables para cada tipo de documento

**Resultado esperado:** Documento maestro con lista exacta de todos los archivos a descargar, sus URLs, formatos, y cómo integrarlos en Qdrant.

---

## 📊 ESTADO ACTUAL DE CAPA 3

### Inventario Actual (5 de diciembre 2025)
```
Capa 3: Material Academias
├── Temarios de preparación: 287 documentos
├── Tests/Preguntas: 156 documentos  
├── Casos prácticos: 110 documentos
└── TOTAL: 553 documentos

⚠️ NECESARIO PARA OPOSICIÓN REAL: 5,000+ documentos
⚠️ DÉFICIT: 4,447 documentos (89% de lo necesario)
```

### ❌ FALTANTES CRÍTICOS IDENTIFICADOS

#### 1. **EXÁMENES OFICIALES 2015-2025**
- Seguridad Social (SS)
  - [ ] Convocatoria 2024 (si existe)
  - [ ] Convocatoria 2023 (1ª y 2ª prueba)
  - [ ] Convocatoria 2022 (1ª y 2ª prueba)
  - [ ] Convocatoria 2021 (1ª y 2ª prueba)
  - [ ] Convocatoria 2020 (1ª y 2ª prueba)
  - [ ] Años previos: 2019, 2018, 2017, 2016, 2015

- Administración General del Estado (AGE)
  - [ ] Convocatoria 2024 (si existe)
  - [ ] Convocatoria 2023 (1ª y 2ª prueba)
  - [ ] Convocatoria 2022 (1ª y 2ª prueba)
  - [ ] Convocatoria 2021 (1ª y 2ª prueba)
  - [ ] Convocatoria 2020 (1ª y 2ª prueba)
  - [ ] Años previos: 2019, 2018, 2017, 2016, 2015

#### 2. **SIMULACROS DE ACADEMIAS RECONOCIDAS**
- [ ] Simulacros Centro de Estudios Financieros (CEF)
- [ ] Simulacros Acelera
- [ ] Simulacros Esdiferencial
- [ ] Simulacros Formación IB
- [ ] Simulacros Academia Claustro

#### 3. **CRITERIOS DE CORRECCIÓN OFICIALES**
- [ ] Resoluciones de los exámenes SS 2015-2025
- [ ] Resoluciones de los exámenes AGE 2015-2025
- [ ] Preguntas anuladas y justificación
- [ ] Criterios de puntuación

#### 4. **JURISPRUDENCIA Y DOCTRINA**
- [ ] Resoluciones del INSS (últimas 50)
- [ ] Circulares de la Tesorería General de la SS
- [ ] Sentencias importantes del Tribunal Supremo (últimas 20)
- [ ] Criterios administrativos publicados

---

## 🔗 FUENTES DE DOCUMENTOS

### 1. BOE - Boletín Oficial del Estado
**URL Base:** https://www.boe.es/

#### Exámenes Oficiales:
- **Búsqueda SS:** "convocatoria examen Seguridad Social" + año
- **Búsqueda AGE:** "convocatoria examen Administración General" + año
- **Documentos esperados:** PDFs con preguntas y respuestas

**Última actualización BOE:** [VERIFICAR AUTOMÁTICAMENTE]

### 2. Portal Empleo Público
**URL Base:** https://www.empleopublico.gob.es/

#### Convocatorias de Oposiciones:
- **Ruta:** Sistema de Oposiciones > Historiales
- **Información disponible:**
  - Bases de convocatoria
  - Temarios oficiales
  - Exámenes publicados
  - Listas de aprobados

**Procedimiento:**
1. Buscar por año de convocatoria
2. Descargar PDF con preguntas
3. Descargar PDF de respuestas

### 3. INSS - Instituto Nacional de la Seguridad Social
**URL Base:** https://www.seg-social.es/

#### Resoluciones y Criterios:
- **Resoluciones:** https://www.seg-social.es/wps/portal/wss/internet/cgi-bin/buscador
- **Circulares:** https://www.seg-social.es/wps/portal/wss/internet/prestaciones/
- **Últimas 50 resoluciones:** JSON API disponible

### 4. AGE - Administración General del Estado
**URL Base:** https://www.administracion.gob.es/

#### Bases de Convocatorias:
- **Histórico:** Acceso a todas las convocatorias publicadas
- **Exámenes:** PDFs con preguntas de años anteriores

### 5. CENDOJ - Centro de Documentación Judicial
**URL Base:** http://www.cendoj.poderjudicial.es/

#### Jurisprudencia:
- **API disponible:** Búsqueda de sentencias por:
  - Materia (Seguridad Social)
  - Tribunal (Supremo, Nacional)
  - Fecha
  - Palabra clave

---

## 📝 TAREAS ESPECÍFICAS DEL SPRINT 0

### Tarea 1: Crear `FUENTES_EXAMENES_OFICIALES.md`
**Duración:** 2 horas

**Objetivo:** Documento maestro con URLs exactas y procedimientos

**Contenido:**
```markdown
# 📌 FUENTES DE EXÁMENES OFICIALES SS Y AGE

## Convocatoria SS 2024
- **Bases:** URL exacta
- **Examen 1ª parte:** URL exacta (PDF)
- **Examen 2ª parte:** URL exacta (PDF)
- **Respuestas oficiales:** URL exacta (PDF)
- **Preguntas anuladas:** URL exacta (Especificación)
- **Criterio de puntuación:** URL exacta

## Convocatoria SS 2023
[Mismo formato para cada año]
```

**Entregable:** `docs/FUENTES_EXAMENES_OFICIALES.md` (50+ URLs verificadas)

---

### Tarea 2: Automatizar Descarga de Exámenes
**Duración:** 3 horas

**Script:** `backend/agents/exam_downloader.py`

**Funcionalidad:**
```python
#!/usr/bin/env python3
"""
Descargador automático de exámenes desde múltiples fuentes
"""

def download_from_boe(search_query: str) -> List[bytes]:
    """Descarga PDFs desde BOE usando búsqueda"""
    pass

def download_from_portal_empleo(convocatoria_id: str) -> Dict:
    """Descarga PDFs del Portal de Empleo Público"""
    pass

def verify_pdf_quality(pdf_bytes: bytes) -> bool:
    """Verifica que el PDF es legible y no está corrupto"""
    pass

def cache_locally(filename: str, content: bytes):
    """Cachea en backend/data/exams/"""
    pass
```

**Entregable:** Script funcionando + carpeta `backend/data/exams/` con PDFs descargados

---

### Tarea 3: Mapear Estructura de Exámenes
**Duración:** 2 horas

**Objetivo:** Entender cómo están estructurados los exámenes para chunking inteligente

**Analizar:**
- ¿Cuántos bloques/temas por examen?
- ¿Cuántas preguntas por bloque?
- ¿Qué información incluyen las "respuestas oficiales"?
- ¿Hay preguntas anuladas en forma consistente?

**Script:** `backend/agents/exam_structure_analyzer.py`

**Output:** `ANALISIS_ESTRUCTURA_EXAMENES.json`

```json
{
  "ss_2023": {
    "1a_prueba": {
      "num_preguntas": 100,
      "temas": ["Cotización y afiliación", "Pensiones", ...],
      "duracion_minutos": 120,
      "preguntas_anuladas": 3,
      "estructura": "4 opciones múltiple"
    },
    "2a_prueba": {
      ...
    }
  }
}
```

---

### Tarea 4: Identificar Simulacros de Academias
**Duración:** 3 horas

**Objetivo:** Localizar simulacros de academias reconocidas

**Procedimiento:**
1. Contactar principales academias:
   - CEF (Centro de Estudios Financieros)
   - Acelera
   - Esdiferencial
   - Formación IB
   - Academia Claustro

2. Verificar si tienen exámenes públicos/descargables

3. Solicitar permisos si están bajo copyright

4. Documentar en `SIMULACROS_ACADEMIAS.md`:
```markdown
## CEF - Centro de Estudios Financieros

### Simulacro SS 2024
- URL: https://...
- Acceso: Gratuito / Requiere registro
- Formato: PDF / Online
- Num. preguntas: 100
- Metadata: año, materia, temas cubiertos
```

---

### Tarea 5: Crear Documento Maestro de Integración
**Duración:** 2 horas

**Archivo:** `GUIA_INTEGRACION_CAPA_3.md`

**Contenido:**
```markdown
# 📦 GUÍA DE INTEGRACIÓN - CAPA 3 COMPLETA

## 1. EXÁMENES OFICIALES SS (2015-2025)

### Descargar:
```bash
python backend/agents/exam_downloader.py \
  --source boe \
  --type "examen-seguridad-social" \
  --year 2023 \
  --output backend/data/exams/ss_2023.pdf
```

### Procesar:
```bash
python backend/agents/exam_processor.py \
  --input backend/data/exams/ss_2023.pdf \
  --output backend/data/exams/ss_2023_processed.json \
  --split-by-question \
  --add-metadata
```

### Indexar en Qdrant:
```python
from backend.agents.qdrant_indexer import index_exams

index_exams(
    exam_file="backend/data/exams/ss_2023_processed.json",
    layer=3,
    type="examen_oficial",
    convocatoria="2023-SS-C1"
)
```

## 2. EXÁMENES OFICIALES AGE (2015-2025)
[Mismo procedimiento]

## 3. SIMULACROS DE ACADEMIAS
[Procedimiento similar]

## 4. VERIFICACIÓN FINAL
```bash
# Contar documentos por tipo
python backend/scripts/count_capa3_docs.py

# Resultado esperado:
# Exámenes oficiales: 40+ documentos
# Simulacros: 50+ documentos
# Material de estudio: 553 documentos
# TOTAL: 643+ documentos
```
```

---

## 🎯 RESULTADO ESPERADO DEL SPRINT 0

### Documentos Generados:
- [ ] `FUENTES_EXAMENES_OFICIALES.md` - 50+ URLs verificadas
- [ ] `ANALISIS_ESTRUCTURA_EXAMENES.json` - Mapeo de estructura
- [ ] `SIMULACROS_ACADEMIAS.md` - Listado de simulacros disponibles
- [ ] `GUIA_INTEGRACION_CAPA_3.md` - Procedimientos de integración

### Scripts Desarrollados:
- [ ] `backend/agents/exam_downloader.py` - Descarga automática
- [ ] `backend/agents/exam_processor.py` - Procesa PDFs a JSON
- [ ] `backend/agents/exam_structure_analyzer.py` - Analiza estructura
- [ ] `backend/scripts/count_capa3_docs.py` - Cuenta documentos

### Datos Descargados:
- [ ] Mínimo 10 exámenes oficiales (SS 2020-2023)
- [ ] Mínimo 10 exámenes oficiales (AGE 2020-2023)
- [ ] Acceso a 5+ simulacros de academias
- [ ] Base de datos local con todo descargado

### Bloqueos Identificados:
- [ ] Dependencias de permisos/copyright
- [ ] APIs que requieren autenticación
- [ ] Formatos especiales que necesitan parsers

### Plan Ejecutivo:
- [ ] Timeline claro para Sprint 1 (Indexación)
- [ ] Estimación de tokens/coste
- [ ] Recursos necesarios identificados

---

## ⏱️ TIMELINE DIARIO

**Día 1 (Lunes):** Tareas 1-2
- Crear FUENTES_EXAMENES_OFICIALES.md
- Crear exam_downloader.py básico
- Descargar primeros 5 exámenes

**Día 2 (Martes):** Tarea 3
- Analizar estructura de exámenes
- Crear exam_processor.py
- Procesar exámenes descargados a JSON

**Día 3 (Miércoles):** Tarea 4
- Investigar simulacros de academias
- Crear SIMULACROS_ACADEMIAS.md
- Contactar academias si es necesario

**Día 4 (Jueves):** Tarea 5
- Crear GUIA_INTEGRACION_CAPA_3.md
- Escribir todos los procedimientos
- Crear scripts de verificación

**Día 5 (Viernes):** Cierre
- Testing de todos los scripts
- Verificación de URLs y descargas
- Documentación final

---

## 🚀 SIGUIENTE PASO (Sprint 1)

Una vez completado Sprint 0, iniciar **Sprint 1: Integración de Exámenes Oficiales (1 semana)** con:
- Indexación de todos los exámenes descargados
- Procesamiento de respuestas oficiales
- Creación de índices separados por convocatoria/año
- Testing de búsquedas de exámenes
- Validación de metadatos

---

**Creado:** 5 de diciembre de 2025  
**Última actualización:** [AUTO]  
**Estado:** 🔴 PENDIENTE INICIO
