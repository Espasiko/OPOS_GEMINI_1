# Estrategias para Qdrant Completo con Trazabilidad (OPOS SS/AGE)

## Problema Base
- 394 leyes × ~500 KB promedio = 197 GB (descarga total)
- Qdrant necesita metadatos + embeddings + búsqueda rápida
- Balance: **tamaño ↔ metadata ↔ velocidad**

---

## OPCIÓN 1: Ingesta Estratificada con Fragmentos (⭐ RECOMENDADO)

### Concepto
Dividir cada ley en **bloques coherentes** (artículos/secciones) con metadatos completos.

### Estructura
```json
{
  "id": "qdrant_uuid",
  "payload": {
    "boe_id": "BOE-A-2015-11430",
    "ley_nombre": "Estatuto de los Trabajadores",
    "capitulo": "Capítulo I - Relación de trabajo",
    "articulo": "Art. 1-5",
    "texto": "[contenido fragmentado]",
    "url_xml": "https://www.boe.es/...",
    "url_boe_directo": "https://www.boe.es/buscar/...",
    "categoria": "laboral",
    "vigencia": "2024-01-01",
    "version_hash": "sha256_del_xml_completo",
    "fuente": "boe.es",
    "indexado_fecha": "2024-12-10"
  },
  "vector": [0.123, 0.456, ...] // embedding del fragmento
}
```

### Ventajas
✅ Fragmentos pequeños (10-50 KB c/u) = búsquedas rápidas  
✅ Metadatos completos en cada punto  
✅ Trazabilidad total (ley → capítulo → artículo → versión)  
✅ Versionado: `version_hash` permite detectar cambios legislativos  

### Tamaño estimado
- 394 leyes × 15 fragmentos promedio = **5,910 documentos**
- ~100 KB por fragmento = **591 MB total en Qdrant** (muy manejable)

### Implementación
```python
# pseudo-código
def ingestar_por_articulos():
    for boe_id in ids_leyes:
        xml = descargar_xml(boe_id)
        articulos = parsear_articulos(xml)  # Div por Art. XX
        
        for art in articulos:
            chunk = {
                "boe_id": boe_id,
                "articulo": art.numero,
                "texto": art.contenido,
                "embedding": modelo.encode(art.contenido),
                "version_hash": hashlib.sha256(xml.encode()).hexdigest()
            }
            qdrant.upsert(chunk)
```

---

## OPCIÓN 2: Two-Tier Storage (Recomendado para Nivel Empresarial)

### Arquitectura
```
┌─ QDRANT (Vector DB)        ┌─ PostgreSQL/MongoDB (Metadata DB)
│  - Embeddings              │  - XML completo
│  - Fragmentos (10 KB c/u)   │  - Historial versiones
│  - Metadatos básicos        │  - Cambios legislativos
│  - 591 MB                   │  - Auditoría
│                             │  - Full-text search
└─────────────────────────────└─────────────────────────
       ↓ (Búsqueda)          ↓ (Recuperación)
     RÁPIDA               COMPLETA + VERIFICABLE
```

### Flujo de Búsqueda
1. Usuario pregunta → **buscar en Qdrant** (embeddings)
2. Top-5 resultados → **enlazar a PostgreSQL** (metadatos completos)
3. Devolver: fragmento + contexto completo + versión + trazabilidad

### Ventajas
✅ Búsqueda rápida (Qdrant)  
✅ Datos completos sin límites de tamaño (PostgreSQL)  
✅ Versionado y auditoría  
✅ Escalable  

### Tamaño estimado
- **Qdrant:** 591 MB (fragmentos + embeddings)
- **PostgreSQL:** ~100 GB (XMLs completos + metadata)
- **Total usado en RAM:** ~2 GB (Qdrant + caché caliente)

---

## OPCIÓN 3: Compresión Inteligente + Snapshot Versionado

### Idea
Comprimir XMLs + mantener snapshots de cambios por fecha.

### Estructura
```
qdrant_storage/
├── collections/
│   ├── opos_ss_age/
│   │   ├── vectors.bin          (embeddings comprimidos)
│   │   ├── payloads.jsonl       (metadatos + referencias)
│   │   └── snapshots/
│   │       ├── 2024-01-01.tar.gz    (snapshot diario)
│   │       ├── 2024-01-02.tar.gz
│   │       └── 2024-12-10.tar.gz
│
└── metadata/
    ├── boe_versions.json        (historial de cambios)
    └── trazabilidad.log         (auditoría)
```

