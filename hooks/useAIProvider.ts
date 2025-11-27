/**
 * useAIProvider Hook - Sprint 10
 * 
 * Hook personalizado para manejar providers de AI con retry automático
 */

import { useModel } from '../contexts/ModelContext';
import { getProviderFromModelId, getProviderInfo, type ProviderInfo } from '../utils/providers';

interface UseAIProviderReturn {
  provider: string;
  providerInfo: ProviderInfo;
  selectedModel: string;
  executeWithRetry: <T>(fn: (provider: string) => Promise<T>, maxRetries?: number) => Promise<T>;
  handleError: (error: unknown) => string;
}

/**
 * Hook personalizado para manejar providers de AI
 * 
 * Proporciona:
 * - Información del provider actual
 * - Función para ejecutar con retry automático
 * - Función para manejar errores con mensajes específicos
 * 
 * @returns Objeto con utilidades para trabajar con providers
 */
export function useAIProvider(): UseAIProviderReturn {
  const { selectedModel } = useModel();
  
  const provider = getProviderFromModelId(selectedModel);
  const providerInfo = getProviderInfo(selectedModel);

  /**
   * Ejecuta una función AI con retry automático
   * 
   * @param fn - Función a ejecutar que recibe el provider
   * @param maxRetries - Número máximo de reintentos (default: 2)
   * @returns Resultado de la función
   * @throws Error si todos los intentos fallan
   */
  async function executeWithRetry<T>(
    fn: (provider: string) => Promise<T>,
    maxRetries = 2
  ): Promise<T> {
    let lastError: Error | null = null;
    
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        return await fn(provider);
      } catch (error) {
        lastError = error instanceof Error ? error : new Error('Error desconocido');
        
        // Si no es el último intento, esperar antes de reintentar
        if (attempt < maxRetries) {
          // Backoff exponencial: 1s, 2s, 4s...
          const delay = 1000 * Math.pow(2, attempt);
          await new Promise(resolve => setTimeout(resolve, delay));
          
          console.log(`Reintentando (${attempt + 1}/${maxRetries})...`);
        }
      }
    }
    
    // Si llegamos aquí, todos los intentos fallaron
    throw lastError;
  }

  /**
   * Maneja errores con mensaje específico del provider
   * 
   * @param error - Error capturado
   * @returns Mensaje de error formateado
   */
  function handleError(error: unknown): string {
    const errorMsg = error instanceof Error ? error.message : 'Error desconocido';
    return `Error con ${providerInfo.name}: ${errorMsg}`;
  }

  return {
    provider,
    providerInfo,
    selectedModel,
    executeWithRetry,
    handleError,
  };
}
