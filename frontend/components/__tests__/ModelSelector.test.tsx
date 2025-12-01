import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ModelSelector from '../ModelSelector';
import { ModelProvider } from '../../contexts/ModelContext';

describe('ModelSelector Component', () => {
  const mockSetSelectedModel = vi.fn();

  const renderWithContext = (selectedModel = 'groq-8b') => {
    return render(
      <ModelProvider value={{ selectedModel, setSelectedModel: mockSetSelectedModel }}>
        <ModelSelector value={selectedModel} onChange={mockSetSelectedModel} />
      </ModelProvider>
    );
  };

  it('renderiza el selector', () => {
    renderWithContext();
    expect(screen.getByRole('combobox')).toBeTruthy();
  });

  it('muestra el modelo actual', () => {
    renderWithContext('groq-8b');
    expect(screen.getByDisplayValue(/groq-8b/i)).toBeTruthy();
  });

  it('llama a setter al cambiar', () => {
    renderWithContext();
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'deepseek-llama' } });
    expect(mockSetSelectedModel).toHaveBeenCalledWith('deepseek-llama');
  });
});
