# Feature Plan: Indexación de Leyes Principales en RAG

**Feature ID**: RAG-indexacion-leyes  
**Created**: 2025-01-18  
**Status**: Planning  
**Priority**: P2 (Alta)

---

## 1. Objetivo

Indexar las leyes principales identificadas por Perplexity y los materiales de ejemplo de las academias en Qdrant para habilitar búsqueda semántica de alta calidad.

---

## 2. Contexto

### Materiales Disponibles

Según `elemplos_leyes_info/ANALISIS_MATERIALES.md`:
- **Temarios**: 2,500+ páginas (6 archivos)
- **Tests**: 600+ páginas (14 archivos)
- **Casos prácticos**: 200+ páginas (12 archivos)
- **Leyes BOE**: ~100 documentos principales

### Leyes Principales (Perplexity)

1. **LGSS** (RDL 8/2015) - Ley General Seguridad Social
2. **Ley 39/2015** - Procedimiento Administrativo
3. **Ley 40/2015** - Régimen Jurídico Sector Público
4. **RDL 5/2015** - EBEP (Estatuto Básico Empleado Público)
5. **RD 1415/2004** - Recaudación SS
6. **RD 84/1996** - Afiliación, altas, bajas
7. **Ley 19/2021** - Ingreso Mínimo Vital
8. **LO 3/2018** - Protección de Datos

### Usuarios Finales

**Opositores** estudiando para Cuerpo Administrativo SS (C1):
- Queries complejas: *"Diferencia entre IT y IP según Art. 169 y 194 LGSS"*
- Necesitan referencias exactas a artículos
- Requieren jurisprudencia actualizada

---

## 3. Arquitectura Técnica

### Stack Decidido

**Embeddings**:
- **Local (desarrollo)**: RoBERTalex o all-minilm
- **Producción**: HuggingFace API (RoBERTalex)
- **Dimensión**: 768 (RoBERTalex) o 384 (all-minilm)

**Vector DB**:
- **Local**: Qdrant en WSL (desarrollo)
- **Producción**: Qdrant Cloud Free Tier (1GB)

**Chunking**:
- **Tamaño**: 512 tokens
- **Overlap**: 50-75 tokens
- **Estrategia**: Respetar estructura de artículos

---

## 4. Plan de Implementación

### Fase 1: Preparación (Día 1)

#### Step 1.1: Configurar Entorno
```bash
# Activar venv
cd backend
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Instalar dependencias
pip install sentence-transformers pypdf qdrant-client python-docx
```

#### Step 1.2: Crear Colección en Qdrant
```python
# backend/setup_qdrant_collection.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")

# Eliminar colección antigua si existe
try:
    client.delete_collection("opositaia_documents")
except:
    pass

# Crear nueva colección
client.create_collection(
    collection_name="opositaia_documents",
    vectors_config=VectorParams(
        size=768,  # RoBERTalex dimension
        distance=Distance.COSINE
    )
)
```

#### Step 1.3: Probar RoBERTalex Local
```bash
cd backend
python test_robertalex_local.py
```

**Decisión**: Basado en resultados, elegir:
- RoBERTalex local (si rápido)
- HuggingFace API (si lento)

---

### Fase 2: Descargar PDFs del BOE (Día 1-2)

#### Step 2.1: Crear Scraper BOE
```python
# backend/agents/boe_scraper.py
import requests
from typing import List, Dict

class BOEScraper:
    BASE_URL = "https://www.boe.es"
    
    LEYES_PRINCIPALES = [
        {
            "nombre": "LGSS",
            "boe_id": "BOE-A-2015-11724",
            "url": "https://www.boe.es/eli/es/rdlg/2015/10/30/8/con"
        },
        {
            "nombre": "Ley 39/2015",
            "boe_id": "BOE-A-2015-10565",
            "url": "https://www.boe.es/eli/es/l/2015/10/01/39/con"
        },
        # ... resto de leyes
    ]
    
    def download_pdf(self, ley: Dict) -> bytes:
        """Descarga PDF consolidado del BOE"""
        response = requests.get(ley["url"] + ".pdf")
        return response.content
    
    def download_all(self) -> List[Dict]:
        """Descarga todas las leyes principales"""
        results = []
        for ley in self.LEYES_PRINCIPALES:
            print(f"Descargando {ley['nombre']}...")
            pdf_content = self.download_pdf(ley)
            results.append({
                "nombre": ley["nombre"],
                "content": pdf_content,
                "metadata": ley
            })
        return results
```

