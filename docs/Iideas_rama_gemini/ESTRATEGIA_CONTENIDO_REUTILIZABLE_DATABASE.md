# 🚀 ESTRATEGIA: Contenido Reutilizable en Base de Datos

**Fecha**: 28 Noviembre 2025  
**Idea**: Crear ONCE, reutilizar 1000 veces  
**Ahorro**: 90%+ en generación IA  
**Coste**: €0.02/mes por usuario (vs €1.14)  
**Complejidad**: Media

---

## 🎯 EL CONCEPTO

### El Cambio de Paradigma

```
ANTES (Generativo por cada usuario):
├─ Usuario 1 pide simulacro → GenAI crea (+0.007 USD)
├─ Usuario 2 pide simulacro → GenAI crea (+0.007 USD)
├─ Usuario 3 pide simulacro → GenAI crea (+0.007 USD)
├─ Usuario 1000 pide simulacro → GenAI crea (+0.007 USD)
└─ TOTAL: 1000 × 0.007 USD = €6.40/mes

DESPUÉS (Crear 1 vez, servir 1000 veces):
├─ Semana 1: Crear 1000 simulacros → GenAI crea 1 vez (+0.007 USD × 1000)
├─ Guardar en BD (PostgreSQL/MongoDB)
├─ Usuario 1 → Sirve desde BD (€0.00)
├─ Usuario 2 → Sirve desde BD (€0.00)
├─ Usuario 1000 → Sirve desde BD (€0.00)
└─ TOTAL: 7 USD (Semana 1) + €0/mes = Casi GRATIS después

AHORRO: 99% después de semana 1 ✅✅✅
```

---

## 📊 ANÁLISIS: QUÉ REUTILIZAR

### Tipo 1: Simulacros (Exámenes Completos) ⭐⭐⭐⭐⭐

```
HECHO: Crear 1000 simulacros variados
├─ Temarios oficiales (ya están en RAG)
├─ Generar 20 simulacros por tema (50 temas = 1000)
├─ Cada uno: 30-50 preguntas tipo test
├─ Coste creación: 1000 × €0.007 = €7/mes (una sola vez)
├─ Variantes: Mezclar preguntas (no duplicar 100%)
└─ Reutilización: 100% para cada usuario

SERVICIO: BD PostgreSQL
├─ Tabla: simulacros
├─ Campos: id, tema, nivel, preguntas (JSON), respuestas, explicaciones
├─ Index: tema, nivel, fecha_creacion
└─ Acceso: O(1) lectura

RESULTADO:
├─ Cada usuario puede hacer infinitos simulacros
├─ Mismos simulacros pero orden aleatorio
├─ Explicaciones ya incluidas
├─ Coste: €0 después de creación inicial
└─ Velocidad: 50ms (vs 3s con GenAI)
```

### Tipo 2: Casos Prácticos ⭐⭐⭐⭐⭐

```
HECHO: Crear 500 casos prácticos reales
├─ Basados en sentencias reales (BOE)
├─ 10 casos por tema (50 temas = 500)
├─ Análisis, solución, referencias
├─ Coste: 500 × €0.015 = €7.50 (creación)
├─ Variantes: Cambiar números, nombres, hechos menores

SERVICIO: BD
├─ Tabla: casos_practicos
├─ Análisis pre-calculado: 3 soluciones diferentes
├─ Explicación jurisprudencial
├─ Referencias a artículos del RAG

REUTILIZACIÓN: 100%
├─ Usuario A → Caso 1 original
├─ Usuario B → Caso 1 variante (números distintos)
├─ Usuario C → Caso 1 variante (hechos distintos)
├─ Mismo contenido, contexto personalizado

RESULTADO:
├─ Mil usuarios, 500 casos únicos
├─ Versión en paralelo para no repetir
├─ GenAI solo para explicar dudas específicas
└─ Coste: €7.50 (inicial) + €0 (reutilización)
```

### Tipo 3: Flashcards/Tarjetas ⭐⭐⭐⭐

```
HECHO: Crear 5000 flashcards automáticas
├─ 1 tarjeta por concepto clave
├─ Pregunta: "¿Qué es...?" → Respuesta: "Es..."
├─ Fuente: RAG + Títulos de artículos
├─ Coste: Casi €0 (extracción automática del RAG)

GENERACIÓN AUTOMÁTICA:
```python
for concept in rag_concepts:  # 5000 conceptos
    card = {
        "pregunta": f"¿Qué es {concept['nombre']}?",
        "respuesta": concept['definicion_corta'],
        "explicacion": concept['texto_completo'][:500],
        "tema": concept['tema'],
        "nivel": concept['nivel']
    }
    guardar_en_bd(card)
