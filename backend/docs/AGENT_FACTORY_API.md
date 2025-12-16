# 🏭 Agent Factory API - Documentación

**Versión:** 1.0  
**Fecha:** 16 Diciembre 2025  
**Estrategia:** COSM (Create Once, Serve Many) + MCP Integration

---

## 🎯 OVERVIEW

La **Agent Factory** es una factoría de agentes especializados que combina:

- **MCP Server** - Acceso directo al RAG de Seguridad Social (18,470 chunks)
- **Estrategia COSM** - Contenido reutilizable (94% ahorro de costes)
- **Formato Oficial** - BOE-A-2024-11403 (100 test + 12 casos prácticos)
- **Personalización** - Variaciones por usuario sin regenerar

### Arquitectura

```
Frontend React
    ↓
FastAPI Agent Factory
    ↓
MCP Server (Node.js)
    ↓
Qdrant Cloud (18,470 chunks)
```

---

## 🚀 ENDPOINTS

### Base URL: `/agents`

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/crear` | POST | Endpoint universal para cualquier contenido |
| `/simulacro` | POST | Crear simulacro oficial BOE-A-2024-11403 |
| `/caso` | POST | Crear caso práctico con jurisprudencia |
| `/flashcards` | POST | Crear lote de flashcards |
| `/resumen` | POST | Crear resumen de ley |
| `/mapa_mental` | POST | Crear mapa mental |
| `/health` | GET | Health check |
| `/batch/generar_inicial` | POST | Generación masiva COSM |

---

## 📝 SIMULACROS OFICIALES

### `POST /agents/simulacro`

Crea simulacro con **formato oficial BOE-A-2024-11403**:
- **100 preguntas test** (temas 1-32 generales)
- **12 casos prácticos** (18 temas SS específicos)
- **Penalización -0.25** por error
- **Mínimo 25/50 puntos** en cada parte

#### Request

```json
{
  "tema": "Seguridad Social",
  "nivel": "INTERMEDIO",
  "formato_oficial": true,
  "usuario_id": 123
}
```

#### Response

```json
{
  "status": "success",
  "data": {
    "id": "sim_Seguridad Social_INTERMEDIO_20251216_153045",
    "tema": "Seguridad Social",
    "nivel": "INTERMEDIO",
    "formato": "BOE-A-2024-11403",
    "estructura": {
      "parte_1": {
        "tipo": "test_general",
        "preguntas": 100,
        "puntuacion_maxima": 50,
        "minimo_aprobar": 25,
        "contenido": [
          {
            "id": 1,
            "texto": "¿Cuál es el concepto principal de...?",
            "opciones": ["A", "B", "C", "D"],
            "respuesta_correcta": 0,
            "explicacion": "La respuesta correcta es A porque...",
            "referencia": "Art. 12 LGSS",
            "nivel": "INTERMEDIO"
          }
        ]
      },
      "parte_2": {
        "tipo": "casos_practicos",
        "preguntas": 12,
        "puntuacion_maxima": 50,
        "minimo_aprobar": 25,
        "contenido": [
          {
            "id": 1,
            "titulo": "Caso Práctico 1: Seguridad Social",
            "hechos": "Situación práctica...",
            "pregunta": "¿Qué procedimiento corresponde aplicar?",
            "opciones": ["A", "B", "C", "D"],
            "respuesta_correcta": 0,
            "solucion": "Análisis jurídico...",
            "referencias": ["Art. X LGSS", "STS 123/2024"]
          }
        ]
      }
    },
    "instrucciones": {
      "penalizacion": -0.25,
      "tiempo_estimado": "3 horas",
      "requisito": "Mínimo 25 puntos en CADA parte"
    }
  },
  "formato": "BOE-A-2024-11403",
  "estructura": "100 test + 12 casos prácticos"
}
```

---

## ⚖️ CASOS PRÁCTICOS

### `POST /agents/caso`

Crea caso práctico realista con jurisprudencia del Tribunal Supremo.

#### Request

```json
{
  "tema": "Incapacidad Temporal",
  "complejidad": "ALTA",
  "incluir_jurisprudencia": true,
  "usuario_id": 123
}
```

#### Response

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "titulo": "Caso Práctico: Incapacidad Temporal",
    "hechos": "María trabaja en una empresa del sector servicios. Su salario base es de 1800€ mensuales y lleva 5 años en la empresa. El 15 de marzo de 2024 causa baja por incapacidad temporal debido a una lesión laboral...",
    "pregunta": "¿Qué prestación le corresponde del día 4º al 15º de baja?",
    "opciones": [
      "60% de la base reguladora a cargo de la empresa",
      "60% de la base reguladora a cargo de la Seguridad Social",
      "75% de la base reguladora a cargo de la empresa",
      "75% de la base reguladora a cargo de la Seguridad Social"
    ],
    "respuesta_correcta": 0,
    "solucion": "Según el artículo 173 LGSS, del día 4º al 15º de baja por IT, corresponde el 60% de la base reguladora a cargo de la empresa. Cálculo: (1800/30) × 60% × 12 días = 432€",
    "referencias": ["Art. 173 LGSS", "STS 1234/2024"],
    "contexto_rag": {
      "title": "Incapacidad Temporal - Prestaciones",
      "content": "La incapacidad temporal es la situación...",
      "source": "BOE-A-2015-11724"
    }
  },
  "incluye_jurisprudencia": true
}
```

