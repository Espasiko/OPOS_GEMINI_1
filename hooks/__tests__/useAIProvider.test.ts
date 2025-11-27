import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useAIProvider } from '../useAIProvider';

// Mock backendService
vi.mock('../../services/backendService', () => ({
  generateSummary: vi.fn(),
  generateMindMap: vi.fn(),
  generateFlashcards: vi.fn(),
}));

describe('useAIProvider Hook', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with default state', () => {
    const { result } = renderHook(() => useAIProvider());
    
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
    expect(result.current.data).toBe(null);
  });

  it('should handle loading state', async () => {
    const { result } = renderHook(() => useAIProvider());
    
    expect(result.current.loading).toBe(false);
    
    // Simulate loading
    result.current.setLoading(true);
    
    await waitFor(() => {
      expect(result.current.loading).toBe(true);
    });
  });

  it('should handle error state', async () => {
    const { result } = renderHook(() => useAIProvider());
    
    const testError = 'Test error';
    result.current.setError(testError);
    
    await waitFor(() => {
      expect(result.current.error).toBe(testError);
    });
  });

  it('should clear error on retry', async () => {
    const { result } = renderHook(() => useAIProvider());
    
    result.current.setError('Error');
    expect(result.current.error).toBe('Error');
    
    result.current.clearError();
    
    await waitFor(() => {
      expect(result.current.error).toBe(null);
    });
  });
});