```

REUTILIZACIÓN: 100%
├─ Todos los usuarios acceden a las mismas 5000
├─ Algoritmo de repetición espaciada (Anki-style)
├─ Cada usuario progresa independientemente
├─ Mismas tarjetas, progreso distinto

RESULTADO:
├─ Coste: €0 (automatizado desde RAG)
├─ Reutilización: 100%
├─ 1000 usuarios = mismas 5000 tarjetas
└─ Ahorro: 100%
```

### Tipo 4: Resúmenes por Ley ⭐⭐⭐⭐⭐

```
HECHO: Crear 1 resumen por ley importante
├─ LGSS (Ley General Seguridad Social): 1 resumen
├─ Ley de Prevención Riesgos: 1 resumen
├─ 50 leyes principales = 50 resúmenes
├─ Cada resumen: 2-5 páginas comprensas
├─ Coste: 50 × €0.010 = €0.50 (muy barato)

GENERACIÓN:
```python
for ley in leyes_principales:
    resumen = genai.summarize(
        ley['texto_completo'],
        max_length=1500,  # tokens
        focus="conceptos_clave"
    )
    bd.save({
        "ley_id": ley['id'],
        "titulo": ley['titulo'],
        "resumen": resumen,
        "conceptos_clave": extract_concepts(resumen),
        "url_ley": ley['url']
    })
```

REUTILIZACIÓN: 100%
├─ 1000 usuarios acceden al mismo resumen
├─ Búsqueda rápida en BD (vs GeneraI cada vez)
├─ Referencia a artículos específicos
├─ Markdown con índice

RESULTADO:
├─ Coste: €0.50 (total, una sola vez)
├─ 1000 usuarios lo usan
├─ Velocidad: 10ms (vs 5s con GenAI)
└─ Ahorro: 99%
```

### Tipo 5: Memes/Diagramas Explicativos ⭐⭐⭐

```
HECHO: Crear 500 memes/diagramas
├─ Conceptos difíciles → Imagen/diagrama
├─ "El Derecho Laboral es..." → Meme divertido
├─ Flujos (cotización → jubilación)
├─ Árboles de decisión
├─ Coste: 500 × €0.005 (imagen simple) = €2.50

ALMACENAMIENTO: CDN (Cloudinary/Cloudflare Images)
├─ Upload una sola vez
├─ Cache global
├─ Serve a 1000 usuarios sin coste

REUTILIZACIÓN: 100%
├─ Mismo meme para todos
├─ 1000 usuarios = 1 descarga de CDN
├─ Bandwidth casi gratis
└─ Personalizacón: Comentarios/anotaciones por usuario

RESULTADO:
├─ Coste: €2.50 (crear) + €0 (distribuir)
└─ Ahorro: 95%+ (vs generar meme per user)
```

### Tipo 6: Preguntas Frecuentes (FAQs) ⭐⭐⭐

```
HECHO: Crear FAQ página por tema
├─ "¿Cómo se calcula la base de cotización?"
├─ "¿Cuándo prescriben los derechos?"
├─ 100-200 preguntas más comunes
├─ Coste: €0.50 (GenAI crea respuestas)

GENERACIÓN:
```python
common_questions = extract_from_forum_data()  # Preguntas reales
for question in common_questions:
    answer = genai.generate(question)
    bd.save({
        "pregunta": question,
        "respuesta": answer,
        "tema": categorize(question),
        "votos": 0,
        "visto_por": 0
    })
```

REUTILIZACIÓN: 100%
├─ FAQ compartida para todos
├─ Búsqueda rápida por tema
├─ Chat del usuario puede linkear respuestas
└─ Coste: €0 después de crear

RESULTADO:
├─ 1000 usuarios = 1 FAQ compartida
├─ Mejor UX (respuestas consistentes)
└─ Ahorro: 99%
```

---

## 💰 COMPARATIVA: Antes vs Después

### ESCENARIO ACTUAL (Generativo por User)