### Ventajas
✅ Recuperación completa por fecha  
✅ Cambios legislativos trazables  
✅ Compresión (tar.gz = ~80% menos espacio)  
✅ Backups automáticos  

### Tamaño con compresión
- Sin compresión: 591 MB
- Con .tar.gz: ~120 MB
- Snapshots diarios (10 días): ~1.2 GB

---

## OPCIÓN 4: Qdrant Sharded + Particionado por Tema

### Concepto
Dividir colecciones por área legal (cada una con sus fragmentos):

```
Qdrant {
  colecciones: {
    "laboral": { 50 leyes, ~750 docs, 75 MB },
    "seguridad_social": { 80 leyes, ~1200 docs, 120 MB },
    "funcion_publica": { 120 leyes, ~1800 docs, 180 MB },
    "justicia": { 60 leyes, ~900 docs, 90 MB },
    "mutualismo": { 84 leyes, ~1260 docs, 126 MB }
  }
}
```

### Ventajas
✅ Búsquedas ultra-rápidas (menos vectores por query)  
✅ Actualizaciones parciales (rápidas)  
✅ Distribución por tema (cognitivo)  
✅ Escalable a múltiples instancias  

### Tamaño total: ~591 MB (igual, pero distribuido)

---

## OPCIÓN 5: Búsqueda Híbrida (Vector + Full-Text)

### Flujo
```
┌─ QDRANT (Búsqueda semántica)
│  "¿Qué límites de edad para jubilación?"
│  → Top-5 resultados similares
│
├─ ELASTICSEARCH (Full-text)
│  "jubilación edad límite"
│  → Resultados exactos rápidos
│
└─ FUSION (Reranking)
   Combinar resultados semánticos + textuales
   Devolver top-3 más relevantes
```

### Ventajas
✅ Búsquedas precisas Y semánticas  
✅ Usuario obtiene respuestas en 100ms  
✅ Trazabilidad total  
✅ Escalable  

### Stack
- Qdrant: 591 MB
- Elasticsearch: ~100 GB (índices full-text)
- Total RAM: ~3-4 GB

---

## OPCIÓN 6: Lazy Loading + Redis Caché

### Idea
Cargar en Qdrant solo las **leyes más consultadas** (80/20 rule):

```python
def estrategia_lazy():
    # TIER 1: Hot (siempre en Qdrant)
    hot_leyes = [
        "TRLET", "TRLGSS", "EBEP", "LOPJ", 
        "Reglamento Afiliación", "Reglamento Cotización"
    ]  # ~6 leyes × 15 docs = 90 docs = ~9 MB
    
    # TIER 2: Warm (en caché Redis)
    warm_leyes = [
        "Leyes de SS especiales", "Normativa AGE", ...
    ]  # ~80 leyes × 15 docs = 1200 docs = ~120 MB (en Redis)
    
    # TIER 3: Cold (bajo demanda desde base de datos)
    cold_leyes = [
        "Normativas muy específicas", "Histórico", ...
    ]  # Acceso disco bajo demanda
```

### Flujo
1. Query llega → **buscar en Qdrant (TIER 1)**
2. Si no hay match → **buscar en Redis (TIER 2)**
3. Si aún no hay → **cargar desde disco (TIER 3)** ← lento pero bajo demanda

### Ventajas
✅ Rapidez para casos comunes  
✅ Flexibilidad para casos raros  
✅ Bajo uso de RAM  
✅ Escalable dinámicamente  

### Consumo
- **RAM:** ~200 MB Qdrant + 200 MB Redis = 400 MB
- **Disco:** 100 GB para tier frío
- **Latencia:** <100ms (hot), <500ms (warm), <2s (cold)

---

## MI RECOMENDACIÓN FINAL (Combinada)

### Stack Híbrido Práctico para OPOS
```
TIER 1: Qdrant + PostgreSQL
├── Qdrant
│   ├── Colección "opos_ss_age" (5,910 docs, 591 MB)
│   ├── Fragmentos por artículo
│   └── Metadatos indexables (boe_id, categoria, vigencia)
│
├── PostgreSQL
│   ├── XMLs completos (100 GB)
│   ├── Historial de cambios
│   ├── Trazabilidad (quién accedió qué, cuándo)
│   └── Versionado por fecha
│
└── Redis (opcional)
    └── Caché de top-100 búsquedas recientes

TIER 2: Snapshots (Backup + Recuperación)
├── Daily snapshot (tar.gz) → ~120 MB
├── Historial de 30 días → ~3.6 GB
└── Comprimido, recuperable por fecha

TIER 3: Elasticsearch (opcional, si quieres full-text)
└── Índice de XMLs completos para búsqueda por keywords exactos
```

