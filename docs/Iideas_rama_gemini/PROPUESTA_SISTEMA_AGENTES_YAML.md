# 🎯 PROPUESTA: Sistema YAML de Agentes Multi-Capa para OpositAIA y comentarios mios dudas etc.

**Fecha**: 27 Noviembre 2025  
**Estado**: 📋 Plan (es muy mejorble, )  
**Autor**: Análisis exhaustivo del espiritu de BMAD Method + best practices para crearlo bien!!! 

---

## 📌 RESUMEN EJECUTIVO

Este documento presenta una propuesta completa para implementar un **Sistema de Agentes YAML Multi-Capa** similar a BMAD Method pero optimizado para OpositAIA. El sistema integrará:

1. **Arquitectura de Agentes YAML** - Definiciones declarativas reutilizables
2. **Manifests CSV** - Registro centralizado de agentes, workflows, tools
3. **Estrategia de Verificación 3-Capas** - Validación, verificación y generación de pruebas
4. **MCP Server Integrado** - Herramientas compartidas entre agentes
5. **Prompts Parametrizados** - Templates dinámicos con context injection

**Beneficios**:
- ✅ Agentes especializados sin code duplication
- ✅ Verificación automática de respuestas (3-layer validation)
- ✅ Reutilización de tools via MCP
- ✅ Fácil extensión y mantenimiento
- ✅ Trazabilidad completa (audit logs)

---

## 1. ARQUITECTURA DEL SISTEMA

### 1.1 Estructura de Directorios

```
opos-agents/
├── README.md                           # Documentación principal
├── config.yaml                         # Configuración global
├── manifests/                          # Registros centralizados
│   ├── agent-manifest.csv              # Catálogo de agentes
│   ├── workflow-manifest.csv           # Catálogo de workflows
│   ├── tool-manifest.csv               # Catálogo de tools
│   └── verification-manifest.csv       # Estrategia de verificación
├── agents/                             # Definiciones de agentes
│   ├── core/
│   │   ├── orchestrator.agent.yaml     # Orquestador principal
│   │   ├── validator.agent.yaml        # Validador de respuestas
│   │   └── synthesizer.agent.yaml      # Síntesis de resultados
│   ├── legal/
│   │   ├── examiner.agent.yaml         # Examinador legal
│   │   ├── jurisprudence-expert.agent.yaml
│   │   ├── case-analyzer.agent.yaml
│   │   └── law-researcher.agent.yaml
│   ├── educational/
│   │   ├── tutor.agent.yaml            # Tutor experto
│   │   ├── content-creator.agent.yaml  # Generador contenido
│   │   ├── assessment-expert.agent.yaml
│   │   └── study-planner.agent.yaml
│   └── verification/
│       ├── fact-checker.agent.yaml
│       ├── consistency-validator.agent.yaml
│       └── legal-auditor.agent.yaml
├── workflows/                          # Procesos multi-agente
│   ├── exam-generation/
│   │   ├── workflow.yaml
│   │   └── verification-rules.yaml
│   ├── case-analysis/
│   │   ├── workflow.yaml
│   │   └── verification-rules.yaml
│   ├── study-planning/
│   │   ├── workflow.yaml
│   │   └── verification-rules.yaml
│   └── legal-research/
│       ├── workflow.yaml
│       └── verification-rules.yaml
├── tools/                              # Herramientas compartidas
│   ├── rag-search.tool.yaml
│   ├── boe-verify.tool.yaml
│   ├── jurisprudence-search.tool.yaml
│   ├── content-generator.tool.yaml
│   ├── output-validator.tool.yaml
│   └── mock-tools.yaml                 # Para testing
├── prompts/                            # Plantillas de prompts
│   ├── system-prompts/
│   │   ├── legal-expert.prompt.yaml
│   │   ├── educational-expert.prompt.yaml
│   │   ├── validator.prompt.yaml
│   │   └── synthesizer.prompt.yaml
│   └── task-prompts/
│       ├── generate-exam.prompt.yaml
│       ├── analyze-case.prompt.yaml
│       ├── create-study-plan.prompt.yaml
│       └── research-law.prompt.yaml
├── verification/                       # Estrategia 3-capas
│   ├── layer1-validation.yaml          # Validación estructural
│   ├── layer2-verification.yaml        # Verificación de hechos
│   └── layer3-test-generation.yaml     # Generación de pruebas
├── examples/                           # Casos de uso
│   ├── exam-generation-example.md
│   ├── case-analysis-example.md
│   └── study-planning-example.md
└── mcp-server/                         # MCP Server (tools compartidas)
    ├── index.ts
    ├── tools/
    │   ├── rag-search.ts
    │   ├── boe-verify.ts
    │   ├── content-generator.ts
    │   └── output-validator.ts
    └── config.ts
```

---

## 2. ESTRUCTURA YAML DE AGENTES

### 2.1 Agente Base (Module Agent - Recomendado para OpositAIA)

