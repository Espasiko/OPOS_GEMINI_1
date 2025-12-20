# 📋 EVALUACIÓN DE MEJORAS PROPUESTAS - OpositaIA

**Fecha:** 25 Noviembre 2025  
**Objetivo:** Evaluar, ordenar y verificar estado de 12 mejoras propuestas

---

## 📊 RESUMEN EJECUTIVO

**Total mejoras:** 12  
**Implementadas:** 3 (25%)  
**Parcialmente implementadas:** 4 (33%)  
**Pendientes:** 5 (42%)

**Prioridad recomendada:**
1. 🔴 **CRÍTICAS** (4) - Impacto alto, esfuerzo medio
2. 🟠 **ALTAS** (5) - Impacto medio-alto, esfuerzo variable
3. 🟡 **MEDIAS** (3) - Impacto medio, esfuerzo alto

---

## 🔴 PRIORIDAD CRÍTICA (Implementar PRIMERO)

### 1. Botón de cerrar panel lateral
**Estado:** ❌ NO IMPLEMENTADO  
**Complejidad:** 🟢 BAJA (2 horas)  
**Impacto:** 🔴 ALTO (UX mejorada significativamente)

**Verificación:**
- Revisado `App.tsx` - Sidebar siempre visible
- No hay botón de toggle/cerrar
- Ocupa espacio fijo en todas las vistas

**Implementación requerida:**
```typescript
// App.tsx
const [sidebarOpen, setSidebarOpen] = useState(true);

// Añadir botón hamburguesa
// Sidebar con clase condicional: hidden/block
// Guardar estado en localStorage
```

**Archivos a modificar:**
- `App.tsx` (añadir estado y toggle)
- `components/Sidebar.tsx` (añadir botón cerrar)
- Estilos responsive

**Tiempo estimado:** 2 horas

---

### 2. Vista caso + preguntas en misma ventana
**Estado:** ❌ NO IMPLEMENTADO  
**Complejidad:** 🟡 MEDIA (4 horas)  
**Impacto:** 🔴 ALTO (Esencial para UX de casos prácticos)

**Verificación:**
```typescript
// CaseGeneratorView.tsx - Líneas revisadas
// Actualmente: Caso y preguntas en secciones separadas
// Usuario debe hacer scroll para ver caso mientras responde
```

**Problema actual:**
- Caso arriba, preguntas abajo
- No se puede ver caso mientras se responde
- Mala experiencia de usuario

**Implementación requerida:**
- Layout de 2 columnas (caso izquierda, preguntas derecha)
- O tabs con caso siempre visible en panel lateral
- Responsive: stack vertical en móvil

**Archivos a modificar:**
- `components/CaseGeneratorView.tsx`
- Estilos CSS/Tailwind

**Tiempo estimado:** 4 horas

---

### 3. Burbuja de chat contextual
**Estado:** ❌ NO IMPLEMENTADO  
**Complejidad:** 🟡 MEDIA (6 horas)  
**Impacto:** 🔴 ALTO (Ayuda contextual invaluable)

**Descripción:**
- Chat flotante en casos prácticos, tests, simulacros
- Contexto automático del caso/test actual
- Explica dudas sobre respuestas

**Verificación:**
- No existe componente de chat flotante
- Chat actual solo en vista dedicada
- No hay contexto compartido entre vistas

**Implementación requerida:**
```typescript
// Nuevo componente: ContextualChatBubble.tsx
// Props: context (caso/test actual), position
// Estado global para mantener conversación
// Integración con RAG + contexto específico
```

**Archivos a crear:**
- `components/ContextualChatBubble.tsx`
- `contexts/ChatContext.tsx` (estado global)
- Integrar en `CaseGeneratorView.tsx`, `MockExamView.tsx`

**Tiempo estimado:** 6 horas

---

### 4. Modo "Ten en cuenta mi progreso"
**Estado:** ⚠️ PARCIALMENTE IMPLEMENTADO  
**Complejidad:** 🟡 MEDIA (8 horas)  
**Impacto:** 🔴 ALTO (Personalización clave)

