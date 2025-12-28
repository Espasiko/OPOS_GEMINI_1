# 🎯 ESTRATEGIA FINAL RAG - SISTEMA INTEGRADO COMPLETO

**Fecha:** 26 Diciembre 2025  
**Estado:** ✅ IMPLEMENTADO

---

## ✅ SISTEMA RAG COMPLETO OPERATIVO

### Tamaño Real del Sistema

- **Qdrant:** 125 MB (21,545 puntos)
- **PostgreSQL:** 26 MB (15,043 laws + 27 leyes_catalogo)
- **TOTAL:** 151 MB

### Componentes Implementados

1. ✅ **Tabla `leyes_catalogo`** - 27 leyes con metadata completa
2. ✅ **URLs verificadas** - Consultadas desde API BOE
3. ✅ **Fechas de vigencia** - Disponibles para todas las leyes

**Resultado:** 
- Enriquecimiento falló 2 veces (0 cambios)
- Tiempo perdido: 2+ horas
- Costes innecesarios en APIs

---

## ✅ NUEVA ESTRATEGIA OBLIGATORIA

### REGLA #1: DRY-RUN SIEMPRE

**Antes de ejecutar CUALQUIER script:**

1. **Verificar estructura de datos**
   ```python
   # Ejemplo: Verificar Qdrant
   from qdrant_client import QdrantClient
   client = QdrantClient(url='http://localhost:6333')
   
   result = client.scroll(collection_name='opositaia_knowledge', limit=1)
   point = result[0][0]
   
   print("Payload keys:", list(point.payload.keys()))
   print("Metadata structure:", point.payload.get('metadata'))
   ```

2. **Verificar endpoints**
   ```python
   # Test manual del endpoint
   import requests
   response = requests.post(
       'http://localhost:8000/api/rag/search',
       json={'query': 'test', 'top_k': 1, 'min_score': 0.3}
   )
   print("Status:", response.status_code)
   print("Response structure:", response.json().keys())
   ```

3. **Verificar PostgreSQL**
   ```python
   # Ver estructura de tabla
   cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='laws';")
   print("Columns:", [row[0] for row in cursor.fetchall()])
   ```

4. **Test con 1 item**
   ```python
   # Procesar solo 1 item primero
   test_item = items[0]
   result = process_item(test_item)
   print("Result:", result)
   # SOLO si funciona, procesar todos
   ```

---

### REGLA #2: VERIFICACIÓN DE TOOLS EN LLMs

**Para DeepSeek, Mistral, Groq:**

1. **Verificar qué buscan en RAG**
   - Revisar código de tools (`buscar_rag`, `verificar_articulo`, `verificar_url`)
   - Comprobar qué campos esperan en response
   - Verificar que esos campos existen en Qdrant

2. **Verificar qué buscan en PostgreSQL**
   - ¿Se consulta PostgreSQL?
   - ¿Qué tablas/columnas se usan?
   - ¿Existen esas columnas?

3. **Test manual de cada tool**
   ```python
   # Test buscar_rag
   result = buscar_rag("jubilación anticipada")
   print("Docs found:", len(result))
   print("First doc metadata:", result[0]['metadata'])
   
   # Test verificar_articulo
   result = verificar_articulo("LGSS", "208")
   print("Article found:", result)
   ```

---

### REGLA #3: ESTRUCTURA REAL DE DATOS

**Qdrant `opositaia_knowledge`:**

```json
{
  "layer": "article_chunk",
  "boe_id": "BOE-A-2015-10566",
  "law_name": "Ley 40/2015 - LRJSP",
  "article_id": "chunk_255",
  "text": "...",
  "metadata": {
    "data": {
      "metadatos": {
        "identificador": {"_text": "BOE-A-2015-10566"}
      }
    }
  }
}
```

**Tabla `leyes_catalogo` (NUEVO):**

```sql
SELECT * FROM leyes_catalogo WHERE boe_id = 'BOE-A-2015-10566';
-- Retorna: url_boe, url_eli, fecha_vigor, departamento, tipo_norma, metadata_xml
```

**PostgreSQL `laws` table:**

```sql
id TEXT PRIMARY KEY
law_id TEXT              -- BOE ID
law_name TEXT            -- Nombre ley
title TEXT               -- Título artículo
content TEXT             -- Contenido completo
xml_content TEXT         -- XML original
metadata TEXT            -- Metadatos JSON
created_at TIMESTAMP
```

**RAG Agent V2 Response:**

```json
{
  "documents": [
    {
      "id": "...",
      "score": 0.85,
      "content": "...",
      "metadata": {
        "layer": 1,
        "norma_nombre": "LGSS",
        "articulo": "208",
        "nivel_jerarquia": 1
        // NO tiene campo "url"
      }
    }
  ]
}
```

