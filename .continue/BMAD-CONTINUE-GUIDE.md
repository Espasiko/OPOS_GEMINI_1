# Guía de Uso: BMAD Method en Continue

## 🎯 Comandos Disponibles

Continue ahora tiene **62 slash commands** para invocar agentes y workflows BMAD:
- **17 agentes** especializados
- **45 workflows** de desarrollo completo

## 🤖 Agentes (17 comandos)

### Core
- `/bmad-master` - BMad Master Executor, Knowledge Custodian, and Workflow Orchestrator

### BMB (BMAD Builder)
- `/bmad-builder` - Generalist Builder and BMAD System Maintainer

### BMM (BMAD Method Manager)
- `/analyst` - Business Analyst (Mary)
- `/architect` - System Architect (Winston)
- `/dev` - Senior Software Engineer (Amelia)
- `/pm` - Product Manager (John)
- `/quick-flow-solo-dev` - Quick Flow Solo Dev (Barry)
- `/sm` - Scrum Master (Bob)
- `/tea` - Master Test Architect (Murat)
- `/tech-writer` - Technical Writer (Paige)
- `/ux-designer` - UX Designer (Sally)

### CIS (Creative Innovation Suite)
- `/brainstorming-coach` - Elite Brainstorming Specialist (Carson)
- `/creative-problem-solver` - Master Problem Solver (Dr. Quinn)
- `/design-thinking-coach` - Design Thinking Maestro (Maya)
- `/innovation-strategist` - Disruptive Innovation Oracle (Victor)
- `/presentation-master` - Visual Communication Expert (Caravaggio)
- `/storyteller` - Master Storyteller (Sophia)

## ⚙️ Workflows (45 comandos)

### Core Workflows
- `/brainstorming-session` - Facilitar sesiones de brainstorming
- `/party-mode` - Discusión grupal entre todos los agentes BMAD

### BMB Workflows (Construcción BMAD)
- `/create-agent` - Crear nuevo agente BMAD
- `/create-module` - Crear módulo BMAD completo
- `/create-workflow` - Crear workflow estructurado
- `/edit-agent` - Editar agente existente
- `/edit-workflow` - Editar workflow existente
- `/workflow-compliance-check` - Validar workflows contra estándares BMAD

### BMM Workflows (Desarrollo Completo)

**Análisis (Phase 1)**
- `/create-product-brief` - Crear brief de producto
- `/research` - Investigación de mercado/técnica/dominio

**Planificación (Phase 2)**
- `/create-prd` - Crear Product Requirements Document
- `/create-ux-design` - Diseñar UX y patrones

**Solutioning (Phase 3)**
- `/create-architecture` - Crear decisiones arquitectónicas
- `/create-epics-stories` - Transformar PRD en epics y stories
- `/check-implementation-readiness` - Validar preparación para implementación

**Implementación (Phase 4)**
- `/create-story` - Crear siguiente user story
- `/dev-story` - Ejecutar story completa
- `/code-review` - Revisión adversarial de código
- `/correct-course` - Navegar cambios significativos
- `/sprint-planning` - Generar sprint status tracking
- `/sprint-status` - Resumir estado del sprint
- `/retrospective` - Retrospectiva post-epic

**Quick Flow**
- `/quick-dev` - Desarrollo flexible rápido
- `/create-tech-spec` - Crear especificación técnica

**Diagramas**
- `/create-excalidraw-diagram` - Crear diagramas técnicos
- `/create-excalidraw-dataflow` - Crear diagramas de flujo de datos
- `/create-excalidraw-flowchart` - Crear flowcharts
- `/create-excalidraw-wireframe` - Crear wireframes

**Documentación**
- `/document-project` - Documentar proyecto brownfield
- `/generate-project-context` - Generar project_context.md

**Test Architecture**
- `/testarch-framework` - Inicializar framework de testing
- `/testarch-atdd` - Generar tests de aceptación (TDD)
- `/testarch-automate` - Expandir cobertura de tests
- `/testarch-test-design` - Diseño de testabilidad
- `/testarch-test-review` - Revisar calidad de tests
- `/testarch-trace` - Matriz de trazabilidad
- `/testarch-ci` - Scaffold CI/CD pipeline
- `/testarch-nfr` - Evaluar requisitos no funcionales

