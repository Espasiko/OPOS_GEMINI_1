import { useMemo } from 'react';

interface ProviderInfo { name: string }

type ExecFn<T> = (provider: string) => Promise<T>;

export function useAIProvider() {
  // Placeholder: en el futuro leer del contexto de modelo
  const provider = 'groq-8b';
  const providerInfo = useMemo<ProviderInfo>(() => ({ name: 'Proveedor por defecto' }), []);

  async function executeWithRetry<T>(fn: ExecFn<T>): Promise<T> {
    // Sin reintentos por ahora (stub)
    return fn(provider);
  }

  function handleError(err: any): string {
    return (err && (err.message || String(err))) || 'Error desconocido';
  }

  return { provider, providerInfo, executeWithRetry, handleError };
}
