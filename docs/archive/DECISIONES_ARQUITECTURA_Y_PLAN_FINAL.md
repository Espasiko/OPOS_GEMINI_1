# 🎯 DECISIONES DE ARQUITECTURA Y PLAN FINAL - OpositaIA

**Fecha:** 26 Noviembre 2025  
**Objetivo:** Definir arquitectura técnica y modificaciones al plan de desarrollo

---

## 📋 ÍNDICE

1. [Respuestas a Preguntas Iniciales](#1-respuestas-a-preguntas-iniciales)
2. [Story 2.2: Algoritmo Adaptativo](#2-story-22-algoritmo-adaptativo)
3. [Story 4.1: RAG Adaptativo - Evaluación BD](#3-story-41-rag-adaptativo)
4. [Story 4.2: Gestión Documentos - Comparativa](#4-story-42-gestión-documentos)
5. [Story 4.3: Búsqueda Web - Comparativa APIs](#5-story-43-búsqueda-web)
6. [Herramientas Seguridad - Aikido vs Semgrep](#6-herramientas-seguridad)
7. [Arquitectura Deployment - Cálculo Espacio VPS](#7-arquitectura-deployment)
8. [Dockerización - Cuándo y Cómo](#8-dockerización)
9. [Firebase vs Vercel - Análisis Completo](#9-firebase-vs-vercel)
10. [Resumen Decisiones y Próximos Pasos](#10-resumen-decisiones)

---

## 1. RESPUESTAS A PREGUNTAS INICIALES

### ✅ PREGUNTA 1: Número de Preguntas por Examen

**Respuesta recibida:**
- **Administrativo (C1):** 70 preguntas test + 15 preguntas caso práctico = **85 total**
- **Gestión (A2) - Acceso Libre:** 90 preguntas test
- **Gestión (A2) - Promoción Interna:** 60 preguntas test

**Decisión para el algoritmo:**
- Simulacro completo = mínimo 60 preguntas (el más pequeño)
- Para evaluación precisa: 3-4 simulacros = 180-240 respuestas mínimo
- Tests de práctica (<60 preguntas) NO cuentan para ajuste de dificultad

---

### ✅ PREGUNTA 2: Estado Actual de la Base de Datos

**Análisis del esquema (backend/database/schema.sql):**


**Tablas existentes:**
1. ✅ `user_progress` - Progreso general del usuario
2. ✅ `answer_history` - Historial de respuestas
3. ✅ `user_cases` - Casos prácticos creados
4. ✅ `simulacros` - Resultados de simulacros
5. ✅ `mind_maps` - Mapas mentales (JSONB)
6. ✅ `study_sessions` - Sesiones de estudio
7. ✅ `recommendations` - Recomendaciones IA
8. ✅ `rag_queries` - Queries RAG para análisis

**Campos clave para algoritmo adaptativo:**
```sql
-- user_progress
total_preguntas INTEGER
total_correctas INTEGER
precision_global FLOAT
temas_debiles INTEGER[]

-- answer_history
es_correcta BOOLEAN
tema_id INTEGER
dificultad VARCHAR(50)
created_at TIMESTAMP

-- simulacros
puntuacion FLOAT
preguntas_correctas INTEGER
preguntas_totales INTEGER
resultados_detallados JSONB
```

**Conclusión:** ✅ La BD ya tiene TODO lo necesario para el algoritmo adaptativo.

---

### ✅ PREGUNTA 3: Información de Progreso para RAG

**Respuesta:** Las tres cosas:
1. Temas ya estudiados
2. Temas con más errores
3. Leyes que el usuario domina vs las que no

**Implementación:**
- Agente evaluador que analiza `user_performance_by_topic` (view ya existe)
- Filtra resultados RAG según nivel del usuario
- Prioriza contenido de temas débiles

---

### ✅ PREGUNTA 4: Evaluación Tamaño BD

**Datos a almacenar por usuario:**
- Historial chats
- Exámenes completados
- Tests realizados
- Mapas mentales
- Esquemas
- Gamificaciones

**Cálculo detallado en sección 7** ⬇️

---

## 2. STORY 2.2: ALGORITMO ADAPTATIVO

### ✅ APROBADO: Lógica de 3-4 Simulacros Mínimo

**Justificación:**
- Simulacro más pequeño: 60 preguntas (Gestión Promoción Interna)
- 3 simulacros = 180 respuestas (muestra estadísticamente significativa)
- 4 simulacros = 240 respuestas (ideal para precisión)

### ✅ APROBADO: Nota de Corte 8.5/10

**Confirmación:** Nota de corte real en última convocatoria = 8.5/10 (85%)

### 📝 MODIFICACIÓN COMPLETA Story 2.2

```markdown
#### Story 2.2: Algoritmo Adaptativo Mejorado

**Como** sistema  
**Quiero** ajustar dificultad según historial de simulacros completos  
**Para** optimizar aprendizaje y calcular probabilidad de aprobar

**Contexto ACTUALIZADO:**
- Simulacros oficiales: 60-90 preguntas según cuerpo
- Evaluación precisa requiere mínimo 3-4 simulacros completos (180-240 respuestas)
- Tests de práctica (<60 preguntas) NO se consideran para ajuste
- Nota de corte real: 8.5/10 (85%) en última convocatoria
- Sistema calcula probabilidad de aprobar basada en progreso

**Criterios de Aceptación:**
- [ ] Calcula dificultad basada en últimos 3-4 simulacros completos (≥60 preguntas)
- [ ] Ignora tests de práctica (<60 preguntas) para cálculo de nivel
- [ ] Clasifica usuario en 3 niveles con probabilidad de aprobar:
  - **Nivel Inicial:** <60% aciertos → Probabilidad aprobar <20%
  - **Nivel Intermedio:** 60-85% aciertos → Probabilidad aprobar 20-70%
  - **Nivel Avanzado:** >85% aciertos → Probabilidad aprobar >70%
- [ ] Dashboard muestra:
  - Nivel actual del usuario
  - Simulacros completos realizados
  - Probabilidad de aprobar (%)
  - Gráfico de evolución
  - Recomendación personalizada
- [ ] Alerta si usuario intenta simulacro difícil sin suficiente historial
- [ ] Logging de decisiones para análisis

**Lógica de Cálculo:**
```python
def calculate_adaptive_difficulty(user_id: str) -> dict:
    """
    Calcula nivel adaptativo y probabilidad de aprobar
    basado en últimos 3-4 simulacros completos
    """
    # 1. Obtener últimos simulacros completos (≥60 preguntas)
    simulacros = db.query("""
        SELECT puntuacion, preguntas_correctas, preguntas_totales, created_at
        FROM simulacros
        WHERE user_id = %s 
          AND preguntas_totales >= 60
        ORDER BY created_at DESC
        LIMIT 4
    """, (user_id,))
    
    # 2. Verificar datos suficientes
    if len(simulacros) < 3:
        return {
            'level': 'insufficient_data',
            'message': f'Completa al menos 3 simulacros (tienes {len(simulacros)})',
            'simulacros_needed': 3 - len(simulacros),
            'probability_pass': None,
            'recommendation': 'Realiza más simulacros para evaluación precisa'
        }
    
    # 3. Calcular % aciertos promedio
    total_correct = sum(s['preguntas_correctas'] for s in simulacros)
    total_questions = sum(s['preguntas_totales'] for s in simulacros)
    accuracy = (total_correct / total_questions) * 100
    
    # 4. Calcular probabilidad de aprobar (nota corte 85%)
    if accuracy >= 85:
        # Usuario avanzado: alta probabilidad
        probability_pass = 70 + min((accuracy - 85) * 2, 30)  # 70-100%
        level = 'avanzado'
        difficulty = 'difícil'
        recommendation = '¡Excelente! Estás listo para el examen oficial'
        
    elif accuracy >= 60:
        # Usuario intermedio: probabilidad media
        probability_pass = 20 + ((accuracy - 60) / 25) * 50  # 20-70%
        level = 'intermedio'
        difficulty = 'media'
        recommendation = 'Sigue practicando, vas por buen camino'
        
    else:
        # Usuario inicial: baja probabilidad
        probability_pass = (accuracy / 60) * 20  # 0-20%
        level = 'inicial'
        difficulty = 'fácil'
        recommendation = 'Refuerza conceptos básicos antes de simulacros'
    
    # 5. Calcular tendencia (mejorando/empeorando)
    if len(simulacros) >= 3:
        recent_avg = sum(s['puntuacion'] for s in simulacros[:2]) / 2
        older_avg = sum(s['puntuacion'] for s in simulacros[2:]) / len(simulacros[2:])
        trend = 'mejorando' if recent_avg > older_avg else 'estable' if recent_avg == older_avg else 'empeorando'
    else:
        trend = 'insuficiente_data'
    
    return {
        'level': level,
        'difficulty': difficulty,
        'accuracy': round(accuracy, 2),
        'probability_pass': round(min(probability_pass, 100), 2),
        'simulacros_completed': len(simulacros),
        'total_questions_answered': total_questions,
        'trend': trend,
        'recommendation': recommendation,
        'next_steps': get_next_steps(level, accuracy, trend)
    }

def get_next_steps(level: str, accuracy: float, trend: str) -> list:
    """Genera recomendaciones personalizadas"""
    steps = []
    
    if level == 'inicial':
        steps.append('Estudia temas básicos: Constitución, LGSS Título I')
        steps.append('Practica tests cortos (10-20 preguntas)')
        steps.append('Revisa errores frecuentes')
    
    elif level == 'intermedio':
        steps.append('Enfócate en temas débiles')
        steps.append('Realiza casos prácticos')
        if trend == 'empeorando':
            steps.append('⚠️ Revisa conceptos que dominabas antes')
    
    else:  # avanzado
        steps.append('Simula condiciones de examen real')
        steps.append('Practica gestión del tiempo')
        steps.append('Repasa jurisprudencia reciente')
    
    return steps
```

**Estimación:** 8 horas (aumentado de 5h)  
**Prioridad:** 🔴 Crítica

**Testing:**
```python
# test_adaptive_algorithm.py
def test_insufficient_data():
    # Usuario con 2 simulacros → debe pedir más
    result = calculate_adaptive_difficulty(user_with_2_simulacros)
    assert result['level'] == 'insufficient_data'
    assert result['simulacros_needed'] == 1

def test_nivel_inicial():
    # Usuario con 50% aciertos → nivel inicial
    result = calculate_adaptive_difficulty(user_with_50_percent)
    assert result['level'] == 'inicial'
    assert result['probability_pass'] < 20

def test_nivel_avanzado():
    # Usuario con 90% aciertos → nivel avanzado
    result = calculate_adaptive_difficulty(user_with_90_percent)
    assert result['level'] == 'avanzado'
    assert result['probability_pass'] > 70
```
```

---

## 3. STORY 4.1: RAG ADAPTATIVO

### 🤔 DECISIÓN PENDIENTE: PostgreSQL vs PostgreSQL + MongoDB/Neon



### 📊 COMPARATIVA DETALLADA

#### Opción A: PostgreSQL para TODO ⭐⭐⭐⭐⭐

**Arquitectura:**
```
PostgreSQL (Una sola BD):
├── Tablas relacionales (users, progress, sessions)
├── Columnas JSONB (mind_maps.contenido, simulacros.resultados_detallados)
└── Arrays (temas_completados[], temas_debiles[])
```

**✅ VENTAJAS:**
1. **Simplicidad:** Una sola BD, un solo backup, una sola conexión
2. **Transacciones ACID:** Consistencia garantizada
3. **Ya implementado:** Tu schema.sql ya usa JSONB para objetos complejos
4. **Queries potentes:** Puedes hacer JOIN entre datos relacionales y JSON
5. **Sin latencia adicional:** Todo en el mismo servidor
6. **Gratis:** Sin costes adicionales
7. **GDPR friendly:** Datos en tu servidor EU

**❌ DESVENTAJAS:**
1. **Escalabilidad:** Si creces mucho, PostgreSQL puede ser más lento con JSONB masivo
2. **Backups:** Backups más grandes (incluyen todo)

**💰 COSTE:**
- Setup: 0€
- Mensual: 0€ (incluido en VPS)
- Complejidad: Baja

**📊 RENDIMIENTO:**
- Queries JSONB: 10-50ms (rápido)
- Escalabilidad: Hasta 10,000 usuarios sin problemas

---

#### Opción B: PostgreSQL + MongoDB Atlas ⭐⭐⭐

**Arquitectura:**
```
PostgreSQL (Datos relacionales):
├── users
├── user_progress
├── answer_history
└── simulacros (solo metadata)

MongoDB Atlas (Documentos):
├── chat_history (conversaciones completas)
├── mind_maps (grafos complejos)
├── study_sessions (actividades detalladas)
└── user_documents (contenido temporal)
```

**✅ VENTAJAS:**
1. **Escalabilidad horizontal:** MongoDB escala mejor con documentos grandes
2. **Flexible:** Esquema dinámico para datos no estructurados
3. **Free tier:** 512MB gratis (suficiente para 50-100 usuarios)
4. **Backups automáticos:** MongoDB Atlas hace backups diarios
5. **Especializado:** MongoDB es mejor para documentos complejos

**❌ DESVENTAJAS:**
1. **Complejidad:** Dos BDs, dos conexiones, dos backups
2. **Latencia:** 50-100ms adicional (MongoDB en cloud)
3. **Consistencia:** No hay transacciones entre PostgreSQL y MongoDB
4. **Dependencia externa:** Si MongoDB cae, pierdes funcionalidad
5. **GDPR:** Datos fuera de tu servidor (aunque MongoDB tiene región EU)
6. **Coste futuro:** Después de 512MB, €9/mes

**💰 COSTE:**
- Setup: 2-3 horas configuración
- Mensual: 0€ (hasta 512MB) → €9/mes (después)
- Complejidad: Media-Alta

**📊 RENDIMIENTO:**
- Queries MongoDB: 50-150ms (más lento por red)
- Escalabilidad: Hasta 100,000 usuarios

---

#### Opción C: PostgreSQL + Neon (PostgreSQL Cloud) ⭐⭐⭐⭐

**Arquitectura:**
```
PostgreSQL Local (Datos críticos):
├── users
├── user_progress
├── answer_history
└── simulacros

Neon PostgreSQL Cloud (Objetos):
├── chat_history (JSONB)
├── mind_maps (JSONB)
├── study_sessions (JSONB)
└── user_documents (JSONB)
```

**✅ VENTAJAS:**
1. **Mismo lenguaje:** SQL en ambas BDs (fácil de mantener)
2. **Free tier generoso:** 3GB gratis (suficiente para 500 usuarios)
3. **Backups automáticos:** Neon hace backups diarios
4. **Serverless:** Escala automáticamente
5. **Región EU:** Datos en Europa (GDPR compliant)
6. **Branching:** Puedes crear "ramas" de BD para testing

**❌ DESVENTAJAS:**
1. **Complejidad:** Dos BDs PostgreSQL (puede confundir)
2. **Latencia:** 30-80ms adicional (Neon en cloud)
3. **Consistencia:** No hay transacciones entre ambas BDs
4. **Dependencia externa:** Si Neon cae, pierdes funcionalidad

**💰 COSTE:**
- Setup: 1-2 horas configuración
- Mensual: 0€ (hasta 3GB) → €19/mes (después)
- Complejidad: Media

**📊 RENDIMIENTO:**
- Queries Neon: 30-100ms (rápido para cloud)
- Escalabilidad: Hasta 50,000 usuarios

---

### 🎯 MI RECOMENDACIÓN

**Para MVP (0-100 usuarios):**
### ✅ OPCIÓN A: PostgreSQL para TODO

**Razones:**
1. **Ya está implementado:** Tu schema.sql ya usa JSONB
2. **Más simple:** Una BD, un backup, menos complejidad
3. **Más rápido:** Sin latencia de red
4. **Gratis:** Sin costes adicionales
5. **GDPR:** Datos en tu servidor EU
6. **Suficiente:** PostgreSQL JSONB maneja 10,000 usuarios sin problemas

**Para Producción (100-1000 usuarios):**
### ⭐ OPCIÓN C: PostgreSQL + Neon

**Razones:**
1. **Escalabilidad:** Neon escala automáticamente
2. **Backups:** Automáticos en Neon
3. **Mismo lenguaje:** SQL en ambas (fácil)
4. **Free tier:** 3GB gratis (suficiente para 500 usuarios)
5. **Migración fácil:** Solo mover tablas de objetos a Neon

**NO recomiendo Opción B (MongoDB):**
- Más complejo (dos lenguajes: SQL + MongoDB)
- Free tier pequeño (512MB vs 3GB de Neon)
- Menos familiar para ti

---

### 📝 PLAN DE MIGRACIÓN (Cuando crezcas)

**Fase 1: MVP (Ahora)**
```sql
-- Todo en PostgreSQL local
CREATE TABLE mind_maps (
    contenido JSONB  -- Funciona perfecto
);
```

**Fase 2: Producción (Cuando tengas 100+ usuarios)**
```sql
-- PostgreSQL Local (datos críticos)
users, user_progress, answer_history, simulacros

-- Neon Cloud (objetos grandes)
chat_history, mind_maps, study_sessions, user_documents
```

**Migración:**
```bash
# 1. Crear cuenta Neon (gratis)
# 2. Exportar tablas de objetos
pg_dump -t chat_history -t mind_maps > objetos.sql

# 3. Importar a Neon
psql $NEON_URL < objetos.sql

# 4. Actualizar backend (dos conexiones)
DB_LOCAL = "postgresql://localhost/opositaia"
DB_NEON = "postgresql://neon.tech/opositaia_objects"
```

---

## 4. STORY 4.2: GESTIÓN DOCUMENTOS

### 🤔 DECISIÓN PENDIENTE: Google Drive vs Temporal vs Híbrido

### 📊 COMPARATIVA DETALLADA

#### Opción A: Google Drive del Usuario ⭐⭐⭐⭐

**Cómo funciona:**
1. Usuario hace clic en "Conectar Google Drive"
2. OAuth2 flow: usuario autoriza acceso a su Drive
3. App lista documentos del Drive del usuario
4. Agente lee documentos en tiempo real desde Drive
5. Documentos NO se almacenan en tu BD

**✅ VENTAJAS:**
1. **Sin almacenamiento:** No usas espacio en tu servidor
2. **GDPR perfecto:** No almacenas datos personales
3. **Sin límites:** Usuario tiene todo el espacio de su Drive
4. **Persistencia:** Documentos persisten entre sesiones
5. **Control del usuario:** Usuario controla sus datos
6. **Sincronización:** Si usuario actualiza doc en Drive, app lo ve

**❌ DESVENTAJAS:**
1. **Complejidad OAuth2:** Implementación compleja (4-6 horas)
2. **Dependencia Google:** Si Google cae, no funciona
3. **Permisos:** Usuario debe autorizar (puede rechazar)
4. **Latencia:** Leer desde Drive es más lento (200-500ms)
5. **Cuota API:** Google Drive API tiene límites (10,000 requests/día gratis)

**💰 COSTE:**
- Setup: 6 horas desarrollo
- Mensual: 0€ (API gratis hasta 10,000 requests/día)
- Complejidad: Alta

**🔧 IMPLEMENTACIÓN:**
```python
# backend/services/google_drive_service.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GoogleDriveService:
    def __init__(self, user_credentials):
        self.creds = Credentials.from_authorized_user_info(user_credentials)
        self.service = build('drive', 'v3', credentials=self.creds)
    
    def list_documents(self, folder_id=None):
        """Lista documentos del Drive del usuario"""
        query = "mimeType='application/pdf' or mimeType='text/plain'"
        results = self.service.files().list(
            q=query, 
            pageSize=100,
            fields="files(id, name, mimeType, modifiedTime)"
        ).execute()
        return results.get('files', [])
    
    def read_document(self, file_id):
        """Lee contenido de documento"""
        request = self.service.files().get_media(fileId=file_id)
        content = request.execute()
        return content
```

**Frontend:**
```typescript
// components/GoogleDriveConnect.tsx
const handleConnectDrive = async () => {
  // 1. Redirect a Google OAuth
  window.location.href = `${API_URL}/auth/google/authorize`;
  
  // 2. Google redirige de vuelta con token
  // 3. Backend guarda token encriptado
  // 4. Usuario ve sus documentos
};
```

---

#### Opción B: Documentos Temporales (Sin Persistencia) ⭐⭐⭐⭐⭐

**Cómo funciona:**
1. Usuario sube documento (PDF, TXT, DOCX)
2. Backend procesa y guarda en memoria/Redis
3. Agente puede leer documento durante la sesión
4. Al cerrar sesión, documento se borra automáticamente

**✅ VENTAJAS:**
1. **Simplicidad extrema:** Ya tienes upload implementado
2. **Sin OAuth:** No necesitas autenticación externa
3. **Rápido:** Documentos en memoria (0-10ms acceso)
4. **GDPR perfecto:** No almacenas nada permanentemente
5. **Sin límites API:** No dependes de servicios externos
6. **Privacidad:** Usuario sabe que no persiste

**❌ DESVENTAJAS:**
1. **No persiste:** Usuario debe re-subir cada sesión
2. **Memoria:** Documentos ocupan RAM (limitado)
3. **Sin sincronización:** Si usuario actualiza doc, debe re-subir

**💰 COSTE:**
- Setup: 1 hora (ya casi implementado)
- Mensual: 0€
- Complejidad: Muy Baja

**🔧 IMPLEMENTACIÓN:**
```python
# backend/routers/upload.py (ya existe, solo añadir)
from fastapi import UploadFile
import redis

redis_client = redis.Redis(host='localhost', port=6379)

@router.post("/upload/temporary")
async def upload_temporary_document(
    file: UploadFile,
    session_id: str
):
    """
    Sube documento temporal (solo para esta sesión)
    """
    # 1. Leer contenido
    content = await file.read()
    
    # 2. Guardar en Redis con TTL (expira en 24h)
    key = f"temp_doc:{session_id}:{file.filename}"
    redis_client.setex(
        key,
        86400,  # 24 horas
        content
    )
    
    # 3. Procesar para RAG (opcional)
    if process_for_rag:
        chunks = chunk_document(content)
        # Indexar en Qdrant con metadata temporal
    
    return {
        "filename": file.filename,
        "size": len(content),
        "expires_in": "24 hours",
        "warning": "Este documento no persiste entre sesiones"
    }

@router.get("/documents/temporary/{session_id}")
async def list_temporary_documents(session_id: str):
    """Lista documentos temporales de la sesión"""
    pattern = f"temp_doc:{session_id}:*"
    keys = redis_client.keys(pattern)
    
    documents = []
    for key in keys:
        filename = key.decode().split(':')[-1]
        ttl = redis_client.ttl(key)
        documents.append({
            "filename": filename,
            "expires_in_seconds": ttl
        })
    
    return {"documents": documents}
```

**Frontend:**
```typescript
// components/TemporaryUpload.tsx
const TemporaryUpload = () => {
  return (
    <div className="upload-zone">
      <p className="warning">
        ⚠️ Los documentos subidos NO persisten entre sesiones.
        Se borrarán automáticamente en 24 horas.
      </p>
      <input type="file" onChange={handleUpload} />
      <p className="info">
        💡 Para documentos permanentes, conecta tu Google Drive
      </p>
    </div>
  );
};
```

---

#### Opción C: Híbrido (Google Drive + Temporal) ⭐⭐⭐⭐⭐

**Cómo funciona:**
1. Usuario elige: "Conectar Drive" o "Subir temporal"
2. Si conecta Drive: documentos persisten
3. Si sube temporal: documentos se borran en 24h
4. Agente puede leer de ambas fuentes

**✅ VENTAJAS:**
1. **Flexibilidad:** Usuario elige según necesidad
2. **Mejor UX:** Opción rápida (temporal) + opción permanente (Drive)
3. **Conversión:** Usuarios que prueban temporal pueden migrar a Drive
4. **GDPR:** Ambas opciones son compliant

**❌ DESVENTAJAS:**
1. **Complejidad:** Implementar ambas opciones
2. **Mantenimiento:** Dos sistemas que mantener

**💰 COSTE:**
- Setup: 7 horas (1h temporal + 6h Drive)
- Mensual: 0€
- Complejidad: Media-Alta

---

### 🎯 MI RECOMENDACIÓN

**Para MVP:**
### ✅ OPCIÓN B: Documentos Temporales

**Razones:**
1. **Ya casi implementado:** Tienes upload.py funcionando
2. **Simplicidad:** 1 hora de desarrollo
3. **Suficiente para MVP:** Usuarios pueden probar funcionalidad
4. **GDPR perfecto:** No almacenas nada
5. **Rápido:** Sin latencia de APIs externas

**Para Producción:**
### ⭐ OPCIÓN C: Híbrido (Temporal + Drive)

**Razones:**
1. **Mejor UX:** Usuario elige según necesidad
2. **Conversión:** Usuarios prueban temporal → migran a Drive
3. **Diferenciador:** Competencia no tiene esto

**Plan de implementación:**
```
Semana 1-2 (MVP):
└── Implementar Opción B (Temporal) - 1 hora

Semana 5-6 (Producción):
└── Añadir Opción A (Google Drive) - 6 horas
└── UI para elegir entre ambas - 2 horas
```

---


## 5. STORY 4.3: BÚSQUEDA WEB

### 🤔 DECISIÓN PENDIENTE: API de Búsqueda + Filtro de Fechas

### 📊 COMPARATIVA APIS DE BÚSQUEDA

#### API 1: Google Custom Search ⭐⭐⭐⭐⭐

**✅ VENTAJAS:**
- **Free tier generoso:** 100 búsquedas/día = 3,000/mes GRATIS
- **Calidad:** Mejor algoritmo de búsqueda
- **Filtro de fecha:** Nativo con parámetro `dateRestrict`
- **Región:** Puede filtrar por país (España)
- **Idioma:** Puede filtrar por español
- **Snippets:** Devuelve resúmenes de calidad

**❌ DESVENTAJAS:**
- **Límite diario:** 100/día (suficiente para MVP)
- **Coste después:** $5 por 1,000 búsquedas adicionales

**💰 COSTE:**
- MVP: 0€ (100/día gratis)
- Producción (100 usuarios, 10 búsquedas/día): €15/mes

**🔧 IMPLEMENTACIÓN:**
```python
# backend/agents/web_search_agent.py
import requests
from datetime import datetime

class GoogleCustomSearch:
    def __init__(self, api_key, search_engine_id):
        self.api_key = api_key
        self.cx = search_engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"
    
    def search_with_date_filter(
        self, 
        query: str, 
        cutoff_date: datetime,
        num_results: int = 10
    ):
        """
        Busca con filtro de fecha
        """
        # Calcular días desde cutoff_date hasta hoy
        days_ago = (datetime.now() - cutoff_date).days
        
        params = {
            'key': self.api_key,
            'cx': self.cx,
            'q': query,
            'num': num_results,
            'dateRestrict': f'd{days_ago}',  # Últimos N días
            'lr': 'lang_es',  # Solo español
            'gl': 'es',  # Región España
            'safe': 'active'  # Filtro seguro
        }
        
        response = requests.get(self.base_url, params=params)
        results = response.json()
        
        # Filtrar resultados por fecha de publicación
        filtered = []
        for item in results.get('items', []):
            # Google devuelve fecha en metadata
            pub_date = self._extract_date(item)
            if pub_date and pub_date <= cutoff_date:
                filtered.append({
                    'title': item['title'],
                    'snippet': item['snippet'],
                    'url': item['link'],
                    'published_date': pub_date.isoformat()
                })
        
        return filtered
```

---

#### API 2: Brave Search ⭐⭐⭐⭐

**✅ VENTAJAS:**
- **Free tier:** 2,000 búsquedas/mes GRATIS
- **Privacidad:** No trackea usuarios
- **Calidad:** Buena calidad de resultados
- **Filtro de fecha:** Soporta parámetro `freshness`

**❌ DESVENTAJAS:**
- **Límite mensual:** 2,000/mes (vs 3,000 de Google)
- **Calidad:** Ligeramente inferior a Google
- **Documentación:** Menos completa

**💰 COSTE:**
- MVP: 0€ (2,000/mes gratis)
- Producción: $5 por 1,000 búsquedas adicionales

---

#### API 3: SerpAPI ⭐⭐⭐

**✅ VENTAJAS:**
- **Múltiples motores:** Google, Bing, DuckDuckGo
- **Scraping robusto:** Maneja CAPTCHAs
- **Filtros avanzados:** Fecha, región, idioma

**❌ DESVENTAJAS:**
- **Free tier pequeño:** Solo 100 búsquedas/mes
- **Caro:** $50 por 5,000 búsquedas

**💰 COSTE:**
- MVP: 0€ (100/mes gratis) - INSUFICIENTE
- Producción: $50/mes

---

#### Opción 4: DuckDuckGo (No oficial) ⭐⭐⭐

**✅ VENTAJAS:**
- **Gratis ilimitado:** Sin API key, sin límites
- **Privacidad:** No trackea
- **Simple:** Fácil de implementar

**❌ DESVENTAJAS:**
- **No oficial:** Puede romperse en cualquier momento
- **Sin filtro de fecha:** No soporta filtro temporal
- **Calidad:** Inferior a Google/Brave
- **Rate limiting:** Pueden bloquearte si abusas

**💰 COSTE:**
- Siempre: 0€

---

### 🎯 MI RECOMENDACIÓN

**Para MVP:**
### ✅ Google Custom Search API

**Razones:**
1. **Free tier generoso:** 100/día = 3,000/mes (suficiente)
2. **Mejor calidad:** Resultados más relevantes
3. **Filtro de fecha nativo:** Fácil de implementar
4. **Confiable:** API oficial de Google

**Implementación del filtro de fecha:**

```python
# backend/routers/search.py
from fastapi import APIRouter, Query
from datetime import datetime
from agents.web_search_agent import GoogleCustomSearch

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/web")
async def search_web(
    query: str,
    cutoff_date: str = Query(
        default="2024-12-31",
        description="Fecha de corte (YYYY-MM-DD). Solo resultados hasta esta fecha"
    ),
    user_id: str = None
):
    """
    Búsqueda web con filtro de fecha
    """
    # 1. Parsear fecha de corte
    cutoff = datetime.strptime(cutoff_date, "%Y-%m-%d")
    
    # 2. Obtener configuración de usuario (si está logueado)
    if user_id:
        user_settings = get_user_settings(user_id)
        cutoff = user_settings.get('exam_cutoff_date', cutoff)
    
    # 3. Buscar con filtro
    search_engine = GoogleCustomSearch(
        api_key=os.getenv("GOOGLE_SEARCH_API_KEY"),
        search_engine_id=os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    )
    
    results = search_engine.search_with_date_filter(
        query=query,
        cutoff_date=cutoff,
        num_results=10
    )
    
    # 4. Log para análisis
    log_search_query(user_id, query, cutoff, len(results))
    
    return {
        "query": query,
        "cutoff_date": cutoff.isoformat(),
        "results_count": len(results),
        "results": results,
        "warning": f"Resultados filtrados hasta {cutoff_date}"
    }
```

**Frontend con selector de fecha:**

```typescript
// components/AdvancedSearch.tsx
import { useState } from 'react';
import DatePicker from 'react-datepicker';

const AdvancedSearch = () => {
  const [query, setQuery] = useState('');
  const [cutoffDate, setCutoffDate] = useState(new Date('2024-12-31'));
  const [includeRecent, setIncludeRecent] = useState(false);
  
  const handleSearch = async () => {
    const params = {
      query,
      cutoff_date: includeRecent 
        ? new Date().toISOString().split('T')[0]
        : cutoffDate.toISOString().split('T')[0]
    };
    
    const results = await fetch(`/api/search/web?${new URLSearchParams(params)}`);
    // ...
  };
  
  return (
    <div className="advanced-search">
      <input 
        type="text" 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Buscar en web..."
      />
      
      <div className="date-filter">
        <label>Fecha de corte:</label>
        <DatePicker 
          selected={cutoffDate}
          onChange={(date) => setCutoffDate(date)}
          maxDate={new Date()}
          dateFormat="dd/MM/yyyy"
        />
        <p className="info">
          ℹ️ Solo se mostrarán resultados publicados hasta esta fecha
        </p>
      </div>
      
      <div className="checkbox">
        <input 
          type="checkbox"
          checked={includeRecent}
          onChange={(e) => setIncludeRecent(e.target.checked)}
        />
        <label>Incluir cambios recientes (para estudio futuro)</label>
      </div>
      
      <button onClick={handleSearch}>Buscar</button>
    </div>
  );
};
```

**Configuración de fecha de corte por usuario:**

```python
# backend/routers/user.py
@router.put("/{user_id}/settings")
async def update_user_settings(
    user_id: str,
    exam_cutoff_date: str = None,  # "2024-12-31"
    exam_type: str = None  # "administrativo", "gestion", etc.
):
    """
    Actualiza configuración del usuario
    """
    settings = {}
    
    if exam_cutoff_date:
        # Validar fecha
        try:
            cutoff = datetime.strptime(exam_cutoff_date, "%Y-%m-%d")
            settings['exam_cutoff_date'] = cutoff
        except ValueError:
            raise HTTPException(400, "Fecha inválida")
    
    if exam_type:
        settings['exam_type'] = exam_type
    
    # Guardar en BD
    db.execute("""
        UPDATE user_progress
        SET settings = settings || %s::jsonb
        WHERE user_id = %s
    """, (json.dumps(settings), user_id))
    
    return {"status": "updated", "settings": settings}
```

---

### 🔍 MÉTODO ALTERNATIVO: Scraping Directo (NO RECOMENDADO)

**Opción:** Scraper propio sin API

```python
# NO RECOMENDADO - Solo para referencia
import requests
from bs4 import BeautifulSoup

def scrape_google(query, cutoff_date):
    """
    Scraping directo de Google (puede ser bloqueado)
    """
    url = f"https://www.google.com/search?q={query}&tbs=cdr:1,cd_max:{cutoff_date}"
    headers = {'User-Agent': 'Mozilla/5.0...'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Parsear resultados...
    # PROBLEMA: Google puede bloquear, cambiar HTML, etc.
```

**❌ Por qué NO:**
1. **Ilegal:** Viola términos de servicio de Google
2. **Inestable:** Google cambia HTML frecuentemente
3. **Bloqueado:** Google detecta y bloquea bots
4. **Sin soporte:** Si se rompe, no hay ayuda

---

### 📝 RESUMEN DECISIÓN Story 4.3

**API elegida:** Google Custom Search  
**Coste MVP:** 0€ (100/día gratis)  
**Implementación:** 6 horas  
**Filtro de fecha:** Nativo con `dateRestrict`  
**UI:** Selector de fecha en búsqueda avanzada  

---

## 6. HERRAMIENTAS SEGURIDAD

### 🤔 DECISIÓN: Aikido vs Semgrep vs SonarQube

### 📊 COMPARATIVA DETALLADA

#### Aikido Security ⭐⭐⭐⭐⭐

**Según su web (aikido.dev/comparison/semgrep):**

**✅ VENTAJAS:**
1. **Todo en uno:** SAST + SCA + DAST + Cloud + Runtime + Secrets
2. **Reducción de ruido:** 75-95% menos falsos positivos
3. **AutoFix con IA:** Genera fixes automáticos
4. **Multi-file analysis:** Analiza contexto entre archivos
5. **Reachability analysis:** Detecta si usas función vulnerable
6. **Code Quality:** No solo seguridad, también calidad
7. **Fácil setup:** 2-10 minutos según reviews
8. **Integraciones:** GitHub, GitLab, Bitbucket, Slack, Jira
9. **UI intuitiva:** Dashboard claro y accionable
10. **Soporte responsive:** Responden en horas

**❌ DESVENTAJAS:**
1. **Coste:** €3,240/año (Basic) o €6,480/año (Pro)
2. **SaaS:** Tu código va a sus servidores
3. **Vendor lock-in:** Dependes de ellos

**💰 COSTE:**
- Basic: €270/mes (€3,240/año)
- Pro: €540/mes (€6,480/año)
- **Para MVP:** DEMASIADO CARO

---

#### Semgrep ⭐⭐⭐⭐

**✅ VENTAJAS:**
1. **Open Source:** Community edition gratis
2. **Reglas custom:** Puedes crear reglas GDPR/LOPDGDD
3. **Rápido:** Análisis en segundos
4. **30+ lenguajes:** Python, TypeScript, JavaScript
5. **Local:** Puede correr 100% local
6. **Reglas GDPR:** Ya existen reglas públicas

**❌ DESVENTAJAS:**
1. **Ruido:** Más falsos positivos que Aikido
2. **Sin AutoFix:** No genera fixes automáticos
3. **Sin multi-file:** Análisis archivo por archivo
4. **Solo SAST:** No hace SCA, DAST, etc.

**💰 COSTE:**
- Community: 0€
- Teams: $344/mes (€4,128/año)
- **Para MVP:** GRATIS ✅

---

#### SonarQube Community ⭐⭐⭐⭐⭐

**✅ VENTAJAS:**
1. **Open Source:** Community edition gratis
2. **Completo:** SAST + Code Quality + Deuda técnica
3. **35+ lenguajes:** Python, TypeScript, JavaScript
4. **Métricas:** Cobertura, complejidad, duplicación
5. **Histórico:** Tracking de calidad en el tiempo
6. **Integración CI/CD:** GitHub Actions, GitLab CI
7. **Local:** 100% en tu servidor

**❌ DESVENTAJAS:**
1. **Requiere servidor:** Docker o VM
2. **Setup complejo:** 2-3 horas configuración
3. **Sin IA:** No tiene AutoFix con IA
4. **Ruido:** Puede generar muchas alertas

**💰 COSTE:**
- Community: 0€
- Developer: $150/año por desarrollador
- **Para MVP:** GRATIS ✅

---

#### Qodo (ya instalado) ⭐⭐⭐⭐

**✅ VENTAJAS:**
1. **Ya instalado:** Lo tienes en tu IDE
2. **PR reviews:** Automáticas con IA
3. **Genera tests:** Automáticamente
4. **Gratis:** Para proyectos open source

**❌ DESVENTAJAS:**
1. **Limitado:** Solo PR reviews y tests
2. **No es auditoría completa:** No reemplaza SAST

**💰 COSTE:**
- Open source: 0€
- Pro: $19/mes por desarrollador

---

### 🎯 MI RECOMENDACIÓN

**Para MVP (Ahora):**
### ✅ Qodo (ya instalado) + Semgrep

**Razones:**
1. **Gratis:** 0€ ambos
2. **Complementarios:** Qodo para PRs, Semgrep para SAST
3. **Reglas GDPR:** Semgrep permite reglas custom
4. **Suficiente:** Para MVP no necesitas más

**Setup Semgrep:**
```bash
# 1. Instalar
pip install semgrep

# 2. Escanear con reglas GDPR
semgrep --config=p/gdpr .

# 3. Crear reglas custom LOPDGDD
# .semgrep/lopdgdd.yml
rules:
  - id: lopdgdd-pii-without-consent
    pattern: user.email
    message: "Verificar consentimiento LOPDGDD Art. 6"
    severity: WARNING
    languages: [python, typescript]
    
  - id: lopdgdd-data-retention
    pattern: DELETE FROM users
    message: "Verificar período retención LOPDGDD Art. 32"
    severity: WARNING
    languages: [sql]

# 4. Integrar en GitHub Actions
# .github/workflows/semgrep.yml
name: Semgrep
on: [push, pull_request]
jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/gdpr
            .semgrep/lopdgdd.yml
```

**Para Producción (Cuando tengas ingresos):**
### ⭐ Aikido Security

**Razones:**
1. **Todo en uno:** Reemplaza Qodo + Semgrep + SonarQube
2. **Menos ruido:** 75-95% reducción falsos positivos
3. **AutoFix:** Ahorra tiempo de desarrollo
4. **ROI positivo:** Si ahorras 10h/mes, vale la pena €270/mes

**Cuándo migrar:**
- Cuando tengas >30 usuarios pagando (€450/mes ingresos)
- O cuando tengas >100 PRs/mes (mucho ruido)

---


## 7. ARQUITECTURA DEPLOYMENT - CÁLCULO ESPACIO VPS

### 📊 ANÁLISIS DETALLADO VPS HOSTINGER (8GB RAM)

#### Estado Actual (Con Mistral)

```
VPS Hostinger (8GB RAM):
├── Sistema Operativo (Ubuntu) - 1GB
├── Mistral 8B (Ollama) - 4.5GB
├── PostgreSQL - 500MB
├── Nginx - 100MB
├── Otros servicios - 500MB
└── Disponible: ~1.4GB
```

**Conclusión:** Con Mistral NO CABE nada más.

---

#### Propuesta: Borrar Mistral, Instalar Todo

```
VPS Hostinger (8GB RAM) - NUEVO:
├── Sistema Operativo (Ubuntu) - 1GB
├── Nginx (proxy reverso) - 100MB
├── PostgreSQL (usuarios + progreso) - 800MB
├── Frontend (React build estático) - 50MB
├── Backend (FastAPI + Python) - 300MB
├── Redis (cache + sessions) - 150MB
├── Qdrant Local (opcional) - 500MB
├── Logs y temp - 200MB
└── Disponible: ~4.9GB para datos
```

**Total usado:** ~3.1GB  
**Disponible para datos:** ~4.9GB

---

### 💾 CÁLCULO ALMACENAMIENTO: 10 USUARIOS, 6 MESES

#### Datos por Usuario - Uso Normal

**PostgreSQL (Datos relacionales):**
```
user_progress: 1 registro × 500 bytes = 500 bytes
answer_history: 500 respuestas × 1KB = 500KB
simulacros: 10 simulacros × 50KB = 500KB
study_sessions: 50 sesiones × 2KB = 100KB
recommendations: 20 recomendaciones × 1KB = 20KB
rag_queries: 100 queries × 2KB = 200KB
```
**Subtotal PostgreSQL:** ~1.3MB por usuario

**JSONB (Objetos complejos):**
```
mind_maps: 5 mapas × 100KB = 500KB
user_cases: 10 casos × 50KB = 500KB
simulacros.resultados_detallados: 10 × 20KB = 200KB
```
**Subtotal JSONB:** ~1.2MB por usuario

**Chat History (si se almacena):**
```
chat_history: 30 conversaciones × 50KB = 1.5MB
```
**Subtotal Chat:** ~1.5MB por usuario

**TOTAL POR USUARIO (Uso Normal):** ~4MB

---

#### Datos por Usuario - Uso Excesivo

**PostgreSQL:**
```
answer_history: 1,500 respuestas × 1KB = 1.5MB
simulacros: 30 simulacros × 50KB = 1.5MB
study_sessions: 150 sesiones × 2KB = 300KB
rag_queries: 300 queries × 2KB = 600KB
```
**Subtotal PostgreSQL:** ~4MB

**JSONB:**
```
mind_maps: 20 mapas × 100KB = 2MB
user_cases: 30 casos × 50KB = 1.5MB
simulacros.resultados_detallados: 30 × 20KB = 600KB
```
**Subtotal JSONB:** ~4.1MB

**Chat History:**
```
chat_history: 100 conversaciones × 50KB = 5MB
```
**Subtotal Chat:** ~5MB

**TOTAL POR USUARIO (Uso Excesivo):** ~13MB

---

### 📊 TOTALES: 10 USUARIOS, 6 MESES

| Escenario | Por Usuario | 10 Usuarios | Disponible VPS |
|-----------|-------------|-------------|----------------|
| **Uso Normal** | 4MB | 40MB | 4.9GB → ✅ SOBRA |
| **Uso Excesivo** | 13MB | 130MB | 4.9GB → ✅ SOBRA |
| **Uso Extremo** | 50MB | 500MB | 4.9GB → ✅ SOBRA |

**Conclusión:** ✅ **SÍ CABE TODO EN EL VPS**

---

### 📈 PROYECCIÓN: ¿Cuántos Usuarios Caben?

```
Espacio disponible: 4.9GB = 4,900MB

Uso normal (4MB/usuario):
4,900MB ÷ 4MB = 1,225 usuarios ✅

Uso excesivo (13MB/usuario):
4,900MB ÷ 13MB = 377 usuarios ✅

Uso extremo (50MB/usuario):
4,900MB ÷ 50MB = 98 usuarios ✅
```

**Conclusión:** El VPS soporta entre **100-1,200 usuarios** según uso.

---

### 🎯 RECOMENDACIÓN ARQUITECTURA

#### Para MVP (0-100 usuarios)

```
VPS Hostinger (8GB):
├── Frontend (React) - Servido por Nginx
├── Backend (FastAPI) - Puerto 8000
├── PostgreSQL - Puerto 5432
├── Redis - Puerto 6379
└── Nginx - Puerto 80/443 (HTTPS)

Qdrant:
└── Qdrant Cloud (1GB gratis) - Leyes indexadas

Mistral:
└── BORRADO (usar Gemini API gratis)
```

**Ventajas:**
- ✅ Todo en un servidor (simple)
- ✅ Datos en tu control (GDPR)
- ✅ Rápido (sin latencia de red)
- ✅ Barato (solo VPS €10/mes)

**Desventajas:**
- ⚠️ Single point of failure
- ⚠️ Backups manuales

---

#### Para Producción (100-500 usuarios)

```
VPS Hostinger (8GB):
├── Frontend (React) - Servido por Nginx
├── Backend (FastAPI)
├── PostgreSQL (datos críticos)
└── Redis

Servicios Cloud:
├── Qdrant Cloud (5GB, €25/mes) - Leyes
├── Neon (3GB gratis) - Objetos grandes (chat, mapas)
└── Cloudflare Tunnel - HTTPS + DDoS protection

LLM:
└── Gemini 2.0 Flash API (€25/mes)
```

**Ventajas:**
- ✅ Escalable (Neon + Qdrant escalan solos)
- ✅ Backups automáticos (Neon)
- ✅ DDoS protection (Cloudflare)
- ✅ Datos críticos en tu VPS (GDPR)

**Desventajas:**
- ⚠️ Más complejo
 
---

### 💰 COMPARATIVA COSTES

| Componente | MVP | Producción |
|------------|-----|------------|
| VPS Hostinger | €10/mes | €10/mes |
| Qdrant Cloud | €0 (1GB) | €25/mes (5GB) |
| Neon PostgreSQL | €0 | €0 (3GB gratis) |
| Gemini API | €0 (1M tokens/día) | €25/mes |
| Cloudflare Tunnel | €0 | €0 |
| Google Search API | €0 (100/día) | €15/mes |
| **TOTAL** | **€10/mes** | **€75/mes** |

**Ingresos estimados (30% conversión a €15/mes):**
- 100 usuarios → 30 Premium → €450/mes
- **Beneficio:** €450 - €75 = €375/mes ✅

---

## 8. DOCKERIZACIÓN

### 🤔 DECISIÓN: ¿Cuándo Dockerizar?

### 📊 ANÁLISIS

#### Ventajas de Dockerizar AHORA

**✅ PROS:**
1. **Deployment consistente:** Mismo entorno dev/prod
2. **Fácil rollback:** `docker-compose down && docker-compose up`
3. **Aislamiento:** Cada servicio en su contenedor
4. **Portabilidad:** Migrar a otro servidor en minutos
5. **Escalabilidad:** Fácil añadir réplicas

**❌ CONTRAS:**
1. **Complejidad inicial:** 4-6 horas setup
2. **Overhead:** Docker usa ~500MB RAM adicional
3. **Curva aprendizaje:** Si no conoces Docker
4. **Debugging:** Más complejo debuggear en contenedores

---

#### Ventajas de Dockerizar DESPUÉS

**✅ PROS:**
1. **Más simple ahora:** Instalación directa en VPS
2. **Menos overhead:** Sin Docker daemon
3. **Debugging fácil:** Logs directos, no contenedores
4. **Cambios rápidos:** No rebuild de imágenes

**❌ CONTRAS:**
1. **Migración futura:** Tendrás que dockerizar después
2. **Inconsistencias:** Dev vs prod pueden diferir
3. **Dependencias:** Conflictos de versiones

---

### 🎯 MI RECOMENDACIÓN

### ✅ DOCKERIZAR AHORA (Antes de cambiar mucho)

**Razones:**
1. **Ahora es el mejor momento:** Antes de añadir más código
2. **Migración futura:** Si creces, migrar será trivial
3. **Backups:** Docker volumes son fáciles de backupear
4. **Profesional:** Deployment moderno y estándar
5. **CI/CD:** Fácil integrar con GitHub Actions

**Tiempo:** 4-6 horas (vale la pena)

---

### 🔧 IMPLEMENTACIÓN DOCKER

#### docker-compose.yml

```yaml
version: '3.8'

services:
  # Frontend
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped

  # Backend
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/opositaia
      - REDIS_URL=redis://redis:6379
      - QDRANT_URL=${QDRANT_URL}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    restart: unless-stopped

  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=opositaia
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/database/schema.sql:/docker-entrypoint-initdb.d/schema.sql
    restart: unless-stopped

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Nginx (Reverse Proxy)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

#### backend/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### frontend/Dockerfile

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build
COPY . .
RUN npm run build

# Production
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

#### Comandos

```bash
# Build y start
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build

# Backup PostgreSQL
docker-compose exec postgres pg_dump -U postgres opositaia > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres opositaia < backup.sql
```

---

### 📝 PLAN DE DOCKERIZACIÓN

**Semana 1 (4-6 horas):**
1. Crear Dockerfiles (1h)
2. Crear docker-compose.yml (1h)
3. Configurar Nginx (1h)
4. Testing local (1h)
5. Deploy a VPS (1h)
6. Documentación (1h)

**Resultado:**
- ✅ App dockerizada
- ✅ Deployment con un comando
- ✅ Fácil migración futura

---

## 9. FIREBASE VS VERCEL

### 🤔 DECISIÓN: ¿Dónde Hostear Frontend y Auth?

### 📊 COMPARATIVA DETALLADA

#### Firebase ⭐⭐⭐⭐

**Servicios útiles:**

**1. Firebase Authentication**
- ✅ Gratis: 50,000 usuarios/mes
- ✅ Email/password, Google, Facebook
- ✅ JWT tokens automáticos
- ✅ Muy fácil integrar
- ⚠️ Datos en servidores Google (pero región EU disponible)

**2. Firebase Hosting**
- ✅ Gratis: 10GB storage, 360MB/día transfer
- ✅ CDN global automático
- ✅ HTTPS automático
- ✅ Deploy: `firebase deploy`

**3. Firebase Storage**
- ✅ Gratis: 5GB storage, 1GB/día transfer
- ✅ Perfecto para documentos temporales
- ⚠️ Datos en Google Cloud

**💰 COSTE:**
- MVP: 0€
- Producción (100 usuarios): 0€ (dentro de free tier)

**🔒 GDPR:**
- ⚠️ Datos en Google Cloud
- ✅ Región EU disponible
- ⚠️ Dependencia de Google

---

#### Vercel ⭐⭐⭐⭐⭐

**Servicios:**

**1. Hosting**
- ✅ Gratis: 100GB bandwidth/mes
- ✅ CDN global Edge Network
- ✅ HTTPS automático
- ✅ Deploy automático desde GitHub
- ✅ Preview deployments (cada PR)

**2. Serverless Functions**
- ✅ Gratis: 100GB-hours/mes
- ⚠️ No ideal para backend completo

**💰 COSTE:**
- MVP: 0€
- Producción (100 usuarios): 0€ (dentro de free tier)

**🔒 GDPR:**
- ⚠️ Datos en Vercel (USA)
- ⚠️ Solo frontend (HTML/JS/CSS)
- ✅ No almacena datos de usuario

---

#### Tu VPS + Nginx ⭐⭐⭐⭐⭐

**Servicios:**

**1. Hosting Frontend**
- ✅ Gratis (incluido en VPS)
- ✅ Control total
- ✅ Datos en tu servidor EU
- ⚠️ Sin CDN global (más lento para usuarios fuera EU)

**2. Auth Custom**
- ✅ Control total
- ✅ Datos en tu servidor
- ⚠️ Más trabajo implementar

**💰 COSTE:**
- Siempre: 0€ (incluido en VPS)

**🔒 GDPR:**
- ✅ Datos 100% en tu servidor EU
- ✅ Control total
- ✅ Sin dependencias externas

---

### 🎯 MI RECOMENDACIÓN

### ✅ OPCIÓN HÍBRIDA: Vercel (Frontend) + VPS (Backend + Auth)

**Arquitectura:**
```
Vercel (Frontend):
└── React app (HTML/JS/CSS estático)
    └── Llama a API en tu VPS

Tu VPS (Backend + Auth + Datos):
├── FastAPI (API REST)
├── PostgreSQL (usuarios, auth, progreso)
├── Redis (sessions)
└── Cloudflare Tunnel (HTTPS + DDoS)
```

**✅ VENTAJAS:**
1. **Frontend rápido:** CDN global de Vercel
2. **Datos seguros:** Auth y datos en tu VPS EU
3. **GDPR compliant:** Datos personales en tu servidor
4. **Gratis:** Vercel free tier + VPS que ya tienes
5. **Deploy automático:** Push a GitHub → Vercel deploya
6. **Preview PRs:** Cada PR tiene URL de preview

**❌ DESVENTAJAS:**
1. **Dos servicios:** Vercel + VPS (pero simple)
2. **CORS:** Necesitas configurar CORS en backend

---

### 🔧 IMPLEMENTACIÓN

#### 1. Deploy Frontend en Vercel

```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy
cd frontend
vercel

# 4. Configurar variables de entorno en Vercel Dashboard
VITE_API_URL=https://api.opositaia.com
```

#### 2. Backend en VPS con Cloudflare Tunnel

```bash
# 1. Instalar cloudflared en VPS
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# 2. Login
cloudflared tunnel login

# 3. Crear tunnel
cloudflared tunnel create opositaia

# 4. Configurar DNS
cloudflared tunnel route dns opositaia api.opositaia.com

# 5. Configurar tunnel
# ~/.cloudflared/config.yml
tunnel: <TUNNEL_ID>
credentials-file: /root/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: api.opositaia.com
    service: http://localhost:8000
  - service: http_status:404

# 6. Correr como servicio
sudo cloudflared service install
sudo systemctl start cloudflared
```

#### 3. Auth Custom en Backend

```python
# backend/routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

@router.post("/register")
async def register(email: str, password: str, username: str):
    """Registrar nuevo usuario"""
    # 1. Hash password
    hashed = pwd_context.hash(password)
    
    # 2. Guardar en PostgreSQL (tu VPS)
    user_id = db.execute("""
        INSERT INTO user_progress (email, password_hash, username)
        VALUES (%s, %s, %s)
        RETURNING user_id
    """, (email, hashed, username))
    
    # 3. Generar JWT
    token = jwt.encode({
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(days=30)
    }, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"token": token, "user_id": str(user_id)}

@router.post("/login")
async def login(email: str, password: str):
    """Login usuario"""
    # 1. Buscar usuario
    user = db.query("""
        SELECT user_id, password_hash
        FROM user_progress
        WHERE email = %s
    """, (email,))
    
    if not user:
        raise HTTPException(401, "Email o password incorrectos")
    
    # 2. Verificar password
    if not pwd_context.verify(password, user['password_hash']):
        raise HTTPException(401, "Email o password incorrectos")
    
    # 3. Generar JWT
    token = jwt.encode({
        'user_id': str(user['user_id']),
        'exp': datetime.utcnow() + timedelta(days=30)
    }, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"token": token, "user_id": str(user['user_id'])}

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Middleware: verificar JWT"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Token inválido")
```

---

### 📝 RESUMEN DECISIÓN

**Frontend:** Vercel (CDN global, gratis)  
**Backend:** VPS + Cloudflare Tunnel (HTTPS, DDoS protection)  
**Auth:** Custom JWT en VPS (datos en tu servidor EU)  
**Datos:** PostgreSQL en VPS (GDPR compliant)  

**Coste total:** €10/mes (solo VPS)

---

## 10. RESUMEN DECISIONES Y PRÓXIMOS PASOS

### ✅ DECISIONES APROBADAS



| # | Decisión | Opción Elegida | Cuándo |
|---|----------|----------------|--------|
| 1 | **Algoritmo Adaptativo** | 3-4 simulacros mínimo, nota corte 8.5/10 | ✅ Aprobado |
| 2 | **BD para RAG** | PostgreSQL para TODO (JSONB) | MVP |
| 3 | **Documentos Usuario** | Temporales (Redis 24h) | MVP |
| 4 | **Búsqueda Web** | Google Custom Search API | MVP |
| 5 | **Herramientas Seguridad** | Qodo + Semgrep | MVP |
| 6 | **Arquitectura** | Todo en VPS (sin Mistral) | MVP |
| 7 | **Dockerización** | SÍ, ahora (4-6h) | MVP |
| 8 | **Frontend Hosting** | Vercel (CDN global) | MVP |
| 9 | **Backend Hosting** | VPS + Cloudflare Tunnel | MVP |
| 10 | **Auth** | Custom JWT en VPS | MVP |
| 11 | **Pagos** | Stripe | Después del MVP |

---

### 📊 ARQUITECTURA FINAL MVP

```
┌─────────────────────────────────────────────────────────┐
│                    VERCEL (Frontend)                     │
│  - React app (CDN global)                                │
│  - Deploy automático desde GitHub                        │
│  - HTTPS automático                                      │
└─────────────────────────────────────────────────────────┘
                          ↓ HTTPS
┌─────────────────────────────────────────────────────────┐
│              CLOUDFLARE TUNNEL (Seguridad)               │
│  - DDoS protection                                       │
│  - HTTPS                                                 │
│  - api.opositaia.com                                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                VPS HOSTINGER (8GB RAM)                   │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Docker Compose                                  │    │
│  │  ├── Nginx (reverse proxy)                       │    │
│  │  ├── Backend (FastAPI)                           │    │
│  │  ├── PostgreSQL (usuarios, progreso, JSONB)     │    │
│  │  └── Redis (cache, sessions, docs temporales)   │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  SERVICIOS EXTERNOS                      │
│  ├── Qdrant Cloud (1GB gratis) - Leyes indexadas        │
│  ├── Gemini API (1M tokens/día gratis) - LLM            │
│  └── Google Custom Search (100/día gratis) - Web        │
└─────────────────────────────────────────────────────────┘
```

---

### 💰 COSTES MENSUALES MVP

| Servicio | Coste | Notas |
|----------|-------|-------|
| VPS Hostinger (8GB) | €10/mes | Ya lo tienes |
| Vercel (Frontend) | €0 | Free tier |
| Cloudflare Tunnel | €0 | Gratis |
| Qdrant Cloud (1GB) | €0 | Free tier |
| Gemini API | €0 | 1M tokens/día gratis |
| Google Custom Search | €0 | 100/día gratis |
| **TOTAL MVP** | **€10/mes** | 🎉 |

---

### 📈 CAPACIDAD MVP

| Métrica | Capacidad |
|---------|-----------|
| **Usuarios simultáneos** | 50-100 |
| **Usuarios totales** | 100-500 |
| **Almacenamiento usado** | 40MB-500MB |
| **Almacenamiento disponible** | 4.9GB |
| **Requests/día** | 10,000+ |
| **Uptime esperado** | 99%+ |

---

### 🚀 PLAN DE IMPLEMENTACIÓN

#### Fase 1: Preparación VPS (1 día)

```bash
# 1. Backup actual
sudo tar -czf backup_$(date +%Y%m%d).tar.gz /var/www /etc/nginx

# 2. Borrar Mistral
docker stop ollama
docker rm ollama
docker rmi ollama/ollama

# 3. Limpiar espacio
sudo apt-get autoremove
sudo apt-get clean
docker system prune -a

# 4. Verificar espacio
df -h
# Deberías tener ~5GB libres
```

#### Fase 2: Dockerización (4-6 horas)

```bash
# 1. Crear Dockerfiles
# backend/Dockerfile
# frontend/Dockerfile

# 2. Crear docker-compose.yml

# 3. Build y test local
docker-compose up -d
docker-compose logs -f

# 4. Verificar funcionamiento
curl http://localhost:8000/health
curl http://localhost:3000
```

#### Fase 3: Deploy VPS (2 horas)

```bash
# 1. Subir código a VPS
git clone https://github.com/tu-repo/opositaia.git
cd opositaia

# 2. Configurar .env
cp .env.example .env
# Editar .env con tus keys

# 3. Deploy
docker-compose up -d

# 4. Verificar
docker-compose ps
docker-compose logs -f backend
```

#### Fase 4: Cloudflare Tunnel (1 hora)

```bash
# 1. Instalar cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# 2. Configurar tunnel
cloudflared tunnel login
cloudflared tunnel create opositaia
cloudflared tunnel route dns opositaia api.opositaia.com

# 3. Configurar servicio
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

#### Fase 5: Deploy Frontend Vercel (30 min)

```bash
# 1. Conectar repo GitHub a Vercel
# Dashboard: vercel.com → New Project → Import Git Repository

# 2. Configurar variables de entorno
VITE_API_URL=https://api.opositaia.com

# 3. Deploy
# Automático al hacer push a main
```

#### Fase 6: Testing E2E (1 hora)

```bash
# 1. Test frontend
curl https://opositaia.vercel.app

# 2. Test backend
curl https://api.opositaia.com/health

# 3. Test auth
curl -X POST https://api.opositaia.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","username":"test"}'

# 4. Test RAG
curl https://api.opositaia.com/rag/search?query=jubilacion

# 5. Test búsqueda web
curl https://api.opositaia.com/search/web?query=LGSS&cutoff_date=2024-12-31
```

---

### 📝 MODIFICACIONES AL PLAN DE DESARROLLO

#### Story 2.2: Algoritmo Adaptativo
- ✅ Modificado: 3-4 simulacros mínimo (180-240 respuestas)
- ✅ Nota de corte: 8.5/10 (85%)
- ✅ Calcula probabilidad de aprobar
- ⏱️ Estimación: 8 horas (aumentado de 5h)

#### Story 4.1: RAG Adaptativo
- ✅ Modificado: PostgreSQL JSONB para todo
- ✅ Agente evaluador de progreso
- ✅ Filtros por nivel de usuario
- ⏱️ Estimación: 10 horas (aumentado de 6h)

#### Story 4.2: Gestión Documentos
- ✅ Modificado: Documentos temporales (Redis 24h)
- ✅ Aviso claro: "No persiste entre sesiones"
- ✅ Opción futura: Google Drive
- ⏱️ Estimación: 3 horas (reducido de 8h)

#### Story 4.3: Búsqueda Web
- ✅ Modificado: Google Custom Search API
- ✅ Filtro de fecha nativo
- ✅ Selector de fecha en UI
- ⏱️ Estimación: 6 horas (aumentado de 4h)

#### Story 5.1: Auditoría Seguridad
- ✅ Modificado: Qodo + Semgrep (no SonarQube)
- ✅ Reglas GDPR + LOPDGDD custom
- ✅ GitHub Actions CI/CD
- ⏱️ Estimación: 2 horas (reducido de 3h)

#### Nueva Story: Dockerización
- ✅ Añadido: Dockerizar toda la app
- ✅ docker-compose.yml completo
- ✅ Deploy con un comando
- ⏱️ Estimación: 6 horas

---

### 📊 TIEMPO TOTAL ACTUALIZADO

| Epic | Original | Actualizado | Diferencia |
|------|----------|-------------|------------|
| Epic 1: UX | 20h | 20h | - |
| Epic 2: Personalización | 14h | 16h | +2h |
| Epic 3: Transparencia | 9h | 9h | - |
| Epic 4: Contexto | 18h | 19h | +1h |
| Epic 5: Seguridad | 12h | 14h | +2h |
| **TOTAL** | **73h** | **78h** | **+5h** |

**Nuevo timeline:** 8 semanas + 3 días

---

### ✅ CHECKLIST ANTES DE EMPEZAR

- [ ] Backup completo del VPS actual
- [ ] Borrar Mistral y liberar espacio
- [ ] Verificar 5GB libres en VPS
- [ ] Crear cuenta Vercel
- [ ] Crear cuenta Cloudflare
- [ ] Obtener API keys:
  - [ ] Gemini API
  - [ ] Google Custom Search
  - [ ] Qdrant Cloud
- [ ] Configurar .env con todas las keys
- [ ] Leer documentación Docker Compose
- [ ] Preparar dominio (api.opositaia.com)

---

### 🎯 PRÓXIMOS PASOS INMEDIATOS

**Esta semana:**
1. ✅ Aprobar este documento
2. ⏱️ Backup VPS (30 min)
3. ⏱️ Borrar Mistral (15 min)
4. ⏱️ Dockerizar app (6 horas)
5. ⏱️ Deploy en VPS (2 horas)

**Próxima semana:**
6. ⏱️ Cloudflare Tunnel (1 hora)
7. ⏱️ Deploy Vercel (30 min)
8. ⏱️ Testing E2E (1 hora)
9. ⏱️ Modificar Story 2.2 (8 horas)

---

### 📞 PREGUNTAS FINALES PARA TI

1. **¿Apruebas todas las decisiones de este documento?**
2. **¿Tienes experiencia con Docker o necesitas tutorial?**
3. **¿Tienes dominio registrado (opositaia.com) o necesitas comprar?**
4. **¿Prefieres que empiece por Dockerización o por modificar Stories?**
5. **¿Alguna duda sobre la arquitectura propuesta?**

---

**Documento creado:** 26 Noviembre 2025  
**Próxima acción:** Esperar tu aprobación para empezar implementación

