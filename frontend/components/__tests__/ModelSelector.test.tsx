import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ModelSelector from '../ModelSelector';
import { ModelProvider } from '../../contexts/ModelContext';

describe('ModelSelector Component', () => {
  const mockSetProvider = vi.fn();

  const renderWithContext = (provider = 'groq') => {
    return render(
      <ModelProvider value={{ provider, setProvider: mockSetProvider }}>
        <ModelSelector />
      </ModelProvider>
    );
  };

  it('should render model selector', () => {
    renderWithContext();
    expect(screen.getByRole('combobox')).toBeInTheDocument();
  });

  it('should display current provider', () => {
    renderWithContext('groq');
    expect(screen.getByDisplayValue(/groq/i)).toBeInTheDocument();
  });

  it('should call setProvider on change', () => {
    renderWithContext();
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'deepseek' } });
    expect(mockSetProvider).toHaveBeenCalledWith('deepseek');
  });

  it('should show all available providers', () => {
    renderWithContext();
    const select = screen.getByRole('combobox');
    const options = select.querySelectorAll('option');
    expect(options.length).toBeGreaterThan(3);
  });
});