```
Usuario 8h/día, 120 requests:

Simulacros: 2 por semana × €0.020 = €0.04/sem
Casos: 2 por semana × €0.030 = €0.06/sem
Resúmenes: 1 por mes × €0.010 = €0.002/sem
Flashcards: Automático (€0)
Chat: 110 preguntas × €0.007 = €0.77/sem
─────────────────────────────
TOTAL: €0.872/sem = €3.50/mes por usuario

× 1000 usuarios = €3,500/mes en GenAI
```

### ESCENARIO CON CONTENIDO REUTILIZABLE

```
FASE 1 (Semana 1 - Crear contenido):
├─ Crear 1000 simulacros: €7
├─ Crear 500 casos prácticos: €7.50
├─ Crear 50 resúmenes: €0.50
├─ Crear 5000 flashcards: €0 (automático)
├─ Crear 500 memes: €2.50
├─ Crear FAQs: €0.50
├─ TOTAL SEMANA 1: €18

FASE 2+ (Semana 2 en adelante - Solo servir):
Per usuario:
├─ Simulacros: €0 (BD)
├─ Casos: €0 (BD)
├─ Resúmenes: €0 (BD)
├─ Flashcards: €0 (BD)
├─ Memes: €0 (CDN)
├─ Chat (solo explicaciones): €0.05 (reduced)
─────────────────────────────
TOTAL: €0.05/mes por usuario

× 1000 usuarios = €50/mes en GenAI
```

### AHORRO TOTAL

```
ANTES: €3,500/mes (1000 usuarios)
DESPUÉS: €50/mes (1000 usuarios)

AHORRO: €3,450/mes = 98.6% ✅✅✅

Inversión inicial: €18 (amortizado en <1 día)
ROI: Infinito
```

---

## 🏗️ ARQUITECTURA TÉCNICA

### Base de Datos Schema

```sql
-- Simulacros
CREATE TABLE simulacros (
    id SERIAL PRIMARY KEY,
    tema VARCHAR(100),
    nivel VARCHAR(20),  -- BASICO, INTERMEDIO, AVANZADO
    titulo VARCHAR(255),
    preguntas JSONB,    -- [{"id": 1, "texto": "...", "opciones": [...], "respuesta_correcta": 0}, ...]
    explicaciones JSONB, -- {"1": "La respuesta es porque...", ...}
    fecha_creacion TIMESTAMP,
    version INT DEFAULT 1,
    created_by VARCHAR(50)  -- "sistema", "admin", "usuario_123"
);

-- Casos Prácticos
CREATE TABLE casos_practicos (
    id SERIAL PRIMARY KEY,
    tema VARCHAR(100),
    nivel VARCHAR(20),
    titulo VARCHAR(255),
    hechos TEXT,              -- Descripción del caso
    soluciones JSONB,         -- [{"respuesta": "...", "fundamento": "...", "sentencia": "..."}]
    referencias_articulos ARRAY, -- [12, 45, 67]  -> ID de artículos RAG
    sentencia_referencia VARCHAR(500),
    fecha_creacion TIMESTAMP
);

-- Resúmenes por Ley
CREATE TABLE resumenes_leyes (
    id SERIAL PRIMARY KEY,
    ley_id INT REFERENCES leyes_rag(id),
    titulo VARCHAR(255),
    resumen TEXT,             -- 1500-3000 chars
    conceptos_clave JSONB,    -- {"concepto": "definición", ...}
    url_ley VARCHAR(500),
    fecha_creacion TIMESTAMP,
    fecha_actualizacion TIMESTAMP
);

-- Flashcards
CREATE TABLE flashcards (
    id SERIAL PRIMARY KEY,
    tema VARCHAR(100),
    pregunta TEXT,
    respuesta TEXT,
    explicacion TEXT,
    categoria VARCHAR(100),
    dificultad INT (1-5),
    fecha_creacion TIMESTAMP
);

-- Usuario Progreso (Personalizado)
CREATE TABLE usuario_progreso (
    id SERIAL PRIMARY KEY,
    usuario_id INT,
    tipo_contenido VARCHAR(50), -- 'simulacro', 'flashcard', 'caso'
    contenido_id INT,
    puntuacion INT,
    intentos INT,
    fecha_ultimo_intento TIMESTAMP,
    completado BOOLEAN
);

-- Índices para velocidad
CREATE INDEX idx_simulacros_tema ON simulacros(tema);
CREATE INDEX idx_simulacros_nivel ON simulacros(nivel);
CREATE INDEX idx_casos_tema ON casos_practicos(tema);
CREATE INDEX idx_flashcards_categoria ON flashcards(categoria);
CREATE INDEX idx_usuario_progreso_usuario ON usuario_progreso(usuario_id);
```

