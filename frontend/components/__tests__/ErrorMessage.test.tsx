import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ErrorMessage from '../ErrorMessage';

describe('ErrorMessage Component', () => {
  it('should render error message', () => {
    render(<ErrorMessage message="Test error" />);
    expect(screen.getByText('Test error')).toBeInTheDocument();
  });

  it('should render with error icon', () => {
    const { container } = render(<ErrorMessage message="Error" />);
    expect(container.querySelector('.error-icon')).toBeInTheDocument();
  });

  it('should handle empty message', () => {
    render(<ErrorMessage message="" />);
    expect(screen.queryByText('')).toBeInTheDocument();
  });

  it('should render long error messages', () => {
    const longMessage = 'A'.repeat(500);
    render(<ErrorMessage message={longMessage} />);
    expect(screen.getByText(longMessage)).toBeInTheDocument();
  });
});
