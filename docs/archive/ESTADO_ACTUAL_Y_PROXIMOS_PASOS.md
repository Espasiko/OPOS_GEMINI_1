# 📊 ESTADO ACTUAL Y PRÓXIMOS PASOS

**Fecha**: 20 Noviembre 2025  
**Hora**: 18:30

---

## ✅ LO QUE HEMOS LOGRADO HOY

### 1. Verificación Completa de Infraestructura
- ✅ **Mistral 7B encontrado** en VPS: `/home/ubuntu/opositor_ia/mistral-7b-instruct-v0.1.Q4_K_M.gguf`
- ✅ **Puerto correcto identificado**: 8080 (NO 8001)
- ✅ **Servidor llama.cpp corriendo**: PID 964, uptime 1 mes
- ✅ **Puerto 8080 accesible**: Test-NetConnection exitoso

### 2. Configuración Actualizada
- ✅ **backend/routers/chat.py**: Cambiado puerto de 8001 a 8080
- ✅ **backend/.env.backend**: Creado con configuración correcta
- ✅ **Backend reiniciado**: Proceso 19 corriendo

### 3. Tests Realizados
- ✅ **Health check backend**: `{"status":"healthy"}`
- ✅ **Chat health**: `{"status":"degraded","mistral":"down","rag":"up"}`
- ✅ **RAG funcionando**: 3 documentos encontrados para query de prueba

---

## ⚠️ PROBLEMA ACTUAL

### Mistral marca "down" en health check

**Posibles causas**:
1. **Timeout muy corto** en health check (5 segundos)
2. **Mistral tarda en responder** (modelo grande, CPU)
3. **Formato de request incorrecto** (llama.cpp vs OpenAI API)

**Evidencia**:
- Puerto 8080 SÍ es accesible (Test-NetConnection: True)
- Servidor llama.cpp SÍ está corriendo (ps aux: PID 964)
- API responde: `curl http://localhost:8080/v1/models` → OK

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

### PASO 1: Verificar Endpoint de Mistral (5 min)

Probar directamente desde el VPS:

```bash
ssh root@147.93.95.67
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral",
    "messages": [{"role": "user", "content": "Hola"}],
    "max_tokens": 50
  }'
```

### PASO 2: Ajustar Health Check (10 min)

Modificar `backend/routers/chat.py`:

```python
# Aumentar timeout
async with httpx.AsyncClient(timeout=30.0) as client:  # Era 5.0
    response = await client.get(f"{MISTRAL_URL}/v1/models")
```

### PASO 3: Test Chat con RAG (15 min)

Una vez Mistral responda:

```bash
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué es la incapacidad temporal?",
    "conversation_id": "test-123",
    "use_rag": true
  }'
```

---

## 🚀 PLAN COMPLETO (DESPUÉS DE ARREGLAR MISTRAL)

### SPRINT 8 - Semana 1

**Día 1: Limpieza + Mistral** (HOY)
- [x] Verificar infraestructura VPS
- [x] Encontrar Mistral (puerto 8080)
- [x] Actualizar configuración backend
- [ ] Arreglar health check Mistral
- [ ] Test chat con RAG funcionando

**Día 2-3: Migrar ChatView**
- [ ] Escribir tests TDD para ChatView
- [ ] Modificar ChatView.tsx para usar backendService
- [ ] Implementar streaming SSE
- [ ] Mostrar fuentes RAG
- [ ] Fallback a Gemini

**Día 4-5: Orquestador Inteligente**
- [ ] Crear `backend/agents/orchestrator_agent.py`
- [ ] Clasificador de complejidad
- [ ] Routing 80% Mistral, 20% Gemini
- [ ] Métricas de uso

**Día 6-7: Supervisor Agent**
- [ ] Crear `backend/agents/supervisor_agent.py`
- [ ] Validación JSON
- [ ] Sistema de reintentos
- [ ] Escalación a Gemini

### SPRINT 9 - Semana 2

**Configuración YAML**
- [ ] Crear `backend/config/agents.yaml`
- [ ] Loader dinámico de agentes
- [ ] Hot-reload
- [ ] QA Agent