```yaml
# opos-agents/agents/legal/examiner.agent.yaml
agent:
  metadata:
    id: "opos-agents/legal/examiner.agent.yaml"
    name: "Examiner"
    title: "Legal Examiner Agent"
    icon: "📝"
    module: "legal"
    version: "1.0.0"
    description: "Generates high-quality exam questions and practical cases for legal studies"
    
  persona:
    role: "Senior Legal Examiner + Assessment Specialist"
    
    identity: |
      Master-level expert in Spanish Social Security legislation and AGE (LGSS, EBEP, etc.).
      15+ years creating official exam questions. Specializes in:
      - Complex practical scenarios
      - Multi-article legal reasoning
      - Realistic assessment design
      - Pedagogical effectiveness
    
    communication_style: |
      Precise, methodical, educator-focused.
      Explains legal reasoning clearly for learning purposes.
      Uses specific article references (e.g., "Art. 161 LGSS").
      Avoids ambiguity in test questions.
    
    principles:
      - "Exam quality over speed - each question must educate"
      - "Ground every answer in specific legal articles"
      - "Create realistic scenarios that prepare students for real exams"
      - "Each question has only ONE correct answer - NO ambiguity"
      - "Explain the 'why' behind correct answers for learning"
  
  critical_actions:
    - "Load agent configuration from {project-root}/opos-agents/config.yaml"
    - "Load MCP tools manifest: {project-root}/opos-agents/manifests/tool-manifest.csv"
    - "Verify all tool dependencies available before proceeding"
    - "Load system prompt: {project-root}/opos-agents/prompts/system-prompts/legal-expert.prompt.yaml"
    - "Apply all verification rules before generating output"
    - "MANDATORY: Inject legal framework context from RAG before generating exam content"
  
  menu:
    - trigger: "*generate-exam"
      workflow: "{project-root}/opos-agents/workflows/exam-generation/workflow.yaml"
      description: "Generate high-quality exam questions"
      
    - trigger: "*analyze-case"
      workflow: "{project-root}/opos-agents/workflows/case-analysis/workflow.yaml"
      description: "Analyze practical legal cases"
      
    - trigger: "*verify-quality"
      exec: "{project-root}/opos-agents/tools/output-validator.tool.yaml"
      data: "{project-root}/opos-agents/verification/layer1-validation.yaml"
      description: "Verify output quality meets standards"
      
    - trigger: "*help"
      action: "Show numbered menu"
      
    - trigger: "*exit"
      action: "Exit with confirmation"
  
  prompts:
    - id: "generate-exam-question"
      content: |
        You are a master legal examiner specializing in Spanish Social Security law.
        
        **CRITICAL INSTRUCTIONS:**
        1. Generate ONLY ONE exam question - no more, no less
        2. The question must be based on {{topic}} from {{source_law}}
        3. Create 4 plausible options: A, B, C, D
        4. ONLY ONE option is correct - no ambiguity and its place is equally distributed between a/b/c/d
        5. Output MUST be valid JSON matching schema: {{schema_id}}
        
        **LEGAL REQUIREMENTS:**
        - Reference specific articles (e.g., "Art. 161 LGSS")
        - Include real-world practical elements
        - Avoid trick questions or gotchas
        - Question difficulty: {{difficulty}}
        
        **JSON OUTPUT SCHEMA:**
        ```json
        {
          "id": "q{{index}}",
          "question": "...",
          "options": [
            {"id": "A", "text": "..."},
            {"id": "B", "text": "..."},
            {"id": "C", "text": "..."},
            {"id": "D", "text": "..."}
          ],
          "correct_option_id": "A|B|C|D",
          "explanation": "Detailed legal explanation citing specific articles",
          "source_articles": ["Art. X LGSS", "Art. Y EBEP"],
          "difficulty": "easy|medium|hard",
          "pedagogical_notes": "Why this question tests important concepts"
        }
        ```

    - id: "verify-exam-quality"
      content: |
        You are a quality assurance expert for legal exams.
        
        **VERIFICATION CHECKLIST:**
        ✓ JSON structure valid?
        ✓ Exactly 1 correct answer?
        ✓ No ambiguous options?
        ✓ Explanation cites specific articles?
        ✓ Difficulty level appropriate?
        ✓ Question tests important legal concept?
        ✓ Options are plausible (not obviously wrong)?
        ✓ Spanish language correct?
        
        **OUTPUT FORMAT:**
        ```json
        {
          "is_valid": true|false,
          "issues": ["list of problems found"],
          "score": 0-100,
          "recommendations": ["improvement suggestions"]
        }
        ```

  install_config:
    compile_time_only: true
    questions:
      - var: "legal_framework"
        prompt: "Which legal framework to focus on?"
        type: "choice"
        options:
          - label: "LGSS (Social Security)"
            value: "LGSS"
          - label: "EBEP (Public Employees)"
            value: "EBEP"
          - label: "Mixed"
            value: "MIXED"
        default: "LGSS"
```

### 2.2 Agente de Validación/Verificación 
### ADOPTAR CRITERIOS CLAROS DE VALIDACION del contenido creado!

