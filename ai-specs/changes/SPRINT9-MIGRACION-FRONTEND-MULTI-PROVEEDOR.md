# 🚀 SPRINT 9 - Migración Frontend Multi-Proveedor

**Fecha Inicio**: 21 Noviembre 2025  
**Sprint**: 9 - Migración Componentes Frontend  
**Estado**: 📋 **PLANIFICADO**

---

## 🎯 OBJETIVO PRINCIPAL

Migrar todos los componentes frontend para usar el sistema multi-proveedor del backend, eliminando dependencias directas de Gemini y permitiendo selección de modelo en toda la aplicación.

---

## 📊 CONTEXTO

### Estado Actual (Post-Sprint 8)

**Backend** ✅
- 7 proveedores LLM configurados (OpenAI, Anthropic, Google, Mistral, Groq, Cohere, OpenRouter)
- 7 endpoints `/ai/*` funcionando
- Sistema multi-proveedor completo
- Tests pasando

**Frontend** ⚠️
- ✅ ChatView migrado (usa backend)
- ✅ ModelSelector global disponible
- ❌ CaseGeneratorView usa Gemini directo
- ❌ MindMapView usa Gemini directo
- ❌ FlashcardsView usa Gemini directo
- ❌ SchemaView usa Gemini directo
- ❌ SummaryView usa Gemini directo
- ❌ CompareView usa Gemini directo
- ❌ StudyPlanView usa Gemini directo

### Problema a Resolver

Los componentes frontend llaman directamente a `geminiService`, ignorando el selector de modelo global. Necesitamos migrarlos para usar `backendService` y respetar la selección del usuario.

---

## 🎯 OBJETIVOS DEL SPRINT

### Funcionales
1. ✅ Todos los componentes usan el selector de modelo
2. ✅ Eliminada dependencia directa de Gemini
3. ✅ Experiencia de usuario consistente
4. ✅ Fallback automático si falla un proveedor

### Técnicos
1. ✅ Actualizar `backendService.ts` con funciones faltantes
2. ✅ Migrar 7 componentes a backend
3. ✅ Mantener compatibilidad con datos existentes
4. ✅ Tests E2E funcionando

### UX
1. ✅ Indicador visual del modelo seleccionado
2. ✅ Mensajes de error claros por proveedor
3. ✅ Loading states consistentes
4. ✅ Transición suave (sin breaking changes)

---

## 📋 PLAN DE EJECUCIÓN

### FASE 1: Actualizar Backend Service (Día 1 - 2h)

**Archivo**: `services/backendService.ts`

**Tareas**:
- [ ] Agregar función `generatePracticalCase()`
- [ ] Agregar función `generateMindMap()`
- [ ] Agregar función `generateFlashcards()`
- [ ] Agregar función `generateSchema()`
- [ ] Agregar función `generateSummary()`
- [ ] Agregar función `compareTexts()`
- [ ] Agregar función `generateStudyPlan()`
- [ ] Agregar tipos TypeScript para todas las respuestas
- [ ] Tests unitarios para nuevas funciones

**Criterios de Aceptación**:
- Todas las funciones tipadas correctamente
- Error handling robusto
- Tests unitarios pasando
- Documentación JSDoc completa

---

### FASE 2: Migrar CaseGeneratorView (Día 1-2 - 3h)

**Archivo**: `components/CaseGeneratorView.tsx`

**Cambios**:
```typescript
// ANTES
import { generatePracticalCase } from '../services/geminiService';

// DESPUÉS
import { generatePracticalCase } from '../services/backendService';
import { useModel } from '../contexts/ModelContext';

// Usar provider del contexto
const { selectedModel } = useModel();
const result = await generatePracticalCase({
  topic,
  difficulty,
  provider: selectedModel.provider
});
```

**Tareas**:
- [ ] Importar `useModel` hook
- [ ] Reemplazar llamadas a `geminiService`
- [ ] Pasar `provider` en todas las llamadas
- [ ] Actualizar manejo de errores
- [ ] Mostrar modelo seleccionado en UI
- [ ] Agregar fallback si falla
- [ ] Test manual completo

**Criterios de Aceptación**:
- Genera casos con cualquier proveedor
- Muestra modelo usado en la UI
- Error handling específico por proveedor
- No hay regresiones en funcionalidad

---

### FASE 3: Migrar MindMapView (Día 2 - 2h)

**Archivo**: `components/MindMapView.tsx`

**Cambios similares a CaseGeneratorView**:
- [ ] Importar `useModel` hook
- [ ] Reemplazar `geminiService` por `backendService`
- [ ] Pasar `provider` en llamadas
- [ ] Actualizar UI con indicador de modelo
- [ ] Test manual completo

---

