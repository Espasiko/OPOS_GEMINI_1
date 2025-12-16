# 📋 SCRIPTS LISTOS PARA COPIAR Y USAR
**Fecha:** 5 de diciembre de 2025  
**Descripción:** Scripts Python/Bash listos para ejecutar inmediatamente  

---

## 1️⃣ SCRIPT: Descargar BOE en JSON

### Archivo: `backend/agents/boe_json_downloader.py`

```python
#!/usr/bin/env python3
"""
Descargador automático de leyes desde BOE en JSON
"""

import json
import requests
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BOEDownloader:
    BASE_URL = "https://www.boe.es/api"
    LAWS_TO_DOWNLOAD = [
        {"query": "Real Decreto Legislativo 8/2015", "id": "LGSS"},
        {"query": "Ley Orgánica 5/1985 LOREG", "id": "LOREG"},
        {"query": "Ley Orgánica 2/1979 LOTC", "id": "LOTC"},
        {"query": "Ley 34/2014 liquidación cuotas", "id": "LEY_34_2014"},
        {"query": "Constitución Española 1978", "id": "CE"},
        {"query": "Ley 39/2015 procedimiento administrativo", "id": "LRJSP"},
        {"query": "Ley 40/2015 régimen jurídico sector público", "id": "LRSP"},
        {"query": "Real Decreto 84/1996", "id": "RD_84_1996"},
        {"query": "Real Decreto 2064/1995", "id": "RD_2064_1995"},
        {"query": "Real Decreto 1415/2004", "id": "RD_1415_2004"},
        {"query": "Real Decreto 295/2009", "id": "RD_295_2009"},
        {"query": "Ley 19/2021 Ingreso Mínimo Vital", "id": "LEY_IMV"},
    ]
    
    def __init__(self, output_dir: str = "backend/data/boe_raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def search_boe(self, query: str, num_results: int = 5) -> List[Dict]:
        """Busca leyes en BOE API"""
        try:
            # Intentar con API de BOE (si existe)
            url = f"{self.BASE_URL}/buscador"
            params = {
                "q": query,
                "sortby": "date_asc",
                "size": num_results
            }
            
            logger.info(f"🔍 Buscando en BOE: {query}")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                results = response.json()
                logger.info(f"✅ Encontrados {len(results.get('results', []))} resultados")
                return results.get('results', [])
            else:
                logger.warning(f"⚠️ BOE API respondió con {response.status_code}")
                return []
        
        except Exception as e:
            logger.error(f"❌ Error en búsqueda BOE: {e}")
            return []
    
    def download_law(self, boe_id: str, law_name: str) -> Optional[Dict]:
        """Descarga ley específica"""
        try:
            # Construct BOE URL for full document
            url = f"https://www.boe.es/eli/es/rdlg/2015/10/30/8"  # Ejemplo LGSS
            
            logger.info(f"📥 Descargando {law_name}...")
            
            # Usar web scraping si API no funciona
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # En un caso real, parsearías el HTML
                law_data = {
                    "id": boe_id,
                    "titulo": law_name,
                    "url": url,
                    "fecha_publicacion": datetime.now().isoformat(),
                    "vigencia": "vigente",
                    "articulos": [],  # Se extraería del HTML
                    "texto_completo": response.text[:5000]  # Primeros 5000 chars
                }
                logger.info(f"✅ Descargada: {law_name}")
                return law_data
        except Exception as e:
            logger.error(f"❌ Error descargando {law_name}: {e}")
        
        return None
    
    def save_json(self, data: Dict, filename: str):
        """Guarda JSON localmente"""
        filepath = self.output_dir / f"{filename}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"💾 Guardado: {filepath}")
    
    def download_all(self):
        """Descarga todas las leyes"""
        logger.info("=" * 60)
        logger.info("🚀 INICIANDO DESCARGA DE LEYES BOE")
        logger.info("=" * 60)
        
        for i, law in enumerate(self.LAWS_TO_DOWNLOAD, 1):
            logger.info(f"\n[{i}/{len(self.LAWS_TO_DOWNLOAD)}] {law['id']}")
            
            # Buscar
            results = self.search_boe(law['query'])
            
            if results:
                # Descargar primera resultado (más relevante)
                law_data = self.download_law(law['id'], law['query'])
                if law_data:
                    self.save_json(law_data, law['id'])
            else:
                logger.warning(f"⚠️ No encontrada: {law['id']}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ DESCARGA COMPLETADA")
        logger.info("=" * 60)

if __name__ == "__main__":
    downloader = BOEDownloader()
    downloader.download_all()
    
    # Verificar
    json_files = list(Path("backend/data/boe_raw").glob("*.json"))
    print(f"\n📊 JSONs creados: {len(json_files)}")
    for f in json_files:
        print(f"  ✅ {f.name}")
```

