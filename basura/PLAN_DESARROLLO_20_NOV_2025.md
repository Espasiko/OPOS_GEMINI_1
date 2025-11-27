# 📋 PLAN DE DESARROLLO - 20 NOVIEMBRE 2025

**Fecha**: 20 Noviembre 2025  
**Versión**: 2.0 (Realista con deficiencias actuales)  
**Estado**: 📋 PLANIFICADO

---

## 🎯 ESTADO ACTUAL REAL DEL PROYECTO

### ✅ LO QUE FUNCIONA (100%)

#### **BACKEND - FastAPI**
- ✅ **RAG System**: 7,833 chunks indexados en Qdrant
- ✅ **RoBERTalex**: Embeddings especializados en legal español
- ✅ **2 Capas jerárquicas**:
  - Capa 1: Normativa oficial (Constitución, LGSS, RDs)
  - Capa 3: Materiales de estudio
- ✅ **4 Routers funcionando**:
  - `/api/v2/rag/*` - Búsqueda RAG (rag_v2.py)
  - `/chat/*` - Chat con Mistral (chat.py)
  - `/upload/*` - Upload de archivos (upload.py)
  - `/health` - Health checks
- ✅ **Tests unitarios**: 7/7 pasando (test_chat.py, test_upload.py)
- ✅ **Mistral 8B**: Desplegado en VPS (147.93.95.67:8001)
- ✅ **Servidor corriendo**: http://localhost:8000

#### **FRONTEND - React + TypeScript**
- ✅ **16 vistas completas**:
  - Chat, Casos Prácticos, Simulacros
  - Búsqueda RAG, Temario, Mapas Mentales
  - Esquemas, Resúmenes, Comparador
  - Flashcards, Plan Estudios, Progreso
  - Configuración, Guía Usuario, Backend Test
- ✅ **3 servicios**:
  - `geminiService.ts` - Gemini API (actual)
  - `backendService.ts` - Backend FastAPI (nuevo)
  - `vpsService.ts` - VPS Mistral (legacy)
- ✅ **Integración Gemini**: 2.5 Flash + Pro + Imagen
- ✅ **UI/UX**: Bootstrap responsive
- ✅ **BackendTestView**: Componente de testing

#### **DOCUMENTACIÓN**
- ✅ **67 archivos .md**: Documentación exhaustiva
- ✅ **AI Specs**: 23 archivos en ai-specs/
- ✅ **Guías completas**: Setup, desarrollo, testing

---

## ⚠️ DEFICIENCIAS ACTUALES (LO QUE NO FUNCIONA)

### 🔴 CRÍTICAS (Bloquean funcionalidad)

#### **1. CHAT NO USA BACKEND**
**Problema**: `ChatView.tsx` usa solo `geminiService`, NO usa el backend FastAPI ni Mistral
```typescript
// ChatView.tsx línea ~200
const response = await geminiService.sendMessage(message); // ❌ Solo Gemini
```
**Impacto**: 
- Backend FastAPI no se usa en producción
- Mistral VPS no se usa ($15/mes desperdiciados)
- RAG no se integra en el chat principal
- Límites de Gemini API se agotan rápido

**Solución**: Migrar ChatView a usar `backendService` (Sprint 8)

---

#### **2. DUPLICACIÓN DE SERVICIOS**
**Problema**: Existen 2 servicios que hacen lo mismo:
- `vpsService.ts` (legacy, 87 líneas)
- `backendService.ts` (nuevo, 350 líneas)

**Impacto**:
- Confusión sobre cuál usar
- Mantenimiento duplicado
- Código muerto

**Solución**: Eliminar `vpsService.ts`, consolidar en `backendService.ts`

---

#### **3. BACKENDTESTVIEW EN UI DE USUARIO**
**Problema**: Componente de testing visible en sidebar para usuarios finales
```typescript
// Sidebar.tsx
<button onClick={() => onViewChange(AppView.BACKEND_TEST)}>
  🧪 Backend Test
</button>
```
**Impacto**:
- Confunde a usuarios (no es una feature)
- Expone endpoints internos
- UI poco profesional