**Verificación:**
```typescript
// ProgressView.tsx - Existe tracking básico
// user_progress table en PostgreSQL - ✅ Existe
// answer_history table - ✅ Existe

// FALTA:
// - Toggle en UI para activar/desactivar
// - Lógica para ajustar dificultad según progreso
// - Integración con generación de casos/tests
```

**Estado actual:**
- ✅ Base de datos lista (user_progress, answer_history)
- ✅ Tracking de respuestas implementado
- ❌ No hay toggle en UI
- ❌ No se usa progreso para ajustar dificultad

**Implementación requerida:**
1. Toggle en Settings o en cada vista
2. Endpoint backend: `/ai/adaptive-difficulty`
3. Lógica de ajuste basada en historial
4. Integración en generación de contenido

**Archivos a modificar:**
- `components/SettingsView.tsx` (añadir toggle)
- `backend/routers/ai_functions.py` (lógica adaptativa)
- `components/CaseGeneratorView.tsx`, `MockExamView.tsx` (usar modo)

**Tiempo estimado:** 8 horas

---

## 🟠 PRIORIDAD ALTA (Implementar SEGUNDO)

### 5. Agentes sincronizados y orquestados
**Estado:** ⚠️ PARCIALMENTE IMPLEMENTADO  
**Complejidad:** 🔴 ALTA (16 horas)  
**Impacto:** 🟠 MEDIO-ALTO (Mejora calidad respuestas)

**Verificación:**
```python
# backend/agents/ - Múltiples agentes existen:
# - rag_agent.py ✅
# - rag_agent_v2.py ✅
# - llm_providers.py ✅

# FALTA:
# - Orquestador central
# - Comunicación entre agentes
# - Estado compartido
# - Sistema de decisión (qué agente usar cuándo)
```

**Estado actual:**
- ✅ Agentes individuales funcionando
- ❌ No hay orquestación
- ❌ No comparten contexto
- ❌ No hay sistema de decisión

**Implementación requerida:**
```python
# backend/agents/orchestrator.py
class AgentOrchestrator:
    def __init__(self):
        self.rag_agent = RAGAgent()
        self.qa_agent = QAAgent()
        self.context = SharedContext()
    
    def process_request(self, request):
        # Decidir qué agente(s) usar
        # Coordinar ejecución
        # Combinar resultados
        pass
```

**Archivos a crear:**
- `backend/agents/orchestrator.py`
- `backend/agents/shared_context.py`
- `backend/agents/qa_agent.py` (nuevo)

**Tiempo estimado:** 16 horas

---

### 6. Acceso completo a RAG + búsqueda web
**Estado:** ⚠️ PARCIALMENTE IMPLEMENTADO  
**Complejidad:** 🟡 MEDIA (10 horas)  
**Impacto:** 🟠 MEDIO-ALTO (Información más completa)

**Verificación:**
```python
# RAG:
# - rag_agent_v2.py ✅ Implementado
# - Qdrant Cloud ✅ Configurado
# - Acceso desde chat ✅ Funciona

# Búsqueda web:
# - Brave Search API ❌ NO implementado
# - Integración en agentes ❌ NO existe

# Compartir info entre páginas:
# - Estado global ❌ NO implementado
# - Context API limitado
```

**Estado actual:**
- ✅ RAG funcionando en chat
- ❌ RAG no disponible en todas las vistas
- ❌ Sin búsqueda web
- ❌ Sin estado compartido entre vistas

**Implementación requerida:**
1. Integrar Brave Search API
2. Crear contexto global para compartir info
3. Añadir RAG a todas las vistas de IA
4. Combinar RAG + Web en respuestas

**Archivos a modificar:**
- `backend/agents/web_search_agent.py` (crear)
- `contexts/GlobalContext.tsx` (crear)
- Todos los componentes de IA (integrar RAG)