```yaml
# opos-agents/agents/core/validator.agent.yaml
agent:
  metadata:
    id: "opos-agents/core/validator.agent.yaml"
    name: "Validator"
    title: "Validation & Verification Agent"
    icon: "✅"
    module: "core"
    version: "1.0.0"
    description: "3-layer verification: structure, facts, test generation"

  persona:
    role: "Master Quality Assurance Expert + Verification Specialist"
    
    identity: |
      Rigorous QA professional specializing in legal content validation.
      Ensures output meets 3 verification layers:
      1. Structural validation (JSON schema, format)
      2. Factual verification (legal accuracy, article citations)
      3. Test coverage (comprehensive testing generated)
    
    communication_style: |
      Direct, checklist-driven, precise scoring.
      Reports issues with specific line references.
      Provides actionable improvement recommendations.
    
    principles:
      - "Verification rigor is non-negotiable"
      - "Each layer catches different issues"
      - "Generate tests to prevent future regressions"
      - "Score output objectively (0-100)"

  critical_actions:
    - "Load verification rules: {project-root}/opos-agents/verification/"
    - "Execute all 3 verification layers in sequence"
    - "Generate test cases from findings"
    - "Log verification results for audit trail"

  menu:
    - trigger: "*layer1-validate"
      exec: "{project-root}/opos-agents/verification/layer1-validation.yaml"
      description: "Validate structure and format"
      
    - trigger: "*layer2-verify"
      exec: "{project-root}/opos-agents/verification/layer2-verification.yaml"
      description: "Verify factual accuracy"
      
    - trigger: "*layer3-test"
      exec: "{project-root}/opos-agents/verification/layer3-test-generation.yaml"
      description: "Generate test cases"
      
    - trigger: "*full-audit"
      action: "Execute all 3 layers sequentially and generate report"
```

---

## 3. MANIFESTS CSV (REGISTROS CENTRALIZADOS)

### 3.1 Agent Manifest

```csv
name,displayName,title,icon,role,module,path,status,depends_on,mcp_tools
"examiner","Legal Examiner","Senior Legal Examiner + Assessment Specialist","📝","Create high-quality exam questions","legal",".opos-agents/agents/legal/examiner.agent.yaml","active","orchestrator","rag_search,boe_verify"
"validator","Validator","Validation & Verification Agent","✅","3-layer verification of outputs","core",".opos-agents/agents/core/validator.agent.yaml","active","","output_validator"
"synthesizer","Synthesizer","Results Synthesizer","🔄","Combine outputs from multiple agents","core",".opos-agents/agents/core/synthesizer.agent.yaml","active","",""
"orchestrator","Orchestrator","Master Orchestrator","🎯","Route tasks to appropriate agents","core",".opos-agents/agents/core/orchestrator.agent.yaml","active","",""
"tutor","Tutor","Educational Tutor","👨‍🏫","Provide tutoring and explanations","educational",".opos-agents/agents/educational/tutor.agent.yaml","active","","rag_search,content_generator"
"case-analyzer","Case Analyzer","Legal Case Analyzer","⚖️","Analyze practical legal cases","legal",".opos-agents/agents/legal/case-analyzer.agent.yaml","active","validator","rag_search,jurisprudence_search"
"study-planner","Study Planner","Study Plan Creator","📚","Create personalized study plans","educational",".opos-agents/agents/educational/study-planner.agent.yaml","active","",""
```

### 3.2 Tool Manifest

```csv
name,displayName,description,type,endpoint,rate_limit,auth_required,status
"rag_search","RAG Search","Search legal documents via Qdrant","tool","mcp://opositaia/rag_search","100/min","true","active"
"boe_verify","BOE Verification","Verify law status in BOE","tool","mcp://opositaia/boe_verify","50/min","true","active"
"jurisprudence_search","Jurisprudence Search","Search relevant case law","tool","mcp://opositaia/jurisprudence_search","50/min","true","active"
"content_generator","Content Generator","Generate study content","tool","mcp://opositaia/content_generator","20/min","true","active"
"output_validator","Output Validator","Validate JSON output format","tool","mcp://opositaia/output_validator","200/min","false","active"
"flashcard_generator","Flashcard Generator","Generate study flashcards","tool","mcp://opositaia/flashcard_generator","30/min","true","active"
```

### 3.3 Workflow Manifest

```csv
name,description,module,path,agents_involved,mcp_tools_required,validation_required,status
"exam-generation","Generate complete exam with questions","legal",".opos-agents/workflows/exam-generation/workflow.yaml","examiner,validator,synthesizer","rag_search,output_validator","true","active"
"case-analysis","Analyze practical legal case","legal",".opos-agents/workflows/case-analysis/workflow.yaml","case-analyzer,validator,tutor","rag_search,jurisprudence_search","true","active"
"study-planning","Create personalized study plan","educational",".opos-agents/workflows/study-planning/workflow.yaml","study-planner,tutor,validator","content_generator","true","active"
"legal-research","Research specific legal topic","legal",".opos-agents/workflows/legal-research/workflow.yaml","law-researcher,case-analyzer","rag_search,boe_verify,jurisprudence_search","false","active"
```

### 3.4 Verification Manifest

```csv
layer,name,description,type,checks,severity,auto_fix,status
"1","structure-validation","Validate JSON schema and format","schema","json_valid,required_fields","critical","false","active"
"1","length-validation","Validate content length constraints","constraint","min_length,max_length","high","false","active"
"2","fact-checking","Verify legal accuracy and citations","semantic","article_exists,date_valid,reference_correct","critical","false","active"
"2","consistency-check","Verify internal consistency","semantic","no_contradictions,logical_flow","high","false","active"
"3","test-generation","Generate regression tests","procedural","create_test_cases,coverage_analysis","medium","true","active"
```

