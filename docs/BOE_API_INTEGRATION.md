# 📘 API BOE - Documentación de Integración

**Fecha:** 5 de diciembre de 2025  
**Estado:** ✅ Implementado y documentado  

---

## 🎯 Resumen

Se ha integrado completamente la **API oficial de datos abiertos del BOE** en el proyecto OpositAIA mediante:

1. ✅ Cliente Python (`backend/agents/boe_api_client.py`)
2. ✅ Router FastAPI (`backend/routers/boe.py`)
3. ✅ Endpoints REST para frontend/agentes

**Documentación oficial BOE:**
- 📘 API Legislación Consolidada: https://www.boe.es/datosabiertos/documentos/APIconsolidada.pdf
- 📘 API Sumarios BOE: https://www.boe.es/datosabiertos/documentos/APIsumarioBOE.pdf
- 🌐 Portal: https://www.boe.es/datosabiertos/api/api.php

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│  Frontend React (puerto 3000)                            │
│  └─ fetch("/api/boe/legislacion/lista")                  │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│  Backend FastAPI (puerto 8000)                           │
│  ├─ routers/boe.py (10 endpoints REST)                   │
│  └─ agents/boe_api_client.py (BOEApiClient)              │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPX
┌───────────────────────▼─────────────────────────────────┐
│  API Oficial BOE (datos abiertos)                        │
│  https://www.boe.es/datosabiertos/api/*                  │
│  ├─ /legislacion-consolidada (lista normas)              │
│  ├─ /legislacion-consolidada/id/{id}/metadatos           │
│  ├─ /legislacion-consolidada/id/{id}/texto               │
│  ├─ /legislacion-consolidada/id/{id}/texto/indice        │
│  └─ /boe/sumario/{fecha} (sumarios diarios)              │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Estructura de Documentos BOE

Según la documentación oficial (páginas 7-18), cada norma consolidada tiene 4 nodos:

```xml
<response>
  <status>
    <code>200</code>
    <text>ok</text>
  </status>
  <data>
    <metadatos>       ✅ Obligatorio [1..1]
    <analisis>        ⚠️  Opcional [0..1]
    <metadata-eli>    ⚠️  Opcional [0..1]
    <texto>           ✅ Obligatorio [1..1]
  </data>
</response>
```

### 1. **Nodo `<metadatos>`** (página 9)

Campos clave:
- `identificador`: ID único (ej: `BOE-A-2015-11724`)
- `titulo`: Nombre de la ley
- `fecha_publicacion`: Formato `YYYYMMDD`
- `fecha_vigencia`: Entrada en vigor
- `vigencia_agotada`: `S`/`N` (si está derogada)
- `estado_consolidacion`: `3` (finalizado) o `4` (en proceso)
- `url_eli`: Permalink European Legislation Identifier
- `url_html_consolidada`: URL en https://www.boe.es

### 2. **Nodo `<analisis>`** (páginas 11-13)

Contiene:
- **`<materias>`**: Temas de la norma (vocabulario controlado)
- **`<notas>`**: Información adicional
- **`<referencias>`**: 
  - `<anteriores>`: Normas que deroga/modifica
  - `<posteriores>`: Normas que la modifican

### 3. **Nodo `<texto>`** (páginas 13-18)

**Estructura jerárquica:**

```
<texto>
  <bloque id="pr" tipo="preambulo" titulo="[preambulo]">
    <version id_norma="BOE-A-2015-11724" fecha_publicacion="20151031">
      <p class="articulo">Artículo 1. Objeto</p>
      <p class="parrafo">La presente Ley...</p>
    </version>
    <version id_norma="BOE-A-2020-12345" fecha_publicacion="20201115">
      <p class="articulo">Artículo 1. Objeto</p>
      <p class="parrafo">La presente Ley (MODIFICADO)...</p>
      <blockquote>
        <p class="nota_pie">Se modifica por Ley 5/2020...</p>
      </blockquote>
    </version>
  </bloque>
  
  <bloque id="a1" tipo="precepto" titulo="Artículo 1">
    ...
  </bloque>
</texto>
```

**Tipos de bloques** (página 13):
- `nota_inicial`: Notas al inicio
- `precepto`: Artículos, disposiciones
- `encabezado`: Títulos, capítulos
- `firma`: Firmas finales
- `parte_dispositiva`: Parte normativa
- `parte_final`: Disposiciones finales
- `preambulo`: Exposición de motivos
- `instrumento`: Instrumentos de ratificación

