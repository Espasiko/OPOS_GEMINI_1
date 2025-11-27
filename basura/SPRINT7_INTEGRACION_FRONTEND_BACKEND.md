# 🚀 SPRINT 7: Integración Frontend-Backend con Mistral + RAG

**Fecha inicio**: 19 Noviembre 2025  
**Duración**: 7-8 días  
**Estado**: 📋 PLANIFICADO  
**Prioridad**: 🔴 CRÍTICA

---

## 📊 RESUMEN EJECUTIVO

### Objetivo
Conectar el frontend React con el backend FastAPI para usar Mistral + RAG en lugar de Gemini API directa.

### Problema Actual
- ❌ Frontend y Backend NO están conectados
- ❌ Frontend usa Gemini directamente (límites de API)
- ❌ Archivos se procesan en navegador
- ❌ RAG no se usa en el chat
- ❌ Mistral en VPS no se está usando

### Solución
Implementar arquitectura cliente-servidor completa con streaming, upload de archivos y consultas RAG.

---

## 🎯 OBJETIVOS DEL SPRINT

### Objetivos Principales
1. ✅ Crear endpoints de chat con streaming en backend
2. ✅ Crear endpoints de upload de archivos
3. ✅ Implementar servicios de backend en frontend
4. ✅ Migrar ChatView de Gemini a Mistral
5. ✅ Tests de integración completos

### Métricas de Éxito
- **Performance**: <3s latencia promedio
- **Calidad**: Scores RAG >0.65
- **Cobertura**: >80% tests
- **Disponibilidad**: >99% uptime

---

## 📋 BACKLOG DEL SPRINT

### 🔴 Prioridad ALTA (Días 1-4)

#### US-7.1: Como desarrollador, necesito endpoints de chat en el backend
**Puntos**: 5  
**Descripción**: Crear router `/chat` con endpoints de streaming y mensaje simple

**Tareas**:
- [ ] Crear `backend/routers/chat.py`
- [ ] Implementar `/chat/stream` con SSE
- [ ] Implementar `/chat/message` sin streaming
- [ ] Integrar con RAG Agent V2
- [ ] Integrar con Mistral VPS
- [ ] Tests unitarios

**Criterios de aceptación**:
- [ ] Endpoint `/chat/stream` devuelve SSE
- [ ] Consulta RAG antes de llamar a Mistral
- [ ] Incluye fuentes en la respuesta
- [ ] Tests pasan con >80% coverage

---

#### US-7.2: Como desarrollador, necesito endpoints de upload
**Puntos**: 3  
**Descripción**: Crear router `/upload` para procesar archivos y URLs en servidor

**Tareas**:
- [ ] Crear `backend/routers/upload.py`
- [ ] Implementar `/upload/file` para PDFs y TXT
- [ ] Implementar `/upload/url` para descargar contenido
- [ ] Extraer texto con pypdf
- [ ] Tests unitarios

**Criterios de aceptación**:
- [ ] Acepta PDF y TXT
- [ ] Extrae texto correctamente
- [ ] Devuelve document_id único
- [ ] Tests pasan

---

#### US-7.3: Como desarrollador, necesito servicio de backend en frontend
**Puntos**: 3  
**Descripción**: Crear `backendService.ts` para comunicación con API

**Tareas**:
- [ ] Crear `services/backendService.ts`
- [ ] Implementar `chatStream()` con SSE
- [ ] Implementar `uploadFile()`
- [ ] Implementar `uploadUrl()`
- [ ] Implementar `healthCheck()`
- [ ] Configurar VITE_BACKEND_URL

**Criterios de aceptación**:
- [ ] Maneja SSE correctamente
- [ ] Maneja errores de red
- [ ] TypeScript sin errores
- [ ] Documentado con JSDoc

---

#### US-7.4: Como desarrollador, necesito servicio de Mistral
**Puntos**: 2  
**Descripción**: Crear `mistralService.ts` como wrapper de backendService

**Tareas**:
- [ ] Crear `services/mistralService.ts`
- [ ] Implementar `sendMessageStream()`
- [ ] Implementar `processFile()`
- [ ] Implementar `processUrl()`
- [ ] Formatear fuentes en respuesta

**Criterios de aceptación**:
- [ ] API compatible con geminiService
- [ ] Agrega fuentes al final
- [ ] TypeScript sin errores

---

### 🟡 Prioridad MEDIA (Días 5-6)