---

## 4. ESTRATEGIA DE VERIFICACIÓN 3-CAPAS

### 4.1 Capa 1: Validación Estructural

```yaml
# opos-agents/verification/layer1-validation.yaml
name: "Layer 1 - Structural Validation"
description: "Validates JSON schema, format, and basic constraints"
severity: "CRITICAL"

checks:
  - id: "schema-validation"
    name: "JSON Schema Validation"
    description: "Verify output matches expected schema"
    validation_type: "schema"
    schema_reference: "schemas/exam-question.json"
    error_on_failure: true
    
  - id: "required-fields"
    name: "Required Fields Check"
    description: "Ensure all mandatory fields present"
    fields: ["id", "question", "options", "correct_option_id", "explanation"]
    error_on_failure: true
    
  - id: "options-count"
    name: "Options Count Validation"
    description: "Verify exactly 4 options (A, B, C, D)"
    min_options: 4
    max_options: 4
    error_on_failure: true
    
  - id: "correct-answer-valid"
    name: "Correct Answer Validation"
    description: "Verify correct_option_id is A, B, C, or D"
    valid_values: ["A", "B", "C", "D"]
    error_on_failure: true
    
  - id: "encoding-check"
    name: "Character Encoding Validation"
    description: "Ensure UTF-8 encoding with no corrupted characters"
    encoding: "utf-8"
    error_on_failure: false

scoring:
  total_points: 20
  checks:
    - id: "schema-validation"
      points: 5
    - id: "required-fields"
      points: 5
    - id: "options-count"
      points: 5
    - id: "correct-answer-valid"
      points: 5
```

### 4.2 Capa 2: Verificación de Hechos

```yaml
# opos-agents/verification/layer2-verification.yaml
name: "Layer 2 - Factual Verification"
description: "Verifies legal accuracy, citations, and consistency"
severity: "CRITICAL"

checks:
  - id: "article-existence"
    name: "Article Citation Validation"
    description: "Verify all cited articles actually exist in laws"
    validation_type: "semantic+hibrid+url-s BOE"
    mcp_tool: "rag_search"
    examples:
      - "Art. 161 LGSS must exist"
      - "Art. 45 BOE-no must exist"
    error_on_failure: true
    
  - id: "legal-accuracy"
    name: "Legal Accuracy Check"
    description: "Verify explanation matches actual law content"
    validation_type: "semantic"
    mcp_tool: "rag_search"
    check_against: "rag-indexed-laws"
    error_on_failure: true
    
  - id: "answer-correctness"
    name: "Answer Correctness Verification"
    description: "Verify that the marked correct answer is indeed correct"
    validation_type: "semantic"
    mcp_tool: "rag_search"
    error_on_failure: true
    
  - id: "no-ambiguity"
    name: "Ambiguity Detection"
    description: "Verify no other options could be correct"
    validation_type: "semantic"
    error_on_failure: true
    
  - id: "consistency-check"
    name: "Internal Consistency"
    description: "Verify no contradictions between question/options/explanation"
    validation_type: "semantic"
    error_on_failure: true

scoring:
  total_points: 40
  checks:
    - id: "article-existence"
      points: 8
    - id: "legal-accuracy"
      points: 12
    - id: "answer-correctness"
      points: 10
    - id: "no-ambiguity"
      points: 5
    - id: "consistency-check"
      points: 5
```

### 4.3 Capa 3: Generación de Pruebas

```yaml
# opos-agents/verification/layer3-test-generation.yaml
name: "Layer 3 - Test Generation"
description: "Generates regression tests to prevent future issues"
severity: "HIGH"

test_generation:
  - id: "correctness-test"
    name: "Answer Correctness Test"
    description: "Verify correct answer is marked correctly"
    test_type: "unit"
    assertions:
      - "correct_option_id must be A, B, C, or D"
      - "Only 1 option is correct"
      - "Explanation supports marked answer"
    
  - id: "format-test"
    name: "Format Compliance Test"
    description: "Verify output format consistency"
    test_type: "unit"
    assertions:
      - "id field format: 'q{{number}}'"
      - "question is non-empty string"
      - "Each option has id and text"
    
  - id: "legal-accuracy-test"
    name: "Legal Accuracy Test"
    description: "Verify legal content accuracy"
    test_type: "integration"
    test_data:
      - articles: ["Art. 161 LGSS"]
        expected_topics: ["incapacidad temporal", "prestaciones"]
      - articles: ["Art. 45 EBEP"]
        expected_topics: ["derechos funcionarios"]
    
  - id: "regression-test"
    name: "Regression Test Suite"
    description: "Prevent similar issues from happening again"
    test_type: "regression"
    stores_for_future: true

coverage:
  required_minimum: 80
  modules:
    - "answer-correctness"
    - "legal-accuracy"
    - "no-ambiguity"
    - "format-compliance"
```

---

## 5. WORKFLOWS MULTI-AGENTE

### 5.1 Workflow de Generación de Examen