**Elementos HTML dentro de versiones:**
- `<p class="...">`: Párrafos
- `<table>`: Tablas (HTML estándar)
- `<img>`: Imágenes en base64 (PNG)
- `<blockquote>`: Notas informativas

---

## 🔌 Endpoints Disponibles

### **Legislación Consolidada**

#### 1. Listar legislación
```http
GET /api/boe/legislacion/lista?limit=10&offset=0
```

**Query params:**
- `from_date`: Fecha inicio `YYYYMMDD` (opcional)
- `to_date`: Fecha fin `YYYYMMDD` (opcional)
- `offset`: Primer resultado (default: 0)
- `limit`: Máximo resultados (default: 50, -1 = todos)

**Respuesta:**
```json
{
  "status": {"code": "200", "text": "ok"},
  "data": [
    {
      "identificador": "BOE-A-2015-11724",
      "titulo": "Real Decreto Legislativo 8/2015, de 30 de octubre...",
      "fecha_publicacion": "20151031",
      "vigencia_agotada": "N",
      "url_html_consolidada": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
    }
  ]
}
```

#### 2. Obtener metadatos
```http
GET /api/boe/legislacion/metadatos/BOE-A-2015-11724?formato=json
```

**Query params:**
- `formato`: `json` o `xml` (default: json)

**Respuesta:** Metadatos completos (19 campos)

#### 3. Obtener índice (artículos)
```http
GET /api/boe/legislacion/indice/BOE-A-2015-11724?formato=json
```

**Respuesta:**
```json
{
  "status": {"code": "200", "text": "ok"},
  "data": [
    {
      "id": "pr",
      "titulo": "[preambulo]",
      "fecha_actualizacion": "20151031",
      "url": "https://..."
    },
    {
      "id": "a1",
      "titulo": "Artículo 1",
      "fecha_actualizacion": "20220915",
      "url": "https://..."
    }
  ]
}
```

#### 4. Descargar texto consolidado completo
```http
GET /api/boe/legislacion/texto/BOE-A-2015-11724
```

⚠️ **ADVERTENCIA:** Puede devolver archivos muy grandes (3-10 MB de XML).

**Respuesta:** XML con todas las versiones de todos los artículos.

#### 5. Obtener artículo específico
```http
GET /api/boe/legislacion/bloque/BOE-A-2015-11724/a1
```

**Path params:**
- `id_norma`: BOE-A-2015-11724
- `id_bloque`: `a1`, `a2`, `pr`, `dd`, etc.

**Respuesta:** XML del bloque con todas sus versiones.

---

### **Helpers de Descarga**

#### Descargar LGSS
```http
POST /api/boe/descargar/lgss?guardar_en=/ruta/completa.xml
```

Descarga la **Ley General de la Seguridad Social** consolidada (BOE-A-2015-11724).

#### Descargar Constitución
```http
POST /api/boe/descargar/constitucion?guardar_en=/ruta/completa.xml
```

Descarga la **Constitución Española** (BOE-A-1978-31229).

---

## 🐍 Uso del Cliente Python

### Ejemplo básico

```python
from agents.boe_api_client import BOEApiClient

with BOEApiClient() as client:
    # Listar legislación
    legislacion = client.get_legislacion_consolidada(limit=10)
    
    # Metadatos de la LGSS
    metadatos = client.get_metadatos("BOE-A-2015-11724", formato="json")
    print(f"Título: {metadatos['data']['titulo']}")
    
    # Índice de artículos
    indice = client.get_indice_texto("BOE-A-2015-11724", formato="json")
    for bloque in indice['data']:
        print(f"{bloque['id']}: {bloque['titulo']}")
    
    # Texto consolidado completo
    texto_xml = client.get_texto_consolidado("BOE-A-2015-11724")
    
    # Artículo específico
    articulo_1 = client.get_bloque_texto("BOE-A-2015-11724", "a1")
```

### Métodos disponibles

**Legislación consolidada:**
- `get_legislacion_consolidada(from_date, to_date, query, offset, limit)` → Dict
- `get_documento_consolidado(id_norma)` → Dict (completo: metadatos + análisis + texto)
- `get_metadatos(id_norma, formato)` → Dict
- `get_texto_consolidado(id_norma)` → str (XML completo)
- `get_indice_texto(id_norma, formato)` → Dict
- `get_bloque_texto(id_norma, id_bloque)` → str (XML del bloque)

**Sumarios BOE:**
- `get_sumario(fecha)` → Dict (ej: "20231201")
- `get_documento_boe(id_documento, formato)` → str

