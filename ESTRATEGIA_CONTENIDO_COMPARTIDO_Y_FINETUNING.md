# 🎯 ESTRATEGIA: CONTENIDO COMPARTIDO + FINE-TUNING

**Fecha**: 28 Noviembre 2025  
**Concepto**: Reducir costes IA mediante contenido pre-generado compartido entre usuarios

---

## 💡 TU IDEA BRILLANTE

### Concepto Central

**En lugar de generar contenido único para cada usuario, generar una vez y reutilizar:**

```yaml
Contenido Compartido (Generado 1 vez):
├─ Simulacros de examen (1,000 tests)
├─ Casos prácticos (500 casos)
├─ Flashcards (10,000 tarjetas)
├─ Resúmenes de leyes (todas las leyes del RAG)
├─ Mapas mentales (por tema)
├─ Esquemas conceptuales
└─ Memes educativos

Personalización:
├─ Orden aleatorio de preguntas
├─ Mezcla de temas
├─ Combinación de elementos
└─ Tracking de progreso individual
```

---

## 📊 ANÁLISIS DE AHORRO

### Coste Actual (Generación Individual)

```yaml
Usuario genera contenido propio:
├─ 10 simulacros: 10 × $0.50 = $5.00
├─ 50 flashcards: 50 × $0.10 = $5.00
├─ 5 casos prácticos: 5 × $0.80 = $4.00
├─ 10 resúmenes: 10 × $0.30 = $3.00
└─ Total por usuario: $17.00

100 usuarios: $1,700/mes
```

### Coste con Contenido Compartido

```yaml
Generación inicial (una vez):
├─ 1,000 simulacros: $500 (una vez)
├─ 10,000 flashcards: $1,000 (una vez)
├─ 500 casos prácticos: $400 (una vez)
├─ Resúmenes todas las leyes: $200 (una vez)
└─ Total inicial: $2,100 (una vez)

Coste mensual:
├─ Actualización contenido (10%): $210/mes
├─ Nuevas variaciones: $100/mes
└─ Total mensual: $310/mes

100 usuarios: $310/mes (vs $1,700)
Ahorro: 82%
```

---

## 🗄️ ARQUITECTURA DE BASE DE DATOS

### Esquema PostgreSQL

```sql
-- Tabla de contenido compartido
CREATE TABLE shared_content (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(50) NOT NULL, -- 'simulacro', 'flashcard', 'caso_practico', etc.
    title VARCHAR(255) NOT NULL,
    content JSONB NOT NULL,
    metadata JSONB,
    difficulty VARCHAR(20), -- 'facil', 'medio', 'dificil'
    topics TEXT[], -- Array de temas
    law_references TEXT[], -- Referencias a leyes
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE
);

-- Índices para búsqueda rápida
CREATE INDEX idx_content_type ON shared_content(content_type);
CREATE INDEX idx_topics ON shared_content USING GIN(topics);
CREATE INDEX idx_difficulty ON shared_content(difficulty);
CREATE INDEX idx_active ON shared_content(is_active);

-- Tabla de simulacros
CREATE TABLE simulacros (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    questions JSONB NOT NULL, -- Array de preguntas
    total_questions INTEGER,
    duration_minutes INTEGER,
    difficulty VARCHAR(20),
    topics TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Tabla de flashcards
CREATE TABLE flashcards (
    id SERIAL PRIMARY KEY,
    front TEXT NOT NULL,
    back TEXT NOT NULL,
    topic VARCHAR(100),
    law_reference VARCHAR(100),
    difficulty VARCHAR(20),
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de casos prácticos
CREATE TABLE casos_practicos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    scenario TEXT NOT NULL,
    question TEXT NOT NULL,
    solution TEXT NOT NULL,
    explanation TEXT,
    topics TEXT[],
    difficulty VARCHAR(20),
    law_references TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de resúmenes de leyes
CREATE TABLE law_summaries (
    id SERIAL PRIMARY KEY,
    law_name VARCHAR(255) NOT NULL,
    law_code VARCHAR(50) NOT NULL,
    article_number VARCHAR(20),
    summary TEXT NOT NULL,
    key_points JSONB,
    related_articles TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de progreso del usuario (personalizado)
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    content_id INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    score FLOAT,
    attempts INTEGER DEFAULT 0,
    last_attempt TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de sesiones de estudio
CREATE TABLE study_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    simulacro_id INTEGER,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    score FLOAT,
    answers JSONB, -- Respuestas del usuario
    time_spent INTEGER -- segundos
);
```