### Costo/Beneficio
| Aspecto | Valor |
|---------|-------|
| **RAM usado** | ~2-3 GB |
| **Disco** | ~100 GB |
| **Velocidad búsqueda** | <100ms (promedio) |
| **Trazabilidad** | Completa (auditoría + historial) |
| **Escalabilidad** | Excelente (añadir leyes sin degradar) |
| **Costo infraestructura** | Bajo (1 servidor ~2TB, ~100€/mes) |

---

## Script de Implementación (Opción 1 + 2)

```python
# backend/agents/ingestar_con_trazabilidad.py

import hashlib
import json
from datetime import datetime
from qdrant_client import QdrantClient
from sqlalchemy import create_engine
import xml.etree.ElementTree as ET

class IngestionTracker:
    def __init__(self):
        self.qdrant = QdrantClient("http://localhost:6333")
        self.pg = create_engine("postgresql://user:pass@localhost/opos_db")
    
    def ingestar_ley_con_trazabilidad(self, boe_id, url_xml):
        """Descarga ley, fragmenta por artículo, indexa en Qdrant + PostgreSQL"""
        
        # 1. Descargar XML
        xml_content = descargar_xml(url_xml)
        version_hash = hashlib.sha256(xml_content.encode()).hexdigest()
        
        # 2. Parsear artículos
        root = ET.fromstring(xml_content)
        articulos = parsear_articulos(root)
        
        # 3. Por cada artículo
        for art_num, art_texto in articulos.items():
            chunk_id = f"{boe_id}_{art_num}"
            
            # Embedding
            embedding = modelo_embedding.encode(art_texto)
            
            # Payload con metadatos
            payload = {
                "boe_id": boe_id,
                "version_hash": version_hash,
                "articulo": art_num,
                "categoria": categorizar(boe_id),
                "vigencia": extraer_vigencia(root),
                "url_xml": url_xml,
                "indexado": datetime.now().isoformat(),
                "fuente": "boe.es"
            }
            
            # Insertar en Qdrant
            self.qdrant.upsert(
                collection_name="opos_ss_age",
                points=[{
                    "id": hash(chunk_id),
                    "vector": embedding,
                    "payload": payload
                }]
            )
            
            # Insertar en PostgreSQL (XML completo + metadata)
            with self.pg.connect() as conn:
                conn.execute("""
                    INSERT INTO leyes_fragmentadas 
                    (boe_id, articulo, xml_contenido, version_hash, metadata, indexado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (boe_id, articulo) DO UPDATE SET 
                        xml_contenido=EXCLUDED.xml_contenido,
                        version_hash=EXCLUDED.version_hash,
                        metadata=EXCLUDED.metadata,
                        indexado=EXCLUDED.indexado
                """, (boe_id, art_num, art_texto, version_hash, json.dumps(payload), datetime.now()))
            
            print(f"✅ {boe_id} Art. {art_num} → Qdrant + PostgreSQL")

def buscar_con_trazabilidad(query: str, limit: int = 5):
    """Búsqueda rápida en Qdrant + recuperación completa en PostgreSQL"""
    
    # 1. Buscar en Qdrant (rápido)
    query_embedding = modelo_embedding.encode(query)
    resultados_qdrant = qdrant.search(
        collection_name="opos_ss_age",
        query_vector=query_embedding,
        limit=limit
    )
    
    # 2. Por cada resultado, traer XML completo de PostgreSQL
    resultados_finales = []
    for hit in resultados_qdrant:
        boe_id = hit.payload["boe_id"]
        articulo = hit.payload["articulo"]
        
        # Consultar PostgreSQL para XML completo
        with pg.connect() as conn:
            row = conn.execute("""
                SELECT xml_contenido, metadata, version_hash 
                FROM leyes_fragmentadas 
                WHERE boe_id=%s AND articulo=%s
            """, (boe_id, articulo)).fetchone()
        
        resultados_finales.append({
            "score": hit.score,
            "boe_id": boe_id,
            "articulo": articulo,
            "fragmento": row.xml_contenido[:200] + "...",
            "metadata": json.loads(row.metadata),
            "version_hash": row.version_hash,
            "url_xml": f"https://www.boe.es/diario_boe/xml.php?id={boe_id}",
            "trazabilidad": {
                "indexado": row.metadata.get("indexado"),
                "vigencia": row.metadata.get("vigencia"),
                "fuente": "boe.es"
            }
        })
    
    return resultados_finales
```

---

## Resumen Comparativo