```yaml
# opos-agents/workflows/exam-generation/workflow.yaml
name: "exam-generation"
description: "Generate complete exam with automatic validation"
author: "OpositAIA"

parameters:
  topic: {type: string, required: true, description: "Legal topic for exam"}
  question_count: {type: integer, required: true, min: 1, max: 50}
  difficulty: {type: choice, required: true, options: ["easy", "medium", "hard"]}
  language_framework: {type: choice, default: "LGSS", options: ["LGSS", "EBEP", "MIXED"]}

steps:
  - id: "step-1-rag-context"
    name: "Load RAG Context"
    agent: "orchestrator"
    action: "search_rag"
    params:
      query: "{{topic}} {{language_framework}}"
      limit: 10
      score_threshold: 0.8
    output: "rag_context"
    on_failure: "abort"
    
  - id: "step-2-generate"
    name: "Generate Questions"
    agent: "examiner"
    parallel_count: "{{question_count}}"
    action: "generate_exam_question"
    params:
      topic: "{{topic}}"
      source_law: "{{language_framework}}"
      difficulty: "{{difficulty}}"
      rag_context: "{{rag_context}}"
      schema_id: "exam-question-v1"
    output: "raw_questions"
    depends_on: ["step-1-rag-context"]
    on_failure: "retry-3x"
    
  - id: "step-3-validate"
    name: "Validate Structure (Layer 1)"
    agent: "validator"
    parallel_count: "{{question_count}}"
    action: "layer1_validate"
    params:
      input: "{{raw_questions}}"
      schema: "schemas/exam-question.json"
    output: "validation_layer1"
    depends_on: ["step-2-generate"]
    on_failure: "report"
    
  - id: "step-4-verify"
    name: "Verify Accuracy (Layer 2)"
    agent: "validator"
    parallel_count: "{{question_count}}"
    action: "layer2_verify"
    params:
      input: "{{raw_questions}}"
      rag_context: "{{rag_context}}"
    output: "verification_layer2"
    depends_on: ["step-3-validate"]
    on_failure: "report"
    
  - id: "step-5-test-generation"
    name: "Generate Tests (Layer 3)"
    agent: "validator"
    action: "layer3_generate_tests"
    params:
      input: "{{raw_questions}}"
      verification_results: "{{verification_layer2}}"
    output: "test_suite"
    depends_on: ["step-4-verify"]
    on_failure: "warn"
    
  - id: "step-6-synthesize"
    name: "Synthesize Results"
    agent: "synthesizer"
    action: "combine_results"
    params:
      questions: "{{raw_questions}}"
      validation: "{{validation_layer1}}"
      verification: "{{verification_layer2}}"
      tests: "{{test_suite}}"
      quality_threshold: 0.85
    output: "final_exam"
    depends_on: ["step-3-validate", "step-4-verify", "step-5-test-generation"]
    on_failure: "abort"

output:
  format: "json"
  schema: "exam-v1.json"
  includes:
    - questions
    - quality_scores
    - verification_results
    - test_suite
    - metadata

quality_gates:
  - gate: "all_questions_valid_json"
    threshold: 100
    action: "abort"
    
  - gate: "all_articles_verified"
    threshold: 100
    action: "abort"
    
  - gate: "no_ambiguous_questions"
    threshold: 100
    action: "abort"
    
  - gate: "average_quality_score"
    threshold: 85
    action: "warn"
```

---

## 6. MCP SERVER INTEGRACIÓN

### 6.1 MCP Tools Manifest

```yaml
# opos-agents/mcp-server/tools.yaml
mcp_server:
  name: "OpositAIA MCP Server"
  version: "1.0.0"
  description: "Shared tools for all agents"

tools:
  - id: "rag_search"
    name: "RAG Search"
    description: "Search legal documents via Qdrant"
    type: "search"
    input_schema:
      query: {type: string, required: true}
      limit: {type: integer, default: 5, min: 1, max: 20}
      score_threshold: {type: number, default: 0.7, min: 0, max: 1}
      layer_filter: {type: integer, optional: true}
    output_schema:
      results:
        - id: string
          ley: string
          articulo: string
          contenido: string
          score: number
    rate_limit: "100/minute"
    auth_required: true
    
  - id: "boe_verify"
    name: "BOE Verification"
    description: "Verify law status in Official Gazette"
    type: "verify"
    input_schema:
      ley_id: {type: string, required: true}
      articulo: {type: string, optional: true}
    output_schema:
      estado: {enum: ["VIGENTE", "DEROGADO", "MODIFICADO"]}
      fecha_ultima_modificacion: string
      boe_url: string
    rate_limit: "50/minute"
    auth_required: true
    
  - id: "jurisprudence_search"
    name: "Jurisprudence Search"
    description: "Search relevant case law"
    type: "search"
    input_schema:
      query: {type: string, required: true}
      tribunal: {type: choice, default: "todos", options: ["TS", "TSJ", "todos"]}
      limit: {type: integer, default: 3}
    output_schema:
      results:
        - id: string
          tribunal: string
          numero_sentencia: string
          fecha: string
          resumen: string
    rate_limit: "50/minute"
    auth_required: true
    
  - id: "content_generator"
    name: "Content Generator"
    description: "Generate study content (summaries, flashcards)"
    type: "generator"
    input_schema:
      content_type: {type: choice, options: ["summary", "flashcard", "mindmap"]}
      topic: {type: string, required: true}
      length: {type: choice, default: "medium", options: ["short", "medium", "long"]}
    rate_limit: "20/minute"
    auth_required: true
    
  - id: "output_validator"
    name: "Output Validator"
    description: "Validate JSON output format"
    type: "validator"
    input_schema:
      output: {type: object, required: true}
      schema_id: {type: string, required: true}
    output_schema:
      is_valid: boolean
      issues: [string]
      score: number
    rate_limit: "200/minute"
    auth_required: false
```

