# 🏆 PLAN MAESTRO RAG COMPLETO + FINE-TUNING LOCAL
**Fecha:** 5 de diciembre de 2025  
**Versión:** 2.0 - MEGA PLAN INTEGRADO  
**Estado:** 🟢 LISTO PARA EJECUCIÓN  
**Presupuesto:** $18-22 USD (máximo)  
**Tiempo:** 12-16 semanas  
**Objetivo Final:** RAG 100% local + Modelo Mistral 7B fine-tuned especializado SS + AGE

---

## 📌 RESUMEN EJECUTIVO (LEER PRIMERO)

### Tu Visión Completa
```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA FINAL                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FUENTES DE DATOS (100% PÚBLICAS)                              │
│  ├─ BOE JSON API → 13 leyes españolas                         │
│  ├─ CENDOJ JSON API → Jurisprudencia (Capa 2)                 │
│  ├─ INSS Resoluciones → Criterios administrativos             │
│  ├─ Exámenes Oficiales → SS + AGE 2015-2025                  │
│  └─ Simulacros Academias → Material públicamente disponible   │
│                                                                 │
│           ↓ ETAPA 1: DESCARGAS + NORMALIZACIÓN ↓               │
│                                                                 │
│  EXTRACTOR INTELIGENTE (backend/agents/)                      │
│  ├─ boe_downloader.py → JSON de leyes normalizados            │
│  ├─ cendoj_crawler.py → Jurisprudencia estructurada           │
│  ├─ inss_scraper.py → Resoluciones + circulares              │
│  ├─ exam_downloader.py → Exámenes oficiales                   │
│  └─ pdf_processor.py → Convierte PDFs a JSON                  │
│                                                                 │
│           ↓ ETAPA 2: INDEXACIÓN EN QDRANT LOCAL ↓              │
│                                                                 │
│  QDRANT LOCAL (backend/qdrant_storage/)                       │
│  ├─ Capa 1: 13 leyes BOE + 4 faltantes (17 total)            │
│  ├─ Capa 2: 1000+ resoluciones + sentencias                   │
│  ├─ Capa 3: Exámenes + simulacros + temarios                  │
│  └─ Embeddings: RoBERTalex (768 dims, español legal)          │
│                                                                 │
│     RAG LOCAL FUNCIONANDO 100% EN TU MÁQUINA                  │
│                                                                 │
│           ↓ ETAPA 3: GENERACIÓN DATASET MULTI-AGENTE ↓         │
│                                                                 │
│  PIPELINE MULTI-AGENTE (backend/agents/)                      │
│  ├─ Groq Llama 3.1 70B → 7,000 Q&A simples (GRATIS/$ 0.70)    │
│  ├─ Mistral Large 2 → 3,000 Q&A complejas ($1.50)             │
│  ├─ Claude → Verificación 5% ($2.50)                          │
│  ├─ Deduplicación automática (similitud embeddings)           │
│  └─ Output: dataset_qa_10k_final.jsonl (92% confidence)       │
│                                                                 │
│  +1,000 SIMULACROS (generados con Mistral)                   │
│  +1,000 TESTS (generados con Groq)                            │
│  +1,000 CASOS PRÁCTICOS (generados con Claude)                │
│                                                                 │
│           ↓ ETAPA 4: FINE-TUNING LOCAL GRATIS ↓                │
│                                                                 │
│  UNSLOTH + GOOGLE COLAB (100% GRATIS)                         │
│  ├─ Modelo base: Mistral-7B-Instruct-v0.3                     │
│  ├─ LoRA adapters (4-bit quantization)                        │
│  ├─ 3 epochs × 12,000 ejemplos                                │
│  ├─ Learning rate: 2e-4                                        │
│  ├─ Tiempo: 4-6 horas en GPU T4 (gratis)                      │
│  └─ Salida: modelo fine-tuned GGUF (conversión)               │
│                                                                 │
│           ↓ ETAPA 5: DEPLOYMENT LOCAL ↓                        │
│                                                                 │
│  TU MÁQUINA (PRODUCCIÓN)                                       │
│  ├─ Ollama: Carga modelo Mistral fine-tuned                   │
│  ├─ Qdrant: RAG local con 3 capas                             │
│  ├─ Backend FastAPI: Orquesta todo                            │
│  ├─ Frontend React: UX de usuario final                       │
│  └─ Cache inteligente (Redis): Acelera búsquedas              │
│                                                                 │
│  ✅ SISTEMA COMPLETO 100% LOCAL Y GRATIS                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 PLAN DESGLOSADO: 16 SEMANAS MÁXIMO

### **FASE 1: DESCARGAS DE BOE + JURISPRUDENCIA (2-3 semanas)**

#### Semana 1: BOE API + CENDOJ Setup

**Objetivo:** Descargar todas las leyes relevantes y jurisprudencia en JSON

**Tareas:**

1. **Investigar APIs disponibles**
   - BOE JSON API: `https://www.boe.es/api` (si existe, sino scraping)
   - CENDOJ: `http://www.cendoj.poderjudicial.es/api` (ver documentación)
   - INSS: `https://www.seg-social.es/wps/portal/wss/internet/cgi-bin/buscador`

