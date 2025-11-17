# AI Specs Quick Start - OpositaIA

## ✅ Setup Complete!

La estructura AI Specs ha sido instalada y configurada para OpositaIA. Ahora puedes desarrollar features de forma estructurada y eficiente.

## 📁 Qué se ha instalado

```
/
├── ai-specs/                    # Sistema AI Specs
│   ├── specs/                   # Estándares de desarrollo
│   │   ├── base-standards.mdc   # Principios core
│   │   ├── opositaia-standards.mdc  # Estándares específicos OpositaIA
│   │   ├── frontend-standards.mdc   # React/TypeScript
│   │   └── documentation-standards.mdc
│   ├── changes/                 # Planes de implementación
│   │   └── EXAMPLE-audio-quiz.md    # Ejemplo completo
│   ├── .commands/               # Comandos AI
│   │   ├── plan-feature.md      # Planificar feature
│   │   └── implement-feature.md # Implementar feature
│   └── README.md
├── AGENTS.md                    # Config para todos los copilots
├── GEMINI.md                    # Config específica Gemini (activa)
├── CLAUDE.md                    # Config para Claude/Cursor
└── codex.md                     # Config para GitHub Copilot
```

## 🚀 Cómo usar (Workflow básico)

### Opción 1: Workflow Completo (Recomendado)

#### Paso 1: Planificar Feature

```
Kiro, planifica una nueva feature: [descripción de la feature]
```

Ejemplo:

```
Kiro, planifica una nueva feature: Generador de cronogramas de estudio personalizados que use gemini-2.5-pro para crear planes semanales basados en el tiempo disponible del usuario
```

**Resultado**: Se crea `ai-specs/changes/study-timeline.md` con plan detallado

#### Paso 2: Revisar Plan

- Lee el plan generado
- Verifica que tenga sentido
- Ajusta si es necesario

#### Paso 3: Implementar

```
Kiro, implementa la feature siguiendo el plan @study-timeline.md
```

**Resultado**: Kiro implementa paso a paso:

1. Crea branch `feature/study-timeline`
2. Define tipos en `types.ts`
3. Implementa función en `geminiService.ts`
4. Crea componente `StudyTimeline.tsx`
5. Actualiza `App.tsx`
6. Actualiza documentación en `/docs`
7. Hace commits

### Opción 2: Desarrollo Directo (Más rápido)

Si la feature es simple, puedes ir directo:

```
Kiro, crea una feature de [descripción]. Sigue los estándares de OpositaIA.
```

Kiro seguirá automáticamente los estándares en `ai-specs/specs/opositaia-standards.mdc`

## 📚 Comandos Útiles

### Planificación

```
@plan-feature.md [descripción de la feature]
```

### Implementación

```
@implement-feature.md @[nombre-del-plan].md
```

### Consultar Estándares

```
Kiro, muéstrame los estándares de OpositaIA
```

### Actualizar Documentación

```
Kiro, actualiza /docs/AI_AGENTS.md con la nueva función generateX()
```

## 🎯 Ejemplo Práctico Completo

Vamos a crear una feature de "Quiz de Vocabulario Legal":

### 1. Planificar

```
Kiro, planifica una nueva feature: Quiz de vocabulario legal que genere preguntas sobre términos legales de la Seguridad Social. Debe usar gemini-2.5-flash para respuestas rápidas y permitir al usuario seleccionar categorías (prestaciones, afiliación, cotización, etc.)
```

### 2. Revisar el Plan

Kiro crea `ai-specs/changes/legal-vocabulary-quiz.md` con:

- Definición del agente AI
- Selección del modelo (gemini-2.5-flash)
- Estructura de tipos
- Pasos de implementación
- Checklist de testing
- Actualización de documentación

### 3. Implementar

```
Kiro, implementa @legal-vocabulary-quiz.md
```

Kiro ejecuta:

```
✅ Step 0: Create feature branch
- Created branch: feature/legal-vocabulary-quiz

✅ Step 1: Define Types
- Added LegalVocabQuestion interface to types.ts
- Added LegalVocabCategory enum
- Updated AppView enum

✅ Step 2: Implement Service Function
- Added generateLegalVocabQuiz() to geminiService.ts
- Configured gemini-2.5-flash model
- Implemented JSON schema for questions

✅ Step 3: Create Component
- Created components/LegalVocabularyQuiz.tsx
- Implemented state management
- Built UI with Bootstrap
- Added error handling

✅ Step 4: Update App.tsx
- Imported LegalVocabularyQuiz component
- Added routing case
- Added navigation button

✅ Step 5: Update Documentation
- Updated /docs/AI_AGENTS.md
- Updated /docs/DATA_MODEL.md
- Updated README.md

✅ Testing Complete
- Manual testing passed
- No console errors
- Responsive design verified

✅ Committed: [LegalVocab] Add: Legal vocabulary quiz generator
```

### 4. Probar

```bash
# Inicia servidor local
live-server
# o
python -m http.server
```

Prueba la feature en el navegador

### 5. Refinar (si es necesario)

```
Kiro, ajusta el quiz para que muestre ejemplos de uso de cada término
```

## 📖 Documentación Clave