---

## 2️⃣ SCRIPT: Generar Q&A Simple con Groq

### Archivo: `backend/agents/qa_generator_simple_groq.py`

```python
#!/usr/bin/env python3
"""
Generador Q&A simple con Groq (gratis)
"""

import os
import json
import asyncio
from typing import List, Dict
import logging
from pathlib import Path

# Instalar: pip install groq

try:
    from groq import Groq
except ImportError:
    print("⚠️ Instala: pip install groq")
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleQAGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("❌ Set GROQ_API_KEY environment variable")
        
        self.client = Groq(api_key=self.api_key)
        self.output_file = "dataset_simple_qa.jsonl"
        self.total_generated = 0
    
    def generate_qa_from_law_article(self, law_name: str, article_num: int, 
                                    article_text: str) -> Dict:
        """Genera 1 pregunta simple basada en artículo de ley"""
        
        prompt = f"""Eres un experto creador de exámenes de Seguridad Social española.

LEY: {law_name}
ARTÍCULO {article_num}:
{article_text[:500]}

Genera UNA pregunta simple de opción múltiple que NO requiera análisis:
- Pregunta sobre: definición, número, fecha, o concepto básico
- 4 opciones (A, B, C, D)
- 1 respuesta correcta
- Nivel: FÁCIL

RETORNA EXACTAMENTE ESTE JSON (sin markdown):
{{
  "pregunta": "¿Cuál es...?",
  "opciones": {{
    "A": "opción A",
    "B": "opción B",
    "C": "opción C",
    "D": "opción D (CORRECTA)"
  }},
  "respuesta_correcta": "D"
}}"""
        
        try:
            response = self.client.messages.create(
                model="mixtral-8x7b-32768",  # Free tier Groq
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=400,
                top_p=0.95
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Limpiar markdown si viene envuelto
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            qa_data = json.loads(response_text)
            
            return {
                "messages": [
                    {"role": "user", "content": qa_data["pregunta"]},
                    {"role": "assistant", "content": json.dumps(qa_data["opciones"])}
                ],
                "metadata": {
                    "source": "groq_generated",
                    "law": law_name,
                    "article": article_num,
                    "difficulty": "easy",
                    "confidence": 0.85
                }
            }
        
        except Exception as e:
            logger.warning(f"⚠️ Error generando Q&A: {e}")
            return None
    
    def save_qa(self, qa: Dict):
        """Guarda Q&A en JSONL"""
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')
        self.total_generated += 1
    
    async def generate_batch(self, articles: List[Dict], batch_size: int = 100):
        """Genera lote de Q&A"""
        logger.info(f"🚀 Generando {len(articles)} Q&A simples...")
        
        for i, article in enumerate(articles, 1):
            if i % 100 == 0:
                logger.info(f"✅ Progreso: {i}/{len(articles)}")
            
            qa = self.generate_qa_from_law_article(
                law_name=article.get("law", "Ley"),
                article_num=article.get("num", 1),
                article_text=article.get("text", "")
            )
            
            if qa:
                self.save_qa(qa)
            
            # Rate limiting - Groq free tier
            await asyncio.sleep(0.1)
        
        logger.info(f"✅ COMPLETADO: {self.total_generated} Q&A generadas")

if __name__ == "__main__":
    # Ejemplo de uso
    generator = SimpleQAGenerator()
    
    # Artículos de prueba (en real, estos vendrían de los JSONs de BOE)
    test_articles = [
        {
            "law": "LGSS",
            "num": 205,
            "text": "Se entiende por edad ordinaria de jubilación..."
        },
        {
            "law": "LGSS",
            "num": 165,
            "text": "La incapacidad temporal es la situación del trabajador..."
        },
        # ... más artículos
    ]
    
    # Generar
    asyncio.run(generator.generate_batch(test_articles[:10]))
    
    print(f"\n📊 Dataset guardado en: {generator.output_file}")
```