**Solución**: Mover a modo desarrollo o eliminar del sidebar

---

### 🟡 IMPORTANTES (Afectan calidad)

#### **4. ESLINT WARNINGS**
**Problema**: 5 warnings en `vpsService.ts`:
- 2x Trailing spaces
- 3x `any` types sin tipar

**Impacto**: Código no profesional, posibles bugs

**Solución**: Arreglar en 5 minutos

---

#### **5. CORS ABIERTO**
**Problema**: Backend acepta requests de cualquier origen
```python
# main.py línea 52
allow_origins=["*"],  # TODO: Restrict in production
```
**Impacto**: Vulnerabilidad de seguridad

**Solución**: Restringir a dominios específicos

---

#### **6. CACHÉ EN MEMORIA**
**Problema**: Upload router usa caché en memoria
```python
# upload.py
document_cache = {}  # Se pierde al reiniciar
```
**Impacto**: Documentos se pierden al reiniciar backend

**Solución**: Implementar Redis o persistencia (Sprint 9)

---

#### **7. SIN RATE LIMITING**
**Problema**: No hay límites de requests por usuario

**Impacto**: Vulnerable a abuso, costes descontrolados

**Solución**: Implementar rate limiting (Sprint 9)

---

### 🟢 MENORES (Mejoras futuras)

8. Tailwind CDN en producción (warning)
9. Metadata incompleta en algunos chunks (esperado)
10. Mistral VPS a veces no responde (timeout)

---

## 🚀 ARQUITECTURA RECOMENDADA

### **HOSTING OPTIMIZADO (Tu recomendación)**

```
┌─────────────────────────────────────────┐
│  VERCEL (Gratis)                        │
│  - Landing page (Next.js/React)         │
│  - UI de la app (React)                 │
│  - CDN global                           │
│  URL: https://opositaia.vercel.app      │
└─────────────────────────────────────────┘
                ↓ API calls
┌─────────────────────────────────────────┐
│  VPS HOSTINGER (8GB → 16GB)             │
│  - Mistral 8B                           │
│  - FastAPI backend                      │
│  - Qdrant                               │
│  - Orquestador Multi-Agente             │
│  URL: https://api.opositaia.com         │
└─────────────────────────────────────────┘
                ↓ Embeddings
┌─────────────────────────────────────────┐
│  HUGGING FACE SPACES (Gratis)           │
│  - RoBERTalex embeddings                │
│  - API pública                          │
│  URL: https://opositaia-embed.hf.space  │
└─────────────────────────────────────────┘
```

**Costes mensuales:**
- Vercel: $0/mes
- HF Spaces: $0/mes
- VPS 8GB: $10-20/mes (actual)
- VPS 16GB: $30-40/mes (futuro)

**Total: $10-40/mes** 🎯

---

## 🤖 ARQUITECTURA MULTI-AGENTE INTELIGENTE

### **1. AGENTE ORQUESTADOR/CLASIFICADOR**

**Función**: Decidir qué modelo usar según complejidad

```
Usuario → Orquestador → Clasifica:
                     ├─ 80% → Mistral 8B (gratis, VPS)
                     └─ 20% → Gemini Pro (complejo, API)
```

**Criterios de clasificación:**
- **Mistral 8B** (gratis):
  - Preguntas simples sobre leyes
  - Explicaciones de conceptos
  - Chat conversacional
  - Búsquedas RAG básicas
  
- **Gemini Pro** (API):
  - Casos prácticos complejos
  - Análisis jurídico profundo
  - Simulacros de examen
  - Generación de contenido creativo

**Beneficio**: Ahorro 80% tokens Gemini = Escalable a 1000+ usuarios

---

### **2. AGENTE SUPERVISOR/VALIDADOR**

**Función**: Validar respuestas y manejar errores