**Utilidades:**
- `_parse_xml_response(xml_text)` → Dict
- `_element_to_dict(element)` → Dict

---

## 🚀 Iniciar el Backend

### Opción 1: WSL (Recomendado)

```bash
# Activar entorno virtual
cd /mnt/e/1/OPOS_GEMINI_1/backend
source venv/bin/activate

# Iniciar FastAPI
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Opción 2: Windows PowerShell

```powershell
# Activar entorno virtual
cd E:\1\OPOS_GEMINI_1\backend
.\venv\Scripts\Activate.ps1

# Iniciar FastAPI
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Verificar:**
```bash
curl http://localhost:8000/api/boe/legislacion/lista?limit=2
```

---

## 📊 IDs de Leyes Importantes

| Ley | ID BOE | Descripción |
|-----|--------|-------------|
| **LGSS** | `BOE-A-2015-11724` | Ley General de la Seguridad Social |
| **Constitución** | `BOE-A-1978-31229` | Constitución Española |
| **EBEP** | `BOE-A-2015-11719` | Estatuto Básico del Empleado Público |
| **TRLCSP** | `BOE-A-2011-17887` | Texto Refundido Ley Contratos Sector Público |
| **Ley 39/2015** | `BOE-A-2015-10565` | Procedimiento Administrativo Común |
| **Ley 40/2015** | `BOE-A-2015-10566` | Régimen Jurídico del Sector Público |
| **LO 6/1985** | `BOE-A-1985-12666` | Ley Orgánica del Poder Judicial |
| **LO 2/1979** | `BOE-A-1979-23709` | Ley Orgánica del Tribunal Constitucional |
| **LOREG** | `BOE-A-1985-11672` | Ley Orgánica del Régimen Electoral General |

---

## 🔍 Búsquedas Avanzadas

La API soporta búsquedas con query strings JSON (página 4):

```python
query = {
    "query": {
        "query_string": {
            "query": "titulo:seguridad AND (materia@codigo:6658 OR materia@codigo:4107)"
        },
        "range": {
            "fecha_publicacion": {"gte": "20200101", "lte": "20231231"}
        }
    },
    "sort": [
        {"fecha_publicacion": "desc"},
        {"titulo": "asc"}
    ]
}

legislacion = client.get_legislacion_consolidada(query=query, limit=100)
```

**Campos búsqueda permitidos:**
- `titulo`: Título de la norma
- `texto`: Búsqueda en texto completo
- `materia@codigo`: Código de materia (vocabulario controlado)
- `ambito@codigo`: Estatal (1) / Autonómico
- `departamento@codigo`: Ministerio emisor
- `rango@codigo`: Tipo de norma (Ley, RD, etc.)
- `fecha_disposicion`, `fecha_publicacion`: Fechas
- `numero_oficial`: Número oficial
- `vigencia_agotada`: S/N
- `estado_consolidacion@codigo`: 3 (finalizado) / 4 (en proceso)

---

## 🧪 Testing

### Test básico del cliente

```bash
cd /mnt/e/1/OPOS_GEMINI_1/backend
source venv/bin/activate
python agents/boe_api_client.py
```

**Output esperado:**
```
=== Test API BOE ===

1. Obteniendo lista de legislación consolidada (primeras 5)...
   Lista obtenida: True

2. Descargando metadatos LGSS...
   Metadatos obtenidos: True

3. Obteniendo índice de artículos LGSS...
   Índice obtenido con 1 bloques

4. Descargando texto consolidado LGSS...
   Tamaño XML texto: 3457722 caracteres

=== Tests completados ===

5. Guardando LGSS consolidada en archivo...
   Guardado en: backend/data/leyes/LGSS_consolidada.xml
```

### Test del router FastAPI

```bash
python backend/test_boe_router.py
```

**Output esperado:**
```
✅ BOE router importado correctamente
   - Prefix: /api/boe
   - Tags: ['boe']
   - Endpoints disponibles:
      {'GET'} /api/boe/legislacion/lista
      {'GET'} /api/boe/legislacion/documento/{id_norma}
      ...
```

---

## 🎯 Próximos Pasos

### 1. Modelos de Embeddings - Opciones Evaluadas

Para generar embeddings de legislación española, se evaluaron 3 opciones:

#### 🥇 Opción Recomendada: `pablosi/bge-m3-spa-law-qa-trained-2`