#### Step 2.2: Ejecutar Descarga
```bash
python backend/agents/boe_scraper.py
```

**Output**: PDFs guardados en `backend/data/leyes/`

---

### Fase 3: Procesar y Chunkear (Día 2)

#### Step 3.1: Crear Procesador de PDFs
```python
# backend/agents/pdf_processor.py
from pypdf import PdfReader
from typing import List, Dict
import re

class PDFProcessor:
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def extract_text(self, pdf_path: str) -> str:
        """Extrae texto de PDF"""
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def detect_articles(self, text: str) -> List[Dict]:
        """Detecta artículos en el texto"""
        # Patrón: "Artículo 123." o "Art. 123."
        pattern = r'(Artículo|Art\.)\s+(\d+)'
        matches = list(re.finditer(pattern, text))
        
        articles = []
        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            
            article_num = match.group(2)
            article_text = text[start:end].strip()
            
            articles.append({
                "article_num": article_num,
                "text": article_text,
                "start_pos": start,
                "end_pos": end
            })
        
        return articles
    
    def chunk_by_articles(self, articles: List[Dict]) -> List[Dict]:
        """Crea chunks respetando estructura de artículos"""
        chunks = []
        
        for article in articles:
            text = article["text"]
            
            # Si artículo es corto, chunk completo
            if len(text.split()) < self.chunk_size:
                chunks.append({
                    "text": text,
                    "metadata": {
                        "article": article["article_num"],
                        "type": "article_complete"
                    }
                })
            else:
                # Si artículo es largo, dividir con overlap
                words = text.split()
                for i in range(0, len(words), self.chunk_size - self.overlap):
                    chunk_words = words[i:i + self.chunk_size]
                    chunks.append({
                        "text": " ".join(chunk_words),
                        "metadata": {
                            "article": article["article_num"],
                            "type": "article_part",
                            "part": i // (self.chunk_size - self.overlap) + 1
                        }
                    })
        
        return chunks
```

#### Step 3.2: Procesar Materiales de Academia
```python
# backend/agents/materials_processor.py
class MaterialsProcessor:
    def process_temarios(self, pdf_path: str) -> List[Dict]:
        """Procesa temarios de academia"""
        # Similar a PDFProcessor pero con metadata específica
        pass
    
    def process_tests(self, pdf_path: str) -> List[Dict]:
        """Procesa tests con respuestas"""
        # Extrae preguntas + respuestas + justificaciones
        pass
    
    def process_casos_practicos(self, pdf_path: str) -> List[Dict]:
        """Procesa casos prácticos"""
        # Extrae planteamiento + preguntas + soluciones
        pass
```

---

### Fase 4: Generar Embeddings e Indexar (Día 2-3)

#### Step 4.1: Crear Indexador
```python
# backend/agents/indexer.py
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid

class Indexer:
    def __init__(self, model_name: str = "PlanTL-GOB-ES/roberta-base-bne"):
        self.model = SentenceTransformer(model_name)
        self.client = QdrantClient(url="http://localhost:6333")
        self.collection_name = "opositaia_documents"
    
    def index_chunks(self, chunks: List[Dict], source: str):
        """Indexa chunks en Qdrant"""
        print(f"Generando embeddings para {len(chunks)} chunks...")
        
        # Generar embeddings en batch
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Crear puntos para Qdrant
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "text": chunk["text"],
                    "source": source,
                    "metadata": chunk.get("metadata", {})
                }
            )
            points.append(point)
        
        # Subir a Qdrant en batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i+batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch
            )
            print(f"Indexados {min(i+batch_size, len(points))}/{len(points)}")
        
        print(f"✅ {len(points)} chunks indexados")
```

