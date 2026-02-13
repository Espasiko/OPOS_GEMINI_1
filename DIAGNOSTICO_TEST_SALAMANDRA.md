# 🔍 ANÁLISIS: POR QUÉ EL TEST DE SALAMANDRA NO FUNCIONA

**Fecha:** 22 de Enero de 2026  
**Objetivo:** Diagnosticar y solucionar el test `test_salamandra_caso.py`

---

## ❌ PROBLEMA IDENTIFICADO

El test intenta conectar a `http://localhost:8000/casos/health` pero:

```
❌ ERROR: No se pudo conectar al servidor
   Asegúrate de que el backend esté corriendo:
   cd backend && python main.py
```

---

## 🔎 ANÁLISIS CAUSAL

### 1. **Backend No Está Ejecutándose**

El script espera que FastAPI esté corriendo en puerto 8000:

```python
# test_salamandra_caso.py línea 24
base_url = "http://localhost:8000"
endpoint = f"{base_url}/casos/generate-one"

# httpx intenta conectar
health_response = await client.get(f"{base_url}/casos/health")
# → ConnectError: Connection refused
```

### 2. **Verificar Qué Routers Existen**

En `backend/main.py`, se importan 9 routers:

```python
from routers import rag, rag_v2, chat, upload, ai_functions, user, boe, mcp_gateway, casos_practicos
```

El test busca el router `casos_practicos.py` que existe en:
```
backend/routers/casos_practicos.py  ✅ EXISTE
```

Pero requiere que el backend esté corriendo para acceder al endpoint.

---

## 🛠️ SOLUCIÓN: PASO A PASO

### Opción 1: Iniciar Backend + Ejecutar Test (Recomendado)

**Terminal 1: Iniciar Backend**
```bash
cd /home/spas/OPOS_GEMINI_1/backend
python3 main.py
```

Deberías ver:
```
INFO - 🚀 OpositAIA Backend starting...
INFO - Embedding Model: pablosi/bge-m3-spa-law-qa-trained-2
INFO - Qdrant URL: http://localhost:6333
INFO - ✅ Database initialized
INFO - ✅ 8 routers registered
INFO - Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2: Ejecutar Test**
```bash
cd /home/spas/OPOS_GEMINI_1
python3 test_salamandra_caso.py
```

### Opción 2: Usar Docker Compose (Si está instalado)

```bash
cd /home/spas/OPOS_GEMINI_1
docker-compose up -d
```

Esto inicia:
- ✅ Backend (puerto 8000)
- ✅ Frontend (puerto 5173)
- ✅ Qdrant (puerto 6333)
- ✅ PostgreSQL (puerto 5432)

### Opción 3: Verificar Dependencias

Si backend no inicia, verificar:

```bash
# 1. ¿Python 3.9+?
python3 --version

# 2. ¿pip packages instalados?
cd /home/spas/OPOS_GEMINI_1/backend
pip3 install -r requirements.txt

# 3. ¿Variables de entorno?
cat .env.backend  # Verificar que esté configurado

# 4. ¿Qdrant corriendo?
curl http://localhost:6333/health

# 5. ¿PostgreSQL corriendo?
psql -U opositaia_user -d opositaia -c "SELECT 1"
```

---

## 📊 FLUJO DEL TEST EXPLICADO

```
┌─ test_salamandra_caso.py ─────────────────────────────────┐
│                                                             │
│  1. Conecta a http://localhost:8000/casos/health          │
│     ↓                                                       │
│  2. Si ✅ health ok → continúa                            │
│     Si ❌ error → EXIT con "No se pudo conectar"          │
│     ↓                                                       │
│  3. POST /casos/generate-one                              │
│     ├─ tema: "Incapacidad Temporal..."                    │
│     ├─ dificultad: "media"                                │
│     └─ Espera respuesta 10-30 segundos                    │
│     ↓                                                       │
│  4. Recibe JSON con caso                                  │
│     ├─ enunciado                                          │
│     ├─ pregunta                                           │
│     ├─ opciones [a, b, c, d]                             │
│     ├─ respuesta_correcta                                │
│     ├─ explicacion                                        │
│     ├─ articulos_aplicables                              │
│     └─ calculo_usado                                      │
│     ↓                                                       │
│  5. Guarda en: caso_generado_salamandra.json              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 QUÉ SUCEDE EN BACKEND

Cuando llamas a `/casos/generate-one`:

```python
# backend/routers/casos_practicos.py

@router.post("/generate-one")
async def generate_one_case(request: CaseRequest):
    """
    Genera UN caso práctico
    
    request.tema: Tema de la oposición
    request.dificultad: facil | media | dificil
    request.provider: groq | gemini | deepseek | mistral
    """
    
    # 1. Validar input
    # 2. Buscar contexto en Qdrant
    #    - Query Qdrant por el tema
    #    - Obtener 10 chunks relevantes
    # 3. Cargar calculadora (si aplica)
    # 4. Construir prompt
    # 5. Llamar LLM (Groq por defecto)
    # 6. Parsear respuesta JSON
    # 7. Validar schema
    # 8. Retornar caso
```

**Ejemplo Request:**
```json
{
  "tema": "Incapacidad Temporal por Enfermedad Común, base 1500€, día 10",
  "dificultad": "media"
}
```