**Workflow Management**
- `/workflow-init` - Inicializar nuevo proyecto BMM
- `/workflow-status` - Verificar estado del workflow

### CIS Workflows (Creatividad e Innovación)
- `/design-thinking` - Proceso de design thinking
- `/innovation-strategy` - Estrategia de innovación disruptiva
- `/problem-solving` - Resolución sistemática de problemas
- `/storytelling` - Crear narrativas convincentes

## 📖 Ejemplos de Uso

### Ejemplo 1: Iniciar Proyecto Nuevo

```
1. /workflow-init
2. /create-product-brief
3. /create-prd
4. /create-architecture
5. /create-epics-stories
6. /check-implementation-readiness
7. /sprint-planning
```

### Ejemplo 2: Desarrollar Feature

```
1. /create-story
2. /dev-story
3. /code-review
4. /testarch-automate
```

### Ejemplo 3: Sesión Creativa

```
1. /brainstorming-session
2. /design-thinking
3. /innovation-strategy
```

### Ejemplo 4: Invocar Agente Específico

```
1. Abre Continue (Ctrl+L)
2. Escribe /pm
3. El agente John (Product Manager) se activará
4. Sigue las instrucciones del agente
```

## 🚀 Cómo Usar

### 1. Copiar Configuración

```bash
cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml ~/.continue/config.yaml
```

### 2. Configurar API Key

```bash
# Mistral (Codestral - modelo por defecto)
export MISTRAL_API_KEY='tu-api-key-aqui'

# Anthropic (Claude - backup)
export ANTHROPIC_API_KEY='tu-api-key-aqui'

# Hacer permanente
echo 'export MISTRAL_API_KEY="tu-key"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Recargar VS Code

Presiona `Ctrl+R` para recargar VS Code.

### 4. Usar Continue

1. Abre Continue: `Ctrl+L` (o `Cmd+L` en Mac)
2. Escribe `/` para ver todos los comandos disponibles
3. Selecciona un agente o workflow
4. Sigue las instrucciones

## 🔧 Troubleshooting

### El comando no aparece

- Verifica que Continue esté actualizado
- Recarga VS Code (`Ctrl+R`)
- Verifica que `config.yaml` esté en `~/.continue/`
- Revisa que `bmad-prompts/` exista en `.continue/`

### El agente no se activa correctamente

- Verifica que el archivo del agente exista en `.bmad/`
- Revisa que la ruta en el prompt sea correcta
- Comprueba los logs de Continue (Developer Tools)

### El workflow no ejecuta todos los pasos

- Lee el archivo del workflow completo primero
- Sigue los pasos en orden
- No improvises pasos adicionales

### Error de API Key

```bash
# Verificar que la variable esté configurada
echo $MISTRAL_API_KEY

# Si está vacía, configurarla
export MISTRAL_API_KEY='tu-api-key'
```

## 📊 Estructura de Archivos

```
.continue/
├── config.yaml                    # Configuración principal
├── rules.md                       # Reglas (incluye BMAD)
├── prompts.md                     # Prompts personalizados
├── bmad-prompts/                  # Prompts BMAD generados
│   ├── agents/                    # 17 agentes
│   │   ├── bmad-master.md
│   │   ├── analyst.md
│   │   └── ...
│   └── workflows/                 # 45 workflows
│       ├── create-prd.md
│       ├── dev-story.md
│       └── ...
└── scripts/
    └── generate-bmad-prompts.js   # Generador automático
```

## 🔄 Regenerar Prompts

Si se añaden nuevos agentes o workflows a BMAD:

```bash
node /home/spas/OPOS_GEMINI_1/.continue/scripts/generate-bmad-prompts.js
```

Esto regenerará automáticamente todos los prompts desde los manifiestos CSV.

## 📚 Recursos

- **Documentación Continue**: https://docs.continue.dev/
- **Manifiestos BMAD**: `.bmad/_cfg/agent-manifest.csv` y `workflow-manifest.csv`
- **Agentes BMAD**: `.bmad/core/agents/`, `.bmad/bmm/agents/`, etc.
- **Workflows BMAD**: `.bmad/core/workflows/`, `.bmad/bmm/workflows/`, etc.

---

**Versión**: 2.0.0  
**Fecha**: 17 de Febrero 2026  
**Estado**: ✅ Configuración completa y funcional