#### US-7.5: Como usuario, quiero chatear usando Mistral
**Puntos**: 5  
**Descripción**: Migrar ChatView de Gemini a Mistral

**Tareas**:
- [ ] Modificar `components/ChatView.tsx`
- [ ] Reemplazar geminiService por mistralService
- [ ] Actualizar manejo de streaming
- [ ] Mostrar fuentes en UI
- [ ] Mantener Gemini como fallback

**Criterios de aceptación**:
- [ ] Chat funciona con Mistral
- [ ] Streaming se ve fluido
- [ ] Fuentes se muestran correctamente
- [ ] Fallback a Gemini si Mistral falla

---

#### US-7.6: Como usuario, quiero subir archivos al servidor
**Puntos**: 3  
**Descripción**: Modificar InputSourceSelector para usar backend

**Tareas**:
- [ ] Modificar `components/InputSourceSelector.tsx`
- [ ] Usar `mistralService.processFile()`
- [ ] Usar `mistralService.processUrl()`
- [ ] Mostrar progreso de upload
- [ ] Manejo de errores

**Criterios de aceptación**:
- [ ] Archivos se suben al servidor
- [ ] URLs se descargan en servidor
- [ ] Progreso visible
- [ ] Errores se muestran claramente

---

### 🟢 Prioridad BAJA (Días 7-8)

#### US-7.7: Como desarrollador, necesito tests de integración
**Puntos**: 5  
**Descripción**: Tests E2E completos

**Tareas**:
- [ ] Tests unitarios backend (`test_chat.py`, `test_upload.py`)
- [ ] Tests E2E frontend (`chat-integration.test.tsx`)
- [ ] Tests de performance
- [ ] Tests de fallback a Gemini
- [ ] Coverage report

**Criterios de aceptación**:
- [ ] >80% coverage backend
- [ ] >70% coverage frontend
- [ ] Todos los tests pasan
- [ ] CI/CD configurado

---

#### US-7.8: Como desarrollador, necesito documentación actualizada
**Puntos**: 2  
**Descripción**: Documentar nueva arquitectura

**Tareas**:
- [ ] Crear `docs/INTEGRACION_FRONTEND_BACKEND.md`
- [ ] Actualizar `README.md`
- [ ] Actualizar `ARCHITECTURE.md`
- [ ] Diagramas de arquitectura
- [ ] Guía de deployment

**Criterios de aceptación**:
- [ ] Documentación completa
- [ ] Diagramas actualizados
- [ ] Ejemplos de código
- [ ] Guía de troubleshooting

---

## 📅 CRONOGRAMA DETALLADO

### Día 1: Setup Backend Chat
- **Mañana**: Crear router chat.py
- **Tarde**: Implementar /chat/stream
- **Entregable**: Endpoint streaming funcional

### Día 2: Completar Backend
- **Mañana**: Implementar /chat/message
- **Tarde**: Crear router upload.py
- **Entregable**: Ambos routers con tests

### Día 3: Setup Frontend Services
- **Mañana**: Crear backendService.ts
- **Tarde**: Crear mistralService.ts
- **Entregable**: Servicios funcionando

### Día 4: Integrar ChatView
- **Mañana**: Modificar ChatView.tsx
- **Tarde**: Testing manual
- **Entregable**: Chat funcionando con Mistral

### Día 5: Upload de Archivos
- **Mañana**: Modificar InputSourceSelector
- **Tarde**: Testing de uploads
- **Entregable**: Upload funcionando

### Día 6: Testing Integración
- **Mañana**: Tests unitarios
- **Tarde**: Tests E2E
- **Entregable**: Suite de tests completa

### Día 7: Documentación
- **Mañana**: Escribir docs
- **Tarde**: Diagramas y ejemplos
- **Entregable**: Documentación completa

### Día 8: Deploy y Verificación
- **Mañana**: Deploy a staging
- **Tarde**: Verificación final
- **Entregable**: Sistema en producción

---

## 🔧 CONFIGURACIÓN NECESARIA

### Backend (.env)
```bash
# Mistral
MISTRAL_URL=http://147.93.95.67:8001
MISTRAL_MODEL=mistral-8b

# Qdrant
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=opositaia_leyes_seguridad_social

# CORS
CORS_ORIGINS=http://localhost:3000,https://opositaia.com
```

### Frontend (.env)
```bash
# Backend
VITE_BACKEND_URL=http://localhost:8000

# Gemini (fallback)
VITE_API_KEY=your-gemini-key
```

