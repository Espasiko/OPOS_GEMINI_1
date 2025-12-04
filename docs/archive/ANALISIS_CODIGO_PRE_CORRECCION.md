# Análisis de Código Pre-Corrección
## Fecha: 30 Noviembre 2025

---

## 1. ESTADO DE geminiService.ts

### ✅ CONCLUSIÓN: **NO SE USA, PUEDE ELIMINARSE**

**Evidencia**:
- ❌ **0 imports** en componentes actuales
- ✅ Todos los componentes usan `backendService`
- ✅ Todos los componentes usan `useModel()` hook
- ✅ Sistema multi-proveedor funcionando

**Componentes verificados**:
- MockExamView.tsx: ✅ Usa `backendService` + `useModel()`
- CaseGeneratorView.tsx: ✅ Usa `backendService` + `useModel()`
- MindMapView.tsx: ✅ Usa `backendService` + `useAIProvider()`
- FlashcardsView.tsx: ✅ Usa `backendService` + `useAIProvider()`

**Recomendación**: 
- Mover a carpeta `basura/` (no eliminar por si acaso)
- Mantener como referencia histórica

---

## 2. USO DEL SELECTOR DE MODELO

### ✅ MockExamView.tsx - CORRECTO

```typescript
const { selectedModel } = useModel();

// Línea 73: Usa selectedModel correctamente
provider: selectedModel || 'deepseek'
```

**Estado**: ✅ **FUNCIONA CORRECTAMENTE**

---

### ⚠️ CaseGeneratorView.tsx - NECESITA MEJORA

```typescript
const { selectedModel } = useModel();

// Línea 133: Mapea modelo a provider
const getProviderFromModelId = (modelId: string): string => {
  if (modelId.startsWith('groq-')) return 'groq';
  if (modelId.startsWith('deepseek-')) return 'deepseek';
  // ...
  return 'groq'; // Default
}

// Línea 148: Usa el provider mapeado
const provider = getProviderFromModelId(selectedModel);
```

**Problema**: 
- ❌ Mapeo manual de modelo a provider
- ❌ Puede no coincidir con backend

**Solución**: 
- Pasar `selectedModel` directamente (como MockExamView)
- Backend ya maneja el routing

---

### ✅ MindMapView.tsx - CORRECTO

```typescript
const { provider, providerInfo, executeWithRetry } = useAIProvider();

// Línea 52: Usa provider del hook
generateMindMap({ topic, depth: 3, provider: p })
```

**Estado**: ✅ **FUNCIONA CORRECTAMENTE**

---

### ✅ FlashcardsView.tsx - CORRECTO

```typescript
const { provider, providerInfo, executeWithRetry } = useAIProvider();

// Línea 48: Usa provider del hook
generateFlashcards({ topic, count: 10, provider: p })
```

**Estado**: ✅ **FUNCIONA CORRECTAMENTE**

---

## 3. MODELOS DE HUGGING FACE

### Estado Actual:
```python
# llm_providers.py - COMENTADO
# 'hf-llama-70b': HuggingFaceProvider('meta-llama/Llama-3.1-70B-Instruct'),
# 'hf-mixtral': HuggingFaceProvider('mistralai/Mixtral-8x7B-Instruct-v0.1'),
# 'hf-qwen': HuggingFaceProvider('Qwen/Qwen2.5-72B-Instruct'),
```

### Modelos GRATIS Recomendados:

#### 1. **meta-llama/Llama-3.2-3B-Instruct** ⭐
- Tamaño: 3B parámetros
- Calidad: Buena para tareas simples
- Límite: ~1000 requests/día
- **Uso**: Flashcards, resúmenes cortos

#### 2. **mistralai/Mistral-7B-Instruct-v0.3** ⭐⭐
- Tamaño: 7B parámetros
- Calidad: Excelente español
- Límite: ~1000 requests/día
- **Uso**: Casos prácticos, simulacros

#### 3. **google/gemma-2-2b-it**
- Tamaño: 2B parámetros
- Calidad: Buena
- Límite: ~1000 requests/día
- **Uso**: Tareas simples

#### 4. **Qwen/Qwen2.5-7B-Instruct** ⭐⭐
- Tamaño: 7B parámetros
- Calidad: Excelente multilingüe
- Límite: ~1000 requests/día
- **Uso**: General, muy bueno

### Configuración Necesaria:

```python
# llm_providers.py
PROVIDERS = {
    # Hugging Face (GRATIS pero con límites)
    'hf-llama-3b': HuggingFaceProvider('meta-llama/Llama-3.2-3B-Instruct'),
    'hf-mistral-7b': HuggingFaceProvider('mistralai/Mistral-7B-Instruct-v0.3'),
    'hf-gemma-2b': HuggingFaceProvider('google/gemma-2-2b-it'),
    'hf-qwen-7b': HuggingFaceProvider('Qwen/Qwen2.5-7B-Instruct'),
}
```

**Limitaciones**:
- ⚠️ Rate limits estrictos (1000 req/día)
- ⚠️ NO para producción
- ✅ Perfecto para testing/desarrollo

---

## 4. ERRORES A CORREGIR

### MockExamView.tsx:

#### Error 1: Líneas vacías múltiples (Línea 7-8)
```typescript
// ❌ INCORRECTO
import { useModel } from '../contexts/ModelContext';


const syllabusTopics = [

// ✅ CORRECTO
import { useModel } from '../contexts/ModelContext';

const syllabusTopics = [
```

#### Error 2: If sin llaves (Línea 107)
```typescript
// ❌ INCORRECTO
if (selectedTopics.length === 0) return;

// ✅ CORRECTO
if (selectedTopics.length === 0) {
  return;
}
```

#### Error 3: Función con argumento incorrecto (Línea 118)
```typescript
// ❌ INCORRECTO
addProgressData(progress);  // addProgressData espera 0 argumentos

// ✅ CORRECTO
// Verificar firma de addProgressData en App.tsx
// Si es addProgressData: () => void, entonces:
progress.forEach(p => addProgressData());
// O cambiar firma a: addProgressData: (data: ProgressData | ProgressData[]) => void
```

#### Error 4: Indentación (Líneas 130-133)
```typescript
// Usar 2 espacios consistentemente
// ESLint espera 2 espacios, hay 8-10 en algunos lugares
```

#### Warning: useEffect dependency (Línea 45)
```typescript
// ⚠️ ADVERTENCIA
useEffect(() => {
  if (stage === 'in_progress' && timeLeft === 0) {
    handleFinishExam();
  }
}, [stage, timeLeft]);  // Falta handleFinishExam

// ✅ CORRECTO
useEffect(() => {
  if (stage === 'in_progress' && timeLeft === 0) {
    handleFinishExam();
  }
}, [stage, timeLeft, handleFinishExam]);
```

---

### geminiService.ts:

#### Error 1: AbortController no definido (Línea 49)
```typescript
// ❌ PROBLEMA
const controller = new AbortController();
// ESLint no reconoce AbortController (es global en Node 18+)

// ✅ SOLUCIÓN 1: Actualizar .eslintrc.json
{
  "env": {
    "es2021": true,
    "node": true,
    "browser": true  // AbortController está en browser
  }
}

// ✅ SOLUCIÓN 2: Tipo explícito
const controller: AbortController = new AbortController();
```

#### Error 2: Property 'cards' no existe (Línea 212)
```typescript
// ❌ INCORRECTO
const result: unknown = await response.json();
const cards = result.cards;  // Error: Property 'cards' does not exist

// ✅ CORRECTO
interface FlashcardsResponse {
  cards: Array<{
    front: string;
    back: string;
  }>;
}
const result = await response.json() as FlashcardsResponse;
const cards = result.cards;
```

#### Warnings: Variables no usadas
```typescript
// ⚠️ ADVERTENCIA
catch (error) {  // 'error' is defined but never used

// ✅ CORRECTO
catch (_error) {  // Prefixar con _ si no se usa
// O eliminar si no se necesita
catch {
```

---

## 5. PLAN DE CORRECCIÓN

### Paso 1: Mover geminiService.ts
```bash
mkdir -p basura/deprecated_services
mv services/geminiService.ts basura/deprecated_services/
mv services/__tests__/geminiService.test.ts basura/deprecated_services/
```

### Paso 2: Corregir MockExamView.tsx
- [ ] Eliminar líneas vacías múltiples
- [ ] Añadir llaves a if
- [ ] Corregir llamada a addProgressData
- [ ] Corregir indentación
- [ ] Añadir handleFinishExam a dependencies

### Paso 3: Mejorar CaseGeneratorView.tsx
- [ ] Eliminar función getProviderFromModelId
- [ ] Pasar selectedModel directamente
- [ ] Simplificar código

### Paso 4: Añadir modelos Hugging Face
- [ ] Descomentar HuggingFaceProvider
- [ ] Actualizar URLs a nueva API
- [ ] Añadir 4 modelos recomendados
- [ ] Actualizar ModelSelector.tsx

### Paso 5: Corregir geminiService.ts (si se decide mantener)
- [ ] Actualizar .eslintrc.json
- [ ] Añadir tipos para responses
- [ ] Eliminar variables no usadas

---

## 6. VERIFICACIÓN FINAL

### Checklist:
- [ ] geminiService.ts movido a basura/
- [ ] MockExamView.tsx sin errores ESLint
- [ ] CaseGeneratorView.tsx simplificado
- [ ] Hugging Face modelos añadidos
- [ ] Todos los componentes usan selectedModel correctamente
- [ ] npm run lint pasa sin errores
- [ ] npm run build pasa sin errores
- [ ] Testing manual de cada proveedor

---

## RESUMEN

### Lo que está BIEN:
1. ✅ Sistema multi-proveedor funcionando
2. ✅ Todos los componentes usan hooks correctos
3. ✅ Backend maneja routing de proveedores

### Lo que hay que CORREGIR:
1. ❌ Errores ESLint en MockExamView.tsx (5 errores)
2. ❌ Errores TypeScript en geminiService.ts (2 errores)
3. ⚠️ CaseGeneratorView.tsx puede simplificarse

### Lo que hay que AÑADIR:
1. ➕ 4 modelos de Hugging Face
2. ➕ Actualizar ModelSelector con nuevos modelos

### Tiempo Estimado:
- Correcciones: 30 minutos
- Hugging Face: 30 minutos
- Testing: 30 minutos
- **Total**: 1.5 horas

**¿Procedo con las correcciones?**