**Tiempo estimado:** 10 horas

---

### 7. Medir tokens y precio en todos los modelos
**Estado:** ❌ NO IMPLEMENTADO  
**Complejidad:** 🟡 MEDIA (6 horas)  
**Impacto:** 🟠 MEDIO-ALTO (Transparencia y control)

**Verificación:**
```typescript
// Frontend: No hay contador de tokens visible
// Backend: No hay tracking de tokens por request

// NECESARIO:
// - Contador en UI (tokens usados, coste estimado)
// - Tracking en backend por provider
// - Almacenar en BD para estadísticas
```

**Estado actual:**
- ❌ No se muestran tokens usados
- ❌ No se calcula coste
- ❌ No hay estadísticas de uso

**Implementación requerida:**
```typescript
// Componente: TokenCounter.tsx
interface TokenUsage {
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  estimated_cost: number;
  provider: string;
}

// Mostrar en cada respuesta
// Acumulado por sesión
// Histórico en Settings
```

**Archivos a crear:**
- `components/TokenCounter.tsx`
- `backend/middleware/token_tracker.py`
- Tabla `token_usage` en PostgreSQL

**Tiempo estimado:** 6 horas

---

### 8. Considerar archivos subidos y enlaces
**Estado:** ⚠️ PARCIALMENTE IMPLEMENTADO  
**Complejidad:** 🟡 MEDIA (8 horas)  
**Impacto:** 🟠 MEDIO-ALTO (Contexto personalizado)

**Verificación:**
```python
# Upload:
# - backend/routers/upload.py ✅ Existe
# - Sube archivos ✅ Funciona
# - Indexa en RAG ✅ Funciona

# FALTA:
# - Persistir archivos subidos por usuario
# - Mostrar lista de archivos en UI
# - Usar en contexto de agentes
# - Enlaces: guardar y usar en contexto
```

**Estado actual:**
- ✅ Upload funciona
- ✅ Indexación en RAG
- ❌ No se persisten por usuario
- ❌ No hay lista de "Mis documentos"
- ❌ Enlaces no se guardan

**Implementación requerida:**
1. Tabla `user_documents` en PostgreSQL
2. Vista "Mis Documentos" en UI
3. Integrar documentos en contexto de agentes
4. Guardar enlaces y usarlos

**Archivos a modificar:**
- `backend/routers/upload.py` (persistir)
- `components/MyDocumentsView.tsx` (crear)
- Agentes (usar documentos de usuario)

**Tiempo estimado:** 8 horas

---

### 9. Añadir Mistral API key (BYOK)
**Estado:** ⚠️ PARCIALMENTE IMPLEMENTADO  
**Complejidad:** 🟢 BAJA (3 horas)  
**Impacto:** 🟠 MEDIO (Experiencia gratis)

**Verificación:**
```python
# backend/agents/llm_providers.py
# - Mistral VPS ✅ Implementado
# - Mistral API ❌ NO implementado

# NECESARIO:
# - Añadir Mistral API como provider
# - UI para que usuario añada su key
# - Guardar key encriptada
```

**Estado actual:**
- ✅ Mistral VPS funcionando
- ❌ Mistral API no disponible
- ❌ No hay UI para BYOK

**Implementación requerida:**
```python
# backend/agents/llm_providers.py
class MistralAPIProvider:
    def __init__(self, api_key):
        self.client = MistralClient(api_key)
    
    def generate(self, prompt):
        # Usar Mistral API
        pass

# UI: Settings → API Keys → Mistral
```

**Archivos a modificar:**
- `backend/agents/llm_providers.py`
- `components/SettingsView.tsx` (sección API Keys)
- `backend/routers/user.py` (guardar keys)

**Tiempo estimado:** 3 horas

---

## 🟡 PRIORIDAD MEDIA (Implementar TERCERO)

### 10. Google Colab para fine-tuning
**Estado:** ❌ NO IMPLEMENTADO  
**Complejidad:** 🔴 ALTA (20 horas)  
**Impacto:** 🟡 MEDIO (Mejora calidad, pero no esencial)

