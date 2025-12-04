# 🔄 Diagrama de Flujo: Agente Mistral con Qdrant

## 📊 Arquitectura Visual

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO                                   │
│                    (Opositor estudiando)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Pregunta/Consulta
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MISTRAL STUDIO AGENT                           │
│                   (Mistral Large 2)                              │
│                                                                   │
│  System Prompt:                                                  │
│  - Experto en oposiciones SS                                     │
│  - Usa funciones para buscar info                                │
│  - Cita fuentes legales                                          │
│  - Genera preguntas tipo test                                    │
│                                                                   │
│  Configuración:                                                  │
│  - Temperature: 0.3 (preciso)                                    │
│  - Tool Choice: auto                                             │
│  - Parallel Calls: true                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Decide qué función usar
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
┌───────────────────────┐     ┌───────────────────────┐
│   buscar_rag()        │     │   verificar_url()     │
│                       │     │                       │
│ Parámetros:           │     │ Parámetros:           │
│ - query: string       │     │ - url: string         │
│ - top_k: int (1-20)   │     │                       │
└──────────┬────────────┘     └──────────┬────────────┘
           │                             │
           │ Llama a backend             │ Llama a backend
           │                             │
           ▼                             ▼
┌───────────────────────┐     ┌───────────────────────┐
│  BACKEND PYTHON       │     │  URL VERIFIER         │
│  mistral_tools.py     │     │  url_verifier.py      │
│                       │     │                       │
│  - Procesa query      │     │  - Valida URL         │
│  - Genera embedding   │     │  - Hace HTTP request  │
│  - Busca en Qdrant    │     │  - Extrae metadatos   │
└──────────┬────────────┘     └──────────┬────────────┘
           │                             │
           │ Vector search               │ HTTP GET
           │                             │
           ▼                             ▼
┌───────────────────────┐     ┌───────────────────────┐
│   QDRANT CLOUD        │     │   BOE.ES              │
│                       │     │   (Web oficial)       │
│ Collection:           │     │                       │
│ leyes_seguridad_social│     │ - Legislación oficial │
│                       │     │ - Texto consolidado   │
│ Contenido:            │     │ - Metadatos           │
│ - 15,234 chunks       │     └───────────────────────┘
│ - BGE-M3 embeddings   │
│ - Metadata completa   │
│                       │
│ Leyes indexadas:      │
│ ✅ Constitución       │
│ ✅ LGSS (368 arts)    │
│ ✅ LISOS (40 arts)    │
│ ✅ LPRL (54 arts)     │
│ ✅ ET (92 arts)       │
│ ✅ Ley 39/2015        │
│ ✅ Ley 40/2015        │
│ ✅ Reglamentos        │
└──────────┬────────────┘
           │
           │ Devuelve resultados
           │ (texto + metadata + score)
           │
           ▼
┌───────────────────────────────────────────────────────────────┐
│                    BACKEND PYTHON                              │
│                    Procesa resultados                          │
│                                                                 │
│  - Formatea texto legal                                        │
│  - Añade referencias (Ley X, Art. Y)                           │
│  - Calcula relevancia                                          │
│  - Estructura respuesta JSON                                   │
└──────────┬────────────────────────────────────────────────────┘
           │
           │ Devuelve JSON estructurado
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MISTRAL STUDIO AGENT                           │
│                   Procesa tool result                            │
│                                                                   │
│  - Analiza información recibida                                  │
│  - Genera respuesta en lenguaje natural                          │
│  - Aplica formato según system prompt                            │
│  - Cita fuentes correctamente                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Respuesta final
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO                                   │
│                    Recibe respuesta                              │
│                                                                   │
│  Formato:                                                        │
│  - Respuesta clara y precisa                                     │
│  - Referencias legales: [LGSS, Art. 267]                         │
│  - Preguntas tipo test (si se pidió)                             │
│  - Explicaciones detalladas                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Ejemplo: Consulta Legal

### Ejemplo 1: "¿Cuáles son los requisitos para la prestación por desempleo?"