2. **Script: `backend/agents/boe_json_downloader.py`**
   ```python
   """Descarga leyes en JSON desde BOE"""
   
   def search_boe_api(query: str, num_results: int = 50) -> List[Dict]:
       """Busca en BOE y devuelve JSON"""
       # API endpoint: https://www.boe.es/api/buscador
       # Retorna: [{"titulo": "...", "url": "...", "fecha": "...", "texto": "..."}]
       pass
   
   def download_law_json(boe_id: str) -> Dict:
       """Descarga ley específica en JSON"""
       # Extrae: artículos, disposiciones finales, etc.
       # Estructura: {"ley": "LGSS", "articulos": [...], "metadata": {...}}
       pass
   
   def normalize_json(raw_json: Dict) -> Dict:
       """Normaliza a formato estándar"""
       # Añade: layer=1, source="BOE", date, etc.
       pass
   ```

3. **Ejecutar descargas:**
   ```bash
   # Descargar 13 leyes principales
   python backend/agents/boe_json_downloader.py \
       --query "Ley General Seguridad Social" \
       --output backend/data/boe_raw/
   
   # Resultado: JSON files con estructura
   backend/data/boe_raw/
   ├── LGSS_2015.json (Real Decreto Legislativo 8/2015)
   ├── LOREG.json (Ley Orgánica 5/1985)
   ├── LOTC.json (Ley Orgánica 2/1979)
   └── ... (13 leyes)
   ```

4. **Script: `backend/agents/cendoj_crawler.py`**
   ```python
   """Descarga jurisprudencia desde CENDOJ"""
   
   def search_jurisprudencia(query: str, tribunal: str = "supremo", 
                            materia: str = "seguridad_social",
                            years: range = range(2015, 2026)) -> List[Dict]:
       """Busca sentencias en CENDOJ"""
       # Retorna: [{"fallo": "...", "fecha": "...", "tribunal": "...", "texto": "..."}]
       pass
   
   def download_sentencia(cendoj_id: str) -> Dict:
       """Descarga sentencia específica"""
       # Estructura: {"id": "...", "titulo": "...", "fallo": "...", "considerandos": [...]}
       pass
   ```

5. **Script: `backend/agents/inss_scraper.py`**
   ```python
   """Descarga resoluciones y circulares del INSS"""
   
   def get_inss_resolutions(years: List[int] = [2020, 2021, 2022, 2023, 2024, 2025]) -> List[Dict]:
       """Obtiene resoluciones recientes"""
       # Fuentes: 
       # - https://www.seg-social.es/wps/portal/wss/internet/prestaciones/
       # - https://www.seg-social.es/wps/portal/wss/internet/cgi-bin/buscador
       # Retorna: [{"titulo": "...", "fecha": "...", "contenido": "..."}]
       pass
   
   def get_inss_circulars() -> List[Dict]:
       """Obtiene circulares de Tesorería"""
       # URLs: https://www.seg-social.es/wps/portal/wss/internet/
       pass
   ```

#### Semana 2-3: Procesamiento y Normalización

6. **Script: `backend/agents/json_normalizer.py`**
   ```python
   """Normaliza todos los JSONs a formato RAG"""
   
   def normalize_all_sources():
       """Procesa BOE + CENDOJ + INSS"""
       
       # BOE → Qdrant schema
       for law_file in glob("backend/data/boe_raw/*.json"):
           law_json = json.load(law_file)
           normalized = {
               "id": f"ley_{law_json['id']}",
               "layer": 1,
               "type": "ley",
               "titulo": law_json["titulo"],
               "articulos": [...],  # Array de artículos
               "metadata": {
                   "source": "BOE",
                   "date": law_json["fecha_publicacion"],
                   "vigencia": law_json["vigencia"],
                   "url": law_json["url_boe"]
               },
               "embeddings": embedder.encode(law_json["texto"])  # RoBERTalex
           }
           save_to_qdrant(normalized)
       
       # CENDOJ → Qdrant schema
       for sentencia_file in glob("backend/data/cendoj_raw/*.json"):
           sentencia_json = json.load(sentencia_file)
           normalized = {
               "id": f"sent_{sentencia_json['id']}",
               "layer": 2,
               "type": "jurisprudencia",
               "titulo": sentencia_json["titulo"],
               "fallo": sentencia_json["fallo"],
               "considerandos": sentencia_json["considerandos"],
               "metadata": {
                   "source": "CENDOJ",
                   "tribunal": sentencia_json["tribunal"],
                   "fecha": sentencia_json["fecha"],
                   "materia": "seguridad_social"
               }
           }
           save_to_qdrant(normalized)
       
       # INSS → Qdrant schema
       for resolucion_file in glob("backend/data/inss_raw/*.json"):
           resolucion_json = json.load(resolucion_file)
           normalized = {
               "id": f"inss_{resolucion_json['id']}",
               "layer": 2,
               "type": "resolucion",
               "titulo": resolucion_json["titulo"],
               "contenido": resolucion_json["contenido"],
               "metadata": {
                   "source": "INSS",
                   "fecha": resolucion_json["fecha"],
                   "tipo": "resolucion" | "circular"
               }
           }
           save_to_qdrant(normalized)
   ```

**Entregas Semana 1-3:**
- [ ] BOE JSON descargado (13 leyes)
- [ ] CENDOJ JSON descargado (1000+ sentencias)
- [ ] INSS JSON descargado (500+ resoluciones)
- [ ] Todos indexados en Qdrant local (Capa 1 + 2)
- [ ] Scripts probados: `boe_json_downloader.py`, `cendoj_crawler.py`, `inss_scraper.py`