**Evaluación:**
- **Ventaja:** Modelos personalizados para oposiciones
- **Desventaja:** Complejidad alta, mantenimiento
- **Alternativa:** Usar modelos existentes con buenos prompts

**Recomendación:** ⏸️ POSPONER
- Primero optimizar prompts
- Luego evaluar si fine-tuning es necesario
- Requiere dataset de calidad (preguntas + respuestas)

**Si se implementa:**
1. Crear notebook en Colab
2. Preparar dataset de entrenamiento
3. Fine-tune modelo (ej: Mistral 7B)
4. Desplegar modelo fine-tuned
5. Integrar en backend

**Tiempo estimado:** 20 horas

---

### 11. Cloudflare Workers + Durable Objects (Prueba)
**Estado:** ❌ NO IMPLEMENTADO  
**Complejidad:** 🟡 MEDIA (12 horas)  
**Impacto:** 🟡 MEDIO (Exploración técnica)

**Evaluación:**
- Ya analizado en `EVALUACION_CLOUDFLARE_WORKERS_AI_DETALLADA.md`
- **Conclusión:** NO migrar ahora (ROI negativo)
- **Alternativa:** Cloudflare Tunnel (€0, 1 hora)

**Recomendación:** ⏸️ POSPONER
- Implementar Cloudflare Tunnel primero
- Evaluar Workers solo si:
  - >1000 usuarios/día
  - Latencia problemática
  - Necesidad de escalado global

**Si se implementa (prueba):**
1. Crear Worker básico
2. Crear Durable Object para estado
3. Probar latencia y coste
4. Comparar con arquitectura actual

**Tiempo estimado:** 12 horas

---

### 12. Sistema de agentes tipo BMAD
**Estado:** ❌ NO IMPLEMENTADO  
**Complejidad:** 🔴 MUY ALTA (40+ horas)  
**Impacto:** 🟡 MEDIO-ALTO (Calidad, pero complejo)

**Descripción BMAD:**
- Multi-agente con orquestación
- Agente QA obligatorio
- Agente YAML para crear agentes dinámicos
- Sistema de verificación y validación

**Evaluación:**
- **Ventaja:** Sistema robusto y escalable
- **Desventaja:** Complejidad muy alta
- **Alternativa:** Orquestador simple + QA manual