---

## 🧪 ESTRATEGIA DE TESTING

### Tests Unitarios Backend
```bash
# Ejecutar tests
pytest backend/tests/test_chat.py -v
pytest backend/tests/test_upload.py -v

# Coverage
pytest --cov=backend --cov-report=html
```

### Tests E2E Frontend
```bash
# Ejecutar tests
npm test

# Coverage
npm test -- --coverage
```

### Tests Manuales
1. Chat básico con Mistral
2. Chat con RAG activado
3. Upload de PDF
4. Upload de URL
5. Fallback a Gemini
6. Manejo de errores

---

## 🚨 RIESGOS Y MITIGACIONES

### Riesgo 1: Mistral VPS caído
**Probabilidad**: Media  
**Impacto**: Alto  
**Mitigación**: 
- Implementar fallback automático a Gemini
- Health check cada 30s
- Alertas por email

### Riesgo 2: CORS issues
**Probabilidad**: Alta  
**Impacto**: Medio  
**Mitigación**:
- Configurar CORS correctamente en FastAPI
- Testing exhaustivo en diferentes navegadores
- Documentar configuración

### Riesgo 3: Streaming no funciona
**Probabilidad**: Baja  
**Impacto**: Alto  
**Mitigación**:
- Implementar polling como fallback
- Testing en diferentes navegadores
- Documentar limitaciones

### Riesgo 4: RAG lento
**Probabilidad**: Media  
**Impacto**: Medio  
**Mitigación**:
- Caché de búsquedas frecuentes
- Optimizar queries
- Timeout de 5s

---

## 📊 MÉTRICAS Y KPIs

### Performance
- **Latencia promedio**: <3s
- **P95 latencia**: <5s
- **Throughput**: >10 req/s

### Calidad
- **RAG score promedio**: >0.65
- **Tasa de error**: <1%
- **Uptime**: >99%

### Testing
- **Coverage backend**: >80%
- **Coverage frontend**: >70%
- **Tests pasando**: 100%

---

## 🔗 DEPENDENCIAS

### Dependencias Externas
- ✅ Mistral en VPS (147.93.95.67:8001)
- ✅ Qdrant con 7,833 chunks
- ✅ Backend FastAPI operativo
- ⏸️ Frontend Vite corriendo

### Dependencias Internas
- ✅ RAG Agent V2 implementado
- ✅ Routers rag_v2.py funcionando
- ✅ Colección Qdrant poblada

---

## 📝 NOTAS IMPORTANTES

### Decisiones Técnicas
1. **SSE vs WebSockets**: Usar SSE por simplicidad
2. **Fallback**: Mantener Gemini como backup
3. **Caché**: Implementar en Sprint 8
4. **Rate Limiting**: Implementar en Sprint 8

### Mejoras Futuras (Sprint 8)
- [ ] WebSockets para mejor performance
- [ ] Caché de búsquedas RAG
- [ ] Rate limiting por usuario
- [ ] Métricas con Prometheus
- [ ] Logs estructurados

---

## ✅ DEFINITION OF DONE

### Código
- [ ] Todos los tests pasan
- [ ] Coverage >80% backend, >70% frontend
- [ ] Sin warnings de ESLint
- [ ] TypeScript sin errores
- [ ] Code review aprobado

### Funcionalidad
- [ ] Chat funciona con Mistral
- [ ] RAG se consulta correctamente
- [ ] Upload de archivos funciona
- [ ] Fallback a Gemini funciona
- [ ] UI responsive

### Documentación
- [ ] README actualizado
- [ ] Docs técnicos completos
- [ ] Diagramas actualizados
- [ ] Ejemplos de código
- [ ] Guía de troubleshooting

### Deploy
- [ ] Deploy a staging exitoso
- [ ] Tests en staging pasan
- [ ] Performance aceptable
- [ ] Rollback plan documentado

---

## 🎉 ENTREGABLES FINALES

1. ✅ Backend con routers `/chat` y `/upload`
2. ✅ Frontend con servicios `backendService` y `mistralService`
3. ✅ ChatView migrado a Mistral
4. ✅ Upload de archivos funcionando
5. ✅ Suite de tests completa (>80% coverage)
6. ✅ Documentación actualizada
7. ✅ Sistema desplegado en staging

---

**Creado**: 2025-11-19  
**Sprint**: 7  
**Estimación**: 7-8 días  
**Story Points**: 28  
**Prioridad**: CRÍTICA 🔴