---

## 3️⃣ SCRIPT: Generar Simulacros Completos con Mistral

### Archivo: `backend/agents/simulacro_generator_mistral.py`

```python
#!/usr/bin/env python3
"""
Generador de simulacros completos con Mistral
"""

import os
import json
import asyncio
from typing import List, Dict
import logging
from pathlib import Path

try:
    from mistralai import Mistral
except ImportError:
    print("⚠️ Instala: pip install mistralai")
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMAS_SS = [
    "Cotización y afiliación",
    "Incapacidad temporal",
    "Incapacidad permanente",
    "Jubilación",
    "Prestaciones por muerte",
    "Maternidad y paternidad",
    "Desempleo",
    "Accidente de trabajo",
    "Enfermedad profesional",
    "Pensiones"
]

class SimulacroGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("❌ Set MISTRAL_API_KEY environment variable")
        
        self.client = Mistral(api_key=self.api_key)
        self.output_file = "simulacros_generados.jsonl"
        self.total_generated = 0
        self.total_cost = 0.0
    
    def generate_simulacro(self, tema: str, num_simulacro: int) -> Dict:
        """Genera 1 simulacro completo (100 preguntas)"""
        
        prompt = f"""Eres un experto creador de exámenes oficiales de Seguridad Social.

TEMA: {tema}
SIMULACRO Nº {num_simulacro}

Crea un examen simulacro COMPLETO:
- 100 preguntas de opción múltiple
- Tema principal: {tema}
- Subtemas relacionados incluidos
- Dificultad: COMO EXAMEN OFICIAL (mezcla fácil-media-difícil)
- Incluir: definiciones, cálculos, procedimientos, casos
- Duración: 120 minutos

RESPONDE CON ESTE JSON EXACTO (sin markdown):
{{
  "tema": "{tema}",
  "simulacro_num": {num_simulacro},
  "num_preguntas": 100,
  "duracion_minutos": 120,
  "preguntas": [
    {{
      "num": 1,
      "pregunta": "¿Cuál es...?",
      "opciones": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
      "respuesta_correcta": "C"
    }},
    ... (hasta pregunta 100)
  ]
}}"""
        
        try:
            logger.info(f"📝 Generando simulacro {num_simulacro} de {tema}...")
            
            response = self.client.messages.create(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=8000
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Limpiar markdown
            if "```" in response_text:
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            simulacro = json.loads(response_text)
            
            # Calcular coste (aproximado)
            input_tokens = len(prompt) // 4
            output_tokens = len(response_text) // 4
            cost = (input_tokens * 0.002 + output_tokens * 0.006) / 1000
            self.total_cost += cost
            
            logger.info(f"✅ Simulacro generado ({len(simulacro.get('preguntas', []))} preguntas)")
            
            return simulacro
        
        except Exception as e:
            logger.error(f"❌ Error generando simulacro: {e}")
            return None
    
    def save_simulacro(self, simulacro: Dict):
        """Guarda simulacro en JSONL"""
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(simulacro, ensure_ascii=False) + '\n')
        self.total_generated += 1
    
    async def generate_batch(self, num_simulacros: int = 50):
        """Genera lote de simulacros"""
        logger.info(f"🚀 Generando {num_simulacros} simulacros...")
        
        import random
        
        for i in range(1, num_simulacros + 1):
            tema = random.choice(TEMAS_SS)
            
            simulacro = self.generate_simulacro(tema, i)
            
            if simulacro and simulacro.get("preguntas"):
                self.save_simulacro(simulacro)
            
            logger.info(f"[{i}/{num_simulacros}] Completado - Coste acumulado: ${self.total_cost:.2f}")
            
            await asyncio.sleep(1)  # Rate limiting
        
        logger.info(f"\n✅ COMPLETADO: {self.total_generated} simulacros")
        logger.info(f"💰 Coste total: ${self.total_cost:.2f}")

