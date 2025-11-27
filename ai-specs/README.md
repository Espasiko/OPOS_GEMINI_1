# AI Specs for OpositaIA

This directory contains AI-driven development standards, commands, and implementation plans for OpositaIA.

## Structure

```
ai-specs/
├── specs/                    # Development standards and guidelines
│   ├── base-standards.mdc    # Core development rules (all projects)
│   ├── opositaia-standards.mdc  # OpositaIA-specific standards
│   ├── frontend-standards.mdc   # React/TypeScript standards
│   └── documentation-standards.mdc  # Documentation guidelines
├── changes/                  # Feature implementation plans
│   └── [feature-name].md     # Step-by-step implementation plans
├── .commands/                # AI commands for development workflow
│   ├── plan-feature.md       # Create implementation plan
│   └── implement-feature.md  # Execute implementation plan
└── README.md                 # This file
```

## How to Use

### 1. Planning a New Feature

When you want to add a new feature to OpositaIA:

```
Hey Kiro, plan a new feature: [describe the feature]
```

Or reference the command:

```
@plan-feature.md Create a vocabulary quiz generator that uses gemini-2.5-flash
```

This will:

- Analyze the feature requirements
- Select appropriate Gemini model
- Create a detailed implementation plan in `ai-specs/changes/`
- Define AI agent configuration
- Plan component structure
- Specify documentation updates

### 2. Implementing a Feature

Once you have a plan:

```
@implement-feature.md @feature-name.md
```

This will:

- Follow the plan step-by-step
- Create feature branch
- Implement types, service, component
- Update App.tsx routing
- Update documentation
- Test the feature
- Commit changes

### 3. Understanding the Standards

All development follows these standards:

- **`base-standards.mdc`**: Core principles (TDD, type safety, English-only, incremental changes)
- **`opositaia-standards.mdc`**: OpositaIA-specific patterns (Gemini API integration, component patterns, documentation requirements)
- **`frontend-standards.mdc`**: React/TypeScript best practices
- **`documentation-standards.mdc`**: How to document code and features

## Key Principles

### 1. AI Agent Documentation is Mandatory

Every Gemini API interaction MUST be documented in `/docs/AI_AGENTS.md`:

- Agent personality/role
- Model selection and justification
- System instructions
- Response format

### 2. Follow Existing Patterns

OpositaIA has established patterns:

- Service layer: `services/geminiService.ts`
- Component structure: `components/[Feature].tsx`
- Type definitions: `types.ts`
- State management: `App.tsx`

### 3. English Only

All code, comments, documentation, and commit messages in English.

### 4. Incremental Development

Work in small steps:

1. Plan → 2. Types → 3. Service → 4. Component → 5. Integration → 6. Documentation → 7. Testing

### 5. Quality Over Speed

- Test thoroughly
- Handle errors gracefully
- Provide good UX (loading states, error messages)
- Update documentation

## Example Workflow

### Scenario: Add a "Legal Term Glossary" feature

#### Step 1: Plan

```
@plan-feature.md Create a legal term glossary that allows users to search for Spanish Social Security legal terms and get AI-generated definitions and examples. Use gemini-2.5-flash for quick responses.
```

**Output**: `ai-specs/changes/legal-glossary.md` with complete implementation plan

#### Step 2: Review Plan

- Read the generated plan
- Verify it makes sense
- Adjust if needed

#### Step 3: Implement

```
@implement-feature.md @legal-glossary.md
```

**Kiro will**:

1. Create branch `feature/legal-glossary`
2. Add types to `types.ts`
3. Add `searchLegalTerm()` to `geminiService.ts`
4. Create `components/LegalGlossary.tsx`
5. Update `App.tsx` routing
6. Update `/docs/AI_AGENTS.md`
7. Test the feature
8. Commit changes

#### Step 4: Test & Refine

- Test manually
- Fix any issues
- Refine UX

#### Step 5: Merge

- Review changes
- Merge to main

## Commands Reference

### Planning Commands

- **`@plan-feature.md [description]`**: Create implementation plan for new feature
  - Analyzes requirements
  - Selects Gemini model
  - Creates step-by-step plan
  - Output: `ai-specs/changes/[feature-name].md`

### Implementation Commands

- **`@implement-feature.md @[plan-file].md`**: Execute implementation plan
  - Follows plan step-by-step
  - Creates branch
  - Implements code
  - Updates documentation
  - Tests feature

### Documentation Commands

- **Update AI Agents**: When adding new Gemini API function

  ```
  Update /docs/AI_AGENTS.md with the new generateFeature() function
  ```

- **Update Data Model**: When adding new types
  ```
  Update /docs/DATA_MODEL.md with the new FeatureType interface
  ```

## Best Practices

### ✅ Do

- Plan before implementing
- Follow the plan step-by-step
- Update documentation as you code
- Test thoroughly
- Use English for everything
- Follow existing patterns
- Handle errors gracefully
- Provide good UX

### ❌ Don't

- Skip planning phase
- Jump ahead in implementation
- Forget to update `/docs/AI_AGENTS.md`
- Mix Spanish and English
- Create inconsistent patterns
- Skip error handling
- Ignore loading states
- Leave documentation outdated

## Integration with Existing Docs

The AI Specs system complements existing documentation:

- **`/docs/AI_AGENTS.md`**: Still the source of truth for AI interactions
- **`/docs/ARCHITECTURE.md`**: Still describes system architecture
- **`/docs/DATA_MODEL.md`**: Still documents types and data structures
- **`/README.md`**: Still the main project README

AI Specs adds:

- Structured development workflow
- Implementation planning
- Step-by-step execution
- Quality standards enforcement

## Customization

You can customize the standards for your needs:

1. **Edit Standards**: Modify files in `ai-specs/specs/`
2. **Add Commands**: Create new command files in `ai-specs/.commands/`
3. **Update Patterns**: Adjust `opositaia-standards.mdc` for project-specific patterns

## Questions?

- Check `ai-specs/specs/opositaia-standards.mdc` for OpositaIA-specific guidance
- Check `ai-specs/specs/base-standards.mdc` for core principles
- Review existing implementation plans in `ai-specs/changes/`
- Ask Kiro: "Explain the AI Specs workflow for OpositaIA"

## Version

AI Specs for OpositaIA v1.0
Based on LIDR AI4Devs methodology
Adapted for React + TypeScript + Gemini API projects