### API Endpoints

```python
# backend/routers/contenido_reutilizable.py

from fastapi import APIRouter
from sqlalchemy import select
from db import database, simulacros, casos_practicos, resumenes_leyes

router = APIRouter(prefix="/api/contenido", tags=["contenido"])

@router.get("/simulacros/{tema}/{nivel}")
async def get_simulacro(tema: str, nivel: str, aleatorio: bool = True):
    """Sirve simulacro desde BD (O(1))"""
    query = select(simulacros).where(
        (simulacros.c.tema == tema) & 
        (simulacros.c.nivel == nivel)
    )
    if aleatorio:
        query = query.order_by(func.random()).limit(1)
    
    result = await database.fetch_one(query)
    return {
        "id": result['id'],
        "preguntas": result['preguntas'],  # JSONB
        "explicaciones": result['explicaciones']
    }

@router.get("/casos/{tema}")
async def get_caso(tema: str):
    """Sirve caso práctico desde BD"""
    query = select(casos_practicos).where(
        casos_practicos.c.tema == tema
    ).order_by(func.random()).limit(1)
    
    result = await database.fetch_one(query)
    return result

@router.get("/resumen/{ley_id}")
async def get_resumen(ley_id: int):
    """Sirve resumen pre-calculado"""
    query = select(resumenes_leyes).where(
        resumenes_leyes.c.ley_id == ley_id
    )
    result = await database.fetch_one(query)
    return result

@router.get("/flashcards/{categoria}")
async def get_flashcards(categoria: str, limit: int = 10):
    """Sirve lote de flashcards"""
    query = select(flashcards).where(
        flashcards.c.categoria == categoria
    ).order_by(func.random()).limit(limit)
    
    results = await database.fetch_all(query)
    return results

@router.post("/usuario/{usuario_id}/progreso")
async def registrar_progreso(
    usuario_id: int,
    tipo: str,  # simulacro, flashcard, caso
    contenido_id: int,
    puntuacion: int
):
    """Guarda progreso (personalizado por usuario)"""
    await database.execute(
        usuario_progreso.insert(),
        {
            "usuario_id": usuario_id,
            "tipo_contenido": tipo,
            "contenido_id": contenido_id,
            "puntuacion": puntuacion,
            "intentos": 1,
            "fecha_ultimo_intento": datetime.now()
        }
    )
    return {"status": "ok"}
```

---

## 🎨 CAPA PERSONALIZACIÓN

### Cómo mantener variedad sin perder reutilización

```python
# backend/services/personalizacion_contenido.py

class PersonalizadorContenido:
    """
    Toma contenido reutilizable y lo personaliza por usuario
    sin regenerar (ahorro total)
    """
    
    def personalizar_simulacro(self, usuario_id: int, simulacro_base: dict):
        """
        Simulacro base: [Q1, Q2, Q3, ...]
        Usuario A: [Q1, Q2, Q3, Q4, ...] (orden 1)
        Usuario B: [Q3, Q1, Q4, Q2, ...] (orden 2)
        Usuario C: [Q2, Q4, Q1, Q3, ...] (orden 3)
        """
        preguntas = simulacro_base['preguntas']
        
        # Mezclar preguntas por usuario (determinístico)
        random.seed(hash(usuario_id))  # Seed por usuario
        preguntas_mezcladas = random.sample(preguntas, len(preguntas))
        
        return {
            **simulacro_base,
            "preguntas": preguntas_mezcladas
        }
    
    def variar_caso_practico(self, usuario_id: int, caso_base: dict):
        """
        Caso base: "María trabaja en empresa X, sueldo Y, años Z"
        Usuario A: "María trabaja en empresa X, sueldo Y, años Z"
        Usuario B: "Juan trabaja en empresa A, sueldo B, años C"
        (mismo caso, nombres/números cambiados)
        """
        hechos = caso_base['hechos']
        
        # Cambiar nombres (determinístico por usuario)
        nombres = ["María", "Juan", "Ana", "Carlos", "Elena"]
        nombre_idx = hash(usuario_id) % len(nombres)
        hechos_variado = hechos.replace("María", nombres[nombre_idx])
        
        # Cambiar números levemente (+/-10%)
        numbers = re.findall(r'\d+', hechos)
        for num in numbers:
            variation = random.randint(-10, 10)
            nuevo_num = int(num) + variation
            hechos_variado = hechos_variado.replace(num, str(nuevo_num), 1)
        
        return {
            **caso_base,
            "hechos": hechos_variado
        }
    
    def mezclar_preguntas_por_tema(self, usuario_id: int, tema: str, cantidad: int):
        """
        En lugar de crear preguntas nuevas,
        mezcla preguntas existentes de ese tema
        """
        # Obtener todas las preguntas del tema
        preguntas_tema = bd.query(
            "SELECT * FROM flashcards WHERE categoria = ?",
            (tema,)
        )
        
        # Seleccionar cantidad aleatoria (determinística)
        random.seed(hash((usuario_id, tema)))
        seleccionadas = random.sample(preguntas_tema, min(cantidad, len(preguntas_tema)))
        
        return seleccionadas
```