```
Respuesta → Supervisor → Valida:
                      ├─ ¿JSON correcto?
                      ├─ ¿Campos requeridos?
                      ├─ ¿Confianza > 0.7?
                      └─ Si falla → Reintenta (2x) → Escala a Gemini
```

**Beneficio**: Sistema robusto, 0 errores en producción

---

### **3. AGENTE QA (QUALITY ASSURANCE)**

**Función**: Verificar respuestas contra fuentes oficiales

```
Respuesta → QA Agent → Valida con RAG → Si dudoso → BOE API
```

**Beneficio**: Respuestas 100% verificadas

---

### **4. CONFIGURACIÓN YAML PARA AGENTES**

**Archivo**: `backend/config/agents.yaml`

```yaml
agents:
  - name: "mistral_agent"
    enabled: true
    priority: 1
    use_cases: 
      - "simple_question"
      - "explanation"
      - "chat"
    config:
      url: "http://147.93.95.67:8001"
      model: "mistral-8b"
      temperature: 0.7
      max_tokens: 2000
    rate_limit:
      max_requests_per_minute: 60
  
  - name: "gemini_pro_agent"
    enabled: true
    priority: 2
    use_cases:
      - "practical_case"
      - "complex_analysis"
      - "exam_simulation"
    config:
      api_key: "${GEMINI_API_KEY}"
      model: "gemini-2.0-flash-exp"
      temperature: 0.8
    rate_limit:
      max_requests_per_day: 100
  
  - name: "rag_agent"
    enabled: true
    priority: 0  # Siempre se ejecuta primero
    config:
      qdrant_url: "http://localhost:6333"
      collection: "opositaia_leyes_seguridad_social"
      top_k: 3
      min_score: 0.5
```

**Beneficio**: Modificar agentes sin tocar código Python

---

## 📅 PLAN DE DESARROLLO (4 SEMANAS)

### **SPRINT 8: ARREGLAR DEFICIENCIAS + ORQUESTADOR** (Semana 1)

**Nota**: Siguiendo principios de **base-standards.mdc**:
- ✅ Small tasks, one at a time (baby steps)
- ✅ Test-Driven Development (TDD)
- ✅ Incremental changes
- ✅ All code and commits in English

#### **Día 1: Limpieza de Código (2 horas) - BABY STEPS**

**Task 1.1: Fix ESLint warnings** (15 min)
- [ ] Fix trailing spaces in `vpsService.ts` (lines 2, 87)
- [ ] Replace `any` types with proper types (lines 12, 19, 28)
- [ ] Run `npm run lint` to verify
- [ ] Commit: "fix: resolve ESLint warnings in vpsService"

**Task 1.2: Consolidate services** (30 min)
- [ ] Search for `vpsService` imports: `grep -r "vpsService" src/`
- [ ] Replace all imports with `backendService`
- [ ] Delete `services/vpsService.ts`
- [ ] Run `npm run type-check` to verify
- [ ] Commit: "refactor: remove duplicate vpsService, use backendService"

**Task 1.3: Hide BackendTestView from users** (15 min)
- [ ] Remove BackendTestView button from `Sidebar.tsx`
- [ ] Keep component file (for dev use)
- [ ] Run `npm run build` to verify
- [ ] Commit: "refactor: hide BackendTestView from user menu"

**Task 1.4: Restrict CORS** (10 min)
- [ ] Update `backend/main.py` CORS config
- [ ] Change `allow_origins=["*"]` to specific origins
- [ ] Add environment variable `CORS_ORIGINS`
- [ ] Test with frontend
- [ ] Commit: "security: restrict CORS to specific origins"

#### **Día 2-3: Migrar ChatView a Backend (8 horas) - TDD APPROACH**

**Task 2.1: Write failing tests first** (1 hora)
- [ ] Create `components/__tests__/ChatView.test.tsx`
- [ ] Test: Chat sends message to backend
- [ ] Test: Streaming SSE displays chunks
- [ ] Test: RAG toggle works
- [ ] Test: Sources display correctly
- [ ] Run tests (should FAIL) ✅
- [ ] Commit: "test: add failing tests for ChatView backend integration"