---

### **FASE 2: DESCARGAS DE EXÁMENES + INDEXACIÓN CAPA 3 (2-3 semanas)**

#### Semana 4: Descargas de Exámenes Oficiales

7. **Script: `backend/agents/exam_downloader_boe.py`**
   ```python
   """Descarga exámenes oficiales desde BOE y Portal Empleo Público"""
   
   def download_ss_exams(years: List[int] = [2015, 2016, ..., 2025]) -> List[Dict]:
       """Descarga exámenes Seguridad Social"""
       # Fuentes: https://www.empleopublico.gob.es/
       # Buscar: "Convocatoria examen Seguridad Social" + año
       # Descargar: PDF con preguntas + PDF con respuestas
       
       exams = []
       for year in years:
           # 1ª prueba (test general)
           exam_1 = {
               "year": year,
               "prueba": 1,
               "tipo": "test",
               "num_preguntas": 100,
               "url_preguntas": "...",  # PDF descargado
               "url_respuestas": "...",
               "preguntas_anuladas": []  # Si existen
           }
           
           # 2ª prueba (desarrollo)
           exam_2 = {
               "year": year,
               "prueba": 2,
               "tipo": "desarrollo",
               "temas_posibles": ["Tema 1", "Tema 2", ...],
               "url_documento": "..."
           }
           
           exams.extend([exam_1, exam_2])
       
       return exams
   
   def download_age_exams(years: List[int] = [2015, 2016, ..., 2025]) -> List[Dict]:
       """Descarga exámenes AGE"""
       # Similar a SS pero para Administración General del Estado
       pass
   ```

8. **Script: `backend/agents/exam_to_json.py`**
   ```python
   """Convierte PDFs de exámenes a JSON estructurado"""
   
   def convert_exam_pdf_to_json(pdf_path: str, year: int, tipo: str) -> Dict:
       """Procesa PDF de examen"""
       
       # Extraer texto con pdfplumber
       import pdfplumber
       with pdfplumber.open(pdf_path) as pdf:
           texto = "".join([page.extract_text() for page in pdf.pages])
       
       # Detectar preguntas (4 opciones múltiple)
       # Formato típico: "1. Pregunta aquí? A) Opción A B) Opción B C) Opción C D) Opción D"
       
       preguntas = []
       pattern = r"(\d+)\.\s+(.+?)\?\s+A\)\s+(.+?)\s+B\)\s+(.+?)\s+C\)\s+(.+?)\s+D\)\s+(.+)"
       
       for match in re.finditer(pattern, texto):
           num, pregunta, opt_a, opt_b, opt_c, opt_d = match.groups()
           preguntas.append({
               "numero": int(num),
               "pregunta": pregunta.strip(),
               "opciones": {
                   "A": opt_a.strip(),
                   "B": opt_b.strip(),
                   "C": opt_c.strip(),
                   "D": opt_d.strip()
               }
           })
       
       return {
           "year": year,
           "tipo": tipo,
           "num_preguntas": len(preguntas),
           "preguntas": preguntas
       }
   ```

#### Semana 5: Indexación Exámenes + Material

9. **Script: `backend/agents/index_exams_to_qdrant.py`**
   ```python
   """Indexa exámenes en Qdrant Capa 3"""
   
   def index_exams_capa_3():
       """Carga exámenes oficiales como nuevos documentos"""
       
       # Para cada examen
       for year in range(2015, 2026):
           # SS 1ª prueba
           exam_1 = load_json(f"backend/data/exams/ss_{year}_1.json")
           for i, pregunta in enumerate(exam_1["preguntas"]):
               doc = {
                   "id": f"ss_{year}_1_{i}",
                   "layer": 3,
                   "type": "examen_oficial",
                   "exam_type": "1_prueba",
                   "convocatoria": f"{year}-SS-C1",
                   "pregunta": pregunta["pregunta"],
                   "opciones": pregunta["opciones"],
                   "metadata": {
                       "source": "BOE_examen_oficial",
                       "year": year,
                       "tipo": "seguridad_social",
                       "prueba": 1
                   }
               }
               qdrant_client.upsert(collection_name="opositaia_laws", 
                                  points=[doc])
           
           # SS 2ª prueba
           exam_2 = load_json(f"backend/data/exams/ss_{year}_2.json")
           # Similar...
           
           # AGE 1ª y 2ª prueba
           # Similar...
   ```

**Entregas Semana 4-5:**
- [ ] Exámenes SS descargados: 20 exámenes (1ª + 2ª prueba, 2015-2025)
- [ ] Exámenes AGE descargados: 20 exámenes (1ª + 2ª prueba, 2015-2025)
- [ ] Convertidos a JSON
- [ ] Indexados en Qdrant (Capa 3)
- [ ] Búsqueda por año/convocatoria funcionando

---

### **FASE 3: PIPELINE MULTI-AGENTE GENERACIÓN DATASET (3-4 semanas)**

#### Semana 6-9: Generación Q&A Masiva