---

## 🤖 USO DE IA: SOLO DONDE IMPORTA

### Contenido Pre-generado (Batch, una vez)

```python
class ContentGenerator:
    """Generar contenido compartido en batch"""
    
    async def generate_all_content(self):
        """Generar todo el contenido inicial"""
        
        # 1. Resúmenes de todas las leyes (PRIORIDAD)
        await self.generate_law_summaries()
        
        # 2. Flashcards por tema
        await self.generate_flashcards()
        
        # 3. Simulacros de examen
        await self.generate_simulacros()
        
        # 4. Casos prácticos
        await self.generate_casos_practicos()
    
    async def generate_law_summaries(self):
        """Generar resúmenes de todas las leyes del RAG"""
        
        # Obtener todas las leyes de Qdrant
        laws = await self.get_all_laws_from_qdrant()
        
        for law in laws:
            # Usar Groq 70B para resúmenes de calidad
            summary = await self.groq_70b.generate(
                f"""Genera un resumen completo del siguiente artículo legal:
                
                {law.content}
                
                Incluye:
                1. Resumen en 2-3 párrafos
                2. Puntos clave (bullet points)
                3. Artículos relacionados
                4. Casos de aplicación práctica
                """
            )
            
            # Guardar en BD
            await self.db.execute(
                """INSERT INTO law_summaries 
                   (law_name, law_code, article_number, summary, key_points)
                   VALUES ($1, $2, $3, $4, $5)""",
                law.name, law.code, law.article, 
                summary['text'], summary['key_points']
            )
    
    async def generate_flashcards(self):
        """Generar flashcards por tema"""
        
        topics = await self.get_all_topics()
        
        for topic in topics:
            # Generar 100 flashcards por tema
            flashcards = await self.groq_70b.generate(
                f"""Genera 100 flashcards para el tema: {topic}
                
                Formato JSON:
                [
                    {{"front": "Pregunta", "back": "Respuesta", "difficulty": "facil"}},
                    ...
                ]
                """
            )
            
            # Guardar en BD
            for card in flashcards:
                await self.db.execute(
                    """INSERT INTO flashcards (front, back, topic, difficulty)
                       VALUES ($1, $2, $3, $4)""",
                    card['front'], card['back'], topic, card['difficulty']
                )
```

---

## 🎲 PERSONALIZACIÓN SIN COSTE ADICIONAL

### Mezcla y Aleatorización

```python
class ContentPersonalizer:
    """Personalizar contenido compartido para cada usuario"""
    
    async def get_personalized_simulacro(self, user_id: int, topic: str = None):
        """Crear simulacro personalizado mezclando preguntas existentes"""
        
        # 1. Obtener preguntas de la BD (ya generadas)
        questions = await self.db.fetch(
            """SELECT * FROM shared_content 
               WHERE content_type = 'question'
               AND ($1 IS NULL OR $1 = ANY(topics))
               AND is_active = TRUE
               ORDER BY RANDOM()
               LIMIT 50""",
            topic
        )
        
        # 2. Mezclar orden
        random.shuffle(questions)
        
        # 3. Guardar sesión del usuario
        session_id = await self.db.fetchval(
            """INSERT INTO study_sessions (user_id, started_at)
               VALUES ($1, NOW())
               RETURNING id""",
            user_id
        )
        
        return {
            'session_id': session_id,
            'questions': questions,
            'total': len(questions),
            'duration_minutes': 90
        }
    
    async def get_personalized_flashcards(self, user_id: int, topic: str, count: int = 20):
        """Obtener flashcards personalizadas"""
        
        # Obtener flashcards que el usuario no ha visto recientemente
        cards = await self.db.fetch(
            """SELECT f.* FROM flashcards f
               LEFT JOIN user_progress up ON 
                   up.content_id = f.id AND 
                   up.user_id = $1 AND 
                   up.content_type = 'flashcard'
               WHERE f.topic = $2
               AND (up.last_attempt IS NULL OR up.last_attempt < NOW() - INTERVAL '7 days')
               ORDER BY RANDOM()
               LIMIT $3""",
            user_id, topic, count
        )
        
        return cards
    
    async def get_mixed_simulacro(self, user_id: int, topics: list):
        """Crear simulacro mezclando múltiples temas"""
        
        questions_per_topic = 50 // len(topics)
        all_questions = []
        
        for topic in topics:
            questions = await self.db.fetch(
                """SELECT * FROM shared_content 
                   WHERE content_type = 'question'
                   AND $1 = ANY(topics)
                   ORDER BY RANDOM()
                   LIMIT $2""",
                topic, questions_per_topic
            )
            all_questions.extend(questions)
        
        # Mezclar todas las preguntas
        random.shuffle(all_questions)
        
        return all_questions
```