**Task 2.2: Implement backend integration** (3 horas)
- [ ] Modify `ChatView.tsx` to use `backendService.sendChatMessage()`
- [ ] Replace `geminiService` imports with `backendService`
- [ ] Add state for `useRag` toggle
- [ ] Run tests (should PASS some) ✅
- [ ] Commit: "feat: integrate ChatView with backendService"

**Task 2.3: Implement SSE streaming** (2 horas)
- [ ] Use `backendService.sendChatMessageStream()`
- [ ] Handle SSE events in UI
- [ ] Display chunks as they arrive
- [ ] Run tests (should PASS more) ✅
- [ ] Commit: "feat: add SSE streaming to ChatView"

**Task 2.4: Display RAG sources** (1 hora)
- [ ] Add sources section to UI
- [ ] Format sources (norma, artículo, score)
- [ ] Add toggle "Show Sources"
- [ ] Run tests (should PASS all) ✅
- [ ] Commit: "feat: display RAG sources in ChatView"

**Task 2.5: Gemini fallback** (1 hora)
- [ ] Add try-catch for backend errors
- [ ] Fallback to `geminiService` if backend fails
- [ ] Show warning message to user
- [ ] Test fallback manually
- [ ] Commit: "feat: add Gemini fallback for ChatView"

#### **Día 4-5: Orquestador Inteligente (8 horas) - TDD + SOLID**

**Task 4.1: Write failing tests** (1 hora)
- [ ] Create `backend/tests/test_orchestrator.py`
- [ ] Test: Simple question → Mistral
- [ ] Test: Complex case → Gemini
- [ ] Test: Metrics tracking
- [ ] Run tests (should FAIL) ✅
- [ ] Commit: "test: add failing tests for orchestrator agent"

**Task 4.2: Create orchestrator interface** (1 hora)
- [ ] Create `backend/agents/orchestrator_agent.py`
- [ ] Define `IOrchestrator` interface (DIP principle)
- [ ] Define `classify_complexity()` method
- [ ] Define `route_to_model()` method
- [ ] Commit: "feat: add orchestrator agent interface"

**Task 4.3: Implement complexity classifier** (2 horas)
- [ ] Implement `classify_complexity()` logic
- [ ] Rules: keywords, length, question type
- [ ] Return complexity score (0-1)
- [ ] Run tests (should PASS some) ✅
- [ ] Commit: "feat: implement complexity classifier"

**Task 4.4: Implement model routing** (2 horas)
- [ ] Implement `route_to_model()` logic
- [ ] If complexity < 0.5 → Mistral
- [ ] If complexity >= 0.5 → Gemini
- [ ] Handle errors and fallbacks
- [ ] Run tests (should PASS more) ✅
- [ ] Commit: "feat: implement model routing logic"

**Task 4.5: Add metrics tracking** (2 horas)
- [ ] Track model usage (Mistral vs Gemini)
- [ ] Track response times
- [ ] Track error rates
- [ ] Log metrics to file
- [ ] Run tests (should PASS all) ✅
- [ ] Commit: "feat: add metrics tracking to orchestrator"

#### **Día 6-7: Supervisor Agent (8 horas) - TDD + SRP**

**Task 6.1: Write failing tests** (1 hora)
- [ ] Create `backend/tests/test_supervisor.py`
- [ ] Test: Valid JSON passes
- [ ] Test: Invalid JSON retries
- [ ] Test: Max retries escalates
- [ ] Test: Required fields validation
- [ ] Run tests (should FAIL) ✅
- [ ] Commit: "test: add failing tests for supervisor agent"

**Task 6.2: Create supervisor interface** (1 hora)
- [ ] Create `backend/agents/supervisor_agent.py`
- [ ] Define `ISupervisor` interface (SRP principle)
- [ ] Define `validate_response()` method
- [ ] Define `retry_with_feedback()` method
- [ ] Commit: "feat: add supervisor agent interface"