```
1. USUARIO
   └─> Pregunta: "¿Cuáles son los requisitos para la prestación por desempleo?"

2. MISTRAL AGENT
   └─> Analiza pregunta
   └─> Decide: Necesito buscar en la base de datos
   └─> Llama: buscar_rag(query="prestación por desempleo requisitos", top_k=5)

3. BACKEND PYTHON
   └─> Recibe: query="prestación por desempleo requisitos"
   └─> Genera embedding con BGE-M3
   └─> Busca en Qdrant Cloud

4. QDRANT CLOUD
   └─> Búsqueda vectorial en 15,234 chunks
   └─> Encuentra artículos relevantes:
       - LGSS Art. 267 (situación legal de desempleo)
       - LGSS Art. 269 (período de cotización)
       - LGSS Art. 270 (duración)
   └─> Devuelve top 5 resultados con scores

5. BACKEND PYTHON
   └─> Formatea resultados:
       {
         "results": [
           {
             "text": "Artículo 267. Situación legal de desempleo...",
             "metadata": {"ley": "LGSS", "articulo": "267"},
             "score": 0.92
           },
           ...
         ]
       }

6. MISTRAL AGENT
   └─> Recibe información legal
   └─> Genera respuesta estructurada:
   
   "Para acceder a la prestación por desempleo, según la LGSS, se requiere:
   
   1. **Situación legal de desempleo** (Art. 267 LGSS)
   2. **Período mínimo de cotización:** 360 días en los 6 años anteriores (Art. 269 LGSS)
   3. **Inscripción como demandante de empleo**
   4. **No haber cumplido la edad de jubilación**
   5. **Suscribir el compromiso de actividad**
   
   **Fundamento legal:**
   - LGSS, Art. 267: Define la situación legal de desempleo
   - LGSS, Art. 269: Establece el período de cotización mínimo
   - LGSS, Art. 270: Regula la duración de la prestación"

7. USUARIO
   └─> Recibe respuesta completa con referencias legales ✅
```

---

## 🔄 Flujo de Ejemplo: Generar Pregunta de Examen

### Ejemplo 2: "Genera una pregunta tipo test sobre infracciones laborales"

```
1. USUARIO
   └─> Pregunta: "Genera una pregunta tipo test sobre infracciones laborales"

2. MISTRAL AGENT
   └─> Analiza: Necesito información sobre infracciones
   └─> Llama: buscar_rag(query="infracciones laborales LISOS clasificación", top_k=10)

3. BACKEND + QDRANT
   └─> Busca en LISOS
   └─> Devuelve artículos sobre infracciones graves, muy graves, leves

4. MISTRAL AGENT
   └─> Recibe información legal
   └─> Analiza diferentes tipos de infracciones
   └─> Genera pregunta con 4 opciones:
   
   "**Pregunta 1:** Según la LISOS, ¿cuál de las siguientes conductas 
   constituye una infracción muy grave?
   
   A) No comunicar la apertura del centro de trabajo en plazo
   B) No entregar el recibo de salarios en el plazo establecido
   C) Emplear a trabajadores extranjeros sin autorización para trabajar
   D) No informar a los trabajadores sobre los riesgos del puesto
   
   **Respuesta correcta:** C
   
   **Explicación:** El empleo de trabajadores extranjeros sin autorización 
   para trabajar está tipificado como infracción muy grave en el artículo 
   23.1.a) de la LISOS. Las opciones A y B son infracciones leves, y la D 
   es grave.
   
   **Fuente:** LISOS, Art. 23.1.a) - Infracciones muy graves en materia 
   de relaciones laborales"

5. USUARIO
   └─> Recibe pregunta completa tipo test ✅
```

---

## 🔄 Flujo de Ejemplo: Verificar URL

### Ejemplo 3: "¿Es válida esta URL? https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"

```
1. USUARIO
   └─> Pregunta: "¿Es válida esta URL? https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"

2. MISTRAL AGENT
   └─> Detecta URL del BOE
   └─> Llama: verificar_url(url="https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724")

3. BACKEND PYTHON (url_verifier.py)
   └─> Valida formato de URL
   └─> Hace HTTP GET a BOE.es
   └─> Extrae metadatos del HTML

4. BOE.ES
   └─> Responde con página HTML
   └─> Contiene: Título, fecha, estado, contenido

5. BACKEND PYTHON
   └─> Procesa respuesta:
       {
         "valid": true,
         "status_code": 200,
         "title": "Ley General de la Seguridad Social",
         "date": "2015-10-30",
         "active": true
       }

6. MISTRAL AGENT
   └─> Genera respuesta:
   
   "✅ **URL válida y accesible**
   
   Esta URL corresponde a la Ley General de la Seguridad Social 
   (Real Decreto Legislativo 8/2015, de 30 de octubre).
   
   **Información:**
   - Título: Ley General de la Seguridad Social
   - Fecha: 30 de octubre de 2015
   - Estado: Vigente (con modificaciones)"

7. USUARIO
   └─> Recibe confirmación de URL válida ✅
```

---