**Características:**
- **Estado:** ✅ Sin restricciones, acceso inmediato
- **Base:** Fine-tuned desde `littlejohn-ai/bge-m3-spa-law-qa`
- **Parámetros:** 567.8M (xlm-roberta)
- **Dataset:** 5,036 pares pregunta-contexto BOE sintéticos
- **Dimensiones:** 1024
- **Licencia:** Apache 2.0
- **Descargas:** 106
- **Enlace:** https://huggingface.co/pablosi/bge-m3-spa-law-qa-trained-2

**Ventajas:**
- ✅ No requiere aceptar términos en HuggingFace
- ✅ Especializado en legislación española (BOE)
- ✅ Hereda conocimiento del modelo original littlejohn-ai
- ✅ Misma arquitectura 1024 dims (compatible)

**Uso:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
embeddings = model.encode([
    "Artículo 1. Objeto de la Ley...",
    "¿Cuál es el plazo de prescripción?"
])
```

#### 🥈 Opción Original: `littlejohn-ai/bge-m3-spa-law-qa`

**Características:**
- **Estado:** ⚠️ Gated repository (requiere aceptar términos)
- **Parámetros:** 567.8M (xlm-roberta)
- **Dataset:** 23,700 pares pregunta-respuesta-contexto legal
- **Dimensiones:** 1024
- **Evaluación:** cosine_accuracy@10 = 0.831
- **Enlace:** https://huggingface.co/littlejohn-ai/bge-m3-spa-law-qa

**Ventajas:**
- ✅ Dataset legal más grande (23.7K vs 5K)
- ✅ Mejor métricas de evaluación documentadas
- ✅ Entrenado con jurisprudencia real

**Desventajas:**
- ❌ Requiere aceptar términos en HF (puede tardar horas/días)
- ❌ Necesita autenticación con token HF_TOKEN

**Uso (requiere autenticación):**
```bash
# Aceptar términos en https://huggingface.co/littlejohn-ai/bge-m3-spa-law-qa
export HF_TOKEN="hf_..."
huggingface-cli login --token $HF_TOKEN
```

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("littlejohn-ai/bge-m3-spa-law-qa")
```

#### 🥉 Opción Fallback: `BAAI/bge-m3`

**Características:**
- **Estado:** ✅ Abierto, sin restricciones
- **Base:** Multilingual general (no especializado en legal)
- **Dimensiones:** 1024
- **Idiomas:** 100+ idiomas incluido español
- **Enlace:** https://huggingface.co/BAAI/bge-m3

**Ventajas:**
- ✅ Acceso inmediato, sin autenticación
- ✅ Muy popular, bien mantenido

**Desventajas:**
- ❌ No especializado en español legal
- ❌ Menor precisión para recuperación de legislación

#### 💡 Opción Investigación: Google Colab Free Tier

**Concepto:** Usar GPUs gratuitas de Google Colab para generar embeddings más rápido.

**Pasos investigados:**
1. Subir modelo a Colab (pablosi o littlejohn-ai)
2. Cargar XMLs de legislación
3. Generar embeddings con GPU Tesla T4 gratis
4. Descargar embeddings para indexar en Qdrant local

**Ventajas:**
- ✅ GPU gratis (más rápido que CPU local)
- ✅ No consume recursos locales
- ✅ Ideal para indexación batch de 17 leyes

**Desventajas:**
- ❌ Requiere upload/download manual de datos
- ❌ Límite de tiempo de ejecución (12h max)
- ❌ No automatizable para updates incrementales

**Estado:** 📋 Pendiente investigar notebook específico en HF de littlejohn-ai

**Referencias:**
- Colab notebook mencionado: https://colab.research.google.com/#fileId=https://huggingface.co/littlejohn-ai/bge-m3-spa-law-qa.ipynb
- Documentación Colab: https://colab.research.google.com/

---

### 2. Indexación en Qdrant - Implementación Actual

Script funcional en `backend/agents/index_lgss_boe_api.py`:

```python
from agents.boe_api_client import BOEApiClient
from agents.rag_agent_v2 import RAGAgentV2
import xml.etree.ElementTree as ET

# MODELO RECOMENDADO (cambiar de BAAI/bge-m3 actual)
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"

# Parsear bloques LGSS
bloques = parsear_bloques_lgss("backend/data/leyes/LGSS_consolidada.xml")  # 567 bloques

# Crear colección Qdrant
rag = RAGAgentV2(
    qdrant_url="http://localhost:6333",
    collection_name="opositaia_lgss",
    embedding_model=EMBEDDING_MODEL,
    use_local_embeddings=True,
    api_key=None  # Local, no cloud
)

# Indexar todos los bloques
for bloque in bloques:
    embedding = rag.generate_embedding(bloque['texto'])
    
    rag.qdrant_client.upsert(
        collection_name="opositaia_lgss",
        points=[{
            "id": bloque['id_bloque'],
            "vector": embedding,
            "payload": {
                "id_bloque": bloque['id_bloque'],
                "titulo": bloque['titulo'],
                "tipo": bloque['tipo'],
                "texto": bloque['texto'],
                "ley": "LGSS",
                "boe_id": "BOE-A-2015-11724"
            }
        }]
    )
```