**Task 6.3: Implement JSON validation** (2 horas)
- [ ] Implement `validate_json()` function
- [ ] Check JSON structure
- [ ] Check required fields
- [ ] Return validation errors
- [ ] Run tests (should PASS some) ✅
- [ ] Commit: "feat: implement JSON validation"

**Task 6.4: Implement retry logic** (2 horas)
- [ ] Implement `retry_with_feedback()` function
- [ ] Max 2 retries
- [ ] Include validation errors in retry prompt
- [ ] Track retry count
- [ ] Run tests (should PASS more) ✅
- [ ] Commit: "feat: implement retry logic with feedback"

**Task 6.5: Implement escalation** (2 horas)
- [ ] If retries exhausted → escalate to Gemini
- [ ] Log escalation event
- [ ] Return final response or error
- [ ] Run tests (should PASS all) ✅
- [ ] Commit: "feat: implement escalation to Gemini"

**Entregables Sprint 8:**
- ✅ Chat usa backend + Mistral
- ✅ Orquestador decide modelo automáticamente
- ✅ 80% requests van a Mistral (ahorro tokens)
- ✅ Sistema robusto con validación

---

### **SPRINT 9: CONFIGURACIÓN YAML + QA AGENT** (Semana 2)

#### **Día 1-2: Sistema de Configuración YAML (6 horas)**
- [ ] Crear `backend/config/agents.yaml`
- [ ] Crear `backend/config/loader.py`
- [ ] Loader dinámico de agentes
- [ ] Hot-reload de configuración
- [ ] Validación de esquemas
- [ ] Commit: "feat: add YAML configuration system"

#### **Día 3-4: Migrar Agentes a YAML (6 horas)**
- [ ] Migrar RAG Agent a YAML
- [ ] Migrar Orquestador a YAML
- [ ] Migrar Supervisor a YAML
- [ ] Documentación de configuración
- [ ] Commit: "refactor: migrate agents to YAML config"

#### **Día 5-7: QA Agent (10 horas)**
- [ ] Crear `backend/agents/qa_agent.py`
- [ ] Validación con RAG local
- [ ] Integración BOE API (casos dudosos)
- [ ] Métricas de calidad (precision, recall)
- [ ] Tests unitarios
- [ ] Commit: "feat: add QA agent for quality assurance"

**Entregables Sprint 9:**
- ✅ Agentes configurables por YAML
- ✅ Hot-reload sin reiniciar servidor
- ✅ QA valida respuestas automáticamente
- ✅ Documentación completa

---

### **SPRINT 10: OPTIMIZACIÓN HOSTING** (Semana 3)

#### **Día 1-2: Hugging Face Spaces (6 horas)**
- [ ] Crear Space en HF
- [ ] Desplegar RoBERTalex
- [ ] API de embeddings
- [ ] Tests de conectividad
- [ ] Actualizar backend para usar HF
- [ ] Commit: "feat: deploy embeddings to HF Spaces"

#### **Día 3-4: Vercel Deployment (6 horas)**
- [ ] Crear proyecto en Vercel
- [ ] Configurar build de React
- [ ] Deploy automático desde GitHub
- [ ] Configurar variables de entorno
- [ ] Tests en producción
- [ ] Commit: "deploy: setup Vercel deployment"