### 6.2 MCP Server Implementation Pattern

```typescript
// opos-agents/mcp-server/tools/rag-search.ts
import { Server, Tool } from "@modelcontextprotocol/sdk/server/index.js";

export const ragSearchTool: Tool = {
  name: "rag_search",
  description: "Search legal documents via Qdrant",
  inputSchema: {
    type: "object" as const,
    properties: {
      query: { type: "string", description: "Search query" },
      limit: { type: "number", description: "Max results", default: 5 },
      score_threshold: { type: "number", description: "Min similarity", default: 0.7 },
      layer_filter: { type: "number", description: "RAG layer filter", optional: true },
    },
    required: ["query"],
  },
};

// Handler
async function handleRagSearch(args: any) {
  // 1. Validate inputs (use MCP tool schema)
  if (!args.query || typeof args.query !== "string") {
    throw new Error("query is required and must be string");
  }
  
  // 2. Rate limiting (100 calls/min)
  await checkRateLimit("rag_search", 100, 60);
  
  // 3. Call Qdrant RAG
  const results = await qdrantClient.search({
    collection: QDRANT_COLLECTION,
    vector: await generateEmbedding(args.query),
    limit: args.limit || 5,
    score_threshold: args.score_threshold || 0.7,
  });
  
  // 4. Format response
  return {
    query: args.query,
    total_results: results.length,
    results: results.map(r => ({
      id: r.id,
      ley: r.payload.ley,
      articulo: r.payload.articulo,
      contenido: r.payload.contenido,
      score: r.score,
    })),
  };
}
```

---

## 7. PROMPTS PARAMETRIZADOS

### 7.1 System Prompt Template

```yaml
# opos-agents/prompts/system-prompts/legal-expert.prompt.yaml
name: "legal-expert-system-prompt"
version: "1.0.0"
description: "System prompt for legal expert agents"

template: |
  You are a {{role}} specializing in {{specialization}}.
  
  **YOUR EXPERTISE:**
  {{expertise}}
  
  **YOUR COMMUNICATION STYLE:**
  {{communication_style}}
  
  **YOUR CORE PRINCIPLES:**
  {{#each principles}}
  - {{this}}
  {{/each}}
  
  **CONTEXT FROM RAG:**
  {{rag_context}}
  
  **VERIFICATION REQUIREMENTS:**
  1. Every claim must cite specific legal articles
  2. All articles must exist in {{legal_framework}}
  3. Your answer must be internally consistent
  4. No ambiguity in your output
  
  **OUTPUT FORMAT:**
  {{output_format_schema}}

variables:
  role: "Senior Legal Examiner"
  specialization: "BOE, AGE (administracion general de estado), Spanish Social Security Laws (LGSS, EBEP)"
  expertise: |
    15+ years creating official exam questions
    Master of LGSS (Real Decreto Legislativo 8/2015)
    Expert in EBEP (Law 39/2015)
    Specialized in practical case scenarios and much more + oposisiones experto
  communication_style: "Precise, methodical, educator-focused using the best practices and altenative methods educatiolal strategies"
  principles:
    - "Exam quality over speed"
    - "Ground every answer in specific articles"
    - "Create realistic exam scenarios"
    -"use thr best legal logic and practices "
    - "Each question has only ONE correct answer"
    -"adapting the level of difficulty of the exam created to the level of the student, when asked to do so"
  legal_framework: "LGSS"
  output_format_schema: "exam-question-v1.json"
  rag_context: "{{injected_at_runtime}}"
```

### 7.2 Task Prompt with Injection

```yaml
# opos-agents/prompts/task-prompts/generate-exam.prompt.yaml
name: "generate-exam-question"
version: "1.0.0"

template: |
  **TASK:** Generate ONE exam question
  
  **PARAMETERS:**
  - Topic: {{topic}}
  - Legal Framework: {{legal_framework}}
  - Difficulty: {{difficulty}}
  - Question Index: {{question_index}} of {{total_questions}}
  
  **RAG CONTEXT (Injected at runtime):**
  {{rag_context}}
  - Related articles found: {{article_count}}
  - Relevance scores: {{article_scores}}
  - Key concepts: {{key_concepts}}
  
  **REQUIREMENTS:**
  1. Question must be based on {{legal_framework}} laws
  2. Reference specific articles in {{article_list}}
  3. Create realistic scenario matching {{difficulty}} level
  4. Exactly 4 options (A, B, C, D)
  5. Only ONE correct answer
  6. Detailed explanation in Spanish
  
  **OUTPUT (MUST be valid JSON):**
  ```json
  {
    "id": "q{{question_index}}",
    "question": "...",
    "options": [...],
    "correct_option_id": "A|B|C|D",
    "explanation": "...",
    "source_articles": [...],
    "difficulty": "{{difficulty}}",
    "pedagogical_notes": "..."
  }
  ```

variables:
  topic: "{{dynamic}}"
  legal_framework: "{{dynamic}}"
  difficulty: "{{dynamic}}"
  question_index: "{{dynamic}}"
  total_questions: "{{dynamic}}"
  rag_context: "{{injected_at_runtime}}"
  article_count: "{{computed}}"
  article_scores: "{{computed}}"
  key_concepts: "{{computed}}"
```