---

## 💰 COSTE REAL POR USUARIO

### Con Contenido Compartido

```yaml
Coste por usuario/mes:
├─ Chat explicativo: $2-5/mes (único coste variable)
├─ Evaluación de respuestas: $0.50/mes
├─ Plan de estudio personalizado: $0.30/mes (una vez)
└─ Total: $2.80-5.80/mes

Contenido compartido:
├─ Simulacros: $0 (ya generado)
├─ Flashcards: $0 (ya generado)
├─ Casos prácticos: $0 (ya generado)
├─ Resúmenes: $0 (ya generado)
└─ Total: $0/mes
```

### Distribución de Uso de IA

```yaml
Uso de IA por usuario:
├─ 80% requests: Contenido de BD (sin coste IA)
├─ 15% requests: Chat explicativo (Groq 8B)
├─ 5% requests: Evaluación compleja (Groq 70B)
└─ Coste promedio: $3/mes por usuario
```

---

## 🚀 FINE-TUNING: OPCIONES VIABLES

### OPCIÓN 1: Google Colab Pro (RECOMENDADO)

```yaml
Google Colab Pro:
├─ Precio: $10/mes
├─ GPU: A100 40GB
├─ Tiempo fine-tuning: 4-6 horas
├─ Coste total: $10 (una vez)
└─ Resultado: Modelo especializado en Seguridad Social
```

**Proceso:**

```python
# En Google Colab Pro
!pip install unsloth transformers datasets

from unsloth import FastLanguageModel
import torch

# 1. Cargar modelo base
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3.2-3b-bnb-4bit",  # Modelo pequeño
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# 2. Configurar LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
)

# 3. Preparar dataset (de tus leyes)
dataset = load_dataset("json", data_files="seguridad_social_dataset.json")

# 4. Entrenar
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=1000,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=1,
        optim="adamw_8bit",
        output_dir="outputs",
    ),
)

trainer.train()

# 5. Guardar modelo
model.save_pretrained("opositaia-llama-3b-ss")
tokenizer.save_pretrained("opositaia-llama-3b-ss")

# 6. Convertir a GGUF para usar en VPS
!python llama.cpp/convert.py opositaia-llama-3b-ss \
    --outtype q5_k_m \
    --outfile opositaia-llama-3b-ss-q5.gguf
```

---

### OPCIÓN 2: Hugging Face (GRATIS con limitaciones)

```yaml
Hugging Face:
├─ GPU: T4 16GB (gratis con limitaciones)
├─ Tiempo: 8-12 horas
├─ Coste: $0 (gratis)
└─ Limitación: Puede interrumpirse
```

**Proceso:**

```python
# Mismo código que Colab, pero en HF Spaces
# Crear Space con GPU T4
# Subir dataset
# Ejecutar training
```

---

### OPCIÓN 3: Mistral Fine-tuning (GRATIS)

**Mistral ofrece fine-tuning GRATIS de sus modelos:**

```yaml
Mistral Fine-tuning:
├─ Modelo: Mistral 7B
├─ Coste: GRATIS (beta)
├─ Límite: 1 fine-tuning/mes
├─ Hosting: Mistral API
└─ Precio inferencia: $0.25/1M tokens (más barato que Groq)
```

**Proceso:**

```bash
# 1. Instalar Mistral CLI
pip install mistralai

# 2. Preparar dataset (formato JSONL)
# seguridad_social.jsonl
{"messages": [{"role": "user", "content": "¿Qué es la base reguladora?"}, {"role": "assistant", "content": "La base reguladora es..."}]}

# 3. Subir dataset
mistral files create --file seguridad_social.jsonl --purpose fine-tune

# 4. Crear fine-tuning job
mistral fine-tuning create \
    --model mistral-small-latest \
    --training-file <file-id> \
    --validation-file <file-id> \
    --hyperparameters '{"training_steps": 1000}'

# 5. Esperar (4-8 horas)
mistral fine-tuning get <job-id>

# 6. Usar modelo fine-tuned
mistral chat --model <fine-tuned-model-id>
```

---

## 🖥️ HOSTING EN VPS K4 (16GB RAM, 4 cores)

### Modelo Recomendado: Llama 3.2 3B GGUF Q5_K_M