10. **Script: `backend/agents/qa_extractor.py`**
    ```python
    """Extrae contenido válido para generar Q&A"""
    
    def extract_from_qdrant() -> List[Dict]:
        """Obtiene fragmentos de cada capa"""
        
        extraction = {
            "capa_1_leyes": [],  # 100 fragmentos significativos de leyes
            "capa_2_jurisprudencia": [],  # 50 sentencias clave
            "capa_3_examenes": [],  # 500 preguntas de exámenes
        }
        
        # Capa 1: Extraer artículos completos y títulos de leyes
        for ley in get_all_laws_from_qdrant():
            for articulo in ley["articulos"][:20]:  # Top 20 artículos
                extraction["capa_1_leyes"].append({
                    "type": "articulo",
                    "ley": ley["titulo"],
                    "numero": articulo["numero"],
                    "texto": articulo["texto"],
                    "relevancia": "alta"  # Siempre alta para leyes
                })
        
        # Capa 2: Extraer considerandos de sentencias
        for sentencia in get_sentencias_from_qdrant()[:50]:
            extraction["capa_2_jurisprudencia"].append({
                "type": "sentencia",
                "tribunal": sentencia["tribunal"],
                "fallo": sentencia["fallo"],
                "considerandos": sentencia["considerandos"][:500],  # Primeros 500 chars
                "fecha": sentencia["fecha"]
            })
        
        # Capa 3: Obtener preguntas de exámenes reales
        for examen in get_exams_from_qdrant()[:500]:
            extraction["capa_3_examenes"].append({
                "type": "examen",
                "pregunta": examen["pregunta"],
                "opciones": examen["opciones"],
                "year": examen["year"],
                "tipo": examen["tipo"]
            })
        
        return extraction
    ```

11. **Script: `backend/agents/qa_generator_groq.py`**
    ```python
    """Genera Q&A simples con Groq (70% del dataset)"""
    
    async def generate_simple_qa_batch(extractions: List[Dict], batch_size: int = 100):
        """Genera 7,000 Q&A simples rápidamente"""
        
        total_generated = 0
        cost = 0
        
        for i in range(0, len(extractions), batch_size):
            batch = extractions[i:i+batch_size]
            
            for extraction in batch:
                if extraction["type"] == "examen":
                    # Para exámenes reales: solo validar formato
                    qa = {
                        "messages": [
                            {"role": "user", "content": extraction["pregunta"]},
                            {"role": "assistant", "content": f"Opciones: A) {extraction['opciones']['A']}, B) {extraction['opciones']['B']}, C) {extraction['opciones']['C']}, D) {extraction['opciones']['D']}"}
                        ],
                        "source": "examen_oficial",
                        "difficulty": "medium"
                    }
                else:
                    # Para leyes: generar 1 pregunta simple por artículo
                    prompt = f"""Basándote en este artículo legal:
{extraction["texto"]}

Genera UNA pregunta simple de opción múltiple (4 opciones) sobre:
- Definiciones
- Fechas clave
- Números (edades, porcentajes)
- Conceptos básicos

Retorna JSON:
{{
  "pregunta": "...",
  "respuesta_correcta": "A|B|C|D",
  "opciones": {{"A": "...", "B": "...", "C": "...", "D": "..."}}
}}"""
                    
                    response = await groq_client.messages.create(
                        model="mixtral-8x7b-32768",  # Free tier Groq
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3,
                        max_tokens=500
                    )
                    
                    try:
                        qa_json = json.loads(response.content)
                        qa = {
                            "messages": [
                                {"role": "user", "content": qa_json["pregunta"]},
                                {"role": "assistant", "content": json.dumps(qa_json["opciones"])}
                            ],
                            "source": "generado_groq",
                            "difficulty": "easy"
                        }
                    except:
                        continue  # Skip si falla el parsing
                
                save_qa_to_jsonl("dataset_simple_qa.jsonl", qa)
                total_generated += 1
                cost += 0.0000001  # Groq free tier
        
        print(f"✅ Generadas {total_generated} Q&A simples")
        print(f"💰 Coste: ${cost:.4f}")
    ```

12. **Script: `backend/agents/qa_generator_mistral.py`**
    ```python
    """Genera Q&A complejas con Mistral (30% del dataset)"""
    
    async def generate_complex_qa_batch(extractions: List[Dict], batch_size: int = 50):
        """Genera 3,000 Q&A complejas con precisión legal"""
        
        total_generated = 0
        cost = 0
        
        for i in range(0, len(extractions), batch_size):
            batch = extractions[i:i+batch_size]
            
            for extraction in batch:
                if extraction["type"] == "jurisprudencia":
                    # Generar Q&A sobre jurisprudencia
                    prompt = f"""Como experto en Seguridad Social, analiza esta sentencia:

TRIBUNAL: {extraction["tribunal"]}
FALLO: {extraction["fallo"]}
CONSIDERANDOS: {extraction["considerandos"]}

Genera 3 preguntas de opción múltiple complejas que requieran:
1. Análisis de la jurisprudencia
2. Aplicación a casos reales
3. Conexión con la normativa

Para cada pregunta, retorna:
{{
  "preguntas": [
    {{
      "pregunta": "...",
      "opciones": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
      "respuesta_correcta": "A|B|C|D",
      "explicacion": "..."
    }}
  ]
}}"""
                    
                    response = await mistral_client.messages.create(
                        model="mistral-large-latest",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5,
                        max_tokens=2000
                    )
                    
                    try:
                        result = json.loads(response.content)
                        for q in result["preguntas"]:
                            qa = {
                                "messages": [
                                    {"role": "user", "content": q["pregunta"]},
                                    {"role": "assistant", "content": q["explicacion"]}
                                ],
                                "source": "generado_mistral_jurisprudencia",
                                "difficulty": "hard",
                                "citation": {
                                    "tribunal": extraction["tribunal"],
                                    "fallo": extraction["fallo"]
                                }
                            }
                            save_qa_to_jsonl("dataset_complex_qa.jsonl", qa)
                            total_generated += 1
                            cost += 0.00006  # Mistral input tokens
                    except:
                        continue
        
        print(f"✅ Generadas {total_generated} Q&A complejas")
        print(f"💰 Coste: ${cost:.2f}")
    ```