**Recomendación:** 📋 PLANIFICAR PARA FUTURO
- Primero implementar orquestador básico (#5)
- Luego añadir agente QA
- Finalmente sistema dinámico

**Fases:**
1. **Fase 1:** Orquestador básico (16h)
2. **Fase 2:** Agente QA (12h)
3. **Fase 3:** Sistema YAML dinámico (20h)
4. **Total:** 48 horas

---

## 📊 MEJORAS YA IMPLEMENTADAS

### ✅ 1. Deployment en Vercel
**Estado:** ⚠️ PARCIALMENTE LISTO  
**Verificación:**
- `vercel.json` ✅ Existe
- Frontend React ✅ Listo para deploy
- **Falta:** Configurar variables de entorno en Vercel

**Próximo paso:**
```bash
# Instalar Vercel CLI
npm install -g vercel

# Deploy
vercel

# Configurar env vars en dashboard
```

**Tiempo:** 1 hora

---

### ✅ 2. Llenar Qdrant con leyes y reglamentos
**Estado:** ⏳ EN PROGRESO  
**Verificación:**
- Script `indexar_todas_las_leyes.py` ✅ Creado
- Proceso de indexación ⏳ Corriendo (5/13 leyes)
- **Falta:** 
  - Completar indexación (1-2 horas)
  - Añadir jurisprudencia
  - Añadir ejemplos reales

**Próximos pasos:**
1. Esperar indexación completa
2. Verificar calidad de respuestas
3. Añadir jurisprudencia (crear script)
4. Añadir ejemplos de exámenes reales

**Tiempo restante:** 10-15 horas

---

### ✅ 3. Simular ataques con Snyk
**Estado:** ❌ NO IMPLEMENTADO  
**Complejidad:** 🟢 BAJA (2 horas)  
**Impacto:** 🟠 MEDIO (Seguridad)

**Implementación:**
```bash
# Instalar Snyk
npm install -g snyk

# Autenticar
snyk auth

# Escanear proyecto
snyk test

# Monitorear
snyk monitor

# Integrar en CI/CD
```

**Archivos a crear:**
- `.snyk` (configuración)
- GitHub Action para Snyk

**Tiempo estimado:** 2 horas

---

## 📋 PLAN DE IMPLEMENTACIÓN RECOMENDADO

### Sprint 1: UX Crítica (2 semanas - 20 horas)
1. ✅ Botón cerrar sidebar (2h)
2. ✅ Vista caso + preguntas (4h)
3. ✅ Burbuja chat contextual (6h)
4. ✅ Modo progreso adaptativo (8h)

**Resultado:** UX significativamente mejorada

---

### Sprint 2: Funcionalidad Core (2 semanas - 27 horas)
5. ✅ Medir tokens y precio (6h)
6. ✅ Archivos y enlaces en contexto (8h)
7. ✅ RAG + Web en todas las vistas (10h)
8. ✅ Mistral API BYOK (3h)

**Resultado:** Funcionalidad completa y transparente

---

### Sprint 3: Agentes y Orquestación (3 semanas - 34 horas)
9. ✅ Orquestador de agentes (16h)
10. ✅ Agente QA (12h)
11. ✅ Completar indexación Qdrant (6h)

**Resultado:** Sistema de agentes robusto

---

### Sprint 4: Seguridad y Deploy (1 semana - 8 horas)
12. ✅ Snyk security scan (2h)
13. ✅ Cloudflare Tunnel (1h)
14. ✅ Deploy Vercel (1h)
15. ✅ Documentación (4h)

**Resultado:** Producción segura y documentada

---

### Futuro (Evaluar después)
- ⏸️ Google Colab fine-tuning
- ⏸️ Cloudflare Workers (prueba)
- ⏸️ Sistema BMAD completo

---

## 📊 RESUMEN POR ESTADO

### ✅ Implementado (3)
1. Deployment Vercel (parcial)
2. Indexación Qdrant (en progreso)
3. Multi-provider LLM

### ⚠️ Parcial (4)
4. Modo progreso (BD lista, falta UI)
5. Agentes (existen, falta orquestación)
6. RAG (funciona, falta en todas las vistas)
7. Upload (funciona, falta persistencia)

### ❌ Pendiente (5)
8. Botón cerrar sidebar
9. Vista caso + preguntas
10. Burbuja chat contextual
11. Tokens y precio
12. Snyk security

### ⏸️ Posponer (3)
13. Fine-tuning Colab
14. Cloudflare Workers
15. Sistema BMAD completo

---

## 💰 ESTIMACIÓN TOTAL

**Críticas:** 20 horas  
**Altas:** 43 horas  
**Medias:** 72 horas (si se implementan)  

**Total MVP (Críticas + Altas):** 63 horas (~2 meses a 8h/semana)  
**Total Completo:** 135 horas (~4 meses a 8h/semana)

---

## ✅ RECOMENDACIÓN FINAL

**Enfoque:** Implementar en orden de prioridad  
**Objetivo:** MVP funcional en 2 meses  
**Estrategia:** Sprints de 2 semanas  

**Próximos pasos inmediatos:**
1. ✅ Completar indexación Qdrant (en progreso)
2. ✅ Implementar botón cerrar sidebar (2h)
3. ✅ Implementar vista caso + preguntas (4h)
4. ✅ Implementar burbuja chat (6h)

**Total primera semana:** 12 horas de desarrollo

---

**Documento creado:** 25 Noviembre 2025  
**Próxima revisión:** Después de Sprint 1