#### Step 4.2: Script Principal de Indexación
```python
# backend/index_all_materials.py
from agents.boe_scraper import BOEScraper
from agents.pdf_processor import PDFProcessor
from agents.materials_processor import MaterialsProcessor
from agents.indexer import Indexer

def main():
    print("="*60)
    print("🚀 INDEXACIÓN DE MATERIALES")
    print("="*60)
    
    indexer = Indexer()
    processor = PDFProcessor()
    materials_proc = MaterialsProcessor()
    
    # 1. Indexar leyes del BOE
    print("\n📖 Paso 1: Leyes del BOE")
    scraper = BOEScraper()
    leyes = scraper.download_all()
    
    for ley in leyes:
        print(f"\nProcesando {ley['nombre']}...")
        articles = processor.detect_articles(ley['content'])
        chunks = processor.chunk_by_articles(articles)
        indexer.index_chunks(chunks, source=f"BOE_{ley['nombre']}")
    
    # 2. Indexar temarios
    print("\n📚 Paso 2: Temarios de academia")
    temarios = [
        "elemplos_leyes_info/de_mi_hija/SS Temario Unificado - Parte específica (1).pdf",
        # ... más temarios
    ]
    
    for temario_path in temarios:
        print(f"\nProcesando {temario_path}...")
        chunks = materials_proc.process_temarios(temario_path)
        indexer.index_chunks(chunks, source="Temario_Academia")
    
    # 3. Indexar tests
    print("\n📝 Paso 3: Tests con respuestas")
    tests = [
        "elemplos_leyes_info/de_mi_hija/Test_Admtvos_AGE_1contestando.pdf",
        # ... más tests
    ]
    
    for test_path in tests:
        print(f"\nProcesando {test_path}...")
        chunks = materials_proc.process_tests(test_path)
        indexer.index_chunks(chunks, source="Test_Academia")
    
    # 4. Indexar casos prácticos
    print("\n💼 Paso 4: Casos prácticos")
    casos = [
        "elemplos_leyes_info/de_mi_hija/Muestra-Supuestos-Practicos-C1-Administrativo-Seguridad-Social-2024.pdf",
        # ... más casos
    ]
    
    for caso_path in casos:
        print(f"\nProcesando {caso_path}...")
        chunks = materials_proc.process_casos_practicos(caso_path)
        indexer.index_chunks(chunks, source="Caso_Practico")
    
    print("\n" + "="*60)
    print("✅ INDEXACIÓN COMPLETADA")
    print("="*60)
    
    # Estadísticas finales
    collection_info = indexer.client.get_collection(indexer.collection_name)
    print(f"\nTotal puntos indexados: {collection_info.points_count}")

if __name__ == "__main__":
    main()
```

---

### Fase 5: Testing (Día 3)