### Para Desarrollo

- **`ai-specs/specs/opositaia-standards.mdc`**: Estándares específicos de OpositaIA
- **`ai-specs/specs/base-standards.mdc`**: Principios core de desarrollo
- **`ai-specs/README.md`**: Guía completa del sistema AI Specs

### Para Referencia

- **`/docs/AI_AGENTS.md`**: Definiciones de todos los agentes AI (CRÍTICO)
- **`/docs/ARCHITECTURE.md`**: Arquitectura del sistema
- **`/docs/DATA_MODEL.md`**: Tipos y estructuras de datos

### Ejemplo

- **`ai-specs/changes/EXAMPLE-audio-quiz.md`**: Plan completo de ejemplo

## ✨ Principios Clave

### 1. Documentación de Agentes AI es Obligatoria

Cada interacción con Gemini API DEBE documentarse en `/docs/AI_AGENTS.md`:

- Personalidad del agente
- Modelo seleccionado y justificación
- Instrucciones del sistema
- Formato de respuesta

### 2. Sigue Patrones Existentes

OpositaIA tiene patrones establecidos:

- **Service layer**: `services/geminiService.ts`
- **Componentes**: `components/[Feature].tsx`
- **Tipos**: `types.ts`
- **Estado**: `App.tsx`

### 3. Todo en Inglés

Código, comentarios, documentación, commits → English only

### 4. Desarrollo Incremental

Trabaja en pasos pequeños:
Plan → Tipos → Service → Componente → Integración → Docs → Testing

### 5. Calidad sobre Velocidad

- Testea exhaustivamente
- Maneja errores con gracia
- Proporciona buena UX (loading states, mensajes de error)
- Actualiza documentación

## 🎨 Selección de Modelos

### Usa `gemini-2.5-pro` cuando:

- Razonamiento complejo (generación de casos legales, exámenes)
- Adherencia estricta a JSON schema
- Contenido creativo de alta calidad (mapas mentales, planes)
- Workflows multi-paso
- Calidad > Velocidad

### Usa `gemini-2.5-flash` cuando:

- Chat/conversación interactiva
- Explicaciones rápidas
- Procesamiento de búsquedas
- Velocidad > Complejidad

### Usa `imagen-4.0-generate-001` cuando:

- Generación de contenido visual (memes, diagramas)

## 🔧 Troubleshooting

### "No encuentro el plan generado"

Busca en `ai-specs/changes/[nombre-feature].md`

### "Kiro no sigue los estándares"

Verifica que `GEMINI.md` esté en la raíz y contenga:

```
ai-specs/specs/base-standards.mdc
ai-specs/specs/opositaia-standards.mdc
docs/AI_AGENTS.md
```

### "Error al implementar"

1. Revisa el plan
2. Verifica que los archivos existan
3. Comprueba errores de TypeScript
4. Consulta `ai-specs/specs/opositaia-standards.mdc`

### "Quiero personalizar los estándares"

Edita `ai-specs/specs/opositaia-standards.mdc` con tus preferencias

## 🎓 Recursos de Aprendizaje

### Ejemplos en el Repo

- `ai-specs/changes/EXAMPLE-audio-quiz.md`: Plan completo de feature
- `ai-specs/changes/SCRUM-10_backend.md`: Ejemplo de backend (referencia)

### Comandos de Ayuda

```
Kiro, explica el workflow de AI Specs para OpositaIA
Kiro, muéstrame un ejemplo de plan de implementación
Kiro, ¿cómo documento un nuevo agente AI?
```

## 🚦 Próximos Pasos

### Ahora puedes:

1. **Explorar el ejemplo**

   ```
   Kiro, explícame el plan de ejemplo en @EXAMPLE-audio-quiz.md
   ```

2. **Crear tu primera feature**

   ```
   Kiro, planifica una feature de [tu idea]
   ```

3. **Mejorar features existentes**

   ```
   Kiro, mejora el generador de casos prácticos para incluir [mejora]
   ```

4. **Refactorizar código**
   ```
   Kiro, refactoriza [componente] siguiendo los estándares de OpositaIA
   ```

## 💡 Tips Pro

1. **Planifica primero**: Aunque sea tentador ir directo al código, planificar ahorra tiempo
2. **Revisa los planes**: Los planes generados son muy detallados, úsalos como guía
3. **Actualiza docs siempre**: `/docs/AI_AGENTS.md` debe estar siempre actualizado
4. **Commits pequeños**: Commits frecuentes y descriptivos
5. **Testea constantemente**: No esperes al final para probar
6. **Consulta ejemplos**: `EXAMPLE-audio-quiz.md` es tu amigo

## 🎉 ¡Listo para Desarrollar!

El sistema AI Specs está configurado y listo. Ahora puedes desarrollar features de forma estructurada, eficiente y con alta calidad.

**Primer comando sugerido:**

```
Kiro, muéstrame las features actuales de OpositaIA y sugiere 3 mejoras que podríamos implementar
```

---

**Versión**: AI Specs for OpositaIA v1.0  
**Basado en**: LIDR AI4Devs methodology  
**Adaptado para**: React + TypeScript + Google Gemini API
