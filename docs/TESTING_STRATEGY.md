# Testing Strategy - OpositaIA

## Overview

This document defines the comprehensive testing strategy for OpositaIA, following Context-Driven Development principles and ensuring bulletproof code quality.

## Testing Pyramid

```
        /\
       /  \
      / E2E\
     /______\
    /        \
   /Integration\
  /______________\
 /                \
/   Unit Tests     \
/____________________\
```

## 1. Unit Testing

### Tools

- **Vitest**: Fast unit test runner
- **@testing-library/react**: React component testing
- **@testing-library/user-event**: User interaction simulation

### Coverage Requirements

- **Minimum**: 90% code coverage
- **Target**: 95% code coverage
- **Critical paths**: 100% coverage

### What to Test

#### Services (`frontend/services/backendService.ts`)

- ✅ API key validation
- ✅ Model selection logic
- ✅ Prompt construction
- ✅ Response parsing
- ✅ Error handling
- ✅ Retry logic
- ✅ Timeout handling

#### Components

- ✅ Rendering with different props
- ✅ User interactions
- ✅ State changes
- ✅ Error states
- ✅ Loading states
- ✅ Edge cases

#### Utilities

- ✅ Type guards
- ✅ Data transformations
- ✅ Validation functions

### Example Unit Test Structure

```typescript
// services/__tests__/backendService.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { sendChatMessage } from '../backendService';

describe('backendService', () => {
  describe('sendChatMessage', () => {
    it('should generate a valid practical case', async () => {
      // Arrange
      const mockResponse = {
        /* ... */
      };

      // Act
      const result = await generatePracticalCase();

      // Assert
      expect(result).toBeDefined();
      expect(result.topic).toBeTruthy();
      expect(result.questions).toHaveLength(5);
    });

    it('should handle API errors gracefully', async () => {
      // Arrange
      vi.mock('@google/genai', () => ({
        GoogleGenAI: vi.fn(() => ({
          models: {
            generateContent: vi.fn().mockRejectedValue(new Error('API Error')),
          },
        })),
      }));

      // Act & Assert
      await expect(generatePracticalCase()).rejects.toThrow();
    });
  });
});
```

## 2. Integration Testing

### What to Test

- ✅ Component + Service integration
- ✅ State management flow
- ✅ localStorage persistence
- ✅ API integration (with mocks)
- ✅ Navigation flow

### Example Integration Test

```typescript
// components/__tests__/CaseGeneratorView.integration.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CaseGeneratorView } from '../CaseGeneratorView';

describe('CaseGeneratorView Integration', () => {
  it('should generate and display a practical case', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<CaseGeneratorView {...props} />);

    // Act
    const generateButton = screen.getByRole('button', { name: /generar/i });
    await user.click(generateButton);

    // Assert
    await waitFor(() => {
      expect(screen.getByText(/tema:/i)).toBeInTheDocument();
    });
  });
});
```

## 3. End-to-End Testing

### Tools

- **Playwright**: E2E testing framework
- **@playwright/test**: Test runner

### Critical User Flows

#### Flow 1: Generate Practical Case

1. User opens app
2. Navigates to Case Generator
3. Clicks "Generate"
4. Waits for generation
5. Reviews case
6. Answers questions
7. Submits answers
8. Views results

#### Flow 2: Chat Interaction

1. User opens chat
2. Types question
3. Sends message
4. Receives AI response
5. Continues conversation

#### Flow 3: Create Mind Map

1. User navigates to Mind Map
2. Enters topic
3. Generates map
4. Interacts with nodes
5. Downloads as image

### Example E2E Test

```typescript
// e2e/practical-case.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Practical Case Generation', () => {
  test('should generate and complete a practical case', async ({ page }) => {
    // Navigate to app
    await page.goto('http://localhost:3000');

    // Navigate to Case Generator
    await page.click('text=Generador de Casos');

    // Generate case
    await page.click('button:has-text("Generar Caso")');

    // Wait for generation
    await page.waitForSelector('text=Tema:', { timeout: 30000 });

    // Verify case structure
    const topic = await page.textContent('[data-testid="case-topic"]');
    expect(topic).toBeTruthy();

    // Answer questions
    await page.click('[data-testid="option-A"]');
    await page.click('button:has-text("Siguiente")');

    // Verify progress
    const progress = await page.textContent('[data-testid="progress"]');
    expect(progress).toContain('1/5');
  });
});
```

## 4. Type Safety Testing

### TypeScript Configuration

- ✅ `strict: true`
- ✅ `noImplicitAny: true`
- ✅ `strictNullChecks: true`
- ✅ `strictFunctionTypes: true`

### Type Testing

```typescript
// types/__tests__/types.test.ts
import { describe, it, expectTypeOf } from 'vitest';
import type { PracticalCase, ChatMessage } from '../types';

describe('Type Safety', () => {
  it('should enforce PracticalCase structure', () => {
    const case: PracticalCase = {
      topic: 'Test',
      scenario: 'Test scenario',
      questions: []
    };

    expectTypeOf(case).toMatchTypeOf<PracticalCase>();
  });
});
```

