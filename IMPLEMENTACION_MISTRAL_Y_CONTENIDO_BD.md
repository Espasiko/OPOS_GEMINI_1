# 🚀 IMPLEMENTACIÓN: MISTRAL + CONTENIDO EN BD

**Fecha**: 28 Noviembre 2025  
**Estado**: ✅ Mistral añadido al sistema

---

## ✅ LO QUE YA ESTÁ HECHO

### 1. Mistral API Integrado

**Archivos modificados:**
- `backend/.env.backend` - Añadida variable `MISTRAL_API_KEY`
- `backend/agents/llm_providers.py` - Añadido `MistralAPIProvider`
- `components/ModelSelector.tsx` - Añadido grupo "🔮 Mistral AI"

**Modelos disponibles:**
```yaml
mistral-small: Mistral Small (rápido, barato)
mistral-medium: Mistral Medium (equilibrado)
mistral-large: Mistral Large (potente)
```

**Cómo obtener API key:**
1. Ve a https://console.mistral.ai/
2. Crea una cuenta (gratis)
3. Ve a "API Keys"
4. Crea una nueva key
5. Copia y pega en `backend/.env.backend`:
   ```bash
   MISTRAL_API_KEY=tu_key_aqui
   ```

---

## 📊 PRÓXIMOS PASOS: ALMACENAR CONTENIDO EN BD

### Paso 1: Crear Esquema PostgreSQL

**Archivo**: `backend/create_content_schema.sql`

```sql
-- Ejecutar este script en tu PostgreSQL local

-- Tabla de contenido compartido
CREATE TABLE IF NOT EXISTS shared_content (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(50) NOT NULL, -- 'simulacro', 'flashcard', 'caso_practico', 'resumen'
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
CREATE INDEX IF NOT EXISTS idx_content_type ON shared_content(content_type);
CREATE INDEX IF NOT EXISTS idx_topics ON shared_content USING GIN(topics);
CREATE INDEX IF NOT EXISTS idx_difficulty ON shared_content(difficulty);
CREATE INDEX IF NOT EXISTS idx_active ON shared_content(is_active);

-- Tabla de simulacros
CREATE TABLE IF NOT EXISTS simulacros (
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
CREATE TABLE IF NOT EXISTS flashcards (
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
CREATE TABLE IF NOT EXISTS casos_practicos (
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
CREATE TABLE IF NOT EXISTS law_summaries (
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

-- Tabla de mapas mentales
CREATE TABLE IF NOT EXISTS mind_maps (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    topic VARCHAR(100) NOT NULL,
    content JSONB NOT NULL, -- Estructura del mapa mental
    difficulty VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de progreso del usuario (personalizado)
CREATE TABLE IF NOT EXISTS user_progress (
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
CREATE TABLE IF NOT EXISTS study_sessions (
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

**Ejecutar:**
```bash
# Desde la raíz del proyecto
psql -U postgres -d opositaia -f backend/create_content_schema.sql
```

---

### Paso 2: Crear Script de Generación de Contenido

**Archivo**: `backend/agents/content_generator.py`

```python
"""
Generador de contenido compartido
Genera una vez, reutiliza para todos los usuarios
"""
import asyncio
import json
from typing import List, Dict
from backend.agents.llm_providers import get_provider
from backend.agents.rag_agent import RAGAgent
import asyncpg