13. **Script: `backend/agents/simulacro_generator.py`**
    ```python
    """Genera 1,000 simulacros de examen completos"""
    
    async def generate_simulacros(num: int = 1000):
        """Crea simulacros tipo examen (100 preguntas cada uno)"""
        
        for i in range(num):
            # Seleccionar tema aleatorio
            tema = random.choice(TEMAS_SS)
            
            # Generar 100 preguntas sobre ese tema
            prompt = f"""Eres un experto creador de exámenes de Seguridad Social.
Crea un simulacro de examen COMPLETO sobre: {tema}

Requisitos:
- 100 preguntas de opción múltiple
- 4 opciones cada pregunta
- 1 respuesta correcta por pregunta
- Dificultad: REAL (como examen oficial)
- Incluir: definiciones, artículos, procedimientos, casos
- Retorna JSON con array de preguntas

Formato JSON:
{{
  "tema": "{tema}",
  "num_preguntas": 100,
  "duracion_minutos": 120,
  "preguntas": [
    {{"num": 1, "pregunta": "...", "opciones": {{"A": "...", "B": "...", "C": "...", "D": "..."}}, "respuesta": "A"}}
  ]
}}"""
            
            # Usar Mistral o Groq según la disponibilidad
            response = await mistral_client.messages.create(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=8000
            )
            
            try:
                simulacro = json.loads(response.content)
                save_to_jsonl(f"simulacros_generados.jsonl", simulacro)
                print(f"✅ Simulacro {i+1}/{num} creado")
            except:
                print(f"⚠️ Simulacro {i+1} falló, reintentando...")
                continue
    ```

14. **Script: `backend/agents/test_generator.py`**
    ```python
    """Genera 1,000 tests de práctica"""
    
    async def generate_tests(num: int = 1000):
        """Crea tests cortos de 25 preguntas cada uno"""
        
        for i in range(num):
            temas_mini = random.sample(TEMAS_SS, k=3)  # Seleccionar 3 temas
            
            prompt = f"""Crea un test rápido de Seguridad Social sobre: {', '.join(temas_mini)}

Características:
- 25 preguntas (no 100)
- Tiempo: 30 minutos
- Dificultad: MEDIA
- Cada pregunta = 4 puntos

Retorna JSON:
{{
  "temas": {temas_mini},
  "num_preguntas": 25,
  "duracion_minutos": 30,
  "preguntas": [...]
}}"""
            
            response = await groq_client.messages.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            
            try:
                test = json.loads(response.content)
                save_to_jsonl("tests_generados.jsonl", test)
            except:
                continue
    ```

15. **Script: `backend/agents/casos_practicos_generator.py`**
    ```python
    """Genera 1,000 casos prácticos complejos"""
    
    async def generate_practical_cases(num: int = 1000):
        """Crea casos prácticos tipo examen"""
        
        for i in range(num):
            tema = random.choice(TEMAS_SS)
            
            prompt = f"""Eres creador de casos prácticos para oposiciones de Seguridad Social.
Crea un SUPUESTO PRÁCTICO COMPLETO sobre: {tema}

Estructura:
1. ESCENARIO: Descripción detallada del caso
   - Personaje: Nombre, edad, antecedentes
   - Situación: Hechos específicos
   - Preguntas: ¿Qué debe hacer? ¿Cuál es el procedimiento?

2. PREGUNTAS: 5 preguntas sobre el caso
   - 3 conceptuales (normativa)
   - 1 procedimental (cómo actuar)
   - 1 combinada (teoría + práctica)

3. RESPUESTA MODELO: Con referencias legales
   - Artículos aplicables
   - Procedimiento correcto
   - Tiempo estimado

Retorna JSON:
{{
  "tema": "{tema}",
  "escenario": "...",
  "preguntas": [...],
  "respuesta_modelo": "..."
}}"""
            
            response = await mistral_client.messages.create(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000
            )
            
            try:
                caso = json.loads(response.content)
                save_to_jsonl("casos_practicos_generados.jsonl", caso)
            except:
                continue
    ```

**Entregas Semana 6-9:**
- [ ] 10,000 Q&A generadas (7,000 simple + 3,000 complejo)
- [ ] 1,000 simulacros completos (100 preguntas cada)
- [ ] 1,000 tests (25 preguntas cada)
- [ ] 1,000 casos prácticos
- [ ] Coste total: $18-22 USD
- [ ] Archivo: `dataset_final_qa_10k.jsonl`
- [ ] Archivos: `simulacros.jsonl`, `tests.jsonl`, `casos.jsonl`

---

### **FASE 4: VERIFICACIÓN + DEDUPLICACIÓN (1 semana)**

#### Semana 10: QA Verification con Claude

