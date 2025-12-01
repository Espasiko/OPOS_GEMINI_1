import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ErrorMessage from '../ErrorMessage';

describe('ErrorMessage Component', () => {
  it('renderiza el mensaje de error', () => {
    render(<ErrorMessage error="Test error" />);
    expect(screen.getByText('Test error')).toBeTruthy();
  });

  it('renderiza mensaje largo', () => {
    const longMessage = 'A'.repeat(500);
    render(<ErrorMessage error={longMessage} />);
    expect(screen.getByText(longMessage)).toBeTruthy();
  });

  it('acepta mensaje vacío sin romper', () => {
    render(<ErrorMessage error="" />);
  });
});