**Estado actual:**
- ✅ 50 bloques LGSS indexados (prueba)
- 🔄 517 bloques LGSS pendientes
- 📋 16 leyes adicionales por indexar

**Ejecutar:**
```bash
cd /mnt/e/1/OPOS_GEMINI_1/backend
source venv/bin/activate
python agents/index_lgss_boe_api.py
```

### 2. Frontend React

Crear componente para descargar leyes:

```tsx
const DownloadBOELaw = () => {
  const [leyes, setLeyes] = useState([]);
  
  useEffect(() => {
    fetch('/api/boe/legislacion/lista?limit=20')
      .then(res => res.json())
      .then(data => setLeyes(data.data));
  }, []);
  
  const downloadLaw = async (idNorma) => {
    const response = await fetch(`/api/boe/legislacion/texto/${idNorma}`);
    const data = await response.json();
    // Procesar y guardar
  };
  
  return (
    <ul>
      {leyes.map(ley => (
        <li key={ley.identificador}>
          {ley.titulo}
          <button onClick={() => downloadLaw(ley.identificador)}>
            Descargar
          </button>
        </li>
      ))}
    </ul>
  );
};
```

### 3. Actualización Automática

Crear cron job para verificar actualizaciones:

```python
from datetime import datetime, timedelta

# Última sincronización
ultima_sync = "20240101"

# Obtener normas modificadas desde última sync
with BOEApiClient() as client:
    actualizadas = client.get_legislacion_consolidada(
        from_date=ultima_sync,
        limit=-1  # Todas
    )
    
    for norma in actualizadas['data']:
        # Re-indexar en Qdrant
        ...
```

---

## 📚 Referencias

- **Documentación oficial API BOE:** https://www.boe.es/datosabiertos/documentacion.php
- **Especificación OpenAPI 3.1.0:** https://spec.openapis.org/oas/v3.1.0
- **European Legislation Identifier (ELI):** https://eur-lex.europa.eu/eli-register/about.html
- **MEGA_PLAN del proyecto:** `MEGA_PLAN_ACTUALIZADO_COMPLETO.md`
- **Análisis XML vs PDF:** `docs/archive/ANALISIS_XML_BOE_VS_PDF.md`

---

## ✅ Checklist de Implementación

**BOE API Integration:**
- [x] Cliente Python `boe_api_client.py` (354 líneas, 8 métodos)
- [x] Router FastAPI `routers/boe.py` (347 líneas, 10 endpoints)
- [x] 10 endpoints REST documentados
- [x] Integración en `backend/main.py`
- [x] Tests de importación
- [x] Documentación completa (BOE_API_INTEGRATION.md, WSL_POWERSHELL_GUIDE.md)
- [x] Descarga LGSS consolidada (3.4MB XML, 567 bloques)

**RAG y Embeddings:**
- [x] RAGAgentV2 actualizado con `use_local_embeddings` parameter
- [x] Parser XML BOE funcional (`index_lgss_boe_api.py`)
- [x] Evaluación de 3 modelos embedding (pablosi, littlejohn-ai, BAAI)
- [x] Primeros 50 bloques LGSS indexados en Qdrant local
- [ ] Cambiar a modelo `pablosi/bge-m3-spa-law-qa-trained-2` (SIGUIENTE)
- [ ] Indexar 517 bloques LGSS restantes
- [ ] Validar calidad de búsqueda semántica
- [ ] Indexar 16 leyes adicionales

**Frontend y Automatización:**
- [ ] Frontend React para descarga leyes
- [ ] Cron job actualización automática
- [ ] Tests E2E completos
- [ ] Migrar a Qdrant Cloud con UI (decisión pendiente)

**Investigación:**
- [ ] Google Colab notebook para embeddings batch
- [ ] HuggingFace Inference API para embeddings remotos
- [ ] Benchmarks de velocidad CPU vs GPU Colab

---

**Última actualización:** 5 de diciembre de 2025  
**Autor:** AI Assistant + Usuario  
**Versión:** 2.0 - Con opciones de embeddings y estado actual