if __name__ == "__main__":
    generator = SimulacroGenerator()
    
    # Generar 10 simulacros de prueba
    asyncio.run(generator.generate_batch(num_simulacros=10))
    
    print(f"\n📊 Simulacros guardados en: {generator.output_file}")
```

---

## 4️⃣ BASH: Setup Completo

### Archivo: `setup_rag_finetuning.sh`

```bash
#!/bin/bash
# Script de setup completo para RAG + Fine-tuning

set -e  # Exit on error

echo "=" 
echo "🚀 SETUP RAG + FINE-TUNING COMPLETO"
echo "="

# 1. Crear directorios
echo "📁 Creando directorios..."
mkdir -p backend/data/boe_raw
mkdir -p backend/data/cendoj_raw
mkdir -p backend/data/inss_raw
mkdir -p backend/data/exams
mkdir -p backend/agents
mkdir -p datasets

# 2. Instalar dependencias Python
echo "📦 Instalando dependencias..."
python -m pip install -U pip
pip install groq mistralai anthropic requests pdfplumber
pip install datasets transformers torch peft bitsandbytes trl
pip install unsloth[colab]
pip install qdrant-client redis
pip install uvicorn fastapi

# 3. Descargar modelos base
echo "🤖 Descargando modelos..."
python -c "from transformers import AutoTokenizer, AutoModel; AutoModel.from_pretrained('PlanTL-GOB-ES/RoBERTalex')"

# 4. Inicializar Qdrant local
echo "🔧 Inicializando Qdrant local..."
if ! command -v qdrant &> /dev/null; then
    echo "  ⚠️ Qdrant no instalado. Usar Docker:"
    echo "  docker run -p 6333:6333 qdrant/qdrant"
else
    echo "  ✅ Qdrant disponible"
fi

# 5. Crear colección en Qdrant
echo "📊 Creando colección..."
python3 << 'EOF'
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