## 📊 Métricas del Sistema

### Base de Datos Qdrant

```
┌─────────────────────────────────────────┐
│  ESTADÍSTICAS QDRANT CLOUD              │
├─────────────────────────────────────────┤
│  Colección: leyes_seguridad_social      │
│  Total chunks: 15,234                   │
│  Dimensiones: 1024 (BGE-M3)             │
│  Tamaño: ~500 MB                        │
│                                         │
│  Distribución por ley:                  │
│  ├─ LGSS: 5,200 chunks (34%)           │
│  ├─ Ley 39/2015: 2,800 chunks (18%)    │
│  ├─ Ley 40/2015: 1,600 chunks (11%)    │
│  ├─ LPRL: 1,100 chunks (7%)            │
│  ├─ ET: 1,500 chunks (10%)             │
│  ├─ LISOS: 800 chunks (5%)             │
│  ├─ Constitución: 600 chunks (4%)      │
│  └─ Reglamentos: 1,634 chunks (11%)    │
│                                         │
│  Velocidad búsqueda: ~50ms             │
│  Precisión (recall@5): 0.92            │
└─────────────────────────────────────────┘
```

### Materiales Disponibles (No indexados aún)

```
┌─────────────────────────────────────────┐
│  MATERIALES ACADEMIA                    │
├─────────────────────────────────────────┤
│  Ubicación: elemplos_leyes_info/        │
│  Total archivos: 158                    │
│  Tamaño total: 337.69 MB                │
│                                         │
│  Contenido:                             │
│  ├─ Exámenes oficiales 2024            │
│  ├─ Exámenes años anteriores           │
│  ├─ Simulacros completos               │
│  ├─ Temarios actualizados              │
│  ├─ Recopilaciones de preguntas        │
│  └─ Correcciones y explicaciones       │
│                                         │
│  Estado: ⏳ Pendiente de indexar       │
│  Prioridad: Alta                        │
└─────────────────────────────────────────┘
```

---

## 🎯 Casos de Uso Principales

### 1. Estudio de Legislación
```
Usuario → "Explícame el artículo 205 de la LGSS"
         ↓
Agente → buscar_rag("artículo 205 LGSS")
         ↓
Respuesta → Texto completo + explicación + contexto
```

### 2. Preparación de Exámenes
```
Usuario → "Genera 10 preguntas sobre jubilación"
         ↓
Agente → buscar_rag("jubilación") × 10 veces
         ↓
Respuesta → 10 preguntas tipo test con explicaciones
```

### 3. Verificación de Referencias
```
Usuario → "¿Esta URL del BOE es correcta?"
         ↓
Agente → verificar_url(url)
         ↓
Respuesta → Validación + metadatos del documento
```

### 4. Consultas Complejas
```
Usuario → "Compara los requisitos de jubilación ordinaria y anticipada"
         ↓
Agente → buscar_rag("jubilación ordinaria") +
         buscar_rag("jubilación anticipada")
         ↓
Respuesta → Comparación detallada con referencias legales
```

---

## 🔧 Configuración Técnica

### Parámetros Recomendados

```yaml
Modelo:
  name: mistral-large-latest
  temperature: 0.3
  max_tokens: 4096

Tool Choice:
  mode: auto
  parallel_calls: true

Funciones:
  - buscar_rag:
      top_k_default: 5
      top_k_max: 20
  
  - verificar_url:
      timeout: 10s
      retry: 3
```

### Variables de Entorno

```bash
# Mistral
MISTRAL_API_KEY=your_key_here

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_key_here
QDRANT_COLLECTION=leyes_seguridad_social

# BGE-M3 Embeddings
EMBEDDING_MODEL=BAAI/bge-m3
EMBEDDING_DIMS=1024
```

---

## 📈 Roadmap de Mejoras

### Fase 1: Actual ✅
- [x] Agente básico configurado
- [x] Función buscar_rag
- [x] Función verificar_url
- [x] Base de datos con 15K chunks

### Fase 2: Próxima ⏳
- [ ] Indexar materiales de academia (337 MB)
- [ ] Añadir función generar_examen_completo
- [ ] Implementar caché de consultas frecuentes
- [ ] Mejorar reranking de resultados

### Fase 3: Futuro 🔮
- [ ] Fine-tuning del modelo con Q&A generadas
- [ ] Función calcular_prestacion
- [ ] Integración con más fuentes legales
- [ ] Dashboard de métricas y uso

---

**Última actualización:** 4 de diciembre de 2025
**Versión:** 1.0
**Autor:** Sistema OpositAI