---

## 📝 AGENTES YAML (DISEÑO)

### Estructura Propuesta

```yaml
# backend/config/agents.yaml
agents:
  - name: "mistral_vps"
    type: "llm"
    enabled: true
    priority: 1  # Más bajo = más prioritario
    use_cases:
      - "simple_question"
      - "explanation"
      - "chat"
    config:
      url: "http://147.93.95.67:8080"
      api_type: "llama_cpp"  # Compatible OpenAI
      model: "mistral"
      temperature: 0.7
      max_tokens: 2000
      timeout: 60
    rate_limit:
      max_requests_per_minute: 60
      max_requests_per_day: 10000
  
  - name: "gemini_flash"
    type: "llm"
    enabled: true
    priority: 2
    use_cases:
      - "complex_analysis"
      - "practical_case"
      - "exam_simulation"
    config:
      api_key: "${GEMINI_API_KEY}"
      model: "gemini-2.0-flash-exp"
      temperature: 0.8
      max_tokens: 4000
    rate_limit:
      max_requests_per_day: 1000
  
  - name: "rag_agent"
    type: "retrieval"
    enabled: true
    priority: 0  # Siempre se ejecuta primero
    config:
      qdrant_url: "http://localhost:6333"
      collection: "opositaia_leyes_seguridad_social"
      embedding_model: "PlanTL-GOB-ES/RoBERTalex"
      top_k: 3
      min_score: 0.5
  
  - name: "orchestrator"
    type: "orchestrator"
    enabled: true
    config:
      default_agent: "mistral_vps"
      fallback_agent: "gemini_flash"
      complexity_threshold: 0.5
      keywords_complex:
        - "caso práctico"
        - "simulacro"
        - "análisis complejo"
      keywords_simple:
        - "qué es"
        - "explica"
        - "define"
  
  - name: "supervisor"
    type: "validator"
    enabled: true
    config:
      max_retries: 2
      required_fields:
        - "response"
      min_confidence: 0.7
      escalate_on_failure: true
  
  - name: "qa_agent"
    type: "quality_assurance"
    enabled: true
    config:
      validate_with_rag: true
      check_boe_api: false  # Solo para casos dudosos
      min_quality_score: 0.8
```

---

## 🔍 DIAGNÓSTICO ACTUAL

### Backend Status
```json
{
  "status": "healthy",
  "embedding_model": "PlanTL-GOB-ES/RoBERTalex",
  "qdrant_url": "http://localhost:6333",
  "ollama_url": "http://localhost:11434"
}
```

### Chat Status
```json
{
  "status": "degraded",
  "mistral": "down",  // ← PROBLEMA
  "rag": "up",        // ← OK
  "mistral_url": "http://147.93.95.67:8080",
  "model": "mistral"
}
```

### RAG Status
- ✅ Qdrant: 7,833 chunks
- ✅ Embeddings: RoBERTalex cargado
- ✅ Búsqueda: 3 documentos encontrados
- ✅ Scores: >0.5

---

## 💡 DECISIÓN INMEDIATA

**Opción A: Arreglar health check Mistral** (RECOMENDADO)
- Tiempo: 15 minutos
- Aumentar timeout a 30s
- Probar endpoint correcto
- Verificar formato de request

**Opción B: Usar Ollama local temporalmente**
- Tiempo: 5 minutos
- Cambiar URL a localhost:11434
- Usar tinyllama
- Problema: Solo funciona con PC encendido

**Opción C: Solo Gemini temporalmente**
- Tiempo: 2 minutos
- Comentar código Mistral
- Problema: Límites de API

---

## ✅ RECOMENDACIÓN

1. **AHORA**: Arreglar health check Mistral (Opción A)
2. **HOY**: Test chat con RAG funcionando
3. **MAÑANA**: Migrar ChatView a backendService
4. **ESTA SEMANA**: Orquestador + Supervisor

---

**Documento creado**: 20 Noviembre 2025 18:30  
**Estado**: Mistral encontrado, configuración actualizada, health check pendiente  
**Próximo paso**: Arreglar timeout health check

