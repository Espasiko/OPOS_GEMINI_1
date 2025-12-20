# 🚀 SPRINT 10 - Optimización y Refactoring

**Fecha Inicio**: 22 Noviembre 2025  
**Sprint**: 10 - Optimización y Refactoring  
**Estado**: 📋 **PLANIFICADO**

---

## 🎯 OBJETIVO PRINCIPAL

Optimizar el código del Sprint 9, eliminar duplicación, crear utilidades compartidas y mejorar la arquitectura del sistema multi-proveedor.

---

## 📊 CONTEXTO

### Estado Actual (Post-Sprint 9)

**Logros** ✅
- 7 componentes migrados a multi-proveedor
- 100% tests pasando
- 80% ahorro en costos

**Problemas Identificados** ⚠️
- Función `getProviderFromModelId()` duplicada en 7 componentes
- Lógica de conversión de formatos repetida
- No hay caché de respuestas
- No hay retry automático
- No hay tracking de uso/costos

---

## 🎯 OBJETIVOS DEL SPRINT

### Funcionales
1. ✅ Eliminar código duplicado
2. ✅ Crear utilidades compartidas
3. ✅ Mejorar manejo de errores
4. ✅ Agregar retry automático

### Técnicos
1. ✅ Crear hook personalizado `useAIProvider()`
2. ✅ Extraer helpers a `utils/`
3. ✅ Consolidar conversiones de formato
4. ✅ Mejorar tipos TypeScript

### Performance
1. ✅ Caché de respuestas frecuentes
2. ✅ Optimizar llamadas al backend
3. ✅ Reducir re-renders innecesarios

---

## 📋 PLAN DE EJECUCIÓN

### FASE 1: Crear Utilidades Compartidas (2h)

**Archivos a crear**:
- `utils/providers.ts` - Helper de providers
- `utils/formatters.ts` - Conversiones de formato
- `hooks/useAIProvider.ts` - Hook personalizado

#### 1.1 `utils/providers.ts`
```typescript
/**
 * Mapea el ID del modelo al provider correspondiente
 */
export function getProviderFromModelId(modelId: string): string {
  if (modelId.startsWith('groq-')) return 'groq';
  if (modelId.startsWith('deepseek-')) return 'deepseek';
  if (modelId.startsWith('gemini-')) return 'google';
  if (modelId.startsWith('hf-')) return 'huggingface';
  if (modelId.startsWith('cohere-')) return 'cohere';
  if (modelId.startsWith('mistral-')) return 'mistral-vps';
  return 'groq'; // Default
}

/**
 * Obtiene información del provider
 */
export function getProviderInfo(modelId: string) {
  const provider = getProviderFromModelId(modelId);
  const providerNames: Record<string, string> = {
    groq: 'Groq',
    deepseek: 'DeepSeek',
    google: 'Google Gemini',
    huggingface: 'Hugging Face',
    cohere: 'Cohere',
    'mistral-vps': 'Mistral VPS',
  };
  return {
    id: provider,
    name: providerNames[provider] || provider,
    modelId,
  };
}
```

#### 1.2 `utils/formatters.ts`
```typescript
import { MindMapNode } from '../types';

/**
 * Convierte nodo del backend (label) a formato frontend (text)
 */
export function convertMindMapNode(node: any, parentId = ''): MindMapNode {
  if (!node || !node.label) {
    throw new Error('Nodo inválido en la respuesta');
  }
  const id = parentId ? `${parentId}-${node.label}` : node.label;
  return {
    id,
    text: node.label,
    children: node.children
      ? node.children.map((child: any, idx: number) => 
          convertMindMapNode(child, `${id}-${idx}`)
        )
      : [],
  };
}

/**
 * Convierte schema del backend a markdown
 */
export function convertSchemaToMarkdown(response: any): string {
  let markdown = `# ${response.title}\n\n`;
  response.sections.forEach((section: any) => {
    markdown += `* ${section.title}\n`;
    section.content.forEach((item: string) => {
      markdown += `  * ${item}\n`;
    });
    if (section.subsections) {
      section.subsections.forEach((sub: any) => {
        markdown += `  * ${sub.title}\n`;
        sub.content.forEach((item: string) => {
          markdown += `    * ${item}\n`;
        });
      });
    }
  });
  return markdown;
}

/**
 * Convierte study plan del backend a texto
 */
export function convertStudyPlanToText(response: any): string {
  let planText = `# ${response.title}\n\n`;
  planText += `**Duración:** ${response.total_weeks} semanas\n`;
  planText += `**Horas totales:** ${response.total_hours} horas\n\n`;

  response.weeks.forEach((week: any) => {
    planText += `## Semana ${week.week}\n\n`;
    planText += `**Temas:**\n`;
    week.topics.forEach((topic: string) => {
      planText += `- ${topic}\n`;
    });
    planText += `\n**Actividades:**\n`;
    week.activities.forEach((activity: string) => {
      planText += `- ${activity}\n`;
    });
    planText += `\n**Objetivos:**\n`;
    week.goals.forEach((goal: string) => {
      planText += `- ${goal}\n`;
    });
    planText += `\n`;
  });

  return planText;
}

