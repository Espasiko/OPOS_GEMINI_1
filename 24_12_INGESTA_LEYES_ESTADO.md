# 📊 INGESTA DE LEYES FALTANTES - Estado de Ejecución

**Fecha:** 24 Diciembre 2025 17:50  
**Script:** `backend/agents/ingest_all_missing_laws.py`  
**Estado:** ⏳ EN EJECUCIÓN (background)

---

## ✅ CONFIGURACIÓN VERIFICADA

### Servicios Activos

- ✅ **Backend:** http://localhost:8000 (healthy)
- ✅ **Qdrant:** http://localhost:6333 (2 colecciones)
- ✅ **PostgreSQL:** localhost:5432 (tabla `laws`)
- ✅ **Modelo:** pablosi/bge-m3-spa-law-qa-trained-2 (1024 dims)

### Colecciones Qdrant

1. **`opositaia_knowledge`** - Colección principal
2. **`leyes_espana`** - Colección legacy

---

## 📋 LEYES A INDEXAR (10 totales)

### Prioridad CRÍTICA (3 leyes)

1. **Ley 47/2003** - General Presupuestaria
   - BOE ID: BOE-A-2003-21614
   - Temas: 22-23 AGE

2. **RDL 2/2015** - Estatuto Trabajadores
   - BOE ID: BOE-A-2015-11430
   - Temas: Laborales (Gestión A2)

3. **Ley 31/1995** - Prevención Riesgos Laborales
   - BOE ID: BOE-A-1995-24292
   - Tema: 30 AGE

### Prioridad ALTA (3 leyes)

4. **Ley 9/2017** - LCSP (Contratos Sector Público)
   - BOE ID: BOE-A-2017-12902
   - Tema: 25 AGE

5. **LO 2/2012** - Estabilidad Presupuestaria
   - BOE ID: BOE-A-2012-5730
   - Tema: 23 AGE

6. **Ley 4/2023** - Igualdad Trans LGTBI
   - BOE ID: BOE-A-2023-5366
   - Tema: 17 AGE

### Prioridad MEDIA (4 leyes)

7. **LO 3/2007** - Igualdad
   - BOE ID: BOE-A-2007-6115
   - Tema: 20 AGE

8. **LO 2/1982** - Tribunal de Cuentas
   - BOE ID: BOE-A-1982-11607
   - Tema: 23 AGE

9. **Ley 20/2007** - Estatuto Autónomo
   - BOE ID: BOE-A-2007-15409
   - Complementaria

10. **LO 6/1985** - LOPJ (Poder Judicial)
    - BOE ID: BOE-A-1985-12666
    - Tema: 6 AGE

---

## 🔧 PROCESO DE INDEXACIÓN

### Arquitectura Utilizada

**Modelo de embeddings:**
- `pablosi/bge-m3-spa-law-qa-trained-2`
- 1024 dimensiones
- Especializado en legislación española

**Estrategia de chunking:**
1. **Capa 1 (Document):** Metadatos de la ley completa
2. **Capa 2 (Article Chunks):** Artículos individuales o chunks de 1000 caracteres

**Almacenamiento:**
- **Qdrant:** Vectores + metadata (payload limitado a 1200 chars)
- **PostgreSQL:** Texto completo + metadatos

### Flujo de Procesamiento

Para cada ley:

1. **Fetch BOE API:**
   - Obtener metadatos
   - Descargar XML consolidado

2. **Parse XML:**
   - Buscar tags `<articulo>`
   - Si no hay: fallback a chunks de 1000 chars

3. **Layer 1 (Document):**
   - Guardar en PostgreSQL: `{boe_id}-document`
   - Guardar en Qdrant: embedding del título

4. **Layer 2 (Articles):**
   - Para cada artículo:
     - PostgreSQL: `{boe_id}-{article_id}` con texto completo
     - Qdrant: embedding + payload con metadata
   - Batch upsert cada 50 artículos

---

## ⏱️ TIEMPO ESTIMADO

**Por ley:**
- Fetch BOE API: 5-10 segundos
- Parse XML: 2-5 segundos
- Embeddings: 1-3 segundos por artículo
- Upsert Qdrant: 1-2 segundos por batch

**Total estimado:**
- Ley pequeña (50 artículos): 2-3 minutos
- Ley mediana (200 artículos): 5-8 minutos
- Ley grande (500+ artículos): 10-15 minutos

**Tiempo total para 10 leyes:** 30-60 minutos

---

## 📁 ARCHIVOS GENERADOS

**Script de ingesta:**
- [`backend/agents/ingest_all_missing_laws.py`](file:///home/spas/OPOS_GEMINI_1/backend/agents/ingest_all_missing_laws.py)

**Log de ejecución:**
- `/tmp/ingest_all_laws.log`

**Comando para monitorear:**
```bash
tail -f /tmp/ingest_all_laws.log
```

---

## ✅ VERIFICACIÓN POST-INGESTA

### Comandos de Verificación

**1. Verificar Qdrant:**
```bash
curl -s http://localhost:6333/collections/opositaia_knowledge | python3 -m json.tool
```

**2. Verificar PostgreSQL:**
```bash
cd backend && source ../.venv/bin/activate && python3 -c "
import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.env.backend')
load_dotenv(env_path)

conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5432'),
    database=os.getenv('POSTGRES_DB', 'opositaia'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD')
)
cur = conn.cursor()
cur.execute('SELECT law_id, COUNT(*) FROM laws GROUP BY law_id ORDER BY law_id')
leyes = cur.fetchall()
print('=== LEYES EN POSTGRESQL ===')
for ley, count in leyes:
    print(f'{ley}: {count} chunks')
print(f'\nTOTAL LEYES: {len(leyes)}')
cur.close()
conn.close()
"
```

**3. Test de búsqueda:**
```bash
curl -X POST http://localhost:8000/api/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query":"presupuestos generales del estado","top_k":5}'
```

---

## 🎯 PRÓXIMOS PASOS

### Después de la Ingesta

1. **Verificar indexación:**
   - Confirmar 10 leyes en PostgreSQL
   - Verificar chunks en Qdrant
   - Test de búsqueda RAG

2. **Actualizar documentación:**
   - Marcar leyes como indexadas
   - Actualizar cobertura de temario

3. **Continuar con dataset:**
   - Completar piloto (80 items)
   - Auditar calidad
   - Escalar a 2,500-5,500 items

---

**Estado:** ⏳ Ingesta en ejecución (background)  
**Monitoreo:** `tail -f /tmp/ingest_all_laws.log`  
**Tiempo estimado:** 30-60 minutos