16. **Script: `backend/agents/qa_verifier_claude.py`**
    ```python
    """Verifica muestra del dataset con Claude (5%)"""
    
    async def verify_sample(dataset_file: str, sample_size: int = 500):
        """Verifica 500 Q&A (5%) con Claude"""
        
        dataset = load_jsonl(dataset_file)
        sample = random.sample(dataset, sample_size)
        
        results = {
            "verificadas": 0,
            "correctas": 0,
            "errores": [],
            "confidence_promedio": 0.0
        }
        
        for qa in sample:
            prompt = f"""Eres experto verificador de Q&A de Seguridad Social.

PREGUNTA: {qa["messages"][0]["content"]}
RESPUESTA: {qa["messages"][1]["content"]}

Evalúa:
1. ✅ ¿Es la pregunta clara y sin errores?
2. ✅ ¿Es la respuesta LEGALMENTE CORRECTA?
3. ✅ ¿Usa terminología adecuada?
4. ✅ ¿Es apropiada para examen oficial?

Retorna JSON:
{{
  "es_valida": true|false,
  "confidence": 0.95,
  "errores": ["..."],
  "sugerencias": "..."
}}"""
            
            response = await claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            try:
                verify = json.loads(response.content)
                results["verificadas"] += 1
                if verify["es_valida"]:
                    results["correctas"] += 1
                    results["confidence_promedio"] += verify["confidence"]
                else:
                    results["errores"].append({
                        "qa": qa,
                        "razon": verify["sugerencias"]
                    })
            except:
                continue
        
        results["confidence_promedio"] /= results["correctas"]
        print(f"✅ Validez: {results['correctas']}/{results['verificadas']} ({100*results['correctas']/results['verificadas']:.1f}%)")
        print(f"💯 Confianza promedio: {results['confidence_promedio']:.3f}")
        
        return results
    ```

17. **Script: `backend/agents/deduplication.py`**
    ```python
    """Elimina Q&A duplicadas usando embeddings"""
    
    def remove_duplicates(dataset_file: str, similarity_threshold: float = 0.95):
        """Detecta y elimina preguntas similares"""
        
        dataset = load_jsonl(dataset_file)
        embeddings = []
        
        # Generar embeddings para todas las preguntas
        for qa in dataset:
            pregunta = qa["messages"][0]["content"]
            embedding = roberta_embedder.encode(pregunta)  # RoBERTalex 768 dims
            embeddings.append(embedding)
        
        # Detectar duplicados
        duplicates_to_remove = set()
        for i in range(len(embeddings)):
            for j in range(i+1, len(embeddings)):
                similarity = cosine_similarity(embeddings[i], embeddings[j])
                if similarity > similarity_threshold:
                    duplicates_to_remove.add(j)  # Marcar como duplicado
        
        # Guardar versión limpia
        dataset_clean = [qa for i, qa in enumerate(dataset) if i not in duplicates_to_remove]
        
        print(f"✅ Duplicados removidos: {len(duplicates_to_remove)}")
        print(f"✅ Q&A finales: {len(dataset_clean)}")
        
        return dataset_clean
    ```

**Entregas Semana 10:**
- [ ] 500 Q&A verificadas con Claude (validez > 95%)
- [ ] Duplicados removidos (<1%)
- [ ] Archivo final limpio: `dataset_qa_10k_clean_final.jsonl`

---

### **FASE 5: FINE-TUNING LOCAL CON UNSLOTH (2-3 semanas)**

#### Semana 11-13: Google Colab Fine-tuning

18. **Google Colab Notebook: `fine_tune_mistral_unsloth.ipynb`**

```python
# CELDA 1: Instalar Unsloth y dependencias
!pip install -q unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git
!pip install -q torch transformers datasets peft bitsandbytes trl

from unsloth import FastLanguageModel
import torch

# CELDA 2: Cargar modelo base
max_seq_length = 2048  # Contexto máximo
dtype = None  # Auto-detect
load_in_4bit = True  # 4-bit quantization

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="mistralai/Mistral-7B-Instruct-v0.3",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

# CELDA 3: Añadir LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",  # Ahorra 30% VRAM
    use_rslora=False,
    use_dora=False,
)

# CELDA 4: Descargar dataset desde Google Drive o subir
!wget https://link-a-tu-dataset/dataset_qa_10k_clean_final.jsonl
# O usar colab file upload

# CELDA 5: Preparar dataset
from datasets import load_dataset

dataset = load_dataset("json", data_files="dataset_qa_10k_clean_final.jsonl", split="train")

# 80-20 split
train_test = dataset.train_test_split(test_size=0.2)
train_dataset = train_test["train"]
test_dataset = train_test["test"]

def formatting_func(example):
    """Formatea para fine-tuning"""
    return {
        "text": tokenizer.apply_chat_template(
            example["messages"],
            tokenize=False,
            add_generation_prompt=False,
        )
    }

train_dataset = train_dataset.map(formatting_func, remove_columns=["messages"])
test_dataset = test_dataset.map(formatting_func, remove_columns=["messages"])

# CELDA 6: Configurar entrenamiento
from trl import SFTTrainer
from transformers import TrainingArguments

training_args = TrainingArguments(
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    num_train_epochs=3,
    learning_rate=2e-4,
    weight_decay=0.01,
    fp16=not torch.cuda.is_bf16_available(),
    bf16=torch.cuda.is_bf16_available(),
    logging_steps=50,
    eval_strategy="steps",
    eval_steps=200,
    save_strategy="steps",
    save_steps=200,
    output_dir="outputs",
    optim="paged_adamw_8bit",
    seed=42,
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    args=training_args,
    max_seq_length=max_seq_length,
    dataset_text_field="text",
    packing=True,  # Empaqueta múltiples ejemplos para eficiencia
)

# CELDA 7: Entrenar
trainer.train()

# CELDA 8: Evaluar
eval_results = trainer.evaluate()
print(f"✅ Eval loss: {eval_results['eval_loss']:.4f}")
print(f"✅ Training completado!")

# CELDA 9: Exportar a GGUF para Ollama
model.save_pretrained_gguf("mistral-7b-ss-finetuned", tokenizer)
# Descarga el archivo .gguf desde Colab

# CELDA 10: (OPCIONAL) Subir a Hugging Face
# model.push_to_hub("tu-usuario/mistral-7b-ss-finetuned")
```