---

## 🎴 FLASHCARDS

### `POST /agents/flashcards`

Crea lote de flashcards usando contenido del RAG.

#### Request

```json
{
  "tema": "Jubilación",
  "cantidad": 10,
  "estilo": "DEFINICION",
  "usuario_id": 123
}
```

**Estilos disponibles:**
- `DEFINICION` - "¿Qué es X?" → "Es..."
- `PREGUNTA` - "¿Cuándo se aplica X?" → "Se aplica cuando..."
- `CALCULO` - "¿Cómo se calcula X?" → "Fórmula: ..."

#### Response

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "pregunta": "¿Qué es la jubilación anticipada?",
      "respuesta": "Es la prestación que permite acceder a la jubilación antes de la edad ordinaria, cumpliendo ciertos requisitos de cotización y edad mínima...",
      "explicacion": "La jubilación anticipada se regula en los artículos 208 y siguientes de la LGSS. Existen dos modalidades: voluntaria (con coeficientes reductores) e involuntaria (por cese no voluntario)...",
      "fuente": "BOE-A-2015-11724",
      "tema": "Jubilación",
      "dificultad": 3
    }
  ],
  "cantidad": 10,
  "estilo": "DEFINICION"
}
```

---

## 📚 RESÚMENES DE LEYES

### `POST /agents/resumen`

Crea resumen estructurado de una ley usando MCP.

#### Request

```json
{
  "ley_id": "LGSS",
  "tema": "Seguridad Social",
  "longitud": "MEDIO",
  "incluir_ejemplos": true
}
```

**Longitudes:**
- `CORTO` - 500 caracteres
- `MEDIO` - 1500 caracteres  
- `LARGO` - 3000 caracteres

#### Response

```json
{
  "status": "success",
  "data": {
    "tema": "LGSS",
    "resumen": "La Ley General de la Seguridad Social (Real Decreto Legislativo 8/2015) es la norma fundamental que regula el sistema de Seguridad Social en España. Establece los principios básicos, la estructura del sistema, los regímenes de cotización, las prestaciones económicas y sanitarias, y los procedimientos administrativos...",
    "conceptos_clave": {
      "prestación": "Derecho económico reconocido por la Seguridad Social ante determinadas contingencias",
      "cotización": "Aportación obligatoria de empresarios y trabajadores para financiar el sistema",
      "jubilación": "Prestación económica vitalicia por cese en la actividad laboral por edad",
      "incapacidad": "Situación de imposibilidad temporal o permanente para el trabajo"
    },
    "referencias": [
      "BOE-A-2015-11724",
      "BOE-A-2019-12345",
      "BOE-A-2020-67890"
    ],
    "longitud": "MEDIO",
    "fecha_creacion": "2025-12-16T15:30:45"
  },
  "longitud": "MEDIO"
}
```

---

## 🧠 MAPAS MENTALES

### `POST /agents/mapa_mental`

Crea mapa mental estructurado con formato Mermaid.

#### Request

```json
{
  "tema": "Prestaciones Seguridad Social",
  "profundidad": 3,
  "formato": "MERMAID"
}
```

#### Response

```json
{
  "status": "success",
  "data": {
    "tema_central": "Prestaciones Seguridad Social",
    "nodos": [
      {
        "id": 1,
        "titulo": "Prestaciones Contributivas",
        "contenido": "Prestaciones que requieren un período mínimo de cotización previa. Incluyen jubilación, incapacidad permanente, muerte y supervivencia...",
        "nivel": 1,
        "hijos": []
      },
      {
        "id": 2,
        "titulo": "Prestaciones No Contributivas",
        "contenido": "Prestaciones asistenciales que no requieren cotización previa. Se financian con cargo a los Presupuestos Generales del Estado...",
        "nivel": 1,
        "hijos": []
      }
    ],
    "formato": "MERMAID",
    "profundidad": 3,
    "mermaid": "graph TD\n    A[Prestaciones Seguridad Social]\n    A --> B1[Prestaciones Contributivas]\n    A --> B2[Prestaciones No Contributivas]\n"
  },
  "formato": "MERMAID",
  "profundidad": 3
}
```

---

## 🎯 ENDPOINT UNIVERSAL

### `POST /agents/crear`

Endpoint universal que puede crear cualquier tipo de contenido.

#### Request

```json
{
  "tipo": "simulacro",
  "tema": "Desempleo",
  "nivel": "AVANZADO",
  "cantidad": 1,
  "usuario_id": 456,
  "personalizar": true,
  "usar_rag": true,
  "formato_oficial": true
}
```

**Tipos disponibles:**
- `simulacro` - Examen completo oficial
- `caso_practico` - Caso jurídico
- `flashcards` - Tarjetas de estudio
- `resumen` - Resumen de ley
- `mapa_mental` - Diagrama conceptual
- `esquema` - Esquema estructurado

#### Response

```json
{
  "status": "success",
  "tipo": "simulacro",
  "data": {
    // Contenido específico según el tipo
  },
  "metadatos": {
    "tiempo_generacion": "2-5s",
    "fuente": "MCP + RAG + COSM",
    "costo": 0.0,
    "personalizado": true
  }
}
```

---

## 🏥 HEALTH CHECK

### `GET /agents/health`

Verifica el estado de la factoría de agentes.

#### Response

```json
{
  "status": "healthy",
  "mcp_server": "connected",
  "collections": 2,
  "agents_available": [
    "simulacro_oficial",
    "caso_practico",
    "flashcards",
    "resumen_ley",
    "mapa_mental"
  ],
  "estrategia": "COSM (Create Once, Serve Many)",
  "formato_oficial": "BOE-A-2024-11403"
}
```

---

## 🚀 GENERACIÓN MASIVA (COSM)

### `POST /agents/batch/generar_inicial`

Ejecuta la generación masiva de contenido para la estrategia COSM.

**⚠️ IMPORTANTE:** Ejecutar solo UNA VEZ. Coste estimado: €18.

#### Response

```json
{
  "status": "started",
  "message": "Generación masiva iniciada en background",
  "estimado": {
    "simulacros": 1000,
    "casos": 500,
    "flashcards": 5000,
    "resumenes": 50,
    "tiempo_estimado": "2-3 horas",
    "coste_estimado": "€18"
  }
}
```

---

## 💰 ESTRATEGIA COSM

### Ahorro de Costes

```
ANTES (Generativo por usuario):
├─ Usuario pide simulacro → GenAI crea (+€0.007)
├─ 1000 usuarios → €7/día
└─ TOTAL: €210/mes