/**
 * Formatea resumen con puntos clave
 */
export function formatSummaryWithKeyPoints(response: any): string {
  let formattedSummary = response.summary;
  if (response.key_points && response.key_points.length > 0) {
    formattedSummary += '\n\n**Puntos Clave:**\n';
    response.key_points.forEach((point: string) => {
      formattedSummary += `• ${point}\n`;
    });
  }
  return formattedSummary;
}
```

#### 1.3 `hooks/useAIProvider.ts`
```typescript
import { useModel } from '../contexts/ModelContext';
import { getProviderFromModelId, getProviderInfo } from '../utils/providers';

/**
 * Hook personalizado para manejar providers de AI
 */
export function useAIProvider() {
  const { selectedModel } = useModel();
  
  const provider = getProviderFromModelId(selectedModel);
  const providerInfo = getProviderInfo(selectedModel);

  /**
   * Ejecuta una función AI con retry automático
   */
  async function executeWithRetry<T>(
    fn: (provider: string) => Promise<T>,
    maxRetries = 2
  ): Promise<T> {
    let lastError: Error | null = null;
    
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        return await fn(provider);
      } catch (error) {
        lastError = error instanceof Error ? error : new Error('Error desconocido');
        
        // Si no es el último intento, esperar antes de reintentar
        if (attempt < maxRetries) {
          await new Promise(resolve => setTimeout(resolve, 1000 * (attempt + 1)));
        }
      }
    }
    
    throw lastError;
  }

  /**
   * Maneja errores con mensaje específico del provider
   */
  function handleError(error: unknown): string {
    const errorMsg = error instanceof Error ? error.message : 'Error desconocido';
    return `Error con ${providerInfo.name}: ${errorMsg}`;
  }

  return {
    provider,
    providerInfo,
    selectedModel,
    executeWithRetry,
    handleError,
  };
}
```

---

### FASE 2: Refactorizar Componentes (3h)

**Componentes a actualizar**:
1. CaseGeneratorView
2. MindMapView
3. FlashcardsView
4. SchemaView
5. SummaryView
6. StudyPlanView

**Cambios en cada componente**:
```typescript
// ANTES
const { selectedModel } = useModel();
const getProviderFromModelId = (modelId: string): string => { ... };
const provider = getProviderFromModelId(selectedModel);

// DESPUÉS
import { useAIProvider } from '../hooks/useAIProvider';
const { provider, providerInfo, executeWithRetry, handleError } = useAIProvider();
```

---

### FASE 3: Mejorar Manejo de Errores (1h)

**Crear componente de error**:
```typescript
// components/ErrorMessage.tsx
interface ErrorMessageProps {
  error: string;
  onRetry?: () => void;
}

export function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  return (
    <div className="bg-red-50 border border-red-200 rounded p-4">
      <p className="text-red-700">{error}</p>
      {onRetry && (
        <button 
          onClick={onRetry}
          className="mt-2 text-sm text-red-600 underline"
        >
          Reintentar
        </button>
      )}
    </div>
  );
}
```

---

### FASE 4: Agregar Caché Simple (1h)

**Crear sistema de caché**:
```typescript
// utils/cache.ts
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutos

export function getCached<T>(key: string): T | null {
  const cached = cache.get(key);
  if (!cached) return null;
  
  if (Date.now() - cached.timestamp > CACHE_TTL) {
    cache.delete(key);
    return null;
  }
  
  return cached.data as T;
}

export function setCache(key: string, data: any): void {
  cache.set(key, { data, timestamp: Date.now() });
}

export function clearCache(): void {
  cache.clear();
}
```

---

### FASE 5: Tests y Documentación (1h)

**Tests a crear**:
- `utils/__tests__/providers.test.ts`
- `utils/__tests__/formatters.test.ts`
- `hooks/__tests__/useAIProvider.test.ts`

**Documentación**:
- Actualizar README con nuevas utilidades
- Documentar hook `useAIProvider`
- Guía de uso de caché

---

## 🔧 ARCHIVOS A CREAR/MODIFICAR

### Nuevos Archivos
```
utils/
├── providers.ts              ✅ Helper de providers
├── formatters.ts             ✅ Conversiones de formato
├── cache.ts                  ✅ Sistema de caché
└── __tests__/
    ├── providers.test.ts     ✅ Tests
    └── formatters.test.ts    ✅ Tests