---

## 📈 GENERACIÓN INICIAL: Proceso Automático

### Pipeline de Creación (Ejecutar UNA VEZ)

```python
# backend/tasks/generar_contenido_reutilizable.py

import asyncio
from services.gemini_service import gemini_client

async def generar_contenido_inicial():
    """
    Ejecutar una sola vez para llenar la BD
    Costo: ~€20 (amortizado en <1 hora de uso)
    """
    
    print("📊 Iniciando generación de contenido reutilizable...")
    
    # FASE 1: Obtener temas del RAG
    temas = await qdrant.get_all_themes()  # [Seguridad Social, Derecho Laboral, ...]
    
    # FASE 2: Generar simulacros (1000 total)
    print("📝 Generando 1000 simulacros...")
    for tema in temas:
        for nivel in ["BASICO", "INTERMEDIO", "AVANZADO"]:
            for num in range(6):  # 6 simulacros por (tema, nivel) = 18 × 50 = 900
                simulacro = await generar_simulacro_tema(tema, nivel)
                await bd.save_simulacro(simulacro)
    
    # FASE 3: Generar casos prácticos (500)
    print("🏛️ Generando 500 casos prácticos...")
    for tema in temas:
        for num in range(10):  # 10 casos por tema = 500
            caso = await generar_caso_practico_tema(tema)
            await bd.save_caso(caso)
    
    # FASE 4: Generar resúmenes (50)
    print("📚 Generando 50 resúmenes...")
    for ley in temas:
        resumen = await generar_resumen_ley(ley)
        await bd.save_resumen(resumen)
    
    # FASE 5: Flashcards (5000, casi automático)
    print("🎴 Generando 5000 flashcards...")
    for concepto in rag_conceptos:  # Extraído del RAG automáticamente
        flashcard = {
            "pregunta": f"¿Qué es {concepto}?",
            "respuesta": rag_definiciones[concepto],
            "categoria": rag_temas[concepto]
        }
        await bd.save_flashcard(flashcard)
    
    print("✅ Contenido reutilizable listo!")

async def generar_simulacro_tema(tema: str, nivel: str) -> dict:
    """Generar 1 simulacro (30-50 preguntas)"""
    
    # Obtener contexto del RAG para este tema/nivel
    contexto = await qdrant.search(tema, filters={"nivel": nivel})
    
    prompt = f"""
    Genera un simulacro de examen sobre {tema} nivel {nivel}.
    
    Contexto:
    {contexto}
    
    Formato JSON:
    {{
        "tema": "{tema}",
        "nivel": "{nivel}",
        "preguntas": [
            {{"id": 1, "texto": "Pregunta 1?", "opciones": ["A", "B", "C", "D"], "respuesta_correcta": 0}},
            ...
        ],
        "explicaciones": {{"1": "Explicación pregunta 1", ...}}
    }}
    """
    
    response = await gemini_client.generate(prompt)
    return json.loads(response)

# Ejecutar:
# asyncio.run(generar_contenido_inicial())
```

---

## 🎯 NUEVA ARQUITECTURA DE COSTES

### Por Tipo de Interacción