DESPUÉS (COSM):
├─ Crear 1000 simulacros UNA VEZ → €7
├─ Servir desde BD → €0/usuario
└─ TOTAL: €7 (una sola vez) + €0/mes

AHORRO: 99.7% después del primer mes
```

### Personalización Sin Coste

```python
# Mismo simulacro, orden diferente por usuario
def personalizar_simulacro(usuario_id, simulacro_base):
    random.seed(hash(usuario_id))  # Determinístico
    preguntas_mezcladas = random.sample(simulacro_base['preguntas'], len(preguntas_base['preguntas']))
    return simulacro_base.update(preguntas=preguntas_mezcladas)
```

---

## 🔗 INTEGRACIÓN MCP

### Herramientas MCP Utilizadas

| Herramienta | Uso en Agent Factory |
|-------------|---------------------|
| `mcp_opositaia_search_rag` | Buscar contexto para generar contenido |
| `mcp_opositaia_search_jurisprudence` | Incluir jurisprudencia en casos |
| `mcp_opositaia_get_law_summary` | Crear resúmenes de leyes |
| `mcp_opositaia_list_collections` | Health check y estadísticas |

### Flujo de Generación

```
1. Request → Agent Factory
2. Agent Factory → MCP Server (buscar contexto)
3. MCP Server → Qdrant Cloud (18,470 chunks)
4. Qdrant → MCP Server (resultados relevantes)
5. MCP Server → Agent Factory (contexto estructurado)
6. Agent Factory → Mistral/Gemini (generar contenido)
7. Agent Factory → Response (contenido + metadatos)
```

---

## 🧪 TESTING

### Ejecutar Tests

```bash
# Instalar dependencias
pip install httpx pytest

# Ejecutar test completo
python backend/examples/test_agent_factory.py

# Test específico
pytest backend/tests/test_agent_factory.py
```

### Ejemplo de Uso

```python
import httpx

async def crear_simulacro():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/agents/simulacro", json={
            "tema": "Seguridad Social",
            "nivel": "INTERMEDIO",
            "formato_oficial": True,
            "usuario_id": 123
        })
        
        simulacro = response.json()
        print(f"Simulacro creado: {simulacro['data']['id']}")
        return simulacro
```

---

## 📊 MÉTRICAS Y MONITOREO

### KPIs Importantes

- **Tiempo de respuesta:** <3s para generación, <100ms para servir desde BD
- **Coste por usuario:** €0.00 después de generación inicial
- **Calidad:** Contenido basado en 18,470 chunks legales verificados
- **Personalización:** 100% de usuarios reciben contenido único sin coste adicional

### Logs

```bash
# Ver logs de generación
tail -f backend/logs/agent_factory.log

# Ver métricas MCP
curl http://localhost:8000/mcp/health

# Ver estadísticas COSM
curl http://localhost:8000/contenido/stats
```

---

## 🚀 PRÓXIMOS PASOS

1. **Implementar BD PostgreSQL** para estrategia COSM completa
2. **Integrar con frontend React** - componentes para cada tipo de contenido
3. **Añadir más tipos de agentes** - esquemas, cronogramas, etc.
4. **Optimizar personalización** - más variaciones sin coste
5. **Métricas avanzadas** - A/B testing, analytics de uso

---

**Documentación creada:** 16 Diciembre 2025  
**Versión API:** 1.0  
**Estado:** ✅ Funcional con MCP + COSM