#### Step 5.1: Crear 100 Queries de Test
```python
# backend/test_queries.py
QUERIES_TEST = [
    # Incapacidad
    "Diferencia entre incapacidad temporal y permanente según LGSS",
    "Requisitos para incapacidad permanente total Art. 194",
    "Duración máxima de la incapacidad temporal",
    
    # Jubilación
    "Edad mínima para jubilación ordinaria 2025",
    "Requisitos jubilación anticipada voluntaria Art. 208",
    "Cálculo de la base reguladora para jubilación",
    
    # Cotización
    "Bases de cotización Régimen General 2025",
    "Diferencia entre base mínima y máxima de cotización",
    "Cuota de solidaridad en cotizaciones",
    
    # Afiliación
    "Situaciones asimiladas al alta en Seguridad Social",
    "Procedimiento de alta en Régimen General",
    "Diferencias entre Régimen General y Especial Autónomos",
    
    # ... 90 queries más
]

def test_rag_quality():
    """Prueba calidad del RAG con 100 queries"""
    from agents.indexer import Indexer
    
    indexer = Indexer()
    results = []
    
    for query in QUERIES_TEST:
        # Buscar en Qdrant
        query_embedding = indexer.model.encode([query])[0]
        search_results = indexer.client.search(
            collection_name=indexer.collection_name,
            query_vector=query_embedding.tolist(),
            limit=5
        )
        
        results.append({
            "query": query,
            "top_result": search_results[0],
            "score": search_results[0].score
        })
    
    # Analizar resultados
    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"Score promedio: {avg_score:.4f}")
    
    # Mostrar mejores y peores
    results.sort(key=lambda x: x["score"], reverse=True)
    print("\n🏆 Top 5 mejores:")
    for r in results[:5]:
        print(f"  {r['score']:.4f} - {r['query']}")
    
    print("\n⚠️  Top 5 peores:")
    for r in results[-5:]:
        print(f"  {r['score']:.4f} - {r['query']}")
```

---

## 5. Estimación de Tamaño

### Cálculo Aproximado

**Leyes BOE** (8 leyes principales):
- ~500 páginas total
- ~1,000 chunks (512 tokens cada uno)
- Embeddings: 1,000 × 768 × 4 bytes = 3 MB

**Temarios** (2,500 páginas):
- ~5,000 chunks
- Embeddings: 5,000 × 768 × 4 bytes = 15 MB

**Tests** (600 páginas):
- ~1,200 chunks
- Embeddings: 1,200 × 768 × 4 bytes = 3.6 MB

**Casos prácticos** (200 páginas):
- ~400 chunks
- Embeddings: 400 × 768 × 4 bytes = 1.2 MB

**TOTAL**: ~7,600 chunks = ~23 MB de vectores + ~10 MB payloads = **~33 MB**

**Conclusión**: ✅ Cabe perfectamente en Qdrant Cloud Free Tier (1GB)

---

## 6. Checklist de Implementación

- [ ] Configurar entorno (venv, dependencias)
- [ ] Crear colección en Qdrant local
- [ ] Probar RoBERTalex local vs HuggingFace
- [ ] Decidir modelo de embeddings
- [ ] Implementar BOE scraper
- [ ] Descargar 8 leyes principales
- [ ] Implementar PDF processor con detección de artículos
- [ ] Implementar materials processor
- [ ] Implementar indexer
- [ ] Indexar leyes BOE
- [ ] Indexar temarios
- [ ] Indexar tests
- [ ] Indexar casos prácticos
- [ ] Crear 100 queries de test
- [ ] Ejecutar testing
- [ ] Analizar resultados
- [ ] Calcular tamaño real
- [ ] Migrar a Qdrant Cloud (si necesario)
- [ ] Actualizar documentación

---

## 7. Documentación a Actualizar

- [ ] `docs/RAG_INTEGRATION_PLAN.md` - Actualizar con implementación real
- [ ] `docs/DECISIONES_CLAVE.md` - Añadir decisión de modelo embeddings
- [ ] `backend/README.md` - Documentar scripts de indexación
- [ ] `ai-specs/changes/RAG-indexacion-leyes-principales.md` - Marcar como completado

---

## 8. Próximos Pasos (Después de P2)

### Prioridad 3: Crear Prompts Basados en Ejemplos Reales

Una vez indexado todo, crear prompts para:
- Generar preguntas tipo test (basado en formato real)
- Generar casos prácticos (basado en ejemplos reales)
- Análisis de respuestas
- Feedback personalizado

### Prioridad 4: Upload de Documentos

- Endpoint FastAPI para subir PDFs
- Procesamiento con Gemini Vision
- Indexación automática

---

**Status**: Ready for Implementation  
**Estimated Time**: 2-3 días  
**Dependencies**: Qdrant local running, Python venv configured