## 5. API Testing

### Gemini API Integration

- ✅ API key validation
- ✅ Rate limiting handling
- ✅ Timeout handling
- ✅ Error response handling
- ✅ Response schema validation

### Mock Strategy

```typescript
// __mocks__/@google/genai.ts
export class GoogleGenAI {
  constructor(config: { apiKey: string }) {}

  models = {
    generateContent: vi.fn().mockResolvedValue({
      text: JSON.stringify({
        /* mock response */
      }),
      response: {
        text: () =>
          JSON.stringify({
            /* mock response */
          }),
      },
    }),
  };
}
```

## 6. Performance Testing

### Metrics to Monitor

- ✅ Initial load time < 3s
- ✅ API response time < 10s
- ✅ Component render time < 100ms
- ✅ Memory usage < 100MB
- ✅ Bundle size < 500KB

### Tools

- Lighthouse CI
- Web Vitals
- React DevTools Profiler

## 7. Accessibility Testing

### Requirements

- ✅ WCAG 2.1 Level AA compliance
- ✅ Keyboard navigation
- ✅ Screen reader support
- ✅ Color contrast ratios
- ✅ Focus management

### Tools

- axe-core
- @testing-library/jest-dom
- Lighthouse accessibility audit

## 8. Security Testing

### Checks

- ✅ API key not exposed in client
- ✅ No XSS vulnerabilities
- ✅ Input sanitization
- ✅ HTTPS only
- ✅ Content Security Policy

## 9. Test Organization

```
/
├── __tests__/              # Global test utilities
│   ├── setup.ts
│   └── helpers.ts
├── services/
│   ├── geminiService.ts
│   └── __tests__/
│       └── geminiService.test.ts
├── components/
│   ├── ChatView.tsx
│   └── __tests__/
│       ├── ChatView.test.tsx
│       └── ChatView.integration.test.tsx
└── e2e/
    ├── practical-case.spec.ts
    ├── chat.spec.ts
    └── mind-map.spec.ts
```

## 10. Continuous Integration

### GitHub Actions Workflow

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '24'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test:unit
      - run: npm run test:integration
      - run: npm run test:e2e
      - run: npm run test:coverage
```

## 11. Test Commands

```json
{
  "scripts": {
    "test": "vitest",
    "test:unit": "vitest run --coverage",
    "test:integration": "vitest run --config vitest.integration.config.ts",
    "test:e2e": "playwright test",
    "test:watch": "vitest watch",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage && open coverage/index.html",
    "type-check": "tsc --noEmit",
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix"
  }
}
```

## 12. Coverage Reports

### Required Coverage

- **Statements**: 90%
- **Branches**: 90%
- **Functions**: 90%
- **Lines**: 90%

### Critical Files (100% coverage required)

- `services/geminiService.ts`
- `types.ts`
- All utility functions

## 13. Testing Checklist

Before merging any PR:

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass
- [ ] Coverage >= 90%
- [ ] No TypeScript errors
- [ ] No ESLint errors
- [ ] Accessibility tests pass
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] CHANGELOG updated

## 14. Test Data Management

### Mock Data Location

```
/__mocks__/
  ├── practicalCases.ts
  ├── chatMessages.ts
  ├── mindMaps.ts
  └── mockExams.ts
```

### Test Fixtures

```typescript
// __mocks__/practicalCases.ts
export const mockPracticalCase: PracticalCase = {
  topic: 'Incapacidad Temporal',
  scenario: 'Un trabajador...',
  questions: [
    /* ... */
  ],
};
```

## 15. Debugging Tests

### VS Code Configuration

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Vitest Tests",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "test:debug"],
      "console": "integratedTerminal"
    }
  ]
}
```

## 16. Best Practices

### DO

- ✅ Write tests before code (TDD)
- ✅ Test behavior, not implementation
- ✅ Use descriptive test names
- ✅ Keep tests isolated
- ✅ Mock external dependencies
- ✅ Test edge cases
- ✅ Test error scenarios

### DON'T

- ❌ Test implementation details
- ❌ Write flaky tests
- ❌ Skip tests
- ❌ Ignore failing tests
- ❌ Over-mock
- ❌ Test third-party libraries

## 17. Maintenance

### Regular Tasks

- Weekly: Review test coverage
- Monthly: Update test dependencies
- Quarterly: Audit test suite performance
- Yearly: Review testing strategy

## 18. Resources

- [Vitest Documentation](https://vitest.dev/)
- [Testing Library](https://testing-library.com/)
- [Playwright](https://playwright.dev/)
- [Context-Driven Testing](http://context-driven-testing.com/)

---

**Last Updated**: 2025-01-16
**Version**: 1.0.0
**Owner**: Development Team
