import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import App from '../../App';
import ChatView from '../../components/ChatView';
import ModelSelector from '../../components/ModelSelector';
import ErrorMessage from '../../components/ErrorMessage';

expect.extend(toHaveNoViolations);

describe('Accessibility Tests', () => {
  it('App should have no accessibility violations', async () => {
    const { container } = render(<App />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('ChatView should have no accessibility violations', async () => {
    const { container } = render(<ChatView />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('ModelSelector should have no accessibility violations', async () => {
    const { container } = render(<ModelSelector />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('ErrorMessage should have no accessibility violations', async () => {
    const { container } = render(<ErrorMessage message="Test error" />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have proper ARIA labels', () => {
    const { container } = render(<App />);
    
    // Check for ARIA landmarks
    const main = container.querySelector('[role="main"]');
    const navigation = container.querySelector('[role="navigation"]');
    
    expect(main || navigation).toBeTruthy();
  });

  it('should have keyboard navigation support', () => {
    const { container } = render(<ModelSelector />);
    
    // Check for focusable elements
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    expect(focusableElements.length).toBeGreaterThan(0);
  });

  it('should have proper heading hierarchy', () => {
    const { container } = render(<App />);
    
    const h1 = container.querySelector('h1');
    expect(h1).toBeTruthy();
  });

  it('should have alt text for images', () => {
    const { container } = render(<App />);
    
    const images = container.querySelectorAll('img');
    images.forEach(img => {
      expect(img.getAttribute('alt')).toBeTruthy();
    });
  });

  it('should have proper form labels', () => {
    const { container } = render(<ChatView />);
    
    const inputs = container.querySelectorAll('input, textarea');
    inputs.forEach(input => {
      const id = input.getAttribute('id');
      if (id) {
        const label = container.querySelector(`label[for="${id}"]`);
        expect(label || input.getAttribute('aria-label')).toBeTruthy();
      }
    });
  });

  it('should have sufficient color contrast', async () => {
    const { container } = render(<App />);
    const results = await axe(container, {
      rules: {
        'color-contrast': { enabled: true }
      }
    });
    expect(results).toHaveNoViolations();
  });
});