---

### REGLA #4: CONSTRUCCIÓN DE URLs

**URL BOE se construye desde BOE ID:**

```python
def construir_url_boe(boe_id):
    """
    BOE-A-2015-10566 -> https://www.boe.es/buscar/doc.php?id=BOE-A-2015-10566
    """
    if not boe_id or boe_id == "N/A":
        return None
    return f"https://www.boe.es/buscar/doc.php?id={boe_id}"
```

**BOE ID se extrae de:**
1. Qdrant: `payload.metadata.data.metadatos.identificador._text`
2. PostgreSQL: `law_id` column
3. RAG response: NO disponible directamente (hay que buscarlo en metadata anidado)

---

### REGLA #5: MONITOREO EN VIVO OBLIGATORIO

**Cada script debe:**

1. **Logging en tiempo real**
   ```python
   print(f"Processing item {i}/{total}", flush=True)
   ```

2. **Checkpoints cada 100 items**
   ```python
   if i % 100 == 0:
       print(f"✅ Checkpoint: {stats}", flush=True)
       # Guardar progreso parcial
   ```

3. **Detección de fallos**
   ```python
   if stats['cambios'] == 0 and i > 100:
       print("⚠️ WARNING: 0 cambios después de 100 items")
       print("Deteniendo para revisión...")
       break
   ```

---

## 🔍 CHECKLIST PRE-EJECUCIÓN

**Antes de ejecutar CUALQUIER script de generación/verificación:**

- [ ] **1. Estructura verificada**
  - [ ] Qdrant payload inspeccionado
  - [ ] PostgreSQL schema revisado
  - [ ] RAG endpoint testeado manualmente

- [ ] **2. Tools verificados**
  - [ ] `buscar_rag`: campos que devuelve
  - [ ] `verificar_articulo`: qué busca y dónde
  - [ ] `verificar_url`: cómo construye URL

- [ ] **3. Dry-run completado**
  - [ ] Test con 1 item exitoso
  - [ ] Test con 10 items exitoso
  - [ ] Verificado que produce cambios

- [ ] **4. Monitoreo configurado**
  - [ ] Logging con `flush=True`
  - [ ] Checkpoints cada 100 items
  - [ ] Detección de 0 cambios

- [ ] **5. Rollback preparado**
  - [ ] Backup de datos originales
  - [ ] Script de rollback listo
  - [ ] Timeout configurado

---

## 📊 POSTGRESQL: ¿PARA QUÉ SIRVE?

**Uso actual:**

1. **Almacenamiento de texto completo**
   - Qdrant: solo 1,200 caracteres en payload
   - PostgreSQL: contenido completo sin límite

2. **Metadatos estructurados**
   - XML original de BOE
   - Metadata JSON completo
   - Trazabilidad (created_at)

3. **Consultas NO implementadas actualmente**
   - ❌ RAG no consulta PostgreSQL
   - ❌ Tools no usan PostgreSQL
   - ✅ Solo Qdrant se usa para búsquedas

**Conclusión:** PostgreSQL es backup/storage, NO se usa en búsquedas.

---

## 🚨 SCRIPTS A REVISAR URGENTEMENTE

### 1. DeepSeek - `generate_razonamiento_deepseek_verified.py`

**Verificar:**
- [ ] Tool `buscar_rag`: qué campos espera
- [ ] Tool `verificar_articulo`: cómo busca
- [ ] ¿Usa PostgreSQL? NO
- [ ] ¿Construye URLs correctamente?

### 2. Mistral - `generate_dialogos_mistral_verified.py`

**Verificar:**
- [ ] Tool `buscar_rag`: límite 3 búsquedas/día
- [ ] Tool `verificar_url`: ¿busca en internet o RAG?
- [ ] ¿Por qué falla verificación BOE?
- [ ] ¿Debe usar MCP para RAG local?

### 3. Groq - `generate_simulacros_groq_twopass.py`

**Verificar:**
- [ ] Pass 1: qué busca en RAG
- [ ] Pass 2: cómo verifica artículos
- [ ] ¿Formato correcto de simulacros? (15 preguntas, no 112)

---

## ✅ PRÓXIMOS PASOS

1. **DETENER script actual si falla**
2. **Revisar scripts de generación (DeepSeek, Mistral, Groq)**
3. **Hacer dry-run de cada uno**
4. **Corregir según estructura real**
5. **Ejecutar con monitoreo en vivo**

---

**IMPORTANTE:** Esta estrategia debe ser aprobada y modificada por el usuario antes de continuar.