### FASE 4: Migrar FlashcardsView (Día 2-3 - 2h)

**Archivo**: `components/FlashcardsView.tsx`

**Tareas**:
- [ ] Migrar a `backendService`
- [ ] Usar `provider` del contexto
- [ ] Actualizar UI
- [ ] Tests manuales

---

### FASE 5: Migrar SchemaView (Día 3 - 2h)

**Archivo**: `components/SchemaView.tsx`

**Tareas**:
- [ ] Migrar a `backendService`
- [ ] Usar `provider` del contexto
- [ ] Actualizar UI
- [ ] Tests manuales

---

### FASE 6: Migrar SummaryView (Día 3 - 2h)

**Archivo**: `components/SummaryView.tsx`

**Tareas**:
- [ ] Migrar a `backendService`
- [ ] Usar `provider` del contexto
- [ ] Actualizar UI
- [ ] Tests manuales

---

### FASE 7: Migrar CompareView (Día 4 - 2h)

**Archivo**: `components/CompareView.tsx`

**Tareas**:
- [ ] Migrar a `backendService`
- [ ] Usar `provider` del contexto
- [ ] Actualizar UI
- [ ] Tests manuales

---

### FASE 8: Migrar StudyPlanView (Día 4 - 2h)

**Archivo**: `components/StudyPlanView.tsx`

**Tareas**:
- [ ] Migrar a `backendService`
- [ ] Usar `provider` del contexto
- [ ] Actualizar UI
- [ ] Tests manuales

---

### FASE 9: Testing E2E y Limpieza (Día 5 - 4h)

**Tareas**:
- [ ] Test E2E de cada componente con 3 proveedores diferentes
- [ ] Verificar fallbacks funcionan
- [ ] Verificar error handling
- [ ] Limpiar código no usado de `geminiService`
- [ ] Actualizar documentación
- [ ] Crear documento de completado

**Tests E2E**:
```bash
# Para cada componente:
1. Seleccionar Groq → Generar contenido → ✅
2. Seleccionar OpenAI → Generar contenido → ✅
3. Seleccionar Gemini → Generar contenido → ✅
4. Simular error → Verificar fallback → ✅
```

---

## 🔧 ARCHIVOS A MODIFICAR

### Servicios
- `services/backendService.ts` - Agregar 7 funciones nuevas
- `services/__tests__/backendService.test.ts` - Tests para nuevas funciones

### Componentes (7 migraciones)
1. `components/CaseGeneratorView.tsx`
2. `components/MindMapView.tsx`
3. `components/FlashcardsView.tsx`
4. `components/SchemaView.tsx`
5. `components/SummaryView.tsx`
6. `components/CompareView.tsx`
7. `components/StudyPlanView.tsx`

### Documentación
- `SPRINT9_COMPLETADO.md` - Documento final

---

## 📐 PATRONES DE MIGRACIÓN

### Patrón Estándar para Todos los Componentes

```typescript
// 1. Importar hook de modelo
import { useModel } from '../contexts/ModelContext';

// 2. Importar función de backendService
import { generateXXX } from '../services/backendService';

// 3. Dentro del componente
const { selectedModel } = useModel();

// 4. En la función de generación
const handleGenerate = async () => {
  setLoading(true);
  setError(null);
  
  try {
    const result = await generateXXX({
      ...params,
      provider: selectedModel.provider  // ← CLAVE
    });
    
    // Procesar resultado
    setResult(result);
    
  } catch (err) {
    // Error handling específico
    const errorMsg = err instanceof Error 
      ? err.message 
      : 'Error desconocido';
    
    setError(`Error con ${selectedModel.name}: ${errorMsg}`);
    
    // Opcional: Intentar fallback
    if (selectedModel.provider !== 'google') {
      console.log('Intentando fallback a Gemini...');
      // Retry con Gemini
    }
    
  } finally {
    setLoading(false);
  }
};

// 5. Mostrar modelo en UI
<div className="model-indicator">
  Usando: {selectedModel.name}
</div>
```

---

## 🎨 MEJORAS DE UX

### Indicador de Modelo

Agregar en cada vista:

```tsx
<div className="flex items-center gap-2 text-sm text-gray-600 mb-4">
  <span className="font-medium">Modelo:</span>
  <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">
    {selectedModel.name}
  </span>
</div>
```

### Loading State Mejorado

```tsx
{loading && (
  <div className="flex items-center gap-2">
    <Loader2 className="animate-spin" />
    <span>Generando con {selectedModel.name}...</span>
  </div>
)}
```

### Error Handling Mejorado

```tsx
{error && (
  <div className="bg-red-50 border border-red-200 rounded p-4">
    <p className="text-red-700">{error}</p>
    <button 
      onClick={() => handleRetry()}
      className="mt-2 text-sm text-red-600 underline"
    >
      Reintentar con otro modelo
    </button>
  </div>
)}
```