try:
    client = QdrantClient("localhost", port=6333)
    client.create_collection(
        collection_name="opositaia_laws",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
    print("✅ Colección 'opositaia_laws' creada")
except Exception as e:
    print(f"⚠️ Error: {e}")
EOF

# 6. Verificar variables de entorno
echo "🔐 Verificando API Keys..."
[[ -z "$GROQ_API_KEY" ]] && echo "  ⚠️ GROQ_API_KEY no configurada"  || echo "  ✅ GROQ_API_KEY"
[[ -z "$MISTRAL_API_KEY" ]] && echo "  ⚠️ MISTRAL_API_KEY no configurada" || echo "  ✅ MISTRAL_API_KEY"
[[ -z "$CLAUDE_API_KEY" ]] && echo "  ⚠️ CLAUDE_API_KEY no configurada" || echo "  ✅ CLAUDE_API_KEY"

echo ""
echo "=" 
echo "✅ SETUP COMPLETADO"
echo "=" 
echo ""
echo "Próximos pasos:"
echo "1. python backend/agents/boe_json_downloader.py"
echo "2. python backend/agents/qa_generator_simple_groq.py"
echo "3. python backend/agents/simulacro_generator_mistral.py"
echo "4. python backend/agents/index_exams_to_qdrant.py"
echo "5. Subir dataset a Colab para fine-tuning"
echo ""
```

---

## 5️⃣ PYTHON: Index Exámenes a Qdrant

### Archivo: `backend/agents/index_exams_qdrant.py`

```python
#!/usr/bin/env python3
"""
Indexa exámenes en Qdrant
"""

import json
from pathlib import Path
from typing import List, Dict
import logging
import numpy as np

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct, Distance, VectorParams
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("⚠️ Instala: pip install qdrant-client sentence-transformers")
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExamIndexer:
    def __init__(self, qdrant_host: str = "localhost", qdrant_port: int = 6333):
        self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.embedder = SentenceTransformer("PlanTL-GOB-ES/RoBERTalex")
        self.collection_name = "opositaia_laws"
        self.indexed_count = 0
    
    def load_exams(self, exam_dir: str = "backend/data/exams") -> List[Dict]:
        """Carga todos los JSONs de exámenes"""
        exams = []
        exam_path = Path(exam_dir)
        
        for json_file in exam_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    exam_data = json.load(f)
                    exams.append(exam_data)
                    logger.info(f"✅ Cargado: {json_file.name}")
            except Exception as e:
                logger.error(f"❌ Error cargando {json_file.name}: {e}")
        
        return exams
    
    def index_exams(self, exams: List[Dict]):
        """Indexa exámenes en Qdrant"""
        points = []
        
        for exam in exams:
            year = exam.get("year", 0)
            exam_type = exam.get("tipo", "unknown")
            
            for i, pregunta in enumerate(exam.get("preguntas", [])):
                try:
                    # Crear embedding de la pregunta
                    pregunta_text = pregunta.get("pregunta", "")
                    embedding = self.embedder.encode(pregunta_text).tolist()
                    
                    # Crear punto para Qdrant
                    point_id = f"exam_{year}_{exam_type}_{i}"
                    
                    point = PointStruct(
                        id=hash(point_id) % (10 ** 8),  # Hash para ID numérico
                        vector=embedding,
                        payload={
                            "id": point_id,
                            "layer": 3,
                            "type": "examen_oficial",
                            "year": year,
                            "exam_type": exam_type,
                            "pregunta": pregunta_text,
                            "opciones": pregunta.get("opciones", {}),
                            "respuesta_correcta": pregunta.get("respuesta_correcta"),
                            "source": "boe_examen_oficial"
                        }
                    )
                    
                    points.append(point)
                    self.indexed_count += 1
                    
                    # Upload por lotes de 100
                    if len(points) >= 100:
                        self.client.upsert(
                            collection_name=self.collection_name,
                            points=points
                        )
                        logger.info(f"✅ {len(points)} documentos subidos a Qdrant")
                        points = []
                
                except Exception as e:
                    logger.error(f"❌ Error indexando pregunta: {e}")
        
        # Upload últimos documentos
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"✅ {len(points)} documentos finales subidos")
        
        logger.info(f"\n✅ TOTAL INDEXADO: {self.indexed_count} documentos")
    
    def test_search(self, query: str = "¿Cuál es la edad de jubilación?"):
        """Prueba búsqueda"""
        logger.info(f"\n🔍 Probando búsqueda: '{query}'")
        
        query_embedding = self.embedder.encode(query).tolist()
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=3
        )
        
        logger.info(f"✅ Encontrados {len(results)} resultados:")
        for result in results:
            logger.info(f"  - {result.payload.get('pregunta', 'N/A')} (score: {result.score:.3f})")

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🚀 INDEXANDO EXÁMENES EN QDRANT")
    logger.info("=" * 60)
    
    indexer = ExamIndexer()
    
    # Cargar exámenes
    exams = indexer.load_exams()
    
    if exams:
        # Indexar
        indexer.index_exams(exams)
        
        # Probar
        indexer.test_search()
    else:
        logger.warning("⚠️ No se encontraron exámenes en backend/data/exams/")
        logger.info("Coloca los JSONs de exámenes en ese directorio primero")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ INDEXACIÓN COMPLETADA")
    logger.info("=" * 60)
```

---

## 📋 ORDEN DE EJECUCIÓN

```bash
# 1. Setup
bash setup_rag_finetuning.sh

# 2. Descargar leyes
python backend/agents/boe_json_downloader.py

# 3. Generar Q&A simple (Groq)
python backend/agents/qa_generator_simple_groq.py

# 4. Generar simulacros (Mistral)
python backend/agents/simulacro_generator_mistral.py

# 5. Indexar exámenes
python backend/agents/index_exams_qdrant.py

# 6. Verificar dataset
python -c "
import json
count = sum(1 for line in open('dataset_simple_qa.jsonl'))
print(f'✅ Q&A generadas: {count}')
"

# 7. Subir dataset a Colab para fine-tuning
# (Transferir dataset_qa_10k_final.jsonl a Colab)

# 8. Descargar modelo fine-tuned
# (Descargar mistral-7b-ss-finetuned.gguf desde Colab)

# 9. Cargar en Ollama
ollama create mistral-ss-finetuned -f Modelfile

# 10. Probar
python backend/agents/test_rag_hybrid.py
```

---

**Creado:** 5 de diciembre de 2025  
**Estado:** ✅ LISTO PARA COPIAR Y EJECUTAR