```
USUARIO PIDE "SIMULACRO":
├─ Buscar en BD (O(1)): 50ms, €0
├─ Personalizar (mezclar): 10ms, €0
├─ Servir: 50ms, €0
└─ TOTAL: 110ms, €0 ✅

USUARIO PIDE "CASO PRÁCTICO":
├─ Buscar en BD: 50ms, €0
├─ Variar números/nombres: 10ms, €0
├─ Servir: 50ms, €0
└─ TOTAL: 110ms, €0 ✅

USUARIO PREGUNTA EN CHAT "¿Por qué es la respuesta C?"
├─ Buscar en BD (explicación pre-calculada): 10ms, €0
├─ SI no está → Generar con GenAI: 2s, €0.005
└─ TOTAL: 10ms, €0 (95% casos) ✅

USUARIO PIDE RESUMEN LGSS:
├─ Buscar en BD: 30ms, €0
├─ Servir: 50ms, €0
└─ TOTAL: 80ms, €0 ✅

USUARIO QUERRÍA CREAR CONTENIDO NUEVO (1% casos):
└─ Generar con GenAI: 3s, €0.010
```

---

## 📊 IMPACTO EN NÚMEROS

### Coste por Usuario

```
ANTES (GenAI por cada request):
├─ Simulacros: 2/sem × €0.020 = €0.04/sem
├─ Casos: 2/sem × €0.030 = €0.06/sem
├─ Resúmenes: 1/mes × €0.010 = €0.002/sem
├─ Chat: 110 reqs × €0.007 = €0.77/sem
└─ TOTAL: €0.872/sem = €3.50/mes

DESPUÉS (Contenido reutilizable):
├─ Simulacros: €0 (BD)
├─ Casos: €0 (BD)
├─ Resúmenes: €0 (BD)
├─ Chat: 110 reqs × €0.0005 (solo explicaciones) = €0.055/sem
└─ TOTAL: €0.055/sem = €0.22/mes

AHORRO: 94% ✅✅✅
```

### Escalabilidad

```
100 usuarios:
├─ Contenido reutilizable creado: €18 (una sola vez)
├─ Coste IA/mes: €22 (solo chat)
├─ Margen: 99.3%

500 usuarios:
├─ Contenido reutilizable creado: €18 (ya pagado)
├─ Coste IA/mes: €110 (solo chat)
├─ Margen: 99.6%

1,000 usuarios:
├─ Contenido reutilizable creado: €18 (ya pagado)
├─ Coste IA/mes: €220 (solo chat)
├─ Margen: 99.7%

10,000 usuarios:
├─ Contenido reutilizable creado: €18 (ya pagado)
├─ Coste IA/mes: €2,200 (solo chat)
├─ Margen: 99.9%
```

---

## 🔄 MANTENIMIENTO Y ACTUALIZACIÓN

### Cómo mantener contenido fresco sin regenerar todo

```
OPCIÓN 1: Versiones (Non-destructive)
├─ Crear simulacro v1
├─ Crear simulacro v2 (nuevas preguntas)
├─ Usuarios pueden elegir versión
└─ Reutilización: 95%+

OPCIÓN 2: Rotación
├─ Semana 1-2: Mostrar simulacros v1
├─ Semana 3-4: Mostrar simulacros v2
├─ Semana 5+: Mezcla aleatoria
└─ Reutilización: 100%

OPCIÓN 3: Actualización Legal
├─ Ley cambia → Actualizar resumen (€0.005)
├─ Generar casos con nueva ley (€0.010)
├─ El resto del contenido no cambia
└─ Reutilización: 95%

COSTO DE MANTENIMIENTO:
├─ Crear nuevas versiones: €10/mes (más simulacros)
├─ Actualizar con cambios legales: €5/mes
├─ TOTAL: €15/mes (amortizado en 1000 usuarios = €0.015/user)
```

---

## ✅ CHECKLIST IMPLEMENTACIÓN

### FASE 1: Setup BD (1 semana)

```
- [ ] Diseñar schema PostgreSQL
- [ ] Crear tablas (simulacros, casos, etc)
- [ ] Crear índices
- [ ] Setup connection pool
- [ ] Tests de velocidad (< 100ms lectura)
```

### FASE 2: Generación Inicial (1 semana)

```
- [ ] Script para generar 1000 simulacros
- [ ] Script para generar 500 casos
- [ ] Script para generar 50 resúmenes
- [ ] Extraer 5000 flashcards del RAG
- [ ] Validar calidad (muestreo)
- [ ] Estimado: €18 en GenAI
```

### FASE 3: APIs y Personalización (1 semana)