---

## 🧪 ESTRATEGIA DE TESTING

### Tests Unitarios (Jest)

```typescript
// services/__tests__/backendService.test.ts
describe('AI Functions', () => {
  it('should generate practical case', async () => {
    const result = await generatePracticalCase({
      topic: 'IT',
      difficulty: 'medium',
      provider: 'groq'
    });
    
    expect(result.scenario).toBeDefined();
    expect(result.questions).toHaveLength(4);
  });
  
  // ... más tests
});
```

### Tests Manuales (Checklist)

Para cada componente:
- [ ] Funciona con Groq (gratis)
- [ ] Funciona con OpenAI
- [ ] Funciona con Gemini
- [ ] Muestra modelo seleccionado
- [ ] Error handling funciona
- [ ] Loading state correcto
- [ ] Resultado se muestra correctamente

---

## 📊 MÉTRICAS DE ÉXITO

### Cobertura
- ✅ 7/7 componentes migrados
- ✅ 7/7 funciones en backendService
- ✅ 100% tests unitarios pasando
- ✅ 100% tests manuales pasando

### Performance
- ✅ Tiempo de respuesta similar o mejor
- ✅ No hay regresiones de UX
- ✅ Fallbacks funcionan en <2s

### Calidad
- ✅ 0 errores TypeScript
- ✅ 0 warnings ESLint
- ✅ Código limpio y documentado

---

## ⚠️ RIESGOS Y MITIGACIONES

### Riesgo 1: Breaking Changes en Componentes
**Mitigación**: Migrar uno a la vez, testear antes de continuar

### Riesgo 2: Diferencias en Formato de Respuesta
**Mitigación**: Backend ya parsea JSON, formato consistente

### Riesgo 3: Proveedores Caídos
**Mitigación**: Sistema de fallback implementado

### Riesgo 4: Límites de API
**Mitigación**: Groq como default (gratis), monitoreo de uso

---

## 💰 IMPACTO EN COSTOS

### Antes (Sprint 8)
- 100% Gemini
- ~€0.10/mes por usuario

### Después (Sprint 9)
- 80% Groq (gratis)
- 20% Gemini (fallback)
- ~€0.02/mes por usuario
- **Ahorro: 80%**

---

## 📝 DOCUMENTACIÓN A ACTUALIZAR

- [ ] README.md - Sección de modelos disponibles
- [ ] ARCHITECTURE.md - Diagrama de flujo actualizado
- [ ] API.md - Endpoints `/ai/*` documentados
- [ ] USER_GUIDE.md - Cómo cambiar de modelo

---

## 🎉 CRITERIOS DE COMPLETADO

### Funcionales
- [ ] Todos los componentes usan selector de modelo
- [ ] No hay llamadas directas a `geminiService`
- [ ] Fallbacks funcionan correctamente
- [ ] Error handling robusto

### Técnicos
- [ ] 0 errores TypeScript
- [ ] 0 warnings ESLint
- [ ] Tests unitarios al 100%
- [ ] Tests manuales completados

### Documentación
- [ ] SPRINT9_COMPLETADO.md creado
- [ ] README actualizado
- [ ] Código comentado
- [ ] Commits descriptivos

---

## 📅 TIMELINE ESTIMADO

**Total**: 5 días (~30 horas)

- **Día 1**: Fase 1-2 (Backend Service + CaseGenerator)
- **Día 2**: Fase 3-4 (MindMap + Flashcards)
- **Día 3**: Fase 5-6 (Schema + Summary)
- **Día 4**: Fase 7-8 (Compare + StudyPlan)
- **Día 5**: Fase 9 (Testing E2E + Documentación)

---

## 🚀 PRÓXIMO SPRINT (Sprint 10)

Una vez completado Sprint 9:

### Sprint 10: Analytics y Monitoreo
1. Sistema de tracking de tokens por proveedor
2. Dashboard de uso en tiempo real
3. Alertas de límites de API
4. Reportes de costos
5. Optimización de routing (ML-based)

---

**Documento creado**: 21 Noviembre 2025  
**Estado**: Planificado, esperando aprobación  
**Autor**: Kiro AI Assistant

---

## ✅ CHECKLIST PRE-INICIO

Antes de empezar el sprint, verificar:

- [ ] Backend corriendo (`uvicorn main:app --reload`)
- [ ] Frontend corriendo (`npm run dev`)
- [ ] Git status clean
- [ ] Branch `sprint-9` creada
- [ ] Todos los tests del Sprint 8 pasando
- [ ] Variables de entorno configuradas
- [ ] Documentación del Sprint 8 revisada

**¿Listo para empezar?** 🚀