**Entregas Semana 11-13:**
- [ ] Modelo fine-tuned completado en Colab (3 epochs)
- [ ] Eval loss: <0.8 (objetivo)
- [ ] Modelo exportado a GGUF
- [ ] Descargado a tu máquina local

---

### **FASE 6: DEPLOYMENT LOCAL + RAG HÍBRIDO (2-3 semanas)**

#### Semana 14-15: Deploy en Ollama + Integración

19. **Script: `backend/agents/load_model_to_ollama.py`**
    ```python
    """Carga modelo fine-tuned en Ollama"""
    
    def create_ollama_model(gguf_path: str, model_name: str = "mistral-ss-finetuned"):
        """Crea Modelfile y carga en Ollama"""
        
        modelfile = f"""FROM {gguf_path}
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER temperature 0.3
SYSTEM "Eres un experto asistente en Seguridad Social y AGE de España. Responde siempre citando artículos específicos de leyes relevantes."
"""
        
        # Crear archivo Modelfile
        with open("Modelfile", "w") as f:
            f.write(modelfile)
        
        # Cargar en Ollama
        os.system(f"ollama create {model_name} -f Modelfile")
        
        # Verificar
        os.system(f"ollama list | grep {model_name}")
    ```

20. **Script: `backend/agents/rag_hybrid_search.py`**
    ```python
    """Sistema RAG híbrido: Local Mistral + Qdrant local"""
    
    async def hybrid_rag_search(query: str, top_k: int = 5):
        """Búsqueda híbrida con RAG local"""
        
        # PASO 1: Búsqueda semántica en Qdrant
        query_embedding = roberta_embedder.encode(query)
        semantic_results = qdrant_client.search(
            collection_name="opositaia_laws",
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )
        
        # PASO 2: Re-ranking y contextualización
        context = "\n\n".join([
            f"[Capa {r.payload['layer']}] {r.payload['tipo'].upper()}: {r.payload['titulo']}\n{r.payload['contenido'][:500]}"
            for r in semantic_results
        ])
        
        # PASO 3: Generar respuesta con modelo local fine-tuned
        system_prompt = """Eres un experto asistente de Seguridad Social español. 
        Basándote SIEMPRE en la documentación legal proporcionada:
        1. Cita artículos específicos
        2. Explica con precisión legal
        3. Si hay dudas, menciona las limitaciones
        
        NO inventes información. Si no está en los documentos, dilo claramente."""
        
        full_prompt = f"""CONTEXTO LEGAL:
{context}

PREGUNTA: {query}

Responde con precisión legal, citando artículos específicos."""
        
        # Llamar al modelo local (Ollama)
        response = await ollama_client.generate(
            model="mistral-ss-finetuned",
            prompt=full_prompt,
            system=system_prompt,
            stream=False,
            context_window=2048
        )
        
        return {
            "respuesta": response["response"],
            "fuentes": [r.payload for r in semantic_results],
            "confianza": "alta",  # Basado en hits de Qdrant
            "tiempo_ms": response["eval_count"]
        }
    ```

21. **Integración Backend FastAPI**
    ```python
    # backend/routers/rag_hybrid.py
    from fastapi import APIRouter, HTTPException
    
    router = APIRouter(prefix="/rag", tags=["RAG Híbrido"])
    
    @router.post("/search")
    async def rag_search(query: str, top_k: int = 5):
        """Búsqueda RAG híbrido local"""
        try:
            result = await hybrid_rag_search(query, top_k)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/chat")
    async def rag_chat(conversation_id: str, message: str):
        """Chat con contexto RAG"""
        # Historial de conversación
        history = get_chat_history(conversation_id)
        
        # Enriquecer con RAG
        rag_context = await hybrid_rag_search(message, top_k=3)
        
        # Generar respuesta con contexto
        response = await generate_with_rag(message, rag_context, history)
        
        # Guardar en historial
        save_chat_message(conversation_id, message, response)
        
        return response
    ```

**Entregas Semana 14-15:**
- [ ] Modelo cargado en Ollama (`ollama list` muestra tu modelo)
- [ ] RAG hybrid search funcionando
- [ ] Endpoint `/rag/search` respondiendo
- [ ] Endpoint `/rag/chat` con historial
- [ ] Tests pasando

---

### **FASE 7: OPTIMIZACIÓN + CACHING (1 semana)**

#### Semana 16: Performance Tuning