---
## !!!! falta el variante para casos practicos mapas mentales etc,hasta cubrir todos los etregables que necesitamos en  la version final de la app para produccion!!!!

## 8. EJEMPLO COMPLETO: GENERACIÓN DE test/preguntas de  EXAMEN para oposiciones

### 8.1 Flujo de Ejecución

```
USER: "Generate 3 exam questions about LGSS Art. 161"
  ↓
ORCHESTRATOR (Core Agent)
  ├─ Parse request
  ├─ Validate parameters
  └─ Route to examiner workflow
       ↓
WORKFLOW: exam-generation
  ├─ Step 1: RAG Context Load
  │  └─ MCP Tool: rag_search
  │     Query: "LGSS Art. 161 incapacidad"
  │     Returns: 10 relevant docs with scores
  │
  ├─ Step 2: Generate Questions (Parallel ×3)
  │  └─ EXAMINER Agent (×3 parallel instances)
  │     Inject: RAG context, system prompt, task prompt
  │     Output: 3 raw JSON questions
  │
  ├─ Step 3: Validate Structure (Parallel ×3)
  │  └─ VALIDATOR Agent Layer 1
  │     Check: JSON schema, required fields, options count
  │     Output: Validation scores + issues
  │
  ├─ Step 4: Verify Accuracy (Parallel ×3)
  │  └─ VALIDATOR Agent Layer 2
  │     Check: Article existence, legal accuracy, no ambiguity
  │     MCP Tool: rag_search (verify citations)
  │     Output: Verification scores + issues
  │
  ├─ Step 5: Generate Tests (Parallel ×3)
  │  └─ VALIDATOR Agent Layer 3
  │     Create: Unit + integration + regression tests
  │     Output: Test suite
  │
  ├─ Step 6: Synthesize Results
  │  └─ SYNTHESIZER Agent
  │     Combine: Questions + validations + verifications + tests
  │     Apply: Quality gates (85% min score)
  │     Output: Final exam JSON
  │
  └─ Return final exam with metadata
```

### 8.2 JSON Output Ejemplo

```json
{
  "exam_id": "exam-lgss-161-20251127-001",
  "metadata": {
    "generated_at": "2025-11-27T15:30:00Z",
    "topic": "LGSS Article 161",
    "difficulty": "hard",
    "question_count": 3,
    "total_score": 92,
    "all_passed_quality_gates": true
  },
  "questions": [
    {
      "id": "q1",
      "question": "Según el Art. 161 LGSS, ¿cuál es la duración máxima...",
      "options": [
        {"id": "A", "text": "..."},
        {"id": "B", "text": "..."},
        {"id": "C", "text": "..."},
        {"id": "D", "text": "..."}
      ],
      "correct_option_id": "B",
      "explanation": "La respuesta correcta es B porque el Art. 161 LGSS...",
      "source_articles": ["Art. 161 LGSS", "RD 575/1997"],
      "difficulty": "hard",
      "layer1_validation": {"score": 100, "passed": true},
      "layer2_verification": {"score": 95, "passed": true},
      "test_suite": [
        {"type": "unit", "name": "answer-correctness", "status": "pass"}
      ]
    }
  ],
  "quality_report": {
    "layer1_avg_score": 100,
    "layer2_avg_score": 93,
    "overall_quality": 92,
    "issues_found": ["Minor: Article 161 could include reference to RD 575"],
    "recommendations": []
  }
}
```

---

## 9. MEJORES PRÁCTICAS IMPLEMENTADAS

### 9.1 Patrones de BMAD Adoptados

| Patrón BMAD | Adaptación OpositAIA | Beneficio |
|-------------|---------------------|----------|
| **Module Agents** | Agentes especializados (Examiner, Validator, Tutor) | Separación de concerns |
| **Critical Actions** | Load config, MCP tools, verification rules | Inicialización consistente |
| **Prompts con Variables** | System + Task prompts parametrizados | Reutilización, context injection |
| **Manifests CSV** | Agent, Tool, Workflow, Verification manifests | Visibilidad centralizada |
| **Workflow YAML** | Multi-step, parallel execution, quality gates | Procesos confiables |
| **MCP Tools** | Herramientas compartidas entre agentes | Eliminación duplicación |
| **3-Layer Verification** | Estructura, Hechos, Pruebas | Calidad garantizada |

### 9.2 Best Practices de Industria

| Práctica | Implementación | Ventaja |
|----------|-----------------|---------|
| **Semantic Versioning** | Agent v1.0.0, Tool v1.0.0 | Rastrabilidad |
| **Schema Validation** | JSON schema v1, output validation | Confiabilidad |
| **Rate Limiting** | 100/min RAG, 20/min generator | Control de costos |
| **Audit Logging** | Todos los pasos registrados | Trazabilidad |
| **Error Handling** | Retry, fallback, abort | Resiliencia |
| **Parallel Execution** | Generar ×N questions en paralelo | Performance |
| **Test Generation** | Regresión tests auto-generados | Calidad sostenida |