hooks/
├── useAIProvider.ts          ✅ Hook personalizado
└── __tests__/
    └── useAIProvider.test.ts ✅ Tests

components/
└── ErrorMessage.tsx          ✅ Componente de error
```

### Archivos a Modificar (6 componentes)
```
components/
├── CaseGeneratorView.tsx     ✅ Usar hook
├── MindMapView.tsx           ✅ Usar hook + formatter
├── FlashcardsView.tsx        ✅ Usar hook
├── SchemaView.tsx            ✅ Usar hook + formatter
├── SummaryView.tsx           ✅ Usar hook + formatter
└── StudyPlanView.tsx         ✅ Usar hook + formatter
```

---

## 📊 MÉTRICAS DE ÉXITO

### Código
- ✅ Reducir duplicación en 80%
- ✅ Eliminar 200+ líneas de código duplicado
- ✅ Centralizar lógica en 3 archivos

### Performance
- ✅ Reducir llamadas al backend con caché
- ✅ Retry automático en fallos
- ✅ Mejor experiencia de usuario

### Mantenibilidad
- ✅ Código más limpio y organizado
- ✅ Fácil agregar nuevos providers
- ✅ Fácil agregar nuevos componentes

---

## 🎯 BENEFICIOS ESPERADOS

### Para Desarrolladores
1. **Menos código duplicado**: Cambios en un solo lugar
2. **Más fácil de mantener**: Lógica centralizada
3. **Más fácil de testear**: Funciones puras
4. **Mejor organización**: Estructura clara

### Para Usuarios
1. **Más rápido**: Caché de respuestas
2. **Más confiable**: Retry automático
3. **Mejor feedback**: Mensajes de error claros
4. **Experiencia consistente**: Mismo comportamiento en toda la app

---

## 📝 COMPARATIVA ANTES/DESPUÉS

### Antes (Sprint 9)
```typescript
// En cada componente (7 veces)
const { selectedModel } = useModel();

const getProviderFromModelId = (modelId: string): string => {
  if (modelId.startsWith('groq-')) return 'groq';
  // ... 20 líneas más
};

const provider = getProviderFromModelId(selectedModel);

try {
  const response = await generateXXX({ ...params, provider });
  // Conversión manual de formato
} catch (err) {
  const errorMsg = err instanceof Error ? err.message : 'Error desconocido';
  setError(`Error con modelo ${selectedModel}: ${errorMsg}`);
}
```

**Total**: ~150 líneas duplicadas × 7 componentes = **1,050 líneas**

### Después (Sprint 10)
```typescript
// En cada componente
import { useAIProvider } from '../hooks/useAIProvider';
import { convertXXXFormat } from '../utils/formatters';

const { provider, providerInfo, executeWithRetry, handleError } = useAIProvider();

try {
  const response = await executeWithRetry(async (p) => 
    generateXXX({ ...params, provider: p })
  );
  const formatted = convertXXXFormat(response);
} catch (err) {
  setError(handleError(err));
}
```

**Total**: ~20 líneas × 7 componentes = **140 líneas**

**Ahorro**: 910 líneas (87% menos código) 🎉

---

## ⏱️ TIMELINE ESTIMADO

**Total**: 8 horas

- **Fase 1**: Crear utilidades (2h)
- **Fase 2**: Refactorizar componentes (3h)
- **Fase 3**: Mejorar errores (1h)
- **Fase 4**: Agregar caché (1h)
- **Fase 5**: Tests y docs (1h)

---

## ✅ CRITERIOS DE COMPLETADO

### Funcionales
- [ ] Hook `useAIProvider` funcionando
- [ ] Utilidades compartidas creadas
- [ ] Todos los componentes refactorizados
- [ ] Caché implementado
- [ ] Retry automático funcionando

### Técnicos
- [ ] 0 errores TypeScript
- [ ] Tests pasando (100%)
- [ ] Código limpio y documentado
- [ ] Sin duplicación

### Performance
- [ ] Caché reduce llamadas al backend
- [ ] Retry mejora confiabilidad
- [ ] Sin regresiones de velocidad

---

## 🚀 PRÓXIMO SPRINT (Sprint 11)

Una vez completado Sprint 10:

### Sprint 11: Analytics y Monitoreo
1. Sistema de tracking de tokens
2. Dashboard de uso
3. Alertas de límites
4. Reportes de costos
5. Métricas de performance

---

**Documento creado**: 22 Noviembre 2025  
**Estado**: Planificado, listo para empezar  
**Autor**: Kiro AI Assistant

---

## ✅ CHECKLIST PRE-INICIO

Antes de empezar el sprint, verificar:

- [x] Sprint 9 completado al 100%
- [x] Todos los tests pasando
- [x] Git status clean
- [x] Documentación del Sprint 9 revisada

**¿Listo para empezar?** 🚀