#### **Día 5-7: VPS Optimization (10 horas)**
- [ ] Optimizar Mistral 8B (GGUF quantization)
- [ ] Configurar Nginx reverse proxy
- [ ] SSL certificates (Let's Encrypt)
- [ ] Monitoring con Prometheus
- [ ] Logs estructurados
- [ ] Backup automático Qdrant
- [ ] Commit: "ops: optimize VPS infrastructure"

**Entregables Sprint 10:**
- ✅ RoBERTalex en HF Spaces (gratis)
- ✅ UI en Vercel con CDN global
- ✅ VPS optimizado para Mistral
- ✅ Arquitectura escalable

---

### **SPRINT 11: INTEGRACIÓN FINAL + MEMES** (Semana 4)

#### **Día 1-2: Integración Completa (6 horas)**
- [ ] Conectar frontend Vercel con backend VPS
- [ ] Configurar CORS para producción
- [ ] Rate limiting por usuario
- [ ] Caché Redis para uploads
- [ ] Tests E2E completos
- [ ] Commit: "feat: complete frontend-backend integration"

#### **Día 3-4: Memes Sin Agotar Gemini (6 horas)**
- [ ] Integrar Stable Diffusion HF API
- [ ] Sistema de caché inteligente (100 memes pre-generados)
- [ ] Fallback a Craiyon (ilimitado)
- [ ] Rate limiting por usuario (5 memes/día)
- [ ] Commit: "feat: add meme generation without Gemini"

#### **Día 5-6: Testing y Optimización (8 horas)**
- [ ] Load testing (100 usuarios concurrentes)
- [ ] Performance optimization
- [ ] Security audit
- [ ] Documentación final
- [ ] Commit: "test: comprehensive load and security testing"

#### **Día 7: Deploy a Producción (4 horas)**
- [ ] Deploy final a Vercel
- [ ] Configurar dominio personalizado
- [ ] Monitoring y alertas
- [ ] Rollback plan
- [ ] Commit: "deploy: production release v1.0"

**Entregables Sprint 11:**
- ✅ Sistema completo en producción
- ✅ Memes sin agotar Gemini
- ✅ Soporta 1000+ usuarios
- ✅ Costes < $40/mes

---

## 🎯 OBJETIVOS POR SPRINT

### **Sprint 8:**
- ✅ Chat integrado con backend
- ✅ Orquestador inteligente funcionando
- ✅ 80% requests a Mistral (ahorro tokens)
- ✅ Sistema robusto con validación

### **Sprint 9:**
- ✅ Configuración YAML completa
- ✅ Agentes modificables sin código
- ✅ QA valida respuestas automáticamente
- ✅ Hot-reload de configuración

### **Sprint 10:**
- ✅ RoBERTalex en cloud (gratis)
- ✅ UI en Vercel (CDN global)
- ✅ VPS optimizado
- ✅ Arquitectura escalable

### **Sprint 11:**
- ✅ Sistema en producción
- ✅ Memes sin agotar Gemini
- ✅ Soporta 1000+ usuarios
- ✅ Documentación completa

---

## 📊 MÉTRICAS DE ÉXITO

### **Performance:**
- [ ] Respuesta < 3 segundos (90% casos)
- [ ] Uptime > 99.5%
- [ ] Soporte 100+ usuarios concurrentes

### **Calidad:**
- [ ] Precisión respuestas > 95%
- [ ] Fuentes verificadas automáticamente
- [ ] 0 errores JSON/formato

### **Costes:**
- [ ] <100 tokens Gemini/día (promedio)
- [ ] Hosting < $40/mes total
- [ ] Escalable sin costes adicionales

### **UX:**
- [ ] Tiempo carga < 2 segundos
- [ ] Mobile responsive 100%
- [ ] Accesibilidad WCAG 2.1

---

## 💰 ESTIMACIÓN DE COSTES

### **Desarrollo (4 semanas):**
- Tiempo: 4 semanas × 40 horas = 160 horas
- Complejidad: Media-Alta
- Riesgo: Bajo (arquitectura probada)

### **Hosting (mensual):**
```
VPS 8GB (actual):     $15/mes
VPS 16GB (futuro):    $35/mes
Vercel:               $0/mes
HF Spaces:            $0/mes
Dominio:              $12/año = $1/mes

Total: $16-36/mes
```

### **APIs (mensual):**
```
Gemini (optimizado):  $0/mes (dentro cuota gratuita)
Mistral (self-host):  $0/mes
BOE API:              $0/mes
Stable Diffusion HF:  $0/mes

Total: $0/mes
```

**COSTE TOTAL: $16-36/mes** 🎯

---

## 🚨 RIESGOS Y MITIGACIONES

### **Riesgo 1: Mistral VPS caído**
**Probabilidad**: Media  
**Impacto**: Alto  
**Mitigación**: 
- Fallback automático a Gemini
- Health check cada 30s
- Alertas por email

### **Riesgo 2: Cuota Gemini agotada**
**Probabilidad**: Baja (con orquestador)  
**Impacto**: Alto  
**Mitigación**:
- Orquestador envía 80% a Mistral
- Rate limiting por usuario
- Caché de respuestas frecuentes

### **Riesgo 3: HF Spaces lento**
**Probabilidad**: Media  
**Impacto**: Medio  
**Mitigación**:
- Caché de embeddings frecuentes
- Timeout de 5s
- Fallback a embeddings locales

---

## ✅ PRÓXIMOS PASOS INMEDIATOS

### **HOY (20 Nov):**
1. ✅ Leer y aprobar este plan
2. ⏰ Arreglar ESLint warnings (5 min)
3. ⏰ Eliminar `vpsService.ts` (10 min)
4. ⏰ Mover `BackendTestView` a dev mode (15 min)
5. ⏰ Backup Qdrant (15 min)

### **MAÑANA (21 Nov):**
1. 🚀 Iniciar Sprint 8: Migrar ChatView
2. 📝 Modificar `ChatView.tsx`
3. 🧪 Tests de integración

### **ESTA SEMANA:**
1. 🎯 Completar Sprint 8
2. 📊 Métricas de ahorro de tokens
3. 🔍 Validación con usuarios beta

---

## 📝 CRITERIOS DE ACEPTACIÓN FINAL

### **Sistema Completado cuando:**
- [ ] Chat usa backend + Mistral (no solo Gemini)
- [ ] Orquestador decide modelo automáticamente
- [ ] 80% requests van a Mistral
- [ ] Sistema soporta 1000+ usuarios
- [ ] Costes < $40/mes total
- [ ] Uptime > 99.5%
- [ ] Documentación completa
- [ ] Ready para lanzamiento público

---

## 📞 CONTACTO Y SOPORTE

**Proyecto**: OpositAIA  
**Repositorio**: GitHub (privado)  
**Documentación**: 67 archivos .md  
**Estado**: Sprint 7 completado, Sprint 8 planificado

---

## 📖 MEJORES PRÁCTICAS APLICADAS

Este plan sigue los estándares definidos en `ai-specs/specs/`:

### **1. Base Standards (base-standards.mdc)**
- ✅ **Small tasks, one at a time**: Cada día dividido en tareas de 1-2 horas
- ✅ **Test-Driven Development**: Tests escritos ANTES de implementar
- ✅ **Type Safety**: Todo el código TypeScript/Python tipado
- ✅ **Clear Naming**: Nombres descriptivos en inglés
- ✅ **Incremental Changes**: Cambios pequeños y frecuentes
- ✅ **English Only**: Código, commits, docs en inglés

### **2. OpositaIA Standards (opositaia-standards.mdc)**
- ✅ **Service Layer Pattern**: Todo pasa por `backendService.ts`
- ✅ **Component Patterns**: Componentes React consistentes
- ✅ **Type Definitions**: Tipos en `types.ts`
- ✅ **Documentation Updates**: Actualizar docs con cada feature
- ✅ **Git Workflow**: Commits descriptivos en inglés

### **3. Backend Standards (backend-standards.mdc)**
- ✅ **Domain-Driven Design**: Separación clara de capas
- ✅ **SOLID Principles**:
  - **SRP**: Cada clase una responsabilidad
  - **OCP**: Abierto a extensión, cerrado a modificación
  - **DIP**: Dependencias en abstracciones (interfaces)
- ✅ **Repository Pattern**: Acceso a datos encapsulado
- ✅ **Error Handling**: Manejo consistente de errores
- ✅ **Logging Standards**: Logs estructurados

### **4. Testing Standards**
- ✅ **Unit Testing**: Tests para cada función
- ✅ **Integration Testing**: Tests E2E
- ✅ **Test Coverage**: >80% backend, >70% frontend
- ✅ **TDD Approach**: Red → Green → Refactor

### **5. API Design Standards**
- ✅ **RESTful Naming**: Endpoints consistentes
- ✅ **JSON Format**: Request/response en JSON
- ✅ **Status Codes**: HTTP codes apropiados
- ✅ **CORS Configuration**: Orígenes específicos

### **6. Security Best Practices**
- ✅ **Input Validation**: Validar todos los inputs
- ✅ **Environment Variables**: Secrets en .env
- ✅ **CORS Restricted**: Solo orígenes permitidos
- ✅ **Error Messages**: No exponer detalles internos

---

## 🔄 METODOLOGÍA SCRUM APLICADA

### **Sprint Structure**
- **Duración**: 1 semana (7 días)
- **Daily Standup**: Revisar progreso diario
- **Sprint Review**: Día 7 de cada sprint
- **Sprint Retrospective**: Qué mejorar para el siguiente sprint

### **Story Points**
- **1 punto**: 1-2 horas (Task pequeña)
- **2 puntos**: 3-4 horas (Task media)
- **3 puntos**: 5-8 horas (Task grande)
- **5 puntos**: 1-2 días (Feature completa)

### **Definition of Done**
Para considerar una tarea completada:
- [ ] Código implementado
- [ ] Tests escritos y pasando
- [ ] Type-check sin errores
- [ ] ESLint sin warnings
- [ ] Documentación actualizada
- [ ] Commit con mensaje descriptivo
- [ ] Code review (si aplica)

### **Sprint Backlog**
Cada sprint tiene:
- **Sprint Goal**: Objetivo principal
- **User Stories**: Funcionalidades desde perspectiva del usuario
- **Tasks**: Tareas técnicas específicas
- **Acceptance Criteria**: Criterios de aceptación

---

## 📝 PLANTILLA DE COMMIT MESSAGES

Seguir formato estándar:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests
- `docs`: Cambios en documentación
- `style`: Cambios de formato (no afectan lógica)
- `perf`: Mejoras de performance
- `chore`: Tareas de mantenimiento

**Ejemplos:**
```bash
feat: add orchestrator agent for model routing

Implements intelligent routing between Mistral and Gemini
based on query complexity. Routes 80% to Mistral (free)
and 20% to Gemini (complex cases).

Closes #123
```

```bash
fix: resolve CORS issue in production

Restricts CORS to specific origins instead of wildcard.
Adds CORS_ORIGINS environment variable.

Fixes #456
```

```bash
test: add unit tests for supervisor agent

Adds tests for JSON validation, retry logic, and
escalation to Gemini. Coverage: 95%.
```

---

## 🎓 RECURSOS Y REFERENCIAS

### **Documentación del Proyecto**
- `README.md` - Guía general del proyecto
- `SETUP.md` - Instalación y configuración
- `docs/AI_AGENTS.md` - Definición de agentes AI
- `docs/ARCHITECTURE.md` - Arquitectura del sistema
- `docs/DATA_MODEL.md` - Modelo de datos

### **AI Specs**
- `ai-specs/specs/base-standards.mdc` - Estándares base
- `ai-specs/specs/opositaia-standards.mdc` - Estándares OpositaIA
- `ai-specs/specs/backend-standards.mdc` - Estándares backend
- `ai-specs/specs/frontend-standards.mdc` - Estándares frontend

### **Guías de Desarrollo**
- `ai-specs/specs/development_guide.md` - Guía de desarrollo
- `ai-specs/specs/documentation-standards.mdc` - Estándares de docs

---

*Plan creado: 20 Noviembre 2025*  
*Próxima revisión: 27 Noviembre 2025*  
*Versión: 2.0 (Realista + Best Practices)*