```
- [ ] Endpoints /api/contenido/*
- [ ] Personalización (mezcla, variación)
- [ ] Tracking de progreso (usuario_progreso)
- [ ] Recomendaciones basadas en progreso
```

### FASE 4: Frontend Integration (1 semana)

```
- [ ] UI para simulacros
- [ ] UI para casos prácticos
- [ ] UI para resúmenes
- [ ] Flashcard widget
- [ ] Analytics de uso
```

### FASE 5: Mantenimiento (Ongoing)

```
- [ ] Monitorear BD performance
- [ ] Actualizar contenido mensual
- [ ] Agregar nuevas versiones
- [ ] A/B testing
```

---

## 🎯 COMPARATIVA: Caché vs Contenido Reutilizable

```
┌─────────────────────────────────────────────────┐
│ CACHÉ (Redis)                                   │
├─────────────────────────────────────────────────┤
│ ✅ Rápido de implementar (1 semana)             │
│ ✅ Ahorr: 60% (si hit rate 60%)                │
│ ❌ Solo cachea preguntas hechas antes           │
│ ❌ Limitado a 256MB (free tier)                │
│ ❌ TTL de 30 días (se expira)                  │
│ └─ Coste: €0.46/mes (con cache 60%)           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ CONTENIDO REUTILIZABLE (Base de Datos)          │
├─────────────────────────────────────────────────┤
│ ✅ Ahorro: 94% (permanente)                    │
│ ✅ Escalable (sin límite de tamaño)             │
│ ✅ Permanente (no expira)                       │
│ ✅ Personalizable (variaciones)                 │
│ ✅ Mejor UX (contenido consistente)             │
│ ⚠️ Setup inicial (2 semanas)                    │
│ └─ Coste: €0.22/mes (después de creación)     │
└─────────────────────────────────────────────────┘

RECOMENDACIÓN: Ambas
├─ Caché para queries de chat (rápido)
├─ Contenido Reutilizable para simulacros/casos
└─ Combinadas: 94% ahorro total ✅
```

---

## 🚀 ROADMAP INTEGRADO

### Semana 1: Caché + Contenido Setup

```
├─ Implement Redis Caché (4 días)
├─ Setup BD PostgreSQL (2 días)
└─ Deploy canary (1 día)
```

### Semana 2-3: Generar Contenido

```
├─ Generar 1000 simulacros (2 días)
├─ Generar 500 casos (1 día)
├─ Generar resúmenes + flashcards (1 día)
└─ Testing y validación (2 días)
```

### Semana 4: Personalización + Integración

```
├─ APIs de personalización (2 días)
├─ Frontend integration (2 días)
└─ Deploy a producción (1 día)
```

### Semana 5+: Mantenimiento y Optimización

```
├─ Monitoreo de BD
├─ Actualizaciones mensuales
├─ Análisis de uso
└─ Mejoras iterativas
```

---

## 💎 RESULTADO FINAL

```
ARQUITECTURA COMPLETA (3 capas):

┌─────────────────────────────────────────────────┐
│ 1. CACHÉ (Redis)                               │
│    └─ Preguntas frecuentes en chat             │
│    └─ Hit rate: 60-70%                         │
│    └─ Velocidad: 50ms                          │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 2. CONTENIDO REUTILIZABLE (PostgreSQL)          │
│    ├─ 1000 simulacros                          │
│    ├─ 500 casos prácticos                      │
│    ├─ 50 resúmenes leyes                       │
│    ├─ 5000 flashcards                          │
│    └─ Velocidad: 100ms                         │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 3. CHAT EXPLICATIVO (GenAI bajo demanda)       │
│    └─ Solo para preguntas nuevas/dudas         │
│    └─ 5% del uso                               │
│    └─ Velocidad: 3s                            │
└─────────────────────────────────────────────────┘

RESULTADO:
├─ Coste IA: €1.14 → €0.22/mes (81% ahorro)
├─ Velocidad promedio: 150-200ms (excelente)
├─ Escalabilidad: Infinita
├─ Margen: 99.3%
└─ ✅ MODELO SOSTENIBLE A ESCALA
```

---

**Creado**: 28 Noviembre 2025  
**Estrategia**: Contenido Reutilizable + BD  
**Ahorro**: 94%
**Timeline**: 4-5 semanas
**Resultado**: €0.22/mes por usuario