| Opción | Tamaño | Velocidad | Trazabilidad | Complejidad | Recomendación |
|--------|--------|-----------|--------------|-------------|---|
| **1. Fragmentación** | 591 MB | ⚡⚡⚡ | ✅✅✅ | Baja | ⭐ Para empezar |
| **2. Two-Tier** | 591 MB (Qdrant) + 100 GB (PostgreSQL) | ⚡⚡⚡ | ✅✅✅ | Media | ⭐⭐⭐ Production |
| **3. Snapshots** | Variable (120 MB/día) | ⚡⚡ | ✅✅✅ | Baja | Backup |
| **4. Sharded** | 591 MB (distribuido) | ⚡⚡⚡⚡ | ✅✅✅ | Alta | Escala grande |
| **5. Híbrida** | 591 MB + 100 GB | ⚡⚡⚡ | ✅✅✅ | Alta | Solo si necesitas full-text |
| **6. Lazy Loading** | 9 MB (Qdrant hot) + 100 GB (disco) | ⚡⚡⚡ | ✅✅ | Media | Recursos limitados |

---

## Próximos Pasos
1. ✅ Ya tienes el índice (`boe_xml_urls.md`) → **394 referencias listas**
2. ⏳ Implementar Opción 2 (Two-Tier):
   - Crear tabla PostgreSQL: `leyes_fragmentadas(boe_id, articulo, xml_contenido, metadata, version_hash)`
   - Script `ingestar_con_trazabilidad.py` para llenar Qdrant + PostgreSQL
   - API REST: `GET /api/buscar?q=...` que devuelva resultados + trazabilidad
3. ⏳ Dashboard de trazabilidad: versiones por fecha, historial de cambios legislativos
Con la restricción de Qdrant Cloud (1 GB) lo sensato es autohospedar Qdrant + PostgreSQL. Tienes dos opciones sólidas:

Todo en tu VPS (2 vCPU, 8 GB RAM, 100 GB disco, Ubuntu 24.04)
Cabe de sobra para Qdrant (0.6 GB embeddings) + PostgreSQL (100 GB XML + metadatos).
Despliegue rápido con Docker Compose: Qdrant + Postgres + (opcional) pgAdmin.
Abre puertos solo a tu IP (o via túnel SSH) para seguridad.
Haz snapshots de Qdrant y backups de Postgres a tu disco local de 2 TB.
Híbrido: Qdrant en la nube (1 GB) + Postgres en local/VPS
Úsalo solo si quieres mantener el Qdrant Cloud: almacena en la nube solo el “hot set” (TOP leyes), y el resto en un Qdrant local/VPS. Complica la operativa; yo priorizaría la opción 1.
Todo en local (2 TB)
Perfecto para desarrollo; pero si necesitas acceso remoto, tendrás que exponer o tunelar, y no tendrás alta disponibilidad en remoto.
Recomendación
Elige la Opción 1: Qdrant + PostgreSQL en tu VPS (2 vCPU, 8 GB, 100 GB). Es suficiente para el tamaño estimado y evita el límite de 1 GB.

Pasos concisos para la Opción 1 (VPS)
Instalar Docker y Docker Compose en el VPS.
Crear una red Docker y levantar servicios:
Qdrant con almacenamiento en volumen.
PostgreSQL con volumen; usuario/contraseña fuertes; solo puerto interno.
(Opcional) pgAdmin expuesto solo a tu IP.
Seguridad:
En el firewall del VPS: permitir 6333 (Qdrant) y 5432 (Postgres) solo a tu IP; o mejor, acceso por túnel SSH sin abrir puertos.
Claves SSH, fail2ban opcional.
Datos:
Volúmenes en disco del VPS (100 GB). Si se queda corto, respalda periódicamente a tu PC (2 TB) mediante pg_dump + rsync de snapshots de Qdrant.
Ingesta:
Corre el script ingestar_con_trazabilidad.py apuntando a http://qdrant:6333 y Postgres interno.
Fragmenta por artículos (≈6k docs, ~0.6 GB en Qdrant).
Backups:
pg_dump diario/semana → bajar a tu PC.
Snapshot de Qdrant (snapshots API o copia de qdrant_storage) comprimido (tar.gz).
Si prefieres híbrido (cloud + VPS/local)
Mantén en Qdrant Cloud solo 80/20 (hot laws: TRLET, TRLGSS, EBEP, LOPJ, Afiliación, Cotización, IT, etc.) ≈ 9–50 MB.
El resto en Qdrant VPS/local con el mismo esquema de payload; la aplicación consulta primero cloud, luego local.