---

## 10. ROADMAP IMPLEMENTACIÓN

### Fase 1: Setup (1-2 semanas)
- [ ] Crear estructura de directorios `opos-agents/`
- [ ] Definir Agent YAML base
- [ ] Crear Manifests CSV
- [ ] Setup MCP tools estructura

### Fase 2: Core Agents (2-3 semanas)
- [ ] Implementar Examiner Agent
- [ ] Implementar Validator Agent (3 capas)
- [ ] Implementar Synthesizer Agent
- [ ] Crear prompts parametrizados

### Fase 3: Workflows (2-3 semanas)
- [ ] Workflow exam-generation completo
- [ ] Workflow case-analysis
- [ ] Workflow study-planning
- [ ] Testing exhaustivo

### Fase 4: MCP Integration (1-2 semanas)
- [ ] Conectar MCP tools a agents
- [ ] Rate limiting
- [ ] Error handling
- [ ] Monitoring

### Fase 5: Operacionalización (1 semana)
- [ ] Documentación completa
- [ ] Training para equipo
- [ ] Monitoring + alertas
- [ ] Deployment a producción

---

## 11. MÉTRICAS Y MONITOREO

```yaml
# opos-agents/monitoring/metrics.yaml
metrics:
  generation:
    - "exam_generation_success_rate"
    - "avg_generation_time_seconds"
    - "parallel_execution_efficiency"
    
  quality:
    - "layer1_validation_pass_rate"
    - "layer2_verification_pass_rate"
    - "overall_quality_score_avg"
    - "questions_with_issues_percentage"
    
  mcp:
    - "rag_search_success_rate"
    - "boe_verify_success_rate"
    - "mcp_tool_call_latency_ms"
    - "rate_limit_hits_per_day"
    
  agent_performance:
    - "examiner_hallucination_rate"
    - "validator_false_positive_rate"
    - "validator_false_negative_rate"
    - "synthesizer_accuracy_rate"

alerts:
  - name: "low_quality_score"
    threshold: "< 80"
    action: "Notify, Disable output"
    
  - name: "high_error_rate"
    threshold: "> 5%"
    action: "Notify, Investigate"
    
  - name: "rate_limit_exceeded"
    threshold: "Hit"
    action: "Queue, Backoff, Notify"
```

---

## 12. COMPARATIVA: ARQUITECTURA ACTUAL vs PROPUESTA

| Aspecto | Actual | Propuesta | Mejora |
|---------|--------|-----------|--------|
| **Agentes** | Monolítico en geminiService.ts | 8+ agentes especializados | ✅ Modularidad |
| **Validación** | Mínima (JSON check) | 3 capas exhaustivas | ✅ Confiabilidad |
| **Tools Compartidas** | No (duplicación) | MCP Server centralizado | ✅ Mantenibilidad |
| **Reproducibilidad** | Difícil (prompts en código) | YAML + manifests | ✅ Trazabilidad |
| **Scaling** | Limitado | Parallelización built-in | ✅ Performance |
| **Documentación de Agentes** | Informal | Formal YAML | ✅ Onboarding |
| **Test Generation** | Manual | Automática (Layer 3) | ✅ Sostenibilidad |

---

## 13. PRÓXIMOS PASOS

**Para el usuario:**

1. **Review esta propuesta** - Feedback sobre arquitectura, agentes, workflows
2. **Validar scope** - ¿Agregar/remover agentes? ¿Alterar flujos?
3. **Definir prioridades** - ¿Empezar con Examiner o Validator primero?
4. **Recursos** - ¿Quién implementa cada componente?
5. **DESICIONES PARA TOMAR** - ¿CUANTOS MAS AGENTES HACEN FALTA PARA TENER MAXIMA VIABILIDAD CALIDAD Y NO HACER EL SISTEMA INFINITAMENTE COMPLEJO Y COMPLICADO?

**Decisiones clave pendientes: no estan bien definidas ni se porque estn aquí?**

- [ ] ¿Usar BMAD Method como framework o implementar nuestro propio? esta decision no se porque y a que se refiere?
- [ ] ¿Integrar con GitHub Copilot o solo backend agents? ¡¡¡ absurdo , no uso github copilot!!!! 
- [ ] ¿Level de formalidad de YAML** - ¿Máximo rigor o pragmático? esto si, hay que decidirlo, pero antes debes investigarlo!!!! 

---

## CONCLUSIÓN

Esta propuesta establece una **base sólida** para evolucionar desde una arquitectura monolítica a un **sistema modular, escalable y verificable de agentes**. 

Principales ventajas:
- 🎯 **Especialización**: Cada agente tiene un propósito claro
- ✅ **Confiabilidad**: 3 capas de verificación garantizan calidad
- 📦 **Reutilización**: MCP tools compartidas, sin duplicación
- 📊 **Observabilidad**: Manifests + audit logs completos
- 🚀 **Escalabilidad**: Ejecución paralela, rate limiting, monitoring

**Siguiente fase**: Implementación incremental comenzando con Core Agents + Workflows de prueba.