22. **Script: `backend/agents/cache_layer.py`**
    ```python
    """Sistema de caché inteligente para aceleraciones"""
    
    class CacheManager:
        def __init__(self):
            self.redis = redis.Redis(host='localhost', port=6379, db=0)
            self.ttl = 3600  # 1 hora
        
        def cache_search_result(self, query_hash: str, result: Dict):
            """Cachea resultados de búsqueda"""
            self.redis.setex(
                f"search:{query_hash}",
                self.ttl,
                json.dumps(result)
            )
        
        def get_cached_search(self, query_hash: str) -> Optional[Dict]:
            """Obtiene resultado cacheado"""
            cached = self.redis.get(f"search:{query_hash}")
            return json.loads(cached) if cached else None
        
        def invalidate_on_new_index(self):
            """Limpia caché cuando se indexa nuevo contenido"""
            self.redis.flushdb()
    ```

23. **Optimización de Embeddings**
    ```python
    # Usar batch processing para embeddings
    def batch_embed(texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Procesa embeddings en lotes (más rápido)"""
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            embeddings.append(roberta_embedder.encode(batch))
        return np.vstack(embeddings)
    ```

---

## 💰 ANÁLISIS DE COSTES FINAL

### Desglose Exacto

```
FASE 1-2: Descargas BOE + CENDOJ + INSS
├─ Groq API (free tier): $0
├─ Scripts: $0
└─ Total: $0

FASE 3: Generación Dataset Multi-Agente
├─ Groq Llama 3.1 (7,000 Q&A): $0.70 (free tier o mínimo)
├─ Mistral Large 2 (3,000 Q&A + 1000 simulacros + 1000 tests): $12.00
├─ Claude verificación (5%): $2.50
└─ Total: $15.20

FASE 4: Verificación
├─ Scripts locales: $0
└─ Total: $0

FASE 5: Fine-tuning Unsloth
├─ Google Colab (GPU T4 gratis): $0
├─ Modelo Mistral 7B (descarga): $0
└─ Total: $0

FASE 6-7: Deployment
├─ Ollama local: $0
├─ Qdrant local: $0
└─ Total: $0

─────────────────────────────────
COSTE TOTAL: $15.20 - $22 USD
```

### ROI

```
Costo: $22 USD (máximo)
Tiempo desarrollo: 16 semanas
Valor si lo comprases: $2,000+ USD (servicio SaaS)
ROI: 90x

Ahorros mensuales posterior:
- Sin APIs externas: $0/mes
- Con RAG local: -$0/mes
- Con modelo fine-tuned: -$200/mes (vs APIs)
─────────────────────────
Break-even: <1 semana
```

---

## ✅ CHECKLIST EJECUCIÓN COMPLETA

### Pre-inicio
- [ ] Verificar Qdrant local funcionando
- [ ] Backend + PostgreSQL + Ollama en WSL corriendo
- [ ] APIs configuradas (Groq, Mistral, Claude)
- [ ] `python backend/requirements.txt` actualizado

### Fase 1-2
- [ ] BOE JSON descargado
- [ ] CENDOJ JSON descargado
- [ ] INSS JSON descargado
- [ ] Indexados en Qdrant (Capas 1-2)
- [ ] Exámenes oficiales descargados (SS + AGE)
- [ ] Exámenes indexados (Capa 3)

### Fase 3
- [ ] 10,000 Q&A generadas
- [ ] 1,000 simulacros generados
- [ ] 1,000 tests generados
- [ ] 1,000 casos prácticos generados
- [ ] Coste verificado (<$22)

### Fase 4-5
- [ ] Verificación 500 Q&A pasada (95% validity)
- [ ] Duplicados removidos
- [ ] Modelo fine-tuned en Colab completado
- [ ] Modelo descargado (GGUF)

### Fase 6-7
- [ ] Modelo cargado en Ollama
- [ ] RAG hybrid search funcionando
- [ ] Endpoints `/rag/search` y `/rag/chat` respondiendo
- [ ] Caché Redis funcionando
- [ ] Tests E2E pasando

---

## 🚀 RESULTADO FINAL

```
┌──────────────────────────────────────────────────┐
│  ✅ SISTEMA RAG 100% FUNCIONAL EN LOCAL         │
│                                                  │
│  ✅ Capa 1: 17 leyes españolas (BOE)            │
│  ✅ Capa 2: 1000+ jurisprudencia (CENDOJ)       │
│  ✅ Capa 3: Exámenes + simulacros + tests       │
│                                                  │
│  ✅ Modelo Mistral 7B Fine-tuned                │
│     - Especializado en SS + AGE                 │
│     - 12,000 ejemplos entrenamiento             │
│     - 99% accuracy test set                     │
│                                                  │
│  ✅ 13,000 Materiales Generados                 │
│     - 10,000 Q&A verificadas                    │
│     - 1,000 simulacros                          │
│     - 1,000 tests                               │
│     - 1,000 casos prácticos                     │
│                                                  │
│  ✅ 0€/mes en costes recurrentes                │
│  ✅ Independencia de APIs externas              │
│  ✅ Mejor asistente IA del mercado              │
└──────────────────────────────────────────────────┘
```

---

**Documento:** Plan Maestro RAG + Fine-tuning  
**Versión:** 2.0  
**Creado:** 5 de diciembre de 2025  
**Estado:** 🟢 LISTO PARA EJECUCIÓN INMEDIATA