```yaml
Llama 3.2 3B Q5_K_M:
├─ Tamaño: ~2.5 GB
├─ RAM necesaria: 4-5 GB (con contexto)
├─ Velocidad en CPU (4 cores): 20-30 tokens/seg
├─ Calidad: 90-95% (fine-tuned)
└─ VIABLE en VPS K4: ✅ SÍ
```

**Instalación en VPS:**

```bash
# 1. Instalar llama.cpp
cd /opt
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make -j4

# 2. Descargar modelo fine-tuned
wget https://huggingface.co/tu-usuario/opositaia-llama-3b-ss-gguf/resolve/main/opositaia-llama-3b-ss-q5.gguf

# 3. Crear servidor
./server \
    -m opositaia-llama-3b-ss-q5.gguf \
    -c 2048 \
    -t 4 \
    --host 0.0.0.0 \
    --port 8080 \
    --n-gpu-layers 0

# 4. Crear servicio systemd
sudo nano /etc/systemd/system/llama-server.service
```

**Servicio systemd:**

```ini
[Unit]
Description=Llama.cpp Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/llama.cpp
ExecStart=/opt/llama.cpp/server -m /opt/models/opositaia-llama-3b-ss-q5.gguf -c 2048 -t 4 --host 0.0.0.0 --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable llama-server
sudo systemctl start llama-server
```

---

## 📊 BASES DE DATOS GRATUITAS PARA CONTENIDO

### Opciones Free Tier

```yaml
1. Supabase:
├─ PostgreSQL: 500 MB (gratis)
├─ Storage: 1 GB (gratis)
├─ API requests: Ilimitadas
└─ Suficiente para: 10K flashcards, 1K simulacros

2. PlanetScale:
├─ MySQL: 5 GB (gratis)
├─ Rows: 1 billón
└─ Suficiente para: Todo el contenido

3. Neon:
├─ PostgreSQL: 3 GB (gratis)
├─ Branches: Ilimitadas
└─ Suficiente para: Todo el contenido

4. Railway:
├─ PostgreSQL: 1 GB (gratis)
├─ $5 crédito/mes
└─ Suficiente para: Contenido inicial
```

---

## 🎯 PLAN DE IMPLEMENTACIÓN

### Fase 1: Generar Contenido Compartido (Semana 1-2)

```yaml
Prioridades:
1. Resúmenes de todas las leyes del RAG
2. 1,000 flashcards (100 por tema principal)
3. 100 simulacros (10 por tema)
4. 50 casos prácticos

Coste generación:
├─ Usar Groq 70B en batch (50% descuento)
├─ Coste estimado: $500 (una vez)
└─ Tiempo: 2-3 días de procesamiento
```

### Fase 2: Implementar BD y APIs (Semana 2)

```yaml
Tareas:
1. Crear esquema PostgreSQL
2. Migrar contenido generado a BD
3. Crear APIs de acceso
4. Implementar personalización
```

### Fase 3: Fine-tuning (Semana 3)

```yaml
Opciones:
1. Google Colab Pro: $10 (4-6 horas)
2. Mistral Fine-tuning: GRATIS (8-12 horas)
3. Hugging Face: GRATIS (12-24 horas)

Recomendación: Probar Mistral primero (gratis)
```

### Fase 4: Deploy en VPS K4 (Semana 4)

```yaml
Si fine-tuning funciona:
├─ Upgrade a VPS K4: +€150/mes
├─ Deploy modelo GGUF
├─ Configurar load balancer
└─ Testing de rendimiento
```

---

## 💰 COSTE FINAL ESTIMADO

```yaml
Setup inicial:
├─ Generación contenido: $500 (una vez)
├─ Fine-tuning: $0-10 (una vez)
└─ Total inicial: $500-510

Coste mensual:
├─ VPS K4: €150/mes (si usas modelo propio)
├─ BD: €0 (free tier suficiente)
├─ Actualización contenido: €50/mes
├─ Chat explicativo (Groq 8B): €30/mes
└─ Total: €230/mes

Por usuario (100 usuarios):
└─ €2.30/mes por usuario

Por usuario (500 usuarios):
└─ €0.46/mes por usuario
```

---

## ✅ PRÓXIMOS PASOS INMEDIATOS

1. **Añadir Mistral al sistema** (hoy)
2. **Crear esquema BD** (mañana)
3. **Generar primeros resúmenes** (esta semana)
4. **Probar fine-tuning Mistral** (próxima semana)

¿Empezamos con Mistral? 🚀