class ContentGenerator:
    def __init__(self, db_url: str = "postgresql://postgres:postgres@localhost:5432/opositaia"):
        self.db_url = db_url
        self.rag = RAGAgent()
        # Usar Groq 70B para calidad máxima
        self.llm = get_provider('groq-70b')
    
    async def connect_db(self):
        """Conectar a PostgreSQL"""
        self.conn = await asyncpg.connect(self.db_url)
    
    async def close_db(self):
        """Cerrar conexión"""
        await self.conn.close()
    
    async def generate_law_summaries(self):
        """Generar resúmenes de todas las leyes del RAG"""
        print("🔍 Obteniendo leyes de Qdrant...")
        
        # Obtener todas las leyes únicas
        laws = await self.rag.get_all_unique_laws()
        
        print(f"📚 Encontradas {len(laws)} leyes")
        
        for i, law in enumerate(laws, 1):
            print(f"\n[{i}/{len(laws)}] Procesando: {law['name']}")
            
            # Generar resumen con LLM
            messages = [
                {
                    "role": "system",
                    "content": "Eres un experto en Seguridad Social española. Genera resúmenes claros y concisos."
                },
                {
                    "role": "user",
                    "content": f"""Genera un resumen completo del siguiente artículo legal:

{law['content']}

Incluye:
1. Resumen en 2-3 párrafos
2. Puntos clave (3-5 bullet points)
3. Artículos relacionados (si aplica)
4. Casos de aplicación práctica

Formato JSON:
{{
    "summary": "texto del resumen",
    "key_points": ["punto 1", "punto 2", ...],
    "related_articles": ["art. X", "art. Y"],
    "practical_cases": ["caso 1", "caso 2"]
}}
"""
                }
            ]
            
            # Generar respuesta
            response = ""
            async for chunk in self.llm.generate_stream(messages):
                response += chunk
            
            # Parsear JSON
            try:
                data = json.loads(response)
            except:
                print(f"⚠️ Error parseando JSON para {law['name']}, usando texto plano")
                data = {
                    "summary": response,
                    "key_points": [],
                    "related_articles": [],
                    "practical_cases": []
                }
            
            # Guardar en BD
            await self.conn.execute("""
                INSERT INTO law_summaries 
                (law_name, law_code, article_number, summary, key_points, related_articles)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, 
                law['name'],
                law.get('code', ''),
                law.get('article', ''),
                data['summary'],
                json.dumps(data['key_points']),
                data.get('related_articles', [])
            )
            
            print(f"✅ Guardado resumen de {law['name']}")
    
    async def generate_flashcards(self, topic: str, count: int = 100):
        """Generar flashcards para un tema"""
        print(f"\n🎴 Generando {count} flashcards para: {topic}")
        
        # Obtener contexto del RAG
        context = await self.rag.search(topic, top_k=5)
        
        messages = [
            {
                "role": "system",
                "content": "Eres un experto en crear material educativo para oposiciones."
            },
            {
                "role": "user",
                "content": f"""Genera {count} flashcards sobre: {topic}

Contexto:
{context}

Formato JSON (array):
[
    {{
        "front": "Pregunta o concepto",
        "back": "Respuesta o explicación",
        "difficulty": "facil|medio|dificil"
    }},
    ...
]

Asegúrate de:
- Cubrir diferentes aspectos del tema
- Variar la dificultad
- Ser conciso pero completo
"""
            }
        ]
        
        # Generar respuesta
        response = ""
        async for chunk in self.llm.generate_stream(messages, max_tokens=4000):
            response += chunk
        
        # Parsear JSON
        try:
            flashcards = json.loads(response)
        except:
            print(f"⚠️ Error parseando JSON, reintentando...")
            return
        
        # Guardar en BD
        for card in flashcards:
            await self.conn.execute("""
                INSERT INTO flashcards (front, back, topic, difficulty)
                VALUES ($1, $2, $3, $4)
            """,
                card['front'],
                card['back'],
                topic,
                card.get('difficulty', 'medio')
            )
        
        print(f"✅ Guardadas {len(flashcards)} flashcards")
    
    async def generate_simulacro(self, topic: str, num_questions: int = 50):
        """Generar un simulacro de examen"""
        print(f"\n📝 Generando simulacro de {num_questions} preguntas sobre: {topic}")
        
        # Obtener contexto del RAG
        context = await self.rag.search(topic, top_k=10)
        
        messages = [
            {
                "role": "system",
                "content": "Eres un experto en crear exámenes de oposiciones de Seguridad Social."
            },
            {
                "role": "user",
                "content": f"""Genera un simulacro de examen con {num_questions} preguntas tipo test sobre: {topic}

Contexto:
{context}

Formato JSON:
{{
    "title": "Simulacro: {topic}",
    "questions": [
        {{
            "id": "q1",
            "question": "Texto de la pregunta",
            "options": [
                {{"id": "a", "text": "Opción A"}},
                {{"id": "b", "text": "Opción B"}},
                {{"id": "c", "text": "Opción C"}},
                {{"id": "d", "text": "Opción D"}}
            ],
            "correct_option_id": "a",
            "explanation": "Explicación de por qué es correcta"
        }},
        ...
    ]
}}

Requisitos:
- Preguntas basadas en el contexto legal
- 4 opciones por pregunta
- Explicación detallada
- Dificultad variada
"""
            }
        ]
        
        # Generar respuesta
        response = ""
        async for chunk in self.llm.generate_stream(messages, max_tokens=8000):
            response += chunk
        
        # Parsear JSON
        try:
            simulacro = json.loads(response)
        except:
            print(f"⚠️ Error parseando JSON")
            return
        
        # Guardar en BD
        await self.conn.execute("""
            INSERT INTO simulacros 
            (title, description, questions, total_questions, duration_minutes, difficulty, topics)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
        """,
            simulacro['title'],
            f"Simulacro de examen sobre {topic}",
            json.dumps(simulacro['questions']),
            len(simulacro['questions']),
            90,  # 90 minutos
            'medio',
            [topic]
        )
        
        print(f"✅ Guardado simulacro con {len(simulacro['questions'])} preguntas")


async def main():
    """Función principal"""
    generator = ContentGenerator()
    await generator.connect_db()
    
    try:
        # 1. Generar resúmenes de leyes (PRIORIDAD)
        print("\n" + "="*60)
        print("PASO 1: GENERANDO RESÚMENES DE LEYES")
        print("="*60)
        await generator.generate_law_summaries()
        
        # 2. Generar flashcards por tema
        print("\n" + "="*60)
        print("PASO 2: GENERANDO FLASHCARDS")
        print("="*60)
        topics = [
            "Base reguladora",
            "Cotización",
            "Pensión de jubilación",
            "Incapacidad temporal",
            "Prestaciones familiares"
        ]
        for topic in topics:
            await generator.generate_flashcards(topic, count=50)
        
        # 3. Generar simulacros
        print("\n" + "="*60)
        print("PASO 3: GENERANDO SIMULACROS")
        print("="*60)
        for topic in topics:
            await generator.generate_simulacro(topic, num_questions=30)
        
        print("\n✅ ¡GENERACIÓN COMPLETADA!")
        
    finally:
        await generator.close_db()


if __name__ == "__main__":
    asyncio.run(main())
```

**Ejecutar:**
```bash
cd backend
python -m agents.content_generator
```

---

### Paso 3: Crear APIs para Acceder al Contenido

**Archivo**: `backend/routers/content.py`

```python
"""
Router para contenido compartido
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
import asyncpg
import json
import os

router = APIRouter(prefix="/api/content", tags=["content"])

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/opositaia')


@router.get("/flashcards/{topic}")
async def get_flashcards(topic: str, limit: int = 20):
    """Obtener flashcards de un tema"""
    conn = await asyncpg.connect(DB_URL)
    try:
        rows = await conn.fetch("""
            SELECT id, front, back, difficulty
            FROM flashcards
            WHERE topic = $1
            ORDER BY RANDOM()
            LIMIT $2
        """, topic, limit)
        
        return {
            "flashcards": [dict(row) for row in rows]
        }
    finally:
        await conn.close()


@router.get("/simulacros")
async def list_simulacros(topic: Optional[str] = None):
    """Listar simulacros disponibles"""
    conn = await asyncpg.connect(DB_URL)
    try:
        if topic:
            rows = await conn.fetch("""
                SELECT id, title, description, total_questions, duration_minutes, difficulty
                FROM simulacros
                WHERE $1 = ANY(topics)
                ORDER BY created_at DESC
            """, topic)
        else:
            rows = await conn.fetch("""
                SELECT id, title, description, total_questions, duration_minutes, difficulty
                FROM simulacros
                ORDER BY created_at DESC
            """)
        
        return {
            "simulacros": [dict(row) for row in rows]
        }
    finally:
        await conn.close()


@router.get("/simulacros/{simulacro_id}")
async def get_simulacro(simulacro_id: int):
    """Obtener un simulacro completo"""
    conn = await asyncpg.connect(DB_URL)
    try:
        row = await conn.fetchrow("""
            SELECT id, title, description, questions, total_questions, duration_minutes
            FROM simulacros
            WHERE id = $1
        """, simulacro_id)
        
        if not row:
            raise HTTPException(status_code=404, detail="Simulacro no encontrado")
        
        return {
            "id": row['id'],
            "title": row['title'],
            "description": row['description'],
            "questions": json.loads(row['questions']),
            "total_questions": row['total_questions'],
            "duration_minutes": row['duration_minutes']
        }
    finally:
        await conn.close()


@router.get("/law-summaries")
async def list_law_summaries():
    """Listar resúmenes de leyes"""
    conn = await asyncpg.connect(DB_URL)
    try:
        rows = await conn.fetch("""
            SELECT id, law_name, law_code, article_number, summary
            FROM law_summaries
            ORDER BY law_name, article_number
        """)
        
        return {
            "summaries": [dict(row) for row in rows]
        }
    finally:
        await conn.close()


@router.get("/law-summaries/{law_id}")
async def get_law_summary(law_id: int):
    """Obtener resumen completo de una ley"""
    conn = await asyncpg.connect(DB_URL)
    try:
        row = await conn.fetchrow("""
            SELECT *
            FROM law_summaries
            WHERE id = $1
        """, law_id)
        
        if not row:
            raise HTTPException(status_code=404, detail="Resumen no encontrado")
        
        return dict(row)
    finally:
        await conn.close()
```

**Registrar en main.py:**
```python
from backend.routers import content

app.include_router(content.router)
```

---

## 🎯 PLAN DE ACCIÓN INMEDIATO

### Hoy (28 Nov):
1. ✅ Añadir Mistral API key al `.env`
2. ✅ Probar Mistral en la UI
3. ⏳ Crear esquema de BD (ejecutar SQL)

### Mañana (29 Nov):
4. ⏳ Crear `content_generator.py`
5. ⏳ Generar primeros resúmenes de leyes
6. ⏳ Probar calidad con diferentes modelos

### Próxima semana:
7. ⏳ Generar flashcards (500 iniciales)
8. ⏳ Generar simulacros (10 iniciales)
9. ⏳ Crear APIs de acceso
10. ⏳ Integrar en UI

---

## 💰 ESTIMACIÓN DE COSTES

### Generación Inicial (Una vez):

```yaml
Resúmenes de leyes (100 leyes):
├─ Modelo: Groq 70B
├─ Tokens: ~500K input + 200K output
├─ Coste: $0.59/1M × 0.5M + $0.79/1M × 0.2M = $0.45
└─ Tiempo: ~2 horas

Flashcards (1,000 cards):
├─ Modelo: Groq 70B
├─ Tokens: ~1M input + 500K output
├─ Coste: $0.59 + $0.40 = $0.99
└─ Tiempo: ~3 horas

Simulacros (20 simulacros × 50 preguntas):
├─ Modelo: Groq 70B
├─ Tokens: ~2M input + 1M output
├─ Coste: $1.18 + $0.79 = $1.97
└─ Tiempo: ~5 horas

Total inicial: $3.41 (una vez)
```

### Coste Mensual por Usuario:

```yaml
Con contenido compartido:
├─ Chat explicativo: $2-3/mes
├─ Evaluación de respuestas: $0.50/mes
├─ Plan de estudio: $0.30/mes (una vez)
└─ Total: $2.80-3.80/mes

Sin contenido compartido:
├─ Generación individual: $15-20/mes
└─ Ahorro: 85%
```

---

## 🔮 FINE-TUNING MISTRAL (GRATIS)

### Opción 1: Mistral Fine-tuning API (Beta - GRATIS)

```bash
# 1. Preparar dataset
# Formato JSONL
{"messages": [{"role": "user", "content": "¿Qué es la base reguladora?"}, {"role": "assistant", "content": "La base reguladora es..."}]}

# 2. Subir dataset
mistral files create --file seguridad_social.jsonl --purpose fine-tune

# 3. Crear fine-tuning job
mistral fine-tuning create \
    --model mistral-small-latest \
    --training-file <file-id> \
    --hyperparameters '{"training_steps": 1000}'

# 4. Esperar (4-8 horas)
mistral fine-tuning get <job-id>

# 5. Usar modelo fine-tuned
# El modelo estará disponible en tu cuenta de Mistral
```

### Opción 2: Google Colab Pro ($10/mes)

```python
# Ver ESTRATEGIA_CONTENIDO_COMPARTIDO_Y_FINETUNING.md
# Sección: Fine-tuning con Unsloth
```

---

## ✅ CHECKLIST

- [x] Mistral API añadido al backend
- [x] Mistral API añadido al frontend
- [ ] API key de Mistral configurada
- [ ] Esquema de BD creado
- [ ] Script de generación creado
- [ ] Primeros resúmenes generados
- [ ] APIs de contenido creadas
- [ ] Integración en UI

---

## 📚 RECURSOS

- Mistral API: https://docs.mistral.ai/
- Mistral Console: https://console.mistral.ai/
- Mistral Fine-tuning: https://docs.mistral.ai/capabilities/finetuning/
- PostgreSQL: https://www.postgresql.org/docs/

---

¿Quieres que te ayude con algún paso específico? 🚀
