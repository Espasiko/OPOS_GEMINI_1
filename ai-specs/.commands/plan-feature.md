# Role

You are an expert React + TypeScript developer with deep knowledge of Google Gemini API integration and AI-driven application development.

# Feature Description

$ARGUMENTS

# Goal

Create a comprehensive, step-by-step implementation plan for a new OpositaIA feature that integrates with Google Gemini API.

# Process and Rules

1. **Analyze Requirements**
   - Understand the feature request
   - Identify which Gemini model to use (pro vs flash)
   - Determine if new AI agent definition is needed

2. **Review Existing Context**
   - Check `/docs/AI_AGENTS.md` for similar patterns
   - Review `/types.ts` for existing types
   - Check `/services/geminiService.ts` for similar functions
   - Review `/components` for similar UI patterns

3. **Create Implementation Plan**
   - Define AI agent personality and configuration
   - Design API integration in `geminiService.ts`
   - Plan component structure
   - Define TypeScript types
   - Plan state management in App.tsx
   - Specify documentation updates

4. **Apply Best Practices**
   - Follow patterns in `ai-specs/specs/opositaia-standards.mdc`
   - Ensure English-only code and documentation
   - Plan for error handling and loading states
   - Consider user experience

5. **Do Not Write Code Yet**
   - Provide only the plan
   - Code implementation comes after plan approval

# Output Format

Create a markdown document at `ai-specs/changes/[feature-name].md` with this structure:

## Implementation Plan: [Feature Name]

### 1. Overview

- Brief description of the feature
- User benefit
- Technical approach

### 2. AI Agent Definition

#### Model Selection

- **Model**: `gemini-2.5-pro` or `gemini-2.5-flash` or `imagen-4.0`
- **Justification**: Why this model?

#### Agent Configuration

```typescript
{
  model: 'model-name',
  generationConfig: {
    responseMimeType: "application/json" | "text/plain",
    responseSchema: SchemaDefinition // if JSON
  }
}
```

#### System Instruction / Prompt

```
Agent personality: [Define the role]

Task: [What the agent should do]

Output format: [Expected format]
```

### 3. Implementation Steps

#### Step 0: Create Feature Branch

- **Branch Name**: `feature/[feature-name]`
- **Commands**:
  ```bash
  git checkout -b feature/[feature-name]
  ```

#### Step 1: Define Types

- **File**: `types.ts`
- **Action**: Add new types/interfaces
- **Types to Add**:

  ```typescript
  export interface NewFeatureType {
    // Define structure
  }

  // Update AppView enum if new view
  export enum AppView {
    // ... existing
    NEW_FEATURE = 'NEW_FEATURE',
  }
  ```

#### Step 2: Implement Service Function

- **File**: `services/geminiService.ts`
- **Function Signature**:
  ```typescript
  export async function generateNewFeature(input: InputType): Promise<OutputType>;
  ```
- **Implementation Steps**:
  1. Get model instance with configuration
  2. Build prompt with agent personality
  3. Call generateContent()
  4. Parse and return result
  5. Handle errors appropriately

#### Step 3: Create Component

- **File**: `components/NewFeature.tsx`
- **Component Structure**:

  ```typescript
  interface NewFeatureProps {
    onClose: () => void;
  }

  export const NewFeature: React.FC<NewFeatureProps>;
  ```

- **State Management**:
  - Loading state
  - Result state
  - Error state
  - Input state
- **UI Elements**:
  - Input form
  - Generate button
  - Loading indicator
  - Result display
  - Error display
  - Close/back button

#### Step 4: Update App.tsx

- **Actions**:
  1. Import new component
  2. Add state for feature data (if needed)
  3. Add case in view switch statement
  4. Add navigation button in sidebar

#### Step 5: Update Documentation

##### Update `/docs/AI_AGENTS.md`

Add new section:

```markdown
### N. `generateNewFeature()`

- **Función:** `generateNewFeature(input)`
- **Agente/Personalidad:** "[Agent description]"
- **Modelo:** `model-name`
- **Justificación:** [Why this model and configuration]
- **Configuración Clave:**
  - `model: 'model-name'`
  - `responseMimeType: "..."`
  - `responseSchema`: [Schema description]
```

##### Update `/docs/DATA_MODEL.md`

Add new types documentation

##### Update `README.md`

Add feature to features list if user-facing

### 4. Testing Checklist

#### Manual Testing

- [ ] Feature loads without errors
- [ ] Input validation works
- [ ] Loading state displays correctly
- [ ] API call succeeds with valid input
- [ ] Results display properly
- [ ] Error handling works (network error, API error)
- [ ] Navigation works (close button, back to menu)
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Data persists if applicable

#### Edge Cases

- [ ] Empty input
- [ ] Very long input
- [ ] Special characters
- [ ] Network timeout
- [ ] API rate limiting

### 5. Error Handling

#### API Errors

```typescript
try {
  const result = await geminiService.generateNewFeature(input);
  setResult(result);
} catch (error) {
  console.error('Error generating feature:', error);
  setError('Failed to generate. Please try again.');
}
```

#### User-Facing Messages

- Loading: "Generating [feature]..."
- Success: Display results
- Error: "Error: [user-friendly message]"

### 6. UI/UX Considerations

#### Bootstrap Components

- Forms: `form-control`, `form-label`
- Buttons: `btn btn-primary`, `btn btn-secondary`
- Cards: `card`, `card-body`
- Layout: `container`, `row`, `col-md-*`

#### Loading States

- Spinner: `spinner-border`
- Disable buttons during loading
- Show progress if multi-step

#### Responsive Design

- Mobile-first approach
- Test on different screen sizes
- Use Bootstrap grid system

### 7. Implementation Order

1. Create feature branch
2. Define types in `types.ts`
3. Implement service function in `geminiService.ts`
4. Create component in `components/`
5. Update `App.tsx` routing
6. Test manually
7. Update documentation (`/docs/AI_AGENTS.md`, etc.)
8. Commit with clear message
9. Create PR

### 8. Dependencies

#### Existing Dependencies

- React, TypeScript
- Google Gemini API
- Bootstrap

#### New Dependencies (if any)

- None expected (use existing stack)

### 9. Notes

- All code and documentation in English
- Follow existing patterns in codebase
- Maintain consistency with other features
- Update AI_AGENTS.md is MANDATORY
- Test in local server before committing

### 10. Next Steps After Implementation

1. Manual testing with checklist
2. Documentation review
3. Code self-review
4. Commit and push
5. Create PR with description
6. Request review (if team)

### 11. Rollback Plan

If issues arise:

```bash
git checkout main
git branch -D feature/[feature-name]
```

### 12. Success Criteria

- [ ] Feature works as expected
- [ ] No console errors
- [ ] Documentation updated
- [ ] Code follows project standards
- [ ] User experience is smooth
- [ ] Error handling is robust