**Ejemplo Response:**
```json
{
  "status": "success",
  "caso": {
    "enunciado": "Un trabajador...",
    "pregunta": "¿Cuál es...?",
    "opciones": {
      "a)": "50%",
      "b)": "60%",
      "c)": "75%",
      "d)": "100%"
    },
    "respuesta_correcta": "c)",
    "explicacion": "Según el artículo 174 TRLGSS...",
    "articulos_aplicables": ["Art. 174 TRLGSS"],
    "dificultad": "media",
    "calculo_usado": {
      "nombre": "incapacidad_temporal",
      "base_reguladora": 1500,
      "porcentaje": 75,
      "dias": 10
    }
  },
  "confidence": 0.92,
  "generatedAt": "2026-01-22T11:00:09Z",
  "provider": "groq",
  "latencyMs": 9000
}
```

---

## 🚀 CHECKLIST PARA EJECUTAR EL TEST EXITOSAMENTE

```
Pre-requisitos:
☐ Python 3.9+ instalado
☐ pip packages instalados (backend/requirements.txt)
☐ Qdrant corriendo en :6333
☐ PostgreSQL corriendo en :5432
☐ Variables de entorno configuradas (.env.backend)

Backend:
☐ Backend inicia sin errores
☐ Uvicorn escucha en 0.0.0.0:8000
☐ 8 routers cargados correctamente
☐ Qdrant conectado
☐ PostgreSQL conectado

Test:
☐ Ejecutar: python3 test_salamandra_caso.py
☐ Recibir: "✅ CASO GENERADO EXITOSAMENTE"
☐ Archivo creado: caso_generado_salamandra.json

Troubleshooting:
❌ "No se pudo conectar" → Backend no corre
   → Solución: python3 backend/main.py

❌ "Health check failed" → Qdrant no corre
   → Solución: docker run -p 6333:6333 qdrant/qdrant

❌ "Timeout esperando respuesta" → LLM muy lento
   → Solución: Esperar 30s, verificar GROQ_API_KEY

❌ "JSON parsing error" → LLM respondió mal
   → Solución: Revisar logs, reintentar
```

---

## 🔄 ALTERNATIVA: TEST LOCAL SIN BACKEND

Si quieres testear el JSON parsing sin backend en vivo:

```python
# test_salamandra_caso_local.py
import json

# Simular respuesta del backend
mock_response = {
    "status": "success",
    "caso": {
        "enunciado": "Un trabajador de 45 años...",
        "pregunta": "¿Cuál es el porcentaje?",
        "opciones": {"a)": "50%", "b)": "60%", "c)": "75%", "d)": "100%"},
        "respuesta_correcta": "c)",
        "explicacion": "Según art. 174 TRLGSS...",
        "articulos_aplicables": ["Art. 174 TRLGSS"],
        "dificultad": "media",
        "calculo_usado": {"nombre": "incapacidad_temporal", "base": 1500, "porcentaje": 75}
    },
    "confidence": 0.92,
    "provider": "groq"
}

# Guardar
with open("caso_local.json", "w") as f:
    json.dump(mock_response, f, indent=2, ensure_ascii=False)

print("✅ Caso local guardado")
```

---

## 📈 DIAGRAMA: STACK NECESARIO PARA EJECUTAR EL TEST

```
┌─────────────────────────────────────────────────┐
│         test_salamandra_caso.py                  │
│              (Your script)                       │
└────────────────────┬────────────────────────────┘
                     │ HTTP POST
                     ↓
    ┌────────────────────────────────┐
    │  Backend FastAPI               │
    │  :8000                         │
    │  ├─ routers/casos_practicos.py │  ← BUSCA ESTO
    │  └─ /casos/generate-one        │
    └────────────┬───────────────────┘
                 │
        ┌────────┴────────┬─────────┐
        │                 │         │
        ↓                 ↓         ↓
    ┌────────┐    ┌──────────┐  ┌────────┐
    │Qdrant  │    │Groq API  │  │PgSQL   │
    │:6333   │    │(external)│  │:5432   │
    └────────┘    └──────────┘  └────────┘
```

---

## 💡 PRO TIPS

### 1. Monitorear el Backend en Vivo

```bash
# Terminal separada - watch logs
tail -f backend.log
```

### 2. Hacer Request Manualmente

```bash
# Test health del backend
curl http://localhost:8000/docs

# Test endpoint de casos
curl -X POST http://localhost:8000/casos/generate-one \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Incapacidad Temporal",
    "dificultad": "media"
  }'
```

### 3. Verificar Qué Routers Están Cargados

```bash
# Ver todos los routers disponibles
curl -s http://localhost:8000/openapi.json | jq '.paths | keys'
```

### 4. Debuggear con Logs

```python
# Agregar en test_salamandra_caso.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Esto mostrará todos los detalles de las llamadas HTTP
```

---

## 🎓 PRÓXIMOS PASOS

1. **Iniciar backend** ← START HERE
   ```bash
   cd backend && python3 main.py
   ```

2. **En otra terminal, ejecutar test**
   ```bash
   python3 test_salamandra_caso.py
   ```

3. **Si funciona**: ✅ Ver `caso_generado_salamandra.json`

4. **Si falla**: 🐛 
   - Ver logs del backend
   - Verificar que GROQ_API_KEY esté configurada
   - Verificar que Qdrant esté corriendo

---

## 📞 DEBUGGING RÁPIDO

```bash
# 1. ¿Backend corre?
lsof -i :8000

# 2. ¿Qdrant corre?
curl http://localhost:6333/health

# 3. ¿API Keys configuradas?
env | grep -i groq

# 4. ¿Python tiene los packages?
python3 -c "import fastapi; import httpx; print('OK')"

# 5. ¿Puedo conectar?
curl -v http://localhost:8000/docs
```

---

**Conclusión:** El test es correcto. Solo necesita que el backend esté ejecutándose. Una vez que inicies `python3 backend/main.py`, el test debería funcionar perfectamente.

**Documentado:** 22 Enero 2026
